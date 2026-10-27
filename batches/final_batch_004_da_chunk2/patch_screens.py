import json, re

path = "batches/final_batch_004_da_chunk2/screens.part.c0_canary.json"

with open(path) as f:
    data = json.load(f)

tiles = data["tiles"]
tile = tiles[0]  # only one tile
steps = tile["steps"]

# Build a lookup by step_id
step_map = {s["step_id"]: s for s in steps}

# --- Fix 1: s01.b2 ---
# "boiling the message down to a single sentence"
# → "boiling the overall message down to a single sentence that captures its core"
s01 = step_map["tile_stakeholder_prioritizing_framing_context.s01"]
for block in s01["blocks"]:
    if block.get("block_id") == "tile_stakeholder_prioritizing_framing_context.s01.b2":
        old = block["text"]
        # Replace the paraphrase with the fuller phrasing
        new = old.replace(
            "boiling the message down to a single sentence.",
            "boiling the overall message down to a single sentence that captures its core."
        )
        assert new != old, f"s01.b2 replacement did not match. Text was:\n{old}"
        block["text"] = new
        print("s01.b2 fixed:", repr(old[-80:]), "->", repr(new[-80:]))
        break

# --- Fix 2: s09.b2 ---
# "what is happening when the story begins"
# → "what is happening, or what the situation is, when the story begins"
s09 = step_map["tile_stakeholder_prioritizing_framing_context.s09"]
for block in s09["blocks"]:
    if block.get("block_id") == "tile_stakeholder_prioritizing_framing_context.s09.b2":
        old = block["text"]
        new = old.replace(
            "what is happening when the story begins",
            "what is happening, or what the situation is, when the story begins"
        )
        assert new != old, f"s09.b2 replacement did not match. Text was:\n{old}"
        block["text"] = new
        print("s09.b2 fixed:", repr(old[60:130]), "->", repr(new[60:130]))
        break

# --- Fix 3: s09.b3 ---
# Two changes:
# (a) "this quarter" → "last quarter"
# (b) append ", with more detailed information placed in a separate section"
#     after "a short paragraph explaining what the publication is about"
for block in s09["blocks"]:
    if block.get("block_id") == "tile_stakeholder_prioritizing_framing_context.s09.b3":
        old = block["text"]
        # (a) this quarter → last quarter
        new = old.replace("this quarter", "last quarter")
        # (b) append the missing clause after "what the publication is about"
        new = new.replace(
            "a short paragraph explaining what the publication is about.",
            "a short paragraph explaining what the publication is about, with more detailed information placed in a separate section."
        )
        assert new != old, f"s09.b3 replacement did not match. Text was:\n{old}"
        block["text"] = new
        print("s09.b3 fixed")
        print("  old:", old)
        print("  new:", new)
        break

with open(path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\nPatch complete.")
