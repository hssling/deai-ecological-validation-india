"""Enhanced real numeric extraction of DNA-methylation clock outcomes.

Supersedes 17_xml_extract.py. Adds:
  1) JATS colspan/rowspan-aware 2D grid for tables (joined header paths).
  2) PDF parsing via pdfplumber (tables + prose).
  3) HTML full-text prose parsing for rescued open-access pages.
  4) Same reconciliation contract as v1.

Strict honesty: when (clock, arm, timepoint) cannot be unambiguously inferred,
skip the cell. Never fabricate.
"""
from __future__ import annotations
import argparse
import csv
import html as html_lib
import re
import sys
import traceback
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import load_config, log, ensure_dirs  # noqa: E402

try:
    import pdfplumber  # type: ignore
    HAS_PDFPLUMBER = True
except Exception:
    HAS_PDFPLUMBER = False


# ------------------------- regex patterns -------------------------
MEAN_SD = re.compile(r"(-?\d+\.?\d*)\s*[±±±]\s*(\d+\.?\d*)")
MEAN_PAREN = re.compile(r"(-?\d+\.?\d*)\s*\(\s*(-?\d+\.?\d*)\s*\)")
MEAN_CI = re.compile(r"(-?\d+\.?\d*)\s*[\[\(]\s*(-?\d+\.?\d*)\s*[,;]\s*(-?\d+\.?\d*)\s*[\]\)]")
N_PATTERN = re.compile(r"\bn\s*=\s*(\d+)", re.I)

ARM_INT_RE = re.compile(
    r"\b(intervention|treatment|treated|active|experimental|exercise(?:\s+group)?|"
    r"training(?:\s+group)?|diet(?:\s+group)?|supplement(?:ation)?(?:\s+group)?|"
    r"tr\s+group|exp\s+group|metformin|rapamycin|nad|nmn|nr|senolytic|fasting|"
    r"caloric restriction|mediterranean|ketogenic|yoga|meditation|mindfulness|"
    r"aerobic|resistance|hiit|tre|fmd|probiotic|vitamin|omega)\b",
    re.I,
)
ARM_CTRL_RE = re.compile(
    r"\b(control|placebo|usual care|sham|wait[- ]?list|standard care|"
    r"ctrl(?:\s+group)?|con(?:\s+group)?|no intervention|no treatment|comparator)\b",
    re.I,
)
TP_BASE_RE = re.compile(
    r"\b(baseline|pre[- ]?intervention|pre[- ]?test|pre-?\b|t0|t1|week\s*0|month\s*0|day\s*0|preintervention)\b",
    re.I,
)
TP_POST_RE = re.compile(
    r"\b(post[- ]?intervention|post[- ]?test|post-?\b|follow[- ]?up|endpoint|"
    r"end[- ]?point|end of|after intervention|endline|postintervention|"
    r"t[2-9]|week\s*[1-9]\d*|month\s*[1-9]\d*|day\s*[1-9]\d*)\b",
    re.I,
)
TP_CHG_RE = re.compile(
    r"\b(change|delta|Δ|difference|change score|from baseline|mean (?:difference|change))\b",
    re.I,
)

GENERIC_CLOCK_TERMS = [
    "epigenetic age", "dna methylation age", "dnam age", "dnamage",
    "epigenetic clock", "methylation age", "dnam-age",
]


# ------------------------- helpers -------------------------
def text_of(elem) -> str:
    if elem is None:
        return ""
    return " ".join(t.strip() for t in elem.itertext() if t and t.strip())


def classify_arm(s: str) -> str | None:
    if not s:
        return None
    has_int = bool(ARM_INT_RE.search(s))
    has_ctrl = bool(ARM_CTRL_RE.search(s))
    if has_ctrl and not has_int:
        return "control"
    if has_int and not has_ctrl:
        return "intervention"
    return None


def classify_timepoint(s: str) -> str | None:
    if not s:
        return None
    if TP_CHG_RE.search(s):
        return "change"
    if TP_POST_RE.search(s):
        return "post"
    if TP_BASE_RE.search(s):
        return "baseline"
    return None


def detect_clock(s: str, clock_list: list[str]) -> str | None:
    if not s:
        return None
    sl = s.lower()
    for c in clock_list:
        if c.lower() in sl:
            return c
    for g in GENERIC_CLOCK_TERMS:
        if g in sl:
            return "UNSPECIFIED_EPIGENETIC_AGE"
    return None


def extract_n(s: str) -> int | None:
    if not s:
        return None
    m = N_PATTERN.search(s)
    if m:
        try:
            return int(m.group(1))
        except ValueError:
            return None
    return None


def extract_numeric_cells(cell: str):
    if not cell:
        return
    found_sd_spans = []
    for m in MEAN_SD.finditer(cell):
        found_sd_spans.append((m.start(), m.end()))
        yield float(m.group(1)), float(m.group(2)), "sd", m.group(0)
    # CI [lo, hi] OR (lo, hi)
    for m in MEAN_CI.finditer(cell):
        mean = float(m.group(1))
        lo = float(m.group(2))
        hi = float(m.group(3))
        if lo <= mean <= hi or (lo > hi):
            half = abs(hi - lo) / 2.0
            yield mean, half, "ci95_halfwidth", m.group(0)
    # Mean (SD)
    for m in MEAN_PAREN.finditer(cell):
        # skip overlap with ± matches
        if any(a <= m.start() < b for a, b in found_sd_spans):
            continue
        # Avoid ranges (lo, hi) that look like CI - those handled above.
        # Heuristic: require at least one decimal point in either component.
        if "." not in m.group(1) and "." not in m.group(2):
            continue
        try:
            v1 = float(m.group(1))
            v2 = float(m.group(2))
        except ValueError:
            continue
        # Skip year-like integers (e.g., "2024 (2)") with no decimals
        yield v1, abs(v2), "sd_or_se", m.group(0)


# ------------------------- JATSTableGrid -------------------------
class JATSTableGrid:
    """Builds a 2D grid honoring colspan/rowspan; identifies header rows."""

    def __init__(self, table_wrap_elem, clock_list):
        self.tw = table_wrap_elem
        self.clocks = clock_list
        self.caption = self._caption()
        self.grid: list[list[str | None]] = []
        self.header_row_count: int = 0
        self._build()

    def _caption(self):
        parts = []
        for tag in ("label", "caption", "title"):
            for el in self.tw.iter(tag):
                t = text_of(el)
                if t:
                    parts.append(t)
        return " | ".join(parts)

    def _expand(self, rows):
        if not rows:
            return []
        width = 0
        for tr in rows:
            w = 0
            for cell in tr:
                if cell.tag not in ("td", "th"):
                    continue
                try:
                    w += int(cell.get("colspan", "1") or "1")
                except ValueError:
                    w += 1
            width = max(width, w)
        if width == 0:
            return []
        grid = []
        rowspan_carry: dict[int, tuple[str, int]] = {}
        for tr in rows:
            grid_row: list[str | None] = [None] * width
            for c_idx, (txt, rem) in list(rowspan_carry.items()):
                if c_idx < width and rem > 0:
                    grid_row[c_idx] = txt
                    new_rem = rem - 1
                    if new_rem <= 0:
                        del rowspan_carry[c_idx]
                    else:
                        rowspan_carry[c_idx] = (txt, new_rem)
            c_idx = 0
            for cell in tr:
                if cell.tag not in ("td", "th"):
                    continue
                while c_idx < width and grid_row[c_idx] is not None:
                    c_idx += 1
                if c_idx >= width:
                    break
                try:
                    colspan = int(cell.get("colspan", "1") or "1")
                except ValueError:
                    colspan = 1
                try:
                    rowspan = int(cell.get("rowspan", "1") or "1")
                except ValueError:
                    rowspan = 1
                t = text_of(cell)
                for k in range(colspan):
                    if c_idx + k < width:
                        grid_row[c_idx + k] = t
                        if rowspan > 1:
                            rowspan_carry[c_idx + k] = (t, rowspan - 1)
                c_idx += colspan
            grid.append(grid_row)
        return grid

    def _build(self):
        # Find <table> children
        head_rows = []
        body_rows = []
        for tbl in self.tw.iter("table"):
            for thead in tbl.iter("thead"):
                for tr in thead.iter("tr"):
                    head_rows.append(tr)
            for tbody in tbl.iter("tbody"):
                for tr in tbody.iter("tr"):
                    body_rows.append(tr)
            if not head_rows and not body_rows:
                # rows directly under <table>; treat first row as header
                trs = [tr for tr in tbl.iter("tr")]
                if trs:
                    head_rows = trs[:1]
                    body_rows = trs[1:]
        head_grid = self._expand(head_rows)
        body_grid = self._expand(body_rows)
        # Normalize widths
        widths = [len(r) for r in head_grid + body_grid]
        if not widths:
            return
        width = max(widths)
        for r in head_grid + body_grid:
            while len(r) < width:
                r.append(None)
        self.grid = head_grid + body_grid
        self.header_row_count = len(head_grid)

    def column_label(self, col_idx: int) -> str:
        parts = []
        for r in range(self.header_row_count):
            if r < len(self.grid) and col_idx < len(self.grid[r]):
                v = self.grid[r][col_idx]
                if v and (not parts or parts[-1] != v):
                    parts.append(v)
        return " | ".join(parts)

    def column_labels(self) -> list[str]:
        if not self.grid:
            return []
        return [self.column_label(i) for i in range(len(self.grid[0]))]

    def row_label(self, row_idx_in_body: int) -> str:
        full_idx = self.header_row_count + row_idx_in_body
        if full_idx >= len(self.grid):
            return ""
        row = self.grid[full_idx]
        return row[0] or ""

    def body_rows(self):
        return self.grid[self.header_row_count:]

    def is_clock_relevant(self) -> bool:
        blob = self.caption.lower() + " " + " ".join(
            (c or "").lower() for c in self.column_labels()
        )
        return detect_clock(blob, self.clocks) is not None

    def extract(self, study_id: str, table_idx: int):
        out = []
        if not self.grid:
            return out
        col_labels = self.column_labels()
        cap_clock = detect_clock(self.caption, self.clocks)

        for body_i, row in enumerate(self.body_rows()):
            if not row:
                continue
            row_label = row[0] or ""
            rl = row_label.lower()
            clock_in_row = detect_clock(row_label, self.clocks)
            row_label_age_like = any(t in rl for t in [
                "age", "clock", "methylation", "dnam", "pace", "horvath",
                "hannum", "grimage", "phenoage", "acceleration", "dnamtl",
                "telomere",
            ])
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

            for col_i in range(1, len(row)):
                cell = row[col_i] or ""
                if not cell.strip():
                    continue
                col_blob = col_labels[col_i] if col_i < len(col_labels) else ""
                arm = row_arm or classify_arm(col_blob)
                tp = row_tp or classify_timepoint(col_blob)
                if not arm or not tp:
                    continue
                n_val = extract_n(col_blob) or extract_n(self.caption)
                for mean, disp, dtype, snip in extract_numeric_cells(cell):
                    out.append({
                        "study_id": study_id,
                        "clock": row_clock,
                        "arm": arm,
                        "timepoint": tp,
                        "value_type": "change_score" if tp == "change" else "raw_clock_age",
                        "mean": mean,
                        "dispersion": disp,
                        "dispersion_type": dtype,
                        "n": n_val,
                        "source_table_or_section": f"XML Table {table_idx} ({self.caption[:80]})",
                        "evidence_snippet": (
                            f"row='{row_label[:60]}' col='{col_blob[:60]}' cell='{snip}'"
                        )[:240],
                        "confidence": "high",
                    })
        return out


# ------------------------- XML prose -------------------------
def find_results_sections(root):
    for sec in root.iter("sec"):
        st = sec.get("sec-type", "") or ""
        title_el = sec.find("title")
        title = text_of(title_el) if title_el is not None else ""
        if "result" in st.lower() or "result" in title.lower():
            yield sec


def scan_prose(text, clock_list, study_id, source_label="Results (prose)"):
    out = []
    for sent in re.split(r"(?<=[.!?])\s+", text or ""):
        if len(sent) > 700 or len(sent) < 10:
            continue
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
            num_pos = sent.find(snip)
            clock_positions = []
            for c in clock_list + GENERIC_CLOCK_TERMS:
                p = sl.find(c.lower())
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
                "source_table_or_section": source_label,
                "evidence_snippet": (sent[:237] + "...") if len(sent) > 240 else sent,
                "confidence": "medium",
            })
    return out


# ------------------------- PDF -------------------------
def process_pdf(pdf_path: Path, clock_list, study_id):
    candidates = []
    n_tables_seen = 0
    if not HAS_PDFPLUMBER:
        return candidates, n_tables_seen
    try:
        with pdfplumber.open(str(pdf_path)) as pdf:
            for p_idx, page in enumerate(pdf.pages, start=1):
                # Tables
                try:
                    tables = page.extract_tables() or []
                except Exception:
                    tables = []
                for t_idx, tbl in enumerate(tables, start=1):
                    if not tbl or len(tbl) < 2:
                        continue
                    n_tables_seen += 1
                    candidates.extend(
                        _scan_pdf_table(tbl, clock_list, study_id, p_idx, t_idx)
                    )
                # Prose
                try:
                    text = page.extract_text() or ""
                except Exception:
                    text = ""
                if text:
                    if detect_clock(text, clock_list):
                        candidates.extend(
                            scan_prose(
                                text, clock_list, study_id,
                                source_label=f"PDF page {p_idx} (prose)",
                            )
                        )
    except Exception as e:
        log("pdf_parse_error", study_id=study_id, error=str(e))
    return candidates, n_tables_seen


def _scan_pdf_table(tbl, clock_list, study_id, page_idx, t_idx):
    out = []
    # First row is header
    header = [(c or "").strip() for c in tbl[0]]
    rows = tbl[1:]
    width = max(len(header), max((len(r) for r in rows), default=0))
    while len(header) < width:
        header.append("")
    caption_blob = " ".join(header)
    cap_clock = detect_clock(caption_blob, clock_list)
    for row in rows:
        cells = [(c or "").strip() for c in row]
        while len(cells) < width:
            cells.append("")
        if not cells or not cells[0]:
            continue
        row_label = cells[0]
        rl = row_label.lower()
        clock_in_row = detect_clock(row_label, clock_list)
        row_label_age_like = any(t in rl for t in [
            "age", "clock", "methylation", "dnam", "pace", "horvath",
            "hannum", "grimage", "phenoage", "acceleration", "dnamtl",
            "telomere",
        ])
        if clock_in_row:
            row_clock = clock_in_row
        elif row_label_age_like:
            row_clock = cap_clock
        else:
            row_clock = None
        if not row_clock:
            continue
        row_arm = classify_arm(row_label)
        row_tp = classify_timepoint(row_label)
        for ci in range(1, width):
            cell = cells[ci]
            if not cell:
                continue
            col_label = header[ci] if ci < len(header) else ""
            arm = row_arm or classify_arm(col_label)
            tp = row_tp or classify_timepoint(col_label)
            if not arm or not tp:
                continue
            n_val = extract_n(col_label)
            for mean, disp, dtype, snip in extract_numeric_cells(cell):
                out.append({
                    "study_id": study_id,
                    "clock": row_clock,
                    "arm": arm,
                    "timepoint": tp,
                    "value_type": "change_score" if tp == "change" else "raw_clock_age",
                    "mean": mean,
                    "dispersion": disp,
                    "dispersion_type": dtype,
                    "n": n_val,
                    "source_table_or_section": f"PDF p{page_idx} Table {t_idx}",
                    "evidence_snippet": (
                        f"row='{row_label[:60]}' col='{col_label[:60]}' cell='{snip}'"
                    )[:240],
                    "confidence": "high",
                })
    return out


# ------------------------- HTML -------------------------
def text_html(path: Path) -> str:
    try:
        raw = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
    raw = re.sub(r"(?is)<(script|style|noscript).*?</\1>", " ", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", html_lib.unescape(raw))


def process_html(html_path: Path, clock_list, study_id):
    text = text_html(html_path)
    if not text or not detect_clock(text, clock_list):
        return []
    return scan_prose(text, clock_list, study_id, source_label="HTML full text (prose)")


# ------------------------- XML driver -------------------------
def process_xml(xml_path: Path, clock_list, study_id):
    candidates = []
    n_grids = 0
    try:
        tree = ET.parse(str(xml_path))
    except ET.ParseError as e:
        log("xml_parse_error", study_id=study_id, error=str(e))
        return candidates, n_grids
    root = tree.getroot()
    for idx, tw in enumerate(root.iter("table-wrap"), start=1):
        try:
            grid = JATSTableGrid(tw, clock_list)
            if not grid.grid:
                continue
            n_grids += 1
            if not grid.is_clock_relevant():
                continue
            candidates.extend(grid.extract(study_id, idx))
        except Exception as e:
            log("xml_table_error", study_id=study_id, table_idx=idx, error=str(e))
    for sec in find_results_sections(root):
        prose = text_of(sec)
        candidates.extend(scan_prose(prose, clock_list, study_id))
    return candidates, n_grids


# ------------------------- Reconciliation -------------------------
def best_candidate(group):
    if not group:
        return None
    return sorted(
        group,
        key=lambda c: (
            0 if c["confidence"] == "high" else (1 if c["confidence"] == "medium" else 2),
            0 if "Table" in c["source_table_or_section"] else 1,
        ),
    )[0]


def reconcile(seed_rows, candidates):
    idx = defaultdict(list)
    for c in candidates:
        idx[(c["study_id"], c["clock"].lower())].append(c)

    complete = 0
    partial = 0
    not_reported = 0
    studies_with_any = set()

    for row in seed_rows:
        sid = row["study_id"]
        seed_clock = (row.get("clock") or "").strip()
        key = (sid, seed_clock.lower())
        cands = list(idx.get(key, []))
        if seed_clock.upper() == "UNSPECIFIED_EPIGENETIC_AGE" or not cands:
            for (s, c), v in idx.items():
                if s == sid:
                    if seed_clock.upper() == "UNSPECIFIED_EPIGENETIC_AGE":
                        cands.extend(v)
                    elif seed_clock.lower() == c:
                        cands.extend(v)
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

        studies_with_any.add(sid)
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
            row["baseline_int_mean"] = b_int["mean"]; row["baseline_int_sd"] = b_int["dispersion"]; any_filled = True
        if p_int:
            row["post_int_mean"] = p_int["mean"]; row["post_int_sd"] = p_int["dispersion"]; any_filled = True
        if b_ctrl:
            row["baseline_ctrl_mean"] = b_ctrl["mean"]; row["baseline_ctrl_sd"] = b_ctrl["dispersion"]; any_filled = True
        if p_ctrl:
            row["post_ctrl_mean"] = p_ctrl["mean"]; row["post_ctrl_sd"] = p_ctrl["dispersion"]; any_filled = True
        if c_int:
            row["change_int_mean"] = c_int["mean"]; row["change_int_sd"] = c_int["dispersion"]; any_filled = True
        if c_ctrl:
            row["change_ctrl_mean"] = c_ctrl["mean"]; row["change_ctrl_sd"] = c_ctrl["dispersion"]; any_filled = True

        n_ints = [c["n"] for c in cands if c["arm"] == "intervention" and c.get("n")]
        n_ctrls = [c["n"] for c in cands if c["arm"] == "control" and c.get("n")]
        if n_ints and not row.get("n_int"):
            row["n_int"] = max(n_ints); any_filled = True
        if n_ctrls and not row.get("n_ctrl"):
            row["n_ctrl"] = max(n_ctrls); any_filled = True

        full_pre_post = all([b_int, p_int, b_ctrl, p_ctrl])
        full_change = c_int and c_ctrl and row.get("n_int") and row.get("n_ctrl")
        if full_pre_post or full_change:
            row["extraction_status"] = "extracted_complete"
            complete += 1
            notes_bits.append("Full effect-size set extracted (enhanced).")
        elif any_filled:
            row["extraction_status"] = "extracted_partial"
            partial += 1
            notes_bits.append("Partial extraction (enhanced); some cells missing.")
        else:
            row["extraction_status"] = "not_reported"
            not_reported += 1

        sources = sorted({c["source_table_or_section"] for c in cands if c in (
            b_int, p_int, b_ctrl, p_ctrl, c_int, c_ctrl
        )})
        if sources:
            notes_bits.append("Sources: " + "; ".join(s[:80] for s in sources))
        if notes_bits:
            row["notes"] = " ".join(notes_bits)

    return complete, partial, not_reported, studies_with_any


# ------------------------- main -------------------------
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
        log("seed_missing", path=str(seed_csv)); sys.exit(1)
    with open(seed_csv, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        seed_rows = list(reader)
        seed_fields = reader.fieldnames

    study_ids = sorted({r["study_id"] for r in seed_rows})
    all_candidates = []
    n_xml_parsed = 0
    n_pdf_parsed = 0
    n_html_parsed = 0
    n_table_grids_built = 0

    for sid in study_ids:
        xml_path = ft_dir / f"{sid}.xml"
        pdf_path = ft_dir / f"{sid}.pdf"
        html_path = ft_dir / f"{sid}.html"
        if xml_path.exists() and xml_path.stat().st_size >= 200:
            try:
                cands, n_grids = process_xml(xml_path, clocks, sid)
                all_candidates.extend(cands)
                n_xml_parsed += 1
                n_table_grids_built += n_grids
                log("xml_parsed", study_id=sid, n_candidates=len(cands), n_grids=n_grids)
            except Exception as e:
                log("xml_fatal_error", study_id=sid, error=str(e), tb=traceback.format_exc()[:300])
        if pdf_path.exists() and pdf_path.stat().st_size >= 1000:
            try:
                cands, n_t = process_pdf(pdf_path, clocks, sid)
                all_candidates.extend(cands)
                n_pdf_parsed += 1
                n_table_grids_built += n_t
                log("pdf_parsed", study_id=sid, n_candidates=len(cands), n_tables=n_t)
            except Exception as e:
                log("pdf_fatal_error", study_id=sid, error=str(e), tb=traceback.format_exc()[:300])
        if html_path.exists() and html_path.stat().st_size >= 1000:
            try:
                cands = process_html(html_path, clocks, sid)
                all_candidates.extend(cands)
                n_html_parsed += 1
                log("html_parsed", study_id=sid, n_candidates=len(cands))
            except Exception as e:
                log("html_fatal_error", study_id=sid, error=str(e), tb=traceback.format_exc()[:300])

    # Confidence buckets
    n_high = sum(1 for c in all_candidates if c["confidence"] == "high")
    n_med = sum(1 for c in all_candidates if c["confidence"] == "medium")
    n_low = sum(1 for c in all_candidates if c["confidence"] == "low")

    # Write candidates CSV
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

    complete, partial, not_reported, studies_with_any = reconcile(seed_rows, all_candidates)

    with open(seed_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=seed_fields)
        w.writeheader()
        for r in seed_rows:
            w.writerow(r)

    log(
        "enhanced_extraction_done",
        n_xml_parsed=n_xml_parsed,
        n_pdf_parsed=n_pdf_parsed,
        n_html_parsed=n_html_parsed,
        n_table_grids_built=n_table_grids_built,
        n_candidates_high=n_high,
        n_candidates_medium=n_med,
        n_candidates_low=n_low,
        n_studies_with_any_extraction=len(studies_with_any),
        n_studies_complete=complete,
        n_studies_partial=partial,
        n_studies_not_reported=not_reported,
        candidates_csv=str(cand_csv),
        seed_csv=str(seed_csv),
    )


if __name__ == "__main__":
    main()
