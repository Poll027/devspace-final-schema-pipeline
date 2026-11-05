"""
Patch interactions.part.c1.json to fix:
1. E s10: starter already passes every result test → remove df definition from starter
2. W s09: remediation r02 teaches f2,f4 but s09 measures f5 → change to r03
3. W s10: remediation r02 teaches f2,f4 but s10 measures f1,f3 → omit (no matching remediation)
4. W r03 never referenced → fixed by #2 above
"""
import json

path = 'batches/final_batch_009_da_pandas/interactions.part.c1.json'

with open(path) as f:
    data = json.load(f)

tile = next(t for t in data['tiles'] if t['tile_id'] == 'tile_pandas_creating_inspecting')

for item in tile['interactions']:
    sid = item['step_id']
    ix = item['interaction']

    if sid == 'tile_pandas_creating_inspecting.s09':
        # Fix W: r02 teaches f2,f4 but s09 measures f5 → point to r03 (teaches f5)
        ix['feedback']['remediation_step_id'] = 'tile_pandas_creating_inspecting.r03'
        print(f"Fixed s09 remediation_step_id → r03")

    elif sid == 'tile_pandas_creating_inspecting.s10':
        # Fix E: starter already passes tests → remove df = pd.read_csv(...) from starter
        # so value_equals expr='df.shape' will fail (NameError) on the unmodified starter
        old_starter = ix['public']['workspace']['files'][0]['content']
        new_starter = (
            "import pandas as pd\n"
            "\n"
            "# TODO: load orders.csv into a DataFrame called df\n"
            "# TODO: print the shape\n"
            "# TODO: print the dtypes\n"
            "# TODO: print the first 5 rows\n"
        )
        ix['public']['workspace']['files'][0]['content'] = new_starter
        print(f"Fixed s10 starter (removed df definition so tests fail on unmodified starter)")

        # Fix W: r02 teaches f2,f4 but s10 measures f1,f3 → omit remediation_step_id
        if 'remediation_step_id' in ix['feedback']:
            del ix['feedback']['remediation_step_id']
            print(f"Fixed s10: removed remediation_step_id (no remediation step teaches f1,f3)")

with open(path, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done.")
