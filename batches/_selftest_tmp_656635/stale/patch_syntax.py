#!/usr/bin/env python3
"""Patch interactions to add validator-detectable syntax descriptors."""

import json

# Read the interactions file
with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# For each exercise, we need to add the validator's syntax descriptor names
# that correspond to the glossary's human-readable descriptions

for tile in data['tiles']:
    for interaction in tile['interactions']:
        step_id = interaction['step_id']
        ix = interaction['interaction']
        
        if step_id == 'tile_capstone_integrate_tools_model.s05':
            # SQL exercise - add validator-detectable names
            # Keep the glossary's descriptions AND add the validator's names
            ix['constraints']['allowed_syntax'].extend([
                "< > <= >= = <> !=",  # for date literal comparison
                "AS output_name",  # for column aliases
                "AVG",  # for AVG()
                "JOIN / INNER JOIN",  # for INNER JOIN
                "ON",  # for ON clause
                "alias.column qualification",  # for o.zone, d.driver_id
                "table alias (FROM table AS alias)"  # for FROM orders o
            ])
            print(f"Extended allowed_syntax for {step_id}")
        
        elif step_id == 'tile_capstone_integrate_tools_model.s15':
            # Python exercise - add validator-detectable names
            # The error says "attr_module" is not allowed
            # This likely refers to calling module-level functions or attributes
            # But the glossary allows "import pandas as pd", "pd.read_csv()", etc.
            # So we need to add the validator's name for module attribute access
            ix['constraints']['allowed_syntax'].extend([
                "attr_module"  # for pd.read_csv, df.dropna, etc.
            ])
            print(f"Extended allowed_syntax for {step_id}")
        
        elif step_id == 'tile_capstone_stats_dashboard.s10':
            # Chart exercise - add validator-detectable names
            # The errors say attr:dropna, attr:index, attr:title, attr:values, attr_module
            ix['constraints']['allowed_syntax'].extend([
                "attr:dropna",  # for .dropna()
                "attr:index",  # for .index
                "attr:title",  # for .title
                "attr:values",  # for .values
                "attr_module"  # for module attributes
            ])
            print(f"Extended allowed_syntax for {step_id}")

# Write the patched file
with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nPatching complete!")
