# Phenotype and Variable Definitions

**DEAI Pipeline — Exposome, Outcome, and Covariate Definitions**
Last updated: 2026-04-22

---

## A. Exposome Variables

### Air Pollution Domain
| Variable | Source | Coding | Units | Transform |
|----------|--------|--------|-------|-----------|
| `pm25_annual_ugm3` | WHO AAQ 2022 / synthetic | Annual mean PM2.5 | μg/m³ | log1p |
| *Reference threshold* | WHO guideline 2021: 5 μg/m³ annual mean | | | |

### Heat / Climate Domain
| Variable | Source | Coding | Units | Transform |
|----------|--------|--------|-------|-----------|
| `heat_days_per_year` | Lancet Countdown / synthetic | Days with max temp >35°C or WBGT >28°C | Days/year | sqrt |

### Lifestyle — Tobacco
| Variable | Source | Coding | Units | Transform |
|----------|--------|--------|-------|-----------|
| `tobacco_ever` | NFHS-5 / synthetic | Ever used tobacco (any form) | Binary (0/1) | none |

### Lifestyle — Alcohol
| Variable | Source | Coding | Units | Transform |
|----------|--------|--------|-------|-----------|
| `alcohol_ever` | NFHS-5 / synthetic | Ever consumed alcohol | Binary (0/1) | none |

### Lifestyle — Diet
| Variable | Source | Coding | Units | Transform |
|----------|--------|--------|-------|-----------|
| `diet_diversity_score` | Derived / synthetic | Count of food groups consumed in 24h | 1–9 scale | none |
| *Reference* | WHO/FAO Minimum Dietary Diversity (≥5 groups) | | | |

### Built Environment
| Variable | Source | Coding | Units | Transform |
|----------|--------|--------|-------|-----------|
| `urban_rural` | NFHS-5 / synthetic | Rural = 1, Urban = 0 | Binary | none |

---

## B. Ageing-Related Outcome Variables

### Primary Outcomes

#### Frailty Index
- **Definition:** Rockwood-style deficit accumulation across 30 health items
- **Formula:** FI = (number of deficits present) / (total items assessed)
- **Threshold:** FI > 0.25 = frail (Rockwood & Mitnitski 2007)
- **Variable:** `frailty_index` (continuous 0–1), `frailty_index_binary` (FI > 0.25)
- **In synthetic cohort:** Derived from age, PM2.5, heat, tobacco, SES, diet with noise

#### Multimorbidity
- **Definition:** Presence of ≥2 concurrent chronic conditions
- **Conditions included:** Hypertension, diabetes, heart disease, stroke, COPD, arthritis, depression, cancer, kidney disease, vision/hearing impairment
- **Variable:** `multimorbidity_binary` (n_chronic_conditions ≥ 2)

#### Disability / ADL
- **Definition:** ≥1 difficulty in Activities of Daily Living (bathing, dressing, eating, toileting, transferring, continence)
- **Variable:** `disability_binary` (adl_difficulty_count ≥ 1)

#### Self-Rated Health (Poor)
- **Definition:** Response of 4 or 5 on 5-point scale (1=excellent, 5=poor)
- **Variable:** `srh_poor_binary`
- **Validation:** Self-rated health predicts mortality independently (Idler & Benyamini 1997)

### Secondary Outcomes

#### 5-Year Mortality Risk
- **Definition:** Modelled probability of death within 5 years
- **Variable:** `mortality_5yr_binary`
- **Note:** In synthetic cohort, derived from frailty and age; in real data, use administrative records or recall data

---

## C. Covariates

| Variable | Coding | Notes |
|----------|--------|-------|
| `age_years` | Continuous, years | Primary confounder |
| `sex` | 0=female, 1=male | Effect modifier for grip/gait |
| `education_years` | Continuous, 0–20 | Proxy for health literacy |
| `ses_quintile` | 1 (lowest) to 5 (highest) | Based on household assets |
| `region` | Categorical (north/south/east/west/central) | Geographic confounder |
| `tobacco_ever` | Binary | Both covariate and exposome variable depending on model |
| `alcohol_ever` | Binary | As above |

---

## D. DEAI Score Versions

| Version | Method | Use |
|---------|--------|-----|
| `deai_knowledge_weighted` | Weighted sum using published effect sizes | Clinical intuition check |
| `deai_pca` | PC1 of standardized exposome | Data-driven reference |
| `deai_elastic_net` | ElasticNet predicted frailty | Sparse, interpretable |
| `deai_xgboost` | XGBoost predicted frailty (Z-scaled) | Primary DEAI score |
| `deai_age_acceleration` | XGBoost DEAI − age-predicted DEAI | Ageing acceleration analogue |

---

## E. Missing Data Strategy

1. **Continuous variables:** Multiple imputation by chained equations (MICE) using `sklearn.impute.IterativeImputer`; complete-case analysis as sensitivity
2. **Binary variables:** Mode imputation; sensitivity analysis with missing-as-category
3. **Report:** Missing-data table in supplement (missingno visualization)
4. **Threshold:** Variables with >40% missing dropped from primary analysis; reported in sensitivity
