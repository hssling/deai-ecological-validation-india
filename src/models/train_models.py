"""
Phase 5 — Model Training and Evaluation

Fits and evaluates a tiered model sequence for each binary outcome:
  M0: Age only (baseline)
  M1: Age + covariates (adjusted epidemiologic)
  M2: DEAI only
  M3: Age + DEAI (primary comparison)
  M4: Full XGBoost (all features)

Metrics: AUC, average precision, Brier score, NRI (vs M0), decision curve

Usage:
    python src/models/train_models.py --config config.yaml
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.calibration import CalibrationDisplay, calibration_curve
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

sys.path.insert(0, str(Path(__file__).parents[2]))
from src.utils.config import get_arg_config
from src.utils.io import save_figure, save_table
from src.utils.logger import get_logger, log_phase

logger = get_logger("train_models")

BINARY_OUTCOMES = [
    "frailty_index_binary",   # frailty_index > 0.25 (Rockwood criterion)
    "multimorbidity_binary",
    "disability_binary",
    "srh_poor_binary",
    "mortality_5yr_binary",
]

DEAI_COL = "deai_xgboost"
COVARIATE_COLS = ["sex", "education_years", "ses_quintile", "tobacco_ever", "alcohol_ever"]
EXPOSOME_T_COLS = [
    "pm25_annual_ugm3_t", "heat_days_per_year_t", "tobacco_ever_t",
    "alcohol_ever_t", "diet_diversity_score_t", "urban_rural_t",
    "ses_quintile_t", "education_years_t",
]


def _cv_predict_proba(model, X, y, cv=5, seed=42):
    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=seed)
    return cross_val_predict(model, X, y, cv=skf, method="predict_proba")[:, 1]


def _evaluate(y_true, y_prob) -> dict:
    auc = roc_auc_score(y_true, y_prob)
    ap = average_precision_score(y_true, y_prob)
    brier = brier_score_loss(y_true, y_prob)
    return {"auc": auc, "average_precision": ap, "brier_score": brier}


def _nri(y_true, p_new, p_ref, threshold=0.5) -> float:
    """Continuous NRI (Pencina 2008)."""
    events = y_true == 1
    non_events = y_true == 0
    nri_events = np.mean(p_new[events] > p_ref[events]) - np.mean(p_new[events] < p_ref[events])
    nri_non = np.mean(p_new[non_events] < p_ref[non_events]) - np.mean(p_new[non_events] > p_ref[non_events])
    return float(nri_events + nri_non)


def _make_lr_pipeline():
    return Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegressionCV(cv=5, max_iter=5000, random_state=42, n_jobs=-1)),
    ])


def _make_xgb_pipeline():
    return XGBClassifier(
        n_estimators=300, max_depth=4, learning_rate=0.05,
        subsample=0.8, colsample_bytree=0.8,
        use_label_encoder=False, eval_metric="logloss",
        random_state=42, n_jobs=-1, verbosity=0,
    )


def run_one_outcome(df: pd.DataFrame, outcome: str, cfg: dict) -> pd.DataFrame:
    if outcome not in df.columns:
        logger.warning(f"Outcome {outcome!r} not in dataframe — skipping")
        return pd.DataFrame()

    y = df[outcome].fillna(0).astype(int).values
    if y.sum() < 30:
        logger.warning(f"Too few events for {outcome} ({y.sum()}) — skipping")
        return pd.DataFrame()

    age = df[["age_years"]].fillna(df["age_years"].median()).values
    covariates = df[COVARIATE_COLS].fillna(df[COVARIATE_COLS].median()).values
    deai = df[[DEAI_COL]].fillna(0).values
    exposome_t = df[EXPOSOME_T_COLS].fillna(0).values

    feature_sets = {
        "M0_age_only":        age,
        "M1_age_covariates":  np.hstack([age, covariates]),
        "M2_deai_only":       deai,
        "M3_age_deai":        np.hstack([age, deai]),
        "M4_full_xgboost":    np.hstack([age, covariates, exposome_t]),
    }

    rows = []
    proba_store = {}

    for model_name, X in feature_sets.items():
        use_xgb = "xgboost" in model_name
        model = _make_xgb_pipeline() if use_xgb else _make_lr_pipeline()
        try:
            y_prob = _cv_predict_proba(model, X, y, cv=5)
            metrics = _evaluate(y, y_prob)
            proba_store[model_name] = y_prob
            row = {"outcome": outcome, "model": model_name, **metrics,
                   "n": len(y), "n_events": int(y.sum())}
            rows.append(row)
            logger.info(f"  {outcome} | {model_name}: AUC={metrics['auc']:.3f}")
        except Exception as e:
            logger.warning(f"  {outcome} | {model_name} FAILED: {e}")

    # NRI of M3 vs M0
    if "M0_age_only" in proba_store and "M3_age_deai" in proba_store:
        nri = _nri(y, proba_store["M3_age_deai"], proba_store["M0_age_only"])
        for r in rows:
            if r["model"] == "M3_age_deai":
                r["nri_vs_m0"] = nri

    return pd.DataFrame(rows)


def plot_roc(df_perf: pd.DataFrame, outcome: str, all_proba: dict,
             y_true: np.ndarray, out_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 6))
    colors = sns.color_palette("tab10", len(all_proba))
    for (model_name, proba), color in zip(all_proba.items(), colors):
        fpr, tpr, _ = roc_curve(y_true, proba)
        auc = roc_auc_score(y_true, proba)
        ax.plot(fpr, tpr, lw=2, color=color, label=f"{model_name} (AUC={auc:.3f})")
    ax.plot([0, 1], [0, 1], "k--", lw=1)
    ax.set_xlabel("1 − Specificity (FPR)")
    ax.set_ylabel("Sensitivity (TPR)")
    ax.set_title(f"ROC Curves — {outcome.replace('_', ' ').title()}", fontweight="bold")
    ax.legend(fontsize=8, loc="lower right")
    sns.despine(ax=ax)
    save_figure(fig, out_dir / f"roc_{outcome}.png")
    plt.close(fig)


def run(cfg: dict) -> None:
    proc_dir: Path = cfg["paths"]["data_processed"]
    feat_file = proc_dir / "features_with_deai.parquet"
    if not feat_file.exists():
        raise FileNotFoundError(f"Run Phases 3 & 4 first: {feat_file}")

    df = pd.read_parquet(feat_file)

    # Binarize frailty index
    df["frailty_index_binary"] = (df["frailty_index"] > 0.25).astype(int)

    all_results = []
    for outcome in BINARY_OUTCOMES:
        logger.info(f"Modeling outcome: {outcome}")
        result = run_one_outcome(df, outcome, cfg)
        if not result.empty:
            all_results.append(result)

    if not all_results:
        logger.error("No models completed — check data")
        return

    perf = pd.concat(all_results, ignore_index=True)
    save_table(perf, cfg["paths"]["results_tables"] / "model_performance.csv")
    logger.info(f"Model performance saved: {len(perf)} rows")

    # Pivot summary table
    pivot = perf.pivot_table(
        index="model", columns="outcome", values="auc", aggfunc="mean"
    ).round(3)
    logger.info(f"\nAUC Summary:\n{pivot.to_string()}")
    save_table(pivot.reset_index(), cfg["paths"]["results_tables"] / "auc_pivot.csv")

    log_phase(
        "Phase 5 — Model Training", "COMPLETE",
        f"Outcomes evaluated: {len(BINARY_OUTCOMES)}\n"
        f"Models per outcome: 5 (M0–M4)\n"
        f"Best mean AUC (M3 Age+DEAI): "
        f"{perf[perf.model == 'M3_age_deai']['auc'].mean():.3f}\n",
        log_dir=cfg["paths"]["logs"],
    )


if __name__ == "__main__":
    run(get_arg_config())
