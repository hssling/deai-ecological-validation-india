from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.utils.io import append_log, load_config, save_csv


META_DATASET_COLUMNS = [
    "study_id",
    "title",
    "year",
    "journal",
    "pmid",
    "pmcid",
    "doi",
    "intervention_name",
    "endpoint_family",
    "outcome_name",
    "outcome_timepoint",
    "effect_metric",
    "effect_direction_beneficial",
    "n_treatment",
    "n_control",
    "mean_treatment",
    "sd_treatment",
    "mean_control",
    "sd_control",
    "change_mean_treatment",
    "change_sd_treatment",
    "change_mean_control",
    "change_sd_control",
    "events_treatment",
    "events_control",
    "time_to_event_metric",
    "log_effect",
    "se_log_effect",
    "ci_lower",
    "ci_upper",
    "p_value",
    "extractor_method",
    "source_used",
    "source_locator",
    "verification_status",
    "duplicate_cohort_flag",
    "risk_of_bias_overall",
    "ready_for_pooling",
    "notes",
]


def _clean_text(value: object) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    text = str(value).strip()
    return "" if text.lower() == "nan" else text


def _bool_text(value: bool) -> str:
    return "yes" if value else "no"


def _endpoint_family(row: pd.Series) -> str:
    text = " ".join(
        [
            _clean_text(row.get("title", "")),
            _clean_text(row.get("outcome_exact", "")),
            _clean_text(row.get("ageing_domain_category", "")),
            _clean_text(row.get("intervention_name", "")),
        ]
    ).lower()
    if any(token in text for token in ["grip", "gait", "frailty", "tinetti", "barthel", "sarcopenia", "physical performance"]):
        return "frailty_function"
    if any(token in text for token in ["dnam", "epigenetic", "biological age", "phenoage", "grimage", "fitage", "telomere"]):
        return "epigenetic_biological_age"
    if any(token in text for token in ["mortality", "survival", "hazard ratio", "all-cause mortality", "death"]):
        return "mortality_survival"
    if any(token in text for token in ["cognition", "cognitive", "mmse", "memory"]):
        return "cognition"
    return "other"


def _study_id(row: pd.Series) -> str:
    for key in ["pmid", "pmcid", "doi"]:
        value = _clean_text(row.get(key, ""))
        if value:
            return value.replace("/", "_")
    title = _clean_text(row.get("title", "")).lower()
    return "_".join(title.split()[:8])[:80]


def _source_locator(row: pd.Series, open_cache: set[str]) -> tuple[str, str]:
    pmcid = _clean_text(row.get("pmcid", ""))
    pmid = _clean_text(row.get("pmid", ""))
    doi = _clean_text(row.get("doi", ""))
    url = _clean_text(row.get("url", ""))
    if pmcid and f"{pmcid}.xml" in open_cache:
        return "pmc_xml", f"data_processed/open_text_cache/{pmcid}.xml"
    if pmid and f"pubmed_{pmid}.xml" in open_cache:
        return "pubmed_xml", f"data_processed/open_text_cache/pubmed_{pmid}.xml"
    if url:
        return "publisher_html", url
    if doi:
        return "doi_landing_page", f"https://doi.org/{doi}"
    return "manual_lookup_required", ""


def _extractor_method(source_type: str, endpoint_family: str) -> str:
    if source_type == "pmc_xml":
        return "pmc_xml_table_text_parse"
    if source_type == "pubmed_xml":
        return "abstract_only_manual_completion"
    if endpoint_family in {"frailty_function", "epigenetic_biological_age", "cognition"}:
        return "table_first_then_figure_digitization_if_needed"
    return "manual_full_text_extraction"


def _figure_needed(row: pd.Series) -> bool:
    text = " ".join(
        [
            _clean_text(row.get("candidate_effect_size_text", "")),
            _clean_text(row.get("effect_size_final", "")),
            _clean_text(row.get("uncertainty_final", "")),
        ]
    ).lower()
    if not text:
        return True
    return any(token in text for token in ["p=", "p<", "significant", "improved", "decreased"]) and not any(
        token in text for token in ["95% ci", "eta-p2", "beta ", "hazard ratio", "hr ", "md ", "sd "]
    )


def _load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def run(cfg: dict) -> None:
    rt = cfg["paths"]["results_tables"]
    root = cfg["paths"]["meta_addon_root"]
    tables = cfg["paths"]["meta_addon_tables"]
    docs = cfg["paths"]["meta_addon_docs"]
    manuscript = cfg["paths"]["meta_addon_manuscript"]
    root.mkdir(parents=True, exist_ok=True)
    tables.mkdir(parents=True, exist_ok=True)
    docs.mkdir(parents=True, exist_ok=True)
    manuscript.mkdir(parents=True, exist_ok=True)

    extracted = _load_csv(rt / "extracted_studies_master.csv")
    queue = _load_csv(rt / "human_evidence_priority_queue.csv")
    verification = _load_csv(rt / "full_text_verification_priority_human.csv")
    effects = _load_csv(rt / "effect_size_extraction_priority_human.csv")
    duplicates = _load_csv(rt / "duplicate_cohort_checks.csv")
    rob = _load_csv(rt / "risk_of_bias_formal_preliminary_human.csv")

    merged = queue.merge(
        extracted[
            [
                "title",
                "authors",
                "year",
                "journal",
                "doi",
                "pmid",
                "study_design",
                "species_model",
                "intervention_name",
                "ageing_domain_category",
                "outcome_exact",
            ]
        ].drop_duplicates(subset=["title"]),
        on=["title", "year", "journal", "doi", "pmid", "study_design", "intervention_name", "ageing_domain_category"],
        how="left",
        suffixes=("", "_extracted"),
    )
    merged = merged.merge(
        verification[["title", "pmcid", "source_text_type", "verification_status"]].drop_duplicates(subset=["title"]),
        on="title",
        how="left",
    )
    merged = merged.merge(
        effects[
            [
                "title",
                "effect_size_extraction_status",
                "candidate_effect_size_text",
                "effect_size_final",
                "uncertainty_final",
            ]
        ].drop_duplicates(subset=["title"]),
        on="title",
        how="left",
    )
    merged = merged.merge(
        rob[["title", "rob_overall"]].drop_duplicates(subset=["title"]),
        on="title",
        how="left",
    )

    human = merged[merged["species_model"].fillna("").astype(str).str.lower().eq("human")].copy()
    empirical_mask = human["study_design"].fillna("").astype(str).str.contains(
        "RCT|trial|cohort|prospective|clinical", case=False, regex=True
    )
    human = human[empirical_mask].copy()
    human["endpoint_family"] = human.apply(_endpoint_family, axis=1)

    cache_dir = cfg["paths"]["data_processed"] / "open_text_cache"
    open_cache = {path.name for path in cache_dir.glob("*.xml")} if cache_dir.exists() else set()

    manifest_rows = []
    for _, row in human.iterrows():
        source_type, locator = _source_locator(row, open_cache)
        study_id = _study_id(row)
        figure_needed = _figure_needed(row)
        manifest_rows.append(
            {
                "study_id": study_id,
                "title": _clean_text(row.get("title", "")),
                "year": _clean_text(row.get("year", "")),
                "journal": _clean_text(row.get("journal", "")),
                "pmid": _clean_text(row.get("pmid", "")),
                "pmcid": _clean_text(row.get("pmcid", "")),
                "doi": _clean_text(row.get("doi", "")),
                "intervention_name": _clean_text(row.get("intervention_name", "")),
                "study_design": _clean_text(row.get("study_design", "")),
                "ageing_domain_category": _clean_text(row.get("ageing_domain_category", "")),
                "outcome_exact": _clean_text(row.get("outcome_exact", "")),
                "endpoint_family": _clean_text(row.get("endpoint_family", "")),
                "source_type": source_type,
                "source_locator": locator,
                "source_cached_locally": _bool_text(bool(locator.startswith("data_processed/open_text_cache/"))),
                "verification_status": _clean_text(row.get("verification_status", "")),
                "effect_size_extraction_status": _clean_text(row.get("effect_size_extraction_status", "")),
                "candidate_effect_size_text": _clean_text(row.get("candidate_effect_size_text", "")),
                "extractor_method": _extractor_method(source_type, _clean_text(row.get("endpoint_family", ""))),
                "needs_figure_digitization": _bool_text(figure_needed),
            }
        )
    manifest = pd.DataFrame(manifest_rows).drop_duplicates(subset=["study_id"])

    duplicate_text = ""
    if not duplicates.empty and "title" in duplicates.columns:
        duplicate_text = "|".join(duplicates["title"].astype(str).tolist()).lower()

    queue_rows = []
    for _, row in manifest.iterrows():
        extraction_status = "ready_for_numeric_extraction"
        if row["source_type"] in {"manual_lookup_required", "doi_landing_page"}:
            extraction_status = "needs_source_resolution"
        elif row["source_type"] == "pubmed_xml":
            extraction_status = "abstract_only_needs_full_text_or_supplement"
        elif row["needs_figure_digitization"] == "yes":
            extraction_status = "needs_table_or_figure_capture"
        queue_rows.append(
            {
                "study_id": row["study_id"],
                "title": row["title"],
                "intervention_name": row["intervention_name"],
                "endpoint_family": row["endpoint_family"],
                "source_type": row["source_type"],
                "extractor_method": row["extractor_method"],
                "extraction_status": extraction_status,
                "priority_rank": 0,
                "duplicate_cohort_flag": _bool_text(row["title"].lower() in duplicate_text if row["title"] else False),
                "notes": "Extract arm-level data first; if tables unavailable, inspect supplements and figures.",
            }
        )
    extraction_queue = pd.DataFrame(queue_rows)
    endpoint_order = {"frailty_function": 1, "epigenetic_biological_age": 2, "mortality_survival": 3, "cognition": 4, "other": 5}
    extraction_queue["priority_rank"] = extraction_queue.apply(
        lambda row: endpoint_order.get(row["endpoint_family"], 99) * 100
        + (0 if row["source_type"] == "pmc_xml" else 10)
        + (0 if row["duplicate_cohort_flag"] == "no" else 5),
        axis=1,
    )
    extraction_queue = extraction_queue.sort_values(["priority_rank", "title"]).reset_index(drop=True)

    endpoint_priority = (
        manifest.groupby("endpoint_family")
        .agg(
            n_studies=("study_id", "nunique"),
            pmc_xml_available=("source_type", lambda s: int((s == "pmc_xml").sum())),
            pubmed_xml_only=("source_type", lambda s: int((s == "pubmed_xml").sum())),
            figure_digitization_needed=("needs_figure_digitization", lambda s: int((s == "yes").sum())),
        )
        .reset_index()
        .sort_values(["n_studies", "pmc_xml_available"], ascending=[False, False])
    )

    figure_queue = manifest[manifest["needs_figure_digitization"].eq("yes")][
        ["study_id", "title", "intervention_name", "endpoint_family", "source_type", "source_locator"]
    ].copy()
    if not figure_queue.empty:
        figure_queue["recommended_tool"] = figure_queue["source_type"].map(
            {"pmc_xml": "webplotdigitizer_or_metaDigitise_from_embedded_figures", "pubmed_xml": "publisher_pdf_then_webplotdigitizer"}
        ).fillna("webplotdigitizer_or_metaDigitise")
        figure_queue["notes"] = "Use figure digitization only if exact numeric tables or supplements are unavailable."

    readiness_rows = []
    for _, row in manifest.iterrows():
        has_numeric_snippet = any(
            token in row["candidate_effect_size_text"].lower()
            for token in ["95% ci", "eta-p2", "beta ", "hr ", "hazard ratio", "md ", "mean "]
        )
        readiness_rows.append(
            {
                "study_id": row["study_id"],
                "title": row["title"],
                "endpoint_family": row["endpoint_family"],
                "source_type": row["source_type"],
                "has_numeric_snippet": _bool_text(has_numeric_snippet),
                "has_local_source": row["source_cached_locally"],
                "ready_for_pooling": "no",
                "reason_not_ready": "Arm-level summary statistics or model-level standard errors not yet extracted",
            }
        )
    readiness = pd.DataFrame(readiness_rows)

    dataset_template = pd.DataFrame(columns=META_DATASET_COLUMNS)

    tool_registry = pd.DataFrame(
        [
            {
                "tool_name": "GROBID",
                "purpose": "scholarly PDF structure and metadata extraction",
                "best_use": "references, sections, body structure",
                "url": "https://github.com/grobidOrg/grobid",
            },
            {
                "tool_name": "Docling",
                "purpose": "document conversion and table-aware extraction",
                "best_use": "complex PDF tables and mixed layouts",
                "url": "https://github.com/DS4SD/docling",
            },
            {
                "tool_name": "Marker",
                "purpose": "PDF to markdown/json conversion",
                "best_use": "quick structured capture from scientific PDFs",
                "url": "https://github.com/VikParuchuri/marker",
            },
            {
                "tool_name": "pdfplumber",
                "purpose": "text and table extraction with geometry control",
                "best_use": "machine-generated PDFs with irregular tables",
                "url": "https://github.com/jsvine/pdfplumber",
            },
            {
                "tool_name": "Camelot",
                "purpose": "rule-based PDF table extraction",
                "best_use": "bordered or lattice-like tables",
                "url": "https://camelot-py.readthedocs.io/",
            },
            {
                "tool_name": "Tabula",
                "purpose": "alternate PDF table extraction",
                "best_use": "manual rescue for difficult machine-generated tables",
                "url": "https://tabula.technology/",
            },
            {
                "tool_name": "OCRmyPDF",
                "purpose": "OCR text layer generation",
                "best_use": "scanned PDFs before parsing",
                "url": "https://github.com/ocrmypdf/OCRmyPDF",
            },
            {
                "tool_name": "WebPlotDigitizer",
                "purpose": "digitize plotted data from figures",
                "best_use": "when tables are unavailable but curves/bars are shown",
                "url": "https://automeris.io/docs/",
            },
            {
                "tool_name": "metaDigitise",
                "purpose": "reproducible R-based figure digitization",
                "best_use": "batch extraction from figures for meta-analysis",
                "url": "https://github.com/daniel1noble/metaDigitise",
            },
        ]
    )

    protocol_text = """# Meta-analysis Add-on Workflow

This add-on is a separate quantitative project layered on top of the broader anti-ageing evidence map.

## Scope
- Human empirical studies only.
- Endpoint-specific quantitative synthesis.
- Separate manuscript from the broad review.

## Priority endpoint families
1. Frailty and functional performance
2. Epigenetic / biological-age biomarkers
3. Mortality / survival
4. Cognition

## Extraction hierarchy
1. PMC XML / supplementary source data
2. Publisher HTML or machine-readable PDF
3. Table extraction from PDF
4. Figure digitization when tables are unavailable

## Minimum data required for pooling
- Arm sizes and means/SDs, or
- Change scores with uncertainty, or
- HR/OR/beta with corresponding standard errors or confidence intervals

## Exclusion from pooling
- p values without estimable effect size
- Protocol-only records
- Duplicate cohorts not adjudicated
- Nonhuman studies
"""

    manuscript_text = """# Quantitative Meta-analysis Add-on Manuscript

## Working title
Quantitative Meta-analysis of Human Anti-ageing Interventions: Frailty, Functional Performance, and Biological-age Biomarkers

## Current status
This manuscript is intentionally separate from the main review. It will include only studies with extractable quantitative data suitable for pooling.

## Planned sections
- Abstract
- Introduction
- Methods
- Results
- Discussion
- Limitations
- Conclusion

## Current quantitative rule
No pooled estimate will be reported until arm-level or model-level data are extracted into `meta_dataset_template.csv`.
"""

    save_csv(manifest, tables / "study_source_manifest.csv")
    save_csv(extraction_queue, tables / "meta_extraction_queue.csv")
    save_csv(endpoint_priority, tables / "endpoint_priority.csv")
    save_csv(figure_queue, tables / "figure_digitization_queue.csv")
    save_csv(readiness, tables / "meta_analysis_readiness_report.csv")
    save_csv(dataset_template, tables / "meta_dataset_template.csv")
    save_csv(tool_registry, tables / "tool_registry.csv")
    (docs / "workflow.md").write_text(protocol_text, encoding="utf-8")
    (manuscript / "manuscript_meta_addon.md").write_text(manuscript_text, encoding="utf-8")

    append_log(
        cfg["paths"]["logs"] / "progress.md",
        "Phase 22 - Meta-analysis Add-on Scaffolding",
        "- Created a separate quantitative meta-analysis add-on workflow.\n- Built source manifest, extraction queue, endpoint priority table, figure digitization queue, and meta-analysis dataset template.\n- Restricted add-on scope to human empirical studies and endpoint-specific pooling.",
        "- results/meta_addon/tables/study_source_manifest.csv\n- results/meta_addon/tables/meta_extraction_queue.csv\n- results/meta_addon/tables/endpoint_priority.csv\n- results/meta_addon/tables/figure_digitization_queue.csv\n- results/meta_addon/tables/meta_analysis_readiness_report.csv\n- results/meta_addon/tables/meta_dataset_template.csv\n- results/meta_addon/tables/tool_registry.csv\n- docs/meta_addon/workflow.md\n- manuscript/meta_addon/manuscript_meta_addon.md",
        "- Populate arm-level or model-level quantitative fields for priority endpoints.\n- Adjudicate duplicate cohorts before pooling.\n- Add actual effect-size computation and pooled models after extraction.",
        "- Current outputs identify extractable studies and source routes but do not infer missing statistics.\n- Figure digitization is a rescue path, not a first-line source when tables or supplements exist.",
        "python -m src.meta_addon.build_addon --config config/meta_addon_config.yaml",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/meta_addon_config.yaml")
    run(load_config(parser.parse_args().config))
