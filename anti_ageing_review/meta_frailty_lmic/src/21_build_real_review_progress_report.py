from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "tables"
DOCS = ROOT / "docs"


def load(name: str) -> pd.DataFrame:
    return pd.read_csv(TABLES / name).fillna("")


def md_table(df: pd.DataFrame) -> str:
    return df.to_markdown(index=False)


def main() -> None:
    search_log = load("expanded_accessible_search_log.csv")
    screen_counts = load("expanded_accessible_screening_counts.csv")
    elig_counts = load("pmc_fulltext_eligibility_first_reviewer_counts.csv")
    primary = load("pmc_accessible_primary_include_first_reviewer.csv")
    numeric_counts = load("primary_accessible_numeric_table_mining_counts.csv")
    numeric_by_study = load("primary_accessible_numeric_table_mining_by_study.csv")

    node_counts = primary["intervention_node_prelim"].replace("", "unclear").value_counts().rename_axis("node").reset_index(name="primary_accessible_studies")
    node_counts.to_csv(TABLES / "primary_accessible_node_counts_first_reviewer.csv", index=False)

    outcome_studies = []
    numeric = load("primary_accessible_numeric_table_mining.csv")
    for outcome in sorted([x for x in numeric["outcome"].unique() if x]):
        subset = numeric[numeric["outcome"].eq(outcome) & numeric["effect_extract_status"].eq("candidate_table_found")]
        outcome_studies.append({"outcome": outcome, "studies_with_candidate_tables": subset["pmcid"].nunique(), "candidate_table_rows": len(subset)})
    outcome_df = pd.DataFrame(outcome_studies)
    outcome_df.to_csv(TABLES / "primary_accessible_outcome_table_availability.csv", index=False)

    nma_gates = pd.DataFrame(
        [
            ["Primary-accessible first-reviewer includes >=20", "pass" if len(primary) >= 20 else "not_met", len(primary)],
            ["At least 3 preliminary intervention nodes with >=2 studies", "pass" if (node_counts["primary_accessible_studies"] >= 2).sum() >= 3 else "not_met", int((node_counts["primary_accessible_studies"] >= 2).sum())],
            ["Arm-level effect sizes extracted", "not_met", 0],
            ["Comparator network connectivity assessed", "not_assessed", ""],
            ["Transitivity assessed", "not_assessed", ""],
            ["Second reviewer agreement completed", "not_met", 0],
        ],
        columns=["gate", "status", "value"],
    )
    nma_gates.to_csv(TABLES / "real_review_nma_gate_status.csv", index=False)

    report = f"""# Real Systematic Review Progress Report

Generated: 2026-05-18

## What Changed

The project has moved from submission-asset scaffolding into real systematic-review execution. The expanded search, deduplication, first-reviewer full-text eligibility and numeric table mining have now been run. Final submission assets should not be rebuilt until second-reviewer eligibility, numeric extraction, RoB 2 and synthesis are complete.

## Expanded Accessible Search

{md_table(search_log)}

## Expanded Screening Counts

{md_table(screen_counts)}

## Accessible PMC Full-Text Eligibility: First Reviewer

{md_table(elig_counts)}

Primary-accessible first-reviewer includes: {len(primary)}

## Preliminary Nodes Among Primary-Accessible Includes

{md_table(node_counts)}

## Numeric Table Mining

Numeric table mining identified candidate outcome tables in {int((numeric_by_study['candidate_table_rows'] > 0).sum())} of {len(numeric_by_study)} primary-accessible studies. These are source-table candidates, not completed effect sizes.

{md_table(outcome_df)}

## NMA Gate Status

{md_table(nma_gates)}

## Current Scientific Decision

The review is now genuinely underway, but it is still not ready for final assets or submission. The accessible evidence base contains enough first-reviewer primary candidates to justify continuing pairwise synthesis planning. NMA remains unavailable until arm-level effect sizes, comparator nodes and transitivity variables are extracted and checked.

## Required Next Steps

1. Complete second-reviewer full-text eligibility for all 237 mined PMC full texts, starting with the 39 primary-accessible includes and 40 deferred records.
2. Retrieve and screen the 84 publisher/library full texts from the original high-confidence queue and any important expanded candidates without PMC access.
3. Extract arm-level numeric data from `results/tables/primary_accessible_numeric_table_mining.csv`.
4. Complete RoB 2 for included randomized trials.
5. Build pairwise meta-analysis datasets for frailty status/score, gait speed, SPPB and grip strength only after numeric extraction is complete.
6. Run NMA only if the final comparator graph is connected and transitivity is defensible.
7. Rebuild submission assets only after these evidence steps are complete.
"""
    (DOCS / "real_systematic_review_progress_2026-05-18.md").write_text(report, encoding="utf-8")
    print(f"primary_accessible={len(primary)}")
    print(f"candidate_table_studies={(numeric_by_study['candidate_table_rows'] > 0).sum()}/{len(numeric_by_study)}")
    print(DOCS / "real_systematic_review_progress_2026-05-18.md")


if __name__ == "__main__":
    main()
