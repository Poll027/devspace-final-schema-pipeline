import json, sys

path = "batches/final_batch_006_da_sql_rest/screens.part.c3.json"

with open(path) as f:
    data = json.load(f)

# Navigate to tile_sql_adv_joining_tables, step s01, block b4
tile = next(t for t in data["tiles"] if t["tile_id"] == "tile_sql_adv_joining_tables")
step = next(s for s in tile["steps"] if s["step_id"] == "tile_sql_adv_joining_tables.s01")
block = next(b for b in step["blocks"] if b.get("block_id") == "tile_sql_adv_joining_tables.s01.b4")

nodes = block["nodes"]

# Find the c4_note node index
c4_note_idx = next(i for i, n in enumerate(nodes) if n["id"] == "c4_note")

# Insert a c3_note node right before c4_note
c3_note = {
    "id": "c3_note",
    "label": "customer_id=3 (Fatima Aliyu) has no matching order — dropped from result",
    "kind": "annotation",
    "group": "note"
}

nodes.insert(c4_note_idx, c3_note)

with open(path, "w") as f:
    json.dump(data, f, indent=2)

print("Patch applied: c3_note inserted before c4_note in s01.b4 nodes.")
