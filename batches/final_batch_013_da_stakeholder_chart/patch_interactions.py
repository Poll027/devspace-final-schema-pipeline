#!/usr/bin/env python3
"""Patch interactions.part.c0_canary.json with advisory fixes."""

import json

# Read the artifact
with open('batches/final_batch_013_da_stakeholder_chart/interactions.part.c0_canary.json', 'r') as f:
    data = json.load(f)

# Find the tile
tile = data['tiles'][0]
interactions = tile['interactions']

# Fix 1: s05 item_4 - rephrase to avoid "distribution"
for interaction_obj in interactions:
    if interaction_obj['step_id'] == 'tile_stakeholder_chart_matching_simplifying.s05':
        items = interaction_obj['interaction']['public']['items']
        for item in items:
            if item['item_id'] == 'item_4':
                item['text'] = 'Show how delivery times differ across all three cities for the operations manager.'
        print("✓ Fixed s05 item_4: rephrased to avoid 'distribution'")
        break

# Fix 2: s10 - add one element that should be kept
for interaction_obj in interactions:
    if interaction_obj['step_id'] == 'tile_stakeholder_chart_matching_simplifying.s10':
        items = interaction_obj['interaction']['public']['items']
        # Add a new item that should be kept
        new_item = {
            "item_id": "item_6",
            "text": "Axis title showing 'Delivery Time (min)'"
        }
        items.append(new_item)
        
        # Update grading assignments
        interaction_obj['interaction']['grading']['assignments']['item_6'] = 'cat_keep'
        
        # Update feedback to reflect the new item
        correct_msg = interaction_obj['interaction']['feedback']['correct']['message']
        # Replace the message to account for 5 removes and 1 keep
        new_correct_msg = "Excellent! You correctly identified which elements to remove and which to keep. The border, gridlines, trailing zeros, rotated labels, and redundant data labels should all be removed \u2014 they add visual effort without adding information. The axis title should be kept because it provides essential context for interpreting the chart values."
        interaction_obj['interaction']['feedback']['correct']['message'] = new_correct_msg
        
        print("✓ Fixed s10: added item_6 (axis title) to 'Keep' bucket")
        break

# Write the patched artifact
with open('batches/final_batch_013_da_stakeholder_chart/interactions.part.c0_canary.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\n✓ Patched artifact written successfully")
