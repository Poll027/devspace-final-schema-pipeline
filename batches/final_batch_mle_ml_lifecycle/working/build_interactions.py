import json,sys,io
from pathlib import Path
sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts')
from checkers import sandbox,pysyntax
B=Path('batches/final_batch_mle.region.ml_lifecycle')
load=lambda f:json.loads((B/f).read_text())
P=load('tile_plans.json'); S=load('screens.json'); G=load('inputs/path_glossary_bundle.json'); R=load('scenario_asset_registry.json')
concepts={c['context']['concept_id']:c for c in G['bundles']}; assets={a['asset_id']:a for a in R['assets']}
pin=json.loads(Path('00_FINAL_PIPELINE_CORE/registry/runtimes.json').read_text())['runtimes']['python']['version']
checks={
'mle.tile.073_075.s04':('After safely reloading the existing dataset-gate configuration, which inspection establishes the required fail-closed wiring?',[
('Inspect the quality image and Python entry-point arguments, step IDs, training waitFor dependency on quality, and absence of failure allowances.','Correct: the resolved command and successful dependency, with fatal gate handling, establish the required wiring.'),
('Inspect only whether the quality step appears before training in the YAML text.','Textual location alone does not establish the explicit required waitFor dependency.'),
('Set allowFailure on quality so rejected snapshots still permit training.','Required quality failures must remain fatal; permitting them to continue defeats the gate.')]),
'mle.tile.073_075.s09':('Which approach safely round-trips and inspects the existing behavior-test configuration?',[
('Write with yaml.safe_dump, reload with yaml.safe_load, and inspect the resolved image, command, IDs and dependencies without failure allowances.','Correct: safe serialization and resolved-field inspection are both required.'),
('Reload arbitrary Python-object YAML tags to recover test-stage objects.','Safe loading accepts standard YAML tags, not arbitrary Python object constructors.'),
('Inspect only the in-memory configuration before writing it.','The required inspection is of the configuration reloaded after safe serialization, not just the original mapping.')]),
'mle.tile.073_075.s15':('A candidate fails a fixed release acceptance limit. Which next action preserves protected-test isolation?',[
('Keep the candidate rejected under the fixed policy and keep protected-test observations out of fitting, selection and tuning.','Correct: rejection does not authorize fitting, selecting or tuning on protected-test observations.'),
('Tune the candidate on protected-test observations until it passes.','Protected-test observations must not be used for tuning.'),
('Select a different candidate by comparing protected-test observations.','Protected-test observations must not be used for candidate selection.')]),
'mle.tile.073_075.s16':('What should be inspected after safely writing and reloading the release configuration?',[
('The release-gate image and command, step IDs, promotion dependency on the gate, and fatal failure handling.','Correct: inspect the resolved required fields, not merely the source representation.'),
('Only whether YAML parsing succeeds.','Successful parsing alone does not verify the required image, command, dependencies or fatal failure handling.'),
('Whether promotion can continue with a failing release-gate exit code in allowExitCodes.','Allowing a failing required gate exit code defeats fatal acceptance gating.')]),
'mle.tile.076_079.s04':('A dependency dictionary says training produced artifact A, but the resolved model-validation command consumes artifact B. What does the audit establish?',[
('The producer-consumer edge is mismatched; repair the reference and verify it against the resolved run inputs.','Correct: the consumer must use the declared immutable producer artifact, and run inputs must agree.'),
('The edge is valid because model validation ran after training.','Execution order does not repair an artifact identity mismatch.'),
('The dependency dictionary is sufficient, so the resolved command can be ignored.','Configured intent must be checked against the actual resolved inputs.')]),
'mle.tile.076_079.s10':('Which inspection respects the supplied promotion credential boundary?',[
('Check the configured secret reference and production-only injection, and verify captured output does not disclose a credential value without displaying that value.','Correct: inspect references, injection scope and non-disclosure without exposing credentials.'),
('Serialize the injected credential value into the release configuration for audit.','The credential must not be serialized; the configuration carries a reference, not the value.'),
('Print the credential to prove production received it.','Printing the credential violates the required non-disclosure boundary.')]),
'mle.tile.076_079.s16':('After retrying a failed stage, which evidence establishes that recovery preserved required gate execution?',[
('Triggered-run results and resolved inputs show the retried stage and required validation executed, and a rejected gate prevented dependent promotion.','Correct: verify executed stages and resolved inputs, including rejected downstream outcomes.'),
('An existing output object proves every required gate passed.','Existing output alone does not establish execution or acceptance of required validation.'),
('The YAML lists validation before promotion, so no execution inspection is needed.','Configuration order alone is not evidence of the actual triggered stage outcomes or resolved inputs.')]),
'mle.tile.076_079.s21':('Which evidence traces a deployed version to its recorded training provenance?',[
('Follow the selected deployed registry version to its exact artifact and originating run, then the recorded dataset, configuration and code references.','Correct: provenance is a chain of recorded identities and references.'),
('Choose any experiment with a similar model name.','Similar names are not matching recorded lineage links.'),
('Use the newest registry version even when deployment selects another version.','The trace must start with the version actually selected by the deployment.')])
}
# Choices are conceptual; no registry cell values are used as keys.
out={'schema_version':P['schema_version'],'kind':'interactions_part','path_id':P['path_id'],'batch_id':P['batch_id'],'tiles':[]}
for t in P['tiles']:
 tile={'tile_id':t['tile_id'],'interactions':[]}; out['tiles'].append(tile)
 rems=next(x for x in S['tiles'] if x['tile_id']==t['tile_id']).get('remediation_steps',[])
 seen=set()
 for step in t['steps']:
  if step['type'] not in ['check','hands_on']:continue
  cid=step['concept_ids'][0];c=concepts[cid]; measures=[]
  for a in step['anchors']:
   if '#assessment:' in a:
    cap=a.split('#assessment:')[1];anchor=next(x for x in c['assessment_anchors'] if x['capability']==cap)
    measures.append({'concept_id':cid,'capability':cap,'fact_ids':anchor['fact_ids']})
  ix={'type':step['planned_interaction_type'],'interaction_id':'ix.'+step['step_id'],'difficulty':('intro' if len(tile['interactions'])<2 else 'stretch' if step['type']=='hands_on' else 'core'),'grading_mode':'client','standalone':step['type']=='check','measures':measures,'anchors':step['anchors'],'feedback':{'correct':'You preserved the required evidence and policy boundary.','incorrect':'Recheck the required evidence rather than relying on textual order or a plausible name.','hints':['Separate configured intent from verified evidence.','Check which identity and failure boundary the requirement names.']}}
  if cid not in seen:
   remediation=next((x['step_id'] for x in rems if cid in x['concept_ids']),None)
   if remediation:ix['feedback']['remediation_step_id']=remediation
   seen.add(cid)
  if ix['type']=='choice':
   prompt,options=checks[step['step_id']]
   ix['public']={'prompt':prompt,'options':[{'option_id':'o'+str(i+1),'text':o[0]} for i,o in enumerate(options)],'selection':'single','shuffle':True}
   ix['grading']={'correct_option_ids':['o1'],'option_feedback':{'o'+str(i+1):{'message':o[1]} for i,o in enumerate(options)}}
   ix['feedback']['correct']=options[0][1];ix['feedback']['incorrect']='Review the feedback for your selected option and the required evidence boundary.'
  elif ix['type']=='code_exercise':
   a=assets['ws.'+cid.split('.')[-1]];af={f['path']:f['content'] for f in a['files']};config=json.loads(af['cloudbuild.yaml'])
   # Minimal syntax-permitted task: safe round-trip, with no fabricated runtime outcomes.
   # Keep the supplied configuration unmodified: inspection must not be portrayed as a full gate run.
   text='\n'.join(k+': '+json.dumps(v) for k,v in config.items() if k!='serviceAccount')+'\nserviceAccount: '+config['serviceAccount']
   setup='import io\nimport yaml\n# df is an alias of the YAML module, not a dataframe.\ndf = yaml\nconfig_text = '+repr(text)+'\ninput_handle = io.StringIO(config_text)\noutput_handle = io.StringIO()\n'
   starter=setup+'# Safely load the supplied configuration into result, then safely dump result to output_handle.\nresult = None\n'
   solution=setup+'result = df.safe_load(input_handle)\ndf.safe_dump(result, output_handle)\n'
   lc=c['practice_anchor']['live_code']
   problems,unmapped,_=pysyntax.judge(solution,lc['allowed_syntax'],lc['blocked_syntax'],starter)
   assert not problems,(cid,problems)
   ix['public']={'prompt':'Safely round-trip the supplied existing configuration. Set result to the mapping read from input_handle using df.safe_load, then write that mapping to output_handle using df.safe_dump. The provided name df aliases the yaml module (it is not a dataframe); these are yaml.safe_load and yaml.safe_dump. Preserve every supplied field and value, including images, commands, step IDs and waitFor lists. Both handles are provided. Do not change config_text or use arbitrary-object YAML constructors. This bounded exercise checks safe serialization only: it does not execute a pipeline, repair its dependencies, or establish a successful gate or promotion.','runtime':{'kind':'python','version':pin,'packages':['pyyaml']},'workspace':{'entry':'main.py','files':[{'path':'main.py','role':'editable','language':'python','content':starter}]},'constraints':{k:lc[k] for k in ['allowed_syntax','blocked_syntax']}}
   ix['standalone']=False
   ix['feedback']={'correct':'The supplied mapping survived safe loading and dumping with its fields preserved. This is not evidence that pipeline stages executed.','incorrect':'Load into result and safely dump that mapping to the provided output handle; preserve the supplied configuration.','hints':['Use the safe YAML interfaces named in the lesson.','The input and output handles are already open; no pipeline submission is required.']}
   ix['grading']={'solution_files':[{'path':'main.py','content':solution}],'tests':[{'test_id':'loaded','kind':'value_equals','spec':{'expr':'result','expected':config}},{'test_id':'written','kind':'value_equals','spec':{'expr':'yaml.safe_load(output_handle.getvalue())','expected':config}}]}
   # Derive expected in pinned Pyodide, not from hand-authored output.
   job={'runtime':'python','packages':['pyyaml'],'scripts':[{'id':'derive','files':[{'path':'main.py','content':solution}],'entry':'main.py','mounts':[],'probes':[{'id':test['test_id'],'kind':'expr','expr':test['spec']['expr']} for test in ix['grading']['tests']]}]}
   # _py_job supplies pinned package arguments in the runner's expected format.
   result=sandbox.node_run(sandbox._py_job('python',['pyyaml'],job['scripts']),'sandbox/run_py.mjs')['results']['derive']
   assert result['ok'],result
   for test in ix['grading']['tests']:
    probe=result['probes'][test['test_id']];assert probe['ok'],probe
    test['spec']['expected']=probe['value']
  else:
   asset=assets['ds.lineage_links'];cols=[x['name'] for x in asset['columns']];rows=[dict(zip(cols,r)) for r in asset['rows']]
   tasks=[];answers=[]
   # Explicit pairwise mismatch and missing-link predicates. Keys/values come from registry rows.
   specs=[('artifact_mismatch',lambda r:r['deployment_artifact']!=r['approved_artifact'],'deployment_artifact','Select the deployment_artifact cell in the row whose deployed artifact differs from its approved artifact.'),('missing_run',lambda r:r['run_id'] in [None,''],'run_id','Select the run_id cell in the row with a missing originating run reference.')]
   for task_id,predicate,column,prompt in specs:
    matches=[r for r in rows if predicate(r)];assert len(matches)==1,(task_id,matches)
    row=matches[0];tasks.append({'task_id':task_id,'prompt':prompt,'target_kind':'cell'});answers.append({'task_id':task_id,'row':{'where':{'case_id':row['case_id']},'occurrence':0},'column':column,'expect_value':row[column]})
   ix['public']={'asset_ref':{'asset_id':asset['asset_id']},'intro':'Inspect the supplied lineage-link table. Select the explicit broken links, not a similarly named model. This table task verifies recorded references only; it cannot verify downloaded bytes or execute local Git commands.','tasks':tasks}
   ix['grading']={'answers':answers,'task_feedback':{x['task_id']:{'correct':'The selected cell identifies the explicitly missing or mismatched link.','incorrect':'Compare the recorded pair or locate the missing run reference; do not infer a link from a familiar name.'} for x in tasks}}
   ix['standalone']=False
   ix['feedback']['hints']=['Trace each recorded edge independently.','A missing link must remain explicit, not guessed from another field.']
  for key in ['correct','incorrect']:
   ix['feedback'][key]={'message':ix['feedback'][key]}
  if ix['type']=='code_exercise':
   for test in ix['grading']['tests']:test['message_on_fail']='Preserve the complete supplied mapping through safe YAML loading and dumping.'
  tile['interactions'].append({'step_id':step['step_id'],'interaction':ix})
(B/'interactions.json').write_text(json.dumps(out,indent=2)+'\n')
print('Wrote',sum(len(t['interactions']) for t in out['tiles']),'interactions')
