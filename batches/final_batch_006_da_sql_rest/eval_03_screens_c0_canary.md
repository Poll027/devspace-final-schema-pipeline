# Evaluation Report — Stage 03 Screens — c0_canary

**Tile evaluated:** `tile_sql_fund_filtering_rows`  
**Concepts covered:** `sql.where_filtering`, `sql.logical_operators`, `sql.null_handling`  
**Steps reviewed:** All 14 main steps (s01–s14) and all 8 remediation steps (r01–r08) — canary tile, full review required.

## Fact-Checking Summary

### sql.where_filtering (f1, f2)
- **s01 prose**: Accurately states WHERE keeps rows where condition is true and discards otherwise; comparison operators listed correctly including `!=` as alias for `<>`. Matches f1 and f2. ✓
- **s01 before_after**: Highlights for `WHERE delivery_time_minutes > 40` verified against registry data. Kept rows (1003/41, 1006/63, 1008/55, 1010/45, 1013/72) are all > 40. Discarded rows (1001/15, 1002/22, 1004/18, 1005/35, 1007/25, 1009/31) are all ≤ 40. Two NULL rows (1011, 1012) are not highlighted — acceptable since NULL handling is a blocked future concept at this point. ✓
- **change_summary** says "five orders" — confirmed 5 rows returned. ✓

### sql.logical_operators (f1, f2)
- **s05 prose**: AND/OR/NOT definitions match f1 exactly. ✓
- **s05 side_by_side**: SQL queries verified against registry data. No-parens query returns 8 rows; with-parens returns 4 rows. Captions and takeaway accurately describe precedence behavior per f2. ✓
- **s06 prose**: Precedence claim (NOT > AND > OR) matches f2. Parenthesized example claim verified: `WHERE customer_id = 1 AND (delivery_time_minutes > 30 OR customer_id = 2)` returns customer 1 orders with delivery_time > 30 (rows 1003, 1006, 1009, 1013). ✓

### sql.null_handling (f1, f2, m1)
- **s10 prose**: NULL as unknown value matches f1. IS NULL / IS NOT NULL predicates match f2. `= NULL` misconception matches m1. ✓
- **s10 before_after**: `= NULL` returns 0 rows, `IS NULL` returns 2 rows (1011, 1012) — verified against registry. Caption "two orders" is correct. ✓
- **s11 video**: References correct segment_id `seg_sql.null_handling_X_cPXHV2NQ4_2574_2798`. ✓

### Recap (s14)
- Accurately summarizes all three concepts' key facts. ✓

### Remediation steps (r01–r08)
- All remediation prose verified against glossary facts. No false claims found. ✓

### Blocked future concepts
- Steps s01–s04 (where_filtering) do not require understanding of logical_operators or null_handling. ✓
- Steps s05–s09 (logical_operators) do not require understanding of null_handling. ✓
- No step requires concepts beyond the three taught in this tile. ✓

### Registry data consistency
- All SQL queries and data references use `ds_orders` with correct column names. ✓
- Row data in highlights and result_of queries verified against registry rows. ✓

## Defects

ADVISORY s01/before_after: The two NULL-delivery-time rows (1011, 1012) appear in the before table (full asset_ref) but have no highlight label. This could momentarily confuse a learner who notices unlabeled rows, though omitting them is defensible since NULL handling is taught later. → Consider adding a neutral-tone "not shown" label or limiting the asset_ref rows to exclude NULLs.

## Verdict

VERDICT: PASS
