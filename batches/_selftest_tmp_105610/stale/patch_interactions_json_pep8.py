#!/usr/bin/env python3
"""
Update interactions.json to reflect the patch to interactions.part.c3.json:
- tile_python_pep8_style/s03: Remove instruction #3 (4-space indentation) and renumber
"""
import json
from pathlib import Path

B = Path('batches/final_batch_008_da_python_core')

with open(B / 'interactions.json') as f:
    d = json.load(f)

changed = False
for tile in d.get('tiles', []):
    if tile['tile_id'] == 'tile_python_pep8_style':
        for step in tile['interactions']:
            if step['step_id'] == 'tile_python_pep8_style.s03':
                ix = step['interaction']
                prompt = ix['public']['prompt']
                
                old_instructions = (
                    "Apply these changes:\n"
                    "1. Rename `CalcFee` → `calc_fee` (lowercase with underscores)\n"
                    "2. Rename `Fee` → `fee` (lowercase)\n"
                    "3. Use **4-space** indentation (not 2 spaces)\n"
                    "4. Remove extraneous spaces inside `()` and before `,`"
                )
                new_instructions = (
                    "Apply these changes:\n"
                    "1. Rename `CalcFee` → `calc_fee` (lowercase with underscores)\n"
                    "2. Rename `Fee` → `fee` (lowercase)\n"
                    "3. Remove extraneous spaces inside `()` and before `,`"
                )
                
                if old_instructions in prompt:
                    new_prompt = prompt.replace(old_instructions, new_instructions)
                    ix['public']['prompt'] = new_prompt
                    changed = True
                    print("Fixed interactions.json tile_python_pep8_style.s03 prompt.")
                else:
                    print("WARNING: Expected instructions not found. Current prompt:")
                    idx = prompt.find('Apply these changes:')
                    print(prompt[idx:idx+300] if idx >= 0 else prompt[:300])

if not changed:
    print("ERROR: No changes made!")
else:
    with open(B / 'interactions.json', 'w') as f:
        json.dump(d, f, indent=2)
    print("Saved interactions.json")

# Verify
with open(B / 'interactions.json') as f:
    d2 = json.load(f)
for tile in d2.get('tiles', []):
    if tile['tile_id'] == 'tile_python_pep8_style':
        for step in tile['interactions']:
            if step['step_id'] == 'tile_python_pep8_style.s03':
                prompt = step['interaction']['public']['prompt']
                idx = prompt.find('Apply these changes:')
                print("\nVerification - interactions.json prompt instructions:")
                print(prompt[idx:])
