import json, re, copy
from pathlib import Path
B=Path('batches/final_batch_mle.region.reproducible_release')
plan=json.loads((B/'tile_plans.json').read_text())
gloss=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
registry=json.loads((B/'scenario_asset_registry.json').read_text())
concepts={x['context']['concept_id']:x for x in gloss['bundles']}
rem_voice=json.loads((B/'scratch/remediation_voice.json').read_text())
assets={a['asset_id']:a for a in registry['assets']}
def file_text(cid,path):
 return next(f['content'] for f in assets['ws.'+cid.split('.')[-1]]['files'] if f['path']==path)
def contract(cid,path):return json.loads(file_text(cid,path))
# Screen voice keyed to source teaching blocks; lineage is always derived below.
voice={
'ml_training_script':[
('Leave notebook state behind','Move the order-training task into a saved script. Its entry point runs directly, while ordinary imports must not launch training.'),
('Make the entry point explicit','Guard the executable call with if __name__ == "__main__":. Define explicit training parameters and resolve defaults and keyword overrides before training. Decode the declared configuration with json.load, then map its fields to those arguments.'),
('Run and round-trip','Run python training_script.py and compare recorded settings and outputs with the supplied notebook behavior. A caller can use subprocess.run(["python", script_path], check=True), which raises on a nonzero exit. Save structured records with json.dump(record, handle); recover their values with json.load(handle). JSON text itself is not a dictionary.'),
('Inspect and commit','Call the entry function with defaults, then explicit keyword overrides. Keep task state in parameters or local values, not notebook globals. Emit resolved parameters and validation results with f-strings, such as f"{parameter_name}={resolved_value}". Save the repository script, stage it with git add SCRIPT_PATH, commit with git commit and retain the resulting revision.'),
('Capture a clean run','From a clean shell, run python training_script.py > capture.log 2>&1. Inspect the captured resolved parameters and result.'),
('Two calls, one explicit contract','For the supplied order workflow, compare a default call with a keyword override. Map decoded JSON to the same arguments; round-trip the configuration. Guard direct execution, save and commit the script, and retain its revision. Run a clean subprocess with checked exit status and capture both output streams. Compare resolved parameters and validation output with notebook behavior: starting successfully does not prove forgotten notebook globals were removed.'),
('Decode and resolve','Decode JSON before treating it as a dictionary. Do not rely on notebook globals or print defaults in place of resolved keyword overrides.')],
 'training_dataset_version':[
('A name can stay while bytes change','The dataset path can survive an overwrite. Reproduction needs the recorded generation and verified content identity, not merely a name called latest.'),
('Select the recorded generation','A mutable object name can point to overwritten contents. Object Versioning retains noncurrent versions for explicit selection. Retrieve the Google Cloud Storage snapshot with bucket.blob(object_name, generation=recorded_generation).download_to_filename(local_path), not the current object. Confirm that object/version exists with the authorized client before recording it as available.'),
('Bind the record to actual bytes','Compute hashlib.sha256(data_bytes).hexdigest() from actual bytes and compare it with the expected content identity. Keep object name, generation and observed digest together in the local snapshot record. Upload to the version-enabled bucket with bucket.blob(object_name).upload_from_filename(local_path), then inspect and record the created generation.'),
('Verify across an overwrite','Read the local dataset in binary mode with open(path, "rb") and update SHA-256 from those bytes before recording upload identity. In the test bucket, overwrite only mutable latest; download the original recorded generation again and compare its digest with the original snapshot digest.'),
('Follow the same snapshot twice','Upload the supplied order dataset and record its created generation and local-byte digest. Explicitly select that generation, confirm it exists, download it and compare its bytes with the expected digest. Change only mutable latest in the authorized overwrite fixture; retrieve the original generation again and verify the digest still matches. Keep the object name, generation and digest together: object family, selected version and checked content are distinct.||Check downloaded content rather than assuming the version-qualified request returned expected bytes. Compare the local pre-upload digest with the later download digest. Keep the generation even when original and latest share a name. This verifies the recorded fixture; it does not make mutable names intrinsically safe for reproduction.'),
('A path is not identity','A mutable name is not immutable data identity. A recorded digest alone does not prove the downloaded bytes belong to the intended snapshot.')],
 'training_environment_record':[
('Record the environment that ran','Capture the actual execution environment. Remembered dependencies and typed commit labels are not independent evidence of the Python runtime and repository revision used.'),
('Inspect revision and dependencies','Read the actual repository revision with git rev-parse --verify HEAD. Collect installed pins with python -m pip freeze; its package==version entries can be installed with pip install -r. Use imported runtime/environment facilities to capture execution context alongside the recorded runtime identity, revision and dependencies.'),
('Verify the saved manifest','Import json. Write the manifest dictionary with json.dump and read it back with json.load, using explicit with open handles in "w" and "r" modes with encoding="utf-8". Compare parsed revision, dependency mapping and runtime identity with independently inspected values. Reject a mismatch.'),
('Capture the interpreter','Import sys and record sys.version and sys.executable: actual interpreter details belong alongside the supplied runtime identity.'),
('Compare the parsed record, not memory','Inspect HEAD and pip freeze, and capture sys.version, sys.executable and the supplied runtime identity. Save the dictionary to the text manifest and parse it back. Compare parsed revision, dependency mapping and runtime identity with independent observations. If the record differs from HEAD, reject the match; do not change observations to fit it. Install pinned dependencies with pip install -r where needed. Retain the saved manifest and verified context for reproduction.||Verification concerns the file a later run will read, not just the dictionary before serialization. Compare parsed dependencies with freeze output, revision with HEAD, and Python/runtime fields with the actual process. Interpreter path and version complement the environment identity; neither substitutes for it. Resolve mismatches instead of declaring an inaccurate record verified.'),
('Writing is not verification','Manifest creation alone is not verification. Runtime details and dependency pins must be observed; a mismatched parsed record is not accurate.')],
 'experiment_reproduction':[
('Resolve the recorded experiment','Resolve recorded code, data, environment and settings first. Today’s working tree and current dataset can describe another experiment despite a familiar run name.'),
('Check identities before execution','Retrieve the recorded revision, snapshot, environment and resolved settings. Check out the recorded local commit and verify HEAD rather than running a changed tree. Download the recorded dataset generation and verify its identity; do not resolve mutable latest.'),
('Pass state into a clean process','Use the recorded Python/dependency environment and install pinned requirements where needed. Give the execution function defaults and explicit keyword overrides, passing resolved run state through parameters. Run the script in a clean subprocess from the recorded working directory, check exit status and capture output.'),
('Resolve paths from the right directory','Navigate the referenced repository and artifact directories before resolving relative script, dataset and configuration paths. Redirect with > capture.log 2>&1 and inspect the file. A pipe sends one command’s output to another command’s input; it is not this two-stream capture.'),
('Rerun the recorded order task','Resolve the recorded commit, generation and pinned environment. Verify HEAD and downloaded snapshot identity. Pass resolved defaults and overrides through execution-function parameters. Navigate recorded directories before resolving relative paths. Launch a clean subprocess with captured output and checked exit status, then inspect the result. In the failure fixture, distinguish changed latest or a different working directory from the recorded context. A pipe connects commands; redirection saves the declared streams.||Also compare captured resolved parameters with the run record. Successful exit alone can hide a wrong dataset or default. Relative paths depend on the actual working directory, so navigate explicitly before invoking the script. Recorded code and environment govern the implementation; the verified snapshot governs inputs. Check these separately rather than relying on memory of a notebook session.'),
('Familiar names can hide a different run','A familiar script filename is not reproduction identity. Changed code, mutable data or unresolved paths can change the experiment.')],
 'model_version_registration':[
('Verify before registering','A registry version must point to the verified originating run artifact. Resolve its exact stored generation and check the bytes against the run’s expected hash first.'),
('Resolve the artifact, not latest','Retrieve the run’s artifact record, expected hash and immutable object version. Download with bucket.blob(key, generation=recorded_generation).download_to_filename(path), not the current object at key. Hash downloaded bytes with SHA-256 and reject a mismatch before registration.'),
('Retain the version and its origin','Require the supplied model name to exist; create_registered_model(name) supports the declared new-name path. Call create_model_version(name=name, source=version_qualified_source, run_id=run_id) and retain its returned numeric version. Save exact object version and hash with set_model_version_tag. Retrieve the version with get_model_version(name, version) and its linked originating run; verify their recorded identities.'),
('Verify after mutable latest changes','Import MlflowClient from mlflow and construct the client for version creation, retrieval and tags. In the authorized test bucket, overwrite only latest, then retrieve the registered generation again and verify its registered hash. Return one keyed registration verdict. An overwrite is not a newly approved registry version.'),
('Bind run, version and artifact','The run record and mutable latest may identify different generations. Retrieve the recorded one and verify its hash before creating a registry version. Use the supplied model name, creating it only on the declared new-name path. Retain numeric version, version-qualified source, run link, generation and hash tags. Retrieve the version and linked run to compare identities. After the authorized latest overwrite, retrieve and verify the registered generation again. Return a keyed verdict binding these identities, not a verdict that approves the overwrite.'),
('A number cannot repair a mutable source','A numeric registry version does not verify a mutable source. Check exact generation and hash; an object overwrite is not an approved version creation.')],
 'model_preprocessing_package':[
('Carry fitted state together','Package the fitted model with its fitted preprocessor. Loading only weights or refitting preprocessing can run successfully while changing the intended prediction representation.'),
('Persist trusted fitted state and build inputs','Import pickle. In the recorded version-tied path, use a binary "wb" handle and pickle.dump({"model": model, "preprocessor": preprocessor}, handle, protocol=5). Reload only trusted, verified artifacts in the compatible pinned environment: use "rb", pickle.load(handle) and the corresponding dictionary keys. Untrusted pickle loading can execute arbitrary code.||Use Dockerfile FROM for the compatible Python image, WORKDIR /app, COPY requirements.txt ./ and RUN pip install --no-cache-dir -r requirements.txt. COPY the declared package and serving source from the build context to their /app paths. Set CMD to the supplied serving command and argument as a JSON array; replace placeholders with the declared package, dependencies and entry point.'),
('Build the intended context and run the image','Build with docker build -t IMAGE:TAG CONTEXT. Include the Dockerfile (or select it with -f) and every COPY source; check .dockerignore exclusions. Retain immutable image identity as well as its tag. Predictions must apply fitted training preprocessing before the model, without refitting. Start with docker run --name NAME -p HOST_PORT:CONTAINER_PORT --env KEY=VALUE IMAGE using declared ports and nonsecret settings.'),
('Inspect identity, state and logs','Use docker container inspect NAME to check image identity and State. Inspect captured output and errors with docker container logs NAME for initialization or execution failures. Never put secrets in Dockerfile ARG or ENV: they persist in the image or metadata.'),
('Dependencies are files; secrets are runtime inputs','Supply sensitive values through the runtime secret mechanism, not literal Compose values. Save/reload model and preprocessor through binary handles, and write/read the pinned dependency manifest through text handles. Record inference pins in the package requirements manifest and install it in the serving image.'),
('Check predictions and fitted parameters separately','Assert pre-save and container-reloaded predictions agree on the same fixed inputs under declared tolerances. Separately verify fitted preprocessing parameters. Write assert predicates for declared valid, boundary and failure cases; a false predicate raises AssertionError in ordinary non-optimized execution.'),
('Trace the package through the container','Save the fitted pair in the trusted version-tied package using binary handles; retain inference pins in the text manifest. Build the context with package, requirements and serving source, and record immutable image identity. Start the declared image with its port and nonsecret settings; inspect identity, state and logs. Compare pre-save and container-reloaded predictions on fixed orders under declared tolerances, and check preprocessing parameters separately. Reject untrusted pickle despite familiar filenames. Keep credentials in the runtime mechanism, outside Dockerfile and Compose literals.'),
('Packaging does not authorize refitting','Do not refit preprocessing or embed credentials. A matching tag alone does not verify image identity. Pickle packages need trusted, verified provenance and a compatible pinned environment.')],
 'protected_test_comparison':[
('Freeze before protected testing','Fix candidate, fitted preprocessing and threshold before protected testing. Report disappointment; do not let test outcomes choose a replacement.'),
('Compare the same protected observations','After freezing the selected candidate, preprocessing and threshold, predict the same protected observations with candidate and baseline. Compare precommitted predictive quantities on that cohort. Test results must not select a new candidate or threshold. Use fixed deployment probabilities, error costs and operating requirements; report failure rather than retuning.'),
('Condition error rates on actual classes','For binary counts, FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) conditions on actual positives. An empty conditioning group has no defined rate. With zero cost for correct predictions and supplied deployment probabilities, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.'),
('Report the frozen comparison, even when it fails','Validation selected B and its threshold. Use B and baseline on the same protected orders, even if this cohort’s observed class mix differs. Keep fixed deployment probabilities and costs instead of changing inputs to make B pass. Retain actual-class conditioning counts and check precommitted quality and operating requirements. Report B’s failure. Adjusting the threshold from these outcomes would let protected observations select the system: this is a final matched comparison, not another selection round.||Freeze choices before observing outcomes: model identity, fitted preprocessing, threshold, metric inputs and requirements. Observed test conditioning counts and supplied deployment probabilities have different roles; retain both. Explicitly report undefined required quantities or failed requirements, without turning final testing into more tuning.'),
('Failure is not a tuning invitation','Protected testing is not another tuning round. Failure does not authorize switching candidate, refitting preprocessing or searching for a better threshold on those observations.')],
 'bounded_managed_training':[
('Submission starts a bounded job','On the existing platform, bind one authorized job to resolved input versions, resource bounds and the expected artifact. Submission is not proof of successful training.'),
('Resolve the bounded request','SageMaker CreateTrainingJob specifies TrainingJobName, AlgorithmSpecification, RoleArn, input/output configuration, ResourceConfig and StoppingCondition. Use the supplied TrainingImage, authorized instance count/type and MaxRuntimeInSeconds. Give InputDataConfig version-resolved inputs and OutputDataConfig the output S3 location; the role must be authorized for those resources.'),
('Honor container paths and retain identities','Channels are exposed under /opt/ml/input/data/CHANNEL; write model output under /opt/ml/model for upload. Inspect final job status and artifact location, checking recorded configuration against the intended artifact. Keep dataset snapshot, code/configuration and resulting run/artifact identities in the execution record.'),
('Submit, describe and round-trip','Import boto3 and construct boto3.client("sagemaker"). Submit with client.create_training_job(**resolved_configuration). Describe by TrainingJobName and inspect TrainingJobStatus, FailureReason when present, and ModelArtifacts.S3ModelArtifacts. Save structured configuration or records with json.dump and recover them with json.load; JSON text is not a dictionary.'),
('Verify inputs and terminal output','Verify every selected input version before submission. If the API accepts only mutable channel URIs, materialize the selected version at a controlled immutable location; do not invent a version parameter. Retrieve the output with the authorized storage client and verify its reference against the completed job record. Managed training creates job resources and releases them after termination. Confirm terminal status; submission alone does not end compute use.'),
('Follow one job to its artifact','Resolve the supplied image, job name, role, channels, output location, instance bounds and runtime before submission. Verify selected input versions. When channel URIs cannot select versions, materialize the chosen version at the controlled immutable location. Read channels beneath /opt/ml/input/data and write the model beneath /opt/ml/model. Inspect terminal status, any failure reason and artifact location. Retrieve the artifact with the authorized client and compare its reference with the completed job record. Retain snapshot, code/configuration and run/artifact identities together.'),
('A request is not completion','Submission is not completion, and a name is not verified input identity. Resources are released after termination; confirm terminal status before concluding compute use has ended.')]
}

def lineage(cid,tbs,facts,anchors=None):
 d={'concept_ids':[cid], 'teaching_block_ids':tbs, 'fact_ids':facts}
 if anchors:d['anchors']=anchors
 return d

def prose(text,lin,role='mechanism'):
 # Deliberate paragraphs first; split only on sentence boundaries for short standalone blocks.
 result=[]
 for para in text.split('||'):
  if len(para.split())<=90:chunks=[para]
  else:
   chunks=[]; chunk=''
   for sent in re.split(r'(?<=[.!?])\s+(?=[A-Z])',para):
    if chunk and len((chunk+' '+sent).split())>90:chunks.append(chunk);chunk=''
    chunk=(chunk+' '+sent).strip()
   if chunk:chunks.append(chunk)
  for chunk in chunks:
   assert len(chunk.split())<=90,(len(chunk.split()),chunk)
   result.append({'type':'prose','text':chunk,'role':role,'lineage':copy.deepcopy(lin)})
 return result

def code(text,lin,language='python'):
 return {'type':'code_walkthrough','language':language,'code':text.strip(),'reveal':'all','lineage':copy.deepcopy(lin)}

# Visual code is instructional input, not an executed result. Runtime observations
# (hashes, revisions, pins, job responses, predictions) are never typed here.
def visual(cid,lin):
 short=cid.split('.')[-1]
 lin=copy.deepcopy(lin);lin['anchors']=[cid+'#visual']
 if short=='ml_training_script':
  # Derive default argument literals from the registered function, not memory.
  source=file_text(cid,'fixture_workflow.py')
  signature=re.search(r'def supplied_workflow\((.*?)\):',source).group(1)
  return [code('''import json
from fixture_workflow import supplied_workflow

def train('''+signature+'''):
    result = supplied_workflow(dataset_path=dataset_path, threshold=threshold)
    for parameter_name, resolved_value in result['resolved_parameters'].items():
        print(f"{parameter_name}={resolved_value}")
    print(f"validation_accuracy={result['validation_accuracy']}")
    return result

# Direct execution runs the calls; ordinary import does not.
if __name__ == '__main__':
    default_result = train()
    with open('configuration.json', encoding='utf-8') as handle:
        configuration = json.load(handle)
    override_result = train(**configuration)
''',lin),code('''python training_script.py > capture.log 2>&1
cat capture.log
git add training_script.py
git commit -m "Save explicit training entry point"
git rev-parse --verify HEAD
''',lin,'bash')]
 if short=='training_dataset_version':
  return [code('''import hashlib, json
from pathlib import Path
from google.cloud import storage
with open('snapshot_fixture.json', encoding='utf-8') as handle:
    supplied = json.load(handle)
bucket = storage.Client().bucket(supplied['bucket_name'])
with open(supplied['local_path'], 'rb') as handle:
    original_digest = hashlib.sha256(handle.read()).hexdigest()
blob = bucket.blob(supplied['object_name'])
blob.upload_from_filename(supplied['local_path'])
record = {'object_name': supplied['object_name'],
          'generation': blob.generation, 'digest': original_digest}
with open(supplied['record_path'], 'w', encoding='utf-8') as handle:
    json.dump(record, handle)
selected = bucket.blob(record['object_name'], generation=record['generation'])
assert selected.exists()
Path(supplied['download_path']).parent.mkdir(parents=True, exist_ok=True)
selected.download_to_filename(supplied['download_path'])
with open(supplied['download_path'], 'rb') as handle:
    retrieved_digest = hashlib.sha256(handle.read()).hexdigest()
assert retrieved_digest == record['digest']
# Authorized overwrite test: change only mutable latest, then select original again.
bucket.blob(record['object_name']).upload_from_filename('changed_latest.csv')
selected.download_to_filename(supplied['download_path'])
with open(supplied['download_path'], 'rb') as handle:
    after_digest = hashlib.sha256(handle.read()).hexdigest()
assert after_digest == record['digest']
''',lin)]
 if short=='training_environment_record':
  return [code('''import json, subprocess, sys
revision = subprocess.run(['git', 'rev-parse', '--verify', 'HEAD'],
                          check=True, capture_output=True, text=True).stdout.strip()
freeze = subprocess.run([sys.executable, '-m', 'pip', 'freeze'],
                        check=True, capture_output=True, text=True).stdout
pins = dict(line.split('==', 1) for line in freeze.splitlines() if '==' in line)
# Symbolic runtime_identity and manifest_path bind the supplied contract.
# Retain runtime_identity alongside observed fields.
manifest = {'revision': revision, 'dependencies': pins,
            'runtime_identity': runtime_identity,
            'sys_version': sys.version, 'sys_executable': sys.executable}
with open(manifest_path, 'w', encoding='utf-8') as handle:
    json.dump(manifest, handle)
with open(manifest_path, 'r', encoding='utf-8') as handle:
    parsed = json.load(handle)
# independent_observations comes from fresh repository/runtime inspection.
for field in manifest:
    assert parsed[field] == independent_observations[field]
''',lin)]
 if short=='experiment_reproduction':
  return [code('''import json, os, subprocess
# Outline: run_record fields below bind the verified recorded execution context.

def execute_recorded(run_record, settings=None, **keyword_overrides):
    resolved = dict(run_record['settings'] if settings is None else settings)
    resolved.update(keyword_overrides)
    # First retrieve the record, checkout its commit and verify HEAD.
    # Verify the recorded dataset generation and use the pinned environment.
    # Resolve relative paths after navigating the recorded directories.
    os.chdir(run_record['working_directory'])
    with open(run_record['configuration_path'], 'w', encoding='utf-8') as handle:
        json.dump(resolved, handle)
    completed = subprocess.run(
        [run_record['python_executable'], run_record['script_path']],
        check=True, capture_output=True, text=True)
    # The script reads configuration mapped from resolved parameters.
    # Inspect captured parameters and outcome against the record/tolerance.
    return {'resolved': resolved, 'returncode': completed.returncode,
            'stdout': completed.stdout, 'stderr': completed.stderr}
''',lin),code('''git checkout RECORDED_COMMIT
git rev-parse --verify HEAD
cd RECORDED_WORKING_DIRECTORY
python -m pip install -r RECORDED_REQUIREMENTS
python RECORDED_SCRIPT > capture.log 2>&1
cat capture.log
''',lin,'bash')]
 if short=='model_version_registration':
  return [code('''import hashlib
from mlflow import MlflowClient
import json
from pathlib import Path
from google.cloud import storage
with open('run_artifact_record.json', encoding='utf-8') as handle:
    record = json.load(handle)
bucket = storage.Client().bucket(record['bucket_name'])
model_name = record['model_name']
version_qualified_source = record['version_qualified_source']
artifact_path = record['local_path']
Path(artifact_path).parent.mkdir(parents=True, exist_ok=True)
selected = bucket.blob(record['key'], generation=record['generation'])
selected.download_to_filename(artifact_path)
with open(artifact_path, 'rb') as handle:
    observed_hash = hashlib.sha256(handle.read()).hexdigest()
if observed_hash != record['expected_hash']:
    raise ValueError('Artifact mismatch: do not create a version')
client = MlflowClient()
# Require the registered name; only the declared new-name path creates it.
version = client.create_model_version(name=model_name,
    source=version_qualified_source, run_id=record['run_id'])
client.set_model_version_tag(model_name, version.version, 'generation',
                             str(record['generation']))
client.set_model_version_tag(model_name, version.version, 'sha256', observed_hash)
retrieved = client.get_model_version(model_name, version.version)
originating_run = client.get_run(retrieved.run_id)
# Compare retrieved source, tags and run link with the verified record.
# After authorized latest overwrite, re-download selected and verify hash again.
''',lin)]
 if short=='model_preprocessing_package':
  pkg=contract(cid,'package_contract.json')
  left=code('''import pickle
# Supplied fitted objects; package_path is the recorded version-tied path.
with open(package_path, 'wb') as handle:
    pickle.dump({'model': model, 'preprocessor': preprocessor},
                handle, protocol=5)
# Only load a trusted, verified artifact in the compatible pinned environment.
with open(package_path, 'rb') as handle:
    reloaded = pickle.load(handle)
predictions = reloaded['model'].predict(
    reloaded['preprocessor'].transform(fixed_inputs))
# Compare with pre-save predictions under declared tolerances.
# Separately check preserved fitted preprocessing parameters.
''',lin)
  # Build configuration literals come from the registered contract.
  docker='\n'.join(['FROM '+pkg['compatible_python_image'],'WORKDIR /app','COPY '+pkg['manifest_path']+' ./','RUN pip install --no-cache-dir -r '+pkg['manifest_path'],'COPY package/ ./package/','COPY '+pkg['serving_source']+' ./','COPY fixture_workflow.py package_contract.json ./','CMD '+json.dumps(pkg['serving_command'])])
  # bash language is used for a shell that writes the Dockerfile, then executes builds.
  right=code("cat > Dockerfile <<'DOCKERFILE'\n"+docker+'\nDOCKERFILE\n'+
    'docker build -t '+pkg['image_tag']+' .\n'+
    'docker run --name '+pkg['container_name']+' -p '+str(pkg['host_port'])+':'+str(pkg['container_port'])+' --env '+next(iter(pkg['nonsecret_settings']))+'='+next(iter(pkg['nonsecret_settings'].values()))+' '+pkg['image_tag']+'\n'+
    'docker container inspect '+pkg['container_name']+'\n'+'docker container logs '+pkg['container_name'],lin,'bash')
  return [{'type':'side_by_side','left':left,'right':right,'left_label':'Trusted fitted pair','right_label':'Declared serving image','takeaway':'Preserve fitted state; verify the reloaded image.', 'lineage':lin}]
 if short=='protected_test_comparison':
  ds=assets['ds.protected_comparison']
  names=[c['name'] for c in ds['columns']]
  shared=[names[0],'model_identity','preprocessing_identity','threshold','cohort_size','TN','FP','FN','TP']
  outcomes=[n for n in names if n not in shared]
  def table(columns,caption):return {'type':'data_table','asset_ref':{'asset_id':ds['asset_id'],'columns':columns},'caption':caption,'lineage':copy.deepcopy(lin)}
  return [{'type':'side_by_side','left':table(shared,'Frozen systems and actual-class counts'),'right':table([names[0],'model_identity']+outcomes,'Fixed comparison inputs and requirement outcomes'), 'left_label':'Same protected cohort','right_label':'Final comparison','takeaway':'Report failed or undefined outcomes without retuning.', 'lineage':lin}]
 if short=='bounded_managed_training':
  return [code('''import boto3, json
with open('managed_contract.json', encoding='utf-8') as handle:
    contract = json.load(handle)
storage_client = boto3.client('s3')
# Verify the selected version before creating a controlled immutable input copy.
selected = storage_client.get_object(Bucket=contract['input_bucket'],
    Key=contract['input_key'], VersionId=contract['input_version'])
input_bytes = selected['Body'].read()
import hashlib
assert hashlib.sha256(input_bytes).hexdigest() == contract['dataset_snapshot']['expected_hash']
storage_client.copy_object(Bucket=contract['input_bucket'],
    Key=contract['immutable_key'], CopySource={'Bucket': contract['input_bucket'],
    'Key': contract['input_key'], 'VersionId': contract['input_version']})
resolved_configuration = {
 'TrainingJobName': contract['job_name'],
 'AlgorithmSpecification': {'TrainingImage': contract['image'],
                            'TrainingInputMode': 'File'},
 'RoleArn': contract['role'],
 'InputDataConfig': [{'ChannelName': contract['channel'], 'DataSource': {
   'S3DataSource': {'S3DataType': 'S3Prefix', 'S3DataDistributionType': 'FullyReplicated',
     'S3Uri': 's3://' + contract['input_bucket'] + '/' + contract['immutable_key']}}}],
 'OutputDataConfig': {'S3OutputPath': contract['output_uri']},
 'ResourceConfig': {'InstanceCount': contract['max_instance_count'],
    'InstanceType': contract['instance_type']},
 'StoppingCondition': {'MaxRuntimeInSeconds': contract['max_runtime_seconds']}}
# The supplied container reads contract['channel_path'], writes contract['model_output_path'].
client = boto3.client('sagemaker')
response = client.create_training_job(**resolved_configuration)
description = client.describe_training_job(TrainingJobName=contract['job_name'])
# A still-running status needs further observation, not a completion verdict.
if description['TrainingJobStatus'] != 'Completed':
    raise ValueError(description.get('FailureReason', description['TrainingJobStatus']))
artifact_reference = description['ModelArtifacts']['S3ModelArtifacts']
assert artifact_reference == contract['artifact_uri']
# Parse this verified S3 reference, then retrieve through authorized storage.
from urllib.parse import urlparse
location = urlparse(artifact_reference)
storage_client.download_file(location.netloc, location.path.lstrip('/'), 'downloads/model.tar.gz')
record = {'dataset_snapshot': contract['dataset_snapshot'],
          'code_reference': contract['code_reference'], 'configuration': resolved_configuration,
          'submission': response, 'description': description,
          'retrieved_artifact_reference': artifact_reference}
with open('execution_record.json', 'w', encoding='utf-8') as handle:
    json.dump(record, handle)
with open('execution_record.json', 'r', encoding='utf-8') as handle:
    parsed = json.load(handle)
''',lin)]
 raise ValueError(cid)

titles={
'mle.tile.058_058':'Compare the Frozen System on Protected Orders',
'mle.tile.059_059':'Run One Bounded Managed Training Job'}
recaps={
'mle.tile.052_055':'Use a committed, guarded training script with explicit resolved state and inspected clean-process output. Identify data by recorded generation and verified bytes. Round-trip the environment manifest and compare it with independent observations. Reproduction resolves code, snapshot, environment, settings and working directory before execution; a familiar name or successful exit is not enough.',
'mle.tile.056_057':'Verify exact run artifact generation and hash before creating a linked numeric registry version. Retrieve the version and run to check identities; mutable overwrite is not approval. Package trusted fitted model and preprocessing together with pinned dependencies. Verify immutable image identity, state, logs, fixed-input predictions and preserved preprocessing. Keep secrets in the runtime mechanism.',
'mle.tile.058_058':'Freeze candidate, fitted preprocessing and threshold before protected testing. Compare B and baseline on the same observations with fixed probabilities, costs and requirements. FPR conditions on negatives; FNR on positives. Empty groups leave rates undefined. Report failed or undefined requirements without selecting a new system from test outcomes.',
'mle.tile.059_059':'Bind one authorized training job to verified input versions, code/configuration and resource bounds. Respect channel and model-output paths. Submission is not completion: inspect terminal status, retrieve the output and verify its reference against the completed job record. Round-trip the structured execution record and retain its identities.'}
next_text={
'mle.tile.052_055':'Next: verify the originating run’s exact artifact before creating a registry version.',
'mle.tile.056_057':'Next: freeze candidate, fitted preprocessing and threshold before protected testing.',
'mle.tile.058_058':'Next: resolve one authorized managed training request with bounded resources.',
'mle.tile.059_059':'Next: validate prediction request and response schemas.'}
contrasts={
'ml_training_script':'Contrast: a saved, committed revision identifies the script; an unsaved notebook edit does not. A clean run must use resolved local/parameter state, not notebook globals.',
 'training_dataset_version':'Contrast: the recorded generation selects the original order snapshot; mutable latest can select changed bytes. Verify the download, not just the name.',
 'training_environment_record':'Contrast: compare the parsed manifest with independently observed HEAD, pins and runtime; writing the file alone is not verification.',
 'experiment_reproduction':'Contrast: recorded commit, snapshot, environment and settings define the rerun; today’s tree and latest dataset can define another experiment.',
 'model_version_registration':'Contrast: a verified, version-qualified run artifact supports registration; a mutable overwrite does not create an approved registry version.',
 'model_preprocessing_package':'Contrast: reload the trusted fitted pair on fixed orders; refitting preprocessing or checking only an image tag does not verify the package.',
 'protected_test_comparison':'Contrast: report B’s protected-test failure with fixed inputs; changing threshold from those results is another tuning round.',
 'bounded_managed_training':'Contrast: a verified input and terminal job/artifact record support the verdict; a submitted request or mutable input name alone does not.'}

out={k:plan[k] for k in ['schema_version','path_id','batch_id']};out['kind']='screens_part';out['tiles']=[]
for pt in plan['tiles']:
 tile={'tile_id':pt['tile_id'],'title':titles.get(pt['tile_id'],pt['title']),'steps':[],'remediation_steps':[]}
 seen=set()
 for ps in pt['steps']:
  s={k:copy.deepcopy(ps[k]) for k in ['step_id','type','concept_ids']}
  s['lineage']={'concept_ids':ps['concept_ids'], 'teaching_block_ids':ps['teaching_block_ids'], 'fact_ids':ps['fact_ids']}
  if ps['anchors']:s['lineage']['anchors']=ps['anchors']
  cid=ps['concept_ids'][0]; short=cid.split('.')[-1]
  if ps['type']=='explainer':
   s['blocks']=[]
   for tbid in ps['teaching_block_ids']:
    tc,local=tbid.split('#'); tb=next(t for t in concepts[tc]['teaching_blocks'] if t['id']==local)
    title,text=voice[tc.split('.')[-1]][int(local[2:])-1]
    if not s.get('title'):s['title']=title
    bl=lineage(tc,[tbid],[tc+'#'+fid for fid in tb['fact_ids']])
    s['blocks']+=prose(text,bl,'intro' if tb['purpose']=='intro' else 'mechanism')
   if ps['planned_visual_block_type']:s['blocks']+=visual(cid,s['lineage'])
  elif ps['type']=='video':
   s['title']='Watch the entry-point walkthrough'
   s['blocks']=[{'type':'media_group','segment_ids':ps['segment_ids']}]
  elif ps['type'] in ['check','hands_on']:
   s['title']=('Check: ' if ps['type']=='check' else 'Practice: ')+{
    'ml_training_script':'explicit, saved training execution',
    'training_dataset_version':'recorded order snapshot identity',
    'training_environment_record':'observed environment identity',
    'experiment_reproduction':'the recorded order experiment',
    'model_version_registration':'verified artifact registration',
    'model_preprocessing_package':'trusted fitted-state packaging',
    'protected_test_comparison':'the frozen protected comparison',
    'bounded_managed_training':'one authorized bounded job'}[short]
   # Each distinct measured fact set receives its own re-teaching destination.
   key=(cid,tuple(ps['fact_ids']))
   if key not in seen:
    seen.add(key)
    qualified=ps['fact_ids']
    # Source facts supply exact tested rules, never inferred answer claims.
    source_facts=concepts[cid]['coverage']['required_facts']
    assert len(source_facts)==len(rem_voice[short])
    fact_lookup={cid+'#'+f['id']:text for f,text in zip(source_facts,rem_voice[short])}
    tbs=[cid+'#'+tb['id'] for tb in concepts[cid]['teaching_blocks'] if any(cid+'#'+f in qualified for f in tb['fact_ids'])]
    lin=lineage(cid,tbs,qualified)
    blocks=prose(contrasts[short],lin,'misconception')
    # Keep one factual rule per short block to support targeted review.
    for f in qualified:blocks+=prose(fact_lookup[f],lineage(cid,[tb for tb in tbs if f.split('#')[1] in next(x for x in concepts[cid]['teaching_blocks'] if cid+'#'+x['id']==tb)['fact_ids']],[f]),'mechanism')
    tile['remediation_steps'].append({'step_id':pt['tile_id']+'.r'+str(len(tile['remediation_steps'])+1).zfill(2), 'type':'remediation','title':'Review: '+s['title'].split(': ',1)[1], 'concept_ids':[cid], 'lineage':lin,'blocks':blocks})
  elif ps['type']=='recap':
   s['title']='Keep the identities and boundaries clear'
   all_tbs=[c+'#'+tb['id'] for c in pt['concept_ids'] for tb in concepts[c]['teaching_blocks']]
   all_facts=[c+'#'+f['id'] for c in pt['concept_ids'] for f in concepts[c]['coverage']['required_facts']]
   lin={'concept_ids':pt['concept_ids'],'teaching_block_ids':all_tbs,'fact_ids':all_facts}
   s['blocks']=prose(recaps[pt['tile_id']],lin,'takeaway')+[{'type':'up_next','title':'Up next','text':next_text[pt['tile_id']]}]
  tile['steps'].append(s)
 out['tiles'].append(tile)

# The generator checklist: derived ids/lineage, plan fidelity, no output fields,
# no unregistered table columns, no prose without lineage, budget and visual tags.
def walk(blocks):
 for b in blocks:
  yield b
  for side in ['left','right']:
   if side in b:yield from walk([b[side]])
def words(blocks):
 return sum(len(b.get('text','').split())+len(b.get('takeaway','').split())+len(b.get('caption','').split()) for b in walk(blocks))
for pt,t in zip(plan['tiles'],out['tiles']):
 assert [(s['step_id'],s['type']) for s in t['steps']]==[(s['step_id'],s['type']) for s in pt['steps']]
 for ps,s in zip(pt['steps'],t['steps']):
  assert s['concept_ids']==ps['concept_ids']
  for field in ['fact_ids','teaching_block_ids']:assert s['lineage'][field]==ps[field]
  if ps['type'] in ['check','hands_on']:assert 'blocks' not in s
  if ps['type']=='video':assert s['blocks']==[{'type':'media_group','segment_ids':ps['segment_ids']}]
  if ps['word_budget']:assert words(s.get('blocks',[]))<=ps['word_budget'],(s['step_id'],words(s['blocks']),ps['word_budget'])
  if ps['planned_visual_block_type'] not in [None,'up_next','media_group']:
   assert any(cid+'#visual' in b.get('lineage',{}).get('anchors',[]) for cid in ps['concept_ids'] for b in walk(s['blocks']))
 for s in t['steps']+t['remediation_steps']:
  for b in walk(s.get('blocks',[])):
   assert not any(k in b for k in ['output','result','computed_values','execution_provenance'])
   if b['type']=='prose':
    assert b.get('lineage') and len(b['text'].split())<=90
    assert not re.search(r'\bvideo\b',b['text'],re.I)
   for key in ['fact_ids','teaching_block_ids']:
    assert all('#' in x for x in b.get('lineage',{}).get(key,[]))
   if b['type']=='data_table':
    a=assets[b['asset_ref']['asset_id']]
    assert set(b['asset_ref'].get('columns',[]))<=set(c['name'] for c in a['columns'])
(B/'screens.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('Checklist passed')
print('Tiles:',len(out['tiles']))
for t in out['tiles']:print(t['tile_id'],len(t['steps']),'planned steps;',len(t['remediation_steps']),'remediation steps')
