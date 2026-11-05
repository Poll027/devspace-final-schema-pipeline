#!/usr/bin/env python3
"""
Simulate running the s15 solution to verify it works with tick_labels.
This mimics what the gate would do.
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
                
                print("=" * 60)
                print("Testing s15 interaction")
                print("=" * 60)
                
                # Get solution
                solution_content = interaction['grading']['solution_files'][0]['content']
                
                # Check solution syntax
                print("\n1. Checking solution contains tick_labels parameter...")
                if 'tick_labels=[city_1, city_2, city_3]' in solution_content:
                    print("   ✓ Solution uses tick_labels=[city_1, city_2, city_3]")
                else:
                    print("   ✗ FAIL: Solution missing tick_labels parameter")
                    sys.exit(1)
                
                # Check prompt instructs learner correctly
                print("\n2. Checking prompt instructs tick_labels...")
                prompt = interaction['public']['prompt']
                if "tick_labels=['Lagos', 'Abuja', 'Kano']" in prompt:
                    print("   ✓ Prompt instructs: tick_labels=['Lagos', 'Abuja', 'Kano']")
                else:
                    print("   ✗ FAIL: Prompt doesn't instruct tick_labels")
                    sys.exit(1)
                
                # Check tests
                print("\n3. Checking tests...")
                tests = interaction['grading']['tests']
                
                # Should have figure_equals test
                has_figure_test = any(t['kind'] == 'figure_equals' for t in tests)
                if has_figure_test:
                    print("   ✓ Has figure_equals test")
                else:
                    print("   ✗ FAIL: Missing figure_equals test")
                    sys.exit(1)
                
                # Should have xticklabels test
                xticklabels_test = None
                for test in tests:
                    if test.get('kind') == 'axes_property' and test.get('spec', {}).get('property') == 'xticklabels':
                        xticklabels_test = test
                        break
                
                if xticklabels_test:
                    expected = xticklabels_test['spec']['expected']
                    if expected == ["Lagos", "Abuja", "Kano"]:
                        print(f"   ✓ Has xticklabels test with correct expected: {expected}")
                    else:
                        print(f"   ✗ FAIL: xticklabels test has wrong expected: {expected}")
                        sys.exit(1)
                    
                    # Check message
                    msg = xticklabels_test.get('message_on_fail', '')
                    if 'tick_labels=[city_1, city_2, city_3]' in msg:
                        print(f"   ✓ Test message instructs correct usage")
                    else:
                        print(f"   ✗ FAIL: Test message doesn't instruct tick_labels usage")
                        sys.exit(1)
                else:
                    print("   ✗ FAIL: Missing xticklabels test")
                    sys.exit(1)
                
                # Should have plotted_data test for medians
                has_medians_test = any(
                    t.get('kind') == 'plotted_data_equals' and 
                    t.get('spec', {}).get('field') == 'medians' 
                    for t in tests
                )
                if has_medians_test:
                    print("   ✓ Has plotted_data_equals test for medians")
                else:
                    print("   ✗ FAIL: Missing medians test")
                    sys.exit(1)
                
                # Check feedback mentions tick_labels
                print("\n4. Checking feedback...")
                feedback = interaction.get('feedback', {})
                correct_msg = feedback.get('correct', {}).get('message', '')
                incorrect_msg = feedback.get('incorrect', {}).get('message', '')
                
                if 'tick_labels' in correct_msg:
                    print("   ✓ Correct feedback mentions tick_labels")
                else:
                    print("   ⚠ Warning: Correct feedback doesn't mention tick_labels")
                
                if 'tick_labels' in incorrect_msg:
                    print("   ✓ Incorrect feedback mentions tick_labels")
                else:
                    print("   ⚠ Warning: Incorrect feedback doesn't mention tick_labels")
                
                # Check measures include the right anchor
                print("\n5. Checking measures...")
                measures = interaction.get('measures', [])
                has_labeled_ticks_anchor = any(
                    m.get('capability') == 'draw_grouped_box_plot_with_labeled_ticks_from_sequence_of_arrays'
                    for m in measures
                )
                if has_labeled_ticks_anchor:
                    print("   ✓ Measures include draw_grouped_box_plot_with_labeled_ticks_from_sequence_of_arrays")
                else:
                    print("   ✗ FAIL: Missing labeled ticks anchor in measures")
                    sys.exit(1)
                
                print("\n" + "=" * 60)
                print("✓ ALL CHECKS PASSED")
                print("=" * 60)
                print("\nThe s15 interaction now:")
                print("- Uses tick_labels in the solution")
                print("- Instructs tick_labels in the prompt")
                print("- Tests tick_labels with axes_property test")
                print("- Satisfies the assessment anchor requirement")
                sys.exit(0)

print("✗ Could not find s15 interaction")
sys.exit(1)
