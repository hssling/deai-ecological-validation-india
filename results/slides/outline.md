# Scientific Presentation Outline — 10 Slides

**Title:** Digital Exposome Aging Index (DEAI): Predicting Accelerated Biological Ageing from Population Data
**Venue:** [Conference/seminar]
**Duration:** 15 minutes + 5 Q&A

---

## Slide 1 — Title

**Title:** Digital Exposome Aging Index (DEAI): A Multi-Domain Exposome Score for Accelerated Ageing
**Subtitle:** Open-science pipeline | LMIC focus | Explainable AI
**Speaker:** [Name, Institution]
**Graphic:** World map showing PM2.5 exposure gradients with population ageing overlay

---

## Slide 2 — The Problem

**Headline:** "Age 65 can mean very different things"
**Key points:**
- Biological vs chronological age diverge based on exposome
- Hallmarks of ageing are all modulated by environmental exposures
- Existing biological clocks (Horvath, GrimAge) require expensive molecular assays
- LMICs bear double burden: highest exposome adversity + fastest-ageing populations

**Visual:** Side-by-side frailty trajectory curves comparing low vs high PM2.5 exposure groups

---

## Slide 3 — DEAI: What It Is

**Headline:** "A composite environmental-lifestyle ageing clock"
**Key points:**
- 8 domains: PM2.5, heat, tobacco, alcohol, diet, urbanicity, SES, education
- Designed for survey data — no lab required
- Four construction methods; XGBoost primary
- Z-standardized: 0 = population mean; positive = adverse

**Visual:** DEAI domain spider/radar chart with domain weights

---

## Slide 4 — Data Sources

**Headline:** "Built for and validated with public data"
**Key points:**
- WHO Ambient Air Quality Database (6,000 cities)
- Lancet Countdown health-climate indicators
- NFHS-5 / LASI (India cohorts)
- GEO transcriptomics (biological triangulation)

**Visual:** Data flow diagram (sources → DEAI → outcomes)

---

## Slide 5 — DEAI Distribution and Internal Validity

**Key points:**
- DEAI versions correlated (Spearman r=0.58–0.83)
- XGBoost and elastic-net most strongly predict frailty index
- Age-acceleration residual: excess DEAI beyond what age predicts

**Visual:** Figure 1 (DEAI distribution plots)

---

## Slide 6 — Model Performance

**Headline:** "DEAI outperforms age alone across all ageing outcomes"
**Key points:**
- Age+DEAI (M3): AUC gain >0.05 vs age-alone (M0) for frailty
- NRI positive across all 5 outcomes
- Consistent across sex, age strata, SES groups

**Visual:** AUC comparison bar chart + ROC curves

---

## Slide 7 — What Drives the DEAI?

**Headline:** "Modifiable exposures dominate — policy targets identified"
**Key points:**
- SHAP: PM2.5, tobacco, diet top 3 contributors
- >50% of SHAP importance = modifiable
- Age ranks 4th–6th depending on outcome

**Visual:** Figure 2 (SHAP summary beeswarm)

---

## Slide 8 — Biological Plausibility

**Headline:** "Pathway triangulation confirms molecular mechanism"
**Key points:**
- GEO ageing transcriptomics: inflammageing pathways (NF-κB, IL-6, ROS) enriched
- These map directly to PM2.5 and tobacco DEAI domains
- Senescence-associated secretory phenotype (SASP) strongly upregulated

**Visual:** Figure 3 (pathway enrichment forest plot)

---

## Slide 9 — Open Science and Reproducibility

**Headline:** "Run the DEAI on your cohort today"
**Key points:**
- Full Python pipeline on GitHub (MIT licence)
- `make phase2 && make phase3 ... make all` — one command end-to-end
- Plug in LASI, NFHS-5, or any DHS dataset
- Synthetic cohort allows immediate testing

**Visual:** Architecture diagram (Makefile → phases → outputs)

---

## Slide 10 — Conclusions and Next Steps

**Headline:** "DEAI: a practical, scalable, actionable ageing index for LMICs"
**Key messages:**
1. DEAI captures accelerated ageing beyond chronological age
2. Modifiable components → public health targets
3. No lab required → scalable to 50+ LMIC survey programmes
4. Empirical validation in LASI Wave 1 underway

**Call to action:** Collaborators for LASI validation + data sharing welcome

**Visual:** Graphical abstract concept
