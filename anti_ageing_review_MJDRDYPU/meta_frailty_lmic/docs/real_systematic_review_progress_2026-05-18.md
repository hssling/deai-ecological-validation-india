# Real Systematic Review Progress Report

Generated: 2026-05-18

## What Changed

The project has moved from submission-asset scaffolding into real systematic-review execution. The expanded search, deduplication, first-reviewer full-text eligibility and numeric table mining have now been run. Final submission assets should not be rebuilt until second-reviewer eligibility, numeric extraction, RoB 2 and synthesis are complete.

## Expanded Accessible Search

| database           | status                           |   records | note                                                                       |
|:-------------------|:---------------------------------|----------:|:---------------------------------------------------------------------------|
| PubMed_existing    | ok                               |      3418 | From prior authenticated PubMed XML pull                                   |
| Europe PMC         | ok                               |      5000 | page_size=1000; max_pages=5                                                |
| ClinicalTrials.gov | ok                               |       895 | page_size=100; max_pages=10                                                |
| Crossref           | ok                               |      1000 | rows=1000                                                                  |
| OpenAlex           | ok                               |      1000 | rows_limit=1000                                                            |
| Embase             | not_searched_no_subscription     |         0 | Requires institutional subscription/API access                             |
| Scopus             | not_searched_no_subscription     |         0 | Requires institutional subscription/API access                             |
| CENTRAL            | not_searched_no_api_in_workspace |         0 | Search manually or through Cochrane Library access before final submission |
| Web of Science     | not_searched_no_subscription     |         0 | Requires institutional subscription/API access                             |

## Expanded Screening Counts

| decision                         |    n |
|:---------------------------------|-----:|
| exclude_no_frailty_or_sarcopenia | 3913 |
| exclude_not_rct_signal           | 2527 |
| fulltext_candidate               |  973 |
| secondary_disease_specific       |  711 |
| context_protocol                 |  575 |
| context_review                   |  418 |
| registry_candidate               |  353 |
| exclude_population_unclear       |  244 |
| maybe_intervention_unclear       |  239 |
| secondary_setting                |  164 |

## Accessible PMC Full-Text Eligibility: First Reviewer

| decision                           |   n |
|:-----------------------------------|----:|
| exclude                            |  74 |
| defer_second_reviewer              |  40 |
| include_primary_accessible         |  39 |
| secondary_sarcopenia_verify        |  36 |
| include_secondary_setting          |  24 |
| include_secondary_disease_specific |  24 |

Primary-accessible first-reviewer includes: 39

## Preliminary Nodes Among Primary-Accessible Includes

| node                              |   primary_accessible_studies |
|:----------------------------------|-----------------------------:|
| exercise_plus_nutrition           |                            9 |
| nutrition_only                    |                            7 |
| multidomain                       |                            7 |
| exercise_only                     |                            6 |
| multicomponent_exercise           |                            5 |
| digital_home_unclear_intervention |                            2 |
| mind_body                         |                            1 |
| unclear                           |                            1 |
| multidomain_exercise_nutrition    |                            1 |

## Numeric Table Mining

Numeric table mining identified candidate outcome tables in 34 of 39 primary-accessible studies. These are source-table candidates, not completed effect sizes.

| outcome                 |   studies_with_candidate_tables |   candidate_table_rows |
|:------------------------|--------------------------------:|-----------------------:|
| adherence               |                               2 |                      2 |
| adl_iadl                |                              11 |                     15 |
| adverse_events          |                               2 |                      6 |
| falls                   |                               6 |                     12 |
| frailty_status_or_score |                              29 |                     56 |
| gait_speed              |                              18 |                     27 |
| grip_strength           |                              19 |                     34 |
| quality_of_life         |                               8 |                     13 |
| sppb                    |                              12 |                     21 |

## NMA Gate Status

| gate                                                       | status       | value   |
|:-----------------------------------------------------------|:-------------|:--------|
| Primary-accessible first-reviewer includes >=20            | pass         | 39      |
| At least 3 preliminary intervention nodes with >=2 studies | pass         | 6       |
| Arm-level effect sizes extracted                           | not_met      | 0       |
| Comparator network connectivity assessed                   | not_assessed |         |
| Transitivity assessed                                      | not_assessed |         |
| Second reviewer agreement completed                        | not_met      | 0       |

## Current Scientific Decision

The review is now genuinely underway, but it is still not ready for final assets or submission. The accessible evidence base contains enough first-reviewer primary candidates to justify continuing pairwise synthesis planning. NMA remains unavailable until arm-level effect sizes, comparator nodes and transitivity variables are extracted and checked.

## Required Next Steps

1. Complete second-reviewer full-text eligibility for all 237 mined PMC full texts, starting with the 39 primary-accessible includes and 40 deferred records.
2. Retrieve and screen the 84 publisher/library full texts from the original high-confidence queue and any important expanded candidates without PMC access.
3. Extract arm-level numeric data from `results/tables/primary_accessible_numeric_table_mining.csv`.
4. Complete RoB 2 for included randomized trials.
5. Build pairwise meta-analysis datasets for frailty status/score, gait speed, SPPB and grip strength only after numeric extraction is complete.
6. Run NMA only if the final comparator graph is connected and transitivity is defensible.
7. Rebuild submission assets only after these evidence steps are complete.
