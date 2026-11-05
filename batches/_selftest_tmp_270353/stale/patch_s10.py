import json

with open('batches/final_batch_011_da_spreadsheet/interactions.part.c2.json') as f:
    data = json.load(f)

# Find tile_spreadsheet_cleaning_cross_sheet, step s10
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_cleaning_cross_sheet':
        for entry in tile['interactions']:
            if entry['step_id'] == 'tile_spreadsheet_cleaning_cross_sheet.s10':
                ix = entry['interaction']
                # Check current measures
                print("Current measures:", json.dumps(ix['measures'], indent=2))
                print("Current anchors:", ix['anchors'])
                
                # Add the missing measure
                ix['measures'].append({
                    "concept_id": "spreadsheet.cross_sheet_references",
                    "capability": "write_cross_workbook_link_with_square_bracket_syntax",
                    "fact_ids": ["f3"]
                })
                
                # Add the missing anchor
                ix['anchors'].append(
                    "spreadsheet.cross_sheet_references#assessment:write_cross_workbook_link_with_square_bracket_syntax"
                )
                
                print("Updated measures:", json.dumps(ix['measures'], indent=2))
                print("Updated anchors:", ix['anchors'])

with open('batches/final_batch_011_da_spreadsheet/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')

print("Done.")
