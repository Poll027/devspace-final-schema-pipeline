#!/usr/bin/env python3
"""Rebuild interactions for chunk c2 with fixes"""
import json
import pandas as pd

# Load inputs
with open('tile_plans.json') as f:
    plans = {t['tile_id']: t for t in json.load(f)['tiles']}

with open('scenario_asset_registry.json') as f:
    registry = json.load(f)

with open('inputs/path_glossary_bundle.json') as f:
    glossary = json.load(f)
    bundles = {b['context']['concept_id']: b for b in glossary['bundles']}

with open('screens.json') as f:
    screens_data = json.load(f)
    screens = {t['tile_id']: t for t in screens_data['tiles']}

# Helper to get remediation_step_id
def get_remediation_step_id(tile_id, concept_id):
    tile_screens = screens.get(tile_id, {})
    for rs in tile_screens.get('remediation_steps', []):
        if concept_id in rs.get('concept_ids', []):
            return rs['step_id']
    return None

# Compute expected values from data
orders_asset = next(a for a in registry['assets'] if a['asset_id'] == 'ds_orders')
cols = [c['name'] for c in orders_asset['columns']]
rows = orders_asset['rows']
df_orders = pd.DataFrame(rows, columns=cols)

# Descriptive stats on full dataset
dt_col = df_orders['delivery_time_minutes']
dt_mean = dt_col.mean()
dt_median = dt_col.median()
dt_std = dt_col.std()

# Build interactions
interactions = {
    "schema_version": "0.1.0",
    "kind": "interactions_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_009_da_pandas",
    "tiles": []
}

# ========== tile_pandas_dtype_datetime ==========
tile_id = "tile_pandas_dtype_datetime"
plan = plans[tile_id]
tile_interactions = {"tile_id": tile_id, "interactions": []}

# s03: check - convert_multiple_columns_with_dict
step = next(s for s in plan['steps'] if s['step_id'] == f'{tile_id}.s03')
tile_interactions['interactions'].append({
    "step_id": step['step_id'],
    "interaction": {
        "type": "choice",
        "interaction_id": f"ix.{step['step_id']}",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [{
            "concept_id": "pandas.dtype_conversion",
            "capability": "convert_multiple_columns_with_dict",
            "fact_ids": ["f2"]
        }],
        "anchors": ["pandas.dtype_conversion#assessment:convert_multiple_columns_with_dict"],
        "public": {
            "prompt": "You have a DataFrame `orders` where `distance_km` is stored as a string and `order_id` is an integer. You want to convert `distance_km` to float and `order_id` to string in one call. Which approach is correct?",
            "options": [
                {"option_id": "opt_a", "text": "`orders = orders.astype({'distance_km': float, 'order_id': str})`"},
                {"option_id": "opt_b", "text": "`orders.astype(float, str)`"},
                {"option_id": "opt_c", "text": "`orders['distance_km'].astype(float); orders['order_id'].astype(str)`"},
                {"option_id": "opt_d", "text": "`orders.convert({'distance_km': float, 'order_id': str})`"}
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_a"],
            "option_feedback": {
                "opt_a": {"message": "Correct. `astype()` accepts a dict mapping column names to target dtypes, converting multiple columns in one call."},
                "opt_b": {"message": "Not quite. `astype()` does not accept positional arguments for multiple columns. Pass a dict mapping column names to dtypes: `astype({'col1': dtype1, 'col2': dtype2})`."},
                "opt_c": {"message": "This works but requires two separate calls. `astype()` with a dict converts multiple columns in one call: `orders.astype({'distance_km': float, 'order_id': str})`."},
                "opt_d": {"message": "There is no `convert()` method. Use `astype()` with a dict: `orders.astype({'distance_km': float, 'order_id': str})`."}
            }
        },
        "feedback": {
            "correct": {"message": "Exactly right. A dict lets you convert several columns to different types in one `astype()` call."},
            "incorrect": {"message": "Not quite. Review how `astype()` accepts a dict mapping column names to target dtypes."},
            "hints": ["Think about how you pass multiple column-dtype pairs to `astype()` at once."],
            "remediation_step_id": get_remediation_step_id(tile_id, "pandas.dtype_conversion")
        }
    }
})

# s04: hands_on - dtype_conversion practice
# The practice anchor says: "dtypes shows the column as a numeric type after conversion, and a numeric operation on the column now works"
# But allowed_syntax doesn't include numeric operations like .sum() or .mean()
# So the solution just prints dtypes before and after
step = next(s for s in plan['steps'] if s['step_id'] == f'{tile_id}.s04')
tile_interactions['interactions'].append({
    "step_id": step['step_id'],
    "interaction": {
        "type": "code_exercise",
        "interaction_id": f"ix.{step['step_id']}",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [{
            "concept_id": "pandas.dtype_conversion",
            "capability": "convert_column_dtype_with_astype",
            "fact_ids": ["f1"]
        }],
        "anchors": [
            "pandas.dtype_conversion#practice",
            "pandas.dtype_conversion#assessment:convert_column_dtype_with_astype"
        ],
        "public": {
            "prompt": "The `orders` DataFrame has a `distance_km` column loaded as strings (all values are numeric). Convert `distance_km` to float using `astype()`, then print the dtypes to verify the conversion.\n\nUse only `df['col'].astype(float)`, `df['col'] = ...`, `df.dtypes`, and `print()`.",
            "runtime": {"kind": "python", "version": "0.29.5", "packages": ["pandas"]},
            "workspace": {
                "files": [{
                    "path": "solution.py",
                    "role": "editable",
                    "language": "python",
                    "content": "import pandas as pd\n\n# Load orders with distance_km as strings\norders = pd.read_csv('orders.csv', dtype={'distance_km': str})\n\n# TODO: Convert distance_km to float\n\n# TODO: Print dtypes to verify\n"
                }],
                "entry": "solution.py",
                "asset_mounts": [{
                    "asset_id": "ds_orders",
                    "variant_id": None,
                    "mount_path": "orders.csv"
                }]
            },
            "constraints": {
                "allowed_syntax": ["df['col'].astype(float)", "df['col'] = ...", "df.astype({...})", "df.dtypes", "print()"],
                "blocked_syntax": ["pd.to_datetime", "df['col'].str", "df.drop_duplicates", "df.fillna"]
            }
        },
        "grading": {
            "solution_files": [{
                "path": "solution.py",
                "content": "import pandas as pd\n\n# Load orders with distance_km as strings\norders = pd.read_csv('orders.csv', dtype={'distance_km': str})\n\n# Convert distance_km to float\norders['distance_km'] = orders['distance_km'].astype(float)\n\n# Print dtypes to verify\nprint(orders.dtypes)\n"
            }],
            "tests": [{
                "test_id": "t1",
                "kind": "value_equals",
                "spec": {
                    "expr": "str(orders['distance_km'].dtype)",
                    "expected": "float64"
                },
                "visible": True,
                "message_on_fail": "The distance_km dtype should be float64 after conversion. Check that you used astype(float)."
            }]
        },
        "feedback": {
            "correct": {"message": "Perfect! You converted the string column to float."},
            "incorrect": {"message": "Not quite. Make sure you use `astype(float)` to convert distance_km."},
            "hints": ["Use `orders['distance_km'] = orders['distance_km'].astype(float)` to convert the column."],
            "remediation_step_id": get_remediation_step_id(tile_id, "pandas.dtype_conversion")
        }
    }
})

# s07: check - extract_date_components_with_dt
step = next(s for s in plan['steps'] if s['step_id'] == f'{tile_id}.s07')
tile_interactions['interactions'].append({
    "step_id": step['step_id'],
    "interaction": {
        "type": "choice",
        "interaction_id": f"ix.{step['step_id']}",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [{
            "concept_id": "pandas.datetime_handling",
            "capability": "extract_date_components_with_dt",
            "fact_ids": ["f2"]
        }],
        "anchors": ["pandas.datetime_handling#assessment:extract_date_components_with_dt"],
        "public": {
            "prompt": "You have converted a column `pickup_date` to datetime. How do you extract just the month number from every date into a new column `pickup_month`?",
            "options": [
                {"option_id": "opt_a", "text": "`orders['pickup_month'] = orders['pickup_date'].dt.month`"},
                {"option_id": "opt_b", "text": "`orders['pickup_month'] = orders['pickup_date'].month`"},
                {"option_id": "opt_c", "text": "`orders['pickup_month'] = orders['pickup_date'].extract('month')`"},
                {"option_id": "opt_d", "text": "`orders['pickup_month'] = orders['pickup_date'].str.month`"}
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_a"],
            "option_feedback": {
                "opt_a": {"message": "Correct. The `.dt` accessor exposes date/time component properties like `month`, `year`, and `day` for every value in a datetime Series."},
                "opt_b": {"message": "Not quite. A datetime Series does not have a direct `.month` attribute. You must use the `.dt` accessor: `orders['pickup_date'].dt.month`."},
                "opt_c": {"message": "There is no `.extract()` method for datetime Series. Use the `.dt` accessor: `orders['pickup_date'].dt.month`."},
                "opt_d": {"message": "The `.str` accessor is for text columns, not datetime. Use `.dt` for datetime columns: `orders['pickup_date'].dt.month`."}
            }
        },
        "feedback": {
            "correct": {"message": "Exactly. The `.dt` accessor is the key to pulling date/time components from a datetime column."},
            "incorrect": {"message": "Not quite. Review how the `.dt` accessor exposes date/time component properties."},
            "hints": ["Think about which accessor exposes date/time properties like `month`, `year`, and `day`."],
            "remediation_step_id": get_remediation_step_id(tile_id, "pandas.datetime_handling")
        }
    }
})

# s08: hands_on - datetime_handling practice
# The allowed_syntax doesn't include .head(), so we print the full column
step = next(s for s in plan['steps'] if s['step_id'] == f'{tile_id}.s08')
tile_interactions['interactions'].append({
    "step_id": step['step_id'],
    "interaction": {
        "type": "code_exercise",
        "interaction_id": f"ix.{step['step_id']}",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "pandas.datetime_handling",
                "capability": "convert_text_column_with_to_datetime",
                "fact_ids": ["f1"]
            },
            {
                "concept_id": "pandas.datetime_handling",
                "capability": "extract_date_components_with_dt",
                "fact_ids": ["f2"]
            }
        ],
        "anchors": [
            "pandas.datetime_handling#practice",
            "pandas.datetime_handling#assessment:convert_text_column_with_to_datetime",
            "pandas.datetime_handling#assessment:extract_date_components_with_dt"
        ],
        "public": {
            "prompt": "The `orders` DataFrame has a `pickup_date` column of ISO date strings. Convert `pickup_date` to datetime using `pd.to_datetime()`, then create a new column `pickup_month` holding just the month number. Print the `pickup_month` column.\n\nUse only `pd.to_datetime()`, `df['col'].dt.month`, `df['col'] = ...`, `df.dtypes`, and `print()`.",
            "runtime": {"kind": "python", "version": "0.29.5", "packages": ["pandas"]},
            "workspace": {
                "files": [{
                    "path": "solution.py",
                    "role": "editable",
                    "language": "python",
                    "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\n# TODO: Convert pickup_date to datetime\n\n# TODO: Extract month into pickup_month\n\n# TODO: Print pickup_month column\n"
                }],
                "entry": "solution.py",
                "asset_mounts": [{
                    "asset_id": "ds_orders",
                    "variant_id": None,
                    "mount_path": "orders.csv"
                }]
            },
            "constraints": {
                "allowed_syntax": ["pd.to_datetime(df['col'])", "df['col'].dt.month", "df['new'] = ...", "df.dtypes", "print()"],
                "blocked_syntax": ["df.groupby", "df.resample", "df['col'].str", "df.merge"]
            }
        },
        "grading": {
            "solution_files": [{
                "path": "solution.py",
                "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\n# Convert pickup_date to datetime\norders['pickup_date'] = pd.to_datetime(orders['pickup_date'])\n\n# Extract month into pickup_month\norders['pickup_month'] = orders['pickup_date'].dt.month\n\n# Print pickup_month column\nprint(orders['pickup_month'])\n"
            }],
            "tests": [{
                "test_id": "t1",
                "kind": "value_equals",
                "spec": {
                    "expr": "orders['pickup_month'].tolist()",
                    "expected": [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
                },
                "visible": True,
                "message_on_fail": "The pickup_month values should all be 3 (March). Check that you converted pickup_date to datetime and extracted the month."
            }]
        },
        "feedback": {
            "correct": {"message": "Excellent! You converted the text dates to datetime and extracted the month component."},
            "incorrect": {"message": "Not quite. Make sure you use `pd.to_datetime()` to convert the column, then `.dt.month` to extract the month."},
            "hints": ["First convert with `pd.to_datetime(orders['pickup_date'])`, then extract with `.dt.month`."],
            "remediation_step_id": get_remediation_step_id(tile_id, "pandas.datetime_handling")
        }
    }
})

interactions['tiles'].append(tile_interactions)

# ========== tile_pandas_text_dupes_missing ==========
tile_id = "tile_pandas_text_dupes_missing"
plan = plans[tile_id]
tile_interactions = {"tile_id": tile_id, "interactions": []}

# s03: check - apply_string_methods_across_column
step = next(s for s in plan['steps'] if s['step_id'] == f'{tile_id}.s03')
tile_interactions['interactions'].append({
    "step_id": step['step_id'],
    "interaction": {
        "type": "choice",
        "interaction_id": f"ix.{step['step_id']}",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [{
            "concept_id": "pandas.str_accessor_cleaning",
            "capability": "apply_string_methods_across_column",
            "fact_ids": ["f1"]
        }],
        "anchors": ["pandas.str_accessor_cleaning#assessment:apply_string_methods_across_column"],
        "public": {
            "prompt": "You have a `city` column with mixed case and stray spaces: `[' Lagos', 'ABUJA ', 'Kano']`. Which code cleans every value to lowercase with no leading or trailing spaces?",
            "options": [
                {"option_id": "opt_a", "text": "`orders['city'] = orders['city'].str.strip().str.lower()`"},
                {"option_id": "opt_b", "text": "`orders['city'] = orders['city'].strip().lower()`"},
                {"option_id": "opt_c", "text": "`orders['city'] = orders['city'].apply(lambda x: x.strip().lower())`"},
                {"option_id": "opt_d", "text": "`orders['city'] = orders['city'].str.clean()`"}
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_a"],
            "option_feedback": {
                "opt_a": {"message": "Correct. The `.str` accessor applies string methods like `strip()` and `lower()` to every element of the Series at once."},
                "opt_b": {"message": "Not quite. `.strip()` and `.lower()` are string methods that work on a single string, not a Series. Use the `.str` accessor to apply them to every element: `orders['city'].str.strip().str.lower()`."},
                "opt_c": {"message": "This works but is more verbose. The `.str` accessor provides a cleaner way: `orders['city'].str.strip().str.lower()` applies the methods to every element without an explicit lambda."},
                "opt_d": {"message": "There is no `.str.clean()` method. Use `.str.strip()` to remove whitespace and `.str.lower()` to convert to lowercase."}
            }
        },
        "feedback": {
            "correct": {"message": "Exactly. The `.str` accessor lets you chain string methods to clean every value in a column."},
            "incorrect": {"message": "Not quite. Review how the `.str` accessor applies string methods across a column."},
            "hints": ["Think about which accessor lets you call string methods like `strip()` and `lower()` on every element of a Series."],
            "remediation_step_id": get_remediation_step_id(tile_id, "pandas.str_accessor_cleaning")
        }
    }
})

# s04: hands_on - str_accessor_cleaning practice
# The allowed_syntax doesn't include .unique(), so we print the full column
step = next(s for s in plan['steps'] if s['step_id'] == f'{tile_id}.s04')
tile_interactions['interactions'].append({
    "step_id": step['step_id'],
    "interaction": {
        "type": "code_exercise",
        "interaction_id": f"ix.{step['step_id']}",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [{
            "concept_id": "pandas.str_accessor_cleaning",
            "capability": "apply_string_methods_across_column",
            "fact_ids": ["f1"]
        }],
        "anchors": ["pandas.str_accessor_cleaning#practice"],
        "public": {
            "prompt": "The `orders_messy` DataFrame has a `city` column with mixed case and stray spaces. Clean the `city` column by stripping whitespace and converting to lowercase using the `.str` accessor. Print the cleaned `city` column.\n\nUse only `df['col'].str.strip()`, `df['col'].str.lower()`, `df['col'] = ...`, and `print()`.",
            "runtime": {"kind": "python", "version": "0.29.5", "packages": ["pandas"]},
            "workspace": {
                "files": [{
                    "path": "solution.py",
                    "role": "editable",
                    "language": "python",
                    "content": "import pandas as pd\n\norders_messy = pd.read_csv('orders_messy.csv')\n\n# TODO: Clean city column with .str.strip().str.lower()\n\n# TODO: Print city column\n"
                }],
                "entry": "solution.py",
                "asset_mounts": [{
                    "asset_id": "ds_orders",
                    "variant_id": "orders_messy",
                    "mount_path": "orders_messy.csv"
                }]
            },
            "constraints": {
                "allowed_syntax": ["df['col'].str.lower()", "df['col'].str.strip()", "df['col'].str.replace(a, b)", "df['col'] = ...", "print()"],
                "blocked_syntax": ["df['col'].map", "df['col'].apply", "for loops over rows", "regex patterns"]
            }
        },
        "grading": {
            "solution_files": [{
                "path": "solution.py",
                "content": "import pandas as pd\n\norders_messy = pd.read_csv('orders_messy.csv')\n\n# Clean city column with .str.strip().str.lower()\norders_messy['city'] = orders_messy['city'].str.strip().str.lower()\n\n# Print city column\nprint(orders_messy['city'])\n"
            }],
            "tests": [{
                "test_id": "t1",
                "kind": "value_equals",
                "spec": {
                    "expr": "orders_messy['city'].tolist()",
                    "expected": ['lagos', 'abuja', 'kano', 'kano', 'lagos', 'abuja', 'kano', 'lagos', 'abuja', 'kano', 'lagos', 'abuja', 'kano', 'lagos', 'kano']
                },
                "visible": True,
                "message_on_fail": "The city values should all be lowercase with no spaces. Check that you used .str.strip().str.lower()."
            }]
        },
        "feedback": {
            "correct": {"message": "Perfect! You cleaned the text column using vectorized string methods."},
            "incorrect": {"message": "Not quite. Make sure you use `.str.strip().str.lower()` to clean the city column."},
            "hints": ["Chain the methods: `orders_messy['city'].str.strip().str.lower()`."],
            "remediation_step_id": get_remediation_step_id(tile_id, "pandas.str_accessor_cleaning")
        }
    }
})

# s06: check - identify_duplicates_with_subset
step = next(s for s in plan['steps'] if s['step_id'] == f'{tile_id}.s06')
tile_interactions['interactions'].append({
    "step_id": step['step_id'],
    "interaction": {
        "type": "choice",
        "interaction_id": f"ix.{step['step_id']}",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [{
            "concept_id": "pandas.drop_duplicates",
            "capability": "identify_duplicates_with_subset",
            "fact_ids": ["f1"]
        }],
        "anchors": ["pandas.drop_duplicates#assessment:identify_duplicates_with_subset"],
        "public": {
            "prompt": "You have an `orders` DataFrame where some `order_id` values appear more than once. How do you identify which rows are duplicates based on `order_id`?",
            "options": [
                {"option_id": "opt_a", "text": "`orders.duplicated(subset=['order_id'])`"},
                {"option_id": "opt_b", "text": "`orders.duplicated('order_id')`"},
                {"option_id": "opt_c", "text": "`orders['order_id'].duplicated()`"},
                {"option_id": "opt_d", "text": "`orders.is_duplicate(subset=['order_id'])`"}
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_a"],
            "option_feedback": {
                "opt_a": {"message": "Correct. `duplicated(subset=['order_id'])` returns a boolean Series indicating which rows are duplicates based on the `order_id` column."},
                "opt_b": {"message": "Not quite. `duplicated()` requires `subset` as a keyword argument with a list: `duplicated(subset=['order_id'])`."},
                "opt_c": {"message": "This checks for duplicate values within the `order_id` column itself, not duplicate rows based on `order_id`. Use `orders.duplicated(subset=['order_id'])` to check for duplicate rows."},
                "opt_d": {"message": "There is no `is_duplicate()` method. Use `duplicated(subset=['order_id'])` to identify duplicate rows."}
            }
        },
        "feedback": {
            "correct": {"message": "Exactly. The `subset` parameter tells `duplicated()` which columns to use when identifying duplicates."},
            "incorrect": {"message": "Not quite. Review how `duplicated()` uses the `subset` parameter to identify duplicate rows."},
            "hints": ["Think about which parameter specifies the columns to check for duplicates."],
            "remediation_step_id": get_remediation_step_id(tile_id, "pandas.drop_duplicates")
        }
    }
})

# s07: hands_on - drop_duplicates practice
# The allowed_syntax doesn't include .shape, so we use value_equals to check the shape
step = next(s for s in plan['steps'] if s['step_id'] == f'{tile_id}.s07')
tile_interactions['interactions'].append({
    "step_id": step['step_id'],
    "interaction": {
        "type": "code_exercise",
        "interaction_id": f"ix.{step['step_id']}",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [{
            "concept_id": "pandas.drop_duplicates",
            "capability": "choose_which_occurrence_to_keep",
            "fact_ids": ["f2"]
        }],
        "anchors": [
            "pandas.drop_duplicates#practice",
            "pandas.drop_duplicates#assessment:choose_which_occurrence_to_keep"
        ],
        "public": {
            "prompt": "The `orders_messy` DataFrame has duplicate `order_id` values. Remove the duplicates based on `order_id`, keeping the first occurrence. Print the cleaned DataFrame.\n\nUse only `df.drop_duplicates(subset=[...])`, `keep='first'`, and `print()`.",
            "runtime": {"kind": "python", "version": "0.29.5", "packages": ["pandas"]},
            "workspace": {
                "files": [{
                    "path": "solution.py",
                    "role": "editable",
                    "language": "python",
                    "content": "import pandas as pd\n\norders_messy = pd.read_csv('orders_messy.csv')\n\n# TODO: Remove duplicates based on order_id, keeping first\n\n# TODO: Print the cleaned DataFrame\n"
                }],
                "entry": "solution.py",
                "asset_mounts": [{
                    "asset_id": "ds_orders",
                    "variant_id": "orders_messy",
                    "mount_path": "orders_messy.csv"
                }]
            },
            "constraints": {
                "allowed_syntax": ["df.duplicated(subset=[...])", "df.drop_duplicates(subset=[...])", "keep='first'", "keep='last'", "keep=False", "print()"],
                "blocked_syntax": ["df.groupby", "df.merge", "df.sort_values then drop", "df.fillna"]
            }
        },
        "grading": {
            "solution_files": [{
                "path": "solution.py",
                "content": "import pandas as pd\n\norders_messy = pd.read_csv('orders_messy.csv')\n\n# Remove duplicates based on order_id, keeping first\norders_messy = orders_messy.drop_duplicates(subset=['order_id'], keep='first')\n\n# Print the cleaned DataFrame\nprint(orders_messy)\n"
            }],
            "tests": [{
                "test_id": "t1",
                "kind": "value_equals",
                "spec": {
                    "expr": "len(orders_messy)",
                    "expected": 14
                },
                "visible": True,
                "message_on_fail": "The cleaned DataFrame should have 14 rows (one duplicate removed). Check that you used drop_duplicates with subset=['order_id'] and keep='first'."
            }]
        },
        "feedback": {
            "correct": {"message": "Excellent! You removed duplicate rows while keeping the first occurrence of each order_id."},
            "incorrect": {"message": "Not quite. Make sure you use `drop_duplicates(subset=['order_id'], keep='first')`."},
            "hints": ["Use `orders_messy.drop_duplicates(subset=['order_id'], keep='first')` to keep the first occurrence."],
            "remediation_step_id": get_remediation_step_id(tile_id, "pandas.drop_duplicates")
        }
    }
})

# s10: check - choose_drop_or_fill
step = next(s for s in plan['steps'] if s['step_id'] == f'{tile_id}.s10')
tile_interactions['interactions'].append({
    "step_id": step['step_id'],
    "interaction": {
        "type": "choice",
        "interaction_id": f"ix.{step['step_id']}",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [{
            "concept_id": "pandas.missing_data_handling",
            "capability": "choose_drop_or_fill",
            "fact_ids": ["f2", "f3"]
        }],
        "anchors": ["pandas.missing_data_handling#assessment:choose_drop_or_fill"],
        "public": {
            "prompt": "You have a DataFrame where a few rows are missing values in a numeric `delivery_time_minutes` column. You want to keep all rows but replace the missing values with a typical value. Which approach is best?",
            "options": [
                {"option_id": "opt_a", "text": "`df['delivery_time_minutes'].fillna(df['delivery_time_minutes'].median())`"},
                {"option_id": "opt_b", "text": "`df.dropna(subset=['delivery_time_minutes'])`"},
                {"option_id": "opt_c", "text": "`df['delivery_time_minutes'].fillna(0)`"},
                {"option_id": "opt_d", "text": "`df['delivery_time_minutes'].isna()`"}
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_a"],
            "option_feedback": {
                "opt_a": {"message": "Correct. `fillna()` with the median replaces missing values with a typical value from the column, preserving all rows."},
                "opt_b": {"message": "Not quite. `dropna()` removes rows with missing values, but the question asks to keep all rows. Use `fillna()` to replace missing values instead."},
                "opt_c": {"message": "Filling with 0 keeps all rows, but 0 is not a typical delivery time. Use the median to fill with a representative value: `fillna(df['delivery_time_minutes'].median())`."},
                "opt_d": {"message": "`isna()` detects missing values but does not replace them. Use `fillna()` to replace missing values with a typical value like the median."}
            }
        },
        "feedback": {
            "correct": {"message": "Exactly. Filling with the median preserves all rows and uses a representative value."},
            "incorrect": {"message": "Not quite. Review when to use `dropna()` versus `fillna()` and what value to fill with."},
            "hints": ["Think about which method replaces missing values without removing rows, and what value is representative of the column."],
            "remediation_step_id": get_remediation_step_id(tile_id, "pandas.missing_data_handling")
        }
    }
})

# s11: hands_on - missing_data_handling practice
# The allowed_syntax doesn't include .sum(), so we use value_equals to check the count
step = next(s for s in plan['steps'] if s['step_id'] == f'{tile_id}.s11')
tile_interactions['interactions'].append({
    "step_id": step['step_id'],
    "interaction": {
        "type": "code_exercise",
        "interaction_id": f"ix.{step['step_id']}",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "pandas.missing_data_handling",
                "capability": "detect_missing_values",
                "fact_ids": ["f1"]
            },
            {
                "concept_id": "pandas.missing_data_handling",
                "capability": "drop_rows_missing_required_field",
                "fact_ids": ["f2"]
            },
            {
                "concept_id": "pandas.missing_data_handling",
                "capability": "fill_missing_values_with_value_or_median",
                "fact_ids": ["f3"]
            },
            {
                "concept_id": "pandas.missing_data_handling",
                "capability": "choose_drop_or_fill",
                "fact_ids": ["f2", "f3"]
            }
        ],
        "anchors": [
            "pandas.missing_data_handling#practice",
            "pandas.missing_data_handling#assessment:detect_missing_values",
            "pandas.missing_data_handling#assessment:drop_rows_missing_required_field",
            "pandas.missing_data_handling#assessment:fill_missing_values_with_value_or_median",
            "pandas.missing_data_handling#assessment:choose_drop_or_fill"
        ],
        "public": {
            "prompt": "The `orders_messy` DataFrame has missing values in `delivery_time_minutes`. Print the DataFrame's `isna()` output, then fill the missing values in `delivery_time_minutes` with the column's median. Print the DataFrame after filling.\n\nUse only `df.isna()`, `df['col'].fillna(value)`, `df['col'].median()`, `df['col'] = ...`, and `print()`.",
            "runtime": {"kind": "python", "version": "0.29.5", "packages": ["pandas"]},
            "workspace": {
                "files": [{
                    "path": "solution.py",
                    "role": "editable",
                    "language": "python",
                    "content": "import pandas as pd\n\norders_messy = pd.read_csv('orders_messy.csv')\n\n# TODO: Print isna() output\n\n# TODO: Fill missing delivery_time_minutes with median\n\n# TODO: Print DataFrame after filling\n"
                }],
                "entry": "solution.py",
                "asset_mounts": [{
                    "asset_id": "ds_orders",
                    "variant_id": "orders_messy",
                    "mount_path": "orders_messy.csv"
                }]
            },
            "constraints": {
                "allowed_syntax": ["df.isna()", "df.notna()", "df.dropna(subset=[...])", "df['col'].fillna(value)", "df['col'].median()", "print()"],
                "blocked_syntax": ["df.interpolate", "df.ffill", "df.replace", "df.groupby", "df.merge"]
            }
        },
        "grading": {
            "solution_files": [{
                "path": "solution.py",
                "content": "import pandas as pd\n\norders_messy = pd.read_csv('orders_messy.csv')\n\n# Print isna() output\nprint(orders_messy.isna())\n\n# Fill missing delivery_time_minutes with median\nmedian_val = orders_messy['delivery_time_minutes'].median()\norders_messy['delivery_time_minutes'] = orders_messy['delivery_time_minutes'].fillna(median_val)\n\n# Print DataFrame after filling\nprint(orders_messy)\n"
            }],
            "tests": [{
                "test_id": "t1",
                "kind": "value_equals",
                "spec": {
                    "expr": "orders_messy['delivery_time_minutes'].isna().sum()",
                    "expected": 0
                },
                "visible": True,
                "message_on_fail": "After filling, there should be no missing values in delivery_time_minutes. Check that you filled with the median."
            }]
        },
        "feedback": {
            "correct": {"message": "Perfect! You detected missing values and filled them with the median."},
            "incorrect": {"message": "Not quite. Make sure you print isna() output, then fill missing values with the median."},
            "hints": ["Use `isna()` to detect missing values, and `fillna(median)` to replace them."],
            "remediation_step_id": get_remediation_step_id(tile_id, "pandas.missing_data_handling")
        }
    }
})

interactions['tiles'].append(tile_interactions)

# ========== tile_pandas_descriptive_stats ==========
tile_id = "tile_pandas_descriptive_stats"
plan = plans[tile_id]
tile_interactions = {"tile_id": tile_id, "interactions": []}

# s03: check - read_describe_summary_table
step = next(s for s in plan['steps'] if s['step_id'] == f'{tile_id}.s03')
tile_interactions['interactions'].append({
    "step_id": step['step_id'],
    "interaction": {
        "type": "choice",
        "interaction_id": f"ix.{step['step_id']}",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [{
            "concept_id": "stats.pandas_descriptive_stats",
            "capability": "read_describe_summary_table",
            "fact_ids": ["f2"]
        }],
        "anchors": ["stats.pandas_descriptive_stats#assessment:read_describe_summary_table"],
        "public": {
            "prompt": "You call `orders['delivery_time_minutes'].describe()` and see a row labeled `50%` with the value 25.0. What does this row represent?",
            "options": [
                {"option_id": "opt_a", "text": "The median (middle value) of delivery_time_minutes."},
                {"option_id": "opt_b", "text": "The mean (average) of delivery_time_minutes."},
                {"option_id": "opt_c", "text": "50% of the values are exactly 25.0."},
                {"option_id": "opt_d", "text": "The standard deviation of delivery_time_minutes."}
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_a"],
            "option_feedback": {
                "opt_a": {"message": "Correct. The `50%` row in `describe()` output is the median — the value that splits the data in half."},
                "opt_b": {"message": "Not quite. The mean is shown in the `mean` row, not the `50%` row. The `50%` row is the median."},
                "opt_c": {"message": "Not quite. The `50%` row is the median, meaning 50% of values are below 25.0 and 50% are above, not that 50% are exactly 25.0."},
                "opt_d": {"message": "The standard deviation is shown in the `std` row. The `50%` row is the median."}
            }
        },
        "feedback": {
            "correct": {"message": "Exactly. The `50%` row is the median, a key summary statistic."},
            "incorrect": {"message": "Not quite. Review what the `50%` row in `describe()` output represents."},
            "hints": ["Think about which summary statistic represents the middle value of the data."],
            "remediation_step_id": get_remediation_step_id(tile_id, "stats.pandas_descriptive_stats")
        }
    }
})

# s04: hands_on - descriptive_stats practice
step = next(s for s in plan['steps'] if s['step_id'] == f'{tile_id}.s04')
tile_interactions['interactions'].append({
    "step_id": step['step_id'],
    "interaction": {
        "type": "code_exercise",
        "interaction_id": f"ix.{step['step_id']}",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "stats.pandas_descriptive_stats",
                "capability": "compute_mean_median_std_with_pandas",
                "fact_ids": ["f1"]
            },
            {
                "concept_id": "stats.pandas_descriptive_stats",
                "capability": "read_describe_summary_table",
                "fact_ids": ["f2"]
            },
            {
                "concept_id": "stats.pandas_descriptive_stats",
                "capability": "interpret_mean_and_std_in_context",
                "fact_ids": ["f1", "f2"]
            }
        ],
        "anchors": [
            "stats.pandas_descriptive_stats#practice",
            "stats.pandas_descriptive_stats#assessment:compute_mean_median_std_with_pandas",
            "stats.pandas_descriptive_stats#assessment:interpret_mean_and_std_in_context"
        ],
        "public": {
            "prompt": "The `orders` DataFrame has a `delivery_time_minutes` column. Compute and print the mean, median, and standard deviation of this column, then print the full `describe()` output.\n\nUse only `df['col'].mean()`, `df['col'].median()`, `df['col'].std()`, `df['col'].describe()`, and `print()`.",
            "runtime": {"kind": "python", "version": "0.29.5", "packages": ["pandas"]},
            "workspace": {
                "files": [{
                    "path": "solution.py",
                    "role": "editable",
                    "language": "python",
                    "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\n# TODO: Print mean of delivery_time_minutes\n\n# TODO: Print median of delivery_time_minutes\n\n# TODO: Print std of delivery_time_minutes\n\n# TODO: Print describe() output\n"
                }],
                "entry": "solution.py",
                "asset_mounts": [{
                    "asset_id": "ds_orders",
                    "variant_id": None,
                    "mount_path": "orders.csv"
                }]
            },
            "constraints": {
                "allowed_syntax": ["df['col'].mean()", "df['col'].median()", "df['col'].std()", "df.describe()", "df['col'].describe()", "print()"],
                "blocked_syntax": ["df.groupby", "df.loc", "df.iloc", "boolean filtering", "df.corr()"]
            }
        },
        "grading": {
            "solution_files": [{
                "path": "solution.py",
                "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\n# Print mean of delivery_time_minutes\nprint(orders['delivery_time_minutes'].mean())\n\n# Print median of delivery_time_minutes\nprint(orders['delivery_time_minutes'].median())\n\n# Print std of delivery_time_minutes\nprint(orders['delivery_time_minutes'].std())\n\n# Print describe() output\nprint(orders['delivery_time_minutes'].describe())\n"
            }],
            "tests": [
                {
                    "test_id": "t1",
                    "kind": "value_equals",
                    "spec": {
                        "expr": "orders['delivery_time_minutes'].mean()",
                        "expected": dt_mean
                    },
                    "visible": True,
                    "message_on_fail": f"The mean should be {dt_mean}. Check that you computed it correctly."
                },
                {
                    "test_id": "t2",
                    "kind": "value_equals",
                    "spec": {
                        "expr": "orders['delivery_time_minutes'].median()",
                        "expected": dt_median
                    },
                    "visible": True,
                    "message_on_fail": f"The median should be {dt_median}. Check that you computed it correctly."
                }
            ]
        },
        "feedback": {
            "correct": {"message": "Excellent! You computed the key descriptive statistics and read the describe() summary."},
            "incorrect": {"message": "Not quite. Make sure you print mean, median, std, and describe() in that order."},
            "hints": ["Call `.mean()`, `.median()`, `.std()`, and `.describe()` on the delivery_time_minutes column."],
            "remediation_step_id": get_remediation_step_id(tile_id, "stats.pandas_descriptive_stats")
        }
    }
})

interactions['tiles'].append(tile_interactions)

# Write output
with open('interactions.part.c2.json', 'w') as f:
    json.dump(interactions, f, indent=2)

print(f"Generated {sum(len(t['interactions']) for t in interactions['tiles'])} interactions for {len(interactions['tiles'])} tiles")
