import pandas as pd
from src.dedup.deduplicate import norm_title, dedup_key
from src.screening.screen_records import screen_row
from src.grading.score_evidence import claim_category_from_row, score_row
from src.utils.quality_checks import missing_schema_fields, run_checks

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

def test_animal_claim_cannot_be_supported_category():
    row = pd.Series({
        "species_model": "animal",
        "ageing_domain_category": "hard_ageing_relevance",
        "claim_score": 11.0,
    })
    assert claim_category_from_row(row) == "promising_but_incomplete"

def test_extraction_schema_detects_missing_fields():
    df = pd.DataFrame({"title": ["Study"], "year": [2024]})
    missing = missing_schema_fields(df)
    assert "effect_size" in missing
    assert "intervention_name" in missing

def test_quality_checks_flag_surrogate_overclassification():
    extracted = pd.DataFrame({
        "title": ["Study"],
        "authors": ["A"],
        "year": [2024],
        "journal": ["J"],
        "doi": [""],
        "pmid": [""],
        "study_design": ["RCT"],
        "species_model": ["human"],
        "intervention_name": ["supplements"],
        "dose_intensity": [""],
        "duration": [""],
        "comparator": [""],
        "outcome_exact": [""],
        "ageing_domain_category": ["surrogate_or_indirect"],
        "effect_size": [""],
        "uncertainty_measure": [""],
        "follow_up_time": [""],
        "mechanism": ["inflammation"],
        "mechanism_directness": ["inferred_from_title_abstract"],
        "extraction_confidence": [0.45],
        "missingness_flag": ["requires_full_text_verification"],
    })
    claims = extracted.assign(
        is_preprint=False,
        claim_category="supported_for_healthspan_related_benefit",
    )
    scores = pd.DataFrame({
        "intervention_name": ["supplements"],
        "classification": ["supported_for_healthspan_related_benefit"],
        "human_records": [1],
        "max_claim_score": [12],
    })
    audit = run_checks(extracted, claims, scores, pd.DataFrame())
    surrogate = audit[audit["issue_type"].eq("surrogate_endpoint_overclassified")].iloc[0]
    assert surrogate["n_records"] == 1
    assert surrogate["severity"] == "medium"
