#!/usr/bin/env python3
"""Patch interactions.json: fix s04 prompt and feedback to include customer 6."""
import json

SRC = "batches/final_batch_006_da_sql_rest/interactions.json"

with open(SRC) as f:
    data = json.load(f)

patched = False
for tile in data["tiles"]:
    if tile["tile_id"] != "tile_sql_adv_joining_tables":
        continue
    for ix in tile["interactions"]:
        if ix["step_id"] != "tile_sql_adv_joining_tables.s04":
            continue
        interaction = ix["interaction"]

        # Fix prompt
        old_prompt = interaction["public"]["prompt"]
        new_prompt = old_prompt.replace(
            "customer_id 1, 2, 3, 4, and 5",
            "customer_id 1, 2, 3, 4, 5, and 6"
        )
        assert new_prompt != old_prompt, "Prompt not changed!"
        interaction["public"]["prompt"] = new_prompt

        # Fix opt_a feedback
        old_a = interaction["grading"]["option_feedback"]["opt_a"]["message"]
        new_a = old_a.replace(
            "Customers 4 and 5 have no orders, so they are excluded.",
            "Customers 4, 5, and 6 have no orders, so they are excluded."
        )
        assert new_a != old_a, "opt_a feedback not changed!"
        interaction["grading"]["option_feedback"]["opt_a"]["message"] = new_a

        # Fix opt_b feedback
        old_b = interaction["grading"]["option_feedback"]["opt_b"]["message"]
        new_b = old_b.replace(
            "Customers 4 and 5 have no matching order rows, so they are dropped.",
            "Customers 4, 5, and 6 have no matching order rows, so they are dropped."
        )
        assert new_b != old_b, "opt_b feedback not changed!"
        interaction["grading"]["option_feedback"]["opt_b"]["message"] = new_b

        patched = True
        print("Patched s04 in interactions.json.")

assert patched, "s04 not found in interactions.json!"

with open(SRC, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print("Done.")
