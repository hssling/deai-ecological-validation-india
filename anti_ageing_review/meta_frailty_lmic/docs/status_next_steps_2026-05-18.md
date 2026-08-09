# Status and Next Steps

Generated: 2026-05-18

## Completed

- Created IJMR-facing project scaffold.
- Created protocol v1 and PROSPERO registration draft.
- Executed full PubMed scoping pull.
- Cached PubMed JSON and XML raw files.
- Deduplicated records.
- Ran transparent title/abstract classifier.
- Created full-text priority queues and extraction template.
- Completed second-pass primary-queue triage.
- Completed conservative high-confidence extraction triage.
- Fetched available PMC open-access full texts for high-confidence candidates.
- Mined PMC XML full texts for methods, intervention, comparator, randomization, outcomes and table previews.
- Created a full-text verification and extraction workbook.
- Created preliminary network feasibility memo and node-count tables.
- Created dual-author full-text assignment, study-characteristics extraction, numeric-outcome extraction, RoB 2 and India implementation-readiness forms.
- Created IJMR audit-ready submission asset folder with first page, declarations, manuscript scaffold, figure file, supplementary appendix and cover letter hold file.
- Replaced the weak minimal manuscript scaffold with a substantive 2773-word IJMR-facing working manuscript containing full sections, five tables, figure legends and 12 references.
- Completed submission-readiness audit, reference/searchability audit and internal double-blind-style peer review.
- Reset workflow priority from asset production to real systematic-review execution.
- Ran expanded accessible searches across PubMed-existing records, Europe PMC, ClinicalTrials.gov, Crossref and OpenAlex; logged unavailable subscription databases.
- Screened expanded accessible records and fetched additional PMC full texts from expanded candidates.
- Completed first-reviewer eligibility classification for 237 mined PMC full texts.
- Mined numeric outcome candidate tables for the 39 first-reviewer primary-accessible included studies.

## Scoping Results

- PubMed reported hits: 3425.
- Records downloaded: 3418.
- Deduplicated records: 3418.
- Title/abstract records flagged as potentially relevant: 1129.
- Primary full-text queue: 297 records.
- Secondary frailty queue: 210 records.
- Community sarcopenia secondary queue: 97 records.
- Second-pass extraction candidates in primary queue: 235 records.
- High-confidence extraction candidates: 179 records.
- PMC full texts fetched and mined: 95 records.
- Records requiring publisher/library full-text access: 84 records.
- Preliminary intervention nodes with at least two candidate records: 8.
- Preliminary intervention nodes with at least two mined PMC full texts: 7.
- Dual-author full-text assignment rows: 179.
- Numeric outcome extraction rows: 1969.
- RoB 2 assessment rows: 1074.
- India implementation-readiness rows: 179.
- Submission audit checks passed: 19.
- Submission audit warnings: 0.
- Submission audit failures: 0.
- Submission audit blocking pending items: 5.
- Expanded accessible raw records: 11313.
- Expanded accessible deduplicated records: 10117.
- Expanded full-text or registry candidates: 1326.
- Expanded candidates not already in original high-confidence queue: 793.
- Additional expanded PMC full texts fetched: 142.
- Total PMC full texts mined after expansion: 237.
- First-reviewer primary-accessible included studies: 39.
- Primary-accessible studies with candidate numeric tables: 34 of 39.

## Interpretation

The evidence base is large enough for a systematic review and probably large enough for pairwise meta-analysis. NMA is still not approved because comparator connectivity, outcome compatibility and transitivity must be checked after full-text extraction.

The primary manuscript should remain India-facing by emphasizing community, home, primary-care and low-resource deliverability rather than repeating broad global exercise/nutrition rankings.

## Current Hard Gate

IJMR requires protocol registration for systematic reviews. The PROSPERO draft should be finalized and submitted before final study selection and synthesis are treated as submission-ready.

The current asset package is audit-ready but not journal-submission-ready. More importantly, asset production is now paused as a downstream task. The next priority is evidence completion: second-reviewer eligibility, publisher/library full-text retrieval, arm-level numeric extraction, RoB 2, pairwise meta-analysis datasets and NMA gate assessment.

## Immediate Work Queue

1. Author-verify the 95 mined PMC full texts in `results/tables/fulltext_verified_extraction_workbook.csv`.
2. Retrieve the 84 publisher/library full texts listed in the same workbook.
3. Exclude protocols, disease-rehabilitation-only studies and non-frailty studies using PRISMA-compatible full-text reasons.
4. Extract numeric outcome data, comparator definitions, dose, follow-up, and risk-of-bias fields.
5. Code final intervention components and implementation-readiness fields.
6. Run network-connectivity and transitivity checks before any NMA.

## Files Created by Current Run

- `data/raw/pubmed_search_2026-05-18.json`
- `data/raw/pubmed_records_2026-05-18.xml`
- `data/interim/pubmed_candidate_records.csv`
- `data/processed/screened_title_abstract.csv`
- `data/processed/screened_prioritized.csv`
- `results/tables/search_log.csv`
- `results/tables/title_abs_screening_counts.csv`
- `results/tables/fulltext_priority_counts.csv`
- `results/tables/fulltext_queue_primary_A.csv`
- `results/tables/extraction_template.csv`
- `results/tables/round2_triage_primary_A.csv`
- `results/tables/extraction_candidate_primary.csv`
- `results/tables/round2_exclusions_primary.csv`
- `results/tables/high_confidence_extraction_queue.csv`
- `results/tables/high_confidence_triage.csv`
- `results/tables/pmc_fulltext_fetch_log.csv`
- `results/tables/pmc_fulltext_mining.csv`
- `results/tables/fulltext_verified_extraction_workbook.csv`
- `results/tables/fulltext_access_status_counts.csv`
- `results/tables/fulltext_verification_status_counts.csv`
- `results/tables/network_feasibility_prelim.csv`
- `results/tables/network_prelim_node_counts.csv`
- `docs/network_feasibility_prelim_2026-05-18.md`
- `results/tables/dual_author_fulltext_assignments.csv`
- `results/tables/study_characteristics_extraction_form.csv`
- `results/tables/numeric_outcome_extraction_form.csv`
- `results/tables/rob2_assessment_form.csv`
- `results/tables/india_implementation_readiness_form.csv`
- `docs/extraction_codebook_v1.md`
- `results/tables/submission_readiness_audit.csv`
- `results/tables/reference_metadata_searchability_audit.csv`
- `docs/submission_readiness_audit_2026-05-18.md`
- `docs/internal_double_blind_peer_review_2026-05-18.md`
- `docs/author_response_revision_plan_2026-05-18.md`
- `submission_assets/IJMR_FRAILTY_INTERVENTIONS_AUDIT_READY_2026-05-18/`
- `submission_assets/IJMR_FRAILTY_INTERVENTIONS_AUDIT_READY_2026-05-18.zip`
- `submission_assets/IJMR_FRAILTY_INTERVENTIONS_AUDIT_READY_2026-05-18/IJMR_frailty_substantive_working_manuscript_2026-05-18.docx`
- `submission_assets/IJMR_FRAILTY_INTERVENTIONS_AUDIT_READY_2026-05-18/IJMR_frailty_substantive_working_manuscript_2026-05-18.md`
- `results/tables/expanded_accessible_search_log.csv`
- `results/tables/expanded_accessible_screening_counts.csv`
- `results/tables/expanded_accessible_fulltext_or_registry_candidates.csv`
- `results/tables/expanded_accessible_new_candidates_not_in_primary_queue.csv`
- `results/tables/expanded_pmc_fulltext_fetch_log.csv`
- `results/tables/pmc_fulltext_eligibility_first_reviewer.csv`
- `results/tables/pmc_accessible_primary_include_first_reviewer.csv`
- `results/tables/primary_accessible_numeric_table_mining.csv`
- `results/tables/primary_accessible_outcome_table_availability.csv`
- `results/tables/real_review_nma_gate_status.csv`
- `docs/real_systematic_review_progress_2026-05-18.md`

## Repository

- Dedicated private GitHub repository: `https://github.com/hssling/ijmr-frailty-interventions-review-2026`
- Initial pushed commit: `4d591d9bdf37b757a00dbfeb6296659ba83e182b`
- Default branch: `main`
- Large-file note: GitHub accepted the push but warned that `data/raw/pubmed_records_2026-05-18.xml` is 75.76 MB, above the recommended 50 MB threshold.
