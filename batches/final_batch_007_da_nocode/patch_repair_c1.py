"""
Repair patch for interactions.part.c1.json and screens.json.

Fixes:
1. (E) s18 lineage.teaching_block_ids in screens.json: reduce to ['stakeholder.identifying_decision_need#tb4']
2. (W) r03 never referenced: add remediation_step_id to s07 feedback
3. (W) r05 never referenced: add remediation_step_id to s11 feedback
4. (W) r07 never referenced: add remediation_step_id to s16 feedback
5. (W) s01.b1 prose block without lineage.fact_ids: add f1 to b1 lineage in screens.json
"""
import json
from pathlib import Path

B = Path("batches/final_batch_007_da_nocode")

# ── Fix interactions.part.c1.json ──────────────────────────────────────────
ix_path = B / "interactions.part.c1.json"
with open(ix_path) as f:
    ix_data = json.load(f)

remediation_map = {
    "tile_stakeholder_framing_requirements.s07": "tile_stakeholder_framing_requirements.r03",
    "tile_stakeholder_framing_requirements.s11": "tile_stakeholder_framing_requirements.r05",
    "tile_stakeholder_framing_requirements.s16": "tile_stakeholder_framing_requirements.r07",
}

for tile in ix_data.get("tiles", []):
    if tile.get("tile_id") == "tile_stakeholder_framing_requirements":
        for ix in tile.get("interactions", []):
            sid = ix.get("step_id")
            if sid in remediation_map:
                fb = ix["interaction"]["feedback"]
                fb["remediation_step_id"] = remediation_map[sid]
                print(f"  Added remediation_step_id={remediation_map[sid]} to {sid}")

with open(ix_path, "w") as f:
    json.dump(ix_data, f, indent=2, ensure_ascii=False)
print(f"Wrote {ix_path}")

# ── Fix screens.json ───────────────────────────────────────────────────────
sc_path = B / "screens.json"
with open(sc_path) as f:
    sc_data = json.load(f)

for tile in sc_data.get("tiles", []):
    if tile.get("tile_id") == "tile_stakeholder_framing_requirements":
        for step in tile.get("steps", []):
            sid = step.get("step_id")

            # Fix 1: s18 teaching_block_ids
            if sid == "tile_stakeholder_framing_requirements.s18":
                old = step["lineage"]["teaching_block_ids"]
                step["lineage"]["teaching_block_ids"] = ["stakeholder.identifying_decision_need#tb4"]
                print(f"  s18 teaching_block_ids: {old} -> {step['lineage']['teaching_block_ids']}")

            # Fix 5: s01.b1 prose block without fact_ids
            if sid == "tile_stakeholder_framing_requirements.s01":
                for b in step.get("blocks", []):
                    if b.get("block_id") == "tile_stakeholder_framing_requirements.s01.b1":
                        if not b["lineage"].get("fact_ids"):
                            b["lineage"]["fact_ids"] = ["stakeholder.identifying_decision_need#f1"]
                            print(f"  s01.b1 fact_ids set to {b['lineage']['fact_ids']}")

with open(sc_path, "w") as f:
    json.dump(sc_data, f, indent=2, ensure_ascii=False)
print(f"Wrote {sc_path}")

# ── Fix screens.part.c1.json ───────────────────────────────────────────────
sc_part_path = B / "screens.part.c1.json"
with open(sc_part_path) as f:
    sc_part_data = json.load(f)

for tile in sc_part_data.get("tiles", []):
    if tile.get("tile_id") == "tile_stakeholder_framing_requirements":
        for step in tile.get("steps", []):
            sid = step.get("step_id")

            if sid == "tile_stakeholder_framing_requirements.s18":
                old = step["lineage"]["teaching_block_ids"]
                step["lineage"]["teaching_block_ids"] = ["stakeholder.identifying_decision_need#tb4"]
                print(f"  screens.part.c1 s18 teaching_block_ids: {old} -> {step['lineage']['teaching_block_ids']}")

            if sid == "tile_stakeholder_framing_requirements.s01":
                for b in step.get("blocks", []):
                    if b.get("block_id") == "tile_stakeholder_framing_requirements.s01.b1":
                        if not b["lineage"].get("fact_ids"):
                            b["lineage"]["fact_ids"] = ["stakeholder.identifying_decision_need#f1"]
                            print(f"  screens.part.c1 s01.b1 fact_ids set to {b['lineage']['fact_ids']}")

with open(sc_part_path, "w") as f:
    json.dump(sc_part_data, f, indent=2, ensure_ascii=False)
print(f"Wrote {sc_part_path}")

print("Done.")
