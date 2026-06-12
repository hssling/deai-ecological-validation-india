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

## Table 2. Care cascade among all affected (% of affected, weighted, 95% CI)

| condition    | stage      |   pct_of_affected | ci          |
|:-------------|:-----------|------------------:|:------------|
| Diabetes     | aware      |              63.4 | (60.1-68.3) |
| Diabetes     | treated    |              52   | (49.0-56.1) |
| Diabetes     | controlled |              39.6 | (34.8-42.9) |
| Hypertension | aware      |              59   | (55.9-63.9) |
| Hypertension | treated    |              42   | (39.4-45.9) |
| Hypertension | controlled |              35.8 | (31.3-42.7) |

## Table 3. Socioeconomic inequality: Erreygers concentration indices (wealth-ranked)

| indicator                |   erreygers_CI | ci95               | direction                   |
|:-------------------------|---------------:|:-------------------|:----------------------------|
| Undiagnosed diabetes     |        -0.0901 | (-0.1219, -0.0617) | pro-poor (worse among poor) |
| Undiagnosed hypertension |        -0.028  | (-0.0483, -0.0066) | pro-poor (worse among poor) |
| Uncontrolled diabetes    |         0.0272 | (0.0018, 0.0523)   | pro-rich (worse among rich) |
| Dysglycaemia             |         0.0358 | (0.0267, 0.0463)   | pro-rich (worse among rich) |
| Central obesity          |         0.1324 | (0.1182, 0.1467)   | pro-rich (worse among rich) |
| Anaemia                  |        -0.0378 | (-0.0487, -0.0248) | pro-poor (worse among poor) |
| Low grip strength        |        -0.0668 | (-0.0776, -0.0564) | pro-poor (worse among poor) |
| High biological burden   |         0.0291 | (0.0179, 0.0414)   | pro-rich (worse among rich) |

## Table 4. Incremental value for predicting past-year hospitalisation (nested models)

| outcome          | model                                    |     n | AUROC_95CI          |     AIC |
|:-----------------|:-----------------------------------------|------:|:--------------------|--------:|
| hospitalised_12m | M1 age+sex                               | 38155 | 0.548 (0.538-0.558) | 26051.5 |
| hospitalised_12m | M2 +social/behaviour (simple indicators) | 38155 | 0.568 (0.561-0.578) | 25919.7 |
| hospitalised_12m | M3 +self-reported disease                | 38155 | 0.614 (0.606-0.623) | 25351.1 |
| hospitalised_12m | M4 +measured biomarker burden            | 38155 | 0.615 (0.607-0.624) | 25343.1 |
