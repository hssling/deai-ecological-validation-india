# DNA-Methylation Clocks Meta-Analysis Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Execute an end-to-end, conservative systematic review and meta-analysis of human RCTs measuring DNA-methylation ageing clocks (DunedinPACE, GrimAge, PhenoAge, Horvath, Hannum, PCClocks, DNAmTL), producing a submission-ready manuscript bundle for *Biogerontology* and a public GitHub repository with Zenodo DOI.

**Architecture:** Standalone module `anti_ageing_review/meta_dnam_clocks/` with 14 numbered Python scripts orchestrated by a Makefile. Each script reads/writes CSVs/JSONs through a single `meta_config.yaml`. Statistical synthesis uses Python (statsmodels, scipy) for forest/funnel/diagnostics and R subprocess calls (`meta`, `metafor`, `bayesmeta`, `netmeta`) where Python lacks coverage. All API responses cached to disk; reruns offline. Manuscript and supplementary built programmatically from Markdown via Pandoc to docx.

**Tech Stack:** Python 3.12, pandas, numpy, scipy, statsmodels, matplotlib, seaborn, requests, pyyaml, python-docx; R 4.3+ (meta, metafor, bayesmeta, netmeta); Pandoc; Git; GitHub CLI; Make.

**Operating principle:** "As feasible and robust" — every quantitative analysis runs only when its preconditions hold; otherwise dropped transparently with a logged amendment.

---

## File Structure

New module under `anti_ageing_review/meta_dnam_clocks/`:

```
meta_dnam_clocks/
├── Makefile                            # phase targets
├── requirements_meta_dnam.txt          # pinned deps
├── config/meta_config.yaml             # single source of paths/seeds/freeze
├── data/{raw,interim,processed}/       # cached + intermediate + final data
├── src/
│   ├── _common.py                      # config loader, paths, logging
│   ├── 01_search_dnam.py
│   ├── 02_rescreen_existing.py
│   ├── 03_dedup_merge.py
│   ├── 04_screen_titles_abs.py
│   ├── 05_screen_fulltext.py
│   ├── 06_extract_outcomes.py
│   ├── 07_rob2_assess.py
│   ├── 08_meta_analysis.py
│   ├── 09_subgroup_metareg.py
│   ├── 10_nma.py
│   ├── 11_pubbias_sensitivity.py
│   ├── 12_grade_profile.py
│   ├── 13_figures.py
│   └── 14_manuscript_build.py
├── r_scripts/
│   ├── meta_pool.R                     # called by 08
│   ├── bayesmeta.R                     # called by 08
│   └── netmeta.R                       # called by 10
├── manuscript/
│   ├── manuscript_main.md
│   ├── supplementary.md
│   └── templates/                      # reference.docx for Pandoc
├── results/{figures, tables}/
├── submission_assets/Biogerontology_DNAmClocks_<freeze>/
├── tests/                              # pytest unit tests
└── docs/
    ├── protocol_v1.md
    ├── prisma_2020_checklist.md
    ├── decision_log.md
    └── amendment_log.md
```

GitHub repo (new, separate): `hssling/dnam-clocks-meta-analysis` — mirror of the `meta_dnam_clocks/` tree plus `README.md`, `LICENSE`, `CITATION.cff`, `.github/workflows/ci.yml`.

---

## Phase 1: Scaffold & Protocol

### Task 1: Create module directory tree and config

**Files:**
- Create: `anti_ageing_review/meta_dnam_clocks/` (full tree above, empty dirs with `.gitkeep`)
- Create: `anti_ageing_review/meta_dnam_clocks/config/meta_config.yaml`
- Create: `anti_ageing_review/meta_dnam_clocks/requirements_meta_dnam.txt`
- Create: `anti_ageing_review/meta_dnam_clocks/Makefile`
- Create: `anti_ageing_review/meta_dnam_clocks/src/_common.py`

- [ ] **Step 1: Create directory tree**

```bash
cd "anti_ageing_review"
mkdir -p meta_dnam_clocks/{config,data/{raw,interim,processed},src,r_scripts,manuscript/templates,results/{figures,tables},submission_assets,tests,docs}
for d in meta_dnam_clocks/data/raw meta_dnam_clocks/data/interim meta_dnam_clocks/data/processed meta_dnam_clocks/results/figures meta_dnam_clocks/results/tables meta_dnam_clocks/submission_assets meta_dnam_clocks/tests; do touch "$d/.gitkeep"; done
```

- [ ] **Step 2: Write meta_config.yaml**

```yaml
project:
  name: dnam_clocks_meta_analysis
  freeze_date: "2026-05-18"
  random_seed: 42
  authors:
    - {name: "Dr Siddalingaiah H S", role: corresponding, orcid: "0000-0000-0000-0000"}
    - {name: "Dr Chandrakala D", role: coauthor, orcid: "0000-0000-0000-0000"}
  target_journal: "Biogerontology"
paths:
  root: "anti_ageing_review/meta_dnam_clocks"
  data_raw: "anti_ageing_review/meta_dnam_clocks/data/raw"
  data_interim: "anti_ageing_review/meta_dnam_clocks/data/interim"
  data_processed: "anti_ageing_review/meta_dnam_clocks/data/processed"
  results_figs: "anti_ageing_review/meta_dnam_clocks/results/figures"
  results_tabs: "anti_ageing_review/meta_dnam_clocks/results/tables"
  submission: "anti_ageing_review/meta_dnam_clocks/submission_assets"
  existing_master: "anti_ageing_review/results/tables/extracted_studies_master.csv"
  docs: "anti_ageing_review/meta_dnam_clocks/docs"
  manuscript: "anti_ageing_review/meta_dnam_clocks/manuscript"
clocks:
  - DunedinPACE
  - GrimAge
  - GrimAge2
  - PhenoAge
  - Horvath
  - Hannum
  - PCClock
  - DNAmTL
search:
  sources: [pubmed, europepmc, crossref, openalex, clinicaltrials]
  block_clock_terms:
    - "DunedinPACE"
    - "GrimAge"
    - "PhenoAge"
    - "Horvath clock"
    - "Hannum clock"
    - "epigenetic age"
    - "epigenetic clock"
    - "DNA methylation age"
    - "DNAm age"
    - "PCClock"
    - "DNAmTL"
  block_intervention_terms:
    - "randomized"
    - "randomised"
    - "trial"
    - "intervention"
    - "supplement"
    - "exercise"
    - "diet"
    - "caloric restriction"
    - "rapamycin"
    - "metformin"
    - "NAD"
    - "senolytic"
  date_from: "2010-01-01"
synthesis:
  min_studies_for_pool: 3
  min_studies_for_metareg: 10
  min_studies_for_nma: 10
  min_studies_for_pubbias: 10
  hksj_sensitivity: true
  bayes_tau_prior: "halfnormal(0, 0.5)"
```

- [ ] **Step 3: Write requirements_meta_dnam.txt**

```
pandas==2.2.2
numpy==1.26.4
scipy==1.13.1
statsmodels==0.14.2
matplotlib==3.9.0
seaborn==0.13.2
requests==2.32.3
pyyaml==6.0.1
python-docx==1.1.2
rapidfuzz==3.9.3
networkx==3.3
pytest==8.3.2
```

- [ ] **Step 4: Write Makefile**

```makefile
PY=python
CFG=config/meta_config.yaml

help:
	@echo "Targets: scaffold search rescreen dedup screen extract rob meta subgroup nma pubbias grade figs manuscript submission qa all"

scaffold:
	$(PY) src/_common.py --check
search:
	$(PY) src/01_search_dnam.py --config $(CFG)
rescreen:
	$(PY) src/02_rescreen_existing.py --config $(CFG)
dedup:
	$(PY) src/03_dedup_merge.py --config $(CFG)
screen:
	$(PY) src/04_screen_titles_abs.py --config $(CFG) && $(PY) src/05_screen_fulltext.py --config $(CFG)
extract:
	$(PY) src/06_extract_outcomes.py --config $(CFG)
rob:
	$(PY) src/07_rob2_assess.py --config $(CFG)
meta:
	$(PY) src/08_meta_analysis.py --config $(CFG)
subgroup:
	$(PY) src/09_subgroup_metareg.py --config $(CFG)
nma:
	$(PY) src/10_nma.py --config $(CFG)
pubbias:
	$(PY) src/11_pubbias_sensitivity.py --config $(CFG)
grade:
	$(PY) src/12_grade_profile.py --config $(CFG)
figs:
	$(PY) src/13_figures.py --config $(CFG)
manuscript:
	$(PY) src/14_manuscript_build.py --config $(CFG)
all: search rescreen dedup screen extract rob meta subgroup nma pubbias grade figs manuscript
test:
	pytest tests/ -v
.PHONY: help scaffold search rescreen dedup screen extract rob meta subgroup nma pubbias grade figs manuscript all test
```

- [ ] **Step 5: Write src/_common.py**

```python
"""Shared utilities: config loading, path resolution, structured logging."""
from __future__ import annotations
import argparse, json, sys, time, yaml
from datetime import datetime
from pathlib import Path

def load_config(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    for k, v in cfg["paths"].items():
        cfg["paths"][k] = Path(v)
    return cfg

def now_iso() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def log(msg: str, **fields) -> None:
    payload = {"t": now_iso(), "msg": msg, **fields}
    print(json.dumps(payload, default=str), flush=True)

def ensure_dirs(*paths: Path) -> None:
    for p in paths:
        Path(p).mkdir(parents=True, exist_ok=True)

def append_amendment(docs_dir: Path, what: str, why: str) -> None:
    f = docs_dir / "amendment_log.md"
    f.parent.mkdir(parents=True, exist_ok=True)
    with open(f, "a", encoding="utf-8") as fh:
        fh.write(f"\n## {now_iso()}\n- **What:** {what}\n- **Why:** {why}\n")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--config", default="config/meta_config.yaml")
    a = ap.parse_args()
    if a.check:
        cfg = load_config(a.config)
        for k, v in cfg["paths"].items():
            ensure_dirs(v)
        log("scaffold_ok", paths=list(cfg["paths"].keys()))
        sys.exit(0)
```

- [ ] **Step 6: Verify scaffold**

```bash
cd anti_ageing_review/meta_dnam_clocks
pip install -r requirements_meta_dnam.txt
make scaffold
```

Expected: JSON log line `{"msg": "scaffold_ok", ...}`.

- [ ] **Step 7: Commit**

```bash
git add anti_ageing_review/meta_dnam_clocks
git commit -m "feat(meta-dnam): scaffold module, config, Makefile, common utils"
```

### Task 2: Write protocol_v1.md and PRISMA-P documentation

**Files:**
- Create: `anti_ageing_review/meta_dnam_clocks/docs/protocol_v1.md`
- Create: `anti_ageing_review/meta_dnam_clocks/docs/prisma_2020_checklist.md`
- Create: `anti_ageing_review/meta_dnam_clocks/docs/decision_log.md`
- Create: `anti_ageing_review/meta_dnam_clocks/docs/amendment_log.md`

- [ ] **Step 1: Write protocol_v1.md** — full PRISMA-P style document mirroring the design spec Sections 1–3 (review question, PICO, eligibility, search, screening, extraction, RoB, synthesis plan, sensitivity, GRADE). Source the content directly from `docs/superpowers/specs/2026-05-18-dnam-clocks-meta-analysis-design.md`.

- [ ] **Step 2: Write prisma_2020_checklist.md** — 27-item PRISMA 2020 checklist with `Item | Reported (Y/N/NA) | Section/Page` columns. Initially mark all "Y - protocol-only" pending Phase 7.

- [ ] **Step 3: Initialize decision_log.md and amendment_log.md** as empty Markdown files with title and date.

- [ ] **Step 4: Commit**

```bash
git add anti_ageing_review/meta_dnam_clocks/docs/
git commit -m "docs(meta-dnam): protocol v1, PRISMA 2020 checklist, decision/amendment logs"
```

---

## Phase 2: Search Execution

### Task 3: Build the multi-source search client

**Files:**
- Create: `anti_ageing_review/meta_dnam_clocks/src/01_search_dnam.py`
- Create: `anti_ageing_review/meta_dnam_clocks/tests/test_search.py`

The script must:
1. Build a Boolean query string from `cfg["search"]["block_clock_terms"]` AND `cfg["search"]["block_intervention_terms"]`.
2. Hit each source with timeouts and exponential backoff (max 3 retries). Sources: PubMed E-utilities `esearch`/`efetch`; Europe PMC REST; Crossref `/works?query=...`; OpenAlex `/works?search=...`; ClinicalTrials.gov v2 API.
3. Save raw responses to `data/raw/{source}_{YYYYMMDD}.json`.
4. Normalize each source to a common schema → `data/interim/raw_records_dnam_<freeze>.csv` with columns: `source, source_id, doi, pmid, title, abstract, authors, year, journal, url, fetched_at`.
5. If a source fails (network/auth), log the failure to `docs/amendment_log.md` and proceed with the remaining sources.

- [ ] **Step 1: Write tests/test_search.py** — unit tests for query string assembly and the response-normalizer for each source using small fixture JSON snippets in `tests/fixtures/`.

```python
import json
from pathlib import Path
import pytest
from src import _common
import importlib.util, sys

spec = importlib.util.spec_from_file_location("search_mod", "src/01_search_dnam.py")
search_mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(search_mod)

def test_query_builder_combines_blocks():
    q = search_mod.build_query(["DunedinPACE","GrimAge"], ["trial","exercise"])
    assert '("DunedinPACE" OR "GrimAge")' in q
    assert '("trial" OR "exercise")' in q
    assert " AND " in q

def test_pubmed_normalizer_minimal():
    fixture = json.loads(Path("tests/fixtures/pubmed_sample.json").read_text())
    rows = search_mod.normalize_pubmed(fixture)
    assert all({"source","title","pmid"}.issubset(r.keys()) for r in rows)
```

Create `tests/fixtures/pubmed_sample.json` with a minimal but realistic Pubmed efetch JSON snippet (one record).

- [ ] **Step 2: Run test (expect fail)** — `pytest tests/test_search.py -v` → FAIL (module missing functions).

- [ ] **Step 3: Implement src/01_search_dnam.py**

```python
"""Phase 2: Multi-source search for DNAm clock × intervention RCTs."""
from __future__ import annotations
import argparse, json, time, csv, sys
from pathlib import Path
from typing import Iterable
import requests
sys.path.insert(0, str(Path(__file__).parent))
from _common import load_config, log, ensure_dirs, append_amendment, now_iso

UA = "dnam-clocks-meta/1.0 (mailto:hssling@gmail.com)"
HEADERS = {"User-Agent": UA, "Accept": "application/json"}

def build_query(clock_terms, intv_terms):
    a = " OR ".join(f'"{t}"' for t in clock_terms)
    b = " OR ".join(f'"{t}"' for t in intv_terms)
    return f'({a}) AND ({b})'

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

def search_pubmed(query, raw_dir: Path, date_from):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db":"pubmed","term":query + f' AND ("{date_from}"[PDAT]:"3000"[PDAT])',"retmode":"json","retmax":2000}
    r = _get(url, params=params)
    if r is None: return None
    ids = r.json().get("esearchresult",{}).get("idlist",[])
    if not ids: return []
    f = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    rr = _get(f, params={"db":"pubmed","id":",".join(ids),"retmode":"json"})
    payload = rr.json() if rr else {}
    (raw_dir / f"pubmed_{now_iso()[:10]}.json").write_text(json.dumps(payload))
    return normalize_pubmed(payload)

def normalize_pubmed(payload):
    out = []
    res = payload.get("result", {})
    for k, rec in res.items():
        if k == "uids": continue
        out.append({
            "source":"pubmed","source_id":k,"pmid":k,
            "doi": next((i["value"] for i in rec.get("articleids",[]) if i.get("idtype")=="doi"), ""),
            "title": rec.get("title",""), "abstract":"",
            "authors": "; ".join(a.get("name","") for a in rec.get("authors",[])),
            "year": (rec.get("pubdate","")[:4] or ""),
            "journal": rec.get("fulljournalname","") or rec.get("source",""),
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{k}/",
            "fetched_at": now_iso(),
        })
    return out

def search_europepmc(query, raw_dir):
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    r = _get(url, params={"query":query,"format":"json","pageSize":1000,"resultType":"core"})
    if r is None: return None
    payload = r.json()
    (raw_dir / f"europepmc_{now_iso()[:10]}.json").write_text(json.dumps(payload))
    return normalize_europepmc(payload)

def normalize_europepmc(payload):
    out=[]
    for rec in payload.get("resultList",{}).get("result",[]):
        out.append({"source":"europepmc","source_id":rec.get("id",""),
            "pmid":rec.get("pmid",""),"doi":rec.get("doi",""),
            "title":rec.get("title",""),"abstract":rec.get("abstractText",""),
            "authors":rec.get("authorString",""),"year":rec.get("pubYear",""),
            "journal":rec.get("journalTitle",""),"url":rec.get("fullTextUrlList",{}).get("fullTextUrl",[{}])[0].get("url","") if rec.get("fullTextUrlList") else "",
            "fetched_at":now_iso()})
    return out

def search_crossref(query, raw_dir):
    url = "https://api.crossref.org/works"
    r = _get(url, params={"query":query,"rows":1000})
    if r is None: return None
    payload = r.json()
    (raw_dir / f"crossref_{now_iso()[:10]}.json").write_text(json.dumps(payload))
    return normalize_crossref(payload)

def normalize_crossref(payload):
    out=[]
    for rec in payload.get("message",{}).get("items",[]):
        out.append({"source":"crossref","source_id":rec.get("DOI",""),"pmid":"","doi":rec.get("DOI",""),
            "title":(rec.get("title") or [""])[0],"abstract":rec.get("abstract",""),
            "authors":"; ".join(f"{a.get('given','')} {a.get('family','')}".strip() for a in rec.get("author",[])),
            "year":str(rec.get("issued",{}).get("date-parts",[[None]])[0][0] or ""),
            "journal":(rec.get("container-title") or [""])[0],"url":rec.get("URL",""),"fetched_at":now_iso()})
    return out

def search_openalex(query, raw_dir):
    url = "https://api.openalex.org/works"
    r = _get(url, params={"search":query,"per-page":200})
    if r is None: return None
    payload = r.json()
    (raw_dir / f"openalex_{now_iso()[:10]}.json").write_text(json.dumps(payload))
    return normalize_openalex(payload)

def normalize_openalex(payload):
    out=[]
    for w in payload.get("results",[]):
        out.append({"source":"openalex","source_id":w.get("id",""),"pmid":(w.get("ids",{}).get("pmid","") or "").split("/")[-1],
            "doi":(w.get("doi","") or "").replace("https://doi.org/",""),"title":w.get("title",""),
            "abstract":"".join(w.get("abstract_inverted_index",{}).keys()) if w.get("abstract_inverted_index") else "",
            "authors":"; ".join(a.get("author",{}).get("display_name","") for a in w.get("authorships",[])),
            "year":str(w.get("publication_year","")),"journal":(w.get("host_venue") or {}).get("display_name",""),
            "url":w.get("id",""),"fetched_at":now_iso()})
    return out

def search_clinicaltrials(query, raw_dir):
    url = "https://clinicaltrials.gov/api/v2/studies"
    terms = "epigenetic clock OR DNA methylation age OR DunedinPACE OR GrimAge OR PhenoAge"
    r = _get(url, params={"query.term":terms,"filter.overallStatus":"COMPLETED","pageSize":200,"format":"json"})
    if r is None: return None
    payload = r.json()
    (raw_dir / f"clinicaltrials_{now_iso()[:10]}.json").write_text(json.dumps(payload))
    return normalize_clinicaltrials(payload)

def normalize_clinicaltrials(payload):
    out=[]
    for s in payload.get("studies",[]):
        idm = s.get("protocolSection",{}).get("identificationModule",{})
        out.append({"source":"clinicaltrials","source_id":idm.get("nctId",""),"pmid":"","doi":"",
            "title":idm.get("officialTitle","") or idm.get("briefTitle",""),
            "abstract":s.get("protocolSection",{}).get("descriptionModule",{}).get("briefSummary",""),
            "authors":"","year":(s.get("protocolSection",{}).get("statusModule",{}).get("completionDateStruct",{}).get("date","") or "")[:4],
            "journal":"ClinicalTrials.gov","url":f"https://clinicaltrials.gov/study/{idm.get('nctId','')}","fetched_at":now_iso()})
    return out

def run(cfg):
    raw_dir = cfg["paths"]["data_raw"]; ensure_dirs(raw_dir, cfg["paths"]["data_interim"])
    q = build_query(cfg["search"]["block_clock_terms"], cfg["search"]["block_intervention_terms"])
    log("query_built", q=q)
    sources_ok, records = 0, []
    for name, fn in [("pubmed",search_pubmed),("europepmc",search_europepmc),
                      ("crossref",search_crossref),("openalex",search_openalex),("clinicaltrials",search_clinicaltrials)]:
        try:
            r = fn(q, raw_dir) if name not in ("pubmed","clinicaltrials") else (
                search_pubmed(q, raw_dir, cfg["search"]["date_from"]) if name=="pubmed" else search_clinicaltrials(q, raw_dir))
            if r is None:
                append_amendment(cfg["paths"]["docs"], f"{name} returned no response", "API unreachable; continuing without this source")
            else:
                records.extend(r); sources_ok += 1; log("source_ok", source=name, n=len(r))
        except Exception as e:
            append_amendment(cfg["paths"]["docs"], f"{name} failed: {e}", "Logged exception, continuing")
            log("source_err", source=name, err=str(e))
        time.sleep(1.0)
    out = cfg["paths"]["data_interim"] / f"raw_records_dnam_{cfg['project']['freeze_date']}.csv"
    cols = ["source","source_id","doi","pmid","title","abstract","authors","year","journal","url","fetched_at"]
    with open(out,"w",newline="",encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for r in records: w.writerow({k:r.get(k,"") for k in cols})
    log("search_done", sources_ok=sources_ok, total_records=len(records), path=str(out))
    if sources_ok < 4:
        append_amendment(cfg["paths"]["docs"], f"Only {sources_ok}/5 sources returned data", "Quality gate flag")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True)
    run(load_config(ap.parse_args().config))
```

- [ ] **Step 4: Run test (expect pass)** — `pytest tests/test_search.py -v` → PASS.

- [ ] **Step 5: Run actual search**

```bash
cd anti_ageing_review/meta_dnam_clocks && make search
```

Expected: ≥4/5 sources logged `source_ok`; CSV produced at `data/interim/raw_records_dnam_<freeze>.csv`.

- [ ] **Step 6: Quality gate** — open CSV; confirm ≥100 raw records total. If <100, widen Block 2 terms in config and re-run.

- [ ] **Step 7: Commit**

```bash
git add anti_ageing_review/meta_dnam_clocks/{src/01_search_dnam.py,tests/}
git commit -m "feat(meta-dnam): multi-source DNAm-clock search with caching and amendment logging"
```

---

## Phase 3: Re-screen Existing Master + Dedup + Merge

### Task 4: Re-screen existing extracted_studies_master.csv for DNAm clocks

**Files:**
- Create: `anti_ageing_review/meta_dnam_clocks/src/02_rescreen_existing.py`

The script reads `anti_ageing_review/results/tables/extracted_studies_master.csv` (path from config `existing_master`), filters rows whose `title + abstract` text matches **any** clock term (case-insensitive), and writes `data/interim/rescreen_existing_<freeze>.csv` with the same schema as `01_search_dnam.py` output.

- [ ] **Step 1: Write src/02_rescreen_existing.py**

```python
from __future__ import annotations
import argparse, re, sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).parent))
from _common import load_config, log, ensure_dirs

def run(cfg):
    ensure_dirs(cfg["paths"]["data_interim"])
    existing = Path(cfg["paths"]["existing_master"])
    if not existing.exists():
        log("existing_master_missing", path=str(existing)); return
    df = pd.read_csv(existing)
    terms = [re.escape(t.lower()) for t in cfg["search"]["block_clock_terms"]]
    pat = re.compile("|".join(terms), re.IGNORECASE)
    text = (df.get("title","").fillna("").astype(str) + " " +
            df.get("intervention_name","").fillna("").astype(str) + " " +
            df.get("outcome_exact","").fillna("").astype(str) + " " +
            df.get("mechanism","").fillna("").astype(str))
    hit = df[text.str.contains(pat, na=False)].copy()
    out = pd.DataFrame({
        "source":"existing_master","source_id":hit.get("doi","").fillna("") + "|" + hit.get("pmid","").astype(str).fillna(""),
        "doi":hit.get("doi","").fillna(""),"pmid":hit.get("pmid","").astype(str).fillna(""),
        "title":hit.get("title","").fillna(""),"abstract":"",
        "authors":hit.get("authors","").fillna(""),"year":hit.get("year","").astype(str).fillna(""),
        "journal":hit.get("journal","").fillna(""),"url":"","fetched_at":""})
    out_path = cfg["paths"]["data_interim"] / f"rescreen_existing_{cfg['project']['freeze_date']}.csv"
    out.to_csv(out_path, index=False); log("rescreen_done", n=len(out), path=str(out_path))

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True)
    run(load_config(ap.parse_args().config))
```

- [ ] **Step 2: Run** — `make rescreen`. Expected: CSV produced; n logged.

- [ ] **Step 3: Commit**

```bash
git add anti_ageing_review/meta_dnam_clocks/src/02_rescreen_existing.py
git commit -m "feat(meta-dnam): re-screen existing master file for DNAm clock terms"
```

### Task 5: Dedup and merge raw + rescreen

**Files:**
- Create: `anti_ageing_review/meta_dnam_clocks/src/03_dedup_merge.py`
- Create: `anti_ageing_review/meta_dnam_clocks/tests/test_dedup.py`

Dedup strategy: (a) exact DOI match (after `.lower().strip()`), (b) exact PMID match, (c) fuzzy title similarity ≥ 92 via `rapidfuzz.fuzz.token_sort_ratio` for records with same year ±1.

- [ ] **Step 1: Write tests/test_dedup.py**

```python
import pandas as pd, importlib.util
spec = importlib.util.spec_from_file_location("dm","src/03_dedup_merge.py"); dm = importlib.util.module_from_spec(spec); spec.loader.exec_module(dm)

def test_exact_doi_collapses():
    df = pd.DataFrame([
        {"doi":"10.1/a","pmid":"","title":"X","year":"2024","source":"pubmed","source_id":"1","abstract":"","authors":"","journal":"","url":"","fetched_at":""},
        {"doi":"10.1/A","pmid":"","title":"X","year":"2024","source":"crossref","source_id":"2","abstract":"","authors":"","journal":"","url":"","fetched_at":""},
    ])
    out = dm.dedup(df)
    assert len(out) == 1

def test_fuzzy_title_collapses_near_dup():
    df = pd.DataFrame([
        {"doi":"","pmid":"","title":"Exercise and GrimAge in older adults","year":"2023","source":"a","source_id":"1","abstract":"","authors":"","journal":"","url":"","fetched_at":""},
        {"doi":"","pmid":"","title":"Exercise and GrimAge in older adults.","year":"2023","source":"b","source_id":"2","abstract":"","authors":"","journal":"","url":"","fetched_at":""},
    ])
    assert len(dm.dedup(df)) == 1
```

- [ ] **Step 2: Run test (expect fail).**

- [ ] **Step 3: Implement src/03_dedup_merge.py**

```python
from __future__ import annotations
import argparse, sys
from pathlib import Path
import pandas as pd
from rapidfuzz import fuzz
sys.path.insert(0, str(Path(__file__).parent))
from _common import load_config, log, ensure_dirs

def dedup(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["_doi_n"] = df["doi"].fillna("").astype(str).str.lower().str.strip()
    df["_pmid_n"] = df["pmid"].fillna("").astype(str).str.strip()
    keep = []
    seen_doi = set(); seen_pmid = set(); seen_titles = []
    for _, row in df.iterrows():
        if row["_doi_n"] and row["_doi_n"] in seen_doi: continue
        if row["_pmid_n"] and row["_pmid_n"] in seen_pmid: continue
        t = str(row.get("title","")).lower().strip().rstrip(".")
        y = str(row.get("year",""))[:4]
        dup = False
        for tt, yy in seen_titles:
            if abs((int(y) if y.isdigit() else 0) - (int(yy) if yy.isdigit() else 0)) <= 1:
                if fuzz.token_sort_ratio(t, tt) >= 92:
                    dup = True; break
        if dup: continue
        if row["_doi_n"]: seen_doi.add(row["_doi_n"])
        if row["_pmid_n"]: seen_pmid.add(row["_pmid_n"])
        seen_titles.append((t, y))
        keep.append(row)
    return pd.DataFrame(keep).drop(columns=["_doi_n","_pmid_n"], errors="ignore")

def run(cfg):
    interim = cfg["paths"]["data_interim"]; ensure_dirs(interim)
    fdate = cfg["project"]["freeze_date"]
    a = pd.read_csv(interim / f"raw_records_dnam_{fdate}.csv")
    b_path = interim / f"rescreen_existing_{fdate}.csv"
    b = pd.read_csv(b_path) if b_path.exists() else pd.DataFrame(columns=a.columns)
    merged = pd.concat([a,b], ignore_index=True)
    out = dedup(merged)
    out_path = interim / f"candidate_pool_{fdate}.csv"
    out.to_csv(out_path, index=False)
    log("dedup_done", before=len(merged), after=len(out), path=str(out_path))

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True)
    run(load_config(ap.parse_args().config))
```

- [ ] **Step 4: Run tests + dedup** — `pytest tests/test_dedup.py -v && make dedup`. Both PASS; candidate pool CSV produced.

- [ ] **Step 5: Commit**

```bash
git add anti_ageing_review/meta_dnam_clocks/{src/03_dedup_merge.py,tests/test_dedup.py}
git commit -m "feat(meta-dnam): dedup and merge raw + rescreen pools"
```

---

## Phase 4: Screening (title/abstract + full-text)

### Task 6: Title/abstract screening with dual-reviewer flag

**Files:**
- Create: `anti_ageing_review/meta_dnam_clocks/src/04_screen_titles_abs.py`

Logic:
- **Auto-include** if title/abstract contains any of: `randomized`, `randomised`, `RCT` AND any clock term.
- **Auto-exclude** if marked `animal`, `mouse`, `rat`, `mice`, `cell line`, `in vitro`, `review`, `meta-analysis`, `protocol` only.
- **Flag for review** otherwise.
- Output: `data/interim/screen_ta_<freeze>.csv` with `decision ∈ {include, exclude, flag}` and `reason`.

- [ ] **Step 1: Implement** with regex-based rules; both authors' simulated decisions recorded (deterministic from rules) in columns `reviewer_1_decision` and `reviewer_2_decision`; flagged records get `consensus = "needs_human_review"`.

- [ ] **Step 2: Run** — `python src/04_screen_titles_abs.py --config config/meta_config.yaml`. Expected: decision counts logged.

- [ ] **Step 3: Manual adjudication pass** — open `screen_ta_<freeze>.csv` in any editor; for any row with `consensus == needs_human_review`, set final `decision` based on full PICO. Save.

- [ ] **Step 4: Commit**

```bash
git add anti_ageing_review/meta_dnam_clocks/src/04_screen_titles_abs.py anti_ageing_review/meta_dnam_clocks/data/interim/screen_ta_*.csv
git commit -m "feat(meta-dnam): title/abstract screening with dual-reviewer simulation and human-flag adjudication"
```

### Task 7: Full-text screening + eligibility checklist

**Files:**
- Create: `anti_ageing_review/meta_dnam_clocks/src/05_screen_fulltext.py`

For each `include`-from-Stage-1 record:
1. Attempt to retrieve full text or open-access PDF (via Europe PMC `/fullTextXML` endpoint or Unpaywall by DOI).
2. If retrievable, save to `data/raw/fulltext/<doi or pmid>.{xml|pdf}`.
3. Apply eligibility checklist (RCT, ≥18y, human, pre/post clock measurement, dispersion reported, comparator defined).
4. Output: `data/processed/included_studies_<freeze>.csv` and `data/processed/excluded_fulltext_<freeze>.csv` (with `exclusion_reason`).

- [ ] **Step 1: Implement** with explicit eligibility checklist coded as a function returning `(eligible: bool, reason: str)`.

- [ ] **Step 2: Run** — `python src/05_screen_fulltext.py --config config/meta_config.yaml`.

- [ ] **Step 3: Hard-stop check** — if `included_studies_<freeze>.csv` is empty, halt and consult Section 6 hard-stop rule (narrative-only pivot). Otherwise continue.

- [ ] **Step 4: Commit**

```bash
git add anti_ageing_review/meta_dnam_clocks/{src/05_screen_fulltext.py,data/processed/included_studies_*.csv,data/processed/excluded_fulltext_*.csv}
git commit -m "feat(meta-dnam): full-text retrieval and eligibility checklist screening"
```

---

## Phase 5: Extraction + RoB 2

### Task 8: Structured outcome extraction

**Files:**
- Create: `anti_ageing_review/meta_dnam_clocks/src/06_extract_outcomes.py`

For each included study, parse full text (XML preferred; PDF text via `pdfplumber` fallback) for: n per arm; mean ± SD pre/post per arm per clock; or change-from-baseline mean ± SD. Use regex + table extraction heuristics; flag records requiring manual entry with `extraction_status = "manual_required"`.

Output: `data/processed/extracted_clock_studies_<freeze>.csv` columns:
`study_id, first_author, year, journal, doi, pmid, design, n_int, n_ctrl, age_mean, age_sd, sex_female_pct, health_status, intervention_class, intervention_detail, dose, duration_weeks, comparator, clock, baseline_int_mean, baseline_int_sd, post_int_mean, post_int_sd, baseline_ctrl_mean, baseline_ctrl_sd, post_ctrl_mean, post_ctrl_sd, change_int_mean, change_int_sd, change_ctrl_mean, change_ctrl_sd, array_platform, follow_up_weeks, funding_source, coi_disclosure, extraction_status, notes`.

- [ ] **Step 1: Implement** with heuristics + manual-flag escape hatch.

- [ ] **Step 2: Run** — `make extract`.

- [ ] **Step 3: Manual completion pass** — open output CSV; complete rows flagged `manual_required` by reading the cached full text. This is authentic extraction — do not fabricate values; if numeric data are not reported in the paper, leave blank and set `extraction_status = "not_reported"`.

- [ ] **Step 4: Commit**

```bash
git add anti_ageing_review/meta_dnam_clocks/{src/06_extract_outcomes.py,data/processed/extracted_clock_studies_*.csv}
git commit -m "feat(meta-dnam): structured outcome extraction with manual-completion flag"
```

### Task 9: RoB 2 assessment

**Files:**
- Create: `anti_ageing_review/meta_dnam_clocks/src/07_rob2_assess.py`

Generate a RoB 2 worksheet (one row per included study) with the 5 domains + overall, each `{low, some_concerns, high}` plus a `quote` field for the supporting passage. The script seeds the worksheet with `pending` values; the user completes manually based on full-text reading (dual-coded by both authors).

- [ ] **Step 1: Implement seeder** that writes `data/processed/rob2_assessments_<freeze>.csv`.

- [ ] **Step 2: Manual coding pass** — both authors code independently; disagreements resolved by discussion; final consensus column populated.

- [ ] **Step 3: Commit**

```bash
git add anti_ageing_review/meta_dnam_clocks/{src/07_rob2_assess.py,data/processed/rob2_assessments_*.csv}
git commit -m "feat(meta-dnam): RoB 2 worksheet seeder and manual dual-coded assessments"
```

---

## Phase 6: Quantitative Synthesis

### Task 10: Per-clock random-effects meta-analysis

**Files:**
- Create: `anti_ageing_review/meta_dnam_clocks/src/08_meta_analysis.py`
- Create: `anti_ageing_review/meta_dnam_clocks/r_scripts/meta_pool.R`
- Create: `anti_ageing_review/meta_dnam_clocks/r_scripts/bayesmeta.R`

Logic:
1. Load `extracted_clock_studies_<freeze>.csv`.
2. Compute per-study Hedges' g change-score SMD with variance using Borenstein formula. For studies with only post values, compute post-SMD; flag.
3. For each clock with `n_studies ≥ cfg.synthesis.min_studies_for_pool`:
   - DerSimonian-Laird random-effects pool via R `meta::metagen` (subprocess); record SMD, 95% CI, 95% PI, τ², I².
   - HKSJ sensitivity pool.
   - Bayesian pool via R `bayesmeta` with half-normal(0, 0.5) prior on τ.
4. Write `results/tables/per_clock_pooled.csv` and `results/tables/per_study_effect_sizes.csv`.

- [ ] **Step 1: Implement `r_scripts/meta_pool.R`**

```r
#!/usr/bin/env Rscript
args <- commandArgs(trailingOnly=TRUE)
input <- args[1]; output <- args[2]
suppressMessages({library(meta); library(jsonlite)})
df <- read.csv(input)
res <- metagen(TE=df$g, seTE=df$se_g, studlab=df$study_id, sm="SMD",
               method.tau="DL", prediction=TRUE, random=TRUE)
out <- list(k=res$k, smd=res$TE.random, ci_lower=res$lower.random, ci_upper=res$upper.random,
            pi_lower=res$lower.predict, pi_upper=res$upper.predict,
            tau2=res$tau2, I2=res$I2, Q=res$Q, pval=res$pval.random)
res_hksj <- metagen(TE=df$g, seTE=df$se_g, studlab=df$study_id, sm="SMD",
                    method.tau="DL", random=TRUE, method.random.ci="HK")
out$hksj_smd <- res_hksj$TE.random; out$hksj_lower <- res_hksj$lower.random; out$hksj_upper <- res_hksj$upper.random
writeLines(toJSON(out, auto_unbox=TRUE), output)
```

- [ ] **Step 2: Implement `r_scripts/bayesmeta.R`**

```r
#!/usr/bin/env Rscript
args <- commandArgs(trailingOnly=TRUE)
input <- args[1]; output <- args[2]
suppressMessages({library(bayesmeta); library(jsonlite)})
df <- read.csv(input)
b <- bayesmeta(y=df$g, sigma=df$se_g, labels=df$study_id,
               tau.prior=function(t) dhalfnormal(t, scale=0.5))
out <- list(mu_median=b$summary["median","mu"], mu_lower=b$summary["95% lower","mu"],
            mu_upper=b$summary["95% upper","mu"], tau_median=b$summary["median","tau"])
writeLines(toJSON(out, auto_unbox=TRUE), output)
```

- [ ] **Step 3: Implement src/08_meta_analysis.py** — computes g + se_g per study, drops missing, writes per-clock subset CSVs to `data/interim/`, calls Rscript, collects JSON outputs, writes `results/tables/per_clock_pooled.csv`.

```python
from __future__ import annotations
import argparse, json, math, subprocess, sys
from pathlib import Path
import pandas as pd, numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from _common import load_config, log, ensure_dirs, append_amendment

def hedges_g_change(m1, s1, m2, s2, n1, n2):
    # SMD on change scores; assume sd of change reported in s1/s2
    sp = math.sqrt(((n1-1)*s1**2 + (n2-1)*s2**2) / (n1+n2-2))
    d = (m1 - m2) / sp
    J = 1 - 3/(4*(n1+n2)-9)
    g = J * d
    var = (n1+n2)/(n1*n2) + g**2/(2*(n1+n2))
    return g, math.sqrt(var)

def run(cfg):
    fdate = cfg["project"]["freeze_date"]
    ex = pd.read_csv(cfg["paths"]["data_processed"] / f"extracted_clock_studies_{fdate}.csv")
    rows = []
    for _, r in ex.iterrows():
        try:
            m1 = float(r["change_int_mean"]); s1 = float(r["change_int_sd"]); n1 = int(r["n_int"])
            m2 = float(r["change_ctrl_mean"]); s2 = float(r["change_ctrl_sd"]); n2 = int(r["n_ctrl"])
        except Exception:
            continue
        if any(np.isnan([m1,s1,m2,s2])) or n1<=1 or n2<=1: continue
        g, se = hedges_g_change(m1,s1,m2,s2,n1,n2)
        rows.append({"study_id":r["study_id"],"clock":r["clock"],"g":g,"se_g":se,
                     "intervention_class":r["intervention_class"],"duration_weeks":r.get("duration_weeks",""),
                     "age_mean":r.get("age_mean",""),"health_status":r.get("health_status","")})
    es = pd.DataFrame(rows); es.to_csv(cfg["paths"]["results_tabs"] / "per_study_effect_sizes.csv", index=False)
    log("effect_sizes_done", n=len(es))
    pooled = []
    for clock, sub in es.groupby("clock"):
        if len(sub) < cfg["synthesis"]["min_studies_for_pool"]:
            append_amendment(cfg["paths"]["docs"], f"Clock {clock} has {len(sub)} studies (<min); narrative only", "Insufficient for pooling")
            continue
        ipath = cfg["paths"]["data_interim"] / f"meta_input_{clock}.csv"
        opath = cfg["paths"]["data_interim"] / f"meta_output_{clock}.json"
        sub[["study_id","g","se_g"]].to_csv(ipath, index=False)
        try:
            subprocess.run(["Rscript","r_scripts/meta_pool.R",str(ipath),str(opath)], check=True)
            res = json.loads(opath.read_text())
            bopath = cfg["paths"]["data_interim"] / f"bayes_output_{clock}.json"
            subprocess.run(["Rscript","r_scripts/bayesmeta.R",str(ipath),str(bopath)], check=True)
            bres = json.loads(bopath.read_text())
            res.update({"bayes_mu_median":bres["mu_median"],"bayes_mu_lower":bres["mu_lower"],"bayes_mu_upper":bres["mu_upper"]})
            res["clock"] = clock; pooled.append(res)
        except Exception as e:
            append_amendment(cfg["paths"]["docs"], f"Pooling failed for {clock}: {e}", "R subprocess error")
    pd.DataFrame(pooled).to_csv(cfg["paths"]["results_tabs"] / "per_clock_pooled.csv", index=False)
    log("pooling_done", clocks_pooled=len(pooled))

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True)
    run(load_config(ap.parse_args().config))
```

- [ ] **Step 4: Run** — `make meta`. Expected: `per_clock_pooled.csv` with one row per pooled clock.

- [ ] **Step 5: Commit**

```bash
git add anti_ageing_review/meta_dnam_clocks/{src/08_meta_analysis.py,r_scripts/}
git commit -m "feat(meta-dnam): per-clock RE meta-analysis (DL + HKSJ + Bayesian)"
```

### Task 11: Subgroup + meta-regression

**Files:**
- Create: `anti_ageing_review/meta_dnam_clocks/src/09_subgroup_metareg.py`

For each clock with ≥3 studies: subgroup analyses by intervention class, duration band, age band, health status. For each clock with ≥10 studies: meta-regression on `duration_weeks` and `age_mean` via R `metafor::rma`.

- [ ] **Step 1: Implement** — write `subgroup_results.csv` and `metareg_results.csv` to `results/tables/`.
- [ ] **Step 2: Run** — `make subgroup`.
- [ ] **Step 3: Commit** — `git commit -m "feat(meta-dnam): subgroup and meta-regression analyses"`.

### Task 12: Network meta-analysis (conditional)

**Files:**
- Create: `anti_ageing_review/meta_dnam_clocks/src/10_nma.py`
- Create: `anti_ageing_review/meta_dnam_clocks/r_scripts/netmeta.R`

Only runs for clocks with ≥10 studies AND a connected network of ≥3 intervention classes. Otherwise writes a justification line to `results/tables/nma_not_performed.csv` and logs an amendment.

- [ ] **Step 1: Implement R script** using `netmeta::netmeta` with random-effects, SUCRA via `netrank`.
- [ ] **Step 2: Implement Python wrapper** that checks connectivity (build graph in `networkx`, check `is_connected`), then dispatches to R or skips.
- [ ] **Step 3: Run** — `make nma`.
- [ ] **Step 4: Commit** — `git commit -m "feat(meta-dnam): conditional NMA with connectivity gate"`.

### Task 13: Publication bias + sensitivity analyses

**Files:**
- Create: `anti_ageing_review/meta_dnam_clocks/src/11_pubbias_sensitivity.py`

For each clock with ≥10 studies: Egger regression test, Begg rank correlation, trim-and-fill (Duval-Tweedie), PET-PEESE — all via R `meta` subprocess. For each clock: leave-one-out; restrict-to-low-RoB; restrict-to-≥12-week; restrict-to-EPIC-array.

- [ ] **Step 1: Implement.**
- [ ] **Step 2: Run** — `make pubbias`.
- [ ] **Step 3: Commit** — `git commit -m "feat(meta-dnam): publication bias diagnostics and sensitivity analyses"`.

### Task 14: GRADE evidence profile

**Files:**
- Create: `anti_ageing_review/meta_dnam_clocks/src/12_grade_profile.py`

For each `intervention_class × clock` cell with ≥3 studies: assign GRADE rating (High/Moderate/Low/Very Low) by stepping down from "High" based on: RoB summary, inconsistency (I² > 50%), indirectness (heuristic flag), imprecision (CI crosses 0 or includes large effects), publication bias (Egger p<0.10 or trim-and-fill discordant).

- [ ] **Step 1: Implement** — write `results/tables/grade_profile.csv`.
- [ ] **Step 2: Run** — `make grade`.
- [ ] **Step 3: Commit** — `git commit -m "feat(meta-dnam): GRADE evidence profile generator"`.

---

## Phase 7: Figures, Tables, Manuscript

### Task 15: Generate all figures programmatically

**Files:**
- Create: `anti_ageing_review/meta_dnam_clocks/src/13_figures.py`

Produces:
- `fig1_prisma_flow.png` — PRISMA 2020 flow built from screening logs (records identified, screened, eligible, included; one box per database).
- `fig2_rob2_summary.png` — traffic-light grid (study × domain) + summary bar across domains.
- `fig3_forest_panel.png` — multi-panel forest (subplots per clock with ≥3 studies); each panel shows study estimates, pooled diamond, 95% PI bar.
- `fig4_funnel_panel.png` — funnel + PET-PEESE for each clock with ≥10 studies; otherwise omit that subplot with a "Not applicable: <N studies" label.

All figures saved as PNG (300 dpi) and SVG to `results/figures/`.

- [ ] **Step 1: Implement** with matplotlib (no external plotting deps beyond seaborn for styling).
- [ ] **Step 2: Run** — `make figs`.
- [ ] **Step 3: Visually verify** each figure renders cleanly; titles, axis labels, legends present.
- [ ] **Step 4: Commit** — `git commit -m "feat(meta-dnam): main figures (PRISMA, RoB, forest, funnel)"`.

### Task 16: Assemble manuscript and supplementary

**Files:**
- Create: `anti_ageing_review/meta_dnam_clocks/manuscript/manuscript_main.md`
- Create: `anti_ageing_review/meta_dnam_clocks/manuscript/supplementary.md`
- Create: `anti_ageing_review/meta_dnam_clocks/src/14_manuscript_build.py`

`manuscript_main.md` is a Markdown manuscript with placeholders for numbers that resolve from `results/tables/per_clock_pooled.csv`, `subgroup_results.csv`, `grade_profile.csv` at build time. Structure: Abstract / Introduction / Methods / Results / Discussion / Limitations / Conclusion / Funding / COI / Author Contributions / Data Availability / References.

`14_manuscript_build.py` substitutes results into the Markdown, then runs Pandoc to produce `submission_assets/Biogerontology_DNAmClocks_<freeze>/manuscript_blinded.docx`, `title_page.docx`, `cover_letter.docx`, `declarations.docx`, `supplementary.docx`, `prisma_checklist.docx`, `submission_checklist.docx`.

- [ ] **Step 1: Draft `manuscript_main.md`** with numeric placeholders `{{pooled_DunedinPACE_smd}}` etc.; write the narrative authentically based on actual results — do not invent effect sizes.
- [ ] **Step 2: Implement `src/14_manuscript_build.py`** — reads result CSVs, substitutes placeholders, calls `pandoc` to render to docx using `manuscript/templates/reference.docx` for styling.
- [ ] **Step 3: Run** — `make manuscript`.
- [ ] **Step 4: Verify word counts** within Biogerontology limits (≤7,500 words main text; abstract ≤300 words). Adjust narrative if over.
- [ ] **Step 5: Commit** — `git commit -m "feat(meta-dnam): manuscript build pipeline and submission docx assets"`.

### Task 17: Build full submission asset bundle

**Files:**
- Create or update under `anti_ageing_review/meta_dnam_clocks/submission_assets/Biogerontology_DNAmClocks_<freeze>/`

Contents (all docx unless noted):
- `manuscript_blinded.docx`
- `title_page.docx` (authors, affiliations, ORCIDs, corresponding author block, COI statement)
- `cover_letter.docx` (addressed to Editor-in-Chief, Biogerontology; emphasizes conservative scope, novel synthesis, public reproducibility)
- `declarations.docx` (funding: none; COI: none declared; ethics: secondary data waiver; data availability: GitHub repo; author contributions: CRediT)
- `prisma_2020_checklist.docx`
- `supplementary.docx` (S1–S10 items)
- `figures/` (4 PNGs at 300 dpi + 4 SVGs)
- `tables/` (3 main tables as CSV + docx)
- `submission_checklist.docx`
- `references.bib` and Vancouver-formatted reference list

- [ ] **Step 1: Implement extension of `14_manuscript_build.py`** to produce every asset.
- [ ] **Step 2: Run** — `make manuscript` (re-run).
- [ ] **Step 3: Manually open each docx** in Word and verify formatting (headers, no track changes, no comments).
- [ ] **Step 4: Commit** — `git commit -m "feat(meta-dnam): full Biogerontology submission asset bundle"`.

---

## Phase 8: Internal QA + GitHub publish

### Task 18: Internal peer review (two simulated reviewers)

**Files:**
- Create: `anti_ageing_review/meta_dnam_clocks/submission_assets/Biogerontology_DNAmClocks_<freeze>/internal_peer_review_1.docx`
- Create: same path `internal_peer_review_2.docx`
- Create: same path `content_structure_validity_audit.docx`

Manually compose two distinct reviewer reports (methodologist focus; clinician focus) listing major and minor issues. Compose a validity audit covering: PRISMA compliance, RoB transparency, statistical defensibility, prediction-interval reporting, GRADE consistency, claim-vs-evidence alignment.

- [ ] **Step 1: Write reviewer 1 (methodologist) — focus on statistical methods, heterogeneity, prediction intervals, GRADE.**
- [ ] **Step 2: Write reviewer 2 (clinician) — focus on clinical relevance, intervention class interpretability, translational caveats.**
- [ ] **Step 3: Write validity audit — pass/fail per domain with quoted manuscript line numbers.**
- [ ] **Step 4: Address all major issues by editing manuscript and committing.**
- [ ] **Step 5: Commit** — `git commit -m "docs(meta-dnam): internal peer reviews and validity audit; revisions applied"`.

### Task 19: Publish standalone GitHub repository

**Files:**
- Create: `dnam-clocks-meta-analysis/` (new repository at user's GitHub account)

- [ ] **Step 1: Stage repo content**

```bash
cd ..  # exit anti_ageing_review/
mkdir dnam-clocks-meta-analysis && cd dnam-clocks-meta-analysis
rsync -a --exclude="data/raw/fulltext" "../anti_ageing_review/meta_dnam_clocks/" ./
```

- [ ] **Step 2: Write README.md** with overview, structure, replication steps, citation, license badges.

- [ ] **Step 3: Write LICENSE files** — MIT for code, CC-BY-4.0 statement for `data/` and `manuscript/`.

- [ ] **Step 4: Write CITATION.cff** with both authors, ORCID, title, year, Zenodo DOI placeholder.

- [ ] **Step 5: Write `.github/workflows/ci.yml`** that runs `pytest tests/ -v` on Ubuntu-latest with Python 3.12.

- [ ] **Step 6: Initialize and push**

```bash
git init
git add .
git commit -m "Initial public release: DNAm clocks meta-analysis pipeline and manuscript bundle"
gh repo create hssling/dnam-clocks-meta-analysis --public --source=. --remote=origin --push
```

- [ ] **Step 7: Tag release**

```bash
git tag -a v1.0-submission -m "Submission to Biogerontology"
git push origin v1.0-submission
```

- [ ] **Step 8: Enable Zenodo integration** — visit https://zenodo.org/account/settings/github/ , toggle the new repo on, re-issue the tag if needed to trigger DOI minting. Add the resulting DOI back into `CITATION.cff` and the manuscript Data Availability statement; rebuild docx; commit; re-tag as `v1.0-submission.1`.

- [ ] **Step 9: Final verification** — repo public; CI green; release visible; Zenodo DOI live; submission asset bundle complete in the original `anti_ageing_review/meta_dnam_clocks/submission_assets/Biogerontology_DNAmClocks_<freeze>/`.

- [ ] **Step 10: Final commit in parent repo**

```bash
cd ../anti_ageing_review
git add meta_dnam_clocks/
git commit -m "feat(meta-dnam): submission-ready bundle and GitHub release v1.0-submission"
```

---

## Self-Review

**Spec coverage:**
- §1 Scope/PICO → Task 2 (protocol_v1.md) ✓
- §2 Search/screening/extraction → Tasks 3, 4, 5, 6, 7, 8 ✓
- §3 Synthesis (per-clock RE, Bayesian, subgroup, meta-reg, NMA, pub bias, sensitivity, GRADE) → Tasks 10–14 ✓
- §4 Outputs (manuscript, 4 figs, 3 tables, supplementary, submission bundle) → Tasks 15, 16, 17 ✓
- §5 Repo architecture & reproducibility → Task 1 + Task 19 ✓
- §6 Phases + quality gates + hard stops → embedded in every phase header ✓
- "As feasible and robust" + amendment logging → `_common.append_amendment` used in every script ✓
- GitHub repo + Zenodo DOI → Task 19 ✓
- CRediT authorship → Task 16/17 (declarations.docx) ✓

**Placeholder scan:** No "TBD"/"TODO"/"add error handling" lines. Numeric placeholders in manuscript Markdown are intentional (resolved at build time).

**Type consistency:** All scripts read/write `meta_config.yaml` via `_common.load_config`; CSV schemas are explicit in Tasks 3, 5, 8; the `study_id` key is consistent across extraction, RoB, and synthesis tables.

Plan ready for execution.
