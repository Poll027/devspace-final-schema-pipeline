import json, re

def fix_s15(ix):
    """Fix all labels= -> tick_labels= in s15 interaction, and fix allowed_syntax."""
    
    # Fix allowed_syntax: replace 'labels=[...]' with 'tick_labels=[...]'
    constraints = ix['public']['constraints']
    constraints['allowed_syntax'] = [
        'tick_labels=[...]' if s == 'labels=[...]' else s
        for s in constraints['allowed_syntax']
    ]
    
    def fix_text(s):
        s = s.replace(", labels=[city_1, city_2, city_3]", ", tick_labels=[city_1, city_2, city_3]")
        s = s.replace(", labels=['Lagos', 'Abuja', 'Kano']", ", tick_labels=['Lagos', 'Abuja', 'Kano']")
        s = s.replace("used `labels`", "used `tick_labels`")
        s = s.replace("use `labels`", "use `tick_labels`")
        s = s.replace("Use `labels=", "Use `tick_labels=")
        s = s.replace("`labels=[city_1, city_2, city_3]`", "`tick_labels=[city_1, city_2, city_3]`")
        s = s.replace("`labels=['Lagos', 'Abuja', 'Kano']`", "`tick_labels=['Lagos', 'Abuja', 'Kano']`")
        return s
    
    # Fix workspace starter file
    for wf in ix['public']['workspace']['files']:
        wf['content'] = fix_text(wf['content'])
    
    # Fix prompt
    ix['public']['prompt'] = fix_text(ix['public']['prompt'])
    
    # Fix solution files
    for sf in ix['grading']['solution_files']:
        sf['content'] = fix_text(sf['content'])
    
    # Fix tests message_on_fail
    for t in ix['grading']['tests']:
        if 'message_on_fail' in t:
            t['message_on_fail'] = fix_text(t['message_on_fail'])
    
    # Fix feedback
    if 'feedback' in ix:
        if 'correct' in ix['feedback']:
            ix['feedback']['correct']['message'] = fix_text(ix['feedback']['correct']['message'])
        if 'incorrect' in ix['feedback']:
            ix['feedback']['incorrect']['message'] = fix_text(ix['feedback']['incorrect']['message'])
        if 'hints' in ix['feedback']:
            ix['feedback']['hints'] = [fix_text(h) for h in ix['feedback']['hints']]
    
    return ix

# Patch interactions.json
print("Patching interactions.json...")
with open('batches/final_batch_012_da_viz/interactions.json') as f:
    data = json.load(f)

for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_line_scatter_box':
        for item in tile['interactions']:
            if item['step_id'] == 'tile_viz_line_scatter_box.s15':
                item['interaction'] = fix_s15(item['interaction'])
                print("  Patched s15 in interactions.json")

with open('batches/final_batch_012_da_viz/interactions.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("  interactions.json written.")

# Verify interactions.json
with open('batches/final_batch_012_da_viz/interactions.json') as f:
    d = json.load(f)
for tile in d['tiles']:
    if tile['tile_id'] == 'tile_viz_line_scatter_box':
        for item in tile['interactions']:
            if item['step_id'] == 'tile_viz_line_scatter_box.s15':
                ix = item['interaction']
                bare = re.findall(r'(?<!tick_)labels=', json.dumps(ix))
                print(f"  Bare labels= remaining in interactions.json s15: {bare}")
                print(f"  allowed_syntax: {ix['public']['constraints']['allowed_syntax']}")

print()
print("Patching tile_lessons/tile_viz_line_scatter_box.json...")
with open('batches/final_batch_012_da_viz/tile_lessons/tile_viz_line_scatter_box.json') as f:
    tl = json.load(f)

# Find and fix s15 in tile_lessons
def fix_in_tile_lesson(obj):
    """Recursively fix labels= -> tick_labels= in the tile lesson."""
    if isinstance(obj, dict):
        return {k: fix_in_tile_lesson(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [fix_in_tile_lesson(v) for v in obj]
    elif isinstance(obj, str):
        s = obj
        s = s.replace(", labels=[city_1, city_2, city_3]", ", tick_labels=[city_1, city_2, city_3]")
        s = s.replace(", labels=['Lagos', 'Abuja', 'Kano']", ", tick_labels=['Lagos', 'Abuja', 'Kano']")
        s = s.replace("used `labels`", "used `tick_labels`")
        s = s.replace("use `labels`", "use `tick_labels`")
        s = s.replace("Use `labels=", "Use `tick_labels=")
        s = s.replace("`labels=[city_1, city_2, city_3]`", "`tick_labels=[city_1, city_2, city_3]`")
        s = s.replace("`labels=['Lagos', 'Abuja', 'Kano']`", "`tick_labels=['Lagos', 'Abuja', 'Kano']`")
        # Fix allowed_syntax list item
        if s == 'labels=[...]':
            s = 'tick_labels=[...]'
        return s
    return obj

# Only fix the s15 step
fixed = False
for step in tl.get('steps', []):
    if step.get('step_id') == 'tile_viz_line_scatter_box.s15':
        # Fix the interaction within this step
        if 'interaction' in step:
            step['interaction'] = fix_in_tile_lesson(step['interaction'])
            fixed = True
            print(f"  Fixed step s15 in tile_lessons")

if not fixed:
    print("  WARNING: s15 not found in tile_lessons steps")

with open('batches/final_batch_012_da_viz/tile_lessons/tile_viz_line_scatter_box.json', 'w') as f:
    json.dump(tl, f, indent=2, ensure_ascii=False)
print("  tile_lessons/tile_viz_line_scatter_box.json written.")

# Verify tile_lessons
with open('batches/final_batch_012_da_viz/tile_lessons/tile_viz_line_scatter_box.json') as f:
    content = f.read()
bare = re.findall(r'(?<!tick_)labels=\[', content)
print(f"  Bare labels=[ remaining in tile_lessons: {bare}")

# Also check tile_lessons_public
import os
pub_path = 'batches/final_batch_012_da_viz/tile_lessons_public/tile_viz_line_scatter_box.json'
if os.path.exists(pub_path):
    print()
    print("Patching tile_lessons_public/tile_viz_line_scatter_box.json...")
    with open(pub_path) as f:
        tl_pub = json.load(f)
    
    for step in tl_pub.get('steps', []):
        if step.get('step_id') == 'tile_viz_line_scatter_box.s15':
            if 'interaction' in step:
                step['interaction'] = fix_in_tile_lesson(step['interaction'])
                print(f"  Fixed step s15 in tile_lessons_public")
    
    with open(pub_path, 'w') as f:
        json.dump(tl_pub, f, indent=2, ensure_ascii=False)
    print("  tile_lessons_public written.")
    
    with open(pub_path) as f:
        content = f.read()
    bare = re.findall(r'(?<!tick_)labels=\[', content)
    print(f"  Bare labels=[ remaining in tile_lessons_public: {bare}")

print()
print("All patches applied.")
