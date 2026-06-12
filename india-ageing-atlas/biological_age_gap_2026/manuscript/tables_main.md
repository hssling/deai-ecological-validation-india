# Tables (main text)

## Table 1. The diagnosis gap: biologically measured vs self-reported disease (weighted %, 95% CI)

| indicator                                | weighted_pct_95CI   |     n |
|:-----------------------------------------|:--------------------|------:|
| Self-reported diabetes                   | 12.0 (11.5–12.4)    | 66280 |
| Biochemical diabetes (HbA1c>=6.5)        | 15.3 (14.7–15.9)    | 58289 |
| Undiagnosed among biochemically diabetic | 51.3 (49.8–52.7)    |  9365 |
| Self-reported hypertension               | 26.1 (25.5–26.7)    | 66283 |
| Measured hypertension (>=140/90 mmHg)    | 31.3 (30.6–31.9)    | 60373 |
| Undiagnosed among measured-hypertensive  | 63.8 (62.8–65.0)    | 20554 |
| Anaemia                                  | 29.9 (29.2–30.7)    | 58294 |
| Elevated CRP (>3 mg/L)                   | 9.6 (9.2–9.9)       | 58288 |
| Central obesity (IDF Asian)              | 47.3 (46.2–48.3)    | 59789 |
| High subclinical burden (>=3 systems)    | 23.2 (22.6–23.9)    | 58151 |

## Table 2. Social patterning of undiagnosed disease and high biological burden (weighted %)

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

## Table 3. Incremental value for predicting past-year hospitalisation (nested models)

| outcome          | model                                    |     n | AUROC_95CI          |     AIC |
|:-----------------|:-----------------------------------------|------:|:--------------------|--------:|
| hospitalised_12m | M1 age+sex                               | 38155 | 0.548 (0.538-0.558) | 26051.5 |
| hospitalised_12m | M2 +social/behaviour (simple indicators) | 38155 | 0.568 (0.561-0.578) | 25919.7 |
| hospitalised_12m | M3 +self-reported disease                | 38155 | 0.614 (0.606-0.623) | 25351.1 |
| hospitalised_12m | M4 +measured biomarker burden            | 38155 | 0.615 (0.607-0.624) | 25343.1 |

## Table 4. Hidden burden among the self-reported healthy

| group                                              | high_burden_pct_95CI           |     n |
|:---------------------------------------------------|:-------------------------------|------:|
| Self-reported healthy (0 diagnosed conditions)     | 15.5 (14.9–16.1)               | 31272 |
| OR hospitalisation per +1 burden (healthy-looking) | OR=1.10 (1.03-1.18); p=7.4e-03 | 17360 |
