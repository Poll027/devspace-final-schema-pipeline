"""
Patch interactions.json (the merged file) with the same fixes as interactions.part.c2.json.
"""
import json

with open('batches/final_batch_006_da_sql_rest/interactions.json') as f:
    data = json.load(f)

# Per-step remediation overrides
all_step_rem = {
    # text_dates_casts
    'tile_sql_text_dates_casts.s02': 'tile_sql_text_dates_casts.r01',
    'tile_sql_text_dates_casts.s03': 'tile_sql_text_dates_casts.r02',
    'tile_sql_text_dates_casts.s05': 'tile_sql_text_dates_casts.r03',
    'tile_sql_text_dates_casts.s06': 'tile_sql_text_dates_casts.r04',
    'tile_sql_text_dates_casts.s08': 'tile_sql_text_dates_casts.r05',
    'tile_sql_text_dates_casts.s09': 'tile_sql_text_dates_casts.r06',
    # null_fallback
    'tile_sql_null_fallback_and_union.s02': 'tile_sql_null_fallback_and_union.r01',
    'tile_sql_null_fallback_and_union.s03': 'tile_sql_null_fallback_and_union.r02',
    'tile_sql_null_fallback_and_union.s04': 'tile_sql_null_fallback_and_union.r01',
    'tile_sql_null_fallback_and_union.s07': 'tile_sql_null_fallback_and_union.r03',
    'tile_sql_null_fallback_and_union.s08': 'tile_sql_null_fallback_and_union.r04',
    # style_conventions (also has s01 as remediation_step_id, fix to r01)
    'tile_sql_style_conventions.s02': 'tile_sql_style_conventions.r01',
    'tile_sql_style_conventions.s03': 'tile_sql_style_conventions.r01',
}

changes = 0
for tile in data['tiles']:
    for step in tile.get('interactions', []):
        ix = step.get('interaction', {})
        sid = step['step_id']

        # Fix fact_ids: strip 'concept_id#' prefix
        for m in ix.get('measures', []):
            cid = m['concept_id']
            prefix = cid + '#'
            new_fids = [
                fid[len(prefix):] if fid.startswith(prefix) else fid
                for fid in m.get('fact_ids', [])
            ]
            if new_fids != m['fact_ids']:
                print(f'  Fixed fact_ids in {sid}: {m["fact_ids"]} -> {new_fids}')
                m['fact_ids'] = new_fids
                changes += 1

        # Fix remediation_step_id
        fb = ix.get('feedback', {})
        if fb and 'remediation_step_id' in fb:
            if sid in all_step_rem:
                old = fb['remediation_step_id']
                new = all_step_rem[sid]
                if old != new:
                    print(f'  Fixed remediation_step_id in {sid}: {old} -> {new}')
                    fb['remediation_step_id'] = new
                    changes += 1

print(f'\nTotal changes: {changes}')

with open('batches/final_batch_006_da_sql_rest/interactions.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write('\n')

print("interactions.json patched")
