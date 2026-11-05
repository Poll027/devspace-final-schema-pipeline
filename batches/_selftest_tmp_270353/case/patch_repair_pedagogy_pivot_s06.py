"""
Repair patch for tile_spreadsheet_pivot_tables/s06:
The prompt implied SUMIF was being previewed/introduced here, but SUMIF is
already taught in tile_spreadsheet_text_date_conditional_agg (which comes
BEFORE tile_spreadsheet_pivot_tables). Add a note clarifying SUMIF was
already covered, removing any misleading curriculum-sequence implication.
"""
import json, copy

path = "batches/final_batch_011_da_spreadsheet/interactions.part.c3.json"

with open(path) as f:
    data = json.load(f)

changed = False
for tile in data["tiles"]:
    if tile["tile_id"] != "tile_spreadsheet_pivot_tables":
        continue
    for item in tile["interactions"]:
        if item["step_id"] != "tile_spreadsheet_pivot_tables.s06":
            continue
        prompt = item["interaction"]["public"]["prompt"]
        # The current prompt uses SUMIF without noting it was already taught.
        # Replace the prompt to add the correct curriculum note (SUMIF was
        # covered earlier, not "will be covered in a later lesson").
        old_prompt = (
            "A PivotTable with city in the Rows area and amount in the Values area "
            "would show the total amount for each city. In cell F1, write a formula "
            "that returns the total amount for Lagos orders \u2014 the value that would "
            "appear in the Lagos row of that PivotTable. Use SUMIF with the city range "
            "B2:B21, the criterion \"Lagos\", and the amount range D2:D21."
        )
        new_prompt = (
            "A PivotTable with city in the Rows area and amount in the Values area "
            "would show the total amount for each city. In cell F1, write a formula "
            "that returns the total amount for Lagos orders \u2014 the value that would "
            "appear in the Lagos row of that PivotTable. Use SUMIF with the city range "
            "B2:B21, the criterion \"Lagos\", and the amount range D2:D21. "
            "(Note: SUMIF was covered in the earlier Text, Date, and Conditional "
            "Aggregation lesson.)"
        )
        if item["interaction"]["public"]["prompt"] == old_prompt:
            item["interaction"]["public"]["prompt"] = new_prompt
            changed = True
            print("Patched s06 prompt.")
        else:
            # Prompt text differs from expected — patch by appending note if not present
            current = item["interaction"]["public"]["prompt"]
            note = "(Note: SUMIF was covered in the earlier Text, Date, and Conditional Aggregation lesson.)"
            if note not in current and "later lesson" not in current and "previewed here" not in current:
                item["interaction"]["public"]["prompt"] = current.rstrip() + " " + note
                changed = True
                print("Appended curriculum note to s06 prompt.")
            elif "later lesson" in current or "previewed here" in current:
                # Replace the incorrect note with the correct one
                import re
                # Remove any parenthetical about "later lesson" or "previewed here"
                current = re.sub(
                    r'\s*\(Note:[^)]*later lesson[^)]*\)',
                    '',
                    current
                )
                current = re.sub(
                    r'\s*\(SUMIF is previewed here[^)]*\)',
                    '',
                    current
                )
                current = current.rstrip() + " " + note
                item["interaction"]["public"]["prompt"] = current
                changed = True
                print("Replaced incorrect curriculum note in s06 prompt.")
            else:
                print("Note already present, no change needed.")

if not changed:
    print("WARNING: target interaction not found or already patched.")

with open(path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("Done.")
