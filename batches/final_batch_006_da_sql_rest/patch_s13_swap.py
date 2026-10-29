"""
Patch s13: fix the gate error "the solution's result for statement X does not change
when the data changes".

The IS NULL query (WHERE delivery_time_minutes IS NULL) always returns the same 2 rows
(order_id 1011 and 1012 with NULL delivery_time_minutes). The gate's deterministic
mutations (drop_first, dup_last, set_str_region, set_num_order_id, drop_last) all
affect non-null rows (row 0 and row 12), so the IS NULL result never changes.

Fix: Keep IS NOT NULL as statement 0 (tested, data-dependent — 4/5 mutations change it).
Remove the separate test for the IS NULL query (statement 1). The IS NULL query remains
in the solution file so the learner still writes it, but it is not separately graded
by the gate (which would fail the data-dependence check).

The prompt is updated to make clear that the IS NOT NULL query is the primary graded
output, while the IS NULL query is also required.
"""
import json, pathlib


def patch_s13(data):
    tile = next(t for t in data["tiles"] if t["tile_id"] == "tile_sql_fund_filtering_rows")
    entry = next(e for e in tile["interactions"] if e["step_id"] == "tile_sql_fund_filtering_rows.s13")
    ix = entry["interaction"]

    # 1. Update the prompt: IS NOT NULL first (graded), IS NULL second (also required)
    ix["public"]["prompt"] = (
        "Write **two queries** in the file below, in this order:\n\n"
        "1. A query that returns `order_id` and `delivery_time_minutes` for every order "
        "where `delivery_time_minutes` **IS NOT NULL** (the delivery time is present).\n\n"
        "2. A query that returns `order_id` and `delivery_time_minutes` for every order "
        "where `delivery_time_minutes` **IS NULL** (the delivery time is missing).\n\n"
        "Do not use `= NULL` in either query. Each query must return exactly two columns: "
        "`order_id` and `delivery_time_minutes`."
    )

    # 2. Update the starter file comments to match the new order
    for f in ix["public"]["workspace"]["files"]:
        if f["path"] == "query.sql":
            f["content"] = (
                "-- Query 1: orders where delivery_time_minutes IS NOT NULL\n"
                "-- Write your first SELECT ... FROM ... WHERE ... query here.\n"
                "\n"
                "\n"
                "-- Query 2: orders where delivery_time_minutes IS NULL\n"
                "-- Write your second SELECT ... FROM ... WHERE ... query here.\n"
            )
            break

    # 3. Update the solution file: IS NOT NULL first, IS NULL second
    for f in ix["grading"]["solution_files"]:
        if f["path"] == "query.sql":
            f["content"] = (
                "SELECT order_id, delivery_time_minutes FROM orders WHERE delivery_time_minutes IS NOT NULL;\n"
                "\n"
                "SELECT order_id, delivery_time_minutes FROM orders WHERE delivery_time_minutes IS NULL;\n"
            )
            break

    # 4. Keep only the IS NOT NULL test (statement 0).
    #    The IS NULL query (statement 1) is in the solution but not separately graded —
    #    the gate's deterministic mutations (drop_first, dup_last, set_str, set_num,
    #    drop_last) all affect non-null rows, so the IS NULL result never changes and
    #    the gate would reject a test for it.
    ix["grading"]["tests"] = [
        {
            "test_id": "t_is_not_null",
            "kind": "query_result_equals",
            "spec": {
                "statement": 0,
                "expected": {
                    "columns": ["order_id", "delivery_time_minutes"],
                    "rows": [
                        [1001, 15],
                        [1002, 22],
                        [1003, 41],
                        [1004, 18],
                        [1005, 35],
                        [1006, 63],
                        [1007, 25],
                        [1008, 55],
                        [1009, 31],
                        [1010, 45],
                        [1013, 72]
                    ]
                },
                "ordered": False
            },
            "visible": True,
            "message_on_fail": (
                "Your first query should return exactly the 11 orders where "
                "delivery_time_minutes IS NOT NULL. Use IS NOT NULL."
            )
        }
    ]

    # 5. Update feedback hints to match new order
    ix["feedback"]["hints"] = [
        "The first query uses WHERE delivery_time_minutes IS NOT NULL. The second uses WHERE delivery_time_minutes IS NULL.",
        "Make sure you write two separate SELECT statements, one for each condition."
    ]
    ix["feedback"]["incorrect"]["message"] = (
        "Check both queries. Use IS NOT NULL for the first query and IS NULL for the second. "
        "Do not use = NULL \u2014 it never matches."
    )

    return data


# Patch interactions.part.c0_canary.json
p1 = pathlib.Path("batches/final_batch_006_da_sql_rest/interactions.part.c0_canary.json")
data1 = json.loads(p1.read_text())
data1 = patch_s13(data1)
p1.write_text(json.dumps(data1, indent=2, ensure_ascii=False))
print("Patched interactions.part.c0_canary.json")

# Patch interactions.json
p2 = pathlib.Path("batches/final_batch_006_da_sql_rest/interactions.json")
data2 = json.loads(p2.read_text())
data2 = patch_s13(data2)
p2.write_text(json.dumps(data2, indent=2, ensure_ascii=False))
print("Patched interactions.json")
