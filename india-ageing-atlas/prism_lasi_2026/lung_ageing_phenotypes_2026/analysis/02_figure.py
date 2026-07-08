"""Figures for the lung-ageing phenotype paper:
  F1  (a) standardized phenotype feature profiles (heatmap);
      (b) external ageing outcomes by phenotype (grouped bars).
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "outputs"))
FIG = os.path.abspath(os.path.join(HERE, "..", "figures"))
os.makedirs(FIG, exist_ok=True)
plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans", "figure.dpi": 150})

prof = pd.read_csv(os.path.join(OUT, "tables", "phenotype_profiles_standardized.csv"), index_col=0)
ext = pd.read_csv(os.path.join(OUT, "tables", "phenotype_outcomes.csv"))

names = {0: "Metabolic-inflammatory\n(lower lung volume)", 1: "Lean / low-inflammation\n(higher lung volume)"}
feat_lab = {"FVC_z": "FVC z", "FEV1FVC_z": "FEV1/FVC z", "bmi": "BMI", "hba1c": "HbA1c",
            "log_crp": "log-CRP", "hb": "Haemoglobin", "r1gripsum": "Grip strength"}
prof = prof.rename(columns=feat_lab)

fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6), gridspec_kw={"width_ratios": [1.25, 1]})

# (a) heatmap
a = axes[0]
M = prof.values
im = a.imshow(M, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
a.set_xticks(range(len(prof.columns))); a.set_xticklabels(prof.columns, rotation=35, ha="right", fontsize=8.5)
a.set_yticks(range(len(prof.index))); a.set_yticklabels([names[i] for i in prof.index], fontsize=8.5)
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        a.text(j, i, f"{M[i,j]:+.2f}", ha="center", va="center", fontsize=8,
               color="white" if abs(M[i, j]) > 0.55 else "#222")
a.set_title("(a) Standardized phenotype profiles", fontsize=10)
cb = fig.colorbar(im, ax=a, fraction=0.046, pad=0.04); cb.set_label("z (within sample)", fontsize=8)

# (b) outcomes
b = axes[1]
oc = ["Frailty", "Functional limitation", "Multimorbidity", "Poor self-rated health"]
x = np.arange(len(oc)); w = 0.38
colours = {0: "#b3261e", 1: "#2e7d32"}
for i, row in ext.iterrows():
    b.bar(x + (i - 0.5) * w, [row[o] for o in oc], w, label=names[int(row["cluster"])].replace("\n", " "),
          color=colours[int(row["cluster"])])
b.set_xticks(x); b.set_xticklabels(oc, rotation=20, ha="right", fontsize=8.2)
b.set_ylabel("Weighted prevalence (%)")
b.set_title("(b) Ageing outcomes NOT used in clustering", fontsize=10)
b.legend(frameon=False, fontsize=7.6, loc="upper right")
b.spines["top"].set_visible(False); b.spines["right"].set_visible(False)
fig.suptitle("A metabolic-inflammatory reserve axis underlies lung-function variation in older Indians", fontsize=11)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "Figure1_phenotypes.png"), bbox_inches="tight")
print("wrote Figure1_phenotypes.png")
