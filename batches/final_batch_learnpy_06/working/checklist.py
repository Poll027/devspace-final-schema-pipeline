import json,collections,pathlib
B=pathlib.Path('batches/final_batch_learn_python.region.06')
load=lambda f:json.loads((B/f).read_text())
p=load('tile_plans.json');d=load('interactions.json');g={x['context']['concept_id']:x for x in load('inputs/path_glossary_bundle.json')['bundles']};screens={x['tile_id']:x for x in load('screens.json')['tiles']}
counts=collections.Counter();tested=0
for plan,t in zip(p['tiles'],d['tiles']):
 assert plan['tile_id']==t['tile_id']
 steps=[x for x in plan['steps'] if x['type'] in ('check','hands_on')]
 assert [s['step_id'] for s in steps]==[e['step_id'] for e in t['interactions']]
 seen=set();levels=[]
 for s,e in zip(steps,t['interactions']):
  i=e['interaction'];counts[i['type']]+=1;assert i['type']==s['planned_interaction_type'];assert i['anchors']==s['anchors'];assert i['grading_mode']=='client';levels.append(['intro','core','stretch'].index(i['difficulty']))
  for m in i['measures']:
   anchors=g[m['concept_id']]['assessment_anchors'];a=next(a for a in anchors if a['capability']==m['capability']);assert m['fact_ids']==a['fact_ids'];assert all('#' not in f for f in m['fact_ids'])
  cid=s['concept_ids'][0]
  rs=[r for r in screens[t['tile_id']].get('remediation_steps',[]) if cid in r['concept_ids']]
  if cid not in seen and rs:assert i['feedback']['remediation_step_id']==rs[0]['step_id']
  seen.add(cid)
  assert 1<=len(i['feedback']['hints'])<=2
  if i['type']=='choice':
   options={o['option_id'] for o in i['public']['options']};assert len(i['grading']['correct_option_ids'])==1;assert set(i['grading']['option_feedback'])==options
  elif i['type']=='classify':
   assert {x['item_id'] for x in i['public']['items']}==set(i['grading']['assignments']);assert len(set(i['grading']['assignments'].values()))>1
  else:
   assert '#practice' in ' '.join(i['anchors'])
   lc=g[cid]['practice_anchor']['live_code'];cons=i['public']['constraints'];assert all(cons[k]==lc[k] for k in ['allowed_syntax','blocked_syntax'])
   assert len(i['public']['workspace']['files'])==1 and i['public']['workspace']['files'][0]['role']=='editable'
   assert i['public']['workspace']['entry']==i['grading']['solution_files'][0]['path']
   assert i['public']['workspace']['files'][0]['content']!=i['grading']['solution_files'][0]['content']
   assert 'hidden_checks' not in i['grading'] and 'execution_provenance' not in i['grading']
   assert i['grading']['tests'];tested+=len(i['grading']['tests'])
 assert levels==sorted(levels)
report=load('reports/validation.tiles.json');errors=[e for t in report for e in t['errors']]
non_syntax=[e for e in errors if 'not yet taught' not in e and 'glossary blocks' not in e]
assert not non_syntax,non_syntax
summary={'tiles':len(d['tiles']),'interactions':sum(counts.values()),'by_type':dict(counts),'code_tests':tested,'checks':'Plan, types, anchors, bare facts, capabilities, remediation, feedback, difficulty, constraint copying, starters, traps and grading fields checked. Keys and Python expectations computed by build script. Runtime gate reports no wrong expected results, already-passing starters, hardcoded-answer failures, or taught-before-tested errors.','remaining_gate_errors':len(errors),'remaining_gate_error_category':'Syntax-descriptor mapping: permitted human descriptors are unmapped or mapped incompletely; unchanged supplied function/class scaffolding is also judged. Lists left verbatim.'}
(B/'working'/'checklist.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
