"""Phase 5a: Seed extraction worksheet (numeric outcomes left blank for manual completion)."""
from __future__ import annotations
import argparse
import csv
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from _common import load_config, log, ensure_dirs


CLASS_PATTERNS = [
    ("caloric_restriction", re.compile(r"(caloric restriction|calorie restriction|fasting|time[- ]restricted)", re.I)),
    ("exercise", re.compile(r"(\bexercise\b|\btraining\b|aerobic|resistance|physical activity)", re.I)),
    ("pharmacological", re.compile(r"(metformin|rapamycin|sirolimus|senolytic|dasatinib|quercetin|fisetin|glp-?1)", re.I)),
    ("supplement", re.compile(r"(supplement|omega[- ]3|vitamin|polyphenol|resveratrol|nicotinamide|\bnad\b)", re.I)),
    ("multimodal_lifestyle", re.compile(r"(lifestyle|multimodal|intervention bundle|diet and exercise)", re.I)),
    ("mind_body", re.compile(r"(meditation|mindfulness|yoga|tai chi)", re.I)),
]

def classify_intervention(text: str) -> str:
    t = (text or "").lower()
    for cls, pat in CLASS_PATTERNS:
        if pat.search(t):
            return cls
    return "other"

def detect_comparator(text: str) -> str:
    t = (text or "").lower()
    if "placebo" in t: return "placebo"
    if "usual care" in t: return "usual_care"
    if "attention control" in t: return "attention_control"
    if "active comparator" in t: return "active_comparator"
    if "wait-list" in t or "waitlist" in t: return "wait_list"
    return "RCT_comparator_unspecified"

def detect_design(text: str) -> str:
    t = (text or "").lower()
    if "crossover" in t or "cross-over" in t: return "crossover"
    if "parallel" in t: return "parallel_group_RCT"
    return "RCT"

def first_author(authors: str) -> str:
    if not authors: return "Anon"
    head = authors.split(";")[0].strip()
    if "," in head:
        return head.split(",")[0].strip()
    parts = head.split()
    return parts[-1] if parts else "Anon"


def run(cfg):
    proc = Path(cfg["paths"]["data_processed"])
    ensure_dirs(proc)
    fdate = cfg["project"]["freeze_date"]
    df = pd.read_csv(proc / f"included_studies_{fdate}.csv").fillna("")
    clocks_cfg = cfg["clocks"]
    clock_patterns = {c: re.compile(re.escape(c).replace(r"\ ", r"\s*"), re.I) for c in clocks_cfg}
    # Also accept the long-form expressions
    extra = {"EpigeneticAgeGeneric": re.compile(r"(epigenetic age|epigenetic clock|dna methylation age|dnam[- ]age)", re.I)}
    out_rows = []
    for _, row in df.iterrows():
        text = str(row.get("title", "")) + " " + str(row.get("abstract", ""))
        cls = classify_intervention(text)
        comp = detect_comparator(text)
        des = detect_design(text)
        matched_clocks = [c for c, p in clock_patterns.items() if p.search(text)]
        if not matched_clocks:
            if extra["EpigeneticAgeGeneric"].search(text):
                matched_clocks = ["UNSPECIFIED_EPIGENETIC_AGE"]
            else:
                matched_clocks = ["UNSPECIFIED_FROM_ABSTRACT"]
        base = {
            "study_id": row["study_id"],
            "first_author": first_author(str(row.get("authors",""))),
            "year": str(row.get("year",""))[:4],
            "journal": row.get("journal",""),
            "doi": row.get("doi",""),
            "pmid": row.get("pmid",""),
            "design": des,
            "n_int": "", "n_ctrl": "", "age_mean": "", "age_sd": "", "sex_female_pct": "",
            "health_status": "",
            "intervention_class": cls,
            "intervention_detail": "",
            "dose": "", "duration_weeks": "",
            "comparator": comp,
            "baseline_int_mean": "", "baseline_int_sd": "",
            "post_int_mean": "", "post_int_sd": "",
            "baseline_ctrl_mean": "", "baseline_ctrl_sd": "",
            "post_ctrl_mean": "", "post_ctrl_sd": "",
            "change_int_mean": "", "change_int_sd": "",
            "change_ctrl_mean": "", "change_ctrl_sd": "",
            "array_platform": "",
            "follow_up_weeks": "",
            "funding_source": "", "coi_disclosure": "",
            "extraction_status": "not_reported",
            "notes": "Auto-seeded from abstract; numeric outcomes pending manual extraction from full text.",
        }
        for clk in matched_clocks:
            r = dict(base); r["clock"] = clk
            out_rows.append(r)
    cols = ["study_id","first_author","year","journal","doi","pmid","design","n_int","n_ctrl","age_mean","age_sd","sex_female_pct","health_status","intervention_class","intervention_detail","dose","duration_weeks","comparator","clock","baseline_int_mean","baseline_int_sd","post_int_mean","post_int_sd","baseline_ctrl_mean","baseline_ctrl_sd","post_ctrl_mean","post_ctrl_sd","change_int_mean","change_int_sd","change_ctrl_mean","change_ctrl_sd","array_platform","follow_up_weeks","funding_source","coi_disclosure","extraction_status","notes"]
    out_path = proc / f"extracted_clock_studies_{fdate}.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for r in out_rows: w.writerow({k: r.get(k, "") for k in cols})
    log("extraction_seeded", n_rows=len(out_rows), n_studies=len(df), path=str(out_path))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    run(load_config(ap.parse_args().config))
