#!/usr/bin/env python3
"""Build screens.part.c2.json for chunk c2 tiles:
  - tile_spreadsheet_lookups_troubleshooting
  - tile_spreadsheet_cleaning_cross_sheet
  - tile_spreadsheet_sorting_filtering
"""
import json

out = {
    "schema_version": "0.1.0",
    "kind": "screens_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_011_da_spreadsheet",
    "tiles": []
}

# ─────────────────────────────────────────────────────────────────────────────
# TILE 1: tile_spreadsheet_lookups_troubleshooting
# Concepts: vlookup_xlookup, index_match, formula_error_troubleshooting
# ─────────────────────────────────────────────────────────────────────────────
T1 = "tile_spreadsheet_lookups_troubleshooting"

tile1 = {
    "tile_id": T1,
    "title": "VLOOKUP/XLOOKUP and INDEX/MATCH",
    "summary": "Look up values across sheets with VLOOKUP, XLOOKUP, and INDEX/MATCH, and diagnose the three most common formula error codes.",
    "steps": [

        # s01 — explainer: vlookup_xlookup intro + visual (spreadsheet_grid)
        {
            "step_id": f"{T1}.s01",
            "type": "explainer",
            "concept_ids": ["spreadsheet.vlookup_xlookup"],
            "eyebrow": "Lookup Functions",
            "title": "Finding a Driver Name from an Order Row",
            "lede": "Your Orders sheet records a driver ID in column F. VLOOKUP and XLOOKUP let you pull the matching driver name from the Drivers sheet automatically.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T1}.s01.p1",
                    "role": "intro",
                    "text": "Suppose your Drivers sheet has driver IDs in its leftmost column and driver names in the column next to it, and your Orders sheet records a driver ID in column F. You want each order row to show the matching driver's name without retyping it. Lookup functions do exactly that: they search one table for a key and return a value from the same row.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.vlookup_xlookup"],
                        "teaching_block_ids": ["spreadsheet.vlookup_xlookup#tb1"],
                        "fact_ids": []
                    }
                },
                {
                    "type": "prose",
                    "block_id": f"{T1}.s01.p2",
                    "role": "syntax",
                    "text": "VLOOKUP looks up a value in the leftmost column of a range and returns a value from the same row in a column you specify by its position. Its syntax is VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup]). Entering FALSE for range_lookup searches for an exact match; leaving it blank or entering TRUE searches for an approximate match — and TRUE is the default when the argument is omitted. To look up a driver ID exactly, write =VLOOKUP(F2,Drivers!A:B,2,FALSE).",
                    "lineage": {
                        "concept_ids": ["spreadsheet.vlookup_xlookup"],
                        "teaching_block_ids": ["spreadsheet.vlookup_xlookup#tb2"],
                        "fact_ids": [
                            "spreadsheet.vlookup_xlookup#f1",
                            "spreadsheet.vlookup_xlookup#f2"
                        ]
                    }
                },
                {
                    "type": "spreadsheet_grid",
                    "block_id": f"{T1}.s01.grid1",
                    "asset_ref": {"asset_id": "asset_drivers_vlookup", "variant_id": None, "columns": None},
                    "sheet_name": "Drivers",
                    "range": "A1:B6",
                    "show_formula_bar": True,
                    "annotations": [
                        {"target": "A1", "text": "Lookup key column (leftmost) — VLOOKUP searches here"},
                        {"target": "B1", "text": "Return column — col_index_num = 2"}
                    ],
                    "lineage": {
                        "concept_ids": ["spreadsheet.vlookup_xlookup"],
                        "teaching_block_ids": ["spreadsheet.vlookup_xlookup#tb1", "spreadsheet.vlookup_xlookup#tb2"],
                        "fact_ids": [
                            "spreadsheet.vlookup_xlookup#f1",
                            "spreadsheet.vlookup_xlookup#f2"
                        ],
                        "anchors": ["spreadsheet.vlookup_xlookup#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["spreadsheet.vlookup_xlookup"],
                "teaching_block_ids": ["spreadsheet.vlookup_xlookup#tb1", "spreadsheet.vlookup_xlookup#tb2"],
                "fact_ids": [
                    "spreadsheet.vlookup_xlookup#f1",
                    "spreadsheet.vlookup_xlookup#f2"
                ],
                "anchors": ["spreadsheet.vlookup_xlookup#visual"]
            }
        },

        # s02 — video: vlookup_xlookup
        {
            "step_id": f"{T1}.s02",
            "type": "video",
            "concept_ids": ["spreadsheet.vlookup_xlookup"],
            "eyebrow": "Lookup Functions",
            "title": "VLOOKUP and XLOOKUP in Action",
            "blocks": [
                {
                    "type": "media_group",
                    "block_id": f"{T1}.s02.mg1",
                    "segment_ids": [
                        "seg_spreadsheet.vlookup_xlookup_8rtvDQVQaA0_79_221",
                        "seg_spreadsheet.vlookup_xlookup_dlBuWllegRg_0_171"
                    ]
                }
            ],
            "lineage": {
                "concept_ids": ["spreadsheet.vlookup_xlookup"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "spreadsheet.vlookup_xlookup#f1",
                    "spreadsheet.vlookup_xlookup#f2",
                    "spreadsheet.vlookup_xlookup#f4"
                ],
                "segment_ids": [
                    "seg_spreadsheet.vlookup_xlookup_8rtvDQVQaA0_79_221",
                    "seg_spreadsheet.vlookup_xlookup_dlBuWllegRg_0_171"
                ]
            }
        },

        # s03 — explainer: HLOOKUP + XLOOKUP
        {
            "step_id": f"{T1}.s03",
            "type": "explainer",
            "concept_ids": ["spreadsheet.vlookup_xlookup"],
            "eyebrow": "Lookup Functions",
            "title": "HLOOKUP and XLOOKUP",
            "lede": "HLOOKUP searches across rows instead of down columns. XLOOKUP is a newer alternative that works in any direction and matches exactly by default.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T1}.s03.p1",
                    "role": "mechanism",
                    "text": "HLOOKUP works like VLOOKUP but searches across the top row of a table and returns a value from a row you specify by its position. Its syntax is HLOOKUP(lookup_value, table_array, row_index_num, [range_lookup]).",
                    "lineage": {
                        "concept_ids": ["spreadsheet.vlookup_xlookup"],
                        "teaching_block_ids": ["spreadsheet.vlookup_xlookup#tb3"],
                        "fact_ids": ["spreadsheet.vlookup_xlookup#f3"]
                    }
                },
                {
                    "type": "prose",
                    "block_id": f"{T1}.s03.p2",
                    "role": "mechanism",
                    "text": "XLOOKUP searches lookup_array for lookup_value and returns the corresponding item from return_array, producing an exact match by default. Its syntax is XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode]). VLOOKUP can only look up a value from left to right, but XLOOKUP works in any direction. The same driver lookup written as =XLOOKUP(F2,Drivers!A:A,Drivers!B:B) already matches exactly, without needing FALSE spelled out.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.vlookup_xlookup"],
                        "teaching_block_ids": ["spreadsheet.vlookup_xlookup#tb4"],
                        "fact_ids": [
                            "spreadsheet.vlookup_xlookup#f4",
                            "spreadsheet.vlookup_xlookup#f5"
                        ]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["spreadsheet.vlookup_xlookup"],
                "teaching_block_ids": [
                    "spreadsheet.vlookup_xlookup#tb3",
                    "spreadsheet.vlookup_xlookup#tb4"
                ],
                "fact_ids": [
                    "spreadsheet.vlookup_xlookup#f3",
                    "spreadsheet.vlookup_xlookup#f4",
                    "spreadsheet.vlookup_xlookup#f5"
                ]
            }
        },

        # s04 — check: HLOOKUP syntax (framing only)
        {
            "step_id": f"{T1}.s04",
            "type": "check",
            "concept_ids": ["spreadsheet.vlookup_xlookup"],
            "eyebrow": "Quick Check",
            "title": "HLOOKUP: Row Index",
            "lede": "Test your understanding of HLOOKUP's row_index_num argument.",
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["spreadsheet.vlookup_xlookup"],
                "teaching_block_ids": [],
                "fact_ids": ["spreadsheet.vlookup_xlookup#f3"],
                "anchors": ["spreadsheet.vlookup_xlookup#assessment:identify_hlookup_syntax_and_row_index_argument"]
            }
        },

        # s05 — hands_on: vlookup/xlookup practice (framing only)
        {
            "step_id": f"{T1}.s05",
            "type": "hands_on",
            "concept_ids": ["spreadsheet.vlookup_xlookup"],
            "eyebrow": "Practice",
            "title": "Write VLOOKUP and XLOOKUP Formulas",
            "lede": "Use the QuickDeliver Orders and Drivers sheets to write lookup formulas that return driver names.",
            "reward": {"gems": 10},
            "lineage": {
                "concept_ids": ["spreadsheet.vlookup_xlookup"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "spreadsheet.vlookup_xlookup#f1",
                    "spreadsheet.vlookup_xlookup#f2",
                    "spreadsheet.vlookup_xlookup#f4",
                    "spreadsheet.vlookup_xlookup#f5"
                ],
                "anchors": [
                    "spreadsheet.vlookup_xlookup#practice",
                    "spreadsheet.vlookup_xlookup#assessment:write_vlookup_with_correct_key_column_and_match_type",
                    "spreadsheet.vlookup_xlookup#assessment:write_xlookup_with_lookup_array_return_array_and_direction_awareness"
                ]
            }
        },

        # s06 — explainer: index_match intro + visual (spreadsheet_grid)
        {
            "step_id": f"{T1}.s06",
            "type": "explainer",
            "concept_ids": ["spreadsheet.index_match"],
            "eyebrow": "INDEX / MATCH",
            "title": "When the Key Column Is Not on the Left",
            "lede": "VLOOKUP requires the lookup key to be in the leftmost column. When the layout is reversed, INDEX and MATCH work together to handle it.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T1}.s06.p1",
                    "role": "intro",
                    "text": "VLOOKUP only works when the column you're returning a value from sits to the right of the key column. If your Drivers sheet instead had driver names in column A and driver IDs in column B, VLOOKUP couldn't look up an ID and return the name to its left.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.index_match"],
                        "teaching_block_ids": ["spreadsheet.index_match#tb1"],
                        "fact_ids": []
                    }
                },
                {
                    "type": "prose",
                    "block_id": f"{T1}.s06.p2",
                    "role": "syntax",
                    "text": "MATCH searches for a specified item in a range of cells and returns the relative position of that item within the range. Its syntax is MATCH(lookup_value, lookup_array, [match_type]). Setting match_type to 0 finds an exact match; a match_type of 1, or omitting the argument, finds the largest value less than or equal to lookup_value and requires lookup_array to be sorted in ascending order.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.index_match"],
                        "teaching_block_ids": ["spreadsheet.index_match#tb2"],
                        "fact_ids": [
                            "spreadsheet.index_match#f1",
                            "spreadsheet.index_match#f2"
                        ]
                    }
                },
                {
                    "type": "prose",
                    "block_id": f"{T1}.s06.p3",
                    "role": "syntax",
                    "text": "INDEX returns the value of an element in a range or array, selected by its row and column position. The array form's syntax is INDEX(array, row_num, [column_num]).",
                    "lineage": {
                        "concept_ids": ["spreadsheet.index_match"],
                        "teaching_block_ids": ["spreadsheet.index_match#tb3"],
                        "fact_ids": ["spreadsheet.index_match#f3"]
                    }
                },
                {
                    "type": "spreadsheet_grid",
                    "block_id": f"{T1}.s06.grid1",
                    "asset_ref": {"asset_id": "asset_drivers_index_match", "variant_id": None, "columns": None},
                    "sheet_name": "Drivers",
                    "range": "A1:B6",
                    "show_formula_bar": True,
                    "annotations": [
                        {"target": "A1", "text": "Return column (driver_name) — sits LEFT of the key"},
                        {"target": "B1", "text": "Key column (driver_id) — VLOOKUP cannot look left from here"}
                    ],
                    "lineage": {
                        "concept_ids": ["spreadsheet.index_match"],
                        "teaching_block_ids": [
                            "spreadsheet.index_match#tb1",
                            "spreadsheet.index_match#tb2",
                            "spreadsheet.index_match#tb3"
                        ],
                        "fact_ids": [
                            "spreadsheet.index_match#f1",
                            "spreadsheet.index_match#f2",
                            "spreadsheet.index_match#f3"
                        ],
                        "anchors": ["spreadsheet.index_match#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["spreadsheet.index_match"],
                "teaching_block_ids": [
                    "spreadsheet.index_match#tb1",
                    "spreadsheet.index_match#tb2",
                    "spreadsheet.index_match#tb3"
                ],
                "fact_ids": [
                    "spreadsheet.index_match#f1",
                    "spreadsheet.index_match#f2",
                    "spreadsheet.index_match#f3"
                ],
                "anchors": ["spreadsheet.index_match#visual"]
            }
        },

        # s07 — video: index_match
        {
            "step_id": f"{T1}.s07",
            "type": "video",
            "concept_ids": ["spreadsheet.index_match"],
            "eyebrow": "INDEX / MATCH",
            "title": "INDEX and MATCH Working Together",
            "blocks": [
                {
                    "type": "media_group",
                    "block_id": f"{T1}.s07.mg1",
                    "segment_ids": ["seg_spreadsheet.index_match_kly0uPIM4IU_49_172"]
                }
            ],
            "lineage": {
                "concept_ids": ["spreadsheet.index_match"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "spreadsheet.index_match#f1",
                    "spreadsheet.index_match#f3"
                ],
                "segment_ids": ["seg_spreadsheet.index_match_kly0uPIM4IU_49_172"]
            }
        },

        # s08 — explainer: INDEX/MATCH combined mechanism
        {
            "step_id": f"{T1}.s08",
            "type": "explainer",
            "concept_ids": ["spreadsheet.index_match"],
            "eyebrow": "INDEX / MATCH",
            "title": "Combining INDEX and MATCH",
            "lede": "MATCH finds the row; INDEX retrieves the value. Together they handle any column layout.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T1}.s08.p1",
                    "role": "mechanism",
                    "text": "VLOOKUP can only look up a value from left to right — the column containing the lookup value must be to the left of the column containing the return value. When the layout isn't built that way, MATCH can find the row position of the key and INDEX can then return the value from any column at that row position. On your Orders sheet, with a driver ID in F2, =INDEX(Drivers!A:A,MATCH(F2,Drivers!B:B,0)) finds the row where that driver ID occurs in column B of the Drivers sheet, then reads the driver name from column A at that same row — something VLOOKUP alone couldn't do on this layout.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.index_match"],
                        "teaching_block_ids": ["spreadsheet.index_match#tb4"],
                        "fact_ids": ["spreadsheet.index_match#f4"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["spreadsheet.index_match"],
                "teaching_block_ids": ["spreadsheet.index_match#tb4"],
                "fact_ids": ["spreadsheet.index_match#f4"]
            }
        },

        # s09 — check: INDEX/MATCH (framing only)
        {
            "step_id": f"{T1}.s09",
            "type": "check",
            "concept_ids": ["spreadsheet.index_match"],
            "eyebrow": "Quick Check",
            "title": "Write an INDEX/MATCH Formula",
            "lede": "Choose the correct INDEX/MATCH formula for a reversed-column layout.",
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["spreadsheet.index_match"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "spreadsheet.index_match#f1",
                    "spreadsheet.index_match#f3",
                    "spreadsheet.index_match#f4"
                ],
                "anchors": ["spreadsheet.index_match#assessment:write_correct_index_match_for_left_of_key_return_column"]
            }
        },

        # s10 — hands_on: index_match practice (framing only)
        {
            "step_id": f"{T1}.s10",
            "type": "hands_on",
            "concept_ids": ["spreadsheet.index_match"],
            "eyebrow": "Practice",
            "title": "Build an INDEX/MATCH Lookup",
            "lede": "Given the reversed Drivers layout, write an INDEX/MATCH formula that returns the driver name for a given driver ID.",
            "reward": {"gems": 10},
            "lineage": {
                "concept_ids": ["spreadsheet.index_match"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "spreadsheet.index_match#f1",
                    "spreadsheet.index_match#f2",
                    "spreadsheet.index_match#f3",
                    "spreadsheet.index_match#f4"
                ],
                "anchors": [
                    "spreadsheet.index_match#practice",
                    "spreadsheet.index_match#assessment:state_match_syntax_and_match_type_behaviour",
                    "spreadsheet.index_match#assessment:state_index_array_form_syntax",
                    "spreadsheet.index_match#assessment:identify_vlookup_left_column_limitation_and_apply_index_match_as_alternative",
                    "spreadsheet.index_match#assessment:write_correct_index_match_for_left_of_key_return_column"
                ]
            }
        },

        # s11 — explainer: formula errors #N/A and #REF! + visual (spreadsheet_grid)
        {
            "step_id": f"{T1}.s11",
            "type": "explainer",
            "concept_ids": ["spreadsheet.formula_error_troubleshooting"],
            "eyebrow": "Formula Errors",
            "title": "Reading #N/A and #REF! Error Codes",
            "lede": "When a formula can't find what it needs or points to a cell that no longer exists, Excel shows an error code instead of a value.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T1}.s11.p1",
                    "role": "intro",
                    "text": "Formulas in your Orders or Drivers sheets sometimes show an error code instead of a value. Each code points at a different kind of problem.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.formula_error_troubleshooting"],
                        "teaching_block_ids": ["spreadsheet.formula_error_troubleshooting#tb1"],
                        "fact_ids": []
                    }
                },
                {
                    "type": "prose",
                    "block_id": f"{T1}.s11.p2",
                    "role": "mechanism",
                    "text": "The #N/A error generally indicates that a formula can't find what it's been asked to look for. The most common cause is with XLOOKUP, VLOOKUP, HLOOKUP, LOOKUP, or MATCH functions when the lookup value doesn't exist in the source data. A VLOOKUP for a driver ID that was never entered on the Drivers sheet would show #N/A.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.formula_error_troubleshooting"],
                        "teaching_block_ids": ["spreadsheet.formula_error_troubleshooting#tb2"],
                        "fact_ids": ["spreadsheet.formula_error_troubleshooting#f1"]
                    }
                },
                {
                    "type": "prose",
                    "block_id": f"{T1}.s11.p3",
                    "role": "mechanism",
                    "text": "The #REF! error shows when a formula refers to a cell that's not valid, which happens most often when cells that were referenced by formulas get deleted or pasted over. Deleting the amount column that a SUM formula depended on would turn that formula into a #REF! error.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.formula_error_troubleshooting"],
                        "teaching_block_ids": ["spreadsheet.formula_error_troubleshooting#tb3"],
                        "fact_ids": ["spreadsheet.formula_error_troubleshooting#f2"]
                    }
                },
                {
                    "type": "spreadsheet_grid",
                    "block_id": f"{T1}.s11.grid1",
                    "asset_ref": {"asset_id": "asset_orders_clean", "variant_id": None, "columns": ["order_id", "driver_id", "amount"]},
                    "sheet_name": "Orders",
                    "range": "A1:C5",
                    "show_formula_bar": True,
                    "cells": [
                        {"ref": "C2", "formula": "=VLOOKUP(B2,Drivers!A:B,2,FALSE)", "note": "Returns #N/A if driver ID not found in Drivers sheet"},
                        {"ref": "C3", "formula": "=SUM(#REF!)", "note": "#REF! after referenced column was deleted"}
                    ],
                    "annotations": [
                        {"target": "C2", "text": "#N/A — lookup value not found in source data"},
                        {"target": "C3", "text": "#REF! — referenced column was deleted"}
                    ],
                    "lineage": {
                        "concept_ids": ["spreadsheet.formula_error_troubleshooting"],
                        "teaching_block_ids": [
                            "spreadsheet.formula_error_troubleshooting#tb1",
                            "spreadsheet.formula_error_troubleshooting#tb2",
                            "spreadsheet.formula_error_troubleshooting#tb3"
                        ],
                        "fact_ids": [
                            "spreadsheet.formula_error_troubleshooting#f1",
                            "spreadsheet.formula_error_troubleshooting#f2"
                        ],
                        "anchors": ["spreadsheet.formula_error_troubleshooting#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["spreadsheet.formula_error_troubleshooting"],
                "teaching_block_ids": [
                    "spreadsheet.formula_error_troubleshooting#tb1",
                    "spreadsheet.formula_error_troubleshooting#tb2",
                    "spreadsheet.formula_error_troubleshooting#tb3"
                ],
                "fact_ids": [
                    "spreadsheet.formula_error_troubleshooting#f1",
                    "spreadsheet.formula_error_troubleshooting#f2"
                ],
                "anchors": ["spreadsheet.formula_error_troubleshooting#visual"]
            }
        },

        # s12 — explainer: #VALUE! error
        {
            "step_id": f"{T1}.s12",
            "type": "explainer",
            "concept_ids": ["spreadsheet.formula_error_troubleshooting"],
            "eyebrow": "Formula Errors",
            "title": "The #VALUE! Error and SUM vs. Arithmetic",
            "lede": "A text value in a cell can break an arithmetic formula but not a SUM — knowing the difference helps you fix the right thing.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T1}.s12.p1",
                    "role": "mechanism",
                    "text": "#VALUE! is Excel's way of saying there's something wrong with the way a formula is typed, or something wrong with the cells it's referencing. A formula like =A1+B1+C1 can break and return #VALUE! if any referenced cell contains a non-numeric (text) value, whereas a SUM formula over the same cells ignores the text values and sums only the numeric ones — so typing a stray note into an amount cell breaks a plain + formula but not a SUM over the same range. In the QuickDeliver Orders sheet, if amount in row 16 holds the text \"N/A\" instead of a number, =D2+D16 returns #VALUE! but =SUM(D2:D21) still returns a total.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.formula_error_troubleshooting"],
                        "teaching_block_ids": ["spreadsheet.formula_error_troubleshooting#tb4"],
                        "fact_ids": [
                            "spreadsheet.formula_error_troubleshooting#f3",
                            "spreadsheet.formula_error_troubleshooting#f4"
                        ]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["spreadsheet.formula_error_troubleshooting"],
                "teaching_block_ids": ["spreadsheet.formula_error_troubleshooting#tb4"],
                "fact_ids": [
                    "spreadsheet.formula_error_troubleshooting#f3",
                    "spreadsheet.formula_error_troubleshooting#f4"
                ]
            }
        },

        # s13 — video: formula errors
        {
            "step_id": f"{T1}.s13",
            "type": "video",
            "concept_ids": ["spreadsheet.formula_error_troubleshooting"],
            "eyebrow": "Formula Errors",
            "title": "Seeing Formula Errors Appear and Propagate",
            "blocks": [
                {
                    "type": "media_group",
                    "block_id": f"{T1}.s13.mg1",
                    "segment_ids": ["seg_spreadsheet.formula_error_troubleshooting_sFn0gE_y1U4_58_413"]
                }
            ],
            "lineage": {
                "concept_ids": ["spreadsheet.formula_error_troubleshooting"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "spreadsheet.formula_error_troubleshooting#f1",
                    "spreadsheet.formula_error_troubleshooting#f2",
                    "spreadsheet.formula_error_troubleshooting#f3",
                    "spreadsheet.formula_error_troubleshooting#f4"
                ],
                "segment_ids": ["seg_spreadsheet.formula_error_troubleshooting_sFn0gE_y1U4_58_413"]
            }
        },

        # s14 — check: #VALUE! (framing only)
        {
            "step_id": f"{T1}.s14",
            "type": "check",
            "concept_ids": ["spreadsheet.formula_error_troubleshooting"],
            "eyebrow": "Quick Check",
            "title": "Diagnosing #VALUE! Errors",
            "lede": "Identify the cause of a #VALUE! error and the fix that avoids it.",
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["spreadsheet.formula_error_troubleshooting"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "spreadsheet.formula_error_troubleshooting#f3",
                    "spreadsheet.formula_error_troubleshooting#f4"
                ],
                "anchors": ["spreadsheet.formula_error_troubleshooting#assessment:diagnose_value_error_as_wrong_type_or_formula_structure"]
            }
        },

        # s15 — check: #VALUE! propagation (framing only)
        {
            "step_id": f"{T1}.s15",
            "type": "check",
            "concept_ids": ["spreadsheet.formula_error_troubleshooting"],
            "eyebrow": "Quick Check",
            "title": "#VALUE! Propagation Through SUM or AVERAGE",
            "lede": "Understand how a single error cell can spread into formulas built on top of it.",
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["spreadsheet.formula_error_troubleshooting"],
                "teaching_block_ids": [],
                "fact_ids": ["spreadsheet.formula_error_troubleshooting#f5"],
                "anchors": ["spreadsheet.formula_error_troubleshooting#assessment:diagnose_value_error_propagation_through_sum_or_average"]
            }
        },

        # s16 — hands_on: error troubleshooting (framing only)
        {
            "step_id": f"{T1}.s16",
            "type": "hands_on",
            "concept_ids": ["spreadsheet.formula_error_troubleshooting"],
            "eyebrow": "Practice",
            "title": "Diagnose Formula Errors",
            "lede": "Given a worksheet with a broken VLOOKUP showing #N/A and a broken addition formula showing #VALUE!, identify the cause of each error.",
            "reward": {"gems": 10},
            "lineage": {
                "concept_ids": ["spreadsheet.formula_error_troubleshooting"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "spreadsheet.formula_error_troubleshooting#f1",
                    "spreadsheet.formula_error_troubleshooting#f2",
                    "spreadsheet.formula_error_troubleshooting#f4"
                ],
                "anchors": [
                    "spreadsheet.formula_error_troubleshooting#practice",
                    "spreadsheet.formula_error_troubleshooting#assessment:diagnose_na_error_as_lookup_value_not_found",
                    "spreadsheet.formula_error_troubleshooting#assessment:diagnose_ref_error_as_invalid_cell_reference",
                    "spreadsheet.formula_error_troubleshooting#assessment:distinguish_sum_from_arithmetic_operator_on_mixed_range"
                ]
            }
        },

        # s17 — recap
        {
            "step_id": f"{T1}.s17",
            "type": "recap",
            "concept_ids": [
                "spreadsheet.vlookup_xlookup",
                "spreadsheet.index_match",
                "spreadsheet.formula_error_troubleshooting"
            ],
            "eyebrow": "Recap",
            "title": "Lookups and Error Codes — Key Points",
            "lede": "You can now look up values across sheets and read the three most common formula error codes.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T1}.s17.p1",
                    "role": "takeaway",
                    "text": "VLOOKUP searches the leftmost column of a range and returns a value by column position; use FALSE for an exact match. XLOOKUP works in any direction and matches exactly by default. When the return column sits to the left of the key column, combine INDEX and MATCH: MATCH finds the row position, INDEX retrieves the value. For errors: #N/A means the lookup value wasn't found; #REF! means a referenced cell is no longer valid; #VALUE! means a formula encountered a wrong data type — and if AVERAGE or SUM refer to cells that contain #VALUE! errors, those formulas will also return #VALUE!.",
                    "lineage": {
                        "concept_ids": [
                            "spreadsheet.vlookup_xlookup",
                            "spreadsheet.index_match",
                            "spreadsheet.formula_error_troubleshooting"
                        ],
                        "teaching_block_ids": ["spreadsheet.formula_error_troubleshooting#tb5"],
                        "fact_ids": ["spreadsheet.formula_error_troubleshooting#f5"]
                    }
                },
                {
                    "type": "up_next",
                    "block_id": f"{T1}.s17.up_next",
                    "title": "Next: Pivot Tables",
                    "text": "In the next tile you'll build PivotTables that summarise your Orders data by city, status, and amount — no formulas required."
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": [
                    "spreadsheet.vlookup_xlookup",
                    "spreadsheet.index_match",
                    "spreadsheet.formula_error_troubleshooting"
                ],
                "teaching_block_ids": ["spreadsheet.formula_error_troubleshooting#tb5"],
                "fact_ids": ["spreadsheet.formula_error_troubleshooting#f5"]
            }
        }
    ],

    # ── Remediation steps ──────────────────────────────────────────────────
    "remediation_steps": [
        # r01: for s04 check (vlookup_xlookup#f3 — HLOOKUP row_index_num)
        {
            "step_id": f"{T1}.r01",
            "type": "remediation",
            "concept_ids": ["spreadsheet.vlookup_xlookup"],
            "eyebrow": "Let's Revisit",
            "title": "VLOOKUP vs. HLOOKUP: Columns vs. Rows",
            "lede": "A clear contrast between the two functions shows which argument controls the return position.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T1}.r01.p1",
                    "role": "example",
                    "text": "VLOOKUP searches down the leftmost column and uses col_index_num to pick which column to return — =VLOOKUP(F2,Drivers!A:B,2,FALSE) returns the value in the 2nd column. HLOOKUP searches across the top row and uses row_index_num to pick which row to return — =HLOOKUP(\"Delivered\",A1:D3,2,FALSE) returns the value in the 2nd row. The key difference: VLOOKUP counts columns; HLOOKUP counts rows.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.vlookup_xlookup"],
                        "teaching_block_ids": ["spreadsheet.vlookup_xlookup#tb3"],
                        "fact_ids": ["spreadsheet.vlookup_xlookup#f3"]
                    }
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["spreadsheet.vlookup_xlookup"],
                "teaching_block_ids": ["spreadsheet.vlookup_xlookup#tb3"],
                "fact_ids": ["spreadsheet.vlookup_xlookup#f3"]
            }
        },
        # r02: for s09 check (index_match#f1,f3,f4)
        {
            "step_id": f"{T1}.r02",
            "type": "remediation",
            "concept_ids": ["spreadsheet.index_match"],
            "eyebrow": "Let's Revisit",
            "title": "INDEX and MATCH: Two Steps, One Result",
            "lede": "See how MATCH produces a row number and INDEX uses it to return a value.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T1}.r02.p1",
                    "role": "example",
                    "text": "On the QuickDeliver Orders sheet, driver ID D03 is in cell F4. MATCH(F4,Drivers!B:B,0) searches column B of the Drivers sheet for D03 and returns its row position — say 4. INDEX(Drivers!A:A,4) then returns the value in row 4 of column A, which is the driver name. The full formula =INDEX(Drivers!A:A,MATCH(F4,Drivers!B:B,0)) combines both steps. VLOOKUP cannot do this because the return column (A) is to the left of the key column (B).",
                    "lineage": {
                        "concept_ids": ["spreadsheet.index_match"],
                        "teaching_block_ids": ["spreadsheet.index_match#tb4"],
                        "fact_ids": [
                            "spreadsheet.index_match#f1",
                            "spreadsheet.index_match#f3",
                            "spreadsheet.index_match#f4"
                        ]
                    }
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["spreadsheet.index_match"],
                "teaching_block_ids": ["spreadsheet.index_match#tb4"],
                "fact_ids": [
                    "spreadsheet.index_match#f1",
                    "spreadsheet.index_match#f3",
                    "spreadsheet.index_match#f4"
                ]
            }
        },
        # r03: for s14 check (#VALUE! — f3, f4)
        {
            "step_id": f"{T1}.r03",
            "type": "remediation",
            "concept_ids": ["spreadsheet.formula_error_troubleshooting"],
            "eyebrow": "Let's Revisit",
            "title": "#VALUE!: Text in a Number Cell",
            "lede": "See the exact difference between an arithmetic formula and SUM when one cell holds text.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T1}.r03.p1",
                    "role": "example",
                    "text": "In the QuickDeliver Orders sheet, amount in row 16 holds the text \"N/A\" instead of a number. The formula =D2+D16 returns #VALUE! because the + operator cannot add text. The formula =SUM(D2:D21) returns a total because SUM ignores text values and sums only the numeric ones. Switching from + to SUM resolves the #VALUE! error without removing the text cell.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.formula_error_troubleshooting"],
                        "teaching_block_ids": ["spreadsheet.formula_error_troubleshooting#tb4"],
                        "fact_ids": [
                            "spreadsheet.formula_error_troubleshooting#f3",
                            "spreadsheet.formula_error_troubleshooting#f4"
                        ]
                    }
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["spreadsheet.formula_error_troubleshooting"],
                "teaching_block_ids": ["spreadsheet.formula_error_troubleshooting#tb4"],
                "fact_ids": [
                    "spreadsheet.formula_error_troubleshooting#f3",
                    "spreadsheet.formula_error_troubleshooting#f4"
                ]
            }
        },
        # r04: for s15 check (#VALUE! propagation — f5)
        {
            "step_id": f"{T1}.r04",
            "type": "remediation",
            "concept_ids": ["spreadsheet.formula_error_troubleshooting"],
            "eyebrow": "Let's Revisit",
            "title": "#VALUE! Spreads Upward",
            "lede": "One bad cell's error can propagate into any formula that references it.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T1}.r04.p1",
                    "role": "example",
                    "text": "If cell D16 already contains a #VALUE! error, then =AVERAGE(D2:D21) will also return #VALUE! — not a number — because AVERAGE and SUM propagate errors from cells they reference. The error in D16 spreads into any formula built on top of it. Fixing D16 (for example, by replacing the text with a valid number) clears the error from all dependent formulas at once.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.formula_error_troubleshooting"],
                        "teaching_block_ids": ["spreadsheet.formula_error_troubleshooting#tb5"],
                        "fact_ids": ["spreadsheet.formula_error_troubleshooting#f5"]
                    }
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["spreadsheet.formula_error_troubleshooting"],
                "teaching_block_ids": ["spreadsheet.formula_error_troubleshooting#tb5"],
                "fact_ids": ["spreadsheet.formula_error_troubleshooting#f5"]
            }
        }
    ]
}

out["tiles"].append(tile1)


# ─────────────────────────────────────────────────────────────────────────────
# TILE 2: tile_spreadsheet_cleaning_cross_sheet
# Concepts: remove_duplicates_cleaning, text_to_columns_split, cross_sheet_references
# ─────────────────────────────────────────────────────────────────────────────
T2 = "tile_spreadsheet_cleaning_cross_sheet"

tile2 = {
    "tile_id": T2,
    "title": "Removing Duplicates and Splitting Text",
    "summary": "Clean your Orders data by removing duplicate rows, split combined text into separate columns, and write formulas that reference cells on other sheets.",
    "steps": [

        # s01 — explainer: remove_duplicates + visual (before_after)
        {
            "step_id": f"{T2}.s01",
            "type": "explainer",
            "concept_ids": ["spreadsheet.remove_duplicates_cleaning"],
            "eyebrow": "Data Cleaning",
            "title": "Removing Duplicate Rows Permanently",
            "lede": "When the same order number appears twice in your Orders sheet, Excel's Remove Duplicates tool clears the extras — but the deletion is permanent.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T2}.s01.p1",
                    "role": "intro",
                    "text": "Say the same order number shows up twice in your Orders sheet — maybe it was entered once by mistake. Excel has a dedicated tool for this, but it's worth being careful with.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.remove_duplicates_cleaning"],
                        "teaching_block_ids": ["spreadsheet.remove_duplicates_cleaning#tb1"],
                        "fact_ids": []
                    }
                },
                {
                    "type": "prose",
                    "block_id": f"{T2}.s01.p2",
                    "role": "mechanism",
                    "text": "When you use the Remove Duplicates feature, the duplicate data is permanently deleted, so it's a good idea to copy the original data to another worksheet before removing duplicates.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.remove_duplicates_cleaning"],
                        "teaching_block_ids": ["spreadsheet.remove_duplicates_cleaning#tb2"],
                        "fact_ids": ["spreadsheet.remove_duplicates_cleaning#f1"]
                    }
                },
                {
                    "type": "prose",
                    "block_id": f"{T2}.s01.p3",
                    "role": "example",
                    "text": "To remove duplicates, select the range of cells that has duplicate values, select Data > Remove Duplicates, and then check or uncheck the columns under Columns to choose which columns are used to identify a duplicate row. On your Orders sheet, checking only the order_id column means two rows with the same order number get treated as duplicates even if other columns differ — while checking every column would only catch rows that match everywhere.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.remove_duplicates_cleaning"],
                        "teaching_block_ids": ["spreadsheet.remove_duplicates_cleaning#tb3"],
                        "fact_ids": ["spreadsheet.remove_duplicates_cleaning#f2"]
                    }
                },
                {
                    "type": "before_after",
                    "block_id": f"{T2}.s01.ba1",
                    "before": {
                        "type": "spreadsheet_grid",
                        "asset_ref": {"asset_id": "asset_orders_clean", "variant_id": "messy", "columns": ["order_id", "city", "status"]},
                        "sheet_name": "Orders",
                        "range": "A1:C7",
                        "annotations": [
                            {"target": "A3", "text": "LG-2005 — duplicate row (first occurrence)"},
                            {"target": "A4", "text": "LG-2005 — duplicate row (second occurrence, highlighted)"}
                        ]
                    },
                    "after": {
                        "type": "spreadsheet_grid",
                        "asset_ref": {"asset_id": "asset_orders_clean", "variant_id": None, "columns": ["order_id", "city", "status"]},
                        "sheet_name": "Orders",
                        "range": "A1:C6",
                        "annotations": [
                            {"target": "A3", "text": "LG-2005 — duplicate removed; row count reduced by 1"}
                        ]
                    },
                    "change_summary": "Remove Duplicates on the order_id column deleted the second LG-2005 row permanently.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.remove_duplicates_cleaning"],
                        "teaching_block_ids": [
                            "spreadsheet.remove_duplicates_cleaning#tb2",
                            "spreadsheet.remove_duplicates_cleaning#tb3"
                        ],
                        "fact_ids": [
                            "spreadsheet.remove_duplicates_cleaning#f1",
                            "spreadsheet.remove_duplicates_cleaning#f2"
                        ],
                        "anchors": ["spreadsheet.remove_duplicates_cleaning#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["spreadsheet.remove_duplicates_cleaning"],
                "teaching_block_ids": [
                    "spreadsheet.remove_duplicates_cleaning#tb1",
                    "spreadsheet.remove_duplicates_cleaning#tb2",
                    "spreadsheet.remove_duplicates_cleaning#tb3"
                ],
                "fact_ids": [
                    "spreadsheet.remove_duplicates_cleaning#f1",
                    "spreadsheet.remove_duplicates_cleaning#f2"
                ],
                "anchors": ["spreadsheet.remove_duplicates_cleaning#visual"]
            }
        },

        # s02 — video: remove_duplicates
        {
            "step_id": f"{T2}.s02",
            "type": "video",
            "concept_ids": ["spreadsheet.remove_duplicates_cleaning"],
            "eyebrow": "Data Cleaning",
            "title": "Remove Duplicates in Action",
            "blocks": [
                {
                    "type": "media_group",
                    "block_id": f"{T2}.s02.mg1",
                    "segment_ids": ["seg_spreadsheet.remove_duplicates_cleaning_ADArCWLz55Y_34_189"]
                }
            ],
            "lineage": {
                "concept_ids": ["spreadsheet.remove_duplicates_cleaning"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "spreadsheet.remove_duplicates_cleaning#f1",
                    "spreadsheet.remove_duplicates_cleaning#f2"
                ],
                "segment_ids": ["seg_spreadsheet.remove_duplicates_cleaning_ADArCWLz55Y_34_189"]
            }
        },

        # s03 — check: permanent deletion (framing only)
        {
            "step_id": f"{T2}.s03",
            "type": "check",
            "concept_ids": ["spreadsheet.remove_duplicates_cleaning"],
            "eyebrow": "Quick Check",
            "title": "Permanent Deletion and the Copy Precaution",
            "lede": "Confirm you understand what Remove Duplicates does to your data.",
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["spreadsheet.remove_duplicates_cleaning"],
                "teaching_block_ids": [],
                "fact_ids": ["spreadsheet.remove_duplicates_cleaning#f1"],
                "anchors": ["spreadsheet.remove_duplicates_cleaning#assessment:identify_permanent_deletion_and_copy_precaution"]
            }
        },

        # s04 — hands_on: remove_duplicates practice (framing only)
        {
            "step_id": f"{T2}.s04",
            "type": "hands_on",
            "concept_ids": ["spreadsheet.remove_duplicates_cleaning"],
            "eyebrow": "Practice",
            "title": "Configure and Run Remove Duplicates",
            "lede": "Select the correct columns to identify duplicate rows in the Orders sheet and run the tool.",
            "reward": {"gems": 10},
            "lineage": {
                "concept_ids": ["spreadsheet.remove_duplicates_cleaning"],
                "teaching_block_ids": [],
                "fact_ids": ["spreadsheet.remove_duplicates_cleaning#f2"],
                "anchors": [
                    "spreadsheet.remove_duplicates_cleaning#practice",
                    "spreadsheet.remove_duplicates_cleaning#assessment:configure_and_run_remove_duplicates_with_column_selection"
                ]
            }
        },

        # s05 — explainer: text_to_columns + visual (before_after)
        {
            "step_id": f"{T2}.s05",
            "type": "explainer",
            "concept_ids": ["spreadsheet.text_to_columns_split"],
            "eyebrow": "Text Splitting",
            "title": "Splitting One Column into Two",
            "lede": "When a single cell holds combined text like \"Lagos,Nigeria\", Text to Columns splits it into separate columns using a delimiter you choose.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T2}.s05.p1",
                    "role": "definition",
                    "text": "To split text into columns, select the cell or column that contains the text, select Data > Text to Columns, choose Delimited, select the delimiter(s) such as Comma or Space, choose the destination for the split data, and select Finish. If your Orders sheet has a single column holding \"Lagos,Nigeria\" as one text value, running Text to Columns with Comma as the delimiter splits it into two columns.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.text_to_columns_split"],
                        "teaching_block_ids": [
                            "spreadsheet.text_to_columns_split#tb1",
                            "spreadsheet.text_to_columns_split#tb2"
                        ],
                        "fact_ids": ["spreadsheet.text_to_columns_split#f1"]
                    }
                },
                {
                    "type": "before_after",
                    "block_id": f"{T2}.s05.ba1",
                    "before": {
                        "type": "spreadsheet_grid",
                        "asset_ref": {"asset_id": "asset_drivers_vlookup", "variant_id": None, "columns": ["driver_name"]},
                        "sheet_name": "Drivers",
                        "range": "A1:A6",
                        "annotations": [
                            {"target": "A1", "text": "Full Name — single column, space-delimited"},
                            {"target": "A2", "text": "Amara Okafor"}
                        ]
                    },
                    "after": {
                        "type": "spreadsheet_grid",
                        "asset_ref": {"asset_id": "asset_drivers_vlookup", "variant_id": None, "columns": ["driver_name"]},
                        "sheet_name": "Drivers",
                        "range": "A1:B6",
                        "annotations": [
                            {"target": "A1", "text": "First Name"},
                            {"target": "B1", "text": "Last Name — split by Space delimiter"}
                        ]
                    },
                    "change_summary": "Text to Columns with Space delimiter split the Full Name column into First Name and Last Name.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.text_to_columns_split"],
                        "teaching_block_ids": [
                            "spreadsheet.text_to_columns_split#tb1",
                            "spreadsheet.text_to_columns_split#tb2"
                        ],
                        "fact_ids": ["spreadsheet.text_to_columns_split#f1"],
                        "anchors": ["spreadsheet.text_to_columns_split#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["spreadsheet.text_to_columns_split"],
                "teaching_block_ids": [
                    "spreadsheet.text_to_columns_split#tb1",
                    "spreadsheet.text_to_columns_split#tb2"
                ],
                "fact_ids": ["spreadsheet.text_to_columns_split#f1"],
                "anchors": ["spreadsheet.text_to_columns_split#visual"]
            }
        },

        # s06 — video: text_to_columns
        {
            "step_id": f"{T2}.s06",
            "type": "video",
            "concept_ids": ["spreadsheet.text_to_columns_split"],
            "eyebrow": "Text Splitting",
            "title": "Text to Columns Wizard Step by Step",
            "blocks": [
                {
                    "type": "media_group",
                    "block_id": f"{T2}.s06.mg1",
                    "segment_ids": ["seg_spreadsheet.text_to_columns_split_9barqPO2pvg_0_180"]
                }
            ],
            "lineage": {
                "concept_ids": ["spreadsheet.text_to_columns_split"],
                "teaching_block_ids": [],
                "fact_ids": ["spreadsheet.text_to_columns_split#f1"],
                "segment_ids": ["seg_spreadsheet.text_to_columns_split_9barqPO2pvg_0_180"]
            }
        },

        # s07 — check: text_to_columns (framing only)
        {
            "step_id": f"{T2}.s07",
            "type": "check",
            "concept_ids": ["spreadsheet.text_to_columns_split"],
            "eyebrow": "Quick Check",
            "title": "Split a Delimited Column",
            "lede": "Choose the correct steps to split a comma-delimited column using Text to Columns.",
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["spreadsheet.text_to_columns_split"],
                "teaching_block_ids": [],
                "fact_ids": ["spreadsheet.text_to_columns_split#f1"],
                "anchors": ["spreadsheet.text_to_columns_split#assessment:split_delimited_column_with_text_to_columns"]
            }
        },

        # s08 — hands_on: text_to_columns practice (framing only)
        {
            "step_id": f"{T2}.s08",
            "type": "hands_on",
            "concept_ids": ["spreadsheet.text_to_columns_split"],
            "eyebrow": "Practice",
            "title": "Split the Full Name Column",
            "lede": "Use Data > Text to Columns with Space as the delimiter to split the driver name column into First Name and Last Name.",
            "reward": {"gems": 10},
            "lineage": {
                "concept_ids": ["spreadsheet.text_to_columns_split"],
                "teaching_block_ids": [],
                "fact_ids": ["spreadsheet.text_to_columns_split#f1"],
                "anchors": [
                    "spreadsheet.text_to_columns_split#practice",
                    "spreadsheet.text_to_columns_split#assessment:split_delimited_column_with_text_to_columns"
                ]
            }
        },

        # s09 — explainer: cross_sheet_references + visual (annotated_image)
        {
            "step_id": f"{T2}.s09",
            "type": "explainer",
            "concept_ids": ["spreadsheet.cross_sheet_references"],
            "eyebrow": "Cross-Sheet References",
            "title": "Referencing Cells on Another Sheet",
            "lede": "A formula on your Orders sheet can pull a value directly from your Drivers sheet — or even from a different workbook — using a cross-sheet reference.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T2}.s09.p1",
                    "role": "definition",
                    "text": "A formula can refer to a cell on another sheet in the same workbook by writing the sheet name followed by an exclamation point (!) and then the cell or range reference, for example Marketing!B1. So a formula on your Orders sheet that needs a value sitting on your Drivers sheet could reference Drivers!B1.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.cross_sheet_references"],
                        "teaching_block_ids": ["spreadsheet.cross_sheet_references#tb1"],
                        "fact_ids": ["spreadsheet.cross_sheet_references#f1"]
                    }
                },
                {
                    "type": "prose",
                    "block_id": f"{T2}.s09.p2",
                    "role": "mechanism",
                    "text": "If the referenced worksheet's name contains spaces or numbers, the name must be enclosed in single quotation marks in the reference, for example ='January Revenue'!A1. So if you renamed your drivers tab to \"Driver List\", a reference to it would need to be written 'Driver List'!A1, not Driver List!A1.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.cross_sheet_references"],
                        "teaching_block_ids": ["spreadsheet.cross_sheet_references#tb2"],
                        "fact_ids": ["spreadsheet.cross_sheet_references#f2"]
                    }
                },
                {
                    "type": "prose",
                    "block_id": f"{T2}.s09.p3",
                    "role": "mechanism",
                    "text": "A workbook link to a cell range in another workbook, when the source workbook is open, includes the workbook name in square brackets, followed by the worksheet name, an exclamation point, and the cells the formula depends on, for example =SUM([Budget.xlsx]Annual!C10:C25).",
                    "lineage": {
                        "concept_ids": ["spreadsheet.cross_sheet_references"],
                        "teaching_block_ids": ["spreadsheet.cross_sheet_references#tb3"],
                        "fact_ids": ["spreadsheet.cross_sheet_references#f3"]
                    }
                },
                {
                    "type": "annotated_image",
                    "block_id": f"{T2}.s09.img1",
                    "asset_id": "asset_orders_clean",
                    "alt_text": "Formula bar showing a cross-sheet reference. Top example: Drivers!B1 with callouts labelling the sheet name, exclamation point, and cell address. Bottom example: 'January Revenue'!A1 with a callout on the single quotes around the sheet name that contains a space. A third example shows [Budget.xlsx]Annual!C10:C25 with the workbook name in square brackets labelled.",
                    "hotspots": [
                        {"x": 0.05, "y": 0.15, "w": 0.25, "h": 0.10, "label": "Sheet name", "detail": "Drivers — no spaces, no quotes needed"},
                        {"x": 0.30, "y": 0.15, "w": 0.05, "h": 0.10, "label": "!", "detail": "Exclamation point separates sheet name from cell address"},
                        {"x": 0.35, "y": 0.15, "w": 0.15, "h": 0.10, "label": "Cell address", "detail": "B1 — the cell being referenced"},
                        {"x": 0.05, "y": 0.40, "w": 0.35, "h": 0.10, "label": "Single quotes", "detail": "'January Revenue' — required because the name contains a space"},
                        {"x": 0.05, "y": 0.65, "w": 0.20, "h": 0.10, "label": "[Budget.xlsx]", "detail": "Workbook name in square brackets for a cross-workbook link"}
                    ],
                    "lineage": {
                        "concept_ids": ["spreadsheet.cross_sheet_references"],
                        "teaching_block_ids": [
                            "spreadsheet.cross_sheet_references#tb1",
                            "spreadsheet.cross_sheet_references#tb2",
                            "spreadsheet.cross_sheet_references#tb3"
                        ],
                        "fact_ids": [
                            "spreadsheet.cross_sheet_references#f1",
                            "spreadsheet.cross_sheet_references#f2",
                            "spreadsheet.cross_sheet_references#f3"
                        ],
                        "anchors": ["spreadsheet.cross_sheet_references#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["spreadsheet.cross_sheet_references"],
                "teaching_block_ids": [
                    "spreadsheet.cross_sheet_references#tb1",
                    "spreadsheet.cross_sheet_references#tb2",
                    "spreadsheet.cross_sheet_references#tb3"
                ],
                "fact_ids": [
                    "spreadsheet.cross_sheet_references#f1",
                    "spreadsheet.cross_sheet_references#f2",
                    "spreadsheet.cross_sheet_references#f3"
                ],
                "anchors": ["spreadsheet.cross_sheet_references#visual"]
            }
        },

        # s10 — check: cross-sheet + cross-workbook (framing only)
        {
            "step_id": f"{T2}.s10",
            "type": "check",
            "concept_ids": ["spreadsheet.cross_sheet_references"],
            "eyebrow": "Quick Check",
            "title": "Same-Workbook and Cross-Workbook References",
            "lede": "Choose the correct reference syntax for same-workbook and cross-workbook scenarios.",
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["spreadsheet.cross_sheet_references"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "spreadsheet.cross_sheet_references#f1",
                    "spreadsheet.cross_sheet_references#f3"
                ],
                "anchors": [
                    "spreadsheet.cross_sheet_references#assessment:write_same_workbook_cross_sheet_reference",
                    "spreadsheet.cross_sheet_references#assessment:write_cross_workbook_link_with_square_bracket_syntax"
                ]
            }
        },

        # s11 — check: select correct syntax (framing only)
        {
            "step_id": f"{T2}.s11",
            "type": "check",
            "concept_ids": ["spreadsheet.cross_sheet_references"],
            "eyebrow": "Quick Check",
            "title": "Choosing the Right Reference Syntax",
            "lede": "Given a formula requirement, select the correctly formed cross-sheet reference.",
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["spreadsheet.cross_sheet_references"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "spreadsheet.cross_sheet_references#f1",
                    "spreadsheet.cross_sheet_references#f2",
                    "spreadsheet.cross_sheet_references#f3"
                ],
                "anchors": ["spreadsheet.cross_sheet_references#assessment:select_correct_reference_syntax_given_formula_requirement"]
            }
        },

        # s12 — hands_on: cross_sheet practice (framing only)
        {
            "step_id": f"{T2}.s12",
            "type": "hands_on",
            "concept_ids": ["spreadsheet.cross_sheet_references"],
            "eyebrow": "Practice",
            "title": "Write a Cross-Sheet Reference",
            "lede": "Write a formula in cell B2 of a Summary sheet that pulls the value from cell B4 on a sheet named Q1 Sales.",
            "reward": {"gems": 10},
            "lineage": {
                "concept_ids": ["spreadsheet.cross_sheet_references"],
                "teaching_block_ids": [],
                "fact_ids": ["spreadsheet.cross_sheet_references#f2"],
                "anchors": [
                    "spreadsheet.cross_sheet_references#practice",
                    "spreadsheet.cross_sheet_references#assessment:quote_sheet_names_with_spaces_or_numbers"
                ]
            }
        },

        # s13 — recap
        {
            "step_id": f"{T2}.s13",
            "type": "recap",
            "concept_ids": [
                "spreadsheet.remove_duplicates_cleaning",
                "spreadsheet.text_to_columns_split",
                "spreadsheet.cross_sheet_references"
            ],
            "eyebrow": "Recap",
            "title": "Cleaning, Splitting, and Linking — Key Points",
            "lede": "You can now remove duplicate rows safely, split delimited text into columns, and reference cells across sheets.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T2}.s13.p1",
                    "role": "takeaway",
                    "text": "Remove Duplicates permanently deletes matched rows — copy your data first. Choose which columns define a duplicate: checking only order_id catches same-ID rows even if other columns differ. Text to Columns splits a delimited column in three steps: choose Delimited, pick the delimiter (Comma, Space, or other), then Finish. Cross-sheet references use the syntax SheetName!CellAddress; if the sheet name contains spaces or numbers, wrap it in single quotes: 'Sheet Name'!A1. Cross-workbook links add the workbook name in square brackets: [Budget.xlsx]Annual!C10.",
                    "lineage": {
                        "concept_ids": [
                            "spreadsheet.remove_duplicates_cleaning",
                            "spreadsheet.text_to_columns_split",
                            "spreadsheet.cross_sheet_references"
                        ],
                        "teaching_block_ids": [],
                        "fact_ids": []
                    }
                },
                {
                    "type": "up_next",
                    "block_id": f"{T2}.s13.up_next",
                    "title": "Next: Formula Syntax and References",
                    "text": "In the next tile you'll write formulas with arithmetic operators, understand operator precedence, and lock cells with absolute references using the $ sign."
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": [
                    "spreadsheet.remove_duplicates_cleaning",
                    "spreadsheet.text_to_columns_split",
                    "spreadsheet.cross_sheet_references"
                ],
                "teaching_block_ids": [],
                "fact_ids": []
            }
        }
    ],

    # ── Remediation steps ──────────────────────────────────────────────────
    "remediation_steps": [
        # r01: for s03 check (remove_duplicates#f1 — permanent deletion)
        {
            "step_id": f"{T2}.r01",
            "type": "remediation",
            "concept_ids": ["spreadsheet.remove_duplicates_cleaning"],
            "eyebrow": "Let's Revisit",
            "title": "Why Copy Before Removing Duplicates",
            "lede": "See the contrast between a reversible and an irreversible operation.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T2}.r01.p1",
                    "role": "example",
                    "text": "Sorting your Orders sheet is reversible — you can sort again in a different order. Remove Duplicates is not: once you click OK, the matched rows are gone and there is no undo after you save. Copying the sheet to a backup tab first means you can always recover the original rows if you removed too many. The copy step takes seconds; recovering without it can be impossible.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.remove_duplicates_cleaning"],
                        "teaching_block_ids": ["spreadsheet.remove_duplicates_cleaning#tb2"],
                        "fact_ids": ["spreadsheet.remove_duplicates_cleaning#f1"]
                    }
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["spreadsheet.remove_duplicates_cleaning"],
                "teaching_block_ids": ["spreadsheet.remove_duplicates_cleaning#tb2"],
                "fact_ids": ["spreadsheet.remove_duplicates_cleaning#f1"]
            }
        },
        # r02: for s07 check (text_to_columns#f1)
        {
            "step_id": f"{T2}.r02",
            "type": "remediation",
            "concept_ids": ["spreadsheet.text_to_columns_split"],
            "eyebrow": "Let's Revisit",
            "title": "Text to Columns: The Three Steps",
            "lede": "Walk through the wizard steps one more time with a concrete example.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T2}.r02.p1",
                    "role": "example",
                    "text": "Starting from a column that holds \"Lagos,Nigeria\" in each cell: (1) select the column, (2) click Data > Text to Columns, (3) choose Delimited and click Next, (4) check Comma as the delimiter — the preview shows the split — (5) choose a destination cell and click Finish. The single column becomes two: one with \"Lagos\" and one with \"Nigeria\". Choosing Space instead of Comma would split on the space character instead.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.text_to_columns_split"],
                        "teaching_block_ids": ["spreadsheet.text_to_columns_split#tb1", "spreadsheet.text_to_columns_split#tb2"],
                        "fact_ids": ["spreadsheet.text_to_columns_split#f1"]
                    }
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["spreadsheet.text_to_columns_split"],
                "teaching_block_ids": ["spreadsheet.text_to_columns_split#tb1", "spreadsheet.text_to_columns_split#tb2"],
                "fact_ids": ["spreadsheet.text_to_columns_split#f1"]
            }
        },
        # r03: for s10 check (cross_sheet#f1,f3)
        {
            "step_id": f"{T2}.r03",
            "type": "remediation",
            "concept_ids": ["spreadsheet.cross_sheet_references"],
            "eyebrow": "Let's Revisit",
            "title": "Cross-Sheet vs. Cross-Workbook Syntax",
            "lede": "Compare the two reference forms side by side.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T2}.r03.p1",
                    "role": "example",
                    "text": "Same workbook, simple sheet name: Drivers!B1 — sheet name, exclamation point, cell address. Same workbook, sheet name with a space: 'January Revenue'!A1 — single quotes wrap the name. Different workbook (source open): =SUM([Budget.xlsx]Annual!C10:C25) — workbook name in square brackets before the sheet name. The square brackets only appear for cross-workbook links; within the same workbook you never use them.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.cross_sheet_references"],
                        "teaching_block_ids": [
                            "spreadsheet.cross_sheet_references#tb1",
                            "spreadsheet.cross_sheet_references#tb3"
                        ],
                        "fact_ids": [
                            "spreadsheet.cross_sheet_references#f1",
                            "spreadsheet.cross_sheet_references#f3"
                        ]
                    }
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["spreadsheet.cross_sheet_references"],
                "teaching_block_ids": [
                    "spreadsheet.cross_sheet_references#tb1",
                    "spreadsheet.cross_sheet_references#tb3"
                ],
                "fact_ids": [
                    "spreadsheet.cross_sheet_references#f1",
                    "spreadsheet.cross_sheet_references#f3"
                ]
            }
        },
        # r04: for s11 check (cross_sheet#f1,f2,f3)
        {
            "step_id": f"{T2}.r04",
            "type": "remediation",
            "concept_ids": ["spreadsheet.cross_sheet_references"],
            "eyebrow": "Let's Revisit",
            "title": "When Do Sheet Names Need Quotes?",
            "lede": "The quoting rule is simple: any name with a space or a number at the start needs single quotes.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T2}.r04.p1",
                    "role": "example",
                    "text": "Drivers!B1 — no quotes needed; the name has no spaces or leading numbers. 'January Revenue'!A1 — quotes required; the name contains a space. '2024 Orders'!C5 — quotes required; the name starts with a number. Forgetting the quotes when they're needed causes a formula error. A safe habit: always click the sheet tab while typing the formula and let Excel insert the correct syntax automatically.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.cross_sheet_references"],
                        "teaching_block_ids": [
                            "spreadsheet.cross_sheet_references#tb1",
                            "spreadsheet.cross_sheet_references#tb2"
                        ],
                        "fact_ids": [
                            "spreadsheet.cross_sheet_references#f1",
                            "spreadsheet.cross_sheet_references#f2"
                        ]
                    }
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["spreadsheet.cross_sheet_references"],
                "teaching_block_ids": [
                    "spreadsheet.cross_sheet_references#tb1",
                    "spreadsheet.cross_sheet_references#tb2"
                ],
                "fact_ids": [
                    "spreadsheet.cross_sheet_references#f1",
                    "spreadsheet.cross_sheet_references#f2"
                ]
            }
        }
    ]
}

out["tiles"].append(tile2)


# ─────────────────────────────────────────────────────────────────────────────
# TILE 3: tile_spreadsheet_sorting_filtering
# Concepts: sorting, filtering
# ─────────────────────────────────────────────────────────────────────────────
T3 = "tile_spreadsheet_sorting_filtering"

tile3 = {
    "tile_id": T3,
    "title": "Sorting and Filtering Data",
    "summary": "Reorder your Orders sheet by one or more columns, and use AutoFilter to show only the rows that meet your criteria.",
    "steps": [

        # s01 — explainer: sorting + visual (annotated_image)
        {
            "step_id": f"{T3}.s01",
            "type": "explainer",
            "concept_ids": ["spreadsheet.sorting"],
            "eyebrow": "Sorting",
            "title": "Putting Your Orders in Order",
            "lede": "Sorting rearranges your Orders sheet rows by the values in one or more columns — oldest first, largest first, or any combination.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T3}.s01.p1",
                    "role": "intro",
                    "text": "With a week of orders in your Orders sheet, you often want them in a particular order rather than the order they were entered in — oldest first, or largest amount first.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.sorting"],
                        "teaching_block_ids": ["spreadsheet.sorting#tb1"],
                        "fact_ids": []
                    }
                },
                {
                    "type": "prose",
                    "block_id": f"{T3}.s01.p2",
                    "role": "mechanism",
                    "text": "To sort a column of numbers, select a cell in that column and, on the Data tab in the Sort & Filter group, select Sort Smallest to Largest or Sort Largest to Smallest. To sort a column of dates or times, select a cell in that column and select Sort Oldest to Newest or Sort Newest to Oldest instead.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.sorting"],
                        "teaching_block_ids": ["spreadsheet.sorting#tb2"],
                        "fact_ids": [
                            "spreadsheet.sorting#f1",
                            "spreadsheet.sorting#f2"
                        ]
                    }
                },
                {
                    "type": "prose",
                    "block_id": f"{T3}.s01.p3",
                    "role": "mechanism",
                    "text": "To sort by more than one column, open the Sort dialog box from Data > Sort, choose the first column to sort by in the Sort by box, then select Add Level to add another column to sort by. Entries higher in the list are sorted before entries lower in the list. Each level added in the dialog box has its own Order setting, so different columns within the same multi-level sort can be sorted in different directions.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.sorting"],
                        "teaching_block_ids": ["spreadsheet.sorting#tb3"],
                        "fact_ids": [
                            "spreadsheet.sorting#f3",
                            "spreadsheet.sorting#f4"
                        ]
                    }
                },
                {
                    "type": "annotated_image",
                    "block_id": f"{T3}.s01.img1",
                    "asset_id": "asset_orders_clean",
                    "alt_text": "Excel Sort dialog with two levels configured. Level 1 shows Sort by: order_date, Order: Oldest to Newest. Level 2 shows Then by: amount, Order: Largest to Smallest. Each level has its own independent Order dropdown.",
                    "hotspots": [
                        {"x": 0.05, "y": 0.25, "w": 0.30, "h": 0.10, "label": "Level 1 — order_date", "detail": "Sort by: order_date, Order: Oldest to Newest"},
                        {"x": 0.05, "y": 0.45, "w": 0.30, "h": 0.10, "label": "Level 2 — amount", "detail": "Then by: amount, Order: Largest to Smallest"},
                        {"x": 0.60, "y": 0.25, "w": 0.30, "h": 0.10, "label": "Independent Order dropdown", "detail": "Each level has its own direction — Oldest to Newest here"},
                        {"x": 0.60, "y": 0.45, "w": 0.30, "h": 0.10, "label": "Independent Order dropdown", "detail": "Largest to Smallest for the tiebreaker level"}
                    ],
                    "lineage": {
                        "concept_ids": ["spreadsheet.sorting"],
                        "teaching_block_ids": [
                            "spreadsheet.sorting#tb1",
                            "spreadsheet.sorting#tb2",
                            "spreadsheet.sorting#tb3"
                        ],
                        "fact_ids": [
                            "spreadsheet.sorting#f1",
                            "spreadsheet.sorting#f2",
                            "spreadsheet.sorting#f3",
                            "spreadsheet.sorting#f4"
                        ],
                        "anchors": ["spreadsheet.sorting#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["spreadsheet.sorting"],
                "teaching_block_ids": [
                    "spreadsheet.sorting#tb1",
                    "spreadsheet.sorting#tb2",
                    "spreadsheet.sorting#tb3"
                ],
                "fact_ids": [
                    "spreadsheet.sorting#f1",
                    "spreadsheet.sorting#f2",
                    "spreadsheet.sorting#f3",
                    "spreadsheet.sorting#f4"
                ],
                "anchors": ["spreadsheet.sorting#visual"]
            }
        },

        # s02 — video: sorting
        {
            "step_id": f"{T3}.s02",
            "type": "video",
            "concept_ids": ["spreadsheet.sorting"],
            "eyebrow": "Sorting",
            "title": "Single-Column Sort and Multi-Level Sort Dialog",
            "blocks": [
                {
                    "type": "media_group",
                    "block_id": f"{T3}.s02.mg1",
                    "segment_ids": ["seg_spreadsheet.sorting_Aw4ZHT3SYzc_45_352"]
                }
            ],
            "lineage": {
                "concept_ids": ["spreadsheet.sorting"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "spreadsheet.sorting#f1",
                    "spreadsheet.sorting#f3",
                    "spreadsheet.sorting#f4"
                ],
                "segment_ids": ["seg_spreadsheet.sorting_Aw4ZHT3SYzc_45_352"]
            }
        },

        # s03 — explainer: multi-level sort example
        {
            "step_id": f"{T3}.s03",
            "type": "explainer",
            "concept_ids": ["spreadsheet.sorting"],
            "eyebrow": "Sorting",
            "title": "A Two-Level Sort in Practice",
            "lede": "Sorting by date first and amount second puts same-day orders in descending amount order while the days stay in ascending order.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T3}.s03.p1",
                    "role": "example",
                    "text": "Sorting your Orders sheet by order_date oldest to newest, and adding a second level that sorts amount largest to smallest as a tiebreaker, puts same-day orders in descending amount order while the days themselves stay in ascending order.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.sorting"],
                        "teaching_block_ids": ["spreadsheet.sorting#tb4"],
                        "fact_ids": [
                            "spreadsheet.sorting#f3",
                            "spreadsheet.sorting#f4"
                        ]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["spreadsheet.sorting"],
                "teaching_block_ids": ["spreadsheet.sorting#tb4"],
                "fact_ids": [
                    "spreadsheet.sorting#f3",
                    "spreadsheet.sorting#f4"
                ]
            }
        },

        # s04 — check: multi-level sort (framing only)
        {
            "step_id": f"{T3}.s04",
            "type": "check",
            "concept_ids": ["spreadsheet.sorting"],
            "eyebrow": "Quick Check",
            "title": "Multi-Level Sort with Independent Directions",
            "lede": "Choose the correct Sort dialog configuration for a two-level sort.",
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["spreadsheet.sorting"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "spreadsheet.sorting#f3",
                    "spreadsheet.sorting#f4"
                ],
                "anchors": ["spreadsheet.sorting#assessment:build_multi_level_sort_with_independent_directions"]
            }
        },

        # s05 — hands_on: sorting practice (framing only)
        {
            "step_id": f"{T3}.s05",
            "type": "hands_on",
            "concept_ids": ["spreadsheet.sorting"],
            "eyebrow": "Practice",
            "title": "Sort the Orders Sheet",
            "lede": "Sort the Orders sheet by order_date ascending, then by amount descending as a tiebreaker.",
            "reward": {"gems": 10},
            "lineage": {
                "concept_ids": ["spreadsheet.sorting"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "spreadsheet.sorting#f1",
                    "spreadsheet.sorting#f2"
                ],
                "anchors": [
                    "spreadsheet.sorting#practice",
                    "spreadsheet.sorting#assessment:sort_number_column_single_level",
                    "spreadsheet.sorting#assessment:sort_date_or_time_column_single_level"
                ]
            }
        },

        # s06 — explainer: filtering + visual (before_after)
        {
            "step_id": f"{T3}.s06",
            "type": "explainer",
            "concept_ids": ["spreadsheet.filtering"],
            "eyebrow": "Filtering",
            "title": "Showing Only the Rows You Need",
            "lede": "AutoFilter hides rows that don't match your criteria — the data is still there, just not visible. Clearing the filter brings it all back.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T3}.s06.p1",
                    "role": "intro",
                    "text": "Sometimes you don't want to reorder your Orders sheet, you want to see only some of it — for example, only the orders above a certain amount.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.filtering"],
                        "teaching_block_ids": ["spreadsheet.filtering#tb1"],
                        "fact_ids": []
                    }
                },
                {
                    "type": "prose",
                    "block_id": f"{T3}.s06.p2",
                    "role": "mechanism",
                    "text": "To filter a range of data, select any cell within the range, select Data > Filter, select the column header's filter arrow, choose Number Filters or Text Filters and a comparison such as Greater Than, enter the filter criteria, and select OK. AutoFilter shows the data you want and hides the rest; clearing a filter redisplays all of the data.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.filtering"],
                        "teaching_block_ids": ["spreadsheet.filtering#tb2"],
                        "fact_ids": [
                            "spreadsheet.filtering#f1",
                            "spreadsheet.filtering#f2"
                        ]
                    }
                },
                {
                    "type": "prose",
                    "block_id": f"{T3}.s06.p3",
                    "role": "example",
                    "text": "A range or table can be filtered by more than one column at once; filters are additive, so each additional filter is based on the current filter and further reduces the subset of data shown. Filtering your Orders sheet to amounts greater than 5000, then filtering the city column to Lagos, leaves only the Lagos orders above 5000 — both conditions apply together, not separately.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.filtering"],
                        "teaching_block_ids": ["spreadsheet.filtering#tb3"],
                        "fact_ids": ["spreadsheet.filtering#f3"]
                    }
                },
                {
                    "type": "before_after",
                    "block_id": f"{T3}.s06.ba1",
                    "before": {
                        "type": "spreadsheet_grid",
                        "asset_ref": {"asset_id": "asset_orders_clean", "variant_id": None, "columns": ["order_id", "city", "amount", "status"]},
                        "sheet_name": "Orders",
                        "range": "A1:D6",
                        "annotations": [
                            {"target": "A1", "text": "All 20 rows visible — no filter applied"}
                        ]
                    },
                    "after": {
                        "type": "spreadsheet_grid",
                        "asset_ref": {"asset_id": "asset_orders_clean", "variant_id": None, "columns": ["order_id", "city", "amount", "status"]},
                        "sheet_name": "Orders",
                        "range": "A1:D4",
                        "annotations": [
                            {"target": "C1", "text": "Filter icon changed — amount > 5000 filter active"},
                            {"target": "B1", "text": "Second filter on city = Lagos — rows further reduced"}
                        ]
                    },
                    "change_summary": "After filtering amount > 5000 and city = Lagos, only matching rows are visible; row numbers are non-consecutive showing hidden rows.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.filtering"],
                        "teaching_block_ids": [
                            "spreadsheet.filtering#tb1",
                            "spreadsheet.filtering#tb2",
                            "spreadsheet.filtering#tb3"
                        ],
                        "fact_ids": [
                            "spreadsheet.filtering#f1",
                            "spreadsheet.filtering#f2",
                            "spreadsheet.filtering#f3"
                        ],
                        "anchors": ["spreadsheet.filtering#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["spreadsheet.filtering"],
                "teaching_block_ids": [
                    "spreadsheet.filtering#tb1",
                    "spreadsheet.filtering#tb2",
                    "spreadsheet.filtering#tb3"
                ],
                "fact_ids": [
                    "spreadsheet.filtering#f1",
                    "spreadsheet.filtering#f2",
                    "spreadsheet.filtering#f3"
                ],
                "anchors": ["spreadsheet.filtering#visual"]
            }
        },

        # s07 — video: filtering
        {
            "step_id": f"{T3}.s07",
            "type": "video",
            "concept_ids": ["spreadsheet.filtering"],
            "eyebrow": "Filtering",
            "title": "AutoFilter: Hiding Rows, Stacking Filters, and Clearing",
            "blocks": [
                {
                    "type": "media_group",
                    "block_id": f"{T3}.s07.mg1",
                    "segment_ids": ["seg_spreadsheet.filtering_cB5koQvGwsA_77_287"]
                }
            ],
            "lineage": {
                "concept_ids": ["spreadsheet.filtering"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "spreadsheet.filtering#f1",
                    "spreadsheet.filtering#f2",
                    "spreadsheet.filtering#f3"
                ],
                "segment_ids": ["seg_spreadsheet.filtering_cB5koQvGwsA_77_287"]
            }
        },

        # s08 — check: AutoFilter criteria (framing only)
        {
            "step_id": f"{T3}.s08",
            "type": "check",
            "concept_ids": ["spreadsheet.filtering"],
            "eyebrow": "Quick Check",
            "title": "Applying AutoFilter Criteria",
            "lede": "Choose the correct steps to apply a Number Filter to a range.",
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["spreadsheet.filtering"],
                "teaching_block_ids": [],
                "fact_ids": ["spreadsheet.filtering#f1"],
                "anchors": ["spreadsheet.filtering#assessment:apply_autofilter_criteria_to_a_range"]
            }
        },

        # s09 — hands_on: filtering practice (framing only)
        {
            "step_id": f"{T3}.s09",
            "type": "hands_on",
            "concept_ids": ["spreadsheet.filtering"],
            "eyebrow": "Practice",
            "title": "Filter the Orders Sheet",
            "lede": "Apply a filter to show only Delivered orders from Lagos, then clear the filter to restore all rows.",
            "reward": {"gems": 10},
            "lineage": {
                "concept_ids": ["spreadsheet.filtering"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "spreadsheet.filtering#f2",
                    "spreadsheet.filtering#f3"
                ],
                "anchors": [
                    "spreadsheet.filtering#practice",
                    "spreadsheet.filtering#assessment:explain_hide_not_delete_and_clear_to_restore",
                    "spreadsheet.filtering#assessment:apply_additive_multi_column_filters"
                ]
            }
        },

        # s10 — recap
        {
            "step_id": f"{T3}.s10",
            "type": "recap",
            "concept_ids": ["spreadsheet.sorting", "spreadsheet.filtering"],
            "eyebrow": "Recap",
            "title": "Sorting and Filtering — Key Points",
            "lede": "You can now sort by one or more columns with independent directions, and filter to show only the rows that match your criteria.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T3}.s10.p1",
                    "role": "takeaway",
                    "text": "To sort numbers, use Sort Smallest to Largest or Largest to Smallest from the Data tab. To sort dates, use Sort Oldest to Newest or Newest to Oldest. For multi-level sorts, open Data > Sort, add levels with Add Level, and set each level's Order independently — higher levels are applied first. AutoFilter hides rows that don't match; clearing the filter redisplays all data. Filters are additive: each additional column filter further reduces the visible subset.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.sorting", "spreadsheet.filtering"],
                        "teaching_block_ids": [],
                        "fact_ids": []
                    }
                },
                {
                    "type": "up_next",
                    "block_id": f"{T3}.s10.up_next",
                    "title": "Next: Conditional Formatting and Data Validation",
                    "text": "In the next tile you'll highlight cells automatically based on their values and restrict what can be entered in a column using dropdown lists."
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["spreadsheet.sorting", "spreadsheet.filtering"],
                "teaching_block_ids": [],
                "fact_ids": []
            }
        }
    ],

    # ── Remediation steps ──────────────────────────────────────────────────
    "remediation_steps": [
        # r01: for s04 check (sorting#f3,f4 — multi-level sort)
        {
            "step_id": f"{T3}.r01",
            "type": "remediation",
            "concept_ids": ["spreadsheet.sorting"],
            "eyebrow": "Let's Revisit",
            "title": "Multi-Level Sort: Each Level Has Its Own Direction",
            "lede": "See the contrast between a single-level sort and a two-level sort with different directions.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T3}.r01.p1",
                    "role": "example",
                    "text": "Single-level sort: sort the Orders sheet by amount Largest to Smallest — all rows reorder by amount alone. Two-level sort: Level 1 is order_date Oldest to Newest; Level 2 is amount Largest to Smallest. The result: rows are grouped by date in ascending order, and within each date the rows are ordered by amount descending. The key point is that Level 2's direction (Largest to Smallest) is completely independent of Level 1's direction (Oldest to Newest) — you set each in its own Order dropdown.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.sorting"],
                        "teaching_block_ids": ["spreadsheet.sorting#tb3", "spreadsheet.sorting#tb4"],
                        "fact_ids": [
                            "spreadsheet.sorting#f3",
                            "spreadsheet.sorting#f4"
                        ]
                    }
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["spreadsheet.sorting"],
                "teaching_block_ids": ["spreadsheet.sorting#tb3", "spreadsheet.sorting#tb4"],
                "fact_ids": [
                    "spreadsheet.sorting#f3",
                    "spreadsheet.sorting#f4"
                ]
            }
        },
        # r02: for s08 check (filtering#f1 — AutoFilter steps)
        {
            "step_id": f"{T3}.r02",
            "type": "remediation",
            "concept_ids": ["spreadsheet.filtering"],
            "eyebrow": "Let's Revisit",
            "title": "AutoFilter: Hide vs. Delete",
            "lede": "Filtering hides rows — it never removes them. Clearing the filter brings them back.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": f"{T3}.r02.p1",
                    "role": "example",
                    "text": "After applying a Number Filter (Greater Than 5000) to the amount column of your Orders sheet, rows with amounts of 5000 or less disappear from view — but they are still in the sheet. The row numbers jump (e.g. 1, 3, 7 …) because the hidden rows are still there. Clicking Data > Filter again, or clicking Clear in the Sort & Filter group, removes the filter and all rows reappear. No data was deleted.",
                    "lineage": {
                        "concept_ids": ["spreadsheet.filtering"],
                        "teaching_block_ids": ["spreadsheet.filtering#tb2"],
                        "fact_ids": ["spreadsheet.filtering#f1"]
                    }
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["spreadsheet.filtering"],
                "teaching_block_ids": ["spreadsheet.filtering#tb2"],
                "fact_ids": ["spreadsheet.filtering#f1"]
            }
        }
    ]
}

out["tiles"].append(tile3)

# Write output
output_path = "batches/final_batch_011_da_spreadsheet/screens.part.c2.json"
with open(output_path, "w") as f:
    json.dump(out, f, indent=2)

print(f"Written: {output_path}")
print(f"Tiles: {len(out['tiles'])}")
for t in out['tiles']:
    steps = t['steps']
    rem = t.get('remediation_steps', [])
    print(f"  {t['tile_id']}: {len(steps)} steps, {len(rem)} remediation steps")
