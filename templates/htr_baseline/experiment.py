"""Lightweight CRNN+CTC baseline for handwritten line recognition (IAM tiny).

This script is intentionally small and CPU-friendly so AI-Scientist can iterate
on it within minutes per run. It is invoked as:

    python experiment.py --out_dir run_X

and writes:

    {out_dir}/final_info.json   # required by AI-Scientist (dict-of-{means: ...})
    {out_dir}/all_results.npy   # per-step training curves used by plot.py

The model is a tiny CNN -> AdaptiveAvgPool(H=1) -> 1-layer BiLSTM -> Linear
trained with CTC loss on `data/iam_tiny/`. Decoding is greedy.

AI-Scientist is encouraged to modify the model architecture, augmentations,
optimizer, scheduler, decoder, or training loop -- but should NOT swap the
dataset, change `final_info.json` keys, or remove the wall-clock guard
(default 15 min per run).
"""

from __future__ import annotations

import argparse
import json
import os
import os.path as osp
import time
from typing import Dict, List, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
from torch.utils.data import DataLoader, Dataset

# --------------------------- data ---------------------------

def _find_data_root() -> str:
    """Locate `data/iam_tiny/manifest.json` by walking up from the current dir.

    AI-Scientist copies this template into `results/htr_baseline/<idea>/` so the
    relative path to the prepared dataset depends on the runtime location.
    Walking up parent directories is a robust way to find the cached data
    regardless of where `python experiment.py` is invoked from.
    """
    here = osp.abspath(os.getcwd())
    for _ in range(6):
        candidate = osp.join(here, "data", "iam_tiny", "manifest.json")
        if osp.exists(candidate):
            return osp.dirname(candidate)
        parent = osp.dirname(here)
        if parent == here:
            break
        here = parent
    # Fallback to the conventional location relative to the template folder.
    return osp.join("..", "..", "data", "iam_tiny")


DATA_ROOT = _find_data_root()


class IAMTinyDataset(Dataset):
    def __init__(self, manifest_path: str, split: str, char_to_idx: Dict[str, int]):
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        self.records = manifest["splits"][split]
        self.root = osp.dirname(manifest_path)
        self.char_to_idx = char_to_idx
        self.image_height = manifest["image_height"]
        self.max_image_width = manifest["max_image_width"]

    def __len__(self) -> int:
        return len(self.records)

    def __getitem__(self, idx: int):
        rec = self.records[idx]
        img = Image.open(osp.join(self.root, rec["image"])).convert("L")
        # Pad-to-max-width keeps batching simple (alternative: bucketed sorting).
        w, h = img.size
        if w > self.max_image_width:
            img = img.resize((self.max_image_width, h), Image.BILINEAR)
            w = self.max_image_width
        canvas = Image.new("L", (self.max_image_width, h), color=255)
        canvas.paste(img, (0, 0))
        arr = np.array(canvas, dtype=np.float32) / 255.0
        arr = (arr - 0.5) / 0.5  # normalise to [-1, 1]
        tensor = torch.from_numpy(arr).unsqueeze(0)  # (1, H, W)

        target = torch.tensor(
            [self.char_to_idx[c] for c in rec["text"] if c in self.char_to_idx],
            dtype=torch.long,
        )
        return tensor, target, rec["text"], w


def collate(batch):
    imgs = torch.stack([b[0] for b in batch], dim=0)  # (B, 1, H, Wmax)
    targets = [b[1] for b in batch]
    target_lengths = torch.tensor([len(t) for t in targets], dtype=torch.long)
    targets_concat = torch.cat(targets, dim=0) if len(targets) else torch.empty(0, dtype=torch.long)
    texts = [b[2] for b in batch]
    actual_widths = [b[3] for b in batch]
    return imgs, targets_concat, target_lengths, texts, actual_widths


# --------------------------- model ---------------------------


class TinyCRNN(nn.Module):
    """Small CNN -> BiLSTM -> Linear. ~0.5M parameters, CPU-friendly.

    Pooling is height-only after the first block so the encoder emits a
    long enough sequence for CTC to align with line transcripts. The
    blank-class bias is initialised to a negative value to discourage the
    classic all-blank local minimum that small CTC models fall into when
    trained on tiny datasets.
    """

    def __init__(self, num_classes: int, lstm_hidden: int = 128, blank_idx: int = 0):
        super().__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d((2, 2)),       # H 32 -> 16, W /2
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d((2, 1)),       # H 16 -> 8 (width preserved)
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d((2, 1)),       # H 8 -> 4
            nn.AdaptiveAvgPool2d((1, None)),  # H -> 1
        )
        self.lstm = nn.LSTM(
            input_size=128, hidden_size=lstm_hidden, num_layers=1, bidirectional=True
        )
        self.classifier = nn.Linear(2 * lstm_hidden, num_classes)
        # Bias the blank class negative so the network prefers emitting
        # real characters early in training (escapes the all-blank minimum).
        with torch.no_grad():
            self.classifier.bias.zero_()
            self.classifier.bias[blank_idx] = -2.0
        # Width downsample factor (only the first MaxPool halves W).
        self.width_downsample = 2

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (B, 1, H, W)
        feat = self.cnn(x)  # (B, C, 1, W')
        feat = feat.squeeze(2)  # (B, C, W')
        feat = feat.permute(2, 0, 1)  # (W', B, C)
        out, _ = self.lstm(feat)  # (W', B, 2*hidden)
        logits = self.classifier(out)  # (W', B, num_classes)
        return logits


# --------------------------- decoding & metrics ---------------------------


def greedy_decode(log_probs: torch.Tensor, idx_to_char: List[str], blank_idx: int) -> List[str]:
    # log_probs: (T, B, C)
    preds = log_probs.argmax(dim=-1).t()  # (B, T)
    decoded = []
    for row in preds.tolist():
        prev = -1
        chars = []
        for p in row:
            if p != prev and p != blank_idx:
                chars.append(idx_to_char[p])
            prev = p
        decoded.append("".join(chars))
    return decoded


def compute_cer_wer(preds: List[str], refs: List[str]) -> Tuple[float, float]:
    # Lazy-import to keep a clean error if jiwer is missing.
    import jiwer  # type: ignore

    # jiwer raises on empty refs/preds; pre-filter.
    pairs = [(p, r) for p, r in zip(preds, refs) if r.strip()]
    if not pairs:
        return 1.0, 1.0
    p_list, r_list = zip(*pairs)
    cer = jiwer.cer(list(r_list), list(p_list))
    wer = jiwer.wer(list(r_list), list(p_list))
    return float(cer), float(wer)


# --------------------------- training ---------------------------


def build_charset(manifest_path: str) -> Tuple[List[str], Dict[str, int]]:
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    # Index 0 is reserved for the CTC blank.
    chars = ["<blank>"] + manifest["charset"]
    char_to_idx = {c: i for i, c in enumerate(chars)}
    return chars, char_to_idx


def train_one_epoch(model, loader, optimizer, ctc_loss, device):
    model.train()
    total_loss = 0.0
    n_batches = 0
    for imgs, targets, target_lengths, _texts, _widths in loader:
        imgs = imgs.to(device)
        targets = targets.to(device)
        target_lengths = target_lengths.to(device)
        logits = model(imgs)  # (T, B, C)
        log_probs = F.log_softmax(logits, dim=-1)
        T = log_probs.size(0)
        B = log_probs.size(1)
        input_lengths = torch.full((B,), T, dtype=torch.long, device=device)
        loss = ctc_loss(log_probs, targets, input_lengths, target_lengths)
        optimizer.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), 5.0)
        optimizer.step()
        total_loss += float(loss.item())
        n_batches += 1
    return total_loss / max(1, n_batches)


@torch.no_grad()
def evaluate(model, loader, idx_to_char, blank_idx, device) -> Dict[str, float]:
    model.eval()
    all_preds: List[str] = []
    all_refs: List[str] = []
    losses = []
    ctc = nn.CTCLoss(blank=blank_idx, zero_infinity=True)
    for imgs, targets, target_lengths, texts, _widths in loader:
        imgs = imgs.to(device)
        logits = model(imgs)
        log_probs = F.log_softmax(logits, dim=-1)
        T, B, _ = log_probs.shape
        if targets.numel() > 0:
            input_lengths = torch.full((B,), T, dtype=torch.long, device=device)
            losses.append(
                float(
                    ctc(
                        log_probs,
                        targets.to(device),
                        input_lengths,
                        target_lengths.to(device),
                    ).item()
                )
            )
        preds = greedy_decode(log_probs.cpu(), idx_to_char, blank_idx)
        all_preds.extend(preds)
        all_refs.extend(texts)
    cer, wer = compute_cer_wer(all_preds, all_refs)
    return {
        "loss": float(np.mean(losses)) if losses else 0.0,
        "CER": cer,
        "WER": wer,
        "n": float(len(all_refs)),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out_dir", type=str, required=True)
    parser.add_argument("--data_root", type=str, default=DATA_ROOT)
    parser.add_argument("--epochs", type=int, default=8)
    parser.add_argument("--batch_size", type=int, default=16)
    parser.add_argument("--lr", type=float, default=5e-4)
    parser.add_argument("--weight_decay", type=float, default=1e-4)
    parser.add_argument("--lstm_hidden", type=int, default=128)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--max_train_minutes",
        type=float,
        default=15.0,
        help="Wall-clock guard. Training stops early when exceeded.",
    )
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    device = torch.device("cpu")

    manifest_path = osp.join(args.data_root, "manifest.json")
    if not osp.exists(manifest_path):
        raise FileNotFoundError(
            f"{manifest_path} not found. Run prepare_iam_tiny.py first."
        )

    idx_to_char, char_to_idx = build_charset(manifest_path)
    blank_idx = 0
    num_classes = len(idx_to_char)

    train_ds = IAMTinyDataset(manifest_path, "train", char_to_idx)
    val_ds = IAMTinyDataset(manifest_path, "val", char_to_idx)
    test_ds = IAMTinyDataset(manifest_path, "test", char_to_idx)
    train_loader = DataLoader(
        train_ds,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=0,
        collate_fn=collate,
    )
    val_loader = DataLoader(
        val_ds, batch_size=args.batch_size, shuffle=False, num_workers=0, collate_fn=collate
    )
    test_loader = DataLoader(
        test_ds, batch_size=args.batch_size, shuffle=False, num_workers=0, collate_fn=collate
    )

    model = TinyCRNN(
        num_classes=num_classes,
        lstm_hidden=args.lstm_hidden,
        blank_idx=blank_idx,
    ).to(device)
    optimizer = torch.optim.AdamW(
        model.parameters(), lr=args.lr, weight_decay=args.weight_decay
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=args.epochs, eta_min=args.lr * 0.05
    )
    ctc_loss = nn.CTCLoss(blank=blank_idx, zero_infinity=True)

    history = {
        "iam_tiny": {
            "epochs": [],
            "train_loss": [],
            "val_loss": [],
            "val_cer": [],
            "val_wer": [],
        }
    }

    t_start = time.time()
    early_stopped = False
    for epoch in range(1, args.epochs + 1):
        train_loss = train_one_epoch(model, train_loader, optimizer, ctc_loss, device)
        scheduler.step()
        val_metrics = evaluate(model, val_loader, idx_to_char, blank_idx, device)
        elapsed = (time.time() - t_start) / 60.0
        print(
            f"[epoch {epoch}/{args.epochs}] train_loss={train_loss:.4f} "
            f"val_loss={val_metrics['loss']:.4f} val_CER={val_metrics['CER']:.4f} "
            f"val_WER={val_metrics['WER']:.4f} "
            f"lr={optimizer.param_groups[0]['lr']:.5f} elapsed_min={elapsed:.2f}"
        )
        history["iam_tiny"]["epochs"].append(epoch)
        history["iam_tiny"]["train_loss"].append(train_loss)
        history["iam_tiny"]["val_loss"].append(val_metrics["loss"])
        history["iam_tiny"]["val_cer"].append(val_metrics["CER"])
        history["iam_tiny"]["val_wer"].append(val_metrics["WER"])

        if elapsed >= args.max_train_minutes:
            print(
                f"[wall-clock guard] Reached {elapsed:.2f} min >= "
                f"{args.max_train_minutes} min; stopping early."
            )
            early_stopped = True
            break

    train_time_sec = time.time() - t_start
    test_metrics = evaluate(model, test_loader, idx_to_char, blank_idx, device)
    print(
        f"[test] CER={test_metrics['CER']:.4f} WER={test_metrics['WER']:.4f} "
        f"loss={test_metrics['loss']:.4f}"
    )

    # Required by AI-Scientist: dict-of-{means: ...}.
    final_info = {
        "iam_tiny_test": {
            "means": {
                "CER": float(test_metrics["CER"]),
                "WER": float(test_metrics["WER"]),
                "test_loss": float(test_metrics["loss"]),
                "train_time_sec": float(train_time_sec),
                "epochs_completed": float(history["iam_tiny"]["epochs"][-1])
                if history["iam_tiny"]["epochs"]
                else 0.0,
                "early_stopped": float(1.0 if early_stopped else 0.0),
            }
        }
    }
    with open(osp.join(args.out_dir, "final_info.json"), "w", encoding="utf-8") as f:
        json.dump(final_info, f, indent=2)

    # Per-step curves for plot.py
    np.save(osp.join(args.out_dir, "all_results.npy"), history)

    print(f"[done] Wrote {args.out_dir}/final_info.json and all_results.npy")


if __name__ == "__main__":
    main()
