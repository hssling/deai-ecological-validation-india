"""Phase 12: build honest manuscript and submission-readiness assets."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt
sys.path.insert(0, str(Path(__file__).parent))
from _common import ensure_dirs, load_config, log  # noqa: E402


TITLE = "Human interventions and DNA-methylation biological ageing clocks: systematic review execution report with meta-analysis hard stop"


def style(doc):
    s = doc.styles["Normal"]; s.font.name = "Times New Roman"; s.font.size = Pt(12)


def add_table(doc, df):
    table = doc.add_table(rows=1, cols=len(df.columns)); table.style = "Table Grid"
    for i, c in enumerate(df.columns): table.rows[0].cells[i].text = str(c)
    for _, row in df.iterrows():
        cells = table.add_row().cells
        for i, c in enumerate(df.columns): cells[i].text = str(row[c])


def run(cfg):
    freeze = cfg["project"]["freeze_date"]
    proc = Path(cfg["paths"]["data_processed"]); tabs = Path(cfg["paths"]["results_tabs"])
    figs = Path(cfg["paths"]["results_figs"]); sub = Path(cfg["paths"]["submission"]); docs_dir = Path(cfg["paths"]["docs"])
    ensure_dirs(sub, docs_dir)
    raw = pd.read_csv(Path(cfg["paths"]["data_interim"]) / f"raw_records_dnam_{freeze}.csv")
    included = pd.read_csv(proc / f"included_studies_{freeze}.csv").fillna("")
    extracted = pd.read_csv(proc / f"extracted_clock_studies_{freeze}.csv").fillna("")
    gates = pd.read_csv(tabs / f"pooling_gate_status_{freeze}.csv").fillna("")
    effects = pd.read_csv(tabs / f"effect_size_candidates_{freeze}.csv").fillna("")
    calc = effects[effects["effect_status"].eq("calculated_candidate")].copy()

    doc = Document(); style(doc)
    doc.add_heading(TITLE, 0)
    doc.add_paragraph("Authors: Dr Siddalingaiah H S; Dr Chandrakala D")
    doc.add_paragraph(f"Target journal: {cfg['project'].get('target_journal', 'Indian Journal of Medical Research')}")
    ft_path = proc / f"fulltext_eligibility_audit_{freeze}.csv"
    ft = pd.read_csv(ft_path).fillna("") if ft_path.exists() else pd.DataFrame()
    ft_counts = pd.read_csv(Path(cfg["paths"]["results_tabs"]) / f"fulltext_eligibility_audit_counts_{freeze}.csv").fillna("") if ft_path.exists() else pd.DataFrame()
    n_ft_include = int(ft["first_reviewer_fulltext_decision"].eq("include_accessible_first_reviewer").sum()) if not ft.empty else "NA"
    n_ft_exclude = int(ft["first_reviewer_fulltext_decision"].eq("exclude_fulltext").sum()) if not ft.empty else "NA"
    n_ft_await = int(ft["first_reviewer_fulltext_decision"].eq("await_fulltext").sum()) if not ft.empty else "NA"

    doc.add_heading("Abstract", 1)
    doc.add_paragraph(
        f"Background: DNA-methylation (DNAm) ageing clocks are increasingly used as surrogate biomarkers in trials of lifestyle, nutritional, "
        f"pharmacological and behavioural interventions, but their randomized evidence base is unevenly reported. Objective: To execute a strict "
        f"RCT-only systematic review workflow and determine whether intervention effects on validated DNAm clocks can be meta-analysed without "
        f"fabricating unavailable data. Methods: Searches of cached PubMed/MEDLINE, Europe PMC, Crossref, OpenAlex and ClinicalTrials.gov records "
        f"were screened against protocol eligibility. Accessible XML/PDF/HTML full texts were audited, and numeric DNAm-clock outcomes were extracted only "
        f"where arm, timepoint, mean, dispersion and sample size could be inferred transparently. Results: The search layer contained {len(raw)} raw "
        f"records. Abstract screening produced {len(included)} included-pending-verification records; accessible full-text audit reduced this to "
        f"{n_ft_include} first-reviewer accessible includes, "
        f"with {n_ft_exclude} exclusions and "
        f"{n_ft_await} records awaiting full text. Enhanced extraction produced "
        f"{len(extracted)} clock-outcome rows, but only {len(calc)} candidate effect-size row was complete. No named clock met the prespecified threshold "
        f"of three real effect estimates. Conclusion: A quantitative meta-analysis, network meta-analysis, publication-bias assessment and GRADE profile "
        f"are not supportable from the verified extracted dataset. The correct current output is a transparent systematic evidence map and hard-stop report."
    )
    doc.add_heading("Introduction", 1)
    doc.add_paragraph(
        "DNAm ageing clocks estimate biological-age-related signatures from methylation profiles and are frequently discussed as candidate surrogate outcomes "
        "for geroscience trials. The appeal is obvious: a clock can potentially detect biological change before disease events accrue. The danger is equally "
        "obvious: a biomarker can become rhetorically stronger than the data supporting it. Intervention studies now report DunedinPACE, GrimAge, PhenoAge, "
        "Horvath, Hannum and other methylation-derived measures, but reporting formats vary across trials, cell types, arrays, model versions and analysis scales."
    )
    doc.add_paragraph(
        "This project was designed to answer a narrow methodological question before making any biological claim: are human randomized intervention studies "
        "reporting DNAm-clock outcomes sufficiently and comparably to support a quantitative meta-analysis? The protocol intentionally required comparator "
        "arms and extractable pre/post or change-score data. This stricter threshold protects against a common failure mode in biomarker reviews: pooling "
        "directional claims, adjusted regression coefficients, within-arm p values and narrative statements as if they were the same evidence object."
    )
    doc.add_heading("Methods", 1)
    doc.add_paragraph(
        "The review followed an RCT-only protocol. Eligible reports had to describe a deliberate human intervention, a comparator arm, and at least one validated "
        "DNAm ageing measure. Outcomes of interest were DunedinPACE, GrimAge, GrimAge2, PhenoAge, Horvath, Hannum, PCClock and DNAmTL; generic epigenetic-age "
        "measures were retained separately when the exact clock could not be assigned."
    )
    doc.add_paragraph(
        "The search and screening workflow used cached API outputs from PubMed/MEDLINE, Europe PMC, Crossref, OpenAlex and ClinicalTrials.gov. Title/abstract "
        "screening was followed by accessible full-text auditing. XML files were parsed through JATS table grids; PDFs were parsed with pdfplumber where possible; "
        "rescued HTML full texts were scanned as prose. "
        "The extraction algorithm required explicit arm, timepoint, mean, dispersion and sample size. Ambiguous cells were skipped. This is conservative, but it "
        "keeps the review reproducible and prevents false precision."
    )
    doc.add_paragraph(
        "For a candidate Hedges g, the preferred effect was intervention-minus-control change from baseline using arm-level change means and standard deviations. "
        "Where only within-arm significance or adjusted regression results were reported, those results were not converted into arm-level SMDs. The prespecified "
        "minimum for pooling was three real effect estimates per clock. Subgroup analysis and publication-bias tests required larger thresholds as specified in "
        "the protocol. NMA was conditional on at least ten studies and a connected intervention-class network."
    )
    doc.add_paragraph(
        "Risk-of-bias forms were seeded for included records, but formal RoB 2 judgements remain pending because outcome-level bias assessment is meaningful only "
        "after final full-text inclusion and outcome selection. This distinction is important: a study may be randomized and relevant, yet still be unusable for "
        "a specific DNAm-clock synthesis if the clock result is exploratory, selectively reported, figure-only, adjusted without arm-level values, or measured in "
        "a cell subset that is not comparable with other studies."
    )
    doc.add_heading("Results", 1)
    doc.add_paragraph(
        f"The search layer produced {len(raw)} raw records. After candidate screening, {len(included)} records were labelled included-pending-full-text verification. "
        "This abstract-level set contained genuine RCTs but also protocols, observational analyses and records without accessible full text. The accessible "
        "full-text audit therefore supersedes the abstract-only label for scientific interpretation."
    )
    if not ft_counts.empty:
        doc.add_heading("Table 1. Accessible full-text eligibility audit", 2)
        add_table(doc, ft_counts)
    doc.add_paragraph(
        f"Enhanced extraction produced {len(extracted)} study-clock rows. Extraction status was: {extracted['extraction_status'].value_counts().to_dict()}. "
        f"Only {len(calc)} row was complete enough to calculate a candidate Hedges g. That row came from Lukkahatai et al. and used an unspecified epigenetic-age "
        "measure in a very small feasibility study. It is not a sufficient basis for a clock-specific meta-analysis and requires author verification of direction."
    )
    doc.add_paragraph(
        "Several studies remain scientifically important despite not producing a poolable row. For example, some report within-arm changes in PCGrimAge or "
        "PCPhenoAge, some examine dietary patterns or supplements in randomized designs, and others report DNAm measures in specialized populations or tissues. "
        "The limitation is not lack of biological interest; it is lack of harmonized extractable arm-level reporting. These records should be retained in an "
        "evidence map and targeted for supplementary-data extraction or author contact."
    )
    doc.add_heading("Table 2. Pooling gate status", 2)
    add_table(doc, gates)
    if not calc.empty:
        doc.add_heading("Table 3. Candidate effect-size row requiring author verification", 2)
        add_table(doc, calc[["study_id", "clock", "intervention_class", "hedges_g", "se", "ci95_low", "ci95_high", "reason"]])
    doc.add_heading("Figures", 1)
    for fig_name, caption in [
        (f"pipeline_status_{freeze}.png", "Figure 1. DNAm clocks review evidence pipeline status."),
        (f"extraction_status_{freeze}.png", "Figure 2. Numeric extraction status."),
    ]:
        path = figs / fig_name
        if path.exists():
            doc.add_paragraph(caption)
            doc.add_picture(str(path), width=Inches(6.2))
    doc.add_heading("Discussion", 1)
    doc.add_paragraph(
        "The principal finding is not a pooled effect; it is evidentiary insufficiency under strict review rules. Several accessible full texts discuss DNAm clocks "
        "in intervention settings, but many do not report arm-level clock means and dispersions in a format that can be converted transparently into between-arm "
        "change effects. Some report within-arm p values, adjusted model coefficients, figures without extractable numeric tables, cell-type-specific exploratory "
        "analyses, or observational associations. These are scientifically useful but not interchangeable with randomized arm-level effect estimates."
    )
    doc.add_paragraph(
        "This hard stop is informative. It indicates that the field has moved faster in biomarker adoption than in standardized trial reporting. Future trials should "
        "report clock values by arm at baseline and follow-up, change scores with SDs, sample sizes at each timepoint, clock version, tissue or cell type, array platform, "
        "normalization pipeline and whether estimates are residualized for chronological age or cell composition. Without these details, systematic reviewers are forced "
        "to choose between underpowered narrative synthesis and analytically fragile conversions."
    )
    doc.add_paragraph(
        "The current dataset should therefore be treated as a systematic evidence map and extraction audit. It identifies which studies are likely relevant, which full "
        "texts remain unavailable, which reports are ineligible after full-text review, and where author data requests should be targeted. A later meta-analysis may "
        "become possible if arm-level data are extracted manually from supplementary files, obtained from authors, or reported in future publications."
    )
    doc.add_heading("Implications for DNAm-clock trial reporting", 1)
    doc.add_paragraph(
        "The review highlights a reporting gap that is fixable. Trials using DNAm clocks should report, for each randomized arm, the sample size at baseline and "
        "follow-up, clock mean and SD at each timepoint, change-score mean and SD, clock version, tissue or sorted cell type, methylation array, preprocessing "
        "pipeline, cell-composition adjustment, and whether values are raw clock ages, age-acceleration residuals, principal-component clocks, or pace measures. "
        "If only adjusted model estimates are reported, authors should provide enough information to map those estimates to synthesis-ready contrasts."
    )
    doc.add_paragraph(
        "The field also needs conceptual discipline. DunedinPACE, GrimAge, PhenoAge, Horvath, Hannum and DNAmTL do not measure the same construct. Pooling across "
        "them as a single 'biological ageing' endpoint would be analytically convenient but biologically weak. Even within a clock family, PC versions and original "
        "versions should not be automatically combined. A future quantitative synthesis should therefore pool only within clearly defined clock versions or use "
        "structured multilevel models after enough data exist."
    )
    doc.add_heading("Planned rescue workflow", 1)
    doc.add_paragraph(
        f"The next phase should focus on data rescue rather than manuscript packaging. First, the {n_ft_await} records awaiting full text should be retrieved through library "
        f"access, author correspondence or preprint repositories. Second, the {n_ft_include} accessible first-reviewer includes should undergo independent second-reviewer "
        "eligibility checks. Third, supplements and figure source data should be inspected manually for arm-level values. Fourth, corresponding authors should be "
        "asked for a minimal dataset: arm, n, baseline mean and SD, follow-up mean and SD, change mean and SD, tissue, clock version and preprocessing details. "
        "Only after this rescue step should the meta-analysis gate be rerun."
    )
    doc.add_heading("Limitations", 1)
    doc.add_paragraph(
        "The full-text eligibility audit is first-reviewer only and must be verified independently. Some subscription-only or preprint full texts remain unavailable in "
        "the workspace. PDF figure-only data were not digitized because that would add measurement error and require manual validation. The extraction algorithm is "
        "conservative and may miss data that a human can recover from complex supplements, but this is preferable to silently manufacturing effect sizes."
    )
    doc.add_heading("Conclusion", 1)
    doc.add_paragraph(
        "A quantitative meta-analysis of human interventions on DNAm clocks is not currently supportable from the verified extracted dataset. The review should "
        "continue as a systematic evidence map with second-reviewer full-text decisions, targeted author data requests and manual extraction from supplementary "
        "materials before any final submission package is built."
    )
    doc.add_heading("References", 1)
    refs = [
        "Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement. BMJ. 2021;372:n71.",
        "Cochrane Methods. Risk of Bias 2 (RoB 2) tool. https://methods.cochrane.org/risk-bias-2.",
        "Bell CG, Lowe R, Adams PD, et al. DNA methylation aging clocks: challenges and recommendations. Genome Biology. 2019;20:249.",
    ]
    for i, ref in enumerate(refs, 1):
        doc.add_paragraph(f"{i}. {ref}")
    out = sub / f"DNAm_clocks_systematic_review_hard_stop_manuscript_{freeze}.docx"
    doc.save(out)

    readme = (
        "# DNAm Clocks Submission Readiness\n\n"
        "Decision: not ready for final journal submission as a meta-analysis.\n\n"
        f"- Raw records: {len(raw)}\n"
        f"- Included-pending-verification studies: {len(included)}\n"
        f"- Clock extraction rows: {len(extracted)}\n"
        f"- Calculable candidate effect sizes: {len(calc)}\n"
        "- Pooled meta-analysis: not run; no clock met the prespecified minimum.\n"
        "- NMA/publication bias/meta-regression/GRADE: not run; hard-stop criteria triggered.\n"
    )
    (sub / f"README_submission_readiness_{freeze}.md").write_text(readme, encoding="utf-8")
    log("manuscript_built", path=str(out))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True)
    run(load_config(ap.parse_args().config))
