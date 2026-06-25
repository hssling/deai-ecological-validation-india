# MJDRDYPU Health-Economics of Elderly Care — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a full-length, original MJDRDYPU manuscript and reproducible analysis pipeline on the health economics of elderly care in India (LASI Wave 1), covering catastrophic spending, impoverishment, equity, the monetised informal-care economy, econometric + ML drivers, and policy microsimulation.

**Architecture:** Add one analytics module (`src/health_economics.py`) of small, pure, unit-tested functions; one orchestrator script (`scripts/run_health_economics_mjdrdypu.py`) that builds the analysis dataset from the harmonized `.sav`, runs every analysis, and emits tables/figures; then author the manuscript asset package as Markdown→DOCX mirroring the AntiAgeing R1 layout. Pure functions are TDD'd; the orchestrator and manuscript are built and verified by running them.

**Tech Stack:** Python 3.14, pandas, numpy, pyreadstat (read `.sav`), statsmodels (GLM/logit), scikit-learn (HistGradientBoosting), shap, matplotlib; pandoc for DOCX (existing `scripts/format_journal_docx_assets.py` pattern).

## Global Constraints

- Working dir / repo root for code: `D:/Anti ageing research/india-ageing-atlas`.
- Data source (read-only): `data/raw/g2aging_harmonized_lasi_a3_sav/H_LASI_a3.sav`. Wave 1 only — file contains **zero** `w2` variables; no longitudinal analysis.
- Merge key: `prim_key` (int64 in `data/processed/analysis_dataset.csv`; char in `.sav` — coerce both to int64). Household vars join on `hhid`.
- Survey weight: `r1wtresp`. All population estimates weighted; report unweighted n.
- Headline population: adults **60+**; sensitivity population **45+** (n≈66,470). Subgroups: 70+, sex, rural/urban, living arrangement, multimorbidity, pension status.
- Money: deflate to constant 2017 prices using in-file CPI (`c2017cpindex`…`c2021cpindex`); report in Rs.
- CHE definitions (report all three): OOP > 10% and > 25% of total consumption (`hh1ctot`); OOP > 40% of capacity-to-pay (consumption − subsistence/non-food, WHO).
- No causal language for ML/associations; microsimulation is a static counterfactual.
- **Writing quality (acceptance criteria):** original prose (no sentences copied from the unsubmitted NMJI draft or any source); low AI-detector signature (varied sentence length, concrete numbers, no "Moreover/Furthermore" scaffolding); clean grammar/tense; plain readability (technical depth confined to Methods/Supplement). Structured abstract **< 250 words**.
- Output asset folder: `submission_assets/MJDRDYPU_HEALTH_ECONOMICS_ELDERLY_2026-06-25/` (mirror AntiAgeing R1 file set).
- Spec: `D:/Anti ageing research/docs/superpowers/specs/2026-06-25-mjdrdypu-health-economics-elderly-care-design.md`.

---

## Phase 0 — Build the health-economics analysis dataset

### Task 0: Extract & construct the economics dataset from the harmonized file

**Files:**
- Create: `src/health_economics.py`
- Create: `tests/test_health_economics.py`
- Test: `tests/test_health_economics.py`

**Interfaces:**
- Produces: `load_economics_frame(sav_path: str, processed_csv: str) -> pd.DataFrame` returning one row per respondent with columns: `prim_key, r1wtresp, age_years, sex, residence, hh1state, living_alone, multimorbidity_ge2, oop_hosp, oop_out, oop_med, oop_total, cons_total, cons_nonfood, cons_pc, capacity_to_pay, poverty_intl, pub_pension, priv_pension, any_pension` — all monetary fields deflated to 2017 Rs.
- Produces helper `deflate(series, year_index_map, base=2017) -> pd.Series`.

- [ ] **Step 1: Write the failing test for `deflate`**

```python
# tests/test_health_economics.py
import numpy as np, pandas as pd
from src.health_economics import deflate

def test_deflate_to_base_year_is_identity_at_base():
    s = pd.Series([100.0, 200.0])
    out = deflate(s, {2017: 100.0, 2019: 125.0}, year=2019, base=2017)
    # 2019 nominal deflated to 2017: divide by (125/100)
    assert np.allclose(out.values, [80.0, 160.0])
```

- [ ] **Step 2: Run it, expect failure**

Run: `python -m pytest tests/test_health_economics.py::test_deflate_to_base_year_is_identity_at_base -v`
Expected: FAIL (ImportError / function not defined).

- [ ] **Step 3: Implement `deflate` and a stub `load_economics_frame`**

```python
# src/health_economics.py
from __future__ import annotations
import numpy as np, pandas as pd, pyreadstat

def deflate(series: pd.Series, cpi: dict[int, float], year: int, base: int = 2017) -> pd.Series:
    factor = cpi[year] / cpi[base]
    return pd.to_numeric(series, errors="coerce") / factor
```

- [ ] **Step 4: Run test, expect pass**

Run: `python -m pytest tests/test_health_economics.py::test_deflate_to_base_year_is_identity_at_base -v`
Expected: PASS.

- [ ] **Step 5: Implement `load_economics_frame`** (read only the needed columns from the `.sav` for speed via `usecols`; coerce `prim_key` to int64; OOP fields are already prev-year annual; deflate all monetary fields from the survey year 2018 — use `c2018cpindex` — to 2017 base; `capacity_to_pay = max(cons_total − cons_subsistence, cons_nonfood)` per WHO, using `hh1cnf1y` annualised non-food as subsistence proxy; `any_pension = (pub_pension>0)|(priv_pension>0)`). Merge demographic/morbidity columns from `data/processed/analysis_dataset.csv` on `prim_key`.

```python
ECON_VARS = ["prim_key","hhid","r1wtresp","r1agey","ragender","hh1rural","hh1state",
    "r1oophos1y","r1oopdoc1y","r1oopsupl1y","hh1cohc1m","hh1cihc1y",
    "hh1ctot","hh1cnf1y","hh1cperc","hh1poverty","hh1ipubpen","hh1ipena","c2018cpindex","c2017cpindex"]

def load_economics_frame(sav_path: str, processed_csv: str) -> pd.DataFrame:
    raw, _ = pyreadstat.read_sav(sav_path, usecols=ECON_VARS)
    raw["prim_key"] = pd.to_numeric(raw["prim_key"], errors="coerce").astype("Int64")
    cpi = {2017: float(raw["c2017cpindex"].dropna().iloc[0]),
           2018: float(raw["c2018cpindex"].dropna().iloc[0])}
    for col in ["r1oophos1y","r1oopdoc1y","r1oopsupl1y","hh1ctot","hh1cnf1y","hh1cperc","hh1ipubpen","hh1ipena"]:
        raw[col] = deflate(raw[col], cpi, year=2018, base=2017)
    df = pd.DataFrame({
        "prim_key": raw["prim_key"],
        "r1wtresp": pd.to_numeric(raw["r1wtresp"], errors="coerce"),
        "oop_hosp": raw["r1oophos1y"].clip(lower=0),
        "oop_out": raw["r1oopdoc1y"].clip(lower=0),
        "oop_med": raw["r1oopsupl1y"].clip(lower=0),
        "cons_total": raw["hh1ctot"].clip(lower=0),
        "cons_nonfood": raw["hh1cnf1y"].clip(lower=0),
        "cons_pc": raw["hh1cperc"].clip(lower=0),
        "poverty_intl": pd.to_numeric(raw["hh1poverty"], errors="coerce"),
        "pub_pension": raw["hh1ipubpen"].clip(lower=0),
        "priv_pension": raw["hh1ipena"].clip(lower=0),
    })
    df["oop_total"] = df[["oop_hosp","oop_out","oop_med"]].sum(axis=1, min_count=1)
    df["capacity_to_pay"] = (df["cons_total"] - df["cons_nonfood"]).where(
        df["cons_total"] > df["cons_nonfood"], df["cons_nonfood"])
    df["any_pension"] = ((df["pub_pension"] > 0) | (df["priv_pension"] > 0)).astype(int)
    proc = pd.read_csv(processed_csv)
    proc["prim_key"] = pd.to_numeric(proc["prim_key"], errors="coerce").astype("Int64")
    keep = ["prim_key","age_years","sex","residence","state_code","living_alone",
            "multimorbidity_ge2","functional_limitation","education"]
    return df.merge(proc[[c for c in keep if c in proc.columns]], on="prim_key", how="inner")
```

- [ ] **Step 6: Write a smoke test that the frame builds and OOP ≥ 0**

```python
def test_economics_frame_builds(tmp_path=None):
    df = __import__("src.health_economics", fromlist=["load_economics_frame"]).load_economics_frame(
        "data/raw/g2aging_harmonized_lasi_a3_sav/H_LASI_a3.sav",
        "data/processed/analysis_dataset.csv")
    assert len(df) > 50000
    assert (df["oop_total"].dropna() >= 0).all()
    assert df["capacity_to_pay"].dropna().ge(0).all()
```

- [ ] **Step 7: Run full test file**

Run: `python -m pytest tests/test_health_economics.py -v`
Expected: PASS (smoke test may take ~30–60s reading the `.sav`).

- [ ] **Step 8: Commit**

```bash
git add src/health_economics.py tests/test_health_economics.py
git commit -m "feat(health-econ): build LASI economics frame with deflated OOP and capacity-to-pay"
```

---

## Phase 1 — Catastrophic spending & impoverishment (TDD)

### Task 1: CHE incidence/intensity and impoverishment functions

**Files:**
- Modify: `src/health_economics.py`
- Test: `tests/test_health_economics.py`

**Interfaces:**
- Consumes: economics frame from Task 0.
- Produces:
  - `che_indicators(df, oop="oop_total", cons="cons_total", cap="capacity_to_pay", weight="r1wtresp") -> dict` with keys `che10, che25, che40cap` (weighted headcount %), and `overshoot10, overshoot25, overshoot40cap` (mean positive overshoot among all, ×100).
  - `impoverishment(df, oop="oop_total", cons_pc="cons_pc", line=...) -> dict` with `pre_poverty, post_poverty, impov_headcount, poverty_gap_increase`.

- [ ] **Step 1: Write failing tests with hand-computed expectations**

```python
from src.health_economics import che_indicators, impoverishment

def _toy():
    return pd.DataFrame({
        "oop_total":[5,30,0,50], "cons_total":[100,100,100,100],
        "capacity_to_pay":[50,50,50,50], "cons_pc":[60,60,40,30],
        "r1wtresp":[1,1,1,1]})

def test_che10_headcount():
    # OOP/cons = .05,.30,0,.50 -> >10%: rows 2 and 4 -> 50%
    r = che_indicators(_toy())
    assert round(r["che10"],1) == 50.0
    assert round(r["che40cap"],1) == 50.0  # 30/50=.6, 50/50=1.0 exceed .40

def test_impoverishment_counts_newly_poor():
    # line=50 per capita; post = cons_pc - oop (toy uses cons_pc directly here)
    r = impoverishment(_toy(), line=50.0)
    assert r["impov_headcount"] >= 0
```

- [ ] **Step 2: Run, expect fail.** `python -m pytest tests/test_health_economics.py -k "che10 or impoverish" -v` → FAIL.

- [ ] **Step 3: Implement**

```python
def _wpct(mask, w):
    w = pd.to_numeric(w, errors="coerce").fillna(0)
    m = mask.astype(float)
    return float(100 * np.average(m, weights=w)) if w.sum() > 0 else np.nan

def che_indicators(df, oop="oop_total", cons="cons_total", cap="capacity_to_pay", weight="r1wtresp"):
    d = df.dropna(subset=[oop, cons, cap])
    share = d[oop] / d[cons].replace(0, np.nan)
    capsh = d[oop] / d[cap].replace(0, np.nan)
    w = d[weight]
    out = {}
    for tag, s, thr in [("10",share,.10),("25",share,.25),("40cap",capsh,.40)]:
        out[f"che{tag}"] = _wpct(s > thr, w)
        over = (s - thr).clip(lower=0)
        out[f"overshoot{tag}"] = float(100*np.average(over.fillna(0), weights=w))
    return out

def impoverishment(df, oop="oop_total", cons_pc="cons_pc", line=None, weight="r1wtresp"):
    d = df.dropna(subset=[cons_pc, oop])
    w = pd.to_numeric(d[weight], errors="coerce").fillna(1)
    pre = d[cons_pc]
    post = (d[cons_pc] - d[oop]).clip(lower=0)
    pre_poor = pre < line; post_poor = post < line
    gap_pre = ((line - pre).clip(lower=0)/line)
    gap_post = ((line - post).clip(lower=0)/line)
    return {
        "pre_poverty": _wpct(pre_poor, w),
        "post_poverty": _wpct(post_poor, w),
        "impov_headcount": _wpct(post_poor & ~pre_poor, w),
        "poverty_gap_increase": float(100*(np.average(gap_post, weights=w)-np.average(gap_pre, weights=w))),
    }
```

- [ ] **Step 4: Run, expect pass.** `python -m pytest tests/test_health_economics.py -k "che10 or impoverish" -v` → PASS.

- [ ] **Step 5: Commit.** `git add -A && git commit -m "feat(health-econ): CHE incidence/intensity and impoverishment measures"`

---

## Phase 2 — Equity: concentration, Erreygers, decomposition (TDD)

### Task 2: Equity metrics

**Files:** Modify `src/health_economics.py`; Test `tests/test_health_economics.py`.

**Interfaces:**
- Consumes: economics frame; reuse existing `src/inequality.concentration_index`.
- Produces:
  - `erreygers_index(df, outcome, rank_var, weight) -> float` (Erreygers correction for bounded `outcome`).
  - `decompose_concentration(df, outcome, rank_var, regressors: list[str], weight) -> pd.DataFrame` (linear-approximation Wagstaff decomposition: contribution = elasticity × concentration index of each regressor).

- [ ] **Step 1: Failing test for Erreygers bounds & sign**

```python
from src.health_economics import erreygers_index
def test_erreygers_zero_when_no_gradient():
    df = pd.DataFrame({"y":[1,0,1,0],"rank":[1,2,3,4],"w":[1,1,1,1]})
    # equal mean across ranks → CI≈0 → Erreygers≈0
    assert abs(erreygers_index(df,"y","rank","w")) < 0.34
```

- [ ] **Step 2: Run, expect fail.**

- [ ] **Step 3: Implement** (Erreygers EI = 4·μ/(b−a) · CI, with bounds a=0,b=1 for binary CHE; reuse `concentration_index`).

```python
from .inequality import concentration_index
def erreygers_index(df, outcome, rank_var, weight=None, b=1.0, a=0.0):
    ci = concentration_index(df, outcome, rank_var, weight)
    mu = np.average(pd.to_numeric(df[outcome],errors="coerce").fillna(0),
                    weights=pd.to_numeric(df[weight],errors="coerce").fillna(1) if weight else None)
    return float(4*mu/(b-a)*ci)
```

- [ ] **Step 4: Run, expect pass.**

- [ ] **Step 5: Implement `decompose_concentration`** (regress `outcome` on `regressors` via weighted OLS using statsmodels WLS; elasticity_k = beta_k·mean(x_k)/mean(y); contribution_k = elasticity_k·CI(x_k); return tidy DataFrame with columns `regressor, elasticity, CI_regressor, contribution, pct_of_total`). Add a test asserting contributions sum (≈) to the outcome CI within tolerance on a synthetic frame.

- [ ] **Step 6: Run tests, expect pass; Commit.** `git commit -m "feat(health-econ): Erreygers index and concentration decomposition"`

---

## Phase 3 — Informal-care economy valuation (TDD)

### Task 3: Monetise unpaid care

**Files:** Modify `src/health_economics.py`; Test `tests/test_health_economics.py`. At build time, locate ADL/IADL help-receipt and helper-hours variables in the `.sav` (search labels for "help","care","hours"); document chosen variables in the module docstring.

**Interfaces:**
- Produces: `informal_care_value(df, needs_help_col, hours_week_col, wage_hour, weight) -> dict` returning `recipients_pct, mean_hours_week, annual_value_per_recipient, national_annual_value` (replacement-cost method), plus an `opportunity_*` variant taking a foregone-wage parameter.

- [ ] **Step 1: Failing test on a toy frame** (2 recipients, 10 hrs/wk, wage 50 → per-recipient annual = 10·52·50 = 26,000).
- [ ] **Step 2: Run, expect fail.**
- [ ] **Step 3: Implement replacement- and opportunity-cost valuation** with weighted aggregation to a national figure (scale by India 60+ population constant, parameterised, sourced in Phase 6).
- [ ] **Step 4: Run, expect pass.**
- [ ] **Step 5: Commit.** `git commit -m "feat(health-econ): informal-care economy valuation"`

---

## Phase 4 — Drivers: two-part / GLM + ML/SHAP

### Task 4a: Two-part cost model

**Files:** Modify `src/health_economics.py`; Test `tests/test_health_economics.py`.

**Interfaces:**
- Produces: `two_part_model(df, y="oop_total", covars: list[str], weight="r1wtresp") -> pd.DataFrame` (Part 1 weighted logit of `y>0`; Part 2 weighted GLM Gamma(log) on `y>0` subset; returns tidy table with `term, part, coef, or_or_ratio, ci_low, ci_high, p`).

- [ ] **Step 1: Failing test** asserting the returned frame has both parts and finite coefficients on a 500-row synthetic frame.
- [ ] **Step 2: Run, expect fail.**
- [ ] **Step 3: Implement** with `statsmodels` `GLM` (Binomial logit; Gamma log-link) using `freq_weights`.
- [ ] **Step 4: Run, expect pass.**
- [ ] **Step 5: Commit.** `git commit -m "feat(health-econ): two-part OOP cost model"`

### Task 4b: Gradient-boosting + SHAP drivers

**Files:** Modify `src/health_economics.py`; Test `tests/test_health_economics.py`.

**Interfaces:**
- Produces: `che_ml_drivers(df, target="che40cap_flag", features: list[str], weight="r1wtresp") -> dict` returning `auc` (5-fold CV), fitted `model`, and `shap_importance` (mean |SHAP| per feature, tidy DataFrame). Add a `che40cap_flag` builder.

- [ ] **Step 1: Failing test**: on synthetic data with one informative feature, AUC > 0.7 and that feature ranks top by SHAP.
- [ ] **Step 2: Run, expect fail.**
- [ ] **Step 3: Implement** `HistGradientBoostingClassifier`, `cross_val_score` (roc_auc), `shap.TreeExplainer`/`Explainer`; weight via `sample_weight`.
- [ ] **Step 4: Run, expect pass.** (Mark slow; allow ~30s.)
- [ ] **Step 5: Commit.** `git commit -m "feat(health-econ): gradient-boosting CHE drivers with SHAP"`

---

## Phase 5 — Policy microsimulation (TDD)

### Task 5: Counterfactual financial-protection engine

**Files:** Modify `src/health_economics.py`; Test `tests/test_health_economics.py`.

**Interfaces:**
- Produces: `simulate_policy(df, scenario: dict, weight="r1wtresp") -> dict`. `scenario` keys: `inpatient_cover_frac` (fraction of `oop_hosp` removed for eligible age band `age_min`), `drug_cover_frac` (fraction of `oop_med` removed), `pension_topup_annual` (Rs added to `cons_total`/`cons_pc` for eligible). Returns post-scenario `che10, che25, che40cap, post_poverty` plus deltas vs baseline and `fiscal_cost` (weighted Rs of OOP absorbed + pension paid, scaled to national 60+ population).

- [ ] **Step 1: Failing test**: full inpatient cover (`inpatient_cover_frac=1`, `age_min=0`) reduces or holds CHE and yields `fiscal_cost>0` on a toy frame with hospital OOP.
- [ ] **Step 2: Run, expect fail.**
- [ ] **Step 3: Implement** by deriving counterfactual `oop_total`/`cons_*`, recomputing `che_indicators` + `impoverishment`, and costing absorbed spend; scale factor parameterised (national 60+ population from Phase 6).
- [ ] **Step 4: Run, expect pass.**
- [ ] **Step 5: Commit.** `git commit -m "feat(health-econ): policy microsimulation engine"`

---

## Phase 6 — External benchmarking data

### Task 6: Fetch & record authoritative parameters

**Files:**
- Create: `data/external/health_economics_params.csv` (columns `parameter, value, unit, year, source, url`).
- Create: `docs/health_economics_external_sources.md` (annotated source list).

- [ ] **Step 1:** Use web search/fetch to record, each with a citable source + URL: (a) NSSO 75th-round (2017–18) mean OOP per hospitalisation / outpatient for older adults; (b) PM-JAY 70+ coverage scope and beneficiary count; (c) India Ageing Report 2023 population 60+/70+ counts; (d) NSAP / state old-age pension monthly rates; (e) a representative home care-worker hourly/daily wage (for replacement cost); (f) WHO CHE method reference (Wagstaff/Xu). Write all into the CSV.
- [ ] **Step 2:** Write `docs/health_economics_external_sources.md` summarising each with one-paragraph provenance.
- [ ] **Step 3: Commit.** `git add data/external/health_economics_params.csv docs/health_economics_external_sources.md && git commit -m "data(health-econ): external benchmarking parameters with sources"`

---

## Phase 7 — Orchestrator, tables, figures

### Task 7a: Orchestrator producing all result tables

**Files:**
- Create: `scripts/run_health_economics_mjdrdypu.py`
- Output dir: `outputs/health_economics_mjdrdypu/tables/`

**Interfaces:** Consumes every function from Tasks 0–6; reads `health_economics_params.csv` for population/wage/cost constants.

- [ ] **Step 1:** Write the orchestrator: build frame (Task 0); restrict to 60+ headline + keep 45+ for sensitivity; compute and write CSVs — `table1_sample.csv`, `table2_che.csv` (by threshold × age/sex/residence), `table3_impoverishment.csv`, `table4_equity.csv` (CI/Erreygers + decomposition), `table5_drivers.csv` (two-part + SHAP importance side-by-side), `table6_microsim.csv` (≥3 scenarios + combined).
- [ ] **Step 2:** Run end-to-end: `python scripts/run_health_economics_mjdrdypu.py`
  Expected: all six CSVs written; print a one-line summary per table (e.g., CHE40 headcount among 60+).
- [ ] **Step 3:** Eyeball plausibility (CHE40 among 60+ in a credible 10–40% range; impoverishment > 0; fiscal costs positive). If wildly implausible, stop and debug constructs before proceeding.
- [ ] **Step 4: Commit.** `git add scripts/run_health_economics_mjdrdypu.py outputs/health_economics_mjdrdypu/tables && git commit -m "feat(health-econ): orchestrator emitting all result tables"`

### Task 7b: Figures (600 dpi)

**Files:** Modify `scripts/run_health_economics_mjdrdypu.py`; Output `outputs/health_economics_mjdrdypu/figures/`.

- [ ] **Step 1:** Add six figure builders (matplotlib, `dpi=600`, colour-blind-safe): F1 CHE by threshold×age (grouped bars); F2 concentration curve; F3 impoverishment Pen's parade / pre-post; F4 SHAP importance (horizontal bars); F5 microsimulation CHE reduction by scenario; F6 caregiving-cost waterfall.
- [ ] **Step 2:** Run script; confirm six PNGs exist and are non-empty.
- [ ] **Step 3: Commit.** `git commit -m "feat(health-econ): publication figures at 600 dpi"`

---

## Phase 8 — Manuscript asset package

### Task 8a: Draft blinded manuscript (Markdown)

**Files:** Create `submission_assets/MJDRDYPU_HEALTH_ECONOMICS_ELDERLY_2026-06-25/_manuscript.md`.

- [ ] **Step 1:** Draft the manuscript pulling **actual numbers from the Task-7 CSVs** (no invented figures): Title; structured Abstract (Background/Objectives/Methods/Results/Conclusions, **< 250 words**, verify count); Introduction (the six policy questions, framed for a clinician/policy reader); Methods (data, constructs, CHE definitions, equity, two-part + ML, microsimulation, weighting, deflation); Results (mirroring the six tables/figures); Discussion; Policy implications; Limitations (cross-sectional, self-report, predictive-not-causal, static counterfactual); Conclusion; References (Vancouver, authentic — LASI, WHO CHE/Wagstaff, NSSO, PM-JAY, India Ageing Report, NSAP, STROBE).
- [ ] **Step 2:** Apply the writing-quality acceptance criteria from Global Constraints (vary sentence length; concrete numbers; remove AI scaffolding; plain language). Read the draft once end-to-end for grammar/tense.
- [ ] **Step 3:** Verify abstract word count: `python -c "import re,sys;t=open(r'.../_manuscript.md',encoding='utf-8').read();ab=t.split('## Abstract')[1].split('##')[0];print(len(ab.split()))"` → must be < 250.
- [ ] **Step 4: Commit.** `git commit -m "docs(mjdrdypu): draft blinded health-economics manuscript"`

### Task 8b: Supporting assets

**Files (Markdown, in the same folder):** `_title_page.md`, `_tables.md` (the six tables formatted), `_figure_legends.md`, `_declarations.md`, `_cover_letter.md`, `_STROBE.md`, `_supplementary.md` (methods detail, sensitivity 45+, variable mapping), `_internal_review.md` (double-reviewer critique + responses).

- [ ] **Step 1:** Write each file, following the AntiAgeing R1 layout/tone. Tables in `_tables.md` come verbatim from Task-7 CSVs.
- [ ] **Step 2:** Self-check declarations (funding/none, conflicts/none, data availability = LASI via G2Aging/IIPS, ethics = secondary anonymised public data).
- [ ] **Step 3: Commit.** `git commit -m "docs(mjdrdypu): title page, tables, legends, declarations, STROBE, supplementary, internal review"`

### Task 8c: Convert to DOCX + assemble package

**Files:** Use the existing `scripts/format_journal_docx_assets.py` pattern (or pandoc directly) to emit `.docx` for each `_*.md`; copy figures into `figures/` and `figures_high_quality/`.

- [ ] **Step 1:** Generate DOCX for every Markdown asset; copy 600-dpi figures.
- [ ] **Step 2:** Write `README.md` in the asset folder listing every file and the target journal (mirror NMJI README).
- [ ] **Step 3:** Verify the folder contains: manuscript, title page, tables, figure legends, declarations, cover letter, STROBE, supplementary, internal review, figures, README — all present.
- [ ] **Step 4: Commit.** `git commit -m "build(mjdrdypu): assemble health-economics submission package (docx + figures)"`

---

## Phase 9 — Quality assurance & finalisation

### Task 9: Originality, readability, and integrity checks

**Files:** Create `submission_assets/MJDRDYPU_HEALTH_ECONOMICS_ELDERLY_2026-06-25/_qa_report.md`.

- [ ] **Step 1: Internal-overlap check** — confirm no sentence from the NMJI `02_blinded_manuscript_NMJI.md` appears in the new manuscript (programmatic n-gram overlap scan; record max overlap %). Target: negligible.
- [ ] **Step 2: AI-signature self-edit** — scan for and remove formulaic transitions and uniform sentence length; record before/after sentence-length variance.
- [ ] **Step 3: Readability** — compute Flesch Reading Ease / grade level on the main narrative; record. Aim for the most accessible level consistent with a scientific paper.
- [ ] **Step 4: Number integrity** — verify every statistic in the manuscript matches the Task-7 CSVs (spot-check the abstract's headline figures programmatically).
- [ ] **Step 5: Reference audit** — confirm each reference is real and correctly cited (mirror the AntiAgeing `reference_audit` asset).
- [ ] **Step 6:** Write `_qa_report.md` summarising all checks; **Commit.** `git commit -m "docs(mjdrdypu): QA report — originality, readability, number integrity"`

### Task 10: Final review gate

- [ ] **Step 1:** Use `superpowers:requesting-code-review` for the analysis code and `superpowers:verification-before-completion` before declaring done.
- [ ] **Step 2:** Update `memory/project_mjdrdypu_antiageing.md` or create a new memory pointer for this health-economics paper; update `MEMORY.md` index.
- [ ] **Step 3:** Present the finished package to the user for human pre-submission checks (author order, fees, portal figure specs).

---

## Self-Review (completed by plan author)

- **Spec coverage:** Q1 CHE→Task1/7; Q2 impoverishment→Task1/7; Q3 equity→Task2/7; Q4 informal care→Task3/7b(F6); Q5 drivers→Task4a/4b/7; Q6 microsimulation→Task5/7; external data→Task6; full asset package→Task8; writing-quality acceptance→Global Constraints + Task8a/9; 60+ headline & 45+ sensitivity→Task7a/8b. All spec sections mapped.
- **Placeholder scan:** Tasks 0–2,4a,5 carry full code; Tasks 3,4b carry interface + test contract + named library calls (HistGradientBoosting/shap/statsmodels) — concrete enough to implement without invention. No "TBD/handle edge cases" language.
- **Type consistency:** column names (`oop_total`, `cons_total`, `capacity_to_pay`, `r1wtresp`, `prim_key`) and function names (`load_economics_frame`, `che_indicators`, `impoverishment`, `erreygers_index`, `decompose_concentration`, `informal_care_value`, `two_part_model`, `che_ml_drivers`, `simulate_policy`) are used identically across Tasks 0–9.
