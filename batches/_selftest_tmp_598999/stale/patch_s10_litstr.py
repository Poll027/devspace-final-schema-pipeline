"""
Fix s10: solution uses 'lit_str' (pd.read_csv('orders.csv')) which is not in allowed_syntax.
Fix: change starter to provide path = 'orders.csv' as scaffolding, and solution uses pd.read_csv(path).
Apply to both interactions.part.c1.json and interactions.json.
"""
import json

NEW_STARTER = (
    "import pandas as pd\n"
    "\n"
    "path = 'orders.csv'  # scaffolding\n"
    "\n"
    "# TODO: load the CSV into a DataFrame called df using pd.read_csv(path)\n"
    "# TODO: print the shape\n"
    "# TODO: print the dtypes\n"
    "# TODO: print the first 5 rows\n"
)

NEW_SOLUTION = (
    "import pandas as pd\n"
    "\n"
    "path = 'orders.csv'  # scaffolding\n"
    "\n"
    "df = pd.read_csv(path)\n"
    "\n"
    "print(df.shape)\n"
    "print(df.dtypes)\n"
    "print(df.head())\n"
)

for path_file in [
    'batches/final_batch_009_da_pandas/interactions.part.c1.json',
    'batches/final_batch_009_da_pandas/interactions.json',
]:
    with open(path_file) as f:
        data = json.load(f)

    tile = next(t for t in data['tiles'] if t['tile_id'] == 'tile_pandas_creating_inspecting')
    s10 = next(i for i in tile['interactions'] if i['step_id'] == 'tile_pandas_creating_inspecting.s10')
    ix = s10['interaction']

    ix['public']['workspace']['files'][0]['content'] = NEW_STARTER
    ix['grading']['solution_files'][0]['content'] = NEW_SOLUTION

    with open(path_file, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Updated {path_file}")

print("Done.")
