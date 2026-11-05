"""
Repair patch for interactions.part.c1.json and screens.json.
Fixes:
1. s05 (aggregation_logical): add apply_average_and_identify_ignored_values and apply_count_and_identify_what_is_excluded to measures
2. s10 (aggregation_logical): add use_or_as_if_logical_test_for_any_condition to measures; add OR task to exercise
3. s03 (text_date): fix reference_formula TRUE -> TRUE()
4. s10 (text_date): redesign to use serial numbers for DATEDIF
5. screens.json s10 (aggregation_logical): change type check -> hands_on
6. screens.json s01 (text_date): add before_after block
"""
import json
import copy

# ── interactions.part.c1.json ──────────────────────────────────────────────────
with open("batches/final_batch_011_da_spreadsheet/interactions.part.c1.json") as f:
    data = json.load(f)

for tile in data["tiles"]:
    if tile["tile_id"] == "tile_spreadsheet_aggregation_logical":
        for ix in tile["interactions"]:
            # Fix 1: s05 – add missing measures
            if ix["step_id"] == "tile_spreadsheet_aggregation_logical.s05":
                caps = {m["capability"] for m in ix["interaction"]["measures"]}
                if "apply_average_and_identify_ignored_values" not in caps:
                    ix["interaction"]["measures"].append({
                        "concept_id": "spreadsheet.aggregation_functions",
                        "capability": "apply_average_and_identify_ignored_values",
                        "fact_ids": ["f2"]
                    })
                if "apply_count_and_identify_what_is_excluded" not in caps:
                    ix["interaction"]["measures"].append({
                        "concept_id": "spreadsheet.aggregation_functions",
                        "capability": "apply_count_and_identify_what_is_excluded",
                        "fact_ids": ["f3"]
                    })

            # Fix 2: s10 – add OR measure and OR task to exercise
            if ix["step_id"] == "tile_spreadsheet_aggregation_logical.s10":
                caps = {m["capability"] for m in ix["interaction"]["measures"]}
                if "use_or_as_if_logical_test_for_any_condition" not in caps:
                    ix["interaction"]["measures"].append({
                        "concept_id": "spreadsheet.logical_functions",
                        "capability": "use_or_as_if_logical_test_for_any_condition",
                        "fact_ids": ["f4"]
                    })
                # Update prompt to include OR task
                ix["interaction"]["public"]["prompt"] = (
                    "The **orders** sheet has delivery times in column C (rows 2\u20135). "
                    "You need to classify each delivery into one of three bands:\n\n"
                    "- **\"Late\"** if delivery_minutes > 60\n"
                    "- **\"On Time\"** if delivery_minutes is between 30 and 60 (inclusive on both ends)\n"
                    "- **\"Fast\"** if delivery_minutes < 30\n\n"
                    "**Task 1 \u2014 nested IF with AND:** In cell F2, write a nested IF formula that classifies "
                    "the delivery time in C2. Use **AND** as the logical_test of the inner IF to enforce both "
                    "the lower bound (>=30) and the upper bound (<=60) of the \"On Time\" band. "
                    "Then write the same formula in F3 and F4.\n\n"
                    "Expected results:\n"
                    "- F2: **\"Fast\"** (C2 = 28)\n"
                    "- F3: **\"On Time\"** (C3 = 45)\n"
                    "- F4: **\"Late\"** (C4 = 62)\n\n"
                    "**Task 2 \u2014 OR flag:** In cell F5, write an IF formula that returns **\"Extreme\"** "
                    "if C5 is less than 20 **OR** greater than 70, and **\"Normal\"** otherwise. "
                    "Use **OR** as the logical_test.\n\n"
                    "Expected result:\n"
                    "- F5: **\"Extreme\"** (C5 = 19)"
                )
                # Update starter content
                ix["interaction"]["public"]["workspace"]["files"][0]["content"] = (
                    "// The orders sheet has delivery_minutes in column C.\n"
                    "// C2=28, C3=45, C4=62, C5=19\n\n"
                    "// Task 1: In F2, write a nested IF formula that classifies C2 as:\n"
                    "//   'Late'    if C2 > 60\n"
                    "//   'On Time' if C2 >= 30 AND C2 <= 60  (use AND for both bounds)\n"
                    "//   'Fast'    if C2 < 30\n"
                    "// Then write the same pattern in F3 and F4.\n\n"
                    "// Task 2: In F5, write an IF formula that returns 'Extreme' if\n"
                    "//   C5 < 20 OR C5 > 70, and 'Normal' otherwise. Use OR.\n"
                )
                # Update solution
                ix["interaction"]["grading"]["solution_files"][0]["content"] = (
                    "F2: =IF(C2>60,\"Late\",IF(AND(C2>=30,C2<=60),\"On Time\",\"Fast\"))\n"
                    "F3: =IF(C3>60,\"Late\",IF(AND(C3>=30,C3<=60),\"On Time\",\"Fast\"))\n"
                    "F4: =IF(C4>60,\"Late\",IF(AND(C4>=30,C4<=60),\"On Time\",\"Fast\"))\n"
                    "F5: =IF(OR(C5<20,C5>70),\"Extreme\",\"Normal\")\n"
                )
                # Add F5 test
                existing_test_ids = {t["test_id"] for t in ix["interaction"]["grading"]["tests"]}
                if "test_f5_extreme" not in existing_test_ids:
                    ix["interaction"]["grading"]["tests"].append({
                        "test_id": "test_f5_extreme",
                        "kind": "cell_equals",
                        "spec": {
                            "cell": "F5",
                            "expected": "Extreme"
                        },
                        "visible": True,
                        "message_on_fail": "F5 should be \"Extreme\" because C5=19 is less than 20. Use =IF(OR(C5<20,C5>70),\"Extreme\",\"Normal\"). OR returns TRUE when any condition is met."
                    })
                if "test_f5_uses_or" not in existing_test_ids:
                    ix["interaction"]["grading"]["tests"].append({
                        "test_id": "test_f5_uses_or",
                        "kind": "formula_uses",
                        "spec": {
                            "cell": "F5",
                            "functions": ["IF", "OR"]
                        },
                        "visible": True,
                        "message_on_fail": "F5 must use both IF and OR. Use OR(C5<20,C5>70) as the logical_test: OR returns TRUE when any one of its conditions is TRUE."
                    })
                # Update feedback
                ix["interaction"]["feedback"]["correct"]["message"] = (
                    "Well done! Your nested IF correctly classifies all three delivery times using AND for the "
                    "On Time band. AND returns TRUE only when BOTH conditions are met. Your OR formula in F5 "
                    "correctly flags C5=19 as Extreme because OR returns TRUE when ANY condition is met "
                    "(19 < 20 is TRUE)."
                )
                ix["interaction"]["feedback"]["incorrect"]["message"] = (
                    "For F2\u2013F4: use =IF(C2>60,\"Late\",IF(AND(C2>=30,C2<=60),\"On Time\",\"Fast\")). "
                    "AND requires BOTH bounds to be true. "
                    "For F5: use =IF(OR(C5<20,C5>70),\"Extreme\",\"Normal\"). "
                    "OR returns TRUE when ANY condition is true."
                )

    if tile["tile_id"] == "tile_spreadsheet_text_date_conditional_agg":
        for ix in tile["interactions"]:
            # Fix 3: s03 – fix TEXTJOIN reference_formula TRUE -> TRUE()
            if ix["step_id"] == "tile_spreadsheet_text_date_conditional_agg.s03":
                ix["interaction"]["grading"]["reference_formula"] = "=TEXTJOIN(\" | \",TRUE(),B2,E2)"

            # Fix 4: s10 – redesign DATEDIF exercise to use serial numbers
            if ix["step_id"] == "tile_spreadsheet_text_date_conditional_agg.s10":
                # G2 and G3 in the CSV are text strings "2024-03-04".
                # We override them with serial numbers in the starter/solution.
                # 2024-03-04 = serial 45355, 2024-03-10 = serial 45361
                ix["interaction"]["public"]["prompt"] = (
                    "The **orders** sheet has order dates in column G (rows 2\u201321). "
                    "The starter file provides the order-date serial numbers for rows 2 and 3 "
                    "in cells G2 and G3 (both are **45355**, representing 2024-03-04), "
                    "and a fixed reference date in H1 (**45361**, representing 2024-03-10).\n\n"
                    "**Task 1 \u2014 days elapsed:** In cell I2, write a DATEDIF formula that calculates "
                    "the number of **days** (unit \"D\") between the order date in G2 and the reference "
                    "date in H1. The result should be **6**.\n\n"
                    "**Task 2 \u2014 days for row 3:** In cell I3, write the same DATEDIF formula for G3. "
                    "The result should also be **6**."
                )
                ix["interaction"]["public"]["workspace"]["files"][0]["content"] = (
                    "// H1 holds the reference date as a serial number (45361 = 2024-03-10).\n"
                    "H1: 45361\n"
                    "// G2 and G3 hold order-date serial numbers (45355 = 2024-03-04).\n"
                    "G2: 45355\n"
                    "G3: 45355\n\n"
                    "// Task 1: In I2, write a DATEDIF formula that returns the number of days\n"
                    "// between the order date in G2 and the reference date in H1.\n"
                    "// DATEDIF syntax: DATEDIF(start_date, end_date, unit)\n"
                    "// Use unit \"D\" for days. Expected result: 6\n\n"
                    "// Task 2: In I3, write the same DATEDIF formula for G3.\n"
                    "// Expected result: 6\n"
                )
                ix["interaction"]["grading"]["solution_files"][0]["content"] = (
                    "H1: 45361\n"
                    "G2: 45355\n"
                    "G3: 45355\n"
                    "I2: =DATEDIF(G2,H1,\"D\")\n"
                    "I3: =DATEDIF(G3,H1,\"D\")\n"
                )

with open("batches/final_batch_011_da_spreadsheet/interactions.part.c1.json", "w") as f:
    json.dump(data, f, indent=2)
print("interactions.part.c1.json patched")

# ── screens.json ───────────────────────────────────────────────────────────────
with open("batches/final_batch_011_da_spreadsheet/screens.json") as f:
    screens = json.load(f)

for tile in screens["tiles"]:
    if tile["tile_id"] == "tile_spreadsheet_aggregation_logical":
        for step in tile["steps"]:
            # Fix 5: s10 – change type from check to hands_on
            if step["step_id"] == "tile_spreadsheet_aggregation_logical.s10":
                if step["type"] == "check":
                    step["type"] = "hands_on"
                    print("Fixed s10 type: check -> hands_on")

    if tile["tile_id"] == "tile_spreadsheet_text_date_conditional_agg":
        for step in tile["steps"]:
            # Fix 6: s01 – add before_after block
            if step["step_id"] == "tile_spreadsheet_text_date_conditional_agg.s01":
                block_types = {b["type"] for b in step.get("blocks", [])}
                if "before_after" not in block_types and "side_by_side" not in block_types:
                    # Add a before_after block showing TEXTJOIN before/after
                    before_after_block = {
                        "type": "before_after",
                        "block_id": "tile_spreadsheet_text_date_conditional_agg.s01.b4",
                        "before": {
                            "type": "spreadsheet_grid",
                            "block_id": "tile_spreadsheet_text_date_conditional_agg.s01.b4.before",
                            "asset_ref": {
                                "asset_id": "asset_orders_clean"
                            },
                            "range": "A1:E3",
                            "sheet_name": "Orders",
                            "show_formula_bar": False,
                            "cells": [],
                            "annotations": [
                                {
                                    "target": "B2",
                                    "text": "city: Lagos"
                                },
                                {
                                    "target": "E2",
                                    "text": "status: Delivered"
                                }
                            ]
                        },
                        "after": {
                            "type": "spreadsheet_grid",
                            "block_id": "tile_spreadsheet_text_date_conditional_agg.s01.b4.after",
                            "asset_ref": {
                                "asset_id": "asset_orders_clean"
                            },
                            "range": "A1:H3",
                            "sheet_name": "Orders",
                            "show_formula_bar": True,
                            "cells": [
                                {
                                    "ref": "H2",
                                    "formula": "=TEXTJOIN(\" | \",TRUE(),B2,E2)",
                                    "note": "Combines city and status with | delimiter"
                                },
                                {
                                    "ref": "H3",
                                    "formula": "=TEXTJOIN(\" | \",TRUE(),B3,E3)"
                                }
                            ],
                            "annotations": [
                                {
                                    "target": "H2",
                                    "text": "TEXTJOIN joins B2 and E2 with \" | \""
                                }
                            ]
                        },
                        "change_summary": "After adding a TEXTJOIN formula in column H, the separate city (B) and status (E) values are combined into a single string with the \" | \" delimiter. Setting ignore_empty to TRUE means blank status cells are skipped rather than producing a stray delimiter.",
                        "lineage": {
                            "concept_ids": [
                                "spreadsheet.text_combining"
                            ],
                            "fact_ids": [
                                "spreadsheet.text_combining#f1",
                                "spreadsheet.text_combining#f2"
                            ],
                            "teaching_block_ids": [
                                "spreadsheet.text_combining#tb1"
                            ],
                            "anchors": [
                                "spreadsheet.text_combining#visual"
                            ]
                        }
                    }
                    step["blocks"].append(before_after_block)
                    print("Added before_after block to s01")

with open("batches/final_batch_011_da_spreadsheet/screens.json", "w") as f:
    json.dump(screens, f, indent=2)
print("screens.json patched")
