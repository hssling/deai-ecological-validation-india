# Catastrophic health spending, impoverishment and the unpaid-care economy among older adults in India: a household health-economic analysis of LASI Wave 1, with policy microsimulation and projections to 2050

## Abstract

**Background & objectives:** India's financial protection for older people is built around hospital insurance, yet much of what ageing households spend on health is incurred outside hospital. We estimated out-of-pocket spending among older Indians, identified who bears it and what drives it, valued unpaid family care, and tested which reform would relieve it most.

**Methods:** This cross-sectional analysis of LASI Wave 1 (2017–18) studied 31,766 adults aged 60 yr and older. Household out-of-pocket spending was set against the World Health Organization capacity-to-pay denominator. We estimated catastrophic health expenditure (CHE), impoverishment, income-related inequality, drivers (two-part and gradient-boosting models), the value of unpaid care, State-level burden, four financing-reform microsimulations with cost-effectiveness, and a projection to 2050.

**Results:** CHE exceeded 40 per cent of capacity to pay in 20.7 per cent of older households and a tenth of consumption in 35.7 per cent. Out-of-pocket payments impoverished an additional 5.8 per cent of older people, with rural areas worst affected. Rural residence, multimorbidity and functional limitation were the strongest drivers. Unpaid family care was worth about Rs 1.3 lakh crore a year. Covering inpatient care removed 2.0 percentage points of CHE; covering outpatient and medicine costs removed 17.8, the most cost-effective lever. On demographic momentum alone, the catastrophic-spending caseload is projected to rise from 31 to 72 million by 2050.

**Interpretation & conclusions:** Catastrophic spending in later life originates outside hospital. Outpatient and medicine cover, not inpatient insurance alone, is the missing pillar of elder-care financing in India.

**Keywords:** Aged; Catastrophic illness; Caregivers; Health expenditures; Health policy; India.

## Introduction

The way a country pays for the health of its older citizens reveals what it believes ageing costs. India has largely answered that question with hospital insurance. The Pradhan Mantri Jan Arogya Yojana (PM-JAY) offers cover of up to Rs 5 lakh per family for inpatient care^1^, and a 2024 expansion extended eligibility to every resident aged 70 yr and above^2^. This is a substantial commitment. It also rests on an assumption worth testing: that the financial danger of growing old lies mainly in hospitalisation.

For an older person managing diabetes, hypertension, arthritis and failing eyesight at the same time, the reality is different. The cost of illness in later life is rarely a single large hospital bill. It is the steady drip of consultations, tests, medicines and travel that recurs month after month, with the occasional admission on top. India is also ageing quickly: the population aged 60 yr and over reached about 149 million in 2022 and is projected to more than double by 2050^3^. Non-communicable disease already imposes heavy and sustained costs on Indian households^4^, catastrophic spending has persisted across two decades of national surveys^5^, and publicly financed insurance has often failed to deliver the financial protection it promises because its benefit package is narrow^6^.

Earlier Indian work has tended to describe spending or coverage gaps without putting them on a common economic footing. Few studies have measured catastrophic spending against a household's genuine capacity to pay among older adults specifically, traced who within the older population bears it, valued the unpaid family labour that substitutes for paid care, or asked which concrete reform would shift the burden. This study addressed six linked questions: how catastrophic is health spending for older Indians; how many are impoverished by it; whether the burden is distributed fairly across the income range and across States; what drives it; what unpaid family care is worth; and which financing reform would buy the most protection per rupee.

## Materials & Methods

*Study design and data:* This was a cross-sectional secondary analysis of LASI Wave 1, a nationally representative survey of adults aged 45 yr and older conducted in 2017–18^7^. The analysis centred on the 31,766 respondents aged 60 yr and over; the full sample aged 45 yr and over was used for sensitivity analysis. All estimates used the survey person weights.

*Spending and capacity to pay:* Household out-of-pocket spending was annualised as inpatient costs over the previous year plus outpatient costs (doctors' fees, diagnostics and medicines obtained during treatment) over the previous month, scaled to a year. Following the World Health Organization approach, capacity to pay was defined as non-food consumption, that is total consumption minus food expenditure^8,9^. Monetary values were deflated to constant 2017 rupees using the survey consumer price indices.

*Outcomes:* CHE was measured three ways — spending above 10 and above 25 per cent of total consumption, and above 40 per cent of capacity to pay (the WHO definition). Impoverishment compared per-capita consumption with a poverty line before and after subtracting per-capita out-of-pocket spending, the line being anchored to the survey poverty measure. Income-related inequality was summarised with the concentration index and the Erreygers correction, ranking households by per-capita consumption^10,11^, and decomposed into the contribution of each correlate.

*Drivers and valuation:* A two-part model estimated the probability of any out-of-pocket spending (logistic regression) and then its amount among spenders (gamma regression with a log link), the standard treatment for skewed cost data^12^. A gradient-boosting classifier predicted catastrophic spending and SHAP values ranked each predictor; this is a predictive, not causal, exercise^13^. Unpaid family care was valued by costing the hours of help that older adults reported receiving from spouses, children and other relatives at a representative care-worker wage (replacement-cost method), with sensitivity to the wage assumed.

*Policy analysis and projection:* Four financing scenarios were microsimulated and CHE, impoverishment and fiscal cost recomputed: full inpatient cover for those aged 70 yr and over (approximating the PM-JAY expansion); full outpatient and medicine cover for all aged 60 yr and over; a pension top-up of Rs 500 a month^14^; and the three combined. Scenarios were ranked by cost-effectiveness (CHE reduction per Rs lakh crore). National costs and the demographic projection to 2036 and 2050 used the older-population counts and benchmark unit costs from official sources^3,14,15^; the projection held the 2017–18 catastrophic-spending rate constant. Reporting followed the STROBE statement^16^. Analyses were run in Python and the full code is openly available so that every result can be reproduced.

## Results

*Sample and burden (Table I, Table II, Figure 1).* Among 31,766 older adults (50.8 per cent women, 69.3 per cent rural), out-of-pocket spending was nearly universal (77.3 per cent), with a median household amount of about Rs 7,200 a year. CHE exceeded 40 per cent of capacity to pay in 20.7 per cent of households, a quarter of consumption in 13.7 per cent and a tenth in 35.7 per cent. The burden rose with concurrent illness (26.7 per cent among those with two or more chronic conditions) and was higher in rural than urban areas (22.9 vs 15.9 per cent).

*Impoverishment (Table II, Figure 2).* Before accounting for medical bills, 19.6 per cent of older adults lived below the poverty line; afterwards, 25.4 per cent did. Out-of-pocket payments alone therefore impoverished a further 5.8 per cent. Rural elders were affected almost twice as often as urban ones (6.8 vs 3.4 percentage points).

*Inequality.* The concentration index for catastrophic spending was mildly positive (+0.090; Erreygers +0.075), and CHE rose monotonically across consumption quintiles (17.0 per cent in the poorest to 26.1 per cent in the richest). This counterintuitive pattern reflects the capacity-to-pay measure: wealthier households spend more on private care and so cross the relative threshold more often. The decomposition tempered this reading — multimorbidity pulled the burden towards the better-off, but rural residence pulled strongly in the pro-poor direction, contributing about a quarter of the index. The impoverishment results show that, in absolute terms, it is poorer and rural households that are pushed below the poverty line.

*Drivers (Table III, Figure 3).* Both models agreed. In the gradient-boosting model, rural residence was the single strongest predictor of catastrophic spending, ahead of multimorbidity and functional limitation. The two-part model concurred: multimorbidity raised the odds of any spending by about 70 per cent and functional limitation by about 60 per cent, and rural residence by a third.

*The unpaid-care economy.* About 12.2 per cent of older adults received regular help with daily activities, averaging 13.9 h a week, almost all from spouses and children. Valued at a care-worker wage, this unpaid care was worth roughly Rs 71,000 per recipient a year and about Rs 1.3 lakh crore nationally — more than four times the cost of insuring every older person's inpatient care. Across plausible wage assumptions the national value ranged from Rs 0.66 to 2.64 lakh crore.

*What reform would buy (Table IV, Figure 4).* Fully covering inpatient care for those aged 70 yr and over — the design of the current PM-JAY expansion — reduced catastrophic spending by only 2.0 percentage points, at about Rs 31,700 crore. Covering outpatient and medicine costs for all older adults reduced it by 17.8 percentage points, almost nine times as much, for about Rs 2.6 lakh crore. A pension top-up cut impoverishment sharply (by 16 percentage points) but moved catastrophic spending less. Combining all three almost eliminated catastrophic spending, but this combined figure assumes full reimbursement of every cost and should be read as a ceiling. Ranked by cost-effectiveness, outpatient and medicine cover was not only the highest-impact lever but also the most efficient (6.7 percentage points of CHE reduction per Rs lakh crore, against 6.2 for inpatient cover).

*Geography (Figure 5).* Catastrophic spending varied more than six-fold across States and union territories, from 28.5 per cent in Bihar, 27.6 per cent in Jammu & Kashmir, 27.4 per cent in West Bengal, 27.0 per cent in Uttar Pradesh and 25.9 per cent in Kerala, down to about 4 per cent in the smallest island territories.

*Projection (Table V, Figure 6).* Holding the 2017–18 catastrophic-spending rate constant, demographic ageing alone would raise the number of older adults living in catastrophic-spending households from about 31 million in 2022 to 47 million in 2036 and 72 million in 2050, and the annual cost of universal outpatient and medicine cover for older adults from about Rs 2.65 to 6.17 lakh crore over the same period.

## Discussion

The economics of growing old in India is not, for most families, the economics of hospitalisation. It is the economics of the chronic, the routine and the recurring. The central finding is the gap between two financing levers that look similar on paper but behave very differently: covering hospital bills for older people removed only about a ninth as much catastrophic spending as covering their outpatient and medicine costs would, and at far lower efficiency. A protection system built on admissions addresses the visible emergencies while leaving the slow, grinding cost of managing chronic disease with the household. This is consistent with the WHO view that healthy ageing depends on continuous, function-centred care rather than episodic hospital treatment^17^, and with the long-standing critique that narrowly hospital-focused public insurance under-protects Indian households^18^.

The burden also falls unevenly, and in two directions that must be read together. On the relative capacity-to-pay measure, catastrophic spending is slightly more common among better-off and urban households, who spend more on private care. In absolute terms, however, it is rural and poorer households that are tipped into poverty, and rural residence is the strongest single predictor the data identify. The State gradient sharpens the point: catastrophic spending is several times more common in Bihar, eastern and northern States than in the smallest territories, marking where outpatient financial protection is most urgently needed.

Two further results deserve emphasis. First, the unpaid care that families provide is an enormous, uncounted subsidy to the health system — on the order of Rs 1.3 lakh crore a year, larger than the entire cost of insuring older people's hospital stays. As families shrink and adult children migrate, that subsidy cannot be assumed to last. Second, pensions and health cover do different jobs: a pension top-up relieved impoverishment but barely touched catastrophic spending, while outpatient cover did the reverse. Income support and service cover are complements, not substitutes. Finally, the projection shows that doing nothing is itself a choice with a rising price: the catastrophic-spending caseload will more than double by 2050 on demographic momentum alone.

The policy implication is specific. The most valuable addition to India's financing of older people's health would be cover for outpatient consultations and, above all, medicines for chronic disease, delivered through primary care and the network of health and wellness centres. This would not replace PM-JAY; it would complete it.

*Limitations.* The data are cross-sectional, so we describe burden and association, not change over time or causation. Spending and care are self-reported. The household outpatient measure captures medicines bought during treatment but may under-record standalone pharmacy purchases for chronic disease, so the true outpatient burden, and the benefit of covering it, may be larger than estimated; the central comparison is therefore conservative. The machine-learning results describe prediction, not cause. The microsimulation is a static counterfactual assuming full uptake and reimbursement, which is why the combined scenario is an upper bound. The projection is a demographic what-if that holds rates constant rather than a forecast. The care-worker wage is an assumption, reported with sensitivity.

## Conclusions

For older Indians, catastrophic health spending begins outside the hospital and ends, too often, in poverty, borne most heavily by rural families. Hospital insurance is necessary but not sufficient. The clearest route to protecting older people financially is to cover the everyday costs of chronic care — outpatient visits and medicines — alongside the pensions that keep a small bill from becoming a crisis, and the case for acting strengthens every year that the older population grows.

## Acknowledgments

The author thanks the LASI investigators, the International Institute for Population Sciences and the survey respondents whose participation made this analysis possible.

*Financial support & sponsorship:* None.

*Conflicts of interest:* None declared.

## References

1. National Health Authority, Government of India. About Pradhan Mantri Jan Arogya Yojana (PM-JAY). New Delhi: NHA. Available from: https://nha.gov.in/PM-JAY (accessed on June 25, 2026).
2. Press Information Bureau, Government of India. Cabinet approves health coverage to all senior citizens aged 70 years and above under AB PM-JAY. New Delhi: PIB; September 11, 2024. Available from: https://www.pib.gov.in/PressReleasesPage.aspx?PRID=2053883 (accessed on June 25, 2026).
3. International Institute for Population Sciences, United Nations Population Fund. India Ageing Report 2023: caring for our elders. New Delhi: UNFPA; 2023.
4. Mahal A, Karan A, Engelgau M. The economic implications of non-communicable disease for India. Washington DC: World Bank; 2010.
5. Pandey A, Ploubidis GB, Clarke L, Dandona L. Trends in catastrophic health expenditure in India: 1993 to 2014. Bull World Health Organ 2018; 96: 18-28. doi:10.2471/BLT.17.191759.
6. Selvaraj S, Karan AK. Why publicly financed health insurance schemes are ineffective in providing financial risk protection. Econ Polit Wkly 2012; 47: 60-8.
7. International Institute for Population Sciences, National Programme for Health Care of Elderly, Harvard T.H. Chan School of Public Health, University of Southern California. Longitudinal Ageing Study in India (LASI) Wave 1, 2017-18: India report. Mumbai: IIPS; 2020.
8. Xu K, Evans DB, Kawabata K, Zeramdini R, Klavus J, Murray CJL. Household catastrophic health expenditure: a multicountry analysis. Lancet 2003; 362: 111-7. doi:10.1016/S0140-6736(03)13861-5.
9. Wagstaff A, van Doorslaer E. Catastrophe and impoverishment in paying for health care: with applications to Vietnam 1993-1998. Health Econ 2003; 12: 921-34. doi:10.1002/hec.776.
10. O'Donnell O, van Doorslaer E, Wagstaff A, Lindelow M. Analyzing health equity using household survey data. Washington DC: World Bank; 2008.
11. Erreygers G. Correcting the concentration index. J Health Econ 2009; 28: 504-15. doi:10.1016/j.jhealeco.2008.02.003.
12. Belotti F, Deb P, Manning WG, Norton EC. twopm: two-part models. Stata J 2015; 15: 3-20. doi:10.1177/1536867X1501500102.
13. Lundberg SM, Lee SI. A unified approach to interpreting model predictions. Adv Neural Inf Process Syst 2017; 30: 4765-74.
14. Ministry of Rural Development, Government of India. National Social Assistance Programme: Indira Gandhi National Old Age Pension Scheme. New Delhi: MoRD. Available from: https://nsap.nic.in (accessed on June 25, 2026).
15. National Sample Survey Office, Ministry of Statistics and Programme Implementation. Health in India: NSS 75th round (July 2017-June 2018), Report No. 586. New Delhi: MoSPI; 2019.
16. von Elm E, Altman DG, Egger M, Pocock SJ, Gøtzsche PC, Vandenbroucke JP. The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement: guidelines for reporting observational studies. Lancet 2007; 370: 1453-7. doi:10.1016/S0140-6736(07)61602-X.
17. World Health Organization. World report on ageing and health. Geneva: WHO; 2015.
18. Prinja S, Kaur M, Kumar R. Universal health insurance in India: ensuring equity, efficiency and quality. Indian J Community Med 2012; 37: 142-9. doi:10.4103/0970-0218.99907.

## Tables

### Table I. Characteristics of the study sample (adults aged 60 yr and older, LASI Wave 1)

| Characteristic | Value |
|:---|:---|
| Unweighted sample size, n | 31,766 |
| Women, % | 50.8 |
| Rural residence, % | 69.3 |
| Two or more chronic conditions, % | 23.2 |
| Any functional limitation, % | 70.8 |
| Living alone, % | 5.5 |
| Any pension, % | 13.6 |
| Reporting any out-of-pocket health spending, % | 77.3 |
| Median annual household out-of-pocket spending, Rs | 7,155 |
| Median annual household consumption, Rs | 140,155 |

*All percentages and monetary values are survey-weighted; monetary values in constant 2017 rupees.*

### Table II. Catastrophic health expenditure and impoverishment, overall and by subgroup

| Group | n | CHE >10% consumption, % | CHE >25% consumption, % | CHE >40% capacity, % | Out-of-pocket impoverishment, pp |
|:---|---:|---:|---:|---:|---:|
| All aged 60+ | 31,766 | 35.7 | 13.7 | 20.7 | 5.8 |
| Aged 70+ | 12,550 | 37.0 | 14.0 | 21.2 | – |
| Men 60+ | 15,294 | 36.2 | 14.0 | 21.0 | 5.8 |
| Women 60+ | 16,472 | 35.2 | 13.3 | 20.5 | 5.7 |
| Rural 60+ | 20,961 | 37.0 | 14.4 | 22.9 | 6.8 |
| Urban 60+ | 10,805 | 32.9 | 12.0 | 15.9 | 3.4 |
| Two or more chronic conditions | 7,576 | 46.5 | 20.0 | 26.7 | – |

*CHE, catastrophic health expenditure; capacity, capacity to pay (non-food consumption); pp, percentage-point rise in the share below the poverty line after out-of-pocket payment.*

### Table III. Predictors of catastrophic health spending and income-related inequality

| Predictor | Two-part model: odds of any spending, OR (95% CI) | Gradient-boosting SHAP rank |
|:---|:---|:---|
| Rural residence | 1.32 (1.24-1.41) | 1 (strongest) |
| Two or more chronic conditions | 1.72 (1.59-1.85) | 2 |
| Functional limitation | 1.59 (1.49-1.69) | 3 |
| Age (per year) | 1.00 (0.99-1.00) | 4 |
| Education (per year) | 1.04 (1.02-1.06) | 5 |
| Concentration index (CHE40, ranked by per-capita consumption) | +0.090 | — |
| Erreygers index | +0.075 | — |

*OR, odds ratio from the participation part of the two-part model; SHAP rank from the gradient-boosting classifier of catastrophic spending (predictive, not causal). The positive concentration index indicates catastrophic spending is marginally concentrated among better-off households on the relative measure; the decomposition (Supplementary) shows rural residence contributing in the pro-poor direction.*

### Table IV. Microsimulation of financing-reform scenarios and cost-effectiveness

| Scenario | CHE >40% capacity, % (Δ pp) | Out-of-pocket impoverishment, Δ pp | Fiscal cost, Rs crore | CHE40 reduction per Rs lakh crore, pp |
|:---|:---|---:|---:|---:|
| Inpatient cover, age 70+ (PM-JAY model) | 18.8 (-2.0) | -0.5 | 31,654 | 6.2 |
| Outpatient and medicine cover, all 60+ | 2.9 (-17.8) | -5.0 | 264,825 | 6.7 |
| Pension top-up (+Rs 500/month), all 60+ | 16.6 (-4.2) | -16.3 | 89,400 | 4.7 |
| Combined (ceiling) | 0.0 (-20.7) | -18.9 | 435,527 | 4.8 |

*All scenarios are applied to the adults-aged-60+ sample and compared with the common baseline (CHE40 20.7%, impoverishment 25.4% below the poverty line). Δ pp, percentage-point change; negative denotes improvement. All scenarios assume full coverage and full reimbursement and are upper-bound ceilings, particularly the combined scenario. Fiscal costs in Rs crore (1 crore = 10 million), scaled to the national older-population count.*

### Table V. Projected catastrophic-spending burden and cost of action, 2022-2050

| Year | Population aged 60+, million | Older adults in catastrophic-spending households, million | Annual cost of outpatient and medicine cover, Rs lakh crore |
|---:|---:|---:|---:|
| 2022 | 149 | 30.9 | 2.65 |
| 2036 | 227 | 47.1 | 4.03 |
| 2050 | 347 | 72.0 | 6.17 |

*Population projections from the India Ageing Report 2023. The catastrophic-spending rate and the per-person cost of cover are held at the 2017-18 level; figures are a demographic what-if, not a forecast, and are in constant 2017 rupees.*

## Legends to Figures

Figure 1. Catastrophic health expenditure among older adults at three thresholds, for all adults aged 60 yr and over and for those aged 70 yr and over. Bars are survey-weighted percentages of households.

Figure 2. Share of older adults below the poverty line before and after out-of-pocket payment, overall and by sex and residence. The gap between the bars is the impoverishment effect.

Figure 3. Drivers of catastrophic spending ranked by mean absolute SHAP value from the gradient-boosting model. Higher values indicate a stronger contribution to the prediction; the ranking is predictive, not causal.

Figure 4. Percentage-point change in catastrophic spending under four financing-reform scenarios, with each scenario's fiscal cost annotated. Scenarios assume full coverage and represent upper-bound ceilings.

Figure 5. Ranking of States and union territories by the share of older households with catastrophic spending (>40% of capacity to pay). The dashed line marks the national 60+ average (20.7%).

Figure 6. Projected number of older adults in catastrophic-spending households and the annual cost of universal outpatient and medicine cover, 2022 to 2050, holding the 2017-18 catastrophic-spending rate constant.
