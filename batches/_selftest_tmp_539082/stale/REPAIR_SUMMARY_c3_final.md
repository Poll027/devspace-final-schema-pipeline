# Repair Round Summary: interactions.part.c3.json

## Artifact Path
`batches/final_batch_009_da_pandas/interactions.part.c3.json`

## Changes Made

### BLOCKING Fixes Applied:
1. **tile_pandas_map_apply/s02** - Changed opt_b feedback to clarify `.replace()` vs `.map()` distinction
2. **tile_pandas_map_apply/s02b** - Added new check step for `map_series_with_function(f1)` capability
3. **tile_pandas_map_apply/s03** - Removed `map_series_with_function(f1)` from MEASURES (moved to new s02b)
4. **tile_pandas_groupby_melt/s05** - Changed test from `stdout_equals` to `dataframe_equals`; updated solution to use column-selected form `df.groupby(key)['order_value'].agg(agg_funcs)`
5. **tile_pandas_groupby_melt/s08** - Changed question stem to "Which single `melt()` call..." and updated opt_b feedback
6. **tile_pandas_pivot_export/s08** - Added test t3 to enforce `index=False` (checks for absence of 'Unnamed: 0' column)

### ADVISORY Fixes Applied:
1. **tile_pandas_groupby_melt/s09** - Changed allowed_syntax `value_name='value'` to `value_name='deliveries'`
2. **tile_pandas_pivot_export/s08** - Renamed variable `no_index` to `write_index` in starter and solution

### ADVISORY Fixes NOT Applied:
1. **tile_pandas_map_apply/s07** - Did NOT change MEASURES to `apply_function_across_rows_with_axis_1` because it caused coverage error (anchor `apply_function_down_columns` would be unmeasured)

## Interaction Counts
- tile_pandas_map_apply: 5 interactions (was 4, added s02b)
- tile_pandas_groupby_melt: 4 interactions
- tile_pandas_pivot_export: 4 interactions

## Known Issue
The groupby_melt s05 sandbox validation fails with "solution uses 'idx'" error. The glossary's allowed_syntax `df.groupby('key')['col'].agg([...])` should permit subscript operations but the pysyntax descriptor_tags extraction doesn't recognize it. This is a glossary/checker mismatch that requires core pipeline fix, not content fix.

## Files Modified
- interactions.part.c3.json (patched)
- interactions.json (merged from c3)
- tile_lessons/tile_pandas_map_apply.json (updated with new s02b step)
- tile_lessons/tile_pandas_groupby_melt.json (updated s05 interaction)
- tile_lessons/tile_pandas_pivot_export.json (updated s08 interaction)
