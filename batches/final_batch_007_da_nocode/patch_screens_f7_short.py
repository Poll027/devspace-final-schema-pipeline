"""
Patch screens.json: update the prose block for f7 in s10 with a shorter text
that fits within the word budget (hard cap 1.5x of 48 = 92 words total).
"""
import json, pathlib

B = pathlib.Path("batches/final_batch_007_da_nocode")

with open(B / "screens.json") as fh:
    screens = json.load(fh)

SHORT_TEXT = (
    "This process is commonly iterative rather than strictly linear: "
    "earlier stages such as inspecting or cleaning may be revisited when "
    "later stages reveal new issues. If a suspicious value appears during "
    "analysis, go back and inspect or clean before continuing."
)

patched = False
for tile in screens["tiles"]:
    if tile["tile_id"] != "tile_data_quality_and_workflow":
        continue
    for step in tile["steps"]:
        if step["step_id"] != "tile_data_quality_and_workflow.s10":
            continue
        for block in step["blocks"]:
            if block.get("block_id") == "tile_data_quality_and_workflow.s10.b2":
                block["text"] = SHORT_TEXT
                patched = True
                print(f"Updated block text for s10.b2 ({len(SHORT_TEXT.split())} words)")

if not patched:
    raise RuntimeError("Block s10.b2 not found")

with open(B / "screens.json", "w") as fh:
    json.dump(screens, fh, indent=2, ensure_ascii=False)
    fh.write("\n")

print("screens.json written.")
