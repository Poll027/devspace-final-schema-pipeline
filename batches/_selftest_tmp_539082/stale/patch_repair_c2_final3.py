"""
Patch interactions.part.c2.json to fix gate errors:

1. tile_pandas_creating_inspecting.s10: starter already passes tests + solution uses lit_str
   → remove df=pd.read_csv from starter, add file_path variable, solution uses file_path
2. tile_pandas_dtype_datetime.s04: solution uses attr:dtype → change to df.dtypes
3. tile_pandas_dtype_datetime.s08: solution uses attr:dtype → change to df.dtypes
4. tile_pandas_text_dupes_missing.s07: allowed_syntax has list_lit (not in glossary) + solution uses list_lit
   → remove list_lit from allowed_syntax, change solution to use subset='order_id' (string, not list)
5. tile_pandas_text_dupes_missing.s11: allowed_syntax has list_lit+df.shape (not in glossary),
   solution uses idx_assign, starter already passes tests
   → copy allowed_syntax verbatim from glossary, rewrite solution without idx_assign, use stdout_equals test
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
    # anything. Solution uses lit_str ('orders.csv').                     #
    # Fix: starter defines file_path variable, solution uses it.          #
    # ------------------------------------------------------------------ #
    if tile_id == 'tile_pandas_creating_inspecting':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_pandas_creating_inspecting.s10':
                interaction = ix['interaction']
                pub = interaction['public']
                # Update starter: define file_path, no df yet
                for f in pub['workspace']['files']:
                    if f['role'] == 'editable':
                        f['content'] = (
                            "import pandas as pd\n"
                            "\n"
                            "# File path provided for you\n"
                            "file_path = 'orders.csv'\n"
                            "\n"
                            "# TODO: Load the CSV file into a DataFrame called df\n"
                            "# TODO: print the shape\n"
                            "# TODO: print the dtypes\n"
                            "# TODO: print the first 5 rows\n"
                        )
                # Update solution: use file_path variable
                for sf in interaction['grading']['solution_files']:
                    sf['content'] = (
                        "import pandas as pd\n"
                        "\n"
                        "# File path provided for you\n"
                        "file_path = 'orders.csv'\n"
                        "\n"
                        "# Load the CSV file into a DataFrame called df\n"
                        "df = pd.read_csv(file_path)\n"
                        "\n"
                        "print(df.shape)\n"
                        "print(df.dtypes)\n"
                        "print(df.head())\n"
                    )
                print("Fixed s10 starter and solution")

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
            # starter already passes tests → use stdout_equals test               #
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
                # Update starter: no assignment, no df defined yet
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
                # Update tests: use stdout_equals (starter doesn't print, so it fails)
                # The exact stdout from the solution (data-dependent):
                expected_stdout = (
                    "0     False\n"
                    "1     False\n"
                    "2     False\n"
                    "3     False\n"
                    "4     False\n"
                    "5     False\n"
                    "6     False\n"
                    "7      True\n"
                    "8     False\n"
                    "9     False\n"
                    "10    False\n"
                    "11    False\n"
                    "12    False\n"
                    "13    False\n"
                    "14    False\n"
                    "Name: delivery_time_minutes, dtype: bool\n"
                    "0     18.0\n"
                    "1     20.0\n"
                    "2     22.0\n"
                    "3     22.0\n"
                    "4     26.0\n"
                    "5     28.0\n"
                    "6     80.0\n"
                    "7     23.0\n"
                    "8     19.0\n"
                    "9     24.0\n"
                    "10    33.0\n"
                    "11    21.0\n"
                    "12    27.0\n"
                    "13    35.0\n"
                    "14    22.0\n"
                    "Name: delivery_time_minutes, dtype: float64"
                )
                interaction['grading']['tests'] = [
                    {
                        "test_id": "t1",
                        "kind": "stdout_equals",
                        "spec": {
                            "expected": expected_stdout
                        },
                        "visible": True,
                        "message_on_fail": "Make sure you print `df['delivery_time_minutes'].isna()` and then print `df['delivery_time_minutes'].fillna(df['delivery_time_minutes'].median())`."
                    }
                ]
                print("Fixed s11 allowed_syntax, solution, and tests")

with open('batches/final_batch_009_da_pandas/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Done patching interactions.part.c2.json")
