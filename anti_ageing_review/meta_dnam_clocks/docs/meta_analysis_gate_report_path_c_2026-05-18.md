# Meta-Analysis Gate Report — Path-C (A3 amendment)

Generated: 2026-05-18

Effect measure: adjusted between-group mean difference on original clock scale (years for age clocks; per-year-per-year for DunedinPACE). Method: DerSimonian-Laird random-effects generic-inverse-variance. Cross-check: R meta::metagen + bayesmeta::bayesmeta. Random seed: 42.

Input: `study_level_effects_2026-05-18.csv` (k_total = 8 study-clock effects across 3 studies).


## Per-clock outcome

| Clock | k | μ_DL | 95% CI | 95% PI | τ² | I² (%) | μ_HKSJ | μ_Bayes | R cross-check |
|---|---|---|---|---|---|---|---|---|---|
| DunedinPACE | 3 | -0.0090 | [-0.1124, 0.0945] | [-1.1786, 1.1607] | 0.0057 | 79.0 | -0.0090 | 0.0192 | DL→R=-0.00895251 (yes) |
| GrimAge | 2 | gate_failed (k<3) | — | — | — | — | — | — | — |
| GrimAge2 | 1 | gate_failed (k<3) | — | — | — | — | — | — | — |
| PhenoAge | 1 | gate_failed (k<3) | — | — | — | — | — | — | — |
| Horvath | 0 | gate_failed (k<3) | — | — | — | — | — | — | — |
| Hannum | 0 | gate_failed (k<3) | — | — | — | — | — | — | — |
| PCClock | 1 | gate_failed (k<3) | — | — | — | — | — | — | — |
| DNAmTL | 0 | gate_failed (k<3) | — | — | — | — | — | — | — |

## Path-C gate verdict

- Clocks reaching k≥3 (pooled): DunedinPACE
- Clocks failing the gate (k<3): GrimAge, GrimAge2, PhenoAge, Horvath, Hannum, PCClock, DNAmTL

## Honesty notes

- Only effects with a CI or SE literally present in the source full text are pooled.
- Where a study reported Cohen's d on the original clock as the headline between-group estimate (e.g., WaziryR_2023 CALERIE), that row is recorded with metric=cohens_d_post_12mo and excluded from the primary MD pool but reported separately as SMD sensitivity.
- DunedinPACE pool mixes effects with somewhat different adjustment sets (ANCOVA on placebo/treatment for CorleyMJ_2025; full-model adjusted β for ChapnickM cohort; covariance-adjusted β for MerrillSM iPCIT). Heterogeneity is therefore expected and is reflected in τ² and the prediction interval.
- The R cross-check uses the same (value, SE) inputs; agreement within 0.01 absolute or 5% relative of the pooled point estimate is recorded as `yes`.