#!/usr/bin/env python3
"""
Fix: restore f5 to s12.p2 block fact_ids so s15 can test it.
The step-level teaching_block_ids is already correct (only tb4).
"""
import json
from pathlib import Path

B = Path('batches/final_batch_011_da_spreadsheet')

with open(B / 'screens.part.c2.json') as f:
    part = json.load(f)

for tile in part['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_lookups_troubleshooting':
        for step in tile['steps']:
            if step['step_id'] == 'tile_spreadsheet_lookups_troubleshooting.s12':
                for block in step.get('blocks', []):
                    if block.get('block_id') == 'tile_spreadsheet_lookups_troubleshooting.s12.p2':
                        blin = block.get('lineage', {})
                        # Restore f5 so s15 can test it (taught-before-tested rule)
                        if 'spreadsheet.formula_error_troubleshooting#f5' not in blin.get('fact_ids', []):
                            blin['fact_ids'] = ['spreadsheet.formula_error_troubleshooting#f5']
                            print(f"Restored f5 to s12.p2 fact_ids: {blin['fact_ids']}")
                        # Also restore step-level fact_ids to include f5
                        step_lin = step['lineage']
                        if 'spreadsheet.formula_error_troubleshooting#f5' not in step_lin.get('fact_ids', []):
                            step_lin['fact_ids'].append('spreadsheet.formula_error_troubleshooting#f5')
                            print(f"Restored f5 to step lineage.fact_ids: {step_lin['fact_ids']}")
                break

with open(B / 'screens.part.c2.json', 'w') as f:
    json.dump(part, f, indent=2)
print("Wrote screens.part.c2.json")

# --- Rebuild screens.json from all parts ---
part_files = sorted(B.glob('screens.part.*.json'))
all_tiles = []
base_data = None
for part_file in part_files:
    with open(part_file) as f:
        pdata = json.load(f)
    if base_data is None:
        base_data = {
            'schema_version': pdata['schema_version'],
            'kind': pdata['kind'],
            'path_id': pdata['path_id'],
            'batch_id': pdata['batch_id'],
        }
    all_tiles.extend(pdata['tiles'])

screens = {**base_data, 'tiles': all_tiles}
with open(B / 'screens.json', 'w') as f:
    json.dump(screens, f, indent=2)
print(f"Wrote screens.json ({len(all_tiles)} tiles)")
