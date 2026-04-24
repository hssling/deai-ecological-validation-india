from __future__ import annotations

import argparse
import re
import time
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

import pandas as pd
import requests

from src.dedup.deduplicate import norm_title
from src.utils.io import append_log, load_config, save_csv


AGEING_TERMS = [
    "frailty",
    "healthspan",
    "lifespan",
    "mortality",
    "survival",
    "biological age",
    "dna methylation age",
    "epigenetic",
    "senescence",
    "gait",
    "grip",
    "cognition",
    "physical performance",
    "disability",
]

INTERVENTION_TERMS = [
    "exercise",
    "resistance training",
    "physical activity",
    "caloric restriction",
    "calorie restriction",
    "fasting",
    "fasting-mimicking",
    "metformin",
    "rapamycin",
    "sirolimus",
    "nad",
    "nmn",
    "nicotinamide riboside",
    "senolytic",
    "fisetin",
    "dasatinib",
    "quercetin",
    "microbiome",
    "probiotic",
    "lifestyle",
]

EFFECT_PATTERN = re.compile(
    r"(?i)(?:mean difference|hazard ratio|odds ratio|risk ratio|relative risk|"
    r"standardized mean difference|beta|β|cohen'?s d|effect size|"
    r"p\s*[<=>]\s*0?\.\d+|95%\s*ci|confidence interval|"
    r"\b\d+(?:\.\d+)?\s*%|\b[-+]?\d+\.\d+\b)"
)


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def xml_text(elem: ET.Element | None) -> str:
    if elem is None:
        return ""
    return clean_text(" ".join(elem.itertext()))


def fetch_pubmed_xml(pmid: str, email: str = "") -> str:
    if not pmid or str(pmid).lower() == "nan":
        return ""
    pmid = str(pmid).split(".")[0]
    params = {"db": "pubmed", "id": pmid, "retmode": "xml"}
    if email:
        params["email"] = email
    r = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi", params=params, timeout=25)
    if r.ok:
        return r.text
    return ""


def fetch_pmc_xml(pmcid: str, email: str = "") -> str:
    if not pmcid or str(pmcid).lower() == "nan":
        return ""
    pmcid = str(pmcid).upper().replace("PMC", "")
    params = {"db": "pmc", "id": pmcid, "retmode": "xml"}
    if email:
        params["email"] = email
    r = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi", params=params, timeout=30)
    if r.ok:
        return r.text
    return ""


def parse_pubmed(xml: str) -> dict[str, str]:
    if not xml:
        return {"source_text_type": "not_retrieved", "title_verified": "", "abstract_text": "", "body_text": ""}
    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        return {"source_text_type": "parse_failed", "title_verified": "", "abstract_text": "", "body_text": ""}
    title = xml_text(root.find(".//ArticleTitle"))
    abstracts = [xml_text(x) for x in root.findall(".//AbstractText")]
    return {
        "source_text_type": "pubmed_abstract",
        "title_verified": title,
        "abstract_text": clean_text(" ".join(abstracts)),
        "body_text": "",
    }


def parse_pmc(xml: str) -> dict[str, str]:
    if not xml:
        return {"source_text_type": "not_retrieved", "title_verified": "", "abstract_text": "", "body_text": ""}
    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        return {"source_text_type": "parse_failed", "title_verified": "", "abstract_text": "", "body_text": ""}
    title = xml_text(root.find(".//article-title"))
    abstract = xml_text(root.find(".//abstract"))
    body = xml_text(root.find(".//body"))
    return {
        "source_text_type": "pmc_open_full_text" if body else "pmc_metadata_or_abstract",
        "title_verified": title,
        "abstract_text": abstract,
        "body_text": body[:250000],
    }


def text_flags(text: str, intervention_name: str) -> dict[str, object]:
    low = text.lower()
    intervention_hits = sorted({term for term in INTERVENTION_TERMS if term in low})
    ageing_hits = sorted({term for term in AGEING_TERMS if term in low})
    if intervention_name and intervention_name not in {"unclear", "controversial"}:
        intervention_hits.append(str(intervention_name).replace("_", " "))
    return {
        "intervention_terms_found": "; ".join(sorted(set(intervention_hits))),
        "ageing_terms_found": "; ".join(ageing_hits),
        "has_intervention_signal": bool(intervention_hits),
        "has_ageing_outcome_signal": bool(ageing_hits),
    }


def effect_candidates(text: str, limit: int = 8) -> tuple[str, str]:
    if not text:
        return "", "not_extracted_no_source_text"
    matches = []
    for match in EFFECT_PATTERN.finditer(text):
        start = max(match.start() - 80, 0)
        end = min(match.end() + 80, len(text))
        snippet = clean_text(text[start:end])
        if snippet and snippet not in matches:
            matches.append(snippet)
        if len(matches) >= limit:
            break
    if matches:
        return " || ".join(matches), "candidate_numeric_effect_text_extracted"
    return "", "no_candidate_effect_text_found"


def rob_from_text(row: pd.Series, text: str) -> dict[str, str]:
    design = str(row.get("study_design", "")).lower()
    low = text.lower()
    title = str(row.get("title", "")).lower()
    is_trial = "rct" in design or "clinical_trial" in design or (
        "unclear" in design and any(x in title for x in ["randomized", "randomised", "trial"])
    )
    is_cohort = "cohort" in design or "cohort" in low

    if is_trial:
        randomization = "low_concern" if "random" in low else "some_concern"
        blinding = "low_concern" if any(x in low for x in ["blind", "masked", "placebo"]) else "some_concern"
        missing = "some_concern" if any(x in low for x in ["dropout", "lost to follow-up", "missing"]) else "unclear"
        confounding = "low_concern_rct_design"
    elif is_cohort:
        randomization = "not_applicable"
        blinding = "not_applicable_or_unclear"
        missing = "some_concern" if any(x in low for x in ["lost to follow-up", "missing"]) else "unclear"
        confounding = "some_concern_observational_confounding"
    else:
        randomization = "unclear_or_not_applicable"
        blinding = "unclear_or_not_applicable"
        missing = "unclear"
        confounding = "serious_or_unclear"

    outcome_measurement = "some_concern" if row.get("ageing_domain_category") == "surrogate_or_indirect" else "low_or_some_concern"
    selective_reporting = "unclear_without_protocol"
    overall = "some_concern"
    if any(v.startswith("serious") for v in [confounding]):
        overall = "serious_or_unclear"
    elif is_trial and randomization == "low_concern" and blinding == "low_concern":
        overall = "low_to_some_concern_pending_full_text_review"

    return {
        "rob_randomization": randomization,
        "rob_blinding": blinding,
        "rob_missing_data": missing,
        "rob_confounding": confounding,
        "rob_outcome_measurement": outcome_measurement,
        "rob_selective_reporting": selective_reporting,
        "rob_overall": overall,
    }


def duplicate_cohort_checks(records: pd.DataFrame) -> pd.DataFrame:
    if records.empty:
        return pd.DataFrame()
    rows = []
    work = records.copy()
    work["title_norm"] = work["title"].fillna("").map(norm_title)
    work["cohort_key"] = work["title_norm"].str.replace(
        r"\b(results|protocol|baseline|secondary analysis|study design|rationale)\b",
        "",
        regex=True,
    ).str.strip()
    trial_regex = re.compile(r"\b([A-Z][A-Z0-9-]{2,}|CALERIE|PEARL|TRIAD|PROMOTe|VIVIFRAIL|SINGER)\b")
    work["trial_acronyms"] = work["title"].fillna("").map(lambda x: "; ".join(sorted(set(trial_regex.findall(x)))))
    for key_col in ["doi", "pmid", "title_norm", "trial_acronyms", "cohort_key"]:
        vals = work[work[key_col].fillna("").astype(str).str.len() > 0]
        for key, group in vals.groupby(key_col):
            if len(group) > 1:
                rows.append({
                    "check_type": key_col,
                    "duplicate_key": key,
                    "n_records": len(group),
                    "titles": " || ".join(group["title"].astype(str).head(10)),
                    "manual_action": "review_for_duplicate_publication_or_overlapping_cohort",
                })
    return pd.DataFrame(rows).drop_duplicates() if rows else pd.DataFrame(columns=[
        "check_type", "duplicate_key", "n_records", "titles", "manual_action"
    ])


def run(cfg):
    rt = cfg["paths"]["results_tables"]
    queue = pd.read_csv(rt / "human_evidence_priority_queue.csv")
    status = pd.read_csv(rt / "full_text_status.csv")
    extracted = pd.read_csv(rt / "extracted_studies_master.csv")
    max_records = int(cfg.get("full_text_verification", {}).get("max_priority_human_records", 40))
    email = cfg.get("project", {}).get("email", "")

    queue = queue.head(max_records).merge(
        status[["title", "pmcid", "abstract", "retrieved_at"]],
        how="left",
        on="title",
    )
    verification_rows = []
    effect_rows = []
    rob_rows = []

    cache_dir = cfg["_root"] / "data_processed" / "open_text_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)

    for _, row in queue.iterrows():
        pmcid = str(row.get("pmcid", "") or "")
        pmid = str(row.get("pmid", "") or "")
        parsed = {"source_text_type": "not_retrieved", "title_verified": "", "abstract_text": "", "body_text": ""}
        source_id = ""

        if pmcid and pmcid.lower() != "nan":
            xml = fetch_pmc_xml(pmcid, email=email)
            parsed = parse_pmc(xml)
            source_id = pmcid
            if xml:
                (cache_dir / f"{pmcid}.xml").write_text(xml, encoding="utf-8", errors="ignore")
            time.sleep(0.34)

        if parsed["source_text_type"] in {"not_retrieved", "parse_failed", "pmc_metadata_or_abstract"} and pmid and pmid.lower() != "nan":
            xml = fetch_pubmed_xml(pmid, email=email)
            pubmed = parse_pubmed(xml)
            if pubmed["abstract_text"]:
                parsed = pubmed
                source_id = pmid
                (cache_dir / f"pubmed_{pmid.split('.')[0]}.xml").write_text(xml, encoding="utf-8", errors="ignore")
            time.sleep(0.34)

        source_text = clean_text(" ".join([parsed["abstract_text"], parsed["body_text"]]))
        if not source_text and str(row.get("abstract", "")).lower() != "nan":
            source_text = clean_text(str(row.get("abstract", "")))
            parsed["source_text_type"] = "repo_abstract_only"

        flags = text_flags(source_text, str(row.get("intervention_name", "")))
        effect_text, effect_status = effect_candidates(source_text)
        full_text_verified = parsed["source_text_type"] == "pmc_open_full_text"
        abstract_verified = parsed["source_text_type"] in {"pubmed_abstract", "repo_abstract_only", "pmc_metadata_or_abstract"}

        verification_status = "open_full_text_verified" if full_text_verified else (
            "abstract_verified_full_text_pending" if abstract_verified else "not_verified_source_unavailable"
        )
        eligibility = "eligible_pending_manual_confirmation" if (
            flags["has_intervention_signal"] and flags["has_ageing_outcome_signal"] and verification_status != "not_verified_source_unavailable"
        ) else "uncertain_or_pending_source_review"

        verification_rows.append({
            "title": row.get("title", ""),
            "pmid": pmid,
            "pmcid": pmcid,
            "source_id": source_id,
            "source_text_type": parsed["source_text_type"],
            "verification_status": verification_status,
            "provisional_full_text_eligibility": eligibility,
            "title_verified": parsed["title_verified"],
            "has_intervention_signal": flags["has_intervention_signal"],
            "has_ageing_outcome_signal": flags["has_ageing_outcome_signal"],
            "intervention_terms_found": flags["intervention_terms_found"],
            "ageing_terms_found": flags["ageing_terms_found"],
            "manual_verification_required": True,
        })
        effect_rows.append({
            "title": row.get("title", ""),
            "intervention_name": row.get("intervention_name", ""),
            "ageing_domain_category": row.get("ageing_domain_category", ""),
            "effect_size_extraction_status": effect_status,
            "candidate_effect_size_text": effect_text,
            "effect_size_final": "",
            "uncertainty_final": "",
            "manual_extraction_required": True,
        })
        rob_rows.append({"title": row.get("title", ""), **rob_from_text(row, source_text)})

    verification = pd.DataFrame(verification_rows)
    effects = pd.DataFrame(effect_rows)
    rob = pd.DataFrame(rob_rows)
    duplicates = duplicate_cohort_checks(extracted)

    save_csv(verification, rt / "full_text_verification_priority_human.csv")
    save_csv(effects, rt / "effect_size_extraction_priority_human.csv")
    save_csv(rob, rt / "risk_of_bias_formal_preliminary_human.csv")
    save_csv(duplicates, rt / "duplicate_cohort_checks.csv")

    append_log(
        cfg["paths"]["logs"] / "progress.md",
        "Phase 5b-7b - Priority Human Full-Text Verification, RoB, Duplicate Checks, and Effect Extraction",
        f"- Attempted open full-text or PubMed/repo abstract verification for the top {len(queue)} prioritized human records.\n- Created preliminary formal RoB domains for prioritized human records.\n- Created candidate effect-size extraction table with manual-verification flags.\n- Ran duplicate cohort/publication checks across {len(extracted)} extracted candidate records.",
        "- results/tables/full_text_verification_priority_human.csv\n- results/tables/effect_size_extraction_priority_human.csv\n- results/tables/risk_of_bias_formal_preliminary_human.csv\n- results/tables/duplicate_cohort_checks.csv\n- data_processed/open_text_cache/*.xml",
        "- Manual full-text reading remains required for final eligibility, final RoB, and final effect sizes.",
        "- Automated extraction is limited to open full text, PubMed abstracts, and repository abstracts; candidate effect snippets are not final quantitative data.",
        "python -m src.viz.make_figures --config config/review_config.yaml",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/review_config.yaml")
    run(load_config(parser.parse_args().config))
