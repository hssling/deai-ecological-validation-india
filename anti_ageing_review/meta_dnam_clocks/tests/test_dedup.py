import importlib.util
from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
spec = importlib.util.spec_from_file_location("dm", ROOT / "src" / "03_dedup_merge.py")
dm = importlib.util.module_from_spec(spec); spec.loader.exec_module(dm)

COLS = ["doi","pmid","title","year","source","source_id","abstract","authors","journal","url","fetched_at"]
def _mk(rows):
    return pd.DataFrame([{c: r.get(c, "") for c in COLS} for r in rows])

def test_exact_doi_collapses():
    df = _mk([{"doi":"10.1/a","title":"X","year":"2024","source":"pubmed","source_id":"1"},
              {"doi":"10.1/A","title":"X","year":"2024","source":"crossref","source_id":"2"}])
    out = dm.dedup(df)
    assert len(out) == 1

def test_exact_pmid_collapses():
    df = _mk([{"pmid":"123","title":"X","year":"2024","source":"a","source_id":"1"},
              {"pmid":"123","title":"X2","year":"2024","source":"b","source_id":"2"}])
    assert len(dm.dedup(df)) == 1

def test_fuzzy_title_collapses_near_dup():
    df = _mk([{"title":"Exercise and GrimAge in older adults","year":"2023","source":"a","source_id":"1"},
              {"title":"Exercise and GrimAge in older adults.","year":"2023","source":"b","source_id":"2"}])
    assert len(dm.dedup(df)) == 1

def test_different_titles_kept():
    df = _mk([{"title":"Exercise and GrimAge","year":"2023","source":"a","source_id":"1"},
              {"title":"Caloric restriction and PhenoAge","year":"2023","source":"b","source_id":"2"}])
    assert len(dm.dedup(df)) == 2
