"""Prepare a tiny IAM Handwriting line-level subset for CPU-friendly experiments.

Downloads the `Teklia/IAM-line` dataset from HuggingFace (no IAM credentials
required), randomly samples 200 train / 50 val / 50 test lines, resizes images
to height 32 (with width capped at 256), and caches everything under
`data/iam_tiny/` as PNGs + a `manifest.json` mapping image paths to ground-truth
strings.

The character set is restricted to ASCII visible characters + space (~95
classes). Any line containing characters outside this set is filtered out
before sampling.

Run once, then `experiment.py` and any AI-Scientist-generated variants will
read from the cached folder without touching the network again.
"""

from __future__ import annotations

import argparse
import json
import os
import os.path as osp
import random
import string
from typing import List, Tuple

from PIL import Image

# Lazy-imported to keep top-level fast for --help.
def _load_dataset():
    from datasets import load_dataset

    return load_dataset("Teklia/IAM-line")


# 95 ASCII printable chars (digits, letters, punctuation, space).
ALLOWED_CHARS = set(string.printable[:-6])  # drop \t \n \r \x0b \x0c (and last)
ALLOWED_CHARS.add(" ")


def _is_clean(text: str) -> bool:
    if not text or not text.strip():
        return False
    return all((c in ALLOWED_CHARS) for c in text)


def _resize_to_height(img: Image.Image, target_h: int = 32, max_w: int = 256) -> Image.Image:
    img = img.convert("L")  # grayscale
    w, h = img.size
    if h == 0:
        return img
    new_w = max(1, int(round(w * target_h / h)))
    new_w = min(new_w, max_w)
    return img.resize((new_w, target_h), Image.BILINEAR)


def _split_indices(
    n_total: int, n_train: int, n_val: int, n_test: int, seed: int
) -> Tuple[List[int], List[int], List[int]]:
    rng = random.Random(seed)
    idxs = list(range(n_total))
    rng.shuffle(idxs)
    train = idxs[:n_train]
    val = idxs[n_train : n_train + n_val]
    test = idxs[n_train + n_val : n_train + n_val + n_test]
    return train, val, test


def _materialise_split(ds, indices, split_name: str, out_root: str) -> List[dict]:
    split_dir = osp.join(out_root, split_name)
    os.makedirs(split_dir, exist_ok=True)
    records = []
    for local_i, src_i in enumerate(indices):
        sample = ds[int(src_i)]
        text = sample["text"]
        img: Image.Image = sample["image"]
        img = _resize_to_height(img)
        fname = f"{split_name}_{local_i:05d}.png"
        out_path = osp.join(split_dir, fname)
        img.save(out_path, format="PNG")
        records.append(
            {
                "image": osp.relpath(out_path, out_root).replace("\\", "/"),
                "text": text,
                "width": img.size[0],
                "height": img.size[1],
            }
        )
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out_root", type=str, default="data/iam_tiny")
    parser.add_argument("--n_train", type=int, default=200)
    parser.add_argument("--n_val", type=int, default=50)
    parser.add_argument("--n_test", type=int, default=50)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    out_root = args.out_root
    manifest_path = osp.join(out_root, "manifest.json")
    if osp.exists(manifest_path):
        print(f"[prepare_iam_tiny] {manifest_path} already exists; skipping.")
        return

    print("[prepare_iam_tiny] Loading Teklia/IAM-line from HuggingFace ...")
    raw = _load_dataset()
    # Use the train split as the candidate pool; we re-split ourselves to
    # guarantee disjoint tiny train/val/test.
    pool = raw["train"]

    print(f"[prepare_iam_tiny] Raw pool size: {len(pool)}; filtering by character set ...")
    keep = [i for i, ex in enumerate(pool) if _is_clean(ex["text"])]
    print(f"[prepare_iam_tiny] After filter: {len(keep)} usable lines.")

    needed = args.n_train + args.n_val + args.n_test
    if len(keep) < needed:
        raise RuntimeError(
            f"Not enough clean samples: have {len(keep)}, need {needed}."
        )

    rng = random.Random(args.seed)
    rng.shuffle(keep)
    keep = keep[:needed]

    train_idx, val_idx, test_idx = _split_indices(
        n_total=len(keep),
        n_train=args.n_train,
        n_val=args.n_val,
        n_test=args.n_test,
        seed=args.seed,
    )

    os.makedirs(out_root, exist_ok=True)

    # Map back to dataset indices.
    train_src = [keep[i] for i in train_idx]
    val_src = [keep[i] for i in val_idx]
    test_src = [keep[i] for i in test_idx]

    print(f"[prepare_iam_tiny] Materialising train/{len(train_src)} ...")
    train_records = _materialise_split(pool, train_src, "train", out_root)
    print(f"[prepare_iam_tiny] Materialising val/{len(val_src)} ...")
    val_records = _materialise_split(pool, val_src, "val", out_root)
    print(f"[prepare_iam_tiny] Materialising test/{len(test_src)} ...")
    test_records = _materialise_split(pool, test_src, "test", out_root)

    # Build the character vocabulary observed in the train split (deterministic).
    charset = sorted({c for r in train_records for c in r["text"]})

    manifest = {
        "image_height": 32,
        "max_image_width": 256,
        "charset": charset,
        "splits": {
            "train": train_records,
            "val": val_records,
            "test": test_records,
        },
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(
        f"[prepare_iam_tiny] Done. {len(train_records)} train / "
        f"{len(val_records)} val / {len(test_records)} test, "
        f"|charset|={len(charset)} -> {manifest_path}"
    )


if __name__ == "__main__":
    main()
