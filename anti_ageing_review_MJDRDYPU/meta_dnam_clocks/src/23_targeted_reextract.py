"""Path-C targeted re-extraction over the union of original includes and
Path-C-promoted studies.

For every study with ``final_eligibility`` in {``include_accessible_first_reviewer``,
``include_relaxed``}:

  * Locate its full-text file (``.xml`` > ``.html`` > ``.pdf``).
  * Run the colspan-aware JATS table grid extractor (imported via importlib
    from ``18_extract_enhanced.py``) where applicable.
  * Run the PDF table + prose scanner (also from 18) for PDF inputs.
  * Run an HTML prose scanner (using the same primitives).
  * Scan figure captions and supplementary-table references for clock names;
    record those as ``low`` confidence with ``requires_supplement`` flag.

Append novel candidates to ``xml_extraction_candidates_<freeze>.csv``,
deduplicated by (study_id, clock, arm, timepoint, mean, dispersion).

Reconcile candidates into ``extracted_clock_studies_<freeze>.csv`` -- promote
a row to ``extracted_complete`` only when the source unambiguously yields a
full effect-size set; otherwise ``extracted_partial`` or unchanged.
"""
from __future__ import annotations
import argparse
import csv
import importlib.util
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import load_config, log, ensure_dirs  # noqa: E402


def _load_enhanced_module():
    here = Path(__file__).resolve().parent
    mod_path = here / "18_extract_enhanced.py"
    spec = importlib.util.spec_from_file_location("extract_enhanced", mod_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


EE = _load_enhanced_module()


SUPPLEMENT_REFS = re.compile(
    r"\b(supplement(?:ary|al)?\s*(?:table|figure|file|material|data)\s*[A-Z]?\d*)\b",
    re.I,
)
FIGCAP_TAGS = ("fig", "caption")  # JATS


def scan_supplement_and_fig_captions_xml(xml_path: Path, clock_list, study_id):
    """Low-confidence scan over <fig>/<caption> and supplement references in JATS XML."""
    out = []
    try:
        tree = ET.parse(str(xml_path))
    except Exception:
        return out
    root = tree.getroot()
    for fig in root.iter("fig"):
        cap = " ".join(t.strip() for t in fig.itertext() if t and t.strip())
        if not cap:
            continue
        clock = EE.detect_clock(cap, clock_list)
        if clock:
            snip = (cap[:237] + "...") if len(cap) > 240 else cap
            out.append({
                "study_id": study_id,
                "clock": clock,
                "arm": "",
                "timepoint": "",
                "value_type": "figure_caption_reference",
                "mean": "",
                "dispersion": "",
                "dispersion_type": "",
                "n": "",
                "source_table_or_section": "XML figure caption",
                "evidence_snippet": f"requires_supplement | {snip}"[:240],
                "confidence": "low",
            })
    full_text = " ".join(t.strip() for t in root.itertext() if t and t.strip())
    for m in SUPPLEMENT_REFS.finditer(full_text):
        # Window around the supplement reference
        start = max(0, m.start() - 200)
        end = min(len(full_text), m.end() + 200)
        window = full_text[start:end]
        clock = EE.detect_clock(window, clock_list)
        if clock:
            out.append({
                "study_id": study_id,
                "clock": clock,
                "arm": "",
                "timepoint": "",
                "value_type": "supplement_reference",
                "mean": "",
                "dispersion": "",
                "dispersion_type": "",
                "n": "",
                "source_table_or_section": f"XML supplement reference ({m.group(0)})",
                "evidence_snippet": f"requires_supplement | {window[:200]}"[:240],
                "confidence": "low",
            })
    return out


def scan_supplement_and_fig_captions_html(html_path: Path, clock_list, study_id):
    out = []
    text = EE.text_html(html_path)
    if not text:
        return out
    for m in SUPPLEMENT_REFS.finditer(text):
        start = max(0, m.start() - 200)
        end = min(len(text), m.end() + 200)
        window = text[start:end]
        clock = EE.detect_clock(window, clock_list)
        if clock:
            out.append({
                "study_id": study_id,
                "clock": clock,
                "arm": "",
                "timepoint": "",
                "value_type": "supplement_reference",
                "mean": "",
                "dispersion": "",
                "dispersion_type": "",
                "n": "",
                "source_table_or_section": f"HTML supplement reference ({m.group(0)})",
                "evidence_snippet": f"requires_supplement | {window[:200]}"[:240],
                "confidence": "low",
            })
    return out


def scan_supplement_and_fig_captions_pdf(pdf_path: Path, clock_list, study_id):
    out = []
    if not EE.HAS_PDFPLUMBER:
        return out
    try:
        import pdfplumber  # type: ignore
        with pdfplumber.open(str(pdf_path)) as pdf:
            chunks = []
            for page in pdf.pages:
                try:
                    t = page.extract_text() or ""
                except Exception:
                    t = ""
                if t:
                    chunks.append(t)
            text = "\n".join(chunks)
    except Exception:
        return out
    for m in SUPPLEMENT_REFS.finditer(text):
        start = max(0, m.start() - 200)
        end = min(len(text), m.end() + 200)
        window = text[start:end]
        clock = EE.detect_clock(window, clock_list)
        if clock:
            out.append({
                "study_id": study_id,
                "clock": clock,
                "arm": "",
                "timepoint": "",
                "value_type": "supplement_reference",
                "mean": "",
                "dispersion": "",
                "dispersion_type": "",
                "n": "",
                "source_table_or_section": f"PDF supplement reference ({m.group(0)})",
                "evidence_snippet": f"requires_supplement | {window[:200]}"[:240],
                "confidence": "low",
            })
    return out


def process_study(study_id: str, ft_dir: Path, clock_list):
    xml_path = ft_dir / f"{study_id}.xml"
    html_path = ft_dir / f"{study_id}.html"
    pdf_path = ft_dir / f"{study_id}.pdf"
    cands = []
    if xml_path.exists() and xml_path.stat().st_size >= 200:
        c, _ = EE.process_xml(xml_path, clock_list, study_id)
        cands.extend(c)
        cands.extend(scan_supplement_and_fig_captions_xml(xml_path, clock_list, study_id))
        return cands, "xml"
    if html_path.exists() and html_path.stat().st_size >= 1000:
        cands.extend(EE.process_html(html_path, clock_list, study_id))
        cands.extend(scan_supplement_and_fig_captions_html(html_path, clock_list, study_id))
        return cands, "html"
    if pdf_path.exists() and pdf_path.stat().st_size >= 1000:
        c, _ = EE.process_pdf(pdf_path, clock_list, study_id)
        cands.extend(c)
        cands.extend(scan_supplement_and_fig_captions_pdf(pdf_path, clock_list, study_id))
        return cands, "pdf"
    return cands, "missing"


def load_existing_candidates(path: Path):
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def cand_key(c):
    return (
        (c.get("study_id") or "").strip(),
        (c.get("clock") or "").strip().lower(),
        (c.get("arm") or "").strip().lower(),
        (c.get("timepoint") or "").strip().lower(),
        str(c.get("mean") or "").strip(),
        str(c.get("dispersion") or "").strip(),
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    cfg = load_config(args.config)
    freeze = cfg["project"]["freeze_date"]
    clocks = cfg["clocks"]
    proc_dir = Path(cfg["paths"]["data_processed"])
    raw_dir = Path(cfg["paths"]["data_raw"])
    ft_dir = raw_dir / "fulltext"
    ensure_dirs(proc_dir)

    relaxed_csv = proc_dir / f"relaxed_eligibility_audit_{freeze}.csv"
    if not relaxed_csv.exists():
        log("relaxed_audit_missing", path=str(relaxed_csv))
        sys.exit(1)
    with open(relaxed_csv, "r", encoding="utf-8", newline="") as f:
        relaxed_rows = list(csv.DictReader(f))

    eligible = {"include_accessible_first_reviewer", "include_relaxed"}
    target_studies = sorted({
        r["study_id"] for r in relaxed_rows
        if (r.get("final_eligibility") or "").strip() in eligible
    })

    cand_csv = proc_dir / f"xml_extraction_candidates_{freeze}.csv"
    existing_cands = load_existing_candidates(cand_csv)
    existing_keys = {cand_key(c) for c in existing_cands}
    cand_fields = [
        "study_id", "clock", "arm", "timepoint", "value_type",
        "mean", "dispersion", "dispersion_type", "n",
        "source_table_or_section", "evidence_snippet", "confidence",
    ]

    new_candidates = []
    studies_processed = 0
    parser_breakdown = defaultdict(int)
    parser_failures = []

    for sid in target_studies:
        try:
            cands, kind = process_study(sid, ft_dir, clocks)
            studies_processed += 1
            parser_breakdown[kind] += 1
            for c in cands:
                k = cand_key(c)
                if k in existing_keys:
                    continue
                existing_keys.add(k)
                new_candidates.append(c)
            log("targeted_study_processed", study_id=sid, kind=kind, n_new=len(cands))
        except Exception as e:
            parser_failures.append((sid, str(e)))
            log("targeted_study_error", study_id=sid, error=str(e))

    # Append new candidates to the candidates CSV (don't overwrite)
    all_cands = existing_cands + new_candidates
    with open(cand_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cand_fields)
        w.writeheader()
        for c in all_cands:
            w.writerow({k: c.get(k, "") for k in cand_fields})

    # Reconcile into the seed extraction CSV
    seed_csv = proc_dir / f"extracted_clock_studies_{freeze}.csv"
    with open(seed_csv, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        seed_rows = list(reader)
        seed_fields = reader.fieldnames

    # Resolve UNSPECIFIED_EPIGENETIC_AGE -> specific clock when full-text is unambiguous
    # Build per-study set of named clocks observed in high/medium-confidence candidates
    named_clocks_by_study = defaultdict(set)
    for c in all_cands:
        if (c.get("confidence") in ("high", "medium")
                and c.get("clock") and c["clock"].upper() != "UNSPECIFIED_EPIGENETIC_AGE"):
            named_clocks_by_study[c["study_id"]].add(c["clock"])

    for r in seed_rows:
        if (r.get("clock") or "").upper() == "UNSPECIFIED_EPIGENETIC_AGE":
            sid = r["study_id"]
            named = named_clocks_by_study.get(sid, set())
            if len(named) == 1:
                only = next(iter(named))
                r["clock"] = only
                r["notes"] = (
                    (r.get("notes") or "") +
                    f" | Path-C: clock disambiguated to {only} from full text."
                ).strip(" |")

    # Reconciliation: use the 18-module reconcile() to update extraction_status
    # Numeric candidates only (skip low-confidence supplement/fig refs)
    numeric_cands = [
        c for c in all_cands
        if c.get("mean") not in ("", None) and c.get("dispersion") not in ("", None)
    ]

    # Cast to floats where possible for the reconciler
    coerced = []
    for c in numeric_cands:
        try:
            cc = dict(c)
            cc["mean"] = float(c["mean"])
            cc["dispersion"] = float(c["dispersion"])
            try:
                cc["n"] = int(c["n"]) if c.get("n") not in ("", None) else None
            except (ValueError, TypeError):
                cc["n"] = None
            coerced.append(cc)
        except (ValueError, TypeError):
            continue

    complete, partial, not_reported, _ = EE.reconcile(seed_rows, coerced)

    with open(seed_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=seed_fields)
        w.writeheader()
        for r in seed_rows:
            w.writerow(r)

    # Per-clock real-effect-eligible counts (rows with extraction_status == extracted_complete)
    per_clock_complete = defaultdict(int)
    per_clock_any = defaultdict(int)
    for r in seed_rows:
        clk = (r.get("clock") or "").strip()
        st = (r.get("extraction_status") or "").strip()
        if st == "extracted_complete":
            per_clock_complete[clk] += 1
        if st in ("extracted_complete", "extracted_partial"):
            per_clock_any[clk] += 1

    log(
        "targeted_reextract_done",
        studies_processed=studies_processed,
        total_candidates_added=len(new_candidates),
        rows_complete_after=complete,
        rows_partial_after=partial,
        rows_not_reported_after=not_reported,
        parser_breakdown=dict(parser_breakdown),
        parser_failures=parser_failures,
        per_clock_complete=dict(per_clock_complete),
        per_clock_complete_or_partial=dict(per_clock_any),
        candidates_csv=str(cand_csv),
        seed_csv=str(seed_csv),
    )


if __name__ == "__main__":
    main()
