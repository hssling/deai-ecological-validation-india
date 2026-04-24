
---
## Phase 2 - Source Discovery and Search Automation
Date/time: 2026-04-23 01:35:30

Completed:
- Ran 11 query strings across PubMed, Europe PMC, and Crossref.
- Retrieved 770 raw metadata rows.

Outputs created:
- results/tables/search_runs.csv
- results/tables/raw_records_all.csv

Remaining tasks:
- Full search should be rerun with larger record caps before submission.
- Full-text retrieval remains pending.

Risks/limitations:
- PubMed abstracts are not fetched in this pilot pass; Europe PMC abstracts support screening where available.
- Crossref metadata is abstract-limited.

Exact next command:
`python src/dedup/deduplicate.py --config config/review_config.yaml`

---
## Phase 3 - Deduplication and Record Hygiene
Date/time: 2026-04-23 01:35:30

Completed:
- Standardized DOI/PMID/title keys.
- Reduced 770 raw rows to 715 deduplicated records.
- Flagged 46 duplicate key groups.

Outputs created:
- results/tables/master_records_dedup.csv
- results/tables/dedup_log.csv
- results/tables/unresolved_duplicate_report.csv

Remaining tasks:
- Manual review of unresolved duplicate title variants remains pending.

Risks/limitations:
- Records without DOI/PMID depend on normalized title matching and may under/over-deduplicate.

Exact next command:
`python src/screening/screen_records.py --config config/review_config.yaml`

---
## Phase 4 - Autonomous Screening Engine
Date/time: 2026-04-23 01:35:30

Completed:
- Screened 715 title/abstract records using conservative rules.
- Included 4; uncertain 378; excluded 333.

Outputs created:
- results/tables/title_abstract_screening.csv
- results/tables/full_text_screening.csv

Remaining tasks:
- Human verification of all include/uncertain records remains mandatory.
- Full-text screening is initialized but not complete.

Risks/limitations:
- Abstract gaps reduce confidence for PubMed/Crossref-only records.

Exact next command:
`python src/retrieval/assess_full_text.py --config config/review_config.yaml`

---
## Phase 5 - Full Text Retrieval and Organization
Date/time: 2026-04-23 01:35:30

Completed:
- Assigned retrieval status to 382 include/uncertain records.

Outputs created:
- results/tables/full_text_status.csv

Remaining tasks:
- Actual PDF/full-text download and copyright-compliant review remain pending.

Risks/limitations:
- Some records are metadata-only; evidence completeness is limited.

Exact next command:
`python src/extraction/extract_metadata.py --config config/review_config.yaml`

---
## Phase 6 - Structured Data Extraction
Date/time: 2026-04-23 01:35:30

Completed:
- Created metadata-assisted extraction table for 382 candidate studies.

Outputs created:
- results/tables/extracted_studies_master.csv
- metadata/extraction_dictionary.csv

Remaining tasks:
- Full effect sizes, doses, durations, and bias fields require full-text extraction.

Risks/limitations:
- Metadata extraction is preliminary and explicitly flagged.

Exact next command:
`python src/grading/score_evidence.py --config config/review_config.yaml`

---
## Phase 7-8 - Risk of Bias and Evidence Scoring
Date/time: 2026-04-23 01:35:30

Completed:
- Scored 382 claim-level records and 14 intervention groups.

Outputs created:
- results/tables/risk_of_bias.csv
- results/tables/intervention_evidence_scores.csv
- results/tables/claim_credibility_matrix.csv

Remaining tasks:
- Risk of bias is design-level preliminary; full RoB requires full text.

Risks/limitations:
- Scores are metadata-assisted and conservative.

Exact next command:
`python src/mechanisms/map_mechanisms.py --config config/review_config.yaml`

---
## Phase 9 - Mechanistic Mapping
Date/time: 2026-04-23 01:35:30

Completed:
- Mapped 419 intervention-mechanism edges.

Outputs created:
- results/tables/intervention_mechanism_map.csv
- results/tables/mechanism_evidence_matrix.csv

Remaining tasks:
- Direct/inferred mechanism labels require full-text verification.

Risks/limitations:
- Mechanism mapping from abstracts may miss measured pathways.

Exact next command:
`python src/nlp/topic_hype.py --config config/review_config.yaml`

---
## Phase 10 - NLP/Text Mining Augmentation
Date/time: 2026-04-23 01:35:31

Completed:
- Assigned topic clusters and hype flags to 382 records.

Outputs created:
- results/tables/topic_assignments.csv
- results/tables/hype_topic_summary.csv
- docs/nlp_summary.md

Remaining tasks:
- Embedding-based clustering can be added later.

Risks/limitations:
- Hype detection is lexical and preliminary.

Exact next command:
`python src/meta_analysis/synthesize.py --config config/review_config.yaml`

---
## Phase 11 - Meta-analysis / Quantitative Synthesis
Date/time: 2026-04-23 01:35:31

Completed:
- Created meta-analysis readiness table.
- Deferred pooling because effect sizes require full-text extraction.

Outputs created:
- results/tables/meta_analysis_inputs.csv
- results/tables/meta_analysis_results.csv
- results/tables/structured_vote_counting.csv

Remaining tasks:
- Full-text extraction of effect sizes is required before any pooled estimate.

Risks/limitations:
- Vote counting is descriptive and should not be overinterpreted.

Exact next command:
`python src/viz/make_figures.py --config config/review_config.yaml`

---
## Phase 14 - Mandatory Figures
Date/time: 2026-04-23 01:35:34

Completed:
- Generated PRISMA, evidence pyramid, heatmap, mechanism network, evidence ranking, hype map, timeline, and translational matrix where data permitted.

Outputs created:
- results/figures/*.png

Remaining tasks:
- Figure styling should be refined before journal submission.

Risks/limitations:
- Some figures are pilot metadata maps, not final full-text synthesis figures.

Exact next command:
`python src/write_manuscript.py --config config/review_config.yaml`

---
## Phase 15-17 - Manuscript Writing and Journal Positioning
Date/time: 2026-04-23 01:35:34

Completed:
- Drafted main manuscript, short version, supplement, cover letter, reviewer memo, figure legends, and research brief.

Outputs created:
- manuscript/*.md
- docs/research_brief.md

Remaining tasks:
- Full-text verified extraction and final references needed before submission.

Risks/limitations:
- Manuscript is a rigorous pilot draft, not final publication-ready systematic review until full-text verification.

Exact next command:
`pytest tests -q`

---
## Phase 19 - Regression Tests After Verification Pass
Date/time: 2026-04-23 11:38:10

Completed:
- Ran unit tests after full-text triage, priority verification, figure regeneration, manuscript update, and QC pass.
- Test result: 8 passed.

Outputs created:
- .pytest_cache

Remaining tasks:
- Add integration tests for open-text retrieval and manuscript artifact consistency.

Risks/limitations:
- Tests validate deterministic pipeline logic; they do not validate final manual full-text interpretation.

Exact next command:
`python -m src.search.run_search --config config/review_config.yaml`

---
## Phase 19 - Tests
Date/time: 2026-04-23 11:21:25

Completed:
- Added tests for extraction schema validation, animal/cellular overclassification prevention, and QC flag behavior.
- Ran unit tests successfully: 8 passed.

Outputs created:
- tests/test_pipeline_units.py

Remaining tasks:
- Add integration tests for full pipeline execution after the full-scale search is rerun.

Risks/limitations:
- Current tests verify core deterministic logic and QC guardrails; they do not validate full-text extraction accuracy.

Exact next command:
`python -m src.search.run_search --config config/review_config.yaml`

---
## Phase 4 - Autonomous Screening Engine
Date/time: 2026-04-23 01:36:31

Completed:
- Screened 715 title/abstract records using conservative rules.
- Included 20; uncertain 362; excluded 333.

Outputs created:
- results/tables/title_abstract_screening.csv
- results/tables/full_text_screening.csv

Remaining tasks:
- Human verification of all include/uncertain records remains mandatory.
- Full-text screening is initialized but not complete.

Risks/limitations:
- Abstract gaps reduce confidence for PubMed/Crossref-only records.

Exact next command:
`python src/retrieval/assess_full_text.py --config config/review_config.yaml`

---
## Phase 5 - Full Text Retrieval and Organization
Date/time: 2026-04-23 01:36:33

Completed:
- Assigned retrieval status to 382 include/uncertain records.

Outputs created:
- results/tables/full_text_status.csv

Remaining tasks:
- Actual PDF/full-text download and copyright-compliant review remain pending.

Risks/limitations:
- Some records are metadata-only; evidence completeness is limited.

Exact next command:
`python src/extraction/extract_metadata.py --config config/review_config.yaml`

---
## Phase 6 - Structured Data Extraction
Date/time: 2026-04-23 01:36:36

Completed:
- Created metadata-assisted extraction table for 382 candidate studies.

Outputs created:
- results/tables/extracted_studies_master.csv
- metadata/extraction_dictionary.csv

Remaining tasks:
- Full effect sizes, doses, durations, and bias fields require full-text extraction.

Risks/limitations:
- Metadata extraction is preliminary and explicitly flagged.

Exact next command:
`python src/grading/score_evidence.py --config config/review_config.yaml`

---
## Phase 7-8 - Risk of Bias and Evidence Scoring
Date/time: 2026-04-23 01:36:38

Completed:
- Scored 382 claim-level records and 14 intervention groups.

Outputs created:
- results/tables/risk_of_bias.csv
- results/tables/intervention_evidence_scores.csv
- results/tables/claim_credibility_matrix.csv

Remaining tasks:
- Risk of bias is design-level preliminary; full RoB requires full text.

Risks/limitations:
- Scores are metadata-assisted and conservative.

Exact next command:
`python src/mechanisms/map_mechanisms.py --config config/review_config.yaml`

---
## Phase 9 - Mechanistic Mapping
Date/time: 2026-04-23 01:36:39

Completed:
- Mapped 419 intervention-mechanism edges.

Outputs created:
- results/tables/intervention_mechanism_map.csv
- results/tables/mechanism_evidence_matrix.csv

Remaining tasks:
- Direct/inferred mechanism labels require full-text verification.

Risks/limitations:
- Mechanism mapping from abstracts may miss measured pathways.

Exact next command:
`python src/nlp/topic_hype.py --config config/review_config.yaml`

---
## Phase 10 - NLP/Text Mining Augmentation
Date/time: 2026-04-23 01:36:44

Completed:
- Assigned topic clusters and hype flags to 382 records.

Outputs created:
- results/tables/topic_assignments.csv
- results/tables/hype_topic_summary.csv
- docs/nlp_summary.md

Remaining tasks:
- Embedding-based clustering can be added later.

Risks/limitations:
- Hype detection is lexical and preliminary.

Exact next command:
`python src/meta_analysis/synthesize.py --config config/review_config.yaml`

---
## Phase 11 - Meta-analysis / Quantitative Synthesis
Date/time: 2026-04-23 01:36:46

Completed:
- Created meta-analysis readiness table.
- Deferred pooling because effect sizes require full-text extraction.

Outputs created:
- results/tables/meta_analysis_inputs.csv
- results/tables/meta_analysis_results.csv
- results/tables/structured_vote_counting.csv

Remaining tasks:
- Full-text extraction of effect sizes is required before any pooled estimate.

Risks/limitations:
- Vote counting is descriptive and should not be overinterpreted.

Exact next command:
`python src/viz/make_figures.py --config config/review_config.yaml`

---
## Phase 14 - Mandatory Figures
Date/time: 2026-04-23 01:36:59

Completed:
- Generated PRISMA, evidence pyramid, heatmap, mechanism network, evidence ranking, hype map, timeline, and translational matrix where data permitted.

Outputs created:
- results/figures/*.png

Remaining tasks:
- Figure styling should be refined before journal submission.

Risks/limitations:
- Some figures are pilot metadata maps, not final full-text synthesis figures.

Exact next command:
`python src/write_manuscript.py --config config/review_config.yaml`

---
## Phase 15-17 - Manuscript Writing and Journal Positioning
Date/time: 2026-04-23 01:37:02

Completed:
- Drafted main manuscript, short version, supplement, cover letter, reviewer memo, figure legends, and research brief.

Outputs created:
- manuscript/*.md
- docs/research_brief.md

Remaining tasks:
- Full-text verified extraction and final references needed before submission.

Risks/limitations:
- Manuscript is a rigorous pilot draft, not final publication-ready systematic review until full-text verification.

Exact next command:
`pytest tests -q`

---
## Phase 1 - Protocol and Governance
Date/time: 2026-04-23 01:37:42

Completed:
- Created PRISMA-style protocol and governance documents.
- Defined anti-ageing, healthspan, lifespan extension, biomarker reversal, and clinical rejuvenation distinctions.
- Created inclusion/exclusion, screening, extraction, evidence, risk-of-bias, and mechanism mapping manuals.

Outputs created:
- docs/protocol.md
- docs/inclusion_exclusion.md
- docs/screening_manual.md
- docs/extraction_manual.md
- docs/evidence_framework.md
- docs/risk_of_bias_plan.md
- docs/mechanism_mapping_plan.md
- docs/decision_log.md

Remaining tasks:
- Register protocol externally if preparing formal submission.
- Expand PRISMA checklist and PRESS search peer review.

Risks/limitations:
- This is an autonomous protocol draft and requires human sign-off before registration.

Exact next command:
`python -m src.search.run_search --config config/review_config.yaml`

---
## Phase 2 - Source Discovery and Search Automation
Date/time: 2026-04-23 01:39:33

Completed:
- Ran 11 query strings across PubMed, Europe PMC, and Crossref.
- Retrieved 770 raw metadata rows.

Outputs created:
- results/tables/search_runs.csv
- results/tables/raw_records_all.csv

Remaining tasks:
- Full search should be rerun with larger record caps before submission.
- Full-text retrieval remains pending.

Risks/limitations:
- PubMed abstracts are not fetched in this pilot pass; Europe PMC abstracts support screening where available.
- Crossref metadata is abstract-limited.

Exact next command:
`python src/dedup/deduplicate.py --config config/review_config.yaml`

---
## Phase 3 - Deduplication and Record Hygiene
Date/time: 2026-04-23 01:39:33

Completed:
- Standardized DOI/PMID/title keys.
- Reduced 770 raw rows to 715 deduplicated records.
- Flagged 46 duplicate key groups.

Outputs created:
- results/tables/master_records_dedup.csv
- results/tables/dedup_log.csv
- results/tables/unresolved_duplicate_report.csv

Remaining tasks:
- Manual review of unresolved duplicate title variants remains pending.

Risks/limitations:
- Records without DOI/PMID depend on normalized title matching and may under/over-deduplicate.

Exact next command:
`python src/screening/screen_records.py --config config/review_config.yaml`

---
## Phase 4 - Autonomous Screening Engine
Date/time: 2026-04-23 01:39:33

Completed:
- Screened 715 title/abstract records using conservative rules.
- Included 20; uncertain 362; excluded 333.

Outputs created:
- results/tables/title_abstract_screening.csv
- results/tables/full_text_screening.csv

Remaining tasks:
- Human verification of all include/uncertain records remains mandatory.
- Full-text screening is initialized but not complete.

Risks/limitations:
- Abstract gaps reduce confidence for PubMed/Crossref-only records.

Exact next command:
`python src/retrieval/assess_full_text.py --config config/review_config.yaml`

---
## Phase 5 - Full Text Retrieval and Organization
Date/time: 2026-04-23 01:39:33

Completed:
- Assigned retrieval status to 382 include/uncertain records.

Outputs created:
- results/tables/full_text_status.csv

Remaining tasks:
- Actual PDF/full-text download and copyright-compliant review remain pending.

Risks/limitations:
- Some records are metadata-only; evidence completeness is limited.

Exact next command:
`python src/extraction/extract_metadata.py --config config/review_config.yaml`

---
## Phase 6 - Structured Data Extraction
Date/time: 2026-04-23 01:39:33

Completed:
- Created metadata-assisted extraction table for 382 candidate studies.

Outputs created:
- results/tables/extracted_studies_master.csv
- metadata/extraction_dictionary.csv

Remaining tasks:
- Full effect sizes, doses, durations, and bias fields require full-text extraction.

Risks/limitations:
- Metadata extraction is preliminary and explicitly flagged.

Exact next command:
`python src/grading/score_evidence.py --config config/review_config.yaml`

---
## Phase 7-8 - Risk of Bias and Evidence Scoring
Date/time: 2026-04-23 01:39:33

Completed:
- Scored 382 claim-level records and 14 intervention groups.

Outputs created:
- results/tables/risk_of_bias.csv
- results/tables/intervention_evidence_scores.csv
- results/tables/claim_credibility_matrix.csv

Remaining tasks:
- Risk of bias is design-level preliminary; full RoB requires full text.

Risks/limitations:
- Scores are metadata-assisted and conservative.

Exact next command:
`python src/mechanisms/map_mechanisms.py --config config/review_config.yaml`

---
## Phase 9 - Mechanistic Mapping
Date/time: 2026-04-23 01:39:34

Completed:
- Mapped 419 intervention-mechanism edges.

Outputs created:
- results/tables/intervention_mechanism_map.csv
- results/tables/mechanism_evidence_matrix.csv

Remaining tasks:
- Direct/inferred mechanism labels require full-text verification.

Risks/limitations:
- Mechanism mapping from abstracts may miss measured pathways.

Exact next command:
`python src/nlp/topic_hype.py --config config/review_config.yaml`

---
## Phase 10 - NLP/Text Mining Augmentation
Date/time: 2026-04-23 01:39:34

Completed:
- Assigned topic clusters and hype flags to 382 records.

Outputs created:
- results/tables/topic_assignments.csv
- results/tables/hype_topic_summary.csv
- docs/nlp_summary.md

Remaining tasks:
- Embedding-based clustering can be added later.

Risks/limitations:
- Hype detection is lexical and preliminary.

Exact next command:
`python src/meta_analysis/synthesize.py --config config/review_config.yaml`

---
## Phase 11 - Meta-analysis / Quantitative Synthesis
Date/time: 2026-04-23 01:39:34

Completed:
- Created meta-analysis readiness table.
- Deferred pooling because effect sizes require full-text extraction.

Outputs created:
- results/tables/meta_analysis_inputs.csv
- results/tables/meta_analysis_results.csv
- results/tables/structured_vote_counting.csv

Remaining tasks:
- Full-text extraction of effect sizes is required before any pooled estimate.

Risks/limitations:
- Vote counting is descriptive and should not be overinterpreted.

Exact next command:
`python src/viz/make_figures.py --config config/review_config.yaml`

---
## Phase 14 - Mandatory Figures
Date/time: 2026-04-23 01:39:37

Completed:
- Generated PRISMA, evidence pyramid, heatmap, mechanism network, evidence ranking, hype map, timeline, and translational matrix where data permitted.

Outputs created:
- results/figures/*.png

Remaining tasks:
- Figure styling should be refined before journal submission.

Risks/limitations:
- Some figures are pilot metadata maps, not final full-text synthesis figures.

Exact next command:
`python src/write_manuscript.py --config config/review_config.yaml`

---
## Phase 15-17 - Manuscript Writing and Journal Positioning
Date/time: 2026-04-23 01:39:37

Completed:
- Drafted main manuscript, short version, supplement, cover letter, reviewer memo, figure legends, and research brief.

Outputs created:
- manuscript/*.md
- docs/research_brief.md

Remaining tasks:
- Full-text verified extraction and final references needed before submission.

Risks/limitations:
- Manuscript is a rigorous pilot draft, not final publication-ready systematic review until full-text verification.

Exact next command:
`pytest tests -q`

---
## Phase 2 - Source Discovery and Search Automation
Date/time: 2026-04-23 01:41:58

Completed:
- Ran 11 query strings across PubMed, Europe PMC, and Crossref.
- Retrieved 1155 raw metadata rows.

Outputs created:
- results/tables/search_runs.csv
- results/tables/raw_records_all.csv

Remaining tasks:
- Full search should be rerun with larger record caps before submission.
- Full-text retrieval remains pending.

Risks/limitations:
- PubMed abstracts are not fetched in this pilot pass; Europe PMC abstracts support screening where available.
- Crossref metadata is abstract-limited.

Exact next command:
`python src/dedup/deduplicate.py --config config/review_config.yaml`

---
## Phase 3 - Deduplication and Record Hygiene
Date/time: 2026-04-23 01:41:58

Completed:
- Standardized DOI/PMID/title keys.
- Reduced 1155 raw rows to 1029 deduplicated records.
- Flagged 85 duplicate key groups.

Outputs created:
- results/tables/master_records_dedup.csv
- results/tables/dedup_log.csv
- results/tables/unresolved_duplicate_report.csv

Remaining tasks:
- Manual review of unresolved duplicate title variants remains pending.

Risks/limitations:
- Records without DOI/PMID depend on normalized title matching and may under/over-deduplicate.

Exact next command:
`python src/screening/screen_records.py --config config/review_config.yaml`

---
## Phase 4 - Autonomous Screening Engine
Date/time: 2026-04-23 01:41:59

Completed:
- Screened 1029 title/abstract records using conservative rules.
- Included 29; uncertain 455; excluded 545.

Outputs created:
- results/tables/title_abstract_screening.csv
- results/tables/full_text_screening.csv

Remaining tasks:
- Human verification of all include/uncertain records remains mandatory.
- Full-text screening is initialized but not complete.

Risks/limitations:
- Abstract gaps reduce confidence for PubMed/Crossref-only records.

Exact next command:
`python src/retrieval/assess_full_text.py --config config/review_config.yaml`

---
## Phase 5 - Full Text Retrieval and Organization
Date/time: 2026-04-23 01:41:59

Completed:
- Assigned retrieval status to 484 include/uncertain records.

Outputs created:
- results/tables/full_text_status.csv

Remaining tasks:
- Actual PDF/full-text download and copyright-compliant review remain pending.

Risks/limitations:
- Some records are metadata-only; evidence completeness is limited.

Exact next command:
`python src/extraction/extract_metadata.py --config config/review_config.yaml`

---
## Phase 6 - Structured Data Extraction
Date/time: 2026-04-23 01:41:59

Completed:
- Created metadata-assisted extraction table for 484 candidate studies.

Outputs created:
- results/tables/extracted_studies_master.csv
- metadata/extraction_dictionary.csv

Remaining tasks:
- Full effect sizes, doses, durations, and bias fields require full-text extraction.

Risks/limitations:
- Metadata extraction is preliminary and explicitly flagged.

Exact next command:
`python src/grading/score_evidence.py --config config/review_config.yaml`

---
## Phase 7-8 - Risk of Bias and Evidence Scoring
Date/time: 2026-04-23 01:41:59

Completed:
- Scored 484 claim-level records and 14 intervention groups.

Outputs created:
- results/tables/risk_of_bias.csv
- results/tables/intervention_evidence_scores.csv
- results/tables/claim_credibility_matrix.csv

Remaining tasks:
- Risk of bias is design-level preliminary; full RoB requires full text.

Risks/limitations:
- Scores are metadata-assisted and conservative.

Exact next command:
`python src/mechanisms/map_mechanisms.py --config config/review_config.yaml`

---
## Phase 9 - Mechanistic Mapping
Date/time: 2026-04-23 01:41:59

Completed:
- Mapped 528 intervention-mechanism edges.

Outputs created:
- results/tables/intervention_mechanism_map.csv
- results/tables/mechanism_evidence_matrix.csv

Remaining tasks:
- Direct/inferred mechanism labels require full-text verification.

Risks/limitations:
- Mechanism mapping from abstracts may miss measured pathways.

Exact next command:
`python src/nlp/topic_hype.py --config config/review_config.yaml`

---
## Phase 10 - NLP/Text Mining Augmentation
Date/time: 2026-04-23 01:41:59

Completed:
- Assigned topic clusters and hype flags to 484 records.

Outputs created:
- results/tables/topic_assignments.csv
- results/tables/hype_topic_summary.csv
- docs/nlp_summary.md

Remaining tasks:
- Embedding-based clustering can be added later.

Risks/limitations:
- Hype detection is lexical and preliminary.

Exact next command:
`python src/meta_analysis/synthesize.py --config config/review_config.yaml`

---
## Phase 11 - Meta-analysis / Quantitative Synthesis
Date/time: 2026-04-23 01:42:00

Completed:
- Created meta-analysis readiness table.
- Deferred pooling because effect sizes require full-text extraction.

Outputs created:
- results/tables/meta_analysis_inputs.csv
- results/tables/meta_analysis_results.csv
- results/tables/structured_vote_counting.csv

Remaining tasks:
- Full-text extraction of effect sizes is required before any pooled estimate.

Risks/limitations:
- Vote counting is descriptive and should not be overinterpreted.

Exact next command:
`python src/viz/make_figures.py --config config/review_config.yaml`

---
## Phase 14 - Mandatory Figures
Date/time: 2026-04-23 01:42:02

Completed:
- Generated PRISMA, evidence pyramid, heatmap, mechanism network, evidence ranking, hype map, timeline, and translational matrix where data permitted.

Outputs created:
- results/figures/*.png

Remaining tasks:
- Figure styling should be refined before journal submission.

Risks/limitations:
- Some figures are pilot metadata maps, not final full-text synthesis figures.

Exact next command:
`python src/write_manuscript.py --config config/review_config.yaml`

---
## Phase 15-17 - Manuscript Writing and Journal Positioning
Date/time: 2026-04-23 01:42:02

Completed:
- Drafted main manuscript, short version, supplement, cover letter, reviewer memo, figure legends, and research brief.

Outputs created:
- manuscript/*.md
- docs/research_brief.md

Remaining tasks:
- Full-text verified extraction and final references needed before submission.

Risks/limitations:
- Manuscript is a rigorous pilot draft, not final publication-ready systematic review until full-text verification.

Exact next command:
`pytest tests -q`

---
## Phase 7-8 - Risk of Bias and Evidence Scoring
Date/time: 2026-04-23 01:42:45

Completed:
- Scored 484 claim-level records and 14 intervention groups.

Outputs created:
- results/tables/risk_of_bias.csv
- results/tables/intervention_evidence_scores.csv
- results/tables/claim_credibility_matrix.csv

Remaining tasks:
- Risk of bias is design-level preliminary; full RoB requires full text.

Risks/limitations:
- Scores are metadata-assisted and conservative.

Exact next command:
`python src/mechanisms/map_mechanisms.py --config config/review_config.yaml`

---
## Phase 9 - Mechanistic Mapping
Date/time: 2026-04-23 01:42:46

Completed:
- Mapped 528 intervention-mechanism edges.

Outputs created:
- results/tables/intervention_mechanism_map.csv
- results/tables/mechanism_evidence_matrix.csv

Remaining tasks:
- Direct/inferred mechanism labels require full-text verification.

Risks/limitations:
- Mechanism mapping from abstracts may miss measured pathways.

Exact next command:
`python src/nlp/topic_hype.py --config config/review_config.yaml`

---
## Phase 10 - NLP/Text Mining Augmentation
Date/time: 2026-04-23 01:42:51

Completed:
- Assigned topic clusters and hype flags to 484 records.

Outputs created:
- results/tables/topic_assignments.csv
- results/tables/hype_topic_summary.csv
- docs/nlp_summary.md

Remaining tasks:
- Embedding-based clustering can be added later.

Risks/limitations:
- Hype detection is lexical and preliminary.

Exact next command:
`python src/meta_analysis/synthesize.py --config config/review_config.yaml`

---
## Phase 11 - Meta-analysis / Quantitative Synthesis
Date/time: 2026-04-23 01:42:52

Completed:
- Created meta-analysis readiness table.
- Deferred pooling because effect sizes require full-text extraction.

Outputs created:
- results/tables/meta_analysis_inputs.csv
- results/tables/meta_analysis_results.csv
- results/tables/structured_vote_counting.csv

Remaining tasks:
- Full-text extraction of effect sizes is required before any pooled estimate.

Risks/limitations:
- Vote counting is descriptive and should not be overinterpreted.

Exact next command:
`python src/viz/make_figures.py --config config/review_config.yaml`

---
## Phase 14 - Mandatory Figures
Date/time: 2026-04-23 01:43:01

Completed:
- Generated PRISMA, evidence pyramid, heatmap, mechanism network, evidence ranking, hype map, timeline, and translational matrix where data permitted.

Outputs created:
- results/figures/*.png

Remaining tasks:
- Figure styling should be refined before journal submission.

Risks/limitations:
- Some figures are pilot metadata maps, not final full-text synthesis figures.

Exact next command:
`python src/write_manuscript.py --config config/review_config.yaml`

---
## Phase 15-17 - Manuscript Writing and Journal Positioning
Date/time: 2026-04-23 01:43:03

Completed:
- Drafted main manuscript, short version, supplement, cover letter, reviewer memo, figure legends, and research brief.

Outputs created:
- manuscript/*.md
- docs/research_brief.md

Remaining tasks:
- Full-text verified extraction and final references needed before submission.

Risks/limitations:
- Manuscript is a rigorous pilot draft, not final publication-ready systematic review until full-text verification.

Exact next command:
`pytest tests -q`

---
## Phase 18-20 - Quality Controls, Tests, and Initial Success Check
Date/time: 2026-04-23 01:43:47

Completed:
- Repaired Python module execution path via Makefile.
- Corrected Europe PMC retrieval by removing unsupported sort parameter.
- Tightened translational readiness classifications to avoid overcalling metformin, rapamycin, microbiome, NAD boosters, supplements, reprogramming, stem-cell, or plasma-based approaches as established anti-ageing interventions.
- Ran unit tests successfully: 5 passed.

Outputs created:
- tests/test_pipeline_units.py
- results/tables/translational_readiness.csv
- logs/audit_trail.md

Remaining tasks:
- Full-text verification, duplicate cohort checking, formal risk-of-bias assessment, and effect-size extraction remain required before journal submission.

Risks/limitations:
- Current manuscript and figures are pilot publication-draft outputs based on metadata-assisted extraction, not final PRISMA-complete systematic review evidence.

Exact next command:
`python -m src.search.run_search --config config/review_config.yaml  # rerun with increased max_records_per_query after updating config`

---
## Phase 15-17 - Manuscript Development Pass
Date/time: 2026-04-23 11:18:56

Completed:
- Expanded manuscript package using live pipeline counts, PRISMA-style flow, screening summaries, retrieval status, evidence rankings, translational readiness, figure legends, supplement, reviewer memo, and submission-readiness checklist.

Outputs created:
- manuscript/manuscript_main.md
- manuscript/manuscript_short.md
- manuscript/supplement.md
- manuscript/cover_letter.md
- manuscript/reviewer_anticipation.md
- manuscript/figure_legends.md
- docs/research_brief.md
- docs/submission_readiness.md

Remaining tasks:
- Full search rerun, human screening adjudication, full-text verification, duplicate cohort checks, final references, formal risk-of-bias assessment, and effect-size extraction remain required before submission.

Risks/limitations:
- Outputs remain a pilot evidence-map manuscript package based on metadata-assisted extraction, not a final PRISMA-complete systematic review.

Exact next command:
`python -m src.search.run_search --config config/review_config.yaml`

---
## Phase 18 - Automated Quality Controls
Date/time: 2026-04-23 11:20:08

Completed:
- Ran automated QC checks for schema completeness, duplicate groups, preprint overclassification, animal/cellular overclaiming, surrogate endpoint drift, metadata-only records, missing effect sizes, and unsupported intervention classifications.
- Flagged 5 medium/high issue categories requiring manual review.

Outputs created:
- results/tables/quality_control_flags.csv
- logs/quality_control_audit.md

Remaining tasks:
- Manual full-text adjudication remains required for all metadata-only and include/uncertain records.

Risks/limitations:
- QC flags are conservative and may include false positives; they are intended to prevent overclaiming before submission.

Exact next command:
`pytest tests -q`

---
## Phase 7-8 - Risk of Bias and Evidence Scoring
Date/time: 2026-04-23 11:21:07

Completed:
- Scored 484 claim-level records and 14 intervention groups.

Outputs created:
- results/tables/risk_of_bias.csv
- results/tables/intervention_evidence_scores.csv
- results/tables/claim_credibility_matrix.csv

Remaining tasks:
- Risk of bias is design-level preliminary; full RoB requires full text.

Risks/limitations:
- Scores are metadata-assisted and conservative.

Exact next command:
`python src/mechanisms/map_mechanisms.py --config config/review_config.yaml`

---
## Phase 14 - Mandatory Figures
Date/time: 2026-04-23 11:21:17

Completed:
- Generated PRISMA, evidence pyramid, heatmap, mechanism network, evidence ranking, hype map, timeline, and translational matrix where data permitted.

Outputs created:
- results/figures/*.png

Remaining tasks:
- Figure styling should be refined before journal submission.

Risks/limitations:
- Some figures are pilot metadata maps, not final full-text synthesis figures.

Exact next command:
`python src/write_manuscript.py --config config/review_config.yaml`

---
## Phase 15-17 - Manuscript Development Pass
Date/time: 2026-04-23 11:21:20

Completed:
- Expanded manuscript package using live pipeline counts, PRISMA-style flow, screening summaries, retrieval status, evidence rankings, translational readiness, figure legends, supplement, reviewer memo, and submission-readiness checklist.

Outputs created:
- manuscript/manuscript_main.md
- manuscript/manuscript_short.md
- manuscript/supplement.md
- manuscript/cover_letter.md
- manuscript/reviewer_anticipation.md
- manuscript/figure_legends.md
- docs/research_brief.md
- docs/submission_readiness.md

Remaining tasks:
- Full search rerun, human screening adjudication, full-text verification, duplicate cohort checks, final references, formal risk-of-bias assessment, and effect-size extraction remain required before submission.

Risks/limitations:
- Outputs remain a pilot evidence-map manuscript package based on metadata-assisted extraction, not a final PRISMA-complete systematic review.

Exact next command:
`python -m src.search.run_search --config config/review_config.yaml`

---
## Phase 18 - Automated Quality Controls
Date/time: 2026-04-23 11:21:21

Completed:
- Ran automated QC checks for schema completeness, duplicate groups, preprint overclassification, animal/cellular overclaiming, surrogate endpoint drift, metadata-only records, missing effect sizes, and unsupported intervention classifications.
- Flagged 4 medium/high issue categories requiring manual review.

Outputs created:
- results/tables/quality_control_flags.csv
- logs/quality_control_audit.md

Remaining tasks:
- Manual full-text adjudication remains required for all metadata-only and include/uncertain records.

Risks/limitations:
- QC flags are conservative and may include false positives; they are intended to prevent overclaiming before submission.

Exact next command:
`pytest tests -q`

---
## Phase 4b-5b - Full-Text Screening Artifact and Human Evidence Prioritization
Date/time: 2026-04-23 11:25:54

Completed:
- Created full-text screening decision artifact for 542 candidate records.
- Prioritized 92 human-evidence records.
- Created first intervention credibility ranking across 14 intervention groups using extracted evidence present in the repo.

Outputs created:
- results/tables/full_text_screening_decisions.csv
- results/tables/human_evidence_priority_queue.csv
- results/tables/intervention_credibility_ranking.csv
- results/supplement/full_text_screening_workbook.md

Remaining tasks:
- Final eligibility remains pending full-text reading; all decisions are provisional triage labels.

Risks/limitations:
- The artifact is intentionally conservative and does not infer effect sizes or definitive eligibility from metadata alone.

Exact next command:
`python -m src.viz.make_figures --config config/review_config.yaml`

---
## Phase 4b-5b - Full-Text Screening Artifact and Human Evidence Prioritization
Date/time: 2026-04-23 11:27:49

Completed:
- Created full-text screening decision artifact for 542 candidate records.
- Prioritized 92 human-evidence records.
- Created first intervention credibility ranking across 14 intervention groups using extracted evidence present in the repo.

Outputs created:
- results/tables/full_text_screening_decisions.csv
- results/tables/human_evidence_priority_queue.csv
- results/tables/intervention_credibility_ranking.csv
- results/supplement/full_text_screening_workbook.md

Remaining tasks:
- Final eligibility remains pending full-text reading; all decisions are provisional triage labels.

Risks/limitations:
- The artifact is intentionally conservative and does not infer effect sizes or definitive eligibility from metadata alone.

Exact next command:
`python -m src.viz.make_figures --config config/review_config.yaml`

---
## Phase 5b-7b - Priority Human Full-Text Verification, RoB, Duplicate Checks, and Effect Extraction
Date/time: 2026-04-23 11:28:54

Completed:
- Attempted open full-text or PubMed/repo abstract verification for the top 40 prioritized human records.
- Created preliminary formal RoB domains for prioritized human records.
- Created candidate effect-size extraction table with manual-verification flags.
- Ran duplicate cohort/publication checks across 484 extracted candidate records.

Outputs created:
- results/tables/full_text_verification_priority_human.csv
- results/tables/effect_size_extraction_priority_human.csv
- results/tables/risk_of_bias_formal_preliminary_human.csv
- results/tables/duplicate_cohort_checks.csv
- data_processed/open_text_cache/*.xml

Remaining tasks:
- Manual full-text reading remains required for final eligibility, final RoB, and final effect sizes.

Risks/limitations:
- Automated extraction is limited to open full text, PubMed abstracts, and repository abstracts; candidate effect snippets are not final quantitative data.

Exact next command:
`python -m src.viz.make_figures --config config/review_config.yaml`

---
## Phase 5b-7b - Priority Human Full-Text Verification, RoB, Duplicate Checks, and Effect Extraction
Date/time: 2026-04-23 11:30:34

Completed:
- Attempted open full-text or PubMed/repo abstract verification for the top 40 prioritized human records.
- Created preliminary formal RoB domains for prioritized human records.
- Created candidate effect-size extraction table with manual-verification flags.
- Ran duplicate cohort/publication checks across 484 extracted candidate records.

Outputs created:
- results/tables/full_text_verification_priority_human.csv
- results/tables/effect_size_extraction_priority_human.csv
- results/tables/risk_of_bias_formal_preliminary_human.csv
- results/tables/duplicate_cohort_checks.csv
- data_processed/open_text_cache/*.xml

Remaining tasks:
- Manual full-text reading remains required for final eligibility, final RoB, and final effect sizes.

Risks/limitations:
- Automated extraction is limited to open full text, PubMed abstracts, and repository abstracts; candidate effect snippets are not final quantitative data.

Exact next command:
`python -m src.viz.make_figures --config config/review_config.yaml`

---
## Phase 4b-5b - Full-Text Screening Artifact and Human Evidence Prioritization
Date/time: 2026-04-23 11:33:55

Completed:
- Created full-text screening decision artifact for 542 candidate records.
- Prioritized 92 human-evidence records.
- Created first intervention credibility ranking across 14 intervention groups using extracted evidence present in the repo.

Outputs created:
- results/tables/full_text_screening_decisions.csv
- results/tables/human_evidence_priority_queue.csv
- results/tables/intervention_credibility_ranking.csv
- results/supplement/full_text_screening_workbook.md

Remaining tasks:
- Final eligibility remains pending full-text reading; all decisions are provisional triage labels.

Risks/limitations:
- The artifact is intentionally conservative and does not infer effect sizes or definitive eligibility from metadata alone.

Exact next command:
`python -m src.viz.make_figures --config config/review_config.yaml`

---
## Phase 5b-7b - Priority Human Full-Text Verification, RoB, Duplicate Checks, and Effect Extraction
Date/time: 2026-04-23 11:35:05

Completed:
- Attempted open full-text or PubMed/repo abstract verification for the top 40 prioritized human records.
- Created preliminary formal RoB domains for prioritized human records.
- Created candidate effect-size extraction table with manual-verification flags.
- Ran duplicate cohort/publication checks across 484 extracted candidate records.

Outputs created:
- results/tables/full_text_verification_priority_human.csv
- results/tables/effect_size_extraction_priority_human.csv
- results/tables/risk_of_bias_formal_preliminary_human.csv
- results/tables/duplicate_cohort_checks.csv
- data_processed/open_text_cache/*.xml

Remaining tasks:
- Manual full-text reading remains required for final eligibility, final RoB, and final effect sizes.

Risks/limitations:
- Automated extraction is limited to open full text, PubMed abstracts, and repository abstracts; candidate effect snippets are not final quantitative data.

Exact next command:
`python -m src.viz.make_figures --config config/review_config.yaml`

---
## Phase 14 - Mandatory Figures
Date/time: 2026-04-23 11:35:23

Completed:
- Generated PRISMA, evidence pyramid, heatmap, mechanism network, evidence ranking, hype map, timeline, and translational matrix where data permitted.

Outputs created:
- results/figures/*.png

Remaining tasks:
- Figure styling should be refined before journal submission.

Risks/limitations:
- Some figures are pilot metadata maps, not final full-text synthesis figures.

Exact next command:
`python src/write_manuscript.py --config config/review_config.yaml`

---
## Phase 15-17 - Manuscript Development Pass
Date/time: 2026-04-23 11:35:26

Completed:
- Expanded manuscript package using live pipeline counts, PRISMA-style flow, screening summaries, retrieval status, evidence rankings, translational readiness, figure legends, supplement, reviewer memo, and submission-readiness checklist.

Outputs created:
- manuscript/manuscript_main.md
- manuscript/manuscript_short.md
- manuscript/supplement.md
- manuscript/cover_letter.md
- manuscript/reviewer_anticipation.md
- manuscript/figure_legends.md
- docs/research_brief.md
- docs/submission_readiness.md

Remaining tasks:
- Full search rerun, human screening adjudication, full-text verification, duplicate cohort checks, final references, formal risk-of-bias assessment, and effect-size extraction remain required before submission.

Risks/limitations:
- Outputs remain a pilot evidence-map manuscript package based on metadata-assisted extraction, not a final PRISMA-complete systematic review.

Exact next command:
`python -m src.search.run_search --config config/review_config.yaml`

---
## Phase 18 - Automated Quality Controls
Date/time: 2026-04-23 11:35:28

Completed:
- Ran automated QC checks for schema completeness, duplicate groups, preprint overclassification, animal/cellular overclaiming, surrogate endpoint drift, metadata-only records, missing effect sizes, and unsupported intervention classifications.
- Flagged 4 medium/high issue categories requiring manual review.

Outputs created:
- results/tables/quality_control_flags.csv
- logs/quality_control_audit.md

Remaining tasks:
- Manual full-text adjudication remains required for all metadata-only and include/uncertain records.

Risks/limitations:
- QC flags are conservative and may include false positives; they are intended to prevent overclaiming before submission.

Exact next command:
`pytest tests -q`

---
## Phase 4b-5b - Full-Text Screening Artifact and Human Evidence Prioritization
Date/time: 2026-04-23 11:36:01

Completed:
- Created full-text screening decision artifact for 484 candidate records.
- Prioritized 90 human-evidence records.
- Created first intervention credibility ranking across 14 intervention groups using extracted evidence present in the repo.

Outputs created:
- results/tables/full_text_screening_decisions.csv
- results/tables/human_evidence_priority_queue.csv
- results/tables/intervention_credibility_ranking.csv
- results/supplement/full_text_screening_workbook.md

Remaining tasks:
- Final eligibility remains pending full-text reading; all decisions are provisional triage labels.

Risks/limitations:
- The artifact is intentionally conservative and does not infer effect sizes or definitive eligibility from metadata alone.

Exact next command:
`python -m src.viz.make_figures --config config/review_config.yaml`

---
## Phase 5b-7b - Priority Human Full-Text Verification, RoB, Duplicate Checks, and Effect Extraction
Date/time: 2026-04-23 11:37:11

Completed:
- Attempted open full-text or PubMed/repo abstract verification for the top 40 prioritized human records.
- Created preliminary formal RoB domains for prioritized human records.
- Created candidate effect-size extraction table with manual-verification flags.
- Ran duplicate cohort/publication checks across 484 extracted candidate records.

Outputs created:
- results/tables/full_text_verification_priority_human.csv
- results/tables/effect_size_extraction_priority_human.csv
- results/tables/risk_of_bias_formal_preliminary_human.csv
- results/tables/duplicate_cohort_checks.csv
- data_processed/open_text_cache/*.xml

Remaining tasks:
- Manual full-text reading remains required for final eligibility, final RoB, and final effect sizes.

Risks/limitations:
- Automated extraction is limited to open full text, PubMed abstracts, and repository abstracts; candidate effect snippets are not final quantitative data.

Exact next command:
`python -m src.viz.make_figures --config config/review_config.yaml`

---
## Phase 14 - Mandatory Figures
Date/time: 2026-04-23 11:37:30

Completed:
- Generated PRISMA, evidence pyramid, heatmap, mechanism network, evidence ranking, hype map, timeline, and translational matrix where data permitted.

Outputs created:
- results/figures/*.png

Remaining tasks:
- Figure styling should be refined before journal submission.

Risks/limitations:
- Some figures are pilot metadata maps, not final full-text synthesis figures.

Exact next command:
`python src/write_manuscript.py --config config/review_config.yaml`

---
## Phase 15-17 - Manuscript Development Pass
Date/time: 2026-04-23 11:37:33

Completed:
- Expanded manuscript package using live pipeline counts, PRISMA-style flow, screening summaries, retrieval status, evidence rankings, translational readiness, figure legends, supplement, reviewer memo, and submission-readiness checklist.

Outputs created:
- manuscript/manuscript_main.md
- manuscript/manuscript_short.md
- manuscript/supplement.md
- manuscript/cover_letter.md
- manuscript/reviewer_anticipation.md
- manuscript/figure_legends.md
- docs/research_brief.md
- docs/submission_readiness.md

Remaining tasks:
- Full search rerun, human screening adjudication, full-text verification, duplicate cohort checks, final references, formal risk-of-bias assessment, and effect-size extraction remain required before submission.

Risks/limitations:
- Outputs remain a pilot evidence-map manuscript package based on metadata-assisted extraction, not a final PRISMA-complete systematic review.

Exact next command:
`python -m src.search.run_search --config config/review_config.yaml`

---
## Phase 18 - Automated Quality Controls
Date/time: 2026-04-23 11:37:34

Completed:
- Ran automated QC checks for schema completeness, duplicate groups, preprint overclassification, animal/cellular overclaiming, surrogate endpoint drift, metadata-only records, missing effect sizes, and unsupported intervention classifications.
- Flagged 4 medium/high issue categories requiring manual review.

Outputs created:
- results/tables/quality_control_flags.csv
- logs/quality_control_audit.md

Remaining tasks:
- Manual full-text adjudication remains required for all metadata-only and include/uncertain records.

Risks/limitations:
- QC flags are conservative and may include false positives; they are intended to prevent overclaiming before submission.

Exact next command:
`pytest tests -q`

---
## Phase 4b-5b - Full-Text Screening Artifact and Human Evidence Prioritization
Date/time: 2026-04-23 11:51:53

Completed:
- Created full-text screening decision artifact for 484 candidate records.
- Prioritized 90 human-evidence records.
- Created first intervention credibility ranking across 14 intervention groups using extracted evidence present in the repo.

Outputs created:
- results/tables/full_text_screening_decisions.csv
- results/tables/human_evidence_priority_queue.csv
- results/tables/intervention_credibility_ranking.csv
- results/supplement/full_text_screening_workbook.md

Remaining tasks:
- Final eligibility remains pending full-text reading; all decisions are provisional triage labels.

Risks/limitations:
- The artifact is intentionally conservative and does not infer effect sizes or definitive eligibility from metadata alone.

Exact next command:
`python -m src.viz.make_figures --config config/review_config.yaml`

---
## Phase 5b-7b - Priority Human Full-Text Verification, RoB, Duplicate Checks, and Effect Extraction
Date/time: 2026-04-23 11:53:02

Completed:
- Attempted open full-text or PubMed/repo abstract verification for the top 40 prioritized human records.
- Created preliminary formal RoB domains for prioritized human records.
- Created candidate effect-size extraction table with manual-verification flags.
- Ran duplicate cohort/publication checks across 484 extracted candidate records.

Outputs created:
- results/tables/full_text_verification_priority_human.csv
- results/tables/effect_size_extraction_priority_human.csv
- results/tables/risk_of_bias_formal_preliminary_human.csv
- results/tables/duplicate_cohort_checks.csv
- data_processed/open_text_cache/*.xml

Remaining tasks:
- Manual full-text reading remains required for final eligibility, final RoB, and final effect sizes.

Risks/limitations:
- Automated extraction is limited to open full text, PubMed abstracts, and repository abstracts; candidate effect snippets are not final quantitative data.

Exact next command:
`python -m src.viz.make_figures --config config/review_config.yaml`

---
## Phase 14 - Mandatory Figures
Date/time: 2026-04-23 11:53:20

Completed:
- Generated PRISMA, evidence pyramid, heatmap, mechanism network, evidence ranking, hype map, timeline, and translational matrix where data permitted.

Outputs created:
- results/figures/*.png

Remaining tasks:
- Figure styling should be refined before journal submission.

Risks/limitations:
- Some figures are pilot metadata maps, not final full-text synthesis figures.

Exact next command:
`python src/write_manuscript.py --config config/review_config.yaml`

---
## Phase 15-17 - Manuscript Development Pass
Date/time: 2026-04-23 11:53:23

Completed:
- Expanded manuscript package using live pipeline counts, PRISMA-style flow, screening summaries, retrieval status, evidence rankings, translational readiness, figure legends, supplement, reviewer memo, and submission-readiness checklist.

Outputs created:
- manuscript/manuscript_main.md
- manuscript/manuscript_short.md
- manuscript/supplement.md
- manuscript/cover_letter.md
- manuscript/reviewer_anticipation.md
- manuscript/figure_legends.md
- docs/research_brief.md
- docs/submission_readiness.md

Remaining tasks:
- Full search rerun, human screening adjudication, full-text verification, duplicate cohort checks, final references, formal risk-of-bias assessment, and effect-size extraction remain required before submission.

Risks/limitations:
- Outputs remain a pilot evidence-map manuscript package based on metadata-assisted extraction, not a final PRISMA-complete systematic review.

Exact next command:
`python -m src.search.run_search --config config/review_config.yaml`

---
## Phase 18 - Automated Quality Controls
Date/time: 2026-04-23 11:53:25

Completed:
- Ran automated QC checks for schema completeness, duplicate groups, preprint overclassification, animal/cellular overclaiming, surrogate endpoint drift, metadata-only records, missing effect sizes, and unsupported intervention classifications.
- Flagged 4 medium/high issue categories requiring manual review.

Outputs created:
- results/tables/quality_control_flags.csv
- logs/quality_control_audit.md

Remaining tasks:
- Manual full-text adjudication remains required for all metadata-only and include/uncertain records.

Risks/limitations:
- QC flags are conservative and may include false positives; they are intended to prevent overclaiming before submission.

Exact next command:
`pytest tests -q`

---
## Phase 21 - MJDRDYPU Publication Asset Package and Double Peer Review
Date/time: 2026-04-23 11:53:28

Completed:
- Prepared MJDRDYPU-style DOCX submission assets.
- Created blinded manuscript, title page, cover letter, declarations, two internal peer reviews, comprehensive audit, checklist, reference metadata, copied source figures and tables.

Outputs created:
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23/*.docx
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23/figures/*.png
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23/tables/*.csv

Remaining tasks:
- Final manual scientific sign-off and portal-specific form checks remain required before upload.

Risks/limitations:
- Journal instructions were inferred from accessible LWW/Medknow-style guidance and MJDRDYPU article patterns because a dedicated current instruction PDF was not directly accessible.

Exact next command:
`pytest tests -q`

---
## Phase 21 - MJDRDYPU Publication Asset Package and Double Peer Review
Date/time: 2026-04-23 11:54:26

Completed:
- Prepared MJDRDYPU-style DOCX submission assets.
- Created blinded manuscript, title page, cover letter, declarations, two internal peer reviews, comprehensive audit, checklist, reference metadata, copied source figures and tables.

Outputs created:
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23/*.docx
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23/figures/*.png
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23/tables/*.csv

Remaining tasks:
- Complete author details, affiliations, guarantor, and final manual scientific sign-off remain required before portal upload.

Risks/limitations:
- Journal instructions were inferred from accessible LWW/Medknow-style guidance and MJDRDYPU article patterns because a dedicated current instruction PDF was not directly accessible.

Exact next command:
`pytest tests -q`

---
## Phase 21 - MJDRDYPU Publication Asset Package and Double Peer Review
Date/time: 2026-04-23 12:03:59

Completed:
- Prepared MJDRDYPU-style DOCX submission assets.
- Created blinded manuscript, title page, cover letter, declarations, two internal peer reviews, comprehensive audit, checklist, reference metadata, copied source figures and tables.

Outputs created:
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23/*.docx
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23/figures/*.png
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23/tables/*.csv

Remaining tasks:
- Complete author details, affiliations, guarantor, and final manual scientific sign-off remain required before portal upload.

Risks/limitations:
- Journal instructions were inferred from accessible LWW/Medknow-style guidance and MJDRDYPU article patterns because a dedicated current instruction PDF was not directly accessible.

Exact next command:
`pytest tests -q`

---
## Phase 21 - MJDRDYPU Publication Asset Package and Double Peer Review
Date/time: 2026-04-23 12:25:26

Completed:
- Prepared MJDRDYPU-style DOCX submission assets.
- Created blinded manuscript, title page, cover letter, declarations, two internal peer reviews, comprehensive audit, checklist, reference metadata, copied source figures and tables.

Outputs created:
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final/*.docx
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final/figures/*.png
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final/tables/*.csv

Remaining tasks:
- Final manual scientific sign-off and portal-specific form checks remain required before upload.

Risks/limitations:
- Journal instructions were inferred from accessible LWW/Medknow-style guidance and MJDRDYPU article patterns because a dedicated current instruction PDF was not directly accessible.

Exact next command:
`pytest tests -q`

---
## Phase 21 - MJDRDYPU Publication Asset Package and Double Peer Review
Date/time: 2026-04-23 12:36:56

Completed:
- Prepared MJDRDYPU-style DOCX submission assets.
- Created blinded manuscript, title page, cover letter, declarations, two internal peer reviews, comprehensive audit, checklist, reference metadata, copied source figures and tables.

Outputs created:
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final/*.docx
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final/figures/*.png
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final/tables/*.csv

Remaining tasks:
- Final manual scientific sign-off and portal-specific form checks remain required before upload.

Risks/limitations:
- Journal instructions were inferred from accessible LWW/Medknow-style guidance and MJDRDYPU article patterns because a dedicated current instruction PDF was not directly accessible.

Exact next command:
`pytest tests -q`

---
## Phase 21 - MJDRDYPU Publication Asset Package and Double Peer Review
Date/time: 2026-04-23 12:39:01

Completed:
- Prepared MJDRDYPU-style DOCX submission assets.
- Created blinded manuscript, title page, cover letter, declarations, two internal peer reviews, comprehensive audit, checklist, reference metadata, copied source figures and tables.

Outputs created:
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final/*.docx
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final/figures/*.png
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final/tables/*.csv

Remaining tasks:
- Final manual scientific sign-off and portal-specific form checks remain required before upload.

Risks/limitations:
- Journal instructions were inferred from accessible LWW/Medknow-style guidance and MJDRDYPU article patterns because a dedicated current instruction PDF was not directly accessible.

Exact next command:
`pytest tests -q`

---
## Phase 21 - MJDRDYPU Publication Asset Package and Double Peer Review
Date/time: 2026-04-23 12:40:51

Completed:
- Prepared MJDRDYPU-style DOCX submission assets.
- Created blinded manuscript, title page, cover letter, declarations, two internal peer reviews, comprehensive audit, checklist, reference metadata, copied source figures and tables.

Outputs created:
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final/*.docx
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final/figures/*.png
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final/tables/*.csv

Remaining tasks:
- Final manual scientific sign-off and portal-specific form checks remain required before upload.

Risks/limitations:
- Journal instructions were inferred from accessible LWW/Medknow-style guidance and MJDRDYPU article patterns because a dedicated current instruction PDF was not directly accessible.

Exact next command:
`pytest tests -q`

---
## Phase 21 - MJDRDYPU Publication Asset Package and Double Peer Review
Date/time: 2026-04-23 13:05:48

Completed:
- Prepared MJDRDYPU-style DOCX submission assets.
- Created blinded manuscript, title page, cover letter, declarations, two internal peer reviews, comprehensive audit, checklist, reference metadata, copied source figures and tables.

Outputs created:
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final_v2/*.docx
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final_v2/figures/*.png
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final_v2/tables/*.csv

Remaining tasks:
- Final manual scientific sign-off and portal-specific form checks remain required before upload.

Risks/limitations:
- Journal instructions were inferred from accessible LWW/Medknow-style guidance and MJDRDYPU article patterns because a dedicated current instruction PDF was not directly accessible.

Exact next command:
`pytest tests -q`

---
## Phase 21 - MJDRDYPU Publication Asset Package and Double Peer Review
Date/time: 2026-04-23 13:11:31

Completed:
- Prepared MJDRDYPU-style DOCX submission assets.
- Created blinded manuscript, title page, cover letter, declarations, two internal peer reviews, comprehensive audit, checklist, reference metadata, copied source figures and tables.

Outputs created:
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final_v2/*.docx
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final_v2/figures/*.png
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final_v2/tables/*.csv

Remaining tasks:
- Final manual scientific sign-off and portal-specific form checks remain required before upload.

Risks/limitations:
- Journal instructions were inferred from accessible LWW/Medknow-style guidance and MJDRDYPU article patterns because a dedicated current instruction PDF was not directly accessible.

Exact next command:
`pytest tests -q`

---
## Phase 21 - MJDRDYPU Publication Asset Package and Double Peer Review
Date/time: 2026-04-23 13:15:10

Completed:
- Prepared MJDRDYPU-style DOCX submission assets.
- Created blinded manuscript, title page, cover letter, declarations, two internal peer reviews, comprehensive audit, checklist, reference metadata, copied source figures and tables.

Outputs created:
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final_v2/*.docx
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final_v2/figures/*.png
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final_v2/tables/*.csv

Remaining tasks:
- Final manual scientific sign-off and portal-specific form checks remain required before upload.

Risks/limitations:
- Journal instructions were inferred from accessible LWW/Medknow-style guidance and MJDRDYPU article patterns because a dedicated current instruction PDF was not directly accessible.

Exact next command:
`pytest tests -q`

---
## Phase 21 - MJDRDYPU Publication Asset Package and Double Peer Review
Date/time: 2026-04-23 13:16:59

Completed:
- Prepared MJDRDYPU-style DOCX submission assets.
- Created blinded manuscript, title page, cover letter, declarations, two internal peer reviews, comprehensive audit, checklist, reference metadata, copied source figures and tables.

Outputs created:
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final_v2/*.docx
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final_v2/figures/*.png
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final_v2/tables/*.csv

Remaining tasks:
- Final manual scientific sign-off and portal-specific form checks remain required before upload.

Risks/limitations:
- Journal instructions were inferred from accessible LWW/Medknow-style guidance and MJDRDYPU article patterns because a dedicated current instruction PDF was not directly accessible.

Exact next command:
`pytest tests -q`

---
## Phase 21 - MJDRDYPU Publication Asset Package and Double Peer Review
Date/time: 2026-04-23 13:18:19

Completed:
- Prepared MJDRDYPU-style DOCX submission assets.
- Created blinded manuscript, title page, cover letter, declarations, two internal peer reviews, comprehensive audit, checklist, reference metadata, copied source figures and tables.

Outputs created:
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final_v2/*.docx
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final_v2/figures/*.png
- submission_assets/MJDRDYPU_AntiAgeing_2026-04-23_final_v2/tables/*.csv

Remaining tasks:
- Final manual scientific sign-off and portal-specific form checks remain required before upload.

Risks/limitations:
- Journal instructions were inferred from accessible LWW/Medknow-style guidance and MJDRDYPU article patterns because a dedicated current instruction PDF was not directly accessible.

Exact next command:
`pytest tests -q`

---
## Phase 22 - Meta-analysis Add-on Scaffolding
Date/time: 2026-04-23 15:15:41

Completed:
- Created a separate quantitative meta-analysis add-on workflow.
- Built source manifest, extraction queue, endpoint priority table, figure digitization queue, and meta-analysis dataset template.
- Restricted add-on scope to human empirical studies and endpoint-specific pooling.

Outputs created:
- results/meta_addon/tables/study_source_manifest.csv
- results/meta_addon/tables/meta_extraction_queue.csv
- results/meta_addon/tables/endpoint_priority.csv
- results/meta_addon/tables/figure_digitization_queue.csv
- results/meta_addon/tables/meta_analysis_readiness_report.csv
- results/meta_addon/tables/meta_dataset_template.csv
- results/meta_addon/tables/tool_registry.csv
- docs/meta_addon/workflow.md
- manuscript/meta_addon/manuscript_meta_addon.md

Remaining tasks:
- Populate arm-level or model-level quantitative fields for priority endpoints.
- Adjudicate duplicate cohorts before pooling.
- Add actual effect-size computation and pooled models after extraction.

Risks/limitations:
- Current outputs identify extractable studies and source routes but do not infer missing statistics.
- Figure digitization is a rescue path, not a first-line source when tables or supplements exist.

Exact next command:
`python -m src.meta_addon.build_addon --config config/meta_addon_config.yaml`

---
## Phase 23 - Meta-analysis Add-on Manual Numeric Extraction Seed
Date/time: 2026-04-23 15:35:46

Completed:
- Seeded the quantitative add-on dataset with exact arm-level end-of-intervention values from the exergame RFA trial.
- Added a sensitivity-only SHARE-FI row from the multidomain lifestyle trial with explicit caveat that SD values were assumed in the source power paragraph.
- Computed Hedges g and standard errors for extracted rows.

Outputs created:
- results/meta_addon/tables/meta_dataset_working.csv
- docs/meta_addon/manual_extraction_notes.md

Remaining tasks:
- Continue extracting exact arm-level or model-level values from additional local XML and open PDFs.
- Keep only exact observed values in the primary pooling set; retain assumed-value rows for sensitivity analyses only.

Risks/limitations:
- Current working dataset is still too sparse for a stable pooled meta-analysis across studies.
- Outcome harmonization remains the main constraint.

Exact next command:
`python -m src.meta_addon.seed_numeric_extractions --config config/meta_addon_config.yaml`

---
## Phase 23 - Meta-analysis Add-on Manual Numeric Extraction Seed
Date/time: 2026-04-23 15:36:50

Completed:
- Seeded the quantitative add-on dataset with exact arm-level end-of-intervention values from the exergame RFA trial.
- Added a sensitivity-only SHARE-FI row from the multidomain lifestyle trial with explicit caveat that SD values were assumed in the source power paragraph.
- Computed Hedges g and standard errors for extracted rows.

Outputs created:
- results/meta_addon/tables/meta_dataset_working.csv
- docs/meta_addon/manual_extraction_notes.md

Remaining tasks:
- Continue extracting exact arm-level or model-level values from additional local XML and open PDFs.
- Keep only exact observed values in the primary pooling set; retain assumed-value rows for sensitivity analyses only.

Risks/limitations:
- Current working dataset is still too sparse for a stable pooled meta-analysis across studies.
- Outcome harmonization remains the main constraint.

Exact next command:
`python -m src.meta_addon.seed_numeric_extractions --config config/meta_addon_config.yaml`

---
## Phase 23 - Meta-analysis Add-on Manual Numeric Extraction Seed
Date/time: 2026-04-23 15:37:41

Completed:
- Seeded the quantitative add-on dataset with exact arm-level end-of-intervention values from the exergame RFA trial.
- Added a sensitivity-only SHARE-FI row from the multidomain lifestyle trial with explicit caveat that SD values were assumed in the source power paragraph.
- Added model-level quantitative rows from the multiple-sclerosis frailty pilot trial and the PROMOTe trial using reported confidence intervals.
- Computed Hedges g and standard errors or generic inverse-variance standard errors for extracted rows.

Outputs created:
- results/meta_addon/tables/meta_dataset_working.csv
- docs/meta_addon/manual_extraction_notes.md

Remaining tasks:
- Continue extracting exact arm-level or model-level values from additional local XML and open PDFs.
- Keep only exact observed values in the primary pooling set; retain assumed-value rows for sensitivity analyses only.

Risks/limitations:
- Current working dataset is still too sparse for a stable pooled meta-analysis across studies.
- Outcome harmonization remains the main constraint.

Exact next command:
`python -m src.meta_addon.seed_numeric_extractions --config config/meta_addon_config.yaml`

---
## Phase 23 - Meta-analysis Add-on Manual Numeric Extraction Seed
Date/time: 2026-04-23 15:38:12

Completed:
- Seeded the quantitative add-on dataset with exact arm-level end-of-intervention values from the exergame RFA trial.
- Added a sensitivity-only SHARE-FI row from the multidomain lifestyle trial with explicit caveat that SD values were assumed in the source power paragraph.
- Added model-level quantitative rows from the multiple-sclerosis frailty pilot trial and the PROMOTe trial using reported confidence intervals.
- Computed Hedges g and standard errors or generic inverse-variance standard errors for extracted rows.

Outputs created:
- results/meta_addon/tables/meta_dataset_working.csv
- results/meta_addon/tables/meta_dataset_primary_pooling.csv
- docs/meta_addon/manual_extraction_notes.md

Remaining tasks:
- Continue extracting exact arm-level or model-level values from additional local XML and open PDFs.
- Keep only exact observed values in the primary pooling set; retain assumed-value rows for sensitivity analyses only.

Risks/limitations:
- Current working dataset is still too sparse for a stable pooled meta-analysis across studies.
- Outcome harmonization remains the main constraint.

Exact next command:
`python -m src.meta_addon.seed_numeric_extractions --config config/meta_addon_config.yaml`

---
## Phase 23 - Meta-analysis Add-on Manual Numeric Extraction Seed
Date/time: 2026-04-23 15:38:33

Completed:
- Seeded the quantitative add-on dataset with exact arm-level end-of-intervention values from the exergame RFA trial.
- Added a sensitivity-only SHARE-FI row from the multidomain lifestyle trial with explicit caveat that SD values were assumed in the source power paragraph.
- Added model-level quantitative rows from the multiple-sclerosis frailty pilot trial and the PROMOTe trial using reported confidence intervals.
- Computed Hedges g and standard errors or generic inverse-variance standard errors for extracted rows.

Outputs created:
- results/meta_addon/tables/meta_dataset_working.csv
- results/meta_addon/tables/meta_dataset_primary_pooling.csv
- docs/meta_addon/manual_extraction_notes.md

Remaining tasks:
- Continue extracting exact arm-level or model-level values from additional local XML and open PDFs.
- Keep only exact observed values in the primary pooling set; retain assumed-value rows for sensitivity analyses only.

Risks/limitations:
- Current working dataset is still too sparse for a stable pooled meta-analysis across studies.
- Outcome harmonization remains the main constraint.

Exact next command:
`python -m src.meta_addon.seed_numeric_extractions --config config/meta_addon_config.yaml`

---
## Phase 23 - Meta-analysis Add-on Manual Numeric Extraction Seed
Date/time: 2026-04-23 15:40:34

Completed:
- Seeded the quantitative add-on dataset with exact arm-level end-of-intervention values from the exergame RFA trial.
- Added a sensitivity-only SHARE-FI row from the multidomain lifestyle trial with explicit caveat that SD values were assumed in the source power paragraph.
- Added model-level quantitative rows from the multiple-sclerosis frailty pilot trial and the PROMOTe trial using reported confidence intervals.
- Computed Hedges g and standard errors or generic inverse-variance standard errors for extracted rows.

Outputs created:
- results/meta_addon/tables/meta_dataset_working.csv
- results/meta_addon/tables/meta_dataset_primary_pooling.csv
- docs/meta_addon/manual_extraction_notes.md

Remaining tasks:
- Continue extracting exact arm-level or model-level values from additional local XML and open PDFs.
- Keep only exact observed values in the primary pooling set; retain assumed-value rows for sensitivity analyses only.

Risks/limitations:
- Current working dataset is still too sparse for a stable pooled meta-analysis across studies.
- Outcome harmonization remains the main constraint.

Exact next command:
`python -m src.meta_addon.seed_numeric_extractions --config config/meta_addon_config.yaml`

---
## Phase 23 - Meta-analysis Add-on Manual Numeric Extraction Seed
Date/time: 2026-04-23 15:41:01

Completed:
- Seeded the quantitative add-on dataset with exact arm-level end-of-intervention values from the exergame RFA trial.
- Added a sensitivity-only SHARE-FI row from the multidomain lifestyle trial with explicit caveat that SD values were assumed in the source power paragraph.
- Added model-level quantitative rows from the multiple-sclerosis frailty pilot trial and the PROMOTe trial using reported confidence intervals.
- Computed Hedges g and standard errors or generic inverse-variance standard errors for extracted rows.

Outputs created:
- results/meta_addon/tables/meta_dataset_working.csv
- results/meta_addon/tables/meta_dataset_primary_pooling.csv
- docs/meta_addon/manual_extraction_notes.md

Remaining tasks:
- Continue extracting exact arm-level or model-level values from additional local XML and open PDFs.
- Keep only exact observed values in the primary pooling set; retain assumed-value rows for sensitivity analyses only.

Risks/limitations:
- Current working dataset is still too sparse for a stable pooled meta-analysis across studies.
- Outcome harmonization remains the main constraint.

Exact next command:
`python -m src.meta_addon.seed_numeric_extractions --config config/meta_addon_config.yaml`

---
## Phase 23 - Meta-analysis Add-on Manual Numeric Extraction Seed
Date/time: 2026-04-23 15:45:55

Completed:
- Seeded the quantitative add-on dataset with exact arm-level end-of-intervention values from the exergame RFA trial.
- Added a sensitivity-only SHARE-FI row from the multidomain lifestyle trial with explicit caveat that SD values were assumed in the source power paragraph.
- Added model-level quantitative rows from the multiple-sclerosis frailty pilot trial and the PROMOTe trial using reported confidence intervals.
- Added full-text standardized DNAm-aging treatment effects from the CALERIE trial.
- Computed Hedges g and standard errors or generic inverse-variance standard errors for extracted rows, and generated a harmonization audit grouped by endpoint family and metric.

Outputs created:
- results/meta_addon/tables/meta_dataset_working.csv
- results/meta_addon/tables/meta_dataset_primary_pooling.csv
- results/meta_addon/tables/meta_pooling_harmonization_audit.csv
- docs/meta_addon/manual_extraction_notes.md

Remaining tasks:
- Continue extracting exact arm-level or model-level values from additional local XML and open PDFs.
- Keep only exact observed values in the primary pooling set; retain assumed-value rows for sensitivity analyses only.

Risks/limitations:
- Current working dataset still has too few independent studies for a stable pooled estimate in most endpoint families.
- Outcome harmonization remains the main constraint even after adding CALERIE's standardized DNAm rows.

Exact next command:
`python -m src.meta_addon.seed_numeric_extractions --config config/meta_addon_config.yaml`

---
## Phase 23 - Meta-analysis Add-on Manual Numeric Extraction Seed
Date/time: 2026-04-23 15:46:52

Completed:
- Seeded the quantitative add-on dataset with exact arm-level end-of-intervention values from the exergame RFA trial.
- Added a sensitivity-only SHARE-FI row from the multidomain lifestyle trial with explicit caveat that SD values were assumed in the source power paragraph.
- Added model-level quantitative rows from the multiple-sclerosis frailty pilot trial and the PROMOTe trial using reported confidence intervals.
- Added full-text standardized DNAm-aging treatment effects from the CALERIE trial.
- Computed Hedges g and standard errors or generic inverse-variance standard errors for extracted rows, and generated a harmonization audit grouped by endpoint family and metric.

Outputs created:
- results/meta_addon/tables/meta_dataset_working.csv
- results/meta_addon/tables/meta_dataset_primary_pooling.csv
- results/meta_addon/tables/meta_pooling_harmonization_audit.csv
- docs/meta_addon/manual_extraction_notes.md

Remaining tasks:
- Continue extracting exact arm-level or model-level values from additional local XML and open PDFs.
- Keep only exact observed values in the primary pooling set; retain assumed-value rows for sensitivity analyses only.

Risks/limitations:
- Current working dataset still has too few independent studies for a stable pooled estimate in most endpoint families.
- Outcome harmonization remains the main constraint even after adding CALERIE's standardized DNAm rows.

Exact next command:
`python -m src.meta_addon.seed_numeric_extractions --config config/meta_addon_config.yaml`

---
## Phase 24 - Same-outcome pooled estimates
Date/time: 2026-04-23 15:50:54

Completed:
- Selected one primary non-TOT row per study and outcome from the standardized-effect subset.
- Generated a same-outcome pooling input table.
- Computed fixed-effect and random-effects pooled estimates for any outcome with at least two independent studies.

Outputs created:
- results/meta_addon/tables/meta_same_outcome_pooling_inputs.csv
- results/meta_addon/tables/meta_same_outcome_pooling_results.csv

Remaining tasks:
- Continue extracting additional same-outcome standardized DNAm rows to strengthen biological-age pooling beyond DunedinPACE.
- Add manuscript text for the pooled DunedinPACE estimate only after manual review of compatibility assumptions.

Risks/limitations:
- Current same-outcome pooling is limited by the small number of studies and should be treated as exploratory.
- Outcome-version compatibility still requires judgment, especially for PhenoAge variants.

Exact next command:
`python -m src.meta_addon.pool_same_outcome --config config/meta_addon_config.yaml`

---
## Phase 23 - Meta-analysis Add-on Manual Numeric Extraction Seed
Date/time: 2026-04-23 15:50:55

Completed:
- Seeded the quantitative add-on dataset with exact arm-level end-of-intervention values from the exergame RFA trial.
- Added a sensitivity-only SHARE-FI row from the multidomain lifestyle trial with explicit caveat that SD values were assumed in the source power paragraph.
- Added model-level quantitative rows from the multiple-sclerosis frailty pilot trial and the PROMOTe trial using reported confidence intervals.
- Added full-text standardized DNAm-aging treatment effects from the CALERIE and DO-HEALTH trials.
- Computed Hedges g and standard errors or generic inverse-variance standard errors for extracted rows, and generated both a harmonization audit and a multi-study pool-candidate table.

Outputs created:
- results/meta_addon/tables/meta_dataset_working.csv
- results/meta_addon/tables/meta_dataset_primary_pooling.csv
- results/meta_addon/tables/meta_pooling_harmonization_audit.csv
- results/meta_addon/tables/meta_multi_study_pool_candidates.csv
- docs/meta_addon/manual_extraction_notes.md

Remaining tasks:
- Continue extracting exact arm-level or model-level values from additional local XML and open PDFs.
- Keep only exact observed values in the primary pooling set; retain assumed-value rows for sensitivity analyses only.

Risks/limitations:
- Current working dataset still has too few independent studies for a stable pooled estimate in most endpoint families.
- Outcome harmonization remains the main constraint, although DunedinPACE now has at least two independent studies for exploratory pooling.

Exact next command:
`python -m src.meta_addon.seed_numeric_extractions --config config/meta_addon_config.yaml`

---
## Phase 23 - Meta-analysis Add-on Manual Numeric Extraction Seed
Date/time: 2026-04-23 15:51:30

Completed:
- Seeded the quantitative add-on dataset with exact arm-level end-of-intervention values from the exergame RFA trial.
- Added a sensitivity-only SHARE-FI row from the multidomain lifestyle trial with explicit caveat that SD values were assumed in the source power paragraph.
- Added model-level quantitative rows from the multiple-sclerosis frailty pilot trial and the PROMOTe trial using reported confidence intervals.
- Added full-text standardized DNAm-aging treatment effects from the CALERIE and DO-HEALTH trials.
- Computed Hedges g and standard errors or generic inverse-variance standard errors for extracted rows, and generated both a harmonization audit and a multi-study pool-candidate table.

Outputs created:
- results/meta_addon/tables/meta_dataset_working.csv
- results/meta_addon/tables/meta_dataset_primary_pooling.csv
- results/meta_addon/tables/meta_pooling_harmonization_audit.csv
- results/meta_addon/tables/meta_multi_study_pool_candidates.csv
- docs/meta_addon/manual_extraction_notes.md

Remaining tasks:
- Continue extracting exact arm-level or model-level values from additional local XML and open PDFs.
- Keep only exact observed values in the primary pooling set; retain assumed-value rows for sensitivity analyses only.

Risks/limitations:
- Current working dataset still has too few independent studies for a stable pooled estimate in most endpoint families.
- Outcome harmonization remains the main constraint, although DunedinPACE now has at least two independent studies for exploratory pooling.

Exact next command:
`python -m src.meta_addon.seed_numeric_extractions --config config/meta_addon_config.yaml`

---
## Phase 24 - Same-outcome pooled estimates
Date/time: 2026-04-23 15:51:44

Completed:
- Selected one primary non-TOT row per study and outcome from the standardized-effect subset.
- Generated a same-outcome pooling input table.
- Computed fixed-effect and random-effects pooled estimates for any outcome with at least two independent studies.

Outputs created:
- results/meta_addon/tables/meta_same_outcome_pooling_inputs.csv
- results/meta_addon/tables/meta_same_outcome_pooling_results.csv

Remaining tasks:
- Continue extracting additional same-outcome standardized DNAm rows to strengthen biological-age pooling beyond DunedinPACE.
- Add manuscript text for the pooled DunedinPACE estimate only after manual review of compatibility assumptions.

Risks/limitations:
- Current same-outcome pooling is limited by the small number of studies and should be treated as exploratory.
- Outcome-version compatibility still requires judgment, especially for PhenoAge variants.

Exact next command:
`python -m src.meta_addon.pool_same_outcome --config config/meta_addon_config.yaml`

---
## Phase 24 - Same-outcome pooled estimates
Date/time: 2026-04-23 15:52:37

Completed:
- Selected one primary non-TOT row per study and outcome from the standardized-effect subset.
- Generated a same-outcome pooling input table.
- Computed fixed-effect and random-effects pooled estimates for any outcome with at least two independent studies.

Outputs created:
- results/meta_addon/tables/meta_same_outcome_pooling_inputs.csv
- results/meta_addon/tables/meta_same_outcome_pooling_results.csv

Remaining tasks:
- Continue extracting additional same-outcome standardized DNAm rows to strengthen biological-age pooling beyond DunedinPACE.
- Add manuscript text for the pooled DunedinPACE estimate only after manual review of compatibility assumptions.

Risks/limitations:
- Current same-outcome pooling is limited by the small number of studies and should be treated as exploratory.
- Outcome-version compatibility still requires judgment, especially for PhenoAge variants.

Exact next command:
`python -m src.meta_addon.pool_same_outcome --config config/meta_addon_config.yaml`

---
## Phase 23 - Meta-analysis Add-on Manual Numeric Extraction Seed
Date/time: 2026-04-23 18:39:19

Completed:
- Seeded the quantitative add-on dataset with exact arm-level end-of-intervention values from the exergame RFA trial.
- Added a sensitivity-only SHARE-FI row from the multidomain lifestyle trial with explicit caveat that SD values were assumed in the source power paragraph.
- Added model-level quantitative rows from the multiple-sclerosis frailty pilot trial and the PROMOTe trial using reported confidence intervals.
- Added full-text standardized DNAm-aging treatment effects from the CALERIE and DO-HEALTH trials.
- Computed Hedges g and standard errors or generic inverse-variance standard errors for extracted rows, and generated both a harmonization audit and a multi-study pool-candidate table.

Outputs created:
- results/meta_addon/tables/meta_dataset_working.csv
- results/meta_addon/tables/meta_dataset_primary_pooling.csv
- results/meta_addon/tables/meta_pooling_harmonization_audit.csv
- results/meta_addon/tables/meta_multi_study_pool_candidates.csv
- docs/meta_addon/manual_extraction_notes.md

Remaining tasks:
- Continue extracting exact arm-level or model-level values from additional local XML and open PDFs.
- Keep only exact observed values in the primary pooling set; retain assumed-value rows for sensitivity analyses only.

Risks/limitations:
- Current working dataset still has too few independent studies for a stable pooled estimate in most endpoint families.
- Outcome harmonization remains the main constraint, although DunedinPACE now has at least two independent studies for exploratory pooling.

Exact next command:
`python -m src.meta_addon.seed_numeric_extractions --config config/meta_addon_config.yaml`

---
## Phase 23 - Meta-analysis Add-on Manual Numeric Extraction Seed
Date/time: 2026-04-23 18:39:43

Completed:
- Seeded the quantitative add-on dataset with exact arm-level end-of-intervention values from the exergame RFA trial.
- Added a sensitivity-only SHARE-FI row from the multidomain lifestyle trial with explicit caveat that SD values were assumed in the source power paragraph.
- Added model-level quantitative rows from the multiple-sclerosis frailty pilot trial and the PROMOTe trial using reported confidence intervals.
- Added full-text standardized DNAm-aging treatment effects from the CALERIE and DO-HEALTH trials.
- Computed Hedges g and standard errors or generic inverse-variance standard errors for extracted rows, and generated both a harmonization audit and a multi-study pool-candidate table.

Outputs created:
- results/meta_addon/tables/meta_dataset_working.csv
- results/meta_addon/tables/meta_dataset_primary_pooling.csv
- results/meta_addon/tables/meta_pooling_harmonization_audit.csv
- results/meta_addon/tables/meta_multi_study_pool_candidates.csv
- docs/meta_addon/manual_extraction_notes.md

Remaining tasks:
- Continue extracting exact arm-level or model-level values from additional local XML and open PDFs.
- Keep only exact observed values in the primary pooling set; retain assumed-value rows for sensitivity analyses only.

Risks/limitations:
- Current working dataset still has too few independent studies for a stable pooled estimate in most endpoint families.
- Outcome harmonization remains the main constraint, although DunedinPACE now has at least two independent studies for exploratory pooling.

Exact next command:
`python -m src.meta_addon.seed_numeric_extractions --config config/meta_addon_config.yaml`

---
## Phase 23 - Meta-analysis Add-on Manual Numeric Extraction Seed
Date/time: 2026-04-23 18:54:37

Completed:
- Seeded the quantitative add-on dataset with exact arm-level end-of-intervention values from the exergame RFA trial.
- Added a sensitivity-only SHARE-FI row from the multidomain lifestyle trial with explicit caveat that SD values were assumed in the source power paragraph.
- Added model-level quantitative rows from the multiple-sclerosis frailty pilot trial and the PROMOTe trial using reported confidence intervals.
- Added full-text standardized DNAm-aging treatment effects from the CALERIE and DO-HEALTH trials.
- Added sensitivity-only epigenetic-age rows from the greens crossover trial and the Fitzgerald pilot RCT where exact contrasts were reported but uncertainty was missing.
- Downloaded the official FMD source workbook and documented the remaining algorithm-reconstruction blocker.
- Computed Hedges g and standard errors or generic inverse-variance standard errors for extracted rows, and generated both a harmonization audit and a multi-study pool-candidate table.

Outputs created:
- results/meta_addon/tables/meta_dataset_working.csv
- results/meta_addon/tables/meta_dataset_primary_pooling.csv
- results/meta_addon/tables/meta_pooling_harmonization_audit.csv
- results/meta_addon/tables/meta_multi_study_pool_candidates.csv
- docs/meta_addon/manual_extraction_notes.md

Remaining tasks:
- Continue extracting exact arm-level or model-level values from additional local XML and open PDFs.
- Keep only exact observed values in the primary pooling set; retain assumed-value rows for sensitivity analyses only.

Risks/limitations:
- Current working dataset still has too few independent studies for a stable pooled estimate in most endpoint families.
- Outcome harmonization remains the main constraint, although DunedinPACE now has at least two independent studies for exploratory pooling.
- The FMD biological-age endpoint is blocked on reconstruction of the exact NHANES-trained algorithm used by the authors.

Exact next command:
`python -m src.meta_addon.seed_numeric_extractions --config config/meta_addon_config.yaml`

---
## Phase 25 - FMD biological-age reconstruction
Date/time: 2026-04-23 19:17:52

Completed:
- Reconstructed participant-level change scores for the FMD biological-age endpoint from the official figshare workbook.
- Used the published Levine biological-age q/k/s parameters and an NHANES-derived variance constant approximation.
- Kept the reconstruction separate from the primary pooling dataset because cohort-wide HbA1c was absent from the workbook.

Outputs created:
- results/meta_addon/tables/fmd_bioage_reconstruction_person_level.csv
- results/meta_addon/tables/fmd_bioage_reconstruction_summary.csv

Remaining tasks:
- Continue searching for the exact original code or full seven-biomarker source values if a publication-grade FMD effect estimate is needed.
- Keep reconstructed FMD values out of primary pooled analyses unless the missing biomarker issue is resolved.

Risks/limitations:
- This reconstruction uses 6 of the 7 biomarkers named in the paper and therefore should be treated as sensitivity analysis only.
- The NHANES-derived variance constant is reproduced from the same method family but is not confirmed against the authors' exact implementation.

Exact next command:
`python -m src.meta_addon.reconstruct_fmd_bioage --config config/meta_addon_config.yaml`

---
## Phase 25 - FMD biological-age reconstruction
Date/time: 2026-04-23 19:18:10

Completed:
- Reconstructed participant-level change scores for the FMD biological-age endpoint from the official figshare workbook.
- Used the published Levine biological-age q/k/s parameters and an NHANES-derived variance constant approximation.
- Kept the reconstruction separate from the primary pooling dataset because cohort-wide HbA1c was absent from the workbook.

Outputs created:
- results/meta_addon/tables/fmd_bioage_reconstruction_person_level.csv
- results/meta_addon/tables/fmd_bioage_reconstruction_summary.csv

Remaining tasks:
- Continue searching for the exact original code or full seven-biomarker source values if a publication-grade FMD effect estimate is needed.
- Keep reconstructed FMD values out of primary pooled analyses unless the missing biomarker issue is resolved.

Risks/limitations:
- This reconstruction uses 6 of the 7 biomarkers named in the paper and therefore should be treated as sensitivity analysis only.
- The NHANES-derived variance constant is reproduced from the same method family but is not confirmed against the authors' exact implementation.

Exact next command:
`python -m src.meta_addon.reconstruct_fmd_bioage --config config/meta_addon_config.yaml`

---
## Phase 23 - Meta-analysis Add-on Manual Numeric Extraction Seed
Date/time: 2026-04-23 19:22:11

Completed:
- Seeded the quantitative add-on dataset with exact arm-level end-of-intervention values from the exergame RFA trial.
- Added a sensitivity-only SHARE-FI row from the multidomain lifestyle trial with explicit caveat that SD values were assumed in the source power paragraph.
- Added model-level quantitative rows from the multiple-sclerosis frailty pilot trial and the PROMOTe trial using reported confidence intervals.
- Added full-text standardized DNAm-aging treatment effects from the CALERIE and DO-HEALTH trials.
- Added sensitivity-only epigenetic-age rows from the greens crossover trial and the Fitzgerald pilot RCT where exact contrasts were reported but uncertainty was missing.
- Downloaded the official FMD source workbook and documented the remaining algorithm-reconstruction blocker.
- Computed Hedges g and standard errors or generic inverse-variance standard errors for extracted rows, and generated both a harmonization audit and a multi-study pool-candidate table.

Outputs created:
- results/meta_addon/tables/meta_dataset_working.csv
- results/meta_addon/tables/meta_dataset_primary_pooling.csv
- results/meta_addon/tables/meta_pooling_harmonization_audit.csv
- results/meta_addon/tables/meta_multi_study_pool_candidates.csv
- docs/meta_addon/manual_extraction_notes.md

Remaining tasks:
- Continue extracting exact arm-level or model-level values from additional local XML and open PDFs.
- Keep only exact observed values in the primary pooling set; retain assumed-value rows for sensitivity analyses only.

Risks/limitations:
- Current working dataset still has too few independent studies for a stable pooled estimate in most endpoint families.
- Outcome harmonization remains the main constraint, although DunedinPACE now has at least two independent studies for exploratory pooling.
- The FMD biological-age endpoint is blocked on reconstruction of the exact NHANES-trained algorithm used by the authors.

Exact next command:
`python -m src.meta_addon.seed_numeric_extractions --config config/meta_addon_config.yaml`

---
## Phase 24 - Same-outcome pooled estimates
Date/time: 2026-04-23 19:29:29

Completed:
- Selected one primary non-TOT row per study and outcome from the standardized-effect subset.
- Generated a same-outcome pooling input table.
- Computed fixed-effect and random-effects pooled estimates for any outcome with at least two independent studies.

Outputs created:
- results/meta_addon/tables/meta_same_outcome_pooling_inputs.csv
- results/meta_addon/tables/meta_same_outcome_pooling_results.csv

Remaining tasks:
- Continue extracting additional same-outcome standardized DNAm rows to strengthen biological-age pooling beyond DunedinPACE.
- Add manuscript text for the pooled DunedinPACE estimate only after manual review of compatibility assumptions.

Risks/limitations:
- Current same-outcome pooling is limited by the small number of studies and should be treated as exploratory.
- Outcome-version compatibility still requires judgment, especially for PhenoAge variants.

Exact next command:
`python -m src.meta_addon.pool_same_outcome --config config/meta_addon_config.yaml`

---
## Phase 23 - Meta-analysis Add-on Manual Numeric Extraction Seed
Date/time: 2026-04-23 19:29:30

Completed:
- Seeded the quantitative add-on dataset with exact arm-level end-of-intervention values from the exergame RFA trial.
- Added a sensitivity-only SHARE-FI row from the multidomain lifestyle trial with explicit caveat that SD values were assumed in the source power paragraph.
- Added model-level quantitative rows from the multiple-sclerosis frailty pilot trial and the PROMOTe trial using reported confidence intervals.
- Added full-text standardized DNAm-aging treatment effects from the CALERIE and DO-HEALTH trials.
- Added sensitivity-only epigenetic-age rows from the greens crossover trial and the Fitzgerald pilot RCT where exact contrasts were reported but uncertainty was missing.
- Downloaded the official FMD source workbook and documented the remaining algorithm-reconstruction blocker.
- Computed Hedges g and standard errors or generic inverse-variance standard errors for extracted rows, and generated both a harmonization audit and a multi-study pool-candidate table.

Outputs created:
- results/meta_addon/tables/meta_dataset_working.csv
- results/meta_addon/tables/meta_dataset_primary_pooling.csv
- results/meta_addon/tables/meta_pooling_harmonization_audit.csv
- results/meta_addon/tables/meta_multi_study_pool_candidates.csv
- docs/meta_addon/manual_extraction_notes.md

Remaining tasks:
- Continue extracting exact arm-level or model-level values from additional local XML and open PDFs.
- Keep only exact observed values in the primary pooling set; retain assumed-value rows for sensitivity analyses only.

Risks/limitations:
- Current working dataset still has too few independent studies for a stable pooled estimate in most endpoint families.
- Outcome harmonization remains the main constraint, although DunedinPACE now has at least two independent studies for exploratory pooling.
- The FMD biological-age endpoint is blocked on reconstruction of the exact NHANES-trained algorithm used by the authors.

Exact next command:
`python -m src.meta_addon.seed_numeric_extractions --config config/meta_addon_config.yaml`

---
## Phase 24 - Same-outcome pooled estimates
Date/time: 2026-04-23 19:33:40

Completed:
- Selected one primary non-TOT row per study and outcome from the standardized-effect subset.
- Generated a same-outcome pooling input table.
- Computed fixed-effect and random-effects pooled estimates for any outcome with at least two independent studies.

Outputs created:
- results/meta_addon/tables/meta_same_outcome_pooling_inputs.csv
- results/meta_addon/tables/meta_same_outcome_pooling_results.csv

Remaining tasks:
- Continue extracting additional same-outcome standardized DNAm rows to strengthen biological-age pooling beyond DunedinPACE.
- Add manuscript text for the pooled DunedinPACE estimate only after manual review of compatibility assumptions.

Risks/limitations:
- Current same-outcome pooling is limited by the small number of studies and should be treated as exploratory.
- Outcome-version compatibility still requires judgment, especially for PhenoAge variants.

Exact next command:
`python -m src.meta_addon.pool_same_outcome --config config/meta_addon_config.yaml`

---
## Phase 23 - Meta-analysis Add-on Manual Numeric Extraction Seed
Date/time: 2026-04-23 19:33:40

Completed:
- Seeded the quantitative add-on dataset with exact arm-level end-of-intervention values from the exergame RFA trial.
- Added a sensitivity-only SHARE-FI row from the multidomain lifestyle trial with explicit caveat that SD values were assumed in the source power paragraph.
- Added model-level quantitative rows from the multiple-sclerosis frailty pilot trial and the PROMOTe trial using reported confidence intervals.
- Added full-text standardized DNAm-aging treatment effects from the CALERIE and DO-HEALTH trials.
- Added sensitivity-only epigenetic-age rows from the greens crossover trial and the Fitzgerald pilot RCT where exact contrasts were reported but uncertainty was missing.
- Downloaded the official FMD source workbook and documented the remaining algorithm-reconstruction blocker.
- Computed Hedges g and standard errors or generic inverse-variance standard errors for extracted rows, and generated both a harmonization audit and a multi-study pool-candidate table.

Outputs created:
- results/meta_addon/tables/meta_dataset_working.csv
- results/meta_addon/tables/meta_dataset_primary_pooling.csv
- results/meta_addon/tables/meta_pooling_harmonization_audit.csv
- results/meta_addon/tables/meta_multi_study_pool_candidates.csv
- docs/meta_addon/manual_extraction_notes.md

Remaining tasks:
- Continue extracting exact arm-level or model-level values from additional local XML and open PDFs.
- Keep only exact observed values in the primary pooling set; retain assumed-value rows for sensitivity analyses only.

Risks/limitations:
- Current working dataset still has too few independent studies for a stable pooled estimate in most endpoint families.
- Outcome harmonization remains the main constraint, although DunedinPACE now has at least two independent studies for exploratory pooling.
- The FMD biological-age endpoint is blocked on reconstruction of the exact NHANES-trained algorithm used by the authors.

Exact next command:
`python -m src.meta_addon.seed_numeric_extractions --config config/meta_addon_config.yaml`

---
## Phase 23 - Meta-analysis Add-on Manual Numeric Extraction Seed
Date/time: 2026-04-23 19:40:33

Completed:
- Seeded the quantitative add-on dataset with exact arm-level end-of-intervention values from the exergame RFA trial.
- Added a sensitivity-only SHARE-FI row from the multidomain lifestyle trial with explicit caveat that SD values were assumed in the source power paragraph.
- Added model-level quantitative rows from the multiple-sclerosis frailty pilot trial and the PROMOTe trial using reported confidence intervals.
- Added full-text standardized DNAm-aging treatment effects from the CALERIE and DO-HEALTH trials.
- Added sensitivity-only epigenetic-age rows from the greens crossover trial and the Fitzgerald pilot RCT where exact contrasts were reported but uncertainty was missing.
- Downloaded the official FMD source workbook and documented the remaining algorithm-reconstruction blocker.
- Computed Hedges g and standard errors or generic inverse-variance standard errors for extracted rows, and generated harmonization, multi-study candidate, and peer-reviewed pool-eligibility audits.

Outputs created:
- results/meta_addon/tables/meta_dataset_working.csv
- results/meta_addon/tables/meta_dataset_primary_pooling.csv
- results/meta_addon/tables/meta_pooling_harmonization_audit.csv
- results/meta_addon/tables/meta_multi_study_pool_candidates.csv
- results/meta_addon/tables/peer_reviewed_pool_eligibility_audit.csv
- docs/meta_addon/manual_extraction_notes.md

Remaining tasks:
- Continue extracting exact arm-level or model-level values from additional local XML and open PDFs.
- Keep only exact observed values in the primary pooling set; retain assumed-value rows for sensitivity analyses only.

Risks/limitations:
- Current working dataset still has too few independent studies for a stable pooled estimate in most endpoint families.
- Outcome harmonization remains the main constraint, although DunedinPACE now has at least two independent studies for exploratory pooling.
- The FMD biological-age endpoint is blocked on reconstruction of the exact NHANES-trained algorithm used by the authors.

Exact next command:
`python -m src.meta_addon.seed_numeric_extractions --config config/meta_addon_config.yaml`

---
## Phase 26 - External Peer-Reviewed Candidate Audit
Date/time: 2026-04-23 19:44:55

Completed:
- Searched beyond the current queue for additional peer-reviewed human intervention studies reporting quantified epigenetic-clock outcomes with extractable uncertainty.
- Audited newly screened candidates against the primary-pool rule: peer-reviewed, human, intervention-based, and directly poolable with reported uncertainty.
- Documented exclusion reasons for non-poolable peer-reviewed candidates rather than forcing weak additions into the primary meta-analysis dataset.

Outputs created:
- results/meta_addon/tables/external_peer_reviewed_candidate_audit.csv
- docs/meta_addon/manual_extraction_notes.md

Remaining tasks:
- Continue targeted searching for peer-reviewed human trials with direct DunedinPACE, GrimAge, or PhenoAge between-group estimates and confidence intervals.
- Keep preprints and reconstructed rows outside the primary pooling set.

Risks/limitations:
- External peer-reviewed candidates found to date mostly report medians, correlations, reconstructed uncertainty, or non-comparator analyses rather than pool-ready contrasts.
- The main peer-reviewed pooled clock result therefore still rests on CALERIE and DO-HEALTH for DunedinPACE.

Exact next command:
`python -m src.meta_addon.seed_numeric_extractions --config config/meta_addon_config.yaml`

---
## Phase 27 - Peer-Reviewed Clock Trial Access Audit
Date/time: 2026-04-23 20:09:00

Completed:
- Rechecked newer peer-reviewed human intervention-clock candidates through primary NCBI metadata rather than secondary summaries.
- Audited `PMID 40424097` (`Aging Cell`, therapeutic plasma exchange) and `PMID 40576558` (`Clinical Infectious Diseases`, pitavastatin/REPRIEVE) against the primary-pool rule.
- Confirmed that both studies are randomized and peer-reviewed, but neither currently yields a directly extractable between-group effect estimate with confidence interval or standard error from accessible primary sources.
- Updated the external peer-reviewed candidate audit and manual extraction notes instead of weakening the primary pooling set.

Outputs created:
- results/meta_addon/tables/external_peer_reviewed_candidate_audit.csv
- docs/meta_addon/manual_extraction_notes.md

Remaining tasks:
- Continue targeted searching for peer-reviewed human trials with direct DunedinPACE, GrimAge, or PhenoAge between-group estimates and reported uncertainty.
- Keep the primary pooling set restricted to peer-reviewed rows with directly extractable uncertainty.

Risks/limitations:
- Several recent peer-reviewed trials report promising clock effects at the abstract level but still lack accessible clock-specific confidence intervals or standard errors.
- The primary pooled biological-age result therefore remains limited to the exact extractable DunedinPACE evidence from CALERIE and DO-HEALTH.

Exact next command:
`python -m src.meta_addon.seed_numeric_extractions --config config/meta_addon_config.yaml`

---
## Phase 28 - DIRECT PLUS Full-Text Pooling Check
Date/time: 2026-04-23 20:22:00

Completed:
- Retrieved the full text PDF for `PMID 37743489` (`DIRECT PLUS`, `BMC Medicine`) and checked the statistical reporting at the article level.
- Confirmed that the trial does not report randomized between-arm differences in methylation-clock change with directly extractable confidence intervals or standard errors.
- Documented that the positive quantitative signals in the paper are adherence-based multivariable beta coefficients for Li and Hannum clocks rather than poolable intervention contrasts.
- Updated the external candidate audit and manual extraction notes without changing the primary pooling dataset.

Outputs created:
- results/meta_addon/tables/external_peer_reviewed_candidate_audit.csv
- docs/meta_addon/manual_extraction_notes.md

Remaining tasks:
- Continue targeted searching for peer-reviewed human intervention studies with direct clock-specific between-group estimates and reported uncertainty.
- Keep the primary DunedinPACE pool restricted to exact extractable peer-reviewed contrasts.

Risks/limitations:
- Even when peer-reviewed full text is accessible, several clock-intervention papers report only null between-arm comparisons or within-trial adherence associations rather than pool-ready randomized contrasts.
- The primary pooled biological-age estimate therefore remains narrow by design.

Exact next command:
`python -m src.meta_addon.seed_numeric_extractions --config config/meta_addon_config.yaml`

---
## Phase 29 - Primary Pool Freeze and Narrow Manuscript Draft
Date/time: 2026-04-23 20:34:00

Completed:
- Adopted the decision to stop expanding the primary meta-analysis until another peer-reviewed study with directly extractable uncertainty is found.
- Replaced the placeholder add-on manuscript with a narrow quantitative draft centered on the exact peer-reviewed DunedinPACE evidence.
- Updated the meta-add-on workflow to state the current primary-pool boundary explicitly.

Outputs created:
- manuscript/meta_addon/manuscript_meta_addon.md
- docs/meta_addon/workflow.md

Remaining tasks:
- If desired, convert the narrow add-on draft into a journal-formatted submission package.
- Continue searching only when a new peer-reviewed human clock trial with CI/SE-bearing treatment estimates becomes available.

Risks/limitations:
- The primary pooled estimate remains narrow by design and should not be written as a broad meta-analysis of all anti-ageing interventions.
- Most additional human clock studies remain sensitivity-only or non-poolable because of incomplete quantitative reporting.

Exact next command:
`python -m src.meta_addon.pool_same_outcome --config config/meta_addon_config.yaml`

---
## Phase 30 - Narrow Add-on Publication Assets
Date/time: 2026-04-23 20:49:00

Completed:
- Added a reproducible renderer for the frozen primary-pool publication assets.
- Generated a primary DunedinPACE study table and pooled summary table from the existing pooling outputs.
- Rendered a forest plot for the peer-reviewed primary DunedinPACE model.
- Added add-on-specific figure legends and references files.
- Updated the narrow manuscript so the pooled estimate cites the underlying studies and points to the rendered figure and table assets.

Outputs created:
- src/meta_addon/render_primary_pool_assets.py
- results/meta_addon/figures/forest_dunedinpace_primary.png
- results/meta_addon/tables/primary_dunedinpace_pool_studies.csv
- results/meta_addon/tables/primary_dunedinpace_pool_summary.csv
- manuscript/meta_addon/figure_legends_meta_addon.md
- manuscript/meta_addon/references_meta_addon.md
- manuscript/meta_addon/manuscript_meta_addon.md

Remaining tasks:
- Convert the narrow markdown manuscript into journal-formatted DOCX assets if submission packaging is needed.
- Add any future peer-reviewed clock trial only if it satisfies the current primary-pool rule.

Risks/limitations:
- The rendered publication assets still represent a two-study biomarker-only pool.
- The add-on remains intentionally narrow and should not be presented as a broad pooled review of anti-ageing interventions.

Exact next command:
`python -m src.meta_addon.render_primary_pool_assets --config config/meta_addon_config.yaml`

---
## Phase 31 - Narrow Meta-analysis Submission Package
Date/time: 2026-04-23 20:10:43

Completed:
- Prepared a dedicated submission package for the narrow peer-reviewed biomarker meta-analysis add-on.
- Generated blinded manuscript, title page, cover letter, declarations, figure legends, two internal peer-review memos, a content/structure/validity audit, a checklist, and automated audit checks.
- Copied the primary forest plot and pooled summary tables into the submission package.

Outputs created:
- submission_assets/MJDRDYPU_AntiAgeing_MetaAddon_2026-04-23/*.docx
- submission_assets/MJDRDYPU_AntiAgeing_MetaAddon_2026-04-23/figures/*.png
- submission_assets/MJDRDYPU_AntiAgeing_MetaAddon_2026-04-23/tables/*.csv
- submission_assets/MJDRDYPU_AntiAgeing_MetaAddon_2026-04-23/*_automated_audit_checks.csv

Remaining tasks:
- Final author scientific sign-off remains required before external submission.

Risks/limitations:
- The package remains intentionally narrow and should be described as a focused biomarker meta-analysis add-on rather than a broad meta-analysis of all anti-ageing interventions.

Exact next command:
`python -m src.meta_addon.prepare_meta_addon_submission --config config/review_config.yaml`

---
## Phase 31 - Narrow Meta-analysis Submission Package
Date/time: 2026-04-23 20:11:31

Completed:
- Prepared a dedicated submission package for the narrow peer-reviewed biomarker meta-analysis add-on.
- Generated blinded manuscript, title page, cover letter, declarations, figure legends, two internal peer-review memos, a content/structure/validity audit, a checklist, and automated audit checks.
- Copied the primary forest plot and pooled summary tables into the submission package.

Outputs created:
- submission_assets/MJDRDYPU_AntiAgeing_MetaAddon_2026-04-23/*.docx
- submission_assets/MJDRDYPU_AntiAgeing_MetaAddon_2026-04-23/figures/*.png
- submission_assets/MJDRDYPU_AntiAgeing_MetaAddon_2026-04-23/tables/*.csv
- submission_assets/MJDRDYPU_AntiAgeing_MetaAddon_2026-04-23/*_automated_audit_checks.csv

Remaining tasks:
- Final author scientific sign-off remains required before external submission.

Risks/limitations:
- The package remains intentionally narrow and should be described as a focused biomarker meta-analysis add-on rather than a broad meta-analysis of all anti-ageing interventions.

Exact next command:
`python -m src.meta_addon.prepare_meta_addon_submission --config config/review_config.yaml`

---
## Phase 31 - Narrow Meta-analysis Submission Package
Date/time: 2026-04-23 20:12:30

Completed:
- Prepared a dedicated submission package for the narrow peer-reviewed biomarker meta-analysis add-on.
- Generated blinded manuscript, title page, cover letter, declarations, figure legends, two internal peer-review memos, a content/structure/validity audit, a checklist, and automated audit checks.
- Copied the primary forest plot and pooled summary tables into the submission package.

Outputs created:
- submission_assets/MJDRDYPU_AntiAgeing_MetaAddon_2026-04-23/*.docx
- submission_assets/MJDRDYPU_AntiAgeing_MetaAddon_2026-04-23/figures/*.png
- submission_assets/MJDRDYPU_AntiAgeing_MetaAddon_2026-04-23/tables/*.csv
- submission_assets/MJDRDYPU_AntiAgeing_MetaAddon_2026-04-23/*_automated_audit_checks.csv

Remaining tasks:
- Final author scientific sign-off remains required before external submission.

Risks/limitations:
- The package remains intentionally narrow and should be described as a focused biomarker meta-analysis add-on rather than a broad meta-analysis of all anti-ageing interventions.

Exact next command:
`python -m src.meta_addon.prepare_meta_addon_submission --config config/review_config.yaml`

---
## Phase 31 - Narrow Meta-analysis Submission Package
Date/time: 2026-04-23 20:25:20

Completed:
- Prepared a dedicated submission package for the narrow peer-reviewed biomarker meta-analysis add-on.
- Generated blinded manuscript, title page, cover letter, declarations, figure legends, two internal peer-review memos, a content/structure/validity audit, a checklist, and automated audit checks.
- Copied the primary forest plot and pooled summary tables into the submission package.

Outputs created:
- submission_assets/MJDRDYPU_AntiAgeing_MJDRDYPU_MetaAddon_Final_2026-04-23/*.docx
- submission_assets/MJDRDYPU_AntiAgeing_MJDRDYPU_MetaAddon_Final_2026-04-23/figures/*.png
- submission_assets/MJDRDYPU_AntiAgeing_MJDRDYPU_MetaAddon_Final_2026-04-23/tables/*.csv
- submission_assets/MJDRDYPU_AntiAgeing_MJDRDYPU_MetaAddon_Final_2026-04-23/*_automated_audit_checks.csv

Remaining tasks:
- Final author scientific sign-off remains required before external submission.

Risks/limitations:
- The package remains intentionally narrow and should be described as a focused biomarker meta-analysis add-on rather than a broad meta-analysis of all anti-ageing interventions.

Exact next command:
`python -m src.meta_addon.prepare_meta_addon_submission --config config/review_config.yaml`
