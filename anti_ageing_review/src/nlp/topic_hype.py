from __future__ import annotations
import argparse
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from src.utils.io import load_config, save_csv, append_log

HYPE = ["reversal","reverse","rejuvenation","breakthrough","young plasma","immortality","cure","anti-aging","anti-ageing"]

def run(cfg):
    s = pd.read_csv(cfg["paths"]["results_tables"] / "title_abstract_screening.csv")
    cand = s[s["screen_label"].isin(["include","uncertain"])].copy()
    texts = (cand["title"].fillna("") + " " + cand["abstract"].fillna("")).tolist()
    if len(cand) >= 4:
        X = TfidfVectorizer(max_features=800, stop_words="english").fit_transform(texts)
        k = min(8, max(2, len(cand)//10))
        cand["topic_cluster"] = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(X)
    else:
        cand["topic_cluster"] = 0
    cand["hype_terms_n"] = [sum(h in t.lower() for h in HYPE) for t in texts]
    cand["hype_flag"] = cand["hype_terms_n"] > 0
    save_csv(cand[["title","intervention_classes","outcome_terms","topic_cluster","hype_terms_n","hype_flag","screen_label"]], cfg["paths"]["results_tables"] / "topic_assignments.csv")
    summary = cand.groupby("topic_cluster").agg(n=("title","count"), hype_rate=("hype_flag","mean")).reset_index()
    save_csv(summary, cfg["paths"]["results_tables"] / "hype_topic_summary.csv")
    (cfg["paths"]["docs"] / "nlp_summary.md").write_text("# NLP Summary\n\nTopic clustering and hype flags are metadata-assisted. Hype terms flag language needing skeptical review; they do not prove poor science.\n", encoding="utf-8")
    append_log(cfg["paths"]["logs"] / "progress.md", "Phase 10 - NLP/Text Mining Augmentation",
               f"- Assigned topic clusters and hype flags to {len(cand)} records.",
               "- results/tables/topic_assignments.csv\n- results/tables/hype_topic_summary.csv\n- docs/nlp_summary.md",
               "- Embedding-based clustering can be added later.",
               "- Hype detection is lexical and preliminary.",
               "python src/meta_analysis/synthesize.py --config config/review_config.yaml")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/review_config.yaml")
    run(load_config(ap.parse_args().config))
