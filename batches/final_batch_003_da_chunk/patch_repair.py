import json, copy

with open("batches/final_batch_003_da_chunk/screens.part.c0_canary.json", "r") as f:
    data = json.load(f)

tile = data["tiles"][0]
steps = tile["steps"]

# ── BLOCKING: s01.b3 ──────────────────────────────────────────────────────────
# Find s01 and its b3 block
for step in steps:
    if step["step_id"] == "tile_stats_shape_outliers.s01":
        for block in step["blocks"]:
            if block["block_id"] == "tile_stats_shape_outliers.s01.b3":
                # Fix title
                block["title"] = "Right-skewed distribution: QuickShip delivery times"
                # Fix alt_text
                block["alt_text"] = (
                    "A bar chart showing the QuickShip delivery-time sample with bars tallest "
                    "at 18–28 min and a long tail trailing right toward 52 min — labelled "
                    "Right-skewed. An arrow marks the long tail."
                )
                # Remove left-skewed and symmetric annotations; keep only the right-skewed one
                block["annotations"] = [
                    {
                        "text": "Long tail → right-skewed",
                        "target": "tail_right"
                    }
                ]
                print("Patched s01.b3: title, alt_text, annotations")
                break

# ── ADVISORY: s06.b4 ─────────────────────────────────────────────────────────
# Change "genuine observation" → "genuine, correct observation"
for step in steps:
    if step["step_id"] == "tile_stats_shape_outliers.s06":
        for block in step["blocks"]:
            if block["block_id"] == "tile_stats_shape_outliers.s06.b4":
                old = block["text"]
                new = old.replace(
                    "it may instead be a genuine observation.",
                    "it may instead be a genuine, correct observation."
                )
                if new != old:
                    block["text"] = new
                    print("Patched s06.b4: genuine observation → genuine, correct observation")
                else:
                    print("WARNING: s06.b4 pattern not found, no change made")
                break

# ── ADVISORY: s12 lede ───────────────────────────────────────────────────────
# Add missing "50–80 min: 0 orders" bin to the frequency table listing in the lede
for step in steps:
    if step["step_id"] == "tile_stats_shape_outliers.s12":
        old_lede = step["lede"]
        # Current lede ends with "40–50 min: 2 orders; 80–90 min: 1 order."
        # Insert "50–80 min: 0 orders;" before "80–90 min: 1 order."
        new_lede = old_lede.replace(
            "40–50 min: 2 orders; 80–90 min: 1 order.",
            "40–50 min: 2 orders; 50–80 min: 0 orders; 80–90 min: 1 order."
        )
        if new_lede != old_lede:
            step["lede"] = new_lede
            print("Patched s12 lede: added 50–80 min: 0 orders bin")
        else:
            print("WARNING: s12 lede pattern not found, no change made")
        break

with open("batches/final_batch_003_da_chunk/screens.part.c0_canary.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done.")
