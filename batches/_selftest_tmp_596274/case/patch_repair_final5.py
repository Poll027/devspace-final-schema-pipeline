#!/usr/bin/env python3
"""
Fix tile_viz_line_scatter_box.s15.t03 by splitting it into three separate tests,
one for each box, using the series parameter.
"""
import json

# Read the interactions file
with open('batches/final_batch_012_da_viz/interactions.part.c1.json', 'r') as f:
    data = json.load(f)

# Fix tile_viz_line_scatter_box.s15
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_line_scatter_box':
        for interaction_entry in tile['interactions']:
            if interaction_entry['step_id'] == 'tile_viz_line_scatter_box.s15':
                interaction = interaction_entry['interaction']
                
                # Find and remove the old t03 test
                tests = interaction['grading']['tests']
                new_tests = []
                for test in tests:
                    if test['test_id'] != 'ix.tile_viz_line_scatter_box.s15.t03':
                        new_tests.append(test)
                    else:
                        # Replace with three separate tests, one per box
                        # Test for Lagos (box 0)
                        new_tests.append({
                            "test_id": "ix.tile_viz_line_scatter_box.s15.t03a",
                            "kind": "plotted_data_equals",
                            "spec": {
                                "chart": "box",
                                "field": "n",
                                "expected": 8,
                                "series": 0,
                                "axes": 0
                            },
                            "visible": True,
                            "message_on_fail": "The first box (Lagos) should contain 8 data points. Make sure you filter the orders DataFrame correctly."
                        })
                        # Test for Abuja (box 1)
                        new_tests.append({
                            "test_id": "ix.tile_viz_line_scatter_box.s15.t03b",
                            "kind": "plotted_data_equals",
                            "spec": {
                                "chart": "box",
                                "field": "n",
                                "expected": 8,
                                "series": 1,
                                "axes": 0
                            },
                            "visible": True,
                            "message_on_fail": "The second box (Abuja) should contain 8 data points. Make sure you filter the orders DataFrame correctly."
                        })
                        # Test for Kano (box 2)
                        new_tests.append({
                            "test_id": "ix.tile_viz_line_scatter_box.s15.t03c",
                            "kind": "plotted_data_equals",
                            "spec": {
                                "chart": "box",
                                "field": "n",
                                "expected": 8,
                                "series": 2,
                                "axes": 0
                            },
                            "visible": True,
                            "message_on_fail": "The third box (Kano) should contain 8 data points. Make sure you filter the orders DataFrame correctly."
                        })
                
                interaction['grading']['tests'] = new_tests
                print(f"Fixed tile_viz_line_scatter_box.s15.t03 by splitting into three tests")
                break
        break

# Write the fixed file
with open('batches/final_batch_012_da_viz/interactions.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Done! Fixed interactions.part.c1.json")
