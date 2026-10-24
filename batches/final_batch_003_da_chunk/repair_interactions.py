#!/usr/bin/env python3
"""
Repair script for interactions.part.c2.json based on evaluator findings.
"""
import json

# Read the artifact
with open('batches/final_batch_003_da_chunk/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Find the tile_datamodel_dimensional_er tile
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_datamodel_dimensional_er':
        # Find s03 interaction
        for interaction_wrapper in tile['interactions']:
            if interaction_wrapper['step_id'] == 'tile_datamodel_dimensional_er.s03':
                interaction = interaction_wrapper['interaction']
                # ADVISORY: Reword opt_correct text
                for option in interaction['public']['options']:
                    if option['option_id'] == 'opt_correct':
                        option['text'] = "Each order must be linked to exactly one customer (mandatory), and one customer can be linked to many orders"
                        break
            
            # Find s04 interaction (classify)
            elif interaction_wrapper['step_id'] == 'tile_datamodel_dimensional_er.s04':
                interaction = interaction_wrapper['interaction']
                
                # BLOCKING: Add bkt_not_erd bucket
                new_bucket = {
                    "bucket_id": "bkt_not_erd",
                    "label": "Not an ERD element (data value, not structure)"
                }
                interaction['public']['buckets'].append(new_bucket)
                
                # BLOCKING: Change grading assignment for item_trap_customer_id_number
                interaction['grading']['assignments']['item_trap_customer_id_number'] = 'bkt_not_erd'
                
                # BLOCKING: Add to role_map
                interaction['grading']['role_map']['bkt_not_erd'] = 'not_erd_element'
                
                # BLOCKING: Update item_feedback for item_trap_customer_id_number
                interaction['grading']['item_feedback']['item_trap_customer_id_number']['message'] = \
                    "Correct. This is a data value (the integer 1 stored in a row), not an ERD element. In an ERD, customer_id appears as an underlined oval (a primary key attribute), not as a row value. The ERD shows structure, not data."
    
    # Find tile_stakeholder_recommendation_translation tile
    elif tile['tile_id'] == 'tile_stakeholder_recommendation_translation':
        # Find s06 interaction
        for interaction_wrapper in tile['interactions']:
            if interaction_wrapper['step_id'] == 'tile_stakeholder_recommendation_translation.s06':
                interaction = interaction_wrapper['interaction']
                
                # ADVISORY: Strengthen feedback for item_both
                interaction['grading']['item_feedback']['item_both']['message'] = \
                    "Correct. 'The average (mean)' glosses the specialist term (Rule 1), and the sentence replaces formal alternatives with plain words like 'rose' instead of 'increased' and 'recommend' instead of 'advise' (Rule 2). Both rules are applied."

# Write the repaired artifact
with open('batches/final_batch_003_da_chunk/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Repairs applied successfully")
