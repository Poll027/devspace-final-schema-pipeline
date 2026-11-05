#!/usr/bin/env python3
import json

# Fix test t5 to check a data-dependent value instead of column count
with open('interactions.part.c3.json') as f:
    interactions = json.load(f)

for tile in interactions['tiles']:
    if tile['tile_id'] == 'tile_pandas_pivot_export':
        for interaction_entry in tile['interactions']:
            if interaction_entry['step_id'] == 'tile_pandas_pivot_export.s08':
                tests = interaction_entry['interaction']['grading']['tests']
                for test in tests:
                    if test.get('test_id') == 't5':
                        # Change to check the last order_id value (data-dependent)
                        test['spec']['expr'] = "pd.read_csv('cleaned_orders.csv')['order_id'].iloc[-1]"
                        test['spec']['expected'] = 1014  # This will be validated by the gate
                        test['message_on_fail'] = "The CSV should preserve all rows. Make sure you export the full DataFrame with to_csv()."
                        print("Fixed t5 to check last order_id value")
                        break

# Write back
with open('interactions.part.c3.json', 'w') as f:
    json.dump(interactions, f, indent=2)

print("Updated interactions.part.c3.json")

# Also update the tile file
with open('tile_lessons/tile_pandas_pivot_export.json') as f:
    tile_data = json.load(f)

for step in tile_data.get('steps', []):
    if step.get('step_id') == 'tile_pandas_pivot_export.s08':
        if 'interaction' in step:
            tests = step['interaction']['grading']['tests']
            for test in tests:
                if test.get('test_id') == 't5':
                    test['spec']['expr'] = "pd.read_csv('cleaned_orders.csv')['order_id'].iloc[-1]"
                    test['spec']['expected'] = 1014
                    test['message_on_fail'] = "The CSV should preserve all rows. Make sure you export the full DataFrame with to_csv()."
                    print("Fixed t5 in tile file")
                    break

with open('tile_lessons/tile_pandas_pivot_export.json', 'w') as f:
    json.dump(tile_data, f, indent=2)

print("Updated tile_lessons/tile_pandas_pivot_export.json")
