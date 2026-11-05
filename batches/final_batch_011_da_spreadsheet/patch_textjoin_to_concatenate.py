#!/usr/bin/env python3
"""
Fix TEXTJOIN formulas that produce #NAME? errors in HyperFormula.

The formula engine (HyperFormula 3.4.0) doesn't support TEXTJOIN, but it does
support CONCATENATE. Change the formulas in the visual from TEXTJOIN to CONCATENATE.

The teaching text and glossary still mention TEXTJOIN (which is correct for Excel),
but the visual demonstration uses CONCATENATE (which works in the engine).
"""

import json

# Load the screens part file
with open('batches/final_batch_011_da_spreadsheet/screens.part.c1.json', 'r') as f:
    data = json.load(f)

# Find and fix tile_spreadsheet_text_date_conditional_agg.s01
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_text_date_conditional_agg':
        for step in tile['steps']:
            if step['step_id'] == 'tile_spreadsheet_text_date_conditional_agg.s01':
                for block in step['blocks']:
                    if block.get('type') == 'before_after':
                        # Change TEXTJOIN formulas to CONCATENATE
                        after = block['after']
                        for cell in after.get('cells', []):
                            if 'formula' in cell and 'TEXTJOIN' in cell['formula']:
                                old_formula = cell['formula']
                                # =TEXTJOIN(", ",TRUE,B2,E2) -> =CONCATENATE(B2,", ",E2)
                                # Extract the cell references from TEXTJOIN
                                if cell['ref'] == 'G2':
                                    cell['formula'] = '=CONCATENATE(B2,", ",E2)'
                                elif cell['ref'] == 'G3':
                                    cell['formula'] = '=CONCATENATE(B3,", ",E3)'
                                print(f"Changed {cell['ref']}: {old_formula} -> {cell['formula']}")
                        
                        # Update annotations to reflect CONCATENATE
                        for ann in after.get('annotations', []):
                            if ann.get('target') == 'G2' and 'TEXTJOIN' in ann.get('text', ''):
                                old_text = ann['text']
                                ann['text'] = '=CONCATENATE(B2,", ",E2)'
                                print(f"Updated annotation: {old_text} -> {ann['text']}")
                            if ann.get('target') == 'G1' and 'TEXTJOIN' in ann.get('text', ''):
                                old_text = ann['text']
                                ann['text'] = 'city_status — combined with CONCATENATE'
                                print(f"Updated annotation: {old_text} -> {ann['text']}")

# Write back
with open('batches/final_batch_011_da_spreadsheet/screens.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nPatch complete.")
