"""Phase 7 (A3 amendment): extract ADJUSTED between-group effect estimates.

For each eligible study (relaxed_eligibility_audit_2026-05-18.csv with
final_eligibility in {include_accessible_first_reviewer, include_relaxed}),
parse the locally-cached full text (XML/HTML/PDF) and search for adjusted
between-group effect patterns near a clock mention.

Emits:
  data/processed/adjusted_effect_candidates_2026-05-18.csv
  data/processed/study_level_effects_2026-05-18.csv

No fabrication: only emits numbers literally present in the source.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from _common import ensure_dirs, load_config, log  # noqa: E402

# Canonical clock names and regex patterns to detect them.
CLOCK_PATTERNS = [
    ("DunedinPACE", r"Dunedin\s*PACE|Dunedin\s*Pace|DunedinPoAm"),
    ("GrimAge2", r"GrimAge\s*[2II]|GrimAge\s*v2|PCGrimAge\s*2"),
    ("GrimAge", r"(?<!PC)GrimAge(?!\s*[2II])|PCGrimAge(?!\s*2)"),
    ("PhenoAge", r"PhenoAge|DNAm\s*PhenoAge|PCPhenoAge"),
    ("Horvath", r"Horvath(?:'s)?(?:\s+clock|\s+multi-tissue|\s+pan-tissue)?|PCHorvath"),
    ("Hannum", r"Hannum(?:'s)?(?:\s+clock)?|PCHannum"),
    ("PCClock", r"PCClock|PC\s*Clock|PC-clocks?"),
    ("DNAmTL", r"DNAmTL|DNAm\s*TL|epigenetic\s+telomere\s+length"),
]


def detect_clock(text: str) -> str | None:
    for canon, pat in CLOCK_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            return canon
    if re.search(r"epigenetic\s+age|DNA\s*methylation\s+age|DNAm\s+age", text, re.IGNORECASE):
        return "UNSPECIFIED_EPIGENETIC_AGE"
    return None


def read_xml(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="replace")
    # strip xml tags but keep text content (and table cells separated by space)
    text = re.sub(r"<[^>]+>", " ", raw)
    text = re.sub(r"\s+", " ", text)
    return text


def read_html(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"<script[^>]*>.*?</script>", " ", raw, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"\s+", " ", text)
    return text


def read_pdf(path: Path) -> str:
    try:
        import pypdf  # type: ignore
    except Exception:
        try:
            import PyPDF2 as pypdf  # type: ignore
        except Exception:
            return ""
    try:
        reader = pypdf.PdfReader(str(path))
        chunks = []
        for page in reader.pages:
            try:
                chunks.append(page.extract_text() or "")
            except Exception:
                continue
        text = " ".join(chunks)
        text = re.sub(r"\s+", " ", text)
        return text
    except Exception:
        return ""


def load_fulltext(path: Path) -> str:
    if not path or not path.exists():
        return ""
    suffix = path.suffix.lower()
    if suffix == ".xml":
        return read_xml(path)
    if suffix == ".html" or suffix == ".htm":
        return read_html(path)
    if suffix == ".pdf":
        return read_pdf(path)
    return ""


# A number like -0.42, 0.5, .03, -.03 (allowing Unicode minus/dash as sign)
NUM = r"[\-−–—]?(?:\d+\.?\d*|\.\d+)"

CLOCK_TOKEN = r"(?:DunedinPACE|DunedinPoAm|Dunedin\s*Pace|GrimAge\s*V?2|GrimAge\s*v2|GrimAgeV1|GrimAge|PhenoAge|Horvath\s*1|Horvath\s*2|Horvath|Hannum|PCGrimAge|PCPhenoAge|PCHorvath|PCHannum|PCClock|DNAmTL)"

# Pattern A: "Horvath β = 0.66, p = 0.56" / "GrimAge β = −0.02, 95% CI -0.81 to -0.03"
PAT_BETA_CLOCK = re.compile(
    rf"(?P<clock>{CLOCK_TOKEN})"
    rf"(?:\s+(?:clock|age|acceleration|accel|mAge))?\s*[:,\-]?\s*"
    rf"(?:\(?adjusted\)?\s*)?(?:β|beta|coefficient|estimate|effect|MD|mean\s+difference|(?<![A-Za-z])d(?=\s*[=:]))"
    rf"\s*(?:was|=|of|:|\()?\s*"
    rf"(?P<val>{NUM})\s*(?:years?(?:/year)?)?\s*"
    rf"(?:"
    rf"[,;\s]*(?:95%?\s*(?:CI|confidence\s+interval)\s*[:=,]?\s*[\[\(]?(?P<lo>{NUM})\s*(?:,|to|;|–|—|-)\s*(?P<hi>{NUM})[\]\)]?)"
    rf"|[,;\s]*\((?P<lo2>{NUM})\s*(?:,|to|;|–|—)\s*(?P<hi2>{NUM})\)"
    rf"|[,;\s]*(?:SE|standard\s+error)\s*[=:]?\s*(?P<se>{NUM})"
    rf"|\s*±\s*(?P<sd>{NUM})"
    rf")?",
    re.IGNORECASE,
)

# Pattern B: "Clock (value, 95% CI lo, hi)" e.g. "DunedinPACE (−0.03, 95% CI −0.06, −0.004)" or "DunedinPACE (-0.03, -0.06, -0.004)"
PAT_CLOCK_PARENS = re.compile(
    rf"(?P<clock>{CLOCK_TOKEN})"
    rf"(?:\s+(?:clock|age|acceleration|accel|mAge))?\s*"
    rf"\(\s*(?P<val>{NUM})\s*(?:years?(?:/year)?)?"
    rf"(?:\s*,\s*(?:95%?\s*CI[:\s]*)?(?P<lo>{NUM})\s*(?:,|to|–|—|-)\s*(?P<hi>{NUM}))?\s*\)",
    re.IGNORECASE,
)

# Pattern C: "treatment effect on Clock ... value (95% CI lo, hi)"
PAT_EFFECT_THEN_CLOCK = re.compile(
    rf"(?:β|beta|coefficient|estimate|adjusted\s+(?:mean\s+)?difference|mean\s+difference|ANCOVA\s+adjusted\s+difference|MD|treatment\s+effect|intervention\s+effect|(?<![A-Za-z])d(?=\s*[=:]))"
    rf"\s*(?:was|=|of|:)?\s*"
    rf"(?P<val>{NUM})\s*(?:years?(?:/year)?)?\s*"
    rf"(?:[,;\s]*95%?\s*(?:CI|confidence\s+interval)\s*[:=,]?\s*[\[\(]?"
    rf"(?P<lo>{NUM})\s*(?:,|to|;|–|—|-)\s*(?P<hi>{NUM})[\]\)]?)?"
    rf".{{0,120}}?"
    rf"(?P<clock>{CLOCK_TOKEN})",
    re.IGNORECASE | re.DOTALL,
)

# Pattern D: "for/in Clock, β/value = X.XX, 95% CI [lo, hi]"
PAT_FOR_CLOCK_BETA = re.compile(
    rf"(?:for|in|on)\s+(?P<clock>{CLOCK_TOKEN})"
    rf"(?:\s+(?:clock|age|acceleration|accel|mAge))?[^.]{{0,80}}?"
    rf"(?:β|beta|coefficient|estimate|MD|difference|(?<![A-Za-z])d(?=\s*[=:]))\s*(?:was|=|of|:)?\s*"
    rf"(?P<val>{NUM})\s*(?:years?(?:/year)?)?"
    rf"(?:[,;\s]*95%?\s*CI\s*[:=]?\s*[\[\(]?(?P<lo>{NUM})\s*(?:,|to|;|–|—|-)\s*(?P<hi>{NUM})[\]\)]?)?",
    re.IGNORECASE,
)


def normalize_clock(raw: str) -> str:
    s = raw.replace(" ", "").lower()
    if "dunedin" in s:
        return "DunedinPACE"
    if "grimage2" in s or "grimagev2" in s:
        return "GrimAge2"
    if "grimage" in s:
        return "GrimAge"
    if "phenoage" in s:
        return "PhenoAge"
    if "horvath" in s:
        return "Horvath"
    if "hannum" in s:
        return "Hannum"
    if "pcclock" in s:
        return "PCClock"
    if "dnamtl" in s:
        return "DNAmTL"
    return raw


def _to_float(s: str) -> float | None:
    if s is None:
        return None
    s = s.replace("−", "-").replace("–", "-").replace("—", "-").strip()
    try:
        return float(s)
    except Exception:
        return None


def context_is_between_group(snippet: str) -> tuple[bool, str]:
    """Heuristic: does the snippet describe an intervention/exposure-vs-control between-group effect?"""
    s = snippet.lower()
    pos_terms = [
        "intervention", "treatment", "vs control", "vs. control", "versus control",
        "compared to control", "compared with control", "group difference",
        "between-group", "between group", "adjusted",
        "effect of", "interaction", "time-by-group", "time by group",
        "group*time", "group x time", "group by time",
        "linear mixed", "regression", "ancova", "estimated mean difference",
    ]
    neg_terms = [
        "correlation", "correlated", "pearson", "spearman",
        "baseline", "cross-sectional",
        "association with age", "with chronological age", "calibrat",
    ]
    has_pos = any(t in s for t in pos_terms)
    has_neg = any(t in s for t in neg_terms) and not has_pos
    if has_pos:
        return True, "between-group context terms present"
    if has_neg:
        return False, "context appears autocorrelative/cross-sectional"
    return True, "ambiguous, kept (flag for review)"


def make_snippet(text: str, start: int, end: int, pad: int = 150) -> str:
    s = max(0, start - pad)
    e = min(len(text), end + pad)
    return text[s:e].strip()[:300]


def _emit_match(study_id: str, m, ft: str, pattern_name: str) -> dict | None:
    gd = m.groupdict()
    val = _to_float(gd.get("val"))
    if val is None:
        return None
    lo = _to_float(gd.get("lo")) if gd.get("lo") else None
    hi = _to_float(gd.get("hi")) if gd.get("hi") else None
    if lo is None and gd.get("lo2"):
        lo = _to_float(gd.get("lo2"))
        hi = _to_float(gd.get("hi2"))
    se = _to_float(gd.get("se")) if gd.get("se") else None
    clock = normalize_clock(gd.get("clock") or "")
    if not clock:
        return None
    snippet = make_snippet(ft, m.start(), m.end())
    ok, note = context_is_between_group(snippet)
    if se is None and lo is not None and hi is not None:
        se = (hi - lo) / (2 * 1.96)
    # CONSERVATIVE: require either CI or SE — value-only is too noisy
    if lo is None and hi is None and se is None:
        return None
    # plausibility: drop values that are clearly not effect estimates
    # For DunedinPACE: typical effect range +/- 0.5; for age clocks +/- 20 years
    abs_val = abs(val)
    if clock == "DunedinPACE" and abs_val > 2.0:
        return None
    if clock != "DunedinPACE" and abs_val > 30.0:
        return None
    confidence = "medium"
    flag = "no"
    if not ok:
        confidence = "low"
        flag = "yes"
    if lo is not None and hi is not None:
        if not (min(lo, hi) - 1e-6 <= val <= max(lo, hi) + 1e-6):
            # CI doesn't bracket value — likely a misparse
            return None
        ci_width = abs(hi - lo)
        # plausibility on CI width
        if clock == "DunedinPACE" and ci_width > 2.0:
            confidence = "low"
            flag = "yes"
            note = note + "; CI width implausible for DunedinPACE"
        if clock != "DunedinPACE" and ci_width > 30.0:
            confidence = "low"
            flag = "yes"
            note = note + "; CI width implausibly large"
    if se is not None and se <= 0:
        return None
    # Boost confidence to "high" when CI present AND between-group context is clear
    if lo is not None and hi is not None and ok and "ambiguous" not in note:
        confidence = "high"
    metric = "mean_difference_pace" if clock == "DunedinPACE" else "mean_difference_years"
    return {
        "study_id": study_id,
        "clock": clock,
        "effect_metric": metric,
        "value": val,
        "se": se,
        "ci_lower": lo,
        "ci_upper": hi,
        "n_int": None,
        "n_ctrl": None,
        "n_total": None,
        "source_section_or_table": f"fulltext_regex_{pattern_name}",
        "evidence_snippet": snippet,
        "confidence": confidence,
        "direction_note": "negative value = slower epigenetic ageing (beneficial) for age clocks and DunedinPACE",
        "flag_for_human_review": flag,
        "context_note": note,
    }


def extract_candidates(study_id: str, ft: str) -> list[dict]:
    out: list[dict] = []
    if not ft:
        return out
    for pat, name in [
        (PAT_BETA_CLOCK, "PAT_BETA_CLOCK"),
        (PAT_CLOCK_PARENS, "PAT_CLOCK_PARENS"),
        (PAT_EFFECT_THEN_CLOCK, "PAT_EFFECT_THEN_CLOCK"),
        (PAT_FOR_CLOCK_BETA, "PAT_FOR_CLOCK_BETA"),
    ]:
        for m in pat.finditer(ft):
            row = _emit_match(study_id, m, ft, name)
            if row is not None:
                out.append(row)
    return out


def dedupe(rows: list[dict]) -> list[dict]:
    seen = set()
    keep = []
    for r in rows:
        key = (r["study_id"], r["clock"], round(r["value"], 4) if r["value"] is not None else None,
               round(r["se"], 4) if r["se"] is not None else None)
        if key in seen:
            continue
        seen.add(key)
        keep.append(r)
    return keep


CONF_RANK = {"high": 3, "medium": 2, "low": 1}


def pick_best(rows: list[dict]) -> dict:
    def score(r):
        c = CONF_RANK.get(r["confidence"], 0)
        completeness = (1 if r["ci_lower"] is not None and r["ci_upper"] is not None else 0) + (
            1 if r["se"] is not None else 0
        )
        return (c, completeness)
    return sorted(rows, key=score, reverse=True)[0]


# Manually-curated extractions read literally from snippets returned by the regex
# survey of the full-text corpus on 2026-05-19. Each entry includes the exact source
# sentence and a pointer to the section. These are emitted in addition to the regex
# candidates so that effects clearly stated in narrative form but in formats the regex
# does not capture (e.g., "exhibited a 1.39-year lower GrimAgeV1 estimate ... 95% CI ...")
# are not lost. Operating principle (protocol §0): numbers must be LITERALLY in the
# source — no fabrication.
MANUAL_EXTRACTIONS = [
    # CorleyMJ_2025_ad19fa (semaglutide RCT, n=39 placebo / n=45 semaglutide; 32-week)
    {
        "study_id": "CorleyMJ_2025_ad19fa", "clock": "GrimAge",
        "value": -1.39, "ci_lower": -2.72, "ci_upper": -0.05, "n_int": 45, "n_ctrl": 39,
        "section": "Results (GrimAge V1 ANCOVA)",
        "snippet": "exhibited a 1.39-year lower GrimAgeV1 estimate compared to placebo (95% CI: -2.72 to -0.05; p = 0.042) over the 32-week trial",
    },
    {
        "study_id": "CorleyMJ_2025_ad19fa", "clock": "GrimAge2",
        "value": -2.26, "ci_lower": -3.94, "ci_upper": -0.59, "n_int": 45, "n_ctrl": 39,
        "section": "Results (GrimAge V2 ANCOVA)",
        "snippet": "2.26-year reduction relative to placebo (95% CI: -3.94 to -0.59; p = 0.008)",
    },
    {
        "study_id": "CorleyMJ_2025_ad19fa", "clock": "DunedinPACE",
        "value": -0.09, "ci_lower": -0.17, "ci_upper": -0.02, "n_int": 45, "n_ctrl": 39,
        "section": "Results (DunedinPACE ANCOVA)",
        "snippet": "For DunedinPACE, semaglutide was associated with a 0.09 lower pace-of-aging (units per year) relative to placebo (95% CI: -0.17 to -0.02, p = 0.01)",
    },
    {
        "study_id": "CorleyMJ_2025_ad19fa", "clock": "PCClock",
        "value": -3.08, "ci_lower": -5.29, "ci_upper": -0.86, "n_int": 45, "n_ctrl": 39,
        "section": "Results (PCGrimAge ANCOVA)",
        "snippet": "PCGrimAge ... ANCOVA adjusted difference = -3.08 years/year, 95% CI: -5.29 to -0.86, p = 0.007",
    },
    # ChapnickM_2025_d1605d (early-life nutrition supplementation, atole exposure cohort)
    {
        "study_id": "ChapnickM_2025_d1605d", "clock": "DunedinPACE",
        "value": -0.03, "ci_lower": -0.06, "ci_upper": -0.004, "n_int": None, "n_ctrl": None,
        "section": "Results (DunedinPACE adjusted)",
        "snippet": "exposure to atole during any of the first 1,000-day period was associated with lower DunedinPACE (-0.03, 95% CI -0.06, -0.004)",
    },
    {
        "study_id": "ChapnickM_2025_d1605d", "clock": "PhenoAge",
        "value": -1.91, "ci_lower": -3.43, "ci_upper": -0.39, "n_int": None, "n_ctrl": None,
        "section": "Results (PhenoAge acceleration adjusted)",
        "snippet": "PhenoAge acceleration (-1.91 y, 95% CI -3.43, -0.39)",
    },
    {
        "study_id": "ChapnickM_2025_d1605d", "clock": "GrimAge",
        "value": -0.85, "ci_lower": -1.53, "ci_upper": -0.11, "n_int": None, "n_ctrl": None,
        "section": "Results (GrimAge acceleration adjusted)",
        "snippet": "GrimAge acceleration (-0.85 y, 95% CI -1.53, -0.11) compared to other exposures",
    },
    # WaziryR_2023_29b3ce (CALERIE CR trial; Cohen's d, not raw MD — recorded as standardized
    # effect; we accept under A3 because text reports it as the headline between-group estimate)
    {
        "study_id": "WaziryR_2023_29b3ce", "clock": "DunedinPACE",
        "value": -0.29, "ci_lower": -0.45, "ci_upper": -0.13, "n_int": 128, "n_ctrl": 69,
        "section": "Results (12-month Cohen's d)",
        "snippet": "12-month d = -0.29 (95% CI -0.45, -0.13), 24-month d = -0.25 (95% CI -0.41, -0.09), P < 0.003 for both (DunedinPACE)",
    },
    {
        "study_id": "WaziryR_2023_29b3ce", "clock": "PhenoAge",
        "value": -0.03, "ci_lower": -0.19, "ci_upper": 0.12, "n_int": 128, "n_ctrl": 69,
        "section": "Results (12-month Cohen's d)",
        "snippet": "for PhenoAge, 12-month d = -0.03 (95% CI -0.19, 0.12), 24-month d = 0.05 (95% CI -0.11, 0.20), P > 0.50",
    },
    {
        "study_id": "WaziryR_2023_29b3ce", "clock": "GrimAge",
        "value": -0.04, "ci_lower": -0.16, "ci_upper": 0.07, "n_int": 128, "n_ctrl": 69,
        "section": "Results (12-month Cohen's d)",
        "snippet": "for GrimAge, 12-month d = -0.04 (95% CI -0.16, 0.07), 24-month d = 0.05 (95% CI -0.07, 0.17), P > 0.40",
    },
    # MerrillSM_2024_5ee99d (iPCIT parenting RCT; DunedinPACE)
    {
        "study_id": "MerrillSM_2024_5ee99d", "clock": "DunedinPACE",
        "value": 0.26, "ci_lower": 0.03, "ci_upper": 0.49, "n_int": None, "n_ctrl": None,
        "section": "Results (treatment effect, beta)",
        "snippet": "significant treatment condition associations were observed (beta = 0.26; 95% CI, 0.03-0.49; P = .03) for DunedinPACE",
    },
    # YaskolkaMeirA_2023 (DIRECT PLUS; Hannum & Li mAge beta on 18-mo relative change)
    {
        "study_id": "YaskolkaMeirA_2023_ba151d", "clock": "Hannum",
        "value": -0.38, "ci_lower": None, "ci_upper": None, "se": None, "n_int": None, "n_ctrl": None,
        "section": "Results (Hannum multivariate beta)",
        "snippet": "greater Hannum mAge (beta = -0.38, p = 0.03) attenuation",
    },
    # OlasoGonzalezG_2026 (multidomain lifestyle RCT) — reported only group*time p-values
    # and graphical effects; numeric β with CI not present in narrative. Skip.
    # StanfieldB_2026 (rapamycin RCT) — outcome reported per arm with SD; no adjusted β with CI in narrative.
]


def emit_manual(study_id: str) -> list[dict]:
    out = []
    for e in MANUAL_EXTRACTIONS:
        if e["study_id"] != study_id:
            continue
        val = e["value"]; lo = e.get("ci_lower"); hi = e.get("ci_upper")
        se = e.get("se")
        if se is None and lo is not None and hi is not None:
            se = (hi - lo) / (2 * 1.96)
        clock = e["clock"]
        # Decide effect metric. For WaziryR_2023, values are Cohen's d — flag as SMD sensitivity
        metric = "mean_difference_pace" if clock == "DunedinPACE" else "mean_difference_years"
        if e["study_id"] == "WaziryR_2023_29b3ce":
            metric = "cohens_d_post_12mo"
        confidence = "high" if (lo is not None and hi is not None) else "low"
        out.append({
            "study_id": study_id,
            "clock": clock,
            "effect_metric": metric,
            "value": val,
            "se": se,
            "ci_lower": lo,
            "ci_upper": hi,
            "n_int": e.get("n_int"),
            "n_ctrl": e.get("n_ctrl"),
            "n_total": (e.get("n_int") + e.get("n_ctrl")) if e.get("n_int") and e.get("n_ctrl") else None,
            "source_section_or_table": f"manual_curation:{e['section']}",
            "evidence_snippet": e["snippet"][:300],
            "confidence": confidence,
            "direction_note": "negative value = slower epigenetic ageing (beneficial)",
            "flag_for_human_review": "no" if confidence == "high" else "yes",
            "context_note": "manually curated from source full-text snippet",
        })
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="anti_ageing_review/meta_dnam_clocks/config/meta_config.yaml")
    args = ap.parse_args()

    cfg = load_config(args.config)
    processed = Path(cfg["paths"]["data_processed"])
    ensure_dirs(processed)

    audit = pd.read_csv(processed / "relaxed_eligibility_audit_2026-05-18.csv")
    elig = audit[audit["final_eligibility"].isin(["include_accessible_first_reviewer", "include_relaxed"])].copy()

    all_rows: list[dict] = []
    per_study_count = {}
    for _, r in elig.iterrows():
        sid = r["study_id"]
        ft_path_raw = r.get("local_fulltext_path")
        if pd.isna(ft_path_raw) or not ft_path_raw:
            continue
        ft_path = Path(str(ft_path_raw))
        ft = load_fulltext(ft_path)
        cands = extract_candidates(sid, ft)
        cands.extend(emit_manual(sid))
        cands = dedupe(cands)
        all_rows.extend(cands)
        per_study_count[sid] = len(cands)

    cand_path = processed / "adjusted_effect_candidates_2026-05-18.csv"
    cols = ["study_id", "clock", "effect_metric", "value", "se", "ci_lower", "ci_upper",
            "n_int", "n_ctrl", "n_total", "source_section_or_table", "evidence_snippet",
            "confidence", "direction_note", "flag_for_human_review", "context_note"]
    with open(cand_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for row in all_rows:
            w.writerow({c: row.get(c) for c in cols})

    # study-level best pick
    df = pd.DataFrame(all_rows)
    best_rows = []
    if not df.empty:
        for (sid, clock), grp in df.groupby(["study_id", "clock"]):
            best = pick_best(grp.to_dict("records"))
            best_rows.append(best)

    study_level_path = processed / "study_level_effects_2026-05-18.csv"
    with open(study_level_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for row in best_rows:
            w.writerow({c: row.get(c) for c in cols})

    per_clock = {}
    for r in best_rows:
        per_clock[r["clock"]] = per_clock.get(r["clock"], 0) + 1

    log("adjusted_effect_extraction_done",
        candidates_emitted=len(all_rows),
        study_clock_pairs_with_pooled_input=len(best_rows),
        per_clock_counts=per_clock,
        per_study_counts=per_study_count)


if __name__ == "__main__":
    main()
