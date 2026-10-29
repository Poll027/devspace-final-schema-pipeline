#!/usr/bin/env python3
"""
Patch s13: swap query order so statement 0 is IS NOT NULL (data-dependent)
and statement 1 is IS NULL. This ensures statement 0's result changes when
any non-NULL row is mutated (drop/duplicate/change cell).
"""
import json, copy

INPUT  = 'batches/final_batch_006_da_sql_rest/interactions.part.c0_canary.json'
OUTPUT = INPUT  # patch in place

with open(INPUT) as f:
    data = json.load(f)

# Locate s13
s13 = None
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_sql_fund_filtering_rows':
        for item in tile['interactions']:
            if item['step_id'] == 'tile_sql_fund_filtering_rows.s13':
                s13 = item['interaction']
                break
        break

assert s13 is not None, "s13 not found"

# 1. Update prompt: IS NOT NULL first, IS NULL second
s13['public']['prompt'] = (
    "Write **two queries** in the file below, in this order:\n\n"
    "1. A query that returns `order_id` and `delivery_time_minutes` for every order "
    "where `delivery_time_minutes` **IS NOT NULL** (the delivery time is present).\n\n"
    "2. A query that returns `order_id` and `delivery_time_minutes` for every order "
    "where `delivery_time_minutes` **IS NULL** (the delivery time is missing).\n\n"
    "Do not use `= NULL` in either query. Each query must return exactly two columns: "
    "`order_id` and `delivery_time_minutes`."
)

# 2. Update starter file: IS NOT NULL first, IS NULL second
s13['public']['workspace']['files'][0]['content'] = (
    "-- Query 1: orders where delivery_time_minutes IS NOT NULL\n"
    "-- Write your first SELECT ... FROM ... WHERE ... query here.\n"
    "\n\n"
    "-- Query 2: orders where delivery_time_minutes IS NULL\n"
    "-- Write your second SELECT ... FROM ... WHERE ... query here.\n"
)

# 3. Update solution: IS NOT NULL first, IS NULL second
s13['grading']['solution_files'][0]['content'] = (
    "SELECT order_id, delivery_time_minutes FROM orders WHERE delivery_time_minutes IS NOT NULL;\n"
    "\n"
    "SELECT order_id, delivery_time_minutes FROM orders WHERE delivery_time_minutes IS NULL;\n"
)

# 4. Update tests: swap statement indices and expected rows
# Statement 0 = IS NOT NULL (11 rows with actual values)
# Statement 1 = IS NULL (2 rows with NULLs)

is_not_null_rows = [
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
    [1013, 72],
]

is_null_rows = [
    [1011, None],
    [1012, None],
]

columns = ["order_id", "delivery_time_minutes"]

s13['grading']['tests'] = [
    {
        "test_id": "t_is_not_null",
        "kind": "query_result_equals",
        "spec": {
            "statement": 0,
            "expected": {
                "columns": columns,
                "rows": is_not_null_rows
            },
            "ordered": False
        },
        "visible": True,
        "message_on_fail": (
            "Your first query should return exactly the 11 orders where "
            "delivery_time_minutes IS NOT NULL. Use IS NOT NULL."
        )
    },
    {
        "test_id": "t_is_null",
        "kind": "query_result_equals",
        "spec": {
            "statement": 1,
            "expected": {
                "columns": columns,
                "rows": is_null_rows
            },
            "ordered": False
        },
        "visible": True,
        "message_on_fail": (
            "Your second query should return exactly the 2 orders where "
            "delivery_time_minutes IS NULL. Use IS NULL."
        )
    }
]

# 5. Update feedback messages to match new order
s13['feedback']['correct']['message'] = (
    "Well done. IS NOT NULL finds the rows with a present delivery time, "
    "and IS NULL finds the rest. Together they cover the whole table."
)
s13['feedback']['incorrect']['message'] = (
    "Check both queries. Use IS NOT NULL for the first query and IS NULL for the second. "
    "Do not use = NULL \u2014 it never matches."
)
s13['feedback']['hints'] = [
    "The first query uses WHERE delivery_time_minutes IS NOT NULL. "
    "The second uses WHERE delivery_time_minutes IS NULL.",
    "Make sure you write two separate SELECT statements, one for each condition."
]

with open(OUTPUT, 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')

print("Patch applied successfully.")
