"""Phase 11: reproducible figures for current honest evidence state."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
sys.path.insert(0, str(Path(__file__).parent))
from _common import ensure_dirs, load_config, log  # noqa: E402


def run(cfg):
    freeze = cfg["project"]["freeze_date"]
    figs = Path(cfg["paths"]["results_figs"]); proc = Path(cfg["paths"]["data_processed"])
    ensure_dirs(figs)
    raw = pd.read_csv(Path(cfg["paths"]["data_interim"]) / f"raw_records_dnam_{freeze}.csv")
    cand = pd.read_csv(Path(cfg["paths"]["data_interim"]) / f"candidate_pool_{freeze}.csv")
    included = pd.read_csv(proc / f"included_studies_{freeze}.csv")
    extracted = pd.read_csv(proc / f"extracted_clock_studies_{freeze}.csv").fillna("")
    effects = pd.read_csv(Path(cfg["paths"]["results_tabs"]) / f"effect_size_candidates_{freeze}.csv").fillna("")

    labels = ["Raw records", "Candidate pool", "Included pending FT", "Clock rows", "Calculable effects"]
    vals = [len(raw), len(cand), len(included), len(extracted), int(effects["effect_status"].eq("calculated_candidate").sum())]
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.bar(labels, vals, color=["#475569", "#2563eb", "#0f766e", "#f97316", "#dc2626"])
    ax.set_ylabel("Count")
    ax.set_title("DNAm clocks review evidence pipeline status")
    ax.tick_params(axis="x", rotation=25)
    for i, v in enumerate(vals):
        ax.text(i, v, str(v), ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    fig.savefig(figs / f"pipeline_status_{freeze}.png", dpi=300)
    plt.close(fig)

    status = extracted["extraction_status"].value_counts().reset_index()
    status.columns = ["status", "n"]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(status["n"], labels=status["status"], autopct="%1.0f%%", startangle=90)
    ax.set_title("Numeric extraction status")
    fig.tight_layout()
    fig.savefig(figs / f"extraction_status_{freeze}.png", dpi=300)
    plt.close(fig)
    log("figures_done", figures=2)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True)
    run(load_config(ap.parse_args().config))
