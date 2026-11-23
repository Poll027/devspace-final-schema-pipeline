# EVALUATOR PACKET — Bound retries and preserve error evidence (aws_devops.tile.067)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.handle_aws_automation_errors_with_bounded_retries_and_useful_reporting — Handle AWS automation errors with bounded retries and useful reporting; AWS SDK call is a supplied ready function, not an assumed skill or prerequisite

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.handle_aws_automation_errors_with_bounded_retries_and_useful_reporting)   objective: Handle AWS automation errors with bounded retries
A.f1: AWS SDK retries cover selected transient or throttling errors rather than making every failed request safe to repeat.   [sources: boto3_guide#retries.html]
A.f2: Set botocore.config.Config(retries={"mode": "standard", "total_max_attempts": APPROVED_ATTEMPTS}) on the supplied Boto3 client to bound requests with the SDK’s backoff; do not wrap terminal errors in an unbounded retry loop.   [sources: boto3_guide#retries.html]
A.f3: Catch botocore.exceptions.ClientError around the supplied call, inspect its response["Error"]["Code"] and response["Error"]["Message"] and preserve response["ResponseMetadata"]["RequestId"] when present; report the terminal failure or exhausted retry outcome.   [sources: boto3_guide#error-handling.html]
A.f4: When configuring Boto3, total_max_attempts includes the initial request, whereas max_attempts in a Config object counts retries after the initial request.   [sources: boto3_guide#retries.html]
note: Use supplied call and ClientError handling; do not invent error codes, additional retry causes or independent retry loops.
PRACTICE ANCHOR (live_code): Configure the supplied Boto3 client with standard SDK retries and the approved total attempt budget. Add ClientError handling around the supplied ready AWS-call function and report the final outcome without implementing the AWS operation or adding an independent retry loop.  SUCCESS: The supplied client uses standard mode and total_max_attempts equal to APPROVED_ATTEMPTS. The supplied call is invoked once at the application level. Terminal or exhausted-retry ClientError outcomes retain Error Code, Error Message, and RequestId when present, and are reported rather than repeated indefinitely.
ASSESSMENT ANCHOR: distinguish_retry_eligible_errors_from_terminal_failures facts=['f1', 'f2']
ASSESSMENT ANCHOR: interpret_and_bound_sdk_attempt_counts facts=['f2', 'f4']
ASSESSMENT ANCHOR: report_final_outcome_with_error_details_and_request_id facts=['f3']

## DATA ASSETS USED
ds.retry_counting: SDK request budget comparison — columns: configuration(categorical), mode(categorical), configured_value(numerical), initial_requests(numerical), maximum_retries(numerical), maximum_total_requests(numerical)
   ["total_max_attempts","standard",3,1,2,3]
   ["max_attempts","standard",3,1,3,4]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply an approved security baseline to sandbox accounts; Apply bounded EKS workload configuration and secrets after external configuration/secrets preparation; Audit KMS-backed audit-storage encryption (SSE-KMS): verify encryption and KMS key-use authority; key-use authority is required for SSE-KMS, not SSE-S3; Audit storage access; Configure CodePipeline source-to-deploy actions; directly require native IAM identity-policy evaluation and role trust for the service execution role, not pipeline federation; Credential expiry; Deploy a supplied CloudFormation S3 environment across accounts and Regions with assumed roles; directly require the native S3 object-storage concept; Destroy review; Diagnose AWS connectivity failures using prepared DNS, HTTP, ports and CIDR foundations; Dry run; Ecs task identity; Execute an established fleet patch task after external package-management and shell preparation; Expose an EKS workload using a Kubernetes Service; Identify avoidable charges with Cost Explorer; Inject a controlled failure and verify alarm behavior; Operate an EKS Deployment using supplied cluster-access setup; Partial failure; Perform a Lambda version-and-alias release with rollback

## LESSON, in learner order

### s01 · explainer · Bound retries and preserve error evidence
Understand — 
(intro) A supplied AWS call needs a finite retry budget and a useful final report, not a loop around every failure. ⟦A:tb1⟧
(definition) SDK retries cover selected transient or throttling errors; not every failed request is safe to repeat. ⟦A.f1 A:tb2⟧
(mechanism) Configure the supplied Boto3 client with botocore.config.Config(retries={"mode": "standard", "total_max_attempts": APPROVED_ATTEMPTS}) for bounded SDK backoff. Do not loop around terminal errors. ⟦A.f2 A:tb3⟧
(mechanism) Catch botocore.exceptions.ClientError around the supplied call. Inspect response["Error"]["Code"] and response["Error"]["Message"], retain response["ResponseMetadata"]["RequestId"] when present, and report terminal failure or exhausted retries. ⟦A.f3 A:tb3⟧
(mechanism) total_max_attempts includes the initial request; Config max_attempts counts retries after it. ⟦A.f4 A:tb3⟧
[CODE python]
from botocore.config import Config
from botocore.exceptions import ClientError

config = Config(retries={"mode": "standard", "total_max_attempts": APPROVED_ATTEMPTS})
client = supplied_client_setup(config)
try:
    result = supplied_ready_call(client)
except ClientError as error:
    code = error.response["Error"]["Code"]
    message = error.response["Error"]["Message"]
    request_id = error.response.get("ResponseMetadata", {}).get("RequestId")
    supplied_report_failure(code, message, request_id)
else:
    supplied_report_success(result)
  annotations: ['Supplied setup and reporting helpers are illustrative. APPROVED_ATTEMPTS=3: 1 initial request plus at most 2 retries; Config max_attempts=3 counts 3 retries after the initial request.', 'One application-level call; selected eligible SDK retries use bounded backoff.', 'Report terminal failure or exhausted retries with Code, Message and optional RequestId.']
[TABLE ds.retry_counting cols=all ] caption: SDK attempt-count comparison

### s02 · explainer · Bound retries and preserve error evidence
Understand — 
(example) With the approved total_max_attempts budget of 3, the initial request leaves at most 2 retries. Config max_attempts=3 instead allows 3 retries after the first request. Invoke the supplied call once at application level; let standard SDK backoff handle eligible retries. Catch ClientError and report Code and Message, retaining RequestId if present. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧
(misconception) The two settings count different things. Selected retry support does not justify repeating every error indefinitely; terminal or exhausted-retry failures need a final report. ⟦A.f1 A.f4 A:tb5⟧

### s03 · check · Judge bound retries and preserve error evidence
Check your judgement — Read the supplied excerpts in this step and decide which conclusions or procedures are correct, defective or unsafe.

### s04 · hands_on · Review bound retries and preserve error evidence
Evidence review — Read the supplied excerpts in this step and decide which conclusions or procedures are correct, defective or unsafe.

### s05 · recap · Keep the evidence distinctions
Takeaways — 
(takeaway) Use standard SDK backoff for selected eligible errors, with a finite total_max_attempts budget including the initial request. Config max_attempts counts retries instead. Report ClientError Code and Message and preserve RequestId when present. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Support a cost-driver recommendation: An apparently unused resource is a lead, not a billed-charge conclusion.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit bound retries and preserve error evidence
(mechanism) Catch botocore.exceptions.ClientError around the supplied call. Inspect response["Error"]["Code"] and response["Error"]["Message"], preserve response["ResponseMetadata"]["RequestId"] when present, and report terminal failure or exhausted retries. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) Contrast bounded SDK handling with an unlimited application retry loop. Report terminal or exhausted outcomes instead of treating every error as repeatable. ⟦A.f3 A:tb3 A:tb4⟧
[TABLE ds.retry_counting cols=all ] caption: Revisit the same supplied exercise evidence
### r02 · Revisit bound retries and preserve error evidence
(mechanism) SDK retries cover selected transient or throttling errors, not every failed request. ⟦A.f1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Use botocore.config.Config(retries={"mode": "standard", "total_max_attempts": APPROVED_ATTEMPTS}) on the supplied client for bounded SDK backoff; do not loop around terminal errors. ⟦A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) total_max_attempts includes the initial request; max_attempts in a Config object counts retries after it. ⟦A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast bounded SDK handling with an unlimited application retry loop. Report terminal or exhausted outcomes instead of treating every error as repeatable. ⟦A.f1 A.f2 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.retry_counting cols=all ] caption: Revisit the same supplied exercise evidence

=========

# EVALUATOR PACKET — Support a cost-driver recommendation (aws_devops.tile.068)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.identify_avoidable_charges_with_cost_explorer — Identify avoidable charges with Cost Explorer

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.identify_avoidable_charges_with_cost_explorer)   objective: Identify avoidable charges with Cost Explorer
A.f1: Cost Explorer analyzes billed cost and usage for selected time intervals and grouping dimensions.   [sources: aws_cost_management_user_guide#ce-what-is.html]
A.f2: Filter the supplied period and account, group by service or usage type, and inspect the cost and usage values to identify the supported cost driver.   [sources: aws_cost_management_user_guide#ce-filtering.html]
A.f3: Use the billed usage evidence to justify the avoidable charge rather than equating the existence of a resource with a specific charge.   [sources: aws_cost_management_user_guide#ce-what-is.html]
note: Do not introduce price estimates or unapproved teardown; use the supplied billing evidence.
PRACTICE ANCHOR (tool_simulation): Inspect one supplied billing dataset using Cost Explorer controls: filter to the supplied account and period, group by service or usage type, and identify an actionable avoidable charge supported by billed cost and usage evidence.  SUCCESS: The selected driver matches the filtered billing evidence. The recommendation cites the account, period, service or usage-type grouping, and associated cost and usage values, using supplied context to explain why the charge is avoidable rather than inferring a charge from resource existence. It recommends an action for review without estimating future costs or deleting resources.
ASSESSMENT ANCHOR: distinguish_evidence_backed_cost_driver_from_unsupported_guess facts=['f1', 'f2', 'f3']

## DATA ASSETS USED
ds.billing_evidence: Filtered cost and usage evidence — columns: account(identifier,digits-as-label), period_start(datetime), period_end(datetime), service(categorical), usage_type(categorical), billed_cost(numerical), usage(numerical), usage_unit(categorical), supplied_context(text)
   [1001,"2026-01-01","2026-01-31","Compute","idle-test-usage",24,120,"exercise usage units","Supplied owner record: temporary test usage is no longer required; recommend review."]
   [1001,"2026-01-01","2026-01-31","Storage","required-data-usage",12,60,"exercise usage units","Supplied owner record: workload still requires this usage."]
   [1002,"2026-01-01","2026-01-31","Compute","idle-test-usage",48,240,"exercise usage units","Different account; exclude from selected report."]
   [1001,"2025-12-01","2025-12-31","Compute","idle-test-usage",36,180,"exercise usage units","Different period; exclude from selected report."]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply an approved security baseline to sandbox accounts; Apply bounded EKS workload configuration and secrets after external configuration/secrets preparation; Audit KMS-backed audit-storage encryption (SSE-KMS): verify encryption and KMS key-use authority; key-use authority is required for SSE-KMS, not SSE-S3; Audit storage access; Configure CodePipeline source-to-deploy actions; directly require native IAM identity-policy evaluation and role trust for the service execution role, not pipeline federation; Credential expiry; Deploy a supplied CloudFormation S3 environment across accounts and Regions with assumed roles; directly require the native S3 object-storage concept; Destroy review; Diagnose AWS connectivity failures using prepared DNS, HTTP, ports and CIDR foundations; Dry run; Ecs task identity; Execute an established fleet patch task after external package-management and shell preparation; Expose an EKS workload using a Kubernetes Service; Inject a controlled failure and verify alarm behavior; Operate an EKS Deployment using supplied cluster-access setup; Partial failure; Perform a Lambda version-and-alias release with rollback; Perform a managed EKS Deployment rollout; Per

## LESSON, in learner order

### s01 · explainer · Support a cost-driver recommendation
Understand — 
(intro) An apparently unused resource is a lead, not a billed-charge conclusion. ⟦A:tb1⟧
(definition) Cost Explorer analyzes billed cost and usage within selected time intervals and grouping dimensions. ⟦A.f1 A:tb2⟧
(mechanism) Filter the supplied account and period. Group by service or usage type, then inspect cost and usage to identify the supported driver. Justify an avoidable charge with billed usage evidence, not resource existence. ⟦A.f2 A.f3 A:tb3⟧
[DIAGRAM: Cost Explorer review: scope, grouping, evidence] nodes=['Selected account and period {1001; 2026-01-01; 2026-01-31}', 'Group by service or usage type', 'Inspect billed cost, usage and supplied owner context'] edges=[('scope', 'groups', None), ('groups', 'evidence', None)] alt: Cost Explorer review: scope, grouping, evidence
[TABLE computed result ] caption: Selected account and interval: compare category evidence
  produced by sql: SELECT * FROM evidence WHERE account = 1001 AND period_start = '2026-01-01' AND period_end = '2026-01-31' ORDER BY service, usage_type

### s02 · explainer · Support a cost-driver recommendation
Understand — 
(example) Use account 1001 and 2026-01-01 through 2026-01-31. Compare the service or usage-type groups and their billed cost and usage. The supplied owner record for idle-test-usage says its temporary usage is no longer required; cite its report values when recommending review. The required-data-usage context says that usage remains required. Keep account, interval, grouping and values with the recommendation so another reviewer can check the attribution. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) A resource name, age or existence does not establish a numerical charge. Compare suspected drivers within the supplied interval; use billed cost and usage rather than inventing charges from inventory. This is a supported recommendation, not a forecast or an independent deletion decision. ⟦A.f1 A.f3 A:tb5⟧

### s03 · check · Judge support a cost-driver recommendation
Check your judgement — Read the supplied excerpts in this step and decide which conclusions or procedures are correct, defective or unsafe.

### s04 · hands_on · Review support a cost-driver recommendation
Evidence review — Read the supplied excerpts in this step and decide which conclusions or procedures are correct, defective or unsafe.

### s05 · recap · Keep the evidence distinctions
Takeaways — 
(takeaway) Filter account and period, group by service or usage type, and cite billed cost and usage. A resource merely existing does not establish its charge; support the recommendation with report evidence. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Verify fixed-replica reconciliation: A removed test Pod and the Deployment target are different evidence.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit support a cost-driver recommendation
(mechanism) Cost Explorer analyzes billed cost and usage for selected time intervals and grouping dimensions. ⟦A.f1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Filter the supplied period and account, group by service or usage type, and inspect the cost and usage values to identify the supported cost driver. ⟦A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Use the billed usage evidence to justify the avoidable charge rather than equating the existence of a resource with a specific charge. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast billed usage and owner context with a resource merely existing. Only the former supports this report-based cost recommendation. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.billing_evidence cols=all ] caption: Revisit the same supplied exercise evidence
### r02 · Revisit support a cost-driver recommendation
(mechanism) Cost Explorer analyzes billed cost and usage for selected time intervals and grouping dimensions. ⟦A.f1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Filter the supplied period and account, group by service or usage type, and inspect the cost and usage values to identify the supported cost driver. ⟦A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Use the billed usage evidence to justify the avoidable charge rather than equating the existence of a resource with a specific charge. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast billed usage and owner context with a resource merely existing. Only the former supports this report-based cost recommendation. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.billing_evidence cols=all ] caption: Revisit the same supplied exercise evidence

=========

# EVALUATOR PACKET — Verify fixed-replica reconciliation (aws_devops.tile.069)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.operate_an_eks_deployment_using_supplied_cluster_access_setup — Operate an EKS Deployment using supplied cluster-access setup

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.operate_an_eks_deployment_using_supplied_cluster_access_setup)   objective: Operate an EKS Deployment
A.f1: A Deployment manages ReplicaSets to reconcile the requested Pod replicas and Pod template.   [sources: kubernetes_overview#../workloads/controllers/deployment/]
A.f2: Apply the supplied Deployment with kubectl apply -f FILE and inspect kubectl get deployment NAME and the associated Pods.   [sources: kubernetes_overview#../workloads/controllers/deployment/]
A.f3: Delete one controlled test Pod and verify the controller creates a replacement and restores the requested replica count.   [sources: kubernetes_overview#../workloads/controllers/deployment/]
note: Use supplied cluster access and deletion procedure; do not add kubectl commands absent from allowed knowledge.
PRACTICE ANCHOR (tool_simulation): With cluster access supplied, apply the supplied three-replica Deployment using kubectl apply -f FILE. Inspect kubectl get deployment NAME and the associated Pods through the supplied inspection procedure. Remove one approved test Pod through the supplied deletion procedure, then observe reconciliation.  SUCCESS: Evidence records the requested three replicas and associated Pods before deletion, identifies the removed Pod and its replacement, and confirms that the requested count remains three and the observed count returns to three. Deletion acceptance alone does not establish success.
ASSESSMENT ANCHOR: explain_deployment_replicaset_reconciliation facts=['f1']
ASSESSMENT ANCHOR: verify_requested_and_observed_replica_counts facts=['f2']
ASSESSMENT ANCHOR: verify_controller_replacement_and_replica_restoration facts=['f1', 'f3']

## DATA ASSETS USED
ds.deployment_reconciliation: Unchanged target and replacement Pod — columns: phase(categorical), deployment(identifier), requested_replicas(numerical), observed_replicas(numerical), associated_pod_identities(text), removed_pod(identifier), replacement_pod(identifier)
   ["before removal","orders",3,3,"orders-pod-a, orders-pod-b, orders-pod-c",null,null]
   ["during reconciliation","orders",3,2,"orders-pod-b, orders-pod-c","orders-pod-a",null]
   ["after replacement","orders",3,3,"orders-pod-b, orders-pod-c, orders-pod-d","orders-pod-a","orders-pod-d"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply an approved security baseline to sandbox accounts; Apply bounded EKS workload configuration and secrets after external configuration/secrets preparation; Audit KMS-backed audit-storage encryption (SSE-KMS): verify encryption and KMS key-use authority; key-use authority is required for SSE-KMS, not SSE-S3; Audit storage access; Configure CodePipeline source-to-deploy actions; directly require native IAM identity-policy evaluation and role trust for the service execution role, not pipeline federation; Credential expiry; Deploy a supplied CloudFormation S3 environment across accounts and Regions with assumed roles; directly require the native S3 object-storage concept; Destroy review; Diagnose AWS connectivity failures using prepared DNS, HTTP, ports and CIDR foundations; Dry run; Ecs task identity; Execute an established fleet patch task after external package-management and shell preparation; Expose an EKS workload using a Kubernetes Service; Inject a controlled failure and verify alarm behavior; Partial failure; Perform a Lambda version-and-alias release with rollback; Perform a managed EKS Deployment rollout; Perform an EC2 blue/green deployment with CodeDeploy; Perform clea

## LESSON, in learner order

### s01 · explainer · Verify fixed-replica reconciliation
Understand — 
(intro) A removed test Pod and the Deployment target are different evidence. ⟦A:tb1⟧
(definition) A Deployment manages ReplicaSets to reconcile requested Pod replicas and the Pod template. ⟦A.f1 A:tb2⟧
(mechanism) Apply the supplied Deployment with kubectl apply -f orders-deployment.yaml. Inspect kubectl get deployment orders and associated Pods. Delete one controlled test Pod through the supplied procedure; verify a replacement restores the requested count. ⟦A.f2 A.f3 A:tb3⟧
[BEFORE_AFTER] The requested target is unchanged; replacement identity and restored observed count verify reconciliation.
  before:
[TABLE computed result ] caption: before removal
  produced by sql: SELECT * FROM evidence WHERE phase = 'before removal'
  after:
[TABLE computed result ] caption: after replacement
  produced by sql: SELECT * FROM evidence WHERE phase = 'after replacement'
[TABLE computed result ] caption: during reconciliation
  produced by sql: SELECT * FROM evidence WHERE phase = 'during reconciliation'

### s02 · explainer · Verify fixed-replica reconciliation
Understand — 
(example) The orders Deployment requests 3 replicas throughout this exercise. Before removal, inspect its requested count and associated Pods. The controlled removal of orders-pod-a produces a temporary observed shortage. Continue inspection until the controller creates orders-pod-d and restores the target. Completion evidence combines replacement identity with the restored count; accepted deletion alone does not verify reconciliation. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) The requested count stays the target while the observed count temporarily falls. Deleting one test Pod does not change that target. ReplicaSet reconciliation restores requested Pods and template; this is not demand-based scaling or cluster control-plane administration. ⟦A.f1 A.f3 A:tb5⟧

### s03 · check · Judge verify fixed-replica reconciliation
Check your judgement — Read the supplied excerpts in this step and decide which conclusions or procedures are correct, defective or unsafe.

### s04 · hands_on · Review verify fixed-replica reconciliation
Evidence review — Read the supplied excerpts in this step and decide which conclusions or procedures are correct, defective or unsafe.

### s05 · recap · Keep the evidence distinctions
Takeaways — 
(takeaway) A Deployment manages ReplicaSets to reconcile replicas and template. Apply the supplied Deployment, inspect it and associated Pods, and verify replacement plus restored count after controlled Pod removal. The requested target stays unchanged. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Order recovery by verified prerequisites: A component list can still describe an unusable recovery order.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit verify fixed-replica reconciliation
(mechanism) A Deployment manages ReplicaSets to reconcile the requested Pod replicas and Pod template. ⟦A.f1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Delete one controlled test Pod and verify the controller creates a replacement and restores the requested replica count. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast an accepted Pod deletion with a replacement and restored count. Only the latter verifies the requested workload is reconciled. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.deployment_reconciliation cols=all ] caption: Revisit the same supplied exercise evidence
### r02 · Revisit verify fixed-replica reconciliation
(mechanism) A Deployment manages ReplicaSets to reconcile the requested Pod replicas and Pod template. ⟦A.f1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Apply the supplied Deployment with kubectl apply -f FILE and inspect kubectl get deployment NAME and the associated Pods. ⟦A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Delete one controlled test Pod and verify the controller creates a replacement and restores the requested replica count. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast an accepted Pod deletion with a replacement and restored count. Only the latter verifies the requested workload is reconciled. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.deployment_reconciliation cols=all ] caption: Revisit the same supplied exercise evidence

=========

# EVALUATOR PACKET — Order recovery by verified prerequisites (aws_devops.tile.070)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.plan_infrastructure_and_data_restoration_in_dependency_order — Plan infrastructure and data restoration in dependency order

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.plan_infrastructure_and_data_restoration_in_dependency_order)   objective: Order infrastructure and data restoration
A.f1: A workload recovery plan must account for dependencies and the recovery capabilities needed to satisfy its objectives.   [sources: aws_well_architected_framework#rel13-bp02.html]
A.f2: List the supplied infrastructure, data and service dependencies and place each prerequisite restoration before the steps that depend on it.   [sources: aws_well_architected_framework#rel13-bp02.html]
A.f3: Include verification points before dependent services resume so incomplete restoration is not mistaken for usable recovery.   [sources: aws_well_architected_framework#rel13-bp02.html]
note: Use supplied dependency graph and objectives; do not invent a mandatory service-wide recovery ordering.
PRACTICE ANCHOR (ordering): Order the supplied infrastructure restoration, database restoration, verification, and application resumption steps using one workload's supplied dependency record, recovery objectives, and recovery capabilities.  SUCCESS: Every prerequisite restoration precedes its dependent step, and every supplied readiness verification precedes dependent service resumption. The plan is compared with the stated recovery objectives and capabilities, without imposing an unsupported order on independent steps.
ASSESSMENT ANCHOR: identify_recovery_prerequisites_for_a_dependent_service facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_required_verification_before_service_resumption facts=['f3']

## DATA ASSETS USED
ds.recovery_dependencies: Supplied restoration dependencies — columns: step_id(identifier), step(text), prerequisite_step_id(identifier), supplied_capability(text), readiness_objective(text)
   ["restore_infrastructure","Restore infrastructure",null,"Supplied infrastructure restoration procedure","Infrastructure can be restored in the isolated exercise."]
   ["verify_infrastructure","Verify infrastructure readiness","restore_infrastructure","Supplied infrastructure readiness check","Infrastructure readiness must pass before database restoration."]
   ["restore_database","Restore database","verify_infrastructure","Supplied database restoration procedure","Database restoration capability is supplied."]
   ["verify_database","Verify database readiness","restore_database","Supplied database readiness check","Database readiness must pass before application resumption."]
   ["resume_application","Resume orders application","verify_database","Supplied application resumption procedure","Resume only after prerequisite readiness is verified."]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply an approved security baseline to sandbox accounts; Apply bounded EKS workload configuration and secrets after external configuration/secrets preparation; Audit KMS-backed audit-storage encryption (SSE-KMS): verify encryption and KMS key-use authority; key-use authority is required for SSE-KMS, not SSE-S3; Audit storage access; Configure CodePipeline source-to-deploy actions; directly require native IAM identity-policy evaluation and role trust for the service execution role, not pipeline federation; Credential expiry; Deploy a supplied CloudFormation S3 environment across accounts and Regions with assumed roles; directly require the native S3 object-storage concept; Destroy review; Diagnose AWS connectivity failures using prepared DNS, HTTP, ports and CIDR foundations; Dry run; Ecs task identity; Execute an established fleet patch task after external package-management and shell preparation; Expose an EKS workload using a Kubernetes Service; Inject a controlled failure and verify alarm behavior; Partial failure; Perform a Lambda version-and-alias release with rollback; Perform a managed EKS Deployment rollout; Perform an EC2 blue/green deployment with CodeDeploy; Perform clea

## LESSON, in learner order

### s01 · explainer · Order recovery by verified prerequisites
Understand — 
(intro) A component list can still describe an unusable recovery order. ⟦A:tb1⟧
(definition) Account for workload dependencies and the recovery capabilities needed to meet recovery objectives. ⟦A.f1 A:tb2⟧
(mechanism) List supplied infrastructure, data and service dependencies. Restore each prerequisite before dependent work, with readiness verification before dependent services resume. Incomplete restoration is not usable recovery. ⟦A.f2 A.f3 A:tb3⟧
[DIAGRAM: Supplied workload recovery dependencies and readiness checkpoints] nodes=['Restore infrastructure {Supplied infrastructure restoration procedure; Infrastructure can be restored in the isolated exercise.}', 'Verify infrastructure readiness {Supplied infrastructure readiness check; Infrastructure readiness must pass before database restoration.}', 'Restore database {Supplied database restoration procedure; Database restoration capability is supplied.}', 'Verify database readiness {Supplied database readiness check; Database readiness must pass before application resumption.}', 'Resume orders application {Supplied application resumption procedure; Resume only after prerequisite readiness is verified.}'] edges=[('restore_infrastructure', 'verify_infrastructure', 'Prerequisite before dependent step'), ('verify_infrastructure', 'restore_database', 'Prerequisite before dependent step'), ('restore_database', 'verify_database', 'Prerequisite before dependent step'), ('verify_database', 'resume_application', 'Prerequisite before dependent step')] alt: Supplied workload recovery dependencies and readiness checkpoints

### s02 · explainer · Order recovery by verified prerequisites
Understand — 
(example) The supplied record makes infrastructure readiness a prerequisite for database restoration, and database readiness a prerequisite for resuming the orders application. Place restoration and its verification before each dependent step. Compare the ordered plan with the supplied capabilities and recovery objective: usable service with verified prerequisites. A scheduled dependent step is not ready if earlier restoration remains incomplete. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) These edges describe this exercise, not a universal AWS sequence. If supplied dependencies include independent branches, do not invent an order between them. Listing components is not enough: the plan must show prerequisite order and readiness checkpoints before dependent services resume. ⟦A.f2 A.f3 A:tb5⟧

### s03 · check · Judge order recovery by verified prerequisites
Check your judgement — Read the supplied excerpts in this step and decide which conclusions or procedures are correct, defective or unsafe.

### s04 · hands_on · Review order recovery by verified prerequisites
Evidence review — Read the supplied excerpts in this step and decide which conclusions or procedures are correct, defective or unsafe.

### s05 · recap · Keep the evidence distinctions
Takeaways — 
(takeaway) Order supplied infrastructure, data and service prerequisites before dependent work. Match recovery capabilities to objectives and require readiness verification before services resume; incomplete restoration is not usable recovery. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Correlate a request in logs: Correlate the failed orders request with its identity and timestamps, not unrelated nearby messages.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit order recovery by verified prerequisites
(mechanism) Include verification points before dependent services resume so incomplete restoration is not mistaken for usable recovery. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast a scheduled dependent service with one whose prerequisites passed readiness checks. Scheduling alone is not usable recovery. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.recovery_dependencies cols=all ] caption: Revisit the same supplied exercise evidence
### r02 · Revisit order recovery by verified prerequisites
(mechanism) A workload recovery plan must account for dependencies and the recovery capabilities needed to satisfy its objectives. ⟦A.f1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) List the supplied infrastructure, data and service dependencies and place each prerequisite restoration before the steps that depend on it. ⟦A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Include verification points before dependent services resume so incomplete restoration is not mistaken for usable recovery. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast a scheduled dependent service with one whose prerequisites passed readiness checks. Scheduling alone is not usable recovery. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.recovery_dependencies cols=all ] caption: Revisit the same supplied exercise evidence

=========

# EVALUATOR PACKET — Correlate a request in logs / Verify the owner receives the alarm (aws_devops.tile.071)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.query_logs_to_correlate_a_service_symptom — Query logs to correlate a service symptom
B = aws_devops.route_alarm_notifications_to_an_operational_owner — Route alarm notifications to an operational owner

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.query_logs_to_correlate_a_service_symptom)   objective: Correlate a service symptom using logs
A.f1: Logs Insights queries select and transform log events using commands connected with pipe characters.   [sources: aws_cloudwatch_user_guide#../logs/CWL_QuerySyntax.html]
A.f2: Select the log group and time window, then use fields @timestamp, @message, REQUEST_FIELD | filter REQUEST_FIELD = "ID" | sort @timestamp asc with the actual supplied request field and identity.   [sources: aws_cloudwatch_user_guide#../logs/CWL_QuerySyntax-Filter.html]
A.f3: Use shared request identity and event timestamps to reconstruct the supplied symptom’s sequence, retaining the relevant events as evidence.   [sources: aws_cloudwatch_user_guide#../logs/CWL_QuerySyntax-Sort.html]
note: Trace the supplied fields/filter/sort query; do not add untaught query functions or X-Ray tracing.
PRACTICE ANCHOR (live_code): Query one supplied structured log group within the supplied time window, substituting the actual request field and identity into the fields/filter/sort template to reconstruct the seeded orders request failure.  SUCCESS: The query returns events for the supplied request identity in ascending timestamp order. The learner retains the relevant receipt, failure and response events and uses them to describe the request sequence without treating unrelated nearby messages as evidence.
ASSESSMENT ANCHOR: scope_and_filter_events_by_time_window_and_request_identity facts=['f1', 'f2']
ASSESSMENT ANCHOR: reconstruct_request_sequence_from_relevant_events facts=['f3']

## SOURCE FACTS — B (aws_devops.route_alarm_notifications_to_an_operational_owner)   objective: Route alarm notifications to an owner
B.f1: An alarm action can publish state-change notifications to an SNS topic without changing the alarm’s metric evaluation.   [sources: aws_cloudwatch_user_guide#Notify_Users_Alarm_Changes.html]
B.f2: Configure the approved topic as the alarm’s notification action and create the approved recipient subscription, confirming it when required.   [sources: aws_cloudwatch_user_guide#Notify_Users_Alarm_Changes.html]
B.f3: Verify the recipient receives a test alarm notification containing alarm and workload context; a configured but unconfirmed subscription may not deliver notifications.   [sources: aws_cloudwatch_user_guide#Notify_Users_Alarm_Changes.html]
note: Use supplied SNS topic/recipient and test; leave fault injection to its dedicated concept.
PRACTICE ANCHOR (tool_simulation): Connect one supplied CloudWatch alarm to the approved SNS topic and recipient endpoint, confirm the subscription when required, and use the supplied test alarm notification to verify receipt.  SUCCESS: The supplied alarm uses the approved SNS topic as its notification action without changes to metric evaluation. The approved recipient subscription is confirmed when required, and receipt evidence shows that the intended operational owner received the supplied test notification containing alarm and workload context.
ASSESSMENT ANCHOR: distinguish_notification_routing_from_metric_evaluation facts=['f1']
ASSESSMENT ANCHOR: verify_approved_recipient_subscription_readiness facts=['f2', 'f3']
ASSESSMENT ANCHOR: verify_test_notification_receipt_with_alarm_and_workload_context facts=['f3']

## DATA ASSETS USED
ds.alarm_receipt: Notification configuration versus receipt — columns: case_id(identifier), alarm(identifier), workload(identifier), sns_topic(identifier), recipient(pii), subscription_status(categorical), metric_evaluation_changed(categorical), test_notification(text), receipt_evidence(text)
   ["confirmed_test","orders-alarm","orders","orders-notifications","orders-owner@example.invalid","confirmed",false,"Test alarm notification: alarm=orders-alarm; workload=orders","Recipient recorded receipt with alarm and workload context."]
   ["unconfirmed_test","orders-alarm","orders","orders-notifications","orders-owner@example.invalid","unconfirmed",false,"Test alarm notification: alarm=orders-alarm; workload=orders",null]
ds.orders_logs: Structured request evidence — columns: log_group(identifier), @timestamp(datetime), @message(text), request_id(identifier)
   ["/exercise/orders","2026-01-15T10:00:03Z","Response recorded: request failed","orders-request-a"]
   ["/exercise/orders","2026-01-15T10:00:01Z","Request received","orders-request-a"]
   ["/exercise/orders","2026-01-15T10:00:02Z","Request failure recorded","orders-request-a"]
   ["/exercise/orders","2026-01-15T10:00:02Z","Unrelated request failure recorded","orders-request-b"]
   ["/exercise/orders","2026-01-15T09:59:00Z","Earlier request receipt outside selected interval","orders-request-a"]
   ["/exercise/other","2026-01-15T10:00:01Z","Event in another group","orders-request-a"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply an approved security baseline to sandbox accounts; Apply bounded EKS workload configuration and secrets after external configuration/secrets preparation; Audit KMS-backed audit-storage encryption (SSE-KMS): verify encryption and KMS key-use authority; key-use authority is required for SSE-KMS, not SSE-S3; Audit storage access; Configure CodePipeline source-to-deploy actions; directly require native IAM identity-policy evaluation and role trust for the service execution role, not pipeline federation; Credential expiry; Deploy a supplied CloudFormation S3 environment across accounts and Regions with assumed roles; directly require the native S3 object-storage concept; Destroy review; Diagnose AWS connectivity failures using prepared DNS, HTTP, ports and CIDR foundations; Dry run; Ecs task identity; Execute an established fleet patch task after external package-management and shell preparation; Expose an EKS workload using a Kubernetes Service; Inject a controlled failure and verify alarm behavior; Partial failure; Perform a Lambda version-and-alias release with rollback; Perform a managed EKS Deployment rollout; Perform an EC2 blue/green deployment with CodeDeploy; Perform clea

## LESSON, in learner order

### s01 · explainer · Correlate a request in logs
Understand — 
(intro) Correlate the failed orders request with its identity and timestamps, not unrelated nearby messages. ⟦A:tb1⟧
(definition) Logs Insights selects and transforms events with commands connected by pipe characters. ⟦A.f1 A:tb2⟧
(mechanism) Select the intended log group and supplied interval. Use fields @timestamp, @message, request_id | filter request_id = "orders-request-a" | sort @timestamp asc. Replace template fields and identity with the supplied values. Retain relevant events in timestamp order to reconstruct the symptom sequence. ⟦A.f2 A.f3 A:tb3⟧
[DIAGRAM: Scoped request evidence review] nodes=['Selected log scope {/exercise/orders; 2026-01-15T10:00:00Z; 2026-01-15T10:05:00Z}', 'Logs Insights query {fields @timestamp, @message, request_id | filter request_id = "orders-request-a" | sort @timestamp asc}', 'Retain matching events in ascending timestamp order'] edges=[('scope', 'query', None), ('query', 'sequence', None)] alt: Scoped request evidence review
[TABLE computed result ] caption: Computed projection of the supplied identity and time-window selection
  produced by sql: SELECT "@timestamp", "@message", request_id FROM evidence WHERE log_group = '/exercise/orders' AND "@timestamp" >= '2026-01-15T10:00:00Z' AND "@timestamp" <= '2026-01-15T10:05:00Z' AND request_id = 'orders-request-a' ORDER BY "@timestamp" ASC

### s02 · explainer · Correlate a request in logs
Understand — 
(example) The supplied group is /exercise/orders; the interval is 2026-01-15T10:00:00Z through 2026-01-15T10:05:00Z. fields selects timestamp, message and request identity; filter keeps orders-request-a; sort orders ascending timestamps. Retain request receipt, the later failure message and the final response record as the symptom's evidence. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) Time proximity alone does not establish a shared request or prove causation. Use identity and timestamps together, keep group and interval boundaries, and retain relevant events. Correlation of this request does not prove every nearby error caused it. ⟦A.f2 A.f3 A:tb5⟧

### s03 · check · Judge correlate a request in logs
Check your judgement — Read the supplied excerpts in this step and decide which conclusions or procedures are correct, defective or unsafe.

### s04 · hands_on · Review correlate a request in logs
Evidence review — Read the supplied excerpts in this step and decide which conclusions or procedures are correct, defective or unsafe.

### s05 · explainer · Verify the owner receives the alarm
Understand — 
(intro) An alarm route needs receipt evidence, not configuration alone. ⟦B:tb1⟧
(definition) An alarm action can publish state-change notifications to SNS without changing metric evaluation. ⟦B.f1 B:tb2⟧
(mechanism) Configure the approved topic as the notification action. Create the approved recipient subscription and confirm it when required. Verify receipt of a test alarm notification with alarm and workload context; an unconfirmed subscription may not deliver. ⟦B.f2 B.f3 B:tb3⟧
(example) For orders-alarm, use orders-notifications and the approved recipient orders-owner@example.invalid. Check confirmation, then retain the test receipt containing alarm and workload context alongside the configuration. Compare the supplied confirmed receipt case with the unconfirmed case lacking receipt evidence. ⟦B.f1 B.f2 B.f3 B:tb4⟧
(misconception) A topic action is not proof of delivery. Confirm where required and test receipt. Notification routing is separate from metric evaluation; an unconfirmed subscription may not deliver, rather than necessarily failing in every case. ⟦B.f1 B.f3 B:tb5⟧
[DIAGRAM: Alarm notification route and receipt checkpoint] nodes=['orders-alarm {Metric evaluation is unchanged}', 'orders-notifications', 'orders-owner@example.invalid {Confirm subscription when required}', 'Test receipt: alarm and workload context'] edges=[('alarm', 'topic', 'Approved notification action'), ('topic', 'recipient', 'Approved subscription'), ('recipient', 'receipt', 'Verify receipt')] alt: Alarm notification route and receipt checkpoint
[TABLE ds.alarm_receipt cols=all ] caption: Configuration, confirmation and actual receipt evidence

### s06 · video · Trace the notification route
Notification route — 
[VIDEO ] bridge-before:  | bridge-after: 

### s07 · check · Judge verify the owner receives the alarm
Check your judgement — Read the supplied excerpts in this step and decide which conclusions or procedures are correct, defective or unsafe.

### s08 · hands_on · Review verify the owner receives the alarm
Evidence review — Read the supplied excerpts in this step and decide which conclusions or procedures are correct, defective or unsafe.

### s09 · recap · Keep the evidence distinctions
Takeaways — 
(takeaway) Use the supplied group, interval, request identity and piped fields/filter/sort query. Retain timestamp-ordered relevant events; nearby messages alone do not prove correlation or causation. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Route the alarm to the approved SNS topic and recipient; confirm when required and verify test receipt with alarm/workload context. Configuration alone is not receipt, and routing leaves metric evaluation unchanged. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Separate Lambda invocation from task outcome: A supplied Lambda task needs bounded permissions and separate invocation and outcome evidence.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit correlate a request in logs
(mechanism) Use shared request identity and event timestamps to reconstruct the supplied symptom’s sequence, retaining the relevant events as evidence. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast shared identity plus timestamps with time proximity alone. Nearby events can belong to another request. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.orders_logs cols=all ] caption: Revisit the same supplied exercise evidence
### r02 · Revisit correlate a request in logs
(mechanism) Logs Insights queries select and transform log events using commands connected with pipe characters. ⟦A.f1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Select the log group and time window, then use fields @timestamp, @message, REQUEST_FIELD | filter REQUEST_FIELD = "ID" | sort @timestamp asc with the actual supplied request field and identity. ⟦A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Use shared request identity and event timestamps to reconstruct the supplied symptom’s sequence, retaining the relevant events as evidence. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast shared identity plus timestamps with time proximity alone. Nearby events can belong to another request. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.orders_logs cols=all ] caption: Revisit the same supplied exercise evidence
### r03 · Revisit verify the owner receives the alarm
(mechanism) Verify the recipient receives a test alarm notification containing alarm and workload context; a configured but unconfirmed subscription may not deliver notifications. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) Contrast a configured subscription with a received test notification. An unconfirmed subscription may not deliver; configuration alone is not receipt evidence. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.alarm_receipt cols=all ] caption: Revisit the same supplied exercise evidence
### r04 · Revisit verify the owner receives the alarm
(mechanism) An alarm action can publish state-change notifications to an SNS topic without changing the alarm’s metric evaluation. ⟦B.f1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Configure the approved topic as the alarm’s notification action and create the approved recipient subscription, confirming it when required. ⟦B.f2 B:tb2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Verify the recipient receives a test alarm notification containing alarm and workload context; a configured but unconfirmed subscription may not deliver notifications. ⟦B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
(misconception) Contrast a configured subscription with a received test notification. An unconfirmed subscription may not deliver; configuration alone is not receipt evidence. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.alarm_receipt cols=all ] caption: Revisit the same supplied exercise evidence

=========

# EVALUATOR PACKET — Separate Lambda invocation from task outcome (aws_devops.tile.073)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.run_a_bounded_operational_action_with_lambda — Run a bounded operational action with Lambda

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.run_a_bounded_operational_action_with_lambda)   objective: Run a bounded Lambda operational action
A.f1: A Lambda execution role grants the function permission to access AWS resources during invocation.   [sources: aws_lambda_developer_guide#lambda-intro-execution-role.html]
A.f2: Assign the approved execution role whose actions and resources are limited to the supplied operational task.   [sources: aws_lambda_developer_guide#lambda-intro-execution-role.html]
A.f3: Invoke the function with the supplied payload and inspect its returned result and execution logs, distinguishing successful invocation from a successful operational result.   [sources: aws_lambda_developer_guide#invocation-sync.html]
note: Use supplied function and payload; do not introduce serverless concurrency or application authoring.
PRACTICE ANCHOR (tool_simulation): Assign the approved scoped execution role to one supplied Lambda operational function, invoke it with the supplied payload, and inspect its returned result and execution logs.  SUCCESS: The assigned role permits only the approved task's actions and resources. The supplied payload is used unchanged, and the recorded outcome distinguishes successful invocation from operational success or failure using the returned task result and execution logs, without broadening permissions.
ASSESSMENT ANCHOR: verify_execution_role_limits_actions_and_resources_to_approved_task facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_invocation_success_from_operational_success_using_result_and_logs facts=['f3']

## DATA ASSETS USED
ds.lambda_outcomes: Invocation and operational outcomes — columns: case_id(identifier), function(identifier), execution_role(identifier), approved_task_scope(text), supplied_payload(text), invocation_status(categorical), task_result(categorical), execution_logs(text), permission_context(text)
   ["task_failed","orders-resource-check","orders-check-role","Only approved actions/resources for the supplied resource check","Supplied resource-check payload, unchanged","success","failure","Resource check completed: expected operation failed.","Do not broaden approved role."]
   ["task_succeeded","orders-resource-check","orders-check-role","Only approved actions/resources for the supplied resource check","Supplied resource-check payload, unchanged","success","success","Resource check completed: task succeeded.","Evidence verifies this bounded task only."]
   ["permission_not_approved","orders-resource-check","orders-check-role","Only approved actions/resources for the supplied resource check","Supplied resource-check payload, unchanged","success","failure","Task reports needed action absent from approved role.","Report permission/result evidence without

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply an approved security baseline to sandbox accounts; Apply bounded EKS workload configuration and secrets after external configuration/secrets preparation; Audit KMS-backed audit-storage encryption (SSE-KMS): verify encryption and KMS key-use authority; key-use authority is required for SSE-KMS, not SSE-S3; Audit storage access; Configure CodePipeline source-to-deploy actions; directly require native IAM identity-policy evaluation and role trust for the service execution role, not pipeline federation; Credential expiry; Deploy a supplied CloudFormation S3 environment across accounts and Regions with assumed roles; directly require the native S3 object-storage concept; Destroy review; Diagnose AWS connectivity failures using prepared DNS, HTTP, ports and CIDR foundations; Dry run; Ecs task identity; Execute an established fleet patch task after external package-management and shell preparation; Expose an EKS workload using a Kubernetes Service; Inject a controlled failure and verify alarm behavior; Partial failure; Perform a Lambda version-and-alias release with rollback; Perform a managed EKS Deployment rollout; Perform an EC2 blue/green deployment with CodeDeploy; Perform clea

## LESSON, in learner order

### s01 · explainer · Separate Lambda invocation from task outcome
Understand — 
(intro) A supplied Lambda task needs bounded permissions and separate invocation and outcome evidence. ⟦A:tb1⟧
(definition) The execution role grants the function access to AWS resources during invocation. ⟦A.f1 A:tb2⟧
(mechanism) Assign the approved role limited to the supplied task’s actions and resources. Invoke with the supplied payload. Inspect returned result and execution logs: invocation success is not proof of operational success. ⟦A.f2 A.f3 A:tb3⟧
[DIAGRAM: Bounded role, supplied payload and separate outcome evidence] nodes=['orders-resource-check {Supplied resource-check payload, unchanged}', 'orders-check-role {Only approved actions/resources for the supplied resource check}', 'Invocation status', 'Operational outcome {Inspect returned task result and execution logs}'] edges=[('role', 'function', 'Approved resource permissions'), ('function', 'invocation', None), ('function', 'outcome', None)] alt: Bounded role, supplied payload and separate outcome evidence
[TABLE ds.lambda_outcomes cols=all ] caption: Invocation status is separate from task result and execution logs

### s02 · explainer · Separate Lambda invocation from task outcome
Understand — 
(example) The supplied function orders-resource-check uses orders-check-role, limited to the approved resource check. Keep its supplied payload unchanged. In the failure case, invocation succeeds but the task result reports failure and the logs support that failure. Do not label the operation successful from invocation status alone. Compare with the case whose task-success result and execution logs support success; record both with role and payload context. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) This verifies the bounded task, not every possible operation. The execution role is not unlimited authority. If the task reports an action absent from the approved role, retain permission and result evidence rather than broadening the role during the test. Always separate ability to invoke from permission scope and task outcome. ⟦A.f1 A.f3 A:tb5⟧

### s03 · check · Judge separate Lambda invocation from task outcome
Check your judgement — Read the supplied excerpts in this step and decide which conclusions or procedures are correct, defective or unsafe.

### s04 · hands_on · Review separate Lambda invocation from task outcome
Evidence review — Read the supplied excerpts in this step and decide which conclusions or procedures are correct, defective or unsafe.

### s05 · recap · Keep the evidence distinctions
Takeaways — 
(takeaway) Keep the approved execution role limited to the supplied task’s actions and resources. Invoke with the supplied payload and inspect returned result plus logs. Invocation success alone is not operational success. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Continue to aws_devops.tile.074: Continue the operational-response path.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit separate Lambda invocation from task outcome
(mechanism) Invoke the function with the supplied payload and inspect its returned result and execution logs, distinguishing successful invocation from a successful operational result. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast successful invocation with a successful task result supported by logs. Invocation alone does not verify the operation; keep approved role scope unchanged. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.lambda_outcomes cols=all ] caption: Revisit the same supplied exercise evidence
### r02 · Revisit separate Lambda invocation from task outcome
(mechanism) A Lambda execution role grants the function permission to access AWS resources during invocation. ⟦A.f1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Assign the approved execution role whose actions and resources are limited to the supplied operational task. ⟦A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Invoke the function with the supplied payload and inspect its returned result and execution logs, distinguishing successful invocation from a successful operational result. ⟦A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast successful invocation with a successful task result supported by logs. Invocation alone does not verify the operation; keep approved role scope unchanged. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.lambda_outcomes cols=all ] caption: Revisit the same supplied exercise evidence