# National spirometry reference equations from LASI — discovery paper design

**Date:** 2026-07-08
**Author:** Dr Siddalingaiah H S (single author)
**Status:** Approved concept → build derivation core, then checkpoint before manuscript

## Idea

Derive the first *nationally representative* spirometry reference equations for middle-aged
and older Indians (≥45 y) from LASI Wave 1, and re-estimate the national burden of
restrictive (RSP) and preserved-ratio (PRISm) impairment under a home-grown reference.
Motivated directly by the Lung India reviewer's point that India lacks population-appropriate
reference values; existing Indian equations (Chhabra n=685 Delhi; Agarwal n=1,258 Pune) are
small regional convenience samples. LASI is the first national spirometry dataset.

Companion to the Lung India revision (`LungIndia_revised_2026-07-08/`), which quantified that
PRISm prevalence swings 40.6%→3.9% by reference choice. This paper builds the missing tool.

## Approved decisions (2026-07-08)

1. **Healthy reference population = GLI convention**: never-smokers, no self-reported lung
   disease/asthma, all body sizes. n ≈ 24,300 (10,241 M / 14,059 F). Maximises
   representativeness and sample; matches GLI/Chhabra/Agarwal practice.
2. **Method = Python LMS-style now, GAMLSS refinement later.** Model median (M) and scatter
   (S) as functions of age and height per sex; z = (obs−M)/S; LLN = 5th centile. Validate
   holdout mean-z≈0, SD≈1. Port to R `gamlss` for final submission if a toolchain is available.
3. **Scope = focused**: equations + validation + comparison + burden re-estimation. Phenotypes
   (direction ③) and prognostic low-FVC-vs-PRISm (④) are sequenced follow-ups that will cite
   this reference.

## Method detail

- Data: `data/processed/biomarker_integrated_analysis_dataset.csv` + height (`bm067`) from
  raw `lasi_w1b_ind_bm.dta`, linked by `prim_key` (as in the revision analysis).
- Healthy subset filters: acceptable spirometry, age 45–95, plausible height (120–210),
  `r1smokev`≠1, `chronic_lung_disease`≠1, `chronic_asthma`≠1.
- Per sex, per parameter (FEV1, FVC in L; FEV1/FVC):
  - **M (median):** log-linear GLI-style form, ln(param) = a + b·ln(height) + spline(age);
    natural cubic spline for age nonlinearity. Ratio modelled on natural scale, ~linear in age.
  - **S (scatter):** age-varying SD from a smooth model of residual spread
    (E|resid| = S·√(2/π)); L fixed at 1 (normal) for v1, skew noted as GAMLSS refinement.
  - z = (obs − M)/S; LLN = M − 1.645·S (5th centile).
- **Validation:** 80/20 split within healthy subset; in holdout, mean z should be ≈0 and
  SD ≈1 overall and across age bands (45–54, 55–64, 65–74, 75+) — the standard reference-
  equation adequacy check.
- **Comparison:** apply the LASI reference to the full analytic sample (n≈30,996) and report
  PRISm/RSP prevalence beside GLI-2012 SE-Asian, GLI-Global 2022, Chhabra-2014, Agarwal-2020.
- **Figures:** centile curves (M, LLN vs age at reference height, by sex); z-score adequacy
  in holdout; reference-comparison prevalence with LASI reference added.

## Honest limitations (to state prominently)

- ≥45 only → explicitly *older-adult* equations (novel niche, not universal).
- Field/handheld spirometry → measurement floor; not lab-gold-standard.
- "Healthy" from survey self-report (no symptom questionnaire / prior TB detail).
- Cross-sectional, single spirometry occasion; L fixed at 1 in v1.

## Deliverables (new folder `prism_lasi_2026/national_ref_equations_2026/`)

- `analysis/01_derive_reference.py` (derivation + validation + comparison)
- `analysis/02_figures.py` (centile curves, adequacy, comparison)
- `outputs/` (coefficient tables, validation metrics, comparison, key_numbers.json)
- Manuscript + assets AFTER the derivation-core checkpoint with the user.

## Success criteria

- Holdout adequacy: |mean z| < 0.1 and SD within 0.9–1.1 overall.
- Reproducible; equations published as explicit coefficient tables.
- Burden re-estimation traces to outputs.
- Nothing outside the new folder modified (except this spec).
