"""
08_equity_fig_robustness.py
  (1) Concentration-index forest figure (equity).
  (2) Cluster-bootstrap robustness for a headline regression + incremental delta-AUROC,
      confirming design-based inference agrees with the weighted point estimates
      (neutralises the statsmodels freq_weights caveat).
"""
import os, numpy as np, pandas as pd
import statsmodels.api as sm, statsmodels.formula.api as smf
from sklearn.metrics import roc_auc_score
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(__file__); OUT = os.path.join(HERE, "..", "outputs")
T = os.path.join(OUT, "tables"); F = os.path.join(OUT, "figures")
plt.rcParams.update({"font.size": 11, "figure.dpi": 150, "savefig.bbox": "tight",
                     "axes.spines.top": False, "axes.spines.right": False})
df = pd.read_parquet(os.path.join(OUT, "analytic_final.parquet"))
W = "person_weight"; df["clust"] = df["ssuid"].fillna(-1)

# ---------- (1) concentration-index forest ----------
ci = pd.read_csv(os.path.join(T, "t11_concentration_index.csv"))
ci["lo"] = ci["ci95"].str.extract(r"\(([-0-9.]+),")[0].astype(float)
ci["hi"] = ci["ci95"].str.extract(r", ([-0-9.]+)\)")[0].astype(float)
ci = ci.iloc[::-1].reset_index(drop=True)
colors = ["#1b7a78" if v < 0 else "#e06c5a" for v in ci["erreygers_CI"]]
fig, ax = plt.subplots(figsize=(8.5, 5))
y = np.arange(len(ci))
ax.errorbar(ci["erreygers_CI"], y, xerr=[ci["erreygers_CI"]-ci["lo"], ci["hi"]-ci["erreygers_CI"]],
            fmt="none", ecolor="grey", capsize=3, zorder=1)
ax.scatter(ci["erreygers_CI"], y, color=colors, s=60, zorder=2)
ax.axvline(0, color="#34495e", lw=1)
ax.set_yticks(y); ax.set_yticklabels(ci["indicator"])
ax.set_xlabel("Erreygers concentration index (wealth-ranked)\n← concentrated among the poor      concentrated among the rich →")
ax.set_title("Socioeconomic inequality in biological ageing burden")
fig.savefig(os.path.join(F, "fig7_concentration_index.png")); plt.close(fig)
print("Equity forest -> fig7_concentration_index.png")

# ---------- (2) cluster-bootstrap robustness ----------
def cluster_boot_glm(d, formula, term, n=400, seed=7):
    rng = np.random.default_rng(seed)
    base = smf.glm(formula, data=d, family=sm.families.Binomial(),
                   freq_weights=d[W]).fit()
    pt = base.params[term]
    clusters = d["clust"].unique(); groups = {c: g for c, g in d.groupby("clust")}
    est = []
    for _ in range(n):
        samp = rng.choice(clusters, len(clusters), replace=True)
        b = pd.concat([groups[c] for c in samp], ignore_index=True)
        try:
            m = smf.glm(formula, data=b, family=sm.families.Binomial(), freq_weights=b[W]).fit()
            est.append(m.params[term])
        except Exception:
            pass
    lo, hi = np.percentile(est, [2.5, 97.5])
    return np.exp(pt), np.exp(lo), np.exp(hi)

# headline association: undiagnosed diabetes ~ rural (among biochemically diabetic)
d1 = df[df["biochem_diab"] == 1][["undx_diab", "residence", "age_years", "sex", "education_years", W, "clust"]].dropna()
orr, lo, hi = cluster_boot_glm(d1, "undx_diab ~ C(residence) + age_years + C(sex) + education_years",
                               "C(residence)[T.urban]")
print(f"\n[bootstrap] Undiagnosed diabetes, urban vs rural OR = {orr:.3f} ({lo:.3f}-{hi:.3f})")

# incremental delta-AUROC bootstrap (M3 self-report vs M4 +biomarker burden)
cols = ["hospitalised_12m", "age_years", "sex", "residence", "education_years", "poverty",
        "current_smoking", "unclean_cooking_fuel", "chronic_condition_count", "subclinical_burden", W, "clust"]
dd = df[cols].dropna()
f3 = ("hospitalised_12m ~ age_years + C(sex) + C(residence) + education_years + poverty + "
      "current_smoking + unclean_cooking_fuel + chronic_condition_count")
f4 = f3 + " + subclinical_burden"
rng = np.random.default_rng(11)
clusters = dd["clust"].unique(); groups = {c: g for c, g in dd.groupby("clust")}
deltas = []
for _ in range(300):
    samp = rng.choice(clusters, len(clusters), replace=True)
    b = pd.concat([groups[c] for c in samp], ignore_index=True)
    if b["hospitalised_12m"].nunique() < 2: continue
    m3 = smf.glm(f3, data=b, family=sm.families.Binomial(), freq_weights=b[W]).fit()
    m4 = smf.glm(f4, data=b, family=sm.families.Binomial(), freq_weights=b[W]).fit()
    a3 = roc_auc_score(b["hospitalised_12m"], m3.predict(b))
    a4 = roc_auc_score(b["hospitalised_12m"], m4.predict(b))
    deltas.append(a4 - a3)
dlo, dhi = np.percentile(deltas, [2.5, 97.5])
print(f"[bootstrap] delta-AUROC (biomarker burden over self-report) = {np.mean(deltas):.4f} ({dlo:.4f}-{dhi:.4f})")

rob = pd.DataFrame([
    {"quantity": "Undiagnosed diabetes urban-vs-rural OR (cluster bootstrap)", "estimate": f"{orr:.2f} ({lo:.2f}-{hi:.2f})"},
    {"quantity": "delta-AUROC biomarker burden over self-report (cluster bootstrap)", "estimate": f"{np.mean(deltas):.4f} ({dlo:.4f}-{dhi:.4f})"},
])
rob.to_csv(os.path.join(T, "t_S3_bootstrap_robustness.csv"), index=False)
print("\nSaved t_S3_bootstrap_robustness.csv")
