# Appendix E: Example payloads

One real, complete interaction of each type used by the Data Analyst path (as stored in `interactions.json`: `public` goes to the player, `grading` stays server-side when `grading_mode` is `server`).

## `choice`
From `tile_data_shape_and_types` step `tile_data_shape_and_types.s03`.

```json
{
 "type": "choice",
 "interaction_id": "ix.tile_data_shape_and_types.s03",
 "difficulty": "intro",
 "grading_mode": "client",
 "standalone": false,
 "measures": [
  {
   "concept_id": "data.dataset_rows_columns",
   "capability": "identify_column_as_variable",
   "fact_ids": [
    "f4"
   ]
  }
 ],
 "anchors": [
  "data.dataset_rows_columns#assessment:identify_column_as_variable"
 ],
 "public": {
  "prompt": "In the Kwik Courier delivery table, what does the delivery_min column represent?",
  "options": [
   {
    "option_id": "opt_a",
    "text": "One delivery \u2014 the record for a single order"
   },
   {
    "option_id": "opt_b",
    "text": "One variable \u2014 the delivery time recorded for every order"
   },
   {
    "option_id": "opt_c",
    "text": "The entire dataset of all deliveries"
   },
   {
    "option_id": "opt_d",
    "text": "A summary statistic calculated from the table"
   }
  ],
  "selection": "single",
  "shuffle": true
 },
 "grading": {
  "correct_option_ids": [
   "opt_b"
  ],
  "option_feedback": {
   "opt_a": {
    "message": "That describes a row, not a column. A row holds all the information about one delivery; a column holds one kind of information across every delivery."
   },
   "opt_b": {
    "message": "Correct. A column represents one variable \u2014 one attribute recorded for every observation in the dataset."
   },
   "opt_c": {
    "message": "The dataset is the whole table, not a single column. A column is just one variable within that table."
   },
   "opt_d": {
    "message": "Columns hold raw values, not computed summaries. delivery_min stores the actual delivery time for each order."
   }
  }
 },
 "feedback": {
  "correct": {
   "message": "Exactly right. Each column is one variable \u2014 one attribute recorded across all observations."
  },
  "incorrect": {
   "message": "Not quite. Remember: a column runs top-to-bottom and holds one kind of information for every row."
  },
  "hints": [
   "Think about which direction a column runs in the table.",
   "Ask yourself: does delivery_min describe one delivery, or does it appear for every delivery?"
  ],
  "remediation_step_id": "tile_data_shape_and_types.r01"
 }
}
```

## `classify`
From `tile_data_shape_and_types` step `tile_data_shape_and_types.s07`.

```json
{
 "type": "classify",
 "interaction_id": "ix.tile_data_shape_and_types.s07",
 "difficulty": "stretch",
 "grading_mode": "client",
 "standalone": false,
 "measures": [
  {
   "concept_id": "data.categorical_numeric_types",
   "capability": "recognize_numeric_looking_categorical",
   "fact_ids": [
    "m1"
   ]
  }
 ],
 "anchors": [
  "data.categorical_numeric_types#practice",
  "data.categorical_numeric_types#assessment:recognize_numeric_looking_categorical"
 ],
 "public": {
  "prompt": "Drag each column name into the correct bucket. Use the arithmetic test: can you meaningfully add or subtract values in that column?",
  "buckets": [
   {
    "bucket_id": "bucket_categorical",
    "label": "Categorical"
   },
   {
    "bucket_id": "bucket_numerical",
    "label": "Numerical"
   }
  ],
  "items": [
   {
    "item_id": "item_city",
    "text": "city",
    "source": {
     "asset_id": "ds_courier_orders_base",
     "row": {
      "where": {
       "order_id": 1042
      },
      "occurrence": 0
     },
     "column": "city"
    }
   },
   {
    "item_id": "item_delivery_min",
    "text": "delivery_min",
    "source": {
     "asset_id": "ds_courier_orders_base",
     "row": {
      "where": {
       "order_id": 1042
      },
      "occurrence": 0
     },
     "column": "delivery_min"
    }
   },
   {
    "item_id": "item_driver",
    "text": "driver",
    "source": {
     "asset_id": "ds_courier_orders_base",
     "row": {
      "where": {
       "order_id": 1042
      },
      "occurrence": 0
     },
     "column": "driver"
    }
   },
   {
    "item_id": "item_zone_code",
    "text": "zone_code",
    "source": {
     "asset_id": "ds_courier_orders_base",
     "row": {
      "where": {
       "order_id": 1042
      },
      "occurrence": 0
     },
     "column": "zone_code"
    }
   }
  ]
 },
 "grading": {
  "assignments": {
   "item_city": "bucket_categorical",
   "item_delivery_min": "bucket_numerical",
   "item_driver": "bucket_categorical",
   "item_zone_code": "bucket_categorical"
  },
  "role_map": {
   "bucket_categorical": "categorical",
   "bucket_numerical": "numerical"
  },
  "item_feedback": {
   "item_city": {
    "message": "Correct. City values ('Lagos', 'Abuja', 'Kano') are labels \u2014 levels of a categorical variable. You cannot add or subtract city names."
   },
   "item_delivery_min": {
    "message": "Correct. Delivery time is numerical: 41 minutes minus 32 minutes is a meaningful 9-minute difference."
   },
   "item_driver": {
    "message": "Correct. Driver names are category labels. Adding 'Emeka Obi' and 'Fatima Bello' produces nothing meaningful."
   },
   "item_zone_code": {
    "message": "Correct \u2014 and this is the trap. zone_code holds digits (101, 102, 103) but adding two zone codes is meaningless. Stored as a number does not mean it is numerical."
   }
  }
 },
 "feedback": {
  "correct": {
   "message": "Excellent! You correctly classified all columns \u2014 including zone_code, which looks numerical but is actually a categorical label."
  },
  "incorrect": {
   "message": "Check your work. For each column, ask: would adding or subtracting two values produce a meaningful result? If not, it is categorical \u2014 even if the values look like numbers."
  },
  "hints": [
   "Apply the arithmetic test to each column: does adding or subtracting two values give a meaningful result?",
   "Pay close attention to zone_code \u2014 the values are digits, but ask whether zone 101 + zone 102 means anything."
  ],
  "remediation_step_id": "tile_data_shape_and_types.r02"
 }
}
```

## `code_exercise` (chart_renderer)
From `tile_capstone_stats_dashboard` step `tile_capstone_stats_dashboard.s10`.

```json
{
 "type": "code_exercise",
 "interaction_id": "ix.tile_capstone_stats_dashboard.s10",
 "difficulty": "stretch",
 "grading_mode": "client",
 "standalone": false,
 "measures": [
  {
   "concept_id": "capstone.building_dashboard_or_viz",
   "capability": "select_appropriate_multi_panel_layout_for_capstone_findings",
   "fact_ids": [
    "f1",
    "f2"
   ]
  }
 ],
 "anchors": [
  "capstone.building_dashboard_or_viz#practice"
 ],
 "public": {
  "prompt": "The DataFrame `df` is loaded from `orders.csv`. Three data summaries are prepared for you: `zone_counts`, `delivery_times`, and `zone_means`.\n\nBuild a single figure with three side-by-side panels:\n- Call `plt.subplot(131)` then use the current axes to create a bar chart\n- Call `plt.subplot(132)` then create a histogram\n- Call `plt.subplot(133)` then create another bar chart\n\nAdd titles to each panel and call `plt.suptitle('QuickRide Capstone Dashboard')` and `plt.tight_layout()` at the end.",
  "runtime": {
   "kind": "chart_renderer",
   "version": "0.29.5",
   "packages": [
    "pandas",
    "matplotlib",
    "seaborn"
   ]
  },
  "workspace": {
   "files": [
    {
     "path": "dashboard.py",
     "role": "editable",
     "language": "python",
     "content": "import pandas as pd\nimport matplotlib.pyplot as plt\n\ndf = pd.read_csv('orders.csv')\n\n# TODO: Create first panel with plt.subplot(131), then bar chart\n# TODO: Create second panel with plt.subplot(132), then histogram\n# TODO: Create third panel with plt.subplot(133), then bar chart\n# TODO: Add suptitle and tight_layout\n"
    }
   ],
   "entry": "dashboard.py",
   "asset_mounts": [
    {
     "asset_id": "ds_capstone_orders",
     "mount_path": "orders.csv"
    }
   ]
  },
  "constraints": {
   "allowed_syntax": [
    "plt.subplots(nrows, ncols)",
    "axs[row, col].plot(...)",
    "axs[row, col].bar(...)",
    "axs[row, col].hist(...)",
    "axs[row, col].set_title(...)",
    "plt.subplot(131)",
    "plt.subplot(132)",
    "plt.subplot(133)",
    "plt.suptitle(...)",
    "plt.tight_layout()",
    "plt.show()",
    "ax.set_xlabel(...)",
    "ax.set_ylabel(...)",
    "sns.barplot(..., ax=ax)",
    "sns.histplot(..., ax=ax)",
    "sns.boxplot(..., ax=ax)",
    "df['column'].value_counts()",
    "df.groupby(...).mean()",
    "import matplotlib.pyplot as plt",
    "import seaborn as sns"
   ],
   "blocked_syntax": []
  }
 },
 "grading": {
  "solution_files": [
   {
    "path": "dashboard.py",
    "content": "import pandas as pd\nimport matplotlib.pyplot as plt\n\ndf = pd.read_csv('orders.csv')\n\nax = plt.subplot(131)\ndf['zone'].value_counts().plot.bar(ax=ax)\nax.set_title('Orders per Zone')\n\nax = plt.subplot(132)\nax.hist(df['delivery_time'])\nax.set_title('Delivery Time Distribution')\n\nax = plt.subplot(133)\ndf.groupby('zone')['delivery_time'].mean().plot.bar(ax=ax)\nax.set_title('Mean Delivery Time per Zone')\n\nplt.suptitle('QuickRide Capstone Dashboard')\nplt.tight_layout()\n"
   }
  ],
  "tests": [
   {
    "test_id": "t_figure_structure",
    "kind": "figure_equals",
    "spec": {
     "expected": {
      "n_axes": 3
     }
    },
    "visible": true,
    "message_on_fail": "The figure should contain exactly 3 axes (one per panel). Make sure you call plt.subplot(131), plt.subplot(132), and plt.subplot(133)."
   },
   {
    "test_id": "t_panel3_title",
    "kind": "axes_property",
    "spec": {
     "property": "title",
     "expected": "Mean Delivery Time per Zone",
     "axes": 2
    },
    "visible": true,
    "message_on_fail": "Panel 3 (axes index 2) should have the title 'Mean Delivery Time per Zone'."
   },
   {
    "test_id": "t_zone_means_bars",
    "kind": "plotted_data_equals",
    "spec": {
     "chart": "bar",
     "field": "heights",
     "axes": 2,
     "sorted": false,
     "tolerance": 0.0001,
     "expected": [
      52.0,
      30.285714285714285,
      25.714285714285715,
      33.75
     ]
    },
    "visible": true,
    "message_on_fail": "Panel 3 bar heights should equal the mean delivery_time per zone from the data. Make sure you use df.groupby('zone')['delivery_time'].mean() for the bar heights."
   }
  ],
  "execution_provenance": {
   "runtime": "pyodide",
   "runtime_version": "0.29.5",
   "solution_sha256": "40fad29470ec3d2c90661bdd95160e2af3d579603af70eaad2feb6ba9731fb9d",
   "tests_passed": 3
  },
  "hidden_checks": [
   {
    "check_id": "hc_orders.csv_drop_first_t_zone_means_bars",
    "mutation": {
     "table": "orders.csv",
     "ops": [
      {
       "op": "drop_row",
       "index": 0
      }
     ]
    },
    "test_id": "t_zone_means_bars",
    "expected": {
     "value": [
      54.666666666666664,
      30.285714285714285,
      25.714285714285715,
      33.75
     ]
    },
    "ordered": false
   },
   {
    "check_id": "hc_orders.csv_dup_last_t_zone_means_bars",
    "mutation": {
     "table": "orders.csv",
     "ops": [
      {
       "op": "duplicate_row",
       "index": 33
      }
     ]
    },
    "test_id": "t_zone_means_bars",
    "expected": {
     "value": [
      52,
      30.285714285714285,
      25.714285714285715,
      34.666666666666664
     ]
    },
    "ordered": false
   },
   {
    "check_id": "hc_orders.csv_drop_last_t_zone_means_bars",
    "mutation": {
     "table": "orders.csv",
     "ops": [
      {
       "op": "drop_row",
       "index": 33
      }
     ]
    },
    "test_id": "t_zone_means_bars",
    "expected": {
     "value": [
      52,
      30.285714285714285,
      25.714285714285715,
      32.57142857142857
     ]
    },
    "ordered": false
   },
   {
    "check_id": "hc_orders.csv_null_zone_t_zone_means_bars",
    "mutation": {
     "table": "orders.csv",
     "ops": [
      {
       "op": "set_cell",
       "index": 0,
       "column": "zone",
       "value": null
      }
     ]
    },
    "test_id": "t_zone_means_bars",
    "expected": {
     "value": [
      54.666666666666664,
      30.285714285714285,
      25.714285714285715,
      33.75
     ]
    },
    "ordered": false
   }
  ]
 },
 "feedback": {
  "correct": {
   "message": "Excellent. Your dashboard shows three panels in one figure with a shared title \u2014 orders per zone, delivery time distribution, and mean delivery time per zone."
  },
  "incorrect": {
   "message": "Check that you have three plt.subplot() calls (131, 132, 133), each with a bar or hist chart and a title, and that plt.suptitle('QuickRide Capstone Dashboard') is called."
  },
  "hints": [
   "Call plt.subplot(131) before drawing the first chart, plt.subplot(132) before the second, and plt.subplot(133) before the third.",
   "For Panel 3: zone_means = df.groupby('zone')['delivery_time'].mean(); plt.bar(zone_means.index, zone_means.values)"
  ],
  "remediation_step_id": "tile_capstone_stats_dashboard.r03"
 }
}
```

## `code_exercise` (python)
From `tile_python_comprehensions_iterating` step `tile_python_comprehensions_iterating.s03`.

```json
{
 "type": "code_exercise",
 "interaction_id": "ix.tile_python_comprehensions_iterating.s03",
 "difficulty": "core",
 "grading_mode": "client",
 "standalone": false,
 "measures": [
  {
   "concept_id": "python.comprehensions",
   "capability": "write_list_comprehension",
   "fact_ids": [
    "f1",
    "f2"
   ]
  },
  {
   "concept_id": "python.comprehensions",
   "capability": "write_dict_comprehension",
   "fact_ids": [
    "f3"
   ]
  }
 ],
 "anchors": [
  "python.comprehensions#practice",
  "python.comprehensions#assessment:write_list_comprehension",
  "python.comprehensions#assessment:write_dict_comprehension"
 ],
 "public": {
  "prompt": "QuickDeliver wants to analyse delivery times.\n\n`numbers` and `threshold` are already assigned below.\n\n**Part 1 \u2014 list comprehension:** Assign to `squares` the squares of only the numbers in `numbers` that are divisible by `threshold`, in the original order. Use `x * x` as the expression and `x % threshold == 0` as the filter. Then `print(squares)`.\n\n**Part 2 \u2014 dict comprehension:** Assign to `sq_map` a dictionary that maps each number in `numbers` to its square (all numbers, no filter). Use `{x: x * x for x in numbers}`. Then `print(sq_map)`.\n\nExpected output:\n```\n[4, 16, 36, 64]\n{1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36, 7: 49, 8: 64}\n```",
  "runtime": {
   "kind": "python",
   "version": "0.29.5"
  },
  "workspace": {
   "files": [
    {
     "path": "solution.py",
     "role": "editable",
     "language": "python",
     "content": "numbers = [1, 2, 3, 4, 5, 6, 7, 8]\nthreshold = 2\n# Part 1: write your list comprehension, assign to squares, then print it\n# Part 2: write your dict comprehension, assign to sq_map, then print it\n"
    }
   ],
   "entry": "solution.py"
  },
  "constraints": {
   "allowed_syntax": [
    "name = value assignment",
    "using assigned names in an expression, as in the width * height example",
    "int, float, str and bool literals",
    "single- or double-quoted strings",
    "True / False",
    "print()",
    "type()",
    "+ - * / // % **",
    "parentheses for grouping",
    "< <= > >= == !=",
    "and",
    "or",
    "not",
    "int()",
    "float()",
    "str()",
    "[...] list literal",
    "list[i] and list[-1] indexing",
    "list[a:b] slicing",
    "list[i] = value",
    "list.append()",
    "len()",
    "{key: value} dictionary literal",
    "d[key] lookup and assignment",
    "d.get()",
    "key in d",
    "tuple literal with commas or parentheses",
    "unpacking a, b = t",
    "one-item tuple with trailing comma",
    "set()",
    "{...} set literal",
    "x in a_set",
    "| and & on sets",
    "quote mixing to embed a quote",
    "f-strings f\"...{expr}...\"",
    "format specifier such as {value:.2f}",
    "if",
    "elif",
    "else",
    "colon and indented block",
    "for item in sequence:",
    "while condition:",
    "break",
    "continue",
    "[expr for x in seq]",
    "[expr for x in seq if cond]",
    "{k: v for ...}"
   ],
   "blocked_syntax": [
    "for key in d:",
    "for k, v in d.items():",
    "def name():",
    "calling name()",
    "def f(a, b):",
    "positional arguments in a call",
    "return",
    "def f(a, b=default):",
    "keyword arguments f(name=value)",
    "global statement",
    "try:",
    "except ValueError:",
    "input()",
    "import module",
    "module.name",
    "from module import name",
    "open(file, mode)",
    "with open(...) as f:",
    "f.read()",
    "f.write()",
    "csv.DictReader",
    "csv.DictWriter",
    "newline=''",
    "range()",
    "+= and other augmented assignment",
    "enumerate()",
    "zip()",
    "lambda",
    "class definitions",
    "pandas / numpy"
   ]
  }
 },
 "grading": {
  "solution_files": [
   {
    "path": "solution.py",
    "content": "numbers = [1, 2, 3, 4, 5, 6, 7, 8]\nthreshold = 2\nsquares = [x * x for x in numbers if x % threshold == 0]\nprint(squares)\nsq_map = {x: x * x for x in numbers}\nprint(sq_map)\n"
   }
  ],
  "tests": [
   {
    "test_id": "t1_both_comps",
    "kind": "stdout_equals",
    "spec": {
     "expected": "[4, 16, 36, 64]\n{1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36, 7: 49, 8: 64}"
    },
    "visible": true,
    "message_on_fail": "Expected two lines of output. Line 1: `[4, 16, 36, 64]` (list comprehension of even squares). Line 2: `{1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36, 7: 49, 8: 64}` (dict comprehension mapping each number to its square)."
   }
  ],
  "execution_provenance": {
   "runtime": "pyodide",
   "runtime_version": "0.29.5",
   "solution_sha256": "894fbc6632323ef79ed34836fbdfcf783d891fc7c16268c623acd3399ccb9af5",
   "tests_passed": 1
  },
  "hidden_checks": [
   {
    "check_id": "hc_var_threshold_t1_both_comps",
    "mutation": {
     "ops": [
      {
       "op": "set_variable",
       "name": "threshold",
       "value": 9
      }
     ]
    },
    "test_id": "t1_both_comps",
    "expected": {
     "value": "[]\n{1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36, 7: 49, 8: 64}"
    },
    "ordered": false
   }
  ]
 },
 "feedback": {
  "correct": {
   "message": "Both comprehensions are correct. The list comprehension filtered to numbers divisible by `threshold` and squared each one; the dict comprehension mapped every number to its square."
  },
  "incorrect": {
   "message": "A list comprehension has the form `[expression for var in iterable if condition]`. A dict comprehension has the form `{key: value for var in iterable}`. Check both parts."
  },
  "hints": [
   "Part 1: `[x * x for x in numbers if x % threshold == 0]` \u2014 filter first, then square.",
   "Part 2: `{x: x * x for x in numbers}` \u2014 curly braces, `key: value` before the `for` clause, no filter."
  ],
  "remediation_step_id": "tile_python_comprehensions_iterating.r01"
 }
}
```

## `code_exercise` (spreadsheet)
From `tile_spreadsheet_aggregation_logical` step `tile_spreadsheet_aggregation_logical.s10`.

```json
{
 "type": "code_exercise",
 "interaction_id": "ix.tile_spreadsheet_aggregation_logical.s10",
 "difficulty": "stretch",
 "grading_mode": "client",
 "standalone": false,
 "measures": [
  {
   "concept_id": "spreadsheet.logical_functions",
   "capability": "construct_nested_if_for_multi_band_classification",
   "fact_ids": [
    "f1",
    "f2",
    "f6"
   ]
  },
  {
   "concept_id": "spreadsheet.logical_functions",
   "capability": "use_and_as_if_logical_test_for_multiple_conditions",
   "fact_ids": [
    "f3"
   ]
  },
  {
   "concept_id": "spreadsheet.logical_functions",
   "capability": "select_and_combine_if_and_or_for_given_decision_logic",
   "fact_ids": [
    "f1",
    "f3",
    "f4",
    "f5"
   ]
  },
  {
   "concept_id": "spreadsheet.logical_functions",
   "capability": "use_or_as_if_logical_test_for_any_condition",
   "fact_ids": [
    "f4"
   ]
  }
 ],
 "anchors": [
  "spreadsheet.logical_functions#practice",
  "spreadsheet.logical_functions#assessment:construct_nested_if_for_multi_band_classification",
  "spreadsheet.logical_functions#assessment:use_and_as_if_logical_test_for_multiple_conditions",
  "spreadsheet.logical_functions#assessment:use_or_as_if_logical_test_for_any_condition",
  "spreadsheet.logical_functions#assessment:select_and_combine_if_and_or_for_given_decision_logic"
 ],
 "public": {
  "prompt": "The **orders** sheet has delivery times in column C (rows 2\u20135). You need to classify each delivery into one of three bands:\n\n- **\"Late\"** if delivery_minutes > 60\n- **\"On Time\"** if delivery_minutes is between 30 and 60 (inclusive on both ends)\n- **\"Fast\"** if delivery_minutes < 30\n\n**Task 1 \u2014 nested IF with AND:** In cell F2, write a nested IF formula that classifies the delivery time in C2. Use **AND** as the logical_test of the inner IF to enforce both the lower bound (>=30) and the upper bound (<=60) of the \"On Time\" band. Then write the same formula in F3 and F4.\n\nExpected results:\n- F2: **\"Fast\"** (C2 = 28)\n- F3: **\"Fast\"** (C3 = 25)\n- F4: **\"On Time\"** (C4 = 56)\n\n**Task 2 \u2014 OR flag:** In cell F5, write an IF formula that returns **\"Extreme\"** if C5 is less than 20 **OR** greater than 70, and **\"Normal\"** otherwise. Use **OR** as the logical_test.\n\nExpected result:\n- F5: **\"Extreme\"** (C5 = 19)",
  "runtime": {
   "kind": "spreadsheet",
   "version": "3.4.0"
  },
  "workspace": {
   "files": [
    {
     "path": "book.sheet",
     "role": "editable",
     "language": "sheet",
     "content": "// The orders sheet has delivery_minutes in column C.\n// Input cells (typed constants - the gate will mutate these):\norders!C2: 28\norders!C3: 25\norders!C4: 56\norders!C5: 19\n\n// Task 1: In F2, write a nested IF formula that classifies C2 as:\n//   'Late'    if C2 > 60\n//   'On Time' if C2 >= 30 AND C2 <= 60  (use AND for both bounds)\n//   'Fast'    if C2 < 30\n// Then write the same pattern in F3 and F4.\n\n// Task 2: In F5, write an IF formula that returns 'Extreme' if\n//   C5 < 20 OR C5 > 70, and 'Normal' otherwise. Use OR.\n"
    }
   ],
   "entry": "book.sheet",
   "asset_mounts": [
    {
     "asset_id": "asset_orders_clean",
     "mount_path": "orders.csv"
    }
   ]
  },
  "constraints": {
   "allowed_syntax": [
    "IF(logical_test, value_if_true, value_if_false)",
    "AND(condition1, condition2)",
    "OR(condition1, condition2)",
    "comparison operators",
    "text in quotes",
    "numbers",
    "relative cell references"
   ],
   "blocked_syntax": [
    "IFS",
    "SWITCH",
    "CHOOSE"
   ]
  }
 },
 "grading": {
  "solution_files": [
   {
    "path": "book.sheet",
    "content": "// Input cells (typed constants):\norders!C2: 28\norders!C3: 25\norders!C4: 56\norders!C5: 19\n\n// Formula cells:\nF2: =IF(C2>60,\"Late\",IF(AND(C2>=30,C2<=60),\"On Time\",\"Fast\"))\nF3: =IF(C3>60,\"Late\",IF(AND(C3>=30,C3<=60),\"On Time\",\"Fast\"))\nF4: =IF(C4>60,\"Late\",IF(AND(C4>=30,C4<=60),\"On Time\",\"Fast\"))\nF5: =IF(OR(C5<20,C5>70),\"Extreme\",\"Normal\")\n"
   }
  ],
  "tests": [
   {
    "test_id": "test_f2_fast",
    "kind": "cell_equals",
    "spec": {
     "cell": "F2",
     "expected": "Fast"
    },
    "visible": true,
    "message_on_fail": "F2 should be \"Fast\" because C2=28 is less than 30. Check the order of your IF conditions: test >60 first, then AND(>=30,<=60), then the else is Fast."
   },
   {
    "test_id": "test_f3_fast",
    "kind": "cell_equals",
    "spec": {
     "cell": "F3",
     "expected": "Fast"
    },
    "visible": true,
    "message_on_fail": "F3 should be \"Fast\" because C3=25 is less than 30. Check the order of your IF conditions: test >60 first, then AND(>=30,<=60), then the else is Fast."
   },
   {
    "test_id": "test_f4_on_time",
    "kind": "cell_equals",
    "spec": {
     "cell": "F4",
     "expected": "On Time"
    },
    "visible": true,
    "message_on_fail": "F4 should be \"On Time\" because C4=56 is between 30 and 60. Use AND(C4>=30,C4<=60) as the logical_test of the inner IF."
   },
   {
    "test_id": "test_f2_uses_if_and",
    "kind": "formula_uses",
    "spec": {
     "cell": "F2",
     "functions": [
      "IF",
      "AND"
     ]
    },
    "visible": true,
    "message_on_fail": "F2 must use both IF and AND. Use AND(C2>=30,C2<=60) as the logical_test of the inner IF to enforce both bounds of the 'On Time' band."
   },
   {
    "test_id": "test_f5_extreme",
    "kind": "cell_equals",
    "spec": {
     "cell": "F5",
     "expected": "Extreme"
    },
    "visible": true,
    "message_on_fail": "F5 should be \"Extreme\" because C5=19 is less than 20. Use =IF(OR(C5<20,C5>70),\"Extreme\",\"Normal\"). OR returns TRUE when any condition is met."
   },
   {
    "test_id": "test_f5_uses_or",
    "kind": "formula_uses",
    "spec": {
     "cell": "F5",
     "functions": [
      "IF",
      "OR"
     ]
    },
    "visible": true,
    "message_on_fail": "F5 must use both IF and OR. Use OR(C5<20,C5>70) as the logical_test: OR returns TRUE when any one of its conditions is TRUE."
   }
  ],
  "execution_provenance": {
   "runtime": "hyperformula",
   "runtime_version": "3.4.0",
   "solution_sha256": "cc956c65595c48ba85b924789c089efc2422155b0035bf84d05febdb1d045359",
   "tests_passed": 6
  },
  "hidden_checks": [
   {
    "check_id": "hc_cell_C2_test_f2_fast",
    "mutation": {
     "ops": [
      {
       "op": "set_variable",
       "name": "orders!C2",
       "value": 35
      }
     ]
    },
    "test_id": "test_f2_fast",
    "expected": {
     "value": "On Time"
    }
   },
   {
    "check_id": "hc_cell_C3_test_f3_fast",
    "mutation": {
     "ops": [
      {
       "op": "set_variable",
       "name": "orders!C3",
       "value": 32
      }
     ]
    },
    "test_id": "test_f3_fast",
    "expected": {
     "value": "On Time"
    }
   },
   {
    "check_id": "hc_cell_C4_test_f4_on_time",
    "mutation": {
     "ops": [
      {
       "op": "set_variable",
       "name": "orders!C4",
       "value": 63
      }
     ]
    },
    "test_id": "test_f4_on_time",
    "expected": {
     "value": "Late"
    }
   },
   {
    "check_id": "hc_cell_C5_test_f5_extreme",
    "mutation": {
     "ops": [
      {
       "op": "set_variable",
       "name": "orders!C5",
       "value": 26
      }
     ]
    },
    "test_id": "test_f5_extreme",
    "expected": {
     "value": "Normal"
    }
   }
  ]
 },
 "feedback": {
  "correct": {
   "message": "Well done! Your nested IF correctly classifies all three delivery times using AND for the On Time band. AND returns TRUE only when BOTH conditions are met. Your OR formula in F5 correctly flags C5=19 as Extreme because OR returns TRUE when ANY condition is met (19 < 20 is TRUE)."
  },
  "incorrect": {
   "message": "For F2\u2013F4: use =IF(C2>60,\"Late\",IF(AND(C2>=30,C2<=60),\"On Time\",\"Fast\")). AND requires BOTH bounds to be true. For F5: use =IF(OR(C5<20,C5>70),\"Extreme\",\"Normal\"). OR returns TRUE when ANY condition is true."
  },
  "hints": [
   "Start with the outer IF: =IF(C2>60,\"Late\", ...). Then nest another IF for the middle band.",
   "AND(C2>=30,C2<=60) returns TRUE only when C2 is at least 30 AND at most 60."
  ],
  "remediation_step_id": "tile_spreadsheet_aggregation_logical.r02"
 }
}
```

## `code_exercise` (sql)
From `tile_sql_fund_alias_distinct` step `tile_sql_fund_alias_distinct.s04`.

```json
{
 "type": "code_exercise",
 "interaction_id": "ix.tile_sql_fund_alias_distinct.s04",
 "difficulty": "core",
 "grading_mode": "client",
 "standalone": false,
 "measures": [
  {
   "concept_id": "sql.aliasing",
   "capability": "alias_a_table_and_use_the_alias",
   "fact_ids": [
    "f1",
    "f2"
   ]
  },
  {
   "concept_id": "sql.aliasing",
   "capability": "qualify_and_alias_columns_correctly",
   "fact_ids": [
    "f3",
    "f4"
   ]
  }
 ],
 "anchors": [
  "sql.aliasing#practice",
  "sql.aliasing#assessment:alias_a_table_and_use_the_alias",
  "sql.aliasing#assessment:qualify_and_alias_columns_correctly"
 ],
 "public": {
  "prompt": "Write a query against the orders table that: (1) gives orders the alias o using AS, (2) qualifies every column reference with o, and (3) renames delivery_time_minutes to delivery_min using AS. Return all three columns \u2014 order_id, customer_id, delivery_min \u2014 in that order. Do not filter or sort.",
  "runtime": {
   "kind": "sql",
   "version": "1.32.0"
  },
  "workspace": {
   "files": [
    {
     "path": "query.sql",
     "role": "editable",
     "language": "sql",
     "content": "-- Give the orders table the alias o.\n-- Qualify every column with o (e.g. o.order_id).\n-- Rename delivery_time_minutes to delivery_min using AS.\n-- Return: order_id, customer_id, delivery_min\n"
    }
   ],
   "entry": "query.sql",
   "asset_mounts": [
    {
     "asset_id": "ds.orders",
     "mount_path": "orders"
    }
   ]
  },
  "constraints": {
   "allowed_syntax": [
    "SELECT",
    "FROM",
    "AS output_name",
    "* and table_name.*",
    "table alias (FROM table AS alias)",
    "alias.column qualification"
   ],
   "blocked_syntax": [
    "DISTINCT",
    "ALL",
    "WHERE",
    "< > <= >= = <> !=",
    "AND",
    "OR",
    "NOT",
    "parentheses",
    "IS NULL",
    "IS NOT NULL",
    "ORDER BY",
    "ASC",
    "DESC",
    "LIMIT",
    "OFFSET",
    "COUNT",
    "SUM",
    "AVG",
    "MIN",
    "MAX",
    "GROUP BY",
    "HAVING",
    "CASE WHEN ... THEN ... ELSE ... END",
    "LOWER",
    "UPPER",
    "TRIM",
    "CONCAT",
    "LENGTH",
    "EXTRACT(field FROM source)",
    "date - date",
    "CAST(expression AS type)",
    "expression::type",
    "COALESCE",
    "UNION",
    "UNION ALL",
    "JOIN / INNER JOIN",
    "ON",
    "USING",
    "ON with AND across several columns",
    "USING (a, b)",
    "LEFT JOIN",
    "RIGHT JOIN",
    "FULL JOIN",
    "OUTER keyword",
    "subquery in WHERE",
    "IN (SELECT ...)",
    "subquery in FROM with an alias",
    "WITH name AS (...)",
    "window functions (OVER)",
    "EXISTS",
    "correlated subqueries",
    "CROSS JOIN",
    "self-joins"
   ]
  }
 },
 "grading": {
  "solution_files": [
   {
    "path": "query.sql",
    "content": "SELECT o.order_id, o.customer_id, o.delivery_time_minutes AS delivery_min\nFROM orders AS o;\n"
   }
  ],
  "tests": [
   {
    "test_id": "test_columns_and_rows",
    "kind": "query_result_equals",
    "spec": {
     "expected": {
      "columns": [
       "order_id",
       "customer_id",
       "delivery_min"
      ],
      "rows": [
       [
        1001,
        1,
        42
       ],
       [
        1002,
        2,
        31
       ],
       [
        1003,
        3,
        55
       ],
       [
        1004,
        4,
        28
       ],
       [
        1005,
        5,
        67
       ],
       [
        1006,
        6,
        19
       ],
       [
        1007,
        7,
        83
       ],
       [
        1008,
        8,
        45
       ],
       [
        1009,
        1,
        38
       ],
       [
        1010,
        3,
        72
       ]
      ]
     },
     "ordered": false
    },
    "visible": true,
    "message_on_fail": "Your result should have columns order_id, customer_id, delivery_min (in that order) with 10 rows. Make sure you alias the table as o, qualify all columns with o., and rename delivery_time_minutes to delivery_min."
   },
   {
    "test_id": "test_no_distinct",
    "kind": "forbidden_syntax",
    "spec": {
     "descriptors": [
      "DISTINCT"
     ]
    },
    "visible": false,
    "message_on_fail": "Do not use DISTINCT in this exercise."
   }
  ],
  "execution_provenance": {
   "runtime": "duckdb-wasm",
   "runtime_version": "1.32.0",
   "solution_sha256": "d0342c929226ebd22279adf96b129d64321c4b1d60a75ee3cea0497b8e8e52e5",
   "tests_passed": 2
  },
  "hidden_checks": [
   {
    "check_id": "hc_orders_drop_first",
    "mutation": {
     "table": "orders",
     "ops": [
      {
       "op": "drop_row",
       "index": 0
      }
     ]
    },
    "expected": {
     "columns": [
      "order_id",
      "customer_id",
      "delivery_min"
     ],
     "rows": [
      [
       1002,
       2,
       31
      ],
      [
       1003,
       3,
       55
      ],
      [
       1004,
       4,
       28
      ],
      [
       1005,
       5,
       67
      ],
      [
       1006,
       6,
       19
      ],
      [
       1007,
       7,
       83
      ],
      [
       1008,
       8,
       45
      ],
      [
       1009,
       1,
       38
      ],
      [
       1010,
       3,
       72
      ]
     ]
    },
    "ordered": false
   },
   {
    "check_id": "hc_orders_dup_last",
    "mutation": {
     "table": "orders",
     "ops": [
      {
       "op": "duplicate_row",
       "index": 9
      }
     ]
    },
    "expected": {
     "columns": [
      "order_id",
      "customer_id",
      "delivery_min"
     ],
     "rows": [
      [
       1001,
       1,
       42
      ],
      [
       1002,
       2,
       31
      ],
      [
       1003,
       3,
       55
      ],
      [
       1004,
       4,
       28
      ],
      [
       1005,
       5,
       67
      ],
      [
       1006,
       6,
       19
      ],
      [
       1007,
       7,
       83
      ],
      [
       1008,
       8,
       45
      ],
      [
       1009,
       1,
       38
      ],
      [
       1010,
       3,
       72
      ],
      [
       1010,
       3,
       72
      ]
     ]
    },
    "ordered": false
   },
   {
    "check_id": "hc_orders_drop_last",
    "mutation": {
     "table": "orders",
     "ops": [
      {
       "op": "drop_row",
       "index": 9
      }
     ]
    },
    "expected": {
     "columns": [
      "order_id",
      "customer_id",
      "delivery_min"
     ],
     "rows": [
      [
       1001,
       1,
       42
      ],
      [
       1002,
       2,
       31
      ],
      [
       1003,
       3,
       55
      ],
      [
       1004,
       4,
       28
      ],
      [
       1005,
       5,
       67
      ],
      [
       1006,
       6,
       19
      ],
      [
       1007,
       7,
       83
      ],
      [
       1008,
       8,
       45
      ],
      [
       1009,
       1,
       38
      ]
     ]
    },
    "ordered": false
   },
   {
    "check_id": "hc_orders_null_order_id",
    "mutation": {
     "table": "orders",
     "ops": [
      {
       "op": "set_cell",
       "index": 0,
       "column": "order_id",
       "value": null
      }
     ]
    },
    "expected": {
     "columns": [
      "order_id",
      "customer_id",
      "delivery_min"
     ],
     "rows": [
      [
       null,
       1,
       42
      ],
      [
       1002,
       2,
       31
      ],
      [
       1003,
       3,
       55
      ],
      [
       1004,
       4,
       28
      ],
      [
       1005,
       5,
       67
      ],
      [
       1006,
       6,
       19
      ],
      [
       1007,
       7,
       83
      ],
      [
       1008,
       8,
       45
      ],
      [
       1009,
       1,
       38
      ],
      [
       1010,
       3,
       72
      ]
     ]
    },
    "ordered": false
   }
  ]
 },
 "feedback": {
  "correct": {
   "message": "Well done. FROM orders AS o assigns the alias, o.column_name qualifies each reference, and AS delivery_min renames the output column. The alias replaces the original table name for the whole query."
  },
  "incorrect": {
   "message": "Assign the alias in FROM (orders AS o), then use o. before every column name in the SELECT list. Rename delivery_time_minutes with AS delivery_min."
  },
  "hints": [
   "Start with FROM orders AS o, then write SELECT o.order_id, o.customer_id, ...",
   "To rename a column in the output, write the column expression followed by AS and the new name."
  ],
  "remediation_step_id": "tile_sql_fund_alias_distinct.r02"
 }
}
```

## `external_proof`
From `tile_stakeholder_presentation_structure` step `tile_stakeholder_presentation_structure.s07`.

```json
{
 "type": "external_proof",
 "interaction_id": "ix.tile_stakeholder_presentation_structure.s07",
 "difficulty": "core",
 "grading_mode": "client",
 "standalone": false,
 "measures": [
  {
   "concept_id": "stakeholder.executive_summary_writing",
   "capability": "identify_executive_summary_purpose_and_scope",
   "fact_ids": [
    "f1"
   ]
  },
  {
   "concept_id": "stakeholder.executive_summary_writing",
   "capability": "construct_title_and_narrative_arc_for_executive_summary",
   "fact_ids": [
    "f2"
   ]
  },
  {
   "concept_id": "stakeholder.executive_summary_writing",
   "capability": "apply_section_headers_and_prose_structure_over_bullets",
   "fact_ids": [
    "f3"
   ]
  },
  {
   "concept_id": "stakeholder.executive_summary_writing",
   "capability": "write_executive_summary_covering_findings_and_recommendation",
   "fact_ids": [
    "f1",
    "f2",
    "f3"
   ]
  }
 ],
 "anchors": [
  "stakeholder.executive_summary_writing#practice",
  "stakeholder.executive_summary_writing#assessment:identify_executive_summary_purpose_and_scope",
  "stakeholder.executive_summary_writing#assessment:construct_title_and_narrative_arc_for_executive_summary",
  "stakeholder.executive_summary_writing#assessment:apply_section_headers_and_prose_structure_over_bullets",
  "stakeholder.executive_summary_writing#assessment:write_executive_summary_covering_findings_and_recommendation"
 ],
 "public": {
  "instruction": "Using the Lagos scenario below, write a brief executive summary with a title, a Finding section (one sentence), and a Recommendation section (one sentence). Your summary should:\n\u2022 Have a title that states the main takeaway\n\u2022 Include a 'Finding' section header followed by one sentence describing the delivery-time problem\n\u2022 Include a 'Recommendation' section header followed by one sentence proposing the second hub\n\u2022 Use prose (not bullets)\n\u2022 Be concise (approximately 50\u201375 words total)",
  "evidence_kinds": [
   "text"
  ],
  "checklist": [
   "Title states the main takeaway",
   "Includes 'Finding' section with problem description",
   "Includes 'Recommendation' section with proposed solution",
   "Uses prose structure (not bullets)",
   "Concise and focused (50\u201375 words)"
  ]
 },
 "grading": {
  "mode": "rubric_ai",
  "rubric": [
   {
    "criterion": "Title states main takeaway (e.g., 'Second Lagos Hub Needed to Meet Delivery Targets')",
    "weight": 1.0
   },
   {
    "criterion": "Includes a 'Finding' section header followed by a sentence describing the delivery-time problem",
    "weight": 1.0
   },
   {
    "criterion": "Includes a 'Recommendation' section header followed by a sentence proposing the second hub",
    "weight": 1.0
   },
   {
    "criterion": "Uses prose paragraphs rather than bullet points",
    "weight": 1.0
   },
   {
    "criterion": "The summary is concise (approximately 50\u201375 words) and focused on the key points",
    "weight": 1.0
   }
  ]
 },
 "feedback": {
  "correct": {
   "message": "Excellent work. Your executive summary follows the taught structure with a takeaway title, section headers, and prose paragraphs."
  },
  "incorrect": {
   "message": "Review the structure: a takeaway title, 'Finding' and 'Recommendation' section headers, and prose paragraphs (not bullets)."
  },
  "hints": [
   "Start with a title that states the main takeaway, not just a description.",
   "Use section headers ('Finding' and 'Recommendation') to organize your content.",
   "Write in prose paragraphs, not bullet points.",
   "Keep it concise \u2014 aim for 50\u201375 words total."
  ]
 }
}
```

## `find_issues`
From `tile_datamodel_normalization_many_to_many` step `tile_datamodel_normalization_many_to_many.s04`.

```json
{
 "type": "find_issues",
 "interaction_id": "ix.tile_datamodel_normalization_many_to_many.s04",
 "difficulty": "core",
 "grading_mode": "client",
 "standalone": false,
 "measures": [
  {
   "concept_id": "datamodel.normalization_basics",
   "capability": "identify_redundancy_and_its_update_problem",
   "fact_ids": [
    "f1",
    "f2"
   ]
  },
  {
   "concept_id": "datamodel.normalization_basics",
   "capability": "split_a_table_to_remove_redundancy",
   "fact_ids": [
    "f3"
   ]
  }
 ],
 "anchors": [
  "datamodel.normalization_basics#practice",
  "datamodel.normalization_basics#assessment:identify_redundancy_and_its_update_problem",
  "datamodel.normalization_basics#assessment:split_a_table_to_remove_redundancy"
 ],
 "public": {
  "asset_ref": {
   "asset_id": "ds_customers",
   "variant_id": "ds_customers.with_duplicate",
   "columns": [
    "customer_id",
    "name",
    "city"
   ]
  },
  "instructions": "The table below shows a customers table where a data entry error has introduced a duplicate row. Flag the cell that reveals the redundancy problem \u2014 the repeated customer_id that would cause an update anomaly if the customer's details changed.",
  "categories": [
   {
    "category_id": "cat_redundant_row",
    "label": "Redundant row \u2014 update anomaly risk"
   },
   {
    "category_id": "cat_clean",
    "label": "Clean \u2014 no redundancy issue"
   }
  ],
  "goal_count": 1
 },
 "grading": {
  "issues": [
   {
    "issue_id": "issue_duplicate_customer",
    "category_id": "cat_redundant_row",
    "locations": [
     {
      "where": {
       "customer_id": 1
      },
      "column": "customer_id",
      "occurrence": 0
     },
     {
      "where": {
       "customer_id": 1
      },
      "column": "customer_id",
      "occurrence": 1
     }
    ],
    "explanation": "customer_id 1 appears twice. This duplicate row means that if Amara Okafor's city changes, both rows must be updated \u2014 missing one creates an update anomaly where the same customer appears to live in two different cities."
   }
  ],
  "decoys": [
   {
    "location": {
     "where": {
      "customer_id": 2
     },
     "column": "customer_id",
     "occurrence": 0
    },
    "message": "customer_id 2 (Emeka Nwosu) appears only once \u2014 no redundancy here."
   },
   {
    "location": {
     "where": {
      "customer_id": 3
     },
     "column": "customer_id",
     "occurrence": 0
    },
    "message": "customer_id 3 (Fatima Bello) appears only once \u2014 no redundancy here."
   }
  ],
  "wrong_category_message": "You found the duplicate row, but check the category. A repeated customer_id is a redundancy problem \u2014 it creates an update anomaly risk, not a clean record.",
  "completion_message": "Well done. You identified the duplicate row for customer_id 1. Storing the same customer twice means any update to their details must be applied to both rows \u2014 missing one leaves inconsistent data."
 },
 "feedback": {
  "correct": {
   "message": "Correct. The duplicate row for customer_id 1 is the redundancy problem. If the customer's city changes, both rows must be updated \u2014 missing one creates an update anomaly."
  },
  "incorrect": {
   "message": "Look for a customer_id that appears more than once. That repeated row is the redundancy that normalization removes."
  },
  "hints": [
   "Scan the customer_id column for any value that appears more than once.",
   "A redundant row means the same customer's details are stored twice \u2014 what happens if their city changes?"
  ],
  "remediation_step_id": "tile_datamodel_normalization_many_to_many.r01"
 }
}
```

## `formula_entry`
From `tile_capstone_integrate_tools_model` step `tile_capstone_integrate_tools_model.s11`.

```json
{
 "type": "formula_entry",
 "interaction_id": "ix.tile_capstone_integrate_tools_model.s11",
 "difficulty": "stretch",
 "grading_mode": "client",
 "standalone": false,
 "measures": [
  {
   "concept_id": "capstone.integrate_spreadsheet",
   "capability": "apply_countifs_with_multiple_criteria_ranges",
   "fact_ids": [
    "f2"
   ]
  }
 ],
 "anchors": [
  "capstone.integrate_spreadsheet#assessment:apply_countifs_with_multiple_criteria_ranges"
 ],
 "public": {
  "prompt": "The capstone delivery sheet is loaded with zone in column A, shift in column B, and delivery_time in column C (header in row 1, data in rows 2\u201337). In cell E2, write a COUNTIFS formula that counts the rows where zone is 'Ikeja' AND delivery_time is greater than 45.",
  "asset_ref": {
   "asset_id": "ds_capstone_delivery_sheet",
   "columns": [
    "zone",
    "shift",
    "delivery_time"
   ]
  },
  "sheet_name": "ds_capstone_delivery_sheet",
  "target_cell": "E2"
 },
 "grading": {
  "expected_value": 2,
  "reference_formula": "=COUNTIFS(A2:A37,\"Ikeja\",C2:C37,\">45\")",
  "must_use_functions": [
   "COUNTIFS"
  ]
 },
 "feedback": {
  "correct": {
   "message": "Correct. COUNTIFS(A2:A37,\"Ikeja\",C2:C37,\">45\") counts the 2 Ikeja deliveries that took more than 45 minutes."
  },
  "incorrect": {
   "message": "Check that you are using COUNTIFS (not COUNTIF), that the zone range is A2:A37 with criterion \"Ikeja\", and that the delivery_time range is C2:C37 with criterion \">45\"."
  },
  "hints": [
   "COUNTIFS takes pairs: (criteria_range1, criteria1, criteria_range2, criteria2). Your first pair checks zone; your second pair checks delivery_time.",
   "The criterion for 'greater than 45' is written as the text string \">45\" inside the formula."
  ],
  "remediation_step_id": "tile_capstone_integrate_tools_model.r03"
 }
}
```

## `ordering`
From `tile_stakeholder_presentation_structure` step `tile_stakeholder_presentation_structure.s04`.

```json
{
 "type": "ordering",
 "interaction_id": "ix.tile_stakeholder_presentation_structure.s04",
 "difficulty": "intro",
 "grading_mode": "client",
 "standalone": false,
 "measures": [
  {
   "concept_id": "stakeholder.presentation_structure_basics",
   "capability": "organize_findings_into_opening_body_call_to_action",
   "fact_ids": [
    "f1",
    "f2"
   ]
  },
  {
   "concept_id": "stakeholder.presentation_structure_basics",
   "capability": "place_call_to_action_after_context_is_established",
   "fact_ids": [
    "f2",
    "f3"
   ]
  }
 ],
 "anchors": [
  "stakeholder.presentation_structure_basics#practice",
  "stakeholder.presentation_structure_basics#assessment:organize_findings_into_opening_body_call_to_action",
  "stakeholder.presentation_structure_basics#assessment:place_call_to_action_after_context_is_established"
 ],
 "public": {
  "prompt": "Drag the five Lagos presentation elements into the correct opening\u2013body\u2013call-to-action order.",
  "items": [
   {
    "item_id": "item_context",
    "text": "QuickShip's Lagos operations have grown 40% in the past year"
   },
   {
    "item_id": "item_problem",
    "text": "40% of deliveries now exceed the 60-minute target"
   },
   {
    "item_id": "item_evidence",
    "text": "Eastern districts average 78 minutes, 18 minutes over target"
   },
   {
    "item_id": "item_solution",
    "text": "A second hub in the eastern zone would reduce average delivery time to 42 minutes"
   },
   {
    "item_id": "item_action",
    "text": "We recommend approving the second hub by end of quarter"
   }
  ]
 },
 "grading": {
  "correct_order": [
   "item_context",
   "item_problem",
   "item_evidence",
   "item_solution",
   "item_action"
  ]
 },
 "feedback": {
  "correct": {
   "message": "Perfect. You organized the elements into the correct structure: opening (context + problem), body (evidence + solution), and call to action (request)."
  },
  "incorrect": {
   "message": "Think about the three-part structure. The opening establishes context, the body presents findings and evidence, and the end states what is being asked."
  },
  "hints": [
   "Start with context to establish the situation.",
   "Present the problem and evidence in the middle.",
   "End with the solution and what you are asking for."
  ]
 }
}
```

## `table_select`
From `tile_data_shape_and_types` step `tile_data_shape_and_types.s04`.

```json
{
 "type": "table_select",
 "interaction_id": "ix.tile_data_shape_and_types.s04",
 "difficulty": "core",
 "grading_mode": "client",
 "standalone": false,
 "measures": [
  {
   "concept_id": "data.dataset_rows_columns",
   "capability": "describe_dataset_structure",
   "fact_ids": [
    "f1",
    "f2"
   ]
  },
  {
   "concept_id": "data.dataset_rows_columns",
   "capability": "identify_row_as_observation",
   "fact_ids": [
    "f3"
   ]
  },
  {
   "concept_id": "data.dataset_rows_columns",
   "capability": "identify_column_as_variable",
   "fact_ids": [
    "f4"
   ]
  }
 ],
 "anchors": [
  "data.dataset_rows_columns#practice",
  "data.dataset_rows_columns#assessment:describe_dataset_structure",
  "data.dataset_rows_columns#assessment:identify_row_as_observation",
  "data.dataset_rows_columns#assessment:identify_column_as_variable"
 ],
 "public": {
  "asset_ref": {
   "asset_id": "ds_courier_orders_base",
   "variant_id": null,
   "columns": [
    "order_id",
    "city",
    "delivery_min",
    "driver"
   ],
   "max_rows": 4
  },
  "intro": "Use the Kwik Courier delivery table to answer each question by clicking the correct part of the table.",
  "tasks": [
   {
    "task_id": "task_row_1043",
    "prompt": "Click the row that is the observation for order #1043.",
    "target_kind": "row"
   },
   {
    "task_id": "task_col_city",
    "prompt": "Click the column that holds the destination city for every delivery.",
    "target_kind": "column"
   },
   {
    "task_id": "task_col_delivery_min",
    "prompt": "Click the column that is the variable for delivery time.",
    "target_kind": "column"
   }
  ]
 },
 "grading": {
  "answers": [
   {
    "task_id": "task_row_1043",
    "row": {
     "where": {
      "order_id": 1043
     },
     "occurrence": 0
    }
   },
   {
    "task_id": "task_col_city",
    "column": "city"
   },
   {
    "task_id": "task_col_delivery_min",
    "column": "delivery_min"
   }
  ],
  "task_feedback": {
   "task_row_1043": {
    "correct": "Right \u2014 that entire row is the observation for order #1043, one record of one delivery.",
    "incorrect": "Look for the row where order_id is 1043. Each row is one observation \u2014 one delivery record."
   },
   "task_col_city": {
    "correct": "Correct. The city column runs down the whole table and holds the destination city for every delivery.",
    "incorrect": "A column runs top-to-bottom and holds one kind of information across all rows. Look for the column labelled 'city'."
   },
   "task_col_delivery_min": {
    "correct": "Correct. delivery_min is the variable that records delivery time for every order.",
    "incorrect": "A variable is a column \u2014 it holds one kind of information for every observation. Look for the column labelled 'delivery_min'."
   }
  }
 },
 "feedback": {
  "correct": {
   "message": "Well done! You correctly identified a row as one observation and a column as one variable across all observations."
  },
  "incorrect": {
   "message": "Not all selections were right. Remember: a row is one delivery record; a column is one attribute recorded for every delivery."
  },
  "hints": [
   "Rows run left-to-right and describe one delivery. Columns run top-to-bottom and describe one attribute.",
   "Find the row where order_id matches 1043, and the column whose header matches the attribute you need."
  ],
  "remediation_step_id": "tile_data_shape_and_types.r01"
 }
}
```

## One explainer step with its blocks (shape of the non-interactive content)

```json
{
 "step_id": "tile_data_shape_and_types.s01",
 "type": "explainer",
 "concept_ids": [
  "data.dataset_rows_columns"
 ],
 "eyebrow": "Rows and Columns",
 "title": "A dataset is a table of observations",
 "lede": "Every delivery Kwik Courier makes gets logged in the same way \u2014 and that shared structure is what makes it a dataset.",
 "blocks": [
  {
   "type": "prose",
   "block_id": "tile_data_shape_and_types.s01.b01",
   "role": "intro",
   "text": "Kwik Courier records every delivery it makes: the order number, the destination city, how long the delivery took, and which driver handled it. Written down together, all of those records form a dataset \u2014 a collection of observations that are all recorded on the same set of variables. Every delivery in the batch was captured using the same kinds of information, and that shared structure is what turns a pile of individual facts into one dataset you can work with.",
   "lineage": {
    "concept_ids": [
     "data.dataset_rows_columns"
    ],
    "teaching_block_ids": [
     "data.dataset_rows_columns#tb1"
    ],
    "fact_ids": [
     "data.dataset_rows_columns#f1"
    ]
   }
  },
  {
   "type": "prose",
   "block_id": "tile_data_shape_and_types.s01.b02",
   "role": "definition",
   "text": "That information is commonly organised as a table \u2014 sometimes called a data matrix \u2014 made of rows and columns. Open the Kwik Courier delivery file and you see exactly this: a grid where every delivery has its own line, and every piece of information about a delivery has its own column. The table below shows the first few deliveries.",
   "lineage": {
    "concept_ids": [
     "data.dataset_rows_columns"
    ],
    "teaching_block_ids": [
     "data.dataset_rows_columns#tb2"
    ],
    "fact_ids": [
     "data.dataset_rows_columns#f2"
    ]
   }
  },
  {
   "type": "data_table",
   "block_id": "tile_data_shape_and_types.s01.b03",
   "asset_ref": {
    "asset_id": "ds_courier_orders_base",
    "variant_id": null,
    "columns": [
     "order_id",
     "city",
     "delivery_min",
     "driver"
    ],
    "max_rows": 4
   },
   "caption": "Kwik Courier delivery orders \u2014 each row is one delivery, each column is one attribute.",
   "highlight": [
    {
     "target": {
      "kind": "row",
      "row": {
       "where": {
        "order_id": 1042
       }
      }
     },
     "label": "one observation",
     "tone": "focus"
    },
    {
     "target": {
      "kind": "column",
      "column": "city"
     },
     "label": "one variable",
     "tone": "focus"
    }
   ],
   "lineage": {
    "concept_ids": [
     "data.dataset_rows_columns"
    ],
    "teaching_block_ids": [
     "data.dataset_rows_columns#tb1",
     "data.dataset_rows_columns#tb2"
    ],
    "fact_ids": [
     "data.dataset_rows_columns#f1",
     "data.dataset_rows_columns#f2"
    ],
    "anchors": [
     "data.dataset_rows_columns#visual"
    ]
   }
  }
 ],
 "reward": {
  "gems": 2
 },
 "lineage": {
  "concept_ids": [
   "data.dataset_rows_columns"
  ],
  "teaching_block_ids": [
   "data.dataset_rows_columns#tb1",
   "data.dataset_rows_columns#tb2"
  ],
  "fact_ids": [
   "data.dataset_rows_columns#f1",
   "data.dataset_rows_columns#f2"
  ],
  "anchors": [
   "data.dataset_rows_columns#visual"
  ]
 }
}
```
