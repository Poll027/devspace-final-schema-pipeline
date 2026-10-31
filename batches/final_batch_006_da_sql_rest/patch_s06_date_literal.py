#!/usr/bin/env python3
"""
Patch interactions.part.c2.json:
  - Fix tile_sql_text_dates_casts.s06 solution: change `order_date - '2024-01-01'`
    to `order_date - DATE '2024-01-01'` so DuckDB can resolve the subtraction.
  - Update prompt, hints, and message_on_fail to match.
"""
import json, re

path = "batches/final_batch_006_da_sql_rest/interactions.part.c2.json"

with open(path) as f:
    data = json.load(f)

# Find the tile and step
for tile in data["tiles"]:
    if tile["tile_id"] == "tile_sql_text_dates_casts":
        for item in tile["interactions"]:
            if item["step_id"] == "tile_sql_text_dates_casts.s06":
                ix = item["interaction"]

                # 1. Fix solution_files content
                for sf in ix["grading"]["solution_files"]:
                    if sf["path"] == "query.sql":
                        sf["content"] = sf["content"].replace(
                            "order_date - '2024-01-01'",
                            "order_date - DATE '2024-01-01'"
                        )
                        print("Fixed solution_files content:", repr(sf["content"]))

                # 2. Fix prompt
                ix["public"]["prompt"] = ix["public"]["prompt"].replace(
                    "order_date - '2024-01-01'",
                    "order_date - DATE '2024-01-01'"
                )
                print("Fixed prompt")

                # 3. Fix hints
                for i, hint in enumerate(ix["feedback"]["hints"]):
                    if "'2024-01-01'" in hint:
                        ix["feedback"]["hints"][i] = hint.replace(
                            "order_date - '2024-01-01'",
                            "order_date - DATE '2024-01-01'"
                        )
                        print(f"Fixed hint {i}")

                # 4. Fix message_on_fail in tests
                for test in ix["grading"]["tests"]:
                    if "message_on_fail" in test and "'2024-01-01'" in test["message_on_fail"]:
                        test["message_on_fail"] = test["message_on_fail"].replace(
                            "order_date - '2024-01-01'",
                            "order_date - DATE '2024-01-01'"
                        )
                        print("Fixed message_on_fail")

                # 5. Fix incorrect feedback message
                if "'2024-01-01'" in ix["feedback"]["incorrect"]["message"]:
                    ix["feedback"]["incorrect"]["message"] = ix["feedback"]["incorrect"]["message"].replace(
                        "order_date - '2024-01-01'",
                        "order_date - DATE '2024-01-01'"
                    )
                    print("Fixed incorrect feedback message")

                print("Done patching s06")
                break

with open(path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print("Written:", path)
