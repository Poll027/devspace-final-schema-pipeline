import json, re, textwrap
from pathlib import Path
B=Path('batches/final_batch_mle.region.reproducible_release')
plan=json.loads((B/'tile_plans.json').read_text())
gloss=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
reg=json.loads((B/'scenario_asset_registry.json').read_text())
bundles={x['context']['concept_id']:x for x in gloss['bundles']}
assets={x['asset_id']:x for x in reg['assets']}
def file(cid,path):
    return next(x['content'] for x in assets['ws.'+cid.split('.')[-1]]['files'] if x['path']==path)
def config(cid,path): return json.loads(file(cid,path))
def lin(cids,tbs=(),facts=(),anchors=()):
    return dict(concept_ids=list(cids),teaching_block_ids=list(tbs),fact_ids=list(facts),anchors=list(anchors))
def prose(text,cid,tbs,facts,role='mechanism'):
    return dict(type='prose',text=text,role=role,lineage=lin([cid],tbs,facts))
# Each entry is a re-voiced teaching block; its original fact mapping is copied below.
texts={
'mle.ml_training_script':[
('Leave notebook state behind','Move training into a saved script that works from a clean shell. An explicit entry point runs the task directly without launching training during an ordinary import.'),
('Guard the entry point','Put execution behind if __name__ == "__main__":. Direct execution reaches that call; ordinary imports do not. Give the training function explicit parameters, resolving defaults and keyword overrides before training. Decode the declared configuration with json.load and map its fields to those arguments.'),
('Check the saved behavior','Run python training_script.py and compare recorded settings and outputs with the supplied notebook behavior. A caller can use subprocess.run(["python", script_path], check=True); a nonzero exit raises an error. Use json.dump(record, file_handle) to save structured state and json.load(file_handle) to recover it. JSON text itself is not a Python dictionary.'),
('Record what actually ran','Call the function with defaults and with explicit keyword overrides. Keep task state in parameters or locals, not notebook globals. Report resolved parameters and the validation result with f-strings such as f"{parameter_name}={resolved_value}". Save the script, stage it with git add SCRIPT_PATH, commit with git commit, and retain the revision.'),
('Capture a clean process','From a clean shell, run python training_script.py > capture.log 2>&1. Inspect the log for the parameters that actually resolved and the validation result.'),
('Compare both invocation forms','For the order fixture, compare default and configured calls against their corresponding notebook behavior. Decode JSON into keyword arguments, keep task state local, and guard execution. Retain the committed script revision. Launch a clean, checked subprocess and inspect its captured resolved settings and validation output. Redirection captures both standard output and error. Starting successfully alone does not show that forgotten notebook globals were unnecessary.'),
('Defaults are not overrides','Decode JSON before treating it as a dictionary. Neither notebook globals nor printed defaults can stand in for the task state and keyword overrides that actually resolved.')],
'mle.training_dataset_version':[
('A name can outlive its contents','An overwritten dataset can keep the same name. Reproduction needs its recorded generation and verified bytes, not a path labelled latest.'),
('Select the recorded generation','Overwriting a mutable object name can change its contents. Object Versioning retains noncurrent versions for explicit selection. Use bucket.blob(object_name, generation=recorded_generation).download_to_filename(local_path), not the current object. Before recording availability, confirm that exact object/version exists with the authorized client.'),
('Bind generation to bytes','Compute hashlib.sha256(data_bytes).hexdigest() from actual bytes and compare it with the expected identity. Keep object name, generation and observed digest in the local snapshot record. To create a snapshot, upload with bucket.blob(object_name).upload_from_filename(local_path) in the version-enabled bucket; inspect and record the created generation.'),
('Verify after an overwrite','Read local bytes with with open(path, "rb") as handle and update SHA-256 before recording upload identity. In the authorized overwrite fixture, retrieve the original recorded generation again and compare its digest with the original snapshot digest.'),
('Keep three identities together','Upload the order dataset to the version-enabled test bucket and record its created generation and local-byte SHA-256. Confirm that generation exists, select it explicitly, download it, and compare the downloaded digest with the record. After the authorized latest-object overwrite, repeat retrieval of the original generation and verify the original digest. The object name identifies the family; generation selects the version; digest checks the bytes obtained. This verifies the recorded fixture, not the safety of mutable names. A local digest alone is insufficient: compare it with bytes retrieved later, keeping the selected generation even though old and current objects share a name.'),
('A name or digest alone is insufficient','A mutable name is not immutable data identity. A recorded digest does not verify retrieval unless you check the downloaded bytes.')],
'mle.training_environment_record':[
('Inspect the environment, not memory','An environment record describes the process that actually executed. Remembered packages or a typed commit label are not independent evidence of its runtime and revision.'),
('Capture independently observed values','Read the actual repository revision with git rev-parse --verify HEAD. Capture installed package pins with python -m pip freeze; package==version entries can be installed with pip install -r. Use imported runtime/environment facilities to record the actual execution context alongside the supplied runtime identity, revision and dependencies.'),
('Verify the saved manifest','Import json, write json.dump(manifest, handle), and parse the saved file with json.load(handle). Use explicit with open(path, "w"/"r", encoding="utf-8") handles. Compare the parsed revision, dependency-version mapping and runtime identity against independent inspection. Reject any mismatch.'),
('Identify the interpreter','Import sys and record sys.version and sys.executable beside the supplied runtime identity. These are details of the Python process that actually ran.'),
('Round-trip and compare','Inspect HEAD and pip freeze, and capture sys.version and sys.executable beside the supplied runtime identity. Save the manifest with a text handle and parse it back. Compare the parsed revision with HEAD, dependencies with freeze output, and Python/runtime fields with the actual process. If they disagree, reject the match; never edit observed values to fit the manifest. Install the recorded pins with pip install -r where needed. The saved, parsed artifact is what later execution reads, so checking only the earlier in-memory dictionary is insufficient. Interpreter path and version complement, rather than replace, the environment identity.'),
('Saving is not verification','A written manifest can still be wrong. Inspect actual runtime details and dependency pins, parse the saved record, and reject mismatched values.')],
'mle.experiment_reproduction':[
('Resolve before executing','Reproduction starts with recorded code, data, environment and settings. Today’s working tree and latest dataset may describe another experiment despite a familiar run name.'),
('Recover code and data identity','Retrieve the experiment’s revision, snapshot, environment and resolved settings first. Check out the recorded local commit and verify HEAD instead of using a changed working tree. Download the recorded dataset generation and verify its identity instead of resolving latest.'),
('Launch in the recorded context','Use the recorded Python/dependency environment, installing pinned requirements where needed. Define the execution function with defaults and explicit keyword overrides, passing resolved state as parameters. Launch the script in a clean subprocess at its recorded working directory; check exit status and capture output.'),
('Resolve relative paths deliberately','Navigate the referenced repository and artifact directories before resolving relative data, configuration or script paths. Save both output streams with > capture.log 2>&1 and inspect that file. A pipe instead connects one command’s output to the next command’s input.'),
('Verify more than exit success','Recover and verify the recorded commit and dataset generation, use the pinned environment, and resolve defaults and overrides through function parameters. Navigate recorded directories before interpreting relative paths. Launch a clean subprocess, check its exit status and inspect captured settings and results against the record. A successful exit can still accompany a wrong dataset or default. Changed latest data or a different working directory must remain distinguishable from recorded context. Code governs the implementation; the verified snapshot governs inputs. Output redirection saves both streams to a log, whereas a pipe feeds another command. Keep these identities and configuration checks together rather than relying on memory.'),
('A filename is not an experiment','A familiar script name does not verify reproduction. A different commit, mutable dataset or unresolved relative path can change what executes.')],
'mle.model_version_registration':[
('Verify the artifact before registration','A registry version should link to verified run bytes. Resolve the stored generation and compare its content hash before creating the version.'),
('Retrieve the exact run artifact','Resolve the originating run’s artifact record, expected hash and immutable object version. Download with bucket.blob(key, generation=recorded_generation).download_to_filename(path), not the current key. Compute SHA-256 over downloaded bytes; a mismatch must stop registration.'),
('Create and retrieve a traceable version','Require the supplied registered model name to exist; for a new name, use client.create_registered_model(name). Call client.create_model_version(name=name, source=version_qualified_source, run_id=run_id) and retain the returned numeric version. Keep exact generation and hash with set_model_version_tag. Retrieve get_model_version(name, version) and its originating run, then compare their recorded identities.'),
('An overwrite is not approval','Only in the authorized test bucket, overwrite latest and retrieve the registered generation again. Verify its bytes against the registered hash and return one keyed registration verdict. An overwrite is not a new approved registry version. Import from mlflow import MlflowClient and construct MlflowClient() for version creation, retrieval and tagging.'),
('Keep the run link stable','For the order run, explicitly retrieve its recorded generation even when latest now differs. Verify the hash before creating a numeric version with a version-qualified source and run link. Use the supplied model name; create a new name only on the declared new-name path. Retain generation/hash tags, retrieve the version and linked run, and compare identities. After an authorized test overwrite, retrieve and verify that same registered generation again. Return one verdict binding run, version and artifact, not a claim that overwriting latest approved a replacement.'),
('A version number cannot repair a mutable source','A numeric registry version does not verify an unresolved mutable source. Verify generation and bytes, and distinguish overwriting an object from approving a registry version.')],
'mle.model_preprocessing_package':[
('Package the fitted representation','Keep the fitted model and fitted preprocessor together. Loading weights alone or refitting preprocessing may run successfully without reproducing the intended predictions.'),
('Persist trusted fitted state','Import pickle. At the recorded version-tied package path, use a binary "wb" handle and pickle.dump({"model": model, "preprocessor": preprocessor}, handle, protocol=5). Reload only a trusted, verified package in the compatible pinned inference environment: open "rb", call pickle.load(handle), and retrieve both dictionary keys. Untrusted pickle loading is unsafe and can execute arbitrary code. In the Dockerfile, use FROM with the compatible Python image, WORKDIR /app, COPY requirements.txt ./ and RUN pip install --no-cache-dir -r requirements.txt. COPY the declared package and serving source from the build context into their /app paths. Use a JSON-array CMD containing the declared serving command and argument, replacing placeholders so it loads this package.'),
('Build and start the recorded image','Use docker build -t IMAGE:TAG CONTEXT. Include the Dockerfile (or select it with -f) and all COPY sources; .dockerignore must not exclude required files. Record immutable image identity as well as tag. Prediction applies fitted training preprocessing before the model, without refitting. Start with docker run --name NAME -p HOST_PORT:CONTAINER_PORT --env KEY=VALUE IMAGE using declared ports and nonsecret settings.'),
('Inspect identity, state and logs','Use docker container inspect NAME to check image identity and State. Read captured standard output and error with docker container logs NAME for initialization or execution failures. Secrets must not appear in Dockerfile ARG or ENV: they persist in the image or metadata.'),
('Keep secrets out of the package configuration','Supply sensitive values through the runtime secret mechanism, not literal Compose values. Save and reload fitted state with explicit binary handles; write and read the pinned dependency manifest with text handles. Record pinned inference versions in requirements and install that manifest in the serving image.'),
('Assert reproducibility, not just execution','On the same fixed inputs, assert pre-save and container-reloaded predictions agree under declared tolerances. Separately check preserved fitted preprocessing parameters. Add assert predicate checks for declared valid, boundary and failure cases; a false predicate raises AssertionError in ordinary non-optimized execution.'),
('Check the whole package boundary','Persist trusted fitted model/preprocessor state with binary handles at the version-tied path. Keep pinned inference requirements in a text manifest. Include package, requirements and serving source in the Docker context, build it, and record immutable image identity. Start with declared ports and nonsecret settings; inspect identity, state and logs. Compare pre-save and container-reloaded predictions on fixed orders under explicit tolerances, separately checking preprocessing parameters. Reject untrusted pickle artifacts and supply credentials through the runtime mechanism, not Dockerfile or Compose literals.'),
('A matching tag is not matching fitted state','Packaging does not permit inference-time refitting or embedded credentials. A tag alone does not verify image identity. Pickle needs trusted, verified provenance and a compatible pinned environment.')],
'mle.protected_test_comparison':[
('Freeze before final testing','Protected testing compares an already fixed system. Freeze candidate, fitted preprocessing and threshold first; report disappointing results instead of selecting a replacement.'),
('Compare on one protected cohort','Evaluate only after fixing candidate, fitted preprocessing and threshold. Test results cannot select a replacement candidate or threshold. Generate candidate and baseline predictions for the same protected observations and compare precommitted quantities. Preserve fixed deployment probabilities, error costs and operating requirements; report failure rather than retune.'),
('Condition rates on actual classes','FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. An empty conditioning group makes its rate undefined. With zero correct-prediction cost, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN, using supplied deployment probabilities.'),
('Failure does not unfreeze the system','Candidate B and its threshold were selected before protected outcomes. Predict the same protected orders with B and the baseline. Keep deployment probabilities, costs and operating requirements fixed, even if the observed cohort’s class mix differs. Retain actual-class conditioning counts for rates while applying deployment probabilities to expected error cost: these have different roles. Report undefined quantities or failed requirements explicitly. Do not adjust the threshold, replace the candidate or refit preprocessing to make B pass. The final output is a matched comparison, not another selection round. Model identity, fitted preprocessing, threshold and metric inputs retain their declared values throughout.'),
('No second tuning opportunity','A protected-test failure does not authorize switching candidate, refitting preprocessing or searching for a better threshold.')],
'mle.bounded_managed_training':[
('Submission is only the beginning','Use supplied settings for one authorized bounded job. Verify consumed inputs and terminal output rather than treating submission as proof of success.'),
('Resolve a bounded request','CreateTrainingJob specifies TrainingJobName, AlgorithmSpecification, RoleArn, input/output data configuration, ResourceConfig and StoppingCondition. Use the supplied custom TrainingImage, permitted instance count/type and MaxRuntimeInSeconds. InputDataConfig must refer to version-resolved inputs; OutputDataConfig supplies the output S3 location. The role must be authorized for those resources.'),
('Record consumption and completion','The training container reads channels under /opt/ml/input/data/CHANNEL and writes model output under /opt/ml/model for upload. Inspect final job status and artifact location; check the intended artifact against recorded configuration. Keep dataset snapshot, code/configuration and resulting run/artifact identities together in the execution record.'),
('Inspect the job through the client','Import boto3; create client = boto3.client("sagemaker") and call client.create_training_job(**resolved_configuration). Inspect with client.describe_training_job(TrainingJobName=job_name): check TrainingJobStatus, any FailureReason and ModelArtifacts.S3ModelArtifacts. Save records with json.dump(record, file_handle), then decode with json.load(file_handle); JSON text is not a Python dictionary.'),
('Resolve input and output identities','Verify each selected input version before submission. If the API only accepts a mutable channel URI, materialize the selected version at a controlled immutable location instead of inventing a version parameter. Retrieve the output with the authorized storage client and check its reference against the completed job record. Managed resources are created for the job and released after termination; confirm terminal status, not merely submission.'),
('Follow one job from input to artifact','Resolve the supplied image, job name, role, channels, output location and resource/time limits before submission. Verify each input version and, where needed, materialize it at the controlled immutable location without unsupported API fields. The container reads the channel beneath /opt/ml/input/data and writes under /opt/ml/model. Inspect terminal status, any failure reason and the artifact location. Retrieve that artifact with the authorized storage client, checking its reference against the completed job record. Preserve snapshot, code/configuration and run/artifact identities together.'),
('A request does not end compute use','Submission is not completion, and an input name is not verified identity. Managed resources are released after termination; explicitly confirm terminal status.')]
}
# Registry supplies every concrete scenario value used by code examples.
training=config('mle.ml_training_script','configuration.json')
default_source=file('mle.ml_training_script','training_script.py').splitlines()[0]
default_args=default_source.removeprefix('def training_entry(').removesuffix('):')
train_code=f'''# Supplied configuration: {training!r}
import json
from fixture_workflow import supplied_workflow

def training_entry({default_args}):
    result = supplied_workflow(dataset_path=dataset_path, threshold=threshold)
    print(f"dataset_path={{dataset_path}}, threshold={{threshold}}")
    print(f"validation_accuracy={{result['validation_accuracy']}}")
    return result

if __name__ == "__main__":
    with open("configuration.json") as handle:
        configuration = json.load(handle)
    default_result = training_entry()
    configured_result = training_entry(
        dataset_path=configuration["dataset_path"],
        threshold=configuration["threshold"])
    record = {{"default": default_result, "configured": configured_result}}
    # Save structured parameters/results, not fitted Python objects.
    record = {{key: {{"resolved_parameters": value["resolved_parameters"],
                     "validation_accuracy": value["validation_accuracy"]}}
              for key, value in record.items()}}
    with open("training_record.json", "w") as handle:
        json.dump(record, handle)
    with open("training_record.json") as handle:
        saved_record = json.load(handle)
'''
train_shell='''git add training_script.py
git commit -m "Save executable training entry point"
git rev-parse --verify HEAD
python training_script.py > capture.log 2>&1
cat capture.log
python -c 'import training_script' # ordinary import does not train
python -c 'import subprocess; subprocess.run(["python", "training_script.py"], check=True)'
'''
snapshot_cfg=config('mle.training_dataset_version','snapshot_fixture.json')
snapshot_code=f'# Supplied snapshot settings: {snapshot_cfg!r}\n'+'''import hashlib, json
from google.cloud import storage
with open("snapshot_fixture.json") as handle:
    cfg = json.load(handle)
client = storage.Client()
bucket = client.bucket(cfg["bucket_name"])
with open(cfg["local_path"], "rb") as handle:
    original_hash = hashlib.sha256(handle.read()).hexdigest()
blob = bucket.blob(cfg["object_name"])
blob.upload_from_filename(cfg["local_path"])
generation = blob.generation
selected = bucket.blob(cfg["object_name"], generation=generation)
if not selected.exists(client=client):
    raise ValueError("Recorded version is unavailable")
record = {"object_name": cfg["object_name"], "generation": generation,
          "observed_digest": original_hash}
with open(cfg["record_path"], "w") as handle:
    json.dump(record, handle)
selected.download_to_filename(cfg["download_path"])
with open(cfg["download_path"], "rb") as handle:
    observed = hashlib.sha256(handle.read()).hexdigest()
if observed != record["observed_digest"]:
    raise ValueError("Snapshot bytes do not match")
# Authorized fixture changes only the mutable current object.
bucket.blob(cfg["object_name"]).upload_from_filename("changed_latest.csv")
selected.download_to_filename(cfg["download_path"])
with open(cfg["download_path"], "rb") as handle:
    after_overwrite = hashlib.sha256(handle.read()).hexdigest()
if after_overwrite != record["observed_digest"]:
    raise ValueError("Recorded generation did not verify after overwrite")
'''
env_code='''import json, subprocess, sys
revision = subprocess.run(["git", "rev-parse", "--verify", "HEAD"],
    check=True, capture_output=True, text=True).stdout.strip()
pins = subprocess.run([sys.executable, "-m", "pip", "freeze"],
    check=True, capture_output=True, text=True).stdout.splitlines()
manifest = {"revision": revision, "dependency_pins": pins,
    "python_version": sys.version, "python_executable": sys.executable,
    "runtime_identity": supplied_runtime_identity}
with open(manifest_path, "w", encoding="utf-8") as handle:
    json.dump(manifest, handle)
with open(manifest_path, "r", encoding="utf-8") as handle:
    parsed = json.load(handle)
# Independently inspect HEAD, freeze and runtime fields again.
if parsed != independently_inspected_environment:
    raise ValueError("Environment verification failed")
'''
reproduce_code='''import json, subprocess
# Resolve the recorded run before invoking its script.
with open("recorded_experiment.json") as handle:
    record = json.load(handle)
subprocess.run(["git", "checkout", record["revision"]],
    cwd=record["working_directory"], check=True)
head = subprocess.run(["git", "rev-parse", "--verify", "HEAD"],
    cwd=record["working_directory"], check=True,
    capture_output=True, text=True).stdout.strip()
if head != record["revision"]:
    raise ValueError("Wrong code revision")
# Verify recorded dataset generation and pinned environment first.
# Resolve relative data/configuration paths in the recorded directories.
def execute(script, cwd, python_executable="python", configuration_path="configuration.json"):
    # Read paths relative to the recorded working directory.
    from pathlib import Path
    with open(Path(cwd) / configuration_path) as handle:
        settings = json.load(handle)
    if settings != record["settings"]:
        raise ValueError("Resolved settings differ from the run record")
    return subprocess.run([python_executable, script], cwd=cwd,
        check=True, capture_output=True, text=True)
completed = execute(record["script"], cwd=record["working_directory"],
    python_executable=record["python_executable"],
    configuration_path=record["configuration_path"])
# Inspect completed.stdout/stderr and compare resolved settings/results
# with the record; exit success alone does not establish reproduction.
'''
run_artifact=config('mle.model_version_registration','run_artifact_record.json')
register_code=f'# Originating run artifact record: {run_artifact!r}\n'+'''import hashlib, json
from google.cloud import storage
from mlflow import MlflowClient
with open("run_artifact_record.json") as handle:
    record = json.load(handle)
storage_client = storage.Client()
bucket = storage_client.bucket(record["bucket_name"])
selected = bucket.blob(record["key"], generation=record["generation"])
selected.download_to_filename(record["local_path"])
with open(record["local_path"], "rb") as handle:
    observed_hash = hashlib.sha256(handle.read()).hexdigest()
if observed_hash != record["expected_hash"]:
    raise ValueError("Hash mismatch: do not create a registry version")
client = MlflowClient()
# Require the supplied name to exist; only on the new-name path:
# client.create_registered_model(name)
created = client.create_model_version(name=record["model_name"],
    source=record["version_qualified_source"], run_id=record["run_id"])
version = created.version
client.set_model_version_tag(record["model_name"], version,
    "generation", str(record["generation"]))
client.set_model_version_tag(record["model_name"], version,
    "sha256", observed_hash)
retrieved = client.get_model_version(record["model_name"], version)
origin = client.get_run(retrieved.run_id)
# Compare retrieved generation/hash/run/source with record.
# After authorized latest overwrite, retrieve the recorded generation
# again and compare its byte hash; return one keyed registration verdict.
'''
managed_contract=config('mle.bounded_managed_training','managed_contract.json')
managed_code=f'# Supplied job settings: {managed_contract!r}\n'+'''import boto3, json, hashlib
with open("managed_contract.json") as handle:
    contract = json.load(handle)
client = boto3.client("sagemaker")
storage_client = boto3.client("s3")
# Verify the selected version, then materialize a controlled immutable input.
selected = {"Bucket": contract["input_bucket"],
    "Key": contract["input_key"], "VersionId": contract["input_version"]}
storage_client.head_object(**selected)
bytes_response = storage_client.get_object(**selected)
observed_hash = hashlib.sha256(bytes_response["Body"].read()).hexdigest()
if observed_hash != contract["dataset_snapshot"]["expected_hash"]:
    raise ValueError("Input bytes do not match the selected snapshot")
storage_client.copy_object(Bucket=contract["input_bucket"],
    Key=contract["immutable_key"], CopySource=selected)
resolved_configuration = {
    "TrainingJobName": contract["job_name"],
    "AlgorithmSpecification": {"TrainingImage": contract["image"],
                               "TrainingInputMode": "File"},
    "RoleArn": contract["role"],
    "InputDataConfig": [{"ChannelName": contract["channel"],
        "DataSource": {"S3DataSource": {"S3DataType": "S3Prefix",
            "S3Uri": "s3://" + contract["input_bucket"] + "/" + contract["immutable_key"],
            "S3DataDistributionType": "FullyReplicated"}}}],
    "OutputDataConfig": {"S3OutputPath": contract["output_uri"]},
    "ResourceConfig": {"InstanceCount": contract["max_instance_count"],
        "InstanceType": contract["instance_type"]},
    "StoppingCondition": {"MaxRuntimeInSeconds": contract["max_runtime_seconds"]}}
with open(contract["configuration_path"], "w") as handle:
    json.dump(resolved_configuration, handle)
with open(contract["configuration_path"]) as handle:
    resolved_configuration = json.load(handle)
submission = client.create_training_job(**resolved_configuration) # once
# Re-inspect until terminal state; do not resubmit while polling.
while True:
    description = client.describe_training_job(TrainingJobName=contract["job_name"])
    status = description["TrainingJobStatus"]
    if status in ("Completed", "Failed", "Stopped"):
        break
failure_reason = description.get("FailureReason")
if status != "Completed":
    raise ValueError(f"Job did not complete: {failure_reason}")
artifact_uri = description["ModelArtifacts"]["S3ModelArtifacts"]
if artifact_uri != contract["artifact_uri"]:
    raise ValueError("Returned artifact differs from the intended job artifact")
artifact_bucket, artifact_key = artifact_uri.removeprefix("s3://").split("/", 1)
storage_client.download_file(Bucket=artifact_bucket, Key=artifact_key,
    Filename="downloads/model.tar.gz")
execution_record = {"snapshot": contract["dataset_snapshot"],
    "code_reference": contract["code_reference"], "configuration": resolved_configuration,
    "job_name": contract["job_name"], "submission": submission,
    "status": status, "artifact_uri": artifact_uri}
with open("execution_record.json", "w") as handle:
    json.dump(execution_record, handle)
with open("execution_record.json") as handle:
    parsed_record = json.load(handle)
assert parsed_record == execution_record
# The supplied channel is /opt/ml/input/data/CHANNEL; output is /opt/ml/model.
'''
visual_codes={
'mle.ml_training_script':[(train_code,'python'),(train_shell,'bash')],
'mle.training_dataset_version':[(snapshot_code,'python')],
'mle.training_environment_record':[(env_code,'python')],
'mle.experiment_reproduction':[(reproduce_code,'python')],
'mle.model_version_registration':[(register_code,'python')],
'mle.bounded_managed_training':[(managed_code,'python')]
}
def code_block(code,cid,language='python',tbs=(),facts=()):
    return dict(type='code_walkthrough',language=language,code=code,
        lineage=lin([cid],tbs,facts,[cid+'#visual']))
package_contract=config('mle.model_preprocessing_package','package_contract.json')
# Only inputs, tolerance and identities are displayed here; predictions are not typed outputs.
package_display={k:package_contract[k] for k in ['model_identity','registry_version','package_path','compatible_python_image','image_tag','container_name','rtol','atol']}
package_left=f'# Supplied package settings: {package_display!r}\n'+'''# Before saving: use the fitted training state on the fixed fixture.
with open("package_contract.json") as handle:
    contract = json.load(handle)
fixed_inputs = contract["fixed_inputs"]
pre_save_predictions = model.predict(preprocessor.transform(fixed_inputs))
pre_save_parameters = preprocessor.mean_
# Persist both objects with pickle.dump(..., protocol=5) at
# contract["package_path"], using an explicit binary handle.
'''
package_right='''# Inside the compatible pinned container: load only trusted, verified state.
with open(contract["package_path"], "rb") as handle:
    package = pickle.load(handle)
reloaded_predictions = package["model"].predict(
    package["preprocessor"].transform(fixed_inputs))
assert np.allclose(pre_save_predictions, reloaded_predictions,
    rtol=contract["rtol"], atol=contract["atol"])
assert np.allclose(pre_save_parameters, package["preprocessor"].mean_,
    rtol=contract["rtol"], atol=contract["atol"])
# Compare recorded immutable image identity with container inspect.
# Inspect state and logs; check declared valid, boundary and failure cases.
'''
# Protected comparison displays registered tables, never invented result rows.
def table(asset_id,cid):
    return dict(type='data_table',asset_ref={'asset_id':asset_id},lineage=lin([cid],anchors=[cid+'#visual']))
def visual(s):
    cid=s['concept_ids'][0];tbs=s['teaching_block_ids'];facts=s['fact_ids']
    if s['planned_visual_block_type']=='code_walkthrough':
        return [code_block(code,cid,language,tbs,facts) for code,language in visual_codes[cid]]
    if cid=='mle.model_preprocessing_package':
        return [dict(type='side_by_side',left_label='Before saving: fixed inputs',right_label='Container reload: same inputs',
          left=code_block(package_left,cid),right=code_block(package_right,cid),
          takeaway='Compare predictions under declared tolerances and check fitted preprocessing separately; inspect immutable image identity, state and logs.',
          lineage=lin([cid],tbs,facts,[cid+'#visual']))]
    if cid=='mle.protected_test_comparison':
        return [dict(type='side_by_side',left_label='Shared protected observations',right_label='Frozen B and baseline comparison',
          left=table('ds.protected_orders',cid),right=table('ds.protected_comparison',cid),
          takeaway='Keep the same observations and frozen choices. Report failed requirements or undefined rates without retuning.',
          lineage=lin([cid],tbs,facts,[cid+'#visual']))]
    raise ValueError(s)

# Compact remediation groups: one focused contrast followed by the evidence rule.
# Fact ids are selected from the failed task, not from another interaction.
remediation_groups={
'mle.ml_training_script':[
('f1 f2 f3 f6 f7','Guard execution with if __name__ == "__main__":; ordinary imports must not train. Define explicit defaults and keyword overrides, keep state local, and call both forms. Decode configuration with json.load, map fields to arguments, and use json.dump/json.load for a structured record rather than treating JSON text as a dictionary.'),
('f4 f5 f8 f9 f10','Save training_script.py, stage with git add SCRIPT_PATH, commit with git commit, and retain the revision. Run python training_script.py > capture.log 2>&1 in a clean shell. Inspect f-string reports of resolved parameters and validation results against notebook behavior. A caller uses subprocess.run(["python", script_path], check=True); a nonzero exit raises an error.')],
'mle.training_dataset_version':[
('f1 f2 f3 f4','Latest can change while Object Versioning retains explicitly selectable noncurrent versions. Confirm the recorded object/version exists with the authorized client. Retrieve with bucket.blob(object_name, generation=recorded_generation).download_to_filename(local_path), then compare hashlib.sha256(data_bytes).hexdigest() from actual downloaded bytes with the expected digest.'),
('f5 f6 f7 f8','Read local data with with open(path, "rb") as handle and hash its bytes. Upload using bucket.blob(object_name).upload_from_filename(local_path) in the version-enabled bucket; inspect the created generation. Keep object name, generation and observed digest in a local record. After an authorized latest overwrite, retrieve that original generation again and compare its digest with the original snapshot.')],
'mle.training_environment_record':[
('f1 f2 f3 f7','Inspect git rev-parse --verify HEAD and python -m pip freeze, not remembered labels. The package==version pins can be installed with pip install -r. Use imported runtime/environment facilities, including import sys, sys.version and sys.executable, to capture actual process details beside the supplied runtime identity, revision and dependencies.'),
('f4 f5 f6','Import json. Save with json.dump(manifest, handle), parse with json.load(handle), and use explicit with open(path, "w"/"r", encoding="utf-8") handles. Independently inspect revision, dependency mapping and runtime identity and compare them with the parsed artifact. Reject a mismatch; writing alone is not verification.')],
'mle.experiment_reproduction':[
('f1 f2 f3 f4','Before execution, retrieve the recorded revision, dataset snapshot, environment and resolved settings. Check out the recorded local commit and verify HEAD. Explicitly download the recorded generation and verify its identity. Use the recorded Python/dependency environment, installing its pinned requirements where needed. Today’s code and latest data are not substitutes.'),
('f5 f6 f7 f8','Pass resolved state through an execution function with defaults and explicit keyword overrides. Navigate recorded repository/artifact directories before resolving relative data, configuration and script paths. Launch a clean subprocess in the recorded working directory; check exit status and inspect captured output. Shell > capture.log 2>&1 saves standard output and error; a pipe instead feeds one command’s output into another’s input.')],
'mle.model_version_registration':[
('f1 f2 f3 f4 f5 f6 f9','Resolve the run artifact record, expected hash and generation. Download with bucket.blob(key, generation=recorded_generation).download_to_filename(path); reject a downloaded-byte SHA-256 mismatch before registration. Import from mlflow import MlflowClient and construct MlflowClient(). Require the registered name to exist, creating it with create_registered_model only for a new name. Use create_model_version with name, version-qualified source and run_id; retain its numeric version. Preserve generation/hash with set_model_version_tag, then retrieve get_model_version and the linked run to compare identities.'),
('f7 f8','Only in the authorized test bucket, overwrite latest. Re-retrieve the registered generation, compare its byte digest with the registered hash, and return one keyed verdict binding the run, version and artifact. The overwrite does not approve a new registry version.')],
'mle.model_preprocessing_package':[
('f1 f2 f11 f12','Import pickle; persist both fitted objects at the version-tied path using a binary "wb" handle and pickle.dump({"model": model, "preprocessor": preprocessor}, handle, protocol=5). In the compatible pinned environment, reload only trusted, verified state with a binary "rb" handle and pickle.load; retrieve both dictionary keys. Untrusted pickle can execute arbitrary code. Write/read pinned inference requirements through text handles and install that manifest in the image.'),
('f3 f4','Use FROM for the compatible Python image, WORKDIR /app, COPY requirements.txt ./, RUN pip install --no-cache-dir -r requirements.txt, COPY the declared package and serving source to /app paths, and a JSON-array CMD for the declared command/argument. Build with docker build -t IMAGE:TAG CONTEXT; include the Dockerfile (or use -f) and all COPY sources without .dockerignore exclusions. Record immutable image identity, not only tag.'),
('f5 f6 f7 f8 f9 f10','Apply fitted preprocessing before the model; do not refit at inference. Start docker run --name NAME -p HOST_PORT:CONTAINER_PORT --env KEY=VALUE IMAGE with declared ports and nonsecret settings. Check image identity and State using docker container inspect NAME; inspect captured stdout/stderr with docker container logs NAME. Dockerfile ARG/ENV secrets persist in the image or metadata. Use runtime secrets, not literal Compose credentials.'),
('f13 f14','On the same fixed inputs, assert pre-save and container-reloaded predictions agree under declared tolerances; separately check preserved fitted preprocessing parameters. Check declared valid, boundary and failure predicates. A false assert raises AssertionError in ordinary non-optimized execution, so successful startup alone does not establish reproducibility.')],
'mle.protected_test_comparison':[
('f1 f2','Freeze candidate, fitted preprocessing and threshold before protected testing. Candidate and baseline predictions must use the same protected observations and precommitted quantities. Protected outcomes cannot choose a replacement candidate or threshold.'),
('f3 f4 f5','Keep deployment probabilities, costs and operating requirements fixed; report failure without retuning. FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) conditions on actual positives. An empty conditioning group gives an undefined rate. With zero correct-prediction cost, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.')],
'mle.bounded_managed_training':[
('f1 f2 f3 f4 f10','Resolve TrainingJobName, AlgorithmSpecification with supplied TrainingImage, authorized RoleArn, InputDataConfig, OutputDataConfig, ResourceConfig and StoppingCondition. Keep instance count/type within budget and bound MaxRuntimeInSeconds. Verify selected input versions first; where the API only accepts a mutable channel URI, materialize the verified version at a controlled immutable location, not an unsupported version argument. Channels appear under /opt/ml/input/data/CHANNEL; model output goes under /opt/ml/model for upload.'),
('f5 f6 f7 f8 f9 f11 f12','Import boto3; use boto3.client("sagemaker") and create_training_job(**resolved_configuration) once. Inspect describe_training_job(TrainingJobName=job_name) for terminal TrainingJobStatus, any FailureReason and ModelArtifacts.S3ModelArtifacts. Check intended output against recorded configuration; retrieve it through authorized storage and compare its reference with the completed job record. Keep snapshot, code/configuration and run/artifact identities in a json.dump/json.load round-tripped record. Managed resources are released after termination, not submission.')]
}

short_names={
'mle.ml_training_script':'the executable training entry point',
'mle.training_dataset_version':'dataset snapshot identity',
'mle.training_environment_record':'the saved environment record',
'mle.experiment_reproduction':'recorded experiment context',
'mle.model_version_registration':'the run-to-registry artifact link',
'mle.model_preprocessing_package':'the fitted prediction package',
'mle.protected_test_comparison':'the frozen protected comparison',
'mle.bounded_managed_training':'the bounded training request'}
contrast={
'mle.ml_training_script':'A saved filename is not evidence of the revision that ran: retain the committed revision, then inspect the clean process.',
'mle.training_dataset_version':'Latest may change; select the recorded generation and verify retrieved bytes against the snapshot digest.',
'mle.training_environment_record':'A typed manifest label can disagree with the process. Compare the parsed record with independent inspection, and reject a mismatch.',
'mle.experiment_reproduction':'A familiar script name or successful exit is not enough: verify recorded code, data, environment, settings and working directory.',
'mle.model_version_registration':'An authorized overwrite changes latest, not the approved registry version. Re-retrieve the registered generation and verify its hash.',
'mle.model_preprocessing_package':'Successful startup does not show matching fitted state or safe secret handling. Preserve preprocessing and use runtime secrets, not image or Compose literals.',
'mle.protected_test_comparison':'Report a failed or undefined result; do not change the fixed candidate, preprocessing or threshold to make it pass.',
'mle.bounded_managed_training':'Submission is not termination. Verify selected input identity before submission and inspect terminal status and artifact identity afterward.'}
recaps={
'mle.tile.052_055':[
('mle.ml_training_script','Use a guarded, parameterized, committed script; inspect resolved settings and results in a clean process.'),
('mle.training_dataset_version','Bind dataset name, recorded generation and verified byte digest.'),
('mle.training_environment_record','Round-trip the environment manifest and compare it with independent inspection.'),
('mle.experiment_reproduction','Resolve recorded code, data, environment, settings and directories before reproducing.')],
'mle.tile.056_057':[
('mle.model_version_registration','Verify exact artifact bytes before creating a run-linked numeric version; retain generation/hash tags and verify after an authorized overwrite.'),
('mle.model_preprocessing_package','Package trusted fitted model and preprocessing together with pinned dependencies. Verify container identity and fixed-input agreement; keep secrets in runtime mechanisms.')],
'mle.tile.058_058':[
('mle.protected_test_comparison','Freeze candidate, preprocessing and threshold before protected testing. Compare both systems on the same observations. Condition FPR on actual negatives and FNR on actual positives; report undefined rates. Apply fixed deployment probabilities, costs and requirements; report failure without retuning.')],
'mle.tile.059_059':[
('mle.bounded_managed_training','Verify version-resolved inputs and submit one authorized request within resource/time limits. Inspect terminal status and retrieve the matching artifact. Round-trip a record linking snapshot, code/configuration, job and artifact. Submission alone does not confirm compute has ended.')]
}
next_ideas={t['tile_id']:short_names[t['concept_ids'][0]] for t in plan['tiles']}
next_ideas['mle.tile.060_063']=gloss['names']['mle.prediction_schema_validation']
output=dict(schema_version=plan['schema_version'],kind='screens_part',path_id=plan['path_id'],batch_id=plan['batch_id'],tiles=[])
for tile in plan['tiles']:
    out=dict(tile_id=tile['tile_id'],title=tile['title'],steps=[],remediation_steps=[])
    for s in tile['steps']:
        cids=s['concept_ids'];cid=cids[0];kind=s['type']
        step=dict(step_id=s['step_id'],type=kind,concept_ids=cids,
            title='',eyebrow={'explainer':'Understand','video':'Optional support','check':'Quick check','hands_on':'Review evidence','recap':'Takeaways'}[kind],
            lineage=lin(cids,s['teaching_block_ids'],s['fact_ids'],s['anchors']))
        if kind=='explainer':
            step['blocks']=[];titles=[]
            for qualified in s['teaching_block_ids']:
                c,tbid=qualified.split('#');tb=next(x for x in bundles[c]['teaching_blocks'] if x['id']==tbid)
                title,text=texts[c][int(tbid[2:])-1];titles.append(title)
                role={'mechanism':'mechanism','example':'example','misconception':'misconception','motivation':'intro'}.get(tb['purpose'],'intro')
                # Split only at sentence boundaries to keep prose readable and <=90 words.
                sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z])',text)
                chunks=[];chunk=''
                for sentence in sentences:
                    if chunk and len((chunk+' '+sentence).split())>90:
                        chunks.append(chunk);chunk=''
                    chunk=(chunk+' '+sentence).strip()
                if chunk: chunks.append(chunk)
                for chunk in chunks:
                    step['blocks'].append(prose(chunk,c,[qualified],[c+'#'+f for f in tb['fact_ids']],role))
            step['title']=titles[0]
            if s['planned_visual_block_type']:
                step['blocks']+=visual(s)
        elif kind=='video':
            step['title']='Revisit '+short_names[cid]
            step['blocks']=[dict(type='media_group',segment_ids=s['segment_ids'])]
        elif kind in ['check','hands_on']:
            step['title']=('Review ' if kind=='hands_on' else 'Check ')+short_names[cid]
            step['lede']='Read the supplied excerpts in this step and decide which are correct, defective or unsafe.' if kind=='hands_on' else 'Choose the judgement that preserves the recorded evidence and the rule you just learned.'
        elif kind=='recap':
            step['title']='Keep the evidence together'
            step['blocks']=[]
            for c,text in recaps[tile['tile_id']]:
                all_tb=[c+'#'+tb['id'] for tb in bundles[c]['teaching_blocks']]
                all_f=[c+'#'+f['id'] for f in bundles[c]['coverage']['required_facts']]
                step['blocks'].append(prose(text,c,all_tb,all_f,'takeaway'))
            step['blocks'].append(dict(type='up_next',title='Up next: '+next_ideas[tile['next_tile_id']],text='Continue to '+next_ideas[tile['next_tile_id']]+'.'))
        out['steps'].append(step)
        if kind in ['check','hands_on']:
            # Separate routes cover differing measured fact sets without borrowing another task's scope.
            facts=s['fact_ids'];tbs=[]
            for tb in bundles[cid]['teaching_blocks']:
                if set(cid+'#'+f for f in tb['fact_ids']) & set(facts): tbs.append(cid+'#'+tb['id'])
            rid=tile['tile_id']+f'.r{len(out["remediation_steps"])+1:02d}'
            remediation=dict(step_id=rid,type='remediation',concept_ids=[cid],title='Contrast: '+short_names[cid],
                lineage=lin([cid],tbs,facts),blocks=[])
            remediation['blocks'].append(prose(contrast[cid],cid,tbs,facts,'misconception'))
            if kind=='hands_on':
                for local_ids, text in remediation_groups[cid]:
                    covered=[cid+'#'+f for f in local_ids.split() if cid+'#'+f in facts]
                    if not covered: continue
                    relevant=[cid+'#'+tb['id'] for tb in bundles[cid]['teaching_blocks'] if set(tb['fact_ids']) & set(local_ids.split())]
                    remediation['blocks'].append(prose(text,cid,relevant,covered,'mechanism'))
            else:
                # Checks use only their focused measured facts, sourced exactly.
                for fact_id in facts:
                    fact=next(f for f in bundles[cid]['coverage']['required_facts'] if cid+'#'+f['id']==fact_id)
                    relevant=[cid+'#'+tb['id'] for tb in bundles[cid]['teaching_blocks'] if fact['id'] in tb['fact_ids']]
                    remediation['blocks'].append(prose(fact['statement'],cid,relevant,[fact_id],'mechanism'))
            out['remediation_steps'].append(remediation)
    output['tiles'].append(out)
(B/'screens.json').write_text(json.dumps(output,indent=2)+'\n')
print('Tiles:',len(output['tiles']))
for t in output['tiles']:print(t['tile_id'],len(t['steps']),'planned steps;',len(t['remediation_steps']),'remediation steps')
# Stage-specific mistakes-to-avoid checklist: structural, budget, lineage, values and no fabricated outputs.
def walk(block):
    yield block
    for k in ['left','right','before','after']:
        if isinstance(block.get(k),dict): yield from walk(block[k])
for t,p in zip(output['tiles'],plan['tiles']):
    assert [(s['step_id'],s['type'],s['concept_ids']) for s in t['steps']]==[(s['step_id'],s['type'],s['concept_ids']) for s in p['steps']]
    for s,ps in zip(t['steps'],p['steps']):
        assert s['lineage']['fact_ids']==ps['fact_ids']
        assert s['lineage']['teaching_block_ids']==ps['teaching_block_ids']
        if s['type'] in ['check','hands_on']:assert 'blocks' not in s
        if s['type']=='explainer':
            words=sum(len(b['text'].split()) for b in s['blocks'] if b['type']=='prose')
            assert words<=ps['word_budget'],(s['step_id'],words,ps['word_budget'])
    for s in t['steps']+t['remediation_steps']:
        for b in s.get('blocks',[]):
            for sub in walk(b):
                assert 'result' not in sub and 'output' not in sub and 'computed_values' not in sub
                if sub['type']=='prose':
                    assert sub['lineage'] and len(sub['text'].split())<=90,(s['step_id'],len(sub['text'].split()))
                    assert not re.search(r'\bvideo\b',sub['text'],re.I)
                for f in sub.get('lineage',{}).get('fact_ids',[]):assert '#f' in f
                if sub['type'] in ['side_by_side','code_walkthrough','data_table']:
                    assert any(x.endswith('#visual') for x in sub['lineage']['anchors'])
                if 'asset_ref' in sub:
                    asset=assets[sub['asset_ref']['asset_id']]
                    assert set(sub['asset_ref'].get('columns',[]))<=set(x['name'] for x in asset['columns'])
print('Mistakes-to-avoid automated checklist passed. Registry values copied/read, no computed outputs authored.')
