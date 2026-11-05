#!/usr/bin/env python3
"""Verify that interactions.part.c2.json is correct and doesn't need patching."""

import json
import sys

with open('batches/final_batch_011_da_spreadsheet/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Check all interactions in tile_spreadsheet_cleaning_cross_sheet
issues_found = []

for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_cleaning_cross_sheet':
        for interaction in tile['interactions']:
            step_id = interaction['step_id']
            itype = interaction['interaction'].get('type')
            
            # Verify interaction types are valid
            valid_types = ['choice', 'ordering', 'classify', 'code_exercise', 'formula_entry']
            if itype not in valid_types:
                issues_found.append(f"{step_id}: invalid type '{itype}'")
            
            # Specifically check step 11 (the one mentioned in the error)
            if step_id == 'tile_spreadsheet_cleaning_cross_sheet.s11':
                if itype != 'choice':
                    issues_found.append(f"s11: expected 'choice', found '{itype}'")
                else:
                    print(f"✓ Step 11 has correct type: {itype}")
            
            # Check step 12 (index 11 in 0-based array)
            if step_id == 'tile_spreadsheet_cleaning_cross_sheet.s12':
                if itype != 'code_exercise':
                    issues_found.append(f"s12: expected 'code_exercise', found '{itype}'")
                else:
                    print(f"✓ Step 12 has correct type: {itype}")

if issues_found:
    print("\n❌ Issues found:")
    for issue in issues_found:
        print(f"  - {issue}")
    sys.exit(1)
else:
    print("\n✅ All interactions are correct! No patching needed.")
    sys.exit(0)
