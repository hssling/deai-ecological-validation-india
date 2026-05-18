"""Unit tests for src/01_search_dnam.py."""
import json
from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
spec = importlib.util.spec_from_file_location("search_mod", ROOT / "src" / "01_search_dnam.py")
search_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(search_mod)


def test_query_builder_combines_blocks():
    q = search_mod.build_query(["DunedinPACE", "GrimAge"], ["trial", "exercise"])
    assert '"DunedinPACE"' in q
    assert '"GrimAge"' in q
    assert '"trial"' in q
    assert " AND " in q


def test_pubmed_normalizer_minimal():
    fixture = json.loads((Path(__file__).parent / "fixtures" / "pubmed_sample.json").read_text())
    rows = search_mod.normalize_pubmed(fixture)
    assert len(rows) == 1
    r = rows[0]
    assert r["source"] == "pubmed"
    assert r["pmid"] == "12345"
    assert r["doi"] == "10.1/example"
    assert "Exercise" in r["title"]
    assert r["year"] == "2024"


def test_europepmc_normalizer_minimal():
    payload = {"resultList": {"result": [{"id": "abc", "pmid": "999", "doi": "10.2/x",
                                          "title": "T", "abstractText": "A", "authorString": "X Y",
                                          "pubYear": "2023", "journalTitle": "J"}]}}
    rows = search_mod.normalize_europepmc(payload)
    assert len(rows) == 1 and rows[0]["pmid"] == "999" and rows[0]["title"] == "T"


def test_crossref_normalizer_minimal():
    payload = {"message": {"items": [{"DOI": "10.3/y", "title": ["Hi"], "abstract": "ab",
                                       "author": [{"given": "A", "family": "B"}],
                                       "issued": {"date-parts": [[2022]]},
                                       "container-title": ["J2"], "URL": "https://x"}]}}
    rows = search_mod.normalize_crossref(payload)
    assert len(rows) == 1 and rows[0]["doi"] == "10.3/y" and rows[0]["year"] == "2022"


def test_openalex_normalizer_minimal():
    payload = {"results": [{"id": "W1", "ids": {"pmid": "https://pubmed.gov/7"},
                            "doi": "https://doi.org/10.4/z", "title": "T3", "publication_year": 2021,
                            "authorships": [{"author": {"display_name": "Z"}}],
                            "host_venue": {"display_name": "J3"}}]}
    rows = search_mod.normalize_openalex(payload)
    assert len(rows) == 1 and rows[0]["pmid"] == "7" and rows[0]["doi"] == "10.4/z"


def test_clinicaltrials_normalizer_minimal():
    payload = {"studies": [{"protocolSection": {
        "identificationModule": {"nctId": "NCT0001", "officialTitle": "Of T"},
        "descriptionModule": {"briefSummary": "summ"},
        "statusModule": {"completionDateStruct": {"date": "2024-06-01"}}}}]}
    rows = search_mod.normalize_clinicaltrials(payload)
    assert len(rows) == 1 and rows[0]["source_id"] == "NCT0001" and rows[0]["year"] == "2024"
