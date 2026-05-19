"""Phase 10: GRADE feasibility profile."""
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
    rows = []
    for clock, group in effects.groupby("clock", dropna=False):
        n = int(group["effect_status"].eq("calculated_candidate").sum())
        rows.append({
            "clock": clock,
            "calculable_effects": n,
            "grade_status": "not_assessable" if n < 3 else "pending",
            "certainty": "not_rated" if n < 3 else "pending_full_grade",
            "reason": "fewer than 3 real effect estimates" if n < 3 else "requires RoB and pooled estimate",
        })
    out = pd.DataFrame(rows)
    out.to_csv(tabs / f"grade_profile_{freeze}.csv", index=False)
    (docs / f"grade_profile_report_{freeze}.md").write_text(
        "# GRADE Profile Report\n\n"
        + out.to_markdown(index=False)
        + "\n\nGRADE certainty was not assigned because no clock has enough real extracted effect estimates.\n",
        encoding="utf-8",
    )
    log("grade_profile_done", assessable=int((out["grade_status"] == "pending").sum()))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True)
    run(load_config(ap.parse_args().config))
