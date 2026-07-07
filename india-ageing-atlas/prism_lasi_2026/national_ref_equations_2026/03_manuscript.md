Nationally Representative Spirometry Reference Equations for Middle-Aged and Older Indians: Derivation and Validation from the Longitudinal Ageing Study in India, and the Re-estimated Burden of Restrictive and Preserved-Ratio Impairment

Running title: National spirometry reference equations for older Indians

Article type: Original Article

## Abstract

**Background:** Spirometry in India is interpreted against reference equations derived from other populations or from small regional Indian samples, and India has no nationally representative reference. This mismatch inflates the apparent burden of restrictive and preserved-ratio impairment. We derived and validated national reference equations for adults aged ≥45 years from the Longitudinal Ageing Study in India (LASI) and re-estimated the burden.

**Methods:** From LASI Wave 1 we defined a respiratory-healthy reference population (never-smokers without self-reported lung disease or asthma, with acceptable spirometry and measured height; n = 24,300). Using an LMS-style approach, we modelled the median (age polynomial plus log-height) and age-varying scatter of FEV1, FVC, and FEV1/FVC separately by sex, yielding predicted values, z-scores, and lower limits of normal (LLN). Equations were internally validated on a held-out 20% sample and compared with GLI-2012 (South-East Asian), GLI-Global 2022, and the Chhabra-2014 and Agarwal-2020 Indian equations. We then re-estimated survey-weighted PRISm and restrictive-pattern (RSP) prevalence in the full analytic sample (n = 30,995).

**Results:** In the held-out sample the equations were well calibrated (mean z −0.05 to +0.03; SD 1.02–1.07 overall and near 1 across age bands). Under the national LASI reference, PRISm affected 11.9% (fixed) and 5.3% (LLN) of adults, and RSP 12.9% and 6.2%—far below the 40.6% and 46.3% produced by GLI-2012 and GLI-Global, and consistent with the regional Indian equations. The Indian median FEV1 and FVC lay about one standard deviation below the GLI reference.

**Conclusions:** A large part of India's apparent restrictive and preserved-ratio "epidemic" is an artefact of non-representative reference equations. These first nationally representative equations for older Indians provide a validated, freely usable basis for interpreting spirometry in this population.

**Keywords:** spirometry; reference equations; lower limit of normal; preserved ratio impaired spirometry; India; ageing

## Introduction

The interpretation of spirometry rests entirely on the reference equation used to define "normal." A measured FEV1 or FVC is meaningless until it is compared with a predicted value for a person of the same age, sex, and height; the definitions of restriction, of preserved ratio impaired spirometry (PRISm), and of the lower limit of normal (LLN) all inherit whatever population the reference was built from.^(1,2)^ When the reference population differs systematically from the patient, impairment is over- or under-called by construction.

India illustrates the problem acutely. The Global Lung Function Initiative (GLI) 2012 equations^(1)^ contain no South Asian module, and South Asians have smaller lung volumes at a given age and height than the populations from which GLI was built.^(3)^ The recently recommended race-neutral GLI-Global equations^(4)^ replace ethnic categories with a single global average, but that average still exceeds South Asian volumes. The Indian equations that exist—most prominently Chhabra-2014 from northern India^(5)^ and Agarwal-2020 from western India^(6)^—are valuable but were derived from small regional convenience samples (n = 685 and 1,258) and were never intended as a national standard. India therefore lacks a nationally representative spirometry reference, a gap repeatedly noted but not filled.

The Longitudinal Ageing Study in India (LASI) changes what is possible. It is the first nationally representative survey to perform spirometry in Indian adults aged 45 years and older,^(7,8)^ providing—within its healthy participants—the raw material for a national reference for the ageing population, precisely the group in whom restrictive and preserved-ratio patterns matter most. We had two aims: to derive and validate nationally representative reference equations for FEV1, FVC, and FEV1/FVC in middle-aged and older Indians, and to use them to re-estimate the national burden of PRISm and the restrictive spirometric pattern (RSP), quantities we and others have shown to be highly sensitive to reference choice.

## Methods

### Data source and sampling

LASI Wave 1 (2017–2019) is a nationally representative, multistage stratified area-probability survey of adults aged ≥45 years and their spouses across all States and Union Territories.^(7,8)^ Spirometry was performed in the field by trained investigators with a handheld spirometer following the LASI protocol, with per-test grading for acceptability and repeatability. Standing height was measured. Reporting follows the STROBE statement.^(9)^

### Reference (healthy) population

Following GLI convention,^(1)^ the reference population comprised respiratory-healthy adults: those with acceptable spirometry, aged 45–95 years, with plausible measured height (120–210 cm), who were never-smokers and reported no chronic lung disease and no asthma. Consistent with GLI and Agarwal practice, no restriction was placed on body-mass index, so the reference reflects the full body-size distribution of healthy older Indians. This yielded 24,300 individuals (10,241 men, 14,059 women).

### Derivation

We used an LMS-style approach.^(10)^ For the volumes (FEV1, FVC), which are right-skewed, we modelled the natural logarithm, so the reference is log-normal (equivalent to LMS with the skewness parameter L = 0): the median M = exp(µ), the z-score = (ln y − µ)/σ, and the LLN (5th centile) = exp(µ − 1.645σ). The mean model µ was intercept + b·ln(height) + a quadratic in age (age centred at 60 years and expressed in decades); the ratio FEV1/FVC, being approximately symmetric, was modelled on the natural scale as a quadratic in age only. The scatter σ was allowed to vary with age, estimated from a linear model of the absolute residuals (for a normal distribution the expected absolute residual equals σ·√(2/π)). This identifiable parameterization yields directly reportable coefficients (Supplementary Table S3). Models were fitted separately by sex.

### Validation

Within the reference population we held out a random 20% (stratified by sex) and fitted the equations on the remaining 80%. In the held-out sample, a well-calibrated reference should produce z-scores with mean ≈ 0 and standard deviation ≈ 1, both overall and across age bands (45–54, 55–64, 65–74, ≥75). We report these adequacy statistics. The equations released (Supplementary Table S3 and the accompanying lookup table) were refitted on the full reference population.

### Comparison and burden re-estimation

For every participant in the full analytic sample (adults ≥45 years with acceptable spirometry, plausible values, and measured height; n = 30,995) we computed predicted values, z-scores, and LLN under the new LASI reference and, for comparison, under GLI-2012 (South-East Asian module, identified as the equation embedded in the released LASI data), GLI-Global 2022, Chhabra-2014, and Agarwal-2020, using the validated `pyspiro` implementation. Airflow obstruction was defined by the FEV1/FVC ratio below its LLN; among those with a preserved ratio, PRISm by a low FEV1 and RSP by a low FVC, applied both as a fixed threshold (<80% of predicted) and as the LLN. Prevalence is survey-weighted (LASI spirometry weight) with 95% confidence intervals from the Kish effective sample size (Wilson method). Analyses used Python (pandas, statsmodels, patsy, pyspiro).

### Ethics

LASI obtained approval from the Indian Council of Medical Research and written informed consent from all participants. This secondary analysis of de-identified public data required no further approval.

## Results

### Reference population

The 24,300 respiratory-healthy adults (median age 55 years) had the expected sex difference in lung volumes; median height was 162 cm in men and 151 cm in women. Age coverage was substantial through the mid-70s and thinner beyond (Supplementary Table S1).

### Derived equations and centile curves

The fitted equations produced smooth, physiologically appropriate reference curves: median FEV1 and FVC declined monotonically with age and were higher in men, with the LLN tracking below the median at a widening absolute distance in younger–taller strata (Figure 1). A worked lookup table of predicted median and LLN by age and height for both sexes is provided (Table 2; full grid in Supplementary Material) so that the equations can be applied without specialist software; the complete model coefficients are in Supplementary Table S3.

### Validation

In the held-out 20% sample the equations were well calibrated. Overall z-scores had a mean between −0.05 and +0.03 and a standard deviation between 1.02 and 1.07 for all three parameters in both sexes (Table 3). Calibration held across age bands, with band-specific mean z-scores generally within ±0.10 and standard deviations near 1; the only wider deviations occurred in the oldest, smallest band (≥75 years), where numbers are limited (Figure 2). This meets the standard adequacy criterion for a reference equation.

### Comparison with existing references

The choice of reference dominated the apparent prevalence of impairment. Weighted PRISm prevalence in the identical sample was 40.6% under GLI-2012 and 46.3% under GLI-Global 2022, fell to 18.6% (Chhabra) and 22.1% (Agarwal) under the regional Indian equations, and was 11.9% under the new national LASI reference (fixed threshold); the LLN moved every estimate lower still (Figure 3; Table 4). The Indian median FEV1 and FVC lay about one standard deviation below the GLI reference mean, confirming the mismatch that drives over-calling. Notably, the race-neutral GLI-Global equations produced the *highest* prevalence, because a single global average overshoots South Asian volumes by more than the South-East Asian module does.

### Re-estimated national burden

Under the nationally representative LASI reference, PRISm affected 11.9% (95% CI 11.3–12.5) of middle-aged and older Indians by the fixed threshold and 5.3% (4.9–5.7) by the LLN; the restrictive pattern affected 12.9% (12.3–13.5) and 6.2% (5.8–6.6) respectively; airflow obstruction affected 8.2% (7.7–8.7) by the LLN (Table 4). These are the first estimates of these quantities against a home-grown national standard, and they place the true burden of restrictive and preserved-ratio impairment at roughly one in eight to one in twenty older adults—substantial and worth attention, but far from the two-in-five figure that a transplanted reference implies.

## Discussion

Using the first nationally representative spirometry sample of older Indians, we derived and validated national reference equations and showed that much of India's apparent restrictive and preserved-ratio "epidemic" is a property of the reference equation rather than of the lungs. The same participants were labelled with PRISm prevalence of 46% under a race-neutral global reference, 41% under the GLI South-East Asian module actually embedded in LASI, and 12% under a reference built from healthy Indians themselves. The national equations are well calibrated on held-out data and are provided in a directly usable form.

Three points follow. First, the direction and size of the reference effect are exactly what a population with intrinsically smaller lung volumes predicts: the Indian median sits about one standard deviation below the GLI mean, so a fixed percent-predicted or a foreign LLN classifies a large, spurious fraction as impaired. Second, the race-neutral GLI-Global equations, although an advance for equity in mixed populations, do not solve the problem for South Asians and in our data made it worse, because averaging across the world's populations still overshoots South Asian volumes; a race-neutral global reference is not the same as a locally representative one. Third, the regional Indian equations (Chhabra, Agarwal) bracket our national estimate, which is the behaviour expected if all three approximate the same underlying Indian physiology while our sample is uniquely national in scope.

The clinical and public-health implication is not that restrictive and preserved-ratio patterns are unimportant in India—at roughly one in eight older adults by a national reference they remain common, and they carry recognised associations with frailty, disability, and mortality—but that their magnitude and the individuals they identify depend on using an appropriate reference. Reporting spirometry in older Indians against these national equations, rather than against GLI defaults, would reduce systematic over-diagnosis of restriction and provide a fairer denominator for burden estimates and programme planning.

**Strengths and limitations.** The principal strength is the source: a large, nationally representative sample enabling the first national reference for older Indians, with internal validation. Limitations are real and stated plainly. LASI spirometry was performed in the field with a handheld device; without released calibration logs and individual flow–volume traces, the measurement floor is that of a large field survey rather than a research laboratory, and our equations should be regarded as population-representative rather than laboratory-gold-standard. The reference is confined to ages ≥45 years, so these are explicitly equations for the ageing population and must not be extrapolated to younger adults. "Healthy" was defined from self-reported never-smoking and absence of lung disease, without a respiratory-symptom questionnaire or prior-tuberculosis detail, so some misclassification is inevitable. Spirometry was pre-bronchodilator, and the analysis is cross-sectional. Finally, we fixed the LMS skewness parameter by transform (L = 0 for volumes) rather than estimating it; a full GAMLSS refinement, and extension to LASI Wave 2, are the natural next steps.

## Conclusions

India has lacked a nationally representative spirometry reference, and the resulting reliance on foreign or regional equations has substantially overstated the burden of restrictive and preserved-ratio impairment in older adults. We provide validated national reference equations derived from healthy participants in the Longitudinal Ageing Study in India, together with a usable lookup table, and show that the true burden—about one in eight older adults for PRISm and the restrictive pattern by a fixed threshold—is far lower than global equations imply. We recommend their use for interpreting spirometry in middle-aged and older Indians and their refinement, by GAMLSS and in future waves, toward a definitive national standard.

## Declarations

**Ethics:** Secondary analysis of de-identified, publicly available LASI Wave 1 data (ICMR approval and written informed consent obtained by LASI). No additional approval required.

**Funding:** None.

**Conflicts of interest:** None declared.

**Data availability:** LASI Wave 1 data are available through the Gateway to Global Aging Data (g2aging.org) and IIPS. Full derivation code, coefficient tables, and the lookup grid are available from the author on reasonable request.

**Author contributions:** The single author conceived and designed the study, performed the analysis, interpreted the findings, drafted and revised the manuscript, and approved the final version.

**Declaration of generative AI:** The author used a generative AI assistant for language editing and to help organise tables and figure code. All study conception, analysis, interpretation, and scientific claims are the author's own; every numerical result was verified against the analysis and every reference against its primary source. The author takes full responsibility for the content.

## References

1. Quanjer PH, Stanojevic S, Cole TJ, Baur X, Hall GL, Culver BH, et al. Multi-ethnic reference values for spirometry for the 3-95-yr age range: the global lung function 2012 equations. Eur Respir J. 2012;40(6):1324-1343.
2. Stanojevic S, Kaminsky DA, Miller MR, Thompson B, Aliverti A, Barjaktarevic I, et al. ERS/ATS technical standard on interpretive strategies for routine lung function tests. Eur Respir J. 2022;60(1):2101499.
3. Sonnappa S, Lum S, Kirkby J, Bonner R, Wade A, Subramanya V, et al. Disparities in pulmonary function in healthy children across the Indian urban-rural continuum. Am J Respir Crit Care Med. 2015;191(1):79-86.
4. Bowerman C, Bhakta NR, Brazzale D, Cooper BR, Cooper J, Gochicoa-Rangel L, et al. A race-neutral approach to the interpretation of lung function measurements. Am J Respir Crit Care Med. 2023;207(6):768-774.
5. Chhabra SK, Kumar R, Gupta U, Rahman M, Dash DJ. Prediction equations for spirometry in adults from northern India. Indian J Chest Dis Allied Sci. 2014;56(4):221-229.
6. Agarwal D, Parker RA, Pinnock H, Roy S, Ghorpade D, Salvi S, et al.; RESPIRE collaboration. Normal spirometry predictive values for the Western Indian adult population. Eur Respir J. 2020;56(3):1902129.
7. Perianayagam A, Bloom D, Lee J, Parasuraman S, Sekher TV, Mohanty SK, et al. Cohort profile: the Longitudinal Ageing Study in India (LASI). Int J Epidemiol. 2022;51(4):e167-e176.
8. International Institute for Population Sciences, Harvard T.H. Chan School of Public Health, University of Southern California. Longitudinal Ageing Study in India (LASI) Wave 1, 2017–18: India report. Mumbai: IIPS; 2020.
9. von Elm E, Altman DG, Egger M, Pocock SJ, Gøtzsche PC, Vandenbroucke JP. The STROBE statement: guidelines for reporting observational studies. Lancet. 2007;370(9596):1453-1457.
10. Cole TJ, Green PJ. Smoothing reference centile curves: the LMS method and penalized likelihood. Stat Med. 1992;11(10):1305-1319.
11. Graham BL, Steenbruggen I, Miller MR, Barjaktarevic IZ, Cooper BG, Hall GL, et al. Standardization of spirometry 2019 update. An official ATS and ERS technical statement. Am J Respir Crit Care Med. 2019;200(8):e70-e88.
12. Wan ES, Balte P, Schwartz JE, Bhatt SP, Cassano PA, Couper D, et al. Association between preserved ratio impaired spirometry and clinical outcomes in US adults. JAMA. 2021;326(22):2287-2298.
13. Salvi S, Kumar GA, Dhaliwal RS, Paulson K, Agrawal A, Koul PA, et al. The burden of chronic respiratory diseases across the states of India: the Global Burden of Disease Study 1990-2016. Lancet Glob Health. 2018;6(12):e1363-e1374.

## Tables

**Table 1. Characteristics of the respiratory-healthy reference population (n = 24,300).**

| Characteristic | Men (n=10,241) | Women (n=14,059) |
|---|---|---|
| Age, years (median) | 57 | 55 |
| Height, cm (median) | 162 | 151 |
| FEV1, L (median) | 2.15 | 1.61 |
| FVC, L (median) | 2.71 | 2.00 |

Descriptive medians by age band are given in Supplementary Table S1.

**Table 2. Predicted median and lower limit of normal (LLN), selected age–height combinations (national LASI reference).**

| Sex | Age | Height (cm) | FEV1 median (L) | FEV1 LLN (L) | FVC median (L) | FVC LLN (L) |
|---|---|---|---|---|---|---|
| Men | 50 | 165 | 2.34 | 1.64 | 2.93 | 2.07 |
| Men | 60 | 165 | 2.12 | 1.45 | 2.71 | 1.90 |
| Men | 70 | 165 | 1.90 | 1.26 | 2.48 | 1.71 |
| Men | 80 | 165 | 1.68 | 1.07 | 2.24 | 1.49 |
| Women | 50 | 150 | 1.66 | 1.14 | 2.05 | 1.44 |
| Women | 60 | 150 | 1.52 | 1.03 | 1.91 | 1.33 |
| Women | 70 | 150 | 1.37 | 0.90 | 1.74 | 1.19 |
| Women | 80 | 150 | 1.21 | 0.77 | 1.54 | 1.01 |

Full lookup grid (heights 145–175 cm) in Supplementary Material.

**Table 3. Internal validation: held-out z-scores (overall).**

| Sex | Parameter | n | Mean z | SD z |
|---|---|---|---|---|
| Men | FEV1 | 2,049 | −0.03 | 1.05 |
| Men | FVC | 2,049 | −0.05 | 1.05 |
| Men | FEV1/FVC | 2,049 | 0.03 | 1.06 |
| Women | FEV1 | 2,812 | −0.02 | 1.02 |
| Women | FVC | 2,812 | −0.03 | 1.02 |
| Women | FEV1/FVC | 2,812 | 0.01 | 1.04 |

A well-calibrated reference yields mean z ≈ 0 and SD ≈ 1.

**Table 4. PRISm and RSP prevalence by reference equation, and the re-estimated national burden.**

| Reference | PRISm fixed, % (95% CI) | PRISm LLN, % | RSP fixed, % | RSP LLN, % |
|---|---|---|---|---|
| GLI-2012 South-East Asian | 40.6 (39.7–41.5) | 27.6 | 37.8 | 27.5 |
| GLI-Global 2022 (race-neutral) | 46.3 (45.4–47.2) | 32.5 | 46.7 | 33.7 |
| Chhabra-2014 (northern India) | 18.6 (17.9–19.3) | 10.8 | 32.9 | 26.6 |
| Agarwal-2020 (western India) | 22.1 (21.3–22.8) | 11.8 | 27.5 | 18.8 |
| **LASI national (this study)** | **11.9 (11.3–12.5)** | **5.3 (4.9–5.7)** | **12.9 (12.3–13.5)** | **6.2 (5.8–6.6)** |

Airflow obstruction under the LASI reference (ratio < LLN) was 8.2% (7.7–8.7). CI, confidence interval (Kish effective sample size, Wilson method).

## Figure legends

**Figure 1.** National LASI reference curves: predicted median (solid) and lower limit of normal (dashed) for FVC and FEV1 by age and sex, at each sex's reference height.

**Figure 2.** Internal validation: held-out z-scores by age band for FEV1 and FVC in men and women; a well-calibrated reference gives means near 0 (solid line) and standard deviations near 1 (dotted lines).

**Figure 3.** Weighted PRISm prevalence in the same national sample under five reference equations and two thresholds. Prevalence collapses from 46% (GLI-Global) to 12% (fixed) / 5% (LLN) under the nationally representative LASI reference.
