#!/usr/bin/env python3
"""
Reassemble screens.json from the part files.
"""
import json
from pathlib import Path

def main():
    batch_dir = Path('batches/final_batch_011_da_spreadsheet')
    
    # Read all part files
    part_files = sorted(batch_dir.glob('screens.part.*.json'))
    
    all_tiles = []
    base_data = None
    
    for part_file in part_files:
        with open(part_file, 'r') as f:
            part_data = json.load(f)
        
        if base_data is None:
            base_data = {
                'schema_version': part_data['schema_version'],
                'kind': part_data['kind'],
                'path_id': part_data['path_id'],
                'batch_id': part_data['batch_id']
            }
        
        all_tiles.extend(part_data['tiles'])
        print(f"Added {len(part_data['tiles'])} tiles from {part_file.name}")
    
    # Assemble the full screens file
    screens = {
        **base_data,
        'tiles': all_tiles
    }
    
    # Write the assembled file
    output_path = batch_dir / 'screens.json'
    with open(output_path, 'w') as f:
        json.dump(screens, f, indent=2)
    
    print(f"\nWrote {len(all_tiles)} tiles to screens.json")

if __name__ == '__main__':
    main()
