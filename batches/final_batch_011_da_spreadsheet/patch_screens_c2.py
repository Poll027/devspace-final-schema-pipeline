#!/usr/bin/env python3
"""Patch screens.part.c2.json to fix the two blocking findings for c2."""

import json

# Load the artifact
with open('batches/final_batch_011_da_spreadsheet/screens.part.c2.json', 'r') as f:
    data = json.load(f)

# Find the tile
tile = next(t for t in data['tiles'] if t['tile_id'] == 'tile_spreadsheet_lookups_troubleshooting')

# Fix 1: r02 - Change F4/D03 to F5/D03
r02 = next(s for s in tile['remediation_steps'] if s['step_id'] == 'tile_spreadsheet_lookups_troubleshooting.r02')
r02_prose = next(b for b in r02['blocks'] if b['block_id'] == 'tile_spreadsheet_lookups_troubleshooting.r02.p1')

# Original text mentions "driver ID D03 is in cell F4"
# Registry shows F4 has D01, F5 has D03
# Change F4 to F5
old_text = r02_prose['text']
new_text = old_text.replace(
    'driver ID D03 is in cell F4',
    'driver ID D03 is in cell F5'
).replace(
    'MATCH(F4,Drivers!B:B,0)',
    'MATCH(F5,Drivers!B:B,0)'
).replace(
    '=INDEX(Drivers!A:A,MATCH(F4,Drivers!B:B,0))',
    '=INDEX(Drivers!A:A,MATCH(F5,Drivers!B:B,0))'
)

r02_prose['text'] = new_text

print("Fixed r02:")
print(f"  Old: {old_text[:80]}...")
print(f"  New: {new_text[:80]}...")

# Fix 2: r03 - Change row 16 reference to hypothetical
r03 = next(s for s in tile['remediation_steps'] if s['step_id'] == 'tile_spreadsheet_lookups_troubleshooting.r03')
r03_prose = next(b for b in r03['blocks'] if b['block_id'] == 'tile_spreadsheet_lookups_troubleshooting.r03.p1')

# Original text says "amount in row 16 holds the text 'N/A'"
# Registry shows row 16 has amount 2600.0 (valid number)
# Change to hypothetical
old_text = r03_prose['text']
new_text = old_text.replace(
    'In the QuickDeliver Orders sheet, amount in row 16 holds the text "N/A" instead of a number.',
    'Suppose the QuickDeliver Orders sheet had an amount cell that held the text "N/A" instead of a number.'
).replace(
    'The formula =D2+D16 returns #VALUE! because the + operator cannot add text.',
    'A formula like =D2+D16 would return #VALUE! because the + operator cannot add text.'
).replace(
    'The formula =SUM(D2:D21) returns a total because SUM ignores text values and sums only the numeric ones.',
    'But a formula like =SUM(D2:D21) would return a total because SUM ignores text values and sums only the numeric ones.'
)

r03_prose['text'] = new_text

print("\nFixed r03:")
print(f"  Old: {old_text[:80]}...")
print(f"  New: {new_text[:80]}...")

# Save the patched file
with open('batches/final_batch_011_da_spreadsheet/screens.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nPatched file saved.")
