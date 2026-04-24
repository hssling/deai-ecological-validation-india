# Digital Exposome Aging Index (DEAI) — Full Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete, reproducible, publication-grade pipeline that constructs a Digital Exposome Aging Index (DEAI) from public population, environmental, and omics data, validates it as a predictor of accelerated biological ageing, and produces a near-submission manuscript with all supporting figures and tables.

**Architecture:** Modular Python pipeline with phase-gated execution controlled via `Makefile` and `config.yaml`; each phase writes clean artefacts to `/data_processed` and `/results`; manuscript auto-assembled from Markdown templates.

**Tech Stack:** Python 3.11, pandas, numpy, scikit-learn, xgboost, lightgbm, shap, lifelines, statsmodels, matplotlib, seaborn, plotly, biopython, GEOparse, scipy, pydeseq2 (or limma via rpy2), jupyter, conda/mamba, pytest, black, isort, pyyaml.

---

## Phase 1 — Project Scaffolding

### Task 1.1: Directory tree + init files

**Files:**
- Create: all `/src/**/__init__.py`
- Create: `config.yaml`
- Create: `.gitignore`
- Create: `Makefile`
- Create: `requirements.txt`
- Create: `environment.yml`

- [ ] Create `__init__.py` in every `src/` subpackage
- [ ] Write `config.yaml` with all path and parameter defaults
- [ ] Write `requirements.txt` and `environment.yml`
- [ ] Write `Makefile` with phased targets
- [ ] Write `.gitignore`
- [ ] Commit: `feat: project scaffold`

---

## Phase 2 — Data Discovery & Ingestion

### Task 2.1: Data inventory and decision log

**Files:**
- Create: `docs/data_inventory.md`
- Create: `docs/data_decisions.md`
- Create: `results/tables/data_source_summary.csv`

- [ ] Document all candidate datasets with access status
- [ ] Implement `src/ingest/download_who_mortality.py`
- [ ] Implement `src/ingest/download_global_burden.py`
- [ ] Implement `src/ingest/download_air_pollution.py`
- [ ] Implement `src/ingest/download_geo_omics.py`
- [ ] Implement `src/ingest/ingest_all.py` orchestrator
- [ ] Write metadata dictionaries to `/metadata/`
- [ ] Commit: `feat: data ingestion layer`

---

## Phase 3 — Feature Engineering

### Task 3.1: Outcome and exposome definitions

**Files:**
- Create: `docs/phenotype_definitions.md`
- Create: `src/features/build_features.py`
- Create: `src/features/exposome_vars.py`
- Create: `src/features/outcome_vars.py`
- Create: `results/tables/variable_map.csv`

- [ ] Define all exposome variables with source, coding, units
- [ ] Define all ageing outcome proxies
- [ ] Define covariate set
- [ ] Build feature matrix `data_processed/features_master.parquet`
- [ ] Unit test: missing value rates within expected bounds
- [ ] Commit: `feat: feature definitions and build_features`

---

## Phase 4 — DEAI Construction

### Task 4.1: DEAI score variants

**Files:**
- Create: `src/models/deai_build.py`
- Create: `src/models/deai_versions.py`
- Create: `results/tables/deai_versions_comparison.csv`
- Create: `results/figures/deai_distribution.png`

- [ ] Knowledge-weighted composite score
- [ ] PCA/factor-analysis score
- [ ] Elastic-net regularized regression score
- [ ] XGBoost risk score (probability → Z-scaled)
- [ ] Age-acceleration residual metric
- [ ] Standardize all to mean=0, SD=1
- [ ] Compare Spearman correlations between versions
- [ ] Commit: `feat: DEAI score construction`

---

## Phase 5 — Predictive Modeling

### Task 5.1: Model training and evaluation

**Files:**
- Create: `src/models/train_models.py`
- Create: `src/stats/evaluate.py`
- Create: `src/stats/sensitivity_analysis.py`
- Create: `results/tables/model_performance.csv`
- Create: `results/figures/roc_*.png`
- Create: `results/figures/calibration_*.png`

- [ ] Baseline: chronological age only
- [ ] Epidemiologic: age + covariates
- [ ] DEAI-only model
- [ ] Age + DEAI model
- [ ] XGBoost / LightGBM / elastic-net
- [ ] 5-fold cross-validated AUC, Brier score, NRI
- [ ] Decision-curve analysis
- [ ] Subgroup analyses: sex, age strata, SES
- [ ] Commit: `feat: model training and evaluation`

---

## Phase 6 — Omics Integration

### Task 6.1: GEO transcriptomics

**Files:**
- Create: `src/omics/geo_ingest.py`
- Create: `src/omics/dge_analysis.py`
- Create: `src/omics/pathway_scoring.py`
- Create: `results/tables/dge_summary.csv`
- Create: `results/figures/pathway_enrichment.png`
- Create: `docs/omics_integration_notes.md`

- [ ] Pull ageing-relevant GEO datasets
- [ ] QC: filter low-variance probes, log2-normalize
- [ ] Differential expression (linear model or DESeq2 via rpy2)
- [ ] GSEA or ORA for hallmarks of ageing pathways
- [ ] Triangulate pathway scores with DEAI
- [ ] Commit: `feat: omics integration layer`

---

## Phase 7 — Explainability

### Task 7.1: SHAP and feature ranking

**Files:**
- Create: `src/models/explain.py`
- Create: `results/figures/shap_summary.png`
- Create: `results/figures/shap_beeswarm.png`
- Create: `results/tables/top_predictors.csv`
- Create: `docs/explainability_notes.md`

- [ ] SHAP TreeExplainer on best-performing model
- [ ] Partial dependence plots for top-10 features
- [ ] Rank modifiable vs non-modifiable features
- [ ] Commit: `feat: explainability layer`

---

## Phase 8 — Statistical Rigor

### Task 8.1: Sensitivity and robustness

**Files:**
- Create: `src/stats/dag_analysis.py`
- Create: `results/tables/sensitivity_results.csv`
- Create: `results/figures/dag_concept.png`
- Create: `docs/statistical_analysis_plan.md`

- [ ] VIF / multicollinearity checks
- [ ] Multiple imputation comparison
- [ ] Alternate DEAI weight sensitivity
- [ ] Negative-control outcome analysis
- [ ] DAG concept figure
- [ ] Commit: `feat: statistical rigor layer`

---

## Phase 9 — Manuscript

### Task 9.1: Full manuscript draft

**Files:**
- Create: `manuscript/manuscript_main.md`
- Create: `manuscript/manuscript_short.md`
- Create: `manuscript/supplement.md`
- Create: `manuscript/cover_letter.md`
- Create: `manuscript/figure_legends.md`
- Create: `manuscript/references.bib`

- [ ] Title page, abstract, intro, methods, results, discussion
- [ ] Table shells populated from `/results/tables/`
- [ ] Inline figure references
- [ ] Journal-targeting note (tier 1/2/3)
- [ ] Commit: `feat: manuscript draft`

---

## Phase 10 — Dissemination

### Task 10.1: Research brief and slides

**Files:**
- Create: `docs/research_brief.md`
- Create: `docs/plain_language_summary.md`
- Create: `docs/next_studies.md`
- Create: `results/slides/outline.md`

- [ ] 10-slide scientific deck outline
- [ ] One-page research brief
- [ ] Plain-language summary
- [ ] Grant-direction notes
- [ ] Commit: `docs: dissemination materials`
