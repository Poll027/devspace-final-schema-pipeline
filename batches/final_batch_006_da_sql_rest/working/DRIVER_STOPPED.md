# STOPPED final_batch_006_da_sql_rest

04_interactions:c0_canary the same blocking defects came back unchanged after a repair (check whether the finding is a false positive):
BLOCKING `tile_sql_fund_filtering_rows/s13`: The exercise asks for two queries (IS NULL and IS NOT NULL) but only tests IS NOT NULL (statement 1). No test exists for the IS NULL query (statement 0). A learner could write an incorrect or empty first query and still pass. → Add a second test with `"test_id": "t_is_null"`, `"kind": "query_result_equals"`, `"spec": {"statement": 0, "expected": {"columns": ["order_id", "delivery_time_minutes"], "rows": [[1011, null], [1012, null]]}, "ordered": false}`, `"visible": true`, `"message_on_fail": "Your first query should return exactly the 2 orders where delivery_time_minutes IS NULL. Use IS NULL."`.

Spend so far $27.50. Fix the cause, then rerun the same command (finished stages are skipped).
