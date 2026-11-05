"""
Repair patch for interactions.part.c0_canary.json:

1. s05: add missing allowed_syntax descriptors (list_lit, dict_lit, lit_int, lit_str)
2. s05: redesign solution to have first_time=18 as top-level constant (so py_var_mutations can mutate it)
3. s05: make delivery_times and data depend on first_time (so results change when first_time changes)
4. s05: use col_name variable for column selection (avoids lit_str in df['col'] call)
5. s05: update starter to match new solution structure
6. s05: change remediation_step_id from r01 to r02 (r02 is about constructing Series/DataFrames)
7. s10: add 'single- or double-quoted strings' to allowed_syntax (covers lit_str from file_path)
"""
import json, copy

with open('batches/final_batch_009_da_pandas/interactions.part.c0_canary.json') as f:
    d = json.load(f)

for tile in d.get('tiles', []):
    for ix in tile.get('interactions', []):
        step_id = ix.get('step_id')
        interaction = ix['interaction']

        # ── s05 ──────────────────────────────────────────────────────────────
        if step_id == 'tile_pandas_dataframe_reading.s05':
            pub = interaction['public']

            # 1. Add missing allowed_syntax descriptors
            pub['constraints']['allowed_syntax'] = [
                "import pandas as pd",
                "pd.Series(list)",
                "pd.DataFrame(dict_of_lists)",
                "df['col']",
                "print()",
                "type()",
                "[...] list literal",
                "{key: value} dictionary literal",
                "int, float, str and bool literals",
                "single- or double-quoted strings",
                "name = value assignment"
            ]

            # 2. Update prompt to clarify col_name usage
            pub['prompt'] = (
                "Complete the script to:\n"
                "1. `first_time` is already set to `18` (the first delivery time). "
                "Build `delivery_times = [first_time, 20, 22, 22, 26, 28, 80]` and a Series `s` from it; print `s`.\n"
                "2. Build a DataFrame `df` from the `data` dict "
                "(keys: `order_id`, `city`, `delivery_time_minutes`) and print it.\n"
                "3. Pull out the column named by `col_name` from `df` into `col` and print its type.\n\n"
                "Use only `pd.Series(list)`, `pd.DataFrame(dict_of_lists)`, `df['col']`, `print()`, and `type()`."
            )

            # 3. Update starter: provide first_time, delivery_times, data, col_name as variables
            starter_content = (
                "import pandas as pd\n\n"
                "# First delivery time (minutes) — change this to test your code\n"
                "first_time = 18\n\n"
                "# Delivery times list — uses first_time as the first element\n"
                "delivery_times = [first_time, 20, 22, 22, 26, 28, 80]\n\n"
                "# Data dict for the DataFrame\n"
                "data = {\n"
                "    'order_id': [1001, 1002, 1003],\n"
                "    'city': ['Lagos', 'Abuja', 'Kano'],\n"
                "    'delivery_time_minutes': [first_time, 20, 26]\n"
                "}\n\n"
                "# Column to select\n"
                "col_name = 'delivery_time_minutes'\n\n"
                "# TODO: Create a Series from delivery_times and print it\n\n"
                "# TODO: Create a DataFrame from data and print it\n\n"
                "# TODO: Pull out the col_name column from df and print its type\n"
            )
            pub['workspace']['files'][0]['content'] = starter_content

            # 4. Update solution: same structure, adds the three lines
            solution_content = (
                "import pandas as pd\n\n"
                "# First delivery time (minutes) — change this to test your code\n"
                "first_time = 18\n\n"
                "# Delivery times list — uses first_time as the first element\n"
                "delivery_times = [first_time, 20, 22, 22, 26, 28, 80]\n\n"
                "# Data dict for the DataFrame\n"
                "data = {\n"
                "    'order_id': [1001, 1002, 1003],\n"
                "    'city': ['Lagos', 'Abuja', 'Kano'],\n"
                "    'delivery_time_minutes': [first_time, 20, 26]\n"
                "}\n\n"
                "# Column to select\n"
                "col_name = 'delivery_time_minutes'\n\n"
                "# Create a Series from delivery_times and print it\n"
                "s = pd.Series(delivery_times)\n"
                "print(s)\n\n"
                "# Create a DataFrame from data and print it\n"
                "df = pd.DataFrame(data)\n"
                "print(df)\n\n"
                "# Pull out the col_name column from df and print its type\n"
                "col = df[col_name]\n"
                "print(type(col))\n"
            )
            interaction['grading']['solution_files'][0]['content'] = solution_content

            # 5. Update tests — expected values are the same (first_time=18)
            # t1: s.tolist() = [18, 20, 22, 22, 26, 28, 80]  (unchanged)
            # t2: df = same 3-row DataFrame                   (unchanged)
            # t3: col.tolist() = [18, 20, 26]                 (unchanged)
            # No changes needed to test specs.

            # 6. Change remediation_step_id to r02
            interaction['feedback']['remediation_step_id'] = 'tile_pandas_dataframe_reading.r02'

        # ── s10 ──────────────────────────────────────────────────────────────
        elif step_id == 'tile_pandas_dataframe_reading.s10':
            pub = interaction['public']

            # Add 'single- or double-quoted strings' to allowed_syntax to cover lit_str
            if 'single- or double-quoted strings' not in pub['constraints']['allowed_syntax']:
                pub['constraints']['allowed_syntax'].append('single- or double-quoted strings')

with open('batches/final_batch_009_da_pandas/interactions.part.c0_canary.json', 'w') as f:
    json.dump(d, f, indent=2)

print("Patch applied.")
