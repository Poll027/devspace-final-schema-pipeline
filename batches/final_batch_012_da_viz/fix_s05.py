#!/usr/bin/env python3
"""Add workspace to s05."""

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
            
            if step_id == 'tile_viz_labeling_chart_selection.s05':
                if 'workspace' not in interaction:
                    solution = interaction['grading']['solution_files'][0]['content']
                    
                    # Create starter - keep data and imports, remove plotting code
                    lines = solution.strip().split('\n')
                    starter_lines = []
                    for line in lines:
                        if line.startswith('import ') or line.startswith('from ') or '# Data' in line or line.startswith('day_') or line.startswith('days ') or line.startswith('lagos_') or line.startswith('abuja_'):
                            starter_lines.append(line)
                        elif line.strip() == '':
                            starter_lines.append(line)
                        else:
                            break
                    
                    starter_lines.append('')
                    starter_lines.append('# Your code here')
                    starter_content = '\n'.join(starter_lines) + '\n'
                    
                    interaction['workspace'] = {
                        'files': [{
                            'path': 'solution.py',
                            'language': 'python',
                            'editable': True,
                            'content': starter_content
                        }],
                        'asset_mounts': [],
                        'entry': 'solution.py'
                    }
                    changes.append(f"Added workspace to {step_id}")
    
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
