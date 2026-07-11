import math

import pytest

from lasi_spirometry_reference import available_age_range, predict, score_spirometry


def test_age_range():
    assert available_age_range() == (45, 90)


def test_lookup_values_match_manuscript_examples():
    fvc = predict("M", 60, 165, "fvc")
    fev1 = predict("M", 60, 165, "fev1")
    assert round(fvc.median, 2) == 2.78
    assert round(fvc.lln, 2) == 1.83
    assert round(fev1.median, 2) == 2.19
    assert round(fev1.lln, 2) == 1.37

    fvc_w = predict("F", 70, 150, "fvc")
    fev1_w = predict("F", 70, 150, "fev1")
    assert round(fvc_w.median, 2) == 1.78
    assert round(fvc_w.lln, 2) == 1.14
    assert round(fev1_w.median, 2) == 1.41
    assert round(fev1_w.lln, 2) == 0.85


def test_score_spirometry_returns_ratio_and_classification():
    result = score_spirometry("male", 60, 165, fev1_l=2.10, fvc_l=2.60)
    assert math.isclose(result["fev1fvc"]["observed"], 80.76923076923077)
    assert set(result["classification"]) == {
        "obstruction_lln",
        "preserved_ratio",
        "prism_fixed",
        "prism_lln",
        "rsp_fixed",
        "rsp_lln",
    }


def test_age_outside_range_raises():
    with pytest.raises(ValueError):
        predict("M", 44, 165, "fvc")
