from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_FULLTEXT = ROOT / "data" / "raw" / "pmc_fulltext"
TABLES = ROOT / "results" / "tables"


OUTCOME_PATTERNS = {
    "frailty": r"frailty|frail|prefrail|pre-frail",
    "gait_speed": r"gait speed|walking speed",
    "sppb": r"short physical performance battery|sppb",
    "grip_strength": r"grip strength|handgrip",
    "adl": r"activities of daily living|\badl\b|iadl",
    "falls": r"\bfalls?\b|fall risk",
    "quality_of_life": r"quality of life|qol|eq-5d|sf-36",
    "adherence": r"adherence|compliance|attendance",
    "adverse_events": r"adverse event|safety|injury",
}


def text_of(elem: ET.Element | None) -> str:
    if elem is None:
        return ""
    return re.sub(r"\s+", " ", " ".join(elem.itertext())).strip()


def find_sections(root: ET.Element, title_pattern: str) -> str:
    chunks = []
    for sec in root.findall(".//sec"):
        title = text_of(sec.find("./title")).lower()
        if re.search(title_pattern, title):
            chunks.append(text_of(sec)[:4000])
    return "\n".join(chunks)


def snippet(text: str, pattern: str, width: int = 180) -> str:
    match = re.search(pattern, text, flags=re.I)
    if not match:
        return ""
    start = max(match.start() - width, 0)
    end = min(match.end() + width, len(text))
    return text[start:end].strip()


def mine_file(path: Path) -> dict[str, str | int]:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError:
        return {"pmcid": path.stem, "parse_status": "parse_error"}

    article_title = text_of(root.find(".//article-title"))
    abstract = text_of(root.find(".//abstract"))
    methods = find_sections(root, r"method|material|intervention|participant")
    results = find_sections(root, r"result|finding")
    full = text_of(root)

    table_texts = []
    for table in root.findall(".//table-wrap"):
        label = text_of(table.find("./label"))
        caption = text_of(table.find("./caption"))
        body = text_of(table)
        table_texts.append(f"{label} {caption} {body}"[:2500])
    table_blob = "\n---TABLE---\n".join(table_texts[:8])

    outcomes = []
    outcome_snips = {}
    for name, pattern in OUTCOME_PATTERNS.items():
        if re.search(pattern, full, flags=re.I):
            outcomes.append(name)
            outcome_snips[f"snippet_{name}"] = snippet(full, pattern)
        else:
            outcome_snips[f"snippet_{name}"] = ""

    intervention_snip = snippet(full, r"intervention|exercise|nutrition|protein|resistance|multicomponent|tai chi|home-based")
    comparator_snip = snippet(full, r"control group|usual care|waitlist|placebo|comparator|attention control")
    randomization_snip = snippet(full, r"randomi[sz]ed|random allocation|randomly assigned|allocation conceal")

    return {
        "pmcid": path.stem,
        "parse_status": "ok",
        "article_title": article_title,
        "abstract": abstract[:1200],
        "detected_outcomes": ";".join(outcomes),
        "randomization_snippet": randomization_snip,
        "intervention_snippet": intervention_snip,
        "comparator_snippet": comparator_snip,
        "methods_snippet": methods[:1800],
        "results_snippet": results[:1800],
        "table_count": len(table_texts),
        "table_text_preview": table_blob[:3000],
        **outcome_snips,
    }


def main() -> None:
    rows = [mine_file(path) for path in sorted(RAW_FULLTEXT.glob("PMC*.xml"))]
    out = pd.DataFrame(rows)
    out.to_csv(TABLES / "pmc_fulltext_mining.csv", index=False)
    print(f"fulltexts_mined={len(out)}")
    if not out.empty:
        print(out["parse_status"].value_counts().to_string())
        print(out["detected_outcomes"].str.get_dummies(sep=";").sum().sort_values(ascending=False).to_string())


if __name__ == "__main__":
    main()
