# EVALUATOR PACKET — Validate and serve fitted predictions (mle.tile.060_063)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.prediction_schema_validation — Validate prediction request and response schemas
B = mle.online_prediction_contract — Implement online prediction using the fitted preprocessing and model
C = mle.bounded_batch_inference — Implement batch inference over a bounded dataset
D = mle.model_service_readiness — Expose model readiness checks before admitting prediction traffic

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (mle.prediction_schema_validation)   objective: Implement and test structured request/response checks for prediction inputs and outputs.
A.f1: A prediction request schema declares the expected features, their types and permitted values, and a response schema declares the expected output structure.   [sources: google_mlops_pipelines#Data and model validation]
A.f2: Decode the incoming JSON into Python values before validating field presence and value types; raw JSON text is not the structured request.   [sources: python_tutorial#inputoutput.html — Saving structured data with json]
A.f3: Compare required and supplied key sets, then check each value’s declared type or numeric boundary with conditional predicates.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
A.f4: For matrix-valued inputs, construct the declared NumPy representation and verify rank, feature width and output row alignment against the request/response contract.   [sources: numpy_user_guide#user/absolute_beginners.html — Attributes of an array; How to create a basic array]
A.f5: Reject malformed or out-of-contract requests explicitly rather than returning a successful prediction from invalid inputs.   [sources: python_tutorial#errors.html — Handling Exceptions; Raising Exceptions]
A.f6: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
A.f7: Send a JSON request body as encoded bytes in urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST"), then read the response through urlopen with a stated timeout.   [sources: python_tutorial#../library/urllib.request.html — Request; urlopen]
A.f8: Use json.dumps to encode structured request/response values and json.loads to decode JSON before checking their fields.   [sources: python_tutorial#inputoutput.html — Saving structured data with json]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Validate and Serve Predictions.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.numpy_shape_dtype. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Within supplied infrastructure scaffolding, write a Python function and its required imports to exchange JSON requests and responses against one declared prediction contract. Author reusable fixtures for a valid three-row, two-feature order matrix, an included numeric limit, a value beyond that limit, a missing required key, an incorrect matrix width and an incorrectly aligned response. Validate decoded structures and assert the expected acceptance or rejection of each case.  SUCCESS: The learner-defined function sends encoded JSON bytes using POST, the JSON content-type header and an explicit timeout; decodes responses before inspection; checks required keys, declared types, numeric boundaries, matrix rank and width, and output row alignment; and uses assertions to confirm valid and boundary acceptance alongside explicit malformed-request rejection and response-violation detection.
ASSESSMENT ANCHOR: reject_malformed_prediction_requests facts=['f1', 'f2', 'f3', 'f4', 'f5', 'f8']
ASSESSMENT ANCHOR: detect_prediction_response_schema_violations facts=['f1', 'f3', 'f4', 'f8']
ASSESSMENT ANCHOR: verify_schema_acceptance_and_rejection_in_json_exchanges facts=['f6', 'f7', 'f8']

## SOURCE FACTS — B (mle.online_prediction_contract)   objective: Serve bounded predictions through the fitted inference path and a validated JSON contract.
B.f1: For a bounded standard-library HTTP implementation, subclass BaseHTTPRequestHandler and implement do_POST to handle the declared prediction route.   [sources: python_tutorial#../library/http.server.html — BaseHTTPRequestHandler]
B.f2: Read the declared request body length from the headers and read that many bytes from rfile before JSON decoding and schema checks.   [sources: python_tutorial#../library/http.server.html — BaseHTTPRequestHandler]
B.f3: Pass validated input through the already fitted preprocessing and model without fitting or updating either during the request.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.1 Inconsistent preprocessing]
B.f4: Encode the response dictionary with json.dumps(...).encode("utf-8") so its named output fields match the declared response schema.   [sources: python_tutorial#inputoutput.html — Saving structured data with json]
B.f5: Write the status with send_response, declare Content-Type and body length with send_header, call end_headers and write the encoded body to wfile.   [sources: python_tutorial#../library/http.server.html — BaseHTTPRequestHandler]
B.f6: http.server is suitable for the bounded supplied fixture but is not recommended as a production server.   [sources: python_tutorial#../library/http.server.html — BaseHTTPRequestHandler]
B.f7: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
B.f8: For the bounded fixture, construct HTTPServer((host, port), Handler) with the declared handler and serve_forever(), using the configured host/port and the existing runtime rather than creating a new platform.   [sources: python_tutorial#../library/http.server.html — BaseHTTPRequestHandler]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Validate and Serve Predictions.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.model_preprocessing_package, mle.prediction_schema_validation, mle.preprocessing_pipeline. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a learner-defined Python function that constructs the bounded HTTP prediction fixture around the supplied frozen fitted package. Author the required imports and a BaseHTTPRequestHandler subclass with do_POST for the declared route. Read and validate JSON features, apply only fitted prediction operations, and return schema-conforming JSON predictions. Create reusable valid, boundary and malformed request fixtures, with assert checks for stable predictions and the declared rejected failure paths. Use the configured host and port in the existing runtime.  SUCCESS: Valid requests receive the declared status and named prediction fields. Response headers describe the actual UTF-8 JSON body. Repeated identical valid requests produce stable predictions without fitting or updating the package. Boundary and malformed fixtures satisfy their declared acceptance or rejection outcomes, and all assertions pass during ordinary non-optimized execution.
ASSESSMENT ANCHOR: handle_valid_requests_with_frozen_prediction_state facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: return_schema_conforming_json_http_responses facts=['f4', 'f5']
ASSESSMENT ANCHOR: assert_stable_predictions_and_rejected_failure_paths facts=['f7']
ASSESSMENT ANCHOR: run_the_bounded_prediction_fixture_on_the_existing_runtime facts=['f6', 'f8']

## SOURCE FACTS — C (mle.bounded_batch_inference)   objective: Write keyed batch predictions with bounded reading and explicit file operations.
C.f1: Use the format-appropriate bounded reader, such as pd.read_csv(path, chunksize=declared_rows), to iterate the input dataset rather than requiring it all in memory.   [sources: pandas_user_guide#io.html — CSV & text files; Iteration; Parquet]
C.f2: Apply the fitted preprocessing/model to each chunk without fitting new state during inference.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.1 Inconsistent preprocessing]
C.f3: Preserve each chunk’s observation keys alongside predictions and verify one result per eligible input key, rather than relying on a changed output row order.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
C.f4: Write output records in the declared serialized format and decode the written fixture again to verify its schema and observation alignment.   [sources: python_tutorial#inputoutput.html — Saving structured data with json]
C.f5: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
C.f6: Use explicit with open(...) handles for input/identity or output records, and write one bounded set of prediction records before reading the next batch.   [sources: python_tutorial#inputoutput.html — Reading and Writing Files]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Validate and Serve Predictions.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.model_preprocessing_package, mle.label_integrity, mle.preprocessing_pipeline. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a Python batch-prediction function and its required imports within supplied infrastructure scaffolding. Read the finite keyed-order CSV fixture through an explicit file handle in declared-size chunks, apply the supplied fitted model package without refitting, and write each chunk's keyed predictions as JSON Lines through an explicit output handle before requesting the next chunk. Decode the written fixture and author count, schema and key-alignment assertions using the supplied valid, boundary and failure fixtures.  SUCCESS: The five-order fixture produces five decoded prediction records across chunks of two, two and one. Each eligible order key occurs exactly once with its prediction, regardless of output order. The fitted package is never refitted, each output batch is written before the next input batch is read, and assertions accept valid and final-partial-chunk cases while detecting missing, duplicate or mismatched keys and malformed output records.
ASSESSMENT ANCHOR: process_and_persist_bounded_prediction_chunks facts=['f1', 'f6']
ASSESSMENT ANCHOR: reuse_fitted_preprocessing_and_model_without_refitting facts=['f2']
ASSESSMENT ANCHOR: verify_decoded_prediction_schema_and_key_alignment facts=['f3', 'f4']
ASSESSMENT ANCHOR: assert_prediction_contract_for_valid_boundary_and_failure_cases facts=['f5']

## SOURCE FACTS — D (mle.model_service_readiness)   objective: Make readiness accurately reflect initialized model/preprocessor state and verify it over HTTP.
D.f1: A model health endpoint must respond successfully within the runtime’s health-check contract; in SageMaker the health check uses /ping.   [sources: sagemaker_developer_guide#adapt-inference-container.html — /ping; /invocations]
D.f2: Return a successful readiness result only after the model is loaded and the service can accept inference, rather than treating process startup alone as model readiness.   [sources: sagemaker_developer_guide#adapt-inference-container.html — /ping; /invocations]
D.f3: Configure the container healthcheck with the declared command, interval, timeout and retry count for the readiness endpoint.   [sources: docker_docs#https://docs.docker.com/reference/compose-file/services/ — image; environment; ports; healthcheck; cpus; mem_limit]
D.f4: Use docker inspect to inspect the health result and status after initialization, and verify that an unready model does not pass the ready fixture.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/inspect/ — Description; Examples]
D.f5: Implement do_GET for the declared readiness route, send a non-ready HTTP status until both the fitted model and preprocessor are initialized, and send success only after that condition is met.   [sources: python_tutorial#../library/http.server.html — BaseHTTPRequestHandler]
D.f6: Serialize readiness state as JSON and test both the HTTP status and decoded state before and after initialization.   [sources: python_tutorial#inputoutput.html — Saving structured data with json]
D.f7: Use docker run --name NAME -p HOST_PORT:CONTAINER_PORT --env KEY=VALUE IMAGE to start the referenced image with the declared port and nonsecret runtime settings.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/run/ — Publish or expose port; Set environment variables; Specify a container name]
D.f8: Inspect the named container with docker container inspect NAME to check its image identity and State fields.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/inspect/ — Description; Examples]
D.f9: Use docker container logs NAME to inspect its captured standard output and error for initialization or execution failures.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/logs/ — Description]
D.f10: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Validate and Serve Predictions.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.online_prediction_contract, mle.model_preprocessing_package. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Implement readiness handling and verification in learner-defined Python functions with learner-written imports, using the supplied container image and its declared contract. Implement do_GET for the readiness route, serialize readiness as JSON, and admit inference only when both the fitted model and preprocessor are initialized and usable. Configure the declared healthcheck, start the named container with its declared port and nonsecret settings, inspect its identity, State and logs, and assert HTTP status and decoded readiness before and after initialization.  SUCCESS: The declared non-ready HTTP status and JSON state are returned when neither fitted object is initialized or when either one remains unavailable. Success is returned only when both are initialized and the service can accept inference. Assertions reject premature success and pass for the declared ready fixture. The named container has the expected image identity, and its State, health result and initialization logs have been inspected.
ASSESSMENT ANCHOR: gate_readiness_on_initialized_inference_assets facts=['f1', 'f2', 'f5']
ASSESSMENT ANCHOR: verify_readiness_status_and_decoded_state facts=['f5', 'f6', 'f10']
ASSESSMENT ANCHOR: verify_container_healthcheck_contract facts=['f3', 'f4']
ASSESSMENT ANCHOR: run_and_inspect_the_supplied_model_container facts=['f7', 'f8', 'f9']

## DATA ASSETS USED
ds.orders: Five keyed orders — columns: order_id(identifier), feature_1(numerical), feature_2(numerical)
   ["A",1.0,2.0]
   ["B",2.0,3.0]
   ["C",3.0,4.0]
   ["D",4.0,5.0]
   ["E",5.0,6.0]
   variant variant.included_limit: 1 ops; planted: 
   variant variant.beyond_limit: 1 ops; planted: issue.beyond_limit(impossible_value)
   variant variant.missing_feature: 1 ops; planted: issue.missing_feature(missing_value)
   variant variant.wrong_type: 1 ops; planted: issue.wrong_type(wrong_type)
   variant variant.duplicate_order: 1 ops; planted: issue.duplicate_order(duplicate_row)
   variant variant.missing_order: 1 ops; planted: 
   variant variant.wrong_width: 1 ops; planted: 
ds.readiness_cases: Controllable initialization fixtures — columns: case_id(identifier), model_initialized(categorical), preprocessor_initialized(categorical), initialization_failed(categorical)
   ["neither",false,false,false]
   ["model_only",true,false,false]
   ["preprocessor_only",false,true,false]
   ["both",true,true,false]
   ["initialization_failure",false,false,true]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Audit dataset, code, run and artifact lineage of a deployed model; Block release promotion when model acceptance gates fail; Choose inference batching under latency constraints; Choose scheduled, new-data or investigated quality/drift retraining triggers; Configure actionable model and service alerts; Configure bounded prediction-worker concurrency on an existing runtime; Configure replica scaling to right-size serving capacity under a service objective; Define artifact dependencies between ML pipeline stages; Detect model-input data drift against a defined reference distribution; Distinguish data drift, concept drift and observed quality degradation; Enforce prediction-service authentication on an existing platform; Expose model readiness checks before admitting prediction traffic; Gate pipeline execution on dataset-quality tests; Implement batch inference over a bounded dataset; Implement online prediction using the fitted preprocessing and model; Instrument prediction-service availability, errors and latency; Invoke retraining with a versioned input snapshot from an authorized trigger; Load-test a prediction endpoint against tail-latency and sustainable-throughput objectives; Me

## LESSON, in learner order

### s01 · explainer · Validate prediction request and response schemas
(intro) Parseable JSON can still violate a prediction contract. Decode first; acceptance also needs field, value and response-alignment checks. ⟦A:tb1⟧
(definition) The request schema specifies features, types and permitted values; the response schema specifies output structure. ⟦A.f1 A:tb2⟧
(definition) Decode JSON into Python values before checking field presence and types. Raw text is not the structured request. ⟦A.f2 A:tb2⟧
(definition) Compare required versus supplied key sets, then test declared types and numeric boundaries with conditional predicates. ⟦A.f3 A:tb2⟧
(mechanism) For matrix-valued inputs, construct the declared NumPy representation and verify rank, feature width and output row alignment against the request/response contract. ⟦A.f4 A:tb3⟧
(mechanism) Reject malformed or out-of-contract requests explicitly rather than returning a successful prediction from invalid inputs. ⟦A.f5 A:tb3⟧
(mechanism) Assert the declared valid, boundary and failure predicates. In ordinary non-optimized execution, a false assertion raises AssertionError. ⟦A.f6 A:tb3⟧
[CODE python]
# Symbolic checks against the supplied contract, not computed output.
body = json.dumps(request_values).encode("utf-8")
request = json.loads(body)
assert set(request) == set(contract["request_keys"])
values = reject_malformed(request)  # checks declared types and bounds
matrix = np.array(values, dtype=contract["numpy_dtype"])
assert matrix.ndim == contract["matrix_rank"]
assert matrix.shape[1] == contract["matrix_width"]
response = json.loads(response_body)
assert set(response) == set(contract["response_keys"])
assert len(response["predictions"]) == matrix.shape[0]
# Use valid, boundary and rejected fixtures; decoding alone is not acceptance.
  annotations: []

### s02 · explainer · Encode and send the JSON request
(mechanism) Send a JSON request body as encoded bytes in urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST"), then read the response through urlopen with a stated timeout. ⟦A.f7 A:tb4⟧
(mechanism) Serialize structured request/response values with json.dumps; decode JSON with json.loads before inspecting fields. ⟦A.f8 A:tb4⟧

### s03 · explainer · Validate decoded request and response contracts
(example) In the order fixture, decode the body before checking required keys, numeric types, permitted bounds and matrix dimensions. Check the decoded response separately for required output keys and one output per request row. A missing key must be rejected before prediction; an included boundary and a value beyond it are different test cases. Serialize the request, send encoded bytes with the JSON header and stated timeout, then decode the response. Parsing, schema acceptance and output correctness are separate assertions. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A:tb5⟧

### s04 · explainer · Distinguish JSON decoding from schema acceptance
(misconception) Raw JSON text is not the structured request, and successful JSON decoding is not schema acceptance. A response with the wrong row correspondence still violates the prediction contract. ⟦A.f1 A.f2 A.f4 A.f5 A.f8 A:tb6⟧

### s05 · check · Check: Validate prediction request and response schemas
Check your decision — 

### s06 · hands_on · Practice: Validate prediction request and response schemas
Bounded fixture practice — 

### s07 · explainer · Implement online prediction using the fitted preprocessing and model
(intro) This bounded HTTP fixture carries validated data through existing fitted prediction state. It is not a production-server design. ⟦B:tb1⟧
(mechanism) For a bounded standard-library HTTP implementation, subclass BaseHTTPRequestHandler and implement do_POST to handle the declared prediction route. ⟦B.f1 B:tb2⟧
(mechanism) Read the declared request body length from the headers and read that many bytes from rfile before JSON decoding and schema checks. ⟦B.f2 B:tb2⟧
(mechanism) Pass validated input through the already fitted preprocessing and model without fitting or updating either during the request. ⟦B.f3 B:tb2⟧
(mechanism) Encode the response dictionary with json.dumps(...).encode("utf-8") so its named output fields match the declared response schema. ⟦B.f4 B:tb3⟧
(mechanism) Write the status with send_response, declare Content-Type and body length with send_header, call end_headers and write the encoded body to wfile. ⟦B.f5 B:tb3⟧
(mechanism) http.server is suitable for the bounded supplied fixture but is not recommended as a production server. ⟦B.f6 B:tb3⟧
[PROCESS_FLOW] nodes=['do_POST: declared Content-Length → rfile bytes', 'Decode JSON; reject schema failures', 'Validated input → fitted transform and predict; no fitting', 'json.dumps → UTF-8 bytes', 'Status; Content-Type; encoded Content-Length; end_headers', 'wfile body; valid/boundary/failure assertions'] edges=[('n0', 'n1', None), ('n1', 'n2', None), ('n2', 'n3', None), ('n3', 'n4', None), ('n4', 'n5', None)] alt: do_POST: declared Content-Length → rfile bytes → Decode JSON; reject schema failures → Validated input → fitted transform and predict; no fitting → json.dumps → UTF-8 bytes → Status; Content-Type; encoded Content-Length; end_headers → wfile body; valid/boundary/failure assertions

### s08 · explainer · Assert fixtures and serve online predictions
(mechanism) Assert the declared valid, boundary and failure predicates. In ordinary non-optimized execution, a false assertion raises AssertionError. ⟦B.f7 B:tb4⟧
(mechanism) For the bounded fixture, construct HTTPServer((host, port), Handler) with the declared handler and serve_forever(), using the configured host/port and the existing runtime rather than creating a new platform. ⟦B.f8 B:tb4⟧

### s09 · explainer · Trace the online prediction HTTP response
(example) Trace the supplied request through do_POST: read the declared byte count, decode JSON, validate, then apply the fitted preprocessor and model without updates. Serialize and UTF-8 encode the response before setting its status, content type and byte length. Finish the headers before writing to wfile. The encoded body determines its length, not an assumed character count. Exercise valid, boundary and malformed fixtures on the configured HTTPServer; this bounded demonstration does not prescribe a production server. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 B:tb5⟧
(misconception) A working http.server fixture is not a production-server recommendation. A response also needs its declared status, content type and body length, not merely a printed prediction. ⟦B.f5 B.f6 B:tb6⟧

### s10 · check · Check: Implement online prediction using the fitted preprocessing and model
Check your decision — 

### s11 · hands_on · Practice: Implement online prediction using the fitted preprocessing and model
Bounded fixture practice — 

### s12 · explainer · Implement batch inference over a bounded dataset
(intro) Bounded chunks still need stable observation identity. Keep keys with predictions and reuse fitted state. ⟦C:tb1⟧
(mechanism) Use the format-appropriate bounded reader, such as pd.read_csv(path, chunksize=declared_rows), to iterate the input dataset without loading the entire dataset at once. ⟦C.f1 C:tb2⟧
(mechanism) Apply the fitted preprocessing/model to each chunk without refitting during inference. ⟦C.f2 C:tb2⟧
(mechanism) Preserve each chunk’s observation keys alongside predictions and verify one result per eligible input key, rather than relying on a changed output row order. ⟦C.f3 C:tb2⟧
(mechanism) Write output records in the declared serialized format and decode the written fixture again to verify its schema and observation alignment. ⟦C.f4 C:tb3⟧
(mechanism) Assert the declared valid, boundary and failure predicates. In ordinary non-optimized execution, a false assertion raises AssertionError. ⟦C.f5 C:tb3⟧
(mechanism) Use explicit with open(...) handles for input/identity or output records, and write one bounded set of prediction records before reading the next batch. ⟦C.f6 C:tb3⟧
[CODE python]
# Context: json, pandas as pd, contract and fitted objects are supplied.
with open(contract["batch_input_path"]) as source, open(contract["batch_output_path"], "w") as target:
    for chunk in pd.read_csv(source, chunksize=contract["chunk_size"]):
        values = preprocessing_pipeline.transform(chunk[contract["feature_names"]])
        predictions = model.predict(values)
        for key, prediction in zip(chunk[contract["batch_key"]], predictions):
            record = {contract["batch_key"]: key, "prediction": float(prediction), "version": contract["version"]}
            target.write(json.dumps(record) + "\n")
# Reopen, decode, assert schema and one result per eligible input key.
# Matching row counts alone cannot detect duplicate-plus-missing keys.
  annotations: []
[TABLE ds.orders cols=all ] caption: Authored keyed input: retain observation identity across the declared bounded chunks.

### s13 · explainer · Preserve batch keys and verify output coverage
(example) Use the declared chunk size for orders.csv. Keep each order_id beside its prediction, serialize that chunk, then read the next one using the same fitted objects. Reopen and decode the written fixture to inspect schema and eligible-key correspondence. A duplicate output key and a missing key can leave the total row count unchanged. Verify coverage and uniqueness rather than incidental output order, retaining explicit input and output handles. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C:tb4⟧

### s14 · explainer · Distinguish row counts from key correspondence
(misconception) A matching total row count does not guarantee one result for every eligible input key. Batch inference preserves keys and fitted state, rather than relying on incidental output order. ⟦C.f2 C.f3 C:tb5⟧

### s15 · check · Check: Implement batch inference over a bounded dataset
Check your decision — 

### s16 · hands_on · Practice: Implement batch inference over a bounded dataset
Bounded fixture practice — 

### s17 · explainer · Expose model readiness checks before admitting prediction traffic
(intro) A running process may still lack initialized prediction assets. Readiness must describe whether inference can be accepted. ⟦D:tb1⟧
(mechanism) A model health endpoint must respond successfully within the runtime’s health-check contract; in SageMaker the health check uses /ping. ⟦D.f1 D:tb2⟧
(mechanism) Return a successful readiness result only after the model is loaded and the service can accept inference, not merely after process startup. ⟦D.f2 D:tb2⟧
(mechanism) Configure the container healthcheck with the declared command, interval, timeout and retry count for the readiness endpoint. ⟦D.f3 D:tb2⟧
(mechanism) Use docker inspect to inspect the health result and status after initialization, and verify that an unready model does not pass the ready fixture. ⟦D.f4 D:tb3⟧
(mechanism) Implement do_GET for the declared readiness route, send a non-ready HTTP status until both the fitted model and preprocessor are initialized, and send success only after that condition is met. ⟦D.f5 D:tb3⟧
(mechanism) Serialize readiness state as JSON and test both the HTTP status and decoded state before and after initialization. ⟦D.f6 D:tb3⟧
[BEFORE_AFTER] Initialization, not process startup, is the readiness boundary. Inspect the configured command, interval, timeout and retries.
  before:
[DIAGRAM: Before initialization] nodes=['Process started', 'Either fitted model or preprocessor uninitialized', 'Non-ready HTTP status 503; decoded JSON {"ready": false}'] edges=[('n0', 'n1', None), ('n1', 'n2', None)] alt: Process started → Either fitted model or preprocessor uninitialized → Non-ready HTTP status 503; decoded JSON {"ready": false}
  after:
[DIAGRAM: After initialization] nodes=['Both fitted objects initialized; inference accepted', 'Successful HTTP status 200; decoded JSON {"ready": true}', 'Inspect configured healthcheck result'] edges=[('n0', 'n1', None), ('n1', 'n2', None)] alt: Both fitted objects initialized; inference accepted → Successful HTTP status 200; decoded JSON {"ready": true} → Inspect configured healthcheck result
[TABLE ds.readiness_cases cols=all ] caption: Authored initialization cases: both fitted assets must be usable; initialization failure cannot pass readiness.

### s18 · explainer · Start and inspect the readiness fixture container
(mechanism) Use docker run --name NAME -p HOST_PORT:CONTAINER_PORT --env KEY=VALUE IMAGE to start the referenced image with the declared port and nonsecret runtime settings. ⟦D.f7 D:tb4⟧
(mechanism) Inspect the named container with docker container inspect NAME to check its image identity and State fields. ⟦D.f8 D:tb4⟧
(mechanism) Use docker container logs NAME to inspect its captured standard output and error for initialization or execution failures. ⟦D.f9 D:tb4⟧
(mechanism) Assert the declared valid, boundary and failure predicates. In ordinary non-optimized execution, a false assertion raises AssertionError. ⟦D.f10 D:tb5⟧
(example) Start the referenced image with its declared runtime settings. Inspect identity, State and initialization logs. Before both fitted objects initialize, the readiness route must return the declared non-ready status and JSON state. After initialization, check success status and decoded readiness state together. Configure the readiness healthcheck command, interval, timeout and retries, and inspect its result. Process startup alone cannot pass the ready fixture. ⟦D.f1 D.f2 D.f3 D.f4 D.f5 D.f6 D.f7 D.f8 D.f9 D.f10 D:tb6⟧
(misconception) Running is not ready. A success status needs the declared inference-ready condition, and the test must inspect both HTTP status and decoded state instead of treating any endpoint response as readiness. ⟦D.f1 D.f2 D.f5 D.f6 D:tb7⟧

### s19 · check · Check: Expose model readiness checks before admitting prediction traffic
Check your decision — 

### s20 · hands_on · Practice: Expose model readiness checks before admitting prediction traffic
Bounded fixture practice — 

### s21 · recap · Carry these rules forward
(takeaway) Decoding is not schema acceptance; request validity and response row alignment need separate checks. ⟦A.f1 A.f2 A.f4 A.f5 A.f8 A:tb6⟧
(takeaway) A bounded http.server fixture is not a production recommendation; return status, headers and encoded body. ⟦B.f5 B.f6 B:tb6⟧
(takeaway) Preserve keys and fitted state. Matching row counts do not prove one output per eligible key. ⟦C.f2 C.f3 C:tb5⟧
(takeaway) Running is not ready. Verify initialized assets, HTTP status and decoded readiness state. ⟦D.f1 D.f2 D.f5 D.f6 D:tb7⟧
[UP NEXT] Reproduce a model deployment from parameterized runtime configuration and an immutable artifact reference: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try again: Validate prediction request and response schemas — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) Assert the declared valid, boundary and failure predicates. In ordinary non-optimized execution, a false assertion raises AssertionError. ⟦A.f6 A:tb3⟧
(mechanism) Send a JSON request body as encoded bytes in urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST"), then read the response through urlopen with a stated timeout. ⟦A.f7 A:tb4⟧
(mechanism) Serialize structured request/response values with json.dumps; decode JSON with json.loads before inspecting fields. ⟦A.f8 A:tb4⟧
(misconception) Raw JSON text is not the structured request, and successful JSON decoding is not schema acceptance. A response with the wrong row correspondence still violates the prediction contract. ⟦A.f1 A.f2 A.f4 A.f5 A.f8 A:tb6⟧
### r02 · Try again: Validate prediction request and response schemas — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) The request schema specifies features, types and permitted values; the response schema specifies output structure. ⟦A.f1 A:tb2⟧
(mechanism) Decode JSON into Python values before checking field presence and types. Raw text is not the structured request. ⟦A.f2 A:tb2⟧
(mechanism) Compare required versus supplied key sets, then test declared types and numeric boundaries with conditional predicates. ⟦A.f3 A:tb2⟧
(mechanism) For matrix-valued inputs, construct the declared NumPy representation and verify rank, feature width and output row alignment against the request/response contract. ⟦A.f4 A:tb3⟧
(mechanism) Reject malformed or out-of-contract requests explicitly rather than returning a successful prediction from invalid inputs. ⟦A.f5 A:tb3⟧
(mechanism) Assert the declared valid, boundary and failure predicates. In ordinary non-optimized execution, a false assertion raises AssertionError. ⟦A.f6 A:tb3⟧
(mechanism) Send a JSON request body as encoded bytes in urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST"), then read the response through urlopen with a stated timeout. ⟦A.f7 A:tb4⟧
(mechanism) Serialize structured request/response values with json.dumps; decode JSON with json.loads before inspecting fields. ⟦A.f8 A:tb4⟧
(misconception) Raw JSON text is not the structured request, and successful JSON decoding is not schema acceptance. A response with the wrong row correspondence still violates the prediction contract. ⟦A.f1 A.f2 A.f4 A.f5 A.f8 A:tb6⟧
### r03 · Try again: Implement online prediction using the fitted preprocessing and model — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) http.server is suitable for the bounded supplied fixture but is not recommended as a production server. ⟦B.f6 B:tb3⟧
(mechanism) For the bounded fixture, construct HTTPServer((host, port), Handler) with the declared handler and serve_forever(), using the configured host/port and the existing runtime rather than creating a new platform. ⟦B.f8 B:tb4⟧
(misconception) A working http.server fixture is not a production-server recommendation. A response also needs its declared status, content type and body length, not merely a printed prediction. ⟦B.f5 B.f6 B:tb6⟧
### r04 · Try again: Implement online prediction using the fitted preprocessing and model — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) For a bounded standard-library HTTP implementation, subclass BaseHTTPRequestHandler and implement do_POST to handle the declared prediction route. ⟦B.f1 B:tb2⟧
(mechanism) Read the declared request body length from the headers and read that many bytes from rfile before JSON decoding and schema checks. ⟦B.f2 B:tb2⟧
(mechanism) Pass validated input through the already fitted preprocessing and model without fitting or updating either during the request. ⟦B.f3 B:tb2⟧
(mechanism) Encode the response dictionary with json.dumps(...).encode("utf-8") so its named output fields match the declared response schema. ⟦B.f4 B:tb3⟧
(mechanism) Write the status with send_response, declare Content-Type and body length with send_header, call end_headers and write the encoded body to wfile. ⟦B.f5 B:tb3⟧
(mechanism) http.server is suitable for the bounded supplied fixture but is not recommended as a production server. ⟦B.f6 B:tb3⟧
(mechanism) Assert the declared valid, boundary and failure predicates. In ordinary non-optimized execution, a false assertion raises AssertionError. ⟦B.f7 B:tb4⟧
(mechanism) For the bounded fixture, construct HTTPServer((host, port), Handler) with the declared handler and serve_forever(), using the configured host/port and the existing runtime rather than creating a new platform. ⟦B.f8 B:tb4⟧
(misconception) A working http.server fixture is not a production-server recommendation. A response also needs its declared status, content type and body length, not merely a printed prediction. ⟦B.f5 B.f6 B:tb6⟧
### r05 · Try again: Implement batch inference over a bounded dataset — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) Assert the declared valid, boundary and failure predicates. In ordinary non-optimized execution, a false assertion raises AssertionError. ⟦C.f5 C:tb3⟧
(misconception) A matching total row count does not guarantee one result for every eligible input key. Batch inference preserves keys and fitted state, rather than relying on incidental output order. ⟦C.f2 C.f3 C:tb5⟧
### r06 · Try again: Implement batch inference over a bounded dataset — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) Use the format-appropriate bounded reader, such as pd.read_csv(path, chunksize=declared_rows), to iterate the input dataset without loading the entire dataset at once. ⟦C.f1 C:tb2⟧
(mechanism) Apply the fitted preprocessing/model to each chunk without refitting during inference. ⟦C.f2 C:tb2⟧
(mechanism) Preserve each chunk’s observation keys alongside predictions and verify one result per eligible input key, rather than relying on a changed output row order. ⟦C.f3 C:tb2⟧
(mechanism) Write output records in the declared serialized format and decode the written fixture again to verify its schema and observation alignment. ⟦C.f4 C:tb3⟧
(mechanism) Assert the declared valid, boundary and failure predicates. In ordinary non-optimized execution, a false assertion raises AssertionError. ⟦C.f5 C:tb3⟧
(mechanism) Use explicit with open(...) handles for input/identity or output records, and write one bounded set of prediction records before reading the next batch. ⟦C.f6 C:tb3⟧
(misconception) A matching total row count does not guarantee one result for every eligible input key. Batch inference preserves keys and fitted state, rather than relying on incidental output order. ⟦C.f2 C.f3 C:tb5⟧
### r07 · Try again: Expose model readiness checks before admitting prediction traffic — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) Use docker run --name NAME -p HOST_PORT:CONTAINER_PORT --env KEY=VALUE IMAGE to start the referenced image with the declared port and nonsecret runtime settings. ⟦D.f7 D:tb4⟧
(mechanism) Inspect the named container with docker container inspect NAME to check its image identity and State fields. ⟦D.f8 D:tb4⟧
(mechanism) Use docker container logs NAME to inspect its captured standard output and error for initialization or execution failures. ⟦D.f9 D:tb4⟧
(misconception) Running is not ready. A success status needs the declared inference-ready condition, and the test must inspect both HTTP status and decoded state instead of treating any endpoint response as readiness. ⟦D.f1 D.f2 D.f5 D.f6 D:tb7⟧
### r08 · Try again: Expose model readiness checks before admitting prediction traffic — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) A model health endpoint must respond successfully within the runtime’s health-check contract; in SageMaker the health check uses /ping. ⟦D.f1 D:tb2⟧
(mechanism) Assert the declared valid, boundary and failure predicates. In ordinary non-optimized execution, a false assertion raises AssertionError. ⟦D.f10 D:tb5⟧
(mechanism) Return a successful readiness result only after the model is loaded and the service can accept inference, not merely after process startup. ⟦D.f2 D:tb2⟧
(mechanism) Configure the container healthcheck with the declared command, interval, timeout and retry count for the readiness endpoint. ⟦D.f3 D:tb2⟧
(mechanism) Use docker inspect to inspect the health result and status after initialization, and verify that an unready model does not pass the ready fixture. ⟦D.f4 D:tb3⟧
(mechanism) Implement do_GET for the declared readiness route, send a non-ready HTTP status until both the fitted model and preprocessor are initialized, and send success only after that condition is met. ⟦D.f5 D:tb3⟧
(mechanism) Serialize readiness state as JSON and test both the HTTP status and decoded state before and after initialization. ⟦D.f6 D:tb3⟧
(mechanism) Use docker run --name NAME -p HOST_PORT:CONTAINER_PORT --env KEY=VALUE IMAGE to start the referenced image with the declared port and nonsecret runtime settings. ⟦D.f7 D:tb4⟧
(mechanism) Inspect the named container with docker container inspect NAME to check its image identity and State fields. ⟦D.f8 D:tb4⟧
(mechanism) Use docker container logs NAME to inspect its captured standard output and error for initialization or execution failures. ⟦D.f9 D:tb4⟧
(misconception) Running is not ready. A success status needs the declared inference-ready condition, and the test must inspect both HTTP status and decoded state instead of treating any endpoint response as readiness. ⟦D.f1 D.f2 D.f5 D.f6 D:tb7⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: One distinction to restore
· remediation_steps.eyebrow: One distinction to restore
· remediation_steps.eyebrow: One distinction to restore
· remediation_steps.eyebrow: One distinction to restore
· remediation_steps.eyebrow: One distinction to restore
· remediation_steps.eyebrow: One distinction to restore
· remediation_steps.eyebrow: One distinction to restore
· remediation_steps.eyebrow: One distinction to restore

=========

# EVALUATOR PACKET — Reproduce and verify a serving release (mle.tile.064_065)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.deployment_configuration_code — Reproduce a model deployment from parameterized runtime configuration and an immutable artifact reference
B = mle.deployment_verification — Verify a model release on an existing runtime

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (mle.deployment_configuration_code)   objective: Version, apply and recreate an existing deployment from parsed runtime configuration.
A.f1: Use the recorded immutable image digest in the deployment instead of a mutable tag that can later resolve to different contents.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/image/pull/ — Pull an image by digest (immutable identifier)]
A.f2: In the supplied Docker Compose runtime, author the mapping services: {prediction: {image: IMAGE_DIGEST, environment: {SETTING: VALUE}, ports: ["HOST_PORT:CONTAINER_PORT"], secrets: [credential], deploy: {replicas: REPLICA_COUNT}}} and top-level secrets: {credential: {environment: INJECTED_SECRET_VARIABLE}}; substitute the approved digest, nonsecret setting, port numbers, supported replica count and host secret-variable name, never the secret value.   [sources: docker_docs#https://docs.docker.com/reference/compose-file/services/ — image; environment; ports; secrets, docker_docs#https://docs.docker.com/reference/compose-file/deploy/ — replicas; resources, docker_docs#https://docs.docker.com/reference/compose-file/secrets/ — environment]
A.f3: Set a service’s image to its immutable artifact reference, its ports to HOST:CONTAINER mappings, and its environment to the declared nonsecret key/value settings.   [sources: docker_docs#https://docs.docker.com/reference/compose-file/services/ — image; environment; ports; healthcheck; cpus; mem_limit]
A.f4: Use docker compose -f CONFIG_PATH config to parse, resolve and validate the authored YAML before applying it; check its resolved fields against the intended runtime contract.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/compose/config/ — Description; Options]
A.f5: Apply the declared local Compose deployment with docker compose -f CONFIG_PATH up -d and inspect the resulting containers.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/compose/up/ — Description]
A.f6: Set replica count at services.<service>.deploy.replicas; set resource bounds at services.<service>.deploy.resources.limits.cpus and memory in a runtime supporting these deploy fields, and validate the resolved count and bounds before applying the configuration.   [sources: docker_docs#https://docs.docker.com/reference/compose-file/deploy/ — replicas; resources]
A.f7: Do not embed secrets in Dockerfile ARG or ENV instructions, because they persist in the final image or its metadata.   [sources: docker_docs#https://docs.docker.com/reference/build-checks/secrets-used-in-arg-or-env/ — Description]
A.f8: Supply sensitive values through the runtime secret mechanism rather than placing their literal values in the Compose configuration.   [sources: docker_docs#https://docs.docker.com/reference/compose-file/secrets/ — secrets]
A.f9: After application, inspect the running image identity and compare it with the recorded artifact reference.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/image/inspect/ — Description]
A.f10: For an authorized supplied Compute Engine VM, gcloud compute instances start INSTANCE --zone=ZONE and gcloud compute instances stop INSTANCE --zone=ZONE change its lifecycle state; wait for the operation and inspect the resulting state.   [sources: google_mlops_pipelines#https://cloud.google.com/compute/docs/instances/stop-start-instance — Stop an instance; Start an instance]
A.f11: Connect to the running authorized VM with gcloud compute ssh INSTANCE --zone=ZONE to execute the workload.   [sources: google_mlops_pipelines#https://cloud.google.com/compute/docs/connect/standard-ssh — Connect to VMs]
A.f12: Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect the instance status and identity before and after the authorized lifecycle action.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/sdk/gcloud/reference/compute/instances/describe — DESCRIPTION; EXAMPLES]
A.f13: Create the configuration branch with git checkout -b BRANCH, commit the verified configuration, then merge the branch under the existing repository workflow.   [sources: git_docs#git-checkout — DESCRIPTION; git-commit — DESCRIPTION; git-merge — DESCRIPTION]
A.f14: Destroy only the test deployment with docker compose -f CONFIG_PATH down, then reapply the same file and verify identical image identity and resolved runtime settings.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/compose/down/ — Description]
A.f15: With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading accepts standard YAML tags, not arbitrary Python object constructors.   [sources: python_tutorial#https://pyyaml.org/wiki/PyYAMLDocumentation — Reference: safe_load; safe_dump]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Configure and Verify Deployment.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.model_version_registration, mle.model_preprocessing_package. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): On a branch in the supplied repository, author a parameterized Compose YAML configuration for prediction using the approved immutable image digest, nonsecret environment setting, port mapping, supported replica count and resource bounds, and injected credential reference. Write and reload it with PyYAML, then validate its resolved fields with Compose. Using only the authorized supplied VM and test deployment, inspect the instance, start and connect as required, apply the configuration, inspect container state and logs without exposing credentials, and compare the running image identity with the recorded artifact. Destroy only this test deployment, reapply the same file, verify unchanged identity and settings, then commit and merge the verified configuration.  SUCCESS: One reproducible-deployment verdict records whether the initial and recreated deployments match the approved immutable artifact and resolved runtime settings. Evidence includes YAML and Compose validation, authorized instance status and identity, container running or exit state, credential-safe log inspection, and the committed and merged configuration. No literal credential appears in configuration, image instructions, logs, or submitted evidence.
ASSESSMENT ANCHOR: author_and_validate_parameterized_runtime_configuration facts=['f1', 'f2', 'f3', 'f4', 'f6', 'f15']
ASSESSMENT ANCHOR: separate_runtime_secrets_from_configuration_and_image facts=['f7', 'f8']
ASSESSMENT ANCHOR: inspect_and_operate_authorized_compute_instance facts=['f10', 'f11', 'f12']
ASSESSMENT ANCHOR: verify_container_state_and_immutable_image_identity facts=['f5', 'f9']
ASSESSMENT ANCHOR: recreate_test_deployment_with_identical_artifact_and_settings facts=['f1', 'f3', 'f6', 'f9', 'f14']
ASSESSMENT ANCHOR: commit_and_merge_verified_deployment_configuration facts=['f13']

## SOURCE FACTS — B (mle.deployment_verification)   objective: Verify a referenced serving artifact through real runtime inspection and prediction fixtures.
B.f1: Verify the same recorded artifact and runtime configuration in the existing execution environment, rather than accepting the fact that deployment started as proof of a correct release.   [sources: google_mlops_pipelines#MLOps level 1: ML pipeline automation — Characteristics]
B.f2: Use docker run --name NAME -p HOST_PORT:CONTAINER_PORT --env KEY=VALUE IMAGE to start the referenced image with the declared port and nonsecret runtime settings.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/run/ — Publish or expose port; Set environment variables; Specify a container name]
B.f3: Inspect the named container with docker container inspect NAME to check its image identity and State fields.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/inspect/ — Description; Examples]
B.f4: Use docker container logs NAME to inspect its captured standard output and error for initialization or execution failures.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/logs/ — Description]
B.f5: Inspect the running container identity and State, including Health when a healthcheck is configured, and compare them with the intended release.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/inspect/ — Description; Examples]
B.f6: Inspect runtime logs for initialization and execution failures without copying sensitive request data or credentials into the evidence record.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/logs/ — Description]
B.f7: Call the declared readiness and prediction endpoints with bounded timeouts and check the returned status and payload against the expected contracts.   [sources: python_tutorial#../library/urllib.request.html — Request; urlopen]
B.f8: Send a JSON request body as encoded bytes in urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST"), then read the response through urlopen with a stated timeout.   [sources: python_tutorial#../library/urllib.request.html — Request; urlopen]
B.f9: Use json.dumps to encode structured request/response values and json.loads to decode JSON before checking their fields.   [sources: python_tutorial#inputoutput.html — Saving structured data with json]
B.f10: Inspect the small prediction fixture’s output shape and values against the declared task/response contract.   [sources: numpy_user_guide#user/absolute_beginners.html — Attributes of an array; How to create a basic array]
B.f11: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Configure and Verify Deployment.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.online_prediction_contract, mle.model_service_readiness, mle.model_version_registration, mle.prediction_schema_validation, mle.model_preprocessing_package. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Start the supplied immutable release image on the existing authorized runtime with its declared published port and nonsecret settings. Inspect container identity, State, configured Health and logs. Author reusable valid, boundary and malformed JSON fixtures using only the supplied prediction fields, and assert readiness status, decoded prediction shape and values, malformed-request rejection and immutable release identity. Execute the bounded checks and record one acceptance verdict.  SUCCESS: The release receives an acceptance verdict only when its recorded artifact and runtime configuration match the observed container, initialization checks pass, readiness satisfies its contract, valid and boundary fixtures produce the declared responses, and the malformed fixture receives the declared rejection. All endpoint calls have stated timeouts, and the evidence excludes credentials and sensitive request data.
ASSESSMENT ANCHOR: verify_release_identity_and_runtime_configuration facts=['f1', 'f2', 'f3', 'f5']
ASSESSMENT ANCHOR: inspect_runtime_failures_without_exposing_sensitive_data facts=['f4', 'f6']
ASSESSMENT ANCHOR: verify_endpoint_status_and_decoded_prediction_contract facts=['f7', 'f8', 'f9', 'f10']
ASSESSMENT ANCHOR: determine_release_acceptance_from_explicit_checks facts=['f11', 'f1', 'f5', 'f7', 'f10']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Audit dataset, code, run and artifact lineage of a deployed model; Block release promotion when model acceptance gates fail; Choose inference batching under latency constraints; Choose scheduled, new-data or investigated quality/drift retraining triggers; Configure actionable model and service alerts; Configure bounded prediction-worker concurrency on an existing runtime; Configure replica scaling to right-size serving capacity under a service objective; Define artifact dependencies between ML pipeline stages; Detect model-input data drift against a defined reference distribution; Distinguish data drift, concept drift and observed quality degradation; Enforce prediction-service authentication on an existing platform; Gate a retrained candidate against the incumbent using validation evidence before controlled promotion; Gate pipeline execution on dataset-quality tests; Instrument prediction-service availability, errors and latency; Invoke retraining with a versioned input snapshot from an authorized trigger; Load-test a prediction endpoint against tail-latency and sustainable-throughput objectives; Measure production model quality when labels arrive; Monitor production input and pre

## LESSON, in learner order

### s01 · explainer · Reproduce a model deployment from parameterized runtime configuration and an immutable artifact reference
(intro) Prepare repeatable configuration before applying it. Separate nonsecret settings from runtime secret references. ⟦A:tb1⟧
(mechanism) Pin deployment to the recorded immutable image digest; a mutable tag may later resolve to different contents. ⟦A.f1 A:tb2⟧
(mechanism) In the supplied Docker Compose runtime, author the mapping services: {prediction: {image: IMAGE_DIGEST, environment: {SETTING: VALUE}, ports: ["HOST_PORT:CONTAINER_PORT"], secrets: [credential], deploy: {replicas: REPLICA_COUNT}}} and top-level secrets: {credential: {environment: INJECTED_SECRET_VARIABLE}}; substitute the approved digest, nonsecret setting, port numbers, supported replica count and host secret-variable name, never the secret value. ⟦A.f2 A:tb2⟧
(mechanism) Set a service’s image to its immutable artifact reference, its ports to HOST:CONTAINER mappings, and its environment to the declared nonsecret key/value settings. ⟦A.f3 A:tb2⟧
[SIDE_BY_SIDE] Parsed configuration is not proof of running identity; runtime support for deploy fields must be checked. left_label: Configuration intent | right_label: Running evidence
  left:
[DIAGRAM: Authored configuration] nodes=['Recorded immutable image', 'HOST:CONTAINER ports; nonsecret environment', 'Runtime secret-variable reference', 'Supported replica/resource bounds', 'Safely reloaded YAML → compose config'] edges=[('n0', 'n1', None), ('n1', 'n2', None), ('n2', 'n3', None), ('n3', 'n4', None)] alt: Recorded immutable image → HOST:CONTAINER ports; nonsecret environment → Runtime secret-variable reference → Supported replica/resource bounds → Safely reloaded YAML → compose config
  right:
[DIAGRAM: Observed runtime] nodes=['compose up -d', 'Inspect running image and State', 'Compare actual identity and runtime settings', 'Destroy only test deployment; reapply same file', 'Verify identical artifact and resolved settings'] edges=[('n0', 'n1', None), ('n1', 'n2', None), ('n2', 'n3', None), ('n3', 'n4', None)] alt: compose up -d → Inspect running image and State → Compare actual identity and runtime settings → Destroy only test deployment; reapply same file → Verify identical artifact and resolved settings
[CODE python]
import json
with open("runtime_contract.json") as source:
    intended = json.load(source)
# Inspect live fixture execution separately from the intended configuration.
# Compare container Config.Image with intended["IMAGE_DIGEST"].
# Check State and Health when configured, plus sanitized initialization/execution logs.
# Bounded readiness and prediction checks must verify status and decoded payload.
# Do not interpret launch success as acceptance.
  annotations: []
[CODE python]
# Authored intended fixture configuration; no credential literals.
config = {'services': {'prediction': {'image': 'fixture.local/orders@sha256:29371dd36fb111803c6fe996426f342680170dec59168e1e52139cdb4fbfaf83', 'environment': {'MODE': 'fixture'}, 'ports': ['8080:8080'], 'secrets': ['credential'], 'deploy': {'replicas': 1, 'resources': {'limits': {'cpus': 1.0, 'memory': '256M'}}}}}, 'secrets': {'credential': {'environment': 'ORDER_FIXTURE_CREDENTIAL'}}}
# Safely write/reload; resolve fields before application.
# Compare initial and recreated running identity/settings with this same file.
  annotations: []
[DIAGRAM: Authorized fixture instance, not a real cloud deployment] nodes=['Authorized instance: order-lab', 'Zone: fixture-zone', 'Describe identity/status before and after authorized lifecycle action'] edges=[('n0', 'n1', None), ('n1', 'n2', None)] alt: Authorized instance: order-lab → Zone: fixture-zone → Describe identity/status before and after authorized lifecycle action

### s02 · explainer · Resolve configuration before deployment
(mechanism) Use docker compose -f CONFIG_PATH config to parse, resolve and validate the authored YAML before applying it; check its resolved fields against the intended runtime contract. ⟦A.f4 A:tb3⟧
(mechanism) Apply the declared local Compose deployment with docker compose -f CONFIG_PATH up -d and inspect the resulting containers. ⟦A.f5 A:tb3⟧
(mechanism) Set replica count at services.<service>.deploy.replicas; set resource bounds at services.<service>.deploy.resources.limits.cpus and memory in a runtime supporting these deploy fields, and validate the resolved count and bounds before applying the configuration. ⟦A.f6 A:tb3⟧
(mechanism) Keep secrets out of Dockerfile ARG and ENV: they persist in the final image or its metadata. ⟦A.f7 A:tb4⟧
(mechanism) Deliver sensitive values through runtime secrets, never as literal Compose values. ⟦A.f8 A:tb4⟧
(mechanism) After application, inspect the running image identity and compare it with the recorded artifact reference. ⟦A.f9 A:tb4⟧

### s03 · explainer · Inspect authorized VM lifecycle changes
(mechanism) For an authorized supplied Compute Engine VM, gcloud compute instances start INSTANCE --zone=ZONE and gcloud compute instances stop INSTANCE --zone=ZONE change its lifecycle state; wait for the operation and inspect the resulting state. ⟦A.f10 A:tb5⟧
(mechanism) Connect to the running authorized VM with gcloud compute ssh INSTANCE --zone=ZONE to execute the workload. ⟦A.f11 A:tb5⟧
(mechanism) Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect the instance status and identity before and after the authorized lifecycle action. ⟦A.f12 A:tb5⟧
(mechanism) Create the configuration branch with git checkout -b BRANCH, commit the verified configuration, then merge the branch under the existing repository workflow. ⟦A.f13 A:tb6⟧
(mechanism) Destroy only the test deployment with docker compose -f CONFIG_PATH down, then reapply the same file and verify identical image identity and resolved runtime settings. ⟦A.f14 A:tb6⟧
(mechanism) With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading supports standard YAML tags, not arbitrary Python object constructors. ⟦A.f15 A:tb6⟧

### s04 · explainer · Verify immutable deployment configuration
(example) In the fixture, configure the approved immutable image, declared port mapping, supported replica count and resource bounds. Safely reload the YAML and inspect compose config before applying it. Compare the running image with the recorded artifact, then commit the verified configuration through the existing branch and merge workflow. Destroy only the test deployment, reapply the same file and verify identical identity and settings. Use only authorized VM lifecycle and connection actions. Secret references name injected variables, never credential values. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A.f9 A.f10 A.f11 A.f12 A.f13 A.f14 A.f15 A:tb7⟧
(misconception) A mutable tag is not the immutable release identity. Parsed configuration also does not prove running state, and deploy resource fields must be supported by the supplied runtime. ⟦A.f1 A.f6 A.f9 A:tb8⟧

### s05 · check · Check: Reproduce a model deployment from parameterized runtime configuration and an immutable artifact reference
Check your decision — 

### s06 · hands_on · Practice: Reproduce a model deployment from parameterized runtime configuration and an immutable artifact reference
Bounded fixture practice — 

### s07 · explainer · Verify a model release on an existing runtime
(intro) A launch message is not release acceptance. Verify identity, execution state and bounded endpoint behavior. ⟦B:tb1⟧
(mechanism) Verify the same recorded artifact and runtime configuration in the existing execution environment, rather than accepting the fact that deployment started as proof of a correct release. ⟦B.f1 B:tb2⟧
(mechanism) Use docker run --name NAME -p HOST_PORT:CONTAINER_PORT --env KEY=VALUE IMAGE to start the referenced image with the declared port and nonsecret runtime settings. ⟦B.f2 B:tb2⟧
(mechanism) Inspect the named container with docker container inspect NAME to check its image identity and State fields. ⟦B.f3 B:tb2⟧
(mechanism) Use docker container logs NAME to inspect its captured standard output and error for initialization or execution failures. ⟦B.f4 B:tb3⟧
(mechanism) Inspect the running container identity and State, including Health when a healthcheck is configured, and compare them with the intended release. ⟦B.f5 B:tb3⟧
(mechanism) Inspect runtime logs for initialization and execution failures without copying sensitive request data or credentials into the evidence record. ⟦B.f6 B:tb3⟧
[CODE python]
# Infrastructure helper: bounded status/body transport, not a client validation solution.
import urllib.request
from urllib.error import HTTPError

def request_bytes(request, timeout_seconds):
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            return response.status, response.read()
    except HTTPError as response:
        return response.code, response.read()

  annotations: []
[CODE python]
import json
with open("runtime_contract.json") as source:
    intended = json.load(source)
# Inspect live fixture execution separately from the intended configuration.
# Compare container Config.Image with intended["IMAGE_DIGEST"].
# Check State and Health when configured, plus sanitized initialization/execution logs.
# Bounded readiness and prediction checks must verify status and decoded payload.
# Do not interpret launch success as acceptance.
  annotations: []

### s08 · explainer · Probe readiness and prediction contracts
(mechanism) Call the declared readiness and prediction endpoints with bounded timeouts and check the returned status and payload against the expected contracts. ⟦B.f7 B:tb4⟧
(mechanism) Send a JSON request body as encoded bytes in urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST"), then read the response through urlopen with a stated timeout. ⟦B.f8 B:tb4⟧
(mechanism) Serialize structured request/response values with json.dumps; decode JSON with json.loads before inspecting fields. ⟦B.f9 B:tb4⟧
(mechanism) Inspect the small prediction fixture’s output shape and values against the declared task/response contract. ⟦B.f10 B:tb5⟧
(mechanism) Assert the declared valid, boundary and failure predicates. In ordinary non-optimized execution, a false assertion raises AssertionError. ⟦B.f11 B:tb5⟧

### s09 · explainer · Compare the running release with its record
(example) Inspect the named fixture container against the release record: image, State and Health when configured. Review initialization and execution logs without copying sensitive requests or credentials. Call readiness and prediction with stated timeouts, sending encoded JSON and decoding the response. Verify status, output shape and declared values with assertions. Plausible predictions do not repair an image-identity mismatch; retain separate identity, initialization and contract checks. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 B.f9 B.f10 B.f11 B:tb6⟧
(misconception) Launch success is not release verification. A correct-looking prediction is insufficient if the artifact identity or runtime configuration differs from the intended release. ⟦B.f1 B.f5 B.f7 B.f10 B:tb7⟧

### s10 · check · Check: Verify a model release on an existing runtime
Check your decision — 

### s11 · hands_on · Practice: Verify a model release on an existing runtime
Bounded fixture practice — 

### s12 · recap · Carry these rules forward
(takeaway) A mutable tag is not immutable identity. Parsed settings do not prove running state or deploy-field support. ⟦A.f1 A.f6 A.f9 A:tb8⟧
(takeaway) Launch success is not verification; check intended artifact, runtime configuration and prediction contract. ⟦B.f1 B.f5 B.f7 B.f10 B:tb7⟧
[UP NEXT] Enforce prediction-service authentication on an existing platform: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try again: Reproduce a model deployment from parameterized runtime configuration and an immutable artifact reference — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) Create the configuration branch with git checkout -b BRANCH, commit the verified configuration, then merge the branch under the existing repository workflow. ⟦A.f13 A:tb6⟧
(misconception) A mutable tag is not the immutable release identity. Parsed configuration also does not prove running state, and deploy resource fields must be supported by the supplied runtime. ⟦A.f1 A.f6 A.f9 A:tb8⟧
### r02 · Try again: Reproduce a model deployment from parameterized runtime configuration and an immutable artifact reference — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) Pin deployment to the recorded immutable image digest; a mutable tag may later resolve to different contents. ⟦A.f1 A:tb2⟧
(mechanism) For an authorized supplied Compute Engine VM, gcloud compute instances start INSTANCE --zone=ZONE and gcloud compute instances stop INSTANCE --zone=ZONE change its lifecycle state; wait for the operation and inspect the resulting state. ⟦A.f10 A:tb5⟧
(mechanism) Connect to the running authorized VM with gcloud compute ssh INSTANCE --zone=ZONE to execute the workload. ⟦A.f11 A:tb5⟧
(mechanism) Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect the instance status and identity before and after the authorized lifecycle action. ⟦A.f12 A:tb5⟧
(mechanism) Create the configuration branch with git checkout -b BRANCH, commit the verified configuration, then merge the branch under the existing repository workflow. ⟦A.f13 A:tb6⟧
(mechanism) Destroy only the test deployment with docker compose -f CONFIG_PATH down, then reapply the same file and verify identical image identity and resolved runtime settings. ⟦A.f14 A:tb6⟧
(mechanism) With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading supports standard YAML tags, not arbitrary Python object constructors. ⟦A.f15 A:tb6⟧
(mechanism) In the supplied Docker Compose runtime, author the mapping services: {prediction: {image: IMAGE_DIGEST, environment: {SETTING: VALUE}, ports: ["HOST_PORT:CONTAINER_PORT"], secrets: [credential], deploy: {replicas: REPLICA_COUNT}}} and top-level secrets: {credential: {environment: INJECTED_SECRET_VARIABLE}}; substitute the approved digest, nonsecret setting, port numbers, supported replica count and host secret-variable name, never the secret value. ⟦A.f2 A:tb2⟧
(mechanism) Set a service’s image to its immutable artifact reference, its ports to HOST:CONTAINER mappings, and its environment to the declared nonsecret key/value settings. ⟦A.f3 A:tb2⟧
(mechanism) Use docker compose -f CONFIG_PATH config to parse, resolve and validate the authored YAML before applying it; check its resolved fields against the intended runtime contract. ⟦A.f4 A:tb3⟧
(mechanism) Apply the declared local Compose deployment with docker compose -f CONFIG_PATH up -d and inspect the resulting containers. ⟦A.f5 A:tb3⟧
(mechanism) Set replica count at services.<service>.deploy.replicas; set resource bounds at services.<service>.deploy.resources.limits.cpus and memory in a runtime supporting these deploy fields, and validate the resolved count and bounds before applying the configuration. ⟦A.f6 A:tb3⟧
(mechanism) Keep secrets out of Dockerfile ARG and ENV: they persist in the final image or its metadata. ⟦A.f7 A:tb4⟧
(mechanism) Deliver sensitive values through runtime secrets, never as literal Compose values. ⟦A.f8 A:tb4⟧
(mechanism) After application, inspect the running image identity and compare it with the recorded artifact reference. ⟦A.f9 A:tb4⟧
(misconception) A mutable tag is not the immutable release identity. Parsed configuration also does not prove running state, and deploy resource fields must be supported by the supplied runtime. ⟦A.f1 A.f6 A.f9 A:tb8⟧
### r03 · Try again: Verify a model release on an existing runtime — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) Verify the same recorded artifact and runtime configuration in the existing execution environment, rather than accepting the fact that deployment started as proof of a correct release. ⟦B.f1 B:tb2⟧
(mechanism) Inspect the small prediction fixture’s output shape and values against the declared task/response contract. ⟦B.f10 B:tb5⟧
(mechanism) Assert the declared valid, boundary and failure predicates. In ordinary non-optimized execution, a false assertion raises AssertionError. ⟦B.f11 B:tb5⟧
(mechanism) Inspect the running container identity and State, including Health when a healthcheck is configured, and compare them with the intended release. ⟦B.f5 B:tb3⟧
(mechanism) Call the declared readiness and prediction endpoints with bounded timeouts and check the returned status and payload against the expected contracts. ⟦B.f7 B:tb4⟧
(misconception) Launch success is not release verification. A correct-looking prediction is insufficient if the artifact identity or runtime configuration differs from the intended release. ⟦B.f1 B.f5 B.f7 B.f10 B:tb7⟧
### r04 · Try again: Verify a model release on an existing runtime — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) Verify the same recorded artifact and runtime configuration in the existing execution environment, rather than accepting the fact that deployment started as proof of a correct release. ⟦B.f1 B:tb2⟧
(mechanism) Inspect the small prediction fixture’s output shape and values against the declared task/response contract. ⟦B.f10 B:tb5⟧
(mechanism) Assert the declared valid, boundary and failure predicates. In ordinary non-optimized execution, a false assertion raises AssertionError. ⟦B.f11 B:tb5⟧
(mechanism) Use docker run --name NAME -p HOST_PORT:CONTAINER_PORT --env KEY=VALUE IMAGE to start the referenced image with the declared port and nonsecret runtime settings. ⟦B.f2 B:tb2⟧
(mechanism) Inspect the named container with docker container inspect NAME to check its image identity and State fields. ⟦B.f3 B:tb2⟧
(mechanism) Use docker container logs NAME to inspect its captured standard output and error for initialization or execution failures. ⟦B.f4 B:tb3⟧
(mechanism) Inspect the running container identity and State, including Health when a healthcheck is configured, and compare them with the intended release. ⟦B.f5 B:tb3⟧
(mechanism) Inspect runtime logs for initialization and execution failures without copying sensitive request data or credentials into the evidence record. ⟦B.f6 B:tb3⟧
(mechanism) Call the declared readiness and prediction endpoints with bounded timeouts and check the returned status and payload against the expected contracts. ⟦B.f7 B:tb4⟧
(mechanism) Send a JSON request body as encoded bytes in urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST"), then read the response through urlopen with a stated timeout. ⟦B.f8 B:tb4⟧
(mechanism) Serialize structured request/response values with json.dumps; decode JSON with json.loads before inspecting fields. ⟦B.f9 B:tb4⟧
(misconception) Launch success is not release verification. A correct-looking prediction is insufficient if the artifact identity or runtime configuration differs from the intended release. ⟦B.f1 B.f5 B.f7 B.f10 B:tb7⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: One distinction to restore
· remediation_steps.eyebrow: One distinction to restore
· remediation_steps.eyebrow: One distinction to restore
· remediation_steps.eyebrow: One distinction to restore

=========

# EVALUATOR PACKET — Protect predictions and measure client outcomes (mle.tile.066_067)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.prediction_authentication — Enforce prediction-service authentication on an existing platform
B = mle.service_telemetry — Instrument prediction-service availability, errors and latency

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (mle.prediction_authentication)   objective: Adapt and test the existing service’s runtime-injected authorization configuration.
A.f1: Authentication establishes the caller identity and authorization checks whether that identity may perform the prediction action; both are needed for the supplied protected service.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/blueprints/security-foundations/authentication-authorization — Authentication and authorization]
A.f2: Reference the protected credential through an authorized runtime secret, and give it only to the service permitted to use it rather than writing its literal value in the YAML.   [sources: docker_docs#https://docs.docker.com/reference/compose-file/secrets/ — secrets]
A.f3: Inject the platform’s declared nonsecret authentication settings in the service configuration, keeping them separate from the credential secret.   [sources: docker_docs#https://docs.docker.com/reference/compose-file/services/ — image; environment; ports; healthcheck; cpus; mem_limit]
A.f4: Make one request with the authorized supplied credential and negative requests with missing or invalid credentials; verify allowed and denied responses under the existing platform policy.   [sources: python_tutorial#../library/urllib.request.html — Request; urlopen]
A.f5: Inspect runtime logs to verify failures are visible without displaying the credential or protected request values.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/logs/ — Description]
A.f6: A Compose YAML document declares services by name; use indented mappings for service fields and lists or mappings in the forms required by the Compose specification.   [sources: docker_docs#https://docs.docker.com/reference/compose-file/ — The Compose Specification]
A.f7: Set a service’s image to its immutable artifact reference, its ports to HOST:CONTAINER mappings, and its environment to the declared nonsecret key/value settings.   [sources: docker_docs#https://docs.docker.com/reference/compose-file/services/ — image; environment; ports; healthcheck; cpus; mem_limit]
A.f8: Use docker compose -f CONFIG_PATH config to parse, resolve and validate the authored YAML before applying it; check its resolved fields against the intended runtime contract.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/compose/config/ — Description; Options]
A.f9: Apply the declared local Compose deployment with docker compose -f CONFIG_PATH up -d and inspect the resulting containers.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/compose/up/ — Description]
A.f10: For the supplied Google ID-token verifier contract, use from google.oauth2 import id_token and from google.auth.transport import requests; implement authorize_prediction(token, expected_audience, permitted_subjects) to reject a missing token, call claims = id_token.verify_oauth2_token(token, requests.Request(), audience=expected_audience), and return the verified claims only when claims["sub"] is in the supplied permitted_subjects policy, otherwise raising PermissionError. Use the verified sub identity, not an unverified decode or a changeable email address.   [sources: google_mlops_pipelines#https://developers.google.com/identity/gsi/web/guides/verify-google-id-token — Using a Google API Client Library — Python; sub identifier, google_mlops_pipelines#https://raw.githubusercontent.com/googleapis/google-auth-library-python/main/google/oauth2/id_token.py — verify_oauth2_token — signature, return value, issuer check and exceptions, python_tutorial#errors.html — Raising Exceptions]
A.f11: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
A.f12: With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading accepts standard YAML tags, not arbitrary Python object constructors.   [sources: python_tutorial#https://pyyaml.org/wiki/PyYAMLDocumentation — Reference: safe_load; safe_dump]
A.f13: Use from google.auth.exceptions import GoogleAuthError; catch (ValueError, GoogleAuthError) from verification and raise PermissionError for the service harness’s declared denied HTTP path before calling prediction; a ValueError signals verification failure and GoogleAuthError includes invalid issuer. Missing credentials, invalid tokens and verified-but-unpermitted subjects must all be denied without executing prediction or logging the token.   [sources: google_mlops_pipelines#https://developers.google.com/identity/gsi/web/guides/verify-google-id-token — Using a Google API Client Library — Python; sub identifier, google_mlops_pipelines#https://raw.githubusercontent.com/googleapis/google-auth-library-python/main/google/oauth2/id_token.py — verify_oauth2_token — signature, return value, issuer check and exceptions, python_tutorial#errors.html — Handling Exceptions; Raising Exceptions]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Secure and Observe the Endpoint.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.online_prediction_contract. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Implement authorize_prediction(token, expected_audience, permitted_subjects) with learner-written Google verifier imports and connect it to the supplied endpoint harness before prediction. Author the Compose configuration using the declared PyYAML dependency, runtime secret reference, immutable image, ports and nonsecret authentication settings. Validate and apply it within the supplied infrastructure. Use reusable supplied request fixtures to send HTTP JSON requests with authorized, missing, invalid and verified-but-unpermitted credentials, and write assertions for the permitted and denied paths.  SUCCESS: The authored configuration round-trips through safe YAML loading, passes Compose validation, matches the supplied runtime contract and starts the intended containers. The authorized fixture receives the declared prediction response. Missing credentials, verification failures including invalid issuer, and verified-but-unpermitted subjects reach the declared denied HTTP path without executing prediction. Learner-written assertions pass in ordinary non-optimized execution, and inspected logs expose failures without exposing credentials or protected request values.
ASSESSMENT ANCHOR: enforce_verified_identity_and_prediction_permission facts=['f1', 'f10', 'f13']
ASSESSMENT ANCHOR: separate_runtime_credentials_from_nonsecret_settings facts=['f2', 'f3']
ASSESSMENT ANCHOR: author_validate_and_apply_protected_service_configuration facts=['f6', 'f7', 'f8', 'f9', 'f12']
ASSESSMENT ANCHOR: verify_permitted_and_denied_prediction_paths facts=['f4', 'f11', 'f13']
ASSESSMENT ANCHOR: verify_denial_visibility_without_sensitive_value_disclosure facts=['f5', 'f13']

## SOURCE FACTS — B (mle.service_telemetry)   objective: Instrument handler behavior and report a reconciled external client-availability probe.
B.f1: Choose client-visible request outcomes and latency as service indicators instead of inferring availability only from container or CPU state.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/reliability/define-reliability-based-on-user-experience-goals — Define reliability based on user experience goals]
B.f2: Measure an attempt’s elapsed time as time.perf_counter() after completion minus its start value, retaining a consistent duration unit.   [sources: python_tutorial#../library/time.html — time.perf_counter]
B.f3: Record enough timestamped outcome and duration evidence to distinguish successes, errors and timeouts in the measurement window.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/reliability/observability — Establish robust observability]
B.f4: Compute an error fraction as error attempts divided by eligible attempts, using the same clearly declared observation window and denominator as the success indicator.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/reliability/define-reliability-based-on-user-experience-goals — Define reliability based on user experience goals]
B.f5: Estimate client-visible success probability as successful eligible attempts divided by all eligible attempts in the defined measurement window, counting failed attempts in the denominator.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/reliability/define-reliability-based-on-user-experience-goals — Define reliability based on user experience goals]
B.f6: Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations.   [sources: numpy_user_guide#reference/generated/numpy.mean.html — Parameters; Notes]
B.f7: Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor.   [sources: numpy_user_guide#reference/generated/numpy.std.html — Parameters; Notes]
B.f8: Instrument the handler around JSON decoding, prediction and JSON response encoding, recording duration and status/error counts even on its handled error paths.   [sources: python_tutorial#../library/http.server.html — BaseHTTPRequestHandler]
B.f9: For the prescribed probe, retain its half-open five-minute window [t0, t0+300 seconds), its one valid request per second and all 300 attempt outcomes.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/reliability/define-reliability-based-on-user-experience-goals — Define reliability based on user experience goals]
B.f10: Count an attempt as available only for an HTTP 200 response with a valid prediction received within its two-second deadline; allow the final attempt its entire deadline before summarizing.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/reliability/define-reliability-based-on-user-experience-goals — Define reliability based on user experience goals]
B.f11: Compute availability as that successful-deadline count divided by 300, including connection-refused and response-timeout attempts that never reach the handler.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/reliability/define-reliability-based-on-user-experience-goals — Define reliability based on user experience goals]
B.f12: Reconcile absent handler records with the external failure record and report the probe window, numerator and denominator alongside handler latency/statistics and status counts.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/reliability/observability — Establish robust observability]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Secure and Observe the Endpoint.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.online_prediction_contract. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Instrument one prediction handler in the supplied service scaffolding using learner-written imports and a learner-defined Python function. Include JSON decoding, prediction and JSON response encoding in handler timing, and record timestamped durations and status/error counts on successful and handled-error paths. Calculate handler latency mean and population standard deviation. Run the supplied external probe and fault scaffolding without implementing infrastructure or probe scheduling. Summarize all 300 client-side attempt outcomes and reconcile them with handler records.  SUCCESS: The report declares the half-open attempt window [t0, t0+300 seconds), retains one valid request per second and all 300 attempts, and allows the final attempt its full two-second deadline. Its availability numerator includes only HTTP 200 responses containing a valid prediction received within the deadline; its denominator remains 300, including connection refusals and response timeouts. It reports the availability fraction and an error fraction with an explicitly declared error classification using the same window and denominator. Handler status/error counts, timestamped durations in a consistent unit, np.mean results and np.std results with ddof=0 accompany a reconciliation of external failures and absent handler records. Handler counts never replace the availability denominator.
ASSESSMENT ANCHOR: instrument_handler_latency_and_status_outcomes facts=['f1', 'f2', 'f3', 'f8']
ASSESSMENT ANCHOR: calculate_handler_latency_mean_and_standard_deviation facts=['f6', 'f7']
ASSESSMENT ANCHOR: apply_probe_window_and_response_deadline facts=['f9', 'f10']
ASSESSMENT ANCHOR: calculate_external_availability_and_error_fraction facts=['f4', 'f5', 'f11']
ASSESSMENT ANCHOR: reconcile_external_attempts_with_handler_records facts=['f3', 'f11', 'f12']

## DATA ASSETS USED
ds.serving_attempts: Complete client and handler evidence — columns: request_id(identifier), experiment(categorical), setting(categorical), attempt_index(identifier,digits-as-label), request_start_seconds(numerical), response_complete_seconds(numerical), outcome(categorical), http_status(categorical,digits-as-label), valid_prediction(categorical), handler_start_seconds(numerical), handler_complete_seconds(numerical), handler_status(categorical,digits-as-label), terminal_outcome_seconds(numerical)
   ["probe.baseline.000","probe","baseline",0,0.0,0.15,"success",200,true,0.01,0.06,200,0.15]
   ["probe.baseline.001","probe","baseline",1,1.0,1.16,"success",200,true,1.01,1.065,200,1.16]
   ["probe.baseline.002","probe","baseline",2,2.0,2.17,"success",200,true,2.01,2.07,200,2.17]
   ["probe.baseline.003","probe","baseline",3,3.0,3.18,"success",200,true,3.01,3.075,200,3.18]
   ["probe.baseline.004","probe","baseline",4,4.0,4.19,"success",200,true,4.01,4.08,200,4.19]
   ["probe.baseline.005","probe","baseline",5,5.0,5.2,"success",200,true,5.01,5.06,200,5.2]
   ["probe.baseline.006","probe","baseline",6,6.0,6.21,"success",200,true,6.01,6.065,200,6.21]
   ["probe.baseline.007","probe","baseline",7,7.0,7.15,"success",200,true,7.01,7.07,200,7.15]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute training and inference expenditure to workloads; Audit dataset, code, run and artifact lineage of a deployed model; Block release promotion when model acceptance gates fail; Choose inference batching under latency constraints; Choose scheduled, new-data or investigated quality/drift retraining triggers; Configure actionable model and service alerts; Configure bounded prediction-worker concurrency on an existing runtime; Configure replica scaling to right-size serving capacity under a service objective; Define artifact dependencies between ML pipeline stages; Detect model-input data drift against a defined reference distribution; Distinguish data drift, concept drift and observed quality degradation; Gate a retrained candidate against the incumbent using validation evidence before controlled promotion; Gate pipeline execution on dataset-quality tests; Instrument prediction-service availability, errors and latency; Invoke retraining with a versioned input snapshot from an authorized trigger; Load-test a prediction endpoint against tail-latency and sustainable-throughput objectives; Measure production model quality when labels arrive; Monitor production input and prediction 

## LESSON, in learner order

### s01 · explainer · Enforce prediction-service authentication on an existing platform
(intro) Verify who the caller is, then whether that identity may predict. Neither check replaces runtime-secret handling. ⟦A:tb1⟧
(mechanism) Authentication establishes the caller identity and authorization checks whether that identity may perform the prediction action; both are needed for the supplied protected service. ⟦A.f1 A:tb2⟧
(mechanism) Reference the protected credential through an authorized runtime secret, and give it only to the service permitted to use it rather than writing its literal value in the YAML. ⟦A.f2 A:tb2⟧
(mechanism) Inject the platform’s declared nonsecret authentication settings in the service configuration, keeping them separate from the credential secret. ⟦A.f3 A:tb2⟧
(mechanism) Make one request with the authorized supplied credential and negative requests with missing or invalid credentials; verify allowed and denied responses under the existing platform policy. ⟦A.f4 A:tb3⟧
(mechanism) Inspect runtime logs to verify failures are visible without displaying the credential or protected request values. ⟦A.f5 A:tb3⟧
(mechanism) A Compose YAML document declares services by name; use indented mappings for service fields and lists or mappings in the forms required by the Compose specification. ⟦A.f6 A:tb3⟧
[CODE python]
from google.oauth2 import id_token
from google.auth.transport import requests
from google.auth.exceptions import GoogleAuthError

def authorize_prediction(token, expected_audience, permitted_subjects):
    if not token:
        raise PermissionError("missing credential")
    try:
        claims = id_token.verify_oauth2_token(token, requests.Request(), audience=expected_audience)
    except (ValueError, GoogleAuthError):
        raise PermissionError("verification failed") from None
    if claims["sub"] not in permitted_subjects:
        raise PermissionError("unpermitted subject")
    return claims
# Harness maps PermissionError to denial before prediction.
# Log failure classes only, never the token or protected request values.
  annotations: []

### s02 · explainer · Resolve authentication runtime settings
(mechanism) Set a service’s image to its immutable artifact reference, its ports to HOST:CONTAINER mappings, and its environment to the declared nonsecret key/value settings. ⟦A.f7 A:tb4⟧
(mechanism) Use docker compose -f CONFIG_PATH config to parse, resolve and validate the authored YAML before applying it; check its resolved fields against the intended runtime contract. ⟦A.f8 A:tb4⟧
(mechanism) Apply the declared local Compose deployment with docker compose -f CONFIG_PATH up -d and inspect the resulting containers. ⟦A.f9 A:tb4⟧

### s03 · explainer · Verify tokens and permitted subjects
(mechanism) For the supplied Google ID-token verifier contract, use from google.oauth2 import id_token and from google.auth.transport import requests; implement authorize_prediction(token, expected_audience, permitted_subjects) to reject a missing token, call claims = id_token.verify_oauth2_token(token, requests.Request(), audience=expected_audience), and return the verified claims only when claims["sub"] is in the supplied permitted_subjects policy, otherwise raising PermissionError. Use the verified sub identity, not an unverified decode or a changeable email address. ⟦A.f10 A:tb5⟧
(mechanism) Assert the declared valid, boundary and failure predicates. In ordinary non-optimized execution, a false assertion raises AssertionError. ⟦A.f11 A:tb5⟧
(mechanism) With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading supports standard YAML tags, not arbitrary Python object constructors. ⟦A.f12 A:tb5⟧

### s04 · explainer · Reject unauthorized requests before prediction
(mechanism) Use from google.auth.exceptions import GoogleAuthError; catch (ValueError, GoogleAuthError) from verification and raise PermissionError for the service harness’s declared denied HTTP path before calling prediction; a ValueError signals verification failure and GoogleAuthError includes invalid issuer. Missing credentials, invalid tokens and verified-but-unpermitted subjects must all be denied without executing prediction or logging the token. ⟦A.f13 A:tb6⟧
(example) Use the supplied audience and permitted-subject policy. Reject a missing token; verify an offered token, then check verified sub membership. A verified but unpermitted subject is denied too. Convert declared verification exceptions into the denied HTTP path before prediction. Safely inspect Compose image, ports, nonsecret settings and runtime secret references. Test authorized, missing, invalid and unpermitted fixtures. Denied requests must neither execute prediction nor disclose tokens in logs. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A.f9 A.f10 A.f11 A.f12 A.f13 A:tb7⟧
(misconception) Authentication does not automatically grant authorization. A verified-but-unpermitted subject must be denied, and neither YAML nor logs should contain the credential's literal value. ⟦A.f1 A.f10 A.f13 A:tb8⟧

### s05 · check · Check: Enforce prediction-service authentication on an existing platform
Check your decision — 

### s06 · hands_on · Practice: Enforce prediction-service authentication on an existing platform
Bounded fixture practice — 

### s07 · explainer · Instrument prediction-service availability, errors and latency
(intro) Client outcomes can differ from handler records. Reconcile external requests with handler timing, including attempts that never arrived. ⟦B:tb1⟧
(mechanism) Choose client-visible request outcomes and latency as service indicators instead of inferring availability only from container or CPU state. ⟦B.f1 B:tb2⟧
(mechanism) Measure an attempt’s elapsed time as time.perf_counter() after completion minus its start value, retaining a consistent duration unit. ⟦B.f2 B:tb2⟧
(mechanism) Record enough timestamped outcome and duration evidence to distinguish successes, errors and timeouts in the measurement window. ⟦B.f3 B:tb2⟧
(mechanism) Compute an error fraction as error attempts divided by eligible attempts, using the same clearly declared observation window and denominator as the success indicator. ⟦B.f4 B:tb3⟧
(mechanism) Estimate client-visible success probability as successful eligible attempts divided by all eligible attempts in the defined measurement window, counting failed attempts in the denominator. ⟦B.f5 B:tb3⟧
(mechanism) Use np.mean(numeric_values) for the arithmetic mean of the selected numeric observations. ⟦B.f6 B:tb3⟧
[TABLE ds.serving_attempts cols=all ] caption: Authored offline attempts: reconcile client outcomes with handler timestamps and absent handler records. These are not production measurements.

### s08 · explainer · Count every scheduled probe attempt
(mechanism) Use np.std(numeric_values, ddof=0): divide squared deviations by N, then take the square root. Use ddof=1 only when the declared calculation requires N−1. ⟦B.f7 B:tb4⟧
(mechanism) Instrument the handler around JSON decoding, prediction and JSON response encoding, recording duration and status/error counts even on its handled error paths. ⟦B.f8 B:tb4⟧
(mechanism) For the prescribed probe, retain its half-open five-minute window [t0, t0+300 seconds), its one valid request per second and all 300 attempt outcomes. ⟦B.f9 B:tb4⟧
(mechanism) Count an attempt as available only for an HTTP 200 response with a valid prediction received within its two-second deadline; allow the final attempt its entire deadline before summarizing. ⟦B.f10 B:tb5⟧
(mechanism) Compute availability as that successful-deadline count divided by 300, including connection-refused and response-timeout attempts that never reach the handler. ⟦B.f11 B:tb5⟧
(mechanism) Reconcile absent handler records with the external failure record and report the probe window, numerator and denominator alongside handler latency/statistics and status counts. ⟦B.f12 B:tb5⟧

### s09 · explainer · Separate probe availability from handler telemetry
(example) For the prescribed probe, retain every scheduled attempt, including connection refusals and timeouts with no handler record. Count only valid successful predictions received by the deadline, allowing the final attempt its full deadline before summarizing. Report the window, successful-deadline numerator and full attempt denominator. Reconcile missing handler events with external failures. Handler timing covers JSON decoding, prediction and encoding, including handled error paths; its success rate alone is not client-visible availability. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f8 B.f9 B.f10 B.f11 B.f12 B:tb6⟧
(misconception) Handler success rate is not automatically client-visible availability. Excluding attempts that never reached the handler would omit part of the prescribed denominator and conceal failures. ⟦B.f5 B.f10 B.f11 B.f12 B:tb7⟧

### s10 · check · Check: Instrument prediction-service availability, errors and latency
Check your decision — 

### s11 · hands_on · Practice: Instrument prediction-service availability, errors and latency
Bounded fixture practice — 

### s12 · recap · Carry these rules forward
(takeaway) Verified identity still needs permission. Never put credential values in YAML or logs. ⟦A.f1 A.f10 A.f13 A:tb8⟧
(takeaway) Handler success rate is not client availability; retain attempts that never reached the handler. ⟦B.f5 B.f10 B.f11 B.f12 B:tb7⟧
[UP NEXT] Load-test a prediction endpoint against tail-latency and sustainable-throughput objectives: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try again: Enforce prediction-service authentication on an existing platform — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) Use from google.auth.exceptions import GoogleAuthError; catch (ValueError, GoogleAuthError) from verification and raise PermissionError for the service harness’s declared denied HTTP path before calling prediction; a ValueError signals verification failure and GoogleAuthError includes invalid issuer. Missing credentials, invalid tokens and verified-but-unpermitted subjects must all be denied without executing prediction or logging the token. ⟦A.f13 A:tb6⟧
(mechanism) Inspect runtime logs to verify failures are visible without displaying the credential or protected request values. ⟦A.f5 A:tb3⟧
(misconception) Authentication does not automatically grant authorization. A verified-but-unpermitted subject must be denied, and neither YAML nor logs should contain the credential's literal value. ⟦A.f1 A.f10 A.f13 A:tb8⟧
### r02 · Try again: Enforce prediction-service authentication on an existing platform — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) Authentication establishes the caller identity and authorization checks whether that identity may perform the prediction action; both are needed for the supplied protected service. ⟦A.f1 A:tb2⟧
(mechanism) For the supplied Google ID-token verifier contract, use from google.oauth2 import id_token and from google.auth.transport import requests; implement authorize_prediction(token, expected_audience, permitted_subjects) to reject a missing token, call claims = id_token.verify_oauth2_token(token, requests.Request(), audience=expected_audience), and return the verified claims only when claims["sub"] is in the supplied permitted_subjects policy, otherwise raising PermissionError. Use the verified sub identity, not an unverified decode or a changeable email address. ⟦A.f10 A:tb5⟧
(mechanism) Assert the declared valid, boundary and failure predicates. In ordinary non-optimized execution, a false assertion raises AssertionError. ⟦A.f11 A:tb5⟧
(mechanism) With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading supports standard YAML tags, not arbitrary Python object constructors. ⟦A.f12 A:tb5⟧
(mechanism) Use from google.auth.exceptions import GoogleAuthError; catch (ValueError, GoogleAuthError) from verification and raise PermissionError for the service harness’s declared denied HTTP path before calling prediction; a ValueError signals verification failure and GoogleAuthError includes invalid issuer. Missing credentials, invalid tokens and verified-but-unpermitted subjects must all be denied without executing prediction or logging the token. ⟦A.f13 A:tb6⟧
(mechanism) Reference the protected credential through an authorized runtime secret, and give it only to the service permitted to use it rather than writing its literal value in the YAML. ⟦A.f2 A:tb2⟧
(mechanism) Inject the platform’s declared nonsecret authentication settings in the service configuration, keeping them separate from the credential secret. ⟦A.f3 A:tb2⟧
(mechanism) Make one request with the authorized supplied credential and negative requests with missing or invalid credentials; verify allowed and denied responses under the existing platform policy. ⟦A.f4 A:tb3⟧
(mechanism) A Compose YAML document declares services by name; use indented mappings for service fields and lists or mappings in the forms required by the Compose specification. ⟦A.f6 A:tb3⟧
(mechanism) Set a service’s image to its immutable artifact reference, its ports to HOST:CONTAINER mappings, and its environment to the declared nonsecret key/value settings. ⟦A.f7 A:tb4⟧
(mechanism) Use docker compose -f CONFIG_PATH config to parse, resolve and validate the authored YAML before applying it; check its resolved fields against the intended runtime contract. ⟦A.f8 A:tb4⟧
(mechanism) Apply the declared local Compose deployment with docker compose -f CONFIG_PATH up -d and inspect the resulting containers. ⟦A.f9 A:tb4⟧
(misconception) Authentication does not automatically grant authorization. A verified-but-unpermitted subject must be denied, and neither YAML nor logs should contain the credential's literal value. ⟦A.f1 A.f10 A.f13 A:tb8⟧
### r03 · Try again: Instrument prediction-service availability, errors and latency — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) Compute availability as that successful-deadline count divided by 300, including connection-refused and response-timeout attempts that never reach the handler. ⟦B.f11 B:tb5⟧
(mechanism) Reconcile absent handler records with the external failure record and report the probe window, numerator and denominator alongside handler latency/statistics and status counts. ⟦B.f12 B:tb5⟧
(mechanism) Record enough timestamped outcome and duration evidence to distinguish successes, errors and timeouts in the measurement window. ⟦B.f3 B:tb2⟧
(misconception) Handler success rate is not automatically client-visible availability. Excluding attempts that never reached the handler would omit part of the prescribed denominator and conceal failures. ⟦B.f5 B.f10 B.f11 B.f12 B:tb7⟧
### r04 · Try again: Instrument prediction-service availability, errors and latency — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) Choose client-visible request outcomes and latency as service indicators instead of inferring availability only from container or CPU state. ⟦B.f1 B:tb2⟧
(mechanism) Count an attempt as available only for an HTTP 200 response with a valid prediction received within its two-second deadline; allow the final attempt its entire deadline before summarizing. ⟦B.f10 B:tb5⟧
(mechanism) Compute availability as that successful-deadline count divided by 300, including connection-refused and response-timeout attempts that never reach the handler. ⟦B.f11 B:tb5⟧
(mechanism) Reconcile absent handler records with the external failure record and report the probe window, numerator and denominator alongside handler latency/statistics and status counts. ⟦B.f12 B:tb5⟧
(mechanism) Measure an attempt’s elapsed time as time.perf_counter() after completion minus its start value, retaining a consistent duration unit. ⟦B.f2 B:tb2⟧
(mechanism) Record enough timestamped outcome and duration evidence to distinguish successes, errors and timeouts in the measurement window. ⟦B.f3 B:tb2⟧
(mechanism) Compute an error fraction as error attempts divided by eligible attempts, using the same clearly declared observation window and denominator as the success indicator. ⟦B.f4 B:tb3⟧
(mechanism) Estimate client-visible success probability as successful eligible attempts divided by all eligible attempts in the defined measurement window, counting failed attempts in the denominator. ⟦B.f5 B:tb3⟧
(mechanism) Use np.mean(numeric_values) for the arithmetic mean of the selected numeric observations. ⟦B.f6 B:tb3⟧
(mechanism) Use np.std(numeric_values, ddof=0): divide squared deviations by N, then take the square root. Use ddof=1 only when the declared calculation requires N−1. ⟦B.f7 B:tb4⟧
(mechanism) Instrument the handler around JSON decoding, prediction and JSON response encoding, recording duration and status/error counts even on its handled error paths. ⟦B.f8 B:tb4⟧
(mechanism) For the prescribed probe, retain its half-open five-minute window [t0, t0+300 seconds), its one valid request per second and all 300 attempt outcomes. ⟦B.f9 B:tb4⟧
(misconception) Handler success rate is not automatically client-visible availability. Excluding attempts that never reached the handler would omit part of the prescribed denominator and conceal failures. ⟦B.f5 B.f10 B.f11 B.f12 B:tb7⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: One distinction to restore
· remediation_steps.eyebrow: One distinction to restore
· remediation_steps.eyebrow: One distinction to restore
· remediation_steps.eyebrow: One distinction to restore

=========

# EVALUATOR PACKET — Measure and bound serving capacity (mle.tile.068_071)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.prediction_load_test — Load-test a prediction endpoint against tail-latency and sustainable-throughput objectives
B = mle.inference_batching_decision — Choose inference batching under latency constraints
C = mle.serving_worker_concurrency — Configure bounded prediction-worker concurrency on an existing runtime
D = mle.serving_replica_scaling — Configure replica scaling to right-size serving capacity under a service objective

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (mle.prediction_load_test)   objective: Measure the highest feasible stable-throughput load point under fixed error and tail-latency constraints.
A.f1: Exercise the endpoint with the declared arrival/concurrency profile and bounded duration, and record client-visible outcomes and response times rather than only attempted request count.   [sources: sagemaker_model_deployment#inference-recommender-load-test.html — Create an Advanced Job Using Customized Load Tests]
A.f2: Treat a load point as acceptable only if it meets the predeclared client-visible success and tail-latency requirements, as well as the required completed throughput.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/reliability/define-reliability-based-on-user-experience-goals — Define reliability based on user experience goals]
A.f3: Retain failures and timeouts separately so latency measured only for completed responses is not misrepresented as the experience of every attempted request.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/reliability/define-reliability-based-on-user-experience-goals — Define reliability based on user experience goals]
A.f4: Estimate client-visible success probability as successful eligible attempts divided by all eligible attempts in the defined measurement window, counting failed attempts in the denominator.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/reliability/define-reliability-based-on-user-experience-goals — Define reliability based on user experience goals]
A.f5: Compute the declared tail-latency percentile with np.percentile(completed_latency_values, declared_percentile), retaining its convention, sample count and time unit.   [sources: numpy_user_guide#reference/generated/numpy.percentile.html — Parameters; Notes]
A.f6: Measure completed successful requests divided by elapsed measurement time for successful throughput, and compare it with the offered load rather than equating arrivals with completed work.   [sources: sagemaker_model_deployment#inference-recommender-load-test.html — Create an Advanced Job Using Customized Load Tests]
A.f7: Run valid and malformed HTTP JSON fixtures with assertions, keeping intentional malformed tests outside the valid-traffic capacity measurement.   [sources: python_tutorial#../library/urllib.request.html — Request; urlopen]
A.f8: At every fixed offered load, use the stated valid payload mix, warm-up and fixed measurement duration, counting successful completions, HTTP errors, timeouts and other failed attempts separately.   [sources: sagemaker_model_deployment#inference-recommender-load-test.html — Create an Advanced Job Using Customized Load Tests]
A.f9: Compute failed-request fraction from all failed attempts divided by all valid-traffic attempts; timeouts remain failures.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/reliability/define-reliability-based-on-user-experience-goals — Define reliability based on user experience goals]
A.f10: Inspect backlog growth and unfinished work throughout the window; accept only stable-backlog loads meeting the predeclared tail-latency and error limits, and report the highest measured successful throughput or no feasible measured envelope.   [sources: sagemaker_model_deployment#inference-recommender-load-test.html — Create an Advanced Job Using Customized Load Tests]
A.f11: Use docker run --name NAME -p HOST_PORT:CONTAINER_PORT --env KEY=VALUE IMAGE to start the referenced image with the declared port and nonsecret runtime settings.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/run/ — Publish or expose port; Set environment variables; Specify a container name]
A.f12: Inspect the named container with docker container inspect NAME to check its image identity and State fields.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/inspect/ — Description; Examples]
A.f13: Use docker container logs NAME to inspect its captured standard output and error for initialization or execution failures.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/logs/ — Description]
A.f14: Send a JSON request body as encoded bytes in urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST"), then read the response through urlopen with a stated timeout.   [sources: python_tutorial#../library/urllib.request.html — Request; urlopen]
A.f15: Use json.dumps to encode structured request/response values and json.loads to decode JSON before checking their fields.   [sources: python_tutorial#inputoutput.html — Saving structured data with json]
A.f16: Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations.   [sources: numpy_user_guide#reference/generated/numpy.mean.html — Parameters; Notes]
A.f17: Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor.   [sources: numpy_user_guide#reference/generated/numpy.std.html — Parameters; Notes]
A.f18: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Load-Test and Scale Serving.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.online_prediction_contract, mle.prediction_schema_validation, mle.service_telemetry, mle.deployment_verification, mle.model_service_readiness. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Run and inspect the supplied prediction-service image with its declared published HTTP port and nonsecret runtime settings. Author reusable valid, boundary and malformed JSON fixtures with assertions for the declared contract, keeping intentional rejection checks separate from capacity measurements. Use the supplied bounded load driver to exercise a small fixed range of offered rates with the stated valid payload mix, arrival/concurrency profile, warm-up and measurement duration. Account for outcomes, calculate completed-response latency statistics and successful throughput, inspect backlog throughout each window, and determine the measured feasible envelope against predeclared requirements.  SUCCESS: The named container has the expected image identity and running State, and its captured logs have been inspected. Fixture assertions verify successful predictions and declared invalid-request rejections. Each measured load reports attempted requests, successful completions, HTTP errors, timeouts, other failures and unfinished work without silently discarding attempts. Reports include successful completions per elapsed second, success probability, failed-request fraction, completed-response latency mean, standard deviation and declared percentile with sample count, convention and units. Only loads with stable backlog satisfying all declared success, latency, error and completed-throughput requirements pass. The final result identifies the highest measured successful throughput among passing loads, or explicitly reports no feasible measured envelope.
ASSESSMENT ANCHOR: define_representative_valid_traffic_measurement facts=['f1', 'f7', 'f8']
ASSESSMENT ANCHOR: account_for_all_attempts_and_failures facts=['f3', 'f4', 'f8', 'f9']
ASSESSMENT ANCHOR: distinguish_offered_rate_from_successful_throughput facts=['f1', 'f6']
ASSESSMENT ANCHOR: interpret_completed_response_tail_latency facts=['f3', 'f5']
ASSESSMENT ANCHOR: establish_feasible_measured_throughput_envelope facts=['f2', 'f9', 'f10']

## SOURCE FACTS — B (mle.inference_batching_decision)   objective: Select a batching limit from matched end-to-end latency traces.
B.f2: Use json.dumps to encode structured request/response values and json.loads to decode JSON before checking their fields.   [sources: python_tutorial#inputoutput.html — Saving structured data with json]
B.f3: Match each successful JSON response to its request identity and batching setting before computing its end-to-end duration from the trace.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
B.f4: Use response-completion minus request-start time in one declared unit, including batch waiting time in the latency interpretation.   [sources: python_tutorial#../library/time.html — time.perf_counter]
B.f5: Calculate the required tail percentile with np.percentile(latencies, declared_percentile), keeping the convention and successful-response sample count explicit.   [sources: numpy_user_guide#reference/generated/numpy.percentile.html — Parameters; Notes]
B.f6: Choose only a batching limit meeting the stated latency objective, comparing the same trace/population interpretation.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/reliability/define-reliability-based-on-user-experience-goals — Define reliability based on user experience goals]
B.f7: Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations.   [sources: numpy_user_guide#reference/generated/numpy.mean.html — Parameters; Notes]
B.f8: Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor.   [sources: numpy_user_guide#reference/generated/numpy.std.html — Parameters; Notes]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Load-Test and Scale Serving.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: none within this path. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Encode structured trace values as JSON and decode supplied HTTP JSON request/response traces for two batching settings. Match successful responses to their request identities and settings, calculate end-to-end durations, mean, standard deviation and the declared tail percentile, then choose a supplied batching limit satisfying the latency objective.  SUCCESS: Only matched successful responses contribute durations. Both settings use response-completion minus request-start in the same declared unit, including batch waiting. Results report successful-response counts, arithmetic means, standard deviations with the required divisor, and tail percentiles with an explicit convention. The chosen limit meets the stated objective under the same trace/population interpretation.
ASSESSMENT ANCHOR: choose_batching_limit_meeting_tail_latency_objective facts=['f3', 'f4', 'f5', 'f6']

## SOURCE FACTS — C (mle.serving_worker_concurrency)   objective: Apply and verify a configured worker bound under supplied request load.
C.f1: A Compose YAML document declares services by name; use indented mappings for service fields and lists or mappings in the forms required by the Compose specification.   [sources: docker_docs#https://docs.docker.com/reference/compose-file/ — The Compose Specification]
C.f2: Set a service’s image to its immutable artifact reference, its ports to HOST:CONTAINER mappings, and its environment to the declared nonsecret key/value settings.   [sources: docker_docs#https://docs.docker.com/reference/compose-file/services/ — image; environment; ports; healthcheck; cpus; mem_limit]
C.f3: Use docker compose -f CONFIG_PATH config to parse, resolve and validate the authored YAML before applying it; check its resolved fields against the intended runtime contract.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/compose/config/ — Description; Options]
C.f4: Apply the declared local Compose deployment with docker compose -f CONFIG_PATH up -d and inspect the resulting containers.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/compose/up/ — Description]
C.f5: Set the existing runtime’s worker-limit setting in the YAML, validate its parsed value and run the referenced image under that bound.   [sources: docker_docs#https://docs.docker.com/reference/compose-file/services/ — image; environment; ports; healthcheck; cpus; mem_limit]
C.f6: Inspect running worker processes with docker container top NAME during the load fixture and compare the observed count with the configured limit to detect oversubscription.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/top/ — Description]
C.f7: Inspect concurrent CPU/memory usage during the same fixture to support the bound check rather than assuming the configuration was honored.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/stats/ — Description; Examples]
C.f8: With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading accepts standard YAML tags, not arbitrary Python object constructors.   [sources: python_tutorial#https://pyyaml.org/wiki/PyYAMLDocumentation — Reference: safe_load; safe_dump]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Load-Test and Scale Serving.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: none within this path. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Configure the approved limit of two workers for the supplied containerized runtime. Write and reload its Compose YAML safely, validate the resolved runtime contract, apply the supplied immutable image, and inspect worker processes and CPU/memory usage during the supplied load fixture.  SUCCESS: The reloaded YAML and Compose-resolved configuration preserve the supplied service name, immutable image, port mappings and nonsecret environment settings, with the worker limit set to two. The runtime is applied and inspected. Evidence from the same load interval distinguishes worker processes from other processes, compares the worker count with two, and records concurrent CPU/memory usage. Any excess worker count is identified as oversubscription rather than accepted because configuration validation succeeded.
ASSESSMENT ANCHOR: validate_safe_runtime_configuration facts=['f1', 'f2', 'f3', 'f8']
ASSESSMENT ANCHOR: apply_declared_worker_bound facts=['f4', 'f5']
ASSESSMENT ANCHOR: detect_worker_oversubscription_under_load facts=['f5', 'f6', 'f7']

## SOURCE FACTS — D (mle.serving_replica_scaling)   objective: Verify a bounded replica policy from demand evidence and restore the original runtime settings.
D.f1: For a fixed Compose scaling fixture, declare deploy.replicas or use docker compose up -d --scale SERVICE=COUNT, then inspect the actual replica count.   [sources: docker_docs#https://docs.docker.com/reference/compose-file/deploy/ — replicas; resources; restart_policy]
D.f2: For SageMaker Application Auto Scaling, register the supplied endpoint variant as a scalable target with explicit MinCapacity and MaxCapacity bounds.   [sources: sagemaker_model_deployment#endpoint-auto-scaling-add-code-define.html — Register a model as a scalable target]
D.f3: A target-tracking scaling policy specifies a metric, target value and scale-in/scale-out cooldowns; apply only the supported supplied policy to the existing scalable target.   [sources: sagemaker_model_deployment#endpoint-auto-scaling-add-code-apply.html — Apply a scaling policy]
D.f4: Compare scale settings at the same declared load and select capacity that meets observed success, p99 latency and throughput requirements rather than assuming more replicas are always better.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/reliability/define-reliability-based-on-user-experience-goals — Define reliability based on user experience goals]
D.f5: Estimate client-visible success probability as successful eligible attempts divided by all eligible attempts in the defined measurement window, counting failed attempts in the denominator.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/reliability/define-reliability-based-on-user-experience-goals — Define reliability based on user experience goals]
D.f6: Compute the declared tail-latency percentile with np.percentile(completed_latency_values, declared_percentile), retaining its convention, sample count and time unit.   [sources: numpy_user_guide#reference/generated/numpy.percentile.html — Parameters; Notes]
D.f7: Measure completed successful requests divided by elapsed measurement time for successful throughput, and compare it with the offered load rather than equating arrivals with completed work.   [sources: sagemaker_model_deployment#inference-recommender-load-test.html — Create an Advanced Job Using Customized Load Tests]
D.f8: Edit the existing runtime’s YAML replica policy from the demand/capacity evidence, then parse and inspect the resolved replica bounds before applying it.   [sources: docker_docs#https://docs.docker.com/reference/compose-file/ — The Compose Specification]
D.f9: Inspect running containers before and after the bounded demand change and compare the observed count and identities with the intended replica policy.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/inspect/ — Description; Examples]
D.f10: Restore the nonproduction runtime’s original replica and lifecycle settings after the bounded scaling check.   [sources: google_mlops_pipelines#https://cloud.google.com/compute/docs/instances/stop-start-instance — Stop an instance; Start an instance]
D.f11: Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations.   [sources: numpy_user_guide#reference/generated/numpy.mean.html — Parameters; Notes]
D.f12: Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor.   [sources: numpy_user_guide#reference/generated/numpy.std.html — Parameters; Notes]
D.f13: Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect the instance status and identity before and after the authorized lifecycle action.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/sdk/gcloud/reference/compute/instances/describe — DESCRIPTION; EXAMPLES]
D.f14: With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading accepts standard YAML tags, not arbitrary Python object constructors.   [sources: python_tutorial#https://pyyaml.org/wiki/PyYAMLDocumentation — Reference: safe_load; safe_dump]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Load-Test and Scale Serving.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.prediction_load_test, mle.service_telemetry. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Configure the supplied nonproduction runtime from demand/capacity evidence. Calculate the declared mean and standard deviation, select bounded replica settings against the service objective, edit and safely reload its YAML configuration, and inspect resolved fields before applying it. Inspect running containers and instance identity/status before and after the authorized bounded demand and lifecycle actions, then restore the original replica and lifecycle settings.  SUCCESS: The selected configuration satisfies the declared success probability, p99 latency and successful-throughput requirements at the same offered load. Calculations retain the specified window, denominator, percentile convention, sample count and time unit. Resolved settings match the permitted policy, observed container counts and identities are checked against it, instance state is inspected before and after the authorized action, and the original nonproduction settings are restored with evidence retained.
ASSESSMENT ANCHOR: select_capacity_meeting_service_objective facts=['f4', 'f5', 'f6', 'f7']
ASSESSMENT ANCHOR: interpret_demand_and_capacity_summary_statistics facts=['f11', 'f12']
ASSESSMENT ANCHOR: select_and_validate_bounded_replica_settings facts=['f1', 'f2', 'f3', 'f8', 'f14']
ASSESSMENT ANCHOR: verify_observed_scaling_and_restore_original_settings facts=['f9', 'f10', 'f13']

## DATA ASSETS USED
ds.backlog: Backlog observations throughout each measurement — columns: experiment(categorical), setting(categorical), elapsed_seconds(numerical), unfinished_requests(numerical)
   ["load","rate_5",0.0,0]
   ["load","rate_5",5.0,0]
   ["load","rate_5",10.0,0]
   ["load","rate_10",0.0,0]
   ["load","rate_10",5.0,2]
   ["load","rate_10",10.0,4]
   ["load","rate_15",0.0,0]
   ["load","rate_15",5.0,2]
ds.batching_trace: Identified batching trace — columns: request_id(identifier), batching_setting(categorical), request_start_seconds(numerical), batch_wait_end_seconds(numerical), response_complete_seconds(numerical), success(categorical), response_json(text)
   ["order_1","limit_1",1.0,1.0,1.2,true,"{\"request_id\": \"order_1\", \"batching_setting\": \"limit_1\", \"predictions\": [5.0]}"]
   ["order_2","limit_1",2.0,2.0,2.2,true,"{\"request_id\": \"order_2\", \"batching_setting\": \"limit_1\", \"predictions\": [8.0]}"]
   ["order_3","limit_1",3.0,3.0,3.2,true,"{\"request_id\": \"order_3\", \"batching_setting\": \"limit_1\", \"predictions\": [11.0]}"]
   ["order_4","limit_1",4.0,4.0,4.2,true,"{\"request_id\": \"order_4\", \"batching_setting\": \"limit_1\", \"predictions\": [14.0]}"]
   ["order_5","limit_1",5.0,5.0,5.2,true,"{\"request_id\": \"order_5\", \"batching_setting\": \"limit_1\", \"predictions\": [17.0]}"]
   ["order_1","limit_2",1.0,1.4,1.6,true,"{\"request_id\": \"order_1\", \"batching_setting\": \"limit_2\", \"predictions\": [5.0]}"]
   ["order_2","limit_2",2.0,2.4,2.6,true,"{\"request_id\": \"order_2\", \"batching_setting\": \"limit_2\", \"predictions\": [8.0]}"]
   ["order_3","limit_2",3.0,3.4,3.6,true,"{\"request_id\": \"order_3\", \"batching_setting\": \"limit_2\", \"predictions\": [11.0]}"]
ds.replica_states: Original, changed and restored identities — columns: phase(categorical), intended_replicas(numerical), container_name(identifier), container_running(categorical), instance(identifier), zone(categorical), instance_status(categorical)
   ["original",1,"prediction-1",true,"order-lab","fixture-zone","RUNNING"]
   ["changed_two",2,"prediction-1",true,"order-lab","fixture-zone","RUNNING"]
   ["changed_two",2,"prediction-2",true,"order-lab","fixture-zone","RUNNING"]
   ["changed_three",3,"prediction-1",true,"order-lab","fixture-zone","RUNNING"]
   ["changed_three",3,"prediction-2",true,"order-lab","fixture-zone","RUNNING"]
   ["changed_three",3,"prediction-3",true,"order-lab","fixture-zone","RUNNING"]
   ["restored",1,"prediction-1",true,"order-lab","fixture-zone","RUNNING"]
ds.serving_attempts: Complete client and handler evidence — columns: request_id(identifier), experiment(categorical), setting(categorical), attempt_index(identifier,digits-as-label), request_start_seconds(numerical), response_complete_seconds(numerical), outcome(categorical), http_status(categorical,digits-as-label), valid_prediction(categorical), handler_start_seconds(numerical), handler_complete_seconds(numerical), handler_status(categorical,digits-as-label), terminal_outcome_seconds(numerical)
   ["probe.baseline.000","probe","baseline",0,0.0,0.15,"success",200,true,0.01,0.06,200,0.15]
   ["probe.baseline.001","probe","baseline",1,1.0,1.16,"success",200,true,1.01,1.065,200,1.16]
   ["probe.baseline.002","probe","baseline",2,2.0,2.17,"success",200,true,2.01,2.07,200,2.17]
   ["probe.baseline.003","probe","baseline",3,3.0,3.18,"success",200,true,3.01,3.075,200,3.18]
   ["probe.baseline.004","probe","baseline",4,4.0,4.19,"success",200,true,4.01,4.08,200,4.19]
   ["probe.baseline.005","probe","baseline",5,5.0,5.2,"success",200,true,5.01,5.06,200,5.2]
   ["probe.baseline.006","probe","baseline",6,6.0,6.21,"success",200,true,6.01,6.065,200,6.21]
   ["probe.baseline.007","probe","baseline",7,7.0,7.15,"success",200,true,7.01,7.07,200,7.15]
ds.worker_processes: Authored container-top process snapshots — columns: interval_id(identifier), container_name(identifier), pid(identifier,digits-as-label), process_kind(categorical), is_prediction_worker(categorical)
   ["within_limit","prediction",100,"supervisor",false]
   ["within_limit","prediction",101,"prediction_worker",true]
   ["within_limit","prediction",102,"prediction_worker",true]
   ["oversubscribed","prediction",100,"supervisor",false]
   ["oversubscribed","prediction",101,"prediction_worker",true]
   ["oversubscribed","prediction",102,"prediction_worker",true]
   ["oversubscribed","prediction",103,"prediction_worker",true]
ds.worker_resources: Concurrent CPU and memory observations — columns: interval_id(identifier), elapsed_seconds(numerical), cpu_percent(numerical), memory_mib(numerical)
   ["within_limit",0.0,70.0,128.0]
   ["within_limit",5.0,75.0,138.0]
   ["within_limit",10.0,80.0,148.0]
   ["oversubscribed",0.0,95.0,192.0]
   ["oversubscribed",5.0,100.0,202.0]
   ["oversubscribed",10.0,105.0,212.0]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute training and inference expenditure to workloads; Audit dataset, code, run and artifact lineage of a deployed model; Block release promotion when model acceptance gates fail; Choose inference batching under latency constraints; Choose scheduled, new-data or investigated quality/drift retraining triggers; Configure actionable model and service alerts; Configure bounded prediction-worker concurrency on an existing runtime; Configure replica scaling to right-size serving capacity under a service objective; Define artifact dependencies between ML pipeline stages; Detect model-input data drift against a defined reference distribution; Distinguish data drift, concept drift and observed quality degradation; Gate a retrained candidate against the incumbent using validation evidence before controlled promotion; Gate pipeline execution on dataset-quality tests; Invoke retraining with a versioned input snapshot from an authorized trigger; Measure production model quality when labels arrive; Monitor production input and prediction distributions; Prevent duplicate or overlapping retraining runs; Promote an approved registry version through accountable staged ML release gates; Recover a

## LESSON, in learner order

### s01 · explainer · Load-test a prediction endpoint against tail-latency and sustainable-throughput objectives
(intro) Measure a capacity envelope from client outcomes, tail latency, completed work and backlog at each declared load. ⟦A:tb1⟧
(mechanism) Exercise the endpoint with the declared arrival/concurrency profile and bounded duration, and record client-visible outcomes and response times rather than only attempted request count. ⟦A.f1 A:tb2⟧
(mechanism) Treat a load point as acceptable only if it meets the predeclared client-visible success and tail-latency requirements, as well as the required completed throughput. ⟦A.f2 A:tb2⟧
(mechanism) Retain failures and timeouts separately so latency measured only for completed responses is not misrepresented as the experience of every attempted request. ⟦A.f3 A:tb2⟧
(mechanism) Estimate client-visible success probability as successful eligible attempts divided by all eligible attempts in the defined measurement window, counting failed attempts in the denominator. ⟦A.f4 A:tb3⟧
(mechanism) Compute the declared tail-latency percentile with np.percentile(completed_latency_values, declared_percentile), retaining its convention, sample count and time unit. ⟦A.f5 A:tb3⟧
(mechanism) Measure successful throughput as completed successful requests divided by elapsed measurement time, and compare it with the offered load rather than equating arrivals with completed work. ⟦A.f6 A:tb3⟧
[TABLE ds.serving_attempts cols=all ] caption: Authored offline attempts include multiple experiment settings. Select the declared valid-traffic load population before calculating capacity; retain errors and timeouts.
[TABLE ds.backlog cols=all ] caption: Authored unfinished-work observations for the same fixed load settings; inspect change across the measurement window.

### s02 · explainer · Measure valid-traffic load outcomes
(mechanism) Run valid and malformed HTTP JSON fixtures with assertions, keeping intentional malformed tests outside the valid-traffic capacity measurement. ⟦A.f7 A:tb4⟧
(mechanism) At every fixed offered load, use the stated valid payload mix, warm-up and fixed measurement duration, counting successful completions, HTTP errors, timeouts and other failed attempts separately. ⟦A.f8 A:tb4⟧
(mechanism) Compute failed-request fraction from all failed attempts divided by all valid-traffic attempts; timeouts remain failures. ⟦A.f9 A:tb4⟧
(mechanism) Inspect backlog growth and unfinished work throughout the window; accept only stable-backlog loads meeting the predeclared tail-latency and error limits, and report the highest measured successful throughput or no feasible measured envelope. ⟦A.f10 A:tb5⟧
(mechanism) Use docker run --name NAME -p HOST_PORT:CONTAINER_PORT --env KEY=VALUE IMAGE to start the referenced image with the declared port and nonsecret runtime settings. ⟦A.f11 A:tb5⟧
(mechanism) Inspect the named container with docker container inspect NAME to check its image identity and State fields. ⟦A.f12 A:tb5⟧

### s03 · explainer · Inspect load-test logs and HTTP responses
(mechanism) Use docker container logs NAME to inspect its captured standard output and error for initialization or execution failures. ⟦A.f13 A:tb6⟧
(mechanism) Send a JSON request body as encoded bytes in urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST"), then read the response through urlopen with a stated timeout. ⟦A.f14 A:tb6⟧
(mechanism) Serialize structured request/response values with json.dumps; decode JSON with json.loads before inspecting fields. ⟦A.f15 A:tb6⟧
(mechanism) Use np.mean(numeric_values) for the arithmetic mean of the selected numeric observations. ⟦A.f16 A:tb7⟧
(mechanism) Use np.std(numeric_values, ddof=0): divide squared deviations by N, then take the square root. Use ddof=1 only when the declared calculation requires N−1. ⟦A.f17 A:tb7⟧
(mechanism) Assert the declared valid, boundary and failure predicates. In ordinary non-optimized execution, a false assertion raises AssertionError. ⟦A.f18 A:tb7⟧

### s04 · explainer · Compare completed throughput with backlog
(example) Inspect the registered valid-traffic attempts alongside unfinished work. Keep HTTP errors, timeouts and other failures separate, but include all valid attempts in success and failed-fraction denominators. Calculate successful completions per measurement time, not arrivals per time. Percentiles describe completed-response samples with declared units and convention, not timed-out responses. Accept only stable-backlog points meeting all declared latency, error and throughput objectives, or report no feasible measured envelope. Intentional malformed fixtures stay outside this capacity population. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A.f9 A.f10 A.f14 A.f15 A:tb8⟧
(misconception) Arrivals are not completed work. A low latency for completed responses cannot hide timeouts, and a growing backlog is not a stable acceptable load point. ⟦A.f3 A.f6 A.f10 A:tb9⟧

### s05 · check · Check: Load-test a prediction endpoint against tail-latency and sustainable-throughput objectives
Check your decision — 

### s06 · hands_on · Practice: Load-test a prediction endpoint against tail-latency and sustainable-throughput objectives
Bounded fixture practice — 

### s07 · explainer · Choose inference batching under latency constraints
(intro) Batch waiting belongs in full request latency. Match each response to its request and setting first. ⟦B:tb1⟧
(mechanism) Serialize structured request/response values with json.dumps; decode JSON with json.loads before inspecting fields. ⟦B.f2 B:tb2⟧
(mechanism) Match each successful JSON response to its request identity and batching setting before computing its end-to-end duration from the trace. ⟦B.f3 B:tb2⟧
(mechanism) Use response-completion minus request-start time in one declared unit, including batch waiting time in the latency interpretation. ⟦B.f4 B:tb2⟧
(mechanism) Calculate the required tail percentile with np.percentile(latencies, declared_percentile), keeping the convention and successful-response sample count explicit. ⟦B.f5 B:tb3⟧
(mechanism) Choose only a batching limit meeting the stated latency objective, comparing the same trace/population interpretation. ⟦B.f6 B:tb3⟧
(mechanism) Use np.mean(numeric_values) for the arithmetic mean of the selected numeric observations. ⟦B.f7 B:tb3⟧
(mechanism) Use np.std(numeric_values, ddof=0): divide squared deviations by N, then take the square root. Use ddof=1 only when the declared calculation requires N−1. ⟦B.f8 B:tb4⟧
[DIAGRAM: End-to-end batching latency includes waiting] nodes=['Decode successful response; match request_id and batching_setting', 'request_start_seconds', 'batch_wait_end_seconds: waiting ends', 'response_complete_seconds: full duration ends', 'Matched successful population → declared percentile, mean and spread', 'Compare same population; choose only a limit meeting the objective'] edges=[('n0', 'n1', None), ('n1', 'n2', None), ('n2', 'n3', None), ('n3', 'n4', None), ('n4', 'n5', None)] alt: Decode successful response; match request_id and batching_setting → request_start_seconds → batch_wait_end_seconds: waiting ends → response_complete_seconds: full duration ends → Matched successful population → declared percentile, mean and spread → Compare same population; choose only a limit meeting the objective
[DIAGRAM: One matched request: full start-to-response interval] nodes=['order_1 / limit_2', 'Start: 1.0 seconds', 'Batch wait ends: 1.4 seconds', 'Response completes: 1.6 seconds'] edges=[('n0', 'n1', None), ('n1', 'n2', None), ('n2', 'n3', None)] alt: order_1 / limit_2 → Start: 1.0 seconds → Batch wait ends: 1.4 seconds → Response completes: 1.6 seconds
[TABLE ds.batching_trace cols=all ] caption: Authored trace: exclude failed and unmatched responses; the full start-to-response interval includes batch waiting.
[CODE python]
wait = batch_wait_end_seconds - request_start_seconds
post_wait = response_complete_seconds - batch_wait_end_seconds
end_to_end = response_complete_seconds - request_start_seconds
# Compute summaries over matched successful decoded responses only.
tail = np.percentile(latencies, declared_percentile)
mean = np.mean(latencies)
spread = np.std(latencies, ddof=0)
  annotations: []

### s08 · explainer · Match batching responses and full request latency
(example) For each registered trace row, decode the successful response and match its request identity and batching setting before calculating duration. Measure request start through response completion, including the waiting interval. Compute the declared percentile, mean and spread over matched successful responses, retaining units, convention and sample count. Compare settings using that same population interpretation and choose only a measured limit meeting the objective. A shorter execution interval cannot compensate for a full request interval that misses the latency limit. ⟦B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 B:tb5⟧

### s09 · explainer · Include batch waiting in latency
(misconception) Batch waiting belongs in the stated end-to-end latency. A faster execution interval alone does not make a batching limit acceptable under the full request objective. ⟦B.f4 B.f6 B:tb6⟧

### s10 · check · Check: Choose inference batching under latency constraints
Check your decision — 

### s11 · hands_on · Practice: Choose inference batching under latency constraints
Bounded fixture practice — 

### s12 · explainer · Configure bounded prediction-worker concurrency on an existing runtime
(intro) A worker limit in YAML is intent. Inspect whether running workers honor it during the bounded load. ⟦C:tb1⟧
(mechanism) A Compose YAML document declares services by name; use indented mappings for service fields and lists or mappings in the forms required by the Compose specification. ⟦C.f1 C:tb2⟧
(mechanism) Set a service’s image to its immutable artifact reference, its ports to HOST:CONTAINER mappings, and its environment to the declared nonsecret key/value settings. ⟦C.f2 C:tb2⟧
(mechanism) Use docker compose -f CONFIG_PATH config to parse, resolve and validate the authored YAML before applying it; check its resolved fields against the intended runtime contract. ⟦C.f3 C:tb2⟧
(mechanism) Apply the declared local Compose deployment with docker compose -f CONFIG_PATH up -d and inspect the resulting containers. ⟦C.f4 C:tb3⟧
(mechanism) Set the existing runtime’s worker-limit setting in the YAML, validate its parsed value and run the referenced image under that bound. ⟦C.f5 C:tb3⟧
(mechanism) Inspect running worker processes with docker container top NAME during the load fixture and compare the observed count with the configured limit to detect oversubscription. ⟦C.f6 C:tb3⟧
[SIDE_BY_SIDE] Safely reload and resolve the changed worker limit, then compare actual prediction workers with that bound and inspect same-interval CPU/memory. left_label: Configured worker bound | right_label: Observed processes under load
  left:
[CODE python]
# Approved changed configuration (intent, not process evidence)
config = {'services': {'prediction': {'image': 'fixture.local/orders@sha256:29371dd36fb111803c6fe996426f342680170dec59168e1e52139cdb4fbfaf83', 'environment': {'MODE': 'fixture', 'WORKER_LIMIT': '2'}, 'ports': ['8080:8080'], 'secrets': ['credential']}}, 'secrets': {'credential': {'environment': 'ORDER_FIXTURE_CREDENTIAL'}}}
  annotations: []
  right:
[TABLE ds.worker_processes cols=all ] caption: Authored process evidence: distinguish prediction workers from supervisor processes; align interval_id with resource observations.
[TABLE ds.worker_resources cols=all ] caption: Authored CPU/memory observations: align interval_id with the process evidence.
[CODE python]
import json, yaml
with open("runtime_contract.json") as source:
    runtime = json.load(source)
service = config["services"][runtime["SERVICE"]]
service["environment"][runtime["worker_limit_key"]] = str(runtime["approved_worker_limit"])
with open(runtime["CONFIG_PATH"], "w") as target:
    yaml.safe_dump(config, target)
with open(runtime["CONFIG_PATH"]) as source:
    reloaded = yaml.safe_load(source)
assert int(reloaded["services"][runtime["SERVICE"]]["environment"][runtime["worker_limit_key"]]) == runtime["approved_worker_limit"]
# Resolve with compose config; apply and compare observed workers with this bound.
  annotations: []

### s13 · explainer · Reload worker bounds and inspect resources
(mechanism) Inspect concurrent CPU/memory usage during the same fixture to support the bound check rather than assuming the configuration was honored. ⟦C.f7 C:tb4⟧
(mechanism) With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading supports standard YAML tags, not arbitrary Python object constructors. ⟦C.f8 C:tb4⟧
(example) Edit the existing worker bound, safely reload it and inspect the Compose-resolved value before applying the referenced image. During the authorized load interval, inspect prediction-worker processes and compare their count with the configured limit. Record CPU and memory in that same interval. A parsed bound is intent; excess observed workers are oversubscription even when configuration validation succeeds. Keep authored settings, reloaded settings and actual process evidence distinct. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C.f7 C.f8 C:tb5⟧
(misconception) Configuration is intent, not proof of the running process count. Worker-count evidence and concurrent resource measurements must refer to the same bounded fixture. ⟦C.f5 C.f6 C.f7 C:tb6⟧

### s14 · check · Check: Configure bounded prediction-worker concurrency on an existing runtime
Check your decision — 

### s15 · hands_on · Practice: Configure bounded prediction-worker concurrency on an existing runtime
Bounded fixture practice — 

### s16 · explainer · Configure replica scaling to right-size serving capacity under a service objective
(intro) More replicas are not automatically better. Compare client outcomes at equal load under explicit capacity bounds. ⟦D:tb1⟧
(mechanism) For a fixed Compose scaling fixture, declare deploy.replicas or use docker compose up -d --scale SERVICE=COUNT, then inspect the actual replica count. ⟦D.f1 D:tb2⟧
(mechanism) For SageMaker Application Auto Scaling, register the supplied endpoint variant as a scalable target with explicit MinCapacity and MaxCapacity bounds. ⟦D.f2 D:tb2⟧
(mechanism) A target-tracking scaling policy specifies a metric, target value and scale-in/scale-out cooldowns; apply only the supported supplied policy to the existing scalable target. ⟦D.f3 D:tb2⟧
(mechanism) Compare scale settings at the same declared load and select capacity that meets observed success, p99 latency and throughput requirements not merely more replicas. ⟦D.f4 D:tb3⟧
(mechanism) Estimate client-visible success probability as successful eligible attempts divided by all eligible attempts in the defined measurement window, counting failed attempts in the denominator. ⟦D.f5 D:tb3⟧
(mechanism) Compute the declared tail-latency percentile with np.percentile(completed_latency_values, declared_percentile), retaining its convention, sample count and time unit. ⟦D.f6 D:tb3⟧
[BEFORE_AFTER] Intended replica settings and observed capacity are different evidence. Increase capacity only within supplied bounds and service objectives.
  before:
[DIAGRAM: Before bounded scaling] nodes=['Original replica and lifecycle settings', 'Record container count and identities', 'Inspect authorized instance status and identity'] edges=[('n0', 'n1', None), ('n1', 'n2', None)] alt: Original replica and lifecycle settings → Record container count and identities → Inspect authorized instance status and identity
  after:
[DIAGRAM: After bounded scaling and restoration] nodes=['Parsed bounded replica policy applied', 'Inspect count, identities and lifecycle state after bounded demand/action', 'Compare same-load success, tail latency and throughput', 'Restore original replica and lifecycle settings'] edges=[('n0', 'n1', None), ('n1', 'n2', None), ('n2', 'n3', None)] alt: Parsed bounded replica policy applied → Inspect count, identities and lifecycle state after bounded demand/action → Compare same-load success, tail latency and throughput → Restore original replica and lifecycle settings
[TABLE ds.replica_states cols=all ] caption: Authored original, changed and restored phases: compare intended replicas, actual container identities and instance state.

### s17 · explainer · Verify replica policy and completed throughput
(mechanism) Measure successful throughput as completed successful requests divided by elapsed measurement time, and compare it with the offered load rather than equating arrivals with completed work. ⟦D.f7 D:tb4⟧
(mechanism) Edit the existing runtime’s YAML replica policy from the demand/capacity evidence, then parse and inspect the resolved replica bounds before applying it. ⟦D.f8 D:tb4⟧
(mechanism) Inspect running containers before and after the bounded demand change and compare the observed count and identities with the intended replica policy. ⟦D.f9 D:tb4⟧
(mechanism) Restore the nonproduction runtime’s original replica and lifecycle settings after the bounded scaling check. ⟦D.f10 D:tb5⟧
(mechanism) Use np.mean(numeric_values) for the arithmetic mean of the selected numeric observations. ⟦D.f11 D:tb5⟧
(mechanism) Use np.std(numeric_values, ddof=0): divide squared deviations by N, then take the square root. Use ddof=1 only when the declared calculation requires N−1. ⟦D.f12 D:tb5⟧

### s18 · explainer · Compare intended replicas with runtime evidence
(mechanism) Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect the instance status and identity before and after the authorized lifecycle action. ⟦D.f13 D:tb6⟧
(mechanism) With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading supports standard YAML tags, not arbitrary Python object constructors. ⟦D.f14 D:tb6⟧
(example) For the fixed fixture, declare the permitted replica count and compare intended versus observed container identities before and after the bounded demand change. A supplied SageMaker target instead retains explicit capacity bounds, metric target and cooldowns. Compare success, tail latency and successful throughput at the same load and sample conventions. Safely inspect the changed YAML before application; inspect runtime identity and lifecycle state afterward. Restore the original nonproduction replica and lifecycle settings. ⟦D.f1 D.f2 D.f3 D.f4 D.f5 D.f6 D.f7 D.f8 D.f9 D.f10 D.f13 D.f14 D:tb7⟧
(example) More replicas alone do not establish an acceptable setting. ⟦D.f1 D.f2 D.f3 D.f4 D.f5 D.f6 D.f7 D.f8 D.f9 D.f10 D.f13 D.f14 D:tb7⟧
(misconception) More replicas are not guaranteed to satisfy the task. Intended and observed counts differ in kind, and completed throughput must not be replaced with offered load. ⟦D.f1 D.f4 D.f7 D.f9 D:tb8⟧

### s19 · check · Check: Configure replica scaling to right-size serving capacity under a service objective
Check your decision — 

### s20 · hands_on · Practice: Configure replica scaling to right-size serving capacity under a service objective
Bounded fixture practice — 

### s21 · recap · Carry these rules forward
(takeaway) Arrivals are not completions; timeouts and growing backlog cannot be hidden by low completed-response latency. ⟦A.f3 A.f6 A.f10 A:tb9⟧
(takeaway) Include batch waiting in full request latency; fast execution alone does not meet the objective. ⟦B.f4 B.f6 B:tb6⟧
(takeaway) Configuration is intent. Compare observed workers and same-interval resource evidence with the declared bound. ⟦C.f5 C.f6 C.f7 C:tb6⟧
(takeaway) More replicas are not guaranteed to pass; distinguish intended counts, observed counts and completed throughput. ⟦D.f1 D.f4 D.f7 D.f9 D:tb8⟧
[UP NEXT] Roll back a serving release to a previous approved registry artifact: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try again: Load-test a prediction endpoint against tail-latency and sustainable-throughput objectives — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) Exercise the endpoint with the declared arrival/concurrency profile and bounded duration, and record client-visible outcomes and response times rather than only attempted request count. ⟦A.f1 A:tb2⟧
(mechanism) Run valid and malformed HTTP JSON fixtures with assertions, keeping intentional malformed tests outside the valid-traffic capacity measurement. ⟦A.f7 A:tb4⟧
(mechanism) At every fixed offered load, use the stated valid payload mix, warm-up and fixed measurement duration, counting successful completions, HTTP errors, timeouts and other failed attempts separately. ⟦A.f8 A:tb4⟧
(misconception) Arrivals are not completed work. A low latency for completed responses cannot hide timeouts, and a growing backlog is not a stable acceptable load point. ⟦A.f3 A.f6 A.f10 A:tb9⟧
### r02 · Try again: Load-test a prediction endpoint against tail-latency and sustainable-throughput objectives — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) Exercise the endpoint with the declared arrival/concurrency profile and bounded duration, and record client-visible outcomes and response times rather than only attempted request count. ⟦A.f1 A:tb2⟧
(mechanism) Inspect backlog growth and unfinished work throughout the window; accept only stable-backlog loads meeting the predeclared tail-latency and error limits, and report the highest measured successful throughput or no feasible measured envelope. ⟦A.f10 A:tb5⟧
(mechanism) Treat a load point as acceptable only if it meets the predeclared client-visible success and tail-latency requirements, as well as the required completed throughput. ⟦A.f2 A:tb2⟧
(mechanism) Retain failures and timeouts separately so latency measured only for completed responses is not misrepresented as the experience of every attempted request. ⟦A.f3 A:tb2⟧
(mechanism) Estimate client-visible success probability as successful eligible attempts divided by all eligible attempts in the defined measurement window, counting failed attempts in the denominator. ⟦A.f4 A:tb3⟧
(mechanism) Compute the declared tail-latency percentile with np.percentile(completed_latency_values, declared_percentile), retaining its convention, sample count and time unit. ⟦A.f5 A:tb3⟧
(mechanism) Measure successful throughput as completed successful requests divided by elapsed measurement time, and compare it with the offered load rather than equating arrivals with completed work. ⟦A.f6 A:tb3⟧
(mechanism) At every fixed offered load, use the stated valid payload mix, warm-up and fixed measurement duration, counting successful completions, HTTP errors, timeouts and other failed attempts separately. ⟦A.f8 A:tb4⟧
(mechanism) Compute failed-request fraction from all failed attempts divided by all valid-traffic attempts; timeouts remain failures. ⟦A.f9 A:tb4⟧
(misconception) Arrivals are not completed work. A low latency for completed responses cannot hide timeouts, and a growing backlog is not a stable acceptable load point. ⟦A.f3 A.f6 A.f10 A:tb9⟧
### r03 · Try again: Choose inference batching under latency constraints — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) Match each successful JSON response to its request identity and batching setting before computing its end-to-end duration from the trace. ⟦B.f3 B:tb2⟧
(mechanism) Use response-completion minus request-start time in one declared unit, including batch waiting time in the latency interpretation. ⟦B.f4 B:tb2⟧
(mechanism) Calculate the required tail percentile with np.percentile(latencies, declared_percentile), keeping the convention and successful-response sample count explicit. ⟦B.f5 B:tb3⟧
(mechanism) Choose only a batching limit meeting the stated latency objective, comparing the same trace/population interpretation. ⟦B.f6 B:tb3⟧
(misconception) Batch waiting belongs in the stated end-to-end latency. A faster execution interval alone does not make a batching limit acceptable under the full request objective. ⟦B.f4 B.f6 B:tb6⟧
### r04 · Try again: Configure bounded prediction-worker concurrency on an existing runtime — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) Apply the declared local Compose deployment with docker compose -f CONFIG_PATH up -d and inspect the resulting containers. ⟦C.f4 C:tb3⟧
(mechanism) Set the existing runtime’s worker-limit setting in the YAML, validate its parsed value and run the referenced image under that bound. ⟦C.f5 C:tb3⟧
(misconception) Configuration is intent, not proof of the running process count. Worker-count evidence and concurrent resource measurements must refer to the same bounded fixture. ⟦C.f5 C.f6 C.f7 C:tb6⟧
### r05 · Try again: Configure bounded prediction-worker concurrency on an existing runtime — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) A Compose YAML document declares services by name; use indented mappings for service fields and lists or mappings in the forms required by the Compose specification. ⟦C.f1 C:tb2⟧
(mechanism) Set a service’s image to its immutable artifact reference, its ports to HOST:CONTAINER mappings, and its environment to the declared nonsecret key/value settings. ⟦C.f2 C:tb2⟧
(mechanism) Use docker compose -f CONFIG_PATH config to parse, resolve and validate the authored YAML before applying it; check its resolved fields against the intended runtime contract. ⟦C.f3 C:tb2⟧
(mechanism) Set the existing runtime’s worker-limit setting in the YAML, validate its parsed value and run the referenced image under that bound. ⟦C.f5 C:tb3⟧
(mechanism) Inspect running worker processes with docker container top NAME during the load fixture and compare the observed count with the configured limit to detect oversubscription. ⟦C.f6 C:tb3⟧
(mechanism) Inspect concurrent CPU/memory usage during the same fixture to support the bound check rather than assuming the configuration was honored. ⟦C.f7 C:tb4⟧
(mechanism) With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading supports standard YAML tags, not arbitrary Python object constructors. ⟦C.f8 C:tb4⟧
(misconception) Configuration is intent, not proof of the running process count. Worker-count evidence and concurrent resource measurements must refer to the same bounded fixture. ⟦C.f5 C.f6 C.f7 C:tb6⟧
### r06 · Try again: Configure replica scaling to right-size serving capacity under a service objective — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) Restore the nonproduction runtime’s original replica and lifecycle settings after the bounded scaling check. ⟦D.f10 D:tb5⟧
(mechanism) Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect the instance status and identity before and after the authorized lifecycle action. ⟦D.f13 D:tb6⟧
(mechanism) Inspect running containers before and after the bounded demand change and compare the observed count and identities with the intended replica policy. ⟦D.f9 D:tb4⟧
(misconception) More replicas are not guaranteed to satisfy the task. Intended and observed counts differ in kind, and completed throughput must not be replaced with offered load. ⟦D.f1 D.f4 D.f7 D.f9 D:tb8⟧
### r07 · Try again: Configure replica scaling to right-size serving capacity under a service objective — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) For a fixed Compose scaling fixture, declare deploy.replicas or use docker compose up -d --scale SERVICE=COUNT, then inspect the actual replica count. ⟦D.f1 D:tb2⟧
(mechanism) Restore the nonproduction runtime’s original replica and lifecycle settings after the bounded scaling check. ⟦D.f10 D:tb5⟧
(mechanism) Use np.mean(numeric_values) for the arithmetic mean of the selected numeric observations. ⟦D.f11 D:tb5⟧
(mechanism) Use np.std(numeric_values, ddof=0): divide squared deviations by N, then take the square root. Use ddof=1 only when the declared calculation requires N−1. ⟦D.f12 D:tb5⟧
(mechanism) Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect the instance status and identity before and after the authorized lifecycle action. ⟦D.f13 D:tb6⟧
(mechanism) With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading supports standard YAML tags, not arbitrary Python object constructors. ⟦D.f14 D:tb6⟧
(mechanism) For SageMaker Application Auto Scaling, register the supplied endpoint variant as a scalable target with explicit MinCapacity and MaxCapacity bounds. ⟦D.f2 D:tb2⟧
(mechanism) A target-tracking scaling policy specifies a metric, target value and scale-in/scale-out cooldowns; apply only the supported supplied policy to the existing scalable target. ⟦D.f3 D:tb2⟧
(mechanism) Compare scale settings at the same declared load and select capacity that meets observed success, p99 latency and throughput requirements not merely more replicas. ⟦D.f4 D:tb3⟧
(mechanism) Estimate client-visible success probability as successful eligible attempts divided by all eligible attempts in the defined measurement window, counting failed attempts in the denominator. ⟦D.f5 D:tb3⟧
(mechanism) Compute the declared tail-latency percentile with np.percentile(completed_latency_values, declared_percentile), retaining its convention, sample count and time unit. ⟦D.f6 D:tb3⟧
(mechanism) Measure successful throughput as completed successful requests divided by elapsed measurement time, and compare it with the offered load rather than equating arrivals with completed work. ⟦D.f7 D:tb4⟧
(mechanism) Edit the existing runtime’s YAML replica policy from the demand/capacity evidence, then parse and inspect the resolved replica bounds before applying it. ⟦D.f8 D:tb4⟧
(mechanism) Inspect running containers before and after the bounded demand change and compare the observed count and identities with the intended replica policy. ⟦D.f9 D:tb4⟧
(misconception) More replicas are not guaranteed to satisfy the task. Intended and observed counts differ in kind, and completed throughput must not be replaced with offered load. ⟦D.f1 D.f4 D.f7 D.f9 D:tb8⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: One distinction to restore
· remediation_steps.eyebrow: One distinction to restore
· remediation_steps.eyebrow: One distinction to restore
· remediation_steps.eyebrow: One distinction to restore
· remediation_steps.eyebrow: One distinction to restore
· remediation_steps.eyebrow: One distinction to restore
· remediation_steps.eyebrow: One distinction to restore

=========

# EVALUATOR PACKET — Restore an approved serving release (mle.tile.072_072)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.model_release_rollback — Roll back a serving release to a previous approved registry artifact

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (mle.model_release_rollback)   objective: Restore the previous approved serving artifact and retire the faulty release only after verification.
A.f1: Resolve the previously approved registry version and its artifact as the rollback target, preserving the approval/version identity rather than selecting an unapproved latest version.   [sources: mlflow_docs#ml/model-registry/workflow/ — Registering a Model; Fetching an MLflow Model from the Model Registry; Deploy and Organize Models]
A.f2: Use the recorded previous immutable image reference for the approved replacement container.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/image/pull/ — Pull an image by digest (immutable identifier)]
A.f3: Verify readiness and a bounded prediction fixture after the rollback, and confirm the response contract still matches the service.   [sources: python_tutorial#../library/urllib.request.html — Request; urlopen]
A.f4: Do not embed secrets in Dockerfile ARG or ENV instructions, because they persist in the final image or its metadata.   [sources: docker_docs#https://docs.docker.com/reference/build-checks/secrets-used-in-arg-or-env/ — Description]
A.f5: Supply sensitive values through the runtime secret mechanism rather than placing their literal values in the Compose configuration.   [sources: docker_docs#https://docs.docker.com/reference/compose-file/secrets/ — secrets]
A.f6: Start the approved replacement under its distinct container identity with the required environment and published port; do not retire the faulty test release before the replacement is ready.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/run/ — Publish or expose port; Set environment variables; Specify a container name]
A.f7: After replacement readiness and a verified JSON prediction/version response, stop and remove only the faulty test release, preserving the approved replacement.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/stop/ — Description]
A.f8: Send a JSON request body as encoded bytes in urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST"), then read the response through urlopen with a stated timeout.   [sources: python_tutorial#../library/urllib.request.html — Request; urlopen]
A.f9: Use json.dumps to encode structured request/response values and json.loads to decode JSON before checking their fields.   [sources: python_tutorial#inputoutput.html — Saving structured data with json]
A.f10: Inspect the running container identity and State, including Health when a healthcheck is configured, and compare them with the intended release.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/inspect/ — Description; Examples]
A.f11: Inspect runtime logs for initialization and execution failures without copying sensitive request data or credentials into the evidence record.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/logs/ — Description]
A.f12: Call the declared readiness and prediction endpoints with bounded timeouts and check the returned status and payload against the expected contracts.   [sources: python_tutorial#../library/urllib.request.html — Request; urlopen]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Roll Back a Model Release.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.model_version_registration, mle.deployment_verification. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Restore approved version A using its recorded immutable image reference on the supplied authorized runtime while faulty test version B remains running. Use runtime-injected credentials, the required environment and a distinct published HTTP port. Inspect A's container identity, State, available Health and logs; verify readiness and the bounded JSON prediction/version fixture before stopping and removing only B. Do not retrain or change model identity.  SUCCESS: Version A matches the recorded approved registry version and immutable image reference, remains running, and passes the declared readiness and prediction contracts within bounded timeouts. The decoded prediction response confirms A and the expected fixture prediction. Only B is stopped and removed, after verification. Release configuration and recorded evidence contain no credential literals or sensitive request data.
ASSESSMENT ANCHOR: resolve_approved_rollback_artifact facts=['f1', 'f2']
ASSESSMENT ANCHOR: preserve_runtime_secret_boundary facts=['f4', 'f5']
ASSESSMENT ANCHOR: start_and_inspect_approved_replacement facts=['f6', 'f10', 'f11']
ASSESSMENT ANCHOR: verify_restored_serving_version_and_prediction facts=['f3', 'f8', 'f9', 'f12']
ASSESSMENT ANCHOR: retire_faulty_test_release_after_verification facts=['f6', 'f7']

## DATA ASSETS USED
ds.release_records: Approval and immutable fixture artifact records — columns: version(categorical), approved(categorical), image_reference(identifier), container_name(identifier), host_port(categorical,digits-as-label), release_role(categorical)
   ["A",true,"fixture.local/orders@sha256:29371dd36fb111803c6fe996426f342680170dec59168e1e52139cdb4fbfaf83","prediction-A",8081,"approved_previous"]
   ["B",false,"fixture.local/orders@sha256:cb8f33490a33bce2025fd396588bde12c4f8822336c379bcc96449329c5762ce","prediction-B",8082,"faulty_test"]
ds.release_transition: Rollback ordering fixture — columns: sequence(numerical), event(categorical), A_running(categorical), A_verified(categorical), B_running(categorical), B_removed(categorical)
   [0,"initial",false,false,true,false]
   [1,"start_A",true,false,true,false]
   [2,"verify_A",true,true,true,false]
   [3,"stop_B",true,true,false,false]
   [4,"remove_B",true,true,false,true]
   variant variant.retire_before_verify: 2 ops; planted: issue.retire_before_verify(other)

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute training and inference expenditure to workloads; Audit dataset, code, run and artifact lineage of a deployed model; Block release promotion when model acceptance gates fail; Choose scheduled, new-data or investigated quality/drift retraining triggers; Configure actionable model and service alerts; Define artifact dependencies between ML pipeline stages; Detect model-input data drift against a defined reference distribution; Distinguish data drift, concept drift and observed quality degradation; Gate a retrained candidate against the incumbent using validation evidence before controlled promotion; Gate pipeline execution on dataset-quality tests; Invoke retraining with a versioned input snapshot from an authorized trigger; Measure production model quality when labels arrive; Monitor production input and prediction distributions; Prevent duplicate or overlapping retraining runs; Promote an approved registry version through accountable staged ML release gates; Recover a failed ML pipeline run without bypassing quality gates; Remove model-serving resources safely on an existing platform; Set an ML workload cost guardrail on an existing platform; Test preprocessing and model i

## LESSON, in learner order

### s01 · explainer · Roll back a serving release to a previous approved registry artifact
(intro) Resolve the approved previous artifact. Verify its replacement service before retiring the faulty test release. ⟦A:tb1⟧
(mechanism) Resolve the previously approved registry version and its artifact as the rollback target, preserving the approval/version identity rather than selecting an unapproved latest version. ⟦A.f1 A:tb2⟧
(mechanism) Use the recorded previous immutable image reference for the approved replacement container. ⟦A.f2 A:tb2⟧
(mechanism) Verify readiness and a bounded prediction fixture after the rollback, and confirm the response contract still matches the service. ⟦A.f3 A:tb2⟧
(mechanism) Keep secrets out of Dockerfile ARG and ENV: they persist in the final image or its metadata. ⟦A.f4 A:tb3⟧
(mechanism) Deliver sensitive values through runtime secrets, never as literal Compose values. ⟦A.f5 A:tb3⟧
(mechanism) Start the approved replacement under its distinct container identity with the required environment and published port; do not retire the faulty test release before the replacement is ready. ⟦A.f6 A:tb3⟧
[BEFORE_AFTER] Start the approved replacement under its distinct identity; inspect State, available Health and sanitized logs, then verify readiness and decoded prediction/version before stopping and removing only the faulty test release.
  before:
[TABLE ds.release_records cols=all ] caption: Authored approval records identify the previous immutable replacement; the faulty test release is still running.
  after:
[TABLE ds.release_transition cols=all ] caption: Authored chronology, not live command evidence: replacement is verified before faulty-release retirement.
[CODE python]
import json
with open("runtime_contract.json") as source:
    intended = json.load(source)
# Inspect live fixture execution separately from the intended configuration.
# Compare container Config.Image with intended["IMAGE_DIGEST"].
# Check State and Health when configured, plus sanitized initialization/execution logs.
# Bounded readiness and prediction checks must verify status and decoded payload.
# Do not interpret launch success as acceptance.
  annotations: []

### s02 · explainer · Verify replacement endpoints before retiring the faulty release
(mechanism) After replacement readiness and a verified JSON prediction/version response, stop and remove only the faulty test release, preserving the approved replacement. ⟦A.f7 A:tb4⟧
(mechanism) Send a JSON request body as encoded bytes in urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST"), then read the response through urlopen with a stated timeout. ⟦A.f8 A:tb4⟧
(mechanism) Serialize structured request/response values with json.dumps; decode JSON with json.loads before inspecting fields. ⟦A.f9 A:tb4⟧
(mechanism) Inspect the running container identity and State, including Health when a healthcheck is configured, and compare them with the intended release. ⟦A.f10 A:tb5⟧
(mechanism) Inspect runtime logs for initialization and execution failures without copying sensitive request data or credentials into the evidence record. ⟦A.f11 A:tb5⟧
(mechanism) Call the declared readiness and prediction endpoints with bounded timeouts and check the returned status and payload against the expected contracts. ⟦A.f12 A:tb5⟧

### s03 · explainer · Trace the approved rollback replacement
(example) Keep the faulty test release running while starting the approved previous release under its distinct identity and published port. Resolve the recorded immutable artifact rather than latest. Inspect replacement State, available Health and sanitized logs. With bounded calls, verify readiness and decoded JSON prediction/version against the contract. Only then stop and remove the faulty test release, preserving the replacement. Keep credentials runtime-injected, not in image metadata, Compose values or evidence. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A.f9 A.f10 A.f11 A.f12 A:tb6⟧
(misconception) Rollback is not ‘use latest’ or remove everything old. The target must retain its approval/version identity, and the faulty test release is not retired before replacement readiness. ⟦A.f1 A.f2 A.f6 A.f7 A:tb7⟧

### s04 · check · Check: Roll back a serving release to a previous approved registry artifact
Check your decision — 

### s05 · check · Check: Roll back a serving release to a previous approved registry artifact
Check your decision — 

### s06 · hands_on · Practice: Roll back a serving release to a previous approved registry artifact
Bounded fixture practice — 

### s07 · recap · Carry these rules forward
(takeaway) Rollback preserves approved immutable identity. Verify the replacement before retiring only the faulty test release. ⟦A.f1 A.f2 A.f6 A.f7 A:tb7⟧
[UP NEXT] Gate pipeline execution on dataset-quality tests: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try again: Roll back a serving release to a previous approved registry artifact — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) Resolve the previously approved registry version and its artifact as the rollback target, preserving the approval/version identity rather than selecting an unapproved latest version. ⟦A.f1 A:tb2⟧
(mechanism) Use the recorded previous immutable image reference for the approved replacement container. ⟦A.f2 A:tb2⟧
(misconception) Rollback is not ‘use latest’ or remove everything old. The target must retain its approval/version identity, and the faulty test release is not retired before replacement readiness. ⟦A.f1 A.f2 A.f6 A.f7 A:tb7⟧
### r02 · Try again: Roll back a serving release to a previous approved registry artifact — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) Keep secrets out of Dockerfile ARG and ENV: they persist in the final image or its metadata. ⟦A.f4 A:tb3⟧
(mechanism) Deliver sensitive values through runtime secrets, never as literal Compose values. ⟦A.f5 A:tb3⟧
(misconception) Rollback is not ‘use latest’ or remove everything old. The target must retain its approval/version identity, and the faulty test release is not retired before replacement readiness. ⟦A.f1 A.f2 A.f6 A.f7 A:tb7⟧
### r03 · Try again: Roll back a serving release to a previous approved registry artifact — Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.
(mechanism) Inspect the running container identity and State, including Health when a healthcheck is configured, and compare them with the intended release. ⟦A.f10 A:tb5⟧
(mechanism) Inspect runtime logs for initialization and execution failures without copying sensitive request data or credentials into the evidence record. ⟦A.f11 A:tb5⟧
(mechanism) Call the declared readiness and prediction endpoints with bounded timeouts and check the returned status and payload against the expected contracts. ⟦A.f12 A:tb5⟧
(mechanism) Verify readiness and a bounded prediction fixture after the rollback, and confirm the response contract still matches the service. ⟦A.f3 A:tb2⟧
(mechanism) Start the approved replacement under its distinct container identity with the required environment and published port; do not retire the faulty test release before the replacement is ready. ⟦A.f6 A:tb3⟧
(mechanism) After replacement readiness and a verified JSON prediction/version response, stop and remove only the faulty test release, preserving the approved replacement. ⟦A.f7 A:tb4⟧
(mechanism) Send a JSON request body as encoded bytes in urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST"), then read the response through urlopen with a stated timeout. ⟦A.f8 A:tb4⟧
(mechanism) Serialize structured request/response values with json.dumps; decode JSON with json.loads before inspecting fields. ⟦A.f9 A:tb4⟧
(misconception) Rollback is not ‘use latest’ or remove everything old. The target must retain its approval/version identity, and the faulty test release is not retired before replacement readiness. ⟦A.f1 A.f2 A.f6 A.f7 A:tb7⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: One distinction to restore
· remediation_steps.eyebrow: One distinction to restore
· remediation_steps.eyebrow: One distinction to restore