"""
Patch interactions.part.c1.json: fix tile_pandas_selection_filtering.s05
- Replace solution that uses lit_int (the integer 1) and tuple_lit (comma in subscript)
  with a chained-selection approach that avoids both.
"""
import json, re

path = "batches/final_batch_009_da_pandas/interactions.part.c1.json"

with open(path) as f:
    data = json.load(f)

# New solution content: use chained selection to avoid tuple_lit and lit_int
new_solution_content = (
    "import pandas as pd\n"
    "\n"
    "df = pd.read_csv('orders.csv')\n"
    "\n"
    "# Slice bounds and column info provided\n"
    "start_row = 2\n"
    "end_row_loc = 4  # loc stop is inclusive\n"
    "end_row_iloc = 5  # iloc stop is exclusive\n"
    "city_col_name = 'city'\n"
    "\n"
    "# Select rows with loc slice, then select the column by name\n"
    "loc_result = df.loc[start_row:end_row_loc][city_col_name]\n"
    "print(loc_result)\n"
    "\n"
    "# Select rows with iloc slice, then select the column by name\n"
    "iloc_result = df.iloc[start_row:end_row_iloc][city_col_name]\n"
    "print(iloc_result)\n"
)

# Find the tile and interaction
for tile in data["tiles"]:
    if tile["tile_id"] == "tile_pandas_selection_filtering":
        for item in tile["interactions"]:
            if item["step_id"] == "tile_pandas_selection_filtering.s05":
                ix = item["interaction"]
                # Update solution file content
                for sf in ix["grading"]["solution_files"]:
                    if sf["path"] == "solution.py":
                        sf["content"] = new_solution_content
                        print("Updated solution_files content")
                print("Done patching s05")
                break

with open(path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("File written.")
