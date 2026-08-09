# Extraction Codebook v1

Generated: 2026-05-18

## Reviewers

- Primary author 1: Dr Siddalingaiah H S
- Primary author 2: Dr Chandrakala D
- Arbitration: joint consensus between both authors

## Core Forms

- `results/tables/dual_author_fulltext_assignments.csv`: full-text verification and reviewer allocation.
- `results/tables/study_characteristics_extraction_form.csv`: design, population, intervention and comparator extraction.
- `results/tables/numeric_outcome_extraction_form.csv`: synthesis-ready numeric outcomes by study and outcome.
- `results/tables/rob2_assessment_form.csv`: Cochrane RoB 2 domain-level judgements.
- `results/tables/india_implementation_readiness_form.csv`: Indian primary-care deliverability scoring.

## Extraction Rules

1. Do not mark a study as finally included until the full text has been checked by at least one author and conflicts have been resolved.
2. Use the longest common clinically relevant follow-up for primary synthesis; retain all timepoints in notes if multiple are reported.
3. Prefer intention-to-treat values when both intention-to-treat and per-protocol results are available.
4. For continuous outcomes, extract mean, SD and n by arm. If only change scores are available, extract change-score data and note this explicitly.
5. For binary frailty reversal or adverse events, extract events and denominators by arm.
6. Keep comparator wording literal during extraction; collapse comparator nodes only after all records are extracted.
7. NMA eligibility requires final comparator-node connectivity and a transitivity table. Do not infer this from title/abstract screening.

## Implementation-Readiness Scoring

Score each domain 0 to 2, where 2 is most feasible for Indian primary care:

- Delivery setting: 2 = home/community/primary care, 1 = outpatient/day service, 0 = hospital/residential-only.
- Workforce fit: 2 = ASHA/ANM/physiotherapist/community worker feasible, 1 = specialist supervision intermittently needed, 0 = specialist-intensive.
- Equipment burden: 2 = no/minimal equipment, 1 = low-cost equipment, 0 = machines/gym/lab equipment.
- Dose clarity: 2 = replicable frequency/intensity/duration, 1 = partially specified, 0 = unclear.
- Safety monitoring: 2 = low-risk and monitored, 1 = moderate monitoring need, 0 = high-risk or poorly described.
- Adherence feasibility: 2 = adherence support/reporting clear, 1 = partial, 0 = unclear or low adherence.
- Procurement burden: 2 = no product/supplement procurement, 1 = low-cost supplement/materials, 0 = expensive/proprietary supply.
