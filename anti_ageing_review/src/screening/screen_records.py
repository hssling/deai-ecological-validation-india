from __future__ import annotations
import argparse, re
import pandas as pd
from src.utils.io import load_config, save_csv, append_log

INTERVENTIONS = {
 "caloric_restriction":["caloric restriction","calorie restriction","dietary restriction"],
 "fasting":["fasting","time restricted","fasting mimicking"],
 "exercise":["exercise","physical activity","resistance training","aerobic"],
 "sleep_circadian":["sleep","circadian"],
 "metformin":["metformin"],
 "rapamycin_mtor":["rapamycin","sirolimus","mtor"],
 "nad_sirtuin":["nad","nicotinamide riboside","nmn","sirtuin"],
 "senolytics":["senolytic","senomorphic","fisetin","dasatinib","quercetin"],
 "stem_cell":["stem cell","regenerative"],
 "reprogramming":["yamanaka","partial reprogramming","epigenetic reprogramming"],
 "microbiome":["microbiome","probiotic","fecal microbiota"],
 "supplements":["resveratrol","curcumin","omega","vitamin d","supplement"],
 "lifestyle_bundle":["lifestyle","multidomain"],
 "controversial":["parabiosis","young plasma","plasma dilution","telomerase"],
}
OUTCOME_TERMS = ["lifespan","survival","mortality","healthspan","frailty","disability","adl","iadl","grip","gait","cognition","multimorbidity","epigenetic clock","biological age","dna methylation age","senescence","inflammaging","rejuvenation"]
NON_EMP = ["review","editorial","commentary","letter","protocol","perspective"]

def text(row):
    return f"{row.get('title','')} {row.get('abstract','')} {row.get('publication_type','')}".lower()

def classify_model(t):
    if any(x in t for x in ["mouse","mice","murine","c elegans","drosophila","rat "]): return "animal"
    if any(x in t for x in ["cell","in vitro","fibroblast","organoid"]): return "cellular"
    if any(x in t for x in ["human","randomized","clinical trial","participants","patients","adults","men","women"]): return "human"
    return "unclear"

def screen_row(row):
    t = text(row)
    inter = [k for k, vals in INTERVENTIONS.items() if any(v in t for v in vals)]
    outcomes = [o for o in OUTCOME_TERMS if o in t]
    non_emp = any(x in t for x in NON_EMP) and "trial" not in t
    score = len(inter)*2 + min(len(outcomes), 4)
    if "randomized" in t or "trial" in t: score += 1
    if row.get("is_preprint", False): score -= 1
    if non_emp and not inter:
        return "exclude", 0.85, "non_empirical", inter, outcomes, classify_model(t)
    if not inter:
        return "exclude", 0.7, "no_clear_intervention", inter, outcomes, classify_model(t)
    if not outcomes:
        return "uncertain", 0.45, "ageing_outcome_unclear", inter, outcomes, classify_model(t)
    if score >= 4:
        return "include", min(0.95, 0.55 + score/20), "", inter, outcomes, classify_model(t)
    return "uncertain", 0.55, "needs_full_text_or_abstract", inter, outcomes, classify_model(t)

def run(cfg):
    master = pd.read_csv(cfg["paths"]["results_tables"] / "master_records_dedup.csv")
    rows = []
    for _, r in master.iterrows():
        label, conf, reason, inter, outcomes, model = screen_row(r)
        d = r.to_dict()
        d.update({"screen_label":label,"screen_confidence":round(conf,2),"exclusion_reason":reason,
                  "intervention_classes":"; ".join(inter),"outcome_terms":"; ".join(outcomes),"evidence_model":model})
        rows.append(d)
    out = pd.DataFrame(rows)
    save_csv(out, cfg["paths"]["results_tables"] / "title_abstract_screening.csv")
    full = out[out["screen_label"].isin(["include","uncertain"])].copy()
    full["full_text_label"] = "pending"
    full["full_text_exclusion_reason"] = ""
    save_csv(full, cfg["paths"]["results_tables"] / "full_text_screening.csv")
    append_log(cfg["paths"]["logs"] / "progress.md", "Phase 4 - Autonomous Screening Engine",
               f"- Screened {len(out)} title/abstract records using conservative rules.\n- Included {sum(out.screen_label=='include')}; uncertain {sum(out.screen_label=='uncertain')}; excluded {sum(out.screen_label=='exclude')}.",
               "- results/tables/title_abstract_screening.csv\n- results/tables/full_text_screening.csv",
               "- Human verification of all include/uncertain records remains mandatory.\n- Full-text screening is initialized but not complete.",
               "- Abstract gaps reduce confidence for PubMed/Crossref-only records.",
               "python src/retrieval/assess_full_text.py --config config/review_config.yaml")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/review_config.yaml")
    run(load_config(ap.parse_args().config))
