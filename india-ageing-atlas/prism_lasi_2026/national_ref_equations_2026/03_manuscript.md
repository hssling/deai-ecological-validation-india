Nationally Representative Spirometry Reference Equations for Middle-Aged and Older Indians: A Cross-sectional Derivation and Validation Study from the Longitudinal Ageing Study in India, and Re-estimated Burden of Restrictive and Preserved-Ratio Impairment

Running title: Indian spirometry reference equations

Article type: Original Article

## Abstract

**Background:** Spirometry in India is interpreted against reference equations derived from other populations or from small regional Indian samples, and India has no nationally representative reference. This mismatch inflates the apparent burden of restrictive and preserved-ratio impairment. We derived and validated national reference equations for adults aged ≥45 years from the Longitudinal Ageing Study in India (LASI) and re-estimated the burden.

**Methods:** From LASI Wave 1 we defined a respiratory-healthy reference population (never-smokers without self-reported lung disease or asthma, with acceptable spirometry and measured height; n = 24,300). Using GAMLSS (the Box-Cox Cole-Green / LMS method used by the Global Lung Function Initiative), we modelled the median, coefficient of variation, and skewness of FEV1, FVC, and FEV1/FVC as penalized-spline functions of age (with log-height for volumes), separately by sex, yielding predicted values, z-scores, and lower limits of normal (LLN). Equations were internally validated on a held-out 20% sample and compared with GLI-2012 (South-East Asian), GLI-Global 2022, and the Chhabra-2014 and Agarwal-2020 Indian equations. We then re-estimated survey-weighted PRISm and restrictive-pattern (RSP) prevalence in the full analytic sample (n = 30,995).

**Results:** In the held-out sample the equations were well calibrated (mean z −0.05 to +0.03; SD 0.98–1.01). Under the national LASI reference, PRISm affected 13.8% (fixed) and 4.0% (LLN) of adults, and RSP 14.4% and 4.8%—far below the 40.6% and 46.3% produced by GLI-2012 and GLI-Global, and consistent with the regional Indian equations. The Indian median FEV1 and FVC lay about one standard deviation below the GLI reference, so that the national reference recentred the population (median FVC z −0.01 versus −1.1 against GLI).

**Conclusions:** A large part of India's apparent restrictive and preserved-ratio "epidemic" is an artefact of non-representative reference equations. These first nationally representative equations for older Indians provide a validated, freely usable basis for interpreting spirometry in this population.

**Clinical significance:** For respiratory clinicians and public-health programmes in India, using a national age-, sex-, and height-matched reference can reduce systematic over-diagnosis of restrictive and preserved-ratio impairment in adults aged 45 years and older while preserving LLN-based identification of genuinely abnormal spirometry.

**Keywords:** spirometry; reference equations; lower limit of normal; preserved ratio impaired spirometry; India; ageing

## Introduction

The interpretation of spirometry rests entirely on the reference equation used to define "normal." A measured FEV1 or FVC is meaningless until it is compared with a predicted value for a person of the same age, sex, and height; the definitions of restriction, of preserved ratio impaired spirometry (PRISm), and of the lower limit of normal (LLN) all inherit whatever population the reference was built from.^(1,2)^ When the reference population differs systematically from the patient, impairment is over- or under-called by construction.

India illustrates the problem acutely. The Global Lung Function Initiative (GLI) 2012 equations^(1)^ contain no South Asian module, and South Asians have smaller lung volumes at a given age and height than the populations from which GLI was built.^(3)^ The recently recommended race-neutral GLI-Global equations^(4)^ replace ethnic categories with a single global average, but that average still exceeds South Asian volumes. The Indian equations that exist—most prominently Chhabra-2014 from northern India^(5)^ and Agarwal-2020 from western India^(6)^—are valuable but were derived from small regional convenience samples (n = 685 and 1,258) and were never intended as a national standard. India therefore lacks a nationally representative spirometry reference, a gap repeatedly noted but not filled.

The Longitudinal Ageing Study in India (LASI) changes what is possible. It is the first nationally representative survey to perform spirometry in Indian adults aged 45 years and older,^(7,8)^ providing—within its healthy participants—the raw material for a national reference for the ageing population, precisely the group in whom restrictive and preserved-ratio patterns matter most. This is also the age range in which spirometry is most likely to influence respiratory-care decisions: referral for suspected chronic lung disease, interpretation of dyspnoea and exercise limitation, pulmonary rehabilitation eligibility, perioperative risk assessment, and public-health estimates of chronic respiratory morbidity. If the reference equation systematically overestimates expected lung volume, these downstream decisions inherit the bias. We had two aims: to derive and validate nationally representative reference equations for FEV1, FVC, and FEV1/FVC in middle-aged and older Indians, and to use them to re-estimate the national burden of PRISm and the restrictive spirometric pattern (RSP), quantities we and others have shown to be highly sensitive to reference choice.

## Materials and Methods

### Data source and sampling

LASI Wave 1 (2017–2019) is a nationally representative, multistage stratified area-probability survey of adults aged ≥45 years and their spouses across all States and Union Territories.^(7,8)^ Spirometry was performed in the field by trained investigators with a handheld spirometer following the LASI protocol, with per-test grading for acceptability and repeatability. Standing height was measured. Reporting follows the STROBE statement.^(9)^

### Reference (healthy) population

Following GLI convention,^(1)^ the reference population comprised respiratory-healthy adults: those with acceptable spirometry, aged 45–95 years, with plausible measured height (120–210 cm), who were never-smokers and reported no chronic lung disease and no asthma. Consistent with GLI and Agarwal practice, no restriction was placed on body-mass index, so the reference reflects the full body-size distribution of healthy older Indians. This yielded 24,300 individuals (10,241 men, 14,059 women).

### Derivation

We used the LMS method,^(10)^ implemented by generalized additive models for location, scale and shape (GAMLSS)^(14)^ with the Box-Cox Cole-Green distribution (BCCG)—the same family and framework used to build the GLI equations. For each parameter and sex, three age-varying curves were estimated: the median (M), the coefficient of variation (S), and the Box-Cox skewness (L), each as a penalized B-spline function of age; for the volumes, log-height entered the median multiplicatively. Modelling L explicitly accommodates the right-skew of FEV1 and FVC without forcing a log-normal assumption. From the fitted L, M, and S, the z-score and the LLN (5th centile) follow by the standard BCCG quantile transform. The released reference (Supplementary Tables S3–S4) was fitted on the full reference population; a simpler quadratic-in-age parameterization gave concordant estimates (sensitivity analysis). Models were fitted separately by sex in R (gamlss).

### Validation

Within the reference population we held out a random 20% (stratified by sex) and fitted the equations on the remaining 80%. In the held-out sample, a well-calibrated reference should produce z-scores with mean ≈ 0 and standard deviation ≈ 1. We report these adequacy statistics. The released reference was refitted on the full reference population.

### Comparison and burden re-estimation

For every participant in the full analytic sample (adults ≥45 years with acceptable spirometry, plausible values, and measured height; n = 30,995) we computed predicted values, z-scores, and LLN under the new LASI reference and, for comparison, under GLI-2012 (South-East Asian module, identified as the equation embedded in the released LASI data), GLI-Global 2022, Chhabra-2014, and Agarwal-2020, using the validated `pyspiro` implementation. Airflow obstruction was defined by the FEV1/FVC ratio below its LLN; among those with a preserved ratio, PRISm by a low FEV1 and RSP by a low FVC, applied both as a fixed threshold (<80% of predicted) and as the LLN. Prevalence is survey-weighted (LASI spirometry weight) with 95% confidence intervals from the Kish effective sample size (Wilson method). Analyses used Python (pandas, statsmodels, patsy, pyspiro).

### Implementation and reproducibility

To make the equations directly usable, we exported the age-specific L, M, and S values and the height exponents rather than only fitted model objects. For FEV1 and FVC, the tabulated median at the sex-specific reference height is scaled by height as M(age, height) = M_ref(age) × (height/reference height)^b. The z-score is then calculated as [(observed/M)^L − 1]/(L × S), and the LLN is the 5th centile of the same BCCG distribution. For FEV1/FVC, M is expressed as a percentage and no height term is used. The lookup table gives selected clinically common ages and heights, while the full single-year LMS table supports implementation over the complete 45–90-year range. Non-integer ages can be handled by linear interpolation between adjacent tabulated LMS rows; extrapolation outside the fitted age range is not recommended. A small open-source Python package (`lasi-spirometry-reference`) was prepared with the bundled LMS table, prediction functions, z-score calculation, LLN calculation, and PRISm/RSP classification helpers so that laboratories and researchers can reproduce the calculations without refitting GAMLSS models.

### Ethics

LASI obtained approval from the Indian Council of Medical Research and written informed consent from all participants. This secondary analysis of de-identified public data required no further approval.

### Reporting and AI-assisted editing

Reporting follows the STROBE statement. A generative AI assistant (OpenAI ChatGPT/Codex) was used only for language editing and to help organise tables and figure/analysis code. The tool was not used to collect data, derive the equations, run the statistical models, select results, or make scientific interpretations; every numerical value reported here was verified against the analysis outputs.

## Results

### Reference population

The 24,300 respiratory-healthy adults (median age 55 years) had the expected sex difference in lung volumes; median height was 162 cm in men and 151 cm in women. Age coverage was substantial through the mid-70s and thinner beyond (Supplementary Table S1).

### Derived equations and centile curves

The fitted equations produced smooth, physiologically appropriate reference curves: median FEV1 and FVC declined monotonically with age and were higher in men, with the LLN tracking below the median (Figure 1). The estimated skewness (L) departed from unity and varied with age, confirming the value of modelling it rather than assuming log-normality. A worked lookup table of predicted median and LLN by age and height for both sexes is provided in Supplementary Table S3 so that the equations can be applied without specialist software; the age-specific L, M, and S values are in Supplementary Table S2.

### Validation

In the held-out 20% sample the equations were well calibrated: z-scores had a mean between −0.05 and +0.03 and a standard deviation between 0.98 and 1.01 for all three parameters in both sexes (Figure 2; Supplementary Table S4). This meets the standard adequacy criterion for a reference equation, and the standard deviations closer to unity than a simpler quadratic parameterization reflect the explicit modelling of scatter and skewness.

### Comparison with existing references

The choice of reference dominated the apparent prevalence of impairment. Weighted PRISm prevalence in the identical sample was 40.6% under GLI-2012 and 46.3% under GLI-Global 2022, fell to 18.6% (Chhabra) and 22.1% (Agarwal) under the regional Indian equations, and was 13.8% under the new national LASI reference (fixed threshold); the LLN moved every estimate lower still (Figure 3; Table 2). Against GLI the Indian median FEV1 and FVC lay about one standard deviation below the reference mean, whereas the national reference recentred the population (median FVC z −0.01), confirming the mismatch that drives over-calling. Notably, the race-neutral GLI-Global equations produced the *highest* prevalence, because a single global average overshoots South Asian volumes by more than the South-East Asian module does.

### Re-estimated national burden

Under the nationally representative LASI reference, PRISm affected 13.8% (95% CI 13.2–14.4) of middle-aged and older Indians by the fixed threshold and 4.0% (3.7–4.4) by the LLN; the restrictive pattern affected 14.4% (13.8–15.1) and 4.8% (4.4–5.2) respectively; airflow obstruction affected 6.6% (6.2–7.1) by the LLN (Table 2). These are the first estimates of these quantities against a home-grown national standard, and they place the true burden of restrictive and preserved-ratio impairment at roughly one in seven older adults by a fixed threshold and about one in twenty-five by the LLN—substantial and worth attention, but far from the two-in-five figure that a transplanted reference implies.

## Discussion

Using the first nationally representative spirometry sample of older Indians, we derived and validated national reference equations and showed that much of India's apparent restrictive and preserved-ratio "epidemic" is a property of the reference equation rather than of the lungs. The same participants were labelled with PRISm prevalence of 46.3% under a race-neutral global reference, 40.6% under the GLI South-East Asian module actually embedded in LASI, and 13.8% under a reference built from healthy Indians themselves. The national equations are well calibrated on held-out data and are provided in a directly usable form.

The novelty is therefore practical as well as statistical. Prior Indian equations established that regional Indian populations differ from GLI norms, but they were not built from a national sampling frame and could not quantify the national reclassification effect in the same individuals. LASI makes both steps possible: derivation of an Indian ageing-population reference and direct re-estimation of burden under competing references. The resulting message is actionable for respiratory care, because a laboratory or programme using GLI defaults in older Indians will not merely shift a z-score distribution; it will change who is labelled abnormal, who is sent for further work-up, and how national prevalence is described.

Several choices were made to favour robustness over a visually smooth curve alone. We used a respiratory-healthy subset with acceptable spirometry, separated derivation by sex, modelled the median, variation, and skewness rather than only the mean, and validated calibration in a held-out sample before refitting the release equation on all eligible healthy participants. We also compared the new reference with two GLI standards and two Indian regional equations in the identical analytic sample. The direction of change was coherent across fixed and LLN thresholds and across PRISm and RSP: global references over-called impairment most, regional Indian equations moved estimates downward, and the national LASI equations recentred the population. This pattern would be unlikely if the result were driven only by model choice.

Three points follow. First, the direction and size of the reference effect are exactly what a population with intrinsically smaller lung volumes predicts: the Indian median sits about one standard deviation below the GLI mean, so a fixed percent-predicted or a foreign LLN classifies a large, spurious fraction as impaired. Second, the race-neutral GLI-Global equations, although an advance for equity in mixed populations, do not solve the problem for South Asians and in our data made it worse, because averaging across the world's populations still overshoots South Asian volumes; a race-neutral global reference is not the same as a locally representative one. Third, the regional Indian equations (Chhabra, Agarwal) bracket our national estimate, which is the behaviour expected if all three approximate the same underlying Indian physiology while our sample is uniquely national in scope.

The clinical and public-health implication is not that restrictive and preserved-ratio patterns are unimportant in India—at roughly one in eight older adults by a national reference they remain common, and they carry recognised associations with frailty, disability, and mortality—but that their magnitude and the individuals they identify depend on using an appropriate reference. Reporting spirometry in older Indians against these national equations, rather than against GLI defaults, would reduce systematic over-diagnosis of restriction and provide a fairer denominator for burden estimates and programme planning.

Implementation is a key part of that implication. A reference equation that remains only a printed table is unlikely to change practice, particularly when most spirometry software defaults to GLI. For this reason the release is deliberately redundant: the manuscript provides the formulae and selected lookup values, the supplement provides the tabulated LMS values, and the accompanying software package applies the same formulae programmatically. This allows a clinician or analyst to verify a single patient manually, a laboratory to embed the calculations in a reporting workflow, and a researcher to re-score an epidemiological dataset. The package also makes the age boundary explicit and refuses extrapolation beyond 45–90 years by default, which is important because an apparently convenient national equation could otherwise be misapplied to young adults and children.

The results should be interpreted as a first national standard for older Indians, not as the final word on Indian lung-function prediction. The proper next step is not to discard GLI in all settings but to test the LASI equations prospectively and externally: in hospital pulmonary-function laboratories, community screening programmes, occupational cohorts, and future LASI waves. Agreement with regional Indian equations provides reassurance about direction, but external validation should examine calibration by region, rural/urban residence, height extremes, age above 80 years, and histories such as prior tuberculosis or biomass exposure. If such validation confirms the current calibration, the equations could support a pragmatic Indian reporting pathway in which older adults are interpreted against a national reference, while younger ages await a deliberately sampled all-age Indian reference.

Adoption should also preserve interpretive discipline. The equations do not replace clinical assessment, imaging, bronchodilator testing, or full lung-volume measurement when those are indicated. Their purpose is narrower but important: to provide a population-appropriate predicted value, z-score, and LLN for the first step of spirometric interpretation in older Indians, so that subsequent clinical decisions begin from a fair reference.

**Strengths and limitations.** The principal strength is the source: a large, nationally representative sample enabling the first national reference for older Indians, with internal validation. Limitations are real and stated plainly. LASI spirometry was performed in the field with a handheld device; without released calibration logs and individual flow–volume traces, the measurement floor is that of a large field survey rather than a research laboratory, and our equations should be regarded as population-representative rather than laboratory-gold-standard. The reference is confined to ages ≥45 years, so these are explicitly equations for the ageing population and must not be extrapolated to younger adults. "Healthy" was defined from self-reported never-smoking and absence of lung disease, without a respiratory-symptom questionnaire or prior-tuberculosis detail, so some misclassification is inevitable. Spirometry was pre-bronchodilator, and the analysis is cross-sectional. The equations are first-generation: although fitted by the full GAMLSS/LMS method, extension to LASI Wave 2, external validation in independent Indian cohorts, and the addition of younger adults are the natural next steps toward a definitive national standard.

## Conclusion

India has lacked a nationally representative spirometry reference, and the resulting reliance on foreign or regional equations has substantially overstated the burden of restrictive and preserved-ratio impairment in older adults. We provide GAMLSS/LMS-based national reference equations derived from healthy participants in the Longitudinal Ageing Study in India, together with a usable lookup table, and show that the true burden—about one in seven older adults for PRISm and the restrictive pattern by a fixed threshold—is far lower than global equations imply. We recommend their use for interpreting spirometry in middle-aged and older Indians, and their extension to future waves and external validation toward a definitive national standard.

## Clinical Significance

These equations give respiratory clinicians a nationally representative reference for interpreting spirometry in Indians aged 45 years and older. Their use can reduce systematic over-diagnosis of restrictive and preserved-ratio impairment caused by applying GLI equations to a population with lower expected lung volumes. For respiratory-care programmes, the re-estimated prevalence provides a more credible denominator for planning, referral, and surveillance. The equations should be used within their intended age range and strengthened through external validation and future LASI waves.

## List of Abbreviations

ATS, American Thoracic Society; BCCG, Box-Cox Cole-Green; CI, confidence interval; ERS, European Respiratory Society; FEV1, forced expiratory volume in 1 second; FVC, forced vital capacity; GAMLSS, generalized additive models for location, scale and shape; GLI, Global Lung Function Initiative; LASI, Longitudinal Ageing Study in India; LLN, lower limit of normal; LMS, lambda-mu-sigma; PRISm, preserved ratio impaired spirometry; RSP, restrictive spirometric pattern; STROBE, Strengthening the Reporting of Observational Studies in Epidemiology.

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
14. Rigby RA, Stasinopoulos DM. Generalized additive models for location, scale and shape. J R Stat Soc Ser C Appl Stat. 2005;54(3):507-554.

## Tables

**Table 1. Characteristics of the respiratory-healthy reference population (n = 24,300).**

| Characteristic | Men (n=10,241) | Women (n=14,059) |
|---|---|---|
| Age, years (median) | 57 | 55 |
| Height, cm (median) | 162 | 151 |
| FEV1, L (median) | 2.15 | 1.61 |
| FVC, L (median) | 2.71 | 2.00 |

Descriptive medians by age band are given in Supplementary Table S1.

**Table 2. PRISm and RSP prevalence by reference equation, and the re-estimated national burden.**

| Reference | PRISm fixed, % (95% CI) | PRISm LLN, % | RSP fixed, % | RSP LLN, % |
|---|---|---|---|---|
| GLI-2012 South-East Asian | 40.6 (39.7–41.5) | 27.6 | 37.8 | 27.5 |
| GLI-Global 2022 (race-neutral) | 46.3 (45.4–47.2) | 32.5 | 46.7 | 33.7 |
| Chhabra-2014 (northern India) | 18.6 (17.9–19.3) | 10.8 | 32.9 | 26.6 |
| Agarwal-2020 (western India) | 22.1 (21.3–22.8) | 11.8 | 27.5 | 18.8 |
| **LASI national (GAMLSS, this study)** | **13.8 (13.2–14.4)** | **4.0 (3.7–4.4)** | **14.4 (13.8–15.1)** | **4.8 (4.4–5.2)** |

Airflow obstruction under the LASI reference (ratio < LLN) was 6.6% (6.2–7.1). CI, confidence interval (Kish effective sample size, Wilson method).

## Figure legends

**Figure 1.** National LASI reference curves (GAMLSS/BCCG): predicted median (solid) and lower limit of normal (dashed) for FVC and FEV1 by age and sex, at each sex's reference height.

**Figure 2.** Internal validation: held-out z-scores for FEV1, FVC, and FEV1/FVC in men and women; a well-calibrated reference gives means near 0 with standard deviations near 1.

**Figure 3.** Weighted PRISm prevalence in the same national sample under five reference equations and two thresholds. Prevalence collapses from 46% (GLI-Global) to 14% (fixed) / 4% (LLN) under the nationally representative GAMLSS reference.
