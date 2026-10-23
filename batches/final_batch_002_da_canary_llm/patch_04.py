import json

path = "batches/final_batch_002_da_canary_llm/interactions.json"

with open(path) as f:
    data = json.load(f)

# Navigate to tile_data_shape_and_types / s03 / grading / option_feedback / opt_a
for tile in data["tiles"]:
    if tile["tile_id"] == "tile_data_shape_and_types":
        for step in tile["interactions"]:
            if step["step_id"] == "tile_data_shape_and_types.s03":
                opt_a_fb = step["interaction"]["grading"]["option_feedback"]["opt_a"]
                if "misconception_id" in opt_a_fb:
                    del opt_a_fb["misconception_id"]
                    print("Removed misconception_id from opt_a feedback in s03.")
                else:
                    print("misconception_id not found — nothing to remove.")

with open(path, "w") as f:
    json.dump(data, f, indent=2)

print("Done.")
