# Scoping Report

Generated from PubMed scoping search on 2026-05-18.

## Search Yield

- PubMed reported hits: 3425
- Records downloaded: 3418
- Deduplicated records: 3418

## Title/Abstract Screening Counts

| screen_decision       |    n |
|:----------------------|-----:|
| include_title_abs     | 1129 |
| exclude               |  656 |
| context_review        |  564 |
| maybe_nonrandomized   |  384 |
| maybe_outcome_unclear |  360 |
| context_protocol      |  325 |

## Full-Text Priority Counts

| screen_decision       | fulltext_priority      |   n |
|:----------------------|:-----------------------|----:|
| context_protocol      | not_applicable         | 325 |
| context_review        | not_applicable         | 564 |
| exclude               | not_applicable         | 656 |
| include_title_abs     | A_primary_fulltext     | 297 |
| include_title_abs     | B_secondary_fulltext   | 210 |
| include_title_abs     | C_sarcopenia_secondary |  97 |
| include_title_abs     | D_sarcopenia_context   | 123 |
| include_title_abs     | low                    | 402 |
| maybe_nonrandomized   | not_applicable         | 384 |
| maybe_outcome_unclear | not_applicable         | 360 |

## Interpretation

The field is large and cannot be screened as a generic exercise/nutrition review without substantial duplication of recent NMAs. The primary full-text queue contains 297 records that appear to be community, primary-care, home-based or implementation-relevant frailty RCT candidates. A further 210 frailty RCT candidates are retained as secondary because setting or delivery is less directly relevant to Indian primary care. Sarcopenia-only trials are retained as a secondary stratum (97 community sarcopenia candidates) and should not drive the main frailty conclusion unless frailty outcomes are reported.

## Immediate Next Step

Full-text screening should begin with `results/tables/fulltext_queue_primary_A.csv`. Each exclusion must be logged against PRISMA-compatible reasons:

- not randomized or not cluster randomized
- not prefrail/frail or no frailty/function vulnerability at baseline
- not community/home/outpatient/primary-care relevant
- no eligible intervention
- no extractable frailty/function outcome
- duplicate cohort/publication
- abstract/protocol only

## NMA Feasibility Status

NMA is not yet approved. It becomes eligible only after full-text extraction demonstrates a connected network with coherent intervention nodes and at least one primary outcome.
