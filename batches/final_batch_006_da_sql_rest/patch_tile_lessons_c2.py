"""
Patch tile_lessons directly with fixed interactions (fact_ids, remediation_step_ids)
and fix the data_table cell highlight in tile_sql_null_fallback_and_union.
"""
import json, sys, hashlib

def sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()

B = 'batches/final_batch_006_da_sql_rest'

# Load the fixed interactions.json
with open(f'{B}/interactions.json') as f:
    ixdata = json.load(f)
inters = {t["tile_id"]: {i["step_id"]: i["interaction"] for i in t["interactions"]} for t in ixdata["tiles"]}

tiles_to_fix = [
    'tile_sql_style_conventions',
    'tile_sql_text_dates_casts',
    'tile_sql_null_fallback_and_union',
]

for tile_id in tiles_to_fix:
    path = f'{B}/tile_lessons/{tile_id}.json'
    with open(path) as f:
        t = json.load(f)

    ix = inters.get(tile_id, {})
    changes = 0

    # Fix interactions in steps
    for step in t.get('steps', []):
        sid = step['step_id']
        if sid in ix:
            old_ix = step.get('interaction')
            new_ix = ix[sid]
            # Preserve execution_provenance and hidden_checks from old interaction
            if old_ix and 'grading' in old_ix:
                if 'execution_provenance' in old_ix['grading']:
                    new_ix = json.loads(json.dumps(new_ix))
                    new_ix['grading']['execution_provenance'] = old_ix['grading']['execution_provenance']
                if 'hidden_checks' in old_ix['grading']:
                    new_ix['grading']['hidden_checks'] = old_ix['grading']['hidden_checks']
            step['interaction'] = new_ix
            changes += 1

    # Fix data_table cell highlight in tile_sql_null_fallback_and_union.s01
    if tile_id == 'tile_sql_null_fallback_and_union':
        for step in t.get('steps', []):
            if step['step_id'] == 'tile_sql_null_fallback_and_union.s01':
                for b in step.get('blocks', []):
                    if b.get('type') == 'before_after':
                        before = b.get('before', {})
                        if before.get('type') == 'data_table':
                            for h in before.get('highlight', []):
                                tg = h['target']
                                if tg.get('kind') == 'cell' and 'row' not in tg:
                                    tg['row'] = {"where": {"customer_id": 4}, "occurrence": 0}
                                    print(f'  Fixed cell highlight in {step["step_id"]}')
                                    changes += 1

    # Recompute content_hash
    old_hash = t.pop('content_hash', None)
    t['content_hash'] = sha(t)
    print(f'{tile_id}: {changes} changes, hash {old_hash[:8] if old_hash else "none"} -> {t["content_hash"][:8]}')

    with open(path, 'w') as f:
        json.dump(t, f, indent=2, ensure_ascii=False)
        f.write('\n')

    # Also patch tile_lessons_public
    pub_path = f'{B}/tile_lessons_public/{tile_id}.json'
    try:
        with open(pub_path) as f:
            tp = json.load(f)
        for step in tp.get('steps', []):
            sid = step['step_id']
            if sid in ix:
                old_ix = step.get('interaction')
                new_ix = json.loads(json.dumps(ix[sid]))
                # For public, remove grading from server-graded interactions
                if new_ix.get('grading_mode') == 'server':
                    new_ix.pop('grading', None)
                elif old_ix and 'grading' in old_ix:
                    if 'execution_provenance' in old_ix['grading']:
                        new_ix['grading']['execution_provenance'] = old_ix['grading']['execution_provenance']
                    if 'hidden_checks' in old_ix['grading']:
                        new_ix['grading']['hidden_checks'] = old_ix['grading']['hidden_checks']
                step['interaction'] = new_ix
        if tile_id == 'tile_sql_null_fallback_and_union':
            for step in tp.get('steps', []):
                if step['step_id'] == 'tile_sql_null_fallback_and_union.s01':
                    for b in step.get('blocks', []):
                        if b.get('type') == 'before_after':
                            before = b.get('before', {})
                            if before.get('type') == 'data_table':
                                for h in before.get('highlight', []):
                                    tg = h['target']
                                    if tg.get('kind') == 'cell' and 'row' not in tg:
                                        tg['row'] = {"where": {"customer_id": 4}, "occurrence": 0}
        with open(pub_path, 'w') as f:
            json.dump(tp, f, indent=2, ensure_ascii=False)
            f.write('\n')
        print(f'  patched tile_lessons_public/{tile_id}.json')
    except FileNotFoundError:
        print(f'  no tile_lessons_public/{tile_id}.json')

print('Done.')
