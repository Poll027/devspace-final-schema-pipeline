import json,re,ast
from pathlib import Path
B=Path(__file__).parent
S=json.loads((B/'screens.json').read_text());P=json.loads((B/'tile_plans.json').read_text());G=json.loads((B/'inputs/path_glossary_bundle.json').read_text());R=json.loads((B/'scenario_asset_registry.json').read_text())
bundles={b['context']['concept_id']:b for b in G['bundles']};assets={a['asset_id']:a for a in R['assets']}
facts={c+'#'+f['id'] for c,b in bundles.items() for f in b['coverage']['required_facts']}
tbs={c+'#'+t['id'] for c,b in bundles.items() for t in b['teaching_blocks']}

def walk(block):
 yield block
 for field in ('left','right','before','after'):
  if field in block:yield from walk(block[field])

def check_block(block):
 assert not any(k in block for k in ['output','result','computed_values','execution_provenance','rows']),block
 if block['type']=='media_group':
  assert set(block)<= {'type','block_id','segment_ids'}
  return
 if block['type']=='up_next':return
 assert 'lineage' in block
 lin=block['lineage']
 assert set(lin['fact_ids'])<=facts
 assert set(lin['teaching_block_ids'])<=tbs
 assert all('#' in x for x in lin['fact_ids']+lin['teaching_block_ids'])
 if block['type']=='prose':
  assert len(block['text'].split())<=90
  assert not re.search(r'\bvideo\b',block['text'],re.I)
  for c in lin['concept_ids']:
   for future in bundles[c]['context']['blocked_future_concepts']:
    name=G['names'].get(future,'')
    assert not (name and name.lower() in block['text'].lower())
 if 'asset_ref' in block:
  ref=block['asset_ref'];a=assets[ref['asset_id']]
  assert set(ref.get('columns',[]))<={x['name'] for x in a.get('columns',[])}
 if block['type']=='code_walkthrough':
  parsed=ast.parse(block['code'])
  c=lin['concept_ids'][0]
  workspace=assets['ws.'+c.split('.',1)[1]]
  fixture=json.loads(next(f['content'] for f in workspace['files'] if f['path']=='fixtures.json'))
  for node in ast.walk(parsed):
   if isinstance(node,ast.Subscript) and isinstance(node.value,ast.Name) and node.value.id=='F' and isinstance(node.slice,ast.Constant):
    assert node.slice.value in fixture,(c,node.slice.value)

assert S['kind']=='screens_part'
assert [t['tile_id'] for t in S['tiles']]==[t['tile_id'] for t in P['tiles']]
for tile,plan in zip(S['tiles'],P['tiles']):
 assert len(tile['steps'])==len(plan['steps'])
 taught=set()
 visual=set()
 for st,ps in zip(tile['steps'],plan['steps']):
  assert all(st[k]==ps[k] for k in ['step_id','type','concept_ids'])
  assert all(st['lineage'][k]==ps[k] for k in ['teaching_block_ids','fact_ids'])
  if st['type'] in ['check','hands_on']:
   assert not any(k in st for k in ['blocks','interaction'])
   assert set(ps['fact_ids'])<=taught
  else:
   blocks=[x for b in st['blocks'] for x in walk(b)]
   for block in blocks:check_block(block)
   count=sum(len(re.findall(r'\w+',x.get('text',''))) for x in blocks)
   assert count<=ps['word_budget'],(st['step_id'],count,ps['word_budget'])
   for x in blocks:
    if x['type']=='prose':taught.update(x['lineage']['fact_ids'])
    visual.update(x.get('lineage',{}).get('anchors',[]))
   kind=ps['planned_visual_block_type']
   if kind: assert kind in [x['type'] for x in blocks],(st['step_id'],kind)
   if st['type']=='video':assert st['blocks'][0]['segment_ids']==ps['segment_ids']
 for c in plan['concept_ids']:
  assert {c+'#'+f['id'] for f in bundles[c]['coverage']['required_facts']}<=taught
  assert c+'#visual' in visual
 for st in tile['remediation_steps']:
  assert st['type']=='remediation'
  for b in st['blocks']:
   for block in walk(b):check_block(block)
 for ps in plan['steps']:
  if ps['type'] in ['check','hands_on']:
   assert any(st['concept_ids']==ps['concept_ids'] and st['lineage']['fact_ids']==ps['fact_ids'] for st in tile['remediation_steps'])
report={'artifact':str(B/'screens.json'),'tiles':len(S['tiles']), 'planned_steps':sum(len(t['steps']) for t in S['tiles']), 'remediation_steps':sum(len(t['remediation_steps']) for t in S['tiles']), 'mistakes_to_avoid':{'qualified_lineage':'PASS','all_prose_has_lineage':'PASS','no_video_mentions':'PASS','registered_assets_and_fixture_keys':'PASS','word_budgets':'PASS','fact_coverage_and_prior_teaching':'PASS','no_unregistered_columns':'PASS','visual_anchor_tags':'PASS','no_authored_computed_outputs':'PASS','plan_identity_types_order':'PASS','distinct_measured_fact_remediations':'PASS'}, 'interactions_exist':(B/'interactions.json').exists()}
(B/'screens_checklist.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
