"""
Apply the same patches to interactions.json (the merged file used by assemble_tiles.py).
"""
import json

path = 'batches/final_batch_009_da_pandas/interactions.json'

with open(path) as f:
    data = json.load(f)

tile = next(t for t in data['tiles'] if t['tile_id'] == 'tile_pandas_creating_inspecting')

for item in tile['interactions']:
    sid = item['step_id']
    ix = item['interaction']

    if sid == 'tile_pandas_creating_inspecting.s09':
        ix['feedback']['remediation_step_id'] = 'tile_pandas_creating_inspecting.r03'
        print(f"Fixed s09 remediation_step_id → r03")

    elif sid == 'tile_pandas_creating_inspecting.s10':
        new_starter = (
            "import pandas as pd\n"
            "\n"
            "# TODO: load orders.csv into a DataFrame called df\n"
            "# TODO: print the shape\n"
            "# TODO: print the dtypes\n"
            "# TODO: print the first 5 rows\n"
        )
        ix['public']['workspace']['files'][0]['content'] = new_starter
        print(f"Fixed s10 starter")

        if 'remediation_step_id' in ix['feedback']:
            del ix['feedback']['remediation_step_id']
            print(f"Fixed s10: removed remediation_step_id")

with open(path, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done.")
