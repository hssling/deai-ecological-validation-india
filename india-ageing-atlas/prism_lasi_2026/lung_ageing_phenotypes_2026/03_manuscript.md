A Metabolic-Inflammatory Reserve Axis Underlies Lung-Function Variation in Middle-Aged and Older Indians: A Data-Driven Analysis of the Longitudinal Ageing Study in India

Running title: Lung-ageing phenotypes in older Indians

Article type: Original Article

## Abstract

**Background:** Reduced lung function in older adults is increasingly seen as part of a systemic ageing process rather than an isolated respiratory finding. We asked, without prior labelling, whether middle-aged and older Indians fall into distinct lung-ageing phenotypes when nationally referenced lung function is analysed together with metabolic and inflammatory biomarkers and muscle strength.

**Methods:** In 29,828 adults aged ≥45 years from the Longitudinal Ageing Study in India (LASI) Wave 1 with complete data, we applied k-means clustering to seven standardized features—FVC and FEV1/FVC z-scores against a nationally representative reference, body-mass index, HbA1c, log C-reactive protein (CRP), haemoglobin, and grip strength. The number of clusters was chosen by silhouette score. Clusters were then compared on ageing outcomes not used to build them (frailty, functional limitation, multimorbidity, self-rated health), an external-validation design.

**Results:** The optimal solution was two clusters, with modest separation (silhouette 0.16), indicating a dominant continuous axis rather than sharply distinct subtypes. One phenotype (37.8% weighted) combined higher BMI, HbA1c, and CRP with lower FVC z-scores—a metabolic-inflammatory, lower-lung-volume pattern; the other (62.2%) was leaner with lower inflammation and higher lung volumes. On outcomes not used in clustering, the metabolic-inflammatory phenotype had markedly higher multimorbidity (27.9% vs 10.0%) and more functional limitation (56.3% vs 52.4%), while frailty and self-rated health were similar.

**Conclusions:** Lung-function variation in older Indians is organised along a systemic metabolic-inflammatory reserve axis rather than into discrete respiratory phenotypes. The higher-risk pole of this axis carries excess multimorbidity and disability, supporting a dimensional, whole-person view of lung ageing in this population.

**Keywords:** lung function; ageing; phenotypes; inflammation; metabolic; India; unsupervised clustering

## Introduction

Reduced lung function predicts frailty, disability, and death well beyond the respiratory system, and preserved ratio impaired spirometry in particular behaves as a marker of systemic rather than purely pulmonary ageing.^(1,2)^ If that is so, then the natural structure of lung ageing in a population may be better revealed by analysing lung function together with metabolic, inflammatory, and physical-reserve markers than by respiratory labels alone. Whether such joint structure forms discrete phenotypes or a continuous gradient is unknown for South Asians, in whom lung volumes are low and metabolic disease is rising.^(3)^

We took a deliberately label-free approach. Using the first nationally representative spirometry sample of older Indians, and interpreting lung function against a nationally representative reference derived in the same programme, we asked unsupervised clustering to organise adults on a small set of reserve markers, and then tested whether the resulting groups differed in ageing outcomes that were not used to create them.

## Methods

We analysed LASI Wave 1 (2017–2019), a nationally representative survey of adults aged ≥45 years.^(4,5)^ The analytic sample comprised 29,828 adults with acceptable field spirometry, measured height, and complete biomarker and grip data. Lung function was expressed as FVC and FEV1/FVC z-scores against a nationally representative reference derived from LASI's respiratory-healthy participants (companion analysis from the same programme). Clustering features were these two lung z-scores plus body-mass index, HbA1c, log-CRP, haemoglobin, and grip strength—markers of metabolic, inflammatory, haematological, and muscular reserve; ageing outcomes (frailty index ≥0.25, functional limitation, multimorbidity, self-rated health) were deliberately excluded from clustering so they could serve as external validation.

Features were standardized and clustered by k-means (fixed seed, 10 initialisations). The number of clusters was selected by the silhouette score over k = 2–6. Phenotypes were characterised by standardized feature means; outcomes were compared as survey-weighted prevalence. Because the aim is structure discovery, analyses are exploratory and hypothesis-generating. Analyses used Python (scikit-learn, pandas).

## Results

Across k = 2–6 the silhouette score was low throughout (0.14–0.16) and highest at **k = 2** (0.16), indicating that adults do not separate into strongly distinct clusters but lie along a dominant continuous axis. The two-cluster solution divided the sample into a metabolic-inflammatory phenotype (37.8% weighted) and a lean, low-inflammation phenotype (62.2%).

The phenotypes differed along a coherent systemic axis (Figure 1a; Table 1). The metabolic-inflammatory phenotype had higher body-mass index (standardized +0.79), HbA1c (+0.63), and log-CRP (+0.71), together with **lower** FVC z-scores (−0.30); the lean phenotype was the mirror image, with higher lung volumes. Grip strength and haemoglobin differed little between groups, so the axis was metabolic-inflammatory rather than sarcopenic or anaemic.

On the four ageing outcomes not used in clustering (Figure 1b; Table 2), the metabolic-inflammatory phenotype had more than double the multimorbidity of the lean phenotype (27.9% vs 10.0%) and more functional limitation (56.3% vs 52.4%). Frailty (37.0% vs 37.6%) and poor self-rated health (39.9% vs 38.5%) were similar, and the groups were closely matched on age and broadly on sex, so the multimorbidity and disability gradients were not simply age effects.

## Discussion

Asked to organise older Indians on lung function and reserve markers without any prior labels, the data returned a single dominant metabolic-inflammatory axis rather than a set of discrete lung-ageing phenotypes. Reduced lung volume travelled with higher adiposity, dysglycaemia, and inflammation, and the metabolic-inflammatory pole of this axis carried a markedly higher burden of multimorbidity and functional limitation, even though these outcomes played no part in defining it. This is external validation of a real signal: the clustering "knew" nothing about multimorbidity, yet separated adults who differ nearly threefold in it.

Two interpretive points follow. First, the low silhouette across all solutions argues against reifying discrete "phenotypes"; lung ageing in this population is better modelled dimensionally, as position along a metabolic-inflammatory gradient, than categorically. This matters because categorical phenotype labels, once coined, tend to be treated as diseases. Second, the axis is metabolic-inflammatory rather than sarcopenic: grip strength and haemoglobin barely distinguished the groups, whereas adiposity, glycaemia, and CRP did. This aligns with prior evidence that reduced lung volume in this setting is embedded in cardiometabolic ageing, and complements companion findings from the same programme that preserved-ratio impairment here is metabolically, not smoking, patterned.

Clinically, the implication is a whole-person reading of low lung function in older Indians: a reduced FVC is a reasonable flag for concurrent metabolic-inflammatory burden and multimorbidity, and might be used to prompt cardiometabolic assessment rather than a narrow respiratory work-up. This is a hypothesis for prospective testing, not a screening recommendation.

**Limitations.** The analysis is cross-sectional and exploratory; clusters are descriptive summaries of a continuous distribution, not diagnostic entities, and the weak separation is itself a central result. Biomarkers were measured once. k-means imposes spherical clusters; alternative algorithms may partition the same gradient differently, though the dominant axis is unlikely to change. Spirometry was field-grade and pre-bronchodilator. Frailty and self-rated health did not distinguish the phenotypes, so the axis captures multimorbidity and disability more than global frailty.

## Conclusions

Lung-function variation in middle-aged and older Indians is organised along a systemic metabolic-inflammatory reserve axis rather than into discrete respiratory phenotypes, and the higher-risk pole of this axis carries excess multimorbidity and functional limitation. Low lung function in this population is best read as one facet of cardiometabolic ageing, supporting a dimensional, whole-person approach.

## Declarations

**Ethics:** Secondary analysis of de-identified public LASI Wave 1 data (ICMR approval and consent obtained by LASI); no additional approval required.

**Funding:** None. **Conflicts of interest:** None declared.

**Data availability:** LASI data via g2aging.org and IIPS; clustering code available from the author on request.

**Author contributions:** The single author conceived, analysed, drafted, and approved the work.

**Declaration of generative AI:** A generative AI assistant was used for language editing and analysis/figure code; all conception, analysis, interpretation, and claims are the author's own, verified against the analysis and primary sources, with full responsibility retained.

## References

1. Wan ES, Balte P, Schwartz JE, Bhatt SP, Cassano PA, Couper D, et al. Association between preserved ratio impaired spirometry and clinical outcomes in US adults. JAMA. 2021;326(22):2287-2298.
2. Wijnant SRA, De Roos E, Kavousi M, Stricker BH, Terzikhan N, Lahousse L, et al. Trajectory and mortality of preserved ratio impaired spirometry: the Rotterdam Study. Eur Respir J. 2020;55(1):1901217.
3. Sonnappa S, Lum S, Kirkby J, Bonner R, Wade A, Subramanya V, et al. Disparities in pulmonary function in healthy children across the Indian urban-rural continuum. Am J Respir Crit Care Med. 2015;191(1):79-86.
4. Perianayagam A, Bloom D, Lee J, Parasuraman S, Sekher TV, Mohanty SK, et al. Cohort profile: the Longitudinal Ageing Study in India (LASI). Int J Epidemiol. 2022;51(4):e167-e176.
5. International Institute for Population Sciences, Harvard T.H. Chan School of Public Health, University of Southern California. Longitudinal Ageing Study in India (LASI) Wave 1, 2017–18: India report. Mumbai: IIPS; 2020.
6. Searle SD, Mitnitski A, Gahbauer EA, Gill TM, Rockwood K. A standard procedure for creating a frailty index. BMC Geriatr. 2008;8:24.

## Tables

**Table 1. Phenotype feature profiles (weighted share and feature means; n = 29,828).**

| Feature | Metabolic-inflammatory (37.8%) | Lean / low-inflammation (62.2%) |
|---|---|---|
| FVC z (national reference) | −0.32 | 0.18 |
| FEV1/FVC z | 0.02 | −0.15 |
| Body-mass index (kg/m²) | 26.7 | 20.9 |
| HbA1c (%) | 6.68 | 5.54 |
| log-CRP | 0.16 | −1.50 |
| Haemoglobin (g/dL) | 13.8 | 13.5 |
| Grip strength (kg) | 24.8 | 25.4 |

Standardized profiles are shown in Figure 1a. Groups were matched on age (57.3 vs 57.8 years).

**Table 2. Ageing outcomes by phenotype (weighted %; outcomes not used in clustering).**

| Outcome | Metabolic-inflammatory | Lean / low-inflammation |
|---|---|---|
| Frailty (index ≥0.25) | 37.0 | 37.6 |
| Functional limitation | 56.3 | 52.4 |
| Multimorbidity (≥2) | 27.9 | 10.0 |
| Poor self-rated health | 39.9 | 38.5 |

## Figure legend

**Figure 1.** (a) Standardized feature profiles of the two data-driven phenotypes; the metabolic-inflammatory phenotype combines higher BMI, HbA1c, and CRP with lower FVC z-scores. (b) Ageing outcomes not used in clustering: the metabolic-inflammatory phenotype has nearly threefold higher multimorbidity and more functional limitation, while frailty and self-rated health are similar.
