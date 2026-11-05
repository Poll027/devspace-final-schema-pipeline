#!/usr/bin/env python3
"""Move workspace and constraints into public for code_exercise interactions."""

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
                # Move workspace into public
                if 'workspace' in interaction and 'workspace' not in interaction.get('public', {}):
                    workspace = interaction.pop('workspace')
                    if 'public' not in interaction:
                        interaction['public'] = {}
                    interaction['public']['workspace'] = workspace
                    changes.append(f"Moved workspace into public for {step_id}")
                
                # Move constraints into public
                if 'constraints' in interaction and 'constraints' not in interaction.get('public', {}):
                    constraints = interaction.pop('constraints')
                    if 'public' not in interaction:
                        interaction['public'] = {}
                    interaction['public']['constraints'] = constraints
                    changes.append(f"Moved constraints into public for {step_id}")
    
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
