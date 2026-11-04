import json
import hashlib
import sys
sys.path.insert(0, '00_FINAL_PIPELINE_CORE/scripts')

def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def sha(obj):
    return hashlib.sha256(canon(obj).encode()).hexdigest()

# Patch tile_lessons
fpath = 'batches/final_batch_008_da_python_core/tile_lessons/tile_python_lists_dicts_tuples.json'
with open(fpath) as f:
    data = json.load(f)

patched = False
for step in data['steps']:
    if step['step_id'] == 'tile_python_lists_dicts_tuples.s13':
        ix = step.get('interaction', {})
        caps = [m['capability'] for m in ix.get('measures', [])]
        if 'recognize_tuple_immutability' not in caps:
            ix['measures'].append({
                "concept_id": "python.tuples",
                "capability": "recognize_tuple_immutability",
                "fact_ids": ["f2"]
            })
            ix['anchors'].append("python.tuples#assessment:recognize_tuple_immutability")
            patched = True
            print("Patched s13 in tile_lessons")
        else:
            print("s13 already has recognize_tuple_immutability in tile_lessons")
        break

# Recompute content_hash
old_hash = data.get('content_hash')
data['content_hash'] = sha({k: v for k, v in data.items() if k != 'content_hash'})
print(f"Old content_hash: {old_hash[:16]}...")
print(f"New content_hash: {data['content_hash'][:16]}...")

with open(fpath, 'w') as f:
    json.dump(data, f, indent=2)

print("Done.")
