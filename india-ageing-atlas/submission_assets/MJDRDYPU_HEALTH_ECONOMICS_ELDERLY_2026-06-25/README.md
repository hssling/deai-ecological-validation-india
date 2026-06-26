# MJDRDYPU submission package — Health economics of elderly care in India

Generated 2026-06-26.

**Title:** Where the money goes: catastrophic spending, impoverishment, and the hidden cost of family care among older adults in India

**Target journal:** Medical Journal of Dr. D.Y. Patil University (MJDRDYPU) — original full-length article.

**Data:** Longitudinal Ageing Study in India (LASI) Wave 1, 2017–18 (harmonised Gateway to Global Aging file), adults aged 60+ (n=31,766); 45+ used as a sensitivity sample.

## Files

| File (.docx and .md) | Purpose |
|---|---|
| `manuscript` | Blinded manuscript (abstract ~247 words; main text ~2,800 words) |
| `title_page` | Title, running title, authorship block (placeholders), word counts, keywords |
| `tables` | Tables 1–6 plus the caregiving table |
| `figure_legends` | Legends for Figures 1–6 |
| `declarations` | Ethics, funding, conflicts, data availability, contributions, AI-use statement |
| `cover_letter` | Cover letter to the Editor |
| `STROBE` | STROBE cross-sectional checklist with section mapping |
| `supplementary` | Variable definitions, 45+ sensitivity, full decomposition and two-part model, caveats |
| `internal_review` | Internal double-reviewer critique and author responses |
| `figures/` | Figures 1–6 (PNG, 600 dpi) |

## Headline findings

- 20.7% of older households spent more than 40% of capacity to pay on health; 35.7% exceeded a tenth of total consumption.
- Out-of-pocket payments pushed an additional 5.8% of older people below the poverty line; rural areas worst affected.
- Rural residence, multimorbidity and functional limitation were the strongest predictors of catastrophic spending.
- Unpaid family care was worth about Rs 1.3 lakh crore a year.
- Covering inpatient care alone removed 1.8 percentage points of catastrophic spending; covering outpatient and medicine costs removed 16.1.

## Reproducibility

All result tables and figures are produced by `scripts/run_health_economics_mjdrdypu.py` and `scripts/make_health_economics_figures.py` in the repository root, using functions in `src/health_economics.py` (unit-tested in `tests/test_health_economics.py`). External benchmark parameters and their sources are in `data/external/health_economics_params.csv` and `docs/health_economics_external_sources.md`.

## Before submission (human checks)

Author name, affiliation, ORCID, email and date are bracketed placeholders in the title page, cover letter and declarations. Confirm the journal's current word limits, figure-resolution and table-placement rules, and fee policy before upload.
