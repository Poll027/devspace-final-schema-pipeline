# Devspace Final Schema Pipeline (draft v0.1)

Turns each path's **Glossary Learning Bundles** into **tile lessons** — the screens, visuals, questions, answer keys, datasets and code exercises the player renders — authored once, validated by scripts, stored. **Role-agnostic**: one pipeline for all 64 paths. Spec: `00_FINAL_PIPELINE_CORE/PLAYBOOK.md`.

## Status (2026-10-20)
Built and tested: schemas (16 block types, 12 interaction types, registries), `preflight` · `plan_tiles` · `assemble_tiles` · `validate_tile` · `update_ledger` · `build_unions` · `visual_inventory` · `selftest`, pack checkers (`core`, `data`), per-path profiles, stage instruction files, agents.
**Canary** `batches/final_batch_001_da_canary` — Data Analyst tile `tile_data_shape_and_types` (2 concepts, 8 steps): registry gate, assemble and validate all PASS; `selftest.py` 13 mutations + 10 demo-parity interaction cases + fail-closed test, 0 missed.
**Not done:** LLM evaluator stages have not run (the canary content was authored by the orchestrator as a stand-in generator); stage 05 code/formula execution (no sandbox runner → those types are `UNVERIFIED`); stage 12 publish; the player's `grader-core` and block components; multi-chunk merge; Bedrock driver (`run_pipeline.py` port from the glossary pack).

## Layout
```
00_FINAL_PIPELINE_CORE/  PLAYBOOK.md  pipeline_manifest.json
  schemas/   one JSON Schema per block (block.*), interaction (ix.*), plus tile_lesson, step, registry, plan, parts, ledger
  registry/  block_registry · interaction_registry · anchor_mapping · path_profiles/<path_id>.json
  scripts/   the stages + finlib · schema_check · selftest · checkers/{core,data,dataset}.py
01_FINAL_PACK_TEMPLATE/  START_HERE.md  NEW_ROLE_RUNBOOK.md  <stage>/{GENERATOR,EVALUATOR,RUN}.md
.claude/agents/  final-generator (Sonnet) · final-evaluator (Opus)
examples/        demo_parity_interactions.json   batches/<batch_id>/  every artifact of one batch
```

## Try it (needs `pip install jsonschema`)
```bash
B=batches/final_batch_001_da_canary; S=00_FINAL_PIPELINE_CORE/scripts
python3 $S/validate_tile.py $B --registry && python3 $S/assemble_tiles.py $B && python3 $S/validate_tile.py $B --strict
python3 $S/selftest.py $B
python3 $S/visual_inventory.py <path_glossary_bundle.data_analyst.json>      # what a path needs from the player
```

## Decisions (2026-10-20, with the user)
Pre-authored content now, runtime-generated "custom path" later · scenario/asset registry before any screens, glossary examples may be re-voiced to registry values (facts unchanged, evaluator-checked) · client-graded checks, server-graded assessments · core visual set + pluggable per-domain packs (datasets/spreadsheets are one pack, not the model) · player prototype is the localhost:5180 app · canary first, then Bedrock on EC2 like the glossary pack · Thesys/OpenUI not adopted for core content.
