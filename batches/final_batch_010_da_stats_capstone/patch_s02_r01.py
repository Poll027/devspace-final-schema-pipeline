import json

path = "batches/final_batch_010_da_stats_capstone/screens.part.c2.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

changes = 0

def patch_block(block, bid_target, old_marker, new_suffix):
    global changes
    bid = block.get("block_id", "")
    if bid != bid_target:
        return
    old = block["text"]
    if "full dataset" in old:
        print(f"  {bid}: already patched, skipping")
        return
    if old_marker in old:
        block["text"] = old.replace(old_marker, old_marker + new_suffix, 1)
        changes += 1
        print(f"  Patched {bid}")
    else:
        print(f"  WARNING: marker not found in {bid}")
        print(f"  Text: {repr(old[:120])}")

note = " (In the full dataset, beyond this sample, a handful of deliveries took over three hours, pulling the mean to 52 minutes while the median stays at 38 minutes.)"

for tile in data["tiles"]:
    if tile["tile_id"] != "tile_capstone_stats_dashboard":
        continue
    print(f"Processing tile: {tile['tile_id']}")

    # Patch s02.b1 in steps
    for step in tile.get("steps", []):
        if step["step_id"] == "tile_capstone_stats_dashboard.s02":
            for block in step.get("blocks", []):
                if block.get("type") == "prose":
                    patch_block(
                        block,
                        "tile_capstone_stats_dashboard.s02.b1",
                        "while the median stays at 38 minutes.",
                        note
                    )

    # Patch r01.b1 and r01.b2 in remediation_steps
    for step in tile.get("remediation_steps", []):
        if step["step_id"] == "tile_capstone_stats_dashboard.r01":
            for block in step.get("blocks", []):
                if block.get("type") == "prose":
                    patch_block(
                        block,
                        "tile_capstone_stats_dashboard.r01.b1",
                        "returns a mean of 52 minutes and a median of 38 minutes.",
                        note
                    )
                    patch_block(
                        block,
                        "tile_capstone_stats_dashboard.r01.b2",
                        "the mean rises to 52 minutes even though most deliveries were around 38 minutes.",
                        note
                    )

print(f"\nTotal changes: {changes}")

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("Written.")
