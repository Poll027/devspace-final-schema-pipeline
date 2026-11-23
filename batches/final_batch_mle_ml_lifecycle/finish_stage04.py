import json,pathlib,ast
B=pathlib.Path(__file__).parent
D=json.loads((B/'interactions.json').read_text())

def replace_body(code,old,new):
 assert old in code,old
 return code.replace(old,new)

jobs=[]
for tile in D['tiles']:
 for entry in tile['interactions']:
  ix=entry['interaction']
  if ix['type']!='code_exercise':continue
  c=ix['measures'][0]['concept_id'].split('.')[-1]
  solution=ix['grading']['solution_files'][0]['content']
  edits=[]
  # These are supplied unchanged infrastructure and implementations. The learner's edits
  # are assignments, the only universally detectable allowed construct in these anchors.
  if c=='dataset_quality_gate':
   solution=solution.replace('def dataset_gate(snapshot, required):','def strict_dataset_gate(snapshot, required):')
   pos=solution.index('\ndef fatal_dataset(args):')
   solution=solution[:pos]+'''\ndef warning_dataset_gate(snapshot, required):
    checks = named_dataset_checks(snapshot)
    return {'snapshot_id':snapshot['snapshot_id'],'sha256':snapshot['sha256'],'checks':checks,'failed_checks':[],'accepted':True}

# Learner binding: select the function that aggregates required failures.
dataset_gate = strict_dataset_gate
'''+solution[pos:]
   edits=[('dataset_gate = strict_dataset_gate','dataset_gate = warning_dataset_gate')]
   solution=solution.replace("{'branch':'main','snapshot_id':selected_case}","{'branch':trigger_branch,'snapshot_id':selected_case}")
   prompt='''Inspect the two supplied dataset gate implementations. Bind dataset_gate to the one that aggregates every named required failure and returns fatal rejection evidence, rather than merely warning and accepting. Change only the learner-binding assignment; preserve the fixture/runtime scaffold. Run the program. Its ordinary assertions check valid and boundary acceptance and missing-required-feature rejection, while fatal_dataset records snapshot identity and failed checks and raises on rejection. The scaffold safely writes/reloads the existing configuration with training waiting for quality, inspects required images/commands/IDs/fatal settings, and executes the configured repository_commit fixture events. The graded report contains config, per-case results, retained snapshot evidence, actual computed runs, selected_run and the false-assert observation. Accepted execution must reach training; rejected quality must exit nonzero with training skipped. Read those results, not just the function name. PyYAML is supplied from the pinned runtime dependency. This is a bounded local execution adapter, not a real-cloud submission.'''
  elif c=='model_behavior_tests':
   solution=solution.replace('def test_behavior(package, fixture, contract):','def strict_behavior_tests(package, fixture, contract):')
   pos=solution.index("\ncases=read('fixtures/behavior_cases.json')")
   solution=solution[:pos]+'''\ndef reference_only_tests(package, fixture, contract):
    if 'expected_exception' in fixture: return {'rejected_input':True}
    return {'sample_ids':fixture['expected_sample_ids'],'values':fixture['expected_values'],'shape':fixture['expected_shape']}

# Learner binding: select executable package assertions, not fixture echoing.
test_behavior = strict_behavior_tests
'''+solution[pos:]
   edits=[('test_behavior = strict_behavior_tests','test_behavior = reference_only_tests')]
   solution=solution.replace("{'branch':'main','snapshot_id':'valid','case_id':selected_case}","{'branch':trigger_branch,'snapshot_id':'valid','case_id':selected_case}")
   prompt='''Inspect the two supplied test implementations. Bind test_behavior to the one that exercises the fitted prediction package, checks row count/correspondence/shape before numerical agreement with explicit contract tolerances, and requires InputContractError for prohibited inputs. Do not bind a function that merely echoes expected fixtures. Change only the learner-binding assignment and run the supplied scaffold. Ordinary assertions exercise valid, boundary, empty and malformed cases and all four regressions. The configuration is safely written/reloaded with release_gate waiting for behavior_tests and fatal failures preserved. The unchanged repository_commit trigger executes accepted and regressed fixtures, and records actual resolved inputs and gate exit codes. The graded report includes config, results, regressions, runs, selected_run and false_assert_raises. Accepted execution must pass; deliberate regression must fail behavior_tests and skip release_gate. Inspect the outputs to distinguish executable assertions from plausible-looking expected values. Dependencies are supplied; execution is a bounded local adapter, not an actual Cloud Build run.'''
  elif c=='model_release_quality_gate':
   solution=solution.replace('def acceptance(candidate, reference, contract, event_id):','def complete_acceptance(candidate, reference, contract, event_id):')
   pos=solution.index("\ncases=read('fixtures/release_cases.json')")
   solution=solution[:pos]+'''\ndef cost_only_acceptance(candidate, reference, contract, event_id):
    cost=expected_cost(candidate,contract)
    return {'candidate_id':candidate['candidate_id'],'expected_error_cost':cost,'checks':{'cost_maximum':cost <= contract['max_expected_error_cost']}}

# Learner binding: all required predicates must hold, not only cost.
acceptance = complete_acceptance
'''+solution[pos:]
   edits=[('acceptance = complete_acceptance','acceptance = cost_only_acceptance')]
   solution=solution.replace("event={'event_type':'artifact_ready','case_id':selected_case,'artifact_id':selected_case}","event={'event_type':trigger_event_type,'case_id':selected_case,'artifact_id':selected_case}")
   prompt='''Inspect the supplied acceptance implementations. Bind acceptance to the function that rejects every failed or incomplete required predicate, not to cost-only acceptance. Change only the learner-binding assignment; run the program and inspect report. The supplied calculation validates integer counts and actual-class denominators, then uses fixed validation probabilities/costs. Acceptance must enforce candidate identity, complete evidence, operating constraints, latency and both fixed/reference cost limits, naming failures explicitly. No protected-test observations tune the system. Ordinary assertions check passing/boundary cases, latency rejection, incomplete evidence and both empty conditioning groups. The scaffold safe_dumps/safe_loads the existing configuration, keeps release_gate fatal and promotion dependent, and executes configured Pub/Sub accepted/rejected fixtures without changing bindings/filters. The graded report includes config, results, actual computed runs and selected_run with resolved candidates. Accepted execution must reach promotion; rejected gate execution must exit unsuccessfully and skip promotion. This is a bounded local runtime, not a cloud submission.'''
  elif c=='pipeline_artifact_dependencies':
   solution=solution.replace("config['steps'][1]['waitFor']=['data_validation']","config['steps'][1]['waitFor']=training_waits")
   solution=solution.replace("config['steps'][2]['waitFor']=['training']","config['steps'][2]['waitFor']=model_waits")
   solution=solution.replace("config['steps'][2]['args'][3]=cases['valid']['training']['produced']","config['steps'][2]['args'][3]=model_input")
   pos=solution.index("config['steps'][1]['waitFor']=training_waits")
   solution=solution[:pos]+'''required_training_waits = ['data_validation']
required_model_waits = ['training']
no_waits = []
training_output = cases['valid']['training']['produced']
other_input = cases['mismatch']['model_validation']['consumed']
# Learner bindings: completion dependencies and artifact identity are separate.
training_waits = required_training_waits
model_waits = required_model_waits
model_input = training_output
'''+solution[pos:]
   edits=[('training_waits = required_training_waits','training_waits = no_waits'),('model_waits = required_model_waits','model_waits = no_waits'),('model_input = training_output','model_input = other_input')]
   solution=solution.replace('report=dependency_suite(resolved,cases,selected_case)','report=dependency_suite(resolved,cases,selected_case,trigger_event_type)')
   prompt='''Repair the three learner-binding assignments using the supplied named values. training_waits must require successful data_validation; model_waits must require successful training. model_input must be the immutable identity training produces, not the mismatch fixture's other artifact. Do not modify the negative fixtures or any other scaffold. Run the program. It applies your values to the existing configuration, safely writes/reloads resolved.yaml, and asserts valid/boundary producer-consumer agreement and mismatch disagreement. The supplied suite executes identity and required-validation predicates under the existing Pub/Sub bindings and filters, inspecting reloaded images, entry points, IDs and fatal settings. report contains config, runs, selected_run and false_assert_raises. Accepted fixture results must show the actual producer-consumer identities; mismatch must fail model_validation, and failed_validation must prevent dependent training/model execution. Inspect resolved command inputs separately from waitFor order: both must agree with the contract. This is a bounded local execution adapter, not a real Cloud Build run.'''
  elif c=='staged_ml_promotion':
   solution=solution.replace("config['steps'][1]['waitFor']=['compatibility']","config['steps'][1]['waitFor']=staging_waits")
   solution=solution.replace("config['steps'][2]['waitFor']=['staging_quality']","config['steps'][2]['waitFor']=authorization_waits")
   solution=solution.replace("config['steps'][3]['waitFor']=['staging_quality','authorization']","config['steps'][3]['waitFor']=production_waits")
   pos=solution.index("config['steps'][1]['waitFor']=staging_waits")
   solution=solution[:pos]+'''compatibility_required = ['compatibility']
staging_required = ['staging_quality']
quality_and_authorization_required = ['staging_quality','authorization']
no_waits = []
# Learner bindings: production requires quality AND separate authorization.
staging_waits = compatibility_required
authorization_waits = staging_required
production_waits = quality_and_authorization_required
'''+solution[pos:]
   edits=[('staging_waits = compatibility_required','staging_waits = no_waits'),('authorization_waits = staging_required','authorization_waits = no_waits'),('production_waits = quality_and_authorization_required','production_waits = staging_required')]
   solution=solution.replace('report=promotion_suite(resolved,selected_case)','report=promotion_suite(resolved,selected_case,trigger_event_type)')
   prompt='''Repair the three learner-binding assignments using the supplied named predecessor lists. Staging must depend on compatibility; authorization on staging quality; production on BOTH staging quality and separate authorization. Change only those assignments, preserving immutable registry/run/artifact inputs, fatal settings and existing authorization scope. Run the scaffold, which safe_dumps/safe_loads and inspects the configuration and computes supplied gate results from all promotion fixtures. Inspect report: config, runs, records, selected_run, selected_record and credential_values_recorded. Accepted production must follow compatibility/offline/staged validation and authorization for the same artifact; unauthorized, wrong-artifact and failed-staging fixtures must not execute production. The accepted record must retain approval, accountable identity, registry version, run, artifact and per-stage evidence. Secret Manager version references remain in availableSecrets; secretEnv is only on production; no credential values are supplied, serialized or displayed. This is the bounded local runtime, not a claim of real cloud deployment.'''
  else:
   solution=solution.replace('def recover(context):','def reconcile_outputs(context):')
   pos=solution.index("\nconfig=read('cloudbuild.yaml')")
   solution=solution[:pos]+'''\ndef ignore_failure(context):
    return {}

# Learner binding: recovery must reconcile and validate, not ignore the failure.
recover = reconcile_outputs
'''+solution[pos:]
   edits=[('recover = reconcile_outputs','recover = ignore_failure')]
   solution=solution.replace('report=recovery_suite(resolved,recover,selected_case)','report=recovery_suite(resolved,recover,selected_case,trigger_event_type)')
   prompt='''Inspect the supplied recovery implementations. Bind recover to the implementation that catches only the declared RecoverableFailure, records it, applies the bounded action, reconciles each named upload and verifies exact-generation bytes/hash plus required validation. Do not bind the ignore-and-return implementation. Change only the learner-binding assignment and run the scaffold. Missing outputs must use create-only upload with if_generation_match=0; a 412 must cause re-read/verification, never overwrite. Unrelated failures, content conflicts and invalid existing output remain fatal. The scaffold safely writes/reloads the configuration with recovery → required_validation → promotion dependencies and executes all configured fixture cases. report contains config, outcomes, runs and selected_run. Inspect the two-call observations: A generation/hash preserved, only missing B completed, safe 412 reconciliation, no second-call uploads/generations, repeated validation. Accepted retry and later gates must execute; rejected required_validation must fail with promotion skipped. Ordinary assertions check these outcomes. Execution is a bounded local storage/trigger simulator, not a real-cloud run.'''
  # Add a real event/filter input which mutations can vary without causing a missing-case error.
  if c in ['dataset_quality_gate','model_behavior_tests']:
   solution='trigger_branch = "main"\n'+solution
  else:
   solution='trigger_event_type = "artifact_ready"\n'+solution
   # Patch supplied suite API inside materialized support_files, without hand-writing data values.
   tree=ast.parse(solution)
   assignment=next(n for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='support_files')
   files=ast.literal_eval(assignment.value)
   helper=files['support.py']
   helper=helper.replace('def dependency_suite(config, cases, selected):','def dependency_suite(config, cases, selected, event_type):')
   helper=helper.replace("event=dict(events[0]);event['case_id']=selected","event=dict(events[0]);event['case_id']=selected;event['event_type']=event_type")
   helper=helper.replace('def promotion_suite(config, selected):','def promotion_suite(config, selected, event_type):')
   helper=helper.replace('def execute(name):','def execute(name, event_type_override=None):')
   helper=helper.replace("event['artifact_id']=case['artifact_id']\n        run=", "event['artifact_id']=case['artifact_id']\n        if event_type_override is not None: event['event_type']=event_type_override\n        run=")
   helper=helper.replace('chosen,record=execute(selected)','chosen,record=execute(selected,event_type)')
   helper=helper.replace('def recovery_suite(config, recover, selected):','def recovery_suite(config, recover, selected, event_type):')
   helper=helper.replace("    return {'config':config,'outcomes':outcomes,'runs':runs,'selected_run':runs[selected]}","    ctx=recovery_context(selected)\n    def selected_retry(args): return recover(ctx)\n    def selected_gate(args):\n        fatal({'required_validation':ctx['case']['gate_ok']})\n        return {'validated_outputs':list(ctx['client'].objects)}\n    event=dict(fixture_events('pubsub')[0]);event['case_id']=selected;event['event_type']=event_type\n    selected_run=trigger_run(config,'pubsub',event,{'recovery':selected_retry,'required_validation':selected_gate})\n    return {'config':config,'outcomes':outcomes,'runs':runs,'selected_run':selected_run}")
   files['support.py']=helper
   lines=solution.splitlines(keepends=True)
   lines[assignment.lineno-1:assignment.end_lineno]=['support_files = '+repr(files)+'\n']
   solution=''.join(lines)
  starter=solution
  for correct,wrong in edits:
   assert correct in starter
   starter=starter.replace(correct,wrong)
  assert starter != solution
  ix['public']['workspace']['files'][0]['content']=starter
  ix['public']['prompt']=prompt
  ix['grading']['solution_files'][0]['content']=solution
  # Keep expected reports derived from execution; no manual edits to them.
  jobs.append({'id':entry['step_id'],'entry':'learner.py','files':[{'path':'learner.py','content':solution}],'mounts':[],'probes':[{'id':'report','kind':'expr','expr':'report'}]})
(B/'interactions.json').write_text(json.dumps(D,indent=2)+'\n')
(B/'stage04_execution_job.json').write_text(json.dumps({'packages':['numpy','pandas'],'scripts':jobs}))
print('Applied assignment-only learner tasks; preserved glossary constraints.')
