# EVALUATOR PACKET — From supplied build commands to EC2 deployment (aws_devops.tile.053)
Tile summary: Match supplied phase commands and generated output selection; verify both phase logs and exported files. Keep revision, intended targets, AppSpec mappings, hook results and target files connected.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.configure_a_codebuild_buildspec_for_a_supplied_application — Configure a CodeBuild buildspec for a supplied application
B = aws_devops.configure_a_codedeploy_deployment_action_for_a_supplied_ec2_application — Configure a CodeDeploy deployment action for a supplied EC2 application

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.configure_a_codebuild_buildspec_for_a_supplied_application)   objective: Configure a CodeBuild buildspec
A.f1: A buildspec is a YAML document describing build commands and artifacts; version: 0.2 supports commands in the same shell environment.   [sources: aws_codebuild_user_guide#build-spec-ref.html]
A.f2: Place supplied commands under phases such as install, pre_build, build and post_build, using commands lists in the needed phases.   [sources: aws_codebuild_user_guide#build-spec-ref.html]
A.f3: Set artifacts.files and, if needed, base-directory to match the generated output, then inspect the build’s phase logs and exported artifact.   [sources: aws_codebuild_user_guide#build-spec-ref.html]
note: Use supplied commands and application output; require shared shell/testing preparation.
PRACTICE ANCHOR (live_code): Configure a version 0.2 buildspec for the supplied application, place its supplied commands in the needed phases, and select its generated output for export.  SUCCESS: The supplied commands complete successfully, artifact selection matches the generated output, and inspection of phase logs and the exported artifact confirms the intended file was retained.
ASSESSMENT ANCHOR: identify_buildspec_phase_commands_that_produce_the_declared_output facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_artifact_selection_matches_generated_output facts=['f3']
ASSESSMENT ANCHOR: distinguish_command_success_from_verified_artifact_export facts=['f2', 'f3']

## SOURCE FACTS — B (aws_devops.configure_a_codedeploy_deployment_action_for_a_supplied_ec2_application)   objective: Configure a CodeDeploy action for a supplied EC2 application
B.f1: For EC2 deployments, appspec.yml maps revision files to destinations and lists scripts for deployment lifecycle hooks.   [sources: aws_codedeploy_user_guide#reference-appspec-file.html]
B.f2: Configure the supplied application and deployment group to identify the intended EC2 targets and revision, with the approved service role and installed agent.   [sources: aws_codedeploy_user_guide#deployment-groups.html]
B.f3: Inspect the AppSpec files mapping and hooks, execute the supplied deployment action and verify hook results and application files on the target.   [sources: aws_codedeploy_user_guide#reference-appspec-file.html]
note: Do not invent lifecycle ordering or hook script behavior beyond the supplied AppSpec facts.
PRACTICE ANCHOR (tool_simulation): Configure the supplied CodeDeploy application and deployment group for one intended EC2 target set and application revision. Confirm the approved service role and installed agent, inspect the supplied AppSpec mappings and hooks, and execute one supplied deployment action.  SUCCESS: The deployment uses the intended application, deployment group, EC2 targets and revision with the approved service role and installed agent. Hook results are inspected for that revision, and application files on the target match the supplied AppSpec destinations. Any failed hook or file mismatch is retained as evidence rather than treated as a completed deployment.
ASSESSMENT ANCHOR: verify_appspec_file_mapping_and_hook_results facts=['f1', 'f3']
ASSESSMENT ANCHOR: verify_revision_and_target_alignment facts=['f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Audit KMS-backed audit-storage encryption (SSE-KMS): verify encryption and KMS key-use authority; key-use authority is required for SSE-KMS, not SSE-S3; Audit storage access; Configure a CodeDeploy deployment action for a supplied EC2 application; Configure and verify an EC2 Auto Scaling policy under bounded load; Configure artifact repository access; Configure artifact repository retention; Configure load-balancer listeners, targets and health checks; Configure log retention; Configure managed database backups and create/restore RDS snapshots; require only native RDS and backup foundations, with existing network setup given and no routing or security-group skills assumed; Configure scoped log access; Define an ECS task for a supplied image; Destroy review; Diagnose an IAM denied request from request and policy evidence; Dry run; Execute a reviewed Terraform plan provisioning EC2; directly require the native EC2 instance foundation; Execute a scoped Systems Manager remote command after external shell preparation; Gate infrastructure changes with configuration validation after external declarative/configuration preparation; Handle AWS automation errors with bounded retries and usefu

## LESSON, in learner order

### s01 · explainer · Configure a CodeBuild buildspec for a supplied application
Understand the evidence — 
(definition) A buildspec describes commands and artifacts in YAML. Version 0.2 supports commands in the same shell environment. ⟦A.f1 A:tb1 A:tb2 A:tb3⟧
(mechanism) Put supplied commands in commands lists under needed phases, such as install, pre_build, build and post_build. ⟦A.f2 A:tb1 A:tb2 A:tb3⟧
(mechanism) Match artifacts.files and, when needed, base-directory to generated output. Inspect phase logs and the exported artifact. ⟦A.f3 A:tb1 A:tb2 A:tb3⟧
[SIDE_BY_SIDE] Compare the generated path with the selected file. left_label: Commands | right_label: Export
  left:
[CODE bash]
cat <<'YAML'
version: 0.2
phases:
  build:
    commands:
      - mkdir -p dist
      - cp supplied-release.txt dist/release.txt
artifacts:
  base-directory: dist
  files: [release.txt]
YAML
  annotations: ['Illustrative supplied case — buildspec.yml (YAML)', 'Supplied build-phase commands list generates dist/release.txt.', 'Artifact selection: release.txt within base-directory dist.']
  right:
[DIAGRAM: Illustrative supplied case] nodes=['Build phase: commands succeeded', 'Generated file: dist/release.txt', 'Exported artifact contains: release.txt'] edges=[] alt: Illustrative supplied case: Build phase: commands succeeded; Generated file: dist/release.txt; Exported artifact contains: release.txt

### s02 · explainer · Command success is not verified artifact export.
Understand the evidence — 
(example) For delivery-api, compare the generated output path literally with artifact selection. If commands succeed but the selected path misses the generated file, export is not verified. Do not add unfamiliar commands merely to fill every phase. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧
(mechanism) A buildspec describes commands and artifacts in YAML. Version 0.2 supports commands in the same shell environment. ⟦A.f1 A:tb4 A:tb5⟧
(mechanism) Put supplied commands in commands lists under needed phases, such as install, pre_build, build and post_build. ⟦A.f2 A:tb4 A:tb5⟧
(mechanism) Match artifacts.files and, when needed, base-directory to generated output. Inspect phase logs and the exported artifact. ⟦A.f3 A:tb4 A:tb5⟧

### s03 · check · Judge buildspec evidence
Check your judgement — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] Phase logs show the supplied build commands succeeded, but the exported artifact has not been inspected. Which conclusion is justified?
  ✔ o1: Command success is known; intended artifact export still needs verification.
      why: Correct. Artifact paths must match generated output, and the exported artifact must be inspected.
  ✘ o2: Successful commands prove the intended file was exported.
      why: Not supported. Artifact paths must match generated output, and the exported artifact must be inspected.
  ✘ o3: Artifact selection is irrelevant once commands succeed.
      why: Not supported. Artifact paths must match generated output, and the exported artifact must be inspected.
  feedback✔: Artifact paths must match generated output, and the exported artifact must be inspected.  feedback✘: Artifact paths must match generated output, and the exported artifact must be inspected.  hints: ['Separate the observation already recorded from the additional evidence the conclusion needs.']  remediation→r01
  MEASURES: A:distinguish_command_success_from_verified_artifact_export(f2,f3)   anchors=['assessment:distinguish_command_success_from_verified_artifact_export']
  taught-before-tested: A.f2←s01; A.f3←s01

### s04 · hands_on · Review buildspec evidence
Evidence review — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [classify, core, grading=client] Read each independent supplied evidence excerpt and its reviewer decision. Decide whether that decision is supported by the evidence and the verification requirements, or unsupported. A supported decision may correctly identify a failure; it does not always mean the operation succeeded.
  '```text
version: 0.2
phases:
  build:
    commands:
      - mkdir -p dist
      - cp supplied-release.txt dist/release.txt
artifacts:
  base-directory: dist
  files: [release.txt]
Phase log: both supplied commands succeeded.
Generated: dist/release.txt
Export inspection: release.txt retained and matches generated file.
Reviewer decision: Commands, output selection and export inspection meet the supplied requirement.
```' -> Supported decision
      feedback: The command list produces dist/release.txt, selected relative to dist and confirmed in the export.
  '```text
version: 0.2
phases:
  build:
    commands:
      - mkdir -p dist
      - cp supplied-release.txt dist/release.txt
artifacts:
  base-directory: dist
  files: [other.txt]
Phase log: both supplied commands succeeded.
Generated: dist/release.txt
Export inspection: intended release.txt absent.
Reviewer decision: Accept as complete because phase commands succeeded.
```' -> Unsupported decision
      feedback: Successful commands do not repair selection of the wrong output file.
  '```text
version: 0.2
phases:
  build:
    commands:
      - mkdir -p dist
      - cp supplied-release.txt dist/release.txt
artifacts:
  base-directory: dist
  files: [release.txt]
Phase log: cp command failed.
Generated: dist/release.txt
Export inspection: not performed.
Reviewer decision: Accept without phase or export follow-up.
```' -> Unsupported decision
      feedback: The supplied commands must succeed and the intended exported file must be verified.
  feedback✔: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  feedback✘: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  hints: ['Distinguish saved configuration from observed execution evidence.', 'Check whether the reviewer preserves failures and respects the supplied scope.']  remediation→r02
  MEASURES: A:identify_buildspec_phase_commands_that_produce_the_declared_output(f1,f2); A:verify_artifact_selection_matches_generated_output(f3); A:distinguish_command_success_from_verified_artifact_export(f2,f3)   anchors=['practice', 'assessment:identify_buildspec_phase_commands_that_produce_the_declared_output', 'assessment:verify_artifact_selection_matches_generated_output', 'assessment:distinguish_command_success_from_verified_artifact_export']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f2←s01; A.f3←s01

### s05 · explainer · Configure a CodeDeploy deployment action for a supplied EC2 application
Understand the evidence — 
(definition) For EC2, appspec.yml maps revision files to destinations and lists lifecycle-hook scripts. ⟦B.f1 B:tb1 B:tb2 B:tb3⟧
(mechanism) Use the supplied application and deployment group to identify intended EC2 targets and revision, with the approved service role and installed agent. ⟦B.f2 B:tb1 B:tb2 B:tb3⟧
(mechanism) Inspect AppSpec mappings and hooks; execute the supplied action, then verify hook results and application files on the target. ⟦B.f3 B:tb1 B:tb2 B:tb3⟧
[DIAGRAM: Illustrative supplied deployment evidence] nodes=['Application: delivery-api; deployment group: delivery-sandbox; intended target: approved-node-1; revision: revision-A', 'Approved service role: delivery-deploy-role; agent: installed', 'appspec.yml mapping: release.txt → /opt/delivery-api; AfterInstall script: scripts/check-release.sh', 'revision-A on approved-node-1: AfterInstall succeeded; /opt/delivery-api/release.txt inspected and matches revision-A'] edges=[] alt: Illustrative supplied deployment evidence: Application: delivery-api; deployment group: delivery-sandbox; intended target: approved-node-1; revision: revision-A; Approved service role: delivery-deploy-role; agent: installed; appspec.yml mapping: release.txt → /opt/delivery-api; AfterInstall script: scripts/check-release.sh; revision-A on approved-node-1: AfterInstall succeeded; /opt/delivery-api/release.txt inspected and matches revision-A

### s06 · explainer · An action request is not verified target change.
Understand the evidence — 
(example) Trace one supplied AppSpec mapping to files inspected on the intended target. Relate hook results to that same revision. A requested action, failed hook or successful hook from another deployment cannot establish this revision’s target change. ⟦B.f1 B.f2 B.f3 B:tb4 B:tb5⟧
(mechanism) For EC2, appspec.yml maps revision files to destinations and lists lifecycle-hook scripts. ⟦B.f1 B:tb4 B:tb5⟧
(mechanism) Use the supplied application and deployment group to identify intended EC2 targets and revision, with the approved service role and installed agent. ⟦B.f2 B:tb4 B:tb5⟧
(mechanism) Inspect AppSpec mappings and hooks; execute the supplied action, then verify hook results and application files on the target. ⟦B.f3 B:tb4 B:tb5⟧

### s07 · check · Judge deployment evidence
Check your judgement — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [choice, core, grading=client] The approved deployment is revision-A on approved-node-1, but the action selected revision-B on that target. Which verification conclusion is justified?
  ✘ o1: The correct target alone proves the intended revision was selected.
      why: Not supported. The deployment must use both the intended target set and the intended revision; the agent does not replace that comparison.
  ✘ o2: An installed agent makes revision comparison unnecessary.
      why: Not supported. The deployment must use both the intended target set and the intended revision; the agent does not replace that comparison.
  ✔ o3: Target selection matches, but revision alignment fails; retain the mismatch.
      why: Correct. The deployment must use both the intended target set and the intended revision; the agent does not replace that comparison.
  feedback✔: The deployment must use both the intended target set and the intended revision; the agent does not replace that comparison.  feedback✘: The deployment must use both the intended target set and the intended revision; the agent does not replace that comparison.  hints: ['Separate the observation already recorded from the additional evidence the conclusion needs.']  remediation→r03
  MEASURES: B:verify_revision_and_target_alignment(f2,f3)   anchors=['assessment:verify_revision_and_target_alignment']
  taught-before-tested: B.f2←s05; B.f3←s05

### s08 · hands_on · Review deployment evidence
Evidence review — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each independent supplied evidence excerpt and its reviewer decision. Decide whether that decision is supported by the evidence and the verification requirements, or unsupported. A supported decision may correctly identify a failure; it does not always mean the operation succeeded.
  '```text
Approval: application delivery-api; group delivery-sandbox; target approved-node-1; revision revision-A; role delivery-deploy-role; agent installed.
Selected deployment: all approved values above.
appspec.yml: release.txt maps to /opt/delivery-api; AfterInstall uses scripts/check-release.sh.
revision-A on approved-node-1: AfterInstall succeeded; inspected /opt/delivery-api/release.txt matches revision-A.
Reviewer decision: Accept: selection, hook results and destination file all match.
```' -> Supported decision
      feedback: The intended revision and target are backed by hook and AppSpec destination evidence.
  '```text
Approval: application delivery-api; group delivery-sandbox; target approved-node-1; revision revision-A; role delivery-deploy-role; agent installed.
Selected deployment: revision-B; all other approved values match.
appspec.yml: release.txt maps to /opt/delivery-api; AfterInstall uses scripts/check-release.sh.
revision-A on approved-node-1: AfterInstall succeeded; inspected /opt/delivery-api/release.txt matches revision-A.
Reviewer decision: Accept the deployment as the intended revision.
```' -> Unsupported decision
      feedback: The selected revision differs from the supplied revision even with the correct target.
  '```text
Approval: application delivery-api; group delivery-sandbox; target approved-node-1; revision revision-A; role delivery-deploy-role; agent installed.
Selected deployment: all approved values above.
appspec.yml: release.txt maps to /opt/delivery-api; AfterInstall uses scripts/check-release.sh.
revision-A on approved-node-1: AfterInstall failed; inspected /opt/delivery-api/release.txt does not match revision-A.
Reviewer decision: Keep both failures as evidence and do not mark deployment completed.
```' -> Supported decision
      feedback: A failed hook and file mismatch must remain visible rather than count as completion.
  feedback✔: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  feedback✘: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  hints: ['Distinguish saved configuration from observed execution evidence.', 'Check whether the reviewer preserves failures and respects the supplied scope.']  remediation→r04
  MEASURES: B:verify_appspec_file_mapping_and_hook_results(f1,f3); B:verify_revision_and_target_alignment(f2,f3)   anchors=['practice', 'assessment:verify_appspec_file_mapping_and_hook_results', 'assessment:verify_revision_and_target_alignment']
  taught-before-tested: B.f1←s05; B.f3←s05; B.f2←s05; B.f3←s05

### s09 · recap · Keep these checks separate
Takeaways — 
(takeaway) Match supplied phase commands and generated output selection; verify both phase logs and exported files. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Keep revision, intended targets, AppSpec mappings, hook results and target files connected. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Configure and verify an EC2 Auto Scaling policy under bounded load: Target tracking adjusts Auto Scaling capacity to keep a chosen metric near its target.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Command success is not verified artifact export.
(mechanism) Put supplied commands in commands lists under needed phases, such as install, pre_build, build and post_build. ⟦A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Match artifacts.files and, when needed, base-directory to generated output. Inspect phase logs and the exported artifact. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) For delivery-api, compare the generated output path literally with artifact selection. If commands succeed but the selected path misses the generated file, export is not verified. Do not add unfamiliar commands merely to fill every phase. ⟦A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Command success is not verified artifact export.
(mechanism) A buildspec describes commands and artifacts in YAML. Version 0.2 supports commands in the same shell environment. ⟦A.f1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Put supplied commands in commands lists under needed phases, such as install, pre_build, build and post_build. ⟦A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Match artifacts.files and, when needed, base-directory to generated output. Inspect phase logs and the exported artifact. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) For delivery-api, compare the generated output path literally with artifact selection. If commands succeed but the selected path misses the generated file, export is not verified. Do not add unfamiliar commands merely to fill every phase. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · An action request is not verified target change.
(mechanism) Use the supplied application and deployment group to identify intended EC2 targets and revision, with the approved service role and installed agent. ⟦B.f2 B:tb2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Inspect AppSpec mappings and hooks; execute the supplied action, then verify hook results and application files on the target. ⟦B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
(example) Trace one supplied AppSpec mapping to files inspected on the intended target. Relate hook results to that same revision. A requested action, failed hook or successful hook from another deployment cannot establish this revision’s target change. ⟦B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r04 · An action request is not verified target change.
(mechanism) For EC2, appspec.yml maps revision files to destinations and lists lifecycle-hook scripts. ⟦B.f1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Use the supplied application and deployment group to identify intended EC2 targets and revision, with the approved service role and installed agent. ⟦B.f2 B:tb2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Inspect AppSpec mappings and hooks; execute the supplied action, then verify hook results and application files on the target. ⟦B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
(example) Trace one supplied AppSpec mapping to files inspected on the intended target. Relate hook results to that same revision. A requested action, failed hook or successful hook from another deployment cannot establish this revision’s target change. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧

=========

# EVALUATOR PACKET — Configure and verify an EC2 Auto Scaling policy under bounded load (aws_devops.tile.055)
Tile summary: Compare metric, activities and capacity within approved bounds; above-target load cannot override the maximum.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.configure_and_verify_an_ec2_auto_scaling_policy_under_bounded_load — Configure and verify an EC2 Auto Scaling policy under bounded load

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.configure_and_verify_an_ec2_auto_scaling_policy_under_bounded_load)   objective: Configure an EC2 Auto Scaling policy
A.f1: Target tracking adjusts Auto Scaling capacity to keep a chosen metric near its target value.   [sources: aws_ec2_autoscaling_user_guide#as-scaling-target-tracking.html]
A.f2: Select the approved metric and target value and configure instance warmup along with the group’s minimum, desired and maximum capacities.   [sources: aws_ec2_autoscaling_user_guide#as-scaling-target-tracking.html]
A.f3: Run the bounded load test and compare metric values and scaling activities with resulting capacity; capacity cannot exceed the group’s configured maximum.   [sources: aws_ec2_autoscaling_user_guide#as-scaling-target-tracking.html]
note: Cover EC2 Auto Scaling only; defer load-driven ECS scaling and serverless/database capacity choices.
PRACTICE ANCHOR (tool_simulation): Configure one target-tracking policy on a supplied EC2 Auto Scaling group using the approved metric, target value, instance warmup and minimum, desired and maximum capacities; run the supplied bounded load test.  SUCCESS: The saved configuration matches the supplied settings. Observations correlate metric values and scaling activities with resulting capacity during the bounded test, confirm capacity remains within the configured bounds, and recognize that an above-target metric cannot make capacity exceed the maximum.
ASSESSMENT ANCHOR: verify_capacity_response_against_metric_target facts=['f1', 'f3']
ASSESSMENT ANCHOR: verify_capacity_response_within_configured_bounds facts=['f2', 'f3']

## DATA ASSETS USED
img.scaling_bounded_timeline: image
ds.scaling_timeline: Bounded Auto Scaling test — columns: elapsed_seconds(numerical), metric_name(categorical), metric_value(numerical), metric_target(numerical), scaling_activity(text), resulting_capacity(numerical), minimum_capacity(numerical), desired_capacity_at_start(numerical), maximum_capacity(numerical), instance_warmup_seconds(numerical)
   [0,"CPU utilization",35,50,"No scaling activity",2,1,2,4,120]
   [60,"CPU utilization",70,50,"Scale-out activity: add one instance",3,1,2,4,120]
   [120,"CPU utilization",78,50,"New instance warming up",3,1,2,4,120]
   [180,"CPU utilization",72,50,"Scale-out activity: add one instance",4,1,2,4,120]
   [240,"CPU utilization",68,50,"New instance warming up",4,1,2,4,120]
   [300,"CPU utilization",63,50,"At configured maximum",4,1,2,4,120]
   [360,"CPU utilization",54,50,"At configured maximum",4,1,2,4,120]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Audit KMS-backed audit-storage encryption (SSE-KMS): verify encryption and KMS key-use authority; key-use authority is required for SSE-KMS, not SSE-S3; Audit storage access; Configure artifact repository access; Configure artifact repository retention; Configure load-balancer listeners, targets and health checks; Configure log retention; Configure managed database backups and create/restore RDS snapshots; require only native RDS and backup foundations, with existing network setup given and no routing or security-group skills assumed; Configure scoped log access; Credential expiry; Define an ECS task for a supplied image; Destroy review; Diagnose an IAM denied request from request and policy evidence; Dry run; Execute a reviewed Terraform plan provisioning EC2; directly require the native EC2 instance foundation; Execute a scoped Systems Manager remote command after external shell preparation; Gate infrastructure changes with configuration validation after external declarative/configuration preparation; Handle AWS automation errors with bounded retries and useful reporting; AWS SDK call is a supplied ready function, not an assumed skill or prerequisite; Identify avoidable charges w

## LESSON, in learner order

### s01 · explainer · Configure and verify an EC2 Auto Scaling policy under bounded load
Understand the evidence — 
(definition) Target tracking adjusts Auto Scaling capacity to keep a chosen metric near its target. ⟦A.f1 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Choose the approved metric and target; configure instance warmup and minimum, desired and maximum capacities. ⟦A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) During the bounded load test, compare metric values, scaling activities and resulting capacity. Capacity cannot exceed the configured maximum. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) In the supplied timeline, read metric values alongside activities and capacity. At the maximum, an above-target metric is not permission to exceed the bound. These authored observations are not exact response-time guarantees. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[IMAGE img.scaling_bounded_timeline: Metric target, activities and bounded capacity] alt_text: Two aligned panels show the fictional bounded-test timeline. CPU utilization rises above the approved target while capacity increases from its starting desired capacity to the configured maximum. CPU remains above target at the maximum; capacity does not exceed that bound. The lower panel labels scale-out activities and the maximum-capacity observation, minimum and maximum bounds and the starting desired capacity; the footer states the supplied instance warmup. These are authored observations, not exact response-time guarantees.
  rendered by pyodide 0.29.5 from datasets ['ds.scaling_timeline'] with this code (the gate re-renders it to the same bytes):
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("scaling_timeline.csv")
fig, (metric_ax, capacity_ax) = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
metric_ax.plot(df["elapsed_seconds"], df["metric_value"], marker="o", label="Observed CPU utilization")
metric_ax.plot(df["elapsed_seconds"], df["metric_target"], linestyle="--", label="Approved metric target")
metric_ax.set_ylabel("CPU utilization (%)")
metric_ax.legend(loc="upper left")
metric_ax.grid(alpha=0.3)
capacity_ax.step(df["elapsed_seconds"], df["resulting_capacity"], where="post", marker="o", label="Resulting capacity")
capacity_ax.axhline(df["maximum_capacity"].iloc[0], color="red", linestyle="--", label="Maximum capacity")
capacity_ax.axhline(df["minimum_capacity"].iloc[0], color="gray", linestyle=":", label="Minimum capacity")
capacity_ax.axhline(df["desired_capacity_at_start"].iloc[0], color="green", linestyle=":", label="Desired capacity at start")
for i in [1, 3, 5]:
    r = df.iloc[i]
    capacity_ax.annotate(r["scaling_activity"], (r["elapsed_seconds"], r["resulting_capacity"]), xytext=(7, -32 if i == 3 else -20), textcoords="offset points", fontsize=8)
capacity_ax.set_xlabel("Elapsed time in bounded test (seconds)")
capacity_ax.set_ylabel("Capacity (instances)")
capacity_ax.set_yticks(range(int(df["minimum_capacity"].iloc[0]), int(df["maximum_capacity"].iloc[0]) + 1))
capacity_ax.set_ylim(0.5, df["maximum_capacity"].iloc[0] + 1.4)
capacity_ax.legend(loc="upper left", fontsize=8)
capacity_ax.grid(alpha=0.3)
fig.suptitle("Fictional bounded Auto Scaling test")
fig.text(0.5, 0.02, "Instance warmup: " + str(df["instance_warmup_seconds"].iloc[0]) + " seconds; desired capacity is the starting baseline.", ha="center", fontsize=9)
fig.tight_layout(rect=(0, 0.04, 1, 0.95))


### s02 · video · Trace the supplied evidence
Evidence walkthrough — 
[VIDEO How target tracking responds to rising CPU utilization] bridge-before: Watch how rising CPU utilization leads target tracking to add capacity toward the chosen target. The five-instance increase belongs to this example; it is not a universal rule. | bridge-after: The clip explains the response mechanism, but omits warmup, group capacity settings and bounded-test verification. The text covers those settings and comparing metrics, scaling activities and resulting capacity against the maximum.
  - 9BlsFNBnKHc 931-995s facts=['f1'] label: Target tracking adds capacity toward a CPU utilization target | summary: Target tracking adjusts capacity toward a chosen metric target, much like a thermostat regulates temperature. In this example, the target is average CPU utilization of 50%. Increased traffic raises utilization to 75%, and target tracking determines that adding five instances will bring utilization back toward the target. Five instances is the result in this example, not a fixed scaling increment.

### s03 · check · Judge bounded scaling evidence
Check your judgement — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] During a bounded target-tracking test, the metric remains above target while capacity is at its configured maximum. Which interpretation is valid?
  ✘ o1: An above-target metric proves that the maximum setting is ignored.
      why: Not supported. Capacity cannot exceed the configured maximum even when the metric remains above target.
  ✔ o2: The metric cannot cause capacity to exceed that maximum.
      why: Correct. Capacity cannot exceed the configured maximum even when the metric remains above target.
  ✘ o3: Target tracking must exceed the configured maximum to reach the metric target.
      why: Not supported. Capacity cannot exceed the configured maximum even when the metric remains above target.
  feedback✔: Capacity cannot exceed the configured maximum even when the metric remains above target.  feedback✘: Capacity cannot exceed the configured maximum even when the metric remains above target.  hints: ['Separate the observation already recorded from the additional evidence the conclusion needs.']  remediation→r01
  MEASURES: A:verify_capacity_response_within_configured_bounds(f2,f3)   anchors=['assessment:verify_capacity_response_within_configured_bounds']
  taught-before-tested: A.f2←s01; A.f3←s01

### s04 · hands_on · Review bounded scaling evidence
Evidence review — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each independent supplied evidence excerpt and its reviewer decision. Decide whether that decision is supported by the evidence and the verification requirements, or unsupported. A supported decision may correctly identify a failure; it does not always mean the operation succeeded.
  '| elapsed_seconds | metric_name | metric_value | metric_target | scaling_activity | resulting_capacity | minimum_capacity | desired_capacity_at_start | maximum_capacity | instance_warmup_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | CPU utilization | 35 | 50 | No scaling activity | 2 | 1 | 2 | 4 | 120 |
| 60 | CPU utilization | 70 | 50 | Scale-out activity: add one instance | 3 | 1 | 2 | 4 | 120 |
| 120 | CPU utilization | 78 | 50 | New instance warming up | 3 | 1 | 2 | 4 | 120 |
| 180 | CPU utilization | 72 | 50 | Scale-out activity: add one instance | 4 | 1 | 2 | 4 | 120 |
| 240 | CPU utilization | 68 | 50 | New instance warming up | 4 | 1 | 2 | 4 | 120 |
| 300 | CPU utilization | 63 | 50 | At configured maximum | 4 | 1 | 2 | 4 | 120 |
| 360 | CPU utilization | 54 | 50 | At configured maximum | 4 | 1 | 2 | 4 | 120 |

Saved settings: match all supplied metric, target, warmup and min/desired/max values.

Reviewer decision: Accept configuration and bounded response; correlate activities with capacity, without assuming an exact response time.' -> Supported decision
      feedback: The complete timeline links metric values, activities and capacity within the saved bounds.
  '```text
{"elapsed_seconds": 360, "metric_name": "CPU utilization", "metric_value": 54, "metric_target": 50, "scaling_activity": "At configured maximum", "resulting_capacity": 4, "minimum_capacity": 1, "desired_capacity_at_start": 2, "maximum_capacity": 4, "instance_warmup_seconds": 120}
Reviewer decision: Above-target metric means capacity must grow beyond maximum_capacity.
```' -> Unsupported decision
      feedback: Target tracking does not override the group maximum.
  '| elapsed_seconds | metric_name | metric_value | metric_target | scaling_activity | resulting_capacity | minimum_capacity | desired_capacity_at_start | maximum_capacity | instance_warmup_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | CPU utilization | 35 | 50 | No scaling activity | 2 | 1 | 2 | 4 | 120 |
| 60 | CPU utilization | 70 | 50 | Scale-out activity: add one instance | 3 | 1 | 2 | 4 | 120 |
| 120 | CPU utilization | 78 | 50 | New instance warming up | 3 | 1 | 2 | 4 | 120 |
| 180 | CPU utilization | 72 | 50 | Scale-out activity: add one instance | 4 | 1 | 2 | 4 | 120 |
| 240 | CPU utilization | 68 | 50 | New instance warming up | 4 | 1 | 2 | 4 | 120 |
| 300 | CPU utilization | 63 | 50 | At configured maximum | 4 | 1 | 2 | 4 | 120 |
| 360 | CPU utilization | 54 | 50 | At configured maximum | 4 | 1 | 2 | 4 | 120 |

Saved settings: warmup differs from supplied instance_warmup_seconds.

Reviewer decision: Approve settings because capacity stayed in bounds.' -> Unsupported decision
      feedback: Bounded capacity is not proof that the saved warmup matches the approved configuration.
  feedback✔: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  feedback✘: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  hints: ['Distinguish saved configuration from observed execution evidence.', 'Check whether the reviewer preserves failures and respects the supplied scope.']  remediation→r02
  MEASURES: A:verify_capacity_response_against_metric_target(f1,f3); A:verify_capacity_response_within_configured_bounds(f2,f3)   anchors=['practice', 'assessment:verify_capacity_response_against_metric_target', 'assessment:verify_capacity_response_within_configured_bounds']
  taught-before-tested: A.f1←s01; A.f3←s01; A.f2←s01; A.f3←s01

### s05 · recap · Keep these checks separate
Takeaways — 
(takeaway) Compare metric, activities and capacity within approved bounds; above-target load cannot override the maximum. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Configure artifact repository access: An ECR repository policy grants specified principals operations such as image pulls or image-layer uploads.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Target tracking is bounded, not unlimited capacity.
(mechanism) Choose the approved metric and target; configure instance warmup and minimum, desired and maximum capacities. ⟦A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) During the bounded load test, compare metric values, scaling activities and resulting capacity. Capacity cannot exceed the configured maximum. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) In the supplied timeline, read metric values alongside activities and capacity. At the maximum, an above-target metric is not permission to exceed the bound. These authored observations are not exact response-time guarantees. ⟦A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Target tracking is bounded, not unlimited capacity.
(mechanism) Target tracking adjusts Auto Scaling capacity to keep a chosen metric near its target. ⟦A.f1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Choose the approved metric and target; configure instance warmup and minimum, desired and maximum capacities. ⟦A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) During the bounded load test, compare metric values, scaling activities and resulting capacity. Capacity cannot exceed the configured maximum. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) In the supplied timeline, read metric values alongside activities and capacity. At the maximum, an above-target metric is not permission to exceed the bound. These authored observations are not exact response-time guarantees. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Safe ECR repository operation (aws_devops.tile.056)
Tile summary: Test publisher, consumer and unapproved access; separate repository authorization from identity-policy authentication. Preview expiry by digest and protect still-needed versions by excluding them from eligibility.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.configure_artifact_repository_access — Configure artifact repository access
B = aws_devops.configure_artifact_repository_retention — Configure artifact repository retention

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.configure_artifact_repository_access)   objective: Authorize artifact repository access
A.f1: An ECR repository policy grants specified principals repository operations such as pulling images or uploading image layers.   [sources: aws_ecr_user_guide#repository-policy-examples.html]
A.f2: Scope the supplied policy’s principals and actions to approved publishers and consumers, then test push and pull and an unapproved principal.   [sources: aws_ecr_user_guide#repository-policy-examples.html]
A.f3: ECR authentication also requires ecr:GetAuthorizationToken through an identity policy; repository permissions alone do not grant that action.   [sources: aws_ecr_user_guide#repository-policy-examples.html]
note: Use supplied publisher/consumer roles; do not broaden repository scope to fix an unexplained denial.
PRACTICE ANCHOR (tool_simulation): Apply one supplied ECR repository policy, scoping principals and repository actions to the approved publisher and consumer. Check their supplied identity policies for ecr:GetAuthorizationToken, then run the supplied push, pull and unapproved-principal tests.  SUCCESS: The repository policy grants only the approved principals their intended repository operations. The publisher can push, the consumer can pull, and the supplied unapproved principal is denied repository access. The approved identities have ecr:GetAuthorizationToken through their identity policies. Policy scopes, test identities and observed results are retained without broadening access to resolve a denial.
ASSESSMENT ANCHOR: verify_publisher_push_consumer_pull_and_unapproved_principal_denial facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_identity_policy_authorizes_ecr_authentication facts=['f3']

## SOURCE FACTS — B (aws_devops.configure_artifact_repository_retention)   objective: Configure artifact repository retention
B.f1: ECR lifecycle policies select images using criteria such as tag status and count or age and expire matching images.   [sources: aws_ecr_user_guide#LifecyclePolicies.html]
B.f2: Use rulePriority, selection and action fields to express the supplied retention policy and run a lifecycle preview before applying it.   [sources: aws_ecr_user_guide#LifecyclePolicies.html]
B.f3: Check previewed digests against deployed versions; exclude still-needed versions from eligible expiry rather than assuming deployment makes an image immune to lifecycle rules.   [sources: aws_ecr_user_guide#LifecyclePolicies.html]
note: Do not invent lifecycle-policy JSON or retention durations; use supplied policy criteria.
PRACTICE ANCHOR (tool_simulation): Configure one bounded ECR lifecycle policy using supplied approved criteria and image tags, express it with rulePriority, selection and action fields, preview its results, and compare eligible digests with the supplied deployed-version record before applying it.  SUCCESS: The policy matches the supplied retention criteria. Preview evidence shows that only eligible old images are selected and no deployed or otherwise still-needed digest is eligible for expiry. Any unsafe selection is revised and previewed again before the policy is applied.
ASSESSMENT ANCHOR: verify_retention_selection_and_preview facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_needed_digests_are_excluded_from_expiry facts=['f3']

## DATA ASSETS USED
ds.repository_access_tests: Publisher, consumer and unapproved access tests — columns: principal(identifier), approved_role(categorical), repository(identifier), operation(categorical), repository_grant(text), identity_authentication_action(text), identity_authentication_allowed(categorical), expected_result(categorical), observed_result(categorical)
   ["delivery-publisher","publisher","delivery-api","push","Supplied image-layer upload and image-publish operations","ecr:GetAuthorizationToken",true,"allowed","allowed"]
   ["delivery-consumer","consumer","delivery-api","pull","Supplied image-pull operations","ecr:GetAuthorizationToken",true,"allowed","allowed"]
   ["unapproved-reader","unapproved","delivery-api","pull","No repository grant","ecr:GetAuthorizationToken",true,"denied","denied"]
ds.retention_preview: Image retention preview and needed versions — columns: digest(identifier), tags(text), tag_status(categorical), age_days(numerical), age_threshold_days(numerical), rulePriority(numerical), selection(text), action(categorical), eligible(categorical), deployed(categorical), still_needed(categorical), previewed_expiry(categorical)
   ["sha256:803f4d7b1b5ef95b5a7467b65ec0f62c2f5c1a99fab92707d8910d1603750469","release-current","tagged",45,30,1,"Untagged images older than 30 days","expire",false,true,true,false]
   ["sha256:a8e7366785f60b4e5af2e2b44cad9259f8b9661d4268503efe4bb12e51d15aaf","release-rollback","tagged",60,30,1,"Untagged images older than 30 days","expire",false,false,true,false]
   ["sha256:04c0b9af03b847028a63dff5a9c1393e98082146378251f7c8e904d506a28335","","untagged",40,30,1,"Untagged images older than 30 days","expire",true,false,false,true]
   ["sha256:a55b050cb15206c8cdfe242657088dc99e97a88ff13992688fabc36262bfdfb5","","untagged",10,30,1,"Untagged images older than 30 days","expire",false,false,false,false]
   ["sha256:3428dad144a085557ad6d5eda09054f4bb2f8111232389d3dbdd07b319be52b2","release-candidate","tagged",5,30,1,"Untagged images older than 30 days","expire",false,false,true,false]
   variant var.retention_unsafe: 4 ops; planted: issue.needed_image_expiry(other)

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply an approved security baseline to sandbox accounts; Audit KMS-backed audit-storage encryption (SSE-KMS): verify encryption and KMS key-use authority; key-use authority is required for SSE-KMS, not SSE-S3; Audit storage access; Configure artifact repository retention; Configure load-balancer listeners, targets and health checks; Configure log retention; Configure managed database backups and create/restore RDS snapshots; require only native RDS and backup foundations, with existing network setup given and no routing or security-group skills assumed; Configure scoped log access; Credential expiry; Define an ECS task for a supplied image; Destroy review; Diagnose an IAM denied request from request and policy evidence; Dry run; Ecs task identity; Execute a reviewed Terraform plan provisioning EC2; directly require the native EC2 instance foundation; Execute a scoped Systems Manager remote command after external shell preparation; Gate infrastructure changes with configuration validation after external declarative/configuration preparation; Handle AWS automation errors with bounded retries and useful reporting; AWS SDK call is a supplied ready function, not an assumed skill or prer

## LESSON, in learner order

### s01 · explainer · Configure artifact repository access
Understand the evidence — 
(definition) An ECR repository policy grants specified principals operations such as image pulls or image-layer uploads. ⟦A.f1 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Scope principals and actions to approved publishers and consumers; test push, pull and an unapproved principal. ⟦A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Authentication also needs ecr:GetAuthorizationToken through an identity policy. Repository permissions alone do not grant that action. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Compare the publisher’s push, consumer’s pull and unapproved principal’s test. Authentication and repository authorization are separate: an authenticated principal still needs the relevant repository grant. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[SIDE_BY_SIDE] Authentication and repository authorization need separate evidence. left_label: Repository grants | right_label: Authentication and tests
  left:
[TABLE ds.repository_access_tests cols=['principal', 'repository', 'operation', 'repository_grant'] ] caption: 
  right:
[TABLE ds.repository_access_tests cols=['principal', 'identity_authentication_action', 'identity_authentication_allowed', 'expected_result', 'observed_result'] ] caption: 

### s02 · check · Judge repository access evidence
Check your judgement — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] A principal has repository pull permissions but no identity-policy authorization for ecr:GetAuthorizationToken. What does the repository policy alone establish?
  ✔ o1: Repository pull permission, not authorization for the authentication action.
      why: Correct. ECR authentication requires ecr:GetAuthorizationToken through an identity policy.
  ✘ o2: Authorization for ecr:GetAuthorizationToken as well as pull.
      why: Not supported. ECR authentication requires ecr:GetAuthorizationToken through an identity policy.
  ✘ o3: Authentication is unnecessary whenever repository pull is granted.
      why: Not supported. ECR authentication requires ecr:GetAuthorizationToken through an identity policy.
  feedback✔: ECR authentication requires ecr:GetAuthorizationToken through an identity policy.  feedback✘: ECR authentication requires ecr:GetAuthorizationToken through an identity policy.  hints: ['Separate the observation already recorded from the additional evidence the conclusion needs.']  remediation→r01
  MEASURES: A:verify_identity_policy_authorizes_ecr_authentication(f3)   anchors=['assessment:verify_identity_policy_authorizes_ecr_authentication']
  taught-before-tested: A.f3←s01

### s03 · hands_on · Review repository access evidence
Evidence review — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [classify, core, grading=client] Read each independent supplied evidence excerpt and its reviewer decision. Decide whether that decision is supported by the evidence and the verification requirements, or unsupported. A supported decision may correctly identify a failure; it does not always mean the operation succeeded.
  '| Field | Observation 1 | Observation 2 | Observation 3 |
| --- | --- | --- | --- |
| principal | delivery-publisher | delivery-consumer | unapproved-reader |
| approved_role | publisher | consumer | unapproved |
| repository | delivery-api | delivery-api | delivery-api |
| operation | push | pull | pull |
| repository_grant | Supplied image-layer upload and image-publish operations | Supplied image-pull operations | No repository grant |
| identity_authentication_action | ecr:GetAuthorizationToken | ecr:GetAuthorizationToken | ecr:GetAuthorizationToken |
| identity_authentication_allowed | true | true | true |
| expected_result | allowed | allowed | denied |
| observed_result | allowed | allowed | denied |

Policy review: only listed approved publishers/consumers receive their intended repository operations; no broader grants.

Reviewer decision: Accept scoped grants and authentication, with successful publisher/consumer tests and denied unapproved pull.' -> Supported decision
      feedback: The evidence separates identity authentication from repository grants and covers all three identities.
  '| Field | Observation 1 | Observation 2 | Observation 3 |
| --- | --- | --- | --- |
| principal | delivery-publisher | delivery-consumer | unapproved-reader |
| approved_role | publisher | consumer | unapproved |
| repository | delivery-api | delivery-api | delivery-api |
| operation | push | pull | pull |
| repository_grant | Supplied image-layer upload and image-publish operations | Supplied image-pull operations | No repository grant |
| identity_authentication_action | ecr:GetAuthorizationToken | ecr:GetAuthorizationToken | ecr:GetAuthorizationToken |
| identity_authentication_allowed | true | true | true |
| expected_result | allowed | allowed | denied |
| observed_result | allowed | allowed | denied |

Policy review: only listed approved publishers/consumers receive their intended repository operations; no broader grants.

Reviewer decision: Unapproved authentication means its repository pull should also be allowed.' -> Unsupported decision
      feedback: Authentication permission does not grant repository pull.
  '| Field | Observation 1 | Observation 2 | Observation 3 |
| --- | --- | --- | --- |
| principal | delivery-publisher | delivery-consumer | unapproved-reader |
| approved_role | publisher | consumer | unapproved |
| repository | delivery-api | delivery-api | delivery-api |
| operation | push | pull | pull |
| repository_grant | Supplied image-layer upload and image-publish operations | Supplied image-pull operations | No repository grant |
| identity_authentication_action | ecr:GetAuthorizationToken | ecr:GetAuthorizationToken | ecr:GetAuthorizationToken |
| identity_authentication_allowed | true | true | true |
| expected_result | allowed | allowed | denied |
| observed_result | allowed | allowed | denied |

Proposed change: remove approved principals’ identity authorization for ecr:GetAuthorizationToken; keep repository grants.

Policy review: only listed approved publishers/consumers receive their intended repository operations; no broader grants.

Reviewer decision: Publisher and consumer authentication will still be authorized by the repository policy.' -> Unsupported decision
      feedback: Repository permissions alone do not grant ecr:GetAuthorizationToken.
  feedback✔: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  feedback✘: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  hints: ['Distinguish saved configuration from observed execution evidence.', 'Check whether the reviewer preserves failures and respects the supplied scope.']  remediation→r02
  MEASURES: A:verify_publisher_push_consumer_pull_and_unapproved_principal_denial(f1,f2); A:verify_identity_policy_authorizes_ecr_authentication(f3)   anchors=['practice', 'assessment:verify_publisher_push_consumer_pull_and_unapproved_principal_denial', 'assessment:verify_identity_policy_authorizes_ecr_authentication']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s04 · explainer · Configure artifact repository retention
Understand the evidence — 
(definition) ECR lifecycle policies expire images selected by criteria such as tag status and count or age. ⟦B.f1 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Express supplied retention using rulePriority, selection and action. Run a lifecycle preview before applying it. ⟦B.f2 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Compare previewed digests with deployed versions. Exclude still-needed versions from eligible expiry; deployment does not make images immune. ⟦B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(example) Use the preview table to compare eligible digests with deployed and still-needed flags. If a needed digest would expire, revise eligibility before applying the policy; a deployment reference is not protection. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.retention_preview cols=['digest', 'tags', 'tag_status', 'age_days', 'age_threshold_days', 'rulePriority', 'selection', 'action', 'eligible', 'deployed', 'still_needed', 'previewed_expiry'] ] caption: 

### s05 · video · Trace the supplied evidence
Evidence walkthrough — 
[VIDEO ECR lifecycle selection and preview] bridge-before: Watch how tag prefixes, tag status and image counts define eligibility. The clip calls lifecycle preview a “dry run”; its example counts are not your approved retention criteria. | bridge-after: The clip demonstrates count-based selection and application, but not the complete rulePriority, selection and action structure or deployed-digest checks. The text supplies both; deployment does not protect an eligible image.
  - H73uX0TOX9g 177-341s facts=['f1'] label: Preview and apply count-based ECR lifecycle rules | summary: ECR lifecycle policies can clean up older images while retaining recent versions. This example starts in the lifecycle-rule preview tab and sets rule priorities, tag prefixes and image-count thresholds for tagged images. It also adds a separate rule selecting untagged images above a count threshold. After reviewing the result, the policy is applied. These counts illustrate the creator's repository needs; use the supplied approved criteria for your own retention decision.

### s06 · check · Judge retention preview evidence
Check your judgement — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [choice, core, grading=client] A lifecycle preview includes a digest still used by a deployed version. What should happen before applying the policy?
  ✘ o1: Apply unchanged because deployment automatically prevents expiry.
      why: Not supported. Deployed versions are not immune to lifecycle rules; exclude needed digests from eligible expiry.
  ✘ o2: Skip digest comparison because lifecycle rules only affect unused images.
      why: Not supported. Deployed versions are not immune to lifecycle rules; exclude needed digests from eligible expiry.
  ✔ o3: Revise selection to exclude the still-needed digest and preview again.
      why: Correct. Deployed versions are not immune to lifecycle rules; exclude needed digests from eligible expiry.
  feedback✔: Deployed versions are not immune to lifecycle rules; exclude needed digests from eligible expiry.  feedback✘: Deployed versions are not immune to lifecycle rules; exclude needed digests from eligible expiry.  hints: ['Separate the observation already recorded from the additional evidence the conclusion needs.']  remediation→r03
  MEASURES: B:verify_needed_digests_are_excluded_from_expiry(f3)   anchors=['assessment:verify_needed_digests_are_excluded_from_expiry']
  taught-before-tested: B.f3←s04

### s07 · hands_on · Review retention preview evidence
Evidence review — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each independent supplied evidence excerpt and its reviewer decision. Decide whether that decision is supported by the evidence and the verification requirements, or unsupported. A supported decision may correctly identify a failure; it does not always mean the operation succeeded.
  '| Field | Observation 1 | Observation 2 | Observation 3 | Observation 4 | Observation 5 |
| --- | --- | --- | --- | --- | --- |
| digest | sha256:803f4d7b1b5ef95b5a7467b65ec0f62c2f5c1a99fab92707d8910d1603750469 | sha256:a8e7366785f60b4e5af2e2b44cad9259f8b9661d4268503efe4bb12e51d15aaf | sha256:04c0b9af03b847028a63dff5a9c1393e98082146378251f7c8e904d506a28335 | sha256:a55b050cb15206c8cdfe242657088dc99e97a88ff13992688fabc36262bfdfb5 | sha256:3428dad144a085557ad6d5eda09054f4bb2f8111232389d3dbdd07b319be52b2 |
| tags | release-current | release-rollback |  |  | release-candidate |
| tag_status | tagged | tagged | untagged | untagged | tagged |
| age_days | 45 | 60 | 40 | 10 | 5 |
| age_threshold_days | 30 | 30 | 30 | 30 | 30 |
| rulePriority | 1 | 1 | 1 | 1 | 1 |
| selection | Untagged images older than 30 days | Untagged images older than 30 days | Untagged images older than 30 days | Untagged images older than 30 days | Untagged images older than 30 days |
| action | expire | expire | expire | expire | expire |
| eligible | false | false | true | false | false |
| deployed | true | false | false | false | false |
| still_needed | true | true | false | false | true |
| previewed_expiry | false | false | true | false | false |

Approved criteria match selection, rulePriority and action; this preview was inspected before application.

Reviewer decision: Accept: eligible old images expire and all deployed/still-needed digests are excluded.' -> Supported decision
      feedback: Preview selection matches criteria and excludes every needed digest.
  '| Field | Observation 1 |
| --- | --- |
| digest | sha256:803f4d7b1b5ef95b5a7467b65ec0f62c2f5c1a99fab92707d8910d1603750469 |
| tags | release-current |
| tag_status | tagged |
| age_days | 45 |
| age_threshold_days | 30 |
| rulePriority | 1 |
| selection | Untagged images older than 30 days |
| action | expire |
| eligible | false |
| deployed | true |
| still_needed | true |
| previewed_expiry | false |

Alternative proposed selection: all images older than age_threshold_days; preview now includes this deployed digest.

Reviewer decision: Apply unchanged because deployment protects the digest.' -> Unsupported decision
      feedback: A needed digest must be excluded from eligibility; deployment is not immunity.
  '| Field | Observation 1 | Observation 2 | Observation 3 | Observation 4 | Observation 5 |
| --- | --- | --- | --- | --- | --- |
| digest | sha256:803f4d7b1b5ef95b5a7467b65ec0f62c2f5c1a99fab92707d8910d1603750469 | sha256:a8e7366785f60b4e5af2e2b44cad9259f8b9661d4268503efe4bb12e51d15aaf | sha256:04c0b9af03b847028a63dff5a9c1393e98082146378251f7c8e904d506a28335 | sha256:a55b050cb15206c8cdfe242657088dc99e97a88ff13992688fabc36262bfdfb5 | sha256:3428dad144a085557ad6d5eda09054f4bb2f8111232389d3dbdd07b319be52b2 |
| tags | release-current | release-rollback |  |  | release-candidate |
| tag_status | tagged | tagged | untagged | untagged | tagged |
| age_days | 45 | 60 | 40 | 10 | 5 |
| age_threshold_days | 30 | 30 | 30 | 30 | 30 |
| rulePriority | 1 | 1 | 1 | 1 | 1 |
| selection | Untagged images older than 30 days | Untagged images older than 30 days | Untagged images older than 30 days | Untagged images older than 30 days | Untagged images older than 30 days |
| action | expire | expire | expire | expire | expire |
| eligible | false | false | true | false | false |
| deployed | true | false | false | false | false |
| still_needed | true | true | false | false | true |
| previewed_expiry | false | false | true | false | false |

Proposed policy changed after this preview; revised preview not inspected.

Reviewer decision: Apply the changed policy using the old preview as proof of safety.' -> Unsupported decision
      feedback: Preview the policy that will be applied and compare its eligible digests with needed versions.
  feedback✔: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  feedback✘: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  hints: ['Distinguish saved configuration from observed execution evidence.', 'Check whether the reviewer preserves failures and respects the supplied scope.']  remediation→r04
  MEASURES: B:verify_retention_selection_and_preview(f1,f2); B:verify_needed_digests_are_excluded_from_expiry(f3)   anchors=['practice', 'assessment:verify_retention_selection_and_preview', 'assessment:verify_needed_digests_are_excluded_from_expiry']
  taught-before-tested: B.f1←s04; B.f2←s04; B.f3←s04

### s08 · recap · Keep these checks separate
Takeaways — 
(takeaway) Test publisher, consumer and unapproved access; separate repository authorization from identity-policy authentication. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Preview expiry by digest and protect still-needed versions by excluding them from eligibility. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Configure load-balancer listeners, targets and health checks: An ALB listener evaluates routing rules and forwards matching requests to a target group.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Authentication is not repository authorization.
(mechanism) Authentication also needs ecr:GetAuthorizationToken through an identity policy. Repository permissions alone do not grant that action. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Compare the publisher’s push, consumer’s pull and unapproved principal’s test. Authentication and repository authorization are separate: an authenticated principal still needs the relevant repository grant. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Authentication is not repository authorization.
(mechanism) An ECR repository policy grants specified principals operations such as image pulls or image-layer uploads. ⟦A.f1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Scope principals and actions to approved publishers and consumers; test push, pull and an unapproved principal. ⟦A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Authentication also needs ecr:GetAuthorizationToken through an identity policy. Repository permissions alone do not grant that action. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Compare the publisher’s push, consumer’s pull and unapproved principal’s test. Authentication and repository authorization are separate: an authenticated principal still needs the relevant repository grant. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Deployment is not immunity from expiry.
(mechanism) Compare previewed digests with deployed versions. Exclude still-needed versions from eligible expiry; deployment does not make images immune. ⟦B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
(example) Use the preview table to compare eligible digests with deployed and still-needed flags. If a needed digest would expire, revise eligibility before applying the policy; a deployment reference is not protection. ⟦B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r04 · Deployment is not immunity from expiry.
(mechanism) ECR lifecycle policies expire images selected by criteria such as tag status and count or age. ⟦B.f1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Express supplied retention using rulePriority, selection and action. Run a lifecycle preview before applying it. ⟦B.f2 B:tb2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Compare previewed digests with deployed versions. Exclude still-needed versions from eligible expiry; deployment does not make images immune. ⟦B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
(example) Use the preview table to compare eligible digests with deployed and still-needed flags. If a needed digest would expire, revise eligibility before applying the policy; a deployment reference is not protection. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧

=========

# EVALUATOR PACKET — Configure load-balancer listeners, targets and health checks (aws_devops.tile.058)
Tile summary: Check listener routing and backend health settings; remember the all-unhealthy fail-open exception.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.configure_load_balancer_listeners_targets_and_health_checks — Configure load-balancer listeners, targets and health checks

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.configure_load_balancer_listeners_targets_and_health_checks)   objective: Configure an ALB request path
A.f1: An Application Load Balancer listener evaluates routing rules and forwards matching requests to a target group.   [sources: aws_elb_user_guide#../application/load-balancer-target-groups.html]
A.f2: Configure the supplied listener protocol and port, forwarding rule and registered target protocol/port, then test the endpoint.   [sources: aws_elb_user_guide#../application/load-balancer-target-groups.html]
A.f3: Configure the health-check path, port and success codes to match the backend and inspect target health reasons when a request path fails.   [sources: aws_elb_user_guide#../application/target-group-health-checks.html]
A.f4: An ALB normally routes to healthy registered targets, but when every registered target in a target group is unhealthy it fails open and routes to those unhealthy targets.   [sources: aws_elb_user_guide#../application/target-group-health-checks.html]
note: Preserve fails-open exception; do not introduce unsupported load-balancer algorithm or DNS behavior.
PRACTICE ANCHOR (tool_simulation): Configure one supplied Application Load Balancer listener-to-target-group path, including the listener protocol and port, forwarding rule, registered target protocol and port, and backend-matched health-check path, port and success codes. Test the supplied endpoint and inspect target health reasons.  SUCCESS: The listener forwards matching requests to the intended target group, the registered target and health-check settings match the supplied backend requirements, target health confirms a healthy backend, and the supplied endpoint returns the expected response.
ASSESSMENT ANCHOR: diagnose_listener_rule_and_target_configuration_mismatches facts=['f1', 'f2']
ASSESSMENT ANCHOR: diagnose_health_check_mismatches_using_target_health_reasons facts=['f3']
ASSESSMENT ANCHOR: distinguish_normal_healthy_target_routing_from_all_unhealthy_fail_open facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply an approved security baseline to sandbox accounts; Apply bounded EKS workload configuration and secrets after external configuration/secrets preparation; Audit KMS-backed audit-storage encryption (SSE-KMS): verify encryption and KMS key-use authority; key-use authority is required for SSE-KMS, not SSE-S3; Audit storage access; Configure log retention; Configure managed database backups and create/restore RDS snapshots; require only native RDS and backup foundations, with existing network setup given and no routing or security-group skills assumed; Configure scoped log access; Credential expiry; Define an ECS task for a supplied image; Destroy review; Diagnose an IAM denied request from request and policy evidence; Dry run; Ecs task identity; Execute a reviewed Terraform plan provisioning EC2; directly require the native EC2 instance foundation; Execute a scoped Systems Manager remote command after external shell preparation; Gate infrastructure changes with configuration validation after external declarative/configuration preparation; Handle AWS automation errors with bounded retries and useful reporting; AWS SDK call is a supplied ready function, not an assumed skill or prer

## LESSON, in learner order

### s01 · explainer · Configure load-balancer listeners, targets and health checks
Understand the evidence — 
(definition) An ALB listener evaluates routing rules and forwards matching requests to a target group. ⟦A.f1 A:tb1 A:tb2 A:tb3⟧
(mechanism) Configure supplied listener protocol/port, forwarding rule and registered target protocol/port; test the endpoint. ⟦A.f2 A:tb1 A:tb2 A:tb3⟧
(mechanism) Match health-check path, port and success codes to the backend. Inspect target health reasons when a request path fails. ⟦A.f3 A:tb1 A:tb2 A:tb3⟧
(mechanism) ALB normally routes to healthy registered targets. If every registered target in a group is unhealthy, it fails open and routes to those unhealthy targets. ⟦A.f4 A:tb1 A:tb2 A:tb3⟧
[DIAGRAM: Routing and health review] nodes=['Supplied listener protocol/port and routing rule', 'Registered target group protocol/port', 'Backend health-check path, port and success codes', 'Endpoint test and target health reasons', 'Normally healthy targets; all registered targets unhealthy → fail open to those targets'] edges=[('n1', 'n2', None), ('n2', 'n3', None), ('n3', 'n4', None), ('n4', 'n5', None)] alt: Routing and health review: Supplied listener protocol/port and routing rule → Registered target group protocol/port → Backend health-check path, port and success codes → Endpoint test and target health reasons → Normally healthy targets; all registered targets unhealthy → fail open to those targets

### s02 · explainer · Unhealthy does not always mean no routed traffic.
Understand the evidence — 
(example) If the supplied health-check path differs from the backend requirement, inspect health reasons and make the approved correction rather than changing unrelated settings. An unhealthy label is not an unconditional no-traffic guarantee: keep the all-unhealthy fail-open exception beside normal routing. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧
(mechanism) An ALB listener evaluates routing rules and forwards matching requests to a target group. ⟦A.f1 A:tb4 A:tb5⟧
(mechanism) Configure supplied listener protocol/port, forwarding rule and registered target protocol/port; test the endpoint. ⟦A.f2 A:tb4 A:tb5⟧
(mechanism) Match health-check path, port and success codes to the backend. Inspect target health reasons when a request path fails. ⟦A.f3 A:tb4 A:tb5⟧
(mechanism) ALB normally routes to healthy registered targets. If every registered target in a group is unhealthy, it fails open and routes to those unhealthy targets. ⟦A.f4 A:tb4 A:tb5⟧

### s03 · check · Judge listener and health-check evidence
Check your judgement — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] Every registered target in an ALB target group is unhealthy, yet requests reach those targets. Which interpretation matches the documented behavior?
  ✘ o1: ALB routing to any unhealthy target is impossible in this situation.
      why: Not supported. When all registered targets are unhealthy, an ALB fails open to them.
  ✔ o2: The ALB fails open to those unhealthy targets; this does not prove health.
      why: Correct. When all registered targets are unhealthy, an ALB fails open to them.
  ✘ o3: A response proves at least one registered target is healthy.
      why: Not supported. When all registered targets are unhealthy, an ALB fails open to them.
  feedback✔: When all registered targets are unhealthy, an ALB fails open to them.  feedback✘: When all registered targets are unhealthy, an ALB fails open to them.  hints: ['Separate the observation already recorded from the additional evidence the conclusion needs.']  remediation→r01
  MEASURES: A:distinguish_normal_healthy_target_routing_from_all_unhealthy_fail_open(f4)   anchors=['assessment:distinguish_normal_healthy_target_routing_from_all_unhealthy_fail_open']
  taught-before-tested: A.f4←s01

### s04 · hands_on · Review listener and health-check evidence
Evidence review — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each independent supplied evidence excerpt and its reviewer decision. Decide whether that decision is supported by the evidence and the verification requirements, or unsupported. A supported decision may correctly identify a failure; it does not always mean the operation succeeded.
  '```text
Supplied requirement: listener and forwarding rule to intended delivery-api target group; registered target protocol/port and backend health-check path/port/success codes.
Saved settings: all match the supplied requirement.
Endpoint test: intended backend response confirmed. Target health inspection: healthy; no failure reasons.
Reviewer decision: Accept routing and health settings; request and health evidence both support the result.
```' -> Supported decision
      feedback: Settings, endpoint result and health inspection agree; a response alone is not enough.
  '```text
Supplied requirement: listener and forwarding rule to intended delivery-api target group; registered target protocol/port and backend health-check path/port/success codes.
Saved settings: listener protocol/port, forwarding rule, registered target protocol/port, and health-check port/success codes match the supplied requirement; the saved health-check path differs from the supplied backend path.
Endpoint test: intended backend response confirmed. Target health inspection: every registered target unhealthy; reason: health-check path does not match backend.
Reviewer decision: A response proves healthy targets, so ignore the health-check mismatch.
```' -> Unsupported decision
      feedback: All-unhealthy fail-open can produce responses; health-check settings and reasons still matter.
  '```text
Supplied requirement: listener and forwarding rule to intended delivery-api target group; registered target protocol/port and backend health-check path/port/success codes.
Saved settings: forwarding rule selects a different target group.
Endpoint test: intended backend response confirmed. Target health inspection: healthy; no failure reasons.
Reviewer decision: Accept because the listener port matches.
```' -> Unsupported decision
      feedback: The forwarding rule must select the intended target group; port agreement alone is insufficient.
  feedback✔: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  feedback✘: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  hints: ['Distinguish saved configuration from observed execution evidence.', 'Check whether the reviewer preserves failures and respects the supplied scope.']  remediation→r02
  MEASURES: A:diagnose_listener_rule_and_target_configuration_mismatches(f1,f2); A:diagnose_health_check_mismatches_using_target_health_reasons(f3)   anchors=['practice', 'assessment:diagnose_listener_rule_and_target_configuration_mismatches', 'assessment:diagnose_health_check_mismatches_using_target_health_reasons']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s05 · recap · Keep these checks separate
Takeaways — 
(takeaway) Check listener routing and backend health settings; remember the all-unhealthy fail-open exception. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Configure log retention: CloudWatch log-group retention controls how long events remain. By default, logs are retained indefinitely.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Unhealthy does not always mean no routed traffic.
(mechanism) ALB normally routes to healthy registered targets. If every registered target in a group is unhealthy, it fails open and routes to those unhealthy targets. ⟦A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) If the supplied health-check path differs from the backend requirement, inspect health reasons and make the approved correction rather than changing unrelated settings. An unhealthy label is not an unconditional no-traffic guarantee: keep the all-unhealthy fail-open exception beside normal routing. ⟦A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Unhealthy does not always mean no routed traffic.
(mechanism) An ALB listener evaluates routing rules and forwards matching requests to a target group. ⟦A.f1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Configure supplied listener protocol/port, forwarding rule and registered target protocol/port; test the endpoint. ⟦A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Match health-check path, port and success codes to the backend. Inspect target health reasons when a request path fails. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) If the supplied health-check path differs from the backend requirement, inspect health reasons and make the approved correction rather than changing unrelated settings. An unhealthy label is not an unconditional no-traffic guarantee: keep the all-unhealthy fail-open exception beside normal routing. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Configure log retention (aws_devops.tile.059)
Tile summary: Inspect retentionInDays; distinguish expiry from physical deletion, which typically takes up to 72 hours.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.configure_log_retention — Configure log retention

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.configure_log_retention)   objective: Configure CloudWatch log retention
A.f1: CloudWatch log-group retention controls how long events remain; by default logs are retained indefinitely.   [sources: aws_cloudwatch_user_guide#../logs/Working-with-log-groups-and-streams.html]
A.f2: Set the supplied retention interval with put-retention-policy and inspect the log group’s retentionInDays.   [sources: aws_cloudwatch_user_guide#../logs/Working-with-log-groups-and-streams.html]
A.f3: Expired events are marked for deletion; physical deletion typically takes up to 72 hours, so expiry is not necessarily immediate disappearance.   [sources: aws_cloudwatch_user_guide#../logs/Working-with-log-groups-and-streams.html]
note: Preserve typically; do not promise a hard deletion deadline beyond the brief.
PRACTICE ANCHOR (tool_simulation): Apply the supplied retention interval to the intended log group using put-retention-policy, then inspect its retentionInDays.  SUCCESS: The intended log group's retentionInDays matches the supplied requirement. The learner interprets expired events as marked for deletion, with physical deletion typically taking up to 72 hours rather than necessarily occurring immediately.
ASSESSMENT ANCHOR: verify_log_group_retention_against_requirement facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_event_expiry_from_physical_deletion facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply an approved security baseline to sandbox accounts; Apply bounded EKS workload configuration and secrets after external configuration/secrets preparation; Audit KMS-backed audit-storage encryption (SSE-KMS): verify encryption and KMS key-use authority; key-use authority is required for SSE-KMS, not SSE-S3; Audit storage access; Configure CodePipeline source-to-deploy actions; directly require native IAM identity-policy evaluation and role trust for the service execution role, not pipeline federation; Configure managed database backups and create/restore RDS snapshots; require only native RDS and backup foundations, with existing network setup given and no routing or security-group skills assumed; Configure scoped log access; Credential expiry; Define an ECS task for a supplied image; Destroy review; Diagnose an IAM denied request from request and policy evidence; Dry run; Ecs task identity; Execute a reviewed Terraform plan provisioning EC2; directly require the native EC2 instance foundation; Execute a scoped Systems Manager remote command after external shell preparation; Gate infrastructure changes with configuration validation after external declarative/configuration prepa

## LESSON, in learner order

### s01 · explainer · Configure log retention
Understand the evidence — 
(definition) CloudWatch log-group retention controls how long events remain. By default, logs are retained indefinitely. ⟦A.f1 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Set the supplied interval with put-retention-policy; inspect the intended log group’s retentionInDays. ⟦A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Expired events are marked for deletion. Physical deletion typically takes up to 72 hours, so expiry need not mean immediate disappearance. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) An expired event may remain visible immediately after expiry. Compare retentionInDays with the supplied requirement before interpreting that visibility; deletion delay is not proof that retention is absent. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[DIAGRAM: Illustrative supplied retention evidence] nodes=['Intended log group: /delivery-api/sandbox', 'Supplied requirement: 30 days', 'Inspected retentionInDays: 30', 'Requirement and inspected setting agree'] edges=[] alt: Illustrative supplied retention evidence: Intended log group: /delivery-api/sandbox; Supplied requirement: 30 days; Inspected retentionInDays: 30; Requirement and inspected setting agree

### s02 · check · Judge log-retention evidence
Check your judgement — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] After the supplied retention policy is applied, an expired event remains physically visible. Which interpretation is valid?
  ✔ o1: Expiry marks events for deletion; physical deletion is not necessarily immediate.
      why: Correct. Expired events are marked for deletion; physical deletion typically takes up to 72 hours.
  ✘ o2: Visible expired events prove the retention setting was not saved.
      why: Not supported. Expired events are marked for deletion; physical deletion typically takes up to 72 hours.
  ✘ o3: Retention requires every expired event to disappear immediately.
      why: Not supported. Expired events are marked for deletion; physical deletion typically takes up to 72 hours.
  feedback✔: Expired events are marked for deletion; physical deletion typically takes up to 72 hours.  feedback✘: Expired events are marked for deletion; physical deletion typically takes up to 72 hours.  hints: ['Separate the observation already recorded from the additional evidence the conclusion needs.']  remediation→r01
  MEASURES: A:distinguish_event_expiry_from_physical_deletion(f3)   anchors=['assessment:distinguish_event_expiry_from_physical_deletion']
  taught-before-tested: A.f3←s01

### s03 · hands_on · Review log-retention evidence
Evidence review — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each independent supplied evidence excerpt and its reviewer decision. Decide whether that decision is supported by the evidence and the verification requirements, or unsupported. A supported decision may correctly identify a failure; it does not always mean the operation succeeded.
  '```text
Intended log group: /delivery-api/sandbox; supplied interval: 30 days.
put-retention-policy: applied 30 days to /delivery-api/sandbox.
Inspection: that log group retentionInDays=30.
Expired events: marked for deletion; physical deletion pending.
Reviewer decision: Accept the saved interval; pending physical deletion is not immediate-policy failure.
```' -> Supported decision
      feedback: The intended setting matches and expiry is distinguished from physical deletion.
  '```text
Intended log group: /delivery-api/sandbox; supplied interval: 30 days.
put-retention-policy: applied 30 days to /delivery-api/sandbox.
Inspection: that log group retentionInDays=30.
Expired events: marked for deletion; physical deletion pending.
Reviewer decision: The visible expired events prove that retentionInDays must be wrong.
```' -> Unsupported decision
      feedback: Physical deletion typically takes up to 72 hours rather than necessarily occurring at expiry.
  '```text
Intended log group: /delivery-api/sandbox; supplied interval: 30 days.
put-retention-policy: applied 30 days to /delivery-api/sandbox.
Inspection: that log group has no retention policy (default indefinite).
Expired events: marked for deletion; physical deletion pending.
Reviewer decision: Approve the supplied 30-day requirement.
```' -> Unsupported decision
      feedback: Indefinite default retention does not match the supplied bounded interval.
  feedback✔: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  feedback✘: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  hints: ['Distinguish saved configuration from observed execution evidence.', 'Check whether the reviewer preserves failures and respects the supplied scope.']  remediation→r02
  MEASURES: A:verify_log_group_retention_against_requirement(f1,f2); A:distinguish_event_expiry_from_physical_deletion(f3)   anchors=['practice', 'assessment:verify_log_group_retention_against_requirement', 'assessment:distinguish_event_expiry_from_physical_deletion']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s04 · recap · Keep these checks separate
Takeaways — 
(takeaway) Inspect retentionInDays; distinguish expiry from physical deletion, which typically takes up to 72 hours. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Configure managed database backups and create/restore RDS snapshots; require only native RDS and backup foundations, with existing network setup given and no routing or security-group skills assumed: An RDS DB snapshot captures a database instance for later restoration.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Expiry is not necessarily immediate deletion.
(mechanism) Expired events are marked for deletion. Physical deletion typically takes up to 72 hours, so expiry need not mean immediate disappearance. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) An expired event may remain visible immediately after expiry. Compare retentionInDays with the supplied requirement before interpreting that visibility; deletion delay is not proof that retention is absent. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Expiry is not necessarily immediate deletion.
(mechanism) CloudWatch log-group retention controls how long events remain. By default, logs are retained indefinitely. ⟦A.f1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Set the supplied interval with put-retention-policy; inspect the intended log group’s retentionInDays. ⟦A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Expired events are marked for deletion. Physical deletion typically takes up to 72 hours, so expiry need not mean immediate disappearance. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) An expired event may remain visible immediately after expiry. Compare retentionInDays with the supplied requirement before interpreting that visibility; deletion delay is not proof that retention is absent. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Configure managed database backups and create/restore RDS snapshots; require only native RDS and backup foundations, with existing network setup given and no routing or security-group skills assumed (aws_devops.tile.060)
Tile summary: Restore to a separate instance and verify its recovery marker at its own endpoint.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.configure_managed_database_backups — Configure managed database backups and create/restore RDS snapshots; require only native RDS and backup foundations, with existing network setup given and no routing or security-group skills assumed

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.configure_managed_database_backups)   objective: Create and restore an RDS snapshot
A.f1: An RDS DB snapshot captures the database instance for later restoration.   [sources: aws_rds_user_guide#USER_CreateSnapshot.html]
A.f2: Create a manual snapshot for the intended DB instance and wait until its snapshot status is available.   [sources: aws_rds_user_guide#USER_CreateSnapshot.html]
A.f3: Restore the snapshot to a new DB instance identifier using the supplied network settings; restoration creates a separate instance rather than overwriting the source.   [sources: aws_rds_user_guide#USER_RestoreFromSnapshot.html]
A.f4: Wait for the restored instance to become available, connect to its endpoint and run the supplied query to verify the recovery marker.   [sources: aws_rds_user_guide#CHAP_CommonTasks.Connect.html]
note: Use supplied network settings and query; do not author new SQL or database backup policy.
PRACTICE ANCHOR (tool_simulation): Create one manual RDS snapshot of the supplied DB instance, wait until the snapshot is available, and restore it to a new DB instance identifier using the supplied network settings. Once the restored instance is available, connect to its endpoint and run the supplied recovery-marker query.  SUCCESS: The snapshot is available, the restored DB instance has a distinct identifier and is available, and the supplied query executed against the restored endpoint returns the expected recovery marker. The source instance remains separate and unchanged.
ASSESSMENT ANCHOR: verify_recovery_marker_on_restored_database facts=['f3', 'f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply an approved security baseline to sandbox accounts; Apply bounded EKS workload configuration and secrets after external configuration/secrets preparation; Audit KMS-backed audit-storage encryption (SSE-KMS): verify encryption and KMS key-use authority; key-use authority is required for SSE-KMS, not SSE-S3; Audit storage access; Configure CodePipeline source-to-deploy actions; directly require native IAM identity-policy evaluation and role trust for the service execution role, not pipeline federation; Configure scoped log access; Credential expiry; Define an ECS task for a supplied image; Deploy a supplied CloudFormation S3 environment across accounts and Regions with assumed roles; directly require the native S3 object-storage concept; Destroy review; Diagnose an IAM denied request from request and policy evidence; Dry run; Ecs task identity; Execute a reviewed Terraform plan provisioning EC2; directly require the native EC2 instance foundation; Execute a scoped Systems Manager remote command after external shell preparation; Gate infrastructure changes with configuration validation after external declarative/configuration preparation; Handle AWS automation errors with bounded

## LESSON, in learner order

### s01 · explainer · Create and verify a separate RDS snapshot restore
Understand the evidence — 
(definition) An RDS DB snapshot captures a database instance for later restoration. ⟦A.f1 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Create a manual snapshot of the intended instance and wait for snapshot status available. ⟦A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Restore to a new DB instance identifier with supplied network settings. This creates a separate instance, not an overwrite of the source. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Wait for the restored instance to become available. Connect to its endpoint and run the supplied query to verify the recovery marker. ⟦A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Keep source, snapshot and restored identifiers together. An available snapshot is not restored-data verification. A query against the source endpoint cannot verify the recovery marker on the separate restored instance. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[DIAGRAM: Illustrative supplied restore evidence] nodes=['Source DB: delivery-source', 'Manual snapshot: delivery-snapshot; source: delivery-source; status: available', 'Restored DB: delivery-restored; status: available; supplied network settings used', 'Restored endpoint: delivery-restored.example.invalid', 'Supplied query against restored endpoint returned recovery_marker = marker-A; expected marker = marker-A'] edges=[] alt: Illustrative supplied restore evidence: Source DB: delivery-source; Manual snapshot: delivery-snapshot; source: delivery-source; status: available; Restored DB: delivery-restored; status: available; supplied network settings used; Restored endpoint: delivery-restored.example.invalid; Supplied query against restored endpoint returned recovery_marker = marker-A; expected marker = marker-A

### s02 · check · Judge snapshot and restore evidence
Check your judgement — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] A snapshot and its new restored DB instance are available. No recovery query has been run. Which verification is still needed?
  ✘ o1: Query only the source endpoint, since restoration overwrites the source.
      why: Not supported. Restoration creates a separate instance; verify the marker against its endpoint.
  ✘ o2: Treat available status as proof that the expected recovery marker was returned.
      why: Not supported. Restoration creates a separate instance; verify the marker against its endpoint.
  ✔ o3: Query the restored endpoint and compare the recovery marker with the expected marker.
      why: Correct. Restoration creates a separate instance; verify the marker against its endpoint.
  feedback✔: Restoration creates a separate instance; verify the marker against its endpoint.  feedback✘: Restoration creates a separate instance; verify the marker against its endpoint.  hints: ['Separate the observation already recorded from the additional evidence the conclusion needs.']  remediation→r01
  MEASURES: A:verify_recovery_marker_on_restored_database(f3,f4)   anchors=['assessment:verify_recovery_marker_on_restored_database']
  taught-before-tested: A.f3←s01; A.f4←s01

### s03 · hands_on · Review snapshot and restore evidence
Evidence review — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each independent supplied evidence excerpt and its reviewer decision. Decide whether that decision is supported by the evidence and the verification requirements, or unsupported. A supported decision may correctly identify a failure; it does not always mean the operation succeeded.
  '```text
Source: delivery-source, unchanged.
Manual snapshot: delivery-snapshot, source delivery-source, available.
Restore: delivery-restored, distinct identifier, available, supplied network settings used.
Connection: delivery-restored.example.invalid.
Supplied recovery query: expected marker-A; observed marker-A.
Reviewer decision: Accept recovery verification on the separate restored instance.
```' -> Supported decision
      feedback: Snapshot and restored availability, separate identity, network settings and restored-endpoint marker all agree.
  '```text
Source: delivery-source, unchanged.
Manual snapshot: delivery-snapshot, source delivery-source, available.
Restore: delivery-restored, distinct identifier, available, supplied network settings used.
Connection: source endpoint only.
Supplied recovery query: expected marker-A; observed marker-A.
Reviewer decision: Accept marker verification for the restored instance.
```' -> Unsupported decision
      feedback: A source-endpoint query does not verify the restored endpoint.
  '```text
Source: delivery-source, unchanged.
Manual snapshot: delivery-snapshot, source delivery-source, available.
Restore: delivery-restored, distinct identifier, still creating, supplied network settings used.
Connection: delivery-restored.example.invalid.
Supplied recovery query: not run.
Reviewer decision: Available snapshot alone proves completed recovery.
```' -> Unsupported decision
      feedback: Wait for restored availability and verify the recovery marker on its endpoint.
  feedback✔: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  feedback✘: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  hints: ['Distinguish saved configuration from observed execution evidence.', 'Check whether the reviewer preserves failures and respects the supplied scope.']  remediation→r01
  MEASURES: A:verify_recovery_marker_on_restored_database(f3,f4)   anchors=['practice', 'assessment:verify_recovery_marker_on_restored_database']
  taught-before-tested: A.f3←s01; A.f4←s01

### s04 · recap · Keep these checks separate
Takeaways — 
(takeaway) Restore to a separate instance and verify its recovery marker at its own endpoint. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Configure scoped log access: CloudWatch Logs authorizes log-group and log-stream operations through IAM policies.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · A source-endpoint query is not restored-data verification.
(mechanism) Restore to a new DB instance identifier with supplied network settings. This creates a separate instance, not an overwrite of the source. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Wait for the restored instance to become available. Connect to its endpoint and run the supplied query to verify the recovery marker. ⟦A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Keep source, snapshot and restored identifiers together. An available snapshot is not restored-data verification. A query against the source endpoint cannot verify the recovery marker on the separate restored instance. ⟦A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Configure scoped log access (aws_devops.tile.061)
Tile summary: Grant required reader actions with supported scopes; test approved and unapproved identities.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.configure_scoped_log_access — Configure scoped log access

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.configure_scoped_log_access)   objective: Scope CloudWatch log access
A.f1: CloudWatch Logs uses IAM policies to authorize log-group and log-stream operations.   [sources: aws_cloudwatch_user_guide#../logs/iam-access-control-overview-cwl.html]
A.f2: Grant the approved reader the required read actions on the intended log-group resources and remove unnecessary broader grants; some operations require resource scope *.   [sources: aws_cloudwatch_user_guide#../logs/iam-identity-based-access-control-cwl.html]
A.f3: Test the approved and unapproved principals against the intended read operations because collecting logs does not itself grant reader access.   [sources: aws_cloudwatch_user_guide#../logs/iam-access-control-overview-cwl.html]
note: Use supplied read actions and supported scopes; do not invent action-to-resource support rules.
PRACTICE ANCHOR (tool_simulation): Restrict access to one supplied log group to the supplied operational reader role using the provided read actions and supported resource scopes. Remove unnecessary broader grants and test the intended read operations under approved and unapproved principals.  SUCCESS: The approved role can perform the supplied read operations on the intended resources, while the unapproved principal cannot. Unnecessary broader grants are removed, required resource scope * is retained only for supplied operations that require it, and each test result records the identity, action, and resource scope.
ASSESSMENT ANCHOR: distinguish_approved_log_readers_from_denied_principals facts=['f1', 'f2', 'f3']

## DATA ASSETS USED
ds.log_access_tests: Scoped log reader test evidence — columns: principal(identifier), approved_reader(categorical), read_operation(text), resource_scope(text), scope_reason(text), expected_result(categorical), observed_result(categorical)
   ["delivery-log-reader",true,"supplied resource-scoped read operation","supplied delivery log-group resource","Supplied operation supports resource scoping","allowed","allowed"]
   ["delivery-log-reader",true,"supplied wildcard-required read operation","*","Supplied operation requires resource scope *","allowed","allowed"]
   ["unapproved-reader",false,"supplied resource-scoped read operation","supplied delivery log-group resource","Supplied operation supports resource scoping","denied","denied"]
   ["unapproved-reader",false,"supplied wildcard-required read operation","*","Supplied operation requires resource scope *","denied","denied"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply an approved security baseline to sandbox accounts; Apply bounded EKS workload configuration and secrets after external configuration/secrets preparation; Audit KMS-backed audit-storage encryption (SSE-KMS): verify encryption and KMS key-use authority; key-use authority is required for SSE-KMS, not SSE-S3; Audit storage access; Configure CodePipeline source-to-deploy actions; directly require native IAM identity-policy evaluation and role trust for the service execution role, not pipeline federation; Credential expiry; Define an ECS task for a supplied image; Deploy a supplied CloudFormation S3 environment across accounts and Regions with assumed roles; directly require the native S3 object-storage concept; Destroy review; Diagnose AWS connectivity failures using prepared DNS, HTTP, ports and CIDR foundations; Diagnose an IAM denied request from request and policy evidence; Dry run; Ecs task identity; Execute a reviewed Terraform plan provisioning EC2; directly require the native EC2 instance foundation; Execute a scoped Systems Manager remote command after external shell preparation; Gate infrastructure changes with configuration validation after external declarative/configur

## LESSON, in learner order

### s01 · explainer · Configure scoped log access
Understand the evidence — 
(definition) CloudWatch Logs authorizes log-group and log-stream operations through IAM policies. ⟦A.f1 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Grant the approved reader required read actions on intended log-group resources; remove unnecessary broader grants. Some operations require resource scope *. ⟦A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Test intended read operations under approved and unapproved principals. Collecting logs does not itself grant reader access. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Test the supplied reader and unapproved principal for each intended operation. Keep identity, action and resource scope with results. Do not force resource scope narrower than the supplied operation supports. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[SIDE_BY_SIDE] Collecting logs does not itself authorize a reader. left_label: Required actions and supported scopes | right_label: Access boundary tests
  left:
[TABLE ds.log_access_tests cols=['principal', 'read_operation', 'resource_scope', 'scope_reason'] ] caption: 
  right:
[TABLE ds.log_access_tests cols=['principal', 'approved_reader', 'read_operation', 'expected_result', 'observed_result'] ] caption: 

### s02 · check · Judge log-reader access evidence
Check your judgement — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] Logs are being collected. Does that alone show an approved role can perform the intended reads while an unapproved principal cannot?
  ✘ o1: Yes; reader identity and resource scope do not affect log read authorization.
      why: Not supported. Collection does not grant reader access; IAM authorization and identity-specific tests are required.
  ✔ o2: No; test both identities against the intended read operations and resource scopes.
      why: Correct. Collection does not grant reader access; IAM authorization and identity-specific tests are required.
  ✘ o3: Yes; collecting logs automatically grants reader access.
      why: Not supported. Collection does not grant reader access; IAM authorization and identity-specific tests are required.
  feedback✔: Collection does not grant reader access; IAM authorization and identity-specific tests are required.  feedback✘: Collection does not grant reader access; IAM authorization and identity-specific tests are required.  hints: ['Separate the observation already recorded from the additional evidence the conclusion needs.']  remediation→r01
  MEASURES: A:distinguish_approved_log_readers_from_denied_principals(f1,f2,f3)   anchors=['assessment:distinguish_approved_log_readers_from_denied_principals']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s03 · hands_on · Review log-reader access evidence
Evidence review — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each independent supplied evidence excerpt and its reviewer decision. Decide whether that decision is supported by the evidence and the verification requirements, or unsupported. A supported decision may correctly identify a failure; it does not always mean the operation succeeded.
  '| Field | Observation 1 | Observation 2 | Observation 3 | Observation 4 |
| --- | --- | --- | --- | --- |
| principal | delivery-log-reader | delivery-log-reader | unapproved-reader | unapproved-reader |
| approved_reader | true | true | false | false |
| read_operation | supplied resource-scoped read operation | supplied wildcard-required read operation | supplied resource-scoped read operation | supplied wildcard-required read operation |
| resource_scope | supplied delivery log-group resource | * | supplied delivery log-group resource | * |
| scope_reason | Supplied operation supports resource scoping | Supplied operation requires resource scope * | Supplied operation supports resource scoping | Supplied operation requires resource scope * |
| expected_result | allowed | allowed | denied | denied |
| observed_result | allowed | allowed | denied | denied |

Policy review: unnecessary broader grants removed; wildcard retained only for supplied operations that require it.

Reviewer decision: Accept approved-reader reads and unapproved denials with identity, operation and scope recorded.' -> Supported decision
      feedback: The complete test set distinguishes required wildcard scope from unnecessary broad grants.
  '| Field | Observation 1 | Observation 2 | Observation 3 | Observation 4 |
| --- | --- | --- | --- | --- |
| principal | delivery-log-reader | delivery-log-reader | unapproved-reader | unapproved-reader |
| approved_reader | true | true | false | false |
| read_operation | supplied resource-scoped read operation | supplied wildcard-required read operation | supplied resource-scoped read operation | supplied wildcard-required read operation |
| resource_scope | supplied delivery log-group resource | * | supplied delivery log-group resource | * |
| scope_reason | Supplied operation supports resource scoping | Supplied operation requires resource scope * | Supplied operation supports resource scoping | Supplied operation requires resource scope * |
| expected_result | allowed | allowed | denied | denied |
| observed_result | allowed | allowed | denied | denied |

Policy review: unnecessary broader grants removed; wildcard retained only for supplied operations that require it.

Reviewer decision: Remove every wildcard resource scope even for the supplied wildcard-required operation.' -> Unsupported decision
      feedback: Some operations require resource scope *; keep it only where required.
  '| Field | Observation 1 | Observation 2 | Observation 3 | Observation 4 |
| --- | --- | --- | --- | --- |
| principal | delivery-log-reader | delivery-log-reader | unapproved-reader | unapproved-reader |
| approved_reader | true | true | false | false |
| read_operation | supplied resource-scoped read operation | supplied wildcard-required read operation | supplied resource-scoped read operation | supplied wildcard-required read operation |
| resource_scope | supplied delivery log-group resource | * | supplied delivery log-group resource | * |
| scope_reason | Supplied operation supports resource scoping | Supplied operation requires resource scope * | Supplied operation supports resource scoping | Supplied operation requires resource scope * |
| expected_result | allowed | allowed | denied | denied |
| observed_result | allowed | allowed | denied | denied |

Proposed evidence replacement: logs collected successfully, read tests discarded.

Policy review: unnecessary broader grants removed; wildcard retained only for supplied operations that require it.

Reviewer decision: Collection alone proves approved access and unapproved denial.' -> Unsupported decision
      feedback: Collection does not establish reader authorization; keep principal-specific read tests.
  feedback✔: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  feedback✘: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  hints: ['Distinguish saved configuration from observed execution evidence.', 'Check whether the reviewer preserves failures and respects the supplied scope.']  remediation→r01
  MEASURES: A:distinguish_approved_log_readers_from_denied_principals(f1,f2,f3)   anchors=['practice', 'assessment:distinguish_approved_log_readers_from_denied_principals']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s04 · recap · Keep these checks separate
Takeaways — 
(takeaway) Grant required reader actions with supported scopes; test approved and unapproved identities. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Define an ECS task for a supplied image: An ECS task definition specifies the image and container runtime settings for tasks.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Log collection is not reader authorization.
(mechanism) CloudWatch Logs authorizes log-group and log-stream operations through IAM policies. ⟦A.f1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Grant the approved reader required read actions on intended log-group resources; remove unnecessary broader grants. Some operations require resource scope *. ⟦A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Test intended read operations under approved and unapproved principals. Collecting logs does not itself grant reader access. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Test the supplied reader and unapproved principal for each intended operation. Keep identity, action and resource scope with results. Do not force resource scope narrower than the supplied operation supports. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Define an ECS task for a supplied image (aws_devops.tile.062)
Tile summary: Compare registered task settings with task status and container details for the supplied launch type.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.define_an_ecs_task_for_a_supplied_image — Define an ECS task for a supplied image

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.define_an_ecs_task_for_a_supplied_image)   objective: Define an ECS task
A.f1: An ECS task definition specifies the image and container runtime settings for tasks.   [sources: aws_ecs_developer_guide#task_definitions.html]
A.f2: Set containerDefinitions entries with name, image, portMappings, cpu and memory settings appropriate to the supplied launch type, and register the task definition.   [sources: aws_ecs_developer_guide#task_definition_parameters.html]
A.f3: Run the registered task definition with the supplied cluster and network configuration, then inspect task status and container details to verify the image and runtime settings.   [sources: aws_ecs_developer_guide#standalone-task-create.html]
note: Use supplied launch-type settings; defer service desired-count and rollout operation.
PRACTICE ANCHOR (tool_simulation): Using the supplied image, launch-type settings, cluster and network configuration, configure and register one ECS task definition, then run one task from it.  SUCCESS: The registered task definition contains the supplied container name, image, port mappings, CPU and memory settings appropriate to the launch type. The task is run using the supplied cluster and network configuration, and its status and container details are inspected to compare the image and runtime settings with the supplied specification.
ASSESSMENT ANCHOR: verify_task_definition_image_ports_and_resources facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_running_task_image_and_runtime_settings facts=['f3']

## DATA ASSETS USED
ds.ecs_configuration_evidence: Supplied, registered and observed ECS settings — columns: evidence_stage(categorical), task_definition(identifier), task_id(identifier), status(categorical), name(identifier), image(identifier), containerPort(categorical,digits-as-label), hostPort(categorical,digits-as-label), cpu(numerical), memory(numerical), launch_type(categorical), cluster(identifier), network_configuration(text)
   ["supplied specification","delivery-task:1","not run","specified","delivery-api","delivery-api@sha256:803f4d7b1b5ef95b5a7467b65ec0f62c2f5c1a99fab92707d8910d1603750469",8080,8080,256,512,"EC2","delivery-cluster","supplied prepared network"]
   ["registered definition","delivery-task:1","not run","registered","delivery-api","delivery-api@sha256:803f4d7b1b5ef95b5a7467b65ec0f62c2f5c1a99fab92707d8910d1603750469",8080,8080,256,512,"EC2","delivery-cluster","supplied prepared network"]
   ["observed task","delivery-task:1","delivery-task-run-1","RUNNING","delivery-api","delivery-api@sha256:803f4d7b1b5ef95b5a7467b65ec0f62c2f5c1a99fab92707d8910d1603750469",8080,8080,256,512,"EC2","delivery-cluster","supplied prepared network"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply an approved security baseline to sandbox accounts; Apply bounded EKS workload configuration and secrets after external configuration/secrets preparation; Audit KMS-backed audit-storage encryption (SSE-KMS): verify encryption and KMS key-use authority; key-use authority is required for SSE-KMS, not SSE-S3; Audit storage access; Configure CodePipeline source-to-deploy actions; directly require native IAM identity-policy evaluation and role trust for the service execution role, not pipeline federation; Credential expiry; Deploy a supplied CloudFormation S3 environment across accounts and Regions with assumed roles; directly require the native S3 object-storage concept; Destroy review; Diagnose AWS connectivity failures using prepared DNS, HTTP, ports and CIDR foundations; Diagnose an IAM denied request from request and policy evidence; Dry run; Ecs task identity; Execute a reviewed Terraform plan provisioning EC2; directly require the native EC2 instance foundation; Execute a scoped Systems Manager remote command after external shell preparation; Execute an established fleet patch task after external package-management and shell preparation; Gate infrastructure changes with conf

## LESSON, in learner order

### s01 · explainer · Define an ECS task for a supplied image
Understand the evidence — 
(definition) An ECS task definition specifies the image and container runtime settings for tasks. ⟦A.f1 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Set containerDefinitions name, image, portMappings, cpu and memory appropriate to the supplied launch type; register the definition. ⟦A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Run that registered definition with the supplied cluster and network configuration. Inspect task status and container details to verify image and runtime settings. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Compare the registered specification with observed task details. Registration alone is not proof that the intended image and runtime settings were used. Do not generalize cpu or memory settings across launch types. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[SIDE_BY_SIDE] Match runtime details with the supplied specification and launch type. left_label: Registered specification | right_label: Observed task evidence
  left:
[TABLE ds.ecs_configuration_evidence cols=['evidence_stage', 'task_definition', 'name', 'image', 'containerPort', 'hostPort', 'cpu', 'memory', 'launch_type'] ] caption: 
  right:
[TABLE ds.ecs_configuration_evidence cols=['evidence_stage', 'task_definition', 'task_id', 'status', 'image', 'cpu', 'memory', 'launch_type', 'cluster', 'network_configuration'] ] caption: 

### s02 · check · Judge ECS task evidence
Check your judgement — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] An ECS task definition is registered with the supplied settings, but no task has been run or inspected. Which verification remains?
  ✔ o1: Run it with the supplied cluster/network and inspect task status and container details.
      why: Correct. The running task image and settings require task-status and container-detail evidence.
  ✘ o2: Registration alone proves a task is running the intended image.
      why: Not supported. The running task image and settings require task-status and container-detail evidence.
  ✘ o3: A task name alone proves its runtime settings match the specification.
      why: Not supported. The running task image and settings require task-status and container-detail evidence.
  feedback✔: The running task image and settings require task-status and container-detail evidence.  feedback✘: The running task image and settings require task-status and container-detail evidence.  hints: ['Separate the observation already recorded from the additional evidence the conclusion needs.']  remediation→r01
  MEASURES: A:verify_running_task_image_and_runtime_settings(f3)   anchors=['assessment:verify_running_task_image_and_runtime_settings']
  taught-before-tested: A.f3←s01

### s03 · hands_on · Review ECS task evidence
Evidence review — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each independent supplied evidence excerpt and its reviewer decision. Decide whether that decision is supported by the evidence and the verification requirements, or unsupported. A supported decision may correctly identify a failure; it does not always mean the operation succeeded.
  '| Field | Observation 1 | Observation 2 | Observation 3 |
| --- | --- | --- | --- |
| evidence_stage | supplied specification | registered definition | observed task |
| task_definition | delivery-task:1 | delivery-task:1 | delivery-task:1 |
| task_id | not run | not run | delivery-task-run-1 |
| status | specified | registered | RUNNING |
| name | delivery-api | delivery-api | delivery-api |
| image | delivery-api@sha256:803f4d7b1b5ef95b5a7467b65ec0f62c2f5c1a99fab92707d8910d1603750469 | delivery-api@sha256:803f4d7b1b5ef95b5a7467b65ec0f62c2f5c1a99fab92707d8910d1603750469 | delivery-api@sha256:803f4d7b1b5ef95b5a7467b65ec0f62c2f5c1a99fab92707d8910d1603750469 |
| containerPort | 8080 | 8080 | 8080 |
| hostPort | 8080 | 8080 | 8080 |
| cpu | 256 | 256 | 256 |
| memory | 512 | 512 | 512 |
| launch_type | EC2 | EC2 | EC2 |
| cluster | delivery-cluster | delivery-cluster | delivery-cluster |
| network_configuration | supplied prepared network | supplied prepared network | supplied prepared network |

Reviewer decision: Accept registered and running settings as matching the supplied specification and prepared cluster/network.' -> Supported decision
      feedback: The registered definition and observed task match the supplied image and runtime settings.
  '| Field | Observation 1 | Observation 2 |
| --- | --- | --- |
| evidence_stage | supplied specification | registered definition |
| task_definition | delivery-task:1 | delivery-task:1 |
| task_id | not run | not run |
| status | specified | registered |
| name | delivery-api | delivery-api |
| image | delivery-api@sha256:803f4d7b1b5ef95b5a7467b65ec0f62c2f5c1a99fab92707d8910d1603750469 | delivery-api@sha256:803f4d7b1b5ef95b5a7467b65ec0f62c2f5c1a99fab92707d8910d1603750469 |
| containerPort | 8080 | 8080 |
| hostPort | 8080 | 8080 |
| cpu | 256 | 256 |
| memory | 512 | 512 |
| launch_type | EC2 | EC2 |
| cluster | delivery-cluster | delivery-cluster |
| network_configuration | supplied prepared network | supplied prepared network |

Reviewer decision: Registration proves the supplied task is running; omit task status and container inspection.' -> Unsupported decision
      feedback: Registration alone does not verify running task status, image or runtime settings.
  '| Field | Observation 1 | Observation 2 | Observation 3 |
| --- | --- | --- | --- |
| evidence_stage | supplied specification | registered definition | observed task |
| task_definition | delivery-task:1 | delivery-task:1 | delivery-task:1 |
| task_id | not run | not run | delivery-task-run-1 |
| status | specified | registered | RUNNING |
| name | delivery-api | delivery-api | delivery-api |
| image | delivery-api@sha256:803f4d7b1b5ef95b5a7467b65ec0f62c2f5c1a99fab92707d8910d1603750469 | delivery-api@sha256:803f4d7b1b5ef95b5a7467b65ec0f62c2f5c1a99fab92707d8910d1603750469 | delivery-api@sha256:803f4d7b1b5ef95b5a7467b65ec0f62c2f5c1a99fab92707d8910d1603750469 |
| containerPort | 8080 | 8080 | 8080 |
| hostPort | 8080 | 8080 | 8080 |
| cpu | 256 | 256 | 256 |
| memory | 512 | 512 | 512 |
| launch_type | EC2 | EC2 | EC2 |
| cluster | delivery-cluster | delivery-cluster | delivery-cluster |
| network_configuration | supplied prepared network | supplied prepared network | supplied prepared network |

Alternate task observation: image differs from the supplied specification; all other settings match.

Reviewer decision: Accept because CPU and memory match.' -> Unsupported decision
      feedback: Matching resources do not excuse a different image in the observed task.
  feedback✔: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  feedback✘: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  hints: ['Distinguish saved configuration from observed execution evidence.', 'Check whether the reviewer preserves failures and respects the supplied scope.']  remediation→r02
  MEASURES: A:verify_task_definition_image_ports_and_resources(f1,f2); A:verify_running_task_image_and_runtime_settings(f3)   anchors=['practice', 'assessment:verify_task_definition_image_ports_and_resources', 'assessment:verify_running_task_image_and_runtime_settings']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s04 · recap · Keep these checks separate
Takeaways — 
(takeaway) Compare registered task settings with task status and container details for the supplied launch type. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Diagnose an IAM denied request from request and policy evidence: Diagnose access denial for the specific principal, operation, resource and request context.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Registration is not observed runtime verification.
(mechanism) Run that registered definition with the supplied cluster and network configuration. Inspect task status and container details to verify image and runtime settings. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Compare the registered specification with observed task details. Registration alone is not proof that the intended image and runtime settings were used. Do not generalize cpu or memory settings across launch types. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Registration is not observed runtime verification.
(mechanism) An ECS task definition specifies the image and container runtime settings for tasks. ⟦A.f1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Set containerDefinitions name, image, portMappings, cpu and memory appropriate to the supplied launch type; register the definition. ⟦A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Run that registered definition with the supplied cluster and network configuration. Inspect task status and container details to verify image and runtime settings. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Compare the registered specification with observed task details. Registration alone is not proof that the intended image and runtime settings were used. Do not generalize cpu or memory settings across launch types. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Diagnose an IAM denied request from request and policy evidence (aws_devops.tile.063)
Tile summary: Localize denial for the exact request; inspect applicable constraints and retest the smallest approved correction.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.diagnose_an_iam_denied_request_from_request_and_policy_evidence — Diagnose an IAM denied request from request and policy evidence

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.diagnose_an_iam_denied_request_from_request_and_policy_evidence)   objective: Diagnose an IAM denied request
A.f1: An access-denied diagnosis is specific to the requesting principal, operation, resource and request context.   [sources: aws_iam_user_guide#troubleshoot_access-denied.html]
A.f2: Inspect the request and applicable policies for an explicit deny, missing allow or unsatisfied condition and use available denial context to localize the cause.   [sources: aws_iam_user_guide#troubleshoot_access-denied.html]
A.f3: Resource policies, session policies, permissions boundaries and organization policies can constrain access beyond one identity policy; explicit deny takes precedence.   [sources: aws_iam_user_guide#reference_policies_evaluation-logic.html]
A.f4: Make the smallest approved policy or request correction supported by the evidence and retest the denied operation.   [sources: aws_iam_user_guide#troubleshoot_access-denied.html]
note: Do not prescribe broad administrator grants or invent missing policies; follow supplied evidence.
PRACTICE ANCHOR (tool_simulation): Resolve one denied sandbox request using supplied principal, operation, resource, request context, denial details and applicable policies. Identify the evidence-backed cause, apply the smallest approved policy or request correction, and retest the same operation.  SUCCESS: The learner identifies the decisive explicit deny, missing allow or unsatisfied condition, checks applicable constraints beyond the identity policy, and applies only the supplied approved correction. A retest of the denied operation succeeds, with before-and-after evidence tied to that request rather than a claim of unrestricted access.
ASSESSMENT ANCHOR: identify_missing_allow_for_the_specific_request facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_decisive_explicit_deny_across_applicable_policies facts=['f2', 'f3']
ASSESSMENT ANCHOR: identify_unsatisfied_policy_condition_from_request_context facts=['f1', 'f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply an approved security baseline to sandbox accounts; Apply bounded EKS workload configuration and secrets after external configuration/secrets preparation; Audit KMS-backed audit-storage encryption (SSE-KMS): verify encryption and KMS key-use authority; key-use authority is required for SSE-KMS, not SSE-S3; Audit storage access; Configure CodePipeline source-to-deploy actions; directly require native IAM identity-policy evaluation and role trust for the service execution role, not pipeline federation; Credential expiry; Deploy a supplied CloudFormation S3 environment across accounts and Regions with assumed roles; directly require the native S3 object-storage concept; Destroy review; Diagnose AWS connectivity failures using prepared DNS, HTTP, ports and CIDR foundations; Dry run; Ecs task identity; Execute a reviewed Terraform plan provisioning EC2; directly require the native EC2 instance foundation; Execute a scoped Systems Manager remote command after external shell preparation; Execute an established fleet patch task after external package-management and shell preparation; Expose an EKS workload using a Kubernetes Service; Gate infrastructure changes with configuration vali

## LESSON, in learner order

### s01 · explainer · Diagnose an IAM denied request from request and policy evidence
Understand the evidence — 
(definition) Diagnose access denial for the specific principal, operation, resource and request context. ⟦A.f1 A:tb1 A:tb2 A:tb3⟧
(mechanism) Inspect the request and applicable policies for explicit deny, missing allow or unsatisfied condition. Use available denial context to localize the cause. ⟦A.f2 A:tb1 A:tb2 A:tb3⟧
(mechanism) Resource policies, session policies, permissions boundaries and organization policies can constrain access beyond one identity policy. Explicit deny takes precedence. ⟦A.f3 A:tb1 A:tb2 A:tb3⟧
(mechanism) Make the smallest approved policy or request correction supported by evidence, then retest the denied operation. ⟦A.f4 A:tb1 A:tb2 A:tb3⟧
[DIAGRAM: Illustrative supplied denial evidence] nodes=['Request: delivery-log-reader; supplied read operation; supplied resource; environment=production', 'Identity policy allows this operation/resource; applicable organization policy explicitly denies it when environment=production; supplied resource, session and boundary evidence adds no other restriction', 'Decisive evidence: applicable explicit deny', 'Approved correction: use the authorized sandbox request context', 'Retest: same principal, operation and resource; environment=sandbox; allowed'] edges=[] alt: Illustrative supplied denial evidence: Request: delivery-log-reader; supplied read operation; supplied resource; environment=production; Identity policy allows this operation/resource; applicable organization policy explicitly denies it when environment=production; supplied resource, session and boundary evidence adds no other restriction; Decisive evidence: applicable explicit deny; Approved correction: use the authorized sandbox request context; Retest: same principal, operation and resource; environment=sandbox; allowed

### s02 · explainer · An identity-policy Allow is not the whole access decision.
Understand the evidence — 
(example) Finding an Allow in one identity policy does not settle this request. Inspect the other applicable constraints and denial context. Choose a minimal approved correction supported by that evidence, then repeat the same operation—not a different request. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧
(mechanism) Diagnose access denial for the specific principal, operation, resource and request context. ⟦A.f1 A:tb4 A:tb5⟧
(mechanism) Inspect the request and applicable policies for explicit deny, missing allow or unsatisfied condition. Use available denial context to localize the cause. ⟦A.f2 A:tb4 A:tb5⟧
(mechanism) Resource policies, session policies, permissions boundaries and organization policies can constrain access beyond one identity policy. Explicit deny takes precedence. ⟦A.f3 A:tb4 A:tb5⟧
(mechanism) Make the smallest approved policy or request correction supported by evidence, then retest the denied operation. ⟦A.f4 A:tb4 A:tb5⟧

### s03 · video · Trace the supplied evidence
Evidence walkthrough — 
[VIDEO Locate the policy evidence behind a denial] bridge-before: Watch how selected operations produce different results for the same identity, and how Show Statement locates supporting evidence. The clip calls denial from a missing allow an “implicit denial.” | bridge-after: The clip demonstrates deny precedence and missing allows. The text additionally covers complete request context, unsatisfied conditions, constraints beyond identity policies, and the smallest approved correction followed by retesting the denied operation.
  - FNbHpOTwifQ 0-274s facts=['f2'] label: Locate an explicit deny or missing allow with the IAM Policy Simulator | summary: The IAM Policy Simulator tests selected operations against policies associated with an existing identity. In the demonstrated case, user Daniel has an S3 allow policy and a separate policy explicitly denying bucket creation. Simulating bucket creation returns a denial because the explicit deny overrides the allow. The Show Statement control identifies the statement responsible. Simulated object retrieval and deletion are allowed, and their results identify the supporting allow statement. Testing DynamoDB operations instead produces implicit denials because the identity has not been granted those permissions. These results distinguish an applicable explicit deny from a missing allow; they do not demonstrate a correction or a successful retest of the actual denied operation.

### s04 · check · Judge IAM denial evidence
Check your judgement — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] For this request, the only applicable allow requires environment=sandbox, but the request context is environment=production. All other applicable policies have been checked and impose no additional restriction. What explains the denial?
  ✘ o1: The operation name alone guarantees that the conditional allow applies.
      why: Not supported. A diagnosis is tied to principal, operation, resource and context; an unsatisfied condition prevents the conditional allow from applying.
  ✘ o2: Request context is irrelevant once a principal is named in an allow.
      why: Not supported. A diagnosis is tied to principal, operation, resource and context; an unsatisfied condition prevents the conditional allow from applying.
  ✔ o3: The allow condition is unsatisfied for this request context.
      why: Correct. A diagnosis is tied to principal, operation, resource and context; an unsatisfied condition prevents the conditional allow from applying.
  feedback✔: A diagnosis is tied to principal, operation, resource and context; an unsatisfied condition prevents the conditional allow from applying.  feedback✘: A diagnosis is tied to principal, operation, resource and context; an unsatisfied condition prevents the conditional allow from applying.  hints: ['Separate the observation already recorded from the additional evidence the conclusion needs.']  remediation→r01
  MEASURES: A:identify_unsatisfied_policy_condition_from_request_context(f1,f2)   anchors=['assessment:identify_unsatisfied_policy_condition_from_request_context']
  taught-before-tested: A.f1←s01; A.f2←s01

### s05 · hands_on · Review IAM denial evidence
Evidence review — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each independent supplied evidence excerpt and its reviewer decision. Decide whether that decision is supported by the evidence and the verification requirements, or unsupported. A supported decision may correctly identify a failure; it does not always mean the operation succeeded.
  '```text
Request: delivery-log-reader; supplied read operation; supplied resource; environment=production.
Identity allow applies. Organization policy explicitly denies this operation/resource when environment=production.
Resource/session/boundary evidence: no additional restriction.
Approved correction: authorized sandbox context. Retest: same principal/operation/resource, environment=sandbox, allowed.
Reviewer decision: Identify decisive organization deny; accept only the approved context correction and this request-specific retest.
```' -> Supported decision
      feedback: The explicit deny dominates the allow; the bounded correction and same-request retest support success, not unrestricted access.
  '```text
Request: delivery-log-reader; supplied read operation; supplied resource; environment=sandbox.
Applicable identity policy: no allow for this operation/resource. Resource policy: no applicable allow. Session, boundary and organization evidence: no additional restriction or explicit deny.
Approval: add only the supplied allow for this principal, operation and resource. Retest: same request allowed.
Reviewer decision: Diagnose missing applicable allow and accept the supplied narrow correction with retest.
```' -> Supported decision
      feedback: The evidence localizes missing allow for this specific request after other constraints are checked.
  '```text
Request: delivery-log-reader; supplied read operation; supplied resource; environment=production.
Only applicable allow requires environment=sandbox; condition not satisfied. All other applicable policies inspected: no additional restriction or deny.
Approval: use sandbox context. Retest: same principal/operation/resource with environment=sandbox allowed.
Reviewer decision: Diagnose unsatisfied condition and accept only the supplied request-context correction.
```' -> Supported decision
      feedback: The condition fails for production and is satisfied by the approved sandbox retest.
  '```text
Request: delivery-log-reader; supplied read operation; supplied resource; environment=production.
Identity allow applies. Organization policy explicitly denies this operation/resource when environment=production.
Resource/session/boundary evidence: no additional restriction.
Approved correction: authorized sandbox context. Retest: same principal/operation/resource, environment=sandbox, allowed.
Reviewer decision: Add a broader identity allow to override the organization deny; omit retest.
```' -> Unsupported decision
      feedback: An identity allow cannot override explicit deny, and a correction needs a request-specific retest.
  feedback✔: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  feedback✘: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  hints: ['Distinguish saved configuration from observed execution evidence.', 'Check whether the reviewer preserves failures and respects the supplied scope.']  remediation→r02
  MEASURES: A:identify_missing_allow_for_the_specific_request(f1,f2); A:identify_decisive_explicit_deny_across_applicable_policies(f2,f3); A:identify_unsatisfied_policy_condition_from_request_context(f1,f2)   anchors=['practice', 'assessment:identify_missing_allow_for_the_specific_request', 'assessment:identify_decisive_explicit_deny_across_applicable_policies', 'assessment:identify_unsatisfied_policy_condition_from_request_context']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f2←s01; A.f3←s01; A.f1←s01; A.f2←s01

### s06 · recap · Keep these checks separate
Takeaways — 
(takeaway) Localize denial for the exact request; inspect applicable constraints and retest the smallest approved correction. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Execute a reviewed Terraform plan provisioning EC2; directly require the native EC2 instance foundation: terraform apply PLAN_FILE executes saved changes without generating a new plan or prompting for approval.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · An identity-policy Allow is not the whole access decision.
(mechanism) Diagnose access denial for the specific principal, operation, resource and request context. ⟦A.f1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Inspect the request and applicable policies for explicit deny, missing allow or unsatisfied condition. Use available denial context to localize the cause. ⟦A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Finding an Allow in one identity policy does not settle this request. Inspect the other applicable constraints and denial context. Choose a minimal approved correction supported by that evidence, then repeat the same operation—not a different request. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · An identity-policy Allow is not the whole access decision.
(mechanism) Diagnose access denial for the specific principal, operation, resource and request context. ⟦A.f1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Inspect the request and applicable policies for explicit deny, missing allow or unsatisfied condition. Use available denial context to localize the cause. ⟦A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Resource policies, session policies, permissions boundaries and organization policies can constrain access beyond one identity policy. Explicit deny takes precedence. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Finding an Allow in one identity policy does not settle this request. Inspect the other applicable constraints and denial context. Choose a minimal approved correction supported by that evidence, then repeat the same operation—not a different request. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Execute a reviewed Terraform plan provisioning EC2; directly require the native EC2 instance foundation (aws_devops.tile.064)
Tile summary: Apply the approved saved file and compare the created instance with that plan.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.execute_a_reviewed_terraform_plan_provisioning_ec2 — Execute a reviewed Terraform plan provisioning EC2; directly require the native EC2 instance foundation

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.execute_a_reviewed_terraform_plan_provisioning_ec2)   objective: Execute a reviewed Terraform EC2 plan
A.f1: terraform apply PLAN_FILE executes the changes recorded in a saved plan without generating a new plan or prompting for approval.   [sources: terraform_language#../cli/commands/apply]
A.f2: Use the supplied approved saved plan file rather than an unplanned apply, and retain the apply outcome as execution evidence.   [sources: terraform_language#../cli/commands/apply]
A.f3: Inspect terraform show PLAN_FILE and the resulting resource or outputs to check that the created EC2 instance matches the approved plan.   [sources: terraform_language#../cli/commands/show]
note: Apply only the approved saved plan; do not add unplanned mutation commands.
PRACTICE ANCHOR (live_code): Inspect and apply one supplied, saved and already-approved Terraform plan in a prepared sandbox, retain the apply outcome, and verify that the created EC2 instance matches the reviewed plan. Approval criteria and authorization are supplied.  SUCCESS: The supplied approved plan was executed without generating a new plan. The apply outcome is retained, and the resulting instance's identity, AMI, instance type and placement are recorded and compared with the planned settings supported by the exercise.
ASSESSMENT ANCHOR: verify_saved_approved_plan_execution facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_created_ec2_instance_matches_reviewed_plan facts=['f3']

## DATA ASSETS USED
ds.reviewed_plan_comparison: Approved plan and resulting EC2 comparison — columns: evidence_stage(categorical), plan_file(identifier), approved(categorical), instance_id(identifier), AMI(identifier), instance_type(categorical), placement(categorical), execution_command(text), apply_outcome(text)
   ["reviewed plan","PLAN_FILE",true,"not yet created","ami-d35dd291e9c4bd0f3","t3.micro","sandbox-zone-a","terraform show PLAN_FILE","not executed"]
   ["resulting resource","PLAN_FILE",true,"i-434bf03a7ef181c2b","ami-d35dd291e9c4bd0f3","t3.micro","sandbox-zone-a","terraform apply PLAN_FILE","Apply complete: one resource added"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply an approved security baseline to sandbox accounts; Apply bounded EKS workload configuration and secrets after external configuration/secrets preparation; Audit KMS-backed audit-storage encryption (SSE-KMS): verify encryption and KMS key-use authority; key-use authority is required for SSE-KMS, not SSE-S3; Audit storage access; Configure CodePipeline source-to-deploy actions; directly require native IAM identity-policy evaluation and role trust for the service execution role, not pipeline federation; Credential expiry; Deploy a supplied CloudFormation S3 environment across accounts and Regions with assumed roles; directly require the native S3 object-storage concept; Destroy review; Diagnose AWS connectivity failures using prepared DNS, HTTP, ports and CIDR foundations; Dry run; Ecs task identity; Execute a scoped Systems Manager remote command after external shell preparation; Execute an established fleet patch task after external package-management and shell preparation; Expose an EKS workload using a Kubernetes Service; Gate infrastructure changes with configuration validation after external declarative/configuration preparation; Handle AWS automation errors with bounded re

## LESSON, in learner order

### s01 · explainer · Execute a reviewed Terraform plan provisioning EC2; directly require the native EC2 instance foundation
Understand the evidence — 
(definition) terraform apply PLAN_FILE executes saved changes without generating a new plan or prompting for approval. ⟦A.f1 A:tb1 A:tb2 A:tb3⟧
(mechanism) Use the supplied approved saved plan, not an unplanned apply. Retain the apply outcome as execution evidence. ⟦A.f2 A:tb1 A:tb2 A:tb3⟧
(mechanism) Inspect terraform show PLAN_FILE and resulting resources or outputs to check the created EC2 instance against the approved plan. ⟦A.f3 A:tb1 A:tb2 A:tb3⟧
[SIDE_BY_SIDE] Compare the created instance with the approved saved plan. left_label: Approved saved plan | right_label: Execution and resource evidence
  left:
[TABLE ds.reviewed_plan_comparison cols=['evidence_stage', 'plan_file', 'approved', 'AMI', 'instance_type', 'placement'] ] caption: 
  right:
[TABLE ds.reviewed_plan_comparison cols=['evidence_stage', 'plan_file', 'instance_id', 'AMI', 'instance_type', 'placement', 'execution_command', 'apply_outcome'] ] caption: 

### s02 · explainer · Saved-plan apply is execution, not a new approval decision.
Understand the evidence — 
(example) Compare planned AMI, instance type and placement with resulting resource evidence. Saved-plan execution has no new approval prompt: the file must already be approved. Completion and resource comparison are distinct checks. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧
(mechanism) terraform apply PLAN_FILE executes saved changes without generating a new plan or prompting for approval. ⟦A.f1 A:tb4 A:tb5⟧
(mechanism) Use the supplied approved saved plan, not an unplanned apply. Retain the apply outcome as execution evidence. ⟦A.f2 A:tb4 A:tb5⟧
(mechanism) Inspect terraform show PLAN_FILE and resulting resources or outputs to check the created EC2 instance against the approved plan. ⟦A.f3 A:tb4 A:tb5⟧

### s03 · check · Judge saved-plan execution evidence
Check your judgement — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] An approved saved plan has been applied. Which evidence verifies that the created EC2 instance matches the reviewed plan?
  ✘ o1: Using any saved plan file is enough; resulting resource inspection is unnecessary.
      why: Not supported. Inspect the reviewed plan and the resulting resource or outputs; retaining apply outcome alone is not a settings comparison.
  ✔ o2: Inspect terraform show PLAN_FILE and compare the resulting resource identity and supported settings with the plan.
      why: Correct. Inspect the reviewed plan and the resulting resource or outputs; retaining apply outcome alone is not a settings comparison.
  ✘ o3: An apply completion message alone proves every resulting setting matches.
      why: Not supported. Inspect the reviewed plan and the resulting resource or outputs; retaining apply outcome alone is not a settings comparison.
  feedback✔: Inspect the reviewed plan and the resulting resource or outputs; retaining apply outcome alone is not a settings comparison.  feedback✘: Inspect the reviewed plan and the resulting resource or outputs; retaining apply outcome alone is not a settings comparison.  hints: ['Separate the observation already recorded from the additional evidence the conclusion needs.']  remediation→r01
  MEASURES: A:verify_created_ec2_instance_matches_reviewed_plan(f3)   anchors=['assessment:verify_created_ec2_instance_matches_reviewed_plan']
  taught-before-tested: A.f3←s01

### s04 · hands_on · Review saved-plan execution evidence
Evidence review — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each independent supplied evidence excerpt and its reviewer decision. Decide whether that decision is supported by the evidence and the verification requirements, or unsupported. A supported decision may correctly identify a failure; it does not always mean the operation succeeded.
  '| Field | Observation 1 | Observation 2 |
| --- | --- | --- |
| evidence_stage | reviewed plan | resulting resource |
| plan_file | PLAN_FILE | PLAN_FILE |
| approved | true | true |
| instance_id | not yet created | i-434bf03a7ef181c2b |
| AMI | ami-d35dd291e9c4bd0f3 | ami-d35dd291e9c4bd0f3 |
| instance_type | t3.micro | t3.micro |
| placement | sandbox-zone-a | sandbox-zone-a |
| execution_command | terraform show PLAN_FILE | terraform apply PLAN_FILE |
| apply_outcome | not executed | Apply complete: one resource added |

Reviewer decision: Accept approved saved-plan execution and retained outcome with AMI, type and placement comparison.' -> Supported decision
      feedback: The command applies the approved file and the resource evidence matches the reviewed settings.
  '| Field | Observation 1 | Observation 2 |
| --- | --- | --- |
| evidence_stage | reviewed plan | resulting resource |
| plan_file | PLAN_FILE | PLAN_FILE |
| approved | true | true |
| instance_id | not yet created | i-434bf03a7ef181c2b |
| AMI | ami-d35dd291e9c4bd0f3 | ami-d35dd291e9c4bd0f3 |
| instance_type | t3.micro | t3.micro |
| placement | sandbox-zone-a | sandbox-zone-a |
| execution_command | terraform show PLAN_FILE | terraform apply PLAN_FILE |
| apply_outcome | not executed | Apply complete: one resource added |

Alternate execution command: terraform apply (no PLAN_FILE).

Reviewer decision: Treat this alternate execution as execution of the approved saved plan.' -> Unsupported decision
      feedback: An apply without the saved file is not execution of that approved recorded plan.
  '| Field | Observation 1 | Observation 2 |
| --- | --- | --- |
| evidence_stage | reviewed plan | resulting resource |
| plan_file | PLAN_FILE | PLAN_FILE |
| approved | true | true |
| instance_id | not yet created | i-434bf03a7ef181c2b |
| AMI | ami-d35dd291e9c4bd0f3 | ami-d35dd291e9c4bd0f3 |
| instance_type | t3.micro | t3.micro |
| placement | sandbox-zone-a | sandbox-zone-a |
| execution_command | terraform show PLAN_FILE | terraform apply PLAN_FILE |
| apply_outcome | not executed | Apply complete: one resource added |

Alternate observed instance: placement differs from reviewed placement.

Reviewer decision: Accept because the apply command used the approved file.' -> Unsupported decision
      feedback: Retaining apply outcome is not enough; resulting instance settings must match the reviewed plan.
  feedback✔: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  feedback✘: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  hints: ['Distinguish saved configuration from observed execution evidence.', 'Check whether the reviewer preserves failures and respects the supplied scope.']  remediation→r02
  MEASURES: A:verify_saved_approved_plan_execution(f1,f2); A:verify_created_ec2_instance_matches_reviewed_plan(f3)   anchors=['practice', 'assessment:verify_saved_approved_plan_execution', 'assessment:verify_created_ec2_instance_matches_reviewed_plan']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s05 · recap · Keep these checks separate
Takeaways — 
(takeaway) Apply the approved saved file and compare the created instance with that plan. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Execute a scoped Systems Manager remote command: Run Command executes Systems Manager documents on managed nodes under authorized access.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Saved-plan apply is execution, not a new approval decision.
(mechanism) Inspect terraform show PLAN_FILE and resulting resources or outputs to check the created EC2 instance against the approved plan. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Compare planned AMI, instance type and placement with resulting resource evidence. Saved-plan execution has no new approval prompt: the file must already be approved. Completion and resource comparison are distinct checks. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Saved-plan apply is execution, not a new approval decision.
(mechanism) terraform apply PLAN_FILE executes saved changes without generating a new plan or prompting for approval. ⟦A.f1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Use the supplied approved saved plan, not an unplanned apply. Retain the apply outcome as execution evidence. ⟦A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Inspect terraform show PLAN_FILE and resulting resources or outputs to check the created EC2 instance against the approved plan. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Compare planned AMI, instance type and placement with resulting resource evidence. Saved-plan execution has no new approval prompt: the file must already be approved. Completion and resource comparison are distinct checks. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Execute a scoped Systems Manager remote command (aws_devops.tile.065)
Tile summary: Keep approved targets and command ID with each invocation’s status and output.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.execute_a_scoped_systems_manager_remote_command — Execute a scoped Systems Manager remote command after external shell preparation

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.execute_a_scoped_systems_manager_remote_command)   objective: Execute a scoped Systems Manager command
A.f1: Run Command executes Systems Manager documents on managed nodes under authorized access.   [sources: aws_systems_manager_user_guide#run-command.html]
A.f2: Use send-command with the supplied document and explicit approved --instance-ids or tag-based --targets and document parameters.   [sources: aws_systems_manager_user_guide#walkthrough-cli.html]
A.f3: Record the command ID and inspect each invocation’s status and output; the parent command status does not replace per-node result checks.   [sources: aws_systems_manager_user_guide#monitor-commands.html]
note: Use supplied document and parameters; require shared Linux/shell preparation for dependent fleet tasks.
PRACTICE ANCHOR (tool_simulation): Run one supplied command in a prepared sandbox using send-command, the supplied document and parameters, and explicit approved instance IDs or supplied tag-based targets. Record the command ID and inspect every target invocation.  SUCCESS: The submitted document, parameters, and target scope match the supplied approval. The execution record contains the command ID, a comparison of invocation target IDs with the approved target set, and each target's status and output. Unintended, missing, failed, or unresolved invocations are identified rather than hidden by the parent command status.
ASSESSMENT ANCHOR: verify_authorized_document_and_approved_target_scope facts=['f1', 'f2']
ASSESSMENT ANCHOR: compare_invocation_targets_with_approved_targets facts=['f2', 'f3']
ASSESSMENT ANCHOR: record_command_id_and_per_node_status_and_output facts=['f3']

## DATA ASSETS USED
ds.command_invocations: Scoped command invocation evidence — columns: command_id(identifier), document_name(identifier), document_parameters(text), approved_target_set(text), invocation_target(identifier), approved_target(categorical), parent_status(categorical), invocation_status(categorical), invocation_output(text)
   ["cmd-93a0fc50c8bf5ea25","SuppliedInspectionDocument","Mode=inspect","i-434bf03a7ef181c2b, i-0ee5823af28beaf29, i-3acda2e1fbcd52071","i-434bf03a7ef181c2b",true,"Success","Success","Supplied inspection completed"]
   ["cmd-93a0fc50c8bf5ea25","SuppliedInspectionDocument","Mode=inspect","i-434bf03a7ef181c2b, i-0ee5823af28beaf29, i-3acda2e1fbcd52071","i-0ee5823af28beaf29",true,"Success","Success","Supplied inspection completed"]
   ["cmd-93a0fc50c8bf5ea25","SuppliedInspectionDocument","Mode=inspect","i-434bf03a7ef181c2b, i-0ee5823af28beaf29, i-3acda2e1fbcd52071","i-3acda2e1fbcd52071",true,"Success","Failed","Supplied inspection failed; retain node-specific output"]
   variant var.command_scope_discrepancy: 4 ops; planted: issue.unapproved_invocation(other)

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply an approved security baseline to sandbox accounts; Apply bounded EKS workload configuration and secrets after external configuration/secrets preparation; Audit KMS-backed audit-storage encryption (SSE-KMS): verify encryption and KMS key-use authority; key-use authority is required for SSE-KMS, not SSE-S3; Audit storage access; Configure CodePipeline source-to-deploy actions; directly require native IAM identity-policy evaluation and role trust for the service execution role, not pipeline federation; Credential expiry; Deploy a supplied CloudFormation S3 environment across accounts and Regions with assumed roles; directly require the native S3 object-storage concept; Destroy review; Diagnose AWS connectivity failures using prepared DNS, HTTP, ports and CIDR foundations; Dry run; Ecs task identity; Execute an established fleet patch task after external package-management and shell preparation; Expose an EKS workload using a Kubernetes Service; Gate infrastructure changes with configuration validation after external declarative/configuration preparation; Handle AWS automation errors with bounded retries and useful reporting; AWS SDK call is a supplied ready function, not an assu

## LESSON, in learner order

### s01 · explainer · Execute a scoped Systems Manager remote command
Understand the evidence — 
(definition) Run Command executes Systems Manager documents on managed nodes under authorized access. ⟦A.f1 A:tb1 A:tb2 A:tb3⟧
(mechanism) Use send-command with supplied document, parameters and explicit approved --instance-ids or tag-based --targets. ⟦A.f2 A:tb1 A:tb2 A:tb3⟧
(mechanism) Record the command ID. Inspect each invocation’s status and output; parent status does not replace per-node checks. ⟦A.f3 A:tb1 A:tb2 A:tb3⟧
[TABLE ds.command_invocations cols=['command_id', 'document_name', 'document_parameters', 'approved_target_set', 'invocation_target', 'approved_target', 'parent_status', 'invocation_status', 'invocation_output'] ] caption: 

### s02 · explainer · Parent status is not per-node evidence.
Understand the evidence — 
(example) Compare invocation targets with the approved target set before interpreting results. A successful unintended-node invocation is still a scope discrepancy. Preserve each node’s status and output under the shared command ID; missing or unresolved invocations are not success. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧
(mechanism) Run Command executes Systems Manager documents on managed nodes under authorized access. ⟦A.f1 A:tb4 A:tb5⟧
(mechanism) Use send-command with supplied document, parameters and explicit approved --instance-ids or tag-based --targets. ⟦A.f2 A:tb4 A:tb5⟧
(mechanism) Record the command ID. Inspect each invocation’s status and output; parent status does not replace per-node checks. ⟦A.f3 A:tb4 A:tb5⟧

### s03 · video · Trace the supplied evidence
Evidence walkthrough — 
[VIDEO Execute a document on explicitly selected managed nodes] bridge-before: Watch how the document, parameters, and two instance targets are selected. The clip disables S3 output storage as a demonstration choice; that choice does not remove the requirement to inspect each invocation's status and output. | bridge-after: The clip demonstrates document execution, but not authorized-access checks, approved CLI targeting with send-command, or command-ID recording and per-node result inspection. The text supplies these requirements; overall success and one node's effects are insufficient.
  - B2MecqC5nJA 1081-1252s facts=['f1'] label: Run a shell-script document on two selected EC2 instances | summary: Run Command uses the AWS-RunShellScript document with parameters that create a file and a Linux user. The presenter manually selects two EC2 instances, disables S3 output storage for the demonstration, and runs the document. After the console reports overall and detailed success, the presenter connects to one instance and checks that the file and user exist. This demonstrates document execution and its effects on one node, rather than checking every node's invocation status and output.

### s04 · check · Judge per-node command evidence
Check your judgement — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] A parent Run Command status is Success, but one approved node invocation is Failed. Which record is required?
  ✔ o1: Retain the command ID and each node status/output, including the failed invocation.
      why: Correct. Parent status does not replace per-node status and output checks.
  ✘ o2: Record only parent Success and mark every node successful.
      why: Not supported. Parent status does not replace per-node status and output checks.
  ✘ o3: Drop the failed node from the record because parent status is authoritative.
      why: Not supported. Parent status does not replace per-node status and output checks.
  feedback✔: Parent status does not replace per-node status and output checks.  feedback✘: Parent status does not replace per-node status and output checks.  hints: ['Separate the observation already recorded from the additional evidence the conclusion needs.']  remediation→r01
  MEASURES: A:record_command_id_and_per_node_status_and_output(f3)   anchors=['assessment:record_command_id_and_per_node_status_and_output']
  taught-before-tested: A.f3←s01

### s05 · hands_on · Review per-node command evidence
Evidence review — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each independent supplied evidence excerpt and its reviewer decision. Decide whether that decision is supported by the evidence and the verification requirements, or unsupported. A supported decision may correctly identify a failure; it does not always mean the operation succeeded.
  '| Field | Observation 1 | Observation 2 | Observation 3 |
| --- | --- | --- | --- |
| command_id | cmd-93a0fc50c8bf5ea25 | cmd-93a0fc50c8bf5ea25 | cmd-93a0fc50c8bf5ea25 |
| document_name | SuppliedInspectionDocument | SuppliedInspectionDocument | SuppliedInspectionDocument |
| document_parameters | Mode=inspect | Mode=inspect | Mode=inspect |
| approved_target_set | i-434bf03a7ef181c2b, i-0ee5823af28beaf29, i-3acda2e1fbcd52071 | i-434bf03a7ef181c2b, i-0ee5823af28beaf29, i-3acda2e1fbcd52071 | i-434bf03a7ef181c2b, i-0ee5823af28beaf29, i-3acda2e1fbcd52071 |
| invocation_target | i-434bf03a7ef181c2b | i-0ee5823af28beaf29 | i-3acda2e1fbcd52071 |
| approved_target | true | true | true |
| parent_status | Success | Success | Success |
| invocation_status | Success | Success | Failed |
| invocation_output | Supplied inspection completed | Supplied inspection completed | Supplied inspection failed; retain node-specific output |

Approval/submission: supplied document, parameters and approved target set match; authorization confirmed. All approved targets are represented; none extra.

Reviewer decision: Accept scope and complete evidence, but flag the failed invocation rather than declaring all nodes successful.' -> Supported decision
      feedback: The command ID, target comparison and each output are retained; parent Success does not erase a node failure.
  '| Field | Observation 1 | Observation 2 | Observation 3 |
| --- | --- | --- | --- |
| command_id | cmd-93a0fc50c8bf5ea25 | cmd-93a0fc50c8bf5ea25 | cmd-93a0fc50c8bf5ea25 |
| document_name | SuppliedInspectionDocument | SuppliedInspectionDocument | SuppliedInspectionDocument |
| document_parameters | Mode=inspect | Mode=inspect | Mode=inspect |
| approved_target_set | i-434bf03a7ef181c2b, i-0ee5823af28beaf29, i-3acda2e1fbcd52071 | i-434bf03a7ef181c2b, i-0ee5823af28beaf29, i-3acda2e1fbcd52071 | i-434bf03a7ef181c2b, i-0ee5823af28beaf29, i-3acda2e1fbcd52071 |
| invocation_target | i-434bf03a7ef181c2b | i-0ee5823af28beaf29 | i-3acda2e1fbcd52071 |
| approved_target | true | true | true |
| parent_status | Success | Success | Success |
| invocation_status | Success | Success | Failed |
| invocation_output | Supplied inspection completed | Supplied inspection completed | Supplied inspection failed; retain node-specific output |

Approval/submission: supplied document, parameters and approved target set match; authorization confirmed. All approved targets are represented; none extra.

Reviewer decision: Parent Success proves all approved targets succeeded; remove node-specific outputs.' -> Unsupported decision
      feedback: Each invocation status and output must be inspected and retained.
  '| Field | Observation 1 | Observation 2 | Observation 3 |
| --- | --- | --- | --- |
| command_id | cmd-93a0fc50c8bf5ea25 | cmd-93a0fc50c8bf5ea25 | cmd-93a0fc50c8bf5ea25 |
| document_name | SuppliedInspectionDocument | SuppliedInspectionDocument | SuppliedInspectionDocument |
| document_parameters | Mode=inspect | Mode=inspect | Mode=inspect |
| approved_target_set | i-434bf03a7ef181c2b, i-0ee5823af28beaf29, i-3acda2e1fbcd52071 | i-434bf03a7ef181c2b, i-0ee5823af28beaf29, i-3acda2e1fbcd52071 | i-434bf03a7ef181c2b, i-0ee5823af28beaf29, i-3acda2e1fbcd52071 |
| invocation_target | i-434bf03a7ef181c2b | i-0ee5823af28beaf29 | i-3acda2e1fbcd52071 |
| approved_target | true | true | true |
| parent_status | Success | Success | Success |
| invocation_status | Success | Success | Failed |
| invocation_output | Supplied inspection completed | Supplied inspection completed | Supplied inspection failed; retain node-specific output |

Alternate target submission: includes an extra unapproved node.

Approval/submission: supplied document, parameters and approved target set match; authorization confirmed. All approved targets are represented; none extra.

Reviewer decision: Accept target scope because all originally approved nodes are also included.' -> Unsupported decision
      feedback: Including approved nodes does not authorize extra targets; compare actual scope with approval.
  feedback✔: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  feedback✘: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  hints: ['Distinguish saved configuration from observed execution evidence.', 'Check whether the reviewer preserves failures and respects the supplied scope.']  remediation→r02
  MEASURES: A:verify_authorized_document_and_approved_target_scope(f1,f2); A:compare_invocation_targets_with_approved_targets(f2,f3); A:record_command_id_and_per_node_status_and_output(f3)   anchors=['practice', 'assessment:verify_authorized_document_and_approved_target_scope', 'assessment:compare_invocation_targets_with_approved_targets', 'assessment:record_command_id_and_per_node_status_and_output']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f2←s01; A.f3←s01; A.f3←s01

### s06 · recap · Keep these checks separate
Takeaways — 
(takeaway) Keep approved targets and command ID with each invocation’s status and output. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Gate infrastructure changes with configuration validation: terraform validate checks syntax and internal consistency, not remote service state or provider API success.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Parent status is not per-node evidence.
(mechanism) Record the command ID. Inspect each invocation’s status and output; parent status does not replace per-node checks. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Compare invocation targets with the approved target set before interpreting results. A successful unintended-node invocation is still a scope discrepancy. Preserve each node’s status and output under the shared command ID; missing or unresolved invocations are not success. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Parent status is not per-node evidence.
(mechanism) Run Command executes Systems Manager documents on managed nodes under authorized access. ⟦A.f1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Use send-command with supplied document, parameters and explicit approved --instance-ids or tag-based --targets. ⟦A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Record the command ID. Inspect each invocation’s status and output; parent status does not replace per-node checks. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Compare invocation targets with the approved target set before interpreting results. A successful unintended-node invocation is still a scope discrepancy. Preserve each node’s status and output under the shared command ID; missing or unresolved invocations are not success. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Gate infrastructure changes with configuration validation (aws_devops.tile.066)
Tile summary: Initialize dependencies, block on validation failure, and distinguish formatting, static validity and provisioning evidence.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.gate_infrastructure_changes_with_configuration_validation — Gate infrastructure changes with configuration validation after external declarative/configuration preparation

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.gate_infrastructure_changes_with_configuration_validation)   objective: Gate infrastructure changes with configuration validation
A.f1: terraform validate checks configuration syntax and internal consistency without checking remote service state or provider API success.   [sources: terraform_language#../cli/commands/validate]
A.f2: Initialize needed providers and modules with terraform init -backend=false before static validation where backend access is not needed.   [sources: terraform_language#../cli/commands/validate]
A.f3: Run terraform validate as a blocking workflow step; stop on its nonzero exit result, correct the invalid declaration and rerun before the supplied approved apply step.   [sources: terraform_language#../cli/commands/validate]
A.f4: terraform fmt -check checks canonical formatting and can be used as an additional blocking configuration check.   [sources: terraform_language#../cli/commands/fmt]
note: Use supplied workflow and corrections; do not imply validation guarantees successful apply.
PRACTICE ANCHOR (live_code): Add blocking Terraform configuration checks to the supplied EC2 provisioning workflow. Initialize dependencies without backend access for static validation, demonstrate that the supplied invalid declaration blocks execution, apply the supplied correction, rerun checks, and execute the supplied approved apply step to provision one EC2 instance.  SUCCESS: The invalid declaration produces a nonzero validation result and the apply step does not execute. After correction, validation and the additional formatting check pass, and the supplied approved apply step provisions one EC2 instance. Recorded evidence distinguishes static-check success from provisioning success.
ASSESSMENT ANCHOR: distinguish_static_validation_from_remote_service_verification facts=['f1']
ASSESSMENT ANCHOR: initialize_dependencies_for_static_validation facts=['f2']
ASSESSMENT ANCHOR: verify_validation_failure_blocks_infrastructure_execution facts=['f3']
ASSESSMENT ANCHOR: distinguish_formatting_failure_from_configuration_invalidity facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply an approved security baseline to sandbox accounts; Apply bounded EKS workload configuration and secrets after external configuration/secrets preparation; Audit KMS-backed audit-storage encryption (SSE-KMS): verify encryption and KMS key-use authority; key-use authority is required for SSE-KMS, not SSE-S3; Audit storage access; Configure CodePipeline source-to-deploy actions; directly require native IAM identity-policy evaluation and role trust for the service execution role, not pipeline federation; Credential expiry; Deploy a supplied CloudFormation S3 environment across accounts and Regions with assumed roles; directly require the native S3 object-storage concept; Destroy review; Diagnose AWS connectivity failures using prepared DNS, HTTP, ports and CIDR foundations; Dry run; Ecs task identity; Execute an established fleet patch task after external package-management and shell preparation; Expose an EKS workload using a Kubernetes Service; Handle AWS automation errors with bounded retries and useful reporting; AWS SDK call is a supplied ready function, not an assumed skill or prerequisite; Identify avoidable charges with Cost Explorer; Inject a controlled failure and verify

## LESSON, in learner order

### s01 · explainer · Gate infrastructure changes with configuration validation
Understand the evidence — 
(definition) terraform validate checks syntax and internal consistency, not remote service state or provider API success. ⟦A.f1 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Where backend access is unnecessary, initialize needed providers and modules with terraform init -backend=false before static validation. ⟦A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Make terraform validate blocking. Stop on nonzero exit, correct the invalid declaration and rerun before the supplied approved apply step. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) terraform fmt -check checks canonical formatting and can serve as an additional blocking configuration check. ⟦A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) For the supplied invalid EC2 declaration, validation failure must block apply. After correction, rerun validation and any blocking formatting check. A formatting-only change is not a configuration-validity correction, and static-check success is not provisioning evidence. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[CODE bash]
# Static checks where backend access is unnecessary
terraform init -backend=false &&
terraform validate &&
terraform fmt -check
# Only after blocking checks pass: supplied approved apply step
  annotations: ['Initialize needed providers and modules.', 'Nonzero validation blocks progression; correct the supplied declaration and rerun.', 'Additional blocking canonical-format check, not remote-state verification.', 'Static success and provisioning success are distinct evidence.']
[SIDE_BY_SIDE] A formatting-only change is separate from correcting an invalid declaration. left_label: Configuration defect | right_label: Correction and recheck
  left:
[CODE bash]
cat <<'HCL'
resource "aws_instance" "delivery" {
  ami           = "ami-d35dd291e9c4bd0f3"
  instance_typ = "t3.micro"
}
HCL
  annotations: ['Illustrative supplied case — invalid EC2 declaration (HCL)', 'Invalid argument: instance_typ; correction is instance_type.', 'Before: validate exit 1; apply blocked']
  right:
[CODE bash]
cat <<'HCL'
resource "aws_instance" "delivery" {
  ami           = "ami-d35dd291e9c4bd0f3"
  instance_type = "t3.micro"
}
HCL
  annotations: ['Illustrative supplied case — corrected EC2 declaration (HCL)', 'Corrected argument: instance_type.', 'After: validate exit 0; fmt -check exit 0; supplied approved apply executed; apply outcome retained separately']
[CODE bash]
cat <<'HCL'
resource "aws_instance" "delivery" {
 ami = "ami-d35dd291e9c4bd0f3"
   instance_type="t3.micro"
}
HCL
  annotations: ['Illustrative supplied case — HCL spacing contrast', 'Formatting-only change: declaration meaning unchanged; not the invalid-argument correction']

### s02 · video · Trace the supplied evidence
Evidence walkthrough — 
[VIDEO Separate formatting checks from configuration validation] bridge-before: Watch how incorrect indentation triggers a formatting check even though the declaration remains syntactically correct. The captions render fmt as “format”; use the command terraform fmt -check. | bridge-after: The clip establishes the formatting check, not validation scope, initialization prerequisites, or nonzero-result blocking. The text teaches those requirements, including correcting and revalidating before the supplied approved apply step.
  - 7xngnjfIlK4 7505-7596s facts=['f4'] label: Check canonical formatting with terraform fmt -check | summary: Terraform has a built-in canonical formatting style. The demonstration changes indentation while leaving the declaration syntactically correct, then runs terraform fmt -check, which identifies instance.tf as needing formatting. Running terraform fmt repairs the formatting. This check is recommended for continuous integration to enforce consistent style; it is distinct from checking configuration validity.

### s03 · check · Judge configuration-gate evidence
Check your judgement — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [choice, intro, grading=client] terraform validate exits successfully, but terraform fmt -check exits nonzero because of noncanonical formatting. What does the formatting result establish?
  ✘ o1: A formatting failure proves the configuration is syntactically invalid.
      why: Not supported. fmt -check checks canonical formatting; validate checks syntax and internal consistency, and neither verifies remote API success.
  ✘ o2: A formatting failure proves remote provider APIs will reject the resource.
      why: Not supported. fmt -check checks canonical formatting; validate checks syntax and internal consistency, and neither verifies remote API success.
  ✔ o3: A formatting failure, not by itself a configuration-validity failure; the additional formatting gate should block progression.
      why: Correct. fmt -check checks canonical formatting; validate checks syntax and internal consistency, and neither verifies remote API success.
  feedback✔: fmt -check checks canonical formatting; validate checks syntax and internal consistency, and neither verifies remote API success.  feedback✘: fmt -check checks canonical formatting; validate checks syntax and internal consistency, and neither verifies remote API success.  hints: ['Separate the observation already recorded from the additional evidence the conclusion needs.']  remediation→r01
  MEASURES: A:distinguish_formatting_failure_from_configuration_invalidity(f4)   anchors=['assessment:distinguish_formatting_failure_from_configuration_invalidity']
  taught-before-tested: A.f4←s01

### s04 · hands_on · Review configuration-gate evidence
Evidence review — Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each independent supplied evidence excerpt and its reviewer decision. Decide whether that decision is supported by the evidence and the verification requirements, or unsupported. A supported decision may correctly identify a failure; it does not always mean the operation succeeded.
  '```text
Workflow: init -backend=false, then blocking validate, then blocking fmt -check, then supplied approved apply.
Before correction: instance_typ argument; validate exit 1; apply not executed.
After supplied correction to instance_type: validate exit 0; fmt -check exit 0.
Approved apply outcome: one EC2 instance provisioned; result retained separately from static results.
Reviewer decision: Accept the failed-to-corrected gate evidence and separate provisioning outcome.
```' -> Supported decision
      feedback: Initialization precedes blocking checks; invalid configuration stops apply, correction passes checks and provisioning has its own evidence.
  '```text
Workflow: init -backend=false; validate exit 1; continue-on-error: true; approved apply executed.
Reviewer decision: Accept as a blocking validation gate.
```' -> Unsupported decision
      feedback: The nonzero validation result did not block apply.
  '```text
Workflow: init -backend=false; validate exit 0; fmt -check exit 1 due only to noncanonical spacing; apply blocked.
After terraform fmt: validate exit 0; fmt -check exit 0; apply not yet executed.
Reviewer decision: The first failure is formatting-only; corrected static success does not prove provisioning.
```' -> Supported decision
      feedback: Canonical formatting is distinct from syntax/internal consistency and from remote provisioning success.
  '```text
Workflow: init -backend=false; validate exit 0; fmt -check exit 0; apply not executed.
Reviewer decision: Declare one EC2 instance provisioned because static checks passed.
```' -> Unsupported decision
      feedback: Static checks do not verify remote state or provider API success; provisioning needs separate execution evidence.
  feedback✔: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  feedback✘: Compare every review decision with the supplied settings and observed results; keep discrepancies visible.  hints: ['Distinguish saved configuration from observed execution evidence.', 'Check whether the reviewer preserves failures and respects the supplied scope.']  remediation→r02
  MEASURES: A:distinguish_static_validation_from_remote_service_verification(f1); A:initialize_dependencies_for_static_validation(f2); A:verify_validation_failure_blocks_infrastructure_execution(f3); A:distinguish_formatting_failure_from_configuration_invalidity(f4)   anchors=['practice', 'assessment:distinguish_static_validation_from_remote_service_verification', 'assessment:initialize_dependencies_for_static_validation', 'assessment:verify_validation_failure_blocks_infrastructure_execution', 'assessment:distinguish_formatting_failure_from_configuration_invalidity']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f4←s01

### s05 · recap · Keep these checks separate
Takeaways — 
(takeaway) Initialize dependencies, block on validation failure, and distinguish formatting, static validity and provisioning evidence. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] aws_devops.tile.067: Continue to the next tile.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Formatting success is not configuration validity or provider API success.
(mechanism) terraform fmt -check checks canonical formatting and can serve as an additional blocking configuration check. ⟦A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) For the supplied invalid EC2 declaration, validation failure must block apply. After correction, rerun validation and any blocking formatting check. A formatting-only change is not a configuration-validity correction, and static-check success is not provisioning evidence. ⟦A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Formatting success is not configuration validity or provider API success.
(mechanism) terraform validate checks syntax and internal consistency, not remote service state or provider API success. ⟦A.f1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Where backend access is unnecessary, initialize needed providers and modules with terraform init -backend=false before static validation. ⟦A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Make terraform validate blocking. Stop on nonzero exit, correct the invalid declaration and rerun before the supplied approved apply step. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) terraform fmt -check checks canonical formatting and can serve as an additional blocking configuration check. ⟦A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) For the supplied invalid EC2 declaration, validation failure must block apply. After correction, rerun validation and any blocking formatting check. A formatting-only change is not a configuration-validity correction, and static-check success is not provisioning evidence. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧