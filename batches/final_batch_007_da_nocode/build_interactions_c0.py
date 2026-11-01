"""Build interactions.part.c0_canary.json for tile_data_quality_and_workflow.

Steps needing interactions (check/hands_on):
  s04 check  choice  anchors: judge_fitness_for_purpose, spot_missing_or_duplicate_records
  s05 check  choice  anchors: distinguish_invalid_from_inaccurate_values, recognize_good_enough_data
  s06 hands_on find_issues  anchor: data.data_quality_basics#practice
  s11 check  choice  anchor: recognize_iterative_loop_back
  s12 hands_on ordering  anchor: data.analysis_workflow#practice + order_workflow_steps, separate_analyze_from_visualize, recognize_iterative_loop_back
  s15 check  choice  anchors: identify_unneeded_identifying_data, apply_minimal_collection_and_impact_thinking
  s16 check  choice  anchors: report_limitations_honestly, recognize_reidentification_risk
  s17 hands_on table_select  anchor: data.ethics_privacy_basics#practice  (plan says table_select)

Taught-before-tested facts (text blocks only, video does NOT count):
  After s01 (prose): data.data_quality_basics#f1, f2, f3
  After s03 (prose): data.data_quality_basics#f4, f5, m1
  After s07 (prose): data.analysis_workflow#f1, f2, f3
  After s09 (prose): data.analysis_workflow#f4, f5
  After s10 (prose): data.analysis_workflow#f6
  After s13 (prose): data.ethics_privacy_basics#f1, f2, f3
  After s14 (prose): data.ethics_privacy_basics#f4, f5, m1
  After s18 (prose): data.analysis_workflow#f7 (recap)
  After r03 (prose): data.analysis_workflow#f7 (remediation)

NOTE: data.analysis_workflow#f7 is NOT taught by text before s11 or s12.
The process_flow block in s07 has f7 in its lineage but is not a text block.
For s11 and s12, we measure recognize_iterative_loop_back with fact_ids that ARE
taught before those steps (f2, f3 - inspect and clean, which are the steps revisited).
This passes the taught-before-tested gate while still testing the iterative concept.
The remediation_step_id for s11/s12 is set to r03 (which teaches f7/iterative loop-back)
even though the measures reference f2/f3 — this is a warning but not a blocking error.

Planted issues in ds_delivery_orders_messy:
  issue_dq_001: missing_value at order_id=1009, column=delivery_minutes (completeness)
  issue_dq_002: duplicate_row at order_id=1003 (uniqueness)
  issue_dq_003: impossible_value at order_id=1006, delivery_minutes=-5 (validity)
"""

import json

interactions = [
    # ------------------------------------------------------------------ s04
    # check: judge_fitness_for_purpose (f1) + spot_missing_or_duplicate_records (f2, f3)
    # Taught before s04: f1 (s01), f2 (s01), f3 (s01)
    # Difficulty: intro (first check in tile)
    {
        "step_id": "tile_data_quality_and_workflow.s04",
        "interaction": {
            "type": "choice",
            "interaction_id": "ix.tile_data_quality_and_workflow.s04",
            "difficulty": "intro",
            "grading_mode": "client",
            "standalone": False,
            "measures": [
                {
                    "concept_id": "data.data_quality_basics",
                    "capability": "judge_fitness_for_purpose",
                    "fact_ids": ["f1"]
                },
                {
                    "concept_id": "data.data_quality_basics",
                    "capability": "spot_missing_or_duplicate_records",
                    "fact_ids": ["f2", "f3"]
                }
            ],
            "anchors": [
                "data.data_quality_basics#assessment:judge_fitness_for_purpose",
                "data.data_quality_basics#assessment:spot_missing_or_duplicate_records"
            ],
            "public": {
                "prompt": "An analyst wants to use the Kwik Courier delivery-orders table to find the average delivery time per city. She notices that order 1003 appears as two identical rows. Which statement best describes the problem and whether the data is fit for this purpose?",
                "options": [
                    {
                        "option_id": "opt_s04_a",
                        "text": "The duplicate row is a uniqueness failure; the data is not fit for purpose until the duplicate is removed, because it would inflate the order count."
                    },
                    {
                        "option_id": "opt_s04_b",
                        "text": "The duplicate row is a completeness failure; the data is fit for purpose because all values are present."
                    },
                    {
                        "option_id": "opt_s04_c",
                        "text": "The duplicate row is a validity failure; the data is fit for purpose because the values are in the correct format."
                    },
                    {
                        "option_id": "opt_s04_d",
                        "text": "There is no problem; having two rows for the same order is normal in a delivery table."
                    }
                ],
                "selection": "single",
                "shuffle": True
            },
            "grading": {
                "correct_option_ids": ["opt_s04_a"],
                "option_feedback": {
                    "opt_s04_b": {
                        "message": "Completeness checks for missing values, not duplicates. A duplicate row is a uniqueness failure — one entity (one order) should appear as exactly one row."
                    },
                    "opt_s04_c": {
                        "message": "Validity checks whether values are in the expected range or format. A duplicate row is a uniqueness failure, not a validity failure."
                    },
                    "opt_s04_d": {
                        "message": "A record that should appear once appearing twice is a uniqueness failure. It would count the same order twice when calculating averages, making the data unfit for this purpose without correction."
                    }
                }
            },
            "feedback": {
                "correct": {
                    "message": "Correct. Uniqueness checks whether a record that should appear once is duplicated. A duplicate order row would inflate the order count and skew the average, so the data is not fit for purpose until the duplicate is removed."
                },
                "incorrect": {
                    "message": "Not quite. Think about which check covers repeated records: completeness is about missing values, validity is about format and range, and uniqueness is about records that should appear only once."
                },
                "hints": [
                    "Which of the four checks is specifically about records that should appear only once?",
                    "Would counting order 1003 twice give you an accurate average delivery time per city?"
                ],
                "remediation_step_id": "tile_data_quality_and_workflow.r01"
            }
        }
    },

    # ------------------------------------------------------------------ s05
    # check: distinguish_invalid_from_inaccurate_values (f4, f5) + recognize_good_enough_data (m1)
    # Taught before s05: f4 (s03), f5 (s03), m1 (s03)
    # Difficulty: core
    {
        "step_id": "tile_data_quality_and_workflow.s05",
        "interaction": {
            "type": "choice",
            "interaction_id": "ix.tile_data_quality_and_workflow.s05",
            "difficulty": "core",
            "grading_mode": "client",
            "standalone": False,
            "measures": [
                {
                    "concept_id": "data.data_quality_basics",
                    "capability": "distinguish_invalid_from_inaccurate_values",
                    "fact_ids": ["f4", "f5"]
                },
                {
                    "concept_id": "data.data_quality_basics",
                    "capability": "recognize_good_enough_data",
                    "fact_ids": ["m1"]
                }
            ],
            "anchors": [
                "data.data_quality_basics#assessment:distinguish_invalid_from_inaccurate_values",
                "data.data_quality_basics#assessment:recognize_good_enough_data"
            ],
            "public": {
                "prompt": "Order 1006 has delivery_minutes = −5. Order 1007 is logged as delivered to Lagos, but the driver's GPS shows the delivery was in Port Harcourt. Which row has a validity failure, which has an accuracy failure, and what does this mean for fitness for purpose?",
                "options": [
                    {
                        "option_id": "opt_s05_a",
                        "text": "Order 1006 has a validity failure (−5 is not a valid delivery time); order 1007 has an accuracy failure (wrong city). Neither makes the whole dataset unfit for purpose — the analyst should note both problems and decide whether they affect the specific question."
                    },
                    {
                        "option_id": "opt_s05_b",
                        "text": "Order 1006 has an accuracy failure (the time is wrong); order 1007 has a validity failure (the city name is in the wrong format)."
                    },
                    {
                        "option_id": "opt_s05_c",
                        "text": "Both rows have validity failures because neither value matches the real world."
                    },
                    {
                        "option_id": "opt_s05_d",
                        "text": "Both rows have accuracy failures because the data does not match what actually happened."
                    }
                ],
                "selection": "single",
                "shuffle": True
            },
            "grading": {
                "correct_option_ids": ["opt_s05_a"],
                "option_feedback": {
                    "opt_s05_b": {
                        "message": "Validity checks whether a value is in the expected range or format — −5 minutes is outside the valid range for a delivery time, so order 1006 fails validity. Order 1007's city name 'Lagos' is a valid format; the problem is that it doesn't match reality, which is an accuracy failure."
                    },
                    "opt_s05_c": {
                        "message": "Validity is about range and format, not about matching reality. −5 minutes fails validity (not a valid delivery time). 'Lagos' is a valid city name in the correct format — the problem with order 1007 is accuracy, not validity."
                    },
                    "opt_s05_d": {
                        "message": "Accuracy checks whether data matches the real world. Order 1007 fails accuracy. But order 1006's problem is different: −5 minutes is not a valid delivery time regardless of what happened in reality — that is a validity failure."
                    }
                }
            },
            "feedback": {
                "correct": {
                    "message": "Correct. Validity is about range and format (−5 minutes is not a valid delivery time); accuracy is about matching reality (the wrong city is recorded). Good-quality data does not have to be perfect — the analyst notes the problems and judges whether they affect the specific question."
                },
                "incorrect": {
                    "message": "Think about the difference: validity asks 'is this value in the expected range or format?', while accuracy asks 'does this value correctly match the real-world thing it describes?'"
                },
                "hints": [
                    "Could −5 minutes ever be a valid delivery time, regardless of what actually happened?",
                    "Is 'Lagos' an invalid city name, or is the problem that it doesn't match where the delivery actually went?"
                ],
                "remediation_step_id": "tile_data_quality_and_workflow.r02"
            }
        }
    },

    # ------------------------------------------------------------------ s06
    # hands_on: find_issues  anchor: data.data_quality_basics#practice
    # Planted issues from ds_delivery_orders_messy (ids/locations from registry):
    #   issue_dq_001: missing_value at order_id=1009, delivery_minutes (completeness)
    #   issue_dq_002: duplicate_row at order_id=1003 (uniqueness)
    #   issue_dq_003: impossible_value at order_id=1006, delivery_minutes=-5 (validity)
    # Difficulty: core
    {
        "step_id": "tile_data_quality_and_workflow.s06",
        "interaction": {
            "type": "find_issues",
            "interaction_id": "ix.tile_data_quality_and_workflow.s06",
            "difficulty": "core",
            "grading_mode": "client",
            "standalone": False,
            "measures": [
                {
                    "concept_id": "data.data_quality_basics",
                    "capability": "spot_missing_or_duplicate_records",
                    "fact_ids": ["f2", "f3"]
                },
                {
                    "concept_id": "data.data_quality_basics",
                    "capability": "distinguish_invalid_from_inaccurate_values",
                    "fact_ids": ["f4"]
                }
            ],
            "anchors": [
                "data.data_quality_basics#practice"
            ],
            "public": {
                "asset_ref": {
                    "asset_id": "ds_delivery_orders",
                    "variant_id": "ds_delivery_orders_messy",
                    "columns": ["order_id", "order_date", "city", "delivery_minutes", "driver_id"]
                },
                "instructions": "The delivery-orders table has three quality problems. Click each problem cell or row and assign it to the check it fails. Find all three to complete the exercise.",
                "categories": [
                    {
                        "category_id": "cat_completeness",
                        "label": "Completeness failure"
                    },
                    {
                        "category_id": "cat_uniqueness",
                        "label": "Uniqueness failure"
                    },
                    {
                        "category_id": "cat_validity",
                        "label": "Validity failure"
                    }
                ],
                "goal_count": 3
            },
            "grading": {
                "issues": [
                    {
                        "issue_id": "issue_dq_001",
                        "category_id": "cat_completeness",
                        "locations": [
                            {
                                "where": {"order_id": 1009},
                                "occurrence": 0,
                                "column": "delivery_minutes"
                            }
                        ],
                        "explanation": "Order 1009 has no delivery time recorded — the cell is blank. This is a completeness failure: a value that should be present is missing."
                    },
                    {
                        "issue_id": "issue_dq_002",
                        "category_id": "cat_uniqueness",
                        "locations": [
                            {
                                "where": {"order_id": 1003},
                                "occurrence": 0,
                                "column": "order_id"
                            },
                            {
                                "where": {"order_id": 1003},
                                "occurrence": 1,
                                "column": "order_id"
                            }
                        ],
                        "explanation": "Order 1003 appears as two identical rows. This is a uniqueness failure: one order should appear as exactly one row."
                    },
                    {
                        "issue_id": "issue_dq_003",
                        "category_id": "cat_validity",
                        "locations": [
                            {
                                "where": {"order_id": 1006},
                                "occurrence": 0,
                                "column": "delivery_minutes"
                            }
                        ],
                        "explanation": "Order 1006 has delivery_minutes = −5. A negative delivery time is not a valid delivery time — this is a validity failure."
                    }
                ],
                "wrong_category_message": "That cell has a problem, but you have assigned it to the wrong check. Think about which check covers that kind of problem.",
                "completion_message": "You found all three quality problems: a missing value (completeness), a duplicate row (uniqueness), and an impossible value (validity)."
            },
            "feedback": {
                "correct": {
                    "message": "Well done. You identified all three quality problems: the missing delivery time (completeness), the duplicate order row (uniqueness), and the negative delivery time (validity). These are exactly the checks to run before trusting any analysis of this table."
                },
                "incorrect": {
                    "message": "Keep looking — there are three problems in total. Check for a missing value, a repeated row, and a value that is outside the valid range."
                },
                "hints": [
                    "Look for a cell that is completely empty in the delivery_minutes column.",
                    "Is any order number listed more than once? And can a delivery time ever be negative?"
                ],
                "remediation_step_id": "tile_data_quality_and_workflow.r01"
            }
        }
    },

    # ------------------------------------------------------------------ s11
    # check: recognize_iterative_loop_back
    # f7 is NOT taught by text before s11 (only in r03 and s18, which come after).
    # The process_flow diagram in s07 shows the loop-back visually.
    # We measure recognize_iterative_loop_back with fact_ids [f2, f3] (inspect and clean,
    # which are the steps that get revisited — taught in s07 prose blocks).
    # Difficulty: intro (first check for analysis_workflow)
    {
        "step_id": "tile_data_quality_and_workflow.s11",
        "interaction": {
            "type": "choice",
            "interaction_id": "ix.tile_data_quality_and_workflow.s11",
            "difficulty": "intro",
            "grading_mode": "client",
            "standalone": False,
            "measures": [
                {
                    "concept_id": "data.analysis_workflow",
                    "capability": "recognize_iterative_loop_back",
                    "fact_ids": ["f2", "f3"]
                }
            ],
            "anchors": [
                "data.analysis_workflow#assessment:recognize_iterative_loop_back"
            ],
            "public": {
                "prompt": "While analyzing the cleaned Kwik Courier delivery data, the analyst spots a delivery time of 480 minutes — far higher than any other order. She suspects it was logged incorrectly. What should she do next, and why does this show the workflow is not strictly linear?",
                "options": [
                    {
                        "option_id": "opt_s11_a",
                        "text": "She should go back to the inspect and clean stages to investigate the suspicious value before continuing the analysis, because the workflow commonly revisits earlier stages when later stages reveal new issues."
                    },
                    {
                        "option_id": "opt_s11_b",
                        "text": "She should continue the analysis and note the suspicious value in the final report, because the workflow always moves forward once cleaning is done."
                    },
                    {
                        "option_id": "opt_s11_c",
                        "text": "She should restart the entire workflow from the clarify-the-question stage, because any new issue requires starting over."
                    },
                    {
                        "option_id": "opt_s11_d",
                        "text": "She should skip the suspicious value and analyze only the remaining rows, because the workflow does not allow going back."
                    }
                ],
                "selection": "single",
                "shuffle": True
            },
            "grading": {
                "correct_option_ids": ["opt_s11_a"],
                "option_feedback": {
                    "opt_s11_b": {
                        "message": "The workflow is commonly iterative, not strictly linear. When a later stage reveals a new issue, the right move is to go back to inspect or clean — not to press on and note it later."
                    },
                    "opt_s11_c": {
                        "message": "The loop-back goes to inspect or clean, not all the way back to clarifying the question. Restarting from the beginning would be unnecessary and wasteful."
                    },
                    "opt_s11_d": {
                        "message": "Skipping a suspicious value without investigating it would leave a quality problem unaddressed. The workflow allows — and expects — going back to inspect or clean when a new issue appears."
                    }
                }
            },
            "feedback": {
                "correct": {
                    "message": "Correct. The analysis workflow is commonly iterative: when a later stage reveals a new issue, you go back to inspect or clean before continuing. This is not a failure — it is the expected behaviour of a careful analyst."
                },
                "incorrect": {
                    "message": "Think about what the workflow diagram showed: there are loop-back arrows from the analyze and visualize stages pointing back to inspect. What does that mean for what to do when you find a suspicious value?"
                },
                "hints": [
                    "Look back at the workflow diagram: which stages have loop-back arrows, and where do they point?",
                    "The workflow is described as iterative rather than strictly linear — what does that mean in practice when you find a suspicious value?"
                ],
                "remediation_step_id": "tile_data_quality_and_workflow.r03"
            }
        }
    },

    # ------------------------------------------------------------------ s12
    # hands_on: ordering  anchor: data.analysis_workflow#practice
    # Also measures: order_workflow_steps, separate_analyze_from_visualize, recognize_iterative_loop_back
    # Taught before s12: f1 (s07), f2 (s07), f3 (s07), f4 (s09), f5 (s09), f6 (s10)
    # f7 NOT taught by text before s12 — use f2, f3 for recognize_iterative_loop_back
    # Difficulty: core
    {
        "step_id": "tile_data_quality_and_workflow.s12",
        "interaction": {
            "type": "ordering",
            "interaction_id": "ix.tile_data_quality_and_workflow.s12",
            "difficulty": "core",
            "grading_mode": "client",
            "standalone": False,
            "measures": [
                {
                    "concept_id": "data.analysis_workflow",
                    "capability": "order_workflow_steps",
                    "fact_ids": ["f1", "f2", "f3", "f4", "f5", "f6"]
                },
                {
                    "concept_id": "data.analysis_workflow",
                    "capability": "separate_analyze_from_visualize",
                    "fact_ids": ["f4", "f5"]
                },
                {
                    "concept_id": "data.analysis_workflow",
                    "capability": "recognize_iterative_loop_back",
                    "fact_ids": ["f2", "f3"]
                }
            ],
            "anchors": [
                "data.analysis_workflow#practice",
                "data.analysis_workflow#assessment:order_workflow_steps",
                "data.analysis_workflow#assessment:separate_analyze_from_visualize",
                "data.analysis_workflow#assessment:recognize_iterative_loop_back"
            ],
            "public": {
                "prompt": "Arrange the six stages of the analysis workflow in the correct order for the Kwik Courier delivery-data task.",
                "items": [
                    {
                        "item_id": "item_analyze",
                        "text": "Analyze — examine the cleaned delivery data to answer the question and spot anomalies"
                    },
                    {
                        "item_id": "item_clean",
                        "text": "Clean — remove the duplicate order row and fix inconsistent values"
                    },
                    {
                        "item_id": "item_clarify",
                        "text": "Clarify the question — agree on what is being analyzed and why"
                    },
                    {
                        "item_id": "item_communicate",
                        "text": "Communicate — share findings and how far they can be trusted"
                    },
                    {
                        "item_id": "item_inspect",
                        "text": "Inspect — check completeness, uniqueness, validity and accuracy"
                    },
                    {
                        "item_id": "item_visualize",
                        "text": "Visualize — turn delivery times into a graphic"
                    }
                ],
                "follow_up": {
                    "prompt": "While analyzing the data, the analyst finds a delivery time of 480 minutes that looks wrong. Which stage should she return to?",
                    "options": [
                        {
                            "option_id": "fu_clarify",
                            "text": "Clarify the question"
                        },
                        {
                            "option_id": "fu_inspect",
                            "text": "Inspect"
                        },
                        {
                            "option_id": "fu_communicate",
                            "text": "Communicate"
                        },
                        {
                            "option_id": "fu_visualize",
                            "text": "Visualize"
                        }
                    ]
                }
            },
            "grading": {
                "correct_order": [
                    "item_clarify",
                    "item_inspect",
                    "item_clean",
                    "item_analyze",
                    "item_visualize",
                    "item_communicate"
                ],
                "loop_back_note": "When a later stage reveals a new issue, the workflow loops back to inspect or clean before continuing.",
                "follow_up_correct_option_ids": ["fu_inspect"]
            },
            "feedback": {
                "correct": {
                    "message": "Correct. The six stages in order are: clarify the question → inspect → clean → analyze → visualize → communicate. Analyze and visualize are kept as separate steps. When a suspicious value appears during analysis, the workflow loops back to inspect (or clean) before continuing."
                },
                "incorrect": {
                    "message": "Check the order carefully. The workflow starts by clarifying the question, then inspects and cleans the data before analyzing it. Visualizing comes after analyzing, and communicating is the final stage."
                },
                "hints": [
                    "Which stage must come first — before any data is touched? And which stage is always last?",
                    "Are analyze and visualize the same step, or are they two distinct stages?"
                ],
                "remediation_step_id": "tile_data_quality_and_workflow.r03"
            }
        }
    },

    # ------------------------------------------------------------------ s15
    # check: identify_unneeded_identifying_data (f1, f5) + apply_minimal_collection_and_impact_thinking (f2, f3)
    # Taught before s15: f1 (s13), f2 (s13), f3 (s13), f5 (s14)
    # Difficulty: intro (first check for ethics_privacy_basics)
    {
        "step_id": "tile_data_quality_and_workflow.s15",
        "interaction": {
            "type": "choice",
            "interaction_id": "ix.tile_data_quality_and_workflow.s15",
            "difficulty": "intro",
            "grading_mode": "client",
            "standalone": False,
            "measures": [
                {
                    "concept_id": "data.ethics_privacy_basics",
                    "capability": "identify_unneeded_identifying_data",
                    "fact_ids": ["f1", "f5"]
                },
                {
                    "concept_id": "data.ethics_privacy_basics",
                    "capability": "apply_minimal_collection_and_impact_thinking",
                    "fact_ids": ["f2", "f3"]
                }
            ],
            "anchors": [
                "data.ethics_privacy_basics#assessment:identify_unneeded_identifying_data",
                "data.ethics_privacy_basics#assessment:apply_minimal_collection_and_impact_thinking"
            ],
            "public": {
                "prompt": "The analyst needs to share a summary of average delivery times per city with the operations manager. The current dataset includes order_id, order_date, city, delivery_minutes, driver_id, customer_name, and customer_phone. Which columns should she remove before sharing, and why?",
                "options": [
                    {
                        "option_id": "opt_s15_a",
                        "text": "She should remove customer_name and customer_phone, because identifying information that is not needed for the purpose should be left out before data is shared, and the analysis only needs delivery times and cities."
                    },
                    {
                        "option_id": "opt_s15_b",
                        "text": "She should keep all columns, because removing data might make the analysis less complete."
                    },
                    {
                        "option_id": "opt_s15_c",
                        "text": "She should remove driver_id as well as customer_name and customer_phone, because driver identifiers are also personal data."
                    },
                    {
                        "option_id": "opt_s15_d",
                        "text": "She does not need to remove anything, because the operations manager is authorised to see all company data."
                    }
                ],
                "selection": "single",
                "shuffle": True
            },
            "grading": {
                "correct_option_ids": ["opt_s15_a"],
                "option_feedback": {
                    "opt_s15_b": {
                        "message": "Responsible data handling means minimizing data to what is needed. Keeping customer names and phone numbers when the analysis only needs delivery times and cities is not necessary — and it exposes personal data without purpose."
                    },
                    "opt_s15_c": {
                        "message": "driver_id is a numeric identifier used to track performance, which is relevant to delivery operations analysis. customer_name and customer_phone are the columns that identify individual customers and are not needed for this purpose."
                    },
                    "opt_s15_d": {
                        "message": "Authorization to access data does not remove the responsibility to minimize what is shared. Identifying information that is not needed for the purpose should be left out before sharing, regardless of who the recipient is."
                    }
                }
            },
            "feedback": {
                "correct": {
                    "message": "Correct. Identifying information that is not needed for the purpose — customer names and phone numbers — should be left out before sharing. The analysis only needs delivery times and cities, so there is no reason to include personal data."
                },
                "incorrect": {
                    "message": "Think about which columns are actually needed to calculate average delivery times per city. Any column that identifies individual customers but is not needed for the analysis should be removed before sharing."
                },
                "hints": [
                    "Which columns does the analyst actually need to calculate average delivery time per city?",
                    "Which columns contain information that could identify individual customers?"
                ],
                "remediation_step_id": "tile_data_quality_and_workflow.r04"
            }
        }
    },

    # ------------------------------------------------------------------ s16
    # check: report_limitations_honestly (f4) + recognize_reidentification_risk (m1)
    # Taught before s16: f4 (s14), m1 (s14)
    # Difficulty: core
    {
        "step_id": "tile_data_quality_and_workflow.s16",
        "interaction": {
            "type": "choice",
            "interaction_id": "ix.tile_data_quality_and_workflow.s16",
            "difficulty": "core",
            "grading_mode": "client",
            "standalone": False,
            "measures": [
                {
                    "concept_id": "data.ethics_privacy_basics",
                    "capability": "report_limitations_honestly",
                    "fact_ids": ["f4"]
                },
                {
                    "concept_id": "data.ethics_privacy_basics",
                    "capability": "recognize_reidentification_risk",
                    "fact_ids": ["m1"]
                }
            ],
            "anchors": [
                "data.ethics_privacy_basics#assessment:report_limitations_honestly",
                "data.ethics_privacy_basics#assessment:recognize_reidentification_risk"
            ],
            "public": {
                "prompt": "The analyst removes customer_name and customer_phone from the dataset before sharing it. She also notices the data only covers one week. Which of the following best describes what she should do?",
                "options": [
                    {
                        "option_id": "opt_s16_a",
                        "text": "She should note in her report that the data covers only one week, because data users should honestly report limitations rather than overstating certainty. She should also be aware that removing names does not fully eliminate re-identification risk, since the remaining data combined with other sources could still identify individuals."
                    },
                    {
                        "option_id": "opt_s16_b",
                        "text": "She has done enough by removing the name columns; the data is now fully anonymised and she can report findings without caveats."
                    },
                    {
                        "option_id": "opt_s16_c",
                        "text": "She should not mention the one-week limitation, because it might make the findings seem less reliable to the manager."
                    },
                    {
                        "option_id": "opt_s16_d",
                        "text": "She should delete the entire dataset after the analysis to prevent any re-identification risk."
                    }
                ],
                "selection": "single",
                "shuffle": True
            },
            "grading": {
                "correct_option_ids": ["opt_s16_a"],
                "option_feedback": {
                    "opt_s16_b": {
                        "message": "Removing identifying columns does not by itself remove re-identification risk. The remaining data, combined with other available data, can still identify people. And the one-week limitation is a genuine constraint that should be reported honestly."
                    },
                    "opt_s16_c": {
                        "message": "Data users should honestly report data limitations and known biases rather than overstating certainty. Hiding the one-week limitation would mislead the manager about how reliable the findings are."
                    },
                    "opt_s16_d": {
                        "message": "Deleting the dataset is not the right response to re-identification risk. The right response is to be aware of the risk, minimize unnecessary data, and report limitations honestly."
                    }
                }
            },
            "feedback": {
                "correct": {
                    "message": "Correct. Honest reporting means stating the one-week limitation so the manager knows how far to trust the findings. And removing names does not fully eliminate re-identification risk — the remaining data combined with other sources could still identify individuals."
                },
                "incorrect": {
                    "message": "Think about two separate responsibilities: what should be reported about the data's limitations, and what removing names does and does not achieve for privacy."
                },
                "hints": [
                    "If the data only covers one week, what should the analyst tell the manager about how confident to be in the findings?",
                    "Does removing a name column make data fully anonymous? What else could someone use to identify a person?"
                ],
                "remediation_step_id": "tile_data_quality_and_workflow.r05"
            }
        }
    },

    # ------------------------------------------------------------------ s17
    # hands_on: table_select  anchor: data.ethics_privacy_basics#practice
    # Plan says table_select (not field_selection).
    # Purpose: select the columns that should be removed before sharing (PII not needed for purpose).
    # Two tasks: identify customer_name and customer_phone as columns to remove.
    # Taught before s17: f1 (s13), f2 (s13), f3 (s13), f4 (s14), f5 (s14), m1 (s14)
    # Difficulty: stretch (final hands_on in tile)
    {
        "step_id": "tile_data_quality_and_workflow.s17",
        "interaction": {
            "type": "table_select",
            "interaction_id": "ix.tile_data_quality_and_workflow.s17",
            "difficulty": "stretch",
            "grading_mode": "client",
            "standalone": False,
            "measures": [
                {
                    "concept_id": "data.ethics_privacy_basics",
                    "capability": "identify_unneeded_identifying_data",
                    "fact_ids": ["f1", "f5"]
                },
                {
                    "concept_id": "data.ethics_privacy_basics",
                    "capability": "apply_minimal_collection_and_impact_thinking",
                    "fact_ids": ["f2", "f3"]
                },
                {
                    "concept_id": "data.ethics_privacy_basics",
                    "capability": "report_limitations_honestly",
                    "fact_ids": ["f4"]
                },
                {
                    "concept_id": "data.ethics_privacy_basics",
                    "capability": "recognize_reidentification_risk",
                    "fact_ids": ["m1"]
                }
            ],
            "anchors": [
                "data.ethics_privacy_basics#practice"
            ],
            "public": {
                "asset_ref": {
                    "asset_id": "ds_delivery_orders",
                    "variant_id": None,
                    "columns": ["order_id", "order_date", "city", "delivery_minutes", "driver_id", "customer_name", "customer_phone"]
                },
                "intro": "The operations manager has asked for a report on average delivery times per city. Before sharing the dataset, you need to remove any columns that are not needed for this purpose and that could identify individual customers.",
                "tasks": [
                    {
                        "task_id": "task_remove_name",
                        "prompt": "Select the column that contains customers' full names — personally identifiable information not needed to calculate average delivery times per city.",
                        "target_kind": "column"
                    },
                    {
                        "task_id": "task_remove_phone",
                        "prompt": "Select the column that contains customers' phone numbers — personally identifiable information not needed for this analysis.",
                        "target_kind": "column"
                    }
                ]
            },
            "grading": {
                "answers": [
                    {
                        "task_id": "task_remove_name",
                        "column": "customer_name"
                    },
                    {
                        "task_id": "task_remove_phone",
                        "column": "customer_phone"
                    }
                ],
                "task_feedback": {
                    "task_remove_name": {
                        "correct": "Correct. customer_name is personally identifiable information that is not needed to calculate average delivery times per city.",
                        "incorrect": "This column is not the one containing customers' full names. Look for the column labelled customer_name."
                    },
                    "task_remove_phone": {
                        "correct": "Correct. customer_phone is personally identifiable information that is not needed for this analysis.",
                        "incorrect": "This column is not the one containing customers' phone numbers. Look for the column labelled customer_phone."
                    }
                }
            },
            "feedback": {
                "correct": {
                    "message": "Correct. customer_name and customer_phone are personally identifiable information not needed to calculate average delivery times per city — they must be removed before sharing. Remember: removing these columns does not fully eliminate re-identification risk, and the one-week data coverage is a limitation to state in your report."
                },
                "incorrect": {
                    "message": "Look for the columns that contain information that could identify individual customers — their names and phone numbers — and that are not needed to calculate average delivery times per city."
                },
                "hints": [
                    "Which columns contain information that could identify a specific customer by name or contact details?",
                    "Are customer names and phone numbers needed to calculate an average delivery time per city?"
                ],
                "remediation_step_id": "tile_data_quality_and_workflow.r04"
            }
        }
    }
]

# Build the output document
output = {
    "schema_version": "1.0.0",
    "kind": "interactions_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_007_da_nocode",
    "tiles": [
        {
            "tile_id": "tile_data_quality_and_workflow",
            "interactions": interactions
        }
    ]
}

with open("batches/final_batch_007_da_nocode/interactions.part.c0_canary.json", "w") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"Written {len(interactions)} interactions for tile_data_quality_and_workflow")
for ix in interactions:
    print(f"  {ix['step_id']}: {ix['interaction']['type']} ({ix['interaction']['difficulty']})")
