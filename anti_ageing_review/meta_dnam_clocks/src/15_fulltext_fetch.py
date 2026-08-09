"""Phase 5c: Fetch open-access full text for included studies (Europe PMC XML first, Unpaywall PDF fallback)."""
from __future__ import annotations
import argparse
import csv
import sys
import time
from pathlib import Path
from xml.etree import ElementTree as ET

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).parent))
from _common import load_config, log, ensure_dirs, now_iso

UA = "dnam-clocks-meta/1.0 (mailto:hssling@gmail.com)"
HEADERS = {"User-Agent": UA}


def _get(url, params=None, retries=3, sleep=1.0, stream=False):
    for i in range(retries):
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=30, stream=stream)
            if r.status_code == 200:
                return r
        except Exception:
            pass
        time.sleep(sleep * (2 ** i))
    return None


def find_pmcid(pmid):
    if not pmid or str(pmid).lower() == "nan":
        return None
    pmid_clean = str(pmid).replace(".0", "").strip()
    if not pmid_clean.isdigit():
        return None
    r = _get(
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search",
        params={"query": f"ext_id:{pmid_clean} src:med", "resultType": "core", "format": "json"},
    )
    if r is None:
        return None
    try:
        results = r.json().get("resultList", {}).get("result", [])
        if results:
            return results[0].get("pmcid")
    except Exception:
        pass
    return None


def fetch_epmc_xml(pmcid, dest):
    pmcid_clean = pmcid.replace("PMC", "") if pmcid else ""
    if not pmcid_clean:
        return False, "no_pmcid"
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/PMC{pmcid_clean}/fullTextXML"
    r = _get(url)
    if r is None:
        return False, "epmc_xml_unreachable"
    if len(r.content) < 1000 or b"<error" in r.content[:200].lower():
        return False, "epmc_xml_empty_or_error"
    dest.write_bytes(r.content)
    return True, "ok"


def fetch_unpaywall_pdf(doi, dest):
    if not doi or str(doi).lower() == "nan":
        return False, "no_doi"
    doi_clean = str(doi).strip()
    r = _get(f"https://api.unpaywall.org/v2/{doi_clean}", params={"email": "hssling@gmail.com"})
    if r is None:
        return False, "unpaywall_unreachable"
    try:
        j = r.json()
        loc = j.get("best_oa_location") or {}
        pdf_url = loc.get("url_for_pdf")
        if not pdf_url:
            return False, "no_oa_pdf"
        pr = _get(pdf_url, stream=True)
        if pr is None or len(pr.content) < 1000:
            return False, "pdf_download_failed"
        dest.write_bytes(pr.content)
        return True, "ok"
    except Exception as e:
        return False, f"unpaywall_parse_err:{e}"


def inspect_xml(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        has_results = False
        for sec in root.iter("sec"):
            title_el = sec.find("title")
            title_text = title_el.text if title_el is not None and title_el.text else ""
            sec_type = sec.get("sec-type") or ""
            combined = (sec_type + " " + title_text).lower()
            if "result" in combined:
                has_results = True
                break
        has_table = any(True for _ in root.iter("table-wrap"))
        return has_results, has_table
    except Exception:
        return False, False


def run(cfg):
    proc = Path(cfg["paths"]["data_processed"])
    raw = Path(cfg["paths"]["data_raw"])
    ft_dir = raw / "fulltext"
    ensure_dirs(proc, raw, ft_dir)
    fdate = cfg["project"]["freeze_date"]
    inc = pd.read_csv(proc / f"included_studies_{fdate}.csv").fillna("")
    inc = inc.drop_duplicates(subset=["study_id"]).reset_index(drop=True)
    rows = []
    counts = {
        "retrieved_xml": 0,
        "retrieved_pdf": 0,
        "failed": 0,
        "with_results_section": 0,
        "with_table": 0,
    }
    for _, r in inc.iterrows():
        sid = r["study_id"]
        pmid = r.get("pmid", "")
        doi = r.get("doi", "")
        method = "none"
        status = "failed"
        fpath = ""
        size = 0
        has_results = "unknown"
        has_table = "unknown"

        # Try Europe PMC XML
        pmcid = find_pmcid(pmid)
        if pmcid:
            dest = ft_dir / f"{sid}.xml"
            ok, why = fetch_epmc_xml(pmcid, dest)
            if ok:
                method = "epmc_xml"
                status = "retrieved"
                fpath = str(dest)
                size = dest.stat().st_size
                hr, ht = inspect_xml(dest)
                has_results = "yes" if hr else "no"
                has_table = "yes" if ht else "no"
                counts["retrieved_xml"] += 1
                if hr:
                    counts["with_results_section"] += 1
                if ht:
                    counts["with_table"] += 1

        # Fallback Unpaywall PDF
        if status != "retrieved":
            dest = ft_dir / f"{sid}.pdf"
            ok, why = fetch_unpaywall_pdf(doi, dest)
            if ok:
                method = "unpaywall_pdf"
                status = "retrieved"
                fpath = str(dest)
                size = dest.stat().st_size
                counts["retrieved_pdf"] += 1
            else:
                counts["failed"] += 1
                status = f"failed:{why}"

        log(
            "study_processed",
            study_id=sid,
            method=method,
            status=status,
            size=size,
        )
        rows.append(
            {
                "study_id": sid,
                "doi": doi,
                "pmid": pmid,
                "retrieval_method": method,
                "retrieval_status": status,
                "file_path": fpath,
                "file_size_bytes": size,
                "has_results_section": has_results,
                "has_numeric_table": has_table,
            }
        )
        time.sleep(1.0)

    out_path = proc / f"fulltext_inventory_{fdate}.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for row in rows:
            w.writerow(row)
    log("fulltext_fetch_done", **counts, total=len(rows), path=str(out_path))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    run(load_config(ap.parse_args().config))
