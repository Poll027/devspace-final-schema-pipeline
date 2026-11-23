import json, csv, io
from pathlib import Path
B=Path(__file__).parent
plan=json.loads((B/'tile_plans.json').read_text())
screens=json.loads((B/'screens.json').read_text())
bundles={b['context']['concept_id']:b for b in json.loads((B/'inputs/path_glossary_bundle.json').read_text())['bundles']}
registry=json.loads((B/'scenario_asset_registry.json').read_text())
assets={a['asset_id']:a for a in registry['assets']}
def file(cid,name):
 return next(f['content'] for f in assets['ws.'+cid]['files'] if f['path']==name)
def record(cid,name):return json.loads(file(cid,name))
# Excerpts are authored implementations / review proposals, not invented execution output.
# The boolean in each specification is the semantic judgement of that exact excerpt.
checks={
'ml_training_script':('A training script is saved in the repository. Which action completes the required repository record?',[
('Stage the script, commit it, and retain the resulting revision.',True,'Saving alone is not a commit; staging, committing and retaining the revision completes the record.'),
('Retain only the saved file path; no commit is needed.',False,'The file path does not replace the required staged and committed script revision.'),
('Stage the script and retain its path without committing.',False,'Staging is not committing; the resulting commit revision must be retained.')]),
 'training_dataset_version':('The latest object has been overwritten. Which retrieval verifies the original recorded snapshot?',[
('Download the recorded generation and compare the digest of its bytes with the original recorded digest.',True,'The selected generation and byte digest verify the original snapshot despite a latest overwrite.'),
('Download the current object at the same name and accept the matching name.',False,'A mutable name can now resolve to different contents; the recorded generation must be selected.'),
('Select the recorded generation but accept it without hashing the downloaded bytes.',False,'Selecting the version is not the required content check; compare its observed byte digest with the original record.')]),
 'training_environment_record':('A saved environment manifest parses as JSON. Which verification is defensible?',[
('Compare its revision, dependency mapping and runtime fields with fresh independent observations; reject any mismatch.',True,'Independent observations verify that the parsed manifest describes the actual environment.'),
('Accept the manifest because it is valid JSON.',False,'Parsing verifies structure, not agreement with the observed revision, dependencies and runtime.'),
('Copy the manifest fields into the observation record, then compare the two.',False,'Overwriting independent observations makes the comparison circular and hides mismatches.')]),
 'experiment_reproduction':('A stochastic rerun is being judged against a recorded experiment. Which evidence supports reproduction?',[
('Verify the recorded revision, dataset generation, environment and resolved settings; check the clean-process result in its recorded working directory and compare the outcome under the supplied tolerances.',True,'Reproduction uses verified recorded inputs and the declared outcome comparison, not a convenient changed setup.'),
('Use the latest dataset and current revision if the final metric looks similar.',False,'A similar outcome does not establish use of the recorded commit and dataset generation.'),
('Skip inspecting the exit result and captured output because the recorded settings were available.',False,'Available settings are not execution evidence; check the subprocess result and captured output.')]),
 'model_version_registration':('After an authorized latest-key overwrite, which check establishes that an existing registry version still identifies its registered content?',[
('Retrieve the registered generation, verify its byte hash against the registered hash, and return the keyed verdict.',True,'The registered version-qualified reference and hash establish retained content identity.'),
('Retrieve latest and accept it because the key name is unchanged.',False,'Latest can change; the registered generation must be retrieved and its bytes verified.'),
('Treat the overwrite itself as creation of a new approved registry version.',False,'A mutable overwrite is not a new approved registry version and does not verify the existing one.')]),
 'model_preprocessing_package':('A package image and Compose configuration need a sensitive value. Which proposal follows the stated secret policy?',[
('Use the authorized runtime secret mechanism, without literal credentials in Dockerfile or Compose.',True,'Sensitive values belong in the runtime secret mechanism, not persisted image or configuration literals.'),
('Put the literal secret in a Dockerfile ARG instead of ENV.',False,'Both ARG and ENV can persist secrets in the image or metadata.'),
('Keep the image clean but write the literal secret into Compose.',False,'A literal sensitive value in Compose still violates the stated runtime-secret requirement.')]),
 'protected_test_comparison':('Candidate B, its fitted preprocessing and threshold were frozen before protected testing. The matched comparison fails a requirement. What should the report do?',[
('Report the failure for B and the baseline on the same protected observations, leaving B and the fixed comparison unchanged.',True,'Protected results report the precommitted comparison; they do not choose a replacement.'),
('Replace B with whichever model looks better on the protected observations.',False,'The protected test must not choose a replacement candidate.'),
('Refit preprocessing or adjust the threshold using the protected results before reporting.',False,'The fitted preprocessing and decision threshold must remain fixed for protected evaluation.')]),
 'bounded_managed_training':('The training API accepts a channel URI but no version parameter. Which preparation respects the input identity and container contract?',[
('Verify the selected object version and materialize it at the controlled immutable input location; use the channel path under /opt/ml/input/data and write model output under /opt/ml/model.',True,'Verified materialization preserves selected input identity without inventing an API parameter, and respects the container paths.'),
('Add an unsupported VersionId field to the channel request and assume it pins the bytes.',False,'An unsupported version parameter does not resolve input identity; verified selected bytes must be materialized when required.'),
('Submit the mutable latest URI without verifying or materializing the selected version.',False,'The latest URI can resolve different bytes; verify and preserve the selected version before submission.')])}
P={}
def add(cid,text,ok,why):P.setdefault(cid,[]).append((text,ok,why))
add('ml_training_script','''# Review this control flow; the supplied workflow is inside train.
def train(dataset_path=default_dataset_path, threshold=default_threshold):
    result = workflow(dataset_path=dataset_path, threshold=threshold)
    print(f"threshold={threshold} validation_accuracy={result}")
    return {"dataset_path": dataset_path, "threshold": threshold, "validation_accuracy": result}
if __name__ == "__main__":
    with open(config_path) as handle:
        config = json.load(handle)
    default_run = train()
    configured_run = train(dataset_path=config["dataset_path"], threshold=config["threshold"])
# All task state is passed in or local; imports do not call train.''',True,'Explicit parameters, resolved-value reporting, both invocation forms and a guarded call distinguish execution from import without notebook globals.')
add('ml_training_script','''# Proposed reporting inside a parameterized training function:
result = workflow(dataset_path=dataset_path, threshold=threshold)
print(f"threshold={default_threshold} validation_accuracy={result}")
# The caller may override threshold; this line always reports the default.''',False,'The printed threshold must be the actual resolved threshold, not the default when an override was used.')
add('ml_training_script','''with open(record_path, "w") as handle:
    json.dump({"default": default_run, "configured": configured_run}, handle)
with open(record_path) as handle:
    recovered = json.load(handle)
assert recovered == {"default": default_run, "configured": configured_run}''',True,'The saved record reloads as structured JSON values and is compared with both actual runs.')
add('ml_training_script','''# Proposed acceptance checks, not a claim they have already run:
# git add training_script.py; git commit; retain the returned revision
# In a clean shell: python training_script.py > capture.log 2>&1
# Inspect capture.log: compare each resolved setting and result with its corresponding notebook behavior.
subprocess.run(["python", script_path], check=True)
# Import separately and confirm that no training call occurs.''',True,'This review plan checks the retained commit, clean-shell captured results, checked caller invocation and import behavior.')
add('ml_training_script','''# Proposed replacement for clean-shell verification:
# Execute notebook cells in the current kernel, then accept its existing outputs.
# Do not inspect capture.log or compare default and configured behavior.''',False,'An existing notebook kernel can supply hidden state; it does not verify the saved script in a clean process or its two captured results.')
add('training_dataset_version','''with open(local_path, "rb") as handle:
    observed_digest = hashlib.sha256(handle.read()).hexdigest()
blob = bucket.blob(object_name)
blob.upload_from_filename(local_path)
created_generation = blob.generation
selected = bucket.blob(object_name, generation=created_generation)
if not selected.exists():
    raise ValueError("snapshot unavailable")
record = {"object_name": object_name, "generation": created_generation, "digest": observed_digest}
# Save record locally only after the existence check.''',True,'The digest comes from original local bytes, the generation from the upload, and availability from the authorized version-specific check.')
add('training_dataset_version','''selected = bucket.blob(record["object_name"], generation=record["generation"])
selected.download_to_filename(download_path)
with open(download_path, "rb") as handle:
    assert hashlib.sha256(handle.read()).hexdigest() == record["digest"]
# After overwriting latest in the authorized version-enabled test bucket,
# repeat this same generation-qualified download and byte-digest assertion.''',True,'Both retrievals explicitly select the original generation and verify downloaded bytes against the original digest.')
add('training_dataset_version','''# Following the authorized latest overwrite:
bucket.blob(record["object_name"]).download_to_filename(download_path)
# Accept because the name still equals the recorded object_name.''',False,'Without the recorded generation this selects current contents; a matching mutable name is not snapshot identity.')
add('training_dataset_version','''selected = bucket.blob(object_name, generation=requested_generation)
record = {"object_name": object_name, "generation": requested_generation, "available": True}
# No authorized existence check is made before saving this record.''',False,'Availability must be confirmed for that object/version before recording it as available.')
add('training_environment_record','''# Proposed collection procedure:
# Inspect git rev-parse --verify HEAD and retain exactly its observed revision.
# Run python -m pip freeze; retain the observed package==version mapping.
manifest = {"revision": observed_revision, "dependencies": observed_dependencies,
            "runtime": supplied_runtime_identity,
            "python_version": sys.version, "python_executable": sys.executable}
with open(manifest_path, "w", encoding="utf-8") as handle:
    json.dump(manifest, handle)
with open(manifest_path, "r", encoding="utf-8") as handle:
    parsed = json.load(handle)''',True,'The manifest uses actual revision and dependency observations, supplied runtime identity and actual Python details, with explicit text-handle JSON round-trip.')
add('training_environment_record','''# fresh is independently inspected, not copied from parsed.
assert parsed["revision"] == fresh["revision"]
assert parsed["dependencies"] == fresh["dependencies"]
assert parsed["runtime"] == fresh["runtime"]
assert parsed["python_version"] == fresh["python_version"]
assert parsed["python_executable"] == fresh["python_executable"]
# Apply the same verification to changed-revision, changed-package and changed-runtime fixtures;
# reject each mismatch without changing fresh.''',True,'Comparing all parsed environment fields with independent observations accepts matching records and rejects each changed field.')
add('training_environment_record','''fresh["revision"] = parsed["revision"]
fresh["dependencies"] = parsed["dependencies"]
fresh["runtime"] = parsed["runtime"]
assert parsed["revision"] == fresh["revision"]
# Declare verification complete.''',False,'Copying manifest values into the independent observations defeats mismatch detection.')
add('training_environment_record','''manifest["python_version"] = "the version we planned to install"
manifest["python_executable"] = "the executable we expected"
# No sys.version or sys.executable observations are collected.''',False,'Python runtime details must describe actual execution, not intended or guessed values.')
add('experiment_reproduction','''# Review procedure before rerunning:
# Navigate the recorded repository and artifact directories.
# Check out the recorded commit and verify HEAD.
# Download the recorded dataset generation and verify its byte identity.
# Use the recorded Python environment and install its pinned requirements where needed.
# Resolve relative script, dataset and configuration paths in that recorded context.''',True,'These checks preserve the recorded revision, snapshot, environment and path context rather than using current mutable state.')
add('experiment_reproduction','''def execute(script_path=recorded_script, working_directory=recorded_directory,
            dataset_path=recorded_dataset, threshold=recorded_threshold):
    return launch_resolved_training(script_path=script_path,
        working_directory=working_directory, dataset_path=dataset_path, threshold=threshold)
# Invoke with explicit keyword overrides for the resolved recorded settings.
# launch_resolved_training uses these parameters, not notebook globals.''',True,'Defaults and explicit overrides pass the resolved run state through parameters.')
add('experiment_reproduction','''# Proposed clean-process review:
# Run the recorded entry point in the recorded working directory.
# Redirect stdout and stderr: python recorded_training_script.py > capture.log 2>&1
# Inspect the subprocess exit result and both captured streams.
# Pipe example: cat capture.log | grep threshold
# Compare the rerun outcome with the recorded outcome under the supplied stochastic tolerances.''',True,'The review checks execution and captured output, includes a pipe, and uses the declared tolerance comparison.')
add('experiment_reproduction','''# Keep the recorded threshold but run the current checkout on latest data.
# If the final metric falls within tolerance, label the run a reproduction.''',False,'A close outcome cannot replace verification of the recorded commit, dataset generation and environment.')
add('experiment_reproduction','''# Use the recorded script but launch it from an arbitrary directory.
# Resolve relative dataset/configuration paths from that directory.
# Accept without checking the subprocess exit result or captured error output.''',False,'Working directory is part of the resolved run context, and execution errors must be inspected.')
add('model_version_registration','''from mlflow import MlflowClient
client = MlflowClient()
blob = bucket.blob(run_record["key"], generation=run_record["generation"])
blob.download_to_filename(local_path)
with open(local_path, "rb") as handle:
    observed_hash = hashlib.sha256(handle.read()).hexdigest()
if observed_hash != run_record["expected_hash"]:
    raise ValueError("artifact mismatch")
# All version-creation calls occur strictly after this check;
# a mismatch fixture reaches no create_model_version call.''',True,'The artifact comes from the originating run generation and a mismatch is rejected before registration.')
add('model_version_registration','''# The supplied model name is required to exist first; create_registered_model for a new name.
version = client.create_model_version(name=run_record["model_name"],
    source=run_record["version_qualified_source"], run_id=run_record["run_id"])
client.set_model_version_tag(run_record["model_name"], version.version, "generation", str(run_record["generation"]))
client.set_model_version_tag(run_record["model_name"], version.version, "hash", observed_hash)
# Retain returned numeric version.version, not just the mutable source key.''',True,'Version creation links the exact version-qualified source and originating run, with retained generation and hash metadata.')
add('model_version_registration','''saved = client.get_model_version(run_record["model_name"], version.version)
origin = client.get_run(saved.run_id)
# Compare source, generation/hash tags and originating run with run_record.
# Overwrite latest only in the authorized test bucket.
# Download saved generation again, hash its bytes and compare with saved hash.
# Return one keyed verdict combining these checks.''',True,'Retrieving the version and linked run plus rechecking registered bytes after overwrite verifies the required persistent identity.')
add('model_version_registration','''# A downloaded artifact hash mismatches the run record.
version = client.create_model_version(name=model_name, source=latest_uri, run_id=run_id)
# Record the mismatch only after version creation.''',False,'A mismatch must stop registration before any registry version is created; a latest URI also fails to pin the source.')
add('model_version_registration','''# Latest is overwritten in the test bucket.
# Mark that overwrite as a newly approved numeric registry version without calling the registry.
# Do not retrieve the original registered generation or compare its hash.''',False,'A mutable overwrite is not registry approval and does not verify the original version survives unchanged.')
add('model_preprocessing_package','''# Both objects are fitted; this package is trusted and verified.
import pickle
with open(package_path, "wb") as handle:
    pickle.dump({"model": model, "preprocessor": preprocessor}, handle, protocol=5)
# package_path is the recorded version-tied path.
with open(package_path, "rb") as handle:
    package = pickle.load(handle)
# Reload only in the compatible pinned inference environment.
with open(manifest_path, "w", encoding="utf-8") as handle:
    handle.write(pinned_manifest)
with open(manifest_path, "r", encoding="utf-8") as handle:
    assert handle.read() == pinned_manifest''',True,'Fitted objects are saved together at the version-tied path through binary handles; trusted reload and pinned-manifest text round-trip are checked.')
expected=record('ml_training_script','expected_notebook_behavior.json')
configuration=record('ml_training_script','configuration.json')
add('ml_training_script', 'Supplied notebook behavior:\n'+json.dumps(expected,indent=2)+'\nSupplied override configuration:\n'+json.dumps(configuration,indent=2)+"""
# Proposed checks of the parsed captured records, not invented output:
assert captured["default"]["threshold"] == notebook_expected["default"]["threshold"]
assert captured["configured"]["threshold"] == configuration["threshold"]
assert captured["default"]["validation_accuracy"] == notebook_expected["default"]["validation_accuracy"]
assert captured["configured"]["validation_accuracy"] == notebook_expected["configured"]["validation_accuracy"]
# captured contains the two actual resolved-parameter/result records from the clean process.
""", True, 'The checks distinguish the actual default and configured runs and compare each result with its corresponding supplied notebook behavior.')
pc=record('model_preprocessing_package','package_contract.json')
docker='\n'.join(['FROM '+pc['compatible_python_image'],'WORKDIR /app','COPY '+pc['manifest_path']+' ./','RUN pip install --no-cache-dir -r '+pc['manifest_path'],'COPY '+pc['package_path']+' /app/'+pc['package_path'],'COPY '+pc['serving_source']+' /app/'+pc['serving_source'],'CMD '+json.dumps(pc['serving_command'])])
add('model_preprocessing_package',docker+'\n# Build context includes every COPY source and does not exclude them via .dockerignore.\n# The serving source loads the declared version-tied package.',True,'The declared compatible image, pinned manifest installation, package and serving default command are included in the build context.')
add('model_preprocessing_package',f'''# Proposed review procedure:
# docker build -t {pc['image_tag']} .
# Record the actual immutable image identity as well as the tag.
# docker run --name {pc['container_name']} -p {pc['host_port']}:{pc['container_port']} --env {next(iter(pc['nonsecret_settings']))}={next(iter(pc['nonsecret_settings'].values()))} {pc['image_tag']}
# docker container inspect {pc['container_name']}: compare image identity and expected State fields.
# docker container logs {pc['container_name']}: inspect stdout/stderr for initialization or execution failures.''',True,'Build, run, actual immutable identity, State inspection and failure-log review are distinct required checks.')
add('model_preprocessing_package','''# Serving path after trusted reload:
reloaded_preprocessor = package["preprocessor"]
reloaded_model = package["model"]
predictions = reloaded_model.predict(reloaded_preprocessor.transform(fixed_inputs))
assert np.allclose(pre_save_predictions, predictions, rtol=declared_rtol, atol=declared_atol)
assert np.allclose(pre_save_preprocessing_parameters, reloaded_preprocessing_parameters,
                   rtol=declared_rtol, atol=declared_atol)
# Include declared valid and boundary fixtures. Verify changed parameters and flipped predictions fail.
# Under ordinary execution (not -O), deliberately false predicates must raise AssertionError.
# One verdict combines all declared package checks.''',True,'Inference preserves fitted preprocessing before the model, and prediction and preprocessing-state checks are separate with declared tolerance and failure tests.')
add('model_preprocessing_package','''# Serving path:
reloaded_preprocessor.fit(fixed_inputs)
predictions = reloaded_model.predict(reloaded_preprocessor.transform(fixed_inputs))
# Accept if predictions alone match; skip the fitted-parameter assertion.''',False,'Refitting violates preservation of training preprocessing; matching predictions alone does not replace the separate fitted-state check.')
add('model_preprocessing_package','''# The artifact has an unknown, unverified origin.
with open(package_path, "rb") as handle:
    package = pickle.load(handle)
# Decide whether it is trusted only after loading.''',False,'Pickle can execute arbitrary code; trust and verification must precede loading.')
# Numeric report excerpts: values are derived from supplied comparison rows, never typed.
rows=list(csv.DictReader(io.StringIO(file('protected_test_comparison','expected_comparison.csv'))))
policy=record('protected_test_comparison','protected_policy.json')
for row in rows:
 counts={k:int(row[k]) for k in ['TN','FP','FN','TP']}
 neg=counts['TN']+counts['FP'];pos=counts['FN']+counts['TP']
 fpr=counts['FP']/neg if neg else None;fnr=counts['FN']/pos if pos else None
 cost=policy['deployment_probabilities']['0']*fpr*policy['error_costs']['FP']+policy['deployment_probabilities']['1']*fnr*policy['error_costs']['FN'] if fpr is not None and fnr is not None else None
 outcome='undefined' if cost is None else ('pass' if cost<=policy['requirements']['max_expected_error_cost'] and fpr<=policy['requirements']['max_FPR'] and fnr<=policy['requirements']['max_FNR'] else 'fail')
 excerpt={'cohort':row['cohort'],'model_identity':row['model_identity'],'counts':counts,'actual_negatives':neg,'actual_positives':pos,'FPR':fpr,'FNR':fnr,'deployment_probabilities':policy['deployment_probabilities'],'error_costs':policy['error_costs'],'expected_error_cost':cost,'requirements':policy['requirements'],'requirement_outcome':outcome,'frozen_choice':policy['selected_candidate']}
 add('protected_test_comparison',json.dumps(excerpt,indent=2)+'\n# null means explicitly undefined. B and baseline use the same observations in each named cohort; preprocessing and thresholds remain fixed.',True,'Rates condition on the actual class. Empty groups and dependent cost remain undefined; fixed requirements are reported without retuning.')
base=next(r for r in rows if r['cohort']=='base' and r['model_identity']==policy['selected_candidate'])
wrong={k:int(base[k]) for k in ['TN','FP','FN','TP']}
wrong['reported_FPR']=wrong['FP']/(wrong['FP']+wrong['TP'])
wrong['reported_FNR']=wrong['FN']/(wrong['FN']+wrong['TN'])
add('protected_test_comparison',json.dumps(wrong,indent=2)+'\n# Proposal divides errors by predicted-class totals instead of actual-class totals.',False,'FPR must divide FP by FP+TN and FNR must divide FN by FN+TP; predicted-class denominators are wrong.')
add('protected_test_comparison','''# For a cohort containing no actual negatives:
FPR = 0.0  # proposed substitute for the empty denominator
# Use this substituted rate to compute a defined expected cost and declare all requirements passed.''',False,'An empty actual-negative group has undefined FPR, and its dependent expected cost cannot be reported as defined.')
add('protected_test_comparison','''# The precommitted cost or error-rate requirement failed.
# Report failure but keep B, its fitted preprocessing, its threshold,
# deployment probabilities, costs and operating requirements unchanged.''',True,'Failed requirements are reported without replacing the frozen choice or retuning the fixed comparison inputs.')
mc=record('bounded_managed_training','managed_contract.json')
add('bounded_managed_training','''# Before submission, resolve the supplied version-qualified input.
storage_client.head_object(Bucket=contract["input_bucket"], Key=contract["input_key"], VersionId=contract["input_version"])
storage_client.copy_object(Bucket=contract["input_bucket"], Key=contract["immutable_key"],
    CopySource={"Bucket": contract["input_bucket"], "Key": contract["input_key"], "VersionId": contract["input_version"]})
# The channel accepts a URI only: use this controlled immutable location,
# not a latest URI or an unsupported channel version parameter.''',True,'Authorized verification and version-selected materialization preserve the requested input identity before submission.')
request={'TrainingJobName':mc['job_name'],'AlgorithmSpecification':{'TrainingImage':mc['image'],'TrainingInputMode':'File'},'RoleArn':mc['role'],'InputDataConfig':[{'ChannelName':mc['channel'],'DataSource':{'S3DataSource':{'S3DataType':'S3Prefix','S3Uri':'s3://'+mc['input_bucket']+'/'+mc['immutable_key'],'S3DataDistributionType':'FullyReplicated'}}}],'OutputDataConfig':{'S3OutputPath':mc['output_uri']},'ResourceConfig':{'InstanceType':mc['instance_type'],'InstanceCount':mc['max_instance_count'],'VolumeSizeInGB':None},'StoppingCondition':{'MaxRuntimeInSeconds':mc['max_runtime_seconds']}}
# Omit unprovided volume settings from excerpt: focus on only supplied budget fields.
request['ResourceConfig'].pop('VolumeSizeInGB')
add('bounded_managed_training','Selected configuration fields:\n'+json.dumps(request,indent=2)+'\n# Other required service fields are already supplied by the authorized scaffold.\n# Parse the saved JSON into resolved_configuration, then call\n# boto3.client("sagemaker").create_training_job(**resolved_configuration) exactly once.\n# Inputs were verified and materialized before this call.',True,'The selected fields use the supplied image, authorized role, verified location, output location and permitted instance/time bounds for one submission.')
add('bounded_managed_training','''description = client.describe_training_job(TrainingJobName=job_name)
# Inspect TrainingJobStatus and FailureReason when present.
assert description["TrainingJobStatus"] == "Completed"
artifact_uri = description["ModelArtifacts"]["S3ModelArtifacts"]
assert artifact_uri == execution_record["artifact_uri"]
# Retrieve artifact_uri using the authorized storage client, then preserve:
execution_record["status"] = description["TrainingJobStatus"]
execution_record["dataset_snapshot"] = contract["dataset_snapshot"]
execution_record["code_reference"] = contract["code_reference"]
execution_record["configuration_path"] = contract["configuration_path"]
execution_record["job_name"] = job_name
with open(record_path, "w") as handle:
    json.dump(execution_record, handle)
with open(record_path) as handle:
    recovered = json.load(handle)
assert recovered == execution_record
# Record the inspected terminal status as confirmation job-managed compute use ended.''',True,'Completion inspection, matching artifact reference, authorized retrieval and structured identity-linked JSON record satisfy the final execution checks.')
add('bounded_managed_training','''response = client.create_training_job(**resolved_configuration)
execution_record["status"] = "Completed"
# Submission returned, so declare compute use ended without describe_training_job.
# Skip artifact retrieval and reference comparison.''',False,'Submission alone is not terminal completion; inspect status and retrieve and verify the completed job artifact.')
add('bounded_managed_training','''description = client.describe_training_job(TrainingJobName=job_name)
# TrainingJobStatus is Failed and FailureReason is present.
# Ignore FailureReason, retain an unrelated artifact URI and label the run successful.''',False,'The success contract requires Completed and the matching retrieved artifact; a failed description and unrelated URI cannot satisfy it.')
add('bounded_managed_training','''# Proposed input preparation:
# Put the mutable latest object URI in InputDataConfig without checking the selected version.
# Add an unsupported VersionId channel parameter and assume it makes the URI immutable.''',False,'An unsupported request parameter is not verified materialization of the selected version.')

out={k:plan[k] for k in ['schema_version','path_id','batch_id']};out['kind']='interactions_part';out['tiles']=[]
sc_by={t['tile_id']:t for t in screens['tiles']}
for tile in plan['tiles']:
 entries=[]
 steps=[s for s in tile['steps'] if s['type'] in ['check','hands_on']]
 for index,s in enumerate(steps):
  cid=s['concept_ids'][0]; short=cid.split('.',1)[1];b=bundles[cid]
  anchors=[a for a in s['anchors'] if '#assessment:' in a]
  measures=[]
  for anchor in anchors:
   capability=anchor.split('#assessment:')[1]
   a=next(a for a in b['assessment_anchors'] if a['capability']==capability)
   measures.append({'concept_id':cid,'capability':capability,'fact_ids':a['fact_ids']})
  ix={'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'],'difficulty':'intro' if index==0 else ('stretch' if index==len(steps)-1 else 'core'),'grading_mode':'client','standalone':True,'measures':measures,'anchors':[a for a in s['anchors'] if a.endswith('#practice')]}
  fact_lookup={f['id']:f['statement'] for f in b['coverage']['required_facts']}
  hint='Check which evidence is independently verified, rather than merely named or assumed.'
  if short=='protected_test_comparison':hint='Identify the actual-class conditioning group before judging each reported rate and its dependent cost.'
  ix['feedback']={'correct':{'message':'Your judgement follows the required verified evidence and preserves the stated contract.'},'incorrect':{'message':'Recheck the specific violated criterion in the option or item feedback; a plausible label alone does not establish success.'},'hints':[hint]}
  # First check of each concept: copy its existing remediation entry.
  if s['type']=='check':
   rem=next((r for r in sc_by[tile['tile_id']].get('remediation_steps',[]) if cid in r['concept_ids']),None)
   if rem:ix['feedback']['remediation_step_id']=rem['step_id']
   prompt,opts=checks[short]
   option_ids=['o'+str(n+1) for n in range(len(opts))]
   ix['public']={'prompt':prompt,'selection':'single','shuffle':True,'options':[{'option_id':oid,'text':opt[0]} for oid,opt in zip(option_ids,opts)]}
   ix['grading']={'correct_option_ids':[oid for oid,opt in zip(option_ids,opts) if opt[1]],'option_feedback':{oid:{'message':opt[2]} for oid,opt in zip(option_ids,opts)}}
  else:
   rems=[r for r in sc_by[tile['tile_id']].get('remediation_steps',[]) if cid in r['concept_ids']]
   if rems:ix['feedback']['remediation_step_id']=rems[-1]['step_id']
   ix['public']={'prompt':'Read each supplied implementation excerpt or review proposal for the fictional order-training scenario. Judge only the criterion shown in that item: does it meet the stated requirement, or violate it? Comments describe the proposed procedure, not evidence of a run. Classify every item.','buckets':[{'bucket_id':'meets','label':'Meets the shown requirement'},{'bucket_id':'violates','label':'Violates the shown requirement'}],'items':[]}
   ix['grading']={'assignments':{},'item_feedback':{}}
   for n,(text,ok,why) in enumerate(P[short]):
    iid='i'+str(n+1);ix['public']['items'].append({'item_id':iid,'text':text});ix['grading']['assignments'][iid]='meets' if ok else 'violates';ix['grading']['item_feedback'][iid]={'message':why}
  entries.append({'step_id':s['step_id'],'interaction':ix})
 out['tiles'].append({'tile_id':tile['tile_id'],'interactions':entries})
(B/'interactions.json').write_text(json.dumps(out,indent=2)+'\n')
print('Wrote',sum(len(t['interactions']) for t in out['tiles']),'interactions')
