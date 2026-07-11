"""Apply the national LASI GAMLSS/LMS spirometry reference equations.

The bundled table contains L, M, and S values for ages 45-90 years.
Non-integer ages are linearly interpolated. Values outside 45-90 are
not extrapolated because the manuscript explicitly limits the reference
to middle-aged and older adults.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from functools import lru_cache
from importlib.resources import files
from typing import Dict, Iterable, Tuple

LMS_Z = -1.6448536269514722
PARAMETERS = {"fev1", "fvc", "fev1fvc"}
SEXES = {"M", "F"}


@dataclass(frozen=True)
class Prediction:
    sex: str
    age: float
    height_cm: float | None
    parameter: str
    median: float
    lln: float
    L: float
    M_ref: float
    S: float
    ref_height_cm: float
    height_exponent: float | None


def available_age_range() -> Tuple[int, int]:
    """Return the valid tabulated age range."""

    ages = [row["age"] for row in _load_lms()]
    return int(min(ages)), int(max(ages))


def predict(
    sex: str,
    age: float,
    height_cm: float | None,
    parameter: str,
) -> Prediction:
    """Return predicted median and LLN for one spirometry parameter.

    Parameters
    ----------
    sex:
        "M"/"F" or a common equivalent such as "male" or "female".
    age:
        Age in years. Valid range is 45-90.
    height_cm:
        Height in centimetres. Required for FEV1 and FVC; ignored for FEV1/FVC.
    parameter:
        One of "fev1", "fvc", or "fev1fvc". FEV1/FVC predictions are in percent.
    """

    sex_norm = _normalize_sex(sex)
    param_norm = _normalize_parameter(parameter)
    row = _interpolate_lms(sex_norm, age, param_norm)

    ref_height = row["refht"]
    height_exponent = None if param_norm == "fev1fvc" else row["lnht_coef"]
    median = row["M"]
    if param_norm != "fev1fvc":
        if height_cm is None:
            raise ValueError("height_cm is required for FEV1 and FVC predictions")
        median = median * (float(height_cm) / ref_height) ** height_exponent

    lln = _bccg_quantile(median, row["L"], row["S"], LMS_Z)
    return Prediction(
        sex=sex_norm,
        age=float(age),
        height_cm=None if height_cm is None else float(height_cm),
        parameter=param_norm,
        median=median,
        lln=lln,
        L=row["L"],
        M_ref=row["M"],
        S=row["S"],
        ref_height_cm=ref_height,
        height_exponent=height_exponent,
    )


def score(
    observed: float,
    sex: str,
    age: float,
    height_cm: float | None,
    parameter: str,
) -> Dict[str, float]:
    """Score an observed value against the LASI reference.

    For `parameter="fev1fvc"`, provide the observed ratio in percent. If a
    fraction such as 0.78 is supplied, it is converted to 78%.
    """

    param_norm = _normalize_parameter(parameter)
    observed_value = float(observed)
    if param_norm == "fev1fvc" and observed_value <= 1.5:
        observed_value *= 100.0

    pred = predict(sex, age, height_cm, param_norm)
    z = _bccg_z(observed_value, pred.median, pred.L, pred.S)
    return {
        "observed": observed_value,
        "predicted": pred.median,
        "lln": pred.lln,
        "z": z,
        "percent_predicted": observed_value / pred.median * 100.0,
    }


def score_spirometry(
    sex: str,
    age: float,
    height_cm: float,
    fev1_l: float,
    fvc_l: float,
) -> Dict[str, object]:
    """Score FEV1, FVC, and FEV1/FVC and return standard classifications."""

    fev1 = score(fev1_l, sex, age, height_cm, "fev1")
    fvc = score(fvc_l, sex, age, height_cm, "fvc")
    ratio_percent = float(fev1_l) / float(fvc_l) * 100.0
    ratio = score(ratio_percent, sex, age, height_cm, "fev1fvc")
    classification = classify_spirometry(fev1, fvc, ratio)
    return {
        "fev1": fev1,
        "fvc": fvc,
        "fev1fvc": ratio,
        "classification": classification,
    }


def classify_spirometry(
    fev1_score: Dict[str, float],
    fvc_score: Dict[str, float],
    ratio_score: Dict[str, float],
) -> Dict[str, bool]:
    """Classify obstruction, PRISm, and restrictive spirometric pattern."""

    obstruction_lln = ratio_score["observed"] < ratio_score["lln"]
    preserved_ratio = not obstruction_lln
    low_fev1_fixed = fev1_score["percent_predicted"] < 80.0
    low_fvc_fixed = fvc_score["percent_predicted"] < 80.0
    low_fev1_lln = fev1_score["observed"] < fev1_score["lln"]
    low_fvc_lln = fvc_score["observed"] < fvc_score["lln"]
    return {
        "obstruction_lln": obstruction_lln,
        "preserved_ratio": preserved_ratio,
        "prism_fixed": preserved_ratio and low_fev1_fixed,
        "prism_lln": preserved_ratio and low_fev1_lln,
        "rsp_fixed": preserved_ratio and low_fvc_fixed,
        "rsp_lln": preserved_ratio and low_fvc_lln,
    }


@lru_cache(maxsize=1)
def _load_lms() -> Tuple[Dict[str, float | str], ...]:
    path = files("lasi_spirometry_reference").joinpath(
        "data", "lasi_gamlss_lms_table.csv"
    )
    with path.open(newline="", encoding="utf-8") as handle:
        rows = []
        for row in csv.DictReader(handle):
            rows.append(
                {
                    "param": _normalize_parameter(row["param"]),
                    "sex": _normalize_sex(row["sex"]),
                    "refht": float(row["refht"]),
                    "lnht_coef": None
                    if row["lnht_coef"] in {"", "NA"}
                    else float(row["lnht_coef"]),
                    "age": float(row["age"]),
                    "L": float(row["L"]),
                    "M": float(row["M"]),
                    "S": float(row["S"]),
                }
            )
    return tuple(rows)


def _interpolate_lms(sex: str, age: float, parameter: str) -> Dict[str, float]:
    rows = [
        row
        for row in _load_lms()
        if row["sex"] == sex and row["param"] == parameter
    ]
    rows = sorted(rows, key=lambda item: item["age"])
    min_age, max_age = rows[0]["age"], rows[-1]["age"]
    age_value = float(age)
    if age_value < min_age or age_value > max_age:
        raise ValueError(
            f"age {age_value:g} is outside the LASI reference range "
            f"{min_age:g}-{max_age:g} years"
        )

    for row in rows:
        if row["age"] == age_value:
            return dict(row)

    lower = max(row for row in rows if row["age"] < age_value)
    upper = min(row for row in rows if row["age"] > age_value)
    weight = (age_value - lower["age"]) / (upper["age"] - lower["age"])
    out = dict(lower)
    for key in ("L", "M", "S"):
        out[key] = lower[key] + (upper[key] - lower[key]) * weight
    return out


def _bccg_z(observed: float, median: float, L: float, S: float) -> float:
    if observed <= 0:
        raise ValueError("observed spirometry value must be positive")
    if abs(L) < 1e-12:
        return math.log(observed / median) / S
    return ((observed / median) ** L - 1.0) / (L * S)


def _bccg_quantile(median: float, L: float, S: float, z: float) -> float:
    if abs(L) < 1e-12:
        return median * math.exp(S * z)
    base = 1.0 + L * S * z
    if base <= 0:
        raise ValueError("invalid BCCG quantile base; check LMS values")
    return median * base ** (1.0 / L)


def _normalize_sex(sex: str) -> str:
    value = str(sex).strip().lower()
    if value in {"m", "male", "man", "men"}:
        return "M"
    if value in {"f", "female", "woman", "women"}:
        return "F"
    raise ValueError(f"sex must be one of {sorted(SEXES)} or a common equivalent")


def _normalize_parameter(parameter: str) -> str:
    value = str(parameter).strip().lower().replace("/", "")
    aliases = {
        "fev1": "fev1",
        "fvc": "fvc",
        "fev1fvc": "fev1fvc",
        "ratio": "fev1fvc",
    }
    if value in aliases:
        return aliases[value]
    raise ValueError(f"parameter must be one of {sorted(PARAMETERS)}")
