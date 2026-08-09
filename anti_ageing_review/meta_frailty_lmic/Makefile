.PHONY: search
.PHONY: screen
.PHONY: prioritize
.PHONY: scoping
.PHONY: triage
.PHONY: highconf
.PHONY: fulltexts
.PHONY: mine
.PHONY: workbook
.PHONY: feasibility
.PHONY: forms
.PHONY: submission-assets
.PHONY: audit
.PHONY: peer-review
.PHONY: substantive-manuscript
.PHONY: expanded-search
.PHONY: expanded-screen
.PHONY: expanded-fulltexts
.PHONY: pmc-eligibility
.PHONY: numeric-table-mining
.PHONY: real-review-report
.PHONY: all

search:
	python src/01_search_pubmed.py

screen:
	python src/02_dedup_screen_title_abs.py

prioritize:
	python src/03_prioritize_fulltext.py

scoping:
	python src/04_build_scoping_assets.py

triage:
	python src/05_round2_triage.py

highconf:
	python src/06_high_confidence_extraction_set.py

fulltexts:
	python src/07_fetch_pmc_fulltexts.py

mine:
	python src/08_mine_pmc_fulltexts.py

workbook:
	python src/09_build_extraction_workbook_from_pmc.py

feasibility:
	python src/10_network_feasibility_prelim.py

forms:
	python src/11_build_author_extraction_forms.py

submission-assets:
	python src/12_build_submission_assets.py

audit:
	python src/13_audit_submission_readiness.py

peer-review:
	python src/14_build_peer_review_assets.py

substantive-manuscript:
	python src/15_build_substantive_manuscript.py

expanded-search:
	python src/16_expanded_accessible_search.py

expanded-screen:
	python src/17_screen_expanded_accessible_records.py

expanded-fulltexts:
	python src/18_fetch_expanded_pmc_fulltexts.py

pmc-eligibility:
	python src/19_first_reviewer_pmc_fulltext_eligibility.py

numeric-table-mining:
	python src/20_mine_numeric_tables_primary_accessible.py

real-review-report:
	python src/21_build_real_review_progress_report.py

all: search screen prioritize scoping triage highconf fulltexts mine workbook feasibility forms submission-assets audit peer-review substantive-manuscript expanded-search expanded-screen expanded-fulltexts pmc-eligibility numeric-table-mining real-review-report
