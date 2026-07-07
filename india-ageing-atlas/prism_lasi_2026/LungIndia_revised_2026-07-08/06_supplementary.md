# Supplementary Material

**How Much Preserved Ratio Impaired Spirometry in Older Indians Is Real? (LASI Wave 1).**

## Supplementary Methods

### Analytic sample and height recovery

The LASI Wave 1 harmonized file contained 66,470 adults aged ≥45 years. Of these, 50,256 had a graded spirometry attempt and 31,090 met the acceptability grade. Measured standing height (variable `bm067`, cm) was recovered from the raw LASI individual biomarker file and linked to the analytic file by participant key; after excluding implausible height (<120 or >210 cm; n = 94), 30,996 adults with height formed the analytic sample used for all reference-equation computations.

### Reference-equation identification and cross-validation

The reference embedded in the released LASI GLI fields was identified by computing GLI-2012 predicted FEV1 for each participant from age, sex, and measured height under each ethnic module and comparing with the supplied predicted values. The **South-East Asian module** reproduced the released values to a median absolute difference of 0.003 L (percent-predicted median 80.9 vs 80.9), identifying it as the equation used. Further references were computed with the open-source `pyspiro` library, validated on this dataset as follows: its GLI-2012 South-East Asian output matched the released LASI values to <0.01 L, and its Chhabra-2014 output matched an independent hand-coded implementation of the published coefficients to 0.0001 L.

### Data-quality disclosure

In the released linked file, the FEV1 and FEV1/FVC z-score fields were non-informative (zero variance across all records) and were **not** used. The FVC z-score field retained valid variation (median −1.12) and was used only for the distributional figure (manuscript Figure 3). All lower-limit-of-normal (LLN) classifications were computed from reference-specific lower-limit values, not from the z-score fields.

### Statistical detail

Prevalence used the LASI spirometry survey weight; confidence intervals were computed on the Kish effective sample size (n_eff = (Σw)²/Σw²) using the Wilson score interval. Primary-sampling-unit and stratum identifiers were not available in the analytic file, so this is a documented approximation of the design-based variance. Determinants used multinomial logistic regression (normal spirometry reference); PRISm–ageing associations used binary logistic regression adjusted for age, sex, residence, smoking, and schooling. Analyses used Python 3 (pandas, statsmodels, pyspiro).

## Supplementary Table S1. Full reference-equation comparison (analytic sample, n = 30,996)

| Reference (equation) | Definition | PRISm, % (95% CI) | RSP, % (95% CI) |
|---|---|---|---|
| GLI-2012 South-East Asian | Fixed | 40.6 (39.7–41.5) | 37.8 (37.0–38.7) |
| GLI-2012 South-East Asian | LLN | 27.6 (26.8–28.4) | 27.5 (26.7–28.3) |
| GLI-Global 2022 (race-neutral) | Fixed | 46.3 (45.4–47.2) | 46.7 (45.8–47.6) |
| GLI-Global 2022 (race-neutral) | LLN | 32.5 (31.7–33.4) | 33.7 (32.8–34.5) |
| Chhabra-2014 (northern India) | Fixed | 18.6 (17.9–19.3) | 32.9 (32.0–33.7) |
| Chhabra-2014 (northern India) | LLN | 10.8 (10.3–11.4) | 26.6 (25.9–27.4) |
| Agarwal-2020 (western India) | Fixed | 22.1 (21.3–22.8) | 27.5 (26.7–28.3) |
| Agarwal-2020 (western India) | LLN | 11.8 (11.2–12.4) | 18.8 (18.1–19.5) |
| Internal LASI healthy-subset | LLN | 3.9 (3.6–4.3) | 4.9 (4.6–5.3) |

Airflow obstruction (ratio-based) was 13.3% (fixed) and 15.4% (LLN) and is comparatively reference-insensitive.

## Supplementary Table S2. Included versus excluded participants (selection)

| Characteristic | Included (n=31,090) | Excluded (n=19,166) | Standardized difference |
|---|---|---|---|
| Age, years (mean) | 57.7 | 59.8 | −0.22 |
| Women, % | 49.0 | 58.4 | −0.19 |
| Frailty, % | 32.9 | 39.1 | −0.13 |
| Functional limitation, % | 49.5 | 56.0 | −0.13 |
| Multimorbidity (≥2), % | 16.3 | 16.5 | −0.01 |
| Diabetes, % | 12.0 | 12.3 | −0.01 |
| Chronic lung disease, % | 1.5 | 1.5 | 0.00 |
| Rural residence, % | 66.9 | 64.8 | 0.04 |

Excluded participants were older and frailer; the resulting bias moves true prevalence upward, so the reported estimates are conservative with respect to selection.

## Supplementary Table S3. Internal LASI healthy-subset reference equations

Fitted by ordinary least squares among healthy participants (never-smokers, no self-reported lung disease, BMI 18.5–24.9 kg/m²); predicted value = constant + b_age·age(years) + b_ht·height(cm); LLN = predicted − 1.645 × RMSE.

| Sex | Parameter | Constant | b_age | b_height | RMSE | n |
|---|---|---|---|---|---|---|
| Male | FVC (L) | −1.669 | −0.02207 | 0.03522 | 0.572 | 5,938 |
| Male | FEV1 (L) | −0.492 | −0.02165 | 0.02426 | 0.468 | 5,938 |
| Female | FVC (L) | −0.888 | −0.01518 | 0.02515 | 0.423 | 6,886 |
| Female | FEV1 (L) | −0.382 | −0.01426 | 0.01880 | 0.365 | 6,886 |

These are provided for transparency and reproducibility. They are illustrative rather than a gold-standard reference, because they are derived from the same field/handheld spirometry and share its measurement floor, and because "healthy" is defined from survey variables. They nonetheless bound the lower end of the plausible prevalence range and motivate deriving formally validated national reference equations.

## Supplementary Note on PRISm–RSP overlap

Under the GLI-2012 reference and fixed cut-offs, 84.3% of adults with PRISm also met the restrictive (low-FVC) criterion, confirming that preserved-ratio impairment in this population is predominantly a low-volume (restrictive) phenomenon rather than isolated FEV1 reduction. This is consistent with the reference-insensitivity of RSP relative to PRISm and with the downward shift of the whole FVC distribution (manuscript Figure 3).
