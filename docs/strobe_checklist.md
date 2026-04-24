# STROBE / TRIPOD Combined Reporting Checklist

**Study:** Digital Exposome Aging Index (DEAI): Multi-domain Prediction of Accelerated Biological Ageing
**Design:** Cross-sectional prediction study
**Checklists applied:** STROBE (observational epidemiology) + TRIPOD (prediction model development)
**Version:** 1.0 | Date: 2026-04-22

---

## STROBE Checklist

| Item | STROBE Requirement | Manuscript Location | Status |
|------|--------------------|--------------------:|--------|
| 1a | Study design in title or abstract | Title + Abstract | ✅ |
| 1b | Abstract informative summary | Abstract | ✅ |
| 2 | Scientific background and rationale | Introduction §1 | ✅ |
| 3 | Study objectives | Introduction §1 (4 aims) | ✅ |
| 4 | Study design | Methods §2.1 | ✅ |
| 5 | Setting, locations, dates | Methods §2.1 | ⚠ Pending real cohort dates |
| 6a | Eligibility criteria | Methods §2.1 | ⚠ Pending LASI microdata |
| 6b | Sources and methods of selection | Methods §2.1, docs/data_decisions.md | ✅ |
| 7 | Definition of all variables | Methods §2.2–2.3, docs/phenotype_definitions.md | ✅ |
| 8 | Data sources and measurement | Methods §2.1–2.2 | ✅ |
| 9 | Bias | Discussion §4.2 | ✅ |
| 10 | Study size (rationale) | Methods §2.1, SAP §3 | ✅ |
| 11 | Statistical methods | Methods §2.5, SAP | ✅ |
| 11b | Methods for missing data | Methods §2.7, SAP §6.2 | ✅ |
| 11c | Sensitivity analyses | Methods §2.7, Phase 8 | ✅ |
| 12 | Participant flow | Results §3.1, Table 1 | ⚠ Pending real data |
| 13a | Numbers at each study stage | Results §3.1 | ⚠ Pending |
| 13b | Missing data | Supplement S4.2, results/tables/ | ✅ (scaffold) |
| 14 | Characteristics of participants | Results §3.1, Table 1 | ⚠ Pending real data |
| 15 | Outcome data | Results §3.3, Table 3 | ⚠ Synthetic scaffold |
| 16 | Main results | Results §3.3–3.5 | ⚠ Synthetic scaffold |
| 17 | Other analyses (subgroups) | Results §3.5 | ✅ |
| 18 | Key results summary | Discussion §4 | ✅ |
| 19 | Limitations | Discussion §4.2 | ✅ |
| 20 | Interpretation | Discussion §4, Conclusions §5 | ✅ |
| 21 | Generalisability | Discussion §4.1 | ✅ |
| 22 | Funding | Title page | ⚠ TBD |

---

## TRIPOD Checklist (Prediction Model Supplement)

| Item | TRIPOD Requirement | Location | Status |
|------|--------------------|----------|--------|
| 1 | Study type (development/validation) | Title, Methods | ✅ Development |
| 2 | Abstract with methods and results | Abstract | ✅ |
| 3a | Background: model purpose | Introduction §1 | ✅ |
| 3b | Objectives: specify model type | Introduction §1 | ✅ |
| 4a | Source of data | Methods §2.1 | ✅ |
| 4b | Dates of data collection | Methods §2.1 | ⚠ Pending real cohort |
| 4c | Outcome definition | Methods §2.3 | ✅ |
| 5a | Predictor variables | Methods §2.2, Table 1 | ✅ |
| 5b | Missing data handling | Methods §2.7, SAP §6.2 | ✅ |
| 6 | Sample size | Methods §2.1 | ✅ |
| 7 | Outcome prevalence | Results §3.1 | ⚠ Synthetic only |
| 8 | Missing data | Supplement S4.2 | ✅ (scaffold) |
| 9 | Statistical methods | Methods §2.5, SAP | ✅ |
| 10a | Predictors selection | Methods §2.2 | ✅ |
| 10b | Type of model | Methods §2.4–2.5 | ✅ |
| 10c | Model building procedure | Methods §2.4, src/models/ | ✅ |
| 10d | Internal validation | Methods §2.5 (5-fold CV) | ✅ |
| 11 | Model performance measures | Results §3.3, Table 3 | ✅ |
| 12 | Model equation | src/models/deai_build.py | ✅ |
| 13 | Participants and outcomes | Results §3.1 | ⚠ Pending |
| 14 | Model performance | Results §3.3 | ⚠ Synthetic scaffold |
| 15 | Calibration | Methods §2.5, results/figures/ | ✅ |
| 16 | Limitations | Discussion §4.2 | ✅ |
| 17 | Interpretation | Discussion §4 | ✅ |
| 18 | Generalisability | Discussion §4.1 | ✅ |
| 19 | Competing interests | Title page | ⚠ TBD |
| 20 | Supplementary materials | Supplement | ✅ |
| 21 | Code availability | README, GitHub | ✅ |

---

## Status Key
- ✅ Complete / addressed
- ⚠ Pending real cohort data or minor completion needed
- ❌ Missing (flag before submission)
