"""Phase 12 (Path-C): GRADE evidence profile for any clock with k>=3.

Domains: RoB, inconsistency, indirectness, imprecision, publication bias.
Starting certainty: HIGH (intervention studies, mostly RCTs).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from _common import ensure_dirs, load_config, log  # noqa: E402

LEVELS = ["High", "Moderate", "Low", "Very Low"]
MIN_POOL = 3


def downgrade(start: str, steps: int) -> str:
    idx = LEVELS.index(start)
    new_idx = min(len(LEVELS) - 1, idx + max(0, steps))
    return LEVELS[new_idx]


def run(cfg: dict) -> None:
    freeze = cfg["project"]["freeze_date"]
    tabs = Path(cfg["paths"]["results_tabs"])
    proc = Path(cfg["paths"]["data_processed"])
    docs = Path(cfg["paths"]["docs"])
    ensure_dirs(tabs, docs)

    pooled = pd.read_csv(tabs / f"per_clock_pooled_{freeze}.csv")
    rob_path = proc / f"rob2_assessments_{freeze}.csv"
    rob = pd.read_csv(rob_path) if rob_path.exists() else pd.DataFrame()

    rows: list[dict] = []
    for _, p in pooled.iterrows():
        clock = p["clock"]
        k = int(p["k"])
        if k < MIN_POOL:
            rows.append({
                "clock": clock, "k": k,
                "start": "—", "rob": "—", "inconsistency": "—",
                "indirectness": "—", "imprecision": "—", "pubbias": "—",
                "downgrades": "—", "certainty": "—",
                "status": "gate_failed",
                "reason": f"k={k}<{MIN_POOL}; no GRADE row",
            })
            continue
        I2 = float(p["I2"])
        ci_lo = float(p["ci_lower_dl"])
        ci_hi = float(p["ci_upper_dl"])

        # RoB
        rob_dec = "Down 1 (RoB dual coding pending; treated as some concerns)"
        rob_steps = 1
        if not rob.empty:
            statuses = rob["consensus_status"].fillna("pending").tolist()
            if statuses and not all(s == "pending" for s in statuses):
                if all(s == "low" for s in statuses):
                    rob_dec, rob_steps = "No downgrade (all studies low RoB)", 0
                else:
                    rob_dec, rob_steps = "Down 1 (some/high RoB present)", 1

        # Inconsistency
        if I2 >= 75:
            incons_dec, incons_steps = f"Down 1 (I²={I2:.0f}% — high)", 1
        elif I2 >= 50:
            incons_dec, incons_steps = f"Down 1 (I²={I2:.0f}% — substantial)", 1
        else:
            incons_dec, incons_steps = f"No downgrade (I²={I2:.0f}%)", 0

        # Indirectness
        indir_dec = "Down 1 (heterogeneous interventions / adjustment sets pooled)"
        indir_steps = 1

        # Imprecision
        crosses_null = ci_lo < 0 < ci_hi
        if crosses_null and k < 10:
            imprec_dec, imprec_steps = f"Down 1 (95% CI crosses null with k={k})", 1
        elif k < 10:
            imprec_dec, imprec_steps = f"Down 1 (k={k}<10; serious imprecision)", 1
        else:
            imprec_dec, imprec_steps = "No downgrade", 0

        # Publication bias
        pubbias_dec = "Not downgraded (k<10; cannot be assessed)"
        pubbias_steps = 0

        total = rob_steps + incons_steps + indir_steps + imprec_steps + pubbias_steps
        certainty = downgrade("High", total)
        rows.append({
            "clock": clock, "k": k, "start": "High",
            "rob": rob_dec, "inconsistency": incons_dec,
            "indirectness": indir_dec, "imprecision": imprec_dec, "pubbias": pubbias_dec,
            "downgrades": total, "certainty": certainty,
            "status": "performed", "reason": "",
        })

    out = pd.DataFrame(rows)
    out_path = tabs / f"grade_profile_path_c_{freeze}.csv"
    out.to_csv(out_path, index=False)
    log("grade_profile_written", output=str(out_path))

    report = docs / f"grade_profile_path_c_{freeze}.md"
    lines = [
        "# GRADE Evidence Profile — Path-C\n",
        f"Generated: {freeze}\n",
        "## Per-clock\n",
        "| Clock | k | Start | RoB | Inconsistency | Indirectness | Imprecision | Pub bias | Downgrades | Certainty |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        if r["status"] == "gate_failed":
            lines.append(f"| {r['clock']} | {r['k']} | — | — | — | — | — | — | — | gate_failed |")
        else:
            lines.append(
                f"| {r['clock']} | {r['k']} | {r['start']} | {r['rob']} | {r['inconsistency']} | "
                f"{r['indirectness']} | {r['imprecision']} | {r['pubbias']} | {r['downgrades']} | **{r['certainty']}** |"
            )
    lines += [
        "\n## Honest interpretation\n",
        "- Per-domain decisions are derived directly from the pooled CSV and the RoB2 worksheet.",
        "- RoB downgrade is conservative because dual coding is pending.",
        "- Publication bias is explicitly *not* downgraded (rather than assumed absent) because k<10 prevents assessment.",
    ]
    report.write_text("\n".join(lines), encoding="utf-8")
    log("grade_report_written", path=str(report))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="anti_ageing_review/meta_dnam_clocks/config/meta_config.yaml")
    args = ap.parse_args()
    cfg = load_config(args.config)
    run(cfg)


if __name__ == "__main__":
    main()
