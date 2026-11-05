#!/usr/bin/env python3
"""Quick validation of the two specific fixes"""
import json
import ast

with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

errors = []
warnings = []

# Check 1: s09 should not have line_graph anchor if it doesn't measure it
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_labeling_chart_selection':
        for ie in tile['interactions']:
            if ie['step_id'] == 'tile_viz_labeling_chart_selection.s09':
                anchors = ie['interaction']['anchors']
                measures = [m['capability'] for m in ie['interaction']['measures']]
                
                has_line_graph_anchor = any('line_graph' in a for a in anchors)
                has_line_graph_measure = any('line_graph' in m for m in measures)
                
                if has_line_graph_anchor and not has_line_graph_measure:
                    errors.append("s09: has line_graph anchor but doesn't measure it")
                else:
                    print("✓ s09: line_graph anchor issue fixed")

# Check 2: s08 solution should not use tuple_lit
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_custom_multi_panel':
        for ie in tile['interactions']:
            if ie['step_id'] == 'tile_viz_custom_multi_panel.s08':
                solution = ie['interaction']['grading']['solution_files'][0]['content']
                
                # Parse and check for Tuple nodes
                try:
                    tree = ast.parse(solution)
                    
                    class TupleFinder(ast.NodeVisitor):
                        def __init__(self):
                            self.found_tuple = False
                        def visit_Tuple(self, node):
                            self.found_tuple = True
                            self.generic_visit(node)
                    
                    finder = TupleFinder()
                    finder.visit(tree)
                    
                    if finder.found_tuple:
                        errors.append("s08: solution still uses tuple_lit")
                    else:
                        print("✓ s08: tuple_lit issue fixed (solution uses double-bracket notation)")
                        
                except SyntaxError as e:
                    errors.append(f"s08: solution has syntax error: {e}")

# Check 3: Verify allowed_syntax was updated too
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_custom_multi_panel':
        for ie in tile['interactions']:
            if ie['step_id'] == 'tile_viz_custom_multi_panel.s08':
                allowed = ie['interaction']['public']['constraints']['allowed_syntax']
                
                # Check if it uses double-bracket notation
                has_double_bracket = any('axs[0][0]' in item or 'axs[row][col]' in item for item in allowed)
                has_tuple_notation = any('axs[0, 0]' in item or 'axs[row, col]' in item for item in allowed)
                
                if has_double_bracket and not has_tuple_notation:
                    print("✓ s08: allowed_syntax uses double-bracket notation")
                elif has_tuple_notation:
                    warnings.append("s08: allowed_syntax still uses tuple notation (may differ from glossary)")

print()
if errors:
    print("ERRORS:")
    for e in errors:
        print(f"  - {e}")
else:
    print("✓ No errors found")

if warnings:
    print("\nWARNINGS:")
    for w in warnings:
        print(f"  - {w}")

print(f"\nSummary: {len(errors)} errors, {len(warnings)} warnings")
