from __future__ import annotations

import argparse
import math
from pathlib import Path

import pandas as pd
from scipy import stats

from src.utils.io import append_log, load_config, save_csv


def hedges_g_from_post(n_t: int, mean_t: float, sd_t: float, n_c: int, mean_c: float, sd_c: float) -> tuple[float, float]:
    pooled = math.sqrt((((n_t - 1) * (sd_t ** 2)) + ((n_c - 1) * (sd_c ** 2))) / (n_t + n_c - 2))
    d = (mean_t - mean_c) / pooled
    correction = 1 - (3 / ((4 * (n_t + n_c)) - 9))
    g = correction * d
    se_g = math.sqrt(((n_t + n_c) / (n_t * n_c)) + ((g ** 2) / (2 * (n_t + n_c - 2))))
    return g, se_g


def row_template() -> dict[str, object]:
    return {
        "study_id": "",
        "title": "",
        "year": "",
        "journal": "",
        "pmid": "",
        "pmcid": "",
        "doi": "",
        "intervention_name": "",
        "endpoint_family": "",
        "outcome_name": "",
        "outcome_timepoint": "",
        "effect_metric": "",
        "effect_direction_beneficial": "",
        "n_treatment": "",
        "n_control": "",
        "mean_treatment": "",
        "sd_treatment": "",
        "mean_control": "",
        "sd_control": "",
        "change_mean_treatment": "",
        "change_sd_treatment": "",
        "change_mean_control": "",
        "change_sd_control": "",
        "events_treatment": "",
        "events_control": "",
        "time_to_event_metric": "",
        "log_effect": "",
        "se_log_effect": "",
        "ci_lower": "",
        "ci_upper": "",
        "p_value": "",
        "extractor_method": "",
        "source_used": "",
        "source_locator": "",
        "verification_status": "",
        "duplicate_cohort_flag": "",
        "risk_of_bias_overall": "",
        "ready_for_pooling": "",
        "notes": "",
        "effect_estimate": "",
        "effect_se": "",
    }


def has_observed_value(series: pd.Series) -> pd.Series:
    text_series = series.astype("string").str.strip()
    return text_series.notna() & text_series.ne("")


def se_from_two_sided_p_unpaired_t(estimate: float, p_value: float, n_treatment: int, n_control: int) -> float:
    df = n_treatment + n_control - 2
    t_value = stats.t.isf(p_value / 2, df)
    return abs(estimate) / t_value


def t_critical_95_unpaired(n_treatment: int, n_control: int) -> float:
    df = n_treatment + n_control - 2
    return stats.t.isf(0.05 / 2, df)


def run(cfg: dict) -> None:
    tables = cfg["paths"]["meta_addon_tables"]
    docs = cfg["paths"]["meta_addon_docs"]
    template_path = tables / "meta_dataset_template.csv"
    working_path = tables / "meta_dataset_working.csv"

    existing = pd.read_csv(working_path) if working_path.exists() else pd.read_csv(template_path)
    rows: list[dict[str, object]] = []

    # Exergame trial: exact arm-level end-of-intervention values from JMIR PDF Table 2.
    title = (
        "Assessing the Clinical Effectiveness of an Exergame-Based Exercise Training Program Using Ring Fit Adventure "
        "to Prevent and Postpone Frailty and Sarcopenia Among Older Adults in Rural Long-Term Care Facilities: "
        "Randomized Controlled Trial."
    )
    base = row_template()
    base.update(
        {
            "study_id": "39024000",
            "title": title,
            "year": 2024,
            "journal": "J Med Internet Res",
            "pmid": "39024000",
            "pmcid": "",
            "doi": "10.2196/59468",
            "intervention_name": "exercise",
            "endpoint_family": "frailty_function",
            "outcome_timepoint": "12_weeks_post_intervention",
            "effect_direction_beneficial": "higher_or_lower_depends_on_scale",
            "n_treatment": 30,
            "n_control": 30,
            "extractor_method": "manual_pdf_table_extraction",
            "source_used": "publisher_pdf",
            "source_locator": "https://www.jmir.org/2024/1/e59468/PDF",
            "verification_status": "exact_table_values_extracted",
            "duplicate_cohort_flag": "no",
            "risk_of_bias_overall": "some_concern",
            "ready_for_pooling": "yes",
        }
    )

    outcomes = [
        ("SOF frailty index", 0.80, 0.85, 0.80, 0.81, ".007", "Lower score favorable"),
        ("Appendicular skeletal muscle mass", 19.13, 4.58, 16.96, 2.40, ".002", "Higher score favorable"),
        ("Appendicular skeletal muscle mass index", 8.15, 1.77, 7.15, 0.84, ".003", "Higher score favorable"),
        ("Dominant handgrip strength", 20.80, 7.59, 16.20, 6.04, ".01", "Higher score favorable"),
        ("Walking speed", 0.53, 0.33, 0.53, 0.27, "<.001", "Higher score favorable"),
    ]
    for outcome_name, mt, sdt, mc, sdc, p_value, direction_note in outcomes:
        row = base.copy()
        row["outcome_name"] = outcome_name
        row["mean_treatment"] = mt
        row["sd_treatment"] = sdt
        row["mean_control"] = mc
        row["sd_control"] = sdc
        row["p_value"] = p_value
        row["notes"] = (
            "End-of-intervention means and SDs extracted from Table 2. Group sizes were 30 versus 30 randomized; "
            "ITT analysis with last-observation-carried-forward reported in the source. "
            + direction_note
        )
        g, se_g = hedges_g_from_post(30, mt, sdt, 30, mc, sdc)
        row["effect_metric"] = "hedges_g_post_intervention"
        row["effect_estimate"] = g
        row["effect_se"] = se_g
        rows.append(row)

    # Multidomain lifestyle trial: sensitivity-only frailty estimate from reported means and assumed SD in power paragraph.
    row = row_template()
    row.update(
        {
            "study_id": "41677077_sharefi_sensitivity",
            "title": "A Multidomain Lifestyle Intervention Is Associated With Improved Functional Trajectories and Favorable Changes in Epigenetic Aging Markers in Frail Older Adults: A Randomized Controlled Trial.",
            "year": 2026,
            "journal": "Aging Cell",
            "pmid": "41677077",
            "pmcid": "PMC12895478",
            "doi": "10.1111/acel.70376",
            "intervention_name": "lifestyle_bundle",
            "endpoint_family": "frailty_function",
            "outcome_name": "SHARE-FI score",
            "outcome_timepoint": "6_months_post_intervention",
            "effect_metric": "hedges_g_sensitivity_reported_means_assumed_sd",
            "effect_direction_beneficial": "lower_score_favorable",
            "n_treatment": 28,
            "n_control": 15,
            "mean_treatment": 0.8,
            "sd_treatment": 1.0,
            "mean_control": 4.0,
            "sd_control": 1.0,
            "p_value": "<0.0001",
            "extractor_method": "manual_pmc_text_extraction",
            "source_used": "pmc_xml",
            "source_locator": "data_processed/open_text_cache/PMC12895478.xml",
            "verification_status": "sensitivity_only_from_power_paragraph",
            "duplicate_cohort_flag": "no",
            "risk_of_bias_overall": "some_concern",
            "ready_for_pooling": "no",
            "notes": (
                "This row is retained for sensitivity tracking only. The source reports final sample sizes of 15 versus 28 and "
                "states that the SHARE-FI effect size was calculated from group means 4.0 and 0.8 assuming SD 1.0 in each group. "
                "Because the SDs appear to be assumed rather than observed, this row should not enter the primary pooled analysis."
            ),
        }
    )
    g, se_g = hedges_g_from_post(28, 0.8, 1.0, 15, 4.0, 1.0)
    row["effect_estimate"] = g
    row["effect_se"] = se_g
    rows.append(row)

    # Multiple sclerosis pilot trial: model-level between-group change estimates with confidence intervals.
    ms_base = row_template()
    ms_base.update(
        {
            "study_id": "ms_frailty_pilot_2026",
            "title": "Reducing frailty in frail people with multiple sclerosis: Feasibility of a 6-week multimodal exercise training program.",
            "year": 2026,
            "journal": "PLoS One",
            "pmid": "41984883",
            "pmcid": "",
            "doi": "10.1371/journal.pone.0347063",
            "intervention_name": "exercise",
            "endpoint_family": "frailty_function",
            "outcome_timepoint": "6_weeks_change_from_baseline",
            "n_treatment": 10,
            "n_control": 6,
            "extractor_method": "manual_text_extraction_from_verified_snippet",
            "source_used": "verified_open_text_snippet",
            "source_locator": "results/tables/effect_size_extraction_priority_human.csv",
            "verification_status": "between_group_change_with_ci_extracted",
            "duplicate_cohort_flag": "no",
            "risk_of_bias_overall": "some_concern",
            "ready_for_pooling": "yes",
        }
    )
    ms_rows = [
        ("Edmonton Frail Scale index performance score", "mean_difference_change", -0.07, 0.03571428571428572, -0.14, 0.00, "", "Lower score favorable"),
        ("MSQoL-54 mental health", "mean_difference_change", 21.24, 7.10204081632653, 7.32, 35.16, "", "Higher score favorable"),
    ]
    for outcome_name, metric, est, se_val, ci_lo, ci_hi, p_value, direction in ms_rows:
        row = ms_base.copy()
        row["outcome_name"] = outcome_name
        row["effect_metric"] = metric
        row["effect_direction_beneficial"] = direction
        row["effect_estimate"] = est
        row["effect_se"] = se_val
        row["ci_lower"] = ci_lo
        row["ci_upper"] = ci_hi
        row["p_value"] = p_value
        row["notes"] = (
            "Between-group difference in baseline-to-6-week change extracted from verified text snippet. "
            "Sixteen participants were randomized; ten intervention and six control participants completed the study."
        )
        rows.append(row)

    # PROMOTe trial: abstract-level regression estimates with confidence intervals.
    promote_base = row_template()
    promote_base.update(
        {
            "study_id": "38424099",
            "title": "Effect of gut microbiome modulation on muscle function and cognition: the PROMOTe randomised controlled trial.",
            "year": 2024,
            "journal": "Nature Communications",
            "pmid": "38424099",
            "pmcid": "PMC10904794",
            "doi": "10.1038/s41467-024-46116-y",
            "intervention_name": "microbiome",
            "extractor_method": "manual_pubmed_xml_abstract_extraction",
            "source_used": "pubmed_xml",
            "source_locator": "data_processed/open_text_cache/pubmed_38424099.xml",
            "verification_status": "abstract_level_model_estimate_extracted",
            "duplicate_cohort_flag": "no",
            "risk_of_bias_overall": "some_concern",
            "ready_for_pooling": "yes",
            "n_treatment": 36,
            "n_control": 36,
            "outcome_timepoint": "12_weeks_model_estimate",
        }
    )
    promote_rows = [
        ("frailty_function", "Chair rise time", "beta_difference", 0.579, 0.8466836734693878, -1.080, 2.239, "0.494", "Lower time favorable"),
        ("cognition", "Cognitive factor score", "beta_difference", -0.482, 0.1714285714285714, -0.813, -0.141, "0.014", "Direction depends on model coding; extracted as reported"),
    ]
    for endpoint_family, outcome_name, metric, est, se_val, ci_lo, ci_hi, p_value, direction in promote_rows:
        row = promote_base.copy()
        row["endpoint_family"] = endpoint_family
        row["outcome_name"] = outcome_name
        row["effect_metric"] = metric
        row["effect_direction_beneficial"] = direction
        row["effect_estimate"] = est
        row["effect_se"] = se_val
        row["ci_lower"] = ci_lo
        row["ci_upper"] = ci_hi
        row["p_value"] = p_value
        row["notes"] = (
            "Regression estimate and 95% CI extracted from the PubMed XML abstract. "
            "The abstract reports 36 twin pairs (72 individuals) randomized in a placebo-controlled trial."
        )
        rows.append(row)

    # CALERIE trial: full-text standardized treatment effects with confidence intervals.
    calerie_base = row_template()
    calerie_base.update(
        {
            "study_id": "37118425",
            "title": "Effect of long-term caloric restriction on DNA methylation measures of biological aging in healthy adults from the CALERIE trial.",
            "year": 2023,
            "journal": "Nature Aging",
            "pmid": "37118425",
            "pmcid": "",
            "doi": "10.1038/s43587-022-00357-y",
            "intervention_name": "caloric_restriction",
            "endpoint_family": "epigenetic_biological_age",
            "effect_metric": "cohens_d_standardized_change_difference",
            "extractor_method": "manual_full_text_primary_source_extraction",
            "source_used": "publisher_html",
            "source_locator": "https://www.nature.com/articles/s43587-022-00357-y",
            "verification_status": "full_text_effect_size_and_ci_extracted",
            "duplicate_cohort_flag": "no",
            "risk_of_bias_overall": "low",
            "ready_for_pooling": "yes",
            "n_treatment": 128,
            "n_control": 69,
        }
    )
    calerie_rows = [
        ("PC PhenoAge", "12_months_itt", -0.03, -0.19, 0.12, "P > 0.50", "Direction depends on clock acceleration coding; extracted as reported"),
        ("PC PhenoAge", "24_months_itt", 0.05, -0.11, 0.20, "P > 0.50", "Direction depends on clock acceleration coding; extracted as reported"),
        ("PC GrimAge", "12_months_itt", -0.04, -0.16, 0.07, "P > 0.40", "Direction depends on clock acceleration coding; extracted as reported"),
        ("PC GrimAge", "24_months_itt", 0.05, -0.07, 0.17, "P > 0.40", "Direction depends on clock acceleration coding; extracted as reported"),
        ("DunedinPACE", "12_months_itt", -0.29, -0.45, -0.13, "P < 0.003", "Lower pace favorable"),
        ("DunedinPACE", "24_months_itt", -0.25, -0.41, -0.09, "P < 0.003", "Lower pace favorable"),
        ("DunedinPACE", "12_months_tot_20pct_cr", -0.43, -0.67, -0.19, "P < 0.005", "Lower pace favorable"),
        ("DunedinPACE", "24_months_tot_20pct_cr", -0.40, -0.67, -0.12, "P < 0.005", "Lower pace favorable"),
    ]
    for outcome_name, timepoint, est, ci_lo, ci_hi, p_value, direction in calerie_rows:
        row = calerie_base.copy()
        row["outcome_name"] = outcome_name
        row["outcome_timepoint"] = timepoint
        row["effect_direction_beneficial"] = direction
        row["effect_estimate"] = est
        row["ci_lower"] = ci_lo
        row["ci_upper"] = ci_hi
        row["effect_se"] = (ci_hi - ci_lo) / (2 * 1.96)
        row["p_value"] = p_value
        row["notes"] = (
            "Standardized effect estimate and 95% CI extracted from the Nature Aging full text. "
            "The article reports n = 197 participants with DNAm data available (128 caloric restriction, 69 ad libitum control)."
        )
        rows.append(row)

    # DO-HEALTH trial: exact omega-3 treatment effects reported in the primary article text.
    do_health_base = row_template()
    do_health_base.update(
        {
            "study_id": "39900648",
            "title": "Individual and additive effects of vitamin D, omega-3 and exercise on DNA methylation clocks of biological aging in older adults from the DO-HEALTH trial.",
            "year": 2025,
            "journal": "Nature Aging",
            "pmid": "39900648",
            "pmcid": "PMC11922767",
            "doi": "10.1038/s43587-024-00793-y",
            "intervention_name": "omega_3",
            "endpoint_family": "epigenetic_biological_age",
            "outcome_timepoint": "36_months_itt_main_effect",
            "effect_metric": "cohens_d_standardized_change_difference",
            "extractor_method": "manual_full_text_primary_source_extraction",
            "source_used": "publisher_html",
            "source_locator": "https://www.nature.com/articles/s43587-024-00793-y",
            "verification_status": "full_text_effect_size_and_ci_extracted",
            "duplicate_cohort_flag": "no",
            "risk_of_bias_overall": "some_concern",
            "ready_for_pooling": "yes",
            "notes": (
                "Main-effect estimate from the 2x2x2 factorial DO-HEALTH Bio-Age trial. "
                "The article reports n = 777 participants with DNAm measures at baseline and year 3."
            ),
        }
    )
    do_health_rows = [
        ("PhenoAge", -0.16, -0.30, -0.02, "omega-3 main effect", "Lower age-acceleration favorable"),
        ("GrimAge2", -0.32, -0.59, -0.06, "omega-3 main effect", "Lower age-acceleration favorable"),
        ("DunedinPACE", -0.17, -0.31, -0.04, "omega-3 main effect", "Lower pace favorable"),
    ]
    for outcome_name, est, ci_lo, ci_hi, p_value, direction in do_health_rows:
        row = do_health_base.copy()
        row["outcome_name"] = outcome_name
        row["effect_estimate"] = est
        row["ci_lower"] = ci_lo
        row["ci_upper"] = ci_hi
        row["effect_se"] = (ci_hi - ci_lo) / (2 * 1.96)
        row["p_value"] = p_value
        row["effect_direction_beneficial"] = direction
        rows.append(row)

    # Greens crossover trial: exact condition-level mean changes and SDs are available,
    # but paired-treatment variance is not reported, so these remain sensitivity-only.
    greens_base = row_template()
    greens_base.update(
        {
            "study_id": "41717034_crossover_sensitivity",
            "title": "Epigenetic and microbiome responses to greens supplementation in obese older adults: results from a randomized crossover-controlled trial.",
            "year": 2026,
            "journal": "Front Nutr",
            "pmid": "41717034",
            "pmcid": "PMC12915338",
            "doi": "10.3389/fnut.2026.1750030",
            "intervention_name": "microbiome",
            "endpoint_family": "epigenetic_biological_age",
            "outcome_timepoint": "30_day_crossover_condition_change",
            "effect_metric": "mean_difference_condition_change_crossover_unpaired_sensitivity",
            "extractor_method": "manual_pmc_text_extraction",
            "source_used": "pmc_xml",
            "source_locator": "data_processed/open_text_cache/PMC12915338.xml",
            "verification_status": "exact_condition_level_means_extracted_paired_variance_missing",
            "duplicate_cohort_flag": "no",
            "risk_of_bias_overall": "some_concern",
            "ready_for_pooling": "no",
        }
    )
    greens_rows = [
        ("Horvath", 1.43, 3.61, -2.07, 4.22, "p = 0.015", "Lower age-acceleration favorable"),
        ("PCGrimAge", -0.25, 1.59, 0.35, 2.02, "not significant", "Lower age-acceleration favorable"),
        ("DamAge", -2.84, 9.06, 5.30, 9.77, "p = 0.028", "Lower damage-age favorable"),
        ("AdaptAge", 3.70, 9.10, -4.50, 11.60, "not significant", "Direction depends on clock coding; extracted as reported"),
    ]
    for outcome_name, mt, sdt, mc, sdc, p_value, direction in greens_rows:
        row = greens_base.copy()
        row["outcome_name"] = outcome_name
        row["mean_treatment"] = mt
        row["sd_treatment"] = sdt
        row["mean_control"] = mc
        row["sd_control"] = sdc
        row["effect_estimate"] = mt - mc
        row["p_value"] = p_value
        row["effect_direction_beneficial"] = direction
        row["notes"] = (
            "Randomized crossover-controlled trial with exact condition-level mean changes and SDs reported in the main text. "
            "Rows are retained for sensitivity tracking only because the article does not report the paired within-person correlation "
            "or a model-based treatment effect standard error needed for defensible generic inverse-variance pooling."
        )
        rows.append(row)

    # Multidomain lifestyle frailty trial: DNAm PhenoAge REA contrast is numerically reported in the main text,
    # but the methylomic control-group sample size is only given as a range in the supplement caption.
    acel_row = row_template()
    acel_estimate = -1.7 - 8.4
    acel_n_treatment = 16
    acel_n_control = 7
    acel_se = se_from_two_sided_p_unpaired_t(acel_estimate, 0.03, acel_n_treatment, acel_n_control)
    acel_tcrit = t_critical_95_unpaired(acel_n_treatment, acel_n_control)
    acel_row.update(
        {
            "study_id": "41677077_phenoage_rea_sensitivity",
            "title": "A Multidomain Lifestyle Intervention Is Associated With Improved Functional Trajectories and Favorable Changes in Epigenetic Aging Markers in Frail Older Adults: A Randomized Controlled Trial.",
            "year": 2026,
            "journal": "Aging Cell",
            "pmid": "41677077",
            "pmcid": "PMC12895478",
            "doi": "10.1111/acel.70376",
            "intervention_name": "lifestyle_bundle",
            "endpoint_family": "epigenetic_biological_age",
            "outcome_name": "DNAm PhenoAge rate of epigenetic aging",
            "outcome_timepoint": "6_months_between_group_rea_difference",
            "effect_metric": "mean_difference_change_se_from_reported_p_sensitivity",
            "effect_direction_beneficial": "Lower pace favorable",
            "extractor_method": "manual_pmc_xml_text_extraction",
            "source_used": "pmc_xml",
            "source_locator": "data_processed/open_text_cache/PMC12895478.xml",
            "verification_status": "between_group_rea_difference_extracted_sample_size_approximated",
            "duplicate_cohort_flag": "no",
            "risk_of_bias_overall": "some_concern",
            "ready_for_pooling": "no",
            "n_treatment": acel_n_treatment,
            "n_control": acel_n_control,
            "effect_estimate": acel_estimate,
            "effect_se": acel_se,
            "ci_lower": acel_estimate - (acel_tcrit * acel_se),
            "ci_upper": acel_estimate + (acel_tcrit * acel_se),
            "p_value": "0.03",
            "notes": (
                "The main text reports DNAm PhenoAge REA means of +8.4 in controls and -1.7 in the intervention group at 6 months, "
                "with p = 0.03 for the between-group comparison. The supplementary caption reports methylomic sample sizes of n_control = 6-7 "
                "and n_intervention = 16 across clocks; this sensitivity row uses n_control = 7 for DNAm PhenoAge. "
                "Standard error and confidence interval were approximated from the reported two-sided unpaired t-test p-value and this assumed "
                "control-group sample size. This row is retained for sensitivity tracking only."
            ),
        }
    )
    rows.append(acel_row)

    # Semaglutide RCT preprint: exact adjusted estimates with 95% CIs are reported in the PMC preprint HTML.
    # These rows remain outside the primary pooling set because the source is a preprint.
    sema_base = row_template()
    sema_base.update(
        {
            "study_id": "40791720_semaglutide_preprint",
            "title": "Semaglutide Slows Epigenetic Aging in People with HIV-associated lipohypertrophy: Evidence from a Randomized Controlled Trial.",
            "year": 2025,
            "journal": "medRxiv",
            "pmid": "40791720",
            "pmcid": "PMC12338914",
            "doi": "10.1101/2025.07.09.25331038",
            "intervention_name": "semaglutide",
            "endpoint_family": "epigenetic_biological_age",
            "extractor_method": "manual_pmc_preprint_html_extraction",
            "source_used": "pmc_html_preprint",
            "source_locator": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12338914/",
            "verification_status": "exact_adjusted_effect_and_ci_extracted_preprint",
            "duplicate_cohort_flag": "no",
            "risk_of_bias_overall": "some_concern",
            "ready_for_pooling": "no",
            "n_treatment": 45,
            "n_control": 39,
            "outcome_timepoint": "32_weeks_adjusted_ancova",
        }
    )
    sema_rows = [
        ("PCGrimAge", -3.08, -5.29, -0.86, "0.007", "Lower age-acceleration favorable"),
        ("DunedinPACE", -0.09, -0.17, -0.02, "0.01", "Lower pace favorable"),
        ("RetroClock", -2.18, -4.14, -0.21, "0.030", "Lower age-acceleration favorable"),
        ("GrimAge V1", -1.39, -2.72, -0.05, "0.042", "Lower age-acceleration favorable"),
        ("GrimAge V2", -2.26, -3.94, -0.59, "0.008", "Lower age-acceleration favorable"),
        ("AdaptAge", 3.49, -2.20, 9.18, "0.23", "Direction depends on clock coding; extracted as reported"),
        ("CausAge", 0.46, -2.40, 3.32, "0.75", "Direction depends on clock coding; extracted as reported"),
        ("DamAge", -2.22, -7.09, 2.65, "0.37", "Lower damage-age favorable"),
    ]
    for outcome_name, est, ci_lo, ci_hi, p_value, direction in sema_rows:
        row = sema_base.copy()
        row["outcome_name"] = outcome_name
        row["effect_metric"] = "mean_difference_change"
        row["effect_estimate"] = est
        row["ci_lower"] = ci_lo
        row["ci_upper"] = ci_hi
        row["effect_se"] = (ci_hi - ci_lo) / (2 * 1.96)
        row["p_value"] = p_value
        row["effect_direction_beneficial"] = direction
        row["notes"] = (
            "Post-hoc epigenetic analysis of a 32-week double-blind placebo-controlled semaglutide trial in adults with "
            "HIV-associated lipohypertrophy. Adjusted ANCOVA estimates and 95% CIs were extracted from the PMC-hosted preprint HTML. "
            "Rows are retained outside the primary pooled set because the source is preprint-only."
        )
        rows.append(row)

    # Fitzgerald pilot RCT: exact between-group Horvath DNAmAge contrast reported in PMC full text,
    # but no confidence interval or standard error is reported.
    fitz_row = row_template()
    fitz_estimate = -3.23
    fitz_se = se_from_two_sided_p_unpaired_t(fitz_estimate, 0.018, 21, 22)
    fitz_tcrit = t_critical_95_unpaired(21, 22)
    fitz_row.update(
        {
            "study_id": "33844651_horvath_sensitivity",
            "title": "Potential reversal of epigenetic age using a diet and lifestyle intervention: a pilot randomized clinical trial.",
            "year": 2021,
            "journal": "Aging (Albany NY)",
            "pmid": "33844651",
            "pmcid": "PMC8064200",
            "doi": "10.18632/aging.202913",
            "intervention_name": "lifestyle_bundle",
            "endpoint_family": "epigenetic_biological_age",
            "outcome_name": "Horvath DNAmAge",
            "outcome_timepoint": "8_weeks_between_group_change",
            "effect_metric": "mean_difference_change_se_from_reported_p_sensitivity",
            "effect_direction_beneficial": "Lower age-acceleration favorable",
            "extractor_method": "manual_pmc_text_extraction",
            "source_used": "pmc_html",
            "source_locator": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8064200/",
            "verification_status": "between_group_change_extracted_no_uncertainty",
            "duplicate_cohort_flag": "no",
            "risk_of_bias_overall": "some_concern",
            "ready_for_pooling": "no",
            "n_treatment": 21,
            "n_control": 22,
            "effect_estimate": fitz_estimate,
            "effect_se": fitz_se,
            "ci_lower": fitz_estimate - (fitz_tcrit * fitz_se),
            "ci_upper": fitz_estimate + (fitz_tcrit * fitz_se),
            "p_value": "0.018",
            "notes": (
                "Randomized pilot trial in healthy adult males. The PMC full text reports a 3.23-year decrease in Horvath DNAmAge "
                "compared with controls and a treatment-group within-person decrease of 1.96 years. "
                "Standard error and confidence interval were approximated from the reported two-sided unpaired t-test p-value "
                "and group sizes (21 treatment, 22 control). This row is retained for sensitivity tracking only."
            ),
        }
    )
    rows.append(fitz_row)

    seeded = pd.DataFrame(rows)
    if existing.empty:
        combined = seeded.copy()
    else:
        combined = pd.concat([existing, seeded], ignore_index=True)
    if "study_id" in combined.columns:
        combined = combined.drop_duplicates(subset=["study_id", "outcome_name", "outcome_timepoint"], keep="last")
    save_csv(combined, working_path)
    primary = combined[combined["ready_for_pooling"].astype(str).str.lower().eq("yes")].copy()
    save_csv(primary, tables / "meta_dataset_primary_pooling.csv")
    ci_lower_present = has_observed_value(combined["ci_lower"])
    ci_upper_present = has_observed_value(combined["ci_upper"])
    mean_t_present = has_observed_value(combined["mean_treatment"])
    sd_t_present = has_observed_value(combined["sd_treatment"])
    mean_c_present = has_observed_value(combined["mean_control"])
    sd_c_present = has_observed_value(combined["sd_control"])
    harmonization = (
        combined.assign(
            ready_for_pooling_flag=combined["ready_for_pooling"].astype(str).str.lower().eq("yes"),
            has_ci=ci_lower_present & ci_upper_present,
            has_arm_level_means=mean_t_present & sd_t_present & mean_c_present & sd_c_present,
        )
        .groupby(["endpoint_family", "effect_metric"], dropna=False)
        .agg(
            rows=("study_id", "size"),
            unique_studies=("study_id", "nunique"),
            ready_rows=("ready_for_pooling_flag", "sum"),
            ci_rows=("has_ci", "sum"),
            arm_level_rows=("has_arm_level_means", "sum"),
        )
        .reset_index()
        .sort_values(["unique_studies", "rows"], ascending=False)
    )
    save_csv(harmonization, tables / "meta_pooling_harmonization_audit.csv")
    pool_candidates = (
        primary.groupby(["endpoint_family", "effect_metric", "outcome_name"], dropna=False)
        .agg(unique_studies=("study_id", "nunique"), rows=("study_id", "size"))
        .reset_index()
        .query("unique_studies >= 2")
        .sort_values(["unique_studies", "rows"], ascending=False)
    )
    save_csv(pool_candidates, tables / "meta_multi_study_pool_candidates.csv")
    peer_reviewed_mask = ~combined["journal"].astype("string").str.contains("medRxiv|bioRxiv", case=False, na=False)
    eligibility_audit = (
        combined.assign(
            peer_reviewed=peer_reviewed_mask.map({True: "yes", False: "no"}),
            primary_pool_eligible=combined["ready_for_pooling"].astype(str).str.lower().eq("yes").map({True: "yes", False: "no"}),
        )
        .loc[
            :,
            [
                "study_id",
                "title",
                "journal",
                "peer_reviewed",
                "endpoint_family",
                "outcome_name",
                "outcome_timepoint",
                "effect_metric",
                "verification_status",
                "primary_pool_eligible",
                "notes",
            ],
        ]
        .sort_values(["peer_reviewed", "primary_pool_eligible", "study_id", "outcome_name"], ascending=[False, False, True, True])
    )
    save_csv(eligibility_audit, tables / "peer_reviewed_pool_eligibility_audit.csv")

    notes = """# Manual Numeric Extractions

## Exergame RFA trial
- Source: JMIR PDF Table 2
- URL: https://www.jmir.org/2024/1/e59468/PDF
- Randomized participants: 30 intervention, 30 control
- Extracted exact end-of-intervention mean and SD values for:
  - SOF frailty index
  - appendicular skeletal muscle mass
  - appendicular skeletal muscle mass index
  - dominant handgrip strength
  - walking speed
- Hedges g and standard error were computed from post-intervention means and pooled SD.

## Multidomain lifestyle trial
- Source: PMC XML `PMC12895478.xml`
- The SHARE-FI row uses values reported in the power paragraph: final sample sizes 15 and 28, group means 4.0 and 0.8, assumed SD 1.0.
- This is a sensitivity-only row and is not marked ready for pooling.
- Added a second sensitivity-only DNAm PhenoAge REA row from the main text:
  - control-group mean REA: `+8.4`
  - intervention-group mean REA: `-1.7`
  - reported `p = 0.03`
- The methylomic control-group sample size is reported only as a range (`n = 6-7`) in the supplement caption, so this row uses `n_control = 7` and remains sensitivity-only.

## Multiple sclerosis frailty pilot trial
- Source: verified extraction snippet in `results/tables/effect_size_extraction_priority_human.csv`
- Sixteen participants were randomized; ten intervention and six control participants completed the study.
- Added two generic inverse-variance rows using reported between-group change estimates and 95% confidence intervals:
  - Edmonton Frail Scale index performance score
  - MSQoL-54 mental health

## PROMOTe trial
- Source: PubMed XML abstract `pubmed_38424099.xml`
- The abstract reports 36 twin pairs (72 individuals) randomized.
- Added two generic inverse-variance rows using reported beta estimates and 95% confidence intervals:
  - chair rise time
  - cognitive factor score

## CALERIE trial
- Source: Nature Aging full text `https://www.nature.com/articles/s43587-022-00357-y`
- Added standardized treatment effects and 95% confidence intervals for:
  - PC PhenoAge at 12 and 24 months
  - PC GrimAge at 12 and 24 months
  - DunedinPACE at 12 and 24 months
  - DunedinPACE effect-of-treatment-on-the-treated estimates for 20% caloric restriction at 12 and 24 months

## DO-HEALTH trial
- Source: Nature Aging full text `https://www.nature.com/articles/s43587-024-00793-y`
- Added omega-3 main-effect standardized treatment estimates and 95% confidence intervals for:
  - PhenoAge
  - GrimAge2
  - DunedinPACE
- These were extracted from the primary article text and are suitable for generic inverse-variance pooling on a same-outcome basis.

## Greens crossover trial
- Source: PMC XML `PMC12915338.xml`
- Added exact condition-level mean changes and SDs for:
  - Horvath
  - PCGrimAge
  - DamAge
  - AdaptAge
- These are sensitivity-only rows because the crossover paper does not report the paired within-person correlation or a model-based treatment-effect SE.

## Fitzgerald pilot RCT
- Source: PMC HTML `https://pmc.ncbi.nlm.nih.gov/articles/PMC8064200/`
- Added a sensitivity-only Horvath DNAmAge row from the reported between-group change:
  - between-group DNAmAge difference: `-3.23 years`
  - reported `p = 0.018`
- This row is not poolable because the article does not report a confidence interval or standard error.

## FMD source-data recovery
- Downloaded official source workbook to `data_processed/open_text_cache/fmd_source_data.xlsx`
- Source article: `https://www.nature.com/articles/s41467-024-45260-9`
- Source data DOI: `https://doi.org/10.6084/m9.figshare.24915063`
- The workbook contains participant-level biomarker inputs for the biological-age analysis, but not the derived biological-age values or formula.
- Quantitative synthesis for this endpoint remains blocked pending reconstruction of the exact NHANES-trained biological-age algorithm used in the paper.

## Semaglutide RCT preprint
- Source: PMC-hosted medRxiv preprint `https://pmc.ncbi.nlm.nih.gov/articles/PMC12338914/`
- Trial population: adults with HIV-associated lipohypertrophy; semaglutide `n = 45`, placebo `n = 39`
- Added exact adjusted effect estimates with 95% confidence intervals for:
  - PCGrimAge
  - DunedinPACE
  - RetroClock
  - GrimAge V1
  - GrimAge V2
  - AdaptAge
  - CausAge
  - DamAge
- These rows are not marked ready for pooling because the source is preprint-only.

## Harmonization audit
- Generated `results/meta_addon/tables/meta_pooling_harmonization_audit.csv`
- This groups rows by endpoint family and effect metric so the next pass can target genuinely poolable subsets instead of mixing incompatible contrasts.
- Generated `results/meta_addon/tables/meta_multi_study_pool_candidates.csv` to flag outcome-level groups with at least two independent studies.
- Generated `results/meta_addon/tables/peer_reviewed_pool_eligibility_audit.csv` to document which quantified rows are peer-reviewed, primary-pool-eligible, or excluded.
"""
    (docs / "manual_extraction_notes.md").write_text(notes, encoding="utf-8")

    append_log(
        cfg["paths"]["logs"] / "progress.md",
        "Phase 23 - Meta-analysis Add-on Manual Numeric Extraction Seed",
        "- Seeded the quantitative add-on dataset with exact arm-level end-of-intervention values from the exergame RFA trial.\n- Added a sensitivity-only SHARE-FI row from the multidomain lifestyle trial with explicit caveat that SD values were assumed in the source power paragraph.\n- Added model-level quantitative rows from the multiple-sclerosis frailty pilot trial and the PROMOTe trial using reported confidence intervals.\n- Added full-text standardized DNAm-aging treatment effects from the CALERIE and DO-HEALTH trials.\n- Added sensitivity-only epigenetic-age rows from the greens crossover trial and the Fitzgerald pilot RCT where exact contrasts were reported but uncertainty was missing.\n- Downloaded the official FMD source workbook and documented the remaining algorithm-reconstruction blocker.\n- Computed Hedges g and standard errors or generic inverse-variance standard errors for extracted rows, and generated harmonization, multi-study candidate, and peer-reviewed pool-eligibility audits.",
        "- results/meta_addon/tables/meta_dataset_working.csv\n- results/meta_addon/tables/meta_dataset_primary_pooling.csv\n- results/meta_addon/tables/meta_pooling_harmonization_audit.csv\n- results/meta_addon/tables/meta_multi_study_pool_candidates.csv\n- results/meta_addon/tables/peer_reviewed_pool_eligibility_audit.csv\n- docs/meta_addon/manual_extraction_notes.md",
        "- Continue extracting exact arm-level or model-level values from additional local XML and open PDFs.\n- Keep only exact observed values in the primary pooling set; retain assumed-value rows for sensitivity analyses only.",
        "- Current working dataset still has too few independent studies for a stable pooled estimate in most endpoint families.\n- Outcome harmonization remains the main constraint, although DunedinPACE now has at least two independent studies for exploratory pooling.\n- The FMD biological-age endpoint is blocked on reconstruction of the exact NHANES-trained algorithm used by the authors.",
        "python -m src.meta_addon.seed_numeric_extractions --config config/meta_addon_config.yaml",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/meta_addon_config.yaml")
    run(load_config(parser.parse_args().config))
