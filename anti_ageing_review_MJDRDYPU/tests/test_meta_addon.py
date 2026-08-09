import pandas as pd

from src.meta_addon.build_addon import _endpoint_family, _source_locator, META_DATASET_COLUMNS


def test_endpoint_family_maps_frailty_function():
    row = pd.Series(
        {
            "title": "Exercise trial in frailty",
            "outcome_exact": "gait speed and grip strength",
            "ageing_domain_category": "healthspan_functional_ageing",
            "intervention_name": "exercise",
        }
    )
    assert _endpoint_family(row) == "frailty_function"


def test_endpoint_family_maps_epigenetic_age():
    row = pd.Series(
        {
            "title": "Lifestyle intervention and DNAm PhenoAge",
            "outcome_exact": "epigenetic age",
            "ageing_domain_category": "biological_ageing_biomarker",
            "intervention_name": "lifestyle_bundle",
        }
    )
    assert _endpoint_family(row) == "epigenetic_biological_age"


def test_source_locator_prefers_local_pmc():
    row = pd.Series({"pmcid": "PMC123", "pmid": "456", "doi": "10.1/x", "url": "https://example.com"})
    source_type, locator = _source_locator(row, {"PMC123.xml", "pubmed_456.xml"})
    assert source_type == "pmc_xml"
    assert locator.endswith("PMC123.xml")


def test_meta_dataset_template_columns_include_required_fields():
    assert "study_id" in META_DATASET_COLUMNS
    assert "effect_metric" in META_DATASET_COLUMNS
    assert "ready_for_pooling" in META_DATASET_COLUMNS
