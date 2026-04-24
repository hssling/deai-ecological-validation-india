# Quantitative Meta-analysis Add-on Manuscript

## Title
Peer-Reviewed Quantitative Synthesis of Human Anti-ageing Interventions on DNA Methylation Biomarkers: A Narrow Meta-analysis Add-on

## Status
This add-on manuscript is intentionally separate from the broad systematic review. The primary quantitative synthesis is frozen at the exact peer-reviewed human evidence with directly extractable uncertainty. Preprints, reconstructed endpoints, and sensitivity-only estimates remain outside the primary pooled model.

## Abstract
### Background
Claims that anti-ageing interventions slow or reverse biological ageing have expanded faster than the pool of human trials reporting quantitatively usable biomarker outcomes. A narrow quantitative synthesis is therefore needed to distinguish peer-reviewed, poolable evidence from broader but methodologically heterogeneous claims.

### Objective
To perform a conservative meta-analysis of peer-reviewed human intervention studies reporting directly extractable quantitative effects on DNA methylation biomarkers of ageing.

### Methods
This add-on was layered on top of the parent systematic review pipeline. Only peer-reviewed human intervention studies with direct between-group effect estimates and confidence intervals or standard errors were eligible for the primary pooled analysis. Preprints, reconstructed endpoints, crossover analyses without paired variance, and studies reporting only p values, medians, or adherence associations were excluded from the primary pool. Same-outcome pooling was restricted to outcome families with at least two independent studies and compatible effect metrics.

### Results
The only peer-reviewed outcome family meeting the primary pooling rule was DunedinPACE, represented by two independent trials: CALERIE and DO-HEALTH.[1,2] The pooled standardized effect estimate was -0.203 (95% CI -0.306 to -0.100; I2 = 0%; Figure 1, Table 1). This direction is consistent with a modest slowing of the pace of biological ageing. Other human clock studies were identified, but most could not be pooled because they reported non-comparator analyses, medians without directly usable variance, p values without confidence intervals, or only sensitivity-level reconstructed estimates.

### Conclusions
The current peer-reviewed human quantitative evidence base for anti-ageing biomarker interventions remains narrow. A signal exists for DunedinPACE, but it rests on only two trials and should not be generalized to broad claims of age reversal. The main limitation is not lack of promising studies, but lack of extractable, comparator-based quantitative reporting.

## Introduction
The broader anti-ageing literature contains a large volume of mechanistic, animal, biomarker, and hypothesis-generating work, but far fewer human intervention studies that can support quantitative synthesis. Even within human trials, many reports emphasize clock changes without publishing directly poolable treatment contrasts. For a publication-grade meta-analysis, that reporting gap matters more than narrative promise.

This add-on therefore takes a deliberately narrow approach. Its purpose is not to summarize all ageing biomarker claims, but to quantify only the subset of peer-reviewed human intervention evidence that can support defensible pooling.

## Methods
### Design
This project was conducted as a quantitative add-on to the main systematic review of anti-ageing and age-reversal interventions. Search, screening, and source discovery were inherited from the parent review, but quantitative inclusion was stricter.

### Eligibility for the primary quantitative pool
Studies were eligible only if they met all of the following:
- human intervention study
- peer-reviewed primary report
- outcome included a DNA methylation biomarker of ageing
- direct between-group estimate with confidence interval or standard error, or enough exact arm-level data to derive one cleanly
- no unresolved duplicate-cohort issue affecting the pooled contrast

The following were excluded from the primary pool:
- preprints
- reconstructed biological-age endpoints
- crossover studies without paired variance
- p values without directly extractable uncertainty
- adherence or association analyses not representing randomized between-group contrasts

### Data sources used in the final primary pool
- CALERIE: Nature Aging full text.[1]
- DO-HEALTH: Nature Aging full text.[2]

### Statistical approach
Pooling was limited to same-outcome, same-metric groups with at least two independent studies. The primary pooled result used DunedinPACE standardized change-difference estimates extracted from full-text peer-reviewed sources.[1,2] DunedinPACE was treated as a biomarker of the pace of biological ageing rather than a direct clinical outcome.[3] Fixed- and random-effects estimates were identical because between-study heterogeneity was zero in the retained pair.

## Results
### Included primary-pool studies
Two peer-reviewed human trials contributed to the primary pooled analysis:
- CALERIE[1]
- DO-HEALTH[2]

Both reported directly extractable DunedinPACE treatment effects with confidence intervals in accessible full text and satisfied the prespecified primary-pool rule.

### Primary pooled estimate
For DunedinPACE, two independent studies were available. The pooled standardized effect estimate was -0.203 with a standard error of 0.053 and a 95% confidence interval from -0.306 to -0.100. Statistical heterogeneity was low to absent (I2 = 0%). Study-level estimates and the pooled result are shown in Table 1 and Figure 1.

This estimate indicates a modest favorable shift in the pace-of-ageing biomarker direction. It does not, by itself, establish organismal rejuvenation or clinical age reversal.

### Table 1. Studies contributing to the primary DunedinPACE pool
See `results/meta_addon/tables/primary_dunedinpace_pool_studies.csv`.

### Quantitative evidence that remained outside the primary pool
Several additional human studies reported potentially relevant epigenetic-age results but did not meet the primary pooling rule. Reasons included:
- p value reported without directly reported confidence interval or standard error
- median and interquartile-range reporting without a usable treatment-effect variance
- adherence-based regression coefficients instead of randomized between-group contrasts
- crossover reporting without paired variance
- preprint-only availability

These studies remain documented in the extraction and audit tables but were not allowed to change the primary pooled estimate.

## Discussion
The main finding of this add-on is not the size of the pooled DunedinPACE effect alone, but the narrowness of the peer-reviewed evidence base that can be quantitatively synthesized without methodological compromise. Human intervention studies are increasingly measuring DNA methylation clocks, yet many still report those outcomes in forms that are not pool-ready.

That reporting pattern creates a predictable risk of overstatement. Narrative summaries can imply a large and convergent human evidence base when, in fact, only a small subset of trials provides comparator-based estimates with directly usable uncertainty. The current primary meta-analysis therefore supports a more limited conclusion: some peer-reviewed human interventions are associated with modest favorable changes in DunedinPACE, but the evidence remains sparse and outcome-specific.

This should also shape interpretation of broader anti-ageing claims. A favorable shift in a methylation biomarker, even a well-studied one, is not equivalent to demonstrated clinical rejuvenation. The present pooled result is better understood as evidence of biomarker-level modulation than as proof of reversed ageing.

## Limitations
- Only one outcome family, DunedinPACE, met the strict primary pooling rule.
- The pooled estimate is based on two studies.
- Several otherwise relevant peer-reviewed studies could not be pooled because their reporting was not quantitatively sufficient.
- Sensitivity-level evidence exists outside the primary pool, but incorporating it would weaken the evidentiary standard of the main model.

## Conclusion
The primary peer-reviewed quantitative evidence for anti-ageing interventions on DNA methylation biomarkers is currently narrow but nonzero. A modest pooled DunedinPACE signal is present across CALERIE and DO-HEALTH, but the field still lacks enough directly extractable randomized contrasts to support broader quantitative claims. This add-on should therefore be presented as a focused biomarker meta-analysis, not as a comprehensive pooled estimate of human age-reversal interventions.

## Figure and table files
- Figure 1: `results/meta_addon/figures/forest_dunedinpace_primary.png`
- Table 1: `results/meta_addon/tables/primary_dunedinpace_pool_studies.csv`
- Pooled summary table: `results/meta_addon/tables/primary_dunedinpace_pool_summary.csv`

## References
1. Belsky DW, Huffman KM, Pieper CF, Shalev I, Kraus WE, Kraus VB, et al. Effect of long-term caloric restriction on DNA methylation measures of biological aging in healthy adults from the CALERIE trial. Nature Aging. 2023;3:248-257. doi:10.1038/s43587-022-00357-y.
2. Bischoff-Ferrari HA, Paulussen M, Chocano-Bedoya PO, Vellas B, Rizzoli R, Cao L, et al. Individual and additive effects of vitamin D, omega-3 and exercise on DNA methylation clocks of biological aging in older adults from the DO-HEALTH trial. Nature Aging. 2025;5:266-278. doi:10.1038/s43587-024-00793-y.
3. Belsky DW, Caspi A, Corcoran DL, Sugden K, Poulton R, Arseneault L, et al. DunedinPACE, a DNA methylation biomarker of the pace of aging. eLife. 2022;11:e73420. doi:10.7554/eLife.73420.
