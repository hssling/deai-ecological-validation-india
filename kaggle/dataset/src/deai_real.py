"""
DEAI Real-Data Analysis — LASI Wave 1 India State/UT Factsheet

Uses state-level LASI data (N=37 states/UTs) to:
1. Construct a state-level DEAI knowledge-weighted score
2. Compute Spearman correlations between DEAI and ageing outcomes
3. Rank states by adverse exposome burden
4. Identify top-burden states (frailty, disability, poor SRH)
5. Produce publication-quality real-data figures

IMPORTANT: This is ecological analysis (state level, N=37).
Individual-level inference requires LASI microdata.
All outputs labelled: DATA_TYPE = REAL

Usage:
    python src/models/deai_real.py --config config.yaml
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).parents[2]))
from src.utils.config import get_arg_config
from src.utils.io import save_figure, save_table
from src.utils.logger import get_logger, log_phase

logger = get_logger("deai_real")

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
})

# Exposome variables available in LASI state factsheet
# All coded so higher value = MORE ADVERSE exposome burden
EXPOSOME_VARS = {
    "adv_indoor_pollution": {
        "label": "Indoor Air Pollution\n(% no clean fuel)",
        "weight": 0.22,
        "source": "LASI Wave 1",
    },
    "adv_sanitation": {
        "label": "Poor Sanitation\n(% no improved)",
        "weight": 0.10,
        "source": "LASI Wave 1",
    },
    "adv_literacy": {
        "label": "Low Literacy\n(% illiterate)",
        "weight": 0.15,
        "source": "LASI Wave 1",
    },
    "tobacco_pct": {
        "label": "Tobacco Use\n(% current consumers)",
        "weight": 0.20,
        "source": "LASI Wave 1",
    },
    "heavy_drinking_pct": {
        "label": "Heavy Episodic\nDrinking (%)",
        "weight": 0.08,
        "source": "LASI Wave 1",
    },
    "adv_water": {
        "label": "Poor Water Access\n(% no improved source)",
        "weight": 0.10,
        "source": "LASI Wave 1",
    },
    "indoor_pollution_pct": {
        "label": "Reported Indoor\nPollution Exposure (%)",
        "weight": 0.08,
        "source": "LASI Wave 1",
    },
    "underweight_pct": {
        "label": "Underweight (%)\n(nutritional deficit)",
        "weight": 0.07,
        "source": "LASI Wave 1",
    },
}

OUTCOME_VARS = {
    "adl_limitation_pct": "ADL Limitations (%)",
    "iadl_limitation_pct": "IADL Limitations (%)",
    "poor_srh_pct": "Poor Self-Rated Health (%)",
    "depression_cidi_pct": "Depression — CIDI-SF (%)",
    "multimorbidity_index": "Multimorbidity Index",
    "fall_pct": "Fall Prevalence (%)",
    "death_rate_60plus_per1000": "Death Rate 60+ (per 1,000)",
}


def build_deai_real(df: pd.DataFrame) -> pd.DataFrame:
    """Build knowledge-weighted DEAI for each state."""
    scaler = StandardScaler()
    avail = {k: v for k, v in EXPOSOME_VARS.items() if k in df.columns}
    cols = list(avail.keys())

    X = df[cols].copy()
    X_filled = X.fillna(X.median())
    X_std = pd.DataFrame(scaler.fit_transform(X_filled), columns=cols, index=df.index)

    weights = np.array([avail[c]["weight"] for c in cols])
    weights = weights / weights.sum()
    df["deai_real"] = X_std.values @ weights

    # Z-standardize
    df["deai_real_z"] = (df["deai_real"] - df["deai_real"].mean()) / df["deai_real"].std()
    logger.info(f"DEAI real: mean={df['deai_real_z'].mean():.3f}, "
                f"range=[{df['deai_real_z'].min():.2f}, {df['deai_real_z'].max():.2f}]")
    return df


def compute_correlations(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    avail_outcomes = {k: v for k, v in OUTCOME_VARS.items() if k in df.columns}
    for outcome_col, outcome_label in avail_outcomes.items():
        valid = df[["deai_real_z", outcome_col]].dropna()
        if len(valid) < 8:
            continue
        r, p = stats.spearmanr(valid["deai_real_z"], valid[outcome_col])
        rows.append({
            "outcome": outcome_col,
            "outcome_label": outcome_label,
            "spearman_r": round(r, 3),
            "p_value": round(p, 4),
            "n_states": len(valid),
            "significant": p < 0.05,
        })
    return pd.DataFrame(rows).sort_values("spearman_r", ascending=False)


def fig_state_deai_ranking(df: pd.DataFrame, out_path: Path) -> None:
    """Horizontal bar chart ranking all states by DEAI score."""
    df_sorted = df.sort_values("deai_real_z", ascending=True).copy()
    df_sorted["state_clean"] = df_sorted["state"].str.replace(" **", "", regex=False)

    # Colour Karnataka distinctly
    colors = ["#c0392b" if z > 0.5 else
              "#e67e22" if z > 0 else
              "#27ae60" if z < -0.5 else
              "#2ecc71" for z in df_sorted["deai_real_z"]]
    karnataka_mask = df_sorted["state_clean"].str.lower() == "karnataka"
    colors = ["#8e44ad" if k else c for k, c in zip(karnataka_mask, colors)]

    fig, ax = plt.subplots(figsize=(10, 12))
    bars = ax.barh(df_sorted["state_clean"], df_sorted["deai_real_z"],
                   color=colors, edgecolor="none", alpha=0.88)
    ax.axvline(0, color="black", lw=1.2, ls="--")
    ax.set_xlabel("DEAI Score (Z-standardized)\nHigher = Greater Adverse Exposome Burden",
                  fontsize=10)
    ax.set_title("State-Level Digital Exposome Aging Index (DEAI)\n"
                 "LASI Wave 1 India — Real Data (IIPS 2022)", fontweight="bold")

    # Mark Karnataka
    karnataka_y = df_sorted["state_clean"].tolist().index("Karnataka")
    ax.get_yticklabels()[karnataka_y].set_color("#8e44ad")
    ax.get_yticklabels()[karnataka_y].set_fontweight("bold")

    legend_elements = [
        mpatches.Patch(color="#c0392b", label="High adverse burden (DEAI > +0.5 SD)"),
        mpatches.Patch(color="#e67e22", label="Moderate adverse (0 to +0.5 SD)"),
        mpatches.Patch(color="#2ecc71", label="Lower adverse burden (DEAI < 0)"),
        mpatches.Patch(color="#8e44ad", label="Karnataka (Tumkur context)"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=8)
    ax.text(0.98, 0.01, "REAL DATA — LASI Wave 1 (2017–18)\nIIPS, Mumbai 2022",
            transform=ax.transAxes, fontsize=8, color="#27ae60", alpha=0.85,
            ha="right", va="bottom", fontstyle="italic",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#27ae60"))
    sns.despine(ax=ax)
    plt.tight_layout()
    save_figure(fig, out_path)
    plt.close(fig)


def fig_deai_outcome_correlations(corr_df: pd.DataFrame, df: pd.DataFrame,
                                   out_path: Path) -> None:
    """Scatter plots: DEAI vs each outcome with Spearman r."""
    avail = corr_df[corr_df["outcome"].isin(df.columns)].head(6)
    n_plots = len(avail)
    if n_plots == 0:
        return
    ncols = 3
    nrows = (n_plots + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(14, 4.5 * nrows))
    axes = np.array(axes).ravel()

    karnataka_mask = df["state"].str.lower() == "karnataka"

    for i, (_, row) in enumerate(avail.iterrows()):
        ax = axes[i]
        outcome = row["outcome"]
        valid = df[["state", "deai_real_z", outcome]].dropna()
        ka = valid[valid["state"].str.lower() == "karnataka"]
        other = valid[valid["state"].str.lower() != "karnataka"]

        ax.scatter(other["deai_real_z"], other[outcome], color="#3498db",
                   alpha=0.7, s=55, edgecolors="white", lw=0.5)
        if not ka.empty:
            ax.scatter(ka["deai_real_z"], ka[outcome], color="#8e44ad",
                       s=120, zorder=5, edgecolors="white", lw=1.5,
                       marker="D", label="Karnataka")
            ax.annotate("Karnataka", (ka["deai_real_z"].values[0], ka[outcome].values[0]),
                        textcoords="offset points", xytext=(6, 4), fontsize=7,
                        color="#8e44ad", fontweight="bold")

        # Trend line
        if len(valid) > 5:
            z_poly = np.polyfit(valid["deai_real_z"], valid[outcome], 1)
            xr = np.linspace(valid["deai_real_z"].min(), valid["deai_real_z"].max(), 50)
            ax.plot(xr, np.polyval(z_poly, xr), color="#e74c3c", lw=1.5, alpha=0.7)

        r_txt = f"ρ={row['spearman_r']:.2f}"
        p_txt = "p<0.001" if row["p_value"] < 0.001 else f"p={row['p_value']:.3f}"
        sig_txt = "✓" if row["significant"] else ""
        ax.text(0.05, 0.93, f"{r_txt}, {p_txt} {sig_txt}",
                transform=ax.transAxes, fontsize=8.5, color="#2c3e50",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#ecf0f1", alpha=0.9))
        ax.set_xlabel("DEAI Score (Z)", fontsize=9)
        ax.set_ylabel(row["outcome_label"], fontsize=9)
        ax.set_title(row["outcome_label"], fontsize=10, fontweight="bold")
        sns.despine(ax=ax)

    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    fig.suptitle("DEAI vs Ageing Outcomes — India State-Level Correlations\n"
                 "LASI Wave 1 (N=37 States/UTs) — REAL DATA",
                 fontsize=12, fontweight="bold", y=1.01)
    ax.legend(fontsize=8, loc="upper left")
    plt.tight_layout()
    save_figure(fig, out_path)
    plt.close(fig)


def fig_exposome_profile_karnataka(df: pd.DataFrame, out_path: Path) -> None:
    """Radar/bar chart: Karnataka vs India mean for each DEAI component."""
    india = df[df["state"] == "INDIA"]
    ka = df[df["state"] == "Karnataka"]
    if india.empty or ka.empty:
        return

    avail_cols = [c for c in EXPOSOME_VARS if c in df.columns]
    labels = [EXPOSOME_VARS[c]["label"] for c in avail_cols]
    india_vals = [india[c].values[0] for c in avail_cols]
    ka_vals = [ka[c].values[0] for c in avail_cols]

    x = np.arange(len(labels))
    width = 0.35
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(x - width / 2, india_vals, width, label="India (national)", color="#3498db", alpha=0.8)
    ax.bar(x + width / 2, ka_vals, width, label="Karnataka", color="#8e44ad", alpha=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=9)
    ax.set_ylabel("% (adverse direction — higher = more adverse burden)")
    ax.set_title("Exposome Profile: Karnataka vs India National Average\n"
                 "LASI Wave 1 (2017–18) — REAL DATA", fontweight="bold")
    ax.legend()
    ax.text(0.98, 0.98, "REAL DATA — LASI Wave 1\nIIPS 2022",
            transform=ax.transAxes, fontsize=8, color="#27ae60", alpha=0.85,
            ha="right", va="top", fontstyle="italic",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#27ae60"))
    sns.despine(ax=ax)
    plt.tight_layout()
    save_figure(fig, out_path)
    plt.close(fig)


def fig_correlation_heatmap(corr_df: pd.DataFrame, df: pd.DataFrame, out_path: Path) -> None:
    """Heatmap: exposome components vs outcomes."""
    avail_exp = [c for c in EXPOSOME_VARS if c in df.columns]
    avail_out = [c for c in OUTCOME_VARS if c in df.columns]

    mat = pd.DataFrame(index=[EXPOSOME_VARS[c]["label"] for c in avail_exp],
                       columns=[OUTCOME_VARS[c] for c in avail_out],
                       dtype=float)
    pmat = mat.copy()
    for exp_col, exp_lbl in zip(avail_exp, mat.index):
        for out_col, out_lbl in zip(avail_out, mat.columns):
            valid = df[[exp_col, out_col]].dropna()
            if len(valid) >= 8:
                r, p = stats.spearmanr(valid[exp_col], valid[out_col])
                mat.loc[exp_lbl, out_lbl] = r
                pmat.loc[exp_lbl, out_lbl] = p

    mat = mat.astype(float)
    fig, ax = plt.subplots(figsize=(12, 6))
    annot = mat.round(2).astype(str)
    for i in mat.index:
        for j in mat.columns:
            if pmat.loc[i, j] < 0.05:
                annot.loc[i, j] = annot.loc[i, j] + "*"

    sns.heatmap(mat, annot=annot, fmt="", cmap="RdBu_r", vmin=-1, vmax=1,
                linewidths=0.5, ax=ax, cbar_kws={"label": "Spearman ρ"},
                annot_kws={"size": 9})
    ax.set_title("Exposome–Outcome Correlations (Spearman ρ)\n"
                 "LASI Wave 1 India, N=37 States/UTs — REAL DATA\n"
                 "* = p<0.05", fontweight="bold", fontsize=11)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right", fontsize=9)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=9)
    ax.text(1.15, -0.1, "REAL DATA — LASI Wave 1\nIIPS 2022",
            transform=ax.transAxes, fontsize=8, color="#27ae60", alpha=0.85,
            ha="right", va="bottom", fontstyle="italic")
    plt.tight_layout()
    save_figure(fig, out_path)
    plt.close(fig)


def run(cfg: dict) -> None:
    proc_dir: Path = cfg["paths"]["data_processed"]
    lasi_file = proc_dir / "lasi_state_real.parquet"

    if not lasi_file.exists():
        logger.info("LASI real data not found — running ingestion first")
        from src.ingest.ingest_lasi_real import run as ingest_run
        ingest_run(cfg)

    df = pd.read_parquet(lasi_file)
    logger.info(f"Loaded LASI real data: {len(df)} states × {len(df.columns)} cols")

    # Build DEAI
    df = build_deai_real(df)

    # Compute outcome correlations
    corr_df = compute_correlations(df)
    save_table(corr_df, cfg["paths"]["results_tables"] / "deai_real_outcome_correlations.csv")
    logger.info(f"Outcome correlations:\n{corr_df[['outcome_label','spearman_r','p_value','significant']].to_string(index=False)}")

    # State rankings
    rank_df = df[["state", "deai_real_z"]].sort_values("deai_real_z", ascending=False)
    rank_df["rank"] = range(1, len(rank_df) + 1)
    save_table(rank_df, cfg["paths"]["results_tables"] / "deai_real_state_rankings.csv")

    # Save full enriched dataset
    save_table(df, proc_dir / "lasi_with_deai_real.parquet")
    save_table(df, cfg["paths"]["results_tables"] / "lasi_with_deai_real.csv")

    figs = cfg["paths"]["results_figures"]
    fig_state_deai_ranking(df, figs / "real_fig1_state_deai_ranking.png")
    fig_deai_outcome_correlations(corr_df, df, figs / "real_fig2_deai_outcome_scatter.png")
    fig_exposome_profile_karnataka(df, figs / "real_fig3_karnataka_exposome_profile.png")
    fig_correlation_heatmap(corr_df, df, figs / "real_fig4_exposome_outcome_heatmap.png")

    logger.info("All real-data figures generated")

    # Karnataka summary
    ka = df[df["state"] == "Karnataka"].iloc[0]
    india = df[df["state"] == "INDIA"].iloc[0]
    logger.info(f"\n=== Karnataka vs India ===")
    logger.info(f"  DEAI Z-score: Karnataka={ka['deai_real_z']:.3f} vs India={india['deai_real_z']:.3f}")
    logger.info(f"  ADL limitation: Karnataka={ka.get('adl_limitation_pct','NA')}% vs India={india.get('adl_limitation_pct','NA')}%")
    logger.info(f"  Poor SRH: Karnataka={ka.get('poor_srh_pct','NA')}% vs India={india.get('poor_srh_pct','NA')}%")
    logger.info(f"  Tobacco: Karnataka={ka.get('tobacco_pct','NA')}% vs India={india.get('tobacco_pct','NA')}%")
    logger.info(f"  Clean fuel: Karnataka={100-ka.get('adv_indoor_pollution',0):.1f}% vs India={100-india.get('adv_indoor_pollution',0):.1f}%")

    log_phase(
        "Phase 4b — DEAI Real Data Analysis", "COMPLETE",
        f"N = {len(df)} states/UTs\n"
        f"Data: LASI Wave 1 (REAL)\n"
        f"DEAI built from {len([c for c in EXPOSOME_VARS if c in df.columns])} exposome variables\n"
        f"Outcome correlations: {corr_df['significant'].sum()}/{len(corr_df)} significant (p<0.05)\n"
        f"Karnataka DEAI Z = {ka['deai_real_z']:.3f}\n"
        f"Top DEAI state: {rank_df.iloc[0]['state']} (Z={rank_df.iloc[0]['deai_real_z']:.2f})",
        log_dir=cfg["paths"]["logs"],
    )


if __name__ == "__main__":
    run(get_arg_config())
