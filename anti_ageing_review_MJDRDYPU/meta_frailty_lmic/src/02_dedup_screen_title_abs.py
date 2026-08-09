from __future__ import annotations

import csv
import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INTERIM = ROOT / "data" / "interim"
PROCESSED = ROOT / "data" / "processed"
TABLES = ROOT / "results" / "tables"


def norm(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def title_key(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", " ", norm(value).lower()).strip()


def has_any(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def screen(row: pd.Series) -> dict[str, str]:
    title = norm(row.get("title", ""))
    abstract = norm(row.get("abstract", ""))
    blob = f"{title} {abstract}".lower()

    review_terms = ["systematic review", "meta-analysis", "network meta-analysis", "narrative review", "umbrella review"]
    protocol_terms = ["study protocol", "protocol for", "trial protocol", "protocol of a randomized"]
    nonhuman_terms = ["mice", "mouse", "rat ", "rats", "animal model", "cell culture"]
    older_terms = ["older", "elderly", "aged", "geriatric", "community-dwelling", "community dwelling", "nursing home", "long-term care"]
    frailty_terms = ["frail", "prefrail", "pre-frail", "physical frailty", "frailty status", "sarcopenia", "sarcopenic"]
    intervention_terms = [
        "exercise",
        "training",
        "resistance",
        "balance",
        "walking",
        "aerobic",
        "tai chi",
        "nutrition",
        "protein",
        "leucine",
        "hmb",
        "vitamin d",
        "multicomponent",
        "multidomain",
        "home-based",
        "mhealth",
        "digital",
    ]
    rct_terms = ["randomized", "randomised", "randomly", "random allocation", "controlled trial", "clinical trial", "rct"]
    outcome_terms = [
        "frailty",
        "gait speed",
        "short physical performance battery",
        "sppb",
        "grip strength",
        "physical performance",
        "physical function",
        "activities of daily living",
        "adl",
        "falls",
    ]

    if has_any(blob, nonhuman_terms):
        return {"screen_decision": "exclude", "reason": "Non-human or preclinical record"}
    if has_any(blob, review_terms):
        return {"screen_decision": "context_review", "reason": "Review or meta-analysis; retain for citation chasing only"}
    if has_any(blob, protocol_terms):
        return {"screen_decision": "context_protocol", "reason": "Protocol; retain for trial follow-up only"}
    if not has_any(blob, older_terms):
        return {"screen_decision": "exclude", "reason": "Older-adult population not evident"}
    if not has_any(blob, frailty_terms):
        return {"screen_decision": "exclude", "reason": "Frailty/sarcopenia target not evident"}
    if not has_any(blob, intervention_terms):
        return {"screen_decision": "exclude", "reason": "Relevant intervention not evident"}
    if not has_any(blob, rct_terms):
        return {"screen_decision": "maybe_nonrandomized", "reason": "Relevant population/intervention, RCT design not evident"}
    if not has_any(blob, outcome_terms):
        return {"screen_decision": "maybe_outcome_unclear", "reason": "RCT candidate but primary frailty/function outcome unclear"}
    return {"screen_decision": "include_title_abs", "reason": "Potential eligible RCT at title/abstract stage"}


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(INTERIM / "pubmed_candidate_records.csv").fillna("")

    grouped: dict[str, dict] = {}
    for _, row in df.iterrows():
        doi = norm(row.get("doi", "")).lower()
        pmid = norm(row.get("pmid", ""))
        key = f"doi:{doi}" if doi else f"pmid:{pmid}" if pmid else f"title:{title_key(row.get('title', ''))}"
        if key not in grouped:
            item = row.to_dict()
            item["dedupe_key"] = key
            grouped[key] = item

    deduped = pd.DataFrame(grouped.values())
    decisions = [screen(row) for _, row in deduped.iterrows()]
    screened = pd.concat([deduped.reset_index(drop=True), pd.DataFrame(decisions)], axis=1)

    screened.to_csv(PROCESSED / "screened_title_abstract.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    screened[screened["screen_decision"].eq("include_title_abs")].to_csv(
        TABLES / "title_abs_included_rct_candidates.csv", index=False, quoting=csv.QUOTE_MINIMAL
    )
    screened["screen_decision"].value_counts().rename_axis("screen_decision").reset_index(name="n").to_csv(
        TABLES / "title_abs_screening_counts.csv", index=False
    )
    print(f"records_input={len(df)}")
    print(f"records_deduped={len(screened)}")
    print(screened["screen_decision"].value_counts().to_string())


if __name__ == "__main__":
    main()
