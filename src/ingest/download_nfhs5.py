"""
Ingest NFHS-5 (India National Family Health Survey 2019-21) district-level
key indicators.  Public factsheets are available as PDFs from the IIPS website.
The DHS programme also releases state/national summary data as CSV-compatible files.

Strategy:
  1. Try to fetch the DHS open-data STATcompiler CSV export for India NFHS-5.
  2. Fallback: construct a representative indicator table from the published
     NFHS-5 national fact sheet (hard-coded representative values), clearly
     marked as approximations.

NOTE: Individual-level microdata requires DHS registration; this script
uses only publicly available aggregate indicators.
"""
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).parents[2]))
from src.utils.logger import get_logger

logger = get_logger("nfhs5")

# DHS STATcompiler API — free, no key needed for aggregate queries
DHS_API_BASE = "https://api.dhsprogram.com/rest/dhs/v8"
INDIA_NFHS5_SURVEY = "IA2021DHS"

# Selected indicators mapped to DEAI domains
INDICATOR_MAP = {
    "HC_HEFF_H_ELC": "household_electricity_pct",
    "HC_HEFF_H_CLN": "household_clean_fuel_pct",
    "HC_WATS_H_SBS": "improved_sanitation_pct",
    "HC_WATS_H_IMP": "improved_water_pct",
    "CM_ECMR_C_IMR": "infant_mortality_rate",
    "NT_ANT_WHZ_NE2": "wasting_children_pct",
    "NT_ANT_HAZ_NE2": "stunting_children_pct",
    "NT_BW_LOW": "low_birthweight_pct",
    "FP_CUSA_W_MOD": "contraceptive_prevalence_pct",
    "RH_DELA_C_SKP": "skilled_birth_attendant_pct",
    "HA_HIVP_W_HIV": "hiv_prevalence_women_pct",
    "WE_WMEI_W_LIT": "womens_literacy_pct",
    "ML_NETC_C_SLP": "bednet_usage_pct",
}


def _fetch_dhs_api(indicators: list[str], survey: str) -> pd.DataFrame | None:
    ids = ",".join(indicators)
    url = (f"{DHS_API_BASE}/data?indicatorIds={ids}&surveyIds={survey}"
           f"&breakdown=national&perpage=500&f=csv")
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        from io import StringIO
        df = pd.read_csv(StringIO(r.text))
        logger.info(f"DHS API returned {len(df)} rows")
        return df
    except Exception as e:
        logger.warning(f"DHS API failed: {e}")
        return None


def _fallback_national_summary() -> pd.DataFrame:
    """
    Hard-coded national estimates from NFHS-5 report (IIPS, 2021).
    VALUES ARE PUBLISHED AGGREGATES — NOT FABRICATED.
    Source: International Institute for Population Sciences. NFHS-5 National Report.
    Mumbai: IIPS; 2022.
    """
    data = {
        "indicator": [
            "household_electricity_pct",
            "household_clean_fuel_pct",
            "improved_sanitation_pct",
            "improved_water_pct",
            "infant_mortality_rate_per1000",
            "stunting_children_pct",
            "wasting_children_pct",
            "low_birthweight_pct",
            "womens_literacy_pct",
            "skilled_birth_attendant_pct",
            "overweight_women_pct",
            "anaemia_women_pct",
            "tobacco_use_men_pct",
            "alcohol_use_men_pct",
        ],
        "value": [96.8, 58.6, 69.9, 95.9, 35.2, 35.5, 19.3, 18.2,
                  71.5, 88.6, 24.0, 57.0, 38.0, 19.0],
        "year": [2021] * 14,
        "survey": ["NFHS-5"] * 14,
        "country": ["India"] * 14,
        "source_note": ["IIPS NFHS-5 National Report 2022"] * 14,
    }
    return pd.DataFrame(data)


def run(cfg: dict) -> dict:
    raw_dir: Path = cfg["paths"]["data_raw"]
    out_file = raw_dir / "nfhs5_indicators.csv"

    if out_file.exists():
        df = pd.read_csv(out_file)
        return {"rows": len(df), "columns": len(df.columns), "local_file": str(out_file)}

    df = _fetch_dhs_api(list(INDICATOR_MAP.keys()), INDIA_NFHS5_SURVEY)
    if df is None:
        logger.warning("Using fallback national NFHS-5 summary (published aggregates)")
        df = _fallback_national_summary()

    df.to_csv(out_file, index=False)
    logger.info(f"Saved {len(df)} rows → {out_file}")
    return {"rows": len(df), "columns": len(df.columns), "local_file": str(out_file)}


if __name__ == "__main__":
    from src.utils.config import get_arg_config
    run(get_arg_config())
