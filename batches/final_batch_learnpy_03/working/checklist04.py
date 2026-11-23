import json, collections, contextlib, io
from pathlib import Path
B=Path('batches/final_batch_learn_python.region.03')
a=json.load(open(B/'interactions.json'));p=json.load(open(B/'tile_plans.json'));s=json.load(open(B/'screens.json'));g=json.load(open(B/'inputs/path_glossary_bundle.json'));cs={c['context']['concept_id']:c for c in g['bundles']}
counts=collections.Counter();ncode=0
for tile,plan,screen in zip(a['tiles'],p['tiles'],s['tiles']):
 wanted={x['step_id']:x for x in plan['steps'] if x['type'] in ['check','hands_on']}
 assert set(wanted)=={i['step_id'] for i in tile['interactions']}
 rem={x['step_id'] for x in screen['remediation_steps']};seen=set();taught=set()
 for step in plan['steps']:
  if step['type']=='explainer':taught.update(step['fact_ids'])
  if step['step_id'] not in wanted:continue
  ix=next(x['interaction'] for x in tile['interactions'] if x['step_id']==step['step_id']);counts[ix['type']]+=1
  assert ix['type']==step['planned_interaction_type']
  assert 1<=len(ix['feedback']['hints'])<=2
  for m in ix['measures']:
   anchor=next(x for x in cs[m['concept_id']]['assessment_anchors'] if x['capability']==m['capability'])
   assert m['fact_ids']==anchor['fact_ids']
   assert all('#' not in fid and m['concept_id']+'#'+fid in taught for fid in m['fact_ids'])
  cid=step['concept_ids'][0]
  if cid not in seen:assert ix['feedback']['remediation_step_id'] in rem
  seen.add(cid)
  if step['type']=='hands_on':assert cid+'#practice' in ix['anchors']
  if ix['type']=='choice':
   assert len(ix['grading']['correct_option_ids'])==1
   assert len({o['text'] for o in ix['public']['options']})==len(ix['public']['options'])
   assert {o['option_id'] for o in ix['public']['options']}==set(ix['grading']['option_feedback'])
   for o in ix['public']['options']:assert ix['grading']['option_feedback'][o['option_id']]['message']
  if ix['type']=='classify':
   assert set(ix['grading']['assignments'])=={i['item_id'] for i in ix['public']['items']}
   assert any(i['text']=='KeyboardInterrupt' for i in ix['public']['items'])
  if ix['type']=='code_exercise':
   ncode+=1
   assert ix['public']['constraints']=={k:cs[cid]['practice_anchor']['live_code'][k] for k in ['allowed_syntax','blocked_syntax']}
   assert 'execution_provenance' not in ix['grading'] and 'hidden_checks' not in ix['grading']
   assert ix['public']['workspace']['entry']==ix['grading']['solution_files'][0]['path']
   sol=ix['grading']['solution_files'][0]['content'];starter=ix['public']['workspace']['files'][0]['content']
   assert sol!=starter
   out=io.StringIO();ns={}
   with contextlib.redirect_stdout(out):exec(compile(sol,'main.py','exec'),ns)
   for t in ix['grading']['tests']:
    spec=t['spec']
    if t['kind']=='value_equals':got=eval(spec['expr'],ns)
    elif t['kind']=='function_call':got=ns[spec['function']](*spec.get('args',[]),**spec.get('kwargs',{}))
    elif t['kind']=='stdout_equals':got=out.getvalue().strip()
    assert json.loads(json.dumps(got))==spec['expected']
   compiled=json.load(open(B/'tile_lessons'/ (tile['tile_id']+'.json')))
   ci=next(x['interaction'] for x in compiled['steps'] if x['step_id']==step['step_id'])
   assert ci['grading']['execution_provenance']['tests_passed']==len(ix['grading']['tests'])
print('Checklist passed: exact plan coverage; bare fact IDs and glossary capabilities; taught-before-tested; valid copied remediation; all wrong choices explained; unique single-choice keys; hierarchy trap present; code expectations re-executed; constraints copied; no authored provenance; non-solution starters; all required outputs named in prompts (manual review).')
print('Counts:',len(a['tiles']),'tiles',dict(counts),'total',sum(counts.values()))
print('Manual review: supplied candidate implementations used where descriptor detection does not support direct learner definitions/operators. Success sentences hold for selected executed implementations. Debugger practice uses registered recorded session; not live interactive pdb.')
