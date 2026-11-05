"""
Patch: fix tile_pandas_selection_filtering.s05 solution.
The .iloc call used city_col_name (a string) as the column selector,
which is invalid for .iloc (requires integer). Fix: use integer index 1
(the position of 'city' in the DataFrame columns).
"""
import json, re

path = 'batches/final_batch_009_da_pandas/interactions.part.c1.json'

with open(path) as f:
    data = json.load(f)

# Find the tile and step
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_pandas_selection_filtering':
        for item in tile['interactions']:
            if item['step_id'] == 'tile_pandas_selection_filtering.s05':
                interaction = item['interaction']
                # Fix the solution file content
                sol_files = interaction['grading']['solution_files']
                for sf in sol_files:
                    if sf['path'] == 'solution.py':
                        old = sf['content']
                        # Replace the bad iloc line: df.iloc[start_row:end_row_iloc, city_col_name]
                        # with: df.iloc[start_row:end_row_iloc, 1]
                        new = old.replace(
                            'df.iloc[start_row:end_row_iloc, city_col_name]',
                            'df.iloc[start_row:end_row_iloc, 1]'
                        )
                        if new == old:
                            print("ERROR: pattern not found in solution content!")
                            print(repr(old))
                        else:
                            sf['content'] = new
                            print("Patched solution_files[0].content")
                            print("Old line: df.iloc[start_row:end_row_iloc, city_col_name]")
                            print("New line: df.iloc[start_row:end_row_iloc, 1]")

with open(path, 'w') as f:
    json.dump(data, f, indent=2)

print("Done.")
