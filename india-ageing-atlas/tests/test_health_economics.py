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


from src.health_economics import erreygers_index, decompose_concentration


def test_erreygers_sign_and_zero():
    base = pd.DataFrame({"rank":[1,2,3,4], "w":[1,1,1,1]})
    prorich = base.assign(y=[0,0,1,1])   # outcome concentrated among richer -> positive
    propoor = base.assign(y=[1,1,0,0])   # concentrated among poorer -> negative
    flat    = base.assign(y=[1,1,1,1])   # no gradient -> 0
    assert erreygers_index(prorich, "y", "rank", "w") > 0
    assert erreygers_index(propoor, "y", "rank", "w") < 0
    assert abs(erreygers_index(flat, "y", "rank", "w")) < 1e-9

def test_decomposition_single_regressor_explains_all():
    # y = 2*x exactly: the single regressor must explain ~100% of the concentration
    df = pd.DataFrame({"x":[1.,2.,3.,4.,5.], "w":[1.,1.,1.,1.,1.]})
    df["y"] = 2 * df["x"]
    out = decompose_concentration(df, "y", "x", ["x"], "w")
    row = out[out["regressor"] == "x"].iloc[0]
    assert abs(row["pct_of_total"] - 100.0) < 1.0


from src.health_economics import compute_care_hours_week, informal_care_value

def test_compute_care_hours_week():
    df = pd.DataFrame({"r1rscaredpm_l":[30],"r1rscarehr_l":[2],
        "r1rccaredpm_l":[0],"r1rccarehr_l":[0],
        "r1rrcaredpm_l":[0],"r1rrcarehr_l":[0],
        "r1rfcaredpm_l":[0],"r1rfcarehr_l":[0]})
    # 30*2=60 hrs/month *12/52 = 13.846 hrs/wk
    assert abs(compute_care_hours_week(df).iloc[0] - 13.846) < 0.05

def test_informal_care_value_per_recipient():
    df = pd.DataFrame({"r1rcany":[1,1,0,0], "care_hours_week":[10,10,0,0], "r1wtresp":[1,1,1,1]})
    r = informal_care_value(df, wage_hour=50.0, pop_scale=1000.0)
    assert round(r["recipients_pct"],1) == 50.0
    assert round(r["mean_hours_week"],1) == 10.0
    assert round(r["annual_value_per_recipient"],0) == 26000.0      # 10*52*50
    assert round(r["national_annual_value"],0) == 13_000_000.0       # 1000*0.5*26000


from src.health_economics import two_part_model


def test_two_part_model_recovers_positive_driver():
    rng = np.random.default_rng(0)
    n = 800
    x = rng.normal(0, 1, n); z = rng.normal(0, 1, n)
    p = 1 / (1 + np.exp(-(0.5 + 1.2 * x)))
    pos = rng.binomial(1, p)
    amount = np.exp(6 + 0.8 * x + rng.normal(0, 0.3, n))
    y = pos * amount
    df = pd.DataFrame({"oop_total": y, "x": x, "z": z, "r1wtresp": 1.0})
    res = two_part_model(df, "oop_total", ["x", "z"])
    assert set(res["part"]) == {"participation", "amount"}
    row = res[(res["part"] == "participation") & (res["term"] == "x")].iloc[0]
    assert row["coef"] > 0


from src.health_economics import add_che_flags, che_ml_drivers


def test_add_che_flags():
    df = pd.DataFrame({"oop_total":[5,30,0,50],"cons_total":[100,100,100,100],"capacity_to_pay":[50,50,50,50]})
    out = add_che_flags(df)
    assert out["che40cap_flag"].tolist() == [0,1,0,1]

def test_ml_drivers_finds_signal_and_ranks_feature():
    rng = np.random.default_rng(1)
    n = 1000
    x = rng.normal(size=n)
    target = (x + 0.3 * rng.normal(size=n) > 0).astype(int)
    df = pd.DataFrame({"che40cap_flag": target, "x": x, "z": rng.normal(size=n), "r1wtresp": 1.0})
    out = che_ml_drivers(df, "che40cap_flag", ["x", "z"])
    assert out["auc"] > 0.7
    assert out["shap_importance"].iloc[0]["feature"] == "x"


from src.health_economics import simulate_policy


def test_simulate_full_inpatient_cover_reduces_che_and_costs():
    df = pd.DataFrame({
        "oop_hosp":[60,0,0,0], "oop_med":[0,0,0,0], "oop_out":[0,0,0,0], "oop_total":[60,0,0,0],
        "cons_total":[100,100,100,100], "cons_nonfood":[50,50,50,50],
        "capacity_to_pay":[50,50,50,50], "cons_pc":[60,60,40,30],
        "age_years":[70,70,70,70], "r1wtresp":[1,1,1,1]})
    base = che_indicators(df)            # che40cap = 25% (one of four: 60/50=1.2>0.4)
    r = simulate_policy(df, {"inpatient_cover_frac":1.0, "age_min":0}, line=50.0)
    assert r["che40cap"] <= base["che40cap"]
    assert r["che40cap"] == 0.0          # hospital OOP fully removed -> no CHE
    assert r["che40cap_delta"] <= 0
    assert r["fiscal_cost"] == 60.0      # absorbed 60 * weight 1
