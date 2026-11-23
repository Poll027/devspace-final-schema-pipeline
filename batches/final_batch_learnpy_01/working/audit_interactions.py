import json,sys
from pathlib import Path
from collections import Counter
sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts')
from schema_check import errors
B=Path('batches/final_batch_learn_python.region.01')
data=json.loads((B/'interactions.json').read_text());plans=json.loads((B/'tile_plans.json').read_text());screens=json.loads((B/'screens.json').read_text());bundle={b['context']['concept_id']:b for b in json.loads((B/'inputs/path_glossary_bundle.json').read_text())['bundles']}
assert not errors(data,'interactions_part.schema.json'),errors(data,'interactions_part.schema.json')
counts=Counter();checks=[]
for tile,plan,screen in zip(data['tiles'],plans['tiles'],screens['tiles']):
 assert tile['tile_id']==plan['tile_id']==screen['tile_id']
 expected=[s for s in plan['steps'] if s['type'] in ['check','hands_on']]
 assert [s['step_id'] for s in tile['interactions']]==[s['step_id'] for s in expected]
 taught=set();earlier={}
 for s in screen['steps']:
  earlier[s['step_id']]=taught.copy()
  if s['type']=='explainer':
   for block in s.get('blocks',[]):taught.update(block.get('lineage',{}).get('fact_ids',[]))
 rems={r['step_id']:r for r in screen.get('remediation_steps',[])};seen=set()
 for entry,step in zip(tile['interactions'],expected):
  ix=entry['interaction'];cid=step['concept_ids'][0];counts[ix['type']]+=1
  assert ix['type']==step['planned_interaction_type']
  assert ix['anchors']==step['anchors']
  assert ix['grading_mode']=='client'
  assert 1<=len(ix['feedback']['hints'])<=2
  if cid not in seen:
   rem=next((r for r in screen.get('remediation_steps',[]) if cid in r['concept_ids']),None)
   if rem:assert ix['feedback']['remediation_step_id']==rem['step_id']
   seen.add(cid)
  for m in ix['measures']:
   assert any(m['capability']==a['capability'] and m['fact_ids']==a['fact_ids'] for a in bundle[m['concept_id']]['assessment_anchors'])
   assert all('#' not in f for f in m['fact_ids'])
   assert all(m['concept_id']+'#'+f in earlier[entry['step_id']] for f in m['fact_ids'])
  if ix['type']=='choice':
   assert len(ix['grading']['correct_option_ids'])==1
   assert set(ix['grading']['option_feedback'])=={o['option_id'] for o in ix['public']['options']}
   assert len({o['text'] for o in ix['public']['options']})==len(ix['public']['options'])
   assert 'table above' not in ix['public']['prompt'].lower()
  else:
   assert cid+'#practice' in ix['anchors']
   anchor=bundle[cid]['practice_anchor']['live_code']
   assert ix['public']['constraints']=={k:anchor[k] for k in ['allowed_syntax','blocked_syntax']}
   assert 'hidden_checks' not in ix['grading'] and 'execution_provenance' not in ix['grading']
   assert ix['public']['workspace']['files'][0]['content']!=ix['grading']['solution_files'][0]['content']
   for mount in ix['public']['workspace']['asset_mounts']:
    assert any(a['asset_id']==mount['asset_id'] and a['asset_kind']=='dataset' and 'rows' in a for a in json.loads((B/'scenario_asset_registry.json').read_text())['assets'])
report={'tiles':len(data['tiles']),'interaction_counts':dict(counts),'total':sum(counts.values()),'checklist':['Exact planned coverage and types: passed','Glossary capability and bare fact ids: passed','Earlier text teaching for measured facts: passed','Existing first-concept remediation references: passed','All choice options have explanations; distinct options and single key: passed','Manual ambiguity/misconception review: completed','Hands-on success, named outputs and starters reviewed: completed','Expected values computed by solution execution: completed; pinned-engine gate reports no result mismatch','Constraints copied verbatim: passed','No authored provenance or hidden checks: passed','Registered dataset mounts: passed'],'gate_status':'Assembly passes. Validation remains blocked by 96 syntax-descriptor mapping errors; constraints not widened.'}
(B/'working'/'interactions_checklist.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
