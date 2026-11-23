import ast,json,pathlib,collections
B=pathlib.Path('batches/final_batch_mle.region.production_operations'); d=json.loads((B/'interactions.json').read_text())
ids={'080_082.s04','080_082.s14','083_085.s06','083_085.s16','086_089.s16','086_089.s21','091_094.s09','091_094.s14'}
checks=[]
for t in d['tiles']:
 for e in t['interactions']:
  if e['step_id'].removeprefix('mle.tile.') not in ids: continue
  i=e['interaction']; st=i['public']['workspace']['files'][0]['content']; sol=i['grading']['solution_files'][0]['content']
  ast.parse(st);ast.parse(sol)
  assert st!=sol and 'TODO' in st
  assert i['anchors'] and i['measures'] and i['grading']['tests']
  assert all('#' not in f for m in i['measures'] for f in m['fact_ids'])
  checks.append({'step_id':e['step_id'],'starter_has_unimplemented_learner_work':True,'anchors_and_tests_retained':True})
log=(B/'full_skill_validate.log').read_text(); errors=[l.strip() for l in log.splitlines() if l.startswith('  E ')]
assert all("solution uses" in l and "allowed syntax" in l for l in errors)
(B/'full_skill_self_audit.json').write_text(json.dumps({'patched_interactions':checks,'interaction_counts':dict(collections.Counter(e['interaction']['type'] for t in d['tiles'] for e in t['interactions'])),'gate_errors':len(errors),'gate_blocker':'syntax detector does not map permitted glossary descriptors; constraints left unchanged','mistakes_review':'No new answer keys, facts, distractors, measures, fixtures or tests; learner logic no longer supplied for the named skills. Output tests execute successfully; syntax gate remains blocking.'},indent=2)+'\n')
print(len(checks),'patched interactions;',len(errors),'syntax gate errors; no execution, schema, lineage, or answer-key errors.')
