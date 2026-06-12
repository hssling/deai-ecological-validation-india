"""
10_absolute_burden_sensitivity.py  — easy, high-value strengthening:
  (A) Absolute national population burden (millions) using LASI population-expansion weights.
  (B) Threshold sensitivity (alternative clinical cut-offs).
  (C) Age-group stratification of the diagnosis gap.
"""
import os, numpy as np, pandas as pd
HERE = os.path.dirname(__file__); OUT = os.path.join(HERE, "..", "outputs"); T = os.path.join(OUT, "tables")
df = pd.read_parquet(os.path.join(OUT, "analytic_final.parquet"))
WD = "dbs_weight"   # population-expansion weight (sums to ~234M, the DBS-eligible 45+ population)
WP = "person_weight"

def wprev(num_mask, den_mask, w):
    den = df.loc[den_mask & df[w].notna(), w].sum()
    num = df.loc[num_mask & den_mask & df[w].notna(), w].sum()
    return (num / den * 100) if den else np.nan
def millions(mask):
    return df.loc[mask & df[WD].notna(), WD].sum() / 1e6

# ---------- (A) absolute national burden ----------
rows = [
    ("Undiagnosed diabetes", (df.biochem_diab == 1) & (df.undx_diab == 1)),
    ("Undiagnosed hypertension", (df.measured_htn == 1) & (df.undx_htn == 1)),
    ("Uncontrolled diabetes (affected, not at target)", (df.dm_present == 1) & (df.dm_controlled == 0)),
    ("Uncontrolled hypertension (affected, not at target)", (df.htn_present == 1) & (df.htn_controlled == 0)),
    ("Anaemia", df.ab_anaemia == 1),
    ("Elevated CRP (>3 mg/L)", df.ab_inflam == 1),
    ("High multi-system burden (>=3 systems)", df.high_burden == 1),
]
ab = pd.DataFrame([{"indicator": n, "represented_millions": round(millions(m), 1)} for n, m in rows])
ab.loc[len(ab)] = ["Represented 45+ population (DBS-eligible)", round(df[WD].sum() / 1e6, 0)]
ab.to_csv(os.path.join(T, "t12_absolute_burden.csv"), index=False)
print("=== TABLE S: Absolute national burden (millions) ===\n", ab.to_string(index=False))

# ---------- (B) threshold sensitivity ----------
sens = []
# diabetes: HbA1c>=6.5 (primary) vs >=7.0
for thr in [6.5, 7.0]:
    m = df["hba1c"] >= thr
    p_prev = wprev(m, df["hba1c"].notna(), WP)
    p_undx = wprev(df["chronic_diabetes"] == 0, m, WP)
    sens.append({"condition": "Diabetes", "threshold": f"HbA1c>={thr}", "prevalence_%": round(p_prev, 1),
                 "undiagnosed_%": round(p_undx, 1)})
# hypertension: >=140/90 (primary) vs >=130/80 (ACC/AHA)
for s_thr, d_thr, lab in [(140, 90, ">=140/90"), (130, 80, ">=130/80")]:
    m = (df["sbp"] >= s_thr) | (df.get("measured_dbp") >= d_thr)
    m = m & (df["sbp"].notna() | df["measured_dbp"].notna())
    p_prev = wprev(m, df["sbp"].notna(), WP)
    p_undx = wprev(df["chronic_hypertension"] == 0, m, WP)
    sens.append({"condition": "Hypertension", "threshold": lab, "prevalence_%": round(p_prev, 1),
                 "undiagnosed_%": round(p_undx, 1)})
# inflammation CRP>3 vs >10
for thr in [3, 10]:
    m = df["crp"] > thr
    sens.append({"condition": "Inflammation", "threshold": f"CRP>{thr}", "prevalence_%": round(wprev(m, df["crp"].notna(), WP), 1),
                 "undiagnosed_%": np.nan})
sdf = pd.DataFrame(sens); sdf.to_csv(os.path.join(T, "t13_threshold_sensitivity.csv"), index=False)
print("\n=== TABLE S: Threshold sensitivity ===\n", sdf.to_string(index=False))

# ---------- (C) age-group stratification of the diagnosis gap ----------
df["age_grp"] = pd.cut(df["age_years"], [44, 59, 74, 200], labels=["45-59", "60-74", "75+"])
ag = []
for g, s in df.groupby("age_grp", observed=True):
    ag.append({"age_group": str(g),
               "biochem_diabetes_%": round(wprev(s.index.to_series().map(lambda i: df.loc[i, "biochem_diab"] == 1).fillna(False),
                                                  df.index.isin(s.index) & df.biochem_diab.notna(), WP), 1) if False else
                                     round(wprev((df.biochem_diab == 1) & df.index.isin(s.index), df.index.isin(s.index) & df.biochem_diab.notna(), WP), 1),
               "undiagnosed_diabetes_%": round(wprev((df.undx_diab == 1) & df.index.isin(s.index), (df.biochem_diab == 1) & df.index.isin(s.index), WP), 1),
               "undiagnosed_htn_%": round(wprev((df.undx_htn == 1) & df.index.isin(s.index), (df.measured_htn == 1) & df.index.isin(s.index), WP), 1)})
agdf = pd.DataFrame(ag); agdf.to_csv(os.path.join(T, "t14_age_group_gap.csv"), index=False)
print("\n=== TABLE S: Diagnosis gap by age group ===\n", agdf.to_string(index=False))
