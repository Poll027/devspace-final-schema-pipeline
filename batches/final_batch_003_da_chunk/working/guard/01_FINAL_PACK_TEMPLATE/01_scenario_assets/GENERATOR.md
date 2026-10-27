# 01 scenario + asset registry — GENERATOR
Write `batches/<batch_id>/scenario_asset_registry.json` (schema `scenario_asset_registry.schema.json`) for the batch scope.

Read `inputs/path_glossary_bundle.json` (all concepts in scope: teaching blocks, anchors) and the playbook §4–5.

1. **Mine the glossary's own example vocabulary first** (tables, columns, people/places, numbers, tools it mentions in teaching blocks and anchors) and list it in `scenarios[].glossary_example_vocab`. The registry must be consistent with what the taught text already says.
2. One scenario per path (or per region if the glossary genuinely uses different domains): a short, concrete, fictional but realistic setting.
3. **Datasets**: the smallest table that supports every concept in scope. Every column/value the glossary examples rely on must exist. Declare `semantic_role` for every column; set `numeric_looking_label: true` for digits used as labels (these are the glossary's misconception traps). Authored rows only — no invented real-world facts.
4. **Variants** (messy/edge versions) only through declared ops (`set_cell`, `duplicate_row`, `drop_rows`, `drop_columns`). Record `planted_issues` with predicate `locations` (`where` + `occurrence` + `column`) and a `rule` where the kind needs one (impossible_value, inconsistent_category, ...).
5. Other asset kinds (`code_workspace`, `image`) only if an anchor needs them.
6. Gate before handing off: `python3 00_FINAL_PIPELINE_CORE/scripts/validate_tile.py batches/<batch_id> --registry` must PASS.

7. **SQL paths:** each dataset becomes a SQL table the learner queries. Use the table and column names the glossary's SQL examples use, declare real column `type`s (`integer`, `number`, `string`, `date`, `boolean`) because the SQL engine loads them as such, and give enough rows (and variants) for hidden tests to distinguish a correct query from a lazy one.

Mistakes to avoid: row width != column count; semantic_role contradicting type; a planted issue that does not hold after the ops; wrong `occurrence` for duplicates; a dataset too small/narrow for later tiles; values that contradict glossary examples (a city or column the text names but the table lacks); two defensible readings of a column's role.
Reply with: artifact path, asset ids, anything you were unsure about.
