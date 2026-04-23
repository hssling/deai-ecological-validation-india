from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_NOTEBOOK = ROOT / "kaggle" / "kernel" / "deai_ecological_validation_public.ipynb"


def markdown_cell(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": text.splitlines(keepends=True),
    }


def code_cell(text: str) -> dict:
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": text.splitlines(keepends=True),
    }


def main() -> None:
    cells = [
        markdown_cell(
            "# DEAI Ecological Validation Notebook\n\n"
            "This notebook accompanies the public release for the manuscript "
            "`Development and ecological validation of a digital exposome ageing index for healthy ageing surveillance in India using LASI Wave 1`.\n\n"
            "It reads the released derived tables, reproduces the main descriptive summaries, and restates the methodological boundary of the index."
        ),
        markdown_cell(
            "## Scientific boundary\n\n"
            "DEAI is a state-level ecological surveillance index. It is not an individual-level biological-age measure, clinical prediction score, or causal model."
        ),
        code_cell(
            "import pandas as pd\n"
            "from pathlib import Path\n\n"
            "DATA_ROOT = Path('/kaggle/input/deai-healthy-ageing-india-lasi-wave1')\n"
            "TABLES = DATA_ROOT / 'tables'\n"
            "FIGURES = DATA_ROOT / 'figures'\n\n"
            "rank = pd.read_csv(TABLES / 'deai_real_state_rankings.csv')\n"
            "robust = pd.read_csv(TABLES / 'deai_real_robustness.csv')\n"
            "components = pd.read_csv(TABLES / 'deai_component_diagnostics.csv')\n"
            "lasi = pd.read_csv(TABLES / 'lasi_with_deai_real.csv')\n\n"
            "rank.head()"
        ),
        markdown_cell("## Highest adverse DEAI burden"),
        code_cell("rank.head(10)"),
        markdown_cell("## Main robustness outputs"),
        code_cell(
            "robust[['outcome_label', 'rho_states_only', 'p_states_only', "
            "'bootstrap95_low_states_only', 'bootstrap95_high_states_only', "
            "'bh_q_states_only', 'robust_direction']]"
        ),
        markdown_cell("## Component diagnostics"),
        code_cell("components.sort_values('spearman_with_deai', ascending=False)"),
        markdown_cell(
            "## Karnataka profile\n\n"
            "The manuscript highlights Karnataka as a state-level contextual comparison with the India aggregate row."
        ),
        code_cell(
            "lasi[lasi['state'].isin(['Karnataka', 'INDIA'])][['state', 'deai_real_z', "
            "'death_rate_60plus_per1000', 'poor_srh_pct', 'iadl_limitation_pct', "
            "'multimorbidity_index']]"
        ),
        markdown_cell(
            "## Public release files\n\n"
            "The accompanying dataset also contains manuscript figures, manuscript assets, and reproducibility scripts."
        ),
    ]

    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.11",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    OUT_NOTEBOOK.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTEBOOK.write_text(json.dumps(notebook, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
