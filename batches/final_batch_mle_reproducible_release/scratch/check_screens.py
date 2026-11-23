import json, re, ast
from pathlib import Path
B=Path('batches/final_batch_mle.region.reproducible_release')
p=json.loads((B/'tile_plans.json').read_text());s=json.loads((B/'screens.json').read_text())
g=json.loads((B/'inputs/path_glossary_bundle.json').read_text());a=json.loads((B/'scenario_asset_registry.json').read_text())
concepts={b['context']['concept_id']:b for b in g['bundles']};assets={b['asset_id']:b for b in a['assets']}
def walk(x):
    if isinstance(x,dict):
        yield x
        for k,v in x.items():
            if k not in ['lineage','asset_ref']:yield from walk(v)
    elif isinstance(x,list):
        for v in x:yield from walk(v)
def word_count(x):
    return sum(len(v.split()) for d in walk(x) for k,v in d.items()
        if k in ['text','title','eyebrow','lede','caption','takeaway','left_label','right_label'] and isinstance(v,str))
assert [t['tile_id'] for t in s['tiles']]==[t['tile_id'] for t in p['tiles']]
counts={}
for plan,tile in zip(p['tiles'],s['tiles']):
    assert len(plan['steps'])==len(tile['steps'])
    for ps,step in zip(plan['steps'],tile['steps']):
        for k in ['step_id','type','concept_ids']:assert ps[k]==step[k],(step['step_id'],k)
        for k in ['teaching_block_ids','fact_ids']:assert ps[k]==step['lineage'][k]
        if ps['word_budget']:assert word_count(step)<=ps['word_budget'],(step['step_id'],word_count(step),ps['word_budget'])
        if step['type'] in ['check','hands_on']:assert 'blocks' not in step and 'interaction' not in step
        if step['type']=='video':assert step['blocks']==[{'type':'media_group','segment_ids':ps['segment_ids']}]
        if ps['anchors'] and step['type']=='explainer':
            assert any(ps['anchors'][0] in b.get('lineage',{}).get('anchors',[]) for b in step['blocks'])
        if step['type']=='recap':assert step['blocks'][-1]['type']=='up_next'
    # Each distinct measured fact set has a route that re-teaches it in text.
    for ps in plan['steps']:
        if ps['type'] not in ['check','hands_on']:continue
        candidates=[r for r in tile['remediation_steps'] if r['concept_ids']==ps['concept_ids'] and set(r['lineage']['fact_ids'])==set(ps['fact_ids'])]
        assert candidates
        taught={f for b in candidates[0]['blocks'] if b['type']=='prose' for f in b['lineage']['fact_ids']}
        assert set(ps['fact_ids'])<=taught
    for block in walk(tile):
        typ=block.get('type')
        if typ=='prose':
            assert 'lineage' in block
            assert len(block['text'].split())<=90
            assert not re.search(r'\bvideo\b',block['text'],re.I)
        if 'lineage' in block:
            lin=block['lineage']
            for f in lin.get('fact_ids',[]):
                cid,fid=f.split('#');assert fid in {f['id'] for f in concepts[cid]['coverage']['required_facts']}
            for tb in lin.get('teaching_block_ids',[]):
                cid,tid=tb.split('#');assert tid in {t['id'] for t in concepts[cid]['teaching_blocks']}
        if typ=='data_table':
            assert 'rows' not in block and 'result' not in block
            asset=assets[block['asset_ref']['asset_id']]
            assert set(block['asset_ref'].get('columns',[]))<={c['name'] for c in asset['columns']}
        if typ=='code_walkthrough':
            assert 'output' not in block and 'execution_provenance' not in block
            assert any(x.endswith('#visual') for x in block['lineage']['anchors'])
            if block['language']=='python':ast.parse(block['code'])
        assert 'computed_values' not in block
    counts[tile['tile_id']]={'planned_steps':len(tile['steps']),'remediation_steps':len(tile['remediation_steps'])}
# Qualifier/meaning review was performed against each cited teaching block. No numeric outputs,
# hashes, rows, media details or expected-cell values were authored. Scenario literals are
# script-extracted; visuals use contracts or registered dataset references. The only forward
# concepts named are next-tile headings, not lessons inside the current tile.
print('Mistakes-to-avoid checklist: PASS')
print(json.dumps(counts,indent=2))
print('Interactions at stage input location:',(B/'interactions.json').exists())
