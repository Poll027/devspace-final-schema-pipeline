# EVALUATOR PACKET — Bound retries and verify capture (aws_devops.tile.117)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.handle_failed_event_delivery_with_bounded_retries_and_failure_capture — Handle failed event delivery with bounded retries and failure capture

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.handle_failed_event_delivery_with_bounded_retries_and_failure_capture)   objective: Handle failed event delivery
A.f1: EventBridge retries retryable target-delivery failures within configured maximum event age and retry-attempt limits.   [sources: aws_eventbridge_user_guide#eb-rule-retry-policy.html]
A.f2: Configure the target RetryPolicy MaximumRetryAttempts and MaximumEventAgeInSeconds to the approved finite budget.   [sources: aws_eventbridge_user_guide#eb-rule-retry-policy.html]
A.f3: Configure DeadLetterConfig with the approved SQS queue ARN and required queue permissions, then inspect a seeded exhausted delivery failure in that queue.   [sources: aws_eventbridge_user_guide#eb-rule-dlq.html]
A.f4: Some nonretryable delivery failures go directly to failure capture; retry configuration does not guarantee every failure receives retries.   [sources: aws_eventbridge_user_guide#eb-rule-dlq.html]
note: Use supplied finite limits and SQS queue; do not invent retry intervals or guaranteed retry causes.
PRACTICE ANCHOR (tool_simulation): Configure one supplied EventBridge target with the approved MaximumRetryAttempts and MaximumEventAgeInSeconds values, then configure DeadLetterConfig with the approved SQS queue ARN and required queue permissions. Inspect the seeded exhausted delivery failure in that queue.  SUCCESS: The target's retry policy matches both approved finite limits, and its dead-letter configuration and queue permissions allow failure capture. The seeded exhausted event is inspectable in the approved queue, and the supplied delivery evidence is consistent with the configured retry budget.
ASSESSMENT ANCHOR: verify_retryable_delivery_is_bounded_by_age_and_attempt_limits facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_queue_permissions_and_inspect_captured_exhausted_event facts=['f3']
ASSESSMENT ANCHOR: distinguish_direct_failure_capture_from_retry_exhaustion facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Control environment promotion with a manual approval; Document incident evidence and a preventive change using reused systematic-debugging coverage; Endpoint cutover; Perform a controlled ECS service rollout; Promote the same artifact version across environments; Recover an incident safely using an established runbook; Residual charge verification; State access isolation; State locking; Verify restored service and data against RTO/RPO in an isolated rehearsal

## LESSON, in learner order

### s01 · explainer · Bound retries and verify capture
Learn — 
(definition) EventBridge retries retryable target-delivery failures within two configured limits: maximum event age and retry attempts. ⟦A.f1 A:tb2⟧
(mechanism) Set RetryPolicy MaximumRetryAttempts and MaximumEventAgeInSeconds to the approved finite budget. Set DeadLetterConfig to the approved SQS queue ARN, with required queue permissions, and inspect the seeded exhausted failure there. Some nonretryable failures go directly to capture; not every failure receives retries. ⟦A.f2 A.f3 A.f4 A:tb3⟧
[PROCESS_FLOW] nodes=['Delivery failure', 'Finite age + attempt limits', 'Approved SQS capture', 'Permissions + event inspection'] edges=[('failure', 'retry', 'Retryable'), ('retry', 'capture', 'Exhausted'), ('failure', 'capture', 'Some nonretryable failures'), ('capture', 'inspect', None)] alt: Retryable delivery is bounded by event age and attempts before exhaustion reaches capture. Some nonretryable failures go directly to capture. Verify queue permissions and inspect the captured event.

### s02 · explainer · Read the evidence, not the shortcut
Learn — 
(example) Review both finite limits and the capture route. A retry count alone does not prove the approved queue can accept the failed event. Check its permissions and inspect the seeded exhausted-delivery event in that queue. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) Contrast retry exhaustion with direct capture. A retryable failure is interpreted against the age and attempt limits; some nonretryable failures reach capture without a full retry history. Both need inspectable capture evidence. An ARN in the configuration is not a substitute for checking the captured event. ⟦A.f1 A.f4 A.f3 A:tb4 A:tb5⟧

### s03 · check · Does capture require retries?
Check — Read the supplied question and choose the conclusion supported by the evidence.
QUESTION [choice, intro, grading=client] A captured nonretryable delivery failure has no full retry history. Which conclusion follows?
  ✔ o1: Some nonretryable failures go directly to capture; the missing retry history alone does not contradict the policy.
      why: Some nonretryable failures go directly to failure capture.
  ✘ o2: Every delivery failure must consume the full retry budget before capture.
      why: The retry budget does not guarantee retries for every failure.
  ✘ o3: Capture without retries proves the configured attempt limit was ignored.
      why: Direct capture of some nonretryable failures is compatible with the policy.
  feedback✔: Your judgement follows the supplied evidence and the required checks.  feedback✘: Recheck the evidence against each required criterion; a partial check is not enough.  hints: ['Check the retry branch separately from the capture evidence.']  remediation→r01
  MEASURES: A:distinguish_direct_failure_capture_from_retry_exhaustion(f4)   anchors=['assessment:distinguish_direct_failure_capture_from_retry_exhaustion']
  taught-before-tested: A.f4←s01

### s04 · hands_on · Review bound retries and verify capture
Review evidence — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Decide whether each supplied EventBridge review record verifies the bounded retry policy and failure capture together. The approved limits and queue below are supplied review criteria, not AWS defaults.
  'RetryPolicy.MaximumRetryAttempts = approved finite attempt limit
RetryPolicy.MaximumEventAgeInSeconds = approved finite age limit
DeadLetterConfig.Arn = approved SQS queue ARN
Queue permissions: required permissions present
Seeded retryable delivery: exhausted within the configured budget; failed event inspected in that queue' -> Meets every supplied verification criterion
      feedback: Both finite limits, the permitted capture route and the seeded exhausted event are verified.
  'RetryPolicy.MaximumRetryAttempts = approved finite attempt limit
RetryPolicy.MaximumEventAgeInSeconds = approved finite age limit
DeadLetterConfig.Arn = approved SQS queue ARN
Queue permissions: not checked
Seeded exhausted event: not inspected
Review conclusion: capture is verified from the ARN alone' -> Does not meet every supplied verification criterion
      feedback: The ARN alone does not verify queue permissions or the captured exhausted event.
  'RetryPolicy: both approved finite limits match
DeadLetterConfig and required queue permissions: verified
Seeded exhausted retryable event: inspected, consistent with the finite budget
Additional failure: nonretryable, inspected in the approved queue without full retry history
Review conclusion: direct capture is consistent with the supplied nonretryable case' -> Meets every supplied verification criterion
      feedback: The exhausted event verifies the budget and capture; direct capture can occur for some nonretryable failures.
  'RetryPolicy.MaximumRetryAttempts = approved finite attempt limit
RetryPolicy.MaximumEventAgeInSeconds = different from approved finite age limit
Queue permissions and captured exhausted event: verified
Review conclusion: the approved retry policy is satisfied' -> Does not meet every supplied verification criterion
      feedback: Both age and attempt limits must match the approved finite budget.
  feedback✔: Your judgement follows the supplied evidence and the required checks.  feedback✘: Recheck the evidence against each required criterion; a partial check is not enough.  hints: ['Check the retry branch separately from the capture evidence.']  remediation→r02
  MEASURES: A:verify_retryable_delivery_is_bounded_by_age_and_attempt_limits(f1,f2); A:verify_queue_permissions_and_inspect_captured_exhausted_event(f3); A:distinguish_direct_failure_capture_from_retry_exhaustion(f4)   anchors=['practice', 'assessment:verify_retryable_delivery_is_bounded_by_age_and_attempt_limits', 'assessment:verify_queue_permissions_and_inspect_captured_exhausted_event', 'assessment:distinguish_direct_failure_capture_from_retry_exhaustion']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f4←s01

### s05 · recap · Keep these distinctions
Takeaways — 
(takeaway) Bound retries by both age and attempts. Verify queue permissions and inspect the captured failure. Some nonretryable failures go directly to capture without a full retry history. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Observe the ECS rollout: An ECS service needs a new image revision without treating the update request as proof of a healthy rollout.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: bound retries and verify capture
(definition) Some nonretryable delivery failures go directly to failure capture; retry configuration does not guarantee every failure receives retries. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast a retryable failure exhausting finite limits with a nonretryable failure that can go directly to capture. A full retry history is not required for every captured failure. ⟦A.f1 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Review: bound retries and verify capture
(definition) EventBridge retries retryable target-delivery failures within configured maximum event age and retry-attempt limits. Configure the target RetryPolicy MaximumRetryAttempts and MaximumEventAgeInSeconds to the approved finite budget. Configure DeadLetterConfig with the approved SQS queue ARN and required queue permissions, then inspect a seeded exhausted delivery failure in that queue. Some nonretryable delivery failures go directly to failure capture; retry configuration does not guarantee every failure receives retries. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast a retryable failure exhausting finite limits with a nonretryable failure that can go directly to capture. A full retry history is not required for every captured failure. ⟦A.f1 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Observe the ECS rollout (aws_devops.tile.118)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.perform_a_controlled_ecs_service_rollout — Perform a controlled ECS service rollout

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.perform_a_controlled_ecs_service_rollout)   objective: Perform an ECS service rollout
A.f1: An ECS rolling deployment replaces service tasks according to minimumHealthyPercent and maximumPercent relative to desiredCount.   [sources: aws_ecs_developer_guide#deployment-type-ecs.html]
A.f2: Register the supplied new image version in a task-definition revision and update the service to that revision.   [sources: aws_ecs_developer_guide#deployment-type-ecs.html]
A.f3: Inspect service events, running task revisions and health until the supplied steady-state criteria are met; a service-update request alone is not proof of a healthy rollout.   [sources: aws_ecs_developer_guide#deployment-type-ecs.html]
note: Use supplied task definition and steady-state checks; do not add load-driven ECS scaling.
PRACTICE ANCHOR (tool_simulation): Roll one supplied ECS service from image version A to B by registering a task-definition revision and updating the service, then verify task health against the supplied steady-state criteria.  SUCCESS: The service uses the registered version B task-definition revision. Observed task replacement is consistent with the supplied minimumHealthyPercent and maximumPercent relative to desiredCount, and service events, running task revisions and health satisfy every supplied steady-state criterion.
ASSESSMENT ANCHOR: interpret_task_replacement_bounds_relative_to_desired_count facts=['f1']
ASSESSMENT ANCHOR: verify_service_task_replacement_and_steady_state_health facts=['f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Control environment promotion with a manual approval; Document incident evidence and a preventive change using reused systematic-debugging coverage; Endpoint cutover; Promote the same artifact version across environments; Recover an incident safely using an established runbook; Residual charge verification; State access isolation; State locking; Verify restored service and data against RTO/RPO in an isolated rehearsal

## LESSON, in learner order

### s01 · explainer · Observe the ECS rollout
Learn — 
(definition) An ECS rolling deployment replaces service tasks within minimumHealthyPercent and maximumPercent bounds relative to desiredCount. These settings do not mean every update replaces all tasks at once. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) Register the supplied new image version in a task-definition revision, then update the service to that revision. Follow service events, running task revisions and health until the supplied steady-state criteria pass. ⟦A.f2 A.f3 A:tb3 A:tb4⟧
(misconception) An accepted service-update request is not evidence of a healthy rollout. Keep the replacement settings alongside the observed events, revisions and health; completion depends on the supplied steady-state checks, not the request. ⟦A.f3 A:tb5⟧
[DIAGRAM: Schematic ECS rollout review] nodes=['Service settings: desiredCount; minimumHealthyPercent; maximumPercent', 'Register supplied image version B in a task-definition revision', 'Service updated to selected revision', 'During replacement: inspect service events, running revisions and health', 'Verified steady state: supplied criteria pass'] edges=[('n1', 'n4', 'Replacement bounds'), ('n2', 'n3', 'Select revision'), ('n3', 'n4', 'Observe'), ('n4', 'n5', 'Verify')] alt: Service settings: desiredCount; minimumHealthyPercent; maximumPercent → Register supplied image version B in a task-definition revision → Service updated to selected revision → During replacement: inspect service events, running revisions and health → Verified steady state: supplied criteria pass

### s02 · check · Is the rollout verified?
Check — Read the supplied question and choose the conclusion supported by the evidence.
QUESTION [choice, intro, grading=client] An ECS service-update request has been accepted. What evidence is still needed to establish a healthy rollout?
  ✘ o1: Only the acceptance of the update request.
      why: An update request alone does not prove a healthy rollout.
  ✔ o2: Service events, running task revisions and health meeting the supplied steady-state criteria.
      why: The rollout is verified against service events, revisions and health.
  ✘ o3: Only registration of a new task-definition revision.
      why: Registration does not establish that running tasks and health meet the criteria.
  feedback✔: Your judgement follows the supplied evidence and the required checks.  feedback✘: Recheck the evidence against each required criterion; a partial check is not enough.  hints: ['Separate a requested revision from observed steady state.']  remediation→r01
  MEASURES: A:verify_service_task_replacement_and_steady_state_health(f2,f3)   anchors=['assessment:verify_service_task_replacement_and_steady_state_health']
  taught-before-tested: A.f2←s01; A.f3←s01

### s03 · hands_on · Review observe the ecs rollout
Review evidence — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, core, grading=client] Read each ECS rollout record and decide whether it establishes every supplied rollout criterion. Criteria: version B registered in a task-definition revision and used by the service; replacement consistent with the supplied minimumHealthyPercent and maximumPercent relative to desiredCount; events, running revisions and health meeting supplied steady state.
  'Task-definition revision: registered with image version B
Service target: registered B revision
Replacement observation: consistent with both supplied percentage bounds relative to desiredCount
Service events: satisfy supplied steady-state checks
Running task revisions: all supplied required B revisions
Health: all supplied required checks pass' -> Meets every supplied verification criterion
      feedback: The revision, replacement bounds and all steady-state evidence are present.
  'Task-definition revision: registered with image version B
Service-update request: accepted
Running tasks: still include version A revision
Health and service events: not checked
Review conclusion: rollout healthy' -> Does not meet every supplied verification criterion
      feedback: Acceptance alone does not establish running B revisions or health and events.
  'Task-definition revision and service: version B
Service events, running revisions and health: meet supplied steady-state checks
Replacement observation: outside the supplied maximumPercent bound relative to desiredCount' -> Does not meet every supplied verification criterion
      feedback: Task replacement must also be consistent with the supplied percentage bounds.
  feedback✔: Your judgement follows the supplied evidence and the required checks.  feedback✘: Recheck the evidence against each required criterion; a partial check is not enough.  hints: ['Separate a requested revision from observed steady state.']  remediation→r02
  MEASURES: A:interpret_task_replacement_bounds_relative_to_desired_count(f1); A:verify_service_task_replacement_and_steady_state_health(f2,f3)   anchors=['practice', 'assessment:interpret_task_replacement_bounds_relative_to_desired_count', 'assessment:verify_service_task_replacement_and_steady_state_health']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s04 · recap · Keep these distinctions
Takeaways — 
(takeaway) Replacement percentage bounds are relative to desiredCount. Register the new image revision and update the service, then verify events, running revisions and health against the supplied steady-state criteria. Update acceptance alone is not completion. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Promote one built artifact: A staging-tested release should promote the same built content to the next environment.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: observe the ecs rollout
(definition) Register the supplied new image version in a task-definition revision and update the service to that revision. Inspect service events, running task revisions and health until the supplied steady-state criteria are met; a service-update request alone is not proof of a healthy rollout. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast an accepted update request with verified steady state: only the latter checks service events, running revisions and health. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Review: observe the ecs rollout
(definition) An ECS rolling deployment replaces service tasks according to minimumHealthyPercent and maximumPercent relative to desiredCount. Register the supplied new image version in a task-definition revision and update the service to that revision. Inspect service events, running task revisions and health until the supplied steady-state criteria are met; a service-update request alone is not proof of a healthy rollout. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast an accepted update request with verified steady state: only the latter checks service events, running revisions and health. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Promote one built artifact (aws_devops.tile.119)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.promote_the_same_artifact_version_across_environments — Promote the same artifact version across environments

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.promote_the_same_artifact_version_across_environments)   objective: Promote the same artifact version across environments
A.f1: The build stage produces a build artifact; release combines that build with environment configuration, and run executes the release.   [sources: twelve_factor_app#build-release-run]
A.f2: Promote the same immutable artifact reference or digest to the next environment while supplying that environment’s configuration rather than rebuilding the source.   [sources: twelve_factor_app#build-release-run]
A.f3: Compare the deployed artifact digests in staging and production and their recorded build provenance to verify the tested output is the promoted output.   [sources: github_actions_docs#how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations]
note: Use supplied artifact and environment configuration; do not create a new build during promotion.
PRACTICE ANCHOR (tool_simulation): Promote the supplied staging artifact to production by retaining its immutable reference or digest and selecting the supplied production configuration, without creating a new build.  SUCCESS: Production uses the supplied production configuration and the same immutable artifact as staging. The deployed staging and production digests match, their recorded build provenance identifies the same build output, and no rebuild occurs.
ASSESSMENT ANCHOR: verify_staging_and_production_artifact_digests_and_build_provenance facts=['f2', 'f3']

## DATA ASSETS USED
ds.artifact_promotion: One build, two environment releases — columns: environment(categorical), immutable_artifact_reference(identifier), deployed_digest(identifier), recorded_build_provenance(identifier), environment_configuration(identifier), new_build_during_promotion(categorical)
   ["staging","artifact.release_b","sha256:97f4fc040deddaef2d33f1e142149274124cc08997822942866bf6674a57c17d","build.release_b","config.staging",false]
   ["production","artifact.release_b","sha256:97f4fc040deddaef2d33f1e142149274124cc08997822942866bf6674a57c17d","build.release_b","config.production",false]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Control environment promotion with a manual approval; Document incident evidence and a preventive change using reused systematic-debugging coverage; Endpoint cutover; Recover an incident safely using an established runbook; Residual charge verification; State access isolation; State locking; Verify restored service and data against RTO/RPO in an isolated rehearsal

## LESSON, in learner order

### s01 · explainer · Promote one built artifact
Learn — 
(definition) Build produces an artifact. Release combines that build with environment configuration, and run executes the release. A staging-tested output should remain the same built content when promoted. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) Carry the same immutable artifact reference or digest from staging to production, supplying production configuration rather than rebuilding the source. Compare deployed digests and recorded build provenance in both environments to verify that the tested output is the promoted output. ⟦A.f2 A.f3 A:tb3 A:tb4⟧
(misconception) The registered comparison keeps one artifact and build provenance across staging and production while configuration differs. Rebuilding from the same source is not this same-artifact check. Different deployed digests do not show that the tested output was promoted. ⟦A.f2 A.f3 A:tb5⟧
[TABLE ds.artifact_promotion cols=['environment', 'immutable_artifact_reference', 'deployed_digest', 'recorded_build_provenance', 'environment_configuration', 'new_build_during_promotion'] ] caption: One build, two environment releases

### s02 · check · Is the tested artifact unchanged?
Check — Read the supplied question and choose the conclusion supported by the evidence.
QUESTION [choice, intro, grading=client] Which comparison verifies that production received the tested staging build output?
  ✘ o1: The environment names are different.
      why: Environment names do not identify the deployed build output.
  ✘ o2: The source was rebuilt separately for production.
      why: Promotion retains the immutable output rather than rebuilding it.
  ✔ o3: The deployed digests match and recorded provenance identifies the same build output.
      why: Matching deployed digests and provenance verify the tested output was promoted.
  feedback✔: Your judgement follows the supplied evidence and the required checks.  feedback✘: Recheck the evidence against each required criterion; a partial check is not enough.  hints: ['Trace the output identity separately from environment configuration.']  remediation→r01
  MEASURES: A:verify_staging_and_production_artifact_digests_and_build_provenance(f2,f3)   anchors=['assessment:verify_staging_and_production_artifact_digests_and_build_provenance']
  taught-before-tested: A.f2←s01; A.f3←s01

### s03 · hands_on · Review promote one built artifact
Review evidence — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each promotion record. Decide whether production retains the tested immutable staging output and its provenance, uses supplied production configuration, and avoids rebuilding.
  'staging: {"deployed_digest": "sha256:97f4fc040deddaef2d33f1e142149274124cc08997822942866bf6674a57c17d", "environment_configuration": "config.staging", "immutable_artifact_reference": "artifact.release_b", "new_build_during_promotion": false, "recorded_build_provenance": "build.release_b"}
production: {"deployed_digest": "sha256:97f4fc040deddaef2d33f1e142149274124cc08997822942866bf6674a57c17d", "environment_configuration": "config.production", "immutable_artifact_reference": "artifact.release_b", "new_build_during_promotion": false, "recorded_build_provenance": "build.release_b"}' -> Meets every supplied verification criterion
      feedback: The deployed digest, immutable reference and build provenance match; production uses its configuration and no new build occurs.
  'staging: {"deployed_digest": "sha256:97f4fc040deddaef2d33f1e142149274124cc08997822942866bf6674a57c17d", "environment_configuration": "config.staging", "immutable_artifact_reference": "artifact.release_b", "new_build_during_promotion": false, "recorded_build_provenance": "build.release_b"}
production: {"deployed_digest": "sha256:97f4fc040deddaef2d33f1e142149274124cc08997822942866bf6674a57c17d", "environment_configuration": "config.production", "immutable_artifact_reference": "artifact.release_b", "new_build_during_promotion": true, "recorded_build_provenance": "build.release_b"}' -> Does not meet every supplied verification criterion
      feedback: Creating a new build during promotion violates the no-rebuild criterion, even if recorded digests match.
  'staging: {"deployed_digest": "sha256:97f4fc040deddaef2d33f1e142149274124cc08997822942866bf6674a57c17d", "environment_configuration": "config.staging", "immutable_artifact_reference": "artifact.release_b", "new_build_during_promotion": false, "recorded_build_provenance": "build.release_b"}
production: {"deployed_digest": "sha256:97f4fc040deddaef2d33f1e142149274124cc08997822942866bf6674a57c17d", "environment_configuration": "config.staging", "immutable_artifact_reference": "artifact.release_b", "new_build_during_promotion": false, "recorded_build_provenance": "build.release_b"}' -> Does not meet every supplied verification criterion
      feedback: Production must use its supplied environment configuration, even when the artifact matches.
  feedback✔: Your judgement follows the supplied evidence and the required checks.  feedback✘: Recheck the evidence against each required criterion; a partial check is not enough.  hints: ['Trace the output identity separately from environment configuration.']  remediation→r02
  MEASURES: A:verify_staging_and_production_artifact_digests_and_build_provenance(f2,f3)   anchors=['practice', 'assessment:verify_staging_and_production_artifact_digests_and_build_provenance']
  taught-before-tested: A.f2←s01; A.f3←s01

### s04 · recap · Keep these distinctions
Takeaways — 
(takeaway) Build once; release combines that artifact with environment configuration. Promote the same immutable reference or digest, not a rebuild. Compare deployed digests and build provenance across staging and production. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Separate usage time from report time: Teardown removed resources, but the bill still needs a time-aware check.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: promote one built artifact
(definition) Promote the same immutable artifact reference or digest to the next environment while supplying that environment’s configuration rather than rebuilding the source. Compare the deployed artifact digests in staging and production and their recorded build provenance to verify the tested output is the promoted output. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast one promoted build with a rebuild from the same source. Compare deployed digests and provenance, not merely source identity. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.artifact_promotion cols=['environment', 'immutable_artifact_reference', 'deployed_digest', 'recorded_build_provenance', 'environment_configuration', 'new_build_during_promotion'] ] caption: One build, two environment releases
### r02 · Review: promote one built artifact
(definition) Promote the same immutable artifact reference or digest to the next environment while supplying that environment’s configuration rather than rebuilding the source. Compare the deployed artifact digests in staging and production and their recorded build provenance to verify the tested output is the promoted output. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast one promoted build with a rebuild from the same source. Compare deployed digests and provenance, not merely source identity. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.artifact_promotion cols=['environment', 'immutable_artifact_reference', 'deployed_digest', 'recorded_build_provenance', 'environment_configuration', 'new_build_during_promotion'] ] caption: One build, two environment releases

=========

# EVALUATOR PACKET — Separate usage time from report time (aws_devops.tile.120)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = cost.residual_charge_verification — Residual charge verification

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (cost.residual_charge_verification)   objective: Verify residual charges after teardown
A.f1: Cost Explorer data is refreshed at least once every 24 hours and some data can take longer to appear.   [sources: aws_cost_management_user_guide#ce-what-is.html]
A.f2: Inspect the supplied teardown interval with account and service or usage-type filters and compare usage timestamps with resource-deletion evidence.   [sources: aws_cost_management_user_guide#ce-filtering.html]
A.f3: Distinguish charges for usage before deletion from evidence of continuing usage and repeat the check after the billing data refresh rather than declaring zero cost from resource absence.   [sources: aws_cost_management_user_guide#ce-what-is.html]
note: Preserve at-least-daily refresh and possible longer appearance delay; do not promise a fixed final billing time.
PRACTICE ANCHOR (tool_simulation): Inspect supplied Cost Explorer usage and cost data for one teardown window using account and service or usage-type filters. Compare usage timestamps with supplied resource-deletion evidence, and repeat the inspection using a supplied refreshed report.  SUCCESS: The inspection uses the supplied interval and relevant filters, distinguishes pre-deletion usage charges from evidence of continuing usage after deletion, and records any empty initial result as provisional. The conclusion incorporates the refreshed report and acknowledges that Cost Explorer refreshes at least once every 24 hours while some data can take longer to appear.
ASSESSMENT ANCHOR: identify_continuing_billed_usage_after_deletion facts=['f2', 'f3']
ASSESSMENT ANCHOR: account_for_billing_data_delay_in_teardown_verification facts=['f1', 'f3']

## DATA ASSETS USED
ds.residual_charge_reports: Initial and refreshed teardown reports — columns: report_state(categorical), reported_at(datetime), teardown_interval_start(datetime), teardown_interval_end(datetime), account(identifier), service(categorical), resource(identifier), usage_timestamp(datetime), cost(numerical), deleted_at(datetime), deletion_evidence(text), report_result(text)
   ["initial","2026-01-12T12:00:00Z","2026-01-12T09:00:00Z","2026-01-12T12:00:00Z","account.exercise","Amazon ECS","service.exercise",null,null,"2026-01-12T10:00:00Z","Deletion recorded for service.exercise","No matching usage row in current extract; provisional"]
   ["refreshed","2026-01-14T12:00:00Z","2026-01-12T09:00:00Z","2026-01-12T12:00:00Z","account.exercise","Amazon ECS","service.exercise","2026-01-12T09:30:00Z",0.25,"2026-01-12T10:00:00Z","Deletion recorded for service.exercise","Usage before deletion appeared in refreshed extract; not proof of continui

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Control environment promotion with a manual approval; Document incident evidence and a preventive change using reused systematic-debugging coverage; Endpoint cutover; Recover an incident safely using an established runbook; State access isolation; State locking; Verify restored service and data against RTO/RPO in an isolated rehearsal

## LESSON, in learner order

### s01 · explainer · Separate usage time from report time
Learn — 
(definition) Deleted resources do not establish zero cost. Cost Explorer refreshes at least once every 24 hours; some data can take longer to appear. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) Filter the supplied teardown interval by account and service or usage type. Compare usage timestamps with deletion evidence. Distinguish pre-deletion charges from continuing usage, then repeat after billing-data refresh rather than concluding from resource absence. ⟦A.f2 A.f3 A:tb3⟧
[TABLE ds.residual_charge_reports cols=['report_state', 'reported_at', 'teardown_interval_start', 'teardown_interval_end', 'account', 'service', 'resource', 'usage_timestamp', 'cost', 'deleted_at', 'deletion_evidence', 'report_result'] ] caption: Initial and refreshed teardown reports

### s02 · explainer · Read the evidence, not the shortcut
Learn — 
(example) In the registered initial and refreshed reports, use the same teardown interval and account/service filter. The initial extract has no matching usage row: retain that as a provisional reporting observation, not measured zero usage. The refreshed extract adds a charge for usage before deletion. Its appearance in a later report is not proof of continuing usage. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) Compare when usage occurred with the deletion evidence, not merely when the report was opened. Repeat after refresh, remembering that some data can appear later. Neither an early empty report nor resource absence proves zero cost; a later charge is not automatically post-deletion usage. This is a timing check, not a new price estimate. ⟦A.f1 A.f3 A:tb4 A:tb5⟧

### s03 · check · What does the report timing prove?
Check — Read the supplied question and choose the conclusion supported by the evidence.
QUESTION [choice, intro, grading=client] The initial filtered Cost Explorer extract is empty after teardown. What conclusion is justified?
  ✔ o1: The result is provisional; repeat the inspection after refresh and compare usage timestamps with deletion evidence.
      why: Cost Explorer refreshes at least once every 24 hours, and some data takes longer to appear.
  ✘ o2: An empty extract proves there are no charges for the interval.
      why: An initial empty result is not final billing evidence.
  ✘ o3: Resource absence proves that all previously incurred usage charges are gone.
      why: Pre-deletion usage can still appear in refreshed data; resource absence does not prove zero cost.
  feedback✔: Your judgement follows the supplied evidence and the required checks.  feedback✘: Recheck the evidence against each required criterion; a partial check is not enough.  hints: ['Compare report timing and usage timing with deletion evidence.']  remediation→r01
  MEASURES: A:account_for_billing_data_delay_in_teardown_verification(f1,f3)   anchors=['assessment:account_for_billing_data_delay_in_teardown_verification']
  taught-before-tested: A.f1←s01; A.f3←s01

### s04 · hands_on · Review separate usage time from report time
Review evidence — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each teardown inspection note with the supplied initial and refreshed records. Decide whether its conclusion uses the supplied interval, account and service filters, compares usage with deletion evidence and treats initial emptiness as provisional. Cost Explorer refreshes at least once every 24 hours; some data may take longer.

{"account": "account.exercise", "cost": null, "deleted_at": "2026-01-12T10:00:00Z", "deletion_evidence": "Deletion recorded for service.exercise", "report_result": "No matching usage row in current extract; provisional", "report_state": "initial", "reported_at": "2026-01-12T12:00:00Z", "resource": "service.exercise", "service": "Amazon ECS", "teardown_interval_end": "2026-01-12T12:00:00Z", "teardown_interval_start": "2026-01-12T09:00:00Z", "usage_timestamp": null}
{"account": "account.exercise", "cost": 0.25, "deleted_at": "2026-01-12T10:00:00Z", "deletion_evidence": "Deletion recorded for service.exercise", "report_result": "Usage before deletion appeared in refreshed extract; not proof of continuing usage", "report_state": "refreshed", "reported_at": "2026-01-14T12:00:00Z", "resource": "service.exercise", "service": "Amazon ECS", "teardown_interval_end": "2026-01-12T12:00:00Z", "teardown_interval_start": "2026-01-12T09:00:00Z", "usage_timestamp": "2026-01-12T09:30:00Z"}
  'Inspection: supplied interval, account and service filters used
Initial empty result: provisional
Refreshed extract: inspected
Usage timestamp: before the recorded deletion
Conclusion: refreshed charge reflects pre-deletion usage, not proof of continuing usage; refresh timing and possible longer appearance acknowledged' -> Meets every supplied verification criterion
      feedback: The conclusion uses both reports and timestamp evidence, without equating an initial empty result with zero cost.
  'Inspection: supplied interval, account and service filters used
Initial result: empty
Refreshed extract: ignored
Conclusion: no cost for the teardown window because the resource is absent' -> Does not meet every supplied verification criterion
      feedback: Resource absence and an initial empty result do not establish zero cost; the refreshed report must be incorporated.
  'Inspection: supplied interval and relevant filters used; both reports inspected
Refreshed usage timestamp: before deletion
Conclusion: the charge proves continuing usage after deletion' -> Does not meet every supplied verification criterion
      feedback: A pre-deletion usage timestamp is not evidence of continuing post-deletion usage.
  'Inspection: different account and outside supplied teardown interval
Conclusion: empty extract proves no charges for the supplied teardown' -> Does not meet every supplied verification criterion
      feedback: An extract outside the supplied interval and account does not answer the requested inspection.
  feedback✔: Your judgement follows the supplied evidence and the required checks.  feedback✘: Recheck the evidence against each required criterion; a partial check is not enough.  hints: ['Compare report timing and usage timing with deletion evidence.']  remediation→r02
  MEASURES: A:identify_continuing_billed_usage_after_deletion(f2,f3); A:account_for_billing_data_delay_in_teardown_verification(f1,f3)   anchors=['practice', 'assessment:identify_continuing_billed_usage_after_deletion', 'assessment:account_for_billing_data_delay_in_teardown_verification']
  taught-before-tested: A.f2←s01; A.f3←s01; A.f1←s01; A.f3←s01

### s05 · recap · Keep these distinctions
Takeaways — 
(takeaway) Filter the teardown interval and compare usage timestamps with deletion evidence. Reporting can lag; repeat after refresh. An early empty report does not prove zero cost, and a later charge does not automatically prove continuing usage. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Test the state access boundary: Remote Terraform state can contain sensitive values, so its reader/writer boundary needs its own access test.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: separate usage time from report time
(definition) Cost Explorer data is refreshed at least once every 24 hours and some data can take longer to appear. Distinguish charges for usage before deletion from evidence of continuing usage and repeat the check after the billing data refresh rather than declaring zero cost from resource absence. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast report appearance time with usage time. The refreshed registered row concerns usage before deletion; an early empty extract is provisional. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.residual_charge_reports cols=['report_state', 'reported_at', 'teardown_interval_start', 'teardown_interval_end', 'account', 'service', 'resource', 'usage_timestamp', 'cost', 'deleted_at', 'deletion_evidence', 'report_result'] ] caption: Initial and refreshed teardown reports
### r02 · Review: separate usage time from report time
(definition) Cost Explorer data is refreshed at least once every 24 hours and some data can take longer to appear. Inspect the supplied teardown interval with account and service or usage-type filters and compare usage timestamps with resource-deletion evidence. Distinguish charges for usage before deletion from evidence of continuing usage and repeat the check after the billing data refresh rather than declaring zero cost from resource absence. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast report appearance time with usage time. The refreshed registered row concerns usage before deletion; an early empty extract is provisional. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.residual_charge_reports cols=['report_state', 'reported_at', 'teardown_interval_start', 'teardown_interval_end', 'account', 'service', 'resource', 'usage_timestamp', 'cost', 'deleted_at', 'deletion_evidence', 'report_result'] ] caption: Initial and refreshed teardown reports

=========

# EVALUATOR PACKET — Test the state access boundary (aws_devops.tile.121)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = terraform.state_access_isolation — State access isolation

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (terraform.state_access_isolation)   objective: Isolate access to S3 Terraform state
A.f1: S3 backend access needs permissions for the selected state bucket and object key; state can contain sensitive values.   [sources: terraform_language#backend/s3, terraform_language#state/sensitive-data]
A.f2: Scope approved readers and writers to the required ListBucket prefix and GetObject/PutObject state object operations, with supplied locking permissions configured separately.   [sources: terraform_language#backend/s3]
A.f3: Initialize the supplied backend, provision the separate exercise bucket through the approved identity, and test that an unapproved identity cannot read or overwrite state.   [sources: terraform_language#backend/s3]
A.f4: State access isolation prevents unauthorized access; it is separate from the mechanism that coordinates concurrent authorized writers.   [sources: terraform_language#backend/s3]
note: Keep state content private; use supplied bucket/key/prefix permissions and approved/unapproved identities.
PRACTICE ANCHOR (live_code): Configure scoped access to the supplied S3 state bucket, prefix, and object key. Using the approved identity and supplied Terraform configuration, initialize the backend and provision one separate S3 exercise bucket. Test that the unapproved identity cannot read or overwrite state, leaving the supplied coordination configuration unchanged.  SUCCESS: Approved readers have the required prefix-scoped ListBucket and state-object GetObject access; approved writers also have state-object PutObject access. The approved provisioning identity creates the separate exercise bucket with state stored in the supplied backend. Unapproved read and overwrite attempts are denied, and recorded evidence does not expose state contents.
ASSESSMENT ANCHOR: verify_state_bucket_key_and_prefix_permission_scope facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_approved_state_access_and_unapproved_read_write_denial facts=['f2', 'f3']
ASSESSMENT ANCHOR: distinguish_state_authorization_from_authorized_writer_coordination facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Control environment promotion with a manual approval; Document incident evidence and a preventive change using reused systematic-debugging coverage; Endpoint cutover; Recover an incident safely using an established runbook; State locking; Verify restored service and data against RTO/RPO in an isolated rehearsal

## LESSON, in learner order

### s01 · explainer · Test the state access boundary
Learn — 
(definition) Remote Terraform state can contain sensitive values. S3 backend access therefore needs permissions for the selected state bucket and object key. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) Scope approved readers and writers to the required ListBucket prefix and GetObject/PutObject state-object operations. Configure supplied locking permissions separately. Initialize the intended backend and provision the separate exercise bucket through the approved identity. Test that an unapproved identity cannot read or overwrite state, retaining outcomes without exposing state contents. ⟦A.f2 A.f3 A:tb3 A:tb4⟧
(misconception) State access isolation prevents unauthorized access; a separate mechanism coordinates concurrent authorized writers. Backend initialization does not prove isolation, and locking is not the authorization boundary. Check unapproved read and overwrite attempts independently of approved provisioning. ⟦A.f4 A:tb3 A:tb5⟧
[SIDE_BY_SIDE] Authorization prevents unapproved access; locking coordinates authorized writers. left_label: State authorization boundary | right_label: Separate provisioning and coordination
  left:
[DIAGRAM] nodes=['Selected state bucket / ListBucket prefix', 'Selected state key / GetObject + PutObject', 'Approved readers and writers: scoped operations', 'Unapproved identity: verify denied read and overwrite'] edges=[('n3', 'n1', 'Scoped listing'), ('n3', 'n2', 'Scoped object access'), ('n4', 'n2', 'Denial check')] alt: Selected state bucket / ListBucket prefix → Selected state key / GetObject + PutObject → Approved readers and writers: scoped operations → Unapproved identity: verify denied read and overwrite
  right:
[DIAGRAM] nodes=['Approved identity initializes intended backend', 'Separate exercise bucket provisioned', 'Record access outcomes, not state contents', 'Supplied locking permissions configured separately'] edges=[('n1', 'n2', 'Approved provisioning'), ('n2', 'n3', 'Retain evidence')] alt: Approved identity initializes intended backend → Separate exercise bucket provisioned → Record access outcomes, not state contents → Supplied locking permissions configured separately

### s02 · check · Authorization or writer coordination?
Check — Read the supplied question and choose the conclusion supported by the evidence.
QUESTION [choice, intro, grading=client] What does denying an unapproved identity access to state establish?
  ✘ o1: It also proves that concurrent authorized writers cannot conflict.
      why: Access isolation is separate from coordination of authorized writers.
  ✔ o2: It establishes access isolation, not coordination of concurrent authorized writers.
      why: Isolation prevents unauthorized access; coordination is a separate mechanism.
  ✘ o3: It makes scoped approved-reader permissions unnecessary.
      why: Approved access still requires the selected bucket, prefix and state-object permissions.
  feedback✔: Your judgement follows the supplied evidence and the required checks.  feedback✘: Recheck the evidence against each required criterion; a partial check is not enough.  hints: ['Separate approved scopes, unapproved denials and writer coordination.']  remediation→r01
  MEASURES: A:distinguish_state_authorization_from_authorized_writer_coordination(f4)   anchors=['assessment:distinguish_state_authorization_from_authorized_writer_coordination']
  taught-before-tested: A.f4←s01

### s03 · hands_on · Review test the state access boundary
Review evidence — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read the supplied S3 state-access policy summaries and operation records. Decide whether each verifies scoped approved access, separate exercise-bucket provisioning and denial of unapproved access without disclosing state. Locking configuration is supplied separately and must remain unchanged.
  'Approved reader: ListBucket restricted to required prefix; GetObject restricted to state object
Approved writer: same scoped listing and reading plus PutObject restricted to state object
Approved provisioning identity: backend initialization succeeded; separate exercise bucket created; state stored in supplied backend
Unapproved identity: GetObject denied; overwrite PutObject denied
Evidence: status records only, no state contents
Separate coordination configuration: unchanged' -> Meets every supplied verification criterion
      feedback: Scoped approved access, provisioning, both unapproved denials and non-disclosing evidence meet the criteria.
  'Approved reader and writer: all required prefix and object scopes verified
Approved identity: backend initialized; separate exercise bucket created
Unapproved identity: state read denied; state overwrite succeeded
Evidence: status records only
Separate coordination configuration: unchanged' -> Does not meet every supplied verification criterion
      feedback: Both unapproved read and overwrite attempts must be denied.
  'Approved reader: ListBucket for every prefix; GetObject for every object in the state bucket
Approved writer: PutObject for every object in the state bucket
Backend initialization and separate exercise bucket: successful
Unapproved read and overwrite: denied
Evidence: no state contents' -> Does not meet every supplied verification criterion
      feedback: Approved permissions must be scoped to the required prefix and state object, not the whole bucket.
  'Approved permissions: required prefix-scoped ListBucket and state-object GetObject/PutObject verified
Backend initialized; separate exercise bucket provisioned through approved identity
Unapproved read and overwrite: denied
Evidence attachment: complete sensitive state contents' -> Does not meet every supplied verification criterion
      feedback: Recorded evidence must not expose state contents even when permission checks succeed.
  feedback✔: Your judgement follows the supplied evidence and the required checks.  feedback✘: Recheck the evidence against each required criterion; a partial check is not enough.  hints: ['Separate approved scopes, unapproved denials and writer coordination.']  remediation→r02
  MEASURES: A:verify_state_bucket_key_and_prefix_permission_scope(f1,f2); A:verify_approved_state_access_and_unapproved_read_write_denial(f2,f3)   anchors=['practice', 'assessment:verify_state_bucket_key_and_prefix_permission_scope', 'assessment:verify_approved_state_access_and_unapproved_read_write_denial']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f2←s01; A.f3←s01

### s04 · recap · Keep these distinctions
Takeaways — 
(takeaway) Protect the selected state bucket, prefix and object key with scoped access. Verify approved provisioning and denied unapproved read/overwrite without exposing state contents. Authorization and concurrent-writer coordination are separate checks. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Verify lock contention: Two authorized Terraform operations must not change shared state at the same time.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: test the state access boundary
(definition) State access isolation prevents unauthorized access; it is separate from the mechanism that coordinates concurrent authorized writers. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast authorization with coordination: denying unapproved read/overwrite protects access; locking coordinates authorized writers. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
### r02 · Review: test the state access boundary
(definition) S3 backend access needs permissions for the selected state bucket and object key; state can contain sensitive values. Scope approved readers and writers to the required ListBucket prefix and GetObject/PutObject state object operations, with supplied locking permissions configured separately. Initialize the supplied backend, provision the separate exercise bucket through the approved identity, and test that an unapproved identity cannot read or overwrite state. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast authorization with coordination: denying unapproved read/overwrite protects access; locking coordinates authorized writers. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Verify lock contention (aws_devops.tile.122)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = terraform.state_locking — State locking

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (terraform.state_locking)   objective: Configure locking for S3 Terraform state
A.f1: The S3 backend supports lock-file locking when use_lockfile = true; locking is opt-in.   [sources: terraform_language#backend/s3]
A.f2: Set use_lockfile = true in the supplied S3 backend configuration and use the supplied s3:GetObject, s3:PutObject and s3:DeleteObject permissions on the .tflock object.   [sources: terraform_language#backend/s3]
A.f3: During the controlled state-changing operation that holds the lock, attempt a competing operation and verify it cannot acquire the lock or change state; do not disable locking to bypass the test.   [sources: terraform_language#backend/s3, terraform_language#state/locking]
A.f4: Locking coordinates concurrent state writers; it is not an authorization boundary against identities that can directly change state objects.   [sources: terraform_language#backend/s3, terraform_language#state/locking]
A.m1 (misconception): Force-unlock is not a safe way to bypass another active state writer; it is reserved for a lock from a failed operation when automatic unlocking failed.   [sources: terraform_language#state/locking]
note: Use current S3 .tflock behavior; do not introduce obsolete mandatory DynamoDB locking or active-writer bypass.
PRACTICE ANCHOR (live_code): Enable use_lockfile = true in the supplied initialized S3 backend, using the supplied permissions for the .tflock object. Reinitialize using the supplied procedure, then use the supplied Terraform configuration to provision one separate S3 exercise bucket. With supplied synchronization holding the first state-changing operation's lock, attempt the supplied competing operation and verify that it cannot acquire the lock or change state. Do not disable locking or force-unlock the active writer.  SUCCESS: The backend has lock-file locking enabled with the supplied s3:GetObject, s3:PutObject and s3:DeleteObject permissions on .tflock. Recorded test evidence shows the competing operation failed to acquire the held lock and made no state change. The authorized first operation completes normally and provisions the separate exercise bucket.
ASSESSMENT ANCHOR: identify_configuration_and_permissions_for_s3_locking facts=['f1', 'f2']
ASSESSMENT ANCHOR: determine_whether_a_competing_state_writer_is_blocked facts=['f3']
ASSESSMENT ANCHOR: distinguish_writer_coordination_from_state_access_authorization facts=['f4']
ASSESSMENT ANCHOR: recognize_unsafe_active_writer_lock_bypasses facts=['f3', 'm1']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Control environment promotion with a manual approval; Document incident evidence and a preventive change using reused systematic-debugging coverage; Endpoint cutover; Recover an incident safely using an established runbook; Verify restored service and data against RTO/RPO in an isolated rehearsal

## LESSON, in learner order

### s01 · explainer · Verify lock contention
Learn — 
(definition) S3 lock-file locking is opt-in: enable it with use_lockfile = true. Two authorized operations must not change shared state concurrently. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) Use the supplied s3:GetObject, s3:PutObject and s3:DeleteObject permissions on the .tflock object. While the controlled state-changing operation holds the lock, attempt the competing operation. Verify it cannot acquire the lock or change state; do not disable locking to bypass contention. ⟦A.f2 A.f3 A:tb3⟧
(mental_model) Locking coordinates concurrent state writers. It does not protect against identities authorized to change state objects directly. ⟦A.f4 A:tb3⟧
[SIDE_BY_SIDE] Verify blocking without disabling locking or bypassing an active writer. left_label: Schematic: contention | right_label: Schematic: normal completion
  left:
[DIAGRAM] nodes=['Authorized terminal 1: controlled state-changing operation holds lock', '.tflock present during contention', 'Authorized terminal 2: competing operation fails lock acquisition', 'Verify competitor makes no state change'] edges=[('n1', 'n2', 'Lock held'), ('n2', 'n3', 'Contention'), ('n3', 'n4', 'Verify')] alt: Authorized terminal 1: controlled state-changing operation holds lock → .tflock present during contention → Authorized terminal 2: competing operation fails lock acquisition → Verify competitor makes no state change
  right:
[DIAGRAM] nodes=['First operation completes normally', '.tflock absent after normal completion', 'Retain contention and lock observations'] edges=[('n1', 'n2', 'Released'), ('n2', 'n3', 'Evidence')] alt: First operation completes normally → .tflock absent after normal completion → Retain contention and lock observations

### s02 · explainer · Read the evidence, not the shortcut
Learn — 
(example) Review the two authorized operations against the same state. The first holds the lock; the competing operation must fail lock acquisition and leave state unchanged. Retain the .tflock observations and contention evidence. Keep this coordination test separate from authorization tests for direct state-object access. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧
(misconception) Force-unlock has a narrow recovery role: a failed operation left a lock and automatic unlocking failed. It is not a safe bypass for another active writer. Lock-file locking remains opt-in and is not an authorization boundary; disabling it to let the second operation proceed defeats the contention test. ⟦A.m1 A.f1 A.f4 A:tb5 A:tb6⟧

### s03 · video · Observe the operating model
Observe — 
[VIDEO Enable S3 lock-file locking and verify writer contention] bridge-before: Watch for the opt-in use_lockfile setting, the temporary .tflock object, and the second terminal's lock-acquisition error. The demonstration uses different infrastructure; your supplied exercise provisions a separate S3 bucket. | bridge-after: The competing apply is blocked until the first operation finishes. The clip omits .tflock permissions and the authorization-boundary distinction; the text covers both, plus why force-unlock must not bypass an active writer.
  - AmWnWfuSTfQ 196-504s facts=['f1', 'f3'] label: Enable locking and observe a competing Terraform apply being blocked | summary: The presenter enables S3 lock-file locking with use_lockfile = true and reinitializes the backend. During an apply awaiting approval, the S3 bucket contains a .tflock object. After the operation completes, the state object remains and the lock object is gone. The demonstration then destroys and recreates its example infrastructure. While the next apply awaits approval, a second terminal attempts another apply against the same state and receives an error acquiring the state lock. Once the first operation completes, the second terminal can retry successfully and reports that the infrastructure matches the configuration. The lock coordinates these Terraform operations; the demonstrated contention ends through normal completion, without disabling locking.

### s04 · check · What does contention establish?
Check — Read the supplied question and choose the conclusion supported by the evidence.
QUESTION [choice, intro, grading=client] Two authorized Terraform operations target the same S3 state. What is the purpose of state locking?
  ✔ o1: Prevent conflicting concurrent state writes.
      why: Locking coordinates concurrent writers to prevent conflicting writes.
  ✘ o2: Replace restrictions on who can read state.
      why: Writer coordination does not replace state-access isolation.
  ✘ o3: Allow both operations to bypass a held lock.
      why: A competing operation must not acquire the held lock or change state.
  feedback✔: Your judgement follows the supplied evidence and the required checks.  feedback✘: Recheck the evidence against each required criterion; a partial check is not enough.  hints: ['Look at what the competitor did while the first lock was held.']  remediation→r01
  MEASURES: A:determine_whether_a_competing_state_writer_is_blocked(f3)   anchors=['assessment:determine_whether_a_competing_state_writer_is_blocked']
  taught-before-tested: A.f3←s01

### s05 · check · Is locking an access boundary?
Check — Read the supplied question and choose the conclusion supported by the evidence.
QUESTION [choice, core, grading=client] A held state lock blocks a competing authorized writer. What does this establish about state access?
  ✔ o1: It verifies writer coordination, not whether unapproved identities are denied state access.
      why: Coordination of authorized writers is distinct from state-access authorization.
  ✘ o2: It proves every unapproved identity is denied state reads.
      why: Blocking a concurrent writer does not verify who can read state.
  ✘ o3: It replaces scoped state access permissions.
      why: State locking coordinates writers; scoped access permissions are separate.
  feedback✔: Your judgement follows the supplied evidence and the required checks.  feedback✘: Recheck the evidence against each required criterion; a partial check is not enough.  hints: ['Look at what the competitor did while the first lock was held.']  remediation→r02
  MEASURES: A:distinguish_writer_coordination_from_state_access_authorization(f4)   anchors=['assessment:distinguish_writer_coordination_from_state_access_authorization']
  taught-before-tested: A.f4←s01

### s06 · hands_on · Review verify lock contention
Review evidence — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each supplied Terraform contention record and decide whether it verifies enabled S3 lock-file coordination and safe completion. State-access permissions are already supplied separately.
  'Backend: use_lockfile = true; supplied reinitialization completed
.tflock permissions: s3:GetObject, s3:PutObject, s3:DeleteObject present
Authorized first apply: lock held under supplied synchronization
Competing operation: lock-acquisition failure; no state change
First apply: normal completion; separate exercise bucket provisioned; lock released' -> Meets every supplied verification criterion
      feedback: Locking is enabled with the required permissions, the competitor fails without changing state, and the first operation completes normally.
  'Backend: use_lockfile = true; reinitialized
.tflock permissions: required operations present
First apply: active and holding lock
Competing operation: bypassed locking and changed state
First apply: later completes' -> Does not meet every supplied verification criterion
      feedback: A competitor must not change state while the first operation holds the lock.
  'Backend: use_lockfile = false
Two authorized operations: completed one after the other without overlap
Separate exercise bucket: provisioned
Review conclusion: controlled lock contention verified' -> Does not meet every supplied verification criterion
      feedback: Sequential completion without an enabled lock or held-lock competition does not verify the required contention behavior.
  'Backend: use_lockfile = true; reinitialized
.tflock permissions: required operations present
First apply: active writer holds lock
Operator: force-unlocked the active writer to let competitor proceed
Competing operation: changed state' -> Does not meet every supplied verification criterion
      feedback: The active writer must not be force-unlocked; the competitor should fail lock acquisition and make no state change.
  feedback✔: Your judgement follows the supplied evidence and the required checks.  feedback✘: Recheck the evidence against each required criterion; a partial check is not enough.  hints: ['Look at what the competitor did while the first lock was held.']  remediation→r03
  MEASURES: A:identify_configuration_and_permissions_for_s3_locking(f1,f2); A:recognize_unsafe_active_writer_lock_bypasses(f3,m1)   anchors=['practice', 'assessment:identify_configuration_and_permissions_for_s3_locking', 'assessment:recognize_unsafe_active_writer_lock_bypasses']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.m1←s02

### s07 · recap · Keep these distinctions
Takeaways — 
(takeaway) Enable opt-in S3 lock-file locking and its .tflock permissions. During contention, verify the competitor cannot acquire the lock or change state. Do not bypass an active writer. Locking coordinates writers; it is not an authorization boundary. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
[UP NEXT] Next: Wait for authorized approval: A production promotion needs an authorized decision for the exact staged revision.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: verify lock contention
(definition) During the controlled state-changing operation that holds the lock, attempt a competing operation and verify it cannot acquire the lock or change state; do not disable locking to bypass the test. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) Contrast legitimate recovery of a failed operation’s leftover lock with bypassing an active writer. Contention is a reason to verify blocking, not disable locking. ⟦A.f3 A.m1 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r02 · Review: verify lock contention
(definition) Locking coordinates concurrent state writers; it is not an authorization boundary against identities that can directly change state objects. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast competing authorized operations with direct state-object access. A lock coordinates the former; it is not an authorization boundary for identities able to change state objects directly. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
### r03 · Review: verify lock contention
(definition) The S3 backend supports lock-file locking when use_lockfile = true; locking is opt-in. Set use_lockfile = true in the supplied S3 backend configuration and use the supplied s3:GetObject, s3:PutObject and s3:DeleteObject permissions on the .tflock object. During the controlled state-changing operation that holds the lock, attempt a competing operation and verify it cannot acquire the lock or change state; do not disable locking to bypass the test. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(definition) Force-unlock is not a safe way to bypass another active state writer; it is reserved for a lock from a failed operation when automatic unlocking failed. ⟦A.m1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(misconception) Contrast legitimate recovery of a failed operation’s leftover lock with bypassing an active writer. Contention is a reason to verify blocking, not disable locking. ⟦A.f3 A.m1 A:tb3 A:tb4 A:tb5 A:tb6⟧

=========

# EVALUATOR PACKET — Wait for authorized approval (aws_devops.tile.123)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.control_environment_promotion_with_a_manual_approval — Control environment promotion with a manual approval

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.control_environment_promotion_with_a_manual_approval)   objective: Gate environment promotion with manual approval
A.f1: A manual approval action stops pipeline progression until an authorized approver approves; rejection or expiration fails the action.   [sources: aws_codepipeline_user_guide#approvals.html]
A.f2: Place an approval action between staging and production with the supplied review link or revision context and authorized approver permissions.   [sources: aws_codepipeline_user_guide#approvals.html]
A.f3: Verify the pipeline stops at approval and advances only after approval of the intended execution and revision.   [sources: aws_codepipeline_user_guide#approvals.html]
A.m1 (misconception): Receiving an approval notification does not itself grant permission to approve the action; approval requires the appropriate authorization.   [sources: aws_codepipeline_user_guide#approvals.html]
note: Use supplied approval context and permissions; do not invent expiration durations or approvers.
PRACTICE ANCHOR (tool_simulation): Add one manual approval action between staging and production in the supplied pipeline, using the supplied review link or revision context and designated approver permissions.  SUCCESS: The approval action sits between staging and production and carries the supplied review context. The intended execution and revision stop at approval, production does not begin while approval is pending, and progression resumes only after the authorized approver accepts that execution and revision.
ASSESSMENT ANCHOR: verify_promotion_waits_for_approval_of_intended_execution_and_revision facts=['f1', 'f3']
ASSESSMENT ANCHOR: verify_approval_gate_placement_context_and_approver_authorization facts=['f2', 'm1']
ASSESSMENT ANCHOR: identify_rejection_and_expiration_as_approval_action_failures facts=['f1']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Document incident evidence and a preventive change using reused systematic-debugging coverage; Endpoint cutover; Recover an incident safely using an established runbook; Verify restored service and data against RTO/RPO in an isolated rehearsal

## LESSON, in learner order

### s01 · explainer · Wait for authorized approval
Learn — 
(definition) Manual approval stops pipeline progression until an authorized approver approves. Rejection or expiration fails the action. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) Place approval between staging and production with the supplied review link or revision context and authorized approver permissions. Verify the pipeline waits there, then advances only after approval of the intended execution and revision. ⟦A.f2 A.f3 A:tb3 A:tb4⟧
(misconception) A notification does not grant approval authority. Check the approver permissions separately from notification delivery. Approval recorded for one revision is not approval of another; keep the intended execution and revision with the wait and progression evidence. ⟦A.m1 A.f3 A:tb5 A:tb6⟧
[DIAGRAM: Schematic approval state review] nodes=['Staging: intended execution and revision', 'Approval pending: review link / revision context', 'Authorized approver approves intended execution and revision', 'Production progression verified', 'Rejection or expiration: action fails'] edges=[('n1', 'n2', 'Wait point'), ('n2', 'n3', 'Authorized decision'), ('n3', 'n4', 'Advance'), ('n2', 'n5', 'Reject / expire')] alt: Staging: intended execution and revision → Approval pending: review link / revision context → Authorized approver approves intended execution and revision → Production progression verified → Rejection or expiration: action fails

### s02 · check · What permits pipeline progression?
Check — Read the supplied question and choose the conclusion supported by the evidence.
QUESTION [choice, intro, grading=client] What happens when the manual approval action is rejected or expires?
  ✘ o1: Production proceeds because staging already completed.
      why: Rejection or expiration fails the approval action; staging completion is not approval.
  ✔ o2: The approval action fails.
      why: Rejection or expiration fails the action.
  ✘ o3: Expiration counts as approval of the intended revision.
      why: Expiration is a failure, not authorized approval.
  feedback✔: Your judgement follows the supplied evidence and the required checks.  feedback✘: Recheck the evidence against each required criterion; a partial check is not enough.  hints: ['Track which execution and revision the approval belongs to.']  remediation→r01
  MEASURES: A:identify_rejection_and_expiration_as_approval_action_failures(f1)   anchors=['assessment:identify_rejection_and_expiration_as_approval_action_failures']
  taught-before-tested: A.f1←s01

### s03 · hands_on · Review wait for authorized approval
Review evidence — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each manual-approval review record. Decide whether it verifies an approval gate between staging and production, supplied review context and authorization, and progression only after acceptance of the intended execution and revision.
  'Stage order: staging -> manual approval -> production
Review context: supplied link and intended revision
Approver permissions: authorized
Intended execution/revision: stops at approval
Pending interval: production has not begun
Authorized acceptance: intended execution and revision approved
Subsequent progression: production begins' -> Meets every supplied verification criterion
      feedback: Placement, context, authorized acceptance and execution-specific waiting are all verified.
  'Stage order: staging -> manual approval -> production
Review context: intended revision; authorized approver
Approval: pending
Production: already began' -> Does not meet every supplied verification criterion
      feedback: Production must not begin while the intended approval is pending.
  'Stage order: staging -> manual approval -> production
Review context and authorized permissions: present
Intended execution/revision: remains pending
Acceptance record: belongs to a different execution and revision
Production: begins for the intended execution' -> Does not meet every supplied verification criterion
      feedback: Acceptance must be for the intended execution and revision, not another one.
  'Stage order: staging -> manual approval -> production
Context and authorization: supplied
Intended execution: stopped at approval
Approval: expired
Review conclusion: expiration accepted as approval; production begins' -> Does not meet every supplied verification criterion
      feedback: Expiration fails the approval action rather than authorizing production.
  feedback✔: Your judgement follows the supplied evidence and the required checks.  feedback✘: Recheck the evidence against each required criterion; a partial check is not enough.  hints: ['Track which execution and revision the approval belongs to.']  remediation→r02
  MEASURES: A:verify_promotion_waits_for_approval_of_intended_execution_and_revision(f1,f3); A:verify_approval_gate_placement_context_and_approver_authorization(f2,m1); A:identify_rejection_and_expiration_as_approval_action_failures(f1)   anchors=['practice', 'assessment:verify_promotion_waits_for_approval_of_intended_execution_and_revision', 'assessment:verify_approval_gate_placement_context_and_approver_authorization', 'assessment:identify_rejection_and_expiration_as_approval_action_failures']
  taught-before-tested: A.f1←s01; A.f3←s01; A.f2←s01; A.m1←s01; A.f1←s01

### s04 · recap · Keep these distinctions
Takeaways — 
(takeaway) Approval belongs between staging and production. Verify waiting and progression for the intended execution and revision. Rejection or expiration fails the action; a notification alone does not grant approval authority. ⟦A.f1 A.f2 A.f3 A.m1 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
[UP NEXT] Next: Stay within the runbook: An incident matches an established runbook, but routine execution still depends on its preconditions and expected outcomes.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: wait for authorized approval
(definition) A manual approval action stops pipeline progression until an authorized approver approves; rejection or expiration fails the action. ⟦A.f1 A:tb2 A:tb4⟧
(misconception) Contrast notification receipt with permission to approve. Only authorized approval of the intended execution and revision supports progression. ⟦A.f3 A.m1 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r02 · Review: wait for authorized approval
(definition) A manual approval action stops pipeline progression until an authorized approver approves; rejection or expiration fails the action. Place an approval action between staging and production with the supplied review link or revision context and authorized approver permissions. Verify the pipeline stops at approval and advances only after approval of the intended execution and revision. Receiving an approval notification does not itself grant permission to approve the action; approval requires the appropriate authorization. ⟦A.f1 A.f2 A.f3 A.m1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(misconception) Contrast notification receipt with permission to approve. Only authorized approval of the intended execution and revision supports progression. ⟦A.f3 A.m1 A:tb3 A:tb4 A:tb5 A:tb6⟧

=========

# EVALUATOR PACKET — Stay within the runbook (aws_devops.tile.124)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.recover_an_incident_safely_using_an_established_runbook — Recover an incident safely using an established runbook

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.recover_an_incident_safely_using_an_established_runbook)   objective: Recover an incident using an established runbook
A.f1: A runbook describes known procedures and their expected operational outcomes.   [sources: aws_well_architected_framework#ops05-bp01.html]
A.f2: Verify the established runbook’s preconditions, execute only the approved actions and check each expected result before advancing.   [sources: aws_well_architected_framework#ops05-bp01.html]
A.f3: On a supplied stop condition or an outcome outside the runbook’s bounds, stop routine execution and escalate with the observed evidence.   [sources: aws_well_architected_framework#ops06-bp03.html]
note: Use established runbook and owners; do not invent recovery actions or skip expected-result checks.
PRACTICE ANCHOR (tool_simulation): Respond to one seeded sandbox service incident using a supplied established runbook and escalation owner. Verify its preconditions, execute only approved actions, and compare each result with its expected outcome before advancing. Stop and escalate with observed evidence if a supplied stop condition occurs.  SUCCESS: The action record shows verified preconditions and only approved actions, with each expected-result check completed before advancement. Execution ends either with the runbook's recovery success checks satisfied or with routine execution stopped at a supplied stop condition or out-of-bounds result and an escalation containing the last completed action and observed evidence.
ASSESSMENT ANCHOR: identify_runbook_procedures_and_expected_outcomes facts=['f1']
ASSESSMENT ANCHOR: verify_preconditions_and_approved_action_success_checks facts=['f2']
ASSESSMENT ANCHOR: stop_and_escalate_out_of_bounds_results_with_evidence facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Document incident evidence and a preventive change using reused systematic-debugging coverage; Endpoint cutover; Verify restored service and data against RTO/RPO in an isolated rehearsal

## LESSON, in learner order

### s01 · explainer · Stay within the runbook
Learn — 
(definition) A runbook describes known procedures and expected operational outcomes. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) Verify its preconditions, take only approved actions, and check each expected result before advancing. On a supplied stop condition or an out-of-bounds outcome, stop routine execution and escalate with observed evidence. ⟦A.f2 A.f3 A:tb3⟧
[DIAGRAM: Schematic runbook execution record] nodes=['Verify supplied runbook preconditions', 'Current approved action', 'Expected outcome ↔ actual result', 'Within bounds: record result, next approved action', 'Stop condition / outside bounds: stop and escalate with evidence'] edges=[('n1', 'n2', 'Before action'), ('n2', 'n3', 'Check'), ('n3', 'n4', 'Matches'), ('n3', 'n5', 'Stop / mismatch')] alt: Verify supplied runbook preconditions → Current approved action → Expected outcome ↔ actual result → Within bounds: record result, next approved action → Stop condition / outside bounds: stop and escalate with evidence

### s02 · explainer · Read the evidence, not the shortcut
Learn — 
(example) Use the supplied runbook to compare each actual result with its expected outcome. A passing result permits the next approved action. A supplied stop condition or result outside the bounds calls for stopping and escalation. Preserve the last completed action and the result that required escalation so the next responder has a reproducible record. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) A runbook that initially matches the incident is not unconditional permission to continue. Its preconditions, expected results and stop bounds remain in force at each action boundary. Do not improvise extra resource changes when a check says the situation is outside routine execution; preserve the observed evidence and escalate. ⟦A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · check · When must routine execution stop?
Check — Read the supplied question and choose the conclusion supported by the evidence.
QUESTION [choice, intro, grading=client] A supplied runbook action returns an outcome outside its bounds. What is the safe next decision?
  ✘ o1: Advance because the action was approved.
      why: Approval to attempt an action does not authorize advancement past an out-of-bounds result.
  ✘ o2: Replace the established procedure with an unapproved action.
      why: Execute only approved actions and stop on the supplied condition.
  ✔ o3: Stop routine execution and escalate with observed evidence.
      why: An out-of-bounds outcome requires stopping and escalation with evidence.
  feedback✔: Your judgement follows the supplied evidence and the required checks.  feedback✘: Recheck the evidence against each required criterion; a partial check is not enough.  hints: ['Look for the expected-result check before each advancement.']  remediation→r01
  MEASURES: A:stop_and_escalate_out_of_bounds_results_with_evidence(f3)   anchors=['assessment:stop_and_escalate_out_of_bounds_results_with_evidence']
  taught-before-tested: A.f3←s01

### s04 · hands_on · Review stay within the runbook
Review evidence — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read the supplied established-runbook action records and decide whether each stays within the procedure: verified preconditions, approved actions only, expected-result checks before advancement, and either verified recovery or stopping and escalation with the last completed action and observations.
  'Preconditions: verified
Action A: approved; expected result checked and met before B
Action B: approved; expected result checked and met
Final recovery success checks: all satisfied' -> Meets every supplied verification criterion
      feedback: Preconditions, approved actions, ordered result checks and recovery success are documented.
  'Preconditions: verified
Action A: approved; expected result checked and met
Action B: approved; observed result outside supplied bounds
Routine execution: stopped; no further action
Escalation to supplied owner: last completed action B and observed out-of-bounds evidence included' -> Meets every supplied verification criterion
      feedback: The out-of-bounds branch stops routine execution and escalates the last action and observed evidence.
  'Preconditions: verified
Action A: approved; expected result not checked
Action B: begun immediately
Review conclusion: advancement safe because A was approved' -> Does not meet every supplied verification criterion
      feedback: Each expected result must be checked before advancing.
  'Preconditions: verified
Approved action: supplied stop condition observed
Routine execution: continued with an unapproved corrective action
Escalation: none' -> Does not meet every supplied verification criterion
      feedback: A supplied stop condition requires stopping and escalation, not an unapproved action.
  feedback✔: Your judgement follows the supplied evidence and the required checks.  feedback✘: Recheck the evidence against each required criterion; a partial check is not enough.  hints: ['Look for the expected-result check before each advancement.']  remediation→r02
  MEASURES: A:identify_runbook_procedures_and_expected_outcomes(f1); A:verify_preconditions_and_approved_action_success_checks(f2); A:stop_and_escalate_out_of_bounds_results_with_evidence(f3)   anchors=['practice', 'assessment:identify_runbook_procedures_and_expected_outcomes', 'assessment:verify_preconditions_and_approved_action_success_checks', 'assessment:stop_and_escalate_out_of_bounds_results_with_evidence']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s05 · recap · Keep these distinctions
Takeaways — 
(takeaway) Verify preconditions, take only approved actions and compare each result with the expected outcome. At a stop condition or out-of-bounds result, stop and escalate with evidence. A familiar runbook is not unconditional permission to continue. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Measure time and data separately: An isolated rehearsal restored a service, but the recovery objectives need two separate measured comparisons.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: stay within the runbook
(definition) On a supplied stop condition or an outcome outside the runbook’s bounds, stop routine execution and escalate with the observed evidence. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast a matching expected result with an out-of-bounds result. The first permits the next approved action; the second requires stopping and escalation. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Review: stay within the runbook
(definition) A runbook describes known procedures and their expected operational outcomes. Verify the established runbook’s preconditions, execute only the approved actions and check each expected result before advancing. On a supplied stop condition or an outcome outside the runbook’s bounds, stop routine execution and escalate with the observed evidence. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast a matching expected result with an out-of-bounds result. The first permits the next approved action; the second requires stopping and escalation. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Measure time and data separately (aws_devops.tile.125)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.verify_restored_service_and_data_against_rto_rpo_in_an_isolated_rehearsal — Verify restored service and data against RTO/RPO in an isolated rehearsal

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.verify_restored_service_and_data_against_rto_rpo_in_an_isolated_rehearsal)   objective: Verify restored service against RTO and RPO
A.f1: Recovery verification must test both restoration time against RTO and recoverable data loss against RPO.   [sources: aws_wa_devops_guidance#ag.dlm.1-define-recovery-objectives-to-maintain-business-continuity.html]
A.f2: Using the supplied timestamps, measure elapsed time from the defined disruption start to passing service-readiness checks and compare it with RTO.   [sources: aws_wa_devops_guidance#ag.dlm.1-define-recovery-objectives-to-maintain-business-continuity.html]
A.f3: Using the supplied recovery markers, measure the gap between the disruption point and the latest recovered data point and compare it with RPO; a running service alone does not prove either objective was met.   [sources: aws_wa_devops_guidance#ag.dlm.1-define-recovery-objectives-to-maintain-business-continuity.html]
note: Use isolated rehearsal and supplied readiness/data markers; do not substitute resource status for service checks.
PRACTICE ANCHOR (spreadsheet): Measure one isolated restoration using supplied disruption-start and passing-readiness timestamps, the latest recovered data marker, and stated RTO and RPO limits. Record each measured interval and its independent pass/fail conclusion.  SUCCESS: The completed worksheet measures restoration time from disruption start to passing service-readiness checks and compares it with RTO. It measures the gap from the latest recovered data marker to the disruption point and compares it with RPO. Both conclusions cite the supplied evidence rather than running-service status alone.
ASSESSMENT ANCHOR: verify_both_recovery_objectives_independently facts=['f1']
ASSESSMENT ANCHOR: compare_elapsed_time_to_service_readiness_with_rto facts=['f2']
ASSESSMENT ANCHOR: compare_recovered_data_gap_with_rpo facts=['f3']
ASSESSMENT ANCHOR: distinguish_running_service_status_from_recovery_verification facts=['f3']

## DATA ASSETS USED
ds.recovery_objectives: Independent RTO and RPO comparisons — columns: case_id(identifier), environment(categorical), disruption_start(datetime), passing_readiness_at(datetime), readiness_evidence(text), latest_recovered_marker(datetime), restoration_minutes(numerical), rto_minutes(numerical), rto_result(categorical), data_gap_minutes(numerical), rpo_minutes(numerical), rpo_result(categorical)
   ["illustrative","isolated rehearsal","10:00","10:18","Supplied service-readiness checks pass","09:56",18,20,"pass",4,5,"pass"]
   ["alternative_marker","isolated rehearsal","10:00","10:18","Supplied service-readiness checks pass","09:50",18,20,"pass",10,5,"fail"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Document incident evidence and a preventive change using reused systematic-debugging coverage; Endpoint cutover

## LESSON, in learner order

### s01 · explainer · Measure time and data separately
Learn — 
(definition) An isolated recovery rehearsal needs two independent comparisons: restoration time against RTO and recoverable data loss against RPO. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) Measure elapsed time from the defined disruption start to passing service-readiness checks for RTO. Measure the gap from the disruption point to the latest recovered data point for RPO. A running service alone proves neither objective. ⟦A.f2 A.f3 A:tb3⟧
[TABLE ds.recovery_objectives cols=['case_id', 'environment', 'disruption_start', 'passing_readiness_at', 'readiness_evidence', 'latest_recovered_marker', 'restoration_minutes', 'rto_minutes', 'rto_result', 'data_gap_minutes', 'rpo_minutes', 'rpo_result'] ] caption: Independent RTO and RPO comparisons

### s02 · explainer · Read the evidence, not the shortcut
Learn — 
(example) Inspect the registered illustrative timestamps, passing-readiness evidence and recovered markers. Compare restoration_minutes with rto_minutes, and data_gap_minutes with rpo_minutes. The alternative marker leaves restoration time unchanged but changes the data-loss comparison. Keep each conclusion attached to its own evidence; these are illustrative objectives and measurements, not AWS defaults. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) A good RTO result cannot substitute for the RPO result. Passing readiness establishes the endpoint for the restoration-time measurement, not the latest recovered data point. Likewise, a recent recovered marker does not establish how long restoration took. Retain both timestamp comparisons instead of calling recovery successful because the service runs. ⟦A.f1 A.f2 A.f3 A:tb5⟧

### s03 · check · Are both recovery objectives verified?
Check — Read the supplied question and choose the conclusion supported by the evidence.
QUESTION [choice, intro, grading=client] Passing service-readiness checks establish a running restored service. Which conclusion about recovery objectives is defensible?
  ✘ o1: Both objectives automatically pass.
      why: A running service alone proves neither objective.
  ✘ o2: Only the RPO needs a timestamp comparison.
      why: Restoration time must also be measured and compared with RTO.
  ✔ o3: Restoration time and recovered-data gap must be measured and compared independently with RTO and RPO.
      why: Recovery verification tests both restoration time and recoverable data loss.
  feedback✔: Your judgement follows the supplied evidence and the required checks.  feedback✘: Recheck the evidence against each required criterion; a partial check is not enough.  hints: ['Use different start and end evidence for restoration and data loss.']  remediation→r01
  MEASURES: A:verify_both_recovery_objectives_independently(f1)   anchors=['assessment:verify_both_recovery_objectives_independently']
  taught-before-tested: A.f1←s01

### s04 · hands_on · Calculate recovery time and data loss
Review evidence — Using the supplied rehearsal timestamps and recovered data markers, calculate the elapsed time from disruption start to passing service-readiness checks and the gap between the latest recovered data point and disruption. Compare these measurements independently with the supplied RTO and RPO.
QUESTION [formula_entry, stretch, grading=client] In Sheet1, enter one formula in M2 that records both independent recovery measurements and pass/fail conclusions for rows 2 and 3, in that order. Columns: A case_id, C disruption_start, D passing_readiness_at, E readiness_evidence, F latest_recovered_marker, H rto_minutes, K rpo_minutes. Times are same-day HH:MM in an isolated rehearsal; the supplied readiness evidence confirms D is when checks passed. Compute restoration minutes from C to D and data-gap minutes from F to C, rounded to whole minutes. Compare restoration <= H and gap <= K independently. Do not use precomputed result columns G, I, J or L. Exact output format for each row: <case_id>: RTO=<minutes> minutes <pass/fail>; RPO=<minutes> minutes <pass/fail>. Join the two row summaries with " | ". The sheet interprets HH:MM values as fractions of a day; multiply each time difference by 1440 to convert to minutes. Use formulas referencing the supplied cells; do not type measured answers. Any supported formula that produces the specified rounded measurements and independent conclusions is acceptable.
  [unrendered interaction type formula_entry] public={"prompt":"In Sheet1, enter one formula in M2 that records both independent recovery measurements and pass/fail conclusions for rows 2 and 3, in that order. Columns: A case_id, C disruption_start, D passing_readiness_at, E readiness_evidence, F latest_recovered_marker, H rto_minutes, K rpo_minutes. Times are same-day HH:MM in an isolated rehearsal; the supplied readiness evidence confirms D is when checks passed. Compute restoration minutes from C to D and data-gap minutes from F to C, rounded to whole minutes. Compare restoration <= H and gap <= K independently. Do not use precomputed result columns G, I, J or L. Exact output format for each row: <case_id>: RTO=<minutes> minutes <pass/fail>; RPO=<minutes> minutes <pass/fail>. Join the two row summaries with \" | \". The sheet interprets HH:MM values as fractions of a day; multiply each time difference by 1440 to convert to minutes. Use  grading={"expected_value":"illustrative: RTO=18 minutes pass; RPO=4 minutes pass | alternative_marker: RTO=18 minutes pass; RPO=10 minutes fail","reference_formula":"=A2&\": RTO=\"&ROUND((D2-C2)*1440,0)&\" minutes \"&IF(ROUND((D2-C2)*1440,0)<=H2,\"pass\",\"fail\")&\"; RPO=\"&ROUND((C2-F2)*1440,0)&\" minutes \"&IF(ROUND((C2-F2)*1440,0)<=K2,\"pass\",\"fail\")&\" | \"&A3&\": RTO=\"&ROUND((D3-C3)*1440,0)&\" minutes \"&IF(ROUND((D3-C3)*1440,0)<=H3,\"pass\",\"fail\")&\"; RPO=\"&ROUND((C3-F3)*1440,0)&\" minutes \"&IF(ROUND((C3-F3)*1440,0)<=K3,\"pass\",\"fail\")","forbid_hardcoded_values":true}
  feedback✔: Both restoration-time and data-gap conclusions follow the supplied timestamps and independent limits.  feedback✘: Recheck the evidence against each required criterion; a partial check is not enough.  hints: ['Use different start and end evidence for restoration and data loss.']  remediation→r02
  MEASURES: A:compare_elapsed_time_to_service_readiness_with_rto(f2); A:compare_recovered_data_gap_with_rpo(f3); A:distinguish_running_service_status_from_recovery_verification(f3)   anchors=['practice', 'assessment:compare_elapsed_time_to_service_readiness_with_rto', 'assessment:compare_recovered_data_gap_with_rpo', 'assessment:distinguish_running_service_status_from_recovery_verification']
  taught-before-tested: A.f2←s01; A.f3←s01; A.f3←s01

### s05 · recap · Keep these distinctions
Takeaways — 
(takeaway) Measure disruption-to-passing-readiness time against RTO. Separately measure the recovered-data gap against RPO. One passing comparison cannot replace the other, and a running service alone proves neither. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Connect evidence to prevention: A verified incident fix should lead to a factual timeline and one justified preventive action.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: measure time and data separately
(definition) Recovery verification must test both restoration time against RTO and recoverable data loss against RPO. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(misconception) Contrast the registered alternative recovered marker with the illustrative marker: restoration time is unchanged, but the data-loss comparison differs. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.recovery_objectives cols=['case_id', 'environment', 'disruption_start', 'passing_readiness_at', 'readiness_evidence', 'latest_recovered_marker', 'restoration_minutes', 'rto_minutes', 'rto_result', 'data_gap_minutes', 'rpo_minutes', 'rpo_result'] ] caption: Independent RTO and RPO comparisons
### r02 · Review: measure time and data separately
(definition) Using the supplied timestamps, measure elapsed time from the defined disruption start to passing service-readiness checks and compare it with RTO. Using the supplied recovery markers, measure the gap between the disruption point and the latest recovered data point and compare it with RPO; a running service alone does not prove either objective was met. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast the registered alternative recovered marker with the illustrative marker: restoration time is unchanged, but the data-loss comparison differs. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.recovery_objectives cols=['case_id', 'environment', 'disruption_start', 'passing_readiness_at', 'readiness_evidence', 'latest_recovered_marker', 'restoration_minutes', 'rto_minutes', 'rto_result', 'data_gap_minutes', 'rpo_minutes', 'rpo_result'] ] caption: Independent RTO and RPO comparisons

## OTHER CONTENT (fields without a dedicated renderer)
· grading.reference_formula: =A2&": RTO="&ROUND((D2-C2)*1440,0)&" minutes "&IF(ROUND((D2-C2)*1440,0)<=H2,"pass","fail")&"; RPO="&ROUND((C2-F2)*1440,0)&" minutes "&IF(ROUND((C2-F2)*1440,0)<=K2,"pass","fail")&" | "&A3&": RTO="&ROUND((D3-C3)*1440,0)&" minutes "&IF(ROUND((D3-C3)*1440,0)<=H3,"pass","fail")&"; RPO="&ROUND((C3-F3)*1440,0)&" minutes "&IF(ROUND((C3-F3)*1440,0)<=K3,"pass","fail")

=========

# EVALUATOR PACKET — Connect evidence to prevention (aws_devops.tile.126)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.document_incident_evidence_and_a_preventive_change — Document incident evidence and a preventive change using reused systematic-debugging coverage

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.document_incident_evidence_and_a_preventive_change)   objective: Document incident evidence and a preventive change
A.f1: Post-incident analysis documents the incident’s impact, events, contributing causes and actions to reduce recurrence.   [sources: aws_well_architected_framework#ops07-bp01.html]
A.f2: Write a timeline from supplied evidence and distinguish direct observations from causal conclusions supported by the verified fix.   [sources: aws_well_architected_framework#ops07-bp01.html]
A.f3: Record one preventive action justified by the demonstrated cause, with an accountable owner and a way to verify completion.   [sources: aws_well_architected_framework#ops07-bp01.html]
note: Use supplied evidence only; do not invent causal facts, blame or unrelated preventive work.
PRACTICE ANCHOR (external_proof): Write one short incident record using supplied logs, impact evidence and a verified fix. Include a factual timeline, a separately identified supported causal conclusion and one justified preventive action with an accountable owner and completion check.  SUCCESS: The record documents impact and timestamped events without inventing evidence, distinguishes observations from the causal conclusion supported by the verified fix, and ties one preventive action to that demonstrated cause. The action names an accountable owner and a verifiable completion condition.
ASSESSMENT ANCHOR: link_incident_timeline_to_supported_cause facts=['f1', 'f2']
ASSESSMENT ANCHOR: justify_accountable_prevention_from_verified_cause facts=['f2', 'f3']

## DATA ASSETS USED
ds.incident_evidence_to_action: Factual timeline and bounded prevention — columns: record_id(identifier), timestamp(datetime), record_kind(categorical), impact_evidence(text), direct_observation(text), supported_causal_conclusion(text), preventive_action(text), accountable_owner(categorical), completion_check(text)
   ["incident.symptom","2026-01-12T10:00:00Z","observation","Supplied service-readiness check fails","Readiness failure recorded","","","",""]
   ["incident.investigation","2026-01-12T10:02:00Z","observation","","Supplied configuration comparison records a mismatch against the approved configuration","","","",""]
   ["incident.correction","2026-01-12T10:10:00Z","observation","","Approved correction restores the mismatched configuration to the supplied approved value","","","",""]
   ["incident.verification","2026-01-12T10:18:00Z","observation","Supplied service-readiness check passes","Readiness passes after the approved configuration correction","","","",""]
   ["incident.follow_up","2026-01-12T10:20:00Z","conclusion_and_action","","","The verified correction supports the identified configuration error; no additional cause is asserted","Detect that configuration mismatch before accepting the configuration","Operational owner","Replay the supplied mismatch 

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Endpoint cutover

## LESSON, in learner order

### s01 · explainer · Connect evidence to prevention
Learn — 
(definition) Post-incident analysis records impact, events, contributing causes and actions to reduce recurrence. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) Build the timeline from supplied evidence. Separate direct observations from causal conclusions supported by the verified fix. Tie one preventive action to the demonstrated cause, naming an accountable owner and a completion check. ⟦A.f2 A.f3 A:tb3⟧
[TABLE ds.incident_evidence_to_action cols=['record_id', 'timestamp', 'record_kind', 'impact_evidence', 'direct_observation', 'supported_causal_conclusion', 'preventive_action', 'accountable_owner', 'completion_check'] ] caption: Factual timeline and bounded prevention

### s02 · explainer · Read the evidence, not the shortcut
Learn — 
(example) Read the registered symptom, investigation, correction and verification observations in timestamp order. The verified correction supports the identified configuration error, not an additional invented cause. The follow-up detects that same mismatch, assigns an accountable owner and checks completion by replaying the supplied mismatch. Keep this bounded conclusion separate from the factual timeline. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) A plausible causal story is not a supported conclusion. Do not treat every nearby event as a contributing cause, assign unsupported blame, or choose unrelated improvements. A preventive action should address the recurrence path demonstrated by the verified fix. Its owner and verification method make the follow-up accountable. ⟦A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · video · Observe the operating model
Observe — 
[VIDEO Evidence-based incident records and accountable prevention] bridge-before: Watch for the incident-record structure and concrete completion criteria for follow-up actions. The clip uses “postmortem” for post-incident analysis and emphasizes contributing causes rather than personal blame. | bridge-after: The clip explains structure and accountability, but does not work through an evidence timeline or justify one action from a verified cause. The text covers observation-versus-conclusion separation and cause-linked prevention.
  - qKTxXE5h-18 73-199s facts=['f1'] label: Structure a factual incident record and accountable preventive actions | summary: Post-incident analysis, called a postmortem here, records impact, response actions, causes and follow-up work. A blameless account focuses on contributing system and process conditions rather than accusing individuals or teams. A useful structure includes an executive summary, incident details, impact, causes and trigger, a timeline, lessons learned and action items. Severity claims should use verifiable data rather than dramatic language. Follow-up actions need clear owners, priorities, tracking tickets and verifiable completion criteria. Include prevention rather than only mitigation, and track completion dates or estimates so actions can be reviewed later.

### s04 · check · Is prevention justified by evidence?
Check — Read the supplied question and choose the conclusion supported by the evidence.
QUESTION [choice, intro, grading=client] What makes a preventive action accountable and justified in a post-incident record?
  ✔ o1: It is tied to the demonstrated cause and names an owner and a verifiable completion condition.
      why: Prevention must follow the demonstrated cause, with an accountable owner and completion check.
  ✘ o2: It is based on a possible cause with no support from the verified fix.
      why: Causal conclusions must be supported by evidence and the verified fix.
  ✘ o3: It names an owner but leaves completion unverifiable.
      why: An accountable action also needs a way to verify completion.
  feedback✔: Your judgement follows the supplied evidence and the required checks.  feedback✘: Recheck the evidence against each required criterion; a partial check is not enough.  hints: ['Separate observations from the causal conclusion and its follow-up.']  remediation→r01
  MEASURES: A:justify_accountable_prevention_from_verified_cause(f2,f3)   anchors=['assessment:justify_accountable_prevention_from_verified_cause']
  taught-before-tested: A.f2←s01; A.f3←s01

### s05 · hands_on · Document the supported follow-up
Review evidence — Use the supplied incident evidence to write a factual timeline, a separately supported causal conclusion and one accountable preventive action.
QUESTION [external_proof, stretch, grading=client] Submit a text post-incident record based only on this supplied fictional evidence. Include impact and a timestamped timeline; label observations separately from the supported causal conclusion. Record one preventive action tied to the demonstrated cause, its accountable owner and a completion verification. Do not invent evidence or additional causes.

2026-01-12T10:00:00Z | impact_evidence: Supplied service-readiness check fails | direct_observation: Readiness failure recorded
2026-01-12T10:02:00Z | direct_observation: Supplied configuration comparison records a mismatch against the approved configuration
2026-01-12T10:10:00Z | direct_observation: Approved correction restores the mismatched configuration to the supplied approved value
2026-01-12T10:18:00Z | impact_evidence: Supplied service-readiness check passes | direct_observation: Readiness passes after the approved configuration correction
2026-01-12T10:20:00Z | supported_causal_conclusion: The verified correction supports the identified configuration error; no additional cause is asserted | preventive_action: Detect that configuration mismatch before accepting the configuration | accountable_owner: Operational owner | completion_check: Replay the supplied mismatch and verify the configuration check detects it
  [unrendered interaction type external_proof] public={"instruction":"Submit a text post-incident record based only on this supplied fictional evidence. Include impact and a timestamped timeline; label observations separately from the supported causal conclusion. Record one preventive action tied to the demonstrated cause, its accountable owner and a completion verification. Do not invent evidence or additional causes.\n\n2026-01-12T10:00:00Z | impact_evidence: Supplied service-readiness check fails | direct_observation: Readiness failure recorded\n2026-01-12T10:02:00Z | direct_observation: Supplied configuration comparison records a mismatch against the approved configuration\n2026-01-12T10:10:00Z | direct_observation: Approved correction restores the mismatched configuration to the supplied approved value\n2026-01-12T10:18:00Z | impact_evidence: Supplied service-readiness check passes | direct_observation: Readiness passes after the appro grading={"mode":"manual","rubric":[{"criterion":"Document the supplied impact and timestamped events, without adding observations.","weight":1},{"criterion":"Separate direct observations from the narrow causal conclusion supported by the verified configuration correction.","weight":1},{"criterion":"Justify one preventive action from that demonstrated cause, name an accountable owner and give a verifiable completion condition.","weight":1}]}
  feedback✔: The record documents supplied impact and events, supports its cause with the verified fix, and makes prevention accountable and verifiable.  feedback✘: Recheck the evidence against each required criterion; a partial check is not enough.  hints: ['Separate observations from the causal conclusion and its follow-up.']  remediation→r02
  MEASURES: A:link_incident_timeline_to_supported_cause(f1,f2); A:justify_accountable_prevention_from_verified_cause(f2,f3)   anchors=['practice', 'assessment:link_incident_timeline_to_supported_cause', 'assessment:justify_accountable_prevention_from_verified_cause']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f2←s01; A.f3←s01

### s06 · recap · Keep these distinctions
Takeaways — 
(takeaway) Keep the incident timeline factual. Separate observations from the causal conclusion supported by the verified fix. Justify one preventive action from that demonstrated cause, with an accountable owner and a verifiable completion condition. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Verify endpoint convergence: A restored target has passed its readiness checks, and clients now need to reach it through the approved endpoint change.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: connect evidence to prevention
(definition) Write a timeline from supplied evidence and distinguish direct observations from causal conclusions supported by the verified fix. Record one preventive action justified by the demonstrated cause, with an accountable owner and a way to verify completion. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast a direct observation with a supported causal conclusion. The registered verified correction supports the configuration error, not an invented additional cause. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.incident_evidence_to_action cols=['record_id', 'timestamp', 'record_kind', 'impact_evidence', 'direct_observation', 'supported_causal_conclusion', 'preventive_action', 'accountable_owner', 'completion_check'] ] caption: Factual timeline and bounded prevention
### r02 · Review: connect evidence to prevention
(definition) Post-incident analysis documents the incident’s impact, events, contributing causes and actions to reduce recurrence. Write a timeline from supplied evidence and distinguish direct observations from causal conclusions supported by the verified fix. Record one preventive action justified by the demonstrated cause, with an accountable owner and a way to verify completion. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast a direct observation with a supported causal conclusion. The registered verified correction supports the configuration error, not an invented additional cause. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.incident_evidence_to_action cols=['record_id', 'timestamp', 'record_kind', 'impact_evidence', 'direct_observation', 'supported_causal_conclusion', 'preventive_action', 'accountable_owner', 'completion_check'] ] caption: Factual timeline and bounded prevention

=========

# EVALUATOR PACKET — Verify endpoint convergence (aws_devops.tile.127)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = recovery.endpoint_cutover — Endpoint cutover

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (recovery.endpoint_cutover)   objective: Cut over a recovered service endpoint
A.f1: Recovery procedures include restoring service and directing clients to the recovered environment.   [sources: aws_well_architected_framework#rel13-bp02.html]
A.f2: Confirm the restored target’s supplied readiness checks pass, perform the approved DNS or application endpoint switch and verify clients reach the restored target.   [sources: aws_well_architected_framework#rel13-bp02.html]
A.f3: For DNS cutover, account for cached answers and TTL when testing client convergence rather than assuming every client immediately uses the new endpoint.   [sources: aws_well_architected_framework#../../../Route53/latest/DeveloperGuide/resource-record-sets-values-basic.html#rrsets-values-basic-ttl]
note: Use approved cutover procedure only after readiness; do not invent DNS record commands or TTL defaults.
PRACTICE ANCHOR (tool_simulation): Use a supplied sandbox cutover procedure to confirm the restored service's readiness checks pass, switch one supplied DNS endpoint to that service, and verify client convergence using the supplied TTL and client-target evidence.  SUCCESS: The endpoint switch occurs only after readiness checks pass and through the approved procedure. Client checks establish that clients reach the restored target, accounting for cached DNS answers and the supplied TTL rather than treating the configuration update as immediate convergence.
ASSESSMENT ANCHOR: verify_clients_reach_restored_target_after_approved_switch facts=['f1', 'f2']
ASSESSMENT ANCHOR: account_for_dns_caching_and_ttl_in_client_convergence_checks facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): 

## LESSON, in learner order

### s01 · explainer · Verify endpoint convergence
Learn — 
(definition) Recovery includes restoring service and directing clients to the recovered environment. A restored target alone is not verified client convergence. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) First confirm the restored target passes the supplied readiness checks. Perform the approved DNS or application endpoint switch, then verify clients reach the restored target. For DNS, account for cached answers and TTL in those client checks. ⟦A.f2 A.f3 A:tb3 A:tb4⟧
(misconception) An updated DNS setting and an old cached client answer can coexist. Keep actual client-target evidence rather than declaring every client moved at the update request. Configuration change is not proof of convergence: verify clients reach the ready restored target, with caching and the supplied TTL accounted for. ⟦A.f2 A.f3 A:tb4 A:tb5⟧
[DIAGRAM] nodes=['Restored target passes supplied readiness checks', 'Approved DNS or application endpoint switch', 'Updated endpoint setting', 'Some DNS clients may retain cached answers within supplied TTL', 'Verify clients reach the restored target'] edges=[('n1', 'n2', 'Ready first'), ('n2', 'n3', 'Setting changes'), ('n3', 'n4', 'Not immediate convergence'), ('n3', 'n5', 'Client checks'), ('n4', 'n5', 'Account for caching / TTL')] alt: Restored target passes supplied readiness checks → Approved DNS or application endpoint switch → Updated endpoint setting → Some DNS clients may retain cached answers within supplied TTL → Verify clients reach the restored target

### s02 · check · Does a DNS update prove convergence?
Check — Read the supplied question and choose the conclusion supported by the evidence.
QUESTION [choice, intro, grading=client] A DNS setting has been switched to the restored target. What must client-convergence verification account for?
  ✘ o1: Every client immediately uses the new setting.
      why: Cached DNS answers and TTL can affect convergence.
  ✔ o2: Actual client targets, cached answers and the supplied TTL.
      why: Check clients reach the restored target while accounting for caching and TTL.
  ✘ o3: Only the configuration update, with no client checks.
      why: The approved switch is not itself proof that clients reach the restored target.
  feedback✔: Your judgement follows the supplied evidence and the required checks.  feedback✘: Recheck the evidence against each required criterion; a partial check is not enough.  hints: ['Separate a changed setting from clients’ actual targets.']  remediation→r01
  MEASURES: A:account_for_dns_caching_and_ttl_in_client_convergence_checks(f3)   anchors=['assessment:account_for_dns_caching_and_ttl_in_client_convergence_checks']
  taught-before-tested: A.f3←s01

### s03 · hands_on · Review verify endpoint convergence
Review evidence — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each DNS cutover record and decide whether it verifies readiness-before-switch, the approved procedure and actual client convergence accounting for supplied TTL and cached answers.
  'Restored target: supplied readiness checks pass before switch
Switch: approved DNS procedure
Client checks: cached old answers observed during supplied TTL; later checks establish clients reach restored target
Conclusion: convergence verified from client-target evidence with TTL considered' -> Meets every supplied verification criterion
      feedback: Readiness preceded the approved switch, and actual client-target evidence accounts for caching and TTL.
  'Restored target: supplied readiness checks not yet passing
Switch: performed through approved DNS procedure anyway
Later client checks: reach restored target' -> Does not meet every supplied verification criterion
      feedback: The endpoint switch must wait for passing readiness checks.
  'Restored target: readiness passes before approved switch
DNS setting: new target recorded
Clients: still using cached old answer within supplied TTL
Conclusion: every client immediately converged because the configuration changed' -> Does not meet every supplied verification criterion
      feedback: The setting change does not prove convergence; client evidence still shows the old target.
  'Restored target: readiness passes
Switch: approved procedure after readiness
DNS configuration: updated
Client-target checks and TTL review: omitted
Conclusion: convergence verified' -> Does not meet every supplied verification criterion
      feedback: Actual client checks accounting for cached answers and TTL are required.
  feedback✔: Your judgement follows the supplied evidence and the required checks.  feedback✘: Recheck the evidence against each required criterion; a partial check is not enough.  hints: ['Separate a changed setting from clients’ actual targets.']  remediation→r02
  MEASURES: A:verify_clients_reach_restored_target_after_approved_switch(f1,f2); A:account_for_dns_caching_and_ttl_in_client_convergence_checks(f3)   anchors=['practice', 'assessment:verify_clients_reach_restored_target_after_approved_switch', 'assessment:account_for_dns_caching_and_ttl_in_client_convergence_checks']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s04 · recap · Keep these distinctions
Takeaways — 
(takeaway) Confirm restored-target readiness before the approved endpoint switch. Verify clients actually reach the restored target afterward. For DNS, account for cached answers and TTL rather than assuming an immediate universal switch. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: verify endpoint convergence
(definition) For DNS cutover, account for cached answers and TTL when testing client convergence rather than assuming every client immediately uses the new endpoint. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast the changed DNS setting with clients’ actual targets. Cached answers can persist; verify convergence with the supplied TTL in view. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Review: verify endpoint convergence
(definition) Recovery procedures include restoring service and directing clients to the recovered environment. Confirm the restored target’s supplied readiness checks pass, perform the approved DNS or application endpoint switch and verify clients reach the restored target. For DNS cutover, account for cached answers and TTL when testing client convergence rather than assuming every client immediately uses the new endpoint. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast the changed DNS setting with clients’ actual targets. Cached answers can persist; verify convergence with the supplied TTL in view. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧