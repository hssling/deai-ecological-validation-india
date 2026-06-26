"""Publication figure builder for the MJDRDYPU health-economics study.

Reads the committed result tables in outputs/health_economics_mjdrdypu/tables/
(and, for F2, reloads the record-level analytic frame) and writes six 600-dpi,
colour-blind-safe PNG figures to outputs/health_economics_mjdrdypu/figures/.

Run as:
    python scripts/make_health_economics_figures.py
from the repo root.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

TABLES = Path("outputs/health_economics_mjdrdypu/tables")
FIGDIR = Path("outputs/health_economics_mjdrdypu/figures")
FIGDIR.mkdir(parents=True, exist_ok=True)

SAV = "data/raw/g2aging_harmonized_lasi_a3_sav/H_LASI_a3.sav"
PROC = "data/processed/analysis_dataset.csv"

DPI = 600

# Colour-blind-safe palette (Wong/Okabe-Ito subset)
BLUE = "#0072B2"
ORANGE = "#D55E00"
GREEN = "#009E73"
PURPLE = "#CC79A7"
YELLOW = "#E69F00"


def _save(fig, path: Path):
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    size_kb = path.stat().st_size / 1024
    print(f"saved {path} ({size_kb:.1f} KB)")


def fig1_che_by_threshold_age():
    df = pd.read_csv(TABLES / "table2_che.csv", index_col="group")
    groups = ["All 60+", "70+"]
    thresholds = [
        ("che10", "CHE >10% of\nconsumption"),
        ("che25", "CHE >25% of\nconsumption"),
        ("che40cap", "CHE >40% of\ncapacity-to-pay"),
    ]
    x = np.arange(len(thresholds))
    width = 0.35
    colors = {groups[0]: BLUE, groups[1]: ORANGE}

    fig, ax = plt.subplots(figsize=(7, 5))
    for i, g in enumerate(groups):
        vals = [df.loc[g, col] for col, _ in thresholds]
        offset = (i - 0.5) * width
        bars = ax.bar(x + offset, vals, width, label=g, color=colors[g])
        for b, v in zip(bars, vals):
            ax.annotate(f"{v:.1f}", (b.get_x() + b.get_width() / 2, v),
                        textcoords="offset points", xytext=(0, 3),
                        ha="center", va="bottom", fontsize=9)

    ax.set_xticks(x)
    ax.set_xticklabels([lbl for _, lbl in thresholds])
    ax.set_ylabel("Weighted % of households")
    ax.set_title("Catastrophic health spending among older Indians")
    ax.legend(title="Age group")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _save(fig, FIGDIR / "fig1_che_by_threshold_age.png")


def fig2_concentration_curve():
    from src.health_economics import load_economics_frame, add_che_flags

    ci_total = None
    try:
        eq = pd.read_csv(TABLES / "table4_equity.csv")
        total_row = eq[eq["regressor"] == "__TOTAL__"]
        if not total_row.empty:
            ci_total = float(total_row["concentration_index"].iloc[0])
    except Exception as exc:
        print(f"WARNING: could not read concentration index from table4_equity.csv: {exc}")

    df = load_economics_frame(SAV, PROC)
    df = add_che_flags(df)
    s60 = df[pd.to_numeric(df["age_years"], errors="coerce") >= 60].copy()

    d = s60.dropna(subset=["cons_pc", "che40cap_flag", "r1wtresp"]).sort_values("cons_pc")
    w = pd.to_numeric(d["r1wtresp"], errors="coerce").fillna(0).values
    y = pd.to_numeric(d["che40cap_flag"], errors="coerce").values

    if w.sum() == 0 or np.sum(w * y) == 0:
        print("WARNING: fig2 — zero weight sum or zero CHE40cap cases; concentration curve may be degenerate.")

    cum_pop = np.cumsum(w) / w.sum()
    cum_y = np.cumsum(w * y) / np.sum(w * y)
    cum_pop = np.concatenate([[0], cum_pop])
    cum_y = np.concatenate([[0], cum_y])

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot([0, 1], [0, 1], linestyle="--", color="grey", label="Equality line")
    ax.plot(cum_pop, cum_y, color=BLUE, linewidth=2, label="CHE (>40% capacity-to-pay)")
    ax.fill_between(cum_pop, cum_y, cum_pop, color=BLUE, alpha=0.15)

    ax.set_xlabel("Cumulative weighted share of population\n(ranked poorest → richest by per-capita consumption)")
    ax.set_ylabel("Cumulative weighted share of catastrophic-spending cases")
    ax.set_title("Who bears catastrophic spending? Concentration by consumption rank")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")

    if ci_total is not None:
        ax.annotate(f"Concentration index = {ci_total:.3f}",
                    xy=(0.05, 0.92), xycoords="axes fraction",
                    fontsize=10, ha="left",
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="grey"))

    ax.legend(loc="lower right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _save(fig, FIGDIR / "fig2_concentration_curve.png")


def fig3_impoverishment():
    df = pd.read_csv(TABLES / "table3_impoverishment.csv", index_col="group")
    groups = ["All 60+", "Men 60+", "Women 60+", "Rural 60+", "Urban 60+"]
    groups = [g for g in groups if g in df.index]

    x = np.arange(len(groups))
    width = 0.35

    pre = df.loc[groups, "pre_poverty"].values
    post = df.loc[groups, "post_poverty"].values
    headcount = df.loc[groups, "impov_headcount"].values

    fig, ax = plt.subplots(figsize=(9, 6))
    bars_pre = ax.bar(x - width / 2, pre, width, label="Pre medical spending", color=BLUE)
    bars_post = ax.bar(x + width / 2, post, width, label="Post medical spending", color=ORANGE)

    ax.set_ylim(0, max(pre.max(), post.max()) * 1.22)

    for xi, (p0, p1, hc) in enumerate(zip(pre, post, headcount)):
        top = max(p0, p1)
        ax.annotate(f"+{hc:.1f} pp", (xi, top), textcoords="offset points",
                    xytext=(0, 6), ha="center", va="bottom", fontsize=9, fontweight="bold")

    for bars, vals in ((bars_pre, pre), (bars_post, post)):
        for b, v in zip(bars, vals):
            ax.annotate(f"{v:.1f}", (b.get_x() + b.get_width() / 2, v),
                        textcoords="offset points", xytext=(0, -12),
                        ha="center", va="top", fontsize=8, color="white", fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(groups)
    ax.set_ylabel("Weighted % below the poverty line")
    ax.set_title("Medical spending pushes older people below the poverty line")
    ax.legend(loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.0))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.text(0.5, -0.02,
              "Annotations show the impoverishment headcount (post − pre): the newly poor due to medical spending.",
              ha="center", fontsize=8, style="italic")
    _save(fig, FIGDIR / "fig3_impoverishment.png")


def fig4_shap_importance():
    df = pd.read_csv(TABLES / "table5_drivers.csv")
    shap_df = df[df["method"] == "shap"].copy()
    if shap_df.empty:
        print("WARNING: fig4 — no rows with method=='shap' in table5_drivers.csv.")

    label_map = {
        "is_female": "Female",
        "is_rural": "Rural",
        "age_years": "Age",
        "multimorbidity_ge2": "Multimorbidity",
        "functional_limitation": "Functional limitation",
        "any_pension": "Any pension",
        "education": "Education",
    }
    shap_df["label"] = shap_df["feature"].map(label_map).fillna(shap_df["feature"])
    shap_df = shap_df.sort_values("importance", ascending=True)

    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.barh(shap_df["label"], shap_df["importance"], color=GREEN)
    for b, v in zip(bars, shap_df["importance"]):
        ax.annotate(f"{v:.3f}", (v, b.get_y() + b.get_height() / 2),
                    textcoords="offset points", xytext=(4, 0),
                    ha="left", va="center", fontsize=9)

    ax.set_xlabel("Mean |SHAP value| (importance)")
    ax.set_title("What predicts catastrophic spending (SHAP importance)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _save(fig, FIGDIR / "fig4_shap_importance.png")


def fig5_microsim_impact():
    df = pd.read_csv(TABLES / "table6_microsim.csv", index_col="scenario")
    label_map = {
        "S1 PM-JAY 70+ full inpatient cover": "PM-JAY 70+\ninpatient",
        "S2 Outpatient (incl. medicines) cover, all 60+": "Outpatient/\nmedicine cover",
        "S3 Pension top-up +Rs500/mo, all 60+": "Pension\ntop-up",
        "S4 Combined S1+S2+S3": "Combined\n(ceiling)",
    }
    scenarios = list(label_map.keys())
    scenarios = [s for s in scenarios if s in df.index]
    labels = [label_map[s] for s in scenarios]

    che40_delta = df.loc[scenarios, "che40cap_delta"].values
    che10_delta = df.loc[scenarios, "che10_delta"].values
    fiscal_cost_cr = df.loc[scenarios, "fiscal_cost"].values / 1e7

    x = np.arange(len(scenarios))
    width = 0.35

    fig, ax = plt.subplots(figsize=(9, 6))
    bars1 = ax.bar(x - width / 2, che40_delta, width, label="CHE >40% capacity-to-pay (Δ pp)", color=BLUE)
    bars2 = ax.bar(x + width / 2, che10_delta, width, label="CHE >10% consumption (Δ pp)", color=ORANGE)

    for b, v in zip(bars1, che40_delta):
        ax.annotate(f"{v:.1f}", (b.get_x() + b.get_width() / 2, v),
                    textcoords="offset points", xytext=(0, -10 if v < 0 else 4),
                    ha="center", va="top" if v < 0 else "bottom", fontsize=8)
    for b, v in zip(bars2, che10_delta):
        ax.annotate(f"{v:.1f}", (b.get_x() + b.get_width() / 2, v),
                    textcoords="offset points", xytext=(0, -10 if v < 0 else 4),
                    ha="center", va="top" if v < 0 else "bottom", fontsize=8)

    ymin = min(che40_delta.min(), che10_delta.min())
    ax.set_ylim(ymin * 1.35, max(che40_delta.max(), che10_delta.max()) + 3)

    for xi, cost in zip(x, fiscal_cost_cr):
        ax.annotate(f"Fiscal cost:\nRs {cost:,.0f} cr", (xi, ymin * 1.18),
                    ha="center", va="top", fontsize=8, color="dimgray")

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Percentage-point change in CHE\n(negative = reduction)")
    ax.set_title("Financial-protection impact of policy scenarios")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.18), ncol=2, frameon=False, fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.subplots_adjust(bottom=0.22, top=0.86)
    fig.text(0.5, 0.02,
              "Scenarios assume full coverage and represent upper-bound ceilings. "
              "Fiscal cost annotated in Rs crore (value / 1e7).",
              ha="center", fontsize=8, style="italic")
    _save(fig, FIGDIR / "fig5_microsim_impact.png")


def fig6_caregiving_value():
    care = pd.read_csv(TABLES / "table_caregiving.csv").iloc[0]
    care_value_cr = care["national_annual_value"] / 1e7

    combined_cost_cr = None
    try:
        micro = pd.read_csv(TABLES / "table6_microsim.csv", index_col="scenario")
        if "S4 Combined S1+S2+S3" in micro.index:
            combined_cost_cr = micro.loc["S4 Combined S1+S2+S3", "fiscal_cost"] / 1e7
    except Exception as exc:
        print(f"WARNING: fig6 — could not read combined-scenario fiscal cost: {exc}")

    labels = ["Unpaid family\ncaregiving (annual value)"]
    values = [care_value_cr]
    colors = [PURPLE]
    if combined_cost_cr is not None:
        labels.append("Combined policy\nscenario (fiscal cost)")
        values.append(combined_cost_cr)
        colors.append(YELLOW)

    fig, ax = plt.subplots(figsize=(7, 6))
    bars = ax.bar(labels, values, color=colors, width=0.5)
    for b, v in zip(bars, values):
        ax.annotate(f"Rs {v:,.0f} cr", (b.get_x() + b.get_width() / 2, v),
                    textcoords="offset points", xytext=(0, 6),
                    ha="center", va="bottom", fontsize=10, fontweight="bold")

    ax.set_ylabel("Rs crore per year")
    ax.set_title("The hidden economy of unpaid elder care")

    annotation = (
        f"{care['recipients_pct']:.1f}% of older adults receive informal care\n"
        f"Mean {care['mean_hours_week']:.1f} hours/week of care\n"
        f"Rs {care['annual_value_per_recipient']:,.0f} annual value per recipient"
    )
    ax.text(0.98, 0.95, annotation, transform=ax.transAxes,
            ha="right", va="top", fontsize=9,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="grey"))

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _save(fig, FIGDIR / "fig6_caregiving_value.png")


def main():
    builders = [
        fig1_che_by_threshold_age,
        fig2_concentration_curve,
        fig3_impoverishment,
        fig4_shap_importance,
        fig5_microsim_impact,
        fig6_caregiving_value,
    ]
    print(f"Writing figures to {FIGDIR.resolve()}")
    for build in builders:
        build()
    print("Done.")


if __name__ == "__main__":
    main()
