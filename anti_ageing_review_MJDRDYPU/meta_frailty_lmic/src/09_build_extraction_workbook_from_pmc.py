from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "tables"


def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path).fillna("")


def yes_no(value: object) -> str:
    return "yes" if str(value or "").strip() else "no"


def main() -> None:
    queue = load_csv(TABLES / "high_confidence_extraction_queue.csv")
    fetch = load_csv(TABLES / "pmc_fulltext_fetch_log.csv")
    mined = load_csv(TABLES / "pmc_fulltext_mining.csv")

    merged = queue.merge(fetch[["pmid", "pmcid", "fetch_status", "local_path"]], on="pmid", how="left")
    merged = merged.merge(mined, on="pmcid", how="left", suffixes=("", "_pmc"))

    merged["fulltext_access_status"] = merged["fetch_status"].map(
        {"fetched": "pmc_fulltext_available"}
    ).fillna("publisher_or_library_fulltext_required")
    merged["verification_status"] = merged["parse_status"].map(
        {"ok": "pmc_fulltext_mined_not_numeric_extracted"}
    ).fillna("not_fulltext_mined")
    merged["numeric_extract_required"] = "yes"
    merged["author_verification_required"] = "yes"
    merged["screening_note"] = (
        "Machine-assisted full-text mining supports extraction only; final inclusion, risk of bias, "
        "and numeric effects require author verification."
    )

    for outcome in [
        "frailty",
        "gait_speed",
        "sppb",
        "grip_strength",
        "adl",
        "falls",
        "quality_of_life",
        "adherence",
        "adverse_events",
    ]:
        merged[f"detected_{outcome}"] = merged["detected_outcomes"].str.contains(outcome, regex=False).map(
            {True: "yes", False: "no"}
        )

    merged["has_randomization_snippet"] = merged["randomization_snippet"].apply(yes_no)
    merged["has_intervention_snippet"] = merged["intervention_snippet"].apply(yes_no)
    merged["has_comparator_snippet"] = merged["comparator_snippet"].apply(yes_no)
    merged["has_results_snippet"] = merged["results_snippet"].apply(yes_no)

    ordered_cols = [
        "pmid",
        "pmcid",
        "doi",
        "title",
        "year",
        "journal",
        "url",
        "setting_code",
        "component_code",
        "intervention_node_prelim",
        "fulltext_access_status",
        "verification_status",
        "numeric_extract_required",
        "author_verification_required",
        "parse_status",
        "local_path",
        "detected_outcomes",
        "has_randomization_snippet",
        "has_intervention_snippet",
        "has_comparator_snippet",
        "has_results_snippet",
        "table_count",
        "randomization_snippet",
        "intervention_snippet",
        "comparator_snippet",
        "methods_snippet",
        "results_snippet",
        "table_text_preview",
        "screening_note",
        "extraction_status",
        "final_include",
        "exclusion_reason_fulltext",
        "risk_of_bias_status",
        "effect_size_status",
        "author_notes",
    ]

    for col in ordered_cols:
        if col not in merged.columns:
            merged[col] = ""

    for outcome in [
        "frailty",
        "gait_speed",
        "sppb",
        "grip_strength",
        "adl",
        "falls",
        "quality_of_life",
        "adherence",
        "adverse_events",
    ]:
        ordered_cols.insert(ordered_cols.index("table_count"), f"detected_{outcome}")

    out = merged[ordered_cols].sort_values(["fulltext_access_status", "year", "pmid"], ascending=[True, False, False])
    out.to_csv(TABLES / "fulltext_verified_extraction_workbook.csv", index=False, quoting=csv.QUOTE_MINIMAL)

    status = out["fulltext_access_status"].value_counts().rename_axis("fulltext_access_status").reset_index(name="n")
    status.to_csv(TABLES / "fulltext_access_status_counts.csv", index=False)

    mined_status = out["verification_status"].value_counts().rename_axis("verification_status").reset_index(name="n")
    mined_status.to_csv(TABLES / "fulltext_verification_status_counts.csv", index=False)

    print(f"workbook_rows={len(out)}")
    print(status.to_string(index=False))
    print(mined_status.to_string(index=False))


if __name__ == "__main__":
    main()
