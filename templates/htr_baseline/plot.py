"""Plot training/validation curves and final metrics across runs.

Reads every `run_*/all_results.npy` and `run_*/final_info.json` produced by
`experiment.py` and renders:
  - train_loss_iam_tiny.png
  - val_loss_iam_tiny.png
  - val_cer_iam_tiny.png
  - test_metrics_bar.png
"""

import json
import os
import os.path as osp

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

DATASET = "iam_tiny"

folders = [f for f in os.listdir("./") if f.startswith("run") and osp.isdir(f)]
folders.sort()

histories = {}
finals = {}
for folder in folders:
    hist_path = osp.join(folder, "all_results.npy")
    final_path = osp.join(folder, "final_info.json")
    if osp.exists(hist_path):
        histories[folder] = np.load(hist_path, allow_pickle=True).item()
    if osp.exists(final_path):
        with open(final_path, "r", encoding="utf-8") as f:
            finals[folder] = json.load(f)

# Add new entries here when AI-Scientist creates additional runs (run_1, run_2, ...).
labels = {folder: ("Baseline" if folder == "run_0" else folder) for folder in folders}


def palette(n):
    cmap = plt.get_cmap("tab10")
    return [mcolors.rgb2hex(cmap(i % 10)) for i in range(n)]


colors = palette(len(folders))


def _curve_plot(metric: str, ylabel: str, fname: str):
    plt.figure(figsize=(8, 5))
    for i, folder in enumerate(folders):
        h = histories.get(folder)
        if not h or DATASET not in h:
            continue
        epochs = h[DATASET].get("epochs", [])
        ys = h[DATASET].get(metric, [])
        if not epochs or not ys:
            continue
        plt.plot(epochs, ys, marker="o", label=labels[folder], color=colors[i])
    plt.xlabel("Epoch")
    plt.ylabel(ylabel)
    plt.title(f"{ylabel} on {DATASET}")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(fname)
    plt.close()


_curve_plot("train_loss", "Train CTC loss", f"train_loss_{DATASET}.png")
_curve_plot("val_loss", "Validation CTC loss", f"val_loss_{DATASET}.png")
_curve_plot("val_cer", "Validation CER", f"val_cer_{DATASET}.png")

# Bar chart of test CER / WER across runs.
if finals:
    runs = list(finals.keys())
    cers = [finals[r]["iam_tiny_test"]["means"]["CER"] for r in runs]
    wers = [finals[r]["iam_tiny_test"]["means"]["WER"] for r in runs]
    x = np.arange(len(runs))
    plt.figure(figsize=(max(6, 1.2 * len(runs)), 5))
    plt.bar(x - 0.2, cers, width=0.4, label="CER")
    plt.bar(x + 0.2, wers, width=0.4, label="WER")
    plt.xticks(x, [labels[r] for r in runs], rotation=30, ha="right")
    plt.ylabel("Error rate")
    plt.title("Test CER / WER across runs")
    plt.grid(True, axis="y", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("test_metrics_bar.png")
    plt.close()

print("[plot] Wrote train_loss / val_loss / val_cer / test_metrics_bar PNGs.")
