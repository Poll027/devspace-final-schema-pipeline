# EVALUATOR PACKET — Bound retries and verify capture (aws_devops.tile.117)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.handle_failed_event_delivery_with_bounded_retries_and_failure_capture — Handle failed event delivery with bounded retries and failure capture

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s04 · hands_on · Review bound retries and verify capture
Review evidence — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · hands_on · Review observe the ecs rollout
Review evidence — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · hands_on · Review promote one built artifact
Review evidence — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s04 · hands_on · Review separate usage time from report time
Review evidence — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · hands_on · Review test the state access boundary
Review evidence — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
[VIDEO ] bridge-before:  | bridge-after: 

### s04 · check · What does contention establish?
Check — Read the supplied question and choose the conclusion supported by the evidence.

### s05 · check · Is locking an access boundary?
Check — Read the supplied question and choose the conclusion supported by the evidence.

### s06 · hands_on · Review verify lock contention
Review evidence — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · hands_on · Review wait for authorized approval
Review evidence — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s04 · hands_on · Review stay within the runbook
Review evidence — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s04 · hands_on · Calculate recovery time and data loss
Review evidence — Using the supplied rehearsal timestamps and recovered data markers, calculate the elapsed time from disruption start to passing service-readiness checks and the gap between the latest recovered data point and disruption. Compare these measurements independently with the supplied RTO and RPO.

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

=========

# EVALUATOR PACKET — Connect evidence to prevention (aws_devops.tile.126)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.document_incident_evidence_and_a_preventive_change — Document incident evidence and a preventive change using reused systematic-debugging coverage

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
[VIDEO ] bridge-before:  | bridge-after: 

### s04 · check · Is prevention justified by evidence?
Check — Read the supplied question and choose the conclusion supported by the evidence.

### s05 · hands_on · Document the supported follow-up
Review evidence — Use the supplied incident evidence to write a factual timeline, a separately supported causal conclusion and one accountable preventive action.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · hands_on · Review verify endpoint convergence
Review evidence — Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.

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