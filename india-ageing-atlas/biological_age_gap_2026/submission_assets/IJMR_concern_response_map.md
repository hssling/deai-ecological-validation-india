# How the revised study addresses every IJMR reviewer concern

This internal document maps each Indian Journal of Medical Research (IJMR_1754_2026) reviewer
comment to the specific change made in the redesigned study submitted to *Discover Aging*. The
redesign does not patch the old index; it replaces the flawed construct and reframes the research
question around what the data can rigorously support.

## Root-cause summary
The rejected paper built an "integrated biological ageing vulnerability (BAV)" index that mixed
biology, function, and social vulnerability, then used social/household variables to "predict" that
same index. This produced circularity, conceptual vagueness, a weak single-construct (PC1 = 23%),
and no validation against anything external to the index. The redesign removes the index entirely.

---

## Reviewer 1

| # | Concern | How addressed |
|---|---------|---------------|
| 1 | Needs multiple data sources, hard to standardise in low-resource settings | We no longer propose a multi-domain composite for deployment. The unit of analysis is measured biomarkers already collected in a national survey (HbA1c, CRP, haemoglobin, BP, spirometry, grip, anthropometry). The policy output is the **diagnosis gap**, actionable with a single point-of-care test (HbA1c, BP cuff). |
| 2 | Frailty, functional limitation, multimorbidity overlap → double counting | These constructs are **removed from the exposure**. The biological burden score contains only directly measured biomarker abnormalities; frailty/function/multimorbidity are used only as *separate outcomes*, never as components. No double counting. |
| 3 | One-time measurement cannot capture dynamic change | Reframed explicitly as cross-sectional **prevalence and equity** of undiagnosed biological burden, not a trajectory. Longitudinal LASI Wave 2 validation named as the explicit next step. |
| 4 | Social and depression proxies measured inconsistently vs lab biomarkers | Social/psychological proxies are **dropped from the construct**. The construct is now lab/clinically measured only. Social variables appear only as predictors of measured burden. |
| 5 | Influence of environmental factors acknowledged | Environment is now a central, explicit *predictor* axis (household exposome), analysed with clean directionality rather than embedded in the outcome. |
| 6 | Urban/rural hides within-category exposome variability; no intra-state/ethnic variation | We add caste, education, wealth tertile and state-level analysis, and explicitly frame urban/rural as a coarse proxy, reporting heterogeneity. Within-state geocoded exposome named as a limitation/next step. |
| 7 | Index not tested across diverse populations → limited generalisability | We make no claim of a deployable index. Findings are descriptive-epidemiological for a nationally representative sample with design weights; generalisability is to the LASI target population, stated plainly. |

## Reviewer 2

| # | Concern | How addressed |
|---|---------|---------------|
| 1 | Inadequate justification/weighting of the composite construct | The composite is replaced by (a) clinically defined binary abnormalities with cited thresholds, and (b) an unweighted count (allostatic-load style) and Mahalanobis distance — established methods requiring no bespoke weighting. |
| 2 | Unclear whether biological age / frailty / vulnerability / surveillance | Conceptually disambiguated: we study **undiagnosed/subclinical biological burden** (prevalence + equity), not "biological age." The word "vulnerability index" is gone. |
| 3 | Missing DBS/spirometry data and selection bias not addressed | Added an explicit **included-vs-excluded comparison table** and inverse-probability-of-availability weighting as sensitivity; module-specific and biomarker weights used. |
| 4 | PCA reporting incomplete; first-PC justification weak | **PCA is removed** as the headline construct (it explained only 23%). We report a transparent count and distance measures instead; any PCA appears only as a sensitivity comparison with full loadings/variance. |
| 5 | Complex sampling not transparently handled | Design-based handling: person and biomarker weights applied per module; **SSU cluster-robust / cluster-bootstrap** variance; state×residence strata; limits of available design fields stated. |
| 6 | Prediction target/LODO rationale/AUROC interpretation unclear | The leave-one-domain-out trick is removed. We use a pre-specified **external outcome (hospitalisation)** and honest nested-model incremental value (ΔAUROC, AIC, LR), explicitly noting where biomarkers do *not* beat age. |
| 7 | Measurement error from proxies (depression, cognition, exposome) | The construct now uses **measured** biomarkers, not proxies. Proxy variables are excluded from the exposure. |

## Reviewer 3 (most severe)

| # | Concern | How addressed |
|---|---------|---------------|
| 1 | BAV defined, measured, validated in same data → external validity | The construct is now standard clinical thresholds (external, pre-defined: ADA HbA1c, JNC/WHO BP, WHO anaemia, CDC/AHA CRP), not data-derived. Validation uses outcomes **not** used to define it. |
| 2 | PCA explains only 23% → items not one construct | We **abandon the single-construct claim**. We explicitly treat ageing biology as multi-system and report markers individually + as a count, not as one latent factor. |
| 3 | Age/smoking/fuel already predict outcomes; complicated index futile | Answered head-on: measured biomarkers reveal **undiagnosed** disease that age/smoking/fuel and self-report **cannot** see — 51% of biochemical diabetes and 60% of measured hypertension are undiagnosed, concentrated in the disadvantaged. This is the precise added value of biological measurement. |
| 4 | Social indicators in index, then "predict" index → circular | **Eliminated.** Social/household variables are now only predictors of an independently, clinically defined biological outcome. No social variable enters the outcome. |
| 5 | No external validation (mortality, hospitalisation) | Validated against **hospitalisation** (past-year, measured externally to the construct) and other non-component outcomes; honest about absence of prospective mortality (Wave 2 named as next step). |
| 6 | Statistical complexity replacing contextual clarity | The redesign is deliberately **simpler and clinically interpretable**: prevalence of undiagnosed conditions, by social group, by state. |
| 7 | Mechanistic, context-free, dataset-driven | Reframed around an actionable Indian health-system problem (the diagnosis/treatment gap and its inequity) with direct policy implications for NP-NCD/Ayushman Bharat screening. |

---

## One-line rebuttal for the cover letter / future correspondence
> The previous construct was circular and unvalidated; the redesigned study removes the composite
> index, defines biological burden by established external clinical thresholds, demonstrates that
> measured biomarkers reveal large, socially patterned undiagnosed disease invisible to self-report
> and simple indicators, and validates this against an outcome (hospitalisation) external to the
> construct — turning every major criticism into a design feature.
