from __future__ import annotations

import csv
import math
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LMS_Z = -1.6448536269514722


def load_rows():
    with (ROOT / "assets" / "lasi_gamlss_lms_table.csv").open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def interpolate(rows, sex, age, param):
    selected = sorted(
        (row for row in rows if row["sex"] == sex and row["param"] == param),
        key=lambda item: float(item["age"]),
    )
    exact = [row for row in selected if float(row["age"]) == age]
    if exact:
        row = exact[0]
    else:
        lower = [row for row in selected if float(row["age"]) < age][-1]
        upper = [row for row in selected if float(row["age"]) > age][0]
        weight = (age - float(lower["age"])) / (float(upper["age"]) - float(lower["age"]))
        row = dict(lower)
        for key in ("L", "M", "S"):
            row[key] = str(float(lower[key]) + (float(upper[key]) - float(lower[key])) * weight)
    return {
        "refht": float(row["refht"]),
        "lnht_coef": None if row["lnht_coef"] == "NA" else float(row["lnht_coef"]),
        "L": float(row["L"]),
        "M": float(row["M"]),
        "S": float(row["S"]),
    }


def quantile(median, l_value, s_value, z_value):
    if abs(l_value) < 1e-12:
        return median * math.exp(s_value * z_value)
    return median * (1 + l_value * s_value * z_value) ** (1 / l_value)


def predict(rows, sex, age, height, param):
    row = interpolate(rows, sex, age, param)
    median = row["M"]
    if param != "fev1fvc":
        median = median * (height / row["refht"]) ** row["lnht_coef"]
    return median, quantile(median, row["L"], row["S"], LMS_Z)


def test_reference_asset_matches_expected_shape():
    rows = load_rows()
    assert len(rows) == 276
    assert sorted({row["param"] for row in rows}) == ["fev1", "fev1fvc", "fvc"]
    assert sorted({row["sex"] for row in rows}) == ["F", "M"]
    assert {int(float(row["age"])) for row in rows} == set(range(45, 91))


def test_known_reference_examples_match_package_readme():
    rows = load_rows()
    fvc_m, fvc_lln = predict(rows, "M", 60, 165, "fvc")
    fev1_m, fev1_lln = predict(rows, "M", 60, 165, "fev1")
    assert round(fvc_m, 2) == 2.78
    assert round(fvc_lln, 2) == 1.83
    assert round(fev1_m, 2) == 2.19
    assert round(fev1_lln, 2) == 1.37

    fvc_w, fvc_w_lln = predict(rows, "F", 70, 150, "fvc")
    fev1_w, fev1_w_lln = predict(rows, "F", 70, 150, "fev1")
    assert round(fvc_w, 2) == 1.78
    assert round(fvc_w_lln, 2) == 1.14
    assert round(fev1_w, 2) == 1.41
    assert round(fev1_w_lln, 2) == 0.85


def test_app_includes_required_credits_and_acknowledgements():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    text = re.sub(r"\s+", " ", html)
    assert "Concept, design, and creation: <strong>Dr Siddalingaiah H S, MD</strong>" in text
    assert "Professor, Department of Community Medicine" in text
    assert "Shridevi Institute of Medical Sciences and Research Hospital, Tumkur, Karnataka, India" in text
    assert "ORCID: 0000-0002-4771-8285" in text
    assert "Longitudinal Ageing Study in India Wave 1" in text
    assert "International Institute for Population Sciences" in text
    assert "Harvard T.H. Chan School of Public Health" in text
    assert "University of Southern California" in text


def test_assessment_summary_explains_outputs():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    js = (ROOT / "app.js").read_text(encoding="utf-8")
    assert "Snapshot of the current patient entry" in html
    assert "Based on generated prompts" in html
    assert "Overall lung pattern" in js
    assert "FEV1 vs reference" in js
    assert "Clinical review priority" in js
    assert "High-priority prompts" in js


def test_portal_language_consent_and_demo_accounts_exist():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    js = (ROOT / "app.js").read_text(encoding="utf-8")
    assert 'class="hero portal-landing" id="portal"' in html
    assert 'id="authStatus"' in html
    assert 'id="portalLaunchGrid"' in html
    assert "Sign in to healthy-ageing workflows" in html
    assert "Module library, saved timeline, and follow-up" in html
    assert "हिन्दी" in html
    assert "ಕನ್ನಡ" in html
    assert "தமிழ்" in html
    assert "తెలుగు" in html
    assert "मराठी" in html
    assert "clinician.demo@ihacs.local" in html
    assert "DemoClinician#2026" in html
    assert "patient.demo@ihacs.local" in html
    assert "care.demo@ihacs.local" in html
    assert "Digital Personal Data Protection Act" in html
    assert "consentAgreement" in js
    assert "LANGUAGE_CONTENT" in js
    assert "ROLE_WORKFLOWS" in js
    assert "PORTAL_LAUNCHES" in js
    assert "renderPortalLaunches" in js


def test_supabase_schema_scaffold_exists():
    migration = ROOT / "supabase" / "migrations" / "202607130001_portal_foundation.sql"
    seed = ROOT / "supabase" / "migrations" / "202607130002_seed_education_modules.sql"
    more_seed = ROOT / "supabase" / "migrations" / "202607130003_seed_more_language_modules.sql"
    config = ROOT / "supabase" / "config.toml"
    for path in (migration, seed, more_seed, config, ROOT / "config.example.json"):
        assert path.exists(), path
    sql = migration.read_text(encoding="utf-8")
    assert "create table public.assessments" in sql
    assert "create table public.consent_events" in sql
    assert "enable row level security" in sql
    assert "active education modules are public" in sql
    more_seed_text = more_seed.read_text(encoding="utf-8")
    assert "'ta'" in more_seed_text
    assert "'te'" in more_seed_text
    assert "'mr'" in more_seed_text


def test_supabase_runtime_config_is_generated_at_build_time():
    package = (ROOT / "package.json").read_text(encoding="utf-8")
    vercel = (ROOT / "vercel.json").read_text(encoding="utf-8")
    script = (ROOT / "scripts" / "build-config.js")
    assert script.exists()
    assert (ROOT / "config.public.json").exists()
    text = script.read_text(encoding="utf-8")
    assert "NEXT_PUBLIC_SUPABASE_URL" in text
    assert "NEXT_PUBLIC_SUPABASE_ANON_KEY" in text
    assert "YOUR_PUBLIC_ANON_KEY" not in text
    assert '"build": "node scripts/build-config.js"' in package
    assert '"buildCommand": "npm run build"' in vercel
    assert "config.public.json" in (ROOT / "app.js").read_text(encoding="utf-8")


def test_static_references_resolve():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    for path in re.findall(r'(?:src|href)="([^"]+)"', html):
        if path.startswith("#") or path.startswith("http"):
            continue
        assert (ROOT / path).exists(), path


if __name__ == "__main__":
    for name, func in sorted(globals().items()):
        if name.startswith("test_") and callable(func):
            func()
            print(f"ok {name}")
