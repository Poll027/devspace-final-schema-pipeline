#!/usr/bin/env python3
"""Patch code exercises to add workspace and fix column names."""

import json

def main():
    # Load the interactions file
    with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'r') as f:
        data = json.load(f)
    
    # Load registry to check available assets
    with open('batches/final_batch_012_da_viz/scenario_asset_registry.json', 'r') as f:
        registry = json.load(f)
    
    # Map file names to assets and column mappings
    file_to_asset = {
        'delivery_times.csv': {
            'asset_id': 'ds.orders',
            'column_map': {
                'delivery_time': 'delivery_time_minutes'
            }
        },
        'sales.csv': {
            'asset_id': 'ds.theming_demo',
            'column_map': {
                'region': 'category',
                'sales': 'value'
            }
        },
        'city_data.csv': {
            'asset_id': 'ds.orders',
            'column_map': {
                'city_data': 'orders',
                'population': 'num_items'  # This is a hack, but we need something
            }
        },
        'metrics.csv': {
            'asset_id': 'ds.chart_selection_mini',
            'column_map': {
                'metric_a': 'distance_km',
                'metric_b': 'delivery_minutes'
            }
        }
    }
    
    changes = []
    
    # Process each tile
    for tile in data['tiles']:
        tile_id = tile['tile_id']
        
        for interaction_entry in tile['interactions']:
            step_id = interaction_entry['step_id']
            interaction = interaction_entry['interaction']
            
            if interaction['type'] == 'code_exercise':
                # Get the solution to find what CSV file it uses
                solution_content = interaction['grading']['solution_files'][0]['content']
                
                # Find CSV file name
                import re
                csv_match = re.search(r"['\"]([^'\"]+\.csv)['\"]", solution_content)
                if csv_match:
                    csv_file = csv_match.group(1)
                    
                    if csv_file in file_to_asset:
                        asset_info = file_to_asset[csv_file]
                        asset_id = asset_info['asset_id']
                        column_map = asset_info['column_map']
                        
                        # Add workspace if missing
                        if 'workspace' not in interaction:
                            interaction['workspace'] = {
                                'files': [],
                                'asset_mounts': [],
                                'entry': 'solution.py'
                            }
                            changes.append(f"Added workspace to {step_id}")
                        
                        # Add asset mount
                        interaction['workspace']['asset_mounts'] = [{
                            'asset_ref': asset_id,
                            'mount_path': csv_file
                        }]
                        changes.append(f"Added asset_mount {asset_id} -> {csv_file} for {step_id}")
                        
                        # Fix column names in solution
                        new_solution = solution_content
                        for old_col, new_col in column_map.items():
                            new_solution = new_solution.replace(f"'{old_col}'", f"'{new_col}'")
                            new_solution = new_solution.replace(f'"{old_col}"', f'"{new_col}"')
                            new_solution = new_solution.replace(f"['{old_col}']", f"['{new_col}']")
                            new_solution = new_solution.replace(f'["{old_col}"]', f'["{new_col}"]')
                        
                        if new_solution != solution_content:
                            interaction['grading']['solution_files'][0]['content'] = new_solution
                            changes.append(f"Fixed column names in solution for {step_id}")
                        
                        # Fix column names in starter if it exists
                        if 'files' in interaction['workspace']:
                            for file_entry in interaction['workspace']['files']:
                                if file_entry.get('editable'):
                                    old_starter = file_entry['content']
                                    new_starter = old_starter
                                    for old_col, new_col in column_map.items():
                                        new_starter = new_starter.replace(f"'{old_col}'", f"'{new_col}'")
                                        new_starter = new_starter.replace(f'"{old_col}"', f'"{new_col}"')
                                        new_starter = new_starter.replace(f"['{old_col}']", f"['{new_col}']")
                                        new_starter = new_starter.replace(f'["{old_col}"]', f'["{new_col}"]')
                                    
                                    if new_starter != old_starter:
                                        file_entry['content'] = new_starter
                                        changes.append(f"Fixed column names in starter for {step_id}")
    
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
