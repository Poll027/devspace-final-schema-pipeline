#!/usr/bin/env python3
"""
Apply ADVISORY fixes to interactions.part.c1.json
"""
import json

# Load the artifact
with open('batches/final_batch_011_da_spreadsheet/interactions.part.c1.json', 'r') as f:
    data = json.load(f)

# Find the tiles
tiles = {tile['tile_id']: tile for tile in data['tiles']}

print("=" * 60)
print("ADVISORY 1: tile_spreadsheet_formula_syntax_refs/s05")
print("=" * 60)
print("The 'question title' refers to the lede in screens.json (stage 03).")
print("Stage 04 (interactions) cannot edit stage 03 artifacts.")
print("The interaction prompt in this file already correctly uses D2:D21.")
print("This advisory requires editing screens.json, which is out of scope.")
print()

print("=" * 60)
print("ADVISORY 2: tile_spreadsheet_aggregation_logical/s01")
print("=" * 60)
print("Step s01 is an 'explainer' step with no interaction.")
print("The SIDE_BY_SIDE visual is in screens.json (stage 03).")
print("Stage 04 (interactions) cannot edit stage 03 artifacts.")
print("This advisory requires editing screens.json, which is out of scope.")
print()

# ADVISORY 3: tile_spreadsheet_text_date_conditional_agg/s09/opt_b
# Change feedback for option B
print("=" * 60)
print("ADVISORY 3: tile_spreadsheet_text_date_conditional_agg/s09/opt_b")
print("=" * 60)
tile3 = tiles['tile_spreadsheet_text_date_conditional_agg']
for item in tile3['interactions']:
    step_id = item['step_id']
    interaction = item['interaction']
    if step_id.endswith('.s09'):
        if 'opt_b' in interaction['grading']['option_feedback']:
            old_feedback = interaction['grading']['option_feedback']['opt_b']['message']
            print(f"Old feedback: {old_feedback}")
            # Change the feedback
            interaction['grading']['option_feedback']['opt_b']['message'] = "if G2 is in the past, this returns a #NUM! error because DATEDIF requires start_date ≤ end_date."
            print(f"New feedback: {interaction['grading']['option_feedback']['opt_b']['message']}")
        break
print()

# ADVISORY 4: tile_spreadsheet_text_date_conditional_agg/s10
# Remove explain_date_serial_number_model(f4) anchor
print("=" * 60)
print("ADVISORY 4: tile_spreadsheet_text_date_conditional_agg/s10")
print("=" * 60)
for item in tile3['interactions']:
    step_id = item['step_id']
    interaction = item['interaction']
    if step_id.endswith('.s10'):
        print(f"Current measures count: {len(interaction['measures'])}")
        # Find the measure with explain_date_serial_number_model(f4)
        measures_to_remove = []
        for i, measure in enumerate(interaction['measures']):
            if 'explain_date_serial_number_model' in measure['capability']:
                print(f"Found measure to remove at index {i}: {measure['capability']}")
                measures_to_remove.append(measure)
        
        for measure in measures_to_remove:
            interaction['measures'].remove(measure)
            print(f"Removed measure: {measure['capability']}")
        
        print(f"Updated measures count: {len(interaction['measures'])}")
        break
print()

# ADVISORY 5: tile_spreadsheet_text_date_conditional_agg/s07
print("=" * 60)
print("ADVISORY 5: tile_spreadsheet_text_date_conditional_agg/s07")
print("=" * 60)
print("Advisory suggests 'Consider adding a RIGHT task to s07 or a dedicated check step'")
print("Since this is advisory ('consider') and we can only reword/delete/move/cite")
print("(not add new claims), leaving s07 as is.")
print()

# Save the modified data
with open('batches/final_batch_011_da_spreadsheet/interactions.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2)

print("=" * 60)
print("✓ Repairs applied successfully")
print("=" * 60)
print()
print("SUMMARY:")
print("- ADVISORY 1: Cannot fix (requires editing screens.json)")
print("- ADVISORY 2: Cannot fix (requires editing screens.json)")
print("- ADVISORY 3: FIXED (updated opt_b feedback in s09)")
print("- ADVISORY 4: FIXED (removed explain_date_serial_number_model measure from s10)")
print("- ADVISORY 5: No action needed (advisory 'consider' suggestion)")
