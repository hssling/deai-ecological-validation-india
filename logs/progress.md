# DEAI Pipeline — Progress Log

---

## Phase 1 — Project Scaffolding — COMPLETE
**Timestamp:** 2026-04-22

**Completed:**
- Full directory tree created (all phases)
- `config.yaml` — master configuration with all paths, seeds, hyperparameters, journal targets
- `environment.yml` + `requirements.txt` — pinned Python 3.11 environment
- `Makefile` — phased execution (`make all` through `make phase2`…`phase10`)
- `.gitignore` — protects raw data, secrets, environments
- `src/**/__init__.py` — all subpackages initialised
- `src/utils/config.py` — YAML config loader with path resolution
- `src/utils/logger.py` — structured logger writing to `logs/progress.md` + `logs/pipeline.log`
- `src/utils/io.py` — save/load helpers for parquet, CSV, figures

**Phase 2 — Data Ingestion — COMPLETE (scripts ready)**
- `src/ingest/download_who_aaq.py` — WHO AAQ 2022 (free download; 6,000+ cities)
- `src/ingest/download_nfhs5.py` — NFHS-5 aggregates via DHS API + published fallback
- `src/ingest/download_lancet_countdown.py` — Lancet Countdown 2023 (Figshare)
- `src/ingest/download_geo_omics.py` — GEO datasets via GEOparse (GSE65765, GSE40279, GSE30272)
- `src/ingest/build_synthetic_cohort.py` — N=5,000 synthetic cohort (calibrated to LASI/NFHS-5)
- `src/ingest/ingest_all.py` — phase orchestrator
- `docs/data_inventory.md` — full dataset registry with access notes
- `docs/data_decisions.md` — substitution and access decisions (5 logged)

**Phase 3 — Feature Engineering — COMPLETE (script ready)**
- `src/features/build_features.py` — 8 exposome variables × 5 outcomes × 7 covariates
- `docs/phenotype_definitions.md` — complete variable definitions

**Phase 4 — DEAI Construction — COMPLETE (script ready)**
- `src/models/deai_build.py` — 4 DEAI versions (knowledge-weighted, PCA, elastic-net, XGBoost)
- Age-acceleration residual implemented

**Phase 5 — Modeling — COMPLETE (script ready)**
- `src/models/train_models.py` — M0–M4, 5-fold CV, AUC/Brier/NRI, 5 outcomes

**Phase 6 — Omics — COMPLETE (scripts ready)**
- `src/omics/geo_ingest.py` — GEO soft file processing + QC
- `src/omics/pathway_scoring.py` — ORA via gseapy / literature-curated fallback
- `docs/omics_integration_notes.md` — triangulation strategy documented

**Phase 7 — Explainability — COMPLETE (script ready)**
- `src/models/explain.py` — SHAP TreeExplainer, beeswarm + bar chart, modifiable flag

**Phase 8 — Statistical Rigor — COMPLETE (script ready)**
- `src/stats/sensitivity_analysis.py` — VIF, subgroup AUC, negative control
- `docs/statistical_analysis_plan.md` — full pre-specified SAP

**Phase 9 — Manuscript — COMPLETE (draft ready)**
- `manuscript/manuscript_main.md` — full draft (4,500 word target)
- `manuscript/cover_letter.md`
- `manuscript/figure_legends.md`
- `manuscript/supplement.md`

**Phase 10 — Dissemination — COMPLETE**
- `docs/research_brief.md`
- `docs/plain_language_summary.md`
- `docs/next_studies.md`
- `results/slides/outline.md`
- `README.md`

---

## What Remains

1. **Execute the pipeline** — run `make all` to generate all outputs:
   ```
   make phase2   # ~10 min (downloads)
   make phase3   # ~1 min
   make phase4   # ~5 min (XGBoost training)
   make phase5   # ~10 min (5-fold CV × 5 outcomes)
   make phase6   # ~30 min (GEO downloads, variable)
   make phase7   # ~5 min
   make phase8   # ~5 min
   ```

2. **Replace synthetic cohort** — apply for LASI/NFHS-5 microdata and re-run from Phase 3

3. **Populate manuscript XX placeholders** — all result numbers are labelled [SYNTHETIC PLACEHOLDER]

4. **Add tests** — `tests/` directory is initialised; add pytest unit tests for feature transforms and DEAI scoring

5. **Add `src/omics/dge_analysis.py`** — differential expression analysis (stub needed)

6. `src/utils/build_manuscript.py` — automated table-population script (Phase 9 automation)

---

## Risks and Blockers

| Risk | Severity | Mitigation |
|------|----------|-----------|
| LASI microdata access delay (weeks) | High | Synthetic cohort enables full pipeline run |
| GEO download speed (large SOFT files) | Medium | Pre-cached; skip with `--skip-geo` flag |
| GEOparse incompatibility with some SOFT formats | Medium | Fallback to literature-curated pathway table |
| XGBoost overfitting in small synthetic cohort | Low | 5-fold CV; results clearly labelled synthetic |

---

## Next Command to Run

```bash
conda activate deai
make phase2
```

This will:
1. Download WHO AAQ data (~5 MB)
2. Fetch NFHS-5 indicators via DHS API (or use published fallback)
3. Download Lancet Countdown data (~2 MB)
4. Attempt GEO downloads (large; may take 30–60 min)
5. Generate synthetic cohort (instant)
6. Write `results/tables/data_source_summary.csv`

## Phase 3 — Feature Engineering — COMPLETE
**Timestamp:** 2026-04-23 00:21:14

Exposome variables: 8
Outcome variables: 5
Total features in matrix: 31

---

## Phase 4 — DEAI Construction — COMPLETE
**Timestamp:** 2026-04-23 00:22:40

Four DEAI versions constructed and standardized.
Primary version: xgboost_risk_score
Age-acceleration residual computed.


---

## Phase 5 — Model Training — COMPLETE
**Timestamp:** 2026-04-23 00:23:32

Outcomes evaluated: 5
Models per outcome: 5 (M0–M4)
Best mean AUC (M3 Age+DEAI): 0.743


---

## Phase 7 — Explainability — COMPLETE
**Timestamp:** 2026-04-23 00:24:25

SHAP computed on frailty_index_binary.
Top feature: Chronological Age
Modifiable features in top 5: 3/5


---

## Phase 8 — Statistical Rigor — COMPLETE
**Timestamp:** 2026-04-23 00:26:52

VIF max: 1.34
Negative control AUC: 1.000
Subgroup analyses: 7 strata evaluated


---

## Phase 8 — Statistical Rigor — COMPLETE
**Timestamp:** 2026-04-23 00:28:51

VIF max: 1.34
Negative control AUC: 0.486
Subgroup analyses: 7 strata evaluated


---

## Phase 6c — Pathway Scoring — COMPLETE
**Timestamp:** 2026-04-23 00:35:39

Top pathway: HALLMARK_INFLAMMATORY_RESPONSE
Using: literature-curated data

---

## Phase 2b — Real Data Ingestion (LASI + NFHS-5) — COMPLETE
**Timestamp:** 2026-04-23 00:52:57

LASI: 37 states/UTs × 53 variables
NFHS-5 Tumkur: 1 rows
Data source: D:/Tumkur NPHCE/
Data type: REAL — LASI Wave 1 India factsheet (IIPS 2022)

---

## Phase 4b — DEAI Real Data Analysis — COMPLETE
**Timestamp:** 2026-04-23 00:53:26

N = 37 states/UTs
Data: LASI Wave 1 (REAL)
DEAI built from 8 exposome variables
Outcome correlations: 2/7 significant (p<0.05)
Karnataka DEAI Z = 0.347
Top DEAI state: Odisha (Z=2.06)

---

## Phase 4c - Real Data Robustness � COMPLETE
**Timestamp:** 2026-04-23 01:10:26

States-only sensitivity: N=36
Mortality rho=0.341
Multimorbidity rho=-0.777
Component alpha=0.688

---

## Phase 4c - Real Data Robustness � COMPLETE
**Timestamp:** 2026-04-23 01:18:04

States-only sensitivity: N=36
Mortality rho=0.341
Multimorbidity rho=-0.777
Component alpha=0.688

---

## Phase 4c - Real Data Robustness � COMPLETE
**Timestamp:** 2026-04-23 01:26:51

States-only sensitivity: N=36
Mortality rho=0.341
Multimorbidity rho=-0.777
Component alpha=0.688

---
