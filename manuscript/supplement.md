# Supplementary Material

**Title:** Digital Exposome Aging Index (DEAI): A Multi-Domain Composite Score for Predicting Accelerated Biological Ageing in Population Settings

---

## S1. Synthetic Cohort Construction

The current analysis uses a synthetic derivation cohort (N=5,000) constructed to enable full pipeline testing prior to acquisition of LASI or NFHS-5 microdata. Marginal distributions for all variables were calibrated to published population statistics from:

- **Age/sex distribution:** LASI Wave 1 (Longitudinal Ageing Study of India, 2017–18)
- **PM2.5 exposure:** WHO Ambient Air Quality Database 2022, India urban mean 62.4 μg/m³
- **Tobacco prevalence:** NFHS-5 national report (men 38%; women 10%)
- **SES distribution:** NFHS-5 asset quintile distribution
- **Frailty prevalence:** Singh et al. (2022) frailty in Indian elderly, ~28%
- **Multimorbidity:** Arokiasamy et al. (2015) India multimorbidity, ~27%

**All synthetic outputs are labeled with `synthetic_flag=True`** in all output files.

The synthetic cohort will be replaced with LASI Wave 1 microdata upon approval of the data access application submitted to https://lasida.iips.in/.

---

## S2. Data Sources — Extended Table

| Dataset | URL | Variables Used | Access |
|---------|-----|----------------|--------|
| WHO AAQ 2022 | who.int/data/gho | PM2.5, PM10, city | Free |
| Lancet Countdown 2023 | lancetcountdown.org | Heat days, mortality | Free (Figshare) |
| GEO GSE65765 | ncbi.nlm.nih.gov/geo | RNA-seq, whole blood | Free |
| GEO GSE40279 | ncbi.nlm.nih.gov/geo | Methylation, multi-tissue | Free |
| GEO GSE30272 | ncbi.nlm.nih.gov/geo | RNA-seq, brain cortex | Free |
| NFHS-5 (aggregate) | iipsindia.ac.in | Nutrition, SES, tobacco | Free |

---

## S3. DEAI Method Details

### S3.1 Knowledge Weights

Weights were assigned based on effect sizes from published meta-analyses:

| Domain | Weight | Evidence source |
|--------|--------|----------------|
| Air pollution (PM2.5) | 0.20 | Chen et al. Lancet 2017; Landrigan et al. Lancet 2018 |
| Tobacco | 0.18 | GBD 2021 risk factors |
| Diet diversity | 0.15 | WHO/FAO dietary diversity evidence |
| Heat stress | 0.12 | Lancet Countdown 2023 |
| SES quintile | 0.12 | Marmot Review; CSDH 2008 |
| Education | 0.08 | Stringhini et al. Lancet 2017 |
| Alcohol | 0.08 | GBD 2021 |
| Urban/rural | 0.07 | Marmot et al. 2020 |

### S3.2 Elastic-Net Hyperparameters

l1_ratio selected from {0.1, 0.5, 0.7, 0.9, 0.95, 1.0} by 5-fold CV; alpha by 100-point grid. Final model parameters reported in `results/tables/deai_versions_comparison.csv`.

### S3.3 XGBoost Hyperparameters

| Parameter | Value |
|-----------|-------|
| n_estimators | 300 |
| max_depth | 4 |
| learning_rate | 0.05 |
| subsample | 0.8 |
| colsample_bytree | 0.8 |
| random_state | 42 |

---

## S4. Sensitivity Analyses

### S4.1 VIF Results
[Table populated from `results/tables/vif_results.csv` after pipeline run]

### S4.2 Subgroup AUC
[Table populated from `results/tables/subgroup_auc.csv` after pipeline run]

### S4.3 Negative Control
[Results from `results/tables/sensitivity_results.csv` — expected AUC ≈ 0.50]

### S4.4 Frailty Threshold Sensitivity
[To be populated — FI thresholds 0.20, 0.25, 0.30]

---

## S5. TRIPOD Checklist

| Item | Section |
|------|---------|
| Title identifying prediction model development | Title |
| Abstract summary of objectives and methods | Abstract |
| Source of data | Methods 2.1 |
| Eligible participants and setting | Methods 2.1 |
| Outcomes | Methods 2.3 |
| Candidate predictors | Methods 2.2 |
| Sample size | Methods 2.1 |
| Missing data handling | Methods 2.7 (SAP Section 6.2) |
| Statistical analysis | Methods 2.5 |
| Development results | Results 3.3 |
| Model performance | Results 3.3, Table 3 |
| Limitations | Discussion 4.2 |
| Interpretation | Discussion |
| Supplementary information | This supplement |

---

## S6. Reproducibility Checklist

- [ ] `environment.yml` conda environment pins all package versions
- [ ] `config.yaml` controls all paths, seeds, and hyperparameters
- [ ] `Makefile` provides single-command phase execution
- [ ] All random operations use `seed=42`
- [ ] No hardcoded paths in any script
- [ ] Synthetic cohort reproducible from seed
- [ ] All intermediate datasets saved to `data_processed/`
- [ ] All figures at 300 DPI
- [ ] `logs/progress.md` tracks each phase
