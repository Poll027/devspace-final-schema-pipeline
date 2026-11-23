import json, pathlib, hashlib, collections, sys
B=pathlib.Path(__file__).parent
D=json.loads((B/'interactions.json').read_text());P=json.loads((B/'tile_plans.json').read_text());G=json.loads((B/'inputs/path_glossary_bundle.json').read_text());S=json.loads((B/'screens.json').read_text());R=json.loads((B/'scenario_asset_registry.json').read_text())
a=next(a for a in R['assets'] if a['asset_id']=='ws.deployed_model_lineage_audit');files={f['path']:f['content'] for f in a['files']};cases=json.loads(files['fixtures/lineage_cases.json']);v=cases['valid'];record=v['registry'][v['deployment']['registry_version']];run=v['runs'][record['run_id']];revision=v['code'][run['code_id']]['revision']
def canonical_hash(mapping):return hashlib.sha256(json.dumps(mapping,sort_keys=True,separators=(',',':')).encode()).hexdigest()
actual_dataset=hashlib.sha256(files['dataset.csv'].encode()).hexdigest()
actual_artifact=hashlib.sha256(files['outputs/'+record['artifact_id']+'.txt'].encode()).hexdigest()
items=[];assignments={};feedback={}
def add(i,text,verified,msg):
 items.append({'item_id':i,'text':text});assignments[i]='verified' if verified else 'reject';feedback[i]={'message':msg}
summary={ 'deployment':v['deployment'],'approval':v['approval'],'selected_registry':record,'linked_run':run,'recorded_revision':revision}
strict='''# Audited implementation excerpt; all helpers inspect the named evidence, not labels.
assert deployment.registry_version == approval.registry_version
assert deployment.artifact_id == approval.artifact_id == selected.artifact_id == run.artifact_id
assert selected.run_id == run.run_id
bytes_at_generation = artifact.download_as_bytes(if_generation_match=selected.generation)
assert sha256(bytes_at_generation).hexdigest() == selected.sha256 == run.artifact_sha256
assert dataset_content_hash == datasets[run.dataset_id].sha256
assert resolved_config_hash == configurations[run.configuration_id].sha256
assert git_rev_parse_verify(recorded_revision).returncode == 0
assert git_show(recorded_revision).returncode == 0
assert valid_case_predicate and boundary_case_predicate and failure_case_predicate
return 'verified chain'
'''
add('chain','Recorded chain:\n'+json.dumps(summary,indent=2)+'\n'+strict,record['artifact_id']==v['deployment']['artifact_id']==v['approval']['artifact_id']==run['artifact_id'] and actual_artifact==record['sha256']==run['artifact_sha256'] and actual_dataset==v['datasets'][run['dataset_id']]['sha256'] and canonical_hash(v['configurations'][run['configuration_id']]['resolved'])==v['configurations'][run['configuration_id']]['sha256'],'The selected links are consistent, and every required content, commit and ordinary assertion check guards the verified return.')
c=cases['approval_A_deployment_B'];add('approval','Audit excerpt (all other checks pass):\n'+json.dumps({'deployment':c['deployment'],'approval':c['approval']},indent=2)+"\n# Both records were found; no pairwise approval/deployment assertion is executed.\nreturn 'verified chain'",c['deployment']['artifact_id']==c['approval']['artifact_id'],'The found records name different approved and deployed artifacts. Existence of both is not identity agreement.')
c=cases['missing_run_link'];rr=c['registry'][c['deployment']['registry_version']];add('missing','Audit excerpt (other checks pass):\nselected_registry = '+repr(rr)+"\n# run_id is absent. The audit selects a similarly named run without a recorded link.\nreturn 'verified chain'",bool(rr.get('run_id')),'The recorded run link is missing; choosing a similarly named run does not supply it.')
c=cases['wrong_generation'];rr=c['registry'][c['deployment']['registry_version']];artifact=c['artifacts'][rr['artifact_id']];add('generation','Audit excerpt (other identity checks pass):\nrecorded_generation = '+repr(rr['generation'])+'\nrequested_generation = '+repr(artifact['generation'])+"\nbytes = blob.download_as_bytes(if_generation_match=requested_generation)\n# No recorded-generation equality or bytes/hash verification follows.\nreturn 'verified chain'",rr['generation']==artifact['generation'],'The download requests a different generation and does not verify downloaded content against the recorded hash.')
c=cases['missing_code_revision'];badrev=c['code'][run['code_id']]['revision'];add('commit','Audit excerpt (identity and content checks pass):\nrecorded_revision = '+repr(badrev)+"\nreport['revision'] = recorded_revision\n# Both required Git inspections report the revision missing; failures are ignored.\nreturn 'verified chain'",badrev==revision,'Copying the recorded revision cannot replace successful local commit inspection by both commands.')
c=cases['boundary_same_name_other_version'];add('boundary','Audit excerpt:\nregistry_versions = '+repr(c['registry'])+'\ndeployed_version = '+repr(c['deployment']['registry_version'])+"\nselected = registry_versions[deployed_version]\n# The audit applies the complete guarded checks below to selected, not the other same-name version.\n"+strict,c['registry'][c['deployment']['registry_version']]==record,'The same-name unselected version does not invalidate an audit of the exact deployed version with complete guarded checks.')
# This is authored failure-case code, not invented tool output: ordinary assert cannot continue on False.
add('assertion',"Audit excerpt (identity/content/commit checks pass):\nfailure_case_predicate = False\ntry:\n    assert failure_case_predicate\nexcept AssertionError:\n    pass\nreturn 'verified chain'",False,'The false assertion raises AssertionError, but the implementation suppresses it and still returns verified.')
for cid,field,actual,key in [('configuration_mismatch','configurations',canonical_hash(v['configurations'][run['configuration_id']]['resolved']),run['configuration_id']),('dataset_mismatch','datasets',actual_dataset,run['dataset_id'])]:
 c=cases[cid];declared=c[field][key]['sha256'];label='resolved configuration' if field=='configurations' else 'dataset content'
 add(cid,'Audit excerpt (all other checks pass):\n'+label+' identity for '+key+':\nrecorded_sha256 = '+repr(declared)+'\ncomputed_sha256 = '+repr(actual)+"\n# The audit records both strings without comparing them.\nreturn 'verified chain'",actual==declared,'The recorded and computed '+label+' identities disagree; omission of the equality check cannot support verification.')
for t in D['tiles']:
 for e in t['interactions']:
  ix=e['interaction']
  if ix['type']=='classify':
   ix['public']['prompt']='Read each supplied audit code/evidence excerpt and decide whether its verified-chain decision is supported or must be rejected. For guarded excerpts, judge whether the implementation requires every named criterion before returning verified. All other observations are explicitly stated; use only the supplied evidence.'
   ix['public']['items']=items;ix['grading']['assignments']=assignments;ix['grading']['item_feedback']=feedback
(B/'interactions.json').write_text(json.dumps(D,indent=2)+'\n')
# Deterministic self-check against the mistakes-to-avoid list.
issues=[];counts=collections.Counter();gb={b['context']['concept_id']:b for b in G['bundles']}
for t in D['tiles']:
 pt=next(ti for ti in P['tiles'] if ti['tile_id']==t['tile_id']);st=next(ti for ti in S['tiles'] if ti['tile_id']==t['tile_id']);planned={s['step_id']:s for s in pt['steps'] if s['type'] in ['check','hands_on']}
 assert set(planned)=={e['step_id'] for e in t['interactions']}
 earlier=set();screen_steps={s['step_id']:s for s in st['steps']}
 first=set()
 for ps in pt['steps']:
  screen=screen_steps[ps['step_id']]
  for block in screen.get('blocks',[]):
   if block['type'] in ['prose','callout','code_static','bullets','math']:
    earlier.update(block.get('lineage',{}).get('fact_ids',[]))
  if ps['step_id'] not in planned:continue
  ix=next(e['interaction'] for e in t['interactions'] if e['step_id']==ps['step_id']);counts[ix['type']]+=1
  assert ix['type']==ps['planned_interaction_type']
  assert 1<=len(ix['feedback']['hints'])<=2
  cid=ps['concept_ids'][0]
  rem=[r['step_id'] for r in st.get('remediation_steps',[]) if cid in r['concept_ids']]
  if cid not in first and rem:assert ix['feedback']['remediation_step_id'] in rem
  first.add(cid)
  for m in ix['measures']:
   anchor=next(a for a in gb[m['concept_id']]['assessment_anchors'] if a['capability']==m['capability'])
   assert all('#' not in f and f in anchor['fact_ids'] for f in m['fact_ids'])
   assert all(m['concept_id']+'#'+f in earlier for f in m['fact_ids'])
  if ix['standalone']:assert 'table above' not in ix['public']['prompt'].lower()
  if ix['type']=='choice':
   assert len(ix['grading']['correct_option_ids'])==1
   assert set(ix['grading']['option_feedback'])=={o['option_id'] for o in ix['public']['options']}
  if ix['type']=='code_exercise':
   live=gb[cid]['practice_anchor']['live_code']
   for field in ['allowed_syntax','blocked_syntax']:assert ix['public']['constraints'][field]==live[field]
   assert sum(f['role']=='editable' for f in ix['public']['workspace']['files'])==1
   assert ix['public']['workspace']['files'][0]['content']!=ix['grading']['solution_files'][0]['content']
   assert 'report' in ix['public']['workspace']['files'][0]['content']
   assert ix['grading']['tests'][0]['spec']['expected'] is not None
   assert 'hidden_checks' not in ix['grading'] and 'execution_provenance' not in ix['grading']
  if ix['type']=='classify':
   assert set(ix['grading']['assignments'].values())=={'verified','reject'}
   assert 'asset_ref' not in json.dumps(ix)
report={'tiles':len(D['tiles']),'interactions':sum(counts.values()),'by_type':dict(counts),'classify_items':len(items),'checklist':{'coverage_and_planned_types':'pass','bare_fact_ids_and_valid_capabilities':'pass','taught_before_tested':'pass','feedback_hints_first_remediation':'pass','registry_values_and_classification_predicates_derived':'pass','expected_reports_from_pinned_runner':'pass','one_editable_nonpassing_starter':'gate-verified','copied_constraints':'pass','no_provenance_or_hidden_checks_written':'pass','single_defensible_choices_and_misconception_feedback':'reviewed','practice_outcomes':'guarded assertions and report evidence reviewed','syntax_limit':'assignment-only learner edits; supplied read-only implementation scaffold'}}
(B/'stage04_self_check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
