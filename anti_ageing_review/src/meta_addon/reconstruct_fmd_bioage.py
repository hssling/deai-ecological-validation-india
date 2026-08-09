from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.utils.io import append_log, load_config, save_csv


LEVINE_PARAMS = {
    "albumin": {"s": 0.334481, "k": -0.00544, "q": 4.423451},
    "alp": {"s": 29.44492, "k": 0.443863, "q": 60.44123},
    "creat": {"s": 0.271155, "k": 0.003463, "q": 0.908423},
    "crp": {"s": 0.615577, "k": 0.004941, "q": 0.179063},
    "hba1c": {"s": 0.943548, "k": 0.017761, "q": 4.5679},
    "sbp": {"s": 14.94318, "k": 0.677014, "q": 90.99925},
    "totchol": {"s": 40.3238, "k": 0.793224, "q": 170.8787},
}

# Approximated from NHANES III training with the same Levine/KDM biomarker family.
S_BA2_APPROX = 1244.6012340103853


def parse_bio_sheet(path: Path, sheet: str) -> pd.DataFrame:
    raw = pd.read_excel(path, sheet_name=sheet, header=None)
    df = raw.iloc[4:, :13].copy()
    df.columns = [
        "ID",
        "albumin_bl",
        "albumin_fu",
        "alp_bl",
        "alp_fu",
        "creat_bl",
        "creat_fu",
        "crp_bl",
        "crp_fu",
        "sbp_bl",
        "sbp_fu",
        "totchol_bl",
        "totchol_fu",
    ]
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=["ID"]).copy()


def compute_change(df: pd.DataFrame) -> pd.DataFrame:
    biomarkers = list(LEVINE_PARAMS)
    ba_denom = sum((LEVINE_PARAMS[b]["k"] / LEVINE_PARAMS[b]["s"]) ** 2 for b in biomarkers) + (1 / S_BA2_APPROX)
    rows: list[dict[str, object]] = []
    for _, row in df.iterrows():
        components = []
        for biomarker in ["albumin", "alp", "creat", "crp", "sbp", "totchol"]:
            baseline = row[f"{biomarker}_bl"]
            follow_up = row[f"{biomarker}_fu"]
            if pd.notna(baseline) and pd.notna(follow_up):
                params = LEVINE_PARAMS[biomarker]
                delta_component = ((follow_up - params["q"]) - (baseline - params["q"])) * (
                    params["k"] / (params["s"] ** 2)
                )
                components.append(delta_component)
        if components:
            delta_bioage = (sum(components) * (len(biomarkers) / len(components))) / ba_denom
            rows.append(
                {
                    "ID": int(row["ID"]),
                    "n_available_biomarkers": len(components),
                    "delta_bioage_reconstructed": delta_bioage,
                }
            )
    return pd.DataFrame(rows)


def summarise(group: str, cohort: str, df: pd.DataFrame) -> dict[str, object]:
    return {
        "study_group": group,
        "cohort": cohort,
        "n": len(df),
        "mean_delta_bioage_reconstructed": df["delta_bioage_reconstructed"].mean(),
        "sd_delta_bioage_reconstructed": df["delta_bioage_reconstructed"].std(ddof=1),
        "median_delta_bioage_reconstructed": df["delta_bioage_reconstructed"].median(),
        "q1_delta_bioage_reconstructed": df["delta_bioage_reconstructed"].quantile(0.25),
        "q3_delta_bioage_reconstructed": df["delta_bioage_reconstructed"].quantile(0.75),
    }


def run(cfg: dict) -> None:
    cache = cfg["paths"]["data_processed"] / "open_text_cache"
    tables = cfg["paths"]["meta_addon_tables"]
    workbook = cache / "fmd_source_data.xlsx"

    sheet_map = {
        "NCT02158897_data_BioAge_FMD": ("NCT02158897", "FMD"),
        "NCT02158897_data_BioAge_CTRL": ("NCT02158897", "Control"),
        "NCT04150159_data_BioAge_FMD": ("NCT04150159", "FMD"),
    }

    person_frames = []
    summaries = []
    for sheet, (study_group, cohort) in sheet_map.items():
        parsed = parse_bio_sheet(workbook, sheet)
        changes = compute_change(parsed)
        if changes.empty:
            continue
        changes["study_group"] = study_group
        changes["cohort"] = cohort
        changes["reconstruction_basis"] = "6_of_7_levine_biomarkers_hba1c_missing"
        person_frames.append(changes)
        summaries.append(summarise(study_group, cohort, changes))

    person_level = pd.concat(person_frames, ignore_index=True)
    summary = pd.DataFrame(summaries)

    save_csv(person_level, tables / "fmd_bioage_reconstruction_person_level.csv")
    save_csv(summary, tables / "fmd_bioage_reconstruction_summary.csv")

    append_log(
        cfg["paths"]["logs"] / "progress.md",
        "Phase 25 - FMD biological-age reconstruction",
        "- Reconstructed participant-level change scores for the FMD biological-age endpoint from the official figshare workbook.\n- Used the published Levine biological-age q/k/s parameters and an NHANES-derived variance constant approximation.\n- Kept the reconstruction separate from the primary pooling dataset because cohort-wide HbA1c was absent from the workbook.",
        "- results/meta_addon/tables/fmd_bioage_reconstruction_person_level.csv\n- results/meta_addon/tables/fmd_bioage_reconstruction_summary.csv",
        "- Continue searching for the exact original code or full seven-biomarker source values if a publication-grade FMD effect estimate is needed.\n- Keep reconstructed FMD values out of primary pooled analyses unless the missing biomarker issue is resolved.",
        "- This reconstruction uses 6 of the 7 biomarkers named in the paper and therefore should be treated as sensitivity analysis only.\n- The NHANES-derived variance constant is reproduced from the same method family but is not confirmed against the authors' exact implementation.",
        "python -m src.meta_addon.reconstruct_fmd_bioage --config config/meta_addon_config.yaml",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/meta_addon_config.yaml")
    run(load_config(parser.parse_args().config))
