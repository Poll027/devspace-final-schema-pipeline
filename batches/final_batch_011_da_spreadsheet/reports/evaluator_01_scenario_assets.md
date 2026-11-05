# Stage 01 – Scenario Asset Registry – Evaluator Report

**Batch:** `final_batch_011_da_spreadsheet`  
**Artifact:** `scenario_asset_registry.json`

---

## Evaluation Summary

Checked every asset against the glossary bundle's teaching blocks, required facts, assessment anchors, and practice anchors. Verified column-to-letter mappings, formula examples, planted issues, chart-source datasets, and cross-asset consistency.

---

## Defects

### BLOCKING

**1. asset_orders_clean / column order (F ↔ G swap)**

The glossary teaching blocks consistently place `driver_id` in column F and `order_date` in column G of the Orders sheet:

- Bundle 19 (vlookup_xlookup) tb1: "your Orders sheet records a driver ID in column F"
- Bundle 19 tb2: `=VLOOKUP(F2,Drivers!A:B,2,FALSE)` — F2 must be driver_id
- Bundle 19 tb4: `=XLOOKUP(F2,Drivers!A:A,Drivers!B:B)` — F2 must be driver_id
- Bundle 20 (index_match) tb4: "with an order's driver ID in F2, =INDEX(Drivers!A:A,MATCH(F2,Drivers!B:B,0))"
- Bundle 17 (date_functions) tb4: "with an order date in G2, =DATEDIF(G2,TODAY(),\"D\")"

The registry defines the columns as:
```
A: order_id, B: city, C: delivery_minutes, D: amount, E: status, F: order_date, G: driver_id
```

Column F is `order_date` and column G is `driver_id` — the reverse of what every formula example requires. All four lookup/date formulas in the glossary_example_vocab would operate on the wrong column.

**Fix:** In `asset_orders_clean` (and its messy variant), swap the column definitions and corresponding row-value positions so that `driver_id` is at index 5 (column F) and `order_date` is at index 6 (column G). Apply the same swap to `asset_orders_location_combined`, which shares the same trailing column order.

---

### ADVISORY

**2. asset_orders_clean / description ("COUNT and COUNTA differ")**

The description states: "delivery_minutes is NULL for Pending/Cancelled rows so COUNT and COUNTA differ." In the clean dataset, delivery_minutes contains only integers and nulls (empty cells). Both COUNT and COUNTA skip empty cells, so they return the same value (13) on this column. The claim would only hold if some cells contained text. The teaching text itself is correct (it explains the general difference); only the asset description is misleading.

**3. Teaching-block ranges vs dataset size**

Teaching blocks reference ranges like `D2:D51` and `C2:C51` (50 data rows), but the dataset has 20 rows. The formulas still work correctly (aggregation functions ignore empty cells), so this is not a data-integrity issue, but the mismatch may confuse exercise authors who expect the range to match the row count.

---

## Verdict

VERDICT: FAIL

BLOCKING asset_orders_clean/column-order: driver_id is at index 6 (col G) and order_date at index 5 (col F), but glossary teaching blocks place driver_id in F and order_date in G; every lookup and DATEDIF formula example references the wrong column → swap the column definitions and row-value positions for driver_id (move to index 5 / col F) and order_date (move to index 6 / col G) in asset_orders_clean, its messy variant, and asset_orders_location_combined.
ADVISORY asset_orders_clean/description: description claims "COUNT and COUNTA differ" on delivery_minutes, but with only integers and nulls they return the same value → remove or qualify the claim (e.g., note that a text entry would be needed for them to differ).
ADVISORY asset_orders_clean/range-size: teaching-block ranges (D2:D51) span 50 rows but dataset has 20 rows → consider noting the mismatch or adjusting the dataset title/description.
