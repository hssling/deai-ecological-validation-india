# Supplementary Material

## S1. Variable definitions

**Household out-of-pocket (OOP) spending.** Measured at the household level and annualised as: inpatient costs reported for the previous year, plus outpatient costs reported for the previous month (multiplied by 12 to annualise). Outpatient costs include doctors' fees, diagnostic tests, and medicines bought in the course of a treatment episode. All monetary values were deflated to constant 2017 rupees using the survey's consumer price indices.

**Capacity to pay.** Following the World Health Organization's approach to catastrophic health expenditure, capacity to pay was defined as a household's non-food consumption: total household consumption expenditure minus food spending. This is the denominator for the 40%-of-capacity-to-pay (CHE40cap) threshold; total consumption (not net of food) is the denominator for the two budget-share thresholds (CHE10, CHE25).

**Poverty line.** The poverty line used for the impoverishment analysis is Rs 18,307 per year, per capita, in constant 2017 rupees. This line is not an externally imported poverty line; it is anchored to the survey's own poverty measure by taking the weighted per-capita-consumption quantile among adults aged 60 and over that corresponds to the survey's international poverty-line indicator. Pre-payment poverty compares per-capita consumption with this line; post-payment poverty repeats the comparison after subtracting per-capita out-of-pocket spending.

**Multimorbidity.** Two or more self-reported chronic conditions.

**Functional limitation.** A binary indicator set to 1 if a respondent reports one or more limitations in any of three domains: activities of daily living (ADL), instrumental activities of daily living (IADL), or basic mobility, as captured in the LASI functional-status modules. The indicator takes the maximum across the three domain-specific flags.

**Catastrophic health expenditure (CHE).** Reported at three thresholds: spending above 10% of total household consumption (CHE10), above 25% of total household consumption (CHE25), and above 40% of capacity to pay (CHE40cap, the WHO definition). Overshoot is the mean amount, in percentage points, by which spending among the catastrophically spending households exceeds the relevant threshold.

## S2. The 45-and-over sensitivity sample

The primary analytic sample is adults aged 60 and over (n=31,766), the population for which the financing-policy questions in this manuscript are most directly relevant. As a sensitivity check, the analysis was repeated on the full LASI Wave 1 sample of adults aged 45 and over (n=66,470) to confirm that restricting attention to 60+ does not change the qualitative pattern of results. It does not. In the broader 45+ frame, catastrophic spending was somewhat lower than at 60+ but followed the same structure, and out-of-pocket payments impoverished a similar share of households:

- Unweighted n, 45+ frame: 66,470
- CHE10 / CHE25 / CHE40cap, 45+ frame: 32.3% / 11.6% / 17.3% (versus 35.7% / 13.7% / 20.7% at 60+)
- Impoverishment, 45+ frame: pre-payment poverty 18.1%, post-payment 23.1%, additional impoverished 5.0 percentage points (versus 5.8 at 60+)

The gradient between the 45+ and 60+ estimates is itself informative: the financial burden of health care rises with age, which is the expected direction and supports the focus of the main analysis on the older group.

## S3. Full concentration-index decomposition (CHE40cap)

| Regressor | Elasticity | Concentration index of regressor | Contribution to overall CI | % of overall CI |
|---|---|---|---|---|
| Age (years) | 0.0556 | -0.00041 | -0.0000229 | -0.03 |
| Female | -0.0412 | -0.01086 | 0.000447 | 0.50 |
| Rural residence | 0.2559 | -0.08853 | -0.02266 | -25.10 |
| Multimorbidity (2+) | 0.0971 | 0.18684 | 0.01815 | 20.11 |
| Functional limitation | 0.1856 | -0.01368 | -0.00254 | -2.81 |
| Any pension | -0.0035 | 0.29083 | -0.00103 | -1.14 |
| Education | -0.0105 | 0.27642 | -0.00290 | -3.21 |

**Overall concentration index: +0.0902. Erreygers (corrected) index: +0.0748.**

*Reading the table.* The concentration index ranks households from poorest to richest by per-capita consumption. Elasticity is the percentage change in CHE40cap associated with a 1% change in the regressor, evaluated at sample means. The concentration index of the regressor describes how that regressor itself is distributed across the consumption ranking (for example, rural residence has a negative concentration index because rural households cluster towards the poorer end). The contribution of each regressor is its elasticity multiplied by its own concentration index; summing the contributions reproduces the overall concentration index. A negative contribution pulls the index in the pro-poor direction (the regressor is associated with poorer households bearing more of the catastrophic-spending burden); a positive contribution pulls it in the pro-rich direction.

## S4. Full two-part model coefficients

### Part 1 — probability of any out-of-pocket spending (logistic regression)

| Predictor | Coefficient | Odds ratio | 95% CI | P value |
|---|---|---|---|---|
| Constant | 0.700 | 2.01 | 1.53-2.65 | <0.001 |
| Age (per year) | -0.0012 | 1.00 | 0.99-1.00 | 0.540 |
| Female | -0.108 | 0.90 | 0.85-0.95 | <0.001 |
| Rural residence | 0.278 | 1.32 | 1.24-1.41 | <0.001 |
| Multimorbidity (2+) | 0.540 | 1.72 | 1.59-1.85 | <0.001 |
| Functional limitation | 0.463 | 1.59 | 1.49-1.69 | <0.001 |
| Any pension | 0.019 | 1.02 | 0.94-1.11 | 0.657 |
| Education (per year) | 0.041 | 1.04 | 1.02-1.06 | <0.001 |

### Part 2 — amount spent among spenders (gamma regression, log link)

| Predictor | Coefficient | Exponentiated coefficient | 95% CI | P value |
|---|---|---|---|---|
| Constant | 9.832 | 18,622.2 | 14,455.0-23,990.7 | <0.001 |
| Age (per year) | 0.0029 | 1.00 | 1.00-1.01 | 0.105 |
| Female | -0.0018 | 1.00 | 0.95-1.05 | 0.949 |
| Rural residence | 0.0064 | 1.01 | 0.95-1.07 | 0.833 |
| Multimorbidity (2+) | 0.379 | 1.46 | 1.38-1.55 | <0.001 |
| Functional limitation | 0.054 | 1.06 | 0.99-1.12 | 0.080 |
| Any pension | 0.172 | 1.19 | 1.10-1.28 | <0.001 |
| Education (per year) | 0.065 | 1.07 | 1.05-1.08 | <0.001 |

*Note.* Part 1 is a logistic regression for the probability of reporting any out-of-pocket spending; odds ratios above 1 indicate higher odds of spending something. Part 2 is a gamma regression with a log link, fitted only among households that reported any spending; exponentiated coefficients above 1 indicate a higher conditional amount. This is the standard two-part treatment for health-cost data, in which a large mass of zero or near-zero spenders sits alongside a long right tail among spenders.

## S5. Gradient-boosting / SHAP importance (CHE40cap)

| Predictor | Mean \|SHAP value\| |
|---|---|
| Rural residence | 0.215 |
| Multimorbidity (2+) | 0.150 |
| Functional limitation | 0.128 |
| Age | 0.057 |
| Education | 0.040 |
| Female | 0.034 |
| Any pension | 0.018 |

SHAP importance ranks the average magnitude of each predictor's contribution to the gradient-boosting model's prediction of catastrophic spending. As in the main text, this is reported as a predictive ranking and should not be read as a causal effect estimate.

## S6. Caveats: medicines under-capture and the ceiling assumption in the combined scenario

**Medicines and outpatient under-capture.** The household outpatient measure used here captures medicines bought in the course of a treatment episode (that is, alongside a consultation or diagnostic visit) but may under-record standalone pharmacy purchases that older adults make for chronic conditions without an accompanying visit — a common pattern for stable hypertension, diabetes or arthritis management in India. If this under-capture is material, the true outpatient and medicines burden, and the catastrophic-spending reduction achievable by covering it (Scenario S2, Table 6), are both probably larger than estimated here. This is the basis for describing the central inpatient-versus-outpatient comparison in the manuscript as conservative rather than overstated: the true gap between the two policy levers is, if anything, likely to be wider than the 1.8-versus-16.1-percentage-point figures reported.

**The combined scenario is a ceiling, not a costed package.** Scenario S4 (Table 6) combines full inpatient cover, full outpatient and medicine cover, and the pension top-up, and shows catastrophic spending falling to zero at every threshold. This is a mechanical consequence of assuming 100% uptake and 100% reimbursement of every covered cost simultaneously across all three levers — an assumption no real financing scheme achieves, owing to incomplete enrolment, co-payments, provider gaps, and claims friction. S4 should be read as an analytic upper bound that establishes how much catastrophic spending is, in principle, addressable by financing reform, not as a forecast of what any single combined programme would deliver. The substantive policy comparison in this manuscript is between S1 and S2, both of which are single-lever scenarios and therefore more directly informative about where reform effort should be concentrated.

**Care-worker wage assumption.** The replacement-cost valuation of unpaid family caregiving (Table 7) depends on the assumed hourly wage for a care worker. This wage was not independently varied in the present analysis; the opportunity-cost variant uses the same wage rate and therefore does not provide an independent cross-check in this run. Readers should treat the Rs 1.3-lakh-crore national valuation as indicative of order of magnitude rather than as a precise national account entry.
