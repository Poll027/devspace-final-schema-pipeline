# Stage 03 Screens — Evaluation Report

**Batch:** final_batch_005_da_sql_canary  
**Tiles evaluated:** tile_sql_fund_relational_select (canary — every step), tile_sql_fund_alias_distinct (every step)

## Methodology

- Re-derived all claims from the glossary bundle (`path_glossary_bundle.json`) and the scenario asset registry (`scenario_asset_registry.json`).
- Verified every required fact for each concept is taught in the tile's steps.
- Checked all data claims (row counts, column names, distinct values) against the registry.
- Verified code walkthroughs reference valid columns from the registry datasets.
- Checked prerequisite ordering and blocked_future_concepts compliance.
- Reviewed all prose for factual accuracy against glossary facts.
- Checked assessment/practice anchors match the glossary's assessment_anchors.

## Tile 1: tile_sql_fund_relational_select

### Fact coverage
All 5 required facts for sql.relational_model (f1–f5) and all 4 required facts for sql.select_fundamentals (f1–f4) are explicitly taught in the tile's explainer steps. ✓

### Data accuracy
- customers table: 3 columns (customer_id, name, city), 8 rows — matches registry. ✓
- data_table block (s01.b03) references ds_customers with columns [customer_id, name, city], max_rows 4 — valid. ✓
- Highlight targets customer_id=1 (Amara Okafor, Lagos) — exists in registry. ✓

### Code walkthrough (s05.b03)
```sql
SELECT name AS customer_name, city FROM customers;
```
All columns exist in ds_customers. Line annotations match code lines. ✓

### Concept ordering
sql.relational_model taught in s01–s04, sql.select_fundamentals in s05–s09. Prerequisite order respected. ✓

### No blocked-concept leakage
No step requires understanding of any blocked_future_concept. ✓

### No issues found.

## Tile 2: tile_sql_fund_alias_distinct

### Fact coverage
All 4 required facts for sql.aliasing (f1–f4) and both required facts for sql.distinct (f1–f2) are explicitly taught. ✓

### Data accuracy
- "8 city rows to 3 unique cities (Lagos, Abuja, Kano)" in before_after change_summary — matches registry (8 customers, 3 distinct cities). ✓
- Remediation r02 says "8 rows because there are 8 customers, even though only 3 cities appear" — matches registry. ✓

### Code walkthrough (s01.b03)
```sql
SELECT o.order_id, o.delivery_time_minutes AS delivery_min FROM orders AS o;
```
order_id and delivery_time_minutes are valid columns in ds_orders. Line annotations correct. ✓

### Concept ordering
sql.aliasing taught in s01–s04, sql.distinct in s05–s07. Prerequisite order respected. ✓

### No blocked-concept leakage
No step requires understanding of any blocked_future_concept. ✓

### Minor lineage gap (advisory)
Recap step s08 text discusses both aliasing and DISTINCT facts, but fact_ids in lineage only list sql.aliasing#f1 and sql.aliasing#f3 — missing sql.distinct#f1 and sql.distinct#f2. Content is accurate; only the lineage metadata is incomplete.

## Defect List

ADVISORY tile_sql_fund_alias_distinct/s08: Recap lineage fact_ids omit sql.distinct#f1 and sql.distinct#f2 despite the prose covering DISTINCT behavior → Add "sql.distinct#f1" and "sql.distinct#f2" to the step-level and block-level lineage fact_ids arrays.

ADVISORY tile_sql_fund_relational_select/s01.b01: Final sentence ("A database is composed of multiple tables like this, each holding data.") is near-verbatim repetition of the preceding sentence's content → Consider trimming for conciseness.

## VERDICT: PASS
