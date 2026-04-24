from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.utils.io import load_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render narrow meta-add-on primary-pool assets.")
    parser.add_argument("--config", required=True, help="Path to review config YAML.")
    return parser.parse_args()


def _root_from_config(config_path: str) -> Path:
    config_file = Path(config_path).resolve()
    return config_file.parent.parent


def build_study_table(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["study_label"] = out["title"].map(
        {
            "Effect of long-term caloric restriction on DNA methylation measures of biological aging in healthy adults from the CALERIE trial.": "CALERIE",
            "Individual and additive effects of vitamin D, omega-3 and exercise on DNA methylation clocks of biological aging in older adults from the DO-HEALTH trial.": "DO-HEALTH",
        }
    ).fillna(out["title"])
    out["effect_95ci"] = out.apply(
        lambda r: f"{r['effect_estimate']:.3f} ({r['ci_lower']:.3f} to {r['ci_upper']:.3f})",
        axis=1,
    )
    out["sample_size"] = out.apply(
        lambda r: (
            f"{int(r['n_treatment'])} vs {int(r['n_control'])}"
            if pd.notna(r.get("n_treatment")) and pd.notna(r.get("n_control"))
            else "DNAm subset reported in source"
        ),
        axis=1,
    )
    keep = [
        "study_label",
        "year",
        "intervention_name",
        "outcome_name",
        "outcome_timepoint",
        "sample_size",
        "effect_95ci",
        "risk_of_bias_overall",
        "source_locator",
    ]
    out = out.loc[:, keep].rename(
        columns={
            "study_label": "study",
            "year": "year",
            "intervention_name": "intervention",
            "outcome_name": "outcome",
            "outcome_timepoint": "timepoint",
            "sample_size": "sample_size",
            "effect_95ci": "effect_95ci",
            "risk_of_bias_overall": "risk_of_bias",
            "source_locator": "source",
        }
    )
    return out


def build_summary_table(df: pd.DataFrame) -> pd.DataFrame:
    row = df.iloc[0]
    return pd.DataFrame(
        [
            {
                "outcome_name": row["outcome_name"],
                "n_studies": int(row["n_studies"]),
                "study_ids": row["study_ids"],
                "fixed_effect_estimate": round(float(row["fixed_effect_estimate"]), 3),
                "fixed_effect_ci": f"{float(row['fixed_effect_ci_lower']):.3f} to {float(row['fixed_effect_ci_upper']):.3f}",
                "random_effect_estimate": round(float(row["random_effect_estimate"]), 3),
                "random_effect_ci": f"{float(row['random_effect_ci_lower']):.3f} to {float(row['random_effect_ci_upper']):.3f}",
                "i_squared_percent": round(float(row["i_squared_percent"]), 1),
            }
        ]
    )


def render_forest_plot(studies: pd.DataFrame, pooled: pd.DataFrame, out_path: Path) -> None:
    studies = studies.reset_index(drop=True)
    pooled_row = pooled.iloc[0]
    labels = studies["title"].map(
        {
            "Effect of long-term caloric restriction on DNA methylation measures of biological aging in healthy adults from the CALERIE trial.": "CALERIE",
            "Individual and additive effects of vitamin D, omega-3 and exercise on DNA methylation clocks of biological aging in older adults from the DO-HEALTH trial.": "DO-HEALTH",
        }
    ).fillna(studies["title"]).tolist() + ["Pooled effect"]
    effects = studies["effect_estimate"].astype(float).tolist() + [float(pooled_row["random_effect_estimate"])]
    lowers = studies["ci_lower"].astype(float).tolist() + [float(pooled_row["random_effect_ci_lower"])]
    uppers = studies["ci_upper"].astype(float).tolist() + [float(pooled_row["random_effect_ci_upper"])]
    y = list(range(len(labels), 0, -1))

    fig, ax = plt.subplots(figsize=(8.5, 3.8))
    ax.axvline(0, color="0.6", linestyle="--", linewidth=1)

    for idx, yi in enumerate(y):
        effect = effects[idx]
        low = lowers[idx]
        high = uppers[idx]
        marker = "D" if idx == len(labels) - 1 else "o"
        size = 70 if idx == len(labels) - 1 else 45
        color = "black" if idx == len(labels) - 1 else "#1f4e79"
        ax.errorbar(
            effect,
            yi,
            xerr=[[effect - low], [high - effect]],
            fmt=marker,
            color=color,
            ecolor=color,
            elinewidth=1.8,
            capsize=3,
            markersize=size ** 0.5,
        )

    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Standardized effect on DunedinPACE (negative favors slower pace of ageing)")
    ax.set_title("Primary Peer-Reviewed DunedinPACE Meta-analysis")
    ax.set_ylim(0.5, len(labels) + 0.7)
    ax.grid(axis="x", color="0.9", linewidth=0.8)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.tick_params(axis="y", length=0)

    summary_text = (
        f"Pooled effect {float(pooled_row['random_effect_estimate']):.3f} "
        f"(95% CI {float(pooled_row['random_effect_ci_lower']):.3f} to {float(pooled_row['random_effect_ci_upper']):.3f}); "
        f"I2 = {float(pooled_row['i_squared_percent']):.0f}%"
    )
    fig.text(0.12, 0.02, summary_text, fontsize=9)
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    args = parse_args()
    load_config(args.config)
    root = _root_from_config(args.config)

    tables_dir = root / "results" / "meta_addon" / "tables"
    figs_dir = root / "results" / "meta_addon" / "figures"
    figs_dir.mkdir(parents=True, exist_ok=True)

    inputs = pd.read_csv(tables_dir / "meta_same_outcome_pooling_inputs.csv")
    pooled = pd.read_csv(tables_dir / "meta_same_outcome_pooling_results.csv")

    study_subset = inputs[
        (inputs["endpoint_family"] == "epigenetic_biological_age")
        & (inputs["effect_metric"] == "cohens_d_standardized_change_difference")
        & (inputs["outcome_name"] == "DunedinPACE")
    ].copy()
    pooled_subset = pooled[
        (pooled["endpoint_family"] == "epigenetic_biological_age")
        & (pooled["effect_metric"] == "cohens_d_standardized_change_difference")
        & (pooled["outcome_name"] == "DunedinPACE")
    ].copy()

    if study_subset.empty or pooled_subset.empty:
        raise SystemExit("No DunedinPACE primary-pool rows available to render.")

    study_table = build_study_table(study_subset)
    summary_table = build_summary_table(pooled_subset)
    study_table.to_csv(tables_dir / "primary_dunedinpace_pool_studies.csv", index=False)
    summary_table.to_csv(tables_dir / "primary_dunedinpace_pool_summary.csv", index=False)
    render_forest_plot(study_subset, pooled_subset, figs_dir / "forest_dunedinpace_primary.png")


if __name__ == "__main__":
    main()
