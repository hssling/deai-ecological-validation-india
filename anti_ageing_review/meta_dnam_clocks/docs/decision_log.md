# Decision Log — DNA-Methylation Clocks Meta-Analysis

This log records material methodological and operational decisions made during the conduct of the review. Each entry is dated and attributed.

## 2026-05-18

- **Task 1 (repo scaffold) complete.** Directory tree under `anti_ageing_review/meta_dnam_clocks/` created per design spec Section 5, including `config/`, `data/{raw,interim,processed}/`, `src/`, `manuscript/`, `results/{figures,tables}/`, `submission_assets/`, `docs/`, `tests/`, plus `Makefile` and `requirements_meta_dnam.txt`.
- **Task 2 (protocol + supporting docs) complete.** `protocol_v1.md`, `prisma_2020_checklist.md`, `decision_log.md`, and `amendment_log.md` initialized under `docs/`.
- **Statistical-stack decision: Python-only.** R and Rscript are not installed on the host machine, so all R subprocess calls (`meta`, `metafor`, `bayesmeta`, `netmeta`) have been dropped. Equivalent Python implementations are specified in `protocol_v1.md` §3: DerSimonian–Laird via `statsmodels.stats.meta_analysis.combine_effects(method_re='dl')`; HKSJ via the same call with `use_t=True`; Bayesian sensitivity via a NumPy/scipy Metropolis–Hastings sampler with half-normal(0, 0.5) prior on τ; Egger's regression via `scipy.stats.linregress`; trim-and-fill implemented in-house in Python. This is logged as Amendment A1 in `amendment_log.md`.
- **Authors confirmed:** Dr Siddalingaiah H S (corresponding); Dr Chandrakala D.
- **Target journal confirmed:** *Biogerontology* (Springer; APC-free traditional subscription track).
- **Operating principle reaffirmed:** *"as feasible and robust"* — no synthetic effect-size data anywhere.
