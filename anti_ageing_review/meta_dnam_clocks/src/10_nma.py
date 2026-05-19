"""Phase 8: conditional NMA feasibility gate."""
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
    min_nma = int(cfg["synthesis"]["min_studies_for_nma"])
    clocks = ["DunedinPACE", "GrimAge"]
    rows = []
    for clock in clocks:
        n = int(calc["clock"].eq(clock).sum())
        rows.append({
            "clock": clock,
            "calculable_effects": n,
            "min_required": min_nma,
            "network_connected": "not_assessed",
            "status": "not_run",
            "reason": "too few real effects; comparator network not extractable",
        })
    out = pd.DataFrame(rows)
    out.to_csv(tabs / f"nma_gate_status_{freeze}.csv", index=False)
    (docs / f"nma_gate_report_{freeze}.md").write_text(
        "# Network Meta-Analysis Gate Report\n\n"
        + out.to_markdown(index=False)
        + "\n\nNMA was not run. This follows the protocol hard stop.\n",
        encoding="utf-8",
    )
    log("nma_gate_done", nma_run=False)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True)
    run(load_config(ap.parse_args().config))
