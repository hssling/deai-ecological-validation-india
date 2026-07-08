"""Figures for the low-FVC vs PRISm head-to-head:
  F1 (a) coverage vs mean adjusted OR (the specificity-risk trade-off);
     (b) adjusted OR (95% CI) by flag across ageing outcomes.
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
plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans",
                     "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 150})

res = pd.read_csv(os.path.join(OUT, "tables", "headtohead.csv"))
summ = pd.read_csv(os.path.join(OUT, "tables", "flag_summary.csv"))

colours = {"GLI-PRISm (fixed)": "#b3261e", "GLI-RSP (fixed)": "#d98a2b",
           "National low-FVC (LLN)": "#2e7d32", "National low-FVC (fixed)": "#1b5e20"}

fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), gridspec_kw={"width_ratios": [1, 1.35]})

# (a) coverage vs mean adjusted OR
a = axes[0]
for _, r in summ.iterrows():
    a.scatter(r["coverage"], r["mean_adjOR"], s=140, color=colours[r["flag"]], zorder=3)
    a.annotate(r["flag"].replace(" (", "\n("), (r["coverage"], r["mean_adjOR"]),
               textcoords="offset points", xytext=(8, 4), fontsize=7.8)
a.set_xlabel("Coverage — adults flagged (%)")
a.set_ylabel("Mean adjusted odds ratio\n(across 5 ageing outcomes)")
a.set_title("(a) Fewer flagged, higher risk:\nthe correct-reference low-FVC concentrates risk", fontsize=9.8)
a.grid(alpha=0.2)

# (b) OR forest by flag x outcome
b = axes[1]
outcomes = list(dict.fromkeys(res["outcome"]))
flags = list(colours.keys())
ypos = np.arange(len(outcomes))
off = np.linspace(-0.3, 0.3, len(flags))
for fi, flag in enumerate(flags):
    sub = res[res["flag"] == flag].set_index("outcome").reindex(outcomes)
    b.errorbar(sub["adj_OR"], ypos + off[fi],
               xerr=[sub["adj_OR"] - sub["lo"], sub["hi"] - sub["adj_OR"]],
               fmt="o", color=colours[flag], ms=5, lw=1.2, capsize=2, label=flag)
b.axvline(1, color="#888", lw=1, ls="--")
b.set_yticks(ypos); b.set_yticklabels(outcomes)
b.invert_yaxis()
b.set_xlabel("Adjusted odds ratio (95% CI)")
b.set_title("(b) Adjusted association with ageing outcomes", fontsize=9.8)
b.legend(frameon=False, fontsize=7.4, loc="lower right")
fig.suptitle("GLI-PRISm flags 40% at near-average risk; a correctly-referenced low-FVC flags fewer at higher risk\n"
             "(but no spirometric label adds much beyond age and sex)", fontsize=10.3)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "Figure1_headtohead.png"), bbox_inches="tight")
print("wrote Figure1_headtohead.png")
