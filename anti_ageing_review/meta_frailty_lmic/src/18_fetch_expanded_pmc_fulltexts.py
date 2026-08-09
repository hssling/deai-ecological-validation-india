from __future__ import annotations

import re
from pathlib import Path
from time import sleep

import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[1]
RAW_FULLTEXT = ROOT / "data" / "raw" / "pmc_fulltext"
TABLES = ROOT / "results" / "tables"
EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def clean_id(value: object) -> str:
    text = str(value or "").strip()
    if text.endswith(".0") and text[:-2].isdigit():
        text = text[:-2]
    return text


def normalize_pmcid(value: object) -> str:
    text = clean_id(value)
    if not text:
        return ""
    text = re.sub(r"^PMC", "", text, flags=re.I)
    return f"PMC{text}" if text.isdigit() else ""


def pmc_numeric(pmcid: str) -> str:
    return re.sub(r"^PMC", "", str(pmcid).strip(), flags=re.I)


def main() -> None:
    RAW_FULLTEXT.mkdir(parents=True, exist_ok=True)
    candidates = pd.read_csv(TABLES / "expanded_accessible_new_candidates_not_in_primary_queue.csv").fillna("")
    candidates["pmcid_norm"] = candidates["pmcid"].map(normalize_pmcid)
    candidates = candidates[candidates["pmcid_norm"].ne("")].copy()
    candidates = candidates.drop_duplicates("pmcid_norm")

    rows = []
    for _, row in candidates.iterrows():
        pmcid = row["pmcid_norm"]
        local = RAW_FULLTEXT / f"{pmcid}.xml"
        if local.exists() and local.stat().st_size > 100:
            rows.append(
                {
                    "source": row.get("source", ""),
                    "pmid": clean_id(row.get("pmid", "")),
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
                    "source": row.get("source", ""),
                    "pmid": clean_id(row.get("pmid", "")),
                    "pmcid": pmcid,
                    "title": row.get("title", ""),
                    "fetch_status": status,
                    "local_path": str(local.relative_to(ROOT)) if local.exists() else "",
                }
            )
        except Exception as exc:
            rows.append(
                {
                    "source": row.get("source", ""),
                    "pmid": clean_id(row.get("pmid", "")),
                    "pmcid": pmcid,
                    "title": row.get("title", ""),
                    "fetch_status": f"error: {type(exc).__name__}",
                    "local_path": "",
                }
            )
        sleep(0.34)

    out = pd.DataFrame(rows)
    out.to_csv(TABLES / "expanded_pmc_fulltext_fetch_log.csv", index=False)
    print(f"pmcid_candidates={len(candidates)}")
    if not out.empty:
        print(out["fetch_status"].value_counts().to_string())


if __name__ == "__main__":
    main()
