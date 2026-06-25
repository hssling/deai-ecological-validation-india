import numpy as np
import pandas as pd

from src.health_economics import deflate
from src.health_economics import che_indicators, impoverishment


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


def _toy():
    return pd.DataFrame({
        "oop_total":[5,30,0,50], "cons_total":[100,100,100,100],
        "capacity_to_pay":[50,50,50,50], "cons_pc":[60,60,40,30],
        "r1wtresp":[1,1,1,1]})

def test_che10_headcount():
    r = che_indicators(_toy())
    assert round(r["che10"],1) == 50.0       # shares .05,.30,0,.50 -> >10%: 2 of 4
    assert round(r["che40cap"],1) == 50.0     # caps .10,.60,0,1.0 -> >40%: 2 of 4

def test_impoverishment_counts_newly_poor():
    r = impoverishment(_toy(), line=50.0)
    assert round(r["pre_poverty"], 1) == 50.0
    assert round(r["post_poverty"], 1) == 75.0
    assert round(r["impov_headcount"], 1) == 25.0
    assert round(r["poverty_gap_increase"], 1) == 25.0
