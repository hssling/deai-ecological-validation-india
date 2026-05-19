# Amendment Log — DNA-Methylation Clocks Meta-Analysis

This log records all deviations from the registered protocol (`protocol_v1.md`). Each amendment is dated, numbered, and includes rationale.

## 2026-05-18

### A1 — Drop R subprocess calls; adopt Python-only statistical stack
- **Original protocol (design spec §3):** Synthesis to use Python plus R (`meta`, `metafor`, `bayesmeta`, `netmeta`) via subprocess for DL/HKSJ pooling, Bayesian meta-analysis, and NMA.
- **Amended approach:** Python-only implementation — `statsmodels.stats.meta_analysis.combine_effects` for DL (primary) and HKSJ (`use_t=True`, sensitivity); Bayesian sensitivity via NumPy/scipy Metropolis–Hastings sampler with half-normal(0, 0.5) prior on τ; Egger's regression via `scipy.stats.linregress`; trim-and-fill implemented in-house in Python; conditional Bayesian NMA via NumPy/scipy Gibbs sampler on the consistency model.
- **Rationale:** R/Rscript is not installed on the host execution environment; the operating principle ("as feasible and robust") requires a reproducible, executable pipeline. Python implementations achieve methodologically equivalent estimates with explicit, auditable code.
- **Impact:** Statistical results are expected to be numerically equivalent to the original R-based plan within sampler tolerance. The deviation is transparent and documented in `protocol_v1.md` §3.

## 2026-05-19

### A2 — Path-C design-eligibility relaxation (RCT-only → any human prospective longitudinal study)
- **Original eligibility (protocol §1.3):** Parallel-group or crossover **RCTs only**, with a defined placebo, usual-care, attention-control, or active comparator arm, reporting pre/post DNAm-clock values (or change scores) with dispersion estimates suitable for SMD calculation.
- **Amendment:** Eligibility is widened to *any human prospective longitudinal study* — i.e., RCT (parallel-group or crossover), non-randomized intervention trial, controlled before-after, prospective exposure cohort with pre/post sampling, or single-arm pre/post intervention — reporting arm-level or group-level mean (or median + IQR) and dispersion (SD or SE) for at least one named DNAm clock at ≥2 timepoints (baseline + post; T1 + T2; pre + post; or week-X equivalents).
- **Reason:** Under strict RCT-only eligibility, the prespecified pooling gate (k ≥ 3 studies per clock) failed for every named DNAm clock — the real numeric extractable yield was **k = 0** for DunedinPACE, GrimAge, GrimAge2, PhenoAge, Horvath, Hannum, PCClock, and DNAmTL. The Path-C amendment is supported by the second-reviewer needs assessment (`docs/systematic_review_completion_status_2026-05-18.md`) and preserves the operating principle of authenticity by avoiding fabrication while widening the evidence base.
- **Consequences:**
  - **Risk-of-bias frameworks (design-stratified):** Cochrane **RoB 2** is retained for the RCT subset; **ROBINS-I** (Cochrane non-randomized intervention bias tool) is used for non-randomized intervention trials and controlled before-after designs; a custom **Newcastle-Ottawa Scale (NOS)-adapted prospective-cohort RoB framework** is used for exposure cohorts and single-arm pre/post studies.
  - **Synthesis:** Design-stratified pooled estimates are reported so the RCT-only subset signal remains separable from the broader pool. Sensitivity analyses include an RCT-only re-pool and a low-RoB-only re-pool.
  - **GRADE:** Non-randomized evidence starts at low certainty per GRADE guidance.
- **Operational principle preserved:** **No fabrication.** Any row with missing arm-level numeric data remains `not_reported`; promotion to `extracted_complete` requires unambiguous arm and timepoint labels in the source full text.

