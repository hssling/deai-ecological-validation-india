from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "tables"


def norm(value: object) -> str:
    text = str(value or "")
    if text.endswith(".0") and text[:-2].isdigit():
        text = text[:-2]
    return re.sub(r"\s+", " ", text).strip()


def norm_pmcid(value: object) -> str:
    text = norm(value)
    if not text:
        return ""
    text = re.sub(r"^PMC", "", text, flags=re.I)
    return f"PMC{text}" if text.isdigit() else text


def has(text: str, pattern: str) -> bool:
    return bool(re.search(pattern, text, flags=re.I))


def reason_flags(blob: str) -> dict[str, str]:
    return {
        "rct_signal": "yes" if has(blob, r"randomi[sz]ed|randomly assigned|random allocation|allocation conceal|controlled trial") else "no",
        "frailty_signal": "yes" if has(blob, r"\bpre[- ]?frail|\bfrail(?:ty)?\b|physical frailty|clinical frailty|frailty phenotype|tilburg frailty") else "no",
        "sarcopenia_signal": "yes" if has(blob, r"sarcopenia|sarcopenic") else "no",
        "older_adult_signal": "yes" if has(blob, r"older|elderly|aged|geriatric|\b6[05]\b|\b7[05]\b|\b80\b") else "no",
        "intervention_signal": "yes" if has(blob, r"intervention|exercise|training|nutrition|protein|supplement|home-based|tai chi|walking|balance|strength|resistance|multidomain") else "no",
        "comparator_signal": "yes" if has(blob, r"control group|usual care|waitlist|placebo|comparator|attention control") else "no",
        "outcome_signal": "yes" if has(blob, r"frailty|gait speed|sppb|short physical performance|grip strength|adl|falls|quality of life|functional") else "no",
        "protocol_or_review_signal": "yes" if has(blob, r"study protocol|protocol for|systematic review|meta-analysis|scoping review") else "no",
        "disease_specific_signal": "yes" if has(blob, r"stroke|parkinson|copd|cancer|heart failure|hip fracture|surgery|icu|intensive care|diabetes") else "no",
        "hospital_or_residential_signal": "yes" if has(blob, r"hospital|inpatient|post-acute|nursing home|residential|long-term care") else "no",
        "community_home_signal": "yes" if has(blob, r"community|home-based|home based|primary care|outpatient") else "no",
    }


def decide(flags: dict[str, str], detected_outcomes: str) -> tuple[str, str]:
    if flags["protocol_or_review_signal"] == "yes":
        return "exclude", "Protocol/review signal in full-text-mined fields"
    if flags["rct_signal"] == "no":
        return "exclude", "Randomized design not confirmed in mined full-text fields"
    if flags["older_adult_signal"] == "no":
        return "exclude", "Older-adult population not confirmed"
    if flags["intervention_signal"] == "no":
        return "exclude", "Relevant intervention not confirmed"
    if flags["comparator_signal"] == "no":
        return "defer_second_reviewer", "Comparator not clearly confirmed from mined fields"
    if flags["outcome_signal"] == "no" and not detected_outcomes:
        return "exclude", "Relevant frailty/function/safety outcome not confirmed"
    if flags["frailty_signal"] == "yes" and flags["community_home_signal"] == "yes" and flags["disease_specific_signal"] == "no":
        return "include_primary_accessible", "Community/home/primary-care frailty RCT confirmed by mined full-text fields"
    if flags["frailty_signal"] == "yes" and flags["hospital_or_residential_signal"] == "yes":
        return "include_secondary_setting", "Frailty RCT but setting likely hospital/residential or mixed"
    if flags["frailty_signal"] == "yes" and flags["disease_specific_signal"] == "yes":
        return "include_secondary_disease_specific", "Frailty RCT but disease-specific population"
    if flags["sarcopenia_signal"] == "yes":
        return "secondary_sarcopenia_verify", "Sarcopenia/vulnerability RCT; frailty-primary status requires verification"
    return "defer_second_reviewer", "Eligibility plausible but frailty/setting classification needs second review"


def main() -> None:
    mining = pd.read_csv(TABLES / "pmc_fulltext_mining.csv").fillna("")
    workbook = pd.read_csv(TABLES / "fulltext_verified_extraction_workbook.csv").fillna("")
    expanded = pd.read_csv(TABLES / "expanded_accessible_fulltext_or_registry_candidates.csv").fillna("")

    workbook["pmcid_norm"] = workbook["pmcid"].map(norm_pmcid)
    expanded["pmcid_norm"] = expanded["pmcid"].map(norm_pmcid)
    mining["pmcid_norm"] = mining["pmcid"].map(norm_pmcid)

    meta_cols = ["pmcid_norm", "pmid", "doi", "title", "year", "journal", "url", "intervention_node_prelim"]
    meta_existing = workbook[[c for c in meta_cols if c in workbook.columns]].copy()
    meta_existing["evidence_source_set"] = "original_high_confidence"

    expanded_cols = ["pmcid_norm", "pmid", "doi", "title", "year", "journal", "url", "intervention_node_expanded"]
    meta_expanded = expanded[[c for c in expanded_cols if c in expanded.columns]].copy()
    meta_expanded = meta_expanded.rename(columns={"intervention_node_expanded": "intervention_node_prelim"})
    meta_expanded["evidence_source_set"] = "expanded_accessible_search"

    meta = pd.concat([meta_existing, meta_expanded], ignore_index=True).fillna("")
    meta = meta.sort_values("evidence_source_set").drop_duplicates("pmcid_norm", keep="first")

    out = mining.merge(meta, on="pmcid_norm", how="left", suffixes=("_mined", "")).fillna("")
    rows = []
    for _, row in out.iterrows():
        blob = " ".join(
            norm(row.get(col, ""))
            for col in [
                "article_title",
                "title",
                "abstract",
                "randomization_snippet",
                "intervention_snippet",
                "comparator_snippet",
                "methods_snippet",
                "results_snippet",
                "table_text_preview",
            ]
        )
        flags = reason_flags(blob)
        decision, reason = decide(flags, norm(row.get("detected_outcomes", "")))
        rows.append(
            {
                **{k: row.get(k, "") for k in ["pmcid", "pmid", "doi", "title", "year", "journal", "url", "evidence_source_set", "intervention_node_prelim"]},
                "article_title_mined": row.get("article_title", ""),
                "first_reviewer_fulltext_decision": decision,
                "first_reviewer_reason": reason,
                **flags,
                "detected_outcomes": row.get("detected_outcomes", ""),
                "randomization_snippet": row.get("randomization_snippet", ""),
                "intervention_snippet": row.get("intervention_snippet", ""),
                "comparator_snippet": row.get("comparator_snippet", ""),
                "results_snippet": row.get("results_snippet", ""),
                "second_reviewer_decision": "",
                "consensus_decision": "",
                "consensus_reason": "",
            }
        )

    elig = pd.DataFrame(rows)
    elig.to_csv(TABLES / "pmc_fulltext_eligibility_first_reviewer.csv", index=False)
    elig["first_reviewer_fulltext_decision"].value_counts().rename_axis("decision").reset_index(name="n").to_csv(
        TABLES / "pmc_fulltext_eligibility_first_reviewer_counts.csv", index=False
    )
    primary = elig[elig["first_reviewer_fulltext_decision"].eq("include_primary_accessible")].copy()
    primary.to_csv(TABLES / "pmc_accessible_primary_include_first_reviewer.csv", index=False)
    print(elig["first_reviewer_fulltext_decision"].value_counts().to_string())
    print(f"primary_accessible_first_reviewer={len(primary)}")


if __name__ == "__main__":
    main()
