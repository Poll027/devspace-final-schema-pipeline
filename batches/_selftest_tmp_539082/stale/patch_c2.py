import re

path = "batches/final_batch_009_da_pandas/screens.part.c2.json"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# BLOCKING fix: tile_pandas_descriptive_stats/r01 — change 25% 20.0 to 21.0
# The line is inside a code comment in the r01 remediation code block
old_blocking = "# 25%      20.0"
new_blocking = "# 25%      21.0"
assert content.count(old_blocking) == 1, f"Expected exactly 1 occurrence of blocking pattern, found {content.count(old_blocking)}"
content = content.replace(old_blocking, new_blocking, 1)

# ADVISORY fix 1: tile_pandas_dtype_datetime/s05 — vary the pickup_date head() output
old_advisory1 = "# '2024-03-14', '2024-03-14', ..."
new_advisory1 = "# '2024-03-14', '2024-03-14', '2024-03-15', ..."
assert content.count(old_advisory1) == 1, f"Expected exactly 1 occurrence of advisory1 pattern, found {content.count(old_advisory1)}"
content = content.replace(old_advisory1, new_advisory1, 1)

# ADVISORY fix 2: tile_pandas_text_dupes_missing/s05 — change #1042 to #1003 in intro
# Only the intro prose (b1) mentions #1042; b3 also mentions #1042 but that's a keep='last' example
# The finding says: change "order `#1042`" to "order `#1003`" in the intro to match the before/after table
# The intro is in b1; b3 also references #1042 but the finding only targets the intro
old_advisory2 = "Suppose order `#1042` appears twice in the SwiftDrop orders DataFrame"
new_advisory2 = "Suppose order `#1003` appears twice in the SwiftDrop orders DataFrame"
assert content.count(old_advisory2) == 1, f"Expected exactly 1 occurrence of advisory2 pattern, found {content.count(old_advisory2)}"
content = content.replace(old_advisory2, new_advisory2, 1)

# Also fix the b3 reference to #1042 to be consistent (same advisory, same intro area)
# The finding says "in the intro" — b3 is mechanism text, not intro, so leave it alone per instructions
# "Change only what the findings name"

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Patch applied successfully.")
