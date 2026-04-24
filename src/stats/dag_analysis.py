"""
Phase 8 — DAG Concept Figure

Generates a conceptual Directed Acyclic Graph (DAG) illustrating assumed
causal pathways between exposome domains, biological ageing mediators,
and ageing-related outcomes.

This is a conceptual/qualitative DAG — not an empirically estimated
structural equation model.  The DAG is used to:
  1. Justify covariate selection (block confounders, open mediator paths)
  2. Communicate assumed causal structure transparently
  3. Identify potential sources of collider bias

Outputs: results/figures/dag_concept.png
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

sys.path.insert(0, str(Path(__file__).parents[2]))
from src.utils.config import get_arg_config
from src.utils.io import save_figure
from src.utils.logger import get_logger

logger = get_logger("dag_analysis")


NODE_POSITIONS = {
    # Upstream: Structural determinants
    "SES / Education": (-3.0, 1.5),
    "Region / Urbanicity": (-3.0, 0.0),
    "Sex": (-3.0, -1.5),
    # Exposome
    "Air Pollution\n(PM2.5)": (-1.0, 2.5),
    "Heat Stress": (-1.0, 1.0),
    "Tobacco Use": (-1.0, -0.5),
    "Diet Quality": (-1.0, -2.0),
    # DEAI composite
    "DEAI Score": (1.0, 0.5),
    # Biological mediators
    "Inflammageing\n(IL-6, NF-κB)": (2.5, 2.0),
    "Oxidative Stress\n(ROS)": (2.5, 0.5),
    "Cellular Senescence\n(SASP)": (2.5, -1.0),
    # Outcomes
    "Frailty": (4.5, 2.5),
    "Multi-\nmorbidity": (4.5, 1.0),
    "Disability\n(ADL)": (4.5, -0.5),
    "Mortality\nRisk": (4.5, -2.0),
}

EDGES = [
    # Structural → Exposome
    ("SES / Education", "Air Pollution\n(PM2.5)", "black"),
    ("SES / Education", "Tobacco Use", "black"),
    ("SES / Education", "Diet Quality", "black"),
    ("Region / Urbanicity", "Air Pollution\n(PM2.5)", "black"),
    ("Region / Urbanicity", "Heat Stress", "black"),
    ("Sex", "Tobacco Use", "black"),
    # Exposome → DEAI
    ("Air Pollution\n(PM2.5)", "DEAI Score", "#e74c3c"),
    ("Heat Stress", "DEAI Score", "#e74c3c"),
    ("Tobacco Use", "DEAI Score", "#e74c3c"),
    ("Diet Quality", "DEAI Score", "#e74c3c"),
    # DEAI → Biological mediators (dashed = observationally inferred)
    ("DEAI Score", "Inflammageing\n(IL-6, NF-κB)", "#8e44ad"),
    ("DEAI Score", "Oxidative Stress\n(ROS)", "#8e44ad"),
    ("DEAI Score", "Cellular Senescence\n(SASP)", "#8e44ad"),
    # Biological mediators → Outcomes
    ("Inflammageing\n(IL-6, NF-κB)", "Frailty", "#27ae60"),
    ("Inflammageing\n(IL-6, NF-κB)", "Multi-\nmorbidity", "#27ae60"),
    ("Oxidative Stress\n(ROS)", "Frailty", "#27ae60"),
    ("Oxidative Stress\n(ROS)", "Disability\n(ADL)", "#27ae60"),
    ("Cellular Senescence\n(SASP)", "Frailty", "#27ae60"),
    ("Cellular Senescence\n(SASP)", "Mortality\nRisk", "#27ae60"),
    # Direct SES → Outcomes (residual confounding path)
    ("SES / Education", "Frailty", "grey"),
    ("Sex", "Frailty", "grey"),
]

DASHED_EDGES = {
    ("DEAI Score", "Inflammageing\n(IL-6, NF-κB)"),
    ("DEAI Score", "Oxidative Stress\n(ROS)"),
    ("DEAI Score", "Cellular Senescence\n(SASP)"),
}

NODE_COLORS = {
    "SES / Education": "#bdc3c7",
    "Region / Urbanicity": "#bdc3c7",
    "Sex": "#bdc3c7",
    "Air Pollution\n(PM2.5)": "#fadbd8",
    "Heat Stress": "#fadbd8",
    "Tobacco Use": "#fadbd8",
    "Diet Quality": "#fadbd8",
    "DEAI Score": "#d5e8d4",
    "Inflammageing\n(IL-6, NF-κB)": "#e8daef",
    "Oxidative Stress\n(ROS)": "#e8daef",
    "Cellular Senescence\n(SASP)": "#e8daef",
    "Frailty": "#fef3cd",
    "Multi-\nmorbidity": "#fef3cd",
    "Disability\n(ADL)": "#fef3cd",
    "Mortality\nRisk": "#fef3cd",
}


def run(cfg: dict) -> None:
    fig, ax = plt.subplots(figsize=(18, 10))
    ax.set_xlim(-4.2, 5.8)
    ax.set_ylim(-3.0, 3.5)
    ax.axis("off")

    # Draw edges
    for src, dst, color in EDGES:
        x0, y0 = NODE_POSITIONS[src]
        x1, y1 = NODE_POSITIONS[dst]
        lw = 1.5
        ls = "--" if (src, dst) in DASHED_EDGES else "-"
        ax.annotate(
            "", xy=(x1, y1), xytext=(x0, y0),
            arrowprops=dict(
                arrowstyle="-|>", color=color, lw=lw,
                linestyle=ls,
                connectionstyle="arc3,rad=0.0",
            ),
        )

    # Draw nodes
    for node, (x, y) in NODE_POSITIONS.items():
        color = NODE_COLORS.get(node, "#ecf0f1")
        ax.text(
            x, y, node,
            ha="center", va="center", fontsize=8.5, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", facecolor=color, edgecolor="#7f8c8d", lw=1.2),
        )

    # Column labels
    for label, x in [("Structural\nDeterminants", -3.0), ("Exposome\nDomains", -1.0),
                     ("DEAI\nComposite", 1.0), ("Biological\nMediators\n(Omics)", 2.5),
                     ("Ageing\nOutcomes", 4.5)]:
        ax.text(x, 3.3, label, ha="center", va="bottom", fontsize=9,
                color="#2c3e50", fontstyle="italic")

    # Legend
    legend_elements = [
        mpatches.Patch(facecolor="#bdc3c7", label="Structural determinants"),
        mpatches.Patch(facecolor="#fadbd8", label="Exposome inputs"),
        mpatches.Patch(facecolor="#d5e8d4", label="DEAI composite"),
        mpatches.Patch(facecolor="#e8daef", label="Biological mediators"),
        mpatches.Patch(facecolor="#fef3cd", label="Ageing outcomes"),
        mpatches.Patch(facecolor="none", edgecolor="grey", label="Confounding path"),
        plt.Line2D([0], [0], color="#8e44ad", lw=1.5, linestyle="--",
                   label="Triangulated (omics)"),
    ]
    ax.legend(handles=legend_elements, loc="lower left", fontsize=8, framealpha=0.9)

    ax.set_title(
        "Conceptual Directed Acyclic Graph (DAG) — DEAI Pipeline\n"
        "Dashed arrows = observationally inferred / omics triangulation paths",
        fontsize=11, fontweight="bold", pad=10,
    )

    save_figure(fig, cfg["paths"]["results_figures"] / "dag_concept.png")
    plt.close(fig)
    logger.info("DAG concept figure saved")


if __name__ == "__main__":
    run(get_arg_config())
