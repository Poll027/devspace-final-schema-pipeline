"""
Update tile_lessons directly with the two fixes:
1. tile_sql_text_dates_casts.json: update s06 solution/prompt/starter
2. tile_sql_null_fallback_and_union.json: add row to cell highlight in s01
"""
import json

# ── Fix 1: tile_sql_text_dates_casts.json ────────────────────────────────────
with open("batches/final_batch_006_da_sql_rest/tile_lessons/tile_sql_text_dates_casts.json") as f:
    tl = json.load(f)

for step in tl["steps"]:
    if step["step_id"] != "tile_sql_text_dates_casts.s06":
        continue
    ix = step.get("interaction", {})
    if ix.get("type") != "code_exercise":
        continue

    # Update prompt
    old_prompt = ix["public"]["prompt"]
    new_prompt = old_prompt.replace("DATE '2024-01-01'", "'2024-01-01'")
    ix["public"]["prompt"] = new_prompt
    if old_prompt != new_prompt:
        print("Updated s06 prompt")

    # Update starter
    for f in ix["public"]["workspace"]["files"]:
        if f["path"] == "query.sql":
            old = f["content"]
            f["content"] = old.replace("DATE '2024-01-01'", "'2024-01-01'")
            if old != f["content"]:
                print("Updated s06 starter")

    # Update solution
    for sf in ix["grading"]["solution_files"]:
        if sf["path"] == "query.sql":
            old = sf["content"]
            sf["content"] = old.replace("DATE '2024-01-01'", "'2024-01-01'")
            if old != sf["content"]:
                print("Updated s06 solution")

    break

with open("batches/final_batch_006_da_sql_rest/tile_lessons/tile_sql_text_dates_casts.json", "w") as f:
    json.dump(tl, f, indent=2)
print("Wrote tile_sql_text_dates_casts.json")

# ── Fix 2: tile_sql_null_fallback_and_union.json ──────────────────────────────
with open("batches/final_batch_006_da_sql_rest/tile_lessons/tile_sql_null_fallback_and_union.json") as f:
    tl2 = json.load(f)

fixed = False
for step in tl2["steps"]:
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
                tg["row"] = {"where": {"customer_id": 4}}
                fixed = True
                print("Fixed s01 dt_before cell highlight: added row")
    break

with open("batches/final_batch_006_da_sql_rest/tile_lessons/tile_sql_null_fallback_and_union.json", "w") as f:
    json.dump(tl2, f, indent=2)
print("Wrote tile_sql_null_fallback_and_union.json")

if not fixed:
    print("WARNING: did not find cell highlight to fix in tile_sql_null_fallback_and_union.json")
