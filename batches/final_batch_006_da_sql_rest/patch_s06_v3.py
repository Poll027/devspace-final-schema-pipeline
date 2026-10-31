import json

def fix_date_literal(data, label):
    """Fix remaining DATE '2024-01-01' references in tile_sql_text_dates_casts.s06."""
    for tile in data["tiles"]:
        if tile["tile_id"] == "tile_sql_text_dates_casts":
            for item in tile["interactions"]:
                if item["step_id"] == "tile_sql_text_dates_casts.s06":
                    ix = item["interaction"]
                    
                    # Fix the prompt
                    old_prompt = ix["public"]["prompt"]
                    new_prompt = old_prompt.replace(
                        "order_date - DATE '2024-01-01'",
                        "order_date - MAKE_DATE(2024, 1, 1)"
                    )
                    if new_prompt != old_prompt:
                        ix["public"]["prompt"] = new_prompt
                        print(f"  [{label}] Fixed prompt")
                    
                    # Fix the starter file comment
                    for wf in ix["public"]["workspace"]["files"]:
                        if wf["path"] == "query.sql":
                            old_content = wf["content"]
                            new_content = old_content.replace(
                                "order_date - DATE '2024-01-01'",
                                "order_date - MAKE_DATE(2024, 1, 1)"
                            )
                            if new_content != old_content:
                                wf["content"] = new_content
                                print(f"  [{label}] Fixed starter comment")
                    
                    return True
    return False

for fname, label in [
    ("batches/final_batch_006_da_sql_rest/interactions.part.c2.json", "part.c2"),
    ("batches/final_batch_006_da_sql_rest/interactions.json", "interactions"),
]:
    with open(fname) as f:
        data = json.load(f)
    fix_date_literal(data, label)
    with open(fname, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

print("Done.")
