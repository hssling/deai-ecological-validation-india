from __future__ import annotations
import argparse, time, hashlib
from pathlib import Path
import requests, yaml
import pandas as pd
from src.utils.io import load_config, save_csv, append_log, now_iso

def clean_text(x):
    return " ".join(str(x or "").replace("\n", " ").split())

def record_id(source, title, doi="", pmid=""):
    key = (doi or pmid or title).lower().strip()
    return hashlib.md5(f"{source}|{key}".encode()).hexdigest()

def pubmed_search(query, max_records, email):
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    params = {"db":"pubmed","term":query,"retmax":max_records,"retmode":"json","sort":"relevance","tool":"anti_ageing_review","email":email}
    ids = requests.get(f"{base}/esearch.fcgi", params=params, timeout=30).json().get("esearchresult", {}).get("idlist", [])
    if not ids:
        return []
    fetch = requests.get(f"{base}/esummary.fcgi", params={"db":"pubmed","id":",".join(ids),"retmode":"json","tool":"anti_ageing_review","email":email}, timeout=30).json()
    rows = []
    for pmid in fetch.get("result", {}).get("uids", []):
        r = fetch["result"][pmid]
        title = clean_text(r.get("title"))
        rows.append({
            "source":"pubmed","source_stream":"peer_reviewed","query":query,"record_id":record_id("pubmed", title, pmid=pmid),
            "title":title,"abstract":"","authors":"; ".join([a.get("name","") for a in r.get("authors", [])[:8]]),
            "year":str(r.get("pubdate",""))[:4],"journal":r.get("fulljournalname") or r.get("source"),"doi":"",
            "pmid":pmid,"pmcid":"","url":f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/","publication_type":"; ".join(r.get("pubtype", [])),
            "is_preprint":False,"retrieved_at":now_iso()
        })
    return rows

def europe_query(query):
    # Europe PMC is sensitive to some PubMed-style quoted phrases in this
    # pilot. Preserve Boolean logic but simplify phrase quoting.
    return query.replace('"', "")

def europe_pmc_search(query, max_records):
    params = {"query":europe_query(query), "format":"json", "pageSize":max_records}
    data = requests.get("https://www.ebi.ac.uk/europepmc/webservices/rest/search", params=params, timeout=30).json()
    rows = []
    for r in data.get("resultList", {}).get("result", []):
        title = clean_text(r.get("title"))
        source = r.get("source","")
        is_pre = source.lower() in {"medrxiv","biorxiv","preprint"}
        rows.append({
            "source":"europe_pmc","source_stream":"preprint" if is_pre else "mixed","query":query,"record_id":record_id("europe_pmc", title, doi=r.get("doi",""), pmid=r.get("pmid","")),
            "title":title,"abstract":clean_text(r.get("abstractText")),"authors":clean_text(r.get("authorString")),
            "year":r.get("pubYear",""),"journal":r.get("journalTitle") or source,"doi":r.get("doi",""),
            "pmid":r.get("pmid",""),"pmcid":r.get("pmcid",""),"url":r.get("fullTextUrlList",{}).get("fullTextUrl",[{}])[0].get("url","") if r.get("fullTextUrlList") else "",
            "publication_type":r.get("pubType",""),"is_preprint":is_pre,"retrieved_at":now_iso()
        })
    return rows

def crossref_search(query, max_records):
    params = {"query.bibliographic": query, "rows": max_records, "select": "DOI,title,author,published-print,published-online,container-title,type,URL"}
    data = requests.get("https://api.crossref.org/works", params=params, timeout=30, headers={"User-Agent":"anti-ageing-review/0.1 (mailto:hssling@yahoo.com)"}).json()
    rows = []
    for r in data.get("message", {}).get("items", []):
        title = clean_text((r.get("title") or [""])[0])
        year = ""
        for k in ["published-print","published-online"]:
            if r.get(k, {}).get("date-parts"):
                year = str(r[k]["date-parts"][0][0]); break
        authors = "; ".join([clean_text(f"{a.get('family','')} {a.get('given','')}") for a in r.get("author", [])[:8]])
        rows.append({
            "source":"crossref","source_stream":"bibliographic","query":query,"record_id":record_id("crossref", title, doi=r.get("DOI","")),
            "title":title,"abstract":"","authors":authors,"year":year,"journal":(r.get("container-title") or [""])[0],
            "doi":r.get("DOI",""),"pmid":"","pmcid":"","url":r.get("URL",""),"publication_type":r.get("type",""),
            "is_preprint":"posted-content" in str(r.get("type","")).lower(),"retrieved_at":now_iso()
        })
    return rows

def run(cfg):
    root = cfg["_root"]
    terms = yaml.safe_load((root / "config/search_terms.yaml").read_text(encoding="utf-8"))
    queries = terms["queries"]["broad"] + terms["queries"]["narrow"]
    max_records = int(cfg["project"].get("max_records_per_query", 30))
    all_rows, run_rows = [], []
    for q in queries:
        for source, fn in [("pubmed", lambda: pubmed_search(q, max_records, cfg["project"].get("email",""))),
                           ("europe_pmc", lambda: europe_pmc_search(q, max_records)),
                           ("crossref", lambda: crossref_search(q, max_records))]:
            try:
                rows = fn()
                all_rows.extend(rows)
                run_rows.append({"timestamp":now_iso(),"source":source,"query":q,"records":len(rows),"status":"ok","error":""})
                time.sleep(0.34)
            except Exception as e:
                run_rows.append({"timestamp":now_iso(),"source":source,"query":q,"records":0,"status":"error","error":str(e)[:300]})
    raw = pd.DataFrame(all_rows)
    runs = pd.DataFrame(run_rows)
    save_csv(raw, cfg["paths"]["results_tables"] / "raw_records_all.csv")
    save_csv(runs, cfg["paths"]["results_tables"] / "search_runs.csv")
    save_csv(raw, cfg["paths"]["data_raw"] / f"raw_records_{cfg['project']['run_label']}.csv")
    append_log(cfg["paths"]["logs"] / "progress.md", "Phase 2 - Source Discovery and Search Automation",
               f"- Ran {len(queries)} query strings across PubMed, Europe PMC, and Crossref.\n- Retrieved {len(raw)} raw metadata rows.",
               "- results/tables/search_runs.csv\n- results/tables/raw_records_all.csv",
               "- Full search should be rerun with larger record caps before submission.\n- Full-text retrieval remains pending.",
               "- PubMed abstracts are not fetched in this pilot pass; Europe PMC abstracts support screening where available.\n- Crossref metadata is abstract-limited.",
               "python src/dedup/deduplicate.py --config config/review_config.yaml")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/review_config.yaml")
    run(load_config(ap.parse_args().config))
