#!/usr/bin/env python3
"""
CivicConnect — Nepali Hard Test Evaluation
Evaluates the trained multilingual DistilBERT model against a challenging
out-of-distribution test set (short, ambiguous, cross-category complaints).
"""

import os
import numpy as np
import pandas as pd
import torch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import DistilBertForSequenceClassification, DistilBertTokenizerFast
from sklearn.metrics import (
    classification_report, confusion_matrix,
    accuracy_score, f1_score, precision_recall_fscore_support
)

# ============================================================
# CONFIG
# ============================================================
MODEL_DIR  = os.path.join(os.path.dirname(__file__), "best_model")
TEST_FILE  = os.path.join(os.path.dirname(__file__), "data", "hard_test.csv")
OUT_DIR    = os.path.join(os.path.dirname(__file__), "analysis", "hard_test_plots")
REPORT_OUT = os.path.join(os.path.dirname(__file__), "analysis", "hard_test_report.txt")

os.makedirs(OUT_DIR, exist_ok=True)

# ============================================================
# 1. Load model & tokenizer
# ============================================================
print("Loading model and tokenizer...")
tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_DIR)
model     = DistilBertForSequenceClassification.from_pretrained(MODEL_DIR)

with open(os.path.join(MODEL_DIR, "labels.txt")) as f:
    label_names = [line.strip() for line in f]

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()
print(f"  Device : {device}")
print(f"  Labels : {label_names}\n")

# ============================================================
# 2. Load hard test data
# ============================================================
df = pd.read_csv(TEST_FILE)
texts            = df["text"].tolist()
true_labels_text = df["label"].tolist()

label2idx  = {label: i for i, label in enumerate(label_names)}
true_labels = np.array([label2idx[l] for l in true_labels_text])

# ============================================================
# 3. Predict
# ============================================================
enc = tokenizer(
    texts,
    padding=True,
    truncation=True,
    max_length=128,
    return_tensors="pt"
).to(device)

with torch.no_grad():
    outputs = model(**enc)
    probs   = torch.nn.functional.softmax(outputs.logits, dim=-1).cpu().numpy()
    preds   = np.argmax(probs, axis=1)

# ============================================================
# 4. Metrics
# ============================================================
acc = accuracy_score(true_labels, preds)
f1  = f1_score(true_labels, preds, average="weighted")
report = classification_report(true_labels, preds, target_names=label_names, digits=4)

print(f"Hard Test Accuracy : {acc:.4f}")
print(f"Hard Test F1 (weighted) : {f1:.4f}\n")
print("Classification Report:")
print(report)

# Save report
with open(REPORT_OUT, "w", encoding="utf-8") as f:
    f.write("CivicConnect — Nepali Hard Test Report\n")
    f.write(f"Model: distilbert-base-multilingual-cased\n")
    f.write(f"Hard Test Accuracy       : {acc:.4f}\n")
    f.write(f"Hard Test F1 (weighted)  : {f1:.4f}\n\n")
    f.write(report)
    f.write("\n\nPer-sample predictions:\n")
    f.write(f"{'Text':<60}  {'True':<12}  {'Predicted':<12}  {'Conf':>6}\n")
    f.write("-" * 100 + "\n")
    for text, true_idx, pred_idx, prob_row in zip(texts, true_labels, preds, probs):
        true_name = label_names[true_idx]
        pred_name = label_names[pred_idx]
        conf      = prob_row[pred_idx]
        marker    = "" if true_idx == pred_idx else "  <-- WRONG"
        f.write(f"{text[:58]:<60}  {true_name:<12}  {pred_name:<12}  {conf:>6.3f}{marker}\n")

print(f"Report saved to: {REPORT_OUT}")

# ============================================================
# 5. Confusion matrix
# ============================================================
cm = confusion_matrix(true_labels, preds)
plt.figure(figsize=(8, 6))
sns.heatmap(
    cm, annot=True, fmt="d",
    xticklabels=label_names, yticklabels=label_names,
    cmap="Reds", linewidths=0.5
)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Nepali Hard Test — Confusion Matrix")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "confusion_matrix.png"), dpi=150)
plt.close()

# ============================================================
# 6. Per-class Precision / Recall / F1 bar chart
# ============================================================
precision, recall, f1_scores, _ = precision_recall_fscore_support(
    true_labels, preds, labels=range(len(label_names))
)
x = np.arange(len(label_names))
width = 0.22

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x - width, precision, width, label="Precision", color="#4C9BE8")
ax.bar(x,         recall,    width, label="Recall",    color="#4CAF50")
ax.bar(x + width, f1_scores, width, label="F1-score",  color="#E85454")
ax.set_xticks(x)
ax.set_xticklabels(label_names)
ax.set_ylabel("Score")
ax.set_ylim(0, 1.05)
ax.set_title("Hard Test — Per-class Precision / Recall / F1")
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "class_metrics.png"), dpi=150)
plt.close()

# ============================================================
# 7. Predicted probability distribution per class
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))
colors = ["#4C9BE8", "#FF9F43", "#4CAF50", "#E85454"]
for i, (label, color) in enumerate(zip(label_names, colors)):
    ax.hist(probs[:, i], bins=20, alpha=0.55, label=label, color=color)
ax.set_xlabel("Predicted Probability")
ax.set_ylabel("Frequency")
ax.set_title("Hard Test — Predicted Probability Distribution per Class")
ax.legend()
ax.grid(linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "probabilities_hist.png"), dpi=150)
plt.close()

# ============================================================
# 8. Save raw arrays for further analysis
# ============================================================
np.save(os.path.join(OUT_DIR, "test_labels.npy"), true_labels)
np.save(os.path.join(OUT_DIR, "test_preds.npy"),  preds)
np.save(os.path.join(OUT_DIR, "test_probs.npy"),  probs)

print(f"\nAll hard-test plots saved to: {OUT_DIR}")
