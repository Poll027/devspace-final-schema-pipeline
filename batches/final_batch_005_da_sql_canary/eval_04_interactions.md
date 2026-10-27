# Stage 04 Interactions — Scoped Re-evaluation Report

**Batch:** `final_batch_005_da_sql_canary`  
**Tiles:** `tile_sql_fund_relational_select`, `tile_sql_fund_alias_distinct`  
**Scope:** Scoped re-evaluation after repair of one BLOCKING and one ADVISORY finding on `tile_sql_fund_alias_distinct/s04`.

---

## Repair Check: BLOCKING tile_sql_fund_alias_distinct/s04

**Original finding:** No test enforced use of a table alias or alias-qualified column references; a query like `SELECT order_id, customer_id, delivery_time_minutes AS delivery_min FROM orders` (no alias) would pass all tests, violating the practice anchor's success sentence.

**Repair applied:** A new hidden test `test_aliasing_requires_table_alias` was added with `kind: "required_syntax"` and descriptors `["table alias (FROM table AS alias)", "alias.column qualification"]`.

**Verification:**
- The test is present in both `interactions.json` (lines 751–761) and the lesson file (`tile_sql_fund_alias_distinct.json`), with identical content.
- The descriptors `"table alias (FROM table AS alias)"` and `"alias.column qualification"` match entries in the `allowed_syntax` list, confirming they are recognized syntax descriptors.
- The reference solution `SELECT o.order_id, o.customer_id, o.delivery_time_minutes AS delivery_min FROM orders AS o` satisfies both required descriptors.
- Execution provenance in the lesson file confirms `tests_passed: 3` (all three tests pass with the solution).
- A lazy shortcut query without alias (`SELECT order_id, customer_id, delivery_time_minutes AS delivery_min FROM orders`) would now fail the `required_syntax` test because it lacks both a table alias and alias-qualified column references.
- The practice anchor success sentence ("every column reference uses the alias rather than the original table name, and the renamed output column appears under its new label") is now enforced.

**Status: RESOLVED** ✓

---

## Repair Check: ADVISORY tile_sql_fund_alias_distinct/s04

**Original finding:** Hidden test `test_aliasing_no_distinct` only forbids DISTINCT, which is tangential to the aliasing objective; renaming or adding a positive alias test would improve clarity.

**Status:** The test name was slightly updated to `test_aliasing_no_distinct_keyword` (cosmetic). The substantive improvement (adding a positive alias-requiring test) was achieved via the new `test_aliasing_requires_table_alias` test. The DISTINCT-forbidding test remains as a secondary guard, which is acceptable. Advisory-only; no action required.

---

## Collateral Damage Check

- All other interactions in both tiles are unchanged and structurally intact.
- `tile_sql_fund_relational_select`: 4 interactions (s03, s04, s08, s09) — no changes detected.
- `tile_sql_fund_alias_distinct`: 4 interactions (s03, s04, s06, s07) — only s04 was modified (new test added).
- Test counts, solution files, and grading structures are consistent between `interactions.json` and the lesson files.

---

## Remaining Advisories

ADVISORY tile_sql_fund_alias_distinct/s04: The hidden test `test_aliasing_no_distinct_keyword` still only forbids DISTINCT, which is tangential to the aliasing objective. Now that `test_aliasing_requires_table_alias` positively enforces alias usage, this is purely cosmetic.

---

VERDICT: PASS

ADVISORY tile_sql_fund_alias_distinct/s04: `test_aliasing_no_distinct_keyword` forbids DISTINCT but is tangential to the aliasing objective; consider renaming to clarify its guard purpose (e.g., `test_aliasing_no_future_syntax`) -> No change required; cosmetic only.
