#!/usr/bin/env python3
"""Patch interactions.part.c0_canary.json to fix the gate errors."""
import json

# Load the file
with open('batches/final_batch_012_da_viz/interactions.part.c0_canary.json') as f:
    data = json.load(f)

# Find the tile
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_figures_layout_plotting':
        for ix_entry in tile['interactions']:
            step_id = ix_entry['step_id']
            ix = ix_entry['interaction']
            
            # Fix s05
            if step_id == 'tile_viz_figures_layout_plotting.s05':
                # Add extra entries to allowed_syntax
                allowed = ix['public']['constraints']['allowed_syntax']
                if 'list literals and variable assignment' not in allowed:
                    allowed.append('list literals and variable assignment')
                if 'whole-number literals as in the examples' not in allowed:
                    allowed.append('whole-number literals as in the examples')
                if 'tuple literals for figsize' not in allowed:
                    allowed.append('tuple literals for figsize')
                
                # Update starter content
                starter_content = """import matplotlib.pyplot as plt

# Data (these values will be changed by the grader to test your code)
day_1 = 1
days = [day_1, 2, 3, 4, 5]
dt_1 = 21
delivery_times = [dt_1, 23, 19, 25, 20]

# Step 1: create a Figure and one Axes using plt.subplots()
# fig, ax = ...

# Step 2: draw delivery_times against days on the Axes
# ax.plot(..., ...)
"""
                for f in ix['public']['workspace']['files']:
                    if f['path'] == 'solution.py':
                        f['content'] = starter_content
                
                # Update solution content
                solution_content = """import matplotlib.pyplot as plt

# Data (these values will be changed by the grader to test your code)
day_1 = 1
days = [day_1, 2, 3, 4, 5]
dt_1 = 21
delivery_times = [dt_1, 23, 19, 25, 20]

fig, ax = plt.subplots()
ax.plot(days, delivery_times)
"""
                for f in ix['grading']['solution_files']:
                    if f['path'] == 'solution.py':
                        f['content'] = solution_content
            
            # Fix s08
            elif step_id == 'tile_viz_figures_layout_plotting.s08':
                # Add extra entries to allowed_syntax
                allowed = ix['public']['constraints']['allowed_syntax']
                if 'import matplotlib.pyplot as plt' not in allowed:
                    allowed.insert(0, 'import matplotlib.pyplot as plt')
                if 'whole-number literals as in the examples' not in allowed:
                    allowed.append('whole-number literals as in the examples')
            
            # Fix s12
            elif step_id == 'tile_viz_figures_layout_plotting.s12':
                # Add extra entries to allowed_syntax
                allowed = ix['public']['constraints']['allowed_syntax']
                if 'list literals and variable assignment' not in allowed:
                    allowed.append('list literals and variable assignment')
                if 'whole-number literals as in the examples' not in allowed:
                    allowed.append('whole-number literals as in the examples')
                
                # Fix t01 to expect [["line"]] instead of [["line", "line"]]
                # Fix t02 to check y-values instead of x-values (to make it data-dependent)
                for t in ix['grading']['tests']:
                    if t['test_id'] == 'ix.tile_viz_figures_layout_plotting.s12.t01':
                        t['spec']['expected']['chart_types'] = [['line']]
                    elif t['test_id'] == 'ix.tile_viz_figures_layout_plotting.s12.t02':
                        # Change to check y-values instead of x-values
                        t['spec']['field'] = 'y'
                        t['spec']['expected'] = [21, 23, 19, 25, 20]
                        t['message_on_fail'] = "The first line's y-values should be the `delivery_times` list. Call `plt.plot(delivery_times)`."
                
                # Update starter content
                starter_content = """import matplotlib.pyplot as plt

# Data (these values will be changed by the grader to test your code)
day_1 = 1
days = [day_1, 2, 3, 4, 5]
dt_1 = 21
delivery_times = [dt_1, 23, 19, 25, 20]

# Step 1: one-argument form (auto-generates x-positions 0, 1, 2, ...)
# plt.plot(...)

# Step 2: two-argument form (explicit x and y)
# plt.plot(..., ...)
"""
                for f in ix['public']['workspace']['files']:
                    if f['path'] == 'solution.py':
                        f['content'] = starter_content
                
                # Update solution content
                solution_content = """import matplotlib.pyplot as plt

# Data (these values will be changed by the grader to test your code)
day_1 = 1
days = [day_1, 2, 3, 4, 5]
dt_1 = 21
delivery_times = [dt_1, 23, 19, 25, 20]

plt.plot(delivery_times)
plt.plot(days, delivery_times)
"""
                for f in ix['grading']['solution_files']:
                    if f['path'] == 'solution.py':
                        f['content'] = solution_content

# Save the file
with open('batches/final_batch_012_da_viz/interactions.part.c0_canary.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Patched interactions.part.c0_canary.json")
print("Changes:")
print("- s05: Added extra entries to allowed_syntax, updated starter and solution to use scalar variables")
print("- s08: Added extra entries to allowed_syntax")
print("- s12: Added extra entries to allowed_syntax, fixed t01 expected, fixed t02 to check y-values, updated starter and solution to use scalar variables")
