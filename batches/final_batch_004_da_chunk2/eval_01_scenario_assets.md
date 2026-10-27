# Stage 01 Scenario Asset Registry — Evaluator Report

**Batch:** final_batch_004_da_chunk2  
**Artifact:** scenario_asset_registry.json  

## Evaluation Summary

Checked all five assets and both messy variants against the glossary bundle. Two data-integrity errors found that would teach wrong facts.

---

### BLOCKING Defects

**1. ds_ab_test_results / test_prop_B row: `null_value_in_ci` contradicts the CI bounds and glossary fact f3**

The row for `test_prop_B` has `ci_lower = 0.15`, `ci_upper = 0.41`, and `null_value_in_ci = "no"`. However, 0.333 falls inside [0.15, 0.41], so `null_value_in_ci` should be `"yes"`. This directly contradicts glossary fact f3 for concept `stats.business_conclusion_from_experiment`, which requires the second textbook example to have the null value (p0 = 0.333) **outside** the 95% CI, with the entire interval below 0.333. The current data cannot serve as that example.

**Fix:** Change `test_prop_B` to `conversions: 10`, `conversion_rate: 0.20`, `p_value: 0.046`, `ci_lower: 0.09`, `ci_upper: 0.31`, keeping `null_value_in_ci: "no"`. This places the entire interval below 0.333, matching the glossary requirement.

---

**2. ds_capstone_zone_summary / Lagos-South row: `pct_on_time` is 33.3 but should be 0.0**

The underlying `ds_capstone_orders` data for Lagos-South contains three orders: ORD-002 (28.1 min, "no"), ORD-006 (null, "unknown"), ORD-010 (29.8 min, "no"). Zero known deliveries meet the 25-minute target. Whether computed over 2 non-null orders (0/2 = 0%) or all 3 (0/3 = 0%), `pct_on_time` must be 0.0, not 33.3. This would teach a wrong fact about which zones are partially on-target.

**Fix:** Change the Lagos-South row's `pct_on_time` from `33.3` to `0.0`.

---

### ADVISORY Defects

**3. ds_capstone_zone_summary / Lagos-South: `n_orders` = 3 but `avg_delivery_min` is computed from 2 non-null values**

`avg_delivery_min = 29.0` equals `(28.1 + 29.8) / 2`, computed from 2 orders (excluding the null). Reporting `n_orders = 3` alongside an average derived from 2 values is potentially confusing. Consider adding a note in the description or adding an `n_valid` column, or adjusting `n_orders` to reflect the count used for the average.

**4. ds_ab_test_results / description: "approximately 10% lift" vs actual 9.8%**

The glossary teaching blocks say "same 10% lift" while the data shows 9.8%. The asset description hedges with "approximately 10% lift," which is acceptable, but the slight mismatch could cause confusion in assessment items that reference "10% lift" literally. Minor; no fix required.

---

## Assets Verified

| Asset | Rows | Columns | Internal Consistency | Glossary Alignment |
|---|---|---|---|---|
| ds_ab_test_results | 6 | 10 | FAIL (test_prop_B) | FAIL (f3 violated) |
| ds_ab_test_results_messy (variant) | — | — | OK (planted issues valid) | OK |
| ds_city_delivery_summary | 3 | 7 | OK | OK |
| ds_city_delivery_summary_messy (variant) | — | — | OK (planted issues valid) | OK |
| ds_capstone_orders | 12 | 6 | OK | OK |
| ds_capstone_drivers | 6 | 4 | OK (FK match) | OK |
| ds_capstone_zone_summary | 4 | 6 | FAIL (Lagos-South pct_on_time) | Partial |

---

VERDICT: FAIL

BLOCKING ds_ab_test_results/test_prop_B row: null_value_in_ci is "no" but 0.333 falls inside CI [0.15, 0.41]; glossary fact f3 requires the entire interval below 0.333 → Change to conversions=10, conversion_rate=0.20, p_value=0.046, ci_lower=0.09, ci_upper=0.31 (keeping null_value_in_ci="no")
BLOCKING ds_capstone_zone_summary/Lagos-South row: pct_on_time is 33.3 but zero Lagos-South orders meet the 25-min target (28.1 and 29.8 both exceed it) → Change pct_on_time from 33.3 to 0.0
ADVISORY ds_capstone_zone_summary/Lagos-South row: n_orders=3 but avg_delivery_min computed from only 2 non-null values; consider clarifying or adding n_valid column
ADVISORY ds_ab_test_results/description: "approximately 10% lift" vs glossary's "same 10% lift" when actual data shows 9.8%; minor wording gap
