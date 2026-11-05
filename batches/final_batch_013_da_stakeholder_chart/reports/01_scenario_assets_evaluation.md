# Stage 01 — Scenario Asset Registry Evaluation

**Batch:** `final_batch_013_da_stakeholder_chart`  
**Tile:** `tile_stakeholder_chart_matching_simplifying`  
**Concepts:** `stakeholder.chart_type_to_point_matching`, `stakeholder.simplifying_charts_for_audience`

## Checks Performed

### 1. Structural Integrity
- Row widths match column counts in both datasets. ✓
- `semantic_role` assignments are defensible and non-ambiguous for all columns. ✓
- `week_number` marked as `identifier` with `numeric_looking_label: true` — defensible since it's a label for time periods, not a quantity to aggregate. ✓
- All variant ops reference valid columns and rows. ✓
- `share_pct` values sum to 100.0 and are consistent with `order_count` proportions. ✓

### 2. Glossary Example Consistency
- Teaching block tb2 (concept 1): "average delivery time side by side across Lagos, Abuja, and Kano" — all three cities present in `ds_city_delivery_summary`. ✓
- Teaching block tb2 (concept 1): "Lagos delivery time rising week over week" — Lagos values in `ds_weekly_delivery_trend` are 34.0 → 36.5 → 38.1 → 40.2, monotonically increasing. ✓
- Teaching block tb3 (concept 1): "Lagos accounts for most of our total delivery volume" — Lagos `share_pct` = 57.1%, the largest. ✓
- Teaching block tb4 (concept 1): "distance/delivery-time relationship" — `ds_weekly_delivery_trend` has both `distance_km` and `avg_delivery_minutes`. ✓
- Teaching block tb3 (concept 2): "'22.00 minutes' can become '22 min'" — Kano `avg_delivery_minutes` = 22.0 in both datasets. ✓
- `glossary_example_vocab` entries all traceable to dataset columns, scenario context, or teaching blocks. ✓

### 3. Assessment Anchor Support
- Bar chart comparison: `ds_city_delivery_summary` (avg_delivery_minutes across cities). ✓
- Line graph trend: `ds_weekly_delivery_trend` (avg_delivery_minutes over weeks). ✓
- Pie chart part-to-whole: `ds_city_delivery_summary` (share_pct sums to 100). ✓
- Scatterplot exploration: `ds_weekly_delivery_trend` (distance_km vs avg_delivery_minutes). ✓
- Boxplot distribution: `ds_weekly_delivery_trend` has 4 rows per city (minimal but usable). ✓
- Simplification anchors are conceptual/design-level and don't require specific data structures. ✓

### 4. Planted Issues
- `ds_city_delivery_summary.messy`: 3 planted issues (impossible_value, inconsistent_category, missing_value) — all are genuine instances of their stated kinds after ops are applied. ✓
- `ds_weekly_delivery_trend.messy`: 2 planted issues (duplicate_row, outlier_suspicious) — both are genuine instances after ops. ✓
- Op ordering is correct; `occurrence` indices are valid after preceding ops. ✓

### 5. Semantic Role Ambiguity Check
- No column has two defensible semantic_role readings that would change how it's used in exercises. ✓

## Defects Found

1. **ADVISORY** `ds_city_delivery_summary/description`: The description claims the dataset "Supports … boxplot (distribution) exercises" but with only 1 row per city, no meaningful boxplot can be drawn from this dataset alone. The boxplot concept is taught at the selection/decision level (when to use vs. not use), and `ds_weekly_delivery_trend` (4 rows per city) could serve boxplot exercises instead. → Revise description to remove boxplot claim, e.g., "Supports bar-chart (comparison) and pie-chart (part-to-whole) exercises."

2. **ADVISORY** `scen_ng_logistics/glossary_example_vocab`: The vocab list includes `"week"` but the actual column name is `"week_number"`. The teaching blocks use "week over week" as a natural-language phrase, so this is not a data mismatch, but adding `"week_number"` to the vocab list would be more precise. → Add `"week_number"` to `glossary_example_vocab` or replace `"week"` with `"week_number"`.

## Verdict

No blocking defects found. Both advisory items are cosmetic/descriptive and do not affect taught facts, data integrity, or exercise correctness.

**VERDICT: PASS**
