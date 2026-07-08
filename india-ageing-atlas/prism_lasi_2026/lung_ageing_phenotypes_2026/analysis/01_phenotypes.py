"""
Data-driven lung-ageing phenotypes in middle-aged and older Indians (LASI Wave 1).

We cluster adults on a physiological-reserve feature set that combines nationally
referenced lung function with metabolic and inflammatory biomarkers and grip
strength, then test whether the resulting phenotypes differ in ageing OUTCOMES
that were NOT used to build them (frailty, disability, multimorbidity, poor
self-rated health) — an external-validation design that avoids circularity.

Clustering features (standardized): FVC z, FEV1/FVC z (national LASI reference,
this programme), BMI, HbA1c, log-CRP, haemoglobin, grip strength.
Method: k-means; k chosen by silhouette over k = 2..6; seed fixed.
Exploratory and hypothesis-generating.
"""
import json
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

SEED = 42
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
BASE = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "data", "processed", "biomarker_integrated_analysis_dataset.csv")
BM = os.path.join(ROOT, "data", "raw", "g2aging_lasi_w1b_stata", "LASI_w1b_Stata", "lasi_w1b_ind_bm.dta")
COEF = os.path.join(BASE, "national_ref_equations_2026", "outputs", "tables", "reference_coefficients.csv")
OUT = os.path.abspath(os.path.join(HERE, "..", "outputs"))
OUTT = os.path.join(OUT, "tables")
os.makedirs(OUTT, exist_ok=True)
SQRT_2_PI = np.sqrt(2 / np.pi)

# ---- national LASI reference z-scores (from paper 2 coefficients) ----
coef = pd.read_csv(COEF)


def cf(sex, param, model, term):
    m = coef[(coef.sex == sex) & (coef.param == param) & (coef.model == model) & (coef.term == term)]
    return float(m["coef"].iloc[0]) if len(m) else 0.0


def z_national(d, param, col, scale):
    """Return z-scores under the national LASI reference for one parameter."""
    z = np.full(len(d), np.nan)
    for sex in ("M", "F"):
        m = d["sexlab"] == sex
        age_c = (d.loc[m, "r1agey"] - 60) / 10.0
        mu = cf(sex, param, "median(mu)", "Intercept") + \
            cf(sex, param, "median(mu)", "age_c") * age_c + \
            cf(sex, param, "median(mu)", "age_c2") * age_c ** 2
        if scale == "log":
            mu = mu + cf(sex, param, "median(mu)", "lnht") * np.log(d.loc[m, "height_cm"])
        sig = (cf(sex, param, "scatter(|resid|)", "Intercept") +
               cf(sex, param, "scatter(|resid|)", "age_c") * age_c) / SQRT_2_PI
        y = d.loc[m, col]
        z[m.values] = ((np.log(y) - mu) / sig) if scale == "log" else ((y - mu) / sig)
    return z


# ---- load ----
df = pd.read_csv(DATA)
bm = pd.read_stata(BM, columns=["prim_key", "bm067"])
df["prim_key"] = df["prim_key"].astype(str); bm["prim_key"] = bm["prim_key"].astype(str)
df = df.merge(bm, on="prim_key", how="left").rename(columns={"bm067": "height_cm"})
d = df[(df["acceptable"] == 1) & (df["r1agey"] >= 45) & df["height_cm"].between(120, 210) &
       df["fev1"].notna() & df["fvc"].notna() & df["fev1fvc"].between(20, 100)].copy()
d["sexlab"] = np.where(d["ragender"] == 1, "M", "F")
d["FVC_z"] = z_national(d, "FVC", "fvc", "log")
d["FEV1FVC_z"] = z_national(d, "FEV1FVC", "fev1fvc", "lin")

# ---- feature set (physiological reserve; outcomes excluded) ----
feats = ["FVC_z", "FEV1FVC_z", "bmi", "hba1c", "log_crp", "hb", "r1gripsum"]
cl = d.dropna(subset=feats).copy()
X = StandardScaler().fit_transform(cl[feats].astype(float))

# ---- choose k by silhouette ----
sil = {}
for k in range(2, 7):
    km = KMeans(n_clusters=k, random_state=SEED, n_init=10).fit(X)
    sil[k] = round(float(silhouette_score(X, km.labels_, sample_size=8000, random_state=SEED)), 4)
best_k = max(sil, key=sil.get)
km = KMeans(n_clusters=best_k, random_state=SEED, n_init=10).fit(X)
cl["cluster"] = km.labels_
cl["w"] = cl["statespiroweight"].clip(lower=0).fillna(0)

# ---- characterise phenotypes (standardized feature means) ----
prof = cl.groupby("cluster")[feats].mean().round(2)
prof_z = ((prof - cl[feats].mean()) / cl[feats].std()).round(2)   # standardized profile
size = cl.groupby("cluster").size()
wshare = cl.groupby("cluster")["w"].sum() / cl["w"].sum()
prof.insert(0, "n", size)
prof.insert(1, "weighted_share_pct", (wshare * 100).round(1))
prof.to_csv(os.path.join(OUTT, "phenotype_profiles.csv"))
prof_z.to_csv(os.path.join(OUTT, "phenotype_profiles_standardized.csv"))

# ---- external validation: outcomes NOT used in clustering ----
outcomes = {"frail_binary": "Frailty", "functional_limitation": "Functional limitation",
            "multimorbidity_ge2": "Multimorbidity", "poor_srh": "Poor self-rated health"}
cl["poor_srh"] = cl["r1shlt"].isin([4, 5]).astype(float)


def wmean(ind, w):
    ind = np.asarray(ind, float); w = np.asarray(w, float)
    ok = ~np.isnan(ind) & ~np.isnan(w)
    return round(100 * np.average(ind[ok], weights=w[ok]), 1)


ext = []
for c, g in cl.groupby("cluster"):
    row = {"cluster": int(c), "n": len(g)}
    for oc, lab in outcomes.items():
        row[lab] = wmean(g[oc], g["w"])
    row["mean_age"] = round(g["r1agey"].mean(), 1)
    row["pct_women"] = round((g["ragender"] == 2).mean() * 100, 1)
    ext.append(row)
ext_df = pd.DataFrame(ext)
ext_df.to_csv(os.path.join(OUTT, "phenotype_outcomes.csv"), index=False)

key = dict(n_clustered=int(len(cl)), features=feats, silhouette=sil, best_k=int(best_k),
           weighted_share=wshare.round(3).to_dict())
json.dump(key, open(os.path.join(OUT, "key_numbers.json"), "w"), indent=2)

# persist for figure
cl[["cluster", "w"] + feats + list(outcomes) + ["poor_srh", "r1agey", "ragender"]].to_csv(
    os.path.join(OUT, "clustered.csv"), index=False)

print(json.dumps(key, indent=2))
print("\n== Standardized phenotype profiles (feature z within analytic sample) ==")
print(prof_z.to_string())
print("\n== Phenotype profiles (raw means) ==")
print(prof.to_string())
print("\n== External outcomes by phenotype (weighted %) ==")
print(ext_df.to_string(index=False))
