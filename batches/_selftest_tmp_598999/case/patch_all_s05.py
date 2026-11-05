"""
Patch all interactions.json files that contain the s05 interaction with the bad solution.
Updates:
1. batches/final_batch_009_da_pandas/interactions.part.c1.json (already done)
2. batches/final_batch_009_da_pandas/interactions.json (merged file)
3. batches/final_batch_009_da_pandas/working/gate_04_interactions_c1/interactions.json (gate working dir)
"""
import json

# The correct solution - no lit_int, no tuple_lit
# city_col_pos = 1 is removed (it was in the merged file but not in the starter, causing lit_int)
# chained selection avoids tuple_lit
GOOD_SOLUTION = (
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

files_to_patch = [
    "batches/final_batch_009_da_pandas/interactions.part.c1.json",
    "batches/final_batch_009_da_pandas/interactions.json",
    "batches/final_batch_009_da_pandas/working/gate_04_interactions_c1/interactions.json",
]

for fpath in files_to_patch:
    with open(fpath) as f:
        data = json.load(f)
    
    patched = False
    for tile in data.get("tiles", []):
        if tile.get("tile_id") == "tile_pandas_selection_filtering":
            for item in tile.get("interactions", []):
                if item.get("step_id") == "tile_pandas_selection_filtering.s05":
                    ix = item["interaction"]
                    for sf in ix.get("grading", {}).get("solution_files", []):
                        if sf["path"] == "solution.py":
                            sf["content"] = GOOD_SOLUTION
                            patched = True
    
    if patched:
        with open(fpath, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"Patched: {fpath}")
    else:
        print(f"No s05 found in: {fpath}")
