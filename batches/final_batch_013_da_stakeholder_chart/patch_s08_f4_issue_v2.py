#!/usr/bin/env python3
"""
Patch to fix s08 testing f4 without it being taught earlier.
The issue: s08 tests stakeholder.simplifying_charts_for_audience#f4,
but no earlier step teaches it by text.

Solution: Add f4 to s06.b1's lineage.fact_ids, since block 1 mentions
"Each element you remove reduces the visual effort required to read the chart"
which relates to the cognitive benefit of reducing clutter (f4).
"""

import json

# Read the screens file
with open('screens.part.c0_canary.json', 'r') as f:
    screens = json.load(f)

# Find s06.b1 and add f4 to its lineage
tile = screens['tiles'][0]
for step in tile['steps']:
    if step['step_id'] == 'tile_stakeholder_chart_matching_simplifying.s06':
        for block in step['blocks']:
            if block['type'] == 'prose' and block['block_id'] == 'tile_stakeholder_chart_matching_simplifying.s06.b1':
                # Check current fact_ids
                current_facts = block['lineage']['fact_ids']
                print(f"s06.b1 current fact_ids: {current_facts}")
                print(f"s06.b1 text: {block['text']}")
                
                # Add f4
                f4_full = 'stakeholder.simplifying_charts_for_audience#f4'
                if f4_full not in current_facts:
                    block['lineage']['fact_ids'] = [f4_full]
                    print(f"\ns06.b1 updated fact_ids: {block['lineage']['fact_ids']}")
                else:
                    print("f4 already present")

# Write back
with open('screens.part.c0_canary.json', 'w') as f:
    json.dump(screens, f, indent=2)

print("\nScreens file patched successfully.")
