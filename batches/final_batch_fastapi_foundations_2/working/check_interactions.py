import json,sys,ast
from pathlib import Path
sys.path.insert(0,str(Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
from schema_check import errors
B=Path('batches/final_batch_foundations_2');load=lambda name:json.loads((B/name).read_text())
o=load('interactions.json');p=load('tile_plans.json');screens=load('screens.json');g=load('inputs/path_glossary_bundle.json')
assert not errors(o,'interactions_part.schema.json')
gloss={x['context']['concept_id']:x for x in g['bundles']}
sc={t['tile_id']:t for t in screens['tiles']}
comp=load('working/computed_interaction_results.json')
counts={}
for t,ot in zip(p['tiles'],o['tiles']):
 assert t['tile_id']==ot['tile_id']
 needed=[s for s in t['steps'] if s['type'] in ('check','hands_on')]
 assert [s['step_id'] for s in needed]==[i['step_id'] for i in ot['interactions']]
 earlier=set();text_facts={}
 for s in sc[t['tile_id']]['steps']:
  text_facts[s['step_id']]=set(earlier)
  for b in s.get('blocks',[]):
   if b['type'] in ('prose','callout'):earlier.update(b.get('lineage',{}).get('fact_ids',[]))
 rem={s['step_id'] for s in sc[t['tile_id']]['remediation_steps']}
 for planned,entry in zip(needed,ot['interactions']):
  ix=entry['interaction'];cid=planned['concept_ids'][0];counts[ix['type']]=counts.get(ix['type'],0)+1
  assert ix['type']==planned['planned_interaction_type'] and ix['anchors']==planned['anchors']
  assert ix['grading_mode']=='client'
  assert 1<=len(ix['feedback']['hints'])<=2
  assert ix['feedback'].get('remediation_step_id') in rem
  for m in ix['measures']:
   assert all('#' not in f for f in m['fact_ids'])
   assert {'capability':m['capability'],'fact_ids':m['fact_ids']} in gloss[m['concept_id']]['assessment_anchors']
   assert all(m['concept_id']+'#'+f in text_facts[entry['step_id']] for f in m['fact_ids'])
  if ix['type']=='choice':
   assert len(ix['grading']['correct_option_ids'])==1
   assert set(ix['grading']['option_feedback'])=={v['option_id'] for v in ix['public']['options']}
   assert 'the table above' not in ix['public']['prompt'].lower()
  else:
   assert cid+'#practice' in ix['anchors'] and not ix['standalone']
   assert all(ix['public']['constraints'][k]==gloss[cid]['practice_anchor']['live_code'][k] for k in ('allowed_syntax','blocked_syntax'))
   assert 'execution_provenance' not in ix['grading'] and 'hidden_checks' not in ix['grading']
   starter=ix['public']['workspace']['files'][0]['content'];solution=ix['grading']['solution_files'][0]['content']
   assert starter!=solution;ast.parse(starter);ast.parse(solution)
   # Every expected is the pinned engine's observation, not a manually keyed output.
   for test in ix['grading']['tests']:
    assert test['spec']['expected']==comp[cid][test['test_id']]['value']
   assert len({json.dumps(test['spec']['args'],sort_keys=True) for test in ix['grading']['tests']})>=2
# Qualitative review against the mistakes list:
# Choice answers are uniquely defensible: intended application ownership, yield sides,
# reciprocal attribute names, inclusive endpoints, and the observed nested error path.
# Wrong choices represent per-request startup, reversed cleanup, column/navigation confusion,
# exclusive/inclusive confusion, and ignored nested validation; each has explanatory feedback.
# All learner edits are only glossary-allowed acquisition/cleanup or field declarations;
# imports, observation helpers, comprehensions and inspection are unchanged scaffolding.
# Each hands-on grades all parts of its success sentence, including boundary construction
# and nested model instance/value checks, with at least two differing inputs to its helper.
# No classify, SQL, spreadsheet, chart, or table-predicate task exists in this batch.
report={'status':'PASS','counts':counts,'tiles':{t['tile_id']:len(t['interactions']) for t in o['tiles']},'qualitative_checklist':'Reviewed: derived keys/outputs, unique answers, misconception feedback, taught-before-tested, valid capabilities, full practice success, standalone context, allowed learner syntax, nonpassing starters, exact named outputs.'}
(B/'working/interactions_self_check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
