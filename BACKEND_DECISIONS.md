# Decisions deferred until the backend/player work starts

Not needed for tile generation (batches 010 and 013 finish without them).

1. **Publish (stage 12) target.** What the backend store is (object storage + which database, schema, API). `01_FINAL_PACK_TEMPLATE/12_publish/RUN.md` is blocked on this. Rough size once known: 1-2 days.
2. **Player grader-core.** Where the player lives (repo/folder); the grader goes next to it. One TypeScript module shared by player, backend and pipeline checks. Rough size: 1-2 weeks, mostly the four code runtimes (DuckDB-WASM, Pyodide, Pyodide+matplotlib, HyperFormula). Must match the pipeline sandbox: Pyodide 0.29.5, matplotlib 3.8.4, seaborn 0.13.2, and the `boxplot(tick_labels=)` -> `labels=` alias in `00_FINAL_PIPELINE_CORE/sandbox/run_py.mjs`.
3. **HyperFormula licence.** GPL-3.0 here; shipping it in the player may need a commercial licence or a different formula engine.

Also later: a true drag-edit interaction type. `UI_edit` is currently mapped to `classify`/`find_issues` (keep/remove chart elements).
