# Statistical Analysis Plan (SAP)

**Study:** Digital Exposome Aging Index (DEAI) — Prediction of Accelerated Ageing
**Version:** 1.0 | **Date:** 2026-04-22

---

## 1. Study Design
Cross-sectional prediction study using a composite multi-domain exposome index to predict accelerated ageing-related outcomes.

## 2. Primary Hypothesis
DEAI (Age + DEAI model, M3) achieves higher AUC than chronological age alone (M0) for frailty prediction (H1, H2).

## 3. Sample Size
- Synthetic cohort: N=5,000 (placeholder)
- Target for real data: N≥3,000 with ≥300 frailty events (event fraction ≥10%)
- Power: 90% power to detect ΔAUC≥0.05 at α=0.05 (two-sided) per Hanley & McNeil 1983

## 4. Primary Analysis

### 4.1 Model Sequence
All models evaluated by 5-fold stratified cross-validation:
- **M0:** Logistic regression — age only (baseline)
- **M1:** Logistic regression — age + sex + education + SES + tobacco + alcohol
- **M2:** Logistic regression — DEAI (primary XGBoost version) only
- **M3:** Logistic regression — age + DEAI (primary comparison)
- **M4:** XGBoost — all features (upper-bound reference)

### 4.2 Primary Outcome
Binary frailty (FI > 0.25); secondary outcomes: multimorbidity, disability, poor SRH, 5-yr mortality

### 4.3 Performance Metrics
| Metric | Threshold for clinical relevance |
|--------|----------------------------------|
| AUC (c-statistic) | M3 AUC ≥ M0 + 0.05 |
| Average Precision | Report for all models |
| Brier Score | Lower is better; report calibration plot |
| Continuous NRI | M3 vs M0; p-value reported |
| Decision Curve | Net benefit across risk thresholds |

## 5. Secondary Analyses

### 5.1 Subgroup AUC
- Sex (female vs male)
- Age strata (40–54, 55–69, 70+)
- SES (bottom 40% vs top 40%)
- Region

### 5.2 DEAI Version Comparison
Spearman correlation between 4 DEAI versions; AUC comparison of each version in M3 structure.

## 6. Sensitivity Analyses

### 6.1 Multicollinearity
VIF for all exposome predictors. Flag VIF > 5; remove highest-VIF variable if > 10.

### 6.2 Missing Data
Primary: complete-case; sensitivity: MICE (5 imputations, pooled by Rubin's rules)

### 6.3 Negative Control
Replace outcome with random binary (50:50) — expected AUC ≈ 0.50; confirms no data leakage.

### 6.4 DEAI Weight Perturbation
Perturb all knowledge weights by ±20%; report IQR of resulting AUCs.

### 6.5 Alternate Frailty Threshold
Repeat primary analysis at FI thresholds 0.20 and 0.30.

## 7. Omics Triangulation
Biological plausibility assessed by:
1. ORA of significantly upregulated genes in aged samples (GEO) vs MSigDB Hallmarks
2. Mapping enriched pathways to DEAI exposome domains
3. Reported as "supportive evidence" — no statistical integration with primary model

## 8. Causal Inference Note
This is an observational, cross-sectional prediction study.
- DAG sketched in `results/figures/dag_concept.png`
- No causal claims made without longitudinal replication
- Language: "associated with", "predicts", "index of risk", NOT "causes" or "reduces"

## 9. Multiple Testing
- Primary hypothesis: single pre-specified test (M3 vs M0 AUC, frailty outcome)
- Secondary outcomes: Bonferroni correction for 5 outcomes (α=0.01)
- Subgroup analyses: exploratory; no correction applied; labelled as hypothesis-generating

## 10. Reporting Standards
- TRIPOD guidelines for prediction models
- STROBE checklist for observational study elements
- EQUATOR network reporting templates

## 11. Software
Python 3.11; scikit-learn 1.5; XGBoost 2.0; SHAP 0.45; statsmodels 0.14; lifelines 0.28
Random seed: 42 (all models)
