"""Phase 9 (Path-C, A3 amendment): subgroup pooling and meta-regression with honest gates.

Gates:
  - subgroup pool requires k>=3 per stratum (relaxed to k>=2 for narrative when total k=3)
  - meta-regression requires k>=10 per clock

For the DunedinPACE k=3 dataset most strata will fail. Each failing stratum is
emitted as a row with `status=gate_failed` and a transparent reason.

Outputs:
  results/tables/subgroup_metareg_2026-05-18.csv
  docs/subgroup_metareg_gate_report_path_c_2026-05-18.md
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).parent))
from _common import ensure_dirs, load_config, log  # noqa: E402

SEED = 42
MIN_POOL = 3
MIN_METAREG = 10
ELIGIBLE_METRICS = {"mean_difference_years", "mean_difference_pace"}


def dl_pool(values: np.ndarray, ses: np.ndarray) -> dict:
    yi = np.asarray(values, dtype=float)
    vi = np.asarray(ses, dtype=float) ** 2
    k = len(yi)
    wi = 1.0 / vi
    mu_fe = float(np.sum(wi * yi) / np.sum(wi))
    Q = float(np.sum(wi * (yi - mu_fe) ** 2))
    df = k - 1
    C = float(np.sum(wi) - np.sum(wi ** 2) / np.sum(wi))
    tau2 = max(0.0, (Q - df) / C) if C > 0 else 0.0
    wi_star = 1.0 / (vi + tau2)
    mu_re = float(np.sum(wi_star * yi) / np.sum(wi_star))
    se_mu = math.sqrt(1.0 / float(np.sum(wi_star)))
    I2 = max(0.0, (Q - df) / Q) * 100 if Q > 0 else 0.0
    return {"mu": mu_re, "se": se_mu, "ci_lo": mu_re - 1.96 * se_mu,
            "ci_hi": mu_re + 1.96 * se_mu, "tau2": tau2, "I2": I2, "Q": Q, "k": k}


def get_first(extracted: pd.DataFrame, study_id: str, key: str) -> str:
    rows = extracted[extracted["study_id"] == study_id]
    if rows.empty:
        return "unknown"
    v = rows.iloc[0].get(key)
    if pd.isna(v) or v in ("", None):
        return "unknown"
    return str(v)


def duration_band(extracted: pd.DataFrame, study_id: str) -> str:
    rows = extracted[extracted["study_id"] == study_id]
    if rows.empty:
        return "unknown"
    try:
        w = float(rows.iloc[0].get("duration_weeks", float("nan")))
        if math.isnan(w):
            return "unknown"
        return "lt_6mo" if w < 26 else "ge_6mo"
    except Exception:
        return "unknown"


def age_band(extracted: pd.DataFrame, study_id: str) -> str:
    rows = extracted[extracted["study_id"] == study_id]
    if rows.empty:
        return "unknown"
    try:
        a = float(rows.iloc[0].get("age_mean", float("nan")))
        if math.isnan(a):
            return "unknown"
        return "lt_60" if a < 60 else "ge_60"
    except Exception:
        return "unknown"


def subgroup_q_test(pooled_results: list[dict]) -> tuple[float, float, int]:
    if len(pooled_results) < 2:
        return float("nan"), float("nan"), 0
    mus = np.array([r["mu"] for r in pooled_results])
    ses = np.array([r["se"] for r in pooled_results])
    wi = 1.0 / ses ** 2
    mu_overall = float(np.sum(wi * mus) / np.sum(wi))
    Q_b = float(np.sum(wi * (mus - mu_overall) ** 2))
    df = len(pooled_results) - 1
    p = float(1 - stats.chi2.cdf(Q_b, df)) if df > 0 else float("nan")
    return Q_b, p, df


def run(cfg: dict) -> None:
    np.random.seed(SEED)
    freeze = cfg["project"]["freeze_date"]
    proc = Path(cfg["paths"]["data_processed"])
    tabs = Path(cfg["paths"]["results_tabs"])
    docs = Path(cfg["paths"]["docs"])
    ensure_dirs(tabs, docs)

    sle_path = proc / f"study_level_effects_{freeze}.csv"
    if not sle_path.exists():
        log("subgroup_skipped", reason="study_level_effects file missing")
        return
    df = pd.read_csv(sle_path)
    df = df[df["effect_metric"].isin(ELIGIBLE_METRICS)].dropna(subset=["value", "se"])
    df = df[df["se"] > 0].copy()

    extracted_path = proc / f"extracted_clock_studies_{freeze}.csv"
    extracted = pd.read_csv(extracted_path) if extracted_path.exists() else pd.DataFrame()

    rows: list[dict] = []

    for clock in sorted(df["clock"].unique()):
        sub = df[df["clock"] == clock].copy()
        k_total = len(sub)
        if k_total < MIN_POOL:
            rows.append({
                "clock": clock, "moderator": "(any)", "stratum": "(any)", "k": k_total,
                "mu": float("nan"), "se": float("nan"),
                "ci_lower": float("nan"), "ci_upper": float("nan"),
                "tau2": float("nan"), "I2": float("nan"),
                "status": "gate_failed",
                "reason": f"clock k={k_total} < {MIN_POOL}; subgroup pooling not run",
            })
            continue

        sub["intervention_class"] = sub["study_id"].apply(lambda s: get_first(extracted, s, "intervention_class"))
        sub["duration_band"] = sub["study_id"].apply(lambda s: duration_band(extracted, s))
        sub["age_band"] = sub["study_id"].apply(lambda s: age_band(extracted, s))
        sub["health_status"] = sub["study_id"].apply(lambda s: get_first(extracted, s, "health_status"))

        for mod in ["intervention_class", "duration_band", "age_band", "health_status"]:
            pooled_strata = []
            for stratum, grp in sub.groupby(mod, dropna=False):
                k = len(grp)
                if k >= 2:
                    res = dl_pool(grp["value"].to_numpy(), grp["se"].to_numpy())
                    status = "pooled" if k >= MIN_POOL else "pooled_low_power"
                    rows.append({
                        "clock": clock, "moderator": mod, "stratum": str(stratum), "k": k,
                        "mu": res["mu"], "se": res["se"],
                        "ci_lower": res["ci_lo"], "ci_upper": res["ci_hi"],
                        "tau2": res["tau2"], "I2": res["I2"],
                        "status": status,
                        "reason": "relaxed pooling for narrative subgroup test" if k < MIN_POOL else "",
                    })
                    pooled_strata.append({"mu": res["mu"], "se": res["se"]})
                else:
                    rows.append({
                        "clock": clock, "moderator": mod, "stratum": str(stratum), "k": k,
                        "mu": float("nan"), "se": float("nan"),
                        "ci_lower": float("nan"), "ci_upper": float("nan"),
                        "tau2": float("nan"), "I2": float("nan"),
                        "status": "gate_failed",
                        "reason": f"k={k} < 2; cannot pool",
                    })
            Q_b, p_b, df_b = subgroup_q_test(pooled_strata)
            rows.append({
                "clock": clock, "moderator": mod, "stratum": "(between-subgroup-test)",
                "k": len(pooled_strata),
                "mu": float("nan"), "se": float("nan"),
                "ci_lower": float("nan"), "ci_upper": float("nan"),
                "tau2": float("nan"), "I2": float("nan"),
                "status": "subgroup_diff_test" if not math.isnan(Q_b) else "gate_failed",
                "reason": (f"Q_between={Q_b:.3f}, df={df_b}, p={p_b:.3f}; LOW POWER (k_total={k_total})"
                           if not math.isnan(Q_b) else "fewer than 2 strata with k>=2"),
            })

        # Meta-regression gate
        if k_total < MIN_METAREG:
            rows.append({
                "clock": clock, "moderator": "(meta_regression)", "stratum": "(continuous covariates)",
                "k": k_total, "mu": float("nan"), "se": float("nan"),
                "ci_lower": float("nan"), "ci_upper": float("nan"),
                "tau2": float("nan"), "I2": float("nan"),
                "status": "meta_reg_gate_failed",
                "reason": f"k={k_total} < {MIN_METAREG}; meta-regression not run",
            })

    out = pd.DataFrame(rows)
    out_path = tabs / f"subgroup_metareg_{freeze}.csv"
    out.to_csv(out_path, index=False)
    log("subgroup_done", n_rows=len(out), output=str(out_path))

    report = docs / f"subgroup_metareg_gate_report_path_c_{freeze}.md"
    lines = [
        "# Subgroup & Meta-Regression Gate Report — Path-C\n",
        f"Generated: {freeze}\n",
        "## Gates\n",
        f"- Subgroup pool: k>=`{MIN_POOL}` per stratum (primary); k>=`2` reported as `pooled_low_power` for the narrative subgroup-difference Q test only.",
        f"- Meta-regression: k>=`{MIN_METAREG}` per clock.\n",
        "## Per-clock summary\n",
    ]
    for clock in sorted(df["clock"].unique()):
        cr = [r for r in rows if r["clock"] == clock]
        pooled = [r for r in cr if r["status"] in ("pooled", "pooled_low_power")]
        failed = [r for r in cr if r["status"] == "gate_failed"]
        diff = [r for r in cr if r["status"] == "subgroup_diff_test"]
        mreg = [r for r in cr if r["status"] == "meta_reg_gate_failed"]
        lines.append(f"### {clock}")
        lines.append(f"- Strata pooled (incl. low-power): {len(pooled)}")
        lines.append(f"- Strata gate-failed: {len(failed)}")
        for d in diff:
            lines.append(f"- {d['moderator']}: {d['reason']}")
        for m in mreg:
            lines.append(f"- meta-regression: {m['reason']}")
        lines.append("")
    lines += [
        "## Honest interpretation\n",
        "- With DunedinPACE k=3, subgroup differences cannot be reliably detected.",
        "- Subgroup Q-tests reported are explicitly flagged LOW POWER.",
        "- Meta-regression is gate-failed for every clock at this evidence base.",
    ]
    report.write_text("\n".join(lines), encoding="utf-8")
    log("subgroup_report_written", path=str(report))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="anti_ageing_review/meta_dnam_clocks/config/meta_config.yaml")
    args = ap.parse_args()
    cfg = load_config(args.config)
    run(cfg)


if __name__ == "__main__":
    main()
