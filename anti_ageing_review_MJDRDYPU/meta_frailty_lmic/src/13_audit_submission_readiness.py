from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
from docx import Document


ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "tables"
DOCS = ROOT / "docs"
ASSET_DIR = ROOT / "submission_assets" / "IJMR_FRAILTY_INTERVENTIONS_AUDIT_READY_2026-05-18"


def load_csv(name: str) -> pd.DataFrame:
    candidates = [
        TABLES / name,
        ROOT / "data" / "processed" / name,
        ROOT / "data" / "interim" / name,
        ROOT / "data" / "raw" / name,
    ]
    for path in candidates:
        if path.exists():
            return pd.read_csv(path).fillna("")
    raise FileNotFoundError(name)


def doc_text(path: Path) -> str:
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)


def audit_row(domain: str, check: str, status: str, detail: str, action: str = "") -> dict[str, str]:
    return {"domain": domain, "check": check, "status": status, "detail": detail, "action": action}


def main() -> None:
    rows: list[dict[str, str]] = []

    search = load_csv("search_log.csv").iloc[0]
    screened = load_csv("screened_title_abstract.csv")
    title_counts = load_csv("title_abs_screening_counts.csv")
    priority = load_csv("screened_prioritized.csv")
    highconf = load_csv("high_confidence_extraction_queue.csv")
    workbook = load_csv("fulltext_verified_extraction_workbook.csv")
    fetch = load_csv("pmc_fulltext_fetch_log.csv")
    mining = load_csv("pmc_fulltext_mining.csv")
    outcome = load_csv("numeric_outcome_extraction_form.csv")
    rob2 = load_csv("rob2_assessment_form.csv")
    assignments = load_csv("dual_author_fulltext_assignments.csv")

    rows.append(
        audit_row(
            "search",
            "PubMed download count is internally consistent",
            "pass" if int(search["records_downloaded"]) == len(screened) else "fail",
            f"search_log records_downloaded={search['records_downloaded']}; screened_title_abstract rows={len(screened)}",
        )
    )
    rows.append(
        audit_row(
            "screening",
            "Title/abstract count sums to downloaded records",
            "pass" if int(title_counts["n"].sum()) == int(search["records_downloaded"]) else "fail",
            f"title_abs count sum={int(title_counts['n'].sum())}; records_downloaded={search['records_downloaded']}",
        )
    )
    rows.append(
        audit_row(
            "identifiers",
            "No duplicate PMIDs in screened records",
            "pass" if screened["pmid"].duplicated().sum() == 0 else "fail",
            f"duplicate PMIDs={int(screened['pmid'].duplicated().sum())}",
        )
    )
    rows.append(
        audit_row(
            "identifiers",
            "High-confidence extraction queue has unique PMIDs",
            "pass" if highconf["pmid"].duplicated().sum() == 0 else "fail",
            f"high-confidence rows={len(highconf)}; duplicate PMIDs={int(highconf['pmid'].duplicated().sum())}",
        )
    )
    rows.append(
        audit_row(
            "workbook",
            "Extraction workbook row count matches high-confidence queue",
            "pass" if len(workbook) == len(highconf) else "fail",
            f"workbook rows={len(workbook)}; high-confidence rows={len(highconf)}",
        )
    )
    rows.append(
        audit_row(
            "workbook",
            "Dual-author assignments match extraction workbook",
            "pass" if len(assignments) == len(workbook) else "fail",
            f"assignments rows={len(assignments)}; workbook rows={len(workbook)}",
        )
    )
    rows.append(
        audit_row(
            "full_text",
            "PMC fetch and mining counts match",
            "pass" if fetch["fetch_status"].eq("fetched").sum() == mining["parse_status"].eq("ok").sum() else "fail",
            f"fetch fetched={int(fetch['fetch_status'].eq('fetched').sum())}; mining ok={int(mining['parse_status'].eq('ok').sum())}",
        )
    )

    fetched = workbook[workbook["fulltext_access_status"].eq("pmc_fulltext_available")].copy()
    missing_paths = []
    for path in fetched["local_path"]:
        if not (ROOT / str(path)).exists():
            missing_paths.append(path)
    rows.append(
        audit_row(
            "full_text",
            "All PMC-mined local XML paths exist",
            "pass" if not missing_paths else "fail",
            f"missing local paths={len(missing_paths)}",
            "Refetch PMC XML if any path is missing.",
        )
    )

    doi_missing = int(workbook["doi"].astype(str).str.strip().eq("").sum())
    url_missing = int(workbook["url"].astype(str).str.strip().eq("").sum())
    pmcid_missing = int(workbook["pmcid"].astype(str).str.strip().eq("").sum())
    ref_meta = workbook[["pmid", "pmcid", "doi", "title", "year", "journal", "url", "fulltext_access_status"]].copy()
    ref_meta["pubmed_searchable"] = ref_meta["pmid"].astype(str).str.strip().ne("").map({True: "yes", False: "no"})
    ref_meta["doi_searchable"] = ref_meta["doi"].astype(str).str.strip().ne("").map({True: "yes", False: "no"})
    ref_meta["pmc_searchable"] = ref_meta["pmcid"].astype(str).str.strip().ne("").map({True: "yes", False: "no"})
    ref_meta.to_csv(TABLES / "reference_metadata_searchability_audit.csv", index=False)

    rows.append(
        audit_row(
            "references",
            "Candidate references are PubMed-searchable",
            "pass" if url_missing == 0 else "warning",
            f"PubMed URL missing={url_missing}; DOI missing={doi_missing}; PMCID missing={pmcid_missing}",
            "Final reference list still requires metadata verification after study inclusion.",
        )
    )

    final_include_filled = int(workbook["final_include"].astype(str).str.strip().ne("").sum())
    outcome_filled = int(outcome["converted_effect_size"].astype(str).str.strip().ne("").sum())
    rob_filled = int(rob2["judgement"].astype(str).str.strip().ne("").sum())
    rows.append(
        audit_row(
            "evidence_gate",
            "Final full-text inclusion decisions completed",
            "blocking_pending" if final_include_filled < len(workbook) else "pass",
            f"final_include filled={final_include_filled}/{len(workbook)}",
            "Complete author-verified full-text screening before submission.",
        )
    )
    rows.append(
        audit_row(
            "evidence_gate",
            "Numeric effect extraction completed",
            "blocking_pending" if outcome_filled == 0 else "partial",
            f"converted_effect_size filled={outcome_filled}/{len(outcome)}",
            "Extract outcome data before meta-analysis or NMA claims.",
        )
    )
    rows.append(
        audit_row(
            "evidence_gate",
            "RoB 2 judgements completed",
            "blocking_pending" if rob_filled == 0 else "partial",
            f"RoB 2 judgement filled={rob_filled}/{len(rob2)}",
            "Complete RoB 2 before final inference.",
        )
    )

    assets = {
        "first_page": ASSET_DIR / "IJMR_frailty_first_page_2026-05-18.docx",
        "declarations": ASSET_DIR / "IJMR_frailty_declarations_2026-05-18.docx",
        "manuscript_scaffold": ASSET_DIR / "IJMR_frailty_blinded_manuscript_scaffold_2026-05-18.docx",
        "figures_docx": ASSET_DIR / "IJMR_frailty_figures_2026-05-18.docx",
        "supplementary": ASSET_DIR / "IJMR_frailty_supplementary_2026-05-18.docx",
        "cover_letter": ASSET_DIR / "IJMR_frailty_cover_letter_hold_2026-05-18.docx",
        "figure1_png": ASSET_DIR / "figures" / "figure1_screening_progress_flow.png",
        "figure2_png": ASSET_DIR / "figures" / "figure2_preliminary_node_distribution.png",
    }
    for name, path in assets.items():
        rows.append(
            audit_row(
                "asset_presence",
                f"{name} exists",
                "pass" if path.exists() and path.stat().st_size > 0 else "fail",
                f"{path.name}; bytes={path.stat().st_size if path.exists() else 0}",
            )
        )

    ms_text = doc_text(assets["manuscript_scaffold"])
    figure_mentions = re.findall(r"Figure\s+(\d+)", ms_text)
    figure_sequence_ok = figure_mentions == sorted(figure_mentions, key=int) and {"1", "2"}.issubset(set(figure_mentions))
    rows.append(
        audit_row(
            "citation_sequence",
            "Manuscript scaffold cites figures sequentially",
            "pass" if figure_sequence_ok else "warning",
            f"figure mentions={','.join(figure_mentions) if figure_mentions else 'none'}",
            "Re-run after final manuscript expansion.",
        )
    )
    table_mentions = re.findall(r"Table\s+(\d+)", ms_text)
    rows.append(
        audit_row(
            "citation_sequence",
            "Main manuscript table citations",
            "warning" if not table_mentions else "pass",
            f"table mentions={','.join(table_mentions) if table_mentions else 'none in scaffold'}",
            "Add sequential table citations after final results tables are generated.",
        )
    )

    protocol_text = (DOCS / "prospero_registration_draft.md").read_text(encoding="utf-8")
    has_registration_number = bool(re.search(r"CRD\d+|registration number:\s*\S+", protocol_text, flags=re.I))
    rows.append(
        audit_row(
            "journal_gate",
            "Protocol registration number present",
            "blocking_pending" if not has_registration_number else "pass",
            "No PROSPERO/registry number detected in local draft.",
            "Register protocol and update title page/manuscript before IJMR submission.",
        )
    )

    rows.append(
        audit_row(
            "journal_gate",
            "Final PRISMA 2020 checklist ready",
            "blocking_pending",
            "Only progress-flow and extraction-preparation materials exist; final PRISMA checklist cannot be completed before final inclusion/synthesis.",
            "Complete final PRISMA checklist after extraction and synthesis.",
        )
    )

    audit = pd.DataFrame(rows)
    audit.to_csv(TABLES / "submission_readiness_audit.csv", index=False)
    audit.to_csv(ASSET_DIR / "submission_readiness_audit.csv", index=False)

    blocking = audit[audit["status"].eq("blocking_pending")]
    failures = audit[audit["status"].eq("fail")]
    warnings = audit[audit["status"].eq("warning")]
    decision = "NOT READY FOR JOURNAL SUBMISSION" if len(blocking) or len(failures) else "READY FOR AUTHOR SIGN-OFF"

    report = [
        "# Submission Readiness Audit",
        "",
        "Generated: 2026-05-18",
        "",
        f"## Decision: {decision}",
        "",
        f"- Pass checks: {int(audit['status'].eq('pass').sum())}",
        f"- Warnings: {len(warnings)}",
        f"- Failures: {len(failures)}",
        f"- Blocking pending items: {len(blocking)}",
        "",
        "## Blocking Items",
        "",
    ]
    if blocking.empty:
        report.append("None.")
    else:
        for _, row in blocking.iterrows():
            report.append(f"- {row['domain']} / {row['check']}: {row['detail']} Action: {row['action']}")
    report.extend(
        [
            "",
            "## Warnings",
            "",
        ]
    )
    if warnings.empty:
        report.append("None.")
    else:
        for _, row in warnings.iterrows():
            report.append(f"- {row['domain']} / {row['check']}: {row['detail']} Action: {row['action']}")
    report.extend(
        [
            "",
            "## Data Integrity Summary",
            "",
            f"- PubMed hits reported: {search['hits_reported']}",
            f"- PubMed records downloaded: {search['records_downloaded']}",
            f"- High-confidence extraction candidates: {len(highconf)}",
            f"- PMC full texts mined: {int(mining['parse_status'].eq('ok').sum())}",
            f"- Publisher/library full texts required: {int(workbook['fulltext_access_status'].eq('publisher_or_library_fulltext_required').sum())}",
            f"- Candidate DOI missing: {doi_missing}",
            "",
            "## Source Requirements Used for Audit",
            "",
            "- IJMR author instructions: IJMR lists Systematic Review including Meta-analysis as an article type, requires editable .docx source files, first page file, author undertaking/copyright forms, and uses double-blind peer review after technical screening. Source: https://ijmr.org.in/for-authors/",
            "- PRISMA 2020: systematic reviews should use the checklist and flow diagram framework. Source: https://www.prisma-statement.org/prisma-2020",
            "- PRISMA-NMA should be used if network meta-analysis proceeds. Source: https://www.prisma-statement.org/nma",
            "- RoB 2 is the planned risk-of-bias framework for randomized trials. Source: https://methods.cochrane.org/risk-bias-2",
        ]
    )
    report_text = "\n".join(report) + "\n"
    (DOCS / "submission_readiness_audit_2026-05-18.md").write_text(report_text, encoding="utf-8")
    (ASSET_DIR / "submission_readiness_audit_2026-05-18.md").write_text(report_text, encoding="utf-8")

    print(decision)
    print(f"passes={int(audit['status'].eq('pass').sum())}")
    print(f"warnings={len(warnings)}")
    print(f"failures={len(failures)}")
    print(f"blocking_pending={len(blocking)}")


if __name__ == "__main__":
    main()
