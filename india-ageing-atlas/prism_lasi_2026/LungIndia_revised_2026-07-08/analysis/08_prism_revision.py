"""
PRISm / RSP in LASI Wave 1 -- Lung India revision (v2) analysis.

Addresses reviewer comments with real re-analysis:
  * STROBE participant flow with spirometry-acceptability exclusions
  * Included-vs-excluded comparison (selection bias) with standardized differences
  * Co-primary classification: GLI fixed cut-offs AND GLI lower limit of normal (LLN)
  * Reference-equation comparison: GLI-2012 vs Chhabra-2014 North-India equations
    (+ an internal, population-derived healthy-subset reference as robustness)
  * Quality-grade (acceptability/repeatability) summary

Data integrity note enforced here: `fev1_z` and `fev1fvc_z` are DEAD columns
(all zeros) in the linked file and are NEVER used. LLN is computed from the
`fev1_lln` / `fvc_lln` / `fev1fvc_lln` columns; `fvc_z` is valid and used only
for the z-distribution figure.

Run from anywhere: paths are resolved relative to this file.
"""
import json
import os
import numpy as np
import pandas as pd
import statsmodels.api as sm
from pyspiro import GLI_2012, BOWERMAN_2022, CHHABRA_2014, AGARWAL_2020

HERE = os.path.dirname(os.path.abspath(__file__))
# .../prism_lasi_2026/LungIndia_revised_2026-07-08/analysis -> india-ageing-atlas
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DATA = os.path.join(ROOT, "data", "processed", "biomarker_integrated_analysis_dataset.csv")
BM = os.path.join(ROOT, "data", "raw", "g2aging_lasi_w1b_stata",
                  "LASI_w1b_Stata", "lasi_w1b_ind_bm.dta")
OUT = os.path.abspath(os.path.join(HERE, "..", "outputs"))
OUTT = os.path.join(OUT, "tables")
os.makedirs(OUTT, exist_ok=True)

# Chhabra SK et al. 2014 (Indian J Chest Dis Allied Sci 2014;56:221-9),
# North-India prediction equations. Age in years, ht in cm, wt in kg; output L.
# SEE used for LLN = predicted - 1.645*SEE.
CHHABRA = {
    # sex code: 1=male, 2=female  (LASI ragender)
    1: dict(
        fvc=lambda a, h, w: -5.048 - 0.014 * a + 0.054 * h + 0.006 * w,
        fev1=lambda a, h, w: -3.682 - 0.024 * a + 0.046 * h,
        see_fvc=0.479, see_fev1=0.402),
    2: dict(
        fvc=lambda a, h, w: 20.07 - 0.010 * a - 0.261 * h + 0.000972 * h * h,
        fev1=lambda a, h, w: -2.267 - 0.019 * a + 0.033 * h,
        see_fvc=0.315, see_fev1=0.286),
}


def wprev_ci(ind, w):
    """Weighted prevalence with Kish effective-N Wilson CI (%)."""
    ind = np.asarray(ind, float)
    w = np.asarray(w, float)
    ok = ~np.isnan(ind) & ~np.isnan(w)
    ind, w = ind[ok], w[ok]
    if w.sum() == 0:
        return np.nan, np.nan, np.nan, 0
    p = np.average(ind, weights=w)
    neff = (w.sum() ** 2) / np.sum(w ** 2)
    z = 1.96
    den = 1 + z ** 2 / neff
    c = (p + z ** 2 / (2 * neff)) / den
    h = (z * np.sqrt(p * (1 - p) / neff + z ** 2 / (4 * neff ** 2))) / den
    return 100 * p, 100 * (c - h), 100 * (c + h), neff


def fmt(p, lo, hi):
    return f"{p:.1f} ({lo:.1f}-{hi:.1f})"


def std_diff(a, b):
    """Standardized difference between two groups for a binary/continuous var."""
    a = np.asarray(a, float); a = a[~np.isnan(a)]
    b = np.asarray(b, float); b = b[~np.isnan(b)]
    m1, m2 = a.mean(), b.mean()
    s1, s2 = a.var(ddof=1), b.var(ddof=1)
    pooled = np.sqrt((s1 + s2) / 2)
    return (m1 - m2) / pooled if pooled > 0 else 0.0, m1, m2


# ---------------------------------------------------------------- load + link
df = pd.read_csv(DATA)
n_lasi_45 = int((df["r1agey"] >= 45).sum())

bm = pd.read_stata(BM, columns=["prim_key", "bm067"])
df["prim_key"] = df["prim_key"].astype(str)
bm["prim_key"] = bm["prim_key"].astype(str)
df = df.merge(bm, on="prim_key", how="left")
df.rename(columns={"bm067": "height_cm"}, inplace=True)

# ---------------------------------------------------------------- STROBE flow
attempted = df["acceptable"].notna()           # spirometry attempted (graded)
n_attempted = int(attempted.sum())
n_not_attempted = n_lasi_45 - n_attempted
n_unacceptable = int((df["acceptable"] == 0).sum())
n_acceptable = int((df["acceptable"] == 1).sum())

d = df[(df["acceptable"] == 1) & (df["r1agey"] >= 45)].copy()
n_acc_age = len(d)
# plausibility
val_ok = (d["fev1fvc"].between(20, 100, inclusive="right") &
          d["pre_fev1_gli"].between(10, 200) &
          d["pre_fvc_gli"].between(10, 200) &
          d["fev1"].notna() & d["fvc"].notna())
n_val_drop = int((~val_ok).sum())
d = d[val_ok].copy()
ht_ok = d["height_cm"].between(120, 210)
n_ht_drop = int((~ht_ok).sum())
d = d[ht_ok].copy()
n_analytic = len(d)

# ---------------------------------------------------------------- derived vars
d["w"] = d["statespiroweight"].clip(lower=0).fillna(0)
d["weight_kg"] = d["bmi"] * (d["height_cm"] / 100.0) ** 2
d["sex_lab"] = np.where(d["ragender"] == 2, "Women", "Men")
d["agegrp"] = pd.cut(d["r1agey"], [44, 59, 69, 200], labels=["45-59", "60-69", "70+"])
d["residence"] = np.where(d["hh1rural"] == 1, "Rural", "Urban")

# ---- Chhabra predicted, %pred, LLN ----
def chhabra_pred(row, param):
    c = CHHABRA[int(row["ragender"])]
    return c[param](row["r1agey"], row["height_cm"], row["weight_kg"])

d["ch_fvc_pred"] = d.apply(lambda r: chhabra_pred(r, "fvc"), axis=1)
d["ch_fev1_pred"] = d.apply(lambda r: chhabra_pred(r, "fev1"), axis=1)
d["ch_fvc_pct"] = 100 * d["fvc"] / d["ch_fvc_pred"]
d["ch_fev1_pct"] = 100 * d["fev1"] / d["ch_fev1_pred"]
d["ch_fvc_lln"] = d["ch_fvc_pred"] - 1.645 * d["ragender"].map(
    {1: CHHABRA[1]["see_fvc"], 2: CHHABRA[2]["see_fvc"]})
d["ch_fev1_lln"] = d["ch_fev1_pred"] - 1.645 * d["ragender"].map(
    {1: CHHABRA[1]["see_fev1"], 2: CHHABRA[2]["see_fev1"]})

# ---------------------------------------------------------------- classifiers
# obstruction is ratio-based (least reference-sensitive) -> fixed 70 or LLN ratio
d["obstruct_fixed"] = d["fev1fvc"] < 70
d["obstruct_lln"] = d["fev1fvc"] < d["fev1fvc_lln"] * 100  # fev1fvc in %, lln as ratio
d["preserved_fixed"] = ~d["obstruct_fixed"]
d["preserved_lln"] = ~d["obstruct_lln"]

# scheme -> (prism indicator, rsp indicator) among *analytic sample*
schemes = {}
# GLI fixed
schemes["GLI-2012 fixed"] = (
    d["preserved_fixed"] & (d["pre_fev1_gli"] < 80),
    d["preserved_fixed"] & (d["pre_fvc_gli"] < 80),
    d["obstruct_fixed"])
# GLI LLN
schemes["GLI-2012 LLN"] = (
    d["preserved_lln"] & (d["fev1"] < d["fev1_lln"]),
    d["preserved_lln"] & (d["fvc"] < d["fvc_lln"]),
    d["obstruct_lln"])
# Chhabra fixed (%pred<80), obstruction by fixed ratio
schemes["Chhabra-2014 fixed"] = (
    d["preserved_fixed"] & (d["ch_fev1_pct"] < 80),
    d["preserved_fixed"] & (d["ch_fvc_pct"] < 80),
    d["obstruct_fixed"])
# Chhabra LLN
schemes["Chhabra-2014 LLN"] = (
    d["preserved_fixed"] & (d["fev1"] < d["ch_fev1_lln"]),
    d["preserved_fixed"] & (d["fvc"] < d["ch_fvc_lln"]),
    d["obstruct_fixed"])

ref_rows = []
for name, (prism, rsp, obstr) in schemes.items():
    pp = wprev_ci(prism, d["w"])
    pr = wprev_ci(rsp, d["w"])
    po = wprev_ci(obstr, d["w"])
    ref_rows.append(dict(scheme=name,
                         PRISm=fmt(*pp[:3]), PRISm_pct=round(pp[0], 1),
                         RSP=fmt(*pr[:3]), RSP_pct=round(pr[0], 1),
                         Obstruction=fmt(*po[:3]), Obstruction_pct=round(po[0], 1)))
# ---- pyspiro cross-validated references: GLI-Global (Bowerman 2022), Agarwal 2020 ----
# pyspiro is validated on this dataset: its GLI-2012 South-East Asian module
# reproduces the released LASI GLI values to <0.01 L, and its CHHABRA_2014
# reproduces our hand-coded Chhabra to 0.0001 L (see analysis log).
d["ps_sex"] = (d["ragender"] == 1).astype(int)   # pyspiro: 1=male, 0=female


def ps_metrics(eq, param, value_col, needs_weight=False, eth=None):
    kw = dict(sex_col="ps_sex", age_col="r1agey", height_col="height_cm",
              value_col=value_col, metrics=("percent", "lln"))
    if needs_weight:
        kw["weight_col"] = "weight_kg"
    if eth is not None:
        d["_eth"] = eth
        kw["ethnicity_col"] = "_eth"
    r = eq.compute(d, param, **kw)
    return pd.to_numeric(r["percent"], errors="coerce"), pd.to_numeric(r["lln"], errors="coerce")


def ref_indicators(pct_fev1, lln_fev1, pct_fvc, lln_fvc):
    pres = (d["fev1fvc"] >= 70).to_numpy()
    fev1 = d["fev1"].to_numpy(float); fvc = d["fvc"].to_numpy(float)

    def mk(mask_ok, cond):
        return np.where(mask_ok, np.where(pres & cond, 1.0, 0.0), np.nan)
    prism_fx = mk(pct_fev1.notna().to_numpy(), pct_fev1.to_numpy() < 80)
    rsp_fx = mk(pct_fvc.notna().to_numpy(), pct_fvc.to_numpy() < 80)
    prism_ln = mk(lln_fev1.notna().to_numpy(), fev1 < lln_fev1.to_numpy())
    rsp_ln = mk(lln_fvc.notna().to_numpy(), fvc < lln_fvc.to_numpy())
    return prism_fx, rsp_fx, prism_ln, rsp_ln


ps_refs = [
    ("GLI-Global 2022 (race-neutral)", BOWERMAN_2022(), BOWERMAN_2022.Parameters, False, None),
    ("Agarwal-2020 (India)", AGARWAL_2020(), AGARWAL_2020.Parameters, False, None),
]
for label, eq, P, nw, eth in ps_refs:
    pf1, lf1 = ps_metrics(eq, P.FEV1, "fev1", nw, eth)
    pfv, lfv = ps_metrics(eq, P.FVC, "fvc", nw, eth)
    prism_fx, rsp_fx, prism_ln, rsp_ln = ref_indicators(pf1, lf1, pfv, lfv)
    for suffix, prism, rsp in [("fixed", prism_fx, rsp_fx), ("LLN", prism_ln, rsp_ln)]:
        pp = wprev_ci(prism, d["w"]); pr = wprev_ci(rsp, d["w"])
        ref_rows.append(dict(scheme=f"{label} {suffix}",
                             PRISm=fmt(*pp[:3]), PRISm_pct=round(pp[0], 1),
                             RSP=fmt(*pr[:3]), RSP_pct=round(pr[0], 1),
                             Obstruction="", Obstruction_pct=np.nan))

ref_df = pd.DataFrame(ref_rows)
ref_df.to_csv(os.path.join(OUTT, "t_reference_comparison.csv"), index=False)

# ---- internal population-derived reference (healthy-subset), robustness ----
healthy = d[(d["r1smokev"] != 1) & (d["chronic_lung_disease"] != 1) &
            (d["chronic_asthma"] != 1) & (d["bmi"].between(18.5, 24.99))].copy()
n_healthy = len(healthy)
internal_rows = []
for sex in (1, 2):
    hs = healthy[healthy["ragender"] == sex]
    Xh = sm.add_constant(hs[["r1agey", "height_cm"]].astype(float))
    for param, col in [("fvc", "fvc"), ("fev1", "fev1")]:
        m = sm.OLS(hs[col].astype(float), Xh).fit()
        rmse = np.sqrt(np.mean(m.resid ** 2))
        internal_rows.append(dict(sex=sex, param=param,
                                  const=m.params["const"], b_age=m.params["r1agey"],
                                  b_ht=m.params["height_cm"], rmse=rmse, n=len(hs)))
internal = pd.DataFrame(internal_rows)
internal.to_csv(os.path.join(OUTT, "t_internal_ref_coefs.csv"), index=False)


def internal_pred(row, param):
    r = internal[(internal["sex"] == int(row["ragender"])) & (internal["param"] == param)].iloc[0]
    return r["const"] + r["b_age"] * row["r1agey"] + r["b_ht"] * row["height_cm"], r["rmse"]


d["in_fvc_pred"], d["in_fvc_rmse"] = zip(*d.apply(lambda r: internal_pred(r, "fvc"), axis=1))
d["in_fev1_pred"], d["in_fev1_rmse"] = zip(*d.apply(lambda r: internal_pred(r, "fev1"), axis=1))
in_prism = d["preserved_fixed"] & (d["fev1"] < d["in_fev1_pred"] - 1.645 * d["in_fev1_rmse"])
in_rsp = d["preserved_fixed"] & (d["fvc"] < d["in_fvc_pred"] - 1.645 * d["in_fvc_rmse"])
ip = wprev_ci(in_prism, d["w"]); ir = wprev_ci(in_rsp, d["w"])
internal_prev = dict(scheme="Internal healthy-subset LLN", n_healthy=n_healthy,
                     PRISm=fmt(*ip[:3]), RSP=fmt(*ir[:3]))

# ---------------------------------------------------------------- included vs excluded
inc = df[(df["acceptable"] == 1) & (df["r1agey"] >= 45)]
exc = df[(df["acceptable"] == 0) & (df["r1agey"] >= 45)]
ie_vars = [("r1agey", "Age (years), mean"),
           ("Women", "Women"), ("frail_binary", "Frailty"),
           ("functional_limitation", "Functional limitation"),
           ("multimorbidity_ge2", "Multimorbidity (>=2)"),
           ("chronic_diabetes", "Diabetes"),
           ("chronic_lung_disease", "Chronic lung disease"),
           ("Rural", "Rural residence")]
tmp_inc = inc.assign(Women=(inc["ragender"] == 2).astype(float),
                     Rural=(inc["hh1rural"] == 1).astype(float))
tmp_exc = exc.assign(Women=(exc["ragender"] == 2).astype(float),
                     Rural=(exc["hh1rural"] == 1).astype(float))
ie_rows = []
for v, lab in ie_vars:
    if v not in tmp_inc:
        continue
    dstd, m_inc, m_exc = std_diff(tmp_inc[v], tmp_exc[v])
    scale = 1 if v == "r1agey" else 100
    ie_rows.append(dict(variable=lab,
                        included=round(m_inc * scale, 1),
                        excluded=round(m_exc * scale, 1),
                        std_diff=round(dstd, 3)))
ie_df = pd.DataFrame(ie_rows)
ie_df["n_included"] = len(inc)
ie_df["n_excluded"] = len(exc)
ie_df.to_csv(os.path.join(OUTT, "t_included_vs_excluded.csv"), index=False)

# ---------------------------------------------------------------- QC grades
qc = dict(attempted=n_attempted,
          acceptable=n_acceptable,
          unacceptable=n_unacceptable,
          repeatable=int((df["repeatable"] == 1).sum()),
          not_repeatable=int((df["repeatable"] == 0).sum()),
          acceptable_and_repeatable=int(((df["acceptable"] == 1) & (df["repeatable"] == 1)).sum()))

# ---------------------------------------------------------------- co-primary subgroup prevalence (PRISm)
d["prism_fixed"] = schemes["GLI-2012 fixed"][0].astype(int)
d["prism_lln"] = schemes["GLI-2012 LLN"][0].astype(int)
d["rsp_fixed"] = schemes["GLI-2012 fixed"][1].astype(int)
sub_rows = []
groups = [("All", d)]
for c in ["sex_lab", "agegrp", "residence"]:
    for val, g in d.groupby(c, observed=True):
        groups.append((f"{c}={val}", g))
for label, g in groups:
    pf = wprev_ci(g["prism_fixed"], g["w"])
    pl = wprev_ci(g["prism_lln"], g["w"])
    sub_rows.append(dict(subgroup=label, n=len(g),
                         prism_fixed=fmt(*pf[:3]), prism_lln=fmt(*pl[:3])))
sub_df = pd.DataFrame(sub_rows)
sub_df.to_csv(os.path.join(OUTT, "t_prism_subgroups_coprimary.csv"), index=False)

# ---------------------------------------------------------------- determinants + ageing (GLI-fixed primary)
d["category"] = np.where(d["obstruct_fixed"], "Obstructive",
                         np.where(d["pre_fev1_gli"] < 80, "PRISm", "Normal"))
d["underweight"] = (d["bmi"] < 18.5).astype(int)
d["obese"] = (d["bmi"] >= 25).astype(int)
d["current_smoke"] = (d["r1smoken"] == 1).astype(int)
d["diabetes"] = (d["chronic_diabetes"] == 1).astype(int)
d["no_school"] = (d["raeduc_l"] == 0).astype(int)
d["Women"] = (d["ragender"] == 2).astype(int)
d["Rural"] = (d["hh1rural"] == 1).astype(int)
d["unclean_fuel"] = (d["hh1clncook"] == 0).astype(int) if "hh1clncook" in d else np.nan
d["age_c"] = (d["r1agey"] - 60) / 10
preds = ["age_c", "Women", "Rural", "underweight", "obese", "current_smoke",
         "unclean_fuel", "diabetes", "no_school"]
md = d.dropna(subset=preds).copy()
md["y"] = md["category"].map({"Normal": 0, "PRISm": 1, "Obstructive": 2})
Xd = sm.add_constant(md[preds].astype(float))
mnl = sm.MNLogit(md["y"], Xd).fit(disp=0)
det_rows = []
for col, oname in [(0, "PRISm"), (1, "Obstructive")]:
    for pn in preds:
        b = mnl.params.loc[pn, col]; se = mnl.bse.loc[pn, col]
        det_rows.append(dict(outcome=oname, predictor=pn, OR=round(np.exp(b), 2),
                             lo=round(np.exp(b - 1.96 * se), 2),
                             hi=round(np.exp(b + 1.96 * se), 2)))
pd.DataFrame(det_rows).to_csv(os.path.join(OUTT, "t_determinants.csv"), index=False)

d["low_grip"] = np.where(d["ragender"] == 2, d["r1gripsum"] < 18, d["r1gripsum"] < 28).astype(float)
d["poor_srh"] = d["r1shlt"].isin([4, 5]).astype(int)
base = d[d["category"].isin(["Normal", "PRISm"])].copy()
base["prism01"] = (base["category"] == "PRISm").astype(int)
adj = ["age_c", "Women", "Rural", "current_smoke", "no_school"]
assoc_rows = []
for outc in ["frail_binary", "functional_limitation", "multimorbidity_ge2", "low_grip", "poor_srh"]:
    s = base.dropna(subset=[outc, "prism01"] + adj)
    Xo = sm.add_constant(s[["prism01"] + adj].astype(float))
    m = sm.Logit(s[outc].astype(int), Xo).fit(disp=0)
    b = m.params["prism01"]; ci = m.conf_int().loc["prism01"]
    assoc_rows.append(dict(outcome=outc, OR=round(np.exp(b), 2),
                           lo=round(np.exp(ci[0]), 2), hi=round(np.exp(ci[1]), 2)))
pd.DataFrame(assoc_rows).to_csv(os.path.join(OUTT, "t_ageing_assoc.csv"), index=False)

# overlap of PRISm with RSP (GLI fixed)
overlap = float((d.loc[d["prism_fixed"] == 1, "rsp_fixed"] == 1).mean() * 100)

# ---------------------------------------------------------------- key numbers
key = dict(
    n_lasi_45=n_lasi_45, n_attempted=n_attempted, n_not_attempted=n_not_attempted,
    n_unacceptable=n_unacceptable, n_acceptable=n_acceptable,
    n_val_drop=n_val_drop, n_ht_drop=n_ht_drop, n_analytic=n_analytic,
    median_age=float(d["r1agey"].median()),
    pct_women=round(float((d["ragender"] == 2).mean() * 100), 1),
    qc=qc,
    reference_comparison=ref_rows,
    internal_reference=internal_prev,
    prism_rsp_overlap_pct=round(overlap, 1),
    median_fvc_z=round(float(np.nanmedian(d["fvc_z"])), 2),
    n_model=int(len(md)),
)
with open(os.path.join(OUT, "key_numbers_v2.json"), "w") as f:
    json.dump(key, f, indent=2)

print(json.dumps(key, indent=2))
print("\n== Reference comparison ==\n", ref_df.to_string(index=False))
print("\n== Included vs excluded ==\n", ie_df.to_string(index=False))
print("\n== PRISm subgroups (co-primary) ==\n", sub_df.to_string(index=False))
print("\n== Determinants ==\n", pd.DataFrame(det_rows).to_string(index=False))
print("\n== Ageing assoc ==\n", pd.DataFrame(assoc_rows).to_string(index=False))
