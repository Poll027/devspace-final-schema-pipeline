# Evaluation — 04_interactions (chunk c1)

**Batch:** `final_batch_006_da_sql_rest`  
**Tiles evaluated:** `tile_sql_fund_sorting_limiting`, `tile_sql_fund_aggregating_data`, `tile_sql_case_expressions`  
**Total interactions reviewed:** 14 (4 + 7 + 3)

## Methodology

1. Read every interaction blind from the lesson text and glossary facts, then compared with the provided key.
2. Verified all expected query results against the `ds_orders` dataset (13 rows).
3. Checked each choice question for: single defensible answer, no distractor that is actually correct, feedback accuracy, and alignment with glossary facts.
4. Checked each code exercise for: prompt pinning (columns, column order, row order), alternative-query acceptance, practice anchor success sentence alignment, and starter completeness.
5. Cross-referenced every `measures` entry against glossary assessment anchors and fact IDs.

## Data Verification

All computed expected results match the `ds_orders` dataset:
- **s03 (sorting):** 13 rows, region ASC / order_id DESC — verified ✓
- **s06 (top 5):** 5 rows, amount DESC — verified ✓
- **s05 (aggregating):** SUM=69400.0, AVG=5338.461538461538 — verified ✓
- **s09 (GROUP BY):** north=24950, other=11150, south=33300 — verified ✓
- **s13 (HAVING):** north=24950, south=33300 (both >20000) — verified ✓
- **case s05:** All 13 labels correct (small/medium/large boundaries at 3000/7000) — verified ✓

## Choice Questions

All 8 choice questions have exactly one defensible correct answer. No distractor is actually correct. All wrong-option feedback is factually accurate. All questions test concepts taught in earlier steps within the same tile.

## Code Exercises

All 6 code exercises:
- Pin output columns and their order in the prompt
- Pin row ordering where applicable (ordered=true with ORDER BY in prompt)
- Accept alternative SQL phrasings that produce the same result set
- Align with their practice anchor's success sentence
- Have starters that are genuinely incomplete (comments only)

## Defects

### ADVISORY

1. **tile_sql_fund_aggregating_data/s12 hint[1]:** The hint says "Aggregate functions like SUM can only appear in HAVING, not in WHERE." This is technically imprecise — aggregates can also appear in SELECT, ORDER BY, etc. The statement is correct only in the narrow context of filtering clauses. → Consider rewording to "For filtering, aggregate functions like SUM belong in HAVING, not in WHERE."

## VERDICT: PASS
