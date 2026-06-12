"""
07_cascade_equity_maps.py  — strengthening additions:
  (A) Full care cascade (affected -> aware -> treated -> controlled) for diabetes & hypertension.
  (B) Concentration indices (socioeconomic inequality) for undiagnosed/uncontrolled burden & domains.
  (C) India choropleth maps from the state shapefile.
Run after 05. Adds medication variables from the harmonized file.
"""
import os, numpy as np, pandas as pd, pyreadstat
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import geopandas as gpd
from util_survey import wmean, cluster_bootstrap_ci, fmt_pct

HERE = os.path.dirname(__file__); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "..", "outputs"); T = os.path.join(OUT, "tables"); F = os.path.join(OUT, "figures")
plt.rcParams.update({"font.size": 11, "figure.dpi": 150, "savefig.bbox": "tight",
                     "axes.spines.top": False, "axes.spines.right": False})
TEAL, CORAL, SLATE, GOLD = "#1b7a78", "#e06c5a", "#34495e", "#c89b3c"

df = pd.read_parquet(os.path.join(OUT, "analytic_final.parquet"))
W = "person_weight"; df["clust"] = df["ssuid"].fillna(-1)
df["prim_key"] = df["prim_key"].astype(str).str.strip()

# ---- merge medication variables ----
med, _ = pyreadstat.read_sav(os.path.join(ROOT, "data/raw/g2aging_harmonized_lasi_a3_sav/H_LASI_a3.sav"),
                             usecols=["prim_key", "r1rxdiab", "r1rxhibp"])
med["prim_key"] = med["prim_key"].astype(str).str.strip()
df = df.merge(med, on="prim_key", how="left")

# =====================================================================
# (A) CARE CASCADE
# =====================================================================
# Diabetes: present if HbA1c>=6.5 OR on diabetes meds OR self-reported diagnosed
df["dm_present"] = (((df["hba1c"] >= 6.5) | (df["r1rxdiab"] == 1) | (df["chronic_diabetes"] == 1))
                    .astype(float))
df.loc[df["hba1c"].isna() & df["r1rxdiab"].isna() & df["chronic_diabetes"].isna(), "dm_present"] = np.nan
df["dm_aware"]      = np.where(df["dm_present"] == 1, (df["chronic_diabetes"] == 1).astype(float), np.nan)
df["dm_treated"]    = np.where(df["dm_present"] == 1, (df["r1rxdiab"] == 1).astype(float), np.nan)
df["dm_controlled"] = np.where(df["dm_present"] == 1, (df["hba1c"] < 7.0).astype(float), np.nan)

# Hypertension: present if BP>=140/90 OR on BP meds OR self-reported diagnosed
bp_high = (df["sbp"] >= 140) | (df.get("measured_dbp") >= 90)
df["htn_present"] = ((bp_high | (df["r1rxhibp"] == 1) | (df["chronic_hypertension"] == 1)).astype(float))
df.loc[df["sbp"].isna() & df["r1rxhibp"].isna() & df["chronic_hypertension"].isna(), "htn_present"] = np.nan
df["htn_aware"]      = np.where(df["htn_present"] == 1, (df["chronic_hypertension"] == 1).astype(float), np.nan)
df["htn_treated"]    = np.where(df["htn_present"] == 1, (df["r1rxhibp"] == 1).astype(float), np.nan)
df["htn_controlled"] = np.where(df["htn_present"] == 1, (~bp_high).astype(float), np.nan)

def cascade_row(cond, sub=None):
    out = {}
    for stage, col in [("aware", f"{cond}_aware"), ("treated", f"{cond}_treated"),
                       ("controlled", f"{cond}_controlled")]:
        p, lo, hi = cluster_bootstrap_ci(df, col, W, "clust", subset=sub, n_boot=300)
        out[stage] = (100*p, 100*lo, 100*hi)
    return out

rows = []
for cond, label in [("dm", "Diabetes"), ("htn", "Hypertension")]:
    c = cascade_row(cond)
    for stage in ["aware", "treated", "controlled"]:
        p, lo, hi = c[stage]
        rows.append({"condition": label, "stage": stage,
                     "pct_of_affected": round(p, 1), "ci": f"({lo:.1f}-{hi:.1f})"})
casc = pd.DataFrame(rows); casc.to_csv(os.path.join(T, "t9_care_cascade.csv"), index=False)
print("=== TABLE 9: Care cascade (% of all affected) ===\n", casc.to_string(index=False))

# cascade by social group (aware/treated/controlled) for each condition
rows = []
for strat in ["residence", "edu_grp", "wealth_grp"]:
    for g, s in df.groupby(strat, observed=True):
        rec = {"stratum": strat, "group": str(g)}
        for cond in ["dm", "htn"]:
            for stage in ["aware", "treated", "controlled"]:
                rec[f"{cond}_{stage}"] = round(100*wmean(df.loc[s.index, f"{cond}_{stage}"], df.loc[s.index, W]), 1)
        rows.append(rec)
casc_soc = pd.DataFrame(rows); casc_soc.to_csv(os.path.join(T, "t10_cascade_by_group.csv"), index=False)
print("\n=== TABLE 10: Cascade by social group ===\n", casc_soc.to_string(index=False))

# =====================================================================
# (B) CONCENTRATION INDEX (socioeconomic inequality, ranked by wealth)
# =====================================================================
def concentration_index(d, yvar, wealthvar, wvar):
    """Wagstaff concentration index + Erreygers-corrected index for bounded [0,1] y."""
    s = d[[yvar, wealthvar, wvar]].dropna()
    if len(s) < 50 or s[yvar].nunique() < 2:
        return np.nan, np.nan
    w = s[wvar].values; y = s[yvar].values
    order = np.argsort(s[wealthvar].values)
    w, y = w[order], y[order]
    wn = w / w.sum()
    cum = np.cumsum(wn) - 0.5 * wn          # fractional rank (weighted)
    mu = np.sum(wn * y)
    CI = 2 * np.sum(wn * y * cum) / mu - 1   # standard concentration index
    EI = 4 * mu * CI                          # Erreygers correction for [0,1] bounded y
    return CI, EI

def ci_boot(d, yvar, wealthvar, wvar, cluster="clust", n=300, seed=3):
    rng = np.random.default_rng(seed)
    s = d[[yvar, wealthvar, wvar, cluster]].dropna()
    clusters = s[cluster].unique(); groups = {c: g for c, g in s.groupby(cluster)}
    pt = concentration_index(s, yvar, wealthvar, wvar)[1]
    est = []
    for _ in range(n):
        samp = rng.choice(clusters, len(clusters), replace=True)
        b = pd.concat([groups[c] for c in samp], ignore_index=True)
        est.append(concentration_index(b, yvar, wealthvar, wvar)[1])
    return pt, np.nanpercentile(est, 2.5), np.nanpercentile(est, 97.5)

df["wealth_rank_var"] = df["hh1itot"]
ci_rows = []
for name, yv in [("Undiagnosed diabetes", "undx_diab"), ("Undiagnosed hypertension", "undx_htn"),
                 ("Uncontrolled diabetes", None), ("Dysglycaemia", "ab_dysgly"),
                 ("Central obesity", "ab_waist"), ("Anaemia", "ab_anaemia"),
                 ("Low grip strength", "ab_grip"), ("High biological burden", "high_burden")]:
    if yv is None and name == "Uncontrolled diabetes":
        df["uncontrolled_dm"] = np.where(df["dm_present"] == 1, (df["hba1c"] >= 7.0).astype(float), np.nan)
        yv = "uncontrolled_dm"
    pt, lo, hi = ci_boot(df, yv, "wealth_rank_var", W)
    ci_rows.append({"indicator": name, "erreygers_CI": round(pt, 4),
                    "ci95": f"({lo:.4f}, {hi:.4f})",
                    "direction": "pro-poor (worse among poor)" if pt < 0 else "pro-rich (worse among rich)"})
cidf = pd.DataFrame(ci_rows); cidf.to_csv(os.path.join(T, "t11_concentration_index.csv"), index=False)
print("\n=== TABLE 11: Erreygers concentration indices (wealth-ranked) ===\n", cidf.to_string(index=False))

# =====================================================================
# (C) CHOROPLETH MAPS
# =====================================================================
NAME_MAP = {"Andaman and Nicobar": "Andaman & Nicobar", "Chhatisgarh": "Chhattisgarh",
            "Jammu and Kashmir": "Jammu & Kashmir",
            "Dadra and Nagar Haveli": "Dadra and Nagar Haveli and Daman and Diu",
            "Daman and Diu": "Dadra and Nagar Haveli and Daman and Diu"}
df["st_shp"] = df["state_name"].replace(NAME_MAP)
def state_stat(col, sub=None):
    d = df if sub is None else df[sub]
    g = d.groupby("st_shp").apply(lambda s: wmean(s[col], s[W]) * 100, include_groups=False)
    return g
state_tab = pd.DataFrame({
    "undx_dm": df[df["biochem_diab"] == 1].groupby("st_shp").apply(lambda s: wmean(s["undx_diab"], s[W])*100, include_groups=False),
    "undx_htn": df[df["measured_htn"] == 1].groupby("st_shp").apply(lambda s: wmean(s["undx_htn"], s[W])*100, include_groups=False),
    "high_burden": state_stat("high_burden"),
    "htn_control": df[df["htn_present"] == 1].groupby("st_shp").apply(lambda s: wmean(s["htn_controlled"], s[W])*100, include_groups=False),
})
gdf = gpd.read_file(os.path.join(ROOT, "data/external/datameet_states/Admin2.shp"))
gdf = gdf.merge(state_tab, left_on="ST_NM", right_index=True, how="left")

panels = [("undx_dm", "Undiagnosed diabetes (%)", "Reds"),
          ("undx_htn", "Undiagnosed hypertension (%)", "Reds"),
          ("high_burden", "High biological burden (%)", "Purples"),
          ("htn_control", "Hypertension control (%)", "Greens")]
fig, axes = plt.subplots(2, 2, figsize=(13, 14))
for ax, (col, title, cmap) in zip(axes.ravel(), panels):
    gdf.plot(column=col, cmap=cmap, linewidth=0.3, edgecolor="white", ax=ax,
             legend=True, missing_kwds={"color": "lightgrey"},
             legend_kwds={"shrink": 0.6})
    ax.set_title(title, fontsize=12); ax.axis("off")
fig.suptitle("State surveillance of the diagnosis gap and biological burden, India (LASI W1)", fontsize=14, y=0.93)
fig.savefig(os.path.join(F, "fig5_india_maps.png")); plt.close(fig)
print("\nMaps written -> fig5_india_maps.png")

# cascade figure (overall)
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), sharey=True)
for ax, (cond, label, col) in zip(axes, [("dm", "Diabetes", TEAL), ("htn", "Hypertension", SLATE)]):
    stages = ["Affected", "Aware", "Treated", "Controlled"]
    vals = [100,
            casc[(casc.condition == label) & (casc.stage == "aware")]["pct_of_affected"].iloc[0],
            casc[(casc.condition == label) & (casc.stage == "treated")]["pct_of_affected"].iloc[0],
            casc[(casc.condition == label) & (casc.stage == "controlled")]["pct_of_affected"].iloc[0]]
    ax.bar(stages, vals, color=col)
    for i, v in enumerate(vals):
        ax.text(i, v + 1.5, f"{v:.0f}%", ha="center", fontweight="bold")
    ax.set_title(f"{label} care cascade"); ax.set_ylim(0, 108)
axes[0].set_ylabel("% of all affected (weighted)")
fig.suptitle("Care cascade among older Indians: aware → treated → controlled", y=1.02)
fig.savefig(os.path.join(F, "fig6_care_cascade.png")); plt.close(fig)
print("Cascade figure -> fig6_care_cascade.png")

df.to_parquet(os.path.join(OUT, "analytic_final.parquet"), index=False)
print("Saved analytic_final.parquet with cascade + medication variables")
