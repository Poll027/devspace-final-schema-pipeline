# EVALUATOR PACKET — Run supplied tests as blocking pipeline gates (aws_devops.tile.100)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.run_supplied_unit_and_integration_tests_as_blocking_pipeline_gates — Run supplied unit and integration tests as blocking pipeline gates after external testing preparation

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.run_supplied_unit_and_integration_tests_as_blocking_pipeline_gates)   objective: Run supplied tests as blocking pipeline gates
A.f1: A nonzero command exit status reports failure to a pipeline step, while zero reports success.   [sources: github_actions_docs#how-tos/create-and-publish-actions/set-exit-codes]
A.f2: Run the supplied unit and integration test commands in workflow steps with run: TEST_COMMAND; set the promotion job’s needs: [UNIT_JOB, INTEGRATION_JOB] to require both test jobs.   [sources: github_actions_docs#reference/workflows-and-actions/workflow-syntax]
A.f3: Do not set continue-on-error on the blocking test steps; demonstrate a failing supplied test prevents the dependent promotion.   [sources: github_actions_docs#reference/workflows-and-actions/workflow-syntax]
note: Use supplied tests; do not teach application test authoring or unfamiliar shell exit-handling syntax.
PRACTICE ANCHOR (live_code): Wire the supplied unit and integration test commands into separate jobs in one prepared GitHub Actions workflow. Require both jobs for promotion, leave continue-on-error unset on blocking test steps, and run the supplied seeded failure case.  SUCCESS: The failing supplied test reports a nonzero exit status, its job fails, and the dependent promotion job is skipped even when the other test job succeeds.
ASSESSMENT ANCHOR: verify_failing_supplied_test_blocks_promotion facts=['f1', 'f2', 'f3']

## DATA ASSETS USED
ds.test_gates: Run supplied unit and integration tests as blocking pipeline gates after external testing preparation — read-only evidence — columns: job(identifier), needs(text), exit_status(categorical), job_status(categorical), continue_on_error(categorical)
   ["UNIT_JOB","",1,"failure",false]
   ["INTEGRATION_JOB","",0,"success",false]
   ["promotion","UNIT_JOB, INTEGRATION_JOB",null,"skipped",false]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Approval stop; Audit evidence; Audit evidence integrity; Audit storage retention; Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template; directly require the native EC2 instance foundation; Backend configuration; Block release on actionable dependency or image security findings; Control environment promotion with a manual approval; Credential readiness; Diagnose EC2 or container health failures using telemetry and prepared Linux inspection skills; Diagnose a failed delivery pipeline action; Gate release completion on a deployed-service smoke check; Handle failed event delivery with bounded retries and failure capture; Perform a controlled ECS service rollout; Promote the same artifact version across environments; Recover an incident safely using an established runbook; Rehearsal isolation; Replacement controls; Residual charge verification; Safe teardown; State access isolation; State locking; Submit small reviewable infrastructure changes after registry Git and code-review prerequisites; Verify availability across Availability Zones under a controlled failure; Verify restored service and data against RTO/RPO in an isolated rehearsal

## LESSON, in learner order

### s01 · explainer · Run supplied tests as blocking pipeline gates
Read the evidence — 
(mechanism) Failure must reach the workflow: a nonzero command exit status means failure; zero means success. ⟦A.f1 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Use run: TEST_COMMAND for the supplied unit and integration commands. Set promotion to needs: [UNIT_JOB, INTEGRATION_JOB], requiring both jobs. ⟦A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Leave continue-on-error unset on blocking test steps. In the supplied failure case, promotion is skipped even though the other test succeeds. Tolerating that failure would defeat the blocking gate. ⟦A.f3 A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[DIAGRAM] nodes=['Unit test command: exit status and job outcome', 'Integration test command: exit status and job outcome', 'Promotion: depends on both test jobs'] edges=[('n0', 'n2', 'required'), ('n1', 'n2', 'required')] alt: Make the workflow dependency and execution outcomes visible: both test jobs feed promotion, one supplied test job fails, the other succeeds, and promotion is skipped. Show the failing command's nonzero exit status.
[TABLE ds.test_gates cols=['job', 'needs', 'exit_status', 'job_status', 'continue_on_error'] ] caption: 

### s02 · check · Review blocking test gates
Check your understanding — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] A supplied unit test exits nonzero while integration succeeds. Which configuration and outcome demonstrate a blocking test gate?
  ✔ a: Both supplied commands run in their jobs; promotion needs both jobs; neither test uses continue-on-error; the unit job fails and promotion is skipped.
      why: Correct. Both supplied commands run in their jobs; promotion needs both jobs; neither test uses continue-on-error; the unit job fails and promotion is skipped.
  ✘ b: Set continue-on-error on the failed test and still describe promotion as blocked.
      why: Failure must propagate from the command to its job and the dependent promotion. continue-on-error defeats this blocking requirement.
  ✘ c: Make promotion need only the successful integration job.
      why: Promotion must require both test jobs, not just the successful one.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The failing supplied test reports a nonzero exit status, its job fails, and the dependent promotion job is skipped even when the other test job succeeds.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r01
  MEASURES: A:verify_failing_supplied_test_blocks_promotion(f1,f2,f3)   anchors=['assessment:verify_failing_supplied_test_blocks_promotion']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s03 · hands_on · Review blocking test gates
Evidence review — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read the workflow and execution excerpts. Classify each record as the failing gate, successful companion gate, or blocked dependent promotion.
  'Supplied workflow excerpt:
```yaml
jobs:
  UNIT_JOB:
    steps:
      - run: TEST_COMMAND # supplied unit test
  INTEGRATION_JOB:
    steps:
      - run: TEST_COMMAND # supplied integration test
  promotion:
    needs: [UNIT_JOB, INTEGRATION_JOB]
```
No blocking step sets continue-on-error. The execution records below belong to this workflow.
```text
job: "UNIT_JOB"
needs: ""
exit_status: 1
job_status: "failure"
continue_on_error: false
```' -> Failing test gate  (column job_status, role=categorical)
      feedback: Judgement: Failing test gate. Compare the stated evidence with the required criterion.
  'Supplied workflow excerpt:
```yaml
jobs:
  UNIT_JOB:
    steps:
      - run: TEST_COMMAND # supplied unit test
  INTEGRATION_JOB:
    steps:
      - run: TEST_COMMAND # supplied integration test
  promotion:
    needs: [UNIT_JOB, INTEGRATION_JOB]
```
No blocking step sets continue-on-error. The execution records below belong to this workflow.
```text
job: "INTEGRATION_JOB"
needs: ""
exit_status: 0
job_status: "success"
continue_on_error: false
```' -> Successful companion test gate  (column job_status, role=categorical)
      feedback: Judgement: Successful companion test gate. Compare the stated evidence with the required criterion.
  'Supplied workflow excerpt:
```yaml
jobs:
  UNIT_JOB:
    steps:
      - run: TEST_COMMAND # supplied unit test
  INTEGRATION_JOB:
    steps:
      - run: TEST_COMMAND # supplied integration test
  promotion:
    needs: [UNIT_JOB, INTEGRATION_JOB]
```
No blocking step sets continue-on-error. The execution records below belong to this workflow.
```text
job: "promotion"
needs: "UNIT_JOB, INTEGRATION_JOB"
exit_status: null
job_status: "skipped"
continue_on_error: false
```' -> Blocked dependent promotion  (column job_status, role=categorical)
      feedback: Judgement: Blocked dependent promotion. Compare the stated evidence with the required criterion.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The failing supplied test reports a nonzero exit status, its job fails, and the dependent promotion job is skipped even when the other test job succeeds.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r01
  MEASURES: A:verify_failing_supplied_test_blocks_promotion(f1,f2,f3)   anchors=['practice', 'assessment:verify_failing_supplied_test_blocks_promotion']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s04 · recap · Keep these distinctions
(takeaway) Nonzero means failure. Require both supplied test jobs and do not tolerate blocking failures. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Submit a small reviewable infrastructure change: Next: Submit a small reviewable infrastructure change.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the evidence
(mechanism) Failure must reach the workflow: a nonzero command exit status means failure; zero means success. ⟦A.f1 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Use run: TEST_COMMAND for the supplied unit and integration commands. Set promotion to needs: [UNIT_JOB, INTEGRATION_JOB], requiring both jobs. ⟦A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Leave continue-on-error unset on blocking test steps. In the supplied failure case, promotion is skipped even though the other test succeeds. Tolerating that failure would defeat the blocking gate. ⟦A.f3 A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) One successful test does not satisfy two required gates. Inspect the failing command and the skipped promotion together. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.test_gates cols=['job', 'needs', 'exit_status', 'job_status', 'continue_on_error'] ] caption: 

=========

# EVALUATOR PACKET — Submit a small reviewable infrastructure change (aws_devops.tile.101)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.submit_small_reviewable_infrastructure_changes — Submit small reviewable infrastructure changes after registry Git and code-review prerequisites

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.submit_small_reviewable_infrastructure_changes)   objective: Submit a small reviewable infrastructure change
A.f1: Small coherent changes reduce review complexity and make delivery feedback easier to act on.   [sources: aws_wa_devops_guidance#dl.ci.1-integrate-code-changes-regularly-and-frequently.html]
A.f2: In the supplied repository workflow, stage the focused files with git add FILES, commit with git commit -m "MESSAGE", push the review branch with git push, and open its supplied pull-request interface to request review.   [sources: git_docs#git-commit, git_docs#git-add, git_docs#git-push]
A.f3: Submit a focused infrastructure pull request with its intent, coherent diff and saved plan evidence showing the affected EC2 resource.   [sources: terraform_language#../cli/commands/plan]
A.f4: After the supplied approval, execute the supplied CI apply using the approved saved plan and attach the execution and resource-verification evidence to the change record.   [sources: terraform_language#../cli/commands/apply]
note: Require external Git/CI preparation; use supplied review interface and approved apply workflow.
PRACTICE ANCHOR (external_proof): Submit one focused Terraform EC2 pull request through the supplied repository and review interface. Stage the focused files, commit and push the review branch, and include intent, a coherent diff and saved-plan evidence. After the supplied reviewer approves it, run the supplied CI apply workflow using the approved saved plan and attach execution and EC2 resource-verification evidence. Independent impact authorization is not reassessed.  SUCCESS: The change record contains one coherent EC2 change, a traceable commit, clear intent, saved-plan evidence identifying the affected EC2 resource, supplied reviewer approval, a successful CI execution using that approved saved plan, and verification of the resulting single EC2 instance.
ASSESSMENT ANCHOR: verify_change_isolation_and_coherence facts=['f1', 'f3']
ASSESSMENT ANCHOR: verify_submission_traceability_and_saved_plan_evidence facts=['f2', 'f3']
ASSESSMENT ANCHOR: verify_approved_execution_and_resource_evidence facts=['f4']

## DATA ASSETS USED
ds.change_record: Submit small reviewable infrastructure changes after registry Git and code-review prerequisites — read-only evidence — columns: change_id(identifier), evidence_kind(categorical), evidence(text)
   ["change-exercise","intent","Focused approved EC2 configuration change"]
   ["change-exercise","diff","Only the supplied EC2 resource arguments changed"]
   ["change-exercise","commit_reference","exercise-focused-commit on the supplied review branch"]
   ["change-exercise","saved_plan","Approved saved plan for the affected exercise EC2 resource"]
   ["change-exercise","approval","Supplied reviewer approval before CI apply"]
   ["change-exercise","execution","CI applied the approved saved plan"]
   ["change-exercise","verification","Resulting exercise instance verified"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Approval stop; Audit evidence; Audit evidence integrity; Audit storage retention; Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template; directly require the native EC2 instance foundation; Backend configuration; Block release on actionable dependency or image security findings; Control environment promotion with a manual approval; Credential readiness; Diagnose EC2 or container health failures using telemetry and prepared Linux inspection skills; Diagnose a failed delivery pipeline action; Document incident evidence and a preventive change using reused systematic-debugging coverage; Gate release completion on a deployed-service smoke check; Handle failed event delivery with bounded retries and failure capture; Perform a controlled ECS service rollout; Promote the same artifact version across environments; Recover an incident safely using an established runbook; Rehearsal isolation; Replacement controls; Residual charge verification; Safe teardown; State access isolation; State locking; Verify availability across Availability Zones under a controlled failure; Verify restored service and data against RTO/RPO in an isolated rehearsal

## LESSON, in learner order

### s01 · explainer · Submit a small reviewable infrastructure change
Read the evidence — 
(mechanism) Keep the change small and coherent: this reduces review complexity and makes delivery feedback easier to act on. ⟦A.f1 A:tb1 A:tb2 A:tb3⟧
(mechanism) Stage focused files with git add FILES, commit with git commit -m "MESSAGE", then git push the review branch. Request review through the supplied pull-request interface. ⟦A.f2 A:tb1 A:tb2 A:tb3⟧
(mechanism) Include intent, a coherent diff and saved-plan evidence for the affected EC2 resource. After supplied approval, use that approved saved plan for the supplied CI apply; attach execution and resource-verification evidence. ⟦A.f3 A.f4 A:tb1 A:tb2 A:tb3⟧
[DIAGRAM] nodes=['Focused review: intent and diff', 'Commit reference and saved EC2 plan', 'Reviewer approval', 'CI apply and resulting instance verification'] edges=[] alt: Make the supplied pull-request record visible with its focused diff, intent, commit reference, saved-plan evidence for the EC2 resource, reviewer approval, CI execution result and resulting instance verification.
[TABLE ds.change_record cols=['change_id', 'evidence_kind', 'evidence'] ] caption: 

### s02 · explainer · Compare the evidence
Read the evidence — 
(example) Approval alone is not execution evidence. The focused change record also needs the approved saved plan, CI apply outcome and resulting resource verification. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Review focused infrastructure change evidence
Check your understanding — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] Which pull-request scope best supports focused infrastructure review?
  ✔ a: One coherent EC2 change with clear intent, a focused diff and saved-plan evidence identifying the affected EC2 resource.
      why: Correct. One coherent EC2 change with clear intent, a focused diff and saved-plan evidence identifying the affected EC2 resource.
  ✘ b: Several unrelated infrastructure changes grouped under one short commit message.
      why: A short message does not make unrelated changes coherent or reduce their review complexity.
  ✘ c: One EC2 change with clear intent but no saved-plan evidence of the affected resource.
      why: Focused scope is not enough: the affected EC2 resource must be visible in saved-plan evidence.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The change record contains one coherent EC2 change, a traceable commit, clear intent, saved-plan evidence identifying the affected EC2 resource, supplied reviewer approval, a successful CI execution using that approved saved plan, and verification of the resulting single EC2 instance.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r01
  MEASURES: A:verify_change_isolation_and_coherence(f1,f3)   anchors=['assessment:verify_change_isolation_and_coherence']
  taught-before-tested: A.f1←s01; A.f3←s01

### s04 · hands_on · Review focused infrastructure change evidence
Evidence review — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each complete or alternate change-record excerpt. Decide whether it establishes a coherent, traceable reviewed EC2 change followed by approved saved-plan execution and single-instance verification, or is insufficient. Treat each record independently.
  'Reviewed record:
```text
intent: "Focused approved EC2 configuration change"
diff: "Only the supplied EC2 resource arguments changed"
commit_reference: "exercise-focused-commit on the supplied review branch"
saved_plan: "Approved saved plan for the affected exercise EC2 resource"
approval: "Supplied reviewer approval before CI apply"
execution: "CI applied the approved saved plan"
verification: "Resulting exercise instance verified"
```
The supplied focused files were staged with git add FILES, committed with git commit -m "MESSAGE", pushed with git push, and review requested through the supplied pull-request interface. Verification identifies a single resulting exercise EC2 instance.
```text
change_id: "change-exercise"
evidence_kind: "intent"
evidence: "Focused approved EC2 configuration change"
```' -> Complete coherent submission and approved execution evidence  (column evidence_kind, role=categorical)
      feedback: Judgement: Complete coherent submission and approved execution evidence. Compare the stated evidence with the required criterion.
  'Alternate record (all other supplied staging, commit, push and review steps are unchanged):
```text
intent: "Focused approved EC2 configuration change"
diff: "Only the supplied EC2 resource arguments changed"
commit_reference: "exercise-focused-commit on the supplied review branch"
saved_plan: "Approved saved plan for the affected exercise EC2 resource"
approval: "Supplied reviewer approval before CI apply"
```
CI execution and resulting-instance verification are not recorded.' -> Insufficient or mismatched execution evidence
      feedback: Judgement: Insufficient or mismatched execution evidence. Compare the stated evidence with the required criterion.
  'Alternate record (the same supplied submission steps were completed):
```text
intent: "Focused approved EC2 configuration change"
diff: "Only the supplied EC2 resource arguments changed"
commit_reference: "exercise-focused-commit on the supplied review branch"
saved_plan: "Approved saved plan for the affected exercise EC2 resource"
approval: "Supplied reviewer approval before CI apply"
execution: "CI applied a different plan, not the approved saved plan"
verification: "Resulting exercise instance verified"
```' -> Insufficient or mismatched execution evidence
      feedback: Judgement: Insufficient or mismatched execution evidence. Compare the stated evidence with the required criterion.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The change record contains one coherent EC2 change, a traceable commit, clear intent, saved-plan evidence identifying the affected EC2 resource, supplied reviewer approval, a successful CI execution using that approved saved plan, and verification of the resulting single EC2 instance.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r02
  MEASURES: A:verify_submission_traceability_and_saved_plan_evidence(f2,f3); A:verify_approved_execution_and_resource_evidence(f4)   anchors=['practice', 'assessment:verify_submission_traceability_and_saved_plan_evidence', 'assessment:verify_approved_execution_and_resource_evidence']
  taught-before-tested: A.f2←s01; A.f3←s01; A.f4←s01

### s05 · recap · Keep these distinctions
(takeaway) Keep changes focused and carry intent, diff and saved plan through approval, CI apply and resource verification. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Verify multi-AZ availability: Next: Verify multi-AZ availability.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the evidence
(mechanism) Keep the change small and coherent: this reduces review complexity and makes delivery feedback easier to act on. ⟦A.f1 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Include intent, a coherent diff and saved-plan evidence for the affected EC2 resource. After supplied approval, use that approved saved plan for the supplied CI apply; attach execution and resource-verification evidence. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Approval alone is not execution evidence. The focused change record also needs the approved saved plan, CI apply outcome and resulting resource verification. ⟦A.f1 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.change_record cols=['change_id', 'evidence_kind', 'evidence'] ] caption: 
### r02 · Separate the evidence
(mechanism) Stage focused files with git add FILES, commit with git commit -m "MESSAGE", then git push the review branch. Request review through the supplied pull-request interface. ⟦A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Include intent, a coherent diff and saved-plan evidence for the affected EC2 resource. After supplied approval, use that approved saved plan for the supplied CI apply; attach execution and resource-verification evidence. ⟦A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Approval alone is not execution evidence. The focused change record also needs the approved saved plan, CI apply outcome and resulting resource verification. ⟦A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.change_record cols=['change_id', 'evidence_kind', 'evidence'] ] caption: 

=========

# EVALUATOR PACKET — Verify multi-AZ availability (aws_devops.tile.102)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.verify_availability_across_availability_zones_under_a_controlled_failure — Verify availability across Availability Zones under a controlled failure

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.verify_availability_across_availability_zones_under_a_controlled_failure)   objective: Verify multi-AZ availability
A.f1: Resilience testing deliberately introduces failures to verify the workload can meet its availability requirements.   [sources: aws_well_architected_framework#rel12-bp04.html]
A.f2: Limit the approved failure to the supplied AZ components, define abort criteria, and monitor client-visible service behavior during the experiment.   [sources: aws_well_architected_framework#rel12-bp04.html]
A.f3: Check that the remaining independent capacity and request path maintain the required service behavior rather than inferring availability from surviving instance count alone.   [sources: aws_well_architected_framework#rel11.html]
note: Use approved failure procedure; do not introduce regional failover or unsafe production faults.
PRACTICE ANCHOR (tool_simulation): Run the supplied approved AZ-component failure procedure in a two-AZ topology. Confirm the target components and define abort criteria before starting, monitor required client-visible behavior during the failure, and check the remaining independent capacity and request path.  SUCCESS: Only the approved components in one AZ are affected, the defined abort criteria are enforced, and the result is judged against the supplied service requirement using client-request outcomes and remaining-path evidence rather than surviving instance count alone.
ASSESSMENT ANCHOR: explain_controlled_failure_as_availability_verification facts=['f1']
ASSESSMENT ANCHOR: bound_az_component_failure_and_monitor_client_behavior facts=['f2']
ASSESSMENT ANCHOR: verify_availability_using_remaining_capacity_and_request_path facts=['f3']

## DATA ASSETS USED
ds.az_availability: Verify availability across Availability Zones under a controlled failure — read-only evidence — columns: case_id(identifier), failed_scope(categorical), abort_criteria(text), independent_capacity_remains(categorical), remaining_request_path(categorical), client_required_behavior(categorical)
   ["az-path-fails","supplied AZ components","Stop on reaching supplied client failure limit",true,"unavailable","fail"]
   ["az-path-passes","supplied AZ components","Stop on reaching supplied client failure limit",true,"available","pass"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Approval stop; Audit evidence; Audit evidence integrity; Audit storage retention; Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template; directly require the native EC2 instance foundation; Backend configuration; Block release on actionable dependency or image security findings; Control environment promotion with a manual approval; Credential readiness; Diagnose EC2 or container health failures using telemetry and prepared Linux inspection skills; Diagnose a failed delivery pipeline action; Document incident evidence and a preventive change using reused systematic-debugging coverage; Endpoint cutover; Gate release completion on a deployed-service smoke check; Handle failed event delivery with bounded retries and failure capture; Perform a controlled ECS service rollout; Promote the same artifact version across environments; Recover an incident safely using an established runbook; Rehearsal isolation; Replacement controls; Residual charge verification; Safe teardown; State access isolation; State locking; Verify restored service and data against RTO/RPO in an isolated rehearsal

## LESSON, in learner order

### s01 · explainer · Verify multi-AZ availability
Read the evidence — 
(mechanism) Resilience testing deliberately introduces failures to check availability requirements. Bound the approved experiment to the supplied AZ components, define abort criteria and monitor client-visible behavior. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3⟧
(mechanism) Verify that remaining independent capacity and the request path maintain required service behavior. Surviving instances alone do not prove availability. ⟦A.f3 A:tb1 A:tb2 A:tb3⟧
[DIAGRAM] nodes=['Client request', 'Approved failed AZ components', 'Remaining independent AZ capacity', 'Remaining request path', 'Observed behavior versus requirement'] edges=[('n0', 'n3', 'client path'), ('n3', 'n2', 'remaining capacity'), ('n3', 'n4', 'verify required behavior')] alt: Show the supplied two-AZ topology with the approved failed components marked, the remaining independent capacity and client request path identified, and observed client-request outcomes compared with the required service behavior.
[TABLE ds.az_availability cols=['case_id', 'failed_scope', 'abort_criteria', 'independent_capacity_remains', 'remaining_request_path', 'client_required_behavior'] ] caption: 

### s02 · explainer · Compare the evidence
Read the evidence — 
(example) Compare the supplied cases: independent capacity remains in both, but only the case with a working client request path demonstrates the required behavior. Preserve scope, abort criteria and client outcomes together; do not widen the experiment beyond the approved AZ components. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · check · Review AZ availability evidence
Check your understanding — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] What is the purpose of deliberately introducing a controlled failure in an availability experiment?
  ✔ a: Verify whether the workload meets its availability requirements under failure.
      why: Correct. Verify whether the workload meets its availability requirements under failure.
  ✘ b: Prove availability merely by counting instances that remain running.
      why: Surviving components alone do not establish the required service behavior.
  ✘ c: Demonstrate that every component remains unchanged during the experiment.
      why: The experiment deliberately introduces a failure; unchanged components are not its success criterion.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. Only the approved components in one AZ are affected, the defined abort criteria are enforced, and the result is judged against the supplied service requirement using client-request outcomes and remaining-path evidence rather than surviving instance count alone.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r01
  MEASURES: A:explain_controlled_failure_as_availability_verification(f1)   anchors=['assessment:explain_controlled_failure_as_availability_verification']
  taught-before-tested: A.f1←s01

### s04 · hands_on · Review AZ availability evidence
Evidence review — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read both bounded experiment excerpts. Decide whether the evidence verifies the supplied client-visible availability requirement; surviving instance count alone is not sufficient.
  'Approved failure affects only the supplied components in one AZ. Abort criteria were defined before the experiment and enforced; client behavior was monitored throughout. Unrelated components were unchanged.
```text
case_id: "az-path-fails"
failed_scope: "supplied AZ components"
abort_criteria: "Stop on reaching supplied client failure limit"
independent_capacity_remains: true
remaining_request_path: "unavailable"
client_required_behavior: "fail"
```' -> Required service behavior failed  (column client_required_behavior, role=categorical)
      feedback: Judgement: Required service behavior failed. Compare the stated evidence with the required criterion.
  'Approved failure affects only the supplied components in one AZ. Abort criteria were defined before the experiment and enforced; client behavior was monitored throughout. Unrelated components were unchanged.
```text
case_id: "az-path-passes"
failed_scope: "supplied AZ components"
abort_criteria: "Stop on reaching supplied client failure limit"
independent_capacity_remains: true
remaining_request_path: "available"
client_required_behavior: "pass"
```' -> Required service behavior verified  (column client_required_behavior, role=categorical)
      feedback: Judgement: Required service behavior verified. Compare the stated evidence with the required criterion.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. Only the approved components in one AZ are affected, the defined abort criteria are enforced, and the result is judged against the supplied service requirement using client-request outcomes and remaining-path evidence rather than surviving instance count alone.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r02
  MEASURES: A:bound_az_component_failure_and_monitor_client_behavior(f2); A:verify_availability_using_remaining_capacity_and_request_path(f3)   anchors=['practice', 'assessment:bound_az_component_failure_and_monitor_client_behavior', 'assessment:verify_availability_using_remaining_capacity_and_request_path']
  taught-before-tested: A.f2←s01; A.f3←s01

### s05 · recap · Keep these distinctions
(takeaway) Bound the failure and abort criteria. Judge availability by required client behavior and the remaining independent path, not survivor count. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Delete exercise resources safely: Next: Delete exercise resources safely.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the evidence
(mechanism) Resilience testing deliberately introduces failures to check availability requirements. Bound the approved experiment to the supplied AZ components, define abort criteria and monitor client-visible behavior. ⟦A.f1 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Compare the supplied cases: independent capacity remains in both, but only the case with a working client request path demonstrates the required behavior. Preserve scope, abort criteria and client outcomes together; do not widen the experiment beyond the approved AZ components. ⟦A.f1 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.az_availability cols=['case_id', 'failed_scope', 'abort_criteria', 'independent_capacity_remains', 'remaining_request_path', 'client_required_behavior'] ] caption: 
### r02 · Separate the evidence
(mechanism) Resilience testing deliberately introduces failures to check availability requirements. Bound the approved experiment to the supplied AZ components, define abort criteria and monitor client-visible behavior. ⟦A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Verify that remaining independent capacity and the request path maintain required service behavior. Surviving instances alone do not prove availability. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Compare the supplied cases: independent capacity remains in both, but only the case with a working client request path demonstrates the required behavior. Preserve scope, abort criteria and client outcomes together; do not widen the experiment beyond the approved AZ components. ⟦A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.az_availability cols=['case_id', 'failed_scope', 'abort_criteria', 'independent_capacity_remains', 'remaining_request_path', 'client_required_behavior'] ] caption: 

=========

# EVALUATOR PACKET — Delete exercise resources safely (aws_devops.tile.103)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = cost.safe_teardown — Safe teardown

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (cost.safe_teardown)   objective: Delete exercise resources safely
A.f1: Resource deletion must respect dependencies; CloudFormation uses resource relationships when deleting a stack.   [sources: aws_cloudformation_user_guide#cfn-console-delete-stack.html]
A.f2: Identify only the supplied exercise resources by stack membership or approved tags, remove dependent resources before their prerequisites and verify deletion results.   [sources: aws_cloudformation_user_guide#cfn-console-delete-stack.html]
A.f3: An S3 bucket must be empty before deletion; remove the exercise bucket’s objects, all object versions and delete markers before deleting that bucket.   [sources: aws_s3_user_guide#delete-bucket.html]
A.f4: Retained resources and failed deletions need explicit inspection and approved follow-up; a completed deletion operation is not billing verification.   [sources: aws_cloudformation_user_guide#cfn-console-delete-stack.html]
note: Use approved scope and dependency order; leave residual-charge verification to its later concept.
PRACTICE ANCHOR (tool_simulation): Delete one supplied tagged sandbox exercise using approved tags or stack membership to establish scope. Remove dependents before prerequisites, empty the exercise S3 bucket of objects, all object versions and delete markers before deleting it, and inspect deletion results.  SUCCESS: Only approved exercise resources are targeted, and unrelated resources remain unchanged. Removal respects dependencies, including complete bucket-content cleanup before bucket deletion. Each deletion result is inspected; retained resources and failures are identified for approved follow-up rather than treated as removed. Completion is reported as a resource-removal result, not billing verification.
ASSESSMENT ANCHOR: verify_exercise_only_deletion_scope facts=['f2']
ASSESSMENT ANCHOR: verify_dependency_ordered_resource_removal facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_bucket_contents_removed_before_bucket_deletion facts=['f3']
ASSESSMENT ANCHOR: inspect_deletion_results_and_identify_approved_follow_up facts=['f2', 'f4']

## DATA ASSETS USED
ds.teardown: Safe teardown — read-only evidence — columns: resource(identifier), scope_evidence(text), remove_before(text), deletion_result(categorical), follow_up(text)
   ["objects","approved exercise stack","S3 bucket","removed",""]
   ["object versions","approved exercise stack","S3 bucket","removed",""]
   ["delete markers","approved exercise stack","S3 bucket","removed",""]
   ["S3 bucket","approved exercise stack","","removed",""]
   ["retained exercise resource","approved exercise stack","","retained","Inspect retention and obtain approved follow-up"]
   ["failed exercise resource","approved exercise tags","","failed","Inspect failure and obtain approved follow-up"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Approval stop; Audit evidence; Audit evidence integrity; Audit storage retention; Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template; directly require the native EC2 instance foundation; Backend configuration; Block release on actionable dependency or image security findings; Control environment promotion with a manual approval; Credential readiness; Diagnose EC2 or container health failures using telemetry and prepared Linux inspection skills; Diagnose a failed delivery pipeline action; Document incident evidence and a preventive change using reused systematic-debugging coverage; Endpoint cutover; Gate release completion on a deployed-service smoke check; Handle failed event delivery with bounded retries and failure capture; Perform a controlled ECS service rollout; Promote the same artifact version across environments; Recover an incident safely using an established runbook; Rehearsal isolation; Replacement controls; Residual charge verification; State access isolation; State locking; Verify restored service and data against RTO/RPO in an isolated rehearsal

## LESSON, in learner order

### s01 · explainer · Delete exercise resources safely
Read the evidence — 
(mechanism) Delete only exercise resources identified by stack membership or approved tags. Remove dependents before prerequisites and verify results. CloudFormation uses resource relationships when deleting a stack. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3⟧
(mechanism) Empty the exercise S3 bucket before deletion: remove objects, all object versions and delete markers. ⟦A.f3 A:tb1 A:tb2 A:tb3⟧
(mechanism) Inspect retained resources and failed deletions for approved follow-up. Completed deletion is not billing verification. ⟦A.f4 A:tb1 A:tb2 A:tb3⟧
[PROCESS_FLOW] nodes=['Approved stack membership or tags', 'Remove dependents before prerequisites; CloudFormation uses relationships', 'Remove objects, all object versions and delete markers', 'Delete empty exercise S3 bucket', 'Inspect deletion results', 'Confirmed removal', 'Retained or failed: inspect and obtain approved follow-up'] edges=[('n0', 'n1', 'bounded scope'), ('n1', 'n2', 'dependent-first'), ('n2', 'n3', 'bucket empty'), ('n3', 'n4', 'verify'), ('n4', 'n5', 'removed'), ('n4', 'n6', 'retained or failed')] alt: Make the approved exercise boundary and dependent-first removal sequence visible. Show objects, all object versions and delete markers being removed before the S3 bucket, CloudFormation using resource relationships during stack deletion, and deletion results branching into confirmed removal or retained/failed resources requiring inspection and approved follow-up. Keep billing verification outside this teardown flow.
[TABLE ds.teardown cols=['resource', 'scope_evidence', 'remove_before', 'deletion_result', 'follow_up'] ] caption: 

### s02 · explainer · Compare the evidence
Read the evidence — 
(example) A current object listing is not complete version cleanup. The bucket also needs all versions and delete markers removed. Inspect retained and failed resources rather than assuming the completed operation removed everything; this flow verifies deletion, not charges. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Review exercise deletion evidence
Check your understanding — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] A supplied exercise resource depends on another exercise resource. Which removal rule respects scope and dependencies?
  ✔ a: Confirm approved exercise membership, remove the dependent resource before its prerequisite, and verify each deletion result.
      why: Correct. Confirm approved exercise membership, remove the dependent resource before its prerequisite, and verify each deletion result.
  ✘ b: Delete the prerequisite first and infer dependent removal from that request.
      why: Dependencies determine removal order; a deletion request is not proof of each resource removal.
  ✘ c: Delete similarly named resources without checking approved tags or stack membership.
      why: Only resources identified by the supplied exercise membership or approved tags are in scope.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. Only approved exercise resources are targeted, and unrelated resources remain unchanged. Removal respects dependencies, including complete bucket-content cleanup before bucket deletion. Each deletion result is inspected; retained resources and failures are identified for approved follow-up rather than treated as removed. Completion is reported as a resource-removal result, not billing verification.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r01
  MEASURES: A:verify_dependency_ordered_resource_removal(f1,f2)   anchors=['assessment:verify_dependency_ordered_resource_removal']
  taught-before-tested: A.f1←s01; A.f2←s01

### s04 · hands_on · Review exercise deletion evidence
Evidence review — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read the deletion records and scope/order excerpts. Decide which demonstrate removal, need approved follow-up, or violate the exercise-only/dependency requirements. A removal result is not billing verification.
  'All rows belong to approved exercise resources. Objects, all object versions and delete markers were removed and inspected before the bucket; other dependents were removed before prerequisites. Unrelated resources were unchanged.
```text
resource: "objects"
scope_evidence: "approved exercise stack"
remove_before: "S3 bucket"
deletion_result: "removed"
follow_up: ""
```' -> Inspected resource removal  (column deletion_result, role=categorical)
      feedback: Judgement: Inspected resource removal. Compare the stated evidence with the required criterion.
  'All rows belong to approved exercise resources. Objects, all object versions and delete markers were removed and inspected before the bucket; other dependents were removed before prerequisites. Unrelated resources were unchanged.
```text
resource: "object versions"
scope_evidence: "approved exercise stack"
remove_before: "S3 bucket"
deletion_result: "removed"
follow_up: ""
```' -> Inspected resource removal  (column deletion_result, role=categorical)
      feedback: Judgement: Inspected resource removal. Compare the stated evidence with the required criterion.
  'All rows belong to approved exercise resources. Objects, all object versions and delete markers were removed and inspected before the bucket; other dependents were removed before prerequisites. Unrelated resources were unchanged.
```text
resource: "delete markers"
scope_evidence: "approved exercise stack"
remove_before: "S3 bucket"
deletion_result: "removed"
follow_up: ""
```' -> Inspected resource removal  (column deletion_result, role=categorical)
      feedback: Judgement: Inspected resource removal. Compare the stated evidence with the required criterion.
  'All rows belong to approved exercise resources. Objects, all object versions and delete markers were removed and inspected before the bucket; other dependents were removed before prerequisites. Unrelated resources were unchanged.
```text
resource: "S3 bucket"
scope_evidence: "approved exercise stack"
remove_before: ""
deletion_result: "removed"
follow_up: ""
```' -> Inspected resource removal  (column deletion_result, role=categorical)
      feedback: Judgement: Inspected resource removal. Compare the stated evidence with the required criterion.
  'All rows belong to approved exercise resources. Objects, all object versions and delete markers were removed and inspected before the bucket; other dependents were removed before prerequisites. Unrelated resources were unchanged.
```text
resource: "retained exercise resource"
scope_evidence: "approved exercise stack"
remove_before: ""
deletion_result: "retained"
follow_up: "Inspect retention and obtain approved follow-up"
```' -> Retained or failed: approved follow-up needed  (column deletion_result, role=categorical)
      feedback: Judgement: Retained or failed: approved follow-up needed. Compare the stated evidence with the required criterion.
  'All rows belong to approved exercise resources. Objects, all object versions and delete markers were removed and inspected before the bucket; other dependents were removed before prerequisites. Unrelated resources were unchanged.
```text
resource: "failed exercise resource"
scope_evidence: "approved exercise tags"
remove_before: ""
deletion_result: "failed"
follow_up: "Inspect failure and obtain approved follow-up"
```' -> Retained or failed: approved follow-up needed  (column deletion_result, role=categorical)
      feedback: Judgement: Retained or failed: approved follow-up needed. Compare the stated evidence with the required criterion.
  'Alternate excerpt: delete an unrelated bucket merely because its name resembles the exercise bucket.' -> Unsafe scope or ordering
      feedback: Judgement: Unsafe scope or ordering. Compare the stated evidence with the required criterion.
  'Alternate excerpt: bucket deletion is attempted while object versions and delete markers remain.' -> Unsafe scope or ordering
      feedback: Judgement: Unsafe scope or ordering. Compare the stated evidence with the required criterion.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. Only approved exercise resources are targeted, and unrelated resources remain unchanged. Removal respects dependencies, including complete bucket-content cleanup before bucket deletion. Each deletion result is inspected; retained resources and failures are identified for approved follow-up rather than treated as removed. Completion is reported as a resource-removal result, not billing verification.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r02
  MEASURES: A:verify_exercise_only_deletion_scope(f2); A:verify_bucket_contents_removed_before_bucket_deletion(f3); A:inspect_deletion_results_and_identify_approved_follow_up(f2,f4)   anchors=['practice', 'assessment:verify_exercise_only_deletion_scope', 'assessment:verify_bucket_contents_removed_before_bucket_deletion', 'assessment:inspect_deletion_results_and_identify_approved_follow_up']
  taught-before-tested: A.f2←s01; A.f3←s01; A.f2←s01; A.f4←s01

### s05 · recap · Keep these distinctions
(takeaway) Delete approved exercise resources dependent-first. Empty all S3 versions and delete markers; inspect retained or failed resources without claiming billing verification. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Verify recovery credential readiness: Next: Verify recovery credential readiness.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the evidence
(mechanism) Delete only exercise resources identified by stack membership or approved tags. Remove dependents before prerequisites and verify results. CloudFormation uses resource relationships when deleting a stack. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) A current object listing is not complete version cleanup. The bucket also needs all versions and delete markers removed. Inspect retained and failed resources rather than assuming the completed operation removed everything; this flow verifies deletion, not charges. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.teardown cols=['resource', 'scope_evidence', 'remove_before', 'deletion_result', 'follow_up'] ] caption: 
### r02 · Separate the evidence
(mechanism) Delete only exercise resources identified by stack membership or approved tags. Remove dependents before prerequisites and verify results. CloudFormation uses resource relationships when deleting a stack. ⟦A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Empty the exercise S3 bucket before deletion: remove objects, all object versions and delete markers. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Inspect retained resources and failed deletions for approved follow-up. Completed deletion is not billing verification. ⟦A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) A current object listing is not complete version cleanup. The bucket also needs all versions and delete markers removed. Inspect retained and failed resources rather than assuming the completed operation removed everything; this flow verifies deletion, not charges. ⟦A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.teardown cols=['resource', 'scope_evidence', 'remove_before', 'deletion_result', 'follow_up'] ] caption: 

=========

# EVALUATOR PACKET — Verify recovery credential readiness / Isolate a recovery rehearsal (aws_devops.tile.104)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = recovery.credential_readiness — Credential readiness
B = recovery.rehearsal_isolation — Rehearsal isolation

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (recovery.credential_readiness)   objective: Verify recovery credential readiness
A.f1: Recovery execution needs a valid, unexpired session with the permissions required for backup access and resource creation.   [sources: aws_iam_user_guide#id_credentials_temp_use-resources.html]
A.f2: Establish the approved recovery session, inspect its identity and expiry, and test the supplied backup-read and recovery-resource operations before rehearsal.   [sources: aws_iam_user_guide#id_credentials_temp_use-resources.html]
A.f3: A valid credential lifetime does not prove sufficient authorization; verify both access outcomes and lifetime.   [sources: aws_iam_user_guide#id_credentials_temp_use-resources.html]
note: Use approved session provider and safe supplied tests; do not expose credentials.
PRACTICE ANCHOR (tool_simulation): Test one approved recovery session before rehearsal using the supplied identity, expiry, backup-read, and recovery-resource checks without exposing credentials.  SUCCESS: The approved session is established, its identity and expiry are inspected, and both supplied operation outcomes are recorded alongside its lifetime. Readiness requires the expected identity, a valid unexpired session, and successful backup-read and recovery-resource operations; an unexpired session with a denied operation is identified as not ready.
ASSESSMENT ANCHOR: verify_recovery_session_identity_and_expiry facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_backup_access_and_recovery_resource_creation facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: distinguish_session_lifetime_from_authorization facts=['f3']

## SOURCE FACTS — B (recovery.rehearsal_isolation)   objective: Isolate a recovery rehearsal
B.f1: Recovery testing should use a controlled environment that limits the experiment’s effects.   [sources: aws_well_architected_framework#rel12-bp04.html]
B.f2: Prepare the supplied isolated account and network target and check restoration destinations and client test traffic do not point to production.   [sources: aws_well_architected_framework#rel12-bp04.html]
B.f3: Record the approved scope and stop conditions before provisioning recovery resources or directing test traffic.   [sources: aws_well_architected_framework#rel12-bp04.html]
note: Use supplied isolated target; do not create production cutover or new network-isolation design.
PRACTICE ANCHOR (tool_simulation): Prepare one recovery target using the supplied isolated account and network boundaries. Inspect restoration destinations and client test traffic settings, and record the approved scope and stop conditions before provisioning resources or directing test traffic.  SUCCESS: The prepared target uses the supplied isolated account and network. Restoration destinations and client test traffic settings do not point to production, and the approved scope and stop conditions are recorded before any provisioning or test traffic begins.
ASSESSMENT ANCHOR: verify_restoration_destinations_and_test_traffic_are_isolated_from_production facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_scope_and_stop_conditions_are_recorded_before_rehearsal_actions facts=['f3']

## DATA ASSETS USED
ds.recovery_readiness: Credential readiness — read-only evidence — columns: session(identifier), acting_role(identifier), checked_at(datetime), expires_at(datetime), backup_read(categorical), recovery_resource(categorical)
   ["recovery-denied","exercise-recovery-role","2026-01-15T10:00:00+00:00","2026-01-15T11:30:00+00:00","denied","allowed"]
   ["recovery-ready","exercise-recovery-role","2026-01-15T10:10:00+00:00","2026-01-15T11:30:00+00:00","allowed","allowed"]
ds.rehearsal_targets: Rehearsal isolation — read-only evidence — columns: setting(categorical), account(identifier), target_environment(categorical), destination(text), approved_scope(text), stop_condition(text)
   ["restoration","exercise-isolated-account","isolated recovery","exercise-recovery-network","isolated recovery only","Stop if a destination points to production"]
   ["client test traffic","exercise-isolated-account","isolated recovery","exercise-recovery-endpoint","isolated recovery only","Stop if a destination points to production"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Approval stop; Audit evidence; Audit evidence integrity; Audit storage retention; Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template; directly require the native EC2 instance foundation; Backend configuration; Block release on actionable dependency or image security findings; Control environment promotion with a manual approval; Diagnose EC2 or container health failures using telemetry and prepared Linux inspection skills; Diagnose a failed delivery pipeline action; Document incident evidence and a preventive change using reused systematic-debugging coverage; Endpoint cutover; Gate release completion on a deployed-service smoke check; Handle failed event delivery with bounded retries and failure capture; Perform a controlled ECS service rollout; Promote the same artifact version across environments; Recover an incident safely using an established runbook; Rehearsal isolation; Replacement controls; Residual charge verification; State access isolation; State locking; Verify restored service and data against RTO/RPO in an isolated rehearsal

## LESSON, in learner order

### s01 · explainer · Verify recovery credential readiness
Read the evidence — 
(mechanism) Recovery needs a valid, unexpired session with permissions for backup access and resource creation. Establish the approved session and inspect identity and expiry. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Before rehearsal, test the supplied backup-read and recovery-resource operations. Record both outcomes alongside lifetime. Unexpired credentials with denied backup access are not ready; successful access does not remove the lifetime requirement. ⟦A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[DIAGRAM] nodes=['Approved session identity and expiry', 'Backup-read authorization outcome', 'Recovery-resource authorization outcome'] edges=[] alt: Show the approved recovery session's identity and expiry alongside the supplied backup-read and recovery-resource test outcomes, making lifetime and authorization separately visible without displaying credentials.
[TABLE ds.recovery_readiness cols=['session', 'acting_role', 'checked_at', 'expires_at', 'backup_read', 'recovery_resource'] ] caption: 

### s02 · check · Review recovery session readiness
Check your understanding — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] An approved recovery session is unexpired, but the supplied backup-read test is denied. What does this establish?
  ✔ a: The session is not ready: valid lifetime does not establish sufficient authorization.
      why: Correct. The session is not ready: valid lifetime does not establish sufficient authorization.
  ✘ b: The session is ready because its expiration time is still in the future.
      why: Credential lifetime and authorization are separate requirements.
  ✘ c: The denied operation can be omitted from the readiness record.
      why: Access outcomes must be verified, not hidden by a valid lifetime.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The approved session is established, its identity and expiry are inspected, and both supplied operation outcomes are recorded alongside its lifetime. Readiness requires the expected identity, a valid unexpired session, and successful backup-read and recovery-resource operations; an unexpired session with a denied operation is identified as not ready.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r01
  MEASURES: A:distinguish_session_lifetime_from_authorization(f3)   anchors=['assessment:distinguish_session_lifetime_from_authorization']
  taught-before-tested: A.f3←s01

### s03 · hands_on · Review recovery session readiness
Evidence review — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, core, grading=client] Read the inspected session and operation records. Decide which approved recovery session is ready and which is not; judge lifetime and both access outcomes.
  'Expected identity is exercise-recovery-role. The approved session was established and its identity and expiry inspected at checked_at; both supplied operation results are recorded.
```text
session: "recovery-denied"
acting_role: "exercise-recovery-role"
checked_at: "2026-01-15T10:00:00+00:00"
expires_at: "2026-01-15T11:30:00+00:00"
backup_read: "denied"
recovery_resource: "allowed"
```' -> Not ready for rehearsal  (column backup_read, role=categorical)
      feedback: Judgement: Not ready for rehearsal. Compare the stated evidence with the required criterion.
  'Expected identity is exercise-recovery-role. The approved session was established and its identity and expiry inspected at checked_at; both supplied operation results are recorded.
```text
session: "recovery-ready"
acting_role: "exercise-recovery-role"
checked_at: "2026-01-15T10:10:00+00:00"
expires_at: "2026-01-15T11:30:00+00:00"
backup_read: "allowed"
recovery_resource: "allowed"
```' -> Ready for rehearsal  (column backup_read, role=categorical)
      feedback: Judgement: Ready for rehearsal. Compare the stated evidence with the required criterion.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The approved session is established, its identity and expiry are inspected, and both supplied operation outcomes are recorded alongside its lifetime. Readiness requires the expected identity, a valid unexpired session, and successful backup-read and recovery-resource operations; an unexpired session with a denied operation is identified as not ready.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r02
  MEASURES: A:verify_recovery_session_identity_and_expiry(f1,f2); A:verify_backup_access_and_recovery_resource_creation(f1,f2,f3); A:distinguish_session_lifetime_from_authorization(f3)   anchors=['practice', 'assessment:verify_recovery_session_identity_and_expiry', 'assessment:verify_backup_access_and_recovery_resource_creation', 'assessment:distinguish_session_lifetime_from_authorization']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f1←s01; A.f2←s01; A.f3←s01; A.f3←s01

### s04 · explainer · Isolate a recovery rehearsal
Read the evidence — 
(mechanism) A recovery test belongs in a controlled environment that limits its effects. Prepare the supplied isolated account and network target. ⟦B.f1 B.f2 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Check that restoration destinations and client test traffic do not point to production. Record approved scope and stop conditions before provisioning resources or directing traffic. A sandbox label alone is not evidence of isolation. ⟦B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[DIAGRAM] nodes=['Approved scope and stop conditions', 'Isolated recovery account and network', 'Restoration destination', 'Client test traffic', 'Production: outside rehearsal paths'] edges=[('n0', 'n1', 'before action'), ('n2', 'n1', 'confined to'), ('n3', 'n1', 'confined to')] alt: Make the supplied isolated account and network boundaries visible, with restoration destinations and client test traffic paths confined to the recovery target and production clearly outside those paths.
[TABLE ds.rehearsal_targets cols=['setting', 'account', 'target_environment', 'destination', 'approved_scope', 'stop_condition'] ] caption: 

### s05 · check · Review rehearsal boundaries
Check your understanding — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [choice, core, grading=client] When must the approved rehearsal scope and stop conditions be recorded?
  ✔ a: Before provisioning recovery resources or directing client test traffic.
      why: Correct. Before provisioning recovery resources or directing client test traffic.
  ✘ b: After provisioning, but before the first client test request.
      why: Provisioning is already a rehearsal action; scope and stop conditions must precede it.
  ✘ c: Only after the rehearsal finishes successfully.
      why: A later record does not bound the actions before they happen.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The prepared target uses the supplied isolated account and network. Restoration destinations and client test traffic settings do not point to production, and the approved scope and stop conditions are recorded before any provisioning or test traffic begins.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r03
  MEASURES: B:verify_scope_and_stop_conditions_are_recorded_before_rehearsal_actions(f3)   anchors=['assessment:verify_scope_and_stop_conditions_are_recorded_before_rehearsal_actions']
  taught-before-tested: B.f3←s04

### s06 · hands_on · Review rehearsal boundaries
Evidence review — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each target excerpt and the alternate configuration. Decide whether isolation, prior scope and stop-condition recording are satisfied.
  'Before any provisioning or test traffic, approved scope and stop conditions were recorded. Both restoration and client-traffic settings were checked against the supplied isolated account and network.
```text
setting: "restoration"
account: "exercise-isolated-account"
target_environment: "isolated recovery"
destination: "exercise-recovery-network"
approved_scope: "isolated recovery only"
stop_condition: "Stop if a destination points to production"
```' -> Isolated and bounded before actions  (column target_environment, role=categorical)
      feedback: Judgement: Isolated and bounded before actions. Compare the stated evidence with the required criterion.
  'Before any provisioning or test traffic, approved scope and stop conditions were recorded. Both restoration and client-traffic settings were checked against the supplied isolated account and network.
```text
setting: "client test traffic"
account: "exercise-isolated-account"
target_environment: "isolated recovery"
destination: "exercise-recovery-endpoint"
approved_scope: "isolated recovery only"
stop_condition: "Stop if a destination points to production"
```' -> Isolated and bounded before actions  (column target_environment, role=categorical)
      feedback: Judgement: Isolated and bounded before actions. Compare the stated evidence with the required criterion.
  'Alternate setting: approved scope is isolated recovery only, but restoration destination points to production.' -> Violates isolation or prior boundary
      feedback: Judgement: Violates isolation or prior boundary. Compare the stated evidence with the required criterion.
  'Alternate setting: isolated destinations are correct, but scope and stop conditions were first recorded after provisioning began.' -> Violates isolation or prior boundary
      feedback: Judgement: Violates isolation or prior boundary. Compare the stated evidence with the required criterion.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The prepared target uses the supplied isolated account and network. Restoration destinations and client test traffic settings do not point to production, and the approved scope and stop conditions are recorded before any provisioning or test traffic begins.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r04
  MEASURES: B:verify_restoration_destinations_and_test_traffic_are_isolated_from_production(f1,f2); B:verify_scope_and_stop_conditions_are_recorded_before_rehearsal_actions(f3)   anchors=['practice', 'assessment:verify_restoration_destinations_and_test_traffic_are_isolated_from_production', 'assessment:verify_scope_and_stop_conditions_are_recorded_before_rehearsal_actions']
  taught-before-tested: B.f1←s04; B.f2←s04; B.f3←s04

### s07 · recap · Keep these distinctions
(takeaway) Check session identity and expiry plus both required access operations. Lifetime alone does not prove authorization. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Keep restoration and test traffic inside the isolated target. Record approved scope and stop conditions before action. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Gate automated response with approvals and stop controls: Next: Gate automated response with approvals and stop controls.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the evidence
(mechanism) Before rehearsal, test the supplied backup-read and recovery-resource operations. Record both outcomes alongside lifetime. Unexpired credentials with denied backup access are not ready; successful access does not remove the lifetime requirement. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) An unexpired session can still lack backup-read permission. Read the session lifetime and both operation outcomes as separate readiness requirements. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.recovery_readiness cols=['session', 'acting_role', 'checked_at', 'expires_at', 'backup_read', 'recovery_resource'] ] caption: 
### r02 · Separate the evidence
(mechanism) Recovery needs a valid, unexpired session with permissions for backup access and resource creation. Establish the approved session and inspect identity and expiry. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Before rehearsal, test the supplied backup-read and recovery-resource operations. Record both outcomes alongside lifetime. Unexpired credentials with denied backup access are not ready; successful access does not remove the lifetime requirement. ⟦A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) An unexpired session can still lack backup-read permission. Read the session lifetime and both operation outcomes as separate readiness requirements. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.recovery_readiness cols=['session', 'acting_role', 'checked_at', 'expires_at', 'backup_read', 'recovery_resource'] ] caption: 
### r03 · Separate the evidence
(mechanism) Check that restoration destinations and client test traffic do not point to production. Record approved scope and stop conditions before provisioning resources or directing traffic. A sandbox label alone is not evidence of isolation. ⟦B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(misconception) A named recovery target is not enough if restoration or client traffic points to production. Check actual destinations within the recorded scope and stop conditions. ⟦B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.rehearsal_targets cols=['setting', 'account', 'target_environment', 'destination', 'approved_scope', 'stop_condition'] ] caption: 
### r04 · Separate the evidence
(mechanism) A recovery test belongs in a controlled environment that limits its effects. Prepare the supplied isolated account and network target. ⟦B.f1 B.f2 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Check that restoration destinations and client test traffic do not point to production. Record approved scope and stop conditions before provisioning resources or directing traffic. A sandbox label alone is not evidence of isolation. ⟦B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(misconception) A named recovery target is not enough if restoration or client traffic points to production. Check actual destinations within the recorded scope and stop conditions. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.rehearsal_targets cols=['setting', 'account', 'target_environment', 'destination', 'approved_scope', 'stop_condition'] ] caption: 

=========

# EVALUATOR PACKET — Gate automated response with approvals and stop controls / Capture automated-response audit evidence (aws_devops.tile.106)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = response.approval_stop — Approval stop
B = response.audit_evidence — Audit evidence

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (response.approval_stop)   objective: Gate automated response with approvals and stop controls
A.f1: An aws:approve Automation step pauses execution pending approval or rejection by the designated approvers.   [sources: aws_systems_manager_user_guide#automation-action-approve.html]
A.f2: Put the approval step before the protected operation and use the supplied branching or failure path to prevent that operation on rejection or stop.   [sources: aws_systems_manager_user_guide#automation-action-approve.html]
A.f3: Stop an Automation execution with the approved stop operation when a stop condition occurs and inspect execution state before allowing further actions.   [sources: aws_systems_manager_user_guide#../../../systems-manager/latest/APIReference/API_StopAutomationExecution.html]
note: Use supplied branching and stop operation; do not invent Automation document syntax.
PRACTICE ANCHOR (tool_simulation): Add the supplied aws:approve gate before the protected operation in a bounded remediation workflow. Connect the supplied rejection or failure path, then use the approved stop operation when the supplied stop condition occurs.  SUCCESS: The workflow pauses for designated approvers before the protected operation. Pending approval, rejection, and stop do not permit that operation. After requesting a stop, execution state is inspected before any further action is allowed.
ASSESSMENT ANCHOR: verify_pending_or_rejected_approval_blocks_protected_operation facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_stopped_execution_blocks_protected_operation_before_further_actions facts=['f2', 'f3']

## SOURCE FACTS — B (response.audit_evidence)   objective: Capture automated-response audit evidence
B.f1: Automation execution details include an execution identifier, step statuses, inputs, outputs and failure information.   [sources: aws_systems_manager_user_guide#../../../systems-manager/latest/APIReference/API_GetAutomationExecution.html]
B.f2: Record execution ID, acting role, target identities, start/end times and per-step outcomes for the supplied response.   [sources: aws_systems_manager_user_guide#../../../systems-manager/latest/APIReference/API_GetAutomationExecution.html]
B.f3: Use CloudTrail request identity and operation evidence to attribute the underlying AWS actions; success and failure outcomes both belong in the response record.   [sources: aws_cloudtrail_user_guide#cloudtrail-event-reference-record-contents.html]
note: Use supplied execution/CloudTrail records; do not infer actions from the operator’s intended plan.
PRACTICE ANCHOR (field_selection): Capture the execution ID, acting role, target identities, start/end times and per-step outcomes for one supplied response run. Include inputs, outputs and failure information, and select CloudTrail request identity and operation evidence that attributes the underlying AWS actions.  SUCCESS: The completed response record accurately captures the supplied execution identifiers, authority, targets, times and step details, links underlying actions to CloudTrail evidence, and retains both successful and failed outcomes without inferring actions from the intended plan.
ASSESSMENT ANCHOR: identify_response_execution_and_per_step_outcomes facts=['f1', 'f2']
ASSESSMENT ANCHOR: attribute_aws_operations_to_acting_authority_and_targets facts=['f2', 'f3']
ASSESSMENT ANCHOR: recognize_success_and_failure_evidence facts=['f1', 'f3']

## DATA ASSETS USED
ds.approval_states: Approval stop — read-only evidence — columns: execution_id(identifier), approval_step(categorical), execution_state(categorical), protected_operation_executed(categorical)
   ["approval-pending","aws:approve","pending",false]
   ["approval-rejected","aws:approve","rejected",false]
   ["approval-stopped","aws:approve","stopped",false]
ds.response_audit: Audit evidence — read-only evidence — columns: execution_id(identifier), acting_role(identifier), target(identifier), start_time(datetime), end_time(datetime), step(identifier), step_start_time(datetime), step_end_time(datetime), step_status(categorical), inputs(text), outputs(text), failure_information(text), cloudtrail_request_id(identifier), cloudtrail_request_identity(identifier), cloudtrail_operation(categorical)
   ["response-exercise","exercise-recovery-role","exercise-backup","2026-01-15T10:00:00+00:00","2026-01-15T10:05:00+00:00","read_backup","2026-01-15T10:00:00+00:00","2026-01-15T10:01:00+00:00","Success","Supplied exercise target","Backup-read test allowed","","request-read_backup","exercise-recovery-ro
   ["response-exercise","exercise-recovery-role","exercise-recovery-stack","2026-01-15T10:00:00+00:00","2026-01-15T10:05:00+00:00","create_recovery","2026-01-15T10:01:00+00:00","2026-01-15T10:02:00+00:00","Failed","Supplied exercise target","","Supplied recovery-resource test denied","request-create_re

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Audit evidence; Audit evidence integrity; Audit storage retention; Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template; directly require the native EC2 instance foundation; Backend configuration; Block release on actionable dependency or image security findings; Control environment promotion with a manual approval; Diagnose EC2 or container health failures using telemetry and prepared Linux inspection skills; Diagnose a failed delivery pipeline action; Document incident evidence and a preventive change using reused systematic-debugging coverage; Endpoint cutover; Gate release completion on a deployed-service smoke check; Handle failed event delivery with bounded retries and failure capture; Perform a controlled ECS service rollout; Promote the same artifact version across environments; Recover an incident safely using an established runbook; Replacement controls; Residual charge verification; State access isolation; State locking; Verify restored service and data against RTO/RPO in an isolated rehearsal

## LESSON, in learner order

### s01 · explainer · Gate automated response with approvals and stop controls
Read the evidence — 
(mechanism) An aws:approve Automation step pauses for the designated approvers to approve or reject. Place it before the protected operation; a pending request is not approval. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Use the supplied branching or failure path to prevent the protected operation on rejection or stop. When a stop condition occurs, use the approved stop operation and inspect execution state before allowing further actions. ⟦A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[DIAGRAM] nodes=['aws:approve: pending designated decision', 'Rejected or stopped execution', 'Protected operation: unexecuted'] edges=[('n0', 'n2', 'must precede'), ('n1', 'n2', 'prevents execution')] alt: Make the approval step's position before the protected operation visible, together with pending, rejected, and stopped execution states and the protected operation remaining unexecuted in each case.
[TABLE ds.approval_states cols=['execution_id', 'approval_step', 'execution_state', 'protected_operation_executed'] ] caption: 

### s02 · check · Review approval and stop states
Check your understanding — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] A stop condition occurs in an Automation response. What must happen before any further action is allowed?
  ✔ a: Request the approved stop operation and inspect execution state before allowing further actions.
      why: Correct. Request the approved stop operation and inspect execution state before allowing further actions.
  ✘ b: Request stop and immediately allow the protected operation without inspecting state.
      why: A stop request alone does not replace inspecting execution state.
  ✘ c: Ignore the stop condition because an approval step exists in the workflow.
      why: The approval step does not nullify a stop condition.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The workflow pauses for designated approvers before the protected operation. Pending approval, rejection, and stop do not permit that operation. After requesting a stop, execution state is inspected before any further action is allowed.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r01
  MEASURES: A:verify_stopped_execution_blocks_protected_operation_before_further_actions(f2,f3)   anchors=['assessment:verify_stopped_execution_blocks_protected_operation_before_further_actions']
  taught-before-tested: A.f2←s01; A.f3←s01

### s03 · hands_on · Review approval and stop states
Evidence review — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, core, grading=client] Read each approval/stop excerpt. Decide whether the protected operation is correctly blocked, or whether the alternate path improperly allows it.
  'aws:approve precedes the protected operation and waits for designated approvers. Rejection follows the supplied blocking path. In the stopped case, the approved stop operation was requested and execution state inspected before considering further action.
```text
execution_id: "approval-pending"
approval_step: "aws:approve"
execution_state: "pending"
protected_operation_executed: false
```' -> Correctly blocked before protected operation  (column protected_operation_executed, role=categorical)
      feedback: Judgement: Correctly blocked before protected operation. Compare the stated evidence with the required criterion.
  'aws:approve precedes the protected operation and waits for designated approvers. Rejection follows the supplied blocking path. In the stopped case, the approved stop operation was requested and execution state inspected before considering further action.
```text
execution_id: "approval-rejected"
approval_step: "aws:approve"
execution_state: "rejected"
protected_operation_executed: false
```' -> Correctly blocked before protected operation  (column protected_operation_executed, role=categorical)
      feedback: Judgement: Correctly blocked before protected operation. Compare the stated evidence with the required criterion.
  'aws:approve precedes the protected operation and waits for designated approvers. Rejection follows the supplied blocking path. In the stopped case, the approved stop operation was requested and execution state inspected before considering further action.
```text
execution_id: "approval-stopped"
approval_step: "aws:approve"
execution_state: "stopped"
protected_operation_executed: false
```' -> Correctly blocked before protected operation  (column protected_operation_executed, role=categorical)
      feedback: Judgement: Correctly blocked before protected operation. Compare the stated evidence with the required criterion.
  'Alternate excerpt: execution_state: pending; protected operation begins while designated approvers have not decided.' -> Protected operation improperly allowed
      feedback: Judgement: Protected operation improperly allowed. Compare the stated evidence with the required criterion.
  'Alternate excerpt: stop condition occurs; stop is requested; protected operation proceeds without execution-state inspection.' -> Protected operation improperly allowed
      feedback: Judgement: Protected operation improperly allowed. Compare the stated evidence with the required criterion.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The workflow pauses for designated approvers before the protected operation. Pending approval, rejection, and stop do not permit that operation. After requesting a stop, execution state is inspected before any further action is allowed.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r02
  MEASURES: A:verify_pending_or_rejected_approval_blocks_protected_operation(f1,f2); A:verify_stopped_execution_blocks_protected_operation_before_further_actions(f2,f3)   anchors=['practice', 'assessment:verify_pending_or_rejected_approval_blocks_protected_operation', 'assessment:verify_stopped_execution_blocks_protected_operation_before_further_actions']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f2←s01; A.f3←s01

### s04 · explainer · Capture automated-response audit evidence
Read the evidence — 
(mechanism) Automation details include execution ID, step statuses, inputs, outputs and failure information. Record the supplied response’s execution ID, acting role, targets, start/end times and per-step outcomes. ⟦B.f1 B.f2 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Attribute underlying AWS actions using CloudTrail request identity and operation evidence. Retain both success and failure outcomes, not just a success-focused summary. ⟦B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.response_audit cols=['execution_id', 'acting_role', 'target', 'start_time', 'end_time', 'step', 'step_start_time', 'step_end_time', 'step_status', 'inputs', 'outputs', 'failure_information', 'cloudtrail_request_id', 'cloudtrail_request_identity', 'cloudtrail_operation'] ] caption: 

### s05 · check · Review response execution evidence
Check your understanding — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [choice, core, grading=client] Which response record accurately represents both successful and failed actions?
  ✔ a: Execution details retain inputs, outputs and failure information; underlying actions are linked to CloudTrail request identity and operation evidence.
      why: Correct. Execution details retain inputs, outputs and failure information; underlying actions are linked to CloudTrail request identity and operation evidence.
  ✘ b: Record only successful steps because failed steps have no useful evidence.
      why: Failure information and failed outcomes belong in the response record.
  ✘ c: Treat the intended workflow plan as proof that its AWS actions occurred.
      why: Actual request identity and operation evidence, not intention, attribute underlying actions.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The completed response record accurately captures the supplied execution identifiers, authority, targets, times and step details, links underlying actions to CloudTrail evidence, and retains both successful and failed outcomes without inferring actions from the intended plan.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r03
  MEASURES: B:recognize_success_and_failure_evidence(f1,f3)   anchors=['assessment:recognize_success_and_failure_evidence']
  taught-before-tested: B.f1←s04; B.f3←s04

### s06 · hands_on · Review response execution evidence
Evidence review — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [table_select, stretch, grading=client] 
  intro shown to learner: Read the supplied completed response record. Select the evidence that belongs in an accurate audit of both outcomes; do not infer actions from the intended plan.
  task outcome0 (row): Select the entire successful step record, preserving its execution, authority, target, times, inputs, outputs and failure details.  KEY: row={'execution_id': 'response-exercise', 'step': 'read_backup'} column=None expect=None dataset-says={'execution_id': 'response-exercise', 'acting_role': 'exercise-recovery-role', 'target': 'exercise-backup', 'start_time': '2026-01-15T10:00:00+00:00', 'end_time': '2026-01-15T10:05:00+00:00', 'step': 'read_backup', 'step_start_time': '2026-01-15T10:00:00+00:00', 'step_end_time': '2026-01-15T10:01:00+00:00', 'step_status': 'Success', 'inputs': 'Supplied exercise target', 'outputs': 'Backup-read test allowed', 'failure_information': '', 'cloudtrail_request_id': 'request-read_backup', 'cloudtrail_request_identity': 'exercise-recovery-role', 'cloudtrail_operation': 'GetObject'}
      feedback: {'correct': 'This recorded evidence belongs in the response audit.', 'incorrect': 'Use the actual step outcome and request evidence, not the intended workflow plan.'}
  task execution_id0 (cell): For the successful step, select the cell containing the execution identifier.  KEY: row={'execution_id': 'response-exercise', 'step': 'read_backup'} column=execution_id expect=response-exercise dataset-says=response-exercise
      feedback: {'correct': 'This recorded evidence belongs in the response audit.', 'incorrect': 'Use the actual step outcome and request evidence, not the intended workflow plan.'}
  task acting_role0 (cell): For the successful step, select the cell containing the execution authority.  KEY: row={'execution_id': 'response-exercise', 'step': 'read_backup'} column=acting_role expect=exercise-recovery-role dataset-says=exercise-recovery-role
      feedback: {'correct': 'This recorded evidence belongs in the response audit.', 'incorrect': 'Use the actual step outcome and request evidence, not the intended workflow plan.'}
  task target0 (cell): For the successful step, select the cell containing the target identity.  KEY: row={'execution_id': 'response-exercise', 'step': 'read_backup'} column=target expect=exercise-backup dataset-says=exercise-backup
      feedback: {'correct': 'This recorded evidence belongs in the response audit.', 'incorrect': 'Use the actual step outcome and request evidence, not the intended workflow plan.'}
  task start_time0 (cell): For the successful step, select the cell containing the execution start time.  KEY: row={'execution_id': 'response-exercise', 'step': 'read_backup'} column=start_time expect=2026-01-15T10:00:00+00:00 dataset-says=2026-01-15T10:00:00+00:00
      feedback: {'correct': 'This recorded evidence belongs in the response audit.', 'incorrect': 'Use the actual step outcome and request evidence, not the intended workflow plan.'}
  task end_time0 (cell): For the successful step, select the cell containing the execution end time.  KEY: row={'execution_id': 'response-exercise', 'step': 'read_backup'} column=end_time expect=2026-01-15T10:05:00+00:00 dataset-says=2026-01-15T10:05:00+00:00
      feedback: {'correct': 'This recorded evidence belongs in the response audit.', 'incorrect': 'Use the actual step outcome and request evidence, not the intended workflow plan.'}
  task step_start_time0 (cell): For the successful step, select the cell containing the per-step start time.  KEY: row={'execution_id': 'response-exercise', 'step': 'read_backup'} column=step_start_time expect=2026-01-15T10:00:00+00:00 dataset-says=2026-01-15T10:00:00+00:00
      feedback: {'correct': 'This recorded evidence belongs in the response audit.', 'incorrect': 'Use the actual step outcome and request evidence, not the intended workflow plan.'}
  task step_end_time0 (cell): For the successful step, select the cell containing the per-step end time.  KEY: row={'execution_id': 'response-exercise', 'step': 'read_backup'} column=step_end_time expect=2026-01-15T10:01:00+00:00 dataset-says=2026-01-15T10:01:00+00:00
      feedback: {'correct': 'This recorded evidence belongs in the response audit.', 'incorrect': 'Use the actual step outcome and request evidence, not the intended workflow plan.'}
  task cloudtrail_request_id0 (cell): For the successful step, select the cell containing the underlying CloudTrail request identifier.  KEY: row={'execution_id': 'response-exercise', 'step': 'read_backup'} column=cloudtrail_request_id expect=request-read_backup dataset-says=request-read_backup
      feedback: {'correct': 'This recorded evidence belongs in the response audit.', 'incorrect': 'Use the actual step outcome and request evidence, not the intended workflow plan.'}
  task cloudtrail_request_identity0 (cell): For the successful step, select the cell containing the request identity attributing the underlying action.  KEY: row={'execution_id': 'response-exercise', 'step': 'read_backup'} column=cloudtrail_request_identity expect=exercise-recovery-role dataset-says=exercise-recovery-role
      feedback: {'correct': 'This recorded evidence belongs in the response audit.', 'incorrect': 'Use the actual step outcome and request evidence, not the intended workflow plan.'}
  task cloudtrail_operation0 (cell): For the successful step, select the cell containing the underlying operation evidence.  KEY: row={'execution_id': 'response-exercise', 'step': 'read_backup'} column=cloudtrail_operation expect=GetObject dataset-says=GetObject
      feedback: {'correct': 'This recorded evidence belongs in the response audit.', 'incorrect': 'Use the actual step outcome and request evidence, not the intended workflow plan.'}
  task outcome1 (row): Select the entire failed step record, preserving its execution, authority, target, times, inputs, outputs and failure details.  KEY: row={'execution_id': 'response-exercise', 'step': 'create_recovery'} column=None expect=None dataset-says={'execution_id': 'response-exercise', 'acting_role': 'exercise-recovery-role', 'target': 'exercise-recovery-stack', 'start_time': '2026-01-15T10:00:00+00:00', 'end_time': '2026-01-15T10:05:00+00:00', 'step': 'create_recovery', 'step_start_time': '2026-01-15T10:01:00+00:00', 'step_end_time': '2026-01-15T10:02:00+00:00', 'step_status': 'Failed', 'inputs': 'Supplied exercise target', 'outputs': '', 'failure_information': 'Supplied recovery-resource test denied', 'cloudtrail_request_id': 'request-create_recovery', 'cloudtrail_request_identity': 'exercise-recovery-role', 'cloudtrail_operation': 'CreateStack'}
      feedback: {'correct': 'This recorded evidence belongs in the response audit.', 'incorrect': 'Use the actual step outcome and request evidence, not the intended workflow plan.'}
  task execution_id1 (cell): For the failed step, select the cell containing the execution identifier.  KEY: row={'execution_id': 'response-exercise', 'step': 'create_recovery'} column=execution_id expect=response-exercise dataset-says=response-exercise
      feedback: {'correct': 'This recorded evidence belongs in the response audit.', 'incorrect': 'Use the actual step outcome and request evidence, not the intended workflow plan.'}
  task acting_role1 (cell): For the failed step, select the cell containing the execution authority.  KEY: row={'execution_id': 'response-exercise', 'step': 'create_recovery'} column=acting_role expect=exercise-recovery-role dataset-says=exercise-recovery-role
      feedback: {'correct': 'This recorded evidence belongs in the response audit.', 'incorrect': 'Use the actual step outcome and request evidence, not the intended workflow plan.'}
  task target1 (cell): For the failed step, select the cell containing the target identity.  KEY: row={'execution_id': 'response-exercise', 'step': 'create_recovery'} column=target expect=exercise-recovery-stack dataset-says=exercise-recovery-stack
      feedback: {'correct': 'This recorded evidence belongs in the response audit.', 'incorrect': 'Use the actual step outcome and request evidence, not the intended workflow plan.'}
  task start_time1 (cell): For the failed step, select the cell containing the execution start time.  KEY: row={'execution_id': 'response-exercise', 'step': 'create_recovery'} column=start_time expect=2026-01-15T10:00:00+00:00 dataset-says=2026-01-15T10:00:00+00:00
      feedback: {'correct': 'This recorded evidence belongs in the response audit.', 'incorrect': 'Use the actual step outcome and request evidence, not the intended workflow plan.'}
  task end_time1 (cell): For the failed step, select the cell containing the execution end time.  KEY: row={'execution_id': 'response-exercise', 'step': 'create_recovery'} column=end_time expect=2026-01-15T10:05:00+00:00 dataset-says=2026-01-15T10:05:00+00:00
      feedback: {'correct': 'This recorded evidence belongs in the response audit.', 'incorrect': 'Use the actual step outcome and request evidence, not the intended workflow plan.'}
  task step_start_time1 (cell): For the failed step, select the cell containing the per-step start time.  KEY: row={'execution_id': 'response-exercise', 'step': 'create_recovery'} column=step_start_time expect=2026-01-15T10:01:00+00:00 dataset-says=2026-01-15T10:01:00+00:00
      feedback: {'correct': 'This recorded evidence belongs in the response audit.', 'incorrect': 'Use the actual step outcome and request evidence, not the intended workflow plan.'}
  task step_end_time1 (cell): For the failed step, select the cell containing the per-step end time.  KEY: row={'execution_id': 'response-exercise', 'step': 'create_recovery'} column=step_end_time expect=2026-01-15T10:02:00+00:00 dataset-says=2026-01-15T10:02:00+00:00
      feedback: {'correct': 'This recorded evidence belongs in the response audit.', 'incorrect': 'Use the actual step outcome and request evidence, not the intended workflow plan.'}
  task cloudtrail_request_id1 (cell): For the failed step, select the cell containing the underlying CloudTrail request identifier.  KEY: row={'execution_id': 'response-exercise', 'step': 'create_recovery'} column=cloudtrail_request_id expect=request-create_recovery dataset-says=request-create_recovery
      feedback: {'correct': 'This recorded evidence belongs in the response audit.', 'incorrect': 'Use the actual step outcome and request evidence, not the intended workflow plan.'}
  task cloudtrail_request_identity1 (cell): For the failed step, select the cell containing the request identity attributing the underlying action.  KEY: row={'execution_id': 'response-exercise', 'step': 'create_recovery'} column=cloudtrail_request_identity expect=exercise-recovery-role dataset-says=exercise-recovery-role
      feedback: {'correct': 'This recorded evidence belongs in the response audit.', 'incorrect': 'Use the actual step outcome and request evidence, not the intended workflow plan.'}
  task cloudtrail_operation1 (cell): For the failed step, select the cell containing the underlying operation evidence.  KEY: row={'execution_id': 'response-exercise', 'step': 'create_recovery'} column=cloudtrail_operation expect=CreateStack dataset-says=CreateStack
      feedback: {'correct': 'This recorded evidence belongs in the response audit.', 'incorrect': 'Use the actual step outcome and request evidence, not the intended workflow plan.'}
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The completed response record accurately captures the supplied execution identifiers, authority, targets, times and step details, links underlying actions to CloudTrail evidence, and retains both successful and failed outcomes without inferring actions from the intended plan.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r04
  MEASURES: B:identify_response_execution_and_per_step_outcomes(f1,f2); B:attribute_aws_operations_to_acting_authority_and_targets(f2,f3); B:recognize_success_and_failure_evidence(f1,f3)   anchors=['practice', 'assessment:identify_response_execution_and_per_step_outcomes', 'assessment:attribute_aws_operations_to_acting_authority_and_targets', 'assessment:recognize_success_and_failure_evidence']
  taught-before-tested: B.f1←s04; B.f2←s04; B.f2←s04; B.f3←s04; B.f1←s04; B.f3←s04

### s07 · recap · Keep these distinctions
(takeaway) Approval precedes the protected operation. Rejection or stop prevents it; inspect execution state after stopping. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Keep execution identity, role, targets, timing and complete step evidence. Attribute AWS actions with CloudTrail; retain failures too. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Verify audit evidence integrity: Next: Verify audit evidence integrity.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the evidence
(mechanism) An aws:approve Automation step pauses for the designated approvers to approve or reject. Place it before the protected operation; a pending request is not approval. ⟦A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Use the supplied branching or failure path to prevent the protected operation on rejection or stop. When a stop condition occurs, use the approved stop operation and inspect execution state before allowing further actions. ⟦A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Pending, rejected and stopped are not approval to perform the protected operation. A stop request also needs execution-state inspection before further action. ⟦A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.approval_states cols=['execution_id', 'approval_step', 'execution_state', 'protected_operation_executed'] ] caption: 
### r02 · Separate the evidence
(mechanism) An aws:approve Automation step pauses for the designated approvers to approve or reject. Place it before the protected operation; a pending request is not approval. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Use the supplied branching or failure path to prevent the protected operation on rejection or stop. When a stop condition occurs, use the approved stop operation and inspect execution state before allowing further actions. ⟦A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Pending, rejected and stopped are not approval to perform the protected operation. A stop request also needs execution-state inspection before further action. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.approval_states cols=['execution_id', 'approval_step', 'execution_state', 'protected_operation_executed'] ] caption: 
### r03 · Separate the evidence
(mechanism) Automation details include execution ID, step statuses, inputs, outputs and failure information. Record the supplied response’s execution ID, acting role, targets, start/end times and per-step outcomes. ⟦B.f1 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Attribute underlying AWS actions using CloudTrail request identity and operation evidence. Retain both success and failure outcomes, not just a success-focused summary. ⟦B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(misconception) A failed response step still belongs in the record. Keep its inputs, outputs and failure information with execution identity, targets and attributed CloudTrail operations. ⟦B.f1 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.response_audit cols=['execution_id', 'acting_role', 'target', 'start_time', 'end_time', 'step', 'step_start_time', 'step_end_time', 'step_status', 'inputs', 'outputs', 'failure_information', 'cloudtrail_request_id', 'cloudtrail_request_identity', 'cloudtrail_operation'] ] caption: 
### r04 · Separate the evidence
(mechanism) Automation details include execution ID, step statuses, inputs, outputs and failure information. Record the supplied response’s execution ID, acting role, targets, start/end times and per-step outcomes. ⟦B.f1 B.f2 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Attribute underlying AWS actions using CloudTrail request identity and operation evidence. Retain both success and failure outcomes, not just a success-focused summary. ⟦B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(misconception) A failed response step still belongs in the record. Keep its inputs, outputs and failure information with execution identity, targets and attributed CloudTrail operations. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.response_audit cols=['execution_id', 'acting_role', 'target', 'start_time', 'end_time', 'step', 'step_start_time', 'step_end_time', 'step_status', 'inputs', 'outputs', 'failure_information', 'cloudtrail_request_id', 'cloudtrail_request_identity', 'cloudtrail_operation'] ] caption: 

=========

# EVALUATOR PACKET — Verify audit evidence integrity / Configure audit-storage retention (aws_devops.tile.108)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = security.audit_evidence_integrity — Audit evidence integrity
B = security.audit_storage_retention — Audit storage retention

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (security.audit_evidence_integrity)   objective: Verify audit evidence integrity
A.f1: CloudTrail log-file integrity validation uses signed digest files and hashes to detect modification or deletion of delivered log files.   [sources: aws_cloudtrail_user_guide#cloudtrail-log-file-validation-intro.html]
A.f2: Run aws cloudtrail validate-logs --trail-arn ARN --start-time TIME --end-time TIME --region REGION against the supplied log/digest interval and inspect validation failures; for an organization trail also provide the required --account-id.   [sources: aws_cloudtrail_user_guide#cloudtrail-log-file-validation-cli.html]
A.f3: Digest validation supplies tamper evidence but does not itself prevent unauthorized access or deletion.   [sources: aws_cloudtrail_user_guide#cloudtrail-log-file-validation-intro.html]
note: Include organization-trail account-id where required; do not invent validation output or claim preventive protection.
PRACTICE ANCHOR (tool_simulation): Validate one supplied CloudTrail log/digest set using aws cloudtrail validate-logs with the supplied trail ARN, start time, end time and Region, including --account-id when required for an organization trail. Inspect the result and identify the seeded integrity failure.  SUCCESS: The validation targets the supplied trail, interval, Region and account when required. The learner identifies the seeded failure from the supplied validation results, preserves its evidence with the validation scope, and does not treat validation as prevention of unauthorized access or deletion.
ASSESSMENT ANCHOR: detect_tampering_or_missing_evidence_in_cloudtrail_validation_results facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_tamper_evidence_from_preventive_protection facts=['f3']

## SOURCE FACTS — B (security.audit_storage_retention)   objective: Configure audit-storage retention
B.f1: S3 Object Lock applies retention to object versions using governance or compliance mode and a retain-until date.   [sources: aws_s3_user_guide#object-lock.html]
B.f2: Apply the supplied default retention duration and mode on the prepared Object Lock bucket and inspect individual audit-object version retention.   [sources: aws_s3_user_guide#object-lock-managing.html]
B.f3: Compliance mode prevents deletion or shortening of retention during the retention period even by root; governance mode permits bypass only with the necessary bypass authorization and request.   [sources: aws_s3_user_guide#object-lock.html#object-lock-retention-modes]
note: Use prepared bucket and supplied retention policy; do not create irreversible unapproved compliance settings.
PRACTICE ANCHOR (tool_simulation): Apply the supplied default retention duration and mode to one prepared Object Lock audit bucket, then inspect individual audit-object versions for their retention mode and retain-until date.  SUCCESS: The prepared bucket's default retention matches the supplied policy. Recorded version-specific modes and retain-until dates show whether the inspected audit-object versions remain protected for the supplied interval, with governance bypass distinguished from compliance protection. No unapproved retention settings are applied.
ASSESSMENT ANCHOR: verify_audit_object_version_retention_against_supplied_interval facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_governance_bypass_from_compliance_retention_protection facts=['f3']

## DATA ASSETS USED
ds.audit_retention: Audit storage retention — read-only evidence — columns: bucket(identifier), object_key(identifier), version_id(identifier), retention_mode(categorical), required_start_date(datetime), required_end_date(datetime), retain_until_date(datetime), bypass_authorization(categorical), bypass_requested(categorical)
   ["exercise-audit-bucket","response-audit","version-governance","governance","2026-01-15","2026-02-14","2026-02-14",true,true]
   ["exercise-audit-bucket","response-audit","version-compliance","compliance","2026-01-15","2026-02-14","2026-02-14",false,false]
ds.integrity_scope: Audit evidence integrity — read-only evidence — columns: trail(identifier), account(identifier), region(categorical), start_time(datetime), end_time(datetime), log_set(identifier), validation_result(categorical), failure_information(text)
   ["exercise-organization-trail","exercise-isolated-account","REGION","2026-01-15T10:00:00+00:00","2026-01-15T11:00:00+00:00","logs-intact","pass",""]
   ["exercise-organization-trail","exercise-isolated-account","REGION","2026-01-15T11:00:00+00:00","2026-01-15T12:00:00+00:00","logs-seeded-failure","fail","Delivered log modification detected in the supplied digest interval"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Audit storage retention; Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template; directly require the native EC2 instance foundation; Backend configuration; Block release on actionable dependency or image security findings; Control environment promotion with a manual approval; Diagnose EC2 or container health failures using telemetry and prepared Linux inspection skills; Diagnose a failed delivery pipeline action; Document incident evidence and a preventive change using reused systematic-debugging coverage; Endpoint cutover; Gate release completion on a deployed-service smoke check; Handle failed event delivery with bounded retries and failure capture; Perform a controlled ECS service rollout; Promote the same artifact version across environments; Recover an incident safely using an established runbook; Replacement controls; Residual charge verification; State access isolation; State locking; Verify restored service and data against RTO/RPO in an isolated rehearsal

## LESSON, in learner order

### s01 · explainer · Verify audit evidence integrity
Read the evidence — 
(mechanism) CloudTrail integrity validation uses signed digest files and hashes to detect modification or deletion of delivered logs. ⟦A.f1 A:tb1 A:tb2 A:tb3⟧
(mechanism) Use aws cloudtrail validate-logs with --trail-arn ARN, --start-time TIME, --end-time TIME and --region REGION for the supplied interval. For an organization trail, also supply the required --account-id. Inspect validation failures. ⟦A.f2 A:tb1 A:tb2 A:tb3⟧
(mechanism) Digest validation provides tamper evidence; it does not prevent unauthorized access or deletion. ⟦A.f3 A:tb1 A:tb2 A:tb3⟧
[DIAGRAM] nodes=['Validation command: trail, account, interval and Region', 'Signed digest and delivered log validation', 'Pass or seeded integrity failure'] edges=[] alt: Make the validation command's trail, interval, Region and required account scope visible alongside the supplied validation results, with the seeded integrity failure identifiable.
[TABLE ds.integrity_scope cols=['trail', 'account', 'region', 'start_time', 'end_time', 'log_set', 'validation_result', 'failure_information'] ] caption: 

### s02 · explainer · Compare the evidence
Read the evidence — 
(example) A pass for one interval does not establish integrity for another. Preserve the seeded failure, with trail, account scope, interval and Region. Validation detects tampering; it is not access prevention. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · check · Review log integrity validation
Check your understanding — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] What does CloudTrail digest validation establish about unauthorized access or deletion?
  ✔ a: It provides tamper evidence; it does not itself prevent unauthorized access or deletion.
      why: Correct. It provides tamper evidence; it does not itself prevent unauthorized access or deletion.
  ✘ b: It prevents all unauthorized deletion once validation passes.
      why: Tamper detection is not preventive protection.
  ✘ c: It replaces access restrictions because signed digests control who can read logs.
      why: Signed digest validation does not itself impose access restrictions.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The validation targets the supplied trail, interval, Region and account when required. The learner identifies the seeded failure from the supplied validation results, preserves its evidence with the validation scope, and does not treat validation as prevention of unauthorized access or deletion.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r01
  MEASURES: A:distinguish_tamper_evidence_from_preventive_protection(f3)   anchors=['assessment:distinguish_tamper_evidence_from_preventive_protection']
  taught-before-tested: A.f3←s01

### s04 · hands_on · Review log integrity validation
Evidence review — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, core, grading=client] Read the scoped validation results. Decide whether each interval has passing validation or a detected integrity failure. Also judge the unsupported prevention claim. Preserve the failure information together with its scope.
  'The supplied organization-trail invocation uses aws cloudtrail validate-logs with --trail-arn, --start-time, --end-time, --region and required --account-id matching the fields below.
```text
trail: "exercise-organization-trail"
account: "exercise-isolated-account"
region: "REGION"
start_time: "2026-01-15T10:00:00+00:00"
end_time: "2026-01-15T11:00:00+00:00"
log_set: "logs-intact"
validation_result: "pass"
failure_information: ""
```' -> Passing validation for supplied scope  (column validation_result, role=categorical)
      feedback: Judgement: Passing validation for supplied scope. Compare the stated evidence with the required criterion.
  'The supplied organization-trail invocation uses aws cloudtrail validate-logs with --trail-arn, --start-time, --end-time, --region and required --account-id matching the fields below.
```text
trail: "exercise-organization-trail"
account: "exercise-isolated-account"
region: "REGION"
start_time: "2026-01-15T11:00:00+00:00"
end_time: "2026-01-15T12:00:00+00:00"
log_set: "logs-seeded-failure"
validation_result: "fail"
failure_information: "Delivered log modification detected in the supplied digest interval"
```' -> Integrity failure: preserve scoped evidence  (column validation_result, role=categorical)
      feedback: Judgement: Integrity failure: preserve scoped evidence. Compare the stated evidence with the required criterion.
  'Alternate conclusion: signed digest validation prevents unauthorized log access and deletion.' -> Unsupported prevention claim
      feedback: Judgement: Unsupported prevention claim. Compare the stated evidence with the required criterion.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The validation targets the supplied trail, interval, Region and account when required. The learner identifies the seeded failure from the supplied validation results, preserves its evidence with the validation scope, and does not treat validation as prevention of unauthorized access or deletion.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r02
  MEASURES: A:detect_tampering_or_missing_evidence_in_cloudtrail_validation_results(f1,f2)   anchors=['practice', 'assessment:detect_tampering_or_missing_evidence_in_cloudtrail_validation_results']
  taught-before-tested: A.f1←s01; A.f2←s01

### s05 · explainer · Configure audit-storage retention
Read the evidence — 
(mechanism) S3 Object Lock retains object versions using governance or compliance mode and a retain-until date. Apply the supplied default duration and mode on the prepared bucket, then inspect individual audit-object versions. ⟦B.f1 B.f2 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(mechanism) During retention, compliance prevents deletion or shortening even by root. Governance permits bypass only with the necessary bypass authorization and request. Record each version’s mode and date rather than treating the modes as interchangeable. ⟦B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.audit_retention cols=['bucket', 'object_key', 'version_id', 'retention_mode', 'required_start_date', 'required_end_date', 'retain_until_date', 'bypass_authorization', 'bypass_requested'] ] caption: 

### s06 · check · Review audit-object retention
Check your understanding — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [choice, core, grading=client] During an active retention period, how do governance and compliance retention differ?
  ✔ a: Governance bypass requires the necessary authorization and bypass request; compliance prevents deletion or shortening even by root.
      why: Correct. Governance bypass requires the necessary authorization and bypass request; compliance prevents deletion or shortening even by root.
  ✘ b: A governance bypass request alone suffices without bypass authorization.
      why: Governance bypass requires both the authorization and the request.
  ✘ c: Root can shorten compliance retention during the retention period.
      why: Compliance retention blocks deletion or shortening during the period even by root.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The prepared bucket's default retention matches the supplied policy. Recorded version-specific modes and retain-until dates show whether the inspected audit-object versions remain protected for the supplied interval, with governance bypass distinguished from compliance protection. No unapproved retention settings are applied.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r03
  MEASURES: B:distinguish_governance_bypass_from_compliance_retention_protection(f3)   anchors=['assessment:distinguish_governance_bypass_from_compliance_retention_protection']
  taught-before-tested: B.f3←s05

### s07 · hands_on · Review audit-object retention
Evidence review — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read the version-retention excerpts. Decide whether protection permits an authorized/requested governance bypass or is compliance protection that cannot be shortened during the active interval; judge the alternate policy violation too.
  'The prepared bucket default matches the supplied approved mode and duration; no unapproved changes were made. Version-specific retain-until dates were inspected against required_start_date and required_end_date; each shown date covers that interval.
```text
bucket: "exercise-audit-bucket"
object_key: "response-audit"
version_id: "version-governance"
retention_mode: "governance"
required_start_date: "2026-01-15"
required_end_date: "2026-02-14"
retain_until_date: "2026-02-14"
bypass_authorization: true
bypass_requested: true
```' -> Governance protection with authorized/requested bypass  (column retention_mode, role=categorical)
      feedback: Judgement: Governance protection with authorized/requested bypass. Compare the stated evidence with the required criterion.
  'The prepared bucket default matches the supplied approved mode and duration; no unapproved changes were made. Version-specific retain-until dates were inspected against required_start_date and required_end_date; each shown date covers that interval.
```text
bucket: "exercise-audit-bucket"
object_key: "response-audit"
version_id: "version-compliance"
retention_mode: "compliance"
required_start_date: "2026-01-15"
required_end_date: "2026-02-14"
retain_until_date: "2026-02-14"
bypass_authorization: false
bypass_requested: false
```' -> Compliance protection: no deletion or shortening during interval  (column retention_mode, role=categorical)
      feedback: Judgement: Compliance protection: no deletion or shortening during interval. Compare the stated evidence with the required criterion.
  'Alternate policy excerpt: supplied mode is compliance, but the proposed default is governance; reviewer approval for this change is absent.' -> Does not match approved retention policy
      feedback: Judgement: Does not match approved retention policy. Compare the stated evidence with the required criterion.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The prepared bucket's default retention matches the supplied policy. Recorded version-specific modes and retain-until dates show whether the inspected audit-object versions remain protected for the supplied interval, with governance bypass distinguished from compliance protection. No unapproved retention settings are applied.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r04
  MEASURES: B:verify_audit_object_version_retention_against_supplied_interval(f1,f2); B:distinguish_governance_bypass_from_compliance_retention_protection(f3)   anchors=['practice', 'assessment:verify_audit_object_version_retention_against_supplied_interval', 'assessment:distinguish_governance_bypass_from_compliance_retention_protection']
  taught-before-tested: B.f1←s05; B.f2←s05; B.f3←s05

### s08 · recap · Keep these distinctions
(takeaway) Validate the supplied trail and interval with the required scope. Signed digests detect tampering; they do not prevent it. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Inspect each object version’s mode and retain-until date. Governance bypass needs authorization and request; compliance bars deletion or shortening during retention even by root. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Configure and initialize an S3 Terraform backend: Next: Configure and initialize an S3 Terraform backend.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the evidence
(mechanism) Digest validation provides tamper evidence; it does not prevent unauthorized access or deletion. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) A pass for one interval does not establish integrity for another. Preserve the seeded failure, with trail, account scope, interval and Region. Validation detects tampering; it is not access prevention. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.integrity_scope cols=['trail', 'account', 'region', 'start_time', 'end_time', 'log_set', 'validation_result', 'failure_information'] ] caption: 
### r02 · Separate the evidence
(mechanism) CloudTrail integrity validation uses signed digest files and hashes to detect modification or deletion of delivered logs. ⟦A.f1 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Use aws cloudtrail validate-logs with --trail-arn ARN, --start-time TIME, --end-time TIME and --region REGION for the supplied interval. For an organization trail, also supply the required --account-id. Inspect validation failures. ⟦A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) A pass for one interval does not establish integrity for another. Preserve the seeded failure, with trail, account scope, interval and Region. Validation detects tampering; it is not access prevention. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.integrity_scope cols=['trail', 'account', 'region', 'start_time', 'end_time', 'log_set', 'validation_result', 'failure_information'] ] caption: 
### r03 · Separate the evidence
(mechanism) During retention, compliance prevents deletion or shortening even by root. Governance permits bypass only with the necessary bypass authorization and request. Record each version’s mode and date rather than treating the modes as interchangeable. ⟦B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(misconception) The governance version’s authorized requested bypass does not apply to compliance. Inspect version-specific mode and retain-until date against the required interval. ⟦B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.audit_retention cols=['bucket', 'object_key', 'version_id', 'retention_mode', 'required_start_date', 'required_end_date', 'retain_until_date', 'bypass_authorization', 'bypass_requested'] ] caption: 
### r04 · Separate the evidence
(mechanism) S3 Object Lock retains object versions using governance or compliance mode and a retain-until date. Apply the supplied default duration and mode on the prepared bucket, then inspect individual audit-object versions. ⟦B.f1 B.f2 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(mechanism) During retention, compliance prevents deletion or shortening even by root. Governance permits bypass only with the necessary bypass authorization and request. Record each version’s mode and date rather than treating the modes as interchangeable. ⟦B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(misconception) The governance version’s authorized requested bypass does not apply to compliance. Inspect version-specific mode and retain-until date against the required interval. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.audit_retention cols=['bucket', 'object_key', 'version_id', 'retention_mode', 'required_start_date', 'required_end_date', 'retain_until_date', 'bypass_authorization', 'bypass_requested'] ] caption: 

=========

# EVALUATOR PACKET — Configure and initialize an S3 Terraform backend / Control Terraform EC2 replacement (aws_devops.tile.110)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = terraform.backend_configuration — Backend configuration
B = terraform.replacement_controls — Replacement controls

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (terraform.backend_configuration)   objective: Configure and initialize an S3 Terraform backend
A.f1: The S3 backend stores Terraform state in a specified bucket and key, separate from the configuration that declares managed resources.   [sources: terraform_language#backend/s3]
A.f2: Provision the protected backend bucket with the supplied local-state bootstrap configuration before selecting it as the backend.   [sources: terraform_language#backend/s3]
A.f3: Configure the already-provisioned backend using line-separated HCL arguments:
terraform {
  backend "s3" {
    bucket = "BUCKET"
    key = "KEY"
    region = "REGION"
  }
}
Use the supplied bucket, key, Region and protection settings.   [sources: terraform_language#backend/s3]
A.f4: Run terraform init -migrate-state after changing the backend, approve the supplied migration and verify state is at the intended bucket/key.   [sources: terraform_language#../cli/commands/init]
note: Show line-separated HCL, not comma-separated shorthand; use supplied bootstrap and migrate-state approval.
PRACTICE ANCHOR (live_code): Use the supplied local-state bootstrap configuration to provision one protected S3 backend bucket. Configure the already-provisioned backend with the supplied bucket, key and Region, retain the supplied protection settings, then initialize and migrate the exercise state.  SUCCESS: The protected bucket exists before backend selection, the backend arguments match the supplied destination, and the approved migration places exercise state at the intended bucket/key.
ASSESSMENT ANCHOR: verify_configured_backend_bucket_and_key facts=['f1', 'f3']
ASSESSMENT ANCHOR: verify_bootstrap_and_migrated_state_location facts=['f2', 'f4']

## SOURCE FACTS — B (terraform.replacement_controls)   objective: Control Terraform EC2 replacement
B.f1: By default Terraform destroys an object before creating its replacement; create_before_destroy requests the reverse order where supported.   [sources: terraform_language#meta-arguments/lifecycle]
B.f2: prevent_destroy rejects a plan that would destroy the protected resource while that lifecycle rule remains in its configuration.   [sources: terraform_language#meta-arguments/lifecycle]
B.f3: Set the supplied lifecycle argument in the resource block, introduce the controlled replacement-triggering change, and inspect the plan’s replacement order or prevention error before the approved permitted apply.   [sources: terraform_language#meta-arguments/lifecycle]
B.f4: Lifecycle settings constrain replacement mechanics but do not replace scope and impact approval.   [sources: terraform_language#meta-arguments/lifecycle]
note: Preserve where-supported and rule-remains qualifiers; do not imply protection after configuration removal.
PRACTICE ANCHOR (live_code): Provision one sandbox EC2 instance from supplied Terraform configuration and authorization. Set the supplied replacement lifecycle argument in its resource block, introduce the supplied replacement-triggering change, and inspect the plan order or prevention error. Execute only an approved permitted replacement to provision the replacement EC2 instance; network setup and any authorized configuration adjustment are supplied.  SUCCESS: The sandbox instance is provisioned, the configured lifecycle argument produces the expected replacement order or prevention error, and an approved permitted replacement provisions the replacement EC2 instance. Recorded plan evidence is separate from scope and impact approval; a rejected plan is not applied.
ASSESSMENT ANCHOR: predict_replacement_order_from_lifecycle_and_diff facts=['f1']
ASSESSMENT ANCHOR: predict_destruction_prevention_from_lifecycle_and_diff facts=['f2']
ASSESSMENT ANCHOR: distinguish_plan_evidence_from_replacement_authorization facts=['f3', 'f4']

## DATA ASSETS USED
ds.backend_sequence: Backend configuration — read-only evidence — columns: sequence(numerical), step(categorical), evidence(text), bucket(identifier), key(identifier), region(categorical)
   [1,"local-state bootstrap","Protected bucket provisioned with supplied settings","BUCKET","KEY","REGION"]
   [2,"backend selection","Backend selects the already-existing bucket and key","BUCKET","KEY","REGION"]
   [3,"approved migration","Supplied migration approved before terraform init -migrate-state","BUCKET","KEY","REGION"]
   [4,"destination inspection","Exercise state found at the intended bucket/key","BUCKET","KEY","REGION"]
ds.replacement_controls: Replacement controls — read-only evidence — columns: plan(identifier), lifecycle_setting(categorical), triggering_diff(text), plan_outcome(categorical), scope_impact_approval(text)
   ["replacement-default","default","Supplied replacement-triggering EC2 argument edit","destroy before create","Supplied approval required before permitted apply"]
   ["replacement-reversed","create_before_destroy","Supplied replacement-triggering EC2 argument edit","create before destroy where supported","Supplied approval required before permitted apply"]
   ["replacement-prevented","prevent_destroy","Supplied replacement-triggering EC2 argument edit","destruction plan rejected while rule remains configured","Rejected plan is not applied"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template; directly require the native EC2 instance foundation; Block release on actionable dependency or image security findings; Control environment promotion with a manual approval; Diagnose EC2 or container health failures using telemetry and prepared Linux inspection skills; Diagnose a failed delivery pipeline action; Document incident evidence and a preventive change using reused systematic-debugging coverage; Endpoint cutover; Gate release completion on a deployed-service smoke check; Handle failed event delivery with bounded retries and failure capture; Perform a controlled ECS service rollout; Promote the same artifact version across environments; Recover an incident safely using an established runbook; Replacement controls; Residual charge verification; State access isolation; State locking; Verify restored service and data against RTO/RPO in an isolated rehearsal

## LESSON, in learner order

### s01 · explainer · Configure and initialize an S3 Terraform backend
Read the evidence — 
(mechanism) The S3 backend stores state at a specified bucket and key, separate from managed-resource declarations. First provision the protected bucket using the supplied local-state bootstrap configuration. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3⟧
(mechanism) Select that existing bucket with the line-separated backend block below, using the supplied bucket, key, Region and protection settings. ⟦A.f3 A:tb1 A:tb2 A:tb3⟧
(mechanism) After changing the backend, run terraform init -migrate-state, approve the supplied migration and verify state at the intended bucket/key. ⟦A.f4 A:tb1 A:tb2 A:tb3⟧
(syntax) terraform {
  backend "s3" {
    bucket = "BUCKET"
    key = "KEY"
    region = "REGION"
  }
} ⟦A.f3 A:tb1 A:tb2 A:tb3⟧
[PROCESS_FLOW] nodes=['Local-state bootstrap: provision protected bucket', 'Backend block: select existing bucket and key', 'terraform init -migrate-state; approve supplied migration', 'Verify state at intended bucket/key'] edges=[('n0', 'n1', 'next'), ('n1', 'n2', 'next'), ('n2', 'n3', 'next')] alt: Make the sequence visible: supplied local-state bootstrap provisions the protected bucket; the backend block selects that existing bucket and key; approved initialization migrates state; destination inspection verifies the intended object location.
[TABLE ds.backend_sequence cols=['sequence', 'step', 'evidence', 'bucket', 'key', 'region'] ] caption: 

### s02 · explainer · Compare the evidence
Read the evidence — 
(example) The backend block selects storage; it does not create its own bucket. Keep the local-state bootstrap result and migrated-state destination in the record, then verify the intended bucket/key. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Review backend setup and migration
Check your understanding — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] Which sequence verifies a bootstrap and migration to an S3 Terraform backend?
  ✔ a: Provision the protected bucket with local-state bootstrap first; change backend, perform the approved migration, and inspect state at the intended bucket/key.
      why: Correct. Provision the protected bucket with local-state bootstrap first; change backend, perform the approved migration, and inspect state at the intended bucket/key.
  ✘ b: Select the backend before its bucket exists and treat the configuration as migration proof.
      why: The bucket must exist before selection; declaring a destination does not verify migration.
  ✘ c: Provision the bucket and assume state moved there without migration or destination inspection.
      why: Bucket existence is not evidence that state reached the intended bucket/key.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The protected bucket exists before backend selection, the backend arguments match the supplied destination, and the approved migration places exercise state at the intended bucket/key.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r01
  MEASURES: A:verify_bootstrap_and_migrated_state_location(f2,f4)   anchors=['assessment:verify_bootstrap_and_migrated_state_location']
  taught-before-tested: A.f2←s01; A.f4←s01

### s04 · hands_on · Review backend setup and migration
Evidence review — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, core, grading=client] Read the backend configuration and sequence excerpts. Decide whether each supports the supplied destination and migration, or whether the alternate setup violates bootstrap/destination requirements.
  'Supplied backend excerpt:
```hcl
terraform {
  backend "s3" {
    bucket = "BUCKET"
    key = "KEY"
    region = "REGION"
  }
}
```
The protected local-state bootstrap bucket already exists. Destination is the supplied bucket/key/Region, not a managed-resource declaration. The approved migration was performed with terraform init -migrate-state and destination inspection follows.
```text
sequence: 1
step: "local-state bootstrap"
evidence: "Protected bucket provisioned with supplied settings"
bucket: "BUCKET"
key: "KEY"
region: "REGION"
```' -> Matches supplied backend destination and sequence  (column step, role=categorical)
      feedback: Judgement: Matches supplied backend destination and sequence. Compare the stated evidence with the required criterion.
  'Supplied backend excerpt:
```hcl
terraform {
  backend "s3" {
    bucket = "BUCKET"
    key = "KEY"
    region = "REGION"
  }
}
```
The protected local-state bootstrap bucket already exists. Destination is the supplied bucket/key/Region, not a managed-resource declaration. The approved migration was performed with terraform init -migrate-state and destination inspection follows.
```text
sequence: 2
step: "backend selection"
evidence: "Backend selects the already-existing bucket and key"
bucket: "BUCKET"
key: "KEY"
region: "REGION"
```' -> Matches supplied backend destination and sequence  (column step, role=categorical)
      feedback: Judgement: Matches supplied backend destination and sequence. Compare the stated evidence with the required criterion.
  'Supplied backend excerpt:
```hcl
terraform {
  backend "s3" {
    bucket = "BUCKET"
    key = "KEY"
    region = "REGION"
  }
}
```
The protected local-state bootstrap bucket already exists. Destination is the supplied bucket/key/Region, not a managed-resource declaration. The approved migration was performed with terraform init -migrate-state and destination inspection follows.
```text
sequence: 3
step: "approved migration"
evidence: "Supplied migration approved before terraform init -migrate-state"
bucket: "BUCKET"
key: "KEY"
region: "REGION"
```' -> Matches supplied backend destination and sequence  (column step, role=categorical)
      feedback: Judgement: Matches supplied backend destination and sequence. Compare the stated evidence with the required criterion.
  'Supplied backend excerpt:
```hcl
terraform {
  backend "s3" {
    bucket = "BUCKET"
    key = "KEY"
    region = "REGION"
  }
}
```
The protected local-state bootstrap bucket already exists. Destination is the supplied bucket/key/Region, not a managed-resource declaration. The approved migration was performed with terraform init -migrate-state and destination inspection follows.
```text
sequence: 4
step: "destination inspection"
evidence: "Exercise state found at the intended bucket/key"
bucket: "BUCKET"
key: "KEY"
region: "REGION"
```' -> Matches supplied backend destination and sequence  (column step, role=categorical)
      feedback: Judgement: Matches supplied backend destination and sequence. Compare the stated evidence with the required criterion.
  'Alternate sequence: select the S3 backend before provisioning the protected bucket.' -> Violates bootstrap or destination requirements
      feedback: Judgement: Violates bootstrap or destination requirements. Compare the stated evidence with the required criterion.
  'Alternate configuration: supplied bucket exists, but backend key selects a different destination from the supplied KEY.' -> Violates bootstrap or destination requirements
      feedback: Judgement: Violates bootstrap or destination requirements. Compare the stated evidence with the required criterion.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The protected bucket exists before backend selection, the backend arguments match the supplied destination, and the approved migration places exercise state at the intended bucket/key.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r02
  MEASURES: A:verify_configured_backend_bucket_and_key(f1,f3)   anchors=['practice', 'assessment:verify_configured_backend_bucket_and_key']
  taught-before-tested: A.f1←s01; A.f3←s01

### s05 · explainer · Control Terraform EC2 replacement
Read the evidence — 
(mechanism) Terraform normally destroys an object before creating its replacement. create_before_destroy requests the reverse order where supported. ⟦B.f1 B:tb1 B:tb2 B:tb3⟧
(mechanism) prevent_destroy rejects a destruction plan while that lifecycle rule remains in the resource’s configuration. ⟦B.f2 B:tb1 B:tb2 B:tb3⟧
(mechanism) Set the supplied lifecycle argument in the resource block, introduce the controlled replacement-triggering change and inspect the plan’s order or prevention error before an approved permitted apply. Lifecycle controls do not replace scope and impact approval. ⟦B.f3 B.f4 B:tb1 B:tb2 B:tb3⟧
[SIDE_BY_SIDE] Ordering requests and destruction prevention are distinct; neither replaces scope and impact approval. left_label: Replacement ordering | right_label: Prevention and separate approval
  left:
[DIAGRAM] nodes=['Default: destroy before create', 'create_before_destroy: reverse order where supported'] edges=[] alt: Make the supplied replacement-triggering diff and lifecycle configuration visible alongside their outcomes: default destroy-before-create order, requested create-before-destroy order where supported, and a prevention error with prevent_destroy still configured. Show scope and impact approval as a separate requirement.
  right:
[DIAGRAM] nodes=['prevent_destroy configured: destruction plan rejected', 'Scope and impact approval still required for permitted apply'] edges=[] alt: Make the supplied replacement-triggering diff and lifecycle configuration visible alongside their outcomes: default destroy-before-create order, requested create-before-destroy order where supported, and a prevention error with prevent_destroy still configured. Show scope and impact approval as a separate requirement.
[TABLE ds.replacement_controls cols=['plan', 'lifecycle_setting', 'triggering_diff', 'plan_outcome', 'scope_impact_approval'] ] caption: 

### s06 · explainer · Compare the evidence
Read the evidence — 
(example) Compare ordering with prevention: create_before_destroy requests reversed order where supported, while a still-configured prevent_destroy rejects destruction. Neither outcome establishes acceptable scope or impact. Inspect plan evidence before an approved permitted apply; do not apply a rejected plan. ⟦B.f1 B.f2 B.f3 B.f4 B:tb4 B:tb5⟧

### s07 · video · A closer look
[VIDEO Preventing destruction with a lifecycle rule] bridge-before: Watch how prevent_destroy turns a destructive change into an error. The clip uses automatic apply approval; use Devspace’s separate plan inspection and supplied authorization instead. | bridge-after: The clip demonstrates prevention while the rule remains configured. The text supplies default and reversed replacement ordering, the complete controlled plan-before-apply procedure, and the separate requirement for scope and impact approval.
  - kK8wbPBNVxA 406-504s facts=['f2'] label: Set prevent_destroy and observe a destruction-prevention error | summary: Setting prevent_destroy = true protects a configured resource against a change that requires its destruction. After changing the configuration, the presenter attempts an automatically approved apply and receives an “instance cannot be destroyed” error. The presenter then explains that removing the lifecycle rule would permit the previously blocked change. This protection depends on the rule remaining in configuration; it does not establish that a permitted change is safe or authorized.

### s08 · check · Review replacement lifecycle evidence
Check your understanding — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [choice, core, grading=client] A replacement plan shows the expected lifecycle order. What does that evidence establish about permission to apply?
  ✔ a: It verifies replacement mechanics, but scope and impact approval are still required before a permitted apply.
      why: Correct. It verifies replacement mechanics, but scope and impact approval are still required before a permitted apply.
  ✘ b: The expected order itself authorizes the replacement.
      why: Lifecycle plan evidence does not replace scope and impact approval.
  ✘ c: A prevent_destroy rejection can be applied because it documents the protected resource.
      why: A rejected plan is not a permitted apply.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The sandbox instance is provisioned, the configured lifecycle argument produces the expected replacement order or prevention error, and an approved permitted replacement provisions the replacement EC2 instance. Recorded plan evidence is separate from scope and impact approval; a rejected plan is not applied.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r03
  MEASURES: B:distinguish_plan_evidence_from_replacement_authorization(f3,f4)   anchors=['assessment:distinguish_plan_evidence_from_replacement_authorization']
  taught-before-tested: B.f3←s05; B.f4←s05

### s09 · hands_on · Review replacement lifecycle evidence
Evidence review — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read the resource lifecycle and replacement-plan excerpts. Classify the mechanics separately from scope/impact approval; a rejected plan must not be applied.
  'The sandbox EC2 instance exists and the supplied lifecycle setting is inside its resource block. The controlled replacement-triggering change produced the plan shown. For permitted plans only, supplied scope/impact approval precedes apply and resource verification confirms the replacement EC2 instance. The rejected plan is not applied.
```text
plan: "replacement-default"
lifecycle_setting: "default"
triggering_diff: "Supplied replacement-triggering EC2 argument edit"
plan_outcome: "destroy before create"
scope_impact_approval: "Supplied approval required before permitted apply"
```' -> Destroy before create  (column lifecycle_setting, role=categorical)
      feedback: Judgement: Destroy before create. Compare the stated evidence with the required criterion.
  'The sandbox EC2 instance exists and the supplied lifecycle setting is inside its resource block. The controlled replacement-triggering change produced the plan shown. For permitted plans only, supplied scope/impact approval precedes apply and resource verification confirms the replacement EC2 instance. The rejected plan is not applied.
```text
plan: "replacement-reversed"
lifecycle_setting: "create_before_destroy"
triggering_diff: "Supplied replacement-triggering EC2 argument edit"
plan_outcome: "create before destroy where supported"
scope_impact_approval: "Supplied approval required before permitted apply"
```' -> Create before destroy where supported  (column lifecycle_setting, role=categorical)
      feedback: Judgement: Create before destroy where supported. Compare the stated evidence with the required criterion.
  'The sandbox EC2 instance exists and the supplied lifecycle setting is inside its resource block. The controlled replacement-triggering change produced the plan shown. For permitted plans only, supplied scope/impact approval precedes apply and resource verification confirms the replacement EC2 instance. The rejected plan is not applied.
```text
plan: "replacement-prevented"
lifecycle_setting: "prevent_destroy"
triggering_diff: "Supplied replacement-triggering EC2 argument edit"
plan_outcome: "destruction plan rejected while rule remains configured"
scope_impact_approval: "Rejected plan is not applied"
```' -> Destruction rejected: do not apply  (column lifecycle_setting, role=categorical)
      feedback: Judgement: Destruction rejected: do not apply. Compare the stated evidence with the required criterion.
  'Alternate decision: the plan has the requested create-before-destroy order, so apply proceeds without the supplied scope/impact approval.' -> Plan treated incorrectly as authorization
      feedback: Judgement: Plan treated incorrectly as authorization. Compare the stated evidence with the required criterion.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The sandbox instance is provisioned, the configured lifecycle argument produces the expected replacement order or prevention error, and an approved permitted replacement provisions the replacement EC2 instance. Recorded plan evidence is separate from scope and impact approval; a rejected plan is not applied.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r04
  MEASURES: B:predict_replacement_order_from_lifecycle_and_diff(f1); B:predict_destruction_prevention_from_lifecycle_and_diff(f2); B:distinguish_plan_evidence_from_replacement_authorization(f3,f4)   anchors=['practice', 'assessment:predict_replacement_order_from_lifecycle_and_diff', 'assessment:predict_destruction_prevention_from_lifecycle_and_diff', 'assessment:distinguish_plan_evidence_from_replacement_authorization']
  taught-before-tested: B.f1←s05; B.f2←s05; B.f3←s05; B.f4←s05

### s10 · recap · Keep these distinctions
(takeaway) Bootstrap the protected bucket first. Select the existing backend, initialize and migrate with approval, then verify the intended state location. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Inspect replacement order or prevention errors. create_before_destroy is conditional; prevent_destroy applies while configured. Keep scope and impact approval separate. ⟦B.f1 B.f2 B.f3 B.f4 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template: Next: Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the evidence
(mechanism) The S3 backend stores state at a specified bucket and key, separate from managed-resource declarations. First provision the protected bucket using the supplied local-state bootstrap configuration. ⟦A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) After changing the backend, run terraform init -migrate-state, approve the supplied migration and verify state at the intended bucket/key. ⟦A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) The backend block selects storage; it does not create its own bucket. Keep the local-state bootstrap result and migrated-state destination in the record, then verify the intended bucket/key. ⟦A.f2 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.backend_sequence cols=['sequence', 'step', 'evidence', 'bucket', 'key', 'region'] ] caption: 
### r02 · Separate the evidence
(mechanism) The S3 backend stores state at a specified bucket and key, separate from managed-resource declarations. First provision the protected bucket using the supplied local-state bootstrap configuration. ⟦A.f1 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Select that existing bucket with the line-separated backend block below, using the supplied bucket, key, Region and protection settings. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(syntax) terraform {
  backend "s3" {
    bucket = "BUCKET"
    key = "KEY"
    region = "REGION"
  }
} ⟦A.f3 A:tb3⟧
(misconception) The backend block selects storage; it does not create its own bucket. Keep the local-state bootstrap result and migrated-state destination in the record, then verify the intended bucket/key. ⟦A.f1 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.backend_sequence cols=['sequence', 'step', 'evidence', 'bucket', 'key', 'region'] ] caption: 
### r03 · Separate the evidence
(mechanism) Set the supplied lifecycle argument in the resource block, introduce the controlled replacement-triggering change and inspect the plan’s order or prevention error before an approved permitted apply. Lifecycle controls do not replace scope and impact approval. ⟦B.f3 B.f4 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(misconception) Compare ordering with prevention: create_before_destroy requests reversed order where supported, while a still-configured prevent_destroy rejects destruction. Neither outcome establishes acceptable scope or impact. Inspect plan evidence before an approved permitted apply; do not apply a rejected plan. ⟦B.f3 B.f4 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.replacement_controls cols=['plan', 'lifecycle_setting', 'triggering_diff', 'plan_outcome', 'scope_impact_approval'] ] caption: 
### r04 · Separate the evidence
(mechanism) Terraform normally destroys an object before creating its replacement. create_before_destroy requests the reverse order where supported. ⟦B.f1 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(mechanism) prevent_destroy rejects a destruction plan while that lifecycle rule remains in the resource’s configuration. ⟦B.f2 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Set the supplied lifecycle argument in the resource block, introduce the controlled replacement-triggering change and inspect the plan’s order or prevention error before an approved permitted apply. Lifecycle controls do not replace scope and impact approval. ⟦B.f3 B.f4 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(misconception) Compare ordering with prevention: create_before_destroy requests reversed order where supported, while a still-configured prevent_destroy rejects destruction. Neither outcome establishes acceptable scope or impact. Inspect plan evidence before an approved permitted apply; do not apply a rejected plan. ⟦B.f1 B.f2 B.f3 B.f4 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.replacement_controls cols=['plan', 'lifecycle_setting', 'triggering_diff', 'plan_outcome', 'scope_impact_approval'] ] caption: 

=========

# EVALUATOR PACKET — Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template (aws_devops.tile.112)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.automate_isolated_infrastructure_restoration_using_a_supplied_cloudformation_ec2_template — Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template; directly require the native EC2 instance foundation

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.automate_isolated_infrastructure_restoration_using_a_supplied_cloudformation_ec2_template)   objective: Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template
A.f1: Creating a stack from a template provisions its declared resources under the target account’s execution authority and selected Region.   [sources: aws_cloudformation_user_guide#cfn-console-create-stack.html]
A.f2: Use the supplied restoration template, approved recovery credentials, explicit isolated target and required parameters to create the replacement EC2 stack.   [sources: aws_cloudformation_user_guide#cfn-console-create-stack.html]
A.f3: Monitor stack events until creation completes, inspect resource IDs and outputs, and run the supplied instance and service recovery-ready checks.   [sources: aws_cloudformation_user_guide#cfn-console-view-stack-data-resources.html]
note: Use supplied template and checks; do not introduce production cutover or guest-OS authoring.
PRACTICE ANCHOR (tool_simulation): Create a replacement EC2 stack from one supplied CloudFormation restoration template using approved recovery credentials, the explicit isolated account and Region, and required parameters. Monitor stack events, inspect resource IDs and outputs, and execute the supplied instance and service recovery-ready checks.  SUCCESS: The stack is created in the approved isolated account and Region with the supplied template and required parameters. Creation completes, resource IDs and outputs are inspected, and the supplied instance and service checks pass. Stack completion and recovery-check results are recorded separately.
ASSESSMENT ANCHOR: verify_restoration_target_and_execution_authority facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_stack_completion_and_resource_evidence facts=['f3']
ASSESSMENT ANCHOR: verify_supplied_instance_and_service_recovery_ready_checks facts=['f3']

## DATA ASSETS USED
ds.restoration_checks: Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template; directly require the native EC2 instance foundation — read-only evidence — columns: case_id(identifier), account(identifier), region(categorical), execution_authority(identifier), template(identifier), parameters(text), stack_events(categorical), resource_id(identifier), outputs(text), instance_check(categorical), service_check(categorical)
   ["restore-service-fails","exercise-isolated-account","REGION","exercise-recovery-role","supplied-ec2-template","Supplied isolated network and instance parameters","creation complete","exercise-recovery-instance","Instance: exercise-recovery-instance","pass","fail"]
   ["restore-service-passes","exercise-isolated-account","REGION","exercise-recovery-role","supplied-ec2-template","Supplied isolated network and instance parameters","creation complete","exercise-recovery-instance","Instance: exercise-recovery-instance","pass","pass"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Block release on actionable dependency or image security findings; Control environment promotion with a manual approval; Diagnose EC2 or container health failures using telemetry and prepared Linux inspection skills; Diagnose a failed delivery pipeline action; Document incident evidence and a preventive change using reused systematic-debugging coverage; Endpoint cutover; Gate release completion on a deployed-service smoke check; Handle failed event delivery with bounded retries and failure capture; Perform a controlled ECS service rollout; Promote the same artifact version across environments; Recover an incident safely using an established runbook; Residual charge verification; State access isolation; State locking; Verify restored service and data against RTO/RPO in an isolated rehearsal

## LESSON, in learner order

### s01 · explainer · Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template
Read the evidence — 
(mechanism) Stack creation provisions the template’s declared resources under the target account’s execution authority and selected Region. ⟦A.f1 A:tb1 A:tb2 A:tb3⟧
(mechanism) Create the replacement EC2 stack with the supplied restoration template, approved recovery credentials, explicit isolated target and required parameters. ⟦A.f2 A:tb1 A:tb2 A:tb3⟧
(mechanism) Monitor events until creation completes. Inspect resource IDs and outputs, then perform the supplied instance and service recovery-ready checks. ⟦A.f3 A:tb1 A:tb2 A:tb3⟧
[DIAGRAM] nodes=['Isolated account, Region and execution authority', 'Supplied template and required parameters', 'Stack events, resource IDs and outputs', 'Separate instance and service checks'] edges=[] alt: Make the isolated account and Region, approved execution authority, supplied template and parameters, completed stack events, resource IDs and outputs, and separate instance and service recovery-check results visible.
[TABLE ds.restoration_checks cols=['case_id', 'account', 'region', 'execution_authority', 'template', 'parameters', 'stack_events', 'resource_id', 'outputs', 'instance_check', 'service_check'] ] caption: 

### s02 · explainer · Compare the evidence
Read the evidence — 
(example) Completed stack events are not the service recovery-ready result. Compare the supplied instance and service checks with resource IDs and outputs; preserve a failed service check even when the instance check passes. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · check · Review isolated stack restoration
Check your understanding — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] Which restoration setup matches the required target and execution authority?
  ✔ a: The supplied template and parameters, approved recovery credentials, and explicit isolated account and Region.
      why: Correct. The supplied template and parameters, approved recovery credentials, and explicit isolated account and Region.
  ✘ b: The supplied template with the current account and Region left unverified.
      why: Stack resources are provisioned under the selected account authority and Region; these must be explicit and approved.
  ✘ c: An arbitrary replacement template in the isolated account, regardless of required parameters.
      why: Isolation does not replace using the supplied restoration template and required parameters.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The stack is created in the approved isolated account and Region with the supplied template and required parameters. Creation completes, resource IDs and outputs are inspected, and the supplied instance and service checks pass. Stack completion and recovery-check results are recorded separately.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r01
  MEASURES: A:verify_restoration_target_and_execution_authority(f1,f2)   anchors=['assessment:verify_restoration_target_and_execution-8462ff44']
  taught-before-tested: A.f1←s01; A.f2←s01

### s04 · hands_on · Review isolated stack restoration
Evidence review — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read the isolated restoration records. Decide whether recovery readiness is verified or remains unverified despite stack completion. Inspect resource IDs and outputs and judge both supplied checks separately from stack status.
  'The supplied template and required parameters were used with approved recovery credentials in the explicit isolated account and Region. Stack events were monitored to completion; resource IDs and outputs were inspected.
```text
case_id: "restore-service-fails"
account: "exercise-isolated-account"
region: "REGION"
execution_authority: "exercise-recovery-role"
template: "supplied-ec2-template"
parameters: "Supplied isolated network and instance parameters"
stack_events: "creation complete"
resource_id: "exercise-recovery-instance"
outputs: "Instance: exercise-recovery-instance"
instance_check: "pass"
service_check: "fail"
```' -> Stack complete but recovery checks not all passing  (column service_check, role=categorical)
      feedback: Judgement: Stack complete but recovery checks not all passing. Compare the stated evidence with the required criterion.
  'The supplied template and required parameters were used with approved recovery credentials in the explicit isolated account and Region. Stack events were monitored to completion; resource IDs and outputs were inspected.
```text
case_id: "restore-service-passes"
account: "exercise-isolated-account"
region: "REGION"
execution_authority: "exercise-recovery-role"
template: "supplied-ec2-template"
parameters: "Supplied isolated network and instance parameters"
stack_events: "creation complete"
resource_id: "exercise-recovery-instance"
outputs: "Instance: exercise-recovery-instance"
instance_check: "pass"
service_check: "pass"
```' -> Stack and supplied recovery checks verified  (column service_check, role=categorical)
      feedback: Judgement: Stack and supplied recovery checks verified. Compare the stated evidence with the required criterion.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The stack is created in the approved isolated account and Region with the supplied template and required parameters. Creation completes, resource IDs and outputs are inspected, and the supplied instance and service checks pass. Stack completion and recovery-check results are recorded separately.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r02
  MEASURES: A:verify_stack_completion_and_resource_evidence(f3); A:verify_supplied_instance_and_service_recovery_ready_checks(f3)   anchors=['practice', 'assessment:verify_stack_completion_and_resource_evidence', 'assessment:verify_supplied_instance_and_service_re-db15f333']
  taught-before-tested: A.f3←s01; A.f3←s01

### s05 · recap · Keep these distinctions
(takeaway) Use the approved isolated target and supplied template. Verify stack completion, IDs and outputs, then both instance and service readiness. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Gate release on actionable security findings: Next: Gate release on actionable security findings.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the evidence
(mechanism) Stack creation provisions the template’s declared resources under the target account’s execution authority and selected Region. ⟦A.f1 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Create the replacement EC2 stack with the supplied restoration template, approved recovery credentials, explicit isolated target and required parameters. ⟦A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Completed stack events are not the service recovery-ready result. Compare the supplied instance and service checks with resource IDs and outputs; preserve a failed service check even when the instance check passes. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.restoration_checks cols=['case_id', 'account', 'region', 'execution_authority', 'template', 'parameters', 'stack_events', 'resource_id', 'outputs', 'instance_check', 'service_check'] ] caption: 
### r02 · Separate the evidence
(mechanism) Monitor events until creation completes. Inspect resource IDs and outputs, then perform the supplied instance and service recovery-ready checks. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Completed stack events are not the service recovery-ready result. Compare the supplied instance and service checks with resource IDs and outputs; preserve a failed service check even when the instance check passes. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.restoration_checks cols=['case_id', 'account', 'region', 'execution_authority', 'template', 'parameters', 'stack_events', 'resource_id', 'outputs', 'instance_check', 'service_check'] ] caption: 

=========

# EVALUATOR PACKET — Gate release on actionable security findings (aws_devops.tile.113)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.block_release_on_actionable_dependency_or_image_security_findings — Block release on actionable dependency or image security findings

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.block_release_on_actionable_dependency_or_image_security_findings)   objective: Gate release on actionable security findings
A.f1: Inspector findings report vulnerability evidence, affected resources and severity that can inform release decisions.   [sources: aws_inspector_user_guide#findings-understanding.html]
A.f2: Compare the supplied scan report with the stated severity threshold and documented exception policy to decide whether a finding is actionable.   [sources: aws_inspector_user_guide#findings-understanding.html]
A.f3: Make the scan-policy check return failure for an actionable unexcepted finding and require its success before promotion; retain the report and policy decision as evidence.   [sources: github_actions_docs#how-tos/create-and-publish-actions/set-exit-codes]
note: Use supplied scan/threshold/exceptions; do not invent vulnerability facts or policy exceptions.
PRACTICE ANCHOR (tool_simulation): Using a supplied Inspector report, severity threshold, documented exceptions and pipeline controls, block one pipeline run on an actionable unexcepted dependency or image finding.  SUCCESS: The supplied scan-policy check returns failure for the actionable unexcepted finding, promotion remains blocked because it requires that check's success, and the report and policy decision are retained as evidence.
ASSESSMENT ANCHOR: identify_finding_evidence_resource_and_severity facts=['f1']
ASSESSMENT ANCHOR: apply_severity_threshold_and_documented_exceptions facts=['f2']
ASSESSMENT ANCHOR: determine_blocking_gate_outcome_and_required_evidence facts=['f3']

## DATA ASSETS USED
ds.security_findings: Block release on actionable dependency or image security findings — read-only evidence — columns: finding_id(identifier), affected_resource(identifier), vulnerability_evidence(text), severity(categorical), threshold(categorical), exception_basis(text), policy_result(categorical), promotion(categorical)
   ["finding-0","exercise-image","Supplied scan report identifies an affected image dependency","HIGH","HIGH","","fail","blocked"]
   ["finding-1","exercise-image","Supplied scan report identifies an affected image dependency","HIGH","HIGH","Supplied documented exception covers this finding","pass","permitted by this gate"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Control environment promotion with a manual approval; Diagnose EC2 or container health failures using telemetry and prepared Linux inspection skills; Diagnose a failed delivery pipeline action; Document incident evidence and a preventive change using reused systematic-debugging coverage; Endpoint cutover; Gate release completion on a deployed-service smoke check; Handle failed event delivery with bounded retries and failure capture; Perform a controlled ECS service rollout; Promote the same artifact version across environments; Recover an incident safely using an established runbook; Residual charge verification; State access isolation; State locking; Verify restored service and data against RTO/RPO in an isolated rehearsal

## LESSON, in learner order

### s01 · explainer · Gate release on actionable security findings
Read the evidence — 
(mechanism) Inspector findings provide vulnerability evidence, affected resources and severity to inform release decisions. ⟦A.f1 A:tb1 A:tb2 A:tb3⟧
(mechanism) Compare the supplied scan report with the stated severity threshold and documented exception policy to decide actionability. ⟦A.f2 A:tb1 A:tb2 A:tb3⟧
(mechanism) The policy check must fail for an actionable unexcepted finding, and promotion must require its success. Retain the report and policy decision: running a scan alone does not enforce a gate. ⟦A.f3 A:tb1 A:tb2 A:tb3⟧
[DIAGRAM] nodes=['Finding: vulnerability evidence, affected resource and severity', 'Threshold and documented exception policy', 'Policy result and promotion dependency', 'Retained report and policy decision'] edges=[] alt: Show the supplied finding's vulnerability evidence, affected resource and severity alongside the threshold and exception decision, with the scan-policy check failed, promotion blocked and retained evidence accessible.
[TABLE ds.security_findings cols=['finding_id', 'affected_resource', 'vulnerability_evidence', 'severity', 'threshold', 'exception_basis', 'policy_result', 'promotion'] ] caption: 

### s02 · explainer · Compare the evidence
Read the evidence — 
(example) Compare an unexcepted actionable finding with a documented exception. Both remain scan evidence; retain the exception basis for its different gate outcome. A tolerated policy failure would not enforce the promotion precondition. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · check · Review scan-policy gate evidence
Check your understanding — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] The scan-policy check identifies an actionable unexcepted finding. Which gate result and evidence are required?
  ✔ a: Return failure, block promotion because it requires check success, and retain the scan report and policy decision.
      why: Correct. Return failure, block promotion because it requires check success, and retain the scan report and policy decision.
  ✘ b: Return success so promotion can proceed, while keeping the report.
      why: Keeping a report does not make an actionable unexcepted finding a passing policy result.
  ✘ c: Return failure but allow promotion without requiring the scan-policy check to succeed.
      why: A failing check only gates progression when promotion requires its success.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The supplied scan-policy check returns failure for the actionable unexcepted finding, promotion remains blocked because it requires that check's success, and the report and policy decision are retained as evidence.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r01
  MEASURES: A:determine_blocking_gate_outcome_and_required_evidence(f3)   anchors=['assessment:determine_blocking_gate_outcome_and_required_evidence']
  taught-before-tested: A.f3←s01

### s04 · hands_on · Review scan-policy gate evidence
Evidence review — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read the finding and scan-policy excerpts. Decide which finding blocks promotion and which is permitted by this policy gate. Compare affected resource, evidence and severity with threshold and documented exceptions.
  'Supplied policy treats severity at the shown threshold as actionable unless the documented exception covers the finding. Promotion requires scan-policy check success. The scan report and policy decision are retained for both outcomes.
```text
finding_id: "finding-0"
affected_resource: "exercise-image"
vulnerability_evidence: "Supplied scan report identifies an affected image dependency"
severity: "HIGH"
threshold: "HIGH"
exception_basis: ""
policy_result: "fail"
promotion: "blocked"
```' -> Actionable unexcepted finding: promotion blocked  (column exception_basis, role=text)
      feedback: Judgement: Actionable unexcepted finding: promotion blocked. Compare the stated evidence with the required criterion.
  'Supplied policy treats severity at the shown threshold as actionable unless the documented exception covers the finding. Promotion requires scan-policy check success. The scan report and policy decision are retained for both outcomes.
```text
finding_id: "finding-1"
affected_resource: "exercise-image"
vulnerability_evidence: "Supplied scan report identifies an affected image dependency"
severity: "HIGH"
threshold: "HIGH"
exception_basis: "Supplied documented exception covers this finding"
policy_result: "pass"
promotion: "permitted by this gate"
```' -> Documented exception: permitted by this gate  (column exception_basis, role=text)
      feedback: Judgement: Documented exception: permitted by this gate. Compare the stated evidence with the required criterion.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The supplied scan-policy check returns failure for the actionable unexcepted finding, promotion remains blocked because it requires that check's success, and the report and policy decision are retained as evidence.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r02
  MEASURES: A:identify_finding_evidence_resource_and_severity(f1); A:apply_severity_threshold_and_documented_exceptions(f2)   anchors=['practice', 'assessment:identify_finding_evidence_resource_and_severity', 'assessment:apply_severity_threshold_and_documented_exceptions']
  taught-before-tested: A.f1←s01; A.f2←s01

### s05 · recap · Keep these distinctions
(takeaway) Apply the stated threshold and documented exceptions to scan evidence. Fail actionable unexcepted findings and require policy success for promotion. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Diagnose a failed delivery pipeline action: Next: Diagnose a failed delivery pipeline action.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the evidence
(mechanism) The policy check must fail for an actionable unexcepted finding, and promotion must require its success. Retain the report and policy decision: running a scan alone does not enforce a gate. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Compare an unexcepted actionable finding with a documented exception. Both remain scan evidence; retain the exception basis for its different gate outcome. A tolerated policy failure would not enforce the promotion precondition. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.security_findings cols=['finding_id', 'affected_resource', 'vulnerability_evidence', 'severity', 'threshold', 'exception_basis', 'policy_result', 'promotion'] ] caption: 
### r02 · Separate the evidence
(mechanism) Inspector findings provide vulnerability evidence, affected resources and severity to inform release decisions. ⟦A.f1 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Compare the supplied scan report with the stated severity threshold and documented exception policy to decide actionability. ⟦A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Compare an unexcepted actionable finding with a documented exception. Both remain scan evidence; retain the exception basis for its different gate outcome. A tolerated policy failure would not enforce the promotion precondition. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.security_findings cols=['finding_id', 'affected_resource', 'vulnerability_evidence', 'severity', 'threshold', 'exception_basis', 'policy_result', 'promotion'] ] caption: 

=========

# EVALUATOR PACKET — Diagnose a failed delivery pipeline action / Diagnose workload health failure from telemetry (aws_devops.tile.114)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.diagnose_a_failed_delivery_pipeline_action — Diagnose a failed delivery pipeline action
B = aws_devops.diagnose_ec2_or_container_health_failures_using_telemetry_and_prepared_linux_inspection_skills — Diagnose EC2 or container health failures using telemetry and prepared Linux inspection skills

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.diagnose_a_failed_delivery_pipeline_action)   objective: Diagnose a failed delivery pipeline action
A.f1: Pipeline execution and action history identify failed actions and their error details.   [sources: aws_codepipeline_user_guide#troubleshooting.html]
A.f2: Find the first failing action in the selected execution, inspect its input artifact revision and linked service logs, and use the error evidence to identify the correction.   [sources: aws_codepipeline_user_guide#pipelines-view-console.html]
A.f3: Retest after the approved correction and verify that action succeeds before investigating later dependent actions that did not run.   [sources: aws_codepipeline_user_guide#troubleshooting.html]
note: Use supplied logs/error evidence; do not invent corrective commands or unsupported causes.
PRACTICE ANCHOR (tool_simulation): Diagnose one seeded CodePipeline action failure using supplied execution history, action error details, input artifact revision and linked service logs. Select the evidence-supported approved correction, then retest the action.  SUCCESS: Identify the first failing action in the selected execution, retain its execution and input revision identities, and select the approved correction supported by its error details and linked service logs. After the correction, verify that action succeeds with the intended input before investigating later dependent actions that did not run.
ASSESSMENT ANCHOR: identify_first_failing_action facts=['f1', 'f2']
ASSESSMENT ANCHOR: select_evidence_supported_correction facts=['f2']
ASSESSMENT ANCHOR: verify_corrected_action_before_investigating_dependencies facts=['f3']

## SOURCE FACTS — B (aws_devops.diagnose_ec2_or_container_health_failures_using_telemetry_and_prepared_linux_inspection_skills)   objective: Diagnose workload health failure from telemetry
B.f1: EC2 system status checks concern underlying AWS host issues, while instance checks concern the instance’s software and networking.   [sources: aws_ec2_user_guide#monitoring-system-instance-status-check.html]
B.f2: Use the supplied metric and log time window to identify the affected workload, then inspect the component’s service status, events and logs rather than assuming the symptom proves its cause.   [sources: aws_well_architected_framework#ops06-bp01.html]
B.f3: For a container, inspect container state, exit status and recent logs; apply the evidence-supported correction and repeat the supplied health check.   [sources: aws_ecs_developer_guide#stopped-task-errors.html]
note: Require external Linux service/process preparation; do not author new inspection commands or boot-startup configuration.
PRACTICE ANCHOR (tool_simulation): Resolve one seeded container health failure using supplied inspection tools: correlate the supplied metric and log time window with the affected workload, inspect component service status, events, container state, exit status and recent logs, and apply the approved correction supported by the evidence.  SUCCESS: The affected workload and failing component are correctly identified from evidence within the supplied time window. The learner applies the evidence-supported approved correction and repeats the supplied health check, confirming that the original failure is resolved rather than relying only on an improved metric or restarted process.
ASSESSMENT ANCHOR: distinguish_ec2_system_and_instance_status_check_boundaries facts=['f1']
ASSESSMENT ANCHOR: identify_failing_workload_component_from_correlated_telemetry_and_inspection facts=['f2', 'f3']
ASSESSMENT ANCHOR: verify_evidence_supported_correction_with_repeated_health_check facts=['f3']

## DATA ASSETS USED
ds.health_inspection: Diagnose EC2 or container health failures using telemetry and prepared Linux inspection skills — read-only evidence — columns: workload(identifier), interval_start(datetime), interval_end(datetime), component(categorical), telemetry(text), container_state(categorical), exit_status(categorical), recent_logs(text), health_check(categorical), correction(text)
   ["exercise-container","2026-01-15T10:00:00+00:00","2026-01-15T10:05:00+00:00","application container","Client request health checks fail","exited",1,"Supplied log identifies a component configuration error","fail","Supplied approved component configuration correction"]
   ["exercise-container","2026-01-15T10:05:00+00:00","2026-01-15T10:10:00+00:00","application container","Metric improved after component correction","running",null,"Component restarted after supplied correction","fail","Retain required failed health check; metric improvement is insufficient"]
   ["exercise-container","2026-01-15T10:10:00+00:00","2026-01-15T10:15:00+00:00","application container","Repeated client request check","running",null,"Component inspection consistent with supplied correction","pass","Supplied correction verified by repeated health check"]
ds.pipeline_actions: Diagnose a failed delivery pipeline action — read-only evidence — columns: execution_id(identifier), revision(identifier), action(categorical), status(categorical), error_details(text), linked_service_logs(text), approved_correction(text)
   ["pipeline-original","exercise-revision","source","success","","",""]
   ["pipeline-original","exercise-revision","build","failed","Build failed because the configured application directory was absent","Build log: cannot enter /workspace/app-old; supplied checkout contains /workspace/app","Change the build working directory to /workspace/app"]
   ["pipeline-original","exercise-revision","deployment","did not run","","",""]
   ["pipeline-retest","exercise-revision","build","success","","Retest build log: successful execution from /workspace/app with the intended input","Build working directory changed to /workspace/app"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Control environment promotion with a manual approval; Diagnose EC2 or container health failures using telemetry and prepared Linux inspection skills; Document incident evidence and a preventive change using reused systematic-debugging coverage; Endpoint cutover; Gate release completion on a deployed-service smoke check; Handle failed event delivery with bounded retries and failure capture; Perform a controlled ECS service rollout; Promote the same artifact version across environments; Recover an incident safely using an established runbook; Residual charge verification; State access isolation; State locking; Verify restored service and data against RTO/RPO in an isolated rehearsal

## LESSON, in learner order

### s01 · explainer · Diagnose a failed delivery pipeline action
Read the evidence — 
(mechanism) Execution and action history identify failures and error details. Start with the first failing action in the selected execution; inspect its input revision and linked service logs to identify the correction. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3⟧
(mechanism) After the approved correction, retest and verify that action succeeds before investigating later dependent actions that did not run. ⟦A.f3 A:tb1 A:tb2 A:tb3⟧
[DIAGRAM] nodes=['Selected execution and input artifact revision', 'Successful source action', 'First failing build: error details and linked logs', 'Dependent deployment: did not run', 'Approved correction and intended-input retest'] edges=[('n1', 'n2', 'execution order'), ('n2', 'n3', 'dependency blocked'), ('n2', 'n4', 'approved correction and retest')] alt: Show the selected CodePipeline execution with a successful source action, a failed build action and a deployment action that did not run. Make the failed action's input artifact revision, error details and linked service logs visible, followed by its successful retest with the intended input.
[TABLE ds.pipeline_actions cols=['execution_id', 'revision', 'action', 'status', 'error_details', 'linked_service_logs', 'approved_correction'] ] caption: 

### s02 · explainer · Compare the evidence
Read the evidence — 
(example) The supplied source succeeded, the build failed and deployment did not run. Inspect build error details and linked logs, apply the evidence-supported approved correction, then verify build success with the intended input. An unrun deployment is not an independent error. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · check · Review pipeline failure evidence
Check your understanding — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] After an approved correction to the first failed action, what should be verified before investigating later actions that did not run?
  ✔ a: Retest and verify the corrected action succeeds with the intended input.
      why: Correct. Retest and verify the corrected action succeeds with the intended input.
  ✘ b: Investigate the skipped deployment first without retesting the failed action.
      why: Verify the corrected failure before investigating later dependent actions that did not run.
  ✘ c: Treat approval of the correction as proof the action now succeeds.
      why: Approval does not replace execution evidence from the retest.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. Identify the first failing action in the selected execution, retain its execution and input revision identities, and select the approved correction supported by its error details and linked service logs. After the correction, verify that action succeeds with the intended input before investigating later dependent actions that did not run.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r01
  MEASURES: A:verify_corrected_action_before_investigating_dependencies(f3)   anchors=['assessment:verify_corrected_action_before_investigating_dependencies']
  taught-before-tested: A.f3←s01

### s04 · hands_on · Review pipeline failure evidence
Evidence review — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, core, grading=client] Read selected execution/action evidence and the retest. Identify the first failed action with its supported correction, distinguish skipped dependencies, and judge verification of the corrected action with the intended input.
  'For the original selected execution the action order is source, build, deployment. The correction shown was approved before retest; execution and input revision identities are retained. Retest success precedes investigation of later dependencies.
```text
execution_id: "pipeline-original"
revision: "exercise-revision"
action: "source"
status: "success"
error_details: ""
linked_service_logs: ""
approved_correction: ""
```' -> Earlier successful action  (column status, role=categorical)
      feedback: Judgement: Earlier successful action. Compare the stated evidence with the required criterion.
  'For the original selected execution the action order is source, build, deployment. The correction shown was approved before retest; execution and input revision identities are retained. Retest success precedes investigation of later dependencies.
```text
execution_id: "pipeline-original"
revision: "exercise-revision"
action: "build"
status: "failed"
error_details: "Build failed because the configured application directory was absent"
linked_service_logs: "Build log: cannot enter /workspace/app-old; supplied checkout contains /workspace/app"
approved_correction: "Change the build working directory to /workspace/app"
```' -> First failed action: evidence-supported correction  (column status, role=categorical)
      feedback: Judgement: First failed action: evidence-supported correction. Compare the stated evidence with the required criterion.
  'For the original selected execution the action order is source, build, deployment. The correction shown was approved before retest; execution and input revision identities are retained. Retest success precedes investigation of later dependencies.
```text
execution_id: "pipeline-original"
revision: "exercise-revision"
action: "deployment"
status: "did not run"
error_details: ""
linked_service_logs: ""
approved_correction: ""
```' -> Later dependent action did not run  (column status, role=categorical)
      feedback: Judgement: Later dependent action did not run. Compare the stated evidence with the required criterion.
  'For the original selected execution the action order is source, build, deployment. The correction shown was approved before retest; execution and input revision identities are retained. Retest success precedes investigation of later dependencies.
```text
execution_id: "pipeline-retest"
revision: "exercise-revision"
action: "build"
status: "success"
error_details: ""
linked_service_logs: "Retest build log: successful execution from /workspace/app with the intended input"
approved_correction: "Build working directory changed to /workspace/app"
```' -> Corrected action verified with intended input  (column status, role=categorical)
      feedback: Judgement: Corrected action verified with intended input. Compare the stated evidence with the required criterion.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. Identify the first failing action in the selected execution, retain its execution and input revision identities, and select the approved correction supported by its error details and linked service logs. After the correction, verify that action succeeds with the intended input before investigating later dependent actions that did not run.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r02
  MEASURES: A:identify_first_failing_action(f1,f2); A:select_evidence_supported_correction(f2); A:verify_corrected_action_before_investigating_dependencies(f3)   anchors=['practice', 'assessment:identify_first_failing_action', 'assessment:select_evidence_supported_correction', 'assessment:verify_corrected_action_before_investigating_dependencies']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f2←s01; A.f3←s01

### s05 · explainer · Diagnose workload health failure from telemetry
Read the evidence — 
(mechanism) EC2 system status checks concern underlying AWS host issues; instance checks concern instance software and networking. ⟦B.f1 B:tb1 B:tb2 B:tb3⟧
(mechanism) Locate the affected workload using the supplied metric/log window. Inspect component service status, events and logs: the symptom alone does not prove its cause. ⟦B.f2 B:tb1 B:tb2 B:tb3⟧
(mechanism) For a container, inspect state, exit status and recent logs. Apply the evidence-supported correction and repeat the supplied health check. ⟦B.f3 B:tb1 B:tb2 B:tb3⟧
[DIAGRAM] nodes=['Affected workload and telemetry interval', 'Component state, exit status and recent logs', 'Evidence-supported correction', 'Original and repeated health checks'] edges=[] alt: Show the supplied telemetry interval and affected workload alongside component inspection results, including container state, exit status and recent logs, with the original and repeated health-check results visible.
[TABLE ds.health_inspection cols=['workload', 'interval_start', 'interval_end', 'component', 'telemetry', 'container_state', 'exit_status', 'recent_logs', 'health_check', 'correction'] ] caption: 

### s06 · explainer · Compare the evidence
Read the evidence — 
(example) A restarted component or improved metric does not erase a failed health check. Tie component logs to the affected workload and telemetry interval, and retain original and repeated health-check outcomes after the approved correction. ⟦B.f1 B.f2 B.f3 B:tb4 B:tb5⟧

### s07 · check · Review component health evidence
Check your understanding — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [choice, core, grading=client] Which pairing correctly distinguishes EC2 status-check boundaries?
  ✔ a: System checks concern the underlying AWS host; instance checks concern instance software and networking.
      why: Correct. System checks concern the underlying AWS host; instance checks concern instance software and networking.
  ✘ b: System checks concern instance software; instance checks concern the underlying AWS host.
      why: These boundaries are reversed: system is host, instance is software and networking.
  ✘ c: Both checks exclusively concern the underlying host.
      why: Instance checks cover the instance software and networking, not exclusively the underlying host.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The affected workload and failing component are correctly identified from evidence within the supplied time window. The learner applies the evidence-supported approved correction and repeats the supplied health check, confirming that the original failure is resolved rather than relying only on an improved metric or restarted process.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r03
  MEASURES: B:distinguish_ec2_system_and_instance_status_check_boundaries(f1)   anchors=['assessment:distinguish_ec2_system_and_instanc-66c2af67']
  taught-before-tested: B.f1←s05

### s08 · hands_on · Review component health evidence
Evidence review — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read the time-correlated workload/component evidence. Decide whether each excerpt identifies the failure, shows an insufficient improvement, or verifies resolution through the repeated supplied health check.
  'Service status and events were inspected for the shown affected workload and component in the supplied time window. Container state, exit status and recent logs were inspected. The supplied approved correction is supported by the original component log; the original and repeated health-check results remain visible.
```text
workload: "exercise-container"
interval_start: "2026-01-15T10:00:00+00:00"
interval_end: "2026-01-15T10:05:00+00:00"
component: "application container"
telemetry: "Client request health checks fail"
container_state: "exited"
exit_status: 1
recent_logs: "Supplied log identifies a component configuration error"
health_check: "fail"
correction: "Supplied approved component configuration correction"
```' -> Correlated component failure and supported correction  (column health_check, role=categorical)
      feedback: Judgement: Correlated component failure and supported correction. Compare the stated evidence with the required criterion.
  'Service status and events were inspected for the shown affected workload and component in the supplied time window. Container state, exit status and recent logs were inspected. The supplied approved correction is supported by the original component log; the original and repeated health-check results remain visible.
```text
workload: "exercise-container"
interval_start: "2026-01-15T10:05:00+00:00"
interval_end: "2026-01-15T10:10:00+00:00"
component: "application container"
telemetry: "Metric improved after component correction"
container_state: "running"
exit_status: null
recent_logs: "Component restarted after supplied correction"
health_check: "fail"
correction: "Retain required failed health check; metric improvement is insufficient"
```' -> Improvement is not resolution: health check still fails  (column health_check, role=categorical)
      feedback: Judgement: Improvement is not resolution: health check still fails. Compare the stated evidence with the required criterion.
  'Service status and events were inspected for the shown affected workload and component in the supplied time window. Container state, exit status and recent logs were inspected. The supplied approved correction is supported by the original component log; the original and repeated health-check results remain visible.
```text
workload: "exercise-container"
interval_start: "2026-01-15T10:10:00+00:00"
interval_end: "2026-01-15T10:15:00+00:00"
component: "application container"
telemetry: "Repeated client request check"
container_state: "running"
exit_status: null
recent_logs: "Component inspection consistent with supplied correction"
health_check: "pass"
correction: "Supplied correction verified by repeated health check"
```' -> Correction verified by repeated supplied health check  (column health_check, role=categorical)
      feedback: Judgement: Correction verified by repeated supplied health check. Compare the stated evidence with the required criterion.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The affected workload and failing component are correctly identified from evidence within the supplied time window. The learner applies the evidence-supported approved correction and repeats the supplied health check, confirming that the original failure is resolved rather than relying only on an improved metric or restarted process.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r04
  MEASURES: B:identify_failing_workload_component_from_correlated_telemetry_and_inspection(f2,f3); B:verify_evidence_supported_correction_with_repeated_health_check(f3)   anchors=['practice', 'assessment:identify_failing_workload_componen-269e92f9', 'assessment:verify_evidence_supported_correcti-9cccc533']
  taught-before-tested: B.f2←s05; B.f3←s05; B.f3←s05

### s09 · recap · Keep these distinctions
(takeaway) Find the first failing action, inspect revision and logs, and verify an approved correction before investigating unrun dependents. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Distinguish system from instance checks. Inspect the affected component in the telemetry window, correct from evidence and repeat the health check. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Gate release completion on a smoke check: Next: Gate release completion on a smoke check.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the evidence
(mechanism) After the approved correction, retest and verify that action succeeds before investigating later dependent actions that did not run. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) The supplied source succeeded, the build failed and deployment did not run. Inspect build error details and linked logs, apply the evidence-supported approved correction, then verify build success with the intended input. An unrun deployment is not an independent error. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.pipeline_actions cols=['execution_id', 'revision', 'action', 'status', 'error_details', 'linked_service_logs', 'approved_correction'] ] caption: 
### r02 · Separate the evidence
(mechanism) Execution and action history identify failures and error details. Start with the first failing action in the selected execution; inspect its input revision and linked service logs to identify the correction. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) After the approved correction, retest and verify that action succeeds before investigating later dependent actions that did not run. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) The supplied source succeeded, the build failed and deployment did not run. Inspect build error details and linked logs, apply the evidence-supported approved correction, then verify build success with the intended input. An unrun deployment is not an independent error. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.pipeline_actions cols=['execution_id', 'revision', 'action', 'status', 'error_details', 'linked_service_logs', 'approved_correction'] ] caption: 
### r03 · Separate the evidence
(mechanism) EC2 system status checks concern underlying AWS host issues; instance checks concern instance software and networking. ⟦B.f1 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(misconception) A restarted component or improved metric does not erase a failed health check. Tie component logs to the affected workload and telemetry interval, and retain original and repeated health-check outcomes after the approved correction. ⟦B.f1 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.health_inspection cols=['workload', 'interval_start', 'interval_end', 'component', 'telemetry', 'container_state', 'exit_status', 'recent_logs', 'health_check', 'correction'] ] caption: 
### r04 · Separate the evidence
(mechanism) Locate the affected workload using the supplied metric/log window. Inspect component service status, events and logs: the symptom alone does not prove its cause. ⟦B.f2 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(mechanism) For a container, inspect state, exit status and recent logs. Apply the evidence-supported correction and repeat the supplied health check. ⟦B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(misconception) A restarted component or improved metric does not erase a failed health check. Tie component logs to the affected workload and telemetry interval, and retain original and repeated health-check outcomes after the approved correction. ⟦B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.health_inspection cols=['workload', 'interval_start', 'interval_end', 'component', 'telemetry', 'container_state', 'exit_status', 'recent_logs', 'health_check', 'correction'] ] caption: 

=========

# EVALUATOR PACKET — Gate release completion on a smoke check (aws_devops.tile.116)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.gate_release_completion_on_a_deployed_service_smoke_check — Gate release completion on a deployed-service smoke check

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.gate_release_completion_on_a_deployed_service_smoke_check)   objective: Gate release completion on a smoke check
A.f1: A post-deployment validation action checks live application behavior rather than merely whether a deployment operation completed.   [sources: aws_codepipeline_user_guide#actions-invoke-lambda-function.html]
A.f2: Run the supplied smoke-check action against the deployed endpoint and verify the expected response for the deployed revision.   [sources: aws_codepipeline_user_guide#actions-invoke-lambda-function.html]
A.f3: In the supplied Lambda validation action, call CodePipeline PutJobSuccessResult with the job ID only after a passing smoke check; call PutJobFailureResult on failure so dependent progression remains blocked.   [sources: aws_codepipeline_user_guide#actions-invoke-lambda-function.html]
note: Use supplied smoke action/Lambda scaffolding; do not teach application endpoint test authoring.
PRACTICE ANCHOR (tool_simulation): Add the supplied Lambda smoke-check action after deployment in a prepared CodePipeline simulation. Configure its supplied deployed endpoint and expected revision response, then connect passing and failing check outcomes to the corresponding job-result reporting paths.  SUCCESS: The action checks the supplied endpoint against the expected response for the deployed revision. A passing check calls PutJobSuccessResult with the job ID; a failing check calls PutJobFailureResult and leaves dependent progression blocked.
ASSESSMENT ANCHOR: verify_deployed_revision_behavior_from_smoke_check_evidence facts=['f1', 'f2']
ASSESSMENT ANCHOR: report_smoke_check_outcome_to_gate_release_completion facts=['f3']

## DATA ASSETS USED
ds.smoke_checks: Gate release completion on a deployed-service smoke check — read-only evidence — columns: job_id(identifier), revision(identifier), endpoint(identifier), deployment_status(categorical), expected_response(text), observed_response(categorical), job_result_call(categorical), dependent_progression(categorical)
   ["smoke-0","exercise-revision","exercise-service-endpoint","completed","Supplied expected response for exercise-revision","does not match","PutJobFailureResult","blocked"]
   ["smoke-1","exercise-revision","exercise-service-endpoint","completed","Supplied expected response for exercise-revision","matches","PutJobSuccessResult","permitted by this gate"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Control environment promotion with a manual approval; Document incident evidence and a preventive change using reused systematic-debugging coverage; Endpoint cutover; Handle failed event delivery with bounded retries and failure capture; Perform a controlled ECS service rollout; Promote the same artifact version across environments; Recover an incident safely using an established runbook; Residual charge verification; State access isolation; State locking; Verify restored service and data against RTO/RPO in an isolated rehearsal

## LESSON, in learner order

### s01 · explainer · Gate release completion on a smoke check
Read the evidence — 
(mechanism) Deployment completion is not a live behavior check. Run the supplied smoke-check action against the deployed endpoint and compare its response with the expectation for the deployed revision. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) In the supplied Lambda validation action, call PutJobSuccessResult with the job ID only after a passing check. On failure, call PutJobFailureResult so dependent progression remains blocked. Retain revision, endpoint result and job outcome together. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[PROCESS_FLOW] nodes=['Deployment operation completed', 'Supplied endpoint smoke check', 'Compare response with expected deployed revision', 'Pass: PutJobSuccessResult with job ID', 'Fail: PutJobFailureResult; dependent progression blocked'] edges=[('n0', 'n1', 'then validate'), ('n1', 'n2', 'live behavior'), ('n2', 'n3', 'matches'), ('n2', 'n4', 'does not match')] alt: Show deployment completion followed by a supplied endpoint smoke check, with the expected deployed-revision response comparison branching to PutJobSuccessResult with the job ID on pass or PutJobFailureResult with dependent progression blocked on failure.
[TABLE ds.smoke_checks cols=['job_id', 'revision', 'endpoint', 'deployment_status', 'expected_response', 'observed_response', 'job_result_call', 'dependent_progression'] ] caption: 

### s02 · video · A closer look
[VIDEO Deployment completion versus live-service validation] bridge-before: Watch for the distinction between completing deployment operations and confirming live application behavior. The endpoint examples illustrate quick smoke checks, not comprehensive testing. | bridge-after: The clip explains why smoke checks matter, but omits supplied-action execution, deployed-revision verification, and Lambda job-result reporting. The text covers those steps, including blocking progression on failure.
  - 90auAVyZswc 1111-1200s facts=['f1'] label: Why deployment success still needs a live-service smoke check | summary: A successful deployment operation does not prove that the application works. Files can be copied and the application started, yet a configuration error or broken database connection can prevent useful behavior. Smoke checks test basic functionality immediately after deployment. Examples include reaching the home page with an HTTP 200 response, signing in with test credentials, and reaching a health endpoint. These checks are deliberately simple and fast—roughly one or two minutes—not comprehensive application testing.

### s03 · check · Review smoke-check reporting
Check your understanding — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] A supplied Lambda smoke check fails. Which job-result reporting path preserves the release gate?
  ✔ a: Call PutJobFailureResult and leave dependent progression blocked.
      why: Correct. Call PutJobFailureResult and leave dependent progression blocked.
  ✘ b: Call PutJobSuccessResult because the deployment operation completed.
      why: Deployment completion does not justify success when live validation fails.
  ✘ c: Call PutJobSuccessResult now and check live behavior afterward.
      why: A passing smoke check must precede PutJobSuccessResult with the job ID.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The action checks the supplied endpoint against the expected response for the deployed revision. A passing check calls PutJobSuccessResult with the job ID; a failing check calls PutJobFailureResult and leaves dependent progression blocked.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r01
  MEASURES: A:report_smoke_check_outcome_to_gate_release_completion(f3)   anchors=['assessment:report_smoke_check_outcome_to_gate_release_completion']
  taught-before-tested: A.f3←s01

### s04 · hands_on · Review smoke-check reporting
Evidence review — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read the live smoke-check and reporting excerpts. Decide whether each correctly reports a failing check that blocks progression or a passing check that permits this gate. Compare the observed response with the expectation for the deployed revision.
  'The supplied Lambda action follows deployment and checks the supplied endpoint. Its job-result call uses the job_id below and occurs after the shown response comparison.
```text
job_id: "smoke-0"
revision: "exercise-revision"
endpoint: "exercise-service-endpoint"
deployment_status: "completed"
expected_response: "Supplied expected response for exercise-revision"
observed_response: "does not match"
job_result_call: "PutJobFailureResult"
dependent_progression: "blocked"
```' -> Failing live check: PutJobFailureResult and blocked progression  (column observed_response, role=categorical)
      feedback: Judgement: Failing live check: PutJobFailureResult and blocked progression. Compare the stated evidence with the required criterion.
  'The supplied Lambda action follows deployment and checks the supplied endpoint. Its job-result call uses the job_id below and occurs after the shown response comparison.
```text
job_id: "smoke-1"
revision: "exercise-revision"
endpoint: "exercise-service-endpoint"
deployment_status: "completed"
expected_response: "Supplied expected response for exercise-revision"
observed_response: "matches"
job_result_call: "PutJobSuccessResult"
dependent_progression: "permitted by this gate"
```' -> Passing live check: PutJobSuccessResult with job ID  (column observed_response, role=categorical)
      feedback: Judgement: Passing live check: PutJobSuccessResult with job ID. Compare the stated evidence with the required criterion.
  'Alternate implementation: deployment completed; the endpoint response does not match the expected deployed-revision response; action nevertheless calls PutJobSuccessResult.' -> Incorrect success reporting
      feedback: Judgement: Incorrect success reporting. Compare the stated evidence with the required criterion.
  feedback✔: Correct. Your judgement follows the supplied evidence and the stated requirement.  feedback✘: Compare the evidence with the requirement rather than inferring success from a partial signal. The action checks the supplied endpoint against the expected response for the deployed revision. A passing check calls PutJobSuccessResult with the job ID; a failing check calls PutJobFailureResult and leaves dependent progression blocked.  hints: ['Separate the observed outcome from what was merely intended.', 'Check every required condition, not just the most reassuring field.']  remediation→r02
  MEASURES: A:verify_deployed_revision_behavior_from_smoke_check_evidence(f1,f2)   anchors=['practice', 'assessment:verify_deployed_revision_behavior_from_smoke_check_evidence']
  taught-before-tested: A.f1←s01; A.f2←s01

### s05 · recap · Keep these distinctions
(takeaway) Validate live behavior for the deployed revision. Report job success only after a pass; report failure to block dependent progression. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Handle failed event delivery with bounded retries and failure capture: Next: Handle failed event delivery with bounded retries and failure capture.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the evidence
(mechanism) In the supplied Lambda validation action, call PutJobSuccessResult with the job ID only after a passing check. On failure, call PutJobFailureResult so dependent progression remains blocked. Retain revision, endpoint result and job outcome together. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) A completed deployment can still have a failing smoke response. Compare behavior for the intended revision before selecting the job-result reporting path. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.smoke_checks cols=['job_id', 'revision', 'endpoint', 'deployment_status', 'expected_response', 'observed_response', 'job_result_call', 'dependent_progression'] ] caption: 
### r02 · Separate the evidence
(mechanism) Deployment completion is not a live behavior check. Run the supplied smoke-check action against the deployed endpoint and compare its response with the expectation for the deployed revision. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) A completed deployment can still have a failing smoke response. Compare behavior for the intended revision before selecting the job-result reporting path. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.smoke_checks cols=['job_id', 'revision', 'endpoint', 'deployment_status', 'expected_response', 'observed_response', 'job_result_call', 'dependent_progression'] ] caption: 