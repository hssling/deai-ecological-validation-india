from __future__ import annotations
import argparse, re
import pandas as pd
from src.screening.screen_records import INTERVENTIONS
from src.utils.io import load_config, save_csv, append_log

MECH = {
 "cellular_senescence":["senescence","senolytic","senomorphic","p16","p21","sasp"],
 "inflammaging":["inflammation","inflammatory","il-6","crp","inflammaging","nf-kb"],
 "mitochondrial_function":["mitochondria","mitochondrial","oxidative phosphorylation"],
 "proteostasis_autophagy":["autophagy","proteostasis","proteasome"],
 "stem_cell_effects":["stem cell","regenerative"],
 "nutrient_sensing":["mtor","ampk","insulin","igf","rapamycin","metformin"],
 "epigenetic_alterations":["epigenetic","dna methylation","yamanaka","reprogramming"],
 "sirtuin_nad":["sirtuin","nad","nmn","nicotinamide"],
 "microbiome_host":["microbiome","microbiota","probiotic"],
 "dna_repair_genomic":["dna repair","genomic instability","telomerase","telomere"],
}

def first_class(t):
    hits = [k for k, vals in INTERVENTIONS.items() if any(v in t for v in vals)]
    return hits[0] if hits else "unclear"

def design(t, pubtype):
    x = f"{t} {pubtype}".lower()
    if "randomized" in x or "randomised" in x or "clinical trial" in x: return "RCT_or_clinical_trial"
    if "cohort" in x: return "cohort"
    if "cross-sectional" in x: return "cross-sectional"
    if any(y in x for y in ["mouse","mice","rat","drosophila","c elegans"]): return "animal_experiment"
    if any(y in x for y in ["cell","in vitro","fibroblast"]): return "in_vitro_study"
    return "unclear_or_metadata_only"

def outcome_domain(t):
    if any(x in t for x in ["mortality","survival","lifespan"]): return "hard_ageing_relevance"
    if any(x in t for x in ["frailty","disability","adl","iadl","grip","gait","cognition","multimorbidity","physical performance"]): return "healthspan_functional_ageing"
    if any(x in t for x in ["epigenetic clock","dna methylation age","biological age","transcriptomic age","proteomic age","senescence"]): return "biological_ageing_biomarker"
    return "surrogate_or_indirect"

def mechanisms(t):
    return [k for k, vals in MECH.items() if any(v in t for v in vals)] or ["unclear"]

def run(cfg):
    s = pd.read_csv(cfg["paths"]["results_tables"] / "title_abstract_screening.csv")
    inc = s[s["screen_label"].isin(["include","uncertain"])].copy()
    rows = []
    for _, r in inc.iterrows():
        t = f"{r.get('title','')} {r.get('abstract','')}".lower()
        rows.append({
            "title":r.get("title",""),"authors":r.get("authors",""),"year":r.get("year",""),"journal":r.get("journal",""),
            "doi":r.get("doi",""),"pmid":r.get("pmid",""),"source":r.get("source",""),"is_preprint":r.get("is_preprint",False),
            "study_design":design(t, r.get("publication_type","")),"species_model":r.get("evidence_model","unclear"),
            "sample_size":"","age_sex":"","disease_status":"","intervention_name":first_class(t),
            "intervention_class":r.get("intervention_classes",""),"dose_intensity":"","duration":"","comparator":"",
            "outcome_exact":r.get("outcome_terms",""),"ageing_domain_category":outcome_domain(t),
            "effect_direction":"not_extracted_metadata_only","effect_size":"","uncertainty_measure":"","follow_up_time":"",
            "mechanism":"; ".join(mechanisms(t)),"mechanism_directness":"inferred_from_title_abstract",
            "extraction_confidence":0.45 if r.get("screen_label")=="uncertain" else 0.6,
            "missingness_flag":"requires_full_text_verification","ambiguity_notes":"Metadata-assisted extraction; do not use as final effect extraction."
        })
    out = pd.DataFrame(rows)
    save_csv(out, cfg["paths"]["results_tables"] / "extracted_studies_master.csv")
    dictionary = pd.DataFrame({"field":out.columns, "description":["See extraction_manual.md; metadata-assisted pilot field." for _ in out.columns]})
    save_csv(dictionary, cfg["_root"] / "metadata/extraction_dictionary.csv")
    append_log(cfg["paths"]["logs"] / "progress.md", "Phase 6 - Structured Data Extraction",
               f"- Created metadata-assisted extraction table for {len(out)} candidate studies.",
               "- results/tables/extracted_studies_master.csv\n- metadata/extraction_dictionary.csv",
               "- Full effect sizes, doses, durations, and bias fields require full-text extraction.",
               "- Metadata extraction is preliminary and explicitly flagged.",
               "python src/grading/score_evidence.py --config config/review_config.yaml")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/review_config.yaml")
    run(load_config(ap.parse_args().config))
