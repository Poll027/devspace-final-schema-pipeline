#!/usr/bin/env python3
"""Fix solutions to use only allowed syntax."""

import json

# Read the interactions file
with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Fix each problematic solution
for tile in data['tiles']:
    for interaction in tile['interactions']:
        step_id = interaction['step_id']
        ix = interaction['interaction']
        
        if step_id == 'tile_capstone_integrate_tools_model.s05':
            # SQL solution - remove AS alias, simplify to use only allowed syntax
            # The allowed syntax doesn't explicitly include AS for column aliases
            # Rewrite to avoid JOIN and use only SELECT, FROM, WHERE, GROUP BY
            # Actually, looking at the allowed syntax, it says "INNER JOIN ... ON" is allowed
            # But the solution uses table aliases with AS which may not be in the allowed list
            # Let me check if we can avoid the JOIN entirely
            
            # Actually, the practice anchor says we MUST use INNER JOIN
            # The issue is that the solution uses syntax not explicitly in the allowed list
            # Let me rewrite to be simpler - maybe the validator is too strict
            
            # Looking at the error: it says the solution uses things like "< > <= >= = <> !="
            # But the allowed syntax says "date literal comparison (>=, <)"
            # The problem is the validator doesn't recognize the descriptive string
            
            # The solution needs to be rewritten to avoid the JOIN since the allowed syntax
            # descriptors don't match what the validator expects
            
            # But wait - the practice anchor REQUIRES a JOIN. So we can't avoid it.
            # The issue is that the allowed_syntax list from the glossary uses human-readable
            # descriptions, but the validator needs specific syntax descriptor strings.
            
            # Let me check what the solution actually needs:
            for sf in ix['grading']['solution_files']:
                if sf['path'] == 'query.sql':
                    print(f"\n{step_id} current solution:")
                    print(sf['content'])
                    
                    # The simplest fix: rewrite to avoid AS for column alias
                    # and use simpler table references
                    new_solution = """SELECT zone, AVG(delivery_time)
FROM orders
INNER JOIN drivers ON orders.driver_id = drivers.driver_id
WHERE order_date >= '2026-04-01' AND order_date < '2026-07-01'
GROUP BY zone"""
                    
                    sf['content'] = new_solution
                    print(f"\nNew solution:")
                    print(new_solution)
                    
                    # Also need to update the expected results
                    for test in ix['grading']['tests']:
                        if test['kind'] == 'query_result_equals':
                            # The columns will now be 'zone' and 'AVG(delivery_time)' instead of 'avg_delivery_time'
                            if 'expected' in test['spec']:
                                old_cols = test['spec']['expected']['columns']
                                print(f"\nOld columns: {old_cols}")
                                # Update column name
                                test['spec']['expected']['columns'] = ['zone', 'AVG(delivery_time)']
                                print(f"New columns: {test['spec']['expected']['columns']}")
        
        elif step_id == 'tile_capstone_integrate_tools_model.s15':
            # Python solution - uses .isna(), .dropna(), .groupby().mean()
            # These should all be in the allowed syntax
            # The error says it uses 'attr_module' which suggests it's using module attributes
            # Let me check the solution
            for sf in ix['grading']['solution_files']:
                if sf['path'] == 'solution.py':
                    print(f"\n{step_id} current solution:")
                    print(sf['content'])
                    
                    # The issue is likely the print statements or the way we're calling methods
                    # Let me simplify to avoid any issues
                    new_solution = """import pandas as pd

df = pd.read_csv('orders.csv')

clean = df.dropna()

result = clean.groupby('zone')['delivery_time'].mean()
print(result)
"""
                    
                    sf['content'] = new_solution
                    print(f"\nNew solution:")
                    print(new_solution)
        
        elif step_id == 'tile_capstone_stats_dashboard.s10':
            # Chart solution - uses .dropna(), .index, .values, .title
            # The error says these are not in allowed syntax
            # But looking at the allowed syntax, it has df.groupby(...).mean() and df['column'].value_counts()
            # The issue is using .index and .values on the result
            # Let me rewrite to avoid these
            for sf in ix['grading']['solution_files']:
                if sf['path'] == 'dashboard.py':
                    print(f"\n{step_id} current solution:")
                    print(sf['content'])
                    
                    # Rewrite to avoid .index and .values
                    new_solution = """import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('orders.csv')

zone_counts = df['zone'].value_counts()
plt.subplot(131)
plt.bar(range(len(zone_counts)), zone_counts.tolist())
plt.title('Orders per Zone')

delivery_times = df['delivery_time']
clean_times = []
for val in delivery_times:
    if pd.notna(val):
        clean_times.append(val)

plt.subplot(132)
plt.hist(clean_times)
plt.title('Delivery Time Distribution')

zone_means = df.groupby('zone')['delivery_time'].mean()
plt.subplot(133)
plt.bar(range(len(zone_means)), zone_means.tolist())
plt.title('Mean Delivery Time per Zone')

plt.suptitle('QuickRide Capstone Dashboard')
plt.tight_layout()
"""
                    
                    sf['content'] = new_solution
                    print(f"\nNew solution:")
                    print(new_solution)

# Write the patched file
with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\n\nSolution patching complete!")
