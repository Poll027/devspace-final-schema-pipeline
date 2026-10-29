#!/usr/bin/env python3
"""Patch interactions.part.c0_canary.json per evaluator findings."""
import json, copy

SRC = "batches/final_batch_006_da_sql_rest/interactions.part.c0_canary.json"

with open(SRC) as f:
    data = json.load(f)

tile = data["tiles"][0]
interactions = tile["interactions"]

# Helper: find interaction by step_id
def find_ix(step_id):
    for item in interactions:
        if item["step_id"] == step_id:
            return item["interaction"]
    raise KeyError(step_id)

# ── ADVISORY s08: add "using explicit parentheses" to prompt ─────────────────
ix08 = find_ix("tile_sql_fund_filtering_rows.s08")
old_prompt = ix08["public"]["prompt"]
# Replace "Which WHERE clause correctly expresses this requirement?"
# with    "Which WHERE clause correctly expresses this requirement, using explicit parentheses?"
new_prompt = old_prompt.replace(
    "Which WHERE clause correctly expresses this requirement?",
    "Which WHERE clause correctly expresses this requirement, using explicit parentheses?"
)
assert new_prompt != old_prompt, "s08 prompt replacement failed"
ix08["public"]["prompt"] = new_prompt

# ── BLOCKING s09: fix solution and expected rows ──────────────────────────────
ix09 = find_ix("tile_sql_fund_filtering_rows.s09")

# Fix solution
ix09["grading"]["solution_files"][0]["content"] = (
    "SELECT order_id, customer_id, delivery_time_minutes "
    "FROM orders WHERE (customer_id = 1 AND delivery_time_minutes > 30) OR region = 'north'\n"
)

# Fix expected rows (8 rows as specified by evaluator)
ix09["grading"]["tests"][0]["spec"]["expected"]["rows"] = [
    [1002, 2, 22],
    [1003, 1, 41],
    [1005, 2, 35],
    [1006, 1, 63],
    [1008, 2, 55],
    [1009, 1, 31],
    [1011, 2, None],
    [1013, 1, 72]
]

# ── BLOCKING s13: add t_is_null test for statement 1 ─────────────────────────
ix13 = find_ix("tile_sql_fund_filtering_rows.s13")

t_is_null = {
    "test_id": "t_is_null",
    "kind": "query_result_equals",
    "spec": {
        "statement": 1,
        "expected": {
            "columns": ["order_id", "delivery_time_minutes"],
            "rows": [
                [1011, None],
                [1012, None]
            ]
        },
        "ordered": False
    },
    "visible": True,
    "message_on_fail": "Your second query should return exactly the 2 orders where delivery_time_minutes IS NULL. Use IS NULL."
}

ix13["grading"]["tests"].append(t_is_null)

with open(SRC, "w") as f:
    json.dump(data, f, indent=2)

print("Patch applied successfully.")
print(f"  s08 prompt updated: {'using explicit parentheses' in ix08['public']['prompt']}")
print(f"  s09 solution: {ix09['grading']['solution_files'][0]['content'].strip()}")
print(f"  s09 expected rows count: {len(ix09['grading']['tests'][0]['spec']['expected']['rows'])}")
print(f"  s13 tests count: {len(ix13['grading']['tests'])}")
