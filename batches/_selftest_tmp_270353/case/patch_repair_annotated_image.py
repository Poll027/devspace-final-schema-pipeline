"""
Repair patch: replace annotated_image (asset_grid_model_visual) in screens.json
at tile_spreadsheet_grid_references.s01.b3 with the diagram block already present
in screens.part.c0_canary.json.
"""
import json

# ── Load the diagram block from the already-patched part file ─────────────
part_path = "batches/final_batch_011_da_spreadsheet/screens.part.c0_canary.json"
with open(part_path) as f:
    part = json.load(f)

part_tile = next(t for t in part["tiles"] if t["tile_id"] == "tile_spreadsheet_grid_references")
part_step = next(s for s in part_tile["steps"] if s["step_id"] == "tile_spreadsheet_grid_references.s01")
part_b3 = next(b for b in part_step["blocks"] if b.get("block_id") == "tile_spreadsheet_grid_references.s01.b3")

assert part_b3["type"] == "diagram", f"Expected diagram in part file, got {part_b3['type']}"
print(f"Part file b3 type: {part_b3['type']} ✓")

# ── Patch screens.json ────────────────────────────────────────────────────
screens_path = "batches/final_batch_011_da_spreadsheet/screens.json"
with open(screens_path) as f:
    screens = json.load(f)

screens_tile = next(t for t in screens["tiles"] if t["tile_id"] == "tile_spreadsheet_grid_references")
screens_step = next(s for s in screens_tile["steps"] if s["step_id"] == "tile_spreadsheet_grid_references.s01")

b3_idx = next(i for i, b in enumerate(screens_step["blocks"])
              if b.get("block_id") == "tile_spreadsheet_grid_references.s01.b3")

old_type = screens_step["blocks"][b3_idx]["type"]
print(f"screens.json b3 type before patch: {old_type}")

screens_step["blocks"][b3_idx] = part_b3

with open(screens_path, "w") as f:
    json.dump(screens, f, indent=2, ensure_ascii=False)

print(f"screens.json b3 type after patch: {screens_step['blocks'][b3_idx]['type']} ✓")
print("Patch applied to screens.json")
