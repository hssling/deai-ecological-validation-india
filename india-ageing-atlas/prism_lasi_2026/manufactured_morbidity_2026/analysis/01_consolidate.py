"""
Manufactured morbidity: consolidate the full grid of PRISm / RSP / obstruction
prevalence across every reference equation x definition already computed in the
Lung India revision and the national reference-equation paper, and quantify the
range (fold-change) attributable to reference choice alone.

No new modelling: this paper's contribution is the synthesis and its message.
"""
import json
import os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(HERE, "..", ".."))          # prism_lasi_2026/
REV = os.path.join(BASE, "LungIndia_revised_2026-07-08", "outputs", "tables",
                   "t_reference_comparison.csv")
REVKEY = os.path.join(BASE, "LungIndia_revised_2026-07-08", "outputs", "key_numbers_v2.json")
NATKEY = os.path.join(BASE, "national_ref_equations_2026", "outputs", "key_numbers.json")
OUT = os.path.abspath(os.path.join(HERE, "..", "outputs"))
os.makedirs(OUT, exist_ok=True)

rev = pd.read_csv(REV)
revk = json.load(open(REVKEY))
natk = json.load(open(NATKEY))

# ---- master prevalence grid (PRISm + RSP), all references x definitions ----
rows = []
label_map = {
    "GLI-2012 fixed": ("GLI-2012 South-East Asian", "Fixed", "Global/foreign"),
    "GLI-2012 LLN": ("GLI-2012 South-East Asian", "LLN", "Global/foreign"),
    "GLI-Global 2022 (race-neutral) fixed": ("GLI-Global 2022 race-neutral", "Fixed", "Global/foreign"),
    "GLI-Global 2022 (race-neutral) LLN": ("GLI-Global 2022 race-neutral", "LLN", "Global/foreign"),
    "Chhabra-2014 fixed": ("Chhabra-2014 (N India, regional)", "Fixed", "Regional Indian"),
    "Chhabra-2014 LLN": ("Chhabra-2014 (N India, regional)", "LLN", "Regional Indian"),
    "Agarwal-2020 (India) fixed": ("Agarwal-2020 (W India, regional)", "Fixed", "Regional Indian"),
    "Agarwal-2020 (India) LLN": ("Agarwal-2020 (W India, regional)", "LLN", "Regional Indian"),
}
rr = rev.set_index("scheme")
for scheme, (ref, defn, family) in label_map.items():
    rows.append(dict(reference=ref, definition=defn, family=family,
                     PRISm=rr.loc[scheme, "PRISm_pct"], RSP=rr.loc[scheme, "RSP_pct"]))
# national LASI reference (from paper 2)
b = natk["burden"]
rows.append(dict(reference="LASI national (this programme)", definition="Fixed",
                 family="National Indian", PRISm=b["PRISm_LASI_fixed"][0], RSP=b["RSP_LASI_fixed"][0]))
rows.append(dict(reference="LASI national (this programme)", definition="LLN",
                 family="National Indian", PRISm=b["PRISm_LASI_LLN"][0], RSP=b["RSP_LASI_LLN"][0]))
# internal healthy-subset floor (from revision)
internal = float(revk["internal_reference"]["PRISm"].split()[0])
internal_rsp = float(revk["internal_reference"]["RSP"].split()[0])
rows.append(dict(reference="Internal healthy-subset (floor)", definition="LLN",
                 family="National Indian", PRISm=internal, RSP=internal_rsp))

grid = pd.DataFrame(rows).sort_values("PRISm").reset_index(drop=True)
grid.to_csv(os.path.join(OUT, "master_grid.csv"), index=False)

# ---- range / fold-change ----
def rng(col):
    lo, hi = grid[col].min(), grid[col].max()
    return dict(low=round(lo, 1), high=round(hi, 1), fold=round(hi / lo, 1),
                abs_range=round(hi - lo, 1))

key = dict(
    n_analytic=revk["n_analytic"],
    prism_range=rng("PRISm"), rsp_range=rng("RSP"),
    families=grid.groupby("family")["PRISm"].agg(["min", "max"]).round(1).to_dict("index"),
    n_scenarios=len(grid),
)
json.dump(key, open(os.path.join(OUT, "key_numbers.json"), "w"), indent=2)
print(json.dumps(key, indent=2))
print("\n== Master grid (sorted by PRISm) ==")
print(grid.to_string(index=False))
