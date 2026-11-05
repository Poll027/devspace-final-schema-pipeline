#!/usr/bin/env python3
"""Remove workspace and constraints from top level of code_exercise interactions."""

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
                # Remove workspace from top level if it's in public
                if 'workspace' in interaction and 'workspace' in interaction.get('public', {}):
                    interaction.pop('workspace')
                    changes.append(f"Removed workspace from top level for {step_id}")
                
                # Remove constraints from top level if it's in public
                if 'constraints' in interaction and 'constraints' in interaction.get('public', {}):
                    interaction.pop('constraints')
                    changes.append(f"Removed constraints from top level for {step_id}")
    
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
