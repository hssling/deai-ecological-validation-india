# India Healthy Ageing Clinical Support

Open-access browser tool for clinicians and practitioners working with middle-aged and older Indian adults.

The first release provides:

- LASI national GAMLSS/LMS spirometry prediction for FEV1, FVC, and FEV1/FVC.
- Lower limit of normal, z-score, percent-predicted, PRISm, restrictive spirometric pattern, and obstruction flags.
- Structured healthy-ageing prompts covering respiratory symptoms, exposures, BMI, BP, glycaemia, falls, frailty, function, cognition, mood, prevention, and referral review.
- Client-side calculation only; no patient database and no server-side clinical data handling.
- A visible roadmap for expanding into a full clinician and patient healthy ageing portal.
- A patient companion plan, follow-up planner, and local JSON export for documentation workflows.
- Mobile-friendly navigation with section highlighting, a bottom tab bar, skip link, and back-to-top control.
- Indian language patient-education support for English, Hindi, Kannada, Tamil, Telugu, and Marathi.
- Demo clinician, patient, and caregiver portal workflows with DPDP-style consent gating.
- Optional Supabase schema for authenticated profiles, assessments, follow-up tasks, consent events, and education modules.

## Portal Expansion Path

This static release can be extended into a complete portal in staged modules:

- Clinician workspace: structured assessment, care maps, referral prompts, printable documentation, and versioned evidence.
- Patient companion: plain-language reports, goals, warning symptoms, follow-up checklists, and caregiver guidance.
- Longitudinal tracker: repeated spirometry, symptoms, falls, BP, HbA1c, function, vaccination status, and patient goals across visits.
- Evidence library: LASI provenance, validation notes, guideline links, module status, and change logs.
- Governance layer: consent language, data minimisation, audit trails, role-based access if accounts are added, and expert clinical review before higher-risk recommendations.

## TODO

- Add longitudinal visit tracking for spirometry, symptoms, falls, BP, HbA1c, function, vaccination status, and patient goals.
- Build a more complete patient printable report with plain-language interpretation, warning symptoms, follow-up questions, and caregiver notes.
- Expand frailty, function, cognition, mood, nutrition, falls, medication review, and vaccination modules with validated screening fields.
- Add clinician dashboard views for domain priorities, follow-up timing, referral prompts, and documentation-ready summaries.
- Link each module to source notes, LASI provenance, validation status, guideline references, and change logs.
- Explore optional account-based portal features only after privacy, consent, audit trail, and governance requirements are defined.

## Demo Portal Accounts

The sign-in/register panel lists these demo accounts:

- Clinician: `clinician.demo@ihacs.local` / `DemoClinician#2026`
- Patient: `patient.demo@ihacs.local` / `DemoPatient#2026`
- Caregiver: `care.demo@ihacs.local` / `DemoCare#2026`

Demo accounts are for training and UI review only. Do not enter real patient identifiers in demo mode.

## Supabase Portal Backend

The calculator remains usable without Supabase. Authenticated portal persistence activates only when a runtime config is provided:

```json
{
  "supabaseUrl": "https://YOUR_PROJECT.supabase.co",
  "supabaseAnonKey": "YOUR_PUBLIC_ANON_KEY"
}
```

For local testing, create `config.json` from `config.example.json` and provide the public Supabase URL and anon key. Do not commit real project keys. If `config.json` is absent, the app stays in demo mode.

For Vercel, set these environment variables. The build script generates `config.json` during deployment:

- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`

For GitHub Actions Supabase migrations, set:

- `SUPABASE_DB_URL`: direct database URL, percent-encoded.
- `SUPABASE_POOLER_DB_URL`: recommended for CI; copy the IPv4 transaction pooler connection string from Supabase Dashboard > Connect > Transaction pooler. GitHub runners often cannot reach Supabase direct IPv6-only database hosts.

The Supabase scaffold is in `supabase/`:

- `supabase/config.toml`
- `supabase/migrations/202607130001_portal_foundation.sql`
- `supabase/migrations/202607130002_seed_education_modules.sql`

When the Supabase CLI is available, apply locally with:

```bash
supabase start
supabase db reset
```

For a hosted Supabase project, link the project and push migrations:

```bash
supabase link --project-ref YOUR_PROJECT_REF
supabase db push
```

The schema enables row-level security for profiles, assessments, follow-up tasks, and consent events. Education modules are readable when active.

## Consent and Data Protection

The portal sign-in/register form requires consent acceptance for each session. The consent language covers clinical-use limits, minimum necessary data, patient notice/consent, withdrawal options, demo-account restrictions, and the need for organisational safeguards under applicable Indian data protection requirements including the Digital Personal Data Protection Act.

## Clinical Boundary

This is clinical decision support, not a diagnostic or prescribing system. It should be used with spirometry quality review, clinical examination, local guidelines, and appropriate referral pathways. LASI reference equations apply to Indian adults aged 45-90 years and should not be extrapolated to younger adults.

## Source

The respiratory calculator uses the bundled LASI GAMLSS/LMS table from:

`prism_lasi_2026/national_ref_equations_2026/reference_package/src/lasi_spirometry_reference/data/lasi_gamlss_lms_table.csv`

Citation text from the source package:

Siddalingaiah HS. Nationally Representative Spirometry Reference Equations for Middle-Aged and Older Indians: A Cross-sectional Derivation and Validation Study from the Longitudinal Ageing Study in India, and Re-estimated Burden of Restrictive and Preserved-Ratio Impairment.

## Evidence Backbone

Current portal modules are organised around these source families:

- LASI national GAMLSS/LMS spirometry equations for Indian adults aged 45-90 years.
- WHO Integrated Care for Older People (ICOPE): person-centred assessment and pathways in primary/community care.
- WHO Decade of Healthy Ageing: intrinsic capacity, functional ability, environments, and person-centred goals.
- WHO physical activity and sedentary behaviour guidance for adults, older adults, and people with chronic conditions or disability.
- Falls-prevention logic consistent with structured falls-risk review frameworks such as CDC STEADI.

The app currently provides education, structured prompts, documentation support, and follow-up planning. It does not provide diagnosis, prescribing, automated emergency triage, or externally validated prognostic risk prediction.

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
