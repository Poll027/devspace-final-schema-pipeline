import json, collections
from pathlib import Path
b=Path('batches/final_batch_learn_python.region.05')
i=json.load(open(b/'interactions.json'));p=json.load(open(b/'tile_plans.json'));s=json.load(open(b/'screens.json'))
g={x['context']['concept_id']:x for x in json.load(open(b/'inputs/path_glossary_bundle.json'))['bundles']}
assert [x['tile_id'] for x in i['tiles']]==[x['tile_id'] for x in p['tiles']]
counts=collections.Counter(); tests=0
for tile,plan,screen in zip(i['tiles'],p['tiles'],s['tiles']):
 steps=[x for x in plan['steps'] if x['type'] in ('check','hands_on')]
 assert [x['step_id'] for x in tile['interactions']]==[x['step_id'] for x in steps]
 rem={x['step_id'] for x in screen['remediation_steps']};seen=set();rank=[]
 for ent,step in zip(tile['interactions'],steps):
  x=ent['interaction'];counts[x['type']]+=1
  assert x['type']==step['planned_interaction_type'];assert x['anchors']==step['anchors']
  assert x['grading_mode']=='client';rank.append({'intro':0,'core':1,'stretch':2}[x['difficulty']])
  for m in x['measures']:
   a=next(a for a in g[m['concept_id']]['assessment_anchors'] if a['capability']==m['capability'])
   assert m['fact_ids']==a['fact_ids'] and all('#' not in f for f in m['fact_ids'])
  for anchor in step['anchors']:
   if '#assessment:' in anchor:
    cid,cap=anchor.split('#assessment:');assert any(m['concept_id']==cid and m['capability']==cap for m in x['measures'])
  f=x['feedback'];assert f['correct']['message'] and f['incorrect']['message'] and 1<=len(f['hints'])<=2
  if 'remediation_step_id' in f: assert f['remediation_step_id'] in rem
  for cid in step['concept_ids']:
   if cid not in seen and any(cid in r['concept_ids'] for r in screen['remediation_steps']): assert 'remediation_step_id' in f
   seen.add(cid)
  if x['standalone']: assert 'table above' not in x['public']['prompt'].lower()
  if x['type']=='choice':
   ids={o['option_id'] for o in x['public']['options']}; assert len(x['grading']['correct_option_ids'])==1
   assert set(x['grading']['option_feedback'])==ids
  elif x['type']=='classify':
   ids={e['item_id'] for e in x['public']['items']};assert set(x['grading']['assignments'])==ids
   assert set(x['grading']['assignments'].values())=={'meets','fails'}
   assert all('source' not in e for e in x['public']['items']) # 9e: excerpts, not registry rows
  else:
   cid=step['concept_ids'][0];live=g[cid]['practice_anchor']['live_code']
   assert x['public']['constraints']=={k:live[k] for k in ('allowed_syntax','blocked_syntax')}
   assert len(x['public']['workspace']['files'])==1 and x['public']['workspace']['files'][0]['role']=='editable'
   assert x['grading']['solution_files'][0]['path']==x['public']['workspace']['entry']
   assert x['grading']['solution_files'][0]['content']!=x['public']['workspace']['files'][0]['content']
   assert 'hidden_checks' not in x['grading'] and 'execution_provenance' not in x['grading']
   assert all('expected' in t['spec'] for t in x['grading']['tests']);tests+=len(x['grading']['tests'])
 assert rank==sorted(rank)
results=json.load(open(b/'working/interaction_gate.json'));assert len(results)==len(i['tiles']) and all(r['status']=='PASS' and not r['errors'] for r in results)
report={'tiles':len(i['tiles']),'interactions':sum(counts.values()),'counts':dict(counts),'python_tests':tests,'gate_errors':0,'gate_warnings':sum(len(r['warnings']) for r in results),'checklist':{'plan_fidelity_and_bare_fact_ids':'PASS','keys_and_expected_values_derived':'PASS: Python expected values from pinned runner; excerpt keys from explicitly stated criteria','single_defensible_answer_and_misconceptions':'REVIEWED: each wrong alternative has fact-grounded feedback','teaching_order_and_anchor_capabilities':'PASS: plan anchors plus stage gate; no extra tested capabilities','practice_success':'REVIEWED: actual dates/deltas, extracted sibling and package helper, captured INFO-only events, import/direct boundary, three argparse invocations, real stdlib resolution after rename, configured/absent/empty environment cases, reproducible bounded draws, whole-label validation; transcripts include success and failure evidence','standalone_prompts_and_classification_traps':'PASS','syntax_and_starter_not_solution':'PASS: immutable constraints; small permitted edits over supplied fixed skeletons; gate checks execution, starter failure and data sensitivity','output_contracts':'REVIEWED: print order and tested variables stated in prompts'},'uncertainties':['Several syntax descriptors are not mapped by the strict checker. Kept lists verbatim and narrowed exercises to permitted small edits over fixed skeletons.','Dependency transcripts use the glossary symbolic package_name/module_name/version: the scenario registry supplies no concrete dependency documentation.']}
(b/'working/interaction_checklist.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
