# Evaluation — 04_interactions — c0_canary (scoped re-evaluation)

**Artifact:** `interactions.part.c0_canary.json`  
**Tile scope:** `tile_sql_fund_filtering_rows`  
**Type:** Scoped re-evaluation after repair attempt

## Repair check

The original BLOCKING finding reported that `s13` (IS NULL / IS NOT NULL code exercise) asks the learner to write two queries but only tests statement 1 (IS NOT NULL). The repair was supposed to add a second test (`t_is_null`) for statement 0 (IS NULL).

**Result: The repair was NOT applied.** The `tests` array in `s13` still contains only one test (`t_is_not_null`, targeting `statement: 1`). No test exists for statement 0. A learner can submit an empty or incorrect first query and still pass the exercise.

## No other regressions detected

The rest of the artifact is unchanged from the prior evaluation. All 8 interactions are present and structurally intact.

---

VERDICT: FAIL

BLOCKING tile_sql_fund_filtering_rows/s13: The exercise asks for two queries (IS NULL and IS NOT NULL) but only tests IS NOT NULL (statement 1). No test exists for the IS NULL query (statement 0). A learner could write an incorrect or empty first query and still pass. → Add a second test with `"test_id": "t_is_null"`, `"kind": "query_result_equals"`, `"spec": {"statement": 0, "expected": {"columns": ["order_id", "delivery_time_minutes"], "rows": [[1011, null], [1012, null]]}, "ordered": false}`, `"visible": true`, `"message_on_fail": "Your first query should return exactly the 2 orders where delivery_time_minutes IS NULL. Use IS NULL."`.
