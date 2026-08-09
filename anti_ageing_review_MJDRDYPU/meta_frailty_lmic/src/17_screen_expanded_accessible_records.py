from __future__ import annotations

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


def intervention_components(text: str) -> str:
    comps = []
    patterns = [
        ("resistance", r"resistance|strength training|strengthening|muscle strength|handgrip"),
        ("balance", r"balance|fall prevention|otago|tinetti"),
        ("aerobic_walking", r"walking|aerobic|endurance"),
        ("multicomponent_exercise", r"multicomponent exercise|multi-component exercise|combined exercise|exercise program"),
        ("mind_body", r"tai chi|taiji|qigong|yoga"),
        ("nutrition", r"nutrition|protein|amino acid|leucine|hmb|vitamin d|supplement|diet"),
        ("multidomain", r"multidomain|multi-domain|comprehensive geriatric|cga|lifestyle intervention"),
        ("digital_home", r"digital|mhealth|mobile|telehealth|home-based|home based|app|tablet|remote"),
    ]
    for name, pattern in patterns:
        if has(text, pattern):
            comps.append(name)
    return ";".join(comps) if comps else "unclear"


def setting_code(text: str) -> str:
    if has(text, r"community|community-dwelling|community dwelling"):
        return "community"
    if has(text, r"home-based|home based|at home|in-home"):
        return "home"
    if has(text, r"primary care|general practice|family practice"):
        return "primary_care"
    if has(text, r"outpatient|day hospital|day care"):
        return "outpatient_or_day_service"
    if has(text, r"nursing home|residential|long-term care|care home"):
        return "residential_or_nursing_home"
    if has(text, r"hospital|post-acute|inpatient|rehabilitation ward"):
        return "hospital_or_postacute"
    return "unclear"


def node_from_components(comps: str) -> str:
    s = set(comps.split(";"))
    exercise = bool(s & {"resistance", "balance", "aerobic_walking", "multicomponent_exercise", "mind_body"})
    nutrition = "nutrition" in s
    multidomain = "multidomain" in s
    digital = "digital_home" in s
    if multidomain and exercise and nutrition:
        return "multidomain_exercise_nutrition"
    if exercise and nutrition:
        return "exercise_plus_nutrition"
    if multidomain:
        return "multidomain"
    if "multicomponent_exercise" in s:
        return "multicomponent_exercise"
    if "mind_body" in s and not (s & {"resistance", "balance", "aerobic_walking"}):
        return "mind_body"
    if exercise:
        return "exercise_only"
    if nutrition:
        return "nutrition_only"
    if digital:
        return "digital_home_unclear_intervention"
    return "unclear"


def screen(row: pd.Series) -> dict[str, str]:
    title = norm(row.get("title", ""))
    abstract = norm(row.get("abstract", ""))
    source = norm(row.get("source", ""))
    blob = f"{title} {abstract}"

    if not has(blob, r"\bpre[- ]?frail|\bfrail(?:ty)?\b|physical frailty|frailty phenotype|clinical frailty|sarcopen"):
        return {"expanded_screen_decision": "exclude_no_frailty_or_sarcopenia", "expanded_screen_reason": "No frailty/sarcopenia signal"}
    if not has(blob, r"randomi[sz]ed|randomly|controlled trial|\btrial\b|interventional|allocation"):
        return {"expanded_screen_decision": "exclude_not_rct_signal", "expanded_screen_reason": "No randomized/interventional signal"}
    if not has(blob, r"older|elderly|aged|geriatric|community|nursing home|primary care|home"):
        return {"expanded_screen_decision": "exclude_population_unclear", "expanded_screen_reason": "Older-adult target unclear"}
    if has(blob, r"protocol|study protocol|design and rationale|baseline characteristics"):
        return {"expanded_screen_decision": "context_protocol", "expanded_screen_reason": "Protocol/design record"}
    if has(blob, r"systematic review|meta-analysis|scoping review|review protocol"):
        return {"expanded_screen_decision": "context_review", "expanded_screen_reason": "Review/context record"}
    if has(blob, r"stroke|cancer|parkinson|copd|heart failure|hip fracture|surgery|icu|intensive care"):
        return {"expanded_screen_decision": "secondary_disease_specific", "expanded_screen_reason": "Disease-specific rehabilitation signal"}

    comps = intervention_components(blob)
    setting = setting_code(blob)
    if not has(blob, r"exercise|training|nutrition|protein|supplement|multidomain|home-based|digital|tai chi|otago|balance|walking"):
        return {"expanded_screen_decision": "maybe_intervention_unclear", "expanded_screen_reason": "Relevant design/population but intervention unclear"}

    if source == "ClinicalTrials.gov":
        return {"expanded_screen_decision": "registry_candidate", "expanded_screen_reason": "Trial registry record requiring publication matching"}

    if setting in {"hospital_or_postacute", "residential_or_nursing_home"}:
        return {"expanded_screen_decision": "secondary_setting", "expanded_screen_reason": "Potentially relevant but outside primary community/home scope"}

    return {"expanded_screen_decision": "fulltext_candidate", "expanded_screen_reason": "Expanded-search frailty intervention RCT candidate"}


def main() -> None:
    df = pd.read_csv(PROCESSED / "expanded_accessible_deduped_records.csv").fillna("")
    decisions = pd.DataFrame([screen(row) for _, row in df.iterrows()])
    out = pd.concat([df.reset_index(drop=True), decisions], axis=1)
    blobs = (out["title"].astype(str) + " " + out["abstract"].astype(str)).map(norm)
    out["setting_code_expanded"] = blobs.map(setting_code)
    out["component_code_expanded"] = blobs.map(intervention_components)
    out["intervention_node_expanded"] = out["component_code_expanded"].map(node_from_components)

    existing = pd.read_csv(TABLES / "high_confidence_extraction_queue.csv").fillna("")
    existing_pmids = set(existing["pmid"].astype(str))
    existing_dois = set(existing["doi"].astype(str).str.lower())
    out["already_in_high_confidence_queue"] = (
        out["pmid"].astype(str).isin(existing_pmids) | out["doi"].astype(str).str.lower().isin(existing_dois)
    ).map({True: "yes", False: "no"})

    out.to_csv(PROCESSED / "expanded_accessible_screened_records.csv", index=False)
    out["expanded_screen_decision"].value_counts().rename_axis("decision").reset_index(name="n").to_csv(
        TABLES / "expanded_accessible_screening_counts.csv", index=False
    )

    candidates = out[out["expanded_screen_decision"].isin(["fulltext_candidate", "registry_candidate"])].copy()
    candidates.to_csv(TABLES / "expanded_accessible_fulltext_or_registry_candidates.csv", index=False)
    new_candidates = candidates[candidates["already_in_high_confidence_queue"].eq("no")].copy()
    new_candidates.to_csv(TABLES / "expanded_accessible_new_candidates_not_in_primary_queue.csv", index=False)
    candidates["intervention_node_expanded"].value_counts().rename_axis("node").reset_index(name="n").to_csv(
        TABLES / "expanded_accessible_candidate_node_counts.csv", index=False
    )
    print(out["expanded_screen_decision"].value_counts().to_string())
    print(f"candidate_or_registry={len(candidates)}")
    print(f"new_not_in_high_confidence={len(new_candidates)}")


if __name__ == "__main__":
    main()
