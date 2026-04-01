#!/usr/bin/env python3
"""
Plot comparison charts: Regular Test vs Hard Test for Nepali complaint classifier.
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    precision_recall_fscore_support, accuracy_score, f1_score, confusion_matrix
)

# ── paths ─────────────────────────────────────────────────────────────────────
BASE      = os.path.dirname(__file__)
REG_DIR   = os.path.join(BASE, "analysis")
HARD_DIR  = os.path.join(BASE, "analysis", "hard_test_plots")
OUT_DIR   = os.path.join(BASE, "analysis", "comparison_plots")
os.makedirs(OUT_DIR, exist_ok=True)

LABEL_NAMES = ["electricity", "water", "road", "garbage"]

# ── load arrays ───────────────────────────────────────────────────────────────
reg_labels = np.load(os.path.join(REG_DIR,  "test_labels.npy"))
reg_preds  = np.load(os.path.join(REG_DIR,  "test_preds.npy"))
reg_probs  = np.load(os.path.join(REG_DIR,  "test_probs.npy"))

hard_labels = np.load(os.path.join(HARD_DIR, "test_labels.npy"))
hard_preds  = np.load(os.path.join(HARD_DIR, "test_preds.npy"))
hard_probs  = np.load(os.path.join(HARD_DIR, "test_probs.npy"))

# ── compute per-class metrics ─────────────────────────────────────────────────
def class_metrics(labels, preds):
    p, r, f, _ = precision_recall_fscore_support(
        labels, preds, labels=range(len(LABEL_NAMES))
    )
    return p, r, f

reg_p,  reg_r,  reg_f  = class_metrics(reg_labels,  reg_preds)
hard_p, hard_r, hard_f = class_metrics(hard_labels, hard_preds)

reg_acc  = accuracy_score(reg_labels,  reg_preds)
hard_acc = accuracy_score(hard_labels, hard_preds)
reg_f1   = f1_score(reg_labels,  reg_preds, average="weighted")
hard_f1  = f1_score(hard_labels, hard_preds, average="weighted")

PALETTE = {"regular": "#4C9BE8", "hard": "#E85454"}
x  = np.arange(len(LABEL_NAMES))
w  = 0.33

# ═══════════════════════════════════════════════════════════════════════════════
# 1.  Side-by-side: F1 per class
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x - w/2, reg_f,  w, label=f"Regular Test (n=1029)", color=PALETTE["regular"], edgecolor="white")
ax.bar(x + w/2, hard_f, w, label=f"Hard Test    (n=40)",   color=PALETTE["hard"],    edgecolor="white")
ax.set_xticks(x); ax.set_xticklabels(LABEL_NAMES)
ax.set_ylabel("F1-score"); ax.set_ylim(0, 1.12)
ax.set_title("Per-class F1 — Regular Test vs Hard Test")
ax.legend(); ax.grid(axis="y", linestyle="--", alpha=0.5)
for i, (rv, hv) in enumerate(zip(reg_f, hard_f)):
    ax.text(i - w/2, rv + 0.02, f"{rv:.2f}", ha="center", fontsize=9, color=PALETTE["regular"])
    ax.text(i + w/2, hv + 0.02, f"{hv:.2f}", ha="center", fontsize=9, color=PALETTE["hard"])
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "f1_comparison.png"), dpi=150)
plt.close()
print("Saved: f1_comparison.png")

# ═══════════════════════════════════════════════════════════════════════════════
# 2.  Grouped: Precision + Recall + F1 for both tests  (2 subplots)
# ═══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
for ax, (p, r, f, title) in zip(
    axes,
    [
        (reg_p,  reg_r,  reg_f,  "Regular Test"),
        (hard_p, hard_r, hard_f, "Hard Test"),
    ]
):
    ax.bar(x - w, p, w, label="Precision", color="#4C9BE8", edgecolor="white")
    ax.bar(x,     r, w, label="Recall",    color="#4CAF50", edgecolor="white")
    ax.bar(x + w, f, w, label="F1-score",  color="#E85454", edgecolor="white")
    ax.set_xticks(x); ax.set_xticklabels(LABEL_NAMES, rotation=15)
    ax.set_title(title, fontsize=13)
    ax.set_ylabel("Score"); ax.set_ylim(0, 1.12)
    ax.legend(fontsize=9); ax.grid(axis="y", linestyle="--", alpha=0.5)
    for i, (pv, rv, fv) in enumerate(zip(p, r, f)):
        ax.text(i - w, pv + 0.02, f"{pv:.2f}", ha="center", fontsize=7.5)
        ax.text(i,     rv + 0.02, f"{rv:.2f}", ha="center", fontsize=7.5)
        ax.text(i + w, fv + 0.02, f"{fv:.2f}", ha="center", fontsize=7.5)
fig.suptitle("Precision / Recall / F1 — Regular Test vs Hard Test", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "prf_comparison.png"), dpi=150)
plt.close()
print("Saved: prf_comparison.png")

# ═══════════════════════════════════════════════════════════════════════════════
# 3.  Overall Accuracy & weighted F1 bar (single chart)
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7, 5))
metrics = ["Accuracy", "F1 (weighted)"]
reg_vals  = [reg_acc,  reg_f1]
hard_vals = [hard_acc, hard_f1]
xi = np.arange(len(metrics))
ax.bar(xi - 0.2, reg_vals,  0.35, label="Regular Test", color=PALETTE["regular"], edgecolor="white")
ax.bar(xi + 0.2, hard_vals, 0.35, label="Hard Test",    color=PALETTE["hard"],    edgecolor="white")
ax.set_xticks(xi); ax.set_xticklabels(metrics)
ax.set_ylim(0, 1.15); ax.set_ylabel("Score")
ax.set_title("Overall Accuracy & F1 — Regular vs Hard Test")
ax.legend(); ax.grid(axis="y", linestyle="--", alpha=0.5)
for i, (rv, hv) in enumerate(zip(reg_vals, hard_vals)):
    ax.text(i - 0.2, rv + 0.02, f"{rv:.4f}", ha="center", fontsize=10, color=PALETTE["regular"], fontweight="bold")
    ax.text(i + 0.2, hv + 0.02, f"{hv:.4f}", ha="center", fontsize=10, color=PALETTE["hard"],    fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "overall_comparison.png"), dpi=150)
plt.close()
print("Saved: overall_comparison.png")

# ═══════════════════════════════════════════════════════════════════════════════
# 4.  Side-by-side confusion matrices
# ═══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
for ax, (labels, preds, title, cmap) in zip(
    axes,
    [
        (reg_labels,  reg_preds,  "Regular Test Confusion Matrix",  "Blues"),
        (hard_labels, hard_preds, "Hard Test Confusion Matrix",     "Reds"),
    ]
):
    cm = confusion_matrix(labels, preds)
    sns.heatmap(
        cm, annot=True, fmt="d",
        xticklabels=LABEL_NAMES, yticklabels=LABEL_NAMES,
        cmap=cmap, linewidths=0.5, ax=ax
    )
    ax.set_xlabel("Predicted"); ax.set_ylabel("True")
    ax.set_title(title, fontsize=13)
plt.suptitle("Confusion Matrices — Regular Test vs Hard Test", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "confusion_matrix_comparison.png"), dpi=150)
plt.close()
print("Saved: confusion_matrix_comparison.png")

# ═══════════════════════════════════════════════════════════════════════════════
# 5.  Confidence distribution: mean predicted probability of correct class
# ═══════════════════════════════════════════════════════════════════════════════
reg_correct_conf  = reg_probs[np.arange(len(reg_labels)),  reg_labels]
hard_correct_conf = hard_probs[np.arange(len(hard_labels)), hard_labels]

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(reg_correct_conf,  bins=30, alpha=0.65, label=f"Regular Test  (n=1029)", color=PALETTE["regular"])
ax.hist(hard_correct_conf, bins=15, alpha=0.65, label=f"Hard Test     (n=40)",   color=PALETTE["hard"])
ax.set_xlabel("Confidence for True Class")
ax.set_ylabel("Frequency")
ax.set_title("Model Confidence on True Class — Regular vs Hard Test")
ax.legend(); ax.grid(linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "confidence_comparison.png"), dpi=150)
plt.close()
print("Saved: confidence_comparison.png")

print(f"\nAll comparison plots saved to: {OUT_DIR}")
print(f"\nSummary:")
print(f"  Regular Test  — Accuracy: {reg_acc:.4f}  |  F1: {reg_f1:.4f}")
print(f"  Hard Test     — Accuracy: {hard_acc:.4f}  |  F1: {hard_f1:.4f}")
