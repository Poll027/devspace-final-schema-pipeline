#!/usr/bin/env python3
"""
Patch s11 interaction to add a visible test checking len(df) after dropna step.
Advisory: drop_rows_missing_required_field(f2) is claimed as measured but no test 
verifies dropna() was actually called.
"""
import json

# Read the artifact
with open('interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Find the s11 interaction
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_pandas_text_dupes_missing':
        for interaction_entry in tile['interactions']:
            if interaction_entry['step_id'] == 'tile_pandas_text_dupes_missing.s11':
                interaction = interaction_entry['interaction']
                
                # Add a new test to verify len(df) after dropna
                # The test should check that df has 15 rows (no rows were dropped since no order_id is missing)
                new_test = {
                    "test_id": "t2",
                    "kind": "value_equals",
                    "spec": {
                        "expr": "len(df)",
                        "expected": 15
                    },
                    "visible": True,
                    "message_on_fail": "After dropna(subset=['order_id']), the DataFrame should have 15 rows (no order_id values are missing in this dataset)."
                }
                
                # Insert the new test after t1
                interaction['grading']['tests'].append(new_test)
                
                print("Added test t2 to verify len(df) after dropna step")
                break

# Write the patched artifact
with open('interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Patch complete")
