from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
TABLES = ROOT / "results" / "tables"
DOCS = ROOT / "docs"


EXTRACTION_COLUMNS = [
    "study_id",
    "pmid",
    "doi",
    "title",
    "year",
    "journal",
    "country",
    "income_setting",
    "setting",
    "design",
    "cluster_rct",
    "sample_size_total",
    "n_intervention",
    "n_control",
    "mean_age",
    "female_percent",
    "frailty_definition",
    "baseline_frailty_status",
    "intervention_label",
    "components",
    "delivery_format",
    "personnel",
    "duration_weeks",
    "frequency_per_week",
    "session_minutes",
    "comparator",
    "primary_outcome",
    "frailty_events_intervention",
    "frailty_total_intervention",
    "frailty_events_control",
    "frailty_total_control",
    "gait_speed_mean_i",
    "gait_speed_sd_i",
    "gait_speed_mean_c",
    "gait_speed_sd_c",
    "sppb_mean_i",
    "sppb_sd_i",
    "sppb_mean_c",
    "sppb_sd_c",
    "grip_mean_i",
    "grip_sd_i",
    "grip_mean_c",
    "grip_sd_c",
    "adherence_percent",
    "dropout_i",
    "dropout_c",
    "adverse_events",
    "rob2_randomization",
    "rob2_deviations",
    "rob2_missing",
    "rob2_measurement",
    "rob2_reporting",
    "rob2_overall",
    "implementation_readiness_score",
    "notes",
]


def main() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(PROCESSED / "screened_prioritized.csv").fillna("")
    counts = pd.read_csv(TABLES / "fulltext_priority_counts.csv")
    a = df[df["fulltext_priority"].eq("A_primary_fulltext")].copy()
    b = df[df["fulltext_priority"].eq("B_secondary_fulltext")].copy()
    c = df[df["fulltext_priority"].eq("C_sarcopenia_secondary")].copy()

    queue_cols = ["pmid", "doi", "title", "year", "journal", "url", "priority_reason"]
    a.sort_values(["year", "title"], ascending=[False, True])[queue_cols].to_csv(
        TABLES / "fulltext_queue_primary_A.csv", index=False, quoting=csv.QUOTE_MINIMAL
    )
    pd.DataFrame(columns=EXTRACTION_COLUMNS).to_csv(TABLES / "extraction_template.csv", index=False)

    report = f"""# Scoping Report

Generated from PubMed scoping search on 2026-05-18.

## Search Yield

- PubMed reported hits: 3425
- Records downloaded: 3418
- Deduplicated records: {len(df)}

## Title/Abstract Screening Counts

{pd.read_csv(TABLES / "title_abs_screening_counts.csv").to_markdown(index=False)}

## Full-Text Priority Counts

{counts.to_markdown(index=False)}

## Interpretation

The field is large and cannot be screened as a generic exercise/nutrition review without substantial duplication of recent NMAs. The primary full-text queue contains {len(a)} records that appear to be community, primary-care, home-based or implementation-relevant frailty RCT candidates. A further {len(b)} frailty RCT candidates are retained as secondary because setting or delivery is less directly relevant to Indian primary care. Sarcopenia-only trials are retained as a secondary stratum ({len(c)} community sarcopenia candidates) and should not drive the main frailty conclusion unless frailty outcomes are reported.

## Immediate Next Step

Full-text screening should begin with `results/tables/fulltext_queue_primary_A.csv`. Each exclusion must be logged against PRISMA-compatible reasons:

- not randomized or not cluster randomized
- not prefrail/frail or no frailty/function vulnerability at baseline
- not community/home/outpatient/primary-care relevant
- no eligible intervention
- no extractable frailty/function outcome
- duplicate cohort/publication
- abstract/protocol only

## NMA Feasibility Status

NMA is not yet approved. It becomes eligible only after full-text extraction demonstrates a connected network with coherent intervention nodes and at least one primary outcome.
"""
    (DOCS / "scoping_report_2026-05-18.md").write_text(report, encoding="utf-8")
    print(f"primary_queue={len(a)}")
    print(f"secondary_frailty={len(b)}")
    print(f"community_sarcopenia_secondary={len(c)}")


if __name__ == "__main__":
    main()
