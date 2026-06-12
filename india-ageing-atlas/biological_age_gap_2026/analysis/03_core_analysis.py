"""
03_core_analysis.py  — core results for "The hidden burden of biological ageing in India".

Produces:
  outputs/tables/t1_diagnosis_gap.csv          headline undiagnosed-burden prevalences (wt + 95% CI)
  outputs/tables/t2_social_patterning.csv       diagnosis gap & burden by social strata
  outputs/tables/t3_incremental_value.csv        nested-model AUROC for hospitalisation
  outputs/tables/t4_looks_healthy.csv            hidden burden among the self-reported-healthy
  outputs/tables/t5_exposome_predictors.csv      adjusted predictors of subclinical biomarker burden
  outputs/analytic_final.parquet                 with subclinical_burden score
"""
import os, numpy as np, pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.metrics import roc_auc_score
from util_survey import wmean, cluster_bootstrap_ci, fmt_pct

HERE = os.path.dirname(__file__); OUT = os.path.join(HERE, "..", "outputs")
T = os.path.join(OUT, "tables"); os.makedirs(T, exist_ok=True)
df = pd.read_parquet(os.path.join(OUT, "analytic_with_bioage.parquet"))
W = "person_weight"; df[W] = df[W].fillna(df[W].median())
df["clust"] = df["ssuid"].fillna(-1)

# ---------------- Subclinical biomarker burden score (measured abnormalities) ----------------
df["ab_dysgly"]  = (df["hba1c"] >= 6.5).astype(float);            df.loc[df["hba1c"].isna(), "ab_dysgly"] = np.nan
df["measured_dbp"] = df["r1diasto"] if "r1diasto" in df else np.nan
df["ab_htn"]     = ((df["sbp"] >= 140) | (df["measured_dbp"] >= 90)).astype(float)
df.loc[df["sbp"].isna() & df["measured_dbp"].isna(), "ab_htn"] = np.nan
df["ab_anaemia"] = df["anaemia"].astype(float)
df["ab_inflam"]  = df["elevated_crp_gt3"].astype(float)
df["ab_lung"]    = df["low_fvc_z"].astype(float) if "low_fvc_z" in df.columns else np.nan
# low grip = sex-specific lowest quintile; central obesity = IDF Asian cutoffs
df["ab_grip"] = np.nan; df["ab_waist"] = np.nan
for sx, wcut in [("male", 90), ("female", 80)]:
    s = df[df["sex"] == sx]
    gthr = s["grip"].quantile(0.20)
    df.loc[s.index, "ab_grip"] = (s["grip"] <= gthr).astype(float)
    df.loc[s.index, "ab_waist"] = (s["waist"] >= wcut).astype(float)
    df.loc[s.index[s["grip"].isna()], "ab_grip"] = np.nan
    df.loc[s.index[s["waist"].isna()], "ab_waist"] = np.nan

AB = ["ab_dysgly", "ab_htn", "ab_anaemia", "ab_inflam", "ab_lung", "ab_grip", "ab_waist"]
df["n_ab_avail"] = df[AB].notna().sum(axis=1)
df["subclinical_burden"] = np.where(df["n_ab_avail"] >= 5, df[AB].sum(axis=1, skipna=True), np.nan)
df["high_burden"] = (df["subclinical_burden"] >= 3).astype(float)
df.loc[df["subclinical_burden"].isna(), "high_burden"] = np.nan

# ---------------- Table 1: diagnosis gap (headline) ----------------
df["undx_diab"] = np.where((df["hba1c"] >= 6.5), (df["chronic_diabetes"] == 0).astype(float), np.nan)
df["undx_htn"]  = np.where((df["ab_htn"] == 1),  (df["chronic_hypertension"] == 0).astype(float), np.nan)
df["biochem_diab"] = (df["hba1c"] >= 6.5).astype(float); df.loc[df["hba1c"].isna(), "biochem_diab"] = np.nan
df["measured_htn"] = df["ab_htn"]

rows = []
for name, col, sub in [
    ("Self-reported diabetes", "chronic_diabetes", None),
    ("Biochemical diabetes (HbA1c>=6.5)", "biochem_diab", None),
    ("Undiagnosed among biochemically diabetic", "undx_diab", df["biochem_diab"] == 1),
    ("Self-reported hypertension", "chronic_hypertension", None),
    ("Measured hypertension (>=140/90 mmHg)", "measured_htn", None),
    ("Undiagnosed among measured-hypertensive", "undx_htn", df["measured_htn"] == 1),
    ("Anaemia", "ab_anaemia", None),
    ("Elevated CRP (>3 mg/L)", "ab_inflam", None),
    ("Central obesity (IDF Asian)", "ab_waist", None),
    ("High subclinical burden (>=3 systems)", "high_burden", None),
]:
    p, lo, hi = cluster_bootstrap_ci(df, col, W, "clust", subset=sub, n_boot=400)
    n = int(df.loc[sub if sub is not None else slice(None), col].notna().sum())
    rows.append({"indicator": name, "weighted_pct_95CI": fmt_pct(p, lo, hi), "n": n})
t1 = pd.DataFrame(rows); t1.to_csv(os.path.join(T, "t1_diagnosis_gap.csv"), index=False)
print("=== TABLE 1: Diagnosis gap / hidden burden ===\n", t1.to_string(index=False))

# ---------------- Table 2: social patterning ----------------
df["edu_grp"] = pd.cut(df["education_years"], [-1, 0, 5, 30], labels=["No education", "1-5 yr", "6+ yr"])
df["wealth_grp"] = pd.qcut(df["hh1itot"].rank(method="first"), 3, labels=["Poorest", "Middle", "Richest"]) \
    if df["hh1itot"].notna().sum() > 100 else np.nan
rows = []
for strat in ["residence", "sex", "edu_grp", "wealth_grp"]:
    if strat not in df or df[strat].isna().all():
        continue
    for g, s in df.groupby(strat, observed=True):
        u_d, _, _ = cluster_bootstrap_ci(df.loc[s.index], "undx_diab", W, "clust", n_boot=200)
        u_h, _, _ = cluster_bootstrap_ci(df.loc[s.index], "undx_htn", W, "clust", n_boot=200)
        b, _, _ = cluster_bootstrap_ci(df.loc[s.index], "high_burden", W, "clust", n_boot=200)
        rows.append({"stratum": strat, "group": str(g),
                     "undx_diabetes_pct": round(100 * u_d, 1),
                     "undx_htn_pct": round(100 * u_h, 1),
                     "high_burden_pct": round(100 * b, 1)})
t2 = pd.DataFrame(rows); t2.to_csv(os.path.join(T, "t2_social_patterning.csv"), index=False)
print("\n=== TABLE 2: Social patterning ===\n", t2.to_string(index=False))

# ---------------- Table 3: incremental value for HOSPITALISATION ----------------
def auc_ci(y, p, n_boot=300, seed=1):
    rng = np.random.default_rng(seed); a = roc_auc_score(y, p); est = []
    y = np.asarray(y); p = np.asarray(p)
    for _ in range(n_boot):
        idx = rng.integers(0, len(y), len(y))
        if len(np.unique(y[idx])) < 2: continue
        est.append(roc_auc_score(y[idx], p[idx]))
    return a, np.percentile(est, 2.5), np.percentile(est, 97.5)

models = {
    "M1 age+sex": "age_years + C(sex)",
    "M2 +social/behaviour (simple indicators)": "age_years + C(sex) + C(residence) + education_years + poverty + current_smoking + unclean_cooking_fuel",
    "M3 +self-reported disease": "age_years + C(sex) + C(residence) + education_years + poverty + current_smoking + unclean_cooking_fuel + chronic_condition_count",
    "M4 +measured biomarker burden": "age_years + C(sex) + C(residence) + education_years + poverty + current_smoking + unclean_cooking_fuel + chronic_condition_count + subclinical_burden",
}
rows = []
for outcome in ["hospitalised_12m"]:
    base = df[["clust", W, outcome, "age_years", "sex", "residence", "education_years",
               "poverty", "current_smoking", "unclean_cooking_fuel",
               "chronic_condition_count", "subclinical_burden"]].dropna()
    for name, rhs in models.items():
        m = smf.glm(f"{outcome} ~ {rhs}", data=base, family=sm.families.Binomial(),
                    freq_weights=base[W]).fit(cov_type="cluster",
                                              cov_kwds={"groups": base["clust"]})
        pred = m.predict(base)
        a, lo, hi = auc_ci(base[outcome], pred)
        rows.append({"outcome": outcome, "model": name, "n": len(base),
                     "AUROC_95CI": f"{a:.3f} ({lo:.3f}-{hi:.3f})", "AIC": round(m.aic, 1)})
t3 = pd.DataFrame(rows); t3.to_csv(os.path.join(T, "t3_incremental_value.csv"), index=False)
print("\n=== TABLE 3: Incremental value (hospitalisation) ===\n", t3.to_string(index=False))

# ---------------- Table 4: hidden burden among the self-reported-healthy ----------------
healthy = df[df["chronic_condition_count"] == 0]
rows = []
hp, hlo, hhi = cluster_bootstrap_ci(healthy, "high_burden", W, "clust", n_boot=400)
rows.append({"group": "Self-reported healthy (0 diagnosed conditions)",
             "high_burden_pct_95CI": fmt_pct(hp, hlo, hhi),
             "n": int(healthy["high_burden"].notna().sum())})
# does hidden burden predict hospitalisation AMONG the self-reported-healthy?
hh = healthy[["hospitalised_12m", "subclinical_burden", "age_years", "sex", W, "clust"]].dropna()
if hh["hospitalised_12m"].nunique() == 2:
    m = smf.glm("hospitalised_12m ~ subclinical_burden + age_years + C(sex)", data=hh,
                family=sm.families.Binomial(), freq_weights=hh[W]).fit(
                cov_type="cluster", cov_kwds={"groups": hh["clust"]})
    orr = np.exp(m.params["subclinical_burden"]); ci = np.exp(m.conf_int().loc["subclinical_burden"])
    rows.append({"group": "OR hospitalisation per +1 burden (healthy-looking)",
                 "high_burden_pct_95CI": f"OR={orr:.2f} ({ci[0]:.2f}-{ci[1]:.2f}); p={m.pvalues['subclinical_burden']:.1e}",
                 "n": len(hh)})
t4 = pd.DataFrame(rows); t4.to_csv(os.path.join(T, "t4_looks_healthy.csv"), index=False)
print("\n=== TABLE 4: Hidden burden among self-reported healthy ===\n", t4.to_string(index=False))

# ---------------- Table 5: exposome/social predictors of subclinical burden ----------------
bs = df[["subclinical_burden", "age_years", "sex", "residence", "education_years", "poverty",
         "current_smoking", "current_smokeless_tobacco", "unclean_cooking_fuel",
         "unimproved_sanitation", "unimproved_drinking_water", W, "clust"]].dropna()
m = smf.glm("subclinical_burden ~ age_years + C(sex) + C(residence) + education_years + poverty + "
            "current_smoking + current_smokeless_tobacco + unclean_cooking_fuel + "
            "unimproved_sanitation + unimproved_drinking_water",
            data=bs, family=sm.families.Poisson(), freq_weights=bs[W]).fit(
            cov_type="cluster", cov_kwds={"groups": bs["clust"]})
t5 = pd.DataFrame({"term": m.params.index, "IRR": np.exp(m.params.values),
                   "ci_lo": np.exp(m.conf_int()[0].values), "ci_hi": np.exp(m.conf_int()[1].values),
                   "p": m.pvalues.values})
t5.to_csv(os.path.join(T, "t5_exposome_predictors.csv"), index=False)
print("\n=== TABLE 5: Predictors of subclinical biomarker burden (IRR) ===\n",
      t5.round(3).to_string(index=False))

df.to_parquet(os.path.join(OUT, "analytic_final.parquet"), index=False)
print("\nSaved analytic_final.parquet", df.shape)
