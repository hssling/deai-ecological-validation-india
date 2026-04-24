"""
Phase 2 orchestrator — runs all ingestion scripts and produces
results/tables/data_source_summary.csv.

Usage:
    python src/ingest/ingest_all.py --config config.yaml
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2]))

import pandas as pd

from src.utils.config import get_arg_config
from src.utils.logger import get_logger, log_phase
from src.ingest import (
    download_who_aaq,
    download_nfhs5,
    download_lancet_countdown,
    download_geo_omics,
    build_synthetic_cohort,
)

logger = get_logger("ingest_all")


def run(cfg: dict) -> None:
    results = []

    steps = [
        ("WHO Ambient Air Quality DB", download_who_aaq.run),
        ("NFHS-5 District Factsheets", download_nfhs5.run),
        ("Lancet Countdown Indicators", download_lancet_countdown.run),
        ("GEO Aging Transcriptomics", download_geo_omics.run),
        ("Synthetic Cohort (fallback)", build_synthetic_cohort.run),
    ]

    for name, fn in steps:
        logger.info(f"Starting: {name}")
        try:
            info = fn(cfg)
            results.append({"dataset": name, "status": "OK", **info})
            logger.info(f"  OK — {info}")
        except Exception as exc:
            logger.warning(f"  FAILED: {exc}")
            results.append({"dataset": name, "status": f"FAILED: {exc}",
                            "rows": 0, "columns": 0, "local_file": ""})

    summary = pd.DataFrame(results)
    out = cfg["paths"]["results_tables"] / "data_source_summary.csv"
    summary.to_csv(out, index=False)
    logger.info(f"Summary saved → {out}")

    log_phase(
        "Phase 2 — Data Ingestion", "COMPLETE",
        f"Datasets attempted: {len(steps)}\n"
        f"Successful: {(summary.status == 'OK').sum()}\n"
        f"Failed/fallback: {(summary.status != 'OK').sum()}",
        log_dir=cfg["paths"]["logs"],
    )


if __name__ == "__main__":
    cfg = get_arg_config()
    run(cfg)
