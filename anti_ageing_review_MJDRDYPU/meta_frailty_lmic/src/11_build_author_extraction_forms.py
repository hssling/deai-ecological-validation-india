from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "tables"
DOCS = ROOT / "docs"

AUTHOR_A = "Dr Siddalingaiah H S"
AUTHOR_B = "Dr Chandrakala D"


def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path).fillna("")


def assign_reviewer(index: int) -> str:
    return AUTHOR_A if index % 2 == 0 else AUTHOR_B


def assign_second_reviewer(first: str) -> str:
    return AUTHOR_B if first == AUTHOR_A else AUTHOR_A


def base_cols(df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "pmid",
        "pmcid",
        "doi",
        "title",
        "year",
        "journal",
        "url",
        "fulltext_access_status",
        "verification_status",
        "setting_code",
        "component_code",
        "intervention_node_prelim",
        "local_path",
    ]
    return df[[col for col in cols if col in df.columns]].copy()


def main() -> None:
    workbook = load_csv(TABLES / "fulltext_verified_extraction_workbook.csv")
    workbook = workbook.sort_values(["fulltext_access_status", "year", "pmid"], ascending=[True, False, False]).reset_index(
        drop=True
    )

    assignments = base_cols(workbook)
    assignments.insert(0, "study_id", [f"FRAIL-{i:03d}" for i in range(1, len(assignments) + 1)])
    assignments["primary_reviewer"] = [assign_reviewer(i) for i in range(len(assignments))]
    assignments["second_reviewer"] = assignments["primary_reviewer"].apply(assign_second_reviewer)
    assignments["arbitration_reviewer"] = "Joint consensus"
    assignments["screening_status"] = ""
    assignments["fulltext_final_decision"] = ""
    assignments["fulltext_exclusion_reason"] = ""
    assignments["consensus_status"] = ""
    assignments.to_csv(TABLES / "dual_author_fulltext_assignments.csv", index=False, quoting=csv.QUOTE_MINIMAL)

    extraction = assignments[
        [
            "study_id",
            "pmid",
            "pmcid",
            "title",
            "primary_reviewer",
            "second_reviewer",
            "fulltext_access_status",
        ]
    ].copy()
    extraction_fields = {
        "country": "",
        "setting_final": "",
        "design_final": "",
        "cluster_randomized": "",
        "sample_size_randomized_total": "",
        "sample_size_analyzed_total": "",
        "mean_age": "",
        "female_percent": "",
        "frailty_definition": "",
        "baseline_frailty_severity": "",
        "intervention_name": "",
        "intervention_components_final": "",
        "exercise_type": "",
        "nutrition_component": "",
        "digital_or_home_support": "",
        "personnel_required": "",
        "dose_frequency": "",
        "session_duration_minutes": "",
        "intervention_duration_weeks": "",
        "comparator_final": "",
        "follow_up_timepoint_primary": "",
        "primary_outcome_for_synthesis": "",
        "effect_measure_preferred": "",
        "notes_for_effect_size_conversion": "",
        "final_include_for_meta": "",
        "final_include_for_nma": "",
    }
    for col, default in extraction_fields.items():
        extraction[col] = default
    extraction.to_csv(TABLES / "study_characteristics_extraction_form.csv", index=False, quoting=csv.QUOTE_MINIMAL)

    outcomes = []
    outcome_names = [
        "frailty_status",
        "frailty_score",
        "gait_speed",
        "sppb",
        "grip_strength",
        "adl_iadl",
        "falls",
        "quality_of_life",
        "adherence",
        "dropout",
        "adverse_events",
    ]
    for _, row in assignments.iterrows():
        for outcome in outcome_names:
            outcomes.append(
                {
                    "study_id": row["study_id"],
                    "pmid": row["pmid"],
                    "outcome": outcome,
                    "timepoint": "",
                    "arm_1_name": "",
                    "arm_1_n": "",
                    "arm_1_mean_or_events": "",
                    "arm_1_sd_or_total": "",
                    "arm_2_name": "",
                    "arm_2_n": "",
                    "arm_2_mean_or_events": "",
                    "arm_2_sd_or_total": "",
                    "reported_effect": "",
                    "reported_ci_or_p": "",
                    "converted_effect_size": "",
                    "converted_effect_se": "",
                    "direction_higher_is_better": "",
                    "extraction_note": "",
                    "verified_by_second_author": "",
                }
            )
    pd.DataFrame(outcomes).to_csv(TABLES / "numeric_outcome_extraction_form.csv", index=False, quoting=csv.QUOTE_MINIMAL)

    rob_domains = [
        "D1_randomization_process",
        "D2_deviations_from_intended_interventions",
        "D3_missing_outcome_data",
        "D4_outcome_measurement",
        "D5_selection_of_reported_result",
        "overall",
    ]
    rob_rows = []
    for _, row in assignments.iterrows():
        for domain in rob_domains:
            rob_rows.append(
                {
                    "study_id": row["study_id"],
                    "pmid": row["pmid"],
                    "domain": domain,
                    "judgement": "",
                    "support_for_judgement": "",
                    "reviewer": row["primary_reviewer"],
                    "second_author_checked": "",
                    "consensus_judgement": "",
                }
            )
    pd.DataFrame(rob_rows).to_csv(TABLES / "rob2_assessment_form.csv", index=False, quoting=csv.QUOTE_MINIMAL)

    readiness = assignments[["study_id", "pmid", "title", "intervention_node_prelim"]].copy()
    readiness_fields = {
        "delivery_setting_score_0_2": "",
        "workforce_fit_score_0_2": "",
        "equipment_burden_score_0_2": "",
        "dose_clarity_score_0_2": "",
        "safety_monitoring_score_0_2": "",
        "adherence_feasibility_score_0_2": "",
        "procurement_burden_score_0_2": "",
        "india_primary_care_readiness_total_0_14": "",
        "implementation_readiness_category": "",
        "readiness_notes": "",
    }
    for col, default in readiness_fields.items():
        readiness[col] = default
    readiness.to_csv(TABLES / "india_implementation_readiness_form.csv", index=False, quoting=csv.QUOTE_MINIMAL)

    codebook = f"""# Extraction Codebook v1

Generated: 2026-05-18

## Reviewers

- Primary author 1: {AUTHOR_A}
- Primary author 2: {AUTHOR_B}
- Arbitration: joint consensus between both authors

## Core Forms

- `results/tables/dual_author_fulltext_assignments.csv`: full-text verification and reviewer allocation.
- `results/tables/study_characteristics_extraction_form.csv`: design, population, intervention and comparator extraction.
- `results/tables/numeric_outcome_extraction_form.csv`: synthesis-ready numeric outcomes by study and outcome.
- `results/tables/rob2_assessment_form.csv`: Cochrane RoB 2 domain-level judgements.
- `results/tables/india_implementation_readiness_form.csv`: Indian primary-care deliverability scoring.

## Extraction Rules

1. Do not mark a study as finally included until the full text has been checked by at least one author and conflicts have been resolved.
2. Use the longest common clinically relevant follow-up for primary synthesis; retain all timepoints in notes if multiple are reported.
3. Prefer intention-to-treat values when both intention-to-treat and per-protocol results are available.
4. For continuous outcomes, extract mean, SD and n by arm. If only change scores are available, extract change-score data and note this explicitly.
5. For binary frailty reversal or adverse events, extract events and denominators by arm.
6. Keep comparator wording literal during extraction; collapse comparator nodes only after all records are extracted.
7. NMA eligibility requires final comparator-node connectivity and a transitivity table. Do not infer this from title/abstract screening.

## Implementation-Readiness Scoring

Score each domain 0 to 2, where 2 is most feasible for Indian primary care:

- Delivery setting: 2 = home/community/primary care, 1 = outpatient/day service, 0 = hospital/residential-only.
- Workforce fit: 2 = ASHA/ANM/physiotherapist/community worker feasible, 1 = specialist supervision intermittently needed, 0 = specialist-intensive.
- Equipment burden: 2 = no/minimal equipment, 1 = low-cost equipment, 0 = machines/gym/lab equipment.
- Dose clarity: 2 = replicable frequency/intensity/duration, 1 = partially specified, 0 = unclear.
- Safety monitoring: 2 = low-risk and monitored, 1 = moderate monitoring need, 0 = high-risk or poorly described.
- Adherence feasibility: 2 = adherence support/reporting clear, 1 = partial, 0 = unclear or low adherence.
- Procurement burden: 2 = no product/supplement procurement, 1 = low-cost supplement/materials, 0 = expensive/proprietary supply.
"""
    (DOCS / "extraction_codebook_v1.md").write_text(codebook, encoding="utf-8")

    print(f"assignments={len(assignments)}")
    print(f"numeric_outcome_rows={len(outcomes)}")
    print(f"rob2_rows={len(rob_rows)}")
    print(f"readiness_rows={len(readiness)}")


if __name__ == "__main__":
    main()
