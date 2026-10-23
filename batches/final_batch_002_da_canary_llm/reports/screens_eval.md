# Stage 03 Screens — Evaluation Report

**Batch:** final_batch_002_da_canary_llm  
**Tile:** tile_data_shape_and_types (canary tile — all steps reviewed)

## Steps Reviewed

All 8 main steps (s01–s08) and both remediation steps (r01, r02).

## Fact Accuracy

### data.dataset_rows_columns
- **f1** ("A dataset is a collection of observations recorded on the same variables."): Correctly stated in s01.b01. ✓
- **f2** ("Data is commonly organized as a table (data matrix) of rows and columns."): Correctly stated in s01.b02. ✓
- **f3** ("Each row represents one observation (one record)."): Correctly stated in s02.b01. ✓
- **f4** ("Each column represents one variable: one attribute recorded for every observation."): Correctly stated in s02.b01. ✓

### data.categorical_numeric_types
- **f1** ("A numerical variable takes numerical values for which it is sensible to add or subtract."): Stated in s05.b02 with minor wording change (see advisory below). ✓
- **f2** ("A categorical variable's values are categories (called levels)."): Correctly stated in s05.b02. ✓
- **m1** ("A column stored as numbers is not automatically numerical…"): Correctly stated in s05.b03 with zone_code example. ✓

## Registry Data Checks

- Order 1042: [1042, "Lagos", 32, "Emeka Obi", 101] — all references in s01, s02, r01 match. ✓
- Order 1043: [1043, "Abuja", 41, "Fatima Bello", 102] — referenced in s02 as "the next row". ✓
- r01 states "city Lagos, 32 minutes, driver Emeka Obi" for order 1042 — matches registry. ✓
- r02 arithmetic: 41 − 32 = 9 — matches registry values for orders 1043 and 1042. ✓
- Column semantic roles in s05.b04 tag_columns match registry: order_id=identifier, city=categorical, delivery_min=numerical, driver=categorical, zone_code=categorical. ✓

## Blocked Future Concepts

No mention of averaging, grouping, plotting, or any concept from the blocked list. ✓

## Visual Anchors

- s01.b03 data_table: highlights one row (order 1042) and one column (city) — matches visual_anchor purpose for dataset_rows_columns. ✓
- s05.b04 data_table: tags columns by type with zone_code visibly tagged categorical — matches visual_anchor purpose for categorical_numeric_types. ✓

## Defects

1. **ADVISORY** s05.b02: Glossary fact f1 says "A numerical variable takes **numerical** values for which it is sensible to add or subtract." The screen drops the word "numerical" before "values," writing "A numerical variable takes values for which it is sensible to add or subtract." The meaning is preserved by context but the precise glossary wording is slightly weakened.

No blocking defects found.

## VERDICT: PASS
