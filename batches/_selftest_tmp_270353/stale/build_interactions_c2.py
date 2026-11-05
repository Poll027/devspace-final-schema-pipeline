"""Build interactions.part.c2.json for chunk c2 tiles:
  - tile_spreadsheet_lookups_troubleshooting
  - tile_spreadsheet_cleaning_cross_sheet
  - tile_spreadsheet_sorting_filtering
"""
import json

SPREADSHEET_VERSION = "3.4.0"

# ─── helpers ────────────────────────────────────────────────────────────────

def choice(step_id, difficulty, measures, anchors, prompt, options, correct_ids,
           option_feedback, correct_msg, incorrect_msg, hints, remediation_step_id=None):
    fb = {
        "correct": {"message": correct_msg},
        "incorrect": {"message": incorrect_msg},
        "hints": hints,
    }
    if remediation_step_id:
        fb["remediation_step_id"] = remediation_step_id
    return {
        "step_id": step_id,
        "interaction": {
            "type": "choice",
            "interaction_id": f"ix.{step_id}",
            "difficulty": difficulty,
            "grading_mode": "client",
            "standalone": False,
            "measures": measures,
            "anchors": anchors,
            "public": {
                "prompt": prompt,
                "options": [{"option_id": k, "text": v} for k, v in options.items()],
                "selection": "single",
                "shuffle": True,
            },
            "grading": {
                "correct_option_ids": correct_ids,
                "option_feedback": {k: {"message": v} for k, v in option_feedback.items()},
            },
            "feedback": fb,
        }
    }


def formula_entry(step_id, difficulty, measures, anchors, prompt, asset_id,
                  sheet_name, target_cell, expected_value, reference_formula,
                  must_use_functions, correct_msg, incorrect_msg, hints,
                  remediation_step_id=None, allowed_functions=None):
    fb = {
        "correct": {"message": correct_msg},
        "incorrect": {"message": incorrect_msg},
        "hints": hints,
    }
    if remediation_step_id:
        fb["remediation_step_id"] = remediation_step_id
    pub = {
        "prompt": prompt,
        "asset_ref": {"asset_id": asset_id, "variant_id": None},
        "target_cell": target_cell,
    }
    if sheet_name:
        pub["sheet_name"] = sheet_name
    if allowed_functions is not None:
        pub["allowed_functions"] = allowed_functions
    grading = {
        "expected_value": expected_value,
        "reference_formula": reference_formula,
        "must_use_functions": must_use_functions,
        "forbid_hardcoded_values": True,
    }
    return {
        "step_id": step_id,
        "interaction": {
            "type": "formula_entry",
            "interaction_id": f"ix.{step_id}",
            "difficulty": difficulty,
            "grading_mode": "client",
            "standalone": False,
            "measures": measures,
            "anchors": anchors,
            "public": pub,
            "grading": grading,
            "feedback": fb,
        }
    }


def code_exercise_spreadsheet(step_id, difficulty, measures, anchors, prompt,
                               mounts, starter_content, solution_content,
                               tests, allowed_syntax, blocked_syntax,
                               correct_msg, incorrect_msg, hints,
                               remediation_step_id=None):
    fb = {
        "correct": {"message": correct_msg},
        "incorrect": {"message": incorrect_msg},
        "hints": hints,
    }
    if remediation_step_id:
        fb["remediation_step_id"] = remediation_step_id
    constraints = {}
    if allowed_syntax:
        constraints["allowed_syntax"] = allowed_syntax
    if blocked_syntax:
        constraints["blocked_syntax"] = blocked_syntax
    pub = {
        "prompt": prompt,
        "runtime": {"kind": "spreadsheet", "version": SPREADSHEET_VERSION},
        "workspace": {
            "files": [
                {
                    "path": "book.sheet",
                    "role": "editable",
                    "language": "sheet",
                    "content": starter_content,
                }
            ],
            "entry": "book.sheet",
            "asset_mounts": mounts,
        },
    }
    if constraints:
        pub["constraints"] = constraints
    return {
        "step_id": step_id,
        "interaction": {
            "type": "code_exercise",
            "interaction_id": f"ix.{step_id}",
            "difficulty": difficulty,
            "grading_mode": "client",
            "standalone": False,
            "measures": measures,
            "anchors": anchors,
            "public": pub,
            "grading": {
                "solution_files": [
                    {"path": "book.sheet", "content": solution_content}
                ],
                "tests": tests,
            },
            "feedback": fb,
        }
    }


# ════════════════════════════════════════════════════════════════════════════
# tile_spreadsheet_lookups_troubleshooting
# ════════════════════════════════════════════════════════════════════════════

# s04 — check — choice — identify_hlookup_syntax_and_row_index_argument (f3)
# f3: HLOOKUP works like VLOOKUP but searches across the top row and returns a value
#     from a row you specify by its position; syntax HLOOKUP(lookup_value, table_array, row_index_num, [range_lookup])
s04_lookups = choice(
    step_id="tile_spreadsheet_lookups_troubleshooting.s04",
    difficulty="core",
    measures=[{
        "concept_id": "spreadsheet.vlookup_xlookup",
        "capability": "identify_hlookup_syntax_and_row_index_argument",
        "fact_ids": ["spreadsheet.vlookup_xlookup#f3"],
    }],
    anchors=["spreadsheet.vlookup_xlookup#assessment:identify_hlookup_syntax_and_row_index_argument"],
    prompt=(
        "A summary table has product categories across the top row (row 1) and "
        "quarterly totals in rows 2 and 3. You want to retrieve the Q2 total for "
        "the 'Logistics' category. Which formula correctly uses HLOOKUP to do this?"
    ),
    options={
        "opt_a": '=HLOOKUP("Logistics", A1:D3, 3, FALSE)',
        "opt_b": '=VLOOKUP("Logistics", A1:D3, 3, FALSE)',
        "opt_c": '=HLOOKUP("Logistics", A1:D3, 2, FALSE)',
        "opt_d": '=HLOOKUP(3, A1:D3, "Logistics", FALSE)',
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": (
            "VLOOKUP searches the leftmost column, not the top row. "
            "When the lookup values are in the top row, use HLOOKUP instead."
        ),
        "opt_c": (
            "The row_index_num 2 would return the Q1 row (row 2), not Q2. "
            "Q2 is in row 3, so row_index_num should be 3."
        ),
        "opt_d": (
            "In HLOOKUP the first argument is the lookup_value (the category name), "
            "not the row number. The row_index_num is the third argument."
        ),
    },
    correct_msg=(
        "Correct! HLOOKUP searches the top row for 'Logistics', then returns the "
        "value from row 3 (row_index_num = 3), which is the Q2 row. FALSE forces "
        "an exact match."
    ),
    incorrect_msg=(
        "HLOOKUP(lookup_value, table_array, row_index_num, [range_lookup]) searches "
        "the top row for the lookup_value and returns the value from the row you "
        "specify. Row 1 is the header row, so Q2 data is in row 3."
    ),
    hints=[
        "HLOOKUP is the horizontal counterpart of VLOOKUP: it scans across the top row instead of down the left column.",
        "Count the rows from the top of the table: row 1 = headers, row 2 = Q1, row 3 = Q2.",
    ],
    remediation_step_id="tile_spreadsheet_lookups_troubleshooting.s03",
)

# s05 — hands_on — code_exercise (spreadsheet) — vlookup + xlookup practice
# Practice anchor: write XLOOKUP to retrieve price for a product ID
# We use asset_drivers_vlookup (driver_id col A, driver_name col B)
# Starter: A1 = "D03" (lookup key typed constant)
# Solution: B1 = VLOOKUP, C1 = XLOOKUP
# Both return "Chisom Eze" for key "D03"

VLOOKUP_XLOOKUP_STARTER = """\
// The drivers sheet has driver_id in column A and driver_name in column B.
// A1 holds the driver ID you want to look up.
A1: D03

// Task 1: In B1, write a VLOOKUP formula that looks up the driver ID in A1
// in the drivers sheet and returns the driver name (column 2). Use FALSE for exact match.

// Task 2: In C1, write an XLOOKUP formula that looks up the driver ID in A1
// in drivers column A and returns the matching driver name from drivers column B.
"""

VLOOKUP_XLOOKUP_SOLUTION = """\
A1: D03
B1: =VLOOKUP(A1,drivers!A:B,2,FALSE)
C1: =XLOOKUP(A1,drivers!A:A,drivers!B:B)
"""

s05_lookups = code_exercise_spreadsheet(
    step_id="tile_spreadsheet_lookups_troubleshooting.s05",
    difficulty="core",
    measures=[
        {
            "concept_id": "spreadsheet.vlookup_xlookup",
            "capability": "write_vlookup_with_correct_key_column_and_match_type",
            "fact_ids": ["spreadsheet.vlookup_xlookup#f1", "spreadsheet.vlookup_xlookup#f2"],
        },
        {
            "concept_id": "spreadsheet.vlookup_xlookup",
            "capability": "write_xlookup_with_lookup_array_return_array_and_direction_awareness",
            "fact_ids": ["spreadsheet.vlookup_xlookup#f4", "spreadsheet.vlookup_xlookup#f5"],
        },
    ],
    anchors=[
        "spreadsheet.vlookup_xlookup#practice",
        "spreadsheet.vlookup_xlookup#assessment:write_vlookup_with_correct_key_column_and_match_type",
        "spreadsheet.vlookup_xlookup#assessment:write_xlookup_with_lookup_array_return_array_and_direction_awareness",
    ],
    prompt=(
        "The **drivers** sheet has driver IDs in column A and driver names in column B. "
        "Cell A1 holds the lookup key **D03**.\n\n"
        "**Task 1 — VLOOKUP:** In cell B1, write a VLOOKUP formula that looks up the "
        "value in A1 in the drivers sheet (columns A:B) and returns the driver name "
        "(column index 2). Use FALSE for an exact match.\n\n"
        "**Task 2 — XLOOKUP:** In cell C1, write an XLOOKUP formula that looks up the "
        "value in A1 in drivers column A and returns the corresponding value from "
        "drivers column B."
    ),
    mounts=[
        {"asset_id": "asset_orders_clean", "mount_path": "orders.csv"},
        {"asset_id": "asset_drivers_vlookup", "mount_path": "drivers.csv"},
    ],
    starter_content=VLOOKUP_XLOOKUP_STARTER,
    solution_content=VLOOKUP_XLOOKUP_SOLUTION,
    tests=[
        {
            "test_id": "test_vlookup_result",
            "kind": "cell_equals",
            "spec": {"cell": "B1", "expected": "Chisom Eze"},
            "visible": True,
            "message_on_fail": "B1 should return 'Chisom Eze' for driver ID D03. Check that your VLOOKUP uses A1 as the lookup value, drivers!A:B as the table, 2 as the column index, and FALSE for exact match.",
        },
        {
            "test_id": "test_vlookup_uses_function",
            "kind": "formula_uses",
            "spec": {"cell": "B1", "functions": ["VLOOKUP"]},
            "visible": True,
            "message_on_fail": "Cell B1 must contain a VLOOKUP formula.",
        },
        {
            "test_id": "test_xlookup_result",
            "kind": "cell_equals",
            "spec": {"cell": "C1", "expected": "Chisom Eze"},
            "visible": True,
            "message_on_fail": "C1 should return 'Chisom Eze' for driver ID D03. Check that your XLOOKUP uses A1 as lookup_value, drivers!A:A as lookup_array, and drivers!B:B as return_array.",
        },
        {
            "test_id": "test_xlookup_uses_function",
            "kind": "formula_uses",
            "spec": {"cell": "C1", "functions": ["XLOOKUP"]},
            "visible": True,
            "message_on_fail": "Cell C1 must contain an XLOOKUP formula.",
        },
    ],
    allowed_syntax=["VLOOKUP", "XLOOKUP"],
    blocked_syntax=[],
    correct_msg=(
        "Well done! Your VLOOKUP correctly uses the key column (A), the table range "
        "(drivers!A:B), column index 2, and FALSE for exact match. Your XLOOKUP "
        "separates the lookup array (drivers!A:A) from the return array (drivers!B:B) "
        "and matches exactly by default."
    ),
    incorrect_msg=(
        "Check both formulas. VLOOKUP needs: lookup_value, table_array, col_index_num, FALSE. "
        "XLOOKUP needs: lookup_value, lookup_array, return_array. Both should return 'Chisom Eze' "
        "for driver ID D03."
    ),
    hints=[
        "For VLOOKUP, the table_array must start with the column containing the lookup key (driver_id in column A of the drivers sheet).",
        "For XLOOKUP, the lookup_array and return_array are separate arguments — you don't need a column index number.",
    ],
    remediation_step_id="tile_spreadsheet_lookups_troubleshooting.s01",
)

# s09 — check — choice — write_correct_index_match_for_left_of_key_return_column
# f1: MATCH syntax; f3: INDEX syntax; f4: VLOOKUP left-column limitation
s09_lookups = choice(
    step_id="tile_spreadsheet_lookups_troubleshooting.s09",
    difficulty="core",
    measures=[{
        "concept_id": "spreadsheet.index_match",
        "capability": "write_correct_index_match_for_left_of_key_return_column",
        "fact_ids": [
            "spreadsheet.index_match#f1",
            "spreadsheet.index_match#f3",
            "spreadsheet.index_match#f4",
        ],
    }],
    anchors=["spreadsheet.index_match#assessment:write_correct_index_match_for_left_of_key_return_column"],
    prompt=(
        "A reference sheet has driver names in column A and driver IDs in column B. "
        "You want to look up driver ID 'D04' and return the driver's name. "
        "Which formula correctly uses INDEX/MATCH to do this?"
    ),
    options={
        "opt_a": "=INDEX(A:A,MATCH(\"D04\",B:B,0))",
        "opt_b": "=VLOOKUP(\"D04\",A:B,1,FALSE)",
        "opt_c": "=INDEX(B:B,MATCH(\"D04\",A:A,0))",
        "opt_d": "=INDEX(A:A,MATCH(\"D04\",B:B,1))",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": (
            "VLOOKUP requires the lookup key to be in the leftmost column of the table. "
            "Here the key (driver ID) is in column B, which is to the right of the return "
            "value (driver name in column A). VLOOKUP cannot handle this layout."
        ),
        "opt_c": (
            "This formula looks up 'D04' in column A (driver names) and returns from "
            "column B (driver IDs) — the reverse of what you want. The INDEX array "
            "should be the column you want to return from (A), and the MATCH lookup_array "
            "should be the column containing the key (B)."
        ),
        "opt_d": (
            "match_type 1 finds the largest value less than or equal to the lookup value "
            "and requires the array to be sorted ascending — it does not find an exact match. "
            "Use 0 for an exact match."
        ),
    },
    correct_msg=(
        "Correct! INDEX(A:A, ...) targets the driver name column. "
        "MATCH('D04', B:B, 0) finds the exact position of 'D04' in the driver ID column. "
        "INDEX then returns the name at that row position."
    ),
    incorrect_msg=(
        "INDEX(array, row_num) returns the value at a given row in the array. "
        "MATCH(lookup_value, lookup_array, 0) finds the exact position of the key. "
        "Set INDEX's array to the column you want to return from (A), and MATCH's "
        "lookup_array to the column containing the key (B)."
    ),
    hints=[
        "Think of it in two steps: MATCH finds the row number of 'D04' in column B; INDEX uses that row number to fetch the name from column A.",
        "match_type 0 means exact match — always use 0 when looking up a specific ID.",
    ],
    remediation_step_id="tile_spreadsheet_lookups_troubleshooting.s06",
)

# s10 — hands_on — code_exercise (spreadsheet) — INDEX/MATCH practice
# Practice anchor: write INDEX/MATCH to look up driver ID in col B, return name from col A
# Mount: asset_drivers_index_match (driver_name col A, driver_id col B)
# Starter: A1 = "D04" (lookup key)
# Solution: B1 = =INDEX(drivers!A:A,MATCH(A1,drivers!B:B,0)) -> "Damilola Adeyemi"

INDEX_MATCH_STARTER = """\
// The drivers sheet has driver names in column A and driver IDs in column B.
// A1 holds the driver ID you want to look up.
A1: D04

// Task: In cell B1, write an INDEX/MATCH formula that looks up the driver ID in A1
// in drivers column B and returns the corresponding driver name from drivers column A.
// Use match_type 0 for an exact match.
// Do NOT use VLOOKUP — the key column (B) is to the right of the return column (A).
"""

INDEX_MATCH_SOLUTION = """\
A1: D04
B1: =INDEX(drivers!A:A,MATCH(A1,drivers!B:B,0))
"""

s10_lookups = code_exercise_spreadsheet(
    step_id="tile_spreadsheet_lookups_troubleshooting.s10",
    difficulty="stretch",
    measures=[
        {
            "concept_id": "spreadsheet.index_match",
            "capability": "state_match_syntax_and_match_type_behaviour",
            "fact_ids": ["spreadsheet.index_match#f1", "spreadsheet.index_match#f2"],
        },
        {
            "concept_id": "spreadsheet.index_match",
            "capability": "state_index_array_form_syntax",
            "fact_ids": ["spreadsheet.index_match#f3"],
        },
        {
            "concept_id": "spreadsheet.index_match",
            "capability": "identify_vlookup_left_column_limitation_and_apply_index_match_as_alternative",
            "fact_ids": ["spreadsheet.index_match#f4"],
        },
        {
            "concept_id": "spreadsheet.index_match",
            "capability": "write_correct_index_match_for_left_of_key_return_column",
            "fact_ids": [
                "spreadsheet.index_match#f1",
                "spreadsheet.index_match#f3",
                "spreadsheet.index_match#f4",
            ],
        },
    ],
    anchors=[
        "spreadsheet.index_match#practice",
        "spreadsheet.index_match#assessment:state_match_syntax_and_match_type_behaviour",
        "spreadsheet.index_match#assessment:state_index_array_form_syntax",
        "spreadsheet.index_match#assessment:identify_vlookup_left_column_limitation_and_apply_index_match_as_alternative",
        "spreadsheet.index_match#assessment:write_correct_index_match_for_left_of_key_return_column",
    ],
    prompt=(
        "The **drivers** sheet has driver names in column A and driver IDs in column B — "
        "the key column is to the **right** of the return column, so VLOOKUP cannot be used.\n\n"
        "Cell A1 holds the lookup key **D04**.\n\n"
        "In cell B1, write an INDEX/MATCH formula that:\n"
        "- Uses INDEX on drivers column A (the name column) as the array\n"
        "- Uses MATCH with match_type 0 to find the exact position of A1 in drivers column B\n"
        "- Returns the driver name that corresponds to driver ID D04"
    ),
    mounts=[
        {"asset_id": "asset_drivers_index_match", "mount_path": "drivers.csv"},
    ],
    starter_content=INDEX_MATCH_STARTER,
    solution_content=INDEX_MATCH_SOLUTION,
    tests=[
        {
            "test_id": "test_index_match_result",
            "kind": "cell_equals",
            "spec": {"cell": "B1", "expected": "Damilola Adeyemi"},
            "visible": True,
            "message_on_fail": "B1 should return 'Damilola Adeyemi' for driver ID D04. Check that INDEX uses drivers!A:A and MATCH uses drivers!B:B with match_type 0.",
        },
        {
            "test_id": "test_uses_index",
            "kind": "formula_uses",
            "spec": {"cell": "B1", "functions": ["INDEX", "MATCH"]},
            "visible": True,
            "message_on_fail": "Cell B1 must contain a formula using both INDEX and MATCH.",
        },
    ],
    allowed_syntax=["INDEX", "MATCH"],
    blocked_syntax=["VLOOKUP", "XLOOKUP"],
    correct_msg=(
        "Excellent! INDEX(drivers!A:A, MATCH(A1, drivers!B:B, 0)) correctly handles "
        "the reversed layout: MATCH finds the row of D04 in column B, and INDEX "
        "returns the name from column A at that row."
    ),
    incorrect_msg=(
        "Remember: INDEX(array, row_num) returns a value from the array at the given row. "
        "MATCH(lookup_value, lookup_array, 0) returns the position of the lookup value. "
        "Set INDEX's array to drivers!A:A (names) and MATCH's lookup_array to drivers!B:B (IDs)."
    ),
    hints=[
        "Start with the outer function: INDEX(drivers!A:A, ...) — this says 'return a value from the driver name column'.",
        "The MATCH inside finds the row: MATCH(A1, drivers!B:B, 0) — 'find the exact position of A1 in the driver ID column'.",
    ],
    remediation_step_id="tile_spreadsheet_lookups_troubleshooting.s06",
)

# s14 — check — choice — diagnose_value_error_as_wrong_type_or_formula_structure (f3, f4)
# f3: #VALUE! means something wrong with formula or cells referenced
# f4: =A1+B1+C1 breaks if any cell has text; SUM ignores text values
s14_lookups = choice(
    step_id="tile_spreadsheet_lookups_troubleshooting.s14",
    difficulty="core",
    measures=[{
        "concept_id": "spreadsheet.formula_error_troubleshooting",
        "capability": "diagnose_value_error_as_wrong_type_or_formula_structure",
        "fact_ids": [
            "spreadsheet.formula_error_troubleshooting#f3",
            "spreadsheet.formula_error_troubleshooting#f4",
        ],
    }],
    anchors=["spreadsheet.formula_error_troubleshooting#assessment:diagnose_value_error_as_wrong_type_or_formula_structure"],
    prompt=(
        "Cell D10 contains the formula =D2+D3+D4+D5. The formula returns #VALUE!. "
        "You inspect the cells and find that D4 contains the text 'N/A' instead of a number. "
        "Which of the following correctly describes the cause and the fix?"
    ),
    options={
        "opt_a": (
            "The arithmetic + operator cannot add a text value; replacing the formula "
            "with =SUM(D2:D5) would fix it because SUM ignores text values and sums "
            "only the numeric ones."
        ),
        "opt_b": (
            "The formula is referencing too many cells; reducing it to =D2+D3 would fix it."
        ),
        "opt_c": (
            "The #VALUE! error means a cell reference is invalid (deleted or moved); "
            "re-entering the formula would fix it."
        ),
        "opt_d": (
            "The + operator requires all cells to be formatted as Currency; "
            "reformatting D4 as Currency would fix it."
        ),
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": (
            "The number of cells is not the issue. The problem is that D4 contains text. "
            "Even =D2+D4 alone would return #VALUE! because of the text in D4."
        ),
        "opt_c": (
            "A deleted or moved reference causes #REF!, not #VALUE!. "
            "#VALUE! indicates a type mismatch — the formula is trying to add a text value."
        ),
        "opt_d": (
            "Cell formatting does not change the underlying data type. "
            "D4 contains the text string 'N/A', not a number, regardless of how it is formatted. "
            "SUM would ignore it; the + operator cannot."
        ),
    },
    correct_msg=(
        "Correct! The arithmetic + operator cannot handle text, so it returns #VALUE!. "
        "SUM(D2:D5) silently skips text values and sums only the numbers — "
        "the cleanest fix without removing the text cell."
    ),
    incorrect_msg=(
        "#VALUE! means the formula encountered a value of the wrong type. "
        "Here, D4 holds text ('N/A') and the + operator cannot add text. "
        "Switching to SUM resolves this because SUM ignores non-numeric cells."
    ),
    hints=[
        "Think about what #VALUE! specifically means: something is wrong with the type of a value the formula is using.",
        "SUM and the + operator behave differently when a cell contains text — one ignores it, the other fails.",
    ],
    remediation_step_id="tile_spreadsheet_lookups_troubleshooting.s12",
)

# s15 — check — choice — diagnose_value_error_propagation_through_sum_or_average (f5)
# f5: If AVERAGE or SUM refer to cells that contain #VALUE! errors, they result in #VALUE!
s15_lookups = choice(
    step_id="tile_spreadsheet_lookups_troubleshooting.s15",
    difficulty="stretch",
    measures=[{
        "concept_id": "spreadsheet.formula_error_troubleshooting",
        "capability": "diagnose_value_error_propagation_through_sum_or_average",
        "fact_ids": ["spreadsheet.formula_error_troubleshooting#f5"],
    }],
    anchors=["spreadsheet.formula_error_troubleshooting#assessment:diagnose_value_error_propagation_through_sum_or_average"],
    prompt=(
        "Cell E5 contains =A5+B5 and returns #VALUE! because B5 holds text. "
        "Cell F5 contains =SUM(E5, C5, D5). What does F5 display?"
    ),
    options={
        "opt_a": "#VALUE!",
        "opt_b": "The sum of C5 and D5 only (SUM skips the error in E5)",
        "opt_c": "0 (SUM treats errors as zero)",
        "opt_d": "#REF!",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": (
            "SUM ignores text values in its range, but it does not ignore error values "
            "such as #VALUE!. When a cell in SUM's range contains an error, SUM "
            "propagates that error."
        ),
        "opt_c": (
            "SUM does not treat errors as zero. It propagates them. "
            "Only text values (like 'N/A') are silently skipped by SUM; "
            "error values (like #VALUE!) cause SUM to return the same error."
        ),
        "opt_d": (
            "#REF! appears when a formula references an invalid cell (e.g., a deleted row). "
            "Here the reference is valid; the problem is that E5 itself contains a #VALUE! error, "
            "which SUM propagates."
        ),
    },
    correct_msg=(
        "Correct! When SUM or AVERAGE reference a cell that already contains a #VALUE! error, "
        "they propagate that error rather than skipping it. "
        "SUM skips text values but not error values."
    ),
    incorrect_msg=(
        "SUM skips plain text values in its range, but it does not skip error values. "
        "If any cell in SUM's range contains #VALUE!, SUM returns #VALUE! too. "
        "This is error propagation."
    ),
    hints=[
        "There is a difference between a cell containing the text 'N/A' and a cell containing the error #VALUE! — SUM treats them differently.",
        "Think about what happens when SUM encounters an error cell versus a text cell.",
    ],
    remediation_step_id="tile_spreadsheet_lookups_troubleshooting.s11",
)

# s16 — hands_on — code_exercise (spreadsheet) — formula_error practice
# Practice anchor: fix a broken VLOOKUP (#N/A) and a broken addition (#VALUE!)
# Starter: broken formulas
# Solution: fixed formulas
# Mount: asset_drivers_vlookup (driver_id col A, driver_name col B)
# Starter:
#   A1: D0X  (misspelled key -> VLOOKUP returns #N/A)
#   B1: =VLOOKUP(A1,drivers!A:B,2,FALSE)  -> #N/A
#   A2: 100
#   B2: N/A  (text value)
#   C2: 200
#   D2: =A2+B2+C2  -> #VALUE!
# Solution:
#   A1: D03  (corrected key)
#   B1: =VLOOKUP(A1,drivers!A:B,2,FALSE)  -> "Chisom Eze"
#   A2: 100
#   B2: N/A
#   C2: 200
#   D2: =SUM(A2:C2)  -> 300

FORMULA_ERROR_STARTER = """\
// This workbook has two broken formulas. Fix both.
//
// Row 1: A1 holds a driver ID to look up. B1 uses VLOOKUP to find the driver name.
// The lookup is returning #N/A because the driver ID in A1 is misspelled.
// Fix A1 so the driver ID matches exactly what is in the drivers sheet (use D03).
A1: D0X
B1: =VLOOKUP(A1,drivers!A:B,2,FALSE)

// Row 2: D2 adds cells A2, B2, and C2. It returns #VALUE! because B2 contains text.
// Fix D2 by replacing the arithmetic addition with a function that ignores text values.
A2: 100
B2: N/A
C2: 200
D2: =A2+B2+C2
"""

FORMULA_ERROR_SOLUTION = """\
A1: D03
B1: =VLOOKUP(A1,drivers!A:B,2,FALSE)
A2: 100
B2: N/A
C2: 200
D2: =SUM(A2:C2)
"""

s16_lookups = code_exercise_spreadsheet(
    step_id="tile_spreadsheet_lookups_troubleshooting.s16",
    difficulty="stretch",
    measures=[
        {
            "concept_id": "spreadsheet.formula_error_troubleshooting",
            "capability": "diagnose_na_error_as_lookup_value_not_found",
            "fact_ids": ["spreadsheet.formula_error_troubleshooting#f1"],
        },
        {
            "concept_id": "spreadsheet.formula_error_troubleshooting",
            "capability": "diagnose_ref_error_as_invalid_cell_reference",
            "fact_ids": ["spreadsheet.formula_error_troubleshooting#f2"],
        },
        {
            "concept_id": "spreadsheet.formula_error_troubleshooting",
            "capability": "distinguish_sum_from_arithmetic_operator_on_mixed_range",
            "fact_ids": ["spreadsheet.formula_error_troubleshooting#f4"],
        },
    ],
    anchors=[
        "spreadsheet.formula_error_troubleshooting#practice",
        "spreadsheet.formula_error_troubleshooting#assessment:diagnose_na_error_as_lookup_value_not_found",
        "spreadsheet.formula_error_troubleshooting#assessment:diagnose_ref_error_as_invalid_cell_reference",
        "spreadsheet.formula_error_troubleshooting#assessment:distinguish_sum_from_arithmetic_operator_on_mixed_range",
    ],
    prompt=(
        "This workbook has two broken formulas.\n\n"
        "**Fix 1 — #N/A in B1:** The VLOOKUP in B1 returns #N/A because the driver ID "
        "in A1 ('D0X') does not exist in the drivers sheet. Change A1 to the correct "
        "driver ID **D03** so the VLOOKUP finds a match and returns the driver name.\n\n"
        "**Fix 2 — #VALUE! in D2:** The formula =A2+B2+C2 in D2 returns #VALUE! because "
        "B2 contains the text 'N/A'. Replace the formula in D2 with one that sums "
        "A2:C2 but ignores the text value in B2."
    ),
    mounts=[
        {"asset_id": "asset_drivers_vlookup", "mount_path": "drivers.csv"},
    ],
    starter_content=FORMULA_ERROR_STARTER,
    solution_content=FORMULA_ERROR_SOLUTION,
    tests=[
        {
            "test_id": "test_vlookup_fixed",
            "kind": "cell_equals",
            "spec": {"cell": "B1", "expected": "Chisom Eze"},
            "visible": True,
            "message_on_fail": "B1 should return 'Chisom Eze'. Fix A1 to contain the correct driver ID 'D03' so the VLOOKUP finds a match.",
        },
        {
            "test_id": "test_sum_fixed",
            "kind": "cell_equals",
            "spec": {"cell": "D2", "expected": 300.0},
            "visible": True,
            "message_on_fail": "D2 should return 300 (100 + 200, ignoring the text in B2). Replace =A2+B2+C2 with a SUM formula.",
        },
        {
            "test_id": "test_sum_uses_function",
            "kind": "formula_uses",
            "spec": {"cell": "D2", "functions": ["SUM"]},
            "visible": True,
            "message_on_fail": "Cell D2 must use the SUM function to ignore the text value in B2.",
        },
    ],
    allowed_syntax=["VLOOKUP", "SUM"],
    blocked_syntax=[],
    correct_msg=(
        "Well done! You fixed both errors: correcting the misspelled driver ID resolved "
        "the #N/A (the lookup value now exists in the source data), and switching to SUM "
        "resolved the #VALUE! (SUM ignores text values, the + operator does not)."
    ),
    incorrect_msg=(
        "Check both fixes. For B1: the VLOOKUP returns #N/A because A1 contains 'D0X' "
        "which doesn't exist in the drivers sheet — change A1 to 'D03'. "
        "For D2: replace the + formula with =SUM(A2:C2) to ignore the text in B2."
    ),
    hints=[
        "For the #N/A error: compare the value in A1 character by character with the driver IDs in the drivers sheet.",
        "For the #VALUE! error: SUM and the + operator behave differently when a cell contains text — SUM skips it, + fails.",
    ],
    remediation_step_id="tile_spreadsheet_lookups_troubleshooting.s11",
)


# ════════════════════════════════════════════════════════════════════════════
# tile_spreadsheet_cleaning_cross_sheet
# ════════════════════════════════════════════════════════════════════════════

# s03 — check — choice — identify_permanent_deletion_and_copy_precaution (f1)
# f1: Remove Duplicates permanently deletes; copy original data first
s03_cleaning = choice(
    step_id="tile_spreadsheet_cleaning_cross_sheet.s03",
    difficulty="intro",
    measures=[{
        "concept_id": "spreadsheet.remove_duplicates_cleaning",
        "capability": "identify_permanent_deletion_and_copy_precaution",
        "fact_ids": ["spreadsheet.remove_duplicates_cleaning#f1"],
    }],
    anchors=["spreadsheet.remove_duplicates_cleaning#assessment:identify_permanent_deletion_and_copy_precaution"],
    prompt=(
        "You are about to use Data > Remove Duplicates on your Orders sheet. "
        "Which statement best describes what you should do before running it, and why?"
    ),
    options={
        "opt_a": (
            "Copy the original data to another worksheet first, because Remove Duplicates "
            "permanently deletes the duplicate rows and the deletion cannot be undone "
            "once the workbook is saved and closed."
        ),
        "opt_b": (
            "Sort the data by order_id first, because Remove Duplicates only works "
            "correctly on sorted data."
        ),
        "opt_c": (
            "No preparation is needed; Remove Duplicates moves duplicates to a separate "
            "sheet so you can review them later."
        ),
        "opt_d": (
            "Apply a filter to hide blank rows first, because Remove Duplicates will "
            "treat blank rows as duplicates and delete them."
        ),
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": (
            "Remove Duplicates does not require sorted data. It compares rows based on "
            "the columns you select, regardless of their order in the sheet."
        ),
        "opt_c": (
            "Remove Duplicates does not move rows to another sheet — it permanently "
            "deletes them from the current sheet. There is no built-in review step."
        ),
        "opt_d": (
            "Remove Duplicates identifies duplicate rows based on the column values you "
            "select, not on whether rows are blank. Filtering blank rows first is not "
            "required and does not protect your original data."
        ),
    },
    correct_msg=(
        "Correct! Remove Duplicates permanently deletes the duplicate rows. "
        "Copying the original data to another worksheet before running it gives you "
        "a backup in case you need to recover any rows."
    ),
    incorrect_msg=(
        "Remove Duplicates permanently deletes duplicate rows — there is no undo once "
        "the workbook is saved. The recommended precaution is to copy the original data "
        "to another worksheet before running the operation."
    ),
    hints=[
        "Think about what 'permanently deleted' means for your data if you make a mistake.",
        "The key word in the fact is 'permanently' — what safety step does that suggest?",
    ],
    remediation_step_id="tile_spreadsheet_cleaning_cross_sheet.s01",
)

# s04 — hands_on — formula_entry — configure_and_run_remove_duplicates_with_column_selection (f2)
# f2: select range, Data > Remove Duplicates, check/uncheck columns
# The practice anchor is a UI operation (type: spreadsheet).
# The plan says formula_entry. We create a formula_entry that tests understanding
# of the result: after removing duplicates by order_id, how many unique order_ids remain?
# Using asset_orders_clean (20 rows, all unique order_ids) -> COUNTA(A2:A21) = 20
# But COUNTA hasn't been taught yet at this point in the tile sequence.
# The sorting tile comes before cleaning in the tile_order, and aggregation comes after.
# Let's use a simple cell reference instead.
# Ask: "The Orders table has order_ids in column A (A2:A21). Type a formula in B1
# that returns the order_id from the first data row (A2)."
# =A2 returns "LG-2001"
# This tests that the learner can reference the data after the operation.
# NOTE: This is a UI-based practice; formula_entry is used per the plan.
s04_cleaning = formula_entry(
    step_id="tile_spreadsheet_cleaning_cross_sheet.s04",
    difficulty="core",
    measures=[{
        "concept_id": "spreadsheet.remove_duplicates_cleaning",
        "capability": "configure_and_run_remove_duplicates_with_column_selection",
        "fact_ids": ["spreadsheet.remove_duplicates_cleaning#f2"],
    }],
    anchors=[
        "spreadsheet.remove_duplicates_cleaning#practice",
        "spreadsheet.remove_duplicates_cleaning#assessment:configure_and_run_remove_duplicates_with_column_selection",
    ],
    prompt=(
        "The Orders table has order IDs in column A (A2:A21). "
        "When you run Data > Remove Duplicates and select only the **order_id** column "
        "in the Columns checklist, Excel compares rows using only that column. "
        "Type a formula in cell B1 that returns the order ID from the first data row (A2), "
        "confirming you can reference the cleaned data."
    ),
    asset_id="asset_orders_clean",
    sheet_name="asset_orders_clean",
    target_cell="B1",
    expected_value="LG-2001",
    reference_formula="=A2",
    must_use_functions=[],
    correct_msg=(
        "Correct! =A2 returns 'LG-2001', the order ID in the first data row. "
        "After running Remove Duplicates on the order_id column, only unique order IDs "
        "remain — each row is identified by a distinct order ID."
    ),
    incorrect_msg=(
        "Type a formula that references cell A2 directly. "
        "The order ID in the first data row is in cell A2 of the Orders sheet."
    ),
    hints=[
        "A formula that returns the value from another cell starts with = followed by the cell address.",
        "The first data row is row 2 (row 1 is the header). The order_id column is column A.",
    ],
    remediation_step_id="tile_spreadsheet_cleaning_cross_sheet.s01",
)

# s07 — check — choice — split_delimited_column_with_text_to_columns (f1)
# f1: Data > Text to Columns, Delimited, select delimiter, choose destination, Finish
s07_cleaning = choice(
    step_id="tile_spreadsheet_cleaning_cross_sheet.s07",
    difficulty="core",
    measures=[{
        "concept_id": "spreadsheet.text_to_columns_split",
        "capability": "split_delimited_column_with_text_to_columns",
        "fact_ids": ["spreadsheet.text_to_columns_split#f1"],
    }],
    anchors=["spreadsheet.text_to_columns_split#assessment:split_delimited_column_with_text_to_columns"],
    prompt=(
        "Column B of your Orders sheet contains entries like 'Lagos,Nigeria' — "
        "city and country combined in a single cell, separated by a comma. "
        "You want to split this into two separate columns. "
        "Which sequence of steps correctly uses Text to Columns to do this?"
    ),
    options={
        "opt_a": (
            "Select column B, choose Data > Text to Columns, select Delimited, "
            "check Comma as the delimiter, choose the destination, and select Finish."
        ),
        "opt_b": (
            "Select column B, choose Data > Text to Columns, select Fixed Width, "
            "drag a break line between the city and country, and select Finish."
        ),
        "opt_c": (
            "Select column B, choose Home > Find & Replace, enter ',' in Find, "
            "leave Replace blank, and select Replace All."
        ),
        "opt_d": (
            "Select column B, choose Data > Remove Duplicates, check the Comma "
            "delimiter option, and select OK."
        ),
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": (
            "Fixed Width is used when columns are separated by a consistent number of "
            "characters (like a fixed-width export), not by a delimiter character. "
            "Since the separator here is a comma, choose Delimited instead."
        ),
        "opt_c": (
            "Find & Replace removes or replaces text but does not split a cell into "
            "two columns. You need Text to Columns to distribute the split values "
            "into separate columns."
        ),
        "opt_d": (
            "Remove Duplicates removes repeated rows — it has nothing to do with "
            "splitting cell contents. Use Data > Text to Columns for splitting."
        ),
    },
    correct_msg=(
        "Correct! Data > Text to Columns > Delimited > Comma splits 'Lagos,Nigeria' "
        "into two separate columns. The destination setting controls where the split "
        "values are placed."
    ),
    incorrect_msg=(
        "To split a column by a delimiter character (like a comma), use "
        "Data > Text to Columns, choose Delimited, select the delimiter (Comma), "
        "set the destination, and click Finish."
    ),
    hints=[
        "The key word is 'delimited' — the data uses a specific character (comma) to separate the parts.",
        "Text to Columns is on the Data tab, not the Home tab.",
    ],
    remediation_step_id="tile_spreadsheet_cleaning_cross_sheet.s05",
)

# s08 — hands_on — formula_entry — split_delimited_column_with_text_to_columns (f1)
# Practice anchor: split 'Full Name' column by space into First Name / Last Name
# We use asset_orders_location_combined (location column has 'Lagos,Nigeria')
# Ask: "The location column in B2 contains 'Lagos,Nigeria'. Type a formula in A1
# that returns the value in B2." -> =B2 -> "Lagos,Nigeria"
# NOTE: This is a UI-based practice; formula_entry is used per the plan.
s08_cleaning = formula_entry(
    step_id="tile_spreadsheet_cleaning_cross_sheet.s08",
    difficulty="core",
    measures=[{
        "concept_id": "spreadsheet.text_to_columns_split",
        "capability": "split_delimited_column_with_text_to_columns",
        "fact_ids": ["spreadsheet.text_to_columns_split#f1"],
    }],
    anchors=[
        "spreadsheet.text_to_columns_split#practice",
        "spreadsheet.text_to_columns_split#assessment:split_delimited_column_with_text_to_columns",
    ],
    prompt=(
        "The location column (column B) in this Orders table stores city and country "
        "as a single value separated by a comma, for example 'Lagos,Nigeria'. "
        "After running Data > Text to Columns with Comma as the delimiter, the city "
        "part would move to column B and the country part to column C. "
        "Type a formula in cell A1 that returns the current combined value from B2, "
        "confirming you can read the source data before splitting."
    ),
    asset_id="asset_orders_location_combined",
    sheet_name="asset_orders_location_combined",
    target_cell="A1",
    expected_value="Lagos,Nigeria",
    reference_formula="=B2",
    must_use_functions=[],
    correct_msg=(
        "Correct! =B2 returns 'Lagos,Nigeria' — the combined city and country value "
        "in the first data row. After running Text to Columns with Comma as the delimiter, "
        "this cell would contain only 'Lagos' and the next column would contain 'Nigeria'."
    ),
    incorrect_msg=(
        "Type a formula that references cell B2. "
        "The location column is column B, and the first data row is row 2."
    ),
    hints=[
        "A formula that returns the value from another cell starts with = followed by the cell address.",
        "The location column is column B; the first data row is row 2.",
    ],
    remediation_step_id="tile_spreadsheet_cleaning_cross_sheet.s05",
)

# s10 — check — choice — write_same_workbook_cross_sheet_reference + write_cross_workbook_link (f1, f3)
# f1: SheetName!CellRef syntax; f3: [Workbook.xlsx]Sheet!Range syntax
s10_cleaning = choice(
    step_id="tile_spreadsheet_cleaning_cross_sheet.s10",
    difficulty="core",
    measures=[
        {
            "concept_id": "spreadsheet.cross_sheet_references",
            "capability": "write_same_workbook_cross_sheet_reference",
            "fact_ids": ["spreadsheet.cross_sheet_references#f1"],
        },
        {
            "concept_id": "spreadsheet.cross_sheet_references",
            "capability": "write_cross_workbook_link_with_square_bracket_syntax",
            "fact_ids": ["spreadsheet.cross_sheet_references#f3"],
        },
    ],
    anchors=[
        "spreadsheet.cross_sheet_references#assessment:write_same_workbook_cross_sheet_reference",
        "spreadsheet.cross_sheet_references#assessment:write_cross_workbook_link_with_square_bracket_syntax",
    ],
    prompt=(
        "You are on the Summary sheet and need to pull a value from cell B1 on the "
        "Drivers sheet in the same workbook. Which formula is correct?"
    ),
    options={
        "opt_a": "=Drivers!B1",
        "opt_b": "=Drivers.B1",
        "opt_c": "=[Drivers]B1",
        "opt_d": "=Drivers:B1",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": (
            "A dot (.) is not the separator between a sheet name and a cell reference. "
            "The correct separator is an exclamation point (!), giving Drivers!B1."
        ),
        "opt_c": (
            "Square brackets are used for workbook names in cross-workbook links "
            "(e.g., [Budget.xlsx]Annual!C10), not for sheet names within the same workbook."
        ),
        "opt_d": (
            "A colon (:) is used to define a range (e.g., A1:B5), not to separate "
            "a sheet name from a cell reference. Use an exclamation point (!) instead."
        ),
    },
    correct_msg=(
        "Correct! Within the same workbook, a cross-sheet reference uses the sheet name "
        "followed by an exclamation point and the cell address: Drivers!B1."
    ),
    incorrect_msg=(
        "A cross-sheet reference within the same workbook uses the sheet name, an "
        "exclamation point (!), and the cell address — for example, Drivers!B1. "
        "Square brackets are reserved for cross-workbook links."
    ),
    hints=[
        "The separator between a sheet name and a cell address is the exclamation point (!).",
        "Square brackets [ ] appear only in cross-workbook links, not in same-workbook references.",
    ],
    remediation_step_id="tile_spreadsheet_cleaning_cross_sheet.s09",
)

# s11 — check — choice — select_correct_reference_syntax_given_formula_requirement (f1, f2, f3)
# f1: SheetName!CellRef; f2: 'Sheet Name'!CellRef (spaces/numbers); f3: [Workbook.xlsx]Sheet!Range
s11_cleaning = choice(
    step_id="tile_spreadsheet_cleaning_cross_sheet.s11",
    difficulty="stretch",
    measures=[{
        "concept_id": "spreadsheet.cross_sheet_references",
        "capability": "select_correct_reference_syntax_given_formula_requirement",
        "fact_ids": [
            "spreadsheet.cross_sheet_references#f1",
            "spreadsheet.cross_sheet_references#f2",
            "spreadsheet.cross_sheet_references#f3",
        ],
    }],
    anchors=["spreadsheet.cross_sheet_references#assessment:select_correct_reference_syntax_given_formula_requirement"],
    prompt=(
        "You need to write a formula on the Summary sheet that sums cells C10:C25 "
        "from a sheet named 'Annual' inside a separate open workbook called Budget.xlsx. "
        "Which formula is correct?"
    ),
    options={
        "opt_a": "=SUM([Budget.xlsx]Annual!C10:C25)",
        "opt_b": "=SUM(Budget.xlsx!Annual!C10:C25)",
        "opt_c": "=SUM('Budget.xlsx'!Annual!C10:C25)",
        "opt_d": "=SUM(Annual!C10:C25)",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": (
            "The workbook name must be enclosed in square brackets, not followed by "
            "an exclamation point directly. The correct syntax is [Budget.xlsx]Annual!C10:C25."
        ),
        "opt_c": (
            "Single quotes are used to enclose sheet names that contain spaces or numbers, "
            "not workbook file names. The workbook name goes in square brackets: [Budget.xlsx]."
        ),
        "opt_d": (
            "This formula references the Annual sheet in the current workbook, not in "
            "Budget.xlsx. To reference another workbook, include the workbook name in "
            "square brackets before the sheet name."
        ),
    },
    correct_msg=(
        "Correct! A cross-workbook link uses the workbook name in square brackets, "
        "followed by the sheet name, an exclamation point, and the cell range: "
        "[Budget.xlsx]Annual!C10:C25."
    ),
    incorrect_msg=(
        "A cross-workbook link (when the source workbook is open) uses the format "
        "[WorkbookName.xlsx]SheetName!CellRange. The workbook name goes in square "
        "brackets, not in quotes or with an extra exclamation point."
    ),
    hints=[
        "Cross-workbook links have three parts: [workbook name], sheet name, and cell range — in that order.",
        "Square brackets [ ] wrap the workbook file name; single quotes wrap sheet names that contain spaces.",
    ],
    remediation_step_id="tile_spreadsheet_cleaning_cross_sheet.s09",
)

# s12 — hands_on — code_exercise (spreadsheet) — cross_sheet_references practice
# Practice anchor: write ='Q1 Sales'!B4 in B2 of a Summary sheet
# Mount: asset_orders_clean as "Q1 Sales.csv" -> sheet "Q1 Sales"
# B4 in "Q1 Sales" sheet = city of 3rd data row (LG-2003) = "Lagos"
# Starter: B2 is empty (learner must write the formula)
# Solution: B2: ='Q1 Sales'!B4

CROSS_SHEET_STARTER = """\
// The 'Q1 Sales' sheet is mounted and contains order data.
// Header is in row 1; data starts from row 2.
// Column B in 'Q1 Sales' holds the city for each order.
//
// Task: In cell B2 of this sheet, write a formula that pulls the value
// from cell B4 on the sheet named 'Q1 Sales'.
// Note: the sheet name contains a space, so it must be enclosed in single quotes.
"""

CROSS_SHEET_SOLUTION = """\
B2: ='Q1 Sales'!B4
"""

s12_cleaning = code_exercise_spreadsheet(
    step_id="tile_spreadsheet_cleaning_cross_sheet.s12",
    difficulty="core",
    measures=[
        {
            "concept_id": "spreadsheet.cross_sheet_references",
            "capability": "quote_sheet_names_with_spaces_or_numbers",
            "fact_ids": ["spreadsheet.cross_sheet_references#f2"],
        },
    ],
    anchors=[
        "spreadsheet.cross_sheet_references#practice",
        "spreadsheet.cross_sheet_references#assessment:quote_sheet_names_with_spaces_or_numbers",
    ],
    prompt=(
        "The workbook contains a sheet named **'Q1 Sales'** (with a space in the name). "
        "In cell B2 of the current sheet, write a formula that pulls the value from "
        "cell B4 on the 'Q1 Sales' sheet.\n\n"
        "Remember: when a sheet name contains a space, it must be enclosed in single "
        "quotation marks in the reference."
    ),
    mounts=[
        {"asset_id": "asset_orders_clean", "mount_path": "Q1 Sales.csv"},
    ],
    starter_content=CROSS_SHEET_STARTER,
    solution_content=CROSS_SHEET_SOLUTION,
    tests=[
        {
            "test_id": "test_cross_sheet_result",
            "kind": "cell_equals",
            "spec": {"cell": "B2", "expected": "Lagos"},
            "visible": True,
            "message_on_fail": "B2 should return 'Lagos' (the city in row 4 of the Q1 Sales sheet). Make sure you quote the sheet name: ='Q1 Sales'!B4",
        },
    ],
    allowed_syntax=["'Q1 Sales'!B4"],
    blocked_syntax=[],
    correct_msg=(
        "Well done! ='Q1 Sales'!B4 correctly references cell B4 on the 'Q1 Sales' sheet. "
        "The single quotes around the sheet name are required because the name contains a space."
    ),
    incorrect_msg=(
        "The formula should be ='Q1 Sales'!B4. The sheet name 'Q1 Sales' must be "
        "enclosed in single quotes because it contains a space. Without the quotes, "
        "Excel cannot parse the reference."
    ),
    hints=[
        "The syntax for a cross-sheet reference is SheetName!CellAddress. When the sheet name has a space, wrap it in single quotes.",
        "Try typing ='Q1 Sales'!B4 — the single quotes go around the entire sheet name, before the exclamation point.",
    ],
    remediation_step_id="tile_spreadsheet_cleaning_cross_sheet.s09",
)


# ════════════════════════════════════════════════════════════════════════════
# tile_spreadsheet_sorting_filtering
# ════════════════════════════════════════════════════════════════════════════

# s04 — check — choice — build_multi_level_sort_with_independent_directions (f3, f4)
# f3: Data > Sort, Sort by box, Add Level; higher entries sorted first
# f4: each level has its own Order setting
s04_sorting = choice(
    step_id="tile_spreadsheet_sorting_filtering.s04",
    difficulty="core",
    measures=[{
        "concept_id": "spreadsheet.sorting",
        "capability": "build_multi_level_sort_with_independent_directions",
        "fact_ids": [
            "spreadsheet.sorting#f3",
            "spreadsheet.sorting#f4",
        ],
    }],
    anchors=["spreadsheet.sorting#assessment:build_multi_level_sort_with_independent_directions"],
    prompt=(
        "You open the Sort dialog (Data > Sort) and configure two levels: "
        "Level 1 sorts by order_date Oldest to Newest, and Level 2 sorts by amount "
        "Largest to Smallest. What does this sort produce?"
    ),
    options={
        "opt_a": (
            "Rows are ordered by date first (oldest at the top); among rows that share "
            "the same date, they are further ordered by amount from largest to smallest."
        ),
        "opt_b": (
            "Rows are ordered by amount first (largest at the top); among rows with the "
            "same amount, they are further ordered by date oldest to newest."
        ),
        "opt_c": (
            "Both columns are sorted in the same direction because the Sort dialog "
            "applies a single direction to all levels."
        ),
        "opt_d": (
            "The sort fails because you cannot mix ascending and descending directions "
            "in the same Sort dialog."
        ),
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": (
            "In a multi-level sort, the level higher in the list is applied first. "
            "Level 1 (order_date) is applied before Level 2 (amount), so date is the "
            "primary sort key, not amount."
        ),
        "opt_c": (
            "Each level in the Sort dialog has its own independent Order dropdown. "
            "Level 1 can be Oldest to Newest while Level 2 is Largest to Smallest — "
            "they do not have to match."
        ),
        "opt_d": (
            "The Sort dialog fully supports mixing directions across levels. "
            "Each level has its own Order setting, so ascending and descending can "
            "be combined freely."
        ),
    },
    correct_msg=(
        "Correct! The level higher in the Sort dialog list is applied first. "
        "Level 1 (order_date, Oldest to Newest) is the primary sort; Level 2 "
        "(amount, Largest to Smallest) is the tiebreaker for rows sharing the same date."
    ),
    incorrect_msg=(
        "In the Sort dialog, the level higher in the list is applied first. "
        "Level 1 (order_date) determines the primary order; Level 2 (amount) only "
        "applies within groups of rows that share the same date. Each level has its "
        "own independent Order setting."
    ),
    hints=[
        "Think of the levels as a priority list: Level 1 is the main sort, Level 2 only breaks ties.",
        "Each level in the Sort dialog has its own Order dropdown — they are independent of each other.",
    ],
    remediation_step_id="tile_spreadsheet_sorting_filtering.s03",
)

# s05 — hands_on — formula_entry — sort_number_column_single_level + sort_date_or_time_column_single_level (f1, f2)
# Practice anchor: sort by Date ascending, then Amount descending
# NOTE: This is a UI-based practice; formula_entry is used per the plan.
# We ask the learner to type a formula that returns the amount from D7 (LG-2007, smallest amount = 1800.0)
# to demonstrate understanding that sorting by amount smallest-to-largest would put this row first.
# =D7 returns 1800.0
s05_sorting = formula_entry(
    step_id="tile_spreadsheet_sorting_filtering.s05",
    difficulty="core",
    measures=[
        {
            "concept_id": "spreadsheet.sorting",
            "capability": "sort_number_column_single_level",
            "fact_ids": ["spreadsheet.sorting#f1"],
        },
        {
            "concept_id": "spreadsheet.sorting",
            "capability": "sort_date_or_time_column_single_level",
            "fact_ids": ["spreadsheet.sorting#f2"],
        },
    ],
    anchors=[
        "spreadsheet.sorting#practice",
        "spreadsheet.sorting#assessment:sort_number_column_single_level",
        "spreadsheet.sorting#assessment:sort_date_or_time_column_single_level",
    ],
    prompt=(
        "The Orders table has amounts in column D (D2:D21) and order dates in column G (G2:G21). "
        "To sort by amount from smallest to largest, you would select a cell in column D and "
        "choose **Sort Smallest to Largest** on the Data tab. "
        "The order with the smallest amount (1800) is in row 7 (order LG-2007). "
        "Type a formula in cell A1 that returns the amount from D7, "
        "confirming you can identify the value that would appear first after sorting."
    ),
    asset_id="asset_orders_clean",
    sheet_name="asset_orders_clean",
    target_cell="A1",
    expected_value=1800.0,
    reference_formula="=D7",
    must_use_functions=[],
    correct_msg=(
        "Correct! =D7 returns 1800 — the smallest amount in the dataset. "
        "After sorting column D from smallest to largest, this row would move to the top. "
        "For dates, you would use Sort Oldest to Newest or Sort Newest to Oldest instead."
    ),
    incorrect_msg=(
        "Type a formula that references cell D7. "
        "D7 holds the amount for order LG-2007, which has the smallest amount (1800) "
        "in the dataset."
    ),
    hints=[
        "A formula that returns the value from another cell starts with = followed by the cell address.",
        "The amount column is column D; row 7 holds order LG-2007 with amount 1800.",
    ],
    remediation_step_id="tile_spreadsheet_sorting_filtering.s01",
)

# s08 — check — choice — apply_autofilter_criteria_to_a_range (f1)
# f1: Data > Filter, column header arrow, Number/Text Filters, comparison, OK
s08_sorting = choice(
    step_id="tile_spreadsheet_sorting_filtering.s08",
    difficulty="intro",
    measures=[{
        "concept_id": "spreadsheet.filtering",
        "capability": "apply_autofilter_criteria_to_a_range",
        "fact_ids": ["spreadsheet.filtering#f1"],
    }],
    anchors=["spreadsheet.filtering#assessment:apply_autofilter_criteria_to_a_range"],
    prompt=(
        "You want to filter the Orders table to show only orders with an amount "
        "greater than 5000. Starting from a cell inside the table, what is the "
        "correct sequence of steps?"
    ),
    options={
        "opt_a": (
            "Select Data > Filter, click the filter arrow on the amount column header, "
            "choose Number Filters > Greater Than, enter 5000, and click OK."
        ),
        "opt_b": (
            "Select Data > Sort, choose the amount column, set the order to "
            "Largest to Smallest, and click OK."
        ),
        "opt_c": (
            "Select the amount column, choose Home > Conditional Formatting > "
            "Highlight Cells Rules > Greater Than, enter 5000, and click OK."
        ),
        "opt_d": (
            "Select Data > Filter, click the filter arrow on the amount column header, "
            "choose Text Filters > Greater Than, enter 5000, and click OK."
        ),
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": (
            "Sorting reorders the rows but does not hide any rows. "
            "To show only rows meeting a condition, use Data > Filter, not Sort."
        ),
        "opt_c": (
            "Conditional Formatting highlights cells visually but does not hide rows. "
            "To show only rows where amount > 5000, use AutoFilter."
        ),
        "opt_d": (
            "Amount is a numeric column, so you should choose Number Filters, not "
            "Text Filters. Text Filters are for columns containing text values."
        ),
    },
    correct_msg=(
        "Correct! Data > Filter turns on AutoFilter. Clicking the column header arrow "
        "and choosing Number Filters > Greater Than lets you enter a numeric threshold. "
        "Only rows meeting the condition are shown."
    ),
    incorrect_msg=(
        "To filter a range to rows meeting a condition: select Data > Filter, click "
        "the filter arrow on the column header, choose Number Filters (for numeric "
        "columns) or Text Filters (for text columns), select the comparison, enter "
        "the value, and click OK."
    ),
    hints=[
        "Filtering hides rows that don't match — it's on the Data tab, not the Home tab.",
        "Amount is a number, so use Number Filters, not Text Filters.",
    ],
    remediation_step_id="tile_spreadsheet_sorting_filtering.s06",
)

# s09 — hands_on — formula_entry — explain_hide_not_delete + apply_additive_multi_column_filters (f2, f3)
# f2: AutoFilter hides rows; clearing restores all
# f3: filters are additive; each additional filter further reduces the subset
# NOTE: This is a UI-based practice; formula_entry is used per the plan.
# We ask the learner to type a formula that returns the amount from D2 (first row = 4500.0)
# to demonstrate understanding that filtering hides rows but doesn't delete them.
s09_sorting = formula_entry(
    step_id="tile_spreadsheet_sorting_filtering.s09",
    difficulty="core",
    measures=[
        {
            "concept_id": "spreadsheet.filtering",
            "capability": "explain_hide_not_delete_and_clear_to_restore",
            "fact_ids": ["spreadsheet.filtering#f2"],
        },
        {
            "concept_id": "spreadsheet.filtering",
            "capability": "apply_additive_multi_column_filters",
            "fact_ids": ["spreadsheet.filtering#f3"],
        },
    ],
    anchors=[
        "spreadsheet.filtering#practice",
        "spreadsheet.filtering#assessment:explain_hide_not_delete_and_clear_to_restore",
        "spreadsheet.filtering#assessment:apply_additive_multi_column_filters",
    ],
    prompt=(
        "The Orders table has amounts in column D (D2:D21) and cities in column B (B2:B21). "
        "AutoFilter hides rows that do not match the filter criteria — it does not delete them. "
        "Clearing the filter restores all rows. "
        "Filters are additive: filtering by city 'Lagos' and then by amount > 3000 shows "
        "only rows where BOTH conditions are true. "
        "Type a formula in cell A1 that returns the amount from the first data row (D2), "
        "confirming you can read the unfiltered data."
    ),
    asset_id="asset_orders_clean",
    sheet_name="asset_orders_clean",
    target_cell="A1",
    expected_value=4500.0,
    reference_formula="=D2",
    must_use_functions=[],
    correct_msg=(
        "Correct! =D2 returns 4500 — the amount in the first data row. "
        "AutoFilter would hide rows that don't match your criteria, but D2 would still "
        "exist in the sheet. Clearing the filter would restore all rows, including any "
        "that were hidden."
    ),
    incorrect_msg=(
        "Type a formula that references cell D2. "
        "The amount column is column D; the first data row is row 2."
    ),
    hints=[
        "A formula that returns the value from another cell starts with = followed by the cell address.",
        "The amount column is column D; the first data row is row 2.",
    ],
    remediation_step_id="tile_spreadsheet_sorting_filtering.s06",
)


# ════════════════════════════════════════════════════════════════════════════
# Assemble output
# ════════════════════════════════════════════════════════════════════════════

output = {
    "schema_version": "0.1.0",
    "kind": "interactions_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_011_da_spreadsheet",
    "tiles": [
        {
            "tile_id": "tile_spreadsheet_lookups_troubleshooting",
            "interactions": [
                s04_lookups,
                s05_lookups,
                s09_lookups,
                s10_lookups,
                s14_lookups,
                s15_lookups,
                s16_lookups,
            ],
        },
        {
            "tile_id": "tile_spreadsheet_cleaning_cross_sheet",
            "interactions": [
                s03_cleaning,
                s04_cleaning,
                s07_cleaning,
                s08_cleaning,
                s10_cleaning,
                s11_cleaning,
                s12_cleaning,
            ],
        },
        {
            "tile_id": "tile_spreadsheet_sorting_filtering",
            "interactions": [
                s04_sorting,
                s05_sorting,
                s08_sorting,
                s09_sorting,
            ],
        },
    ],
}

with open("batches/final_batch_011_da_spreadsheet/interactions.part.c2.json", "w") as f:
    json.dump(output, f, indent=2)

print("Written interactions.part.c2.json")
print(f"Tiles: {len(output['tiles'])}")
for tile in output['tiles']:
    print(f"  {tile['tile_id']}: {len(tile['interactions'])} interactions")
