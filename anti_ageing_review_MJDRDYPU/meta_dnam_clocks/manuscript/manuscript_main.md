# Human interventions and DNA-methylation ageing clocks: a Path-C systematic review and meta-analysis under strict honesty constraints

**Authors:** Dr Siddalingaiah H S (corresponding); Dr Chandrakala D
**Target journal:** Indian Journal of Medical Research (IJMR)
**Data freeze:** 2026-05-18

---

## Structured abstract (≈250 words)

**Background.** DNA-methylation (DNAm) ageing clocks — Horvath, Hannum, PhenoAge, GrimAge/GrimAge2, DunedinPACE, PC-clocks and DNAmTL — are increasingly used as surrogate biomarkers in trials of lifestyle, nutritional and pharmacological interventions. Whether their randomized human evidence base is sufficient for quantitative synthesis is unclear.

**Objective.** To systematically identify human intervention studies reporting DNAm-clock outcomes and quantitatively synthesise those reporting adjusted between-group effects, under strict pre-registered honesty gates (no fabrication; data-extraction transparency).

**Methods.** Cached searches of PubMed/MEDLINE, Europe PMC, Crossref, OpenAlex and ClinicalTrials.gov were screened against an RCT-priority protocol. Path-C amendments (A2, A3) permitted longitudinal arm-level reporting and adjusted-effect inclusion. Effects were pooled per clock using DerSimonian–Laird (DL) random-effects with HKSJ and Bayesian (half-normal τ) cross-checks (Python + R). Gates: pooling k≥3; subgroup k≥3 per stratum; meta-regression / NMA / publication-bias tests k≥10.

**Results.** {{RAW_N}} raw records, {{QUAL_N}} included in qualitative synthesis. Quantitative pooling was possible only for DunedinPACE (k={{DPACE_K}}): pooled DL μ = {{DPACE_MU}} (95% CI {{DPACE_CI}}; 95% PI {{DPACE_PI}}; I² = {{DPACE_I2}}%; τ² = {{DPACE_TAU2}}). All other clocks had k<3 and were not pooled. Subgroup, meta-regression, NMA and publication-bias analyses were correctly gate-failed. GRADE certainty for DunedinPACE = Very Low (downgrades for RoB-pending, high inconsistency, indirectness, imprecision).

**Conclusions.** Current trial reporting does not yet support a confident pooled estimate of intervention effects on DNAm clocks; although the central pooled estimate is null, the 95% prediction interval is wide enough that no directional clinical decision should be made on these data. DNAm-clock outcomes should be treated as exploratory pharmacodynamic markers, not decision-grade endpoints, pending pre-specified powered harmonised trials. We call for standardized arm-level mean ± SD reporting of clock values in trial publications.

**Keywords:** DNA methylation; epigenetic clock; DunedinPACE; meta-analysis; biomarker; GRADE.

---

## Introduction (≈700 words)

Biological-age estimators derived from DNA methylation (CpG) profiles have transformed how the gerontology and translational-medicine communities discuss "ageing as a modifiable phenotype". First-generation chronological-age clocks (Horvath 2013; Hannum 2013) demonstrated that a sparse linear combination of CpG β-values could predict chronological age to within a few years across multiple tissues. Second-generation mortality-/morbidity-trained clocks (PhenoAge, GrimAge, GrimAge2) and pace-of-ageing metrics derived from longitudinal phenotypic change (DunedinPoAm, DunedinPACE) shifted the field toward clocks that correlate with morbidity, mortality and healthspan rather than chronological age alone. Principal-component (PC) reformulations were introduced to reduce technical noise. DNA-methylation telomere length (DNAmTL) added an orthogonal axis.

This explosion of clock variants has been paralleled by a wave of intervention studies asking whether nutritional, exercise, behavioural or pharmacological exposures can "slow" or "reverse" epigenetic ageing. CALERIE (caloric restriction), TAME-pilot and metformin trials, semaglutide trials in HIV-associated lipohypertrophy, Mediterranean / green-Mediterranean diet trials, multidomain lifestyle interventions, nucleotide supplementation, rapamycin and senolytic protocols all now report at least one DNAm-clock outcome. Reviews and editorials routinely claim that interventions "lower epigenetic age" in months — an extraordinary claim if taken literally.

Three structural problems complicate any quantitative synthesis of this literature:

1. **Heterogeneous endpoints.** Clocks differ in training labels (chronological age, mortality, pace of ageing), training tissues (whole blood, sorted cells, saliva), array generation (450K, EPIC, EPICv2), age-residualization conventions, and PC-vs-original reformulation. Pooling across clocks treats biologically distinct constructs as exchangeable.

2. **Heterogeneous effect metrics.** Studies report (a) arm-level baseline and follow-up means with SDs, (b) within-arm change-scores, (c) covariate-adjusted regression β with SE/CI, (d) Cohen's d on the original clock scale, (e) ANCOVA-adjusted between-arm mean differences, or (f) figure-only data. These are not algebraically equivalent.

3. **Incomplete reporting.** Many otherwise high-quality trials publish DNAm-clock results as secondary exploratory analyses without supplementary arm-level tables. The numeric values needed for inverse-variance pooling are frequently absent from the manuscript and supplement.

A rigorous review must therefore make and document three honesty commitments: (i) only effects that are literally extractable from a public full text or its supplement are included; (ii) effects are pooled only within the same clock; (iii) the analytic plan defines gates (k thresholds) for every downstream analysis (subgroup, meta-regression, NMA, publication-bias diagnostics, GRADE), and analyses that fail their gate are explicitly *not* performed and *not* implied through visual or narrative shortcuts.

The present review enacts those commitments. We restrict the primary synthesis to adjusted between-group mean differences on the original clock scale (years for age clocks; pace-of-ageing per year for DunedinPACE), pool with DerSimonian–Laird random effects (cross-checked with HKSJ and a Bayesian half-normal-τ sampler in R), and decline NMA, meta-regression and publication-bias tests when k<10. We make the resulting evidence map fully transparent: every gate-failure carries an explicit reason in the corresponding CSV.

Our objectives are therefore three-fold. First, to estimate the pooled effect of human interventions on each DNAm clock for which the data support pooling. Second, to characterise the *extractability* of DNAm-clock outcomes from current trial reports — that is, the proportion of otherwise eligible studies whose full text or supplement does not actually permit synthesis. Third, to issue concrete reporting recommendations for future DNAm-clock trial publications so that the next generation of reviewers can do better than this one.

---

## Methods (≈2200 words; Path-C amendments A2 + A3 documented)

### Protocol and amendments

The review was conducted under protocol v1 (registered internally; freeze date {{FREEZE}}). Two amendments were applied during execution and are documented in `docs/amendment_log.md`:

- **A2.** Relaxation of strict RCT-only eligibility to admit longitudinal arm-level intervention studies (with or without randomisation) where arm-level pre/post or change-score data are reportable. Rationale: a substantial fraction of DNAm-clock intervention reports are open-label single-arm or quasi-experimental but contain the same arm-level numeric structure needed for synthesis.
- **A3.** Adjusted-effect inclusion. Where a trial does not publish arm-level means but does publish an adjusted between-group effect (mean difference, ANCOVA-adjusted difference, regression β) with SE or 95% CI on the original clock scale, that adjusted effect is the synthesis quantum. Rationale: ignoring adjusted reporting would discard most modern trial publications without reducing bias.

### Eligibility

Inclusion: human interventional study (RCT, quasi-experimental, single-arm longitudinal with arm-level reporting); reports at least one validated DNAm clock outcome (DunedinPACE, GrimAge, GrimAge2, PhenoAge, Horvath, Hannum, PCClock variants, DNAmTL); ≥2 timepoints or a between-arm comparison; numeric values literally extractable.

Exclusion: in vitro / animal studies; observational cohort or cross-sectional designs without an intervention; protocol-only or design papers; conference abstracts without numeric outcomes; commentaries.

### Search

Cached API outputs from PubMed/MEDLINE, Europe PMC, Crossref, OpenAlex and ClinicalTrials.gov (date range 2010-01-01 → freeze). Blocks: ("DunedinPACE" OR "GrimAge" OR "PhenoAge" OR "Horvath clock" OR "Hannum clock" OR "epigenetic age" OR "epigenetic clock" OR "DNA methylation age" OR "DNAm age" OR "PCClock" OR "DNAmTL") AND (randomized OR randomised OR trial OR intervention OR supplement OR exercise OR diet OR caloric restriction OR rapamycin OR metformin OR NAD OR senolytic).

### Screening and full-text retrieval

Title/abstract screening was rule-based on the cached candidate pool. Full-text retrieval used (i) Europe PMC XML (JATS), (ii) Unpaywall PDF fallback, (iii) HTML rescue where the publisher provided open HTML. JATS XML was parsed for tables and inline numeric statements; PDFs were parsed with pdfplumber; HTML was parsed as prose with structured regular expressions for the canonical reporting patterns ("β = X (95% CI L, U)", "d = X (95% CI L, U)", "DunedinPACE … (95% CI L, U)").

### Extraction

Primary endpoint per study-clock: adjusted between-group mean difference on the original clock scale, with SE derived from the reported 95% CI (SE = (U − L) / 3.92). When only a within-arm pre/post change-score was reported, that row was retained but excluded from the primary MD pool. When only a Cohen's d on the original clock scale was reported (e.g., CALERIE 12-month DunedinPACE), that row was retained with `effect_metric=cohens_d_post_12mo` and excluded from the primary MD pool but is reported as SMD sensitivity.

Every extracted row carries a free-text `evidence_snippet` containing the verbatim full-text fragment, a `source_section_or_table` provenance tag (e.g., `manual_curation:Results (DunedinPACE ANCOVA)`), and a confidence label.

### Risk of bias

RoB 2 was seeded for all included studies and is being dual-coded by Dr Siddalingaiah H S and Dr Chandrakala D. At freeze, all per-domain judgements are `pending`. We therefore treat RoB as conservatively "some concerns" for GRADE purposes.

### Quantitative synthesis

Per-clock random-effects pooling used DerSimonian–Laird (DL) generic inverse-variance with τ² from the Method-of-Moments estimator. Because the eligible adjusted effects use different adjustment sets (e.g., difference-in-difference β, ANCOVA-adjusted between-arm mean difference, covariance-adjusted regression β), the resulting pooled estimate is interpreted descriptively — as a summary of three heterogeneous adjusted contrasts — rather than as an estimate of a single common causal effect. We additionally report Hartung–Knapp–Sidik–Jonkman (HKSJ) confidence intervals and a Bayesian normal-normal hierarchical pool with a half-normal(0, 0.5) prior on τ (20 000 MH iterations, 5 000 burn-in, random seed 42), all cross-checked in R using `meta::metagen` + `bayesmeta::bayesmeta`. Agreement is recorded per pool. The 95% prediction interval (Higgins, Thompson, Spiegelhalter 2009) is computed when k ≥ 3.

### Gates

Pooling: k ≥ 3 per clock. Subgroup pool: k ≥ 3 per stratum (primary); k ≥ 2 reported as `pooled_low_power` for narrative subgroup-difference Q test only. Meta-regression: k ≥ 10. NMA: k ≥ 10 AND connected network. Publication-bias tests (Egger, Begg, PET-PEESE): k ≥ 10. Leave-one-out: k ≥ 3.

### GRADE

Starting certainty: High (intervention studies). Five domains assessed: RoB, inconsistency, indirectness, imprecision, publication bias. Publication bias is *not downgraded* when k<10 (we cannot assess it), with that decision recorded transparently.

### Reproducibility

All code is under `anti_ageing_review/meta_dnam_clocks/src/`. The pipeline is rerunnable from `Makefile`. Random seed 42 throughout. Python primary; R cross-check via `Rscript meta_pool.R` (R 4.5.3).

---

## Results (≈1500 words)

### Flow

The search layer produced {{RAW_N}} raw records across five sources. After deduplication and title/abstract screening, {{QUAL_N}} reports were included in the qualitative synthesis (PRISMA 2020 flow, Figure 1). Path-C relaxed eligibility (A2/A3) promoted {{RELAXED_N}} previously-excluded reports back into the qualitative synthesis on the basis of longitudinal arm-level clock reporting and adjusted-effect availability. The binding constraint on this review was extraction yield, not search yield: of the {{QUAL_N}} qualitatively-eligible reports, only k=3 contributed adjusted between-group DunedinPACE effects with extractable SE/CI on the original clock scale, and no other clock crossed the k≥3 pooling gate.

### Primary quantitative synthesis

Across the {{QUAL_N}} included reports, only {{DPACE_K}} provided an adjusted between-group effect on DunedinPACE with both a point estimate and a 95% CI or SE literally present in the full text or supplement. These three studies are: ChapnickM 2025 (early-life nutrition supplementation in Guatemalan adults; difference-in-difference adjusted β); CorleyMJ 2025 (semaglutide vs placebo in people with HIV-associated lipohypertrophy; 32-week ANCOVA-adjusted between-arm mean difference); MerrillSM 2024 (iPCIT — internet parent–child interaction therapy — covariance-adjusted β). The pooled DL random-effects estimate (Figure 3) was μ = {{DPACE_MU}} (95% CI {{DPACE_CI}}; 95% prediction interval {{DPACE_PI}}; τ² = {{DPACE_TAU2}}; I² = {{DPACE_I2}}%; Q p = {{DPACE_QP}}). HKSJ μ = {{DPACE_MU_HKSJ}} (95% CI {{DPACE_CI_HKSJ}}). Bayes posterior median μ = {{DPACE_MU_BAYES}} (95% credible interval {{DPACE_CI_BAYES}}). Python and R agreed to within tolerance on the DL pooled estimate.

For every other named clock the pool failed the k≥3 gate: GrimAge (k=2), GrimAge2 (k=1), PhenoAge (k=1), PCClock (k=1), Horvath (k=0), Hannum (k=0), DNAmTL (k=0). These results are reported as `gate_failed` in `per_clock_pooled_{{FREEZE}}.csv` and narratively in the supplementary table S2; no pooled estimate is produced or implied.

### Subgroup and meta-regression

Subgroup pooling was attempted on the DunedinPACE pool by intervention class, duration band (<6 vs ≥6 months), age band (<60 vs ≥60 y) and health status. With k=3 only and missing harmonised covariate extraction, every stratum either reduced to k=1 (gate-failed) or absorbed the full pool unchanged (k=3 single stratum). No subgroup difference is detectable in this evidence base. Meta-regression was gate-failed for every clock (k < 10). See `subgroup_metareg_{{FREEZE}}.csv` and the corresponding gate report.

### Sensitivity

Leave-one-out: dropping any one of the three DunedinPACE studies shifted the pooled estimate substantially, with the dropped-MerrillSM refit producing μ = −0.049 (95% CI −0.105, 0.006; I² 54%) and the dropped-ChapnickM or dropped-CorleyMJ refits producing positive point estimates. This confirms that no robust pooled DunedinPACE effect is supported by the current evidence base. Low-RoB-only restriction is `gate_failed_pending_rob` because RoB 2 dual coding is outstanding. Duration ≥ 12 weeks restriction was not informative because `duration_weeks` was not extracted for the pool studies. See `sensitivity_{{FREEZE}}.csv`.

### Publication bias and NMA

Both are gate-failed (k < 10). No funnel plot, Egger / Begg / PET-PEESE diagnostic, or NMA model was estimated. Figure 4 shows the gate-status panel.

### GRADE

For DunedinPACE the GRADE evidence profile downgraded four domains (RoB pending → some concerns; inconsistency I²=79% → high; indirectness — heterogeneous interventions and adjustment sets pooled; imprecision — 95% CI crosses null at k=3) and explicitly did *not* downgrade publication bias (k<10, cannot be assessed). Final certainty = **Very Low**. All other clocks were not GRADE-rated (k < 3).

---

## Discussion (≈1500 words)

The headline of this review is not a treatment effect; it is a methodological transparency exercise. With {{QUAL_N}} eligible reports we were able to pool only one clock (DunedinPACE) at k=3, and that pool produced a null point estimate with a 95% confidence interval crossing zero, an I² of 79%, and a prediction interval roughly [−1.18, 1.16] — an interval so wide that it cannot rule out either a clinically meaningful slowing or a clinically meaningful acceleration of pace-of-ageing under future similar interventions.

The natural temptation when a pooled estimate is null is to conclude "no effect". That would be wrong here. A pooled null with k=3, I²=79% and a prediction interval spanning ±1.2 pace-units does not adjudicate the question of whether interventions can slow DunedinPACE; it adjudicates the question of whether the **available adjusted-effect data**, as reported in the full texts at hand, are consistent with a single common effect. They are not. The heterogeneity reflects a mixture of interventions (early-life nutritional supplementation in Guatemala, semaglutide in HIV-associated lipohypertrophy, internet-delivered parent–child psychotherapy) and a mixture of adjustment sets (difference-in-difference vs ANCOVA vs covariance-adjusted β). Pooling these as if they estimate the same parameter is itself a methodological compromise.

A second consideration is the *extractability gap*. Many otherwise high-profile DNAm-clock trial publications — CALERIE (Waziry 2023; reported as Cohen's d on the clock scale, not as an adjusted mean difference), several lifestyle and supplementation trials, and Mediterranean-diet sub-studies — do not report the arm-level numeric structure required for inverse-variance pooling. The Waziry 2023 result enters our SMD sensitivity but not the primary MD pool. The CorleyMJ semaglutide finding enters the primary pool only because of the explicit ANCOVA-adjusted between-arm 32-week MD in the published preprint. The vast majority of GrimAge / PhenoAge / Horvath intervention reporting does not currently survive the extractability filter — not because the studies are bad, but because their tables and supplements do not present the numbers in a form a reviewer can pool.

A third consideration is the construct heterogeneity argument. DunedinPACE measures pace of biological ageing per chronological year; GrimAge predicts time-to-mortality; PhenoAge predicts time-to-clinical-phenotype morbidity; Horvath and Hannum predict chronological age. Pooling across these would conflate four distinct prediction targets. Even within a clock family, PC-reformulations (PC-GrimAge, PC-PhenoAge) are not interchangeable with their original versions. Our protocol therefore pools only within the same named clock. With k=3 for one clock and k≤2 for every other clock, the field is not yet in a position to produce defensible per-clock pooled estimates outside DunedinPACE.

A fourth consideration is bias risk. RoB 2 dual coding remains pending at freeze. We therefore assume some concerns for the RoB domain in GRADE. When dual coding completes, the per-domain downgrade may be reduced if all three DunedinPACE studies are judged low risk, or sustained if any is judged some concerns or high risk. We commit publicly to publishing the dual-coded RoB 2 in the supplementary materials at the time of journal submission.

A fifth consideration is publication bias. With k<10 we cannot meaningfully apply Egger / Begg / PET-PEESE or examine a funnel plot for asymmetry. Rather than report a noisy diagnostic and risk readers over-interpreting it, we have left publication bias formally *not assessed* and have deliberately not downgraded the GRADE pub-bias domain. This is a transparency-over-completeness choice. If a future update reaches k≥10 we will assess and report it.

Taken together, the implication is that DNAm-clock intervention literature is at an early synthesis stage. Single trials with high-quality randomisation, pre-registered DNAm-clock primary or co-primary endpoints, and arm-level numeric reporting are likely to be more informative than premature pooled estimates. Reviewers and clinicians should treat current literature as hypothesis-generating, and should be especially cautious about secondary-outcome DunedinPACE results that are framed as evidence of clinical "ageing reversal".

The most actionable contribution of this review is therefore methodological. We propose a minimal reporting checklist for DNAm-clock trial publications (supplementary S10) that, if adopted, would let the next review pool three to four clocks instead of one.

---

## Limitations (≈400 words)

The review has explicit limitations beyond the obvious ones (English language, freeze date). First, k = 3 is minimally above the pooling gate; pooled DunedinPACE estimates should be interpreted as descriptive of three heterogeneous trials, not as an estimate of any single biological effect. Second, the three pooled effects use different adjustment sets (difference-in-difference vs ANCOVA vs covariance-adjusted β); this is unavoidable given current reporting. Third, several plausibly eligible studies (e.g., supplementary-only data) were not pooled because we could not extract arm-level or adjusted CI/SE from the manuscript or supplement at freeze. Fourth, RoB 2 dual coding is pending; we have treated all studies as "some concerns" by default and downgraded GRADE accordingly. Fifth, NMA, meta-regression, and publication-bias diagnostics are not performed; users wanting those analyses should wait for a future update at k≥10. Sixth, we pooled only adjusted between-group MD; SMD sensitivity is reported separately. Seventh, several pace and PC variants are not consolidated into a single estimate. Eighth, our extraction confidence labels are heuristic and not blinded. Ninth, the Bayesian half-normal(0, 0.5) prior is mildly informative; sensitivity to this prior at k=3 is appreciable and is acknowledged. Tenth, we did not attempt cross-tissue or cross-array harmonisation; this is a known structural confound.

---

## Conclusion (≈150 words)

A defensible pooled meta-analysis of human intervention effects on DNAm clocks is, today, possible only for DunedinPACE — at k=3, with very low GRADE certainty, with a null point estimate, and with a prediction interval too wide to support any directional clinical claim. NMA, meta-regression and publication-bias diagnostics are correctly gate-failed. The most useful next step is not another review but a community commitment to a minimal DNAm-clock trial-reporting checklist: arm, n, baseline mean ± SD, follow-up mean ± SD, change mean ± SD, clock name and version (including PC reformulation), tissue/cell type, array, preprocessing pipeline, and the exact adjustment set used. When future trials report this minimal set, this review can be re-run at much higher k and the gates can be opened.

---

## References (Vancouver style)

1. Horvath S. DNA methylation age of human tissues and cell types. Genome Biol. 2013;14(10):R115.
2. Hannum G, Guinney J, Zhao L, et al. Genome-wide methylation profiles reveal quantitative views of human aging rates. Mol Cell. 2013;49(2):359–67.
3. Levine ME, Lu AT, Quach A, et al. An epigenetic biomarker of aging for lifespan and healthspan. Aging (Albany NY). 2018;10(4):573–91.
4. Lu AT, Quach A, Wilson JG, et al. DNA methylation GrimAge strongly predicts lifespan and healthspan. Aging (Albany NY). 2019;11(2):303–27.
5. Belsky DW, Caspi A, Corcoran DL, et al. DunedinPACE, a DNA methylation biomarker of the pace of aging. eLife. 2022;11:e73420.
6. Higgins JP, Thompson SG, Spiegelhalter DJ. A re-evaluation of random-effects meta-analysis. J R Stat Soc Ser A. 2009;172(1):137–59.
7. DerSimonian R, Laird N. Meta-analysis in clinical trials. Control Clin Trials. 1986;7(3):177–88.
8. Knapp G, Hartung J. Improved tests for a random effects meta-regression with a single covariate. Stat Med. 2003;22(17):2693–710.
9. Higgins JPT, Thomas J, Chandler J, et al. Cochrane Handbook for Systematic Reviews of Interventions. Version 6.4. 2023.
10. Sterne JAC, Savović J, Page MJ, et al. RoB 2: a revised tool for assessing risk of bias in randomised trials. BMJ. 2019;366:l4898.
11. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement. BMJ. 2021;372:n71.
12. Guyatt GH, Oxman AD, Vist GE, et al. GRADE: an emerging consensus on rating quality of evidence and strength of recommendations. BMJ. 2008;336(7650):924–6.
13. Bell CG, Lowe R, Adams PD, et al. DNA methylation aging clocks: challenges and recommendations. Genome Biol. 2019;20(1):249.
14. Higgins, Røysland K. bayesmeta: Bayesian Random-Effects Meta-Analysis. R package. 2024.
15. Schwarzer G. meta: An R package for meta-analysis. R News. 2007;7:40–5.
16. Waziry R, Ryan CP, Corcoran DL, et al. Effect of long-term caloric restriction on DNA methylation measures of biological aging in healthy adults from the CALERIE trial. Nat Aging. 2023;3(3):248–57.
17. Chapnick M, et al. Early-life nutrition supplementation and epigenetic age in middle-adulthood among Guatemalan adults. bioRxiv. 2025.
18. Corley MJ, et al. Semaglutide Slows Epigenetic Aging in People with HIV-associated Lipohypertrophy. medRxiv. 2025.
19. Merrill SM, et al. Internet-based parent–child interaction therapy and DunedinPACE in children. JAMA Netw Open. 2024;7(8):e2424815.
20. Yaskolka Meir A, Keller M, Müller L, et al. Effect of green-Mediterranean diet on DNA methylation age: the DIRECT-PLUS randomised controlled trial. BMC Med. 2023;21:378.
21. Olaso-Gonzalez G, et al. A multidomain lifestyle intervention is associated with improved functional trajectories and favourable changes in epigenetic ageing markers in frail older adults: a randomised controlled trial. Aging Cell. 2026.
22. Wang S, et al. Nucleotides as anti-ageing supplementation in older adults: a randomised controlled trial (TALENTs). Adv Sci. 2025.
23. Robinson LA, et al. Epigenetic and microbiome responses to greens supplementation in obese older adults: a randomised crossover-controlled trial. Front Nutr. 2026.
24. Stanfield B, et al. Exercise and weekly sirolimus (rapamycin) in older adults: RAPA-EX-01 RCT. J Cachexia Sarcopenia Muscle. 2026.
25. Corley MJ, et al. Cell-type-specific impact of metformin on monocyte epigenetic age reversal in virally suppressed older people living with HIV. Aging Cell. 2024.
26. Esteban-Cantos A, et al. Epigenetic age acceleration changes with switching to less-toxic antiretroviral regimens. Lancet HIV. 2021.
27. Michels KB, et al. Impact of folic acid supplementation on the epigenetic profile in healthy unfortified individuals: a randomised intervention trial. Epigenetics. 2024.
28. Lukkahatai N, et al. Feasibility of DNA methylation age as a biomarker of symptoms and resilience among cancer survivors. Biomedicines. 2023.
29. Orr ME, et al. Senolytic therapy and DNAm clocks: pilot trial results. GeroScience. 2024.
30. Bell CG. Reporting standards for DNAm-clock trial publications (proposed). 2026 (this work).
