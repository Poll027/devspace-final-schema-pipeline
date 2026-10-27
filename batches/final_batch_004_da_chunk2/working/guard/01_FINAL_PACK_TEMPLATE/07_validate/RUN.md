# 07 validate — script (the deterministic gate)
```bash
python3 00_FINAL_PIPELINE_CORE/scripts/validate_tile.py batches/<batch_id> [--strict]
python3 00_FINAL_PIPELINE_CORE/scripts/update_ledger.py batches/<batch_id> record 07_validate reports/validation.tiles.json PASS
```
Universal checks + pack checkers (see the script header). Read the UNVERIFIED warnings: each is something no checker could verify; `--strict` turns them into errors and should be the bar for publishing. Before relying on this gate after any change: `selftest.py batches/<batch_id>` → `0 missed`.
