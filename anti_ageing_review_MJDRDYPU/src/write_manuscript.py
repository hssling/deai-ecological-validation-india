from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import pandas as pd

from src.utils.io import append_log, load_config


def read_table(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


def value_counts_md(df: pd.DataFrame, column: str, label: str) -> str:
    if df.empty or column not in df:
        return f"| {label} | n |\n|---|---:|\n| Not available | 0 |"
    out = (
        df[column]
        .fillna("missing")
        .astype(str)
        .value_counts()
        .rename_axis(label)
        .reset_index(name="n")
    )
    return out.to_markdown(index=False)


def table_md(df: pd.DataFrame, columns: list[str], *, limit: int | None = None) -> str:
    if df.empty:
        return "No data available."
    keep = [col for col in columns if col in df.columns]
    if not keep:
        return "No compatible columns available."
    out = df.loc[:, keep]
    if limit:
        out = out.head(limit)
    return out.to_markdown(index=False)


def count_label(df: pd.DataFrame, column: str, value: str) -> int:
    if df.empty or column not in df:
        return 0
    return int((df[column].fillna("").astype(str) == value).sum())


def build_summary(tables: dict[str, pd.DataFrame]) -> dict[str, int]:
    raw = tables["raw"]
    dedup = tables["dedup"]
    screened = tables["screened"]
    full_text = tables["full_text"]
    scores = tables["scores"]
    return {
        "raw_records": len(raw),
        "deduplicated_records": len(dedup),
        "screened_records": len(screened),
        "screen_include": count_label(screened, "screen_label", "include"),
        "screen_uncertain": count_label(screened, "screen_label", "uncertain"),
        "screen_exclude": count_label(screened, "screen_label", "exclude"),
        "full_text_candidates": len(full_text),
        "intervention_groups": len(scores),
        "human_records": int(scores.get("human_records", pd.Series(dtype=int)).sum()) if not scores.empty else 0,
        "animal_records": int(scores.get("animal_records", pd.Series(dtype=int)).sum()) if not scores.empty else 0,
        "cellular_records": int(scores.get("cellular_records", pd.Series(dtype=int)).sum()) if not scores.empty else 0,
    }


def top_included_records(screened: pd.DataFrame) -> pd.DataFrame:
    if screened.empty or "screen_label" not in screened:
        return pd.DataFrame()
    out = screened[screened["screen_label"].eq("include")].copy()
    if "screen_confidence" in out:
        out = out.sort_values(["screen_confidence", "year"], ascending=[False, False])
    return out


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def run(cfg):
    rt = cfg["paths"]["results_tables"]
    tables = {
        "raw": read_table(rt / "raw_records_all.csv"),
        "dedup": read_table(rt / "master_records_dedup.csv"),
        "screened": read_table(rt / "title_abstract_screening.csv"),
        "full_text": read_table(rt / "full_text_status.csv"),
        "scores": read_table(rt / "intervention_evidence_scores.csv"),
        "readiness": read_table(rt / "translational_readiness.csv"),
        "mechanisms": read_table(rt / "mechanism_evidence_matrix.csv"),
        "hype": read_table(rt / "hype_topic_summary.csv"),
        "vote": read_table(rt / "structured_vote_counting.csv"),
        "meta": read_table(rt / "meta_analysis_results.csv"),
        "search": read_table(rt / "search_runs.csv"),
        "duplicates": read_table(rt / "unresolved_duplicate_report.csv"),
        "full_text_decisions": read_table(rt / "full_text_screening_decisions.csv"),
        "human_queue": read_table(rt / "human_evidence_priority_queue.csv"),
        "ranking": read_table(rt / "intervention_credibility_ranking.csv"),
        "verification": read_table(rt / "full_text_verification_priority_human.csv"),
        "effects": read_table(rt / "effect_size_extraction_priority_human.csv"),
        "formal_rob": read_table(rt / "risk_of_bias_formal_preliminary_human.csv"),
        "duplicate_cohorts": read_table(rt / "duplicate_cohort_checks.csv"),
    }
    summary = build_summary(tables)

    scores = tables["scores"]
    top_scores = (
        scores.sort_values(["max_claim_score", "human_records"], ascending=False).head(14)
        if not scores.empty
        else pd.DataFrame()
    )
    ranking = tables["ranking"]
    if not ranking.empty:
        top_scores = ranking.head(14)
    included = top_included_records(tables["screened"])
    current_date = datetime.now().strftime("%Y-%m-%d")

    top_scores_md = table_md(
        top_scores,
        [
            "rank",
            "intervention_name",
            "n_extracted_records",
            "credibility_score",
            "credibility_tier",
            "human_records",
            "human_trial_records",
            "healthspan_records",
            "hard_ageing_records",
            "biomarker_records",
            "hype_rate",
            "n_records",
            "max_claim_score",
            "mean_claim_score",
            "animal_records",
            "cellular_records",
            "classification",
        ],
    )
    readiness_md = table_md(
        tables["readiness"],
        ["intervention_name", "translational_category", "credibility_score", "human_records", "hype_rate", "classification", "max_claim_score"],
    )
    mechanisms_md = table_md(tables["mechanisms"], list(tables["mechanisms"].columns), limit=12)
    vote_md = table_md(tables["vote"], list(tables["vote"].columns), limit=20)
    search_md = table_md(
        tables["search"],
        ["source", "query", "records", "status", "error"],
        limit=20,
    )
    include_queue_md = table_md(
        included,
        ["title", "year", "journal", "intervention_classes", "outcome_terms", "evidence_model", "url"],
        limit=30,
    )

    retrieval_md = value_counts_md(tables["full_text"], "retrieval_status", "retrieval_status")
    screening_md = value_counts_md(tables["screened"], "screen_label", "screen_label")
    model_md = value_counts_md(tables["screened"], "evidence_model", "evidence_model")
    source_md = value_counts_md(tables["raw"], "source", "source")
    classification_md = value_counts_md(scores, "classification", "classification")
    verification_md = value_counts_md(tables["verification"], "verification_status", "verification_status")
    source_text_md = value_counts_md(tables["verification"], "source_text_type", "source_text_type")
    effect_status_md = value_counts_md(tables["effects"], "effect_size_extraction_status", "effect_size_extraction_status")
    rob_md = value_counts_md(tables["formal_rob"], "rob_overall", "rob_overall")
    priority_band_md = value_counts_md(tables["full_text_decisions"], "full_text_priority_band", "full_text_priority_band")
    human_queue_md = table_md(
        tables["human_queue"],
        ["title", "year", "journal", "intervention_name", "study_design", "ageing_domain_category", "full_text_priority_score", "retrieval_status"],
        limit=20,
    )
    verification_examples_md = table_md(
        tables["verification"],
        ["title", "source_text_type", "verification_status", "provisional_full_text_eligibility", "has_intervention_signal", "has_ageing_outcome_signal"],
        limit=20,
    )
    rob_examples_md = table_md(
        tables["formal_rob"],
        ["title", "rob_randomization", "rob_blinding", "rob_missing_data", "rob_confounding", "rob_outcome_measurement", "rob_overall"],
        limit=20,
    )
    duplicate_cohort_md = table_md(
        tables["duplicate_cohorts"],
        ["check_type", "duplicate_key", "n_records", "manual_action"],
        limit=20,
    )

    manuscript = f"""
# Can Ageing Be Slowed or Reversed? A Reproducible Pilot Systematic Review, Evidence Map, and Mechanistic Synthesis of Anti-Ageing and Age-Reversal Interventions

## Structured Abstract

**Background:** Anti-ageing claims combine clinically established healthy-ageing interventions, biomarker-modifying therapies, preclinical geroscience, and speculative rejuvenation approaches. Treating these as equivalent can mislead clinicians, researchers, and the public.

**Objective:** To develop a reproducible evidence-mapping pipeline that separates healthspan benefit, lifespan extension, biological-age slowing, biomarker reversal, and true clinical rejuvenation claims.

**Methods:** Searches were run across PubMed, Europe PMC, and Crossref using broad and intervention-specific anti-ageing queries. Records were deduplicated by DOI, PMID, and normalized title. Title/abstract screening used conservative rules requiring both an intervention signal and an ageing-relevant outcome. Candidate studies were mapped to intervention classes, model systems, mechanistic domains, and preliminary evidence scores. A prioritized human-evidence queue was then screened against open PMC full text, PubMed abstracts, or repository abstracts where available. Meta-analysis was intentionally deferred because final verified effect sizes have not yet been extracted.

**Results:** The pilot search retrieved {summary["raw_records"]} raw metadata records and {summary["deduplicated_records"]} deduplicated records. Screening classified {summary["screen_include"]} records as include, {summary["screen_uncertain"]} as uncertain, and {summary["screen_exclude"]} as exclude. A total of {summary["full_text_candidates"]} include/uncertain records entered the full-text retrieval queue. Evidence scoring covered {summary["intervention_groups"]} intervention groups, with {summary["human_records"]} human, {summary["animal_records"]} animal, and {summary["cellular_records"]} cellular records represented across scored claims. In the prioritized human-evidence pass, open full text or abstract verification was attempted for {len(tables["verification"])} records. Exercise ranked highest in the first credibility ranking derived from extracted repository evidence; microbiome, rapamycin/mTOR, senolytic, caloric restriction, lifestyle-bundle, NAD/sirtuin, and fasting records showed human signals requiring verification rather than definitive recommendation-level evidence.

**Conclusions:** Extracted repository evidence supports a cautious hierarchy: healthspan-oriented human exercise evidence is strongest; several other interventions have human or biomarker signals requiring full-text verification; true clinical rejuvenation remains unproven in this evidence set. This draft is suitable as a transparent evidence map and protocolized manuscript scaffold, but it is not submission-ready until final manual full-text eligibility, final risk-of-bias assessment, duplicate cohort adjudication, and finalized effect-size extraction are completed.

## Keywords

ageing; longevity; healthspan; rejuvenation; biological age; epigenetic clock; senolytics; metformin; rapamycin; systematic review; evidence map

## Introduction

Anti-ageing research now spans lifestyle intervention, pharmacology, senescence biology, nutrient-sensing pathways, epigenetic clocks, regenerative medicine, plasma exchange, microbiome manipulation, supplements, and partial cellular reprogramming. These approaches are often discussed under a single anti-ageing label even though their evidentiary standards differ substantially.

This review uses a deliberately conservative taxonomy. Healthspan improvement refers to functional, clinical, or resilience benefits relevant to ageing. Lifespan extension refers to survival effects, usually in model organisms unless demonstrated in humans. Biological-age slowing refers to intervention-associated change in validated ageing biomarkers or clocks, preferably linked to clinical outcomes. Biomarker reversal refers to short-term movement in a surrogate marker and should not be treated as organismal rejuvenation. True clinical rejuvenation requires evidence that an intervention restores multiple age-impaired functions with durable clinical benefit and acceptable safety.

## Methods

### Search Strategy and Data Sources

Metadata were retrieved from PubMed, Europe PMC, and Crossref. Searches combined broad ageing terms with intervention, biological-age, rejuvenation, diet, exercise, pharmacologic, senolytic, NAD/sirtuin, microbiome, regenerative, plasma, and controversial claim terms. The current run was capped for pilot development and should be rerun with larger record limits before formal submission.

### Record Handling and Screening

Records were deduplicated using DOI, PMID, and normalized-title keys. Screening rules were intentionally conservative: records needed an intervention signal and an ageing-relevant outcome signal to be included. Records with incomplete abstracts or ambiguous ageing relevance were retained as uncertain rather than excluded when the title suggested possible relevance.

### Extraction and Evidence Scoring

Extraction in this version is metadata-assisted. Each record was assigned preliminary intervention classes, outcome terms, and model-system labels. Evidence credibility scoring combined model system, directness to ageing, mechanism plausibility, translational readiness, and penalties for preprint or hype-heavy claims. Scores are transparent prioritization aids, not formal GRADE determinations.

### Priority Full-Text Verification, Risk of Bias, and Effect Extraction

Full-text screening artifacts were created for all include/uncertain records. A high-priority human queue was ranked by human model status, trial/cohort design signal, ageing-outcome directness, retrieval availability, and screening label. For the top-priority human records, the pipeline attempted to verify source text using open PMC XML, PubMed XML abstracts, or abstracts already present in the repository. Preliminary RoB domains were generated only as structured prompts for human review. Candidate numeric effect text was extracted where available, but final effect sizes and uncertainty measures remain manually unverified.

### Duplicate Cohort Checks

Duplicate and overlapping-cohort checks used DOI, PMID, normalized titles, trial acronyms, and simplified cohort keys. These checks flag records for manual adjudication and are not treated as final duplicate-removal decisions.

### Quantitative Synthesis

Meta-analysis was deferred. The current data contain candidate numeric effect text for some prioritized human records, but they do not yet contain finalized verified effect sizes, denominators, intervention dose/duration, comparator details, or harmonized outcome definitions.

## Results

### PRISMA-Style Pilot Flow

- Raw records retrieved: {summary["raw_records"]}
- Deduplicated records: {summary["deduplicated_records"]}
- Title/abstract records screened: {summary["screened_records"]}
- Included at title/abstract stage: {summary["screen_include"]}
- Uncertain and requiring human review: {summary["screen_uncertain"]}
- Excluded at title/abstract stage: {summary["screen_exclude"]}
- Include/uncertain records assigned full-text retrieval status: {summary["full_text_candidates"]}
- Unresolved duplicate-key groups requiring manual review: {len(tables["duplicates"])}

### Screening Distribution

{screening_md}

### Full-Text Retrieval Status

{retrieval_md}

### Full-Text Screening Triage

Full-text screening artifacts were created for all include/uncertain records. These artifacts do not claim final eligibility; they provide a reproducible worklist for manual verification.

{priority_band_md}

### Prioritized Human Evidence Queue

The human-evidence queue prioritizes records most likely to affect clinical or translational conclusions. The top records are shown below.

{human_queue_md}

### Priority Human Verification Results

Open full text or abstract verification was attempted for the highest-priority human records available in the repo-derived queue.

{verification_md}

{source_text_md}

Representative verification records are shown below.

{verification_examples_md}

### Candidate Effect-Size Extraction

Candidate numeric effect text was detected where available, but final effect sizes and uncertainty measures remain unverified and are not pooled.

{effect_status_md}

### Preliminary Formal Risk of Bias

The preliminary RoB artifact provides domain-level prompts for manual review. It should not be interpreted as a final RoB 2, ROBINS-I, SYRCLE, or GRADE assessment.

{rob_md}

{rob_examples_md}

### Duplicate Cohort and Publication Checks

Duplicate and overlapping-publication checks identified records requiring manual adjudication before final synthesis.

{duplicate_cohort_md}

### Evidence Model Distribution

{model_md}

### First Intervention Credibility Ranking

{top_scores_md}

### Translational Readiness Summary

{readiness_md}

### Classification Summary

{classification_md}

### Structured Vote Counting

{vote_md}

### Mechanistic Synthesis

Candidate interventions mapped most frequently to nutrient sensing, senescence, inflammation, epigenetic regulation, mitochondrial function, autophagy/proteostasis, stem-cell biology, and microbiome-host pathways. Mechanistic labels remain preliminary when inferred from title/abstract metadata rather than confirmed full-text assays.

{mechanisms_md}

## Discussion

This synthesis is restricted to evidence extracted or verified within the repository. On that basis, exercise is the clearest high-priority human healthspan signal: it had the largest number of extracted human records, the largest number of human trial records, and the highest credibility score. This does not mean that exercise reverses ageing; it means that, among the extracted records, exercise has the strongest human-facing evidence for functional or healthspan-relevant outcomes.

Several other intervention domains have signals that are important but not yet recommendation-level in this pipeline. Microbiome, rapamycin/mTOR, senolytic, caloric-restriction, lifestyle-bundle, NAD/sirtuin, and fasting records contain human or direct-ageing signals, but the current artifacts still require manual full-text eligibility confirmation, final RoB assessment, and final effect extraction. Supplement, metformin, sleep/circadian, controversial rejuvenation, reprogramming, and stem-cell categories are more limited by surrogate endpoints, low human directness, preclinical emphasis, or hype-language burden in the extracted dataset.

The priority verification pass improved the evidence map by separating open-full-text verified records from abstract-only records and inaccessible records. It also created candidate effect-size extraction text for some prioritized human studies. These candidate snippets are useful for the next manual extraction step, but they are not final quantitative data and should not be pooled.

The most important finding is negative and methodological: no intervention class in this pilot should be described as proven to reverse human ageing. Several interventions may improve ageing-related function, modify pathways associated with ageing, or shift biomarkers, but those outcomes are not interchangeable.

## Strengths and Limitations

Strengths include reproducible searches, transparent deduplication, conservative screening, explicit separation of claim types, intervention-level evidence scoring, mechanism mapping, hype detection, figure generation, a full-text triage artifact, priority human verification, preliminary formal RoB prompts, duplicate-publication checks, and candidate effect-size extraction.

Limitations are substantial. The search was capped for pilot development. PubMed and Crossref abstract gaps reduce screening certainty. Many records remain metadata-only. The verification pass prioritized human records and therefore does not complete full-text review for all candidate animal, cellular, or mechanistic studies. RoB fields are preliminary prompts, not final judgments. Duplicate cohorts have been flagged but not adjudicated. Quantitative synthesis has not been performed because effect sizes, denominators, dose, duration, comparator details, and outcome definitions remain manually unverified.

## Submission Readiness

This manuscript is not yet ready for journal submission as a final systematic review. It can be used as a protocolized evidence map, internal review draft, or pre-submission scaffold. Required upgrades before submission are: rerun the search at full scale, manually adjudicate include/uncertain records, complete manual full-text eligibility decisions, finalize RoB, adjudicate duplicate cohorts, extract final effect sizes and intervention details, update references, and regenerate figures.

## Conclusions

Evidence for anti-ageing interventions is strongest for healthspan and functional benefit, weaker for biological-age slowing, and weakest for true clinical rejuvenation. Biomarker shifts should not be equated with rejuvenation unless accompanied by durable, clinically meaningful functional benefit and acceptable safety.
"""

    short = f"""
# Can Ageing Be Slowed or Reversed? Concise Pilot Evidence Map

The current anti-ageing review is a reproducible pilot evidence map, not a final systematic review. It retrieved {summary["raw_records"]} raw records, deduplicated to {summary["deduplicated_records"]}, and screened {summary["screened_records"]} records. Screening produced {summary["screen_include"]} includes, {summary["screen_uncertain"]} uncertain records, and {summary["screen_exclude"]} exclusions. The full-text queue currently contains {summary["full_text_candidates"]} include/uncertain records.

The strongest extracted signal is for exercise as a healthspan-oriented human evidence domain. Caloric restriction, fasting, metformin, rapamycin/mTOR modulation, microbiome interventions, senolytics, NAD/sirtuin approaches, supplements, stem-cell approaches, plasma-based approaches, and partial reprogramming should be separated by model system and outcome type. None should be presented as proven human age reversal in this pilot draft.

## Evidence Ranking

{top_scores_md}

## Required Before Submission

Full-text verification, duplicate cohort review, formal risk-of-bias assessment, effect-size extraction, final references, and refreshed figures are still required.
"""

    supplement = f"""
# Supplementary Material

Generated: {current_date}

## Search Run Audit

{search_md}

## Source Distribution

{source_md}

## Screening Distribution

{screening_md}

## Full-Text Retrieval Queue Summary

{retrieval_md}

## Full-Text Screening Priority Bands

{priority_band_md}

## Priority Human Verification Summary

{verification_md}

{source_text_md}

## Candidate Effect-Size Extraction Summary

{effect_status_md}

## Preliminary Formal Risk of Bias Summary

{rob_md}

## Duplicate Cohort Checks

{duplicate_cohort_md}

## Priority Records for Manual Full-Text Verification

{human_queue_md}

## Intervention Credibility Ranking

{top_scores_md}

## Translational Readiness

{readiness_md}

## Meta-Analysis Status

{table_md(tables["meta"], list(tables["meta"].columns))}
"""

    figure_legends = """
# Figure Legends

**Figure 1. PRISMA-style pilot flow diagram.** Flow of records through metadata retrieval, deduplication, title/abstract screening, and full-text retrieval assignment. Counts reflect the capped pilot run and should be regenerated after the full search.

**Figure 2. Evidence pyramid.** Distribution of candidate evidence by model system and evidence tier, emphasizing the distinction between human functional outcomes, animal studies, cellular studies, and surrogate biomarker evidence.

**Figure 3. Intervention-outcome heatmap.** Metadata-assisted map of intervention classes against ageing-relevant outcome categories. Cells require full-text verification before final interpretation.

**Figure 4. Mechanism network.** Preliminary intervention-mechanism network showing mapped links to nutrient sensing, senescence, inflammation, epigenetic regulation, mitochondrial pathways, autophagy/proteostasis, stem-cell biology, and microbiome-host pathways.

**Figure 5. Evidence score ranking.** Intervention-level evidence credibility ranking based on model system, outcome directness, mechanism plausibility, translational readiness, and conservative penalties for hype-heavy or preprint evidence.

**Figure 6. Hype versus evidence map.** Intervention-level comparison of credibility score from extracted repository evidence against hype-flagged record rate. Bubble size reflects number of extracted records.

**Figure 7. Evidence timeline.** Chronologic distribution of candidate anti-ageing records across intervention domains.

**Figure 8. Translational readiness matrix.** Conservative categorization of intervention classes using credibility score, human record count, human trial count, direct ageing-outcome count, and hype burden. Categories are provisional and require final full-text adjudication.
"""

    cover = """
# Cover Letter Draft

Dear Editor,

Please consider this pilot systematic review and evidence map, "Can Ageing Be Slowed or Reversed?", for consideration as a methods-oriented review or evidence-map manuscript. The manuscript uses a reproducible workflow to separate healthspan benefit, lifespan extension, biological-age slowing, biomarker reversal, and true rejuvenation claims.

The central contribution is conservative claim separation. The draft does not claim that human ageing has been clinically reversed. Instead, it identifies where evidence is strongest, where it remains surrogate-heavy, and where full-text verification is required before stronger conclusions are appropriate.

This version should be submitted only after completion of full-text verification, formal risk-of-bias assessment, duplicate cohort checks, and final reference validation.

Sincerely,
"""

    reviewer = f"""
# Reviewer Criticism Anticipation

## Current Status

This is a pilot evidence map based on {summary["raw_records"]} raw records and {summary["deduplicated_records"]} deduplicated records. It is not yet a final PRISMA-complete systematic review.

## Likely Critiques and Responses

1. **Metadata-assisted screening can misclassify studies.**  
   Response: all include and uncertain records are explicitly queued for human full-text adjudication. No final clinical recommendation depends on automated classification alone.

2. **Evidence scores are subjective.**  
   Response: scores are decomposable prioritization aids, not GRADE ratings. The final version should report component-level scoring and sensitivity to weighting.

3. **No meta-analysis is reported.**  
   Response: pooling was deliberately deferred because full-text effect sizes, denominators, dose, duration, comparator details, and outcome definitions are not yet verified.

4. **The search is capped.**  
   Response: the current run is a pilot. The protocol requires rerunning searches with higher record caps before submission.

5. **Biomarkers are being overinterpreted.**  
   Response: the manuscript explicitly separates biomarker reversal from clinical rejuvenation and treats biomarker-only claims as insufficient for age-reversal conclusions.

## Highest-Priority Fixes

- Rerun search with larger caps.
- Manually adjudicate {summary["screen_include"] + summary["screen_uncertain"]} include/uncertain records.
- Complete full-text extraction for effect sizes, dose, duration, comparator, and outcomes.
- Complete formal risk-of-bias assessment.
- Resolve unresolved duplicate title/cohort groups.
- Convert evidence scoring into transparent tables suitable for peer review.
"""

    brief = f"""
# Research Brief

The anti-ageing review now functions as a reproducible pilot evidence map. It retrieved {summary["raw_records"]} raw records, deduplicated them to {summary["deduplicated_records"]}, and identified {summary["full_text_candidates"]} records requiring full-text review.

The current evidence pattern is conservative: exercise and multidomain lifestyle interventions are strongest for healthspan-related benefit; most pharmacologic and geroscience interventions remain promising but incomplete; biomarker-heavy and preclinical approaches should not be described as proven rejuvenation.
"""

    readiness = f"""
# Submission Readiness Checklist

Generated: {current_date}

## Current Assets

- Main manuscript draft: yes
- Concise manuscript draft: yes
- Supplement: yes
- Cover letter draft: yes
- Reviewer criticism memo: yes
- Figure legends: yes
- Generated figures: yes
- Evidence tables: yes
- Full-text screening decisions artifact: yes
- Priority human verification artifact: yes
- Candidate effect-size extraction artifact: yes
- Preliminary formal RoB artifact: yes
- Duplicate cohort checks: yes

## Current Pilot Counts

- Raw records: {summary["raw_records"]}
- Deduplicated records: {summary["deduplicated_records"]}
- Included records: {summary["screen_include"]}
- Uncertain records: {summary["screen_uncertain"]}
- Excluded records: {summary["screen_exclude"]}
- Full-text candidates: {summary["full_text_candidates"]}
- Intervention groups scored: {summary["intervention_groups"]}
- Priority human records verified/attempted: {len(tables["verification"])}
- Duplicate/cohort check flags: {len(tables["duplicate_cohorts"])}

## Not Yet Submission-Ready

- Full search rerun with larger record caps: pending
- Human adjudication of include/uncertain records: pending
- Manual full-text eligibility decisions: pending
- Final formal risk-of-bias assessment: pending
- Manual duplicate cohort/publication adjudication: pending
- Final effect-size, dose, duration, and comparator extraction: pending
- Meta-analysis or justified no-pooling table: pending
- Final references and citation formatting: pending
- Journal-specific formatting: pending

## Recommended Next Command

`python -m src.search.run_search --config config/review_config.yaml`

Before running, increase `project.max_records_per_query` in `config/review_config.yaml` for the full search.
"""

    mdir = cfg["paths"]["manuscript"]
    ddir = cfg["paths"]["docs"]
    write_text(mdir / "manuscript_main.md", manuscript)
    write_text(mdir / "manuscript_short.md", short)
    write_text(mdir / "supplement.md", supplement)
    write_text(mdir / "cover_letter.md", cover)
    write_text(mdir / "reviewer_anticipation.md", reviewer)
    write_text(mdir / "figure_legends.md", figure_legends)
    write_text(ddir / "research_brief.md", brief)
    write_text(ddir / "submission_readiness.md", readiness)

    append_log(
        cfg["paths"]["logs"] / "progress.md",
        "Phase 15-17 - Manuscript Development Pass",
        "- Expanded manuscript package using live pipeline counts, PRISMA-style flow, screening summaries, retrieval status, evidence rankings, translational readiness, figure legends, supplement, reviewer memo, and submission-readiness checklist.",
        "- manuscript/manuscript_main.md\n- manuscript/manuscript_short.md\n- manuscript/supplement.md\n- manuscript/cover_letter.md\n- manuscript/reviewer_anticipation.md\n- manuscript/figure_legends.md\n- docs/research_brief.md\n- docs/submission_readiness.md",
        "- Full search rerun, human screening adjudication, full-text verification, duplicate cohort checks, final references, formal risk-of-bias assessment, and effect-size extraction remain required before submission.",
        "- Outputs remain a pilot evidence-map manuscript package based on metadata-assisted extraction, not a final PRISMA-complete systematic review.",
        "python -m src.search.run_search --config config/review_config.yaml",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/review_config.yaml")
    run(load_config(parser.parse_args().config))
