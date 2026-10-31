import json, re

path = "batches/final_batch_006_da_sql_rest/interactions.part.c2.json"

with open(path) as f:
    data = json.load(f)

# Find tile_sql_text_dates_casts, step s06
for tile in data["tiles"]:
    if tile["tile_id"] == "tile_sql_text_dates_casts":
        for item in tile["interactions"]:
            if item["step_id"] == "tile_sql_text_dates_casts.s06":
                ix = item["interaction"]
                
                # Fix the prompt: change `order_date - '2024-01-01'` to `order_date - DATE '2024-01-01'`
                ix["public"]["prompt"] = ix["public"]["prompt"].replace(
                    "use `order_date - '2024-01-01'`",
                    "use `order_date - DATE '2024-01-01'`"
                )
                
                # Fix the starter file content
                for f_item in ix["public"]["workspace"]["files"]:
                    if f_item["path"] == "query.sql":
                        f_item["content"] = f_item["content"].replace(
                            "-- days_since_start: order_date - '2024-01-01'",
                            "-- days_since_start: order_date - DATE '2024-01-01'"
                        )
                
                # Fix the solution file content
                for sf in ix["grading"]["solution_files"]:
                    if sf["path"] == "query.sql":
                        sf["content"] = sf["content"].replace(
                            "order_date - '2024-01-01'",
                            "order_date - DATE '2024-01-01'"
                        )
                
                # Fix the hint
                ix["feedback"]["hints"][1] = ix["feedback"]["hints"][1].replace(
                    "order_date - '2024-01-01' returns an integer number of days.",
                    "order_date - DATE '2024-01-01' returns an integer number of days."
                )
                
                print("Patched s06 solution and prompt.")
                print("Solution content:", sf["content"])

with open(path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done.")
