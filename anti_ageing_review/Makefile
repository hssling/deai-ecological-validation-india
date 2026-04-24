PYTHON=python
CONFIG=config/review_config.yaml

.PHONY: all search dedup screen retrieve extract grade mechanisms nlp synth figures manuscript fulltext verify mjdrdypu qc meta-addon meta-seed meta-pool meta-fmd-reconstruct test

all:
	$(PYTHON) -m src.run_pipeline --config $(CONFIG)

search:
	$(PYTHON) -m src.search.run_search --config $(CONFIG)

dedup:
	$(PYTHON) -m src.dedup.deduplicate --config $(CONFIG)

screen:
	$(PYTHON) -m src.screening.screen_records --config $(CONFIG)

retrieve:
	$(PYTHON) -m src.retrieval.assess_full_text --config $(CONFIG)

fulltext:
	$(PYTHON) -m src.screening.full_text_triage --config $(CONFIG)

verify:
	$(PYTHON) -m src.retrieval.verify_full_text --config $(CONFIG)

extract:
	$(PYTHON) -m src.extraction.extract_metadata --config $(CONFIG)

grade:
	$(PYTHON) -m src.grading.score_evidence --config $(CONFIG)

mechanisms:
	$(PYTHON) -m src.mechanisms.map_mechanisms --config $(CONFIG)

nlp:
	$(PYTHON) -m src.nlp.topic_hype --config $(CONFIG)

synth:
	$(PYTHON) -m src.meta_analysis.synthesize --config $(CONFIG)

figures:
	$(PYTHON) -m src.viz.make_figures --config $(CONFIG)

manuscript:
	$(PYTHON) -m src.write_manuscript --config $(CONFIG)

mjdrdypu:
	$(PYTHON) -m src.submission.prepare_mjdrdypu_submission --config $(CONFIG)

qc:
	$(PYTHON) -m src.utils.quality_checks --config $(CONFIG)

meta-addon:
	$(PYTHON) -m src.meta_addon.build_addon --config config/meta_addon_config.yaml

meta-seed:
	$(PYTHON) -m src.meta_addon.seed_numeric_extractions --config config/meta_addon_config.yaml

meta-pool:
	$(PYTHON) -m src.meta_addon.pool_same_outcome --config config/meta_addon_config.yaml

meta-fmd-reconstruct:
	$(PYTHON) -m src.meta_addon.reconstruct_fmd_bioage --config config/meta_addon_config.yaml

test:
	pytest tests -q
