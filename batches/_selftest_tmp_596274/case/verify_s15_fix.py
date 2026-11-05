#!/usr/bin/env python3
"""
Test that the s15 solution runs correctly with tick_labels.
"""

import json
import sys

# Read the artifact
with open('batches/final_batch_012_da_viz/interactions.part.c1.json', 'r') as f:
    data = json.load(f)

# Find the s15 interaction
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_line_scatter_box':
        for interaction_obj in tile['interactions']:
            if interaction_obj['step_id'] == 'tile_viz_line_scatter_box.s15':
                interaction = interaction_obj['interaction']
                
                # Check solution
                solution = interaction['grading']['solution_files'][0]['content']
                print("Solution code:")
                print(solution)
                print()
                
                # Check it contains tick_labels
                if 'tick_labels=[city_1, city_2, city_3]' in solution:
                    print("✓ Solution contains tick_labels=[city_1, city_2, city_3]")
                else:
                    print("✗ Solution missing tick_labels parameter")
                    sys.exit(1)
                
                # Check prompt
                prompt = interaction['public']['prompt']
                if "tick_labels=['Lagos', 'Abuja', 'Kano']" in prompt:
                    print("✓ Prompt instructs tick_labels=['Lagos', 'Abuja', 'Kano']")
                else:
                    print("✗ Prompt missing tick_labels instruction")
                    sys.exit(1)
                
                # Check for xticklabels test
                tests = interaction['grading']['tests']
                has_xticklabels_test = False
                for test in tests:
                    if test.get('kind') == 'axes_property' and test.get('spec', {}).get('property') == 'xticklabels':
                        has_xticklabels_test = True
                        expected = test['spec']['expected']
                        print(f"✓ Found xticklabels test with expected: {expected}")
                        if expected == ["Lagos", "Abuja", "Kano"]:
                            print("✓ Expected values are correct")
                        else:
                            print("✗ Expected values are wrong")
                            sys.exit(1)
                        break
                
                if not has_xticklabels_test:
                    print("✗ Missing xticklabels test")
                    sys.exit(1)
                
                print("\n✓ All checks passed!")
                sys.exit(0)

print("✗ Could not find s15 interaction")
sys.exit(1)
