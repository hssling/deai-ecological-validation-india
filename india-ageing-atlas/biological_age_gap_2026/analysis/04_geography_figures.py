"""
04_geography_figures.py — state surveillance table + publication figures.
Run after 03_core_analysis.py (needs outputs/analytic_final.parquet and tables t1-t5).
"""
import os, numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from util_survey import wmean, cluster_bootstrap_ci

HERE = os.path.dirname(__file__); OUT = os.path.join(HERE, "..", "outputs")
T = os.path.join(OUT, "tables"); F = os.path.join(OUT, "figures")
os.makedirs(F, exist_ok=True)
plt.rcParams.update({"font.size": 11, "figure.dpi": 150, "savefig.bbox": "tight",
                     "axes.spines.top": False, "axes.spines.right": False})
TEAL, CORAL, SLATE = "#1b7a78", "#e06c5a", "#34495e"

df = pd.read_parquet(os.path.join(OUT, "analytic_final.parquet"))
W = "person_weight"

# ---------- state surveillance table ----------
statecol = "state_name" if "state_name" in df and df["state_name"].notna().any() else "state_code"
rows = []
for st, s in df.groupby(statecol):
    if len(s) < 150:
        continue
    burden = wmean(s["subclinical_burden"], s[W])
    undx = wmean(s.loc[s["biochem_diab"] == 1, "undx_diab"], s.loc[s["biochem_diab"] == 1, W])
    rows.append({"state": str(st), "n": len(s),
                 "mean_burden": round(burden, 3),
                 "undx_diabetes_pct": round(100 * undx, 1) if np.isfinite(undx) else np.nan,
                 "high_burden_pct": round(100 * wmean(s["high_burden"], s[W]), 1)})
states = pd.DataFrame(rows).sort_values("high_burden_pct", ascending=False)
states.to_csv(os.path.join(T, "t6_state_surveillance.csv"), index=False)
print("State surveillance (top 8 by high-burden %):\n", states.head(8).to_string(index=False))

# ---------- Figure 1: the diagnosis gap ----------
t1 = pd.read_csv(os.path.join(T, "t1_diagnosis_gap.csv"))
def gp(name):
    return float(t1.loc[t1["indicator"] == name, "weighted_pct_95CI"].iloc[0].split()[0])
fig, ax = plt.subplots(figsize=(7.2, 4.2))
labels = ["Diabetes", "Hypertension"]
selfrep = [gp("Self-reported diabetes"), gp("Self-reported hypertension")]
measured = [gp("Biochemical diabetes (HbA1c>=6.5)"), gp("Measured hypertension (SBP>=140)")]
undx = [gp("Undiagnosed among biochemically diabetic"), gp("Undiagnosed among measured-hypertensive")]
x = np.arange(len(labels)); w = 0.35
ax.bar(x - w/2, selfrep, w, label="Self-reported (known)", color=SLATE)
ax.bar(x + w/2, measured, w, label="Biologically measured", color=TEAL)
for i, u in enumerate(undx):
    ax.text(i, measured[i] + 1.5, f"{u:.0f}% undiagnosed", ha="center", color=CORAL, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(labels); ax.set_ylabel("Weighted prevalence (%)")
ax.set_title("The diagnosis gap: measured vs self-reported disease, adults 45+ (LASI W1)")
ax.legend(frameon=False)
fig.savefig(os.path.join(F, "fig1_diagnosis_gap.png")); plt.close(fig)

# ---------- Figure 2: social patterning ----------
t2 = pd.read_csv(os.path.join(T, "t2_social_patterning.csv"))
order = {"residence": ["rural", "urban"], "sex": ["female", "male"],
         "edu_grp": ["No education", "1-5 yr", "6+ yr"],
         "wealth_grp": ["Poorest", "Middle", "Richest"]}
fig, axes = plt.subplots(1, 4, figsize=(15, 4), sharey=True)
for ax, strat in zip(axes, order):
    sub = t2[t2["stratum"] == strat].set_index("group").reindex(order[strat]).dropna(how="all")
    if sub.empty:
        ax.axis("off"); continue
    ax.bar(sub.index, sub["undx_diabetes_pct"], color=TEAL, alpha=0.9)
    ax.set_title(strat.replace("_grp", "").replace("residence", "Residence").title())
    ax.tick_params(axis="x", rotation=20)
axes[0].set_ylabel("Undiagnosed diabetes (%)")
fig.suptitle("Social patterning of undiagnosed diabetes (among biochemically diabetic)", y=1.03)
fig.savefig(os.path.join(F, "fig2_social_patterning.png")); plt.close(fig)

# ---------- Figure 3: incremental value AUROC ----------
t3 = pd.read_csv(os.path.join(T, "t3_incremental_value.csv"))
t3["auc"] = t3["AUROC_95CI"].str.split().str[0].astype(float)
t3["lo"] = t3["AUROC_95CI"].str.extract(r"\(([0-9.]+)-")[0].astype(float)
t3["hi"] = t3["AUROC_95CI"].str.extract(r"-([0-9.]+)\)")[0].astype(float)
fig, ax = plt.subplots(figsize=(8, 3.6))
y = np.arange(len(t3))[::-1]
ax.errorbar(t3["auc"], y, xerr=[t3["auc"]-t3["lo"], t3["hi"]-t3["auc"]], fmt="o",
            color=TEAL, capsize=3)
ax.set_yticks(y); ax.set_yticklabels(t3["model"]); ax.set_xlabel("AUROC for past-year hospitalisation")
ax.set_title("Incremental value of measured biomarker burden")
fig.savefig(os.path.join(F, "fig3_incremental_value.png")); plt.close(fig)

# ---------- Figure 4: state ranking ----------
fig, ax = plt.subplots(figsize=(7.5, 7))
ss = states.dropna(subset=["high_burden_pct"]).sort_values("high_burden_pct")
ax.barh(ss["state"], ss["high_burden_pct"], color=TEAL)
ax.set_xlabel("High subclinical biomarker burden (% ≥3 systems, weighted)")
ax.set_title("State/UT surveillance: multi-system biological burden")
fig.savefig(os.path.join(F, "fig4_state_ranking.png")); plt.close(fig)

# ---------- Figure 5: exposome predictors (IRR forest) ----------
t5 = pd.read_csv(os.path.join(T, "t5_exposome_predictors.csv"))
t5 = t5[~t5["term"].str.contains("Intercept")]
nice = {"age_years": "Age (per year)", "C(sex)[T.male]": "Male sex",
        "C(residence)[T.urban]": "Urban residence", "education_years": "Education (per year)",
        "poverty": "Household poverty", "current_smoking": "Current smoking",
        "current_smokeless_tobacco": "Smokeless tobacco", "unclean_cooking_fuel": "Unclean cooking fuel",
        "unimproved_sanitation": "Unimproved sanitation", "unimproved_drinking_water": "Unimproved water"}
t5["label"] = t5["term"].map(nice).fillna(t5["term"])
t5 = t5.iloc[::-1]
fig, ax = plt.subplots(figsize=(7.5, 5))
y = np.arange(len(t5))
ax.errorbar(t5["IRR"], y, xerr=[t5["IRR"]-t5["ci_lo"], t5["ci_hi"]-t5["IRR"]], fmt="o",
            color=SLATE, capsize=3)
ax.axvline(1.0, color=CORAL, ls="--", lw=1)
ax.set_yticks(y); ax.set_yticklabels(t5["label"]); ax.set_xlabel("Incidence-rate ratio for biomarker burden count")
ax.set_title("Adjusted predictors of subclinical biomarker burden")
fig.savefig(os.path.join(F, "fig5_exposome_predictors.png")); plt.close(fig)

print("Figures written to", F)
