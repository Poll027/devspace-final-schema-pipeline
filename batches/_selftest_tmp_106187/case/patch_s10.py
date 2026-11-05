import json

path = "batches/final_batch_008_da_python_core/interactions.part.c1.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Find tile_python_operators_conversion, step s10
for tile in data["tiles"]:
    if tile["tile_id"] == "tile_python_operators_conversion":
        for item in tile["interactions"]:
            if item["step_id"] == "tile_python_operators_conversion.s10":
                interaction = item["interaction"]
                options = interaction["public"]["options"]
                feedback = interaction["grading"]["option_feedback"]

                # Find opt_c and rewrite it
                for opt in options:
                    if opt["option_id"] == "opt_c":
                        opt["text"] = (
                            "`False` \u2014 `not` cancels out the comparison, "
                            "making the whole expression `False`"
                        )
                        break

                # Rewrite opt_c feedback
                feedback["opt_c"] = {
                    "message": (
                        "`not` does not cancel the comparison. It has lower priority than `==`, "
                        "so Python evaluates `is_late == False` first "
                        "(`True == False` \u2192 `False`), then `not False` \u2192 `True`."
                    )
                }

                print("Patched s10 opt_c successfully.")
                break

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("File written.")
