# Decisions deferred until the backend/player work starts

Not needed for tile generation (batches 010 and 013 finish without them).

1. **Publish (stage 12) target.** What the backend store is (object storage + which database, schema, API). `01_FINAL_PACK_TEMPLATE/12_publish/RUN.md` is blocked on this. Rough size once known: 1-2 days.
2. **Player grader-core.** Where the player lives (repo/folder); the grader goes next to it. One TypeScript module shared by player, backend and pipeline checks. Rough size: 1-2 weeks, mostly the four code runtimes (DuckDB-WASM, Pyodide, Pyodide+matplotlib, HyperFormula). Must match the pipeline sandbox: Pyodide 0.29.5, matplotlib 3.8.4, seaborn 0.13.2, and the `boxplot(tick_labels=)` -> `labels=` alias in `00_FINAL_PIPELINE_CORE/sandbox/run_py.mjs`.
3. **HyperFormula licence.** GPL-3.0 here; shipping it in the player may need a commercial licence or a different formula engine.

Also later: a true drag-edit interaction type. `UI_edit` is currently mapped to `classify`/`find_issues` (keep/remove chart elements).

## Flutter live coding: the backend must run the tests (added 2026-11-26)
Flutter `code_exercise` items (`public.runtime.kind = "flutter"`, `grading_mode = "server"`) cannot be graded in the browser. The backend needs a Dart runner:
- **Toolchain:** Flutter 3.47.9 (Dart 3.13.7), a template app named `exercise` with the packages listed in `00_FINAL_PIPELINE_CORE/registry/runtimes.json` (go_router 17.x; system libsqlite3).
- **Grading:** copy the template; write `public.workspace.files` (learner's editable files replace the starters); for each `grading.tests[]` (`kind: dart_test`) write `spec.code` as `test/<test_id>_grader_test.dart` (no `code` = run the learner's own `test/..._test.dart`), apply `spec.replace`, run `flutter test`; the test is satisfied when the outcome equals `spec.expect` ("pass" by default; "fail" means it ran and failed, not a compile error). All tests satisfied = correct.
- **Isolation (required, this executes learner code):** no network, no secrets or host files, unprivileged user, memory/process/time limits. Reference implementation: `00_FINAL_PIPELINE_CORE/scripts/checkers/dart.py` + `dartbox_runner.py`.
- **Cost/latency:** one cold compile per submission, about 6-15 s on a 16-core machine.
