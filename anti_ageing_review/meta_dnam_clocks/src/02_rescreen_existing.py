"""Phase 3a: Re-screen existing extracted_studies_master.csv for DNAm clock terms."""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from _common import load_config, log, ensure_dirs


def _resolve_existing(p: Path) -> Path:
    if p.is_absolute() and p.exists():
        return p
    if p.exists():
        return p
    # try project root
    root = Path("d:/Anti ageing research")
    cand = root / p
    if cand.exists():
        return cand
    return p  # caller will check existence


def run(cfg):
    ensure_dirs(cfg["paths"]["data_interim"])
    existing = _resolve_existing(Path(cfg["paths"]["existing_master"]))
    if not existing.exists():
        log("existing_master_missing", path=str(existing))
        # write empty file with header
        empty = pd.DataFrame(columns=["source","source_id","doi","pmid","title","abstract","authors","year","journal","url","fetched_at"])
        out_path = Path(cfg["paths"]["data_interim"]) / f"rescreen_existing_{cfg['project']['freeze_date']}.csv"
        empty.to_csv(out_path, index=False)
        return
    df = pd.read_csv(existing)
    terms = [re.escape(t.lower()) for t in cfg["search"]["block_clock_terms"]]
    pat = re.compile("|".join(terms), re.IGNORECASE)
    text_cols = ["title","intervention_name","outcome_exact","mechanism"]
    text = pd.Series([""] * len(df))
    for c in text_cols:
        if c in df.columns:
            text = text + " " + df[c].fillna("").astype(str)
    hit = df[text.str.contains(pat, na=False)].copy()
    out = pd.DataFrame({
        "source": "existing_master",
        "source_id": hit.get("doi", pd.Series([""]*len(hit))).fillna("").astype(str) + "|" + hit.get("pmid", pd.Series([""]*len(hit))).astype(str).fillna(""),
        "doi": hit.get("doi", pd.Series([""]*len(hit))).fillna("").astype(str),
        "pmid": hit.get("pmid", pd.Series([""]*len(hit))).astype(str).fillna(""),
        "title": hit.get("title", pd.Series([""]*len(hit))).fillna("").astype(str),
        "abstract": "",
        "authors": hit.get("authors", pd.Series([""]*len(hit))).fillna("").astype(str),
        "year": hit.get("year", pd.Series([""]*len(hit))).astype(str).fillna(""),
        "journal": hit.get("journal", pd.Series([""]*len(hit))).fillna("").astype(str),
        "url": "",
        "fetched_at": "",
    })
    out_path = Path(cfg["paths"]["data_interim"]) / f"rescreen_existing_{cfg['project']['freeze_date']}.csv"
    out.to_csv(out_path, index=False)
    log("rescreen_done", n=len(out), path=str(out_path))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    run(load_config(ap.parse_args().config))
