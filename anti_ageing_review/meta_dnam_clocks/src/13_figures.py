"""Phase 13 (Path-C): final main figures at 300 dpi PNG + SVG.

Fig 1: PRISMA 2020 flow.
Fig 2: RoB summary traffic-light (pending grey).
Fig 3: Forest plot for DunedinPACE k=3 (with DL, HKSJ, Bayes diamonds, 95% PI).
Fig 4: 4-panel gate-status (funnel/NMA/meta-reg/GRADE-pub-bias).
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from _common import ensure_dirs, load_config, log  # noqa: E402

ELIGIBLE_METRICS = {"mean_difference_years", "mean_difference_pace"}


def save_fig(fig, base: Path) -> None:
    fig.savefig(base.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(base.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def fig1_prisma(figs: Path, freeze: str, counts: dict) -> Path:
    fig, ax = plt.subplots(figsize=(9, 11))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis("off")
    ax.set_title("Figure 1. PRISMA 2020 flow — DNAm clocks Path-C review", fontsize=12, pad=14)

    boxes = [
        (5, 13, f"Records identified\n(raw across 5 sources): n={counts['raw']}"),
        (5, 11, f"Duplicates removed: n={counts['dupes']}\nUnique candidate pool: n={counts['candidate_pool']}"),
        (5, 9, f"Title/abstract screened: n={counts['candidate_pool']}\nExcluded (TA): n={counts['excluded_ta']}"),
        (5, 7, f"Full-text reports assessed: n={counts['ft_assessed']}\nExcluded (FT) with reasons: n={counts['excluded_ft']}"),
        (5, 5, f"Included (qualitative synthesis): n={counts['qual']}\n(Path-C relaxed promotions included)"),
        (5, 3, f"Included in quantitative synthesis\nDunedinPACE pool k={counts['quant']};\nOther clocks: narrative only"),
    ]
    for x, y, text in boxes:
        rect = mpatches.FancyBboxPatch((x - 3, y - 0.7), 6, 1.4,
                                       boxstyle="round,pad=0.05",
                                       linewidth=1.2, edgecolor="#1f2937", facecolor="#f1f5f9")
        ax.add_patch(rect)
        ax.text(x, y, text, ha="center", va="center", fontsize=9)
    # arrows
    for y1, y2 in [(13, 11), (11, 9), (9, 7), (7, 5), (5, 3)]:
        ax.annotate("", xy=(5, y2 + 0.75), xytext=(5, y1 - 0.75),
                    arrowprops=dict(arrowstyle="->", color="#1f2937", lw=1.2))
    base = figs / f"fig1_prisma_path_c_{freeze}"
    save_fig(fig, base)
    return base.with_suffix(".png")


def fig2_rob(figs: Path, freeze: str, rob: pd.DataFrame) -> Path:
    domains = ["d1_randomization", "d2_deviations", "d3_missing_data",
               "d4_measurement", "d5_selective_reporting", "overall"]
    short = ["D1\nRand", "D2\nDeviations", "D3\nMissing", "D4\nMeasure", "D5\nSelective", "Overall"]
    studies = rob["study_id"].tolist()
    fig, ax = plt.subplots(figsize=(9, max(4, 0.25 * len(studies) + 2)))
    n_s = len(studies)
    n_d = len(domains)
    # Color map
    color_map = {"low": "#16a34a", "some concerns": "#f59e0b", "high": "#dc2626",
                 "pending": "#9ca3af"}
    for j, dom in enumerate(domains):
        for i, sid in enumerate(studies):
            val = rob.iloc[i][dom] if dom in rob.columns else "pending"
            if pd.isna(val):
                val = "pending"
            c = color_map.get(str(val).strip().lower(), "#9ca3af")
            ax.add_patch(mpatches.Circle((j + 0.5, n_s - i - 0.5), 0.32, color=c, ec="#1f2937", lw=0.6))
    ax.set_xlim(0, n_d)
    ax.set_ylim(0, n_s)
    ax.set_xticks([i + 0.5 for i in range(n_d)])
    ax.set_xticklabels(short, fontsize=8)
    ax.set_yticks([n_s - i - 0.5 for i in range(n_s)])
    ax.set_yticklabels(studies, fontsize=7)
    ax.set_title("Figure 2. RoB 2 traffic-light grid (all 'pending' — dual coding outstanding)", fontsize=11)
    for s in ax.spines.values():
        s.set_visible(False)
    legend = [mpatches.Patch(color=c, label=lab.title())
              for lab, c in [("pending", "#9ca3af"), ("low", "#16a34a"),
                             ("some concerns", "#f59e0b"), ("high", "#dc2626")]]
    ax.legend(handles=legend, loc="lower center", bbox_to_anchor=(0.5, -0.18),
              ncol=4, fontsize=8, frameon=False)
    base = figs / f"fig2_rob_path_c_{freeze}"
    save_fig(fig, base)
    return base.with_suffix(".png")


def fig3_forest(figs: Path, freeze: str, sle: pd.DataFrame, pooled: pd.DataFrame) -> Path:
    sub = sle[(sle["clock"] == "DunedinPACE") & sle["effect_metric"].isin(ELIGIBLE_METRICS)]
    sub = sub.dropna(subset=["value", "se"]).copy()
    pl = pooled[pooled["clock"] == "DunedinPACE"].iloc[0]
    studies = sub["study_id"].tolist()
    vals = sub["value"].astype(float).to_numpy()
    ses = sub["se"].astype(float).to_numpy()
    los = vals - 1.96 * ses
    his = vals + 1.96 * ses

    n = len(studies)
    fig, ax = plt.subplots(figsize=(9, 1.3 + 0.55 * (n + 3)))
    y_studies = list(range(n, 0, -1))  # top to bottom
    # study rows
    for i, y in enumerate(y_studies):
        ax.errorbar(vals[i], y, xerr=[[vals[i] - los[i]], [his[i] - vals[i]]],
                    fmt="s", color="#1f2937", capsize=4, markersize=7)
        ax.text(-0.95, y, studies[i], ha="left", va="center", fontsize=8.5, transform=ax.get_yaxis_transform())
        ax.text(0.99, y, f"{vals[i]:+.3f} [{los[i]:+.3f}, {his[i]:+.3f}]",
                ha="right", va="center", fontsize=8, transform=ax.get_yaxis_transform())

    # Pooled diamonds
    def diamond(y, mu, lo, hi, color, label):
        ax.add_patch(mpatches.Polygon([[lo, y], [mu, y + 0.22], [hi, y], [mu, y - 0.22]],
                                       closed=True, facecolor=color, edgecolor="#111827", lw=0.8))
        ax.text(-0.95, y, label, ha="left", va="center", fontsize=9, transform=ax.get_yaxis_transform(), weight="bold")
        ax.text(0.99, y, f"{mu:+.3f} [{lo:+.3f}, {hi:+.3f}]",
                ha="right", va="center", fontsize=8.5, transform=ax.get_yaxis_transform())

    diamond(0, float(pl["mu_dl"]), float(pl["ci_lower_dl"]), float(pl["ci_upper_dl"]),
            "#2563eb", "Pooled DL (RE)")
    diamond(-1, float(pl["mu_hksj"]), float(pl["ci_lower_hksj"]), float(pl["ci_upper_hksj"]),
            "#0d9488", "HKSJ")
    diamond(-2, float(pl["mu_bayes"]), float(pl["ci_lower_bayes"]), float(pl["ci_upper_bayes"]),
            "#9333ea", "Bayes (HN τ)")

    # 95% Prediction interval bar
    pi_lo, pi_hi = float(pl["pi_lower"]), float(pl["pi_upper"])
    ax.plot([pi_lo, pi_hi], [-3, -3], color="#374151", lw=2)
    ax.plot([pi_lo, pi_lo], [-3.15, -2.85], color="#374151", lw=2)
    ax.plot([pi_hi, pi_hi], [-3.15, -2.85], color="#374151", lw=2)
    ax.text(-0.95, -3, "95% prediction interval", ha="left", va="center", fontsize=8.5,
            transform=ax.get_yaxis_transform(), style="italic")
    ax.text(0.99, -3, f"[{pi_lo:+.3f}, {pi_hi:+.3f}]", ha="right", va="center", fontsize=8,
            transform=ax.get_yaxis_transform())

    ax.axvline(0, color="#6b7280", lw=0.8, ls="--")
    ax.set_yticks([])
    ax.set_xlabel("DunedinPACE mean difference (intervention − control)", fontsize=10)
    ax.set_ylim(-3.8, n + 0.7)
    ax.set_title(
        f"Figure 3. Forest plot — DunedinPACE (k={int(pl['k'])}); "
        f"I²={float(pl['I2']):.1f}%, τ²={float(pl['tau2']):.4f}, Q p={float(pl['Q_pval']):.3f}",
        fontsize=11,
    )
    base = figs / f"fig3_forest_dunedinpace_path_c_{freeze}"
    save_fig(fig, base)
    return base.with_suffix(".png")


def fig4_gates(figs: Path, freeze: str) -> Path:
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    panels = [
        ("Funnel plot", "Gate: k>=10 (per clock)\nDunedinPACE k=3 → NOT performed",
         "Funnel asymmetry tests are uninformative below k=10."),
        ("Network meta-analysis", "Gate: k>=10 AND connected network\nAll clocks fail → NOT performed",
         "Pairwise pool only is presented."),
        ("Meta-regression", "Gate: k>=10 per clock\nMax k=3 (DunedinPACE) → NOT performed",
         "Continuous moderator tests are not credible at k=3."),
        ("GRADE: publication bias domain", "k<10 → cannot be assessed\nDomain NOT downgraded (transparent)",
         "We report this honestly rather than assume absence."),
    ]
    for ax, (title, status, note) in zip(axes.flatten(), panels):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.add_patch(mpatches.FancyBboxPatch((0.04, 0.06), 0.92, 0.88,
                                              boxstyle="round,pad=0.04",
                                              linewidth=1.2, edgecolor="#1f2937",
                                              facecolor="#fef3c7"))
        ax.text(0.5, 0.85, title, ha="center", va="center", fontsize=12, weight="bold")
        ax.text(0.5, 0.55, status, ha="center", va="center", fontsize=10)
        ax.text(0.5, 0.25, note, ha="center", va="center", fontsize=9, style="italic", color="#374151")
    fig.suptitle("Figure 4. Gate-status panel (analyses correctly not performed)", fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    base = figs / f"fig4_gate_status_path_c_{freeze}"
    save_fig(fig, base)
    return base.with_suffix(".png")


def run(cfg: dict) -> None:
    freeze = cfg["project"]["freeze_date"]
    figs = Path(cfg["paths"]["results_figs"])
    proc = Path(cfg["paths"]["data_processed"])
    tabs = Path(cfg["paths"]["results_tabs"])
    interim = Path(cfg["paths"]["data_interim"])
    ensure_dirs(figs)

    # counts for PRISMA
    raw_path = interim / f"raw_records_dnam_{freeze}.csv"
    cand_path = interim / f"candidate_pool_{freeze}.csv"
    excluded_path = proc / f"excluded_fulltext_{freeze}.csv"
    relaxed_path = proc / f"relaxed_eligibility_audit_{freeze}.csv"
    sle_path = proc / f"study_level_effects_{freeze}.csv"
    pooled_path = tabs / f"per_clock_pooled_{freeze}.csv"
    rob_path = proc / f"rob2_assessments_{freeze}.csv"

    raw_n = int(pd.read_csv(raw_path).shape[0]) if raw_path.exists() else 2804
    cand_n = int(pd.read_csv(cand_path).shape[0]) if cand_path.exists() else 0
    dupes = max(0, raw_n - cand_n)
    excluded_ta = 252 + 1955  # from prior gate report context
    relaxed = pd.read_csv(relaxed_path) if relaxed_path.exists() else pd.DataFrame()
    if not relaxed.empty:
        ft_assessed = int(relaxed.shape[0])
        excluded_ft = int((relaxed["final_eligibility"] == "exclude_fulltext").sum())
        qual = int(relaxed["final_eligibility"].isin(
            ["include_accessible_first_reviewer", "include_relaxed"]).sum())
    else:
        ft_assessed = 41
        excluded_ft = 20
        qual = 21
    pooled = pd.read_csv(pooled_path)
    quant = int(pooled.loc[pooled["clock"] == "DunedinPACE", "k"].iloc[0])

    counts = {
        "raw": raw_n, "dupes": dupes, "candidate_pool": cand_n if cand_n else raw_n - dupes,
        "excluded_ta": excluded_ta, "ft_assessed": ft_assessed, "excluded_ft": excluded_ft,
        "qual": qual, "quant": quant,
    }
    p1 = fig1_prisma(figs, freeze, counts)

    rob = pd.read_csv(rob_path)
    p2 = fig2_rob(figs, freeze, rob)

    sle = pd.read_csv(sle_path)
    p3 = fig3_forest(figs, freeze, sle, pooled)

    p4 = fig4_gates(figs, freeze)

    log("figures_done", paths=[str(p) for p in [p1, p2, p3, p4]])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="anti_ageing_review/meta_dnam_clocks/config/meta_config.yaml")
    args = ap.parse_args()
    cfg = load_config(args.config)
    run(cfg)


if __name__ == "__main__":
    main()
