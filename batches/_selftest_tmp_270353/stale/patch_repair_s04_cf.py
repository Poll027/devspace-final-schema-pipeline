"""
Repair patch for tile_spreadsheet_formatting_validation.s04 in screens.part.c3.json.
Finding: BLOCKING - hands_on step requires writing COUNTIF (blocked concept).
Fix (stage 03 scope): change step type from hands_on to check, update framing.
"""
import json, copy

with open("batches/final_batch_011_da_spreadsheet/screens.part.c3.json") as f:
    data = json.load(f)

patched = False
for tile in data["tiles"]:
    if tile["tile_id"] != "tile_spreadsheet_formatting_validation":
        continue
    for step in tile["steps"]:
        if step["step_id"] != "tile_spreadsheet_formatting_validation.s04":
            continue
        # Change type from hands_on to check
        step["type"] = "check"
        # Update eyebrow
        step["eyebrow"] = "Quick Check"
        # Update title and lede to reflect choice/identification (no COUNTIF)
        step["title"] = "Identifying a Conditional Formatting Rule"
        step["lede"] = "Identify which steps and settings define a Highlight Cells Rules rule for a given condition."
        # Update reward: check steps use 5 gems
        step["reward"]["gems"] = 5
        # Update lineage anchors: remove #practice, keep assessment anchor
        step["lineage"]["anchors"] = [
            "spreadsheet.conditional_formatting#assessment:apply_conditional_formatting_rule_for_given_condition"
        ]
        patched = True
        print(f"Patched step: {step['step_id']}")
        print(f"  type: {step['type']}")
        print(f"  eyebrow: {step['eyebrow']}")
        print(f"  title: {step['title']}")
        print(f"  lede: {step['lede']}")
        print(f"  reward gems: {step['reward']['gems']}")
        print(f"  anchors: {step['lineage']['anchors']}")
        break

if not patched:
    raise RuntimeError("Step tile_spreadsheet_formatting_validation.s04 not found!")

with open("batches/final_batch_011_da_spreadsheet/screens.part.c3.json", "w") as f:
    json.dump(data, f, indent=2)

print("Done.")
