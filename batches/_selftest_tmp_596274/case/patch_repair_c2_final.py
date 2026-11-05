"""
Patch screens.json to remove duplicate tile entries (indices 6,7,8) that have
remediation steps incorrectly placed in steps[] instead of remediation_steps[].
The correct entries are at indices 3,4,5 which have proper structure.
"""
import json
from pathlib import Path

B = Path("batches/final_batch_012_da_viz")

# Load screens.json
with open(B / "screens.json") as f:
    screens = json.load(f)

print("Before: number of tiles:", len(screens["tiles"]))
for i, tile in enumerate(screens["tiles"]):
    print(f"  [{i}] {tile['tile_id']}: steps={len(tile.get('steps',[]))}, rem={len(tile.get('remediation_steps',[]))}")

# The tiles at indices 6,7,8 are duplicates of 3,4,5 but with wrong structure
# (remediation steps in steps[] instead of remediation_steps[])
# Remove them
TARGET_IDS = {
    "tile_viz_labeling_chart_selection",
    "tile_viz_custom_multi_panel",
    "tile_viz_seaborn_stats_themes",
}

# Keep only the first occurrence of each tile_id
seen = set()
new_tiles = []
for tile in screens["tiles"]:
    tid = tile["tile_id"]
    if tid in TARGET_IDS:
        if tid not in seen:
            seen.add(tid)
            new_tiles.append(tile)
        else:
            print(f"  Removing duplicate: {tid}")
    else:
        new_tiles.append(tile)

screens["tiles"] = new_tiles

print("\nAfter: number of tiles:", len(screens["tiles"]))
for i, tile in enumerate(screens["tiles"]):
    print(f"  [{i}] {tile['tile_id']}: steps={len(tile.get('steps',[]))}, rem={len(tile.get('remediation_steps',[]))}")

# Verify the correct structure
for tile in screens["tiles"]:
    if tile["tile_id"] == "tile_viz_labeling_chart_selection":
        # Check s11 lineage
        for step in tile.get("steps", []):
            if step["step_id"] == "tile_viz_labeling_chart_selection.s11":
                tbs = step.get("lineage", {}).get("teaching_block_ids", [])
                print(f"\ns11 teaching_block_ids: {tbs}")
                assert "viz.chart_type_selection#tb3" in tbs, "s11 missing tb3!"
        # Check no remediation in steps
        for step in tile.get("steps", []):
            assert step["type"] != "remediation", f"Remediation step {step['step_id']} in steps[]!"
        print(f"tile_viz_labeling_chart_selection: remediation_steps = {[s['step_id'] for s in tile.get('remediation_steps', [])]}")
    
    if tile["tile_id"] == "tile_viz_seaborn_stats_themes":
        # Check s01 has chart block
        for step in tile.get("steps", []):
            if step["step_id"] == "tile_viz_seaborn_stats_themes.s01":
                block_types = [b["type"] for b in step.get("blocks", [])]
                print(f"\ns01 block types: {block_types}")
                assert "chart" in block_types, "s01 missing chart block!"
        # Check no remediation in steps
        for step in tile.get("steps", []):
            assert step["type"] != "remediation", f"Remediation step {step['step_id']} in steps[]!"
        print(f"tile_viz_seaborn_stats_themes: remediation_steps = {[s['step_id'] for s in tile.get('remediation_steps', [])]}")
    
    if tile["tile_id"] == "tile_viz_custom_multi_panel":
        # Check no remediation in steps
        for step in tile.get("steps", []):
            assert step["type"] != "remediation", f"Remediation step {step['step_id']} in steps[]!"
        print(f"tile_viz_custom_multi_panel: remediation_steps = {[s['step_id'] for s in tile.get('remediation_steps', [])]}")

# Save
with open(B / "screens.json", "w") as f:
    json.dump(screens, f, indent=2)

print("\nscreens.json patched successfully.")
