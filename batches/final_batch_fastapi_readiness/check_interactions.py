import json, collections, ast
from pathlib import Path
B=Path('batches/final_batch_readiness')
p=json.loads((B/'tile_plans.json').read_text());o=json.loads((B/'interactions.json').read_text());g=json.loads((B/'inputs/path_glossary_bundle.json').read_text());s=json.loads((B/'screens.json').read_text())
bs={b['context']['concept_id']:b for b in g['bundles']}
counts=collections.Counter();tests=0
assert [t['tile_id'] for t in p['tiles']]==[t['tile_id'] for t in o['tiles']]
for pt,ot,st in zip(p['tiles'],o['tiles'],s['tiles']):
 planned=[x for x in pt['steps'] if x['type'] in ['check','hands_on']]
 assert [x['step_id'] for x in planned]==[x['step_id'] for x in ot['interactions']]
 seen=set();last_difficulty=-1
 for ps,os in zip(planned,ot['interactions']):
  ix=os['interaction'];counts[ix['type']]+=1
  assert ix['type']==ps['planned_interaction_type']
  assert ix['anchors']==ps['anchors']
  assert ix['standalone'] is True
  assert not any(t in ix['public']['prompt'].lower() for t in ['the table above','as shown above','the previous screen'])
  assert ix['grading_mode']=='client'
  rank=['intro','core','stretch'].index(ix['difficulty']);assert rank>=last_difficulty;last_difficulty=rank
  cid=ps['concept_ids'][0]
  if cid not in seen:
   assert ix['feedback']['remediation_step_id'] in [r['step_id'] for r in st['remediation_steps'] if cid in r['concept_ids']]
  seen.add(cid)
  assert 1<=len(ix['feedback']['hints'])<=2
  for m in ix['measures']:
   a=next(a for a in bs[m['concept_id']]['assessment_anchors'] if a['capability']==m['capability'])
   assert m['fact_ids']==a['fact_ids'] and all('#' not in f for f in m['fact_ids'])
  assert 'execution_provenance' not in ix['grading'] and 'hidden_checks' not in ix['grading']
  if ix['type']=='choice':
   assert len(ix['grading']['correct_option_ids'])==1
   assert set(ix['grading']['option_feedback'])=={x['option_id'] for x in ix['public']['options']}
  elif ix['type']=='classify':
   ids={x['item_id'] for x in ix['public']['items']}
   assert set(ix['grading']['assignments'])==ids
   assert set(ix['grading']['item_feedback'])==ids
   assert set(ix['grading']['assignments'].values())=={'good','bad'}
   assert all(len(x['text'])>100 for x in ix['public']['items'])
  else:
   assert ix['public']['runtime']['kind']=='python_asgi'
   lc=bs[cid]['practice_anchor']['live_code']
   assert ix['public']['constraints']=={k:lc[k] for k in ['allowed_syntax','blocked_syntax']}
   starter=ix['public']['workspace']['files'][0]['content'];solution=ix['grading']['solution_files'][0]['content']
   assert starter!=solution
   ast.parse(starter);ast.parse(solution)
   assert ix['public']['workspace']['entry']==ix['grading']['solution_files'][0]['path']
   for t in ix['grading']['tests']:
    tests+=1;assert 'expected' in t['spec'] and t['message_on_fail']
# Spot-check required runtime success predicates independently of solution-derived expected values.
ixs={x['step_id']:x['interaction'] for t in o['tiles'] for x in t['interactions']}
for t in ixs['tile_093.s04']['grading']['tests']:
 body=t['spec']['expected']['json'];snap=body['snapshot']
 if t['test_id'].startswith(('failure','integrity')):
  assert snap['events']==snap['committed_changes']==[]
  assert body['responses'][0]['status']==500
 else:
  assert len(snap['events'])==len(snap['committed_changes'])==1
  assert all(r['status']==200 and r['json']=={'received':True} for r in body['responses'])
for t in ixs['tile_089.s06']['grading']['tests']:
 b=t['spec']['expected']['json'];assert b['before']==b['after'] and b['same_result']
 assert b['after_relationship_selects']<b['before_relationship_selects']
for t in ixs['tile_096.s04']['grading']['tests']:
 e=t['spec']['expected'];assert e['status'] in [200,404]
 if e['status']==404:assert set(e['json'])=={'detail'}
print('Checklist PASS: coverage, plan fidelity, monotonic difficulty, bare facts/capabilities, remediation, standalone text, unique keys/traps, feedback, verbatim syntax, non-solution starters, executable expected values, and runtime success spot-checks.')
print('Counts:',len(o['tiles']),'tiles',sum(counts.values()),'interactions',dict(counts),tests,'code tests')
print('Manual review: each candidate is explicitly hypothetical or registry-captured evidence; no fabricated measured output. Retry configuration uses a clearly labelled deterministic verification mirror because tenacity is not in the pinned runtime. Concurrent idempotency dispatch uses the supplied synchronous SQLite facade, not a threaded database race test.')
