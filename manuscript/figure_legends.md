# Figure Legends

**DEAI Pipeline — Publication Figures**

---

## Figure 1 — DEAI Score Distributions and Inter-Version Correlations

**Panel A–D:** Distribution of four DEAI score versions (knowledge-weighted, PCA-based, elastic-net, XGBoost) in the derivation cohort (N=5,000). Scores are standardized to mean=0, SD=1. Dashed vertical line indicates population mean. Higher scores indicate greater adverse exposome burden.

**Panel E:** Spearman correlation heatmap between DEAI versions. Values represent Spearman's ρ; all p<0.001.

---

## Figure 2 — SHAP Feature Importance: Top Predictors of Frailty Risk

SHAP (SHapley Additive exPlanations) values from the XGBoost frailty model. **Top panel:** Mean absolute SHAP values for each feature (bars); red = modifiable feature, blue = non-modifiable. **Bottom panel:** SHAP beeswarm plot showing individual-level feature contributions (each dot = one individual, coloured by feature value: red=high, blue=low).

Abbreviations: PM2.5, particulate matter ≤2.5μm annual mean; SES, socioeconomic status quintile.

---

## Figure 3 — Pathway Enrichment: Hallmarks of Ageing in Transcriptomic Data

Forest plot showing normalized enrichment scores (NES) for MSigDB Hallmark gene sets in ageing transcriptomic samples (GEO datasets GSE65765, GSE40279). Colour indicates direction (red=upregulated, blue=downregulated in high-age/high-DEAI groups). Error bars: 95% CI. Dashed line at NES=0. Labels show FDR q-value. SASP = Senescence-Associated Secretory Phenotype; ROS = Reactive Oxygen Species.

*Note: These results represent biological triangulation evidence and are based on independent GEO cohorts with no individual-level overlap with the DEAI derivation cohort.*

---

## Figure 4 — Model Performance: ROC Curves Across Ageing Outcomes

ROC curves for five prediction models (M0–M4) for frailty (Panel A), multimorbidity (B), disability (C), poor self-rated health (D), and 5-year mortality risk (E). AUC values from 5-fold stratified cross-validation (mean ± SD across folds). Reference line: random classifier (AUC=0.50).

---

## Figure 5 — Subgroup Consistency of Age+DEAI Model (M3)

Forest plot of AUC (95% CI) for the Age+DEAI model (M3) across pre-specified subgroups: sex, age strata (40–54, 55–69, 70+ years), SES quintile group, and geographic region. Reference AUC (overall) shown as vertical dashed line with grey band (95% CI).

---

## Figure 6 — Real LASI State-Level DEAI Ranking

Horizontal bar chart ranking 37 Indian states/UTs by state-level DEAI Z-score using LASI Wave 1 public factsheet indicators. Higher scores indicate greater adverse exposome burden from indoor air pollution/no clean fuel, poor sanitation, low literacy, tobacco use, heavy episodic drinking, poor water access, reported indoor pollution exposure, and underweight prevalence. Karnataka is highlighted for the Tumkur context. These are ecological state-level estimates and should not be interpreted as individual-level risk scores.

---

## Figure 7 — Real LASI DEAI and Ageing Outcomes

Scatter plots showing state-level DEAI Z-score against LASI ageing outcomes across 37 states/UTs. Spearman correlations show a significant positive association with death rate among adults aged 60+ (rho=+0.342, p=0.038) and a strong inverse association with diagnosed multimorbidity (rho=-0.778, p<0.001). The multimorbidity association is interpreted as an epidemiological transition and ascertainment signal rather than a protective effect of adverse exposome burden.

---

## Figure 8 — Karnataka Exposome Profile Versus India

Grouped bar chart comparing Karnataka with the India national LASI estimate across DEAI components. Karnataka's DEAI was close to the national value (Z=+0.35 versus India Z=+0.44), with lower tobacco and underweight burden but persistent limitations in clean-fuel and sanitation-related domains.

---

## Figure 9 — Real LASI Exposome-Outcome Heatmap

Heatmap of Spearman correlations between individual DEAI exposome components and ageing outcomes in LASI Wave 1 state/UT data. Asterisks mark p<0.05. The heatmap is intended for ecological hypothesis generation and for identifying domains that may require individual-level validation in LASI microdata.

---

## Supplementary Figure S1 — Conceptual DAG

Directed acyclic graph (DAG) illustrating assumed causal relationships between exposome domains (air pollution, heat, tobacco, diet, SES), biological ageing mediators (inflammageing, oxidative stress, cellular senescence), and ageing-related outcomes (frailty, multimorbidity, disability). Arrows represent proposed causal pathways; dashed arrows represent associations evaluated in this study.

---

## Supplementary Figure S2 — Missing Data Pattern

Missingno matrix showing pattern of missing values across all variables in the derivation dataset. Columns = variables; rows = observations. White = missing.
