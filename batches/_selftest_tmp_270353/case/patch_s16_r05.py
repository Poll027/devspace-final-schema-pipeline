import json

path = "batches/final_batch_011_da_spreadsheet/screens.part.c1.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

changes = 0

for tile in data["tiles"]:
    if tile["tile_id"] != "tile_spreadsheet_text_date_conditional_agg":
        continue

    # Fix s16 lede (in steps)
    for step in tile.get("steps", []):
        if step["step_id"] == "tile_spreadsheet_text_date_conditional_agg.s16":
            old_lede = step.get("lede", "")
            new_lede = "How do you count values in C2:C21 that are greater than or equal to 30 AND less than or equal to 60?"
            if old_lede != new_lede:
                step["lede"] = new_lede
                print(f"Fixed s16 lede: {old_lede!r}")
                changes += 1
            else:
                print("s16 lede already correct")

    # Fix r05 prose block (in remediation_steps)
    for step in tile.get("remediation_steps", []):
        if step["step_id"] == "tile_spreadsheet_text_date_conditional_agg.r05":
            print("Found r05 in remediation_steps")
            for block in step.get("blocks", []):
                if block.get("block_id") == "tile_spreadsheet_text_date_conditional_agg.r05.b1":
                    old_text = block["text"]
                    new_text = (
                        'COUNTIFS allows the same range to appear in more than one criteria pair. '
                        'To count values between 30 and 60 (inclusive) in C2:C21, write: '
                        '=COUNTIFS(C2:C21,">=30",C2:C21,"<=60"). '
                        'The first pair filters rows where delivery_minutes is greater than or equal to 30; '
                        'the second pair further filters to delivery_minutes less than or equal to 60. '
                        'Both criteria must be in quotes because they contain comparison symbols.'
                    )
                    if old_text != new_text:
                        block["text"] = new_text
                        print(f"Fixed r05.b1 text")
                        changes += 1
                    else:
                        print("r05.b1 text already correct")

print(f"Total changes: {changes}")

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Written.")
