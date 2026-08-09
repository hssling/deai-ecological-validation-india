from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "tables"
DOCS = ROOT / "docs"


def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path).fillna("")


def gate(value: bool) -> str:
    return "pass" if value else "not_met"


def main() -> None:
    queue = load_csv(TABLES / "high_confidence_extraction_queue.csv")
    workbook = load_csv(TABLES / "fulltext_verified_extraction_workbook.csv")
    node_counts = queue["intervention_node_prelim"].value_counts()
    mined_nodes = workbook[workbook["verification_status"].eq("pmc_fulltext_mined_not_numeric_extracted")][
        "intervention_node_prelim"
    ].value_counts()

    total_candidates = len(queue)
    mined_fulltexts = int(workbook["verification_status"].eq("pmc_fulltext_mined_not_numeric_extracted").sum())
    nodes_ge_2 = int((node_counts >= 2).sum())
    mined_nodes_ge_2 = int((mined_nodes >= 2).sum())

    rows = [
        {
            "domain": "study_volume",
            "criterion": "At least 20 high-confidence RCT candidates before numeric extraction",
            "result": gate(total_candidates >= 20),
            "value": total_candidates,
            "interpretation": "Large enough to proceed to full extraction and pairwise synthesis planning.",
        },
        {
            "domain": "fulltext_availability",
            "criterion": "Open-access PMC full text mined for at least 20 candidates",
            "result": gate(mined_fulltexts >= 20),
            "value": mined_fulltexts,
            "interpretation": "Sufficient for immediate author extraction subset; remaining records need publisher/library access.",
        },
        {
            "domain": "candidate_nodes",
            "criterion": "At least 3 preliminary intervention nodes have two or more studies",
            "result": gate(nodes_ge_2 >= 3),
            "value": nodes_ge_2,
            "interpretation": "Component coding appears feasible, but node definitions must be confirmed from full texts.",
        },
        {
            "domain": "mined_nodes",
            "criterion": "At least 3 preliminary intervention nodes have two or more mined full texts",
            "result": gate(mined_nodes_ge_2 >= 3),
            "value": mined_nodes_ge_2,
            "interpretation": "Open-access subset supports early piloting of extraction and component coding.",
        },
        {
            "domain": "network_connectivity",
            "criterion": "Comparator nodes form a connected analyzable network",
            "result": "not_assessed",
            "value": "",
            "interpretation": "Requires final comparator extraction; cannot be inferred from abstracts or snippets.",
        },
        {
            "domain": "transitivity",
            "criterion": "Baseline frailty, setting, dose and comparator distributions are clinically coherent",
            "result": "not_assessed",
            "value": "",
            "interpretation": "Requires final extraction and a transitivity table before NMA.",
        },
        {
            "domain": "ijmr_submission_gate",
            "criterion": "Protocol registration completed before final screening/synthesis is reported as submission-ready",
            "result": "pending",
            "value": "",
            "interpretation": "PROSPERO draft exists but registration number must be added before IJMR submission assets are finalized.",
        },
    ]

    pd.DataFrame(rows).to_csv(TABLES / "network_feasibility_prelim.csv", index=False)

    node_table = node_counts.rename_axis("preliminary_node").reset_index(name="candidate_records")
    mined_node_table = mined_nodes.rename_axis("preliminary_node").reset_index(name="pmc_mined_records")
    node_merge = node_table.merge(mined_node_table, on="preliminary_node", how="left").fillna(0)
    node_merge["pmc_mined_records"] = node_merge["pmc_mined_records"].astype(int)
    node_merge.to_csv(TABLES / "network_prelim_node_counts.csv", index=False)

    doc = f"""# Preliminary Network Feasibility Memo

Generated: 2026-05-18

## Current Evidence Base

- High-confidence extraction candidates: {total_candidates}
- PMC full texts fetched and mined: {mined_fulltexts}
- Records still requiring publisher/library full text access: {total_candidates - mined_fulltexts}
- Preliminary intervention nodes with at least two candidate records: {nodes_ge_2}
- Preliminary intervention nodes with at least two mined PMC full texts: {mined_nodes_ge_2}

## Interpretation

The project is feasible for a full systematic review and likely feasible for pairwise meta-analysis after author extraction. A network meta-analysis remains a conditional objective, not a completed decision. The decisive checks are comparator-node connectivity, outcome harmonisation, and transitivity across frailty definition, baseline severity, setting, intervention dose, and follow-up time.

## Preliminary Node Distribution

{node_merge.to_markdown(index=False)}

## NMA Gate

Proceed to NMA only if full-text extraction confirms:

1. At least one clinically coherent primary outcome has enough studies.
2. Comparator definitions create a connected network.
3. At least three intervention/comparator nodes have two or more studies.
4. Important effect modifiers can be tabulated and judged acceptably balanced.
5. Pairwise contrasts do not show irreconcilable clinical heterogeneity.

Until these checks pass, the planned manuscript should describe NMA as conditional and should default to pairwise random-effects meta-analysis plus structured implementation-readiness mapping.
"""
    (DOCS / "network_feasibility_prelim_2026-05-18.md").write_text(doc, encoding="utf-8")

    print(f"high_confidence_candidates={total_candidates}")
    print(f"pmc_mined_fulltexts={mined_fulltexts}")
    print(f"nodes_ge_2={nodes_ge_2}")
    print(f"mined_nodes_ge_2={mined_nodes_ge_2}")


if __name__ == "__main__":
    main()
