# 06 assemble — script
```bash
python3 00_FINAL_PIPELINE_CORE/scripts/assemble_tiles.py batches/<batch_id>
python3 00_FINAL_PIPELINE_CORE/scripts/update_ledger.py batches/<batch_id> record 06_assemble "tile_lessons/*.json" PASS
```
Compiles parts into `tile_lessons/`, splits `tile_lessons_public/` and `grading/`, copies media segments and bridge notes from the glossary, computes `requires`, pacing and hashes. Exit 1 if a part is missing/unmatched or a lesson fails the `tile_lesson` schema.
