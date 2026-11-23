import json,ast
from pathlib import Path
B=Path('batches/final_batch_persistence')
load=lambda f:json.loads((B/f).read_text())
plans=load('tile_plans.json');screens=load('screens.json');out=load('interactions.json')
gloss={b['context']['concept_id']:b for b in load('inputs/path_glossary_bundle.json')['bundles']}
counts={};ntests=0
for plan,tile in zip(plans['tiles'],out['tiles']):
 assert plan['tile_id']==tile['tile_id']
 expected=[s for s in plan['steps'] if s['type'] in ('check','hands_on')]
 assert [s['step_id'] for s in expected]==[s['step_id'] for s in tile['interactions']]
 screen=next(t for t in screens['tiles'] if t['tile_id']==tile['tile_id'])
 seen=set();previous=-1
 for step,item in zip(expected,tile['interactions']):
  ix=item['interaction'];cid=step['concept_ids'][0];bundle=gloss[cid]
  counts[ix['type']]=counts.get(ix['type'],0)+1
  assert ix['type']==step['planned_interaction_type']
  assert ix['anchors']==step['anchors']
  difficulty=['intro','core','stretch'].index(ix['difficulty']);assert difficulty>=previous;previous=difficulty
  assert ix['grading_mode']=='client'
  assert 1<=len(ix['feedback']['hints'])<=2
  rem=next((r for r in screen.get('remediation_steps',[]) if cid in r['concept_ids']),None)
  if cid not in seen and rem: assert ix['feedback']['remediation_step_id']==rem['step_id']
  if 'remediation_step_id' in ix['feedback']:assert any(r['step_id']==ix['feedback']['remediation_step_id'] for r in screen.get('remediation_steps',[]))
  seen.add(cid)
  for measure in ix['measures']:
   anchor=next(a for a in bundle['assessment_anchors'] if a['capability']==measure['capability'])
   assert measure['fact_ids']==anchor['fact_ids']
   assert all('#' not in f for f in measure['fact_ids'])
  if ix['type']=='choice':
   correct=set(ix['grading']['correct_option_ids']);assert len(correct)==1
   options={o['option_id'] for o in ix['public']['options']};assert correct<=options
   assert options-correct==set(ix['grading']['option_feedback'])
   assert len({o['text'] for o in ix['public']['options']})==len(options)
  if ix['type']=='code_exercise':
   assert cid+'#practice' in ix['anchors']
   live=bundle['practice_anchor']['live_code']
   assert ix['public']['constraints']=={k:live[k] for k in ('allowed_syntax','blocked_syntax')}
   assert 'execution_provenance' not in ix['grading'] and 'hidden_checks' not in ix['grading']
   starter=ix['public']['workspace']['files'][0]['content'];solution=ix['grading']['solution_files'][0]['content']
   assert starter!=solution
   # The executed scaffold is supplied unchanged; all learner changes remain visible in the marked region.
   assert ast.literal_eval(ast.parse(starter).body[0].value)==ast.literal_eval(ast.parse(solution).body[0].value)
   ast.parse(solution);ast.parse(starter)
   for t in ix['grading']['tests']:
    assert 'expected' in t['spec'];ntests+=1
  if ix['type']=='classify':
   assert len(ix['public']['items'])==len(ix['grading']['assignments'])
   assert len(set(ix['grading']['assignments'].values()))>=3
   assert all(i.get('source',{}).get('row',{}).get('occurrence')==0 for i in ix['public']['items'])
assert len(out['tiles'])==len(plans['tiles'])
report={'tiles':len(out['tiles']),'interactions':sum(counts.values()),'by_type':counts,'code_tests':ntests,'automated_checklist':'PASS','manual_checklist':{'single_defensible_choices':'reviewed','distractors_explain_misconceptions':'reviewed','taught_before_tested':'stage gate verifies lineage','keys_and_outputs_script_derived':'reference engine outputs and numeric asset comparisons','practice_success':'reviewed including migration commands, independent persistence reads, concurrent per-request correlation, cache failure boundaries, and signal count/rate trap','untaught_syntax':'unchanged supplied scaffold separated; learner regions reviewed against verbatim constraints','starters_unsolved':'stage gate rejects already-passing starters','standalone_prompts':'self-contained; code exercises not standalone','exact_output_contracts':'prompts fix models, outcomes, ordering, keys, or required review phrases'}}
(B/'working/checklist.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
