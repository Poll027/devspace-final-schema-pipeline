#!/usr/bin/env python3
"""Patch interactions.part.c2.json to fix validation errors."""

import json

# Read the current file
with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Fix 1: tile_capstone_integrate_tools_model.s05 - add blocked_syntax
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_capstone_integrate_tools_model':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_capstone_integrate_tools_model.s05':
                # Add the correct blocked_syntax from glossary
                ix['interaction']['public']['constraints']['blocked_syntax'] = [
                    "HAVING",
                    "LEFT JOIN",
                    "RIGHT JOIN",
                    "FULL OUTER JOIN",
                    "subquery",
                    "CTE (WITH ...)",
                    "UNION",
                    "FORMAT()",
                    "CASE",
                    "COALESCE",
                    "ORDER BY"
                ]
                print("Fixed s05: Added blocked_syntax")

# Fix 2: tile_capstone_stats_dashboard.s10 - remove .dropna() from solution and starter
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_capstone_stats_dashboard':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_capstone_stats_dashboard.s10':
                # Fix starter file - remove .dropna()
                for f in ix['interaction']['public']['workspace']['files']:
                    if f['path'] == 'dashboard.py':
                        # Replace the line with .dropna()
                        f['content'] = f['content'].replace(
                            "delivery_times = df['delivery_time'].dropna()",
                            "delivery_times = df['delivery_time']"
                        )
                        print("Fixed s10 starter: Removed .dropna()")
                
                # Fix solution file - remove .dropna()
                if 'grading' in ix['interaction']:
                    for sf in ix['interaction']['grading'].get('solution_files', []):
                        if sf['path'] == 'dashboard.py':
                            sf['content'] = sf['content'].replace(
                                "delivery_times = df['delivery_time'].dropna()",
                                "delivery_times = df['delivery_time']"
                            )
                            print("Fixed s10 solution: Removed .dropna()")

# Write the patched file
with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nPatching complete!")
