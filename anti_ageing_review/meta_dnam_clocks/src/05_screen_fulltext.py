"""Phase 4b: Stricter abstract-level eligibility screening (full-text retrieval not attempted).

Adapts the original plan: rather than fetching PDFs/XML unattended (unreliable, unverifiable),
apply a stricter eligibility checklist using title+abstract on the auto-include set.
"""
from __future__ import annotations
import argparse
import hashlib
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from _common import load_config, log, ensure_dirs, append_amendment


CLOCK_PAT = re.compile(
    r"\b(dunedinpace|grimage|phenoage|horvath|hannum|pcclock|dnamtl|"
    r"epigenetic age|epigenetic clock|dna methylation age|dnam[- ]age)\b",
    re.IGNORECASE,
)
RCT_PAT = re.compile(
    r"(randomized|randomised|\brct\b|randomly assigned|randomly allocated|"
    r"placebo[- ]controlled|double[- ]blind(ed)?|crossover trial|cross-over trial|"
    r"parallel[- ]group)",
    re.IGNORECASE,
)
HUMAN_PAT = re.compile(
    r"\b(adults?|men|women|participants|patients|subjects|humans|volunteers|"
    r"older adults|elderly|middle-aged)\b",
    re.IGNORECASE,
)
EXCLUDE_RULES = [
    ("animal", re.compile(r"(animal model|\bmice\b|\bmouse\b|\brat\b|\brats\b|zebrafish|drosophila|c\. elegans|caenorhabditis)", re.I)),
    ("in_vitro", re.compile(r"(cell line|in vitro|cultured cells|organoid)", re.I)),
    ("review", re.compile(r"(systematic review|meta[- ]analysis|narrative review|scoping review|umbrella review)", re.I)),
    ("protocol_only", re.compile(r"(study protocol|protocol for |protocol: a|study design paper)", re.I)),
    ("commentary", re.compile(r"(commentary|editorial|letter to the editor|correspondence|erratum|corrigendum|retraction)", re.I)),
    ("conference_abstract", re.compile(r"(conference abstract|\bposter\b|symposium)", re.I)),
]


def _study_id(row) -> str:
    authors = str(row.get("authors", "") or "")
    if authors:
        first = authors.split(";")[0].strip()
        if "," in first:
            surname = first.split(",")[0].strip()
        else:
            parts = first.split()
            surname = parts[-1] if parts else "Anon"
    else:
        surname = "Anon"
    surname = re.sub(r"[^A-Za-z]", "", surname) or "Anon"
    year = str(row.get("year", "") or "")[:4] or "NA"
    title = str(row.get("title", "") or "")
    if not title:
        sid = str(row.get("source_id", "") or "")
        if sid:
            return sid
    h = hashlib.md5(title.encode("utf-8")).hexdigest()[:6]
    return f"{surname}_{year}_{h}"


def eligibility(row) -> tuple[bool, str]:
    title = str(row.get("title", "") or "")
    abstract = str(row.get("abstract", "") or "")
    text = (title + " " + abstract).lower()
    if not text.strip():
        return False, "no_text_available"
    for reason, pat in EXCLUDE_RULES:
        if pat.search(text):
            return False, f"exclusion_marker:{reason}"
    if not CLOCK_PAT.search(text):
        return False, "no_clock_term_in_abstract"
    if not RCT_PAT.search(text):
        return False, "no_rct_signal_in_abstract"
    if not HUMAN_PAT.search(text):
        return False, "ambiguous_human_signal"
    return True, "eligible_pending_fulltext"


def run(cfg):
    interim = Path(cfg["paths"]["data_interim"])
    proc = Path(cfg["paths"]["data_processed"])
    ensure_dirs(proc)
    fdate = cfg["project"]["freeze_date"]
    df = pd.read_csv(interim / f"screen_ta_{fdate}.csv").fillna("")
    inc = df[df["decision"] == "include"].copy()
    log("screen_fulltext_input", auto_includes=len(inc))

    statuses = inc.apply(eligibility, axis=1)
    inc["eligibility_eligible"] = statuses.apply(lambda x: x[0])
    inc["eligibility_reason"] = statuses.apply(lambda x: x[1])
    inc["study_id"] = inc.apply(_study_id, axis=1)

    included = inc[inc["eligibility_eligible"]].copy()
    included["eligibility_status"] = "included_pending_fulltext_verification"
    excluded = inc[~inc["eligibility_eligible"]].copy()
    excluded = excluded.rename(columns={"eligibility_reason": "exclusion_reason"})

    included_path = proc / f"included_studies_{fdate}.csv"
    excluded_path = proc / f"excluded_fulltext_{fdate}.csv"
    included.drop(columns=["eligibility_eligible"]).to_csv(included_path, index=False)
    excluded.drop(columns=["eligibility_eligible"]).to_csv(excluded_path, index=False)

    log("screen_fulltext_done",
        included=int(len(included)),
        excluded=int(len(excluded)),
        included_path=str(included_path),
        excluded_path=str(excluded_path))

    if len(included) == 0:
        append_amendment(cfg["paths"]["docs"],
                         "Zero included studies after stricter abstract eligibility screen",
                         "Pivot to narrative-only synthesis if downstream extraction yields nothing")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    run(load_config(ap.parse_args().config))
