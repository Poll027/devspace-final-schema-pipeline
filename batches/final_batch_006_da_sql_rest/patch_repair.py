import json, re, copy

path = "batches/final_batch_006_da_sql_rest/interactions.part.c2.json"

with open(path) as f:
    data = json.load(f)

# Locate the tile_sql_text_dates_casts tile
for tile in data["tiles"]:
    if tile["tile_id"] != "tile_sql_text_dates_casts":
        continue

    for entry in tile["interactions"]:
        step_id = entry["step_id"]
        ix = entry["interaction"]

        # ── s06: replace MAKE_DATE(2024, 1, 1) with DATE '2024-01-01' ──────────
        if step_id == "tile_sql_text_dates_casts.s06":
            OLD = "MAKE_DATE(2024, 1, 1)"
            NEW = "DATE '2024-01-01'"

            # 1. Prompt text
            ix["public"]["prompt"] = ix["public"]["prompt"].replace(OLD, NEW)

            # 2. Starter file content (comment line)
            for f_obj in ix["public"]["workspace"]["files"]:
                f_obj["content"] = f_obj["content"].replace(OLD, NEW)

            # 3. Solution file content
            for sf in ix["grading"]["solution_files"]:
                sf["content"] = sf["content"].replace(OLD, NEW)

            print("s06 patched — MAKE_DATE replaced with DATE literal")

        # ── s08: rephrase question stem only ────────────────────────────────────
        if step_id == "tile_sql_text_dates_casts.s08":
            OLD_STEM = (
                "Which of these casts is **not** guaranteed to succeed because "
                "no suitable type conversion is defined between the value's type "
                "and the target type?"
            )
            NEW_STEM = (
                "Which of these casts will fail at runtime because the value "
                "cannot be meaningfully interpreted as the target type?"
            )
            if ix["public"]["prompt"] == OLD_STEM:
                ix["public"]["prompt"] = NEW_STEM
                print("s08 patched — stem rephrased")
            else:
                # Try a looser match in case whitespace differs
                current = ix["public"]["prompt"]
                if "no suitable type conversion is defined" in current:
                    ix["public"]["prompt"] = NEW_STEM
                    print("s08 patched (loose match) — stem rephrased")
                else:
                    print(f"s08 WARNING: stem not matched. Current: {current!r}")

with open(path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done — file written.")
