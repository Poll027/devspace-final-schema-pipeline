# Stage 03 Screens — Scoped Re-evaluation (c3)

**Batch:** final_batch_006_da_sql_rest
**Chunk:** c3 (tile_sql_adv_joining_tables, tile_sql_adv_execution_order_subquery_where, tile_sql_adv_subquery_from_cte)
**Scope:** Scoped re-evaluation after repair of 3 BLOCKING + 2 ADVISORY findings.

## Repair Verification

### BLOCKING 1 — tile_sql_adv_joining_tables/s01.b4: c3 node kind
**Original defect:** Node c3 (Fatima Aliyu, customer_id=3) was marked "matched" but had no matching edge.
**Repair status:** ✅ FIXED. Node c3 now has `"kind": "unmatched"` (line 96). No edge connects c3 to any order node. Alt_text correctly states both customer_id=3 and customer_id=4 are dropped. Diagram consistency verified: all "matched" nodes have edges, all "unmatched" nodes do not.

### BLOCKING 2 — tile_sql_adv_joining_tables/s06.b4: USING-form column qualification
**Original defect:** USING-form code qualified USING columns with table aliases, which is invalid in PostgreSQL.
**Repair status:** ✅ FIXED. USING-form SELECT now reads `SELECT order_id, product_id, s.shipped_date` — USING columns are unqualified, only the non-USING column `shipped_date` is qualified with `s.`. This is valid PostgreSQL.

### BLOCKING 3 — tile_sql_adv_subquery_from_cte/s10.b1: Recap alias wording
**Original defect:** Recap said alias "must" be given, dropping the hedge from fact sql.subquery_in_from#f1 ("may be given").
**Repair status:** ✅ FIXED. Text now reads: "A subquery in FROM must be wrapped in parentheses and should be given an alias (the SQL standard requires it, though PostgreSQL allows omission); the outer query reads its output columns by name." This is faithful to fact f1 which says "may be given a table alias" and "the SQL standard requires this alias, and while PostgreSQL allows it to be omitted, writing one is good practice."

### ADVISORY 1 — tile_sql_adv_joining_tables/s01.b4: Confusing edge from c4 to o1001
**Original defect:** Edge labeled "no match — dropped" was visually confusing.
**Repair status:** ✅ ADDRESSED. The edge was removed and replaced with a standalone annotation node `c4_note` explaining "customer_id=4 has no matching order — dropped from result."

### ADVISORY 2 — tile_sql_adv_subquery_from_cte/s01.b2: Opening sentence wording
**Original defect:** Said "must be … given a table alias" before qualifying.
**Repair status:** ✅ ADDRESSED. Now reads "is typically given a table alias" with the qualification about the SQL standard and PostgreSQL.

## Collateral Damage Check

No other content appears to have been altered outside the repaired areas. JSON structure is valid. All three tiles are present.

## Remaining Issues

**None blocking.**

ADVISORY tile_sql_adv_joining_tables/s01.b4: The annotation node `c4_note` mentions only customer_id=4 but not customer_id=3 (Fatima Aliyu), who is also unmatched. The alt_text correctly mentions both. Minor inconsistency, not misleading.

## Verdict

VERDICT: PASS
