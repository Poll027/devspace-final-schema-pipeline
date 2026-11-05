#!/usr/bin/env python3
"""
Patch interaction s16 to add #REF! error fix, matching the visual in s11 and the plan.
"""
import json

# Read the interactions file
with open('interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Find the s16 interaction
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_lookups_troubleshooting':
        for item in tile['interactions']:
            if item['step_id'] == 'tile_spreadsheet_lookups_troubleshooting.s16':
                interaction = item['interaction']
                
                # Add the #REF! capability to measures
                interaction['measures'].insert(1, {
                    "concept_id": "spreadsheet.formula_error_troubleshooting",
                    "capability": "diagnose_ref_error_as_invalid_cell_reference",
                    "fact_ids": ["f2"]
                })
                
                # Add the #REF! anchor
                interaction['anchors'].insert(2, 
                    "spreadsheet.formula_error_troubleshooting#assessment:diagnose_ref_error_as_invalid_cell_reference"
                )
                
                # Update the prompt to include Fix 3 for #REF!
                old_prompt = interaction['public']['prompt']
                new_prompt = """This workbook has three broken formulas.

**Fix 1 — #N/A in B8:** The VLOOKUP in B8 returns #N/A because the driver ID in A8 ('D0X') does not exist in the drivers sheet. Change A8 to the correct driver ID **D01** so the VLOOKUP finds a match and returns the driver name.

**Fix 2 — #REF! in C8:** The formula in C8 returns #REF! because it references a cell that was deleted. Replace the formula in C8 with **=A8+B8** to sum the values in A8 and B8.

**Fix 3 — #VALUE! in D9:** The formula =A9+B9+C9 in D9 returns #VALUE! because B9 contains the text 'N/A'. Replace the formula in D9 with one that sums A9:C9 but ignores the text value in B9."""
                
                interaction['public']['prompt'] = new_prompt
                
                # Update the starter file to include the #REF! error
                old_content = interaction['public']['workspace']['files'][0]['content']
                new_content = """// This workbook has three broken formulas. Fix all three.
//
// Row 8: A8 holds a driver ID to look up. B8 uses VLOOKUP to find the driver name.
// The lookup is returning #N/A because the driver ID in A8 is misspelled.
// Fix A8 so the driver ID matches exactly what is in the drivers sheet (use D01).
// The drivers data is in rows 1-6 (A1:B6).
A8: D0X
B8: =VLOOKUP(A8,A1:B6,2,0)

// Row 8 continued: C8 has a #REF! error because it references a deleted cell.
// Replace the formula in C8 with =A8+B8 to sum A8 and B8.
C8: =#REF!+B8

// Row 9: D9 adds cells A9, B9, and C9. It returns #VALUE! because B9 contains text.
// Fix D9 by replacing the arithmetic addition with a function that ignores text values.
A9: 100
B9: N/A
C9: 200
D9: =A9+B9+C9
"""
                
                interaction['public']['workspace']['files'][0]['content'] = new_content
                
                # Update the solution to include the #REF! fix
                old_solution = interaction['grading']['solution_files'][0]['content']
                new_solution = """A8: D01
B8: =VLOOKUP(A8,A1:B6,2,0)
C8: =A8+B8
A9: 100
B9: N/A
C9: 200
D9: =SUM(A9:C9)
"""
                
                interaction['grading']['solution_files'][0]['content'] = new_solution
                
                # Add a test for the #REF! fix
                # The test should check that C8 returns a number (not #REF!)
                # Assuming A8 will be D01 (a text value) and B8 will be "Amara Okafor" (text),
                # C8 = A8+B8 would try to add two text values, which would return #VALUE!
                # This doesn't make sense. Let me reconsider.
                
                # Actually, looking at the starter, A8 is a driver ID (text) and B8 is a VLOOKUP result (text name).
                # So C8 = A8+B8 would try to add two text values, which is wrong.
                
                # Let me think about what makes sense for a #REF! error fix.
                # The visual in s11 shows =SUM(#REF!), which is a SUM formula that references a deleted range.
                # A more realistic scenario would be: C8 originally had =SUM(E8:F8), but columns E and F were deleted,
                # so now it shows =SUM(#REF!). The fix would be to replace it with a valid formula.
                
                # But we need to keep the fix simple and testable. Let me use numeric values.
                # Let's say row 8 has numeric data in columns other than A and B.
                
                # Actually, let me look at what data is available. The starter mounts asset_drivers_vlookup.
                # Let me check what that asset contains.
                
                print("Need to check asset_drivers_vlookup structure")
                break

# Don't write yet, need to understand the data structure first
print("Pausing to check asset structure")
