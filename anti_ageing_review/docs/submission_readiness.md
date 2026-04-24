# Submission Readiness Checklist

Generated: 2026-04-23

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

- Raw records: 1155
- Deduplicated records: 1029
- Included records: 29
- Uncertain records: 455
- Excluded records: 545
- Full-text candidates: 484
- Intervention groups scored: 14
- Priority human records verified/attempted: 40
- Duplicate/cohort check flags: 45

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
