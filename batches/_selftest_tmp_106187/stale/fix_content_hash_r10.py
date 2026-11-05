"""Fix content_hash in tile_lessons after patch_pedagogy_repair_r10.py.

The sha function must use sort_keys=True, separators=(',', ':') to match finlib.sha.
The validator checks: sha({k: v for k, v in L.items() if k != 'content_hash'})
"""
import json
import hashlib
from pathlib import Path

B = Path('batches/final_batch_008_da_python_core')


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def sha(obj):
    return hashlib.sha256(canon(obj).encode()).hexdigest()


def fix_hash(path):
    with open(path) as f:
        lesson = json.load(f)
    # Hash everything except content_hash (matches validator logic)
    lesson['content_hash'] = sha({k: v for k, v in lesson.items() if k != 'content_hash'})
    with open(path, 'w') as f:
        json.dump(lesson, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print(f"Fixed {path.name}: {lesson['content_hash'][:16]}")


fix_hash(B / 'tile_lessons' / 'tile_python_operators_conversion.json')
fix_hash(B / 'tile_lessons_public' / 'tile_python_operators_conversion.json')
fix_hash(B / 'tile_lessons' / 'tile_python_pep8_style.json')
fix_hash(B / 'tile_lessons_public' / 'tile_python_pep8_style.json')

print("Done.")
