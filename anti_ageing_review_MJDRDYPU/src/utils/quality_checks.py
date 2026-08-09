from __future__ import annotations

import argparse

import pandas as pd

from src.utils.io import append_log, load_config, save_csv


SUPPORTED = "supported_for_healthspan_related_benefit"
PROMISING = "promising_but_incomplete"
PRECLINICAL = "biomarker_or_preclinical_evidence"
SPECULATIVE = "speculative_or_hype_heavy"


REQUIRED_EXTRACTION_FIELDS = [
    "title",
    "authors",
    "year",
    "journal",
    "doi",
    "pmid",
    "study_design",
    "species_model",
    "intervention_name",
    "dose_intensity",
    "duration",
    "comparator",
    "outcome_exact",
    "ageing_domain_category",
    "effect_size",
    "uncertainty_measure",
    "follow_up_time",
    "mechanism",
    "mechanism_directness",
    "extraction_confidence",
    "missingness_flag",
]


def missing_schema_fields(df: pd.DataFrame) -> list[str]:
    return [field for field in REQUIRED_EXTRACTION_FIELDS if field not in df.columns]


def classify_issue(issue_type: str, n_records: int, severity: str, detail: str) -> dict[str, object]:
    return {
        "issue_type": issue_type,
        "n_records": int(n_records),
        "severity": severity,
        "detail": detail,
    }


def run_checks(
    extracted: pd.DataFrame,
    claims: pd.DataFrame,
    scores: pd.DataFrame,
    duplicates: pd.DataFrame,
) -> pd.DataFrame:
    issues: list[dict[str, object]] = []

    missing = missing_schema_fields(extracted)
    issues.append(
        classify_issue(
            "extraction_schema_missing_fields",
            len(missing),
            "high" if missing else "none",
            "; ".join(missing) if missing else "All required extraction fields present.",
        )
    )

    if not duplicates.empty:
        issues.append(
            classify_issue(
                "unresolved_duplicate_groups",
                len(duplicates),
                "medium",
                "Potential duplicate title/identifier groups require manual review before submission.",
            )
        )

    if not claims.empty:
        preprints_supported = claims[
            claims.get("is_preprint", pd.Series(False, index=claims.index)).astype(str).str.lower().eq("true")
            & claims.get("claim_category", pd.Series("", index=claims.index)).eq(SUPPORTED)
        ]
        issues.append(
            classify_issue(
                "preprint_treated_as_supported",
                len(preprints_supported),
                "high" if len(preprints_supported) else "none",
                "Preprints should not be treated as established evidence.",
            )
        )

        animal_or_cell_supported = claims[
            claims.get("species_model", pd.Series("", index=claims.index)).isin(["animal", "cellular"])
            & claims.get("claim_category", pd.Series("", index=claims.index)).eq(SUPPORTED)
        ]
        issues.append(
            classify_issue(
                "animal_or_cellular_claim_supported",
                len(animal_or_cell_supported),
                "high" if len(animal_or_cell_supported) else "none",
                "Animal/cellular records should not be described as human-ready evidence.",
            )
        )

        surrogate_supported = claims[
            claims.get("ageing_domain_category", pd.Series("", index=claims.index)).eq("surrogate_or_indirect")
            & claims.get("claim_category", pd.Series("", index=claims.index)).isin([SUPPORTED, PROMISING])
        ]
        issues.append(
            classify_issue(
                "surrogate_endpoint_overclassified",
                len(surrogate_supported),
                "medium" if len(surrogate_supported) else "none",
                "Surrogate-only records should not drive strong anti-ageing conclusions.",
            )
        )

        metadata_only = claims[
            claims.get("missingness_flag", pd.Series("", index=claims.index))
            .fillna("")
            .astype(str)
            .str.contains("requires_full_text", case=False, regex=False)
        ]
        issues.append(
            classify_issue(
                "metadata_only_claims",
                len(metadata_only),
                "medium" if len(metadata_only) else "none",
                "These records require full-text verification before final inference.",
            )
        )

        no_effect_size = claims[
            claims.get("effect_size", pd.Series("", index=claims.index)).fillna("").astype(str).str.len().eq(0)
        ]
        issues.append(
            classify_issue(
                "missing_effect_sizes",
                len(no_effect_size),
                "high" if len(no_effect_size) else "none",
                "Comparable effect sizes are required before meta-analysis.",
            )
        )

    if not scores.empty:
        unsupported_category_names = scores[
            scores.get("classification", pd.Series("", index=scores.index)).isin([SUPPORTED])
            & scores.get("human_records", pd.Series(0, index=scores.index)).fillna(0).astype(float).eq(0)
        ]
        issues.append(
            classify_issue(
                "intervention_supported_without_human_records",
                len(unsupported_category_names),
                "high" if len(unsupported_category_names) else "none",
                "No intervention should be marked supported for healthspan without human records.",
            )
        )

        speculative_high_score = scores[
            scores.get("classification", pd.Series("", index=scores.index)).eq(SPECULATIVE)
            & scores.get("max_claim_score", pd.Series(0, index=scores.index)).fillna(0).astype(float).ge(10)
        ]
        issues.append(
            classify_issue(
                "speculative_intervention_high_score",
                len(speculative_high_score),
                "medium" if len(speculative_high_score) else "none",
                "Speculative classes with high scores need manual review of scoring components.",
            )
        )

    return pd.DataFrame(issues)


def run(cfg):
    rt = cfg["paths"]["results_tables"]
    extracted = pd.read_csv(rt / "extracted_studies_master.csv")
    claims = pd.read_csv(rt / "claim_credibility_matrix.csv")
    scores = pd.read_csv(rt / "intervention_evidence_scores.csv")
    duplicates = pd.read_csv(rt / "unresolved_duplicate_report.csv")

    audit = run_checks(extracted, claims, scores, duplicates)
    save_csv(audit, rt / "quality_control_flags.csv")

    high_or_medium = audit[audit["severity"].isin(["high", "medium"])]
    audit_md = "# Quality Control Audit\n\n" + audit.to_markdown(index=False) + "\n"
    (cfg["paths"]["logs"] / "quality_control_audit.md").write_text(audit_md, encoding="utf-8")

    append_log(
        cfg["paths"]["logs"] / "progress.md",
        "Phase 18 - Automated Quality Controls",
        f"- Ran automated QC checks for schema completeness, duplicate groups, preprint overclassification, animal/cellular overclaiming, surrogate endpoint drift, metadata-only records, missing effect sizes, and unsupported intervention classifications.\n- Flagged {len(high_or_medium)} medium/high issue categories requiring manual review.",
        "- results/tables/quality_control_flags.csv\n- logs/quality_control_audit.md",
        "- Manual full-text adjudication remains required for all metadata-only and include/uncertain records.",
        "- QC flags are conservative and may include false positives; they are intended to prevent overclaiming before submission.",
        "pytest tests -q",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/review_config.yaml")
    run(load_config(parser.parse_args().config))
