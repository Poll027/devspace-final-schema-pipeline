# 03 screens — GENERATOR
Write `batches/<batch_id>/screens.json` (`kind: screens_part`, schema `screens_part.schema.json`) for the assigned tiles. Read `tile_plans.json`, `inputs/path_glossary_bundle.json`, `scenario_asset_registry.json`, playbook §2 and §5.

1. **The plan is law.** Same `step_id`s, types and order; for each planned step copy `concept_ids`, and set `lineage.teaching_block_ids` and `fact_ids` equal to the plan's. `check`/`hands_on` steps carry framing only (title, eyebrow, lede, reward, lineage) — their interactions are stage 04. Extra `remediation` steps (`<tile>.rNN`) are allowed and expected.
2. **Re-voice, don't re-teach.** Turn the glossary teaching blocks into short screen text using the registry's scenario values. Keep every fact's meaning; never add a claim, upgrade a hedge ("commonly" → "always"), close an open list, or add a cause. No concept from `blocked_future_concepts`. **The text must teach on its own** — never "as the video shows".
3. Each `prose` block: one idea, about 90 words or fewer, with `lineage {concept_ids, teaching_block_ids, fact_ids}` using qualified ids (`<concept_id>#f1`, `<concept_id>#tb2`, `<concept_id>#assessment:<capability>`, `#practice`, `#visual`). Stay within the step's `word_budget`.
4. **Visuals:** realise the planned block type (or an allowed alternate in `registry/anchor_mapping.json`) and tag it `lineage.anchors: ["<concept_id>#visual"]`. Data visuals reference registry assets with `asset_ref` — never inline rows. Code/formula/chart outputs are computed in stage 05; do not type them.
5. **Video steps:** a `media_group` with `segment_ids` only (assemble copies segments, summaries and bridge notes from the glossary).
6. **Recap:** the planned takeaways plus an `up_next` block naming the next tile's first idea.
7. Add a short `remediation` step for the first check/hands-on of each concept (same dataset, one clear contrast).
8. Gate: `schema_check.py screens_part.schema.json batches/<id>/screens.json`; then, once interactions exist, `assemble_tiles.py` + `validate_tile.py`.

Mistakes to avoid: unqualified fact ids; text blocks with no lineage; any mention of the video; examples that disagree with registry values (ids, cities, numbers); step text over budget; paraphrase that changes meaning; showing a column the dataset lacks; forgetting `#visual` on the visual block.
Reply with: artifact path, step counts, anything you were unsure about.
