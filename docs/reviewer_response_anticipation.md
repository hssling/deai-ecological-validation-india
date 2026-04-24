# Anticipated Reviewer Criticisms and Pre-emptive Responses

**Study:** DEAI — Digital Exposome Aging Index
**Purpose:** Prepare authors for peer review; refine manuscript proactively
**Version:** 1.0 | Date: 2026-04-22

---

## Critique 1: "The synthetic cohort limits the validity of all results."

**Likelihood:** Certain (Major)

**What reviewers will say:** "All results are derived from a synthetic dataset. This is a proof-of-concept, not an empirical study. Without validation in a real population cohort, no publication-ready claims can be made."

**Manuscript response:**
- Acknowledge prominently and early (Abstract, Methods §2.1, Results header)
- Frame explicitly as "methodological scaffold enabling empirical validation"
- Use language: "The current analysis demonstrates pipeline validity and structural plausibility; empirical estimates will replace synthetic values upon LASI microdata acquisition"
- Demonstrate that all distributions are calibrated to published LASI/NFHS-5 statistics (cite sources)
- Include LASI data access application status in cover letter
- Offer pre-submission sharing with editors pending real data

**Prevention:** Submit only after LASI data available. Current manuscript = preprint stage.

---

## Critique 2: "The DEAI is an arbitrary composite — why these weights? Why these variables?"

**Likelihood:** Certain (Major)

**What reviewers will say:** "Knowledge weights are subjective. The variable selection reflects investigator assumptions, not data-driven evidence. Different weights would give different results."

**Manuscript response:**
- All weight choices are documented and referenced (docs/phenotype_definitions.md Table)
- Four DEAI versions compared — including fully data-driven (PCA, elastic-net, XGBoost)
- Sensitivity analysis: weight perturbation ±20% (Phase 8); results table included
- If findings robust across DEAI versions, state: "Convergent findings across data-driven and knowledge-weighted versions suggest results are not artifact of weight choice"
- Cite precedent: Rockwood FI uses equal weighting; still predictive and validated internationally

---

## Critique 3: "Individual-level exposure measurement is absent — only ecological PM2.5."

**Likelihood:** Certain (Major for epidemiology journals)

**What reviewers will say:** "City-level or ecological exposure assignment introduces substantial measurement error and precludes causal inference about individual exposure-outcome relationships."

**Manuscript response:**
- Explicitly acknowledged as limitation (Discussion §4.2)
- "Ecological exposure assignment introduces non-differential measurement error, which biases associations toward the null — meaning true effect sizes may be larger than observed"
- Reframe: DEAI is explicitly designed as a population-level screening index, not an individual causal exposure estimate
- Cite precedent: WHO Ambient Air Quality Database used in >100 peer-reviewed epidemiological studies (cite 3–5)
- Point to future studies (docs/next_studies.md Study 4) with GPS-linked individual exposure

---

## Critique 4: "Cross-sectional design — you cannot establish temporality or causation."

**Likelihood:** Certain (Major)

**What reviewers will say:** "Without longitudinal data, it is impossible to determine whether exposome adversity precedes frailty or whether frail individuals have higher exposome burden due to reverse causation."

**Manuscript response:**
- Explicit in Abstract ("cross-sectional prediction study") and Discussion §4.2
- Consistently use language: "associated with", "predicted", "index of risk" — never "caused" or "reduced"
- Include DAG (Figure S1) showing assumed causal direction, with note: "Temporal ordering is assumed based on biological plausibility and prior longitudinal evidence; prospective validation is underway"
- Cite longitudinal evidence from other cohorts supporting PM2.5 → frailty temporality (cite ACS CPS, EPIC studies)

---

## Critique 5: "No external validation cohort — how generalisable is the DEAI?"

**Likelihood:** Likely (Major)

**What reviewers will say:** "Without external validation in an independent cohort, it is impossible to assess whether the DEAI is overfitted or generalisable."

**Manuscript response:**
- 5-fold cross-validation provides internal validation estimate (not optimistic train-test split)
- XGBoost DEAI scores are cross-validated predictions (not training-set predictions)
- Acknowledge: "External validation in LASI and NFHS-5 microdata is the immediate next step"
- Note: docs/next_studies.md Study 2 (DHS Cross-Country Validation) planned
- For submission version with real data: hold out 20% for held-out validation

---

## Critique 6: "The omics integration is superficial — it's just a literature review."

**Likelihood:** Likely (Moderate)

**What reviewers will say:** "The 'biological triangulation' is not empirical integration. You haven't linked individual-level exposome data to transcriptomics. This section adds little."

**Manuscript response:**
- Explicitly acknowledge distinction (Discussion, Supplement S1, docs/omics_integration_notes.md)
- Frame as "biological plausibility evidence" not "mechanistic integration"
- Precedent: Lancet Countdown explicitly uses triangulation across heterogeneous evidence types
- When GEO data is fully processed: empirical GSEA results will replace literature table
- For final manuscript: if direct integration impossible, reduce omics section to 1 paragraph in Discussion with reference to Supplement

---

## Critique 7: "Why use XGBoost for population epidemiology? It's a black box."

**Likelihood:** Moderate

**What reviewers will say:** "XGBoost is hard to interpret and not standard in epidemiological research. Logistic regression would be more appropriate and transparent."

**Manuscript response:**
- XGBoost is used for DEAI construction only, not for the primary epidemiological models (M0–M3 are logistic regression)
- SHAP provides full post-hoc explainability — cite Lundberg & Lee 2017
- XGBoost included as "upper bound reference" (M4); primary inference from M3 (logistic regression)
- Precedent: Frailty literature routinely uses machine learning for index construction (Pajewski et al. 2019; Segal et al. 2021)
- Note: elastic-net DEAI version available as a fully transparent alternative

---

## Critique 8: "The novelty claim is overstated."

**Likelihood:** Moderate

**What reviewers will say:** "Composite exposome indices for ageing have been proposed before (EWAS, exposome scores). The DEAI adds little that is new."

**Manuscript response:**
- Novelty statement explicitly acknowledges prior work and specifies what is new:
  1. First DEAI specifically integrating LMIC-relevant exposures (heat, PM2.5, diet diversity in LMIC context)
  2. First to apply explainable AI modifiable-vs-nonmodifiable framework to exposome ageing indexing
  3. First fully reproducible open pipeline designed for direct application to LASI/DHS surveys
  4. Biological triangulation with contemporaneous GEO ageing data
- Distinguish from EWAS approaches: those are hypothesis-generating; DEAI is a pre-specified composite with clinical interpretation

---

## Summary Table

| Critique | Severity | Pre-empted in manuscript? | Action required |
|----------|----------|--------------------------|-----------------|
| Synthetic cohort | Critical | Yes — explicit in Abstract | Get real data before submission |
| Arbitrary weights | Major | Yes — sensitivity analysis | Ensure weight perturbation in results |
| Ecological exposure | Major | Yes — limitation §4.2 | No additional action |
| Cross-sectional | Major | Yes — explicit framing | No additional action |
| No external validation | Major | Partial | 20% holdout in final analysis |
| Omics superficiality | Moderate | Yes — framing as triangulation | Run GSEA when GEO downloaded |
| XGBoost justification | Moderate | Yes — explainability + alternatives | No additional action |
| Novelty | Moderate | Yes — explicit novelty paragraph | Strengthen comparison to prior work |
