# 02 tile plan — script
```bash
python3 00_FINAL_PIPELINE_CORE/scripts/plan_tiles.py batches/<batch_id>
python3 00_FINAL_PIPELINE_CORE/scripts/update_ledger.py batches/<batch_id> record 02_tile_plan tile_plans.json PASS
```
Deterministic step skeleton per tile (rules in the script header and `registry/anchor_mapping.json`). Read the printed WARN lines: a warning such as "no interaction type registered" or "no block mapping" means a developer must add a type (NEW_ROLE_RUNBOOK step 4) before that tile can be authored. The plan is law for stages 03–04.
