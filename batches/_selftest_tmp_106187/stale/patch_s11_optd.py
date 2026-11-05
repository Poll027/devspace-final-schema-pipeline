import json

path = "batches/final_batch_008_da_python_core/interactions.part.c1.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Find tile_python_operators_conversion, step s11
for tile in data["tiles"]:
    if tile["tile_id"] == "tile_python_operators_conversion":
        for item in tile["interactions"]:
            if item["step_id"] == "tile_python_operators_conversion.s11":
                old_msg = item["interaction"]["grading"]["option_feedback"]["opt_d"]["message"]
                print(f"OLD: {old_msg}")
                new_msg = (
                    "That describes `or` when the left side is false \u2014 Python evaluates the right side and returns it. "
                    "For `and`, if the left side is false, Python returns it immediately without evaluating the right side."
                )
                item["interaction"]["grading"]["option_feedback"]["opt_d"]["message"] = new_msg
                print(f"NEW: {new_msg}")

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patch applied.")
