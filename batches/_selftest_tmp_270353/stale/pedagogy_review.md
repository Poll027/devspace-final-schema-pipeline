# Pedagogy Review — final_batch_011_da_spreadsheet

**Reviewer:** Independent evaluator (stage 08)  
**Tiles reviewed:** All 11 tiles  
**Date:** 2026-11-03

---

## Summary

All 11 tiles follow the explain → check → apply flow correctly: every check and hands-on step is preceded by an explainer for the same concept. No step teaches two concepts at once (except recap steps, which are summaries). Remediation steps exist in screens.json and all remediation_step_id references resolve. Wrong-option feedback addresses the specific mistake in every choice interaction. Computed values and expected answers are consistent with the scenario asset registry data.

Two tiles exceed the 14-step guideline (lookups_troubleshooting at 17, text_date_conditional_agg at 18). All tiles except grid_references exceed the 12-minute pacing guideline. One registry-level data inconsistency exists between asset_city_totals and asset_orders_clean (Lagos total differs by 200 NGN), though the chart_types tile uses city_totals as a standalone dataset and doesn't claim it's derived from orders_clean within the lesson text.

---

## Tile-by-tile findings

### tile_spreadsheet_grid_references
- **Steps:** 9 (within 8–14) | **Minutes:** 8.0 (within 6–12)
- Flow: explainer → explainer → check → hands_on → explainer → explainer → check → hands_on → recap ✓
- All checks preceded by explainers for the same concept ✓
- Computed values verified: B2 = "Lagos" ✓, =B2 returns "Lagos" ✓
- No issues found.

### tile_spreadsheet_formula_syntax_refs
- **Steps:** 12 (within 8–14) | **Minutes:** 16.4 (exceeds 12)
- Flow: explain → check → apply pattern maintained for both concepts ✓
- Computed values: F2 = D3−D2 = 2700 ✓, F3 = SUM(D2:D21) = 99100 ✓, (D2+D3)*2 = 23400 ✓
- Mixed reference question (=$A2*B$1) is correct and well-explained ✓
- ADVISORY: Estimated time 16.4 min exceeds 12-min guideline.

### tile_spreadsheet_aggregation_logical
- **Steps:** 11 (within 8–14) | **Minutes:** 22.4 (exceeds 12)
- Flow: explain → video → explain → check → hands_on (aggregation), then explain → video → explain → check → hands_on (logical) → recap ✓
- COUNT(C2:C21) = 13 ✓, COUNTA(C2:C21) = 13 ✓, COUNTA(A2:A21) = 20 ✓
- IF formula computed values: H2 = "On Time" (C2=28 ≤ 60) ✓, H3 = "On Time" (C3=45 ≤ 60) ✓, H4 = "Late" (C4=62 > 60) ✓
- ADVISORY: Side-by-side visual (s01.b2) shows COUNT and COUNTA both returning 13 for delivery_minutes, which doesn't demonstrate the difference the takeaway claims. Using column A (order_id, all text) vs column D (amount, all numeric) would better illustrate the contrast.
- ADVISORY: Estimated time 22.4 min exceeds 12-min guideline.

### tile_spreadsheet_text_date_conditional_agg
- **Steps:** 18 (exceeds 14) | **Minutes:** 25.4 (exceeds 12)
- Four concepts in one tile (text_combining, text_extraction, date_functions, conditional_aggregation)
- Flow maintained per concept: each concept has explainer(s) before its checks/hands_on ✓
- TEXTJOIN expected value "Lagos | Delivered" verified ✓
- LEFT(A2,2) = "LG" verified ✓
- SUMIF Lagos = 28000 verified ✓
- ADVISORY: 18 steps significantly exceeds the 8–14 guideline. Consider splitting into two tiles.
- ADVISORY: Estimated time 25.4 min exceeds 12-min guideline.

### tile_spreadsheet_lookups_troubleshooting
- **Steps:** 17 (exceeds 14) | **Minutes:** 27.1 (exceeds 12)
- Three concepts (vlookup_xlookup, index_match, formula_error_troubleshooting)
- Flow maintained per concept ✓
- Driver lookup data verified against asset_drivers_vlookup and asset_drivers_index_match ✓
- ADVISORY: 17 steps exceeds the 8–14 guideline. Consider splitting into two tiles.
- ADVISORY: Estimated time 27.1 min exceeds 12-min guideline.

### tile_spreadsheet_cleaning_cross_sheet
- **Steps:** 13 (within 8–14) | **Minutes:** 17.1 (exceeds 12)
- Three concepts (remove_duplicates, text_to_columns, cross_sheet_references)
- Flow maintained ✓
- Expected values: A2 = "LG-2001" ✓, B2 of location_combined = "Lagos,Nigeria" ✓
- Cross-sheet reference syntax matches glossary facts ✓
- ADVISORY: Estimated time 17.1 min exceeds 12-min guideline.

### tile_spreadsheet_sorting_filtering
- **Steps:** 10 (within 8–14) | **Minutes:** 16.4 (exceeds 12)
- Flow maintained ✓
- D8 = 1800 (smallest amount, LG-2007) verified ✓
- D2 = 4500 verified ✓
- ADVISORY: Estimated time 16.4 min exceeds 12-min guideline.

### tile_spreadsheet_tables_named_ranges
- **Steps:** 9 (within 8–14) | **Minutes:** 10.9 (within 6–12)
- Flow maintained ✓
- Expected values: A2 = "LG-2001" ✓, C2 = 28 ✓
- No issues found.

### tile_spreadsheet_pivot_tables
- **Steps:** 11 (within 8–14) | **Minutes:** 15.1 (exceeds 12)
- Flow maintained ✓
- SUMIF Lagos = 28000 ✓, AVERAGE(D2:D21) = 4955 ✓
- s06 uses SUMIF which is taught in the prior tile (text_date_conditional_agg, position 50 vs 52) ✓
- ADVISORY: Estimated time 15.1 min exceeds 12-min guideline.

### tile_spreadsheet_chart_types
- **Steps:** 14 (at boundary of 8–14) | **Minutes:** 23.3 (exceeds 12)
- Three concepts (bar_chart, line_chart, pie_chart)
- Flow maintained ✓
- SUM(B2:B7) of city_totals = 99300 ✓ (internally consistent with asset_city_totals)
- SUM(B2:B7) of monthly_summary = 1976900 ✓
- COUNTA(A2:A7) of city_totals = 6 ✓
- ADVISORY: asset_city_totals Lagos total (28200) differs from SUMIF on asset_orders_clean (28000) by 200 NGN. The tile summary says "from Orders data" and the pie chart text says "the cities together represent all orders", implying derivation from orders_clean. This is a registry-level inconsistency.
- ADVISORY: Estimated time 23.3 min exceeds 12-min guideline.

### tile_spreadsheet_formatting_validation
- **Steps:** 11 (within 8–14) | **Minutes:** 15.0 (exceeds 12)
- Flow maintained ✓
- C2 < 30 → TRUE (C2=28) ✓
- E2 = "Delivered" → validation formula returns TRUE ✓
- ADVISORY: Estimated time 15.0 min exceeds 12-min guideline.

---

## Cross-cutting checks

| Check | Result |
|---|---|
| Explain before check (every tile) | ✓ All checks preceded by explainer for same concept |
| One idea per step | ✓ No non-recap step has >1 concept_id |
| Remediation addresses specific mistake | ✓ All wrong-option feedback is specific |
| Visuals earn their place | ✓ (one weak case: COUNT/COUNTA side-by-side) |
| Reading load per step | ✓ No step exceeds ~200 words of prose |
| 8–14 steps per tile | ✗ 2 tiles exceed (lookups: 17, text_date: 18) |
| 6–12 minutes per tile | ✗ 9 of 11 tiles exceed 12 min |
| Video adds value | ✓ Videos cover demonstration aspects text doesn't |
| Next-tile chain matches tile_order | ✓ |
| Computed values match registry | ✓ (except city_totals/orders_clean cross-asset) |

---

## Defect list

ADVISORY tile_spreadsheet_formula_syntax_refs/pacing: estimated_minutes 16.4 exceeds 12-min guideline → consider trimming or splitting content

ADVISORY tile_spreadsheet_aggregation_logical/s01.b2: COUNT/COUNTA side-by-side both return 13 for delivery_minutes column, failing to demonstrate the difference the takeaway claims → use column A (text order_ids) for COUNTA and column D (numeric amounts) for COUNT to show different results

ADVISORY tile_spreadsheet_aggregation_logical/pacing: estimated_minutes 22.4 exceeds 12-min guideline → consider splitting aggregation and logical into separate tiles

ADVISORY tile_spreadsheet_text_date_conditional_agg/pacing: 18 steps and 25.4 min far exceed 8–14 step and 6–12 min guidelines → split into two tiles (e.g., text+date and conditional_aggregation)

ADVISORY tile_spreadsheet_lookups_troubleshooting/pacing: 17 steps and 27.1 min far exceed 8–14 step and 6–12 min guidelines → split into two tiles (e.g., lookups and error_troubleshooting)

ADVISORY tile_spreadsheet_cleaning_cross_sheet/pacing: estimated_minutes 17.1 exceeds 12-min guideline → consider trimming

ADVISORY tile_spreadsheet_sorting_filtering/pacing: estimated_minutes 16.4 exceeds 12-min guideline → consider trimming

ADVISORY tile_spreadsheet_pivot_tables/pacing: estimated_minutes 15.1 exceeds 12-min guideline → consider trimming

ADVISORY tile_spreadsheet_chart_types/pacing: estimated_minutes 23.3 exceeds 12-min guideline → consider splitting three chart concepts across two tiles

ADVISORY tile_spreadsheet_chart_types/registry: asset_city_totals Lagos total (28200) differs from SUMIF on asset_orders_clean Lagos (28000); tile summary says "from Orders data" implying derivation → reconcile city_totals with orders_clean, or remove "from Orders data" from tile summary

ADVISORY tile_spreadsheet_formatting_validation/pacing: estimated_minutes 15.0 exceeds 12-min guideline → consider trimming

---

VERDICT: PASS
