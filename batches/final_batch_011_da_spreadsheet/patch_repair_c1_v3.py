#!/usr/bin/env python3
"""
Repair patch for interactions.part.c1.json:

Fix 1: tile_spreadsheet_aggregation_logical.s10 / test_f5_extreme
  - The starter file has no typed input cells for C2-C5; the formula references
    cells that come from the mount, but C5 in the mount is null (LG-2004 is Pending).
  - Fix: add C2=28, C3=45, C4=62, C5=19 as typed constants in the starter file
    so the gate's hidden_checks can mutate them and the formula result changes.

Fix 2: tile_spreadsheet_text_date_conditional_agg.s03
  - reference_formula uses TRUE() (fn:TRUE) which is not in allowed syntax.
  - Fix: change TRUE() to TRUE (boolean literal).
"""
import json, re

path = "batches/final_batch_011_da_spreadsheet/interactions.part.c1.json"

with open(path) as f:
    data = json.load(f)

fixed = [0, 0]

for tile in data["tiles"]:
    for item in tile["interactions"]:
        ix = item["interaction"]

        # Fix 1: tile_spreadsheet_aggregation_logical.s10
        if ix["interaction_id"] == "ix.tile_spreadsheet_aggregation_logical.s10":
            # Update the starter file to include typed input cells C2-C5
            for wf in ix["public"]["workspace"]["files"]:
                if wf["path"] == "book.sheet" and wf["role"] == "editable":
                    wf["content"] = (
                        "// The orders sheet has delivery_minutes in column C.\n"
                        "// Input cells (typed constants - the gate will mutate these):\n"
                        "orders!C2: 28\n"
                        "orders!C3: 45\n"
                        "orders!C4: 62\n"
                        "orders!C5: 19\n"
                        "\n"
                        "// Task 1: In F2, write a nested IF formula that classifies C2 as:\n"
                        "//   'Late'    if C2 > 60\n"
                        "//   'On Time' if C2 >= 30 AND C2 <= 60  (use AND for both bounds)\n"
                        "//   'Fast'    if C2 < 30\n"
                        "// Then write the same pattern in F3 and F4.\n"
                        "\n"
                        "// Task 2: In F5, write an IF formula that returns 'Extreme' if\n"
                        "//   C5 < 20 OR C5 > 70, and 'Normal' otherwise. Use OR.\n"
                    )
                    fixed[0] += 1
                    print("Fix 1 applied: starter file updated with typed input cells C2-C5")

        # Fix 2: tile_spreadsheet_text_date_conditional_agg.s03
        if ix["interaction_id"] == "ix.tile_spreadsheet_text_date_conditional_agg.s03":
            grading = ix.get("grading", {})
            if "reference_formula" in grading:
                old = grading["reference_formula"]
                # Replace TRUE() with TRUE (boolean literal, not function call)
                new = old.replace("TRUE()", "TRUE")
                if new != old:
                    grading["reference_formula"] = new
                    fixed[1] += 1
                    print(f"Fix 2 applied: reference_formula changed from {old!r} to {new!r}")

print(f"Fixes applied: {fixed}")

with open(path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("Done.")
