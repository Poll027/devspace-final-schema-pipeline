"""
Repair patch for pedagogy_review findings:
- Step 0 (s01): annotation on G1 in after-grid contradicts text (says "Full_Name" but prose says city+status)
- Step 7 (s08): annotation on H2 says "DATEDIF formula in formula bar" but H2 shows the computed result
- Step 10 (c2 s11): annotation on C3 says "referenced column was deleted" but formula is IN the amount column
"""
import json, copy

# ── Fix c1 ──────────────────────────────────────────────────────────────────
with open("batches/final_batch_011_da_spreadsheet/screens.part.c1.json") as f:
    c1 = json.load(f)

fixed_s01 = False
fixed_s08 = False

for tile in c1["tiles"]:
    for step in tile.get("steps", []):
        sid = step.get("step_id", "")

        # Step 0: tile_spreadsheet_text_date_conditional_agg.s01
        # Fix: annotation on G1 in the "after" grid says "Full_Name — combined with TEXTJOIN"
        # but the prose says city and status are combined, not First_Name/Last_Name.
        if sid == "tile_spreadsheet_text_date_conditional_agg.s01":
            for block in step.get("blocks", []):
                if block.get("type") == "before_after":
                    after = block.get("after", {})
                    for ann in after.get("annotations", []):
                        if ann.get("target") == "G1" and "Full_Name" in ann.get("text", ""):
                            ann["text"] = "city_status — combined with TEXTJOIN"
                            fixed_s01 = True

        # Step 7: tile_spreadsheet_text_date_conditional_agg.s08
        # Fix: annotation on H2 says "DATEDIF formula in formula bar"
        # H2 shows the computed result (days elapsed), not the formula itself.
        if sid == "tile_spreadsheet_text_date_conditional_agg.s08":
            for block in step.get("blocks", []):
                if block.get("type") == "spreadsheet_grid":
                    for ann in block.get("annotations", []):
                        if ann.get("target") == "H2" and "formula bar" in ann.get("text", ""):
                            ann["text"] = "days since order placed"
                            fixed_s08 = True

print(f"c1 s01 fixed: {fixed_s01}")
print(f"c1 s08 fixed: {fixed_s08}")

with open("batches/final_batch_011_da_spreadsheet/screens.part.c1.json", "w") as f:
    json.dump(c1, f, indent=2, ensure_ascii=False)
print("c1 written.")

# ── Fix c2 ──────────────────────────────────────────────────────────────────
with open("batches/final_batch_011_da_spreadsheet/screens.part.c2.json") as f:
    c2 = json.load(f)

fixed_s11 = False

for tile in c2["tiles"]:
    for step in tile.get("steps", []):
        sid = step.get("step_id", "")

        # Step 10: tile_spreadsheet_lookups_troubleshooting.s11
        # Fix: annotation on C3 says "#REF! — referenced column was deleted"
        # but =SUM(#REF!) is IN column C (amount). If C was deleted, C3 wouldn't exist.
        # The annotation should describe that the formula's referenced range was deleted,
        # not that C itself was deleted.
        if sid == "tile_spreadsheet_lookups_troubleshooting.s11":
            for block in step.get("blocks", []):
                if block.get("type") == "spreadsheet_grid":
                    for ann in block.get("annotations", []):
                        if ann.get("target") == "C3" and "referenced column was deleted" in ann.get("text", ""):
                            ann["text"] = "#REF! \u2014 formula references a deleted range"
                            fixed_s11 = True

print(f"c2 s11 fixed: {fixed_s11}")

with open("batches/final_batch_011_da_spreadsheet/screens.part.c2.json", "w") as f:
    json.dump(c2, f, indent=2, ensure_ascii=False)
print("c2 written.")
