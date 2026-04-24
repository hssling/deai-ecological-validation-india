# Omics Integration Notes

## Strategy
Direct sample-level integration of GEO transcriptomics with the DEAI population cohort
is not possible as GEO datasets have no overlap with the DEAI cohort individuals.

## Triangulation Approach
1. Identify ageing hallmark pathways significantly enriched in the GEO ageing datasets.
2. Map these pathways to DEAI exposome domains that have documented molecular links:
   - PM2.5 → Inflammatory Response, Reactive Oxygen Species, NF-κB signaling
   - Heat stress → Hypoxia, Heat Shock Response, Protein Secretion
   - Tobacco → DNA Damage Response, Apoptosis, Inflammatory Response
   - Diet diversity → Oxidative Phosphorylation, AMPK signaling
3. This triangulation supports biological plausibility of DEAI exposome domains
   without claiming individual-level molecular measurement.

## Caution
- These GEO analyses are supportive evidence, not primary outcomes.
- GEO datasets may differ by tissue, age range, and study design.
- Results are clearly labeled in the manuscript as "biological triangulation."

## Primary GEO Datasets
- GSE65765: Whole-blood RNA-seq, 20–89 yr (Upton et al.)
- GSE40279: Methylation array, multi-tissue (Hannum et al.)
- GSE30272: Post-mortem cortex (Colantuoni et al.)

## Status
Empirical GSEA results will replace the literature-curated table when GEO
soft files are fully downloaded and processed.
