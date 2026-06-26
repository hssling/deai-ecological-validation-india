# Where the money goes: catastrophic spending, impoverishment, and the hidden cost of family care among older adults in India

## Abstract

**Background:** India has built its financial protection for older people around hospital insurance, yet most of what ageing households spend on health never reaches a hospital ward. We asked how heavy out-of-pocket spending is for older Indians, who carries it, what drives it, and which financing reforms would relieve it most.

**Methods:** We analysed 31,766 adults aged 60 and older in the Longitudinal Ageing Study in India Wave 1. Out-of-pocket spending and household consumption were taken at the household level and expressed in constant 2017 rupees. We measured catastrophic health expenditure at three thresholds, impoverishment before and after payment, income-related inequality (concentration and Erreygers indices with decomposition), drivers (a two-part cost model and a gradient-boosting model with SHAP values), and the replacement-cost value of unpaid family care. A microsimulation tested four financing scenarios.

**Results:** One in five households (20.7%) spent more than 40% of their capacity to pay on health; 35.7% exceeded a tenth of total consumption. Out-of-pocket payments pushed an additional 5.8% of older people below the poverty line, with rural areas worst affected. Rural residence, multimorbidity and functional limitation were the strongest predictors. Unpaid family care was worth about Rs 1.3 lakh crore a year. Covering inpatient care alone removed 1.8 percentage points of catastrophic spending; covering outpatient and medicine costs removed 16.1.

**Conclusions:** Catastrophic spending in later life originates outside the hospital. Outpatient and medicine cover, not inpatient insurance alone, is the missing pillar of elder-care financing.

**Key words:** Aged; Health Expenditures; Catastrophic Illness; Caregivers; Health Policy; India.

## Introduction

The way a country pays for the health of its older citizens reveals what it believes ageing costs. India has largely answered that question with hospital insurance. The Pradhan Mantri Jan Arogya Yojana (PM-JAY) offers cover of up to Rs 5 lakh per family for inpatient care, and a 2024 expansion extended eligibility to every resident aged 70 and above.[1,2] This is a substantial commitment. It also rests on an assumption worth testing: that the financial danger of growing old lies mainly in hospitalisation.

For an older person managing diabetes, hypertension, arthritis and failing eyesight at the same time, the reality is different. The cost of illness in later life is rarely a single large hospital bill. It is the steady drip of consultations, blood tests, refills and travel that recurs month after month, with the occasional admission on top. Hospital insurance, by design, does little for this routine expenditure. If most of an older household's medical spending happens outside the hospital, then a financing system organised around admissions can leave the largest part of the burden untouched.

India is also ageing quickly. The population aged 60 and over reached roughly 149 million in 2022 and is projected to keep climbing.[3] Most older adults have no health insurance, and only a minority receive any pension. When predictable income is thin, even modest medical costs can force a household to borrow, sell assets or simply go without care.

Earlier work on ageing and money in India has tended to describe spending and coverage gaps without putting them on a common economic footing. Few studies have measured catastrophic spending against a household's genuine capacity to pay, traced who within the older population bears it, or asked what specific reforms would shift it. We set out to do this and to answer six linked questions. How catastrophic is health spending for older Indians? How many are pushed into poverty by it? Is the burden distributed fairly across the income range? What drives it? What is the unpaid care that families provide actually worth? And which financing reform would buy the most protection per rupee?

## Materials and Methods

### Data and population

We used the Longitudinal Ageing Study in India (LASI) Wave 1, a nationally representative survey of adults aged 45 and older conducted in 2017–18, accessed through the harmonised Gateway to Global Aging file.[4] The analysis centres on the 31,766 respondents aged 60 and over; results for the full sample aged 45 and over are reported as a sensitivity check. All estimates use the survey's person-level weights.

### Spending and capacity to pay

Out-of-pocket spending was measured at the household level and annualised: inpatient costs over the previous year plus outpatient costs (including doctors' fees, diagnostics and medicines bought in the course of treatment) over the previous month, scaled to a year. Following the World Health Organization's approach, a household's capacity to pay was defined as its non-food consumption, that is, total consumption minus food spending.[5,6] All monetary values were deflated to constant 2017 rupees using the survey's consumer price indices.

### Outcomes

We measured catastrophic health expenditure three ways: spending above 10% and above 25% of total consumption (the budget-share definition), and above 40% of capacity to pay (the WHO definition). For each we report the share of households affected and the average amount by which spending overshot the threshold. Impoverishment was assessed by comparing per-capita consumption with a poverty line, before and after subtracting per-capita out-of-pocket spending; the line was anchored to the survey's own poverty measure. Income-related inequality was summarised with the concentration index and the Erreygers correction for a binary outcome, ranking households by per-capita consumption, and decomposed into the contribution of each correlate.[7,8]

### Drivers and valuation

We modelled spending two ways. A two-part model first estimated the probability of any out-of-pocket spending (logistic regression) and then its amount among spenders (a gamma regression with a log link), the standard treatment for skewed health costs.[9] Alongside it, a gradient-boosting classifier predicted catastrophic spending, and SHAP values ranked the contribution of each predictor; this is a predictive exercise, not a causal one.[10] The economic value of unpaid family care was estimated by costing the hours of help that older adults reported receiving from spouses, children and other relatives at a representative care-worker wage (the replacement-cost method).

### Microsimulation

We simulated four financing scenarios and recomputed catastrophic spending, impoverishment and the fiscal cost of each: full inpatient cover for those aged 70 and over (approximating the PM-JAY expansion); full cover of outpatient and medicine costs for all those aged 60 and over; a pension top-up of Rs 500 a month; and the three combined. National costs were scaled using the older-population count and benchmark parameters drawn from official sources.[1,3,11]

### Reporting

The study followed the STROBE guidance for observational research.[12] Analyses were run in Python; the full code is openly available so that every figure can be reproduced.

## Results

### A burden that is common, and largely outpatient

Among older households, out-of-pocket health spending was nearly universal: 77% reported some, with a median annual amount of about Rs 7,200 and a long upper tail. Set against capacity to pay, this spending was frequently catastrophic. One in five households (20.7%) spent more than 40% of their non-food budget on health; 13.7% crossed a quarter of total consumption, and 35.7% crossed a tenth (Table 2, Figure 1). The picture worsened with concurrent illness: among older adults with two or more chronic conditions, 26.7% faced catastrophic spending by the capacity-to-pay measure.

The burden was not evenly spread. Rural households were considerably more exposed than urban ones (22.9% versus 15.9%), and the gap widened at the strictest threshold. Differences between men and women were small.

### Spending that pushes families into poverty

Before accounting for medical bills, 19.6% of older adults lived below the poverty line. After subtracting what they paid out of pocket, that figure rose to 25.4%. In other words, health payments alone pushed a further 5.8% of older people into poverty (Table 3, Figure 3). Here too the rural disadvantage was stark: out-of-pocket spending impoverished 6.8% of rural elders against 3.4% of urban ones, nearly a twofold difference.

### Who carries the burden

The concentration index for catastrophic spending was mildly positive (+0.090), meaning that, taken as a whole, such spending was slightly more common among better-off households (Figure 2). This headline conceals a more uncomfortable pattern. Decomposing the index showed that multimorbidity, education and pension receipt, all correlated with higher consumption, pulled the burden towards the better-off, while rural residence pulled strongly in the opposite direction, contributing about a quarter of the index in the pro-poor direction. The mild overall figure is therefore a balance of two forces: wealthier households spend more by choice and access, while poorer rural households spend heavily relative to what they can afford.

### What drives catastrophic spending

Both modelling approaches told a consistent story (Table 5, Figure 4). In the gradient-boosting model, rural residence was the single strongest predictor of catastrophic spending, ahead of multimorbidity and functional limitation; age, education, sex and pension status mattered far less. The two-part model agreed: multimorbidity raised the odds of any spending by about 70% and functional limitation by about 60%, and rural residence by a third. Among households that did spend, multimorbidity, education and pension receipt were each associated with larger amounts, consistent with greater use of care where means and need allow.

### The value of unpaid care

Out-of-pocket spending captures only the cash cost of ageing. Behind it lies a second, invisible economy of family labour. About 12% of older adults received regular help with daily activities, averaging 14 hours a week, almost all of it from spouses and children. Valued at a care-worker wage, this unpaid care was worth roughly Rs 71,000 per recipient each year and about Rs 1.3 lakh crore nationally (Figure 6), several times the cost of covering every older person's inpatient care. None of it appears in any health account.

### What reform would buy

The microsimulation made the central point of the study concrete (Table 6, Figure 5). Fully covering inpatient care for those aged 70 and over, the design of the current PM-JAY expansion, reduced catastrophic spending by only 1.8 percentage points, at a cost of about Rs 31,700 crore. Covering outpatient and medicine costs for all older adults reduced it by 16.1 percentage points, almost nine times as much, for about Rs 2.6 lakh crore. A Rs 500 monthly pension top-up cut impoverishment sharply but moved catastrophic spending little. Combining all three effectively eliminated catastrophic spending, but this combined figure is a ceiling rather than a realistic package: it assumes that every covered cost is fully reimbursed, which no scheme achieves. The comparison that matters is between the first two scenarios, and it points clearly away from an inpatient-only design.

## Discussion

The economics of growing old in India is not, for most families, the economics of hospitalisation. It is the economics of the chronic, the routine and the recurring. Our central finding is the gap between two policy levers that look similar on paper but behave very differently in practice: covering hospital bills for older people removed less than a tenth of the catastrophic spending that covering their outpatient and medicine costs would remove. A financial-protection system built on admissions addresses the visible emergencies while leaving the slow, grinding cost of managing chronic disease where it has always sat, with the household.

This matters because the cost it leaves behind falls hardest on those least able to bear it. Rural older adults were the most likely to spend catastrophically, the most likely to be impoverished by it, and the strongest single group the predictive model identified. The mildly pro-rich concentration index should not be read as reassurance; its decomposition shows that rural households carry a burden that is heavy relative to their means, masked in the aggregate by the larger discretionary spending of wealthier urban ones.

Two further results deserve emphasis. First, the unpaid care that families provide is an enormous, uncounted subsidy to the health system, on the order of Rs 1.3 lakh crore a year. As families shrink and adult children migrate, that subsidy cannot be assumed to last, and its erosion would convert today's invisible labour into tomorrow's cash demand. Second, pensions and health cover do different jobs: a pension top-up relieved impoverishment but barely touched catastrophic spending, while outpatient cover did the reverse. Income support and service cover are complements, not substitutes, and an elder-care strategy needs both.

The policy implication is specific. The most valuable addition to India's financing of older people's health would be cover for outpatient consultations and, above all, medicines for chronic disease, delivered through primary care and aligned with the existing network of health and wellness centres. This would not replace PM-JAY; it would complete it.

### Limitations

Several cautions apply. The data are cross-sectional, so we describe burden and association, not change over time or causation. Spending and care are self-reported and subject to recall. Our household outpatient measure captures medicines bought in the course of treatment but may under-record standalone pharmacy purchases for chronic conditions, so the true outpatient burden, and the benefit of covering it, may be larger than we estimate; this makes our central comparison conservative rather than overstated. The machine-learning results describe prediction, not cause. The microsimulation is a static counterfactual that assumes full uptake and full reimbursement, which is why the combined scenario should be read as an upper bound. Finally, the care-worker wage used to value unpaid care is an assumption, and we report it as such.

## Conclusion

For older Indians, catastrophic health spending begins outside the hospital and ends, too often, in poverty, and it is borne most heavily by rural families already stretched thin. Hospital insurance is necessary but not sufficient. The clearest route to protecting older people financially is to cover the everyday costs of chronic care, outpatient visits and medicines, alongside the pensions that keep a small bill from becoming a crisis. The hidden economy of family care, worth more than the entire cost of insuring older people's hospital stays, is a reminder of how much of this burden is currently met by people the system never counts.

## References

1. National Health Authority, Government of India. About Pradhan Mantri Jan Arogya Yojana (PM-JAY). Available from: https://nha.gov.in/PM-JAY
2. Press Information Bureau, Government of India. Cabinet approves health coverage to all senior citizens aged 70 years and above under AB PM-JAY. 11 September 2024. Available from: https://www.pib.gov.in/PressReleasesPage.aspx?PRID=2053883
3. United Nations Population Fund and International Institute for Population Sciences. India Ageing Report 2023: Caring for Our Elders. New Delhi: UNFPA; 2023.
4. International Institute for Population Sciences, National Programme for Health Care of Elderly, Harvard T.H. Chan School of Public Health, University of Southern California. Longitudinal Ageing Study in India (LASI) Wave 1, 2017–18, India Report. Mumbai: IIPS; 2020.
5. Xu K, Evans DB, Kawabata K, Zeramdini R, Klavus J, Murray CJL. Household catastrophic health expenditure: a multicountry analysis. Lancet. 2003;362:111–117.
6. Wagstaff A, van Doorslaer E. Catastrophe and impoverishment in paying for health care: with applications to Vietnam 1993–1998. Health Econ. 2003;12:921–933.
7. O'Donnell O, van Doorslaer E, Wagstaff A, Lindelow M. Analyzing Health Equity Using Household Survey Data. Washington DC: World Bank; 2008.
8. Erreygers G. Correcting the concentration index. J Health Econ. 2009;28:504–515.
9. Belotti F, Deb P, Manning WG, Norton EC. twopm: Two-part models. Stata J. 2015;15:3–20.
10. Lundberg SM, Lee SI. A unified approach to interpreting model predictions. Adv Neural Inf Process Syst. 2017;30:4765–4774.
11. Ministry of Rural Development, Government of India. National Social Assistance Programme: Indira Gandhi National Old Age Pension Scheme. Available from: https://nsap.nic.in
12. von Elm E, Altman DG, Egger M, Pocock SJ, Gøtzsche PC, Vandenbroucke JP. The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement. Lancet. 2007;370:1453–1457.
13. National Sample Survey Office, Ministry of Statistics and Programme Implementation. Health in India: NSS 75th Round (July 2017–June 2018), Report No. 586. New Delhi: MoSPI; 2019.
14. Pandey A, Ploubidis GB, Clarke L, Dandona L. Trends in catastrophic health expenditure in India: 1993 to 2014. Bull World Health Organ. 2018;96:18–28.
15. Mahal A, Karan A, Engelgau M. The Economic Implications of Non-Communicable Disease for India. Washington DC: World Bank; 2010.
16. World Health Organization. World Report on Ageing and Health. Geneva: WHO; 2015.
17. Prinja S, Kaur M, Kumar R. Universal health insurance in India: ensuring equity, efficiency, and quality. Indian J Community Med. 2012;37:142–149.
18. Selvaraj S, Karan AK. Why publicly financed health insurance schemes are ineffective in providing financial risk protection. Econ Polit Wkly. 2012;47:60–68.
