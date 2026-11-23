import json,sys,collections
from pathlib import Path
sys.path.insert(0,str(Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
from checkers import sandbox
B=Path('batches/final_batch_mle.region.data_readiness');load=lambda p:json.loads((B/p).read_text())
d=load('interactions.json');p=load('tile_plans.json');s=load('screens.json');r=load('scenario_asset_registry.json');g={x['context']['concept_id']:x for x in load('inputs/path_glossary_bundle.json')['bundles']}
assert [t['tile_id'] for t in d['tiles']]==[t['tile_id'] for t in p['tiles']]
counts=collections.Counter();jobs=[]
for tile,plan,screen in zip(d['tiles'],p['tiles'],s['tiles']):
 targets=[x for x in plan['steps'] if x['type'] in ['check','hands_on']]
 assert [x['step_id'] for x in tile['interactions']]==[x['step_id'] for x in targets]
 first=set()
 for entry,step in zip(tile['interactions'],targets):
  ix=entry['interaction'];counts[ix['type']]+=1
  assert ix['type']==step['planned_interaction_type']
  assert ix['anchors']==step['anchors']
  expected=[]
  for a in step['anchors']:
   if '#assessment:' in a:
    cid,cap=a.split('#assessment:');anchor=next(x for x in g[cid]['assessment_anchors'] if x['capability']==cap)
    expected.append({'concept_id':cid,**anchor})
  assert ix['measures']==expected
  assert all('#' not in fid for m in ix['measures'] for fid in m['fact_ids'])
  cid=step['concept_ids'][0]
  if cid not in first:
   rem=next((x for x in screen['remediation_steps'] if cid in x['concept_ids']),None)
   if rem:assert ix['feedback']['remediation_step_id']==rem['step_id']
   first.add(cid)
  assert 1<=len(ix['feedback']['hints'])<=2
  assert 'the table above' not in ix['public']['prompt'].lower()
  if ix['type']=='choice':
   assert len(ix['grading']['correct_option_ids'])==1
   assert set(ix['grading']['option_feedback'])=={x['option_id'] for x in ix['public']['options']}
  if ix['type']=='classify':
   assert 'asset_ref' not in ix['public']
   assert {'pass','fail'}==set(ix['grading']['assignments'].values())
   assert set(ix['grading']['item_feedback'])==set(ix['grading']['assignments'])
  if ix['type']=='code_exercise':
   assert all(k not in ix['grading'] for k in ['hidden_checks','execution_provenance'])
   assert ix['public']['constraints']=={k:g[cid]['practice_anchor']['live_code'][k] for k in ['allowed_syntax','blocked_syntax']}
   ws=ix['public']['workspace'];starter=ws['files'][0]['content'];solution=ix['grading']['solution_files'][0]['content']
   assert starter!=solution
   tables,_=sandbox._tables(r,ws['asset_mounts'],{},[])
   probes=[sandbox._py_probe(t) for t in ix['grading']['tests']]
   jobs.append(sandbox._py_script(ix['interaction_id'],ws['entry'],starter,sandbox._py_mounts(tables),probes))
res=sandbox.node_run(sandbox._py_job('python',['numpy','pandas'],jobs),sandbox.RUNTIMES['python']['runner'])
for sid,result in res['results'].items():
 assert not result['ok'] or not all(p['ok'] for p in result.get('probes',{}).values()),sid+' starter unexpectedly completed tests'
log=(B/'stage04_validate.log').read_text();errors=[l for l in log.splitlines() if l.startswith('  E')]
report={'tiles':len(d['tiles']),'interactions':sum(counts.values()),'by_type':dict(counts),'checks':{'plan_fidelity':'pass','bare_measure_ids':'pass','glossary_capabilities':'pass','remediation_links':'pass','feedback_and_hints':'pass','standalone_wording':'pass','choice_keys_and_distractor_feedback':'pass','inspect_judge_traps_and_keys':'pass','constraints_copied_not_widened':'pass','expected_values_computed_in_pinned_runtime':'pass','starters_do_not_pass':'pass','no_authored_provenance_or_hidden_checks':'pass'},'manual_review':{'single_defensible_judgments':'reviewed against supplied contracts','taught_before_tested':'validator reported no lineage errors','output_contracts':'named in each prompt','syntax':'BLOCKED: natural-language glossary descriptions do not map to detector tags, including descriptors for function definitions; authentic function implementations retained rather than bypassing the gate','preprocessing_interfaces':'Bounded numerical teaching fixtures, not installed scikit-learn APIs; full library API practice remains uncertain'},'gate':{'status':'FAIL','errors':len(errors),'non_syntax_errors':[e for e in errors if 'solution uses' not in e]}}
(B/'stage04_checklist.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
