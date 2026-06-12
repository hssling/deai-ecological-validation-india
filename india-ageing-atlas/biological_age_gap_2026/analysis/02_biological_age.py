"""
02_biological_age.py
Compute biological age and biological age acceleration (BAA) from measured biomarkers only.

Primary measure : KDM biological age (Klemera-Doubal Method), faithful port of the
                  BioAge R package (Kwon & Belsky 2021, GeroScience), sex-specific,
                  survey-weighted training regressions.
Triangulation   : Mahalanobis physiological dysregulation (Cohen et al.);
                  allostatic-load count (high-risk quartile tally).

Outputs:
  outputs/analytic_with_bioage.parquet
  outputs/tables/t_kdm_training_params.csv
  outputs/tables/t_biomarker_age_assoc.csv
"""
import os, numpy as np, pandas as pd
import statsmodels.api as sm
from scipy.spatial.distance import mahalanobis

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "outputs")
os.makedirs(os.path.join(OUT, "tables"), exist_ok=True)

df = pd.read_parquet(os.path.join(OUT, "analytic_dataset.parquet"))
BIO = ["logcrp", "hba1c_v", "hb_v", "sbp", "pulse", "fev1_raw", "grip", "waist"]

# weight for biomarker training: prefer biomarker (DBS) weight, fall back to person weight
df["w"] = df["dbs_weight"].fillna(df["person_weight"])
df["w"] = df["w"].fillna(df["w"].median())

# ---------- diagnostics: weighted biomarker-age association ----------
diag = []
for b in BIO:
    s = df[["age_years", b, "w"]].dropna()
    X = sm.add_constant(s["age_years"])
    m = sm.WLS(s[b], X, weights=s["w"]).fit()
    diag.append({"biomarker": b, "slope_per_yr": m.params["age_years"],
                 "p": m.pvalues["age_years"], "r2": m.rsquared, "n": len(s)})
pd.DataFrame(diag).to_csv(os.path.join(OUT, "tables", "t_biomarker_age_assoc.csv"), index=False)
print("Biomarker-age associations:")
print(pd.DataFrame(diag).to_string(index=False))


# ---------- KDM (faithful BioAge port), sex-specific ----------
def kdm_train(d):
    """Return per-biomarker params q,k,s,r and characteristic s_r for a (sex) subset."""
    rows = []
    for b in BIO:
        s = d[["age_years", b, "w"]].dropna()
        X = sm.add_constant(s["age_years"])
        m = sm.WLS(s[b], X, weights=s["w"]).fit()
        resid_sd = np.sqrt(np.sum(m.resid ** 2 * s["w"]) / s["w"].sum())  # weighted RMSE
        rows.append({"bm": b, "q": m.params["const"], "k": m.params["age_years"],
                     "s": resid_sd, "r": m.rsquared})
    agev = pd.DataFrame(rows)
    agev["r1"] = np.abs((agev["k"] / agev["s"]) * np.sqrt(agev["r"]))
    agev["r2"] = np.abs(agev["k"] / agev["s"])
    agev["n2"] = (agev["k"] / agev["s"]) ** 2
    age_min, age_max = d["age_years"].min(), d["age_years"].max()
    rchar = agev["r1"].sum() / agev["r2"].sum()
    s_r = ((1 - rchar ** 2) / rchar ** 2) * (((age_max - age_min) ** 2) / (12 * len(agev)))
    return agev, s_r


def kdm_project(d, agev, s_r, s_ba2=None):
    obs = pd.DataFrame(index=d.index)
    for _, r in agev.iterrows():
        b = r["bm"]
        obs[b] = (d[b] - r["q"]) * (r["k"] / (r["s"] ** 2))
    nmiss = obs.isna().sum(axis=1)
    BAe_n = obs.sum(axis=1, skipna=True)
    BAe_d = agev["n2"].sum()
    BA_obs = len(BIO) - nmiss
    BA_eo = BAe_n / BAe_d
    BA_e = (BA_eo / BA_obs) * len(BIO)
    BA_CA = BA_e - d["age_years"]
    s2 = np.nanmean((BA_CA - np.nanmean(BA_CA)) ** 2)
    if s_ba2 is None:
        s_ba2 = s2 - s_r
    kdm = (BAe_n + d["age_years"] / s_ba2) / (BAe_d + 1 / s_ba2)
    kdm = kdm.where(nmiss <= 2, np.nan)   # require >=6 of 8 markers (BioAge rule)
    return kdm, s_ba2, s2, s_r


df["kdm_bioage"] = np.nan
train_records = []
for sx in ["male", "female"]:
    sub = df[df["sex"] == sx]
    agev, s_r = kdm_train(sub)
    kdm, s_ba2, s2, s_r = kdm_project(sub, agev, s_r)
    df.loc[sub.index, "kdm_bioage"] = kdm
    agev2 = agev.copy(); agev2["sex"] = sx; agev2["s_r"] = s_r; agev2["s_ba2"] = s_ba2
    train_records.append(agev2)
    print(f"\n[{sx}] s_r={s_r:.3f} s_ba2={s_ba2:.3f} n_kdm={kdm.notna().sum()}")

pd.concat(train_records).to_csv(os.path.join(OUT, "tables", "t_kdm_training_params.csv"), index=False)

# Biological age acceleration
df["baa"] = df["kdm_bioage"] - df["age_years"]
# age-residualized BAA (removes any residual age correlation) for robustness
v = df[["kdm_bioage", "age_years"]].dropna()
res = sm.OLS(v["kdm_bioage"], sm.add_constant(v["age_years"])).fit()
df.loc[v.index, "baa_resid"] = res.resid

print("\nKDM BioAge vs chronological age:")
ok = df[["kdm_bioage", "age_years", "baa"]].dropna()
print("  n           :", len(ok))
print("  corr(BA,CA) :", round(ok["kdm_bioage"].corr(ok["age_years"]), 3))
print("  BAA mean/sd :", round(ok["baa"].mean(), 2), "/", round(ok["baa"].std(), 2))


# ---------- Mahalanobis physiological dysregulation (Cohen) ----------
# reference = clock-eligible adults 45-54 without diagnosed chronic disease, sex-specific
df["mahalanobis_dr"] = np.nan
healthy_mask = (
    (df["age_years"].between(45, 54))
    & (df.get("chronic_diabetes", 0).fillna(0) == 0)
    & (df.get("chronic_hypertension", 0).fillna(0) == 0)
    & (df.get("multimorbidity_ge2", 0).fillna(0) == 0)
)
for sx in ["male", "female"]:
    ref = df[(df["sex"] == sx) & healthy_mask][BIO].dropna()
    mu = ref.mean().values
    cov = np.cov(ref.values, rowvar=False)
    cov_inv = np.linalg.pinv(cov)
    sub = df[df["sex"] == sx]
    full = sub[BIO].dropna()
    md = full.apply(lambda row: mahalanobis(row.values, mu, cov_inv), axis=1)
    df.loc[full.index, "mahalanobis_dr"] = np.log(md)   # log MD per Cohen
print("\nMahalanobis dysregulation n:", df["mahalanobis_dr"].notna().sum())

# ---------- Allostatic-load count (high-risk quartile tally, sex-specific) ----------
# direction: higher risk = elevated except hb/fev1/grip where LOW is risk
HIGH_BAD = ["logcrp", "hba1c_v", "sbp", "pulse", "waist"]
LOW_BAD  = ["hb_v", "fev1_raw", "grip"]
al = pd.Series(0.0, index=df.index)
aln = pd.Series(0.0, index=df.index)
for sx in ["male", "female"]:
    sub = df[df["sex"] == sx]
    for b in HIGH_BAD:
        thr = sub[b].quantile(0.75)
        hit = (sub[b] >= thr).astype(float); hit[sub[b].isna()] = np.nan
        al.loc[sub.index] = al.loc[sub.index].add(hit.fillna(0)); aln.loc[sub.index] += hit.notna().astype(float)
    for b in LOW_BAD:
        thr = sub[b].quantile(0.25)
        hit = (sub[b] <= thr).astype(float); hit[sub[b].isna()] = np.nan
        al.loc[sub.index] = al.loc[sub.index].add(hit.fillna(0)); aln.loc[sub.index] += hit.notna().astype(float)
df["allostatic_load"] = np.where(aln >= 6, al, np.nan)   # need >=6 markers
print("Allostatic load n:", df["allostatic_load"].notna().sum(),
      "mean:", round(np.nanmean(df["allostatic_load"]), 2))

# convergence of the three measures
conv = df[["baa", "mahalanobis_dr", "allostatic_load"]].dropna()
print("\nConvergent validity (Spearman):")
print(conv.corr(method="spearman").round(3).to_string())

df.to_parquet(os.path.join(OUT, "analytic_with_bioage.parquet"), index=False)
print("\nSaved analytic_with_bioage.parquet", df.shape)
