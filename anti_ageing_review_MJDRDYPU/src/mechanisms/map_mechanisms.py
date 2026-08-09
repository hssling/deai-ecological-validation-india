from __future__ import annotations
import argparse
import pandas as pd
from src.utils.io import load_config, save_csv, append_log

def run(cfg):
    ex = pd.read_csv(cfg["paths"]["results_tables"] / "extracted_studies_master.csv")
    rows = []
    for _, r in ex.iterrows():
        for m in str(r.get("mechanism","unclear")).split("; "):
            rows.append({"intervention":r.get("intervention_name","unclear"),"mechanism":m,"directness":r.get("mechanism_directness","inferred"),"species_model":r.get("species_model","unclear"),"title":r.get("title","")})
    mp = pd.DataFrame(rows)
    mat = pd.crosstab(mp["intervention"], mp["mechanism"]).reset_index() if not mp.empty else pd.DataFrame()
    save_csv(mp, cfg["paths"]["results_tables"] / "intervention_mechanism_map.csv")
    save_csv(mat, cfg["paths"]["results_tables"] / "mechanism_evidence_matrix.csv")
    append_log(cfg["paths"]["logs"] / "progress.md", "Phase 9 - Mechanistic Mapping",
               f"- Mapped {len(mp)} intervention-mechanism edges.",
               "- results/tables/intervention_mechanism_map.csv\n- results/tables/mechanism_evidence_matrix.csv",
               "- Direct/inferred mechanism labels require full-text verification.",
               "- Mechanism mapping from abstracts may miss measured pathways.",
               "python src/nlp/topic_hype.py --config config/review_config.yaml")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/review_config.yaml")
    run(load_config(ap.parse_args().config))
