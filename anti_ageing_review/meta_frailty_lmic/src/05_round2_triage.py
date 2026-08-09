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


def rx(text: str, pattern: str) -> bool:
    return bool(re.search(pattern, text, flags=re.I))


def component_code(text: str) -> str:
    components = []
    checks = [
        ("resistance", r"resistance|strength|weight training|quadriceps"),
        ("balance", r"balance|fall|falls"),
        ("aerobic_walking", r"aerobic|walking|endurance|water exercise"),
        ("multicomponent_exercise", r"multicomponent|multi-component|vivifrail|combined exercise"),
        ("mind_body", r"tai chi|taiji|qigong|baduanjin|yoga"),
        ("nutrition", r"nutrition|protein|leucine|hmb|vitamin d|supplement|whey|soy"),
        ("digital_home", r"home-based|video|app|mhealth|digital|telerehabilitation|remote|exergame"),
        ("multidomain", r"multidomain|multi-domain|geriatric team|comprehensive geriatric|lifestyle"),
    ]
    for label, pattern in checks:
        if rx(text, pattern):
            components.append(label)
    return ";".join(components) if components else "unclear"


def setting_code(text: str) -> str:
    if rx(text, r"nursing home|long[- ]term care|residential care|care home"):
        return "residential_or_nursing_home"
    if rx(text, r"hospitali[sz]ed|inpatient|surgical|surgery|hip fracture|icu|intensive"):
        return "hospital_or_postacute"
    if rx(text, r"primary care|general practice"):
        return "primary_care"
    if rx(text, r"home[- ]based|live at home|living at home"):
        return "home"
    if rx(text, r"community[- ]dwelling|community"):
        return "community"
    if rx(text, r"outpatient|day-service|day service"):
        return "outpatient_or_day_service"
    return "unclear"


def triage(row: pd.Series) -> dict[str, str]:
    title = norm(row.get("title", ""))
    journal = norm(row.get("journal", ""))
    abstract = norm(row.get("abstract", ""))
    blob = f"{title} {journal} {abstract}"
    blob_l = blob.lower()
    setting = setting_code(blob)
    components = component_code(blob)

    if rx(blob, r"medrxiv|preprint server"):
        return {
            "round2_decision": "exclude_or_hold",
            "round2_reason": "Preprint; not eligible for IJMR primary evidence unless later peer-reviewed",
            "setting_code": setting,
            "component_code": components,
        }
    if rx(title, r"protocol|study design|design and rationale|baseline characteristics|recruitment"):
        return {
            "round2_decision": "exclude",
            "round2_reason": "Protocol/design/baseline paper rather than outcome report",
            "setting_code": setting,
            "component_code": components,
        }
    if rx(title, r"systematic review|meta-analysis|scoping review|narrative review|consensus|recommendations"):
        return {
            "round2_decision": "context_citation",
            "round2_reason": "Review/consensus; use for citation chasing only",
            "setting_code": setting,
            "component_code": components,
        }
    if setting in {"hospital_or_postacute", "residential_or_nursing_home"}:
        return {
            "round2_decision": "secondary_setting",
            "round2_reason": "Hospital/post-acute/residential setting; not primary Indian primary-care scope",
            "setting_code": setting,
            "component_code": components,
        }
    if rx(blob, r"stroke|heart failure|cancer|multiple sclerosis|alzheimer|dementia|copd|parkinson|diabetes") and not rx(
        blob, r"community[- ]dwelling|primary care|home[- ]based|frail older"
    ):
        return {
            "round2_decision": "secondary_disease_specific",
            "round2_reason": "Disease-rehabilitation population; secondary/sensitivity only",
            "setting_code": setting,
            "component_code": components,
        }
    if not rx(blob, r"randomi[sz]ed|randomly|random allocation|controlled trial|clinical trial"):
        return {
            "round2_decision": "unclear_verify",
            "round2_reason": "Randomization not clear from title/abstract metadata",
            "setting_code": setting,
            "component_code": components,
        }
    if not rx(blob, r"frail|pre[- ]?frail|frailty|sarcopenia|sarcopenic"):
        return {
            "round2_decision": "exclude",
            "round2_reason": "No clear prefrail/frail/sarcopenic target",
            "setting_code": setting,
            "component_code": components,
        }
    if rx(blob, r"sarcopenia|sarcopenic") and not rx(blob, r"frail|pre[- ]?frail|frailty"):
        return {
            "round2_decision": "sarcopenia_secondary",
            "round2_reason": "Sarcopenia-only trial; retain as secondary stratum",
            "setting_code": setting,
            "component_code": components,
        }
    if not rx(
        blob,
        r"frailty status|frailty score|physical function|physical performance|gait|sppb|short physical performance|grip|adl|activities of daily living|falls|mobility|functional",
    ):
        return {
            "round2_decision": "unclear_verify",
            "round2_reason": "Eligible population/design possible but outcome needs full-text verification",
            "setting_code": setting,
            "component_code": components,
        }
    return {
        "round2_decision": "extraction_candidate",
        "round2_reason": "Peer-reviewed community/home/primary-care frailty RCT candidate with relevant outcome",
        "setting_code": setting,
        "component_code": components,
    }


def main() -> None:
    q = pd.read_csv(TABLES / "fulltext_queue_primary_A.csv").fillna("")
    all_records = pd.read_csv(PROCESSED / "screened_prioritized.csv").fillna("")
    merged = q.merge(
        all_records[["pmid", "abstract", "screen_decision", "fulltext_priority"]],
        on="pmid",
        how="left",
        suffixes=("", "_full"),
    ).fillna("")
    decisions = pd.DataFrame([triage(row) for _, row in merged.iterrows()])
    out = pd.concat([merged.reset_index(drop=True), decisions], axis=1)
    out.to_csv(TABLES / "round2_triage_primary_A.csv", index=False, quoting=csv.QUOTE_MINIMAL)

    out[out["round2_decision"].eq("extraction_candidate")].to_csv(
        TABLES / "extraction_candidate_primary.csv", index=False, quoting=csv.QUOTE_MINIMAL
    )
    out[out["round2_decision"].str.startswith("exclude", na=False)].to_csv(
        TABLES / "round2_exclusions_primary.csv", index=False, quoting=csv.QUOTE_MINIMAL
    )
    out["round2_decision"].value_counts().rename_axis("round2_decision").reset_index(name="n").to_csv(
        TABLES / "round2_triage_counts.csv", index=False
    )
    out["component_code"].str.get_dummies(sep=";").sum().sort_values(ascending=False).rename_axis("component").reset_index(
        name="n"
    ).to_csv(TABLES / "candidate_component_counts.csv", index=False)
    out["setting_code"].value_counts().rename_axis("setting").reset_index(name="n").to_csv(
        TABLES / "candidate_setting_counts.csv", index=False
    )

    print(out["round2_decision"].value_counts().to_string())


if __name__ == "__main__":
    main()
