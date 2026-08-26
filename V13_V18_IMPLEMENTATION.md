# v13–v18 Implementation

- v13: normalized ingestion/data layer and browser JSON export.
- v14: SQLite database with evidence, signals, runs, alerts tables.
- v15: reproducible signal recomputation script with corroboration gates.
- v16: UI reads API when backend is running and falls back to static JSON.
- v17: weekly recompute workflow blueprint; discovery/verification intentionally remains reviewed before ingestion.
- v18: local Flask operating app + deployable static `docs/` build.

## Run locally
Double-click `run_local.command` on macOS, then open http://127.0.0.1:8787 .

## Deployment boundary
The static `docs/` directory can be hosted on a static host. Server-side API/SQLite requires a Python-capable host. GitHub Pages is static-only, so it can host the `docs/` UI but not Flask/SQLite server code.
