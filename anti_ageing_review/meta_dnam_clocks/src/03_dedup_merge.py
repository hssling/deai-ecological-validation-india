"""Phase 3b: Dedup + merge raw + rescreen-existing pools."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

import pandas as pd
from rapidfuzz import fuzz

sys.path.insert(0, str(Path(__file__).parent))
from _common import load_config, log, ensure_dirs


def dedup(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy().fillna("")
    df["_doi_n"] = df["doi"].astype(str).str.lower().str.strip()
    df["_pmid_n"] = df["pmid"].astype(str).str.strip()
    keep = []
    seen_doi = set()
    seen_pmid = set()
    seen_titles = []  # list of (normalized_title, year_str)
    for _, row in df.iterrows():
        doi_n = row["_doi_n"]
        pmid_n = row["_pmid_n"]
        if doi_n and doi_n in seen_doi:
            continue
        if pmid_n and pmid_n in seen_pmid:
            continue
        title_n = str(row.get("title", "")).lower().strip().rstrip(".")
        y = str(row.get("year", ""))[:4]
        y_int = int(y) if y.isdigit() else 0
        dup = False
        for tt, yy in seen_titles:
            yy_int = int(yy) if yy.isdigit() else 0
            if abs(y_int - yy_int) <= 1 and fuzz.token_sort_ratio(title_n, tt) >= 92:
                dup = True
                break
        if dup:
            continue
        if doi_n:
            seen_doi.add(doi_n)
        if pmid_n:
            seen_pmid.add(pmid_n)
        seen_titles.append((title_n, y))
        keep.append(row)
    out = pd.DataFrame(keep)
    return out.drop(columns=["_doi_n", "_pmid_n"], errors="ignore")


def run(cfg):
    interim = Path(cfg["paths"]["data_interim"])
    ensure_dirs(interim)
    fdate = cfg["project"]["freeze_date"]
    a_path = interim / f"raw_records_dnam_{fdate}.csv"
    b_path = interim / f"rescreen_existing_{fdate}.csv"
    a = pd.read_csv(a_path) if a_path.exists() else pd.DataFrame()
    b = pd.read_csv(b_path) if b_path.exists() else pd.DataFrame()
    merged = pd.concat([a, b], ignore_index=True)
    before = len(merged)
    out = dedup(merged)
    out_path = interim / f"candidate_pool_{fdate}.csv"
    out.to_csv(out_path, index=False)
    log("dedup_done", before=before, after=len(out), path=str(out_path))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    run(load_config(ap.parse_args().config))
