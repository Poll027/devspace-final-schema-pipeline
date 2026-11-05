#!/usr/bin/env python3
"""Check if allowed_syntax matches glossary practice anchor."""
import json

# Load glossary bundle
with open('batches/final_batch_009_da_pandas/inputs/path_glossary_bundle.json', 'r') as f:
    glossary = json.load(f)

# Find the practice anchor for pandas.apply_transform
glossary_allowed = None
for bundle in glossary['bundles']:
    if bundle['context']['concept_id'] == 'pandas.apply_transform':
        practice = bundle.get('practice_anchor')
        if practice and 'live_code' in practice:
            glossary_allowed = practice['live_code']['allowed_syntax']
        break

# Load interactions file
with open('batches/final_batch_009_da_pandas/interactions.part.c3.json', 'r') as f:
    interactions = json.load(f)

# Find the interaction for tile_pandas_map_apply.s07
interaction_allowed = None
for tile in interactions['tiles']:
    if tile['tile_id'] == 'tile_pandas_map_apply':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_pandas_map_apply.s07':
                interaction_allowed = ix['interaction']['public']['constraints']['allowed_syntax']
                break
        break

print("Glossary practice anchor allowed_syntax:")
print(json.dumps(glossary_allowed, indent=2))
print("\nInteraction allowed_syntax:")
print(json.dumps(interaction_allowed, indent=2))
print("\nMatch:", glossary_allowed == interaction_allowed)

if glossary_allowed == interaction_allowed:
    print("✓ PASS: allowed_syntax matches glossary practice anchor verbatim")
    exit(0)
else:
    print("✗ FAIL: allowed_syntax differs from glossary practice anchor")
    exit(1)
