"""First-reviewer accessible full-text eligibility audit for DNAm clocks."""
from __future__ import annotations
import argparse
import html as html_lib
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).parent))
from _common import ensure_dirs, load_config, log  # noqa: E402

try:
    import pdfplumber  # type: ignore
except Exception:
    pdfplumber = None


CLOCK = re.compile(r"dunedinpace|grimage|phenoage|horvath|hannum|pcclock|dnamtl|epigenetic age|epigenetic clock|dna methylation age|dnam[- ]age|methylation age", re.I)
RCT = re.compile(r"randomi[sz]ed|randomly assigned|randomly allocated|placebo|control group|controlled trial|crossover|cross-over|parallel", re.I)
PROTOCOL = re.compile(r"study design and protocol|study protocol|protocol for|rationale, design|baseline characteristics|conference|abstract only", re.I)
OBS = re.compile(r"cross-sectional|observational|cohort|nhanes|association|predicting|machine learning|relationship intervention moderates", re.I)
NUMERIC = re.compile(r"mean|sd|standard deviation|95% ci|confidence interval|±|\([0-9.]+\)|p\s*[<=>]", re.I)


def text_xml(path: Path) -> str:
    try:
        root = ET.parse(path).getroot()
    except Exception:
        return ""
    return re.sub(r"\s+", " ", " ".join(root.itertext()))


def text_pdf(path: Path) -> str:
    if pdfplumber is None:
        return ""
    try:
        chunks = []
        with pdfplumber.open(str(path)) as pdf:
            for page in pdf.pages[:20]:
                chunks.append(page.extract_text() or "")
        return re.sub(r"\s+", " ", " ".join(chunks))
    except Exception:
        return ""


def text_html(path: Path) -> str:
    try:
        raw = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
    raw = re.sub(r"(?is)<(script|style|noscript).*?</\1>", " ", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", html_lib.unescape(raw))


def decide(title: str, abstract: str, fulltext: str, has_file: bool) -> tuple[str, str]:
    ta = f"{title} {abstract}"
    blob = f"{ta} {fulltext[:15000]}"
    if not has_file:
        return "await_fulltext", "No accessible XML/PDF/HTML full text in workspace"
    if PROTOCOL.search(ta) or PROTOCOL.search(fulltext[:15000]):
        return "exclude_fulltext", "Protocol/design/baseline-only/conference signal"
    if OBS.search(ta):
        return "exclude_fulltext", "Observational/association title-abstract signal"
    if not CLOCK.search(fulltext):
        return "exclude_fulltext", "DNAm clock outcome not confirmed in accessible full text"
    if not (RCT.search(ta) or RCT.search(fulltext[:20000])):
        return "exclude_fulltext", "Comparator randomized/intervention design not confirmed"
    if not NUMERIC.search(fulltext):
        return "defer_manual", "Clock outcome present but numeric reporting not captured"
    if re.search(r"single[- ]arm|single arm|within[- ]group only", blob, flags=re.I) and not re.search(r"control group|placebo|observation arm|usual care", blob, flags=re.I):
        return "secondary_noncomparative", "Single-arm or within-group design"
    return "include_accessible_first_reviewer", "Accessible full text confirms intervention/RCT signal and DNAm clock numeric reporting"


def run(cfg):
    freeze = cfg["project"]["freeze_date"]
    proc = Path(cfg["paths"]["data_processed"]); raw = Path(cfg["paths"]["data_raw"]); tabs = Path(cfg["paths"]["results_tabs"])
    ensure_dirs(proc, tabs)
    inc = pd.read_csv(proc / f"included_studies_{freeze}.csv").fillna("")
    rows = []
    for _, row in inc.iterrows():
        sid = row["study_id"]
        xml = raw / "fulltext" / f"{sid}.xml"
        pdf = raw / "fulltext" / f"{sid}.pdf"
        html = raw / "fulltext" / f"{sid}.html"
        ftxt = ""
        local_path = ""
        if xml.exists() and xml.stat().st_size > 200:
            ftxt = text_xml(xml); local_path = str(xml)
        elif pdf.exists() and pdf.stat().st_size > 1000:
            ftxt = text_pdf(pdf); local_path = str(pdf)
        elif html.exists() and html.stat().st_size > 1000:
            ftxt = text_html(html); local_path = str(html)
        decision, reason = decide(str(row.get("title", "")), str(row.get("abstract", "")), ftxt, bool(local_path))
        rows.append({
            "study_id": sid,
            "title": row.get("title", ""),
            "year": row.get("year", ""),
            "doi": row.get("doi", ""),
            "pmid": row.get("pmid", ""),
            "local_fulltext_path": local_path,
            "first_reviewer_fulltext_decision": decision,
            "first_reviewer_reason": reason,
            "clock_signal": "yes" if CLOCK.search(ftxt) else "no",
            "rct_signal": "yes" if RCT.search(ftxt) else "no",
            "numeric_signal": "yes" if NUMERIC.search(ftxt) else "no",
            "second_reviewer_decision": "",
            "consensus_decision": "",
            "consensus_reason": "",
        })
    out = pd.DataFrame(rows)
    out.to_csv(proc / f"fulltext_eligibility_audit_{freeze}.csv", index=False)
    out["first_reviewer_fulltext_decision"].value_counts().rename_axis("decision").reset_index(name="n").to_csv(
        tabs / f"fulltext_eligibility_audit_counts_{freeze}.csv", index=False
    )
    log("fulltext_eligibility_audit_done", **out["first_reviewer_fulltext_decision"].value_counts().to_dict())


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True)
    run(load_config(ap.parse_args().config))
