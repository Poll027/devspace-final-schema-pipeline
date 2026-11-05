#!/usr/bin/env python3
"""
Verify that the allowed_syntax constraint matches the glossary practice anchor.
This is the specific check that was failing in validate_tile.py.
"""
import json
import sys

def check_constraint_match():
    # Load glossary bundle
    with open('batches/final_batch_009_da_pandas/inputs/path_glossary_bundle.json', 'r') as f:
        glossary = json.load(f)
    
    # Find the practice anchor for pandas.apply_transform
    glossary_allowed = None
    glossary_blocked = None
    for bundle in glossary['bundles']:
        if bundle['context']['concept_id'] == 'pandas.apply_transform':
            practice = bundle.get('practice_anchor')
            if practice and 'live_code' in practice:
                glossary_allowed = practice['live_code']['allowed_syntax']
                glossary_blocked = practice['live_code']['blocked_syntax']
            break
    
    if not glossary_allowed:
        print("ERROR: Could not find glossary practice anchor")
        return False
    
    # Load interactions file
    with open('batches/final_batch_009_da_pandas/interactions.part.c3.json', 'r') as f:
        interactions = json.load(f)
    
    # Find the interaction for tile_pandas_map_apply.s07
    interaction_allowed = None
    interaction_blocked = None
    for tile in interactions['tiles']:
        if tile['tile_id'] == 'tile_pandas_map_apply':
            for ix in tile['interactions']:
                if ix['step_id'] == 'tile_pandas_map_apply.s07':
                    constraints = ix['interaction']['public']['constraints']
                    interaction_allowed = constraints['allowed_syntax']
                    interaction_blocked = constraints['blocked_syntax']
                    break
            break
    
    if not interaction_allowed:
        print("ERROR: Could not find interaction")
        return False
    
    # Check if they match
    allowed_match = glossary_allowed == interaction_allowed
    blocked_match = glossary_blocked == interaction_blocked
    
    print("Constraint verification for tile_pandas_map_apply.s07/ix.tile_pandas_map_apply.s07:")
    print(f"  allowed_syntax match: {allowed_match}")
    print(f"  blocked_syntax match: {blocked_match}")
    
    if allowed_match and blocked_match:
        print("✓ PASS: constraints match glossary practice anchor verbatim")
        return True
    else:
        print("✗ FAIL: constraints differ from glossary practice anchor")
        if not allowed_match:
            print(f"\n  Glossary allowed: {glossary_allowed}")
            print(f"  Interaction allowed: {interaction_allowed}")
        if not blocked_match:
            print(f"\n  Glossary blocked: {glossary_blocked}")
            print(f"  Interaction blocked: {interaction_blocked}")
        return False

if __name__ == '__main__':
    success = check_constraint_match()
    sys.exit(0 if success else 1)
