"""IJMR extension analytics for the elderly health-economics paper.

Produces the additional tables/figures requested for the IJMR version:
  - state/UT catastrophic-spending ranking
  - policy-scenario cost-effectiveness ranking
  - catastrophic spending by per-capita-consumption quintile
  - caregiving-value sensitivity to the assumed care-worker wage
  - demographic projection of the catastrophic-spending caseload and the
    outpatient-cover fiscal cost to 2036 and 2050 (rates held at 2017-18)

Reuses the tested functions in src/health_economics.py. Run from repo root:
    python scripts/run_health_economics_ijmr_extras.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.health_economics import (load_economics_frame, che_indicators, add_che_flags,
    compute_care_hours_week, informal_care_value)

SAV = "data/raw/g2aging_harmonized_lasi_a3_sav/H_LASI_a3.sav"
PROC = "data/processed/analysis_dataset.csv"
OUT = Path("outputs/health_economics_mjdrdypu/tables"); OUT.mkdir(parents=True, exist_ok=True)
CARE_COLS = ["prim_key","r1rcany","r1rscaredpm_l","r1rscarehr_l","r1rccaredpm_l","r1rccarehr_l",
             "r1rrcaredpm_l","r1rrcarehr_l","r1rfcaredpm_l","r1rfcarehr_l"]

STATE_NAMES = {1:"Jammu & Kashmir",2:"Himachal Pradesh",3:"Punjab",4:"Chandigarh",5:"Uttarakhand",
    6:"Haryana",7:"Delhi",8:"Rajasthan",9:"Uttar Pradesh",10:"Bihar",11:"Sikkim",12:"Arunachal Pradesh",
    13:"Nagaland",14:"Manipur",15:"Mizoram",16:"Tripura",17:"Meghalaya",18:"Assam",19:"West Bengal",
    20:"Jharkhand",21:"Odisha",22:"Chhattisgarh",23:"Madhya Pradesh",24:"Gujarat",25:"Daman & Diu",
    26:"Dadra & Nagar Haveli",27:"Maharashtra",28:"Andhra Pradesh",29:"Karnataka",30:"Goa",
    31:"Lakshadweep",32:"Kerala",33:"Tamil Nadu",34:"Puducherry",35:"Andaman & Nicobar",36:"Telangana"}

# India Ageing Report 2023 (UNFPA/IIPS) 60+ population projections
POP_60 = {2022: 149e6, 2036: 227e6, 2050: 347e6}


def params():
    p = pd.read_csv("data/external/health_economics_params.csv")
    return dict(zip(p["parameter"], pd.to_numeric(p["value"], errors="coerce")))


def weighted_quintiles(values, w, q=5):
    v = pd.to_numeric(values, errors="coerce")
    wn = pd.to_numeric(w, errors="coerce").fillna(0)
    order = np.argsort(v.values)
    vv, ww = v.values[order], wn.values[order]
    cw = np.cumsum(ww) / ww.sum()
    edges = np.searchsorted(cw, np.linspace(1/q, 1, q, endpoint=True))
    grp = np.empty(len(v), dtype=float); grp[:] = np.nan
    bins = np.zeros(len(vv), dtype=int)
    cuts = [np.interp(k/q, cw, vv) for k in range(1, q)]
    return pd.cut(v, [-np.inf] + cuts + [np.inf], labels=list(range(1, q+1)))


def main():
    import pyreadstat
    df = load_economics_frame(SAV, PROC)
    care, _ = pyreadstat.read_sav(SAV, usecols=CARE_COLS)
    care["prim_key"] = pd.to_numeric(care["prim_key"], errors="coerce").astype("Int64")
    df = df.merge(care, on="prim_key", how="left")
    df["care_hours_week"] = compute_care_hours_week(df)
    df = add_che_flags(df)
    s = df[pd.to_numeric(df["age_years"], errors="coerce") >= 60].copy()
    P = params()

    # --- 1. State/UT CHE ranking (n >= 150) ---
    rows = []
    for code, sub in s.groupby("state_code"):
        if len(sub) >= 150:
            r = che_indicators(sub)
            rows.append({"state": STATE_NAMES.get(int(code), f"code{int(code)}"),
                         "n": len(sub), "che40cap": round(r["che40cap"], 1),
                         "che10": round(r["che10"], 1)})
    state = pd.DataFrame(rows).sort_values("che40cap", ascending=False).reset_index(drop=True)
    state.to_csv(OUT / "table_state_che.csv", index=False)
    print("State CHE40 range: %.1f%% (%s) to %.1f%% (%s)" % (
        state.iloc[0]["che40cap"], state.iloc[0]["state"],
        state.iloc[-1]["che40cap"], state.iloc[-1]["state"]))

    # --- 2. Scenario cost-effectiveness ranking ---
    t6 = pd.read_csv(OUT / "table6_microsim.csv")
    t6["che40_pp_per_lakh_cr"] = (-t6["che40cap_delta"]) / (t6["fiscal_cost"] / 1e12)
    t6["che10_pp_per_lakh_cr"] = (-t6["che10_delta"]) / (t6["fiscal_cost"] / 1e12)
    ce = t6[["scenario", "che40cap_delta", "che10_delta", "fiscal_cost",
             "che40_pp_per_lakh_cr", "che10_pp_per_lakh_cr"]].copy()
    ce["fiscal_cost_cr"] = (ce["fiscal_cost"] / 1e7).round(0)
    ce = ce.sort_values("che40_pp_per_lakh_cr", ascending=False)
    ce.round(2).to_csv(OUT / "table_cost_effectiveness.csv", index=False)
    print("Most cost-effective (CHE40 pp / lakh-cr): %s = %.1f" % (
        ce.iloc[0]["scenario"][:30], ce.iloc[0]["che40_pp_per_lakh_cr"]))

    # --- 3. CHE by per-capita-consumption quintile ---
    s = s.dropna(subset=["cons_pc", "r1wtresp"]).copy()
    s["pc_quintile"] = weighted_quintiles(s["cons_pc"], s["r1wtresp"])
    qrows = []
    for qv, sub in s.groupby("pc_quintile", observed=True):
        r = che_indicators(sub)
        qrows.append({"consumption_quintile": int(qv), "n": len(sub),
                      "che40cap": round(r["che40cap"], 1), "che10": round(r["che10"], 1)})
    quint = pd.DataFrame(qrows).sort_values("consumption_quintile")
    quint.to_csv(OUT / "table_quintile_che.csv", index=False)
    print("CHE40 poorest vs richest quintile: %.1f%% vs %.1f%%" % (
        quint.iloc[0]["che40cap"], quint.iloc[-1]["che40cap"]))

    # --- 4. Caregiving value sensitivity to wage ---
    wages = [50, 75, P["care_worker_wage_hour"], 150, 200]
    crows = []
    for wage in wages:
        v = informal_care_value(s, needs_help_col="r1rcany", hours_week_col="care_hours_week",
                                wage_hour=wage, pop_scale=P["pop_60plus_india"])
        crows.append({"wage_per_hour": round(wage, 1),
                      "value_per_recipient": round(v["annual_value_per_recipient"], 0),
                      "national_value_cr": round(v["national_annual_value"] / 1e7, 0)})
    pd.DataFrame(crows).to_csv(OUT / "table_caregiving_sensitivity.csv", index=False)

    # --- 5. Demographic projection (rates held at 2017-18) ---
    base = che_indicators(s)
    che40_rate = base["che40cap"] / 100.0
    s2_cost_per_capita = float(t6[t6["scenario"].str.startswith("S2")]["fiscal_cost"].iloc[0]) / POP_60[2022]
    prows = []
    for yr in (2022, 2036, 2050):
        pop = POP_60[yr]
        prows.append({"year": yr, "pop_60plus_million": round(pop / 1e6, 0),
                      "che40_caseload_million": round(che40_rate * pop / 1e6, 1),
                      "outpatient_cover_cost_lakh_cr": round(s2_cost_per_capita * pop / 1e12, 2)})
    proj = pd.DataFrame(prows)
    proj.to_csv(OUT / "table_projections.csv", index=False)
    print("Projected CHE40 caseload: %.0fM (2022) -> %.0fM (2050)" % (
        proj.iloc[0]["che40_caseload_million"], proj.iloc[-1]["che40_caseload_million"]))
    print("All IJMR-extra tables written to", OUT)


if __name__ == "__main__":
    main()
