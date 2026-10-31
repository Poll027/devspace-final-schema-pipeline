import json

def fix_s06(data):
    """Fix tile_sql_text_dates_casts.s06 in the given interactions data."""
    for tile in data["tiles"]:
        if tile["tile_id"] == "tile_sql_text_dates_casts":
            for item in tile["interactions"]:
                if item["step_id"] == "tile_sql_text_dates_casts.s06":
                    ix = item["interaction"]
                    
                    # Fix the solution file
                    for sf in ix["grading"]["solution_files"]:
                        if sf["path"] == "query.sql":
                            old = sf["content"]
                            new = old.replace(
                                "order_date - DATE '2024-01-01'",
                                "order_date - MAKE_DATE(2024, 1, 1)"
                            )
                            assert new != old, f"Solution not changed in {data.get('kind', '?')}"
                            sf["content"] = new
                            print(f"  Fixed solution")
                    
                    # Fix the prompt
                    old_prompt = ix["public"]["prompt"]
                    new_prompt = old_prompt.replace(
                        "order_date - '2024-01-01'",
                        "order_date - MAKE_DATE(2024, 1, 1)"
                    )
                    if new_prompt != old_prompt:
                        ix["public"]["prompt"] = new_prompt
                        print(f"  Fixed prompt")
                    
                    # Fix the starter file comment
                    for wf in ix["public"]["workspace"]["files"]:
                        if wf["path"] == "query.sql":
                            old_content = wf["content"]
                            new_content = old_content.replace(
                                "order_date - '2024-01-01'",
                                "order_date - MAKE_DATE(2024, 1, 1)"
                            )
                            if new_content != old_content:
                                wf["content"] = new_content
                                print(f"  Fixed starter comment")
                    
                    # Fix feedback hints
                    for hint in ix["feedback"].get("hints", []):
                        pass  # hints are strings, can't mutate in place
                    hints = ix["feedback"].get("hints", [])
                    new_hints = [h.replace("DATE '2024-01-01'", "MAKE_DATE(2024, 1, 1)") for h in hints]
                    if new_hints != hints:
                        ix["feedback"]["hints"] = new_hints
                        print(f"  Fixed hints")
                    
                    # Fix incorrect feedback message
                    inc = ix["feedback"].get("incorrect", {})
                    if inc.get("message"):
                        new_msg = inc["message"].replace("DATE '2024-01-01'", "MAKE_DATE(2024, 1, 1)")
                        if new_msg != inc["message"]:
                            inc["message"] = new_msg
                            print(f"  Fixed incorrect message")
                    
                    # Fix message_on_fail in tests
                    for test in ix["grading"].get("tests", []):
                        if test.get("message_on_fail"):
                            new_msg = test["message_on_fail"].replace("DATE '2024-01-01'", "MAKE_DATE(2024, 1, 1)")
                            if new_msg != test["message_on_fail"]:
                                test["message_on_fail"] = new_msg
                                print(f"  Fixed message_on_fail")
                    
                    return True
    return False

# Fix interactions.part.c2.json
print("Fixing interactions.part.c2.json...")
path = "batches/final_batch_006_da_sql_rest/interactions.part.c2.json"
with open(path) as f:
    data = json.load(f)
result = fix_s06(data)
assert result, "s06 not found in part.c2"
with open(path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("  Done.")

# Fix interactions.json
print("Fixing interactions.json...")
path2 = "batches/final_batch_006_da_sql_rest/interactions.json"
with open(path2) as f:
    data2 = json.load(f)
result2 = fix_s06(data2)
assert result2, "s06 not found in interactions.json"
with open(path2, "w") as f:
    json.dump(data2, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("  Done.")
