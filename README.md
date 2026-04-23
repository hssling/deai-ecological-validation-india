# DEAI Ecological Validation in India

This repository contains the public release for the manuscript:

`Development and ecological validation of a digital exposome ageing index for healthy ageing surveillance in India using LASI Wave 1`

## Overview

The project develops a state-level Digital Exposome Ageing Index (DEAI) from publicly available LASI Wave 1 indicators and evaluates its ecological validity against ageing-related outcomes across Indian states and union territories.

DEAI is an ecological surveillance index, not a biological-age clock and not an individual-level clinical risk score.

## DEAI construction

The index uses eight adverse exposome components coded so that higher values indicate greater adverse burden:

1. no clean cooking fuel
2. poor sanitation
3. low literacy
4. tobacco use
5. heavy episodic drinking
6. poor water access
7. reported indoor pollution exposure
8. underweight prevalence

Each component is standardized as a z score after median imputation for missing state-level values. The weighted state-level score is:

`DEAI_raw(s) = sum_i(w_i * z_si)`

The standardized ecological index is:

`DEAI_Z(s) = [DEAI_raw(s) - mean(DEAI_raw)] / SD(DEAI_raw)`

Weights used in the manuscript:

- no clean cooking fuel: `0.22`
- tobacco use: `0.20`
- low literacy: `0.15`
- poor sanitation: `0.10`
- poor water access: `0.10`
- heavy episodic drinking: `0.08`
- reported indoor pollution exposure: `0.08`
- underweight prevalence: `0.07`

## Repository contents

- [tables](./tables): processed state-level outputs used in the manuscript
- [figures](./figures): manuscript figures
- [src](./src): analysis scripts used to generate scores, robustness checks, and publication figures
- [manuscript](./manuscript): current IJMR submission assets
- [notebooks](./notebooks): public notebook assets for reproducible exploration
- [kaggle](./kaggle): Kaggle dataset and notebook packaging metadata

## Key results

- Highest adverse DEAI burden: Odisha, Jharkhand, Bihar, Uttar Pradesh, Assam
- Mortality signal: nominal positive association with old-age death rate
- Multimorbidity signal: robust inverse association, interpreted as epidemiological transition and diagnostic ascertainment rather than protection
- Internal consistency: Cronbach alpha `0.688`

## Data sources

This release uses derived outputs from publicly available aggregate sources:

- LASI Wave 1 India report
- LASI Wave 1 state and UT factsheets
- NFHS-5 contextual references

Source public data remain with the original providers. This repository distributes derived reproducibility files and manuscript assets.

## Reproducibility

Primary scripts included here:

- `src/deai_real.py`
- `src/real_data_robustness.py`
- `src/publication_figures.py`

The public notebook reproduces the main descriptive ranking and robustness summaries from the released tables.

## Intended use

This release is intended for:

- public-health methods review
- ecological surveillance research
- teaching and reproducibility

It should not be used for individual prediction, patient triage, or causal inference.
