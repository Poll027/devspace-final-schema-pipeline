import json,re,collections
from pathlib import Path
B=Path('batches/final_batch_learn_python.region.01')
S=json.loads((B/'screens.json').read_text());P=json.loads((B/'tile_plans.json').read_text())
G={g['context']['concept_id']:g for g in json.loads((B/'inputs/path_glossary_bundle.json').read_text())['bundles']}
R=json.loads((B/'scenario_asset_registry.json').read_text()); assets={a['asset_id']:a for a in R['assets']}
assert [t['tile_id'] for t in S['tiles']]==[t['tile_id'] for t in P['tiles']]

def walk(b):
    yield b
    for k in ('before','after'):
        if isinstance(b.get(k),dict):yield from walk(b[k])
def words(b):
    if b['type']=='prose':return len(b['text'].split())
    if b['type']=='up_next':return len((b['title']+' '+b.get('text','')).split())
    if b['type']=='code_walkthrough':return sum(len(a['text'].split()) for a in b.get('annotations',[]))
    if b['type']=='before_after':return len(b['change_summary'].split())+words(b['before'])+words(b['after'])
    return 0

def check_lineage(l):
    for k,field in [('fact_ids','required_facts'),('teaching_block_ids','teaching_blocks')]:
        for q in l.get(k,[]):
            assert '#' in q,q
            c,f=q.split('#');assert c in G,q
            ids=[x['id'] for x in (G[c]['coverage'][field] if k=='fact_ids' else G[c][field])]
            assert f in ids,q

types=collections.Counter();rem_count=0
for tile,plan in zip(S['tiles'],P['tiles'],strict=True):
    taught=set()
    for step,ps in zip(tile['steps'],plan['steps'],strict=True):
        assert (step['step_id'],step['type'],step['concept_ids'])==(ps['step_id'],ps['type'],ps['concept_ids'])
        for key in ('teaching_block_ids','fact_ids'):assert step['lineage'][key]==ps[key]
        types[step['type']]+=1
        if step['type'] in ('check','hands_on'):
            assert not step.get('blocks') and 'interaction' not in step
            assert set(ps['fact_ids'])<=taught
            fs=set(ps['fact_ids'])
            if not fs:
                fs={c+'#'+f for c in ps['concept_ids'] for a in G[c]['assessment_anchors'] for f in a['fact_ids']}
            assert any(fs<=set(r['lineage']['fact_ids']) for r in tile['remediation_steps'])
            if step['type']=='hands_on' and ps['planned_interaction_type'] in ('choice','classify'):
                assert not re.search(r'\b(implement|build|run|execute|provision|train|commit|submit|README)\b|ws\.',step['title']+' '+step.get('lede',''),re.I)
        if ps['word_budget']:
            assert sum(words(b) for b in step.get('blocks',[]))<=ps['word_budget'],step['step_id']
        if step['type']=='recap':assert step['blocks'][-1]['type']=='up_next'
        if step['type']=='video':
            assert step['blocks']==[{'type':'media_group','segment_ids':ps['segment_ids']}]
        if ps['anchors'] and ps['planned_visual_block_type'] and step['type']=='explainer':
            assert any(b['type']==ps['planned_visual_block_type'] and set(ps['anchors'])<=set(b.get('lineage',{}).get('anchors',[])) for b in step['blocks'])
        for block in step.get('blocks',[]):
            for b in walk(block):
                if b['type']=='prose':taught.update(b['lineage']['fact_ids'])
    for c in plan['concept_ids']:
        assert {c+'#'+f['id'] for f in G[c]['coverage']['required_facts']}<=taught
    rem_count+=len(tile['remediation_steps'])
    for step in tile['steps']+tile['remediation_steps']:
        check_lineage(step['lineage'])
        for block in step.get('blocks',[]):
            for b in walk(block):
                if 'lineage' in b:check_lineage(b['lineage'])
                if b['type']=='prose':
                    assert 'lineage' in b and len(b['text'].split())<=90
                    assert not re.search(r'\bvideo\b',b['text'],re.I)
                if b['type']=='code_walkthrough':
                    assert 'output' not in b and 'execution_provenance' not in b
                    for a in b.get('annotations',[]):assert 1<=a['start_line']<=a['end_line']<=len(b['code'].splitlines())
                if b.get('asset_ref'):
                    ref=b['asset_ref'];assert ref['asset_id'] in assets
                    assert set(ref.get('columns',[]))<={c['name'] for c in assets[ref['asset_id']]['columns']}
                assert not {'result','computed_values','rows'}&b.keys()
print('CHECKLIST PASS: all assigned tiles; exact plan steps and lineage; qualified IDs; prior text teaching; fact-set remediation; prose length; word budgets; visuals and anchors; registry columns; no typed outputs or video references; framing-only interactions.')
print('COUNTS:',len(S['tiles']),'tiles;',dict(types),';',rem_count,'remediation steps')
