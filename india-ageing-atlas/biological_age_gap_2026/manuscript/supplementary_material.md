# Supplementary material

## Table S1. Included (clock-eligible, ≥5 biomarkers) vs excluded participants

| variable             |   included_mean |   included_n |   excluded_mean |   excluded_n |    abs_diff |
|:---------------------|----------------:|-------------:|----------------:|-------------:|------------:|
| age_years            |       59.4885   |        59638 |       61.1401   |         6832 | -1.65158    |
| education_years      |        4.14938  |        59638 |        4.6127   |         6832 | -0.46332    |
| frailty_index        |        0.249002 |        59601 |        0.262172 |         5462 | -0.0131706  |
| multimorbidity_ge2   |        0.18391  |        59638 |        0.198624 |         6832 | -0.0147145  |
| poor_srh             |        0.377581 |        59619 |        0.371659 |         5949 |  0.00592187 |
| adl_limitation       |        0.137882 |        59616 |        0.210085 |         6564 | -0.0722029  |
| poverty              |        0.169847 |        59636 |        0.158958 |         6832 |  0.0108892  |
| current_smoking      |        0.137618 |        59556 |        0.122036 |         6326 |  0.0155823  |
| unclean_cooking_fuel |        0.466547 |        58665 |        0.394874 |         6516 |  0.0716732  |

## Table S2. Inverse-probability-of-availability weighting sensitivity (max diff 0.3 pp)

| indicator                    |   person_weight_% |   IPW_% |   abs_diff |
|:-----------------------------|------------------:|--------:|-----------:|
| Undiagnosed diabetes (%)     |              51.3 |    51   |      -0.28 |
| Undiagnosed hypertension (%) |              63.8 |    63.6 |      -0.24 |
| Biochemical diabetes (%)     |              15.3 |    15.4 |       0.15 |
| Measured hypertension (%)    |              31.3 |    31.2 |      -0.07 |
| Anaemia (%)                  |              29.9 |    29.9 |      -0.03 |
| High burden >=3 (%)          |              23.2 |    23.4 |       0.16 |

## Table S3. Cluster-bootstrap robustness for key regression estimates (SSU resampling)

| quantity                                                          | estimate               |
|:------------------------------------------------------------------|:-----------------------|
| Undiagnosed diabetes urban-vs-rural OR (cluster bootstrap)        | 0.65 (0.58-0.74)       |
| delta-AUROC biomarker burden over self-report (cluster bootstrap) | 0.0011 (0.0000-0.0028) |

## Table S4. Social patterning of undiagnosed disease and high burden (weighted %)

| stratum    | group        |   undx_diabetes_pct |   undx_htn_pct |   high_burden_pct |
|:-----------|:-------------|--------------------:|---------------:|------------------:|
| residence  | rural        |                57.8 |           68   |              19.6 |
| residence  | urban        |                44   |           56.5 |              31.2 |
| sex        | female       |                51.4 |           58.5 |              27.4 |
| sex        | male         |                51.2 |           68.6 |              19.5 |
| edu_grp    | No education |                59.6 |           66.5 |              21.7 |
| edu_grp    | 1-5 yr       |                49.5 |           62.3 |              23.7 |
| edu_grp    | 6+ yr        |                44.3 |           60.5 |              25.5 |
| wealth_grp | Poorest      |                54.8 |           63.5 |              22.9 |
| wealth_grp | Middle       |                54.7 |           67.3 |              20.9 |
| wealth_grp | Richest      |                45.4 |           60.6 |              26.3 |

## Table S5. Care cascade by social group (% of affected)

| stratum    | group        |   dm_aware |   dm_treated |   dm_controlled |   htn_aware |   htn_treated |   htn_controlled |
|:-----------|:-------------|-----------:|-------------:|----------------:|------------:|--------------:|-----------------:|
| residence  | rural        |       57.8 |         44.3 |            42.4 |        54.9 |          35.4 |             33.7 |
| residence  | urban        |       69.5 |         60.1 |            36.7 |        65.6 |          52.7 |             39.1 |
| edu_grp    | No education |       57.2 |         44.3 |            43.9 |        56.8 |          37.8 |             35   |
| edu_grp    | 1-5 yr       |       64.4 |         52.6 |            39.3 |        60   |          43.9 |             35.7 |
| edu_grp    | 6+ yr        |       68.8 |         58.8 |            35.8 |        61.8 |          47.3 |             36.9 |
| wealth_grp | Poorest      |       61.3 |         49.1 |            42   |        59   |          40.3 |             35.5 |
| wealth_grp | Middle       |       59.9 |         47.8 |            39.6 |        56.1 |          39   |             34.8 |
| wealth_grp | Richest      |       68.2 |         57.8 |            37.8 |        61.8 |          46.8 |             37   |

## Table S6. Domain prevalence by social group (the dual burden)

| stratum    | group        |     n |   Dysglycaemia |   Hypertension(meas) |   Central obesity |   Anaemia |   Low grip |   Low lung reserve |   Inflammation |
|:-----------|:-------------|------:|---------------:|---------------------:|------------------:|----------:|-----------:|-------------------:|---------------:|
| residence  | rural        | 43112 |           11.7 |                 29   |              39.5 |      31.4 |       21.2 |               32.1 |            8.9 |
| residence  | urban        | 23358 |           23.2 |                 36.2 |              64.5 |      26.7 |       18.5 |               39.9 |           11.1 |
| edu_grp    | No education | 31231 |           11.6 |                 29.9 |              41.1 |      33.7 |       25.1 |               32.5 |            9.8 |
| edu_grp    | 1-5 yr       | 12156 |           16.8 |                 31.6 |              46.6 |      27.8 |       19.5 |               35.9 |            9.9 |
| edu_grp    | 6+ yr        | 23083 |           20.6 |                 33.4 |              57.9 |      24.9 |       12.9 |               36.4 |            9   |
| wealth_grp | Poorest      | 22097 |           14.2 |                 31.4 |              42.7 |      31.9 |       24.2 |               33.4 |            9.6 |
| wealth_grp | Middle       | 22097 |           13.7 |                 29.3 |              43.3 |      29.7 |       19.3 |               33.9 |            9.4 |
| wealth_grp | Richest      | 22097 |           18.3 |                 33.4 |              56.8 |      28.1 |       17.4 |               36.1 |            9.7 |

## Table S7. Adjusted predictors of each biological domain (odds ratios)

| domain             | predictor                 |    OR |   ci_lo |   ci_hi |           p |
|:-------------------|:--------------------------|------:|--------:|--------:|------------:|
| Dysglycaemia       | C(residence)[T.urban]     | 1.414 |   1.291 |   1.55  | 1.11203e-13 |
| Dysglycaemia       | education_years           | 1.029 |   1.021 |   1.036 | 3.06624e-14 |
| Dysglycaemia       | poverty                   | 0.842 |   0.763 |   0.93  | 0.000635575 |
| Dysglycaemia       | current_smoking           | 0.686 |   0.619 |   0.76  | 5.19403e-13 |
| Dysglycaemia       | current_smokeless_tobacco | 0.766 |   0.703 |   0.834 | 8.31411e-10 |
| Dysglycaemia       | unclean_cooking_fuel      | 0.511 |   0.468 |   0.559 | 1.77237e-49 |
| Dysglycaemia       | unimproved_drinking_water | 1.276 |   1.137 |   1.432 | 3.51027e-05 |
| Hypertension(meas) | C(residence)[T.urban]     | 1.199 |   1.117 |   1.287 | 5.35432e-07 |
| Hypertension(meas) | education_years           | 1.008 |   1.002 |   1.014 | 0.0128352   |
| Hypertension(meas) | poverty                   | 0.961 |   0.898 |   1.029 | 0.253034    |
| Hypertension(meas) | current_smoking           | 0.82  |   0.761 |   0.883 | 1.37557e-07 |
| Hypertension(meas) | current_smokeless_tobacco | 1.028 |   0.966 |   1.094 | 0.384287    |
| Hypertension(meas) | unclean_cooking_fuel      | 0.798 |   0.75  |   0.849 | 9.67934e-13 |
| Hypertension(meas) | unimproved_drinking_water | 1.119 |   1.018 |   1.23  | 0.0202514   |
| Central obesity    | C(residence)[T.urban]     | 1.565 |   1.437 |   1.704 | 5.39275e-25 |
| Central obesity    | education_years           | 1.074 |   1.066 |   1.081 | 4.478e-87   |
| Central obesity    | poverty                   | 0.628 |   0.583 |   0.675 | 9.25346e-36 |
| Central obesity    | current_smoking           | 0.655 |   0.605 |   0.708 | 4.29615e-26 |
| Central obesity    | current_smokeless_tobacco | 0.726 |   0.68  |   0.776 | 3.95424e-21 |
| Central obesity    | unclean_cooking_fuel      | 0.524 |   0.489 |   0.561 | 4.30423e-75 |
| Central obesity    | unimproved_drinking_water | 1.313 |   1.165 |   1.479 | 7.57269e-06 |
| Anaemia            | C(residence)[T.urban]     | 0.875 |   0.805 |   0.952 | 0.00178545  |
| Anaemia            | education_years           | 0.991 |   0.984 |   0.997 | 0.00667179  |
| Anaemia            | poverty                   | 1.15  |   1.072 |   1.234 | 0.000104437 |
| Anaemia            | current_smoking           | 0.967 |   0.894 |   1.046 | 0.400821    |
| Anaemia            | current_smokeless_tobacco | 1.085 |   1.018 |   1.157 | 0.0116796   |
| Anaemia            | unclean_cooking_fuel      | 1.078 |   1.01  |   1.151 | 0.0236181   |
| Anaemia            | unimproved_drinking_water | 0.978 |   0.87  |   1.098 | 0.704589    |
| Low grip           | C(residence)[T.urban]     | 0.976 |   0.865 |   1.101 | 0.691104    |
| Low grip           | education_years           | 0.94  |   0.932 |   0.949 | 1.77749e-42 |
| Low grip           | poverty                   | 1.161 |   1.068 |   1.261 | 0.000429152 |
| Low grip           | current_smoking           | 0.839 |   0.764 |   0.921 | 0.000217141 |
| Low grip           | current_smokeless_tobacco | 0.876 |   0.809 |   0.948 | 0.00100711  |
| Low grip           | unclean_cooking_fuel      | 0.886 |   0.805 |   0.975 | 0.0129175   |
| Low grip           | unimproved_drinking_water | 1.431 |   1.225 |   1.672 | 6.03759e-06 |
| Low lung reserve   | C(residence)[T.urban]     | 1.331 |   1.202 |   1.474 | 3.5798e-08  |
| Low lung reserve   | education_years           | 0.989 |   0.981 |   0.997 | 0.00724663  |
| Low lung reserve   | poverty                   | 1.088 |   0.991 |   1.195 | 0.076111    |
| Low lung reserve   | current_smoking           | 1.037 |   0.938 |   1.147 | 0.47723     |
| Low lung reserve   | current_smokeless_tobacco | 1.013 |   0.93  |   1.103 | 0.76859     |
| Low lung reserve   | unclean_cooking_fuel      | 0.816 |   0.747 |   0.892 | 7.63228e-06 |
| Low lung reserve   | unimproved_drinking_water | 1.232 |   1.064 |   1.427 | 0.00525613  |
| Inflammation       | C(residence)[T.urban]     | 1.254 |   1.139 |   1.381 | 3.99166e-06 |
| Inflammation       | education_years           | 0.986 |   0.977 |   0.996 | 0.00381386  |
| Inflammation       | poverty                   | 1.076 |   0.97  |   1.192 | 0.16538     |
| Inflammation       | current_smoking           | 1.173 |   1.045 |   1.316 | 0.00677913  |
| Inflammation       | current_smokeless_tobacco | 0.818 |   0.74  |   0.904 | 8.56771e-05 |
| Inflammation       | unclean_cooking_fuel      | 0.864 |   0.792 |   0.944 | 0.00114584  |
| Inflammation       | unimproved_drinking_water | 1.056 |   0.902 |   1.236 | 0.497376    |

## Table S8. State/UT surveillance: burden and undiagnosed fraction

| state                  |    n |   mean_burden |   undx_diabetes_pct |   high_burden_pct |
|:-----------------------|-----:|--------------:|--------------------:|------------------:|
| Andhra Pradesh         | 2001 |         2.379 |                48.2 |              45.7 |
| Chandigarh             |  788 |         2.203 |                47.2 |              39.7 |
| Punjab                 | 1831 |         2.136 |                44.3 |              35.3 |
| Telangana              | 1940 |         2.105 |                57.6 |              34.3 |
| Maharashtra            | 3050 |         2.03  |                48.8 |              33.8 |
| Delhi                  | 1141 |         2.039 |                52.6 |              32.4 |
| Sikkim                 |  879 |         2.059 |                64.1 |              32.3 |
| Lakshadweep            | 1014 |         2.038 |                40.8 |              30.8 |
| Kerala                 | 2119 |         1.985 |                38   |              30.1 |
| Daman and Diu          |  849 |         1.868 |                42.6 |              28.8 |
| Puducherry             | 1165 |         1.92  |                38.2 |              28.4 |
| Andaman and Nicobar    | 1020 |         1.849 |                45.2 |              27.9 |
| Jammu and Kashmir      | 1288 |         1.845 |                62.3 |              26.4 |
| Tamil Nadu             | 2990 |         1.813 |                45.9 |              26.3 |
| Goa                    | 1119 |         1.84  |                31.4 |              25.7 |
| Gujarat                | 1919 |         1.736 |                48.2 |              24   |
| Odisha                 | 2385 |         1.68  |                59.3 |              23.4 |
| West Bengal            | 3069 |         1.662 |                46.5 |              23.4 |
| Dadra and Nagar Haveli |  909 |         1.591 |                55.7 |              22.8 |
| Meghalaya              |  876 |         1.728 |                58.8 |              22.2 |
| Jharkhand              | 2082 |         1.696 |                53.6 |              22.2 |
| Himachal Pradesh       | 1184 |         1.658 |                34.9 |              20.9 |
| Uttarakhand            | 1183 |         1.604 |                50.1 |              20.1 |
| Karnataka              | 1913 |         1.598 |                42.6 |              19.7 |
| Haryana                | 1582 |         1.621 |                60.7 |              18.7 |
| Chhatisgarh            | 1803 |         1.586 |                65.4 |              18.4 |
| Manipur                | 1089 |         1.59  |                55.8 |              18.4 |
| Uttar Pradesh          | 3917 |         1.425 |                59.9 |              15.9 |
| Tripura                |  951 |         1.429 |                55.5 |              15.5 |
| Rajasthan              | 1975 |         1.459 |                59.8 |              15   |
| Assam                  | 1805 |         1.492 |                57.3 |              14.9 |
| Mizoram                | 1018 |         1.39  |                49.2 |              14.8 |
| Bihar                  | 3187 |         1.409 |                64.1 |              14.8 |
| Arunachal Pradesh      |  926 |         1.374 |                82.3 |              14.1 |
| Madhya Pradesh         | 2446 |         1.308 |                69.2 |              13.3 |
| Nagaland               | 1117 |         1.297 |                71.8 |              11.5 |

## Table S9. Biomarker–chronological age associations (weighted) — context for retiring the KDM clock

| biomarker   |   slope_per_yr |            p |          r2 |     n |
|:------------|---------------:|-------------:|------------:|------:|
| logcrp      |     0.00511929 | 7.24351e-19  | 0.00134927  | 58288 |
| hba1c_v     |     0.00263702 | 6.98035e-10  | 0.000652188 | 58289 |
| hb_v        |    -0.0286405  | 1.04895e-200 | 0.0155519   | 58294 |
| sbp         |     0.37852    | 0            | 0.0444968   | 60373 |
| pulse       |    -0.0729705  | 8.6422e-59   | 0.00432002  | 60373 |
| fev1_raw    |    -0.0175571  | 0            | 0.0865071   | 50244 |
| grip        |    -0.281431   | 0            | 0.130105    | 59137 |
| waist       |    -0.0956902  | 1.28518e-80  | 0.00602934  | 59789 |

## Supplementary Note S10. Why a chronological-age-calibrated biological-age clock is not the primary measure

We pre-registered an intention to compute Klemera–Doubal Method (KDM) biological age. On implementation
(faithful port of the BioAge package, sex-specific, survey-weighted training), the clock proved
ill-conditioned in these data: the characteristic variance s_BA^2 was negative and the implied biological-
age acceleration had an implausible standard deviation (~26 years), with negative convergent validity
against multi-system physiological dysregulation and allostatic load. The cause is visible in Table S9:
the LASI biomarker panel (lacking renal, hepatic and lipid chemistries) is only weakly correlated with
chronological age in this 45+ population (most r^2 < 0.05), and the population carries two opposing ageing
phenotypes — cardiometabolic excess and frailty/wasting — so a single age-anchored latent score is not
well defined. We therefore do not report KDM biological age as a primary or secondary result, and instead
use externally-thresholded abnormalities and their two clinically coherent axes. This is reported
transparently rather than omitted.
