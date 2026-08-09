from __future__ import annotations

import csv
import datetime as dt
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from time import sleep

import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
INTERIM = ROOT / "data" / "interim"
TABLES = ROOT / "results" / "tables"
RUN_DATE = dt.date.today().isoformat()

ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

QUERY = (
    '((frail*[Title/Abstract] OR prefrail*[Title/Abstract] OR "physical frailty"[Title/Abstract] '
    'OR "frailty status"[Title/Abstract] OR "frailty phenotype"[Title/Abstract] OR sarcopenia[Title/Abstract] '
    'OR "functional decline"[Title/Abstract]) '
    'AND (exercise[Title/Abstract] OR "resistance training"[Title/Abstract] OR "strength training"[Title/Abstract] '
    'OR balance[Title/Abstract] OR walking[Title/Abstract] OR aerobic[Title/Abstract] '
    'OR "multicomponent exercise"[Title/Abstract] OR "Tai Chi"[Title/Abstract] OR nutrition[Title/Abstract] '
    'OR protein[Title/Abstract] OR leucine[Title/Abstract] OR HMB[Title/Abstract] OR "vitamin D"[Title/Abstract] '
    'OR multidomain[Title/Abstract] OR "comprehensive geriatric assessment"[Title/Abstract] '
    'OR mHealth[Title/Abstract] OR digital[Title/Abstract] OR "home-based"[Title/Abstract]) '
    'AND (random*[Title/Abstract] OR trial[Title/Abstract] OR RCT[Title/Abstract] OR "controlled trial"[Title/Abstract]) '
    'AND (older[Title/Abstract] OR elderly[Title/Abstract] OR aged[Title/Abstract] OR geriatric[Title/Abstract] '
    'OR "community dwelling"[Title/Abstract] OR "primary care"[Title/Abstract]))'
)


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def parse_pubmed(xml_text: str) -> list[dict[str, str]]:
    root = ET.fromstring(xml_text)
    rows: list[dict[str, str]] = []
    for article in root.findall(".//PubmedArticle"):
        medline = article.find("./MedlineCitation")
        pmid = clean(medline.findtext("./PMID")) if medline is not None else ""
        art = medline.find("./Article") if medline is not None else None
        title = clean("".join(art.findtext("./ArticleTitle") or "")) if art is not None else ""
        abstract = (
            " ".join(clean("".join(elem.itertext())) for elem in art.findall("./Abstract/AbstractText"))
            if art is not None
            else ""
        )
        journal = clean(art.findtext("./Journal/Title")) if art is not None else ""
        year = clean(art.findtext("./Journal/JournalIssue/PubDate/Year")) if art is not None else ""
        if not year and art is not None:
            year = clean(art.findtext("./Journal/JournalIssue/PubDate/MedlineDate"))[:4]
        authors = []
        if art is not None:
            for author in art.findall("./AuthorList/Author"):
                last = clean(author.findtext("./LastName"))
                initials = clean(author.findtext("./Initials"))
                collective = clean(author.findtext("./CollectiveName"))
                if collective:
                    authors.append(collective)
                elif last:
                    authors.append(f"{last} {initials}".strip())
        doi = ""
        pmcid = ""
        pubmed_data = article.find("./PubmedData")
        if pubmed_data is not None:
            for aid in pubmed_data.findall("./ArticleIdList/ArticleId"):
                typ = aid.attrib.get("IdType", "").lower()
                if typ == "doi":
                    doi = clean(aid.text)
                elif typ == "pmc":
                    pmcid = clean(aid.text)
        rows.append(
            {
                "pmid": pmid,
                "pmcid": pmcid,
                "doi": doi,
                "title": title,
                "authors": "; ".join(authors[:10]),
                "year": year,
                "journal": journal,
                "abstract": abstract,
                "source": "PubMed",
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "",
            }
        )
    return rows


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    INTERIM.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)

    search_params = {"db": "pubmed", "term": QUERY, "retmode": "json", "retmax": 5000, "sort": "relevance"}
    search_response = requests.get(ESEARCH, params=search_params, timeout=30)
    search_response.raise_for_status()
    search_json = search_response.json()
    (RAW / f"pubmed_search_{RUN_DATE}.json").write_text(json.dumps(search_json, indent=2), encoding="utf-8")

    ids = search_json.get("esearchresult", {}).get("idlist", [])
    count = int(search_json.get("esearchresult", {}).get("count", 0))
    records = []
    xml_chunks = []
    batch_size = 200
    for start in range(0, len(ids), batch_size):
        batch = ids[start : start + batch_size]
        fetch_response = requests.get(
            EFETCH,
            params={"db": "pubmed", "id": ",".join(batch), "retmode": "xml"},
            timeout=90,
        )
        fetch_response.raise_for_status()
        xml_chunks.append(fetch_response.text)
        records.extend(parse_pubmed(fetch_response.text))
        sleep(0.35)
    (RAW / f"pubmed_records_{RUN_DATE}.xml").write_text("\n".join(xml_chunks), encoding="utf-8")

    df = pd.DataFrame(records)
    df.to_csv(INTERIM / "pubmed_candidate_records.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    pd.DataFrame(
        [
            {
                "run_date": RUN_DATE,
                "database": "PubMed",
                "query": QUERY,
                "hits_reported": count,
                "records_downloaded": len(df),
                "status": "ok",
            }
        ]
    ).to_csv(TABLES / "search_log.csv", index=False)
    print(f"hits_reported={count}")
    print(f"records_downloaded={len(df)}")


if __name__ == "__main__":
    main()
