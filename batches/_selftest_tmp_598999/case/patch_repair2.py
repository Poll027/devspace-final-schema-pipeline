"""
Repair patch for interactions.part.c0_canary.json

Fixes:
1. fact_ids in measures: remove concept_id prefix (e.g. 'pandas.dataframe_series_model#f1' -> 'f1')
2. remediation_step_id: s01->r01, s06->r03 or r04 (based on what the step measures)
3. s05: redesign to fix syntax violations and hard-coded tests
4. s10: add 'single- or double-quoted strings' to allowed_syntax
"""
import json, copy

with open('batches/final_batch_009_da_pandas/interactions.part.c0_canary.json') as f:
    d = json.load(f)

tile = d['tiles'][0]
assert tile['tile_id'] == 'tile_pandas_dataframe_reading'

for ix in tile['interactions']:
    step_id = ix['step_id']
    interaction = ix['interaction']

    # ---- Fix 1: fact_ids in measures (remove concept_id prefix) ----
    for m in interaction.get('measures', []):
        cid = m['concept_id']
        prefix = cid + '#'
        m['fact_ids'] = [
            fid[len(prefix):] if fid.startswith(prefix) else fid
            for fid in m['fact_ids']
        ]

    # ---- Fix 2: remediation_step_id ----
    feedback = interaction.get('feedback', {})
    if step_id in ('tile_pandas_dataframe_reading.s04', 'tile_pandas_dataframe_reading.s05'):
        # r01 covers pandas.dataframe_series_model f1, f2, f5
        feedback['remediation_step_id'] = 'tile_pandas_dataframe_reading.r01'
    elif step_id == 'tile_pandas_dataframe_reading.s08':
        # r03 covers pandas.reading_data f1, f2
        feedback['remediation_step_id'] = 'tile_pandas_dataframe_reading.r03'
    elif step_id == 'tile_pandas_dataframe_reading.s09':
        # r04 covers pandas.reading_data f3, f4
        feedback['remediation_step_id'] = 'tile_pandas_dataframe_reading.r04'
    elif step_id == 'tile_pandas_dataframe_reading.s10':
        # r03 covers pandas.reading_data f1, f2 (s10 measures f1, f3 - r03 is closer)
        feedback['remediation_step_id'] = 'tile_pandas_dataframe_reading.r03'

    # ---- Fix 3: s05 redesign ----
    if step_id == 'tile_pandas_dataframe_reading.s05':
        pub = interaction['public']
        gr = interaction['grading']

        # Update prompt to use delivery_time_minutes column
        pub['prompt'] = (
            "Complete the script to:\n"
            "1. Define `first_time = 18` (the first delivery time in minutes), then build "
            "`delivery_times = [first_time, 20, 22, 22, 26, 28, 80]` and a Series `s` from it; print `s`.\n"
            "2. Build a DataFrame `df` from the `data` dict "
            "(keys: `order_id`, `city`, `delivery_time_minutes`) and print it.\n"
            "3. Pull out the `'delivery_time_minutes'` column from `df` into `col` and print its type.\n\n"
            "Use only `pd.Series(list)`, `pd.DataFrame(dict_of_lists)`, `df['col']`, `print()`, and `type()`."
        )

        # Update starter
        pub['workspace']['files'][0]['content'] = (
            "import pandas as pd\n\n"
            "# first_time = 18  # first delivery time in minutes\n"
            "# delivery_times = [first_time, 20, 22, 22, 26, 28, 80]\n\n"
            "# data = {\n"
            "#     'order_id': [1001, 1002, 1003],\n"
            "#     'city': ['Lagos', 'Abuja', 'Kano'],\n"
            "#     'delivery_time_minutes': [first_time, 20, 26]\n"
            "# }\n\n"
            "# TODO: define first_time, delivery_times, and data\n"
            "# TODO: build a Series from delivery_times and print it\n"
            "# TODO: build a DataFrame from data and print it\n"
            "# TODO: pull out the 'delivery_time_minutes' column into col, print its type\n"
        )

        # Remove asset_mounts if present (not needed)
        pub['workspace'].pop('asset_mounts', None)

        # Update allowed_syntax to include literals needed by the solution
        pub['constraints']['allowed_syntax'] = [
            "import pandas as pd",
            "pd.Series(list)",
            "pd.DataFrame(dict_of_lists)",
            "df['col']",
            "print()",
            "type()",
            "[...] list literal",
            "{key: value} dictionary literal",
            "whole-number literals as in the examples",
            "single- or double-quoted strings",
            "name = value assignment"
        ]

        # Update solution
        solution_content = (
            "import pandas as pd\n\n"
            "first_time = 18\n"
            "delivery_times = [first_time, 20, 22, 22, 26, 28, 80]\n"
            "data = {\n"
            "    'order_id': [1001, 1002, 1003],\n"
            "    'city': ['Lagos', 'Abuja', 'Kano'],\n"
            "    'delivery_time_minutes': [first_time, 20, 26]\n"
            "}\n\n"
            "s = pd.Series(delivery_times)\n"
            "print(s)\n\n"
            "df = pd.DataFrame(data)\n"
            "print(df)\n\n"
            "col = df['delivery_time_minutes']\n"
            "print(type(col))\n"
        )
        gr['solution_files'][0]['content'] = solution_content

        # Update tests
        gr['tests'] = [
            {
                "test_id": "ix.tile_pandas_dataframe_reading.s05.t1",
                "kind": "value_equals",
                "spec": {
                    "expr": "s.tolist()",
                    "expected": [18, 20, 22, 22, 26, 28, 80]
                },
                "visible": True,
                "message_on_fail": (
                    "Make sure `s = pd.Series(delivery_times)` where "
                    "`delivery_times = [first_time, 20, 22, 22, 26, 28, 80]` and `first_time = 18`."
                )
            },
            {
                "test_id": "ix.tile_pandas_dataframe_reading.s05.t2",
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
                    "Make sure `df = pd.DataFrame(data)` where `data` has keys "
                    "`order_id`, `city`, `delivery_time_minutes` with the given lists."
                )
            },
            {
                "test_id": "ix.tile_pandas_dataframe_reading.s05.t3",
                "kind": "value_equals",
                "spec": {
                    "expr": "col.tolist()",
                    "expected": [18, 20, 26]
                },
                "visible": True,
                "message_on_fail": (
                    "Use `col = df['delivery_time_minutes']` to pull out the column. "
                    "Its values should match `data['delivery_time_minutes']`."
                )
            }
        ]

    # ---- Fix 4: s10 allowed_syntax ----
    if step_id == 'tile_pandas_dataframe_reading.s10':
        pub = interaction['public']
        if 'single- or double-quoted strings' not in pub['constraints']['allowed_syntax']:
            pub['constraints']['allowed_syntax'].append('single- or double-quoted strings')

with open('batches/final_batch_009_da_pandas/interactions.part.c0_canary.json', 'w') as f:
    json.dump(d, f, indent=2)

print("Patch applied successfully.")
