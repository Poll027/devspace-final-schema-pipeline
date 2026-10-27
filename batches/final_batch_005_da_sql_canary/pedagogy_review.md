# Pedagogy Review — final_batch_005_da_sql_canary

**Reviewer:** Independent evaluator (stage 08)  
**Tiles reviewed:** tile_sql_fund_relational_select, tile_sql_fund_alias_distinct  
**Date:** 2026-10-27

---

## Tile 1: tile_sql_fund_relational_select

### Structure
- **Steps:** 10 (+ 4 remediation) — within 8–14 range ✓
- **Estimated time:** 9.7 min — within 6–12 min range ✓
- **Concepts:** sql.relational_model, sql.select_fundamentals

### Explain → Check → Apply flow
| Concept | Explain | Check | Apply |
|---|---|---|---|
| sql.relational_model | s01, s02 | s03 | s04 |
| sql.select_fundamentals | s05, s06 (video), s07 | s08 | s09 |

Flow is correct: every check arrives after its idea is explained; every hands-on follows its check. ✓

### Step-by-step notes

- **s01 (explainer):** Introduces tables, rows, columns with a data_table visual of ds.customers. One idea (table structure). Data table earns its place — labels row/column terminology on real data. ✓
- **s02 (explainer):** Well-formed table properties (unique name, no duplicate rows, one kind of thing). One idea. ✓
- **s03 (check):** Tests whether learner can judge a mixed-entity table design. All four option feedbacks are accurate and address the specific wrong reasoning. Remediation (r01) re-teaches well-formed properties. ✓
- **s04 (hands_on, table_select):** Learner clicks a row and a column in the customers table. Tasks are clear. Feedback addresses specific mistakes (wrong row vs wrong column). Remediation (r02) re-teaches row/column definitions. ✓
- **s05 (explainer):** Teaches SELECT list, FROM clause, and AS renaming. Three blocks (intro, definition, syntax) build progressively. The code_walkthrough visual earns its place — annotates the query line by line. All three sub-facts belong to one glossary concept (sql.select_fundamentals). ✓
- **s06 (video):** Shows a live demo of SELECT column_list FROM table. Bridge notes clarify that AS is not shown in the clip (taught in text above). The video adds concrete demonstration value beyond the text. ✓
- **s07 (explainer):** Teaches SELECT * shorthand. One idea. ✓
- **s08 (check):** Tests SELECT column list + FROM. All four option feedbacks are accurate. Remediation (r03) re-teaches SELECT list and FROM. ✓
- **s09 (hands_on, code_exercise):** Learner writes SELECT with AS rename. Prompt is clear. Expected output matches registry data (8 rows, 3 columns). Remediation (r04) re-teaches AS. ✓
- **s10 (recap):** Summarises both concepts. Up_next previews aliasing and DISTINCT. ✓

### Difficulty ramp
Intro (table structure) → core (well-formed judgment) → intro (identify rows/columns) → core (SELECT syntax) → core (write SELECT with AS). Smooth progression. ✓

### Reading load
All prose blocks are concise (1–3 sentences). No dead text identified. ✓

### Visuals
- s01 data_table: supports terminology mapping — earns its place ✓
- s05 code_walkthrough: annotates query structure — earns its place ✓
- s06 video: live demo adds beyond text — earns its place ✓

---

## Tile 2: tile_sql_fund_alias_distinct

### Structure
- **Steps:** 8 (+ 4 remediation) — within 8–14 range ✓
- **Estimated time:** 7.7 min — within 6–12 min range ✓
- **Concepts:** sql.aliasing, sql.distinct

### Explain → Check → Apply flow
| Concept | Explain | Check | Apply |
|---|---|---|---|
| sql.aliasing | s01, s02 | s03 | s04 |
| sql.distinct | s05 | s06 | s07 |

Flow is correct. ✓

### Step-by-step notes

- **s01 (explainer):** Introduces table aliases with FROM orders AS o. Code walkthrough shows alias in context. One idea (table aliasing). ✓
- **s02 (explainer):** Teaches column aliasing (AS output_name) and qualified references (alias.column). Two closely related sub-facts from one teaching block (sql.aliasing#tb3). Neither is hidden. ✓
- **s03 (check):** Tests qualified column reference with alias. All four option feedbacks are accurate and address specific syntax errors. opt_b correctly explains that the original name can't be used after aliasing. Remediation (r01) re-teaches column aliases and qualified references. ✓
- **s04 (hands_on, code_exercise):** Learner writes a query aliasing orders to o, qualifying columns, and renaming one. Expected output matches registry data (10 rows, 3 columns: order_id, customer_id, delivery_min). Remediation (r02) re-teaches table aliases. ✓
- **s05 (explainer):** Teaches DISTINCT vs ALL. before_after visual shows city column with and without DISTINCT. The "before" shows all 8 rows; the "after" shows 4 distinct cities. Data matches registry (Lagos×3, Abuja×2, Kano×2, Port Harcourt×1). Visual earns its place — makes the duplicate-collapsing concrete. ✓
- **s06 (check):** Tests prediction of row counts with/without DISTINCT. Prompt provides the city distribution. All four option feedbacks are accurate. Remediation (r03) re-teaches ALL vs DISTINCT. ✓
- **s07 (hands_on, code_exercise):** Learner writes SELECT DISTINCT city FROM customers. Expected output: 4 rows, 1 column. Matches registry. Remediation (r04) re-teaches DISTINCT. ✓
- **s08 (recap):** Summarises aliasing and DISTINCT. Up_next previews WHERE filtering. ✓

### Difficulty ramp
Core (table alias) → core (column alias + qualification) → core (DISTINCT prediction) → core (write DISTINCT). Smooth. ✓

### Reading load
All prose blocks are concise. No dead text. ✓

### Visuals
- s01 code_walkthrough: annotates alias syntax — earns its place ✓
- s05 before_after: shows duplicate collapsing — earns its place ✓

---

## Defect list

### ADVISORY

1. **ADVISORY tile_sql_fund_relational_select/s05:** Step title "SELECT, FROM and AS" bundles three syntax elements. While they belong to one glossary concept and are progressively introduced across three blocks, a title like "Your first SELECT statement" would better signal a single cohesive idea. → Consider renaming to "Writing your first SELECT statement" or similar.

2. **ADVISORY tile_sql_fund_alias_distinct/s02:** The second prose block mentions "once a query reads from more than one table" which forward-references JOINs. The learner does not need to understand JOINs to follow the step (it's motivational context from glossary fact sql.aliasing#f4), but it could momentarily confuse a beginner. → Consider softening to "once you start combining tables in later tiles" or similar.

3. **ADVISORY tile_sql_fund_relational_select/s07:** Similarly mentions "When a query reads from more than one table, table_name.* narrows the star to just that table's columns" — a forward reference from glossary fact sql.select_fundamentals#f4. Not blocking since understanding JOINs is not required. → Consider adding "(you will learn this later)" parenthetical.

---

## Summary

Both tiles follow a clean explain → check → apply flow for each concept. Step counts and timing are within bounds. All checks arrive after their ideas are taught. All remediation steps target the specific concept being tested and re-teach the relevant facts. All option feedback addresses the specific wrong reasoning. All data claims match the scenario asset registry. All visuals earn their place. No blocking defects found.

**VERDICT: PASS**
