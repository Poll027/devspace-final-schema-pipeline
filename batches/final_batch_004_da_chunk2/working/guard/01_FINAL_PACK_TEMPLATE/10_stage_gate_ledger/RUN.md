# 10 stage gate ledger — script
```bash
python3 00_FINAL_PIPELINE_CORE/scripts/update_ledger.py batches/<batch_id> verify 00_preflight 01_scenario_assets 02_tile_plan 03_screens 04_interactions 06_assemble 07_validate 08_pedagogy_review 09_leakage_check
```
Exits 1 if any gate is missing, FAIL, or STALE (its artifact changed after it was gated).
