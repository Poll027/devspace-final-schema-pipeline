# EVALUATOR PACKET — Inject a controlled failure and verify alarm behavior (aws_devops.tile.089)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.inject_a_controlled_failure_and_verify_alarm_behavior — Inject a controlled failure and verify alarm behavior

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.inject_a_controlled_failure_and_verify_alarm_behavior)   objective: Verify alarm behavior under controlled failure
A.f1: Controlled failure experiments test how a system behaves under disruption rather than merely inspecting its configuration.   [sources: aws_wa_devops_guidance#qa.nt.6-experiment-with-failure-using-resilience-testing-to-build-recovery-preparedness.html]
A.f2: Define the approved fault, limited scope, expected signals and abort conditions before injecting the sandbox failure.   [sources: aws_wa_devops_guidance#qa.nt.6-experiment-with-failure-using-resilience-testing-to-build-recovery-preparedness.html]
A.f3: Observe alarm state history and receipt of the expected notification during the fault, then remove the fault and verify recovery.   [sources: aws_cloudwatch_user_guide#Notify_Users_Alarm_Changes.html]
note: Use approved fault and supplied abort conditions; do not invent failure-injection commands.
PRACTICE ANCHOR (tool_simulation): Use a supplied sandbox simulation to inject one approved failure and observe the supplied alarm's response. Before injection, record the approved fault, limited target scope, expected signals and supplied abort conditions.  SUCCESS: Stay within the approved scope and abort conditions. Record the alarm state history and whether the expected notification actually arrives. Remove the fault using the supplied control and record the recovery check result. Preserve missing signals, absent notifications or unsuccessful recovery as test outcomes rather than claiming success.
ASSESSMENT ANCHOR: verify_fault_induced_alarm_transition_and_notification_receipt facts=['f1', 'f3']
ASSESSMENT ANCHOR: define_approved_fault_scope_signals_and_abort_conditions facts=['f2']
ASSESSMENT ANCHOR: verify_recovery_after_fault_removal facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Approval stop; Audit evidence; Audit evidence integrity; Audit storage retention; Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template; directly require the native EC2 instance foundation; Backend configuration; Block release on actionable dependency or image security findings; Credential readiness; Diagnose a failed delivery pipeline action; Perform a Lambda version-and-alias release with rollback; Perform a managed EKS Deployment rollout; Perform an EC2 blue/green deployment with CodeDeploy; Perform cleanup after supplied-script failure; Reconcile Terraform EC2 drift; directly require the native EC2 instance foundation; Rehearsal isolation; Replacement controls; Reuse a supplied Terraform module provisioning EC2; directly require the native EC2 instance foundation; Rightsize a resource using a supplied workload baseline; Route a security finding with evidence to its responsible owner; Route an operational event to a notification or established Systems Manager action; Run an ECS service with a desired task count; Run supplied unit and integration tests as blocking pipeline gates after external testing preparation; Safe teardown; Submit small re

## LESSON, in learner order

### s01 · explainer · Operating model
Understand — 
(mechanism) Configuration alone does not demonstrate behavior under disruption. Before the approved sandbox fault, define its limited scope, expected signals and abort conditions. During the fault, inspect alarm state history and actual notification receipt. Then remove the fault and verify recovery. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3⟧
[DIAGRAM: Illustrative sandbox record — observations, not live evidence] nodes=['Before injection: approved sandbox fault; limited target scope; expected alarm and notification; abort conditions recorded', 'Fault active: alarm state history shows ALARM; expected recipient receipt recorded', 'Fault removed: recovery check passed'] edges=[('n1', 'n2', None), ('n2', 'n3', None)] alt: Illustrative sandbox observations, not live evidence. Before injection: approved sandbox fault; limited target scope; expected alarm and notification; abort conditions recorded; Fault active: alarm state history shows ALARM; expected recipient receipt recorded; Fault removed: recovery check passed

### s02 · explainer · Keep the evidence distinct
Understand — 
(example) Keep the sandbox record in order: approved limits, fault, alarm behavior, notification receipt, then recovery. An absent notification is a result to preserve, not a successful test inferred from configuration. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧
(example) If an abort condition is reached, follow the approved stop path. Do not extend the fault to obtain a desired alarm. Retain missed signals, absent notifications and unsuccessful recovery honestly; this exercise does not authorize production disruption. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · check · Review the fault-test record
Check your understanding — Read the supplied excerpt(s) in this step and decide which are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] Record: approved fault removed using the supplied control; post-removal recovery check reports recovered; alarm configuration still exists; notification arrived during the fault. Which observation verifies recovery?
  ✔ o1: The supplied post-removal recovery check reports that the system recovered.
      why: Recovery must be checked after removing the fault.
  ✘ o2: The alarm configuration still exists.
      why: Configuration does not verify recovery after fault removal.
  ✘ o3: The expected notification arrived during the fault, so no recovery check is needed.
      why: Notification receipt during the fault and recovery after removal are separate observations.
  feedback✔: Recovery must be checked after removing the fault.  feedback✘: Review why each alternative fails the specific verification requirement.  hints: ['Compare the recorded observations with every criterion in the question.']  remediation→r01
  MEASURES: A:verify_recovery_after_fault_removal(f3)   anchors=['assessment:verify_recovery_after_fault_removal']
  taught-before-tested: A.f3←s01

### s04 · hands_on · Review the fault-test record
Review the evidence — Read the supplied excerpt(s) in this step and decide which are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each sandbox experiment record. Decide whether it preserves a bounded, evidence-backed outcome or substitutes an unsupported success claim or unsafe scope change.
  'Approved fault: supplied sandbox disruption; targets: limited approved scope; expected: alarm transition and recipient notification; abort: supplied stop condition.
Fault injected within limits. Alarm history: transition observed. Recipient receipt: absent. Fault removed with supplied control. Recovery check: recovered. Outcome: notification missing; do not claim full success.' -> Meets the stated verification criteria
      feedback: This record respects limits, records actual receipt and recovery, and preserves the missing notification honestly.
  'Approved limits and fault followed. Alarm history: transition observed. Recipient receipt: absent. Fault removed. Recovery check: unsuccessful. Outcome: successful because the alarm was configured.' -> Fails at least one stated criterion
      feedback: Configuration cannot override absent receipt or unsuccessful recovery; preserve those outcomes.
  'Before injection: abort conditions not recorded. During the fault: supplied stop condition reached; fault extended beyond the approved target scope to obtain an alarm. Recovery check omitted.' -> Fails at least one stated criterion
      feedback: Limits and abort conditions belong before injection; follow the stop path and verify recovery after removal.
  feedback✔: The judgement matches the supplied evidence and verification requirements.  feedback✘: Separate the requested outcome from evidence that it actually occurred; check the approved scope and the missing observations.  hints: ['Compare the recorded observations with every criterion in the question.']  remediation→r02
  MEASURES: A:verify_fault_induced_alarm_transition_and_notification_receipt(f1,f3); A:define_approved_fault_scope_signals_and_abort_conditions(f2)   anchors=['practice', 'assessment:verify_fault_induced_alarm_transition_and_notification_receipt', 'assessment:define_approved_fault_scope_signals_and_abort_conditions']
  taught-before-tested: A.f1←s01; A.f3←s01; A.f2←s01

### s05 · recap · What to carry forward
Takeaways — 
(takeaway) Bound the fault first. Verify alarm history, actual notification receipt and recovery. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Perform a Lambda version-and-alias release with rollback

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast: evidence versus assumption
(definition) Observe alarm state history and receipt of the expected notification during the fault, then remove the fault and verify recovery. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Alarm configuration is not proof of notification receipt or recovery. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Contrast: evidence versus assumption
(definition) Controlled failure experiments test how a system behaves under disruption rather than merely inspecting its configuration. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Define the approved fault, limited scope, expected signals and abort conditions before injecting the sandbox failure. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Observe alarm state history and receipt of the expected notification during the fault, then remove the fault and verify recovery. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Alarm configuration is not proof of notification receipt or recovery. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Try this distinction
· remediation_steps.eyebrow: Try this distinction

=========

# EVALUATOR PACKET — Perform a Lambda version-and-alias release with rollback / Perform a managed EKS Deployment rollout / Perform an EC2 blue/green deployment with CodeDeploy (aws_devops.tile.090)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.perform_a_lambda_version_and_alias_release_with_rollback — Perform a Lambda version-and-alias release with rollback
B = aws_devops.perform_a_managed_eks_deployment_rollout — Perform a managed EKS Deployment rollout
C = aws_devops.perform_an_ec2_blue_green_deployment_with_codedeploy — Perform an EC2 blue/green deployment with CodeDeploy

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.perform_a_lambda_version_and_alias_release_with_rollback)   objective: Release a Lambda version through an alias
A.f1: A published Lambda version is an immutable snapshot of function code and most configuration.   [sources: aws_lambda_developer_guide#configuration-versions.html]
A.f2: A Lambda alias points to a published version and can be updated to direct invocations to a different version.   [sources: aws_lambda_developer_guide#configuration-aliases.html]
A.f3: Use aws lambda publish-version --function-name NAME, then aws lambda update-alias --function-name NAME --name ALIAS --function-version VERSION; invoke NAME:ALIAS through the supplied test and roll back by updating the alias to the approved previous version.   [sources: aws_lambda_developer_guide#configuration-aliases.html, aws_lambda_developer_guide#configuration-versions.html]
note: Use supplied test; do not introduce weighted aliases, concurrency or application code changes.
PRACTICE ANCHOR (live_code): Publish one version of the supplied Lambda function, switch the supplied alias to the approved published version, verify NAME:ALIAS through the supplied test, and demonstrate rollback to the approved previous version.  SUCCESS: The recorded alias targets show the approved previous version before release, the newly approved version after release, and the approved previous version after rollback. The supplied test targets NAME:ALIAS and confirms the expected result after both alias updates.
ASSESSMENT ANCHOR: distinguish_immutable_version_from_movable_alias facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_alias_invokes_approved_version facts=['f2', 'f3']
ASSESSMENT ANCHOR: restore_and_verify_previous_alias_target facts=['f2', 'f3']

## SOURCE FACTS — B (aws_devops.perform_a_managed_eks_deployment_rollout)   objective: Perform an EKS Deployment rollout
B.f1: Changing a Deployment’s Pod template creates a new rollout revision; scaling alone does not create a new template revision.   [sources: kubernetes_overview#../workloads/controllers/deployment/]
B.f2: Use kubectl set image deployment/NAME CONTAINER=IMAGE to update the supplied image and kubectl rollout status deployment/NAME to monitor rollout.   [sources: kubernetes_overview#../workloads/controllers/deployment/]
B.f3: On the controlled failure, inspect rollout history and use kubectl rollout undo deployment/NAME --to-revision=REVISION to restore the approved prior revision and verify readiness.   [sources: kubernetes_overview#../workloads/controllers/deployment/]
note: Use supplied cluster access and history/readiness procedure; do not introduce self-managed cluster administration.
PRACTICE ANCHOR (tool_simulation): Using supplied cluster access, Deployment and container names, image, and history/readiness procedure, update one Deployment image with kubectl set image and monitor its rollout. In the seeded failure case, inspect history, restore the approved prior revision with kubectl rollout undo --to-revision, and verify readiness within the supplied test bounds.  SUCCESS: The image update targets only the supplied Deployment and container. Rollout status is checked, the failed revision and approved prior revision are distinguished using the supplied history procedure, and the explicit approved revision is restored. The supplied readiness check confirms the restored Deployment is ready; acceptance of the undo request alone does not count as success.
ASSESSMENT ANCHOR: distinguish_template_revision_changes_from_scaling facts=['f1']
ASSESSMENT ANCHOR: verify_deployment_rollout_status facts=['f2']
ASSESSMENT ANCHOR: restore_approved_prior_revision_and_verify_readiness facts=['f3']

## SOURCE FACTS — C (aws_devops.perform_an_ec2_blue_green_deployment_with_codedeploy)   objective: Perform EC2 blue/green deployment with CodeDeploy
C.f1: An EC2 blue/green deployment installs a revision on replacement instances before rerouting traffic from the original instances.   [sources: aws_codedeploy_user_guide#deployment-groups-create-blue-green.html]
C.f2: Use the supplied blue/green deployment group, replacement fleet and load balancer configuration and verify lifecycle and health evidence before the approved traffic rerouting.   [sources: aws_codedeploy_user_guide#deployment-groups-create-blue-green.html]
C.f3: Use the supplied rollback configuration or redeployment procedure and verify traffic and application behavior return to the known-good revision.   [sources: aws_codedeploy_user_guide#deployments-rollback-and-redeploy.html]
note: Use supplied fleet and rollback procedure; avoid absolute availability promises.
PRACTICE ANCHOR (tool_simulation): Run one supplied EC2 blue/green deployment using the supplied deployment group, replacement fleet and load balancer configuration, then perform the supplied controlled rollback check.  SUCCESS: Replacement-instance revision installation, lifecycle and health evidence are verified before the approved traffic switch. Client-visible behavior confirms the traffic outcome and expected revision after switching. The supplied rollback/redeployment procedure is followed, and separate observations verify the traffic destination, known-good revision and application behavior according to that procedure.
ASSESSMENT ANCHOR: verify_healthy_replacement_before_traffic_rerouting facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_rollback_restores_known_good_revision_and_behavior facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Approval stop; Audit evidence; Audit evidence integrity; Audit storage retention; Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template; directly require the native EC2 instance foundation; Backend configuration; Block release on actionable dependency or image security findings; Credential readiness; Diagnose EC2 or container health failures using telemetry and prepared Linux inspection skills; Diagnose a failed delivery pipeline action; Gate release completion on a deployed-service smoke check; Handle failed event delivery with bounded retries and failure capture; Perform a managed EKS Deployment rollout; Perform an EC2 blue/green deployment with CodeDeploy; Perform cleanup after supplied-script failure; Reconcile Terraform EC2 drift; directly require the native EC2 instance foundation; Rehearsal isolation; Replacement controls; Reuse a supplied Terraform module provisioning EC2; directly require the native EC2 instance foundation; Rightsize a resource using a supplied workload baseline; Route a security finding with evidence to its responsible owner; Route an operational event to a notification or established Systems Manager action; Run an ECS 

## LESSON, in learner order

### s01 · explainer · Operating model
Understand — 
(mechanism) A published Lambda version freezes function code and most configuration. The alias is movable: it selects a published version for invocations. Use aws lambda publish-version --function-name NAME, then aws lambda update-alias --function-name NAME --name ALIAS --function-version VERSION. Test NAME:ALIAS. For rollback, point the alias at the approved previous version and repeat verification. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3⟧
[BEFORE_AFTER] The alias target moves; published snapshots do not change.
  before:
[DIAGRAM: Illustrative state: Before] nodes=['Before: ALIAS → approved previous published version; NAME:ALIAS test returns the expected previous-version result', 'Same published snapshots throughout: approved previous version unchanged; newly approved version unchanged'] edges=[('n1', 'n2', None)] alt: Illustrative release record, not live evidence. Before: ALIAS → approved previous published version; NAME:ALIAS test returns the expected previous-version result; Same published snapshots throughout: approved previous version unchanged; newly approved version unchanged
  after:
[DIAGRAM: Illustrative states: Released and Rolled back] nodes=['Released: ALIAS → newly approved published version; NAME:ALIAS test returns the expected new-version result', 'Same published snapshots throughout: approved previous version unchanged; newly approved version unchanged', 'Rolled back: ALIAS → approved previous published version; NAME:ALIAS test returns the expected previous-version result', 'Same published snapshots throughout: approved previous version unchanged; newly approved version unchanged'] edges=[('n1', 'n2', None), ('n2', 'n3', None), ('n3', 'n4', None)] alt: Illustrative release and rollback record, not live evidence. Released: ALIAS → newly approved published version; NAME:ALIAS test returns the expected new-version result; Same published snapshots throughout: approved previous version unchanged; newly approved version unchanged; Rolled back: ALIAS → approved previous published version; NAME:ALIAS test returns the expected previous-version result; Same published snapshots throughout: approved previous version unchanged; newly approved version unchanged

### s02 · explainer · Keep the evidence distinct
Understand — 
(example) Record the alias target before release, after release and after rollback. The supplied NAME:ALIAS test checks the version selected by that alias; an unqualified function invocation is not that test. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧
(example) Rollback changes the alias target, not the immutable published snapshot. Inspect the target and repeat the supplied result check for the approved previous version. A version captures most configuration, not every possible configuration property. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · check · Review the alias release and rollback
Check your understanding — Read the supplied excerpt(s) in this step and decide which are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] Release record: published versions 7 and 8 retain their original code and configuration snapshots. Alias LIVE initially targets version 7, then targets version 8 after an alias update. Which statement correctly explains this record?
  ✘ o1: Rollback edits the code inside the previously published version.
      why: Rollback moves the alias; it does not rewrite an immutable published snapshot.
  ✘ o2: An alias is an immutable snapshot, while the published version is the movable pointer.
      why: This reverses the roles: the alias is movable and the version is immutable.
  ✔ o3: The published version is an immutable snapshot; the alias can move between published versions.
      why: The version freezes code and most configuration; the alias selects the invocation target.
  feedback✔: The version freezes code and most configuration; the alias selects the invocation target.  feedback✘: Review why each alternative fails the specific verification requirement.  hints: ['Compare the recorded observations with every criterion in the question.']  remediation→r01
  MEASURES: A:distinguish_immutable_version_from_movable_alias(f1,f2)   anchors=['assessment:distinguish_immutable_version_from_movable_alias']
  taught-before-tested: A.f1←s01; A.f2←s01

### s04 · hands_on · Review the alias release and rollback
Review the evidence — Read the supplied excerpt(s) in this step and decide which are correct, defective or unsafe.
QUESTION [classify, core, grading=client] Read each Lambda release-and-rollback transcript. Decide whether it verifies both approved alias updates using the alias-qualified test.
  'Approved previous: PREVIOUS; approved new: NEW. Version NEW published; ALIAS moves PREVIOUS -> NEW -> PREVIOUS. Both checks invoke unqualified NAME. Record says alias verification complete.' -> Fails at least one stated criterion
      feedback: The supplied verification must target NAME:ALIAS; an unqualified invocation does not verify the alias target.
  'Approved previous: PREVIOUS; new: NEW. Before: ALIAS -> PREVIOUS. After release: ALIAS -> NEW; NAME:ALIAS test confirms NEW. Rollback request accepted; no alias-target observation or post-rollback result check.' -> Fails at least one stated criterion
      feedback: Rollback needs the restored target observation and the alias-qualified test result, not only request acceptance.
  'Approved previous version: PREVIOUS; approved new version: NEW.
Before: ALIAS -> PREVIOUS.
aws lambda publish-version --function-name NAME
Result: NEW
aws lambda update-alias --function-name NAME --name ALIAS --function-version NEW
After release: ALIAS -> NEW; supplied test invokes NAME:ALIAS; expected NEW result confirmed.
aws lambda update-alias --function-name NAME --name ALIAS --function-version PREVIOUS
After rollback: ALIAS -> PREVIOUS; supplied test invokes NAME:ALIAS; expected PREVIOUS result confirmed.' -> Meets the stated verification criteria
      feedback: The targets are recorded before, after release and after rollback, with alias-qualified result checks after both updates.
  feedback✔: The judgement matches the supplied evidence and verification requirements.  feedback✘: Separate the requested outcome from evidence that it actually occurred; check the approved scope and the missing observations.  hints: ['Compare the recorded observations with every criterion in the question.']  remediation→r02
  MEASURES: A:verify_alias_invokes_approved_version(f2,f3); A:restore_and_verify_previous_alias_target(f2,f3)   anchors=['practice', 'assessment:verify_alias_invokes_approved_version', 'assessment:restore_and_verify_previous_alias_target']
  taught-before-tested: A.f2←s01; A.f3←s01; A.f2←s01; A.f3←s01

### s05 · explainer · Operating model
Understand — 
(mechanism) A Deployment Pod-template change creates a rollout revision; scaling alone does not. Update the supplied image with kubectl set image deployment/NAME CONTAINER=IMAGE and monitor kubectl rollout status deployment/NAME. On the controlled failure, inspect rollout history, restore the approved prior revision with kubectl rollout undo deployment/NAME --to-revision=REVISION, and verify readiness. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3⟧
[DIAGRAM: Illustrative terminal-state sequence — schematic, not computed output] nodes=['kubectl set image deployment/NAME CONTAINER=IMAGE — supplied image update accepted', 'kubectl rollout status deployment/NAME — controlled rollout failure observed', 'kubectl rollout history deployment/NAME — approved prior REVISION identified', 'kubectl rollout undo deployment/NAME --to-revision=REVISION — rollback requested', 'Post-rollback readiness check — restored Deployment meets the supplied readiness requirement'] edges=[('n1', 'n2', None), ('n2', 'n3', None), ('n3', 'n4', None), ('n4', 'n5', None)] alt: Schematic states, not computed terminal output. kubectl set image deployment/NAME CONTAINER=IMAGE — supplied image update accepted; kubectl rollout status deployment/NAME — controlled rollout failure observed; kubectl rollout history deployment/NAME — approved prior REVISION identified; kubectl rollout undo deployment/NAME --to-revision=REVISION — rollback requested; Post-rollback readiness check — restored Deployment meets the supplied readiness requirement

### s06 · explainer · Keep the evidence distinct
Understand — 
(example) Keep the failed revision evidence separate from the approved rollback revision. Use the supplied procedure to select the authorized prior revision, rather than choosing an arbitrary history entry. ⟦B.f1 B.f2 B.f3 B:tb4 B:tb5⟧
(example) After undo, inspect readiness. An accepted undo request is not evidence that the restored template’s Pods satisfy the supplied readiness check. Scaling changes alone do not create a new Pod-template revision. ⟦B.f1 B.f2 B.f3 B:tb4 B:tb5⟧

### s07 · check · Review the rollout and readiness evidence
Check your understanding — Read the supplied excerpt(s) in this step and decide which are correct, defective or unsafe.
QUESTION [choice, core, grading=client] Deployment record: scaling replicas from 2 to 3 leaves the Pod template and revision unchanged. Updating the container image changes the Pod template and produces a new revision. A subsequent status check makes no template change. Which recorded action created the new rollout revision?
  ✘ o1: Checking rollout status without changing the Pod template.
      why: A status check observes the rollout; it is not a Pod-template change.
  ✔ o2: Updating the container image in the Pod template.
      why: A Pod-template change creates a new rollout revision.
  ✘ o3: Scaling the number of replicas without changing the Pod template.
      why: Scaling alone does not create a new template revision.
  feedback✔: A Pod-template change creates a new rollout revision.  feedback✘: Review why each alternative fails the specific verification requirement.  hints: ['Compare the recorded observations with every criterion in the question.']  remediation→r03
  MEASURES: B:distinguish_template_revision_changes_from_scaling(f1)   anchors=['assessment:distinguish_template_revision_changes_from_scaling']
  taught-before-tested: B.f1←s05

### s08 · hands_on · Review the rollout and readiness evidence
Review the evidence — Read the supplied excerpt(s) in this step and decide which are correct, defective or unsafe.
QUESTION [classify, core, grading=client] Read each EKS rollout record. Decide whether it verifies the supplied image update and explicit approved rollback, including readiness.
  'Supplied image update and status checked. History distinguishes FAILED from approved REVISION. Undo to REVISION accepted. No readiness observation; record says rollback verified.' -> Fails at least one stated criterion
      feedback: Acceptance of undo alone is not the required readiness verification.
  'Supplied target: deployment/NAME, container CONTAINER, image IMAGE.
kubectl set image deployment/NAME CONTAINER=IMAGE
kubectl rollout status deployment/NAME
Controlled failure observed. Supplied history: failed revision FAILED; approved prior revision REVISION.
kubectl rollout undo deployment/NAME --to-revision=REVISION
Restored revision: REVISION. Supplied readiness check: ready.' -> Meets the stated verification criteria
      feedback: The record targets only the supplied image update, distinguishes revisions, restores the approved revision and verifies readiness.
  'Image update targets deployment/NAME and CONTAINER=IMAGE; rollout status and history checked. History identifies approved prior REVISION and another unapproved prior OTHER. Undo targets OTHER; readiness reports ready.' -> Fails at least one stated criterion
      feedback: A ready unapproved history entry is not the explicit approved prior revision.
  feedback✔: The judgement matches the supplied evidence and verification requirements.  feedback✘: Separate the requested outcome from evidence that it actually occurred; check the approved scope and the missing observations.  hints: ['Compare the recorded observations with every criterion in the question.']  remediation→r04
  MEASURES: B:verify_deployment_rollout_status(f2); B:restore_approved_prior_revision_and_verify_readiness(f3)   anchors=['practice', 'assessment:verify_deployment_rollout_status', 'assessment:restore_approved_prior_revision_and_verify_readiness']
  taught-before-tested: B.f2←s05; B.f3←s05

### s09 · explainer · Operating model
Understand — 
(mechanism) EC2 blue/green installs a revision on replacement instances before traffic leaves the original instances. Use the supplied deployment group, replacement fleet and load balancer configuration. Check lifecycle and health evidence before approved rerouting. For rollback, follow the supplied configuration or redeployment procedure and verify both traffic and application behavior return to the known-good revision. ⟦C.f1 C.f2 C.f3 C:tb1 C:tb2 C:tb3⟧
[PROCESS_FLOW] nodes=['Original fleet serves traffic', 'Install revision on supplied replacement fleet', 'Verify replacement lifecycle and health evidence', 'Approved load balancer traffic rerouting', 'Verify client traffic and application behavior', 'Supplied rollback/redeployment path: verify known-good traffic and behavior'] edges=[('n1', 'n2', None), ('n2', 'n3', None), ('n3', 'n4', None), ('n4', 'n5', None), ('n5', 'n6', None)] alt: Original fleet serves traffic; Install revision on supplied replacement fleet; Verify replacement lifecycle and health evidence; Approved load balancer traffic rerouting; Verify client traffic and application behavior; Supplied rollback/redeployment path: verify known-good traffic and behavior

### s10 · explainer · Keep the evidence distinct
Understand — 
(example) Installation evidence shows the replacement revision is present; it does not show which fleet clients reach. Preserve lifecycle and health evidence before the approved traffic switch. ⟦C.f1 C.f2 C.f3 C:tb4 C:tb5⟧
(example) After the switch and after rollback, check client-visible behavior as well as traffic. Rerouting alone does not establish correct application behavior. Follow the supplied rollback path; do not infer automatic rollback or guaranteed zero disruption. ⟦C.f1 C.f2 C.f3 C:tb4 C:tb5⟧

### s11 · check · Review the fleet and traffic evidence
Check your understanding — Read the supplied excerpt(s) in this step and decide which are correct, defective or unsafe.
QUESTION [choice, core, grading=client] Rollback record: the supplied procedure completed; traffic reaches the procedure-designated destination; the known-good revision is confirmed; the supplied application-behavior check passes. The record also includes an accepted rollback request and installation evidence from before the original switch. Which option identifies the evidence that verifies this rollback?
  ✔ o1: The supplied rollback procedure is followed, and traffic destination, revision and application behavior are verified.
      why: Rollback requires evidence of the traffic and behavior returning to the known-good revision.
  ✘ o2: A rollback request was accepted, with no traffic or application check.
      why: Request acceptance is not verification of the resulting traffic or application behavior.
  ✘ o3: The replacement revision was installed before the original traffic switch.
      why: Installation before the switch does not verify a later rollback outcome.
  feedback✔: Rollback requires evidence of the traffic and behavior returning to the known-good revision.  feedback✘: Review why each alternative fails the specific verification requirement.  hints: ['Compare the recorded observations with every criterion in the question.']  remediation→r05
  MEASURES: C:verify_rollback_restores_known_good_revision_and_behavior(f3)   anchors=['assessment:verify_rollback_restores_known_good_revision_and_behavior']
  taught-before-tested: C.f3←s09

### s12 · hands_on · Review the fleet and traffic evidence
Review the evidence — Read the supplied excerpt(s) in this step and decide which are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each EC2 blue/green record. Decide whether it verifies replacement readiness before traffic switching and verifies the traffic, revision and behavior outcomes after switching and rollback.
  'Supplied deployment group, replacement fleet and load balancer used. Replacement revision installed; lifecycle passed; health passed before approved traffic switch. After switch: traffic reaches replacement fleet; expected revision and client-visible behavior confirmed. Supplied rollback/redeployment procedure followed. After rollback: traffic reaches procedure-designated known-good destination; known-good revision confirmed; application behavior passes supplied check.' -> Meets the stated verification criteria
      feedback: Installation, lifecycle and health precede switching; separate traffic, revision and behavior evidence verifies both outcomes.
  'Supplied deployment group, fleet and load balancer used. Traffic switched before replacement lifecycle and health evidence was checked. Afterward health passed. Rollback procedure and final traffic, known-good revision and behavior were verified.' -> Fails at least one stated criterion
      feedback: Healthy evidence must be verified before the approved switch, not retroactively after rerouting.
  'Replacement installation, lifecycle and health verified before approved switch; post-switch traffic, revision and behavior verified. Supplied rollback requested; record contains no post-rollback traffic, revision or behavior observations and calls rollback successful.' -> Fails at least one stated criterion
      feedback: The request does not verify return of traffic and application behavior to the known-good revision.
  feedback✔: The judgement matches the supplied evidence and verification requirements.  feedback✘: Separate the requested outcome from evidence that it actually occurred; check the approved scope and the missing observations.  hints: ['Compare the recorded observations with every criterion in the question.']  remediation→r06
  MEASURES: C:verify_healthy_replacement_before_traffic_rerouting(f1,f2); C:verify_rollback_restores_known_good_revision_and_behavior(f3)   anchors=['practice', 'assessment:verify_healthy_replacement_before_traffic_rerouting', 'assessment:verify_rollback_restores_known_good_revision_and_behavior']
  taught-before-tested: C.f1←s09; C.f2←s09; C.f3←s09

### s13 · recap · What to carry forward
Takeaways — 
(takeaway) Lambda rollback moves the alias to an approved previous immutable version; repeat the alias test. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) EKS rollback restores an approved template revision; verify readiness. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(takeaway) EC2 blue/green needs replacement health evidence before traffic moves, plus verified known-good behavior after rollback. ⟦C.f1 C.f2 C.f3 C:tb1 C:tb2 C:tb3 C:tb4 C:tb5⟧
[UP NEXT] Up next: Perform cleanup after supplied-script failure

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast: evidence versus assumption
(definition) A published Lambda version is an immutable snapshot of function code and most configuration. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) A Lambda alias points to a published version and can be updated to direct invocations to a different version. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) Changing the alias target is not editing the published version. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Contrast: evidence versus assumption
(definition) A Lambda alias points to a published version and can be updated to direct invocations to a different version. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Use aws lambda publish-version --function-name NAME, then aws lambda update-alias --function-name NAME --name ALIAS --function-version VERSION; invoke NAME:ALIAS through the supplied test and roll back by updating the alias to the approved previous version. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Changing the alias target is not editing the published version. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
### r03 · Contrast: evidence versus assumption
(definition) Changing a Deployment’s Pod template creates a new rollout revision; scaling alone does not create a new template revision. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(misconception) An undo request is not the same as verified readiness. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
### r04 · Contrast: evidence versus assumption
(definition) Use kubectl set image deployment/NAME CONTAINER=IMAGE to update the supplied image and kubectl rollout status deployment/NAME to monitor rollout. ⟦B.f2 B:tb3 B:tb4⟧
(definition) On the controlled failure, inspect rollout history and use kubectl rollout undo deployment/NAME --to-revision=REVISION to restore the approved prior revision and verify readiness. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) An undo request is not the same as verified readiness. ⟦B.f2 B.f3 B:tb3 B:tb4 B:tb5⟧
### r05 · Contrast: evidence versus assumption
(definition) Use the supplied rollback configuration or redeployment procedure and verify traffic and application behavior return to the known-good revision. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
(misconception) Installation evidence is not client traffic or application-behavior evidence. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
### r06 · Contrast: evidence versus assumption
(definition) An EC2 blue/green deployment installs a revision on replacement instances before rerouting traffic from the original instances. ⟦C.f1 C:tb2 C:tb4 C:tb5⟧
(definition) Use the supplied blue/green deployment group, replacement fleet and load balancer configuration and verify lifecycle and health evidence before the approved traffic rerouting. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
(definition) Use the supplied rollback configuration or redeployment procedure and verify traffic and application behavior return to the known-good revision. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
(misconception) Installation evidence is not client traffic or application-behavior evidence. ⟦C.f1 C.f2 C.f3 C:tb2 C:tb3 C:tb4 C:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Try this distinction
· remediation_steps.eyebrow: Try this distinction
· remediation_steps.eyebrow: Try this distinction
· remediation_steps.eyebrow: Try this distinction
· remediation_steps.eyebrow: Try this distinction
· remediation_steps.eyebrow: Try this distinction

=========

# EVALUATOR PACKET — Perform cleanup after supplied-script failure (aws_devops.tile.093)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.perform_cleanup_after_supplied_script_failure — Perform cleanup after supplied-script failure

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.perform_cleanup_after_supplied_script_failure)   objective: Clean up after automation failure
A.f1: A Python finally block runs cleanup when control leaves its try block, including when an exception is raised.   [sources: python_tutorial#errors.html#defining-clean-up-actions]
A.f2: Wrap the supplied failing task in try: ... finally: ... and put the supplied scoped cleanup calls in finally.   [sources: python_tutorial#errors.html#defining-clean-up-actions]
A.f3: Track resources created by the exercise and clean up only those resources, then verify their removal and preservation of preexisting resources.   [sources: python_tutorial#errors.html#defining-clean-up-actions]
note: Require external Python preparation; try/finally ellipses are scaffolding, not a runnable task.
PRACTICE ANCHOR (live_code): Wrap one supplied failing automation task in try/finally, placing the supplied scoped cleanup calls in finally and using the tracked exercise-created resource identities.  SUCCESS: The controlled task exception triggers the supplied scoped cleanup calls. The supplied postcheck confirms that exercise-created resources are removed and preexisting resources remain, including any that share a label.
ASSESSMENT ANCHOR: verify_exercise_resource_removal_and_preexisting_resource_preservation facts=['f1', 'f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Approval stop; Audit evidence; Audit evidence integrity; Audit storage retention; Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template; directly require the native EC2 instance foundation; Backend configuration; Block release on actionable dependency or image security findings; Credential readiness; Diagnose EC2 or container health failures using telemetry and prepared Linux inspection skills; Diagnose a failed delivery pipeline action; Gate release completion on a deployed-service smoke check; Handle failed event delivery with bounded retries and failure capture; Perform a controlled ECS service rollout; Reconcile Terraform EC2 drift; directly require the native EC2 instance foundation; Rehearsal isolation; Replacement controls; Reuse a supplied Terraform module provisioning EC2; directly require the native EC2 instance foundation; Rightsize a resource using a supplied workload baseline; Route a security finding with evidence to its responsible owner; Route an operational event to a notification or established Systems Manager action; Run an ECS service with a desired task count; Run supplied unit and integration tests as blocking pipeline gates

## LESSON, in learner order

### s01 · explainer · Operating model
Understand — 
(mechanism) Python finally runs when control leaves try, including after an exception. Put the supplied failing task in try and scoped cleanup calls in finally. Track identities created by this exercise, clean up only those identities, and verify both their removal and preservation of preexisting resources. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3⟧
[CODE python]
try:
    # Supplied failing task; track exercise-created identities.
    pass
finally:
    # Supplied cleanup calls: only tracked exercise-created identities.
    pass
  annotations: ['The supplied task belongs in try; an exception still leads to finally.', 'The supplied cleanup calls must be scoped to tracked exercise-created identities.']
[DIAGRAM: Illustrative exception and postcheck record] nodes=['Supplied task raises the controlled exception in try', 'finally runs supplied cleanup scoped to tracked exercise-created identities', 'Independent postcheck after failure: exercise-created identity removed; preexisting identity with a shared label preserved'] edges=[('n1', 'n2', 'exception path')] alt: Illustrative record, not computed output. The exception leads directly to finally. The postcheck is independent, not ordinary code following an unhandled exception. Supplied task raises the controlled exception in try; finally runs supplied cleanup scoped to tracked exercise-created identities; Independent postcheck after failure: exercise-created identity removed; preexisting identity with a shared label preserved

### s02 · explainer · Keep the evidence distinct
Understand — 
(example) Use the supplied scaffolding and cleanup calls. Track created identities at the exercise boundary instead of reconstructing ownership from similar resource names after failure. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧
(example) A preexisting resource with a shared label must remain untouched. The postcheck must confirm removal of exercise-created resources and preservation of preexisting ones. finally controls when cleanup runs; it does not make an overbroad cleanup safe. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · check · Judge the cleanup scope
Check your understanding — Read the supplied excerpt(s) in this step and decide which are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] Record: tracked exercise-created identity CREATED and preexisting identity PREEXISTING share a label. The controlled task raises an exception; finally calls the supplied cleanup for CREATED. Independent postcheck: CREATED absent; PREEXISTING present. Which option accurately describes why this postcheck demonstrates correctly scoped cleanup?
  ✘ o1: Every identity sharing the exercise label is gone.
      why: Labels do not establish exercise ownership; a preexisting resource sharing the label must remain.
  ✘ o2: The finally block was entered, so no resource postcheck is necessary.
      why: finally controls when cleanup runs; it does not prove correct cleanup scope or removal.
  ✔ o3: Exercise-created identities are removed; preexisting identities remain, including ones sharing a label.
      why: Both removal and preservation must be verified by identity.
  feedback✔: Both removal and preservation must be verified by identity.  feedback✘: Review why each alternative fails the specific verification requirement.  hints: ['Compare the recorded observations with every criterion in the question.']  remediation→r01
  MEASURES: A:verify_exercise_resource_removal_and_preexisting_resource_preservation(f1,f2,f3)   anchors=['assessment:verify_exercise_resource_removal_and_preexisting_resource_preservation']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s04 · hands_on · Judge the cleanup scope
Review the evidence — Read the supplied excerpt(s) in this step and decide which are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each controlled-failure cleanup excerpt and postcheck. Decide whether cleanup runs on the exception and removes only tracked exercise-created identities, preserving preexisting ones even with shared labels.
  'Tracked exercise-created identities: CREATED; PREEXISTING shares the label.
try:
    supplied_failing_task()
    supplied_scoped_cleanup(CREATED)
finally:
    pass
Trace: controlled exception before cleanup. Postcheck: CREATED still present; PREEXISTING remains.' -> Fails at least one stated criterion
      feedback: Cleanup placed after the failing task in try is skipped here; the supplied cleanup belongs in finally.
  'Tracked exercise-created identities: CREATED; PREEXISTING shares the label.
try:
    supplied_failing_task()
finally:
    cleanup_every_identity_with_shared_label()
Trace: controlled exception; cleanup called.
Postcheck: CREATED removed; PREEXISTING also removed.' -> Fails at least one stated criterion
      feedback: finally does not make label-wide deletion safe; the preexisting identity must remain.
  'Tracked exercise-created identities: CREATED; preexisting identity PREEXISTING shares the label.
try:
    supplied_failing_task()
finally:
    supplied_scoped_cleanup(CREATED)
Trace: controlled exception; scoped cleanup called.
Postcheck: CREATED removed; PREEXISTING remains.' -> Meets the stated verification criteria
      feedback: finally triggers the supplied scoped cleanup after the exception; the identity-based postcheck proves both removal and preservation.
  feedback✔: The judgement matches the supplied evidence and verification requirements.  feedback✘: Separate the requested outcome from evidence that it actually occurred; check the approved scope and the missing observations.  hints: ['Compare the recorded observations with every criterion in the question.']
  MEASURES: A:verify_exercise_resource_removal_and_preexisting_resource_preservation(f1,f2,f3)   anchors=['practice', 'assessment:verify_exercise_resource_removal_and_preexisting_resource_preservation']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s05 · recap · What to carry forward
Takeaways — 
(takeaway) Use finally for supplied cleanup, scope it to exercise-created identities, and verify preexisting resources remain. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Reconcile Terraform EC2 drift; directly require the native EC2 instance foundation

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast: evidence versus assumption
(definition) A Python finally block runs cleanup when control leaves its try block, including when an exception is raised. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Wrap the supplied failing task in try: ... finally: ... and put the supplied scoped cleanup calls in finally. ⟦A.f2 A:tb3 A:tb4⟧
(definition) Track resources created by the exercise and clean up only those resources, then verify their removal and preservation of preexisting resources. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) finally guarantees block execution here, not safe target selection. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Try this distinction

=========

# EVALUATOR PACKET — Reconcile Terraform EC2 drift; directly require the native EC2 instance foundation (aws_devops.tile.094)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.reconcile_terraform_ec2_drift — Reconcile Terraform EC2 drift; directly require the native EC2 instance foundation

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.reconcile_terraform_ec2_drift)   objective: Reconcile Terraform EC2 drift
A.f1: Terraform normally refreshes tracked resources before planning, revealing out-of-band changes relevant to the proposed actions.   [sources: terraform_language#../cli/commands/plan]
A.f2: After the supplied drift, compare observed instance settings with configuration and decide whether to restore the declaration or update it to reflect an approved intended change.   [sources: terraform_language#../cli/commands/plan]
A.f3: Generate and inspect a new plan, run the supplied approval/apply workflow and verify live instance settings match the chosen declaration.   [sources: terraform_language#../cli/commands/plan]
A.f4: A refresh-only plan updates state and outputs to reflect remote changes; it does not itself change remote infrastructure to restore configuration.   [sources: terraform_language#../cli/commands/plan]
note: Preserve normally; do not imply refresh discovers every untracked resource or property.
PRACTICE ANCHOR (live_code): Provision one EC2 instance using the supplied approved Terraform configuration and workflow. Introduce the scaffolded out-of-band setting change, compare the observed setting with the declaration and approved requirement, then choose whether to restore the declaration or update it. Generate and inspect a new plan, complete the supplied approval/apply workflow, and verify the live setting against the chosen declaration.  SUCCESS: The initial instance is provisioned through the supplied workflow. The reconciliation choice matches the approved requirement, the new plan reflects that choice, and the workflow completes with the live instance setting matching the chosen declaration. Refresh-only is not treated as remote repair.
ASSESSMENT ANCHOR: choose_declared_ec2_intent_after_drift facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_complete_ec2_drift_reconciliation facts=['f3']
ASSESSMENT ANCHOR: distinguish_refresh_only_from_remote_repair facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Approval stop; Audit evidence; Audit evidence integrity; Audit storage retention; Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template; directly require the native EC2 instance foundation; Backend configuration; Block release on actionable dependency or image security findings; Credential readiness; Diagnose EC2 or container health failures using telemetry and prepared Linux inspection skills; Diagnose a failed delivery pipeline action; Gate release completion on a deployed-service smoke check; Handle failed event delivery with bounded retries and failure capture; Perform a controlled ECS service rollout; Promote the same artifact version across environments; Rehearsal isolation; Replacement controls; Reuse a supplied Terraform module provisioning EC2; directly require the native EC2 instance foundation; Rightsize a resource using a supplied workload baseline; Route a security finding with evidence to its responsible owner; Route an operational event to a notification or established Systems Manager action; Run an ECS service with a desired task count; Run supplied unit and integration tests as blocking pipeline gates after external testing prepa

## LESSON, in learner order

### s01 · explainer · Operating model
Understand — 
(mechanism) Terraform normally refreshes tracked resources before planning, exposing relevant out-of-band changes. Compare observed EC2 settings with configuration and choose an approved intent: restore the declaration or update it. Inspect a new plan, follow the approval/apply workflow, and verify live settings. Refresh-only planning proposes state and output updates; planning does not persist them. Applying the approved refresh-only plan persists those updates without restoring remote infrastructure to configuration. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3⟧
[BEFORE_AFTER] Separate contrast — Refresh-only apply: state/outputs reflect B; live setting remains B
  before:
[DIAGRAM: Before — labelled symbolic example] nodes=['Declaration: setting A', 'Observed live setting: setting B', 'Approved intent: restore A'] edges=[('n1', 'n2', None), ('n2', 'n3', None)] alt: Symbolic example, not live evidence. Declaration: setting A; Observed live setting: setting B; Approved intent: restore A
  after:
[DIAGRAM: After — labelled symbolic example] nodes=['Reviewed plan: change live B → A', 'Approved apply completed', 'Final comparison: declaration A; live A'] edges=[('n1', 'n2', None), ('n2', 'n3', None)] alt: Symbolic example, not live evidence. Reviewed plan: change live B → A; Approved apply completed; Final comparison: declaration A; live A

### s02 · explainer · Keep the evidence distinct
Understand — 
(example) Keep observed drift, approved intent, planned action and the final live comparison together. Accepting a setting requires an approved declaration change; restoring it requires the appropriate reviewed action. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧
(example) Refresh-only planning does not persist state or output changes. Applying its approved plan persists those updates, but does not change the remote instance to repair drift. Verify live settings against the chosen declaration after the supplied workflow. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Review the drift-resolution record
Check your understanding — Read the supplied excerpt(s) in this step and decide which are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] Drift record: declaration ORIGINAL; observed live setting CHANGED; the supplied requirement explicitly approves CHANGED as the intended setting. The proposed reconciliation updates the declaration to CHANGED. Which option explains why that choice is justified?
  ✘ o1: Always restore the old declaration even if an intended change was approved.
      why: The declaration may be updated to reflect an approved intended change.
  ✔ o2: Compare the observed settings and declaration with the approved intended requirement.
      why: The reconciliation choice follows approved intent, not merely whichever setting was observed last.
  ✘ o3: Always accept the observed settings because refresh exposed them.
      why: Refresh reveals drift; it does not approve the observed change as intended.
  feedback✔: The reconciliation choice follows approved intent, not merely whichever setting was observed last.  feedback✘: Review why each alternative fails the specific verification requirement.  hints: ['Compare the recorded observations with every criterion in the question.']  remediation→r01
  MEASURES: A:choose_declared_ec2_intent_after_drift(f1,f2)   anchors=['assessment:choose_declared_ec2_intent_after_drift']
  taught-before-tested: A.f1←s01; A.f2←s01

### s04 · hands_on · Review the drift-resolution record
Review the evidence — Read the supplied excerpt(s) in this step and decide which are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each Terraform drift record. Decide whether it completes reconciliation to approved intent, rather than treating refresh-only as remote repair.
  'Initial provisioning completed. Approved requirement accepts CHANGED; declaration updated to CHANGED; new plan inspected. Approval/apply workflow not completed and no live comparison recorded. Record says editing the declaration completed reconciliation.' -> Fails at least one stated criterion
      feedback: The declaration choice alone is insufficient; complete the workflow and verify the live setting against it.
  'Initial instance provisioned through supplied workflow. Declaration: ORIGINAL; observed drift: CHANGED; approved requirement: restore ORIGINAL. New normal plan inspected: restore remote setting to ORIGINAL. Supplied approval/apply workflow completed. Postcheck: live setting ORIGINAL equals chosen declaration ORIGINAL.' -> Meets the stated verification criteria
      feedback: Approved intent, new plan, completed workflow and live comparison agree.
  'Initial provisioning completed. Declaration ORIGINAL; live CHANGED; approved requirement restore ORIGINAL. Approved refresh-only plan applied: state and outputs reflect CHANGED. Remote remains CHANGED. Record says refresh-only restored ORIGINAL.' -> Fails at least one stated criterion
      feedback: Refresh-only state/output updates do not change remote infrastructure to restore the declaration.
  feedback✔: The judgement matches the supplied evidence and verification requirements.  feedback✘: Separate the requested outcome from evidence that it actually occurred; check the approved scope and the missing observations.  hints: ['Compare the recorded observations with every criterion in the question.']  remediation→r02
  MEASURES: A:identify_complete_ec2_drift_reconciliation(f3); A:distinguish_refresh_only_from_remote_repair(f4)   anchors=['practice', 'assessment:identify_complete_ec2_drift_reconciliation', 'assessment:distinguish_refresh_only_from_remote_repair']
  taught-before-tested: A.f3←s01; A.f4←s01

### s05 · recap · What to carry forward
Takeaways — 
(takeaway) Choose approved intent, inspect a new plan, apply through approval and verify live settings. Refresh-only apply updates state/outputs, not remote infrastructure. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Reuse a supplied Terraform module provisioning EC2; directly require the native EC2 instance foundation

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast: evidence versus assumption
(definition) Terraform normally refreshes tracked resources before planning, revealing out-of-band changes relevant to the proposed actions. ⟦A.f1 A:tb2 A:tb4⟧
(definition) After the supplied drift, compare observed instance settings with configuration and decide whether to restore the declaration or update it to reflect an approved intended change. ⟦A.f2 A:tb3 A:tb4⟧
(misconception) Refresh-only state/output updates are not remote repair. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4⟧
### r02 · Contrast: evidence versus assumption
(definition) Generate and inspect a new plan, run the supplied approval/apply workflow and verify live instance settings match the chosen declaration. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(definition) A refresh-only plan proposes state and output updates to reflect remote changes; planning alone does not persist them. Applying the approved refresh-only plan persists those updates without changing remote infrastructure to restore configuration. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Refresh-only state/output updates are not remote repair. ⟦A.f3 A.f4 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Try this distinction
· remediation_steps.eyebrow: Try this distinction

=========

# EVALUATOR PACKET — Reuse a supplied Terraform module provisioning EC2; directly require the native EC2 instance foundation (aws_devops.tile.095)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.reuse_a_supplied_terraform_module_provisioning_ec2 — Reuse a supplied Terraform module provisioning EC2; directly require the native EC2 instance foundation

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.reuse_a_supplied_terraform_module_provisioning_ec2)   objective: Reuse a Terraform EC2 module
A.f1: A module packages resource declarations behind input variables and output values.   [sources: terraform_language#modules/syntax]
A.f2: Configure module "NAME" with the supplied source and named input arguments; reference its output as module.NAME.OUTPUT.   [sources: terraform_language#modules/syntax]
A.f3: Initialize the module, inspect the input values and planned instance settings, apply through the approved workflow and verify the created instance and declared outputs.   [sources: terraform_language#../cli/run]
note: Use supplied source/interface; do not author a new module or invent output names.
PRACTICE ANCHOR (live_code): Configure one supplied Terraform EC2 module using its documented source and named inputs. Inspect its declared outputs, reference a supplied output name, initialize and review the plan, then apply through the approved sandbox workflow and verify the single instance and outputs against the chosen inputs.  SUCCESS: The configuration uses the supplied module interface without inventing inputs or outputs. The reviewed plan provisions exactly one sandbox EC2 instance with the intended settings, and the created instance and declared outputs agree with the chosen inputs.
ASSESSMENT ANCHOR: verify_supplied_module_input_and_output_contract facts=['f1', 'f2']
ASSESSMENT ANCHOR: compare_module_inputs_with_planned_instance_settings facts=['f2', 'f3']
ASSESSMENT ANCHOR: verify_created_instance_and_declared_outputs facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Approval stop; Audit evidence; Audit evidence integrity; Audit storage retention; Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template; directly require the native EC2 instance foundation; Backend configuration; Block release on actionable dependency or image security findings; Credential readiness; Diagnose EC2 or container health failures using telemetry and prepared Linux inspection skills; Diagnose a failed delivery pipeline action; Gate release completion on a deployed-service smoke check; Handle failed event delivery with bounded retries and failure capture; Perform a controlled ECS service rollout; Promote the same artifact version across environments; Rehearsal isolation; Replacement controls; Residual charge verification; Rightsize a resource using a supplied workload baseline; Route a security finding with evidence to its responsible owner; Route an operational event to a notification or established Systems Manager action; Run an ECS service with a desired task count; Run supplied unit and integration tests as blocking pipeline gates after external testing preparation; Safe teardown; Submit small reviewable infrastructure changes after

## LESSON, in learner order

### s01 · explainer · Operating model
Understand — 
(mechanism) A module packages resource declarations behind inputs and outputs. Configure module "NAME" with the supplied source and named input arguments; reference its declared output as module.NAME.OUTPUT. Initialize the module, inspect inputs and planned instance settings, apply through the approved workflow, then verify the created instance and declared outputs. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) The supplied module interface is not proof that its input values are correct. Compare inputs and planned EC2 settings with the approved requirement before apply. Keep the declared output tied to the verified instance rather than treating an output reference as live verification. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[CODE bash]
# Interface schematic, not a shell command:
# module "NAME" {
#   source = <supplied source>
#   <named input argument> = <supplied value>
# }
# module.NAME.OUTPUT
  annotations: ['Use the supplied source and named inputs; inspect the planned EC2 settings.', 'Reference the declared output and verify it with the created instance after approved apply.']

### s02 · check · Review the module interface and verification
Check your understanding — Read the supplied excerpt(s) in this step and decide which are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] Module record: initialization completed; the reviewed plan specifies one sandbox instance with the chosen inputs; approved apply completed; the created instance settings match those inputs; declared outputs agree with that instance. Which recorded evidence completes post-apply verification?
  ✔ o1: The created instance settings and declared outputs agree with the chosen inputs.
      why: The created instance and declared outputs require post-apply verification.
  ✘ o2: The configuration contains an output reference, so the live instance needs no check.
      why: An output reference is not live instance verification.
  ✘ o3: Initialization completed, so no plan or created-instance comparison is needed.
      why: Initialization does not replace review of settings or verification of the created instance.
  feedback✔: The created instance and declared outputs require post-apply verification.  feedback✘: Review why each alternative fails the specific verification requirement.  hints: ['Compare the recorded observations with every criterion in the question.']  remediation→r01
  MEASURES: A:verify_created_instance_and_declared_outputs(f3)   anchors=['assessment:verify_created_instance_and_declared_outputs']
  taught-before-tested: A.f3←s01

### s03 · hands_on · Review the module interface and verification
Review the evidence — Read the supplied excerpt(s) in this step and decide which are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each supplied-module configuration and verification record. Decide whether it respects the supplied interface and verifies exactly one sandbox instance and declared outputs against chosen inputs.
  'Supplied interface: source SOURCE; named input INPUT; declared output OUTPUT. Intended INPUT value: INTENDED.
module "NAME" {
  source = "SOURCE"
  INPUT = "INTENDED"
}
Output reference: module.NAME.OUTPUT.
Initialized. Reviewed plan: exactly one sandbox EC2 instance with settings INTENDED. Approved apply completed. Created instance: exactly one, settings INTENDED. Declared OUTPUT agrees with created instance and chosen inputs.' -> Meets the stated verification criteria
      feedback: Only supplied interface names are used; the plan and created instance/outputs agree with chosen inputs.
  'Supplied interface: source SOURCE; input INPUT; output OUTPUT. Configuration instead supplies invented input OTHER and references module.NAME.INVENTED. No declaration of either name exists in the supplied interface. Record claims module interface respected.' -> Fails at least one stated criterion
      feedback: A reusable module does not authorize invented inputs or outputs; use the supplied interface.
  'Supplied source SOURCE, input INPUT=INTENDED and output module.NAME.OUTPUT used; initialized; plan reviewed for exactly one instance with settings INTENDED. Apply completed; actual instance settings DIFFERENT. Output and instance comparison reports mismatch. Record calls verification successful.' -> Fails at least one stated criterion
      feedback: Successful verification requires created settings and declared outputs to agree with the chosen inputs, not a mismatch.
  feedback✔: The judgement matches the supplied evidence and verification requirements.  feedback✘: Separate the requested outcome from evidence that it actually occurred; check the approved scope and the missing observations.  hints: ['Compare the recorded observations with every criterion in the question.']  remediation→r02
  MEASURES: A:verify_supplied_module_input_and_output_contract(f1,f2); A:compare_module_inputs_with_planned_instance_settings(f2,f3); A:verify_created_instance_and_declared_outputs(f3)   anchors=['practice', 'assessment:verify_supplied_module_input_and_output_contract', 'assessment:compare_module_inputs_with_planned_instance_settings', 'assessment:verify_created_instance_and_declared_outputs']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f2←s01; A.f3←s01; A.f3←s01

### s04 · recap · What to carry forward
Takeaways — 
(takeaway) Use supplied module inputs and declared outputs; review planned settings and verify the created instance after approved apply. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Rightsize a resource using a supplied workload baseline

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast: evidence versus assumption
(definition) Initialize the module, inspect the input values and planned instance settings, apply through the approved workflow and verify the created instance and declared outputs. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) A reusable module does not replace plan review or live verification. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Contrast: evidence versus assumption
(definition) A module packages resource declarations behind input variables and output values. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Configure module "NAME" with the supplied source and named input arguments; reference its output as module.NAME.OUTPUT. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Initialize the module, inspect the input values and planned instance settings, apply through the approved workflow and verify the created instance and declared outputs. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) A reusable module does not replace plan review or live verification. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Try this distinction
· remediation_steps.eyebrow: Try this distinction

=========

# EVALUATOR PACKET — Rightsize a resource using a supplied workload baseline (aws_devops.tile.096)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.rightsize_a_resource_using_a_supplied_workload_baseline — Rightsize a resource using a supplied workload baseline

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.rightsize_a_resource_using_a_supplied_workload_baseline)   objective: Rightsize a resource against a workload baseline
A.f1: Rightsizing matches resource type and size to workload performance and capacity requirements rather than simply choosing the smallest instance.   [sources: aws_well_architected_framework#cost06-bp02.html]
A.f2: Compare supplied load, utilization and performance evidence with service constraints and recommend a smaller instance only when those constraints remain satisfied.   [sources: aws_well_architected_framework#cost06-bp02.html]
A.f3: Account for peak and changing demand in the baseline rather than using one low-utilization sample as sufficient evidence.   [sources: aws_well_architected_framework#cost06-bp02.html]
note: Use supplied baseline and constraints; do not introduce EC2 pricing estimates or unsupported instance recommendations.
PRACTICE ANCHOR (field_selection): Select one EC2 sizing recommendation from supplied options using workload load, utilization, performance evidence and service constraints across normal, peak and changing demand. Select a smaller option only when the supplied evidence supports it; otherwise withhold a reduction.  SUCCESS: The selected recommendation preserves every supplied performance and capacity constraint across the relevant baseline. Supporting evidence identifies the workload requirement and the normal, peak and changing-demand observations that justify the choice, rather than relying on one low-utilization sample.
ASSESSMENT ANCHOR: choose_smaller_ec2_capacity_only_when_service_constraints_are_preserved facts=['f1', 'f2']
ASSESSMENT ANCHOR: evaluate_peak_and_changing_demand_before_recommending_a_reduction facts=['f2', 'f3']

## DATA ASSETS USED
ds.ec2_sizing_evidence: EC2 sizing: baseline and candidate evidence — columns: workload(identifier), size_option(categorical), demand_period(categorical), load_requests_per_second(numerical), capacity_utilization_pct(numerical), response_latency_ms(numerical), max_response_latency_ms(numerical), max_capacity_utilization_pct(numerical)
   ["sandbox workload","current size","normal",40,20,80,200,100]
   ["sandbox workload","smaller candidate","normal",40,40,120,200,100]
   ["sandbox workload","current size","peak",200,90,200,200,100]
   ["sandbox workload","smaller candidate","peak",200,100,260,200,100]
   ["sandbox workload","current size","changing demand",160,75,180,200,100]
   ["sandbox workload","smaller candidate","changing demand",160,100,230,200,100]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Approval stop; Audit evidence; Audit evidence integrity; Audit storage retention; Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template; directly require the native EC2 instance foundation; Backend configuration; Block release on actionable dependency or image security findings; Credential readiness; Diagnose EC2 or container health failures using telemetry and prepared Linux inspection skills; Diagnose a failed delivery pipeline action; Gate release completion on a deployed-service smoke check; Handle failed event delivery with bounded retries and failure capture; Perform a controlled ECS service rollout; Promote the same artifact version across environments; Rehearsal isolation; Replacement controls; Residual charge verification; Route a security finding with evidence to its responsible owner; Route an operational event to a notification or established Systems Manager action; Run an ECS service with a desired task count; Run supplied unit and integration tests as blocking pipeline gates after external testing preparation; Safe teardown; State access isolation; Submit small reviewable infrastructure changes after registry Git and code-review pre

## LESSON, in learner order

### s01 · explainer · Operating model
Understand — 
(mechanism) Rightsizing matches resource type and size to workload performance and capacity requirements, not simply the smallest instance. Compare supplied load, utilization and performance with service constraints. Recommend a smaller instance only if those constraints remain satisfied. Include peak and changing demand; one low-utilization sample is not enough. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3⟧
[TABLE ds.ec2_sizing_evidence cols=['workload', 'size_option', 'demand_period', 'load_requests_per_second', 'capacity_utilization_pct', 'response_latency_ms', 'max_response_latency_ms', 'max_capacity_utilization_pct'] ] caption: EC2 sizing: baseline and candidate evidence

### s02 · explainer · Keep the evidence distinct
Understand — 
(example) Compare the current size and smaller candidate across normal, peak and changing demand. Keep observed load, measured utilization and latency separate from the recommendation they support. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧
(example) The current peak reaches the supplied latency boundary. The smaller candidate’s peak and changing-demand latency exceed the supplied bound, so the normal sample cannot justify that reduction. Preserve the constraints and withhold the unsupported reduction; do not invent a price comparison. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · check · Review the sizing evidence
Check your understanding — Read the supplied excerpt(s) in this step and decide which are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] Sizing excerpt: latency bound 200 ms and utilization bound 100%. Smaller candidate: normal 120 ms/40%; peak 260 ms/100%; changing demand 230 ms/100%. A proposed recommendation cites only normal utilization. Which option identifies the comparison omitted by that recommendation?
  ✘ o1: Use the normal observation alone because it shows spare capacity.
      why: One low-utilization sample does not account for peak or changing demand.
  ✘ o2: Choose the smallest candidate regardless of the supplied peak performance.
      why: Rightsizing preserves workload requirements rather than simply choosing the smallest size.
  ✔ o3: Compare the proposed size with every supplied capacity and performance constraint across normal, peak and changing demand.
      why: A reduction must preserve constraints across the relevant baseline.
  feedback✔: A reduction must preserve constraints across the relevant baseline.  feedback✘: Review why each alternative fails the specific verification requirement.  hints: ['Compare the recorded observations with every criterion in the question.']  remediation→r01
  MEASURES: A:evaluate_peak_and_changing_demand_before_recommending_a_reduction(f2,f3)   anchors=['assessment:evaluate_peak_and_changing_demand_before_recommending_a_reduction']
  taught-before-tested: A.f2←s01; A.f3←s01

### s04 · hands_on · Review the sizing evidence
Review the evidence — Inspect the supplied evidence and select the supported recommendation or handoff.
QUESTION [table_select, stretch, grading=client] 
  intro shown to learner: Choose the option that preserves every supplied latency and capacity bound across all three demand periods. Select its supporting row for each period, then the failing candidate evidence. Together these selections justify whether to withhold the smaller-size reduction; equality satisfies a bound.
  task t1 (row): Select the normal row for the only size option that satisfies both constraints in every supplied demand period.  KEY: row={'workload': 'sandbox workload', 'size_option': 'current size', 'demand_period': 'normal'} column=None expect=None dataset-says={'workload': 'sandbox workload', 'size_option': 'current size', 'demand_period': 'normal', 'load_requests_per_second': 40, 'capacity_utilization_pct': 20, 'response_latency_ms': 80, 'max_response_latency_ms': 200, 'max_capacity_utilization_pct': 100}
      feedback: {'correct': 'This selection preserves the supplied evidence needed for the decision.', 'incorrect': 'Select the exact requested evidence, not a different period or an unsupported replacement claim.'}
  task t2 (row): Select the peak row for the only size option that satisfies both constraints in every supplied demand period.  KEY: row={'workload': 'sandbox workload', 'size_option': 'current size', 'demand_period': 'peak'} column=None expect=None dataset-says={'workload': 'sandbox workload', 'size_option': 'current size', 'demand_period': 'peak', 'load_requests_per_second': 200, 'capacity_utilization_pct': 90, 'response_latency_ms': 200, 'max_response_latency_ms': 200, 'max_capacity_utilization_pct': 100}
      feedback: {'correct': 'This selection preserves the supplied evidence needed for the decision.', 'incorrect': 'Select the exact requested evidence, not a different period or an unsupported replacement claim.'}
  task t3 (row): Select the changing demand row for the only size option that satisfies both constraints in every supplied demand period.  KEY: row={'workload': 'sandbox workload', 'size_option': 'current size', 'demand_period': 'changing demand'} column=None expect=None dataset-says={'workload': 'sandbox workload', 'size_option': 'current size', 'demand_period': 'changing demand', 'load_requests_per_second': 160, 'capacity_utilization_pct': 75, 'response_latency_ms': 180, 'max_response_latency_ms': 200, 'max_capacity_utilization_pct': 100}
      feedback: {'correct': 'This selection preserves the supplied evidence needed for the decision.', 'incorrect': 'Select the exact requested evidence, not a different period or an unsupported replacement claim.'}
  task t4 (cell): Select the latency cell exceeding the bound in the peak row of the smaller candidate; this is evidence against the reduction.  KEY: row={'workload': 'sandbox workload', 'size_option': 'smaller candidate', 'demand_period': 'peak'} column=response_latency_ms expect=260 dataset-says=260
      feedback: {'correct': 'This selection preserves the supplied evidence needed for the decision.', 'incorrect': 'Select the exact requested evidence, not a different period or an unsupported replacement claim.'}
  task t5 (cell): Select the latency cell exceeding the bound in the changing demand row of the smaller candidate; this is evidence against the reduction.  KEY: row={'workload': 'sandbox workload', 'size_option': 'smaller candidate', 'demand_period': 'changing demand'} column=response_latency_ms expect=230 dataset-says=230
      feedback: {'correct': 'This selection preserves the supplied evidence needed for the decision.', 'incorrect': 'Select the exact requested evidence, not a different period or an unsupported replacement claim.'}
  feedback✔: The selected option preserves every supplied bound; peak and changing-demand candidate latency rule out the smaller-size reduction.  feedback✘: Separate the requested outcome from evidence that it actually occurred; check the approved scope and the missing observations.  hints: ['Compare the recorded observations with every criterion in the question.']  remediation→r02
  MEASURES: A:choose_smaller_ec2_capacity_only_when_service_constraints_are_preserved(f1,f2); A:evaluate_peak_and_changing_demand_before_recommending_a_reduction(f2,f3)   anchors=['practice', 'assessment:choose_smaller_ec2_capacity_only_when_service_constraints_are_preserved', 'assessment:evaluate_peak_and_changing_demand_before_recommending_a_reduction']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f2←s01; A.f3←s01

### s05 · recap · What to carry forward
Takeaways — 
(takeaway) Match size to requirements across normal, peak and changing demand. A low sample alone cannot justify a reduction. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Route a security finding with evidence to its responsible owner

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast: evidence versus assumption
(definition) Compare supplied load, utilization and performance evidence with service constraints and recommend a smaller instance only when those constraints remain satisfied. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Account for peak and changing demand in the baseline rather than using one low-utilization sample as sufficient evidence. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) A low normal sample is not sufficient evidence for a smaller size. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Contrast: evidence versus assumption
(definition) Rightsizing matches resource type and size to workload performance and capacity requirements rather than simply choosing the smallest instance. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Compare supplied load, utilization and performance evidence with service constraints and recommend a smaller instance only when those constraints remain satisfied. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Account for peak and changing demand in the baseline rather than using one low-utilization sample as sufficient evidence. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) A low normal sample is not sufficient evidence for a smaller size. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.ec2_sizing_evidence cols=['workload', 'size_option', 'demand_period', 'load_requests_per_second', 'capacity_utilization_pct', 'response_latency_ms', 'max_response_latency_ms', 'max_capacity_utilization_pct'] ] caption: EC2 sizing: baseline and candidate evidence

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Try this distinction
· remediation_steps.eyebrow: Try this distinction

=========

# EVALUATOR PACKET — Route a security finding with evidence to its responsible owner (aws_devops.tile.097)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.route_a_security_finding_with_evidence_to_its_responsible_owner — Route a security finding with evidence to its responsible owner

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.route_a_security_finding_with_evidence_to_its_responsible_owner)   objective: Route a security finding to its owner
A.f1: A finding’s resource identity, severity and activity details provide context needed by the accountable responder.   [sources: aws_guardduty_user_guide#guardduty_findings-summary.html]
A.f2: Route the supplied finding ID or evidence link, affected resource, observed activity and urgency to the responsible owner and apply the established escalation path.   [sources: aws_well_architected_framework#ops06-bp03.html]
A.f3: Preserve the finding evidence rather than replacing it with an unsupported claim that the resource is compromised.   [sources: aws_guardduty_user_guide#guardduty_findings-summary.html]
note: Use established owner and escalation path; do not author specialist security conclusions.
PRACTICE ANCHOR (field_selection): Use a supplied security finding, owner mapping and escalation path to select the evidence link or finding ID, affected resource, severity, observed activity, urgency, responsible recipient and escalation context for a handoff.  SUCCESS: The handoff retains the supplied evidence reference and accurate resource and activity details, communicates severity and urgency, reaches the mapped accountable owner, and follows the supplied escalation path without asserting an unsupported compromise.
ASSESSMENT ANCHOR: verify_finding_context_reaches_accountable_owner facts=['f1', 'f2']
ASSESSMENT ANCHOR: apply_established_escalation_path facts=['f2']
ASSESSMENT ANCHOR: preserve_finding_evidence_without_unsupported_conclusions facts=['f3']

## DATA ASSETS USED
ds.security_finding_handoff: Security finding: evidence and accountable owner — columns: finding_id(identifier), affected_resource(identifier), severity(categorical), observed_activity(text), urgency(categorical), accountable_owner(categorical), established_escalation_path(text)
   ["finding-sandbox","sandbox-workload-resource","high","Finding reports suspicious activity on the affected resource.","prompt review","sandbox workload operations team","Notify the accountable owner; escalate to the established security on-call if the owner is unavailable."]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Approval stop; Audit evidence; Audit evidence integrity; Audit storage retention; Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template; directly require the native EC2 instance foundation; Backend configuration; Block release on actionable dependency or image security findings; Credential readiness; Diagnose EC2 or container health failures using telemetry and prepared Linux inspection skills; Diagnose a failed delivery pipeline action; Gate release completion on a deployed-service smoke check; Handle failed event delivery with bounded retries and failure capture; Perform a controlled ECS service rollout; Promote the same artifact version across environments; Rehearsal isolation; Replacement controls; Residual charge verification; Route an operational event to a notification or established Systems Manager action; Run an ECS service with a desired task count; Run supplied unit and integration tests as blocking pipeline gates after external testing preparation; Safe teardown; State access isolation; State locking; Submit small reviewable infrastructure changes after registry Git and code-review prerequisites; Verify availability across Availabilit

## LESSON, in learner order

### s01 · explainer · Operating model
Understand — 
(mechanism) Resource identity, severity and activity details give the accountable responder context. Send the supplied finding ID or evidence link, affected resource, observed activity and urgency to the responsible owner, using the established escalation path. Preserve the finding evidence; suspicious activity is not an unsupported conclusion that the resource is compromised. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Use the registered finding’s reported severity and urgency. Preserve its activity description and evidence reference so the accountable owner can inspect it. Follow the supplied escalation route if the owner is unavailable; a concise handoff must not erase context or exaggerate the evidence. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.security_finding_handoff cols=['finding_id', 'affected_resource', 'severity', 'observed_activity', 'urgency', 'accountable_owner', 'established_escalation_path'] ] caption: Security finding: evidence and accountable owner

### s02 · check · Review the finding handoff
Check your understanding — Read the supplied excerpt(s) in this step and decide which are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] Finding excerpt: ID finding-sandbox; affected resource sandbox-workload-resource; reported activity ‘Finding reports suspicious activity on the affected resource.’ The excerpt contains no confirmed-compromise conclusion. Which handoff treatment preserves this excerpt’s evidentiary meaning?
  ✘ o1: Remove the finding reference and activity to make the handoff shorter.
      why: A concise handoff must not erase the evidence needed by the responder.
  ✔ o2: Retain the finding reference and reported activity without declaring compromise unsupported by the record.
      why: Preserve the evidence and avoid unsupported conclusions.
  ✘ o3: Replace the activity description with "the resource is compromised".
      why: A stronger unsupported compromise claim is not a substitute for the finding evidence.
  feedback✔: Preserve the evidence and avoid unsupported conclusions.  feedback✘: Review why each alternative fails the specific verification requirement.  hints: ['Compare the recorded observations with every criterion in the question.']  remediation→r01
  MEASURES: A:preserve_finding_evidence_without_unsupported_conclusions(f3)   anchors=['assessment:preserve_finding_evidence_without_unsupported_conclusions']
  taught-before-tested: A.f3←s01

### s03 · hands_on · Review the finding handoff
Review the evidence — Inspect the supplied evidence and select the supported recommendation or handoff.
QUESTION [table_select, stretch, grading=client] 
  intro shown to learner: Select the supplied evidence and routing cells for an accurate finding handoff. Retain the reported activity as evidence, not an unsupported compromise conclusion. Use the mapped owner and established escalation route; each selected cell is part of the handoff.
  task t1 (cell): Select the evidence reference to retain in the handoff.  KEY: row={'finding_id': 'finding-sandbox'} column=finding_id expect=finding-sandbox dataset-says=finding-sandbox
      feedback: {'correct': 'This selection preserves the supplied evidence needed for the decision.', 'incorrect': 'Select the requested finding-context or routing field from the supplied record; preserve its reported value.'}
  task t2 (cell): Select the affected resource identity.  KEY: row={'finding_id': 'finding-sandbox'} column=affected_resource expect=sandbox-workload-resource dataset-says=sandbox-workload-resource
      feedback: {'correct': 'This selection preserves the supplied evidence needed for the decision.', 'incorrect': 'Select the requested finding-context or routing field from the supplied record; preserve its reported value.'}
  task t3 (cell): Select the reported severity without changing it.  KEY: row={'finding_id': 'finding-sandbox'} column=severity expect=high dataset-says=high
      feedback: {'correct': 'This selection preserves the supplied evidence needed for the decision.', 'incorrect': 'Select the requested finding-context or routing field from the supplied record; preserve its reported value.'}
  task t4 (cell): Select the reported activity to preserve without asserting compromise.  KEY: row={'finding_id': 'finding-sandbox'} column=observed_activity expect=Finding reports suspicious activity on the affected resource. dataset-says=Finding reports suspicious activity on the affected resource.
      feedback: {'correct': 'This selection preserves the supplied evidence needed for the decision.', 'incorrect': 'Select the requested finding-context or routing field from the supplied record; preserve its reported value.'}
  task t5 (cell): Select the supplied urgency to communicate.  KEY: row={'finding_id': 'finding-sandbox'} column=urgency expect=prompt review dataset-says=prompt review
      feedback: {'correct': 'This selection preserves the supplied evidence needed for the decision.', 'incorrect': 'Select the requested finding-context or routing field from the supplied record; preserve its reported value.'}
  task t6 (cell): Select the accountable recipient from the owner mapping.  KEY: row={'finding_id': 'finding-sandbox'} column=accountable_owner expect=sandbox workload operations team dataset-says=sandbox workload operations team
      feedback: {'correct': 'This selection preserves the supplied evidence needed for the decision.', 'incorrect': 'Select the requested finding-context or routing field from the supplied record; preserve its reported value.'}
  task t7 (cell): Select the established path to follow if the owner is unavailable.  KEY: row={'finding_id': 'finding-sandbox'} column=established_escalation_path expect=Notify the accountable owner; escalate to the established security on-call if the owner is unavailable. dataset-says=Notify the accountable owner; escalate to the established security on-call if the owner is unavailable.
      feedback: {'correct': 'This selection preserves the supplied evidence needed for the decision.', 'incorrect': 'Select the requested finding-context or routing field from the supplied record; preserve its reported value.'}
  feedback✔: The handoff retains evidence, resource, severity, activity and urgency, and follows the mapped owner and established escalation path without an unsupported compromise claim.  feedback✘: Separate the requested outcome from evidence that it actually occurred; check the approved scope and the missing observations.  hints: ['Compare the recorded observations with every criterion in the question.']  remediation→r02
  MEASURES: A:verify_finding_context_reaches_accountable_owner(f1,f2); A:apply_established_escalation_path(f2); A:preserve_finding_evidence_without_unsupported_conclusions(f3)   anchors=['practice', 'assessment:verify_finding_context_reaches_accountable_owner', 'assessment:apply_established_escalation_path', 'assessment:preserve_finding_evidence_without_unsupported_conclusions']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f2←s01; A.f3←s01

### s04 · recap · What to carry forward
Takeaways — 
(takeaway) Preserve finding context and evidence, route to the accountable owner and follow established escalation without exaggerating activity. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Route an operational event to a notification or established Systems Manager action

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast: evidence versus assumption
(definition) Preserve the finding evidence rather than replacing it with an unsupported claim that the resource is compromised. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) A report of suspicious activity is not a supported compromise conclusion. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Contrast: evidence versus assumption
(definition) A finding’s resource identity, severity and activity details provide context needed by the accountable responder. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Route the supplied finding ID or evidence link, affected resource, observed activity and urgency to the responsible owner and apply the established escalation path. ⟦A.f2 A:tb3 A:tb4⟧
(definition) Preserve the finding evidence rather than replacing it with an unsupported claim that the resource is compromised. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) A report of suspicious activity is not a supported compromise conclusion. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.security_finding_handoff cols=['finding_id', 'affected_resource', 'severity', 'observed_activity', 'urgency', 'accountable_owner', 'established_escalation_path'] ] caption: Security finding: evidence and accountable owner

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Try this distinction
· remediation_steps.eyebrow: Try this distinction

=========

# EVALUATOR PACKET — Route an operational event to a notification or established Systems Manager action (aws_devops.tile.098)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.route_an_operational_event_to_a_notification_or_established_systems_manager_action — Route an operational event to a notification or established Systems Manager action

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.route_an_operational_event_to_a_notification_or_established_systems_manager_action)   objective: Route an operational event to an established action
A.f1: An EventBridge rule pairs an event pattern with one or more targets to receive matching events.   [sources: aws_eventbridge_user_guide#eb-create-rule-wizard.html]
A.f2: Set the supplied event bus and pattern and add only the approved SNS or Systems Manager target and required target parameters.   [sources: aws_eventbridge_user_guide#eb-create-rule-wizard.html]
A.f3: Configure the target’s required permissions, then send matching and nonmatching test events and inspect the approved target’s execution or notification evidence.   [sources: aws_eventbridge_user_guide#eb-events-iam-roles.html]
note: Use established Systems Manager action or approved SNS target; do not author a new response document.
PRACTICE ANCHOR (tool_simulation): Connect one EventBridge rule on the supplied event bus, using the supplied event pattern, to one approved SNS target or established Systems Manager action. Set the required target parameters and permissions, then send the supplied matching and nonmatching test events.  SUCCESS: The rule contains only the supplied approved target with its required parameters and permissions. Target execution or notification evidence confirms that the matching test event invokes the approved target and the nonmatching test event does not.
ASSESSMENT ANCHOR: verify_rule_pattern_and_approved_target_configuration facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_matching_and_nonmatching_events_against_target_evidence facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Approval stop; Audit evidence; Audit evidence integrity; Audit storage retention; Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template; directly require the native EC2 instance foundation; Backend configuration; Block release on actionable dependency or image security findings; Control environment promotion with a manual approval; Credential readiness; Diagnose EC2 or container health failures using telemetry and prepared Linux inspection skills; Diagnose a failed delivery pipeline action; Gate release completion on a deployed-service smoke check; Handle failed event delivery with bounded retries and failure capture; Perform a controlled ECS service rollout; Promote the same artifact version across environments; Rehearsal isolation; Replacement controls; Residual charge verification; Run an ECS service with a desired task count; Run supplied unit and integration tests as blocking pipeline gates after external testing preparation; Safe teardown; State access isolation; State locking; Submit small reviewable infrastructure changes after registry Git and code-review prerequisites; Verify availability across Availability Zones under a controlled fai

## LESSON, in learner order

### s01 · explainer · Operating model
Understand — 
(mechanism) An EventBridge rule pairs a pattern with one or more targets for matching events. Set the supplied event bus and pattern, adding only the approved SNS or Systems Manager target and required parameters. Configure the target’s required permissions. Send matching and nonmatching test events and inspect execution or notification evidence at the approved target. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Compare matching and nonmatching test results with the intended rule selection. Pattern matching in isolation does not complete the routing check: inspect execution or notification evidence at the approved target. Keep the required target authorization model and parameters with that evidence. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[DIAGRAM: Illustrative SNS routing record — sandbox observations] nodes=['Setup: supplied event bus and pattern; one approved SNS target; required parameters and permissions configured', 'Matching test: matches the supplied pattern; expected SNS notification receipt recorded', 'Nonmatching test: does not match the supplied pattern; no notification from this rule recorded'] edges=[('n1', 'n2', None), ('n2', 'n3', None)] alt: Illustrative sandbox observations, not live evidence. Setup: supplied event bus and pattern; one approved SNS target; required parameters and permissions configured; Matching test: matches the supplied pattern; expected SNS notification receipt recorded; Nonmatching test: does not match the supplied pattern; no notification from this rule recorded

### s02 · check · Review the event route
Check your understanding — Read the supplied excerpt(s) in this step and decide which are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] Routing record: only approved TARGET is configured with supplied parameters and required permissions. MATCH produces a notification at TARGET; NONMATCH produces no notification from this rule at TARGET. A separate pattern-only check also passes. Which option identifies the observations that verify the route rather than just its pattern?
  ✔ o1: At the approved target, the matching event has execution or notification evidence and the nonmatching event does not.
      why: Both event selection and actual approved-target evidence must be checked.
  ✘ o2: The matching event passes a pattern-only check, without target evidence.
      why: Pattern matching in isolation does not verify target execution or notification.
  ✘ o3: The target is listed in the rule, without testing either event.
      why: Configuration alone does not demonstrate matching and nonmatching event behavior.
  feedback✔: Both event selection and actual approved-target evidence must be checked.  feedback✘: Review why each alternative fails the specific verification requirement.  hints: ['Compare the recorded observations with every criterion in the question.']  remediation→r01
  MEASURES: A:verify_matching_and_nonmatching_events_against_target_evidence(f3)   anchors=['assessment:verify_matching_and_nonmatching_events_against-190551e9']
  taught-before-tested: A.f3←s01

### s03 · hands_on · Review the event route
Review the evidence — Read the supplied excerpt(s) in this step and decide which are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each EventBridge configuration-and-test record. Decide whether it verifies only the approved route with required parameters, permissions and matching/nonmatching target evidence.
  'Supplied bus BUS and pattern PATTERN configured. Only target: approved SNS notification target TARGET. Required target parameters match supplied values; required target permissions configured. Matching test event MATCH: notification observed at TARGET. Nonmatching event NONMATCH: no notification at TARGET. Both observations retained.' -> Meets the stated verification criteria
      feedback: The approved-only configuration and actual target evidence verify the positive and negative route tests.
  'BUS and PATTERN configured. Approved TARGET has required parameters and permissions; an additional unapproved target EXTRA is also present. Matching and nonmatching results at TARGET are as expected.' -> Fails at least one stated criterion
      feedback: Correct test results at the approved target do not authorize an extra unapproved target.
  'BUS and PATTERN configured with only approved TARGET and supplied parameters. Required target permissions not configured. Pattern-only check matches MATCH and rejects NONMATCH; no target execution or notification evidence recorded. Record says route verified.' -> Fails at least one stated criterion
      feedback: The route requires target permissions and actual approved-target evidence, not just pattern matching.
  feedback✔: The judgement matches the supplied evidence and verification requirements.  feedback✘: Separate the requested outcome from evidence that it actually occurred; check the approved scope and the missing observations.  hints: ['Compare the recorded observations with every criterion in the question.']  remediation→r02
  MEASURES: A:verify_rule_pattern_and_approved_target_configuration(f1,f2); A:verify_matching_and_nonmatching_events_against_target_evidence(f3)   anchors=['practice', 'assessment:verify_rule_pattern_and_approved_target_configuration', 'assessment:verify_matching_and_nonmatching_events_against-190551e9']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s04 · recap · What to carry forward
Takeaways — 
(takeaway) Use the approved target, parameters and permissions. Verify matching and nonmatching tests with target evidence. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Run an ECS service with a desired task count

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast: evidence versus assumption
(definition) Configure the target’s required permissions, then send matching and nonmatching test events and inspect the approved target’s execution or notification evidence. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) A pattern match alone is not verified target execution or notification. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Contrast: evidence versus assumption
(definition) An EventBridge rule pairs an event pattern with one or more targets to receive matching events. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Set the supplied event bus and pattern and add only the approved SNS or Systems Manager target and required target parameters. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Configure the target’s required permissions, then send matching and nonmatching test events and inspect the approved target’s execution or notification evidence. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) A pattern match alone is not verified target execution or notification. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Try this distinction
· remediation_steps.eyebrow: Try this distinction

=========

# EVALUATOR PACKET — Run an ECS service with a desired task count (aws_devops.tile.099)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.run_an_ecs_service_with_a_desired_task_count — Run an ECS service with a desired task count

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.run_an_ecs_service_with_a_desired_task_count)   objective: Run an ECS service at a desired task count
A.f1: An ECS service maintains the desired number of tasks and replaces tasks that stop or fail.   [sources: aws_ecs_developer_guide#ecs_services.html]
A.f2: Create the service with the supplied cluster, task definition, network settings and desiredCount.   [sources: aws_ecs_developer_guide#service_definition_parameters.html]
A.f3: Remove one task in the controlled exercise and inspect service events and running/pending task counts until the desired count is restored.   [sources: aws_ecs_developer_guide#ecs_services.html]
note: Use supplied removal procedure; defer task identity and rolling deployment details to their own concepts.
PRACTICE ANCHOR (tool_simulation): Create one ECS service using the supplied cluster, task definition, network settings and desiredCount. Use the supplied removal procedure to remove one approved task, then inspect service events and running/pending task counts until the desired count is restored.  SUCCESS: The service uses the supplied configuration. After the controlled removal, service events show replacement activity, the running task count returns to desiredCount, and the pending count settles to zero.
ASSESSMENT ANCHOR: verify_service_restores_desired_task_count facts=['f1', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Approval stop; Audit evidence; Audit evidence integrity; Audit storage retention; Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template; directly require the native EC2 instance foundation; Backend configuration; Block release on actionable dependency or image security findings; Control environment promotion with a manual approval; Credential readiness; Diagnose EC2 or container health failures using telemetry and prepared Linux inspection skills; Diagnose a failed delivery pipeline action; Gate release completion on a deployed-service smoke check; Handle failed event delivery with bounded retries and failure capture; Perform a controlled ECS service rollout; Promote the same artifact version across environments; Recover an incident safely using an established runbook; Rehearsal isolation; Replacement controls; Residual charge verification; Run supplied unit and integration tests as blocking pipeline gates after external testing preparation; Safe teardown; State access isolation; State locking; Submit small reviewable infrastructure changes after registry Git and code-review prerequisites; Verify availability across Availability Zones under a con

## LESSON, in learner order

### s01 · explainer · Operating model
Understand — 
(mechanism) An ECS service maintains the desired task count and replaces stopped or failed tasks. Create it with the supplied cluster, task definition, network settings and desiredCount. In the controlled exercise, remove the one approved task, then inspect service events and running/pending task counts until the desired count is restored. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) The task definition supplies what runs; the service maintains how many tasks are requested. Observe the controlled task loss, replacement progress and restored running count. Keep service events and running/pending counts in the record rather than assuming service creation proves replacement. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[DIAGRAM: Illustrative three-task sequence — not a guaranteed timing trace] nodes=['Before removal: desiredCount=3; running=3; pending=0', 'Controlled removal: one approved task removed; running=2; pending=0', 'Replacement: service event records replacement started; running=2; pending=1', 'Restored: replacement running; desiredCount=3; running=3; pending=0'] edges=[('n1', 'n2', None), ('n2', 'n3', None), ('n3', 'n4', None)] alt: Illustrative sandbox sequence, not live evidence or a guaranteed timing trace. Before removal: desiredCount=3; running=3; pending=0; Controlled removal: one approved task removed; running=2; pending=0; Replacement: service event records replacement started; running=2; pending=1; Restored: replacement running; desiredCount=3; running=3; pending=0

### s02 · check · Review task-count restoration
Check your understanding — Read the supplied excerpt(s) in this step and decide which are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] Service record: desiredCount=3. After one approved task is removed, events report replacement activity. Final counts: running=3, pending=0. The task definition still exists and service creation occurred earlier. Which option identifies the observations demonstrating restored task count?
  ✘ o1: The task definition still exists, without any count check.
      why: The task definition supplies what runs; it does not prove restored service task count.
  ✘ o2: The service was created earlier, so replacement requires no observation.
      why: Service creation alone does not verify replacement after controlled removal.
  ✔ o3: Service events show replacement activity; running equals desiredCount and pending settles to zero.
      why: Service events and running/pending counts demonstrate completed restoration.
  feedback✔: Service events and running/pending counts demonstrate completed restoration.  feedback✘: Review why each alternative fails the specific verification requirement.  hints: ['Compare the recorded observations with every criterion in the question.']  remediation→r01
  MEASURES: A:verify_service_restores_desired_task_count(f1,f3)   anchors=['assessment:verify_service_restores_desired_task_count']
  taught-before-tested: A.f1←s01; A.f3←s01

### s03 · hands_on · Review task-count restoration
Review the evidence — Read the supplied excerpt(s) in this step and decide which are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each ECS service configuration-and-replacement record. Decide whether the supplied configuration and observed task replacement meet the desired-count restoration criterion.
  'Service uses supplied CLUSTER, TASK_DEFINITION, NETWORK and desiredCount DESIRED. One approved task removed. Events show replacement started. Running count remains below DESIRED; pending count has not settled to zero. Record says replacement complete.' -> Fails at least one stated criterion
      feedback: Replacement progress is not completed restoration; running must return to desiredCount and pending must settle to zero.
  'Service created with a cluster different from supplied CLUSTER; other settings supplied. After controlled removal, events show replacement and running returns to DESIRED with pending zero. Record says all exercise criteria met.' -> Fails at least one stated criterion
      feedback: Restored count does not excuse configuration that differs from the supplied cluster.
  'Service uses supplied cluster CLUSTER, task definition TASK_DEFINITION, network NETWORK and desiredCount DESIRED. One approved task removed using supplied procedure. Service events: replacement activity observed. Final running count: DESIRED; final pending count: zero.' -> Meets the stated verification criteria
      feedback: The supplied configuration and replacement evidence show completed restoration to desiredCount with no pending tasks.
  feedback✔: The judgement matches the supplied evidence and verification requirements.  feedback✘: Separate the requested outcome from evidence that it actually occurred; check the approved scope and the missing observations.  hints: ['Compare the recorded observations with every criterion in the question.']
  MEASURES: A:verify_service_restores_desired_task_count(f1,f3)   anchors=['practice', 'assessment:verify_service_restores_desired_task_count']
  taught-before-tested: A.f1←s01; A.f3←s01

### s04 · recap · What to carry forward
Takeaways — 
(takeaway) The service replaces stopped or failed tasks. Verify restoration through events and running/pending counts after controlled removal. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Run supplied unit and integration tests as blocking pipeline gates after external testing preparation

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast: evidence versus assumption
(definition) An ECS service maintains the desired number of tasks and replaces tasks that stop or fail. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Remove one task in the controlled exercise and inspect service events and running/pending task counts until the desired count is restored. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) A service definition is not evidence that the desired running count was restored. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Try this distinction