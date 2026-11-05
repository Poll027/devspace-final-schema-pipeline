"""Build screens.part.c0_canary.json for tile_pandas_dataframe_reading."""
import json

# ── helpers ──────────────────────────────────────────────────────────────────
def qid(concept, frag):
    """Return a qualified id like pandas.dataframe_series_model#f1"""
    return f"{concept}#{frag}"

DSM = "pandas.dataframe_series_model"
RD  = "pandas.reading_data"

tile = {
    "tile_id": "tile_pandas_dataframe_reading",
    "title": "DataFrames, Series, and Reading Data",
    "summary": (
        "Learn the two core pandas data structures — Series and DataFrame — "
        "and how to load tabular data from CSV and Excel files into a DataFrame."
    ),
    "steps": [],
    "remediation_steps": []
}

# ── s01: explainer — Series + DataFrame intro + diagram ──────────────────────
# Plan: tb1, tb2, tb3 → f1, f2, f3 | budget 174 | visual: diagram
# Prose word counts kept ≤ 90 each; total ≤ 174
tile["steps"].append({
    "step_id": "tile_pandas_dataframe_reading.s01",
    "type": "explainer",
    "concept_ids": [DSM],
    "eyebrow": "Series & DataFrame",
    "title": "Two building blocks: Series and DataFrame",
    "lede": (
        "Every pandas table is built from just two structures. "
        "Understanding them makes every later operation predictable."
    ),
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_pandas_dataframe_reading.s01.b1",
            "role": "definition",
            "text": (
                "A pandas **Series** is a one-dimensional labeled array that can hold data of any type. "
                "Its axis labels are collectively called the **index**. "
                "Think of it as a single column of a spreadsheet: each cell has a value, "
                "and each row has a label on the left."
            ),
            "lineage": {
                "concept_ids": [DSM],
                "teaching_block_ids": [qid(DSM, "tb1")],
                "fact_ids": [qid(DSM, "f1")]
            }
        },
        {
            "type": "prose",
            "block_id": "tile_pandas_dataframe_reading.s01.b2",
            "role": "example",
            "text": (
                "A Series can be built from a Python list, a dict, or a scalar. "
                "`pd.Series([18, 20, 22, 22, 26, 28, 80])` — SwiftDrop delivery times — "
                "gets index labels 0 through 6 by default. "
                "`pd.Series({\"Lagos\": 18, \"Abuja\": 20, \"Kano\": 26})` uses the dict keys as the index instead."
            ),
            "lineage": {
                "concept_ids": [DSM],
                "teaching_block_ids": [qid(DSM, "tb2")],
                "fact_ids": [qid(DSM, "f3")]
            }
        },
        {
            "type": "prose",
            "block_id": "tile_pandas_dataframe_reading.s01.b3",
            "role": "definition",
            "text": (
                "A pandas **DataFrame** is a two-dimensional labeled data structure whose columns can hold different types. "
                "It can be thought of as a dict of Series objects that all share the same index — "
                "one Series per column, all aligned row-by-row."
            ),
            "lineage": {
                "concept_ids": [DSM],
                "teaching_block_ids": [qid(DSM, "tb3")],
                "fact_ids": [qid(DSM, "f2")]
            }
        },
        {
            # diagram: DataFrame as columns side by side, each column = a Series, shared index on left
            "type": "diagram",
            "block_id": "tile_pandas_dataframe_reading.s01.b4",
            "diagram_kind": "container",
            "title": "A DataFrame is a collection of Series sharing one index",
            "nodes": [
                {"id": "idx",       "label": "Index\n0\n1\n2",          "kind": "index"},
                {"id": "col_order", "label": "order_id\n1001\n1002\n1003", "kind": "series", "group": "dataframe"},
                {"id": "col_city",  "label": "city\nLagos\nAbuja\nKano",   "kind": "series", "group": "dataframe"},
                {"id": "col_dt",    "label": "delivery_time_minutes\n18\n20\n22", "kind": "series", "group": "dataframe"}
            ],
            "edges": [
                {"from": "idx", "to": "col_order", "label": "shared index"},
                {"from": "idx", "to": "col_city",  "label": "shared index"},
                {"from": "idx", "to": "col_dt",    "label": "shared index"}
            ],
            "layout": "manual",
            "alt_text": (
                "A DataFrame shown as three columns side by side — order_id, city, delivery_time_minutes — "
                "each highlighted as a Series, all sharing the same index (0, 1, 2) on the left."
            ),
            "lineage": {
                "concept_ids": [DSM],
                "teaching_block_ids": [qid(DSM, "tb1"), qid(DSM, "tb3")],
                "fact_ids": [qid(DSM, "f1"), qid(DSM, "f2")],
                "anchors": [qid(DSM, "visual")]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": [DSM],
        "teaching_block_ids": [qid(DSM, "tb1"), qid(DSM, "tb2"), qid(DSM, "tb3")],
        "fact_ids": [qid(DSM, "f1"), qid(DSM, "f2"), qid(DSM, "f3")],
        "anchors": [qid(DSM, "visual")]
    }
})

# ── s02: video — media_group ──────────────────────────────────────────────────
tile["steps"].append({
    "step_id": "tile_pandas_dataframe_reading.s02",
    "type": "video",
    "concept_ids": [DSM],
    "eyebrow": "Series & DataFrame",
    "title": "Series and DataFrame from plain Python data",
    "lede": "Watch how a list becomes a Series and a dict of lists becomes a DataFrame.",
    "blocks": [
        {
            "type": "media_group",
            "block_id": "tile_pandas_dataframe_reading.s02.b1",
            "segment_ids": [
                "seg_pandas.dataframe_series_model_W6WFX_H-AA4_0_161",
                "seg_pandas.dataframe_series_model_zmdjNSmRXF4_189_668"
            ]
        }
    ],
    "reward": {"gems": 3},
    "lineage": {
        "concept_ids": [DSM],
        "teaching_block_ids": [],
        "fact_ids": [qid(DSM, "f1"), qid(DSM, "f2"), qid(DSM, "f4")],
        "segment_ids": [
            "seg_pandas.dataframe_series_model_W6WFX_H-AA4_0_161",
            "seg_pandas.dataframe_series_model_zmdjNSmRXF4_189_668"
        ]
    }
})

# ── s03: explainer — DataFrame from dict + column access ─────────────────────
# Plan: tb4, tb5 → f4, f5 | budget 120
tile["steps"].append({
    "step_id": "tile_pandas_dataframe_reading.s03",
    "type": "explainer",
    "concept_ids": [DSM],
    "eyebrow": "Series & DataFrame",
    "title": "Building a DataFrame and accessing columns",
    "lede": "Pass a dict of equal-length lists to pd.DataFrame and use bracket notation to get or set columns.",
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_pandas_dataframe_reading.s03.b1",
            "role": "example",
            "text": (
                "Pass a dict of equal-length lists to `pd.DataFrame()` and each key becomes a column name: "
                "`orders = pd.DataFrame({\"order_id\": [1001, 1002, 1003], "
                "\"city\": [\"Lagos\", \"Abuja\", \"Kano\"], "
                "\"delivery_time_minutes\": [18, 20, 26]})` "
                "produces a three-column, three-row orders table."
            ),
            "lineage": {
                "concept_ids": [DSM],
                "teaching_block_ids": [qid(DSM, "tb4")],
                "fact_ids": [qid(DSM, "f4")]
            }
        },
        {
            "type": "prose",
            "block_id": "tile_pandas_dataframe_reading.s03.b2",
            "role": "mechanism",
            "text": (
                "A DataFrame behaves like a dict of like-indexed Series. "
                "`orders['city']` returns the city column as a Series. "
                "`orders['courier'] = ['Ada', 'Bayo', 'Chidi']` adds a new column — "
                "the same bracket syntax you use to read or write a dict entry."
            ),
            "lineage": {
                "concept_ids": [DSM],
                "teaching_block_ids": [qid(DSM, "tb5")],
                "fact_ids": [qid(DSM, "f5")]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": [DSM],
        "teaching_block_ids": [qid(DSM, "tb4"), qid(DSM, "tb5")],
        "fact_ids": [qid(DSM, "f4"), qid(DSM, "f5")]
    }
})

# ── s04: check — framing only ─────────────────────────────────────────────────
tile["steps"].append({
    "step_id": "tile_pandas_dataframe_reading.s04",
    "type": "check",
    "concept_ids": [DSM],
    "eyebrow": "Quick check",
    "title": "Columns and Series",
    "lede": "Test your understanding of how DataFrame columns relate to Series.",
    "reward": {"gems": 5, "first_try_bonus": 3},
    "lineage": {
        "concept_ids": [DSM],
        "teaching_block_ids": [],
        "fact_ids": [qid(DSM, "f1"), qid(DSM, "f2"), qid(DSM, "f5")],
        "anchors": [qid(DSM, "assessment:relate_dataframe_columns_to_series")]
    }
})

# ── s05: hands_on — framing only ──────────────────────────────────────────────
tile["steps"].append({
    "step_id": "tile_pandas_dataframe_reading.s05",
    "type": "hands_on",
    "concept_ids": [DSM],
    "eyebrow": "Hands-on",
    "title": "Build a Series and a DataFrame",
    "lede": (
        "Create a Series from a list of delivery times, build a DataFrame from a dict of lists, "
        "then pull one column out and confirm it is a Series."
    ),
    "reward": {"gems": 10, "first_try_bonus": 5},
    "lineage": {
        "concept_ids": [DSM],
        "teaching_block_ids": [],
        "fact_ids": [
            qid(DSM, "f1"), qid(DSM, "f2"), qid(DSM, "f3"),
            qid(DSM, "f4"), qid(DSM, "f5")
        ],
        "anchors": [
            qid(DSM, "practice"),
            qid(DSM, "assessment:construct_series_from_list_or_dict"),
            qid(DSM, "assessment:construct_dataframe_from_dict_of_lists"),
            qid(DSM, "assessment:relate_dataframe_columns_to_series")
        ]
    }
})

# ── s06: explainer — reading_data + before_after visual ──────────────────────
# Plan: tb1–tb5 → f1–f4 | budget 153 | visual: before_after
tile["steps"].append({
    "step_id": "tile_pandas_dataframe_reading.s06",
    "type": "explainer",
    "concept_ids": [RD],
    "eyebrow": "Reading Data",
    "title": "Loading CSV and Excel files into a DataFrame",
    "lede": "Delivery records often arrive as CSV exports or Excel workbooks. Two pandas functions cover both.",
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_pandas_dataframe_reading.s06.b1",
            "role": "intro",
            "text": (
                "Before pandas can work with your delivery records, you read the file into a DataFrame. "
                "`pd.read_csv(\"orders.csv\")` is the main function for reading a delimited text file — "
                "such as a CSV — into a DataFrame. "
                "`pd.read_excel(\"orders.xlsx\", sheet_name=\"January\")` reads an Excel workbook instead."
            ),
            "lineage": {
                "concept_ids": [RD],
                "teaching_block_ids": [qid(RD, "tb1"), qid(RD, "tb2"), qid(RD, "tb3")],
                "fact_ids": [qid(RD, "f1"), qid(RD, "f2")]
            }
        },
        {
            "type": "prose",
            "block_id": "tile_pandas_dataframe_reading.s06.b2",
            "role": "mechanism",
            "text": (
                "`read_csv()` takes the file path (or URL) as its first argument. "
                "`read_excel()` additionally takes `sheet_name` to choose which sheet to load — "
                "that is why the Excel call names `\"January\"` but the CSV call does not need to. "
                "`read_csv()` also accepts `sep` to change the field delimiter: "
                "`pd.read_csv(\"orders.csv\", sep=\";\")` handles a semicolon-delimited export correctly."
            ),
            "lineage": {
                "concept_ids": [RD],
                "teaching_block_ids": [qid(RD, "tb4"), qid(RD, "tb5")],
                "fact_ids": [qid(RD, "f3"), qid(RD, "f4")]
            }
        },
        {
            # before_after: CSV plain text → DataFrame
            # before: code_walkthrough showing the CSV content
            # after: data_table showing the resulting DataFrame (asset_ref)
            "type": "before_after",
            "block_id": "tile_pandas_dataframe_reading.s06.b3",
            "before": {
                "type": "code_walkthrough",
                "block_id": "tile_pandas_dataframe_reading.s06.b3.before",
                "language": "python",
                "code": (
                    "# orders.csv — plain text on disk\n"
                    "order_id,city,delivery_time_minutes\n"
                    "1001,Lagos,18\n"
                    "1002,Abuja,20\n"
                    "1003,Kano,22\n"
                    "\n"
                    "# Read it into a DataFrame\n"
                    "import pandas as pd\n"
                    "orders = pd.read_csv(\"orders.csv\")"
                ),
                "annotations": [
                    {
                        "start_line": 1,
                        "end_line": 5,
                        "text": "CSV file: comma-separated plain text with a header row"
                    },
                    {
                        "start_line": 8,
                        "end_line": 9,
                        "text": "File path is the first argument; pandas infers the header from row 1"
                    }
                ],
                "reveal": "all"
            },
            "after": {
                "type": "data_table",
                "block_id": "tile_pandas_dataframe_reading.s06.b3.after",
                "asset_ref": {
                    "asset_id": "ds_orders",
                    "variant_id": None,
                    "columns": ["order_id", "city", "delivery_time_minutes"],
                    "max_rows": 3
                },
                "caption": "The DataFrame produced by pd.read_csv(\"orders.csv\") — columns taken from the header row, index added automatically.",
                "tag_columns": [
                    {"column": "order_id",               "tag": "from CSV header", "tone": "focus"},
                    {"column": "city",                   "tag": "from CSV header", "tone": "focus"},
                    {"column": "delivery_time_minutes",  "tag": "from CSV header", "tone": "focus"}
                ]
            },
            "change_summary": "pd.read_csv(\"orders.csv\") turns the plain-text CSV on the left into the labeled DataFrame on the right.",
            "lineage": {
                "concept_ids": [RD],
                "teaching_block_ids": [qid(RD, "tb2"), qid(RD, "tb4")],
                "fact_ids": [qid(RD, "f1"), qid(RD, "f3")],
                "anchors": [qid(RD, "visual")]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": [RD],
        "teaching_block_ids": [
            qid(RD, "tb1"), qid(RD, "tb2"), qid(RD, "tb3"),
            qid(RD, "tb4"), qid(RD, "tb5")
        ],
        "fact_ids": [qid(RD, "f1"), qid(RD, "f2"), qid(RD, "f3"), qid(RD, "f4")],
        "anchors": [qid(RD, "visual")]
    }
})

# ── s07: video — media_group ──────────────────────────────────────────────────
tile["steps"].append({
    "step_id": "tile_pandas_dataframe_reading.s07",
    "type": "video",
    "concept_ids": [RD],
    "eyebrow": "Reading Data",
    "title": "Reading a CSV into a DataFrame",
    "lede": "Watch a one-line read_csv call load a file into a DataFrame.",
    "blocks": [
        {
            "type": "media_group",
            "block_id": "tile_pandas_dataframe_reading.s07.b1",
            "segment_ids": [
                "seg_pandas.reading_data_dUpyC40cF6Q_58_172"
            ]
        }
    ],
    "reward": {"gems": 3},
    "lineage": {
        "concept_ids": [RD],
        "teaching_block_ids": [],
        "fact_ids": [qid(RD, "f1")],
        "segment_ids": ["seg_pandas.reading_data_dUpyC40cF6Q_58_172"]
    }
})

# ── s08: check — framing only ─────────────────────────────────────────────────
tile["steps"].append({
    "step_id": "tile_pandas_dataframe_reading.s08",
    "type": "check",
    "concept_ids": [RD],
    "eyebrow": "Quick check",
    "title": "Choosing the right reader",
    "lede": "Which pandas function do you call for a CSV file, and which for an Excel workbook?",
    "reward": {"gems": 5, "first_try_bonus": 3},
    "lineage": {
        "concept_ids": [RD],
        "teaching_block_ids": [],
        "fact_ids": [qid(RD, "f1"), qid(RD, "f2")],
        "anchors": [
            qid(RD, "assessment:choose_read_csv_for_delimited_text"),
            qid(RD, "assessment:choose_read_excel_for_workbooks")
        ]
    }
})

# ── s09: check — framing only ─────────────────────────────────────────────────
tile["steps"].append({
    "step_id": "tile_pandas_dataframe_reading.s09",
    "type": "check",
    "concept_ids": [RD],
    "eyebrow": "Quick check",
    "title": "Arguments: path, sheet_name, and sep",
    "lede": "Test your knowledge of the key arguments for read_csv and read_excel.",
    "reward": {"gems": 5, "first_try_bonus": 3},
    "lineage": {
        "concept_ids": [RD],
        "teaching_block_ids": [],
        "fact_ids": [qid(RD, "f3"), qid(RD, "f4")],
        "anchors": [qid(RD, "assessment:set_path_sheet_name_and_sep_arguments")]
    }
})

# ── s10: hands_on — framing only ──────────────────────────────────────────────
tile["steps"].append({
    "step_id": "tile_pandas_dataframe_reading.s10",
    "type": "hands_on",
    "concept_ids": [RD],
    "eyebrow": "Hands-on",
    "title": "Load the SwiftDrop orders CSV",
    "lede": (
        "Load the provided orders CSV into a DataFrame and print it "
        "to confirm the expected columns and rows arrived."
    ),
    "reward": {"gems": 10, "first_try_bonus": 5},
    "lineage": {
        "concept_ids": [RD],
        "teaching_block_ids": [],
        "fact_ids": [],
        "anchors": [qid(RD, "practice")]
    }
})

# ── s11: recap ────────────────────────────────────────────────────────────────
# Plan: tb6 (DSM) + tb6 (RD) → f1,f2 (DSM) + f1,f2 (RD) | budget 90 | up_next
tile["steps"].append({
    "step_id": "tile_pandas_dataframe_reading.s11",
    "type": "recap",
    "concept_ids": [DSM, RD],
    "eyebrow": "Recap",
    "title": "What you've learned",
    "lede": "Two structures, two readers — the foundation for every pandas operation ahead.",
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_pandas_dataframe_reading.s11.b1",
            "role": "takeaway",
            "text": (
                "A **Series** is a one-dimensional labeled array; a **DataFrame** is a collection of Series sharing one index. "
                "Pull a column with `df['col']` and you get a Series back. "
                "`pd.read_csv()` loads a delimited text file; `pd.read_excel()` loads a workbook. "
                "Either way, the result is a DataFrame ready to work with."
            ),
            "lineage": {
                "concept_ids": [DSM, RD],
                "teaching_block_ids": [qid(DSM, "tb6"), qid(RD, "tb6")],
                "fact_ids": [
                    qid(DSM, "f1"), qid(DSM, "f2"),
                    qid(RD, "f1"), qid(RD, "f2")
                ]
            }
        },
        {
            "type": "up_next",
            "block_id": "tile_pandas_dataframe_reading.s11.b2",
            "title": "Up next: Creating and Inspecting DataFrames",
            "text": (
                "Not every DataFrame starts life as a file — sometimes delivery data already exists as Python data "
                "and you build the table directly from it. Next you'll create DataFrames from Python objects "
                "and use head, shape, dtypes, info, and describe to understand what's inside."
            )
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": [DSM, RD],
        "teaching_block_ids": [qid(DSM, "tb6"), qid(RD, "tb6")],
        "fact_ids": [
            qid(DSM, "f1"), qid(DSM, "f2"),
            qid(RD, "f1"), qid(RD, "f2")
        ]
    }
})

# ── remediation steps ─────────────────────────────────────────────────────────
# Rule 7: first check/hands_on of each concept gets a remediation step.
# s04 (check) measures f1,f2,f5 → relate_dataframe_columns_to_series
# s05 (hands_on) measures f1-f5 — covers construct_series, construct_df, relate
#   s04 and s05 share the same concept and the check (s04) is the first check.
#   s04 measures f1,f2,f5; s05 measures f1-f5 (different facts from s04 for f3,f4)
#   → need one remediation for s04 (f1,f2,f5) and one for s05 (f3,f4 are new)
# s08 (check) measures f1,f2 → choose_read_csv / choose_read_excel
# s09 (check) measures f3,f4 → set_path_sheet_name_and_sep_arguments

# rem_s04: re-teaches f1, f2, f5 (relate_dataframe_columns_to_series)
tile["remediation_steps"].append({
    "step_id": "tile_pandas_dataframe_reading.r01",
    "type": "remediation",
    "concept_ids": [DSM],
    "eyebrow": "Let's revisit",
    "title": "Columns are Series — a closer look",
    "lede": "A DataFrame column and a Series are the same thing. Here's the contrast that makes it click.",
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_pandas_dataframe_reading.r01.b1",
            "role": "definition",
            "text": (
                "A **Series** is a one-dimensional labeled array — its labels are the index. "
                "A **DataFrame** is a two-dimensional structure you can think of as a dict of Series sharing one index. "
                "Every column in a DataFrame is itself a Series."
            ),
            "lineage": {
                "concept_ids": [DSM],
                "teaching_block_ids": [qid(DSM, "tb1"), qid(DSM, "tb3")],
                "fact_ids": [qid(DSM, "f1"), qid(DSM, "f2")]
            }
        },
        {
            "type": "prose",
            "block_id": "tile_pandas_dataframe_reading.r01.b2",
            "role": "mechanism",
            "text": (
                "Use `orders['delivery_time_minutes']` to pull the delivery-time column out of the SwiftDrop orders table. "
                "The result is a Series — the same one-dimensional, indexed structure — sharing the DataFrame's index. "
                "`orders['courier'] = ['Ada', 'Bayo', 'Chidi']` adds a new column using the same dict-style syntax."
            ),
            "lineage": {
                "concept_ids": [DSM],
                "teaching_block_ids": [qid(DSM, "tb5")],
                "fact_ids": [qid(DSM, "f5")]
            }
        }
    ],
    "lineage": {
        "concept_ids": [DSM],
        "teaching_block_ids": [qid(DSM, "tb1"), qid(DSM, "tb3"), qid(DSM, "tb5")],
        "fact_ids": [qid(DSM, "f1"), qid(DSM, "f2"), qid(DSM, "f5")]
    }
})

# rem_s05: re-teaches f3, f4 (construct_series_from_list_or_dict, construct_dataframe_from_dict_of_lists)
tile["remediation_steps"].append({
    "step_id": "tile_pandas_dataframe_reading.r02",
    "type": "remediation",
    "concept_ids": [DSM],
    "eyebrow": "Let's revisit",
    "title": "Constructing a Series and a DataFrame",
    "lede": "Two constructors, two input shapes — here is the contrast.",
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_pandas_dataframe_reading.r02.b1",
            "role": "example",
            "text": (
                "Pass a Python list to `pd.Series()` and the index defaults to 0, 1, …, n−1. "
                "Pass a dict and the dict's keys become the index labels. "
                "`pd.Series([18, 20, 22, 22, 26, 28, 80])` gives index 0–6; "
                "`pd.Series({\"Lagos\": 18, \"Abuja\": 20, \"Kano\": 26})` gives city-name labels."
            ),
            "lineage": {
                "concept_ids": [DSM],
                "teaching_block_ids": [qid(DSM, "tb2")],
                "fact_ids": [qid(DSM, "f3")]
            }
        },
        {
            "type": "prose",
            "block_id": "tile_pandas_dataframe_reading.r02.b2",
            "role": "example",
            "text": (
                "Pass a dict of equal-length lists to `pd.DataFrame()` and each key becomes a column name. "
                "`pd.DataFrame({\"order_id\": [1001, 1002, 1003], \"city\": [\"Lagos\", \"Abuja\", \"Kano\"], "
                "\"delivery_time_minutes\": [18, 20, 26]})` builds a three-column, three-row orders table."
            ),
            "lineage": {
                "concept_ids": [DSM],
                "teaching_block_ids": [qid(DSM, "tb4")],
                "fact_ids": [qid(DSM, "f4")]
            }
        }
    ],
    "lineage": {
        "concept_ids": [DSM],
        "teaching_block_ids": [qid(DSM, "tb2"), qid(DSM, "tb4")],
        "fact_ids": [qid(DSM, "f3"), qid(DSM, "f4")]
    }
})

# rem_s08: re-teaches f1, f2 (choose_read_csv / choose_read_excel)
tile["remediation_steps"].append({
    "step_id": "tile_pandas_dataframe_reading.r03",
    "type": "remediation",
    "concept_ids": [RD],
    "eyebrow": "Let's revisit",
    "title": "read_csv vs read_excel — which file, which function",
    "lede": "The file extension tells you which reader to call.",
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_pandas_dataframe_reading.r03.b1",
            "role": "definition",
            "text": (
                "`pd.read_csv()` is the main pandas function for reading a delimited text file — such as a CSV — into a DataFrame. "
                "`pd.read_excel()` reads an Excel file (such as a .xlsx workbook) into a DataFrame. "
                "Use `read_csv` for `orders.csv`; use `read_excel` for `orders.xlsx`."
            ),
            "lineage": {
                "concept_ids": [RD],
                "teaching_block_ids": [qid(RD, "tb2"), qid(RD, "tb3")],
                "fact_ids": [qid(RD, "f1"), qid(RD, "f2")]
            }
        }
    ],
    "lineage": {
        "concept_ids": [RD],
        "teaching_block_ids": [qid(RD, "tb2"), qid(RD, "tb3")],
        "fact_ids": [qid(RD, "f1"), qid(RD, "f2")]
    }
})

# rem_s09: re-teaches f3, f4 (set_path_sheet_name_and_sep_arguments)
tile["remediation_steps"].append({
    "step_id": "tile_pandas_dataframe_reading.r04",
    "type": "remediation",
    "concept_ids": [RD],
    "eyebrow": "Let's revisit",
    "title": "Key arguments: path, sheet_name, and sep",
    "lede": "Three arguments cover the most common reading scenarios.",
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_pandas_dataframe_reading.r04.b1",
            "role": "mechanism",
            "text": (
                "`read_csv()` takes the file path (or URL) as its first argument. "
                "`read_excel()` additionally takes `sheet_name` to choose which sheet to load — "
                "that is why `pd.read_excel(\"orders.xlsx\", sheet_name=\"January\")` names the sheet "
                "but `pd.read_csv(\"orders.csv\")` does not need to. "
                "`read_csv()` also accepts `sep` to change the delimiter: "
                "`pd.read_csv(\"orders.csv\", sep=\";\")` handles a semicolon-delimited export."
            ),
            "lineage": {
                "concept_ids": [RD],
                "teaching_block_ids": [qid(RD, "tb4"), qid(RD, "tb5")],
                "fact_ids": [qid(RD, "f3"), qid(RD, "f4")]
            }
        }
    ],
    "lineage": {
        "concept_ids": [RD],
        "teaching_block_ids": [qid(RD, "tb4"), qid(RD, "tb5")],
        "fact_ids": [qid(RD, "f3"), qid(RD, "f4")]
    }
})

# ── assemble output ───────────────────────────────────────────────────────────
output = {
    "schema_version": "0.1.0",
    "kind": "screens_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_009_da_pandas",
    "tiles": [tile]
}

out_path = "batches/final_batch_009_da_pandas/screens.part.c0_canary.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"Written: {out_path}")
print(f"Steps: {len(tile['steps'])}")
print(f"Remediation steps: {len(tile['remediation_steps'])}")
for s in tile["steps"]:
    print(f"  {s['step_id']} ({s['type']})")
for r in tile["remediation_steps"]:
    print(f"  {r['step_id']} ({r['type']})")
