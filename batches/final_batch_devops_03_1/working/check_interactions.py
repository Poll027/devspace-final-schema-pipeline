import json,re
from pathlib import Path
from collections import Counter
B=Path('batches/final_batch_aws_devops.region.03_1')
load=lambda name:json.loads((B/name).read_text())
p=load('tile_plans.json');o=load('interactions.json');sc=load('screens.json');g=load('inputs/path_glossary_bundle.json');r=load('scenario_asset_registry.json')
bs={x['context']['concept_id']:x for x in g['bundles']};assets={a['asset_id']:a for a in r['assets']}
counts=Counter()
for t in p['tiles']:
 out=next(x for x in o['tiles'] if x['tile_id']==t['tile_id']); screen=next(x for x in sc['tiles'] if x['tile_id']==t['tile_id'])
 planned={s['step_id']:s for s in t['steps'] if s['type'] in ('check','hands_on')}
 assert {x['step_id'] for x in out['interactions']}==set(planned)
 assert len(out['interactions'])==len(planned)
 rem={s['step_id']:s for s in screen.get('remediation_steps',[])}
 for v in out['interactions']:
  ix=v['interaction'];s=planned[v['step_id']];counts[ix['type']]+=1
  assert ix['type']==s['planned_interaction_type'] and ix['anchors']==s['anchors']
  assert ix['grading_mode']=='client'
  assert len(ix['feedback']['hints']) in (1,2)
  if 'remediation_step_id' in ix['feedback']:assert ix['feedback']['remediation_step_id'] in rem
  for m in ix['measures']:
   cap=next(a for a in bs[m['concept_id']]['assessment_anchors'] if a['capability']==m['capability'])
   assert m['fact_ids']==cap['fact_ids'] and all('#' not in f for f in m['fact_ids'])
  if s['type']=='hands_on':
   assert any(a.endswith('#practice') for a in ix['anchors'])
  if ix['type']=='choice':
   assert len(ix['grading']['correct_option_ids'])==1
   assert set(ix['grading']['option_feedback'])=={v['option_id'] for v in ix['public']['options']}
  elif ix['type']=='classify':
   assert 'asset_ref' not in ix['public'] and 'runtime' not in ix['public']
   assert set(ix['grading']['assignments'])=={v['item_id'] for v in ix['public']['items']}
   assert len(set(ix['grading']['assignments'].values()))>=2 # all sets include a trap
   for it in ix['public']['items']:
    if 'source' in it:
     src=it['source'];a=assets[src['asset_id']];cols=[c['name'] for c in a['columns']];rows=[dict(zip(cols,r)) for r in a['rows']]
     selected=[row for row in rows if all(row[k]==val for k,val in src['row']['where'].items())][src['row']['occurrence']]
     assert selected[src['column']] in it['text'] # excerpt retains cited evidence verbatim
     assert ix['grading']['role_map'][ix['grading']['assignments'][it['item_id']]]==next(c['semantic_role'] for c in a['columns'] if c['name']==src['column'])
   assert not re.search(r'\b(workspace|README|ws\.)',ix['public']['prompt'],re.I)
  else:
   a=assets[ix['public']['asset_ref']['asset_id']];cols=[c['name'] for c in a['columns']];rows=[dict(zip(cols,r)) for r in a['rows']]
   for answer in ix['grading']['answers']:
    selected=[row for row in rows if all(row[k]==val for k,val in answer['row']['where'].items())]
    assert len(selected)==1
    if 'column' in answer:assert answer['expect_value']==selected[0][answer['column']]
  if ix['standalone']:assert 'table above' not in json.dumps(ix['public']).lower()
reports=load('reports/validation.tiles.json');assert all(not x['errors'] for x in reports)
summary={'tiles':len(o['tiles']),'interactions':sum(counts.values()),'types':dict(counts),'gate_errors':sum(len(x['errors']) for x in reports),'gate_warnings':sum(len(x['warnings']) for x in reports),'automated_checklist':'PASS','manual_review':['One defensible choice per prompt; alternatives contradict the fact under the stated context.','Wrong options and all classification traps include fact-grounded explanations.','Hands-on excerpts judged against every named practice success criterion; no execution requested.','Registry-based excerpt text, row predicates and expected cells derived in script.','Inline cloud evidence is authored inspect-and-judge material, not an executed runtime or invented credential/hash value.','SQL/Python starter, syntax and expected-output checks are not applicable: no code exercises planned.','Remaining gate warnings are existing screen prose lineage warnings; screens were not edited.']}
(B/'working/interactions_checklist.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
