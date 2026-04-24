# Data Inventory

**DEAI Pipeline — Data Source Registry**
Last updated: 2026-04-22

---

## Summary Table

| # | Dataset | Domain | Access | Format | Local Path | Notes |
|---|---------|--------|--------|--------|------------|-------|
| 1 | WHO Ambient Air Quality Database 2022 | Air pollution | Public | Excel | `data_raw/who_aaq_database.xlsx` | City-level PM2.5/PM10; 117 countries |
| 2 | NFHS-5 National Indicators | Sociodemographic / lifestyle | Public (aggregates) | CSV | `data_raw/nfhs5_indicators.csv` | Microdata requires DHS registration |
| 3 | Lancet Countdown 2023 Indicators | Heat/climate | Public | Excel/CSV | `data_raw/lancet_countdown.csv` | Annual country-level climate-health |
| 4 | GEO GSE65765 | Transcriptomics (blood) | Public | SOFT | `data_raw/geo/GSE65765*` | Whole-blood RNA-seq, 20–89 yr |
| 5 | GEO GSE40279 | Epigenomics / methylation | Public | SOFT | `data_raw/geo/GSE40279*` | Hannum clock, 656 samples |
| 6 | GEO GSE30272 | Transcriptomics (brain) | Public | SOFT | `data_raw/geo/GSE30272*` | Post-mortem cortex lifespan |
| 7 | Synthetic Cohort (DEAI pipeline) | All domains | Generated | Parquet | `data_raw/synthetic_cohort.parquet` | **PLACEHOLDER** — clearly labelled |

---

## Dataset Details

### 1. WHO Ambient Air Quality Database
- **Source:** WHO Global Health Observatory
- **URL:** https://www.who.int/data/gho/data/themes/air-pollution/who-ambient-air-quality-database
- **Variables:** PM2.5 annual mean (μg/m³), PM10, station type, year, country, city, population
- **Coverage:** 6,000+ cities, 117 countries, 2010–2022
- **Key limitation:** City-level only; no individual-level linkage
- **Access status:** Freely downloadable as Excel (no registration)
- **DEAI domain:** Air pollution

### 2. NFHS-5 India (DHS)
- **Source:** International Institute for Population Sciences (IIPS), 2021
- **URL:** https://dhsprogram.com/data/ (microdata) | https://iipsindia.ac.in (factsheets)
- **Variables:** Household assets, sanitation, nutrition, women's health, child health, tobacco, alcohol, BMI
- **Coverage:** 707 districts, 636,699 households (microdata); aggregates used here
- **Key limitation:** Aggregates only; microdata requires DHS portal registration
- **Access status:** National/state/district summaries — free; microdata — registration required
- **DEAI domain:** Lifestyle, SES, built environment

### 3. Lancet Countdown on Health and Climate Change
- **Source:** Lancet Countdown Consortium (annual report)
- **URL:** https://www.lancetcountdown.org/data-repository/
- **Variables:** Heat-attributable deaths, heatwave exposure, labour capacity, wildfire PM2.5, air-pollution deaths
- **Coverage:** Country-level, 1990–2022
- **Access status:** Freely downloadable from Figshare
- **DEAI domain:** Heat stress, climate exposures

### 4–6. GEO Transcriptomic Datasets
- **Source:** NCBI Gene Expression Omnibus (GEO)
- **Access:** Fully public, fetched via GEOparse Python library
- **DEAI role:** Biological triangulation (not individual-level linkage)
- **Limitations:**
  - No demographic overlap with DEAI cohort
  - Different tissues, study designs, platforms
  - Results used only for pathway-level supportive evidence

### 7. Synthetic Cohort
- **Status:** PLACEHOLDER — epidemiologically structured, not empirical data
- **Purpose:** Enables full pipeline testing and manuscript-quality figure generation
- **Clearly marked:** `synthetic_flag = True` in all outputs
- **Parameters:** Drawn from published LASI/NFHS-5/GBD marginal distributions
- **Replaceability:** Drop any real cohort parquet with matching column names into `data_raw/`

---

## Priority Queue for Real Data Replacement

1. **Highest priority:** LASI Wave 1 (Longitudinal Ageing Study in India)
   - Access: https://lasida.iips.in/
   - Contains: frailty, multimorbidity, disability, cognition, 72,000+ individuals ≥45yr
   - Requires: user registration (free for researchers)

2. **Second priority:** NFHS-5 microdata via DHS portal
   - Access: https://dhsprogram.com/data/
   - Requires: DHS data access application (typically approved in 1–2 weeks)

3. **Third priority:** Global Burden of Disease 2021 risk factor data
   - Access: https://ghdx.healthdata.org/
   - Country-level risk factor prevalence, can strengthen ecological validation

---

## Missing Data Summary

| Dataset | Key Variables with >20% Missing | Strategy |
|---------|--------------------------------|----------|
| Synthetic | None (by construction) | N/A |
| WHO AAQ | ~30% of cities lack PM2.5 (PM10 only) | Use PM10→PM2.5 conversion ratio |
| NFHS-5 (agg) | State-level only for many indicators | District imputation from state means |
