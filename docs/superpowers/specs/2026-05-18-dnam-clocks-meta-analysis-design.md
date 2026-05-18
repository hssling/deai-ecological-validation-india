# DNA-Methylation Clocks Meta-Analysis — Design Specification

**Spec date:** 2026-05-18
**Authors:** Dr Siddalingaiah H S (corresponding); Dr Chandrakala D
**Target journal:** *Biogerontology* (Springer) — APC-free under traditional subscription track
**Working title:** *Human interventions and DNA-methylation biological ageing clocks: a conservative systematic review and meta-analysis*

## 1. Scope, Question, and Eligibility

**Review question.** Among human intervention studies, which interventions measurably change validated DNA-methylation ageing biomarkers, especially DunedinPACE, GrimAge, PhenoAge, Horvath, Hannum, PCClocks, and DNAmTL?

**PICO.**
- **P:** Adults ≥18 y, any health status, enrolled in prospective intervention studies.
- **I:** Any deliberate human intervention measured pre- and post-intervention (caloric restriction, dietary patterns, exercise, supplements, pharmacological agents, multimodal lifestyle bundles, mind-body interventions).
- **C:** Placebo, usual care, attention control, or active comparator (in an RCT).
- **O (primary):** Change in any validated DNA-methylation ageing clock — DunedinPACE, GrimAge (v1/v2), PhenoAge, Horvath (multi-tissue 2013), Hannum (blood 2013), PCClocks (Higgins-Chen 2022), epigenetic telomere clocks (DNAmTL).
- **O (secondary):** Clock-derived age acceleration residuals, intrinsic vs extrinsic epigenetic age acceleration.

**Design eligibility (strict, as feasible).** Include parallel-group or crossover RCTs with a defined placebo, usual-care, or attention control, reporting pre/post DNAm-clock values (or change scores) with dispersion. Exclude single-arm trials, non-randomized cohorts, observational studies, animal studies, simulations, reviews, conference abstracts without extractable numeric data. Deviations from strict criteria, if necessary at execution, are logged in `docs/amendment_log.md`.

**Language/time.** English; database inception → freeze date set at search execution.

## 2. Search, Screening, Extraction

**Information sources.** PubMed/MEDLINE (E-utilities); Europe PMC; Crossref; OpenAlex; ClinicalTrials.gov (results-posted RCTs); bioRxiv/medRxiv (in-press RCTs); backward/forward citation chasing via OpenAlex.

**Search strategy (two-block Boolean).**
- Block 1 — clock terms: `"DunedinPACE" OR "GrimAge" OR "PhenoAge" OR "Horvath clock" OR "Hannum clock" OR "epigenetic age*" OR "epigenetic clock" OR "DNA methylation age" OR "DNAm age" OR "PCClock*" OR "DNAmTL"`.
- Block 2 — intervention/design: `"random*" OR "trial" OR "intervention" OR "supplement*" OR "exercise" OR "diet*" OR "caloric restriction" OR "rapamycin" OR "metformin" OR "NAD" OR "senolytic*"`.
- Combined: Block 1 AND Block 2; inception → freeze.

**Reuse pathway.** Re-screen existing `anti_ageing_review/results/tables/extracted_studies_master.csv` for DNAm-clock outcomes; top-up with fresh API pulls. All raw API responses cached under `data/raw/` with timestamps.

**Screening (two-stage).**
- Stage 1: Title/abstract — automated keyword classifier + two-author adjudication on flagged borderline cases (consensus resolution).
- Stage 2: Full-text against eligibility checklist; reasons-for-exclusion logged.

**Extraction (structured CSV).** Per study: bibliographic, design, n per arm, age (mean ± SD), sex distribution, health status, intervention class + dose + duration, comparator, clock(s) reported, baseline + post values (mean, SD) per arm, change scores if reported, follow-up time, conflict-of-interest disclosure, funding source.

**Risk of bias.** Cochrane RoB 2 for RCTs — randomization, deviations, missing data, measurement, selective reporting, overall.

## 3. Statistical Synthesis

**Effect measure.** Standardized mean difference (Hedges' g) of change-from-baseline, intervention vs control. For post-only studies, post-value SMD with sensitivity check. Median/IQR converted via Wan et al. (2014).

**Primary pooling.** Random-effects meta-analysis per clock (DerSimonian-Laird; Hartung-Knapp-Sidik-Jonkman as sensitivity). One forest plot per clock with ≥3 studies; clocks with <3 studies reported narratively. Pooled SMD with 95% CI **and 95% prediction interval**.

**Heterogeneity.** τ², I², Cochran's Q; prediction interval reported alongside every pooled estimate.

**Bayesian sensitivity.** BAYESMETA with weakly-informative half-normal(0.5) prior on τ; posterior median + 95% credible interval per clock.

**Subgroup analyses (pre-specified).** Intervention class (caloric restriction / exercise / supplement / pharmacological / multimodal); duration (<6 mo vs ≥6 mo); baseline age (<60 vs ≥60); health status (healthy vs disease cohort).

**Meta-regression.** Intervention duration and mean baseline age as continuous moderators when ≥10 studies per clock.

**Network meta-analysis.** Bayesian random-effects NMA across intervention classes for DunedinPACE and GrimAge only if ≥10 studies and a connected network exists. SUCRA rankings reported; otherwise dropped without overreach.

**Publication bias.** Funnel plot, Egger's regression, Begg's rank correlation, PET-PEESE, trim-and-fill (Duval-Tweedie) — only when ≥10 studies per clock.

**Sensitivity.** Leave-one-out per clock; low-RoB-only; ≥12-week interventions only; EPIC-array-only.

**GRADE.** Full GRADE evidence profile per intervention-class × clock cell with ≥3 studies.

**IPD request.** Standardized request letter to corresponding authors of included RCTs reporting arm-level summaries only; transparency log maintained; no analysis blocked on response.

**Software.** Python (statsmodels, scipy, numpy, pandas); R (`meta`, `metafor`, `bayesmeta`, `netmeta`) via subprocess. Random seed 42.

## 4. Manuscript Outputs & Deliverables

**Manuscript (Biogerontology, ~6,000–7,500 words main text).** Structured abstract (300 w); Introduction (~700 w); Methods (~2,200 w); Results (~2,000 w); Discussion (~1,500 w); Limitations (~300 w); Conclusion (~150 w).

**Main figures (4).**
1. PRISMA 2020 flow diagram.
2. Risk-of-bias traffic-light + summary plot (RoB 2).
3. Forest panel — one panel per clock with ≥3 studies (SMD, 95% CI, 95% PI).
4. Funnel + bias diagnostic panel — funnel + PET-PEESE adjusted estimate per clock with ≥10 studies.

**Main tables (3).**
1. Characteristics of included studies (PICO grid).
2. Per-clock pooled SMDs with τ², I², 95% CI, 95% PI, Bayesian credible interval.
3. GRADE evidence profile (intervention class × clock).

**Supplementary materials.** S1 search strings & dates; S2 PRISMA 2020 checklist; S3 excluded full texts + reasons; S4 full extracted data; S5 RoB 2 domain judgments with quotes; S6 leave-one-out / low-RoB / ≥12-wk sensitivity forests; S7 subgroup forests; S8 meta-regression bubble plots; S9 NMA network + SUCRA (conditional); S10 IPD request transparency log.

**Submission asset bundle (Biogerontology house style).** Title page; blinded manuscript; cover letter; declarations (funding, COI, ethics waiver, data availability, CRediT contributions); PRISMA 2020 checklist; highlights/bullet summary; 300 dpi PNG + editable SVG figures; Springer Vancouver reference list; supplementary appendix as single docx; submission checklist; reproducibility statement + GitHub/Zenodo link.

## 5. Repository Architecture & Reproducibility

**New standalone GitHub repository.** Suggested name: `dnam-clocks-meta-analysis`. License: MIT (code) + CC-BY-4.0 (data/manuscript drafts). Public at submission. CITATION.cff with both authors + ORCID. `.github/workflows/ci.yml` smoke test. Zenodo integration enabled for DOI at release tag `v1.0-submission`. Local scaffold first; `gh repo create hssling/dnam-clocks-meta-analysis --public --source=. --remote=origin --push` at appropriate phase.

**Local directory tree (under `anti_ageing_review/meta_dnam_clocks/`).**

```
meta_dnam_clocks/
├── config/meta_config.yaml
├── data/{raw,interim,processed}/
├── src/
│   ├── 01_search_dnam.py
│   ├── 02_rescreen_existing.py
│   ├── 03_dedup_merge.py
│   ├── 04_screen_titles_abs.py
│   ├── 05_screen_fulltext.py
│   ├── 06_extract_outcomes.py
│   ├── 07_rob2_assess.py
│   ├── 08_meta_analysis.py
│   ├── 09_subgroup_metareg.py
│   ├── 10_nma.py
│   ├── 11_pubbias_sensitivity.py
│   ├── 12_grade_profile.py
│   ├── 13_figures.py
│   └── 14_manuscript_build.py
├── manuscript/{manuscript_main.md, supplementary.md, templates/}
├── results/{figures, tables}/
├── submission_assets/Biogerontology_DNAmClocks_<freeze>/
└── docs/{protocol_v1.md, prisma_2020_checklist.md, decision_log.md, amendment_log.md}
```

**Reproducibility primitives.** Single `meta_config.yaml`; Makefile phase targets; cached API responses (no network on re-run); pinned `requirements_meta_dnam.txt`; programmatic figures only; provenance label on every output (REAL_DATA expected); git tag at submission freeze; Zenodo DOI placeholder.

**Authorship (CRediT).**
- **Dr Siddalingaiah H S** — Conceptualization, Methodology, Software, Formal analysis, Data curation, Writing – original draft, Visualization, Project administration. Corresponding author.
- **Dr Chandrakala D** — Conceptualization, Methodology, Validation, Investigation, Writing – review & editing, Supervision.

## 6. Execution Phases & Quality Gates

| # | Phase | Output | Quality gate |
|---|-------|--------|--------------|
| 1 | Protocol & repo scaffold | `protocol_v1.md`, repo tree, config, Makefile | Protocol mirrors PRISMA-P; repo runs `make help` |
| 2 | Search execution | Cached API responses across all 5 sources | ≥4/5 sources returned data; total raw records logged |
| 3 | Dedup + re-screen existing master | Merged candidate pool | Dedup rate reasonable; ≥30 candidate records remain |
| 4 | Screening (title/abs + full-text) | Inclusion list + exclusion-reasons log | ≥1 included RCT per major clock OR documented absence |
| 5 | Extraction + RoB 2 | `extracted_clock_studies.csv`, `rob2_assessments.csv` | All included studies extracted; RoB 2 dual-coded with disagreements resolved |
| 6 | Quantitative synthesis | Per-clock pools, subgroups, meta-reg, NMA (conditional), bias, GRADE | Pooling executes; ≥1 clock with ≥3 RCTs OR pivot to narrative |
| 7 | Manuscript + figures + supplementary | All docx assets in `submission_assets/` | All 4 main figs at 300 dpi; word counts within limits |
| 8 | Internal QA + repo publish | 2 internal peer reviews, validity audit, GitHub repo public + Zenodo DOI | All audits pass; CI green; bundle complete |

**Hard stops (halt-and-ask).**
- Zero RCTs included after Phase 4 → halt, present narrative-only pivot option.
- Network disconnected at Phase 6 NMA → drop NMA, continue without overreach.
- Any clock with no peer-reviewed RCT effect data → drop from manuscript with transparent statement.

**No synthetic effect-size data anywhere.** If real extraction fails, we narrate and disclose — we do not fabricate.

## Operating Principle

Across every phase: **"as feasible and robust"** — when a planned analysis cannot execute authentically, we drop it transparently rather than synthesize fragile estimates. All deviations recorded in `docs/amendment_log.md`.
