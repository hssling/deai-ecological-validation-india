"""
Real data ingestion — LASI Wave 1 India State/UT Factsheet (2017-18)
and NFHS-5 Tumkur/Karnataka district data.

Source: D:/Tumkur NPHCE/
These are REAL empirical data from published government surveys.
All outputs labelled: data_source = 'LASI_Wave1_Real' or 'NFHS5_Real'
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parents[2]))
from src.utils.config import get_arg_config
from src.utils.io import save_table
from src.utils.logger import get_logger, log_phase

logger = get_logger("ingest_lasi_real")

LASI_FILE = Path("D:/Tumkur NPHCE/LASI data/LASI_India_State_UT_Factsheet-Final Checked 23.08.22.xls")
NFHS5_TUMKUR = Path("D:/Tumkur NPHCE/external/NFHS-5_KA_Tumkur.csv")

# Mapping: original LASI column → clean variable name
LASI_COLMAP = {
    "Indicators": "state",
    # Demographics
    "60-69 Years of Household population (%)": "pop_60_69_pct",
    "70-79 Years of Household population (%)": "pop_70_79_pct",
    "80+ Years of Household population (%)": "pop_80plus_pct",
    "Death Rate ( per thousand population ) 60 + population2": "death_rate_60plus_per1000",
    # Exposome — SES
    "Literate (%)": "literacy_pct",
    "10 or more years school complete (%)": "education_10plus_pct",
    "Per Capita Annual Household Income (in INR) 12": "per_capita_income_inr",
    "Household Monthly Per Capita Consumption Expenditure (MPCE) in INR 10": "mpce_inr",
    "Households covered by any health insurance (%) 17": "health_insurance_pct",
    # Exposome — built environment / infrastructure
    "Households with electricity (%) ": "electricity_pct",
    "Households using clean cooking fuel (%)7": "clean_fuel_pct",
    "Households exposed to indoor pollution (%)8": "indoor_pollution_pct",
    "Households with improved sanitation (%) 4": "improved_sanitation_pct",
    "Households with improved drinking water source (%)6": "improved_water_pct",
    "Households with pucca house (%)9": "pucca_house_pct",
    # Exposome — lifestyle
    "Currently smoking (%)39": "smoking_pct",
    "Currently consuming tobacco (%)40": "tobacco_pct",
    "Prevalence of heavy episodic drinking (%)41": "heavy_drinking_pct",
    "Physically active (%)42": "physically_active_pct",
    # Outcomes — ageing and frailty
    "Poor Self Rated Health (SRH) (%)45": "poor_srh_pct",
    "Any Activities of Daily Living (ADL) Limitations  (%)71": "adl_limitation_pct",
    "Any Instrumental Activities of Daily Living (IADL) Limitations (%) 72": "iadl_limitation_pct",
    "Persons who need helpers for ADL and IADL limitations (%)73": "need_adl_helper_pct",
    "Mean grip strength in dominant hand (kg)91": "mean_grip_strength_kg",
    "Prevalence of depression based on CIDI-SF (%)78": "depression_cidi_pct",
    "Fall (%)": "fall_pct",
    "Permanent physical disability (%)": "permanent_disability_pct",
    "Mean score for immediate word recall 76": "immediate_word_recall",
    "Mean score of delayed word recall 77": "delayed_word_recall",
    # Multimorbidity components
    "Cardiovascular diseases (CVDs) (%)46": "cvd_pct",
    "Hypertension or high blood pressure (%)": "hypertension_pct",
    "Diabetes or high blood sugar (%)": "diabetes_pct",
    "Chronic lung diseases (%)47": "chronic_lung_pct",
    "Chronic Obstructive Pulmonary Disease (COPD) (%)": "copd_pct",
    "Bone/Joint diseases (%)48": "bone_joint_pct",
    "Anaemia (%)": "anaemia_pct",
    "Depression (%)": "depression_diagnosed_pct",
    "Stroke (%)": "stroke_pct",
    # Anthropometrics
    "Underweight by Anthropometric Indicators\xa0\xa0 (%)88": "underweight_pct",
    "Overweight by Anthropometric Indicators\xa0\xa0(%)88": "overweight_pct",
    "High-risk waist circumference (%)89": "high_waist_pct",
    "Metabolic risk: Prevalence of high-risk waist-hip ratio (%)90": "high_whr_pct",
    # Healthcare utilisation
    "Hospitalization in past 12 months (%)": "hospitalisation_pct",
    "Sought out-patient care in the past 12 months (%)": "outpatient_pct",
}


def build_lasi_state_df() -> pd.DataFrame:
    raw = pd.read_excel(str(LASI_FILE))
    # Rename columns that exist
    rename = {k: v for k, v in LASI_COLMAP.items() if k in raw.columns}
    df = raw.rename(columns=rename)
    df = df[list(rename.values())].copy()

    # Derive multimorbidity index: mean of disease prevalences (scaled 0-100)
    disease_cols = ["cvd_pct", "hypertension_pct", "diabetes_pct",
                    "chronic_lung_pct", "bone_joint_pct", "anaemia_pct",
                    "stroke_pct", "depression_diagnosed_pct"]
    available_disease = [c for c in disease_cols if c in df.columns]
    df[available_disease] = df[available_disease].apply(pd.to_numeric, errors="coerce")
    df["multimorbidity_index"] = df[available_disease].mean(axis=1)

    # Adverse exposome score (knowledge-weighted — higher = more adverse)
    # Direction: clean_fuel (protective→flip), literacy (protective→flip),
    # smoking (adverse), indoor_pollution (adverse), etc.
    for col in ["clean_fuel_pct", "literacy_pct", "improved_sanitation_pct", "improved_water_pct",
                "tobacco_pct", "heavy_drinking_pct", "indoor_pollution_pct", "underweight_pct"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df["adv_indoor_pollution"] = 100 - df.get("clean_fuel_pct", pd.Series([np.nan]*len(df), index=df.index))
    df["adv_literacy"] = 100 - df.get("literacy_pct", pd.Series([np.nan]*len(df), index=df.index))
    df["adv_sanitation"] = 100 - df.get("improved_sanitation_pct", pd.Series([np.nan]*len(df), index=df.index))
    df["adv_water"] = 100 - df.get("improved_water_pct", pd.Series([np.nan]*len(df), index=df.index))

    # Coerce all numeric columns
    for col in df.columns:
        if col != "state":
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Data labels
    df["data_source"] = "LASI_Wave1_Real"
    df["data_type"] = "REAL"
    df["synthetic_flag"] = False

    logger.info(f"LASI state data: {len(df)} states/UTs × {len(df.columns)} cols")
    return df


def build_nfhs5_tumkur_df() -> pd.DataFrame:
    if not NFHS5_TUMKUR.exists():
        return pd.DataFrame()
    raw = pd.read_csv(str(NFHS5_TUMKUR))
    # Pivot to wide format: indicator → column
    pivot = raw.pivot_table(index=["State", "District"],
                            columns="Indicator", values="NFHS5", aggfunc="first")
    pivot.columns = [c[:60] for c in pivot.columns]
    pivot = pivot.reset_index()
    pivot["data_source"] = "NFHS5_Tumkur_Real"
    pivot["data_type"] = "REAL"
    pivot["synthetic_flag"] = False
    return pivot


def run(cfg: dict) -> dict:
    proc_dir: Path = cfg["paths"]["data_processed"]

    # --- LASI state-level data ---
    lasi_df = build_lasi_state_df()
    save_table(lasi_df, proc_dir / "lasi_state_real.parquet")
    save_table(lasi_df, cfg["paths"]["results_tables"] / "lasi_state_real.csv")
    logger.info(f"LASI real data saved: {len(lasi_df)} rows")

    # --- NFHS-5 Tumkur ---
    tumkur_df = build_nfhs5_tumkur_df()
    if not tumkur_df.empty:
        # Deduplicate column names before saving
        tumkur_df.columns = pd.io.common.dedup_names(
            tumkur_df.columns.tolist(), is_potential_multiindex=False
        ) if hasattr(pd.io.common, 'dedup_names') else tumkur_df.loc[:, ~tumkur_df.columns.duplicated()].columns
        tumkur_df = tumkur_df.loc[:, ~tumkur_df.columns.duplicated()]
        save_table(tumkur_df, proc_dir / "nfhs5_tumkur_real.parquet")
        logger.info(f"NFHS-5 Tumkur real data saved: {len(tumkur_df)} rows")

    log_phase(
        "Phase 2b — Real Data Ingestion (LASI + NFHS-5)", "COMPLETE",
        f"LASI: {len(lasi_df)} states/UTs × {len(lasi_df.columns)} variables\n"
        f"NFHS-5 Tumkur: {len(tumkur_df)} rows\n"
        f"Data source: D:/Tumkur NPHCE/\n"
        f"Data type: REAL — LASI Wave 1 India factsheet (IIPS 2022)",
        log_dir=cfg["paths"]["logs"],
    )
    return {"lasi_rows": len(lasi_df), "nfhs5_tumkur_rows": len(tumkur_df)}


if __name__ == "__main__":
    run(get_arg_config())
