"""
Repair round 2 patch:
1. tile_sql_text_dates_casts.s06: change solution (and prompt/starter) to use
   '2024-01-01' instead of DATE '2024-01-01' so sqlglot does not detect CAST.
2. tile_sql_null_fallback_and_union.s01/data_table (in screens.part.c2.json):
   add a `row` field to the cell highlight target so the checker is satisfied.
"""
import json, copy

# ── Fix 1: interactions.part.c2.json ─────────────────────────────────────────
with open("batches/final_batch_006_da_sql_rest/interactions.part.c2.json") as f:
    ix_data = json.load(f)

for tile in ix_data["tiles"]:
    if tile["tile_id"] != "tile_sql_text_dates_casts":
        continue
    for entry in tile["interactions"]:
        if entry["step_id"] != "tile_sql_text_dates_casts.s06":
            continue
        ix = entry["interaction"]

        # Update prompt: replace DATE '2024-01-01' with '2024-01-01'
        ix["public"]["prompt"] = ix["public"]["prompt"].replace(
            "DATE '2024-01-01'", "'2024-01-01'"
        )

        # Update starter comment
        for f in ix["public"]["workspace"]["files"]:
            if f["path"] == "query.sql":
                f["content"] = f["content"].replace(
                    "DATE '2024-01-01'", "'2024-01-01'"
                )

        # Update solution
        for sf in ix["grading"]["solution_files"]:
            if sf["path"] == "query.sql":
                sf["content"] = sf["content"].replace(
                    "DATE '2024-01-01'", "'2024-01-01'"
                )

        print("Fixed tile_sql_text_dates_casts.s06 solution/prompt/starter")
        break

with open("batches/final_batch_006_da_sql_rest/interactions.part.c2.json", "w") as f:
    json.dump(ix_data, f, indent=2)
print("Wrote interactions.part.c2.json")

# ── Fix 2: screens.part.c2.json ──────────────────────────────────────────────
with open("batches/final_batch_006_da_sql_rest/screens.part.c2.json") as f:
    sc_data = json.load(f)

fixed = False
for tile in sc_data["tiles"]:
    if tile["tile_id"] != "tile_sql_null_fallback_and_union":
        continue
    for step in tile["steps"]:
        if step["step_id"] != "tile_sql_null_fallback_and_union.s01":
            continue
        for block in step.get("blocks", []):
            if block.get("type") != "before_after":
                continue
            before = block.get("before", {})
            if before.get("type") != "data_table":
                continue
            for h in before.get("highlight", []):
                tg = h.get("target", {})
                if tg.get("kind") == "cell" and "row" not in tg:
                    # Add row pointing to customer 4 (first row with NULL city)
                    tg["row"] = {"where": {"customer_id": 4}}
                    fixed = True
                    print("Fixed tile_sql_null_fallback_and_union.s01 dt_before cell highlight: added row")

with open("batches/final_batch_006_da_sql_rest/screens.part.c2.json", "w") as f:
    json.dump(sc_data, f, indent=2)
print("Wrote screens.part.c2.json")

if not fixed:
    print("WARNING: did not find the cell highlight to fix in screens.part.c2.json")
