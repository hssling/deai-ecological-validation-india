from __future__ import annotations

import csv
import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
TABLES = ROOT / "results" / "tables"


def norm(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def has(text: str, pattern: str) -> bool:
    return bool(re.search(pattern, text, flags=re.I))


def priority(row: pd.Series) -> dict[str, str]:
    title = norm(row.get("title", ""))
    abstract = norm(row.get("abstract", ""))
    blob = f"{title} {abstract}"

    frailty_core = has(blob, r"\bpre[- ]?frail|\bfrail(?:ty)?\b|physical frailty|frailty status")
    sarcopenia = has(blob, r"\bsarcopenia|sarcopenic|osteosarcopenia")
    rct = has(blob, r"randomi[sz]ed|random allocation|randomly assigned|controlled trial|clinical trial")
    community = has(blob, r"community[- ]dwelling|community|primary care|home[- ]based|outpatient|older adults")
    residential = has(blob, r"nursing home|long[- ]term care|residential care|care home")
    hospital = has(blob, r"hospitali[sz]ed|inpatient|intensive care|icu|stroke|cancer survivor|heart failure|multiple sclerosis")
    implementation = has(blob, r"home[- ]based|mhealth|digital|app[- ]based|telerehabilitation|caregiver|lay|community health")
    target_outcome = has(
        blob,
        r"frailty status|frailty score|gait speed|short physical performance battery|sppb|grip strength|physical performance|physical function|adl|activities of daily living",
    )

    if row.get("screen_decision") != "include_title_abs":
        return {"fulltext_priority": "not_applicable", "priority_reason": "Not included at title/abstract stage"}
    if not rct:
        return {"fulltext_priority": "low", "priority_reason": "RCT design not sufficiently clear"}
    if frailty_core and community and target_outcome and not hospital and not residential:
        return {"fulltext_priority": "A_primary_fulltext", "priority_reason": "Community/primary-care frailty RCT candidate"}
    if frailty_core and implementation and target_outcome:
        return {"fulltext_priority": "A_primary_fulltext", "priority_reason": "Implementation-relevant frailty RCT candidate"}
    if frailty_core and target_outcome:
        return {"fulltext_priority": "B_secondary_fulltext", "priority_reason": "Frailty RCT candidate, setting or delivery less directly Indian-primary-care relevant"}
    if sarcopenia and community and target_outcome and not hospital:
        return {"fulltext_priority": "C_sarcopenia_secondary", "priority_reason": "Community sarcopenia RCT; secondary stratum"}
    if sarcopenia and target_outcome:
        return {"fulltext_priority": "D_sarcopenia_context", "priority_reason": "Sarcopenia RCT; context or sensitivity only"}
    return {"fulltext_priority": "low", "priority_reason": "Does not meet primary frailty/community priority after detailed rule"}


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(PROCESSED / "screened_title_abstract.csv").fillna("")
    priorities = pd.DataFrame([priority(row) for _, row in df.iterrows()])
    out = pd.concat([df.reset_index(drop=True), priorities], axis=1)
    out.to_csv(PROCESSED / "screened_prioritized.csv", index=False, quoting=csv.QUOTE_MINIMAL)

    counts = (
        out.groupby(["screen_decision", "fulltext_priority"], dropna=False)
        .size()
        .reset_index(name="n")
        .sort_values(["screen_decision", "fulltext_priority"])
    )
    counts.to_csv(TABLES / "fulltext_priority_counts.csv", index=False)

    for label in ["A_primary_fulltext", "B_secondary_fulltext", "C_sarcopenia_secondary", "D_sarcopenia_context"]:
        out[out["fulltext_priority"].eq(label)].to_csv(
            TABLES / f"{label}.csv", index=False, quoting=csv.QUOTE_MINIMAL
        )

    print(counts.to_string(index=False))


if __name__ == "__main__":
    main()
