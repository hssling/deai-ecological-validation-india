"""
06_sensitivity_ipw.py — inverse-probability-of-availability weighting sensitivity.
Confirms headline diagnosis-gap / burden estimates are robust to non-random biomarker availability.
"""
import os, numpy as np, pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm
from util_survey import wmean

HERE = os.path.dirname(__file__); OUT = os.path.join(HERE, "..", "outputs")
df = pd.read_parquet(os.path.join(OUT, "analytic_final.parquet"))
W = "person_weight"

# availability model: predict having a near-complete biomarker panel
df["avail"] = (df[["ab_dysgly","ab_htn","ab_anaemia","ab_inflam","ab_grip","ab_waist"]]
               .notna().sum(axis=1) >= 5).astype(int)
m = smf.glm("avail ~ age_years + C(sex) + C(residence) + education_years + poverty + "
            "frailty_index + adl_limitation",
            data=df, family=sm.families.Binomial()).fit()
df["p_avail"] = m.predict(df)
df["ipw"] = np.where(df["avail"] == 1, 1.0 / df["p_avail"].clip(0.05, 0.99), np.nan)
df["w_ipw"] = df[W] * df["ipw"]

def cmp(col, sub=None):
    d = df if sub is None else df[sub]
    return wmean(d[col], d[W]), wmean(d[col], d["w_ipw"])

rows = []
for name, col, sub in [
    ("Undiagnosed diabetes (%)", "undx_diab", df["biochem_diab"] == 1),
    ("Undiagnosed hypertension (%)", "undx_htn", df["measured_htn"] == 1),
    ("Biochemical diabetes (%)", "biochem_diab", None),
    ("Measured hypertension (%)", "measured_htn", None),
    ("Anaemia (%)", "ab_anaemia", None),
    ("High burden >=3 (%)", "high_burden", None),
]:
    base, ipw = cmp(col, sub)
    rows.append({"indicator": name, "person_weight_%": round(100*base,1),
                 "IPW_%": round(100*ipw,1), "abs_diff": round(100*(ipw-base),2)})
out = pd.DataFrame(rows)
out.to_csv(os.path.join(OUT, "tables", "t_S2_ipw_sensitivity.csv"), index=False)
print(out.to_string(index=False))
print("\nMax absolute difference (pp):", round(out["abs_diff"].abs().max(), 2))
