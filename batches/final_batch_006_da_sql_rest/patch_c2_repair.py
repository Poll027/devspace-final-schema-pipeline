"""
Repair patch for interactions.part.c2.json and screens.json.

Fixes:
1. fact_ids in measures: strip the 'concept_id#' prefix (e.g. 'sql.coalesce#f1' -> 'f1')
2. remediation_step_ids in tile_sql_null_fallback_and_union: change s01/s05/s06 to r01/r02/r03/r04
3. remediation_step_ids in tile_sql_text_dates_casts: change s01/s04/s07 to r01/r02/r03/r04/r05/r06
4. screens.json: add 'row' to the cell highlight in tile_sql_null_fallback_and_union.s01 data_table
"""
import json
import copy

# ── 1. Fix interactions.part.c2.json ─────────────────────────────────────────

with open('batches/final_batch_006_da_sql_rest/interactions.part.c2.json') as f:
    data = json.load(f)

# Mapping of wrong remediation_step_ids to correct ones
# tile_sql_text_dates_casts
text_dates_rem_map = {
    'tile_sql_text_dates_casts.s01': 'tile_sql_text_dates_casts.r01',
    'tile_sql_text_dates_casts.s04': 'tile_sql_text_dates_casts.r04',
    'tile_sql_text_dates_casts.s07': 'tile_sql_text_dates_casts.r06',
}
# tile_sql_null_fallback_and_union
null_fallback_rem_map = {
    'tile_sql_null_fallback_and_union.s01': 'tile_sql_null_fallback_and_union.r01',
    'tile_sql_null_fallback_and_union.s06': 'tile_sql_null_fallback_and_union.r03',
    'tile_sql_null_fallback_and_union.s05': 'tile_sql_null_fallback_and_union.r04',
}

# Per-step remediation overrides (to ensure all r-steps are referenced)
# text_dates_casts:
#   s02 measures string_functions#f1 -> r01 (teaches f1)
#   s03 measures string_functions#f2,f3,f4 -> r02 (teaches f2,f3,f4)
#   s05 measures date_time_functions#f2 -> r03 (teaches f2)
#   s06 measures date_time_functions#f1,f2 -> r04 (teaches f1,f2)
#   s08 measures type_casting#f2 -> r05 (teaches f2)
#   s09 measures type_casting#f1 -> r06 (teaches f1)
text_dates_step_rem = {
    'tile_sql_text_dates_casts.s02': 'tile_sql_text_dates_casts.r01',
    'tile_sql_text_dates_casts.s03': 'tile_sql_text_dates_casts.r02',
    'tile_sql_text_dates_casts.s05': 'tile_sql_text_dates_casts.r03',
    'tile_sql_text_dates_casts.s06': 'tile_sql_text_dates_casts.r04',
    'tile_sql_text_dates_casts.s08': 'tile_sql_text_dates_casts.r05',
    'tile_sql_text_dates_casts.s09': 'tile_sql_text_dates_casts.r06',
}
# null_fallback:
#   s02 measures coalesce#f1 -> r01 (teaches f1)
#   s03 measures coalesce#f2 -> r02 (teaches f2)
#   s04 measures coalesce#f1,f2 -> r01 (teaches f1, which is in measured set)
#   s07 measures union#f3 -> r03 (teaches f3)
#   s08 measures union#f1,f2 -> r04 (teaches f1,f2)
null_fallback_step_rem = {
    'tile_sql_null_fallback_and_union.s02': 'tile_sql_null_fallback_and_union.r01',
    'tile_sql_null_fallback_and_union.s03': 'tile_sql_null_fallback_and_union.r02',
    'tile_sql_null_fallback_and_union.s04': 'tile_sql_null_fallback_and_union.r01',
    'tile_sql_null_fallback_and_union.s07': 'tile_sql_null_fallback_and_union.r03',
    'tile_sql_null_fallback_and_union.s08': 'tile_sql_null_fallback_and_union.r04',
}

all_step_rem = {**text_dates_step_rem, **null_fallback_step_rem}

for tile in data['tiles']:
    for step in tile.get('interactions', []):
        ix = step.get('interaction', {})
        sid = step['step_id']

        # Fix fact_ids: strip 'concept_id#' prefix
        for m in ix.get('measures', []):
            cid = m['concept_id']
            prefix = cid + '#'
            m['fact_ids'] = [
                fid[len(prefix):] if fid.startswith(prefix) else fid
                for fid in m.get('fact_ids', [])
            ]

        # Fix remediation_step_id
        fb = ix.get('feedback', {})
        if fb and 'remediation_step_id' in fb:
            if sid in all_step_rem:
                fb['remediation_step_id'] = all_step_rem[sid]

with open('batches/final_batch_006_da_sql_rest/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write('\n')

print("interactions.part.c2.json patched")

# ── 2. Fix screens.json: add 'row' to cell highlight ─────────────────────────

with open('batches/final_batch_006_da_sql_rest/screens.json') as f:
    screens = json.load(f)

for tile in screens['tiles']:
    if tile['tile_id'] == 'tile_sql_null_fallback_and_union':
        for step in tile.get('steps', []):
            if step['step_id'] == 'tile_sql_null_fallback_and_union.s01':
                for b in step.get('blocks', []):
                    if b.get('type') == 'before_after':
                        before = b.get('before', {})
                        if before.get('type') == 'data_table':
                            for h in before.get('highlight', []):
                                tg = h['target']
                                if tg.get('kind') == 'cell' and 'row' not in tg:
                                    # Add row pointing to customer 4 (first NULL city row)
                                    tg['row'] = {"where": {"customer_id": 4}, "occurrence": 0}
                                    print(f"Fixed cell highlight in {step['step_id']}/data_table")

with open('batches/final_batch_006_da_sql_rest/screens.json', 'w') as f:
    json.dump(screens, f, indent=2, ensure_ascii=False)
    f.write('\n')

print("screens.json patched")
