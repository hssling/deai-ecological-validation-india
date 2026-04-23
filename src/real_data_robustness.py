"""
Robustness checks for real state-level LASI DEAI analysis.

The real-data analysis is ecological (state/UT level), so reliability depends on
showing that the main findings are not artifacts of the national India row,
single-state influence, or uncorrected multiple comparisons.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

sys.path.insert(0, str(Path(__file__).parents[2]))
from src.models.deai_real import EXPOSOME_VARS, OUTCOME_VARS
from src.utils.config import get_arg_config
from src.utils.io import save_table
from src.utils.logger import get_logger, log_phase

logger = get_logger("real_data_robustness")


def spearman(x: pd.Series, y: pd.Series) -> tuple[float, float, int]:
    valid = pd.concat([x, y], axis=1).dropna()
    if len(valid) < 8:
        return np.nan, np.nan, len(valid)
    r, p = stats.spearmanr(valid.iloc[:, 0], valid.iloc[:, 1])
    return float(r), float(p), len(valid)


def bootstrap_spearman(
    df: pd.DataFrame,
    outcome: str,
    *,
    n_boot: int = 5000,
    seed: int = 42,
) -> tuple[float, float]:
    valid = df[["deai_real_z", outcome]].dropna().reset_index(drop=True)
    if len(valid) < 8:
        return np.nan, np.nan
    rng = np.random.default_rng(seed)
    estimates = []
    n = len(valid)
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        sample = valid.iloc[idx]
        if sample["deai_real_z"].nunique() < 2 or sample[outcome].nunique() < 2:
            continue
        estimates.append(stats.spearmanr(sample["deai_real_z"], sample[outcome]).statistic)
    if not estimates:
        return np.nan, np.nan
    lo, hi = np.percentile(estimates, [2.5, 97.5])
    return float(lo), float(hi)


def leave_one_out(df: pd.DataFrame, outcome: str) -> dict[str, object]:
    rows = []
    for state in df["state"]:
        sub = df[df["state"] != state]
        r, p, n = spearman(sub["deai_real_z"], sub[outcome])
        rows.append({"excluded_state": state, "rho": r, "p_value": p, "n": n})
    loo = pd.DataFrame(rows).dropna(subset=["rho"])
    if loo.empty:
        return {
            "loo_min_rho": np.nan,
            "loo_max_rho": np.nan,
            "most_influential_state": "",
            "max_abs_delta": np.nan,
        }
    full_r, _, _ = spearman(df["deai_real_z"], df[outcome])
    loo["abs_delta"] = (loo["rho"] - full_r).abs()
    influential = loo.sort_values("abs_delta", ascending=False).iloc[0]
    return {
        "loo_min_rho": round(float(loo["rho"].min()), 3),
        "loo_max_rho": round(float(loo["rho"].max()), 3),
        "most_influential_state": influential["excluded_state"],
        "max_abs_delta": round(float(influential["abs_delta"]), 3),
    }


def cronbach_alpha(items: pd.DataFrame) -> float:
    clean = items.dropna(axis=1, how="all").copy()
    clean = clean.fillna(clean.median(numeric_only=True))
    if clean.shape[1] < 2:
        return np.nan
    item_vars = clean.var(axis=0, ddof=1)
    total_var = clean.sum(axis=1).var(ddof=1)
    if total_var == 0:
        return np.nan
    k = clean.shape[1]
    return float((k / (k - 1)) * (1 - item_vars.sum() / total_var))


def component_diagnostics(df: pd.DataFrame) -> pd.DataFrame:
    cols = [c for c in EXPOSOME_VARS if c in df.columns]
    rows = []
    for col in cols:
        r, p, n = spearman(df[col], df["deai_real_z"])
        rows.append(
            {
                "component": col,
                "label": EXPOSOME_VARS[col]["label"].replace("\n", " "),
                "weight": EXPOSOME_VARS[col]["weight"],
                "spearman_with_deai": round(r, 3),
                "p_value": round(p, 4),
                "n_states": n,
            }
        )
    return pd.DataFrame(rows).sort_values("spearman_with_deai", ascending=False)


def run(cfg: dict) -> None:
    tables = cfg["paths"]["results_tables"]
    df = pd.read_csv(tables / "lasi_with_deai_real.csv")
    state_df = df[df["state"].str.upper() != "INDIA"].copy()

    outcomes = [c for c in OUTCOME_VARS if c in df.columns]
    rows = []
    for outcome in outcomes:
        r_all, p_all, n_all = spearman(df["deai_real_z"], df[outcome])
        r_state, p_state, n_state = spearman(state_df["deai_real_z"], state_df[outcome])
        lo, hi = bootstrap_spearman(state_df, outcome)
        loo = leave_one_out(state_df, outcome)
        rows.append(
            {
                "outcome": outcome,
                "outcome_label": OUTCOME_VARS[outcome],
                "rho_including_india": round(r_all, 3),
                "p_including_india": round(p_all, 4),
                "n_including_india": n_all,
                "rho_states_only": round(r_state, 3),
                "p_states_only": round(p_state, 4),
                "n_states_only": n_state,
                "bootstrap95_low_states_only": round(lo, 3),
                "bootstrap95_high_states_only": round(hi, 3),
                **loo,
            }
        )

    robust = pd.DataFrame(rows)
    robust["bh_q_states_only"] = multipletests(
        robust["p_states_only"].fillna(1.0), method="fdr_bh"
    )[1].round(4)
    robust["robust_direction"] = np.where(
        (np.sign(robust["rho_including_india"]) == np.sign(robust["rho_states_only"]))
        & (np.sign(robust["bootstrap95_low_states_only"]) == np.sign(robust["bootstrap95_high_states_only"])),
        "stable",
        "sensitive",
    )
    save_table(robust, tables / "deai_real_robustness.csv")

    components = component_diagnostics(state_df)
    save_table(components, tables / "deai_component_diagnostics.csv")

    cols = [c for c in EXPOSOME_VARS if c in state_df.columns]
    alpha = cronbach_alpha(state_df[cols])
    summary = pd.DataFrame(
        [
            {
                "metric": "states_only_n",
                "value": len(state_df),
                "interpretation": "State/UT rows after excluding national India row.",
            },
            {
                "metric": "deai_component_cronbach_alpha",
                "value": round(alpha, 3),
                "interpretation": "Internal consistency of adverse exposome components; moderate values are expected for a multi-domain index.",
            },
            {
                "metric": "mortality_states_only_rho",
                "value": robust.loc[
                    robust["outcome"] == "death_rate_60plus_per1000", "rho_states_only"
                ].iloc[0],
                "interpretation": "Primary real-data ecological validation signal.",
            },
            {
                "metric": "multimorbidity_states_only_rho",
                "value": robust.loc[
                    robust["outcome"] == "multimorbidity_index", "rho_states_only"
                ].iloc[0],
                "interpretation": "Transition/ascertainment signal; not interpreted as protective effect.",
            },
        ]
    )
    save_table(summary, tables / "deai_real_robustness_summary.csv")

    logger.info("Real-data robustness tables generated")
    log_phase(
        "Phase 4c - Real Data Robustness",
        "COMPLETE",
        f"States-only sensitivity: N={len(state_df)}\n"
        f"Mortality rho={summary.loc[summary['metric']=='mortality_states_only_rho','value'].iloc[0]}\n"
        f"Multimorbidity rho={summary.loc[summary['metric']=='multimorbidity_states_only_rho','value'].iloc[0]}\n"
        f"Component alpha={round(alpha, 3)}",
        log_dir=cfg["paths"]["logs"],
    )


if __name__ == "__main__":
    run(get_arg_config())
