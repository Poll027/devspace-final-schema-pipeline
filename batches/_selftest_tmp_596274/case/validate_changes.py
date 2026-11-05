import json

with open('batches/final_batch_012_da_viz/interactions.part.c1.json', 'r') as f:
    data = json.load(f)

errors = []
warnings = []

for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_line_scatter_box':
        for interaction_entry in tile['interactions']:
            if interaction_entry['step_id'] == 'tile_viz_line_scatter_box.s15':
                interaction = interaction_entry['interaction']
                
                # Check prompt uses tick_labels
                prompt = interaction['public']['prompt']
                if 'tick_labels' not in prompt:
                    errors.append("s15: prompt should mention 'tick_labels' parameter")
                if 'labels' in prompt and 'tick_labels' not in prompt:
                    errors.append("s15: prompt should not use 'labels' parameter (should be tick_labels)")
                
                # Check solution uses tick_labels
                solution = interaction['grading']['solution_files'][0]['content']
                if 'tick_labels=' not in solution:
                    errors.append("s15: solution should use 'tick_labels=' parameter")
                if 'labels=' in solution and 'tick_labels=' not in solution:
                    errors.append("s15: solution should not use 'labels=' (should be tick_labels=)")
                
                print("✓ s15 validation:")
                print(f"  - Prompt mentions tick_labels: {'tick_labels' in prompt}")
                print(f"  - Solution uses tick_labels=: {'tick_labels=' in solution}")
                
            elif interaction_entry['step_id'] == 'tile_viz_line_scatter_box.s08':
                interaction = interaction_entry['interaction']
                
                # Check prompt asks for interpretation
                prompt = interaction['public']['prompt']
                has_interpretation = 'relationship' in prompt.lower() or 'positive' in prompt.lower() or 'negative' in prompt.lower()
                
                # Check solution includes interpretation
                solution = interaction['grading']['solution_files'][0]['content']
                has_solution_interpretation = 'relationship' in solution.lower() or 'positive' in solution.lower() or 'negative' in solution.lower()
                
                print("\n✓ s08 validation:")
                print(f"  - Prompt asks about relationship: {has_interpretation}")
                print(f"  - Solution includes interpretation: {has_solution_interpretation}")
                
                if not has_interpretation:
                    warnings.append("s08: prompt should ask learner to describe the relationship")
                if not has_solution_interpretation:
                    warnings.append("s08: solution should include relationship interpretation")

if errors:
    print("\n❌ ERRORS:")
    for e in errors:
        print(f"  - {e}")
else:
    print("\n✓ No errors found")

if warnings:
    print("\n⚠ WARNINGS:")
    for w in warnings:
        print(f"  - {w}")

print("\n" + "="*60)
print("Summary: Changes applied successfully" if not errors else "Summary: Errors found")
