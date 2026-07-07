"""
National spirometry reference equations for middle-aged and older Indians (LASI Wave 1).

LMS-style derivation (L fixed by transform):
  FEV1, FVC  -> modelled on the LOG scale (equivalent to LMS with L=0), so the
               reference is log-normal: median M = exp(mu), z = (ln y - mu)/sigma,
               LLN(5th centile) = exp(mu - 1.645*sigma).
  FEV1/FVC   -> modelled on the natural scale (approximately symmetric).
Mean (mu) model: intercept + ln(height) + natural cubic spline in age (df=3).
Scatter (sigma) model: age-varying, from a smooth fit to |residual|
  (E|resid| = sigma*sqrt(2/pi) for a normal), giving heteroscedastic LLN.

Healthy reference population (GLI convention): acceptable spirometry, age 45-95,
never-smoker, no self-reported lung disease or asthma, plausible height; all body sizes.

Validation: 80/20 split; holdout mean z should be ~0 and SD ~1 overall and by age band.
"""
import json
import os
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

RNG = np.random.default_rng(42)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DATA = os.path.join(ROOT, "data", "processed", "biomarker_integrated_analysis_dataset.csv")
BM = os.path.join(ROOT, "data", "raw", "g2aging_lasi_w1b_stata",
                  "LASI_w1b_Stata", "lasi_w1b_ind_bm.dta")
OUT = os.path.abspath(os.path.join(HERE, "..", "outputs"))
OUTT = os.path.join(OUT, "tables")
os.makedirs(OUTT, exist_ok=True)
SQRT_2_PI = np.sqrt(2 / np.pi)

# ---------------------------------------------------------------- load + link
df = pd.read_csv(DATA)
bm = pd.read_stata(BM, columns=["prim_key", "bm067"])
df["prim_key"] = df["prim_key"].astype(str)
bm["prim_key"] = bm["prim_key"].astype(str)
df = df.merge(bm, on="prim_key", how="left").rename(columns={"bm067": "height_cm"})

analytic = df[(df["acceptable"] == 1) & (df["r1agey"].between(45, 95)) &
              df["height_cm"].between(120, 210) &
              df["fev1"].notna() & df["fvc"].notna() &
              df["fev1fvc"].between(20, 100)].copy()
analytic["male"] = (analytic["ragender"] == 1).astype(int)

healthy = analytic[(analytic["r1smokev"] != 1) &
                   (analytic["chronic_lung_disease"] != 1) &
                   (analytic["chronic_asthma"] != 1)].copy()

# ---------------------------------------------------------------- model fitting
# parameter -> (column, scale)  scale: "log" for volumes, "lin" for ratio
PARAMS = {"FEV1": ("fev1", "log"), "FVC": ("fvc", "log"), "FEV1FVC": ("fev1fvc", "lin")}


def fit_sex_param(train, col, scale):
    """Return dict with mean-model, scatter-model for one sex/parameter."""
    d = train.copy()
    if scale == "log":
        d["yv"] = np.log(d[col])
        mform = "yv ~ np.log(height_cm) + cr(r1agey, df=3)"
    else:
        d["yv"] = d[col]
        mform = "yv ~ cr(r1agey, df=3)"          # ratio ~ age only
    mM = smf.ols(mform, data=d).fit()
    d["resid"] = d["yv"] - mM.predict(d)
    d["absr"] = d["resid"].abs()
    mS = smf.ols("absr ~ cr(r1agey, df=3)", data=d).fit()
    return dict(mM=mM, mS=mS, scale=scale, col=col)


def predict_M_S(fit, data):
    """Return median M (natural scale) and sigma (on modelling scale)."""
    mu = fit["mM"].predict(data)
    sigma = (fit["mS"].predict(data) / SQRT_2_PI).clip(lower=1e-6)
    if fit["scale"] == "log":
        M = np.exp(mu)
    else:
        M = mu
    return mu, M, sigma


def zscore_lln(fit, data):
    mu, M, sigma = predict_M_S(fit, data)
    y = data[fit["col"]].to_numpy(float)
    if fit["scale"] == "log":
        z = (np.log(y) - mu) / sigma
        lln = np.exp(mu - 1.645 * sigma)
        pctpred = 100 * y / M
    else:
        z = (y - mu) / sigma
        lln = mu - 1.645 * sigma
        pctpred = 100 * y / M
    return z, lln, M, pctpred


# ---- split-sample validation (80/20 within healthy, per sex) ----
healthy = healthy.sample(frac=1.0, random_state=42).reset_index(drop=True)
val_rows = []
fits = {}                                   # (sex, param) -> fit on FULL healthy (for release)
for sex in (1, 0):
    hs = healthy[healthy["male"] == sex]
    ntr = int(0.8 * len(hs))
    train, hold = hs.iloc[:ntr], hs.iloc[ntr:]
    for pname, (col, scale) in PARAMS.items():
        f_tr = fit_sex_param(train, col, scale)
        z, _, _, _ = zscore_lln(f_tr, hold)
        z = z[np.isfinite(z)]
        holdband = hold.assign(_z=zscore_lln(f_tr, hold)[0])
        holdband["band"] = pd.cut(holdband["r1agey"], [44, 54, 64, 74, 95],
                                  labels=["45-54", "55-64", "65-74", "75+"])
        for b, g in holdband.groupby("band", observed=True):
            zz = g["_z"][np.isfinite(g["_z"])]
            val_rows.append(dict(sex="M" if sex else "F", param=pname, band=str(b),
                                 n=len(zz), mean_z=round(float(zz.mean()), 3),
                                 sd_z=round(float(zz.std()), 3)))
        val_rows.append(dict(sex="M" if sex else "F", param=pname, band="ALL",
                             n=len(z), mean_z=round(float(z.mean()), 3),
                             sd_z=round(float(z.std()), 3)))
        # release model refit on full healthy subset
        fits[(sex, pname)] = fit_sex_param(hs, col, scale)
val_df = pd.DataFrame(val_rows)
val_df.to_csv(os.path.join(OUTT, "validation_zscores.csv"), index=False)

# ---------------------------------------------------------------- apply LASI reference to full analytic sample
a = analytic.copy()
a["w"] = a["statespiroweight"].clip(lower=0).fillna(0)
for sex in (1, 0):
    idx = a["male"] == sex
    for pname in PARAMS:
        z, lln, M, pct = zscore_lln(fits[(sex, pname)], a[idx])
        a.loc[idx, f"{pname}_z"] = z
        a.loc[idx, f"{pname}_lln"] = lln
        a.loc[idx, f"{pname}_pct"] = pct

pres = a["FEV1FVC_z"] >= -1.645           # preserved ratio by LASI-reference LLN
a["obstruct"] = a["FEV1FVC_z"] < -1.645
# LLN-based
a["prism_lln"] = pres & (a["FEV1_z"] < -1.645)
a["rsp_lln"] = pres & (a["FVC_z"] < -1.645)
# fixed 80%%-pred based (under LASI reference median)
presf = a["fev1fvc"] >= 70
a["prism_fixed"] = presf & (a["FEV1_pct"] < 80)
a["rsp_fixed"] = presf & (a["FVC_pct"] < 80)


def wprev(ind):
    ind = np.asarray(ind, float)
    w = a["w"].to_numpy(float)
    ok = ~np.isnan(ind) & ~np.isnan(w)
    p = np.average(ind[ok], weights=w[ok])
    neff = (w[ok].sum() ** 2) / np.sum(w[ok] ** 2)
    z = 1.96
    den = 1 + z ** 2 / neff
    c = (p + z ** 2 / (2 * neff)) / den
    h = (z * np.sqrt(p * (1 - p) / neff + z ** 2 / (4 * neff ** 2))) / den
    return round(100 * p, 1), round(100 * (c - h), 1), round(100 * (c + h), 1)


burden = {
    "PRISm_LASI_fixed": wprev(a["prism_fixed"]),
    "PRISm_LASI_LLN": wprev(a["prism_lln"]),
    "RSP_LASI_fixed": wprev(a["rsp_fixed"]),
    "RSP_LASI_LLN": wprev(a["rsp_lln"]),
    "Obstruction_LASI_LLN": wprev(a["obstruct"]),
}

# ---------------------------------------------------------------- coefficient tables
coef_rows = []
for (sex, pname), f in fits.items():
    for term, val in f["mM"].params.items():
        coef_rows.append(dict(sex="M" if sex else "F", param=pname, model="median(mu)",
                              term=term, coef=round(float(val), 6)))
    for term, val in f["mS"].params.items():
        coef_rows.append(dict(sex="M" if sex else "F", param=pname, model="scatter(|resid|)",
                              term=term, coef=round(float(val), 6)))
pd.DataFrame(coef_rows).to_csv(os.path.join(OUTT, "reference_coefficients.csv"), index=False)

# ---------------------------------------------------------------- centile grid (for figures)
ref_ht = {1: float(healthy.loc[healthy["male"] == 1, "height_cm"].median()),
          0: float(healthy.loc[healthy["male"] == 0, "height_cm"].median())}
grid_rows = []
ages = np.arange(45, 91)
for sex in (1, 0):
    g = pd.DataFrame({"r1agey": ages, "height_cm": ref_ht[sex]})
    for pname in ("FEV1", "FVC"):
        mu, M, sigma = predict_M_S(fits[(sex, pname)], g)
        lln = np.exp(mu - 1.645 * sigma)
        for age, m, l in zip(ages, M, lln):
            grid_rows.append(dict(sex="M" if sex else "F", param=pname,
                                  ref_height=round(ref_ht[sex], 1), age=int(age),
                                  median=round(float(m), 3), lln=round(float(l), 3)))
pd.DataFrame(grid_rows).to_csv(os.path.join(OUTT, "centile_grid.csv"), index=False)

key = dict(
    n_analytic=int(len(a)), n_healthy=int(len(healthy)),
    ref_height_M=ref_ht[1], ref_height_F=ref_ht[0],
    n_healthy_M=int((healthy["male"] == 1).sum()),
    n_healthy_F=int((healthy["male"] == 0).sum()),
    burden=burden,
    validation_overall=val_df[val_df["band"] == "ALL"].to_dict("records"),
)
with open(os.path.join(OUT, "key_numbers.json"), "w") as fjson:
    json.dump(key, fjson, indent=2)

# persist scored analytic frame for the figure/burden script
a.to_parquet(os.path.join(OUT, "scored_analytic.parquet")) if False else \
    a[["r1agey", "male", "height_cm", "w", "fev1", "fvc", "fev1fvc",
       "FEV1_z", "FVC_z", "FEV1FVC_z", "FEV1_lln", "FVC_lln",
       "prism_lln", "rsp_lln", "obstruct"]].to_csv(
        os.path.join(OUT, "scored_analytic.csv"), index=False)

print(json.dumps(key, indent=2))
print("\n== Validation (ALL bands) ==")
print(val_df[val_df["band"] == "ALL"].to_string(index=False))
print("\n== Validation by age band ==")
print(val_df[val_df["band"] != "ALL"].to_string(index=False))
