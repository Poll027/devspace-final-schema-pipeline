#!/usr/bin/env python3
"""Patch screens files to teach fact f4 by text in step s07 (after the video)."""

import json

def patch_screens_file(filepath):
    """Patch a screens file to add f4 teaching in s07."""
    with open(filepath, 'r') as f:
        screens = json.load(f)

    # Find tile_stakeholder_chart_matching_simplifying
    for tile in screens['tiles']:
        if tile['tile_id'] == 'tile_stakeholder_chart_matching_simplifying':
            # First, remove the f4 block from s06 if it exists
            for step in tile['steps']:
                if step['step_id'] == 'tile_stakeholder_chart_matching_simplifying.s06':
                    # Remove the b3_takeaway block if it exists
                    step['blocks'] = [b for b in step['blocks'] if b.get('block_id') != 'tile_stakeholder_chart_matching_simplifying.s06.b3_takeaway']
                    # Remove f4 from lineage
                    step['lineage']['fact_ids'] = [f for f in step['lineage']['fact_ids'] if f != 'stakeholder.simplifying_charts_for_audience#f4']
                    step['lineage']['teaching_block_ids'] = [t for t in step['lineage']['teaching_block_ids'] if t != 'stakeholder.simplifying_charts_for_audience#tb4']
                    break
            
            # Now add a callout to s07 that teaches f4
            for step in tile['steps']:
                if step['step_id'] == 'tile_stakeholder_chart_matching_simplifying.s07':
                    # Check if we already added the callout
                    has_f4_callout = any(
                        block['type'] == 'callout' and 'stakeholder.simplifying_charts_for_audience#f4' in block.get('lineage', {}).get('fact_ids', [])
                        for block in step['blocks']
                    )
                    
                    if has_f4_callout:
                        print(f"  {filepath}: already has f4 callout in s07")
                        return False
                    
                    # Add a callout block after the media_group
                    callout_block = {
                        "type": "callout",
                        "block_id": "tile_stakeholder_chart_matching_simplifying.s07.b2",
                        "callout_kind": "key_point",
                        "title": "Why remove clutter?",
                        "text": "Reducing clutter lets the audience use their attention to decide what actions might be warranted, rather than working out how to read the graph.",
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
                    
                    # Append after the media_group
                    step['blocks'].append(callout_block)
                    
                    # Update the step's lineage to include tb4
                    if 'stakeholder.simplifying_charts_for_audience#tb4' not in step['lineage'].get('teaching_block_ids', []):
                        if 'teaching_block_ids' not in step['lineage']:
                            step['lineage']['teaching_block_ids'] = []
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
        print(f"Patched {filepath}: added callout teaching f4 in step s07")
    else:
        print(f"Skipped {filepath}: already patched")
