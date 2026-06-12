"""
01_build_dataset.py
Assemble the analytic dataset for the India Biological Age Gap study (Discover Aging).

Inputs (all REAL LASI Wave 1, 2017-18):
  - data/processed/biomarker_integrated_analysis_dataset.csv  (linked DBS+spirometry+harmonized)
  - data/raw/g2aging_harmonized_lasi_a3_sav/H_LASI_a3.sav     (measured BP, pulse, waist)
  - data_raw/iips_extracted/3_LASI_W1_Individual_v4.sav        (hospitalisation, falls)

Output:
  - biological_age_gap_2026/outputs/analytic_dataset.parquet
  - biological_age_gap_2026/outputs/tables/t_included_vs_excluded.csv
"""
import os, numpy as np, pandas as pd, pyreadstat

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROC = os.path.join(ROOT, "data", "processed", "biomarker_integrated_analysis_dataset.csv")
HARM = os.path.join(ROOT, "data", "raw", "g2aging_harmonized_lasi_a3_sav", "H_LASI_a3.sav")
IND  = os.path.join(ROOT, "..", "data_raw", "iips_extracted", "3_LASI_W1_Individual_v4.sav")
OUT  = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(os.path.join(OUT, "tables"), exist_ok=True)

def winsorize(s, lo=0.001, hi=0.999):
    ql, qh = s.quantile(lo), s.quantile(hi)
    return s.clip(ql, qh)

print("Loading processed linked dataset ...")
df = pd.read_csv(PROC, low_memory=False, dtype={"prim_key": str})
df["prim_key"] = df["prim_key"].str.strip()
print("  processed:", df.shape)

print("Merging measured BP / pulse / waist from harmonized A.3 ...")
harm, _ = pyreadstat.read_sav(HARM, usecols=["prim_key", "r1systo", "r1diasto", "r1pulse", "r1mwaist"])
harm["prim_key"] = harm["prim_key"].astype(str).str.strip()
df = df.merge(harm, on="prim_key", how="left")
print("  BP merge match:", df["r1systo"].notna().sum(), "/", len(df))

print("Merging hospitalisation / falls from IIPS Individual v4 ...")
ind, _ = pyreadstat.read_sav(IND, usecols=["prim_key", "hc202", "hc203", "ht103"])
ind["prim_key"] = ind["prim_key"].astype(str).str.strip()
df = df.merge(ind, on="prim_key", how="left")
print("  hosp merge match:", df["hc202"].notna().sum(), "/", len(df))

# ---- Restrict to analytic population: adults 45+ (LASI design age) ----
df = df[df["age_years"] >= 45].copy()
print("  adults 45+:", df.shape)

# ---- External outcomes (NOT used in the biological-age clock) ----
df["hospitalised_12m"] = np.where(df["hc202"].notna(), (df["hc202"] >= 1).astype(float), np.nan)
df["fall_2yr"] = np.where(df["ht103"].isin([1, 2]), (df["ht103"] == 1).astype(float), np.nan)
df["poor_srh"] = df.get("deficit_poor_self_rated_health")
# adl_limitation, iadl_limitation, frail_binary, multimorbidity_ge2 already present

# ---- Biomarker panel for KDM (measured, multi-system; raw scales) ----
df["sbp"]   = winsorize(df["r1systo"])
df["pulse"] = winsorize(df["r1pulse"])
df["waist"] = winsorize(df["r1mwaist"])
df["fev1_raw"] = winsorize(df["fev1"])           # litres, declines with age
df["grip"]  = winsorize(df["r1gripsum"])
df["hb_v"]  = winsorize(df["hb"])
df["hba1c_v"] = winsorize(df["hba1c"])
df["logcrp"] = df["log_crp"]                      # already log; winsorized below
df["logcrp"] = winsorize(df["logcrp"])

BIOMARKERS = ["logcrp", "hba1c_v", "hb_v", "sbp", "pulse", "fev1_raw", "grip", "waist"]

# how many biomarkers available per person
df["n_biomarkers"] = df[BIOMARKERS].notna().sum(axis=1)

# ---- Exposome / social predictors (PREDICTORS of biological ageing; never in clock) ----
# already present: unclean_cooking_fuel, indoor_pollution, unimproved_sanitation,
# unimproved_drinking_water, current_smoking, current_smokeless_tobacco, poverty,
# education_years, sex, residence, r1caste, hh1itot

# ---- Save analytic file ----
keep = list(dict.fromkeys([
    "prim_key", "age_years", "sex", "residence", "state_code", "state_name",
    "person_weight", "dbs_weight", "spiro_weight", "ssuid",
    *BIOMARKERS, "n_biomarkers",
    # raw biomarker source for reference
    "crp", "hba1c", "hb", "fev1", "fvc", "r1gripsum", "r1mwaist", "r1systo", "r1diasto", "r1pulse",
    "spirometry_qc_usable_acceptable", "low_fvc_z", "fvc_z_qc",
    # outcomes
    "hospitalised_12m", "fall_2yr", "poor_srh", "adl_limitation", "iadl_limitation",
    "frail_binary", "frailty_index", "multimorbidity_ge2", "chronic_condition_count",
    # self-reported diagnoses for "hidden ageing"
    "chronic_diabetes", "chronic_hypertension", "diabetes_hba1c_ge65",
    "elevated_crp_gt3", "anaemia",
    # exposome / social
    "unclean_cooking_fuel", "indoor_pollution", "unimproved_sanitation",
    "unimproved_drinking_water", "current_smoking", "ever_smoking",
    "current_smokeless_tobacco", "poverty", "education_years", "raedyrs",
    "r1caste", "hh1itot", "literacy",
]))
keep = [c for c in keep if c in df.columns]
adf = df[keep].copy()

outpath = os.path.join(OUT, "analytic_dataset.parquet")
adf.to_parquet(outpath, index=False)
print("Saved", outpath, adf.shape)

# ---- Included vs excluded comparison (selection-bias transparency; R2.3) ----
# "Included" = has >=5 of 8 biomarkers (clock-eligible); compare to excluded on key vars.
adf["clock_eligible"] = (adf["n_biomarkers"] >= 5).astype(int)
compare_vars = ["age_years", "education_years", "frailty_index", "multimorbidity_ge2",
                "poor_srh", "adl_limitation", "poverty", "current_smoking",
                "unclean_cooking_fuel"]
rows = []
for v in compare_vars:
    if v not in adf.columns:
        continue
    g = adf.groupby("clock_eligible")[v]
    inc = g.get_group(1) if 1 in adf["clock_eligible"].values else pd.Series(dtype=float)
    exc = g.get_group(0) if 0 in adf["clock_eligible"].values else pd.Series(dtype=float)
    rows.append({
        "variable": v,
        "included_mean": np.nanmean(inc), "included_n": inc.notna().sum(),
        "excluded_mean": np.nanmean(exc), "excluded_n": exc.notna().sum(),
        "abs_diff": np.nanmean(inc) - np.nanmean(exc),
    })
cmp = pd.DataFrame(rows)
cmp.to_csv(os.path.join(OUT, "tables", "t_included_vs_excluded.csv"), index=False)
print("\nIncluded vs excluded (clock-eligible >=5 biomarkers):")
print(cmp.to_string(index=False))

# ---- quick biomarker availability + sex coding sanity ----
print("\nClock-eligible n:", int(adf["clock_eligible"].sum()), "of", len(adf))
print("sex values:", adf["sex"].value_counts(dropna=False).to_dict())
print("Biomarker availability:")
for b in BIOMARKERS:
    print(f"  {b:10s} n={adf[b].notna().sum():6d}")
