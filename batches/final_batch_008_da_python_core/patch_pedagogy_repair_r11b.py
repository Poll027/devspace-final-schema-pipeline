#!/usr/bin/env python3
"""
Pedagogy repair round 11b – fix starter code to match prompt's code block exactly.

The prompt's code block shows:
  def CalcFee( minutes,rate ):
    Fee=minutes*rate
    return Fee
  print( CalcFee( 30,2 ) )

The starter should have the same "before" code (with the same issues to fix).
"""

import json

C3_PATH = "batches/final_batch_008_da_python_core/interactions.part.c3.json"
with open(C3_PATH) as f:
    c3 = json.load(f)

# The starter should match the prompt's code block exactly (same issues to fix)
NEW_STARTER = (
    "minutes = 30\nrate = 2\n\n"
    "# Rewrite the function below to follow PEP 8 style.\n"
    "# Use 4-space indentation, lowercase_with_underscores names,\n"
    "# and tidy whitespace. Do not change what the function does.\n\n"
    "def CalcFee( minutes,rate ):\n"
    "  Fee=minutes*rate\n"
    "  return Fee\n\n"
    "print( CalcFee( 30,2 ) )\n"
)

for tile in c3["tiles"]:
    if tile["tile_id"] == "tile_python_pep8_style":
        for item in tile["interactions"]:
            if item["step_id"] == "tile_python_pep8_style.s03":
                ix = item["interaction"]
                for wf in ix["public"]["workspace"]["files"]:
                    if wf["path"] == "solution.py" and wf["role"] == "editable":
                        old = wf["content"]
                        wf["content"] = NEW_STARTER
                        print(f"Updated starter:")
                        print(f"  OLD: {repr(old)}")
                        print(f"  NEW: {repr(NEW_STARTER)}")

with open(C3_PATH, "w") as f:
    json.dump(c3, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(f"Written: {C3_PATH}")
