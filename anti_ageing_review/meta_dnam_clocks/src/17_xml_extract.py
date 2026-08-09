"""Real numeric extraction of DNA-methylation clock outcomes from JATS XML full text.

Reads Europe PMC fulltext XML files in data/raw/fulltext/, parses <table-wrap> elements
and Results-section prose, attempts to attribute numeric mean/SD/CI values to
(clock, arm, timepoint) tuples, and emits two outputs:

  1. xml_extraction_candidates_<freeze>.csv  -- audit trail of every candidate value
  2. extracted_clock_studies_<freeze>.csv    -- updated seed worksheet (in-place)

Strict honesty: only values where (clock, arm, timepoint) can be unambiguously inferred
are populated. Otherwise the seed row's numeric fields are left blank.
"""
from __future__ import annotations
import argparse
import csv
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import load_config, log, ensure_dirs  # noqa: E402


# ------------------------- regex patterns -------------------------
MEAN_SD = re.compile(r"(-?\d+\.?\d*)\s*[±±±]\s*(\d+\.?\d*)")
MEAN_PAREN = re.compile(r"(-?\d+\.?\d*)\s*\(\s*(\d+\.?\d*)\s*\)")
MEAN_CI = re.compile(r"(-?\d+\.?\d*)\s*\[\s*(-?\d+\.?\d*)\s*[,;]\s*(-?\d+\.?\d*)\s*\]")
N_PATTERN = re.compile(r"\bn\s*=\s*(\d+)", re.I)

INT_TERMS = [
    "intervention", "treatment", "treated", "active", "exercise", "training",
    "diet", "supplement", "drug", "metformin", "rapamycin", "nad", "nmn", "nr",
    "senolytic", "fasting", "caloric restriction", "vitamin", "omega",
    "probiotic", "mediterranean", "ketogenic", "yoga", "meditation",
    "mindfulness", "aerobic", "resistance", "hiit", "tre", "fmd",
]
CTRL_TERMS = [
    "control", "placebo", "usual care", "sham", "wait-list", "waitlist",
    "wait list", "no intervention", "no treatment", "comparator",
]
TP_BASE = ["baseline", "pre-intervention", "pre intervention", "pre-", "week 0", "t0", "month 0", "preintervention"]
TP_POST = ["post-intervention", "post intervention", "post-", "follow-up", "followup", "endpoint", "end of", "after intervention", "week 8", "week 12", "week 24", "week 26", "week 52", "month 3", "month 6", "month 12", "endline", "postintervention"]
TP_CHG = ["change", "delta", "Δ", "difference", "change score", "from baseline"]

GENERIC_CLOCK_TERMS = [
    "epigenetic age", "dna methylation age", "dnam age", "dnamage",
    "epigenetic clock", "biological age", "methylation age",
]


def text_of(elem) -> str:
    """Concatenate all text content within an XML element."""
    if elem is None:
        return ""
    return " ".join(t.strip() for t in elem.itertext() if t and t.strip())


def classify_arm(s: str) -> str | None:
    sl = s.lower()
    has_int = any(t in sl for t in INT_TERMS)
    has_ctrl = any(t in sl for t in CTRL_TERMS)
    if has_ctrl and not has_int:
        return "control"
    if has_int and not has_ctrl:
        return "intervention"
    return None


def classify_timepoint(s: str) -> str | None:
    sl = s.lower()
    if any(t in sl for t in TP_CHG):
        return "change"
    if any(t in sl for t in TP_POST):
        return "post"
    if any(t in sl for t in TP_BASE):
        return "baseline"
    return None


def detect_clock(s: str, clock_list: list[str]) -> str | None:
    sl = s.lower()
    for c in clock_list:
        if c.lower() in sl:
            return c
    for g in GENERIC_CLOCK_TERMS:
        if g in sl:
            return "UNSPECIFIED_EPIGENETIC_AGE"
    return None


def extract_n(s: str) -> int | None:
    m = N_PATTERN.search(s)
    if m:
        try:
            return int(m.group(1))
        except ValueError:
            return None
    return None


def parse_table(table_wrap, clock_list):
    """Return (caption_text, header_rows[list[list[str]]], body_rows[list[list[str]]])."""
    caption_parts = []
    for tag in ("label", "caption", "title"):
        for el in table_wrap.iter(tag):
            t = text_of(el)
            if t:
                caption_parts.append(t)
    caption = " | ".join(caption_parts)

    def expand_row(tr):
        """Expand a <tr> to a list of cell text values, repeating cell text per colspan."""
        out = []
        for c in tr:
            if c.tag not in ("th", "td"):
                continue
            try:
                cs = int(c.get("colspan", "1") or "1")
            except ValueError:
                cs = 1
            t = text_of(c)
            for _ in range(max(cs, 1)):
                out.append(t)
        return out

    header_rows = []
    body_rows = []
    for tbl in table_wrap.iter("table"):
        for thead in tbl.iter("thead"):
            for tr in thead.iter("tr"):
                cells = expand_row(tr)
                if cells:
                    header_rows.append(cells)
        for tbody in tbl.iter("tbody"):
            for tr in tbody.iter("tr"):
                cells = expand_row(tr)
                if cells:
                    body_rows.append(cells)
        # Some JATS tables put rows directly under <table>
        if not header_rows and not body_rows:
            for tr in tbl.iter("tr"):
                cells = expand_row(tr)
                if cells:
                    body_rows.append(cells)
    return caption, header_rows, body_rows


def table_is_clock_relevant(caption, header_rows, clock_list):
    blob = caption.lower() + " " + " ".join(" ".join(r).lower() for r in header_rows)
    if detect_clock(blob, clock_list):
        return True
    return False


def extract_numeric_cells(cell: str):
    """Yield (mean, dispersion, dispersion_type) tuples from a cell string."""
    if not cell:
        return
    # Mean ± SD
    for m in MEAN_SD.finditer(cell):
        yield float(m.group(1)), float(m.group(2)), "sd", m.group(0)
    # Mean (SD) — only if no ± already in same span; require parens
    if not MEAN_SD.search(cell):
        for m in MEAN_PAREN.finditer(cell):
            # Avoid matching "Table 1 (rev 2)" or trivial counts; require decimal point in mean
            txt = m.group(0)
            if "." in m.group(1) or "." in m.group(2):
                yield float(m.group(1)), float(m.group(2)), "sd_or_se", txt
    # CI form
    for m in MEAN_CI.finditer(cell):
        mean = float(m.group(1))
        lo = float(m.group(2))
        hi = float(m.group(3))
        # convert 95% CI half-width to approximate SD if n unknown -- emit as ci half-width
        half = (hi - lo) / 2.0
        yield mean, half, "ci95_halfwidth", m.group(0)


def find_results_sections(root):
    """Yield Results section elements."""
    for sec in root.iter("sec"):
        st = sec.get("sec-type", "") or ""
        title_el = sec.find("title")
        title = text_of(title_el) if title_el is not None else ""
        if "result" in st.lower() or "result" in title.lower():
            yield sec


def scan_prose(text, clock_list, study_id):
    """Scan prose for clock + numeric + arm + timepoint co-occurrences in same sentence."""
    out = []
    # Split into sentences crudely
    for sent in re.split(r"(?<=[.!?])\s+", text):
        if len(sent) > 600:
            continue
        # Reject sentences talking about chronological/calendar age rather than
        # an epigenetic/methylation age outcome.
        sl = sent.lower()
        if "chronological age" in sl or "calendar age" in sl:
            continue
        clock = detect_clock(sent, clock_list)
        if not clock:
            continue
        arm = classify_arm(sent)
        tp = classify_timepoint(sent)
        if not arm or not tp:
            continue
        for mean, disp, dtype, snip in extract_numeric_cells(sent):
            # Require the numeric expression to be near the clock mention
            # (within 150 chars) to reduce spurious co-occurrence in long
            # sentences.
            num_pos = sent.find(snip)
            clock_positions = []
            for c in clock_list + GENERIC_CLOCK_TERMS:
                p = sent.lower().find(c.lower())
                if p >= 0:
                    clock_positions.append(p)
            if num_pos >= 0 and clock_positions:
                if min(abs(num_pos - p) for p in clock_positions) > 150:
                    continue
            out.append({
                "study_id": study_id,
                "clock": clock,
                "arm": arm,
                "timepoint": tp,
                "value_type": "change_score" if tp == "change" else "raw_clock_age",
                "mean": mean,
                "dispersion": disp,
                "dispersion_type": dtype,
                "n": extract_n(sent),
                "source_table_or_section": "Results (prose)",
                "evidence_snippet": (sent[:197] + "...") if len(sent) > 200 else sent,
                "confidence": "medium",
            })
    return out


def scan_table(table_wrap, clock_list, study_id, table_idx):
    """Extract candidate values from a clock-relevant table."""
    caption, header_rows, body_rows = parse_table(table_wrap, clock_list)
    if not table_is_clock_relevant(caption, header_rows, clock_list):
        return []

    out = []
    # Build column metadata from header_rows (last header row most specific)
    if not header_rows:
        return []
    # Determine total column count from widest row (header or body)
    n_cols = max(
        max((len(r) for r in header_rows), default=0),
        max((len(r) for r in body_rows), default=0),
    )
    # Right-align shorter header rows: if a header row is shorter than n_cols
    # it usually means the leftmost columns (row-label area) are intentionally
    # blank — pad with empties on the LEFT so subordinate headers align under
    # their parent groups.
    col_blobs = [""] * n_cols
    for r in header_rows:
        if len(r) < n_cols:
            pad = [""] * (n_cols - len(r))
            r_aligned = pad + list(r)
        else:
            r_aligned = list(r)
        for i, c in enumerate(r_aligned):
            if i < n_cols:
                col_blobs[i] = (col_blobs[i] + " " + c).strip()

    # Detect n per arm from headers
    col_n = [extract_n(b) for b in col_blobs]

    # Caption-level clock if header rows don't carry one
    cap_clock = detect_clock(caption, clock_list)

    # Detect whether header rows ALREADY carry both arm and timepoint metadata
    # at the same column index. If yes (single-row or well-flattened headers),
    # we can attribute confidently. If only one of the two is present per col,
    # we conservatively skip the table to avoid mis-attribution from
    # multi-row colspan headers (would need full grid alignment to fix).
    cols_with_arm = sum(1 for b in col_blobs if classify_arm(b))
    cols_with_tp = sum(1 for b in col_blobs if classify_timepoint(b))
    # Conservative: only trust per-column attribution when headers are a single
    # row (no colspan ambiguity) AND each column carries both arm and timepoint
    # signals. Multi-row spanning headers require grid-aware alignment which
    # we do not implement here -- skip those tables (honesty > yield).
    headers_fully_labelled = (
        len(header_rows) == 1
        and cols_with_arm >= 1
        and cols_with_tp >= 1
    )

    for row in body_rows:
        if not row:
            continue
        row_label = row[0] if row else ""
        row_label_l = row_label.lower()
        clock_in_row = detect_clock(row_label, clock_list)
        row_label_age_like = any(t in row_label_l for t in [
            "age", "clock", "methylation", "dnam", "pace", "horvath", "hannum",
            "grimage", "phenoage", "acceleration",
        ])
        # Restrict caption fallback to age-like row labels to avoid miscapturing
        # other outcomes (pain, fatigue, etc.) in tables whose caption mentions
        # epigenetic age alongside other variables.
        if clock_in_row:
            row_clock = clock_in_row
        elif row_label_age_like:
            row_clock = cap_clock
        else:
            row_clock = None
        row_arm = classify_arm(row_label)
        row_tp = classify_timepoint(row_label)

        if not row_clock:
            continue
        # We need to know arm and timepoint per data cell. If the row label
        # itself supplies both (e.g. "Intervention baseline"), use that for all
        # numeric cells in the row. Else require headers to supply them.
        row_supplies_both = bool(row_arm and row_tp)
        if not row_supplies_both and not headers_fully_labelled:
            continue

        for i, cell in enumerate(row[1:], start=1):
            col_blob = col_blobs[i] if i < n_cols else ""
            clock = row_clock
            arm = row_arm or classify_arm(col_blob)
            tp = row_tp or classify_timepoint(col_blob)
            if not clock or not arm or not tp:
                continue

            for mean, disp, dtype, snip in extract_numeric_cells(cell):
                out.append({
                    "study_id": study_id,
                    "clock": clock,
                    "arm": arm,
                    "timepoint": tp,
                    "value_type": "change_score" if tp == "change" else "raw_clock_age",
                    "mean": mean,
                    "dispersion": disp,
                    "dispersion_type": dtype,
                    "n": col_n[i] if i < len(col_n) else None,
                    "source_table_or_section": f"Table {table_idx} ({caption[:80]})",
                    "evidence_snippet": (f"row='{row_label[:60]}' col='{col_blob[:60]}' cell='{snip}'")[:200],
                    "confidence": "high",
                })
    return out


def process_xml(xml_path: Path, clock_list: list[str], study_id: str):
    candidates = []
    try:
        tree = ET.parse(str(xml_path))
    except ET.ParseError as e:
        log("xml_parse_error", study_id=study_id, error=str(e))
        return candidates
    root = tree.getroot()

    # Tables
    for idx, tw in enumerate(root.iter("table-wrap"), start=1):
        candidates.extend(scan_table(tw, clock_list, study_id, idx))

    # Results prose
    for sec in find_results_sections(root):
        prose = text_of(sec)
        candidates.extend(scan_prose(prose, clock_list, study_id))

    return candidates


# ---------------- Reconciliation into the seed worksheet ----------------
SEED_NUM_FIELDS = [
    "baseline_int_mean", "baseline_int_sd",
    "post_int_mean", "post_int_sd",
    "baseline_ctrl_mean", "baseline_ctrl_sd",
    "post_ctrl_mean", "post_ctrl_sd",
    "change_int_mean", "change_int_sd",
    "change_ctrl_mean", "change_ctrl_sd",
    "n_int", "n_ctrl",
]


def best_candidate(group):
    """Pick the most reliable candidate from a list (prefer high confidence, then table source)."""
    if not group:
        return None
    group_sorted = sorted(
        group,
        key=lambda c: (
            0 if c["confidence"] == "high" else (1 if c["confidence"] == "medium" else 2),
            0 if c["source_table_or_section"].startswith("Table") else 1,
        ),
    )
    return group_sorted[0]


def reconcile(seed_rows, candidates):
    """Given seed worksheet rows and candidate values, populate the rows in-place."""
    # Index candidates by (study_id, clock_normalized)
    idx = defaultdict(list)
    for c in candidates:
        idx[(c["study_id"], c["clock"].lower())].append(c)

    updated = 0
    complete = 0
    partial = 0
    not_reported = 0

    for row in seed_rows:
        sid = row["study_id"]
        seed_clock = (row.get("clock") or "").strip()
        # Find matching candidates: exact clock, or generic match
        key = (sid, seed_clock.lower())
        cands = list(idx.get(key, []))
        # If seed clock is generic placeholder, accept any clock from this study
        if seed_clock.upper() in ("UNSPECIFIED_EPIGENETIC_AGE", "") or not cands:
            # also try generic bucket
            for (s, c), v in idx.items():
                if s == sid and (seed_clock.lower() == c or seed_clock.upper() == "UNSPECIFIED_EPIGENETIC_AGE"):
                    cands.extend(v)
        # Dedup
        seen = set()
        unique = []
        for c in cands:
            k = (c["arm"], c["timepoint"], c["mean"], c["dispersion"], c["source_table_or_section"])
            if k not in seen:
                seen.add(k)
                unique.append(c)
        cands = unique

        if not cands:
            if not row.get("extraction_status") or row.get("extraction_status") == "not_reported":
                row["extraction_status"] = "not_reported"
            not_reported += 1
            continue

        # Group by (arm, timepoint)
        buckets = defaultdict(list)
        for c in cands:
            buckets[(c["arm"], c["timepoint"])].append(c)

        b_int = best_candidate(buckets.get(("intervention", "baseline"), []))
        p_int = best_candidate(buckets.get(("intervention", "post"), []))
        b_ctrl = best_candidate(buckets.get(("control", "baseline"), []))
        p_ctrl = best_candidate(buckets.get(("control", "post"), []))
        c_int = best_candidate(buckets.get(("intervention", "change"), []))
        c_ctrl = best_candidate(buckets.get(("control", "change"), []))

        any_filled = False
        notes_bits = []

        if b_int:
            row["baseline_int_mean"] = b_int["mean"]
            row["baseline_int_sd"] = b_int["dispersion"]
            any_filled = True
        if p_int:
            row["post_int_mean"] = p_int["mean"]
            row["post_int_sd"] = p_int["dispersion"]
            any_filled = True
        if b_ctrl:
            row["baseline_ctrl_mean"] = b_ctrl["mean"]
            row["baseline_ctrl_sd"] = b_ctrl["dispersion"]
            any_filled = True
        if p_ctrl:
            row["post_ctrl_mean"] = p_ctrl["mean"]
            row["post_ctrl_sd"] = p_ctrl["dispersion"]
            any_filled = True
        if c_int:
            row["change_int_mean"] = c_int["mean"]
            row["change_int_sd"] = c_int["dispersion"]
            any_filled = True
        if c_ctrl:
            row["change_ctrl_mean"] = c_ctrl["mean"]
            row["change_ctrl_sd"] = c_ctrl["dispersion"]
            any_filled = True

        # Sample size detection
        n_ints = [c["n"] for c in cands if c["arm"] == "intervention" and c.get("n")]
        n_ctrls = [c["n"] for c in cands if c["arm"] == "control" and c.get("n")]
        if n_ints and not row.get("n_int"):
            row["n_int"] = max(n_ints)
            any_filled = True
        if n_ctrls and not row.get("n_ctrl"):
            row["n_ctrl"] = max(n_ctrls)
            any_filled = True

        # Classify completeness
        full_pre_post = all([b_int, p_int, b_ctrl, p_ctrl])
        full_change = c_int and c_ctrl and row.get("n_int") and row.get("n_ctrl")
        if full_pre_post or full_change:
            row["extraction_status"] = "extracted_complete"
            complete += 1
            notes_bits.append("Full effect-size set extracted from XML.")
        elif any_filled:
            row["extraction_status"] = "extracted_partial"
            partial += 1
            notes_bits.append("Partial extraction; some arm/timepoint cells missing.")
        else:
            row["extraction_status"] = "not_reported"
            not_reported += 1

        # Build provenance note
        sources = sorted({c["source_table_or_section"] for c in cands if (
            c in (b_int, p_int, b_ctrl, p_ctrl, c_int, c_ctrl)
        )})
        if sources:
            notes_bits.append("Sources: " + "; ".join(s[:80] for s in sources))
        if notes_bits:
            row["notes"] = " ".join(notes_bits)
        updated += 1

    return updated, complete, partial, not_reported


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

    seed_csv = proc_dir / f"extracted_clock_studies_{freeze}.csv"
    if not seed_csv.exists():
        log("seed_missing", path=str(seed_csv))
        sys.exit(1)

    with open(seed_csv, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        seed_rows = list(reader)
        seed_fields = reader.fieldnames

    # Collect unique study_ids that have XML
    study_ids = sorted({r["study_id"] for r in seed_rows})
    all_candidates = []
    n_parsed = 0
    for sid in study_ids:
        xml_path = ft_dir / f"{sid}.xml"
        if not xml_path.exists():
            continue
        if xml_path.stat().st_size < 200:
            log("xml_too_small_skip", study_id=sid, bytes=xml_path.stat().st_size)
            continue
        n_parsed += 1
        cands = process_xml(xml_path, clocks, sid)
        all_candidates.extend(cands)
        log("xml_parsed", study_id=sid, n_candidates=len(cands))

    # Write candidate CSV
    cand_csv = proc_dir / f"xml_extraction_candidates_{freeze}.csv"
    cand_fields = [
        "study_id", "clock", "arm", "timepoint", "value_type",
        "mean", "dispersion", "dispersion_type", "n",
        "source_table_or_section", "evidence_snippet", "confidence",
    ]
    with open(cand_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cand_fields)
        w.writeheader()
        for c in all_candidates:
            w.writerow({k: c.get(k, "") for k in cand_fields})

    # Reconcile
    updated, complete, partial, not_reported = reconcile(seed_rows, all_candidates)

    # Write back seed
    with open(seed_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=seed_fields)
        w.writeheader()
        for r in seed_rows:
            w.writerow(r)

    log(
        "xml_extraction_done",
        n_xmls_parsed=n_parsed,
        n_candidate_extractions=len(all_candidates),
        n_rows_marked_complete=complete,
        n_rows_marked_partial=partial,
        n_rows_marked_not_reported=not_reported,
        candidates_csv=str(cand_csv),
        seed_csv=str(seed_csv),
    )


if __name__ == "__main__":
    main()
