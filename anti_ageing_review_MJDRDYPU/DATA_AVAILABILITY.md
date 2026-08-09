# Data availability and redistribution boundaries

This repository releases the project code, configuration, methodological record,
bibliographic metadata snapshots, derived tables, audit logs, manuscript sources,
figures, and journal submission assets needed to inspect and extend the project.

The raw PubMed XML included under `meta_frailty_lmic/data/raw/` is bibliographic
metadata and abstracts. Cached full-text files are intentionally not redistributed:

- `data_processed/open_text_cache/`
- `meta_frailty_lmic/data/raw/pmc_fulltext/`
- `meta_dnam_clocks/data/raw/fulltext/`

Those folders were present locally but are excluded from the public package because
the underlying article texts may carry publisher or source-specific redistribution
conditions. Retrieval and mining scripts, fetch logs, identifiers, and derived
tables are included so an investigator can obtain permitted open-access material
directly from the source and regenerate relevant analyses. Do not add licensed full
text to the repository without checking the source licence.

Search results and API metadata can change. Each new run should be dated and should
record source, query, retrieval date, endpoint, and any access/eligibility decision.
Derived data remain subject to the licences and terms of their original providers.
The manuscript and proof files are retained for scholarly reproducibility and are
not a substitute for the journal’s final published version.
