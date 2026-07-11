# LASI spirometry reference equations

This folder makes the national LASI GAMLSS/LMS spirometry reference equations usable outside the manuscript.

It contains:

- `pyproject.toml` and `src/lasi_spirometry_reference/`: a small Python package.
- Bundled LMS data from `gamlss/gamlss_LMS_table.csv`.
- Tests against the published lookup examples.

The equations apply to Indian adults aged 45-90 years. They should not be extrapolated to younger adults, and they should be externally validated before being treated as a definitive clinical standard.

## Formula

For each sex, age, and parameter, the package reads the tabulated GAMLSS/BCCG values:

- `L`: Box-Cox skewness.
- `M`: median at the sex-specific reference height.
- `S`: coefficient of variation.
- `b`: height exponent for FEV1 and FVC.

For FEV1 and FVC:

```text
M(age, height) = M_ref(age) * (height_cm / reference_height_cm)^b
z = ((observed / M)^L - 1) / (L * S)
LLN = M * (1 + L * S * -1.6448536269514722)^(1 / L)
```

For FEV1/FVC, `M` is in percent and no height scaling is applied.

Integer ages 45-90 are tabulated. Non-integer ages are linearly interpolated between adjacent LMS rows. Ages outside 45-90 raise an error by default.

## Python

Install from PyPI:

```bash
python -m pip install lasi-spirometry-reference
```

Install locally from this folder:

```bash
python -m pip install -e .
```

Example:

```python
from lasi_spirometry_reference import predict, score_spirometry

print(predict("M", 60, 165, "fvc"))

result = score_spirometry(sex="M", age=60, height_cm=165, fev1_l=2.10, fvc_l=2.60)
print(result["classification"])
```

Run tests:

```bash
python -m pytest tests
```

## Citation

Please cite the manuscript:

Siddalingaiah HS. Nationally Representative Spirometry Reference Equations for Middle-Aged and Older Indians: A Cross-sectional Derivation and Validation Study from the Longitudinal Ageing Study in India, and Re-estimated Burden of Restrictive and Preserved-Ratio Impairment.

## Release checklist

Before public package release, confirm:

- The manuscript citation and DOI/preprint URL, once available.
- The intended license for code and reference tables.
- Whether an R package should be added later and released on GitHub, CRAN, or r-universe.
