"""
Regenerate Figures 1-4 for the MJDRDYPU anti-ageing evidence map (revision R1).

Fixes applied vs. the submitted version:
- Figure 1 (PRISMA): proper connected flow with screening breakdown; no 'pilot' jargon.
- Figure 2: plots the credibility_score column (matching Table 1 and the caption),
  NOT the max_claim_score column that the submitted figure mistakenly used; data
  labels added to every bar.
- Figures 3 & 4: axis relabelled (remove 'repo' workspace jargon); data labels /
  de-overlapped annotations.
All values are read from intervention_credibility_ranking.csv (single source of truth).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import pandas as pd
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
df = pd.read_csv(HERE / "tables" / "intervention_credibility_ranking.csv")
df = df.sort_values("credibility_score", ascending=False).reset_index(drop=True)
OUT = HERE / "figures"
OUT.mkdir(exist_ok=True)

plt.rcParams.update({"font.size": 11, "savefig.dpi": 200, "savefig.bbox": "tight"})

TIER_COLOR = {
    "highest_current_human_healthspan_signal": "#1f77b4",
    "human_signal_requires_verification": "#ff7f0e",
    "biomarker_or_indirect_human_signal": "#2ca02c",
    "low_directness_or_speculative": "#d62728",
}
TIER_LABEL = {
    "highest_current_human_healthspan_signal": "Strongest current human healthspan signal",
    "human_signal_requires_verification": "Human signal, requires confirmation",
    "biomarker_or_indirect_human_signal": "Biomarker / indirect human signal",
    "low_directness_or_speculative": "Low directness / speculative",
}
# Display labels — kept identical to main-manuscript Table 1 so figure axis
# labels match the table exactly. "supplements" and "controversial" are the two
# grouped search categories given self-explanatory labels in revision R1.
DISPLAY = {
    "exercise": "Exercise",
    "microbiome": "Microbiome",
    "rapamycin_mtor": "Rapamycin/mTOR",
    "senolytics": "Senolytics",
    "caloric_restriction": "Caloric restriction",
    "lifestyle_bundle": "Lifestyle bundle",
    "nad_sirtuin": "NAD+/sirtuin",
    "fasting": "Fasting",
    "supplements": "Dietary supplements",
    "metformin": "Metformin",
    "sleep_circadian": "Sleep/circadian",
    "controversial": "Plasma/telomerase",
    "reprogramming": "Reprogramming",
    "stem_cell": "Stem cell",
}
def pretty(name):
    return DISPLAY.get(name, name.replace("_", " ").title())

# ---------------------------------------------------------------- Figure 1: PRISMA
def fig1_prisma():
    FIGW, FIGH, XR = 10.0, 11.0, 14.0
    fig, ax = plt.subplots(figsize=(FIGW, FIGH))
    # Pin the axes to a known fraction of the figure so the data-unit -> inch
    # mapping is deterministic; this lets the wrapper below size text reliably.
    fig.subplots_adjust(left=0.0, right=1.0, top=0.94, bottom=0.0)
    ax.axis("off"); ax.set_xlim(0, XR); ax.set_ylim(0, 14)
    main_x, side_x = 4.6, 11.4
    main_w, side_w = 8.2, 4.4
    fs = 10
    in_per_x = FIGW / XR                 # inches per x data-unit
    char_in = 0.092                      # ~width of one character at fs=10 (in)
    def box(x, y, w, lines, fc="#eef1fb", ec="#34386e"):
        # Wrap each line to the box's own width so text can never spill past the
        # box edge, then size the box height to the wrapped line count.
        max_chars = max(10, int((w * in_per_x - 0.5) / char_in))
        wrapped = []
        for ln in lines:
            wrapped.extend(textwrap.wrap(ln, max_chars) or [""])
        h = 0.62 + 0.42 * len(wrapped)
        ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                    boxstyle="round,pad=0.10,rounding_size=0.14",
                    fc=fc, ec=ec, lw=1.4))
        ax.text(x, y, "\n".join(wrapped), ha="center", va="center", fontsize=fs)
        return h
    def arrow(x1, y1, x2, y2):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                    arrowstyle="-|>", mutation_scale=18, lw=1.5, color="#34386e"))
    ys = [12.8, 10.6, 8.6, 6.5, 4.3, 2.0]
    h0 = box(main_x, ys[0], main_w, ["Records identified through database searching",
                                     "(PubMed, Europe PMC, Crossref)", "n = 1155"])
    h1 = box(main_x, ys[1], main_w, ["Records after duplicate removal",
                                     "(by DOI, PMID, normalised title)", "n = 1029"])
    h2 = box(main_x, ys[2], main_w, ["Records screened on title/abstract", "n = 1029"])
    h3 = box(main_x, ys[3], main_w, ["Records taken to full-text eligibility assessment",
                                     "n = 484 (29 include + 455 uncertain)"])
    h4 = box(main_x, ys[4], main_w, ["Priority human-evidence verification (n = 40)",
                                     "19 open full text, 16 abstract, 5 not retrieved"])
    h5 = box(main_x, ys[5], main_w, ["Records contributing extracted effect information",
                                     "n = 28 (14 representative records in Table 2)"])
    hs = [h0, h1, h2, h3, h4, h5]
    for i in range(len(ys) - 1):
        arrow(main_x, ys[i] - hs[i]/2, main_x, ys[i+1] + hs[i+1]/2)
    # side exclusion boxes, connected from the main-column right edge
    box(side_x, ys[0], side_w, ["Duplicates removed", "n = 126"], fc="#fbeeee", ec="#8a3a3a")
    arrow(main_x + main_w/2, ys[0], side_x - side_w/2, ys[0])
    box(side_x, ys[2], side_w, ["Excluded at screening", "n = 545"], fc="#fbeeee", ec="#8a3a3a")
    arrow(main_x + main_w/2, ys[2], side_x - side_w/2, ys[2])
    ax.set_title("Study selection flow", fontsize=14, pad=2)
    fig.savefig(OUT / "prisma_flow.png"); plt.close(fig)

# ---------------------------------------------------- Figure 2: credibility ranking
def fig2_ranking():
    d = df.sort_values("credibility_score", ascending=True)
    fig, ax = plt.subplots(figsize=(8.6, 6.2))
    colors = [TIER_COLOR[t] for t in d["credibility_tier"]]
    bars = ax.barh(d["intervention_name"].map(pretty), d["credibility_score"], color=colors)
    for bar, val in zip(bars, d["credibility_score"]):
        ax.text(val + 0.3, bar.get_y() + bar.get_height()/2, f"{val:.2f}",
                va="center", ha="left", fontsize=9.5)
    ax.set_xlabel("Intervention credibility score")
    ax.set_xlim(0, df["credibility_score"].max() * 1.12)
    ax.set_title("Intervention credibility ranking (n = 14 classes)", fontsize=13)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in
               ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]]
    labels = [TIER_LABEL[k] for k in
              ["highest_current_human_healthspan_signal", "human_signal_requires_verification",
               "biomarker_or_indirect_human_signal", "low_directness_or_speculative"]]
    ax.legend(handles, labels, fontsize=8.2, loc="lower right", frameon=True)
    fig.savefig(OUT / "evidence_score_ranking.png"); plt.close(fig)

# ------------------------------------------------------- Figure 3: hype vs evidence
def fig3_hype():
    fig, ax = plt.subplots(figsize=(8.8, 6.2))
    for tier, sub in df.groupby("credibility_tier"):
        ax.scatter(sub["credibility_score"], sub["hype_rate"],
                   s=sub["n_extracted_records"] * 12 + 30,
                   c=TIER_COLOR[tier], alpha=0.75, edgecolors="white",
                   linewidths=0.8, label=TIER_LABEL[tier])
    # de-overlapped labels: (dx, dy, ha) per class to separate the dense
    # lower-right cluster (senolytics/microbiome/rapamycin/caloric restriction).
    offsets = {
        "exercise":            (0.0,  0.045, "center"),
        "microbiome":          (0.8,  0.052, "left"),
        "rapamycin_mtor":      (0.9, -0.052, "left"),
        "senolytics":          (-0.6, 0.058, "right"),
        "caloric_restriction": (-0.7, 0.052, "right"),
        "lifestyle_bundle":    (0.4, -0.052, "left"),
        "nad_sirtuin":         (-0.6,-0.052, "right"),
        "fasting":             (0.4,  0.040, "left"),
        "supplements":         (0.0,  0.042, "center"),
        "metformin":           (-0.3, 0.045, "right"),
        "sleep_circadian":     (0.0, -0.050, "center"),
        "controversial":       (0.5,  0.045, "left"),
        "reprogramming":       (0.5,  0.042, "left"),
        "stem_cell":           (0.4,  0.045, "left"),
    }
    for _, r in df.iterrows():
        dx, dy, ha = offsets.get(r["intervention_name"], (0.0, 0.030, "center"))
        ax.annotate(pretty(r["intervention_name"]),
                    (r["credibility_score"], r["hype_rate"]),
                    xytext=(r["credibility_score"] + dx, r["hype_rate"] + dy),
                    ha=ha, fontsize=8.3)
    ax.axhline(0.10, ls="--", color="grey", lw=1)
    ax.text(df["credibility_score"].max(), 0.105, "hype-flag threshold 0.10",
            ha="right", va="bottom", fontsize=8, color="grey")
    ax.set_ylim(-0.06, 0.86)
    ax.set_xlabel("Intervention credibility score")
    ax.set_ylabel("Proportion of records flagged for hype-heavy language")
    ax.set_title("Credibility versus promotional-language burden", fontsize=13)
    order = ["highest_current_human_healthspan_signal", "human_signal_requires_verification",
             "biomarker_or_indirect_human_signal", "low_directness_or_speculative"]
    handles = [plt.Line2D([0], [0], marker="o", ls="", mfc=TIER_COLOR[k],
               mec="white", ms=9) for k in order]
    ax.legend(handles, [TIER_LABEL[k] for k in order], fontsize=8.0, loc="upper right",
              frameon=True, title="Credibility tier", title_fontsize=8.5)
    fig.savefig(OUT / "hype_vs_evidence_map.png"); plt.close(fig)

# ------------------------------------------------- Figure 4: translational readiness
def fig4_translational():
    d = df.sort_values("credibility_score", ascending=True)
    fig, ax = plt.subplots(figsize=(8.8, 6.4))
    for tier, sub in d.groupby("credibility_tier"):
        ax.scatter(sub["credibility_score"], sub["intervention_name"].map(pretty),
                   s=sub["human_records"] * 22 + 40, c=TIER_COLOR[tier],
                   alpha=0.8, edgecolors="white", linewidths=0.8, label=TIER_LABEL[tier])
    for _, r in d.iterrows():
        ax.text(r["credibility_score"] + 0.5, pretty(r["intervention_name"]),
                f"{r['credibility_score']:.1f}", va="center", fontsize=8.5)
    ax.set_xlabel("Intervention credibility score")
    ax.set_xlim(0, df["credibility_score"].max() * 1.15)
    ax.set_title("Translational readiness by intervention class\n(marker size ∝ human-study count)",
                 fontsize=12.5)
    order = ["highest_current_human_healthspan_signal", "human_signal_requires_verification",
             "biomarker_or_indirect_human_signal", "low_directness_or_speculative"]
    handles = [plt.Line2D([0], [0], marker="o", ls="", mfc=TIER_COLOR[k],
               mec="white", ms=9) for k in order]
    ax.legend(handles, [TIER_LABEL[k] for k in order], fontsize=8.0, loc="lower right",
              frameon=True)
    fig.savefig(OUT / "translational_matrix.png"); plt.close(fig)

fig1_prisma(); fig2_ranking(); fig3_hype(); fig4_translational()
print("Figures written to", OUT)
for p in sorted(OUT.glob("*.png")):
    print(" -", p.name)
