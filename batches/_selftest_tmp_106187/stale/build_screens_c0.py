"""Build screens.part.c0_canary.json for tile_python_variables_types."""
import json

def wc(s):
    return len(s.split())

tile = {
    "tile_id": "tile_python_variables_types",
    "title": "Variables and Core Data Types",
    "summary": "Learn to store values in variables using Python's assignment operator, understand naming rules, and recognise the four core scalar types: int, float, str and bool.",
    "steps": [
        # ── s01: explainer – variables_assignment tb1+tb2+tb3, before_after visual ──
        {
            "step_id": "tile_python_variables_types.s01",
            "type": "explainer",
            "concept_ids": ["python.variables_assignment"],
            "eyebrow": "Variables and assignment",
            "title": "Storing a value under a name",
            "lede": "Before you can work with a delivery time in code, you need to give it a name you can refer back to.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_python_variables_types.s01.b01",
                    "role": "intro",
                    "text": "Suppose you are processing a delivery order and need to keep track of how long it took. In Python, the equal sign (=) is used to assign a value to a variable, so writing delivery_minutes = 32 stores the number 32 under the name delivery_minutes. From that point on, any line that mentions delivery_minutes reads back the stored value.",
                    "lineage": {
                        "concept_ids": ["python.variables_assignment"],
                        "fact_ids": ["python.variables_assignment#f1"],
                        "teaching_block_ids": ["python.variables_assignment#tb1"],
                        "anchors": []
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_python_variables_types.s01.b02",
                    "role": "misconception",
                    "text": "A name only exists once something has been assigned to it. Referring to average_delivery_minutes before any earlier line has set it raises a NameError — Python does not invent a default value for you.",
                    "lineage": {
                        "concept_ids": ["python.variables_assignment"],
                        "fact_ids": ["python.variables_assignment#f2"],
                        "teaching_block_ids": ["python.variables_assignment#tb2"],
                        "anchors": []
                    }
                },
                {
                    "type": "before_after",
                    "block_id": "tile_python_variables_types.s01.b03",
                    "before": {
                        "type": "code_walkthrough",
                        "block_id": "tile_python_variables_types.s01.b03.before",
                        "language": "python",
                        "code": "delivery_minutes = 32",
                        "annotations": [
                            {
                                "start_line": 1,
                                "end_line": 1,
                                "text": "delivery_minutes now holds 32"
                            }
                        ],
                        "reveal": "all"
                    },
                    "after": {
                        "type": "code_walkthrough",
                        "block_id": "tile_python_variables_types.s01.b03.after",
                        "language": "python",
                        "code": "delivery_minutes = 32\ndelivery_minutes = 45",
                        "annotations": [
                            {
                                "start_line": 2,
                                "end_line": 2,
                                "text": "The name is rebound to 45; 32 is gone"
                            }
                        ],
                        "reveal": "all"
                    },
                    "change_summary": "Assigning to delivery_minutes a second time replaces 32 with 45 — the name now refers to the new value.",
                    "lineage": {
                        "concept_ids": ["python.variables_assignment"],
                        "fact_ids": ["python.variables_assignment#f3"],
                        "teaching_block_ids": ["python.variables_assignment#tb3"],
                        "anchors": ["python.variables_assignment#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["python.variables_assignment"],
                "fact_ids": [
                    "python.variables_assignment#f1",
                    "python.variables_assignment#f2",
                    "python.variables_assignment#f3"
                ],
                "teaching_block_ids": [
                    "python.variables_assignment#tb1",
                    "python.variables_assignment#tb2",
                    "python.variables_assignment#tb3"
                ],
                "anchors": ["python.variables_assignment#visual"]
            }
        },

        # ── s02: explainer – variables_assignment tb4+tb5 ──
        {
            "step_id": "tile_python_variables_types.s02",
            "type": "explainer",
            "concept_ids": ["python.variables_assignment"],
            "eyebrow": "Variables and assignment",
            "title": "Naming rules and using stored values",
            "lede": "Not every word is a valid variable name, and once a name holds a value you can use it in later expressions.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_python_variables_types.s02.b01",
                    "role": "syntax",
                    "text": "A valid variable name is made of letters, digits and underscores, cannot start with a digit, is case-significant (delivery_minutes and Delivery_Minutes are two different names), and cannot be a reserved keyword such as if, for or class.",
                    "lineage": {
                        "concept_ids": ["python.variables_assignment"],
                        "fact_ids": ["python.variables_assignment#f4"],
                        "teaching_block_ids": ["python.variables_assignment#tb4"],
                        "anchors": []
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_python_variables_types.s02.b02",
                    "role": "example",
                    "text": "Once a name holds a value, later code can use it in an expression. After orders_per_driver = 20 and days_worked = 5, a line such as orders_per_driver * days_worked reads back both stored values and computes a result from them.",
                    "lineage": {
                        "concept_ids": ["python.variables_assignment"],
                        "fact_ids": ["python.variables_assignment#f5"],
                        "teaching_block_ids": ["python.variables_assignment#tb5"],
                        "anchors": []
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["python.variables_assignment"],
                "fact_ids": [
                    "python.variables_assignment#f4",
                    "python.variables_assignment#f5"
                ],
                "teaching_block_ids": [
                    "python.variables_assignment#tb4",
                    "python.variables_assignment#tb5"
                ],
                "anchors": []
            }
        },

        # ── s03: check – framing only ──
        {
            "step_id": "tile_python_variables_types.s03",
            "type": "check",
            "concept_ids": ["python.variables_assignment"],
            "eyebrow": "Quick check",
            "title": "What happens when you use an unassigned name?",
            "lede": "Test whether you can predict what Python does when a name has never been assigned.",
            "reward": {"gems": 10, "first_try_bonus": 5},
            "lineage": {
                "concept_ids": ["python.variables_assignment"],
                "fact_ids": ["python.variables_assignment#f2"],
                "teaching_block_ids": [],
                "anchors": ["python.variables_assignment#assessment:predict_name_error_for_unassigned_name"]
            }
        },

        # ── s04: hands_on – framing only ──
        {
            "step_id": "tile_python_variables_types.s04",
            "type": "hands_on",
            "concept_ids": ["python.variables_assignment"],
            "eyebrow": "Practice",
            "title": "Assign and reassign delivery variables",
            "lede": "Write Python to store delivery values, reassign one of them, and use the stored names in an expression.",
            "reward": {"gems": 15, "first_try_bonus": 5},
            "lineage": {
                "concept_ids": ["python.variables_assignment"],
                "fact_ids": [
                    "python.variables_assignment#f1",
                    "python.variables_assignment#f3",
                    "python.variables_assignment#f4",
                    "python.variables_assignment#f5"
                ],
                "teaching_block_ids": [],
                "anchors": [
                    "python.variables_assignment#practice",
                    "python.variables_assignment#assessment:assign_and_reassign_variables",
                    "python.variables_assignment#assessment:choose_valid_variable_name"
                ]
            }
        },

        # ── s05: explainer – core_data_types tb1+tb2+tb3+tb4, side_by_side visual ──
        {
            "step_id": "tile_python_variables_types.s05",
            "type": "explainer",
            "concept_ids": ["python.core_data_types"],
            "eyebrow": "Core data types",
            "title": "Four kinds of value: int, float, str and bool",
            "lede": "Every value in Python has a type. Delivery data uses all four core scalar types.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_python_variables_types.s05.b01",
                    "role": "intro",
                    "text": "Every value in Python has a type. In delivery data, an order id like 1042, a delivery time like 32.5, a city name like 'Lagos', and whether an order was late are four different kinds of value — Python has a core scalar type for each.",
                    "lineage": {
                        "concept_ids": ["python.core_data_types"],
                        "fact_ids": [
                            "python.core_data_types#f1",
                            "python.core_data_types#f2",
                            "python.core_data_types#f3"
                        ],
                        "teaching_block_ids": ["python.core_data_types#tb1"],
                        "anchors": []
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_python_variables_types.s05.b02",
                    "role": "definition",
                    "text": "Whole numbers written without a decimal point — such as 2, 4 or 20 — have type int. A literal written with a fractional part, such as 5.0 or 1.6, has type float. So order_id = 1042 is an int, while delivery_minutes = 32.5 is a float.",
                    "lineage": {
                        "concept_ids": ["python.core_data_types"],
                        "fact_ids": ["python.core_data_types#f1"],
                        "teaching_block_ids": ["python.core_data_types#tb2"],
                        "anchors": []
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_python_variables_types.s05.b03",
                    "role": "definition",
                    "text": "Text values are of type str. They can be written with single quotes or double quotes with the same result — city = 'Lagos' and city = \"Lagos\" create the identical string value.",
                    "lineage": {
                        "concept_ids": ["python.core_data_types"],
                        "fact_ids": ["python.core_data_types#f2"],
                        "teaching_block_ids": ["python.core_data_types#tb3"],
                        "anchors": []
                    }
                },
                {
                    "type": "side_by_side",
                    "block_id": "tile_python_variables_types.s05.b04",
                    "left": {
                        "type": "code_walkthrough",
                        "block_id": "tile_python_variables_types.s05.b04.left",
                        "language": "python",
                        "code": "order_id = 1042        # int\ndelivery_minutes = 32.5  # float",
                        "annotations": [
                            {"start_line": 1, "end_line": 1, "text": "Whole number → int"},
                            {"start_line": 2, "end_line": 2, "text": "Fractional part → float"}
                        ],
                        "reveal": "all"
                    },
                    "right": {
                        "type": "code_walkthrough",
                        "block_id": "tile_python_variables_types.s05.b04.right",
                        "language": "python",
                        "code": "city = 'Lagos'   # str\nis_late = True   # bool",
                        "annotations": [
                            {"start_line": 1, "end_line": 1, "text": "Text in quotes → str"},
                            {"start_line": 2, "end_line": 2, "text": "True or False → bool"}
                        ],
                        "reveal": "all"
                    },
                    "left_label": "int and float",
                    "right_label": "str and bool",
                    "takeaway": "1042, 32.5, 'Lagos' and True are four different kinds of value — int, float, str and bool.",
                    "lineage": {
                        "concept_ids": ["python.core_data_types"],
                        "fact_ids": [
                            "python.core_data_types#f1",
                            "python.core_data_types#f2",
                            "python.core_data_types#f3"
                        ],
                        "teaching_block_ids": [
                            "python.core_data_types#tb2",
                            "python.core_data_types#tb3",
                            "python.core_data_types#tb4"
                        ],
                        "anchors": ["python.core_data_types#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["python.core_data_types"],
                "fact_ids": [
                    "python.core_data_types#f1",
                    "python.core_data_types#f2",
                    "python.core_data_types#f3"
                ],
                "teaching_block_ids": [
                    "python.core_data_types#tb1",
                    "python.core_data_types#tb2",
                    "python.core_data_types#tb3",
                    "python.core_data_types#tb4"
                ],
                "anchors": ["python.core_data_types#visual"]
            }
        },

        # ── s06: explainer – core_data_types tb5+tb6 ──
        {
            "step_id": "tile_python_variables_types.s06",
            "type": "explainer",
            "concept_ids": ["python.core_data_types"],
            "eyebrow": "Core data types",
            "title": "Printing values and checking types",
            "lede": "Two built-in tools let you see what a value is and what type it has.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_python_variables_types.s06.b01",
                    "role": "mechanism",
                    "text": "print() writes the value of its argument. When that value is a string, print() writes it without the surrounding quotes — print(city) displays Lagos, not 'Lagos'.",
                    "lineage": {
                        "concept_ids": ["python.core_data_types"],
                        "fact_ids": ["python.core_data_types#f4"],
                        "teaching_block_ids": ["python.core_data_types#tb5"],
                        "anchors": []
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_python_variables_types.s06.b02",
                    "role": "syntax",
                    "text": "The built-in type() function returns the type of its argument. print(type(delivery_minutes)) shows <class 'float'> and print(type(city)) shows <class 'str'>, so you can check a value's type directly.",
                    "lineage": {
                        "concept_ids": ["python.core_data_types"],
                        "fact_ids": ["python.core_data_types#f5"],
                        "teaching_block_ids": ["python.core_data_types#tb6"],
                        "anchors": []
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["python.core_data_types"],
                "fact_ids": [
                    "python.core_data_types#f4",
                    "python.core_data_types#f5"
                ],
                "teaching_block_ids": [
                    "python.core_data_types#tb5",
                    "python.core_data_types#tb6"
                ],
                "anchors": []
            }
        },

        # ── s07: check – framing only ──
        {
            "step_id": "tile_python_variables_types.s07",
            "type": "check",
            "concept_ids": ["python.core_data_types"],
            "eyebrow": "Quick check",
            "title": "Predict print() output and check a type",
            "lede": "Test whether you can predict what print() and type() produce for a given value.",
            "reward": {"gems": 10, "first_try_bonus": 5},
            "lineage": {
                "concept_ids": ["python.core_data_types"],
                "fact_ids": [
                    "python.core_data_types#f4",
                    "python.core_data_types#f5"
                ],
                "teaching_block_ids": [],
                "anchors": ["python.core_data_types#assessment:predict_print_output_and_check_type"]
            }
        },

        # ── s08: hands_on – framing only ──
        {
            "step_id": "tile_python_variables_types.s08",
            "type": "hands_on",
            "concept_ids": ["python.core_data_types"],
            "eyebrow": "Practice",
            "title": "Create one variable of each core type",
            "lede": "Write Python to create an int, float, str and bool variable, then print the type of each using type().",
            "reward": {"gems": 15, "first_try_bonus": 5},
            "lineage": {
                "concept_ids": ["python.core_data_types"],
                "fact_ids": [
                    "python.core_data_types#f1",
                    "python.core_data_types#f2",
                    "python.core_data_types#f3",
                    "python.core_data_types#f4",
                    "python.core_data_types#f5"
                ],
                "teaching_block_ids": [],
                "anchors": [
                    "python.core_data_types#practice",
                    "python.core_data_types#assessment:identify_value_type",
                    "python.core_data_types#assessment:predict_print_output_and_check_type"
                ]
            }
        },

        # ── s09: recap ──
        {
            "step_id": "tile_python_variables_types.s09",
            "type": "recap",
            "concept_ids": [
                "python.variables_assignment",
                "python.core_data_types"
            ],
            "eyebrow": "Recap",
            "title": "What you learned",
            "lede": "Key ideas from this tile.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_python_variables_types.s09.b01",
                    "role": "takeaway",
                    "text": "= stores a value under a name; assigning again to that name replaces what it held; using a name that was never assigned raises a NameError. The four core scalar types are int, float, str and bool — type() tells you which one a value is.",
                    "lineage": {
                        "concept_ids": [
                            "python.variables_assignment",
                            "python.core_data_types"
                        ],
                        "fact_ids": [
                            "python.variables_assignment#f1",
                            "python.variables_assignment#f2",
                            "python.variables_assignment#f3",
                            "python.core_data_types#f1",
                            "python.core_data_types#f2",
                            "python.core_data_types#f3",
                            "python.core_data_types#f5"
                        ],
                        "teaching_block_ids": [
                            "python.variables_assignment#tb6",
                            "python.core_data_types#tb7"
                        ],
                        "anchors": []
                    }
                },
                {
                    "type": "up_next",
                    "block_id": "tile_python_variables_types.s09.b02",
                    "title": "Up next: Operators and Type Conversion",
                    "text": "In the next tile you will use arithmetic and comparison operators on the values you have just learned to store."
                }
            ],
            "reward": {"gems": 10},
            "lineage": {
                "concept_ids": [
                    "python.variables_assignment",
                    "python.core_data_types"
                ],
                "fact_ids": [
                    "python.core_data_types#f1",
                    "python.core_data_types#f2",
                    "python.core_data_types#f3",
                    "python.core_data_types#f5",
                    "python.variables_assignment#f1",
                    "python.variables_assignment#f2",
                    "python.variables_assignment#f3"
                ],
                "teaching_block_ids": [
                    "python.variables_assignment#tb6",
                    "python.core_data_types#tb7"
                ],
                "anchors": []
            }
        }
    ],

    # ── remediation steps ──
    "remediation_steps": [
        # r01: re-teaches f2 (NameError for unassigned name) — for s03
        {
            "step_id": "tile_python_variables_types.r01",
            "type": "remediation",
            "concept_ids": ["python.variables_assignment"],
            "eyebrow": "Let's revisit",
            "title": "Why does Python raise NameError?",
            "lede": "A name only exists after you assign it. Here is the contrast.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_python_variables_types.r01.b01",
                    "role": "misconception",
                    "text": "Python does not create a variable for you automatically. If you write print(average_delivery_minutes) before any line has assigned a value to that name, Python raises NameError: name 'average_delivery_minutes' is not defined. You must assign first: average_delivery_minutes = 32 before you can use it.",
                    "lineage": {
                        "concept_ids": ["python.variables_assignment"],
                        "fact_ids": ["python.variables_assignment#f2"],
                        "teaching_block_ids": ["python.variables_assignment#tb2"],
                        "anchors": []
                    }
                },
                {
                    "type": "before_after",
                    "block_id": "tile_python_variables_types.r01.b02",
                    "before": {
                        "type": "code_walkthrough",
                        "block_id": "tile_python_variables_types.r01.b02.before",
                        "language": "python",
                        "code": "print(average_delivery_minutes)",
                        "annotations": [
                            {
                                "start_line": 1,
                                "end_line": 1,
                                "text": "NameError — name was never assigned"
                            }
                        ],
                        "reveal": "all"
                    },
                    "after": {
                        "type": "code_walkthrough",
                        "block_id": "tile_python_variables_types.r01.b02.after",
                        "language": "python",
                        "code": "average_delivery_minutes = 32\nprint(average_delivery_minutes)",
                        "annotations": [
                            {
                                "start_line": 1,
                                "end_line": 1,
                                "text": "Assign first"
                            },
                            {
                                "start_line": 2,
                                "end_line": 2,
                                "text": "Now the name exists — prints 32"
                            }
                        ],
                        "reveal": "all"
                    },
                    "change_summary": "Adding the assignment before the print removes the NameError.",
                    "lineage": {
                        "concept_ids": ["python.variables_assignment"],
                        "fact_ids": ["python.variables_assignment#f2"],
                        "teaching_block_ids": ["python.variables_assignment#tb2"],
                        "anchors": []
                    }
                }
            ],
            "lineage": {
                "concept_ids": ["python.variables_assignment"],
                "fact_ids": ["python.variables_assignment#f2"],
                "teaching_block_ids": ["python.variables_assignment#tb2"],
                "anchors": []
            }
        },

        # r02: re-teaches f1,f3,f4,f5 — for s04 (hands_on)
        {
            "step_id": "tile_python_variables_types.r02",
            "type": "remediation",
            "concept_ids": ["python.variables_assignment"],
            "eyebrow": "Let's revisit",
            "title": "Assigning, reassigning and naming variables",
            "lede": "A quick recap of the rules before you try the exercise again.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_python_variables_types.r02.b01",
                    "role": "mechanism",
                    "text": "Use = to assign: delivery_minutes = 32. Assigning again to the same name replaces the old value — delivery_minutes = 45 makes the name hold 45. Once assigned, you can use the name in an expression: orders_per_driver * days_worked reads both stored values.",
                    "lineage": {
                        "concept_ids": ["python.variables_assignment"],
                        "fact_ids": [
                            "python.variables_assignment#f1",
                            "python.variables_assignment#f3",
                            "python.variables_assignment#f5"
                        ],
                        "teaching_block_ids": [
                            "python.variables_assignment#tb1",
                            "python.variables_assignment#tb3",
                            "python.variables_assignment#tb5"
                        ],
                        "anchors": []
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_python_variables_types.r02.b02",
                    "role": "syntax",
                    "text": "A valid name uses letters, digits and underscores, cannot start with a digit, is case-significant, and cannot be a reserved keyword such as if or for. delivery_minutes is valid; 1st_order and for are not.",
                    "lineage": {
                        "concept_ids": ["python.variables_assignment"],
                        "fact_ids": ["python.variables_assignment#f4"],
                        "teaching_block_ids": ["python.variables_assignment#tb4"],
                        "anchors": []
                    }
                }
            ],
            "lineage": {
                "concept_ids": ["python.variables_assignment"],
                "fact_ids": [
                    "python.variables_assignment#f1",
                    "python.variables_assignment#f3",
                    "python.variables_assignment#f4",
                    "python.variables_assignment#f5"
                ],
                "teaching_block_ids": [
                    "python.variables_assignment#tb1",
                    "python.variables_assignment#tb3",
                    "python.variables_assignment#tb4",
                    "python.variables_assignment#tb5"
                ],
                "anchors": []
            }
        },

        # r03: re-teaches f4,f5 — for s07 (check: predict_print_output_and_check_type)
        {
            "step_id": "tile_python_variables_types.r03",
            "type": "remediation",
            "concept_ids": ["python.core_data_types"],
            "eyebrow": "Let's revisit",
            "title": "What print() and type() show",
            "lede": "A clear contrast between what print() displays and what type() returns.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_python_variables_types.r03.b01",
                    "role": "mechanism",
                    "text": "print() writes the value without quotes — print(city) displays Lagos, not 'Lagos'. type() returns the type object — print(type(city)) shows <class 'str'> and print(type(delivery_minutes)) shows <class 'float'>.",
                    "lineage": {
                        "concept_ids": ["python.core_data_types"],
                        "fact_ids": [
                            "python.core_data_types#f4",
                            "python.core_data_types#f5"
                        ],
                        "teaching_block_ids": [
                            "python.core_data_types#tb5",
                            "python.core_data_types#tb6"
                        ],
                        "anchors": []
                    }
                },
                {
                    "type": "before_after",
                    "block_id": "tile_python_variables_types.r03.b02",
                    "before": {
                        "type": "code_walkthrough",
                        "block_id": "tile_python_variables_types.r03.b02.before",
                        "language": "python",
                        "code": "city = 'Lagos'\nprint(city)",
                        "annotations": [
                            {
                                "start_line": 2,
                                "end_line": 2,
                                "text": "Displays: Lagos  (no quotes)"
                            }
                        ],
                        "reveal": "all"
                    },
                    "after": {
                        "type": "code_walkthrough",
                        "block_id": "tile_python_variables_types.r03.b02.after",
                        "language": "python",
                        "code": "city = 'Lagos'\nprint(type(city))",
                        "annotations": [
                            {
                                "start_line": 2,
                                "end_line": 2,
                                "text": "Displays: <class 'str'>"
                            }
                        ],
                        "reveal": "all"
                    },
                    "change_summary": "Wrapping city in type() changes the output from the value to its type.",
                    "lineage": {
                        "concept_ids": ["python.core_data_types"],
                        "fact_ids": [
                            "python.core_data_types#f4",
                            "python.core_data_types#f5"
                        ],
                        "teaching_block_ids": [
                            "python.core_data_types#tb5",
                            "python.core_data_types#tb6"
                        ],
                        "anchors": []
                    }
                }
            ],
            "lineage": {
                "concept_ids": ["python.core_data_types"],
                "fact_ids": [
                    "python.core_data_types#f4",
                    "python.core_data_types#f5"
                ],
                "teaching_block_ids": [
                    "python.core_data_types#tb5",
                    "python.core_data_types#tb6"
                ],
                "anchors": []
            }
        },

        # r04: re-teaches f1,f2,f3,f4,f5 — for s08 (hands_on: identify_value_type + predict_print_output_and_check_type)
        {
            "step_id": "tile_python_variables_types.r04",
            "type": "remediation",
            "concept_ids": ["python.core_data_types"],
            "eyebrow": "Let's revisit",
            "title": "The four core types and how to inspect them",
            "lede": "A quick recap of int, float, str and bool, plus print() and type().",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_python_variables_types.r04.b01",
                    "role": "definition",
                    "text": "Whole numbers are int (order_id = 1042); numbers with a decimal point are float (delivery_minutes = 32.5); text in quotes is str (city = 'Lagos'); True or False is bool (is_late = True). These are the four core scalar types.",
                    "lineage": {
                        "concept_ids": ["python.core_data_types"],
                        "fact_ids": [
                            "python.core_data_types#f1",
                            "python.core_data_types#f2",
                            "python.core_data_types#f3"
                        ],
                        "teaching_block_ids": [
                            "python.core_data_types#tb2",
                            "python.core_data_types#tb3",
                            "python.core_data_types#tb4"
                        ],
                        "anchors": []
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_python_variables_types.r04.b02",
                    "role": "syntax",
                    "text": "print(city) displays Lagos without quotes. print(type(city)) shows <class 'str'>. Use type() any time you need to confirm what kind of value a variable holds.",
                    "lineage": {
                        "concept_ids": ["python.core_data_types"],
                        "fact_ids": [
                            "python.core_data_types#f4",
                            "python.core_data_types#f5"
                        ],
                        "teaching_block_ids": [
                            "python.core_data_types#tb5",
                            "python.core_data_types#tb6"
                        ],
                        "anchors": []
                    }
                }
            ],
            "lineage": {
                "concept_ids": ["python.core_data_types"],
                "fact_ids": [
                    "python.core_data_types#f1",
                    "python.core_data_types#f2",
                    "python.core_data_types#f3",
                    "python.core_data_types#f4",
                    "python.core_data_types#f5"
                ],
                "teaching_block_ids": [
                    "python.core_data_types#tb2",
                    "python.core_data_types#tb3",
                    "python.core_data_types#tb4",
                    "python.core_data_types#tb5",
                    "python.core_data_types#tb6"
                ],
                "anchors": []
            }
        }
    ]
}

# Word count checks
print("=== Word count checks ===")
# s01 budget: 165
s01_words = 0
for b in tile["steps"][0]["blocks"]:
    if b["type"] == "prose":
        s01_words += wc(b["text"])
print(f"s01 prose words: {s01_words} / 165 budget")

# s02 budget: 122
s02_words = sum(wc(b["text"]) for b in tile["steps"][1]["blocks"] if b["type"] == "prose")
print(f"s02 prose words: {s02_words} / 122 budget")

# s05 budget: 154
s05_words = sum(wc(b["text"]) for b in tile["steps"][4]["blocks"] if b["type"] == "prose")
print(f"s05 prose words: {s05_words} / 154 budget")

# s06 budget: 72
s06_words = sum(wc(b["text"]) for b in tile["steps"][5]["blocks"] if b["type"] == "prose")
print(f"s06 prose words: {s06_words} / 72 budget")

# s09 budget: 90
s09_words = sum(wc(b["text"]) for b in tile["steps"][8]["blocks"] if b["type"] == "prose")
print(f"s09 prose words: {s09_words} / 90 budget")

output = {
    "schema_version": "0.1.0",
    "kind": "screens_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_008_da_python_core",
    "tiles": [tile]
}

with open("batches/final_batch_008_da_python_core/screens.part.c0_canary.json", "w") as f:
    json.dump(output, f, indent=2)

print("\nFile written.")
print(f"Steps: {len(tile['steps'])}")
print(f"Remediation steps: {len(tile['remediation_steps'])}")
