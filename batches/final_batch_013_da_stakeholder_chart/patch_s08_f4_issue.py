#!/usr/bin/env python3
"""
Patch to fix s08 testing f4 without it being taught earlier.
The issue: s08 tests stakeholder.simplifying_charts_for_audience#f4,
but s06 (the explainer that introduces simplifying concepts) doesn't teach it.
Solution: Add f4 to s06's lineage.fact_ids.
"""

import json

# Read the screens file
with open('screens.part.c0_canary.json', 'r') as f:
    screens = json.load(f)

# Find s06 and add f4 to its lineage
tile = screens['tiles'][0]
for step in tile['steps']:
    if step['step_id'] == 'tile_stakeholder_chart_matching_simplifying.s06':
        # Check current fact_ids
        current_facts = step['lineage']['fact_ids']
        print(f"s06 current fact_ids: {current_facts}")
        
        # Add f4 if not present
        f4_full = 'stakeholder.simplifying_charts_for_audience#f4'
        if f4_full not in current_facts:
            # Insert f4 in the right position (after f3, before f5)
            # Current order: f1, f2, f3, f5, f6
            # Should be: f1, f2, f3, f4, f5, f6
            new_facts = []
            for fact in current_facts:
                new_facts.append(fact)
                if fact == 'stakeholder.simplifying_charts_for_audience#f3':
                    new_facts.append(f4_full)
            
            step['lineage']['fact_ids'] = new_facts
            print(f"s06 updated fact_ids: {new_facts}")
        else:
            print("f4 already present")

# Write back
with open('screens.part.c0_canary.json', 'w') as f:
    json.dump(screens, f, indent=2)

print("\nScreens file patched successfully.")
