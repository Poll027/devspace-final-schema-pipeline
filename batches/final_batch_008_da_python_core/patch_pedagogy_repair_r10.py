"""Repair round patch for pedagogy review findings.

Finding 1 (tile_python_operators_conversion/s10, in c1.json):
  opt_b feedback falsely claims the result would be False under alternative priority.
  Fix: Replace feedback with the correct explanation.
  NOTE: c1.json already has this fix. Sync to interactions.json and tile_lessons.

Finding 2 (tile_python_pep8_style/s03, in c3.json):
  Instruction #3 says rename Minutes->minutes and Rate->rate but starter already
  uses lowercase minutes and rate (as top-level vars; the instruction is confusing/wrong).
  Fix: Remove instruction #3 and renumber remaining instructions.
  NOTE: c3.json already has this fix. Sync to interactions.json and tile_lessons.
"""
import json
import hashlib
from pathlib import Path

B = Path('batches/final_batch_008_da_python_core')


def sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


# ── Load source parts ────────────────────────────────────────────────────────
with open(B / 'interactions.part.c1.json') as f:
    c1 = json.load(f)

with open(B / 'interactions.part.c3.json') as f:
    c3 = json.load(f)

# ── Extract the fixed interactions from parts ────────────────────────────────
# From c1: tile_python_operators_conversion s10 opt_b feedback
c1_ops_conv = None
for tile in c1['tiles']:
    if tile['tile_id'] == 'tile_python_operators_conversion':
        c1_ops_conv = {ix['step_id']: ix['interaction'] for ix in tile['interactions']}
        break

# From c3: tile_python_pep8_style s03 prompt
c3_pep8 = None
for tile in c3['tiles']:
    if tile['tile_id'] == 'tile_python_pep8_style':
        c3_pep8 = {ix['step_id']: ix['interaction'] for ix in tile['interactions']}
        break

# ── Patch interactions.json ──────────────────────────────────────────────────
with open(B / 'interactions.json') as f:
    interactions = json.load(f)

for tile in interactions['tiles']:
    if tile['tile_id'] == 'tile_python_operators_conversion' and c1_ops_conv:
        for ix_entry in tile['interactions']:
            sid = ix_entry['step_id']
            if sid == 'tile_python_operators_conversion.s10' and sid in c1_ops_conv:
                # Sync opt_b feedback from c1
                src_grading = c1_ops_conv[sid].get('grading', {})
                src_opt_b = src_grading.get('option_feedback', {}).get('opt_b', {})
                if src_opt_b:
                    ix_entry['interaction']['grading']['option_feedback']['opt_b'] = src_opt_b
                    print(f"Patched {sid} opt_b feedback in interactions.json")

    if tile['tile_id'] == 'tile_python_pep8_style' and c3_pep8:
        for ix_entry in tile['interactions']:
            sid = ix_entry['step_id']
            if sid == 'tile_python_pep8_style.s03' and sid in c3_pep8:
                # Sync prompt from c3 (instruction #3 removed, renumbered)
                src_prompt = c3_pep8[sid]['public']['prompt']
                ix_entry['interaction']['public']['prompt'] = src_prompt
                print(f"Patched {sid} prompt in interactions.json")

with open(B / 'interactions.json', 'w') as f:
    json.dump(interactions, f, indent=2, ensure_ascii=False)
print("interactions.json updated")

# ── Patch tile_lessons ───────────────────────────────────────────────────────
# Patch tile_python_operators_conversion.json
ops_lesson_path = B / 'tile_lessons' / 'tile_python_operators_conversion.json'
with open(ops_lesson_path) as f:
    ops_lesson = json.load(f)

for step in ops_lesson['steps']:
    if step['step_id'] == 'tile_python_operators_conversion.s10':
        src_opt_b = c1_ops_conv['tile_python_operators_conversion.s10']['grading']['option_feedback']['opt_b']
        step['interaction']['grading']['option_feedback']['opt_b'] = src_opt_b
        print(f"Patched tile_lessons/tile_python_operators_conversion.json s10 opt_b")
        break

ops_lesson['content_hash'] = sha(ops_lesson)
with open(ops_lesson_path, 'w') as f:
    json.dump(ops_lesson, f, indent=2, ensure_ascii=False)
print("tile_lessons/tile_python_operators_conversion.json updated")

# Patch tile_lessons_public/tile_python_operators_conversion.json
ops_pub_path = B / 'tile_lessons_public' / 'tile_python_operators_conversion.json'
if ops_pub_path.exists():
    with open(ops_pub_path) as f:
        ops_pub = json.load(f)
    for step in ops_pub['steps']:
        if step['step_id'] == 'tile_python_operators_conversion.s10':
            src_opt_b = c1_ops_conv['tile_python_operators_conversion.s10']['grading']['option_feedback']['opt_b']
            step['interaction']['grading']['option_feedback']['opt_b'] = src_opt_b
            print(f"Patched tile_lessons_public/tile_python_operators_conversion.json s10 opt_b")
            break
    ops_pub['content_hash'] = sha({k: v for k, v in ops_pub.items() if k != 'content_hash'})
    with open(ops_pub_path, 'w') as f:
        json.dump(ops_pub, f, indent=2, ensure_ascii=False)
    print("tile_lessons_public/tile_python_operators_conversion.json updated")

# Patch tile_lessons/tile_python_pep8_style.json
pep8_lesson_path = B / 'tile_lessons' / 'tile_python_pep8_style.json'
with open(pep8_lesson_path) as f:
    pep8_lesson = json.load(f)

for step in pep8_lesson['steps']:
    if step['step_id'] == 'tile_python_pep8_style.s03':
        src_prompt = c3_pep8['tile_python_pep8_style.s03']['public']['prompt']
        step['interaction']['public']['prompt'] = src_prompt
        print(f"Patched tile_lessons/tile_python_pep8_style.json s03 prompt")
        break

pep8_lesson['content_hash'] = sha(pep8_lesson)
with open(pep8_lesson_path, 'w') as f:
    json.dump(pep8_lesson, f, indent=2, ensure_ascii=False)
print("tile_lessons/tile_python_pep8_style.json updated")

# Patch tile_lessons_public/tile_python_pep8_style.json
pep8_pub_path = B / 'tile_lessons_public' / 'tile_python_pep8_style.json'
if pep8_pub_path.exists():
    with open(pep8_pub_path) as f:
        pep8_pub = json.load(f)
    for step in pep8_pub['steps']:
        if step['step_id'] == 'tile_python_pep8_style.s03':
            src_prompt = c3_pep8['tile_python_pep8_style.s03']['public']['prompt']
            step['interaction']['public']['prompt'] = src_prompt
            print(f"Patched tile_lessons_public/tile_python_pep8_style.json s03 prompt")
            break
    pep8_pub['content_hash'] = sha({k: v for k, v in pep8_pub.items() if k != 'content_hash'})
    with open(pep8_pub_path, 'w') as f:
        json.dump(pep8_pub, f, indent=2, ensure_ascii=False)
    print("tile_lessons_public/tile_python_pep8_style.json updated")

print("\nAll patches applied.")
