# Protocol v1 — DNA-Methylation Clocks Meta-Analysis

**Protocol date:** 2026-05-18
**Working title:** *Human interventions and DNA-methylation biological ageing clocks: a conservative systematic review and meta-analysis*
**Target journal:** *Biogerontology* (Springer; APC-free traditional subscription track)
**Authors:** Dr Siddalingaiah H S (corresponding); Dr Chandrakala D
**Operating principle:** *"as feasible and robust"* — when a planned analysis cannot execute authentically, drop it transparently rather than synthesize fragile estimates. **No synthetic effect-size data anywhere.** All deviations recorded in `docs/amendment_log.md`.

This protocol follows PRISMA-P 2015 reporting guidance and is registered locally in the project repository. It will be lodged to OSF or PROSPERO before search execution.

---

## 1. Review Question, PICO, and Eligibility

### 1.1 Review question
Among human intervention studies, which interventions measurably change validated DNA-methylation (DNAm) ageing biomarkers — DunedinPACE, GrimAge (v1/v2), PhenoAge, Horvath (multi-tissue 2013), Hannum (blood 2013), PCClocks (Higgins-Chen 2022), and epigenetic telomere length (DNAmTL)?

### 1.2 PICO
- **Population (P):** Adults aged ≥18 years, any health status, enrolled in prospective intervention studies.
- **Intervention (I):** Any deliberate human intervention measured pre- and post-intervention — caloric restriction, dietary patterns, exercise, supplements, pharmacological agents, multimodal lifestyle bundles, mind-body interventions.
- **Comparator (C):** Placebo, usual care, attention control, or active comparator within an RCT design.
- **Outcomes — primary (O₁):** Change in any validated DNAm ageing clock: DunedinPACE, GrimAge (v1/v2), PhenoAge, Horvath multi-tissue (2013), Hannum blood (2013), PCClocks (Higgins-Chen 2022), DNAmTL.
- **Outcomes — secondary (O₂):** Age-acceleration residuals; intrinsic epigenetic age acceleration (IEAA); extrinsic epigenetic age acceleration (EEAA).

### 1.3 Design eligibility (strict)
**Include** parallel-group or crossover RCTs with a defined placebo, usual-care, attention-control, or active comparator arm, reporting pre/post DNAm-clock values (or change scores) with dispersion estimates suitable for SMD calculation.

**Exclude** single-arm trials; non-randomized cohorts; observational studies; animal studies; in-silico simulations; reviews; conference abstracts without extractable numeric data.

### 1.4 Language and time frame
English-language reports; database inception through search-execution freeze date (planned freeze: **2026-05-18**).

---

## 2. Information Sources, Search Strategy, Screening, Extraction, RoB

### 2.1 Information sources
- PubMed/MEDLINE (NCBI E-utilities)
- Europe PMC REST API
- Crossref REST API
- OpenAlex API
- ClinicalTrials.gov (results-posted RCTs)
- bioRxiv / medRxiv preprint servers (in-press RCTs)
- Backward and forward citation chasing via OpenAlex `referenced_works` / `cited_by_api_url`

All raw API responses are cached under `data/raw/` with retrieval timestamps so the pipeline runs offline after the first pull.

### 2.2 Search strategy
A two-block Boolean strategy is applied to each source.

- **Block 1 — clock terms:** *DunedinPACE, GrimAge, PhenoAge, Horvath clock, Hannum clock, epigenetic age(s), epigenetic clock, DNA methylation age, DNAm age, PCClock(s), DNAmTL*.
- **Block 2 — intervention/design terms:** *random\*, trial, intervention, supplement\*, exercise, diet\*, caloric restriction, rapamycin, metformin, NAD, senolytic\**.
- **Combined query:** Block 1 **AND** Block 2; inception to freeze.

Exact query strings, field tags, and date ranges are codified in `config/meta_config.yaml` (single source of truth).

### 2.3 Re-use of existing extraction pool
The pipeline re-screens `anti_ageing_review/results/tables/extracted_studies_master.csv` from the parent anti-ageing review for DNAm-clock outcomes; this is topped up with fresh API pulls.

### 2.4 Screening (two-stage, dual-reviewer)
- **Stage 1 (title/abstract):** Automated keyword classifier flags candidates; two reviewers (HSS, CD) independently adjudicate flagged and borderline records. Disagreements resolved by consensus discussion.
- **Stage 2 (full-text):** Independent dual review against the eligibility checklist; reasons for exclusion are logged in a structured CSV.

Reliability between reviewers will be reported (Cohen's κ) where feasible.

### 2.5 Data extraction
Structured CSV extraction per study capturing: bibliographic identifiers; trial design; *n* per arm; age (mean ± SD); sex distribution; health status; intervention class, dose, and duration; comparator; clocks reported; baseline and post values (mean, SD) per arm; change scores where reported; follow-up time; conflict-of-interest disclosure; funding source; DNAm array platform (450K / EPIC / other).

Where dispersion is reported as median/IQR, conversion uses Wan et al. (2014). Where data are insufficient, a standardized IPD request letter is sent to corresponding authors and tracked in an IPD log; no analysis is blocked on response.

### 2.6 Risk of bias
Cochrane **RoB 2** for RCTs across the five domains plus overall judgment: randomization process; deviations from intended interventions; missing outcome data; measurement of the outcome; selective reporting. Dual coding with consensus resolution.

---

## 3. Statistical Synthesis

All analyses are implemented in **Python only** (statsmodels, scipy, numpy, pandas). R/Rscript is not installed on the host machine, so the original plan's R subprocess calls have been dropped; equivalent Python implementations are specified below. Random seed: **42**.

### 3.1 Effect measure
Hedges' *g* standardized mean difference of **change from baseline** (intervention vs control), computed with the Borenstein (2009) formulas including small-sample correction *J*. For post-only studies, post-value SMD is used with a sensitivity check. Median/IQR are converted to mean/SD via Wan et al. (2014).

### 3.2 Primary pooling — DerSimonian-Laird random effects
Per clock with ≥3 studies, a DerSimonian-Laird (DL) random-effects model is fitted using
`statsmodels.stats.meta_analysis.combine_effects(..., method_re='dl')`,
returning pooled SMD, 95% CI, τ², I², Cochran's Q. A 95% **prediction interval** is computed from τ² and reported alongside every pooled estimate. One forest plot per clock with ≥3 studies; clocks with <3 studies are reported narratively.

### 3.3 Sensitivity pooling — HKSJ
Hartung–Knapp–Sidik–Jonkman adjustment is applied as a sensitivity pool via
`combine_effects(..., method_re='dl', use_t=True)`,
which substitutes a *t*-distribution and the HKSJ variance correction; results are reported next to the DL primary pool.

### 3.4 Sensitivity pooling — Bayesian
A weakly-informative half-normal(0, 0.5) prior on between-study heterogeneity τ is used. The posterior on τ and the pooled mean is sampled with NumPy/scipy (Metropolis–Hastings on the normal–normal hierarchical likelihood, 4 chains × 5,000 draws, 1,000 burn-in), reporting posterior median and 95% credible interval. This replaces the original BAYESMETA R implementation.

### 3.5 Heterogeneity
τ², I², Cochran's Q, and the 95% prediction interval are reported for every pooled estimate.

### 3.6 Subgroup analyses (pre-specified)
- Intervention class (caloric restriction / exercise / supplement / pharmacological / multimodal / mind-body)
- Duration (<6 months vs ≥6 months)
- Baseline age (<60 y vs ≥60 y)
- Health status (healthy vs disease cohort)

Between-subgroup heterogeneity is assessed by Q-between.

### 3.7 Meta-regression
Continuous moderators `duration_weeks` and `age_mean` are entered when ≥10 studies per clock are available, using a mixed-effects meta-regression with DL τ² (`statsmodels` weighted least squares with random-effects variance term).

### 3.8 Conditional network meta-analysis
A Bayesian random-effects NMA across intervention classes is run for **DunedinPACE** and **GrimAge** only if (a) ≥10 studies and (b) a connected network exists. Implementation uses a NumPy/scipy Gibbs sampler on the consistency model; SUCRA rankings are reported. If either condition fails the NMA is dropped transparently.

### 3.9 Publication / reporting bias
When ≥10 studies per clock are available: funnel plot; **Egger's regression** via `scipy.stats.linregress` on standardized effects against their precision; **Begg's rank correlation** via Kendall's τ (`scipy.stats.kendalltau`); **PET-PEESE**; **trim-and-fill (Duval-Tweedie)** implemented in-house in Python.

### 3.10 Sensitivity analyses
- Leave-one-out per clock
- Low-RoB-only re-pool
- ≥12-week interventions only
- EPIC-array-only

### 3.11 GRADE
A full GRADE evidence profile is produced per intervention-class × clock cell with ≥3 studies, downgrading for risk of bias, inconsistency, indirectness, imprecision, and publication bias per GRADE handbook.

### 3.12 IPD request log
A transparency log of all author IPD requests, dates, and outcomes is maintained at `docs/ipd_request_log.md`. No analysis is blocked on response.

---

## 4. Deliverables Summary

**Manuscript.** Structured abstract (300 w); IMRaD main manuscript (~6,000–7,500 w) comprising Introduction (~700 w), Methods (~2,200 w), Results (~2,000 w), Discussion (~1,500 w), Limitations (~300 w), and Conclusion (~150 w).

**Main figures (4).**
1. PRISMA 2020 flow diagram.
2. Risk-of-bias traffic-light plot plus weighted-bar summary (RoB 2).
3. Forest panel — one sub-panel per clock with ≥3 studies (SMD, 95% CI, 95% PI).
4. Funnel + bias diagnostic panel — funnel plot plus PET-PEESE adjusted estimate per clock with ≥10 studies.

**Main tables (3).**
1. Characteristics of included studies (PICO grid).
2. Per-clock pooled SMDs with τ², I², 95% CI, 95% PI, Bayesian credible interval.
3. GRADE evidence profile (intervention class × clock).

**Supplementary materials.** S1 search strings and dates; S2 PRISMA 2020 checklist (this document, completed); S3 excluded full texts with reasons; S4 full extracted dataset; S5 RoB 2 domain judgments with supporting quotations; S6 leave-one-out / low-RoB / ≥12-week sensitivity forests; S7 subgroup forests; S8 meta-regression bubble plots; S9 NMA network diagram + SUCRA (conditional); S10 IPD request transparency log.

**Submission bundle (Biogerontology house style).** Title page; blinded manuscript; cover letter; declarations (funding, COI, ethics waiver, data availability, CRediT contributions); PRISMA 2020 checklist; highlights/bullet summary; 300 dpi PNG plus editable SVG figures; Springer Vancouver reference list; supplementary appendix as a single docx; submission checklist; reproducibility statement with GitHub/Zenodo link.

## 4a. Reproducibility and Authorship

**Reproducibility primitives.** A single `meta_config.yaml` is the source of truth for all parameters. Makefile phase targets orchestrate the pipeline. All API responses are cached so re-runs are offline. Dependencies are pinned in `requirements_meta_dnam.txt`. Figures and tables are produced programmatically only. Every output carries a provenance label (`REAL_DATA` expected). A git tag marks the submission freeze; a Zenodo DOI is minted at release.

**Authorship (CRediT).**
- **Dr Siddalingaiah H S** — Conceptualization, Methodology, Software, Formal analysis, Data curation, Writing – original draft, Visualization, Project administration. Corresponding author.
- **Dr Chandrakala D** — Conceptualization, Methodology, Validation, Investigation, Writing – review & editing, Supervision.

---

## 5. Hard Stops

- Zero RCTs included after Phase 4 → halt, present narrative-only pivot.
- Disconnected network at Phase 6 NMA → drop NMA, continue without overreach.
- Any clock with no peer-reviewed RCT effect data → drop from manuscript with transparent statement.

---

*End of Protocol v1.*
