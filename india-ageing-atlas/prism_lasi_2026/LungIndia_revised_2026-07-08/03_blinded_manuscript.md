How Much Preserved Ratio Impaired Spirometry in Older Indians Is Real? National Prevalence, Metabolic and Ageing Correlates, and Dependence on the Reference Equation in the Longitudinal Ageing Study in India

Running title: Reference equations and PRISm in older Indians

Article type: Original Article

## Abstract

**Background:** Preserved ratio impaired spirometry (PRISm) and the restrictive spirometric pattern (RSP) predict disability and death, but their national burden in India is unknown and their measurement in South Asians is contested. We estimated the prevalence of PRISm and RSP in older Indians and tested how far the estimate depends on the reference equation.

**Methods:** We analysed acceptable spirometry from adults aged ≥45 years in the Longitudinal Ageing Study in India (LASI) Wave 1. PRISm (preserved ratio with low FEV1) and RSP (preserved ratio with low FVC) were classified with two co-primary thresholds—fixed cut-offs and the lower limit of normal (LLN)—applied under five reference sets: GLI-2012 (South-East Asian), GLI-Global 2022 (race-neutral), Chhabra-2014 and Agarwal-2020 (Indian), and an internal LASI healthy-subset reference. We report survey-weighted prevalence, an included-versus-excluded comparison, multinomial determinants, and adjusted associations with ageing measures.

**Results:** Among 30,996 adults, weighted PRISm prevalence ranged from 40.6% (GLI-2012 fixed) and 46.3% (GLI-Global) to 18.6% (Chhabra) and 3.9% (internal); the LLN moved every estimate lower. RSP was less reference-sensitive (27–47%). The whole population sat ~1 SD below the GLI mean (median FVC z −1.1). PRISm carried a metabolic-nutritional signature (underweight, obesity, diabetes) distinct from the smoking-and-age profile of obstruction, and was independently associated with frailty, low handgrip strength, functional limitation, and multimorbidity.

**Conclusions:** A low-volume spirometric pattern is genuinely common in older Indians and marks accelerated ageing, but the specific "PRISm" prevalence is governed largely by the reference equation, not the physiology. India needs nationally derived reference values before the burden can be stated with confidence.

**Keywords:** preserved ratio impaired spirometry; restrictive spirometry pattern; reference equations; lung function; frailty; India

## Introduction

Spirometry research has long centred on airflow obstruction, but a large group of adults have reduced lung function without obstruction. Preserved ratio impaired spirometry (PRISm)—a reduced forced expiratory volume in 1 second (FEV1) with a preserved FEV1/forced vital capacity (FVC) ratio—and the closely related restrictive spirometric pattern (RSP) are now recognised as common and consequential, predicting respiratory symptoms, cardiometabolic disease, progression to chronic obstructive pulmonary disease (COPD), and premature death.^(1-5)^ Reported prevalence ranges from about 3% to 20% across high-income populations, with higher figures where undernutrition, biomass exposure, and prior infection are common.^(5,6)^

India carries one of the world's largest burdens of chronic respiratory disease^(7)^ and a rapidly growing older population,^(8)^ yet national estimates of PRISm and RSP based on objective spirometry do not exist. The Longitudinal Ageing Study in India (LASI) is the first to administer spirometry to a nationally representative sample of adults aged 45 years and older.^(9,10)^ There is, however, a measurement problem that any such estimate must confront directly. The Global Lung Function Initiative (GLI) 2012 equations^(11)^ were derived largely from populations of European ancestry and contain no South Asian module; South Asians have smaller lung volumes at any given age and height, so applying a mismatched reference is expected to over-call impairment. India lacks a nationally representative reference of its own; the available Indian equations come from small, regional convenience samples.^(12,13)^

We therefore asked two questions rather than one. First, how common are PRISm and RSP in middle-aged and older Indians, and how are they patterned by metabolic and ageing-related factors? Second—and inseparably—how much of that prevalence is a property of the lungs, and how much is a property of the reference equation? We answer both by classifying the same national sample under two definitions (fixed cut-offs and the lower limit of normal) and five reference sets, ranging from global equations to Indian equations to an internal reference derived from LASI's own healthy participants.

## Materials and Methods

### Design and data source

This was a cross-sectional secondary analysis of LASI Wave 1 (2017–2019). Reporting follows the STROBE statement.^(14)^

### Sampling

LASI is a nationally representative survey of adults aged 45 years and older and their spouses, covering all States and Union Territories. It used a multistage stratified area probability cluster design—selection of primary sampling units within each State, then villages (rural) or urban blocks, then households, then eligible individuals—with survey weights that account for selection probability and non-response so that weighted estimates represent the national older population.^(9,10)^ All prevalence estimates in this paper use the LASI spirometry weight.

### Spirometry and quality assurance

Spirometry was performed in the field by trained investigators using a handheld spirometer following the LASI protocol, with on-screen quality feedback and grading of each test for acceptability and repeatability.^(10)^ We restricted the primary analysis to tests meeting the acceptability grade. We report the full quality profile (attempted, acceptable, and acceptable-and-repeatable tests; Figure 2) so that readers can judge the measurement floor. Two limitations of the source data are stated plainly: post-bronchodilator spirometry was not performed, and the released files do not include device-level calibration logs or the individual flow–volume traces, so central over-reading beyond the recorded acceptability grade was not possible. These constrain interpretation and are revisited in the Discussion.

### Reference equations

Because reference choice is itself a study question, we did not rely on a single equation. We first identified the reference embedded in the released LASI files: reconstructing predicted values from age, sex, and measured height showed that the supplied GLI values correspond to the **GLI-2012 South-East Asian module** (the nearest available proxy for South Asians, reproduced to <0.01 L). We then computed four further references for every participant using the validated `pyspiro` implementation: GLI-Global 2022 race-neutral equations,^(15)^ the Chhabra-2014 northern-Indian equations,^(12)^ the Agarwal-2020 western-Indian equations,^(13)^ and an internal reference fitted to LASI's own healthy subset (never-smokers without self-reported lung disease and with normal body-mass index; n = 12,824), with the lower limit of normal taken as predicted − 1.645 × residual standard deviation. The library's Chhabra output reproduced an independent hand-coded implementation of the published coefficients to 0.0001 L.

### Spirometric classification (co-primary)

Airflow obstruction was defined by the FEV1/FVC ratio (fixed <70, or below the ratio LLN). Among those with a preserved ratio, PRISm was defined by a low FEV1 and RSP by a low FVC, each applied two ways as co-primary definitions: a fixed cut-off (<80% predicted) and the LLN (below the 5th centile / z <−1.64). Every definition was applied under each reference set. We note as a data-quality finding that the released FEV1 and FEV1/FVC z-score fields were non-informative (zero variance) and were not used; the FVC z-score field was valid and used only for the distributional figure, and all LLN classifications used the reference-specific lower-limit values.

### Covariates and ageing measures

Covariates were age, sex, rural residence, schooling, body-mass index category (underweight <18.5, obese ≥25 kg/m²), current smoking, use of unclean cooking fuel, and self-reported diabetes. Ageing-related outcomes were a frailty index (≥0.25 defining frailty),^(16)^ any limitation in activities of daily living or instrumental activities, multimorbidity (≥2 chronic conditions), low handgrip strength by Asian Working Group for Sarcopenia thresholds,^(17)^ and fair or poor self-rated health.

### Statistical analysis

Prevalence is reported as survey-weighted percentages with 95% confidence intervals (Kish effective sample size, Wilson method); explicit primary-sampling-unit and stratum identifiers were not available in the analytic file, so this is a documented approximation of the design-based variance. Selection was examined by comparing acceptable (included) with unacceptable (excluded) participants using standardized differences, which are preferable to p-values at this sample size. Determinants were estimated with multinomial logistic regression (normal spirometry as reference). The association of PRISm (versus normal) with each ageing outcome was estimated by logistic regression adjusted for age, sex, residence, smoking, and schooling. Analyses used Python (pandas, statsmodels, pyspiro).

### Ethics

LASI obtained approval from the Indian Council of Medical Research and written informed consent from all participants. This secondary analysis of de-identified public data required no further approval.

## Results

### Participants and quality

Of 66,470 LASI respondents aged ≥45 years, 50,256 had a graded spirometry attempt; 31,090 met the acceptability grade, and after excluding implausible measured height 30,996 formed the analytic sample (median age 56 years, 49% women; Figure 1). Among graded tests, 62% were acceptable and 97% of acceptable tests were also repeatable (Figure 2).

### Selection

Excluded (unacceptable) participants were older (mean 59.8 vs 57.7 years), more often women (58% vs 49%), frailer (39% vs 33%), and more functionally limited (56% vs 50%) than those included; standardized differences reached 0.22 (Table 1). Comorbidity and diabetes were similar. Because the excluded were systematically frailer, any resulting bias would move the true prevalence of impairment upward relative to our estimate—that is, our figures are, if anything, conservative with respect to selection.

### Prevalence depends on the reference (Table 2, Figure 4)

Under the GLI-2012 South-East Asian reference and fixed cut-offs, weighted PRISm prevalence was 40.6% (95% CI 39.7–41.5), RSP 37.8% (37.0–38.7), and obstruction 13.3% (12.7–13.9). Changing only the reference or the threshold changed the headline substantially. The LLN reduced PRISm to 27.6% (26.8–28.4). The race-neutral GLI-Global 2022 equations raised PRISm to 46.3% (45.4–47.2), not lowered it—because South Asians sit below even the race-neutral average. The Indian equations gave much lower estimates: 18.6% (Chhabra, fixed) and 22.1% (Agarwal, fixed), falling to 10.8% and 11.8% respectively under the LLN. An internal reference built from LASI's own healthy participants gave 3.9% (3.6–4.3). The whole population lay about one standard deviation below the GLI mean (median FVC z −1.1; Figure 3).

The restrictive (low-FVC) pattern was notably less reference-sensitive than PRISm, remaining common across references (RSP 27–47%). Thus the low-volume physiology itself is robustly frequent in older Indians; it is the specific "PRISm" label—which depends on where the FEV1 threshold is drawn—that swings most with the reference equation. Consistent with this, five of every six PRISm cases under the GLI reference also met the restrictive criterion (84.3% overlap), indicating that preserved-ratio impairment in this population is driven overwhelmingly by low FVC rather than by isolated FEV1 reduction.

### Subgroups (Table 3)

The pattern of variation was stable across definitions. Under both fixed and LLN thresholds, GLI-referenced PRISm was similar in men and women, fell with age (fixed: 44.6% at 45–59 to 30.7% at ≥70 years), and was higher in urban than rural residents (fixed 46.9% vs 37.9%). The decline with age was a reclassification effect: obstruction rose steeply across the same bands as the preserved-ratio group shrank.

### Determinants (Table 4)

PRISm and obstruction had distinct profiles. PRISm carried a metabolic-nutritional signature—underweight (adjusted odds ratio 1.43, 95% CI 1.33–1.53), obesity (1.15, 1.09–1.22), and diabetes (1.27, 1.17–1.37)—and was not associated with current smoking (1.02, 0.95–1.10). Obstruction showed the classic profile—older age (1.42 per decade), current smoking (1.78, 1.62–1.96), and underweight (1.78)—and rose with age. Both were less common in women and rural residents.

### Association with ageing (Table 5)

Compared with normal spirometry and adjusted for age, sex, residence, smoking, and schooling, PRISm was independently associated with frailty (odds ratio 1.30, 95% CI 1.23–1.37), low handgrip strength (1.43, 1.35–1.51), functional limitation (1.23, 1.17–1.29), multimorbidity (1.24, 1.16–1.33), and fair or poor self-rated health (1.08, 1.02–1.14).

## Discussion

In the first national, spirometry-based study of PRISm and RSP in India, we report two findings that must be read together. A low-volume, non-obstructive spirometric pattern is genuinely common in middle-aged and older Indians and is clinically meaningful—it is metabolically patterned and independently marks frailty, weakness, functional limitation, and multimorbidity. But the specific prevalence of "PRISm" is governed largely by the reference equation: the same lungs yield a PRISm prevalence of 3.9% to 46.3% depending only on the reference and threshold chosen. Both statements are true, and stating only the first—as a single-reference analysis would—would overstate a precise national disease burden that the data cannot support.

**The reference-equation problem is a finding, not a footnote.** The equations embedded in LASI are the GLI-2012 South-East Asian module, applied to a South Asian population for which GLI has no dedicated module. That mismatch is visible directly: the entire Indian FVC distribution sits about one standard deviation below the GLI mean. Importantly, the recently recommended race-neutral GLI-Global equations^(15)^ did not fix this; they increased PRISm to 46.3%, because a single global average still overshoots the smaller lung volumes of South Asians. Only equations derived within India^(12,13)^ brought the estimate into a plausible range (roughly 11–22% depending on threshold), and an internal reference lower still. The implication is not that PRISm is absent but that its national magnitude cannot be stated with confidence until India has a nationally representative reference of its own—precisely the gap LASI could fill. Our comparison also shows where the estimate is robust: the restrictive/low-FVC pattern remains common (about a quarter to a third) even under Indian equations, so reduced lung volume in older Indians is real even if the "PRISm" count is uncertain.

**These associations are largely confirmatory, and we treat them as such.** PRISm has already been established elsewhere as a marker of poor health, frailty, sarcopenia, multimorbidity, and adverse outcomes.^(1-5)^ Our contribution is not to rediscover those links but to show, in a nationally representative Indian sample, that they hold, that PRISm here is metabolic rather than smoking-related, and—most usefully—that the headline prevalence is an artefact-prone quantity. The dual association with both underweight and obesity mirrors India's nutrition transition and cohort evidence of a U-shaped body-mass relationship with PRISm;^(5)^ the diabetes link echoes reports that dysglycaemia restricts lung volumes.^(18)^ The associations with frailty and low handgrip strength connect reduced lung function to the wider syndrome of physiological depletion in later life.

**Policy implication, stated cautiously.** The programmatic message is recognition, not mass labelling. India's respiratory and ageing programmes focus almost entirely on obstruction and smoking; a non-obstructive, metabolically patterned, function-linked pattern of this kind is currently invisible to them. But we deliberately avoid converting a reference-dependent percentage into a headline count of affected elders, because the denominator of "true" impairment is exactly what is uncertain. The defensible near-term action is to derive Indian reference equations and to add simple spirometry, read against them, at the non-communicable-disease and geriatric contacts these adults already attend.

**Strengths and limitations.** Strengths are a large, nationally representative sample; objective, quality-graded spirometry; measured height enabling multiple reference equations; and an analysis that makes the reference dependence explicit rather than hiding it. Limitations temper interpretation. The design is cross-sectional, so associations are not causal; LASI Wave 2 will allow trajectories. Spirometry was pre-bronchodilator, so "obstruction" is indicative and cannot be equated with COPD, and some PRISm may reflect reversible airway disease. Field spirometry with a handheld device, and the absence of released calibration logs and individual traces, place a genuine floor on measurement precision; the internal reference, being derived from the same imperfect measurements, is illustrative rather than a gold standard. Self-reported diabetes and smoking are subject to misclassification. Finally, design-based variance was approximated because sampling-unit identifiers were unavailable.

Future work should derive and validate nationally representative Indian reference equations from LASI's healthy participants, follow PRISm forward to incident disability and death, and test whether nutritional and metabolic interventions modify its trajectory.

## Conclusions

A low-volume, non-obstructive spirometric pattern is common in middle-aged and older Indians and independently marks frailty, weakness, and disability. Yet the specific prevalence of PRISm depends more on the reference equation than on the lungs, and even the modern race-neutral reference over-calls impairment in this population. The honest conclusion is twofold: the pattern is real and clinically relevant, and its national magnitude cannot be fixed until India builds a reference of its own.

## Declarations

**Ethics:** Secondary analysis of de-identified, publicly available LASI Wave 1 data, which obtained ethical approval from the Indian Council of Medical Research and written informed consent from all participants. No additional approval was required.

**Financial support and sponsorship:** None.

**Conflicts of interest:** There are no conflicts of interest.

**Data availability:** LASI Wave 1 data are available through the Gateway to Global Aging Data (g2aging.org) and the International Institute for Population Sciences. Analysis code is available from the author on reasonable request.

**Author contributions:** The single author conceived and designed the study, analysed the data, interpreted the findings, drafted and revised the manuscript, and approved the final version.

**Declaration of generative AI:** During preparation the author used a generative AI assistant for language editing and to help organise and format tables and figure code. All study conception, data analysis, interpretation, and scientific claims are the author's own; every numerical result was independently verified against the analysis and every reference was checked against its primary source. The author reviewed and edited all output and takes full responsibility for the content.

## References

1. Wan ES, Castaldi PJ, Cho MH, Hokanson JE, Regan EA, Make BJ, et al. Epidemiology, genetics, and subtyping of preserved ratio impaired spirometry (PRISm) in COPDGene. Respir Res. 2014;15(1):89.
2. Guerra S, Sherrill DL, Venker C, Ceccato CM, Halonen M, Martinez FD. Morbidity and mortality associated with the restrictive spirometric pattern: a longitudinal study. Thorax. 2010;65(6):499-504.
3. Wijnant SRA, De Roos E, Kavousi M, Stricker BH, Terzikhan N, Lahousse L, et al. Trajectory and mortality of preserved ratio impaired spirometry: the Rotterdam Study. Eur Respir J. 2020;55(1):1901217.
4. Higbee DH, Granell R, Davey Smith G, Dodd JW. Prevalence, risk factors, and clinical implications of preserved ratio impaired spirometry: a UK Biobank cohort analysis. Lancet Respir Med. 2022;10(2):149-157.
5. Wan ES, Balte P, Schwartz JE, Bhatt SP, Cassano PA, Couper D, et al. Association between preserved ratio impaired spirometry and clinical outcomes in US adults. JAMA. 2021;326(22):2287-2298.
6. Siddharthan T, Grigsby M, Morgan B, Kalyesubula R, Wise RA, Kirenga B, et al. Prevalence and impact of preserved ratio impaired spirometry in low-income and middle-income countries. Lancet Glob Health. 2024;12(9):e1498-e1505.
7. Salvi S, Kumar GA, Dhaliwal RS, Paulson K, Agrawal A, Koul PA, et al. The burden of chronic respiratory diseases across the states of India: the Global Burden of Disease Study 1990-2016. Lancet Glob Health. 2018;6(12):e1363-e1374.
8. International Institute for Population Sciences, United Nations Population Fund. India Ageing Report 2023. New Delhi: UNFPA; 2023.
9. Perianayagam A, Bloom D, Lee J, Parasuraman S, Sekher TV, Mohanty SK, et al. Cohort profile: the Longitudinal Ageing Study in India (LASI). Int J Epidemiol. 2022;51(4):e167-e176.
10. International Institute for Population Sciences, Harvard T.H. Chan School of Public Health, University of Southern California. Longitudinal Ageing Study in India (LASI) Wave 1, 2017–18: India report. Mumbai: IIPS; 2020.
11. Quanjer PH, Stanojevic S, Cole TJ, Baur X, Hall GL, Culver BH, et al. Multi-ethnic reference values for spirometry for the 3-95-yr age range: the global lung function 2012 equations. Eur Respir J. 2012;40(6):1324-1343.
12. Chhabra SK, Kumar R, Gupta U, Rahman M, Dash DJ. Prediction equations for spirometry in adults from northern India. Indian J Chest Dis Allied Sci. 2014;56(4):221-229.
13. Agarwal D, Parker RA, Pinnock H, Roy S, Ghorpade D, Salvi S, et al.; RESPIRE collaboration. Normal spirometry predictive values for the Western Indian adult population. Eur Respir J. 2020;56(3):1902129.
14. von Elm E, Altman DG, Egger M, Pocock SJ, Gøtzsche PC, Vandenbroucke JP. The STROBE statement: guidelines for reporting observational studies. Lancet. 2007;370(9596):1453-1457.
15. Bowerman C, Bhakta NR, Brazzale D, Cooper BR, Cooper J, Gochicoa-Rangel L, et al. A race-neutral approach to the interpretation of lung function measurements. Am J Respir Crit Care Med. 2023;207(6):768-774.
16. Searle SD, Mitnitski A, Gahbauer EA, Gill TM, Rockwood K. A standard procedure for creating a frailty index. BMC Geriatr. 2008;8:24.
17. Chen LK, Woo J, Assantachai P, Auyeung TW, Chou MY, Iijima K, et al. Asian Working Group for Sarcopenia: 2019 consensus update. J Am Med Dir Assoc. 2020;21(3):300-307.e2.
18. Yeh HC, Punjabi NM, Wang NY, Pankow JS, Duncan BB, Cox CE, et al. Cross-sectional and prospective study of lung function in adults with type 2 diabetes: the ARIC study. Diabetes Care. 2008;31(4):741-746.

## Tables

**Table 1. Comparison of included (acceptable spirometry) and excluded (unacceptable) participants aged ≥45 years.**

| Characteristic | Included (n=31,090) | Excluded (n=19,166) | Std. difference |
|---|---|---|---|
| Age, years (mean) | 57.7 | 59.8 | −0.22 |
| Women, % | 49.0 | 58.4 | −0.19 |
| Frailty, % | 32.9 | 39.1 | −0.13 |
| Functional limitation, % | 49.5 | 56.0 | −0.13 |
| Multimorbidity (≥2), % | 16.3 | 16.5 | −0.01 |
| Diabetes, % | 12.0 | 12.3 | −0.01 |
| Chronic lung disease, % | 1.5 | 1.5 | 0.00 |
| Rural residence, % | 66.9 | 64.8 | 0.04 |

Standardized differences >0.10 (bold in text) indicate meaningful imbalance; excluded participants were older and frailer, biasing prevalence downward.

**Table 2. Weighted prevalence of PRISm and RSP under five reference equations and two definitions (analytic sample, n=30,996).**

| Reference (equation) | Definition | PRISm, % (95% CI) | RSP, % (95% CI) |
|---|---|---|---|
| GLI-2012 South-East Asian | Fixed | 40.6 (39.7–41.5) | 37.8 (37.0–38.7) |
| GLI-2012 South-East Asian | LLN | 27.6 (26.8–28.4) | 27.5 (26.7–28.3) |
| GLI-Global 2022 (race-neutral) | Fixed | 46.3 (45.4–47.2) | 46.7 (45.8–47.6) |
| GLI-Global 2022 (race-neutral) | LLN | 32.5 (31.7–33.4) | 33.7 (32.8–34.5) |
| Chhabra-2014 (northern India) | Fixed | 18.6 (17.9–19.3) | 32.9 (32.0–33.7) |
| Chhabra-2014 (northern India) | LLN | 10.8 (10.3–11.4) | 26.6 (25.9–27.4) |
| Agarwal-2020 (western India) | Fixed | 22.1 (21.3–22.8) | 27.5 (26.7–28.3) |
| Agarwal-2020 (western India) | LLN | 11.8 (11.2–12.4) | 18.8 (18.1–19.5) |
| Internal LASI healthy-subset | LLN | 3.9 (3.6–4.3) | 4.9 (4.6–5.3) |

Obstruction (ratio-based) was 13.3% (fixed) and 15.4% (LLN) and is comparatively reference-insensitive. CI, confidence interval (Kish effective sample size, Wilson method).

**Table 3. Weighted PRISm prevalence by subgroup under co-primary definitions (GLI-2012 reference).**

| Subgroup | n | PRISm fixed, % (95% CI) | PRISm LLN, % (95% CI) |
|---|---|---|---|
| All (≥45 years) | 30,996 | 40.6 (39.7–41.5) | 27.6 (26.8–28.4) |
| Men | 15,796 | 40.7 (39.5–41.9) | 28.7 (27.6–29.9) |
| Women | 15,200 | 40.5 (39.3–41.9) | 26.5 (25.3–27.6) |
| Age 45–59 | 18,438 | 44.6 (43.5–45.7) | 31.1 (30.1–32.2) |
| Age 60–69 | 8,681 | 37.3 (35.7–39.0) | 24.4 (23.0–25.9) |
| Age ≥70 | 3,877 | 30.7 (28.3–33.2) | 19.7 (17.7–22.0) |
| Rural | 20,741 | 37.9 (36.9–38.9) | 25.3 (24.4–26.2) |
| Urban | 10,255 | 46.9 (45.2–48.7) | 33.1 (31.5–34.8) |

**Table 4. Multinomial determinants of PRISm and obstruction (normal spirometry as reference; adjusted odds ratios).**

| Predictor | PRISm OR (95% CI) | Obstruction OR (95% CI) |
|---|---|---|
| Age (per 10 years) | 0.85 (0.83–0.88) | 1.42 (1.37–1.47) |
| Women | 0.71 (0.68–0.75) | 0.60 (0.55–0.65) |
| Rural | 0.75 (0.71–0.80) | 0.81 (0.74–0.89) |
| Underweight | 1.43 (1.33–1.53) | 1.78 (1.62–1.96) |
| Obese | 1.15 (1.09–1.22) | 0.89 (0.81–0.98) |
| Current smoker | 1.02 (0.95–1.10) | 1.78 (1.62–1.96) |
| Unclean cooking fuel | 0.87 (0.82–0.92) | 0.81 (0.75–0.89) |
| Diabetes | 1.27 (1.17–1.37) | 1.07 (0.95–1.20) |
| No formal schooling | 1.07 (1.01–1.13) | 1.09 (1.00–1.18) |

**Table 5. Adjusted association of PRISm (versus normal spirometry) with ageing-related outcomes.**

| Outcome | Odds ratio (95% CI) |
|---|---|
| Frailty | 1.30 (1.23–1.37) |
| Low handgrip strength | 1.43 (1.35–1.51) |
| Functional limitation | 1.23 (1.17–1.29) |
| Multimorbidity (≥2) | 1.24 (1.16–1.33) |
| Fair or poor self-rated health | 1.08 (1.02–1.14) |

Adjusted for age, sex, rural residence, current smoking, and schooling.

## Figure legends

**Figure 1.** STROBE participant-flow diagram from LASI respondents aged ≥45 years to the analytic sample, with exclusions and quality steps.

**Figure 2.** Spirometry quality profile: (a) the grading funnel from attempted to acceptable to acceptable-and-repeatable tests; (b) acceptability among graded tests.

**Figure 3.** Distribution of FVC z-scores against the GLI-2012 South-East Asian reference; the Indian median lies about one standard deviation below the reference mean.

**Figure 4.** Weighted prevalence of PRISm and RSP under five reference equations and two thresholds. The same lungs yield PRISm prevalence from 46% to 4% depending on the reference; the dashed line marks the internal LASI healthy-subset estimate.
