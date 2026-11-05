#!/usr/bin/env python3
"""Update prose to match the visual fix."""
import json

with open('batches/final_batch_011_da_spreadsheet/screens.part.c2.json', 'r') as f:
    data = json.load(f)

# Find step s11 and update the prose
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_lookups_troubleshooting':
        for step in tile['steps']:
            if step['step_id'] == 'tile_spreadsheet_lookups_troubleshooting.s11':
                for block in step['blocks']:
                    if block['type'] == 'prose' and block['block_id'] == 'tile_spreadsheet_lookups_troubleshooting.s11.p4':
                        # Update the cell references from C2/C3 to D2/D3
                        block['text'] = block['text'].replace('cells C2 and C3', 'cells D2 and D3')
                        print(f"Updated prose block to reference D2 and D3 instead of C2 and C3")
                        break

with open('batches/final_batch_011_da_spreadsheet/screens.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Prose update complete")
