# Supplementary Material

**Nationally Representative Spirometry Reference Equations for Middle-Aged and Older Indians (LASI Wave 1).**

## Supplementary Methods — how to apply the equations (GAMLSS / LMS)

The reference is a GAMLSS Box-Cox Cole-Green (BCCG) / LMS model. For each sex and parameter it provides three age-specific values: **L** (Box-Cox skewness), **M** (median), and **S** (coefficient of variation), tabulated in Supplementary Table S2. For the volumes (FEV1, FVC), the median depends on height multiplicatively through a fitted exponent *b*:

- **M(age, height) = M_ref(age) × (height / reference height)^b**, where M_ref(age) is the tabulated median at the sex-specific reference height (men 162.5 cm, women 150.6 cm) and *b* is the height exponent (Table S2). For the FEV1/FVC ratio there is no height term.
- **z-score** = [ (observed / M)^L − 1 ] / (L × S)   (for L ≠ 0)
- **LLN (5th centile)** = M × (1 + L × S × (−1.645))^(1/L)

**Worked example (man, 60 years, 165 cm, FVC):** from Table S2, L = 1.017, M_ref = 2.696 L (at 162.5 cm), S = 0.208, b = 2.038. Median at 165 cm = 2.696 × (165/162.5)^2.038 = **2.78 L**. LLN = 2.78 × (1 + 1.017×0.208×(−1.645))^(1/1.017) = **1.83 L** (matches Supplementary Table S3).

## Supplementary Table S1. Reference (healthy) population by sex and age band — median lung volumes

| Sex | Age band | n | Height, cm | FEV1, L | FVC, L |
|---|---|---|---|---|---|
| Men | 45–54 | 4,284 | 163.3 | 2.37 | 2.96 |
| Men | 55–64 | 3,095 | 162.4 | 2.13 | 2.70 |
| Men | 65–74 | 2,173 | 162.1 | 1.93 | 2.46 |
| Men | ≥75 | 689 | 160.0 | 1.65 | 2.16 |
| Women | 45–54 | 6,455 | 151.5 | 1.73 | 2.13 |
| Women | 55–64 | 4,716 | 150.2 | 1.58 | 1.97 |
| Women | 65–74 | 2,331 | 149.3 | 1.42 | 1.78 |
| Women | ≥75 | 557 | 148.2 | 1.26 | 1.54 |

Values are medians. Numbers thin beyond age 75, where equation confidence is correspondingly lower.

## Supplementary Table S2. GAMLSS reference values (L, M, S) by age at the sex-specific reference height

Reference height: men 162.5 cm, women 150.6 cm. Height exponent *b* (for M scaling): FVC 2.038 (men) / 2.014 (women); FEV1 1.816 (men) / 1.920 (women); ratio has no height term. M for FEV1/FVC is in per-cent.

| Parameter | Sex | Age | L | M | S |
|---|---|---|---|---|---|
| FVC | Men | 50 | 1.084 | 2.911 | 0.201 |
| FVC | Men | 60 | 1.017 | 2.696 | 0.208 |
| FVC | Men | 70 | 0.950 | 2.460 | 0.219 |
| FVC | Men | 80 | 0.884 | 2.237 | 0.232 |
| FVC | Women | 50 | 0.766 | 2.096 | 0.206 |
| FVC | Women | 60 | 0.921 | 1.970 | 0.209 |
| FVC | Women | 70 | 1.075 | 1.797 | 0.217 |
| FVC | Women | 80 | 1.229 | 1.616 | 0.224 |
| FEV1 | Men | 50 | 1.182 | 2.341 | 0.206 |
| FEV1 | Men | 60 | 1.113 | 2.128 | 0.221 |
| FEV1 | Men | 70 | 1.044 | 1.900 | 0.237 |
| FEV1 | Men | 80 | 0.974 | 1.695 | 0.253 |
| FEV1 | Women | 50 | 0.800 | 1.702 | 0.220 |
| FEV1 | Women | 60 | 0.971 | 1.578 | 0.228 |
| FEV1 | Women | 70 | 1.142 | 1.423 | 0.235 |
| FEV1 | Women | 80 | 1.313 | 1.279 | 0.243 |
| FEV1/FVC | Men | 50 | 2.675 | 80.95 | 0.087 |
| FEV1/FVC | Men | 60 | 2.592 | 79.52 | 0.098 |
| FEV1/FVC | Men | 70 | 2.509 | 78.16 | 0.110 |
| FEV1/FVC | Men | 80 | 2.426 | 76.91 | 0.124 |
| FEV1/FVC | Women | 50 | 2.344 | 81.62 | 0.087 |
| FEV1/FVC | Women | 60 | 2.244 | 80.57 | 0.094 |
| FEV1/FVC | Women | 70 | 2.144 | 79.66 | 0.104 |
| FEV1/FVC | Women | 80 | 2.043 | 79.73 | 0.115 |

Full single-year L, M, S curves (ages 45–90) accompany the analysis code.

## Supplementary Table S3. Full lookup table — predicted median and LLN (litres) by age and height (GAMLSS reference)

| Sex | Age | Height (cm) | FEV1 median | FEV1 LLN | FVC median | FVC LLN |
|---|---|---|---|---|---|---|
| Men | 50 | 155 | 2.15 | 1.39 | 2.64 | 1.76 |
| Men | 60 | 155 | 1.95 | 1.23 | 2.45 | 1.61 |
| Men | 70 | 155 | 1.74 | 1.06 | 2.23 | 1.44 |
| Men | 80 | 155 | 1.56 | 0.91 | 2.03 | 1.28 |
| Men | 50 | 160 | 2.28 | 1.48 | 2.82 | 1.87 |
| Men | 60 | 160 | 2.07 | 1.30 | 2.61 | 1.71 |
| Men | 70 | 160 | 1.85 | 1.12 | 2.38 | 1.53 |
| Men | 80 | 160 | 1.65 | 0.97 | 2.17 | 1.36 |
| Men | 50 | 165 | 2.41 | 1.56 | 3.00 | 2.00 |
| Men | 60 | 165 | 2.19 | 1.37 | 2.78 | 1.83 |
| Men | 70 | 165 | 1.95 | 1.19 | 2.54 | 1.63 |
| Men | 80 | 165 | 1.74 | 1.02 | 2.31 | 1.45 |
| Men | 50 | 170 | 2.54 | 1.65 | 3.19 | 2.12 |
| Men | 60 | 170 | 2.31 | 1.45 | 2.96 | 1.94 |
| Men | 70 | 170 | 2.06 | 1.25 | 2.70 | 1.73 |
| Men | 80 | 170 | 1.84 | 1.08 | 2.45 | 1.54 |
| Men | 50 | 175 | 2.68 | 1.74 | 3.39 | 2.25 |
| Men | 60 | 175 | 2.44 | 1.53 | 3.14 | 2.06 |
| Men | 70 | 175 | 2.17 | 1.32 | 2.86 | 1.84 |
| Men | 80 | 175 | 1.94 | 1.14 | 2.60 | 1.64 |
| Women | 50 | 145 | 1.58 | 1.03 | 1.94 | 1.31 |
| Women | 60 | 145 | 1.47 | 0.92 | 1.82 | 1.21 |
| Women | 70 | 145 | 1.32 | 0.79 | 1.66 | 1.06 |
| Women | 80 | 145 | 1.19 | 0.67 | 1.50 | 0.92 |
| Women | 50 | 150 | 1.69 | 1.10 | 2.08 | 1.40 |
| Women | 60 | 150 | 1.57 | 0.98 | 1.95 | 1.29 |
| Women | 70 | 150 | 1.41 | 0.85 | 1.78 | 1.14 |
| Women | 80 | 150 | 1.27 | 0.72 | 1.60 | 0.98 |
| Women | 50 | 155 | 1.80 | 1.17 | 2.22 | 1.50 |
| Women | 60 | 155 | 1.67 | 1.05 | 2.09 | 1.38 |
| Women | 70 | 155 | 1.50 | 0.90 | 1.90 | 1.21 |
| Women | 80 | 155 | 1.35 | 0.77 | 1.71 | 1.05 |
| Women | 50 | 160 | 1.91 | 1.25 | 2.37 | 1.60 |
| Women | 60 | 160 | 1.77 | 1.11 | 2.23 | 1.47 |
| Women | 70 | 160 | 1.60 | 0.96 | 2.03 | 1.29 |
| Women | 80 | 160 | 1.44 | 0.81 | 1.83 | 1.12 |
| Women | 50 | 165 | 2.03 | 1.32 | 2.52 | 1.70 |
| Women | 60 | 165 | 1.88 | 1.18 | 2.37 | 1.57 |
| Women | 70 | 165 | 1.70 | 1.02 | 2.16 | 1.38 |
| Women | 80 | 165 | 1.52 | 0.86 | 1.94 | 1.19 |

Intermediate ages and heights are obtained from the L, M, S values (Supplementary Table S2) via the formulae above.

## Supplementary Note — method and validation

Models were fitted in R (`gamlss`, BCCGo family) with penalized B-splines `pb()` for the L, M, and S curves in age, and log-height as a linear term in the median for volumes. A simpler quadratic-in-age, log-normal (L fixed) parameterization implemented in Python gave concordant estimates (PRISm 11.9% fixed / 5.3% LLN versus the GAMLSS 13.8% / 4.0%), confirming the burden re-estimation is not an artefact of the modelling choice. Held-out validation (main Table 3) gave z-score means within ±0.05 and standard deviations 0.98–1.01 for all six sex × parameter combinations.
