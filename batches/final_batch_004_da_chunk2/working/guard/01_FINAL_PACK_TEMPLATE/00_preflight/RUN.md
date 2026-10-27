# 00 preflight — script
Verifies the frozen TOC and the glossary batch, and stages the batch's inputs.
```bash
python3 00_FINAL_PIPELINE_CORE/scripts/preflight.py batches/<batch_id> --path-id <path_id> \
  --glossary-bundle <path_glossary_bundle.<path>.json> --glossary-batch-id <glossary batch id> \
  --toc-workspace <dir containing freeze_manifest.json> [--tiles tile_a,tile_b] [--player-version 0.1.0]
python3 00_FINAL_PIPELINE_CORE/scripts/update_ledger.py batches/<batch_id> record 00_preflight batch_run_context.json PASS
```
Outputs: `batch_run_context.json`, `inputs/path_glossary_bundle.json` (chosen tiles' bundles + a `names` map of every concept + `tile_order`). Refuses unless the TOC is frozen and every chosen bundle is `ready_for_final_schema`. Also run `visual_inventory.py` on the full glossary once per path and keep its GAPS list (see NEW_ROLE_RUNBOOK.md).
