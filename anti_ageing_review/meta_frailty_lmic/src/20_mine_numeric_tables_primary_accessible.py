from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_FULLTEXT = ROOT / "data" / "raw" / "pmc_fulltext"
TABLES = ROOT / "results" / "tables"


OUTCOME_PATTERNS = {
    "frailty_status_or_score": r"frailty|frail|prefrail|pre-frail|clinical frailty|fried|share-fi|tilburg",
    "gait_speed": r"gait speed|walking speed|walk speed|m/s",
    "sppb": r"short physical performance battery|\bsppb\b",
    "grip_strength": r"grip strength|handgrip|hand grip",
    "adl_iadl": r"activities of daily living|\badl\b|\biadl\b|barthel|lawton",
    "falls": r"\bfalls?\b|fall rate|fall-related",
    "quality_of_life": r"quality of life|qol|eq-5d|sf-36|sf36",
    "adherence": r"adherence|attendance|compliance|sessions attended",
    "adverse_events": r"adverse event|serious adverse|safety|injur",
}


def text_of(elem: ET.Element | None) -> str:
    if elem is None:
        return ""
    return re.sub(r"\s+", " ", " ".join(elem.itertext())).strip()


def norm(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def find_numeric_context(text: str, pattern: str, width: int = 900) -> str:
    match = re.search(pattern, text, flags=re.I)
    if not match:
        return ""
    start = max(0, match.start() - width)
    end = min(len(text), match.end() + width)
    return text[start:end]


def has_arm_signal(text: str) -> str:
    return "yes" if re.search(r"intervention|control|usual care|placebo|exercise|nutrition|group|arm", text, flags=re.I) else "no"


def numeric_density(text: str) -> int:
    return len(re.findall(r"[-+]?\d+(?:\.\d+)?(?:\s*\([^)]+\))?", text))


def mine_tables(pmcid: str) -> list[dict[str, str | int]]:
    path = RAW_FULLTEXT / f"{pmcid}.xml"
    if not path.exists():
        return []
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError:
        return []
    rows = []
    for idx, table in enumerate(root.findall(".//table-wrap"), start=1):
        label = text_of(table.find("./label")) or f"Table {idx}"
        caption = text_of(table.find("./caption"))
        body = text_of(table)
        full = f"{label}. {caption}. {body}"
        for outcome, pattern in OUTCOME_PATTERNS.items():
            if re.search(pattern, full, flags=re.I):
                context = find_numeric_context(full, pattern)
                rows.append(
                    {
                        "pmcid": pmcid,
                        "table_index": idx,
                        "table_label": label,
                        "outcome": outcome,
                        "arm_signal": has_arm_signal(context),
                        "numeric_tokens": numeric_density(context),
                        "candidate_numeric_context": context[:2500],
                        "effect_extract_status": "candidate_table_found",
                        "extractor_note": "Requires author extraction of arm-level n/mean/SD or events/denominators.",
                    }
                )
    return rows


def main() -> None:
    primary = pd.read_csv(TABLES / "pmc_accessible_primary_include_first_reviewer.csv").fillna("")
    all_rows = []
    for _, row in primary.iterrows():
        pmcid = norm(row.get("pmcid", ""))
        mined = mine_tables(pmcid)
        if mined:
            for item in mined:
                item.update(
                    {
                        "pmid": norm(row.get("pmid", "")),
                        "doi": norm(row.get("doi", "")),
                        "title": norm(row.get("title", "")) or norm(row.get("article_title_mined", "")),
                        "intervention_node_prelim": norm(row.get("intervention_node_prelim", "")),
                    }
                )
                all_rows.append(item)
        else:
            all_rows.append(
                {
                    "pmcid": pmcid,
                    "pmid": norm(row.get("pmid", "")),
                    "doi": norm(row.get("doi", "")),
                    "title": norm(row.get("title", "")) or norm(row.get("article_title_mined", "")),
                    "intervention_node_prelim": norm(row.get("intervention_node_prelim", "")),
                    "table_index": "",
                    "table_label": "",
                    "outcome": "",
                    "arm_signal": "no",
                    "numeric_tokens": 0,
                    "candidate_numeric_context": "",
                    "effect_extract_status": "no_candidate_table_found",
                    "extractor_note": "No relevant outcome table was identified by text mining; author must inspect full text manually.",
                }
            )
    out = pd.DataFrame(all_rows)
    out.to_csv(TABLES / "primary_accessible_numeric_table_mining.csv", index=False)
    summary = out.groupby(["outcome", "effect_extract_status"], dropna=False).size().reset_index(name="candidate_table_rows")
    summary.to_csv(TABLES / "primary_accessible_numeric_table_mining_counts.csv", index=False)
    study_summary = out.groupby("pmcid").agg(
        candidate_table_rows=("effect_extract_status", lambda s: int((s == "candidate_table_found").sum())),
        outcomes_detected=("outcome", lambda s: ";".join(sorted({x for x in s if x}))),
    ).reset_index()
    study_summary.to_csv(TABLES / "primary_accessible_numeric_table_mining_by_study.csv", index=False)
    print(f"primary_accessible_studies={len(primary)}")
    print(f"numeric_table_rows={len(out)}")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
