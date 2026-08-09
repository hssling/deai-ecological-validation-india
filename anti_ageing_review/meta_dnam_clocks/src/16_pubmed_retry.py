"""PubMed retry with PubMed-friendly tagged-field Boolean syntax."""
from __future__ import annotations
import argparse, json, importlib.util, sys, time
from pathlib import Path
import pandas as pd, requests

sys.path.insert(0, str(Path(__file__).parent))
from _common import load_config, log, ensure_dirs, now_iso

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("sm", ROOT / "01_search_dnam.py")
sm = importlib.util.module_from_spec(spec); spec.loader.exec_module(sm)
dm_spec = importlib.util.spec_from_file_location("dm", ROOT / "03_dedup_merge.py")
dm = importlib.util.module_from_spec(dm_spec); dm_spec.loader.exec_module(dm)

UA = "dnam-clocks-meta/1.0 (mailto:hssling@gmail.com)"
H = {"User-Agent": UA}

QUERY = (
    "((DunedinPACE[tiab] OR GrimAge[tiab] OR PhenoAge[tiab] OR \"Horvath clock\"[tiab] "
    "OR \"Hannum clock\"[tiab] OR \"epigenetic age\"[tiab] OR \"epigenetic clock\"[tiab] "
    "OR \"DNA methylation age\"[tiab] OR \"DNAm age\"[tiab] OR PCClock*[tiab] OR DNAmTL[tiab])) "
    "AND (randomized[tiab] OR randomised[tiab] OR trial[tiab] OR intervention[tiab] "
    "OR supplement*[tiab] OR exercise[tiab] OR diet*[tiab] OR \"caloric restriction\"[tiab] "
    "OR rapamycin[tiab] OR metformin[tiab] OR NAD[tiab] OR senolytic*[tiab])"
)

def _get(url, params, retries=3, sleep=1.0):
    for i in range(retries):
        try:
            r = requests.get(url, params=params, headers=H, timeout=30)
            if r.status_code == 200: return r
        except Exception: pass
        time.sleep(sleep * (2**i))
    return None

def run(cfg):
    raw_dir = Path(cfg["paths"]["data_raw"])
    interim = Path(cfg["paths"]["data_interim"])
    ensure_dirs(raw_dir, interim)
    fdate = cfg["project"]["freeze_date"]
    r = _get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
             {"db":"pubmed","term":QUERY,"retmode":"json","retmax":2000})
    if r is None:
        log("pubmed_esearch_failed"); return
    ids = r.json().get("esearchresult",{}).get("idlist",[])
    log("pubmed_esearch_ok", n_ids=len(ids), query=QUERY[:100])
    if not ids:
        return
    records = []
    for batch_start in range(0, len(ids), 200):
        batch = ids[batch_start:batch_start+200]
        rr = _get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
                  {"db":"pubmed","id":",".join(batch),"retmode":"json"})
        if rr is None:
            continue
        payload = rr.json()
        out_p = raw_dir / f"pubmed_retry_{now_iso()[:10]}_batch{batch_start}.json"
        out_p.write_text(json.dumps(payload))
        records.extend(sm.normalize_pubmed(payload))
        time.sleep(0.5)
    # append to existing CSV
    inp = interim / f"raw_records_dnam_{fdate}.csv"
    existing = pd.read_csv(inp).fillna("") if inp.exists() else pd.DataFrame()
    existing_pmids = set(existing.get("pmid", pd.Series([],dtype=str)).astype(str).tolist())
    new_df = pd.DataFrame(records)
    if not new_df.empty:
        new_df = new_df[~new_df["pmid"].astype(str).isin(existing_pmids)]
    combined = pd.concat([existing, new_df], ignore_index=True) if not new_df.empty else existing
    combined.to_csv(inp, index=False)
    log("pubmed_appended", n_new=len(new_df), total=len(combined))
    # Re-run dedup
    b_path = interim / f"rescreen_existing_{fdate}.csv"
    b = pd.read_csv(b_path).fillna("") if b_path.exists() else pd.DataFrame()
    merged = pd.concat([combined, b], ignore_index=True)
    deduped = dm.dedup(merged)
    pool_path = interim / f"candidate_pool_{fdate}.csv"
    before = len(merged); deduped.to_csv(pool_path, index=False)
    log("pubmed_retry_done", n_new_pubmed=len(new_df), pool_before=before, pool_after=len(deduped))

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True)
    run(load_config(ap.parse_args().config))
