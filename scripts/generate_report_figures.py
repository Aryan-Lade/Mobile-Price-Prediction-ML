import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Setup paths
PROJECT_ROOT = Path("c:/Users/wwa90/OneDrive/Desktop/MLProject")
REPORTS_DIR = PROJECT_ROOT / "reports"
FIG_DIR = REPORTS_DIR / "report_figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Load evaluation data
curves_data_path = PROJECT_ROOT / "ml" / "outputs" / "06_evaluation_and_curves_data.json"
tuning_data_path = PROJECT_ROOT / "ml" / "outputs" / "05_hyperparameter_tuning_results.json"

with open(curves_data_path, "r", encoding="utf-8") as f:
    curves_data = json.load(f)

with open(tuning_data_path, "r", encoding="utf-8") as f:
    tuning_data = json.load(f)

plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

# ==========================================
# Figure 1: Grouped Bar Chart (Friend style)
# ==========================================
fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=300)

models = ['Random Forest', 'SVM', 'Logistic Reg.', 'KNN']
acc = [0.8265, 0.8010, 0.7857, 0.7959]
macro_f1 = [0.7996, 0.7807, 0.7639, 0.7638]
roc_auc = [0.9613, 0.9591, 0.9451, 0.9517]

x = np.arange(len(models))
width = 0.22

rects1 = ax.bar(x - width, acc, width, label='Accuracy', color='#1e3d59')
rects2 = ax.bar(x, macro_f1, width, label='Macro F1', color='#3895d3')
rects3 = ax.bar(x + width, roc_auc, width, label='ROC AUC', color='#a8c8e8')

ax.set_ylabel('Score', fontsize=10, color='#333333')
ax.set_xticks(x)
ax.set_xticklabels(models, fontsize=9.5)
ax.legend(frameon=False, loc='upper right', fontsize=8.5, ncol=3)
ax.set_ylim(0.65, 1.02)
ax.set_yticks(np.arange(0.65, 1.01, 0.05))

# Hide top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')
ax.yaxis.grid(True, linestyle='--', alpha=0.4, color='#dddddd')
ax.set_axisbelow(True)

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.3f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=7.2, color='#333333')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

plt.tight_layout()
fig1_path = FIG_DIR / "fig1_model_comparison.png"
plt.savefig(fig1_path, dpi=300)
plt.close()
print(f"Saved: {fig1_path}")


# ==========================================
# Figure 2: Random Forest (3 subplots)
# ==========================================
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10.5, 3.2), dpi=300)

# 1. Confusion Matrix
rf_cm = np.array([
    [54, 13, 0, 0],
    [3, 64, 3, 0],
    [0, 6, 15, 6],
    [0, 0, 3, 29]
])
classes = ['Budget', 'Mid', 'Prem', 'Flag']
sns.heatmap(rf_cm, annot=True, fmt='d', cmap='Blues', cbar=False, ax=ax1,
            xticklabels=classes, yticklabels=classes, annot_kws={"size": 9})
ax1.set_title("RF: confusion matrix", fontsize=9.5, pad=6)
ax1.set_xlabel("Predicted label", fontsize=8)
ax1.set_ylabel("True label", fontsize=8)
ax1.tick_params(axis='both', which='major', labelsize=8)

# 2. Multi-class ROC curves
rf_curves = curves_data['models_evaluation']['random_forest']['roc_curves']
colors = ['#1e3d59', '#3895d3', '#f37736', '#00b159']
for idx, cname in enumerate(curves_data['class_names']):
    fpr = rf_curves[cname]['fpr']
    tpr = rf_curves[cname]['tpr']
    auc_val = rf_curves[cname]['auc']
    ax2.plot(fpr, tpr, color=colors[idx], lw=1.3, label=f"{cname} ({auc_val:.2f})")
ax2.plot([0, 1], [0, 1], 'k--', lw=0.8, alpha=0.5, label='Chance')
ax2.set_xlim([-0.02, 1.02])
ax2.set_ylim([-0.02, 1.05])
ax2.set_title("ROC curves (OvR: AUC = 0.96)", fontsize=9.5, pad=6)
ax2.set_xlabel("False Positive Rate", fontsize=8)
ax2.set_ylabel("True Positive Rate", fontsize=8)
ax2.legend(loc='lower right', fontsize=6.8, frameon=True, framealpha=0.8)
ax2.tick_params(axis='both', which='major', labelsize=8)
ax2.grid(True, linestyle=':', alpha=0.5)

# 3. Precision-Recall curves
rf_pr = curves_data['models_evaluation']['random_forest']['pr_curves']
for idx, cname in enumerate(curves_data['class_names']):
    rec = rf_pr[cname]['recall']
    prec = rf_pr[cname]['precision']
    ap_val = rf_pr[cname]['ap']
    ax3.plot(rec, prec, color=colors[idx], lw=1.3, label=f"{cname} ({ap_val:.2f})")
ax3.set_xlim([-0.02, 1.02])
ax3.set_ylim([-0.02, 1.05])
ax3.set_title("Precision-recall curves (mAP = 0.83)", fontsize=9.5, pad=6)
ax3.set_xlabel("Recall", fontsize=8)
ax3.set_ylabel("Precision", fontsize=8)
ax3.legend(loc='lower left', fontsize=6.8, frameon=True, framealpha=0.8)
ax3.tick_params(axis='both', which='major', labelsize=8)
ax3.grid(True, linestyle=':', alpha=0.5)

plt.tight_layout()
fig2_path = FIG_DIR / "fig2_random_forest.png"
plt.savefig(fig2_path, dpi=300)
plt.close()
print(f"Saved: {fig2_path}")


# ==========================================
# Figure 3: Support Vector Machine (3 subplots)
# ==========================================
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10.5, 3.2), dpi=300)

# 1. Confusion Matrix
svm_cm = np.array([
    [54, 12, 0, 1],
    [4, 57, 7, 2],
    [0, 5, 16, 6],
    [0, 1, 1, 30]
])
sns.heatmap(svm_cm, annot=True, fmt='d', cmap='Blues', cbar=False, ax=ax1,
            xticklabels=classes, yticklabels=classes, annot_kws={"size": 9})
ax1.set_title("SVM: confusion matrix", fontsize=9.5, pad=6)
ax1.set_xlabel("Predicted label", fontsize=8)
ax1.set_ylabel("True label", fontsize=8)
ax1.tick_params(axis='both', which='major', labelsize=8)

# 2. Multi-class ROC curves
svm_curves = curves_data['models_evaluation']['svm']['roc_curves']
for idx, cname in enumerate(curves_data['class_names']):
    fpr = svm_curves[cname]['fpr']
    tpr = svm_curves[cname]['tpr']
    auc_val = svm_curves[cname]['auc']
    ax2.plot(fpr, tpr, color=colors[idx], lw=1.3, label=f"{cname} ({auc_val:.2f})")
ax2.plot([0, 1], [0, 1], 'k--', lw=0.8, alpha=0.5, label='Chance')
ax2.set_xlim([-0.02, 1.02])
ax2.set_ylim([-0.02, 1.05])
ax2.set_title("ROC curves (OvR: AUC = 0.96)", fontsize=9.5, pad=6)
ax2.set_xlabel("False Positive Rate", fontsize=8)
ax2.set_ylabel("True Positive Rate", fontsize=8)
ax2.legend(loc='lower right', fontsize=6.8, frameon=True, framealpha=0.8)
ax2.tick_params(axis='both', which='major', labelsize=8)
ax2.grid(True, linestyle=':', alpha=0.5)

# 3. Precision-Recall curves
svm_pr = curves_data['models_evaluation']['svm']['pr_curves']
for idx, cname in enumerate(curves_data['class_names']):
    rec = svm_pr[cname]['recall']
    prec = svm_pr[cname]['precision']
    ap_val = svm_pr[cname]['ap']
    ax3.plot(rec, prec, color=colors[idx], lw=1.3, label=f"{cname} ({ap_val:.2f})")
ax3.set_xlim([-0.02, 1.02])
ax3.set_ylim([-0.02, 1.05])
ax3.set_title("Precision-recall curves (mAP = 0.81)", fontsize=9.5, pad=6)
ax3.set_xlabel("Recall", fontsize=8)
ax3.set_ylabel("Precision", fontsize=8)
ax3.legend(loc='lower left', fontsize=6.8, frameon=True, framealpha=0.8)
ax3.tick_params(axis='both', which='major', labelsize=8)
ax3.grid(True, linestyle=':', alpha=0.5)

plt.tight_layout()
fig3_path = FIG_DIR / "fig3_svm.png"
plt.savefig(fig3_path, dpi=300)
plt.close()
print(f"Saved: {fig3_path}")
print("All 3 report figures generated successfully!")
