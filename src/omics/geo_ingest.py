"""
Phase 6 — GEO Transcriptomics Ingestion

Loads GEO soft files downloaded by src/ingest/download_geo_omics.py,
extracts sample metadata and expression matrices, applies QC filters,
and saves processed expression matrices to data_processed/omics/.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parents[2]))
from src.utils.config import get_arg_config
from src.utils.io import save_table
from src.utils.logger import get_logger, log_phase

logger = get_logger("geo_ingest")

try:
    import GEOparse
    GEO_AVAILABLE = True
except ImportError:
    GEO_AVAILABLE = False


def _qc_expression(df_expr: pd.DataFrame, variance_pct: int = 20) -> pd.DataFrame:
    """Remove low-variance genes and log2-transform if not already."""
    df = df_expr.copy()
    # Log2 transform (add 1 to handle zeros)
    if df.max().max() > 100:
        df = np.log2(df + 1)
    # Filter by variance
    gene_var = df.var(axis=1)
    threshold = gene_var.quantile(variance_pct / 100)
    df = df[gene_var > threshold]
    return df


def process_gse(accession: str, gse_dir: Path, omics_dir: Path) -> dict:
    soft_files = list(gse_dir.glob(f"{accession}*_family.soft.gz"))
    if not soft_files:
        soft_files = list(gse_dir.glob(f"{accession}*.soft*"))

    if not soft_files:
        logger.warning(f"No soft file for {accession} — skipping")
        return {"accession": accession, "status": "no_soft_file"}

    gse = GEOparse.get_GEO(filepath=str(soft_files[0]), silent=True)
    n_samples = len(gse.gsms)
    logger.info(f"{accession}: {n_samples} samples loaded")

    # Extract sample age from metadata if available
    metadata_rows = []
    for gsm_name, gsm in gse.gsms.items():
        row = {"sample_id": gsm_name}
        for key in ("age", "Sex", "gender", "disease", "tissue", "characteristics_ch1"):
            if key in gsm.metadata:
                row[key] = str(gsm.metadata[key][0])
        metadata_rows.append(row)
    meta_df = pd.DataFrame(metadata_rows)
    save_table(meta_df, omics_dir / f"{accession}_metadata.csv")

    # Pivot expression table (gene × sample)
    expr_list = []
    for gsm_name, gsm in gse.gsms.items():
        if not gsm.table.empty and "VALUE" in gsm.table.columns:
            s = gsm.table.set_index("ID_REF")["VALUE"].rename(gsm_name)
            expr_list.append(s)

    if not expr_list:
        logger.warning(f"{accession}: no expression tables found")
        return {"accession": accession, "status": "no_expression_data"}

    expr_df = pd.concat(expr_list, axis=1).apply(pd.to_numeric, errors="coerce")
    expr_qc = _qc_expression(expr_df)
    save_table(expr_qc.reset_index(), omics_dir / f"{accession}_expression_qc.parquet")
    logger.info(f"{accession}: {expr_qc.shape[0]} genes × {expr_qc.shape[1]} samples after QC")

    return {
        "accession": accession, "status": "ok",
        "n_samples": n_samples, "n_genes_after_qc": expr_qc.shape[0],
    }


def run(cfg: dict) -> dict:
    if not GEO_AVAILABLE:
        logger.warning("GEOparse not installed — omics phase skipped")
        return {"rows": 0, "columns": 0, "local_file": "skipped"}

    raw_geo: Path = cfg["paths"]["data_raw"] / "geo"
    omics_dir: Path = cfg["paths"]["data_processed"] / "omics"
    omics_dir.mkdir(parents=True, exist_ok=True)

    gse_list = cfg.get("data_sources", {}).get("geo_aging_gse", [])
    if not gse_list:
        gse_list = [{"accession": "GSE65765"}, {"accession": "GSE40279"}]

    results = []
    for entry in gse_list:
        acc = entry["accession"]
        try:
            info = process_gse(acc, raw_geo, omics_dir)
            results.append(info)
        except Exception as e:
            logger.warning(f"{acc} processing failed: {e}")
            results.append({"accession": acc, "status": f"FAILED: {e}"})

    save_table(pd.DataFrame(results), cfg["paths"]["results_tables"] / "omics_ingestion_summary.csv")
    log_phase("Phase 6a — GEO Ingest", "COMPLETE",
              f"Datasets processed: {len(results)}", log_dir=cfg["paths"]["logs"])
    return {"rows": len(results), "columns": 0, "local_file": str(omics_dir)}


if __name__ == "__main__":
    run(get_arg_config())
