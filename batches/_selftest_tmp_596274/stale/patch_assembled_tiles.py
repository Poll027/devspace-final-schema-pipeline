#!/usr/bin/env python3
"""
Patch the assembled tiles directly to fix validation errors.
"""
import json

# Read the patched interactions
with open('batches/final_batch_012_da_viz/interactions.part.c2.json') as f:
    interactions_data = json.load(f)

# Build a map of step_id -> interaction
interactions_map = {}
for tile in interactions_data['tiles']:
    for ix_entry in tile['interactions']:
        interactions_map[ix_entry['step_id']] = ix_entry['interaction']

# Patch each assembled tile
for tile_id in ['tile_viz_labeling_chart_selection', 'tile_viz_custom_multi_panel', 'tile_viz_seaborn_stats_themes']:
    tile_path = f'batches/final_batch_012_da_viz/tile_lessons/{tile_id}.json'
    
    with open(tile_path) as f:
        tile = json.load(f)
    
    print(f"Patching {tile_id}...")
    
    # Update interactions in steps
    for step in tile['steps']:
        step_id = step['step_id']
        if step_id in interactions_map:
            step['interaction'] = interactions_map[step_id]
            # Remove execution_provenance and hidden_checks (will be recomputed)
            if step['interaction'].get('type') == 'code_exercise':
                step['interaction']['grading'].pop('execution_provenance', None)
                step['interaction']['grading'].pop('hidden_checks', None)
            print(f"  Updated {step_id}")
    
    # Fix s11 lineage for tile_viz_labeling_chart_selection
    if tile_id == 'tile_viz_labeling_chart_selection':
        for step in tile['steps']:
            if step['step_id'] == 'tile_viz_labeling_chart_selection.s11':
                # Fix the lineage
                step['lineage']['teaching_block_ids'] = ['viz.chart_type_selection#tb3']
                # Also fix the block lineage
                for block in step.get('blocks', []):
                    if block.get('lineage'):
                        block['lineage']['teaching_block_ids'] = ['viz.chart_type_selection#tb3']
                print(f"  Fixed s11 lineage")
    
    # Move remediation steps from steps to remediation_steps
    new_steps = []
    new_remediation_steps = []
    for step in tile['steps']:
        if step['type'] == 'remediation':
            new_remediation_steps.append(step)
        else:
            new_steps.append(step)
    
    if new_remediation_steps:
        print(f"  Moved {len(new_remediation_steps)} remediation steps")
        tile['steps'] = new_steps
        tile['remediation_steps'] = new_remediation_steps
    
    # Recompute content_hash
    import hashlib
    tile_copy = {k: v for k, v in tile.items() if k != 'content_hash'}
    content_json = json.dumps(tile_copy, sort_keys=True, separators=(',', ':'))
    tile['content_hash'] = hashlib.sha256(content_json.encode()).hexdigest()
    
    with open(tile_path, 'w') as f:
        json.dump(tile, f, indent=2)
    
    print(f"  Saved {tile_path}")

print("Done patching assembled tiles")
