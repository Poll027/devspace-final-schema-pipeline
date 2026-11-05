import json

# Update the merged interactions.json to match the patched part
path = "batches/final_batch_011_da_spreadsheet/interactions.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

for tile in data["tiles"]:
    if tile["tile_id"] == "tile_spreadsheet_tables_named_ranges":
        for item in tile["interactions"]:
            if item["step_id"] == "tile_spreadsheet_tables_named_ranges.s08":
                old_msg = item["interaction"]["feedback"]["incorrect"]["message"]
                print(f"OLD: {old_msg}")
                new_msg = "Use SUM with the delivery_minutes range: =SUM(C2:C21). The delivery_minutes column is column C, rows 2 through 21."
                item["interaction"]["feedback"]["incorrect"]["message"] = new_msg
                print(f"NEW: {new_msg}")

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Merged interactions.json patched.")
