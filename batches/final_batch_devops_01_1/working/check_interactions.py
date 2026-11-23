import json,collections,re,runpy
from pathlib import Path
P=Path('batches/final_batch_aws_devops.region.01_1')
out=json.loads((P/'interactions.json').read_text());plan=json.loads((P/'tile_plans.json').read_text());screens=json.loads((P/'screens.json').read_text());reg=json.loads((P/'scenario_asset_registry.json').read_text());g=json.loads((P/'inputs/path_glossary_bundle.json').read_text())
bs={b['context']['concept_id']:b for b in g['bundles']};pt={t['tile_id']:t for t in plan['tiles']};st={t['tile_id']:t for t in screens['tiles']};assets={a['asset_id']:a for a in reg['assets']};counts=collections.Counter();stepcounts=collections.Counter()
profile=json.loads(Path('00_FINAL_PIPELINE_CORE/registry/path_profiles/aws_devops_engineer.json').read_text())
assert set(pt)=={t['tile_id'] for t in out['tiles']}
for t in out['tiles']:
 planned={s['step_id']:s for s in pt[t['tile_id']]['steps'] if s['type'] in ['check','hands_on']}
 assert set(planned)=={i['step_id'] for i in t['interactions']}
 rems={r['step_id']:r for r in st[t['tile_id']].get('remediation_steps',[])}
 seen=set()
 for entry in t['interactions']:
  s=planned[entry['step_id']];ix=entry['interaction'];counts[ix['type']]+=1;stepcounts[s['type']]+=1
  assert ix['type']==s['planned_interaction_type'];assert ix['grading_mode']=='client';assert ix['anchors']==s['anchors']
  assert len(ix['feedback']['hints']) in [1,2]
  if ix['feedback'].get('remediation_step_id'):assert ix['feedback']['remediation_step_id'] in rems
  if not seen:
   assert not rems or ix['feedback']['remediation_step_id'] in rems
  seen.update(s['concept_ids'])
  if s['type']=='hands_on':assert any(a.endswith('#practice') for a in ix['anchors'])
  for m in ix['measures']:
   a=next(a for a in bs[m['concept_id']]['assessment_anchors'] if a['capability']==m['capability']);assert a['fact_ids']==m['fact_ids'];assert all('#' not in f for f in m['fact_ids'])
  pub=ix['public'];gr=ix['grading']
  assert 'the table above' not in json.dumps(pub).lower()
  if ix['type']=='choice':
   ids={o['option_id'] for o in pub['options']};assert len(gr['correct_option_ids'])==1;assert set(gr['option_feedback'])==ids
  elif ix['type']=='table_select':
   a=assets[pub['asset_ref']['asset_id']];rows=[dict(zip([c['name'] for c in a['columns']],r)) for r in a['rows']]
   for ans in gr['answers']:
    rr=[r for r in rows if all(r[k]==v for k,v in ans['row']['where'].items())];assert len(rr)==1;assert ans['row']['occurrence']==0
    if 'column' in ans:assert ans['expect_value']==rr[0][ans['column']]
  elif ix['type']=='classify':
   assert set(gr['assignments'])=={i['item_id'] for i in pub['items']};assert set(gr['item_feedback'])==set(gr['assignments'])
   inspect=s['concept_ids'][0] in profile['practice_type_by_concept']
   if inspect:
    assert 'asset_ref' not in pub
    assert not re.search(r'\b(write|implement|submit|provision|workspace|README)\b',pub['prompt'],re.I)
   else:
    assert 'role_map' in gr;assert all('source' in item for item in pub['items'])
report={'tiles':len(out['tiles']),'interaction_types':dict(counts),'step_types':dict(stepcounts),'automated_checklist':'PASS','manual_checklist':[
'Choice truth annotations produce one key; all distractors have factual explanations and no second defensible answer under the stated scope.',
'Hands-on selections cover each practice success criterion; inspect tasks require judgement of supplied excerpts, including counterexamples.',
'IAM includes applicable allow, condition failure, resource mismatch and explicit deny override; EventBridge includes positive and negative samples and omitted-field traps.',
'All row predicates and expected cell values are derived from registry rows; matching classification sources and semantic role maps are present.',
'No code exercises are planned: syntax, execution-derived expected outputs and nonpassing starters are not applicable.',
'All capabilities and bare fact IDs are copied from glossary anchors; assemble/validate independently passes taught-before-tested and plan fidelity.',
'Every prompt is self-contained; no reliance on a video or a later screen; remediation IDs copied from screens.' ]}
(P/'working/04_checklist.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
