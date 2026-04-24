# Quality Control Audit

| issue_type                                   |   n_records | severity   | detail                                                                               |
|:---------------------------------------------|------------:|:-----------|:-------------------------------------------------------------------------------------|
| extraction_schema_missing_fields             |           0 | none       | All required extraction fields present.                                              |
| unresolved_duplicate_groups                  |          84 | medium     | Potential duplicate title/identifier groups require manual review before submission. |
| preprint_treated_as_supported                |           0 | none       | Preprints should not be treated as established evidence.                             |
| animal_or_cellular_claim_supported           |           0 | none       | Animal/cellular records should not be described as human-ready evidence.             |
| surrogate_endpoint_overclassified            |          79 | medium     | Surrogate-only records should not drive strong anti-ageing conclusions.              |
| metadata_only_claims                         |         484 | medium     | These records require full-text verification before final inference.                 |
| missing_effect_sizes                         |         484 | high       | Comparable effect sizes are required before meta-analysis.                           |
| intervention_supported_without_human_records |           0 | none       | No intervention should be marked supported for healthspan without human records.     |
| speculative_intervention_high_score          |           0 | none       | Speculative classes with high scores need manual review of scoring components.       |
