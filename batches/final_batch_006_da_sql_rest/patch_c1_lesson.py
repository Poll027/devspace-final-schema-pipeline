"""
Patch tile_lessons/tile_sql_fund_sorting_limiting.json:
Fix remediation_step_id references (s01->r01, s04->r02) and recompute content_hash.
Also patch interactions.json for consistency.
"""
import json
import hashlib
import sys
sys.path.insert(0, '00_FINAL_PIPELINE_CORE/scripts')
from finlib import sha, save, load

B = 'batches/final_batch_006_da_sql_rest'

fixes = {
    "tile_sql_fund_sorting_limiting.s01": "tile_sql_fund_sorting_limiting.r01",
    "tile_sql_fund_sorting_limiting.s04": "tile_sql_fund_sorting_limiting.r02",
}

# 1. Patch interactions.json
path_ix = f"{B}/interactions.json"
data = load(path_ix)
changed = 0
for tile in data["tiles"]:
    if tile["tile_id"] != "tile_sql_fund_sorting_limiting":
        continue
    for ix_entry in tile["interactions"]:
        fb = ix_entry["interaction"].get("feedback", {})
        rid = fb.get("remediation_step_id")
        if rid in fixes:
            fb["remediation_step_id"] = fixes[rid]
            print(f"  interactions.json {ix_entry['step_id']}: {rid} -> {fixes[rid]}")
            changed += 1
save(path_ix, data)
print(f"interactions.json: {changed} changes")

# 2. Patch tile_lessons/tile_sql_fund_sorting_limiting.json
path_lesson = f"{B}/tile_lessons/tile_sql_fund_sorting_limiting.json"
lesson = load(path_lesson)
changed = 0
for s in lesson["steps"]:
    fb = s.get("interaction", {}).get("feedback", {})
    rid = fb.get("remediation_step_id")
    if rid in fixes:
        fb["remediation_step_id"] = fixes[rid]
        print(f"  tile_lessons {s['step_id']}: {rid} -> {fixes[rid]}")
        changed += 1
# Recompute content_hash
lesson["content_hash"] = sha({k: v for k, v in lesson.items() if k != "content_hash"})
save(path_lesson, lesson)
print(f"tile_lessons: {changed} changes, new hash: {lesson['content_hash'][:12]}")

# 3. Patch tile_lessons_public if it exists
import os
path_pub = f"{B}/tile_lessons_public/tile_sql_fund_sorting_limiting.json"
if os.path.exists(path_pub):
    pub = load(path_pub)
    changed = 0
    for s in pub.get("steps", []):
        fb = s.get("interaction", {}).get("feedback", {})
        rid = fb.get("remediation_step_id")
        if rid in fixes:
            fb["remediation_step_id"] = fixes[rid]
            print(f"  tile_lessons_public {s['step_id']}: {rid} -> {fixes[rid]}")
            changed += 1
    # Recompute content_hash if present
    if "content_hash" in pub:
        pub["content_hash"] = sha({k: v for k, v in pub.items() if k != "content_hash"})
    save(path_pub, pub)
    print(f"tile_lessons_public: {changed} changes")

print("Done.")
