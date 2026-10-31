"""
Repair patch for interactions.part.c2.json and screens.json:

1. Fix tile_sql_text_dates_casts.s06 solution: change `order_date - '2024-01-01'`
   to `order_date - DATE '2024-01-01'` (DuckDB cannot subtract STRING_LITERAL from DATE).
   Also fix the prompt and starter comment to use the correct syntax.

2. Fix tile_sql_null_fallback_and_union.s01/data_table highlight: add missing `row`
   field to the cell highlight in screens.json.
"""
import json
import copy

# ── Fix 1: interactions.part.c2.json ──────────────────────────────────────────
with open("batches/final_batch_006_da_sql_rest/interactions.part.c2.json") as f:
    ixdata = json.load(f)

for tile in ixdata["tiles"]:
    if tile["tile_id"] == "tile_sql_text_dates_casts":
        for item in tile["interactions"]:
            if item["step_id"] == "tile_sql_text_dates_casts.s06":
                ix = item["interaction"]

                # Fix solution: replace string literal with DATE literal
                sol = ix["grading"]["solution_files"][0]
                sol["content"] = sol["content"].replace(
                    "order_date - '2024-01-01'",
                    "order_date - DATE '2024-01-01'"
                )

                # Fix prompt: update the hint in the prompt text
                ix["public"]["prompt"] = ix["public"]["prompt"].replace(
                    "use `order_date - '2024-01-01'`",
                    "use `order_date - DATE '2024-01-01'`"
                )

                # Fix starter file comment
                for wf in ix["public"]["workspace"]["files"]:
                    if wf["path"] == "query.sql":
                        wf["content"] = wf["content"].replace(
                            "order_date - '2024-01-01'",
                            "order_date - DATE '2024-01-01'"
                        )

                print("Fixed tile_sql_text_dates_casts.s06 solution and prompt")
                break

with open("batches/final_batch_006_da_sql_rest/interactions.part.c2.json", "w") as f:
    json.dump(ixdata, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("Wrote interactions.part.c2.json")

# ── Fix 2: screens.json ────────────────────────────────────────────────────────
with open("batches/final_batch_006_da_sql_rest/screens.json") as f:
    scdata = json.load(f)

for tile in scdata["tiles"]:
    if tile["tile_id"] == "tile_sql_null_fallback_and_union":
        for step in tile["steps"]:
            if step["step_id"] == "tile_sql_null_fallback_and_union.s01":
                for block in step.get("blocks", []):
                    if block.get("type") == "before_after":
                        before = block.get("before", {})
                        for h in before.get("highlight", []):
                            tg = h.get("target", {})
                            if tg.get("kind") == "cell" and "row" not in tg:
                                tg["row"] = {"where": {"customer_id": 4}}
                                print("Fixed tile_sql_null_fallback_and_union.s01 dt_before highlight: added row")

with open("batches/final_batch_006_da_sql_rest/screens.json", "w") as f:
    json.dump(scdata, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("Wrote screens.json")
