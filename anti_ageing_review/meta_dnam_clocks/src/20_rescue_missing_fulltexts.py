"""Targeted full-text rescue for records awaiting full text."""
from __future__ import annotations
import argparse
import re
import sys
import time
from pathlib import Path
from urllib.parse import quote
import pandas as pd
import requests
sys.path.insert(0, str(Path(__file__).parent))
from _common import ensure_dirs, load_config, log  # noqa: E402


HEADERS = {"User-Agent": "dnam-clocks-review/1.0 (mailto:hssling@yahoo.com)"}


def clean(value) -> str:
    text = str(value or "").strip()
    if text.endswith(".0") and text[:-2].isdigit():
        return text[:-2]
    return text


def get(url, params=None, stream=False, timeout=45):
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=timeout, stream=stream, allow_redirects=True)
        if r.status_code == 200:
            return r
    except Exception:
        return None
    return None


def epmc_search(row) -> dict:
    doi = clean(row.get("doi", ""))
    pmid = clean(row.get("pmid", ""))
    title = clean(row.get("title", ""))
    query = ""
    if pmid:
        query = f"EXT_ID:{pmid} SRC:MED"
    elif doi:
        query = f'DOI:"{doi}"'
    else:
        query = f'TITLE:"{title[:120]}"'
    r = get("https://www.ebi.ac.uk/europepmc/webservices/rest/search", params={"query": query, "format": "json", "resultType": "core"})
    if not r:
        return {}
    try:
        results = r.json().get("resultList", {}).get("result", [])
        return results[0] if results else {}
    except Exception:
        return {}


def fetch_epmc_xml(pmcid: str, dest: Path) -> tuple[bool, str]:
    if not pmcid:
        return False, "no_pmcid"
    pmcid = pmcid if pmcid.upper().startswith("PMC") else f"PMC{pmcid}"
    r = get(f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML")
    if not r or len(r.content) < 1000:
        return False, "no_epmc_xml"
    dest.write_bytes(r.content)
    return True, "epmc_xml"


def fetch_unpaywall(doi: str, dest: Path) -> tuple[bool, str]:
    if not doi:
        return False, "no_doi"
    r = get(f"https://api.unpaywall.org/v2/{doi}", params={"email": "hssling@yahoo.com"})
    if not r:
        return False, "unpaywall_unreachable"
    try:
        data = r.json()
    except Exception:
        return False, "unpaywall_bad_json"
    locations = []
    if data.get("best_oa_location"):
        locations.append(data["best_oa_location"])
    locations.extend(data.get("oa_locations") or [])
    for loc in locations:
        for key in ["url_for_pdf", "url"]:
            url = loc.get(key)
            if not url:
                continue
            rr = get(url, stream=True)
            if rr and len(rr.content) > 1000:
                suffix = ".pdf" if b"%PDF" in rr.content[:20] or url.lower().endswith(".pdf") else ".html"
                final = dest.with_suffix(suffix)
                final.write_bytes(rr.content)
                return True, f"unpaywall_{key}"
    return False, "no_oa_location_downloaded"


def fetch_medrxiv_biorxiv(doi: str, dest: Path) -> tuple[bool, str]:
    if not doi or "1101/" not in doi:
        return False, "not_rxiv_doi"
    for server in ["medrxiv", "biorxiv"]:
        url = f"https://www.{server}.org/content/{doi}v1.full.pdf"
        r = get(url, stream=True)
        if r and len(r.content) > 1000 and b"%PDF" in r.content[:50]:
            dest.write_bytes(r.content)
            return True, f"{server}_pdf_v1"
        url = f"https://www.{server}.org/content/{doi}.full.pdf"
        r = get(url, stream=True)
        if r and len(r.content) > 1000 and b"%PDF" in r.content[:50]:
            dest.write_bytes(r.content)
            return True, f"{server}_pdf"
    return False, "rxiv_pdf_not_found"


def run(cfg):
    freeze = cfg["project"]["freeze_date"]
    proc = Path(cfg["paths"]["data_processed"])
    raw = Path(cfg["paths"]["data_raw"])
    ft_dir = raw / "fulltext"
    tabs = Path(cfg["paths"]["results_tabs"])
    ensure_dirs(ft_dir, tabs)
    audit = pd.read_csv(proc / f"fulltext_eligibility_audit_{freeze}.csv").fillna("")
    missing = audit[audit["first_reviewer_fulltext_decision"].eq("await_fulltext")].copy()
    rows = []
    for _, row in missing.iterrows():
        sid = row["study_id"]
        doi = clean(row.get("doi", ""))
        xml_dest = ft_dir / f"{sid}.xml"
        pdf_dest = ft_dir / f"{sid}.pdf"
        status = "failed"
        method = ""
        path = ""
        epmc = epmc_search(row)
        if epmc.get("pmcid"):
            ok, method = fetch_epmc_xml(epmc["pmcid"], xml_dest)
            if ok:
                status = "retrieved"
                path = str(xml_dest)
        if status != "retrieved":
            ok, method = fetch_unpaywall(doi, pdf_dest)
            if ok:
                status = "retrieved"
                path = str(next(ft_dir.glob(f"{sid}.*")))
        if status != "retrieved":
            ok, method = fetch_medrxiv_biorxiv(doi, pdf_dest)
            if ok:
                status = "retrieved"
                path = str(pdf_dest)
        rows.append({
            "study_id": sid,
            "title": row.get("title", ""),
            "doi": doi,
            "pmid": clean(row.get("pmid", "")),
            "rescue_status": status,
            "rescue_method": method,
            "local_path": path,
            "epmc_pmcid": epmc.get("pmcid", ""),
            "epmc_is_open_access": epmc.get("isOpenAccess", ""),
        })
        log("rescue_fulltext", study_id=sid, status=status, method=method)
        time.sleep(0.7)
    out = pd.DataFrame(rows)
    out.to_csv(tabs / f"missing_fulltext_rescue_log_{freeze}.csv", index=False)
    log("rescue_missing_fulltexts_done", retrieved=int(out["rescue_status"].eq("retrieved").sum()), total=len(out))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True)
    run(load_config(ap.parse_args().config))
