"""
Head-to-head: does a correctly-referenced low-FVC identify older Indians with
concurrent frailty/disability better than the GLI-labelled PRISm?

Cross-sectional (LASI Wave 1), so this is CONCURRENT identification/discrimination,
not prognosis. We compare spirometric flags on how many they flag, the risk among
those flagged, and the adjusted association with ageing outcomes.

Flags compared:
  GLI-PRISm (fixed)          : GLI-2012 ratio>=70 & FEV1 <80% pred   (the literature label)
  GLI-RSP (fixed)            : GLI-2012 ratio>=70 & FVC  <80% pred
  National low-FVC (LLN)     : FVC z < -1.645 under the national LASI reference
  National low-FVC (fixed)   : FVC <80% of national-reference median
Outcomes (not respiratory): frailty, functional limitation, low grip, multimorbidity, poor SRH.
"""
import json
import os
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.metrics import roc_auc_score

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

coef = pd.read_csv(COEF)


def cf(sex, param, model, term):
    m = coef[(coef.sex == sex) & (coef.param == param) & (coef.model == model) & (coef.term == term)]
    return float(m["coef"].iloc[0]) if len(m) else 0.0


def nat_fvc(d):
    """National-reference FVC median (M) and z per participant."""
    M = np.full(len(d), np.nan); z = np.full(len(d), np.nan)
    for sex in ("M", "F"):
        m = (d["sexlab"] == sex).values
        age_c = (d.loc[m, "r1agey"] - 60) / 10.0
        mu = (cf(sex, "FVC", "median(mu)", "Intercept") +
              cf(sex, "FVC", "median(mu)", "lnht") * np.log(d.loc[m, "height_cm"]) +
              cf(sex, "FVC", "median(mu)", "age_c") * age_c +
              cf(sex, "FVC", "median(mu)", "age_c2") * age_c ** 2)
        sig = (cf(sex, "FVC", "scatter(|resid|)", "Intercept") +
               cf(sex, "FVC", "scatter(|resid|)", "age_c") * age_c) / SQRT_2_PI
        M[m] = np.exp(mu)
        z[m] = (np.log(d.loc[m, "fvc"]) - mu) / sig
    return M, z


# ---- load ----
df = pd.read_csv(DATA)
bm = pd.read_stata(BM, columns=["prim_key", "bm067"])
df["prim_key"] = df["prim_key"].astype(str); bm["prim_key"] = bm["prim_key"].astype(str)
df = df.merge(bm, on="prim_key", how="left").rename(columns={"bm067": "height_cm"})
d = df[(df["acceptable"] == 1) & (df["r1agey"] >= 45) & df["height_cm"].between(120, 210) &
       df["fev1"].notna() & df["fvc"].notna() & df["fev1fvc"].between(20, 100) &
       df["pre_fev1_gli"].between(10, 200) & df["pre_fvc_gli"].between(10, 200)].copy()
d["sexlab"] = np.where(d["ragender"] == 1, "M", "F")
d["w"] = d["statespiroweight"].clip(lower=0).fillna(0)
natM, natZ = nat_fvc(d)
d["nat_fvc_pct"] = 100 * d["fvc"] / natM
d["nat_fvc_z"] = natZ

# ---- flags ----
pres = d["fev1fvc"] >= 70
d["gli_prism"] = (pres & (d["pre_fev1_gli"] < 80)).astype(int)
d["gli_rsp"] = (pres & (d["pre_fvc_gli"] < 80)).astype(int)
d["nat_lowfvc_lln"] = (d["nat_fvc_z"] < -1.645).astype(int)
d["nat_lowfvc_fixed"] = (d["nat_fvc_pct"] < 80).astype(int)
FLAGS = {"GLI-PRISm (fixed)": "gli_prism", "GLI-RSP (fixed)": "gli_rsp",
         "National low-FVC (LLN)": "nat_lowfvc_lln", "National low-FVC (fixed)": "nat_lowfvc_fixed"}

# ---- outcomes ----
d["low_grip"] = np.where(d["ragender"] == 2, d["r1gripsum"] < 18, d["r1gripsum"] < 28).astype(float)
d["poor_srh"] = d["r1shlt"].isin([4, 5]).astype(float)
OUTC = {"frail_binary": "Frailty", "functional_limitation": "Functional limitation",
        "low_grip": "Low grip", "multimorbidity_ge2": "Multimorbidity", "poor_srh": "Poor SRH"}

# covariates for adjustment
d["age_c"] = (d["r1agey"] - 60) / 10
d["Women"] = (d["ragender"] == 2).astype(int)
d["Rural"] = (d["hh1rural"] == 1).astype(int)
d["current_smoke"] = (d["r1smoken"] == 1).astype(int)
d["no_school"] = (d["raeduc_l"] == 0).astype(int)
ADJ = ["age_c", "Women", "Rural", "current_smoke", "no_school"]


def wmean(ind, w):
    ind = np.asarray(ind, float); w = np.asarray(w, float)
    ok = ~np.isnan(ind) & ~np.isnan(w)
    return 100 * np.average(ind[ok], weights=w[ok])


# ---- coverage (weighted % flagged) ----
cover = {name: round(wmean(d[col], d["w"]), 1) for name, col in FLAGS.items()}

# ---- per flag x outcome: risk among flagged/unflagged, adjusted OR, sensitivity/PPV, AUC ----
rows = []
for name, col in FLAGS.items():
    for oc, olab in OUTC.items():
        s = d.dropna(subset=[oc, col] + ADJ).copy()
        y = s[oc].astype(int); f = s[col].astype(int); w = s["w"]
        risk_flag = wmean(y[f == 1], w[f == 1])
        risk_unflag = wmean(y[f == 0], w[f == 0])
        # adjusted OR
        X = sm.add_constant(s[[col] + ADJ].astype(float))
        m = sm.Logit(y, X).fit(disp=0)
        beta = m.params[col]; ci = m.conf_int().loc[col]
        OR = np.exp(beta); lo, hi = np.exp(ci[0]), np.exp(ci[1])
        # unweighted sensitivity / PPV (identification framing)
        tp = int(((f == 1) & (y == 1)).sum()); fp = int(((f == 1) & (y == 0)).sum())
        fn = int(((f == 0) & (y == 1)).sum())
        sens = 100 * tp / (tp + fn) if (tp + fn) else np.nan
        ppv = 100 * tp / (tp + fp) if (tp + fp) else np.nan
        # AUC added by flag over covariates
        base = sm.Logit(y, sm.add_constant(s[ADJ].astype(float))).fit(disp=0)
        auc_base = roc_auc_score(y, base.predict(sm.add_constant(s[ADJ].astype(float))))
        auc_full = roc_auc_score(y, m.predict(X))
        rows.append(dict(flag=name, outcome=olab,
                         risk_flagged=round(risk_flag, 1), risk_unflagged=round(risk_unflag, 1),
                         risk_ratio=round(risk_flag / risk_unflag, 2) if risk_unflag else np.nan,
                         adj_OR=round(OR, 2), lo=round(lo, 2), hi=round(hi, 2),
                         sensitivity=round(sens, 1), ppv=round(ppv, 1),
                         dAUC=round(auc_full - auc_base, 4)))
res = pd.DataFrame(rows)
res.to_csv(os.path.join(OUTT, "headtohead.csv"), index=False)

# summary: mean adjusted OR and mean risk-among-flagged per flag
summ = res.groupby("flag").agg(coverage=("flag", lambda s: cover[s.iloc[0]]),
                               mean_adjOR=("adj_OR", "mean"),
                               mean_risk_flagged=("risk_flagged", "mean"),
                               mean_ppv=("ppv", "mean")).round(2)
summ.to_csv(os.path.join(OUTT, "flag_summary.csv"))

key = dict(n=int(len(d)), coverage=cover,
           summary=summ.reset_index().to_dict("records"))
json.dump(key, open(os.path.join(OUT, "key_numbers.json"), "w"), indent=2)
d[["w"] + list(FLAGS.values()) + list(OUTC)].to_csv(os.path.join(OUT, "flagged.csv"), index=False)

print(json.dumps(key, indent=2))
print("\n== Head-to-head (flag x outcome) ==")
print(res.to_string(index=False))
