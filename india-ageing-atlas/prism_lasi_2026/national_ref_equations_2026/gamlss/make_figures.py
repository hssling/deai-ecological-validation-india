"""Regenerate Paper 2 figures from the GAMLSS (BCCG/LMS) reference, overwriting the
PNGs used by the manuscript build so the paper reflects the gold-standard method."""
import json
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(HERE, ".."))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
FIG = os.path.join(BASE, "figures")
REVREF = os.path.join(BASE, "..", "LungIndia_revised_2026-07-08", "outputs", "tables",
                      "t_reference_comparison.csv")
plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans",
                     "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 150})
colors = {"M": "#22636f", "F": "#b5651d"}

grid = pd.read_csv(os.path.join(HERE, "gamlss_centile_grid.csv"))
val = pd.read_csv(os.path.join(HERE, "gamlss_validation.csv"))
K = json.load(open(os.path.join(BASE, "outputs", "key_numbers_gamlss.json")))

# ---- F1 centile curves (GAMLSS) ----
fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.4), sharex=True)
for ax, param in zip(axes, ["fvc", "fev1"]):
    for sex in ["M", "F"]:
        g = grid[(grid["param"] == param) & (grid["sex"] == sex)]
        ht = g["refht"].iloc[0]
        ax.plot(g["age"], g["median"], color=colors[sex], lw=2, label=f"{sex} median (ht {ht:.0f} cm)")
        ax.plot(g["age"], g["lln"], color=colors[sex], lw=1.3, ls="--", label=f"{sex} LLN (5th centile)")
    ax.set_title(f"{param.upper()} (L)", fontsize=10); ax.set_xlabel("Age (years)"); ax.grid(alpha=0.25)
axes[0].set_ylabel("Litres"); axes[0].legend(frameon=False, fontsize=7.6, loc="upper right")
fig.suptitle("National LASI reference (GAMLSS BCCG): median and LLN by age and sex", fontsize=11)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "Figure1_centile_curves.png"), bbox_inches="tight"); plt.close(fig)

# ---- F2 validation (GAMLSS holdout) ----
val["plab"] = val["param"].map({"fvc": "FVC", "fev1": "FEV1", "fev1fvc": "FEV1/FVC"})
fig, ax = plt.subplots(figsize=(7.2, 4.2))
x = np.arange(len(val)); ax.errorbar(x, val["mean_z"], yerr=val["sd_z"], fmt="o", capsize=4,
                                     color="#22636f", lw=1.4)
ax.axhline(0, color="#888", lw=1); ax.axhline(1, color="#ccc", ls=":"); ax.axhline(-1, color="#ccc", ls=":")
ax.set_xticks(x); ax.set_xticklabels([f"{r.plab}\n{r.sex}" for r in val.itertuples()], fontsize=8.5)
ax.set_ylabel("Held-out z-score (mean ± SD)")
ax.set_title("GAMLSS internal validation: held-out z centred at 0 with SD ≈ 1", fontsize=10)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "Figure2_validation.png"), bbox_inches="tight"); plt.close(fig)

# ---- F3 reference comparison incl. GAMLSS LASI ----
rev = pd.read_csv(REVREF).set_index("scheme")
b = K["burden"]
rows = [
    ("GLI-2012 SE-Asian", rev.loc["GLI-2012 fixed", "PRISm_pct"], rev.loc["GLI-2012 LLN", "PRISm_pct"]),
    ("GLI-Global 2022", rev.loc["GLI-Global 2022 (race-neutral) fixed", "PRISm_pct"],
     rev.loc["GLI-Global 2022 (race-neutral) LLN", "PRISm_pct"]),
    ("Chhabra-2014", rev.loc["Chhabra-2014 fixed", "PRISm_pct"], rev.loc["Chhabra-2014 LLN", "PRISm_pct"]),
    ("Agarwal-2020", rev.loc["Agarwal-2020 (India) fixed", "PRISm_pct"], rev.loc["Agarwal-2020 (India) LLN", "PRISm_pct"]),
    ("LASI national\n(GAMLSS, this study)", b["PRISm_fixed"][0], b["PRISm_LLN"][0]),
]
labels = [r[0] for r in rows]; fixed = [r[1] for r in rows]; lln = [r[2] for r in rows]
x = np.arange(len(rows)); w = 0.38
hl = ["#22636f", "#22636f", "#b5651d", "#b5651d", "#2e7d32"]
fig, ax = plt.subplots(figsize=(8.8, 4.6))
ax.bar(x - w/2, fixed, w, label="Fixed (<80% pred)", color="#6b7d83")
ax.bar(x + w/2, lln, w, label="LLN", color=hl)
for xi, v in zip(x - w/2, fixed): ax.text(xi, v + 0.6, f"{v:.0f}", ha="center", fontsize=8)
for xi, v in zip(x + w/2, lln): ax.text(xi, v + 0.6, f"{v:.0f}", ha="center", fontsize=8)
ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=8.4); ax.set_ylabel("Weighted PRISm prevalence (%)")
ax.set_title("PRISm prevalence collapses under a nationally representative (GAMLSS) reference", fontsize=10.5)
ax.legend(frameon=False); ax.set_ylim(0, 50)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "Figure3_reference_comparison.png"), bbox_inches="tight"); plt.close(fig)
print("regenerated Figure1/2/3 from GAMLSS")
