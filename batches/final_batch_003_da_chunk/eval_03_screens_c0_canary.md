# Stage 03 Screens Evaluation — c0_canary (tile_stats_shape_outliers)

## Summary
Evaluated all steps in the canary tile `tile_stats_shape_outliers` covering three concepts: stats.distribution_shape, stats.outlier_reasoning, and stats.frequency_distribution_reading.

## Defects Found

### BLOCKING

1. **tile_stats_shape_outliers.s01/b3 (chart block)**: The chart claims to show "Three bar charts placed side by side" with right-skewed, left-skewed, and symmetric distributions, but the `asset_ref` only points to `ds_delivery_times_sample` which contains data for a single right-skewed distribution (9 values: 18, 20, 22, 22, 26, 28, 34, 41, 52). The visual cannot serve its `visual_anchor.purpose` of showing "Three value spreads side by side, one with the tail trailing right, one trailing left and one trailing evenly both ways."

   **Fix**: Either:
   - (a) Create a new asset `ds_distribution_shape_comparison` with three separate datasets (right-skewed, left-skewed, symmetric) and update the asset_ref, OR
   - (b) Change the chart to a `diagram` block type with illustrative/conceptual content that doesn't require data-driven rendering, OR
   - (c) Simplify the chart to show only the right-skewed QuickShip data and update the title/alt_text to: `"title": "Right-skewed distribution: QuickShip delivery times"` and `"alt_text": "A bar chart showing the QuickShip delivery-time sample with bars tallest at 18–28 min and a long tail trailing right toward 52 min — labelled Right-skewed. An arrow marks the long tail."` and remove the left-skewed and symmetric annotations.

### ADVISORY

1. **tile_stats_shape_outliers.s06/b4**: Minor wording difference from glossary. Glossary m1 says "genuine, correct observation" but screen says "genuine observation". Meaning is preserved.

2. **tile_stats_shape_outliers.s12**: The lede omits the 50–80 min bin (0 orders) from the frequency table listing. Does not affect the question ("Which bin has the most orders?") or answer (20–30 min with 9 orders).

## Verification Notes

- Mean (29.2) and median (26) for the 9-value dataset verified correct
- Frequency table totals (21 orders) verified correct
- Outlier variant (7 values: 18, 20, 22, 22, 26, 28, 80) verified correct
- All required facts from glossary are covered in the teaching content
- No blocked_future_concepts are required to understand the content
- Video bridge notes appropriately flag terminology differences

## VERDICT: FAIL

One blocking defect: chart block s01.b3 cannot render the described three-way comparison with only single-distribution data.
