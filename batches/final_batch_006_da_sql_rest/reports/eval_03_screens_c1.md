# Evaluation Report — Stage 03 Screens, Chunk c1

**Batch:** `final_batch_006_da_sql_rest`  
**Tiles evaluated:** `tile_sql_fund_sorting_limiting`, `tile_sql_fund_aggregating_data`, `tile_sql_case_expressions`  
**Evaluator scope:** All steps reviewed (3 tiles, 27 main steps + 8 remediation steps).

## Methodology

- Re-derived every factual claim from the glossary bundle (`path_glossary_bundle.json`) and the scenario asset registry (`scenario_asset_registry.json`).
- Verified all data-specific claims (row counts, NULL counts, customer groupings) against the `ds_orders` asset.
- Checked that no step requires understanding of a `blocked_future_concepts` concept.
- Verified code_walkthrough line-number annotations against the actual code.
- Confirmed assessment anchors and practice anchors match the glossary bundle.

## Findings

### Tile: tile_sql_fund_sorting_limiting

All facts (sql.order_by#f1–f3, sql.limit_offset#f1–f2, sql.limit_offset#m1) are accurately represented. The before/after visual correctly demonstrates multi-column ORDER BY. The process_flow for LIMIT/OFFSET correctly shows OFFSET-then-LIMIT ordering. The remediation steps accurately restate the glossary facts. The "13-row orders table" claim matches the registry (13 rows). No issues found.

### Tile: tile_sql_fund_aggregating_data

All six aggregate function facts (f1–f6) are accurately covered. The "two undelivered QuickCart orders" claim matches the registry (orders 1011 and 1012 have NULL delivery_time_minutes). The remediation r01 claim "COUNT(*) returns 13 while COUNT(delivery_time_minutes) returns 11" is arithmetically correct (13 − 2 = 11). The GROUP BY diagram correctly lists customer_id=1 → {1001,1003,1006,1009,1012,1013}, customer_id=2 → {1002,1005,1008,1011}, customer_id=3 → {1004,1007,1010}, matching the registry. HAVING facts f1–f2 are accurately represented. The process_flow (WHERE → GROUP BY → HAVING) is correct. No issues found.

### Tile: tile_sql_case_expressions

All three facts (f1–f3) are accurately covered. The code_walkthrough annotations correctly map to the SQL code lines. The "Branch 2: Returns 'normal' for times 20–39" annotation is correct (≥20 and <40). The ELSE/NULL behavior and simple CASE form are accurately described. No issues found.

## Defects

No blocking defects found. No advisory defects found.

## Verdict

VERDICT: PASS
