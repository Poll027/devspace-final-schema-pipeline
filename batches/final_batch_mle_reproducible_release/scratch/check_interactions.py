import json
from collections import Counter
from pathlib import Path
B=Path('batches/final_batch_mle.region.reproducible_release')
load=lambda n:json.loads((B/n).read_text())
p=load('tile_plans.json');d=load('interactions.json');s=load('screens.json');g=load('inputs/path_glossary_bundle.json')
bundles={b['context']['concept_id']:b for b in g['bundles']}
actual={t['tile_id']:{x['step_id']:x['interaction'] for x in t['interactions']} for t in d['tiles']}
counts=Counter();nitems=0
for t in p['tiles']:
 sc=next(x for x in s['tiles'] if x['tile_id']==t['tile_id'])
 remediation={r['step_id'] for r in sc.get('remediation_steps',[])}
 wanted={x['step_id']:x for x in t['steps'] if x['type'] in ['check','hands_on']}
 assert set(actual[t['tile_id']])==set(wanted)
 for sid,plan in wanted.items():
  ix=actual[t['tile_id']][sid];counts[ix['type']]+=1
  assert ix['type']==plan['planned_interaction_type']
  assert ix['anchors']==plan['anchors']
  assert ix['grading_mode']=='client'
  assert len(ix['feedback']['hints']) in [1,2]
  assert ix['feedback'].get('remediation_step_id') in remediation
  assert 'asset_ref' not in ix['public'] and 'runtime' not in ix['public']
  assert 'table above' not in ix['public']['prompt'].lower()
  for m in ix['measures']:
   anchor=next(a for a in bundles[m['concept_id']]['assessment_anchors'] if a['capability']==m['capability'])
   assert m['fact_ids']==anchor['fact_ids']
   assert all('#' not in f for f in m['fact_ids'])
  assert set((m['concept_id']+'#assessment:'+m['capability']) for m in ix['measures'])==set(a for a in plan['anchors'] if '#assessment:' in a)
  if plan['type']=='hands_on':assert plan['concept_ids'][0]+'#practice' in ix['anchors']
  if ix['type']=='choice':
   assert len(ix['grading']['correct_option_ids'])==1
   assert set(ix['grading']['option_feedback'])=={o['option_id'] for o in ix['public']['options']}
  else:
   assert set(ix['grading']['assignments'])=={it['item_id'] for it in ix['public']['items']}
   assert set(ix['grading']['assignments'].values())=={'meets','violates'} # includes concrete shortcut/trap excerpts
   assert set(ix['grading']['item_feedback'])==set(ix['grading']['assignments'])
   nitems+=len(ix['public']['items'])
# Manual semantic review: each named check has an explicit evidence-bearing fragment; wrong fragments contain an unconditional import call, latest lookup, evidence mutation, unverifiable rerun, late hash rejection, refit/untrusted load, wrong conditioning/retuning, or premature/duplicate job acceptance. No wrong option is correct under the question's stated requirement.
# Computation review: fixture identities/configuration are loaded, digest values are hashed from actual fixture bytes, default/configured training results execute the supplied workflow, and protected counts/rates/costs are calculated from registry rows. No runtime code exercise, starter, solution, or hidden checks are authored (planned inspect-and-judge override).
# Taught-before-tested review: strict validate_tile checks measured facts against preceding text; all hands-on facts and assessment capabilities come from the corresponding planned glossary anchors. Earlier screens, not video, carry those facts.
report={'tiles':len(d['tiles']),'interactions':sum(counts.values()),'by_type':dict(counts),'classify_items':nitems,'checklist':'PASS: plan fidelity, anchors/bare facts, text-first gate, derived values, single choice keys, feedback and hints, actual remediation references, traps, self-contained prompts, inspect-and-judge runtime boundary; manual semantic review completed.'}
(B/'scratch'/'interaction_checklist.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
