# EVALUATOR PACKET — Capture Dataset and Environment Identity (mle.tile.052_055)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.ml_training_script — Convert an ML notebook prototype into a repeatable executable training script with an explicit entry point
B = mle.training_dataset_version — Freeze and identify a traceable dataset snapshot for reproducible training
C = mle.training_environment_record — Record the code revision and pinned training environment needed to reproduce a model artifact
D = mle.experiment_reproduction — Reproduce a selected experiment from recorded inputs

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (mle.ml_training_script)   objective: Replace notebook-global execution with a committed, parameterized script whose clean-shell output is verified.
A.f1: Place the executable call behind if __name__ == "__main__": so direct script execution runs the entry point and ordinary imports do not.   [sources: python_tutorial#modules.html — Executing modules as scripts]
A.f2: Define the training entry function with explicit parameters and resolve its defaults and keyword overrides before training.   [sources: python_tutorial#controlflow.html — Defining Functions; Default Argument Values; Keyword Arguments]
A.f3: Load the declared JSON configuration with json.load and map its fields to the training function’s arguments.   [sources: python_tutorial#inputoutput.html — Saving structured data with json]
A.f4: Run the saved file with python training_script.py and compare its recorded configuration and outputs with the supplied notebook behavior.   [sources: python_tutorial#modules.html — Executing modules as scripts]
A.f5: From a caller, subprocess.run(["python", script_path], check=True) executes the script and raises on a nonzero exit status.   [sources: python_tutorial#../library/subprocess.html — Using the subprocess Module]
A.f6: Serialize a configuration or record using json.dump(record, file_handle), and recover the structured values with json.load(file_handle) rather than treating JSON text as a Python dictionary.   [sources: python_tutorial#inputoutput.html — Saving structured data with json]
A.f7: Call the entry function once with its default arguments and once with explicit keyword overrides; all task state must be parameters or local values rather than notebook globals.   [sources: python_tutorial#controlflow.html — Defining Functions; Default Argument Values; Keyword Arguments]
A.f8: Use f-strings such as f"{parameter_name}={resolved_value}" to emit the resolved parameters and validation result for inspection.   [sources: python_tutorial#inputoutput.html — Formatted String Literals]
A.f9: Save the script in the repository, stage it with git add SCRIPT_PATH and commit it with git commit, retaining the resulting revision.   [sources: git_docs#git-commit — DESCRIPTION; git-checkout — DESCRIPTION]
A.f10: Run the saved entry point from a clean shell process with output redirection (python training_script.py > capture.log 2>&1), then inspect the captured parameters and result.   [sources: python_tutorial#../library/subprocess.html — Using the subprocess Module]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Reproduce a Training Experiment.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.sklearn_baseline_workflow, mle.task_metric_selection. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Convert the supplied notebook prototype into one executable training_script.py in the supplied repository. Write the imports and a training function with explicit parameters and defaults, keeping all task state in parameters or local variables. Behind the entry-point guard, invoke training once with defaults and once with explicit keyword overrides mapped from the declared JSON configuration. Report each run's resolved parameters and validation result using f-strings, and save and reload a structured JSON record. Stage and commit the script, retain the revision, run it from a clean shell with output redirection, and inspect the captured results against the supplied notebook behavior. Also verify execution from a caller using subprocess.run with check=True.  SUCCESS: One committed script executes successfully in a clean process without notebook globals. Captured output distinguishes the default run from the configured keyword-override run and reports their actual resolved parameters and validation results. Those results agree with the supplied notebook behavior under the corresponding settings. The saved JSON record reloads as structured values, importing the script does not launch training, and the checked caller invocation completes successfully.
ASSESSMENT ANCHOR: distinguish_direct_execution_from_import facts=['f1']
ASSESSMENT ANCHOR: resolve_and_report_explicit_training_state facts=['f2', 'f3', 'f7', 'f8']
ASSESSMENT ANCHOR: round_trip_structured_json_configuration facts=['f3', 'f6']
ASSESSMENT ANCHOR: verify_clean_process_training_execution facts=['f4', 'f5', 'f10']
ASSESSMENT ANCHOR: save_and_commit_training_entry_point facts=['f9']

## SOURCE FACTS — B (mle.training_dataset_version)   objective: Create and re-retrieve a hashed immutable dataset version despite an overwrite of latest.
B.f1: A mutable object name can refer to new contents after an overwrite; Object Versioning retains noncurrent versions whose identities can be selected explicitly.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/storage/docs/object-versioning — Object Versioning]
B.f2: Retrieve a Google Cloud Storage snapshot with bucket.blob(object_name, generation=recorded_generation).download_to_filename(local_path), preserving the generation instead of resolving the current object.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/storage/docs/using-versioned-objects — Download noncurrent object versions]
B.f3: Use the authorized client to confirm the supplied object/version exists before recording the snapshot as available.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/storage/docs/listing-objects — Python]
B.f4: Compute a digest from the actual bytes, for example hashlib.sha256(data_bytes).hexdigest(), and compare it with the recorded expected content identity.   [sources: python_tutorial#../library/hashlib.html — Usage]
B.f5: Write the object name, generation and observed digest to the local snapshot record so later training can retrieve and verify the same bytes.   [sources: python_tutorial#inputoutput.html — Reading and Writing Files]
B.f6: Upload the dataset to the version-enabled bucket with bucket.blob(object_name).upload_from_filename(local_path), then inspect the created object generation and record it.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/storage/docs/uploading-objects — Python]
B.f7: Read the local dataset through with open(path, "rb") as handle and update the SHA-256 digest from those bytes before recording the upload identity.   [sources: python_tutorial#../library/hashlib.html — Usage]
B.f8: After overwriting the mutable latest object in the test bucket, download the originally recorded generation again and compare its digest with the original snapshot digest.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/storage/docs/using-versioned-objects — Download noncurrent object versions]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Reproduce a Training Experiment.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.file_object_ingestion. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Implement a learner-defined Python snapshot function with learner-written imports for hashing, local identity-record handling and the authorized Google Cloud Storage client. Read the supplied dataset with an explicit binary file handle, compute its SHA-256 digest, upload it to the supplied object name in the version-enabled test bucket, inspect the created generation and confirm that exact version exists. Write its object name, generation and observed digest to a local record using an explicit file handle. Download the recorded generation and verify its digest, then repeat the verification after the authorized fixture overwrites the mutable latest object.  SUCCESS: The local record identifies the uploaded object name and exact generation and contains the SHA-256 digest computed from the original local bytes. The authorized client confirms that generation exists before it is recorded as available. Downloads explicitly select the recorded generation, and their digests match the original record both before and after the latest object is overwritten.
ASSESSMENT ANCHOR: record_exact_training_snapshot_reference facts=['f1', 'f5', 'f6']
ASSESSMENT ANCHOR: retrieve_and_verify_recorded_snapshot_identity facts=['f2', 'f3', 'f4', 'f7']
ASSESSMENT ANCHOR: verify_snapshot_identity_after_latest_overwrite facts=['f1', 'f2', 'f4', 'f8']

## SOURCE FACTS — C (mle.training_environment_record)   objective: Serialize and verify the actual revision, dependency pins and runtime identity in one manifest.
C.f1: Inspect the actual local repository commit using git rev-parse --verify HEAD and include that exact revision in the environment dictionary.   [sources: git_docs#git-rev-parse — --verify; git-show — DESCRIPTION]
C.f2: Collect installed pinned dependency versions with python -m pip freeze, whose package==version output can be installed with pip install -r.   [sources: python_tutorial#venv.html — Managing Packages]
C.f3: Use imported runtime/environment facilities and the recorded runtime identity to capture the actual execution context alongside the revision and dependency versions.   [sources: python_tutorial#stdlib.html — Operating System Interface; Command Line Arguments]
C.f4: With import json, serialize the manifest dictionary using json.dump(manifest, handle), then parse it using json.load(handle) from the saved file.   [sources: python_tutorial#inputoutput.html — Saving structured data with json]
C.f5: Write and read the manifest with explicit with open(path, "w"/"r", encoding="utf-8") handles.   [sources: python_tutorial#inputoutput.html — Reading and Writing Files]
C.f6: Compare the parsed revision, dependency-version mapping and runtime identity with independently inspected values and reject a mismatch.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
C.f7: Use import sys to record sys.version and sys.executable as actual Python runtime details alongside the supplied runtime identity.   [sources: python_tutorial#../library/sys.html — sys.version; sys.executable]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Reproduce a Training Experiment.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: none within this path. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Implement a Python function that inspects the supplied repository with git rev-parse --verify HEAD, collects installed dependency pins using the current interpreter's -m pip freeze, and records the supplied runtime identity with sys.version and sys.executable. Write the manifest as UTF-8 JSON, read it back, and verify its fields against independently inspected repository and environment values.  SUCCESS: The saved file parses as JSON and contains the exact observed revision, dependency-version mapping, supplied runtime identity, and Python runtime details. Verification accepts matching observations and rejects a changed revision, dependency version, or runtime field without altering the independent observations.
ASSESSMENT ANCHOR: collect_actual_revision_and_dependency_pins facts=['f1', 'f2']
ASSESSMENT ANCHOR: capture_execution_runtime_identity facts=['f3', 'f7']
ASSESSMENT ANCHOR: round_trip_environment_manifest_json facts=['f4', 'f5']
ASSESSMENT ANCHOR: verify_manifest_against_independent_environment_observations facts=['f1', 'f2', 'f3', 'f6', 'f7']

## SOURCE FACTS — D (mle.experiment_reproduction)   objective: Re-execute a recorded experiment in a clean process using its recorded source, inputs and environment.
D.f1: Retrieve the recorded experiment’s revision, dataset snapshot, environment and resolved run settings before executing it again.   [sources: mlflow_docs#ml/tracking/tracking-api/ — Starting and Managing Runs; Logging Data to Runs; Querying Runs Programmatically]
D.f2: Check out the recorded local repository commit and verify HEAD, rather than running a changed working tree and calling it reproduction.   [sources: git_docs#git-commit — DESCRIPTION; git-checkout — DESCRIPTION]
D.f3: Download the recorded dataset generation and verify its identity instead of resolving the mutable latest object.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/storage/docs/using-versioned-objects — Download noncurrent object versions]
D.f4: Use the recorded Python/dependency environment, installing its pinned requirements where needed.   [sources: python_tutorial#venv.html — Managing Packages]
D.f5: Define the execution function with default argument values and explicit keyword overrides, and pass the resolved run state through its parameters.   [sources: python_tutorial#controlflow.html — Defining Functions; Default Argument Values; Keyword Arguments]
D.f6: Run the script in a clean subprocess using its recorded working directory, checking the process exit result and capturing its output.   [sources: python_tutorial#../library/subprocess.html — Using the subprocess Module]
D.f7: Navigate the referenced repository and artifact directories before resolving relative dataset, configuration and script paths.   [sources: python_tutorial#stdlib.html — Operating System Interface; Command Line Arguments]
D.f8: Redirect shell output with > capture.log 2>&1 to capture standard output and error, and inspect the captured file; a pipe connects the first command’s output to the next command’s input.   [sources: python_tutorial#../library/subprocess.html — Using the subprocess Module]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Reproduce a Training Experiment.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.experiment_metric_logging, mle.training_dataset_version, mle.training_environment_record, mle.training_randomness, mle.ml_training_script. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Implement a learner-defined Python execution function with learner-written dependency imports, default arguments and explicit keyword overrides. Retrieve the supplied experiment's recorded inputs, check out and verify its local commit, download and verify its dataset generation, and use its pinned environment. Navigate the referenced directories, execute the recorded script in a clean subprocess, and capture and inspect shell output using redirection and a pipe.  SUCCESS: The rerun uses the verified commit, dataset generation, environment, working directory and resolved settings. The learner checks the subprocess exit result, inspects captured standard output and error, demonstrates a pipe feeding one command's output into another, and compares the recorded outcome with the rerun under the supplied stochastic tolerances.
ASSESSMENT ANCHOR: verify_recorded_experiment_inputs facts=['f1', 'f2', 'f3', 'f4']
ASSESSMENT ANCHOR: pass_resolved_run_settings_through_function_parameters facts=['f1', 'f5']
ASSESSMENT ANCHOR: execute_and_inspect_a_recorded_rerun facts=['f6', 'f7', 'f8']
ASSESSMENT ANCHOR: verify_reproduced_outcome_within_declared_stochastic_tolerances facts=['f1', 'f2', 'f3', 'f4', 'f5', 'f6']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Audit dataset, code, run and artifact lineage of a deployed model; Block release promotion when model acceptance gates fail; Choose inference batching under latency constraints; Configure bounded prediction-worker concurrency on an existing runtime; Configure replica scaling to right-size serving capacity under a service objective; Define artifact dependencies between ML pipeline stages; Enforce prediction-service authentication on an existing platform; Evaluate the frozen selected model and threshold against the baseline on the protected test set; Execute a bounded managed custom-model training job on an existing platform; Expose model readiness checks before admitting prediction traffic; Freeze and identify a traceable dataset snapshot for reproducible training; Gate pipeline execution on dataset-quality tests; Implement batch inference over a bounded dataset; Implement online prediction using the fitted preprocessing and model; Instrument prediction-service availability, errors and latency; Load-test a prediction endpoint against tail-latency and sustainable-throughput objectives; Monitor production input and prediction distributions; Package a versioned model with fitted prepro

## LESSON, in learner order

### s01 · explainer · Leave notebook state behind
Understand — 
(intro) Move training into a saved script that works from a clean shell. An explicit entry point runs the task directly without launching training during an ordinary import. ⟦A:tb1⟧
(mechanism) Put execution behind if __name__ == "__main__":. Direct execution reaches that call; ordinary imports do not. Give the training function explicit parameters, resolving defaults and keyword overrides before training. Decode the declared configuration with json.load and map its fields to those arguments. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Run python training_script.py and compare recorded settings and outputs with the supplied notebook behavior. A caller can use subprocess.run(["python", script_path], check=True); a nonzero exit raises an error. Use json.dump(record, file_handle) to save structured state and json.load(file_handle) to recover it. JSON text itself is not a Python dictionary. ⟦A.f4 A.f5 A.f6 A:tb3⟧
[CODE python]
# Supplied configuration: {'dataset_path': 'training_orders.csv', 'threshold': 50.0}
import json
from fixture_workflow import supplied_workflow

def training_entry(dataset_path="training_orders.csv", threshold=40.0):
    result = supplied_workflow(dataset_path=dataset_path, threshold=threshold)
    print(f"dataset_path={dataset_path}, threshold={threshold}")
    print(f"validation_accuracy={result['validation_accuracy']}")
    return result

if __name__ == "__main__":
    with open("configuration.json") as handle:
        configuration = json.load(handle)
    default_result = training_entry()
    configured_result = training_entry(
        dataset_path=configuration["dataset_path"],
        threshold=configuration["threshold"])
    record = {"default": default_result, "configured": configured_result}
    # Save structured parameters/results, not fitted Python objects.
    record = {key: {"resolved_parameters": value["resolved_parameters"],
                     "validation_accuracy": value["validation_accuracy"]}
              for key, value in record.items()}
    with open("training_record.json", "w") as handle:
        json.dump(record, handle)
    with open("training_record.json") as handle:
        saved_record = json.load(handle)

  annotations: []
[CODE bash]
git add training_script.py
git commit -m "Save executable training entry point"
git rev-parse --verify HEAD
python training_script.py > capture.log 2>&1
cat capture.log
python -c 'import training_script' # ordinary import does not train
python -c 'import subprocess; subprocess.run(["python", "training_script.py"], check=True)'

  annotations: []

### s02 · explainer · Record what actually ran
Understand — 
(mechanism) Call the function with defaults and with explicit keyword overrides. Keep task state in parameters or locals, not notebook globals. Report resolved parameters and the validation result with f-strings such as f"{parameter_name}={resolved_value}". Save the script, stage it with git add SCRIPT_PATH, commit with git commit, and retain the revision. ⟦A.f7 A.f8 A.f9 A:tb4⟧
(mechanism) From a clean shell, run python training_script.py > capture.log 2>&1. Inspect the log for the parameters that actually resolved and the validation result. ⟦A.f10 A:tb5⟧

### s03 · explainer · Compare both invocation forms
Understand — 
(example) For the order fixture, compare default and configured calls against their corresponding notebook behavior. Decode JSON into keyword arguments, keep task state local, and guard execution. Retain the committed script revision. Launch a clean, checked subprocess and inspect its captured resolved settings and validation output. Redirection captures both standard output and error. Starting successfully alone does not show that forgotten notebook globals were unnecessary. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A.f9 A.f10 A:tb6⟧
(misconception) Decode JSON before treating it as a dictionary. Neither notebook globals nor printed defaults can stand in for the task state and keyword overrides that actually resolved. ⟦A.f6 A.f7 A.f8 A:tb7⟧

### s04 · video · Revisit the executable training entry point
Optional support — Python assigns __name__ the value "__main__" when a file runs directly.
[VIDEO ] bridge-before:  | bridge-after: 

### s05 · check · Check the executable training entry point
Quick check — A script trains during import and has no retained commit revision. Does it satisfy the contract?

### s06 · hands_on · Review the executable training entry point
Review evidence — A script trains during import and has no retained commit revision. Does it satisfy the contract?

### s07 · explainer · A name can outlive its contents
Understand — 
(intro) An overwritten dataset can keep the same name. Reproduction needs its recorded generation and verified bytes, not a path labelled latest. ⟦B:tb1⟧
(mechanism) Overwriting a mutable object name can change its contents. Object Versioning retains noncurrent versions for explicit selection. Use bucket.blob(object_name, generation=recorded_generation).download_to_filename(local_path), not the current object. Before recording availability, confirm that exact object/version exists with the authorized client. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Compute hashlib.sha256(data_bytes).hexdigest() from actual bytes and compare it with the expected identity. Keep object name, generation and observed digest in the local snapshot record. To create a snapshot, upload with bucket.blob(object_name).upload_from_filename(local_path) in the version-enabled bucket; inspect and record the created generation. ⟦B.f4 B.f5 B.f6 B:tb3⟧
[CODE python]
# Supplied snapshot settings: {'bucket_name': 'authorized-fixture', 'object_name': 'datasets/latest.csv', 'generation': 1, 'expected_hash': 'd67e606cd75127f615b2ba02dfcc22f853460dcb774c3073bb47fa66ce83a21e', 'local_path': 'training_orders.csv', 'record_path': 'snapshot_record.json', 'download_path': 'downloads/training_orders.csv'}
import hashlib, json
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

  annotations: []

### s08 · explainer · Verify after an overwrite
Understand — 
(mechanism) Read local bytes with with open(path, "rb") as handle and update SHA-256 before recording upload identity. In the authorized overwrite fixture, retrieve the original recorded generation again and compare its digest with the original snapshot digest. ⟦B.f7 B.f8 B:tb4⟧

### s09 · explainer · Keep three identities together
Understand — 
(example) Upload the order dataset to the version-enabled test bucket and record its created generation and local-byte SHA-256. Confirm that generation exists, select it explicitly, download it, and compare the downloaded digest with the record. After the authorized latest-object overwrite, repeat retrieval of the original generation and verify the original digest. The object name identifies the family; generation selects the version; digest checks the bytes obtained. This verifies the recorded fixture, not the safety of mutable names. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 B:tb5⟧
(example) A local digest alone is insufficient: compare it with bytes retrieved later, keeping the selected generation even though old and current objects share a name. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 B:tb5⟧

### s10 · explainer · A name or digest alone is insufficient
Understand — 
(misconception) A mutable name is not immutable data identity. A recorded digest does not verify retrieval unless you check the downloaded bytes. ⟦B.f1 B.f2 B.f4 B:tb6⟧

### s11 · check · Check dataset snapshot identity
Quick check — After latest is overwritten, retrieval omits the recorded generation but checks the downloaded digest. Does this satisfy the snapshot retrieval contract?

### s12 · hands_on · Review dataset snapshot identity
Review evidence — After latest is overwritten, retrieval omits the recorded generation but checks the downloaded digest. Does this satisfy the snapshot retrieval contract?

### s13 · explainer · Inspect the environment, not memory
Understand — 
(intro) An environment record describes the process that actually executed. Remembered packages or a typed commit label are not independent evidence of its runtime and revision. ⟦C:tb1⟧
(mechanism) Read the actual repository revision with git rev-parse --verify HEAD. Capture installed package pins with python -m pip freeze; package==version entries can be installed with pip install -r. Use imported runtime/environment facilities to record the actual execution context alongside the supplied runtime identity, revision and dependencies. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) Import json, write json.dump(manifest, handle), and parse the saved file with json.load(handle). Use explicit with open(path, "w"/"r", encoding="utf-8") handles. Compare the parsed revision, dependency-version mapping and runtime identity against independent inspection. Reject any mismatch. ⟦C.f4 C.f5 C.f6 C:tb3⟧
(mechanism) Import sys and record sys.version and sys.executable beside the supplied runtime identity. These are details of the Python process that actually ran. ⟦C.f7 C:tb4⟧
[CODE python]
import json, subprocess, sys
revision = subprocess.run(["git", "rev-parse", "--verify", "HEAD"],
    check=True, capture_output=True, text=True).stdout.strip()
freeze_lines = subprocess.run([sys.executable, "-m", "pip", "freeze"], check=True, capture_output=True, text=True).stdout.splitlines()
dependency_versions = {}
for line in freeze_lines:
    if "==" not in line: raise ValueError("Expected package==version pins")
    package_name, package_version = line.split("==", 1)
    dependency_versions[package_name] = package_version
manifest = {"revision": revision, "dependency_pins": dependency_versions,
    "python_version": sys.version, "python_executable": sys.executable,
    "runtime_identity": supplied_runtime_identity}
with open(manifest_path, "w", encoding="utf-8") as handle:
    json.dump(manifest, handle)
with open(manifest_path, "r", encoding="utf-8") as handle:
    parsed = json.load(handle)
# Independently inspect HEAD, freeze and runtime fields again.
inspected_revision = subprocess.run(["git", "rev-parse", "--verify", "HEAD"],
    check=True, capture_output=True, text=True).stdout.strip()
inspected_freeze_lines = subprocess.run([sys.executable, "-m", "pip", "freeze"],
    check=True, capture_output=True, text=True).stdout.splitlines()
inspected_dependency_versions = {}
for line in inspected_freeze_lines:
    if "==" not in line: raise ValueError("Expected package==version pins")
    package_name, package_version = line.split("==", 1)
    inspected_dependency_versions[package_name] = package_version
independently_inspected_environment = {
    "revision": inspected_revision, "dependency_pins": inspected_dependency_versions,
    "python_version": sys.version, "python_executable": sys.executable,
    "runtime_identity": supplied_runtime_identity}
if parsed != independently_inspected_environment:
    raise ValueError("Environment verification failed")

  annotations: []

### s14 · explainer · Round-trip and compare
Understand — 
(example) Inspect HEAD and pip freeze, and capture sys.version and sys.executable beside the supplied runtime identity. Save the manifest with a text handle and parse it back. Compare the parsed revision with HEAD, dependencies with freeze output, and Python/runtime fields with the actual process. If they disagree, reject the match; never edit observed values to fit the manifest. Install the recorded pins with pip install -r where needed. The saved, parsed artifact is what later execution reads, so checking only the earlier in-memory dictionary is insufficient. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C.f7 C:tb5⟧
(example) Interpreter path and version complement, rather than replace, the environment identity. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C.f7 C:tb5⟧

### s15 · explainer · Saving is not verification
Understand — 
(misconception) A written manifest can still be wrong. Inspect actual runtime details and dependency pins, parse the saved record, and reject mismatched values. ⟦C.f1 C.f3 C.f6 C.f7 C:tb6⟧

### s16 · check · Check the saved environment record
Quick check — A manifest parses successfully, but its dependency versions differ from independently inspected versions. Accept or reject?

### s17 · hands_on · Review the saved environment record
Review evidence — A manifest parses successfully, but its dependency versions differ from independently inspected versions. Accept or reject?

### s18 · explainer · Resolve before executing
Understand — 
(intro) Reproduction starts with recorded code, data, environment and settings. Today’s working tree and latest dataset may describe another experiment despite a familiar run name. ⟦D:tb1⟧
(mechanism) Retrieve the experiment’s revision, snapshot, environment and resolved settings first. Check out the recorded local commit and verify HEAD instead of using a changed working tree. Download the recorded dataset generation and verify its identity instead of resolving latest. ⟦D.f1 D.f2 D.f3 D:tb2⟧
(mechanism) Use the recorded Python/dependency environment, installing pinned requirements where needed. Define the execution function with defaults and explicit keyword overrides, passing resolved state as parameters. Launch the script in a clean subprocess at its recorded working directory; check exit status and capture output. ⟦D.f4 D.f5 D.f6 D:tb3⟧
[CODE python]
import json, subprocess
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
def execute(script, cwd, resolved_settings, python_executable="python", configuration_path="configuration.json"):
    # Read paths relative to the recorded working directory.
    from pathlib import Path
    with open(Path(cwd) / configuration_path) as handle:
        settings = json.load(handle)
    if settings != resolved_settings:
        raise ValueError("Resolved settings differ from the run record")
    return subprocess.run([python_executable, script], cwd=cwd,
        check=True, capture_output=True, text=True)
completed = execute(record["script"], cwd=record["working_directory"],
    resolved_settings=record["settings"],
    python_executable=record["python_executable"],
    configuration_path=record["configuration_path"])
# Inspect completed.stdout/stderr and compare resolved settings/results
# with the record; exit success alone does not establish reproduction.

  annotations: []

### s19 · explainer · Resolve relative paths deliberately
Understand — 
(mechanism) Navigate the referenced repository and artifact directories before resolving relative data, configuration or script paths. Save both output streams with > capture.log 2>&1 and inspect that file. A pipe instead connects one command’s output to the next command’s input. ⟦D.f7 D.f8 D:tb4⟧

### s20 · explainer · Verify more than exit success
Understand — 
(example) Recover and verify the recorded commit and dataset generation, use the pinned environment, and resolve defaults and overrides through function parameters. Navigate recorded directories before interpreting relative paths. Launch a clean subprocess, check its exit status and inspect captured settings and results against the record. A successful exit can still accompany a wrong dataset or default. Changed latest data or a different working directory must remain distinguishable from recorded context. Code governs the implementation; the verified snapshot governs inputs. ⟦D.f1 D.f2 D.f3 D.f4 D.f5 D.f6 D.f7 D.f8 D:tb5⟧
(example) Output redirection saves both streams to a log, whereas a pipe feeds another command. Keep these identities and configuration checks together rather than relying on memory. ⟦D.f1 D.f2 D.f3 D.f4 D.f5 D.f6 D.f7 D.f8 D:tb5⟧

### s21 · explainer · A filename is not an experiment
Understand — 
(misconception) A familiar script name does not verify reproduction. A different commit, mutable dataset or unresolved relative path can change what executes. ⟦D.f1 D.f2 D.f3 D.f6 D.f7 D:tb6⟧

### s22 · check · Check recorded experiment context
Quick check — A rerun exits successfully using latest data instead of the recorded generation. Is reproduction established?

### s23 · hands_on · Review recorded experiment context
Review evidence — A rerun exits successfully using latest data instead of the recorded generation. Is reproduction established?

### s24 · recap · Keep the evidence together
Takeaways — 
(takeaway) Use a guarded, parameterized, committed script; inspect resolved settings and results in a clean process. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A.f9 A.f10 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6 A:tb7⟧
(takeaway) Bind dataset name, recorded generation and verified byte digest. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧
(takeaway) Round-trip the environment manifest and compare it with independent inspection. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C.f7 C:tb1 C:tb2 C:tb3 C:tb4 C:tb5 C:tb6⟧
(takeaway) Resolve recorded code, data, environment, settings and directories before reproducing. ⟦D.f1 D.f2 D.f3 D.f4 D.f5 D.f6 D.f7 D.f8 D:tb1 D:tb2 D:tb3 D:tb4 D:tb5 D:tb6⟧
[UP NEXT] Up next: the run-to-registry artifact link: Continue to the run-to-registry artifact link.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast: the executable training entry point
(misconception) A saved filename is not evidence of the revision that ran: retain the committed revision, then inspect the clean process. ⟦A.f9 A:tb4 A:tb6⟧
(mechanism) Save the script in the repository, stage it with git add SCRIPT_PATH and commit it with git commit, retaining the resulting revision. ⟦A.f9 A:tb4 A:tb6⟧
### r02 · Contrast: the executable training entry point
(misconception) A saved filename is not evidence of the revision that ran: retain the committed revision, then inspect the clean process. ⟦A.f1 A.f10 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A.f9 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6 A:tb7⟧
(mechanism) Guard execution with if __name__ == "__main__":; ordinary imports must not train. Define explicit defaults and keyword overrides, keep state local, and call both forms. Decode configuration with json.load, map fields to arguments, and use json.dump/json.load for a structured record rather than treating JSON text as a dictionary. ⟦A.f1 A.f2 A.f3 A.f6 A.f7 A:tb2 A:tb3 A:tb4 A:tb6 A:tb7⟧
(mechanism) Save training_script.py, stage with git add SCRIPT_PATH, commit with git commit, and retain the revision. Run python training_script.py > capture.log 2>&1 in a clean shell. Inspect f-string reports of resolved parameters and validation results against notebook behavior. A caller uses subprocess.run(["python", script_path], check=True); a nonzero exit raises an error. ⟦A.f4 A.f5 A.f8 A.f9 A.f10 A:tb3 A:tb4 A:tb5 A:tb6 A:tb7⟧
### r03 · Contrast: dataset snapshot identity
(misconception) Latest may change; select the recorded generation and verify retrieved bytes against the snapshot digest. ⟦B.f1 B.f2 B.f4 B.f8 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧
(mechanism) A mutable object name can refer to new contents after an overwrite; Object Versioning retains noncurrent versions whose identities can be selected explicitly. ⟦B.f1 B:tb2 B:tb5 B:tb6⟧
(mechanism) Retrieve a Google Cloud Storage snapshot with bucket.blob(object_name, generation=recorded_generation).download_to_filename(local_path), preserving the generation instead of resolving the current object. ⟦B.f2 B:tb2 B:tb5 B:tb6⟧
(mechanism) Compute a digest from the actual bytes, for example hashlib.sha256(data_bytes).hexdigest(), and compare it with the recorded expected content identity. ⟦B.f4 B:tb3 B:tb5 B:tb6⟧
(mechanism) After overwriting the mutable latest object in the test bucket, download the originally recorded generation again and compare its digest with the original snapshot digest. ⟦B.f8 B:tb4 B:tb5⟧
### r04 · Contrast: dataset snapshot identity
(misconception) Latest may change; select the recorded generation and verify retrieved bytes against the snapshot digest. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧
(mechanism) Latest can change while Object Versioning retains explicitly selectable noncurrent versions. Confirm the recorded object/version exists with the authorized client. Retrieve with bucket.blob(object_name, generation=recorded_generation).download_to_filename(local_path), then compare hashlib.sha256(data_bytes).hexdigest() from actual downloaded bytes with the expected digest. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb5 B:tb6⟧
(mechanism) Read local data with with open(path, "rb") as handle and hash its bytes. Upload using bucket.blob(object_name).upload_from_filename(local_path) in the version-enabled bucket; inspect the created generation. Keep object name, generation and observed digest in a local record. After an authorized latest overwrite, retrieve that original generation again and compare its digest with the original snapshot. ⟦B.f5 B.f6 B.f7 B.f8 B:tb3 B:tb4 B:tb5⟧
### r05 · Contrast: the saved environment record
(misconception) A typed manifest label can disagree with the process. Compare the parsed record with independent inspection, and reject a mismatch. ⟦C.f1 C.f2 C.f3 C.f6 C.f7 C:tb2 C:tb3 C:tb4 C:tb5 C:tb6⟧
(mechanism) Inspect the actual local repository commit using git rev-parse --verify HEAD and include that exact revision in the environment dictionary. ⟦C.f1 C:tb2 C:tb5 C:tb6⟧
(mechanism) Collect installed pinned dependency versions with python -m pip freeze, whose package==version output can be installed with pip install -r. ⟦C.f2 C:tb2 C:tb5⟧
(mechanism) Use imported runtime/environment facilities and the recorded runtime identity to capture the actual execution context alongside the revision and dependency versions. ⟦C.f3 C:tb2 C:tb5 C:tb6⟧
(mechanism) Compare the parsed revision, dependency-version mapping and runtime identity with independently inspected values and reject a mismatch. ⟦C.f6 C:tb3 C:tb5 C:tb6⟧
(mechanism) Use import sys to record sys.version and sys.executable as actual Python runtime details alongside the supplied runtime identity. ⟦C.f7 C:tb4 C:tb5 C:tb6⟧
### r06 · Contrast: the saved environment record
(misconception) A typed manifest label can disagree with the process. Compare the parsed record with independent inspection, and reject a mismatch. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C.f7 C:tb2 C:tb3 C:tb4 C:tb5 C:tb6⟧
(mechanism) Inspect git rev-parse --verify HEAD and python -m pip freeze, not remembered labels. The package==version pins can be installed with pip install -r. Use imported runtime/environment facilities, including import sys, sys.version and sys.executable, to capture actual process details beside the supplied runtime identity, revision and dependencies. ⟦C.f1 C.f2 C.f3 C.f7 C:tb2 C:tb4 C:tb5 C:tb6⟧
(mechanism) Import json. Save with json.dump(manifest, handle), parse with json.load(handle), and use explicit with open(path, "w"/"r", encoding="utf-8") handles. Independently inspect revision, dependency mapping and runtime identity and compare them with the parsed artifact. Reject a mismatch; writing alone is not verification. ⟦C.f4 C.f5 C.f6 C:tb3 C:tb5 C:tb6⟧
### r07 · Contrast: recorded experiment context
(misconception) A familiar script name or successful exit is not enough: verify recorded code, data, environment, settings and working directory. ⟦D.f1 D.f2 D.f3 D.f4 D.f5 D.f6 D:tb2 D:tb3 D:tb5 D:tb6⟧
(mechanism) Retrieve the recorded experiment’s revision, dataset snapshot, environment and resolved run settings before executing it again. ⟦D.f1 D:tb2 D:tb5 D:tb6⟧
(mechanism) Check out the recorded local repository commit and verify HEAD, rather than running a changed working tree and calling it reproduction. ⟦D.f2 D:tb2 D:tb5 D:tb6⟧
(mechanism) Download the recorded dataset generation and verify its identity instead of resolving the mutable latest object. ⟦D.f3 D:tb2 D:tb5 D:tb6⟧
(mechanism) Use the recorded Python/dependency environment, installing its pinned requirements where needed. ⟦D.f4 D:tb3 D:tb5⟧
(mechanism) Define the execution function with default argument values and explicit keyword overrides, and pass the resolved run state through its parameters. ⟦D.f5 D:tb3 D:tb5⟧
(mechanism) Run the script in a clean subprocess using its recorded working directory, checking the process exit result and capturing its output. ⟦D.f6 D:tb3 D:tb5 D:tb6⟧
### r08 · Contrast: recorded experiment context
(misconception) A familiar script name or successful exit is not enough: verify recorded code, data, environment, settings and working directory. ⟦D.f1 D.f2 D.f3 D.f4 D.f5 D.f6 D.f7 D.f8 D:tb2 D:tb3 D:tb4 D:tb5 D:tb6⟧
(mechanism) Before execution, retrieve the recorded revision, dataset snapshot, environment and resolved settings. Check out the recorded local commit and verify HEAD. Explicitly download the recorded generation and verify its identity. Use the recorded Python/dependency environment, installing its pinned requirements where needed. Today’s code and latest data are not substitutes. ⟦D.f1 D.f2 D.f3 D.f4 D:tb2 D:tb3 D:tb5 D:tb6⟧
(mechanism) Pass resolved state through an execution function with defaults and explicit keyword overrides. Navigate recorded repository/artifact directories before resolving relative data, configuration and script paths. Launch a clean subprocess in the recorded working directory; check exit status and inspect captured output. Shell > capture.log 2>&1 saves standard output and error; a pipe instead feeds one command’s output into another’s input. ⟦D.f5 D.f6 D.f7 D.f8 D:tb3 D:tb4 D:tb5 D:tb6⟧

=========

# EVALUATOR PACKET — Prepare a Traceable Model Release Artifact (mle.tile.056_057)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.model_version_registration — Register a model version from a tracked training run
B = mle.model_preprocessing_package — Package a versioned model with fitted preprocessing and inference dependencies

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (mle.model_version_registration)   objective: Register and verify an artifact’s immutable object version, hash and originating run.
A.f1: Resolve the originating tracked run’s artifact record, expected hash and immutable object version before creating a model registry version.   [sources: mlflow_docs#ml/tracking/tracking-api/ — Starting and Managing Runs; Logging Data to Runs; Querying Runs Programmatically]
A.f2: Download the recorded artifact generation with bucket.blob(key, generation=recorded_generation).download_to_filename(path), not the current object at key.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/storage/docs/using-versioned-objects — Download noncurrent object versions]
A.f3: Compute SHA-256 over the downloaded artifact bytes and reject a mismatch against the run record before registration.   [sources: python_tutorial#../library/hashlib.html — Usage]
A.f4: Before version creation, require the supplied model name to exist as a registered model (for a new name, client.create_registered_model(name) creates it); then call client.create_model_version(name=name, source=version_qualified_source, run_id=run_id) and retain its returned numeric version.   [sources: mlflow_docs#https://mlflow.org/docs/latest/api_reference/python_api/mlflow.client.html — MlflowClient.create_registered_model; MlflowClient.create_model_version — Examples]
A.f5: Preserve the exact object version and hash in that version’s metadata/tags with set_model_version_tag, so the registry record identifies more than a mutable object name.   [sources: mlflow_docs#ml/model-registry/workflow/ — Registering a Model; Fetching an MLflow Model from the Model Registry; Deploy and Organize Models]
A.f6: Retrieve the created record using get_model_version(name, version), and retrieve its linked originating run to verify the recorded identities.   [sources: mlflow_docs#ml/model-registry/workflow/ — Registering a Model; Fetching an MLflow Model from the Model Registry; Deploy and Organize Models]
A.f7: Overwrite the latest object only in the authorized test bucket, then use the registered version-qualified reference to retrieve the original generation again.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/storage/docs/uploading-objects — Python]
A.f8: Verify the re-retrieved bytes have the registered hash and return one keyed registration verdict; do not treat a mutable overwrite as a new approved registry version.   [sources: python_tutorial#../library/hashlib.html — Usage]
A.f9: Import the registry dependency with from mlflow import MlflowClient, construct MlflowClient(), and use the resulting client for create_model_version, get_model_version and set_model_version_tag.   [sources: mlflow_docs#ml/model-registry/workflow/ — Registering a Model; Fetching an MLflow Model from the Model Registry; Deploy and Organize Models]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Register and Package the Model.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.experiment_metric_logging, mle.training_dataset_version. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Implement a Python registration function using the supplied versioned test bucket, hashing dependency, MlflowClient and dictionary run artifact record. Resolve and download the recorded generation, reject a hash mismatch before registration, and create a numeric registry version with a version-qualified source, originating run link, generation tag and hash tag. Retrieve the version and linked run, overwrite the latest object only in the authorized test bucket, and verify that retrieving the registered generation still yields the registered hash. Return one keyed registration verdict.  SUCCESS: The matching-hash fixture produces a registry version whose source, tags and originating run agree with the run artifact record. Its exact generation retains the registered hash after the latest key is overwritten. The supplied mismatch fixture is rejected before any registry version is created.
ASSESSMENT ANCHOR: resolve_and_verify_exact_run_artifact facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: create_registry_version_with_pinned_artifact_identity facts=['f4', 'f5', 'f9']
ASSESSMENT ANCHOR: retrieve_registry_version_and_verify_originating_run facts=['f6']
ASSESSMENT ANCHOR: verify_registered_content_survives_mutable_key_overwrite facts=['f7', 'f8']

## SOURCE FACTS — B (mle.model_preprocessing_package)   objective: Package fitted preprocessing and model state with dependencies and verify container-reloaded predictions.
B.f1: Persist the fitted model and fitted preprocessor together using a package path tied to the recorded version:
import pickle
with open(package_path, "wb") as handle:
    pickle.dump({"model": model, "preprocessor": preprocessor}, handle, protocol=5)   [sources: scikit_learn_user_guide#https://scikit-learn.org/stable/model_persistence.html — 11.4 Using pickle, joblib, or cloudpickle; 11.5 Security & Maintainability Limitations, python_tutorial#inputoutput.html — Reading and Writing Files]
B.f2: Reload only a trusted, verified package in the compatible pinned inference environment:
with open(package_path, "rb") as handle:
    package = pickle.load(handle)
model = package["model"]
preprocessor = package["preprocessor"]
Pickle loading can execute arbitrary code and is unsafe for untrusted artifacts.   [sources: scikit_learn_user_guide#https://scikit-learn.org/stable/model_persistence.html — 11.4 Using pickle, joblib, or cloudpickle; 11.5 Security & Maintainability Limitations]
B.f3: Write Dockerfile instructions FROM <compatible-python-image>, WORKDIR /app, COPY requirements.txt ./, RUN pip install --no-cache-dir -r requirements.txt, COPY <package-path-in-context> /app/<package-filename>, COPY <serving-source-in-context> /app/<serving-source>, and CMD ["<serving-command>", "<argument>"]; replace placeholders with the declared package, inference dependencies and serving entry point so the default command loads that package.   [sources: docker_docs#https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/ — Common instructions; Python application Dockerfile]
B.f4: Run docker build -t IMAGE:TAG CONTEXT to build and tag the package image; CONTEXT must contain the Dockerfile (or select it with -f) and every source used by COPY, with needed files not excluded by .dockerignore; record the resulting immutable image identity as well as its tag.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/buildx/build/ — Usage; Specify a Dockerfile; Tag an image, docker_docs#docker-concepts/building-images/build-tag-and-publish-an-image — Build an image; Tag an image, docker_docs#https://docs.docker.com/build/concepts/context/ — Filesystem contexts; .dockerignore files]
B.f5: The packaged prediction path must apply the fitted training preprocessing before the packaged model, not refit preprocessing at inference time.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.1 Inconsistent preprocessing]
B.f6: Use docker run --name NAME -p HOST_PORT:CONTAINER_PORT --env KEY=VALUE IMAGE to start the referenced image with the declared port and nonsecret runtime settings.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/run/ — Publish or expose port; Set environment variables; Specify a container name]
B.f7: Inspect the named container with docker container inspect NAME to check its image identity and State fields.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/inspect/ — Description; Examples]
B.f8: Use docker container logs NAME to inspect its captured standard output and error for initialization or execution failures.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/logs/ — Description]
B.f9: Do not embed secrets in Dockerfile ARG or ENV instructions, because they persist in the final image or its metadata.   [sources: docker_docs#https://docs.docker.com/reference/build-checks/secrets-used-in-arg-or-env/ — Description]
B.f10: Supply sensitive values through the runtime secret mechanism rather than placing their literal values in the Compose configuration.   [sources: docker_docs#https://docs.docker.com/reference/compose-file/secrets/ — secrets]
B.f11: Save and reload the fitted model/preprocessor through explicit binary file handles, and write/read the pinned dependency manifest through a text file handle.   [sources: python_tutorial#inputoutput.html — Reading and Writing Files]
B.f12: Record pinned inference package versions in the package’s requirements manifest and install that manifest in the serving image.   [sources: python_tutorial#venv.html — Managing Packages]
B.f13: Assert the pre-save and container-reloaded predictions agree on the same fixed inputs under declared tolerances, and separately check that fitted preprocessing parameters are preserved.   [sources: numpy_user_guide#reference/generated/numpy.testing.assert_allclose.html]
B.f14: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Register and Package the Model.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.preprocessing_pipeline, mle.sklearn_baseline_workflow, mle.training_environment_record. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Implement a Python packaging function that imports its serialization dependency, saves and reloads the supplied fitted model/preprocessor pair at a recorded version-tied path, and writes and reads the supplied pinned inference manifest. Complete a Dockerfile using the supplied compatible Python image and serving entry point, build and tag its image, record its immutable identity, then run and inspect the named container. Execute assertions comparing pre-save and container-reloaded predictions on the same supplied fixed order inputs and separately checking fitted preprocessing parameters. Cover the declared valid, boundary and failure fixtures, and issue one package reproducibility verdict.  SUCCESS: The trusted package reloads in the pinned environment, the manifest round-trips through text file handles, and the image installs that manifest. Container inspection confirms the recorded image identity and expected State fields; captured logs are checked for failures. The supplied serving entry point applies the reloaded fitted preprocessor before the reloaded model without refitting. Prediction and preprocessing-state assertions pass under the declared tolerances; deliberately false predicates raise AssertionError in ordinary non-optimized execution. One verdict reports whether every declared reproducibility check passed.
ASSESSMENT ANCHOR: persist_and_reload_a_trusted_versioned_package_with_pinned_dependencies facts=['f1', 'f2', 'f11', 'f12']
ASSESSMENT ANCHOR: build_run_and_inspect_the_referenced_package_image facts=['f3', 'f4', 'f6', 'f7', 'f8']
ASSESSMENT ANCHOR: verify_prediction_agreement_and_preserved_fitted_preprocessing facts=['f5', 'f13', 'f14']
ASSESSMENT ANCHOR: keep_sensitive_values_out_of_image_and_configuration_literals facts=['f9', 'f10']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Audit dataset, code, run and artifact lineage of a deployed model; Block release promotion when model acceptance gates fail; Choose inference batching under latency constraints; Configure bounded prediction-worker concurrency on an existing runtime; Configure replica scaling to right-size serving capacity under a service objective; Define artifact dependencies between ML pipeline stages; Detect model-input data drift against a defined reference distribution; Distinguish data drift, concept drift and observed quality degradation; Enforce prediction-service authentication on an existing platform; Evaluate the frozen selected model and threshold against the baseline on the protected test set; Execute a bounded managed custom-model training job on an existing platform; Expose model readiness checks before admitting prediction traffic; Gate pipeline execution on dataset-quality tests; Implement batch inference over a bounded dataset; Implement online prediction using the fitted preprocessing and model; Instrument prediction-service availability, errors and latency; Load-test a prediction endpoint against tail-latency and sustainable-throughput objectives; Monitor production input and pr

## LESSON, in learner order

### s01 · explainer · Verify the artifact before registration
Understand — 
(intro) A registry version should link to verified run bytes. Resolve the stored generation and compare its content hash before creating the version. ⟦A:tb1⟧
(mechanism) Resolve the originating run’s artifact record, expected hash and immutable object version. Download with bucket.blob(key, generation=recorded_generation).download_to_filename(path), not the current key. Compute SHA-256 over downloaded bytes; a mismatch must stop registration. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Require the supplied registered model name to exist; for a new name, use client.create_registered_model(name). Call client.create_model_version(name=name, source=version_qualified_source, run_id=run_id) and retain the returned numeric version. Keep exact generation and hash with set_model_version_tag. Retrieve get_model_version(name, version) and its originating run, then compare their recorded identities. ⟦A.f4 A.f5 A.f6 A:tb3⟧
[CODE python]
# Originating run artifact record: {'run_id': 'run.order.B', 'bucket_name': 'authorized-fixture', 'key': 'models/B/latest.json', 'generation': 1, 'expected_hash': 'cb182766714027c89ef572c9cf1c437b88b0cea465e51eeeec10a184cf8ae8c2', 'version_qualified_source': 'gs://authorized-fixture/models/B/latest.json#1', 'model_name': 'B', 'new_name_model': 'baseline', 'local_path': 'downloads/B.json'}
import hashlib, json
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

  annotations: []

### s02 · explainer · An overwrite is not approval
Understand — 
(mechanism) Only in the authorized test bucket, overwrite latest and retrieve the registered generation again. Verify its bytes against the registered hash and return one keyed registration verdict. An overwrite is not a new approved registry version. Import from mlflow import MlflowClient and construct MlflowClient() for version creation, retrieval and tagging. ⟦A.f7 A.f8 A.f9 A:tb4⟧
(example) For the order run, explicitly retrieve its recorded generation even when latest now differs. Verify the hash before creating a numeric version with a version-qualified source and run link. Use the supplied model name; create a new name only on the declared new-name path. Retain generation/hash tags, retrieve the version and linked run, and compare identities. After an authorized test overwrite, retrieve and verify that same registered generation again. Return one verdict binding run, version and artifact, not a claim that overwriting latest approved a replacement. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A.f9 A:tb5⟧
(misconception) A numeric registry version does not verify an unresolved mutable source. Verify generation and bytes, and distinguish overwriting an object from approving a registry version. ⟦A.f1 A.f2 A.f3 A.f5 A.f8 A:tb6⟧

### s03 · check · Check the run-to-registry artifact link
Quick check — The downloaded artifact hash differs from the originating run’s expected hash. Should a registry version be created?

### s04 · hands_on · Review the run-to-registry artifact link
Review evidence — The downloaded artifact hash differs from the originating run’s expected hash. Should a registry version be created?

### s05 · explainer · Package the fitted representation
Understand — 
(intro) Keep the fitted model and fitted preprocessor together. Loading weights alone or refitting preprocessing may run successfully without reproducing the intended predictions. ⟦B:tb1⟧
[SIDE_BY_SIDE] Compare predictions under declared tolerances and check fitted preprocessing separately; inspect immutable image identity, state and logs. left_label: Before saving: fixed inputs | right_label: Container reload: same inputs
  left:
[CODE python]
# Supplied package settings: {'model_identity': 'B', 'registry_version': 1, 'package_path': 'package/B/version_1.pkl', 'compatible_python_image': 'python:3.12-slim', 'image_tag': 'order-fixture:version-1', 'container_name': 'order-fixture', 'rtol': 1e-07, 'atol': 1e-09}
# Before saving: use the fitted training state on the fixed fixture.
with open("package_contract.json") as handle:
    contract = json.load(handle)
fixed_inputs = contract["fixed_inputs"]
pre_save_predictions = model.predict(preprocessor.transform(fixed_inputs))
pre_save_parameters = preprocessor.mean_
# Persist both objects with pickle.dump(..., protocol=5) at
# contract["package_path"], using an explicit binary handle.

  annotations: []
  right:
[CODE python]
# Inside the compatible pinned container: load only trusted, verified state.
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

  annotations: []

### s06 · explainer · Persist trusted fitted state
Understand — 
(mechanism) Import pickle. At the recorded version-tied package path, use a binary "wb" handle and pickle.dump({"model": model, "preprocessor": preprocessor}, handle, protocol=5). Reload only a trusted, verified package in the compatible pinned inference environment: open "rb", call pickle.load(handle), and retrieve both dictionary keys. Untrusted pickle loading is unsafe and can execute arbitrary code. In the Dockerfile, use FROM with the compatible Python image, WORKDIR /app, COPY requirements.txt ./ and RUN pip install --no-cache-dir -r requirements.txt. COPY the declared package and serving source from the build context into their /app paths. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Use a JSON-array CMD containing the declared serving command and argument, replacing placeholders so it loads this package. ⟦B.f1 B.f2 B.f3 B:tb2⟧

### s07 · explainer · Build and start the recorded image
Understand — 
(mechanism) Use docker build -t IMAGE:TAG CONTEXT. Include the Dockerfile (or select it with -f) and all COPY sources; .dockerignore must not exclude required files. Record immutable image identity as well as tag. Prediction applies fitted training preprocessing before the model, without refitting. Start with docker run --name NAME -p HOST_PORT:CONTAINER_PORT --env KEY=VALUE IMAGE using declared ports and nonsecret settings. ⟦B.f4 B.f5 B.f6 B:tb3⟧
(mechanism) Use docker container inspect NAME to check image identity and State. Read captured standard output and error with docker container logs NAME for initialization or execution failures. Secrets must not appear in Dockerfile ARG or ENV: they persist in the image or metadata. ⟦B.f7 B.f8 B.f9 B:tb4⟧

### s08 · explainer · Keep secrets out of the package configuration
Understand — 
(mechanism) Supply sensitive values through the runtime secret mechanism, not literal Compose values. Save and reload fitted state with explicit binary handles; write and read the pinned dependency manifest with text handles. Record pinned inference versions in requirements and install that manifest in the serving image. ⟦B.f10 B.f11 B.f12 B:tb5⟧
(mechanism) On the same fixed inputs, assert pre-save and container-reloaded predictions agree under declared tolerances. Separately check preserved fitted preprocessing parameters. Add assert predicate checks for declared valid, boundary and failure cases; a false predicate raises AssertionError in ordinary non-optimized execution. ⟦B.f13 B.f14 B:tb6⟧

### s09 · explainer · Check the whole package boundary
Understand — 
(example) Persist trusted fitted model/preprocessor state with binary handles at the version-tied path. Keep pinned inference requirements in a text manifest. Include package, requirements and serving source in the Docker context, build it, and record immutable image identity. Start with declared ports and nonsecret settings; inspect identity, state and logs. Compare pre-save and container-reloaded predictions on fixed orders under explicit tolerances, separately checking preprocessing parameters. Reject untrusted pickle artifacts and supply credentials through the runtime mechanism, not Dockerfile or Compose literals. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 B.f9 B.f10 B.f11 B.f12 B.f13 B.f14 B:tb7⟧
(misconception) Packaging does not permit inference-time refitting or embedded credentials. A tag alone does not verify image identity. Pickle needs trusted, verified provenance and a compatible pinned environment. ⟦B.f2 B.f4 B.f5 B.f9 B.f10 B:tb8⟧

### s10 · check · Check the fitted prediction package
Quick check — The container reloads the model but refits preprocessing on prediction inputs. Does this preserve the package contract?

### s11 · hands_on · Review the fitted prediction package
Review evidence — The container reloads the model but refits preprocessing on prediction inputs. Does this preserve the package contract?

### s12 · recap · Keep the evidence together
Takeaways — 
(takeaway) Verify exact artifact bytes before creating a run-linked numeric version; retain generation/hash tags and verify after an authorized overwrite. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A.f9 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(takeaway) Package trusted fitted model and preprocessing together with pinned dependencies. Verify container identity and fixed-input agreement; keep secrets in runtime mechanisms. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 B.f9 B.f10 B.f11 B.f12 B.f13 B.f14 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6 B:tb7 B:tb8⟧
[UP NEXT] Up next: the frozen protected comparison: Continue to the frozen protected comparison.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast: the run-to-registry artifact link
(misconception) An authorized overwrite changes latest, not the approved registry version. Re-retrieve the registered generation and verify its hash. ⟦A.f7 A.f8 A:tb4 A:tb5 A:tb6⟧
(mechanism) Overwrite the latest object only in the authorized test bucket, then use the registered version-qualified reference to retrieve the original generation again. ⟦A.f7 A:tb4 A:tb5⟧
(mechanism) Verify the re-retrieved bytes have the registered hash and return one keyed registration verdict; do not treat a mutable overwrite as a new approved registry version. ⟦A.f8 A:tb4 A:tb5 A:tb6⟧
### r02 · Contrast: the run-to-registry artifact link
(misconception) An authorized overwrite changes latest, not the approved registry version. Re-retrieve the registered generation and verify its hash. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A.f9 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(mechanism) Resolve the run artifact record, expected hash and generation. Download with bucket.blob(key, generation=recorded_generation).download_to_filename(path); reject a downloaded-byte SHA-256 mismatch before registration. Import from mlflow import MlflowClient and construct MlflowClient(). Require the registered name to exist, creating it with create_registered_model only for a new name. Use create_model_version with name, version-qualified source and run_id; retain its numeric version. Preserve generation/hash with set_model_version_tag, then retrieve get_model_version and the linked run to compare identities. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f9 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(mechanism) Only in the authorized test bucket, overwrite latest. Re-retrieve the registered generation, compare its byte digest with the registered hash, and return one keyed verdict binding the run, version and artifact. The overwrite does not approve a new registry version. ⟦A.f7 A.f8 A:tb4 A:tb5 A:tb6⟧
### r03 · Contrast: the fitted prediction package
(misconception) Successful startup does not show matching fitted state or safe secret handling. Preserve preprocessing and use runtime secrets, not image or Compose literals. ⟦B.f10 B.f9 B:tb4 B:tb5 B:tb7 B:tb8⟧
(mechanism) Supply sensitive values through the runtime secret mechanism rather than placing their literal values in the Compose configuration. ⟦B.f10 B:tb5 B:tb7 B:tb8⟧
(mechanism) Do not embed secrets in Dockerfile ARG or ENV instructions, because they persist in the final image or its metadata. ⟦B.f9 B:tb4 B:tb7 B:tb8⟧
### r04 · Contrast: the fitted prediction package
(misconception) Successful startup does not show matching fitted state or safe secret handling. Preserve preprocessing and use runtime secrets, not image or Compose literals. ⟦B.f1 B.f11 B.f12 B.f13 B.f14 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6 B:tb7 B:tb8⟧
(mechanism) Import pickle; persist both fitted objects at the version-tied path using a binary "wb" handle and pickle.dump({"model": model, "preprocessor": preprocessor}, handle, protocol=5). In the compatible pinned environment, reload only trusted, verified state with a binary "rb" handle and pickle.load; retrieve both dictionary keys. Untrusted pickle can execute arbitrary code. Write/read pinned inference requirements through text handles and install that manifest in the image. ⟦B.f1 B.f2 B.f11 B.f12 B:tb2 B:tb5 B:tb7 B:tb8⟧
(mechanism) Use FROM for the compatible Python image, WORKDIR /app, COPY requirements.txt ./, RUN pip install --no-cache-dir -r requirements.txt, COPY the declared package and serving source to /app paths, and a JSON-array CMD for the declared command/argument. Build with docker build -t IMAGE:TAG CONTEXT; include the Dockerfile (or use -f) and all COPY sources without .dockerignore exclusions. Record immutable image identity, not only tag. ⟦B.f3 B.f4 B:tb2 B:tb3 B:tb7 B:tb8⟧
(mechanism) Apply fitted preprocessing before the model; do not refit at inference. Start docker run --name NAME -p HOST_PORT:CONTAINER_PORT --env KEY=VALUE IMAGE with declared ports and nonsecret settings. Check image identity and State using docker container inspect NAME; inspect captured stdout/stderr with docker container logs NAME. Dockerfile ARG/ENV secrets persist in the image or metadata. Use runtime secrets, not literal Compose credentials. ⟦B.f5 B.f6 B.f7 B.f8 B:tb3 B:tb4 B:tb5 B:tb7 B:tb8⟧
(mechanism) On the same fixed inputs, assert pre-save and container-reloaded predictions agree under declared tolerances; separately check preserved fitted preprocessing parameters. Check declared valid, boundary and failure predicates. A false assert raises AssertionError in ordinary non-optimized execution, so successful startup alone does not establish reproducibility. ⟦B.f13 B.f14 B:tb6 B:tb7⟧

=========

# EVALUATOR PACKET — mle.tile.058_058 (mle.tile.058_058)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.protected_test_comparison — Evaluate the frozen selected model and threshold against the baseline on the protected test set

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (mle.protected_test_comparison)   objective: Evaluate the frozen selected candidate on protected test observations without retuning.
A.f1: Only evaluate the protected test set after fixing the selected candidate, fitted preprocessing and decision threshold; test results must not choose a replacement candidate or threshold.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
A.f2: Generate selected-model and baseline predictions for the same protected-test observations and compare the precommitted predictive quantities on that cohort.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f3: Use the already fixed deployment class probabilities, error costs and operating requirements when computing the final comparison; report failure rather than retuning on the test.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
A.f4: For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f5: With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Evaluate the Frozen Choice.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.task_metric_selection, mle.validation_candidate_comparison, mle.model_acceptance_criteria, mle.decision_threshold_selection, mle.reference_baseline. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Implement a learner-defined Python function, with learner-written imports for required dependencies, that evaluates frozen candidate B and the baseline on the same protected observations using supplied infrastructure scaffolding. Derive conditional error rates and expected error costs using fixed deployment probabilities and error costs, compare the precommitted requirements, and report the frozen choice unchanged.  SUCCESS: The function returns a matched comparison containing actual-class conditioning counts, FPR, FNR, expected error cost and requirement outcomes for B and the baseline. Empty conditioning groups produce explicitly undefined rates and any dependent cost is reported as undefined. Failed requirements are reported without replacing B, refitting preprocessing or changing the threshold or comparison inputs.
ASSESSMENT ANCHOR: report_matched_test_comparison_without_new_selection facts=['f1', 'f2']
ASSESSMENT ANCHOR: apply_fixed_comparison_inputs_and_report_requirement_failures facts=['f3']
ASSESSMENT ANCHOR: derive_conditional_error_rates_and_identify_undefined_rates facts=['f4']
ASSESSMENT ANCHOR: compute_expected_error_cost_from_supplied_deployment_probabilities facts=['f5']

## DATA ASSETS USED
ds.protected_comparison: Computed frozen B versus baseline comparison — columns: cohort(identifier), model_identity(categorical), preprocessing_identity(identifier), threshold(numerical), cohort_size(numerical), TN(numerical), FP(numerical), FN(numerical), TP(numerical), FPR(numerical), FNR(numerical), P_Y0(numerical), P_Y1(numerical), cost_FP(numerical), cost_FN(numerical), expected_error_cost(numerical), max_expected_error_cost(numerical), max_FPR(numerical), max_FNR(numerical), requirement_outcome(categorical)
   ["base","B","B.fitted.order_amount.center",40.0,8,2,1,1,4,0.3333333333333333,0.2,0.7,0.3,2.0,5.0,0.7666666666666666,0.5,0.25,0.4,"fail"]
   ["no_negatives","B","B.fitted.order_amount.center",40.0,5,0,0,1,4,null,0.2,0.7,0.3,2.0,5.0,null,0.5,0.25,0.4,"undefined"]
   ["no_positives","B","B.fitted.order_amount.center",40.0,3,2,1,0,0,0.3333333333333333,null,0.7,0.3,2.0,5.0,null,0.5,0.25,0.4,"undefined"]
   ["base","baseline","baseline.fitted.order_amount.center",60.0,8,3,0,3,2,0.0,0.6,0.7,0.3,2.0,5.0,0.8999999999999999,0.5,0.25,0.4,"fail"]
   ["no_negatives","baseline","baseline.fitted.order_amount.center",60.0,5,0,0,3,2,null,0.6,0.7,0.3,2.0,5.0,null,0.5,0.25,0.4,"undefined"]
   ["no_positives","baseline","baseline.fitted.order_amount.center",60.0,3,3,0,0,0,0.0,null,0.7,0.3,2.0,5.0,null,0.5,0.25,0.4,"undefined"]
ds.protected_orders: Protected matched cohort — columns: order_id(identifier), order_amount(numerical), late(categorical,digits-as-label)
   ["protected_01",10.0,0]
   ["protected_02",20.0,1]
   ["protected_03",30.0,0]
   ["protected_04",40.0,1]
   ["protected_05",45.0,0]
   ["protected_06",50.0,1]
   ["protected_07",60.0,1]
   ["protected_08",70.0,1]
   variant no_negatives: 1 ops; planted: 
   variant no_positives: 1 ops; planted: 

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Audit dataset, code, run and artifact lineage of a deployed model; Block release promotion when model acceptance gates fail; Choose inference batching under latency constraints; Configure bounded prediction-worker concurrency on an existing runtime; Configure replica scaling to right-size serving capacity under a service objective; Define artifact dependencies between ML pipeline stages; Detect model-input data drift against a defined reference distribution; Distinguish data drift, concept drift and observed quality degradation; Enforce prediction-service authentication on an existing platform; Execute a bounded managed custom-model training job on an existing platform; Expose model readiness checks before admitting prediction traffic; Gate pipeline execution on dataset-quality tests; Implement batch inference over a bounded dataset; Implement online prediction using the fitted preprocessing and model; Instrument prediction-service availability, errors and latency; Load-test a prediction endpoint against tail-latency and sustainable-throughput objectives; Measure production model quality when labels arrive; Monitor production input and prediction distributions; Promote an approved 

## LESSON, in learner order

### s01 · explainer · Freeze before final testing
Understand — 
(intro) Protected testing compares an already fixed system. Freeze candidate, fitted preprocessing and threshold first; report disappointing results instead of selecting a replacement. ⟦A:tb1⟧
(mechanism) Evaluate only after fixing candidate, fitted preprocessing and threshold. Test results cannot select a replacement candidate or threshold. Generate candidate and baseline predictions for the same protected observations and compare precommitted quantities. Preserve fixed deployment probabilities, error costs and operating requirements; report failure rather than retune. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. An empty conditioning group makes its rate undefined. With zero correct-prediction cost, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN, using supplied deployment probabilities. ⟦A.f4 A.f5 A:tb3⟧
[SIDE_BY_SIDE] Keep the same observations and frozen choices. Report failed requirements or undefined rates without retuning. left_label: Shared protected observations | right_label: Frozen B and baseline comparison
  left:
[TABLE ds.protected_orders cols=all ] caption: 
  right:
[TABLE ds.protected_comparison cols=all ] caption: 

### s02 · explainer · Failure does not unfreeze the system
Understand — 
(example) Candidate B and its threshold were selected before protected outcomes. Predict the same protected orders with B and the baseline. Keep deployment probabilities, costs and operating requirements fixed, even if the observed cohort’s class mix differs. Retain actual-class conditioning counts for rates while applying deployment probabilities to expected error cost: these have different roles. Report undefined quantities or failed requirements explicitly. Do not adjust the threshold, replace the candidate or refit preprocessing to make B pass. The final output is a matched comparison, not another selection round. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb4⟧
(example) Model identity, fitted preprocessing, threshold and metric inputs retain their declared values throughout. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb4⟧
(misconception) A protected-test failure does not authorize switching candidate, refitting preprocessing or searching for a better threshold. ⟦A.f1 A.f3 A:tb5⟧

### s03 · check · Check the frozen protected comparison
Quick check — Frozen B fails the maximum expected-error-cost requirement on the base protected cohort. Should its threshold be changed using these test results?

### s04 · hands_on · Review the frozen protected comparison
Review evidence — Frozen B fails the maximum expected-error-cost requirement on the base protected cohort. Should its threshold be changed using these test results?

### s05 · recap · Keep the evidence together
Takeaways — 
(takeaway) Freeze candidate, preprocessing and threshold before protected testing. Compare both systems on the same observations. Condition FPR on actual negatives and FNR on actual positives; report undefined rates. Apply fixed deployment probabilities, costs and requirements; report failure without retuning. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: the bounded training request: Continue to the bounded training request.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast: the frozen protected comparison
(misconception) Report a failed or undefined result; do not change the fixed candidate, preprocessing or threshold to make it pass. ⟦A.f1 A.f2 A:tb2 A:tb4 A:tb5⟧
(mechanism) Only evaluate the protected test set after fixing the selected candidate, fitted preprocessing and decision threshold; test results must not choose a replacement candidate or threshold. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Generate selected-model and baseline predictions for the same protected-test observations and compare the precommitted predictive quantities on that cohort. ⟦A.f2 A:tb2 A:tb4⟧
### r02 · Contrast: the frozen protected comparison
(misconception) Report a failed or undefined result; do not change the fixed candidate, preprocessing or threshold to make it pass. ⟦A.f3 A.f4 A.f5 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Keep deployment probabilities, costs and operating requirements fixed; report failure without retuning. FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) conditions on actual positives. An empty conditioning group gives an undefined rate. With zero correct-prediction cost, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. ⟦A.f3 A.f4 A.f5 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — mle.tile.059_059 (mle.tile.059_059)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.bounded_managed_training — Execute a bounded managed custom-model training job on an existing platform

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (mle.bounded_managed_training)   objective: Invoke a bounded managed job from parsed settings and verify its consumed inputs, output and terminal state.
A.f1: A SageMaker CreateTrainingJob request specifies TrainingJobName, AlgorithmSpecification, RoleArn, input/output data configuration, ResourceConfig and StoppingCondition.   [sources: sagemaker_developer_guide#../APIReference/API_CreateTrainingJob.html — Request Syntax; Request Parameters; Response Syntax]
A.f2: Select the supplied custom training image with TrainingImage, set instance count/type within the authorized budget and set MaxRuntimeInSeconds to bound execution.   [sources: sagemaker_developer_guide#../APIReference/API_CreateTrainingJob.html — Request Syntax; Request Parameters; Response Syntax]
A.f3: Provide version-resolved input locations through InputDataConfig and an output S3 location through OutputDataConfig; the role must be authorized for those resources.   [sources: sagemaker_developer_guide#../APIReference/API_CreateTrainingJob.html — Request Syntax; Request Parameters; Response Syntax]
A.f4: In the SageMaker training container contract, supplied input channels are exposed under /opt/ml/input/data/CHANNEL and model output is written under /opt/ml/model for upload.   [sources: sagemaker_developer_guide#adapt-training-container.html — SageMaker AI training environment]
A.f5: Inspect the created job’s final status and output artifact location, and use its recorded configuration to check that the one bounded job produced the intended artifact.   [sources: sagemaker_developer_guide#../APIReference/API_CreateTrainingJob.html — Request Syntax; Request Parameters; Response Syntax]
A.f6: Keep the dataset snapshot, code/configuration and resulting run/artifact identities in the execution record.   [sources: google_mlops_pipelines#Metadata management]
A.f7: Use import boto3, client = boto3.client("sagemaker") and client.create_training_job(**resolved_configuration) for the authorized request.   [sources: sagemaker_developer_guide#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_training_job.html — Request Syntax]
A.f8: Call client.describe_training_job(TrainingJobName=job_name) to inspect TrainingJobStatus, FailureReason when present and ModelArtifacts.S3ModelArtifacts.   [sources: sagemaker_developer_guide#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_training_job.html — Response Syntax]
A.f9: Serialize a configuration or record using json.dump(record, file_handle), and recover the structured values with json.load(file_handle) rather than treating JSON text as a Python dictionary.   [sources: python_tutorial#inputoutput.html — Saving structured data with json]
A.f10: Resolve and verify each version-qualified input before submitting the job; if the training API accepts only a mutable channel URI, materialize the selected version at a controlled immutable input location rather than passing an unsupported version parameter.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/storage/docs/using-versioned-objects — Download noncurrent object versions]
A.f11: Retrieve the output artifact using the authorized storage client and verify the returned artifact reference against the completed job record.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/storage/docs/downloading-objects — Python]
A.f12: Managed training creates the requested training resources for the job and releases them after it terminates; confirm terminal job status instead of assuming submission has already ended compute use.   [sources: sagemaker_developer_guide#how-it-works-training.html — How SageMaker AI works with Docker containers]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Run Bounded Managed Training.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.training_dataset_version. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Implement a learner-defined Python function with learner-written imports that authors and parses the supplied job configuration, verifies version-qualified object inputs, submits one authorized custom-model training job within the supplied resource limits, inspects its terminal state and retrieves its verified output artifact. Preserve the dataset snapshot, code/configuration and job/artifact identities in a JSON execution record.  SUCCESS: Exactly one job is submitted using the supplied image, authorized role, verified input locations, output location and permitted instance count/type and maximum runtime. The job reaches Completed, its returned artifact reference matches the execution record, and the artifact is retrieved through the authorized storage client. The JSON record round-trips as structured values and records terminal status as confirmation that job-managed compute use has ended.
ASSESSMENT ANCHOR: submit_authorized_resource_bounded_training_job facts=['f1', 'f2', 'f3', 'f7']
ASSESSMENT ANCHOR: verify_input_identity_and_container_contract facts=['f3', 'f4', 'f10']
ASSESSMENT ANCHOR: verify_terminal_status_and_retrieve_expected_artifact facts=['f5', 'f8', 'f11', 'f12']
ASSESSMENT ANCHOR: preserve_structured_training_execution_record facts=['f6', 'f9']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Audit dataset, code, run and artifact lineage of a deployed model; Block release promotion when model acceptance gates fail; Choose inference batching under latency constraints; Configure actionable model and service alerts; Configure bounded prediction-worker concurrency on an existing runtime; Configure replica scaling to right-size serving capacity under a service objective; Define artifact dependencies between ML pipeline stages; Detect model-input data drift against a defined reference distribution; Distinguish data drift, concept drift and observed quality degradation; Enforce prediction-service authentication on an existing platform; Expose model readiness checks before admitting prediction traffic; Gate pipeline execution on dataset-quality tests; Implement batch inference over a bounded dataset; Implement online prediction using the fitted preprocessing and model; Instrument prediction-service availability, errors and latency; Load-test a prediction endpoint against tail-latency and sustainable-throughput objectives; Measure production model quality when labels arrive; Monitor production input and prediction distributions; Promote an approved registry version through accou

## LESSON, in learner order

### s01 · explainer · Submission is only the beginning
Understand — 
(intro) Use supplied settings for one authorized bounded job. Verify consumed inputs and terminal output rather than treating submission as proof of success. ⟦A:tb1⟧
(mechanism) CreateTrainingJob specifies TrainingJobName, AlgorithmSpecification, RoleArn, input/output data configuration, ResourceConfig and StoppingCondition. Use the supplied custom TrainingImage, permitted instance count/type and MaxRuntimeInSeconds. InputDataConfig must refer to version-resolved inputs; OutputDataConfig supplies the output S3 location. The role must be authorized for those resources. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) The training container reads channels under /opt/ml/input/data/CHANNEL and writes model output under /opt/ml/model for upload. Inspect final job status and artifact location; check the intended artifact against recorded configuration. Keep dataset snapshot, code/configuration and resulting run/artifact identities together in the execution record. ⟦A.f4 A.f5 A.f6 A:tb3⟧
[CODE python]
# Supplied job settings: {'job_name': 'order-training-job', 'image': 'fixture.local/order-training:custom', 'role': 'arn:aws:iam::000000000000:role/fixture-training', 'channel': 'training', 'input_bucket': 'authorized-fixture', 'input_key': 'datasets/latest.csv', 'input_version': '1', 'immutable_key': 'snapshots/order-training/input.csv', 'output_uri': 's3://authorized-fixture/outputs', 'instance_type': 'ml.m5.large', 'max_instance_count': 1, 'max_runtime_seconds': 120, 'dataset_snapshot': {'bucket_name': 'authorized-fixture', 'object_name': 'datasets/latest.csv', 'generation': 1, 'expected_hash': 'd67e606cd75127f615b2ba02dfcc22f853460dcb774c3073bb47fa66ce83a21e', 'local_path': 'training_orders.csv', 'record_path': 'snapshot_record.json', 'download_path': 'downloads/training_orders.csv'}, 'code_reference': 'managed_training_code.py', 'configuration_path': 'job_config.json', 'artifact_uri': 's3://authorized-fixture/outputs/order-training-job/output/model.tar.gz', 'channel_path': '/opt/ml/input/data/training', 'model_output_path': '/opt/ml/model'}
import boto3, json, hashlib
import time
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
    time.sleep(5)
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

  annotations: []

### s02 · explainer · Inspect the job through the client
Understand — 
(mechanism) Import boto3; create client = boto3.client("sagemaker") and call client.create_training_job(**resolved_configuration). Inspect with client.describe_training_job(TrainingJobName=job_name): check TrainingJobStatus, any FailureReason and ModelArtifacts.S3ModelArtifacts. Save records with json.dump(record, file_handle), then decode with json.load(file_handle); JSON text is not a Python dictionary. ⟦A.f7 A.f8 A.f9 A:tb4⟧
(mechanism) Verify each selected input version before submission. If the API only accepts a mutable channel URI, materialize the selected version at a controlled immutable location instead of inventing a version parameter. Retrieve the output with the authorized storage client and check its reference against the completed job record. Managed resources are created for the job and released after termination; confirm terminal status, not merely submission. ⟦A.f10 A.f11 A.f12 A:tb5⟧

### s03 · explainer · Follow one job from input to artifact
Understand — 
(example) Resolve the supplied image, job name, role, channels, output location and resource/time limits before submission. Verify each input version and, where needed, materialize it at the controlled immutable location without unsupported API fields. The container reads the channel beneath /opt/ml/input/data and writes under /opt/ml/model. Inspect terminal status, any failure reason and the artifact location. Retrieve that artifact with the authorized storage client, checking its reference against the completed job record. Preserve snapshot, code/configuration and run/artifact identities together. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A.f9 A.f10 A.f11 A.f12 A:tb6⟧
(misconception) Submission is not completion, and an input name is not verified identity. Managed resources are released after termination; explicitly confirm terminal status. ⟦A.f10 A.f11 A.f12 A:tb7⟧

### s04 · check · Check the bounded training request
Quick check — CreateTrainingJob returned successfully, but no terminal status has been inspected. Is successful completion and ended job-managed compute use established?

### s05 · hands_on · Review the bounded training request
Review evidence — CreateTrainingJob returned successfully, but no terminal status has been inspected. Is successful completion and ended job-managed compute use established?

### s06 · recap · Keep the evidence together
Takeaways — 
(takeaway) Verify version-resolved inputs and submit one authorized request within resource/time limits. Inspect terminal status and retrieve the matching artifact. Round-trip a record linking snapshot, code/configuration, job and artifact. Submission alone does not confirm compute has ended. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A.f9 A.f10 A.f11 A.f12 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6 A:tb7⟧
[UP NEXT] Up next: Validate prediction request and response schemas: Continue to Validate prediction request and response schemas.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast: the bounded training request
(misconception) Submission is not termination. Verify selected input identity before submission and inspect terminal status and artifact identity afterward. ⟦A.f10 A.f3 A.f4 A:tb2 A:tb3 A:tb5 A:tb6 A:tb7⟧
(mechanism) Resolve and verify each version-qualified input before submitting the job; if the training API accepts only a mutable channel URI, materialize the selected version at a controlled immutable input location rather than passing an unsupported version parameter. ⟦A.f10 A:tb5 A:tb6 A:tb7⟧
(mechanism) Provide version-resolved input locations through InputDataConfig and an output S3 location through OutputDataConfig; the role must be authorized for those resources. ⟦A.f3 A:tb2 A:tb6⟧
(mechanism) In the SageMaker training container contract, supplied input channels are exposed under /opt/ml/input/data/CHANNEL and model output is written under /opt/ml/model for upload. ⟦A.f4 A:tb3 A:tb6⟧
### r02 · Contrast: the bounded training request
(misconception) Submission is not termination. Verify selected input identity before submission and inspect terminal status and artifact identity afterward. ⟦A.f1 A.f11 A.f12 A.f2 A.f3 A.f5 A.f6 A.f7 A.f8 A.f9 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6 A:tb7⟧
(mechanism) Resolve TrainingJobName, AlgorithmSpecification with supplied TrainingImage, authorized RoleArn, InputDataConfig, OutputDataConfig, ResourceConfig and StoppingCondition. Keep instance count/type within budget and bound MaxRuntimeInSeconds. Verify selected input versions first; where the API only accepts a mutable channel URI, materialize the verified version at a controlled immutable location, not an unsupported version argument. Channels appear under /opt/ml/input/data/CHANNEL; model output goes under /opt/ml/model for upload. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb5 A:tb6 A:tb7⟧
(mechanism) Import boto3; use boto3.client("sagemaker") and create_training_job(**resolved_configuration) once. Inspect describe_training_job(TrainingJobName=job_name) for terminal TrainingJobStatus, any FailureReason and ModelArtifacts.S3ModelArtifacts. Check intended output against recorded configuration; retrieve it through authorized storage and compare its reference with the completed job record. Keep snapshot, code/configuration and run/artifact identities in a json.dump/json.load round-tripped record. Managed resources are released after termination, not submission. ⟦A.f5 A.f6 A.f7 A.f8 A.f9 A.f11 A.f12 A:tb3 A:tb4 A:tb5 A:tb6 A:tb7⟧