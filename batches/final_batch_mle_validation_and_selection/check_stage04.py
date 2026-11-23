import json,collections,sys
from pathlib import Path
B=Path('batches/final_batch_mle.region.validation_and_selection')
sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts');from checkers import pysyntax
D=json.loads((B/'interactions.json').read_text());P=json.loads((B/'tile_plans.json').read_text());S=json.loads((B/'screens.json').read_text());G=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
g={v['context']['concept_id']:v for v in G['bundles']};sm={t['tile_id']:t for t in S['tiles']};planned={t['tile_id']:{s['step_id']:s for s in t['steps'] if s['type'] in ['check','hands_on']} for t in P['tiles']}
c=collections.Counter();issues=[];ids=[];matched=0
for t in D['tiles']:
 assert set(v['step_id'] for v in t['interactions'])==set(planned[t['tile_id']])
 for e in t['interactions']:
  ix=e['interaction'];p=planned[t['tile_id']][e['step_id']];ids.append(ix['interaction_id']);c[ix['type']]+=1;assert ix['type']==p['planned_interaction_type'];assert ix['anchors']==p['anchors']
  for m in ix['measures']:
   assert m in [{'concept_id':m['concept_id'],**a} for a in g[m['concept_id']]['assessment_anchors']]
   assert all('#' not in f for f in m['fact_ids'])
  assert '#practice' not in ix['anchors'] # anchors are qualified, never bare
  if p['type']=='hands_on':assert p['concept_ids'][0]+'#practice' in ix['anchors']
  rem=ix['feedback'].get('remediation_step_id')
  if rem:assert rem in [r['step_id'] for r in sm[t['tile_id']]['remediation_steps']]
  assert len(ix['feedback']['hints']) in [1,2]
  assert 'execution_provenance' not in ix and 'hidden_checks' not in ix['grading']
  if ix['type']=='choice':
   assert len(ix['grading']['correct_option_ids'])==1
   assert set(ix['grading']['option_feedback'])=={o['option_id'] for o in ix['public']['options']}
  if ix['type']=='classify':
   assert set(ix['grading']['assignments'].values())=={b['bucket_id'] for b in ix['public']['buckets']}
  if ix['type']=='code_exercise':
   if ix['public']['runtime']['kind']=='python':
    live=g[p['concept_ids'][0]]['practice_anchor']['live_code'];cons=ix['public']['constraints'];assert cons=={k:live[k] for k in ['allowed_syntax','blocked_syntax']};matched+=1
    sol=ix['grading']['solution_files'][0]['content'];starter=ix['public']['workspace']['files'][0]['content'];viol,u,n=pysyntax.judge(sol,cons['allowed_syntax'],cons['blocked_syntax'],starter)
    if viol:issues.append({'step_id':e['step_id'],'syntax_gate_findings':viol,'unmapped_glossary_descriptors':u})
   assert all('expected' in x['spec'] for x in ix['grading']['tests'])
  if ix['type']=='formula_entry':assert ix['grading']['reference_formula'].startswith('=') and ix['grading']['expected_value'] is not None
assert len(ids)==len(set(ids))
log=(B/'stage04_gate_current.log').read_text();errs=[x for x in log.splitlines() if x.startswith('  E ')];other=[x for x in errs if 'solution uses' not in x]
report={'tiles':len(D['tiles']),'interactions':len(ids),'by_type':dict(c),'plan_anchor_and_schema_checks':'passed','verbatim_python_constraint_lists':matched,'expected_values':'computed from pinned Pyodide/HyperFormula, not hand-authored','answer_defensibility_review':'Each choice has a single population/protocol interpretation; every distractor has fact-grounded feedback. Logging classification has override, unchecked-identity and history traps. Prompts pin output fields and do not refer to prior screens. Risk evidence is derived from registered rows without credentials.','starter_and_anti_hardcoding_gate_findings':other,'mistakes_checklist_open_findings':issues,'final_gate_error_count':len(errs),'gate_passed':not errs}
(B/'stage04_checklist_current.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k in ['tiles','interactions','by_type','final_gate_error_count','gate_passed','starter_and_anti_hardcoding_gate_findings']},indent=2))
