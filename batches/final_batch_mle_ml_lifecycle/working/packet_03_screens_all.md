# EVALUATOR PACKET — Fail-Closed Data, Behavior and Release Gates (mle.tile.073_075)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.dataset_quality_gate — Gate pipeline execution on dataset-quality tests
B = mle.model_behavior_tests — Test preprocessing and model inference behavior
C = mle.model_release_quality_gate — Block release promotion when model acceptance gates fail

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (mle.dataset_quality_gate)   objective: Wire a fail-closed data-quality function into an existing commit-triggered pipeline.
A.f1: Run data validation before model training; unexpected features, missing features or invalid feature values should prevent the affected pipeline execution from continuing.   [sources: google_mlops_pipelines#Data and model validation]
A.f2: Represent each required schema/quality check as a named result and aggregate them into an explicit pass/fail decision under the supplied gate policy.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
A.f3: On a failed required test, raise or return the declared failure result and do not invoke the downstream training stage.   [sources: python_tutorial#errors.html — Handling Exceptions; Raising Exceptions]
A.f4: Retain the tested input snapshot and failed check evidence so a repaired dataset can be validated against the same requirements.   [sources: google_mlops_pipelines#Data and model validation]
A.f5: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
A.f6: In an existing Cloud Build YAML/JSON configuration, each steps item declares its execution image in name and its command in args or script; wire the function/test entry point into the assigned stage.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/build-config-file-schema — Build steps; name; args; script; serviceAccount; allowFailure; allowExitCodes]
A.f7: Assign step IDs and set waitFor to the required preceding step IDs; downstream execution depends on those steps completing successfully, not just their textual location.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/configuring-builds/configure-build-step-order — id; waitFor]
A.f8: Keep required gate failures fatal: do not set allowFailure or add failing gate exit codes to allowExitCodes, and ensure a rejected Python gate exits unsuccessfully.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/build-config-file-schema — Build steps; name; args; script; serviceAccount; allowFailure; allowExitCodes]
A.f9: Use the configured repository commit trigger and branch filter to run the existing pipeline, then inspect actual stage results and resolved inputs for accepted and rejected fixtures.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/automating-builds/create-manage-triggers — Creating a build trigger; Manually running triggers]
A.f10: With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading accepts standard YAML tags, not arbitrary Python object constructors.   [sources: python_tutorial#https://pyyaml.org/wiki/PyYAMLDocumentation — Reference: safe_load; safe_dump]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Gate Data and Model Releases.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.dataset_schema_validation, mle.label_integrity, mle.dataset_cleaning_policy. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Implement a learner-defined Python dataset-gate function and write its required imports in the supplied pipeline's test stage. Author named contract checks and assertions for valid, boundary and invalid fixtures, including a fixture missing a required feature. Preserve tested snapshot identities and failure evidence. Write and reload the existing Cloud Build configuration with PyYAML, inspect its resolved fields, and wire fatal gate execution and explicit training dependencies. Use the configured repository commit trigger and branch filter to run accepted and rejected fixtures.  SUCCESS: The declared valid and acceptable boundary fixtures pass; invalid fixtures produce named failure evidence and an unsuccessful gate-process exit. Reloaded configuration retains the required image, command, step IDs and waitFor dependencies without permitting required gate failures. Actual triggered-run results show training starts only after an accepted quality stage and never starts after a rejected quality stage. Tested snapshots and failed checks remain available for validation of a repaired dataset against the same contract.
ASSESSMENT ANCHOR: demonstrate_dataset_contract_acceptance_and_rejection facts=['f1', 'f2', 'f3', 'f5']
ASSESSMENT ANCHOR: enforce_fatal_quality_stage_before_training facts=['f6', 'f7', 'f8']
ASSESSMENT ANCHOR: verify_triggered_run_outcomes_and_preserve_failure_evidence facts=['f4', 'f9']
ASSESSMENT ANCHOR: inspect_round_tripped_gate_configuration facts=['f6', 'f7', 'f8', 'f10']

## SOURCE FACTS — B (mle.model_behavior_tests)   objective: Connect behavior assertions to a pipeline gate that blocks dependent stages on failure.
B.f1: Behavior tests must exercise the packaged fitted preprocessing and model through the same prediction path used for inference.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.1 Inconsistent preprocessing]
B.f2: For each supplied fixture, check its expected output row count, feature/target alignment and output shape before comparing values.   [sources: numpy_user_guide#user/absolute_beginners.html — Attributes of an array; How to create a basic array]
B.f3: Compare numerical output to the expected fixture with np.testing.assert_allclose using explicitly declared tolerances.   [sources: numpy_user_guide#reference/generated/numpy.testing.assert_allclose.html]
B.f4: Exercise malformed input and boundary fixtures, checking explicit rejection when the contract does not permit them.   [sources: python_tutorial#errors.html — Handling Exceptions; Raising Exceptions]
B.f5: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
B.f6: In an existing Cloud Build YAML/JSON configuration, each steps item declares its execution image in name and its command in args or script; wire the function/test entry point into the assigned stage.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/build-config-file-schema — Build steps; name; args; script; serviceAccount; allowFailure; allowExitCodes]
B.f7: Assign step IDs and set waitFor to the required preceding step IDs; downstream execution depends on those steps completing successfully, not just their textual location.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/configuring-builds/configure-build-step-order — id; waitFor]
B.f8: Keep required gate failures fatal: do not set allowFailure or add failing gate exit codes to allowExitCodes, and ensure a rejected Python gate exits unsuccessfully.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/build-config-file-schema — Build steps; name; args; script; serviceAccount; allowFailure; allowExitCodes]
B.f9: Use the configured repository commit trigger and branch filter to run the existing pipeline, then inspect actual stage results and resolved inputs for accepted and rejected fixtures.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/automating-builds/create-manage-triggers — Creating a build trigger; Manually running triggers]
B.f10: With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading accepts standard YAML tags, not arbitrary Python object constructors.   [sources: python_tutorial#https://pyyaml.org/wiki/PyYAMLDocumentation — Reference: safe_load; safe_dump]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Gate Data and Model Releases.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.online_prediction_contract, mle.preprocessing_pipeline. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a learner-defined Python test function, with learner-written imports, that uses reusable valid, boundary and malformed fixtures to exercise the supplied packaged prediction function. Assert row count, feature/target correspondence and output shape before numerical comparisons with explicit tolerances, and test the declared exception path. Safely write and reload the supplied Cloud Build configuration, connect the test entry point to its assigned stage, and verify accepted and deliberately regressed runs through the configured repository commit trigger and branch filter.  SUCCESS: The accepted fixtures pass all structural and numerical checks, and contract-prohibited inputs produce the declared exception. The reloaded configuration has the required execution image, command, step IDs and waitFor dependencies without failure allowances. A deliberate behavior regression produces an unsuccessful test-stage exit in an actual triggered run, and dependent later stages do not execute.
ASSESSMENT ANCHOR: detect_packaged_prediction_structure_regressions facts=['f1', 'f2']
ASSESSMENT ANCHOR: detect_numerical_regressions_with_explicit_tolerances facts=['f3']
ASSESSMENT ANCHOR: assert_valid_boundary_and_failure_behavior facts=['f4', 'f5']
ASSESSMENT ANCHOR: verify_behavior_test_failures_stop_dependent_stages facts=['f6', 'f7', 'f8', 'f9']
ASSESSMENT ANCHOR: safely_round_trip_and_inspect_test_stage_configuration facts=['f10']

## SOURCE FACTS — C (mle.model_release_quality_gate)   objective: Implement a fail-closed, event-triggered candidate release gate from fixed validation and operating evidence.
C.f1: A release gate compares the candidate with the accepted reference and the predeclared quality requirements before promotion.   [sources: google_mlops_pipelines#Data and model validation]
C.f2: Read the supplied candidate evidence fields, evaluate each required acceptance predicate and report which predicate failed when the verdict is reject.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
C.f3: Calculate validation expected error cost using the predeclared deployment probabilities and error costs, and include the fixed latency/operating limits in eligibility.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
C.f4: A failed or incomplete required gate blocks promotion rather than being treated as success.   [sources: python_tutorial#errors.html — Handling Exceptions; Raising Exceptions]
C.f5: For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
C.f6: With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
C.f7: Do not use protected test observations to fit preprocessing, choose a model or tune its settings; doing so leaks information into the chosen system.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
C.f8: In an existing Cloud Build YAML/JSON configuration, each steps item declares its execution image in name and its command in args or script; wire the function/test entry point into the assigned stage.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/build-config-file-schema — Build steps; name; args; script; serviceAccount; allowFailure; allowExitCodes]
C.f9: Assign step IDs and set waitFor to the required preceding step IDs; downstream execution depends on those steps completing successfully, not just their textual location.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/configuring-builds/configure-build-step-order — id; waitFor]
C.f10: Keep required gate failures fatal: do not set allowFailure or add failing gate exit codes to allowExitCodes, and ensure a rejected Python gate exits unsuccessfully.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/build-config-file-schema — Build steps; name; args; script; serviceAccount; allowFailure; allowExitCodes]
C.f11: Use the configured Pub/Sub artifact/event trigger with its configured payload bindings and filters to run the existing pipeline, then inspect actual stage results and resolved inputs for accepted and rejected fixtures.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/automating-builds/create-pubsub-triggers — Creating a Pub/Sub trigger; Substitution variables; Filters]
C.f12: With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading accepts standard YAML tags, not arbitrary Python object constructors.   [sources: python_tutorial#https://pyyaml.org/wiki/PyYAMLDocumentation — Reference: safe_load; safe_dump]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Gate Data and Model Releases.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.model_acceptance_criteria, mle.protected_test_comparison, mle.model_version_registration, mle.validation_candidate_comparison. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Implement a learner-defined Python acceptance function in the supplied artifact-triggered Cloud Build pipeline, writing the required imports yourself. Read the supplied candidate and accepted-reference evidence, calculate validation expected error cost from the declared probabilities and costs, and evaluate every required quality and operating predicate. Reject failed or incomplete evidence with explicit exceptions identifying the affected predicates. Write assertions for passing and failing evidence, safely write and reload the existing configuration, wire the assigned gate entry point and required step dependencies, and trigger accepted and rejected fixtures through the configured Pub/Sub event trigger.  SUCCESS: Assertions confirm acceptance only when all required predicates are complete and passing, and confirm explicit rejection for failed or incomplete evidence, including undefined rates from empty conditioning groups. The reloaded configuration retains the required image, command, step IDs and waitFor dependencies without failure-tolerant gate settings. Actual resolved inputs identify the intended candidate fixtures. The accepted run passes the gate and reaches promotion; the rejected run exits unsuccessfully at the gate and does not execute promotion.
ASSESSMENT ANCHOR: reject_failed_or_incomplete_candidate_acceptance facts=['f1', 'f2', 'f3', 'f4']
ASSESSMENT ANCHOR: calculate_validation_error_cost_and_apply_operating_limits facts=['f3', 'f5', 'f6']
ASSESSMENT ANCHOR: preserve_protected_test_isolation facts=['f7']
ASSESSMENT ANCHOR: wire_a_fatal_acceptance_gate_before_promotion facts=['f8', 'f9', 'f10']
ASSESSMENT ANCHOR: verify_event_triggered_gate_results_block_rejected_promotion facts=['f4', 'f11']
ASSESSMENT ANCHOR: safely_round_trip_and_inspect_release_configuration facts=['f12']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute training and inference expenditure to workloads; Audit dataset, code, run and artifact lineage of a deployed model; Block release promotion when model acceptance gates fail; Choose scheduled, new-data or investigated quality/drift retraining triggers; Configure actionable model and service alerts; Define artifact dependencies between ML pipeline stages; Detect model-input data drift against a defined reference distribution; Distinguish data drift, concept drift and observed quality degradation; Gate a retrained candidate against the incumbent using validation evidence before controlled promotion; Invoke retraining with a versioned input snapshot from an authorized trigger; Measure production model quality when labels arrive; Monitor production input and prediction distributions; Prevent duplicate or overlapping retraining runs; Promote an approved registry version through accountable staged ML release gates; Recover a failed ML pipeline run without bypassing quality gates; Remove model-serving resources safely on an existing platform; Set an ML workload cost guardrail on an existing platform; Test preprocessing and model inference behavior; Track ML workload compute and m

## LESSON, in learner order

### s01 · explainer · Keep the boundary explicit
Fail-Closed Data, Behavior and Release Gates — 
(mechanism) Keep data-quality rejection fatal on the affected training path, rather than reporting a warning that training can ignore. ⟦A:tb1⟧
(mechanism) Validate before training. Unexpected or missing features and invalid feature values should stop the affected execution. Give every required schema/quality check a name, aggregate its result under the supplied pass/fail policy, and raise or return the declared failure without invoking training. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Retain the tested snapshot and failed checks for revalidation after repair. Assert the declared valid, boundary and failure predicates; false predicates raise AssertionError in ordinary non-optimized execution. In Cloud Build steps, name selects the execution image and args or script supplies the command: wire the assigned function/test entry point. ⟦A.f4 A.f5 A.f6 A:tb3⟧
(example) Accepted quality checks permit training; a rejected required check exits unsuccessfully and training does not start. These panels show bounded fixture-run results. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A:tb1 A:tb2 A:tb3⟧
[DIAGRAM: Computed dataset-gate fixture runs] nodes=["valid {failed_checks: []; named_checks: {'feature_values': True, 'label_values': True, 'schema': True, 'unique_sample_id': True}; sha256: 9a80d8aba1a479286779fd296606d795b9d7b91cfc0feaceacddeaffa24b8572; snapshot_id: snapshot.valid; quality: SUCCESS, exit=0; resolved args: ['python', 'panel_worker.py', 'dataset', 'valid']; training: SUCCESS, exit=0; resolved args: ['python', 'training_entry.py', 'valid']}", "missing_required_feature {failed_checks: ['schema', 'feature_values']; named_checks: {'feature_values': False, 'label_values': True, 'schema': False, 'unique_sample_id': True}; sha256: 09398d2fd8847ec08e07b24bc0cd5cfc4f10e9f7ac6c9bc3e6c507ad8f8e1257; snapshot_id: snapshot.missing_required_feature; quality: FAILURE, exit=1; resolved args: ['python', 'panel_worker.py', 'dataset', 'missing_required_feature']; training: NOT_STARTED, exit=None; resolved args: ['python', 'training_entry.py', 'missing_required_feature']}"] edges=[] alt: Accepted and rejected fixture panels show resolved snapshots, named check evidence, quality exit and training status.
(example) Accepted quality checks permit training; a rejected required check exits unsuccessfully and training does not start. These panels show bounded fixture-run results. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A:tb1 A:tb2 A:tb3⟧

### s02 · explainer · Gate pipeline execution on dataset-quality tests
Fail-Closed Data, Behavior and Release Gates — 
(mechanism) Give stages IDs and waitFor their required predecessors: successful completion, not textual position, controls dependencies. Keep rejection fatal: no allowFailure or failing exit codes in allowExitCodes; rejected Python gates must exit unsuccessfully. Use the configured repository commit trigger and branch filter; inspect stage results and resolved inputs for accepted and rejected fixtures. ⟦A.f7 A.f8 A.f9 A:tb4⟧
(mechanism) With declared PyYAML, import yaml. Write mapping/list configuration with yaml.safe_dump(config, file_handle), reload with yaml.safe_load(file_handle), and inspect required resolved fields before runtime submission. Safe loading accepts standard YAML tags, not arbitrary Python object constructors. ⟦A.f10 A:tb5⟧

### s03 · explainer · Gate pipeline execution on dataset-quality tests
Fail-Closed Data, Behavior and Release Gates — 
(example) For the missing-required-feature fixture, retain the snapshot identity and named failure. Raise or return the declared rejection and verify training did not run. Wire the assigned image, command, IDs and waitFor edges; do not allow failing gate exits. Inspect accepted and rejected repository-triggered results. Repair must pass the same requirements before this path continues. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A.f9 A.f10 A:tb6⟧
(mechanism) A failure report is not a blocking gate if training still runs. Allowing gate failures or their exit codes defeats the fatal boundary. ⟦A.f3 A.f7 A.f8 A:tb7⟧

### s04 · check · Inspect round-tripped gate configuration
Fail-Closed Data, Behavior and Release Gates — Use the supplied evidence to judge the required predicates and boundaries.

### s05 · hands_on · Verify gate pipeline execution on dataset-quality tests
Fail-Closed Data, Behavior and Release Gates — Implement the assigned function and configuration checks using the supplied fixtures; verify accepted and rejected behavior at the required fatal boundary.

### s06 · explainer · Test preprocessing and model inference behavior
Fail-Closed Data, Behavior and Release Gates — 
(mechanism) Test the package clients use, including fitted preprocessing. An isolated estimator with manually prepared input could miss a package defect. ⟦B:tb1⟧
(mechanism) Call the packaged fitted preprocessing and model through the inference prediction path. Check fixture row count, feature/target correspondence and output shape before values. Compare numerical output with np.testing.assert_allclose and explicitly declared tolerances. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Exercise malformed and boundary fixtures, requiring explicit rejection where the contract forbids them. Assert valid, boundary and failure predicates; false predicates raise AssertionError in ordinary non-optimized execution. Wire the assigned test entry point into Cloud Build: name specifies its image, args or script its command. ⟦B.f4 B.f5 B.f6 B:tb3⟧
[SIDE_BY_SIDE] Compare packaged-path check results, not just inputs: a required regression fails the test stage and prevents dependent execution. left_label: Accepted fixture | right_label: Rejected fixture
  left:
[CODE python]
computed_panel = {'source_asset_id': 'ws.model_behavior_tests',
 'runtime': 'bounded local runtime_sim; not a cloud run',
 'event': {'branch': 'main', 'snapshot_id': 'valid', 'case_id': 'accepted'},
 'triggered': True,
 'resolved_inputs': {'_ARTIFACT': 'A', '_CASE': 'accepted', '_SNAPSHOT': 'valid'},
 'steps': [{'id': 'behavior_tests',
            'name': 'python:3.11',
            'resolved_args': ['python', 'panel_worker.py', 'behavior', 'accepted'],
            'waitFor': [],
            'status': 'SUCCESS',
            'exit_code': 0,
            'evidence': {'accepted': True,
                         'execution': {'fixture_id': 'valid', 'regression': None},
                         'fixtures': {'boundary_high': {'accepted': True,
                                                        'actual_count': 1,
                                                        'actual_sample_ids': ['sample.204'],
                                                        'actual_shape': [1, 1],
                                                        'atol': 1e-08,
                                                        'correspondence': True,
                                                        'expected_count': 1,
                                                        'expected_sample_ids': ['sample.204'],
                                                        'expected_shape': [1, 1],
                                                        'numerical_check': True,
                                                        'numerical_status': 'PASS',
                                                        'rtol': 1e-07},
                                      'boundary_low': {'accepted': True,
                                                       'actual_count': 1,
                                                       'actual_sample_ids': ['sample.201'],
                                                       'actual_shape': [1, 1],
                                                       'atol': 1e-08,
                                                       'correspondence': True,
                                                       'expected_count': 1,
                                                       'expected_sample_ids': ['sample.201'],
                                                       'expected_shape': [1, 1],
                                                       'numerical_check': True,
                                                       'numerical_status': 'PASS',
                                                       'rtol': 1e-07},
                                      'empty': {'accepted': True,
                                                'actual_count': 0,
                                                'actual_sample_ids': [],
                                                'actual_shape': [0, 1],
                                                'atol': 1e-08,
                                                'correspondence': True,
                                                'expected_count': 0,
                                                'expected_sample_ids': [],
                                                'expected_shape': [0, 1],
                                                'numerical_check': True,
                                                'numerical_status': 'PASS',
                                                'rtol': 1e-07},
                                      'malformed': {'accepted': True,
                                                    'contract_required_rejection': True,
                                                    'expected_exception': 'InputContractError',
                                                    'observed_exception': 'InputContractError'},
                                      'missing_feature': {'accepted': True,
                                                          'contract_required_rejection': True,
                                                          'expected_exception': 'InputContractError',
                                                          'observed_exception': 'InputContractError'},
                                      'out_of_bounds': {'accepted': True,
                                                        'contract_required_rejection': True,
                                                        'expected_exception': 'InputContractError',
                                                        'observed_exception': 'InputContractError'},
                                      'valid': {'accepted': True,
                                                'actual_count': 4,
                                                'actual_sample_ids': ['sample.201',
                                                                      'sample.202',
                                                                      'sample.203',
                                                                      'sample.204'],
                                                'actual_shape': [4, 1],
                                                'atol': 1e-08,
                                                'correspondence': True,
                                                'expected_count': 4,
                                                'expected_sample_ids': ['sample.201',
                                                                        'sample.202',
                                                                        'sample.203',
                                                                        'sample.204'],
                                                'expected_shape': [4, 1],
                                                'numerical_check': True,
                                                'numerical_status': 'PASS',
                                                'rtol': 1e-07}},
                         'packaged_path': 'FittedPackage.predict -> predict_records'}},
           {'id': 'release_gate',
            'name': 'python:3.11',
            'resolved_args': ['python', 'downstream_entry.py', 'A'],
            'waitFor': ['behavior_tests'],
            'status': 'SUCCESS',
            'exit_code': 0}]}
  annotations: ['Computed accepted results']
  right:
[CODE python]
computed_panel = {'source_asset_id': 'ws.model_behavior_tests',
 'runtime': 'bounded local runtime_sim; not a cloud run',
 'event': {'branch': 'main',
           'snapshot_id': 'missing_required_feature',
           'case_id': 'regressed'},
 'triggered': True,
 'resolved_inputs': {'_ARTIFACT': 'A',
                     '_CASE': 'regressed',
                     '_SNAPSHOT': 'missing_required_feature'},
 'steps': [{'id': 'behavior_tests',
            'name': 'python:3.11',
            'resolved_args': ['python', 'panel_worker.py', 'behavior', 'regressed'],
            'waitFor': [],
            'status': 'FAILURE',
            'exit_code': 1,
            'evidence': {'accepted': False,
                         'execution': {'fixture_id': 'valid',
                                       'regression': 'reverse_rows'},
                         'fixtures': {'boundary_high': {'accepted': True,
                                                        'actual_count': 1,
                                                        'actual_sample_ids': ['sample.204'],
                                                        'actual_shape': [1, 1],
                                                        'atol': 1e-08,
                                                        'correspondence': True,
                                                        'expected_count': 1,
                                                        'expected_sample_ids': ['sample.204'],
                                                        'expected_shape': [1, 1],
                                                        'numerical_check': True,
                                                        'numerical_status': 'PASS',
                                                        'rtol': 1e-07},
                                      'boundary_low': {'accepted': True,
                                                       'actual_count': 1,
                                                       'actual_sample_ids': ['sample.201'],
                                                       'actual_shape': [1, 1],
                                                       'atol': 1e-08,
                                                       'correspondence': True,
                                                       'expected_count': 1,
                                                       'expected_sample_ids': ['sample.201'],
                                                       'expected_shape': [1, 1],
                                                       'numerical_check': True,
                                                       'numerical_status': 'PASS',
                                                       'rtol': 1e-07},
                                      'empty': {'accepted': True,
                                                'actual_count': 0,
                                                'actual_sample_ids': [],
                                                'actual_shape': [0, 1],
                                                'atol': 1e-08,
                                                'correspondence': True,
                                                'expected_count': 0,
                                                'expected_sample_ids': [],
                                                'expected_shape': [0, 1],
                                                'numerical_check': True,
                                                'numerical_status': 'PASS',
                                                'rtol': 1e-07},
                                      'malformed': {'accepted': True,
                                                    'contract_required_rejection': True,
                                                    'expected_exception': 'InputContractError',
                                                    'observed_exception': 'InputContractError'},
                                      'missing_feature': {'accepted': True,
                                                          'contract_required_rejection': True,
                                                          'expected_exception': 'InputContractError',
                                                          'observed_exception': 'InputContractError'},
                                      'out_of_bounds': {'accepted': True,
                                                        'contract_required_rejection': True,
                                                        'expected_exception': 'InputContractError',
                                                        'observed_exception': 'InputContractError'},
                                      'valid': {'accepted': False,
                                                'actual_count': 4,
                                                'actual_sample_ids': ['sample.204',
                                                                      'sample.203',
                                                                      'sample.202',
                                                                      'sample.201'],
                                                'actual_shape': [4, 1],
                                                'atol': 1e-08,
                                                'correspondence': False,
                                                'expected_count': 4,
                                                'expected_sample_ids': ['sample.201',
                                                                        'sample.202',
                                                                        'sample.203',
                                                                        'sample.204'],
                                                'expected_shape': [4, 1],
                                                'numerical_check': None,
                                                'numerical_status': 'NOT_RUN: '
                                                                    'structural checks '
                                                                    'failed',
                                                'rtol': 1e-07}},
                         'packaged_path': 'FittedPackage.predict -> predict_records'}},
           {'id': 'release_gate',
            'name': 'python:3.11',
            'resolved_args': ['python', 'downstream_entry.py', 'A'],
            'waitFor': ['behavior_tests'],
            'status': 'NOT_STARTED',
            'exit_code': None}]}
  annotations: ['Computed rejected results']

### s07 · explainer · Test preprocessing and model inference behavior
Fail-Closed Data, Behavior and Release Gates — 
(mechanism) Give stages IDs and waitFor their required predecessors: successful completion, not textual position, controls dependencies. Keep rejection fatal: no allowFailure or failing exit codes in allowExitCodes; rejected Python gates must exit unsuccessfully. Use the configured repository commit trigger and branch filter; inspect stage results and resolved inputs for accepted and rejected fixtures. ⟦B.f7 B.f8 B.f9 B:tb4⟧
(mechanism) With declared PyYAML, import yaml. Write mapping/list configuration with yaml.safe_dump(config, file_handle), reload with yaml.safe_load(file_handle), and inspect required resolved fields before runtime submission. Safe loading accepts standard YAML tags, not arbitrary Python object constructors. ⟦B.f10 B:tb5⟧

### s08 · explainer · Test preprocessing and model inference behavior
Fail-Closed Data, Behavior and Release Gates — 
(example) For the supplied valid fixture, check rows, correspondence and shape before numerical agreement at explicit tolerances. Exercise malformed and boundary inputs with contract-required rejection. Wire dependencies and fatal rejection into the existing build. Inspect repository-triggered stage results and resolved YAML fields: local test success alone is not the pipeline verdict. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 B.f9 B.f10 B:tb6⟧
(mechanism) Right-looking numbers for the wrong rows are still defective. Require correspondence and shape, call the packaged fitted path, and block downstream execution on required test failure. ⟦B.f1 B.f2 B.f3 B.f8 B:tb7⟧

### s09 · check · Inspect packaged-path test evidence
Fail-Closed Data, Behavior and Release Gates — Use the supplied evidence to judge the required predicates and boundaries.

### s10 · hands_on · Verify test preprocessing and model inference behavior
Fail-Closed Data, Behavior and Release Gates — Implement the assigned function and configuration checks using the supplied fixtures; verify accepted and rejected behavior at the required fatal boundary.

### s11 · explainer · Block release promotion when model acceptance gates fail
Fail-Closed Data, Behavior and Release Gates — 
(mechanism) Gate the exact candidate evidence against predeclared requirements. Aggregate improvement cannot replace complete, passing quality and operating predicates. ⟦C:tb1⟧
(mechanism) Before promotion, compare the candidate with the accepted reference and predeclared requirements. Evaluate every supplied acceptance predicate and identify failures. Calculate validation expected error cost with fixed deployment probabilities and error costs; include fixed latency and operating limits in eligibility. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) Failed or incomplete required gates block promotion. FPR conditions on actual negatives; FNR on actual positives. An empty conditioning group has no defined rate. With zero cost for correct predictions, weight each error rate by its supplied deployment class probability and error cost. ⟦C.f4 C.f5 C.f6 C:tb3⟧
[SIDE_BY_SIDE] A meets the fixed requirements. B meets the cost requirement but exceeds the latency limit, so its gate rejects and promotion does not execute. left_label: Accepted fixture | right_label: Rejected fixture
  left:
[CODE python]
computed_panel = {'source_asset_id': 'ws.model_release_quality_gate',
 'runtime': 'bounded local runtime_sim; not a cloud run',
 'event': {'event_type': 'artifact_ready', 'case_id': 'A', 'artifact_id': 'A'},
 'triggered': True,
 'resolved_inputs': {'_ARTIFACT': 'A', '_CASE': 'A', '_SNAPSHOT': 'valid'},
 'steps': [{'id': 'release_gate',
            'name': 'python:3.11',
            'resolved_args': ['python', 'panel_worker.py', 'release', 'A', 'A'],
            'waitFor': [],
            'status': 'SUCCESS',
            'exit_code': 0,
            'evidence': {'accepted': True,
                         'candidate_id': 'A',
                         'cost_limit': 0.16,
                         'event_artifact': 'A',
                         'evidence_complete': True,
                         'expected_error_cost': 0.08,
                         'latency_limit_ms': 20,
                         'latency_result_ms': 20,
                         'operating_ok': True,
                         'reference_cost': 0.16,
                         'required_predicates': {'all evidence fields present': True,
                                                 'both actual-class denominators nonempty': True,
                                                 'candidate identity matches event': True,
                                                 'evidence_complete is True': True,
                                                 'expected error cost <= fixed maximum and <= accepted reference cost': True,
                                                 'latency_ms <= fixed maximum': True,
                                                 'nonnegative integer counts': True,
                                                 'operating_ok is True': True}}},
           {'id': 'promotion',
            'name': 'python:3.11',
            'resolved_args': ['python', 'downstream_entry.py', 'A'],
            'waitFor': ['release_gate'],
            'status': 'SUCCESS',
            'exit_code': 0}]}
  annotations: ['Computed accepted results']
  right:
[CODE python]
computed_panel = {'source_asset_id': 'ws.model_release_quality_gate',
 'runtime': 'bounded local runtime_sim; not a cloud run',
 'event': {'event_type': 'artifact_ready', 'case_id': 'B', 'artifact_id': 'B'},
 'triggered': True,
 'resolved_inputs': {'_ARTIFACT': 'B', '_CASE': 'B', '_SNAPSHOT': 'valid'},
 'steps': [{'id': 'release_gate',
            'name': 'python:3.11',
            'resolved_args': ['python', 'panel_worker.py', 'release', 'B', 'B'],
            'waitFor': [],
            'status': 'FAILURE',
            'exit_code': 1,
            'evidence': {'accepted': False,
                         'candidate_id': 'B',
                         'cost_limit': 0.16,
                         'event_artifact': 'B',
                         'evidence_complete': True,
                         'expected_error_cost': 0.064,
                         'latency_limit_ms': 20,
                         'latency_result_ms': 21,
                         'operating_ok': True,
                         'reference_cost': 0.16,
                         'required_predicates': {'all evidence fields present': True,
                                                 'both actual-class denominators nonempty': True,
                                                 'candidate identity matches event': True,
                                                 'evidence_complete is True': True,
                                                 'expected error cost <= fixed maximum and <= accepted reference cost': True,
                                                 'latency_ms <= fixed maximum': False,
                                                 'nonnegative integer counts': True,
                                                 'operating_ok is True': True}}},
           {'id': 'promotion',
            'name': 'python:3.11',
            'resolved_args': ['python', 'downstream_entry.py', 'B'],
            'waitFor': ['release_gate'],
            'status': 'NOT_STARTED',
            'exit_code': None}]}
  annotations: ['Computed rejected results']

### s12 · explainer · Block release promotion when model acceptance gates fail
Fail-Closed Data, Behavior and Release Gates — 
(mechanism) Protected test observations must not fit preprocessing, select a model or tune settings: that leaks information into the chosen system. Wire the assigned Cloud Build entry point with name for its image and args or script for its command. Set IDs and waitFor required predecessors; textual order is not the dependency. ⟦C.f7 C.f8 C.f9 C:tb4⟧

### s13 · explainer · Block release promotion when model acceptance gates fail
Fail-Closed Data, Behavior and Release Gates — 
(mechanism) Keep rejection fatal: no allowFailure or allowed failing exit codes, and a rejected Python gate exits unsuccessfully. Use the configured Pub/Sub trigger, payload bindings and filters; inspect stage results and resolved inputs for accepted and rejected fixtures. With declared PyYAML, import yaml. Write mapping/list configuration with yaml.safe_dump(config, file_handle), reload with yaml.safe_load(file_handle), and inspect required resolved fields before runtime submission. Safe loading accepts standard YAML tags, not arbitrary Python object constructors. ⟦C.f10 C.f11 C.f12 C:tb5⟧

### s14 · explainer · Block release promotion when model acceptance gates fail
Fail-Closed Data, Behavior and Release Gates — 
(example) If cost meets its bound but latency fails, reject and name the latency predicate. Use fixed probabilities, costs and actual-class denominators. Bind evidence to the candidate. Configure image, command and waitFor without failure tolerance, then inspect event-bound inputs and results. Keep protected tests outside fitting/tuning; incomplete requirements block promotion too. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C.f7 C.f8 C.f9 C.f10 C.f11 C.f12 C:tb6⟧
(mechanism) This gate is not an average of requirements. One failed or incomplete condition blocks promotion even when another metric improves. ⟦C.f2 C.f3 C.f4 C:tb7⟧

### s15 · check · Distinguish protected-test evaluation from tuning
Fail-Closed Data, Behavior and Release Gates — Use the supplied evidence to judge the required predicates and boundaries.

### s16 · check · Inspect fixed release requirements
Fail-Closed Data, Behavior and Release Gates — Use the supplied evidence to judge the required predicates and boundaries.

### s17 · hands_on · Verify block release promotion when model acceptance gates fail
Fail-Closed Data, Behavior and Release Gates — Implement the assigned function and configuration checks using the supplied fixtures; verify accepted and rejected behavior at the required fatal boundary.

### s18 · recap · Keep each boundary accountable
Fail-Closed Data, Behavior and Release Gates — 
(takeaway) Dataset rejection must stop the affected training path. ⟦A.f3 A.f7 A.f8 A:tb7⟧
(takeaway) Test the packaged fitted path: correspondence and shape matter alongside numbers. ⟦B.f1 B.f2 B.f3 B.f8 B:tb7⟧
(takeaway) One failed or incomplete required acceptance condition blocks promotion. ⟦C.f2 C.f3 C.f4 C:tb7⟧
[UP NEXT] Define explicit input/output artifact dependencies: Next: mle.tile.076_079.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the required checks — Return to the same fictional lifecycle fixtures.
(mechanism) With declared PyYAML, import yaml; yaml.safe_dump(config, file_handle), then yaml.safe_load(file_handle). Inspect required resolved fields before runtime submission. Safe loading accepts standard tags, not arbitrary Python constructors. ⟦A.f10 A:tb5⟧
(mechanism) Cloud Build steps use name for the image and args or script for the command; wire the assigned entry point. ⟦A.f6 A:tb3⟧
(mechanism) Assign IDs and waitFor required predecessors’ successful completion, not merely textual order. ⟦A.f7 A:tb4 A:tb7⟧
(mechanism) No allowFailure or allowed failing exit codes for required gates; rejected Python gates exit unsuccessfully. ⟦A.f8 A:tb4 A:tb7⟧
(misconception) A failure report is not a blocking gate if training still runs. Allowing gate failures or their exit codes defeats the fatal boundary. ⟦A.f3 A.f7 A.f8 A:tb7⟧
### r02 · Separate the required checks — Return to the same fictional lifecycle fixtures.
(mechanism) Validate before training; unexpected/missing features or invalid values should stop the affected execution. ⟦A.f1 A:tb2⟧
(mechanism) With declared PyYAML, import yaml; yaml.safe_dump(config, file_handle), then yaml.safe_load(file_handle). Inspect required resolved fields before runtime submission. Safe loading accepts standard tags, not arbitrary Python constructors. ⟦A.f10 A:tb5⟧
(mechanism) Name every required check and aggregate explicit pass/fail under the supplied gate policy. ⟦A.f2 A:tb2⟧
(mechanism) Raise or return declared failure on required rejection; do not invoke training. ⟦A.f3 A:tb2 A:tb7⟧
(mechanism) Retain snapshot and failed checks so repaired data can meet the same requirements. ⟦A.f4 A:tb3⟧
(mechanism) Assert valid, boundary and failure predicates; false predicates raise AssertionError in ordinary non-optimized execution. ⟦A.f5 A:tb3⟧
(mechanism) Cloud Build steps use name for the image and args or script for the command; wire the assigned entry point. ⟦A.f6 A:tb3⟧
(mechanism) Assign IDs and waitFor required predecessors’ successful completion, not merely textual order. ⟦A.f7 A:tb4 A:tb7⟧
(mechanism) No allowFailure or allowed failing exit codes for required gates; rejected Python gates exit unsuccessfully. ⟦A.f8 A:tb4 A:tb7⟧
(mechanism) Use the configured commit trigger and branch filter; inspect stage results and resolved inputs for accepted/rejected fixtures. ⟦A.f9 A:tb4⟧
(misconception) A failure report is not a blocking gate if training still runs. Allowing gate failures or their exit codes defeats the fatal boundary. ⟦A.f3 A.f7 A.f8 A:tb7⟧
### r03 · Separate the required checks — Return to the same fictional lifecycle fixtures.
(mechanism) With declared PyYAML, import yaml; yaml.safe_dump(config, file_handle), then yaml.safe_load(file_handle). Inspect required resolved fields before runtime submission. Safe loading accepts standard tags, not arbitrary Python constructors. ⟦B.f10 B:tb5⟧
(misconception) Right-looking numbers for the wrong rows are still defective. Require correspondence and shape, call the packaged fitted path, and block downstream execution on required test failure. ⟦B.f1 B.f2 B.f3 B.f8 B:tb7⟧
### r04 · Separate the required checks — Return to the same fictional lifecycle fixtures.
(mechanism) Test packaged fitted preprocessing and model through the inference prediction path. ⟦B.f1 B:tb2 B:tb7⟧
(mechanism) With declared PyYAML, import yaml; yaml.safe_dump(config, file_handle), then yaml.safe_load(file_handle). Inspect required resolved fields before runtime submission. Safe loading accepts standard tags, not arbitrary Python constructors. ⟦B.f10 B:tb5⟧
(mechanism) Check each fixture’s row count, feature/target correspondence and output shape before values. ⟦B.f2 B:tb2 B:tb7⟧
(mechanism) Compare numerical output with np.testing.assert_allclose at explicitly declared tolerances. ⟦B.f3 B:tb2 B:tb7⟧
(mechanism) Exercise malformed/boundary fixtures; require explicit rejection where the contract forbids them. ⟦B.f4 B:tb3⟧
(mechanism) Assert valid, boundary and failure predicates; false predicates raise AssertionError in ordinary non-optimized execution. ⟦B.f5 B:tb3⟧
(mechanism) Cloud Build steps use name for the image and args or script for the command; wire the assigned entry point. ⟦B.f6 B:tb3⟧
(mechanism) Assign IDs and waitFor required predecessors’ successful completion, not merely textual order. ⟦B.f7 B:tb4⟧
(mechanism) No allowFailure or allowed failing exit codes for required gates; rejected Python gates exit unsuccessfully. ⟦B.f8 B:tb4 B:tb7⟧
(mechanism) Use the configured commit trigger and branch filter; inspect stage results and resolved inputs for accepted/rejected fixtures. ⟦B.f9 B:tb4⟧
(misconception) Right-looking numbers for the wrong rows are still defective. Require correspondence and shape, call the packaged fitted path, and block downstream execution on required test failure. ⟦B.f1 B.f2 B.f3 B.f8 B:tb7⟧
### r05 · Separate the required checks — Return to the same fictional lifecycle fixtures.
(mechanism) Protected test observations must not fit preprocessing, select models or tune settings; that leaks information. ⟦C.f7 C:tb4⟧
(misconception) This gate is not an average of requirements. One failed or incomplete condition blocks promotion even when another metric improves. ⟦C.f2 C.f3 C.f4 C:tb7⟧
### r06 · Separate the required checks — Return to the same fictional lifecycle fixtures.
(mechanism) With declared PyYAML, import yaml; yaml.safe_dump(config, file_handle), then yaml.safe_load(file_handle). Inspect required resolved fields before runtime submission. Safe loading accepts standard tags, not arbitrary Python constructors. ⟦C.f12 C:tb5⟧
(misconception) This gate is not an average of requirements. One failed or incomplete condition blocks promotion even when another metric improves. ⟦C.f2 C.f3 C.f4 C:tb7⟧
### r07 · Separate the required checks — Return to the same fictional lifecycle fixtures.
(mechanism) Compare candidate with accepted reference and predeclared requirements before promotion. ⟦C.f1 C:tb2⟧
(mechanism) No allowFailure or allowed failing exit codes for required gates; rejected Python gates exit unsuccessfully. ⟦C.f10 C:tb5⟧
(mechanism) Use configured Pub/Sub payload bindings and filters; inspect stage results and resolved inputs for accepted/rejected fixtures. ⟦C.f11 C:tb5⟧
(mechanism) Evaluate every supplied acceptance predicate; identify failures on rejection. ⟦C.f2 C:tb2 C:tb7⟧
(mechanism) Calculate validation expected error cost using fixed deployment probabilities/costs; include fixed latency/operating limits. ⟦C.f3 C:tb2 C:tb7⟧
(mechanism) Failed or incomplete required gates block promotion. ⟦C.f4 C:tb3 C:tb7⟧
(mechanism) FPR = FP/(FP+TN); FNR = FN/(FN+TP). Empty actual-class groups give undefined rates. ⟦C.f5 C:tb3⟧
(mechanism) With zero correct-prediction cost, expected cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. ⟦C.f6 C:tb3⟧
(mechanism) Cloud Build steps use name for the image and args or script for the command; wire the assigned entry point. ⟦C.f8 C:tb4⟧
(mechanism) Assign IDs and waitFor required predecessors’ successful completion, not merely textual order. ⟦C.f9 C:tb4⟧
(misconception) This gate is not an average of requirements. One failed or incomplete condition blocks promotion even when another metric improves. ⟦C.f2 C.f3 C.f4 C:tb7⟧

=========

# EVALUATOR PACKET — mle.tile.076_079 (mle.tile.076_079)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.pipeline_artifact_dependencies — Define artifact dependencies between ML pipeline stages
B = mle.staged_ml_promotion — Promote an approved registry version through accountable staged ML release gates
C = mle.pipeline_failure_recovery — Recover a failed ML pipeline run without bypassing quality gates
D = mle.deployed_model_lineage_audit — Audit dataset, code, run and artifact lineage of a deployed model

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (mle.pipeline_artifact_dependencies)   objective: Encode and verify immutable artifact dependencies between pipeline stages.
A.f1: Reusable pipeline components need explicit input/output artifacts so the same workflow can run across experiment and production environments.   [sources: google_mlops_pipelines#MLOps level 1: ML pipeline automation — Characteristics]
A.f2: Record each stage’s consumed dataset/artifact identity, execution parameters and produced artifact identity rather than joining unrelated stage outputs only by filename.   [sources: google_mlops_pipelines#Metadata management]
A.f3: Represent the stage dependency map as a dictionary and check that every required upstream artifact identity matches the supplied downstream reference.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
A.f4: Require the relevant dataset or model validation result before executing a stage that depends on that validated artifact.   [sources: google_mlops_pipelines#Data and model validation]
A.f5: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
A.f6: In an existing Cloud Build YAML/JSON configuration, each steps item declares its execution image in name and its command in args or script; wire the function/test entry point into the assigned stage.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/build-config-file-schema — Build steps; name; args; script; serviceAccount; allowFailure; allowExitCodes]
A.f7: Assign step IDs and set waitFor to the required preceding step IDs; downstream execution depends on those steps completing successfully, not just their textual location.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/configuring-builds/configure-build-step-order — id; waitFor]
A.f8: Keep required gate failures fatal: do not set allowFailure or add failing gate exit codes to allowExitCodes, and ensure a rejected Python gate exits unsuccessfully.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/build-config-file-schema — Build steps; name; args; script; serviceAccount; allowFailure; allowExitCodes]
A.f9: Use the configured Pub/Sub artifact/event trigger with its configured payload bindings and filters to run the existing pipeline, then inspect actual stage results and resolved inputs for accepted and rejected fixtures.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/automating-builds/create-pubsub-triggers — Creating a Pub/Sub trigger; Substitution variables; Filters]
A.f10: Bind each consumer stage’s args/substitutions to the immutable artifact identifier produced by its declared upstream stage; inspect actual run inputs to verify the edge rather than only reviewing stage order.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/build-config-file-schema — Build steps; name; args; script; serviceAccount; allowFailure; allowExitCodes]
A.f11: With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading accepts standard YAML tags, not arbitrary Python object constructors.   [sources: python_tutorial#https://pyyaml.org/wiki/PyYAMLDocumentation — Reference: safe_load; safe_dump]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Orchestrate Traceable Promotion.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.training_dataset_version, mle.model_version_registration. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Edit the supplied Cloud Build YAML configuration and dependency-map checks to connect data validation, training and model validation through immutable artifact references. Preserve required fatal gates, serialize and reload the configuration, then exercise the existing configured Pub/Sub trigger with bounded accepted and rejected fixtures and inspect resolved stage inputs.  SUCCESS: The reloaded configuration has the required execution images, entry points, step IDs, waitFor edges and immutable consumer references. Predicate checks distinguish the declared valid, boundary and failure cases, including training output A incorrectly referenced as B. Accepted fixture results confirm the actual producer-consumer identities; rejected fixture results show unsuccessful required gates and no execution of their dependent stages.
ASSESSMENT ANCHOR: specify_immutable_artifact_producer_consumer_edges facts=['f1', 'f2', 'f3', 'f10']
ASSESSMENT ANCHOR: configure_required_stage_dependencies_and_fatal_validation_gates facts=['f4', 'f6', 'f7', 'f8']
ASSESSMENT ANCHOR: assert_artifact_dependency_contracts_for_declared_cases facts=['f3', 'f5']
ASSESSMENT ANCHOR: serialize_reload_and_inspect_pipeline_configuration facts=['f6', 'f11']
ASSESSMENT ANCHOR: verify_artifact_edges_from_resolved_run_inputs facts=['f9', 'f10']

## SOURCE FACTS — B (mle.staged_ml_promotion)   objective: Gate an existing staging-to-production handoff on artifact-specific approval, quality and protected identity.
B.f1: Read the approved registered model name/version and its run/artifact link before authorizing staged deployment.   [sources: mlflow_docs#ml/model-registry/workflow/ — Registering a Model; Fetching an MLflow Model from the Model Registry; Deploy and Organize Models]
B.f2: Automated continuous delivery first checks the model’s compatibility in a test environment and then passes model validation before production deployment.   [sources: google_mlops_pipelines#MLOps level 2: CI/CD pipeline automation — CI/CD pipeline]
B.f3: Preserve the validation verdict for the exact artifact being promoted, including its offline requirements and supplied staged evaluation evidence.   [sources: google_mlops_pipelines#Data and model validation]
B.f4: Keep the promotion within the permitted identity and approval scope, recording the accountable authorization rather than changing the policy.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/blueprints/security-foundations/authentication-authorization — Authentication and authorization]
B.f5: Write the approval, registry version, artifact identity and per-stage gate results into the promotion record.   [sources: google_mlops_pipelines#Metadata management]
B.f6: In an existing Cloud Build YAML/JSON configuration, each steps item declares its execution image in name and its command in args or script; wire the function/test entry point into the assigned stage.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/build-config-file-schema — Build steps; name; args; script; serviceAccount; allowFailure; allowExitCodes]
B.f7: Assign step IDs and set waitFor to the required preceding step IDs; downstream execution depends on those steps completing successfully, not just their textual location.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/configuring-builds/configure-build-step-order — id; waitFor]
B.f8: Keep required gate failures fatal: do not set allowFailure or add failing gate exit codes to allowExitCodes, and ensure a rejected Python gate exits unsuccessfully.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/build-config-file-schema — Build steps; name; args; script; serviceAccount; allowFailure; allowExitCodes]
B.f9: Use the configured Pub/Sub artifact/event trigger with its configured payload bindings and filters to run the existing pipeline, then inspect actual stage results and resolved inputs for accepted and rejected fixtures.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/automating-builds/create-pubsub-triggers — Creating a Pub/Sub trigger; Substitution variables; Filters]
B.f10: Bind approved Secret Manager version references with availableSecrets.secretManager and expose them only to the needed step through secretEnv; the YAML contains references, not secret values.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/securing-builds/use-secrets — Configuring builds to access UTF-8 secrets from Secret Manager]
B.f11: Use the authorized build/step identity and preserve the separate authorization required for a promotion action.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/blueprints/security-foundations/authentication-authorization — Authentication and authorization]
B.f12: Check captured build output for non-disclosure of secret values; do not echo or serialize runtime credentials.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/securing-builds/use-secrets — Configuring builds to access UTF-8 secrets from Secret Manager]
B.f13: Edit and parse the existing staging/production YAML so production depends on staging quality and authorization gates for the identical immutable artifact; test an unauthorized promotion and inspect that production did not execute.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/build-config-file-schema — Build steps; name; args; script; serviceAccount; allowFailure; allowExitCodes]
B.f14: With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading accepts standard YAML tags, not arbitrary Python object constructors.   [sources: python_tutorial#https://pyyaml.org/wiki/PyYAMLDocumentation — Reference: safe_load; safe_dump]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Orchestrate Traceable Promotion.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.model_release_quality_gate, mle.deployment_verification, mle.model_version_registration. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Edit and safely parse the supplied staging/production configuration to promote one approved immutable registry version through staging quality and separate authorization gates. Use the configured event trigger and approved credential references, then inspect accepted and unauthorized fixture results without changing the permission policy.  SUCCESS: The reloaded configuration preserves the approved registry version and artifact identity, wires the supplied entry points into explicit stage dependencies, and keeps required gate failures fatal. The accepted fixture reaches production only after compatibility, validation and authorization succeed. The unauthorized fixture does not execute production. The promotion record retains the approval, exact artifact, validation evidence and per-stage results. Credentials are scoped to the needed step, and neither configuration nor captured output contains their values.
ASSESSMENT ANCHOR: preserve_approved_artifact_identity_and_promotion_evidence facts=['f1', 'f3', 'f5']
ASSESSMENT ANCHOR: enforce_staged_quality_and_authorization_dependencies facts=['f2', 'f6', 'f7', 'f8', 'f13']
ASSESSMENT ANCHOR: record_accountable_promotion_within_authorized_scope facts=['f4', 'f11']
ASSESSMENT ANCHOR: verify_event_bound_inputs_and_rejected_promotion_results facts=['f9', 'f13']
ASSESSMENT ANCHOR: verify_scoped_credential_injection_and_non_disclosure facts=['f10', 'f12']
ASSESSMENT ANCHOR: safely_write_reload_and_inspect_promotion_configuration facts=['f14']

## SOURCE FACTS — C (mle.pipeline_failure_recovery)   objective: Recover an injected stage failure through verified artifact boundaries without bypassing gates.
C.f1: Locate the failed stage from its execution status and retained artifact records, preserving the identities of successfully completed required stages.   [sources: google_mlops_pipelines#Metadata management]
C.f2: Catch the declared recoverable error with try/except, record the failure and apply only the supplied recovery action rather than silently declaring success.   [sources: python_tutorial#errors.html — Handling Exceptions; Raising Exceptions]
C.f3: After a repair, rerun the affected required quality check and stop if it still fails; failure recovery must not bypass dataset or model gates.   [sources: google_mlops_pipelines#Data and model validation]
C.f4: Reuse a completed upstream artifact only when its recorded identity and required validation are still valid for the resumed downstream stage.   [sources: google_mlops_pipelines#MLOps level 1: ML pipeline automation — Characteristics]
C.f5: In an existing Cloud Build YAML/JSON configuration, each steps item declares its execution image in name and its command in args or script; wire the function/test entry point into the assigned stage.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/build-config-file-schema — Build steps; name; args; script; serviceAccount; allowFailure; allowExitCodes]
C.f6: Assign step IDs and set waitFor to the required preceding step IDs; downstream execution depends on those steps completing successfully, not just their textual location.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/configuring-builds/configure-build-step-order — id; waitFor]
C.f7: Keep required gate failures fatal: do not set allowFailure or add failing gate exit codes to allowExitCodes, and ensure a rejected Python gate exits unsuccessfully.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/build-config-file-schema — Build steps; name; args; script; serviceAccount; allowFailure; allowExitCodes]
C.f8: Use the configured Pub/Sub artifact/event trigger with its configured payload bindings and filters to run the existing pipeline, then inspect actual stage results and resolved inputs for accepted and rejected fixtures.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/automating-builds/create-pubsub-triggers — Creating a Pub/Sub trigger; Substitution variables; Filters]
C.f9: The recovery function must distinguish the injected recoverable exception from unrelated failures, then retry from the verified artifact boundary and inspect that the retry and later required gates actually executed.   [sources: python_tutorial#errors.html — Handling Exceptions; Raising Exceptions]
C.f10: With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading accepts standard YAML tags, not arbitrary Python object constructors.   [sources: python_tutorial#https://pyyaml.org/wiki/PyYAMLDocumentation — Reference: safe_load; safe_dump]
C.f11: Bound the recovery fixture’s partial effects to declared named Cloud Storage artifact uploads and reconcile each declared output before repeating it: use blob.exists(), blob.reload() and its generation to retrieve the existing bytes, verify their expected content hash and required validation, then skip only the matching completed upload; create a missing output with blob.upload_from_filename(path, if_generation_match=0). If the create reports 412 Precondition Failed, re-read and verify the already-created output instead of overwriting it; conflicting content or failed validation stops recovery.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/python/docs/reference/storage/latest/google.cloud.storage.blob.Blob — exists; reload; generation; download_to_filename; upload_from_filename, google_mlops_pipelines#https://docs.cloud.google.com/storage/docs/request-preconditions — The 0 value in a generation-match precondition, python_tutorial#../library/hashlib.html — Usage, google_mlops_pipelines#Data and model validation]
C.f12: Inject failure after one declared output upload but before the remaining stage work; assert recovery retains the first output’s generation/hash, completes only missing uploads, runs the retried stage and downstream required gates, and reports failure for an invalid existing output. Invoke recovery again on the completed fixture and assert no extra output generations or uploads occur, while required validation is not bypassed.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/python/docs/reference/storage/latest/google.cloud.storage.blob.Blob — exists; reload; generation; download_to_filename; upload_from_filename, google_mlops_pipelines#https://docs.cloud.google.com/storage/docs/request-preconditions — The 0 value in a generation-match precondition, python_tutorial#../reference/simple_stmts.html — The assert statement, google_mlops_pipelines#Data and model validation]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Orchestrate Traceable Promotion.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.pipeline_artifact_dependencies, mle.dataset_quality_gate, mle.model_release_quality_gate. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a Python recovery function and its required imports for the supplied event-triggered pipeline. Inject the declared recoverable failure after output A uploads but before B, record and isolate the failure, reconcile declared outputs, and resume from a verified artifact boundary. Wire the function/test entry point into the assigned Cloud Build stage, round-trip its configuration through PyYAML, and exercise accepted and rejected fixtures through the configured Pub/Sub trigger without changing its bindings or filters.  SUCCESS: Recovery preserves A's generation and hash, creates only missing B, and verifies an existing output after a 412 response instead of overwriting it. Conflicting content, invalid artifacts, unrelated exceptions and rejected gates remain failures. Actual results show the retried stage and subsequent required gates executed. A second recovery invocation creates no additional uploads or generations while required validation remains enforced.
ASSESSMENT ANCHOR: identify_verified_recovery_boundary facts=['f1', 'f4']
ASSESSMENT ANCHOR: handle_only_declared_recoverable_failure facts=['f2', 'f9']
ASSESSMENT ANCHOR: preserve_required_gate_execution_and_failure facts=['f3', 'f6', 'f7']
ASSESSMENT ANCHOR: wire_and_verify_recovery_stage_configuration facts=['f5', 'f10']
ASSESSMENT ANCHOR: verify_triggered_stage_execution_and_resolved_inputs facts=['f8', 'f9']
ASSESSMENT ANCHOR: reconcile_partial_uploads_without_duplicate_effects facts=['f11', 'f12']

## SOURCE FACTS — D (mle.deployed_model_lineage_audit)   objective: Audit the served artifact’s registry, run, input, revision and configuration lineage.
D.f1: Lineage connects the served artifact to its training execution, resolved configuration, code revision and dataset snapshot.   [sources: google_mlops_pipelines#Metadata management]
D.f2: Resolve the deployed registry version and inspect its artifact source and run link.   [sources: mlflow_docs#ml/model-registry/workflow/ — Registering a Model; Fetching an MLflow Model from the Model Registry; Deploy and Organize Models]
D.f3: Retrieve that recorded run and compare its dataset/configuration/artifact evidence with the deployment and approval records.   [sources: mlflow_docs#ml/tracking/tracking-api/ — Starting and Managing Runs; Logging Data to Runs; Querying Runs Programmatically]
D.f4: Implement pairwise identity checks along the supplied lineage chain, and flag a missing link or mismatched identity rather than inferring provenance from similar names.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
D.f5: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
D.f6: Download the registry’s exact recorded artifact generation and verify its content identity against the lineage record.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/storage/docs/using-versioned-objects — Download noncurrent object versions]
D.f7: Inspect the recorded local code revision with git rev-parse --verify REVISION and git show REVISION, verifying that the referenced commit exists rather than only copying its string.   [sources: git_docs#git-rev-parse — --verify; git-show — DESCRIPTION]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Orchestrate Traceable Promotion.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.model_version_registration, mle.training_dataset_version, mle.training_environment_record, mle.experiment_metric_logging. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Implement a learner-defined Python function with learner-written dependency imports that audits the supplied deployment, registry, run, approval, dataset, configuration, artifact and code records. Resolve dictionary links, compare identities pairwise, download the exact recorded artifact generation, verify its content identity, and inspect the recorded revision in the supplied local repository. Return the verified lineage chain or an explicit missing or mismatched link.  SUCCESS: The function reports a verified chain only when the supplied identity links, downloaded artifact content and local commit checks agree. It explicitly reports missing links and identity mismatches without relying on similar names. Learner-written assert predicates pass for the declared valid, boundary and failure fixtures; a deliberately false predicate raises AssertionError during ordinary non-optimized execution.
ASSESSMENT ANCHOR: trace_deployed_version_to_recorded_training_evidence facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: identify_missing_or_mismatched_lineage_links facts=['f4']
ASSESSMENT ANCHOR: assert_declared_lineage_case_predicates facts=['f5']
ASSESSMENT ANCHOR: verify_exact_artifact_generation_and_content_identity facts=['f6']
ASSESSMENT ANCHOR: verify_recorded_local_code_commit facts=['f7']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute training and inference expenditure to workloads; Audit dataset, code, run and artifact lineage of a deployed model; Choose scheduled, new-data or investigated quality/drift retraining triggers; Configure actionable model and service alerts; Detect model-input data drift against a defined reference distribution; Distinguish data drift, concept drift and observed quality degradation; Gate a retrained candidate against the incumbent using validation evidence before controlled promotion; Invoke retraining with a versioned input snapshot from an authorized trigger; Measure production model quality when labels arrive; Monitor production input and prediction distributions; Prevent duplicate or overlapping retraining runs; Promote an approved registry version through accountable staged ML release gates; Recover a failed ML pipeline run without bypassing quality gates; Remove model-serving resources safely on an existing platform; Set an ML workload cost guardrail on an existing platform; Track ML workload compute and memory utilization; Triage a production regression to select data repair, rollback or gated retraining; Use an ML incident runbook for safe recovery on an existing p

## LESSON, in learner order

### s01 · explainer · Keep the boundary explicit
mle.tile.076_079 — 
(mechanism) Explicitly connect the artifact training produces to the one validation consumes. Correct stage order alone can still connect the wrong files. ⟦A:tb1⟧
(mechanism) Give reusable components explicit input/output artifacts across experiment and production environments. Record each stage’s consumed identities, execution parameters and produced identity, not just filenames. Represent dependencies as a dictionary and check each required upstream identity against its downstream reference. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Require relevant dataset or model validation before dependent execution. Assert declared valid, boundary and failure predicates; false predicates raise AssertionError in ordinary non-optimized execution. Wire the assigned Cloud Build entry point: name specifies the image, args or script the command. ⟦A.f4 A.f5 A.f6 A:tb3⟧
(example) Successful predecessor completion and artifact-identity agreement are separate checks: training output A must be the artifact validation actually consumes. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A:tb1 A:tb2 A:tb3⟧
[CODE python]
fixture_inputs = {'valid': {'data_validation': {'consumed': 'snapshot.A',
                               'parameters': {'contract': 'dataset_contract'},
                               'produced': 'validated.snapshot.A',
                               'validation_ok': True},
           'training': {'consumed': 'validated.snapshot.A',
                        'parameters': {'feature_scale': 5.0,
                                       'threshold': 0.4,
                                       'package': 'A'},
                        'produced': 'A'},
           'model_validation': {'consumed': 'A',
                                'parameters': {'rtol': 1e-07, 'atol': 1e-08},
                                'produced': 'validated.A',
                                'validation_ok': True}},
 'mismatch': {'data_validation': {'consumed': 'snapshot.A',
                                  'parameters': {'contract': 'dataset_contract'},
                                  'produced': 'validated.snapshot.A',
                                  'validation_ok': True},
              'training': {'consumed': 'validated.snapshot.A',
                           'parameters': {'feature_scale': 5.0,
                                          'threshold': 0.4,
                                          'package': 'A'},
                           'produced': 'A'},
              'model_validation': {'consumed': 'B',
                                   'parameters': {'rtol': 1e-07, 'atol': 1e-08},
                                   'produced': 'validated.A',
                                   'validation_ok': True}}}
  annotations: ['Inspect consumed/produced identities and parameters. A waitFor edge alone cannot establish the same artifact was consumed. Fixture inputs are not run results.']
[CODE python]
computed_panel = {'steps': [{'id': 'data_validation',
            'name': 'python:3.11',
            'args': ['python', 'learner.py', '${_CASE}'],
            'waitFor': ['-']},
           {'id': 'training',
            'name': 'python:3.11',
            'args': ['python', 'downstream_entry.py', '${_ARTIFACT}'],
            'waitFor': []},
           {'id': 'model_validation',
            'name': 'python:3.11',
            'args': ['python', 'learner.py', '${_CASE}', 'B'],
            'waitFor': []}],
 'substitutions': {'_SNAPSHOT': 'valid', '_CASE': 'valid', '_ARTIFACT': 'A'},
 'serviceAccount': 'projects/fixture-project/serviceAccounts/fixture-build@fixture-project.iam.gserviceaccount.com'}
  annotations: ['Supplied configuration (before fixture-only wiring)']
[CODE python]
computed_panel = {'source_asset_id': 'ws.pipeline_artifact_dependencies',
 'runtime': 'bounded local runtime_sim; not a cloud run',
 'fixture_execution_configuration': {'serviceAccount': 'projects/fixture-project/serviceAccounts/fixture-build@fixture-project.iam.gserviceaccount.com',
                                     'steps': [{'args': ['python',
                                                         'panel_worker.py',
                                                         'dependency',
                                                         'valid',
                                                         'data_validation',
                                                         'snapshot.A',
                                                         'validated.snapshot.A'],
                                                'id': 'data_validation',
                                                'name': 'python:3.11',
                                                'waitFor': ['-']},
                                               {'args': ['python',
                                                         'panel_worker.py',
                                                         'dependency',
                                                         'valid',
                                                         'training',
                                                         'validated.snapshot.A',
                                                         'A'],
                                                'id': 'training',
                                                'name': 'python:3.11',
                                                'waitFor': ['data_validation']},
                                               {'args': ['python',
                                                         'panel_worker.py',
                                                         'dependency',
                                                         'valid',
                                                         'model_validation',
                                                         'A',
                                                         'validated.A'],
                                                'id': 'model_validation',
                                                'name': 'python:3.11',
                                                'waitFor': ['training']}],
                                     'substitutions': {'_ARTIFACT': 'A',
                                                       '_CASE': 'valid',
                                                       '_SNAPSHOT': 'valid'}},
 'event': {'event_type': 'artifact_ready', 'case_id': 'valid', 'artifact_id': 'A'},
 'triggered': True,
 'resolved_inputs': {'_ARTIFACT': 'A', '_CASE': 'valid', '_SNAPSHOT': 'valid'},
 'steps': [{'id': 'data_validation',
            'name': 'python:3.11',
            'resolved_args': ['python',
                              'panel_worker.py',
                              'dependency',
                              'valid',
                              'data_validation',
                              'snapshot.A',
                              'validated.snapshot.A'],
            'waitFor': [],
            'status': 'SUCCESS',
            'exit_code': 0,
            'evidence': {'accepted': True,
                         'checks': {'resolved_args_agree_with_dictionary': True,
                                    'validation_ok': True},
                         'resolved_consumed_identity': 'snapshot.A',
                         'resolved_consumer': {'consumed': 'snapshot.A',
                                               'parameters': {'contract': 'dataset_contract'},
                                               'produced': 'validated.snapshot.A',
                                               'validation_ok': True},
                         'resolved_produced_identity': 'validated.snapshot.A',
                         'training_produced': 'A'}},
           {'id': 'training',
            'name': 'python:3.11',
            'resolved_args': ['python',
                              'panel_worker.py',
                              'dependency',
                              'valid',
                              'training',
                              'validated.snapshot.A',
                              'A'],
            'waitFor': ['data_validation'],
            'status': 'SUCCESS',
            'exit_code': 0,
            'evidence': {'accepted': True,
                         'checks': {'data_validation_output_equals_training_input': True,
                                    'resolved_args_agree_with_dictionary': True},
                         'resolved_consumed_identity': 'validated.snapshot.A',
                         'resolved_consumer': {'consumed': 'validated.snapshot.A',
                                               'parameters': {'feature_scale': 5.0,
                                                              'package': 'A',
                                                              'threshold': 0.4},
                                               'produced': 'A'},
                         'resolved_produced_identity': 'A',
                         'training_produced': 'A'}},
           {'id': 'model_validation',
            'name': 'python:3.11',
            'resolved_args': ['python',
                              'panel_worker.py',
                              'dependency',
                              'valid',
                              'model_validation',
                              'A',
                              'validated.A'],
            'waitFor': ['training'],
            'status': 'SUCCESS',
            'exit_code': 0,
            'evidence': {'accepted': True,
                         'checks': {'resolved_args_agree_with_dictionary': True,
                                    'training_output_equals_resolved_validation_input': True,
                                    'validation_ok': True},
                         'resolved_consumed_identity': 'A',
                         'resolved_consumer': {'consumed': 'A',
                                               'parameters': {'atol': 1e-08,
                                                              'rtol': 1e-07},
                                               'produced': 'validated.A',
                                               'validation_ok': True},
                         'resolved_produced_identity': 'validated.A',
                         'training_produced': 'A'}}]}
  annotations: ['Computed valid run: predecessor completion versus identity agreement']
[CODE python]
computed_panel = {'source_asset_id': 'ws.pipeline_artifact_dependencies',
 'runtime': 'bounded local runtime_sim; not a cloud run',
 'fixture_execution_configuration': {'serviceAccount': 'projects/fixture-project/serviceAccounts/fixture-build@fixture-project.iam.gserviceaccount.com',
                                     'steps': [{'args': ['python',
                                                         'panel_worker.py',
                                                         'dependency',
                                                         'mismatch',
                                                         'data_validation',
                                                         'snapshot.A',
                                                         'validated.snapshot.A'],
                                                'id': 'data_validation',
                                                'name': 'python:3.11',
                                                'waitFor': ['-']},
                                               {'args': ['python',
                                                         'panel_worker.py',
                                                         'dependency',
                                                         'mismatch',
                                                         'training',
                                                         'validated.snapshot.A',
                                                         'A'],
                                                'id': 'training',
                                                'name': 'python:3.11',
                                                'waitFor': ['data_validation']},
                                               {'args': ['python',
                                                         'panel_worker.py',
                                                         'dependency',
                                                         'mismatch',
                                                         'model_validation',
                                                         'B',
                                                         'validated.A'],
                                                'id': 'model_validation',
                                                'name': 'python:3.11',
                                                'waitFor': ['training']}],
                                     'substitutions': {'_ARTIFACT': 'A',
                                                       '_CASE': 'valid',
                                                       '_SNAPSHOT': 'valid'}},
 'event': {'event_type': 'artifact_ready', 'case_id': 'mismatch', 'artifact_id': 'B'},
 'triggered': True,
 'resolved_inputs': {'_ARTIFACT': 'B', '_CASE': 'mismatch', '_SNAPSHOT': 'valid'},
 'steps': [{'id': 'data_validation',
            'name': 'python:3.11',
            'resolved_args': ['python',
                              'panel_worker.py',
                              'dependency',
                              'mismatch',
                              'data_validation',
                              'snapshot.A',
                              'validated.snapshot.A'],
            'waitFor': [],
            'status': 'SUCCESS',
            'exit_code': 0,
            'evidence': {'accepted': True,
                         'checks': {'resolved_args_agree_with_dictionary': True,
                                    'validation_ok': True},
                         'resolved_consumed_identity': 'snapshot.A',
                         'resolved_consumer': {'consumed': 'snapshot.A',
                                               'parameters': {'contract': 'dataset_contract'},
                                               'produced': 'validated.snapshot.A',
                                               'validation_ok': True},
                         'resolved_produced_identity': 'validated.snapshot.A',
                         'training_produced': 'A'}},
           {'id': 'training',
            'name': 'python:3.11',
            'resolved_args': ['python',
                              'panel_worker.py',
                              'dependency',
                              'mismatch',
                              'training',
                              'validated.snapshot.A',
                              'A'],
            'waitFor': ['data_validation'],
            'status': 'SUCCESS',
            'exit_code': 0,
            'evidence': {'accepted': True,
                         'checks': {'data_validation_output_equals_training_input': True,
                                    'resolved_args_agree_with_dictionary': True},
                         'resolved_consumed_identity': 'validated.snapshot.A',
                         'resolved_consumer': {'consumed': 'validated.snapshot.A',
                                               'parameters': {'feature_scale': 5.0,
                                                              'package': 'A',
                                                              'threshold': 0.4},
                                               'produced': 'A'},
                         'resolved_produced_identity': 'A',
                         'training_produced': 'A'}},
           {'id': 'model_validation',
            'name': 'python:3.11',
            'resolved_args': ['python',
                              'panel_worker.py',
                              'dependency',
                              'mismatch',
                              'model_validation',
                              'B',
                              'validated.A'],
            'waitFor': ['training'],
            'status': 'FAILURE',
            'exit_code': 1,
            'evidence': {'accepted': False,
                         'checks': {'resolved_args_agree_with_dictionary': True,
                                    'training_output_equals_resolved_validation_input': False,
                                    'validation_ok': True},
                         'resolved_consumed_identity': 'B',
                         'resolved_consumer': {'consumed': 'B',
                                               'parameters': {'atol': 1e-08,
                                                              'rtol': 1e-07},
                                               'produced': 'validated.A',
                                               'validation_ok': True},
                         'resolved_produced_identity': 'validated.A',
                         'training_produced': 'A'}}]}
  annotations: ['Computed mismatch run: predecessor completion versus identity agreement']
(example) Successful predecessor completion and artifact-identity agreement are separate checks: training output A must be the artifact validation actually consumes. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A:tb1 A:tb2 A:tb3⟧

### s02 · explainer · Define artifact dependencies between ML pipeline stages
mle.tile.076_079 — 
(mechanism) Give stages IDs and waitFor their required predecessors: successful completion, not textual position, controls dependencies. Keep rejection fatal: no allowFailure or failing exit codes in allowExitCodes; rejected Python gates must exit unsuccessfully. Use the configured Pub/Sub trigger, payload bindings and filters; inspect stage results and resolved inputs for accepted and rejected fixtures. ⟦A.f7 A.f8 A.f9 A:tb4⟧
(mechanism) Bind consumer args/substitutions to the immutable identifier produced by its declared upstream stage. Inspect actual run inputs to verify this edge, not just stage order. With declared PyYAML, import yaml. Write mapping/list configuration with yaml.safe_dump(config, file_handle), reload with yaml.safe_load(file_handle), and inspect required resolved fields before runtime submission. Safe loading accepts standard YAML tags, not arbitrary Python object constructors. ⟦A.f10 A.f11 A:tb5⟧

### s03 · explainer · Define artifact dependencies between ML pipeline stages
mle.tile.076_079 — 
(example) If training produces A but validation arguments name B, flag the mismatch even if filenames look alike. Record input identities, parameters and outputs; bind consumers to the upstream immutable identifier and inspect resolved inputs. Require relevant validation, waitFor predecessors and fatal failure. Inspect accepted/rejected events under the existing trigger bindings and filters. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A.f9 A.f10 A.f11 A:tb6⟧
(mechanism) waitFor proves a completion dependency, not artifact agreement. Verify the consumed identity separately. ⟦A.f3 A.f7 A.f10 A:tb7⟧

### s04 · check · Inspect the gate evidence
mle.tile.076_079 — Use the supplied evidence to judge the required predicates and boundaries.

### s05 · hands_on · Verify define artifact dependencies between ml pipeline stages
mle.tile.076_079 — Implement the assigned function and configuration checks using the supplied fixtures; verify accepted and rejected behavior at the required fatal boundary.

### s06 · explainer · Promote an approved registry version through accountable staged ML release gates
mle.tile.076_079 — 
(mechanism) Carry one approved artifact across existing test and production boundaries. A completed build is not deployment permission: retain validation and separate authorization. ⟦B:tb1⟧
(mechanism) Read the approved registered name/version and run/artifact link. Continuous delivery checks test-environment compatibility, then model validation before production. Preserve the exact artifact’s validation verdict, including offline requirements and supplied staged evidence. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Stay within permitted identity and approval scope; record accountable authorization without changing policy. Record approval, registry version, artifact identity and per-stage gates. In Cloud Build, name selects the image and args or script the command for the assigned entry point. ⟦B.f4 B.f5 B.f6 B:tb3⟧
(example) Production requires staging quality and separate authorization for the same immutable artifact. Rejected authorization prevents production execution; credential values are not displayed. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B:tb1 B:tb2 B:tb3⟧
[CODE python]
computed_panel = {'steps': [{'id': 'compatibility',
            'name': 'python:3.11',
            'args': ['python', 'learner.py', '${_CASE}'],
            'waitFor': ['-']},
           {'id': 'staging_quality',
            'name': 'python:3.11',
            'args': ['python', 'learner.py', '${_CASE}'],
            'waitFor': []},
           {'id': 'authorization',
            'name': 'python:3.11',
            'args': ['python', 'learner.py', '${_CASE}'],
            'waitFor': []},
           {'id': 'production',
            'name': 'python:3.11',
            'args': ['python', 'downstream_entry.py', '${_ARTIFACT}'],
            'waitFor': [],
            'secretEnv': ['PROMOTION_TOKEN']}],
 'substitutions': {'_SNAPSHOT': 'valid', '_CASE': 'accepted', '_ARTIFACT': 'A'},
 'serviceAccount': 'projects/fixture-project/serviceAccounts/fixture-build@fixture-project.iam.gserviceaccount.com',
 'availableSecrets': {'secretManager': [{'versionName': 'projects/fixture-project/secrets/promotion-token/versions/1',
                                         'env': 'PROMOTION_TOKEN'}]}}
  annotations: ['Supplied staging/production configuration; secret references only']
[CODE python]
computed_panel = {'source_asset_id': 'ws.staged_ml_promotion',
 'runtime': 'bounded local runtime_sim; not a cloud run',
 'fixture_execution_configuration': {'availableSecrets': {'secretManager': [{'env': 'PROMOTION_TOKEN',
                                                                             'versionName': 'projects/fixture-project/secrets/promotion-token/versions/1'}]},
                                     'serviceAccount': 'projects/fixture-project/serviceAccounts/fixture-build@fixture-project.iam.gserviceaccount.com',
                                     'steps': [{'args': ['python',
                                                         'panel_worker.py',
                                                         'promotion',
                                                         'accepted',
                                                         'compatibility'],
                                                'id': 'compatibility',
                                                'name': 'python:3.11',
                                                'waitFor': ['-']},
                                               {'args': ['python',
                                                         'panel_worker.py',
                                                         'promotion',
                                                         'accepted',
                                                         'staging_quality'],
                                                'id': 'staging_quality',
                                                'name': 'python:3.11',
                                                'waitFor': ['compatibility']},
                                               {'args': ['python',
                                                         'panel_worker.py',
                                                         'promotion',
                                                         'accepted',
                                                         'authorization'],
                                                'id': 'authorization',
                                                'name': 'python:3.11',
                                                'waitFor': ['staging_quality']},
                                               {'args': ['python',
                                                         'downstream_entry.py',
                                                         '${_ARTIFACT}'],
                                                'id': 'production',
                                                'name': 'python:3.11',
                                                'secretEnv': ['PROMOTION_TOKEN'],
                                                'waitFor': ['authorization']}],
                                     'substitutions': {'_ARTIFACT': 'A',
                                                       '_CASE': 'accepted',
                                                       '_SNAPSHOT': 'valid'}},
 'event': {'event_type': 'artifact_ready', 'case_id': 'accepted', 'artifact_id': 'A'},
 'triggered': True,
 'resolved_inputs': {'_ARTIFACT': 'A', '_CASE': 'accepted', '_SNAPSHOT': 'valid'},
 'steps': [{'id': 'compatibility',
            'name': 'python:3.11',
            'resolved_args': ['python',
                              'panel_worker.py',
                              'promotion',
                              'accepted',
                              'compatibility'],
            'waitFor': [],
            'status': 'SUCCESS',
            'exit_code': 0,
            'evidence': {'accepted': True,
                         'artifact_id': 'A',
                         'checks': {'compatibility': True, 'offline_validation': True},
                         'registry_version': '1',
                         'run_id': 'run.A'}},
           {'id': 'staging_quality',
            'name': 'python:3.11',
            'resolved_args': ['python',
                              'panel_worker.py',
                              'promotion',
                              'accepted',
                              'staging_quality'],
            'waitFor': ['compatibility'],
            'status': 'SUCCESS',
            'exit_code': 0,
            'evidence': {'accepted': True,
                         'artifact_id': 'A',
                         'checks': {'staged_validation': True,
                                    'unchanged_artifact': True},
                         'registry_version': '1',
                         'run_id': 'run.A'}},
           {'id': 'authorization',
            'name': 'python:3.11',
            'resolved_args': ['python',
                              'panel_worker.py',
                              'promotion',
                              'accepted',
                              'authorization'],
            'waitFor': ['staging_quality'],
            'status': 'SUCCESS',
            'exit_code': 0,
            'evidence': {'accepted': True,
                         'artifact_id': 'A',
                         'checks': {'accountable_identity': True,
                                    'approval_artifact': True,
                                    'approval_version': True,
                                    'authorized': True,
                                    'scoped_artifact': True},
                         'registry_version': '1',
                         'run_id': 'run.A'}},
           {'id': 'production',
            'name': 'python:3.11',
            'resolved_args': ['python', 'downstream_entry.py', 'A'],
            'waitFor': ['authorization'],
            'status': 'SUCCESS',
            'exit_code': 0}],
 'unchanged_immutable_artifact': {'artifact_id': 'A',
                                  'artifact_source': 'gs://fixture-artifacts/A.txt',
                                  'generation': 1,
                                  'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6'},
 'promotion_record': {'approval': {'approval_id': 'approval.A',
                                   'registry_version': '1',
                                   'artifact_id': 'A',
                                   'authorized': True,
                                   'accountable_identity': 'fixture-promoter'},
                      'registry_version': '1',
                      'run_id': 'run.A',
                      'artifact_id': 'A',
                      'accountable_identity': 'fixture-promoter',
                      'per_stage_results': {'compatibility': 'SUCCESS',
                                            'staging_quality': 'SUCCESS',
                                            'authorization': 'SUCCESS',
                                            'production': 'SUCCESS'}},
 'non_disclosure': {'real_credentials_supplied': False,
                    'credential_values_displayed': False,
                    'check_pass': True}}
  annotations: ['Computed accepted result; parsed fixture execution fields']
[CODE python]
computed_panel = {'source_asset_id': 'ws.staged_ml_promotion',
 'runtime': 'bounded local runtime_sim; not a cloud run',
 'fixture_execution_configuration': {'availableSecrets': {'secretManager': [{'env': 'PROMOTION_TOKEN',
                                                                             'versionName': 'projects/fixture-project/secrets/promotion-token/versions/1'}]},
                                     'serviceAccount': 'projects/fixture-project/serviceAccounts/fixture-build@fixture-project.iam.gserviceaccount.com',
                                     'steps': [{'args': ['python',
                                                         'panel_worker.py',
                                                         'promotion',
                                                         'unauthorized',
                                                         'compatibility'],
                                                'id': 'compatibility',
                                                'name': 'python:3.11',
                                                'waitFor': ['-']},
                                               {'args': ['python',
                                                         'panel_worker.py',
                                                         'promotion',
                                                         'unauthorized',
                                                         'staging_quality'],
                                                'id': 'staging_quality',
                                                'name': 'python:3.11',
                                                'waitFor': ['compatibility']},
                                               {'args': ['python',
                                                         'panel_worker.py',
                                                         'promotion',
                                                         'unauthorized',
                                                         'authorization'],
                                                'id': 'authorization',
                                                'name': 'python:3.11',
                                                'waitFor': ['staging_quality']},
                                               {'args': ['python',
                                                         'downstream_entry.py',
                                                         '${_ARTIFACT}'],
                                                'id': 'production',
                                                'name': 'python:3.11',
                                                'secretEnv': ['PROMOTION_TOKEN'],
                                                'waitFor': ['authorization']}],
                                     'substitutions': {'_ARTIFACT': 'A',
                                                       '_CASE': 'accepted',
                                                       '_SNAPSHOT': 'valid'}},
 'event': {'event_type': 'artifact_ready',
           'case_id': 'unauthorized',
           'artifact_id': 'A'},
 'triggered': True,
 'resolved_inputs': {'_ARTIFACT': 'A', '_CASE': 'unauthorized', '_SNAPSHOT': 'valid'},
 'steps': [{'id': 'compatibility',
            'name': 'python:3.11',
            'resolved_args': ['python',
                              'panel_worker.py',
                              'promotion',
                              'unauthorized',
                              'compatibility'],
            'waitFor': [],
            'status': 'SUCCESS',
            'exit_code': 0,
            'evidence': {'accepted': True,
                         'artifact_id': 'A',
                         'checks': {'compatibility': True, 'offline_validation': True},
                         'registry_version': '1',
                         'run_id': 'run.A'}},
           {'id': 'staging_quality',
            'name': 'python:3.11',
            'resolved_args': ['python',
                              'panel_worker.py',
                              'promotion',
                              'unauthorized',
                              'staging_quality'],
            'waitFor': ['compatibility'],
            'status': 'SUCCESS',
            'exit_code': 0,
            'evidence': {'accepted': True,
                         'artifact_id': 'A',
                         'checks': {'staged_validation': True,
                                    'unchanged_artifact': True},
                         'registry_version': '1',
                         'run_id': 'run.A'}},
           {'id': 'authorization',
            'name': 'python:3.11',
            'resolved_args': ['python',
                              'panel_worker.py',
                              'promotion',
                              'unauthorized',
                              'authorization'],
            'waitFor': ['staging_quality'],
            'status': 'FAILURE',
            'exit_code': 1,
            'evidence': {'accepted': False,
                         'artifact_id': 'A',
                         'checks': {'accountable_identity': True,
                                    'approval_artifact': True,
                                    'approval_version': True,
                                    'authorized': False,
                                    'scoped_artifact': True},
                         'registry_version': '1',
                         'run_id': 'run.A'}},
           {'id': 'production',
            'name': 'python:3.11',
            'resolved_args': ['python', 'downstream_entry.py', 'A'],
            'waitFor': ['authorization'],
            'status': 'NOT_STARTED',
            'exit_code': None}],
 'unchanged_immutable_artifact': {'artifact_id': 'A',
                                  'artifact_source': 'gs://fixture-artifacts/A.txt',
                                  'generation': 1,
                                  'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6'},
 'promotion_record': None,
 'non_disclosure': {'real_credentials_supplied': False,
                    'credential_values_displayed': False,
                    'check_pass': True}}
  annotations: ['Computed unauthorized result; parsed fixture execution fields']
(example) Production requires staging quality and separate authorization for the same immutable artifact. Rejected authorization prevents production execution; credential values are not displayed. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B:tb1 B:tb2 B:tb3⟧

### s07 · explainer · Promote an approved registry version through accountable staged ML release gates
mle.tile.076_079 — 
(mechanism) Give stages IDs and waitFor their required predecessors: successful completion, not textual position, controls dependencies. Keep rejection fatal: no allowFailure or failing exit codes in allowExitCodes; rejected Python gates must exit unsuccessfully. Use the configured Pub/Sub trigger, payload bindings and filters; inspect stage results and resolved inputs for accepted and rejected fixtures. ⟦B.f7 B.f8 B.f9 B:tb4⟧
(mechanism) Bind approved Secret Manager version references through availableSecrets.secretManager, exposing them only to the needed step through secretEnv. YAML stores references, not values. Use the authorized build/step identity and separate promotion authorization. Check captured output for non-disclosure; never echo or serialize runtime credentials. ⟦B.f10 B.f11 B.f12 B:tb5⟧

### s08 · explainer · Promote an approved registry version through accountable staged ML release gates
mle.tile.076_079 — 
(mechanism) Edit and parse existing staging/production YAML: production depends on staging quality and authorization for the identical immutable artifact. Test unauthorized promotion and inspect that production did not execute. With declared PyYAML, import yaml. Write mapping/list configuration with yaml.safe_dump(config, file_handle), reload with yaml.safe_load(file_handle), and inspect required resolved fields before runtime submission. Safe loading accepts standard YAML tags, not arbitrary Python object constructors. ⟦B.f13 B.f14 B:tb6⟧

### s09 · explainer · Promote an approved registry version through accountable staged ML release gates
mle.tile.076_079 — 
(example) Read the approved version and run/artifact link. Make production depend on staging quality and authorization for that same artifact. Record offline/staged evidence, approval and stage results. Use the approved identity and step-scoped secret references. Inspect unauthorized-event results, resolved inputs and output non-disclosure; keep rejection fatal. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 B.f9 B.f10 B.f11 B.f12 B.f13 B.f14 B:tb7⟧
(mechanism) Passing staging for A cannot approve B. Training or staging success is not promotion authorization, and credentials must not enter the promotion record. ⟦B.f3 B.f4 B.f11 B.f12 B.f13 B:tb8⟧

### s10 · check · Inspect the gate evidence
mle.tile.076_079 — Use the supplied evidence to judge the required predicates and boundaries.

### s11 · hands_on · Verify promote an approved registry version through accountable staged ml release gates
mle.tile.076_079 — Implement the assigned function and configuration checks using the supplied fixtures; verify accepted and rejected behavior at the required fatal boundary.

### s12 · explainer · Recover a failed ML pipeline run without bypassing quality gates
mle.tile.076_079 — 
(mechanism) Resume at a verified artifact boundary after the declared recoverable failure. Preserve required quality decisions instead of turning retry into permission to continue. ⟦C:tb1⟧
(mechanism) Locate the failed stage and affected artifacts, preserving identities of completed required stages. Catch only the declared recoverable error with try/except, record it, and apply only the supplied recovery action. After repair, rerun the affected required check; stop if it still fails. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) Reuse upstream output only when its recorded identity and required validation remain valid for the resumed stage. Wire the assigned Cloud Build entry point using name for the image and args or script for the command. Set IDs and waitFor required predecessors: successful completion, not textual location, controls dependencies. ⟦C.f4 C.f5 C.f6 C:tb3⟧
[BEFORE_AFTER] Recovery preserves verified A, creates only missing B and executes required gates. A second invocation adds no uploads or generations while retaining validation. Invalid existing output stops recovery.
  before:
[CODE python]
computed_panel = {'source_asset_id': 'ws.pipeline_failure_recovery',
 'runtime': 'bounded local runtime_sim; not a cloud run',
 'event': {'event_type': 'artifact_ready', 'case_id': 'accepted', 'artifact_id': 'A'},
 'triggered': True,
 'resolved_inputs': {'_ARTIFACT': 'A', '_CASE': 'accepted', '_SNAPSHOT': 'valid'},
 'steps': [{'id': 'recovery',
            'name': 'python:3.11',
            'resolved_args': ['python',
                              'panel_worker.py',
                              'recovery',
                              'accepted',
                              'injection'],
            'waitFor': [],
            'status': 'FAILURE',
            'exit_code': 1,
            'evidence': {'accepted': False,
                         'after': {'A': {'exists': True,
                                         'generation': 1,
                                         'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                         'validation_ok': True},
                                   'B': {'exists': False,
                                         'generation': None,
                                         'sha256': None,
                                         'validation_ok': False}},
                         'before': {'A': {'exists': True,
                                          'generation': 1,
                                          'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                          'validation_ok': True},
                                    'B': {'exists': False,
                                          'generation': None,
                                          'sha256': None,
                                          'validation_ok': False}},
                         'failure': 'RecoverableFailure: after A upload before B',
                         'new_uploads': [],
                         'required_gate_ok': True,
                         'upload_change': 0,
                         'upload_count': 1}},
           {'id': 'required_validation',
            'name': 'python:3.11',
            'resolved_args': ['python',
                              'panel_worker.py',
                              'recovery',
                              'accepted',
                              'validation'],
            'waitFor': ['recovery'],
            'status': 'NOT_STARTED',
            'exit_code': None},
           {'id': 'promotion',
            'name': 'python:3.11',
            'resolved_args': ['python', 'downstream_entry.py', 'A'],
            'waitFor': ['required_validation'],
            'status': 'NOT_STARTED',
            'exit_code': None}]}
  annotations: ['Observed injection boundary']
  after:
[CODE python]
computed_panel = {'source_asset_id': 'ws.pipeline_failure_recovery',
 'runtime': 'bounded local runtime_sim; not a cloud run',
 'event': {'event_type': 'artifact_ready', 'case_id': 'accepted', 'artifact_id': 'A'},
 'triggered': True,
 'resolved_inputs': {'_ARTIFACT': 'A', '_CASE': 'accepted', '_SNAPSHOT': 'valid'},
 'steps': [{'id': 'recovery',
            'name': 'python:3.11',
            'resolved_args': ['python',
                              'panel_worker.py',
                              'recovery',
                              'accepted',
                              'recovery'],
            'waitFor': [],
            'status': 'SUCCESS',
            'exit_code': 0,
            'evidence': {'accepted': True,
                         'after': {'A': {'exists': True,
                                         'generation': 1,
                                         'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                         'validation_ok': True},
                                   'B': {'exists': True,
                                         'generation': 1,
                                         'sha256': '6d5f5cbc73990d86a040e72f9e6d1cad2cb36297b10887e5444900c7286f634a',
                                         'validation_ok': True}},
                         'before': {'A': {'exists': True,
                                          'generation': 1,
                                          'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                          'validation_ok': True},
                                    'B': {'exists': False,
                                          'generation': None,
                                          'sha256': None,
                                          'validation_ok': False}},
                         'failure': None,
                         'new_uploads': ['B'],
                         'required_gate_ok': True,
                         'upload_change': 1,
                         'upload_count': 2}},
           {'id': 'required_validation',
            'name': 'python:3.11',
            'resolved_args': ['python',
                              'panel_worker.py',
                              'recovery',
                              'accepted',
                              'validation'],
            'waitFor': ['recovery'],
            'status': 'SUCCESS',
            'exit_code': 0,
            'evidence': {'accepted': True,
                         'after': {'A': {'exists': True,
                                         'generation': 1,
                                         'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                         'validation_ok': True},
                                   'B': {'exists': True,
                                         'generation': 1,
                                         'sha256': '6d5f5cbc73990d86a040e72f9e6d1cad2cb36297b10887e5444900c7286f634a',
                                         'validation_ok': True}},
                         'before': {'A': {'exists': True,
                                          'generation': 1,
                                          'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                          'validation_ok': True},
                                    'B': {'exists': True,
                                          'generation': 1,
                                          'sha256': '6d5f5cbc73990d86a040e72f9e6d1cad2cb36297b10887e5444900c7286f634a',
                                          'validation_ok': True}},
                         'failure': None,
                         'new_uploads': [],
                         'required_gate_ok': True,
                         'upload_change': 0,
                         'upload_count': 2}},
           {'id': 'promotion',
            'name': 'python:3.11',
            'resolved_args': ['python', 'downstream_entry.py', 'A'],
            'waitFor': ['required_validation'],
            'status': 'SUCCESS',
            'exit_code': 0}]}
  annotations: ['Observed recovered execution']
[CODE python]
computed_panel = {'source_asset_id': 'ws.pipeline_failure_recovery',
 'runtime': 'bounded local runtime_sim; not a cloud run',
 'event': {'event_type': 'artifact_ready', 'case_id': 'accepted', 'artifact_id': 'A'},
 'triggered': True,
 'resolved_inputs': {'_ARTIFACT': 'A', '_CASE': 'accepted', '_SNAPSHOT': 'valid'},
 'steps': [{'id': 'recovery',
            'name': 'python:3.11',
            'resolved_args': ['python',
                              'panel_worker.py',
                              'recovery',
                              'accepted',
                              'recovery'],
            'waitFor': [],
            'status': 'SUCCESS',
            'exit_code': 0,
            'evidence': {'accepted': True,
                         'after': {'A': {'exists': True,
                                         'generation': 1,
                                         'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                         'validation_ok': True},
                                   'B': {'exists': True,
                                         'generation': 1,
                                         'sha256': '6d5f5cbc73990d86a040e72f9e6d1cad2cb36297b10887e5444900c7286f634a',
                                         'validation_ok': True}},
                         'before': {'A': {'exists': True,
                                          'generation': 1,
                                          'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                          'validation_ok': True},
                                    'B': {'exists': True,
                                          'generation': 1,
                                          'sha256': '6d5f5cbc73990d86a040e72f9e6d1cad2cb36297b10887e5444900c7286f634a',
                                          'validation_ok': True}},
                         'failure': None,
                         'new_uploads': [],
                         'required_gate_ok': True,
                         'upload_change': 0,
                         'upload_count': 2}},
           {'id': 'required_validation',
            'name': 'python:3.11',
            'resolved_args': ['python',
                              'panel_worker.py',
                              'recovery',
                              'accepted',
                              'validation'],
            'waitFor': ['recovery'],
            'status': 'SUCCESS',
            'exit_code': 0,
            'evidence': {'accepted': True,
                         'after': {'A': {'exists': True,
                                         'generation': 1,
                                         'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                         'validation_ok': True},
                                   'B': {'exists': True,
                                         'generation': 1,
                                         'sha256': '6d5f5cbc73990d86a040e72f9e6d1cad2cb36297b10887e5444900c7286f634a',
                                         'validation_ok': True}},
                         'before': {'A': {'exists': True,
                                          'generation': 1,
                                          'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                          'validation_ok': True},
                                    'B': {'exists': True,
                                          'generation': 1,
                                          'sha256': '6d5f5cbc73990d86a040e72f9e6d1cad2cb36297b10887e5444900c7286f634a',
                                          'validation_ok': True}},
                         'failure': None,
                         'new_uploads': [],
                         'required_gate_ok': True,
                         'upload_change': 0,
                         'upload_count': 2}},
           {'id': 'promotion',
            'name': 'python:3.11',
            'resolved_args': ['python', 'downstream_entry.py', 'A'],
            'waitFor': ['required_validation'],
            'status': 'SUCCESS',
            'exit_code': 0}]}
  annotations: ['Second invocation: retained validation']
[CODE python]
computed_panel = {'source_asset_id': 'ws.pipeline_failure_recovery',
 'runtime': 'bounded local runtime_sim; not a cloud run',
 'event': {'event_type': 'artifact_ready',
           'case_id': 'invalid_existing',
           'artifact_id': 'A'},
 'triggered': True,
 'resolved_inputs': {'_ARTIFACT': 'A',
                     '_CASE': 'invalid_existing',
                     '_SNAPSHOT': 'valid'},
 'steps': [{'id': 'recovery',
            'name': 'python:3.11',
            'resolved_args': ['python',
                              'panel_worker.py',
                              'recovery',
                              'invalid_existing',
                              'recovery'],
            'waitFor': [],
            'status': 'FAILURE',
            'exit_code': 1,
            'evidence': {'accepted': False,
                         'after': {'A': {'exists': True,
                                         'generation': 1,
                                         'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                         'validation_ok': False},
                                   'B': {'exists': False,
                                         'generation': None,
                                         'sha256': None,
                                         'validation_ok': False}},
                         'before': {'A': {'exists': True,
                                          'generation': 1,
                                          'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                          'validation_ok': False},
                                    'B': {'exists': False,
                                          'generation': None,
                                          'sha256': None,
                                          'validation_ok': False}},
                         'failure': 'invalid existing output: A',
                         'new_uploads': [],
                         'required_gate_ok': True,
                         'upload_change': 0,
                         'upload_count': 1}},
           {'id': 'required_validation',
            'name': 'python:3.11',
            'resolved_args': ['python',
                              'panel_worker.py',
                              'recovery',
                              'invalid_existing',
                              'validation'],
            'waitFor': ['recovery'],
            'status': 'NOT_STARTED',
            'exit_code': None},
           {'id': 'promotion',
            'name': 'python:3.11',
            'resolved_args': ['python', 'downstream_entry.py', 'A'],
            'waitFor': ['required_validation'],
            'status': 'NOT_STARTED',
            'exit_code': None}]}
  annotations: ['Invalid-existing-output rejection']
[CODE python]
computed_panel = {'source_asset_id': 'ws.pipeline_failure_recovery',
 'runtime': 'bounded local runtime_sim; not a cloud run',
 'event': {'event_type': 'artifact_ready',
           'case_id': 'rejected_gate',
           'artifact_id': 'A'},
 'triggered': True,
 'resolved_inputs': {'_ARTIFACT': 'A', '_CASE': 'rejected_gate', '_SNAPSHOT': 'valid'},
 'steps': [{'id': 'recovery',
            'name': 'python:3.11',
            'resolved_args': ['python',
                              'panel_worker.py',
                              'recovery',
                              'rejected_gate',
                              'recovery'],
            'waitFor': [],
            'status': 'SUCCESS',
            'exit_code': 0,
            'evidence': {'accepted': True,
                         'after': {'A': {'exists': True,
                                         'generation': 1,
                                         'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                         'validation_ok': True},
                                   'B': {'exists': True,
                                         'generation': 1,
                                         'sha256': '6d5f5cbc73990d86a040e72f9e6d1cad2cb36297b10887e5444900c7286f634a',
                                         'validation_ok': True}},
                         'before': {'A': {'exists': True,
                                          'generation': 1,
                                          'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                          'validation_ok': True},
                                    'B': {'exists': False,
                                          'generation': None,
                                          'sha256': None,
                                          'validation_ok': False}},
                         'failure': None,
                         'new_uploads': ['B'],
                         'required_gate_ok': False,
                         'upload_change': 1,
                         'upload_count': 2}},
           {'id': 'required_validation',
            'name': 'python:3.11',
            'resolved_args': ['python',
                              'panel_worker.py',
                              'recovery',
                              'rejected_gate',
                              'validation'],
            'waitFor': ['recovery'],
            'status': 'FAILURE',
            'exit_code': 1,
            'evidence': {'accepted': False,
                         'after': {'A': {'exists': True,
                                         'generation': 1,
                                         'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                         'validation_ok': True},
                                   'B': {'exists': True,
                                         'generation': 1,
                                         'sha256': '6d5f5cbc73990d86a040e72f9e6d1cad2cb36297b10887e5444900c7286f634a',
                                         'validation_ok': True}},
                         'before': {'A': {'exists': True,
                                          'generation': 1,
                                          'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                          'validation_ok': True},
                                    'B': {'exists': True,
                                          'generation': 1,
                                          'sha256': '6d5f5cbc73990d86a040e72f9e6d1cad2cb36297b10887e5444900c7286f634a',
                                          'validation_ok': True}},
                         'failure': None,
                         'new_uploads': [],
                         'required_gate_ok': False,
                         'upload_change': 0,
                         'upload_count': 2}},
           {'id': 'promotion',
            'name': 'python:3.11',
            'resolved_args': ['python', 'downstream_entry.py', 'A'],
            'waitFor': ['required_validation'],
            'status': 'NOT_STARTED',
            'exit_code': None}]}
  annotations: ['Rejected required downstream gate']

### s13 · explainer · Recover a failed ML pipeline run without bypassing quality gates
mle.tile.076_079 — 
(mechanism) Keep gate failures fatal: no allowFailure or allowed failing exit codes; rejected Python gates exit unsuccessfully. Use the configured Pub/Sub trigger, payload bindings and filters; inspect stage results and resolved inputs for accepted and rejected fixtures. Distinguish the injected recoverable exception from unrelated failures. Retry at the verified boundary and inspect execution of the retry and later required gates. ⟦C.f7 C.f8 C.f9 C:tb4⟧

### s14 · explainer · Recover a failed ML pipeline run without bypassing quality gates
mle.tile.076_079 — 
(mechanism) With declared PyYAML, import yaml. Write mapping/list configuration with yaml.safe_dump(config, file_handle), reload with yaml.safe_load(file_handle), and inspect required resolved fields before runtime submission. Safe loading accepts standard YAML tags, not arbitrary Python object constructors. ⟦C.f10 C.f11 C.f12 C:tb5⟧
(mechanism) Reconcile only declared named uploads. Use blob.exists(), blob.reload() and generation to retrieve bytes; verify expected hash and required validation. Skip only verified completed uploads. Create missing output with blob.upload_from_filename(path, if_generation_match=0). On 412, re-read and verify, never overwrite; conflicts or failed validation stop recovery. ⟦C.f10 C.f11 C.f12 C:tb5⟧
(mechanism) Inject failure after one upload; assert its generation/hash is retained, only missing outputs complete, retry and later gates run, and invalid existing output fails. Repeat recovery: no extra uploads/generations, with required validation still enforced. ⟦C.f10 C.f11 C.f12 C:tb5⟧

### s15 · explainer · Recover a failed ML pipeline run without bypassing quality gates
mle.tile.076_079 — 
(example) After failure between A and B uploads, verify A’s generation, bytes, hash and validation before reuse. Create only missing B with if_generation_match=0; on 412 re-read and verify, never overwrite. Conflict or invalid content stops recovery. Retry the stage and required gates; repeat recovery with no extra uploads/generations while revalidating. Catch only the declared recoverable exception. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C.f7 C.f8 C.f9 C.f10 C.f11 C.f12 C:tb6⟧
(mechanism) Recovery is not ignore-and-continue. Reuse requires identity and validation; retry must not overwrite conflicting content or bypass gates. ⟦C.f3 C.f4 C.f9 C.f11 C.f12 C:tb7⟧

### s16 · check · Inspect the gate evidence
mle.tile.076_079 — Use the supplied evidence to judge the required predicates and boundaries.

### s17 · hands_on · Verify recover a failed ml pipeline run without bypassing quality gates
mle.tile.076_079 — Implement the assigned function and configuration checks using the supplied fixtures; verify accepted and rejected behavior at the required fatal boundary.

### s18 · explainer · Audit dataset, code, run and artifact lineage of a deployed model
mle.tile.076_079 — 
(mechanism) Trace the served model through supplied records to training, code and data. Similar record names do not establish identity links. ⟦D:tb1⟧
(mechanism) Lineage connects the served artifact to training execution, resolved configuration, code revision and dataset snapshot. Resolve the deployed registry version’s artifact source and run link. Retrieve that run and compare dataset, configuration and artifact evidence with deployment and approval records. ⟦D.f1 D.f2 D.f3 D:tb2⟧
(mechanism) Check the supplied lineage chain pair by pair; flag missing or mismatched identities instead of inferring provenance from names. Assert declared valid, boundary and failure predicates; false predicates raise AssertionError in ordinary non-optimized execution. Download the registry’s exact recorded artifact generation and verify content identity against the lineage record. ⟦D.f4 D.f5 D.f6 D:tb3⟧
(mechanism) Inspect the recorded local revision with git rev-parse --verify REVISION and git show REVISION. Confirm the commit exists rather than merely copying its string. ⟦D.f7 D:tb4⟧
(example) Recorded names are inputs, not proof. The audit verifies each identity edge, exact artifact content and the referenced local commit, and reports every missing or mismatched link. ⟦D.f1 D.f2 D.f3 D.f4 D.f5 D.f6 D.f7 D:tb1 D:tb2 D:tb3 D:tb4⟧
[CODE python]
computed_panel = {'valid': {'records': {'deployment': {'deployment_id': 'deployment.A',
                                      'registry_version': '1',
                                      'artifact_id': 'A'},
                       'approval': {'approval_id': 'approval.A',
                                    'registry_version': '1',
                                    'artifact_id': 'A',
                                    'authorized': True,
                                    'accountable_identity': 'fixture-promoter'}},
           'pairwise_verdicts': {'deployment_to_registry': True,
                                 'approval_to_deployment': True}},
 'approval_A_deployment_B': {'records': {'deployment': {'deployment_id': 'deployment.A',
                                                        'registry_version': '1',
                                                        'artifact_id': 'B'},
                                         'approval': {'approval_id': 'approval.A',
                                                      'registry_version': '1',
                                                      'artifact_id': 'A',
                                                      'authorized': True,
                                                      'accountable_identity': 'fixture-promoter'}},
                             'pairwise_verdicts': {'deployment_to_registry': False,
                                                   'approval_to_deployment': False}}}
  annotations: ['Deployment / approval — deployment artifact differs; approval remains unchanged']
[CODE python]
computed_panel = {'valid': {'records': {'registry': {'1': {'model_name': 'fixture_model',
                                          'version': '1',
                                          'artifact_id': 'A',
                                          'artifact_source': 'gs://fixture-artifacts/A.txt',
                                          'generation': 1,
                                          'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                          'run_id': 'run.A'}},
                       'runs': {'run.A': {'run_id': 'run.A',
                                          'artifact_id': 'A',
                                          'artifact_sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                          'dataset_id': 'snapshot.A',
                                          'configuration_id': 'config.A',
                                          'code_id': 'code.A'}}},
           'pairwise_verdicts': {'registry_to_run': True,
                                 'registry_to_artifact': True,
                                 'run_to_artifact': True}},
 'approval_A_deployment_B': {'records': {'registry': {'1': {'model_name': 'fixture_model',
                                                            'version': '1',
                                                            'artifact_id': 'A',
                                                            'artifact_source': 'gs://fixture-artifacts/A.txt',
                                                            'generation': 1,
                                                            'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                                            'run_id': 'run.A'}},
                                         'runs': {'run.A': {'run_id': 'run.A',
                                                            'artifact_id': 'A',
                                                            'artifact_sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                                            'dataset_id': 'snapshot.A',
                                                            'configuration_id': 'config.A',
                                                            'code_id': 'code.A'}}},
                             'pairwise_verdicts': {'registry_to_run': True,
                                                   'registry_to_artifact': True,
                                                   'run_to_artifact': True}}}
  annotations: ['Registry / run — inspect exact identities, not similar names']
[CODE python]
computed_panel = {'valid': {'records': {'datasets': {'snapshot.A': {'sha256': '94d86c2f748dbd3ec7fb8e27dded66533bde22a109a97d9fde2191d96b831d61',
                                                   'file': 'dataset.csv'}},
                       'configurations': {'config.A': {'sha256': '75bc2039e3a69484813ab3b30218dba912ae9ecc3f03a7087a068915072e8e4a',
                                                       'resolved': {'feature_scale': 5.0,
                                                                    'threshold': 0.4,
                                                                    'package': 'A'}}}},
           'pairwise_verdicts': {'run_to_dataset': True, 'run_to_configuration': True},
           'computed_evidence': {'dataset': {'expected_sha256': '94d86c2f748dbd3ec7fb8e27dded66533bde22a109a97d9fde2191d96b831d61',
                                             'id': 'snapshot.A',
                                             'observed_sha256': '94d86c2f748dbd3ec7fb8e27dded66533bde22a109a97d9fde2191d96b831d61'},
                                 'configuration': {'expected_sha256': '75bc2039e3a69484813ab3b30218dba912ae9ecc3f03a7087a068915072e8e4a',
                                                   'id': 'config.A',
                                                   'observed_sha256': '75bc2039e3a69484813ab3b30218dba912ae9ecc3f03a7087a068915072e8e4a'}}},
 'approval_A_deployment_B': {'records': {'datasets': {'snapshot.A': {'sha256': '94d86c2f748dbd3ec7fb8e27dded66533bde22a109a97d9fde2191d96b831d61',
                                                                     'file': 'dataset.csv'}},
                                         'configurations': {'config.A': {'sha256': '75bc2039e3a69484813ab3b30218dba912ae9ecc3f03a7087a068915072e8e4a',
                                                                         'resolved': {'feature_scale': 5.0,
                                                                                      'threshold': 0.4,
                                                                                      'package': 'A'}}}},
                             'pairwise_verdicts': {'run_to_dataset': True,
                                                   'run_to_configuration': True},
                             'computed_evidence': {'dataset': {'expected_sha256': '94d86c2f748dbd3ec7fb8e27dded66533bde22a109a97d9fde2191d96b831d61',
                                                               'id': 'snapshot.A',
                                                               'observed_sha256': '94d86c2f748dbd3ec7fb8e27dded66533bde22a109a97d9fde2191d96b831d61'},
                                                   'configuration': {'expected_sha256': '75bc2039e3a69484813ab3b30218dba912ae9ecc3f03a7087a068915072e8e4a',
                                                                     'id': 'config.A',
                                                                     'observed_sha256': '75bc2039e3a69484813ab3b30218dba912ae9ecc3f03a7087a068915072e8e4a'}}}}
  annotations: ['Dataset / configuration — inspect exact identities, not similar names']
[CODE python]
computed_panel = {'valid': {'records': {'artifacts': {'A': {'artifact_id': 'A',
                                           'uri': 'gs://fixture-artifacts/A.txt',
                                           'generation': 1,
                                           'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                           'validation_ok': True},
                                     'B': {'artifact_id': 'B',
                                           'uri': 'gs://fixture-artifacts/B.txt',
                                           'generation': 1,
                                           'sha256': '6d5f5cbc73990d86a040e72f9e6d1cad2cb36297b10887e5444900c7286f634a',
                                           'validation_ok': True}},
                       'code': {'code.A': {'revision': 'da89ee877040e427fd3de821dffbdc0abd82017b',
                                           'repository': 'local_repo'}}},
           'pairwise_verdicts': {'exact_generation_content': True,
                                 'code_revision': True},
           'computed_evidence': {'artifact': {'errors': [],
                                              'expected_sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                              'observed_sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                              'requested_generation': 1,
                                              'requested_uri': 'gs://fixture-artifacts/A.txt',
                                              'requests': [['gs://fixture-artifacts/A.txt',
                                                            1]]},
                                 'code': {'commands': [{'args': ['git',
                                                                 'rev-parse',
                                                                 '--verify',
                                                                 'da89ee877040e427fd3de821dffbdc0abd82017b'],
                                                        'exit_code': 0,
                                                        'stderr': '',
                                                        'stdout': 'da89ee877040e427fd3de821dffbdc0abd82017b\n'},
                                                       {'args': ['git',
                                                                 'show',
                                                                 'da89ee877040e427fd3de821dffbdc0abd82017b'],
                                                        'exit_code': 0,
                                                        'stderr': '',
                                                        'stdout': 'commit '
                                                                  'da89ee877040e427fd3de821dffbdc0abd82017b\n'
                                                                  'Author: Fixture '
                                                                  'Author '
                                                                  '<fixture@example.invalid>\n'
                                                                  'Date:   Tue Nov 14 '
                                                                  '22:13:20 2023 '
                                                                  '+0000\n'
                                                                  '\n'
                                                                  '    Authored '
                                                                  'lineage fixture\n'
                                                                  '\n'
                                                                  'diff --git '
                                                                  'a/model_source.py '
                                                                  'b/model_source.py\n'
                                                                  'new file mode '
                                                                  '100644\n'
                                                                  'index '
                                                                  '0000000..80bd3ad\n'
                                                                  '--- /dev/null\n'
                                                                  '+++ '
                                                                  'b/model_source.py\n'
                                                                  '@@ -0,0 +1,3 @@\n'
                                                                  '+"""Fictional '
                                                                  'package source '
                                                                  'retained for '
                                                                  'lineage '
                                                                  'inspection."""\n'
                                                                  '+def '
                                                                  'transform(feature):\n'
                                                                  '+    return feature '
                                                                  '/ 5.0\n'}],
                                          'revision': 'da89ee877040e427fd3de821dffbdc0abd82017b'}}},
 'approval_A_deployment_B': {'records': {'artifacts': {'A': {'artifact_id': 'A',
                                                             'uri': 'gs://fixture-artifacts/A.txt',
                                                             'generation': 1,
                                                             'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                                             'validation_ok': True},
                                                       'B': {'artifact_id': 'B',
                                                             'uri': 'gs://fixture-artifacts/B.txt',
                                                             'generation': 1,
                                                             'sha256': '6d5f5cbc73990d86a040e72f9e6d1cad2cb36297b10887e5444900c7286f634a',
                                                             'validation_ok': True}},
                                         'code': {'code.A': {'revision': 'da89ee877040e427fd3de821dffbdc0abd82017b',
                                                             'repository': 'local_repo'}}},
                             'pairwise_verdicts': {'exact_generation_content': True,
                                                   'code_revision': True},
                             'computed_evidence': {'artifact': {'errors': [],
                                                                'expected_sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                                                'observed_sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6',
                                                                'requested_generation': 1,
                                                                'requested_uri': 'gs://fixture-artifacts/A.txt',
                                                                'requests': [['gs://fixture-artifacts/A.txt',
                                                                              1]]},
                                                   'code': {'commands': [{'args': ['git',
                                                                                   'rev-parse',
                                                                                   '--verify',
                                                                                   'da89ee877040e427fd3de821dffbdc0abd82017b'],
                                                                          'exit_code': 0,
                                                                          'stderr': '',
                                                                          'stdout': 'da89ee877040e427fd3de821dffbdc0abd82017b\n'},
                                                                         {'args': ['git',
                                                                                   'show',
                                                                                   'da89ee877040e427fd3de821dffbdc0abd82017b'],
                                                                          'exit_code': 0,
                                                                          'stderr': '',
                                                                          'stdout': 'commit '
                                                                                    'da89ee877040e427fd3de821dffbdc0abd82017b\n'
                                                                                    'Author: '
                                                                                    'Fixture '
                                                                                    'Author '
                                                                                    '<fixture@example.invalid>\n'
                                                                                    'Date:   '
                                                                                    'Tue '
                                                                                    'Nov '
                                                                                    '14 '
                                                                                    '22:13:20 '
                                                                                    '2023 '
                                                                                    '+0000\n'
                                                                                    '\n'
                                                                                    '    '
                                                                                    'Authored '
                                                                                    'lineage '
                                                                                    'fixture\n'
                                                                                    '\n'
                                                                                    'diff '
                                                                                    '--git '
                                                                                    'a/model_source.py '
                                                                                    'b/model_source.py\n'
                                                                                    'new '
                                                                                    'file '
                                                                                    'mode '
                                                                                    '100644\n'
                                                                                    'index '
                                                                                    '0000000..80bd3ad\n'
                                                                                    '--- '
                                                                                    '/dev/null\n'
                                                                                    '+++ '
                                                                                    'b/model_source.py\n'
                                                                                    '@@ '
                                                                                    '-0,0 '
                                                                                    '+1,3 '
                                                                                    '@@\n'
                                                                                    '+"""Fictional '
                                                                                    'package '
                                                                                    'source '
                                                                                    'retained '
                                                                                    'for '
                                                                                    'lineage '
                                                                                    'inspection."""\n'
                                                                                    '+def '
                                                                                    'transform(feature):\n'
                                                                                    '+    '
                                                                                    'return '
                                                                                    'feature '
                                                                                    '/ '
                                                                                    '5.0\n'}],
                                                            'revision': 'da89ee877040e427fd3de821dffbdc0abd82017b'}}}}
  annotations: ['Artifact / code — inspect exact identities, not similar names']
[CODE python]
computed_panel = {'case_assertions': [{'case_id': 'valid',
                      'expected_audit_acceptance': True,
                      'observed_audit_acceptance': True,
                      'assertion_pass': True,
                      'missing_or_mismatched_links': []},
                     {'case_id': 'boundary_same_name_other_version',
                      'expected_audit_acceptance': True,
                      'observed_audit_acceptance': True,
                      'assertion_pass': True,
                      'missing_or_mismatched_links': []},
                     {'case_id': 'approval_A_deployment_B',
                      'expected_audit_acceptance': False,
                      'observed_audit_acceptance': False,
                      'assertion_pass': True,
                      'missing_or_mismatched_links': ['deployment_to_registry',
                                                      'approval_to_deployment']},
                     {'case_id': 'missing_run_link',
                      'expected_audit_acceptance': False,
                      'observed_audit_acceptance': False,
                      'assertion_pass': True,
                      'missing_or_mismatched_links': ['registry_to_run']},
                     {'case_id': 'wrong_generation',
                      'expected_audit_acceptance': False,
                      'observed_audit_acceptance': False,
                      'assertion_pass': True,
                      'missing_or_mismatched_links': ['registry_to_artifact',
                                                      'exact_generation_content']},
                     {'case_id': 'missing_code_revision',
                      'expected_audit_acceptance': False,
                      'observed_audit_acceptance': False,
                      'assertion_pass': True,
                      'missing_or_mismatched_links': ['code_revision']},
                     {'case_id': 'configuration_mismatch',
                      'expected_audit_acceptance': False,
                      'observed_audit_acceptance': False,
                      'assertion_pass': True,
                      'missing_or_mismatched_links': ['run_to_configuration']},
                     {'case_id': 'dataset_mismatch',
                      'expected_audit_acceptance': False,
                      'observed_audit_acceptance': False,
                      'assertion_pass': True,
                      'missing_or_mismatched_links': ['run_to_dataset']}],
 'selected_audit_results': {'valid': {'pairwise_verdicts': {'approval_to_deployment': True,
                                                            'code_revision': True,
                                                            'deployment_to_registry': True,
                                                            'exact_generation_content': True,
                                                            'registry_to_artifact': True,
                                                            'registry_to_run': True,
                                                            'run_to_artifact': True,
                                                            'run_to_configuration': True,
                                                            'run_to_dataset': True},
                                      'missing_or_mismatched_links': [],
                                      'accepted': True,
                                      'stage_status': 'SUCCESS',
                                      'exit_code': 0},
                            'approval_A_deployment_B': {'pairwise_verdicts': {'approval_to_deployment': False,
                                                                              'code_revision': True,
                                                                              'deployment_to_registry': False,
                                                                              'exact_generation_content': True,
                                                                              'registry_to_artifact': True,
                                                                              'registry_to_run': True,
                                                                              'run_to_artifact': True,
                                                                              'run_to_configuration': True,
                                                                              'run_to_dataset': True},
                                                        'missing_or_mismatched_links': ['deployment_to_registry',
                                                                                        'approval_to_deployment'],
                                                        'accepted': False,
                                                        'stage_status': 'FAILURE',
                                                        'exit_code': 1}}}
  annotations: ['Declared case assertions and final audit verdicts', 'Recorded names are inputs, not proof. The audit verifies each identity edge, exact artifact content and the referenced local commit, and reports every missing or mismatched link.']

### s19 · explainer · Audit dataset, code, run and artifact lineage of a deployed model
mle.tile.076_079 — 
(example) Walk deployment → registry → artifact/run → configuration and dataset; check the recorded code against an existing local commit. Resolve the exact registry generation and verify downloaded content against the lineage record. Compare run evidence with deployment and approval, preserving each missing or mismatched edge. Approval for A cannot cover a deployment linked to B. Inspect the revision with git rev-parse and git show; a revision string alone is not commit-existence evidence. These checks audit supplied provenance; they cannot recover an absent link by guessing from familiar model names. ⟦D.f1 D.f2 D.f3 D.f4 D.f5 D.f6 D.f7 D:tb5⟧

### s20 · explainer · Audit dataset, code, run and artifact lineage of a deployed model
mle.tile.076_079 — 
(mechanism) Matching names are not lineage. Report missing or mismatched run/artifact links; an unverified revision string does not prove a commit exists. ⟦D.f1 D.f4 D.f7 D:tb6⟧

### s21 · check · Inspect the gate evidence
mle.tile.076_079 — Use the supplied evidence to judge the required predicates and boundaries.

### s22 · hands_on · Review the lineage evidence
mle.tile.076_079 — Read the supplied excerpts in this step and decide which preserve the required identity checks and which are defective.

### s23 · recap · Keep each boundary accountable
mle.tile.076_079 — 
(takeaway) Stage order and artifact-identity agreement are separate checks. ⟦A.f3 A.f7 A.f10 A:tb7⟧
(takeaway) Validation and authorization must cover the exact promoted artifact. ⟦B.f3 B.f4 B.f11 B.f12 B.f13 B:tb8⟧
(takeaway) Reuse only verified output; recovery must not bypass required gates. ⟦C.f3 C.f4 C.f9 C.f11 C.f12 C:tb7⟧
(takeaway) Report missing identity links; inspect exact content and the recorded commit. ⟦D.f1 D.f4 D.f7 D:tb6⟧
[UP NEXT] Monitor production input and prediction distributions: Next: mle.tile.080_082.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the required checks — Return to the same fictional lifecycle fixtures.
(mechanism) Bind consumer args/substitutions to upstream-produced immutable identity; verify actual resolved inputs, not just order. ⟦A.f10 A:tb5 A:tb7⟧
(mechanism) Use configured Pub/Sub payload bindings and filters; inspect stage results and resolved inputs for accepted/rejected fixtures. ⟦A.f9 A:tb4⟧
(misconception) waitFor proves a completion dependency, not artifact agreement. Verify the consumed identity separately. ⟦A.f3 A.f7 A.f10 A:tb7⟧
### r02 · Separate the required checks — Return to the same fictional lifecycle fixtures.
(mechanism) Explicit component input/output artifacts support reuse across experiment and production environments. ⟦A.f1 A:tb2⟧
(mechanism) Bind consumer args/substitutions to upstream-produced immutable identity; verify actual resolved inputs, not just order. ⟦A.f10 A:tb5 A:tb7⟧
(mechanism) With declared PyYAML, import yaml; yaml.safe_dump(config, file_handle), then yaml.safe_load(file_handle). Inspect required resolved fields before runtime submission. Safe loading accepts standard tags, not arbitrary Python constructors. ⟦A.f11 A:tb5⟧
(mechanism) Record consumed identities, execution parameters and produced identity per stage; filenames alone cannot join outputs. ⟦A.f2 A:tb2⟧
(mechanism) Use a dependency dictionary; verify every required upstream identity against its downstream reference. ⟦A.f3 A:tb2 A:tb7⟧
(mechanism) Require relevant dataset/model validation before dependent execution. ⟦A.f4 A:tb3⟧
(mechanism) Assert valid, boundary and failure predicates; false predicates raise AssertionError in ordinary non-optimized execution. ⟦A.f5 A:tb3⟧
(mechanism) Cloud Build steps use name for the image and args or script for the command; wire the assigned entry point. ⟦A.f6 A:tb3⟧
(mechanism) Assign IDs and waitFor required predecessors’ successful completion, not merely textual order. ⟦A.f7 A:tb4 A:tb7⟧
(mechanism) No allowFailure or allowed failing exit codes for required gates; rejected Python gates exit unsuccessfully. ⟦A.f8 A:tb4⟧
(mechanism) Use configured Pub/Sub payload bindings and filters; inspect stage results and resolved inputs for accepted/rejected fixtures. ⟦A.f9 A:tb4⟧
(misconception) waitFor proves a completion dependency, not artifact agreement. Verify the consumed identity separately. ⟦A.f3 A.f7 A.f10 A:tb7⟧
### r03 · Separate the required checks — Return to the same fictional lifecycle fixtures.
(mechanism) Use approved availableSecrets.secretManager version references and step-scoped secretEnv, never literal secret values. ⟦B.f10 B:tb5⟧
(mechanism) Check captured output for non-disclosure; never echo or serialize runtime credentials. ⟦B.f12 B:tb5 B:tb8⟧
(misconception) Passing staging for A cannot approve B. Training or staging success is not promotion authorization, and credentials must not enter the promotion record. ⟦B.f3 B.f4 B.f11 B.f12 B.f13 B:tb8⟧
### r04 · Separate the required checks — Return to the same fictional lifecycle fixtures.
(mechanism) Read approved registry name/version and run/artifact link before authorization. ⟦B.f1 B:tb2⟧
(mechanism) Use authorized build/step identity; retain separate promotion authorization. ⟦B.f11 B:tb5 B:tb8⟧
(mechanism) Edit and parse existing staging/production YAML: production requires staging quality and authorization for the identical artifact. Verify unauthorized production does not execute. ⟦B.f13 B:tb6 B:tb8⟧
(mechanism) With declared PyYAML, import yaml; yaml.safe_dump(config, file_handle), then yaml.safe_load(file_handle). Inspect required resolved fields before runtime submission. Safe loading accepts standard tags, not arbitrary Python constructors. ⟦B.f14 B:tb6⟧
(mechanism) Continuous delivery checks test-environment compatibility, then model validation before production. ⟦B.f2 B:tb2⟧
(mechanism) Preserve exact-artifact validation, including offline requirements and supplied staged evidence. ⟦B.f3 B:tb2 B:tb8⟧
(mechanism) Stay within permitted identity/approval scope; record accountable authorization without changing policy. ⟦B.f4 B:tb3 B:tb8⟧
(mechanism) Record approval, registry version, artifact identity and per-stage gates. ⟦B.f5 B:tb3⟧
(mechanism) Cloud Build steps use name for the image and args or script for the command; wire the assigned entry point. ⟦B.f6 B:tb3⟧
(mechanism) Assign IDs and waitFor required predecessors’ successful completion, not merely textual order. ⟦B.f7 B:tb4⟧
(mechanism) No allowFailure or allowed failing exit codes for required gates; rejected Python gates exit unsuccessfully. ⟦B.f8 B:tb4⟧
(mechanism) Use configured Pub/Sub payload bindings and filters; inspect stage results and resolved inputs for accepted/rejected fixtures. ⟦B.f9 B:tb4⟧
(misconception) Passing staging for A cannot approve B. Training or staging success is not promotion authorization, and credentials must not enter the promotion record. ⟦B.f3 B.f4 B.f11 B.f12 B.f13 B:tb8⟧
### r05 · Separate the required checks — Return to the same fictional lifecycle fixtures.
(mechanism) Use configured Pub/Sub payload bindings and filters; inspect stage results and resolved inputs for accepted/rejected fixtures. ⟦C.f8 C:tb4⟧
(mechanism) Distinguish injected recoverable exceptions from unrelated failures; retry at the verified boundary and inspect retry/later-gate execution. ⟦C.f9 C:tb4 C:tb7⟧
(misconception) Recovery is not ignore-and-continue. Reuse requires identity and validation; retry must not overwrite conflicting content or bypass gates. ⟦C.f3 C.f4 C.f9 C.f11 C.f12 C:tb7⟧
### r06 · Separate the required checks — Return to the same fictional lifecycle fixtures.
(mechanism) Identify failed stage/affected artifacts; preserve completed required-stage identities. ⟦C.f1 C:tb2⟧
(mechanism) With declared PyYAML, import yaml; yaml.safe_dump(config, file_handle), then yaml.safe_load(file_handle). Inspect required resolved fields before runtime submission. Safe loading accepts standard tags, not arbitrary Python constructors. ⟦C.f10 C:tb5⟧
(mechanism) Reconcile declared named uploads: blob.exists(), blob.reload(), generation-bound bytes, expected hash and required validation. Skip only verified completion. Create missing output with blob.upload_from_filename(path, if_generation_match=0). On 412, re-read/verify, never overwrite. Conflict or failed validation stops recovery. ⟦C.f11 C:tb5 C:tb7⟧
(mechanism) Inject failure after one upload; assert retained generation/hash, only missing uploads complete, retry/later gates execute, and invalid existing output fails. Repeat recovery: no extra uploads/generations, required validation still enforced. ⟦C.f12 C:tb5 C:tb7⟧
(mechanism) Catch declared recoverable error with try/except; record it and apply only supplied recovery action, never silent success. ⟦C.f2 C:tb2⟧
(mechanism) Rerun affected required quality checks after repair; stop on failure, never bypass gates. ⟦C.f3 C:tb2 C:tb7⟧
(mechanism) Reuse upstream artifacts only with valid recorded identity and required validation for the resumed stage. ⟦C.f4 C:tb3 C:tb7⟧
(mechanism) Cloud Build steps use name for the image and args or script for the command; wire the assigned entry point. ⟦C.f5 C:tb3⟧
(mechanism) Assign IDs and waitFor required predecessors’ successful completion, not merely textual order. ⟦C.f6 C:tb3⟧
(mechanism) No allowFailure or allowed failing exit codes for required gates; rejected Python gates exit unsuccessfully. ⟦C.f7 C:tb4⟧
(mechanism) Distinguish injected recoverable exceptions from unrelated failures; retry at the verified boundary and inspect retry/later-gate execution. ⟦C.f9 C:tb4 C:tb7⟧
(misconception) Recovery is not ignore-and-continue. Reuse requires identity and validation; retry must not overwrite conflicting content or bypass gates. ⟦C.f3 C.f4 C.f9 C.f11 C.f12 C:tb7⟧
### r07 · Separate the required checks — Return to the same fictional lifecycle fixtures.
(mechanism) Trace served artifact to training, resolved configuration, code revision and dataset snapshot. ⟦D.f1 D:tb2 D:tb6⟧
(mechanism) Resolve deployed registry version, artifact source and run link. ⟦D.f2 D:tb2⟧
(mechanism) Retrieve the run; compare dataset/configuration/artifact evidence with deployment and approval. ⟦D.f3 D:tb2⟧
(misconception) Matching names are not lineage. Report missing or mismatched run/artifact links; an unverified revision string does not prove a commit exists. ⟦D.f1 D.f4 D.f7 D:tb6⟧
### r08 · Separate the required checks — Return to the same fictional lifecycle fixtures.
(mechanism) Check identity links pairwise; flag missing/mismatched links, never infer provenance from names. ⟦D.f4 D:tb3 D:tb6⟧
(mechanism) Assert valid, boundary and failure predicates; false predicates raise AssertionError in ordinary non-optimized execution. ⟦D.f5 D:tb3⟧
(mechanism) Download registry’s exact recorded artifact generation; verify content identity against lineage. ⟦D.f6 D:tb3⟧
(mechanism) Inspect local revision with git rev-parse --verify REVISION and git show REVISION; confirm the commit exists, not just its string. ⟦D.f7 D:tb4 D:tb6⟧
(misconception) Matching names are not lineage. Report missing or mismatched run/artifact links; an unverified revision string does not prove a commit exists. ⟦D.f1 D.f4 D.f7 D:tb6⟧