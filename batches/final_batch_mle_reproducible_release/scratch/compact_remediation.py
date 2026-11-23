from pathlib import Path
p=Path('batches/final_batch_mle.region.reproducible_release/build_screens.py')
s=p.read_text()
insert='''
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
'''
s=s.replace("short_names={",insert+"\nshort_names={")
old='''            # Source supplies exact measured fact statements, including syntax, with no invented claims.
            for fact_id in facts:
                fact=next(f for f in bundles[cid]['coverage']['required_facts'] if cid+'#'+f['id']==fact_id)
                relevant=[cid+'#'+tb['id'] for tb in bundles[cid]['teaching_blocks'] if fact['id'] in tb['fact_ids']]
                remediation['blocks'].append(prose(fact['statement'],cid,relevant,[fact_id],'mechanism'))
'''
new='''            if kind=='hands_on':
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
'''
assert old in s
s=s.replace(old,new)
p.write_text(s)
