#!/usr/bin/env python3
"""Patch the s05 interaction to fix allowed syntax errors."""
import json

with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Find and patch the s05 interaction
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_capstone_integrate_tools_model':
        for interaction in tile['interactions']:
            if interaction['step_id'] == 'tile_capstone_integrate_tools_model.s05':
                # The issue is that the solution uses constructs that are in allowed_syntax,
                # but the starter should contain almost all of them so the learner only adds GROUP BY
                
                # Update the starter to include everything except GROUP BY
                new_starter = """SELECT zone, AVG(delivery_time)
FROM orders o
INNER JOIN drivers d ON o.driver_id = d.driver_id
WHERE order_date >= '2026-04-01' AND order_date < '2026-07-01'
-- Add GROUP BY clause here
"""
                
                # Update the workspace file
                for file in interaction['interaction']['public']['workspace']['files']:
                    if file['path'] == 'query.sql':
                        file['content'] = new_starter
                
                # The solution stays the same - it's correct
                # The prompt is already good - it asks to add GROUP BY
                
                print("Patched s05 interaction")
                break

# Write back
with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done")
