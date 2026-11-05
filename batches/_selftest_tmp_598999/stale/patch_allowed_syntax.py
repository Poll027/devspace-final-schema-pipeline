import json

with open('batches/final_batch_009_da_pandas/interactions.part.c0_canary.json') as f:
    data = json.load(f)

# Verbatim allowed_syntax from glossary practice anchors
ALLOWED_SYNTAX_DSM = [
    "import pandas as pd",
    "pd.Series(list)",
    "pd.DataFrame(dict_of_lists)",
    "df['col']",
    "print()",
    "type()"
]

ALLOWED_SYNTAX_RD = [
    "import pandas as pd",
    "pd.read_csv(path)",
    "pd.read_csv(path, sep=...)",
    "pd.read_excel(path, sheet_name=...)",
    "print(df)"
]

tiles = data.get('tiles', [])
for tile in tiles:
    for item in tile.get('interactions', []):
        step_id = item.get('step_id', '')
        interaction = item.get('interaction', {})
        public = interaction.get('public', {})
        constraints = public.get('constraints', {})

        if step_id == 'tile_pandas_dataframe_reading.s05':
            print(f"Before s05 allowed_syntax: {constraints.get('allowed_syntax')}")
            constraints['allowed_syntax'] = ALLOWED_SYNTAX_DSM
            print(f"After  s05 allowed_syntax: {constraints.get('allowed_syntax')}")

        elif step_id == 'tile_pandas_dataframe_reading.s10':
            print(f"Before s10 allowed_syntax: {constraints.get('allowed_syntax')}")
            constraints['allowed_syntax'] = ALLOWED_SYNTAX_RD
            print(f"After  s10 allowed_syntax: {constraints.get('allowed_syntax')}")

with open('batches/final_batch_009_da_pandas/interactions.part.c0_canary.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Patch applied successfully.")
