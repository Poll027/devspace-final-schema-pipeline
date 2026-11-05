#!/usr/bin/env python3
"""Fix remediation mismatches in interactions.part.c1.json"""
import json

with open('batches/final_batch_011_da_spreadsheet/interactions.part.c1.json') as f:
    interactions = json.load(f)

# Fix s02: remove remediation_step_id because r01 teaches f1,f2 but check measures f3
for tile in interactions['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_text_date_conditional_agg':
        for interaction_entry in tile['interactions']:
            if interaction_entry['step_id'] == 'tile_spreadsheet_text_date_conditional_agg.s02':
                ix = interaction_entry['interaction']
                if 'feedback' in ix and 'remediation_step_id' in ix['feedback']:
                    del ix['feedback']['remediation_step_id']
                    print(f"Removed remediation_step_id from s02")
            
            # Fix s07: remove remediation_step_id because r02 teaches f3,f4 but check measures f1,f2
            elif interaction_entry['step_id'] == 'tile_spreadsheet_text_date_conditional_agg.s07':
                ix = interaction_entry['interaction']
                if 'feedback' in ix and 'remediation_step_id' in ix['feedback']:
                    del ix['feedback']['remediation_step_id']
                    print(f"Removed remediation_step_id from s07")

with open('batches/final_batch_011_da_spreadsheet/interactions.part.c1.json', 'w') as f:
    json.dump(interactions, f, indent=2, ensure_ascii=False)

print("Remediation mismatches fixed")
