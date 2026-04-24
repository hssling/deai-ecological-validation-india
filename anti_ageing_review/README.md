# Can Ageing Be Slowed or Reversed?

Autonomous systematic review, evidence grading, and mechanistic synthesis of anti-ageing and age-reversal interventions.

This repository separates:
- lifespan extension
- healthspan improvement
- slowing of biological ageing
- biomarker reversal
- true organismal rejuvenation claims

The pipeline is intentionally conservative. Metadata-assisted automation supports search, deduplication, screening, extraction, evidence scoring, mechanism mapping, NLP augmentation, figures, and manuscript drafting. Human verification is required before submission.

## Meta-analysis add-on

The repository also contains a separate quantitative add-on workflow for a later human-only meta-analysis manuscript. It is intentionally stricter than the main review and only admits studies with extractable numerical data suitable for pooling.

```bash
python -m src.meta_addon.build_addon --config config/meta_addon_config.yaml
```

This add-on builds:
- a study/source manifest
- an endpoint-priority table
- a meta-extraction queue
- a figure-digitization rescue queue
- a clean meta-analysis dataset template

## Quick start

```bash
python src/run_pipeline.py --config config/review_config.yaml
pytest tests -q
```
