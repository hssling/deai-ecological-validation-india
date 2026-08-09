# Data dictionary and output map

## Main evidence-map products

| File | Purpose | Key fields |
|---|---|---|
| `tables/intervention_credibility_ranking.csv` | Ranked intervention classes | intervention, study counts, claim scores, hype rate, credibility score/tier |
| `tables/translational_readiness.csv` | Translation-oriented summary | credibility, human/trial counts, ageing/healthspan/biomarker counts, category |
| `tables/quality_control_flags.csv` | QC issues retained for review | issue type, count, severity, detail |
| `tables/duplicate_cohort_checks.csv` | Potential cohort-overlap checks | duplicate key, record count, titles, manual action |
| `tables/full_text_verification_priority_human.csv` | Human full-text queue | identifiers, source/access type, eligibility and signal fields, verification status |
| `tables/effect_size_extraction_priority_human.csv` | Human numerical-extraction queue | intervention, ageing domain, candidate text, final effect/uncertainty, status |
| `tables/risk_of_bias_formal_preliminary_human.csv` | Preliminary risk-of-bias worksheet | randomization, blinding, missing data, confounding, measurement, reporting, overall |

The complete project-level exports are under `results/tables/` and include search,
deduplication, title/abstract screening, full-text status, extraction, topic,
mechanism, evidence, meta-analysis, and translational tables. The supplementary
workbook in `results/supplement/` preserves the human-review queue and notes.

## Metadata and analysis add-ons

- `metadata/extraction_dictionary.csv` is the field-level extraction dictionary.
- `meta_dnam_clocks/data/processed/` contains clock-specific normalized records,
  eligibility/extraction tables, and meta-analysis inputs; its `docs/` and `src/`
  define the fields and processing stages.
- `meta_frailty_lmic/data/processed/` and its results tables contain the frailty
  workflow outputs; its `docs/` and numbered `src/` scripts define the data model.
- `data_raw/raw_records_initial_pilot.csv` is the initial pilot snapshot; newer
  dated raw metadata are retained in the scoped add-on trees.

## Interpretation rules

Blank values mean “not reported/not extracted/not applicable” unless table
documentation says otherwise. An automated field is not a final human
adjudication. Scores and flags are derived summaries and must be interpreted with
the source records, decision logs, protocol, and extraction manual.
