#!/usr/bin/env python3
"""Merge workspace from top level into public and fix asset_ref -> asset_id."""

import json

def main():
    # Load the interactions file
    with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'r') as f:
        data = json.load(f)
    
    changes = []
    
    # Process each tile
    for tile in data['tiles']:
        for interaction_entry in tile['interactions']:
            step_id = interaction_entry['step_id']
            interaction = interaction_entry['interaction']
            
            if interaction['type'] == 'code_exercise':
                # Merge workspace from top level into public
                if 'workspace' in interaction:
                    top_ws = interaction['workspace']
                    if 'public' not in interaction:
                        interaction['public'] = {}
                    if 'workspace' not in interaction['public']:
                        interaction['public']['workspace'] = {}
                    
                    public_ws = interaction['public']['workspace']
                    
                    # Merge asset_mounts
                    if 'asset_mounts' in top_ws:
                        public_ws['asset_mounts'] = top_ws['asset_mounts']
                        changes.append(f"Merged asset_mounts into public.workspace for {step_id}")
                    
                    # Merge files if needed
                    if 'files' in top_ws and 'files' not in public_ws:
                        public_ws['files'] = top_ws['files']
                        changes.append(f"Merged files into public.workspace for {step_id}")
                    
                    # Merge entry if needed
                    if 'entry' in top_ws and 'entry' not in public_ws:
                        public_ws['entry'] = top_ws['entry']
                        changes.append(f"Merged entry into public.workspace for {step_id}")
                    
                    # Remove top-level workspace
                    del interaction['workspace']
                    changes.append(f"Removed top-level workspace for {step_id}")
                
                # Fix asset_ref -> asset_id in asset_mounts
                if 'public' in interaction and 'workspace' in interaction['public']:
                    mounts = interaction['public']['workspace'].get('asset_mounts', [])
                    for mount in mounts:
                        if 'asset_ref' in mount:
                            mount['asset_id'] = mount.pop('asset_ref')
                            changes.append(f"Fixed asset_ref -> asset_id for {step_id}")
    
    # Write the updated file
    with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Applied {len(changes)} changes:")
    for change in changes:
        print(f"  - {change}")
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
