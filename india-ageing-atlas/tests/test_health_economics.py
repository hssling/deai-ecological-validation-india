import numpy as np
import pandas as pd

from src.health_economics import deflate


def test_deflate_to_base_year_is_identity_at_base():
    s = pd.Series([100.0, 200.0])
    out = deflate(s, {2017: 100.0, 2019: 125.0}, year=2019, base=2017)
    assert np.allclose(out.values, [80.0, 160.0])


def test_economics_frame_builds():
    from src.health_economics import load_economics_frame

    df = load_economics_frame(
        "data/raw/g2aging_harmonized_lasi_a3_sav/H_LASI_a3.sav",
        "data/processed/analysis_dataset.csv",
    )
    assert len(df) > 50000
    assert (df["oop_total"].dropna() >= 0).all()
    assert df["capacity_to_pay"].dropna().ge(0).all()
