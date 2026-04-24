"""
Download WHO Ambient Air Quality Database (city-level PM2.5/PM10).
Public download: https://www.who.int/data/gho/data/themes/air-pollution/who-ambient-air-quality-database

The 2022 update is distributed as a zipped Excel file.  We fetch it,
extract the data sheet, and write a cleaned CSV.
"""
import io
import sys
import zipfile
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).parents[2]))
from src.utils.logger import get_logger

logger = get_logger("who_aaq")

# Direct link to WHO AQD 2022 download (verified 2026-04)
WHO_AQD_URL = (
    "https://cdn.who.int/media/docs/default-source/air-pollution-documents/"
    "air-quality-and-health/air_quality_data_2022_v0.4.1.xlsx"
)
FALLBACK_URL = (
    "https://www.who.int/docs/default-source/air-pollution-documents/"
    "air-quality-and-health/air_quality_data_2022_v0.4.1.xlsx"
)


def run(cfg: dict) -> dict:
    raw_dir: Path = cfg["paths"]["data_raw"]
    out_file = raw_dir / "who_aaq_database.xlsx"
    csv_file = raw_dir / "who_aaq_pm25_clean.csv"

    if csv_file.exists():
        logger.info("WHO AAQ CSV already present — skipping download")
        df = pd.read_csv(csv_file)
        return {"rows": len(df), "columns": len(df.columns), "local_file": str(csv_file)}

    logger.info(f"Downloading WHO Ambient Air Quality DB → {out_file}")
    for url in [WHO_AQD_URL, FALLBACK_URL]:
        try:
            r = requests.get(url, timeout=60, stream=True)
            r.raise_for_status()
            with open(out_file, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            logger.info("Download complete")
            break
        except Exception as e:
            logger.warning(f"URL failed: {url} — {e}")
    else:
        raise RuntimeError("All WHO AAQ download URLs failed. Place file manually at "
                           f"{out_file}")

    # Parse Excel
    xls = pd.ExcelFile(out_file)
    sheet = next((s for s in xls.sheet_names if "data" in s.lower()), xls.sheet_names[0])
    df = pd.read_excel(out_file, sheet_name=sheet)

    # Standardise column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Keep core variables
    keep_cols = [c for c in df.columns if any(
        k in c for k in ("country", "city", "pm2", "pm10", "year", "region", "pop")
    )]
    df = df[keep_cols].copy()
    df.to_csv(csv_file, index=False)
    logger.info(f"Saved {len(df)} rows → {csv_file}")

    return {"rows": len(df), "columns": len(df.columns), "local_file": str(csv_file)}


if __name__ == "__main__":
    from src.utils.config import get_arg_config
    run(get_arg_config())
