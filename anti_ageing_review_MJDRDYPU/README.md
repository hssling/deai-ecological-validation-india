# Anti-ageing evidence map: reproducibility package

This folder is a self-contained package for:

> Can Ageing Be Slowed or Reversed? A Reproducible Evidence Map and Credibility Ranking of Anti-Ageing and Age-Reversal Interventions

Manuscript: `mjdrdypu_451_26` (Revision R1)  
Journal: Medical Journal of Dr. D.Y. Patil Vidyapeeth (MJDRDYPU)  
Package status: source and reproducibility archive; the publisher proof remains a separate proof-stage artifact.

This package is also the long-term working archive for the project. It includes
the complete analysis tree used to develop the evidence map, not only the files
submitted to the journal. New evidence can be added through dated search runs,
screening decisions, extraction tables, and versioned manuscript/submission
folders without changing the historical revision archive.

## What is included

- `make_figures.py`: deterministic generation of Figures 1–4 from the intervention-ranking CSV.
- `tables/`: analysis inputs and exported evidence-map tables, including verification, risk-of-bias, effect-extraction, duplicate-check, ranking, and quality-control data.
- `figures/`: generated main figures.
- `media/`: embedded supplementary-figure assets used by the supplementary document.
- `_manuscript_R1.md` and `_manuscript_R1_marked.md`: manuscript source and marked source.
- `MJDRDYPU_AntiAgeing_*`: retained submission documents, title page, declarations, response, checklist, PRISMA checklist, reference audit, summary of changes, figures, and supplementary material.
- `mjdrdypu_451_26_R3.pdf`: publisher author proof retained for reference; it is not treated as the reproducibility source.
- `proof_review/`: annotated proof PDF and the DOCX correction/confirmation record prepared for the publisher upload.
- `config/`: search, review, source-registry, and meta-analysis configuration.
- `data_raw/` and `data_processed/`: reproducibility snapshots and derived working data; intentionally excluded full-text caches are documented in `DATA_AVAILABILITY.md`.
- `docs/`: protocol, eligibility rules, extraction manual, evidence framework, decision logs, and project briefs.
- `src/`: modular search, deduplication, screening, retrieval, extraction, grading, mechanism, NLP, synthesis, visualization, and submission code.
- `results/` and `metadata/`: audit logs, analysis tables, supplementary workbooks, and extraction dictionary.
- `meta_dnam_clocks/` and `meta_frailty_lmic/`: separately scoped quantitative add-ons with their own source, data, scripts, tests, and documentation.
- `tests/`, `Makefile`, and `environment.yml`: automated checks and environment/run targets.

The existing repository projects are preserved. This article is intentionally stored
under its own folder so it does not overwrite the DEAI ecological-validation project.

## Reproduce the main figures

From this folder, create a clean Python environment and install the package requirements:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python make_figures.py
python scripts/validate_package.py
```

To run the broader project pipeline from this folder:

```powershell
conda env create -f environment.yml
conda activate anti-ageing-review
python src/run_pipeline.py --config config/review_config.yaml
pytest tests -q
```

The pipeline may query external bibliographic services and therefore can produce
new records as databases change. For an offline check of the released snapshot,
run `python make_figures.py`, `python scripts/validate_package.py`, and
`pytest tests -q` without rerunning network retrieval.

The figure script reads `tables/intervention_credibility_ranking.csv` as its single
source of truth and writes the four PNGs to `figures/`. Existing figures are
overwritten only when the script is deliberately run.

## Data and interpretation boundaries

The package contains bibliographic metadata, screening/verification exports, and
derived evidence-map tables. It does not contain redistributed publisher-licensed
full-text cache files. The study is a narrative evidence map and credibility-ranking
exercise; the heterogeneous extracted estimates are not a pooled meta-analysis.
The ranking is not a treatment recommendation, and biomarker changes are not evidence
of human rejuvenation.

Some supplementary tables retain analysis-oriented fields because they document the
workflow. These fields must be read with the table notes and should not be presented
as independently adjudicated clinical evidence.

## Proof-stage correction notes

The author proof contains two unresolved author queries and several production-stage
items. See `PROOF_CORRECTIONS.md` for the confirmation/correction list. In particular,
the proof currently points to the repository root; the article-specific reproducibility
link is now live at:

`https://github.com/hssling/deai-ecological-validation-india/tree/main/anti_ageing_review_MJDRDYPU`

The initial proof-review package was committed in `28153a7`; the full project
expansion described here is recorded in the latest repository commit.

## Repository naming note

The complete package is maintained in the `anti_ageing_review_MJDRDYPU` folder.
The article's data-availability statement intentionally continues to use the
repository root address; the folder name is only a navigation aid within the
repository.

## Reproducibility limitations

The workflow is deliberately scoped to the included metadata and exported tables.
Search-platform responses, publisher access, and some full-text retrieval results may
change over time. The included exports therefore provide the auditable snapshot used
for the revision rather than a guarantee of identical future database retrieval.

See [`METHODS.md`](./METHODS.md) for the end-to-end methodological record,
[`DATA_DICTIONARY.md`](./DATA_DICTIONARY.md) for the main data products, and
[`DATA_AVAILABILITY.md`](./DATA_AVAILABILITY.md) for provenance and redistribution
boundaries.
