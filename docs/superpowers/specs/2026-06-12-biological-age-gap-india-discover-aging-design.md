# Design Spec — The Biological Age Gap in India (Discover Aging submission)

**Date:** 2026-06-12
**Author/guarantor:** Dr Siddalingaiah H S
**Target journal:** Discover Aging (Springer Nature, OA; journal 44518). In scope: geroscience & biomarkers of aging, frailty/sarcopenia, big data, translational + policy, SDG-aligned.
**Supersedes:** IJMR submission "Biological ageing vulnerability among adults aged 45+ in India…" (IJMR_1754_2026), rejected 2026-06-12.

## 1. Problem with the rejected paper

Twenty-one reviewer comments reduce to one fatal flaw plus four supporting ones:

1. **Circularity (R3.4, R1.2):** social/functional measures were components of the "integrated BAV" index AND used as predictors of it.
2. **No external validation (R3.1, R3.5):** index defined, measured, validated in one cross-section, against itself.
3. **Conceptual vagueness (R2.1, R2.2):** "vulnerability / frailty / biological age / surveillance" used interchangeably.
4. **Weak construct (R3.2, R2.4):** PC1 explained only 23.3% of variance.
5. **No incremental value shown (R3.3, R3.6, R3.7):** never demonstrated added value over age + smoking + fuel.

Plus: missing-data/selection handling (R2.3), incomplete survey-design variance (R2.5), measurement error from proxies (R2.7, R1.4), generalisability untested (R1.7).

These cannot be patched; the index design is the problem. Replace it.

## 1b. EVIDENCE-DRIVEN PIVOT (2026-06-12, after first analysis pass)

Empirical reality forced an honest change of primary thesis:
- LASI's DBS panel lacks renal/liver/lipid markers, so KDM biological-age is ill-conditioned
  (s_ba2 < 0; BAA SD = 25.8 yr; negative convergent validity). The 45+ sample also carries TWO
  opposing ageing phenotypes (metabolic excess vs frailty/wasting). KDM-in-years is therefore NOT
  a defensible primary measure here — retired to supplement, reported honestly.
- For physical-function outcomes (ADL, frailty, falls) chronological AGE out-predicts any biomarker
  composite (e.g., ADL AUROC age 0.65 vs dysregulation 0.57). Forcing a "biological clock beats age"
  claim would repeat the exact overclaim IJMR R3 rejected.
- Where biomarkers genuinely add value: capturing UNDISCLOSED disease burden. 51% of biochemically
  diabetic (HbA1c>=6.5) older Indians are UNDIAGNOSED; 60% of measured-hypertensive are undiagnosed;
  both steeply socially patterned (rural 58% vs urban 44%; no-education 60% vs educated 44%).

**Revised primary thesis:** "The hidden burden of biological ageing in India" — measured biomarkers
reveal subclinical/undiagnosed cardiometabolic, haematologic and inflammatory burden invisible to
self-report and to simple indicators, and this hidden burden is concentrated in the rural, poor,
low-education and (for some markers) female. This is the rigorous, honest answer to "why not just use
age + smoking + fuel," it is novel and policy-shaping for India (diagnosis/treatment gap, equity,
SDG3), and it is squarely in Discover Aging scope (biomarkers of aging).

Supporting (honest) threads: (i) a multi-system subclinical biomarker burden score (allostatic-load
style count) + Mahalanobis physiological dysregulation as biomarker-of-ageing measures that add to
disease-burden prediction (multimorbidity, hospitalisation) while age dominates physical function;
(ii) exposome/social predictors of biological burden (clean directionality, no circularity);
(iii) equity gap and geographic surveillance.

## 2. (original) Reframe — validated biological-age clock + exposome gap [superseded by 1b]

### 2.1 Construct (biomarkers only — no social, no self-reported function)
**Biological Age (BA)** via the **Klemera–Doubal Method (KDM)**, self-calibrated to the LASI sample.
Biomarker panel (measured): log-CRP, HbA1c, haemoglobin, systolic BP, resting pulse,
spirometry (FEV1 or FVC, GLI-referenced), waist circumference (or BMI), grip strength.
**Biological Age Acceleration (BAA)** = BA − chronological age (KDM residual form).

Triangulation / robustness measures (also biomarker-only):
- Mahalanobis physiological dysregulation (Cohen) — needs no chronological age.
- Allostatic-load count (number of biomarkers in high-risk quartile).

This fixes circularity (social vars become predictors), conceptual clarity (BA in years,
established method), construct strength (KDM not PC1-variance), measurement (measured not proxy).

### 2.2 Validation (honest; cross-sectional Wave 1 only — confirmed no r2*/mortality locally)
Criterion = outcomes NOT used to build the clock:
- Concurrent: hospitalisation (past year), ADL/IADL disability, frailty index, falls, poor SRH, multimorbidity.
- **Incremental-value test (kills R3.3):** nested logistic models per outcome:
  (a) age+sex; (b) +smoking+fuel+education+wealth (the "simple indicators"); (c) +BAA.
  Report ΔAUROC, NRI/IDI, LR test, AIC. Honest where BAA does not add.
- **External benchmark:** cite KDM-BA mortality prediction in NHANES/CHARLS/ELSA; name prospective
  LASI Wave 2 validation as explicit next step. No mortality overclaim.

### 2.3 Novel India contributions
- **Hidden ageing / undiagnosed risk:** among adults reporting no diagnosed diabetes/hypertension,
  quantify biologically-defined risk (HbA1c≥6.5 undiagnosed; elevated unmedicated BP); show BAA
  captures it; show it is socially patterned (low-education, rural, poor, female). Direct evidence
  that biomarkers reveal what self-report misses.
- **Exposome → BAA (clean directionality, no circularity):** household exposome (cooking fuel,
  sanitation, drinking water, tobacco, indoor air) + social position (education, caste, wealth, sex,
  residence) + state climate/PM2.5 context as predictors of accelerated biological ageing.
- **Equity gap headline:** design-weighted biological-age gap, poorest vs richest and no-education
  vs higher-education (years of excess biological ageing). Population-attributable framing for
  modifiable household exposures.
- **Geographic surveillance:** design-weighted state-level mean BAA; states with excess biological
  ageing beyond chronological-age/composition expectation.

### 2.4 Methods rigour (addresses R2.3, R2.5, R2.7)
- Survey design: person + biomarker weights; PSU/strata extracted from IIPS raw modules where
  available; design-based (Taylor) variance; SSU clustering fallback. Transparent about limits.
- Missing data: included-vs-excluded comparison table; complete-case primary; multiple imputation
  (MICE) + inverse-probability-of-availability weighting as sensitivity.
- Measurement: measured biomarkers; spirometry restricted to QC acceptable/usable; recompute GLI
  z-scores correctly (prior pipeline had zero-variance FEV1 z — fix).

### 2.5 Dropped from old paper
Integrated BAV stew; PCA headline; circular social-predicts-index regression; vague
vulnerability/surveillance language; leave-one-domain-out AUROC trick.

## 3. Deliverables
- New project folder `india-ageing-atlas/biological_age_gap_2026/` (analysis, outputs, manuscript, submission_assets).
- Reproducible Python pipeline (+ optional R survey cross-check).
- Figures: BA vs chronological calibration; BAA distribution; equity gap; exposome predictors;
  hidden-ageing; incremental-value; state map.
- Manuscript formatted to Discover Aging guidelines.
- Submission assets: cover letter, declarations, data availability, reporting checklist (STROBE),
  supplementary tables.
- Point-by-point map: every IJMR reviewer concern → how addressed.
- Post-acceptance letter to IJMR editorial board (draft/template).

## 4. Data foundation (verified real)
Harmonized LASI A.3 (Wave 1, 2017-18; 73,408 rows; measured BP/pulse/grip/BMI/waist) + IIPS DBS
(CRP n=58,288; HbA1c n=58,289; Hb n=58,294) + IIPS spirometry (FVC/FEV1 n≈50,235) linked by prim_key.
Weights: r1wtresp, r1nwtresp (biomarker), hh1wthh. Cluster: ssuid. Strata/PSU: from IIPS raw zips.

## 5. Out of scope / non-goals
No causal claims; no individual clinical risk score; no mortality prediction from local data;
no genetic/omics analysis; no redistribution of restricted microdata.
