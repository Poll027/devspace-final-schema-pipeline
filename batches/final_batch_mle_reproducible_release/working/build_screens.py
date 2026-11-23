import json, re, copy, ast
from pathlib import Path
P=Path('batches/final_batch_mle.region.reproducible_release')
plan=json.loads((P/'tile_plans.json').read_text())
gloss=json.loads((P/'inputs/path_glossary_bundle.json').read_text())
B={b['context']['concept_id']:b for b in gloss['bundles']}
R=json.loads((P/'scenario_asset_registry.json').read_text()); A={a['asset_id']:a for a in R['assets']}
def file(c,n): return next(f['content'] for f in A['ws.'+c]['files'] if f['path']==n)
def data(c,n): return json.loads(file(c,n))
# Each entry re-voices one named teaching block, without extending its facts.
texts={
'ml_training_script':[
'A training script must work outside the notebook. Its entry point separates direct execution from ordinary imports.',
'Guard the executable call with if __name__ == "__main__": direct execution runs it; ordinary imports do not. Give the training function explicit parameters. Resolve defaults and keyword overrides before training, and map fields decoded by json.load to those arguments.',
'Run python training_script.py and compare recorded configuration and outputs with the supplied notebook behavior. subprocess.run(["python", script_path], check=True) raises on nonzero exit. Save structured records with json.dump and recover them with json.load.',
'Call the function with defaults and with keyword overrides. Keep task state in parameters or locals, not notebook globals. Emit resolved parameters and validation results with f-strings. Save the script, stage it with git add SCRIPT_PATH, commit with git commit and retain the revision.',
'From a clean shell, run python training_script.py > capture.log 2>&1. Inspect the captured parameters and result.',
'For the order fixture, pass task state explicitly, test default and override calls, and decode JSON into arguments. Guard execution, save and commit the script. Run a clean subprocess, check its exit and compare captured resolved parameters and validation output with the notebook behavior. Round-trip the record with json.dump/json.load; redirect both output streams to the log. Starting successfully alone does not check for forgotten notebook globals.',
'JSON text is not a dictionary until decoded. Do not depend on notebook globals or report defaults when keyword overrides actually supplied different values.'
],
 'training_dataset_version':[
'An overwritten dataset can keep the same name. Record the generation and content identity, not just latest.',
'Object Versioning retains noncurrent versions; a mutable name may resolve to new bytes. Select the recorded generation with bucket.blob(object_name, generation=recorded_generation).download_to_filename(local_path). Confirm that object/version exists using the authorized client before declaring it available.',
'Hash actual bytes with hashlib.sha256(data_bytes).hexdigest() and compare the expected identity. Keep object name, generation and observed digest in the snapshot record. Upload with bucket.blob(object_name).upload_from_filename(local_path); inspect and record the created generation.',
'Read the local dataset with open(path, "rb") and update SHA-256 from those bytes before recording upload identity. After an authorized overwrite of latest, retrieve the original generation again and compare its digest with the snapshot digest.',
'For the supplied training orders, hash the local binary bytes, upload to the version-enabled test bucket and retain the created generation. Confirm that generation exists, retrieve it explicitly and compare the downloaded digest with the expected identity. In the authorized overwrite fixture, change only latest, then retrieve the recorded generation again. Compare its digest with the original record. The object name identifies the family; the generation selects a version; the digest checks the actual bytes.',
'A mutable name is not immutable identity. A recorded digest without checking downloaded bytes does not verify retrieval.'
],
 'training_environment_record':[
'Record what actually executed. A remembered dependency list or typed commit label is not independent environment evidence.',
'Inspect the actual commit with git rev-parse --verify HEAD. Collect installed pins with python -m pip freeze; package==version output can be installed with pip install -r. Capture the actual execution context with runtime/environment facilities alongside its recorded runtime identity.',
'Use json.dump to save the manifest dictionary and json.load to parse it back. Use explicit with open handles in "w" and "r" modes with encoding="utf-8". Compare parsed revision, dependency mapping and runtime identity with independent observations; reject mismatches.',
'Import sys and record sys.version and sys.executable beside the supplied runtime identity.',
'Inspect HEAD, pip freeze, sys.version and sys.executable in the actual process. Save the manifest through a UTF-8 text handle, then parse it back. Compare the parsed commit, dependency mapping and runtime fields with independently inspected values. Install pins with pip install -r where needed. Retain the saved manifest and verified environment identity for later resolution. A revision mismatch is a verification failure, not permission to change observed HEAD to fit the record.',
'Writing is not verification. Use actual runtime details and dependency pins; reject a parsed manifest that disagrees with independent observations.'
],
 'experiment_reproduction':[
'Resolve the recorded code, dataset, environment and settings before rerunning. A familiar run name does not identify today’s working tree or data as the old experiment.',
'Retrieve the recorded revision, snapshot, environment and resolved settings. Check out the recorded local commit and verify HEAD. Download the recorded dataset generation and verify its identity instead of choosing latest.',
'Use the recorded Python/dependency environment, installing pins where needed. Give the execution function defaults and explicit keyword overrides; pass resolved state through parameters. Run a clean subprocess in the recorded working directory, checking exit status and capturing output.',
'Navigate the referenced repository and artifact directories before resolving relative paths. > capture.log 2>&1 saves stdout and stderr; inspect the log. A pipe instead connects one command’s output to the next command’s input.',
'For the order run, retrieve and verify the recorded commit and dataset generation, and use the pinned Python environment. Resolve defaults and overrides through function parameters. Navigate the recorded directories before resolving script, dataset and configuration paths. Launch a clean subprocess with checked exit and captured output, then inspect its resolved parameters against the record. Successful exit alone cannot verify dataset or settings. A changed latest dataset or working directory belongs to a different execution context. Redirection saves both streams; a pipe feeds another command.',
'A matching filename is not reproduction identity. Changed code, mutable data or an unresolved local path can change the experiment.'
],
 'model_version_registration':[
'A registry version must trace to a verified run artifact. Resolve its stored generation and compare its bytes with the originating run’s expected hash first.',
'Resolve the tracked run’s artifact record, expected hash and immutable version. Download with bucket.blob(key, generation=recorded_generation).download_to_filename(path), not the current key. Compute SHA-256 over downloaded bytes and reject a mismatch before registration.',
'Require the supplied registered model name; create it with client.create_registered_model(name) only on the new-name path. Call client.create_model_version(name=name, source=version_qualified_source, run_id=run_id) and retain its numeric version. Preserve exact generation and hash with set_model_version_tag. Retrieve get_model_version(name, version) and the linked originating run to compare identities.',
'Import MlflowClient from mlflow and construct the client for version creation, retrieval and tagging. In the authorized test bucket, overwrite latest, then retrieve the registered generation again and verify its hash. Return one keyed verdict. An overwrite is not a new approved registry version.',
'For the order artifact, verify the recorded generation’s bytes before creating a numeric version under the supplied model name. Link the version-qualified source and originating run, retain generation/hash tags, and retrieve both records to compare identities. In the authorized overwrite fixture, retrieve that registered generation again and verify its hash. One keyed verdict binds run, version and artifact; a later overwrite does not approve another registry version.',
'A numeric registry version does not verify a mutable source. Check the exact generation and hash; object overwrite is not registry approval.'
],
 'model_preprocessing_package':[
'Package the fitted model and fitted preprocessor together. Loading only weights or refitting preprocessing can change prediction representation despite successful execution.',
'Import pickle. Save {"model": model, "preprocessor": preprocessor} at the recorded version-tied path using a binary "wb" handle and pickle.dump(..., protocol=5). Reload only trusted, verified packages in the compatible pinned environment with an "rb" handle and pickle.load; retrieve both keys. Untrusted pickle can execute arbitrary code.',
'Build with docker build -t IMAGE:TAG CONTEXT. Include the Dockerfile (or select with -f) and every COPY source; .dockerignore must not exclude required files. Record immutable image identity, not just its tag. Apply fitted preprocessing before the packaged model, without refitting. Start with docker run --name NAME -p HOST_PORT:CONTAINER_PORT --env KEY=VALUE IMAGE, using declared nonsecret settings.',
'Use docker container inspect NAME to check image identity and State. Read stdout/stderr with docker container logs NAME for initialization or execution failures. Do not put secrets in Dockerfile ARG or ENV: they persist in the image or metadata.',
'Use the runtime secret mechanism, not literal sensitive values in Compose. Save/reload fitted state through binary handles. Write/read pinned inference requirements through text handles and install that manifest in the serving image.',
'Assert that pre-save and container-reloaded predictions agree on identical fixed inputs under declared tolerances. Separately verify fitted preprocessing parameters. Write assert predicate checks for valid, boundary and failure cases; a false assertion raises AssertionError in ordinary non-optimized execution.',
'For the order package, save fitted state in its version-tied trusted path and retain pinned requirements. Build the declared context containing the package, requirements and serving source; record immutable image identity. Start that image with declared port and nonsecret settings, then inspect identity, state and logs. Compare pre-save and container-reloaded predictions on the same fixed orders under supplied tolerances; separately verify preprocessing parameters. Use runtime secrets and reject untrusted pickle loading.',
'Packaging does not permit refitting or embedded credentials. A tag alone does not verify image identity. Pickle requires trusted, verified provenance and compatible pinned dependencies.'
],
 'protected_test_comparison':[
'Protected testing compares an already fixed system. Freeze candidate, fitted preprocessing and threshold first; report disappointing results instead of selecting a replacement.',
'Evaluate only after fixing candidate, fitted preprocessing and threshold. Compare selected-model and baseline predictions on identical protected observations using precommitted predictive quantities. Keep deployment class probabilities, error costs and operating requirements fixed. Report failure; do not retune or choose a replacement from test results.',
'FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) conditions on actual positives. Empty conditioning groups yield undefined rates. With zero cost for correct predictions, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN, using supplied deployment probabilities.',
'For the order fixture, compare frozen B and baseline on the same protected observations. Keep model identity, fitted preprocessing, threshold, deployment probabilities, costs and requirements at their pre-test values. Retain observed actual-class conditioning counts; those counts and deployment probabilities have different roles. Apply the precommitted quality and operating requirements, explicitly reporting failure or undefined quantities. FPR uses actual negatives and FNR actual positives; an empty group is undefined. Compute expected error cost from the fixed deployment probabilities and error costs, not a class mix chosen to make B pass.',
'Test failure does not authorize switching candidate, refitting preprocessing or searching for a better threshold on protected observations.'
],
 'bounded_managed_training':[
'One managed custom-training job must bind authorized resource bounds, verified inputs and the expected artifact. Submission alone does not verify successful training.',
'A SageMaker CreateTrainingJob request includes TrainingJobName, AlgorithmSpecification, RoleArn, InputDataConfig, OutputDataConfig, ResourceConfig and StoppingCondition. Use the supplied TrainingImage, authorized instance count/type and MaxRuntimeInSeconds. Provide version-resolved inputs and the output S3 location; the role must be authorized for them.',
'The container reads channels at /opt/ml/input/data/CHANNEL and writes model output at /opt/ml/model for upload. Inspect final status and artifact location against recorded configuration. Preserve snapshot, code/configuration and resulting run/artifact identities in the execution record.',
'Import boto3; construct boto3.client("sagemaker") and call client.create_training_job(**resolved_configuration). Inspect client.describe_training_job(TrainingJobName=job_name): TrainingJobStatus, FailureReason when present, and ModelArtifacts.S3ModelArtifacts. Round-trip structured configuration or records with json.dump/json.load; JSON text is not a dictionary.',
'Verify each version-qualified input before submission. If the API accepts only a mutable channel URI, materialize the chosen version at a controlled immutable location; do not invent a version parameter. Retrieve output with the authorized storage client and compare its reference with the completed job record. Training resources are released after termination; confirm terminal status, not just submission.',
'For the authorized order job, resolve image, role, name, channels, output, instance count/type and runtime limit before submission. Verify input versions and materialize at a controlled immutable location if needed. Read channel inputs under /opt/ml/input/data; write the model under /opt/ml/model. Inspect terminal status, any failure reason and output reference. Retrieve the artifact through authorized storage and compare it with the completed record. Round-trip snapshot, code/configuration and run/artifact identities as structured JSON.',
'Submission is not completion; an input name is not verified identity. Confirm terminal status before concluding managed compute has ended.'
]}
# Dockerfile mechanism belongs to tb2; retain it as a separate single-idea paragraph.
docker_text='The Dockerfile selects compatible Python with FROM, sets WORKDIR /app, copies requirements.txt and runs pip install --no-cache-dir -r requirements.txt. COPY the supplied package and serving source from the build context into declared /app paths. Set CMD to the supplied serving command and argument as a JSON array; replace placeholders with the declared package, dependencies and entry point.'

def lineage(c,tbs=(),facts=(),visual=False):
 d={'concept_ids':[c],'teaching_block_ids':list(tbs),'fact_ids':list(facts)}
 if visual:d['anchors']=[c+'#visual']
 return d

def prose(text,c,tbs,facts,role='mechanism'):
 return {'type':'prose','text':text,'role':role,'lineage':lineage(c,tbs,facts)}
def tb_blocks(c,t):
 idx=int(t['id'][2:])-1; txt=texts[c.split('.')[-1]][idx]; fs=[c+'#'+f for f in t['fact_ids']]; ts=[c+'#'+t['id']]
 out=[prose(txt,c,ts,fs,t['purpose'] if t['purpose'] in ['intro','mechanism','example','misconception'] else 'mechanism')]
 if c=='mle.model_preprocessing_package' and t['id']=='tb2':out.append(prose(docker_text,c,ts,fs))
 return out

def cw(code,c,annotation=None):
 d={'type':'code_walkthrough','language':'python','code':code.strip(),'reveal':'all','lineage':lineage(c,visual=True)}
 if annotation:d['annotations']=[{'start_line':1,'end_line':len(d['code'].splitlines()),'text':annotation}]
 return d

codes={
'ml_training_script':'''import json
from fixture_workflow import supplied_workflow
with open("configuration.json") as handle:
    configuration = json.load(handle)

def train(dataset_path=configuration["dataset_path"], threshold=configuration["threshold"]):
    result = supplied_workflow(dataset_path=dataset_path, threshold=threshold)
    for name, value in result["resolved_parameters"].items():
        print(f"{name}={value}")
    print(f"validation_accuracy={result['validation_accuracy']}")
    return result

if __name__ == "__main__":
    default_result = train()
    override_result = train(**configuration)
# Direct execution enters the guard; ordinary imports do not.
# python training_script.py > capture.log 2>&1
# git add training_script.py
# git commit
# git rev-parse --verify HEAD''',
 'training_dataset_version':'''import hashlib
with open(local_path, "rb") as handle:
    original_digest = hashlib.sha256(handle.read()).hexdigest()
blob = bucket.blob(object_name)
blob.upload_from_filename(local_path)
blob.reload()
recorded_generation = blob.generation
selected = bucket.blob(object_name, generation=recorded_generation)
assert selected.exists()
selected.download_to_filename(download_path)
with open(download_path, "rb") as handle:
    observed_digest = hashlib.sha256(handle.read()).hexdigest()
assert observed_digest == original_digest
record = {"object_name": object_name, "generation": recorded_generation,
          "observed_digest": observed_digest}
# Save this record locally.
# After the authorized latest overwrite, repeat the selected download
# and binary hash comparison using the retained generation and digest.''',
 'training_environment_record':'''import json, subprocess, sys
revision = subprocess.run(["git", "rev-parse", "--verify", "HEAD"],
    check=True, capture_output=True, text=True).stdout.strip()
pins = subprocess.run([sys.executable, "-m", "pip", "freeze"],
    check=True, capture_output=True, text=True).stdout
dependency_mapping = dict(line.split("==", 1) for line in pins.splitlines() if "==" in line)
manifest = {"revision": revision, "dependencies": dependency_mapping,
            "runtime_identity": runtime_identity,
            "sys_version": sys.version, "sys_executable": sys.executable}
with open(manifest_path, "w", encoding="utf-8") as handle:
    json.dump(manifest, handle)
with open(manifest_path, "r", encoding="utf-8") as handle:
    parsed = json.load(handle)
# Independently inspect HEAD, dependency mapping and runtime fields.
# Compare them with parsed values and reject any mismatch.''',
 'experiment_reproduction':'''import subprocess
# Resolve the run record: commit, generation, environment, settings, cwd.
subprocess.run(["git", "checkout", recorded_revision], check=True)
head = subprocess.run(["git", "rev-parse", "--verify", "HEAD"],
    check=True, capture_output=True, text=True).stdout.strip()
assert head == recorded_revision
bucket.blob(object_name, generation=recorded_generation).download_to_filename(local_path)
# Verify downloaded bytes against recorded snapshot identity.
# Install recorded pins in the recorded Python environment where needed.
def execute(settings=recorded_settings, working_directory=recorded_directory):
    return subprocess.run([recorded_python, script_path],
        cwd=working_directory, check=True, capture_output=True, text=True)
default_run = execute()
explicit_run = execute(settings=recorded_settings, working_directory=recorded_directory)
# Pass settings to the script's declared configuration interface.
# Inspect captured output against recorded resolved parameters.
# Shell alternative: python training_script.py > capture.log 2>&1''',
 'model_version_registration':'''import hashlib
from mlflow import MlflowClient
client = MlflowClient()
bucket.blob(key, generation=recorded_generation).download_to_filename(path)
with open(path, "rb") as handle:
    observed_hash = hashlib.sha256(handle.read()).hexdigest()
assert observed_hash == expected_hash
# Require the supplied registered model; create only on the new-name path.
created = client.create_model_version(name=name,
    source=version_qualified_source, run_id=run_id)
client.set_model_version_tag(name, created.version, "generation", str(recorded_generation))
client.set_model_version_tag(name, created.version, "hash", observed_hash)
version_record = client.get_model_version(name, created.version)
originating_run = client.get_run(run_id)
# Compare version and run identities.
# After authorized latest overwrite, retrieve the same generation,
# verify the registered hash again, and return one keyed verdict.''',
 'bounded_managed_training':'''import boto3, json
# resolved_configuration contains the supplied job name, TrainingImage,
# RoleArn, InputDataConfig, OutputDataConfig, ResourceConfig and StoppingCondition.
# Verify each selected input version; use a controlled immutable URI if needed.
client = boto3.client("sagemaker")
submission = client.create_training_job(**resolved_configuration)
final = client.describe_training_job(TrainingJobName=job_name)
status = final["TrainingJobStatus"]
failure_reason = final.get("FailureReason")
artifact_reference = final.get("ModelArtifacts", {}).get("S3ModelArtifacts")
# Continue inspection until terminal status; submission is not completion.
# Container: read /opt/ml/input/data/CHANNEL; write /opt/ml/model.
# Retrieve output with authorized storage and verify against completed record.
record = {"dataset_snapshot": snapshot, "code_reference": code_reference,
          "configuration": resolved_configuration, "job_name": job_name,
          "status": status, "artifact_reference": artifact_reference}
with open(record_path, "w") as handle:
    json.dump(record, handle)
with open(record_path) as handle:
    parsed_record = json.load(handle)'''
}
# Obtain function defaults from registered source rather than typing scenario values.
workflow_tree=ast.parse(file('ml_training_script','fixture_workflow.py'))
fn=next(n for n in workflow_tree.body if isinstance(n,ast.FunctionDef) and n.name=='supplied_workflow')
args=[n.arg for n in fn.args.args]
defaults=dict(zip(args[-len(fn.args.defaults):],[ast.literal_eval(n) for n in fn.args.defaults]))
codes['ml_training_script']=codes['ml_training_script'].replace('with open("configuration.json") as handle:\n    configuration = json.load(handle)\n','')
codes['ml_training_script']=codes['ml_training_script'].replace('dataset_path=configuration["dataset_path"], threshold=configuration["threshold"]', ', '.join(k+'='+repr(v) for k,v in defaults.items()))
codes['ml_training_script']=codes['ml_training_script'].replace('    default_result = train()', '    with open("configuration.json") as handle:\n        configuration = json.load(handle)\n    default_result = train()')
codes['experiment_reproduction']=codes['experiment_reproduction'].replace('import subprocess','import subprocess, json\nfrom pathlib import Path')
codes['experiment_reproduction']=codes['experiment_reproduction'].replace('    return subprocess.run([recorded_python, script_path],','    with open(Path(working_directory) / "configuration.json", "w") as handle:\n        json.dump(settings, handle)\n    return subprocess.run([recorded_python, script_path],')
codes['experiment_reproduction']=codes['experiment_reproduction'].replace("# Pass settings to the script's declared configuration interface.",'# The recorded script reads configuration.json in its working directory.')
# Visuals contain instructional code only; no authored runtime output.
def visual(c):
 short=c.split('.')[-1]
 if short=='model_preprocessing_package':
  d=data(short,'package_contract.json')
  left=cw('''# Fitted state before saving
package = {"model": model, "preprocessor": preprocessor}
transformed = preprocessor.transform(fixed_inputs)
pre_save = model.predict(transformed)
# Keep fitted preprocessing parameters for a separate preservation check.''',c)
  right=cw('''import pickle
with open(PACKAGE_PATH, "wb") as handle:
    pickle.dump(package, handle, protocol=5)
# Reload only trusted, verified artifacts in the compatible pinned environment.
with open(PACKAGE_PATH, "rb") as handle:
    reloaded = pickle.load(handle)
reloaded_predictions = reloaded["model"].predict(
    reloaded["preprocessor"].transform(fixed_inputs))
# Compare predictions under declared tolerances and fitted parameters separately.'''.replace('PACKAGE_PATH',repr(d['package_path'])),c)
  return {'type':'side_by_side','left':left,'right':right,'left_label':'Before save: fitted state','right_label':'After trusted reload: same fitted state','takeaway':'Preserve fitted preprocessing; do not refit at inference.','lineage':lineage(c,visual=True)}
 if short=='protected_test_comparison':
  policy=data(short,'protected_policy.json')
  # Display fixed policy inputs from registry, not calculated results.
  left=cw('''# Pre-test candidate policy (supplied fixture inputs)
policy = '''+repr(policy)+'''\n# Preserve selected_candidate, preprocessing_identity and threshold.
# Use the same protected observations as the baseline.''',c)
  right=cw('''# Baseline: same protected observations; fixed baseline threshold.
# For each system retain TN, FP, FN, TP.
FPR = FP / (FP + TN) if FP + TN else None
FNR = FN / (FN + TP) if FN + TP else None
# Undefined conditioning groups must be reported.
# With zero correct-prediction cost:
# expected_error_cost = P0 * FPR * cost_FP + P1 * FNR * cost_FN
# Apply fixed probabilities, costs and requirements; report failure, not retuning.''',c)
  return {'type':'side_by_side','left':left,'right':right,'left_label':'Frozen B policy','right_label':'Matched baseline comparison','takeaway':'Same observations; fixed choices and requirements.','lineage':lineage(c,visual=True)}
 code=codes[short]
 # Explicit scenario bindings are copied from registered fixture inputs.
 if short=='training_dataset_version':
  code='import json\nwith open("snapshot_fixture.json") as handle:\n    snapshot_fixture = json.load(handle)\nobject_name = snapshot_fixture["object_name"]\nlocal_path = snapshot_fixture["local_path"]\ndownload_path = snapshot_fixture["download_path"]\n# bucket is the supplied authorized version-enabled bucket.\n'+code
  code += '\nwith open(snapshot_fixture["record_path"], "w") as handle:\n    json.dump(record, handle)\n# After the authorized overwrite, select recorded_generation again.\nselected.download_to_filename(download_path)\nwith open(download_path, "rb") as handle:\n    retrieved_digest = hashlib.sha256(handle.read()).hexdigest()\nassert retrieved_digest == original_digest' 
 elif short=='bounded_managed_training':
  prefix='import json\nwith open("managed_contract.json") as handle:\n    bounds = json.load(handle)\n# Verify the selected input version with authorized storage first.\n# Materialize it at bounds["immutable_key"] if only mutable channel URIs are accepted.\nimmutable_uri = "s3://" + bounds["input_bucket"] + "/" + bounds["immutable_key"]\njob_name = bounds["job_name"]\nresolved_configuration = {\n    "TrainingJobName": job_name,\n    "AlgorithmSpecification": {"TrainingImage": bounds["image"]},\n    "RoleArn": bounds["role"],\n    "InputDataConfig": [{"ChannelName": bounds["channel"], "DataSource": {\n        "S3DataSource": {"S3Uri": immutable_uri}}}],\n    "OutputDataConfig": {"S3OutputPath": bounds["output_uri"]},\n    "ResourceConfig": {"InstanceCount": bounds["max_instance_count"],\n                       "InstanceType": bounds["instance_type"]},\n    "StoppingCondition": {"MaxRuntimeInSeconds": bounds["max_runtime_seconds"]}\n}\n# Use the supplied channel_path and model_output_path inside the container.\n'
  code=prefix+code
  code=code.replace('final = client.describe_training_job', '# After confirming terminal job status, inspect the completed record.\nfinal = client.describe_training_job')
 return cw(code,c,'Instructional workflow; inspect computed identities and results in the workspace, not a typed output.')

recaps={
'mle.tile.052_055':'Keep training state explicit in a committed script. Select and hash the recorded dataset generation. Independently inspect and round-trip the actual environment manifest. Reproduce only after resolving recorded code, data, environment, settings and working directory; verify exit status and captured parameters.',
'mle.tile.056_057':'Verify run-artifact generation and bytes before creating a linked numeric registry version. Retain exact generation and hash metadata. Package the fitted model with fitted preprocessing, pinned dependencies and verified image identity. Reload trusted artifacts only; check prediction and preprocessing preservation and keep secrets in runtime mechanisms.',
'mle.tile.058_058':'Freeze candidate, preprocessing and threshold before protected testing. Compare B and baseline on the same observations using fixed deployment probabilities, costs and requirements. Retain actual-class conditioning counts, report undefined rates or failed requirements, and do not retune from test outcomes.',
'mle.tile.059_059':'Resolve authorized image, role, verified input versions and resource limits before submission. Respect channel and model-output paths. Confirm terminal status and retrieve the expected artifact through authorized storage. Preserve snapshot, code/configuration and run/artifact identities in a round-tripped execution record.'}
next_ideas={
'mle.tile.056_057':'Verify the originating run artifact before creating its registry version.',
'mle.tile.058_058':'Freeze candidate, fitted preprocessing and threshold before protected testing.',
'mle.tile.059_059':'Resolve authorized resources and verified inputs for one bounded managed-training job.'}
# For the out-of-batch next tile, use only its name from the supplied glossary metadata.
names=gloss.get('names',{})
next_ideas['mle.tile.060_063']=names['mle.prediction_schema_validation']+'.'

out={k:plan[k] for k in ['schema_version','path_id','batch_id']};out['kind']='screens_part';out['tiles']=[]
for tile in plan['tiles']:
 title=tile['title'] if tile['title']!=tile['tile_id'] else ('Compare on the Protected Test' if tile['tile_id']=='mle.tile.058_058' else 'Run Bounded Managed Training')
 ot={'tile_id':tile['tile_id'],'title':title,'steps':[],'remediation_steps':[]}
 for s in tile['steps']:
  c=s['concept_ids'][0];bb=B[c];sline={k:copy.deepcopy(s[k]) for k in ['teaching_block_ids','fact_ids','segment_ids','anchors']}
  step={'step_id':s['step_id'],'type':s['type'],'concept_ids':s['concept_ids'],'title':'','lineage':sline}
  if s['type']=='explainer':
   tbs=[t for t in bb['teaching_blocks'] if c+'#'+t['id'] in s['teaching_block_ids']]
   first=tbs[0];step['title']= ('Resolve explicit training state' if first['id']=='tb1' and c=='mle.ml_training_script' else bb['coverage']['learning_objective'].rstrip('.')) if first['id']=='tb1' else first['title']
   step['blocks']=[block for t in tbs for block in tb_blocks(c,t)]
   title_map={
    'ml_training_script':['Make execution explicit','Capture and commit','Verify outside the notebook'],
    'training_dataset_version':['Select the recorded bytes','Test an overwrite','Keep snapshot evidence together','Name is not identity'],
    'training_environment_record':['Record the actual environment','Verify the parsed manifest','Writing is not verification'],
    'experiment_reproduction':['Resolve before rerunning','Use the recorded directories','Check the whole execution context','Filename is not identity'],
    'model_version_registration':['Verify before registration','Re-retrieve the registered artifact'],
    'model_preprocessing_package':['Keep fitted state together','Persist and reload safely','Build, start and inspect','Preserve state and protect secrets','Verify the package boundary'],
    'protected_test_comparison':['Freeze before final testing','Report the matched comparison'],
    'bounded_managed_training':['Bound the authorized job','Verify inputs and completion','Retain the execution record']}
   explainer_index=sum(st['type']=='explainer' and st['concept_ids']==[c] for st in ot['steps'])
   step['title']=title_map[c.split('.')[-1]][explainer_index]
   if s['planned_visual_block_type']:step['blocks'].append(visual(c))
   if s['planned_visual_block_type'] and c=='mle.protected_test_comparison':
    step['blocks'].append({'type':'data_table','asset_ref':{'asset_id':'ds.protected_comparison'},'caption':'Registered fixture comparison: both frozen identities, conditioning counts, fixed policy and outcomes.','lineage':lineage(c,visual=True)})
  elif s['type']=='video':
   step['title']='Direct execution and imports';step['blocks']=[{'type':'media_group','segment_ids':s['segment_ids']}]
  elif s['type'] in ['check','hands_on']:
   step['title']='Verify the distinction' if s['type']=='check' else 'Apply and verify the recorded workflow'
   step['eyebrow']='Quick check' if s['type']=='check' else 'Practice'
   # Each distinct measured fact set receives its own recoverable explanation.
   fs=s['fact_ids'];tbids=[c+'#'+t['id'] for t in bb['teaching_blocks'] if set(t['fact_ids']) & {f.split('#')[-1] for f in fs}]
   blocks=[]
   if s['type']=='check':
    for f in bb['coverage']['required_facts']:
     if c+'#'+f['id'] in fs:
      blocks.append(prose(f['statement'],c,[q for q in tbids if f['id'] in next(t['fact_ids'] for t in bb['teaching_blocks'] if c+'#'+t['id']==q)], [c+'#'+f['id']]))
   else:
    # Mechanism blocks provide compact factual reteaching, avoiding repeated example paragraphs.
    covered=set()
    for t in bb['teaching_blocks']:
     hit=set(c+'#'+f for f in t['fact_ids']) & set(fs)
     if t['purpose']=='mechanism' and hit-covered:
      blocks.extend(tb_blocks(c,t));covered |=hit
   contrasts={
    'ml_training_script':'A saved file is not a committed revision; a successful start is not verified clean-process behavior.',
    'training_dataset_version':'The same latest name can contain different bytes; select the recorded generation and check its digest.',
    'training_environment_record':'A saved manifest is not a verified manifest; compare parsed values with independent observations.',
    'experiment_reproduction':'A familiar script name is not the recorded execution context; verify identities, settings and working directory.',
    'model_version_registration':'A mutable overwrite is not a newly approved numeric registry version.',
    'model_preprocessing_package':'Reload fitted preprocessing; do not refit it on inference inputs.',
    'protected_test_comparison':'Report test failure rather than selecting a new candidate or threshold.',
    'bounded_managed_training':'Submission is not terminal completion; a channel name is not verified input identity.'}
   contrast=contrasts[c.split('.')[-1]]
   if s['type']=='check' and c=='mle.ml_training_script':contrast='Saving the script is not committing it: stage, commit and retain the resulting revision.'
   blocks.append(prose(contrast,c,tbids,fs,'misconception'))
   rid=tile['tile_id']+'.r'+str(len(ot['remediation_steps'])+1).zfill(2)
   ot['remediation_steps'].append({'step_id':rid,'type':'remediation','concept_ids':[c],'title':'Review: '+('identity contrast' if s['type']=='check' else 'verified workflow'),'blocks':blocks,'lineage':lineage(c,tbids,fs)})
  else:
   step['title']='Keep these boundaries';facts=[c2+'#'+f['id'] for c2 in tile['concept_ids'] for f in B[c2]['coverage']['required_facts']];tbs=[c2+'#'+t['id'] for c2 in tile['concept_ids'] for t in B[c2]['teaching_blocks']]
   step['blocks']=[{'type':'prose','role':'takeaway','text':recaps[tile['tile_id']],'lineage':{'concept_ids':tile['concept_ids'],'teaching_block_ids':tbs,'fact_ids':facts}}, {'type':'up_next','title':'Up next','text':next_ideas[tile['next_tile_id']]}]
  ot['steps'].append(step)
 out['tiles'].append(ot)
(P/'screens.json').write_text(json.dumps(out,indent=2)+'\n')
print('Written',len(out['tiles']),'tiles;',sum(len(t['steps']) for t in out['tiles']),'planned steps;',sum(len(t['remediation_steps']) for t in out['tiles']),'remediations')
