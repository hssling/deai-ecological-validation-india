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
