from __future__ import annotations
import argparse
import pandas as pd
from src.utils.io import load_config, save_csv, append_log

def status(row):
    if str(row.get("pmcid","")).strip() and str(row.get("pmcid","")).lower() != "nan":
        return "retrieved_open_metadata", "PMC full text likely available"
    if str(row.get("url","")).startswith("http"):
        return "link_available", "Full text link or landing page available"
    if row.get("is_preprint", False):
        return "preprint_only", "Preprint stream"
    return "abstract_or_metadata_only", "No full text link captured"

def run(cfg):
    s = pd.read_csv(cfg["paths"]["results_tables"] / "title_abstract_screening.csv")
    cand = s[s["screen_label"].isin(["include","uncertain"])].copy()
    vals = cand.apply(status, axis=1, result_type="expand")
    cand["retrieval_status"] = vals[0]
    cand["retrieval_note"] = vals[1]
    save_csv(cand, cfg["paths"]["results_tables"] / "full_text_status.csv")
    append_log(cfg["paths"]["logs"] / "progress.md", "Phase 5 - Full Text Retrieval and Organization",
               f"- Assigned retrieval status to {len(cand)} include/uncertain records.",
               "- results/tables/full_text_status.csv",
               "- Actual PDF/full-text download and copyright-compliant review remain pending.",
               "- Some records are metadata-only; evidence completeness is limited.",
               "python src/extraction/extract_metadata.py --config config/review_config.yaml")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/review_config.yaml")
    run(load_config(ap.parse_args().config))
