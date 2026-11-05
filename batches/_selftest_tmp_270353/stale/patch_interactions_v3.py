"""
Final patch script for interactions.part.c1.json
Starts from .bak (which has the first patch's code_exercise for s05).
Reverts s05 to formula_entry, then applies all fixes.
"""
import json, copy

with open('batches/final_batch_011_da_spreadsheet/interactions.part.c1.json.bak') as f:
    data = json.load(f)

# ─────────────────────────────────────────────────────────────────────────────
# ADVISORY: tile_spreadsheet_formula_syntax_refs/s05
# Change title to "Which formula correctly sums the range D2:D21 on the Orders sheet?"
# ─────────────────────────────────────────────────────────────────────────────
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_formula_syntax_refs':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_spreadsheet_formula_syntax_refs.s05':
                ix['interaction']['public']['prompt'] = (
                    "Which formula correctly sums the range D2:D21 on the Orders sheet?\n\n"
                    "The Orders sheet has 20 rows of data in rows 2–21. You want to add up all the values "
                    "in the amount column (D2:D21) using the SUM function. Which formula is correctly structured?"
                )
                print("ADVISORY s05 formula_syntax: updated prompt title")

# ─────────────────────────────────────────────────────────────────────────────
# BLOCKING: tile_spreadsheet_aggregation_logical/s05
# The .bak has code_exercise (from first patch). Revert to formula_entry.
# Then remove the 3 extra anchors (apply_sum_to_a_range,
# apply_average_and_identify_ignored_values, apply_count_and_identify_what_is_excluded).
# ─────────────────────────────────────────────────────────────────────────────
ANCHORS_TO_MOVE = {
    'apply_sum_to_a_range',
    'apply_average_and_identify_ignored_values',
    'apply_count_and_identify_what_is_excluded',
}

for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_aggregation_logical':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_spreadsheet_aggregation_logical.s05':
                # Revert to formula_entry
                ix['interaction']['type'] = 'formula_entry'
                # Restore the original formula_entry public fields
                ix['interaction']['public'] = {
                    "prompt": (
                        "The Orders sheet has 20 rows of data (rows 2–21). Column A holds order IDs — "
                        "text values like \"LG-2001\". Column D holds order amounts — all numeric.\n\n"
                        "In cell H1, write a formula using **COUNTA** that counts how many non-empty cells "
                        "are in the order_id column (A2:A21). Because order IDs are text, COUNT would return "
                        "0 — COUNTA is the right choice here.\n\n"
                        "The expected result is **20**."
                    ),
                    "asset_ref": {
                        "asset_id": "asset_orders_clean",
                        "variant_id": None
                    },
                    "target_cell": "H1",
                    "allowed_functions": ["COUNTA"],
                    "sheet_name": "orders"
                }
                ix['interaction']['grading'] = {
                    "expected_value": 20,
                    "reference_formula": "=COUNTA(A2:A21)",
                    "must_use_functions": ["COUNTA"],
                    "forbid_hardcoded_values": True
                }
                ix['interaction']['feedback'] = {
                    "correct": {
                        "message": (
                            "Correct! =COUNTA(A2:A21) returns 20 because all 20 order-ID cells are non-empty. "
                            "COUNTA counts any non-empty cell — numbers, text, or errors — while COUNT counts "
                            "only numeric cells. Since order IDs are text, COUNT(A2:A21) would return 0."
                        )
                    },
                    "incorrect": {
                        "message": (
                            "Use =COUNTA(A2:A21). COUNTA counts every non-empty cell regardless of type, "
                            "so it correctly counts the 20 text order IDs. COUNT would return 0 here because "
                            "it only counts numeric cells."
                        )
                    },
                    "hints": [
                        "COUNTA counts cells that contain any value — numbers, text, or errors. COUNT counts only numbers.",
                        "The range A2:A21 covers all 20 data rows in column A (order_id)."
                    ],
                    "remediation_step_id": "tile_spreadsheet_aggregation_logical.r01"
                }
                # Remove the 3 extra anchors from measures
                ix['interaction']['measures'] = [
                    m for m in ix['interaction']['measures']
                    if m['capability'] not in ANCHORS_TO_MOVE
                ]
                # Remove the 3 extra anchors from anchors list
                ix['interaction']['anchors'] = [
                    a for a in ix['interaction']['anchors']
                    if not any(cap in a for cap in ANCHORS_TO_MOVE)
                ]
                print("BLOCKING s05 aggregation: reverted to formula_entry, removed 3 extra anchors")

# Add the 3 anchors to s04's measures
# s04 is a choice question that tests all 4 aggregation functions:
# - COUNT is the correct answer (tests apply_count_and_identify_what_is_excluded)
# - SUM is a distractor with feedback explaining what SUM does (tests apply_sum_to_a_range)
# - AVERAGE is a distractor with feedback explaining what AVERAGE does (tests apply_average_and_identify_ignored_values)
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_aggregation_logical':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_spreadsheet_aggregation_logical.s04':
                existing_caps = {m['capability'] for m in ix['interaction']['measures']}
                new_measures = [
                    {"concept_id": "spreadsheet.aggregation_functions",
                     "capability": "apply_sum_to_a_range",
                     "fact_ids": ["f1"]},
                    {"concept_id": "spreadsheet.aggregation_functions",
                     "capability": "apply_average_and_identify_ignored_values",
                     "fact_ids": ["f2"]},
                    {"concept_id": "spreadsheet.aggregation_functions",
                     "capability": "apply_count_and_identify_what_is_excluded",
                     "fact_ids": ["f3"]},
                ]
                for m in new_measures:
                    if m['capability'] not in existing_caps:
                        ix['interaction']['measures'].append(m)
                existing_anchors = set(ix['interaction']['anchors'])
                for cap in ['apply_sum_to_a_range', 'apply_average_and_identify_ignored_values',
                            'apply_count_and_identify_what_is_excluded']:
                    anchor = f"spreadsheet.aggregation_functions#assessment:{cap}"
                    if anchor not in existing_anchors:
                        ix['interaction']['anchors'].append(anchor)
                print("BLOCKING s04 aggregation: added 3 anchors to measures/anchors")

# ─────────────────────────────────────────────────────────────────────────────
# BLOCKING: tile_spreadsheet_text_date_conditional_agg/s05
# Remove apply_trim_to_remove_extraneous_whitespace from measures and anchors
# ─────────────────────────────────────────────────────────────────────────────
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_text_date_conditional_agg':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_spreadsheet_text_date_conditional_agg.s05':
                ix['interaction']['measures'] = [
                    m for m in ix['interaction']['measures']
                    if m['capability'] != 'apply_trim_to_remove_extraneous_whitespace'
                ]
                ix['interaction']['anchors'] = [
                    a for a in ix['interaction']['anchors']
                    if 'apply_trim_to_remove_extraneous_whitespace' not in a
                ]
                print("BLOCKING s05 text_date: removed TRIM anchor from measures/anchors")

# ─────────────────────────────────────────────────────────────────────────────
# BLOCKING: tile_spreadsheet_text_date_conditional_agg/s06
# Add apply_trim_to_remove_extraneous_whitespace to measures and anchors
# Also add apply_right_to_extract_trailing_characters (moved from s07)
# s06 MEASURES: select_correct_extraction_function_for_given_text_task(f1,f2,f3,f4)
#               + apply_trim_to_remove_extraneous_whitespace(f4)
#               + apply_right_to_extract_trailing_characters(f2)
# ─────────────────────────────────────────────────────────────────────────────
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_text_date_conditional_agg':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_spreadsheet_text_date_conditional_agg.s06':
                existing_caps = {m['capability'] for m in ix['interaction']['measures']}
                new_measures = [
                    {"concept_id": "spreadsheet.text_extraction",
                     "capability": "apply_trim_to_remove_extraneous_whitespace",
                     "fact_ids": ["f4"]},
                    {"concept_id": "spreadsheet.text_extraction",
                     "capability": "apply_right_to_extract_trailing_characters",
                     "fact_ids": ["f2"]},
                ]
                for m in new_measures:
                    if m['capability'] not in existing_caps:
                        ix['interaction']['measures'].append(m)
                existing_anchors = set(ix['interaction']['anchors'])
                for cap in ['apply_trim_to_remove_extraneous_whitespace',
                            'apply_right_to_extract_trailing_characters']:
                    anchor = f"spreadsheet.text_extraction#assessment:{cap}"
                    if anchor not in existing_anchors:
                        ix['interaction']['anchors'].append(anchor)
                print("BLOCKING s06 text_date: added TRIM and RIGHT anchors to measures/anchors")

# ─────────────────────────────────────────────────────────────────────────────
# BLOCKING: tile_spreadsheet_text_date_conditional_agg/s07
# Keep as formula_entry (plan enforces this).
# The .bak has code_exercise (from first patch). Revert to formula_entry.
# Change the formula from RIGHT to LEFT (so learner writes LEFT).
# Remove apply_right_to_extract_trailing_characters (moved to s06).
# ─────────────────────────────────────────────────────────────────────────────
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_text_date_conditional_agg':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_spreadsheet_text_date_conditional_agg.s07':
                # Revert to formula_entry
                ix['interaction']['type'] = 'formula_entry'
                # Remove apply_right from measures (moved to s06)
                ix['interaction']['measures'] = [
                    m for m in ix['interaction']['measures']
                    if m['capability'] != 'apply_right_to_extract_trailing_characters'
                ]
                # Remove apply_right from anchors
                ix['interaction']['anchors'] = [
                    a for a in ix['interaction']['anchors']
                    if 'apply_right_to_extract_trailing_characters' not in a
                ]
                # Update the formula_entry to test LEFT
                ix['interaction']['public'] = {
                    "prompt": (
                        "The Orders sheet has order IDs in column A (e.g., **\"LG-2001\"**). "
                        "Each order ID has a 2-letter prefix (\"LG\") followed by a hyphen and a 4-digit number.\n\n"
                        "In cell G2, write a formula using **LEFT** that extracts the first 2 characters "
                        "of the order ID in A2 — the 2-letter prefix.\n\n"
                        "The expected result is **\"LG\"**."
                    ),
                    "asset_ref": {
                        "asset_id": "asset_orders_clean",
                        "variant_id": None
                    },
                    "target_cell": "G2",
                    "allowed_functions": ["LEFT"],
                    "sheet_name": "orders"
                }
                ix['interaction']['grading'] = {
                    "expected_value": "LG",
                    "reference_formula": "=LEFT(A2,2)",
                    "must_use_functions": ["LEFT"],
                    "forbid_hardcoded_values": True
                }
                ix['interaction']['feedback'] = {
                    "correct": {
                        "message": (
                            "Correct! =LEFT(A2,2) extracts the first 2 characters of \"LG-2001\", returning \"LG\". "
                            "LEFT(text, num_chars) always counts from the beginning of the string."
                        )
                    },
                    "incorrect": {
                        "message": (
                            "Use =LEFT(A2,2). LEFT(text, num_chars) returns the first num_chars characters. "
                            "\"LG-2001\" starts with \"LG\" — the first 2 characters."
                        )
                    },
                    "hints": [
                        "LEFT(text, num_chars) extracts characters from the left end of the string.",
                        "\"LG-2001\" has 7 characters. The first 2 characters are \"LG\"."
                    ]
                }
                print("BLOCKING s07 text_date: reverted to formula_entry, changed to test LEFT")

# ─────────────────────────────────────────────────────────────────────────────
# BLOCKING: tile_spreadsheet_text_date_conditional_agg/s10
# Update exercise to use TODAY() so write_today_function_with_correct_syntax
# and construct_age_calculation_formula_using_datedif_and_today are tested.
# Remove TODAY from blocked_syntax; add TODAY() task in J2.
# ─────────────────────────────────────────────────────────────────────────────
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_text_date_conditional_agg':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_spreadsheet_text_date_conditional_agg.s10':
                pub = ix['interaction']['public']
                # Update prompt to include TODAY() task
                pub['prompt'] = (
                    "The **orders** sheet has order dates in column G (rows 2–21). "
                    "The starter file provides the order-date serial numbers for rows 2 and 3 in cells G2 and G3 "
                    "(both are **45355**, representing 2024-03-04), and a fixed reference date in H1 "
                    "(**45361**, representing 2024-03-10).\n\n"
                    "**Task 1 — days elapsed (fixed date):** In cell I2, write a DATEDIF formula that calculates "
                    "the number of **days** (unit \"D\") between the order date in G2 and the reference date in H1. "
                    "The result should be **6**.\n\n"
                    "**Task 2 — days for row 3:** In cell I3, write the same DATEDIF formula for G3. "
                    "The result should also be **6**.\n\n"
                    "**Task 3 — age in years (TODAY):** In cell J2, write a formula using **DATEDIF** and **TODAY()** "
                    "that calculates the number of complete **years** (unit \"Y\") between the order date in G2 and "
                    "today's date. Use TODAY() as the end_date argument. "
                    "Syntax: =DATEDIF(G2,TODAY(),\"Y\")."
                )
                # Update constraints to allow TODAY
                pub['constraints'] = {
                    "allowed_syntax": [
                        "DATEDIF(start_date, end_date, unit)",
                        "TODAY()",
                        "relative cell references",
                        "text in quotes"
                    ],
                    "blocked_syntax": [
                        "NOW",
                        "DAYS"
                    ]
                }
                # Update solution to include TODAY() task
                ix['interaction']['grading']['solution_files'] = [
                    {
                        "path": "book.sheet",
                        "content": (
                            "H1: 45361\n"
                            "G2: 45355\n"
                            "G3: 45355\n"
                            "I2: =DATEDIF(G2,H1,\"D\")\n"
                            "I3: =DATEDIF(G3,H1,\"D\")\n"
                            "J2: =DATEDIF(G2,TODAY(),\"Y\")\n"
                        )
                    }
                ]
                # Add formula_uses test for J2 (TODAY + DATEDIF)
                existing_tests = ix['interaction']['grading']['tests']
                # Check if test already exists
                if not any(t.get('test_id') == 'test_j2_uses_today_datedif' for t in existing_tests):
                    j2_test = {
                        "test_id": "test_j2_uses_today_datedif",
                        "kind": "formula_uses",
                        "spec": {
                            "cell": "J2",
                            "functions": ["DATEDIF", "TODAY"]
                        },
                        "visible": True,
                        "message_on_fail": (
                            "J2 must contain a formula using both DATEDIF and TODAY(). "
                            "Use =DATEDIF(G2,TODAY(),\"Y\") — TODAY() supplies the current date as the end_date, "
                            "and \"Y\" returns complete years."
                        )
                    }
                    existing_tests.append(j2_test)
                # Update feedback
                ix['interaction']['feedback']['correct']['message'] = (
                    "Well done! =DATEDIF(G2,H1,\"D\") correctly places the earlier date (G2) as start_date and "
                    "the later date (H1) as end_date, with unit \"D\" for days. "
                    "=DATEDIF(G2,TODAY(),\"Y\") uses TODAY() as the end_date to compute the age in complete years — "
                    "TODAY() returns today's date as a serial number, and \"Y\" counts complete years. "
                    "Excel stores dates as serial numbers, so DATEDIF can subtract them to count days or years."
                )
                ix['interaction']['feedback']['incorrect']['message'] = (
                    "For Tasks 1 and 2: Use =DATEDIF(G2,H1,\"D\") and =DATEDIF(G3,H1,\"D\"). "
                    "The argument order is: start_date (earlier date), end_date (later date), unit (\"D\" for days). "
                    "For Task 3: Use =DATEDIF(G2,TODAY(),\"Y\") — TODAY() supplies today's date as the end_date, "
                    "and \"Y\" returns the number of complete years."
                )
                print("BLOCKING s10 text_date: updated to include TODAY() task")

with open('batches/final_batch_011_da_spreadsheet/interactions.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Patch complete.")
