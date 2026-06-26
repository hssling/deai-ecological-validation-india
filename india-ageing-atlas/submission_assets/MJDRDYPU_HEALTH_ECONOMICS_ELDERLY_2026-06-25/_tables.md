# Tables

## Table 1. Characteristics of the analytic sample, adults aged 60 and over (LASI Wave 1)

| Characteristic | Value |
|---|---|
| Unweighted sample size | 31,766 |
| Female | 50.8% |
| Rural residence | 69.3% |
| Multimorbidity (2+ chronic conditions) | 23.2% |
| Functional limitation | 70.8% |
| Living alone | 5.5% |
| Receiving any pension | 13.6% |
| Any out-of-pocket health spending | 77.3% |
| Annual out-of-pocket spending, median (mean) | Rs 7,155 (Rs 23,230) |
| Annual household consumption, median (mean) | Rs 140,155 (Rs 183,583) |

*Note.* Figures are weighted percentages or weighted medians/means unless stated as unweighted counts; out-of-pocket spending and consumption are household-level, annualised, and expressed in constant 2017 rupees.

## Table 2. Catastrophic health expenditure (CHE) by threshold and group

| Group | n | CHE >10% of consumption, % (overshoot, pp) | CHE >25% of consumption, % (overshoot, pp) | CHE >40% of capacity-to-pay, % (overshoot, pp) |
|---|---|---|---|---|
| All 60+ | 31,766 | 35.7 (5.6) | 13.7 (2.2) | 20.7 (4.3) |
| 70+ | 12,550 | 37.0 (5.7) | 14.0 (2.2) | 21.2 (4.5) |
| Men 60+ | 15,294 | 36.2 (5.7) | 14.0 (2.3) | 21.0 (4.3) |
| Women 60+ | 16,472 | 35.2 (5.4) | 13.3 (2.1) | 20.5 (4.2) |
| Rural 60+ | 20,961 | 37.0 (5.9) | 14.4 (2.3) | 22.9 (4.8) |
| Urban 60+ | 10,805 | 32.9 (4.9) | 12.0 (1.9) | 15.9 (3.0) |
| Multimorbid 60+ | 7,576 | 46.5 (8.0) | 20.0 (3.3) | 26.7 (5.7) |

*Note.* CHE10 and CHE25 are the shares of households whose annualised out-of-pocket health spending exceeds 10% and 25% of total household consumption, respectively. CHE40cap (the WHO definition) is the share exceeding 40% of capacity to pay, defined as household consumption net of food spending. Overshoot is the mean amount by which spending exceeds the threshold, expressed in percentage points. n is the unweighted group size; percentages are survey-weighted.

## Table 3. Impoverishment from out-of-pocket health spending

| Group | n | Poverty line (Rs/year, per capita) | Pre-payment poverty, % | Post-payment poverty, % | Impoverishment headcount, pp | Poverty gap increase, pp |
|---|---|---|---|---|---|---|
| All 60+ | 31,766 | 18,307 | 19.6 | 25.4 | 5.8 | 1.8 |
| Men 60+ | 15,294 | 18,307 | 19.3 | 25.1 | 5.8 | 1.8 |
| Women 60+ | 16,472 | 18,307 | 19.9 | 25.7 | 5.7 | 1.9 |
| Rural 60+ | 20,961 | 18,307 | 23.7 | 30.5 | 6.8 | 2.3 |
| Urban 60+ | 10,805 | 18,307 | 10.3 | 13.7 | 3.4 | 0.8 |

*Note.* Pre-payment poverty is the share of older adults below the poverty line using per-capita consumption; post-payment poverty repeats this after subtracting per-capita out-of-pocket health spending. The impoverishment headcount is the percentage-point difference (post minus pre) — the share of older adults pushed below the line by medical spending alone. The poverty gap increase is the corresponding rise in the normalised mean shortfall below the line. n is the unweighted group size; percentages are survey-weighted.

## Table 4. Concentration-index decomposition of catastrophic health expenditure (CHE40cap)

| Regressor | Elasticity | Concentration index of regressor | Contribution to overall CI | % of overall CI |
|---|---|---|---|---|
| Age (years) | 0.056 | -0.0004 | -0.00002 | -0.03 |
| Female | -0.041 | -0.0109 | 0.0004 | 0.50 |
| Rural residence | 0.256 | -0.0885 | -0.0227 | -25.10 |
| Multimorbidity (2+) | 0.097 | 0.1868 | 0.0181 | 20.11 |
| Functional limitation | 0.186 | -0.0137 | -0.0025 | -2.81 |
| Any pension | -0.004 | 0.2908 | -0.0010 | -1.14 |
| Education | -0.010 | 0.2764 | -0.0029 | -3.21 |

**Overall concentration index (CHE40cap): +0.090. Erreygers (corrected) index: +0.075.**

*Note.* The concentration index ranks households by per-capita consumption; a positive value indicates catastrophic spending is more concentrated among better-off households. The Erreygers index corrects the concentration index for the bounded (0/1) nature of the CHE outcome. Elasticity is the response of CHE40cap to a 1% change in the regressor; the concentration index of the regressor describes how that regressor itself is distributed across the consumption ranking; the contribution is elasticity multiplied by the regressor's concentration index, and the percentage of the overall CI is each contribution divided by the total concentration index. Negative contributions pull the index in the pro-poor direction; positive contributions pull it in the pro-rich direction.

## Table 5. Drivers of out-of-pocket spending: two-part model and SHAP importance

### 5a. Two-part model — part 1, probability of any out-of-pocket spending (logistic regression)

| Predictor | Odds ratio | 95% CI | P value |
|---|---|---|---|
| Age (per year) | 1.00 | 0.99-1.00 | 0.540 |
| Female | 0.90 | 0.85-0.95 | <0.001 |
| Rural residence | 1.32 | 1.24-1.41 | <0.001 |
| Multimorbidity (2+) | 1.72 | 1.59-1.85 | <0.001 |
| Functional limitation | 1.59 | 1.49-1.69 | <0.001 |
| Any pension | 1.02 | 0.94-1.11 | 0.657 |
| Education (per year) | 1.04 | 1.02-1.06 | <0.001 |

### 5b. Two-part model — part 2, amount spent among spenders (gamma regression, log link)

| Predictor | Exponentiated coefficient | 95% CI | P value |
|---|---|---|---|
| Age (per year) | 1.00 | 1.00-1.01 | 0.105 |
| Female | 1.00 | 0.95-1.05 | 0.949 |
| Rural residence | 1.01 | 0.95-1.07 | 0.833 |
| Multimorbidity (2+) | 1.46 | 1.38-1.55 | <0.001 |
| Functional limitation | 1.06 | 0.99-1.12 | 0.080 |
| Any pension | 1.19 | 1.10-1.28 | <0.001 |
| Education (per year) | 1.07 | 1.05-1.08 | <0.001 |

### 5c. Gradient-boosting model — mean absolute SHAP importance for catastrophic spending (CHE40cap)

| Predictor | Mean \|SHAP value\| |
|---|---|
| Rural residence | 0.215 |
| Multimorbidity (2+) | 0.150 |
| Functional limitation | 0.128 |
| Age | 0.057 |
| Education | 0.040 |
| Female | 0.034 |
| Any pension | 0.018 |

*Note.* Part 1 odds ratios describe the likelihood of reporting any out-of-pocket spending; Part 2 ratios describe the multiplicative effect on the amount spent, conditional on spending something (gamma regression with a log link, the standard treatment for skewed cost data). SHAP (SHapley Additive exPlanations) importance ranks each predictor's average contribution to the gradient-boosting model's prediction of catastrophic spending; this is a predictive ranking, not a causal estimate.

## Table 6. Microsimulation of financing-reform scenarios

| Scenario | Coverage | CHE10, % (Δ pp) | CHE25, % (Δ pp) | CHE40cap, % (Δ pp) | Post-payment poverty, % (Δ pp) | Fiscal cost, Rs crore |
|---|---|---|---|---|---|---|
| S1: PM-JAY 70+ full inpatient cover | Full inpatient, age 70+ | 33.2 (-2.5) | 12.1 (-1.6) | 18.8 (-2.0) | 24.8 (-0.5) | 31,654 |
| S2: Outpatient and medicines cover, all 60+ | Full outpatient/medicine, age 60+ | 6.8 (-29.0) | 2.5 (-11.2) | 2.9 (-17.8) | 20.3 (-5.0) | 264,825 |
| S3: Pension top-up (+Rs 500/month), all 60+ | Income support, age 60+ | 34.2 (-1.5) | 12.6 (-1.1) | 16.6 (-4.2) | 9.1 (-16.3) | 89,400 |
| S4: Combined S1+S2+S3 | Full inpatient + outpatient + pension top-up | 0.0 (-35.7) | 0.0 (-13.7) | 0.0 (-20.7) | 6.5 (-18.9) | 435,527 |

*Note.* All scenarios are applied to the same adults-aged-60-and-over sample, so every Δ pp is measured against the common 60+ baseline (CHE10 35.7%, CHE25 13.7%, CHE40cap 20.7%, post-payment poverty 25.4%); negative values denote a reduction. S1 only covers those aged 70 and over within that sample, which is why its reduction is modest at the population level. All scenarios assume full coverage of the modelled cost (complete uptake and full reimbursement) and should be read as upper-bound ceilings rather than realistic programme costings, particularly the combined scenario S4. Fiscal costs are in Rs crore (1 crore = 10 million rupees), scaled using the national older-population count and benchmark unit costs; they are not a substitute for a costed budget line.

## Table 7. The economic value of unpaid family caregiving

| Indicator | Value |
|---|---|
| Older adults receiving regular informal care | 12.2% |
| Mean hours of care received per week | 13.9 |
| Annual replacement-cost value per recipient | Rs 71,000 |
| National annual replacement-cost value | Rs 1,29,117 crore (~Rs 1.3 lakh crore) |

*Note.* Care hours are self-reported help with daily activities from spouses, children and other relatives. Values shown use the replacement-cost method: care hours costed at a representative care-worker wage. The opportunity-cost variant was run with the same wage rate in this analysis and so reproduces identical figures; it is not an independent estimate of forgone earnings. The national total represents an annual flow, not a one-off transfer, and does not appear in any official health account.
