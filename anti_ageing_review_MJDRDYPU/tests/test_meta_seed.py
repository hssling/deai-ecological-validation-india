import pandas as pd

from src.meta_addon.pool_same_outcome import _months_from_timepoint
from src.meta_addon.reconstruct_fmd_bioage import compute_change
from src.meta_addon.seed_numeric_extractions import (
    has_observed_value,
    hedges_g_from_post,
    se_from_two_sided_p_unpaired_t,
)


def test_hedges_g_from_post_positive_when_treatment_better():
    g, se = hedges_g_from_post(30, 20.8, 7.59, 30, 16.2, 6.04)
    assert g > 0
    assert se > 0


def test_hedges_g_from_post_negative_when_lower_is_better_but_treatment_lower():
    g, se = hedges_g_from_post(28, 0.8, 1.0, 15, 4.0, 1.0)
    assert g < 0
    assert se > 0


def test_has_observed_value_treats_blank_strings_as_missing():
    observed = has_observed_value(pd.Series(["", "  ", None, 1.2, "0.0"]))
    assert observed.tolist() == [False, False, False, True, True]


def test_months_from_timepoint_ranks_follow_up_windows():
    assert _months_from_timepoint("24_months_itt") > _months_from_timepoint("12_months_itt")


def test_fmd_compute_change_returns_rows_for_complete_six_marker_records():
    df = pd.DataFrame(
        [
            {
                "ID": 1,
                "albumin_bl": 4.7,
                "albumin_fu": 4.4,
                "alp_bl": 53.0,
                "alp_fu": 43.0,
                "creat_bl": 1.18,
                "creat_fu": 1.06,
                "crp_bl": 0.885,
                "crp_fu": 0.567,
                "sbp_bl": 134.0,
                "sbp_fu": 127.5,
                "totchol_bl": 269.0,
                "totchol_fu": 208.0,
            }
        ]
    )
    res = compute_change(df)
    assert len(res) == 1
    assert res.iloc[0]["n_available_biomarkers"] == 6


def test_se_from_two_sided_p_unpaired_t_returns_positive_value():
    se = se_from_two_sided_p_unpaired_t(-3.23, 0.018, 21, 22)
    assert se > 0
