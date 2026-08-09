# Proof corrections and confirmations

This note records the proof-stage checks for `mjdrdypu_451_26_R3.pdf`.

## Author queries

1. **AQ1 — article type and format:** The safest and methodologically accurate classification is **Systematic Review/Evidence Map**. The manuscript is secondary research: it searches and synthesises published records, performs deduplication/screening/classification, and reports a credibility ranking; it does not enrol participants or analyse a primary patient-level dataset. The journal does publish items labelled “Original Article,” but reclassifying this accepted proof as an Original Article should be requested only if the editor confirms that evidence maps are handled under that category. If the editor confirms it, update the article-type metadata, title page, proof label, abstract framing, and checklist consistently. Otherwise, retain **Systematic Review/Evidence Map** and remove the AQ marker after confirmation.
2. **AQ2 — supplementary material:** **Yes, supplementary material is required.** It supports the main text and contains Supplementary Figures S1–S4 and Supplementary Tables S1–S9. Please retain it as a separate journal-compatible supplementary file and ensure the S1/S2 cross-references remain active. Use a clean publication-ready file; do not expose unresolved internal workflow fields unless the journal specifically requests them.

## Corrections requested before final approval

- Replace the proof’s data-availability link with the article-specific repository folder, now committed and pushed in commit `28153a7`:
  `https://github.com/hssling/deai-ecological-validation-india/tree/main/anti_ageing_review`
  The current root URL resolves to an unrelated DEAI manuscript. The article
  package now includes the full project source, data snapshots, methods, and tests.
- Complete production placeholders: `Volume XX`, `Issue XX`, `Month 2026`, `Web Publication: ***`, and `2026;XX:XX-XX` in the citation box.
- Verify the internal proof identifier: the file is named `R3`, while the page header reads `mjdrdypu_451_26_R2_SREM`.
- Remove or clarify the obsolete parenthetical **“controversial”** in the Results text and Figure 3 legend. The revised manuscript states that the category was renamed **Plasma/telomerase**; the old label should not persist without a clear definition.
- Move the Figure 3 dashed-line label `hype-flag threshold 0.10` so it does not collide visually with the `Microbiome` data label.
- Check title capitalization against the accepted title page: the proof headline uses `Can Ageing be Slowed...`, whereas the accepted title uses `Can Ageing Be Slowed...`. If the journal uses sentence case, apply it consistently across headline, citation, metadata, and repository source.
- In the supplementary file, either use the final category names consistently or retain the old analysis field names only with a prominent crosswalk. The current file retains `Supplements` and `Controversial` in some analysis tables while the main text uses `Dietary supplements` and `Plasma/telomerase`.

## Confirmed checks

- Page makeup is readable: no clipped body text, table overflow, missing figure, or broken column transition was found in the nine-page proof.
- Tables 1–3 and Figures 1–4 are present and legible; the main ranking values agree with the displayed Figure 2.
- Citation order in the proof is sequential for the 14 main-text references, with the additional records cited collectively as [15–40].
- The proof’s Reference 9 page range `Aging (Albany NY) 2025;17:908-936` is supported by PMID 40188830. The local submitted Markdown source carried an older/inconsistent `840-863` range and should be updated in the repository copy.
