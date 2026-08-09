"""Phase 2: Multi-source search for DNAm clock x intervention RCTs."""
from __future__ import annotations
import argparse, json, time, csv, sys
from pathlib import Path
import requests

sys.path.insert(0, str(Path(__file__).parent))
from _common import load_config, log, ensure_dirs, append_amendment, now_iso

UA = "dnam-clocks-meta/1.0 (mailto:hssling@gmail.com)"
HEADERS = {"User-Agent": UA, "Accept": "application/json"}


def build_query(clock_terms, intv_terms):
    a = " OR ".join(f'"{t}"' for t in clock_terms)
    b = " OR ".join(f'"{t}"' for t in intv_terms)
    return f"({a}) AND ({b})"


def _get(url, params=None, retries=3, sleep=1.0):
    for i in range(retries):
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=30)
            if r.status_code == 200:
                return r
            time.sleep(sleep * (2 ** i))
        except Exception as e:
            log("http_retry", url=url, attempt=i, err=str(e))
            time.sleep(sleep * (2 ** i))
    return None


def search_pubmed(query, raw_dir, date_from):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": query + f' AND ("{date_from}"[PDAT]:"3000"[PDAT])',
              "retmode": "json", "retmax": 2000}
    r = _get(url, params=params)
    if r is None:
        return None
    ids = r.json().get("esearchresult", {}).get("idlist", [])
    if not ids:
        (raw_dir / f"pubmed_{now_iso()[:10]}.json").write_text(json.dumps({"esearchresult": {"idlist": []}}))
        return []
    f = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    rr = _get(f, params={"db": "pubmed", "id": ",".join(ids[:500]), "retmode": "json"})
    payload = rr.json() if rr else {}
    (raw_dir / f"pubmed_{now_iso()[:10]}.json").write_text(json.dumps(payload))
    return normalize_pubmed(payload)


def normalize_pubmed(payload):
    out = []
    res = payload.get("result", {})
    for k, rec in res.items():
        if k == "uids":
            continue
        if not isinstance(rec, dict):
            continue
        out.append({
            "source": "pubmed", "source_id": k, "pmid": k,
            "doi": next((i.get("value", "") for i in rec.get("articleids", [])
                         if i.get("idtype") == "doi"), ""),
            "title": rec.get("title", ""), "abstract": "",
            "authors": "; ".join(a.get("name", "") for a in rec.get("authors", [])),
            "year": (rec.get("pubdate", "") or "")[:4],
            "journal": rec.get("fulljournalname", "") or rec.get("source", ""),
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{k}/",
            "fetched_at": now_iso(),
        })
    return out


def search_europepmc(query, raw_dir):
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    r = _get(url, params={"query": query, "format": "json", "pageSize": 1000, "resultType": "core"})
    if r is None:
        return None
    payload = r.json()
    (raw_dir / f"europepmc_{now_iso()[:10]}.json").write_text(json.dumps(payload))
    return normalize_europepmc(payload)


def normalize_europepmc(payload):
    out = []
    for rec in payload.get("resultList", {}).get("result", []):
        fulltext_url = ""
        ftul = rec.get("fullTextUrlList", {})
        if ftul and ftul.get("fullTextUrl"):
            fulltext_url = ftul["fullTextUrl"][0].get("url", "")
        out.append({
            "source": "europepmc", "source_id": rec.get("id", ""),
            "pmid": rec.get("pmid", ""), "doi": rec.get("doi", ""),
            "title": rec.get("title", ""), "abstract": rec.get("abstractText", ""),
            "authors": rec.get("authorString", ""), "year": rec.get("pubYear", ""),
            "journal": rec.get("journalTitle", ""), "url": fulltext_url,
            "fetched_at": now_iso(),
        })
    return out


def search_crossref(query, raw_dir):
    url = "https://api.crossref.org/works"
    r = _get(url, params={"query": query, "rows": 1000})
    if r is None:
        return None
    payload = r.json()
    (raw_dir / f"crossref_{now_iso()[:10]}.json").write_text(json.dumps(payload))
    return normalize_crossref(payload)


def normalize_crossref(payload):
    out = []
    for rec in payload.get("message", {}).get("items", []):
        out.append({
            "source": "crossref", "source_id": rec.get("DOI", ""),
            "pmid": "", "doi": rec.get("DOI", ""),
            "title": (rec.get("title") or [""])[0],
            "abstract": rec.get("abstract", ""),
            "authors": "; ".join(f"{a.get('given', '')} {a.get('family', '')}".strip()
                                 for a in rec.get("author", [])),
            "year": str(rec.get("issued", {}).get("date-parts", [[None]])[0][0] or ""),
            "journal": (rec.get("container-title") or [""])[0],
            "url": rec.get("URL", ""), "fetched_at": now_iso(),
        })
    return out


def search_openalex(query, raw_dir):
    url = "https://api.openalex.org/works"
    r = _get(url, params={"search": query, "per-page": 200})
    if r is None:
        return None
    payload = r.json()
    (raw_dir / f"openalex_{now_iso()[:10]}.json").write_text(json.dumps(payload))
    return normalize_openalex(payload)


def normalize_openalex(payload):
    out = []
    for w in payload.get("results", []):
        host = w.get("host_venue") or w.get("primary_location", {}).get("source") or {}
        out.append({
            "source": "openalex", "source_id": w.get("id", ""),
            "pmid": ((w.get("ids", {}) or {}).get("pmid", "") or "").split("/")[-1],
            "doi": ((w.get("doi", "") or "")).replace("https://doi.org/", ""),
            "title": w.get("title", "") or "",
            "abstract": "",  # invert-index decoding skipped for brevity
            "authors": "; ".join((a.get("author", {}) or {}).get("display_name", "")
                                 for a in w.get("authorships", [])),
            "year": str(w.get("publication_year", "")),
            "journal": host.get("display_name", "") if isinstance(host, dict) else "",
            "url": w.get("id", ""), "fetched_at": now_iso(),
        })
    return out


def search_clinicaltrials(raw_dir):
    url = "https://clinicaltrials.gov/api/v2/studies"
    terms = "epigenetic clock OR DNA methylation age OR DunedinPACE OR GrimAge OR PhenoAge"
    r = _get(url, params={"query.term": terms, "filter.overallStatus": "COMPLETED",
                          "pageSize": 200, "format": "json"})
    if r is None:
        return None
    payload = r.json()
    (raw_dir / f"clinicaltrials_{now_iso()[:10]}.json").write_text(json.dumps(payload))
    return normalize_clinicaltrials(payload)


def normalize_clinicaltrials(payload):
    out = []
    for s in payload.get("studies", []):
        ps = s.get("protocolSection", {})
        idm = ps.get("identificationModule", {})
        out.append({
            "source": "clinicaltrials", "source_id": idm.get("nctId", ""),
            "pmid": "", "doi": "",
            "title": idm.get("officialTitle", "") or idm.get("briefTitle", ""),
            "abstract": ps.get("descriptionModule", {}).get("briefSummary", ""),
            "authors": "",
            "year": (ps.get("statusModule", {}).get("completionDateStruct", {}).get("date", "") or "")[:4],
            "journal": "ClinicalTrials.gov",
            "url": f"https://clinicaltrials.gov/study/{idm.get('nctId', '')}",
            "fetched_at": now_iso(),
        })
    return out


def run(cfg):
    raw_dir = cfg["paths"]["data_raw"]
    ensure_dirs(raw_dir, cfg["paths"]["data_interim"])
    q = build_query(cfg["search"]["block_clock_terms"], cfg["search"]["block_intervention_terms"])
    log("query_built", q=q)
    sources_ok, records = 0, []

    for name, runner in [
        ("pubmed", lambda: search_pubmed(q, raw_dir, cfg["search"]["date_from"])),
        ("europepmc", lambda: search_europepmc(q, raw_dir)),
        ("crossref", lambda: search_crossref(q, raw_dir)),
        ("openalex", lambda: search_openalex(q, raw_dir)),
        ("clinicaltrials", lambda: search_clinicaltrials(raw_dir)),
    ]:
        try:
            r = runner()
            if r is None:
                append_amendment(cfg["paths"]["docs"], f"{name} returned no response",
                                 "API unreachable; continuing without this source")
            else:
                records.extend(r)
                sources_ok += 1
                log("source_ok", source=name, n=len(r))
        except Exception as e:
            append_amendment(cfg["paths"]["docs"], f"{name} failed: {e}", "Logged exception, continuing")
            log("source_err", source=name, err=str(e))
        time.sleep(1.0)

    out = cfg["paths"]["data_interim"] / f"raw_records_dnam_{cfg['project']['freeze_date']}.csv"
    cols = ["source", "source_id", "doi", "pmid", "title", "abstract", "authors", "year", "journal", "url", "fetched_at"]
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in records:
            w.writerow({k: r.get(k, "") for k in cols})
    log("search_done", sources_ok=sources_ok, total_records=len(records), path=str(out))
    if sources_ok < 4:
        append_amendment(cfg["paths"]["docs"], f"Only {sources_ok}/5 sources returned data",
                         "Quality gate flag - below threshold")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    run(load_config(ap.parse_args().config))
