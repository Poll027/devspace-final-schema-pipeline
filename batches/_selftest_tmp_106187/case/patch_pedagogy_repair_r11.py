#!/usr/bin/env python3
"""
Pedagogy repair round 11 – two targeted fixes:

1. interactions.part.c1.json  tile_python_operators_conversion/s10
   opt_b feedback already matches the required text – verify and leave.

2. interactions.part.c3.json  tile_python_pep8_style/s03
   The prompt's code block shows lowercase `minutes`/`rate` as parameters,
   but the starter code has `Minutes`/`Rate` (uppercase).  Fix: update the
   starter code to use lowercase `minutes`/`rate` as parameters, matching
   the prompt's displayed code.  Also remove the implicit rename task by
   updating the prompt to remove instruction #3 ("Rename `Minutes`→`minutes`
   and `Rate`→`rate`") if it exists, and renumber remaining instructions.
   Since the current prompt has 4 instructions and #3 is about indentation
   (not renaming params), the fix is to update the starter code only.
"""

import json, copy, sys

# ── Fix 1: verify opt_b in s10 (c1) ─────────────────────────────────────────
C1_PATH = "batches/final_batch_008_da_python_core/interactions.part.c1.json"
with open(C1_PATH) as f:
    c1 = json.load(f)

REQUIRED_OPT_B = (
    "Even if `not` were evaluated before `==`, the result would be "
    "`(not True) == False` \u2192 `False == False` \u2192 `True`, not `False`. "
    "In fact, `not` has lower priority than `==`, so Python reads "
    "`not (is_late == False)` \u2192 `not False` \u2192 `True`."
)

found_s10 = False
for tile in c1["tiles"]:
    if tile["tile_id"] == "tile_python_operators_conversion":
        for item in tile["interactions"]:
            if item["step_id"] == "tile_python_operators_conversion.s10":
                found_s10 = True
                current = item["interaction"]["grading"]["option_feedback"]["opt_b"]["message"]
                if current == REQUIRED_OPT_B:
                    print("c1/s10 opt_b: already correct – no change needed")
                else:
                    print(f"c1/s10 opt_b: MISMATCH\n  current: {repr(current)}\n  required: {repr(REQUIRED_OPT_B)}")
                    item["interaction"]["grading"]["option_feedback"]["opt_b"]["message"] = REQUIRED_OPT_B
                    print("c1/s10 opt_b: fixed")

if not found_s10:
    print("ERROR: tile_python_operators_conversion/s10 not found in c1", file=sys.stderr)
    sys.exit(1)

with open(C1_PATH, "w") as f:
    json.dump(c1, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(f"Written: {C1_PATH}")

# ── Fix 2: pep8/s03 starter code (c3) ────────────────────────────────────────
C3_PATH = "batches/final_batch_008_da_python_core/interactions.part.c3.json"
with open(C3_PATH) as f:
    c3 = json.load(f)

# The prompt's code block shows:
#   def CalcFee( minutes,rate ):
#     Fee=minutes*rate
# The starter code has:
#   def CalcFee(Minutes,Rate):
#     Fee=Minutes*Rate
# Fix: update starter to use lowercase minutes/rate as parameters.
# Also update the prompt: remove any instruction about renaming Minutes/Rate
# and renumber remaining instructions.

OLD_STARTER = (
    "minutes = 30\nrate = 2\n\n"
    "# Rewrite the function below to follow PEP 8 style.\n"
    "# Use 4-space indentation, lowercase_with_underscores names,\n"
    "# and tidy whitespace. Do not change what the function does.\n\n"
    "def CalcFee(Minutes,Rate):\n"
    "  Fee=Minutes*Rate\n"
    "  return Fee\n\n"
    "print(CalcFee(minutes, rate))\n"
)

NEW_STARTER = (
    "minutes = 30\nrate = 2\n\n"
    "# Rewrite the function below to follow PEP 8 style.\n"
    "# Use 4-space indentation, lowercase_with_underscores names,\n"
    "# and tidy whitespace. Do not change what the function does.\n\n"
    "def CalcFee(minutes, rate):\n"
    "  Fee=minutes*rate\n"
    "  return Fee\n\n"
    "print(CalcFee(minutes, rate))\n"
)

# The prompt currently has 4 instructions:
# 1. Rename `CalcFee` → `calc_fee`
# 2. Rename `Fee` → `fee`
# 3. Use **4-space** indentation (not 2 spaces)
# 4. Remove extraneous spaces inside `()` and before `,`
#
# The finding says instruction #3 says "rename `Minutes`→`minutes` and
# `Rate`→`rate`" but the starter already uses lowercase.  Since the current
# prompt does NOT have such an instruction #3, the fix is only to the starter.
# However, to be safe, also check if the prompt has any such instruction and
# remove it if found.

OLD_PROMPT_INSTR3 = "3. Rename `Minutes` \u2192 `minutes` and `Rate` \u2192 `rate` (lowercase parameter names)\n"
# Also check arrow variants
OLD_PROMPT_INSTR3_ALT = "3. Rename `Minutes` → `minutes` and `Rate` → `rate`"

found_s03 = False
for tile in c3["tiles"]:
    if tile["tile_id"] == "tile_python_pep8_style":
        for item in tile["interactions"]:
            if item["step_id"] == "tile_python_pep8_style.s03":
                found_s03 = True
                ix = item["interaction"]

                # Fix starter code
                for wf in ix["public"]["workspace"]["files"]:
                    if wf["path"] == "solution.py" and wf["role"] == "editable":
                        if wf["content"] == OLD_STARTER:
                            wf["content"] = NEW_STARTER
                            print("c3/s03: starter code updated (Minutes→minutes, Rate→rate)")
                        elif "Minutes" in wf["content"] or "Rate" in wf["content"]:
                            # Patch whatever uppercase params exist
                            wf["content"] = (
                                wf["content"]
                                .replace("Minutes", "minutes")
                                .replace("Rate", "rate")
                            )
                            print("c3/s03: starter code patched (uppercase params → lowercase)")
                        else:
                            print("c3/s03: starter code already lowercase – no change")

                # Check prompt for any instruction about renaming Minutes/Rate
                prompt = ix["public"]["prompt"]
                if "Minutes" in prompt and "minutes" in prompt and "rename" in prompt.lower():
                    # Find and remove the instruction line
                    lines = prompt.split("\n")
                    new_lines = []
                    removed = False
                    counter = 1
                    for line in lines:
                        if ("Minutes" in line and "minutes" in line) or \
                           ("Rate" in line and "rate" in line and "rename" in line.lower()):
                            removed = True
                            print(f"c3/s03: removed prompt instruction: {line!r}")
                            continue
                        new_lines.append(line)
                    if removed:
                        # Renumber instructions
                        import re
                        result_lines = []
                        n = 1
                        for line in new_lines:
                            m = re.match(r'^(\d+)\. (.+)$', line)
                            if m:
                                result_lines.append(f"{n}. {m.group(2)}")
                                n += 1
                            else:
                                result_lines.append(line)
                        ix["public"]["prompt"] = "\n".join(result_lines)
                        print("c3/s03: prompt instructions renumbered")
                else:
                    print("c3/s03: no Minutes/Rate rename instruction found in prompt – no prompt change")

if not found_s03:
    print("ERROR: tile_python_pep8_style/s03 not found in c3", file=sys.stderr)
    sys.exit(1)

with open(C3_PATH, "w") as f:
    json.dump(c3, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(f"Written: {C3_PATH}")
print("Done.")
