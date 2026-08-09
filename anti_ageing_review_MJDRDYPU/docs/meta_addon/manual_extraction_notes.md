# Manual Numeric Extractions

## Exergame RFA trial
- Source: JMIR PDF Table 2
- URL: https://www.jmir.org/2024/1/e59468/PDF
- Randomized participants: 30 intervention, 30 control
- Extracted exact end-of-intervention mean and SD values for:
  - SOF frailty index
  - appendicular skeletal muscle mass
  - appendicular skeletal muscle mass index
  - dominant handgrip strength
  - walking speed
- Hedges g and standard error were computed from post-intervention means and pooled SD.

## Multidomain lifestyle trial
- Source: PMC XML `PMC12895478.xml`
- The SHARE-FI row uses values reported in the power paragraph: final sample sizes 15 and 28, group means 4.0 and 0.8, assumed SD 1.0.
- This is a sensitivity-only row and is not marked ready for pooling.
- Added a second sensitivity-only DNAm PhenoAge REA row from the main text:
  - control-group mean REA: `+8.4`
  - intervention-group mean REA: `-1.7`
  - reported `p = 0.03`
- The methylomic control-group sample size is reported only as a range (`n = 6-7`) in the supplement caption, so this row uses `n_control = 7` and remains sensitivity-only.

## Multiple sclerosis frailty pilot trial
- Source: verified extraction snippet in `results/tables/effect_size_extraction_priority_human.csv`
- Sixteen participants were randomized; ten intervention and six control participants completed the study.
- Added two generic inverse-variance rows using reported between-group change estimates and 95% confidence intervals:
  - Edmonton Frail Scale index performance score
  - MSQoL-54 mental health

## PROMOTe trial
- Source: PubMed XML abstract `pubmed_38424099.xml`
- The abstract reports 36 twin pairs (72 individuals) randomized.
- Added two generic inverse-variance rows using reported beta estimates and 95% confidence intervals:
  - chair rise time
  - cognitive factor score

## CALERIE trial
- Source: Nature Aging full text `https://www.nature.com/articles/s43587-022-00357-y`
- Added standardized treatment effects and 95% confidence intervals for:
  - PC PhenoAge at 12 and 24 months
  - PC GrimAge at 12 and 24 months
  - DunedinPACE at 12 and 24 months
  - DunedinPACE effect-of-treatment-on-the-treated estimates for 20% caloric restriction at 12 and 24 months

## DO-HEALTH trial
- Source: Nature Aging full text `https://www.nature.com/articles/s43587-024-00793-y`
- Added omega-3 main-effect standardized treatment estimates and 95% confidence intervals for:
  - PhenoAge
  - GrimAge2
  - DunedinPACE
- These were extracted from the primary article text and are suitable for generic inverse-variance pooling on a same-outcome basis.

## Greens crossover trial
- Source: PMC XML `PMC12915338.xml`
- Added exact condition-level mean changes and SDs for:
  - Horvath
  - PCGrimAge
  - DamAge
  - AdaptAge
- These are sensitivity-only rows because the crossover paper does not report the paired within-person correlation or a model-based treatment-effect SE.

## Fitzgerald pilot RCT
- Source: PMC HTML `https://pmc.ncbi.nlm.nih.gov/articles/PMC8064200/`
- Added a sensitivity-only Horvath DNAmAge row from the reported between-group change:
  - between-group DNAmAge difference: `-3.23 years`
  - reported `p = 0.018`
- This row is not poolable because the article does not report a confidence interval or standard error.

## FMD source-data recovery
- Downloaded official source workbook to `data_processed/open_text_cache/fmd_source_data.xlsx`
- Source article: `https://www.nature.com/articles/s41467-024-45260-9`
- Source data DOI: `https://doi.org/10.6084/m9.figshare.24915063`
- The workbook contains participant-level biomarker inputs for the biological-age analysis, but not the derived biological-age values or formula.
- Quantitative synthesis for this endpoint remains blocked pending reconstruction of the exact NHANES-trained biological-age algorithm used in the paper.

## Semaglutide RCT preprint
- Source: PMC-hosted medRxiv preprint `https://pmc.ncbi.nlm.nih.gov/articles/PMC12338914/`
- Trial population: adults with HIV-associated lipohypertrophy; semaglutide `n = 45`, placebo `n = 39`
- Added exact adjusted effect estimates with 95% confidence intervals for:
  - PCGrimAge
  - DunedinPACE
  - RetroClock
  - GrimAge V1
  - GrimAge V2
  - AdaptAge
  - CausAge
  - DamAge
- These rows are not marked ready for pooling because the source is preprint-only.

## Harmonization audit
- Generated `results/meta_addon/tables/meta_pooling_harmonization_audit.csv`
- This groups rows by endpoint family and effect metric so the next pass can target genuinely poolable subsets instead of mixing incompatible contrasts.
- Generated `results/meta_addon/tables/meta_multi_study_pool_candidates.csv` to flag outcome-level groups with at least two independent studies.
- Generated `results/meta_addon/tables/peer_reviewed_pool_eligibility_audit.csv` to document which quantified rows are peer-reviewed, primary-pool-eligible, or excluded.

## External peer-reviewed candidate audit
- Generated `results/meta_addon/tables/external_peer_reviewed_candidate_audit.csv` after scanning outside the current queue for additional peer-reviewed human intervention-clock studies.
- Current external scan did not identify another peer-reviewed human study with a primary-pool-ready between-group effect estimate and directly extractable uncertainty for the main clock outcomes.
- Generated `results/meta_addon/tables/peer_reviewed_pool_eligibility_audit.csv` to document which quantified rows are peer-reviewed, primary-pool-eligible, or excluded.
- Added two newer peer-reviewed human candidates to the external audit:
  - `PMID 40424097` therapeutic plasma exchange, `Aging Cell` 2025
  - `PMID 40576558` pitavastatin substudy of REPRIEVE, `Clinical Infectious Diseases` 2026
- Added `PMID 37743489` `DIRECT PLUS`, `BMC Medicine` 2023 after checking the full text PDF.
- Both remain outside the primary pool because accessible primary metadata do not provide a directly extractable between-group effect estimate with confidence interval or standard error for the clock outcomes.
- For `PMID 40424097`, PMC reports the article will not be available there until `2027-02-04`.
- For `PMID 40576558`, PubMed confirms randomized-arm median changes and a `P = .049` treatment-group difference for DunedinPACE, but not a pool-ready generic inverse-variance estimate.
- For `PMID 37743489`, the full text is accessible and explicitly states that intervention groups did not differ in clock changes; the reported quantitative signals are adherence-based multivariable betas for Li and Hannum clocks, not randomized between-group contrasts suitable for pooling.
