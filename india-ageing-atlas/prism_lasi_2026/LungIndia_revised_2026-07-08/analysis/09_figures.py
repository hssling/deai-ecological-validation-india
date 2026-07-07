"""
Figures for the PRISm/LASI Lung India revision (v2).

  F1  STROBE participant-flow diagram (new; reviewer #1, #2, #11)
  F2  Spirometry quality-grade panel (new; reviewer #3, #4, #11)
  F3  FVC z-distribution vs GLI reference (kept; measurement thesis)
  F4  Reference-equation comparison of PRISm/RSP prevalence (new centrepiece)

Duplicative odds-ratio bar charts from the original submission are intentionally
NOT reproduced (reviewer #11: figures should not restate tables).
"""
import json
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.abspath(os.path.join(HERE, "..", "outputs"))
FIG = os.path.abspath(os.path.join(HERE, "..", "figures"))
os.makedirs(FIG, exist_ok=True)
K = json.load(open(os.path.join(OUT, "key_numbers_v2.json")))
ref = pd.read_csv(os.path.join(OUT, "tables", "t_reference_comparison.csv"))

plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans", "axes.spines.top": False,
                     "axes.spines.right": False, "figure.dpi": 150})
INK = "#22333b"

# ---------------------------------------------------------------- F1 STROBE flow
fig, ax = plt.subplots(figsize=(7.2, 8.4))
ax.set_xlim(0, 10); ax.set_ylim(0, 12); ax.axis("off")


def box(x, y, w, h, text, fc="#eef2f4"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.12",
                                fc=fc, ec=INK, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9.3, color=INK)


def arrow(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=14,
                                 color=INK, lw=1.2))


main_x, main_w = 1.0, 5.2
box(main_x, 10.6, main_w, 1.0, f"LASI Wave 1 respondents aged ≥45 years\nn = {K['n_lasi_45']:,}", "#dfe7ea")
arrow(main_x + main_w / 2, 10.6, main_x + main_w / 2, 9.9)
box(main_x, 8.9, main_w, 1.0, f"Spirometry attempted and quality-graded\nn = {K['n_attempted']:,}")
arrow(main_x + main_w / 2, 8.9, main_x + main_w / 2, 8.2)
box(main_x, 7.2, main_w, 1.0, f"Met acceptability grade\nn = {K['n_acceptable']:,}")
arrow(main_x + main_w / 2, 7.2, main_x + main_w / 2, 6.5)
box(main_x, 5.3, main_w, 1.0, f"Valid predicted values and\nplausible measured height\nn = {K['n_analytic']:,}")
arrow(main_x + main_w / 2, 5.3, main_x + main_w / 2, 4.6)
box(main_x, 3.3, main_w, 1.1, f"Analytic sample\nn = {K['n_analytic']:,}\n(median age {K['median_age']:.0f} y, {K['pct_women']:.0f}% women)", "#dfe7ea")

# exclusion side-boxes
ex_x, ex_w = 6.8, 2.9
box(ex_x, 9.3, ex_w, 0.9, f"No spirometry / not gradable\nn = {K['n_not_attempted']:,}", "#f6ece9")
arrow(main_x + main_w, 9.4, ex_x, 9.75)
box(ex_x, 7.6, ex_w, 0.9, f"Did not meet acceptability\nn = {K['n_unacceptable']:,}", "#f6ece9")
arrow(main_x + main_w, 7.7, ex_x, 8.05)
box(ex_x, 5.7, ex_w, 0.9, f"Implausible height\nn = {K['n_ht_drop']:,}", "#f6ece9")
arrow(main_x + main_w, 5.8, ex_x, 6.15)
ax.text(5.0, 2.2, "Excluded participants were older and frailer than those included\n"
                  "(standardized differences up to 0.22; Supplementary Table S2),\n"
                  "which would bias prevalence estimates downward, not upward.",
        ha="center", va="center", fontsize=8.2, style="italic", color="#4a5a62")
fig.tight_layout()
fig.savefig(os.path.join(FIG, "Figure1_participant_flow.png"), bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- F2 QC panel
qc = K["qc"]
fig, axes = plt.subplots(1, 2, figsize=(9.0, 4.0))
# (a) grading funnel
a = axes[0]
stages = ["Attempted", "Acceptable", "Acceptable +\nrepeatable"]
vals = [qc["attempted"], qc["acceptable"], qc["acceptable_and_repeatable"]]
bars = a.barh(range(len(stages))[::-1], vals, color=["#8fb3bf", "#4f8797", "#22636f"], height=0.6)
a.set_yticks(range(len(stages))[::-1]); a.set_yticklabels(stages)
for i, v in zip(range(len(stages))[::-1], vals):
    a.text(v * 0.98, i, f"{v:,}", va="center", ha="right", color="white", fontsize=9)
a.set_xlabel("Participants (n)"); a.set_title("(a) Spirometry quality funnel", fontsize=10)
# (b) acceptable vs unacceptable pie
b = axes[1]
b.pie([qc["acceptable"], qc["unacceptable"]],
      labels=[f"Acceptable\n{qc['acceptable']:,}", f"Not acceptable\n{qc['unacceptable']:,}"],
      colors=["#4f8797", "#e0c3b6"], autopct="%1.0f%%", startangle=90,
      wedgeprops=dict(width=0.42, edgecolor="white"))
b.set_title("(b) Acceptability among graded tests", fontsize=10)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "Figure2_quality_grades.png"), bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- F3 FVC z-distribution
# recompute fvc_z on the analytic sample for a faithful figure
df = pd.read_csv(os.path.join(ROOT, "data", "processed", "biomarker_integrated_analysis_dataset.csv"))
d = df[(df["acceptable"] == 1) & (df["r1agey"] >= 45)].copy()
z = pd.to_numeric(d["fvc_z"], errors="coerce").dropna()
z = z[(z > -6) & (z < 6)]
fig, ax = plt.subplots(figsize=(6.6, 4.2))
ax.hist(z, bins=60, color="#7fa6b0", edgecolor="white", density=True, alpha=0.9)
xs = np.linspace(-6, 6, 400)
ax.plot(xs, 1 / np.sqrt(2 * np.pi) * np.exp(-xs ** 2 / 2), color="#b5651d", lw=1.8,
        label="GLI reference (z ~ N(0,1))")
med = float(np.median(z))
ax.axvline(med, color="#22333b", ls="--", lw=1.4, label=f"Indian median z = {med:.2f}")
ax.axvline(0, color="#8a8a8a", ls=":", lw=1.0)
ax.set_xlabel("FVC z-score (GLI-2012 South-East Asian reference)")
ax.set_ylabel("Density"); ax.legend(frameon=False, fontsize=8.6)
ax.set_title("The whole population sits ~1 SD below the GLI reference mean", fontsize=9.8)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "Figure3_fvc_zdistribution.png"), bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- F4 reference comparison
# PRISm and RSP prevalence by reference/definition
order = ["GLI-2012 fixed", "GLI-2012 LLN",
         "GLI-Global 2022 (race-neutral) fixed", "GLI-Global 2022 (race-neutral) LLN",
         "Chhabra-2014 fixed", "Chhabra-2014 LLN",
         "Agarwal-2020 (India) fixed", "Agarwal-2020 (India) LLN"]
lab = {"GLI-2012 fixed": "GLI-2012 SE-Asian\n(fixed)",
       "GLI-2012 LLN": "GLI-2012 SE-Asian\n(LLN)",
       "GLI-Global 2022 (race-neutral) fixed": "GLI-Global 2022\n(fixed)",
       "GLI-Global 2022 (race-neutral) LLN": "GLI-Global 2022\n(LLN)",
       "Chhabra-2014 fixed": "Chhabra-2014 India\n(fixed)",
       "Chhabra-2014 LLN": "Chhabra-2014 India\n(LLN)",
       "Agarwal-2020 (India) fixed": "Agarwal-2020 India\n(fixed)",
       "Agarwal-2020 (India) LLN": "Agarwal-2020 India\n(LLN)"}
rr = ref.set_index("scheme")
prism = [rr.loc[s, "PRISm_pct"] for s in order]
rsp = [rr.loc[s, "RSP_pct"] for s in order]
x = np.arange(len(order)); w = 0.38
colors_p = ["#22636f" if "GLI" in s else "#b5651d" for s in order]
fig, ax = plt.subplots(figsize=(9.6, 4.8))
ax.bar(x - w / 2, prism, w, label="PRISm", color=colors_p)
ax.bar(x + w / 2, rsp, w, label="RSP", color="#c9d6da", edgecolor="#6b7d83")
# internal reference reference line
intern = float(K["internal_reference"]["PRISm"].split()[0])
ax.axhline(intern, color="#555", ls="--", lw=1.2)
ax.text(len(order) - 0.5, intern + 0.8, f"Internal LASI healthy-subset PRISm = {intern:.1f}%",
        ha="right", fontsize=8.2, color="#555")
for xi, v in zip(x - w / 2, prism):
    ax.text(xi, v + 0.6, f"{v:.0f}", ha="center", fontsize=7.8)
ax.set_xticks(x); ax.set_xticklabels([lab[s] for s in order], fontsize=7.6)
ax.set_ylabel("Weighted prevalence (%)")
ax.set_title("Same lungs, five references: spirometric-impairment prevalence is\n"
             "governed by the reference equation, not the physiology", fontsize=10)
ax.legend(frameon=False, ncol=2, loc="upper right")
ax.set_ylim(0, 52)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "Figure4_reference_comparison.png"), bbox_inches="tight")
plt.close(fig)

print("Figures written to", FIG)
for f in sorted(os.listdir(FIG)):
    print(" -", f)
