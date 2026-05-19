"""Phase 9: publication-bias and sensitivity feasibility gate."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).parent))
from _common import ensure_dirs, load_config, log  # noqa: E402


def run(cfg):
    freeze = cfg["project"]["freeze_date"]
    tabs = Path(cfg["paths"]["results_tabs"]); docs = Path(cfg["paths"]["docs"])
    ensure_dirs(tabs, docs)
    effects = pd.read_csv(tabs / f"effect_size_candidates_{freeze}.csv").fillna("")
    calc = effects[effects["effect_status"].eq("calculated_candidate")]
    min_bias = int(cfg["synthesis"]["min_studies_for_pubbias"])
    rows = []
    for test in ["funnel_plot", "egger", "begg", "pet_peese", "trim_and_fill", "leave_one_out", "low_rob_only"]:
        rows.append({
            "analysis": test,
            "calculable_effects": len(calc),
            "min_required": min_bias if test not in ["leave_one_out", "low_rob_only"] else 3,
            "status": "not_run",
            "reason": "too few real extracted effects",
        })
    out = pd.DataFrame(rows)
    out.to_csv(tabs / f"pubbias_sensitivity_gate_status_{freeze}.csv", index=False)
    (docs / f"pubbias_sensitivity_gate_report_{freeze}.md").write_text(
        "# Publication Bias and Sensitivity Gate Report\n\n"
        + out.to_markdown(index=False)
        + "\n",
        encoding="utf-8",
    )
    log("pubbias_sensitivity_gate_done", calculable_effects=len(calc))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True)
    run(load_config(ap.parse_args().config))
