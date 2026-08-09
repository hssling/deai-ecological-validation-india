"""Phase 5b: Seed RoB 2 worksheet for dual-coded manual completion."""
from __future__ import annotations
import argparse
import csv
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from _common import load_config, log, ensure_dirs


COLS = [
    "study_id", "first_author", "year", "doi", "pmid",
    "d1_randomization", "d1_quote",
    "d2_deviations", "d2_quote",
    "d3_missing_data", "d3_quote",
    "d4_measurement", "d4_quote",
    "d5_selective_reporting", "d5_quote",
    "overall",
    "reviewer_1", "reviewer_2",
    "consensus_status",
    "notes",
]


def _first_author(authors: str) -> str:
    if not authors: return "Anon"
    head = str(authors).split(";")[0].strip()
    if "," in head: return head.split(",")[0].strip()
    parts = head.split()
    return parts[-1] if parts else "Anon"


def run(cfg):
    proc = Path(cfg["paths"]["data_processed"])
    ensure_dirs(proc)
    fdate = cfg["project"]["freeze_date"]
    inc = pd.read_csv(proc / f"included_studies_{fdate}.csv").fillna("")
    # Deduplicate by study_id since the extraction worksheet has multiple rows per study
    inc = inc.drop_duplicates(subset=["study_id"]).reset_index(drop=True)
    rows = []
    for _, r in inc.iterrows():
        row = {c: "" for c in COLS}
        row["study_id"] = r["study_id"]
        row["first_author"] = _first_author(str(r.get("authors", "")))
        row["year"] = str(r.get("year", ""))[:4]
        row["doi"] = r.get("doi", "")
        row["pmid"] = r.get("pmid", "")
        for d in ["d1_randomization","d2_deviations","d3_missing_data","d4_measurement","d5_selective_reporting","overall"]:
            row[d] = "pending"
        row["reviewer_1"] = "Dr Siddalingaiah H S"
        row["reviewer_2"] = "Dr Chandrakala D"
        row["consensus_status"] = "pending"
        row["notes"] = "Auto-seeded; dual coding pending full-text reading."
        rows.append(row)
    out_path = proc / f"rob2_assessments_{fdate}.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        for row in rows:
            w.writerow(row)
    log("rob2_seeded", n=len(rows), path=str(out_path))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    run(load_config(ap.parse_args().config))
