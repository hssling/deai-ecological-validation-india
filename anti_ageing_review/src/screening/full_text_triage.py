from __future__ import annotations

import argparse

import pandas as pd

from src.utils.io import append_log, load_config, save_csv


def read_csv(path):
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def priority_score(row: pd.Series) -> int:
    score = 0
    if row.get("screen_label") == "include":
        score += 15
    if row.get("species_model") == "human":
        score += 45
    elif row.get("species_model") == "animal":
        score += 15
    elif row.get("species_model") == "cellular":
        score += 5

    design = str(row.get("study_design", ""))
    if "RCT" in design or "clinical_trial" in design:
        score += 20
    elif "cohort" in design:
        score += 12

    domain = str(row.get("ageing_domain_category", ""))
    if domain == "hard_ageing_relevance":
        score += 20
    elif domain == "healthspan_functional_ageing":
        score += 18
    elif domain == "biological_ageing_biomarker":
        score += 10

    retrieval = str(row.get("retrieval_status", ""))
    if retrieval == "retrieved_open_metadata":
        score += 8
    elif retrieval == "link_available":
        score += 5

    if str(row.get("is_preprint", "False")).lower() == "true":
        score -= 10
    return max(score, 0)


def priority_band(score: int) -> str:
    if score >= 75:
        return "priority_1_human_direct_ageing"
    if score >= 55:
        return "priority_2_human_or_direct_ageing"
    if score >= 35:
        return "priority_3_contextual_or_preclinical"
    return "priority_4_low_directness_or_unclear"


def provisional_decision(row: pd.Series) -> str:
    if row.get("screen_label") == "exclude":
        return "exclude_from_full_text_queue"
    if row.get("species_model") == "human" and row.get("ageing_domain_category") in {
        "hard_ageing_relevance",
        "healthspan_functional_ageing",
        "biological_ageing_biomarker",
    }:
        return "likely_eligible_pending_full_text"
    if row.get("screen_label") == "include":
        return "possibly_eligible_pending_full_text"
    return "uncertain_pending_full_text"


def build_credibility_ranking(claims: pd.DataFrame, topics: pd.DataFrame) -> pd.DataFrame:
    if claims.empty:
        return pd.DataFrame()

    work = claims.copy()
    for col in ["claim_score", "title"]:
        if col not in work:
            work[col] = 0 if col == "claim_score" else ""

    grouped = work.groupby("intervention_name").agg(
        n_extracted_records=("title", "count"),
        human_records=("species_model", lambda x: int((x == "human").sum())),
        human_trial_records=("study_design", lambda x: int(x.astype(str).str.contains("RCT|clinical_trial", case=False, regex=True).sum())),
        hard_ageing_records=("ageing_domain_category", lambda x: int((x == "hard_ageing_relevance").sum())),
        healthspan_records=("ageing_domain_category", lambda x: int((x == "healthspan_functional_ageing").sum())),
        biomarker_records=("ageing_domain_category", lambda x: int((x == "biological_ageing_biomarker").sum())),
        surrogate_records=("ageing_domain_category", lambda x: int((x == "surrogate_or_indirect").sum())),
        max_claim_score=("claim_score", "max"),
        mean_claim_score=("claim_score", "mean"),
    ).reset_index()
    grouped["mean_claim_score"] = grouped["mean_claim_score"].round(2)

    if not topics.empty and "intervention_classes" in topics and "hype_flag" in topics:
        topic_work = topics.copy()
        topic_work["intervention_name"] = topic_work["intervention_classes"].fillna("").astype(str).str.split(";").str[0]
        hype = topic_work.groupby("intervention_name").agg(
            hype_flagged_records=("hype_flag", lambda x: int(x.astype(str).str.lower().eq("true").sum())),
            mean_hype_terms=("hype_terms_n", "mean"),
        ).reset_index()
        grouped = grouped.merge(hype, how="left", on="intervention_name")
    else:
        grouped["hype_flagged_records"] = 0
        grouped["mean_hype_terms"] = 0

    grouped[["hype_flagged_records", "mean_hype_terms"]] = grouped[
        ["hype_flagged_records", "mean_hype_terms"]
    ].fillna(0)
    grouped["mean_hype_terms"] = grouped["mean_hype_terms"].round(2)
    grouped["hype_rate"] = (grouped["hype_flagged_records"] / grouped["n_extracted_records"]).round(2)

    grouped["credibility_score"] = (
        grouped["max_claim_score"]
        + grouped["human_records"].clip(upper=10) * 0.8
        + grouped["human_trial_records"].clip(upper=5) * 1.2
        + grouped["healthspan_records"].clip(upper=5) * 0.8
        + grouped["hard_ageing_records"].clip(upper=5) * 0.8
        + grouped["biomarker_records"].clip(upper=5) * 0.3
        - grouped["surrogate_records"].clip(upper=20) * 0.15
        - grouped["hype_rate"] * 2
    ).round(2)

    def tier(row):
        if row["human_records"] >= 10 and row["human_trial_records"] >= 3 and row["healthspan_records"] >= 3:
            return "highest_current_human_healthspan_signal"
        if row["human_records"] >= 3 and row["human_trial_records"] >= 1 and (row["hard_ageing_records"] + row["healthspan_records"] + row["biomarker_records"]) >= 1:
            return "human_signal_requires_verification"
        if row["biomarker_records"] >= 1 or row["human_records"] >= 1:
            return "biomarker_or_indirect_human_signal"
        if row["hard_ageing_records"] + row["healthspan_records"] >= 1:
            return "preclinical_direct_ageing_signal"
        return "low_directness_or_speculative"

    grouped["credibility_tier"] = grouped.apply(tier, axis=1)
    grouped = grouped.sort_values(
        ["credibility_score", "human_trial_records", "human_records"],
        ascending=False,
    )
    grouped.insert(0, "rank", range(1, len(grouped) + 1))
    return grouped


def run(cfg):
    rt = cfg["paths"]["results_tables"]
    extracted = read_csv(rt / "extracted_studies_master.csv")
    full_text = read_csv(rt / "full_text_status.csv")
    claims = read_csv(rt / "claim_credibility_matrix.csv")
    topics = read_csv(rt / "topic_assignments.csv")

    full_text_unique = full_text[
            [
                "title",
                "screen_label",
                "screen_confidence",
                "exclusion_reason",
                "retrieval_status",
                "retrieval_note",
                "url",
                "publication_type",
            ]
        ].drop_duplicates(subset=["title"], keep="first")
    triage = extracted.merge(
        full_text_unique,
        how="left",
        on="title",
    )
    triage["full_text_screening_status"] = "pending_full_text_verification"
    triage["full_text_decision"] = triage.apply(provisional_decision, axis=1)
    triage["full_text_priority_score"] = triage.apply(priority_score, axis=1)
    triage["full_text_priority_band"] = triage["full_text_priority_score"].map(priority_band)
    triage["full_text_screening_note"] = (
        "Artifact generated from repository metadata/extraction only; final eligibility requires full-text review."
    )

    sort_cols = ["full_text_priority_score", "screen_confidence", "year"]
    triage = triage.sort_values(sort_cols, ascending=[False, False, False])
    decisions = triage[
        [
            "title",
            "authors",
            "year",
            "journal",
            "doi",
            "pmid",
            "url",
            "publication_type",
            "screen_label",
            "screen_confidence",
            "full_text_decision",
            "full_text_screening_status",
            "full_text_priority_score",
            "full_text_priority_band",
            "retrieval_status",
            "retrieval_note",
            "study_design",
            "species_model",
            "intervention_name",
            "ageing_domain_category",
            "outcome_exact",
            "mechanism",
            "missingness_flag",
            "full_text_screening_note",
        ]
    ]

    human_priority = decisions[decisions["species_model"].eq("human")].copy()
    human_priority = human_priority.sort_values(
        ["full_text_priority_score", "screen_confidence", "year"],
        ascending=[False, False, False],
    )

    ranking = build_credibility_ranking(claims, topics)

    save_csv(decisions, rt / "full_text_screening_decisions.csv")
    save_csv(human_priority, rt / "human_evidence_priority_queue.csv")
    save_csv(ranking, rt / "intervention_credibility_ranking.csv")

    supplement_dir = cfg["paths"]["results_supplement"]
    supplement_dir.mkdir(parents=True, exist_ok=True)
    workbook = "# Full-Text Screening Artifact\n\n"
    workbook += "This artifact is generated from extracted metadata already present in the repository. It does not claim that full texts have been read.\n\n"
    workbook += "## Priority Bands\n\n"
    workbook += decisions["full_text_priority_band"].value_counts().rename_axis("priority_band").reset_index(name="n").to_markdown(index=False)
    workbook += "\n\n## Human Evidence Priority Queue\n\n"
    workbook += human_priority[
        [
            "title",
            "year",
            "journal",
            "intervention_name",
            "study_design",
            "ageing_domain_category",
            "full_text_priority_score",
            "retrieval_status",
        ]
    ].head(40).to_markdown(index=False)
    workbook += "\n\n## First Intervention Credibility Ranking\n\n"
    workbook += ranking.to_markdown(index=False) if not ranking.empty else "No ranking available."
    (supplement_dir / "full_text_screening_workbook.md").write_text(workbook + "\n", encoding="utf-8")

    append_log(
        cfg["paths"]["logs"] / "progress.md",
        "Phase 4b-5b - Full-Text Screening Artifact and Human Evidence Prioritization",
        f"- Created full-text screening decision artifact for {len(decisions)} candidate records.\n- Prioritized {len(human_priority)} human-evidence records.\n- Created first intervention credibility ranking across {len(ranking)} intervention groups using extracted evidence present in the repo.",
        "- results/tables/full_text_screening_decisions.csv\n- results/tables/human_evidence_priority_queue.csv\n- results/tables/intervention_credibility_ranking.csv\n- results/supplement/full_text_screening_workbook.md",
        "- Final eligibility remains pending full-text reading; all decisions are provisional triage labels.",
        "- The artifact is intentionally conservative and does not infer effect sizes or definitive eligibility from metadata alone.",
        "python -m src.viz.make_figures --config config/review_config.yaml",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/review_config.yaml")
    run(load_config(parser.parse_args().config))
