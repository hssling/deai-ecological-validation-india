"""Phase 6: effect-size calculation and honest pooling gate.

Computes study-level candidate Hedges g only for rows with complete real numeric
data. Pools nothing unless the prespecified minimum study count is met.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from _common import ensure_dirs, load_config, log  # noqa: E402


def to_float(value):
    try:
        if value == "" or pd.isna(value):
            return None
        return float(value)
    except Exception:
        return None


def hedges_g_change(row: pd.Series) -> dict:
    ni = to_float(row.get("n_int"))
    nc = to_float(row.get("n_ctrl"))
    mi = to_float(row.get("change_int_mean"))
    mc = to_float(row.get("change_ctrl_mean"))
    sdi = to_float(row.get("change_int_sd"))
    sdc = to_float(row.get("change_ctrl_sd"))
    if not all(v is not None for v in [ni, nc, mi, mc, sdi, sdc]) or ni < 2 or nc < 2:
        return {"effect_status": "not_calculable", "reason": "missing complete change-score n/mean/sd"}
    df = ni + nc - 2
    if df <= 0:
        return {"effect_status": "not_calculable", "reason": "invalid degrees of freedom"}
    sp = math.sqrt(((ni - 1) * sdi**2 + (nc - 1) * sdc**2) / df)
    if sp <= 0:
        return {"effect_status": "not_calculable", "reason": "invalid pooled SD"}
    d = (mi - mc) / sp
    j = 1 - (3 / (4 * (ni + nc) - 9))
    g = j * d
    var_g = ((ni + nc) / (ni * nc)) + (g**2 / (2 * (ni + nc - 2)))
    se_g = math.sqrt(var_g)
    return {
        "effect_status": "calculated_candidate",
        "reason": "complete change-score data available; direction requires author confirmation",
        "effect_metric": "Hedges_g_change_intervention_minus_control",
        "hedges_g": g,
        "se": se_g,
        "variance": var_g,
        "ci95_low": g - 1.96 * se_g,
        "ci95_high": g + 1.96 * se_g,
        "n_total": int(ni + nc),
    }


def run(cfg: dict) -> None:
    freeze = cfg["project"]["freeze_date"]
    proc = Path(cfg["paths"]["data_processed"])
    tabs = Path(cfg["paths"]["results_tabs"])
    docs = Path(cfg["paths"]["docs"])
    ensure_dirs(tabs, docs)

    extracted = pd.read_csv(proc / f"extracted_clock_studies_{freeze}.csv").fillna("")
    rows = []
    for _, row in extracted.iterrows():
        result = hedges_g_change(row)
        base = {
            "study_id": row.get("study_id", ""),
            "first_author": row.get("first_author", ""),
            "year": row.get("year", ""),
            "clock": row.get("clock", ""),
            "intervention_class": row.get("intervention_class", ""),
            "comparator": row.get("comparator", ""),
            "extraction_status": row.get("extraction_status", ""),
            "notes": row.get("notes", ""),
        }
        base.update(result)
        rows.append(base)
    effects = pd.DataFrame(rows)
    effects.to_csv(tabs / f"effect_size_candidates_{freeze}.csv", index=False)

    min_pool = int(cfg["synthesis"]["min_studies_for_pool"])
    calc = effects[effects["effect_status"].eq("calculated_candidate")].copy()
    gate_rows = []
    for clock, group in effects.groupby("clock", dropna=False):
        n_calc = int(group["effect_status"].eq("calculated_candidate").sum())
        gate_rows.append(
            {
                "clock": clock,
                "calculable_effects": n_calc,
                "min_required_for_pool": min_pool,
                "pooling_status": "poolable" if n_calc >= min_pool else "not_poolable",
                "reason": "meets minimum count" if n_calc >= min_pool else "fewer than prespecified minimum real effects",
            }
        )
    gates = pd.DataFrame(gate_rows).sort_values(["pooling_status", "clock"])
    gates.to_csv(tabs / f"pooling_gate_status_{freeze}.csv", index=False)

    report = [
        "# Meta-Analysis Gate Report",
        "",
        f"Generated for freeze date: {freeze}",
        "",
        f"Rows in extraction sheet: {len(extracted)}",
        f"Calculated candidate effect sizes: {len(calc)}",
        f"Minimum studies required per clock for pooling: {min_pool}",
        "",
        "## Decision",
        "",
    ]
    if calc.empty:
        report.append("No effect sizes were calculable from verified extracted data. Meta-analysis is not permissible.")
    elif gates["pooling_status"].eq("poolable").any():
        report.append("At least one clock met the minimum count for pooling. Pooling script must be run for those clocks only.")
    else:
        report.append("No clock met the prespecified minimum count for pooling. Report candidate effects narratively and continue extraction.")
    report.extend(["", "## Pooling Gates", "", gates.to_markdown(index=False)])
    if not calc.empty:
        report.extend(["", "## Candidate Effects", "", calc.to_markdown(index=False)])
    (docs / f"meta_analysis_gate_report_{freeze}.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    log("meta_gate_done", candidate_effects=len(calc), poolable_clocks=int(gates["pooling_status"].eq("poolable").sum()))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    run(load_config(ap.parse_args().config))
