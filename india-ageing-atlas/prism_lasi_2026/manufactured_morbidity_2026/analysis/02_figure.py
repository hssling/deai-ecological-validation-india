"""Signature figure for the manufactured-morbidity paper: PRISm (and RSP)
prevalence for every reference x definition, coloured by reference family."""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "outputs"))
FIG = os.path.abspath(os.path.join(HERE, "..", "figures"))
os.makedirs(FIG, exist_ok=True)
plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans",
                     "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 150})

g = pd.read_csv(os.path.join(OUT, "master_grid.csv")).sort_values("PRISm").reset_index(drop=True)
colour = {"Global/foreign": "#b3261e", "Regional Indian": "#b5651d", "National Indian": "#2e7d32"}
y = range(len(g))
labels = [f"{r.reference} ({r.definition})" for r in g.itertuples()]

fig, ax = plt.subplots(figsize=(9.4, 6.2))
for yi, r in zip(y, g.itertuples()):
    c = colour[r.family]
    ax.plot([0, r.PRISm], [yi, yi], color=c, lw=1.2, alpha=0.5, zorder=1)
    ax.scatter(r.PRISm, yi, color=c, s=70, zorder=2)
    ax.text(r.PRISm + 0.7, yi, f"{r.PRISm:.0f}", va="center", fontsize=8.5, color=c)
ax.set_yticks(list(y)); ax.set_yticklabels(labels, fontsize=8.2)
ax.set_xlabel("Weighted PRISm prevalence (%)")
ax.set_xlim(0, 52)
ax.set_title("Same 30,996 lungs, one label, eleven answers:\n"
             "PRISm prevalence is manufactured by the reference equation (3.9%–46.3%, ~12-fold)",
             fontsize=11)
handles = [Line2D([0], [0], marker="o", color="w", markerfacecolor=c, markersize=9, label=k)
           for k, c in colour.items()]
ax.legend(handles=handles, frameon=False, loc="lower right", title="Reference family")
ax.grid(axis="x", alpha=0.2)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "Figure1_manufactured_morbidity.png"), bbox_inches="tight")
print("wrote Figure1_manufactured_morbidity.png")
