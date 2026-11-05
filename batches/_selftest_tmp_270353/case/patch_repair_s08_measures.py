"""
Repair patch: remove write_whole_row_or_whole_column_reference measure from s08.
The exercise only asks for a rectangular range (C2:C21), not a whole-column reference,
so that capability measure is not exercised and must be removed.
"""
import json, pathlib

path = pathlib.Path("batches/final_batch_011_da_spreadsheet/interactions.part.c0_canary.json")
data = json.loads(path.read_text())

# Locate s08 interaction
for tile in data["tiles"]:
    if tile["tile_id"] == "tile_spreadsheet_grid_references":
        for entry in tile["interactions"]:
            if entry["step_id"] == "tile_spreadsheet_grid_references.s08":
                ix = entry["interaction"]
                # Remove the write_whole_row_or_whole_column_reference measure
                before = len(ix["measures"])
                ix["measures"] = [
                    m for m in ix["measures"]
                    if m["capability"] != "write_whole_row_or_whole_column_reference"
                ]
                after = len(ix["measures"])
                print(f"measures: {before} -> {after}")

                # Also remove the corresponding anchor
                before_a = len(ix["anchors"])
                ix["anchors"] = [
                    a for a in ix["anchors"]
                    if "write_whole_row_or_whole_column_reference" not in a
                ]
                after_a = len(ix["anchors"])
                print(f"anchors: {before_a} -> {after_a}")

path.write_text(json.dumps(data, indent=2))
print("Done.")
