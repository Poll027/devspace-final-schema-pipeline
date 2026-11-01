"""
Sync interactions.json with the updated interactions.part.c1.json.
Replaces the tile_stakeholder_framing_requirements tile in interactions.json
with the updated version from interactions.part.c1.json.
"""
import json
from pathlib import Path

B = Path("batches/final_batch_007_da_nocode")

# Load the updated part
with open(B / "interactions.part.c1.json") as f:
    part = json.load(f)

# Load the merged file
with open(B / "interactions.json") as f:
    merged = json.load(f)

# Find the c1 tile in the part
c1_tile = next(t for t in part["tiles"] if t["tile_id"] == "tile_stakeholder_framing_requirements")

# Replace in merged
for i, tile in enumerate(merged["tiles"]):
    if tile["tile_id"] == "tile_stakeholder_framing_requirements":
        merged["tiles"][i] = c1_tile
        print(f"Replaced tile_stakeholder_framing_requirements in interactions.json")
        break

with open(B / "interactions.json", "w") as f:
    json.dump(merged, f, indent=2, ensure_ascii=False)
print(f"Wrote interactions.json")

# Verify
with open(B / "interactions.json") as f:
    check = json.load(f)
for tile in check["tiles"]:
    if tile["tile_id"] == "tile_stakeholder_framing_requirements":
        for ix in tile["interactions"]:
            sid = ix["step_id"]
            if sid in ["tile_stakeholder_framing_requirements.s07",
                       "tile_stakeholder_framing_requirements.s11",
                       "tile_stakeholder_framing_requirements.s16"]:
                rid = ix["interaction"]["feedback"].get("remediation_step_id")
                print(f"  {sid} -> {rid}")
