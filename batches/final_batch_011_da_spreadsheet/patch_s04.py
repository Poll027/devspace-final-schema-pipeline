import json

with open('batches/final_batch_011_da_spreadsheet/screens.part.c3.json') as f:
    data = json.load(f)

patched = False
for tile in data.get('tiles', []):
    if tile.get('tile_id') == 'tile_spreadsheet_formatting_validation':
        for step in tile.get('steps', []):
            if step.get('step_id') == 'tile_spreadsheet_formatting_validation.s04':
                # Fix type: check -> hands_on
                assert step['type'] == 'check', f"Expected check, got {step['type']}"
                step['type'] = 'hands_on'
                # Fix eyebrow
                step['eyebrow'] = 'Practice'
                # Fix title and lede to match hands_on framing
                step['title'] = 'Apply a Conditional Formatting Rule'
                step['lede'] = 'Apply a Highlight Cells Rules rule to the delivery_minutes column to flag values above a threshold.'
                # Fix reward gems: 5 -> 10
                step['reward']['gems'] = 10
                # Add #practice anchor if missing
                anchors = step.get('lineage', {}).get('anchors', [])
                practice_anchor = 'spreadsheet.conditional_formatting#practice'
                if practice_anchor not in anchors:
                    anchors.insert(0, practice_anchor)
                    step['lineage']['anchors'] = anchors
                patched = True
                print("Patched s04:", step['type'], step['eyebrow'], step['title'])
                print("Anchors:", step['lineage']['anchors'])
                print("Reward:", step['reward'])

assert patched, "Step not found!"

with open('batches/final_batch_011_da_spreadsheet/screens.part.c3.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Done.")
