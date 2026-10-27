# Scoped Re-evaluation — Stage 03 screens

**Batch:** `final_batch_005_da_sql_canary`  
**Tiles:** `tile_sql_fund_relational_select`, `tile_sql_fund_alias_distinct`  
**Scope:** Verify repairs for four prior findings; check nothing else broke.

---

## Finding 1 (was BLOCKING): tile_sql_fund_alias_distinct/r03.b1 — "three distinct cities" vs four

**Status: FIXED ✓**

The repaired text at `tile_sql_fund_alias_distinct.r03.b1` now reads:

> "The customers table has eight rows with four distinct cities: Lagos (3 customers), Abuja (2), Kano (2), Port Harcourt (1). SELECT city FROM customers returns eight rows; SELECT DISTINCT city FROM customers returns four."

Verified against `scenario_asset_registry.json` (`ds.customers`): 8 rows, 4 distinct cities with exactly those counts. Correct.

## Finding 2 (was ADVISORY): tile_sql_fund_alias_distinct/s08 lineage missing fact_ids

**Status: FIXED ✓**

Step `s08` and block `s08.b1` lineage now include `sql.distinct#f1`, `sql.distinct#f2`, and `sql.aliasing#f2`. Step-level and block-level lineages are consistent for this step.

## Finding 3 (was ADVISORY): tile_sql_fund_relational_select/s01.b1 lineage missing f5

**Status: PARTIALLY FIXED**

Block `s01.b1` lineage now includes `sql.relational_model#f5`. However, the step-level lineage for `s01` was **not** updated to include `f5`, creating a block-vs-step lineage inconsistency. (New ADVISORY below.)

## Finding 4 (was ADVISORY, no change required): tile_sql_fund_alias_distinct/s01 lede framing

**Status: UNCHANGED (as expected) ✓**

---

## New findings from repair

**ADVISORY** `tile_sql_fund_relational_select/s01 step lineage`: `sql.relational_model#f5` is present in block `s01.b1` lineage but absent from the step-level `fact_ids`. Step lineage should be a superset of its blocks' lineages. → Add `sql.relational_model#f5` to the step-level `lineage.fact_ids` array.

---

## Collateral-damage check

- JSON validity: ✓
- Tile count (2), step counts (10 + 8), block counts: unchanged from expected structure.
- Full scan of all step-vs-block lineage consistency: only the one issue above.
- No other text changes detected outside the four repaired locations.

---

VERDICT: PASS

ADVISORY tile_sql_fund_relational_select/s01 step lineage: sql.relational_model#f5 present in block s01.b1 lineage but missing from step-level fact_ids → add "sql.relational_model#f5" to the step-level lineage.fact_ids array
