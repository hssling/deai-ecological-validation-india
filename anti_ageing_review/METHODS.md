# Methods and reproducibility record

## Study design

This project is a systematic evidence map and credibility-ranking synthesis of
interventions marketed or investigated for anti-ageing, slowing biological ageing,
healthspan improvement, biomarker reversal, or organismal rejuvenation. It is
secondary research: it does not enrol participants and does not analyse a new
patient-level cohort. The manuscript therefore distinguishes human outcomes,
healthspan, biomarkers, lifespan, and mechanistic evidence rather than treating
all ageing signals as equivalent.

## Search and record construction

Search terms and source endpoints are versioned in `config/search_terms.yaml` and
`config/source_registry.yaml`. The main workflow uses bibliographic metadata from
PubMed/Europe PMC and other configured metadata services, then stores search-run
outputs and provenance in `results/tables/search_runs.csv` and the raw-data trees.
The dated exports in this repository are the snapshot used for the accepted
revision; rerunning retrieval is expected to find new or changed records.

## Screening, deduplication, and verification

The pipeline normalises records, deduplicates by persistent identifiers where
available and by title/metadata fallbacks otherwise, and assigns screening queues.
Eligibility definitions, exclusion reasons, and manual adjudication rules are in
`docs/inclusion_exclusion.md`, `docs/screening_manual.md`, and
`docs/extraction_manual.md`. Full-text access is assessed separately from
eligibility. Human verification remains required for high-priority records,
effect-size extraction, and risk-of-bias judgments.

## Classification and evidence grading

Interventions are mapped to controlled categories in the review configuration and
mechanism maps. Outcomes are separated into hard ageing/health outcomes, healthspan,
clinical measures, biological-age or other biomarkers, and surrogate signals.
Credibility scores combine the documented evidence dimensions and are used for
ranking and visualization; they are not causal effect estimates, clinical
recommendations, or a pooled meta-analysis. Risk-of-bias forms and quality flags
are retained as auditable intermediate products.

## Quantitative add-ons

`meta_dnam_clocks/` is a scoped DNA-methylation-clock meta-analysis workflow.
`meta_frailty_lmic/` is a scoped frailty-intervention evidence workflow. Each has
its own README/docs, configuration, raw metadata, processing scripts, outputs, and
tests. These add-ons must not be interpreted as automatically changing the main
evidence-map conclusions; they are designed for later human review and manuscript
development.

## Figures, manuscript, and supplementary material

`make_figures.py` regenerates the four main evidence-map figures from the released
ranking table. The modular `src/` workflow can regenerate broader tables, figures,
manuscript drafts, supplementary assets, and journal files through the `Makefile`.
The accepted revision files and publisher proof are retained for comparison with
the exact submission state.

## Updating the project

For a new evidence cycle:

1. Add a dated configuration or search-run revision.
2. Record source, query, retrieval date, endpoint, and response files.
3. Preserve raw metadata and write new derived outputs rather than overwriting the
   accepted snapshot.
4. Complete screening, full-text verification, extraction, and risk-of-bias fields
   with explicit provenance and reviewer notes.
5. Regenerate figures/manuscript assets, run tests and validation, and record the
   decision in `docs/decision_log.md`.

The project is designed for incremental evidence updates rather than silent
replacement of historical results.
