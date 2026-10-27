# Start Here — running a Final Schema batch

Stage **instructions** live in `01_FINAL_PACK_TEMPLATE/<stage>/` and are read in place, never copied. A batch's **artifacts** go in one flat folder: `batches/<batch_id>/`. Run everything from the pack root. New role? Read `NEW_ROLE_RUNBOOK.md` first. Spec: `00_FINAL_PIPELINE_CORE/PLAYBOOK.md`.

## The loop

You (the main session) are the orchestrator. **Don't author content in your own context** — dispatch it, so your context stays small and every evaluator starts fresh. Walk `00_FINAL_PIPELINE_CORE/pipeline_manifest.json` in order. Per stage `kind`:

- **`script`** — run the command in the stage's `RUN.md`. Exit 0 → record the gate. Non-zero → read the error, fix the input stage it names, rerun.
- **`generate_evaluate`** — dispatch `final-generator` with the stage id and batch folder. Run the stage's **deterministic gate first** (see below). Only if it passes, dispatch a **new** `final-evaluator` with the same ids and nothing about the generator's reasoning.
  - `VERDICT: FAIL` (≥1 BLOCKING): send all findings to a generator repair round, re-run the script gate, then a **new** evaluator **scoped to what the repair changed**. Stop after 3 failed rounds and report to the user.
  - `VERDICT: PASS` with advisories: one generator repair round, re-run the script gate, gate. **No re-evaluation.** Advisory fixes may only reword, delete, move or cite — never add a claim or change an answer key.
  - A repair may resume the same generator (cheaper). Evaluators are always new.
- **`evaluator_only`** — dispatch `final-evaluator`; it writes its own artifact.

Deterministic gates that run **before** any evaluator: stage 01 → `validate_tile.py <batch> --registry`; stage 03/04 → `assemble_tiles.py <batch>` then `validate_tile.py <batch>`. Their errors are fixed by the generator with no evaluator call.

After every gate decision:
```bash
python3 00_FINAL_PIPELINE_CORE/scripts/update_ledger.py batches/<batch_id> record <stage_id> <artifact> PASS|FAIL --generator <model|none> --evaluator <model|none> --unresolved <n>
```
`update_ledger.py <batch> verify` flags any gate whose artifact changed after it was recorded.

## Fan-out
A path has ~70 tiles. Chunk by **region boundaries, never splitting a tile** (≈10–12 tiles). Run the first chunk alone as the canary (full evaluator depth), then ≈3 chunks in parallel (more hit usage limits). Each agent writes `screens.part.<chunk>.json` / `interactions.part.<chunk>.json`; merge with the glossary pack's `merge_parts.py` pattern (port it when the first multi-chunk path runs).

## Cost control (lessons carried over from the glossary pilot)
1. Scripts before evaluators. 2. Generator self-checks against its GENERATOR.md "mistakes" list before handing off. 3. Depth tracks stakes: full verification for core concepts and anything the validator reports UNVERIFIED; sampled for standard/reference once a stage is stable. 4. Canary-then-sample, re-upgrading to full depth the moment a sampled chunk finds a real defect. 5. State a ceiling as well as a floor wherever a stage asks for a sample. 6. An `evaluator_only` PASS means "did its job", not "content was good".

## Before you trust the gates
`python3 00_FINAL_PIPELINE_CORE/scripts/selftest.py batches/<a PASSing batch>` — must print `0 missed`. Run it after any schema, checker or validator change.

## Stage kinds at a glance
| Stage | Kind | Files |
|---|---|---|
| 00_preflight | script | RUN |
| 01_scenario_assets | generate_evaluate | GENERATOR / EVALUATOR |
| 02_tile_plan | script | RUN |
| 03_screens, 04_interactions | generate_evaluate | GENERATOR / EVALUATOR |
| 05_code_exercises | generate_evaluate (planned) | GENERATOR / EVALUATOR |
| 06_assemble, 07_validate | script | RUN |
| 08_pedagogy_review, 09_leakage_check | evaluator_only | EVALUATOR |
| 10_stage_gate_ledger | script | RUN |
| 11_final_audit | evaluator_only | INDEPENDENT_AUDIT |
| 12_publish | script (planned) | RUN |
