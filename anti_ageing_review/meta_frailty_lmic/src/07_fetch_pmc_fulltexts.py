from __future__ import annotations

import re
from pathlib import Path
from time import sleep

import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[1]
RAW_FULLTEXT = ROOT / "data" / "raw" / "pmc_fulltext"
TABLES = ROOT / "results" / "tables"
PROCESSED = ROOT / "data" / "processed"
EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def pmc_numeric(pmcid: str) -> str:
    return re.sub(r"^PMC", "", str(pmcid).strip(), flags=re.I)


def main() -> None:
    RAW_FULLTEXT.mkdir(parents=True, exist_ok=True)
    high = pd.read_csv(TABLES / "high_confidence_extraction_queue.csv").fillna("")
    allr = pd.read_csv(PROCESSED / "screened_prioritized.csv").fillna("")
    merged = high.merge(allr[["pmid", "pmcid"]], on="pmid", how="left").fillna("")
    rows = []
    for _, row in merged.iterrows():
        pmcid = str(row.get("pmcid", "")).strip()
        if not pmcid:
            rows.append(
                {
                    "pmid": row.get("pmid", ""),
                    "pmcid": "",
                    "title": row.get("title", ""),
                    "fetch_status": "no_pmcid",
                    "local_path": "",
                }
            )
            continue
        local = RAW_FULLTEXT / f"{pmcid}.xml"
        if local.exists() and local.stat().st_size > 100:
            rows.append(
                {
                    "pmid": row.get("pmid", ""),
                    "pmcid": pmcid,
                    "title": row.get("title", ""),
                    "fetch_status": "cached",
                    "local_path": str(local.relative_to(ROOT)),
                }
            )
            continue
        try:
            resp = requests.get(
                EFETCH,
                params={"db": "pmc", "id": pmc_numeric(pmcid), "retmode": "xml"},
                timeout=60,
            )
            resp.raise_for_status()
            text = resp.text
            if "<article" in text or "<pmc-articleset" in text:
                local.write_text(text, encoding="utf-8")
                status = "fetched"
            else:
                status = "not_article_xml"
            rows.append(
                {
                    "pmid": row.get("pmid", ""),
                    "pmcid": pmcid,
                    "title": row.get("title", ""),
                    "fetch_status": status,
                    "local_path": str(local.relative_to(ROOT)) if local.exists() else "",
                }
            )
        except Exception as exc:
            rows.append(
                {
                    "pmid": row.get("pmid", ""),
                    "pmcid": pmcid,
                    "title": row.get("title", ""),
                    "fetch_status": f"error: {type(exc).__name__}",
                    "local_path": "",
                }
            )
        sleep(0.35)
    out = pd.DataFrame(rows)
    out.to_csv(TABLES / "pmc_fulltext_fetch_log.csv", index=False)
    print(out["fetch_status"].value_counts().to_string())


if __name__ == "__main__":
    main()
