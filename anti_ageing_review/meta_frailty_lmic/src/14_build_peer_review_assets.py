from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ASSET_DIR = ROOT / "submission_assets" / "IJMR_FRAILTY_INTERVENTIONS_AUDIT_READY_2026-05-18"


PEER_REVIEW = """# Internal Double-Blind-Style Peer Review

Generated: 2026-05-18

This is an internal simulated double-blind-style review for quality control. It is not an external journal peer review.

## Reviewer 1: Methods and Statistical Review

Recommendation: Major revision before submission.

Major comments:

1. The review question is important and India-facing, but the manuscript cannot yet claim final systematic review or meta-analysis findings. Final inclusion, exclusions, effect sizes and RoB 2 judgements are absent.
2. PubMed-only searching is insufficient for a final systematic review unless justified as a rapid or scoped review. Add Embase/Scopus/Web of Science/Cochrane CENTRAL, trial registries and citation chasing, or explicitly narrow the manuscript type.
3. Protocol registration is mandatory for the intended target and must occur before the review is described as submission-ready.
4. NMA should remain conditional. The current node counts are based on title/abstract and text-mined snippets; comparator connectivity and transitivity cannot be inferred from these data.
5. Numeric outcome extraction needs explicit conversion rules for frailty status, continuous frailty scores, gait speed, SPPB and grip strength. Change scores and endpoint scores should not be pooled without prespecified hierarchy.
6. RoB 2 and certainty assessment are required before inferential statements. Consider CINeMA or GRADE adapted to NMA if NMA proceeds.
7. AI-assisted triage should be described transparently as an aid, with author verification as the decisive step.

Minor comments:

1. Rename Figure 1 as a progress-flow figure until final PRISMA numbers are available.
2. Keep implementation-readiness scoring separate from efficacy ranking to avoid conflating feasibility with effectiveness.
3. Add an exclusion taxonomy before full-text screening begins.

## Reviewer 2: Clinical, Public Health and Indian Primary-Care Review

Recommendation: Major revision before submission.

Major comments:

1. The India-facing contribution is promising, but the paper must avoid implying that all effective interventions are deliverable in Indian primary care. Workforce, equipment, adherence support and procurement burden require extracted evidence.
2. The population definition is broad. Prefrailty, frailty, sarcopenia, functional vulnerability and disease-specific rehabilitation should be separated before synthesis.
3. Indian relevance should include ASHA/ANM/Health and Wellness Centre feasibility, family-caregiver support, low-cost nutrition options, fall-risk safety, and referral thresholds.
4. The current high-confidence queue includes disease-specific and setting-unclear records by design. These should be handled transparently with sensitivity analyses or excluded from the primary synthesis.
5. Adverse events and adherence should be treated as core outcomes, not secondary afterthoughts, because feasibility in older adults depends on safety and sustained participation.
6. The manuscript needs a clear "what can be implemented tomorrow" table only after final extraction.

Minor comments:

1. Use "older adults" consistently rather than alternating with "elderly".
2. Define community-deliverable interventions early.
3. Avoid overclaiming NMA novelty; the novelty should be the component and Indian implementation-readiness framing.

## Editorial Triage View

Current decision: Do not submit yet.

Rationale: The asset package is structurally organized and promising, but IJMR technical and scientific screening would likely return it at present because protocol registration, final PRISMA, full-text decisions, RoB 2, effect estimates and final references are incomplete.
"""


RESPONSE = """# Author Response and Revision Plan

Generated: 2026-05-18

## Overall Response

We agree that the current package is not ready for journal submission. We have retained the assets as an audit-ready working package and have labelled NMA as conditional. No final efficacy, safety or implementation conclusions will be reported until full-text verification and synthesis are complete.

## Actions Before Submission

1. Register the protocol in PROSPERO or another acceptable registry and insert the registration number into the first page, abstract and methods.
2. Expand the search beyond PubMed, or explicitly reframe the manuscript type if a narrower rapid review is chosen.
3. Complete dual-author full-text screening for all 179 high-confidence candidates.
4. Retrieve the 84 publisher/library full texts.
5. Complete numeric extraction, final component coding, RoB 2 and implementation-readiness scoring.
6. Generate final PRISMA 2020 flow diagram and checklist.
7. Run pairwise meta-analysis only where outcomes are compatible.
8. Run NMA only if comparator connectivity and transitivity are confirmed.
9. Complete reference metadata verification for the final included studies.
10. Replace scaffold text with final Results, Discussion, limitations and conclusion.

## Manuscript Strengthening Decisions Already Applied

- The title and asset labels use "conditional component network meta-analysis" to avoid overclaiming.
- Figure 1 is labelled a progress-flow figure, not the final PRISMA flow diagram.
- The declaration file explicitly states that AI assistance does not replace author verification.
- The supplementary file includes feasibility gates and avoids pooled-effect claims.
- The audit report marks protocol registration, full-text decisions, numeric extraction, RoB 2 and final PRISMA as blocking items.
"""


def main() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    peer_path = DOCS / "internal_double_blind_peer_review_2026-05-18.md"
    response_path = DOCS / "author_response_revision_plan_2026-05-18.md"
    peer_path.write_text(PEER_REVIEW, encoding="utf-8")
    response_path.write_text(RESPONSE, encoding="utf-8")
    (ASSET_DIR / peer_path.name).write_text(PEER_REVIEW, encoding="utf-8")
    (ASSET_DIR / response_path.name).write_text(RESPONSE, encoding="utf-8")
    print(peer_path)
    print(response_path)


if __name__ == "__main__":
    main()
