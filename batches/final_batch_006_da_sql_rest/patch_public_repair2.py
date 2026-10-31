"""
Update tile_lessons_public with the same fixes as tile_lessons.
"""
import json

# ── Fix 1: tile_sql_text_dates_casts.json (public) ───────────────────────────
with open("batches/final_batch_006_da_sql_rest/tile_lessons_public/tile_sql_text_dates_casts.json") as f:
    tl = json.load(f)

for step in tl["steps"]:
    if step["step_id"] != "tile_sql_text_dates_casts.s06":
        continue
    ix = step.get("interaction", {})
    if ix.get("type") != "code_exercise":
        continue

    # Update prompt
    old = ix["public"]["prompt"]
    ix["public"]["prompt"] = old.replace("DATE '2024-01-01'", "'2024-01-01'")
    if old != ix["public"]["prompt"]:
        print("Updated public s06 prompt")

    # Update starter
    for f in ix["public"]["workspace"]["files"]:
        if f["path"] == "query.sql":
            old = f["content"]
            f["content"] = old.replace("DATE '2024-01-01'", "'2024-01-01'")
            if old != f["content"]:
                print("Updated public s06 starter")

    # Update solution (if present in public)
    gr = ix.get("grading", {})
    for sf in gr.get("solution_files", []):
        if sf["path"] == "query.sql":
            old = sf["content"]
            sf["content"] = old.replace("DATE '2024-01-01'", "'2024-01-01'")
            if old != sf["content"]:
                print("Updated public s06 solution")

    break

with open("batches/final_batch_006_da_sql_rest/tile_lessons_public/tile_sql_text_dates_casts.json", "w") as f:
    json.dump(tl, f, indent=2)
print("Wrote tile_lessons_public/tile_sql_text_dates_casts.json")

# ── Fix 2: tile_sql_null_fallback_and_union.json (public) ────────────────────
with open("batches/final_batch_006_da_sql_rest/tile_lessons_public/tile_sql_null_fallback_and_union.json") as f:
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
                print("Fixed public s01 dt_before cell highlight: added row")
    break

with open("batches/final_batch_006_da_sql_rest/tile_lessons_public/tile_sql_null_fallback_and_union.json", "w") as f:
    json.dump(tl2, f, indent=2)
print("Wrote tile_lessons_public/tile_sql_null_fallback_and_union.json")
if not fixed:
    print("(public null_fallback tile_lesson already had row field or no highlight found)")
