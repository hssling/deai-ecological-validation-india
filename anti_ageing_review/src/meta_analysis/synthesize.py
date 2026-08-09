from __future__ import annotations
import argparse
import pandas as pd
from src.utils.io import load_config, save_csv, append_log

def run(cfg):
    ex = pd.read_csv(cfg["paths"]["results_tables"] / "extracted_studies_master.csv")
    inputs = ex[["title","intervention_name","ageing_domain_category","effect_size","uncertainty_measure","effect_direction"]].copy()
    inputs["meta_ready"] = False
    inputs["reason_not_meta_ready"] = "Effect sizes not extracted from full text in pilot metadata pass"
    results = pd.DataFrame([{"analysis":"none_pilot","n_studies":0,"pooled_effect":"","heterogeneity":"","note":"No quantitative meta-analysis performed because comparable effect sizes require full-text extraction."}])
    vote = ex.groupby(["intervention_name","ageing_domain_category"]).size().reset_index(name="n_candidate_records") if not ex.empty else pd.DataFrame()
    save_csv(inputs, cfg["paths"]["results_tables"] / "meta_analysis_inputs.csv")
    save_csv(results, cfg["paths"]["results_tables"] / "meta_analysis_results.csv")
    save_csv(vote, cfg["paths"]["results_tables"] / "structured_vote_counting.csv")
    append_log(cfg["paths"]["logs"] / "progress.md", "Phase 11 - Meta-analysis / Quantitative Synthesis",
               "- Created meta-analysis readiness table.\n- Deferred pooling because effect sizes require full-text extraction.",
               "- results/tables/meta_analysis_inputs.csv\n- results/tables/meta_analysis_results.csv\n- results/tables/structured_vote_counting.csv",
               "- Full-text extraction of effect sizes is required before any pooled estimate.",
               "- Vote counting is descriptive and should not be overinterpreted.",
               "python src/viz/make_figures.py --config config/review_config.yaml")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/review_config.yaml")
    run(load_config(ap.parse_args().config))
