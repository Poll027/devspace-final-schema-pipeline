#!/usr/bin/env python3
"""
Patch interactions.part.c3.json for pedagogy repair:
- tile_python_pep8_style/s03: Remove instruction #3 (4-space indentation) and renumber
  remaining instructions (old #4 becomes new #3).
  
Note: tile_python_operators_conversion/s10 opt_b feedback is already correct in c1.json.
"""
import json
from pathlib import Path

B = Path('batches/final_batch_008_da_python_core')

with open(B / 'interactions.part.c3.json') as f:
    d = json.load(f)

changed = False
for tile in d['tiles']:
    if tile['tile_id'] == 'tile_python_pep8_style':
        for step in tile['interactions']:
            if step['step_id'] == 'tile_python_pep8_style.s03':
                ix = step['interaction']
                prompt = ix['public']['prompt']
                
                # Current prompt has:
                # 1. Rename `CalcFee` → `calc_fee` (lowercase with underscores)
                # 2. Rename `Fee` → `fee` (lowercase)
                # 3. Use **4-space** indentation (not 2 spaces)
                # 4. Remove extraneous spaces inside `()` and before `,`
                #
                # Finding: Remove instruction #3 entirely and renumber remaining instructions.
                # After fix:
                # 1. Rename `CalcFee` → `calc_fee` (lowercase with underscores)
                # 2. Rename `Fee` → `fee` (lowercase)
                # 3. Remove extraneous spaces inside `()` and before `,`
                
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
                    print("Fixed tile_python_pep8_style.s03 prompt: removed instruction #3 and renumbered.")
                else:
                    print("WARNING: Expected instructions not found in prompt. Current prompt:")
                    print(repr(prompt))

if not changed:
    print("ERROR: No changes made!")
else:
    with open(B / 'interactions.part.c3.json', 'w') as f:
        json.dump(d, f, indent=2)
    print("Saved interactions.part.c3.json")

# Verify
with open(B / 'interactions.part.c3.json') as f:
    d2 = json.load(f)
for tile in d2['tiles']:
    if tile['tile_id'] == 'tile_python_pep8_style':
        for step in tile['interactions']:
            if step['step_id'] == 'tile_python_pep8_style.s03':
                print("\nVerification - new prompt:")
                print(step['interaction']['public']['prompt'])
