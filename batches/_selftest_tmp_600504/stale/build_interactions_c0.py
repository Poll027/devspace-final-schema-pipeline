"""Build interactions.part.c0_canary.json for tile_pandas_dataframe_reading."""
import json

# ---- helpers ----------------------------------------------------------------

def fact(concept, fid):
    return f"{concept}#{fid}"

def anchor(concept, kind, cap=None):
    if cap:
        return f"{concept}#assessment:{cap}"
    return f"{concept}#{kind}"

# ---- constants --------------------------------------------------------------

TILE = "tile_pandas_dataframe_reading"
DFM  = "pandas.dataframe_series_model"
RD   = "pandas.reading_data"
PY_VERSION = "0.29.5"

# ---- s04: choice — relate_dataframe_columns_to_series ----------------------
# Facts tested: f1, f2, f5 — all taught in s01 (text) and s03 (text)
# Capability: relate_dataframe_columns_to_series
# Difficulty: core (mid-tile, after intro explainer + video + second explainer)

s04 = {
    "step_id": f"{TILE}.s04",
    "interaction": {
        "type": "choice",
        "interaction_id": f"ix.{TILE}.s04",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": DFM,
                "capability": "relate_dataframe_columns_to_series",
                "fact_ids": [
                    fact(DFM, "f1"),
                    fact(DFM, "f2"),
                    fact(DFM, "f5"),
                ]
            }
        ],
        "anchors": [anchor(DFM, "assessment", "relate_dataframe_columns_to_series")],
        "public": {
            "prompt": (
                "You have a DataFrame called `orders` with columns `order_id`, `city`, and `delivery_time_minutes`. "
                "What is the type of `orders['city']`, and how does it relate to the DataFrame?"
            ),
            "options": [
                {
                    "option_id": "opt_a",
                    "text": "It is a pandas Series that shares the same index as the DataFrame."
                },
                {
                    "option_id": "opt_b",
                    "text": "It is a Python list extracted from the DataFrame."
                },
                {
                    "option_id": "opt_c",
                    "text": "It is a new DataFrame containing only the `city` column."
                },
                {
                    "option_id": "opt_d",
                    "text": "It is a dict mapping index labels to city values."
                }
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_a"],
            "option_feedback": {
                "opt_a": {
                    "message": (
                        "Correct. `df['col']` returns a Series — the same one-dimensional, "
                        "indexed structure that a DataFrame is built from. It shares the DataFrame's index."
                    )
                },
                "opt_b": {
                    "message": (
                        "Not quite. `df['col']` uses dict-like syntax, but the result is a pandas Series, "
                        "not a plain Python list. A Series carries index labels alongside its values."
                    )
                },
                "opt_c": {
                    "message": (
                        "A single-column selection with `df['col']` returns a Series, not a DataFrame. "
                        "To get a one-column DataFrame you would use double brackets: `df[['col']]`."
                    )
                },
                "opt_d": {
                    "message": (
                        "A pandas Series is not a dict, even though a DataFrame can be thought of as a "
                        "dict of Series. `df['city']` returns a Series with an integer index, not a dict."
                    )
                }
            }
        },
        "feedback": {
            "correct": {
                "message": (
                    "Exactly right. A DataFrame is a collection of like-indexed Series objects, "
                    "so pulling out a column with `df['col']` gives you back one of those Series."
                )
            },
            "incorrect": {
                "message": (
                    "Remember: a DataFrame can be thought of as a dict of Series that share an index. "
                    "Selecting a column with `df['col']` returns one of those Series."
                )
            },
            "hints": [
                "Think about what a DataFrame is made of at its core.",
                "The teaching block said: 'A DataFrame can be treated like a dict of like-indexed Series.'"
            ],
            "remediation_step_id": f"{TILE}.s01"
        }
    }
}

# ---- s05: code_exercise — pandas.dataframe_series_model#practice -----------
# Practice anchor: Create a Series from a list and a DataFrame from a dict of lists,
# pull one column out, print its type.
# allowed_syntax: import pandas as pd, pd.Series(list), pd.DataFrame(dict_of_lists),
#                 df['col'], print(), type()
# blocked_syntax: pd.read_csv, df.head(), df.shape, df.info(), df.loc, df.iloc,
#                 boolean filtering
#
# Solution:
#   import pandas as pd
#   delivery_times = [18, 20, 22, 22, 26, 28, 80]
#   s = pd.Series(delivery_times)
#   print(s)
#   data = {'order_id': [1001, 1002, 1003], 'city': ['Lagos', 'Abuja', 'Kano'],
#           'delivery_time_minutes': [18, 20, 26]}
#   df = pd.DataFrame(data)
#   print(df)
#   col = df['city']
#   print(type(col))
#
# Tests:
#   value_equals: type(s).__name__ == 'Series'  -> True
#   dataframe_equals: df -> columns=[order_id, city, delivery_time_minutes], rows=...
#   value_equals: type(col).__name__ == 'Series' -> True

STARTER_S05 = """\
import pandas as pd

# A list of delivery times (minutes)
# delivery_times = [18, 20, 22, 22, 26, 28, 80]

# A dict of equal-length lists for an orders table
# data = {
#     'order_id': [1001, 1002, 1003],
#     'city': ['Lagos', 'Abuja', 'Kano'],
#     'delivery_time_minutes': [18, 20, 26]
# }

# TODO: build a Series from delivery_times and print it
# TODO: build a DataFrame from data and print it
# TODO: pull out the 'city' column, print its type
"""

SOLUTION_S05 = """\
import pandas as pd

delivery_times = [18, 20, 22, 22, 26, 28, 80]
s = pd.Series(delivery_times)
print(s)

data = {
    'order_id': [1001, 1002, 1003],
    'city': ['Lagos', 'Abuja', 'Kano'],
    'delivery_time_minutes': [18, 20, 26]
}
df = pd.DataFrame(data)
print(df)

col = df['city']
print(type(col))
"""

s05 = {
    "step_id": f"{TILE}.s05",
    "interaction": {
        "type": "code_exercise",
        "interaction_id": f"ix.{TILE}.s05",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": DFM,
                "capability": "construct_series_from_list_or_dict",
                "fact_ids": [fact(DFM, "f1"), fact(DFM, "f3")]
            },
            {
                "concept_id": DFM,
                "capability": "construct_dataframe_from_dict_of_lists",
                "fact_ids": [fact(DFM, "f2"), fact(DFM, "f4")]
            },
            {
                "concept_id": DFM,
                "capability": "relate_dataframe_columns_to_series",
                "fact_ids": [fact(DFM, "f1"), fact(DFM, "f2"), fact(DFM, "f5")]
            }
        ],
        "anchors": [
            anchor(DFM, "practice"),
            anchor(DFM, "assessment", "construct_series_from_list_or_dict"),
            anchor(DFM, "assessment", "construct_dataframe_from_dict_of_lists"),
            anchor(DFM, "assessment", "relate_dataframe_columns_to_series"),
        ],
        "public": {
            "prompt": (
                "Complete the script to:\n"
                "1. Build a pandas Series from `delivery_times = [18, 20, 22, 22, 26, 28, 80]` and print it.\n"
                "2. Build a DataFrame from the `data` dict (keys: `order_id`, `city`, `delivery_time_minutes`) and print it.\n"
                "3. Pull out the `'city'` column from the DataFrame and print its type.\n\n"
                "Use only `pd.Series(list)`, `pd.DataFrame(dict_of_lists)`, `df['col']`, `print()`, and `type()`."
            ),
            "runtime": {
                "kind": "python",
                "version": PY_VERSION,
                "packages": ["pandas"]
            },
            "workspace": {
                "files": [
                    {
                        "path": "starter.py",
                        "role": "editable",
                        "language": "python",
                        "content": STARTER_S05
                    }
                ],
                "entry": "starter.py"
            },
            "constraints": {
                "allowed_syntax": [
                    "import pandas as pd",
                    "pd.Series(list)",
                    "pd.DataFrame(dict_of_lists)",
                    "df['col']",
                    "print()",
                    "type()"
                ],
                "blocked_syntax": [
                    "pd.read_csv",
                    "df.head()",
                    "df.shape",
                    "df.info()",
                    "df.loc",
                    "df.iloc",
                    "boolean filtering"
                ]
            }
        },
        "grading": {
            "solution_files": [
                {
                    "path": "starter.py",
                    "content": SOLUTION_S05
                }
            ],
            "tests": [
                {
                    "test_id": f"ix.{TILE}.s05.t1",
                    "kind": "value_equals",
                    "spec": {
                        "expr": "type(s).__name__",
                        "expected": "Series"
                    },
                    "visible": True,
                    "message_on_fail": "Make sure you assign `pd.Series(delivery_times)` to a variable called `s`."
                },
                {
                    "test_id": f"ix.{TILE}.s05.t2",
                    "kind": "dataframe_equals",
                    "spec": {
                        "expr": "df",
                        "expected": {
                            "columns": ["order_id", "city", "delivery_time_minutes"],
                            "rows": [
                                [1001, "Lagos", 18],
                                [1002, "Abuja", 20],
                                [1003, "Kano", 26]
                            ]
                        },
                        "ordered": True
                    },
                    "visible": True,
                    "message_on_fail": (
                        "Make sure `df` is built with `pd.DataFrame(data)` where `data` has keys "
                        "`order_id`, `city`, and `delivery_time_minutes` with the given lists."
                    )
                },
                {
                    "test_id": f"ix.{TILE}.s05.t3",
                    "kind": "value_equals",
                    "spec": {
                        "expr": "type(col).__name__",
                        "expected": "Series"
                    },
                    "visible": True,
                    "message_on_fail": (
                        "Use `df['city']` to pull out the city column and assign it to `col`. "
                        "The result should be a pandas Series."
                    )
                }
            ]
        },
        "feedback": {
            "correct": {
                "message": (
                    "Well done! You built a Series from a list, a DataFrame from a dict of lists, "
                    "and confirmed that a column pulled from a DataFrame is itself a Series."
                )
            },
            "incorrect": {
                "message": (
                    "Check that you used `pd.Series(delivery_times)` for the Series, "
                    "`pd.DataFrame(data)` for the DataFrame, and `df['city']` to select the column."
                )
            },
            "hints": [
                "Start with `s = pd.Series(delivery_times)` — pass the list directly.",
                "For the DataFrame, pass the whole `data` dict to `pd.DataFrame()`."
            ],
            "remediation_step_id": f"{TILE}.s01"
        }
    }
}

# ---- s08: choice — choose_read_csv + choose_read_excel ---------------------
# Facts tested: f1 (read_csv for delimited text), f2 (read_excel for workbooks)
# Both taught in s06 (text block b1)
# Difficulty: intro (first check for reading_data concept)

s08 = {
    "step_id": f"{TILE}.s08",
    "interaction": {
        "type": "choice",
        "interaction_id": f"ix.{TILE}.s08",
        "difficulty": "intro",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": RD,
                "capability": "choose_read_csv_for_delimited_text",
                "fact_ids": [fact(RD, "f1")]
            },
            {
                "concept_id": RD,
                "capability": "choose_read_excel_for_workbooks",
                "fact_ids": [fact(RD, "f2")]
            }
        ],
        "anchors": [
            anchor(RD, "assessment", "choose_read_csv_for_delimited_text"),
            anchor(RD, "assessment", "choose_read_excel_for_workbooks"),
        ],
        "public": {
            "prompt": (
                "A colleague sends you two files: `deliveries.csv` (a comma-separated text file) "
                "and `deliveries.xlsx` (an Excel workbook). "
                "Which pandas functions do you use to load each file into a DataFrame?"
            ),
            "options": [
                {
                    "option_id": "opt_a",
                    "text": "`pd.read_csv()` for the CSV and `pd.read_excel()` for the Excel file."
                },
                {
                    "option_id": "opt_b",
                    "text": "`pd.read_excel()` for both, because Excel can also open CSV files."
                },
                {
                    "option_id": "opt_c",
                    "text": "`pd.read_csv()` for both, because CSV is the universal format."
                },
                {
                    "option_id": "opt_d",
                    "text": "`pd.read_table()` for the CSV and `pd.read_csv()` for the Excel file."
                }
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_a"],
            "option_feedback": {
                "opt_a": {
                    "message": (
                        "Correct. `pd.read_csv()` reads delimited text files like CSV, "
                        "and `pd.read_excel()` reads Excel workbooks (.xlsx)."
                    )
                },
                "opt_b": {
                    "message": (
                        "While Excel can open CSV files in the application, `pd.read_excel()` "
                        "expects a binary Excel workbook format. Use `pd.read_csv()` for `.csv` files."
                    )
                },
                "opt_c": {
                    "message": (
                        "`pd.read_csv()` reads delimited text files, not Excel workbooks. "
                        "Passing an `.xlsx` file to `pd.read_csv()` will raise an error."
                    )
                },
                "opt_d": {
                    "message": (
                        "`pd.read_table()` is not the main function taught here, and "
                        "`pd.read_csv()` does not read Excel workbooks. "
                        "Use `pd.read_csv()` for CSV and `pd.read_excel()` for `.xlsx`."
                    )
                }
            }
        },
        "feedback": {
            "correct": {
                "message": (
                    "Right. Each file format has its own reader: `read_csv` for delimited text, "
                    "`read_excel` for Excel workbooks."
                )
            },
            "incorrect": {
                "message": (
                    "Each file format needs its own reader. `pd.read_csv()` is for delimited text files "
                    "like `.csv`; `pd.read_excel()` is for Excel workbooks like `.xlsx`."
                )
            },
            "hints": [
                "The function name matches the file type: `read_csv` for CSV, `read_excel` for Excel.",
                "Think about what each function name describes."
            ],
            "remediation_step_id": f"{TILE}.s06"
        }
    }
}

# ---- s09: choice — set_path_sheet_name_and_sep_arguments -------------------
# Facts tested: f3 (path arg + sheet_name), f4 (sep argument)
# Both taught in s06 (text blocks b2 and b3)
# Difficulty: core

s09 = {
    "step_id": f"{TILE}.s09",
    "interaction": {
        "type": "choice",
        "interaction_id": f"ix.{TILE}.s09",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": RD,
                "capability": "set_path_sheet_name_and_sep_arguments",
                "fact_ids": [fact(RD, "f3"), fact(RD, "f4")]
            }
        ],
        "anchors": [anchor(RD, "assessment", "set_path_sheet_name_and_sep_arguments")],
        "public": {
            "prompt": (
                "A delivery export file uses a semicolon (`;`) as its delimiter instead of a comma. "
                "Which call correctly reads it into a DataFrame?"
            ),
            "options": [
                {
                    "option_id": "opt_a",
                    "text": '`pd.read_csv("deliveries.csv", sep=";")`'
                },
                {
                    "option_id": "opt_b",
                    "text": '`pd.read_csv("deliveries.csv", delimiter=",")`'
                },
                {
                    "option_id": "opt_c",
                    "text": '`pd.read_excel("deliveries.csv", sheet_name="Sheet1")`'
                },
                {
                    "option_id": "opt_d",
                    "text": '`pd.read_csv("deliveries.csv")`'
                }
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_a"],
            "option_feedback": {
                "opt_a": {
                    "message": (
                        "Correct. `sep=\";\"` tells `read_csv()` to split fields on semicolons "
                        "instead of the default comma."
                    )
                },
                "opt_b": {
                    "message": (
                        "The argument name is `sep`, not `delimiter` (though `delimiter` is an alias, "
                        "the value here is wrong: passing `\",\"` keeps the default comma separator, "
                        "which won't parse a semicolon-delimited file correctly)."
                    )
                },
                "opt_c": {
                    "message": (
                        "`pd.read_excel()` reads Excel workbooks, not CSV files. "
                        "The `sheet_name` argument is for Excel sheets, not CSV files."
                    )
                },
                "opt_d": {
                    "message": (
                        "Without `sep=\";\"`, `read_csv()` uses the default comma separator. "
                        "A semicolon-delimited file would be read as a single column."
                    )
                }
            }
        },
        "feedback": {
            "correct": {
                "message": (
                    "Exactly. `sep` lets you override the default comma delimiter. "
                    "The file path is always the first argument."
                )
            },
            "incorrect": {
                "message": (
                    "When the delimiter is not a comma, pass `sep=\";\"` (or whatever character is used) "
                    "as a keyword argument to `pd.read_csv()`."
                )
            },
            "hints": [
                "The default separator for `read_csv` is a comma. What argument changes it?",
                "Look at the `sep` parameter of `pd.read_csv()`."
            ],
            "remediation_step_id": f"{TILE}.s06"
        }
    }
}

# ---- s10: code_exercise — pandas.reading_data#practice ---------------------
# Practice anchor: Load a provided small CSV file into a DataFrame and print it.
# allowed_syntax: import pandas as pd, pd.read_csv(path), pd.read_csv(path, sep=...),
#                 pd.read_excel(path, sheet_name=...), print(df)
# blocked_syntax: df.shape, df.head(), df.info(), df.describe(), df.dtypes
#
# Mount: ds_orders -> orders.csv
# Solution: orders = pd.read_csv('orders.csv'); print(orders)
# Test: dataframe_equals on orders variable

STARTER_S10 = """\
import pandas as pd

# The orders CSV is available at: 'orders.csv'
# orders = pd.read_csv('orders.csv')

# TODO: read orders.csv into a DataFrame called orders
# TODO: print the DataFrame
"""

SOLUTION_S10 = """\
import pandas as pd

orders = pd.read_csv('orders.csv')
print(orders)
"""

# Expected rows from ds_orders (14 rows)
ORDERS_ROWS = [
    [1001, "Lagos", "LOS", "Ada", 201, 301, "2024-03-14", 18, 4.2, 2500],
    [1002, "Abuja", "ABJ", "Bayo", 202, 302, "2024-03-14", 20, 6.1, 3100],
    [1003, "Kano", "KAN", "Chidi", 203, 303, "2024-03-15", 22, 5.5, 1800],
    [1004, "Lagos", "LOS", "Ada", 201, 304, "2024-03-15", 22, 3.8, 2200],
    [1005, "Abuja", "ABJ", "Bayo", 202, 305, "2024-03-16", 26, 7.3, 4000],
    [1006, "Kano", "KAN", "Chidi", 203, 306, "2024-03-16", 28, 8.0, 1500],
    [1007, "Lagos", "LOS", "Ada", 201, 307, "2024-03-17", 80, 12.4, 5500],
    [1008, "Abuja", "ABJ", "Bayo", 202, 308, "2024-03-17", 31, 9.2, 3800],
    [1009, "Kano", "KAN", "Chidi", 203, 309, "2024-03-18", 19, 4.9, 2100],
    [1010, "Lagos", "LOS", "Ada", 201, 310, "2024-03-18", 24, 5.1, 2900],
    [1011, "Abuja", "ABJ", "Bayo", 202, 311, "2024-03-19", 33, 10.0, 4200],
    [1012, "Kano", "KAN", "Chidi", 203, 312, "2024-03-19", 21, 4.4, 1700],
    [1013, "Lagos", "LOS", "Ada", 201, 313, "2024-03-20", 27, 6.6, 3300],
    [1014, "Abuja", "ABJ", "Bayo", 202, 314, "2024-03-20", 35, 11.1, 4600],
]

ORDERS_COLS = [
    "order_id", "city", "city_code", "courier", "driver_id", "customer_id",
    "pickup_date", "delivery_time_minutes", "distance_km", "order_value"
]

s10 = {
    "step_id": f"{TILE}.s10",
    "interaction": {
        "type": "code_exercise",
        "interaction_id": f"ix.{TILE}.s10",
        "difficulty": "intro",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": RD,
                "capability": "choose_read_csv_for_delimited_text",
                "fact_ids": [fact(RD, "f1")]
            },
            {
                "concept_id": RD,
                "capability": "set_path_sheet_name_and_sep_arguments",
                "fact_ids": [fact(RD, "f3")]
            }
        ],
        "anchors": [anchor(RD, "practice")],
        "public": {
            "prompt": (
                "The file `orders.csv` contains SwiftDrop delivery records. "
                "Read it into a DataFrame called `orders` using `pd.read_csv()`, then print the DataFrame.\n\n"
                "After running your code, the output should show all 10 columns "
                "(`order_id`, `city`, `city_code`, `courier`, `driver_id`, `customer_id`, "
                "`pickup_date`, `delivery_time_minutes`, `distance_km`, `order_value`) "
                "and all 14 rows."
            ),
            "runtime": {
                "kind": "python",
                "version": PY_VERSION,
                "packages": ["pandas"]
            },
            "workspace": {
                "files": [
                    {
                        "path": "starter.py",
                        "role": "editable",
                        "language": "python",
                        "content": STARTER_S10
                    }
                ],
                "entry": "starter.py",
                "asset_mounts": [
                    {
                        "asset_id": "ds_orders",
                        "variant_id": None,
                        "mount_path": "orders.csv"
                    }
                ]
            },
            "constraints": {
                "allowed_syntax": [
                    "import pandas as pd",
                    "pd.read_csv(path)",
                    "pd.read_csv(path, sep=...)",
                    "pd.read_excel(path, sheet_name=...)",
                    "print(df)"
                ],
                "blocked_syntax": [
                    "df.shape",
                    "df.head()",
                    "df.info()",
                    "df.describe()",
                    "df.dtypes"
                ]
            }
        },
        "grading": {
            "solution_files": [
                {
                    "path": "starter.py",
                    "content": SOLUTION_S10
                }
            ],
            "tests": [
                {
                    "test_id": f"ix.{TILE}.s10.t1",
                    "kind": "dataframe_equals",
                    "spec": {
                        "expr": "orders",
                        "expected": {
                            "columns": ORDERS_COLS,
                            "rows": ORDERS_ROWS
                        },
                        "ordered": True
                    },
                    "visible": True,
                    "message_on_fail": (
                        "Make sure you read `orders.csv` with `pd.read_csv('orders.csv')` "
                        "and assign the result to a variable called `orders`."
                    )
                }
            ]
        },
        "feedback": {
            "correct": {
                "message": (
                    "Great work! You loaded the CSV into a DataFrame with all 10 columns and 14 rows. "
                    "That's the first step in every pandas workflow."
                )
            },
            "incorrect": {
                "message": (
                    "Use `orders = pd.read_csv('orders.csv')` to load the file. "
                    "Make sure the variable is named `orders` and you print it."
                )
            },
            "hints": [
                "The file path is the first argument: `pd.read_csv('orders.csv')`.",
                "Assign the result to `orders`, then call `print(orders)`."
            ],
            "remediation_step_id": f"{TILE}.s06"
        }
    }
}

# ---- assemble ---------------------------------------------------------------

output = {
    "schema_version": "0.1.0",
    "kind": "interactions_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_009_da_pandas",
    "tiles": [
        {
            "tile_id": TILE,
            "interactions": [s04, s05, s08, s09, s10]
        }
    ]
}

out_path = "batches/final_batch_009_da_pandas/interactions.part.c0_canary.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"Written: {out_path}")
print(f"Interactions: {len(output['tiles'][0]['interactions'])}")
for ix in output['tiles'][0]['interactions']:
    print(f"  {ix['step_id']} -> {ix['interaction']['type']}")
