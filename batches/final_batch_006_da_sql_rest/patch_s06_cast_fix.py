"""
Patch: replace DATE '2024-01-01' (parsed as CAST) with '2024-01-01' in
tile_sql_text_dates_casts.s06 solution and prompt.
DATE 'literal' is parsed by sqlglot as CAST('literal' AS DATE), which
triggers the 'CAST(expression AS type)' blocked-syntax detector.
Using a bare string literal '2024-01-01' is implicitly coerced by DuckDB
when subtracted from a date column, and is not detected as CAST.
"""
import json, re

PATH = "batches/final_batch_006_da_sql_rest/interactions.part.c2.json"

with open(PATH) as f:
    data = json.load(f)

changed = 0
for tile in data["tiles"]:
    if tile["tile_id"] != "tile_sql_text_dates_casts":
        continue
    for item in tile["interactions"]:
        if item["step_id"] != "tile_sql_text_dates_casts.s06":
            continue
        ix = item["interaction"]

        # Fix solution: replace DATE '2024-01-01' with '2024-01-01'
        sol = ix["grading"]["solution_files"][0]
        old_sol = sol["content"]
        new_sol = old_sol.replace("DATE '2024-01-01'", "'2024-01-01'")
        assert new_sol != old_sol, "Solution was not changed"
        sol["content"] = new_sol
        changed += 1
        print(f"Fixed solution: {repr(old_sol)} -> {repr(new_sol)}")

        # Fix prompt: replace `order_date - DATE '2024-01-01'` with `order_date - '2024-01-01'`
        old_prompt = ix["public"]["prompt"]
        new_prompt = old_prompt.replace(
            "use `order_date - DATE '2024-01-01'`",
            "use `order_date - '2024-01-01'`"
        )
        assert new_prompt != old_prompt, "Prompt was not changed"
        ix["public"]["prompt"] = new_prompt
        changed += 1
        print("Fixed prompt.")

        # Fix starter file comment if it mentions DATE '2024-01-01'
        for wf in ix["public"]["workspace"]["files"]:
            if "DATE '2024-01-01'" in wf.get("content", ""):
                wf["content"] = wf["content"].replace("DATE '2024-01-01'", "'2024-01-01'")
                changed += 1
                print("Fixed starter file comment.")

        # Fix hints if they mention DATE '2024-01-01'
        hints = ix.get("feedback", {}).get("hints", [])
        for i, h in enumerate(hints):
            if "DATE '2024-01-01'" in h:
                hints[i] = h.replace("DATE '2024-01-01'", "'2024-01-01'")
                changed += 1
                print(f"Fixed hint {i}.")

print(f"\nTotal changes: {changed}")

with open(PATH, "w") as f:
    json.dump(data, f, indent=2)
print("Written.")
