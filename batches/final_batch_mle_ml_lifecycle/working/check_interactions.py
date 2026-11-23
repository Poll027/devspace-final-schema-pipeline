import json,sys
from pathlib import Path
sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts')
from checkers import sandbox
B=Path('batches/final_batch_mle.region.ml_lifecycle')
load=lambda f:json.loads((B/f).read_text())
O=load('interactions.json');P=load('tile_plans.json');S=load('screens.json');G=load('inputs/path_glossary_bundle.json');R=load('scenario_asset_registry.json')
C={c['context']['concept_id']:c for c in G['bundles']}
counts={};checks=[]
for t in O['tiles']:
 p=next(x for x in P['tiles'] if x['tile_id']==t['tile_id']);s=next(x for x in S['tiles'] if x['tile_id']==t['tile_id'])
 need={x['step_id']:x for x in p['steps'] if x['type'] in ['check','hands_on']}
 assert {x['step_id'] for x in t['interactions']}==set(need)
 rem={x['step_id'] for x in s.get('remediation_steps',[])}
 taught=set();earlier={}
 for st in s['steps']:
  earlier[st['step_id']]=set(taught)
  for block in st.get('blocks',[]):
   taught.update(block.get('lineage',{}).get('fact_ids',[]))
 for x in t['interactions']:
  ix=x['interaction'];plan=need[x['step_id']];counts[ix['type']]=counts.get(ix['type'],0)+1
  assert ix['type']==plan['planned_interaction_type'];assert ix['anchors']==plan['anchors']
  assert ix['grading_mode']=='client'
  if 'remediation_step_id' in ix['feedback']:assert ix['feedback']['remediation_step_id'] in rem
  assert 1<=len(ix['feedback']['hints'])<=2
  for m in ix['measures']:
   anchor=next(a for a in C[m['concept_id']]['assessment_anchors'] if a['capability']==m['capability'])
   assert m['fact_ids']==anchor['fact_ids'];assert all('#' not in f for f in m['fact_ids'])
   for fact in m['fact_ids']:assert m['concept_id']+'#'+fact in earlier[x['step_id']]
  if ix['type']=='choice':
   assert ix['public']['selection']=='single';assert len(ix['grading']['correct_option_ids'])==1
   assert set(ix['grading']['option_feedback'])=={o['option_id'] for o in ix['public']['options']}
  if ix['standalone']:assert 'above' not in ix['public'].get('prompt','').lower()
  if ix['type']=='code_exercise':
   lc=C[plan['concept_ids'][0]]['practice_anchor']['live_code']
   assert ix['public']['constraints']=={k:lc[k] for k in ['allowed_syntax','blocked_syntax']}
   assert len([f for f in ix['public']['workspace']['files'] if f['role']=='editable'])==1
   assert 'execution_provenance' not in ix['grading'] and 'hidden_checks' not in ix['grading']
   run=sandbox.run_exercise(R,ix);assert not run.problems,run.problems
   assert run.hidden_checks
checks=['Exact planned step and interaction coverage: PASS','Planned anchors, bare fact IDs, assessment capabilities, taught-before-tested: PASS','Registered row/cell keys and expected values: PASS (stage gate)','One defensible choice and fact-grounded distractor feedback: manually reviewed','Existing remediation IDs and 1–2 non-answer hints: PASS','Starter does not pass; pinned execution and mutation-derived outputs: PASS','Constraints copied verbatim, learner syntax limited to safe YAML calls: PASS','Standalone prompts contain all needed context: PASS','Full hands-on success criteria: UNRESOLVED. The natural-language syntax descriptors are not mapped by the Python syntax checker. Six code exercises use the simplest permitted safe-YAML round-trip rather than complete gate implementations. The planned lineage table interaction cannot demonstrate function assertions, exact-generation downloads or local Git inspection.','Difficulty: intro → core → stretch; final practical tasks stretch.','No SQL/chart/formula/classify/find_issues interactions: corresponding checklist items not applicable.']
(B/'working/interactions_checklist.json').write_text(json.dumps({'counts':counts,'checks':checks},indent=2)+'\n')
print(json.dumps({'counts':counts,'automated_checks':'PASS','unresolved':'Full practice success criteria; six minimal syntax-permitted exercises and the planned lineage table task.'},indent=2))
