import json, sys

path = "batches/final_batch_004_da_chunk2/interactions.part.c0_canary.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Navigate to the s04 interaction
tiles = data["tiles"]
target_interaction = None
for tile in tiles:
    for step in tile["interactions"]:
        if step["step_id"] == "tile_stakeholder_prioritizing_framing_context.s04":
            target_interaction = step["interaction"]
            break

if target_interaction is None:
    print("ERROR: s04 step not found", file=sys.stderr)
    sys.exit(1)

# Change opt_bac text
options = target_interaction["public"]["options"]
changed_text = False
for opt in options:
    if opt["option_id"] == "opt_bac":
        opt["text"] = "B first, then A, then C — start with the secondary miss before the primary one, to build context."
        changed_text = True
        break

if not changed_text:
    print("ERROR: opt_bac option not found in public options", file=sys.stderr)
    sys.exit(1)

# Change opt_bac feedback
feedback = target_interaction["grading"]["option_feedback"]
if "opt_bac" not in feedback:
    print("ERROR: opt_bac not found in option_feedback", file=sys.stderr)
    sys.exit(1)

feedback["opt_bac"]["message"] = (
    "Starting with the secondary miss before the primary one does not follow the inverted pyramid. "
    "The inverted pyramid ranks by importance to the decision — Lagos is primary because it directly "
    "informs the staffing decision, so it must come first."
)

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patch applied successfully.")
