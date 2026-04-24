"""
Construct a synthetic but epidemiologically realistic ageing cohort.

PURPOSE: Allows every downstream pipeline phase (feature engineering, DEAI
construction, modeling, explainability) to run end-to-end before real datasets
are placed in data_raw/.  All outputs are clearly labelled SYNTHETIC.

DESIGN:
- N = 5 000 simulated individuals aged 40–90
- Marginal distributions drawn from published LASI / NFHS-5 / GBD estimates
- No fabricated effect sizes: associations are generated from plausible
  parameter ranges documented in the methods; they are NOT presented as
  empirical findings.
- Seed: config.yaml → project.seed (default 42)

Variables generated:
  demographics : age, sex, education_years, ses_quintile, region
  exposome     : pm25_annual, heat_days_per_year, tobacco_ever,
                 alcohol_ever, diet_diversity_score, urban_rural
  clinical     : n_chronic_conditions, adl_difficulty_count,
                 self_rated_health (1–5), grip_strength_kg,
                 gait_speed_ms
  outcomes     : frailty_index (0–1, Rockwood-style 30-item count),
                 multimorbidity_binary, disability_binary,
                 srh_poor_binary, mortality_5yr_binary
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parents[2]))
from src.utils.logger import get_logger

logger = get_logger("synthetic_cohort")

N = 5_000


def _logistic(x: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-x))


def run(cfg: dict) -> dict:
    seed: int = cfg.get("project", {}).get("seed", 42)
    rng = np.random.default_rng(seed)
    raw_dir: Path = cfg["paths"]["data_raw"]
    out_file = raw_dir / "synthetic_cohort.parquet"

    if out_file.exists():
        df = pd.read_parquet(out_file)
        logger.info(f"Synthetic cohort already exists ({len(df)} rows) — skipping")
        return {"rows": len(df), "columns": len(df.columns),
                "local_file": str(out_file)}

    logger.info(f"Generating synthetic cohort N={N}, seed={seed}")

    # ── Demographics ─────────────────────────────────────────────────────────
    age = rng.integers(40, 91, size=N).astype(float)
    sex = rng.choice([0, 1], size=N, p=[0.52, 0.48])          # 0=female, 1=male
    education_years = np.clip(rng.normal(7, 4, N), 0, 20)
    ses_quintile = rng.choice([1, 2, 3, 4, 5], size=N,
                               p=[0.28, 0.24, 0.21, 0.16, 0.11])
    region = rng.choice(
        ["north", "south", "east", "west", "central"], size=N,
        p=[0.22, 0.20, 0.18, 0.22, 0.18]
    )

    # ── Exposome ──────────────────────────────────────────────────────────────
    # PM2.5 correlated with SES (lower SES → higher exposure) and urban/rural
    urban_rural = rng.choice([0, 1], size=N, p=[0.35, 0.65])  # 0=urban, 1=rural
    pm25_base = rng.normal(60, 25, N)                           # μg/m³ (India urban avg ~60)
    pm25_annual = np.clip(pm25_base - 15 * urban_rural + 5 * (6 - ses_quintile), 10, 200)

    heat_days_per_year = np.clip(rng.normal(45, 20, N), 0, 180)
    tobacco_ever = rng.binomial(1, 0.35 * sex + 0.10 * (1 - sex), N)
    alcohol_ever = rng.binomial(1, 0.25 * sex + 0.05 * (1 - sex), N)
    diet_diversity_score = np.clip(
        rng.normal(5, 1.5, N) + 0.2 * education_years - 0.3 * (6 - ses_quintile), 1, 9
    )

    # ── Clinical ──────────────────────────────────────────────────────────────
    # Grip strength (kg): declines with age, lower in women
    grip_strength_kg = np.clip(
        35 - 0.3 * (age - 40) - 8 * (1 - sex) + rng.normal(0, 4, N), 5, 70
    )
    gait_speed_ms = np.clip(
        1.2 - 0.01 * (age - 40) + rng.normal(0, 0.2, N), 0.2, 2.0
    )
    n_chronic_conditions = np.clip(
        rng.poisson(1.5 + 0.04 * (age - 40) + 0.3 * tobacco_ever), 0, 10
    ).astype(int)
    adl_difficulty_count = np.clip(
        rng.poisson(0.5 + 0.03 * (age - 40)), 0, 6
    ).astype(int)
    self_rated_health = np.clip(
        np.round(rng.normal(3.0 + 0.02 * (age - 40), 0.8, N)), 1, 5
    ).astype(int)

    # ── Frailty index (Rockwood 30-item proxy, 0–1) ───────────────────────────
    fi_logit = (
        -3.5
        + 0.06 * (age - 40)
        + 0.3 * tobacco_ever
        + 0.25 * (pm25_annual / 40)
        + 0.20 * (heat_days_per_year / 30)
        - 0.15 * (diet_diversity_score - 5)
        - 0.10 * (education_years - 7)
        + 0.30 * (6 - ses_quintile) / 5
        + rng.normal(0, 0.8, N)
    )
    frailty_index = np.clip(_logistic(fi_logit), 0.01, 0.90)

    # ── Binary outcomes ───────────────────────────────────────────────────────
    multimorbidity_binary = (n_chronic_conditions >= 2).astype(int)
    disability_binary = (adl_difficulty_count >= 1).astype(int)
    srh_poor_binary = (self_rated_health >= 4).astype(int)

    mortality_logit = (
        -5.0
        + 0.07 * (age - 40)
        + 0.5 * frailty_index * 5
        + 0.2 * tobacco_ever
        + rng.normal(0, 0.5, N)
    )
    mortality_5yr_binary = rng.binomial(1, _logistic(mortality_logit), N)

    df = pd.DataFrame({
        "id": [f"SYN{i:05d}" for i in range(N)],
        "synthetic_flag": True,
        # demographics
        "age_years": age,
        "sex": sex,
        "education_years": education_years,
        "ses_quintile": ses_quintile,
        "region": region,
        "urban_rural": urban_rural,
        # exposome
        "pm25_annual_ugm3": pm25_annual,
        "heat_days_per_year": heat_days_per_year,
        "tobacco_ever": tobacco_ever,
        "alcohol_ever": alcohol_ever,
        "diet_diversity_score": diet_diversity_score,
        # clinical
        "grip_strength_kg": grip_strength_kg,
        "gait_speed_ms": gait_speed_ms,
        "n_chronic_conditions": n_chronic_conditions,
        "adl_difficulty_count": adl_difficulty_count,
        "self_rated_health": self_rated_health,
        # outcomes
        "frailty_index": frailty_index,
        "multimorbidity_binary": multimorbidity_binary,
        "disability_binary": disability_binary,
        "srh_poor_binary": srh_poor_binary,
        "mortality_5yr_binary": mortality_5yr_binary,
    })

    df.to_parquet(out_file, index=False)
    logger.info(f"Synthetic cohort saved → {out_file}")
    logger.info(f"  Frailty index mean={frailty_index.mean():.3f} SD={frailty_index.std():.3f}")
    logger.info(f"  Multimorbidity prevalence={multimorbidity_binary.mean():.2%}")
    logger.info(f"  Mortality (5yr) prevalence={mortality_5yr_binary.mean():.2%}")

    return {"rows": len(df), "columns": len(df.columns), "local_file": str(out_file)}


if __name__ == "__main__":
    from src.utils.config import get_arg_config
    run(get_arg_config())
