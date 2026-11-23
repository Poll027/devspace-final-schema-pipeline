import json
from pathlib import Path
B=Path('batches/final_batch_foundations_1')
d=json.loads((B/'interactions.json').read_text());p=json.loads((B/'tile_plans.json').read_text());sc=json.loads((B/'screens.json').read_text());gg=json.loads((B/'inputs/path_glossary_bundle.json').read_text());g={b['context']['concept_id']:b for b in gg['bundles']}
checks={};errors=[]
assert {t['tile_id'] for t in d['tiles']}=={t['tile_id'] for t in p['tiles']}
lookup={e['step_id']:e['interaction'] for t in d['tiles'] for e in t['interactions']}
expected={s['step_id']:s for t in p['tiles'] for s in t['steps'] if s['type'] in ['check','hands_on']}
assert set(lookup)==set(expected)
for sid,ix in lookup.items():
 assert ix['type']==expected[sid]['planned_interaction_type']
 assert ix['grading_mode']=='client'
 assert ix['anchors']==expected[sid]['anchors']
 for m in ix['measures']:
  assert all('#' not in f for f in m['fact_ids'])
  assert any(a['capability']==m['capability'] and a['fact_ids']==m['fact_ids'] for a in g[m['concept_id']]['assessment_anchors'])
 if 'remediation_step_id' in ix['feedback']:
  assert any(r['step_id']==ix['feedback']['remediation_step_id'] for t in sc['tiles'] for r in t.get('remediation_steps',[]))
 assert 1<=len(ix['feedback']['hints'])<=2
 if ix['type']=='choice':
  assert len(ix['grading']['correct_option_ids'])==1
  assert all(o['option_id'] in ix['grading']['option_feedback'] for o in ix['public']['options'])
 if ix['type']=='code_exercise':
  assert 'execution_provenance' not in ix['grading'] and 'hidden_checks' not in ix['grading']
  for anchor in ix['anchors']:
   if anchor.endswith('#practice'):
    c=anchor.split('#')[0]; lc=g[c]['practice_anchor'].get('live_code')
    if lc: assert ix['public']['constraints']=={k:lc[k] for k in ['allowed_syntax','blocked_syntax']}
checks['structure_and_anchors']='PASS: 40 interactions for 40 planned steps; all 12 requested tiles; glossary capabilities and bare fact ids; remediation ids copied from screens; constraints verbatim; no authored provenance or hidden checks.'
checks['choice_distractors']='Reviewed all 22 checks: single truth-labelled answer; false options distinguish glossary-grounded roles/conditions; each option has explanatory feedback.'
checks['untaught_facts']='Validator reports no taught-before-tested errors.'
checks['computed_expectations']='Pinned Pyodide executions stored in working/expected_python.json, working/expected_python_asgi.json and working/asgi_actual_result.json. Password booleans are explicit glossary success predicates, not execution evidence: pwdlib is unavailable.'
checks['standalone_context']='All interactions have standalone=false; no standalone table-above references.'
checks['classify_sources']='BLOCKED: origin classifications and differing components derived from ds.browser_origins with source and role_map; method matching has no corresponding registry dataset and is unsourced rather than falsely tied to unrelated rows.'
checks['hands_on_success']='BLOCKED: three table-select practices have no transcript datasets; raw HTTP, package/terminal and PostgreSQL exercises have no pinned runners. These entries remain unverified drafts, with no invented transcript row predicates.'
checks['syntax_and_mutation']='BLOCKED: several glossary descriptors do not map to the constructs they expressly name. Constraints remain verbatim. Ten literal status assignments also conflict with the mutation gate (only first four variables are mutated). No gate weakening attempted.'
checks['starter_does_not_pass']='Pinned runnable starters fail their result tests. Unsupported-runtime exercises cannot establish starter-versus-solution results.'
checks['prompt_exact_outputs']='Runnable programming tasks identify required declarations/calls and retain supplied inspectors. Comment-only async trace grading is exact-string based and requires review before publication.'
gate=json.loads((B/'working/validate_gate.json').read_text())
checks['gate']={'assembled_tiles':len(d['tiles']),'validation_pass_tiles':sum(not t['errors'] for t in gate),'validation_fail_tiles':sum(bool(t['errors']) for t in gate),'errors':sum(len(t['errors']) for t in gate),'unverified':sum(t.get('stats',{}).get('unverified',0) for t in gate)}
(B/'working/mistakes_checklist.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks['gate']))
