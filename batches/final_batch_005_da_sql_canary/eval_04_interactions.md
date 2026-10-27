# Stage 04 Interactions — Evaluation Report

**Batch:** final_batch_005_da_sql_canary  
**Tiles evaluated:** tile_sql_fund_relational_select, tile_sql_fund_alias_distinct  
**Interactions evaluated:** All 7 (canary batch — full coverage)

## Evaluation Method

1. Read every interaction blind against the lesson text, glossary facts, and scenario registry data.
2. Solved each interaction independently before checking the key.
3. Verified data values in expected results against the scenario asset registry.
4. Checked code exercises for alternative-correct-query risks, prompt pinning, and hidden test coverage.

## Tile: tile_sql_fund_relational_select

### s03 (choice) — Judge table design well-formedness
- **Key:** opt_b (mixes two kinds of thing). Correct per glossary f5 ("Each table should contain information about one kind of thing only").
- **Distractors:** All clearly wrong. opt_d feedback accurately notes that no-duplicate-rows is necessary but not sufficient (f3 + f5). ✅
- **No defects.**

### s04 (table_select) — Identify row and column
- **Key:** Row where customer_id=3 (Fatima Bello), column "city". Verified against registry: Fatima Bello is customer_id=3, within the first 4 rows shown (max_rows=4). ✅
- **Facts:** f1 (row=record/tuple), f2 (columns=fields/attributes), f4 (database composed of tables). All exercised. ✅
- **No defects.**

### s08 (choice) — Identify correct SELECT statement
- **Key:** opt_a ("SELECT name, city FROM customers"). Correct per f1 (SELECT list) and f3 (FROM clause). ✅
- **Distractors:** opt_b wrong clause order, opt_c table name after SELECT, opt_d returns all columns. All clearly wrong with accurate feedback. ✅
- **No defects.**

### s09 (code_exercise) — Write SELECT with AS rename
- **Prompt pins:** Column names (customer_name, city, customer_id), column order, and requires AS. ✅
- **Solution:** `SELECT name AS customer_name, city, customer_id FROM customers;` ✅
- **Expected data:** 8 rows matching registry exactly. ✅
- **Alternative queries:** Omitting AS (e.g., `SELECT name customer_name, ...`) would produce the same result and pass the test, but the prompt explicitly says "using AS". The hidden test blocks table aliases. Acceptable.
- **Practice anchor:** "The query runs and returns exactly the three requested columns in the requested order, with the renamed column showing its new name." Satisfied. ✅
- **No defects.**

## Tile: tile_sql_fund_alias_distinct

### s03 (choice) — Qualify column with alias and rename
- **Key:** opt_a ("SELECT o.delivery_time_minutes AS delivery_min"). Correct per f3 (column aliasing) and f4 (correlation.columnname). ✅
- **Distractors:** opt_b uses original table name after aliasing (correctly flagged per f2), opt_c puts alias after AS (wrong syntax), opt_d garbled syntax. All clearly wrong with accurate feedback. ✅
- **No defects.**

### s04 (code_exercise) — Alias table, qualify columns, rename column
- **Prompt pins:** Column names (order_id, customer_id, delivery_min), column order, requires AS for both table alias and column rename. ✅
- **Solution:** `SELECT o.order_id, o.customer_id, o.delivery_time_minutes AS delivery_min FROM orders AS o;` ✅
- **Expected data:** 10 rows matching registry exactly. ✅
- **Alternative queries:** Could omit AS in `FROM orders o` or write `delivery_time_minutes delivery_min`. Prompt explicitly says "using AS" for both. Test checks result equality. Hidden test blocks DISTINCT. Acceptable.
- **Practice anchor:** "The query runs, returns the correct rows, and uses the alias to qualify every column reference." Satisfied. ✅
- **No defects.**

### s06 (choice) — Predict rows with/without DISTINCT
- **Key:** opt_a ("Query A: 8 rows. Query B: 4 rows."). Correct per registry (8 customers, 4 unique cities) and f2 (SELECT ALL is default). ✅
- **Distractors:** All clearly wrong with accurate feedback referencing the default ALL behavior and DISTINCT collapsing. ✅
- **No defects.**

### s07 (code_exercise) — Write DISTINCT query for unique cities
- **Prompt pins:** Column name (city), unique values only. ✅
- **Solution:** `SELECT DISTINCT city FROM customers;` ✅
- **Expected data:** 4 rows (Lagos, Abuja, Kano, Port Harcourt), ordered=false. Matches registry. ✅
- **Alternative queries:** `SELECT DISTINCT city AS city FROM customers;` would also pass — this is fine, it's equivalent. ✅
- **Practice anchor:** "The query returns one row per distinct value, with no value repeated." Satisfied. ✅
- **Feedback:** "collapsing the three Lagos rows into one" — registry confirms 3 Lagos customers. ✅
- **No defects.**

## Summary

All 7 interactions are correct, well-pinned, and aligned with glossary facts and registry data. No blocking or advisory defects found.

---

VERDICT: PASS
