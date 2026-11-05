#!/usr/bin/env python3
"""
Run code exercises to generate hidden_checks and execution_provenance.
"""
import json
import sys
sys.path.insert(0, '00_FINAL_PIPELINE_CORE/scripts')
from checkers import sandbox

# Load registry
with open('batches/final_batch_012_da_viz/scenario_asset_registry.json') as f:
    registry = json.load(f)

# Load tiles
for tile_id in ['tile_viz_labeling_chart_selection', 'tile_viz_custom_multi_panel', 'tile_viz_seaborn_stats_themes']:
    tile_path = f'batches/final_batch_012_da_viz/tile_lessons/{tile_id}.json'
    
    with open(tile_path) as f:
        tile = json.load(f)
    
    print(f"Processing {tile_id}...")
    
    # Process each step
    for step in tile['steps']:
        ix = step.get('interaction')
        if ix and ix.get('type') == 'code_exercise':
            step_id = step['step_id']
            print(f"  Running {step_id}...")
            
            try:
                result = sandbox.run_exercise(registry, ix)
                
                if result.provenance:
                    ix['grading']['execution_provenance'] = result.provenance
                    print(f"    Added execution_provenance")
                
                if result.hidden_checks:
                    ix['grading']['hidden_checks'] = result.hidden_checks
                    print(f"    Added {len(result.hidden_checks)} hidden_checks")
                
                if result.problems:
                    print(f"    Problems: {result.problems[:3]}")
            
            except Exception as e:
                print(f"    ERROR: {e}")
    
    # Recompute content_hash
    import hashlib
    tile_copy = {k: v for k, v in tile.items() if k != 'content_hash'}
    content_json = json.dumps(tile_copy, sort_keys=True, separators=(',', ':'))
    tile['content_hash'] = hashlib.sha256(content_json.encode()).hexdigest()
    
    with open(tile_path, 'w') as f:
        json.dump(tile, f, indent=2)
    
    print(f"  Saved {tile_path}")

print("Done")
