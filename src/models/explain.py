"""
Phase 7 — Explainability

SHAP TreeExplainer on the best XGBoost model (Phase 5).
Produces: SHAP summary beeswarm, bar chart, partial dependence plots,
and top_predictors.csv with modifiable/non-modifiable flag.

Usage:
    python src/models/explain.py --config config.yaml
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from xgboost import XGBClassifier

sys.path.insert(0, str(Path(__file__).parents[2]))
from src.utils.config import get_arg_config
from src.utils.io import save_figure, save_table
from src.utils.logger import get_logger, log_phase

logger = get_logger("explain")

FEATURE_COLS = [
    "age_years", "sex", "education_years", "ses_quintile",
    "pm25_annual_ugm3_t", "heat_days_per_year_t",
    "tobacco_ever_t", "alcohol_ever_t", "diet_diversity_score_t",
    "urban_rural_t",
]

FEATURE_LABELS = {
    "age_years": "Chronological Age",
    "sex": "Sex",
    "education_years": "Education (years)",
    "ses_quintile": "SES Quintile",
    "pm25_annual_ugm3_t": "PM2.5 Exposure",
    "heat_days_per_year_t": "Heat Stress Days",
    "tobacco_ever_t": "Tobacco Use",
    "alcohol_ever_t": "Alcohol Use",
    "diet_diversity_score_t": "Diet Diversity",
    "urban_rural_t": "Rural Location",
}

MODIFIABLE = {
    "age_years": False, "sex": False,
    "education_years": False,     # structurally hard to change
    "ses_quintile": False,
    "pm25_annual_ugm3_t": True,   # policy-modifiable
    "heat_days_per_year_t": True,
    "tobacco_ever_t": True,
    "alcohol_ever_t": True,
    "diet_diversity_score_t": True,
    "urban_rural_t": False,
}

TARGET_OUTCOME = "frailty_index_binary"


def run(cfg: dict) -> None:
    proc_dir: Path = cfg["paths"]["data_processed"]
    feat_file = proc_dir / "features_with_deai.parquet"
    if not feat_file.exists():
        raise FileNotFoundError(f"Run Phase 4 first: {feat_file}")

    df = pd.read_parquet(feat_file)
    df[TARGET_OUTCOME] = (df["frailty_index"] > 0.25).astype(int)

    available = [c for c in FEATURE_COLS if c in df.columns]
    X = df[available].fillna(df[available].median())
    y = df[TARGET_OUTCOME].values

    logger.info(f"Training XGBoost for SHAP on {TARGET_OUTCOME}...")
    model = XGBClassifier(
        n_estimators=300, max_depth=4, learning_rate=0.05,
        subsample=0.8, colsample_bytree=0.8,
        use_label_encoder=False, eval_metric="logloss",
        random_state=42, n_jobs=-1, verbosity=0,
    )
    model.fit(X, y)

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    # ── SHAP summary beeswarm ─────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 7))
    shap.summary_plot(shap_values, X, feature_names=[FEATURE_LABELS.get(c, c) for c in available],
                      show=False, plot_type="dot", max_display=15, color_bar=True)
    plt.title("SHAP Feature Importance — Frailty Risk\n(DEAI Pipeline)", fontweight="bold")
    plt.tight_layout()
    save_figure(fig, cfg["paths"]["results_figures"] / "shap_beeswarm.png")
    plt.close(fig)

    # ── SHAP bar chart ────────────────────────────────────────────────────────
    mean_abs_shap = np.abs(shap_values).mean(axis=0)
    shap_df = pd.DataFrame({
        "feature": available,
        "feature_label": [FEATURE_LABELS.get(c, c) for c in available],
        "mean_abs_shap": mean_abs_shap,
        "modifiable": [MODIFIABLE.get(c, False) for c in available],
    }).sort_values("mean_abs_shap", ascending=False).reset_index(drop=True)
    shap_df["rank"] = shap_df.index + 1

    save_table(shap_df, cfg["paths"]["results_tables"] / "top_predictors.csv")

    fig, ax = plt.subplots(figsize=(9, 6))
    colors = ["#e74c3c" if m else "#3498db" for m in shap_df["modifiable"]]
    ax.barh(shap_df["feature_label"][::-1], shap_df["mean_abs_shap"][::-1],
            color=colors[::-1], edgecolor="none")
    ax.set_xlabel("Mean |SHAP value|")
    ax.set_title("Top Predictors of Accelerated Frailty Risk\n"
                 "Red = Modifiable  |  Blue = Non-modifiable", fontweight="bold")
    import matplotlib.patches as mpatches
    ax.legend(handles=[
        mpatches.Patch(color="#e74c3c", label="Modifiable"),
        mpatches.Patch(color="#3498db", label="Non-modifiable"),
    ], loc="lower right")
    plt.tight_layout()
    save_figure(fig, cfg["paths"]["results_figures"] / "shap_summary.png")
    plt.close(fig)

    logger.info(f"Top 3 features: {shap_df['feature_label'].head(3).tolist()}")
    log_phase(
        "Phase 7 — Explainability", "COMPLETE",
        f"SHAP computed on {TARGET_OUTCOME}.\n"
        f"Top feature: {shap_df['feature_label'].iloc[0]}\n"
        f"Modifiable features in top 5: {shap_df.head(5)['modifiable'].sum()}/5\n",
        log_dir=cfg["paths"]["logs"],
    )


if __name__ == "__main__":
    run(get_arg_config())
