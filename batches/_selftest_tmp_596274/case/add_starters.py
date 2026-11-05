#!/usr/bin/env python3
"""Add starter files to code exercises."""

import json

def create_starter(solution_content, csv_file):
    """Create a starter file from the solution."""
    lines = solution_content.strip().split('\n')
    
    # Keep imports and data loading, add a comment for the rest
    starter_lines = []
    in_data_section = False
    
    for line in lines:
        if line.startswith('import ') or line.startswith('from '):
            starter_lines.append(line)
        elif 'pd.read_csv' in line or line.strip() == '# Data':
            starter_lines.append(line)
            in_data_section = True
        elif in_data_section and (line.strip() == '' or line.startswith('df = ')):
            starter_lines.append(line)
            if line.startswith('df = '):
                in_data_section = False
        elif not in_data_section and line.strip():
            # Add a comment for the rest
            if not any('# TODO' in l or '# Your code' in l for l in starter_lines):
                starter_lines.append('')
                starter_lines.append('# Your code here')
            break
    
    return '\n'.join(starter_lines) + '\n'

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
            
            if interaction['type'] == 'code_exercise' and 'workspace' in interaction:
                # Get the solution
                solution_content = interaction['grading']['solution_files'][0]['content']
                
                # Find CSV file name
                import re
                csv_match = re.search(r"['\"]([^'\"]+\.csv)['\"]", solution_content)
                csv_file = csv_match.group(1) if csv_match else 'data.csv'
                
                # Create starter
                starter_content = create_starter(solution_content, csv_file)
                
                # Add starter file if files list is empty
                if not interaction['workspace']['files']:
                    interaction['workspace']['files'] = [{
                        'path': 'solution.py',
                        'language': 'python',
                        'editable': True,
                        'content': starter_content
                    }]
                    changes.append(f"Added starter file to {step_id}")
    
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
