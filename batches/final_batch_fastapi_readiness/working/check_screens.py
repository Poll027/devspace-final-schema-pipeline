import json,re
from pathlib import Path
from collections import Counter
P=Path('batches/final_batch_readiness')
s=json.loads((P/'screens.json').read_text());p=json.loads((P/'tile_plans.json').read_text())
g=json.loads((P/'inputs/path_glossary_bundle.json').read_text());r=json.loads((P/'scenario_asset_registry.json').read_text())
bundles={b['context']['concept_id']:b for b in g['bundles']};assets={a['asset_id']:a for a in r['assets']}
allowed=json.loads(Path('00_FINAL_PIPELINE_CORE/registry/anchor_mapping.json').read_text())
fail=[];checks=Counter()
def require(test,message):
    checks['assertions']+=1
    if not test:fail.append(message)
def walk(blocks):
    for b in blocks:
        yield b
        for k in ['left','right','before','after']:
            if isinstance(b.get(k),dict):yield from walk([b[k]])
require([t['tile_id'] for t in s['tiles']]==[t['tile_id'] for t in p['tiles']],'tile coverage/order')
for t,pt in zip(s['tiles'],p['tiles']):
    require(len(t['steps'])==len(pt['steps']),t['tile_id']+' step count')
    seen=set();taught=set()
    for st,pst in zip(t['steps'],pt['steps']):
        for k in ['step_id','type','concept_ids']:require(st[k]==pst[k],st['step_id']+' plan '+k)
        for k in ['fact_ids','teaching_block_ids','segment_ids','anchors']:require(st['lineage'][k]==pst[k],st['step_id']+' lineage '+k)
        bs=list(walk(st.get('blocks',[])))
        if st['type'] in ['check','hands_on']:require('blocks' not in st and 'interaction' not in st,st['step_id']+' framing only')
        if st['type']=='video':require(st['blocks']==[{'type':'media_group','segment_ids':pst['segment_ids']}],st['step_id']+' media IDs only')
        if st['type'] in ['explainer','recap']:
            require(sum(len(b.get('text','').split()) for b in bs if b['type']=='prose')<=pst['word_budget'],st['step_id']+' budget')
        if st['type']=='explainer' and pst['planned_visual_block_type']:
            c=st['concept_ids'][0];anchor=bundles[c]['visual_anchor']['type']
            types=[pst['planned_visual_block_type']]+allowed['visual_alternates'].get(anchor,[])
            require(any(b['type'] in types and c+'#visual' in b.get('lineage',{}).get('anchors',[]) for b in bs),st['step_id']+' planned visual realization')
        if st['type']=='recap':require(any(b['type']=='up_next' for b in bs),st['step_id']+' up next')
        if st['type'] in ['check','hands_on']:
            require(set(pst['fact_ids'])<=taught,st['step_id']+' measured facts taught by earlier prose')
        for b in bs:
            if b['type']=='prose':taught.update(b['lineage']['fact_ids'])
    for st in t['steps']+t['remediation_steps']:
        require(st['step_id'] not in seen,st['step_id']+' duplicate');seen.add(st['step_id'])
        for b in walk(st.get('blocks',[])):
            checks['blocks']+=1
            require(not any(k in b for k in ['result','computed_values','output','execution_provenance']),st['step_id']+' typed computed output')
            if b['type']=='prose':
                checks['prose_blocks']+=1
                require(len(b['text'].split())<=90,st['step_id']+' prose <=90 words')
                require(bool(b.get('lineage',{}).get('fact_ids')),st['step_id']+' prose fact lineage')
                require(bool(b.get('lineage',{}).get('concept_ids')),st['step_id']+' prose concept lineage')
                require(bool(b.get('lineage',{}).get('teaching_block_ids')),st['step_id']+' prose teaching lineage')
                require(not re.search(r'\bvideo\b|as (?:shown|seen) above',b['text'],re.I),st['step_id']+' standalone text')
            for fid in b.get('lineage',{}).get('fact_ids',[]):
                cid,sep,local=fid.partition('#');require(sep and cid in bundles and local in [f['id'] for f in bundles[cid]['coverage']['required_facts']],st['step_id']+' qualified valid fact '+fid)
            for tbid in b.get('lineage',{}).get('teaching_block_ids',[]):
                cid,sep,local=tbid.partition('#');require(sep and cid in bundles and local in [v['id'] for v in bundles[cid]['teaching_blocks']],st['step_id']+' qualified valid teaching '+tbid)
            if 'asset_ref' in b:
                ar=b['asset_ref'];require(ar['asset_id'] in assets,st['step_id']+' asset exists')
                require(set(ar.get('columns',[]))<=set(c['name'] for c in assets[ar['asset_id']]['columns']),st['step_id']+' columns exist')
                require('rows' not in b and 'max_rows' not in ar,st['step_id']+' registry rows only')
            if b['type']=='code_walkthrough':
                for a in b.get('annotations',[]):require(a['start_line']<=a['end_line']<=len(b['code'].splitlines()),st['step_id']+' annotation range')
            if b['type'] in ['diagram','process_flow']:
                ids={n['id'] for n in b['nodes']}
                for e in b.get('edges',[]):require(e['from'] in ids and e['to'] in ids,st['step_id']+' visual edge resolves')
    rem=t['remediation_steps']
    for pst in pt['steps']:
        if pst['type'] in ['check','hands_on'] and pst['fact_ids']:
            require(any(set(pst['fact_ids'])<=set(st['lineage']['fact_ids']) for st in rem),pst['step_id']+' remediation measured-fact coverage')
    require(set(f['id'] for c in pt['concept_ids'] for f in bundles[c]['coverage']['required_facts'])!=set(),t['tile_id']+' glossary has facts')
    for c in pt['concept_ids']:
        require(set(c+'#'+f['id'] for f in bundles[c]['coverage']['required_facts'])<=taught,t['tile_id']+' required fact taught '+c)
checks.update({'tiles':len(s['tiles']),'planned_steps':sum(len(t['steps']) for t in s['tiles']),'remediation_steps':sum(len(t['remediation_steps']) for t in s['tiles'])})
report={'status':'PASS' if not fail else 'FAIL','counts':dict(checks),'findings':fail,'manual_review':['Re-voiced facts preserve hedges and open lists; scenario values are copied or interpolated from registry fixtures.','No future concepts taught; next-tile names appear only in required up_next framing.','SQL revised output and two-order database-test results intentionally not fabricated: execution evidence must be supplied by the later computation stage.','Final tile has no next_tile_id; up_next marks path completion rather than inventing another tile.']}
(P/'working/screens_checklist.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
raise SystemExit(bool(fail))
