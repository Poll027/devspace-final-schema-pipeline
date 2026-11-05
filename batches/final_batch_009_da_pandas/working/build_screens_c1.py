"""
Build screens.part.c1.json for tiles:
  - tile_pandas_creating_inspecting
  - tile_pandas_selection_filtering
  - tile_pandas_sort_rename
"""
import json

# ── helpers ──────────────────────────────────────────────────────────────────

def qid(concept_id, suffix):
    """Qualified id: concept_id#suffix"""
    return f"{concept_id}#{suffix}"


# ── tile_pandas_creating_inspecting ──────────────────────────────────────────

tile_creating_inspecting = {
    "tile_id": "tile_pandas_creating_inspecting",
    "title": "Creating and Inspecting DataFrames",
    "summary": (
        "Build a DataFrame directly from Python data — a dict of lists or a list of dicts — "
        "then use head, shape, dtypes, info, and describe to get an immediate overview of what is inside."
    ),
    "steps": [
        # s01 — explainer: creating_dataframes (side_by_side visual)
        {
            "step_id": "tile_pandas_creating_inspecting.s01",
            "type": "explainer",
            "concept_ids": ["pandas.creating_dataframes"],
            "eyebrow": "Creating DataFrames",
            "title": "Two ways to build a DataFrame from Python data",
            "lede": "Not every DataFrame starts life as a file. When delivery data already exists as Python objects, you can build the table directly.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_pandas_creating_inspecting.s01.b1",
                    "role": "example",
                    "text": (
                        "Pass a **dict of equal-length lists** to `pd.DataFrame()` and each key becomes a column name; "
                        "each list becomes that column's values. With no index argument the result uses a default range index: "
                        "`orders = pd.DataFrame({\"order_id\": [1001, 1002, 1003], \"city\": [\"Lagos\", \"Abuja\", \"Kano\"]})`."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.creating_dataframes"],
                        "teaching_block_ids": ["pandas.creating_dataframes#tb2"],
                        "fact_ids": ["pandas.creating_dataframes#f1"]
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_pandas_creating_inspecting.s01.b2",
                    "role": "example",
                    "text": (
                        "Alternatively, pass a **list of dicts** where each dict becomes one row and the dict keys become column names: "
                        "`orders = pd.DataFrame([{\"order_id\": 1001, \"city\": \"Lagos\"}, {\"order_id\": 1002, \"city\": \"Abuja\"}])`. "
                        "Both routes produce the same kind of table — pick whichever shape your data is already in."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.creating_dataframes"],
                        "teaching_block_ids": ["pandas.creating_dataframes#tb3", "pandas.creating_dataframes#tb4"],
                        "fact_ids": ["pandas.creating_dataframes#f2"]
                    }
                },
                {
                    "type": "side_by_side",
                    "block_id": "tile_pandas_creating_inspecting.s01.b3",
                    "left_label": "Dict of lists (one key per column)",
                    "right_label": "List of dicts (one dict per row)",
                    "left": {
                        "type": "code_walkthrough",
                        "language": "python",
                        "code": (
                            "orders = pd.DataFrame({\n"
                            "    \"order_id\": [1001, 1002, 1003],\n"
                            "    \"city\":     [\"Lagos\", \"Abuja\", \"Kano\"],\n"
                            "})"
                        ),
                        "annotations": [
                            {"start_line": 1, "end_line": 4, "text": "Each key → column name; each list → column values"}
                        ]
                    },
                    "right": {
                        "type": "code_walkthrough",
                        "language": "python",
                        "code": (
                            "orders = pd.DataFrame([\n"
                            "    {\"order_id\": 1001, \"city\": \"Lagos\"},\n"
                            "    {\"order_id\": 1002, \"city\": \"Abuja\"},\n"
                            "    {\"order_id\": 1003, \"city\": \"Kano\"},\n"
                            "])"
                        ),
                        "annotations": [
                            {"start_line": 1, "end_line": 5, "text": "Each dict → one row; keys → column names"}
                        ]
                    },
                    "takeaway": "Both produce the same orders table — choose the shape that matches your existing Python data.",
                    "lineage": {
                        "concept_ids": ["pandas.creating_dataframes"],
                        "teaching_block_ids": [
                            "pandas.creating_dataframes#tb2",
                            "pandas.creating_dataframes#tb3"
                        ],
                        "fact_ids": [
                            "pandas.creating_dataframes#f1",
                            "pandas.creating_dataframes#f2"
                        ],
                        "anchors": ["pandas.creating_dataframes#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["pandas.creating_dataframes"],
                "teaching_block_ids": [
                    "pandas.creating_dataframes#tb1",
                    "pandas.creating_dataframes#tb2",
                    "pandas.creating_dataframes#tb3"
                ],
                "fact_ids": [
                    "pandas.creating_dataframes#f1",
                    "pandas.creating_dataframes#f2"
                ],
                "anchors": ["pandas.creating_dataframes#visual"]
            }
        },

        # s02 — video: creating_dataframes
        {
            "step_id": "tile_pandas_creating_inspecting.s02",
            "type": "video",
            "concept_ids": ["pandas.creating_dataframes"],
            "eyebrow": "Creating DataFrames",
            "title": "Building a DataFrame from Python data",
            "lede": "See how a dict of lists becomes a DataFrame in a live coding session.",
            "blocks": [
                {
                    "type": "media_group",
                    "block_id": "tile_pandas_creating_inspecting.s02.b1",
                    "segment_ids": [
                        "seg_pandas.creating_dataframes_OUnnuKHbmbU_0_134"
                    ]
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["pandas.creating_dataframes"],
                "teaching_block_ids": [],
                "fact_ids": ["pandas.creating_dataframes#f1"],
                "segment_ids": ["seg_pandas.creating_dataframes_OUnnuKHbmbU_0_134"]
            }
        },

        # s03 — check: creating_dataframes (framing only)
        {
            "step_id": "tile_pandas_creating_inspecting.s03",
            "type": "check",
            "concept_ids": ["pandas.creating_dataframes"],
            "eyebrow": "Quick check",
            "title": "Building a DataFrame from a list of dicts",
            "lede": "Confirm you can identify what each dict contributes when you pass a list of dicts to pd.DataFrame.",
            "reward": {"gems": 5, "first_try_bonus": 3},
            "lineage": {
                "concept_ids": ["pandas.creating_dataframes"],
                "teaching_block_ids": [],
                "fact_ids": ["pandas.creating_dataframes#f2"],
                "anchors": ["pandas.creating_dataframes#assessment:build_dataframe_from_list_of_dicts"]
            }
        },

        # s04 — hands_on: creating_dataframes (framing only)
        {
            "step_id": "tile_pandas_creating_inspecting.s04",
            "type": "hands_on",
            "concept_ids": ["pandas.creating_dataframes"],
            "eyebrow": "Hands-on",
            "title": "Create a DataFrame two ways",
            "lede": "Build the same small orders table once from a dict of lists and once from a list of dicts, then confirm both produce the same result.",
            "reward": {"gems": 10, "first_try_bonus": 5},
            "lineage": {
                "concept_ids": ["pandas.creating_dataframes"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "pandas.creating_dataframes#f1",
                    "pandas.creating_dataframes#f2"
                ],
                "anchors": [
                    "pandas.creating_dataframes#practice",
                    "pandas.creating_dataframes#assessment:build_dataframe_from_dict_of_lists",
                    "pandas.creating_dataframes#assessment:build_dataframe_from_list_of_dicts"
                ]
            }
        },

        # s05 — explainer: inspecting_dataframes (annotated_image visual)
        {
            "step_id": "tile_pandas_creating_inspecting.s05",
            "type": "explainer",
            "concept_ids": ["pandas.inspecting_dataframes"],
            "eyebrow": "Inspecting DataFrames",
            "title": "Five methods that answer your first questions about a DataFrame",
            "lede": "Before doing anything else with a newly loaded or built orders DataFrame, get an overview of what is actually in it.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_pandas_creating_inspecting.s05.b1",
                    "role": "mechanism",
                    "text": (
                        "`orders.head()` shows the first five delivery records by default — a quick sanity check that the data loaded correctly. "
                        "`orders.shape` returns a tuple of (rows, columns), such as `(250, 10)` for 250 orders across 10 columns."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.inspecting_dataframes"],
                        "teaching_block_ids": [
                            "pandas.inspecting_dataframes#tb2",
                            "pandas.inspecting_dataframes#tb3"
                        ],
                        "fact_ids": [
                            "pandas.inspecting_dataframes#f1",
                            "pandas.inspecting_dataframes#f2"
                        ]
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_pandas_creating_inspecting.s05.b2",
                    "role": "mechanism",
                    "text": (
                        "`orders.dtypes` returns the data type of each column — for example, that `delivery_time_minutes` holds integers and `city` holds text. "
                        "`orders.info()` combines that dtype list with a count of non-missing values per column and the DataFrame's memory usage in one concise summary."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.inspecting_dataframes"],
                        "teaching_block_ids": [
                            "pandas.inspecting_dataframes#tb4",
                            "pandas.inspecting_dataframes#tb5"
                        ],
                        "fact_ids": [
                            "pandas.inspecting_dataframes#f3",
                            "pandas.inspecting_dataframes#f4"
                        ]
                    }
                },
                {
                    "type": "annotated_image",
                    "block_id": "tile_pandas_creating_inspecting.s05.b3",
                    "asset_id": "img_inspect_overview",
                    "alt_text": (
                        "Five pandas inspection outputs on the SwiftDrop orders DataFrame: "
                        "head() showing the first five rows, shape returning (250, 10), "
                        "dtypes listing each column's type, info() showing non-null counts and memory, "
                        "and describe() showing statistics for numeric columns — each labelled with the question it answers."
                    ),
                    "hotspots": [
                        {"x": 0.05, "y": 0.08, "w": 0.40, "h": 0.18,
                         "label": "head()", "detail": "What do the first rows look like?"},
                        {"x": 0.55, "y": 0.08, "w": 0.40, "h": 0.08,
                         "label": "shape", "detail": "How many rows and columns?"},
                        {"x": 0.55, "y": 0.20, "w": 0.40, "h": 0.18,
                         "label": "dtypes", "detail": "What type is each column?"},
                        {"x": 0.05, "y": 0.35, "w": 0.40, "h": 0.28,
                         "label": "info()", "detail": "How many non-missing values? How much memory?"},
                        {"x": 0.55, "y": 0.35, "w": 0.40, "h": 0.28,
                         "label": "describe()", "detail": "What do the numbers look like statistically?"}
                    ],
                    "lineage": {
                        "concept_ids": ["pandas.inspecting_dataframes"],
                        "teaching_block_ids": [
                            "pandas.inspecting_dataframes#tb1",
                            "pandas.inspecting_dataframes#tb2",
                            "pandas.inspecting_dataframes#tb3",
                            "pandas.inspecting_dataframes#tb4",
                            "pandas.inspecting_dataframes#tb5"
                        ],
                        "fact_ids": [
                            "pandas.inspecting_dataframes#f1",
                            "pandas.inspecting_dataframes#f2",
                            "pandas.inspecting_dataframes#f3",
                            "pandas.inspecting_dataframes#f4"
                        ],
                        "anchors": ["pandas.inspecting_dataframes#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["pandas.inspecting_dataframes"],
                "teaching_block_ids": [
                    "pandas.inspecting_dataframes#tb1",
                    "pandas.inspecting_dataframes#tb2",
                    "pandas.inspecting_dataframes#tb3",
                    "pandas.inspecting_dataframes#tb4",
                    "pandas.inspecting_dataframes#tb5"
                ],
                "fact_ids": [
                    "pandas.inspecting_dataframes#f1",
                    "pandas.inspecting_dataframes#f2",
                    "pandas.inspecting_dataframes#f3",
                    "pandas.inspecting_dataframes#f4"
                ],
                "anchors": ["pandas.inspecting_dataframes#visual"]
            }
        },

        # s06 — video: inspecting_dataframes
        {
            "step_id": "tile_pandas_creating_inspecting.s06",
            "type": "video",
            "concept_ids": ["pandas.inspecting_dataframes"],
            "eyebrow": "Inspecting DataFrames",
            "title": "head, shape, dtypes, info, and describe in action",
            "lede": "Watch each inspection method called on a real table and see what it returns.",
            "blocks": [
                {
                    "type": "media_group",
                    "block_id": "tile_pandas_creating_inspecting.s06.b1",
                    "segment_ids": [
                        "seg_pandas.inspecting_dataframes_Liv6eeb1VfE_225_366",
                        "seg_pandas.inspecting_dataframes_ZyhVh-qRZPA_677_860",
                        "seg_pandas.inspecting_dataframes_BspcRHPiFk4_104_562"
                    ]
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["pandas.inspecting_dataframes"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "pandas.inspecting_dataframes#f1",
                    "pandas.inspecting_dataframes#f2",
                    "pandas.inspecting_dataframes#f3",
                    "pandas.inspecting_dataframes#f4",
                    "pandas.inspecting_dataframes#f5"
                ],
                "segment_ids": [
                    "seg_pandas.inspecting_dataframes_Liv6eeb1VfE_225_366",
                    "seg_pandas.inspecting_dataframes_ZyhVh-qRZPA_677_860",
                    "seg_pandas.inspecting_dataframes_BspcRHPiFk4_104_562"
                ]
            }
        },

        # s07 — explainer: inspecting_dataframes (describe, tb6, f5)
        {
            "step_id": "tile_pandas_creating_inspecting.s07",
            "type": "explainer",
            "concept_ids": ["pandas.inspecting_dataframes"],
            "eyebrow": "Inspecting DataFrames",
            "title": "describe() — a statistical overview in one call",
            "lede": "One method summarises all numeric columns at once.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_pandas_creating_inspecting.s07.b1",
                    "role": "mechanism",
                    "text": (
                        "`orders.describe()` computes a quick statistical overview of each numeric column — "
                        "count, mean, std, min, quartiles, and max — in a single call."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.inspecting_dataframes"],
                        "teaching_block_ids": ["pandas.inspecting_dataframes#tb6"],
                        "fact_ids": ["pandas.inspecting_dataframes#f5"]
                    }
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["pandas.inspecting_dataframes"],
                "teaching_block_ids": ["pandas.inspecting_dataframes#tb6"],
                "fact_ids": ["pandas.inspecting_dataframes#f5"]
            }
        },

        # s08 — check: inspecting_dataframes (shape + info)
        {
            "step_id": "tile_pandas_creating_inspecting.s08",
            "type": "check",
            "concept_ids": ["pandas.inspecting_dataframes"],
            "eyebrow": "Quick check",
            "title": "shape and info",
            "lede": "Test your understanding of what shape and info() each report about a DataFrame.",
            "reward": {"gems": 5, "first_try_bonus": 3},
            "lineage": {
                "concept_ids": ["pandas.inspecting_dataframes"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "pandas.inspecting_dataframes#f2",
                    "pandas.inspecting_dataframes#f4"
                ],
                "anchors": [
                    "pandas.inspecting_dataframes#assessment:report_rows_and_columns_with_shape",
                    "pandas.inspecting_dataframes#assessment:read_info_summary"
                ]
            }
        },

        # s09 — check: inspecting_dataframes (describe)
        {
            "step_id": "tile_pandas_creating_inspecting.s09",
            "type": "check",
            "concept_ids": ["pandas.inspecting_dataframes"],
            "eyebrow": "Quick check",
            "title": "describe() overview",
            "lede": "Confirm what describe() computes and when to reach for it.",
            "reward": {"gems": 5, "first_try_bonus": 3},
            "lineage": {
                "concept_ids": ["pandas.inspecting_dataframes"],
                "teaching_block_ids": [],
                "fact_ids": ["pandas.inspecting_dataframes#f5"],
                "anchors": ["pandas.inspecting_dataframes#assessment:get_describe_overview"]
            }
        },

        # s10 — hands_on: inspecting_dataframes
        {
            "step_id": "tile_pandas_creating_inspecting.s10",
            "type": "hands_on",
            "concept_ids": ["pandas.inspecting_dataframes"],
            "eyebrow": "Hands-on",
            "title": "Inspect the orders DataFrame",
            "lede": "Call head() to preview the first rows, then use dtypes to read each column's type.",
            "reward": {"gems": 10, "first_try_bonus": 5},
            "lineage": {
                "concept_ids": ["pandas.inspecting_dataframes"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "pandas.inspecting_dataframes#f1",
                    "pandas.inspecting_dataframes#f3"
                ],
                "anchors": [
                    "pandas.inspecting_dataframes#practice",
                    "pandas.inspecting_dataframes#assessment:preview_rows_with_head",
                    "pandas.inspecting_dataframes#assessment:read_column_dtypes"
                ]
            }
        },

        # s11 — recap
        {
            "step_id": "tile_pandas_creating_inspecting.s11",
            "type": "recap",
            "concept_ids": ["pandas.creating_dataframes", "pandas.inspecting_dataframes"],
            "eyebrow": "Recap",
            "title": "What you learned: creating and inspecting DataFrames",
            "lede": "Two construction routes, five inspection tools — here is the summary.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_pandas_creating_inspecting.s11.b1",
                    "role": "summary",
                    "text": (
                        "A DataFrame can be built from a **dict of equal-length lists** (one key per column) "
                        "or a **list of dicts** (one dict per row). Both routes produce the same table — "
                        "pick whichever shape your Python data is already in."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.creating_dataframes"],
                        "teaching_block_ids": ["pandas.creating_dataframes#tb4"],
                        "fact_ids": [
                            "pandas.creating_dataframes#f1",
                            "pandas.creating_dataframes#f2"
                        ]
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_pandas_creating_inspecting.s11.b2",
                    "role": "summary",
                    "text": (
                        "Five methods answer your first questions: `head()` previews rows, `shape` reports dimensions, "
                        "`dtypes` lists column types, `info()` adds non-null counts and memory, "
                        "and `describe()` gives a statistical overview of numeric columns — all in one call each."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.inspecting_dataframes"],
                        "teaching_block_ids": ["pandas.inspecting_dataframes#tb7"],
                        "fact_ids": [
                            "pandas.inspecting_dataframes#f1",
                            "pandas.inspecting_dataframes#f2",
                            "pandas.inspecting_dataframes#f3",
                            "pandas.inspecting_dataframes#f4",
                            "pandas.inspecting_dataframes#f5"
                        ]
                    }
                },
                {
                    "type": "up_next",
                    "block_id": "tile_pandas_creating_inspecting.s11.b3",
                    "title": "Up next: Descriptive Statistics",
                    "text": (
                        "Next you will compute descriptive statistics — mean, median, std, and more — "
                        "directly on DataFrame columns using pandas methods."
                    )
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["pandas.creating_dataframes", "pandas.inspecting_dataframes"],
                "teaching_block_ids": [
                    "pandas.creating_dataframes#tb4",
                    "pandas.inspecting_dataframes#tb7"
                ],
                "fact_ids": [
                    "pandas.creating_dataframes#f1",
                    "pandas.creating_dataframes#f2",
                    "pandas.inspecting_dataframes#f1",
                    "pandas.inspecting_dataframes#f2",
                    "pandas.inspecting_dataframes#f3",
                    "pandas.inspecting_dataframes#f4",
                    "pandas.inspecting_dataframes#f5"
                ]
            }
        }
    ],
    "remediation_steps": [
        # r01 — remediation for s03 (check: build_dataframe_from_list_of_dicts → f2)
        {
            "step_id": "tile_pandas_creating_inspecting.r01",
            "type": "remediation",
            "concept_ids": ["pandas.creating_dataframes"],
            "eyebrow": "Let's revisit",
            "title": "List of dicts: each dict is one row",
            "lede": "When you pass a list of dicts, each dict contributes exactly one row.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_pandas_creating_inspecting.r01.b1",
                    "role": "example",
                    "text": (
                        "In `pd.DataFrame([{\"order_id\": 1001, \"city\": \"Lagos\"}, {\"order_id\": 1002, \"city\": \"Abuja\"}])`, "
                        "the first dict becomes row 0 and the second becomes row 1. "
                        "The dict keys — `order_id` and `city` — become the column names. "
                        "Contrast this with the dict-of-lists form, where each key maps to a whole column."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.creating_dataframes"],
                        "teaching_block_ids": ["pandas.creating_dataframes#tb3"],
                        "fact_ids": ["pandas.creating_dataframes#f2"]
                    }
                }
            ],
            "lineage": {
                "concept_ids": ["pandas.creating_dataframes"],
                "teaching_block_ids": ["pandas.creating_dataframes#tb3"],
                "fact_ids": ["pandas.creating_dataframes#f2"]
            }
        },
        # r02 — remediation for s08 (check: shape + info → f2, f4)
        {
            "step_id": "tile_pandas_creating_inspecting.r02",
            "type": "remediation",
            "concept_ids": ["pandas.inspecting_dataframes"],
            "eyebrow": "Let's revisit",
            "title": "shape vs info() — dimensions vs column detail",
            "lede": "shape tells you how big the table is; info() tells you what is inside each column.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_pandas_creating_inspecting.r02.b1",
                    "role": "contrast",
                    "text": (
                        "`orders.shape` returns a tuple of (rows, columns) — for example `(250, 10)`. "
                        "It answers only: how many rows and how many columns? "
                        "`orders.info()` prints a concise summary that includes column names, their data types, "
                        "how many non-missing values each column has, and the DataFrame's memory usage. "
                        "Use `shape` for a quick size check; use `info()` when you need to see missing-value counts."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.inspecting_dataframes"],
                        "teaching_block_ids": [
                            "pandas.inspecting_dataframes#tb3",
                            "pandas.inspecting_dataframes#tb5"
                        ],
                        "fact_ids": [
                            "pandas.inspecting_dataframes#f2",
                            "pandas.inspecting_dataframes#f4"
                        ]
                    }
                }
            ],
            "lineage": {
                "concept_ids": ["pandas.inspecting_dataframes"],
                "teaching_block_ids": [
                    "pandas.inspecting_dataframes#tb3",
                    "pandas.inspecting_dataframes#tb5"
                ],
                "fact_ids": [
                    "pandas.inspecting_dataframes#f2",
                    "pandas.inspecting_dataframes#f4"
                ]
            }
        },
        # r03 — remediation for s09 (check: describe → f5)
        {
            "step_id": "tile_pandas_creating_inspecting.r03",
            "type": "remediation",
            "concept_ids": ["pandas.inspecting_dataframes"],
            "eyebrow": "Let's revisit",
            "title": "describe() — one call, many statistics",
            "lede": "describe() computes a statistical overview of numeric columns in a single call.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_pandas_creating_inspecting.r03.b1",
                    "role": "example",
                    "text": (
                        "`orders.describe()` computes a quick statistical overview of each numeric column — "
                        "count, mean, std, min, 25th percentile, median (50%), 75th percentile, and max — in a single call. "
                        "It covers all numeric columns at once, so you do not need to call `mean()` and `std()` separately just to get a first look."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.inspecting_dataframes"],
                        "teaching_block_ids": ["pandas.inspecting_dataframes#tb6"],
                        "fact_ids": ["pandas.inspecting_dataframes#f5"]
                    }
                }
            ],
            "lineage": {
                "concept_ids": ["pandas.inspecting_dataframes"],
                "teaching_block_ids": ["pandas.inspecting_dataframes#tb6"],
                "fact_ids": ["pandas.inspecting_dataframes#f5"]
            }
        }
    ]
}


# ── tile_pandas_selection_filtering ──────────────────────────────────────────

tile_selection_filtering = {
    "tile_id": "tile_pandas_selection_filtering",
    "title": "Selecting and Filtering Data",
    "summary": (
        "Use .loc and .iloc to select rows and columns by label or position, "
        "and apply boolean filters — single conditions or combined with & | ~ — to keep only the rows you need."
    ),
    "steps": [
        # s01 — explainer: loc_iloc_selection (side_by_side visual)
        {
            "step_id": "tile_pandas_selection_filtering.s01",
            "type": "explainer",
            "concept_ids": ["pandas.loc_iloc_selection"],
            "eyebrow": "loc & iloc",
            "title": "Two accessors: .loc for labels, .iloc for positions",
            "lede": "Pandas gives two different accessors depending on whether you want to address rows by their labels or by their integer positions.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_pandas_selection_filtering.s01.b1",
                    "role": "definition",
                    "text": (
                        "`.loc` selects data **by label** — row index labels and column names. "
                        "`.iloc` selects data **by integer position**, from 0 to length−1 of the axis. "
                        "Both accept a row selector and a column selector separated by a comma: `df.loc[rows, cols]`. "
                        "A colon (`:`) or omitting an axis means 'all of that axis'."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.loc_iloc_selection"],
                        "teaching_block_ids": [
                            "pandas.loc_iloc_selection#tb2",
                            "pandas.loc_iloc_selection#tb3"
                        ],
                        "fact_ids": [
                            "pandas.loc_iloc_selection#f1",
                            "pandas.loc_iloc_selection#f4"
                        ]
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_pandas_selection_filtering.s01.b2",
                    "role": "example",
                    "text": (
                        "`orders.loc[2:4, \"city\"]` selects the `city` column for the rows **labeled** 2 through 4 — "
                        "and because `.loc` uses label slicing, **both endpoints are included** in the result. "
                        "So `orders.loc[2:4]` returns rows labeled 2, 3, and 4."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.loc_iloc_selection"],
                        "teaching_block_ids": [
                            "pandas.loc_iloc_selection#tb4",
                            "pandas.loc_iloc_selection#tb5"
                        ],
                        "fact_ids": [
                            "pandas.loc_iloc_selection#f2"
                        ]
                    }
                },
                {
                    "type": "side_by_side",
                    "block_id": "tile_pandas_selection_filtering.s01.b3",
                    "left_label": ".loc — label-based (stop included)",
                    "right_label": ".iloc — position-based (stop excluded)",
                    "left": {
                        "type": "data_table",
                        "asset_ref": {
                            "asset_id": "ds_orders",
                            "columns": ["order_id", "city", "delivery_time_minutes"],
                            "max_rows": 5
                        },
                        "caption": "orders.loc[0:2, ['order_id','city']] — rows labeled 0, 1, 2 (all three included)",
                        "highlight": [
                            {"target": {"kind": "row", "row": {"where": {"order_id": 1001}}}, "label": "label 0", "tone": "focus"},
                            {"target": {"kind": "row", "row": {"where": {"order_id": 1002}}}, "label": "label 1", "tone": "focus"},
                            {"target": {"kind": "row", "row": {"where": {"order_id": 1003}}}, "label": "label 2 (stop included)", "tone": "focus"}
                        ]
                    },
                    "right": {
                        "type": "data_table",
                        "asset_ref": {
                            "asset_id": "ds_orders",
                            "columns": ["order_id", "city", "delivery_time_minutes"],
                            "max_rows": 5
                        },
                        "caption": "orders.iloc[0:3, [0,1]] — positions 0, 1, 2 (position 3 excluded)",
                        "highlight": [
                            {"target": {"kind": "row", "row": {"where": {"order_id": 1001}}}, "label": "pos 0", "tone": "focus"},
                            {"target": {"kind": "row", "row": {"where": {"order_id": 1002}}}, "label": "pos 1", "tone": "focus"},
                            {"target": {"kind": "row", "row": {"where": {"order_id": 1003}}}, "label": "pos 2 (stop excluded at 3)", "tone": "focus"}
                        ]
                    },
                    "takeaway": ".loc includes the stop label; .iloc excludes the stop position — double-check this boundary whenever a slice's last row matters.",
                    "lineage": {
                        "concept_ids": ["pandas.loc_iloc_selection"],
                        "teaching_block_ids": [
                            "pandas.loc_iloc_selection#tb2",
                            "pandas.loc_iloc_selection#tb5",
                            "pandas.loc_iloc_selection#tb7"
                        ],
                        "fact_ids": [
                            "pandas.loc_iloc_selection#f1",
                            "pandas.loc_iloc_selection#f2",
                            "pandas.loc_iloc_selection#f4"
                        ],
                        "anchors": ["pandas.loc_iloc_selection#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["pandas.loc_iloc_selection"],
                "teaching_block_ids": [
                    "pandas.loc_iloc_selection#tb1",
                    "pandas.loc_iloc_selection#tb2",
                    "pandas.loc_iloc_selection#tb3",
                    "pandas.loc_iloc_selection#tb4",
                    "pandas.loc_iloc_selection#tb5"
                ],
                "fact_ids": [
                    "pandas.loc_iloc_selection#f1",
                    "pandas.loc_iloc_selection#f2",
                    "pandas.loc_iloc_selection#f4"
                ],
                "anchors": ["pandas.loc_iloc_selection#visual"]
            }
        },

        # s02 — video: loc_iloc_selection
        {
            "step_id": "tile_pandas_selection_filtering.s02",
            "type": "video",
            "concept_ids": ["pandas.loc_iloc_selection"],
            "eyebrow": "loc & iloc",
            "title": "Selecting rows and columns with .loc and .iloc",
            "lede": "Watch .loc and .iloc used on real tables to pick rows by label and by position.",
            "blocks": [
                {
                    "type": "media_group",
                    "block_id": "tile_pandas_selection_filtering.s02.b1",
                    "segment_ids": [
                        "seg_pandas.loc_iloc_selection_zmdjNSmRXF4_934_1327",
                        "seg_pandas.loc_iloc_selection_aoNRYtVEhAM_163_438"
                    ]
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["pandas.loc_iloc_selection"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "pandas.loc_iloc_selection#f1",
                    "pandas.loc_iloc_selection#f3",
                    "pandas.loc_iloc_selection#f4"
                ],
                "segment_ids": [
                    "seg_pandas.loc_iloc_selection_zmdjNSmRXF4_934_1327",
                    "seg_pandas.loc_iloc_selection_aoNRYtVEhAM_163_438"
                ]
            }
        },

        # s03 — explainer: loc_iloc_selection (iloc position rules, tb6+tb7, f3)
        {
            "step_id": "tile_pandas_selection_filtering.s03",
            "type": "explainer",
            "concept_ids": ["pandas.loc_iloc_selection"],
            "eyebrow": "loc & iloc",
            "title": ".iloc uses 0-based positions with an exclusive stop",
            "lede": "iloc follows the same slicing rules as Python lists — the stop position is not included.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_pandas_selection_filtering.s03.b1",
                    "role": "mechanism",
                    "text": (
                        "`orders.iloc[0:3, 0:2]` selects the first three rows (positions 0, 1, 2) and the first two columns (positions 0, 1) "
                        "by pure position. The stop position 3 is **excluded**, following ordinary Python slicing rules. "
                        "So `orders.iloc[0:3]` returns exactly three rows — not four."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.loc_iloc_selection"],
                        "teaching_block_ids": [
                            "pandas.loc_iloc_selection#tb6",
                            "pandas.loc_iloc_selection#tb7"
                        ],
                        "fact_ids": ["pandas.loc_iloc_selection#f3"]
                    }
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["pandas.loc_iloc_selection"],
                "teaching_block_ids": [
                    "pandas.loc_iloc_selection#tb6",
                    "pandas.loc_iloc_selection#tb7"
                ],
                "fact_ids": ["pandas.loc_iloc_selection#f3"]
            }
        },

        # s04 — check: loc_iloc_selection (iloc exclusive stop)
        {
            "step_id": "tile_pandas_selection_filtering.s04",
            "type": "check",
            "concept_ids": ["pandas.loc_iloc_selection"],
            "eyebrow": "Quick check",
            "title": "Predict an iloc slice",
            "lede": "Apply the exclusive-stop rule to predict which rows orders.iloc[1:3] returns.",
            "reward": {"gems": 5, "first_try_bonus": 3},
            "lineage": {
                "concept_ids": ["pandas.loc_iloc_selection"],
                "teaching_block_ids": [],
                "fact_ids": ["pandas.loc_iloc_selection#f3"],
                "anchors": ["pandas.loc_iloc_selection#assessment:predict_iloc_slice_with_exclusive_stop"]
            }
        },

        # s05 — hands_on: loc_iloc_selection
        {
            "step_id": "tile_pandas_selection_filtering.s05",
            "type": "hands_on",
            "concept_ids": ["pandas.loc_iloc_selection"],
            "eyebrow": "Hands-on",
            "title": "Select rows and columns with .loc and .iloc",
            "lede": "Use .loc to select by label and .iloc to select by position on the SwiftDrop orders table.",
            "reward": {"gems": 10, "first_try_bonus": 5},
            "lineage": {
                "concept_ids": ["pandas.loc_iloc_selection"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "pandas.loc_iloc_selection#f1",
                    "pandas.loc_iloc_selection#f2",
                    "pandas.loc_iloc_selection#f3",
                    "pandas.loc_iloc_selection#f4"
                ],
                "anchors": [
                    "pandas.loc_iloc_selection#practice",
                    "pandas.loc_iloc_selection#assessment:choose_loc_or_iloc",
                    "pandas.loc_iloc_selection#assessment:write_row_and_column_selectors",
                    "pandas.loc_iloc_selection#assessment:predict_loc_slice_with_inclusive_stop",
                    "pandas.loc_iloc_selection#assessment:predict_iloc_slice_with_exclusive_stop"
                ]
            }
        },

        # s06 — explainer: boolean_filtering (before_after visual)
        {
            "step_id": "tile_pandas_selection_filtering.s06",
            "type": "explainer",
            "concept_ids": ["pandas.boolean_filtering"],
            "eyebrow": "Boolean Filtering",
            "title": "Filter rows with a True/False mask",
            "lede": "Suppose you only want the delivery orders that took longer than 25 minutes — a boolean filter does exactly that.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_pandas_selection_filtering.s06.b1",
                    "role": "mechanism",
                    "text": (
                        "Comparing a DataFrame column with a value — such as `orders['delivery_time_minutes'] > 25` — "
                        "produces a **True/False Series** of the same length as the column. "
                        "Passing that Series inside `orders[...]` keeps only the rows where the value is `True`."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.boolean_filtering"],
                        "teaching_block_ids": [
                            "pandas.boolean_filtering#tb2",
                            "pandas.boolean_filtering#tb3"
                        ],
                        "fact_ids": [
                            "pandas.boolean_filtering#f1",
                            "pandas.boolean_filtering#f2"
                        ]
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_pandas_selection_filtering.s06.b2",
                    "role": "mechanism",
                    "text": (
                        "When combining multiple conditions, each must be wrapped in parentheses and joined with `&` (and), `|` (or), or `~` (not). "
                        "For example: `orders[(orders['city'] == 'Lagos') & (orders['delivery_time_minutes'] > 25)]`. "
                        "Without the parentheses Python evaluates the comparison operators in the wrong order."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.boolean_filtering"],
                        "teaching_block_ids": ["pandas.boolean_filtering#tb4"],
                        "fact_ids": ["pandas.boolean_filtering#f3"]
                    }
                },
                {
                    "type": "before_after",
                    "block_id": "tile_pandas_selection_filtering.s06.b3",
                    "before": {
                        "type": "data_table",
                        "asset_ref": {
                            "asset_id": "ds_orders",
                            "columns": ["order_id", "city", "delivery_time_minutes"],
                            "max_rows": 7
                        },
                        "caption": "All orders — delivery_time_minutes varies",
                        "tag_columns": [
                            {"column": "delivery_time_minutes", "tag": "mask column", "tone": "neutral"}
                        ]
                    },
                    "after": {
                        "type": "data_table",
                        "asset_ref": {
                            "asset_id": "ds_orders",
                            "columns": ["order_id", "city", "delivery_time_minutes"],
                            "max_rows": 7
                        },
                        "caption": "orders[orders['delivery_time_minutes'] > 25] — only rows where mask is True",
                        "highlight": [
                            {"target": {"kind": "row", "row": {"where": {"order_id": 1005}}}, "label": "True", "tone": "good"},
                            {"target": {"kind": "row", "row": {"where": {"order_id": 1006}}}, "label": "True", "tone": "good"},
                            {"target": {"kind": "row", "row": {"where": {"order_id": 1007}}}, "label": "True", "tone": "good"}
                        ]
                    },
                    "change_summary": "The boolean mask keeps only rows where delivery_time_minutes > 25; all other rows are dropped.",
                    "lineage": {
                        "concept_ids": ["pandas.boolean_filtering"],
                        "teaching_block_ids": [
                            "pandas.boolean_filtering#tb1",
                            "pandas.boolean_filtering#tb2",
                            "pandas.boolean_filtering#tb3"
                        ],
                        "fact_ids": [
                            "pandas.boolean_filtering#f1",
                            "pandas.boolean_filtering#f2"
                        ],
                        "anchors": ["pandas.boolean_filtering#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["pandas.boolean_filtering"],
                "teaching_block_ids": [
                    "pandas.boolean_filtering#tb1",
                    "pandas.boolean_filtering#tb2",
                    "pandas.boolean_filtering#tb3",
                    "pandas.boolean_filtering#tb4"
                ],
                "fact_ids": [
                    "pandas.boolean_filtering#f1",
                    "pandas.boolean_filtering#f2",
                    "pandas.boolean_filtering#f3"
                ],
                "anchors": ["pandas.boolean_filtering#visual"]
            }
        },

        # s07 — video: boolean_filtering
        {
            "step_id": "tile_pandas_selection_filtering.s07",
            "type": "video",
            "concept_ids": ["pandas.boolean_filtering"],
            "eyebrow": "Boolean Filtering",
            "title": "Boolean masks in action",
            "lede": "Watch a comparison expression produce a True/False Series and filter a table.",
            "blocks": [
                {
                    "type": "media_group",
                    "block_id": "tile_pandas_selection_filtering.s07.b1",
                    "segment_ids": [
                        "seg_pandas.boolean_filtering_AdR_gx5Y4wE_198_376",
                        "seg_pandas.boolean_filtering_Lw2rlcxScZY_53_285"
                    ]
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["pandas.boolean_filtering"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "pandas.boolean_filtering#f1",
                    "pandas.boolean_filtering#f2",
                    "pandas.boolean_filtering#f3"
                ],
                "segment_ids": [
                    "seg_pandas.boolean_filtering_AdR_gx5Y4wE_198_376",
                    "seg_pandas.boolean_filtering_Lw2rlcxScZY_53_285"
                ]
            }
        },

        # s08 — check: boolean_filtering (single condition + mask explanation)
        {
            "step_id": "tile_pandas_selection_filtering.s08",
            "type": "check",
            "concept_ids": ["pandas.boolean_filtering"],
            "eyebrow": "Quick check",
            "title": "Writing a single-condition filter",
            "lede": "Confirm you can write a boolean filter and explain what the mask does to the rows.",
            "reward": {"gems": 5, "first_try_bonus": 3},
            "lineage": {
                "concept_ids": ["pandas.boolean_filtering"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "pandas.boolean_filtering#f1",
                    "pandas.boolean_filtering#f2"
                ],
                "anchors": [
                    "pandas.boolean_filtering#assessment:write_single_condition_filter",
                    "pandas.boolean_filtering#assessment:explain_boolean_mask_row_selection"
                ]
            }
        },

        # s09 — check: boolean_filtering (combined conditions)
        {
            "step_id": "tile_pandas_selection_filtering.s09",
            "type": "check",
            "concept_ids": ["pandas.boolean_filtering"],
            "eyebrow": "Quick check",
            "title": "Combining conditions with parentheses",
            "lede": "Identify the correct way to combine two boolean conditions in a pandas filter.",
            "reward": {"gems": 5, "first_try_bonus": 3},
            "lineage": {
                "concept_ids": ["pandas.boolean_filtering"],
                "teaching_block_ids": [],
                "fact_ids": ["pandas.boolean_filtering#f3"],
                "anchors": ["pandas.boolean_filtering#assessment:combine_conditions_with_parentheses"]
            }
        },

        # s10 — hands_on: boolean_filtering
        {
            "step_id": "tile_pandas_selection_filtering.s10",
            "type": "hands_on",
            "concept_ids": ["pandas.boolean_filtering"],
            "eyebrow": "Hands-on",
            "title": "Filter the orders DataFrame",
            "lede": "Write a boolean filter to keep only Lagos orders, then combine two conditions to find long Lagos deliveries.",
            "reward": {"gems": 10, "first_try_bonus": 5},
            "lineage": {
                "concept_ids": ["pandas.boolean_filtering"],
                "teaching_block_ids": [],
                "fact_ids": [],
                "anchors": ["pandas.boolean_filtering#practice"]
            }
        },

        # s11 — recap
        {
            "step_id": "tile_pandas_selection_filtering.s11",
            "type": "recap",
            "concept_ids": ["pandas.loc_iloc_selection", "pandas.boolean_filtering"],
            "eyebrow": "Recap",
            "title": "What you learned: selecting and filtering data",
            "lede": "Two accessors and a mask — here is the summary.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_pandas_selection_filtering.s11.b1",
                    "role": "summary",
                    "text": (
                        "`.loc` selects by **label** and includes the stop label in a slice. "
                        "`.iloc` selects by **integer position** and excludes the stop position, following Python slicing rules. "
                        "Both accept `[rows, cols]` — a colon means 'all of that axis'."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.loc_iloc_selection"],
                        "teaching_block_ids": ["pandas.loc_iloc_selection#tb8"],
                        "fact_ids": [
                            "pandas.loc_iloc_selection#f1",
                            "pandas.loc_iloc_selection#f2",
                            "pandas.loc_iloc_selection#f3"
                        ]
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_pandas_selection_filtering.s11.b2",
                    "role": "summary",
                    "text": (
                        "A boolean filter is a same-length True/False Series you compute first, then pass to `df[...]` to keep only the matching rows. "
                        "When combining conditions with `&`, `|`, or `~`, each condition must be in parentheses."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.boolean_filtering"],
                        "teaching_block_ids": ["pandas.boolean_filtering#tb5"],
                        "fact_ids": [
                            "pandas.boolean_filtering#f1",
                            "pandas.boolean_filtering#f2",
                            "pandas.boolean_filtering#f3"
                        ]
                    }
                },
                {
                    "type": "up_next",
                    "block_id": "tile_pandas_selection_filtering.s11.b3",
                    "title": "Up next: Sorting and Renaming",
                    "text": (
                        "Next you will sort a DataFrame by one or more columns using sort_values, "
                        "and rename column and index labels with rename."
                    )
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["pandas.loc_iloc_selection", "pandas.boolean_filtering"],
                "teaching_block_ids": [
                    "pandas.loc_iloc_selection#tb8",
                    "pandas.boolean_filtering#tb5"
                ],
                "fact_ids": [
                    "pandas.boolean_filtering#f1",
                    "pandas.boolean_filtering#f2",
                    "pandas.boolean_filtering#f3",
                    "pandas.loc_iloc_selection#f1",
                    "pandas.loc_iloc_selection#f2",
                    "pandas.loc_iloc_selection#f3"
                ]
            }
        }
    ],
    "remediation_steps": [
        # r01 — remediation for s04 (check: iloc exclusive stop → f3)
        {
            "step_id": "tile_pandas_selection_filtering.r01",
            "type": "remediation",
            "concept_ids": ["pandas.loc_iloc_selection"],
            "eyebrow": "Let's revisit",
            "title": ".iloc stop position is excluded",
            "lede": "iloc follows Python slicing: the stop is not included in the result.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_pandas_selection_filtering.r01.b1",
                    "role": "contrast",
                    "text": (
                        "`orders.iloc[0:3]` returns rows at positions 0, 1, and 2 — **not** position 3. "
                        "This is the same rule as Python list slicing: `my_list[0:3]` gives three items. "
                        "Contrast with `.loc`: `orders.loc[0:3]` returns rows labeled 0, 1, 2, **and** 3 — "
                        "the stop label is included. Always double-check which accessor you are using when the last row matters."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.loc_iloc_selection"],
                        "teaching_block_ids": [
                            "pandas.loc_iloc_selection#tb7",
                            "pandas.loc_iloc_selection#tb8"
                        ],
                        "fact_ids": ["pandas.loc_iloc_selection#f3"]
                    }
                }
            ],
            "lineage": {
                "concept_ids": ["pandas.loc_iloc_selection"],
                "teaching_block_ids": [
                    "pandas.loc_iloc_selection#tb7",
                    "pandas.loc_iloc_selection#tb8"
                ],
                "fact_ids": ["pandas.loc_iloc_selection#f3"]
            }
        },
        # r02 — remediation for s08 (check: single condition + mask → f1, f2)
        {
            "step_id": "tile_pandas_selection_filtering.r02",
            "type": "remediation",
            "concept_ids": ["pandas.boolean_filtering"],
            "eyebrow": "Let's revisit",
            "title": "How a boolean mask filters rows",
            "lede": "The mask is a True/False Series — only True rows survive.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_pandas_selection_filtering.r02.b1",
                    "role": "mechanism",
                    "text": (
                        "`orders['delivery_time_minutes'] > 25` produces a True/False Series the same length as the DataFrame. "
                        "Passing it inside `orders[...]` keeps only the rows where the value is `True` — "
                        "every row where the condition is `False` is dropped. "
                        "The mask must be the same length as the DataFrame's index; pandas aligns them row by row."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.boolean_filtering"],
                        "teaching_block_ids": [
                            "pandas.boolean_filtering#tb2",
                            "pandas.boolean_filtering#tb3"
                        ],
                        "fact_ids": [
                            "pandas.boolean_filtering#f1",
                            "pandas.boolean_filtering#f2"
                        ]
                    }
                }
            ],
            "lineage": {
                "concept_ids": ["pandas.boolean_filtering"],
                "teaching_block_ids": [
                    "pandas.boolean_filtering#tb2",
                    "pandas.boolean_filtering#tb3"
                ],
                "fact_ids": [
                    "pandas.boolean_filtering#f1",
                    "pandas.boolean_filtering#f2"
                ]
            }
        },
        # r03 — remediation for s09 (check: combined conditions → f3)
        {
            "step_id": "tile_pandas_selection_filtering.r03",
            "type": "remediation",
            "concept_ids": ["pandas.boolean_filtering"],
            "eyebrow": "Let's revisit",
            "title": "Parentheses are required when combining conditions",
            "lede": "Each condition must be in its own parentheses before you join them with & or |.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_pandas_selection_filtering.r03.b1",
                    "role": "contrast",
                    "text": (
                        "When combining conditions, each must be grouped in parentheses: "
                        "`orders[(orders['city'] == 'Lagos') & (orders['delivery_time_minutes'] > 25)]`. "
                        "Without the parentheses, Python evaluates the comparison operators in the wrong order "
                        "and raises a `ValueError`. The `&`, `|`, and `~` operators work element-wise on the boolean Series."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.boolean_filtering"],
                        "teaching_block_ids": ["pandas.boolean_filtering#tb4"],
                        "fact_ids": ["pandas.boolean_filtering#f3"]
                    }
                }
            ],
            "lineage": {
                "concept_ids": ["pandas.boolean_filtering"],
                "teaching_block_ids": ["pandas.boolean_filtering#tb4"],
                "fact_ids": ["pandas.boolean_filtering#f3"]
            }
        }
    ]
}


# ── tile_pandas_sort_rename ───────────────────────────────────────────────────

tile_sort_rename = {
    "tile_id": "tile_pandas_sort_rename",
    "title": "Sorting and Renaming",
    "summary": (
        "Sort a DataFrame by one or more columns with sort_values, controlling ascending/descending order per column, "
        "and rename column and index labels with rename using a dict mapping."
    ),
    "steps": [
        # s01 — explainer: sort_values (before_after visual)
        {
            "step_id": "tile_pandas_sort_rename.s01",
            "type": "explainer",
            "concept_ids": ["pandas.sort_values"],
            "eyebrow": "Sorting",
            "title": "sort_values: sort by one or more columns",
            "lede": "Reorder the rows of a DataFrame by the values in one or more columns.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_pandas_sort_rename.s01.b1",
                    "role": "definition",
                    "text": (
                        "`DataFrame.sort_values(by=...)` sorts rows using the values of the listed column(s). "
                        "When `by` is a list, the first column sets the primary sort order and each later column breaks ties: "
                        "`orders.sort_values(by=['city', 'delivery_time_minutes'])` sorts by city first, "
                        "then by delivery time within each city."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.sort_values"],
                        "teaching_block_ids": ["pandas.sort_values#tb1"],
                        "fact_ids": ["pandas.sort_values#f1"]
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_pandas_sort_rename.s01.b2",
                    "role": "mechanism",
                    "text": (
                        "The `ascending` parameter defaults to `True`. "
                        "Pass a list of booleans matching the length of `by` to sort some columns ascending and others descending in the same call: "
                        "`orders.sort_values(by=['city', 'delivery_time_minutes'], ascending=[True, False])` "
                        "sorts cities alphabetically but delivery times from slowest to fastest within each city."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.sort_values"],
                        "teaching_block_ids": ["pandas.sort_values#tb2"],
                        "fact_ids": ["pandas.sort_values#f2"]
                    }
                },
                {
                    "type": "before_after",
                    "block_id": "tile_pandas_sort_rename.s01.b3",
                    "before": {
                        "type": "data_table",
                        "asset_ref": {
                            "asset_id": "ds_orders",
                            "columns": ["order_id", "city", "delivery_time_minutes"],
                            "max_rows": 7
                        },
                        "caption": "orders — original row order"
                    },
                    "after": {
                        "type": "data_table",
                        "asset_ref": {
                            "asset_id": "ds_orders",
                            "columns": ["order_id", "city", "delivery_time_minutes"],
                            "max_rows": 7
                        },
                        "caption": "orders.sort_values(by=['city','delivery_time_minutes']) — sorted by city, then time",
                        "highlight": [
                            {"target": {"kind": "column", "column": "city"}, "label": "primary sort", "tone": "focus"},
                            {"target": {"kind": "column", "column": "delivery_time_minutes"}, "label": "tie-breaker", "tone": "neutral"}
                        ]
                    },
                    "change_summary": "Rows are reordered: city is the primary sort key; delivery_time_minutes breaks ties within each city.",
                    "lineage": {
                        "concept_ids": ["pandas.sort_values"],
                        "teaching_block_ids": [
                            "pandas.sort_values#tb1",
                            "pandas.sort_values#tb2"
                        ],
                        "fact_ids": [
                            "pandas.sort_values#f1",
                            "pandas.sort_values#f2"
                        ],
                        "anchors": ["pandas.sort_values#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["pandas.sort_values"],
                "teaching_block_ids": [
                    "pandas.sort_values#tb1",
                    "pandas.sort_values#tb2"
                ],
                "fact_ids": [
                    "pandas.sort_values#f1",
                    "pandas.sort_values#f2"
                ],
                "anchors": ["pandas.sort_values#visual"]
            }
        },

        # s02 — check: sort_values (ascending per column)
        {
            "step_id": "tile_pandas_sort_rename.s02",
            "type": "check",
            "concept_ids": ["pandas.sort_values"],
            "eyebrow": "Quick check",
            "title": "Setting ascending per column",
            "lede": "Identify the correct call to sort one column ascending and another descending in the same sort_values call.",
            "reward": {"gems": 5, "first_try_bonus": 3},
            "lineage": {
                "concept_ids": ["pandas.sort_values"],
                "teaching_block_ids": [],
                "fact_ids": ["pandas.sort_values#f2"],
                "anchors": ["pandas.sort_values#assessment:set_ascending_per_column"]
            }
        },

        # s03 — hands_on: sort_values
        {
            "step_id": "tile_pandas_sort_rename.s03",
            "type": "hands_on",
            "concept_ids": ["pandas.sort_values"],
            "eyebrow": "Hands-on",
            "title": "Sort the orders DataFrame",
            "lede": "Sort orders by city ascending, then by delivery_time_minutes descending within each city.",
            "reward": {"gems": 10, "first_try_bonus": 5},
            "lineage": {
                "concept_ids": ["pandas.sort_values"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "pandas.sort_values#f1",
                    "pandas.sort_values#f2"
                ],
                "anchors": [
                    "pandas.sort_values#practice",
                    "pandas.sort_values#assessment:sort_by_one_or_more_columns",
                    "pandas.sort_values#assessment:set_ascending_per_column"
                ]
            }
        },

        # s04 — explainer: rename_columns_index (before_after visual)
        {
            "step_id": "tile_pandas_sort_rename.s04",
            "type": "explainer",
            "concept_ids": ["pandas.rename_columns_index"],
            "eyebrow": "Renaming",
            "title": "rename(): relabel columns and index entries with a dict",
            "lede": "Clean up column names or row labels without rebuilding the DataFrame.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_pandas_sort_rename.s04.b1",
                    "role": "definition",
                    "text": (
                        "`rename()` relabels a DataFrame's axes using a dict mapping. "
                        "Pass `columns=` to rename column labels: "
                        "`orders.rename(columns={'delivery_time_minutes': 'delivery_min'})` "
                        "renames that one column and leaves every other label unchanged."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.rename_columns_index"],
                        "teaching_block_ids": ["pandas.rename_columns_index#tb1"],
                        "fact_ids": ["pandas.rename_columns_index#f1"]
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_pandas_sort_rename.s04.b2",
                    "role": "mechanism",
                    "text": (
                        "A single `rename()` call can rename columns and index labels together by passing both `columns=` and `index=` at once: "
                        "`orders.rename(columns={'city': 'destination_city'}, index={0: 'first_order'})` "
                        "relabels one column and one row label in one call — any label not in the mapping is left as-is."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.rename_columns_index"],
                        "teaching_block_ids": ["pandas.rename_columns_index#tb2"],
                        "fact_ids": ["pandas.rename_columns_index#f2"]
                    }
                },
                {
                    "type": "before_after",
                    "block_id": "tile_pandas_sort_rename.s04.b3",
                    "before": {
                        "type": "data_table",
                        "asset_ref": {
                            "asset_id": "ds_orders",
                            "columns": ["order_id", "city", "delivery_time_minutes"],
                            "max_rows": 4
                        },
                        "caption": "orders — original column names"
                    },
                    "after": {
                        "type": "data_table",
                        "asset_ref": {
                            "asset_id": "ds_orders",
                            "columns": ["order_id", "city", "delivery_time_minutes"],
                            "max_rows": 4
                        },
                        "caption": "orders.rename(columns={'delivery_time_minutes': 'delivery_min', 'city': 'destination_city'})",
                        "highlight": [
                            {"target": {"kind": "column", "column": "city"}, "label": "→ destination_city", "tone": "focus"},
                            {"target": {"kind": "column", "column": "delivery_time_minutes"}, "label": "→ delivery_min", "tone": "focus"}
                        ]
                    },
                    "change_summary": "Two column labels are renamed; order_id and all other labels are unchanged.",
                    "lineage": {
                        "concept_ids": ["pandas.rename_columns_index"],
                        "teaching_block_ids": [
                            "pandas.rename_columns_index#tb1",
                            "pandas.rename_columns_index#tb2"
                        ],
                        "fact_ids": [
                            "pandas.rename_columns_index#f1",
                            "pandas.rename_columns_index#f2"
                        ],
                        "anchors": ["pandas.rename_columns_index#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["pandas.rename_columns_index"],
                "teaching_block_ids": [
                    "pandas.rename_columns_index#tb1",
                    "pandas.rename_columns_index#tb2"
                ],
                "fact_ids": [
                    "pandas.rename_columns_index#f1",
                    "pandas.rename_columns_index#f2"
                ],
                "anchors": ["pandas.rename_columns_index#visual"]
            }
        },

        # s05 — check: rename_columns_index
        {
            "step_id": "tile_pandas_sort_rename.s05",
            "type": "check",
            "concept_ids": ["pandas.rename_columns_index"],
            "eyebrow": "Quick check",
            "title": "Renaming columns with a mapping",
            "lede": "Identify the correct rename() call to relabel a column using a dict.",
            "reward": {"gems": 5, "first_try_bonus": 3},
            "lineage": {
                "concept_ids": ["pandas.rename_columns_index"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "pandas.rename_columns_index#f1",
                    "pandas.rename_columns_index#f2"
                ],
                "anchors": [
                    "pandas.rename_columns_index#assessment:rename_columns_with_mapping",
                    "pandas.rename_columns_index#assessment:rename_columns_and_index_together"
                ]
            }
        },

        # s06 — hands_on: rename_columns_index
        {
            "step_id": "tile_pandas_sort_rename.s06",
            "type": "hands_on",
            "concept_ids": ["pandas.rename_columns_index"],
            "eyebrow": "Hands-on",
            "title": "Rename columns and an index label",
            "lede": "Rename two columns to clearer names and rename one index label in a single rename() call.",
            "reward": {"gems": 10, "first_try_bonus": 5},
            "lineage": {
                "concept_ids": ["pandas.rename_columns_index"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "pandas.rename_columns_index#f1",
                    "pandas.rename_columns_index#f2"
                ],
                "anchors": [
                    "pandas.rename_columns_index#practice",
                    "pandas.rename_columns_index#assessment:rename_columns_with_mapping",
                    "pandas.rename_columns_index#assessment:rename_columns_and_index_together"
                ]
            }
        },

        # s07 — recap
        {
            "step_id": "tile_pandas_sort_rename.s07",
            "type": "recap",
            "concept_ids": ["pandas.sort_values", "pandas.rename_columns_index"],
            "eyebrow": "Recap",
            "title": "What you learned: sorting and renaming",
            "lede": "One method to reorder rows, one method to relabel axes.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_pandas_sort_rename.s07.b1",
                    "role": "summary",
                    "text": (
                        "`sort_values(by=[...])` reorders rows by the listed columns. "
                        "The first column is the primary sort key; later columns break ties. "
                        "`ascending` defaults to `True` and can be a list of booleans to mix directions."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.sort_values"],
                        "teaching_block_ids": [],
                        "fact_ids": [
                            "pandas.sort_values#f1",
                            "pandas.sort_values#f2"
                        ]
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_pandas_sort_rename.s07.b2",
                    "role": "summary",
                    "text": (
                        "`rename(columns={...})` relabels column headers using a dict mapping; "
                        "`rename(index={...})` relabels row index entries. "
                        "Both can be combined in one call — any label not in the mapping is left unchanged."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.rename_columns_index"],
                        "teaching_block_ids": [],
                        "fact_ids": [
                            "pandas.rename_columns_index#f1",
                            "pandas.rename_columns_index#f2"
                        ]
                    }
                },
                {
                    "type": "up_next",
                    "block_id": "tile_pandas_sort_rename.s07.b3",
                    "title": "Up next: Type Conversion and Datetime Handling",
                    "text": (
                        "Next you will convert column dtypes with astype and parse date strings into datetime objects "
                        "so you can extract months, days, and other time components."
                    )
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["pandas.sort_values", "pandas.rename_columns_index"],
                "teaching_block_ids": [],
                "fact_ids": []
            }
        }
    ],
    "remediation_steps": [
        # r01 — remediation for s02 (check: ascending per column → f2)
        {
            "step_id": "tile_pandas_sort_rename.r01",
            "type": "remediation",
            "concept_ids": ["pandas.sort_values"],
            "eyebrow": "Let's revisit",
            "title": "ascending as a list of booleans",
            "lede": "To mix sort directions, pass a list of booleans matching the length of by.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_pandas_sort_rename.r01.b1",
                    "role": "example",
                    "text": (
                        "`sort_values()`'s `ascending` parameter defaults to `True` (all columns sorted ascending). "
                        "To sort some columns ascending and others descending in the same call, pass a list of booleans "
                        "the same length as `by`: "
                        "`orders.sort_values(by=['city', 'delivery_time_minutes'], ascending=[True, False])` "
                        "sorts cities A→Z but delivery times from largest to smallest within each city."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.sort_values"],
                        "teaching_block_ids": ["pandas.sort_values#tb2"],
                        "fact_ids": ["pandas.sort_values#f2"]
                    }
                }
            ],
            "lineage": {
                "concept_ids": ["pandas.sort_values"],
                "teaching_block_ids": ["pandas.sort_values#tb2"],
                "fact_ids": ["pandas.sort_values#f2"]
            }
        },
        # r02 — remediation for s05 (check: rename → f1, f2)
        {
            "step_id": "tile_pandas_sort_rename.r02",
            "type": "remediation",
            "concept_ids": ["pandas.rename_columns_index"],
            "eyebrow": "Let's revisit",
            "title": "rename() with columns= and index= together",
            "lede": "One rename() call can relabel both column headers and row index entries.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_pandas_sort_rename.r02.b1",
                    "role": "example",
                    "text": (
                        "`orders.rename(columns={'delivery_time_minutes': 'delivery_min'})` renames one column; "
                        "every other column label is left unchanged. "
                        "To rename a column and an index label in the same call: "
                        "`orders.rename(columns={'city': 'destination_city'}, index={0: 'first_order'})`. "
                        "Any label not listed in the mapping is untouched."
                    ),
                    "lineage": {
                        "concept_ids": ["pandas.rename_columns_index"],
                        "teaching_block_ids": [
                            "pandas.rename_columns_index#tb1",
                            "pandas.rename_columns_index#tb2"
                        ],
                        "fact_ids": [
                            "pandas.rename_columns_index#f1",
                            "pandas.rename_columns_index#f2"
                        ]
                    }
                }
            ],
            "lineage": {
                "concept_ids": ["pandas.rename_columns_index"],
                "teaching_block_ids": [
                    "pandas.rename_columns_index#tb1",
                    "pandas.rename_columns_index#tb2"
                ],
                "fact_ids": [
                    "pandas.rename_columns_index#f1",
                    "pandas.rename_columns_index#f2"
                ]
            }
        }
    ]
}


# ── assemble and write ────────────────────────────────────────────────────────

output = {
    "schema_version": "0.1.0",
    "kind": "screens_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_009_da_pandas",
    "tiles": [
        tile_creating_inspecting,
        tile_selection_filtering,
        tile_sort_rename
    ]
}

out_path = "batches/final_batch_009_da_pandas/screens.part.c1.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"Written: {out_path}")

# Count steps
for tile in output["tiles"]:
    main = len(tile["steps"])
    rem = len(tile.get("remediation_steps", []))
    print(f"  {tile['tile_id']}: {main} steps + {rem} remediation steps")
