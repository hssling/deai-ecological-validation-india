# Supplementary Material

**Nationally Representative Spirometry Reference Equations for Middle-Aged and Older Indians (LASI Wave 1).**

## Supplementary Methods — how to apply the equations

Age is centred and expressed in decades: **age_c = (age in years − 60) / 10**. Height is in cm.

**Volumes (FEV1, FVC), log-normal:**
- ln(median) µ = Intercept + b·ln(height) + c₁·age_c + c₂·age_c²
- σ (log scale) = [Intercept_S + b_S·age_c] / √(2/π), where √(2/π) = 0.7979
- Median M = exp(µ);  LLN = exp(µ − 1.645·σ);  z = (ln(observed) − µ) / σ

**Ratio (FEV1/FVC), natural scale:**
- median M = Intercept + c₁·age_c + c₂·age_c²
- σ = [Intercept_S + b_S·age_c] / √(2/π)
- LLN = M − 1.645·σ;  z = (observed − M) / σ

**Worked example (man, 60 years, 165 cm, FEV1):**
µ = −8.5450 + 1.8207·ln(165) + (−0.1051)·0 + (−0.0058)·0² = −8.5450 + 9.298 = 0.753.
σ = (0.1848 + 0.0144·0)/0.7979 = 0.2316. Median = e^0.753 = **2.12 L**;
LLN = e^(0.753 − 1.645·0.2316) = **1.45 L** (cf. lookup Table, matches).

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

## Supplementary Table S2. Internal validation — held-out z-scores by age band

| Sex | Parameter | Age band | n | Mean z | SD z |
|---|---|---|---|---|---|
| Men | FEV1 | 45–54 | 838 | −0.03 | 1.08 |
| Men | FEV1 | 55–64 | 626 | −0.03 | 1.05 |
| Men | FEV1 | 65–74 | 436 | −0.05 | 1.01 |
| Men | FEV1 | ≥75 | 149 | −0.04 | 0.96 |
| Men | FVC | 45–54 | 838 | −0.04 | 1.07 |
| Men | FVC | 55–64 | 626 | −0.04 | 1.05 |
| Men | FVC | 65–74 | 436 | −0.08 | 1.04 |
| Men | FVC | ≥75 | 149 | −0.06 | 0.98 |
| Women | FEV1 | 45–54 | 1,313 | −0.04 | 1.03 |
| Women | FEV1 | 55–64 | 926 | 0.04 | 1.01 |
| Women | FEV1 | 65–74 | 448 | −0.10 | 1.03 |
| Women | FEV1 | ≥75 | 125 | 0.02 | 0.88 |
| Women | FVC | 45–54 | 1,313 | −0.04 | 1.04 |
| Women | FVC | 55–64 | 926 | 0.02 | 1.02 |
| Women | FVC | 65–74 | 448 | −0.08 | 1.00 |
| Women | FVC | ≥75 | 125 | −0.05 | 0.93 |

## Supplementary Table S3. Reference equation coefficients

Median model: µ = Intercept + b_lnht·ln(height) + c₁·age_c + c₂·age_c² (age_c in decades, centred at 60). Scatter model: |residual| = Intercept_S + b_S·age_c; σ = fitted/0.7979.

| Sex | Parameter | Scale | Intercept | ln(height) | age_c | age_c² | Scatter Int | Scatter age_c |
|---|---|---|---|---|---|---|---|---|
| Men | FEV1 | log | −8.5450 | 1.8207 | −0.1051 | −0.0058 | 0.1848 | 0.0144 |
| Men | FVC | log | −9.2434 | 2.0059 | −0.0834 | −0.0064 | 0.1738 | 0.0081 |
| Men | FEV1/FVC | linear | 78.8086 | — | −1.5054 | 0.0844 | 6.1925 | 0.7545 |
| Women | FEV1 | log | −9.0624 | 1.8921 | −0.0963 | −0.0083 | 0.1906 | 0.0126 |
| Women | FVC | log | −9.2585 | 1.9767 | −0.0828 | −0.0108 | 0.1750 | 0.0085 |
| Women | FEV1/FVC | linear | 80.0212 | — | −0.9569 | 0.2190 | 5.9803 | 0.5299 |

## Supplementary Table S4. Full lookup table — predicted median and LLN (litres) by age and height

| Sex | Age | Height (cm) | FEV1 median | FEV1 LLN | FVC median | FVC LLN |
|---|---|---|---|---|---|---|
| Men | 50 | 155 | 2.09 | 1.47 | 2.58 | 1.83 |
| Men | 60 | 155 | 1.89 | 1.29 | 2.39 | 1.68 |
| Men | 70 | 155 | 1.69 | 1.12 | 2.19 | 1.51 |
| Men | 80 | 155 | 1.50 | 0.95 | 1.98 | 1.31 |
| Men | 50 | 160 | 2.21 | 1.55 | 2.75 | 1.95 |
| Men | 60 | 160 | 2.00 | 1.37 | 2.55 | 1.79 |
| Men | 70 | 160 | 1.80 | 1.19 | 2.33 | 1.61 |
| Men | 80 | 160 | 1.59 | 1.01 | 2.11 | 1.40 |
| Men | 50 | 165 | 2.34 | 1.64 | 2.93 | 2.07 |
| Men | 60 | 165 | 2.12 | 1.45 | 2.71 | 1.90 |
| Men | 70 | 165 | 1.90 | 1.26 | 2.48 | 1.71 |
| Men | 80 | 165 | 1.68 | 1.07 | 2.24 | 1.49 |
| Men | 50 | 170 | 2.47 | 1.73 | 3.11 | 2.20 |
| Men | 60 | 170 | 2.24 | 1.53 | 2.88 | 2.02 |
| Men | 70 | 170 | 2.01 | 1.33 | 2.64 | 1.82 |
| Men | 80 | 170 | 1.77 | 1.13 | 2.38 | 1.58 |
| Men | 50 | 175 | 2.61 | 1.83 | 3.30 | 2.33 |
| Men | 60 | 175 | 2.36 | 1.61 | 3.05 | 2.14 |
| Men | 70 | 175 | 2.11 | 1.40 | 2.79 | 1.92 |
| Men | 80 | 175 | 1.87 | 1.19 | 2.52 | 1.68 |
| Women | 50 | 145 | 1.55 | 1.07 | 1.91 | 1.35 |
| Women | 60 | 145 | 1.42 | 0.96 | 1.78 | 1.25 |
| Women | 70 | 145 | 1.28 | 0.85 | 1.63 | 1.11 |
| Women | 80 | 145 | 1.13 | 0.72 | 1.44 | 0.95 |
| Women | 50 | 150 | 1.66 | 1.14 | 2.05 | 1.44 |
| Women | 60 | 150 | 1.52 | 1.03 | 1.91 | 1.33 |
| Women | 70 | 150 | 1.37 | 0.90 | 1.74 | 1.19 |
| Women | 80 | 150 | 1.21 | 0.77 | 1.54 | 1.01 |
| Women | 50 | 155 | 1.76 | 1.22 | 2.18 | 1.54 |
| Women | 60 | 155 | 1.62 | 1.09 | 2.04 | 1.42 |
| Women | 70 | 155 | 1.46 | 0.96 | 1.86 | 1.27 |
| Women | 80 | 155 | 1.29 | 0.82 | 1.65 | 1.08 |
| Women | 50 | 160 | 1.87 | 1.29 | 2.33 | 1.64 |
| Women | 60 | 160 | 1.72 | 1.16 | 2.17 | 1.51 |
| Women | 70 | 160 | 1.55 | 1.02 | 1.98 | 1.35 |
| Women | 80 | 160 | 1.37 | 0.87 | 1.75 | 1.15 |
| Women | 50 | 165 | 1.98 | 1.37 | 2.47 | 1.74 |
| Women | 60 | 165 | 1.82 | 1.23 | 2.30 | 1.61 |
| Women | 70 | 165 | 1.64 | 1.08 | 2.10 | 1.44 |
| Women | 80 | 165 | 1.45 | 0.92 | 1.86 | 1.23 |

Intermediate ages/heights are obtained from the equations (Supplementary Table S3).
