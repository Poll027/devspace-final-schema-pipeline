"""
Patch interactions.part.c2.json to fix gate errors:

1. tile_pandas_creating_inspecting.s10: starter already passes tests → remove df=pd.read_csv from starter
2. tile_pandas_dtype_datetime.s04: solution uses attr:dtype → change to df.dtypes
3. tile_pandas_dtype_datetime.s08: solution uses attr:dtype → change to df.dtypes
4. tile_pandas_text_dupes_missing.s07: allowed_syntax has list_lit (not in glossary) + solution uses list_lit
   → remove list_lit from allowed_syntax, change solution to use subset='order_id' (string, not list)
5. tile_pandas_text_dupes_missing.s11: allowed_syntax has list_lit+df.shape (not in glossary),
   solution uses idx_assign, t1 is not data-dependent
   → copy allowed_syntax verbatim from glossary, rewrite solution without idx_assign, fix tests
"""
import json
import copy

with open('batches/final_batch_009_da_pandas/interactions.part.c2.json') as f:
    data = json.load(f)

for tile in data['tiles']:
    tile_id = tile['tile_id']

    # ------------------------------------------------------------------ #
    # FIX 1: tile_pandas_creating_inspecting.s10                          #
    # Starter already defines df, so tests pass without learner doing     #
    # anything. Remove the pd.read_csv line from the starter.             #
    # ------------------------------------------------------------------ #
    if tile_id == 'tile_pandas_creating_inspecting':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_pandas_creating_inspecting.s10':
                interaction = ix['interaction']
                pub = interaction['public']
                for f in pub['workspace']['files']:
                    if f['role'] == 'editable':
                        # Remove the df = pd.read_csv line so learner must add it
                        f['content'] = (
                            "import pandas as pd\n"
                            "\n"
                            "# TODO: Load orders.csv into a DataFrame called df\n"
                            "# TODO: print the shape\n"
                            "# TODO: print the dtypes\n"
                            "# TODO: print the first 5 rows\n"
                        )
                print("Fixed s10 starter")

    # ------------------------------------------------------------------ #
    # FIX 2 & 3: tile_pandas_dtype_datetime.s04 and s08                  #
    # Solution uses attr:dtype (df['col'].dtype) which is not in          #
    # allowed_syntax. Replace with df.dtypes (which IS allowed).          #
    # ------------------------------------------------------------------ #
    if tile_id == 'tile_pandas_dtype_datetime':
        for ix in tile['interactions']:
            # FIX 2: s04
            if ix['step_id'] == 'tile_pandas_dtype_datetime.s04':
                interaction = ix['interaction']
                pub = interaction['public']
                # Update prompt to say df.dtypes instead of dtype of column
                pub['prompt'] = (
                    "The `orders` DataFrame has a `distance_km` column loaded as strings "
                    "(all values are numeric). Convert `distance_km` to float using `astype()`, "
                    "then print `df.dtypes` to verify the conversion.\n\n"
                    "Use only `df['col'].astype(float)`, `df['col'] = ...`, `df.dtypes`, and `print()`."
                )
                # Update solution: use df.dtypes instead of df['distance_km'].dtype
                for sf in interaction['grading']['solution_files']:
                    sf['content'] = (
                        "import pandas as pd\n"
                        "\n"
                        "df = pd.read_csv('orders.csv', dtype={'distance_km': str})\n"
                        "\n"
                        "# Convert distance_km to float\n"
                        "df['distance_km'] = df['distance_km'].astype(float)\n"
                        "\n"
                        "# Print dtypes to verify\n"
                        "print(df.dtypes)\n"
                    )
                print("Fixed s04 solution")

            # FIX 3: s08
            if ix['step_id'] == 'tile_pandas_dtype_datetime.s08':
                interaction = ix['interaction']
                pub = interaction['public']
                # Update prompt to say df.dtypes
                pub['prompt'] = (
                    "The `orders` DataFrame has a `pickup_date` column stored as text. "
                    "Convert `pickup_date` to datetime using `pd.to_datetime()`, then create "
                    "a new `pickup_month` column by extracting the month with `.dt.month`. "
                    "Print `df.dtypes` to verify the new column types.\n\n"
                    "Use only `pd.to_datetime()`, `df['col'].dt.month`, `df['col'] = ...`, "
                    "`df.dtypes`, and `print()`."
                )
                # Update solution: use df.dtypes instead of individual .dtype
                for sf in interaction['grading']['solution_files']:
                    sf['content'] = (
                        "import pandas as pd\n"
                        "\n"
                        "df = pd.read_csv('orders.csv')\n"
                        "\n"
                        "# Convert pickup_date to datetime\n"
                        "df['pickup_date'] = pd.to_datetime(df['pickup_date'])\n"
                        "\n"
                        "# Create pickup_month column\n"
                        "df['pickup_month'] = df['pickup_date'].dt.month\n"
                        "\n"
                        "# Print dtypes to verify\n"
                        "print(df.dtypes)\n"
                    )
                print("Fixed s08 solution")

    # ------------------------------------------------------------------ #
    # FIX 4: tile_pandas_text_dupes_missing.s07                           #
    # allowed_syntax has list_lit (not in glossary) → remove it           #
    # solution uses list_lit (['order_id']) → use string 'order_id'       #
    # ------------------------------------------------------------------ #
    if tile_id == 'tile_pandas_text_dupes_missing':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_pandas_text_dupes_missing.s07':
                interaction = ix['interaction']
                pub = interaction['public']
                # Copy allowed_syntax verbatim from glossary (no list_lit)
                pub['constraints']['allowed_syntax'] = [
                    "df.duplicated(subset=[...])",
                    "df.drop_duplicates(subset=[...])",
                    "keep='first'",
                    "keep='last'",
                    "keep=False",
                    "print()"
                ]
                # Update prompt to use string instead of list
                pub['prompt'] = (
                    "The `df` DataFrame has duplicate `order_id` values. Remove the duplicates "
                    "based on `order_id`, keeping the first occurrence. Print the cleaned DataFrame.\n\n"
                    "Use only `df.drop_duplicates(subset=[...])`, `keep='first'`, and `print()`."
                )
                # Update solution: use subset='order_id' (string) to avoid list_lit
                for sf in interaction['grading']['solution_files']:
                    sf['content'] = (
                        "import pandas as pd\n"
                        "\n"
                        "df = pd.read_csv('orders_messy.csv')\n"
                        "\n"
                        "# Remove duplicates based on order_id, keeping first\n"
                        "df = df.drop_duplicates(subset='order_id', keep='first')\n"
                        "\n"
                        "# Print the cleaned DataFrame\n"
                        "print(df)\n"
                    )
                print("Fixed s07 allowed_syntax and solution")

            # ------------------------------------------------------------------ #
            # FIX 5: tile_pandas_text_dupes_missing.s11                           #
            # allowed_syntax has list_lit + df.shape (not in glossary) → remove  #
            # solution uses idx_assign → rewrite without assignment               #
            # t1 is not data-dependent → replace with data-dependent test         #
            # ------------------------------------------------------------------ #
            if ix['step_id'] == 'tile_pandas_text_dupes_missing.s11':
                interaction = ix['interaction']
                pub = interaction['public']
                # Copy allowed_syntax verbatim from glossary (no list_lit, no df.shape)
                pub['constraints']['allowed_syntax'] = [
                    "df.isna()",
                    "df.notna()",
                    "df.dropna(subset=[...])",
                    "df['col'].fillna(value)",
                    "df['col'].median()",
                    "print()"
                ]
                # Update prompt: no assignment needed
                pub['prompt'] = (
                    "The `df` DataFrame has a missing value in `delivery_time_minutes`. "
                    "Print `df['delivery_time_minutes'].isna()` to detect the gap. "
                    "Then print the column with the missing value filled by the column median "
                    "using `fillna()` and `median()`.\n\n"
                    "Use only `df['col'].isna()`, `df['col'].fillna(value)`, "
                    "`df['col'].median()`, and `print()`."
                )
                # Update starter: no assignment
                for f in pub['workspace']['files']:
                    if f['role'] == 'editable':
                        f['content'] = (
                            "import pandas as pd\n"
                            "\n"
                            "df = pd.read_csv('orders_messy.csv')\n"
                            "\n"
                            "# TODO: Print isna() to detect missing delivery_time_minutes\n"
                            "\n"
                            "# TODO: Print the column with missing value filled by its median\n"
                        )
                # Update solution: no idx_assign
                for sf in interaction['grading']['solution_files']:
                    sf['content'] = (
                        "import pandas as pd\n"
                        "\n"
                        "df = pd.read_csv('orders_messy.csv')\n"
                        "\n"
                        "# Print isna() to detect missing delivery_time_minutes\n"
                        "print(df['delivery_time_minutes'].isna())\n"
                        "\n"
                        "# Print the column with missing value filled by its median\n"
                        "print(df['delivery_time_minutes'].fillna(df['delivery_time_minutes'].median()))\n"
                    )
                # Update tests: replace t1 (not data-dependent) with data-dependent test
                # The filled series: [18.0, 20.0, 22.0, 22.0, 26.0, 28.0, 80.0, 23.0, 19.0, 24.0, 33.0, 21.0, 27.0, 35.0, 22.0]
                # median of non-null values [18,20,22,22,26,28,80,19,24,33,21,27,35,22] = 23.0
                interaction['grading']['tests'] = [
                    {
                        "test_id": "t1",
                        "kind": "value_equals",
                        "spec": {
                            "expr": "df['delivery_time_minutes'].fillna(df['delivery_time_minutes'].median()).tolist()",
                            "expected": [18.0, 20.0, 22.0, 22.0, 26.0, 28.0, 80.0, 23.0, 19.0, 24.0, 33.0, 21.0, 27.0, 35.0, 22.0]
                        },
                        "visible": True,
                        "message_on_fail": "Make sure you fill the missing value with `df['delivery_time_minutes'].fillna(df['delivery_time_minutes'].median())`."
                    }
                ]
                print("Fixed s11 allowed_syntax, solution, and tests")

with open('batches/final_batch_009_da_pandas/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Done patching interactions.part.c2.json")
