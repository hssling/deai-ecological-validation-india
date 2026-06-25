# Design Spec — MJDRDYPU flagship: Health Economics of Elderly Care in India

**Date:** 2026-06-25
**Target journal:** MJDRDYPU (Medical Journal of Dr. D.Y. Patil University) — full-length original article
**Data:** Longitudinal Ageing Study in India (LASI) Wave 1, harmonized G2Aging file `H_LASI_a3.sav` (local), survey-weighted
**Prior internal draft:** an NMJI-targeted descriptive household health-economic strain paper exists locally but is **not submitted and not planned for submission** (confirmed by author). This paper therefore **supersedes and absorbs** that groundwork rather than working around it — no companion-citation or non-overlap constraint applies.

---

## 1. Purpose and contribution

A single full-length, original health-economics paper on elderly care in India that answers six pressing policy questions and converts them into reproducible, decision-relevant evidence. The contribution is the combination — formal catastrophic-spending and impoverishment measurement, equity decomposition, econometric **and** machine-learning drivers, a monetised informal-care economy, and a policy microsimulation — in one coherent analysis of a nationally representative older population.

### Relationship to the unsubmitted NMJI draft
The prior NMJI draft is purely descriptive: out-of-pocket (OOP), insurance and pension *gaps*, with **no** capacity-to-pay denominator, **no** catastrophic-expenditure (CHE) thresholds, **no** equity decomposition, and **no** causal or policy modelling. Because it is not submitted and not planned for submission, this paper **absorbs and supersedes** it:
- Reuse its validated data-linkage and weighting groundwork freely as a foundation.
- Go well beyond it: CHE/impoverishment, equity decomposition, econometric + ML drivers, monetised care economy, policy microsimulation.
- No companion citation or non-overlap constraint. The only originality requirement is external (Section 7).

---

## 2. Population and unit

- **Headline population:** adults **60+** (the "elderly care" frame).
- **Sensitivity population:** adults **45+** (n≈66,470; comparability and power).
- **Subgroups:** 70+, sex, rural/urban, living arrangement, multimorbidity, pension status.
- Survey-weighted throughout (`r1wtresp`, design-aware where feasible).

---

## 3. Constructs (all variables confirmed present in `H_LASI_a3.sav`)

| Construct | Source variables | Notes |
|---|---|---|
| OOP health spend | `r1oophos1y` (hospital), `r1oopdoc1y` (outpatient), `r1oopsupl1y` (medication/supplements); household `hh1cohc1m`, `hh1cihc1y` cross-checks | Annualise consistently; net of reimbursement where available; reconcile individual vs household OOP and document the choice. |
| Capacity to pay | `hh1ctot` (total consumption), `hh1cnf1m`/`hh1cnf1y` (non-food), `hh1cperc` (per-capita) | Enables WHO capacity-to-pay (non-subsistence) and budget-share CHE definitions. |
| Poverty | `hh1poverty` (international line) + consumption-based line | Pre- vs post-OOP headcount and gap. |
| Informal care | ADL/IADL help receipt + helper identity/hours (locate exact vars at build) | Monetise: replacement cost (care-worker wage) and opportunity cost (foregone earnings). |
| Income decomposition | `hh1ipubpen`, `hh1ipena`, `hh1iearn`, etc. | Pension adequacy vs OOP context. |
| Deflation | `c2017cpindex`…`c2021cpindex` | Constant-price reporting. |

---

## 4. Six policy questions → analyses

1. **CHE incidence & intensity** — thresholds: OOP > 10% and > 25% of total consumption (budget share); OOP > 40% of capacity-to-pay (WHO, non-subsistence). Report headcount + overshoot/mean positive gap, by age/sex/residence.
2. **Impoverishment** — pre/post-OOP poverty headcount and normalised poverty gap; Pen's-parade visualisation.
3. **Equity** — concentration index and Erreygers index of CHE ranked by per-capita consumption; Wagstaff-style decomposition of contributors.
4. **Monetised informal-care economy** — national and per-recipient value of unpaid ADL/IADL care (replacement + opportunity cost), with sensitivity to wage assumptions.
5. **Drivers** — (a) two-part model: logit participation × GLM gamma-log positive OOP; report marginal effects. (b) Gradient-boosting classifier for catastrophic spending + SHAP importance/dependence; report discrimination with explicit survey-aware/causal caveats (prediction, not causation).
6. **Policy microsimulation** — counterfactual OOP under: (i) PM-JAY 70+ universal inpatient cover, (ii) outpatient-drug cover, (iii) pension top-up. Recompute CHE/impoverishment; estimate financial-protection gains, fiscal cost, and cost of inaction. Deterministic core + one-way sensitivity.

---

## 5. External data (selective; benchmarking/costing only, not micro-merged)

NSSO 75th-round health (OOP benchmark) · PM-JAY / NHA coverage & 70+ expansion · India Ageing Report 2023 · NSAP pension rates (top-up costing) · WHO CHE methodology references. Pulled via web/literature, sourced and cited; used to calibrate microsimulation parameters and sanity-check magnitudes.

---

## 6. Deliverables — full MJDRDYPU asset package (mirrors the AntiAgeing R1 structure)

- Blinded manuscript: structured abstract (**< 250 words**), Introduction, Methods, Results, Discussion, Policy implications, Limitations, Conclusion.
- **6 tables:** (1) sample characteristics; (2) CHE incidence/intensity by threshold & group; (3) impoverishment pre/post; (4) concentration + decomposition; (5) two-part + ML drivers; (6) microsimulation scenarios.
- **6 figures (600 dpi):** (1) CHE by threshold & age; (2) concentration curve; (3) impoverishment/Pen's parade; (4) SHAP importance; (5) microsimulation impact; (6) caregiving-cost waterfall.
- Supplementary: methods detail, sensitivity analyses, STROBE, variable mapping.
- Title page; declarations & data availability; cover letter; figure legends; STROBE checklist; internal double-reviewer critique + response.
- **Reproducible analysis script** added to the existing pipeline (`scripts/run_health_economics_mjdrdypu.py`) generating all tables/figures from `H_LASI_a3.sav`.

---

## 7. Writing-quality requirements (hard constraints)

These are acceptance criteria, not aspirations:
- **Novelty / low similarity:** all prose original; zero copied sentences from NMJI or any source; paraphrase and cite; no boilerplate template language.
- **Low AI-detection signature:** vary sentence length and structure; avoid formulaic scaffolding ("Moreover/Furthermore/In conclusion" chains, tricolon padding, hollow hedging); prefer concrete numbers and specific clinical/policy detail over generic statements.
- **High language/grammar quality:** careful proofreading; consistent tense; correct statistical phrasing.
- **Easy readability:** plain, direct sentences; define terms on first use; keep the main narrative accessible to a clinician/policy reader, with technical depth pushed to Methods/Supplement.

---

## 8. Methods integrity & limitations to state plainly

- Cross-sectional Wave 1 only (Wave 2 harmonized expenditure not available locally — verified: `H_LASI_a3.sav` contains only `w1` variables). No causal claims; microsimulation is a static counterfactual, not a dynamic forecast.
- Self-reported expenditure and recall; household OOP linked to individuals represents a household economic environment.
- ML results are predictive/explanatory, not causal; SHAP describes the model, not the world.
- Microsimulation assumes stated coverage/uptake parameters; report sources and run sensitivity.

---

## 9. Out of scope (YAGNI)

- No longitudinal/panel analysis (data unavailable).
- No district-level small-area estimation.
- No primary cost-effectiveness (ICER) model beyond the financial-protection microsimulation.
