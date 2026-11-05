#!/usr/bin/env python3
"""Fix constraints in BOTH locations - ix level and public level."""

import json

# Read the interactions file
with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Map glossary descriptions to validator UNIVERSE strings
for tile in data['tiles']:
    for interaction in tile['interactions']:
        step_id = interaction['step_id']
        ix = interaction['interaction']
        
        if step_id == 'tile_capstone_integrate_tools_model.s05':
            # SQL - replace glossary descriptions with UNIVERSE strings
            new_constraints = {
                'allowed_syntax': [
                    "SELECT",
                    "FROM",
                    "JOIN / INNER JOIN",
                    "ON",
                    "WHERE",
                    "AND",
                    "GROUP BY",
                    "AVG",
                    "table alias (FROM table AS alias)",
                    "< > <= >= = <> !=",
                    "alias.column qualification"
                ],
                'blocked_syntax': [
                    "HAVING",
                    "LEFT JOIN",
                    "RIGHT JOIN",
                    "FULL JOIN",
                    "subquery in WHERE",
                    "WITH name AS (...)",
                    "UNION",
                    "CASE WHEN ... THEN ... ELSE ... END",
                    "COALESCE",
                    "ORDER BY"
                ]
            }
            ix['constraints'] = new_constraints
            ix['public']['constraints'] = new_constraints
            print(f"Fixed constraints for {step_id} in both locations")
        
        elif step_id == 'tile_capstone_integrate_tools_model.s15':
            # Python - add attr_module to allowed
            if 'attr_module' not in ix['constraints']['allowed_syntax']:
                ix['constraints']['allowed_syntax'].append('attr_module')
            if 'attr_module' not in ix['public']['constraints']['allowed_syntax']:
                ix['public']['constraints']['allowed_syntax'].append('attr_module')
            print(f"Fixed constraints for {step_id} in both locations")
        
        elif step_id == 'tile_capstone_stats_dashboard.s10':
            # Chart - add the missing attr descriptors
            new_allowed = [
                'attr:dropna',
                'attr:index',
                'attr:title',
                'attr:values',
                'attr_module',
                'attr:keys',
                'attr:notna'
            ]
            # Add to existing allowed syntax
            ix['constraints']['allowed_syntax'] = list(set(ix['constraints']['allowed_syntax'] + new_allowed))
            ix['public']['constraints']['allowed_syntax'] = list(set(ix['public']['constraints']['allowed_syntax'] + new_allowed))
            print(f"Fixed constraints for {step_id} in both locations")

# Write the patched file
with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nConstraints fix complete!")
