import json, collections, re
from pathlib import Path
B=Path(__file__).parent
ix=json.loads((B/'interactions.json').read_text());p=json.loads((B/'tile_plans.json').read_text());sc=json.loads((B/'screens.json').read_text());gl=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
g={b['context']['concept_id']:b for b in gl['bundles']}
counts=collections.Counter();items=0
assert [t['tile_id'] for t in ix['tiles']]==[t['tile_id'] for t in p['tiles']]
for tile,pt,st in zip(ix['tiles'],p['tiles'],sc['tiles']):
 planned=[s for s in pt['steps'] if s['type'] in ('check','hands_on')]
 assert [i['step_id'] for i in tile['interactions']]==[s['step_id'] for s in planned]
 authored={s['step_id']:s for s in st['steps']}
 taught=set();before={}
 def text_facts(block):
  if block.get('type') in ('prose','callout','comparison','side_by_side','before_after','code_walkthrough','diagram','process_flow','data_table'):
   return set(block.get('lineage',{}).get('fact_ids',[]))
  return set()
 for step in pt['steps']:
  before[step['step_id']]=set(taught)
  if step['type']=='explainer':
   for block in authored[step['step_id']].get('blocks',[]):taught |= text_facts(block)
 remids={s['step_id'] for s in st['remediation_steps']}
 seen=set()
 for rec,step in zip(tile['interactions'],planned):
  x=rec['interaction'];counts[x['type']]+=1
  assert x['type']==step['planned_interaction_type']
  assert x['grading_mode']=='client' and x['anchors']==step['anchors']
  expected=[a for a in step['anchors'] if '#assessment:' in a]
  assert [m['concept_id']+'#assessment:'+m['capability'] for m in x['measures']]==expected
  for m in x['measures']:
   a=next(a for a in g[m['concept_id']]['assessment_anchors'] if a['capability']==m['capability'])
   assert m['fact_ids']==a['fact_ids']
   assert all('#' not in f for f in m['fact_ids'])
   assert {m['concept_id']+'#'+f for f in m['fact_ids']} <= before[step['step_id']]
  assert 1<=len(x['feedback']['hints'])<=2
  assert x['feedback']['correct']['message'] and x['feedback']['incorrect']['message']
  r=x['feedback'].get('remediation_step_id')
  if r:assert r in remids
  cid=step['concept_ids'][0]
  if cid not in seen and any(cid in r['concept_ids'] for r in st['remediation_steps']):assert r
  seen.add(cid)
  prompt=x['public']['prompt'].lower()
  assert not any(s in prompt for s in ('the table above','as the video shows','readme','anchor contract','registered files'))
  assert not re.search(r'\bws\.',prompt)
  if x['type']=='choice':
   options={o['option_id']:o for o in x['public']['options']}
   assert len(x['grading']['correct_option_ids'])==1
   assert set(x['grading']['correct_option_ids'])<=set(options)
   assert set(x['grading']['option_feedback'])==set(options)
   assert len({o['text'] for o in options.values()})==len(options)
  else:
   assert step['type']=='hands_on' and cid+'#practice' in x['anchors']
   assert 'read' in prompt and ('judge' in prompt or 'decide' in prompt)
   assert 'asset_ref' not in x['public'] and 'runtime' not in x['public']
   its={i['item_id']:i for i in x['public']['items']};items+=len(its)
   assert set(x['grading']['assignments'])==set(its)==set(x['grading']['item_feedback'])
   assert set(x['grading']['assignments'].values())=={'meets','violates'}
   # These are excerpt judgements, not registry-column role classifications.
   assert all('source' not in i and len(i['text'])>40 for i in its.values())
result={'artifact':'interactions.json','tiles':len(ix['tiles']),'interaction_counts':dict(counts),'total_interactions':sum(counts.values()),'classify_items':items,'automated_checks':'PASS','manual_mistakes_to_avoid_review':{
 'keys_derived_not_transcribed':'Choice and classification keys follow authored truth predicates; registry trial selection/costs and numeric references are computed by stage04_generate.py.',
 'one_defensible_answer_and_wrong_option_feedback':'Reviewed all 18 choices; single selected answer and explanation on every option. Explicit task contracts disambiguate shape, sign, cohort and timing scope.',
 'taught_before_tested':'Glossary assessment facts checked against earlier text-bearing screen blocks and by the deterministic gate.',
 'practice_success_and_traps':'Reviewed all 17 inspect-and-judge sets against glossary success sentences: full compliant procedure/evidence plus concrete failure or boundary traps. ViT includes rate and expected-cost calculation traps; head gradient layout is explicit.',
 'inspect_exception':'Inline excerpts contain evidence to judge. No runtime, external artifact request or asset_ref. Registry tables are rendered inside the prompt as context, not classified as column semantic roles.',
 'standalone':'All needed contracts, excerpts and numeric context appear in each interaction. No dependence on an unstated table above.',
 'live_code_only_mistakes':'Not applicable: plan contains no code_exercise. There are no execution_provenance, hidden_checks, starter, constraints or expected runtime tests to author.'}}
(B/'stage04_self_check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
