#!/usr/bin/env python3
"""Fix allowed_syntax to match glossary practice anchor verbatim."""
import json

# Load glossary bundle to get the correct allowed_syntax
with open('batches/final_batch_009_da_pandas/inputs/path_glossary_bundle.json', 'r') as f:
    glossary = json.load(f)

# Find the practice anchor for pandas.apply_transform
correct_allowed_syntax = None
correct_blocked_syntax = None
for bundle in glossary['bundles']:
    if bundle['context']['concept_id'] == 'pandas.apply_transform':
        practice = bundle.get('practice_anchor')
        if practice and 'live_code' in practice:
            correct_allowed_syntax = practice['live_code']['allowed_syntax']
            correct_blocked_syntax = practice['live_code']['blocked_syntax']
        break

if not correct_allowed_syntax:
    print("ERROR: Could not find practice anchor")
    exit(1)

print("Correct allowed_syntax from glossary:")
print(json.dumps(correct_allowed_syntax, indent=2))
print("\nCorrect blocked_syntax from glossary:")
print(json.dumps(correct_blocked_syntax, indent=2))

# Load interactions file
with open('batches/final_batch_009_da_pandas/interactions.part.c3.json', 'r') as f:
    interactions = json.load(f)

# Find and fix the interaction for tile_pandas_map_apply.s07
fixed = False
for tile in interactions['tiles']:
    if tile['tile_id'] == 'tile_pandas_map_apply':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_pandas_map_apply.s07':
                print("\nOld allowed_syntax:")
                print(json.dumps(ix['interaction']['public']['constraints']['allowed_syntax'], indent=2))
                
                # Replace with correct values
                ix['interaction']['public']['constraints']['allowed_syntax'] = correct_allowed_syntax
                ix['interaction']['public']['constraints']['blocked_syntax'] = correct_blocked_syntax
                
                print("\nNew allowed_syntax:")
                print(json.dumps(ix['interaction']['public']['constraints']['allowed_syntax'], indent=2))
                fixed = True
                break
        break

if not fixed:
    print("ERROR: Could not find interaction to fix")
    exit(1)

# Write back
with open('batches/final_batch_009_da_pandas/interactions.part.c3.json', 'w') as f:
    json.dump(interactions, f, indent=2)

print("\n✓ Fixed allowed_syntax to match glossary practice anchor verbatim")
