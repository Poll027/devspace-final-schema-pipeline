# Onboarding a new role (path) — the reuse procedure

The pack is role-agnostic. A new role changes **data**, not code, unless its glossary needs a block/interaction type that doesn't exist yet. Do these in order; stop at the first failure.

1. **Inputs ready?** The path's TOC workspace has `freeze_manifest.json`, and its glossary batch has `path_glossary_bundle.<path>.json` with every bundle `ready_for_final_schema`.
2. **Gap report** (free, 5 seconds):
   ```bash
   python3 00_FINAL_PIPELINE_CORE/scripts/visual_inventory.py <path_glossary_bundle.json> --out gap_report.json
   ```
   It lists the visual/practice anchor types the glossary uses against the registries, the runtimes implied by concept ids, and **GAPS**. A gap means a developer must build a block/interaction type (schema + registry entry + checker + player component) *before* those concepts can be authored. Everything else is ready.
3. **Path profile:** copy `registry/path_profiles/_default.json` to `<path_id>.json` and fill `runtime_by_concept_prefix` (concept-id prefix → the runtime the player needs, e.g. `react` → `react_sandbox`). Without it no runtimes are inferred.
4. **New type, only if step 2 reported a gap:** write the schema file → add a registry entry → `python3 00_FINAL_PIPELINE_CORE/scripts/build_unions.py` → add a checker in a pack module (`checkers/<pack>.py`, import it in `checkers/__init__.py`) → add a mutation to `scripts/selftest.py` that proves the checker catches a wrong key → build the player component. Until a checker exists the type is `UNVERIFIED` and `--strict` fails.
5. **New asset kind** (e.g. a code repo for React, a network topology for security): add its schema variant to `scenario_asset_registry.schema.json`, an `ASSET` checker, and (if blocks/interactions reference it) refs that the pack checkers resolve.
6. **Preflight** the batch (`preflight.py`, canary tile first), then run the stages in `START_HERE.md`. Re-run `selftest.py` first — it must report 0 missed.
7. **Canary-then-sample.** First tile/chunk gets full evaluator depth; sample later chunks once the defect rate is low and stable.

What never changes between roles: `finlib.py`, `schema_check.py`, `plan_tiles.py`, `assemble_tiles.py`, `validate_tile.py`, `update_ledger.py`, `selftest.py`, the stage instruction files, the core/data schemas, and the loop in `START_HERE.md`.
