# External benchmarking parameters — provenance notes

This note documents the source, exact figure, and any caveats for each row in
`data/external/health_economics_params.csv`. These parameters calibrate the
microsimulation and benchmark LASI-derived results against authoritative
external policy/economic facts. Every figure below is sourced from a named
organisation/document with a working URL; none are invented. Where an exact
official figure could not be retrieved, the best-sourced authoritative
estimate is recorded and flagged explicitly.

## pop_60plus_india — 149,000,000 persons (2022)
The India Ageing Report 2023, jointly produced by UNFPA India and the
International Institute for Population Sciences (IIPS), states that India had
149 million persons aged 60 and above in 2022, comprising 10.5% of the total
population (up from 10.1% in 2021). This is the standard reference figure
used across Indian government and UN communications on population ageing.
Source: UNFPA India & IIPS, *India Ageing Report 2023 — "Caring for Our
Elders: Institutional Responses"* (released Sep 2023).
URL: https://india.unfpa.org/sites/default/files/pub-pdf/20230926_india_ageing_report_2023_web_version_.pdf

## pop_70plus_india — 60,000,000 persons (2024) — LOW-CONFIDENCE / best estimate
No single demographic publication (Census, NSO, or the India Ageing Report
2023) publishes a clean, separately tabulated "70 years and above" national
headcount for 2021–2024; the standard public releases use 60+ and 80+ as the
reported cut points. The Government of India's own working estimate, used to
size the September 2024 AB PM-JAY 70+ expansion, is "approximately 6 crore
(60 million) senior citizens aged 70 and above" — stated by the Cabinet,
PMO, and Ministry of Health & Family Welfare in the official rollout
communications. This is recorded here as the best-available authoritative
estimate because it is the figure the Government of India itself uses for
policy planning at this age cut-off; it should be treated as an
order-of-magnitude planning estimate rather than a precise census count, and
revisited if/when Census 2021 (still pending as of 2026) or a future India
Ageing Report publishes an explicit 70+ breakdown.
Source: Press Information Bureau / PMO, Cabinet decision on AB PM-JAY
coverage for senior citizens 70+, 11 Sep 2024.
URL: https://www.pib.gov.in/PressReleasesPage.aspx?PRID=2053883

## pmjay_70plus_families — 45,000,000 families (2024)
The Union Cabinet's AB PM-JAY 70+ expansion (approved 11 September 2024,
launched 29 October 2024) was sized to cover approximately 4.5 crore (45
million) families, encompassing approximately 6 crore (60 million) senior
citizens aged 70 and above, irrespective of income. Existing PM-JAY families
get an additional top-up cover for their 70+ members; all other 70+ seniors
get a new family-floater cover. Recorded unit is **families**; the
person-level figure (60 million) is captured separately as
`pop_70plus_india` above since the brief asks for an explicit statement of
which unit is used.
Source: Press Information Bureau, Cabinet approval of AB PM-JAY senior
citizen coverage, 11 Sep 2024.
URL: https://www.pib.gov.in/PressReleasesPage.aspx?PRID=2053883

## pmjay_family_cover — Rs 500,000 (Rs 5 lakh) per family per year
AB PM-JAY provides a health cover of up to Rs 5,00,000 per family per year on
a family-floater basis (no restriction on family size, age, or gender; all
pre-existing conditions covered from day one). For 70+ beneficiaries already
in a PM-JAY family, this Rs 5 lakh is an *additional* top-up specific to
members aged 70+, not shared with younger family members.
Source: National Health Authority, Government of India — official PM-JAY
scheme description.
URL: https://nha.gov.in/PM-JAY

## ignoaps_pension_60_79 — Rs 200 per month (central rate)
Under the National Social Assistance Programme (NSAP), the Indira Gandhi
National Old Age Pension Scheme (IGNOAPS) central government contribution is
Rs 200 per month per BPL beneficiary aged 60–79. **Caveat: this is the
central contribution only.** State governments commonly top this up — total
disbursed pensions to beneficiaries range roughly Rs 200–1,000/month
depending on the state's own contribution, so this figure understates the
total pension actually received in most states.
Source: Ministry of Rural Development, National Social Assistance Programme
— official scheme FAQ/guidelines.
URL: https://nsap.nic.in/circular.do?method=faq

## ignoaps_pension_80plus — Rs 500 per month (central rate)
The IGNOAPS central contribution rises to Rs 500 per month per BPL
beneficiary aged 80 and above. Same caveat as above applies: this is the
central component only, and states may add their own top-up on top of this
amount.
Source: Ministry of Rural Development, National Social Assistance Programme
— official scheme FAQ/guidelines.
URL: https://nsap.nic.in/circular.do?method=faq

## care_worker_wage_hour — Rs 97.9 per hour (2024) — EXPLICIT ASSUMPTION
**This parameter is an assumption, not a directly published wage rate.**
There is no single official "home care worker" or "domestic worker" wage
notification at the national level; home/elder-care work in India is largely
informal and unregulated. The value here is derived as a proxy from the
Central Government's unskilled-worker minimum wage under the Variable
Dearness Allowance (VDA) revision effective 1 October 2024: Rs 783 per day.
Converting to an hourly rate using the standard 8-hour working day
(consistent with the Factories Act, 1948 / OSH Code, 2020 convention) gives
Rs 783 / 8 = **Rs 97.9 per hour**. This is the basis that should be varied in
sensitivity analysis — e.g. testing semi-skilled (Rs 868/day → Rs 108.5/hr)
or state-specific minimum wage notifications, which can differ substantially
from the central floor (some states set unskilled minimum wages well above
or below the central rate).
Source (daily rate): Press Information Bureau / Chief Labour Commissioner,
Central Government minimum wage revision effective 1 Oct 2024 (as
summarised by ClearTax); hourly conversion is this project's own calculation
(783/8).
URL: https://cleartax.in/s/minimum-wages-in-india

## nsso75_oop_hosp_avg — Rs 16,676 (rural), 2017–18
NSSO 75th Round, "Health in India" (Report No. 586), Ministry of Statistics
and Programme Implementation (MOSPI): average medical expenditure per
hospitalisation case (excluding childbirth) was approximately Rs 16,676 in
**rural** India and Rs 26,475 in **urban** India. The CSV records the rural
figure under this key; the urban figure (Rs 26,475) is documented here for
completeness but not given a separate CSV row, since the brief asks for one
row per parameter and instructs stating which sector is recorded. A combined
(rural+urban pooled) national average was not located in the publicly
available MOSPI summary release; if a precise pooled figure is needed later,
it should be computed from the NSSO 75th round unit-level microdata
(accessible via MoSPI's microdata portal) using sector population weights.
Source: NSSO 75th Round, "Health in India" (Report No. 586), MOSPI,
Government of India, 2017–18 survey (July 2017 – June 2018).
URL: https://mospi.gov.in/sites/default/files/announcements/Summary%20Analysis_Report_586_Health.pdf

## nsso75_oop_outpatient_avg — Rs 568 (rural), 2017–18 — LOW-CONFIDENCE
**Flagged as a best-sourced estimate, not a directly confirmed official
headline figure.** The same NSSO 75th Round survey collected average medical
expenditure per spell of ailment for non-hospitalised (outpatient) treatment
over a 15-day reference period, but the official MOSPI summary PDF
(Report No. 586) could not be machine-parsed to extract the all-India
headline number directly during this research (the source PDF is a
scanned/compressed image format). The value recorded (Rs 568 rural / Rs 767
urban) comes from a state-level secondary tabulation of the same national
survey round that explicitly cites NSS 75th round methodology. This is
broadly consistent with two independent cross-checks from the same survey
round: (a) Rs 552 per episode reported for households using informal
healthcare providers (Institute of Development Studies Kolkata working
paper), and (b) Rs 785 per episode reported for the 60+ elderly subgroup
specifically (Scientific Reports 2024 CHE/elderly study). Given the
convergence of these independent analyses of the same dataset around the
Rs 550–800 range, Rs 568–767 (rural/urban) is used as the working estimate,
but this row should be re-verified against the official NSSO unit-level
microdata or a full-text rendering of Report No. 586 before being treated as
a precise government-published statistic.
Source: state-level secondary tabulation of NSSO 75th Round, "Health in
India" 2017–18 data (cross-validated against IDSK working paper and
Scientific Reports 2024 elderly CHE study; see note above).
URL: https://www.granthaalayahpublication.org/journals/granthaalayah/article/view/4401

## who_che_method_ref — Xu et al. 2003 (Lancet); Wagstaff & van Doorslaer 2003 (Health Economics)
Two complementary citations underpin the WHO/Wagstaff catastrophic-health-
expenditure (CHE) capacity-to-pay methodology already implemented in this
project's `che_indicators()` function (40% of capacity-to-pay threshold,
`src/health_economics.py`):
- Xu K, Evans DB, Kawabata K, Zeramdini R, Klavus J, Murray CJL.
  "Household catastrophic health expenditure: a multicountry analysis."
  *Lancet.* 2003;362(9378):111–117. DOI: 10.1016/S0140-6736(03)13861-5.
  This is the WHO-affiliated paper that established the cross-country CHE
  measurement framework widely cited in global health-financing analyses.
- Wagstaff A, van Doorslaer E. "Catastrophe and impoverishment in paying for
  health care: with applications to Vietnam 1993–1998." *Health Economics.*
  2003;12(11):921–933. DOI: 10.1002/hec.776.
  This paper defines the capacity-to-pay approach (out-of-pocket payments
  relative to household consumption net of subsistence/food spending) and
  the associated catastrophic/impoverishment indices used as the
  methodological basis for the 40% capacity-to-pay threshold.
URL (primary DOI on record): https://doi.org/10.1016/S0140-6736(03)13861-5

## Summary of low-confidence / flagged figures
- **pop_70plus_india** (60,000,000): government policy-planning estimate,
  not a Census/demographic-survey headcount; treat as order-of-magnitude.
- **nsso75_oop_outpatient_avg** (Rs 568 rural / Rs 767 urban): best-sourced
  cross-validated estimate; the official MOSPI Report No. 586 PDF could not
  be parsed to confirm the precise all-India headline number directly.
- **care_worker_wage_hour** (Rs 97.9/hour): explicit assumption derived from
  the central unskilled minimum daily wage and an 8-hour-day convention, not
  a directly published care-worker wage; intended to be varied in
  sensitivity analysis.
