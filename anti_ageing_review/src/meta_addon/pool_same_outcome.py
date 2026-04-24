from __future__ import annotations

import argparse
import math

import pandas as pd

from src.utils.io import append_log, load_config, save_csv


def _months_from_timepoint(value: str) -> float:
    text = str(value).lower()
    if "36_month" in text:
        return 36
    if "24_month" in text:
        return 24
    if "18_month" in text:
        return 18
    if "12_month" in text:
        return 12
    if "6_month" in text:
        return 6
    if "6_week" in text:
        return 1.5
    if "12_week" in text:
        return 3
    return 0


def _analysis_priority(value: str) -> int:
    text = str(value).lower()
    if "tot" in text:
        return 0
    if "main_effect" in text:
        return 2
    if "itt" in text:
        return 2
    return 1


def _fixed_effect(subset: pd.DataFrame) -> tuple[float, float]:
    weights = 1.0 / (subset["effect_se"] ** 2)
    pooled = (weights * subset["effect_estimate"]).sum() / weights.sum()
    se = math.sqrt(1.0 / weights.sum())
    return pooled, se


def _random_effect(subset: pd.DataFrame) -> tuple[float, float, float]:
    weights_fe = 1.0 / (subset["effect_se"] ** 2)
    pooled_fe = (weights_fe * subset["effect_estimate"]).sum() / weights_fe.sum()
    q = (weights_fe * (subset["effect_estimate"] - pooled_fe) ** 2).sum()
    df = max(len(subset) - 1, 1)
    c = weights_fe.sum() - ((weights_fe ** 2).sum() / weights_fe.sum())
    tau_sq = max((q - df) / c, 0.0) if c > 0 else 0.0
    weights_re = 1.0 / ((subset["effect_se"] ** 2) + tau_sq)
    pooled_re = (weights_re * subset["effect_estimate"]).sum() / weights_re.sum()
    se_re = math.sqrt(1.0 / weights_re.sum())
    return pooled_re, se_re, tau_sq


def run(cfg: dict) -> None:
    tables = cfg["paths"]["meta_addon_tables"]
    primary = pd.read_csv(tables / "meta_dataset_primary_pooling.csv")
    eligible = primary[
        primary["effect_metric"].eq("cohens_d_standardized_change_difference")
        & primary["effect_estimate"].notna()
        & primary["effect_se"].notna()
    ].copy()
    eligible["months"] = eligible["outcome_timepoint"].map(_months_from_timepoint)
    eligible["analysis_priority"] = eligible["outcome_timepoint"].map(_analysis_priority)
    selected = (
        eligible.sort_values(
            ["study_id", "outcome_name", "analysis_priority", "months"],
            ascending=[True, True, False, False],
        )
        .drop_duplicates(subset=["study_id", "outcome_name"], keep="first")
        .copy()
    )
    save_csv(selected, tables / "meta_same_outcome_pooling_inputs.csv")

    poolable = (
        selected.groupby(["endpoint_family", "effect_metric", "outcome_name"], dropna=False)
        .filter(lambda frame: frame["study_id"].nunique() >= 2)
        .copy()
    )

    rows: list[dict[str, object]] = []
    for (endpoint_family, effect_metric, outcome_name), subset in poolable.groupby(
        ["endpoint_family", "effect_metric", "outcome_name"], dropna=False
    ):
        pooled_fe, se_fe = _fixed_effect(subset)
        pooled_re, se_re, tau_sq = _random_effect(subset)
        q = float(((1.0 / (subset["effect_se"] ** 2)) * (subset["effect_estimate"] - pooled_fe) ** 2).sum())
        df_q = max(len(subset) - 1, 1)
        i_sq = max((q - df_q) / q, 0.0) * 100 if q > 0 else 0.0
        rows.append(
            {
                "endpoint_family": endpoint_family,
                "effect_metric": effect_metric,
                "outcome_name": outcome_name,
                "n_studies": subset["study_id"].nunique(),
                "study_ids": "; ".join(subset["study_id"].astype(str).tolist()),
                "fixed_effect_estimate": pooled_fe,
                "fixed_effect_se": se_fe,
                "fixed_effect_ci_lower": pooled_fe - 1.96 * se_fe,
                "fixed_effect_ci_upper": pooled_fe + 1.96 * se_fe,
                "random_effect_estimate": pooled_re,
                "random_effect_se": se_re,
                "random_effect_ci_lower": pooled_re - 1.96 * se_re,
                "random_effect_ci_upper": pooled_re + 1.96 * se_re,
                "tau_sq": tau_sq,
                "q_statistic": q,
                "i_squared_percent": i_sq,
            }
        )
    results = pd.DataFrame(rows)
    save_csv(results, tables / "meta_same_outcome_pooling_results.csv")

    append_log(
        cfg["paths"]["logs"] / "progress.md",
        "Phase 24 - Same-outcome pooled estimates",
        "- Selected one primary non-TOT row per study and outcome from the standardized-effect subset.\n- Generated a same-outcome pooling input table.\n- Computed fixed-effect and random-effects pooled estimates for any outcome with at least two independent studies.",
        "- results/meta_addon/tables/meta_same_outcome_pooling_inputs.csv\n- results/meta_addon/tables/meta_same_outcome_pooling_results.csv",
        "- Continue extracting additional same-outcome standardized DNAm rows to strengthen biological-age pooling beyond DunedinPACE.\n- Add manuscript text for the pooled DunedinPACE estimate only after manual review of compatibility assumptions.",
        "- Current same-outcome pooling is limited by the small number of studies and should be treated as exploratory.\n- Outcome-version compatibility still requires judgment, especially for PhenoAge variants.",
        "python -m src.meta_addon.pool_same_outcome --config config/meta_addon_config.yaml",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/meta_addon_config.yaml")
    run(load_config(parser.parse_args().config))
