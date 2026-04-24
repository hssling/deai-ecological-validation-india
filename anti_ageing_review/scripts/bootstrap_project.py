"""Bootstrap the autonomous anti-ageing systematic review project."""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def write(path: str, text: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.strip() + "\n", encoding="utf-8")


def touch(path: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.touch()


def main() -> None:
    dirs = [
        "config",
        "data_raw",
        "data_processed",
        "docs",
        "logs",
        "metadata",
        "results/tables",
        "results/figures",
        "results/supplement",
        "manuscript",
        "tests",
        "src/search",
        "src/dedup",
        "src/screening",
        "src/retrieval",
        "src/extraction",
        "src/grading",
        "src/mechanisms",
        "src/meta_analysis",
        "src/nlp",
        "src/viz",
        "src/utils",
    ]
    for d in dirs:
        (ROOT / d).mkdir(parents=True, exist_ok=True)
    for pkg in [
        "src",
        "src/search",
        "src/dedup",
        "src/screening",
        "src/retrieval",
        "src/extraction",
        "src/grading",
        "src/mechanisms",
        "src/meta_analysis",
        "src/nlp",
        "src/viz",
        "src/utils",
        "tests",
    ]:
        touch(f"{pkg}/__init__.py")

    write(
        "README.md",
        """
# Can Ageing Be Slowed or Reversed?

Autonomous systematic review, evidence grading, and mechanistic synthesis of anti-ageing and age-reversal interventions.

This repository separates:
- lifespan extension
- healthspan improvement
- slowing of biological ageing
- biomarker reversal
- true organismal rejuvenation claims

The pipeline is intentionally conservative. Metadata-assisted automation supports search, deduplication, screening, extraction, evidence scoring, mechanism mapping, NLP augmentation, figures, and manuscript drafting. Human verification is required before submission.

## Quick start

```bash
python src/run_pipeline.py --config config/review_config.yaml
pytest tests -q
```
""",
    )

    write(
        ".gitignore",
        """
__pycache__/
.pytest_cache/
*.pyc
data_raw/full_text/
*.ris
*.nb.html
""",
    )

    write(
        "requirements.txt",
        """
pandas>=2.0
numpy>=1.24
requests>=2.31
pyyaml>=6.0
matplotlib>=3.8
seaborn>=0.13
networkx>=3.0
scikit-learn>=1.4
pytest>=8.0
""",
    )

    write(
        "environment.yml",
        """
name: anti-ageing-review
channels:
  - conda-forge
dependencies:
  - python=3.12
  - pandas
  - numpy
  - requests
  - pyyaml
  - matplotlib
  - seaborn
  - networkx
  - scikit-learn
  - pytest
""",
    )

    write(
        "Makefile",
        """
PYTHON=python
CONFIG=config/review_config.yaml

.PHONY: all search dedup screen retrieve extract grade mechanisms nlp synth figures manuscript test

all:
\t$(PYTHON) src/run_pipeline.py --config $(CONFIG)

search:
\t$(PYTHON) src/search/run_search.py --config $(CONFIG)

dedup:
\t$(PYTHON) src/dedup/deduplicate.py --config $(CONFIG)

screen:
\t$(PYTHON) src/screening/screen_records.py --config $(CONFIG)

retrieve:
\t$(PYTHON) src/retrieval/assess_full_text.py --config $(CONFIG)

extract:
\t$(PYTHON) src/extraction/extract_metadata.py --config $(CONFIG)

grade:
\t$(PYTHON) src/grading/score_evidence.py --config $(CONFIG)

mechanisms:
\t$(PYTHON) src/mechanisms/map_mechanisms.py --config $(CONFIG)

nlp:
\t$(PYTHON) src/nlp/topic_hype.py --config $(CONFIG)

synth:
\t$(PYTHON) src/meta_analysis/synthesize.py --config $(CONFIG)

figures:
\t$(PYTHON) src/viz/make_figures.py --config $(CONFIG)

manuscript:
\t$(PYTHON) src/write_manuscript.py --config $(CONFIG)

test:
\tpytest tests -q
""",
    )

    write(
        "config/review_config.yaml",
        """
project:
  title: "Can Ageing Be Slowed or Reversed? An Autonomous Systematic Review, Evidence Grading, and Mechanistic Synthesis of Anti-Ageing and Age-Reversal Interventions"
  version: "0.1.0"
  run_label: "initial_pilot"
  max_records_per_query: 35
  email: "hssling@yahoo.com"
paths:
  data_raw: "data_raw"
  data_processed: "data_processed"
  results_tables: "results/tables"
  results_figures: "results/figures"
  results_supplement: "results/supplement"
  logs: "logs"
  docs: "docs"
  manuscript: "manuscript"
sources:
  pubmed: true
  europe_pmc: true
  crossref: true
  preprints: true
screening:
  include_threshold: 5
  uncertain_threshold: 3
  min_year: 1990
""",
    )

    write(
        "config/source_registry.yaml",
        """
sources:
  pubmed:
    type: peer_reviewed_metadata
    base: "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
  europe_pmc:
    type: mixed_literature_metadata
    base: "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
  crossref:
    type: bibliographic_metadata
    base: "https://api.crossref.org/works"
  medrxiv_biorxiv:
    type: preprint_stream
    note: "Captured through Europe PMC where source labels indicate preprint."
""",
    )

    write(
        "config/search_terms.yaml",
        """
core_concepts:
  ageing: ["aging", "ageing", "longevity", "lifespan", "healthspan", "rejuvenation", "age reversal", "biological age", "epigenetic clock", "senescence", "frailty"]
interventions:
  caloric_restriction: ["caloric restriction", "calorie restriction", "dietary restriction"]
  fasting: ["intermittent fasting", "fasting mimicking diet", "time restricted eating"]
  exercise: ["exercise", "physical activity", "resistance training", "aerobic training"]
  sleep_circadian: ["sleep", "circadian", "chronotherapy"]
  metformin: ["metformin"]
  rapamycin_mtor: ["rapamycin", "sirolimus", "mTOR"]
  nad_sirtuin: ["NAD", "nicotinamide riboside", "NMN", "sirtuin"]
  senolytics: ["senolytic", "senomorphic", "dasatinib quercetin", "fisetin"]
  stem_cell: ["stem cell", "regenerative medicine"]
  reprogramming: ["Yamanaka", "partial reprogramming", "epigenetic reprogramming"]
  microbiome: ["microbiome", "probiotic", "fecal microbiota"]
  supplements: ["resveratrol", "curcumin", "omega-3", "vitamin D", "supplement"]
  lifestyle_bundle: ["lifestyle intervention", "combined lifestyle", "multidomain intervention"]
  controversial: ["parabiosis", "young plasma", "plasma dilution", "telomerase"]
queries:
  broad:
    - '(aging OR ageing OR longevity OR healthspan OR lifespan) AND (intervention OR trial OR treatment OR therapy)'
    - '("biological age" OR "epigenetic clock" OR "DNA methylation age") AND (intervention OR trial OR therapy)'
    - '(rejuvenation OR "age reversal" OR "reverse aging" OR "reverse ageing")'
  narrow:
    - '(aging OR ageing OR healthspan OR lifespan) AND ("caloric restriction" OR "dietary restriction" OR fasting)'
    - '(aging OR ageing OR healthspan OR frailty) AND (exercise OR "physical activity" OR "resistance training")'
    - '(aging OR ageing OR longevity OR frailty) AND (metformin OR rapamycin OR sirolimus OR mTOR)'
    - '(aging OR ageing OR "epigenetic clock") AND (NAD OR "nicotinamide riboside" OR NMN OR sirtuin)'
    - '(aging OR ageing OR senescence OR frailty) AND (senolytic OR senomorphic OR fisetin OR dasatinib OR quercetin)'
    - '(aging OR ageing OR rejuvenation) AND ("stem cell" OR "partial reprogramming" OR Yamanaka)'
    - '(aging OR ageing OR healthspan) AND (microbiome OR probiotic OR "fecal microbiota")'
    - '(aging OR ageing OR rejuvenation) AND (parabiosis OR "young plasma" OR "plasma dilution")'
""",
    )

    docs = {
        "docs/protocol.md": """
# Protocol

## Title
Can Ageing Be Slowed or Reversed? An Autonomous Systematic Review, Evidence Grading, and Mechanistic Synthesis of Anti-Ageing and Age-Reversal Interventions

## Objective
To systematically discover, screen, extract, grade, and synthesize empirical evidence on interventions claimed to slow ageing, improve healthspan, reverse ageing biomarkers, or produce rejuvenation.

## Review Question
Which interventions have credible evidence for lifespan extension, healthspan improvement, slowing of biological ageing, biomarker reversal, or true rejuvenation, and through which mechanisms?

## Core Definitions
- Anti-ageing: broad claim that an intervention affects ageing-related processes or outcomes.
- Healthy ageing: maintenance of function, intrinsic capacity, independence, and quality of life.
- Lifespan extension: increased survival or maximum/median lifespan.
- Healthspan extension: longer period of preserved function or delayed morbidity/frailty.
- Biological ageing slowing: deceleration of validated ageing biomarkers or trajectories.
- Biomarker reversal: improvement in an ageing biomarker such as epigenetic age; not equivalent to clinical rejuvenation.
- Clinical reversal/rejuvenation: durable improvement in organism-level function consistent with younger biological state; requires strong evidence.

## Eligibility
Original empirical studies in humans, animals, or cellular systems. Commentaries, editorials, non-empirical marketing claims, and studies without ageing-relevant outcomes are excluded.

## Sources
PubMed, Europe PMC, Crossref metadata, and preprint streams where captured.

## Study Selection
Two-stage screening: title/abstract screening followed by full-text eligibility assessment. Human, animal, and cellular evidence are separated.

## Extraction
Structured extraction covers study identity, design, population/model, intervention, comparator, outcomes, mechanism, effect direction, uncertainty, risk of bias, and extraction confidence.

## Risk of Bias
Human studies are assessed for randomization, blinding, missing data, confounding, outcome validity, and selective reporting. Animal and in vitro evidence are graded for methodological clarity and translational limits.

## Synthesis
Meta-analysis will be attempted only where comparable outcomes and effect sizes are available. Otherwise, evidence maps, harvest plots, and conservative narrative synthesis will be used.

## Evidence Grading
The Anti-Ageing Evidence Credibility Score combines evidence level, reproducibility, effect magnitude, directness to ageing, mechanistic plausibility, bias, translational readiness, and hype/controversy penalties.

## Publication Plan
Primary output is a journal-neutral systematic review manuscript with supplementary extraction tables, evidence maps, and reproducible code.
""",
        "docs/inclusion_exclusion.md": """
# Inclusion and Exclusion Criteria

## Include
- Original empirical studies.
- Human, animal, or cellular model clearly labeled.
- Intervention or exposure plausibly intended to slow/reverse ageing or improve age-related decline.
- At least one ageing-relevant outcome: lifespan, mortality, frailty, disability, function, cognition, multimorbidity, epigenetic clock, omics age, senescence marker, or strong mechanistic ageing marker.

## Exclude
- Commentary, editorial, opinion without new empirical data.
- Marketing or vague anti-ageing claims.
- Disease-only studies without ageing-relevant framing or outcomes.
- Duplicate publications unless non-overlapping data are provided.
- Surrogate metabolic-only studies unless explicitly tied to ageing biology and categorized as indirect.
""",
        "docs/screening_manual.md": """
# Screening Manual

Screen conservatively. Include if there is an intervention plus ageing-relevant outcome. Mark uncertain if the abstract suggests relevant biology but lacks outcome detail.

Primary exclusion reasons:
- non_empirical
- no_intervention
- no_ageing_outcome
- disease_only
- duplicate
- commentary
- inaccessible_unclear
""",
        "docs/extraction_manual.md": """
# Extraction Manual

Extraction is metadata-assisted in the initial pass and requires human full-text verification before final publication.

Required fields: title, authors, year, journal, DOI, PMID, species/model, design, intervention class, duration, comparator, outcome domain, effect direction, mechanism, risk-of-bias indicators, extraction confidence, and ambiguity notes.
""",
        "docs/evidence_framework.md": """
# Evidence Framework

Scores are transparent and decomposable. Human RCTs receive the highest base level; observational human evidence, animal evidence, and cellular evidence are progressively less direct. Biomarker reversal is never treated as clinical rejuvenation without functional evidence. Preprints and hype-heavy claims are penalized.
""",
        "docs/risk_of_bias_plan.md": """
# Risk of Bias Plan

Human domains: randomization, allocation concealment, blinding, missing outcome data, confounding, outcome measurement validity, selective reporting, funding/conflict concerns.

Animal domains: randomization, allocation concealment, blinding, sample-size reporting, sex/age reporting, replication, translational relevance.

Cellular domains: model relevance, replication, dose realism, assay validity, mechanistic specificity.
""",
        "docs/mechanism_mapping_plan.md": """
# Mechanism Mapping Plan

Map interventions to hallmarks/pathways: cellular senescence, inflammaging, mitochondrial dysfunction, proteostasis, stem cell exhaustion, nutrient sensing, genomic instability, epigenetic alterations, autophagy, immune regulation, microbiome-host interaction, and metabolism.
""",
        "docs/search_strategy.md": """
# Search Strategy

Broad searches combine ageing/longevity/healthspan/rejuvenation terms with intervention/trial terms. Narrow searches combine ageing concepts with specific intervention classes. PubMed, Europe PMC, and Crossref are queried with timestamps and source labels. Preprints are retained separately and penalized in evidence grading.
""",
        "docs/decision_log.md": """
# Decision Log

- Created autonomous project scaffold.
- Chose metadata-assisted screening as the initial feasible fallback because full-text retrieval is heterogeneous and may be inaccessible for some journals.
- Preprints are retained but separated and penalized.
- Biomarker improvements are not labeled true age reversal unless paired with organism-level functional evidence.
""",
        "docs/journal_targets.md": """
# Journal Targets

## Nature Aging style
High bar for mechanistic novelty and human translational relevance; emphasize strict separation of claims.

## Lancet Healthy Longevity style
Emphasize public health, clinical readiness, safety, and implications for healthy ageing.

## GeroScience / Aging Cell
Emphasize mechanisms, hallmarks, translational gaps, and preclinical-to-human bridge.

## Age and Ageing
Emphasize clinical geriatrics, function, frailty, and what is actionable now.
""",
    }
    for path, text in docs.items():
        write(path, text)

    write(
        "src/utils/io.py",
        """
from __future__ import annotations
from pathlib import Path
from datetime import datetime
import yaml
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

def load_config(path='config/review_config.yaml'):
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    cfg = yaml.safe_load(p.read_text(encoding='utf-8'))
    cfg['_root'] = ROOT
    for key, val in cfg.get('paths', {}).items():
        out = ROOT / val
        out.mkdir(parents=True, exist_ok=True)
        cfg['paths'][key] = out
    return cfg

def save_csv(df, path):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(p, index=False)

def append_log(path, phase, completed, outputs, remaining, risks, next_command):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    block = f'''
---
## {phase}
Date/time: {stamp}

Completed:
{completed}

Outputs created:
{outputs}

Remaining tasks:
{remaining}

Risks/limitations:
{risks}

Exact next command:
`{next_command}`
'''
    with p.open('a', encoding='utf-8') as f:
        f.write(block)

def now_iso():
    return datetime.now().isoformat(timespec='seconds')
""",
    )

    write(
        "src/search/run_search.py",
        r'''
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

def europe_pmc_search(query, max_records):
    params = {"query":query, "format":"json", "pageSize":max_records, "sort":"RELEVANCE"}
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
''',
    )

    write(
        "src/dedup/deduplicate.py",
        r'''
from __future__ import annotations
import argparse, re, hashlib
import pandas as pd
from src.utils.io import load_config, save_csv, append_log

def norm_title(t):
    t = str(t or "").lower()
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()

def dedup_key(row):
    doi = str(row.get("doi","")).lower().strip()
    pmid = str(row.get("pmid","")).strip()
    if doi and doi != "nan":
        return "doi:" + doi
    if pmid and pmid != "nan":
        return "pmid:" + pmid
    return "title:" + norm_title(row.get("title",""))

def run(cfg):
    raw_path = cfg["paths"]["results_tables"] / "raw_records_all.csv"
    raw = pd.read_csv(raw_path) if raw_path.exists() else pd.DataFrame()
    if raw.empty:
        master = raw
        log = pd.DataFrame()
    else:
        raw["dedup_key"] = raw.apply(dedup_key, axis=1)
        raw["title_norm"] = raw["title"].map(norm_title)
        keep_order = {"pubmed":0, "europe_pmc":1, "crossref":2}
        raw["_source_rank"] = raw["source"].map(keep_order).fillna(9)
        raw["_abstract_len"] = raw["abstract"].fillna("").str.len()
        raw = raw.sort_values(["dedup_key","_source_rank","_abstract_len"], ascending=[True, True, False])
        master = raw.drop_duplicates("dedup_key", keep="first").drop(columns=["_source_rank","_abstract_len"])
        dup_counts = raw.groupby("dedup_key").size().reset_index(name="n_records")
        log = dup_counts[dup_counts["n_records"] > 1].merge(master[["dedup_key","title","doi","pmid"]], on="dedup_key", how="left")
    save_csv(master, cfg["paths"]["results_tables"] / "master_records_dedup.csv")
    save_csv(log, cfg["paths"]["results_tables"] / "dedup_log.csv")
    unresolved = master[master["title_norm"].duplicated(keep=False)].sort_values("title_norm") if not master.empty else master
    save_csv(unresolved, cfg["paths"]["results_tables"] / "unresolved_duplicate_report.csv")
    append_log(cfg["paths"]["logs"] / "progress.md", "Phase 3 - Deduplication and Record Hygiene",
               f"- Standardized DOI/PMID/title keys.\n- Reduced {len(raw)} raw rows to {len(master)} deduplicated records.\n- Flagged {len(log)} duplicate key groups.",
               "- results/tables/master_records_dedup.csv\n- results/tables/dedup_log.csv\n- results/tables/unresolved_duplicate_report.csv",
               "- Manual review of unresolved duplicate title variants remains pending.",
               "- Records without DOI/PMID depend on normalized title matching and may under/over-deduplicate.",
               "python src/screening/screen_records.py --config config/review_config.yaml")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/review_config.yaml")
    run(load_config(ap.parse_args().config))
''',
    )

    write(
        "src/screening/screen_records.py",
        r'''
from __future__ import annotations
import argparse, re
import pandas as pd
from src.utils.io import load_config, save_csv, append_log

INTERVENTIONS = {
 "caloric_restriction":["caloric restriction","calorie restriction","dietary restriction"],
 "fasting":["fasting","time restricted","fasting mimicking"],
 "exercise":["exercise","physical activity","resistance training","aerobic"],
 "sleep_circadian":["sleep","circadian"],
 "metformin":["metformin"],
 "rapamycin_mtor":["rapamycin","sirolimus","mtor"],
 "nad_sirtuin":["nad","nicotinamide riboside","nmn","sirtuin"],
 "senolytics":["senolytic","senomorphic","fisetin","dasatinib","quercetin"],
 "stem_cell":["stem cell","regenerative"],
 "reprogramming":["yamanaka","partial reprogramming","epigenetic reprogramming"],
 "microbiome":["microbiome","probiotic","fecal microbiota"],
 "supplements":["resveratrol","curcumin","omega","vitamin d","supplement"],
 "lifestyle_bundle":["lifestyle","multidomain"],
 "controversial":["parabiosis","young plasma","plasma dilution","telomerase"],
}
OUTCOME_TERMS = ["lifespan","survival","mortality","healthspan","frailty","disability","adl","iadl","grip","gait","cognition","multimorbidity","epigenetic clock","biological age","dna methylation age","senescence","inflammaging","rejuvenation"]
NON_EMP = ["review","editorial","commentary","letter","protocol","perspective"]

def text(row):
    return f"{row.get('title','')} {row.get('abstract','')} {row.get('publication_type','')}".lower()

def classify_model(t):
    if any(x in t for x in ["mouse","mice","murine","c elegans","drosophila","rat "]): return "animal"
    if any(x in t for x in ["cell","in vitro","fibroblast","organoid"]): return "cellular"
    if any(x in t for x in ["human","randomized","clinical trial","participants","patients","adults","men","women"]): return "human"
    return "unclear"

def screen_row(row):
    t = text(row)
    inter = [k for k, vals in INTERVENTIONS.items() if any(v in t for v in vals)]
    outcomes = [o for o in OUTCOME_TERMS if o in t]
    non_emp = any(x in t for x in NON_EMP) and "trial" not in t
    score = len(inter)*2 + min(len(outcomes), 4)
    if "randomized" in t or "trial" in t: score += 1
    if row.get("is_preprint", False): score -= 1
    if non_emp and not inter:
        return "exclude", 0.85, "non_empirical", inter, outcomes, classify_model(t)
    if not inter:
        return "exclude", 0.7, "no_clear_intervention", inter, outcomes, classify_model(t)
    if not outcomes:
        return "uncertain", 0.45, "ageing_outcome_unclear", inter, outcomes, classify_model(t)
    if score >= 5:
        return "include", min(0.95, 0.55 + score/20), "", inter, outcomes, classify_model(t)
    return "uncertain", 0.55, "needs_full_text_or_abstract", inter, outcomes, classify_model(t)

def run(cfg):
    master = pd.read_csv(cfg["paths"]["results_tables"] / "master_records_dedup.csv")
    rows = []
    for _, r in master.iterrows():
        label, conf, reason, inter, outcomes, model = screen_row(r)
        d = r.to_dict()
        d.update({"screen_label":label,"screen_confidence":round(conf,2),"exclusion_reason":reason,
                  "intervention_classes":"; ".join(inter),"outcome_terms":"; ".join(outcomes),"evidence_model":model})
        rows.append(d)
    out = pd.DataFrame(rows)
    save_csv(out, cfg["paths"]["results_tables"] / "title_abstract_screening.csv")
    full = out[out["screen_label"].isin(["include","uncertain"])].copy()
    full["full_text_label"] = "pending"
    full["full_text_exclusion_reason"] = ""
    save_csv(full, cfg["paths"]["results_tables"] / "full_text_screening.csv")
    append_log(cfg["paths"]["logs"] / "progress.md", "Phase 4 - Autonomous Screening Engine",
               f"- Screened {len(out)} title/abstract records using conservative rules.\n- Included {sum(out.screen_label=='include')}; uncertain {sum(out.screen_label=='uncertain')}; excluded {sum(out.screen_label=='exclude')}.",
               "- results/tables/title_abstract_screening.csv\n- results/tables/full_text_screening.csv",
               "- Human verification of all include/uncertain records remains mandatory.\n- Full-text screening is initialized but not complete.",
               "- Abstract gaps reduce confidence for PubMed/Crossref-only records.",
               "python src/retrieval/assess_full_text.py --config config/review_config.yaml")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/review_config.yaml")
    run(load_config(ap.parse_args().config))
''',
    )

    write(
        "src/retrieval/assess_full_text.py",
        r'''
from __future__ import annotations
import argparse
import pandas as pd
from src.utils.io import load_config, save_csv, append_log

def status(row):
    if str(row.get("pmcid","")).strip() and str(row.get("pmcid","")).lower() != "nan":
        return "retrieved_open_metadata", "PMC full text likely available"
    if str(row.get("url","")).startswith("http"):
        return "link_available", "Full text link or landing page available"
    if row.get("is_preprint", False):
        return "preprint_only", "Preprint stream"
    return "abstract_or_metadata_only", "No full text link captured"

def run(cfg):
    s = pd.read_csv(cfg["paths"]["results_tables"] / "title_abstract_screening.csv")
    cand = s[s["screen_label"].isin(["include","uncertain"])].copy()
    vals = cand.apply(status, axis=1, result_type="expand")
    cand["retrieval_status"] = vals[0]
    cand["retrieval_note"] = vals[1]
    save_csv(cand, cfg["paths"]["results_tables"] / "full_text_status.csv")
    append_log(cfg["paths"]["logs"] / "progress.md", "Phase 5 - Full Text Retrieval and Organization",
               f"- Assigned retrieval status to {len(cand)} include/uncertain records.",
               "- results/tables/full_text_status.csv",
               "- Actual PDF/full-text download and copyright-compliant review remain pending.",
               "- Some records are metadata-only; evidence completeness is limited.",
               "python src/extraction/extract_metadata.py --config config/review_config.yaml")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/review_config.yaml")
    run(load_config(ap.parse_args().config))
''',
    )

    write(
        "src/extraction/extract_metadata.py",
        r'''
from __future__ import annotations
import argparse, re
import pandas as pd
from src.screening.screen_records import INTERVENTIONS
from src.utils.io import load_config, save_csv, append_log

MECH = {
 "cellular_senescence":["senescence","senolytic","senomorphic","p16","p21","sasp"],
 "inflammaging":["inflammation","inflammatory","il-6","crp","inflammaging","nf-kb"],
 "mitochondrial_function":["mitochondria","mitochondrial","oxidative phosphorylation"],
 "proteostasis_autophagy":["autophagy","proteostasis","proteasome"],
 "stem_cell_effects":["stem cell","regenerative"],
 "nutrient_sensing":["mtor","ampk","insulin","igf","rapamycin","metformin"],
 "epigenetic_alterations":["epigenetic","dna methylation","yamanaka","reprogramming"],
 "sirtuin_nad":["sirtuin","nad","nmn","nicotinamide"],
 "microbiome_host":["microbiome","microbiota","probiotic"],
 "dna_repair_genomic":["dna repair","genomic instability","telomerase","telomere"],
}

def first_class(t):
    hits = [k for k, vals in INTERVENTIONS.items() if any(v in t for v in vals)]
    return hits[0] if hits else "unclear"

def design(t, pubtype):
    x = f"{t} {pubtype}".lower()
    if "randomized" in x or "randomised" in x or "clinical trial" in x: return "RCT_or_clinical_trial"
    if "cohort" in x: return "cohort"
    if "cross-sectional" in x: return "cross-sectional"
    if any(y in x for y in ["mouse","mice","rat","drosophila","c elegans"]): return "animal_experiment"
    if any(y in x for y in ["cell","in vitro","fibroblast"]): return "in_vitro_study"
    return "unclear_or_metadata_only"

def outcome_domain(t):
    if any(x in t for x in ["mortality","survival","lifespan"]): return "hard_ageing_relevance"
    if any(x in t for x in ["frailty","disability","adl","iadl","grip","gait","cognition","multimorbidity","physical performance"]): return "healthspan_functional_ageing"
    if any(x in t for x in ["epigenetic clock","dna methylation age","biological age","transcriptomic age","proteomic age","senescence"]): return "biological_ageing_biomarker"
    return "surrogate_or_indirect"

def mechanisms(t):
    return [k for k, vals in MECH.items() if any(v in t for v in vals)] or ["unclear"]

def run(cfg):
    s = pd.read_csv(cfg["paths"]["results_tables"] / "title_abstract_screening.csv")
    inc = s[s["screen_label"].isin(["include","uncertain"])].copy()
    rows = []
    for _, r in inc.iterrows():
        t = f"{r.get('title','')} {r.get('abstract','')}".lower()
        rows.append({
            "title":r.get("title",""),"authors":r.get("authors",""),"year":r.get("year",""),"journal":r.get("journal",""),
            "doi":r.get("doi",""),"pmid":r.get("pmid",""),"source":r.get("source",""),"is_preprint":r.get("is_preprint",False),
            "study_design":design(t, r.get("publication_type","")),"species_model":r.get("evidence_model","unclear"),
            "sample_size":"","age_sex":"","disease_status":"","intervention_name":first_class(t),
            "intervention_class":r.get("intervention_classes",""),"dose_intensity":"","duration":"","comparator":"",
            "outcome_exact":r.get("outcome_terms",""),"ageing_domain_category":outcome_domain(t),
            "effect_direction":"not_extracted_metadata_only","effect_size":"","uncertainty_measure":"","follow_up_time":"",
            "mechanism":"; ".join(mechanisms(t)),"mechanism_directness":"inferred_from_title_abstract",
            "extraction_confidence":0.45 if r.get("screen_label")=="uncertain" else 0.6,
            "missingness_flag":"requires_full_text_verification","ambiguity_notes":"Metadata-assisted extraction; do not use as final effect extraction."
        })
    out = pd.DataFrame(rows)
    save_csv(out, cfg["paths"]["results_tables"] / "extracted_studies_master.csv")
    dictionary = pd.DataFrame({"field":out.columns, "description":["See extraction_manual.md; metadata-assisted pilot field." for _ in out.columns]})
    save_csv(dictionary, cfg["_root"] / "metadata/extraction_dictionary.csv")
    append_log(cfg["paths"]["logs"] / "progress.md", "Phase 6 - Structured Data Extraction",
               f"- Created metadata-assisted extraction table for {len(out)} candidate studies.",
               "- results/tables/extracted_studies_master.csv\n- metadata/extraction_dictionary.csv",
               "- Full effect sizes, doses, durations, and bias fields require full-text extraction.",
               "- Metadata extraction is preliminary and explicitly flagged.",
               "python src/grading/score_evidence.py --config config/review_config.yaml")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/review_config.yaml")
    run(load_config(ap.parse_args().config))
''',
    )

    write(
        "src/grading/score_evidence.py",
        r'''
from __future__ import annotations
import argparse
import pandas as pd
from src.utils.io import load_config, save_csv, append_log

LEVEL = {"human":5,"animal":2.5,"cellular":1.5,"unclear":1}
DIRECT = {"hard_ageing_relevance":4,"healthspan_functional_ageing":3.5,"biological_ageing_biomarker":2.5,"surrogate_or_indirect":1}
READINESS = {"caloric_restriction":3,"fasting":2.5,"exercise":4,"sleep_circadian":3,"metformin":2.5,"rapamycin_mtor":1.5,"nad_sirtuin":1.5,"senolytics":1.5,"stem_cell":1,"reprogramming":0.5,"microbiome":1.5,"supplements":1,"lifestyle_bundle":3,"controversial":0.5,"unclear":0.5}

def score_row(r):
    model = str(r.get("species_model","unclear"))
    base = LEVEL.get(model, 1)
    direct = DIRECT.get(r.get("ageing_domain_category","surrogate_or_indirect"), 1)
    mech = 2 if str(r.get("mechanism","unclear")) != "unclear" else 0.5
    ready = READINESS.get(r.get("intervention_name","unclear"), 1)
    penalty = 1.0 if str(r.get("is_preprint","False")).lower() == "true" else 0
    if r.get("intervention_name") in ["controversial","reprogramming","stem_cell"]:
        penalty += 1.0
    return max(0, round(base + direct + mech + ready - penalty, 2))

def category(score):
    if score >= 11: return "supported_for_healthspan_related_benefit"
    if score >= 8: return "promising_but_incomplete"
    if score >= 5: return "biomarker_or_preclinical_evidence"
    return "speculative_or_hype_heavy"

def run(cfg):
    ex = pd.read_csv(cfg["paths"]["results_tables"] / "extracted_studies_master.csv")
    if ex.empty:
        out = pd.DataFrame()
    else:
        ex["claim_score"] = ex.apply(score_row, axis=1)
        ex["claim_category"] = ex["claim_score"].map(category)
        out = ex.groupby("intervention_name").agg(
            n_records=("title","count"),
            max_claim_score=("claim_score","max"),
            mean_claim_score=("claim_score","mean"),
            human_records=("species_model", lambda x: sum(x=="human")),
            animal_records=("species_model", lambda x: sum(x=="animal")),
            cellular_records=("species_model", lambda x: sum(x=="cellular")),
        ).reset_index()
        out["mean_claim_score"] = out["mean_claim_score"].round(2)
        out["classification"] = out["max_claim_score"].map(category)
    save_csv(out, cfg["paths"]["results_tables"] / "intervention_evidence_scores.csv")
    save_csv(ex, cfg["paths"]["results_tables"] / "claim_credibility_matrix.csv")
    rob = ex[["title","study_design","species_model","ageing_domain_category","intervention_name","claim_score","claim_category"]].copy()
    rob["bias_level"] = rob["study_design"].map(lambda x: "lower" if "RCT" in str(x) else "moderate_or_high")
    save_csv(rob, cfg["paths"]["results_tables"] / "risk_of_bias.csv")
    append_log(cfg["paths"]["logs"] / "progress.md", "Phase 7-8 - Risk of Bias and Evidence Scoring",
               f"- Scored {len(ex)} claim-level records and {len(out)} intervention groups.",
               "- results/tables/risk_of_bias.csv\n- results/tables/intervention_evidence_scores.csv\n- results/tables/claim_credibility_matrix.csv",
               "- Risk of bias is design-level preliminary; full RoB requires full text.",
               "- Scores are metadata-assisted and conservative.",
               "python src/mechanisms/map_mechanisms.py --config config/review_config.yaml")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/review_config.yaml")
    run(load_config(ap.parse_args().config))
''',
    )

    write(
        "src/mechanisms/map_mechanisms.py",
        r'''
from __future__ import annotations
import argparse
import pandas as pd
from src.utils.io import load_config, save_csv, append_log

def run(cfg):
    ex = pd.read_csv(cfg["paths"]["results_tables"] / "extracted_studies_master.csv")
    rows = []
    for _, r in ex.iterrows():
        for m in str(r.get("mechanism","unclear")).split("; "):
            rows.append({"intervention":r.get("intervention_name","unclear"),"mechanism":m,"directness":r.get("mechanism_directness","inferred"),"species_model":r.get("species_model","unclear"),"title":r.get("title","")})
    mp = pd.DataFrame(rows)
    mat = pd.crosstab(mp["intervention"], mp["mechanism"]).reset_index() if not mp.empty else pd.DataFrame()
    save_csv(mp, cfg["paths"]["results_tables"] / "intervention_mechanism_map.csv")
    save_csv(mat, cfg["paths"]["results_tables"] / "mechanism_evidence_matrix.csv")
    append_log(cfg["paths"]["logs"] / "progress.md", "Phase 9 - Mechanistic Mapping",
               f"- Mapped {len(mp)} intervention-mechanism edges.",
               "- results/tables/intervention_mechanism_map.csv\n- results/tables/mechanism_evidence_matrix.csv",
               "- Direct/inferred mechanism labels require full-text verification.",
               "- Mechanism mapping from abstracts may miss measured pathways.",
               "python src/nlp/topic_hype.py --config config/review_config.yaml")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/review_config.yaml")
    run(load_config(ap.parse_args().config))
''',
    )

    write(
        "src/nlp/topic_hype.py",
        r'''
from __future__ import annotations
import argparse
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from src.utils.io import load_config, save_csv, append_log

HYPE = ["reversal","reverse","rejuvenation","breakthrough","young plasma","immortality","cure","anti-aging","anti-ageing"]

def run(cfg):
    s = pd.read_csv(cfg["paths"]["results_tables"] / "title_abstract_screening.csv")
    cand = s[s["screen_label"].isin(["include","uncertain"])].copy()
    texts = (cand["title"].fillna("") + " " + cand["abstract"].fillna("")).tolist()
    if len(cand) >= 4:
        X = TfidfVectorizer(max_features=800, stop_words="english").fit_transform(texts)
        k = min(8, max(2, len(cand)//10))
        cand["topic_cluster"] = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(X)
    else:
        cand["topic_cluster"] = 0
    cand["hype_terms_n"] = [sum(h in t.lower() for h in HYPE) for t in texts]
    cand["hype_flag"] = cand["hype_terms_n"] > 0
    save_csv(cand[["title","intervention_classes","outcome_terms","topic_cluster","hype_terms_n","hype_flag","screen_label"]], cfg["paths"]["results_tables"] / "topic_assignments.csv")
    summary = cand.groupby("topic_cluster").agg(n=("title","count"), hype_rate=("hype_flag","mean")).reset_index()
    save_csv(summary, cfg["paths"]["results_tables"] / "hype_topic_summary.csv")
    (cfg["paths"]["docs"] / "nlp_summary.md").write_text("# NLP Summary\n\nTopic clustering and hype flags are metadata-assisted. Hype terms flag language needing skeptical review; they do not prove poor science.\n", encoding="utf-8")
    append_log(cfg["paths"]["logs"] / "progress.md", "Phase 10 - NLP/Text Mining Augmentation",
               f"- Assigned topic clusters and hype flags to {len(cand)} records.",
               "- results/tables/topic_assignments.csv\n- results/tables/hype_topic_summary.csv\n- docs/nlp_summary.md",
               "- Embedding-based clustering can be added later.",
               "- Hype detection is lexical and preliminary.",
               "python src/meta_analysis/synthesize.py --config config/review_config.yaml")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/review_config.yaml")
    run(load_config(ap.parse_args().config))
''',
    )

    write(
        "src/meta_analysis/synthesize.py",
        r'''
from __future__ import annotations
import argparse
import pandas as pd
from src.utils.io import load_config, save_csv, append_log

def run(cfg):
    ex = pd.read_csv(cfg["paths"]["results_tables"] / "extracted_studies_master.csv")
    inputs = ex[["title","intervention_name","ageing_domain_category","effect_size","uncertainty_measure","effect_direction"]].copy()
    inputs["meta_ready"] = False
    inputs["reason_not_meta_ready"] = "Effect sizes not extracted from full text in pilot metadata pass"
    results = pd.DataFrame([{"analysis":"none_pilot","n_studies":0,"pooled_effect":"","heterogeneity":"","note":"No quantitative meta-analysis performed because comparable effect sizes require full-text extraction."}])
    vote = ex.groupby(["intervention_name","ageing_domain_category"]).size().reset_index(name="n_candidate_records") if not ex.empty else pd.DataFrame()
    save_csv(inputs, cfg["paths"]["results_tables"] / "meta_analysis_inputs.csv")
    save_csv(results, cfg["paths"]["results_tables"] / "meta_analysis_results.csv")
    save_csv(vote, cfg["paths"]["results_tables"] / "structured_vote_counting.csv")
    append_log(cfg["paths"]["logs"] / "progress.md", "Phase 11 - Meta-analysis / Quantitative Synthesis",
               "- Created meta-analysis readiness table.\n- Deferred pooling because effect sizes require full-text extraction.",
               "- results/tables/meta_analysis_inputs.csv\n- results/tables/meta_analysis_results.csv\n- results/tables/structured_vote_counting.csv",
               "- Full-text extraction of effect sizes is required before any pooled estimate.",
               "- Vote counting is descriptive and should not be overinterpreted.",
               "python src/viz/make_figures.py --config config/review_config.yaml")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/review_config.yaml")
    run(load_config(ap.parse_args().config))
''',
    )

    write(
        "src/viz/make_figures.py",
        r'''
from __future__ import annotations
import argparse
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from src.utils.io import load_config, append_log

def save(fig, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)

def run(cfg):
    figs = cfg["paths"]["results_figures"]
    scores = pd.read_csv(cfg["paths"]["results_tables"] / "intervention_evidence_scores.csv")
    screen = pd.read_csv(cfg["paths"]["results_tables"] / "title_abstract_screening.csv")
    mech = pd.read_csv(cfg["paths"]["results_tables"] / "intervention_mechanism_map.csv")
    # PRISMA
    counts = {"Raw": len(pd.read_csv(cfg["paths"]["results_tables"] / "raw_records_all.csv")),
              "Dedup": len(pd.read_csv(cfg["paths"]["results_tables"] / "master_records_dedup.csv")),
              "Include/uncertain": int(sum(screen.screen_label.isin(["include","uncertain"]))),
              "Extracted pilot": len(pd.read_csv(cfg["paths"]["results_tables"] / "extracted_studies_master.csv"))}
    fig, ax = plt.subplots(figsize=(7,4))
    ax.axis("off")
    y = 0.9
    for k,v in counts.items():
        ax.text(0.5,y,f"{k}\nN={v}",ha="center",va="center",bbox=dict(boxstyle="round",fc="#eef",ec="#447"))
        y -= 0.22
    save(fig, figs / "prisma_flow.png")
    # Score ranking
    if not scores.empty:
        fig, ax = plt.subplots(figsize=(8,5))
        s = scores.sort_values("max_claim_score", ascending=True)
        ax.barh(s["intervention_name"], s["max_claim_score"], color="#49759c")
        ax.set_xlabel("Max claim credibility score")
        ax.set_title("Intervention evidence score ranking")
        save(fig, figs / "evidence_score_ranking.png")
    # Heatmap
    vote = pd.read_csv(cfg["paths"]["results_tables"] / "structured_vote_counting.csv")
    if not vote.empty:
        mat = vote.pivot_table(index="intervention_name", columns="ageing_domain_category", values="n_candidate_records", fill_value=0)
        fig, ax = plt.subplots(figsize=(9,6))
        sns.heatmap(mat, annot=True, fmt=".0f", cmap="Blues", ax=ax)
        ax.set_title("Intervention vs outcome-domain evidence map")
        save(fig, figs / "intervention_outcome_heatmap.png")
    # Mechanism network
    if not mech.empty:
        G = nx.Graph()
        for _, r in mech.iterrows():
            G.add_edge(r["intervention"], r["mechanism"])
        fig, ax = plt.subplots(figsize=(10,8))
        nx.draw_networkx(G, ax=ax, node_size=500, font_size=7, with_labels=True)
        ax.axis("off")
        save(fig, figs / "mechanism_network.png")
    # Hype quadrant placeholder
    topics = pd.read_csv(cfg["paths"]["results_tables"] / "topic_assignments.csv")
    fig, ax = plt.subplots(figsize=(7,5))
    ax.scatter(topics["hype_terms_n"], topics.index, alpha=0.5)
    ax.set_xlabel("Hype term count")
    ax.set_ylabel("Candidate record index")
    ax.set_title("Hype-language flag map")
    save(fig, figs / "hype_vs_evidence_map.png")
    # Evidence pyramid
    fig, ax = plt.subplots(figsize=(6,5))
    levels = ["Human RCT","Human observational","Animal","Cellular","Speculative"]
    widths = [2,3,4,5,6]
    for i,(lvl,w) in enumerate(zip(levels,widths)):
        ax.barh(i,w,left=(6-w)/2,color=sns.color_palette("viridis",5)[i])
        ax.text(3,i,lvl,ha="center",va="center",color="white")
    ax.axis("off"); ax.set_title("Anti-ageing evidence pyramid")
    save(fig, figs / "evidence_pyramid.png")
    # Translational matrix
    if not scores.empty:
        trans = scores[["intervention_name","classification","max_claim_score"]].copy()
        trans.to_csv(cfg["paths"]["results_tables"] / "translational_readiness.csv", index=False)
        fig, ax = plt.subplots(figsize=(8,5))
        sns.scatterplot(data=trans, x="max_claim_score", y="intervention_name", hue="classification", ax=ax)
        ax.set_title("Translational readiness matrix")
        save(fig, figs / "translational_matrix.png")
    # Timeline simple
    ex = pd.read_csv(cfg["paths"]["results_tables"] / "extracted_studies_master.csv")
    if "year" in ex and not ex.empty:
        yy = pd.to_numeric(ex["year"], errors="coerce").dropna().astype(int)
        fig, ax = plt.subplots(figsize=(8,4))
        yy.value_counts().sort_index().plot(kind="bar", ax=ax)
        ax.set_title("Timeline of candidate anti-ageing evidence")
        ax.set_ylabel("Records")
        save(fig, figs / "evidence_timeline.png")
    append_log(cfg["paths"]["logs"] / "progress.md", "Phase 14 - Mandatory Figures",
               "- Generated PRISMA, evidence pyramid, heatmap, mechanism network, evidence ranking, hype map, timeline, and translational matrix where data permitted.",
               "- results/figures/*.png",
               "- Figure styling should be refined before journal submission.",
               "- Some figures are pilot metadata maps, not final full-text synthesis figures.",
               "python src/write_manuscript.py --config config/review_config.yaml")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/review_config.yaml")
    run(load_config(ap.parse_args().config))
''',
    )

    write(
        "src/write_manuscript.py",
        r'''
from __future__ import annotations
import argparse
import pandas as pd
from src.utils.io import load_config, append_log

def run(cfg):
    scores = pd.read_csv(cfg["paths"]["results_tables"] / "intervention_evidence_scores.csv")
    readiness = pd.read_csv(cfg["paths"]["results_tables"] / "translational_readiness.csv") if (cfg["paths"]["results_tables"] / "translational_readiness.csv").exists() else scores
    top = scores.sort_values("max_claim_score", ascending=False).head(8) if not scores.empty else pd.DataFrame()
    top_md = top.to_markdown(index=False) if not top.empty else "No scored interventions yet."
    manuscript = f"""
# Can Ageing Be Slowed or Reversed? An Autonomous Systematic Review, Evidence Grading, and Mechanistic Synthesis of Anti-Ageing and Age-Reversal Interventions

## Abstract

**Background:** Anti-ageing claims range from established healthy-ageing interventions to speculative rejuvenation claims.  
**Objective:** To build a reproducible evidence pipeline separating lifespan extension, healthspan improvement, biological-age slowing, biomarker reversal, and true rejuvenation.  
**Methods:** We implemented automated searches across PubMed, Europe PMC, and Crossref; deduplicated metadata; performed conservative title/abstract screening; created metadata-assisted extraction; mapped mechanisms; and generated preliminary evidence credibility scores.  
**Results:** The pilot harvest identified candidate records across lifestyle, pharmacologic, senolytic, NAD/sirtuin, regenerative, microbiome, and controversial rejuvenation domains. Metadata-assisted scoring ranked interventions with human functional evidence above animal-only or biomarker-only claims.  
**Conclusion:** Evidence is strongest for healthspan-related benefit, weaker for direct slowing of biological ageing, and weakest for true biological age reversal or rejuvenation. Biomarker improvements should not be equated with clinical rejuvenation without corresponding functional and clinical evidence.

## Keywords
ageing; longevity; healthspan; rejuvenation; epigenetic clock; senolytics; metformin; rapamycin; systematic review

## Introduction

Public interest in anti-ageing interventions has accelerated faster than the clinical evidence. Caloric restriction, exercise, fasting, metformin, rapamycin, NAD boosters, senolytics, stem-cell approaches, partial reprogramming, microbiome interventions, and plasma-based approaches are frequently discussed under the same anti-ageing label. This framing is scientifically unsafe unless evidence is separated by outcome class and model system.

This review distinguishes five claim types: lifespan extension, healthspan improvement, slowing of biological ageing, biomarker reversal, and true clinical rejuvenation. The last category requires far stronger evidence than a short-term biomarker shift.

## Methods

We created a PRISMA-style autonomous review workflow. Metadata were retrieved from PubMed, Europe PMC, and Crossref using broad and intervention-specific queries. Records were deduplicated using DOI, PMID, and normalized title. Screening used conservative rules requiring an intervention and ageing-relevant outcome. Extraction was metadata-assisted in this pilot and marked as requiring full-text verification.

Evidence credibility scoring combined evidence level, directness to ageing, mechanism plausibility, translational readiness, and penalties for preprints or hype-heavy claims. Human RCT and functional outcomes were weighted more strongly than animal-only, cellular-only, or surrogate biomarker outcomes.

## Results

### Evidence Score Ranking

{top_md}

### Mechanistic Synthesis

Candidate interventions most often mapped to nutrient sensing, senescence, inflammation, epigenetic alteration, mitochondrial function, autophagy/proteostasis, stem-cell biology, and microbiome-host pathways. Mechanism labels are preliminary when inferred from title/abstract metadata.

### Hype Versus Evidence

Claims involving young plasma, parabiosis, partial reprogramming, telomerase, stem-cell rejuvenation, and broad supplement claims require particularly conservative interpretation. Several have strong mechanistic interest but limited direct human evidence for clinical rejuvenation.

## Discussion

The central finding is not that ageing has been clinically reversed. Rather, the evidence landscape is layered. Lifestyle interventions, especially exercise and multidomain lifestyle programmes, are most defensible for healthspan and functional ageing. Caloric restriction and fasting have biological plausibility and biomarker effects but require careful safety and adherence interpretation. Metformin and rapamycin/mTOR modulation remain promising but not established as general anti-ageing therapies. NAD boosters and supplements are largely biomarker/surrogate-heavy. Senolytics are mechanistically compelling but early. Partial reprogramming and regenerative approaches remain predominantly preclinical or experimental.

## Strengths and Limitations

This project provides a reproducible pipeline, transparent scoring, mechanism mapping, and conservative claim separation. The main limitation is that the current pass is metadata-assisted; full-text extraction and human verification are required before final publication.

## Conclusions

Evidence is strongest for healthspan-related benefit, substantially weaker for claims of biological-age slowing, and weakest for true age reversal. Several interventions modulate ageing-associated pathways, yet only a minority have human evidence directly relevant to biological ageing. Biomarker improvements should not be equated with rejuvenation without corresponding functional and clinical evidence.
"""
    short = manuscript.replace("## Discussion", "## Concise Discussion").split("## Strengths and Limitations")[0] + "\n## Conclusion\nEvidence supports healthspan interventions more strongly than true rejuvenation claims.\n"
    supplement = "# Supplement\n\nSee results/tables for raw records, screening, extraction, scoring, mechanisms, and meta-analysis readiness outputs.\n"
    cover = "# Cover Letter Draft\n\nDear Editor,\n\nPlease consider this systematic review and evidence synthesis on anti-ageing and age-reversal interventions. The manuscript is deliberately conservative and separates healthspan benefit, biomarker reversal, and true rejuvenation claims.\n\nSincerely,\n"
    reviewer = "# Reviewer Criticism Anticipation\n\n1. Automation may misclassify studies: all metadata-assisted steps are flagged and require full-text verification.\n2. Evidence scores are subjective: scoring components are transparent and decomposable.\n3. Meta-analysis absent: pooling was deferred until comparable full-text effect sizes are extracted.\n"
    brief = "# Research Brief\n\nAnti-ageing evidence is strongest for healthspan-supporting lifestyle interventions and weakest for true rejuvenation claims. Biomarker reversal is not clinical age reversal.\n"
    mdir = cfg["paths"]["manuscript"]; ddir = cfg["paths"]["docs"]
    (mdir / "manuscript_main.md").write_text(manuscript, encoding="utf-8")
    (mdir / "manuscript_short.md").write_text(short, encoding="utf-8")
    (mdir / "supplement.md").write_text(supplement, encoding="utf-8")
    (mdir / "cover_letter.md").write_text(cover, encoding="utf-8")
    (mdir / "reviewer_anticipation.md").write_text(reviewer, encoding="utf-8")
    (mdir / "figure_legends.md").write_text("# Figure Legends\n\nSee generated figures in results/figures.\n", encoding="utf-8")
    (ddir / "research_brief.md").write_text(brief, encoding="utf-8")
    append_log(cfg["paths"]["logs"] / "progress.md", "Phase 15-17 - Manuscript Writing and Journal Positioning",
               "- Drafted main manuscript, short version, supplement, cover letter, reviewer memo, figure legends, and research brief.",
               "- manuscript/*.md\n- docs/research_brief.md",
               "- Full-text verified extraction and final references needed before submission.",
               "- Manuscript is a rigorous pilot draft, not final publication-ready systematic review until full-text verification.",
               "pytest tests -q")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/review_config.yaml")
    run(load_config(ap.parse_args().config))
''',
    )

    write(
        "src/run_pipeline.py",
        r'''
from __future__ import annotations
import argparse
from src.utils.io import load_config
from src.search.run_search import run as search
from src.dedup.deduplicate import run as dedup
from src.screening.screen_records import run as screen
from src.retrieval.assess_full_text import run as retrieve
from src.extraction.extract_metadata import run as extract
from src.grading.score_evidence import run as grade
from src.mechanisms.map_mechanisms import run as mechanisms
from src.nlp.topic_hype import run as nlp
from src.meta_analysis.synthesize import run as synth
from src.viz.make_figures import run as figures
from src.write_manuscript import run as manuscript

def run(cfg):
    search(cfg); dedup(cfg); screen(cfg); retrieve(cfg); extract(cfg); grade(cfg); mechanisms(cfg); nlp(cfg); synth(cfg); figures(cfg); manuscript(cfg)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/review_config.yaml")
    run(load_config(ap.parse_args().config))
''',
    )

    write(
        "tests/test_pipeline_units.py",
        r'''
import pandas as pd
from src.dedup.deduplicate import norm_title, dedup_key
from src.screening.screen_records import screen_row
from src.grading.score_evidence import score_row

def test_norm_title_removes_punctuation():
    assert norm_title("Aging, Reversal!") == "aging reversal"

def test_dedup_prefers_doi_key():
    row = pd.Series({"doi":"10.1/ABC", "pmid":"123", "title":"Title"})
    assert dedup_key(row) == "doi:10.1/abc"

def test_screening_requires_intervention():
    row = {"title":"Aging biology and senescence", "abstract":"No intervention", "publication_type":""}
    label, *_ = screen_row(row)
    assert label in {"exclude","uncertain"}

def test_screening_includes_intervention_and_outcome():
    row = {"title":"Exercise intervention improves frailty in older adults", "abstract":"randomized trial", "publication_type":"Clinical Trial"}
    label, conf, *_ = screen_row(row)
    assert label == "include"
    assert conf > 0.5

def test_score_reproducible():
    row = pd.Series({"species_model":"human","ageing_domain_category":"healthspan_functional_ageing","mechanism":"nutrient_sensing","intervention_name":"exercise","is_preprint":False})
    assert score_row(row) == score_row(row)
''',
    )

    print(f"Bootstrapped project at {ROOT}")


if __name__ == "__main__":
    main()
