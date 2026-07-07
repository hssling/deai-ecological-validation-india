# PRISm / LASI — Lung India revision (v2) design

**Date:** 2026-07-08
**Author:** Dr Siddalingaiah H S (single author)
**Status:** Approved design → implementation

## Context

The PRISm/RSP LASI Wave 1 manuscript was **rejected by Lung India**; a reformatted
version was submitted to MJDRDYPU (2026-07-06, under review). Reviewer comments from
Lung India arrived 2026-07-08. This project builds a **robustly revised v2 package**,
Lung-India–formatted, in a **new folder** that does not disturb any existing
MJDRDYPU / original-submission assets. Purpose: a defensible manuscript held in reserve
for resubmission (Lung India appeal or another respiratory journal) and to feed
improvements back if MJDRDYPU returns a revision.

Original manuscript: `india-ageing-atlas/prism_lasi_2026/LungIndia_submission/07_blinded_manuscript.md`
Reviewer comments: `.../LungIndia_submission/Comments on the manuscript.docx`

## Reviewer objections (14) and disposition

| # | Objection | Disposition |
|---|---|---|
| 1 | Sampling methodology not described; spirometry subset representativeness unshown | Describe LASI multistage stratified sampling in Methods |
| 2 | No included-vs-excluded comparison (selection bias) | **New table**: excluded-on-acceptability vs analytic, standardized differences |
| 3 | Spirometry methods inadequate (device, ATS/ERS, calibration, QA, central review) | Expand Methods per published LASI protocol; transparent about what is/isn't recoverable |
| 4 | Handheld spirometer QC / curve review concerns | State QC grading (`acceptable`/`repeatable`), acknowledge handheld limitation |
| 5 | GLI-2012 not justified for India; equation module unspecified | **Identify the module used**; justify; add reference-equation comparison (see below) |
| 6 | Internal inconsistency: acknowledges reference bias yet bases conclusions on it | **Resolved by dual thesis** + co-primary defs + multi-reference comparison |
| 7 | Fixed cut-offs primary despite GLI LLN available | **Co-primary fixed + LLN** throughout |
| 8 | Heterogeneous community sample, not disease-specific | Framing caveat in Discussion/limitations |
| 9 | Pre-BD only → obstruction ≠ COPD | Strengthen existing limitation (honest; LASI has no post-BD) |
| 10 | Associations confirmatory not novel | Concede; reposition novelty = first national Indian spirometry-based estimate + reference-equation demonstration |
| 11 | Figures duplicate tables; flow/QC/grades missing | Add flow + QC figures; cut OR bar charts |
| 12 | Overinterpretation of "hidden national burden" | Temper; drop bare ~50M extrapolation |
| 13 | Repetition in intro/discussion | Tighten |

Honest non-negotiable: post-bronchodilator data do not exist in LASI → remains a stated limitation.

## Scientifically-sound decisions (author judgment)

1. **Co-primary definitions** (fixed + GLI-LLN), reported side by side. Discussion notes LLN is
   physiologically preferable while fixed enables literature comparability.
2. **LLN computed from `_lln` columns**, not the `fev1_z` column, which is **dead (all zeros)** in the
   linked file and must not be used. `fvc_z` is valid. State this data-quality finding.
3. **Included-vs-excluded** reported with **standardized mean differences**, not p-values (uninformative at n≈50k).
4. **Weighted CIs** via Kish effective N (Wilson) — PSU/STRATA unavailable in the analytic file → documented
   approximation, stated as a limitation.
5. **Reference-equation comparison** (measurement thesis centrepiece), three references ranked by defensibility:
   - (a) GLI-2012 as applied — module identified by back-checking predicted vs observed given height/age/sex.
   - (b) Internal population-derived reference — LLN from the healthy LASI subset (never-smoker, no self-reported
     lung disease, BMI 18.5–24.9). Fully self-contained/reproducible.
   - (c) Published India-specific equation (e.g., Chhabra North India) — **only if exact coefficients verified**;
     never fabricated. If unverifiable, drop and cite qualitatively.
6. No fabrication of device make/model/calibration specifics not in the LASI record.

## Deliverables (new folder `prism_lasi_2026/LungIndia_revised_2026-07-08/`)

Nothing outside this folder is modified except this spec and the new analysis script(s)
(which are additive, new filenames).

### Analysis
- `analysis/08_prism_revision.py` — reads `data/processed/biomarker_integrated_analysis_dataset.csv`
  (+ links `bm067` height from `data/raw/.../lasi_w1b_ind_bm.dta` by `prim_key`). Emits:
  - STROBE participant-flow counts (raw → age≥45 → attempted → acceptable → plausible → analytic, with reasons)
  - Included-vs-excluded comparison (age, sex, frailty, functional limitation, multimorbidity, comorbidity; std diffs)
  - Co-primary prevalence (fixed + LLN) overall + by sex/age/residence
  - Multi-reference prevalence comparison (GLI vs internal vs Indian-if-verified)
  - GLI module identification note
  - Determinants + ageing associations, robustness across definitions
  - `outputs/` tables + `outputs/key_numbers_v2.json`

### Figures (new set)
- F1 STROBE participant flow (new) · F2 QC/quality-grade panel (new)
- F3 FVC z-distribution vs GLI (kept) · F4 reference-comparison prevalence (new, dual-thesis centrepiece)
- Cut: OR bar charts (restate Tables 3–4)

### Manuscript + package (Lung India format: structured abstract ≤250 w, Vancouver, STROBE, Original Article)
- `00_response_to_reviewers.md` (point-by-point, quotes each comment)
- `01_title_page.md` · `02_cover_letter.md` · `03_blinded_manuscript.md`
- `04_STROBE_checklist.md` · `05_declarations.md`
- `06_supplementary.md` (fixed-vs-LLN, incl-vs-excl, reference comparison, GLI note, data-quality note)
- `07_suggested_reviewers.md` · `figures/`

## Success criteria
- Every one of the 13 reviewer objections has a concrete, located change in the response document.
- Every numeric claim in the manuscript traces to a regenerated output file.
- No existing MJDRDYPU / original-submission file altered.
- Reference-equation comparison present and honest about method provenance.
