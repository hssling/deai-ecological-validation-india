"""Integration orchestrator for the MJDRDYPU health-economics study.

Runs the full health-economics analysis on real LASI (H_LASI_a3.sav) data and
writes all result tables to outputs/health_economics_mjdrdypu/tables/.

All analytic logic lives in src/health_economics.py and src/inequality.py;
this script only assembles frames, calls those functions, and writes CSVs.

Run as:
    python scripts/run_health_economics_mjdrdypu.py
from the repo root.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd
import pyreadstat

from src.health_economics import (
    load_economics_frame, che_indicators, impoverishment,
    erreygers_index, decompose_concentration, compute_care_hours_week,
    informal_care_value, two_part_model, add_che_flags, che_ml_drivers,
    simulate_policy,
)
from src.inequality import concentration_index

SAV = "data/raw/g2aging_harmonized_lasi_a3_sav/H_LASI_a3.sav"
PROC = "data/processed/analysis_dataset.csv"
OUT = Path("outputs/health_economics_mjdrdypu/tables")
OUT.mkdir(parents=True, exist_ok=True)

CARE_COLS = ["prim_key", "r1rcany", "r1rscaredpm_l", "r1rscarehr_l", "r1rccaredpm_l", "r1rccarehr_l",
             "r1rrcaredpm_l", "r1rrcarehr_l", "r1rfcaredpm_l", "r1rfcarehr_l"]

COVARS = ["age_years", "is_female", "is_rural", "multimorbidity_ge2",
          "functional_limitation", "any_pension", "education"]


def params() -> dict[str, float]:
    p = pd.read_csv("data/external/health_economics_params.csv")
    return dict(zip(p["parameter"], pd.to_numeric(p["value"], errors="coerce")))


def weighted_quantile(values, q, w):
    v = pd.to_numeric(values, errors="coerce")
    wn = pd.to_numeric(w, errors="coerce")
    m = v.notna() & wn.notna()
    v, wn = v[m], wn[m]
    order = np.argsort(v.values)
    vv = v.values[order]
    ww = wn.values[order]
    cw = np.cumsum(ww) - 0.5 * ww
    cw /= ww.sum()
    return float(np.interp(q, cw, vv))


def wpct(mask, w):
    w = pd.to_numeric(w, errors="coerce").fillna(0)
    m = pd.Series(mask).astype(float)
    return float(100 * np.average(m, weights=w)) if w.sum() > 0 else np.nan


def wmedian(values, w):
    return weighted_quantile(values, 0.5, w)


def wmean(values, w):
    v = pd.to_numeric(values, errors="coerce")
    wn = pd.to_numeric(w, errors="coerce").fillna(0)
    m = v.notna()
    return float(np.average(v[m], weights=wn[m])) if wn[m].sum() > 0 else np.nan


# ---------------------------------------------------------------------------
# Table builders
# ---------------------------------------------------------------------------

def build_table1(s60: pd.DataFrame) -> pd.DataFrame:
    w = s60["r1wtresp"]
    row = {
        "n_unweighted": int(len(s60)),
        "pct_female": wpct(s60["is_female"] == 1, w),
        "pct_rural": wpct(s60["is_rural"] == 1, w),
        "pct_multimorbid": wpct(pd.to_numeric(s60["multimorbidity_ge2"], errors="coerce") == 1, w),
        "pct_functional_limitation": wpct(pd.to_numeric(s60["functional_limitation"], errors="coerce") == 1, w),
        "pct_living_alone": wpct(pd.to_numeric(s60["living_alone"], errors="coerce") == 1, w),
        "pct_any_pension": wpct(pd.to_numeric(s60["any_pension"], errors="coerce") == 1, w),
        "median_oop_total": wmedian(s60["oop_total"], w),
        "mean_oop_total": wmean(s60["oop_total"], w),
        "median_cons_total": wmedian(s60["cons_total"], w),
        "mean_cons_total": wmean(s60["cons_total"], w),
        "pct_any_oop": wpct(pd.to_numeric(s60["oop_total"], errors="coerce").fillna(0) > 0, w),
    }
    return pd.DataFrame([row])


def build_table2(s60: pd.DataFrame) -> pd.DataFrame:
    groups = {
        "All 60+": s60,
        "70+": s60[pd.to_numeric(s60["age_years"], errors="coerce") >= 70],
        "Men 60+": s60[s60["is_female"] == 0],
        "Women 60+": s60[s60["is_female"] == 1],
        "Rural 60+": s60[s60["is_rural"] == 1],
        "Urban 60+": s60[s60["is_rural"] == 0],
        "Multimorbid 60+": s60[pd.to_numeric(s60["multimorbidity_ge2"], errors="coerce") == 1],
    }
    rows = []
    for label, sub in groups.items():
        ind = che_indicators(sub)
        rows.append({"group": label, "n_unweighted": int(len(sub)), **ind})
    return pd.DataFrame(rows)


def build_table3(s60: pd.DataFrame, line: float) -> pd.DataFrame:
    groups = {
        "All 60+": s60,
        "Men 60+": s60[s60["is_female"] == 0],
        "Women 60+": s60[s60["is_female"] == 1],
        "Rural 60+": s60[s60["is_rural"] == 1],
        "Urban 60+": s60[s60["is_rural"] == 0],
    }
    rows = []
    for label, sub in groups.items():
        ind = impoverishment(sub, oop="oop_pc", cons_pc="cons_pc", line=line)
        rows.append({"group": label, "n_unweighted": int(len(sub)), "poverty_line": line, **ind})
    return pd.DataFrame(rows)


def build_table4(s60: pd.DataFrame):
    outcome = "che40cap_flag"
    rank_var = "cons_pc"
    ci = concentration_index(s60, outcome, rank_var, "r1wtresp")
    erg = erreygers_index(s60, outcome, rank_var, weight="r1wtresp")
    decomp = decompose_concentration(s60, outcome, rank_var, COVARS, weight="r1wtresp")
    header = pd.DataFrame([{
        "regressor": "__TOTAL__", "elasticity": np.nan, "CI_regressor": ci,
        "contribution": np.nan, "pct_of_total": np.nan,
        "concentration_index": ci, "erreygers_index": erg,
    }])
    decomp = decomp.assign(concentration_index=ci, erreygers_index=erg)
    out = pd.concat([header, decomp], ignore_index=True)
    return out, ci, erg


def build_table5(s60: pd.DataFrame) -> pd.DataFrame:
    tp = two_part_model(s60, y="oop_total", covars=COVARS, weight="r1wtresp")
    tp_rows = []
    for _, r in tp.iterrows():
        method = "two_part_participation" if r["part"] == "participation" else "two_part_amount"
        tp_rows.append({
            "method": method, "feature": r["term"], "coef": r["coef"], "ratio": r["ratio"],
            "ci_low": r["ci_low"], "ci_high": r["ci_high"], "p": r["p"], "importance": np.nan,
        })
    ml = che_ml_drivers(s60, target="che40cap_flag", features=COVARS, weight="r1wtresp")
    shap_rows = []
    for _, r in ml["shap_importance"].iterrows():
        shap_rows.append({
            "method": "shap", "feature": r["feature"], "coef": np.nan, "ratio": np.nan,
            "ci_low": np.nan, "ci_high": np.nan, "p": np.nan, "importance": r["mean_abs_shap"],
        })
    out = pd.DataFrame(tp_rows + shap_rows)
    out.attrs["auc"] = ml["auc"]
    return out


def build_table6(s60: pd.DataFrame, line: float, P: dict[str, float]) -> pd.DataFrame:
    pop_scale = P["pop_60plus_india"]
    wage = P["care_worker_wage_hour"]
    pension_topup_year = P["ignoaps_pension_60_79"] * 12  # informational; topup amounts set per-scenario below

    scenarios = {
        "S1 PM-JAY 70+ full inpatient cover": {"inpatient_cover_frac": 1.0, "age_min": 70},
        "S2 Outpatient (incl. medicines) cover, all 60+": {"outpatient_cover_frac": 1.0, "age_min": 60},
        "S3 Pension top-up +Rs500/mo, all 60+": {"pension_topup_annual": 6000, "age_min": 60},
        "S4 Combined S1+S2+S3": {
            "inpatient_cover_frac": 1.0, "outpatient_cover_frac": 1.0,
            "pension_topup_annual": 6000, "age_min": 60,
        },
    }
    rows = []
    for label, scen in scenarios.items():
        res = simulate_policy(s60, scen, weight="r1wtresp", line=line, pop_scale=pop_scale)
        rows.append({"scenario": label, **scen, **res})
    out = pd.DataFrame(rows)
    out.attrs["wage_hour"] = wage
    out.attrs["pension_topup_annual_ref"] = pension_topup_year
    return out


def build_table_caregiving(s60: pd.DataFrame, P: dict[str, float]) -> pd.DataFrame:
    wage = P["care_worker_wage_hour"]
    pop_scale = P["pop_60plus_india"]
    res = informal_care_value(
        s60, needs_help_col="r1rcany", hours_week_col="care_hours_week",
        wage_hour=wage, weight="r1wtresp", pop_scale=pop_scale, opportunity_wage_hour=wage,
    )
    return pd.DataFrame([res])


def main() -> None:
    df = load_economics_frame(SAV, PROC)
    care, _ = pyreadstat.read_sav(SAV, usecols=CARE_COLS)
    care["prim_key"] = pd.to_numeric(care["prim_key"], errors="coerce").astype("Int64")
    df = df.merge(care, on="prim_key", how="left")
    df["care_hours_week"] = compute_care_hours_week(df)
    df["is_female"] = (df["sex"].astype(str).str.lower() == "female").astype(int)
    df["is_rural"] = (df["residence"].astype(str).str.lower() == "rural").astype(int)
    df = add_che_flags(df)

    P = params()
    s60 = df[pd.to_numeric(df["age_years"], errors="coerce") >= 60].copy()

    # Poverty line: weighted quantile of cons_pc at the weighted poverty_intl rate
    rate = float(np.average(pd.to_numeric(s60["poverty_intl"], errors="coerce").fillna(0),
                             weights=s60["r1wtresp"]))
    line = weighted_quantile(s60["cons_pc"], rate, s60["r1wtresp"])

    print(f"Sample: 45+ frame n={len(df)}, 60+ analytic sample n={len(s60)}")
    print(f"Poverty rate (weighted, intl line) among 60+: {rate * 100:.2f}% -> poverty line (cons_pc) = Rs {line:,.0f}")

    # Table 1: sample characteristics
    t1 = build_table1(s60)
    t1.to_csv(OUT / "table1_sample.csv", index=False)
    print(f"Table1 — 60+ n={t1['n_unweighted'].iloc[0]}, any-OOP={t1['pct_any_oop'].iloc[0]:.1f}%, "
          f"median OOP=Rs {t1['median_oop_total'].iloc[0]:,.0f}")

    # Table 2: CHE indicators by subgroup
    t2 = build_table2(s60)
    t2.to_csv(OUT / "table2_che.csv", index=False)
    che40_all = t2.loc[t2["group"] == "All 60+", "che40cap"].iloc[0]
    print(f"CHE40 among 60+: {che40_all:.1f}%")

    # Table 3: impoverishment
    t3 = build_table3(s60, line)
    t3.to_csv(OUT / "table3_impoverishment.csv", index=False)
    impov_all = t3.loc[t3["group"] == "All 60+", "impov_headcount"].iloc[0]
    print(f"Impoverishment headcount (post-OOP) among 60+: {impov_all:.2f} pp (poverty line = Rs {line:,.0f}/yr per capita)")

    # Table 4: equity / concentration decomposition
    t4, ci_val, erg_val = build_table4(s60)
    t4.to_csv(OUT / "table4_equity.csv", index=False)
    print(f"CHE40cap concentration index (rank=cons_pc): {ci_val:.4f}; Erreygers index: {erg_val:.4f}")

    # Table 5: drivers (two-part model + SHAP)
    t5 = build_table5(s60)
    t5.to_csv(OUT / "table5_drivers.csv", index=False)
    print(f"Two-part + SHAP drivers table written (SHAP model AUC = {t5.attrs.get('auc', float('nan')):.3f})")

    # Table 6: microsimulation scenarios
    t6 = build_table6(s60, line, P)
    t6.to_csv(OUT / "table6_microsim.csv", index=False)
    s4 = t6.loc[t6["scenario"].str.startswith("S4"), ["che40cap_delta", "fiscal_cost"]].iloc[0]
    print(f"S4 combined scenario: che40cap_delta={s4['che40cap_delta']:.2f} pp, "
          f"fiscal_cost=Rs {s4['fiscal_cost'] / 1e7:,.0f} cr")

    # Table: informal caregiving valuation
    tcare = build_table_caregiving(s60, P)
    tcare.to_csv(OUT / "table_caregiving.csv", index=False)
    natval = tcare["national_annual_value"].iloc[0]
    print(f"National informal-care value (60+): Rs {natval / 1e7:,.0f} cr "
          f"(recipients={tcare['recipients_pct'].iloc[0]:.1f}%, "
          f"mean hours/week={tcare['mean_hours_week'].iloc[0]:.1f})")

    print("All 7 tables written to", OUT.resolve())


if __name__ == "__main__":
    main()
