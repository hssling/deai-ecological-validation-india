from __future__ import annotations

import json
import re
import time
from datetime import date
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "expanded_search"
INTERIM = ROOT / "data" / "interim"
PROCESSED = ROOT / "data" / "processed"
TABLES = ROOT / "results" / "tables"

RUN_DATE = date.today().isoformat()

CORE_QUERY = (
    '(frail* OR prefrail* OR "pre-frail" OR "physical frailty" OR "frailty phenotype" OR sarcopenia) '
    'AND (exercise OR "resistance training" OR "strength training" OR nutrition OR protein OR vitamin D '
    'OR multidomain OR "multi-domain" OR "home-based" OR digital OR mHealth OR "Tai Chi") '
    'AND (random* OR trial OR "controlled trial") '
    'AND (older OR elderly OR aged OR geriatric OR "community dwelling" OR "primary care")'
)


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def norm_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def safe_get(url: str, params: dict | None = None, timeout: int = 60) -> requests.Response:
    headers = {"User-Agent": "frailty-review-workflow/0.1 (mailto:hssling@yahoo.com)"}
    resp = requests.get(url, params=params, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp


def load_pubmed_existing() -> list[dict]:
    path = ROOT / "data" / "interim" / "pubmed_candidate_records.csv"
    df = pd.read_csv(path).fillna("")
    rows = []
    for _, row in df.iterrows():
        rows.append(
            {
                "source": "PubMed_existing",
                "source_id": str(row.get("pmid", "")),
                "pmid": str(row.get("pmid", "")),
                "doi": str(row.get("doi", "")),
                "title": clean(row.get("title", "")),
                "year": str(row.get("year", "")),
                "journal": clean(row.get("journal", "")),
                "abstract": clean(row.get("abstract", "")),
                "url": str(row.get("url", "")),
                "record_type": "journal_record",
            }
        )
    return rows


def search_europepmc(max_pages: int = 5, page_size: int = 1000) -> tuple[list[dict], dict]:
    rows = []
    cursor = "*"
    logs = {"database": "Europe PMC", "status": "not_run", "records": 0, "note": ""}
    for page in range(max_pages):
        params = {
            "query": CORE_QUERY,
            "format": "json",
            "pageSize": page_size,
            "cursorMark": cursor,
            "resultType": "core",
        }
        data = safe_get("https://www.ebi.ac.uk/europepmc/webservices/rest/search", params=params).json()
        RAW.mkdir(parents=True, exist_ok=True)
        (RAW / f"europepmc_{RUN_DATE}_page{page + 1}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
        result_list = data.get("resultList", {}).get("result", [])
        for item in result_list:
            rows.append(
                {
                    "source": "Europe_PMC",
                    "source_id": clean(item.get("id", "")),
                    "pmid": clean(item.get("pmid", "")),
                    "pmcid": clean(item.get("pmcid", "")),
                    "doi": clean(item.get("doi", "")),
                    "title": clean(item.get("title", "")),
                    "year": clean(item.get("pubYear", "")),
                    "journal": clean(item.get("journalTitle", "")),
                    "abstract": clean(item.get("abstractText", "")),
                    "url": f"https://europepmc.org/article/{item.get('source', 'MED')}/{item.get('id', '')}",
                    "record_type": clean(item.get("pubType", "")),
                }
            )
        next_cursor = data.get("nextCursorMark")
        cursor = next_cursor or cursor
        if not result_list or not next_cursor:
            break
        time.sleep(0.4)
    logs.update({"status": "ok", "records": len(rows), "note": f"page_size={page_size}; max_pages={max_pages}"})
    return rows, logs


def search_clinicaltrials(max_pages: int = 10, page_size: int = 100) -> tuple[list[dict], dict]:
    rows = []
    token = None
    logs = {"database": "ClinicalTrials.gov", "status": "not_run", "records": 0, "note": ""}
    for page in range(max_pages):
        params = {
            "query.term": CORE_QUERY,
            "pageSize": page_size,
            "format": "json",
        }
        if token:
            params["pageToken"] = token
        data = safe_get("https://clinicaltrials.gov/api/v2/studies", params=params).json()
        RAW.mkdir(parents=True, exist_ok=True)
        (RAW / f"clinicaltrials_{RUN_DATE}_page{page + 1}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
        for study in data.get("studies", []):
            protocol = study.get("protocolSection", {})
            ident = protocol.get("identificationModule", {})
            status = protocol.get("statusModule", {})
            design = protocol.get("designModule", {})
            cond = protocol.get("conditionsModule", {})
            desc = protocol.get("descriptionModule", {})
            arms = protocol.get("armsInterventionsModule", {})
            nct = clean(ident.get("nctId", ""))
            rows.append(
                {
                    "source": "ClinicalTrials.gov",
                    "source_id": nct,
                    "pmid": "",
                    "pmcid": "",
                    "doi": "",
                    "title": clean(ident.get("briefTitle", "")),
                    "year": clean(status.get("startDateStruct", {}).get("date", ""))[:4],
                    "journal": "ClinicalTrials.gov",
                    "abstract": clean(
                        " ".join(
                            [
                                desc.get("briefSummary", ""),
                                " ".join(cond.get("conditions", [])),
                                " ".join(i.get("name", "") for i in arms.get("interventions", [])),
                                str(design.get("studyType", "")),
                                str(design.get("phases", "")),
                            ]
                        )
                    ),
                    "url": f"https://clinicaltrials.gov/study/{nct}" if nct else "",
                    "record_type": clean(design.get("studyType", "")),
                    "trial_status": clean(status.get("overallStatus", "")),
                }
            )
        token = data.get("nextPageToken")
        if not token:
            break
        time.sleep(0.4)
    logs.update({"status": "ok", "records": len(rows), "note": f"page_size={page_size}; max_pages={max_pages}"})
    return rows, logs


def search_crossref(rows_limit: int = 1000) -> tuple[list[dict], dict]:
    rows = []
    params = {
        "query.bibliographic": 'frailty older adults exercise nutrition randomized trial',
        "filter": "type:journal-article",
        "rows": rows_limit,
        "select": "DOI,title,published-print,published-online,container-title,URL,abstract,type",
        "mailto": "hssling@yahoo.com",
    }
    data = safe_get("https://api.crossref.org/works", params=params).json()
    RAW.mkdir(parents=True, exist_ok=True)
    (RAW / f"crossref_{RUN_DATE}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    for item in data.get("message", {}).get("items", []):
        title = clean(" ".join(item.get("title", [])))
        journal = clean(" ".join(item.get("container-title", [])))
        date_parts = item.get("published-print", item.get("published-online", {})).get("date-parts", [[]])
        year = str(date_parts[0][0]) if date_parts and date_parts[0] else ""
        rows.append(
            {
                "source": "Crossref",
                "source_id": clean(item.get("DOI", "")),
                "pmid": "",
                "pmcid": "",
                "doi": clean(item.get("DOI", "")),
                "title": title,
                "year": year,
                "journal": journal,
                "abstract": clean(re.sub("<[^>]+>", " ", item.get("abstract", ""))),
                "url": clean(item.get("URL", "")),
                "record_type": clean(item.get("type", "")),
            }
        )
    return rows, {"database": "Crossref", "status": "ok", "records": len(rows), "note": f"rows={rows_limit}"}


def search_openalex(rows_limit: int = 1000, per_page: int = 200) -> tuple[list[dict], dict]:
    rows = []
    pages = max(1, rows_limit // per_page)
    for page in range(1, pages + 1):
        params = {
            "search": "frailty older adults exercise nutrition randomized trial",
            "per-page": per_page,
            "page": page,
            "mailto": "hssling@yahoo.com",
        }
        data = safe_get("https://api.openalex.org/works", params=params).json()
        RAW.mkdir(parents=True, exist_ok=True)
        (RAW / f"openalex_{RUN_DATE}_page{page}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
        for item in data.get("results", []):
            abstract_inv = item.get("abstract_inverted_index") or {}
            abstract_words = []
            if abstract_inv:
                positions = []
                for word, idxs in abstract_inv.items():
                    for idx in idxs:
                        positions.append((idx, word))
                abstract_words = [word for _, word in sorted(positions)]
            primary = item.get("primary_location") or {}
            source = primary.get("source") or {}
            ids = item.get("ids") or {}
            rows.append(
                {
                    "source": "OpenAlex",
                    "source_id": clean(item.get("id", "")),
                    "pmid": clean(str(ids.get("pmid", "")).rsplit("/", 1)[-1] if ids.get("pmid") else ""),
                    "pmcid": clean(str(ids.get("pmcid", "")).rsplit("/", 1)[-1] if ids.get("pmcid") else ""),
                    "doi": clean(str(ids.get("doi", "")).replace("https://doi.org/", "")),
                    "title": clean(item.get("title", "")),
                    "year": clean(item.get("publication_year", "")),
                    "journal": clean(source.get("display_name", "")),
                    "abstract": clean(" ".join(abstract_words)),
                    "url": clean(primary.get("landing_page_url", item.get("id", ""))),
                    "record_type": clean(item.get("type", "")),
                }
            )
        time.sleep(0.4)
    return rows, {"database": "OpenAlex", "status": "ok", "records": len(rows), "note": f"rows_limit={rows_limit}"}


def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    df = df.fillna("")
    df["doi_norm"] = df["doi"].astype(str).str.lower().str.replace(r"^https?://doi.org/", "", regex=True).str.strip()
    df["pmid_norm"] = df["pmid"].astype(str).str.strip()
    df["title_norm"] = df["title"].map(norm_title)
    df["dedup_key"] = ""
    df.loc[df["doi_norm"].ne(""), "dedup_key"] = "doi:" + df.loc[df["doi_norm"].ne(""), "doi_norm"]
    mask = df["dedup_key"].eq("") & df["pmid_norm"].ne("")
    df.loc[mask, "dedup_key"] = "pmid:" + df.loc[mask, "pmid_norm"]
    mask = df["dedup_key"].eq("") & df["title_norm"].ne("")
    df.loc[mask, "dedup_key"] = "title:" + df.loc[mask, "title_norm"]
    df = df.sort_values(["dedup_key", "source"]).drop_duplicates("dedup_key", keep="first")
    return df.drop(columns=["doi_norm", "pmid_norm", "title_norm"])


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    INTERIM.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)

    all_rows = []
    logs = []
    pubmed_rows = load_pubmed_existing()
    all_rows.extend(pubmed_rows)
    logs.append({"database": "PubMed_existing", "status": "ok", "records": len(pubmed_rows), "note": "From prior authenticated PubMed XML pull"})

    for func in [search_europepmc, search_clinicaltrials, search_crossref, search_openalex]:
        try:
            rows, log = func()
            all_rows.extend(rows)
            logs.append(log)
            print(f"{log['database']}: {log['records']}")
        except Exception as exc:
            logs.append({"database": func.__name__, "status": "error", "records": 0, "note": repr(exc)})
            print(f"{func.__name__} ERROR {exc}")

    logs.extend(
        [
            {"database": "Embase", "status": "not_searched_no_subscription", "records": 0, "note": "Requires institutional subscription/API access"},
            {"database": "Scopus", "status": "not_searched_no_subscription", "records": 0, "note": "Requires institutional subscription/API access"},
            {"database": "CENTRAL", "status": "not_searched_no_api_in_workspace", "records": 0, "note": "Search manually or through Cochrane Library access before final submission"},
            {"database": "Web of Science", "status": "not_searched_no_subscription", "records": 0, "note": "Requires institutional subscription/API access"},
        ]
    )

    raw_df = pd.DataFrame(all_rows).fillna("")
    raw_df.to_csv(INTERIM / "expanded_accessible_candidate_records.csv", index=False)
    deduped = deduplicate(raw_df)
    deduped.to_csv(PROCESSED / "expanded_accessible_deduped_records.csv", index=False)
    pd.DataFrame(logs).to_csv(TABLES / "expanded_accessible_search_log.csv", index=False)
    raw_df["source"].value_counts().rename_axis("source").reset_index(name="records").to_csv(
        TABLES / "expanded_accessible_source_counts_raw.csv", index=False
    )
    deduped["source"].value_counts().rename_axis("source").reset_index(name="records_after_dedup").to_csv(
        TABLES / "expanded_accessible_source_counts_deduped.csv", index=False
    )

    print(f"raw_records={len(raw_df)}")
    print(f"deduped_records={len(deduped)}")
    print(pd.DataFrame(logs).to_string(index=False))


if __name__ == "__main__":
    main()
