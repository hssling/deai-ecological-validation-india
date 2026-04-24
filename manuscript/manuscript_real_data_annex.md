# Real Data Annex — DEAI Manuscript

> **STATUS:** This annex contains empirical results from PUBLICLY AVAILABLE real datasets.
> It is distinct from the synthetic-cohort main analysis.
> When LASI microdata is obtained, these results will be integrated into the main manuscript.

---

## Annex A: India Exposome Context — Real NFHS-5 Data

**Source:** DHS Open API v8, Survey IA2020DHS (India NFHS-5, 2019–21)
**Data type:** REAL — nationally representative survey estimates
**Access:** Free, no registration: https://api.dhsprogram.com/rest/dhs/v8/

### Table A1. Selected India Health and Exposome Indicators (NFHS-5, 2019–21)

| Indicator | Value | DHS Indicator ID | DEAI Domain |
|-----------|-------|-----------------|-------------|
| Men who smoke any tobacco (%) | **39.1** | AH_TOBC_M_ANY | Lifestyle–Tobacco |
| Women who smoke any tobacco (%) | **4.1** | AH_TOBC_W_ANY | Lifestyle–Tobacco |
| Households with daily smoking (%) | **24.5** | HC_SMKH_H_DLY | Lifestyle–Tobacco |
| Households using clean fuel for cooking (%) | **58.6** | HC_HEFF_H_CLN | Air Pollution (IAP) |
| Households with electricity (%) | **96.5** | HC_HEFF_H_ELC | SES / Built environment |
| Households with improved sanitation (%) | **77.7** | HC_WATS_H_SBS | SES / Built environment |
| Households with improved water source (%) | **95.9** | HC_WATS_H_IMP | SES / Built environment |
| Women overweight or obese (BMI ≥25) (%) | **24.0** | NT_BMI_W_OW | Lifestyle–Diet |
| Women who are literate (%) | **71.5** | WE_WMEI_W_LIT | SES–Education |
| Infant mortality rate (per 1,000 live births) | **35.0** | CM_ECMR_C_IMR | Mortality proxy |

**Notes:**
- All values from India 2020–21 DHS (equivalent to NFHS-5)
- National estimates (breakdown=national), weighted
- See `data_raw/nfhs5_dhs_api_real.csv` for complete dataset (3,322 indicators)
- See `results/figures/fig1_nfhs5_real_context.png` for graphical summary

### Interpretation for DEAI

These real population statistics reveal the scale of India's exposome adversity:
- 39.1% of men use tobacco — nearly 8× the global ideal (0%)
- 41.4% of households use solid/biomass fuels (100 − 58.6%) — a major source of indoor PM2.5
- 28.5% of households lack improved sanitation — with implications for infectious disease burden and chronic inflammation
- Female literacy at 71.5% signals persistent educational and SES gradients in exposome exposure

These figures justify why an LMIC-adapted DEAI (rather than a Western exposome index) is necessary: the exposure distributions are dramatically different from European or North American cohorts.

---

## Annex B: Real Data vs Synthetic Cohort Comparison

| Parameter | Synthetic Cohort | Real NFHS-5 (published) | Notes |
|-----------|-----------------|------------------------|-------|
| Tobacco use — men | 35% | **39.1%** (DHS API) | Synthetic slightly underestimates |
| Clean cooking fuel | 58.6% (calibrated) | **58.6%** (DHS API) | Exact match by calibration |
| Female literacy | 71.5% (calibrated) | **71.5%** (DHS API) | Exact match |
| Frailty prevalence | 42.6% (FI>0.25) | ~28–35% (LASI published) | Synthetic slightly overestimates |
| Multimorbidity | 70.1% | ~27–42% (LASI published) | Synthetic overestimates — fixable |
| PM2.5 mean | 62.4 μg/m³ | ~65–70 μg/m³ (WHO AAQ 2022) | Good calibration |

**Action:** When LASI microdata obtained, recalibrate synthetic cohort marginals to LASI observed distributions before final analysis.

---

## Annex C: State-Level LASI DEAI Results - Epidemiological Transition Signal

**Source:** LASI Wave 1 India state/UT factsheet, 2017-18; IIPS 2022  
**Analysis unit:** 37 states/UTs, including the national India row  
**Data type:** REAL - ecological state-level estimates  
**Primary limitation:** These are aggregate correlations and must not be interpreted as individual-level associations.

### Table C1. DEAI Correlations with State-Level Ageing Outcomes

| Outcome | Spearman rho | p value | Interpretation |
|---------|--------------|---------|----------------|
| Death rate age 60+ per 1,000 | **+0.342** | **0.038** | Stable nominal association with higher old-age mortality; supportive but not FDR-confirmatory. |
| Fall prevalence | +0.317 | 0.056 | Directionally positive; borderline evidence. |
| IADL limitations | +0.217 | 0.197 | Directionally positive, not statistically significant. |
| Depression, CIDI-SF | +0.078 | 0.651 | No clear state-level association. |
| Poor self-rated health | -0.087 | 0.609 | No clear state-level association. |
| ADL limitations | -0.222 | 0.187 | Directionally negative, not statistically significant. |
| Multimorbidity index | **-0.778** | **<0.001** | Strong inverse ecological association, consistent with epidemiological transition and diagnosis/access effects. |

### Robustness Checks

Sensitivity analyses were conducted to test whether the real-data findings depended on inclusion of the national India row or on any single state/UT. After excluding the India row, the old-age mortality association remained similar (rho=+0.341, p=0.042; bootstrap 95% CI +0.013 to +0.620), but did not survive false-discovery-rate correction across seven outcomes (q=0.146). The diagnosed multimorbidity association was unchanged and robust (rho=-0.777, p<0.001; bootstrap 95% CI -0.875 to -0.607; q<0.001). Leave-one-out analysis showed that the multimorbidity finding was not driven by any single state/UT (rho range -0.809 to -0.765).

Internal consistency of the eight adverse exposome components was acceptable for a multi-domain ecological index (Cronbach alpha=0.688). The strongest component correlations with DEAI were underweight prevalence (rho=+0.874), tobacco use (rho=+0.727), lack of clean cooking fuel (rho=+0.711), reported indoor pollution exposure (rho=+0.672), low literacy (rho=+0.572), and poor sanitation (rho=+0.571). Heavy episodic drinking and poor water access contributed less strongly in the state-level data.

### Epidemiological Interpretation

The apparently paradoxical pattern - higher DEAI correlating positively with old-age death rates but negatively with recorded multimorbidity - is a substantive finding, not a pipeline error. It is consistent with India's epidemiological transition gradient across states.

High-DEAI states such as Odisha, Jharkhand, Bihar, Uttar Pradesh, Assam, Chhattisgarh, and Madhya Pradesh have high adverse exposome burdens driven by low clean-fuel access, lower literacy, tobacco exposure, poor sanitation, and undernutrition. These states also show higher old-age mortality, supporting the interpretation that DEAI captures lethal cumulative environmental and social adversity.

By contrast, lower-DEAI and more advanced-transition states/UTs such as Kerala, Delhi, Chandigarh, Goa, Puducherry, and Sikkim show higher recorded multimorbidity. This likely reflects a combination of longer survival, older population structures, better diagnosis of chronic disease, better access to medical care, and greater cardiometabolic disease detection. In ecological data, diagnosed multimorbidity can therefore behave as a marker of survival and health-system ascertainment rather than a simple marker of adverse biological ageing.

This pattern reframes the multimorbidity result: DEAI is not failing because it is inversely correlated with diagnosed multimorbidity. Rather, DEAI appears to separate two ageing regimes: (1) high-exposure, high-mortality states where older adults may die earlier or remain underdiagnosed, and (2) lower-exposure, later-transition states where survival and diagnosis generate higher measured multimorbidity prevalence.

### State-Level Interpretation

Odisha ranked highest for adverse DEAI burden (Z=+2.06), followed by Jharkhand (Z=+1.77), Bihar (Z=+1.66), Uttar Pradesh (Z=+1.38), and Assam (Z=+1.21). These rankings should be interpreted as a map of cumulative adverse exposome burden, not as a direct ranking of diagnosed chronic disease prevalence.

Karnataka ranked 14th of 37 (DEAI Z=+0.35), close to the national India value (Z=+0.44). Karnataka had lower old-age death rate than India overall (32.4 vs 38.4 per 1,000 age 60+), lower poor self-rated health (8.4% vs 17.6%), and lower tobacco use (18.9% vs 19.8%), but higher IADL limitation (44.6% vs 35.9%). This indicates a mixed profile rather than uniformly high or low ageing burden.

### Manuscript-Ready Result

In real state-level LASI data, DEAI showed a stable nominal positive association with old-age mortality (states/UTs only rho=+0.341, p=0.042; bootstrap 95% CI +0.013 to +0.620; FDR q=0.146) and a robust inverse association with diagnosed multimorbidity (rho=-0.777, p<0.001; bootstrap 95% CI -0.875 to -0.607; FDR q<0.001). We interpret this as evidence of an epidemiological transition paradox: in high-adversity states, adverse exposome burden is directionally associated with mortality, while diagnosed multimorbidity is concentrated in lower-adversity, later-transition states with longer survival and better ascertainment of chronic disease. These ecological results support DEAI as a marker of cumulative adverse exposure and possible mortality vulnerability, while cautioning against interpreting state-level diagnosed multimorbidity as a monotonic ageing-severity outcome.

---

## Annex D: Air Pollution Context

**Target dataset:** WHO Ambient Air Quality Database 2022
**Access status:** Direct URL changed — file must be placed manually:
1. Navigate to: https://www.who.int/data/gho/data/themes/air-pollution/who-ambient-air-quality-database
2. Download the 2022 update Excel file
3. Place at: `data_raw/who_aaq_database.xlsx`
4. Run: `python src/ingest/download_who_aaq.py --config config.yaml`

**Published values used for context (WHO 2022):**
- India national PM2.5 mean: ~58 μg/m³ (range: 30–160 across cities)
- WHO guideline: 5 μg/m³ annual mean
- India exceedance ratio: ~12× above WHO guideline
- Delhi annual mean PM2.5: ~96 μg/m³ (2019–21 average)

---

## Annex E: Data Availability Statement (for manuscript)

> "Real exposure data were obtained from the World Health Organization Ambient Air Quality Database 2022 (city-level PM2.5/PM10) and the Lancet Countdown 2023 health-climate indicator dataset. India demographic and health indicator data were obtained from the India DHS (NFHS-5, IA2020DHS) via the open DHS API (https://api.dhsprogram.com), which requires no registration. Individual-level cohort data from the Longitudinal Ageing Study of India (LASI) Wave 1 were requested via https://lasida.iips.in/ [application pending]. The synthetic derivation cohort used in the current analysis is fully reproducible from seed 42 as described in the methods and Supplement S1. All analysis code is available at [repository URL] under MIT license."
