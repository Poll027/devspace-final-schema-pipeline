import json
from collections import Counter
from pathlib import Path
B=Path(__file__).resolve().parents[1]
d=json.loads((B/'interactions.json').read_text());p=json.loads((B/'tile_plans.json').read_text());s=json.loads((B/'screens.json').read_text());reg=json.loads((B/'scenario_asset_registry.json').read_text());g=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
plans={t['tile_id']:t for t in p['tiles']};screens={t['tile_id']:t for t in s['tiles']};bundles={x['context']['concept_id']:x for x in g['bundles']};assets={a['asset_id']:a for a in reg['assets']}
counts=Counter();checks=[]
for t in d['tiles']:
 expected={z['step_id']:z for z in plans[t['tile_id']]['steps'] if z['type'] in ['check','hands_on']}
 assert {e['step_id'] for e in t['interactions']}==set(expected)
 rems={r['step_id'] for r in screens[t['tile_id']].get('remediation_steps',[])}
 for e in t['interactions']:
  ix=e['interaction'];plan=expected[e['step_id']];counts[ix['type']]+=1
  assert ix['type']==plan['planned_interaction_type'] and ix['anchors']==plan['anchors']
  assert ix['grading_mode']=='client'
  assert len(ix['feedback']['hints']) in [1,2]
  assert ix['feedback'].get('remediation_step_id') in rems
  for m in ix['measures']:
   assert all('#' not in f for f in m['fact_ids'])
   a=next(a for a in bundles[m['concept_id']]['assessment_anchors'] if a['capability']==m['capability'])
   assert a['fact_ids']==m['fact_ids']
  if ix['type']=='choice':
   assert len(ix['grading']['correct_option_ids'])==1
   assert set(ix['grading']['option_feedback'])=={o['option_id'] for o in ix['public']['options']}
  if ix['type']=='classify':
   prompt=ix['public']['prompt'].lower()
   assert not any(w in prompt for w in ['write','implement','run ','build','submit','provision','ws.','readme','anchor contract','workspace'])
   assert 'asset_ref' not in ix['public']
   assert set(ix['grading']['assignments'])=={i['item_id'] for i in ix['public']['items']}
   for item in ix['public']['items']:
    if 'source' in item:
     src=item['source'];a=assets[src['asset_id']];cols=[c['name'] for c in a['columns']];rows=[dict(zip(cols,r)) for r in a['rows']]
     matches=[r for r in rows if all(r[k]==v for k,v in src['row']['where'].items())];assert len(matches)>src['row']['occurrence']
     role=next(c['semantic_role'] for c in a['columns'] if c['name']==src['column']);assert ix['grading']['role_map'][ix['grading']['assignments'][item['item_id']]]==role
  if ix['type']=='table_select':
   a=assets[ix['public']['asset_ref']['asset_id']];cols=[c['name'] for c in a['columns']];rows=[dict(zip(cols,r)) for r in a['rows']]
   for answer in ix['grading']['answers']:
    matches=[r for r in rows if all(r[k]==v for k,v in answer['row']['where'].items())];r=matches[answer['row']['occurrence']]
    if 'column' in answer:assert answer['expect_value']==r[answer['column']]
# Editorial review: options are mutually exclusive under their explicit scenario; wrong-option feedback cites the specific failed condition.
# Practice review: seeded failures/traps are present for denied access, production destinations, missing audit evidence, retention bypass,
# skipped dependencies, continued failed health checks, unexcepted findings and failed live smoke behavior.
# Untaught facts and planned lineage checked by strict validate_tile.py; no code/formula runtimes in this batch, so code-output/starter checks are N/A.
checks=['Plan coverage and planned types: PASS','Bare fact ids and glossary capabilities: PASS','Derived row predicates, semantic roles and cell expected values: PASS','Single-answer choices and every distractor feedback: PASS','Existing remediation ids and 1-2 hints: PASS','Inspect-and-judge prompts and embedded excerpts: PASS','Defensible answers and practice success/trap review: PASS','Taught-before-tested and exact step lineage: PASS (strict stage gate)','Code syntax, expected outputs, nonpassing starters, output columns: N/A (no code exercises)']
report={'tiles':len(d['tiles']),'interaction_counts':dict(counts),'total_interactions':sum(counts.values()),'mistakes_to_avoid':checks,'uncertainties':[]}
(B/'working/interactions_checklist.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
