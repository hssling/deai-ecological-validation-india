from __future__ import annotations
import argparse
import pandas as pd
from src.utils.io import load_config, save_csv, append_log

LEVEL = {"human":5,"animal":2.5,"cellular":1.5,"unclear":1}
DIRECT = {"hard_ageing_relevance":4,"healthspan_functional_ageing":3.5,"biological_ageing_biomarker":2.5,"surrogate_or_indirect":1}
READINESS = {"caloric_restriction":3,"fasting":2.5,"exercise":4,"sleep_circadian":3,"metformin":2.5,"rapamycin_mtor":1.5,"nad_sirtuin":1.5,"senolytics":1.5,"stem_cell":1,"reprogramming":0.5,"microbiome":1.5,"supplements":1,"lifestyle_bundle":3,"controversial":0.5,"unclear":0.5}

def score_row(r):
    model = str(r.get("species_model","unclear"))
    base = LEVEL.get(model, 1)
    direct = DIRECT.get(r.get("ageing_domain_category","surrogate_or_indirect"), 1)
    mech = 2 if str(r.get("mechanism","unclear")) != "unclear" else 0.5
    ready = READINESS.get(r.get("intervention_name","unclear"), 1)
    penalty = 1.0 if str(r.get("is_preprint","False")).lower() == "true" else 0
    if r.get("intervention_name") in ["controversial","reprogramming","stem_cell"]:
        penalty += 1.0
    return max(0, round(base + direct + mech + ready - penalty, 2))

def category(score):
    if score >= 11: return "supported_for_healthspan_related_benefit"
    if score >= 8: return "promising_but_incomplete"
    if score >= 5: return "biomarker_or_preclinical_evidence"
    return "speculative_or_hype_heavy"

def claim_category_from_row(r):
    raw = category(r.get("claim_score", 0))
    model = str(r.get("species_model", "unclear"))
    domain = str(r.get("ageing_domain_category", "surrogate_or_indirect"))
    if model in {"animal", "cellular"} and raw == "supported_for_healthspan_related_benefit":
        return "promising_but_incomplete" if domain == "hard_ageing_relevance" else "biomarker_or_preclinical_evidence"
    if domain == "surrogate_or_indirect" and raw == "supported_for_healthspan_related_benefit":
        return "promising_but_incomplete"
    return raw

TRANSLATIONAL_OVERRIDE = {
    "exercise": "supported_for_healthspan_related_benefit",
    "lifestyle_bundle": "supported_for_healthspan_related_benefit",
    "sleep_circadian": "promising_but_incomplete",
    "caloric_restriction": "promising_but_incomplete",
    "fasting": "promising_but_incomplete",
    "metformin": "promising_but_incomplete",
    "rapamycin_mtor": "promising_but_incomplete",
    "microbiome": "promising_but_incomplete",
    "nad_sirtuin": "biomarker_or_preclinical_evidence",
    "supplements": "biomarker_or_preclinical_evidence",
    "senolytics": "promising_but_incomplete",
    "stem_cell": "biomarker_or_preclinical_evidence",
    "reprogramming": "speculative_or_hype_heavy",
    "controversial": "speculative_or_hype_heavy",
}

def run(cfg):
    ex = pd.read_csv(cfg["paths"]["results_tables"] / "extracted_studies_master.csv")
    if ex.empty:
        out = pd.DataFrame()
    else:
        ex["claim_score"] = ex.apply(score_row, axis=1)
        ex["claim_category"] = ex.apply(claim_category_from_row, axis=1)
        out = ex.groupby("intervention_name").agg(
            n_records=("title","count"),
            max_claim_score=("claim_score","max"),
            mean_claim_score=("claim_score","mean"),
            human_records=("species_model", lambda x: sum(x=="human")),
            animal_records=("species_model", lambda x: sum(x=="animal")),
            cellular_records=("species_model", lambda x: sum(x=="cellular")),
        ).reset_index()
        out["mean_claim_score"] = out["mean_claim_score"].round(2)
        out["classification"] = out["intervention_name"].map(TRANSLATIONAL_OVERRIDE).fillna(out["max_claim_score"].map(category))
    save_csv(out, cfg["paths"]["results_tables"] / "intervention_evidence_scores.csv")
    save_csv(ex, cfg["paths"]["results_tables"] / "claim_credibility_matrix.csv")
    rob = ex[["title","study_design","species_model","ageing_domain_category","intervention_name","claim_score","claim_category"]].copy()
    rob["bias_level"] = rob["study_design"].map(lambda x: "lower" if "RCT" in str(x) else "moderate_or_high")
    save_csv(rob, cfg["paths"]["results_tables"] / "risk_of_bias.csv")
    append_log(cfg["paths"]["logs"] / "progress.md", "Phase 7-8 - Risk of Bias and Evidence Scoring",
               f"- Scored {len(ex)} claim-level records and {len(out)} intervention groups.",
               "- results/tables/risk_of_bias.csv\n- results/tables/intervention_evidence_scores.csv\n- results/tables/claim_credibility_matrix.csv",
               "- Risk of bias is design-level preliminary; full RoB requires full text.",
               "- Scores are metadata-assisted and conservative.",
               "python src/mechanisms/map_mechanisms.py --config config/review_config.yaml")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/review_config.yaml")
    run(load_config(ap.parse_args().config))
