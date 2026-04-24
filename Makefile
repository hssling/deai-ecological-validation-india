# =============================================================================
# DEAI Pipeline — Makefile
# =============================================================================
# Usage:
#   make setup        — create conda environment
#   make phase1       — scaffold only (already done)
#   make phase2       — data ingestion
#   make phase3       — feature engineering
#   make phase4       — DEAI construction
#   make phase5       — model training and evaluation
#   make phase6       — omics integration
#   make phase7       — explainability
#   make phase8       — statistical rigor
#   make phase9       — manuscript generation
#   make phase10      — dissemination materials
#   make all          — run phases 2–10 sequentially
#   make test         — run pytest
#   make lint         — black + isort check
#   make clean        — remove generated artefacts (not raw data)

PYTHON = python
PYTEST = pytest
CONFIG = config.yaml

.PHONY: setup phase2 phase3 phase4 phase4b robustness phase5 phase6 phase7 phase8 phase9 phase10 all test lint clean

setup:
	conda env create -f environment.yml
	@echo "Activate with: conda activate deai"

phase2:
	$(PYTHON) src/ingest/ingest_all.py --config $(CONFIG)
	@echo "Phase 2 complete — check logs/progress.md"

phase3:
	$(PYTHON) src/features/build_features.py --config $(CONFIG)
	@echo "Phase 3 complete"

phase4:
	$(PYTHON) src/models/deai_build.py --config $(CONFIG)
	@echo "Phase 4 complete"

phase4b:
	$(PYTHON) src/models/deai_real.py --config $(CONFIG)
	$(PYTHON) src/stats/real_data_robustness.py --config $(CONFIG)
	@echo "Phase 4b real-data DEAI + robustness complete"

robustness:
	$(PYTHON) src/stats/real_data_robustness.py --config $(CONFIG)
	@echo "Real-data robustness complete"

phase5:
	$(PYTHON) src/models/train_models.py --config $(CONFIG)
	$(PYTHON) src/stats/sensitivity_analysis.py --config $(CONFIG)
	@echo "Phase 5 complete"

phase6:
	$(PYTHON) src/omics/geo_ingest.py --config $(CONFIG)
	$(PYTHON) src/omics/dge_analysis.py --config $(CONFIG)
	$(PYTHON) src/omics/pathway_scoring.py --config $(CONFIG)
	@echo "Phase 6 complete"

phase7:
	$(PYTHON) src/models/explain.py --config $(CONFIG)
	@echo "Phase 7 complete"

phase8:
	$(PYTHON) src/stats/dag_analysis.py --config $(CONFIG)
	@echo "Phase 8 complete"

phase9:
	$(PYTHON) src/utils/build_manuscript.py --config $(CONFIG)
	@echo "Phase 9 complete"

phase10:
	@echo "Phase 10 — dissemination materials ready in docs/"

all: phase2 phase3 phase4 phase5 phase6 phase7 phase8 phase9 phase10
	@echo "Full pipeline complete."

test:
	$(PYTEST) tests/ -v --cov=src --cov-report=term-missing

lint:
	black --check src/ tests/
	isort --check-only src/ tests/

clean:
	rm -rf data_processed/*.parquet data_processed/*.csv
	rm -rf results/figures/*.png results/tables/*.csv
	find . -type d -name __pycache__ -exec rm -rf {} +
	@echo "Clean complete (raw data preserved)"
