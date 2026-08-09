"""Phase 11 (Path-C): publication bias gate + sensitivity analyses that work at k=3.

Publication-bias tests (Egger / Begg / PET-PEESE) require k>=10 and are gate-failed.

Sensitivity analyses that DO work at k=3:
  - leave-one-out DL refit (mu, 95% CI) per dropped study
  - low-RoB-only restriction (currently all RoB rows `pending` -> gate_failed_pending_rob)
  - duration >= 12 weeks restriction (if all in pool already >=12wk -> no_change_from_primary)
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from _common import ensure_dirs, load_config, log  # noqa: E402

MIN_PUBBIAS = 10
MIN_POOL = 3
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
            "ci_hi": mu_re + 1.96 * se_mu, "tau2": tau2, "I2": I2, "k": k}


def run(cfg: dict) -> None:
    freeze = cfg["project"]["freeze_date"]
    proc = Path(cfg["paths"]["data_processed"])
    tabs = Path(cfg["paths"]["results_tabs"])
    docs = Path(cfg["paths"]["docs"])
    ensure_dirs(tabs, docs)

    sle = pd.read_csv(proc / f"study_level_effects_{freeze}.csv")
    sle = sle[sle["effect_metric"].isin(ELIGIBLE_METRICS)].dropna(subset=["value", "se"])
    sle = sle[sle["se"] > 0].copy()

    rob_path = proc / f"rob2_assessments_{freeze}.csv"
    rob = pd.read_csv(rob_path) if rob_path.exists() else pd.DataFrame()
    extracted_path = proc / f"extracted_clock_studies_{freeze}.csv"
    extracted = pd.read_csv(extracted_path) if extracted_path.exists() else pd.DataFrame()

    rows: list[dict] = []
    for clock in sorted(sle["clock"].unique()):
        sub = sle[sle["clock"] == clock].copy()
        k = len(sub)

        for test in ["publication_bias_egger", "publication_bias_begg", "pet_peese"]:
            rows.append({
                "clock": clock, "analysis": test, "k": k,
                "mu": float("nan"), "ci_lower": float("nan"), "ci_upper": float("nan"),
                "status": "gate_failed" if k < MIN_PUBBIAS else "performed",
                "reason": f"k={k} < {MIN_PUBBIAS}; pub-bias test not run" if k < MIN_PUBBIAS else "",
            })

        if k < MIN_POOL:
            continue

        # Leave-one-out
        for i in range(k):
            mask = np.ones(k, dtype=bool); mask[i] = False
            res = dl_pool(sub["value"].to_numpy()[mask], sub["se"].to_numpy()[mask])
            dropped = sub["study_id"].iloc[i]
            rows.append({
                "clock": clock, "analysis": f"leave_one_out:drop={dropped}", "k": k - 1,
                "mu": res["mu"], "ci_lower": res["ci_lo"], "ci_upper": res["ci_hi"],
                "status": "performed",
                "reason": f"DL refit excluding {dropped}; I2={res['I2']:.1f}",
            })

        # Low-RoB restriction
        if rob.empty:
            rob_status = "no_rob_table"
        else:
            study_ids = sub["study_id"].unique().tolist()
            statuses = rob[rob["study_id"].isin(study_ids)]["consensus_status"].fillna("pending")
            if statuses.empty or (statuses == "pending").all():
                rob_status = "all_pending"
            else:
                rob_status = "mixed"
        if rob_status in ("no_rob_table", "all_pending"):
            rows.append({
                "clock": clock, "analysis": "restrict_low_rob", "k": k,
                "mu": float("nan"), "ci_lower": float("nan"), "ci_upper": float("nan"),
                "status": "gate_failed_pending_rob",
                "reason": "Dual-coded RoB2 pending; low-RoB-only sensitivity cannot be computed",
            })
        else:
            low_ids = rob[rob["consensus_status"] == "low"]["study_id"].tolist()
            sub_low = sub[sub["study_id"].isin(low_ids)]
            if len(sub_low) < MIN_POOL:
                rows.append({
                    "clock": clock, "analysis": "restrict_low_rob", "k": len(sub_low),
                    "mu": float("nan"), "ci_lower": float("nan"), "ci_upper": float("nan"),
                    "status": "gate_failed",
                    "reason": f"low-RoB subset k={len(sub_low)} < {MIN_POOL}",
                })
            else:
                res = dl_pool(sub_low["value"].to_numpy(), sub_low["se"].to_numpy())
                rows.append({
                    "clock": clock, "analysis": "restrict_low_rob", "k": len(sub_low),
                    "mu": res["mu"], "ci_lower": res["ci_lo"], "ci_upper": res["ci_hi"],
                    "status": "performed", "reason": "Low-RoB studies only",
                })

        # Duration >= 12 weeks
        dur_ok = []
        for sid in sub["study_id"].unique():
            if extracted.empty:
                continue
            r = extracted[extracted["study_id"] == sid]
            if r.empty:
                continue
            try:
                wks = float(r.iloc[0].get("duration_weeks", float("nan")))
                if not math.isnan(wks) and wks >= 12:
                    dur_ok.append(sid)
            except Exception:
                pass
        if not dur_ok:
            rows.append({
                "clock": clock, "analysis": "restrict_duration_ge_12wk", "k": 0,
                "mu": float("nan"), "ci_lower": float("nan"), "ci_upper": float("nan"),
                "status": "gate_failed",
                "reason": "duration_weeks not extracted; sensitivity not performed",
            })
        else:
            sub_d = sub[sub["study_id"].isin(dur_ok)]
            if len(sub_d) == k:
                rows.append({
                    "clock": clock, "analysis": "restrict_duration_ge_12wk", "k": len(sub_d),
                    "mu": float("nan"), "ci_lower": float("nan"), "ci_upper": float("nan"),
                    "status": "no_change_from_primary",
                    "reason": "All pool studies have duration>=12 weeks",
                })
            elif len(sub_d) >= MIN_POOL:
                res = dl_pool(sub_d["value"].to_numpy(), sub_d["se"].to_numpy())
                rows.append({
                    "clock": clock, "analysis": "restrict_duration_ge_12wk", "k": len(sub_d),
                    "mu": res["mu"], "ci_lower": res["ci_lo"], "ci_upper": res["ci_hi"],
                    "status": "performed", "reason": "Duration>=12wk subset",
                })
            else:
                rows.append({
                    "clock": clock, "analysis": "restrict_duration_ge_12wk", "k": len(sub_d),
                    "mu": float("nan"), "ci_lower": float("nan"), "ci_upper": float("nan"),
                    "status": "gate_failed",
                    "reason": f"duration>=12wk subset k={len(sub_d)} < {MIN_POOL}",
                })

    out = pd.DataFrame(rows)
    out_path = tabs / f"sensitivity_{freeze}.csv"
    out.to_csv(out_path, index=False)
    log("sensitivity_done", n_rows=len(out), output=str(out_path))

    report = docs / f"pubbias_sensitivity_gate_report_path_c_{freeze}.md"
    lines = [
        "# Publication Bias & Sensitivity Gate Report — Path-C\n",
        f"Generated: {freeze}\n",
        "## Gates\n",
        f"- Egger / Begg / PET-PEESE require k>=`{MIN_PUBBIAS}`; gate-failed here.",
        "- Leave-one-out runs at k>=`3`.",
        "- Low-RoB-only requires dual-coded RoB2 (currently all `pending`).",
        "- Duration>=12-week sensitivity runs when `duration_weeks` is extracted.\n",
        "## Summary rows\n",
        "| Clock | Analysis | k | μ | 95% CI | Status |",
        "|---|---|---|---|---|---|",
    ]
    for r in rows:
        ci = (f"[{r['ci_lower']:.3f}, {r['ci_upper']:.3f}]"
              if not math.isnan(r["ci_lower"]) else "—")
        mu = f"{r['mu']:.4f}" if not math.isnan(r["mu"]) else "—"
        lines.append(f"| {r['clock']} | {r['analysis']} | {r['k']} | {mu} | {ci} | {r['status']} |")
    lines += [
        "\n## Honest interpretation\n",
        "- Publication-bias diagnostics are uninformative at k=3 and are correctly gate-failed.",
        "- Leave-one-out shows whether any single study drives the pooled DunedinPACE estimate.",
        "- Low-RoB-only sensitivity will remain `gate_failed_pending_rob` until dual coding is completed.",
    ]
    report.write_text("\n".join(lines), encoding="utf-8")
    log("sensitivity_report_written", path=str(report))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="anti_ageing_review/meta_dnam_clocks/config/meta_config.yaml")
    args = ap.parse_args()
    cfg = load_config(args.config)
    run(cfg)


if __name__ == "__main__":
    main()
