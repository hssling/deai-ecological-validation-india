# The hidden burden of biological ageing in India (Discover Aging submission)

Redesigned study replacing the IJMR-rejected "biological ageing vulnerability" manuscript
(IJMR_1754_2026). Target journal: **Discover Aging** (Springer Nature).

## What changed and why
The rejected paper built a circular composite index (social variables both inside and predicting the
score), unvalidated against anything external. This redesign removes the index. It defines biological
abnormality by **external clinical thresholds**, keeps biology / social determinants / outcomes strictly
separate, and reframes around the **diagnosis gap** — the disease that biomarkers reveal but self-report
misses — and its social patterning. See `submission_assets/IJMR_concern_response_map.md` for a
point-by-point response to all 21 reviewer comments, and
`docs/superpowers/specs/2026-06-12-...-design.md` for the design rationale and the evidence-driven pivot.

## Data (real LASI Wave 1, 2017-18)
- Harmonized LASI A.3 (Gateway to Global Aging): interview, measured BP, pulse, grip, anthropometry.
- IIPS dried-blood-spot dataset: HbA1c, CRP, haemoglobin.
- IIPS spirometry dataset: FEV1/FVC (GLI-referenced).
Linked by `prim_key`. Restricted microdata are not redistributed.

## Pipeline (run in order, from `analysis/`)
1. `01_build_dataset.py`     — assemble analytic dataset; included-vs-excluded comparison.
2. `02_biological_age.py`    — biomarker measures (KDM [retired], Mahalanobis dysregulation, allostatic load).
3. `03_core_analysis.py`     — diagnosis gap, social patterning, incremental value, burden score.
4. `05_dual_burden_exposome.py` — dual-burden axes + per-domain exposome predictors.
5. `04_geography_figures.py` — state surveillance table + Figures 1-5.
6. `06_sensitivity_ipw.py`   — availability-weighting sensitivity (Table S2).
Helper: `util_survey.py` (weighted estimates, cluster bootstrap CIs).

## Key findings
- 51.3% of biochemical diabetes and 63.8% of measured hypertension undiagnosed in adults 45+.
- Undiagnosed burden concentrated in rural, less-educated, poorer adults.
- Dual burden: cardiometabolic excess (urban/affluent) vs deficit/inflammatory ageing (rural/poor).
- Measured biomarker burden adds little over self-report overall, but carries independent hospitalisation
  signal among the apparently healthy (OR 1.10, 1.03-1.18).

## Outputs
- `outputs/tables/` — all result tables (CSV).
- `outputs/figures/` — Figures 1-5 (PNG).
- `manuscript/` — manuscript, main tables, figures, supplement (Markdown).
- `submission_assets/` — cover letter, declarations, STROBE, IJMR response map, IJMR letter; `docx/` Word versions.

## Honesty notes
- No causal claims; cross-sectional. LASI Wave 2 (not yet in local data: A.3 has no r2* variables)
  is the named next step for prospective validation.
- The KDM biological-age clock was retired after it proved ill-conditioned on this biomarker panel
  (Supplementary note S7) — reported transparently rather than forced.
