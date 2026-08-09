from __future__ import annotations
import argparse, re, hashlib
import pandas as pd
from src.utils.io import load_config, save_csv, append_log

def norm_title(t):
    t = str(t or "").lower()
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()

def dedup_key(row):
    doi = str(row.get("doi","")).lower().strip()
    pmid = str(row.get("pmid","")).strip()
    if doi and doi != "nan":
        return "doi:" + doi
    if pmid and pmid != "nan":
        return "pmid:" + pmid
    return "title:" + norm_title(row.get("title",""))

def run(cfg):
    raw_path = cfg["paths"]["results_tables"] / "raw_records_all.csv"
    raw = pd.read_csv(raw_path) if raw_path.exists() else pd.DataFrame()
    if raw.empty:
        master = raw
        log = pd.DataFrame()
    else:
        raw["dedup_key"] = raw.apply(dedup_key, axis=1)
        raw["title_norm"] = raw["title"].map(norm_title)
        keep_order = {"pubmed":0, "europe_pmc":1, "crossref":2}
        raw["_source_rank"] = raw["source"].map(keep_order).fillna(9)
        raw["_abstract_len"] = raw["abstract"].fillna("").str.len()
        raw = raw.sort_values(["dedup_key","_source_rank","_abstract_len"], ascending=[True, True, False])
        master = raw.drop_duplicates("dedup_key", keep="first").drop(columns=["_source_rank","_abstract_len"])
        dup_counts = raw.groupby("dedup_key").size().reset_index(name="n_records")
        log = dup_counts[dup_counts["n_records"] > 1].merge(master[["dedup_key","title","doi","pmid"]], on="dedup_key", how="left")
    save_csv(master, cfg["paths"]["results_tables"] / "master_records_dedup.csv")
    save_csv(log, cfg["paths"]["results_tables"] / "dedup_log.csv")
    unresolved = master[master["title_norm"].duplicated(keep=False)].sort_values("title_norm") if not master.empty else master
    save_csv(unresolved, cfg["paths"]["results_tables"] / "unresolved_duplicate_report.csv")
    append_log(cfg["paths"]["logs"] / "progress.md", "Phase 3 - Deduplication and Record Hygiene",
               f"- Standardized DOI/PMID/title keys.\n- Reduced {len(raw)} raw rows to {len(master)} deduplicated records.\n- Flagged {len(log)} duplicate key groups.",
               "- results/tables/master_records_dedup.csv\n- results/tables/dedup_log.csv\n- results/tables/unresolved_duplicate_report.csv",
               "- Manual review of unresolved duplicate title variants remains pending.",
               "- Records without DOI/PMID depend on normalized title matching and may under/over-deduplicate.",
               "python src/screening/screen_records.py --config config/review_config.yaml")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/review_config.yaml")
    run(load_config(ap.parse_args().config))
