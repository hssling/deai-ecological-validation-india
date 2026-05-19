# Decision Log â€” DNA-Methylation Clocks Meta-Analysis

This log records material methodological and operational decisions made during the conduct of the review. Each entry is dated and attributed.

## 2026-05-18

- **Task 1 (repo scaffold) complete.** Directory tree under `anti_ageing_review/meta_dnam_clocks/` created per design spec Section 5, including `config/`, `data/{raw,interim,processed}/`, `src/`, `manuscript/`, `results/{figures,tables}/`, `submission_assets/`, `docs/`, `tests/`, plus `Makefile` and `requirements_meta_dnam.txt`.
- **Task 2 (protocol + supporting docs) complete.** `protocol_v1.md`, `prisma_2020_checklist.md`, `decision_log.md`, and `amendment_log.md` initialized under `docs/`.
- **Statistical-stack decision: Python-only.** R and Rscript are not installed on the host machine, so all R subprocess calls (`meta`, `metafor`, `bayesmeta`, `netmeta`) have been dropped. Equivalent Python implementations are specified in `protocol_v1.md` Â§3: DerSimonianâ€“Laird via `statsmodels.stats.meta_analysis.combine_effects(method_re='dl')`; HKSJ via the same call with `use_t=True`; Bayesian sensitivity via a NumPy/scipy Metropolisâ€“Hastings sampler with half-normal(0, 0.5) prior on Ï„; Egger's regression via `scipy.stats.linregress`; trim-and-fill implemented in-house in Python. This is logged as Amendment A1 in `amendment_log.md`.
- **Authors confirmed:** Dr Siddalingaiah H S (corresponding); Dr Chandrakala D.
- **Target journal updated:** *Indian Journal of Medical Research* as the provisional Indian journal target; final submission remains conditional on data rescue and second-reviewer verification.
- **Operating principle reaffirmed:** *"as feasible and robust"* â€” no synthetic effect-size data anywhere.
- **Hard-stop synthesis gate completed.** Decision: do not submit as a meta-analysis yet. Only one candidate effect-size row was calculable from real extracted data, and no named DNAm clock met the prespecified minimum of three real effect estimates.
- **Downstream analyses gated off.** NMA, publication-bias tests, subgroup/meta-regression and GRADE were not run because thresholds were not met.
- **Accessible full-text audit completed.** The accessible full-text audit supersedes abstract-only inclusion labels for current interpretation.

## 2026-05-19 — Internal peer reviews + validity audit + selective revisions

- **Three internal review documents written** in `submission_assets/IJMR_DNAm_clocks_path_c_2026-05-18/`:
  - `internal_peer_review_1_methodologist_2026-05-18.docx` (verdict: major revisions)
  - `internal_peer_review_2_clinician_2026-05-18.docx` (verdict: minor revisions)
  - `content_structure_validity_audit_2026-05-18.docx` (verdict: accept methodologically; pending RoB 2 dual coding)
- **Three selective revisions applied to `manuscript/manuscript_main.md`** in response to the most consequential review feedback:
  1. **Abstract conclusion expanded** to communicate BOTH the null central estimate AND the wide-PI-no-clinical-decision message, plus the "exploratory pharmacodynamic marker, not decision-grade endpoint" framing (per clinician review C1, C2).
  2. **Methods § Quantitative synthesis** now states explicitly that GIV pooling here is descriptive across heterogeneous adjustment sets, not an estimate of a single common causal effect (per methodologist M2 / R1).
  3. **Results § Flow** now states explicitly that extraction yield, not search yield, is the binding constraint, with the k=3 DunedinPACE figure cited in-line (per methodologist R5).
- **Manuscript bundle rebuilt.** Main manuscript body word count: 3051 words. Bundle commit-ready.
- **Outstanding commitment:** dual RoB 2 coding must be completed and posted in supplementary materials before journal acceptance response is filed.
