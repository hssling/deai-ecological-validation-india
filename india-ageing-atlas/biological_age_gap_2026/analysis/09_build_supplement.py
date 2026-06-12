"""Build supplementary_material.md from result tables with consistent S-numbering."""
import os, pandas as pd
HERE = os.path.dirname(__file__); T = os.path.join(HERE, "..", "outputs", "tables")
MAN = os.path.join(HERE, "..", "manuscript")

def md(f):
    p = os.path.join(T, f)
    return pd.read_csv(p).to_markdown(index=False) if os.path.exists(p) else "_[table pending]_"

doc = ["# Supplementary material\n"]
doc += ["## Table S1. Included (clock-eligible, ≥5 biomarkers) vs excluded participants\n", md("t_included_vs_excluded.csv"), ""]
doc += ["## Table S2. Inverse-probability-of-availability weighting sensitivity (max diff 0.3 pp)\n", md("t_S2_ipw_sensitivity.csv"), ""]
doc += ["## Table S3. Cluster-bootstrap robustness for key regression estimates (SSU resampling)\n", md("t_S3_bootstrap_robustness.csv"), ""]
doc += ["## Table S4. Social patterning of undiagnosed disease and high burden (weighted %)\n", md("t2_social_patterning.csv"), ""]
doc += ["## Table S5. Care cascade by social group (% of affected)\n", md("t10_cascade_by_group.csv"), ""]
doc += ["## Table S6. Domain prevalence by social group (the dual burden)\n", md("t7_dual_burden_by_group.csv"), ""]
doc += ["## Table S7. Adjusted predictors of each biological domain (odds ratios)\n", md("t8_domain_predictors.csv"), ""]
doc += ["## Table S8. State/UT surveillance: burden and undiagnosed fraction\n", md("t6_state_surveillance.csv"), ""]
doc += ["## Table S9. Biomarker–chronological age associations (weighted) — context for retiring the KDM clock\n", md("t_biomarker_age_assoc.csv"), ""]
doc += ["""## Supplementary Note S10. Why a chronological-age-calibrated biological-age clock is not the primary measure

We pre-registered an intention to compute Klemera–Doubal Method (KDM) biological age. On implementation
(faithful port of the BioAge package, sex-specific, survey-weighted training), the clock proved
ill-conditioned in these data: the characteristic variance s_BA^2 was negative and the implied biological-
age acceleration had an implausible standard deviation (~26 years), with negative convergent validity
against multi-system physiological dysregulation and allostatic load. The cause is visible in Table S9:
the LASI biomarker panel (lacking renal, hepatic and lipid chemistries) is only weakly correlated with
chronological age in this 45+ population (most r^2 < 0.05), and the population carries two opposing ageing
phenotypes — cardiometabolic excess and frailty/wasting — so a single age-anchored latent score is not
well defined. We therefore do not report KDM biological age as a primary or secondary result, and instead
use externally-thresholded abnormalities and their two clinically coherent axes. This is reported
transparently rather than omitted.
"""]
open(os.path.join(MAN, "supplementary_material.md"), "w", encoding="utf-8").write("\n".join(doc))
print("supplementary_material.md rebuilt (S1–S9 + Note S10)")
