# Pedagogy Review — final_batch_005_da_sql_canary

**Reviewer:** Independent evaluator (stage 08)  
**Tiles reviewed:** tile_sql_fund_relational_select, tile_sql_fund_alias_distinct  
**Date:** 2026-10-27

---

## Tile 1: tile_sql_fund_relational_select

### Structure
- **Steps:** 10 main + 2 remediation (within 8–14 range ✓)
- **Estimated time:** 9.5 min (within 6–12 range ✓)
- **Concepts:** sql.relational_model, sql.select_fundamentals
- **Flow:** explain → check → apply for both concepts ✓

### Step-by-step review

| Step | Type | Concept | Notes |
|------|------|---------|-------|
| s01 | explainer | relational_model | Introduces tables, rows, columns with data_table visual. One idea. ✓ |
| s02 | explainer | relational_model | Well-formed table properties (unique name, no duplicates, one kind of thing). One idea. ✓ |
| s03 | check | relational_model | Tests well-formedness judgment. All distractors have accurate feedback. Remediation → r01 (well-formed tables). ✓ |
| s04 | hands_on | relational_model | table_select: identify row and column in orders table. Clear tasks. **Remediation → r01 is a mismatch** (see findings). |
| s05 | explainer | select_fundamentals | Introduces SELECT/FROM and AS output_name. Two sub-topics in one step but both are parts of the same statement syntax under one concept. Reading load ~106 words, acceptable. |
| s06 | video | select_fundamentals | Live demo of SELECT with step-through. Bridge text differentiates from text (no AS in clip). Adds visual execution flow. ✓ |
| s07 | explainer | select_fundamentals | SELECT * shorthand. One idea, light step. ✓ |
| s08 | check | select_fundamentals | Four-option MCQ on correct SELECT syntax. All feedback accurate. ✓ |
| s09 | hands_on | select_fundamentals | Write SELECT with AS rename. Expected data matches registry. ✓ |
| s10 | recap | both | Summarizes key takeaways. up_next previews aliasing tile. ✓ |

### Remediation review
- **r01** (well-formed tables): Correctly addresses s03 (well-formedness check). Does NOT address s04 (row/column identification). See BLOCKING finding below.
- **r02** (SELECT list vs FROM clause): Correctly addresses s08 and s09.

---

## Tile 2: tile_sql_fund_alias_distinct

### Structure
- **Steps:** 8 main + 2 remediation (within 8–14 range ✓)
- **Estimated time:** 7.4 min (within 6–12 range ✓)
- **Concepts:** sql.aliasing, sql.distinct
- **Flow:** explain → check → apply for both concepts ✓

### Step-by-step review

| Step | Type | Concept | Notes |
|------|------|---------|-------|
| s01 | explainer | aliasing | Table aliases with code_walkthrough. One idea. ✓ |
| s02 | explainer | aliasing | Column aliases and qualified references. Two sub-topics but tightly coupled under one concept. ~133 words, slightly heavy but acceptable. |
| s03 | check | aliasing | Tests alias qualification + column rename. All distractor feedback accurate and addresses specific mistakes. ✓ |
| s04 | hands_on | aliasing | Write query with table alias and column qualification. Expected data matches registry. ✓ |
| s05 | explainer | distinct | DISTINCT definition with before_after visual. **After panel asset_ref issue** (see findings). |
| s06 | check | distinct | Predict row count with DISTINCT. City distribution (Lagos 3, Abuja 3, Kano 2) verified against registry. All feedback accurate. ✓ |
| s07 | hands_on | distinct | Write SELECT DISTINCT query. Expected data matches registry. Hidden variant test is well-designed. ✓ |
| s08 | recap | both | Summarizes aliases and DISTINCT. up_next previews WHERE filtering. ✓ |

### Remediation review
- **r01** (alias must be used): Addresses s03 and s04 (alias usage). Covers f2 only; s03 tests f3/f4 — partial but the most common mistake is addressed.
- **r02** (DISTINCT vs ALL): Correctly addresses s06 and s07. Data claims verified against registry.

---

## Findings

### BLOCKING

1. **tile_sql_fund_relational_select/s04**: Remediation mismatch. Step s04 (table_select) tests the learner's ability to identify rows and columns (facts f1, f2, f4 — "what is a row/record/tuple" and "what is a column/field/attribute"). Its remediation_step_id points to r01, which teaches about well-formed table properties (facts f3, f5 — unique name, no duplicates, one kind of thing). A learner who cannot identify a row or column gets remediation about table design, which does not address their actual mistake.  
   → **Fix:** Create a new remediation step (e.g. `tile_sql_fund_relational_select.r03`) that re-explains what rows and columns are, referencing facts f1 and f2 (rows = records/tuples representing one group of related values; columns = fields/attributes). Point s04's `feedback.remediation_step_id` to this new step. Alternatively, change s04's remediation_step_id to point to a step that re-teaches row/column identification.

2. **tile_sql_fund_alias_distinct/s05**: The before_after block's "after" panel uses `asset_ref: { asset_id: "ds_customers", columns: ["city"], max_rows: 3 }`. If the player renders this as the first 3 rows of the customers table's city column, it would display Lagos, Abuja, Lagos — not the DISTINCT result (Lagos, Abuja, Kano). The caption says "SELECT DISTINCT city FROM customers — one row per unique city" and the change_summary says "3 unique cities (Lagos, Abuja, Kano)," so the text is correct, but the data_table asset_ref would produce contradictory data if rendered literally.  
   → **Fix:** Replace the "after" panel's asset_ref with an inline result set showing the three unique cities explicitly, e.g. `{ "rows": [["Lagos"], ["Abuja"], ["Kano"]], "columns": ["city"] }`, or use a dedicated variant/view asset that represents the DISTINCT result. Alternatively, remove `max_rows: 3` and add a `query` or `transform` field that indicates deduplication.

### ADVISORY

3. **tile_sql_fund_relational_select/s05**: This step teaches both SELECT/FROM basics (f1, f3) and AS column renaming (f2) in one step. While both are under the same concept (sql.select_fundamentals) and are parts of the same statement syntax, splitting AS into its own short step would reduce cognitive load for absolute beginners.

4. **tile_sql_fund_alias_distinct/s02**: Reading load (~133 words across two prose blocks) is the heaviest in either tile. Covers column aliasing (f3) and qualified column references (f4). Both are tightly coupled but could be split for lighter steps.

5. **tile_sql_fund_alias_distinct/s03→r01**: The check tests `qualify_and_alias_columns_correctly` (f3, f4) but remediation r01 only covers f2 (alias replaces original name). A learner confused about qualified references (f4) or column aliasing syntax (f3) would benefit from remediation that also covers those facts.

6. **tile_sql_fund_relational_select/s06**: The video segment uses different column names (first_name, country) than the lesson's scenario (name, city). The bridge text handles this well, but a brief note in the bridge acknowledging the different column names would help learners who notice the discrepancy.

---

## Summary

| Category | Count |
|----------|-------|
| BLOCKING | 2 |
| ADVISORY | 4 |

Both tiles follow the explain → check → apply flow correctly. Step counts and timing are within range. All glossary facts are covered. Data in expected results matches the scenario registry. The two blocking issues are (1) a remediation that doesn't address the specific mistake being tested, and (2) a before_after visual whose asset_ref would produce data contradicting the text if rendered literally.

**VERDICT: FAIL**
