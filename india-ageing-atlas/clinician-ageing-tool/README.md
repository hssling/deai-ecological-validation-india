# India Healthy Ageing Clinical Support

Open-access browser tool for clinicians and practitioners working with middle-aged and older Indian adults.

The first release provides:

- LASI national GAMLSS/LMS spirometry prediction for FEV1, FVC, and FEV1/FVC.
- Lower limit of normal, z-score, percent-predicted, PRISm, restrictive spirometric pattern, and obstruction flags.
- Structured healthy-ageing prompts covering respiratory symptoms, exposures, BMI, BP, glycaemia, falls, frailty, function, cognition, mood, prevention, and referral review.
- Client-side calculation only; no patient database and no server-side clinical data handling.

## Clinical Boundary

This is clinical decision support, not a diagnostic or prescribing system. It should be used with spirometry quality review, clinical examination, local guidelines, and appropriate referral pathways. LASI reference equations apply to Indian adults aged 45-90 years and should not be extrapolated to younger adults.

## Source

The respiratory calculator uses the bundled LASI GAMLSS/LMS table from:

`prism_lasi_2026/national_ref_equations_2026/reference_package/src/lasi_spirometry_reference/data/lasi_gamlss_lms_table.csv`

Citation text from the source package:

Siddalingaiah HS. Nationally Representative Spirometry Reference Equations for Middle-Aged and Older Indians: A Cross-sectional Derivation and Validation Study from the Longitudinal Ageing Study in India, and Re-estimated Burden of Restrictive and Preserved-Ratio Impairment.

## Acknowledgements

This tool uses reference equations derived from public-use Longitudinal Ageing Study in India Wave 1 data, conducted by the International Institute for Population Sciences with the Harvard T.H. Chan School of Public Health and the University of Southern California, supported by the Ministry of Health and Family Welfare, Government of India. We thank the LASI investigators and participants.

Concept, design, and creation: **Dr Siddalingaiah H S, MD**, Professor, Department of Community Medicine, Shridevi Institute of Medical Sciences and Research Hospital, Tumkur, Karnataka, India. ORCID: 0000-0002-4771-8285.

## Local Use

The app is static. Serve this folder with any static server:

```bash
python3 -m http.server 4173
```

Then open `http://localhost:4173`.

## Vercel

Deploy this folder as the Vercel project root:

```bash
vercel --cwd india-ageing-atlas/clinician-ageing-tool
vercel --cwd india-ageing-atlas/clinician-ageing-tool --prod
```

For GitHub Actions CI/CD, configure these repository secrets:

- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`

The workflow at `.github/workflows/vercel-clinician-ageing-tool.yml` deploys preview builds for pull requests and production builds for pushes to the configured branch.
