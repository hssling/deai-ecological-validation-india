"""Figures for the national LASI reference-equation paper.

  F1  Centile curves (median + LLN vs age at reference height, by sex) for FVC and FEV1
  F2  Holdout z-score adequacy (mean z ~ 0, SD ~ 1 by age band)
  F3  PRISm/RSP prevalence by reference equation, with the new LASI reference added
"""
import json
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.abspath(os.path.join(HERE, "..", "outputs"))
FIG = os.path.abspath(os.path.join(HERE, "..", "figures"))
os.makedirs(FIG, exist_ok=True)
REVREF = os.path.join(ROOT, "prism_lasi_2026", "LungIndia_revised_2026-07-08",
                      "outputs", "tables", "t_reference_comparison.csv")

plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans",
                     "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 150})
grid = pd.read_csv(os.path.join(OUT, "tables", "centile_grid.csv"))
val = pd.read_csv(os.path.join(OUT, "tables", "validation_zscores.csv"))
K = json.load(open(os.path.join(OUT, "key_numbers.json")))

# ---------------------------------------------------------------- F1 centile curves
fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.4), sharex=True)
colors = {"M": "#22636f", "F": "#b5651d"}
for ax, param in zip(axes, ["FVC", "FEV1"]):
    for sex in ["M", "F"]:
        g = grid[(grid["param"] == param) & (grid["sex"] == sex)]
        ht = g["ref_height"].iloc[0]
        ax.plot(g["age"], g["median"], color=colors[sex], lw=2,
                label=f"{sex} median (ht {ht:.0f} cm)")
        ax.plot(g["age"], g["lln"], color=colors[sex], lw=1.3, ls="--",
                label=f"{sex} LLN (5th centile)")
    ax.set_title(f"{param} (L)", fontsize=10)
    ax.set_xlabel("Age (years)")
    ax.grid(alpha=0.25)
axes[0].set_ylabel("Litres")
axes[0].legend(frameon=False, fontsize=7.6, loc="upper right")
fig.suptitle("National LASI reference: median and lower limit of normal by age and sex", fontsize=11)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "Figure1_centile_curves.png"), bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- F2 z adequacy
vb = val[val["band"] != "ALL"].copy()
order = ["45-54", "55-64", "65-74", "75+"]
fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.0), sharey=True)
for ax, param in zip(axes, ["FEV1", "FVC"]):
    for sex, mk in [("M", "o"), ("F", "s")]:
        g = vb[(vb["param"] == param) & (vb["sex"] == sex)].set_index("band").reindex(order)
        ax.errorbar(range(len(order)), g["mean_z"], yerr=g["sd_z"], marker=mk, capsize=3,
                    color=colors[sex], label=sex, lw=1.4)
    ax.axhline(0, color="#888", lw=1)
    ax.axhline(1, color="#ccc", lw=0.8, ls=":"); ax.axhline(-1, color="#ccc", lw=0.8, ls=":")
    ax.set_xticks(range(len(order))); ax.set_xticklabels(order)
    ax.set_title(f"{param}: holdout z (mean ± SD)", fontsize=10)
    ax.set_xlabel("Age band")
axes[0].set_ylabel("z-score"); axes[0].legend(frameon=False, fontsize=8)
fig.suptitle("Validation: holdout z-scores are centred near 0 with SD near 1", fontsize=11)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "Figure2_validation.png"), bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- F3 reference comparison incl. LASI
rev = pd.read_csv(REVREF).set_index("scheme")
b = K["burden"]
rows = [
    ("GLI-2012 SE-Asian", rev.loc["GLI-2012 fixed", "PRISm_pct"], rev.loc["GLI-2012 LLN", "PRISm_pct"]),
    ("GLI-Global 2022", rev.loc["GLI-Global 2022 (race-neutral) fixed", "PRISm_pct"],
     rev.loc["GLI-Global 2022 (race-neutral) LLN", "PRISm_pct"]),
    ("Chhabra-2014", rev.loc["Chhabra-2014 fixed", "PRISm_pct"], rev.loc["Chhabra-2014 LLN", "PRISm_pct"]),
    ("Agarwal-2020", rev.loc["Agarwal-2020 (India) fixed", "PRISm_pct"], rev.loc["Agarwal-2020 (India) LLN", "PRISm_pct"]),
    ("LASI national\n(this study)", b["PRISm_LASI_fixed"][0], b["PRISm_LASI_LLN"][0]),
]
labels = [r[0] for r in rows]
fixed = [r[1] for r in rows]
lln = [r[2] for r in rows]
x = np.arange(len(rows)); w = 0.38
fig, ax = plt.subplots(figsize=(8.8, 4.6))
bars1 = ax.bar(x - w / 2, fixed, w, label="Fixed (<80% pred)", color="#6b7d83")
hl = ["#22636f", "#22636f", "#b5651d", "#b5651d", "#2e7d32"]
bars2 = ax.bar(x + w / 2, lln, w, label="LLN", color=hl)
for xi, v in zip(x - w / 2, fixed):
    ax.text(xi, v + 0.6, f"{v:.0f}", ha="center", fontsize=8)
for xi, v in zip(x + w / 2, lln):
    ax.text(xi, v + 0.6, f"{v:.0f}", ha="center", fontsize=8)
ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=8.4)
ax.set_ylabel("Weighted PRISm prevalence (%)")
ax.set_title("PRISm prevalence collapses under a nationally representative reference", fontsize=10.5)
ax.legend(frameon=False)
ax.set_ylim(0, 50)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "Figure3_reference_comparison.png"), bbox_inches="tight")
plt.close(fig)

print("Figures written:")
for f in sorted(os.listdir(FIG)):
    print(" -", f)
