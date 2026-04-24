"""
Download and cache GEO datasets for ageing transcriptomics.

Datasets (config.yaml: data_sources.geo_aging_gse):
  GSE65765 — whole-blood RNA-seq across ages 20–89 (Upton et al.)
  GSE40279 — DNA methylation + expression (Hannum ageing clock)
  GSE30272 — post-mortem brain cortex across lifespan (Colantuoni et al.)

GEOparse fetches soft files and expression matrices directly from NCBI FTP.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parents[2]))
from src.utils.logger import get_logger

logger = get_logger("geo_omics")

try:
    import GEOparse
    GEO_AVAILABLE = True
except ImportError:
    GEO_AVAILABLE = False
    logger.warning("GEOparse not installed — omics phase will be skipped")


def _fetch_gse(accession: str, dest_dir: Path) -> dict:
    gse = GEOparse.get_GEO(geo=accession, destdir=str(dest_dir), silent=True)
    n_samples = len(gse.gsms)
    n_genes = 0
    for gsm in list(gse.gsms.values())[:1]:
        n_genes = len(gsm.table)
    return {"accession": accession, "n_samples": n_samples, "n_genes_approx": n_genes}


def run(cfg: dict) -> dict:
    raw_dir: Path = cfg["paths"]["data_raw"] / "geo"
    raw_dir.mkdir(parents=True, exist_ok=True)

    if not GEO_AVAILABLE:
        logger.warning("Skipping GEO download — GEOparse unavailable")
        return {"rows": 0, "columns": 0, "local_file": str(raw_dir),
                "note": "GEOparse not installed"}

    gse_list = cfg.get("data_sources", {}).get("geo_aging_gse", [])
    if not gse_list:
        gse_list = [
            {"accession": "GSE65765"},
            {"accession": "GSE40279"},
        ]

    results = []
    for entry in gse_list:
        acc = entry["accession"]
        meta_file = raw_dir / f"{acc}_meta.csv"
        if meta_file.exists():
            logger.info(f"{acc} already cached — skipping")
            results.append({"accession": acc, "status": "cached"})
            continue
        try:
            info = _fetch_gse(acc, raw_dir)
            pd.DataFrame([info]).to_csv(meta_file, index=False)
            results.append({"accession": acc, "status": "downloaded", **info})
            logger.info(f"{acc}: {info['n_samples']} samples")
        except Exception as e:
            logger.warning(f"{acc} failed: {e}")
            results.append({"accession": acc, "status": f"FAILED: {e}"})

    summary = pd.DataFrame(results)
    total_rows = len(summary)
    return {"rows": total_rows, "columns": len(summary.columns),
            "local_file": str(raw_dir)}


if __name__ == "__main__":
    from src.utils.config import get_arg_config
    run(get_arg_config())
