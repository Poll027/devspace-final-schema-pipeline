#!/usr/bin/env python3
"""
Patch interactions.part.c3.json based on evaluator findings.
"""
import json

# Read the current artifact
with open('batches/final_batch_009_da_pandas/interactions.part.c3.json', 'r') as f:
    data = json.load(f)

# Helper to find interaction by step_id
def find_interaction(tile_id, step_id):
    for tile in data['tiles']:
        if tile['tile_id'] == tile_id:
            for inter in tile['interactions']:
                if inter['step_id'] == step_id:
                    return inter
    return None

# ADVISORY 1: tile_pandas_map_apply/s02 - Set anchors to ['assessment:map_series_with_function']
print("Fixing tile_pandas_map_apply/s02 anchors...")
inter = find_interaction('tile_pandas_map_apply', 'tile_pandas_map_apply.s02')
if inter:
    inter['interaction']['anchors'] = ['assessment:map_series_with_function']
    print("  ✓ Set anchors=['assessment:map_series_with_function']")

# ADVISORY 2: tile_pandas_map_apply/s02 - Change remediation target
# The check tests f1 (function mapping), but remediation r01 re-teaches f2 (dict mapping)
# Change to r02 which teaches f1
print("\nFixing tile_pandas_map_apply/s02 remediation target...")
inter = find_interaction('tile_pandas_map_apply', 'tile_pandas_map_apply.s02')
if inter:
    current_rem = inter['interaction']['feedback'].get('remediation_step_id')
    print(f"  Current remediation_step_id: {current_rem}")
    # Change to r02 which teaches f1 (function mapping)
    inter['interaction']['feedback']['remediation_step_id'] = 'tile_pandas_map_apply.r02'
    print(f"  ✓ Changed remediation_step_id to tile_pandas_map_apply.r02")

# ADVISORY 3: tile_pandas_map_apply/s07 - Fix MEASURES anchor name
print("\nFixing tile_pandas_map_apply/s07 MEASURES anchor...")
inter = find_interaction('tile_pandas_map_apply', 'tile_pandas_map_apply.s07')
if inter:
    # The exercise uses axis=1 (row-wise), but measures claims apply_function_down_columns
    # Change to apply_function_across_rows_with_axis_1
    for measure in inter['interaction']['measures']:
        if measure['capability'] == 'apply_function_down_columns':
            measure['capability'] = 'apply_function_across_rows_with_axis_1'
            print(f"  ✓ Changed capability to 'apply_function_across_rows_with_axis_1'")

# ADVISORY 4: tile_pandas_pivot_export/s08 - Add test for index=False
print("\nFixing tile_pandas_pivot_export/s08 - adding index=False test...")
inter = find_interaction('tile_pandas_pivot_export', 'tile_pandas_pivot_export.s08')
if inter:
    # Add a test to verify index=False was used
    tests = inter['interaction']['grading']['tests']
    # Check if the test already exists
    has_index_test = any(
        'Unnamed: 0' in test.get('spec', {}).get('expr', '') 
        for test in tests if test['kind'] == 'value_equals'
    )
    if not has_index_test:
        # Add the test
        new_test = {
            "kind": "value_equals",
            "spec": {
                "expr": "'Unnamed: 0' not in pd.read_csv('cleaned_orders.csv').columns",
                "expected": True
            }
        }
        tests.append(new_test)
        print(f"  ✓ Added test to verify index=False")

# ADVISORY 5: tile_pandas_groupby_melt/s09 - Fix constraints.allowed
print("\nFixing tile_pandas_groupby_melt/s09 constraints.allowed...")
inter = find_interaction('tile_pandas_groupby_melt', 'tile_pandas_groupby_melt.s09')
if inter:
    allowed = inter['interaction']['public']['constraints']['allowed_syntax']
    # Find and replace value_name='value' with value_name='deliveries'
    for i, item in enumerate(allowed):
        if item == "value_name='value'":
            allowed[i] = "value_name='deliveries'"
            print(f"  ✓ Changed 'value_name='value'' to 'value_name='deliveries''")
            break

# ADVISORY 6: tile_pandas_concat_merge/s03 - Rephrase question stem
print("\nFixing tile_pandas_concat_merge/s03 question stem...")
inter = find_interaction('tile_pandas_concat_merge', 'tile_pandas_concat_merge.s03')
if inter:
    current_prompt = inter['interaction']['public']['prompt']
    print(f"  Current prompt: {current_prompt[:100]}...")
    # Change "Which call is correct?" to "Which is the most complete answer?"
    if "Which call is correct?" in current_prompt:
        new_prompt = current_prompt.replace("Which call is correct?", "Which is the most complete answer?")
        inter['interaction']['public']['prompt'] = new_prompt
        print(f"  ✓ Changed question stem to 'Which is the most complete answer?'")

# Write the patched artifact
with open('batches/final_batch_009_da_pandas/interactions.part.c3.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\n✓ Patched interactions.part.c3.json")
