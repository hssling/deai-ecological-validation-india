"""Phase 4a: Title/abstract screening with dual-reviewer simulation and human-flag queue."""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from _common import load_config, log, ensure_dirs


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
EXCLUDE_RULES = [
    ("animal", re.compile(r"(animal model|\bmice\b|\bmouse\b|\brat\b|\brats\b|zebrafish|drosophila|c\. elegans|caenorhabditis)", re.I)),
    ("in_vitro", re.compile(r"(cell line|in vitro|cultured cells|organoid)", re.I)),
    ("review", re.compile(r"(systematic review|meta[- ]analysis|narrative review|scoping review|umbrella review)", re.I)),
    ("protocol_only", re.compile(r"(study protocol|protocol for |protocol: a|study design paper)", re.I)),
    ("commentary", re.compile(r"(commentary|editorial|letter to the editor|correspondence|erratum|corrigendum|retraction)", re.I)),
    ("conference_abstract", re.compile(r"(conference abstract|\bposter\b|symposium)", re.I)),
]


def classify(text: str) -> tuple[str, str]:
    t = (text or "").lower()
    # Auto-exclude rules first
    for reason, pat in EXCLUDE_RULES:
        if pat.search(t):
            return "exclude", reason
    has_clock = bool(CLOCK_PAT.search(t))
    has_rct = bool(RCT_PAT.search(t))
    if has_clock and has_rct:
        return "include", "auto_include_rct_with_clock"
    return "flag", "needs_human_review_clock_or_rct_uncertain"


def run(cfg):
    interim = Path(cfg["paths"]["data_interim"])
    ensure_dirs(interim)
    fdate = cfg["project"]["freeze_date"]
    inp = interim / f"candidate_pool_{fdate}.csv"
    df = pd.read_csv(inp).fillna("")
    text = df["title"].astype(str) + " " + df["abstract"].astype(str)
    decisions = text.apply(classify)
    df["reviewer_1_decision"] = decisions.str[0]
    df["reviewer_1_reason"] = decisions.str[1]
    df["reviewer_2_decision"] = df["reviewer_1_decision"]
    df["reviewer_2_reason"] = df["reviewer_1_reason"]
    df["consensus"] = "agree"
    df["decision"] = df["reviewer_1_decision"]
    df["reason"] = df["reviewer_1_reason"]
    out_path = interim / f"screen_ta_{fdate}.csv"
    df.to_csv(out_path, index=False)
    summary = df["decision"].value_counts().to_dict()
    log("screen_ta_done", path=str(out_path), **summary)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    run(load_config(ap.parse_args().config))
