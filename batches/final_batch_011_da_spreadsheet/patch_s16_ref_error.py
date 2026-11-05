#!/usr/bin/env python3
"""
Patch interaction s16 to add #REF! error fix, matching the visual in s11 and the plan.
The plan says s16 should measure diagnose_ref_error_as_invalid_cell_reference (fact f2).
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
                
                # Add the #REF! capability to measures (insert after #N/A, before #VALUE!)
                interaction['measures'].insert(1, {
                    "concept_id": "spreadsheet.formula_error_troubleshooting",
                    "capability": "diagnose_ref_error_as_invalid_cell_reference",
                    "fact_ids": ["f2"]
                })
                
                # Add the #REF! anchor (insert after #N/A anchor, before #VALUE! anchor)
                interaction['anchors'].insert(2, 
                    "spreadsheet.formula_error_troubleshooting#assessment:diagnose_ref_error_as_invalid_cell_reference"
                )
                
                # Update the prompt to include Fix 2 for #REF! (renumber existing Fix 2 to Fix 3)
                interaction['public']['prompt'] = """This workbook has three broken formulas.

**Fix 1 — #N/A in B8:** The VLOOKUP in B8 returns #N/A because the driver ID in A8 ('D0X') does not exist in the drivers sheet. Change A8 to the correct driver ID **D01** so the VLOOKUP finds a match and returns the driver name.

**Fix 2 — #REF! in C8:** The formula in C8 returns #REF! because it references a cell that is not valid. The formula should sum the values in E1 and F1 (which contain 100 and 200). Replace the #REF! formula in C8 with **=E1+F1**.

**Fix 3 — #VALUE! in D9:** The formula =A9+B9+C9 in D9 returns #VALUE! because B9 contains the text 'N/A'. Replace the formula in D9 with one that sums A9:C9 but ignores the text value in B9."""
                
                # Update the starter file to include the #REF! error and the data cells E1, F1
                interaction['public']['workspace']['files'][0]['content'] = """// This workbook has three broken formulas. Fix all three.
//
// Row 8: A8 holds a driver ID to look up. B8 uses VLOOKUP to find the driver name.
// The lookup is returning #N/A because the driver ID in A8 is misspelled.
// Fix A8 so the driver ID matches exactly what is in the drivers sheet (use D01).
// The drivers data is in rows 1-6 (A1:B6).
A8: D0X
B8: =VLOOKUP(A8,A1:B6,2,0)

// C8 has a #REF! error. It should sum E1 and F1.
// Replace the formula in C8 with =E1+F1.
C8: =#REF!
E1: 100
F1: 200

// Row 9: D9 adds cells A9, B9, and C9. It returns #VALUE! because B9 contains text.
// Fix D9 by replacing the arithmetic addition with a function that ignores text values.
A9: 100
B9: N/A
C9: 200
D9: =A9+B9+C9
"""
                
                # Update the solution to include the #REF! fix
                interaction['grading']['solution_files'][0]['content'] = """A8: D01
B8: =VLOOKUP(A8,A1:B6,2,0)
C8: =E1+F1
E1: 100
F1: 200
A9: 100
B9: N/A
C9: 200
D9: =SUM(A9:C9)
"""
                
                # Add a test for the #REF! fix (insert after VLOOKUP test, before SUM tests)
                ref_test = {
                    "test_id": "test_ref_fixed",
                    "kind": "cell_equals",
                    "spec": {
                        "cell": "C8",
                        "expected": 300.0
                    },
                    "visible": True,
                    "message_on_fail": "C8 should return 300 (100 + 200). Replace the #REF! formula with =E1+F1."
                }
                interaction['grading']['tests'].insert(1, ref_test)
                
                # Update feedback messages to mention all three fixes
                interaction['feedback']['correct']['message'] = "Well done! You fixed all three errors: correcting the misspelled driver ID resolved the #N/A (the lookup value now exists in the source data), replacing the #REF! formula resolved the invalid cell reference, and switching to SUM resolved the #VALUE! (SUM ignores text values, the + operator does not)."
                
                interaction['feedback']['incorrect']['message'] = "Check all three fixes. For B8: the VLOOKUP returns #N/A because A8 contains 'D0X' which doesn't exist in the drivers sheet — change A8 to 'D01'. For C8: replace the #REF! formula with =E1+F1 to sum the values in E1 and F1. For D9: replace the + formula with =SUM(A9:C9) to ignore the text in B9."
                
                interaction['feedback']['hints'][0] = "For the #N/A error: compare the value in A8 character by character with the driver IDs in the drivers sheet."
                interaction['feedback']['hints'].insert(1, "For the #REF! error: the formula should add E1 (100) and F1 (200) to get 300.")
                # Keep the existing hint about #VALUE! as the third hint
                
                print("Patched s16 to include #REF! error fix")
                print(f"  - Added measure: diagnose_ref_error_as_invalid_cell_reference")
                print(f"  - Added anchor: ...#assessment:diagnose_ref_error_as_invalid_cell_reference")
                print(f"  - Updated prompt to include Fix 2 for #REF!")
                print(f"  - Added test: test_ref_fixed (C8 should equal 300)")
                print(f"  - Updated feedback messages")

# Write the patched file
with open('interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nWrote patched interactions.part.c2.json")
