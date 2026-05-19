"""Path-C relaxed full-text eligibility re-audit.

Re-evaluates rows in ``fulltext_eligibility_audit_<freeze>.csv`` under the
amended eligibility (see ``docs/amendment_log.md`` §A2). Rows previously
excluded for "Observational/association title-abstract signal" or
"Protocol/design/baseline-only/conference signal" are re-checked against the
local full text for three relaxed signals:

  (a) at least one named DNAm clock,
  (b) at least two timepoints (baseline + post, T1 + T2, pre + post, or week-X),
  (c) numeric arm-level / group-level reporting (mean ± SD or median (IQR)).

Where all three are present, the row is promoted to ``include_relaxed``.
Promotion criteria are intentionally conservative -- no fabrication.
"""
from __future__ import annotations
import argparse
import csv
import html as html_lib
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import load_config, log, ensure_dirs  # noqa: E402

try:
    import pdfplumber  # type: ignore
    HAS_PDFPLUMBER = True
except Exception:
    HAS_PDFPLUMBER = False


# ------------------------- relaxed signal patterns -------------------------
CLOCK_PATTERNS = [
    re.compile(r"\bDunedin\s*PACE\b", re.I),
    re.compile(r"\bGrimAge\s*2?\b", re.I),
    re.compile(r"\bPhenoAge\b", re.I),
    re.compile(r"\bHorvath\b", re.I),
    re.compile(r"\bHannum\b", re.I),
    re.compile(r"\bPC[- ]?Clock", re.I),
    re.compile(r"\bDNAmTL\b", re.I),
    re.compile(r"\bepigenetic age\b", re.I),
    re.compile(r"\bepigenetic clock\b", re.I),
    re.compile(r"\bDNA methylation age\b", re.I),
    re.compile(r"\bDNAm[- ]?age\b", re.I),
    re.compile(r"\bmethylation age\b", re.I),
]

TIMEPOINT_PATTERNS = [
    re.compile(r"\bbaseline\b", re.I),
    re.compile(r"\bpre[- ]?intervention\b", re.I),
    re.compile(r"\bpost[- ]?intervention\b", re.I),
    re.compile(r"\bpre[- ]?test\b", re.I),
    re.compile(r"\bpost[- ]?test\b", re.I),
    re.compile(r"\bfollow[- ]?up\b", re.I),
    re.compile(r"\bendpoint\b", re.I),
    re.compile(r"\bT[0-9]\b"),
    re.compile(r"\bweek\s*\d+\b", re.I),
    re.compile(r"\bmonth\s*\d+\b", re.I),
    re.compile(r"\bday\s*\d+\b", re.I),
    re.compile(r"\bvisit\s*\d+\b", re.I),
    re.compile(r"\bpre\b.{0,30}\bpost\b", re.I | re.S),
    re.compile(r"\bbefore\b.{0,30}\bafter\b", re.I | re.S),
]

NUMERIC_PATTERNS = [
    re.compile(r"-?\d+\.?\d*\s*[±±±]\s*\d+\.?\d*"),
    re.compile(r"-?\d+\.?\d*\s*\(\s*-?\d+\.?\d*\s*[-–,;]\s*-?\d+\.?\d*\s*\)"),  # median (IQR or CI)
    re.compile(r"\bmean\b[^.\n]{0,80}\bSD\b", re.I),
    re.compile(r"\bmedian\b[^.\n]{0,80}\bIQR\b", re.I),
]

RELAXED_TARGET_REASONS = {
    "Observational/association title-abstract signal",
    "Protocol/design/baseline-only/conference signal",
}


def read_text_from_path(p: Path) -> str:
    if not p.exists() or p.stat().st_size < 200:
        return ""
    suffix = p.suffix.lower()
    if suffix == ".xml":
        try:
            tree = ET.parse(str(p))
            root = tree.getroot()
            return " ".join(t.strip() for t in root.itertext() if t and t.strip())
        except Exception as e:
            log("relaxed_xml_parse_error", path=str(p), error=str(e))
            return ""
    if suffix == ".html":
        try:
            raw = p.read_text(encoding="utf-8", errors="ignore")
            raw = re.sub(r"(?is)<(script|style|noscript).*?</\1>", " ", raw)
            raw = re.sub(r"(?s)<[^>]+>", " ", raw)
            return re.sub(r"\s+", " ", html_lib.unescape(raw))
        except Exception as e:
            log("relaxed_html_parse_error", path=str(p), error=str(e))
            return ""
    if suffix == ".pdf":
        if not HAS_PDFPLUMBER:
            return ""
        try:
            chunks = []
            with pdfplumber.open(str(p)) as pdf:
                for page in pdf.pages:
                    try:
                        t = page.extract_text() or ""
                    except Exception:
                        t = ""
                    if t:
                        chunks.append(t)
            return "\n".join(chunks)
        except Exception as e:
            log("relaxed_pdf_parse_error", path=str(p), error=str(e))
            return ""
    return ""


def has_clock(text: str) -> str:
    for pat in CLOCK_PATTERNS:
        m = pat.search(text)
        if m:
            return m.group(0)
    return ""


def has_timepoints(text: str) -> int:
    found = 0
    seen = set()
    for pat in TIMEPOINT_PATTERNS:
        for m in pat.finditer(text):
            tok = m.group(0).lower()
            if tok not in seen:
                seen.add(tok)
                found += 1
            if found >= 2:
                return found
    return found


def has_numeric(text: str) -> str:
    for pat in NUMERIC_PATTERNS:
        m = pat.search(text)
        if m:
            return m.group(0)[:80]
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()

    cfg = load_config(args.config)
    freeze = cfg["project"]["freeze_date"]
    proc_dir = Path(cfg["paths"]["data_processed"])
    raw_dir = Path(cfg["paths"]["data_raw"])
    ft_dir = raw_dir / "fulltext"
    ensure_dirs(proc_dir)

    audit_csv = proc_dir / f"fulltext_eligibility_audit_{freeze}.csv"
    if not audit_csv.exists():
        log("audit_missing", path=str(audit_csv))
        sys.exit(1)

    with open(audit_csv, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        in_fields = reader.fieldnames or []

    out_fields = list(in_fields) + [
        "relaxed_decision",
        "relaxed_reason",
        "relaxed_signal_clock",
        "relaxed_signal_timepoints",
        "relaxed_signal_numeric",
        "final_eligibility",
    ]

    kept_includes = 0
    newly_promoted = 0
    still_excluded = 0
    awaiting_fulltext = 0

    for row in rows:
        first_dec = (row.get("first_reviewer_fulltext_decision") or "").strip()
        first_reason = (row.get("first_reviewer_reason") or "").strip()
        local_path = (row.get("local_fulltext_path") or "").strip()
        row["relaxed_decision"] = ""
        row["relaxed_reason"] = ""
        row["relaxed_signal_clock"] = ""
        row["relaxed_signal_timepoints"] = ""
        row["relaxed_signal_numeric"] = ""
        row["final_eligibility"] = ""

        if first_dec == "include_accessible_first_reviewer":
            row["relaxed_decision"] = "kept_include"
            row["relaxed_reason"] = "Kept original first-reviewer include under Path-C amendment"
            row["final_eligibility"] = "include_accessible_first_reviewer"
            kept_includes += 1
            continue

        if first_dec == "await_fulltext":
            row["relaxed_decision"] = "await_fulltext"
            row["relaxed_reason"] = "No accessible full text; cannot apply relaxed rules"
            row["final_eligibility"] = "await_fulltext"
            awaiting_fulltext += 1
            continue

        if first_dec == "exclude_fulltext" and first_reason in RELAXED_TARGET_REASONS:
            # Re-evaluate against local full text under relaxed rules
            p = Path(local_path) if local_path else None
            text = read_text_from_path(p) if p else ""
            if not text:
                row["relaxed_decision"] = "still_excluded"
                row["relaxed_reason"] = (
                    f"Path-C re-eval: full text unreadable or missing; "
                    f"original reason retained ({first_reason})"
                )
                row["final_eligibility"] = "exclude_fulltext"
                still_excluded += 1
                continue
            clock_sig = has_clock(text)
            tp_count = has_timepoints(text)
            num_sig = has_numeric(text)
            row["relaxed_signal_clock"] = clock_sig
            row["relaxed_signal_timepoints"] = str(tp_count)
            row["relaxed_signal_numeric"] = num_sig
            if clock_sig and tp_count >= 2 and num_sig:
                row["relaxed_decision"] = "include_relaxed"
                row["relaxed_reason"] = (
                    "Path-C amendment: longitudinal arm-level clock data present"
                )
                row["final_eligibility"] = "include_relaxed"
                newly_promoted += 1
            else:
                missing = []
                if not clock_sig:
                    missing.append("clock_signal")
                if tp_count < 2:
                    missing.append(f"timepoints<2 (found {tp_count})")
                if not num_sig:
                    missing.append("numeric_dispersion_pattern")
                row["relaxed_decision"] = "still_excluded"
                row["relaxed_reason"] = (
                    f"Path-C re-eval: missing {'; '.join(missing)}; "
                    f"original reason retained ({first_reason})"
                )
                row["final_eligibility"] = "exclude_fulltext"
                still_excluded += 1
            continue

        # Other exclusion reasons (e.g., "DNAm clock outcome not confirmed") -> keep excluded
        row["relaxed_decision"] = "still_excluded"
        row["relaxed_reason"] = (
            f"Path-C: original exclusion reason not eligible for re-evaluation ({first_reason})"
        )
        row["final_eligibility"] = "exclude_fulltext"
        still_excluded += 1

    out_csv = proc_dir / f"relaxed_eligibility_audit_{freeze}.csv"
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=out_fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in out_fields})

    log(
        "relaxed_eligibility_done",
        kept_includes=kept_includes,
        newly_promoted=newly_promoted,
        still_excluded=still_excluded,
        awaiting_fulltext=awaiting_fulltext,
        output_csv=str(out_csv),
    )


if __name__ == "__main__":
    main()
