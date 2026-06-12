"""
05_dual_burden_exposome.py
Disaggregate biological burden into two clinically coherent axes and model exposome
predictors per domain (avoids conflating opposing phenotypes — the key fix vs the old paper).

  Cardiometabolic EXCESS : dysglycaemia (HbA1c>=6.5), hypertension (SBP>=140), central obesity
  DEFICIT / inflammatory : anaemia, low grip (sex Q1), low lung reserve (FVC z<-1.64), CRP>3

Outputs:
  outputs/tables/t7_dual_burden_by_group.csv     domain prevalence by social stratum
  outputs/tables/t8_domain_predictors.csv         adjusted ORs per domain (exposome/social)
"""
import os, numpy as np, pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from util_survey import wmean

HERE = os.path.dirname(__file__); OUT = os.path.join(HERE, "..", "outputs")
T = os.path.join(OUT, "tables")
df = pd.read_parquet(os.path.join(OUT, "analytic_final.parquet"))
W = "person_weight"; df["clust"] = df["ssuid"].fillna(-1)

df["excess_burden"] = df[["ab_dysgly", "ab_htn", "ab_waist"]].sum(axis=1, skipna=True)
df.loc[df[["ab_dysgly", "ab_htn", "ab_waist"]].notna().sum(axis=1) < 2, "excess_burden"] = np.nan
df["deficit_burden"] = df[["ab_anaemia", "ab_grip", "ab_lung", "ab_inflam"]].sum(axis=1, skipna=True)
df.loc[df[["ab_anaemia", "ab_grip", "ab_lung", "ab_inflam"]].notna().sum(axis=1) < 2, "deficit_burden"] = np.nan
df["high_excess"] = (df["excess_burden"] >= 2).astype(float); df.loc[df["excess_burden"].isna(), "high_excess"] = np.nan
df["high_deficit"] = (df["deficit_burden"] >= 2).astype(float); df.loc[df["deficit_burden"].isna(), "high_deficit"] = np.nan

if "edu_grp" not in df:
    df["edu_grp"] = pd.cut(df["education_years"], [-1, 0, 5, 30], labels=["No education", "1-5 yr", "6+ yr"])
if "wealth_grp" not in df:
    df["wealth_grp"] = pd.qcut(df["hh1itot"].rank(method="first"), 3, labels=["Poorest", "Middle", "Richest"])

DOMAINS = {"Dysglycaemia": "ab_dysgly", "Hypertension(meas)": "ab_htn", "Central obesity": "ab_waist",
           "Anaemia": "ab_anaemia", "Low grip": "ab_grip", "Low lung reserve": "ab_lung",
           "Inflammation": "ab_inflam"}

# ---- Table 7: domain prevalence by social group (the dual-burden picture) ----
rows = []
for strat in ["residence", "edu_grp", "wealth_grp"]:
    for g, s in df.groupby(strat, observed=True):
        rec = {"stratum": strat, "group": str(g), "n": len(s)}
        for nm, col in DOMAINS.items():
            rec[nm] = round(100 * wmean(s[col], s[W]), 1)
        rows.append(rec)
t7 = pd.DataFrame(rows); t7.to_csv(os.path.join(T, "t7_dual_burden_by_group.csv"), index=False)
print("=== TABLE 7: Domain prevalence (%) by social group ===")
print(t7.to_string(index=False))

# ---- Table 8: adjusted predictors per domain ----
rhs = ("age_years + C(sex) + C(residence) + education_years + poverty + current_smoking + "
       "current_smokeless_tobacco + unclean_cooking_fuel + unimproved_drinking_water")
keep_terms = ["C(residence)[T.urban]", "education_years", "poverty", "current_smoking",
              "current_smokeless_tobacco", "unclean_cooking_fuel", "unimproved_drinking_water"]
rows = []
for nm, col in DOMAINS.items():
    d = df[[col, "age_years", "sex", "residence", "education_years", "poverty",
            "current_smoking", "current_smokeless_tobacco", "unclean_cooking_fuel",
            "unimproved_drinking_water", W, "clust"]].dropna()
    if d[col].nunique() < 2:
        continue
    m = smf.glm(f"{col} ~ {rhs}", data=d, family=sm.families.Binomial(),
                freq_weights=d[W]).fit(cov_type="cluster", cov_kwds={"groups": d["clust"]})
    for term in keep_terms:
        if term in m.params.index:
            ci = m.conf_int().loc[term]
            rows.append({"domain": nm, "predictor": term, "OR": round(np.exp(m.params[term]), 3),
                         "ci_lo": round(np.exp(ci[0]), 3), "ci_hi": round(np.exp(ci[1]), 3),
                         "p": m.pvalues[term]})
t8 = pd.DataFrame(rows); t8.to_csv(os.path.join(T, "t8_domain_predictors.csv"), index=False)
print("\n=== TABLE 8: Adjusted ORs per domain (key predictors) ===")
piv = t8.pivot(index="predictor", columns="domain", values="OR")
print(piv.to_string())

df.to_parquet(os.path.join(OUT, "analytic_final.parquet"), index=False)
print("\nUpdated analytic_final.parquet with excess/deficit burden axes")
