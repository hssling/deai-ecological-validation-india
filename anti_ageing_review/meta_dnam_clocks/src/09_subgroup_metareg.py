"""Phase 7: subgroup/meta-regression feasibility gate."""
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
    min_meta = int(cfg["synthesis"]["min_studies_for_metareg"])
    calc = effects[effects["effect_status"].eq("calculated_candidate")]
    rows = []
    for moderator in ["intervention_class", "duration_weeks", "age_mean", "health_status"]:
        rows.append({
            "analysis": moderator,
            "calculable_effects": len(calc),
            "min_required": min_meta,
            "status": "not_run" if len(calc) < min_meta else "eligible_pending_model",
            "reason": "too few real extracted effects" if len(calc) < min_meta else "sufficient count",
        })
    out = pd.DataFrame(rows)
    out.to_csv(tabs / f"subgroup_metareg_gate_status_{freeze}.csv", index=False)
    (docs / f"subgroup_metareg_gate_report_{freeze}.md").write_text(
        "# Subgroup and Meta-Regression Gate Report\n\n"
        + out.to_markdown(index=False)
        + "\n\nNo subgroup or meta-regression model was run because real extracted effect sizes are too sparse.\n",
        encoding="utf-8",
    )
    log("subgroup_metareg_gate_done", calculable_effects=len(calc))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True)
    run(load_config(ap.parse_args().config))
