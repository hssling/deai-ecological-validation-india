from __future__ import annotations

import csv
import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "tables"


def norm(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def has(text: str, pattern: str) -> bool:
    return bool(re.search(pattern, text, flags=re.I))


def intervention_node(component_code: str) -> str:
    comps = set(str(component_code).split(";"))
    exercise = bool(comps & {"resistance", "balance", "aerobic_walking", "multicomponent_exercise", "mind_body"})
    nutrition = "nutrition" in comps
    multidomain = "multidomain" in comps
    digital = "digital_home" in comps
    if multidomain and exercise and nutrition:
        return "multidomain_exercise_nutrition"
    if exercise and nutrition:
        return "exercise_plus_nutrition"
    if multidomain:
        return "multidomain"
    if "multicomponent_exercise" in comps:
        return "multicomponent_exercise"
    if "mind_body" in comps and not (comps & {"resistance", "balance", "aerobic_walking"}):
        return "mind_body"
    if exercise:
        return "exercise_only"
    if nutrition:
        return "nutrition_only"
    if digital:
        return "digital_home_unclear_intervention"
    return "unclear"


def high_confidence(row: pd.Series) -> dict[str, str]:
    title = norm(row.get("title", ""))
    abstract = norm(row.get("abstract", ""))
    blob = f"{title} {abstract}"
    title_l = title.lower()
    setting = norm(row.get("setting_code", ""))

    exclusion_patterns = [
        (r"protocol|study design|design and rationale|baseline characteristics|recruitment", "Protocol/design/baseline paper"),
        (r"systematic review|meta-analysis|scoping review|narrative review|consensus|recommendations", "Review/consensus paper"),
        (r"cross-sectional|observational|cohort study", "Non-randomized observational design"),
        (r"bedrest|hot water immersion|massage versus|mitochondrial respiration", "Not a pragmatic frailty intervention for Indian primary care"),
        (r"stroke|heart failure|cancer|multiple sclerosis|alzheimer|dementia|copd|parkinson|hip fracture|surgery|surgical|icu|intensive", "Disease-specific, post-acute or hospital rehabilitation population"),
        (r"healthy older adults|healthy elderly", "Healthy older-adult trial rather than prefrail/frail population"),
    ]
    for pattern, reason in exclusion_patterns:
        if has(blob, pattern):
            return {
                "high_confidence_decision": "exclude_before_extraction",
                "high_confidence_reason": reason,
                "intervention_node_prelim": intervention_node(row.get("component_code", "")),
            }

    if setting in {"hospital_or_postacute", "residential_or_nursing_home"}:
        return {
            "high_confidence_decision": "exclude_before_extraction",
            "high_confidence_reason": "Setting outside primary community/home/outpatient scope",
            "intervention_node_prelim": intervention_node(row.get("component_code", "")),
        }

    if not has(blob, r"randomi[sz]ed|randomly|random allocation|controlled trial|clinical trial"):
        return {
            "high_confidence_decision": "defer_verify_design",
            "high_confidence_reason": "Randomized design not explicit enough",
            "intervention_node_prelim": intervention_node(row.get("component_code", "")),
        }

    if not has(blob, r"\bpre[- ]?frail|\bfrail(?:ty)?\b|physical frailty|frailty status"):
        return {
            "high_confidence_decision": "defer_sarcopenia_or_vulnerability",
            "high_confidence_reason": "Frailty target not explicit enough for primary set",
            "intervention_node_prelim": intervention_node(row.get("component_code", "")),
        }

    if not has(
        blob,
        r"frailty status|frailty score|physical function|physical performance|gait|sppb|short physical performance|grip|adl|activities of daily living|falls|mobility|functional",
    ):
        return {
            "high_confidence_decision": "defer_verify_outcomes",
            "high_confidence_reason": "Outcome needs full-text verification",
            "intervention_node_prelim": intervention_node(row.get("component_code", "")),
        }

    return {
        "high_confidence_decision": "extract_now",
        "high_confidence_reason": "High-confidence community/home/primary-care frailty RCT candidate",
        "intervention_node_prelim": intervention_node(row.get("component_code", "")),
    }


def main() -> None:
    df = pd.read_csv(TABLES / "round2_triage_primary_A.csv").fillna("")
    decisions = pd.DataFrame([high_confidence(row) for _, row in df.iterrows()])
    out = pd.concat([df.reset_index(drop=True), decisions], axis=1)
    out.to_csv(TABLES / "high_confidence_triage.csv", index=False, quoting=csv.QUOTE_MINIMAL)

    extract = out[out["high_confidence_decision"].eq("extract_now")].copy()
    extract.to_csv(TABLES / "high_confidence_extraction_queue.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    out["high_confidence_decision"].value_counts().rename_axis("decision").reset_index(name="n").to_csv(
        TABLES / "high_confidence_triage_counts.csv", index=False
    )
    extract["intervention_node_prelim"].value_counts().rename_axis("intervention_node_prelim").reset_index(name="n").to_csv(
        TABLES / "prelim_intervention_node_counts.csv", index=False
    )

    prefilled_cols = [
        "pmid",
        "doi",
        "title",
        "year",
        "journal",
        "setting_code",
        "component_code",
        "intervention_node_prelim",
        "round2_reason",
        "high_confidence_reason",
    ]
    extract[prefilled_cols].to_csv(TABLES / "extraction_prefilled_primary.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    print(out["high_confidence_decision"].value_counts().to_string())
    print("\nPreliminary nodes:")
    print(extract["intervention_node_prelim"].value_counts().to_string())


if __name__ == "__main__":
    main()
