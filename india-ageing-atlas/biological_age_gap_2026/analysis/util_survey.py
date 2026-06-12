"""Survey-design helpers: weighted estimates with cluster (SSU) bootstrap CIs."""
import numpy as np, pandas as pd

def wmean(x, w):
    x = np.asarray(x, float); w = np.asarray(w, float)
    m = np.isfinite(x) & np.isfinite(w)
    return np.average(x[m], weights=w[m]) if m.any() else np.nan

def wprop(x, w):
    return wmean(x, w)

def cluster_bootstrap_ci(df, value_col, weight_col, cluster_col,
                         stat=wmean, n_boot=400, seed=12, alpha=0.05, subset=None):
    """Percentile CI by resampling clusters (SSUs) with replacement."""
    rng = np.random.default_rng(seed)
    d = df if subset is None else df[subset]
    d = d[[value_col, weight_col, cluster_col]].dropna(subset=[cluster_col])
    clusters = d[cluster_col].unique()
    point = stat(d[value_col], d[weight_col])
    groups = {c: g for c, g in d.groupby(cluster_col)}
    ests = []
    for _ in range(n_boot):
        samp = rng.choice(clusters, size=len(clusters), replace=True)
        parts = [groups[c] for c in samp]
        b = pd.concat(parts, ignore_index=True)
        ests.append(stat(b[value_col], b[weight_col]))
    lo, hi = np.nanpercentile(ests, [100*alpha/2, 100*(1-alpha/2)])
    return point, lo, hi

def fmt_pct(p, lo, hi):
    return f"{100*p:.1f} ({100*lo:.1f}–{100*hi:.1f})"
