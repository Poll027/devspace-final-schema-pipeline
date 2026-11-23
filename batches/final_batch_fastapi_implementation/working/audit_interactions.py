import json,sys
from pathlib import Path
from collections import Counter
B=Path('batches/final_batch_implementation')
sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts')
from schema_check import errors
def iter_blocks(blocks):
    for block in blocks:
        yield block
        for v in block.values():
            if isinstance(v,list) and v and isinstance(v[0],dict) and "type" in v[0]:
                yield from iter_blocks(v)
out=json.loads((B/'interactions.json').read_text());plans=json.loads((B/'tile_plans.json').read_text());screens=json.loads((B/'screens.json').read_text());bundles={x['context']['concept_id']:x for x in json.loads((B/'inputs/path_glossary_bundle.json').read_text())['bundles']}
assert not errors(out,'interactions_part.schema.json')
assert [t['tile_id'] for t in out['tiles']]==[t['tile_id'] for t in plans['tiles']]
counts=Counter();native=[]
for t,p,sc in zip(out['tiles'],plans['tiles'],screens['tiles']):
 expected={s['step_id']:s for s in p['steps'] if s['type'] in ('check','hands_on')}
 actual={e['step_id']:e['interaction'] for e in t['interactions']}
 assert len(actual)==len(t['interactions']) and actual.keys()==expected.keys()
 taught=set();seen=set();rem={r['step_id']:r for r in sc.get('remediation_steps',[])}
 difficulty=[]
 for s in sc['steps']:
  if s['step_id'] in actual:
   ix=actual[s['step_id']];pl=expected[s['step_id']];counts[ix['type']]+=1;difficulty.append({'intro':0,'core':1,'stretch':2}[ix['difficulty']])
   assert ix['type']==pl['planned_interaction_type'] and ix['grading_mode']=='client'
   assert len(ix['feedback']['hints']) in (1,2)
   for c in s['concept_ids']:
    if c not in seen and any(c in r['concept_ids'] for r in rem.values()):
     r=ix['feedback']['remediation_step_id'];assert r in rem and c in rem[r]['concept_ids']
    seen.add(c)
   for m in ix['measures']:
    an=next(a for a in bundles[m['concept_id']]['assessment_anchors'] if a['capability']==m['capability'])
    assert m['fact_ids']==an['fact_ids']
    assert all('#' not in f and m['concept_id']+'#'+f in taught for f in m['fact_ids'])
   assert 'the table above' not in ix['public']['prompt'].lower()
   if ix['type']=='choice':
    assert len(ix['grading']['correct_option_ids'])==1
    assert len({x['text'] for x in ix['public']['options']})==len(ix['public']['options'])
    for o in ix['public']['options']:assert ix['grading']['option_feedback'][o['option_id']]['message']
   else:
    assert s['type']=='hands_on'
    c=s['concept_ids'][0];assert c+'#practice' in ix['anchors']
    lc=bundles[c]['practice_anchor']['live_code']
    assert ix['public']['constraints']=={k:lc[k] for k in ('allowed_syntax','blocked_syntax')}
    assert 'hidden_checks' not in ix['grading'] and 'execution_provenance' not in ix['grading']
    ws=ix['public']['workspace'];starter=next(f['content'] for f in ws['files'] if f['path']==ws['entry']);solution=next(f['content'] for f in ix['grading']['solution_files'] if f['path']==ws['entry'])
    assert starter!=solution
    if ix['public']['runtime']['kind']=='bash':native.append(s['step_id'])
  for block in iter_blocks(s.get('blocks',[])):
   if block['type'] in ('prose','callout'):taught.update(block.get('lineage',{}).get('fact_ids',[]))
 assert difficulty==sorted(difficulty)
report={'tiles':len(out['tiles']),'interactions':sum(counts.values()),'counts':dict(counts),'checks':{
 'one interaction per planned step and planned type':'pass',
 'bare fact IDs and glossary capabilities':'pass',
 'text taught before tested':'pass',
 'existing remediation IDs on first interaction per concept':'pass',
 'monotonic intro/core/stretch difficulty':'pass',
 'one keyed choice and feedback for every distractor':'pass; manually reviewed semantic uniqueness and fact-grounded misconceptions',
 'standalone prompts include the task context':'pass',
 'classify traps / table keys / cell predicates':'not applicable: none planned',
 'practice success, output names and columns':'manually reviewed all 17 solutions; native execution remains unverified for two',
 'allowed and blocked syntax copied verbatim':'pass; learner edits manually checked against the anchor, instrumentation supplied unchanged',
 'starter does not pass':'pass for pinned execution exercises via deterministic gate; native starters are incomplete',
 'test variables defined':'pass via pinned execution',
 'expected outputs derived':'15 Python-ASGI exercises executed in pinned runner; native settings expectation derived from registry source cases, native serving expectation derived from supplied endpoint; neither native result executed',
 'provenance / hashes / hidden checks not hand authored':'pass'
 },'uncertainties':{'native_runtime_exercises':native,'reason':'No bash runner is registered; pydantic-settings and a native socket/process Uvicorn environment are absent from the pinned in-process ASGI engine. These native workspaces preserve real APIs, not simulations, but need native execution validation. Syntax descriptor detector warnings also remain.'}}
(B/'working/interactions_checklist.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
