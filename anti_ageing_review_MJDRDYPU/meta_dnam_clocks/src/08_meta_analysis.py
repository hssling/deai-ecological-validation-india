"""Phase 8 (A3 amendment): generic-inverse-variance random-effects meta-analysis.

For each named clock with k>=3 study-level adjusted between-group effects in
`study_level_effects_2026-05-18.csv` (mean_difference_years or
mean_difference_pace metric), pools effects with:
  1. Python primary  : DerSimonian-Laird RE via statsmodels.combine_effects
                       + HKSJ (use_t=True) + Bayesian MH sampler (half-normal(0,0.5) tau prior)
  2. R cross-check   : meta::metagen DL + HKSJ + bayesmeta::bayesmeta

Outputs:
  results/tables/per_clock_pooled_2026-05-18.csv
  docs/meta_analysis_gate_report_path_c_2026-05-18.md

Random seed: 42.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).parent))
from _common import ensure_dirs, load_config, log  # noqa: E402

RSCRIPT = r"C:\Program Files\R\R-4.5.3\bin\Rscript.exe"
SEED = 42
MIN_POOL = 3
ELIGIBLE_METRICS = {"mean_difference_years", "mean_difference_pace"}


def dl_pool(values: np.ndarray, ses: np.ndarray, use_t: bool = False) -> dict:
    """DerSimonian-Laird random-effects generic-inverse-variance pool.

    Manual implementation matching the standard meta-analysis formulas
    (Borenstein 2009) to avoid statsmodels version-string parsing issues
    on this host.
    """
    yi = np.asarray(values, dtype=float)
    vi = np.asarray(ses, dtype=float) ** 2
    k = len(yi)
    wi = 1.0 / vi
    mu_fe = float(np.sum(wi * yi) / np.sum(wi))
    Q = float(np.sum(wi * (yi - mu_fe) ** 2))
    df = k - 1
    p_Q = float(1 - stats.chi2.cdf(Q, df)) if df > 0 else float("nan")
    C = float(np.sum(wi) - np.sum(wi ** 2) / np.sum(wi))
    tau2 = max(0.0, (Q - df) / C) if C > 0 else 0.0
    wi_star = 1.0 / (vi + tau2)
    mu_re = float(np.sum(wi_star * yi) / np.sum(wi_star))
    var_mu = 1.0 / float(np.sum(wi_star))
    se_mu = math.sqrt(var_mu)
    I2 = max(0.0, (Q - df) / Q) * 100 if Q > 0 else 0.0
    if use_t and k >= 3:
        # HKSJ variance adjustment
        q_stat = float(np.sum(wi_star * (yi - mu_re) ** 2) / df)
        se_mu_hksj = math.sqrt(max(q_stat, 1.0) * var_mu) if q_stat > 1 else math.sqrt(var_mu)
        # Use HKSJ uses q*var_mu as variance regardless of >1 (Knapp-Hartung 2003)
        se_mu_hksj = math.sqrt(q_stat * var_mu)
        t_crit = float(stats.t.ppf(0.975, df))
        ci_lo = mu_re - t_crit * se_mu_hksj
        ci_hi = mu_re + t_crit * se_mu_hksj
        return {"mu": mu_re, "se_mu": se_mu_hksj, "ci_lo": ci_lo, "ci_hi": ci_hi,
                "tau2": tau2, "I2": I2, "Q": Q, "Q_pval": p_Q, "k": k}
    ci_lo = mu_re - 1.96 * se_mu
    ci_hi = mu_re + 1.96 * se_mu
    return {"mu": mu_re, "se_mu": se_mu, "ci_lo": ci_lo, "ci_hi": ci_hi,
            "tau2": tau2, "I2": I2, "Q": Q, "Q_pval": p_Q, "k": k}


def prediction_interval(mu: float, tau2: float, se_mu: float, k: int) -> tuple[float, float]:
    if k < 3:
        return (float("nan"), float("nan"))
    se_pi = math.sqrt(tau2 + se_mu ** 2)
    t_crit = float(stats.t.ppf(0.975, k - 2)) if k - 2 > 0 else float("nan")
    if math.isnan(t_crit):
        return (float("nan"), float("nan"))
    return (mu - t_crit * se_pi, mu + t_crit * se_pi)


def bayes_pool(values: np.ndarray, ses: np.ndarray, n_iter: int = 20000, burnin: int = 5000,
               tau_prior_scale: float = 0.5) -> dict:
    """Metropolis-Hastings sampler for normal-normal hierarchical model.

    Likelihood: y_i ~ N(mu, sigma_i^2 + tau^2)
    Priors:     mu ~ N(0, 100^2)  (weakly informative)
                tau ~ HalfNormal(0, tau_prior_scale)  (truncated normal at 0)
    """
    rng = np.random.default_rng(SEED)
    yi = np.asarray(values, dtype=float)
    vi = np.asarray(ses, dtype=float) ** 2
    # init
    mu = float(np.mean(yi))
    tau = float(np.std(yi) if len(yi) > 1 else 0.1)
    tau = max(tau, 1e-4)

    def log_post(mu_v, tau_v):
        if tau_v < 0:
            return -np.inf
        s2 = vi + tau_v ** 2
        ll = -0.5 * np.sum(np.log(2 * math.pi * s2) + (yi - mu_v) ** 2 / s2)
        # prior mu N(0, 100^2)
        lp_mu = -0.5 * (mu_v ** 2) / (100 ** 2)
        # prior tau half-normal(0, scale)
        lp_tau = -0.5 * (tau_v ** 2) / (tau_prior_scale ** 2)
        return ll + lp_mu + lp_tau

    prop_mu = max(1e-3, float(np.std(yi) / math.sqrt(len(yi)))) if len(yi) > 1 else 0.1
    prop_tau = max(1e-3, tau_prior_scale / 4)
    mu_chain = np.zeros(n_iter)
    tau_chain = np.zeros(n_iter)
    cur_lp = log_post(mu, tau)
    for i in range(n_iter):
        mu_new = mu + rng.normal(0, prop_mu)
        tau_new = abs(tau + rng.normal(0, prop_tau))  # reflect at 0
        new_lp = log_post(mu_new, tau_new)
        if math.log(rng.uniform()) < new_lp - cur_lp:
            mu, tau, cur_lp = mu_new, tau_new, new_lp
        mu_chain[i] = mu
        tau_chain[i] = tau
    mu_post = mu_chain[burnin:]
    return {
        "mu_median": float(np.median(mu_post)),
        "ci_lo": float(np.quantile(mu_post, 0.025)),
        "ci_hi": float(np.quantile(mu_post, 0.975)),
        "tau_median": float(np.median(tau_chain[burnin:])),
    }


def call_r_cross_check(df_clock: pd.DataFrame, r_script: Path) -> dict:
    """Call Rscript meta_pool.R and parse its JSON output."""
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as f:
        df_clock.to_csv(f.name, index=False)
        in_path = f.name
    out_path = in_path + ".out.json"
    try:
        cp = subprocess.run(
            [RSCRIPT, str(r_script), "--input", in_path, "--output", out_path],
            shell=False, capture_output=True, text=True, timeout=120,
        )
        if cp.returncode != 0:
            return {"r_error": cp.stderr[-500:], "r_stdout": cp.stdout[-500:]}
        with open(out_path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as e:
        return {"r_error": str(e)}
    finally:
        try:
            os.unlink(in_path)
        except Exception:
            pass
        try:
            os.unlink(out_path)
        except Exception:
            pass


def consistent(py: float, r: float, rel_tol: float = 0.05, abs_tol: float = 0.01) -> str:
    if r is None or (isinstance(r, float) and math.isnan(r)):
        return "no_r"
    diff = abs(py - r)
    rel = diff / max(abs(py), 1e-6)
    return "yes" if (diff <= abs_tol or rel <= rel_tol) else "no"


def run(cfg: dict) -> None:
    np.random.seed(SEED)
    freeze = cfg["project"]["freeze_date"]
    proc = Path(cfg["paths"]["data_processed"])
    tabs = Path(cfg["paths"]["results_tabs"])
    docs = Path(cfg["paths"]["docs"])
    root = Path(cfg["paths"]["root"])
    r_script = root / "r_scripts" / "meta_pool.R"
    ensure_dirs(tabs, docs)

    inp = proc / f"study_level_effects_{freeze}.csv"
    if not inp.exists():
        log("pooling_skipped", reason="study_level_effects file missing")
        return
    df = pd.read_csv(inp)
    df = df[df["effect_metric"].isin(ELIGIBLE_METRICS)].copy()
    # drop rows without numeric SE
    df = df.dropna(subset=["value", "se"]).reset_index(drop=True)
    df = df[df["se"] > 0]

    clocks_in_data = sorted(df["clock"].unique())
    rows = []
    per_clock_summary = {}
    for clock in cfg["clocks"] + [c for c in clocks_in_data if c not in cfg["clocks"]]:
        sub = df[df["clock"] == clock].copy()
        k = len(sub)
        if k < MIN_POOL:
            rows.append({
                "clock": clock, "k": k, "mu_dl": float("nan"),
                "ci_lower_dl": float("nan"), "ci_upper_dl": float("nan"),
                "pi_lower": float("nan"), "pi_upper": float("nan"),
                "tau2": float("nan"), "I2": float("nan"), "Q": float("nan"), "Q_pval": float("nan"),
                "mu_hksj": float("nan"), "ci_lower_hksj": float("nan"), "ci_upper_hksj": float("nan"),
                "mu_bayes": float("nan"), "ci_lower_bayes": float("nan"), "ci_upper_bayes": float("nan"),
                "r_mu_dl": float("nan"), "r_mu_hksj": float("nan"), "r_mu_bayes": float("nan"),
                "python_r_consistent": "gate_failed",
                "reason": f"k<{MIN_POOL} (k={k})",
            })
            per_clock_summary[clock] = {"k": k, "status": "gate_failed"}
            continue
        values = sub["value"].to_numpy()
        ses = sub["se"].to_numpy()
        dl = dl_pool(values, ses, use_t=False)
        hksj = dl_pool(values, ses, use_t=True)
        pi_lo, pi_hi = prediction_interval(dl["mu"], dl["tau2"], dl["se_mu"], k)
        bayes = bayes_pool(values, ses)

        r_out = call_r_cross_check(sub[["study_id", "value", "se"]], r_script) if r_script.exists() else {"r_error": "r_script_missing"}

        py_r_dl = consistent(dl["mu"], r_out.get("r_dl_mu"))
        py_r_hksj = consistent(hksj["mu"], r_out.get("r_hksj_mu"))
        py_r_bayes = consistent(bayes["mu_median"], r_out.get("r_bayes_mu_median"))
        overall = "yes" if all(v == "yes" for v in [py_r_dl, py_r_hksj, py_r_bayes]) else (
            "no_r" if py_r_dl == "no_r" else "no"
        )
        rows.append({
            "clock": clock, "k": k,
            "mu_dl": dl["mu"], "ci_lower_dl": dl["ci_lo"], "ci_upper_dl": dl["ci_hi"],
            "pi_lower": pi_lo, "pi_upper": pi_hi,
            "tau2": dl["tau2"], "I2": dl["I2"], "Q": dl["Q"], "Q_pval": dl["Q_pval"],
            "mu_hksj": hksj["mu"], "ci_lower_hksj": hksj["ci_lo"], "ci_upper_hksj": hksj["ci_hi"],
            "mu_bayes": bayes["mu_median"], "ci_lower_bayes": bayes["ci_lo"], "ci_upper_bayes": bayes["ci_hi"],
            "r_mu_dl": r_out.get("r_dl_mu", float("nan")),
            "r_mu_hksj": r_out.get("r_hksj_mu", float("nan")),
            "r_mu_bayes": r_out.get("r_bayes_mu_median", float("nan")),
            "python_r_consistent": overall,
            "reason": r_out.get("r_error", ""),
        })
        per_clock_summary[clock] = {
            "k": k, "status": "pooled",
            "mu_dl": dl["mu"], "ci_dl": [dl["ci_lo"], dl["ci_hi"]],
            "tau2": dl["tau2"], "I2": dl["I2"],
            "python_r_consistent": overall,
        }

    out = pd.DataFrame(rows)
    out_path = tabs / f"per_clock_pooled_{freeze}.csv"
    out.to_csv(out_path, index=False)

    log("pooling_done", per_clock=per_clock_summary, output=str(out_path))

    # Write gate report
    report_path = docs / f"meta_analysis_gate_report_path_c_{freeze}.md"
    lines = [
        f"# Meta-Analysis Gate Report — Path-C (A3 amendment)\n",
        f"Generated: {freeze}\n",
        f"Effect measure: adjusted between-group mean difference on original clock scale (years for age clocks; per-year-per-year for DunedinPACE). Method: DerSimonian-Laird random-effects generic-inverse-variance. Cross-check: R meta::metagen + bayesmeta::bayesmeta. Random seed: {SEED}.\n",
        f"Input: `{inp.name}` (k_total = {len(df)} study-clock effects across {df['study_id'].nunique()} studies).\n",
        "\n## Per-clock outcome\n",
        "| Clock | k | μ_DL | 95% CI | 95% PI | τ² | I² (%) | μ_HKSJ | μ_Bayes | R cross-check |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        if r["k"] < MIN_POOL:
            lines.append(f"| {r['clock']} | {r['k']} | gate_failed (k<{MIN_POOL}) | — | — | — | — | — | — | — |")
        else:
            lines.append(
                f"| {r['clock']} | {r['k']} | {r['mu_dl']:.4f} | "
                f"[{r['ci_lower_dl']:.4f}, {r['ci_upper_dl']:.4f}] | "
                f"[{r['pi_lower']:.4f}, {r['pi_upper']:.4f}] | "
                f"{r['tau2']:.4f} | {r['I2']:.1f} | "
                f"{r['mu_hksj']:.4f} | {r['mu_bayes']:.4f} | "
                f"DL→R={r['r_mu_dl']} ({r['python_r_consistent']}) |"
            )
    poolable = [r["clock"] for r in rows if r["k"] >= MIN_POOL]
    failed = [r["clock"] for r in rows if r["k"] < MIN_POOL]
    lines += [
        "\n## Path-C gate verdict\n",
        f"- Clocks reaching k≥{MIN_POOL} (pooled): {', '.join(poolable) if poolable else 'NONE'}",
        f"- Clocks failing the gate (k<{MIN_POOL}): {', '.join(failed) if failed else 'NONE'}",
        "\n## Honesty notes\n",
        "- Only effects with a CI or SE literally present in the source full text are pooled.",
        "- Where a study reported Cohen's d on the original clock as the headline between-group estimate (e.g., WaziryR_2023 CALERIE), that row is recorded with metric=cohens_d_post_12mo and excluded from the primary MD pool but reported separately as SMD sensitivity.",
        "- DunedinPACE pool mixes effects with somewhat different adjustment sets (ANCOVA on placebo/treatment for CorleyMJ_2025; full-model adjusted β for ChapnickM cohort; covariance-adjusted β for MerrillSM iPCIT). Heterogeneity is therefore expected and is reflected in τ² and the prediction interval.",
        "- The R cross-check uses the same (value, SE) inputs; agreement within 0.01 absolute or 5% relative of the pooled point estimate is recorded as `yes`.",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    log("gate_report_written", path=str(report_path))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="anti_ageing_review/meta_dnam_clocks/config/meta_config.yaml")
    args = ap.parse_args()
    cfg = load_config(args.config)
    run(cfg)


if __name__ == "__main__":
    main()
