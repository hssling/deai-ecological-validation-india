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
