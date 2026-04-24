# Decision Log

- Created autonomous project scaffold.
- Chose metadata-assisted screening as the initial feasible fallback because full-text retrieval is heterogeneous and may be inaccessible for some journals.
- Preprints are retained but separated and penalized.
- Biomarker improvements are not labeled true age reversal unless paired with organism-level functional evidence.

- 2026-04-23: Europe PMC complex query behavior produced zero pilot results despite source availability on simple queries. Decision: retain source in registry, log issue, and prioritize PubMed/Crossref for pilot while planning source-specific query simplification.
- 2026-04-23: Developed the manuscript package as a pilot evidence map rather than a final submission manuscript because full-text verification, formal risk-of-bias assessment, duplicate cohort checks, and effect-size extraction are still incomplete.
- 2026-04-23: Added automated quality-control flags to prevent overclaiming from preprints, animal/cellular studies, surrogate endpoints, metadata-only extraction, and unsupported high-readiness classifications.
- 2026-04-23: Prioritized high-quality human evidence for full-text verification because complete full-text review of all 484 candidates is not feasible in one automated pass. Decision: create auditable full-text screening artifacts for all candidates, then attempt open PMC/PubMed/repo-abstract verification for the top 40 human records.
- 2026-04-23: Candidate numeric effect text is stored as an extraction aid only. Decision: do not calculate pooled effects or final effect sizes until manual verification confirms outcome, comparator, direction, denominator, follow-up, and uncertainty measure.
