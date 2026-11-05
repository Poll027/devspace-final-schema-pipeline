"""
Repair round patch for interactions.part.c1.json and screens.part.c1.json.

Fixes:
1. s04 t1/t2/t3: hard-coded answers — remove [:3] slices so shape depends on data
2. s10 t1: stdout_equals expected differs — replace with value_equals + dataframe_equals
3. s05 screens: add diagram block (plan requires annotated_image or diagram)
"""
import json, copy

# ── interactions.part.c1.json ──────────────────────────────────────────────
with open('batches/final_batch_009_da_pandas/interactions.part.c1.json') as f:
    ix = json.load(f)

for tile in ix['tiles']:
    if tile['tile_id'] != 'tile_pandas_creating_inspecting':
        continue

    for item in tile['interactions']:
        step_id = item['step_id']
        ix_obj = item['interaction']

        # ── Fix s04 ──────────────────────────────────────────────────────
        if step_id == 'tile_pandas_creating_inspecting.s04':
            # New starter: use full dataset (no [:3] / .head(3))
            new_starter = (
                "import pandas as pd\n"
                "\n"
                "# Data loaded from CSV (scaffolding)\n"
                "_raw = pd.read_csv('orders_sample.csv')\n"
                "dict_of_lists = {\n"
                "    'order_id': list(_raw['order_id']),\n"
                "    'city': list(_raw['city']),\n"
                "    'delivery_time_minutes': list(_raw['delivery_time_minutes'])\n"
                "}\n"
                "list_of_dicts = _raw[['order_id', 'city', 'delivery_time_minutes']].to_dict('records')\n"
                "\n"
                "# TODO: Create df1 from dict_of_lists using pd.DataFrame()\n"
                "# TODO: Create df2 from list_of_dicts using pd.DataFrame()\n"
                "# TODO: Print both\n"
            )
            # New solution: same but with the two DataFrame calls
            new_solution = (
                "import pandas as pd\n"
                "\n"
                "# Data loaded from CSV (scaffolding)\n"
                "_raw = pd.read_csv('orders_sample.csv')\n"
                "dict_of_lists = {\n"
                "    'order_id': list(_raw['order_id']),\n"
                "    'city': list(_raw['city']),\n"
                "    'delivery_time_minutes': list(_raw['delivery_time_minutes'])\n"
                "}\n"
                "list_of_dicts = _raw[['order_id', 'city', 'delivery_time_minutes']].to_dict('records')\n"
                "\n"
                "df1 = pd.DataFrame(dict_of_lists)\n"
                "df2 = pd.DataFrame(list_of_dicts)\n"
                "print(df1)\n"
                "print(df2)\n"
            )

            # Update starter file
            for f in ix_obj['public']['workspace']['files']:
                if f['path'] == 'solution.py':
                    f['content'] = new_starter

            # Update solution file
            for f in ix_obj['grading']['solution_files']:
                if f['path'] == 'solution.py':
                    f['content'] = new_solution

            # All 14 rows for (order_id, city, delivery_time_minutes)
            rows_3col = [
                [1001, "Lagos", 18],
                [1002, "Abuja", 20],
                [1003, "Kano",  22],
                [1004, "Lagos", 22],
                [1005, "Abuja", 26],
                [1006, "Kano",  28],
                [1007, "Lagos", 80],
                [1008, "Abuja", 31],
                [1009, "Kano",  19],
                [1010, "Lagos", 24],
                [1011, "Abuja", 33],
                [1012, "Kano",  21],
                [1013, "Lagos", 27],
                [1014, "Abuja", 35],
            ]

            # Replace tests
            ix_obj['grading']['tests'] = [
                {
                    "test_id": "t1",
                    "kind": "value_equals",
                    "spec": {
                        "expr": "df1.shape",
                        "expected": [14, 3]
                    },
                    "visible": True,
                    "message_on_fail": "df1 should have 14 rows and 3 columns. Check that you created it from dict_of_lists using pd.DataFrame()."
                },
                {
                    "test_id": "t2",
                    "kind": "value_equals",
                    "spec": {
                        "expr": "df2.shape",
                        "expected": [14, 3]
                    },
                    "visible": True,
                    "message_on_fail": "df2 should have 14 rows and 3 columns. Check that you created it from list_of_dicts using pd.DataFrame()."
                },
                {
                    "test_id": "t3",
                    "kind": "dataframe_equals",
                    "spec": {
                        "expr": "df1",
                        "expected": {
                            "columns": ["order_id", "city", "delivery_time_minutes"],
                            "rows": rows_3col
                        }
                    },
                    "visible": True,
                    "message_on_fail": "df1 does not match the expected data. Check that you used pd.DataFrame(dict_of_lists)."
                }
            ]

        # ── Fix s10 ──────────────────────────────────────────────────────
        elif step_id == 'tile_pandas_creating_inspecting.s10':
            # First 5 rows of ds_orders (all 10 columns)
            head_rows = [
                [1001, "Lagos", "LOS", "Ada",   201, 301, "2024-03-14", 18, 4.2,  2500],
                [1002, "Abuja", "ABJ", "Bayo",  202, 302, "2024-03-14", 20, 6.1,  3100],
                [1003, "Kano",  "KAN", "Chidi", 203, 303, "2024-03-15", 22, 5.5,  1800],
                [1004, "Lagos", "LOS", "Ada",   201, 304, "2024-03-15", 22, 3.8,  2200],
                [1005, "Abuja", "ABJ", "Bayo",  202, 305, "2024-03-16", 26, 7.3,  4000],
            ]
            all_cols = [
                "order_id", "city", "city_code", "courier",
                "driver_id", "customer_id", "pickup_date",
                "delivery_time_minutes", "distance_km", "order_value"
            ]

            # Replace the single stdout_equals test with two data-dependent tests
            ix_obj['grading']['tests'] = [
                {
                    "test_id": "t1",
                    "kind": "value_equals",
                    "spec": {
                        "expr": "df.shape",
                        "expected": [14, 10]
                    },
                    "visible": True,
                    "message_on_fail": "df.shape should be (14, 10). Make sure you loaded orders.csv and printed the shape."
                },
                {
                    "test_id": "t2",
                    "kind": "dataframe_equals",
                    "spec": {
                        "expr": "df.head()",
                        "expected": {
                            "columns": all_cols,
                            "rows": head_rows
                        }
                    },
                    "visible": True,
                    "message_on_fail": "df.head() should return the first 5 rows of orders.csv. Check that you loaded the file correctly."
                }
            ]

with open('batches/final_batch_009_da_pandas/interactions.part.c1.json', 'w') as f:
    json.dump(ix, f, indent=2)
print("interactions.part.c1.json patched")

# ── screens.part.c1.json — add diagram block to s05 ───────────────────────
with open('batches/final_batch_009_da_pandas/screens.part.c1.json') as f:
    sc = json.load(f)

diagram_block = {
    "type": "diagram",
    "block_id": "tile_pandas_creating_inspecting.s05.b4",
    "diagram_kind": "mapping",
    "title": "Five inspection methods and the question each answers",
    "nodes": [
        {"id": "n_head",     "label": "head()",     "group": "method"},
        {"id": "n_shape",    "label": "shape",      "group": "method"},
        {"id": "n_dtypes",   "label": "dtypes",     "group": "method"},
        {"id": "n_info",     "label": "info()",     "group": "method"},
        {"id": "n_describe", "label": "describe()", "group": "method"},
        {"id": "q_preview",  "label": "What do the first rows look like?",       "group": "question"},
        {"id": "q_size",     "label": "How many rows and columns?",              "group": "question"},
        {"id": "q_types",    "label": "What type is each column?",               "group": "question"},
        {"id": "q_missing",  "label": "Are there missing values?",               "group": "question"},
        {"id": "q_stats",    "label": "What are the numeric distributions?",     "group": "question"}
    ],
    "edges": [
        {"from": "n_head",     "to": "q_preview"},
        {"from": "n_shape",    "to": "q_size"},
        {"from": "n_dtypes",   "to": "q_types"},
        {"from": "n_info",     "to": "q_missing"},
        {"from": "n_describe", "to": "q_stats"}
    ],
    "alt_text": (
        "A mapping diagram showing five pandas inspection methods — head(), shape, dtypes, "
        "info(), and describe() — each connected by an arrow to the question it answers: "
        "head() → 'What do the first rows look like?'; shape → 'How many rows and columns?'; "
        "dtypes → 'What type is each column?'; info() → 'Are there missing values?'; "
        "describe() → 'What are the numeric distributions?'."
    ),
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

for tile in sc['tiles']:
    if tile['tile_id'] != 'tile_pandas_creating_inspecting':
        continue
    for step in tile.get('steps', []):
        if step['step_id'] == 'tile_pandas_creating_inspecting.s05':
            # Check if diagram block already present
            has_visual = any(
                b.get('type') in ('annotated_image', 'diagram')
                for b in step.get('blocks', [])
            )
            if not has_visual:
                step['blocks'].append(diagram_block)
                print("Added diagram block to s05")
            else:
                print("s05 already has a visual block")
            break

with open('batches/final_batch_009_da_pandas/screens.part.c1.json', 'w') as f:
    json.dump(sc, f, indent=2)
print("screens.part.c1.json patched")
