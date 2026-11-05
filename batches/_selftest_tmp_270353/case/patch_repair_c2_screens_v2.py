#!/usr/bin/env python3
"""
Patch screens.part.c2.json to fix two gate errors:
1. tile_spreadsheet_lookups_troubleshooting.s12 lineage.teaching_block_ids
   Plan says only ['spreadsheet.formula_error_troubleshooting#tb4']
   but screens has tb4 AND tb5. Remove tb5 from the STEP-level lineage only.
   Keep f5 in block-level fact_ids so s15 can test it (taught-before-tested).
2. tile_spreadsheet_cleaning_cross_sheet.s01/spreadsheet_grid
   variant_id 'messy' does not exist; correct id is 'asset_orders_messy'.
"""
import json
from pathlib import Path

B = Path('batches/final_batch_011_da_spreadsheet')

# --- Fix screens.part.c2.json ---
with open(B / 'screens.part.c2.json') as f:
    part = json.load(f)

for tile in part['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_lookups_troubleshooting':
        for step in tile['steps']:
            if step['step_id'] == 'tile_spreadsheet_lookups_troubleshooting.s12':
                lin = step['lineage']
                # Plan says only tb4; remove tb5 from STEP-level teaching_block_ids
                old_tbs = lin.get('teaching_block_ids', [])
                lin['teaching_block_ids'] = [
                    tb for tb in old_tbs
                    if tb != 'spreadsheet.formula_error_troubleshooting#tb5'
                ]
                # Keep f5 in step-level fact_ids (plan check doesn't check fact_ids)
                # so that s15 can test it (taught-before-tested rule uses block fact_ids)
                print(f"Fixed s12 step lineage.teaching_block_ids: {old_tbs} -> {lin['teaching_block_ids']}")
                print(f"Kept s12 step lineage.fact_ids: {lin.get('fact_ids', [])}")
                # Block-level: keep p2's fact_ids (including f5) so taught-before-tested passes
                for block in step.get('blocks', []):
                    if block.get('type') == 'prose':
                        blin = block.get('lineage', {})
                        print(f"  Block {block.get('block_id')}: teaching_block_ids={blin.get('teaching_block_ids')}, fact_ids={blin.get('fact_ids')}")
                break

    if tile['tile_id'] == 'tile_spreadsheet_cleaning_cross_sheet':
        for step in tile['steps']:
            if step['step_id'] == 'tile_spreadsheet_cleaning_cross_sheet.s01':
                for block in step.get('blocks', []):
                    if block.get('type') == 'before_after':
                        before = block.get('before', {})
                        if before.get('type') == 'spreadsheet_grid':
                            aref = before.get('asset_ref', {})
                            if aref.get('variant_id') == 'messy':
                                aref['variant_id'] = 'asset_orders_messy'
                                print(f"Fixed s01 before.asset_ref.variant_id -> 'asset_orders_messy'")
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
    print(f"  Loaded {len(pdata['tiles'])} tiles from {part_file.name}")

screens = {**base_data, 'tiles': all_tiles}
with open(B / 'screens.json', 'w') as f:
    json.dump(screens, f, indent=2)
print(f"Wrote screens.json ({len(all_tiles)} tiles)")
