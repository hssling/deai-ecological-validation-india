# Dataset Decision Log

**DEAI Pipeline — Data Substitution and Access Decisions**
Maintained by: Pipeline (auto-updated), Researcher (manual additions)
Last updated: 2026-04-22

---

## Decision 1: Primary Cohort — Synthetic Placeholder for LASI

| Field | Detail |
|-------|--------|
| **Decision date** | 2026-04-22 |
| **Original target** | LASI Wave 1 (Longitudinal Ageing Study in India) |
| **Reason for substitution** | LASI microdata requires free but time-gated registration at https://lasida.iips.in/ |
| **Substitute** | Synthetic cohort (N=5,000, `data_raw/synthetic_cohort.parquet`) |
| **Substitute quality** | Marginal distributions calibrated to LASI/NFHS-5 published statistics |
| **Action to reverse** | Place LASI parquet with matching schema into `data_raw/`, rerun from Phase 3 |
| **Manuscript note** | All results labelled SYNTHETIC; final manuscript requires real cohort |

## Decision 2: Air Pollution — WHO AAQ over IHME PM2.5

| Field | Detail |
|-------|--------|
| **Decision date** | 2026-04-22 |
| **Original target** | IHME Global PM2.5 exposure estimates (GBD 2019) |
| **Reason for substitution** | IHME GBD download requires account; automated download blocked |
| **Substitute** | WHO Ambient Air Quality Database 2022 (free direct download) |
| **Difference** | WHO = city-level monitoring data; IHME = modelled grid-level estimates |
| **Implication** | City-level exposure less precise than grid-level; population not individually linked |
| **Action to reverse** | Download IHME PM2.5 CSV from GHDx, place in `data_raw/`, update `config.yaml` |

## Decision 3: Exposome-to-Cohort Linkage — Ecological

| Field | Detail |
|-------|--------|
| **Decision date** | 2026-04-22 |
| **Decision** | PM2.5 and heat exposure assigned ecologically (region/urban-rural strata) |
| **Alternative** | Individual GPS-linked exposure (requires geocoded residential data) |
| **Rationale** | No publicly available Indian cohort has both individual GPS and frailty outcomes |
| **Limitation** | Ecological exposure estimates introduce non-differential measurement error |
| **Manuscript note** | Ecological exposure assignment is a key limitation; attenuates associations toward null |

## Decision 4: Omics — Triangulation Only (Not Integration)

| Field | Detail |
|-------|--------|
| **Decision date** | 2026-04-22 |
| **Decision** | GEO transcriptomics used for pathway-level biological triangulation, NOT individual-level integration |
| **Reason** | No GEO dataset has matching demographic data overlapping with DEAI cohort |
| **Alternative** | Multi-modal integration requires datasets with both omics + exposome (e.g., UK Biobank) |
| **Action if UK Biobank access available** | Use `src/omics/` framework with matched individual IDs |

## Decision 5: NFHS-5 — Aggregates Only

| Field | Detail |
|-------|--------|
| **Decision date** | 2026-04-22 |
| **Decision** | Use published national/state aggregates only |
| **Reason** | Microdata requires DHS application (typically 1–2 weeks) |
| **Substitute quality** | National estimates from published IIPS report (peer-reviewed source) |
| **Action to reverse** | Apply at https://dhsprogram.com/data/, download IR/HR recode files, update ingest script |
