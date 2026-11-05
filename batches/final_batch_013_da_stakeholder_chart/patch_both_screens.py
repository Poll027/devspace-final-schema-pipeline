#!/usr/bin/env python3
"""Patch both screens.json and screens.part.c0_canary.json to teach fact f4 before step s08 tests it."""

import json

def patch_screens_file(filepath):
    """Patch a screens file to add f4 teaching before s08."""
    with open(filepath, 'r') as f:
        screens = json.load(f)

    # Find tile_stakeholder_chart_matching_simplifying
    for tile in screens['tiles']:
        if tile['tile_id'] == 'tile_stakeholder_chart_matching_simplifying':
            # Find step s06 (the explainer that teaches simplifying)
            for step in tile['steps']:
                if step['step_id'] == 'tile_stakeholder_chart_matching_simplifying.s06':
                    # Check if we already added the block
                    has_f4_block = any(
                        'stakeholder.simplifying_charts_for_audience#f4' in block.get('lineage', {}).get('fact_ids', [])
                        for block in step['blocks']
                        if block['type'] == 'prose'
                    )
                    
                    if has_f4_block:
                        print(f"  {filepath}: already has f4 teaching block")
                        return False
                    
                    # Add a new prose block after b2 that teaches f4
                    new_block = {
                        "type": "prose",
                        "block_id": "tile_stakeholder_chart_matching_simplifying.s06.b3_takeaway",
                        "role": "takeaway",
                        "text": "Reducing clutter lets the audience use their attention to decide what actions might be warranted, rather than working out how to read the graph. None of these changes alter the underlying delivery-time values — only how much visual effort it takes to read them.",
                        "lineage": {
                            "concept_ids": [
                                "stakeholder.simplifying_charts_for_audience"
                            ],
                            "teaching_block_ids": [
                                "stakeholder.simplifying_charts_for_audience#tb4"
                            ],
                            "fact_ids": [
                                "stakeholder.simplifying_charts_for_audience#f4"
                            ]
                        }
                    }
                    
                    # Find the index of b2
                    b2_index = None
                    for i, block in enumerate(step['blocks']):
                        if block.get('block_id') == 'tile_stakeholder_chart_matching_simplifying.s06.b2':
                            b2_index = i
                            break
                    
                    if b2_index is not None:
                        # Insert after b2
                        step['blocks'].insert(b2_index + 1, new_block)
                        
                        # Update the step's lineage to include f4
                        if 'stakeholder.simplifying_charts_for_audience#f4' not in step['lineage']['fact_ids']:
                            step['lineage']['fact_ids'].append('stakeholder.simplifying_charts_for_audience#f4')
                        
                        # Also add tb4 to teaching_block_ids if not present
                        if 'stakeholder.simplifying_charts_for_audience#tb4' not in step['lineage']['teaching_block_ids']:
                            step['lineage']['teaching_block_ids'].append('stakeholder.simplifying_charts_for_audience#tb4')
                    
                    break
            break

    # Write the patched file
    with open(filepath, 'w') as f:
        json.dump(screens, f, indent=2)
    
    return True

# Patch both files
for filepath in ['screens.json', 'screens.part.c0_canary.json']:
    if patch_screens_file(filepath):
        print(f"Patched {filepath}: added prose block teaching f4 in step s06")
    else:
        print(f"Skipped {filepath}: already patched")
