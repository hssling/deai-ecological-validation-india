from __future__ import annotations
import argparse
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from src.utils.io import load_config, append_log

def save(fig, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)

def run(cfg):
    figs = cfg["paths"]["results_figures"]
    rt = cfg["paths"]["results_tables"]
    scores = pd.read_csv(rt / "intervention_evidence_scores.csv")
    ranking_path = rt / "intervention_credibility_ranking.csv"
    ranking = pd.read_csv(ranking_path) if ranking_path.exists() else pd.DataFrame()
    screen = pd.read_csv(cfg["paths"]["results_tables"] / "title_abstract_screening.csv")
    mech = pd.read_csv(cfg["paths"]["results_tables"] / "intervention_mechanism_map.csv")
    # PRISMA
    counts = {"Raw": len(pd.read_csv(cfg["paths"]["results_tables"] / "raw_records_all.csv")),
              "Dedup": len(pd.read_csv(cfg["paths"]["results_tables"] / "master_records_dedup.csv")),
              "Include/uncertain": int(sum(screen.screen_label.isin(["include","uncertain"]))),
              "Extracted pilot": len(pd.read_csv(cfg["paths"]["results_tables"] / "extracted_studies_master.csv"))}
    fig, ax = plt.subplots(figsize=(7,4))
    ax.axis("off")
    y = 0.9
    for k,v in counts.items():
        ax.text(0.5,y,f"{k}\nN={v}",ha="center",va="center",bbox=dict(boxstyle="round",fc="#eef",ec="#447"))
        y -= 0.22
    save(fig, figs / "prisma_flow.png")
    # Score ranking
    if not scores.empty:
        fig, ax = plt.subplots(figsize=(8,5))
        s = scores.sort_values("max_claim_score", ascending=True)
        ax.barh(s["intervention_name"], s["max_claim_score"], color="#49759c")
        ax.set_xlabel("Max claim credibility score")
        ax.set_title("Intervention evidence score ranking")
        save(fig, figs / "evidence_score_ranking.png")
    # Heatmap
    vote = pd.read_csv(cfg["paths"]["results_tables"] / "structured_vote_counting.csv")
    if not vote.empty:
        mat = vote.pivot_table(index="intervention_name", columns="ageing_domain_category", values="n_candidate_records", fill_value=0)
        fig, ax = plt.subplots(figsize=(9,6))
        sns.heatmap(mat, annot=True, fmt=".0f", cmap="Blues", ax=ax)
        ax.set_title("Intervention vs outcome-domain evidence map")
        save(fig, figs / "intervention_outcome_heatmap.png")
    # Mechanism network
    if not mech.empty:
        G = nx.Graph()
        for _, r in mech.iterrows():
            G.add_edge(r["intervention"], r["mechanism"])
        fig, ax = plt.subplots(figsize=(10,8))
        nx.draw_networkx(G, ax=ax, node_size=500, font_size=7, with_labels=True)
        ax.axis("off")
        save(fig, figs / "mechanism_network.png")
    # Hype versus evidence map
    topics = pd.read_csv(cfg["paths"]["results_tables"] / "topic_assignments.csv")
    if not ranking.empty and {"credibility_score", "hype_rate", "intervention_name"}.issubset(ranking.columns):
        fig, ax = plt.subplots(figsize=(9,6))
        sns.scatterplot(
            data=ranking,
            x="credibility_score",
            y="hype_rate",
            hue="credibility_tier",
            size="n_extracted_records",
            sizes=(60, 360),
            ax=ax,
        )
        for _, row in ranking.iterrows():
            ax.text(row["credibility_score"] + 0.05, row["hype_rate"] + 0.005, row["intervention_name"], fontsize=7)
        ax.axhline(0.1, color="#999999", lw=0.8, ls="--")
        ax.set_xlabel("Credibility score from extracted repo evidence")
        ax.set_ylabel("Hype-flagged record rate")
        ax.set_title("Hype versus evidence by intervention class")
        ax.legend(loc="best", fontsize=7)
        save(fig, figs / "hype_vs_evidence_map.png")
    else:
        fig, ax = plt.subplots(figsize=(7,5))
        ax.scatter(topics["hype_terms_n"], topics.index, alpha=0.5)
        ax.set_xlabel("Hype term count")
        ax.set_ylabel("Candidate record index")
        ax.set_title("Hype-language flag map")
        save(fig, figs / "hype_vs_evidence_map.png")
    # Evidence pyramid
    fig, ax = plt.subplots(figsize=(6,5))
    levels = ["Human RCT","Human observational","Animal","Cellular","Speculative"]
    widths = [2,3,4,5,6]
    for i,(lvl,w) in enumerate(zip(levels,widths)):
        ax.barh(i,w,left=(6-w)/2,color=sns.color_palette("viridis",5)[i])
        ax.text(3,i,lvl,ha="center",va="center",color="white")
    ax.axis("off"); ax.set_title("Anti-ageing evidence pyramid")
    save(fig, figs / "evidence_pyramid.png")
    # Translational matrix
    if not ranking.empty:
        trans = ranking[[
            "intervention_name",
            "credibility_tier",
            "credibility_score",
            "human_records",
            "human_trial_records",
            "healthspan_records",
            "hard_ageing_records",
            "biomarker_records",
            "hype_rate",
        ]].copy()
        trans["translational_category"] = trans["credibility_tier"].map({
            "highest_current_human_healthspan_signal": "A_healthspan_support_signal",
            "human_signal_requires_verification": "B_promising_not_recommendation_ready",
            "biomarker_or_indirect_human_signal": "C_biomarker_or_indirect",
            "preclinical_direct_ageing_signal": "C_preclinical_direct_ageing",
            "low_directness_or_speculative": "D_speculative_or_low_directness",
        }).fillna("D_speculative_or_low_directness")
        trans.to_csv(cfg["paths"]["results_tables"] / "translational_readiness.csv", index=False)
        fig, ax = plt.subplots(figsize=(9,6))
        sns.scatterplot(
            data=trans,
            x="credibility_score",
            y="intervention_name",
            hue="translational_category",
            size="human_records",
            sizes=(50, 320),
            ax=ax,
        )
        ax.set_xlabel("Credibility score from extracted repo evidence")
        ax.set_ylabel("")
        ax.set_title("Translational readiness matrix")
        ax.legend(loc="best", fontsize=7)
        save(fig, figs / "translational_matrix.png")
    elif not scores.empty:
        trans = scores[["intervention_name","classification","max_claim_score"]].copy()
        trans.to_csv(cfg["paths"]["results_tables"] / "translational_readiness.csv", index=False)
        fig, ax = plt.subplots(figsize=(8,5))
        sns.scatterplot(data=trans, x="max_claim_score", y="intervention_name", hue="classification", ax=ax)
        ax.set_title("Translational readiness matrix")
        save(fig, figs / "translational_matrix.png")
    # Timeline simple
    ex = pd.read_csv(cfg["paths"]["results_tables"] / "extracted_studies_master.csv")
    if "year" in ex and not ex.empty:
        yy = pd.to_numeric(ex["year"], errors="coerce").dropna().astype(int)
        fig, ax = plt.subplots(figsize=(8,4))
        yy.value_counts().sort_index().plot(kind="bar", ax=ax)
        ax.set_title("Timeline of candidate anti-ageing evidence")
        ax.set_ylabel("Records")
        save(fig, figs / "evidence_timeline.png")
    append_log(cfg["paths"]["logs"] / "progress.md", "Phase 14 - Mandatory Figures",
               "- Generated PRISMA, evidence pyramid, heatmap, mechanism network, evidence ranking, hype map, timeline, and translational matrix where data permitted.",
               "- results/figures/*.png",
               "- Figure styling should be refined before journal submission.",
               "- Some figures are pilot metadata maps, not final full-text synthesis figures.",
               "python src/write_manuscript.py --config config/review_config.yaml")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/review_config.yaml")
    run(load_config(ap.parse_args().config))
