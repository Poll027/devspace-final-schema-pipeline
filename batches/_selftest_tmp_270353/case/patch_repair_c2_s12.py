#!/usr/bin/env python3
"""
Patch interactions.part.c2.json: fix tile_spreadsheet_cleaning_cross_sheet.s12.

Root cause: mount_path "Q1 Sales.csv" contains a space, which causes the
assembler's sandbox to generate a hidden_check with check_id
"hc_Q1 Sales.csv_drop_first_test_cross_sheet_result" — spaces are not
allowed by the id schema pattern ^[A-Za-z0-9][A-Za-z0-9_.:#-]*$.

Fix: change mount_path to "2024Q1.csv" (sheet name "2024Q1", starts with a
digit so it still requires single-quote quoting per fact f2), update the
prompt, starter, solution, and feedback to match.
"""
import json

PATH = "batches/final_batch_011_da_spreadsheet/interactions.part.c2.json"

with open(PATH) as f:
    data = json.load(f)

for tile in data["tiles"]:
    if tile["tile_id"] != "tile_spreadsheet_cleaning_cross_sheet":
        continue
    for entry in tile["interactions"]:
        if entry["step_id"] != "tile_spreadsheet_cleaning_cross_sheet.s12":
            continue
        ix = entry["interaction"]
        pub = ix["public"]
        gr = ix["grading"]

        # --- prompt ---
        pub["prompt"] = (
            "The workbook contains a sheet named **'2024Q1'** (the name starts with a number). "
            "In cell Z1 of the current sheet, write a formula that pulls the value from cell B4 on the '2024Q1' sheet.\n\n"
            "Remember: when a sheet name starts with a number (or contains a space), "
            "it must be enclosed in single quotation marks in the reference."
        )

        # --- starter file ---
        pub["workspace"]["files"][0]["content"] = (
            "// The '2024Q1' sheet is mounted and contains order data.\n"
            "// Header is in row 1; data starts from row 2.\n"
            "// Column B in '2024Q1' holds the city for each order.\n"
            "//\n"
            "// Task: In cell Z1 of this sheet, write a formula that pulls the value\n"
            "// from cell B4 on the sheet named '2024Q1'.\n"
            "// Note: the sheet name starts with a number, so it must be enclosed in single quotes.\n"
        )

        # --- mount_path: no spaces ---
        pub["workspace"]["asset_mounts"][0]["mount_path"] = "2024Q1.csv"

        # --- solution ---
        gr["solution_files"][0]["content"] = "Z1: ='2024Q1'!B4\n"

        # --- test: cell and expected unchanged (Z1, "Lagos") ---
        gr["tests"][0]["spec"]["cell"] = "Z1"
        gr["tests"][0]["spec"]["expected"] = "Lagos"
        gr["tests"][0]["message_on_fail"] = (
            "Z1 should return 'Lagos' (the city in row 4 of the 2024Q1 sheet). "
            "Make sure you quote the sheet name: ='2024Q1'!B4"
        )

        # --- feedback ---
        ix["feedback"]["correct"]["message"] = (
            "Well done! ='2024Q1'!B4 correctly references cell B4 on the '2024Q1' sheet. "
            "The single quotes around the sheet name are required because the name starts with a number."
        )
        ix["feedback"]["incorrect"]["message"] = (
            "The formula should be ='2024Q1'!B4. The sheet name '2024Q1' must be enclosed in single quotes "
            "because it starts with a number. Without the quotes, the spreadsheet cannot parse the reference."
        )
        ix["feedback"]["hints"][0] = (
            "The syntax for a cross-sheet reference is SheetName!CellAddress. "
            "When the sheet name starts with a number (or has a space), wrap it in single quotes."
        )
        ix["feedback"]["hints"][1] = (
            "Try typing ='2024Q1'!B4 — the single quotes go around the entire sheet name, before the exclamation point."
        )

        print("Patched tile_spreadsheet_cleaning_cross_sheet.s12")
        break
    break

with open(PATH, "w") as f:
    json.dump(data, f, indent=2)

print("Written:", PATH)
