#!/usr/bin/env python3
import json

# Read the interactions file
with open('interactions.part.c3.json') as f:
    interactions = json.load(f)

changes_made = []

# Fix 1: Add measurement for apply_function_down_columns in tile_pandas_map_apply.s07
for tile in interactions['tiles']:
    if tile['tile_id'] == 'tile_pandas_map_apply':
        for interaction_entry in tile['interactions']:
            if interaction_entry['step_id'] == 'tile_pandas_map_apply.s07':
                # Add the missing measurement
                measures = interaction_entry['interaction']['measures']
                # Check if it's already there
                has_apply_down = any(
                    m.get('capability') == 'apply_function_down_columns' 
                    for m in measures
                )
                if not has_apply_down:
                    measures.append({
                        "concept_id": "pandas.apply_transform",
                        "capability": "apply_function_down_columns",
                        "fact_ids": ["f1"]
                    })
                    changes_made.append("Added measurement for apply_function_down_columns in tile_pandas_map_apply.s07")

# Fix 2: Fix the allowed_syntax for tile_pandas_groupby_melt.s09
# The correct allowed_syntax from glossary is:
correct_melt_syntax = [
    "df.melt(id_vars=[...])",
    "pd.melt(df, id_vars=[...])",
    "var_name='month'",
    "value_name='value'",
    "print()"
]

for tile in interactions['tiles']:
    if tile['tile_id'] == 'tile_pandas_groupby_melt':
        for interaction_entry in tile['interactions']:
            if interaction_entry['step_id'] == 'tile_pandas_groupby_melt.s09':
                old_syntax = interaction_entry['interaction']['public']['constraints']['allowed_syntax']
                interaction_entry['interaction']['public']['constraints']['allowed_syntax'] = correct_melt_syntax
                changes_made.append(f"Fixed allowed_syntax for tile_pandas_groupby_melt.s09")

# Fix 3: Fix tile_pandas_pivot_export.s08 test t5 to depend on data
for tile in interactions['tiles']:
    if tile['tile_id'] == 'tile_pandas_pivot_export':
        for interaction_entry in tile['interactions']:
            if interaction_entry['step_id'] == 'tile_pandas_pivot_export.s08':
                tests = interaction_entry['interaction']['grading']['tests']
                for test in tests:
                    if test.get('test_id') == 't5':
                        # Change to check number of columns (which depends on the data structure)
                        test['spec']['expr'] = "len(pd.read_csv('cleaned_orders.csv').columns)"
                        test['spec']['expected'] = 4  # order_id, customer_id, city_code, order_value
                        test['message_on_fail'] = "The CSV should have 4 columns. Make sure you export with index=False."
                        changes_made.append("Fixed test t5 in tile_pandas_pivot_export.s08 to check column count")
                        break

print("Changes made:")
for change in changes_made:
    print(f"  - {change}")

# Write the fixed file
with open('interactions.part.c3.json', 'w') as f:
    json.dump(interactions, f, indent=2)
    
print("\nFile updated successfully.")
