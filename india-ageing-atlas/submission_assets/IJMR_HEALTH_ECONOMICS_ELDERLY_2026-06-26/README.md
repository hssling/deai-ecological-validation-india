# IJMR submission package — Health economics of elderly care in India

Generated 2026-06-26. Target journal: **Indian Journal of Medical Research (IJMR)**, original article.

**Title:** Catastrophic health spending, impoverishment and the unpaid-care economy among older adults in India: a household health-economic analysis of LASI Wave 1, with policy microsimulation and projections to 2050

**Author:** Dr Siddalingaiah H S, Professor, Department of Community Medicine, Shridevi Institute of Medical Sciences and Research Hospital, Tumakuru, Karnataka, India (hssling@yahoo.com; ORCID 0000-0002-4771-8285).

## Files (per IJMR submission structure)

| File | Purpose |
|---|---|
| `title_page_and_cover_letter_IJMR.docx` | Title page + cover letter combined in one file (author-identifying) |
| `manuscript_IJMR.docx` | Blinded manuscript — declarations before references; tables and figure legends after references; references as sequential superscript numbers |
| `figures_IJMR.docx` | Figure document with the six main figures embedded, with legends |
| `figures/` | Figures for upload (Figure_1–6 main; Figure_S1–S2 supplementary), 600 dpi PNG |
| `figures_high_quality/` | Duplicate high-resolution copies |
| `supplementary_IJMR.docx` | Supplementary material (variable definitions, 45+ sensitivity, full State ranking, quintiles, wage sensitivity, full decomposition and two-part model, and Supplementary Figures S1–S2) |
| `STROBE_checklist_IJMR.docx` | Reporting-guidelines file (STROBE, cross-sectional) |

Markdown sources (`_*.md`) are retained alongside each DOCX.

## IJMR formatting confirmed
- References: sequential superscript numbers, no brackets, no orphan references (18/18 cited in order); every table (I–V) and figure (1–6) cited in sequence.
- Order: Title, Abstract (Background & objectives / Methods / Results / Interpretation & conclusions / Keywords), Introduction, Materials & Methods, Results, Discussion, Conclusions, Declarations (ethics, consent, data availability, author contributions, AI use, acknowledgments, financial support, conflicts of interest), References, Tables (Arabic numerals), Legends to Figures.
- Indian English; abstract ~244 content words; main text ~2000 words; 5 tables; 6 figures.

## What is new versus the MJDRDYPU version
This IJMR version adds four analytic components: a State/UT catastrophic-spending ranking (Figure 5), forward projections to 2036 and 2050 (Table V, Figure 6), a policy-scenario cost-effectiveness ranking (Table IV), and extended equity/sensitivity analyses (consumption quintiles and caregiving-wage sensitivity, Supplementary). The MJDRDYPU package is retained unchanged in its own folder.

## Headline findings
- 20.7% of older households face catastrophic spending (>40% of capacity to pay); out-of-pocket payments impoverish an extra 5.8%.
- Rural residence is the strongest driver; burden is highest in Bihar, J&K, West Bengal, UP and Kerala.
- Inpatient cover removes 2.0 pp of catastrophic spending; outpatient and medicine cover removes 17.8 pp and is the most cost-effective lever.
- Unpaid family care is worth ~Rs 1.3 lakh crore/year; the catastrophic-spending caseload is projected to reach 72 million by 2050.

## Reproducibility
Tables and figures are produced by `scripts/run_health_economics_mjdrdypu.py`, `scripts/run_health_economics_ijmr_extras.py` and `scripts/make_health_economics_ijmr_figures.py`, using `src/health_economics.py` (unit-tested in `tests/test_health_economics.py`).

## Before submission (human checks)
- Insert the submission date in the cover letter.
- Confirm IJMR's current word limits, reference-style details, figure-format and file-upload requirements.
