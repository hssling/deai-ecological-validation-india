from __future__ import annotations

import numpy as np
import pandas as pd
import pyreadstat


def deflate(series: pd.Series, cpi: dict[int, float], year: int, base: int = 2017) -> pd.Series:
    factor = cpi[year] / cpi[base]
    return pd.to_numeric(series, errors="coerce") / factor


ECON_VARS = [
    "prim_key", "hhid", "r1wtresp", "r1agey", "ragender", "hh1rural", "hh1state",
    "r1oophos1y", "r1oopdoc1y", "r1oopsupl1y", "hh1cohc1m", "hh1cihc1y",
    "hh1ctot", "hh1cnf1y", "hh1cperc", "hh1poverty", "hh1ipubpen", "hh1ipena",
    "c2018cpindex", "c2017cpindex",
]


def load_economics_frame(sav_path: str, processed_csv: str) -> pd.DataFrame:
    raw, _ = pyreadstat.read_sav(sav_path, usecols=ECON_VARS)
    raw["prim_key"] = pd.to_numeric(raw["prim_key"], errors="coerce").astype("Int64")
    cpi = {2017: float(raw["c2017cpindex"].dropna().iloc[0]),
           2018: float(raw["c2018cpindex"].dropna().iloc[0])}
    for col in ["r1oophos1y", "r1oopdoc1y", "r1oopsupl1y", "hh1ctot", "hh1cnf1y", "hh1cperc", "hh1ipubpen", "hh1ipena"]:
        raw[col] = deflate(raw[col], cpi, year=2018, base=2017)
    df = pd.DataFrame({
        "prim_key": raw["prim_key"],
        "r1wtresp": pd.to_numeric(raw["r1wtresp"], errors="coerce"),
        "oop_hosp": raw["r1oophos1y"].clip(lower=0),
        "oop_out": raw["r1oopdoc1y"].clip(lower=0),
        "oop_med": raw["r1oopsupl1y"].clip(lower=0),
        "cons_total": raw["hh1ctot"].clip(lower=0),
        "cons_nonfood": raw["hh1cnf1y"].clip(lower=0),
        "cons_pc": raw["hh1cperc"].clip(lower=0),
        "poverty_intl": pd.to_numeric(raw["hh1poverty"], errors="coerce"),
        "pub_pension": raw["hh1ipubpen"].clip(lower=0),
        "priv_pension": raw["hh1ipena"].clip(lower=0),
    })
    df["oop_total"] = df[["oop_hosp", "oop_out", "oop_med"]].sum(axis=1, min_count=1)
    df["capacity_to_pay"] = (df["cons_total"] - df["cons_nonfood"]).where(
        df["cons_total"] > df["cons_nonfood"], df["cons_nonfood"])
    df["any_pension"] = ((df["pub_pension"] > 0) | (df["priv_pension"] > 0)).astype(int)
    proc = pd.read_csv(processed_csv)
    proc["prim_key"] = pd.to_numeric(proc["prim_key"], errors="coerce").astype("Int64")
    keep = ["prim_key", "age_years", "sex", "residence", "state_code", "living_alone",
            "multimorbidity_ge2", "functional_limitation", "education"]
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
