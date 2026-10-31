#!/usr/bin/env python3
"""Patch interactions.part.c3.json per repair-round findings."""
import json, copy, re

path = "batches/final_batch_006_da_sql_rest/interactions.part.c3.json"
with open(path) as f:
    data = json.load(f)

def find_interaction(tile_id, step_id):
    for tile in data["tiles"]:
        if tile["tile_id"] == tile_id:
            for item in tile["interactions"]:
                if item["step_id"] == step_id:
                    return item["interaction"]
    raise KeyError(f"{tile_id}/{step_id} not found")

# ─────────────────────────────────────────────────────────────────────────────
# BLOCKING: tile_sql_adv_joining_tables/s07
# opt_d is currently a row-value comparison which is valid in DuckDB → two
# defensible answers.  Replace with the crossed-columns distractor the
# evaluator named, and update its feedback.  Also tighten the prompt to
# explicitly ask for the AND-based form.
# ─────────────────────────────────────────────────────────────────────────────
ix_s07 = find_interaction("tile_sql_adv_joining_tables", "tile_sql_adv_joining_tables.s07")

# Tighten prompt to ask for the AND-based form explicitly
ix_s07["public"]["prompt"] = (
    "You are joining `order_items` to `shipments`. A row should only match "
    "when **both** `order_id` and `product_id` are equal. "
    "Which ON clause correctly expresses this two-column condition "
    "using `AND`?"
)

# Replace opt_d text with the crossed-columns distractor
for opt in ix_s07["public"]["options"]:
    if opt["option_id"] == "opt_d":
        opt["text"] = (
            "ON order_items.order_id = shipments.product_id "
            "AND order_items.product_id = shipments.order_id"
        )
        break

# Update opt_d feedback to explain why the crossed version is wrong
ix_s07["grading"]["option_feedback"]["opt_d"] = {
    "message": (
        "The columns are crossed: order_id is compared to product_id and "
        "vice versa. Each column must be matched to its counterpart: "
        "order_id = order_id AND product_id = product_id."
    )
}

# ─────────────────────────────────────────────────────────────────────────────
# ADVISORY: tile_sql_adv_joining_tables/s04
# "How many customer rows appear in the result" → "How many distinct customers
# appear in the result"
# ─────────────────────────────────────────────────────────────────────────────
ix_s04 = find_interaction("tile_sql_adv_joining_tables", "tile_sql_adv_joining_tables.s04")
ix_s04["public"]["prompt"] = ix_s04["public"]["prompt"].replace(
    "How many customer rows appear in the result",
    "How many distinct customers appear in the result"
)

# ─────────────────────────────────────────────────────────────────────────────
# ADVISORY: tile_sql_adv_joining_tables/s13
# Tighten prompt: "Which join type achieves this without adding extra rows for
# unmatched orders?"
# ─────────────────────────────────────────────────────────────────────────────
ix_s13 = find_interaction("tile_sql_adv_joining_tables", "tile_sql_adv_joining_tables.s13")
ix_s13["public"]["prompt"] = (
    "You want a result that lists **every customer**, including those with no "
    "orders, with `NULL` in the order columns for customers who have not "
    "ordered. Which join type achieves this without adding extra rows for "
    "unmatched orders, when customers is the left table?"
)

# ─────────────────────────────────────────────────────────────────────────────
# ADVISORY: tile_sql_adv_execution_order_subquery_where/s09
# The advisory asks for a hidden check via spec.mount_variants to catch the
# shortcut WHERE city = 'Lagos' on the orders table.  The only available
# customers variant (ds_customers_messy) changes customer 2's city to 'kano'
# but leaves customer 1 in Lagos, so it would not catch the shortcut.
# No suitable registry variant exists; this advisory cannot be implemented
# without adding a new variant to the registry (which is out of scope here).
# Skipping this advisory item.
# ─────────────────────────────────────────────────────────────────────────────

with open(path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print("Patch applied successfully.")
