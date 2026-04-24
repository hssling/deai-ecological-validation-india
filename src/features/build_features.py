"""
Phase 3 — Feature Engineering
Loads raw/processed data, applies transformations, and writes
data_processed/features_master.parquet with a complete variable map.

Usage:
    python src/features/build_features.py --config config.yaml
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).parents[2]))
from src.utils.config import get_arg_config
from src.utils.io import save_table
from src.utils.logger import get_logger, log_phase

logger = get_logger("build_features")


# ── Exposome variable definitions ────────────────────────────────────────────

EXPOSOME_VARS = {
    "pm25_annual_ugm3": {
        "domain": "air_pollution",
        "transform": "log1p",
        "direction": "adverse",
        "weight_knowledge": 0.20,
    },
    "heat_days_per_year": {
        "domain": "heat_stress",
        "transform": "sqrt",
        "direction": "adverse",
        "weight_knowledge": 0.12,
    },
    "tobacco_ever": {
        "domain": "lifestyle_tobacco",
        "transform": "none",
        "direction": "adverse",
        "weight_knowledge": 0.18,
    },
    "alcohol_ever": {
        "domain": "lifestyle_alcohol",
        "transform": "none",
        "direction": "adverse",
        "weight_knowledge": 0.08,
    },
    "diet_diversity_score": {
        "domain": "lifestyle_diet",
        "transform": "none",
        "direction": "protective",
        "weight_knowledge": 0.15,
    },
    "urban_rural": {
        "domain": "built_environment",
        "transform": "none",
        "direction": "protective",
        "weight_knowledge": 0.07,
    },
    "ses_quintile": {
        "domain": "ses_income_proxy",
        "transform": "none",
        "direction": "protective",
        "weight_knowledge": 0.12,
    },
    "education_years": {
        "domain": "ses_education",
        "transform": "none",
        "direction": "protective",
        "weight_knowledge": 0.08,
    },
}

OUTCOME_VARS = [
    "frailty_index",
    "multimorbidity_binary",
    "disability_binary",
    "srh_poor_binary",
    "mortality_5yr_binary",
]

COVARIATE_VARS = [
    "age_years", "sex", "education_years", "ses_quintile",
    "region", "tobacco_ever", "alcohol_ever",
]


def _apply_transform(series: pd.Series, transform: str) -> pd.Series:
    if transform == "log1p":
        return np.log1p(series)
    elif transform == "sqrt":
        return np.sqrt(series.clip(0))
    return series


def build_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns (features_df, variable_map_df).
    features_df has standardized exposome features + raw outcomes + covariates.
    """
    feature_df = df.copy()
    var_map_rows = []

    scaler = StandardScaler()
    transformed_cols = []

    for col, meta in EXPOSOME_VARS.items():
        if col not in feature_df.columns:
            logger.warning(f"Column {col!r} missing — filling with NaN")
            feature_df[col] = np.nan

        t_col = f"{col}_t"
        feature_df[t_col] = _apply_transform(feature_df[col], meta["transform"])
        transformed_cols.append(t_col)

        var_map_rows.append({
            "variable": col,
            "transformed_name": t_col,
            "domain": meta["domain"],
            "transform": meta["transform"],
            "direction": meta["direction"],
            "knowledge_weight": meta["weight_knowledge"],
            "type": "exposome",
        })

    # Standardize all transformed exposome columns
    feature_df[transformed_cols] = scaler.fit_transform(
        feature_df[transformed_cols].fillna(feature_df[transformed_cols].median())
    )

    # Flip protective variables so higher = more adverse (for composite scoring)
    for col, meta in EXPOSOME_VARS.items():
        t_col = f"{col}_t"
        if meta["direction"] == "protective":
            feature_df[t_col] = -feature_df[t_col]

    # Add outcome and covariate metadata
    for col in OUTCOME_VARS:
        var_map_rows.append({"variable": col, "transformed_name": col,
                              "domain": "outcome", "transform": "none",
                              "direction": "adverse", "knowledge_weight": np.nan,
                              "type": "outcome"})
    for col in COVARIATE_VARS:
        var_map_rows.append({"variable": col, "transformed_name": col,
                              "domain": "covariate", "transform": "none",
                              "direction": "na", "knowledge_weight": np.nan,
                              "type": "covariate"})

    var_map = pd.DataFrame(var_map_rows)
    return feature_df, var_map


def run(cfg: dict) -> None:
    raw_dir: Path = cfg["paths"]["data_raw"]
    proc_dir: Path = cfg["paths"]["data_processed"]

    cohort_file = raw_dir / "synthetic_cohort.parquet"
    if not cohort_file.exists():
        raise FileNotFoundError(
            f"Cohort not found at {cohort_file}. Run Phase 2 first:\n"
            "  python src/ingest/build_synthetic_cohort.py --config config.yaml"
        )

    df = pd.read_parquet(cohort_file)
    logger.info(f"Loaded cohort: {len(df)} rows × {len(df.columns)} cols")

    feature_df, var_map = build_features(df)

    save_table(feature_df, proc_dir / "features_master.parquet")
    save_table(var_map, cfg["paths"]["results_tables"] / "variable_map.csv")
    logger.info(f"Features saved → {proc_dir / 'features_master.parquet'}")

    log_phase(
        "Phase 3 — Feature Engineering", "COMPLETE",
        f"Exposome variables: {len(EXPOSOME_VARS)}\n"
        f"Outcome variables: {len(OUTCOME_VARS)}\n"
        f"Total features in matrix: {len(feature_df.columns)}",
        log_dir=cfg["paths"]["logs"],
    )


if __name__ == "__main__":
    run(get_arg_config())
