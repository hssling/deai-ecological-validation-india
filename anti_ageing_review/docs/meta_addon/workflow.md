# Meta-analysis Add-on Workflow

This add-on is a separate quantitative project layered on top of the broader anti-ageing evidence map.

## Scope
- Human empirical studies only.
- Endpoint-specific quantitative synthesis.
- Separate manuscript from the broad review.

## Priority endpoint families
1. Frailty and functional performance
2. Epigenetic / biological-age biomarkers
3. Mortality / survival
4. Cognition

## Extraction hierarchy
1. PMC XML / supplementary source data
2. Publisher HTML or machine-readable PDF
3. Table extraction from PDF
4. Figure digitization when tables are unavailable

## Minimum data required for pooling
- Arm sizes and means/SDs, or
- Change scores with uncertainty, or
- HR/OR/beta with corresponding standard errors or confidence intervals

## Exclusion from pooling
- p values without estimable effect size
- Protocol-only records
- Duplicate cohorts not adjudicated
- Nonhuman studies

## Current primary-pool boundary
- The primary quantitative manuscript is currently frozen at the exact peer-reviewed human evidence with directly extractable uncertainty.
- The retained pooled analysis is a narrow DunedinPACE model based on CALERIE and DO-HEALTH.
- Working-dataset rows that are preprint-only, reconstructed, crossover-without-paired-variance, or otherwise sensitivity-level remain outside the primary pooled manuscript.
- New studies should be added to the primary pool only if they provide direct between-group clock estimates with confidence intervals or standard errors from a peer-reviewed source.
- Publication assets for the current frozen pool are rendered from the pooled tables, including `results/meta_addon/figures/forest_dunedinpace_primary.png` and the paired study-summary CSV files.
