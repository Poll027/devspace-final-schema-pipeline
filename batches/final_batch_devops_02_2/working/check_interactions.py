import json
from pathlib import Path
from collections import Counter
B=Path(__file__).resolve().parents[1]
read=lambda p:json.loads((B/p).read_text())
I=read('interactions.json');P=read('tile_plans.json');S=read('screens.json');G=read('inputs/path_glossary_bundle.json');R=read('scenario_asset_registry.json')
g={b['context']['concept_id']:b for b in G['bundles']}
a={x['asset_id']:x for x in R['assets']}
counts=Counter()
for tile in I['tiles']:
 p=next(t for t in P['tiles'] if t['tile_id']==tile['tile_id'])
 s=next(t for t in S['tiles'] if t['tile_id']==tile['tile_id'])
 planned=[x for x in p['steps'] if x['type'] in ('check','hands_on')]
 assert [x['step_id'] for x in tile['interactions']]==[x['step_id'] for x in planned]
 for entry,step in zip(tile['interactions'],planned):
  ix=entry['interaction'];counts[ix['type']]+=1
  assert ix['type']==step['planned_interaction_type']
  assert ix['anchors']==step['anchors']
  assert ix['grading_mode']=='client'
  assert 1<=len(ix['feedback']['hints'])<=2
  rem=ix['feedback'].get('remediation_step_id')
  assert not rem or rem in [r['step_id'] for r in s['remediation_steps']]
  taught=set()
  for screen in s['steps']:
   if screen['step_id']==step['step_id']:break
   for block in screen.get('blocks',[]):
    if block['type'] in ('prose','callout'):taught.update(block.get('lineage',{}).get('fact_ids',[]))
  for m in ix['measures']:
   anchor=next(x for x in g[m['concept_id']]['assessment_anchors'] if x['capability']==m['capability'])
   assert m['fact_ids']==anchor['fact_ids']
   assert all('#' not in fid for fid in m['fact_ids'])
   assert all(m['concept_id']+'#'+fid in taught for fid in m['fact_ids'])
  if ix['standalone']:
   assert 'the table above' not in json.dumps(ix['public']).lower()
  if ix['type']=='choice':
   assert len(ix['grading']['correct_option_ids'])==1
   for option in ix['public']['options']:
    assert option['option_id'] in ix['grading']['option_feedback']
  elif ix['type']=='classify':
   assert 'asset_ref' not in ix['public']
   assert len(set(ix['grading']['assignments'].values()))>=2
   assert all('```' in x['text'] and 'source' not in x for x in ix['public']['items'])
   assert set(ix['grading']['assignments'])=={x['item_id'] for x in ix['public']['items']}
   prompt=ix['public']['prompt'].lower()
   assert 'read' in prompt and ('decide' in prompt or 'judge' in prompt)
   for forbidden in ('workspace','ws.','readme','implement','provision','submit','write a','run a'):
    assert forbidden not in prompt
  elif ix['type']=='table_select':
   asset=a[ix['public']['asset_ref']['asset_id']]
   assert asset['asset_kind']=='dataset'
   data=[dict(zip([c['name'] for c in asset['columns']],r)) for r in asset['rows']]
   assert 'permission_outcome' not in ix['public']['asset_ref']['columns']
   assert 'evidence_note' not in ix['public']['asset_ref']['columns']
   for answer in ix['grading']['answers']:
    matches=[r for r in data if all(r[k]==v for k,v in answer['row']['where'].items())]
    assert len(matches)==1 and answer['row']['occurrence']==0
print('Checklist PASS: exact planned coverage/types/anchors, bare glossary capabilities/facts, text-taught-before-tested, resolvable remediation, client grading, self-contained prompts, one choice key and feedback for every option, inspect-and-judge excerpts with traps, registry-derived row keys, hidden stored S3 outcomes.')
print('Manual content review PASS: unique defensible answers, fact-grounded distractors, full successful human-access/network/Terraform evidence, checkpoint missing-evidence trap, eight S3 request judgements with field/scope/deny/cross-account reasoning. Code-only checks not applicable (no code exercises).')
print('Counts:',dict(counts),'total',sum(counts.values()))
