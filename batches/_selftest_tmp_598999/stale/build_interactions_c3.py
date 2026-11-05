#!/usr/bin/env python3
"""
Build interactions.part.c3.json for chunk c3:
- tile_pandas_map_apply
- tile_pandas_groupby_melt
- tile_pandas_concat_merge
- tile_pandas_pivot_export
"""
import json

# Tile IDs for chunk c3
TILE_IDS = [
    "tile_pandas_map_apply",
    "tile_pandas_groupby_melt",
    "tile_pandas_concat_merge",
    "tile_pandas_pivot_export"
]

def build_interactions():
    """Build the interactions part for chunk c3."""
    
    tiles = []
    
    # ===== tile_pandas_map_apply =====
    tiles.append({
        "tile_id": "tile_pandas_map_apply",
        "interactions": [
            # s02: check - map_substitution
            {
                "step_id": "tile_pandas_map_apply.s02",
                "interaction": {
                    "type": "choice",
                    "interaction_id": "ix.tile_pandas_map_apply.s02",
                    "difficulty": "core",
                    "grading_mode": "client",
                    "standalone": False,
                    "measures": [
                        {
                            "concept_id": "pandas.map_substitution",
                            "capability": "recode_values_with_dict_mapping",
                            "fact_ids": ["f2"]
                        }
                    ],
                    "anchors": ["pandas.map_substitution#assessment:recode_values_with_dict_mapping"],
                    "public": {
                        "prompt": "You have a DataFrame `orders` with a `city_code` column holding 'LOS', 'ABJ', 'KAN'. You want to replace each code with the full city name using a dict `city_lookup = {'LOS': 'Lagos', 'ABJ': 'Abuja', 'KAN': 'Kano'}`. Which approach is correct?",
                        "options": [
                            {
                                "option_id": "opt_a",
                                "text": "`orders['city_name'] = orders['city_code'].map(city_lookup)`"
                            },
                            {
                                "option_id": "opt_b",
                                "text": "`orders['city_name'] = orders['city_code'].replace(city_lookup)`"
                            },
                            {
                                "option_id": "opt_c",
                                "text": "`orders['city_name'] = city_lookup[orders['city_code']]`"
                            },
                            {
                                "option_id": "opt_d",
                                "text": "`orders['city_name'] = orders['city_code'].apply(city_lookup)`"
                            }
                        ],
                        "selection": "single",
                        "shuffle": True
                    },
                    "grading": {
                        "correct_option_ids": ["opt_a"],
                        "option_feedback": {
                            "opt_a": {
                                "message": "Correct. `.map(dict)` replaces each value in the Series with the corresponding dict value."
                            },
                            "opt_b": {
                                "message": "`.replace()` can work with a dict, but `.map()` is the standard method for substituting values using a mapping correspondence. `.map()` is designed for this exact use case."
                            },
                            "opt_c": {
                                "message": "Not quite. You cannot index a dict with a Series directly. Use `.map(city_lookup)` to apply the dict to every element."
                            },
                            "opt_d": {
                                "message": "`.apply()` expects a function, not a dict. Use `.map(city_lookup)` to substitute values using a dict."
                            }
                        }
                    },
                    "feedback": {
                        "correct": {
                            "message": "Exactly right. `.map()` with a dict is the standard way to substitute values."
                        },
                        "incorrect": {
                            "message": "Not quite. Review how `.map()` accepts a dict to replace each value."
                        },
                        "hints": [
                            "Think about which Series method accepts a dict mapping and applies it to every element."
                        ],
                        "remediation_step_id": "tile_pandas_map_apply.r01"
                    }
                }
            },
            # s03: hands_on - map_substitution practice
            {
                "step_id": "tile_pandas_map_apply.s03",
                "interaction": {
                    "type": "code_exercise",
                    "interaction_id": "ix.tile_pandas_map_apply.s03",
                    "difficulty": "core",
                    "grading_mode": "client",
                    "standalone": False,
                    "measures": [
                        {
                            "concept_id": "pandas.map_substitution",
                            "capability": "map_series_with_function",
                            "fact_ids": ["f1"]
                        },
                        {
                            "concept_id": "pandas.map_substitution",
                            "capability": "recode_values_with_dict_mapping",
                            "fact_ids": ["f2"]
                        }
                    ],
                    "anchors": [
                        "pandas.map_substitution#practice",
                        "pandas.map_substitution#assessment:map_series_with_function",
                        "pandas.map_substitution#assessment:recode_values_with_dict_mapping"
                    ],
                    "public": {
                        "prompt": "The `orders` DataFrame has a `city_code` column with three-letter codes ('LOS', 'ABJ', 'KAN'). Use `.map(city_lookup)` to create a new column `city_name` with the full city names, then print the `city_name` column.\n\nThe lookup dict is already defined: `city_lookup = {'LOS': 'Lagos', 'ABJ': 'Abuja', 'KAN': 'Kano'}`.\n\nUse only `df['col'].map(dict)`, `df['new'] = ...`, and `print()`.",
                        "runtime": {
                            "kind": "python",
                            "version": "0.29.5",
                            "packages": ["pandas"]
                        },
                        "workspace": {
                            "files": [
                                {
                                    "path": "solution.py",
                                    "role": "editable",
                                    "language": "python",
                                    "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\n# Lookup dict for city codes\ncity_lookup = {'LOS': 'Lagos', 'ABJ': 'Abuja', 'KAN': 'Kano'}\n\n# TODO: use .map(city_lookup) to create city_name column\n\n# TODO: print the city_name column\n"
                                }
                            ],
                            "entry": "solution.py",
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
                                "df['col'].map(function)",
                                "df['col'].map(dict)",
                                "df['new'] = ...",
                                "print()"
                            ],
                            "blocked_syntax": [
                                "df.apply",
                                "df.replace",
                                "df.groupby",
                                "df.merge"
                            ]
                        }
                    },
                    "grading": {
                        "solution_files": [
                            {
                                "path": "solution.py",
                                "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\ncity_lookup = {'LOS': 'Lagos', 'ABJ': 'Abuja', 'KAN': 'Kano'}\n\norders['city_name'] = orders['city_code'].map(city_lookup)\n\nprint(orders['city_name'])\n"
                            }
                        ],
                        "tests": [
                            {
                                "test_id": "t1",
                                "kind": "dataframe_equals",
                                "spec": {
                                    "expr": "orders[['city_name']]",
                                    "expected": {
                                        "columns": ["city_name"],
                                        "rows": [
                                            ["Lagos"], ["Abuja"], ["Kano"], ["Lagos"], ["Abuja"], ["Kano"], ["Lagos"],
                                            ["Abuja"], ["Kano"], ["Lagos"], ["Abuja"], ["Kano"], ["Lagos"], ["Abuja"]
                                        ]
                                    }
                                },
                                "visible": True,
                                "message_on_fail": "The city_name column should contain the full city names mapped from city_code."
                            }
                        ]
                    },
                    "feedback": {
                        "correct": {
                            "message": "Perfect! You used `.map()` to substitute city codes with full names."
                        },
                        "incorrect": {
                            "message": "Not quite. Make sure you use `.map(city_lookup)` to create the city_name column."
                        },
                        "hints": [
                            "Use `orders['city_name'] = orders['city_code'].map(city_lookup)` to create the new column."
                        ],
                        "remediation_step_id": "tile_pandas_map_apply.r01"
                    }
                }
            },
            # s06: check - apply_transform
            {
                "step_id": "tile_pandas_map_apply.s06",
                "interaction": {
                    "type": "choice",
                    "interaction_id": "ix.tile_pandas_map_apply.s06",
                    "difficulty": "core",
                    "grading_mode": "client",
                    "standalone": False,
                    "measures": [
                        {
                            "concept_id": "pandas.apply_transform",
                            "capability": "apply_function_across_rows_with_axis_1",
                            "fact_ids": ["f1"]
                        }
                    ],
                    "anchors": ["pandas.apply_transform#assessment:apply_function_across_rows_with_axis_1"],
                    "public": {
                        "prompt": "You want to create a new column `speed_label` that labels each order as 'slow' if `delivery_time_minutes > 25`, else 'fast'. You have a function `label_speed(row)` that reads `row['delivery_time_minutes']` and returns the label. Which approach is correct?",
                        "options": [
                            {
                                "option_id": "opt_a",
                                "text": "`orders['speed_label'] = orders.apply(label_speed, axis=1)`"
                            },
                            {
                                "option_id": "opt_b",
                                "text": "`orders['speed_label'] = orders['delivery_time_minutes'].apply(label_speed)`"
                            },
                            {
                                "option_id": "opt_c",
                                "text": "`orders['speed_label'] = orders.apply(label_speed)`"
                            },
                            {
                                "option_id": "opt_d",
                                "text": "`orders['speed_label'] = label_speed(orders)`"
                            }
                        ],
                        "selection": "single",
                        "shuffle": True
                    },
                    "grading": {
                        "correct_option_ids": ["opt_a"],
                        "option_feedback": {
                            "opt_a": {
                                "message": "Correct. `axis=1` tells `.apply()` to pass each row to the function, so `label_speed` receives one row at a time and can read any column."
                            },
                            "opt_b": {
                                "message": "Not quite. `.apply()` on a Series passes individual values, not rows. To read multiple columns from a row, use `df.apply(function, axis=1)`."
                            },
                            "opt_c": {
                                "message": "Without `axis=1`, `.apply()` operates on each column by default, not each row. Use `axis=1` to pass rows to the function."
                            },
                            "opt_d": {
                                "message": "The function expects a single row, not the entire DataFrame. Use `df.apply(label_speed, axis=1)` to apply it to each row."
                            }
                        }
                    },
                    "feedback": {
                        "correct": {
                            "message": "Exactly right. `axis=1` makes `.apply()` pass each row to the function."
                        },
                        "incorrect": {
                            "message": "Not quite. Review how `axis=1` changes what `.apply()` passes to the function."
                        },
                        "hints": [
                            "Think about which axis argument makes `.apply()` operate on rows instead of columns."
                        ],
                        "remediation_step_id": "tile_pandas_map_apply.r02"
                    }
                }
            },
            # s07: hands_on - apply_transform practice
            {
                "step_id": "tile_pandas_map_apply.s07",
                "interaction": {
                    "type": "code_exercise",
                    "interaction_id": "ix.tile_pandas_map_apply.s07",
                    "difficulty": "core",
                    "grading_mode": "client",
                    "standalone": False,
                    "measures": [
                        {
                            "concept_id": "pandas.apply_transform",
                            "capability": "apply_function_down_columns",
                            "fact_ids": ["f1"]
                        }
                    ],
                    "anchors": [
                        "pandas.apply_transform#practice",
                        "pandas.apply_transform#assessment:apply_function_down_columns"
                    ],
                    "public": {
                        "prompt": "Define a function `label_speed(row)` that returns 'slow' if `row['delivery_time_minutes'] > 25`, else 'fast'. Then use `.apply(label_speed, axis=1)` to create a new column `speed_label`, and print the `speed_label` column.\n\nUse only `def function(row): ...`, `df.apply(function, axis=1)`, `df['new'] = ...`, and `print()`.",
                        "runtime": {
                            "kind": "python",
                            "version": "0.29.5",
                            "packages": ["pandas"]
                        },
                        "workspace": {
                            "files": [
                                {
                                    "path": "solution.py",
                                    "role": "editable",
                                    "language": "python",
                                    "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\n# TODO: define label_speed(row) function\n\n# TODO: use .apply(label_speed, axis=1) to create speed_label column\n\n# TODO: print the speed_label column\n"
                                }
                            ],
                            "entry": "solution.py",
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
                                "def function(row): ...",
                                "df.apply(function, axis=1)",
                                "df['new'] = ...",
                                "print()"
                            ],
                            "blocked_syntax": [
                                "df.map",
                                "df.groupby",
                                "df.agg",
                                "df.transform"
                            ]
                        }
                    },
                    "grading": {
                        "solution_files": [
                            {
                                "path": "solution.py",
                                "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\ndef label_speed(row):\n    if row['delivery_time_minutes'] > 25:\n        return 'slow'\n    else:\n        return 'fast'\n\norders['speed_label'] = orders.apply(label_speed, axis=1)\n\nprint(orders['speed_label'])\n"
                            }
                        ],
                        "tests": [
                            {
                                "test_id": "t1",
                                "kind": "dataframe_equals",
                                "spec": {
                                    "expr": "orders[['speed_label']]",
                                    "expected": {
                                        "columns": ["speed_label"],
                                        "rows": [
                                            ["fast"], ["fast"], ["fast"], ["fast"], ["slow"], ["slow"], ["slow"],
                                            ["slow"], ["fast"], ["fast"], ["slow"], ["fast"], ["slow"], ["slow"]
                                        ]
                                    }
                                },
                                "visible": True,
                                "message_on_fail": "The speed_label column should contain 'slow' for delivery_time_minutes > 25, else 'fast'."
                            }
                        ]
                    },
                    "feedback": {
                        "correct": {
                            "message": "Perfect! You used `.apply()` with `axis=1` to compute a value from each row."
                        },
                        "incorrect": {
                            "message": "Not quite. Make sure your function reads `row['delivery_time_minutes']` and you use `axis=1`."
                        },
                        "hints": [
                            "Define the function to take `row` as a parameter and return 'slow' or 'fast' based on the condition."
                        ],
                        "remediation_step_id": "tile_pandas_map_apply.r02"
                    }
                }
            }
        ]
    })
    
    # ===== tile_pandas_groupby_melt =====
    tiles.append({
        "tile_id": "tile_pandas_groupby_melt",
        "interactions": [
            # s04: check - groupby_aggregation
            {
                "step_id": "tile_pandas_groupby_melt.s04",
                "interaction": {
                    "type": "choice",
                    "interaction_id": "ix.tile_pandas_groupby_melt.s04",
                    "difficulty": "intro",
                    "grading_mode": "client",
                    "standalone": False,
                    "measures": [
                        {
                            "concept_id": "pandas.groupby_aggregation",
                            "capability": "describe_split_apply_combine",
                            "fact_ids": ["f1"]
                        }
                    ],
                    "anchors": ["pandas.groupby_aggregation#assessment:describe_split_apply_combine"],
                    "public": {
                        "prompt": "What does the 'split-apply-combine' pattern describe in the context of `groupby()`?",
                        "options": [
                            {
                                "option_id": "opt_a",
                                "text": "Split the data into groups, apply a function to each group independently, and combine the results into a data structure."
                            },
                            {
                                "option_id": "opt_b",
                                "text": "Split the DataFrame into rows and columns, apply a filter, and combine them back."
                            },
                            {
                                "option_id": "opt_c",
                                "text": "Split the data by index, apply a sort, and combine the sorted pieces."
                            },
                            {
                                "option_id": "opt_d",
                                "text": "Split the data into training and test sets, apply a model, and combine predictions."
                            }
                        ],
                        "selection": "single",
                        "shuffle": True
                    },
                    "grading": {
                        "correct_option_ids": ["opt_a"],
                        "option_feedback": {
                            "opt_a": {
                                "message": "Correct. The split-apply-combine pattern is the core of `groupby()`: split by a key, apply a function to each group, and combine the results."
                            },
                            "opt_b": {
                                "message": "Not quite. The pattern is about grouping by a key column, not splitting into rows and columns. Review the three steps: split, apply, combine."
                            },
                            "opt_c": {
                                "message": "The pattern is not about sorting. It's about grouping data by a key, applying a function to each group, and combining the results."
                            },
                            "opt_d": {
                                "message": "That describes a machine learning workflow, not `groupby()`. The split-apply-combine pattern groups data by a key, applies a function to each group, and combines the results."
                            }
                        }
                    },
                    "feedback": {
                        "correct": {
                            "message": "Exactly right. Split-apply-combine is the foundation of `groupby()` operations."
                        },
                        "incorrect": {
                            "message": "Not quite. Review the three steps of the split-apply-combine pattern."
                        },
                        "hints": [
                            "Think about what happens when you group data by a key and compute a summary for each group."
                        ],
                        "remediation_step_id": "tile_pandas_groupby_melt.r01"
                    }
                }
            },
            # s05: hands_on - groupby_aggregation practice
            {
                "step_id": "tile_pandas_groupby_melt.s05",
                "interaction": {
                    "type": "code_exercise",
                    "interaction_id": "ix.tile_pandas_groupby_melt.s05",
                    "difficulty": "core",
                    "grading_mode": "client",
                    "standalone": False,
                    "measures": [
                        {
                            "concept_id": "pandas.groupby_aggregation",
                            "capability": "write_groupby_aggregation",
                            "fact_ids": ["f2", "f3"]
                        },
                        {
                            "concept_id": "pandas.groupby_aggregation",
                            "capability": "read_group_keys_as_result_index",
                            "fact_ids": ["f3"]
                        }
                    ],
                    "anchors": [
                        "pandas.groupby_aggregation#practice",
                        "pandas.groupby_aggregation#assessment:write_groupby_aggregation",
                        "pandas.groupby_aggregation#assessment:read_group_keys_as_result_index"
                    ],
                    "public": {
                        "prompt": "The `orders` DataFrame has `customer_id` and `order_value` columns. Use `groupby('customer_id')` to compute both the sum and mean of `order_value` for each customer in one call using `.agg(['sum', 'mean'])`. Print the result.\n\nThe customer IDs should form the index of the result.\n\nUse only `df.groupby('key')['col'].sum()`, `df.groupby('key')['col'].mean()`, `df.groupby('key')['col'].agg([...])`, and `print()`.",
                        "runtime": {
                            "kind": "python",
                            "version": "0.29.5",
                            "packages": ["pandas"]
                        },
                        "workspace": {
                            "files": [
                                {
                                    "path": "solution.py",
                                    "role": "editable",
                                    "language": "python",
                                    "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\n# TODO: groupby customer_id, compute sum and mean of order_value\n\n# TODO: print the result\n"
                                }
                            ],
                            "entry": "solution.py",
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
                                "df.groupby('key')['col'].sum()",
                                "df.groupby('key')['col'].mean()",
                                "df.groupby('key')['col'].agg([...])",
                                "print()"
                            ],
                            "blocked_syntax": [
                                "df.pivot_table",
                                "df.merge",
                                "df.transform",
                                "df.melt"
                            ]
                        }
                    },
                    "grading": {
                        "solution_files": [
                            {
                                "path": "solution.py",
                                "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\nresult = orders.groupby('customer_id')['order_value'].agg(['sum', 'mean'])\n\nprint(result)\n"
                            }
                        ],
                        "tests": [
                            {
                                "test_id": "t1",
                                "kind": "dataframe_equals",
                                "spec": {
                                    "expr": "orders.groupby('customer_id')['order_value'].agg(['sum', 'mean']).reset_index()",
                                    "expected": {
                                        "columns": ["customer_id", "sum", "mean"],
                                        "rows": [
                                            [301, 2500, 2500.0], [302, 3100, 3100.0], [303, 1800, 1800.0],
                                            [304, 2200, 2200.0], [305, 4000, 4000.0], [306, 1500, 1500.0],
                                            [307, 5500, 5500.0], [308, 3800, 3800.0], [309, 2100, 2100.0],
                                            [310, 2900, 2900.0], [311, 4200, 4200.0], [312, 1700, 1700.0],
                                            [313, 3300, 3300.0], [314, 4600, 4600.0]
                                        ]
                                    }
                                },
                                "visible": True,
                                "message_on_fail": "The result should have one row per customer_id with sum and mean of order_value."
                            }
                        ]
                    },
                    "feedback": {
                        "correct": {
                            "message": "Perfect! You computed multiple aggregations in one call."
                        },
                        "incorrect": {
                            "message": "Not quite. Make sure you use `.agg(['sum', 'mean'])` to compute both aggregations."
                        },
                        "hints": [
                            "Use `orders.groupby('customer_id')['order_value'].agg(['sum', 'mean'])` to compute both."
                        ],
                        "remediation_step_id": "tile_pandas_groupby_melt.r01"
                    }
                }
            },
            # s08: check - melt_reshaping
            {
                "step_id": "tile_pandas_groupby_melt.s08",
                "interaction": {
                    "type": "choice",
                    "interaction_id": "ix.tile_pandas_groupby_melt.s08",
                    "difficulty": "core",
                    "grading_mode": "client",
                    "standalone": False,
                    "measures": [
                        {
                            "concept_id": "pandas.melt_reshaping",
                            "capability": "rename_melt_output_columns",
                            "fact_ids": ["f2"]
                        }
                    ],
                    "anchors": ["pandas.melt_reshaping#assessment:rename_melt_output_columns"],
                    "public": {
                        "prompt": "You melt a wide DataFrame with `id_vars=['city']`. By default, the output has columns named 'variable' and 'value'. How do you rename them to 'month' and 'deliveries'?",
                        "options": [
                            {
                                "option_id": "opt_a",
                                "text": "`df.melt(id_vars=['city'], var_name='month', value_name='deliveries')`"
                            },
                            {
                                "option_id": "opt_b",
                                "text": "`df.melt(id_vars=['city']).rename(columns={'variable': 'month', 'value': 'deliveries'})`"
                            },
                            {
                                "option_id": "opt_c",
                                "text": "`df.melt(id_vars=['city'], columns=['month', 'deliveries'])`"
                            },
                            {
                                "option_id": "opt_d",
                                "text": "`df.melt(id_vars=['city'], names=['month', 'deliveries'])`"
                            }
                        ],
                        "selection": "single",
                        "shuffle": True
                    },
                    "grading": {
                        "correct_option_ids": ["opt_a"],
                        "option_feedback": {
                            "opt_a": {
                                "message": "Correct. `var_name` and `value_name` parameters rename the default 'variable' and 'value' columns."
                            },
                            "opt_b": {
                                "message": "This works, but `melt()` has built-in parameters `var_name` and `value_name` to rename the columns directly: `df.melt(id_vars=['city'], var_name='month', value_name='deliveries')`."
                            },
                            "opt_c": {
                                "message": "There is no `columns` parameter for `melt()`. Use `var_name` and `value_name` to rename the output columns."
                            },
                            "opt_d": {
                                "message": "There is no `names` parameter for `melt()`. Use `var_name` and `value_name` to rename the output columns."
                            }
                        }
                    },
                    "feedback": {
                        "correct": {
                            "message": "Exactly right. `var_name` and `value_name` control the output column names."
                        },
                        "incorrect": {
                            "message": "Not quite. Review the parameters that rename the output columns of `melt()`."
                        },
                        "hints": [
                            "Think about which parameters `melt()` accepts to rename the 'variable' and 'value' columns."
                        ],
                        "remediation_step_id": "tile_pandas_groupby_melt.r02"
                    }
                }
            },
            # s09: hands_on - melt_reshaping practice
            {
                "step_id": "tile_pandas_groupby_melt.s09",
                "interaction": {
                    "type": "code_exercise",
                    "interaction_id": "ix.tile_pandas_groupby_melt.s09",
                    "difficulty": "core",
                    "grading_mode": "client",
                    "standalone": False,
                    "measures": [
                        {
                            "concept_id": "pandas.melt_reshaping",
                            "capability": "melt_wide_to_long_with_id_vars",
                            "fact_ids": ["f1"]
                        },
                        {
                            "concept_id": "pandas.melt_reshaping",
                            "capability": "rename_melt_output_columns",
                            "fact_ids": ["f2"]
                        }
                    ],
                    "anchors": [
                        "pandas.melt_reshaping#practice",
                        "pandas.melt_reshaping#assessment:melt_wide_to_long_with_id_vars",
                        "pandas.melt_reshaping#assessment:rename_melt_output_columns"
                    ],
                    "public": {
                        "prompt": "The `city_deliveries` DataFrame has columns `city`, `jan_deliveries`, `feb_deliveries`, `mar_deliveries`. Use `melt()` to reshape it to long format with `id_vars=['city']`, and rename the output columns to `month` and `deliveries` using `var_name` and `value_name`. Print the result.\n\nUse only `df.melt(id_vars=[...])`, `pd.melt(df, id_vars=[...])`, `var_name='month'`, `value_name='value'`, and `print()`.",
                        "runtime": {
                            "kind": "python",
                            "version": "0.29.5",
                            "packages": ["pandas"]
                        },
                        "workspace": {
                            "files": [
                                {
                                    "path": "solution.py",
                                    "role": "editable",
                                    "language": "python",
                                    "content": "import pandas as pd\n\ncity_deliveries = pd.read_csv('city_deliveries.csv')\n\n# TODO: melt to long format with id_vars=['city'], var_name='month', value_name='deliveries'\n\n# TODO: print the result\n"
                                }
                            ],
                            "entry": "solution.py",
                            "asset_mounts": [
                                {
                                    "asset_id": "ds_monthly_wide",
                                    "variant_id": None,
                                    "mount_path": "city_deliveries.csv"
                                }
                            ]
                        },
                        "constraints": {
                            "allowed_syntax": [
                                "df.melt(id_vars=[...])",
                                "pd.melt(df, id_vars=[...])",
                                "var_name='month'",
                                "value_name='value'",
                                "print()"
                            ],
                            "blocked_syntax": [
                                "df.pivot_table",
                                "df.stack",
                                "df.unstack"
                            ]
                        }
                    },
                    "grading": {
                        "solution_files": [
                            {
                                "path": "solution.py",
                                "content": "import pandas as pd\n\ncity_deliveries = pd.read_csv('city_deliveries.csv')\n\nresult = city_deliveries.melt(id_vars=['city'], var_name='month', value_name='deliveries')\n\nprint(result)\n"
                            }
                        ],
                        "tests": [
                            {
                                "test_id": "t1",
                                "kind": "dataframe_equals",
                                "spec": {
                                    "expr": "city_deliveries.melt(id_vars=['city'], var_name='month', value_name='deliveries')",
                                    "expected": {
                                        "columns": ["city", "month", "deliveries"],
                                        "rows": [
                                            ["Lagos", "jan_deliveries", 142], ["Abuja", "jan_deliveries", 98], ["Kano", "jan_deliveries", 76],
                                            ["Lagos", "feb_deliveries", 138], ["Abuja", "feb_deliveries", 104], ["Kano", "feb_deliveries", 81],
                                            ["Lagos", "mar_deliveries", 155], ["Abuja", "mar_deliveries", 110], ["Kano", "mar_deliveries", 88]
                                        ]
                                    }
                                },
                                "visible": True,
                                "message_on_fail": "The result should have one row per city-month combination with columns city, month, deliveries."
                            }
                        ]
                    },
                    "feedback": {
                        "correct": {
                            "message": "Perfect! You reshaped the wide table to long format."
                        },
                        "incorrect": {
                            "message": "Not quite. Make sure you use `id_vars=['city']`, `var_name='month'`, and `value_name='deliveries'`."
                        },
                        "hints": [
                            "Use `city_deliveries.melt(id_vars=['city'], var_name='month', value_name='deliveries')` to reshape."
                        ],
                        "remediation_step_id": "tile_pandas_groupby_melt.r02"
                    }
                }
            }
        ]
    })
    
    # ===== tile_pandas_concat_merge =====
    tiles.append({
        "tile_id": "tile_pandas_concat_merge",
        "interactions": [
            # s03: check - concat_stacking
            {
                "step_id": "tile_pandas_concat_merge.s03",
                "interaction": {
                    "type": "choice",
                    "interaction_id": "ix.tile_pandas_concat_merge.s03",
                    "difficulty": "core",
                    "grading_mode": "client",
                    "standalone": False,
                    "measures": [
                        {
                            "concept_id": "pandas.concat_stacking",
                            "capability": "choose_concat_axis",
                            "fact_ids": ["f3"]
                        }
                    ],
                    "anchors": ["pandas.concat_stacking#assessment:choose_concat_axis"],
                    "public": {
                        "prompt": "You have three DataFrames with the same columns and want to stack them row-wise (one below the other). Which `pd.concat()` call is correct?",
                        "options": [
                            {
                                "option_id": "opt_a",
                                "text": "`pd.concat([df1, df2, df3])`"
                            },
                            {
                                "option_id": "opt_b",
                                "text": "`pd.concat([df1, df2, df3], axis=1)`"
                            },
                            {
                                "option_id": "opt_c",
                                "text": "`pd.concat([df1, df2, df3], axis=0)`"
                            },
                            {
                                "option_id": "opt_d",
                                "text": "Both A and C are correct"
                            }
                        ],
                        "selection": "single",
                        "shuffle": True
                    },
                    "grading": {
                        "correct_option_ids": ["opt_d"],
                        "option_feedback": {
                            "opt_d": {
                                "message": "Correct. By default, `pd.concat()` stacks row-wise (axis=0), so both calls produce the same result."
                            },
                            "opt_a": {
                                "message": "This is correct, but not the only correct answer. `axis=0` is the default, so `pd.concat([df1, df2, df3])` and `pd.concat([df1, df2, df3], axis=0)` are equivalent."
                            },
                            "opt_b": {
                                "message": "`axis=1` places the DataFrames side by side as columns, not row-wise. For row-wise stacking, use the default (no axis argument) or `axis=0`."
                            },
                            "opt_c": {
                                "message": "This is correct, but not the only correct answer. `axis=0` is the default, so `pd.concat([df1, df2, df3])` and `pd.concat([df1, df2, df3], axis=0)` are equivalent."
                            }
                        }
                    },
                    "feedback": {
                        "correct": {
                            "message": "Exactly right. The default axis is 0 (row-wise stacking)."
                        },
                        "incorrect": {
                            "message": "Not quite. Review the default axis for `pd.concat()`."
                        },
                        "hints": [
                            "Think about what the default axis is for `pd.concat()` when no axis argument is given."
                        ],
                        "remediation_step_id": "tile_pandas_concat_merge.r01"
                    }
                }
            },
            # s04: hands_on - concat_stacking practice
            {
                "step_id": "tile_pandas_concat_merge.s04",
                "interaction": {
                    "type": "code_exercise",
                    "interaction_id": "ix.tile_pandas_concat_merge.s04",
                    "difficulty": "core",
                    "grading_mode": "client",
                    "standalone": False,
                    "measures": [
                        {
                            "concept_id": "pandas.concat_stacking",
                            "capability": "stack_dataframes_row_wise",
                            "fact_ids": ["f1", "f2"]
                        },
                        {
                            "concept_id": "pandas.concat_stacking",
                            "capability": "choose_concat_axis",
                            "fact_ids": ["f3"]
                        }
                    ],
                    "anchors": [
                        "pandas.concat_stacking#practice",
                        "pandas.concat_stacking#assessment:stack_dataframes_row_wise",
                        "pandas.concat_stacking#assessment:choose_concat_axis"
                    ],
                    "public": {
                        "prompt": "You have three monthly order tables: `jan_orders`, `feb_orders`, `mar_orders`, all with the same columns. Use `pd.concat()` to stack them row-wise into one DataFrame, then print the result.\n\nUse only `pd.concat([df1, df2, df3])`, `axis=1`, and `print()`.",
                        "runtime": {
                            "kind": "python",
                            "version": "0.29.5",
                            "packages": ["pandas"]
                        },
                        "workspace": {
                            "files": [
                                {
                                    "path": "solution.py",
                                    "role": "editable",
                                    "language": "python",
                                    "content": "import pandas as pd\n\njan_orders = pd.read_csv('jan_orders.csv')\nfeb_orders = pd.read_csv('feb_orders.csv')\nmar_orders = pd.read_csv('mar_orders.csv')\n\n# TODO: use pd.concat() to stack the three tables row-wise\n\n# TODO: print the result\n"
                                }
                            ],
                            "entry": "solution.py",
                            "asset_mounts": [
                                {
                                    "asset_id": "ds_jan_orders",
                                    "variant_id": None,
                                    "mount_path": "jan_orders.csv"
                                },
                                {
                                    "asset_id": "ds_feb_orders",
                                    "variant_id": None,
                                    "mount_path": "feb_orders.csv"
                                },
                                {
                                    "asset_id": "ds_mar_orders",
                                    "variant_id": None,
                                    "mount_path": "mar_orders.csv"
                                }
                            ]
                        },
                        "constraints": {
                            "allowed_syntax": [
                                "pd.concat([df1, df2, df3])",
                                "axis=1",
                                "print()"
                            ],
                            "blocked_syntax": [
                                "df.merge",
                                "df.join",
                                "df.groupby",
                                "df.append"
                            ]
                        }
                    },
                    "grading": {
                        "solution_files": [
                            {
                                "path": "solution.py",
                                "content": "import pandas as pd\n\njan_orders = pd.read_csv('jan_orders.csv')\nfeb_orders = pd.read_csv('feb_orders.csv')\nmar_orders = pd.read_csv('mar_orders.csv')\n\nresult = pd.concat([jan_orders, feb_orders, mar_orders], ignore_index=True)\n\nprint(result)\n"
                            }
                        ],
                        "tests": [
                            {
                                "test_id": "t1",
                                "kind": "dataframe_equals",
                                "spec": {
                                    "expr": "pd.concat([jan_orders, feb_orders, mar_orders], ignore_index=True)",
                                    "expected": {
                                        "columns": ["order_id", "city", "courier", "delivery_time_minutes", "order_value"],
                                        "rows": [
                                            [2001, "Lagos", "Ada", 18, 2500], [2002, "Abuja", "Bayo", 22, 3100],
                                            [2003, "Kano", "Chidi", 26, 1800], [2004, "Lagos", "Ada", 31, 2900],
                                            [2005, "Abuja", "Bayo", 19, 3400], [2006, "Lagos", "Ada", 20, 2700],
                                            [2007, "Abuja", "Bayo", 28, 4000], [2008, "Kano", "Chidi", 24, 1600],
                                            [2009, "Lagos", "Ada", 35, 5100], [2010, "Kano", "Chidi", 21, 2000],
                                            [2011, "Lagos", "Ada", 22, 2600], [2012, "Abuja", "Bayo", 30, 3700],
                                            [2013, "Kano", "Chidi", 27, 1900], [2014, "Lagos", "Ada", 80, 5500],
                                            [2015, "Abuja", "Bayo", 23, 3200]
                                        ]
                                    }
                                },
                                "visible": True,
                                "message_on_fail": "The result should have all rows from jan, feb, and mar orders stacked row-wise."
                            }
                        ]
                    },
                    "feedback": {
                        "correct": {
                            "message": "Perfect! You stacked the three tables row-wise."
                        },
                        "incorrect": {
                            "message": "Not quite. Make sure you use `pd.concat([jan_orders, feb_orders, mar_orders])` to stack them."
                        },
                        "hints": [
                            "Use `pd.concat([jan_orders, feb_orders, mar_orders])` to stack the tables row-wise."
                        ],
                        "remediation_step_id": "tile_pandas_concat_merge.r01"
                    }
                }
            },
            # s08: check - merge_join (two capabilities)
            {
                "step_id": "tile_pandas_concat_merge.s08",
                "interaction": {
                    "type": "choice",
                    "interaction_id": "ix.tile_pandas_concat_merge.s08",
                    "difficulty": "core",
                    "grading_mode": "client",
                    "standalone": False,
                    "measures": [
                        {
                            "concept_id": "pandas.merge_join",
                            "capability": "merge_on_shared_key",
                            "fact_ids": ["f1"]
                        },
                        {
                            "concept_id": "pandas.merge_join",
                            "capability": "choose_how_join_type",
                            "fact_ids": ["f4"]
                        }
                    ],
                    "anchors": [
                        "pandas.merge_join#assessment:merge_on_shared_key",
                        "pandas.merge_join#assessment:choose_how_join_type"
                    ],
                    "public": {
                        "prompt": "You have `orders` with `customer_id` and `customers` with `customer_id`. You want to keep all orders and attach customer info where available, filling NaN for unmatched orders. Which `how` parameter is correct?",
                        "options": [
                            {
                                "option_id": "opt_a",
                                "text": "`orders.merge(customers, on='customer_id', how='left')`"
                            },
                            {
                                "option_id": "opt_b",
                                "text": "`orders.merge(customers, on='customer_id', how='inner')`"
                            },
                            {
                                "option_id": "opt_c",
                                "text": "`orders.merge(customers, on='customer_id', how='right')`"
                            },
                            {
                                "option_id": "opt_d",
                                "text": "`orders.merge(customers, on='customer_id', how='outer')`"
                            }
                        ],
                        "selection": "single",
                        "shuffle": True
                    },
                    "grading": {
                        "correct_option_ids": ["opt_a"],
                        "option_feedback": {
                            "opt_a": {
                                "message": "Correct. `how='left'` keeps all rows from the left DataFrame (orders) and fills NaN for unmatched keys."
                            },
                            "opt_b": {
                                "message": "`how='inner'` (the default) keeps only rows where the key appears in both DataFrames, dropping unmatched orders. Use `how='left'` to keep all orders."
                            },
                            "opt_c": {
                                "message": "`how='right'` keeps all rows from the right DataFrame (customers), not all orders. Use `how='left'` to keep all orders."
                            },
                            "opt_d": {
                                "message": "`how='outer'` keeps all keys from both DataFrames, including customers with no orders. Use `how='left'` to keep only all orders."
                            }
                        }
                    },
                    "feedback": {
                        "correct": {
                            "message": "Exactly right. `how='left'` keeps all rows from the left DataFrame."
                        },
                        "incorrect": {
                            "message": "Not quite. Review which `how` parameter keeps all rows from the left DataFrame."
                        },
                        "hints": [
                            "Think about which join type keeps all rows from the first (left) DataFrame."
                        ],
                        "remediation_step_id": "tile_pandas_concat_merge.r02"
                    }
                }
            },
            # s09: check - merge_join (explain NA)
            {
                "step_id": "tile_pandas_concat_merge.s09",
                "interaction": {
                    "type": "choice",
                    "interaction_id": "ix.tile_pandas_concat_merge.s09",
                    "difficulty": "core",
                    "grading_mode": "client",
                    "standalone": False,
                    "measures": [
                        {
                            "concept_id": "pandas.merge_join",
                            "capability": "explain_na_for_unmatched_keys",
                            "fact_ids": ["f3"]
                        }
                    ],
                    "anchors": ["pandas.merge_join#assessment:explain_na_for_unmatched_keys"],
                    "public": {
                        "prompt": "After a left merge of `orders` and `customers` on `customer_id`, some rows have NaN in the `customer_name` column. What does this mean?",
                        "options": [
                            {
                                "option_id": "opt_a",
                                "text": "Those orders have a `customer_id` that does not appear in the `customers` table."
                            },
                            {
                                "option_id": "opt_b",
                                "text": "Those orders have a missing `customer_id` value."
                            },
                            {
                                "option_id": "opt_c",
                                "text": "The merge failed for those rows."
                            },
                            {
                                "option_id": "opt_d",
                                "text": "Those customers have no orders."
                            }
                        ],
                        "selection": "single",
                        "shuffle": True
                    },
                    "grading": {
                        "correct_option_ids": ["opt_a"],
                        "option_feedback": {
                            "opt_a": {
                                "message": "Correct. When a key value does not appear in one DataFrame, the columns from that DataFrame are filled with NaN in the result."
                            },
                            "opt_b": {
                                "message": "Not quite. The NaN appears in the customer columns because the `customer_id` from orders does not match any row in customers, not because the `customer_id` itself is missing."
                            },
                            "opt_c": {
                                "message": "The merge did not fail. NaN values are the expected result when a key from the left DataFrame has no match in the right DataFrame."
                            },
                            "opt_d": {
                                "message": "This is a left merge starting from orders, so the NaN means the order's `customer_id` has no match in customers, not that customers have no orders."
                            }
                        }
                    },
                    "feedback": {
                        "correct": {
                            "message": "Exactly right. Unmatched keys result in NaN for the columns from the other DataFrame."
                        },
                        "incorrect": {
                            "message": "Not quite. Review what NaN means in a merge result."
                        },
                        "hints": [
                            "Think about what happens when a key value appears in one DataFrame but not the other."
                        ],
                        "remediation_step_id": "tile_pandas_concat_merge.r03"
                    }
                }
            },
            # s10: hands_on - merge_join practice
            {
                "step_id": "tile_pandas_concat_merge.s10",
                "interaction": {
                    "type": "code_exercise",
                    "interaction_id": "ix.tile_pandas_concat_merge.s10",
                    "difficulty": "core",
                    "grading_mode": "client",
                    "standalone": False,
                    "measures": [
                        {
                            "concept_id": "pandas.merge_join",
                            "capability": "predict_inner_merge_result",
                            "fact_ids": ["f2"]
                        }
                    ],
                    "anchors": [
                        "pandas.merge_join#practice",
                        "pandas.merge_join#assessment:predict_inner_merge_result"
                    ],
                    "public": {
                        "prompt": "The `orders` DataFrame has `customer_id` and the `customers` DataFrame has `customer_id`, `customer_name`, and `segment`. Use `.merge()` to join them on `customer_id` (inner join), then print the result.\n\nThe result should have one row per order whose `customer_id` also appears in customers, with the customer columns attached.\n\nUse only `orders.merge(customers, on='customer_id')`, `how='inner'`, `how='left'`, `how='right'`, `how='outer'`, and `print()`.",
                        "runtime": {
                            "kind": "python",
                            "version": "0.29.5",
                            "packages": ["pandas"]
                        },
                        "workspace": {
                            "files": [
                                {
                                    "path": "solution.py",
                                    "role": "editable",
                                    "language": "python",
                                    "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\ncustomers = pd.read_csv('customers.csv')\n\n# TODO: merge orders with customers on customer_id (inner join)\n\n# TODO: print the result\n"
                                }
                            ],
                            "entry": "solution.py",
                            "asset_mounts": [
                                {
                                    "asset_id": "ds_orders",
                                    "variant_id": None,
                                    "mount_path": "orders.csv"
                                },
                                {
                                    "asset_id": "ds_customers",
                                    "variant_id": None,
                                    "mount_path": "customers.csv"
                                }
                            ]
                        },
                        "constraints": {
                            "allowed_syntax": [
                                "orders.merge(customers, on='customer_id')",
                                "how='inner'",
                                "how='left'",
                                "how='right'",
                                "how='outer'",
                                "print()"
                            ],
                            "blocked_syntax": [
                                "pd.concat",
                                "df.join",
                                "SQL syntax",
                                "df.groupby",
                                "df.pivot_table"
                            ]
                        }
                    },
                    "grading": {
                        "solution_files": [
                            {
                                "path": "solution.py",
                                "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\ncustomers = pd.read_csv('customers.csv')\n\nresult = orders.merge(customers, on='customer_id')\n\nprint(result)\n"
                            }
                        ],
                        "tests": [
                            {
                                "test_id": "t1",
                                "kind": "dataframe_equals",
                                "spec": {
                                    "expr": "orders.merge(customers, on='customer_id')[['customer_id', 'customer_name', 'segment']]",
                                    "expected": {
                                        "columns": ["customer_id", "customer_name", "segment"],
                                        "rows": [
                                            [301, "Ngozi Eze", "Individual"], [302, "Emeka Obi", "Business"],
                                            [303, "Fatima Musa", "Individual"], [304, "Tunde Bakare", "Business"],
                                            [305, "Amaka Nwosu", "Individual"], [306, "Yusuf Garba", "Business"],
                                            [307, "Chisom Ike", "Individual"], [308, "Bisi Adewale", "Business"]
                                        ]
                                    }
                                },
                                "visible": True,
                                "message_on_fail": "The result should have one row per order with matching customer_id, with customer columns attached."
                            }
                        ]
                    },
                    "feedback": {
                        "correct": {
                            "message": "Perfect! You joined the two tables on the shared key."
                        },
                        "incorrect": {
                            "message": "Not quite. Make sure you use `orders.merge(customers, on='customer_id')` for an inner join."
                        },
                        "hints": [
                            "Use `orders.merge(customers, on='customer_id')` to join on the shared key."
                        ],
                        "remediation_step_id": "tile_pandas_concat_merge.r02"
                    }
                }
            }
        ]
    })
    
    # ===== tile_pandas_pivot_export =====
    tiles.append({
        "tile_id": "tile_pandas_pivot_export",
        "interactions": [
            # s04: check - pivot_table_reshaping
            {
                "step_id": "tile_pandas_pivot_export.s04",
                "interaction": {
                    "type": "choice",
                    "interaction_id": "ix.tile_pandas_pivot_export.s04",
                    "difficulty": "core",
                    "grading_mode": "client",
                    "standalone": False,
                    "measures": [
                        {
                            "concept_id": "pandas.pivot_table_reshaping",
                            "capability": "change_pivot_aggfunc",
                            "fact_ids": ["f3"]
                        }
                    ],
                    "anchors": ["pandas.pivot_table_reshaping#assessment:change_pivot_aggfunc"],
                    "public": {
                        "prompt": "You have a long-format table with duplicate product-month combinations. You want to pivot it so each cell shows the total sales (sum) for that product and month. Which `aggfunc` should you use?",
                        "options": [
                            {
                                "option_id": "opt_a",
                                "text": "`aggfunc='sum'`"
                            },
                            {
                                "option_id": "opt_b",
                                "text": "`aggfunc='mean'`"
                            },
                            {
                                "option_id": "opt_c",
                                "text": "`aggfunc='count'`"
                            },
                            {
                                "option_id": "opt_d",
                                "text": "No `aggfunc` needed; `pivot_table()` sums by default"
                            }
                        ],
                        "selection": "single",
                        "shuffle": True
                    },
                    "grading": {
                        "correct_option_ids": ["opt_a"],
                        "option_feedback": {
                            "opt_a": {
                                "message": "Correct. `aggfunc='sum'` combines duplicate rows by summing their values."
                            },
                            "opt_b": {
                                "message": "`aggfunc='mean'` computes the average, not the total. Use `aggfunc='sum'` to get the total sales."
                            },
                            "opt_c": {
                                "message": "`aggfunc='count'` counts the number of rows, not the sum of sales. Use `aggfunc='sum'` to get the total sales."
                            },
                            "opt_d": {
                                "message": "The default `aggfunc` is 'mean', not 'sum'. To get totals, pass `aggfunc='sum'`."
                            }
                        }
                    },
                    "feedback": {
                        "correct": {
                            "message": "Exactly right. `aggfunc='sum'` gives you totals."
                        },
                        "incorrect": {
                            "message": "Not quite. Review which `aggfunc` computes totals."
                        },
                        "hints": [
                            "Think about which aggregation function adds up all the values for each group."
                        ],
                        "remediation_step_id": "tile_pandas_pivot_export.r01"
                    }
                }
            },
            # s05: hands_on - pivot_table_reshaping practice
            {
                "step_id": "tile_pandas_pivot_export.s05",
                "interaction": {
                    "type": "code_exercise",
                    "interaction_id": "ix.tile_pandas_pivot_export.s05",
                    "difficulty": "core",
                    "grading_mode": "client",
                    "standalone": False,
                    "measures": [
                        {
                            "concept_id": "pandas.pivot_table_reshaping",
                            "capability": "build_pivot_table_from_index_columns_values",
                            "fact_ids": ["f1", "f2"]
                        }
                    ],
                    "anchors": [
                        "pandas.pivot_table_reshaping#practice",
                        "pandas.pivot_table_reshaping#assessment:build_pivot_table_from_index_columns_values"
                    ],
                    "public": {
                        "prompt": "The `product_sales` DataFrame has columns `product`, `month`, and `sales`, with some duplicate product-month rows. Use `pivot_table()` to reshape it to wide format with `index='product'`, `columns='month'`, `values='sales'`, and `aggfunc='sum'`. Print the result.\n\nThe result should have one row per product, one column per month, and each cell holding the total sales.\n\nUse only `df.pivot_table(index=..., columns=..., values=...)`, `aggfunc='sum'`, `aggfunc='mean'`, and `print()`.",
                        "runtime": {
                            "kind": "python",
                            "version": "0.29.5",
                            "packages": ["pandas"]
                        },
                        "workspace": {
                            "files": [
                                {
                                    "path": "solution.py",
                                    "role": "editable",
                                    "language": "python",
                                    "content": "import pandas as pd\n\nproduct_sales = pd.read_csv('product_sales.csv')\n\n# TODO: pivot_table with index='product', columns='month', values='sales', aggfunc='sum'\n\n# TODO: print the result\n"
                                }
                            ],
                            "entry": "solution.py",
                            "asset_mounts": [
                                {
                                    "asset_id": "ds_product_sales",
                                    "variant_id": None,
                                    "mount_path": "product_sales.csv"
                                }
                            ]
                        },
                        "constraints": {
                            "allowed_syntax": [
                                "df.pivot_table(index=..., columns=..., values=...)",
                                "aggfunc='sum'",
                                "aggfunc='mean'",
                                "print()"
                            ],
                            "blocked_syntax": [
                                "df.pivot",
                                "df.stack",
                                "df.unstack",
                                "pd.crosstab",
                                "margins=True"
                            ]
                        }
                    },
                    "grading": {
                        "solution_files": [
                            {
                                "path": "solution.py",
                                "content": "import pandas as pd\n\nproduct_sales = pd.read_csv('product_sales.csv')\n\nresult = product_sales.pivot_table(index='product', columns='month', values='sales', aggfunc='sum')\n\nprint(result)\n"
                            }
                        ],
                        "tests": [
                            {
                                "test_id": "t1",
                                "kind": "value_equals",
                                "spec": {
                                    "expr": "product_sales.pivot_table(index='product', columns='month', values='sales', aggfunc='sum').loc['Envelope', 'Jan']",
                                    "expected": 7700
                                },
                                "visible": True,
                                "message_on_fail": "The pivot table should have Envelope-Jan cell = 7700 (sum of 4500 + 3200)."
                            },
                            {
                                "test_id": "t2",
                                "kind": "value_equals",
                                "spec": {
                                    "expr": "product_sales.pivot_table(index='product', columns='month', values='sales', aggfunc='sum').loc['Parcel', 'Feb']",
                                    "expected": 16700
                                },
                                "visible": True,
                                "message_on_fail": "The pivot table should have Parcel-Feb cell = 16700 (sum of 7600 + 9100)."
                            }
                        ]
                    },
                    "feedback": {
                        "correct": {
                            "message": "Perfect! You reshaped the long table to wide format with aggregation."
                        },
                        "incorrect": {
                            "message": "Not quite. Make sure you use `aggfunc='sum'` to total the sales for each product-month."
                        },
                        "hints": [
                            "Use `product_sales.pivot_table(index='product', columns='month', values='sales', aggfunc='sum')` to reshape."
                        ],
                        "remediation_step_id": "tile_pandas_pivot_export.r01"
                    }
                }
            },
            # s07: check - export_to_csv
            {
                "step_id": "tile_pandas_pivot_export.s07",
                "interaction": {
                    "type": "choice",
                    "interaction_id": "ix.tile_pandas_pivot_export.s07",
                    "difficulty": "core",
                    "grading_mode": "client",
                    "standalone": False,
                    "measures": [
                        {
                            "concept_id": "pandas.export_to_csv",
                            "capability": "control_index_column_in_output",
                            "fact_ids": ["f2"]
                        }
                    ],
                    "anchors": ["pandas.export_to_csv#assessment:control_index_column_in_output"],
                    "public": {
                        "prompt": "You export a DataFrame to CSV with `orders.to_csv('output.csv')`. When you open the file, you see an extra column of row numbers (0, 1, 2, ...). How do you prevent this?",
                        "options": [
                            {
                                "option_id": "opt_a",
                                "text": "`orders.to_csv('output.csv', index=False)`"
                            },
                            {
                                "option_id": "opt_b",
                                "text": "`orders.to_csv('output.csv', header=False)`"
                            },
                            {
                                "option_id": "opt_c",
                                "text": "`orders.to_csv('output.csv', columns=False)`"
                            },
                            {
                                "option_id": "opt_d",
                                "text": "`orders.to_csv('output.csv', row_numbers=False)`"
                            }
                        ],
                        "selection": "single",
                        "shuffle": True
                    },
                    "grading": {
                        "correct_option_ids": ["opt_a"],
                        "option_feedback": {
                            "opt_a": {
                                "message": "Correct. `index=False` omits the row labels (index) from the output file."
                            },
                            "opt_b": {
                                "message": "`header=False` omits the column names, not the index. Use `index=False` to omit the row numbers."
                            },
                            "opt_c": {
                                "message": "There is no `columns=False` parameter. Use `index=False` to omit the row numbers."
                            },
                            "opt_d": {
                                "message": "There is no `row_numbers` parameter. Use `index=False` to omit the index."
                            }
                        }
                    },
                    "feedback": {
                        "correct": {
                            "message": "Exactly right. `index=False` omits the index from the CSV."
                        },
                        "incorrect": {
                            "message": "Not quite. Review which parameter controls whether the index is written."
                        },
                        "hints": [
                            "Think about which parameter controls whether the row labels are written to the file."
                        ],
                        "remediation_step_id": "tile_pandas_pivot_export.r02"
                    }
                }
            },
            # s08: hands_on - export_to_csv practice
            {
                "step_id": "tile_pandas_pivot_export.s08",
                "interaction": {
                    "type": "code_exercise",
                    "interaction_id": "ix.tile_pandas_pivot_export.s08",
                    "difficulty": "core",
                    "grading_mode": "client",
                    "standalone": False,
                    "measures": [
                        {
                            "concept_id": "pandas.export_to_csv",
                            "capability": "write_dataframe_to_csv",
                            "fact_ids": ["f1"]
                        },
                        {
                            "concept_id": "pandas.export_to_csv",
                            "capability": "control_index_column_in_output",
                            "fact_ids": ["f2"]
                        }
                    ],
                    "anchors": [
                        "pandas.export_to_csv#practice",
                        "pandas.export_to_csv#assessment:write_dataframe_to_csv",
                        "pandas.export_to_csv#assessment:control_index_column_in_output"
                    ],
                    "public": {
                        "prompt": "The `orders` DataFrame is loaded. Export it to a CSV file named `cleaned_orders.csv` with `index=False` (no row numbers), then read it back with `pd.read_csv()` and print the columns to verify.\n\nUse only `df.to_csv(path)`, `df.to_csv(path, index=False)`, `pd.read_csv(path) to check`, and `print()`.",
                        "runtime": {
                            "kind": "python",
                            "version": "0.29.5",
                            "packages": ["pandas"]
                        },
                        "workspace": {
                            "files": [
                                {
                                    "path": "solution.py",
                                    "role": "editable",
                                    "language": "python",
                                    "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\n# TODO: export orders to 'cleaned_orders.csv' with index=False\n\n# TODO: read it back and print the columns to verify\n"
                                }
                            ],
                            "entry": "solution.py",
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
                                "df.to_csv(path)",
                                "df.to_csv(path, index=False)",
                                "pd.read_csv(path) to check",
                                "print()"
                            ],
                            "blocked_syntax": [
                                "df.to_excel",
                                "df.to_json",
                                "sep=...",
                                "compression options"
                            ]
                        }
                    },
                    "grading": {
                        "solution_files": [
                            {
                                "path": "solution.py",
                                "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\norders.to_csv('cleaned_orders.csv', index=False)\n\nverify = pd.read_csv('cleaned_orders.csv')\nprint(verify.columns.tolist())\n"
                            }
                        ],
                        "tests": [
                            {
                                "test_id": "t1",
                                "kind": "value_equals",
                                "spec": {
                                    "expr": "'Unnamed' in str(pd.read_csv('cleaned_orders.csv').columns.tolist())",
                                    "expected": False
                                },
                                "visible": True,
                                "message_on_fail": "The CSV should not have an 'Unnamed' index column. Use index=False."
                            },
                            {
                                "test_id": "t2",
                                "kind": "value_equals",
                                "spec": {
                                    "expr": "len(pd.read_csv('cleaned_orders.csv').columns)",
                                    "expected": 10
                                },
                                "visible": True,
                                "message_on_fail": "The CSV should have 10 columns (the original columns, no extra index column)."
                            }
                        ]
                    },
                    "feedback": {
                        "correct": {
                            "message": "Perfect! You exported the DataFrame without the index column."
                        },
                        "incorrect": {
                            "message": "Not quite. Make sure you use `index=False` to omit the row numbers."
                        },
                        "hints": [
                            "Use `orders.to_csv('cleaned_orders.csv', index=False)` to export without the index."
                        ],
                        "remediation_step_id": "tile_pandas_pivot_export.r02"
                    }
                }
            }
        ]
    })
    
    return {
        "schema_version": "0.1.0",
        "kind": "interactions_part",
        "path_id": "data_analyst",
        "batch_id": "final_batch_009_da_pandas",
        "tiles": tiles
    }

if __name__ == "__main__":
    interactions = build_interactions()
    print(json.dumps(interactions, indent=2))
