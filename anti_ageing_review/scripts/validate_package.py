"""Validate the anti-ageing evidence-map reproducibility package."""
from pathlib import Path
import csv
import sys


HERE = Path(__file__).resolve().parents[1]


def require(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Missing required package path: {path.relative_to(HERE)}")


def main() -> int:
    required = [
        HERE / "make_figures.py",
        HERE / "tables" / "intervention_credibility_ranking.csv",
        HERE / "figures" / "prisma_flow.png",
        HERE / "figures" / "evidence_score_ranking.png",
        HERE / "figures" / "hype_vs_evidence_map.png",
        HERE / "figures" / "translational_matrix.png",
        HERE / "_manuscript_R1.md",
        HERE / "_supplementary_R1.md",
        HERE / "METHODS.md",
        HERE / "DATA_DICTIONARY.md",
        HERE / "DATA_AVAILABILITY.md",
        HERE / "config" / "review_config.yaml",
        HERE / "src" / "run_pipeline.py",
        HERE / "tests",
        HERE / "proof_review" / "mjdrdypu_451_26_R3_annotated_corrections.pdf",
        HERE / "proof_review" / "MJDRDYPU_451_26_author_proof_corrections_2026-08-09.docx",
    ]
    for path in required:
        require(path)

    ranking = HERE / "tables" / "intervention_credibility_ranking.csv"
    with ranking.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 14:
        raise SystemExit(f"Expected 14 intervention classes, found {len(rows)}")
    for field in ("intervention_name", "credibility_score", "credibility_tier"):
        if not rows or field not in rows[0]:
            raise SystemExit(f"Missing ranking field: {field}")

    manuscript = (HERE / "_manuscript_R1.md").read_text(encoding="utf-8")
    if "deai-ecological-validation-india/tree/main/anti_ageing_review" not in manuscript:
        raise SystemExit("Manuscript data-availability link is not article-specific")
    if '("controversial")' in manuscript:
        raise SystemExit("Obsolete 'controversial' label remains in manuscript text")

    excluded = [
        HERE / "data_processed" / "open_text_cache",
        HERE / "meta_frailty_lmic" / "data" / "raw" / "pmc_fulltext",
        HERE / "meta_dnam_clocks" / "data" / "raw" / "fulltext",
    ]
    for path in excluded:
        if path.exists():
            raise SystemExit(f"Redistribution-excluded cache is present: {path.relative_to(HERE)}")

    print("Anti-ageing package validation passed:")
    print(f"- {len(rows)} intervention classes found")
    print("- required figures and source files present")
    print("- article-specific data-availability link present")
    print("- obsolete category wording absent from manuscript source")
    print("- excluded full-text caches absent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
