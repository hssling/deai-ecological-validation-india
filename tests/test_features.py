"""Unit tests for Phase 3 feature engineering."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.features.build_features import (
    _apply_transform,
    build_features,
    EXPOSOME_VARS,
    OUTCOME_VARS,
)


@pytest.fixture
def minimal_df():
    rng = np.random.default_rng(42)
    n = 200
    return pd.DataFrame({
        "id": [f"T{i:03d}" for i in range(n)],
        "age_years": rng.integers(40, 90, n).astype(float),
        "sex": rng.integers(0, 2, n),
        "education_years": rng.uniform(0, 20, n),
        "ses_quintile": rng.integers(1, 6, n),
        "region": rng.choice(["north", "south"], n),
        "urban_rural": rng.integers(0, 2, n),
        "pm25_annual_ugm3": rng.uniform(10, 200, n),
        "heat_days_per_year": rng.uniform(0, 180, n),
        "tobacco_ever": rng.integers(0, 2, n),
        "alcohol_ever": rng.integers(0, 2, n),
        "diet_diversity_score": rng.uniform(1, 9, n),
        "frailty_index": rng.uniform(0.01, 0.90, n),
        "multimorbidity_binary": rng.integers(0, 2, n),
        "disability_binary": rng.integers(0, 2, n),
        "srh_poor_binary": rng.integers(0, 2, n),
        "mortality_5yr_binary": rng.integers(0, 2, n),
    })


def test_apply_transform_log1p_nonnegative(minimal_df):
    result = _apply_transform(minimal_df["pm25_annual_ugm3"], "log1p")
    assert (result >= 0).all(), "log1p output must be non-negative"


def test_apply_transform_sqrt_nonnegative(minimal_df):
    result = _apply_transform(minimal_df["heat_days_per_year"], "sqrt")
    assert (result >= 0).all()


def test_apply_transform_none_unchanged(minimal_df):
    original = minimal_df["tobacco_ever"].copy()
    result = _apply_transform(minimal_df["tobacco_ever"], "none")
    pd.testing.assert_series_equal(result, original)


def test_build_features_returns_correct_types(minimal_df):
    feature_df, var_map = build_features(minimal_df)
    assert isinstance(feature_df, pd.DataFrame)
    assert isinstance(var_map, pd.DataFrame)


def test_build_features_standardized_cols(minimal_df):
    feature_df, _ = build_features(minimal_df)
    for col in EXPOSOME_VARS:
        t_col = f"{col}_t"
        assert t_col in feature_df.columns, f"Missing transformed column: {t_col}"
        # After standardization, mean should be ~0 and std ~1
        assert abs(feature_df[t_col].mean()) < 0.1, f"{t_col} mean not ~0"
        assert abs(feature_df[t_col].std() - 1.0) < 0.1, f"{t_col} std not ~1"


def test_build_features_outcome_preserved(minimal_df):
    feature_df, _ = build_features(minimal_df)
    for col in OUTCOME_VARS:
        assert col in feature_df.columns, f"Outcome column missing: {col}"


def test_build_features_no_rows_lost(minimal_df):
    feature_df, _ = build_features(minimal_df)
    assert len(feature_df) == len(minimal_df)


def test_variable_map_has_required_cols(minimal_df):
    _, var_map = build_features(minimal_df)
    required = {"variable", "domain", "direction", "type"}
    assert required.issubset(set(var_map.columns))


def test_missing_column_handled_gracefully(minimal_df):
    df_missing = minimal_df.drop(columns=["pm25_annual_ugm3"])
    feature_df, _ = build_features(df_missing)
    assert "pm25_annual_ugm3_t" in feature_df.columns
