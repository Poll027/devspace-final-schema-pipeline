#!/usr/bin/env python3
"""Revert the allowed syntax changes and keep only the solution fixes."""

import json

# Files to patch
files_to_patch = ['interactions.part.c0_canary.json', 'interactions.json']

# Original allowed syntax (from the original artifact before my changes)
original_s05_allowed = [
    "import pandas as pd",
    "pd.Series(list)",
    "pd.DataFrame(dict_of_lists)",
    "df['col']",
    "print()",
    "type()"
]

original_s10_allowed = [
    "import pandas as pd",
    "pd.read_csv(path)",
    "pd.read_csv(path, sep=...)",
    "pd.read_excel(path, sheet_name=...)",
    "print(df)"
]

for filename in files_to_patch:
    print(f"\nPatching {filename}...")
    
    with open(filename, 'r') as f:
        data = json.load(f)

    for tile in data['tiles']:
        if tile['tile_id'] == 'tile_pandas_dataframe_reading':
            for item in tile['interactions']:
                ix = item['interaction']
                
                # Fix s05: Restore original allowed syntax
                if ix['interaction_id'] == 'ix.tile_pandas_dataframe_reading.s05':
                    ix['public']['constraints']['allowed_syntax'] = original_s05_allowed.copy()
                    print(f"  Fixed {ix['interaction_id']}: Restored original allowed syntax")
                
                # Fix s10: Restore original allowed syntax
                elif ix['interaction_id'] == 'ix.tile_pandas_dataframe_reading.s10':
                    ix['public']['constraints']['allowed_syntax'] = original_s10_allowed.copy()
                    print(f"  Fixed {ix['interaction_id']}: Restored original allowed syntax")

    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

print("\nPatching complete!")
