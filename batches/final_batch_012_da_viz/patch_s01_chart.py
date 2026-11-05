"""
Patch: replace the before_after block in tile_viz_seaborn_stats_themes.s01
with the chart block from screens.json, then recompute content_hash.
"""
import json
import sys
sys.path.insert(0, '00_FINAL_PIPELINE_CORE/scripts')
from finlib import sha

# Load the assembled tile
tile_path = 'batches/final_batch_012_da_viz/tile_lessons/tile_viz_seaborn_stats_themes.json'
with open(tile_path) as f:
    tile = json.load(f)

# Load the chart block from screens.json
with open('batches/final_batch_012_da_viz/screens.json') as f:
    screens = json.load(f)

chart_block = None
for t in screens['tiles']:
    if t['tile_id'] == 'tile_viz_seaborn_stats_themes':
        for step in t['steps']:
            if step['step_id'] == 'tile_viz_seaborn_stats_themes.s01':
                for b in step.get('blocks', []):
                    if b['type'] == 'chart':
                        chart_block = b
        break

if chart_block is None:
    print("ERROR: chart block not found in screens.json s01")
    sys.exit(1)

# Find and replace the before_after block in s01
patched = False
for step in tile['steps']:
    if step['step_id'] == 'tile_viz_seaborn_stats_themes.s01':
        new_blocks = []
        for b in step.get('blocks', []):
            if b['type'] == 'before_after' and b['block_id'] == 'tile_viz_seaborn_stats_themes.s01.b03':
                new_blocks.append(chart_block)
                patched = True
                print(f"Replaced before_after block with chart block in s01")
            else:
                new_blocks.append(b)
        step['blocks'] = new_blocks
        break

if not patched:
    print("ERROR: before_after block not found in s01")
    sys.exit(1)

# Recompute content_hash
tile.pop('content_hash', None)
tile['content_hash'] = sha(tile)
print(f"New content_hash: {tile['content_hash'][:12]}")

# Verify block_types are still correct
def iter_blocks(blocks):
    for b in blocks or []:
        yield b
        if b['type'] == 'before_after':
            yield b['before']
            yield b['after']
        if b['type'] == 'side_by_side':
            yield b['left']
            yield b['right']

used_blocks = sorted({b['type'] for s in tile['steps'] + tile['remediation_steps'] for b in iter_blocks(s.get('blocks'))})
print(f"block_types in tile: {used_blocks}")
print(f"block_types in requires: {tile['requires']['block_types']}")

# Update block_types in requires if needed
if set(used_blocks) != set(tile['requires']['block_types']):
    tile['requires']['block_types'] = used_blocks
    # Recompute content_hash again
    tile.pop('content_hash', None)
    tile['content_hash'] = sha(tile)
    print(f"Updated block_types and recomputed hash: {tile['content_hash'][:12]}")

# Save
with open(tile_path, 'w') as f:
    json.dump(tile, f, indent=2, ensure_ascii=False)
    f.write('\n')

print("Done.")
