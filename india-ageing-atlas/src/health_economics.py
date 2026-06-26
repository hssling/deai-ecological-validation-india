from __future__ import annotations

import numpy as np
import pandas as pd
import pyreadstat
import statsmodels.api as sm
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import cross_val_score
import shap

from .inequality import concentration_index


def deflate(series: pd.Series, cpi: dict[int, float], year: int, base: int = 2017) -> pd.Series:
    factor = cpi[year] / cpi[base]
    return pd.to_numeric(series, errors="coerce") / factor


ECON_VARS = ["prim_key","hhid","r1wtresp","r1agey","ragender","hh1rural","hh1state",
    "hh1cohc1m","hh1cihc1y","hh1ctot","hh1cfood1w","hh1cperc","hh1hhres","hh1poverty",
    "hh1ipubpen","hh1ipena","c2018cpindex","c2017cpindex"]

def load_economics_frame(sav_path: str, processed_csv: str) -> pd.DataFrame:
    raw, _ = pyreadstat.read_sav(sav_path, usecols=ECON_VARS)
    raw["prim_key"] = pd.to_numeric(raw["prim_key"], errors="coerce").astype("Int64")
    cpi = {2017: float(raw["c2017cpindex"].dropna().iloc[0]),
           2018: float(raw["c2018cpindex"].dropna().iloc[0])}
    for col in ["hh1cohc1m","hh1cihc1y","hh1ctot","hh1cfood1w","hh1cperc","hh1ipubpen","hh1ipena"]:
        raw[col] = deflate(raw[col], cpi, year=2018, base=2017)
    hosp = pd.to_numeric(raw["hh1cihc1y"], errors="coerce").clip(lower=0)            # household inpatient, annual
    out  = pd.to_numeric(raw["hh1cohc1m"], errors="coerce").clip(lower=0) * 12.0     # household outpatient, annualised
    cons = pd.to_numeric(raw["hh1ctot"], errors="coerce").clip(lower=0)
    food = pd.to_numeric(raw["hh1cfood1w"], errors="coerce").clip(lower=0) * 52.0    # annual food
    hhsize = pd.to_numeric(raw["hh1hhres"], errors="coerce")
    df = pd.DataFrame({
        "prim_key": raw["prim_key"],
        "r1wtresp": pd.to_numeric(raw["r1wtresp"], errors="coerce"),
        "oop_hosp": hosp, "oop_out": out, "oop_med": 0.0,
        "cons_total": cons,
        "cons_pc": pd.to_numeric(raw["hh1cperc"], errors="coerce").clip(lower=0),
        "hhsize": hhsize,
        "poverty_intl": pd.to_numeric(raw["hh1poverty"], errors="coerce"),
        "pub_pension": pd.to_numeric(raw["hh1ipubpen"], errors="coerce").clip(lower=0),
        "priv_pension": pd.to_numeric(raw["hh1ipena"], errors="coerce").clip(lower=0),
    })
    df["oop_total"] = df["oop_hosp"] + df["oop_out"] + df["oop_med"]
    df["oop_pc"] = df["oop_total"] / df["hhsize"].replace(0, np.nan)
    cap = cons - food                                   # WHO capacity-to-pay = non-food consumption
    df["cons_nonfood"] = cap.clip(lower=0)
    df["capacity_to_pay"] = cap.where(cap > 0, np.nan)
    df["any_pension"] = ((df["pub_pension"] > 0) | (df["priv_pension"] > 0)).astype(int)
    proc = pd.read_csv(processed_csv)
    proc["prim_key"] = pd.to_numeric(proc["prim_key"], errors="coerce").astype("Int64")
    keep = ["prim_key","age_years","sex","residence","state_code","living_alone",
            "multimorbidity_ge2","functional_limitation","education"]
    return df.merge(proc[[c for c in keep if c in proc.columns]], on="prim_key", how="inner")


def _wpct(mask, w):
    w = pd.to_numeric(w, errors="coerce").fillna(0)
    m = mask.astype(float)
    return float(100 * np.average(m, weights=w)) if w.sum() > 0 else np.nan


def che_indicators(df, oop="oop_total", cons="cons_total", cap="capacity_to_pay", weight="r1wtresp"):
    d = df.dropna(subset=[oop, cons, cap])
    share = d[oop] / d[cons].replace(0, np.nan)
    capsh = d[oop] / d[cap].replace(0, np.nan)
    w = d[weight]
    out = {}
    for tag, s, thr in [("10", share, .10), ("25", share, .25), ("40cap", capsh, .40)]:
        out[f"che{tag}"] = _wpct(s > thr, w)
        over = (s - thr).clip(lower=0)
        out[f"overshoot{tag}"] = float(100 * np.average(over.fillna(0), weights=pd.to_numeric(w, errors="coerce").fillna(0)))
    return out


def impoverishment(df, oop="oop_total", cons_pc="cons_pc", line=None, weight="r1wtresp"):
    d = df.dropna(subset=[cons_pc, oop])
    w = pd.to_numeric(d[weight], errors="coerce").fillna(1)
    pre = d[cons_pc]
    post = (d[cons_pc] - d[oop]).clip(lower=0)
    pre_poor = pre < line
    post_poor = post < line
    gap_pre = ((line - pre).clip(lower=0) / line)
    gap_post = ((line - post).clip(lower=0) / line)
    return {
        "pre_poverty": _wpct(pre_poor, w),
        "post_poverty": _wpct(post_poor, w),
        "impov_headcount": _wpct(post_poor & ~pre_poor, w),
        "poverty_gap_increase": float(100 * (np.average(gap_post, weights=w) - np.average(gap_pre, weights=w))),
    }


def erreygers_index(df, outcome, rank_var, weight=None, b=1.0, a=0.0):
    ci = concentration_index(df, outcome, rank_var, weight)
    y = pd.to_numeric(df[outcome], errors="coerce")
    if weight and weight in df.columns:
        w = pd.to_numeric(df[weight], errors="coerce").fillna(1)
        mu = float(np.average(y.fillna(0), weights=w))
    else:
        mu = float(y.mean())
    return float(4 * mu / (b - a) * ci)


def decompose_concentration(df, outcome, rank_var, regressors, weight=None):
    cols = [outcome, rank_var] + list(regressors) + ([weight] if weight and weight in df.columns else [])
    cols = list(dict.fromkeys(cols))  # de-dupe (rank_var may also appear in regressors)
    d = df[cols].dropna().copy()
    y = pd.to_numeric(d[outcome], errors="coerce")
    X = sm.add_constant(d[list(regressors)].apply(pd.to_numeric, errors="coerce"))
    if weight and weight in d.columns:
        w = pd.to_numeric(d[weight], errors="coerce").fillna(1)
    else:
        w = pd.Series(1.0, index=d.index)
    model = sm.WLS(y, X, weights=w).fit()
    ybar = float(np.average(y, weights=w))
    ci_y = concentration_index(d, outcome, rank_var, weight)
    rows = []
    for k in regressors:
        beta = float(model.params[k])
        xbar = float(np.average(pd.to_numeric(d[k], errors="coerce"), weights=w))
        elasticity = beta * xbar / ybar if ybar != 0 else np.nan
        if k == rank_var:
            # concentration_index needs distinct outcome/rank columns; alias when a
            # regressor is itself the rank variable.
            ci_x = concentration_index(d.assign(**{f"{k}__self": d[k]}), f"{k}__self", rank_var, weight)
        else:
            ci_x = concentration_index(d, k, rank_var, weight)
        contribution = elasticity * ci_x
        pct = 100 * contribution / ci_y if ci_y not in (0,) and not pd.isna(ci_y) else np.nan
        rows.append({"regressor": k, "elasticity": elasticity, "CI_regressor": ci_x,
                     "contribution": contribution, "pct_of_total": pct})
    return pd.DataFrame(rows)


INFORMAL_CARE_COLS = [
    ("r1rscaredpm_l","r1rscarehr_l"), ("r1rccaredpm_l","r1rccarehr_l"),
    ("r1rrcaredpm_l","r1rrcarehr_l"), ("r1rfcaredpm_l","r1rfcarehr_l"),
]

def compute_care_hours_week(df):
    total = pd.Series(0.0, index=df.index)
    for dpm, hr in INFORMAL_CARE_COLS:
        if dpm in df.columns and hr in df.columns:
            d = pd.to_numeric(df[dpm], errors="coerce").fillna(0).clip(lower=0)
            h = pd.to_numeric(df[hr], errors="coerce").fillna(0).clip(lower=0)
            total = total + d * h * 12.0 / 52.0
    return total

def informal_care_value(df, needs_help_col="r1rcany", hours_week_col="care_hours_week",
                        wage_hour=0.0, weight="r1wtresp", pop_scale=None, opportunity_wage_hour=None):
    w = pd.to_numeric(df[weight], errors="coerce").fillna(0)
    hours = pd.to_numeric(df[hours_week_col], errors="coerce").fillna(0)
    if needs_help_col in df.columns and pd.to_numeric(df[needs_help_col], errors="coerce").notna().any():
        rec_mask = pd.to_numeric(df[needs_help_col], errors="coerce").fillna(0) == 1
    else:
        rec_mask = hours > 0
    recipients_pct = float(100 * np.average(rec_mask.astype(float), weights=w)) if w.sum() > 0 else np.nan
    wr = w[rec_mask]; hr_ = hours[rec_mask]
    mean_hours_week = float(np.average(hr_, weights=wr)) if wr.sum() > 0 else 0.0
    annual_value_per_recipient = mean_hours_week * 52 * wage_hour
    out = {"recipients_pct": recipients_pct, "mean_hours_week": mean_hours_week,
           "annual_value_per_recipient": annual_value_per_recipient}
    if pop_scale is not None:
        out["national_annual_value"] = pop_scale * (recipients_pct / 100) * annual_value_per_recipient
    if opportunity_wage_hour is not None:
        opp = mean_hours_week * 52 * opportunity_wage_hour
        out["opportunity_value_per_recipient"] = opp
        if pop_scale is not None:
            out["opportunity_national_annual_value"] = pop_scale * (recipients_pct / 100) * opp
    return out


def two_part_model(df, y="oop_total", covars=None, weight="r1wtresp"):
    covars = list(covars)
    d = df[[y, weight] + covars].dropna()
    w = pd.to_numeric(d[weight], errors="coerce").fillna(1.0)
    X = sm.add_constant(d[covars].apply(pd.to_numeric, errors="coerce"))
    yv = pd.to_numeric(d[y], errors="coerce")
    rows = []
    p1 = sm.GLM((yv > 0).astype(float), X, family=sm.families.Binomial(), freq_weights=w).fit()
    pos = yv > 0
    p2 = sm.GLM(yv[pos], X[pos.values], family=sm.families.Gamma(sm.families.links.Log()),
                freq_weights=w[pos.values]).fit()
    for part, res in [("participation", p1), ("amount", p2)]:
        for term in res.params.index:
            coef = float(res.params[term]); se = float(res.bse[term])
            rows.append({"term": term, "part": part, "coef": coef,
                         "ratio": float(np.exp(coef)),
                         "ci_low": float(np.exp(coef - 1.96 * se)),
                         "ci_high": float(np.exp(coef + 1.96 * se)),
                         "p": float(res.pvalues[term])})
    return pd.DataFrame(rows)


def add_che_flags(df, oop="oop_total", cons="cons_total", cap="capacity_to_pay"):
    out = df.copy()
    share = pd.to_numeric(out[oop], errors="coerce") / pd.to_numeric(out[cons], errors="coerce").replace(0, np.nan)
    capsh = pd.to_numeric(out[oop], errors="coerce") / pd.to_numeric(out[cap], errors="coerce").replace(0, np.nan)
    out["che10_flag"] = (share > 0.10).fillna(False).astype(int)
    out["che25_flag"] = (share > 0.25).fillna(False).astype(int)
    out["che40cap_flag"] = (capsh > 0.40).fillna(False).astype(int)
    return out


def che_ml_drivers(df, target="che40cap_flag", features=None, weight="r1wtresp", cv=5, random_state=0):
    features = list(features)
    d = df[[target, weight] + features].dropna()
    X = d[features].apply(pd.to_numeric, errors="coerce")
    y = pd.to_numeric(d[target], errors="coerce").astype(int)
    w = pd.to_numeric(d[weight], errors="coerce").fillna(1.0)
    model = HistGradientBoostingClassifier(random_state=random_state)
    auc = float(np.mean(cross_val_score(model, X, y, cv=cv, scoring="roc_auc")))
    model.fit(X, y, sample_weight=w.values)
    try:
        expl = shap.Explainer(model, X)
        sv = expl(X)
        vals = np.abs(sv.values).mean(axis=0)
    except Exception:
        expl = shap.TreeExplainer(model)
        sv = expl.shap_values(X)
        vals = np.abs(sv).mean(axis=0)
    imp = pd.DataFrame({"feature": features, "mean_abs_shap": vals}).sort_values(
        "mean_abs_shap", ascending=False).reset_index(drop=True)
    return {"auc": auc, "model": model, "shap_importance": imp}


def simulate_policy(df, scenario, weight="r1wtresp", line=None, pop_scale=None):
    inp = float(scenario.get("inpatient_cover_frac", 0) or 0)
    drug = float(scenario.get("drug_cover_frac", 0) or 0)
    outp = float(scenario.get("outpatient_cover_frac", 0) or 0)
    topup = float(scenario.get("pension_topup_annual", 0) or 0)
    age_min = float(scenario.get("age_min", 0) or 0)
    d = df.copy()
    w = pd.to_numeric(d[weight], errors="coerce").fillna(0)
    elig = (pd.to_numeric(d["age_years"], errors="coerce") >= age_min).astype(float)
    hosp = pd.to_numeric(d["oop_hosp"], errors="coerce").fillna(0)
    med = pd.to_numeric(d["oop_med"], errors="coerce").fillna(0)
    out = pd.to_numeric(d["oop_out"], errors="coerce").fillna(0)
    absorbed = elig * (inp * hosp + drug * med + outp * out)
    new_oop_total = (hosp - inp * hosp * elig) + (med - drug * med * elig) + (out - outp * out * elig)
    new_cons_total = pd.to_numeric(d["cons_total"], errors="coerce") + topup * elig
    new_cons_pc = pd.to_numeric(d["cons_pc"], errors="coerce") + topup * elig
    nonfood = pd.to_numeric(d["cons_nonfood"], errors="coerce")
    new_cap = (new_cons_total - nonfood).where(new_cons_total > nonfood, nonfood)
    cf = pd.DataFrame({"oop_total": new_oop_total, "cons_total": new_cons_total,
                       "capacity_to_pay": new_cap, "cons_pc": new_cons_pc, weight: w})
    base = che_indicators(df)
    new = che_indicators(cf)
    res = {k: new[k] for k in ("che10", "che25", "che40cap")}
    for k in ("che10", "che25", "che40cap"):
        res[f"{k}_delta"] = new[k] - base[k]
    if line is not None:
        base_imp = impoverishment(df, line=line)
        new_imp = impoverishment(cf, line=line)
        res["post_poverty"] = new_imp["post_poverty"]
        res["post_poverty_delta"] = new_imp["post_poverty"] - base_imp["post_poverty"]
    else:
        res["post_poverty"] = np.nan
        res["post_poverty_delta"] = np.nan
    cost = absorbed + topup * elig
    if pop_scale is not None:
        res["fiscal_cost"] = float(np.average(cost, weights=w)) * pop_scale if w.sum() > 0 else np.nan
    else:
        res["fiscal_cost"] = float((w * cost).sum())
    return res
