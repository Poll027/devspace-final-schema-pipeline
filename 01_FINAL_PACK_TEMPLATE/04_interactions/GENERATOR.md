# 04 interactions — GENERATOR
Write `batches/<batch_id>/interactions.json` (`kind: interactions_part`, schema `interactions_part.schema.json`): exactly one interaction per `check`/`hands_on` step in the plan. Read `tile_plans.json`, `screens.json`, `inputs/path_glossary_bundle.json`, `scenario_asset_registry.json`.

1. Use the **planned interaction type**. `measures` lists `{concept_id, capability, fact_ids}` for the planned anchors (capabilities must be glossary assessment anchors). A `hands_on` includes `anchors: ["<concept_id>#practice"]` and must make the practice anchor's `success` sentence true.
2. **Test only what earlier steps taught by text.** Never test a fact first met in the video or later.
3. **Answer keys are predicates against registry assets**: rows by `where`+`occurrence`; cell answers carry `expect_value`; `classify` items carry `source` and the grading carries `role_map`; `find_issues` keys come from the variant's `planted_issues` (same ids and locations). Never hand-type a value the data can supply.
4. **One defensible answer.** If a thoughtful learner could argue for a second option, rewrite the question.
5. **Distractors come from real misconceptions** (glossary `misconceptions` first, then common errors for the concept). Every wrong option gets feedback saying *why* it is wrong, grounded in the facts — no new claims.
6. `feedback`: correct and incorrect messages, 1–2 hints that don't give the answer, `remediation_step_id` for the first check/hands-on of each concept.
7. Difficulty ramps intro → core → stretch across the tile. `grading_mode: client` for checks; `server` only for assessment tiles. `standalone: true` only if the prompt needs no earlier screen.
8. Gate: `assemble_tiles.py` then `validate_tile.py` until 0 errors (they check keys against the data and the taught-before-tested rule).

Mistakes to avoid: key typed instead of derived; two defensible answers; a distractor that is correct under a valid reading; testing an untaught fact; a capability that isn't a glossary anchor; a hands-on that can be completed without meeting the `success` criteria; "the table above" in a `standalone` prompt; a `classify` set with no trap item when the anchor is about a trap (e.g. numeric-looking labels).
Reply with: artifact path, interaction counts, anything you were unsure about.
