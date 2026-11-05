#!/usr/bin/env python3
"""Patch the allowed_syntax constraints to match glossary practice anchors exactly."""
import json

# Load the interactions file
with open('batches/final_batch_009_da_pandas/interactions.part.c0_canary.json', 'r') as f:
    interactions = json.load(f)

# Define the correct constraints from glossary practice anchors
correct_constraints = {
    'pandas.dataframe_series_model': {
        'allowed_syntax': [
            "import pandas as pd",
            "pd.Series(list)",
            "pd.DataFrame(dict_of_lists)",
            "df['col']",
            "print()",
            "type()"
        ],
        'blocked_syntax': [
            "pd.read_csv",
            "df.head()",
            "df.shape",
            "df.info()",
            "df.loc",
            "df.iloc",
            "boolean filtering"
        ]
    },
    'pandas.reading_data': {
        'allowed_syntax': [
            "import pandas as pd",
            "pd.read_csv(path)",
            "pd.read_csv(path, sep=...)",
            "pd.read_excel(path, sheet_name=...)",
            "print(df)"
        ],
        'blocked_syntax': [
            "df.shape",
            "df.head()",
            "df.info()",
            "df.describe()",
            "df.dtypes"
        ]
    }
}

# Patch the interactions
for tile in interactions.get('tiles', []):
    if tile.get('tile_id') == 'tile_pandas_dataframe_reading':
        for ix_wrapper in tile.get('interactions', []):
            step_id = ix_wrapper.get('step_id', '')
            ix = ix_wrapper.get('interaction', {})
            
            # Determine which concept this interaction measures
            measures = ix.get('measures', [])
            if not measures:
                continue
            
            primary_concept = measures[0].get('concept_id')
            
            # Patch s05 (pandas.dataframe_series_model)
            if 's05' in step_id and primary_concept == 'pandas.dataframe_series_model':
                print(f"Patching {step_id} with pandas.dataframe_series_model constraints")
                ix['public']['constraints']['allowed_syntax'] = correct_constraints['pandas.dataframe_series_model']['allowed_syntax']
                ix['public']['constraints']['blocked_syntax'] = correct_constraints['pandas.dataframe_series_model']['blocked_syntax']
            
            # Patch s10 (pandas.reading_data)
            elif 's10' in step_id and primary_concept == 'pandas.reading_data':
                print(f"Patching {step_id} with pandas.reading_data constraints")
                ix['public']['constraints']['allowed_syntax'] = correct_constraints['pandas.reading_data']['allowed_syntax']
                ix['public']['constraints']['blocked_syntax'] = correct_constraints['pandas.reading_data']['blocked_syntax']

# Write the patched file
with open('batches/final_batch_009_da_pandas/interactions.part.c0_canary.json', 'w') as f:
    json.dump(interactions, f, indent=2)

print("\nPatching complete!")
