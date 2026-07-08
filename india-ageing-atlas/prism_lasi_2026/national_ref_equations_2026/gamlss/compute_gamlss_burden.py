"""Recompute PRISm / RSP / obstruction burden under the GAMLSS (BCCG/LMS) national
reference, from the R-scored analytic sample, and compare with the Python
quadratic reference (paper 2) and the GLI references (revision)."""
import json
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(HERE, ".."))
S = pd.read_csv(os.path.join(BASE, "outputs", "scored_gamlss.csv"))


def wprev(ind, w):
    ind = np.asarray(ind, float); w = np.asarray(w, float)
    ok = ~np.isnan(ind) & ~np.isnan(w)
    p = np.average(ind[ok], weights=w[ok]); neff = (w[ok].sum() ** 2) / np.sum(w[ok] ** 2)
    z = 1.96; den = 1 + z**2 / neff
    c = (p + z**2 / (2*neff)) / den
    h = (z*np.sqrt(p*(1-p)/neff + z**2/(4*neff**2))) / den
    return round(100*p, 1), round(100*(c-h), 1), round(100*(c+h), 1)


w = S["w"]
pres = S["fev1fvc_z"] >= -1.645
presf = S["fev1fvc"] >= 70
burden = {
    "PRISm_fixed": wprev(presf & (100*S["fev1"]/S["fev1_M"] < 80), w),
    "PRISm_LLN": wprev(pres & (S["fev1_z"] < -1.645), w),
    "RSP_fixed": wprev(presf & (100*S["fvc"]/S["fvc_M"] < 80), w),
    "RSP_LLN": wprev(pres & (S["fvc_z"] < -1.645), w),
    "Obstruction_LLN": wprev(S["fev1fvc_z"] < -1.645, w),
}
# holdout validation (from the earlier train/test proof)
val = pd.read_csv(os.path.join(HERE, "gamlss_validation.csv"))
key = dict(n=int(len(S)), method="GAMLSS BCCG (LMS: M/S/L penalized splines)",
           burden=burden,
           validation=val.to_dict("records"),
           median_fvc_z=round(float(np.nanmedian(S["fvc_z"])), 2))
json.dump(key, open(os.path.join(BASE, "outputs", "key_numbers_gamlss.json"), "w"), indent=2)
print(json.dumps(key, indent=2))
