"""
Phase 4 — DEAI Construction

Builds four DEAI score variants and compares them:
  1. knowledge_weighted  — linear combination using domain weights from config
  2. pca_based           — first principal component of standardized exposome
  3. elastic_net_score   — elastic-net regression score predicting frailty_index
  4. xgboost_risk_score  — XGBoost predicted probability → Z-scaled

Additionally computes age-acceleration residual = DEAI_primary - predicted_from_age.

Usage:
    python src/models/deai_build.py --config config.yaml
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.linear_model import ElasticNetCV
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor

sys.path.insert(0, str(Path(__file__).parents[2]))
from src.utils.config import get_arg_config
from src.utils.io import save_figure, save_table
from src.utils.logger import get_logger, log_phase

logger = get_logger("deai_build")

EXPOSOME_TRANSFORMED = [
    "pm25_annual_ugm3_t", "heat_days_per_year_t",
    "tobacco_ever_t", "alcohol_ever_t", "diet_diversity_score_t",
    "urban_rural_t", "ses_quintile_t", "education_years_t",
]
KNOWLEDGE_WEIGHTS = [0.20, 0.12, 0.18, 0.08, 0.15, 0.07, 0.12, 0.08]


def _knowledge_weighted(df: pd.DataFrame) -> pd.Series:
    X = df[EXPOSOME_TRANSFORMED].fillna(0).values
    w = np.array(KNOWLEDGE_WEIGHTS)
    w = w / w.sum()
    return pd.Series(X @ w, index=df.index, name="deai_knowledge_weighted")


def _pca_score(df: pd.DataFrame) -> pd.Series:
    X = df[EXPOSOME_TRANSFORMED].fillna(0).values
    pca = PCA(n_components=1, random_state=42)
    score = pca.fit_transform(X).ravel()
    # Ensure positive polarity (higher = more adverse)
    if np.corrcoef(score, df["frailty_index"].fillna(0))[0, 1] < 0:
        score = -score
    return pd.Series(score, index=df.index, name="deai_pca")


def _elastic_net_score(df: pd.DataFrame) -> pd.Series:
    X = df[EXPOSOME_TRANSFORMED].fillna(0).values
    y = df["frailty_index"].fillna(df["frailty_index"].median()).values
    l1_ratios = [0.1, 0.5, 0.7, 0.9, 0.95, 1.0]
    en = ElasticNetCV(l1_ratio=l1_ratios, cv=5, max_iter=10000, random_state=42)
    en.fit(X, y)
    logger.info(f"ElasticNet best l1_ratio={en.l1_ratio_:.2f}, alpha={en.alpha_:.4f}")
    return pd.Series(en.predict(X), index=df.index, name="deai_elastic_net")


def _xgboost_score(df: pd.DataFrame, cfg: dict) -> pd.Series:
    X = df[EXPOSOME_TRANSFORMED].fillna(0).values
    y = df["frailty_index"].fillna(df["frailty_index"].median()).values
    xgb_params = cfg.get("models", {}).get("xgboost", {})
    model = XGBRegressor(
        n_estimators=xgb_params.get("n_estimators", 300),
        max_depth=xgb_params.get("max_depth", 4),
        learning_rate=xgb_params.get("learning_rate", 0.05),
        subsample=xgb_params.get("subsample", 0.8),
        colsample_bytree=xgb_params.get("colsample_bytree", 0.8),
        random_state=42,
        n_jobs=-1,
        verbosity=0,
    )
    model.fit(X, y)
    return pd.Series(model.predict(X), index=df.index, name="deai_xgboost")


def _standardize(s: pd.Series) -> pd.Series:
    return (s - s.mean()) / s.std()


def _age_acceleration(deai: pd.Series, age: pd.Series) -> pd.Series:
    """Residual of DEAI regressed on chronological age."""
    from sklearn.linear_model import LinearRegression
    lr = LinearRegression()
    lr.fit(age.values.reshape(-1, 1), deai.values)
    predicted = lr.predict(age.values.reshape(-1, 1))
    return pd.Series(deai.values - predicted, index=deai.index,
                     name="deai_age_acceleration")


def build_deai(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    logger.info("Building DEAI versions...")
    scores = pd.DataFrame(index=df.index)
    scores["deai_knowledge_weighted"] = _standardize(_knowledge_weighted(df))
    scores["deai_pca"] = _standardize(_pca_score(df))
    scores["deai_elastic_net"] = _standardize(_elastic_net_score(df))
    scores["deai_xgboost"] = _standardize(_xgboost_score(df, cfg))
    scores["deai_age_acceleration"] = _age_acceleration(
        scores["deai_xgboost"], df["age_years"]
    )

    # Correlation matrix between DEAI versions
    corr = scores[["deai_knowledge_weighted", "deai_pca",
                   "deai_elastic_net", "deai_xgboost"]].corr(method="spearman")
    logger.info(f"DEAI inter-version Spearman correlations:\n{corr.round(3)}")
    return scores, corr


def plot_deai_distribution(scores: pd.DataFrame, out_path: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.ravel()
    versions = ["deai_knowledge_weighted", "deai_pca",
                "deai_elastic_net", "deai_xgboost"]
    labels = ["Knowledge-weighted", "PCA-based",
              "Elastic-net", "XGBoost risk score"]
    palette = sns.color_palette("muted", 4)
    for ax, ver, lab, col in zip(axes, versions, labels, palette):
        ax.hist(scores[ver].dropna(), bins=50, color=col, alpha=0.75, edgecolor="none")
        ax.axvline(0, color="black", lw=1, ls="--")
        ax.set_title(f"DEAI: {lab}", fontsize=11, fontweight="bold")
        ax.set_xlabel("Standardized score (SD units)")
        ax.set_ylabel("Count")
        sns.despine(ax=ax)
    fig.suptitle("Distribution of DEAI Versions\n(Higher = Greater Adverse Exposome Burden)",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    save_figure(fig, out_path)
    plt.close(fig)


def run(cfg: dict) -> None:
    proc_dir: Path = cfg["paths"]["data_processed"]
    features_file = proc_dir / "features_master.parquet"
    if not features_file.exists():
        raise FileNotFoundError(f"Run Phase 3 first: {features_file}")

    df = pd.read_parquet(features_file)
    scores, corr = build_deai(df, cfg)

    # Merge back into feature dataframe and save
    df_out = pd.concat([df, scores], axis=1)
    save_table(df_out, proc_dir / "features_with_deai.parquet")

    # Comparison table
    comparison = scores.describe().T
    comparison["spearman_vs_frailty"] = [
        df["frailty_index"].corr(scores[c], method="spearman")
        for c in scores.columns
    ]
    save_table(comparison.reset_index(), cfg["paths"]["results_tables"] / "deai_versions_comparison.csv")
    save_table(corr.reset_index(), cfg["paths"]["results_tables"] / "deai_intercorrelations.csv")

    plot_deai_distribution(scores, cfg["paths"]["results_figures"] / "deai_distribution.png")
    logger.info("DEAI figures saved")

    log_phase(
        "Phase 4 — DEAI Construction", "COMPLETE",
        "Four DEAI versions constructed and standardized.\n"
        f"Primary version: {cfg.get('deai', {}).get('primary_version', 'xgboost_risk_score')}\n"
        f"Age-acceleration residual computed.\n",
        log_dir=cfg["paths"]["logs"],
    )


if __name__ == "__main__":
    run(get_arg_config())
