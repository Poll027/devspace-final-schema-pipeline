#!/usr/bin/env python3
"""
Patch screens.part.c1.json to teach stats.lift_interpretation#f3 before it's tested.

The evaluator found that steps s06 and s07 test f3 but no earlier step teaches it.
We need to add a prose block to step s05 that teaches f3 (positive/negative/neutral interpretation).
"""

import json

# Read the current screens file
with open('screens.part.c1.json', 'r') as f:
    screens = json.load(f)

# Find tile_stats_ab_test_lift and step s05
tile = screens['tiles'][0]
assert tile['tile_id'] == 'tile_stats_ab_test_lift'

for step in tile['steps']:
    if step['step_id'] == 'tile_stats_ab_test_lift.s05':
        # Add a new prose block after the existing blocks that teaches f3
        # This should be inserted after the side_by_side (b4) but before any closing
        
        # Find the insertion point - after the last block
        last_block_id = step['blocks'][-1]['block_id']
        
        # Create new block that teaches f3
        new_block = {
            "type": "prose",
            "block_id": "tile_stats_ab_test_lift.s05.b5",
            "role": "interpretation",
            "text": "Analyzing an A/B test's results means determining whether the variation had a **positive**, **negative**, or **neutral** effect compared with the baseline (control). A **positive lift** means the variation's rate came out above the control's in this test. A **negative lift** means it came out below. A **neutral** result means the rates were effectively the same.",
            "lineage": {
                "concept_ids": [
                    "stats.lift_interpretation"
                ],
                "fact_ids": [
                    "stats.lift_interpretation#f3"
                ],
                "teaching_block_ids": [
                    "stats.lift_interpretation#tb4"
                ]
            }
        }
        
        # Insert the new block
        step['blocks'].append(new_block)
        
        # Update step lineage to include f3
        if 'stats.lift_interpretation#f3' not in step['lineage']['fact_ids']:
            step['lineage']['fact_ids'].append('stats.lift_interpretation#f3')
        if 'stats.lift_interpretation#tb4' not in step['lineage']['teaching_block_ids']:
            step['lineage']['teaching_block_ids'].append('stats.lift_interpretation#tb4')
        
        print(f"Added block {new_block['block_id']} to step {step['step_id']}")
        print(f"Block teaches fact: stats.lift_interpretation#f3")
        break

# Write the patched file
with open('screens.part.c1.json', 'w') as f:
    json.dump(screens, f, indent=2)

print("\nPatch complete. File written to screens.part.c1.json")
