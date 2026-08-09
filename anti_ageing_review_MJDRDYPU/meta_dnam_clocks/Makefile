PY=python
CFG=config/meta_config.yaml

help:
	@echo "Targets: scaffold search rescreen dedup screen extract enhanced-extract rob fulltext-audit rescue-fulltexts meta subgroup nma pubbias grade figs manuscript data-rescue test all"

scaffold:
	$(PY) src/_common.py --check --config $(CFG)
search:
	$(PY) src/01_search_dnam.py --config $(CFG)
rescreen:
	$(PY) src/02_rescreen_existing.py --config $(CFG)
dedup:
	$(PY) src/03_dedup_merge.py --config $(CFG)
screen:
	$(PY) src/04_screen_titles_abs.py --config $(CFG) && $(PY) src/05_screen_fulltext.py --config $(CFG)
extract:
	$(PY) src/06_extract_outcomes.py --config $(CFG)
enhanced-extract:
	$(PY) src/18_extract_enhanced.py --config $(CFG)
rob:
	$(PY) src/07_rob2_assess.py --config $(CFG)
fulltext-audit:
	$(PY) src/19_fulltext_eligibility_audit.py --config $(CFG)
rescue-fulltexts:
	$(PY) src/20_rescue_missing_fulltexts.py --config $(CFG)
meta:
	$(PY) src/08_meta_analysis.py --config $(CFG)
subgroup:
	$(PY) src/09_subgroup_metareg.py --config $(CFG)
nma:
	$(PY) src/10_nma.py --config $(CFG)
pubbias:
	$(PY) src/11_pubbias_sensitivity.py --config $(CFG)
grade:
	$(PY) src/12_grade_profile.py --config $(CFG)
figs:
	$(PY) src/13_figures.py --config $(CFG)
manuscript:
	$(PY) src/14_manuscript_build.py --config $(CFG)
data-rescue:
	$(PY) src/21_build_data_rescue_package.py --config $(CFG)
all: search rescreen dedup screen extract rob fulltext-audit rescue-fulltexts fulltext-audit enhanced-extract meta subgroup nma pubbias grade figs manuscript data-rescue
test:
	pytest tests/ -v
.PHONY: help scaffold search rescreen dedup screen extract enhanced-extract rob fulltext-audit rescue-fulltexts meta subgroup nma pubbias grade figs manuscript data-rescue all test
