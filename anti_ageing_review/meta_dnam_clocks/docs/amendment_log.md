# Amendment Log — DNA-Methylation Clocks Meta-Analysis

This log records all deviations from the registered protocol (`protocol_v1.md`). Each amendment is dated, numbered, and includes rationale.

## 2026-05-18

### A1 — Drop R subprocess calls; adopt Python-only statistical stack
- **Original protocol (design spec §3):** Synthesis to use Python plus R (`meta`, `metafor`, `bayesmeta`, `netmeta`) via subprocess for DL/HKSJ pooling, Bayesian meta-analysis, and NMA.
- **Amended approach:** Python-only implementation — `statsmodels.stats.meta_analysis.combine_effects` for DL (primary) and HKSJ (`use_t=True`, sensitivity); Bayesian sensitivity via NumPy/scipy Metropolis–Hastings sampler with half-normal(0, 0.5) prior on τ; Egger's regression via `scipy.stats.linregress`; trim-and-fill implemented in-house in Python; conditional Bayesian NMA via NumPy/scipy Gibbs sampler on the consistency model.
- **Rationale:** R/Rscript is not installed on the host execution environment; the operating principle ("as feasible and robust") requires a reproducible, executable pipeline. Python implementations achieve methodologically equivalent estimates with explicit, auditable code.
- **Impact:** Statistical results are expected to be numerically equivalent to the original R-based plan within sampler tolerance. The deviation is transparent and documented in `protocol_v1.md` §3.
