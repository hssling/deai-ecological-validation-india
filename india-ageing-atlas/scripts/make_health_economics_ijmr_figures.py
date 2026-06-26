"""Two extra figures for the IJMR version: state ranking and demographic projection."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

T = Path("outputs/health_economics_mjdrdypu/tables")
F = Path("outputs/health_economics_mjdrdypu/figures"); F.mkdir(parents=True, exist_ok=True)
BLUE, ORANGE, GREEN = "#0072B2", "#D55E00", "#009E73"


def fig_state():
    d = pd.read_csv(T / "table_state_che.csv").sort_values("che40cap")
    fig, ax = plt.subplots(figsize=(8, 9))
    y = np.arange(len(d))
    ax.barh(y, d["che40cap"], color=BLUE)
    ax.set_yticks(y); ax.set_yticklabels(d["state"], fontsize=8)
    ax.axvline(20.7, color=ORANGE, ls="--", lw=1.5, label="National 60+ average (20.7%)")
    ax.set_xlabel("Households with catastrophic health spending (>40% of capacity to pay), %")
    ax.set_title("Catastrophic health spending among older adults, by State/UT")
    ax.legend(loc="lower right", fontsize=9)
    for yi, v in zip(y, d["che40cap"]):
        ax.text(v + 0.3, yi, f"{v:.1f}", va="center", fontsize=7)
    fig.tight_layout(); fig.savefig(F / "fig7_state_che_ranking.png", dpi=600, bbox_inches="tight"); plt.close(fig)
    print("saved fig7_state_che_ranking.png")


def fig_projections():
    d = pd.read_csv(T / "table_projections.csv")
    fig, ax1 = plt.subplots(figsize=(8, 5.5))
    x = np.arange(len(d)); wx = 0.38
    b1 = ax1.bar(x - wx/2, d["che40_caseload_million"], wx, color=BLUE, label="Older adults in catastrophic-spending households (million)")
    ax1.set_ylabel("Older adults in catastrophic-spending households (million)", color=BLUE, fontsize=10)
    ax1.set_xticks(x); ax1.set_xticklabels([f"{int(y)}\n({int(p)}M aged 60+)" for y, p in zip(d["year"], d["pop_60plus_million"])])
    ax1.tick_params(axis="y", labelcolor=BLUE)
    for xi, v in zip(x - wx/2, d["che40_caseload_million"]):
        ax1.text(xi, v + 0.8, f"{v:.0f}M", ha="center", fontsize=9, color=BLUE)
    ax2 = ax1.twinx()
    ax2.bar(x + wx/2, d["outpatient_cover_cost_lakh_cr"], wx, color=ORANGE, label="Annual cost of outpatient cover (Rs lakh crore)")
    ax2.set_ylabel("Annual cost of outpatient/medicine cover (Rs lakh crore)", color=ORANGE, fontsize=10)
    ax2.tick_params(axis="y", labelcolor=ORANGE)
    for xi, v in zip(x + wx/2, d["outpatient_cover_cost_lakh_cr"]):
        ax2.text(xi, v + 0.1, f"{v:.2f}", ha="center", fontsize=9, color=ORANGE)
    ax1.set_title("Projected catastrophic-spending burden and cost of action, 2022-2050\n(catastrophic-spending rate held at the 2017-18 level)")
    fig.tight_layout(); fig.savefig(F / "fig8_projections.png", dpi=600, bbox_inches="tight"); plt.close(fig)
    print("saved fig8_projections.png")


if __name__ == "__main__":
    fig_state(); fig_projections()
