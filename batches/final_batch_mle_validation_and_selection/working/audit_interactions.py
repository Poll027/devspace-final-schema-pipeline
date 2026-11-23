import json,sys,collections
from pathlib import Path
sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts')
from checkers.pysyntax import judge
P=Path('batches/final_batch_mle.region.validation_and_selection')
x=json.load(open(P/'interactions.json'));plans=json.load(open(P/'tile_plans.json'));screens=json.load(open(P/'screens.json'));g=json.load(open(P/'inputs/path_glossary_bundle.json'));registry=json.load(open(P/'scenario_asset_registry.json'))
G={b['context']['concept_id']:b for b in g['bundles']};assets={a['asset_id']:a for a in registry['assets']}
counts=collections.Counter();issues=[]
for t,pt,st in zip(x['tiles'],plans['tiles'],screens['tiles']):
 expected=[s for s in pt['steps'] if s['type'] in ['check','hands_on']]
 assert t['tile_id']==pt['tile_id']==st['tile_id'];assert [e['step_id'] for e in t['interactions']]==[e['step_id'] for e in expected]
 rem={r['step_id'] for r in st['remediation_steps']}
 for e,s in zip(t['interactions'],expected):
  i=e['interaction'];counts[i['type']]+=1
  assert i['type']==s['planned_interaction_type'];assert i['anchors']==s['anchors'];assert not i['standalone']
  assert len(i['feedback']['hints']) in [1,2];assert i['feedback'].get('remediation_step_id') in rem
  for m in i['measures']:
   aa=next(a for a in G[m['concept_id']]['assessment_anchors'] if a['capability']==m['capability'])
   assert m['fact_ids']==aa['fact_ids'];assert all('#' not in f for f in m['fact_ids'])
  if i['type']=='choice':
   opts={o['option_id'] for o in i['public']['options']};assert len(i['grading']['correct_option_ids'])==1;assert opts==set(i['grading']['option_feedback'])
  if i['type']=='formula_entry':assert i['grading']['expected_value'] not in ['#ERROR!','#VALUE!','#DIV/0!','#REF!']
  if i['type']=='code_exercise':
   assert 'hidden_checks' not in i['grading'] and 'execution_provenance' not in i['grading'];assert i['grading']['tests']
   ws=i['public']['workspace'];sol=i['grading']['solution_files'];assert sol[0]['content']!=ws['files'][0]['content'];assert sol[0]['path']==ws['entry']
   if i['public']['runtime']['kind']=='python':
    c=s['concept_ids'][0];live=G[c]['practice_anchor']['live_code'];co=i['public']['constraints'];assert co['allowed_syntax']==live['allowed_syntax'] and co['blocked_syntax']==live['blocked_syntax']
    violations,unmapped,_=judge(sol[0]['content'],co['allowed_syntax'],co['blocked_syntax'],ws['files'][0]['content']);assert not violations
    if unmapped:issues.append({'step_id':s['step_id'],'unmapped_descriptors':unmapped})
manual={
 'key_derivation':'Cell keys come from registry rows; formula and Python expected values come from pinned runtime probes.',
 'one_defensible_choice':'Reviewed every option against the named glossary facts; distractors assert mistaken conditioning, evidence leakage, permission expansion or unsupported generalization.',
 'taught_before_tested':'Measures and assessment anchors copied from plan; deterministic gate also checks preceding text.',
 'success_scope':'Python work is scaffolded small edits due syntax-descriptor conflicts. Full function authoring is not assessed. Training-randomness work summarizes supplied paired results rather than running adapter trials; regularization and search replay supplied records. Logging table selection cannot implement the MLflow anchor because the planned type and sole contract table provide no run or artifact evidence. These are unresolved scope limitations, not claims of success.',
 'starters':'Editable starters use None analysis placeholders, not the reference values; output contracts and infrastructure are supplied.',
 'output_contracts':'All code prompts name result and preserve exact scaffold fields; spreadsheet prompts pin label order, precision, target and decision contract.',
 'boundaries':'No protected-test access; undefined conditioning is guarded; evidence limits are explicit.',
 'gate_blocker':'Existing screen mle.tile.019_020.s06 data_table SQL fails GROUP BY binding of expected_cost_bound. No screen artifact has been edited.'
}
report={'tile_count':len(x['tiles']),'interaction_count':sum(counts.values()),'by_type':dict(counts),'automatic_checks':'passed','mistakes_to_avoid_review':manual,'checker_uncertainties':issues}
(P/'working/interactions_audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['tile_count','interaction_count','by_type','automatic_checks']},indent=2))
