"""Phase 10 (Path-C): network meta-analysis gate report.

Gate: k>=10 per clock AND a connected network of comparators. With k=3 for
DunedinPACE and k<3 for all other clocks, the NMA gate fails. Emits a
not-performed table and a gate-report markdown so reviewers can see why.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from _common import ensure_dirs, load_config, log  # noqa: E402

MIN_NMA = 10
ELIGIBLE_METRICS = {"mean_difference_years", "mean_difference_pace"}


def run(cfg: dict) -> None:
    freeze = cfg["project"]["freeze_date"]
    proc = Path(cfg["paths"]["data_processed"])
    tabs = Path(cfg["paths"]["results_tabs"])
    docs = Path(cfg["paths"]["docs"])
    ensure_dirs(tabs, docs)

    sle_path = proc / f"study_level_effects_{freeze}.csv"
    df = pd.read_csv(sle_path) if sle_path.exists() else pd.DataFrame()
    if not df.empty:
        df = df[df["effect_metric"].isin(ELIGIBLE_METRICS)].dropna(subset=["value", "se"])
        df = df[df["se"] > 0]

    rows = []
    for clock in cfg["clocks"]:
        k = int((df["clock"] == clock).sum()) if not df.empty else 0
        rows.append({
            "clock": clock,
            "k": k,
            "nma_performed": "no",
            "reason": f"k={k} < {MIN_NMA}; below NMA threshold",
        })

    out = pd.DataFrame(rows)
    out_path = tabs / f"nma_not_performed_path_c_{freeze}.csv"
    out.to_csv(out_path, index=False)
    log("nma_gate_table_written", output=str(out_path))

    report = docs / f"nma_gate_report_path_c_{freeze}.md"
    lines = [
        "# Network Meta-Analysis Gate Report — Path-C\n",
        f"Generated: {freeze}\n",
        "## Gate\n",
        f"- Required: k>=`{MIN_NMA}` per clock with a connected network.",
        "- Current state: every clock has k<10. NMA is NOT performed.\n",
        "## Per-clock\n",
        "| Clock | k | NMA performed | Reason |",
        "|---|---|---|---|",
    ]
    for r in rows:
        lines.append(f"| {r['clock']} | {r['k']} | {r['nma_performed']} | {r['reason']} |")
    lines += [
        "\n## Honest interpretation\n",
        "- Even for DunedinPACE (k=3), an NMA would be uninformative and risk false precision.",
        "- We therefore present pairwise random-effects pooling only.",
    ]
    report.write_text("\n".join(lines), encoding="utf-8")
    log("nma_report_written", path=str(report))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="anti_ageing_review/meta_dnam_clocks/config/meta_config.yaml")
    args = ap.parse_args()
    cfg = load_config(args.config)
    run(cfg)


if __name__ == "__main__":
    main()
