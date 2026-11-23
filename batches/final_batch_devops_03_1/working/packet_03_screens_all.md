# EVALUATOR PACKET — Python environment and AWS context / Complete structured CLI inventory (aws_devops.tile.032)
Tile summary: Inspect the supplied evidence and distinguish what each check establishes.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.execute_python_aws_automation_in_an_isolated_dependency_environment — Execute Python AWS automation in an isolated dependency environment after active registry language preparation
B = aws_devops.extract_structured_aws_cli_inventory_across_paginated_results — Extract structured AWS CLI inventory across paginated results

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.execute_python_aws_automation_in_an_isolated_dependency_environment)   objective: Execute Python AWS automation in an isolated environment
A.f1: A virtual environment isolates the Python interpreter context and installed packages used by an application.   [sources: python_tutorial#venv.html]
A.f2: Create one with python -m venv ENV_DIR and activate it using the platform’s activation command, such as source ENV_DIR/bin/activate on Unix.   [sources: python_tutorial#venv.html]
A.f3: Install supplied dependencies with python -m pip install -r requirements.txt inside the environment, inspect them with python -m pip list, and run the supplied script with that interpreter.   [sources: python_tutorial#venv.html]
A.f4: Confirm the approved AWS profile and Region through the supplied credential configuration before running AWS automation.   [sources: boto3_guide#credentials.html]
note: Require external Python and shell preparation; activation paths are platform-specific templates.
PRACTICE ANCHOR (live_code): Create and activate one virtual environment, install and inspect the supplied dependencies, confirm the approved AWS profile and Region, and run the supplied automation script with that environment's interpreter.  SUCCESS: The supplied script runs with the activated environment's interpreter after dependency inspection and AWS context confirmation, without installing packages into the host's global Python environment.
ASSESSMENT ANCHOR: distinguish_dependency_isolation_from_host_configuration facts=['f1']
ASSESSMENT ANCHOR: verify_environment_scoped_dependency_setup_and_execution facts=['f2', 'f3']
ASSESSMENT ANCHOR: confirm_approved_aws_profile_and_region facts=['f4']

## SOURCE FACTS — B (aws_devops.extract_structured_aws_cli_inventory_across_paginated_results)   objective: Extract AWS CLI inventory across pagination
B.f1: The AWS CLI automatically follows service-side pagination for supported commands unless automatic pagination is disabled.   [sources: aws_cli_user_guide#cli-usage-pagination.html]
B.f2: Use an explicit --profile and --region with --output json for structured inventory and avoid --no-paginate when the full listing is required.   [sources: aws_cli_user_guide#cli-usage-pagination.html]
B.f3: --page-size changes service-call page size rather than the total output count; --max-items limits output and a returned NextToken must be resumed with --starting-token when manually collecting the remainder.   [sources: aws_cli_user_guide#cli-usage-pagination.html]
note: Apply pagination only to supported commands; do not invent an inventory command or API continuation format.
PRACTICE ANCHOR (tool_simulation): Export one sandbox resource inventory using a supplied supported AWS CLI inventory command with explicit --profile, --region, and --output json. Keep automatic pagination enabled for the full listing, then use a bounded exercise to practise retaining a returned NextToken and resuming with --starting-token.  SUCCESS: The full-listing export uses the supplied sandbox profile and Region consistently and does not use --no-paginate or an output limit. In the bounded exercise, the learner preserves each returned NextToken, resumes in the same context until no continuation remains, and distinguishes --page-size from --max-items.
ASSESSMENT ANCHOR: verify_full_listing_uses_automatic_pagination facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_consistent_profile_region_and_json_output facts=['f2']
ASSESSMENT ANCHOR: distinguish_page_size_from_output_limit_and_verify_token_resumption facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authorize an event target with least-privilege execution permissions; Automate prohibited-configuration checks; Cloudformation drift; Cloudformation rollback; Configure GitHub Actions AWS role federation; Configure a CodeBuild buildspec for a supplied application; Configure a CodeDeploy deployment action for a supplied EC2 application; Configure a budget notification; Configure and verify an EC2 Auto Scaling policy under bounded load; Configure artifact repository access; Configure artifact repository retention; Configure load-balancer listeners, targets and health checks; Ec2 instance profile; Eks workload identity; Extract structured AWS CLI inventory across paginated results; Hand over an actionable operational runbook; Operate an EKS Pod using supplied cluster-access setup; Operate an RDS managed database as the native backup-resource foundation; Protect recoverable S3 objects with versioning and lifecycle controls; Publish a container image to ECR after external Docker preparation; Publish a traceable immutable build artifact; Read and modify a standard CloudFormation S3 template; directly require the native S3 object-storage concept; Retrieve a managed workload secret after e

## LESSON, in learner order

### s01 · explainer · Python environment and AWS context
Orders sandbox · explainer — 
(intro) Prepare dependencies and confirm the AWS context before the supplied automation script runs. ⟦A:tb1⟧
(definition) An application’s virtual environment isolates its interpreter context and installed Python packages. ⟦A.f1 A:tb2⟧
(mechanism) Create the environment with python -m venv ENV_DIR. Activate it with your platform’s command; on Unix, for example, use source ENV_DIR/bin/activate. ⟦A.f2 A:tb3⟧
(mechanism) Inside the environment, install supplied requirements with python -m pip install -r requirements.txt. Inspect packages with python -m pip list, then use that interpreter for the supplied script. ⟦A.f3 A:tb3⟧
(mechanism) Before AWS automation runs, confirm the approved AWS profile and Region through the supplied credential configuration. ⟦A.f4 A:tb3⟧
[DIAGRAM: Illustrative evidence checklist—not an execution transcript.] nodes=['Virtual environment: ENV_DIR active', 'Dependency installation: requirements.txt through ENV_DIR’s interpreter', 'Package inspection: through the same interpreter', 'AWS context: approved profile and Region confirmed separately', 'Supplied script: uses ENV_DIR’s interpreter after both checks'] edges=[('n1', 'n2', 'environment-scoped installation'), ('n2', 'n3', 'inspect installed packages'), ('n3', 'n5', 'dependency evidence checked'), ('n4', 'n5', 'separate AWS-context check')] alt: Illustrative evidence checklist—not an execution transcript.: Virtual environment: ENV_DIR active; Dependency installation: requirements.txt through ENV_DIR’s interpreter; Package inspection: through the same interpreter; AWS context: approved profile and Region confirmed separately; Supplied script: uses ENV_DIR’s interpreter after both checks. Virtual environment: ENV_DIR active → environment-scoped installation → Dependency installation: requirements.txt through ENV_DIR’s interpreter; Dependency installation: requirements.txt through ENV_DIR’s interpreter → inspect installed packages → Package inspection: through the same interpreter; Package inspection: through the same interpreter → dependency evidence checked → Supplied script: uses ENV_DIR’s interpreter after both checks; AWS context: approved profile and Region confirmed separately → separate AWS-context check → Supplied script: uses ENV_DIR’s interpreter after both checks

### s02 · explainer · Work through the evidence: Python environment and AWS context
Orders sandbox · explainer — 
(example) For the supplied script, create and activate ENV_DIR, install requirements.txt, and inspect the environment’s packages. Confirm the approved AWS profile and Region separately before using the environment’s interpreter. Keep the environment and context with the outcome. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧
(misconception) An isolated Python environment is not an AWS target check. Interpreter and package isolation do not replace profile and Region confirmation. ⟦A.f1 A.f4 A:tb5⟧

### s03 · check · Check python environment and AWS context
Orders sandbox · check — Read the supplied evidence in this step and choose the interpretation it supports.

### s04 · check · Check python environment and AWS context
Orders sandbox · check — Read the supplied evidence in this step and choose the interpretation it supports.

### s05 · hands_on · Review python environment and AWS context
Orders sandbox · hands on — Read the supplied excerpts in this step and decide which are correct, defective or unsafe.

### s06 · explainer · Complete structured CLI inventory
Orders sandbox · explainer — 
(intro) An inventory needs complete results from the approved account and Region. ⟦B:tb1⟧
(definition) For supported commands, AWS CLI follows service-side pagination automatically unless automatic pagination is disabled. ⟦B.f1 B:tb2⟧
(mechanism) For structured inventory, specify --profile, --region and --output json. Leave out --no-paginate when you need the full listing. ⟦B.f2 B:tb3⟧
(mechanism) --page-size adjusts service-call page size, not total output count. --max-items bounds output; retain a returned NextToken and use --starting-token to collect the remainder manually. ⟦B.f3 B:tb3⟧
(example) Keep explicit profile, Region and JSON output on the supplied supported inventory command. A full listing keeps automatic pagination enabled. A deliberately bounded --max-items listing retains NextToken for --starting-token continuation. Preserve continuation evidence with the inventory. ⟦B.f1 B.f2 B.f3 B:tb4⟧
(misconception) Smaller service pages do not imply fewer total results. --page-size and --max-items control different limits; manual continuation must not discard NextToken. ⟦B.f3 B:tb5⟧
[PROCESS_FLOW: Complete structured CLI inventory] nodes=['Explicit --profile / --region / --output json', 'Supported command: automatic pagination', 'Service request / response', 'More results?', 'Full listing', '--max-items bounded portion', 'Returned NextToken', 'Resume with --starting-token', '--page-size: service calls, not total count'] edges=[('n1', 'n2', 'full listing'), ('n2', 'n3', 'automatic service request'), ('n3', 'n4', 'response received'), ('n4', 'n3', 'more results: next request'), ('n4', 'n5', 'no results remain'), ('n1', 'n6', 'bounded collection'), ('n6', 'n7', 'retain continuation'), ('n7', 'n8', 'same explicit profile and Region'), ('n8', 'n6', 'collect remainder')] alt: Automatic collection follows requests and responses until no results remain. Bounded --max-items collection resumes NextToken with --starting-token, keeping the same explicit profile and Region. --page-size changes service-call size, not total output.

### s07 · video · A closer look: Complete structured CLI inventory
Orders sandbox · video — 
[VIDEO ] bridge-before:  | bridge-after: 

### s08 · check · Check complete structured CLI inventory
Orders sandbox · check — Read the supplied evidence in this step and choose the interpretation it supports.

### s09 · hands_on · Review complete structured CLI inventory
Orders sandbox · hands on — Read the supplied excerpts in this step and decide which are correct, defective or unsafe.

### s10 · recap · Keep these distinctions
Orders sandbox · recap — 
(takeaway) Isolate Python dependencies and independently confirm the approved AWS profile and Region. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Distinguish page size from output limits, and preserve manual continuation evidence. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Up next: Hand over an actionable operational runbook: Next tile: aws_devops.tile.034.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · One contrast: Python environment and AWS context
(mechanism) An application’s virtual environment isolates its interpreter context and installed Python packages. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(misconception) An isolated Python environment is not an AWS target check. Interpreter and package isolation do not replace profile and Region confirmation. ⟦A.f1 A.f4 A:tb5⟧
### r02 · One contrast: Python environment and AWS context
(mechanism) Create the environment with python -m venv ENV_DIR. Activate it with your platform’s command; on Unix, for example, use source ENV_DIR/bin/activate. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) Inside the environment, install supplied requirements with python -m pip install -r requirements.txt. Inspect packages with python -m pip list, then use that interpreter for the supplied script. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) An isolated Python environment is not an AWS target check. Interpreter and package isolation do not replace profile and Region confirmation. ⟦A.f1 A.f4 A:tb5⟧
### r03 · One contrast: Python environment and AWS context
(mechanism) An application’s virtual environment isolates its interpreter context and installed Python packages. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Create the environment with python -m venv ENV_DIR. Activate it with your platform’s command; on Unix, for example, use source ENV_DIR/bin/activate. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) Inside the environment, install supplied requirements with python -m pip install -r requirements.txt. Inspect packages with python -m pip list, then use that interpreter for the supplied script. ⟦A.f3 A:tb3 A:tb4⟧
(mechanism) Before AWS automation runs, confirm the approved AWS profile and Region through the supplied credential configuration. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) An isolated Python environment is not an AWS target check. Interpreter and package isolation do not replace profile and Region confirmation. ⟦A.f1 A.f4 A:tb5⟧
### r04 · One contrast: Complete structured CLI inventory
(mechanism) --page-size adjusts service-call page size, not total output count. --max-items bounds output; retain a returned NextToken and use --starting-token to collect the remainder manually. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) Smaller service pages do not imply fewer total results. --page-size and --max-items control different limits; manual continuation must not discard NextToken. ⟦B.f3 B:tb5⟧
### r05 · One contrast: Complete structured CLI inventory
(mechanism) For supported commands, AWS CLI follows service-side pagination automatically unless automatic pagination is disabled. ⟦B.f1 B:tb2 B:tb4⟧
(mechanism) For structured inventory, specify --profile, --region and --output json. Leave out --no-paginate when you need the full listing. ⟦B.f2 B:tb3 B:tb4⟧
(mechanism) --page-size adjusts service-call page size, not total output count. --max-items bounds output; retain a returned NextToken and use --starting-token to collect the remainder manually. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) Smaller service pages do not imply fewer total results. --page-size and --max-items control different limits; manual continuation must not discard NextToken. ⟦B.f3 B:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction

=========

# EVALUATOR PACKET — An actionable restart runbook (aws_devops.tile.034)
Tile summary: Inspect the supplied evidence and distinguish what each check establishes.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.hand_over_an_actionable_operational_runbook — Hand over an actionable operational runbook

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.hand_over_an_actionable_operational_runbook)   objective: Hand over an actionable runbook
A.f1: A runbook documents procedures for a known operational outcome and should be usable by the operator performing the task.   [sources: aws_well_architected_framework#ops05-bp01.html]
A.f2: Write the task’s preconditions, ordered actions and expected results so execution can be checked rather than inferred.   [sources: aws_well_architected_framework#ops05-bp01.html]
A.f3: Include failure-handling and escalation instructions identifying when routine execution must stop and who takes over.   [sources: aws_well_architected_framework#ops06-bp03.html]
note: Use established procedures and owners; defer live incident execution to the later runbook-recovery concept.
PRACTICE ANCHOR (external_proof): Produce one bounded runbook for a supplied restart task using its established procedure and owner information. Document the outcome, preconditions, ordered actions, checkable expected results, failure-handling instructions, stop condition and escalation recipient.  SUCCESS: The submitted runbook lets another operator identify when the task may begin, which approved actions occur in order, how to check each expected result, when routine execution must stop and who takes over. It introduces no actions outside the supplied procedure.
ASSESSMENT ANCHOR: identify_task_outcome_and_preconditions facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_ordered_actions_and_checkable_success_signals facts=['f2']
ASSESSMENT ANCHOR: identify_failure_handling_stop_conditions_and_escalation_recipient facts=['f3']

## DATA ASSETS USED
ds.orders_restart_runbook: Orders restart: operator handover — columns: action_order(numerical), outcome(text), preconditions(text), approved_action(text), expected_result(text), failure_handling(text), stop_condition(text), escalation_recipient(categorical)
   [1,"Orders service restart completed and the supplied health result checked.","Approved restart task; intended orders service identified; receiving operator has the established procedure and on-call owner information.","Compare the task record with the intended service and approved restart procedure
   [2,"Orders service restart completed and the supplied health result checked.","Approved restart task; intended orders service identified; receiving operator has the established procedure and on-call owner information.","Perform the single restart action specified by the approved procedure.","The res
   [3,"Orders service restart completed and the supplied health result checked.","Approved restart task; intended orders service identified; receiving operator has the established procedure and on-call owner information.","Inspect the supplied service health result and compare it with the procedure's e
   [4,"Orders service restart completed and the supplied health result checked.","Approved restart task; intended orders service identified; receiving operator has the established procedure and on-call owner information.","Hand over the task record, action outcomes and checked health result to the rece

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authorize an event target with least-privilege execution permissions; Automate prohibited-configuration checks; Cloudformation drift; Cloudformation rollback; Configure GitHub Actions AWS role federation; Configure a CodeBuild buildspec for a supplied application; Configure a CodeDeploy deployment action for a supplied EC2 application; Configure a budget notification; Configure and verify an EC2 Auto Scaling policy under bounded load; Configure artifact repository access; Configure artifact repository retention; Configure load-balancer listeners, targets and health checks; Configure log retention; Ec2 instance profile; Eks workload identity; Operate an EKS Pod using supplied cluster-access setup; Operate an RDS managed database as the native backup-resource foundation; Protect recoverable S3 objects with versioning and lifecycle controls; Publish a container image to ECR after external Docker preparation; Publish a traceable immutable build artifact; Read and modify a standard CloudFormation S3 template; directly require the native S3 object-storage concept; Retrieve a managed workload secret after external secrets-handling preparation; Select one evidence-backed delivery workflow 

## LESSON, in learner order

### s01 · explainer · An actionable restart runbook
Orders sandbox · explainer — 
(intro) The receiving operator needs observable results, not the author’s memory. ⟦A:tb1⟧
(definition) A runbook records procedures for a known operational outcome and should be usable by the operator doing the task. ⟦A.f1 A:tb2⟧
(mechanism) Make preconditions, action order and expected results explicit so the operator checks execution instead of inferring it. ⟦A.f2 A:tb3⟧
(mechanism) Include failure handling and escalation: state when routine work stops and identify who takes over. ⟦A.f3 A:tb3⟧
(example) In the orders restart record, compare preconditions with the approved task before the restart. Check each expected result before advancing, including the supplied health result. Keep the stop condition and escalation recipient visible; do not invent a recovery action. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) An action list alone is insufficient. Preconditions, expected results and failure/escalation instructions make the task checkable. ⟦A.f2 A.f3 A:tb5⟧
[TABLE ds.orders_restart_runbook cols=['action_order', 'outcome', 'preconditions', 'approved_action', 'expected_result', 'failure_handling', 'stop_condition', 'escalation_recipient'] ] caption: Orders restart: operator handover — fictional supplied evidence

### s02 · check · Check an actionable restart runbook
Orders sandbox · check — Read the supplied evidence in this step and choose the interpretation it supports.

### s03 · hands_on · Review an actionable restart runbook
Orders sandbox · hands on — Read the supplied excerpts in this step and decide which are correct, defective or unsafe.

### s04 · recap · Keep these distinctions
Orders sandbox · recap — 
(takeaway) A useful runbook connects preconditions and ordered actions to checked results, stop conditions and an escalation recipient. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Operate an EKS Pod using supplied cluster-access setup: Next tile: aws_devops.tile.035.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · One contrast: An actionable restart runbook
(mechanism) Include failure handling and escalation: state when routine work stops and identify who takes over. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) An action list alone is insufficient. Preconditions, expected results and failure/escalation instructions make the task checkable. ⟦A.f2 A.f3 A:tb5⟧
[TABLE ds.orders_restart_runbook cols=['action_order', 'outcome', 'preconditions', 'approved_action', 'expected_result', 'failure_handling', 'stop_condition', 'escalation_recipient'] ] caption: Orders restart: operator handover — fictional supplied evidence
### r02 · One contrast: An actionable restart runbook
(mechanism) A runbook records procedures for a known operational outcome and should be usable by the operator doing the task. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Make preconditions, action order and expected results explicit so the operator checks execution instead of inferring it. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Include failure handling and escalation: state when routine work stops and identify who takes over. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) An action list alone is insufficient. Preconditions, expected results and failure/escalation instructions make the task checkable. ⟦A.f2 A.f3 A:tb5⟧
[TABLE ds.orders_restart_runbook cols=['action_order', 'outcome', 'preconditions', 'approved_action', 'expected_result', 'failure_handling', 'stop_condition', 'escalation_recipient'] ] caption: Orders restart: operator handover — fictional supplied evidence

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction

=========

# EVALUATOR PACKET — Read Pod and container evidence (aws_devops.tile.035)
Tile summary: Inspect the supplied evidence and distinguish what each check establishes.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.operate_an_eks_pod_using_supplied_cluster_access_setup — Operate an EKS Pod using supplied cluster-access setup

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.operate_an_eks_pod_using_supplied_cluster_access_setup)   objective: Inspect and operate an EKS Pod
A.f1: A Pod groups containers with shared networking and storage and has a lifecycle distinct from the controller that may replace it.   [sources: kubernetes_overview#../workloads/pods/pod-lifecycle/]
A.f2: Pod phases include Pending, Running, Succeeded, Failed and Unknown; phase alone is not a complete diagnosis of container health.   [sources: kubernetes_overview#../workloads/pods/pod-lifecycle/]
A.f3: Use kubectl get pod NAME, kubectl describe pod NAME and kubectl logs NAME -c CONTAINER to inspect status, scheduling or runtime events and container output.   [sources: kubernetes_overview#../../tasks/debug/debug-application/debug-pods/]
note: Use supplied cluster access; leave Deployment reconciliation and self-managed cluster administration out of scope.
PRACTICE ANCHOR (tool_simulation): Inspect one seeded failing Pod using the supplied cluster access and image. Substitute the supplied Pod and container names into kubectl get pod NAME, kubectl describe pod NAME and kubectl logs NAME -c CONTAINER, then identify the failure supported by the observations.  SUCCESS: Record the Pod phase, relevant scheduling or runtime events, and the intended container's output. Identify the seeded failure using those observations together, without treating Running as proof of container health or changing the workload.
ASSESSMENT ANCHOR: identify_pod_lifecycle_failure_from_status_events_and_logs facts=['f2', 'f3']
ASSESSMENT ANCHOR: distinguish_pod_phase_from_container_health facts=['f2']
ASSESSMENT ANCHOR: select_pod_inspection_commands_for_status_events_and_container_output facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authorize an event target with least-privilege execution permissions; Automate prohibited-configuration checks; Cloudformation drift; Cloudformation rollback; Configure GitHub Actions AWS role federation; Configure a CodeBuild buildspec for a supplied application; Configure a CodeDeploy deployment action for a supplied EC2 application; Configure a budget notification; Configure and verify an EC2 Auto Scaling policy under bounded load; Configure artifact repository access; Configure artifact repository retention; Configure load-balancer listeners, targets and health checks; Configure log retention; Configure managed database backups and create/restore RDS snapshots; require only native RDS and backup foundations, with existing network setup given and no routing or security-group skills assumed; Ec2 instance profile; Eks workload identity; Operate an RDS managed database as the native backup-resource foundation; Protect recoverable S3 objects with versioning and lifecycle controls; Publish a container image to ECR after external Docker preparation; Publish a traceable immutable build artifact; Read and modify a standard CloudFormation S3 template; directly require the native S3 objec

## LESSON, in learner order

### s01 · explainer · Read Pod and container evidence
Orders sandbox · explainer — 
(intro) A Running Pod still needs container and event evidence. ⟦A:tb1⟧
(definition) A Pod groups containers sharing networking and storage. Its lifecycle is distinct from a controller that may replace it. ⟦A.f1 A:tb2⟧
(mechanism) Pod phases include Pending, Running, Succeeded, Failed and Unknown. A phase alone does not fully diagnose container health. ⟦A.f2 A:tb3⟧
(mechanism) Inspect status with kubectl get pod NAME, events with kubectl describe pod NAME, and the intended container’s output with kubectl logs NAME -c CONTAINER. ⟦A.f3 A:tb3⟧
[DIAGRAM: Illustrative case from the lesson—not an execution transcript.] nodes=['Supplied Pod: phase Running', 'Described runtime events: container problem', 'Intended container’s logs: container problem', 'Running is a Pod phase; the events and intended-container output still show a problem.'] edges=[('n1', 'n2', 'same Pod'), ('n2', 'n3', 'same intended container'), ('n1', 'n4', 'phase alone is insufficient'), ('n3', 'n4', 'container evidence')] alt: Illustrative case from the lesson—not an execution transcript.: Supplied Pod: phase Running; Described runtime events: container problem; Intended container’s logs: container problem; Running is a Pod phase; the events and intended-container output still show a problem.. Supplied Pod: phase Running → same Pod → Described runtime events: container problem; Described runtime events: container problem → same intended container → Intended container’s logs: container problem; Supplied Pod: phase Running → phase alone is insufficient → Running is a Pod phase; the events and intended-container output still show a problem.; Intended container’s logs: container problem → container evidence → Running is a Pod phase; the events and intended-container output still show a problem.

### s02 · explainer · Work through the evidence: Read Pod and container evidence
Orders sandbox · explainer — 
(example) Read the supplied Pod’s status, described events and named container’s logs together. For Pending, use scheduling-event evidence rather than guessing a correction. For Running, inspect runtime events and output. Another container’s logs do not establish the named container’s condition. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) Running is a lifecycle phase, not a complete health diagnosis. Keep status, events and the intended container’s output together. ⟦A.f2 A.f3 A:tb5⟧

### s03 · check · Check read Pod and container evidence
Orders sandbox · check — Read the supplied evidence in this step and choose the interpretation it supports.

### s04 · hands_on · Review read Pod and container evidence
Orders sandbox · hands on — Read the supplied excerpts in this step and decide which are correct, defective or unsafe.

### s05 · recap · Keep these distinctions
Orders sandbox · recap — 
(takeaway) Pod phase is only one observation; inspect events and the intended container’s output. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Operate an RDS managed database as the native backup-resource foundation: Next tile: aws_devops.tile.036.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · One contrast: Read Pod and container evidence
(mechanism) Inspect status with kubectl get pod NAME, events with kubectl describe pod NAME, and the intended container’s output with kubectl logs NAME -c CONTAINER. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Running is a lifecycle phase, not a complete health diagnosis. Keep status, events and the intended container’s output together. ⟦A.f2 A.f3 A:tb5⟧
### r02 · One contrast: Read Pod and container evidence
(mechanism) A Pod groups containers sharing networking and storage. Its lifecycle is distinct from a controller that may replace it. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Pod phases include Pending, Running, Succeeded, Failed and Unknown. A phase alone does not fully diagnose container health. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Inspect status with kubectl get pod NAME, events with kubectl describe pod NAME, and the intended container’s output with kubectl logs NAME -c CONTAINER. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Running is a lifecycle phase, not a complete health diagnosis. Keep status, events and the intended container’s output together. ⟦A.f2 A.f3 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction

=========

# EVALUATOR PACKET — Verify the database and its data / Recoverable S3 versions (aws_devops.tile.036)
Tile summary: Inspect the supplied evidence and distinguish what each check establishes.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.operate_an_rds_managed_database — Operate an RDS managed database as the native backup-resource foundation
B = aws_devops.protect_recoverable_s3_objects_with_versioning_and_lifecycle_controls — Protect recoverable S3 objects with versioning and lifecycle controls

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.operate_an_rds_managed_database)   objective: Operate an RDS managed database
A.f1: An RDS DB instance has an identifier, engine, endpoint and operational status that can be inspected in the console or through describe-db-instances.   [sources: aws_rds_user_guide#accessing-monitoring.html]
A.f2: Inspect the intended DB instance and verify its engine and status before attempting the supplied database connection.   [sources: aws_rds_user_guide#accessing-monitoring.html]
A.f3: Connect using the supplied endpoint, database client and approved credentials, then run the supplied query to check the data marker; instance status alone does not verify application data.   [sources: aws_rds_user_guide#CHAP_CommonTasks.Connect.html]
note: Use supplied client and query; do not teach SQL syntax or database capacity selection.
PRACTICE ANCHOR (tool_simulation): Inspect the supplied sandbox RDS instance using preconfigured networking. Verify its identifier, engine and operational status before connecting with the supplied endpoint, database client and approved credentials, then run the supplied query to check the expected data marker.  SUCCESS: The recorded identifier matches the intended instance, its engine and status are compared with the supplied requirements, and its endpoint is recorded. The supplied query result is compared with the expected data marker, with the data-check outcome reported separately from instance status.
ASSESSMENT ANCHOR: verify_intended_db_instance_identity_engine_and_status facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_supplied_data_marker_using_approved_connection facts=['f3']
ASSESSMENT ANCHOR: distinguish_instance_status_from_application_data_verification facts=['f2', 'f3']

## SOURCE FACTS — B (aws_devops.protect_recoverable_s3_objects_with_versioning_and_lifecycle_controls)   objective: Protect S3 data recovery with versioning
B.f1: S3 versioning retains multiple versions of an object, including versions displaced by overwrites.   [sources: aws_s3_user_guide#Versioning.html]
B.f2: In a versioning-enabled bucket, a simple delete ordinarily creates a delete marker rather than removing prior versions; deleting a specified version permanently removes it.   [sources: aws_s3_user_guide#Versioning.html]
B.f3: To restore an overwritten object, copy the selected prior version to the same key to create a new current version; to undo a simple deletion, remove its delete marker to expose the preceding version.   [sources: aws_s3_user_guide#RestoringPreviousVersions.html]
B.f4: Inspect noncurrent-version expiration and other lifecycle rules so required recoverable versions remain for the required window.   [sources: aws_s3_user_guide#intro-lifecycle-rules.html]
note: Use approved versions and recovery window; distinguish marker removal from copying a prior version.
PRACTICE ANCHOR (tool_simulation): Enable versioning on the approved sandbox bucket and apply the supplied recovery-preserving lifecycle policy for releases/orders.zip.  SUCCESS: The bucket reports versioning as enabled, the supplied lifecycle policy is applied, and inspection of noncurrent-version expiration and other applicable rules confirms that required versions remain recoverable for the supplied recovery window.
ASSESSMENT ANCHOR: verify_overwritten_object_recovery_from_prior_version facts=['f1', 'f3']
ASSESSMENT ANCHOR: verify_deleted_object_recovery_by_delete_marker_removal facts=['f2', 'f3']
ASSESSMENT ANCHOR: verify_lifecycle_rules_preserve_required_recovery_window facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authorize an event target with least-privilege execution permissions; Automate prohibited-configuration checks; Cloudformation drift; Cloudformation rollback; Configure GitHub Actions AWS role federation; Configure a CodeBuild buildspec for a supplied application; Configure a CodeDeploy deployment action for a supplied EC2 application; Configure a budget notification; Configure and verify an EC2 Auto Scaling policy under bounded load; Configure artifact repository access; Configure artifact repository retention; Configure load-balancer listeners, targets and health checks; Configure log retention; Configure managed database backups and create/restore RDS snapshots; require only native RDS and backup foundations, with existing network setup given and no routing or security-group skills assumed; Configure scoped log access; Define an ECS task for a supplied image; Ec2 instance profile; Eks workload identity; Protect recoverable S3 objects with versioning and lifecycle controls; Publish a container image to ECR after external Docker preparation; Publish a traceable immutable build artifact; Read and modify a standard CloudFormation S3 template; directly require the native S3 object-st

## LESSON, in learner order

### s01 · explainer · Verify the database and its data
Orders sandbox · explainer — 
(intro) Instance inspection and the application-data check answer different questions. ⟦A:tb1⟧
(definition) Inspect an RDS DB instance’s identifier, engine, endpoint and operational status in the console or with describe-db-instances. ⟦A.f1 A:tb2⟧
(mechanism) Before the supplied connection attempt, inspect the intended DB instance and check its engine and status. ⟦A.f2 A:tb3⟧
(mechanism) Use the supplied endpoint, database client and approved credentials to connect. Check the data marker with the supplied query; instance status alone does not verify application data. ⟦A.f3 A:tb3⟧
[DIAGRAM: Illustrative missing-marker case—not an execution transcript.] nodes=['Intended RDS instance: identifier, engine, endpoint and status inspected', 'Expected query outcome: required data marker present', 'Observed query outcome: required data marker missing', 'Acceptable instance status does not establish application-data success.'] edges=[('n1', 'n3', 'supplied query on intended instance'), ('n2', 'n3', 'Compare the same marker'), ('n3', 'n4', 'missing marker')] alt: Illustrative missing-marker case—not an execution transcript.: Intended RDS instance: identifier, engine, endpoint and status inspected; Expected query outcome: required data marker present; Observed query outcome: required data marker missing; Acceptable instance status does not establish application-data success.. Intended RDS instance: identifier, engine, endpoint and status inspected → supplied query on intended instance → Observed query outcome: required data marker missing; Expected query outcome: required data marker present → Compare the same marker → Observed query outcome: required data marker missing; Observed query outcome: required data marker missing → missing marker → Acceptable instance status does not establish application-data success.

### s02 · explainer · Work through the evidence: Verify the database and its data
Orders sandbox · explainer — 
(example) Tie the supplied instance identifier and endpoint to the engine/status inspection. Then read the supplied connection and query outcome for the expected data marker. Acceptable status with a missing marker is not a successful data check. Keep the safe query result with the instance context. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) Instance status cannot substitute for the data marker, and the marker does not substitute for checking the intended instance. ⟦A.f2 A.f3 A:tb5⟧

### s03 · check · Check verify the database and its data
Orders sandbox · check — Read the supplied evidence in this step and choose the interpretation it supports.

### s04 · hands_on · Review verify the database and its data
Orders sandbox · hands on — Read the supplied excerpts in this step and decide which are correct, defective or unsafe.

### s05 · explainer · Recoverable S3 versions
Orders sandbox · explainer — 
(intro) Choose the recovery method for the actual overwrite or simple-deletion case. ⟦B:tb1⟧
(definition) S3 versioning retains multiple object versions, including versions displaced by an overwrite. ⟦B.f1 B:tb2⟧
(mechanism) In a versioning-enabled bucket, a simple delete ordinarily adds a delete marker rather than removing earlier versions. Deleting a specified version removes it permanently. ⟦B.f2 B:tb3⟧
(mechanism) For an overwrite, copy the selected prior version to the same key, creating a new current version. Undo a simple deletion by removing its delete marker to expose the preceding version. ⟦B.f3 B:tb3⟧
(mechanism) Check noncurrent-version expiration and other lifecycle rules against the required recovery window so needed recoverable versions remain available. ⟦B.f4 B:tb3⟧
[DIAGRAM: Illustrative schematic histories: releases/orders.zip] nodes=['Overwrite: selected prior version', 'Copy to releases/orders.zip', 'New current version', 'Simple deletion: delete marker above preceding version', 'Remove marker', 'Preceding version exposed', 'Versioning enabled; inspect noncurrent-version expiration and other lifecycle rules against the required recovery window', 'Deleting a specified version is permanent.'] edges=[('n1', 'n2', 'copy selected prior version'), ('n2', 'n3', 'creates'), ('n4', 'n5', 'undo simple deletion'), ('n5', 'n6', 'exposes'), ('n7', 'n1', 'overwrite recovery window'), ('n7', 'n4', 'simple-deletion recovery window'), ('n7', 'n8', 'specified-version deletion is distinct')] alt: Illustrative schematic histories: releases/orders.zip: Overwrite: selected prior version; Copy to releases/orders.zip; New current version; Simple deletion: delete marker above preceding version; Remove marker; Preceding version exposed; Versioning enabled; inspect noncurrent-version expiration and other lifecycle rules against the required recovery window; Deleting a specified version is permanent.. Overwrite: selected prior version → copy selected prior version → Copy to releases/orders.zip; Copy to releases/orders.zip → creates → New current version; Simple deletion: delete marker above preceding version → undo simple deletion → Remove marker; Remove marker → exposes → Preceding version exposed; Versioning enabled; inspect noncurrent-version expiration and other lifecycle rules against the required recovery window → overwrite recovery window → Overwrite: selected prior version; Versioning enabled; inspect noncurrent-version expiration and other lifecycle rules against the required recovery window → simple-deletion recovery window → Simple deletion: delete marker above preceding version; Versioning enabled; inspect noncurrent-version expiration and other lifecycle rules against the required recovery window → specified-version deletion is distinct → Deleting a specified version is permanent.

### s06 · explainer · Work through the evidence: Recoverable S3 versions
Orders sandbox · explainer — 
(example) For overwritten releases/orders.zip, copy the required prior version to the same key to create a new current version. For a separate simple deletion, remove the delete marker to expose the preceding version. Check lifecycle expiration against the required recovery window; do not permanently delete a needed specified version. ⟦B.f1 B.f2 B.f3 B.f4 B:tb4⟧
(misconception) A simple delete ordinarily creates a marker; a specified-version deletion is permanent. Versioning alone does not guarantee indefinite retention under lifecycle rules. ⟦B.f2 B.f4 B:tb5⟧

### s07 · check · Check recoverable S3 versions
Orders sandbox · check — Read the supplied evidence in this step and choose the interpretation it supports.

### s08 · check · Check recoverable S3 versions
Orders sandbox · check — Read the supplied evidence in this step and choose the interpretation it supports.

### s09 · hands_on · Review recoverable S3 versions
Orders sandbox · hands on — Read the supplied excerpts in this step and decide which are correct, defective or unsafe.

### s10 · recap · Keep these distinctions
Orders sandbox · recap — 
(takeaway) Check the intended instance’s engine and status, then verify its data marker through the supplied connection and query. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Overwrite recovery and delete-marker recovery differ. Check lifecycle rules against the required recoverability window. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Up next: Publish a container image to ECR: Next tile: aws_devops.tile.038.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · One contrast: Verify the database and its data
(mechanism) Before the supplied connection attempt, inspect the intended DB instance and check its engine and status. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Use the supplied endpoint, database client and approved credentials to connect. Check the data marker with the supplied query; instance status alone does not verify application data. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Instance status cannot substitute for the data marker, and the marker does not substitute for checking the intended instance. ⟦A.f2 A.f3 A:tb5⟧
### r02 · One contrast: Verify the database and its data
(mechanism) Inspect an RDS DB instance’s identifier, engine, endpoint and operational status in the console or with describe-db-instances. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Before the supplied connection attempt, inspect the intended DB instance and check its engine and status. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Use the supplied endpoint, database client and approved credentials to connect. Check the data marker with the supplied query; instance status alone does not verify application data. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Instance status cannot substitute for the data marker, and the marker does not substitute for checking the intended instance. ⟦A.f2 A.f3 A:tb5⟧
### r03 · One contrast: Recoverable S3 versions
(mechanism) S3 versioning retains multiple object versions, including versions displaced by an overwrite. ⟦B.f1 B:tb2 B:tb4⟧
(mechanism) For an overwrite, copy the selected prior version to the same key, creating a new current version. Undo a simple deletion by removing its delete marker to expose the preceding version. ⟦B.f3 B:tb3 B:tb4⟧
(misconception) A simple delete ordinarily creates a marker; a specified-version deletion is permanent. Versioning alone does not guarantee indefinite retention under lifecycle rules. ⟦B.f2 B.f4 B:tb5⟧
### r04 · One contrast: Recoverable S3 versions
(mechanism) In a versioning-enabled bucket, a simple delete ordinarily adds a delete marker rather than removing earlier versions. Deleting a specified version removes it permanently. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(mechanism) For an overwrite, copy the selected prior version to the same key, creating a new current version. Undo a simple deletion by removing its delete marker to expose the preceding version. ⟦B.f3 B:tb3 B:tb4⟧
(misconception) A simple delete ordinarily creates a marker; a specified-version deletion is permanent. Versioning alone does not guarantee indefinite retention under lifecycle rules. ⟦B.f2 B.f4 B:tb5⟧
### r05 · One contrast: Recoverable S3 versions
(mechanism) S3 versioning retains multiple object versions, including versions displaced by an overwrite. ⟦B.f1 B:tb2 B:tb4⟧
(mechanism) In a versioning-enabled bucket, a simple delete ordinarily adds a delete marker rather than removing earlier versions. Deleting a specified version removes it permanently. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(mechanism) For an overwrite, copy the selected prior version to the same key, creating a new current version. Undo a simple deletion by removing its delete marker to expose the preceding version. ⟦B.f3 B:tb3 B:tb4⟧
(mechanism) Check noncurrent-version expiration and other lifecycle rules against the required recovery window so needed recoverable versions remain available. ⟦B.f4 B:tb3 B:tb4 B:tb5⟧
(misconception) A simple delete ordinarily creates a marker; a specified-version deletion is permanent. Versioning alone does not guarantee indefinite retention under lifecycle rules. ⟦B.f2 B.f4 B:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction

=========

# EVALUATOR PACKET — Publish and consume exact image content / Trace an immutable build artifact (aws_devops.tile.038)
Tile summary: Inspect the supplied evidence and distinguish what each check establishes.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.publish_a_container_image_to_ecr — Publish a container image to ECR after external Docker preparation
B = aws_devops.publish_a_traceable_immutable_build_artifact — Publish a traceable immutable build artifact

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.publish_a_container_image_to_ecr)   objective: Publish a container image to ECR
A.f1: ECR stores container images in repositories and assigns image digests that identify image content.   [sources: aws_ecr_user_guide#docker-push-ecr-image.html]
A.f2: Authenticate Docker with aws ecr get-login-password --region REGION piped to docker login --username AWS --password-stdin REGISTRY.   [sources: aws_ecr_user_guide#docker-push-ecr-image.html]
A.f3: Tag the already-built image with REGISTRY/REPOSITORY:TAG and run docker push with that reference.   [sources: aws_ecr_user_guide#docker-push-ecr-image.html]
A.f4: Use docker pull REGISTRY/REPOSITORY@sha256:DIGEST to retrieve the exact image and verify publisher and consumer access with their approved identities.   [sources: aws_ecr_user_guide#docker-pull-ecr-image.html]
note: Require external Docker and shell-pipe preparation; commands are supplied-value templates.
PRACTICE ANCHOR (tool_simulation): Using an already-built image, a sandbox ECR repository, supplied Region and registry values, and separately prepared approved publisher and consumer identities, authenticate Docker, tag and push the image, then retrieve its exact published digest as the consumer.  SUCCESS: The approved publisher authenticates using aws ecr get-login-password --region REGION | docker login --username AWS --password-stdin REGISTRY and successfully pushes REGISTRY/REPOSITORY:TAG. The published digest is recorded. In the separately prepared consumer context, Docker authenticates and successfully retrieves REGISTRY/REPOSITORY@sha256:DIGEST with docker pull. The retrieved digest matches the published digest, and both identity-specific access outcomes are preserved.
ASSESSMENT ANCHOR: verify_approved_publisher_authentication_and_push facts=['f2', 'f3']
ASSESSMENT ANCHOR: verify_exact_digest_retrieval_by_approved_consumer facts=['f1', 'f4']
ASSESSMENT ANCHOR: distinguish_publisher_and_consumer_access_evidence facts=['f3', 'f4']

## SOURCE FACTS — B (aws_devops.publish_a_traceable_immutable_build_artifact)   objective: Publish a traceable immutable build artifact
B.f1: An artifact attestation binds provenance such as source repository, revision and build workflow to an artifact digest.   [sources: github_actions_docs#how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations]
B.f2: For a supplied output file, set workflow permissions id-token: write, contents: read and attestations: write, generate provenance with actions/attest@v4 and subject-path set to the file, then publish it with actions/upload-artifact@v4 using path set to that file and name set to the supplied revision-based version; retain the workflow run, artifact name and upload’s SHA256 digest as the immutable content reference, since v4 artifacts are immutable.   [sources: github_actions_docs#how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations, github_actions_docs#how-tos/writing-workflows/choosing-what-your-workflow-does/storing-and-sharing-data-from-a-workflow]
B.f3: Download the published artifact with actions/download-artifact, which checks the upload’s SHA256 digest and warns on mismatch, then verify the extracted output file’s provenance with gh attestation verify PATH/TO/YOUR/BUILD/ARTIFACT-BINARY -R ORGANIZATION_NAME/REPOSITORY_NAME --format json and inspect the verified attestation for the source revision and build workflow/run before deployment.   [sources: github_actions_docs#how-tos/writing-workflows/choosing-what-your-workflow-does/storing-and-sharing-data-from-a-workflow, github_actions_docs#how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations]
note: Use actions/attest@v4, not a substituted action; preserve the warning behavior and verify the extracted output file.
PRACTICE ANCHOR (live_code): Complete and execute a supplied GitHub Actions workflow to attest and publish the supplied orders release file for revision rev-42 under its supplied revision-based artifact name.  SUCCESS: The workflow attests and uploads the same supplied file with the required permissions and actions. The publication record retains the workflow run, revision-based artifact name and upload SHA256 digest as the immutable content reference.
ASSESSMENT ANCHOR: verify_artifact_digest_source_revision_and_build_run_linkage facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: distinguish_download_integrity_checks_from_verified_provenance facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authorize an event target with least-privilege execution permissions; Automate prohibited-configuration checks; Cloudformation drift; Cloudformation rollback; Configure GitHub Actions AWS role federation; Configure a CodeBuild buildspec for a supplied application; Configure a CodeDeploy deployment action for a supplied EC2 application; Configure a budget notification; Configure and verify an EC2 Auto Scaling policy under bounded load; Configure artifact repository access; Configure artifact repository retention; Configure load-balancer listeners, targets and health checks; Configure log retention; Configure managed database backups and create/restore RDS snapshots; require only native RDS and backup foundations, with existing network setup given and no routing or security-group skills assumed; Configure scoped log access; Define an ECS task for a supplied image; Diagnose an IAM denied request from request and policy evidence; Ec2 instance profile; Eks workload identity; Execute a reviewed Terraform plan provisioning EC2; directly require the native EC2 instance foundation; Publish a traceable immutable build artifact; Read and modify a standard CloudFormation S3 template; directly 

## LESSON, in learner order

### s01 · explainer · Publish and consume exact image content
Orders sandbox · explainer — 
(intro) Keep the publication reference distinct from the exact-content retrieval reference. ⟦A:tb1⟧
(definition) ECR repositories store container images; assigned image digests identify the content. ⟦A.f1 A:tb2⟧
(mechanism) Authenticate Docker by piping aws ecr get-login-password --region REGION to docker login --username AWS --password-stdin REGISTRY. ⟦A.f2 A:tb3⟧
(mechanism) Tag the already-built image as REGISTRY/REPOSITORY:TAG, then docker push that reference. ⟦A.f3 A:tb3⟧
(mechanism) Retrieve exact content with docker pull REGISTRY/REPOSITORY@sha256:DIGEST. Verify access separately with the approved publisher and consumer identities. ⟦A.f4 A:tb3⟧
[SIDE_BY_SIDE] Same content digest: the approved publisher’s published digest DIGEST matches the approved consumer’s retrieved digest DIGEST. left_label: Illustrative successful publication-and-consumption case: publisher | right_label: Illustrative successful publication-and-consumption case: consumer
  left:
[DIAGRAM: Tagged push: illustrative successful publication] nodes=['REGISTRY/REPOSITORY:TAG', 'docker push', 'Approved publisher: push access verified; published digest DIGEST'] edges=[('n1', 'n2', 'tagged push reference'), ('n2', 'n3', 'under approved publisher identity')] alt: Tagged push: illustrative successful publication: REGISTRY/REPOSITORY:TAG; docker push; Approved publisher: push access verified; published digest DIGEST. REGISTRY/REPOSITORY:TAG → tagged push reference → docker push; docker push → under approved publisher identity → Approved publisher: push access verified; published digest DIGEST
  right:
[DIAGRAM: Digest-qualified pull: illustrative successful consumption] nodes=['REGISTRY/REPOSITORY@sha256:DIGEST', 'docker pull', 'Approved consumer: pull access verified; retrieved digest DIGEST', 'Published digest DIGEST (approved publisher, left panel)'] edges=[('n1', 'n2', 'digest-qualified pull reference'), ('n2', 'n3', 'under approved consumer identity'), ('n4', 'n3', 'Same content digest')] alt: Digest-qualified pull: illustrative successful consumption: REGISTRY/REPOSITORY@sha256:DIGEST; docker pull; Approved consumer: pull access verified; retrieved digest DIGEST; Published digest DIGEST (approved publisher, left panel). REGISTRY/REPOSITORY@sha256:DIGEST → digest-qualified pull reference → docker pull; docker pull → under approved consumer identity → Approved consumer: pull access verified; retrieved digest DIGEST; Published digest DIGEST (approved publisher, left panel) → Same content digest → Approved consumer: pull access verified; retrieved digest DIGEST

### s02 · explainer · Work through the evidence: Publish and consume exact image content
Orders sandbox · explainer — 
(example) Use the supplied Region and registry for authentication, then tag and push the already-built image with the approved publisher. Record its digest. The approved consumer pulls that exact digest and checks its own access. Publisher success does not establish consumer access; retain both identity-specific outcomes. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧
(misconception) A convenient tag is not the stated exact-content retrieval test. Publishing alone is not verified consumption. ⟦A.f3 A.f4 A:tb5⟧

### s03 · check · Check publish and consume exact image content
Orders sandbox · check — Read the supplied evidence in this step and choose the interpretation it supports.

### s04 · hands_on · Review publish and consume exact image content
Orders sandbox · hands on — Read the supplied excerpts in this step and decide which are correct, defective or unsafe.

### s05 · explainer · Trace an immutable build artifact
Orders sandbox · explainer — 
(intro) Connect the release file’s content identity to its source and build provenance. ⟦B:tb1⟧
(definition) Artifact attestation connects an artifact digest to provenance such as source repository, revision and build workflow. ⟦B.f1 B:tb2⟧
[DIAGRAM: Illustrative successful verification case—not an execution transcript.] nodes=['Supplied orders output: revision rev-42', 'Immutable upload record: workflow run, revision-based artifact name, upload SHA256', 'Download integrity result: upload SHA256 matches', 'Verified extracted-file attestation: artifact digest, source repository, revision rev-42, build workflow/run'] edges=[('n1', 'n2', 'upload same supplied file'), ('n2', 'n3', 'Upload/download digest check'), ('n3', 'n4', 'Extracted-file provenance verification'), ('n4', 'n2', 'verified revision/workflow linked to upload record'), ('n1', 'n4', 'same revision rev-42')] alt: Illustrative successful verification case—not an execution transcript.: Supplied orders output: revision rev-42; Immutable upload record: workflow run, revision-based artifact name, upload SHA256; Download integrity result: upload SHA256 matches; Verified extracted-file attestation: artifact digest, source repository, revision rev-42, build workflow/run. Supplied orders output: revision rev-42 → upload same supplied file → Immutable upload record: workflow run, revision-based artifact name, upload SHA256; Immutable upload record: workflow run, revision-based artifact name, upload SHA256 → Upload/download digest check → Download integrity result: upload SHA256 matches; Download integrity result: upload SHA256 matches → Extracted-file provenance verification → Verified extracted-file attestation: artifact digest, source repository, revision rev-42, build workflow/run; Verified extracted-file attestation: artifact digest, source repository, revision rev-42, build workflow/run → verified revision/workflow linked to upload record → Immutable upload record: workflow run, revision-based artifact name, upload SHA256; Supplied orders output: revision rev-42 → same revision rev-42 → Verified extracted-file attestation: artifact digest, source repository, revision rev-42, build workflow/run

### s06 · explainer · The verification sequence: Trace an immutable build artifact
Orders sandbox · explainer — 
(mechanism) For the supplied output file, set id-token: write, contents: read and attestations: write. Use actions/attest@v4 with subject-path set to that file, then actions/upload-artifact@v4 with path set to it and the supplied revision-based name. Retain the run, artifact name and upload SHA256 digest as the immutable content reference; v4 artifacts are immutable. ⟦B.f2 B:tb3⟧
(mechanism) Use actions/download-artifact: it checks the upload SHA256 digest and warns on mismatch. Verify the extracted output’s provenance with gh attestation verify PATH/TO/YOUR/BUILD/ARTIFACT-BINARY -R ORGANIZATION_NAME/REPOSITORY_NAME --format json. Before deployment, inspect the verified attestation’s source revision and build workflow/run. ⟦B.f3 B:tb3⟧

### s07 · explainer · Work through the evidence: Trace an immutable build artifact
Orders sandbox · explainer — 
(example) For the supplied orders output at rev-42, attest and upload the same file using the required permissions and revision-based name. Retain the run, name and upload digest. After download, inspect any mismatch warning and verify the extracted file’s attestation for the approved repository, revision and workflow/run. ⟦B.f1 B.f2 B.f3 B:tb4⟧
(misconception) Download integrity and provenance are different checks. A digest-mismatch warning is not a promise to block every mismatch, nor proof of the intended source revision. ⟦B.f1 B.f3 B:tb5⟧

### s08 · check · Check trace an immutable build artifact
Orders sandbox · check — Read the supplied evidence in this step and choose the interpretation it supports.

### s09 · hands_on · Review trace an immutable build artifact
Orders sandbox · hands on — Read the supplied excerpts in this step and decide which are correct, defective or unsafe.

### s10 · recap · Keep these distinctions
Orders sandbox · recap — 
(takeaway) Publish by the approved tag reference; verify exact-digest retrieval with the approved consumer. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Retain the immutable upload reference; check download integrity and verified source/build provenance separately. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Up next: Read and modify a standard CloudFormation S3 template: Next tile: aws_devops.tile.040.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · One contrast: Publish and consume exact image content
(mechanism) Tag the already-built image as REGISTRY/REPOSITORY:TAG, then docker push that reference. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(mechanism) Retrieve exact content with docker pull REGISTRY/REPOSITORY@sha256:DIGEST. Verify access separately with the approved publisher and consumer identities. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) A convenient tag is not the stated exact-content retrieval test. Publishing alone is not verified consumption. ⟦A.f3 A.f4 A:tb5⟧
### r02 · One contrast: Publish and consume exact image content
(mechanism) ECR repositories store container images; assigned image digests identify the content. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Authenticate Docker by piping aws ecr get-login-password --region REGION to docker login --username AWS --password-stdin REGISTRY. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) Tag the already-built image as REGISTRY/REPOSITORY:TAG, then docker push that reference. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(mechanism) Retrieve exact content with docker pull REGISTRY/REPOSITORY@sha256:DIGEST. Verify access separately with the approved publisher and consumer identities. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) A convenient tag is not the stated exact-content retrieval test. Publishing alone is not verified consumption. ⟦A.f3 A.f4 A:tb5⟧
### r03 · One contrast: Trace an immutable build artifact
(mechanism) Use actions/download-artifact: it checks the upload SHA256 digest and warns on mismatch. Verify the extracted output’s provenance with gh attestation verify PATH/TO/YOUR/BUILD/ARTIFACT-BINARY -R ORGANIZATION_NAME/REPOSITORY_NAME --format json. Before deployment, inspect the verified attestation’s source revision and build workflow/run. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) Download integrity and provenance are different checks. A digest-mismatch warning is not a promise to block every mismatch, nor proof of the intended source revision. ⟦B.f1 B.f3 B:tb5⟧
### r04 · One contrast: Trace an immutable build artifact
(mechanism) Artifact attestation connects an artifact digest to provenance such as source repository, revision and build workflow. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(mechanism) For the supplied output file, set id-token: write, contents: read and attestations: write. Use actions/attest@v4 with subject-path set to that file, then actions/upload-artifact@v4 with path set to it and the supplied revision-based name. Retain the run, artifact name and upload SHA256 digest as the immutable content reference; v4 artifacts are immutable. ⟦B.f2 B:tb3 B:tb4⟧
(mechanism) Use actions/download-artifact: it checks the upload SHA256 digest and warns on mismatch. Verify the extracted output’s provenance with gh attestation verify PATH/TO/YOUR/BUILD/ARTIFACT-BINARY -R ORGANIZATION_NAME/REPOSITORY_NAME --format json. Before deployment, inspect the verified attestation’s source revision and build workflow/run. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) Download integrity and provenance are different checks. A digest-mismatch warning is not a promise to block every mismatch, nor proof of the intended source revision. ⟦B.f1 B.f3 B:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction

=========

# EVALUATOR PACKET — Read declaration and deployed bucket evidence (aws_devops.tile.040)
Tile summary: Inspect the supplied evidence and distinguish what each check establishes.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.read_and_modify_a_standard_cloudformation_s3_template — Read and modify a standard CloudFormation S3 template; directly require the native S3 object-storage concept

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.read_and_modify_a_standard_cloudformation_s3_template)   objective: Modify a CloudFormation S3 template
A.f1: A CloudFormation template’s Resources section declares resources by logical ID, Type and Properties.   [sources: aws_cloudformation_user_guide#template-anatomy.html]
A.f2: An S3 bucket declaration uses Type: AWS::S3::Bucket; Ref on its logical ID returns its bucket name.   [sources: aws_cloudformation_user_guide#aws-resource-s3-bucket.html]
A.f3: Modify the supplied declared property and references, validate with aws cloudformation validate-template --template-body file://TEMPLATE, and create the sandbox stack from the approved template.   [sources: aws_cloudformation_user_guide#using-cfn-validate-template.html]
A.f4: Inspect stack events and outputs and the bucket’s live property to confirm the declaration was deployed.   [sources: aws_cloudformation_user_guide#cfn-console-view-stack-data-resources.html]
note: Use the supplied property; do not introduce new resource types or template functions.
PRACTICE ANCHOR (live_code): Modify only the approved property and its supplied references in one standard CloudFormation S3 template. Validate the template, create its approved sandbox stack, and verify the bucket declaration against stack events, outputs and the live bucket property.  SUCCESS: The template declares one AWS::S3::Bucket resource, references resolve to the intended bucket logical ID, validation succeeds, and stack evidence and the live property confirm the approved change. Ref returns the deployed bucket name.
ASSESSMENT ANCHOR: verify_s3_bucket_declaration_and_ref facts=['f1', 'f2']
ASSESSMENT ANCHOR: validate_modified_standard_template facts=['f3']
ASSESSMENT ANCHOR: confirm_deployed_bucket_matches_declaration facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authorize an event target with least-privilege execution permissions; Automate prohibited-configuration checks; Cloudformation drift; Cloudformation rollback; Configure GitHub Actions AWS role federation; Configure a CodeBuild buildspec for a supplied application; Configure a CodeDeploy deployment action for a supplied EC2 application; Configure a budget notification; Configure and verify an EC2 Auto Scaling policy under bounded load; Configure artifact repository access; Configure artifact repository retention; Configure load-balancer listeners, targets and health checks; Configure log retention; Configure managed database backups and create/restore RDS snapshots; require only native RDS and backup foundations, with existing network setup given and no routing or security-group skills assumed; Configure scoped log access; Define an ECS task for a supplied image; Diagnose an IAM denied request from request and policy evidence; Ec2 instance profile; Eks workload identity; Execute a reviewed Terraform plan provisioning EC2; directly require the native EC2 instance foundation; Execute a scoped Systems Manager remote command after external shell preparation; Retrieve a managed workload 

## LESSON, in learner order

### s01 · explainer · Read declaration and deployed bucket evidence
Orders sandbox · explainer — 
(intro) The requested declaration and the live deployed property need separate evidence. ⟦A:tb1⟧
(definition) In a CloudFormation template, Resources declares each resource through its logical ID, Type and Properties. ⟦A.f1 A:tb2⟧
(mechanism) Type: AWS::S3::Bucket declares an S3 bucket. Ref on that logical ID returns the bucket name. ⟦A.f2 A:tb3⟧
(mechanism) Change the supplied declared property and references. Validate with aws cloudformation validate-template --template-body file://TEMPLATE, then create the sandbox stack from the approved template. ⟦A.f3 A:tb3⟧
(mechanism) Confirm deployment by inspecting stack events, outputs and the bucket’s live value for the declared property. ⟦A.f4 A:tb3⟧
[DIAGRAM: Read declaration and deployed bucket evidence] nodes=['Resources', 'Supplied bucket logical ID', 'Type: AWS::S3::Bucket', 'Properties: approved edit', 'Ref: bucket name', 'Validate / create approved sandbox', 'Events / outputs / live property'] edges=[('n1', 'n2', 'declares'), ('n2', 'n3', 'Type'), ('n2', 'n4', 'Properties'), ('n2', 'n5', 'Ref'), ('n4', 'n6', 'approved declaration'), ('n6', 'n7', 'verify deployment')] alt: Read declaration and deployed bucket evidence: Resources; Supplied bucket logical ID; Type: AWS::S3::Bucket; Properties: approved edit; Ref: bucket name; Validate / create approved sandbox; Events / outputs / live property

### s02 · explainer · Work through the evidence: Read declaration and deployed bucket evidence
Orders sandbox · explainer — 
(example) The supplied bucket logical ID declares the approved property value; its Ref output names that bucket. Compare the corresponding live property with the declaration after deployment. Check Type and Properties under Resources, make only approved property/reference edits, and retain validation, sandbox-creation, event and output evidence with the live-property comparison. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧
(misconception) Template validation does not verify the live bucket property. Ref returns the bucket name, not an invented object reference. ⟦A.f2 A.f3 A.f4 A:tb5⟧

### s03 · check · Check read declaration and deployed bucket evidence
Orders sandbox · check — Read the supplied evidence in this step and choose the interpretation it supports.

### s04 · hands_on · Review read declaration and deployed bucket evidence
Orders sandbox · hands on — Read the supplied excerpts in this step and decide which are correct, defective or unsafe.

### s05 · recap · Keep these distinctions
Orders sandbox · recap — 
(takeaway) Read logical ID, Type, Properties and Ref; verify the changed live property after deployment. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Retrieve a managed workload secret: Next tile: aws_devops.tile.041.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · One contrast: Read declaration and deployed bucket evidence
(mechanism) Confirm deployment by inspecting stack events, outputs and the bucket’s live value for the declared property. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Template validation does not verify the live bucket property. Ref returns the bucket name, not an invented object reference. ⟦A.f2 A.f3 A.f4 A:tb5⟧
### r02 · One contrast: Read declaration and deployed bucket evidence
(mechanism) In a CloudFormation template, Resources declares each resource through its logical ID, Type and Properties. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Type: AWS::S3::Bucket declares an S3 bucket. Ref on that logical ID returns the bucket name. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Change the supplied declared property and references. Validate with aws cloudformation validate-template --template-body file://TEMPLATE, then create the sandbox stack from the approved template. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(mechanism) Confirm deployment by inspecting stack events, outputs and the bucket’s live value for the declared property. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Template validation does not verify the live bucket property. Ref returns the bucket name, not an invented object reference. ⟦A.f2 A.f3 A.f4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction

=========

# EVALUATOR PACKET — Verify secret use without revealing it (aws_devops.tile.041)
Tile summary: Inspect the supplied evidence and distinguish what each check establishes.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.retrieve_a_managed_workload_secret — Retrieve a managed workload secret after external secrets-handling preparation

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.retrieve_a_managed_workload_secret)   objective: Retrieve a managed workload secret
A.f1: Secrets Manager stores protected secret values and returns them to authorized consumers at runtime.   [sources: aws_secrets_manager_user_guide#retrieving-secrets.html]
A.f2: Retrieve a secret through GetSecretValue using the supplied secret identifier and approved runtime identity, with secretsmanager:GetSecretValue permission.   [sources: aws_secrets_manager_user_guide#retrieving-secrets-python.html]
A.f3: Use the retrieved value in the runtime consumer without writing it into source code or logs; verify success through the consumer’s safe result rather than displaying the value.   [sources: aws_secrets_manager_user_guide#best-practices.html]
note: Do not teach managed-secret rotation; do not show example secret values.
PRACTICE ANCHOR (tool_simulation): Retrieve one sandbox secret through GetSecretValue using the supplied secret identifier and approved runtime identity, then use it in the supplied runtime consumer.  SUCCESS: The approved runtime identity has secretsmanager:GetSecretValue permission for the supplied secret. The consumer receives the retrieved value and reports safe success without displaying the value or writing it into source code or logs.
ASSESSMENT ANCHOR: verify_authorized_runtime_secret_retrieval facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_secret_use_without_persistence_or_logging facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authorize an event target with least-privilege execution permissions; Automate prohibited-configuration checks; Cloudformation drift; Cloudformation rollback; Configure GitHub Actions AWS role federation; Configure a CodeBuild buildspec for a supplied application; Configure a CodeDeploy deployment action for a supplied EC2 application; Configure a budget notification; Configure and verify an EC2 Auto Scaling policy under bounded load; Configure artifact repository access; Configure artifact repository retention; Configure load-balancer listeners, targets and health checks; Configure log retention; Configure managed database backups and create/restore RDS snapshots; require only native RDS and backup foundations, with existing network setup given and no routing or security-group skills assumed; Configure scoped log access; Define an ECS task for a supplied image; Diagnose an IAM denied request from request and policy evidence; Ec2 instance profile; Eks workload identity; Execute a reviewed Terraform plan provisioning EC2; directly require the native EC2 instance foundation; Execute a scoped Systems Manager remote command after external shell preparation; Gate infrastructure changes 

## LESSON, in learner order

### s01 · explainer · Verify secret use without revealing it
Orders sandbox · explainer — 
(intro) Check authorized runtime use without exposing the value. ⟦A:tb1⟧
(definition) Secrets Manager protects stored secret values and returns them to authorized consumers at runtime. ⟦A.f1 A:tb2⟧
(mechanism) Call GetSecretValue for the supplied secret identifier using the approved runtime identity with secretsmanager:GetSecretValue permission. ⟦A.f2 A:tb3⟧
(mechanism) Use the value in the runtime consumer without putting it in source code or logs. Verify the consumer’s safe result instead of displaying the secret. ⟦A.f3 A:tb3⟧
(example) For the supplied identifier, review GetSecretValue under the approved runtime identity and permission. Pass the value to the consumer and inspect its safe success result. Keep the value out of source and logs; a debugging transcript need not reveal it. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) Showing the secret is not necessary evidence. The consumer’s safe result verifies use without disclosure. ⟦A.f3 A:tb5⟧
[DIAGRAM: Verify secret use without revealing it] nodes=['Supplied secret identifier', 'Approved runtime identity', 'secretsmanager:GetSecretValue', 'GetSecretValue', 'Runtime consumer', 'Safe consumer result', 'No value in source or logs'] edges=[('n1', 'n4', 'identify secret'), ('n2', 'n4', 'authorized runtime identity'), ('n3', 'n4', 'required permission'), ('n4', 'n5', 'use returned value'), ('n5', 'n6', 'verify without display')] alt: Verify secret use without revealing it: Supplied secret identifier; Approved runtime identity; secretsmanager:GetSecretValue; GetSecretValue; Runtime consumer; Safe consumer result; No value in source or logs

### s02 · check · Check verify secret use without revealing it
Orders sandbox · check — Read the supplied evidence in this step and choose the interpretation it supports.

### s03 · check · Check verify secret use without revealing it
Orders sandbox · check — Read the supplied evidence in this step and choose the interpretation it supports.

### s04 · hands_on · Review verify secret use without revealing it
Orders sandbox · hands on — Read the supplied excerpts in this step and decide which are correct, defective or unsafe.

### s05 · recap · Keep these distinctions
Orders sandbox · recap — 
(takeaway) Use authorized GetSecretValue retrieval and the consumer’s safe result; keep secrets out of source and logs. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Select one evidence-backed delivery workflow improvement: Next tile: aws_devops.tile.042.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · One contrast: Verify secret use without revealing it
(mechanism) Secrets Manager protects stored secret values and returns them to authorized consumers at runtime. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Call GetSecretValue for the supplied secret identifier using the approved runtime identity with secretsmanager:GetSecretValue permission. ⟦A.f2 A:tb3 A:tb4⟧
(misconception) Showing the secret is not necessary evidence. The consumer’s safe result verifies use without disclosure. ⟦A.f3 A:tb5⟧
### r02 · One contrast: Verify secret use without revealing it
(mechanism) Use the value in the runtime consumer without putting it in source code or logs. Verify the consumer’s safe result instead of displaying the secret. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Showing the secret is not necessary evidence. The consumer’s safe result verifies use without disclosure. ⟦A.f3 A:tb5⟧
### r03 · One contrast: Verify secret use without revealing it
(mechanism) Secrets Manager protects stored secret values and returns them to authorized consumers at runtime. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Call GetSecretValue for the supplied secret identifier using the approved runtime identity with secretsmanager:GetSecretValue permission. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) Use the value in the runtime consumer without putting it in source code or logs. Verify the consumer’s safe result instead of displaying the secret. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Showing the secret is not necessary evidence. The consumer’s safe result verifies use without disclosure. ⟦A.f3 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction

=========

# EVALUATOR PACKET — Measure one delivery improvement (aws_devops.tile.042)
Tile summary: Inspect the supplied evidence and distinguish what each check establishes.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.select_one_evidence_backed_delivery_workflow_improvement — Select one evidence-backed delivery workflow improvement

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.select_one_evidence_backed_delivery_workflow_improvement)   objective: Select an evidence-backed delivery workflow improvement
A.f1: Continuous improvement uses feedback and measured outcomes to identify and address delivery friction.   [sources: aws_wa_devops_guidance#dl.cd.6-refine-delivery-pipelines-using-metrics-for-continuous-improvement.html]
A.f2: Identify a bottleneck supported by the supplied delivery evidence and propose one bounded change with a measurable expected outcome.   [sources: aws_wa_devops_guidance#dl.cd.6-refine-delivery-pipelines-using-metrics-for-continuous-improvement.html]
A.f3: Compare the success signal before and after the change to determine whether the intervention improved the intended outcome.   [sources: aws_wa_devops_guidance#dl.cd.6-refine-delivery-pipelines-using-metrics-for-continuous-improvement.html]
note: Use supplied delivery evidence; avoid inventing performance targets or attributing results to individuals.
PRACTICE ANCHOR (field_selection): Using supplied delivery records for a review handoff, select one evidence-supported bottleneck, one bounded handoff change, and a measurable success signal. Record the supplied baseline and compare it with the supplied after-change result.  SUCCESS: The selected bottleneck is supported by the records, the change addresses only that bottleneck, and the success signal measures the intended outcome without an invented target. The comparison uses the same signal before and after and reports whether it improved, remained unchanged, or worsened.
ASSESSMENT ANCHOR: identify_evidence_supported_delivery_bottleneck facts=['f2']

## DATA ASSETS USED
ds.orders_review_handoff: Orders delivery: review-handoff evidence — columns: case_id(identifier), review_handoff_evidence(text), selected_bottleneck(categorical), bounded_change(text), success_signal(text), expected_outcome(text), baseline_minutes(numerical), after_change_minutes(numerical)
   ["handoff.improved","The delivery record shows 40 minutes waiting between review-ready handoff and review start; every other measured delivery-stage wait is shorter.","Review handoff","Name one receiving reviewer in the existing handoff record.","Minutes from review-ready handoff to review start","R
   ["handoff.unchanged","The delivery record shows 40 minutes waiting between review-ready handoff and review start; every other measured delivery-stage wait is shorter.","Review handoff","Name one receiving reviewer in the existing handoff record.","Minutes from review-ready handoff to review start","
   ["handoff.worsened","The delivery record shows 40 minutes waiting between review-ready handoff and review start; every other measured delivery-stage wait is shorter.","Review handoff","Name one receiving reviewer in the existing handoff record.","Minutes from review-ready handoff to review start","R

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authorize an event target with least-privilege execution permissions; Automate prohibited-configuration checks; Cloudformation drift; Cloudformation rollback; Configure GitHub Actions AWS role federation; Configure a CodeBuild buildspec for a supplied application; Configure a CodeDeploy deployment action for a supplied EC2 application; Configure a budget notification; Configure and verify an EC2 Auto Scaling policy under bounded load; Configure artifact repository access; Configure artifact repository retention; Configure load-balancer listeners, targets and health checks; Configure log retention; Configure managed database backups and create/restore RDS snapshots; require only native RDS and backup foundations, with existing network setup given and no routing or security-group skills assumed; Configure scoped log access; Define an ECS task for a supplied image; Diagnose an IAM denied request from request and policy evidence; Ec2 instance profile; Eks workload identity; Execute a reviewed Terraform plan provisioning EC2; directly require the native EC2 instance foundation; Execute a scoped Systems Manager remote command after external shell preparation; Gate infrastructure changes 

## LESSON, in learner order

### s01 · explainer · Measure one delivery improvement
Orders sandbox · explainer — 
(intro) Choose one measured bottleneck, not a general preference for change. ⟦A:tb1⟧
(definition) Continuous improvement identifies and addresses delivery friction using feedback and measured outcomes. ⟦A.f1 A:tb2⟧
(mechanism) Choose a bottleneck supported by the supplied delivery evidence. Propose one bounded change and a measurable expected outcome. ⟦A.f2 A:tb3⟧
(mechanism) Compare the same success signal before and after the change to judge whether the intended outcome improved. ⟦A.f3 A:tb3⟧
[TABLE ds.orders_review_handoff cols=['case_id', 'review_handoff_evidence', 'selected_bottleneck', 'bounded_change', 'success_signal', 'expected_outcome', 'baseline_minutes', 'after_change_minutes'] ] caption: Orders delivery: review-handoff evidence — fictional supplied evidence

### s02 · explainer · Work through the evidence: Measure one delivery improvement
Orders sandbox · explainer — 
(example) The orders review-handoff record supports one bottleneck and a bounded handoff change. Keep its success signal fixed across baseline and after-change observations. Report improvement, no change or worsening from that comparison; completing the action alone does not establish success. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) Do not switch to a more flattering measure when the chosen signal fails to improve. Implementation is not proof of improvement. ⟦A.f2 A.f3 A:tb5⟧

### s03 · check · Check measure one delivery improvement
Orders sandbox · check — Read the supplied evidence in this step and choose the interpretation it supports.

### s04 · hands_on · Review measure one delivery improvement
Orders sandbox · hands on — Read the supplied evidence in this step and choose the interpretation it supports.

### s05 · recap · Keep these distinctions
Orders sandbox · recap — 
(takeaway) Choose one evidence-supported bottleneck and compare the same success signal before and after its bounded change. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Triage a basic configuration-compliance finding: Next tile: aws_devops.tile.043.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · One contrast: Measure one delivery improvement
(mechanism) Choose a bottleneck supported by the supplied delivery evidence. Propose one bounded change and a measurable expected outcome. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) Do not switch to a more flattering measure when the chosen signal fails to improve. Implementation is not proof of improvement. ⟦A.f2 A.f3 A:tb5⟧
[TABLE ds.orders_review_handoff cols=['case_id', 'review_handoff_evidence', 'selected_bottleneck', 'bounded_change', 'success_signal', 'expected_outcome', 'baseline_minutes', 'after_change_minutes'] ] caption: Orders delivery: review-handoff evidence — fictional supplied evidence
### r02 · One contrast: Measure one delivery improvement
(mechanism) Continuous improvement identifies and addresses delivery friction using feedback and measured outcomes. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Choose a bottleneck supported by the supplied delivery evidence. Propose one bounded change and a measurable expected outcome. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Compare the same success signal before and after the change to judge whether the intended outcome improved. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Do not switch to a more flattering measure when the chosen signal fails to improve. Implementation is not proof of improvement. ⟦A.f2 A.f3 A:tb5⟧
[TABLE ds.orders_review_handoff cols=['case_id', 'review_handoff_evidence', 'selected_bottleneck', 'bounded_change', 'success_signal', 'expected_outcome', 'baseline_minutes', 'after_change_minutes'] ] caption: Orders delivery: review-handoff evidence — fictional supplied evidence

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction

=========

# EVALUATOR PACKET — Triage recorded configuration evidence (aws_devops.tile.043)
Tile summary: Inspect the supplied evidence and distinguish what each check establishes.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.triage_a_basic_configuration_compliance_finding — Triage a basic configuration-compliance finding

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.triage_a_basic_configuration_compliance_finding)   objective: Triage a configuration compliance finding
A.f1: AWS Config rules evaluate recorded resource configuration against desired conditions and report compliance results.   [sources: aws_config_developer_guide#evaluate-config.html]
A.f2: Open the rule’s noncompliant resources and inspect the affected resource, evaluation result and rule parameters to identify the configuration mismatch.   [sources: aws_config_developer_guide#evaluate-config_view-compliance.html]
A.f3: Choose the established remediation or escalation path from the governing policy rather than treating a compliance result as proof of an attack.   [sources: aws_config_developer_guide#remediation.html]
note: Do not infer compromise or design specialist security remediation.
PRACTICE ANCHOR (tool_simulation): Triage one supplied AWS Config finding under an established policy by opening the rule's noncompliant resources, inspecting the affected resource's recorded configuration, evaluation result and rule parameters, and selecting the permitted remediation or escalation path.  SUCCESS: Identify the violated rule and affected resource, distinguish the rule's required value from the recorded value, and select the next action authorized by the supplied policy. Preserve the evaluation evidence supporting that choice without inferring an attack or applying an unapproved change.
ASSESSMENT ANCHOR: identify_violated_rule_and_configuration_mismatch facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_affected_resource_from_evaluation_evidence facts=['f2']
ASSESSMENT ANCHOR: select_policy_governed_safe_next_action facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authorize an event target with least-privilege execution permissions; Automate prohibited-configuration checks; Cloudformation drift; Cloudformation rollback; Configure GitHub Actions AWS role federation; Configure a CodeBuild buildspec for a supplied application; Configure a CodeDeploy deployment action for a supplied EC2 application; Configure a budget notification; Configure and verify an EC2 Auto Scaling policy under bounded load; Configure artifact repository access; Configure artifact repository retention; Configure load-balancer listeners, targets and health checks; Configure log retention; Configure managed database backups and create/restore RDS snapshots; require only native RDS and backup foundations, with existing network setup given and no routing or security-group skills assumed; Configure scoped log access; Define an ECS task for a supplied image; Diagnose an IAM denied request from request and policy evidence; Ec2 instance profile; Eks workload identity; Execute a reviewed Terraform plan provisioning EC2; directly require the native EC2 instance foundation; Execute a scoped Systems Manager remote command after external shell preparation; Gate infrastructure changes 

## LESSON, in learner order

### s01 · explainer · Triage recorded configuration evidence
Orders sandbox · explainer — 
(intro) Establish the recorded mismatch before selecting the policy-governed response. ⟦A:tb1⟧
(definition) AWS Config rules compare recorded resource configuration with desired conditions and report compliance results. ⟦A.f1 A:tb2⟧
(mechanism) Open the rule’s noncompliant resources. Inspect the affected resource, evaluation result and rule parameters to identify the configuration mismatch. ⟦A.f2 A:tb3⟧
(mechanism) Follow the governing policy’s established remediation or escalation path. A compliance result is not proof of an attack. ⟦A.f3 A:tb3⟧
[DIAGRAM: Illustrative configuration mismatch: A and B are symbolic values.] nodes=['Affected resource: recorded configuration value B', 'Rule parameter: required value A', 'Evaluation result: noncompliant because recorded B differs from required A', 'Governing policy: select the established remediation or escalation path—not proof of an attack'] edges=[('n1', 'n3', 'recorded value'), ('n2', 'n3', 'required value'), ('n3', 'n4', 'governing response')] alt: Illustrative configuration mismatch: A and B are symbolic values.: Affected resource: recorded configuration value B; Rule parameter: required value A; Evaluation result: noncompliant because recorded B differs from required A; Governing policy: select the established remediation or escalation path—not proof of an attack. Affected resource: recorded configuration value B → recorded value → Evaluation result: noncompliant because recorded B differs from required A; Rule parameter: required value A → required value → Evaluation result: noncompliant because recorded B differs from required A; Evaluation result: noncompliant because recorded B differs from required A → governing response → Governing policy: select the established remediation or escalation path—not proof of an attack

### s02 · explainer · Work through the evidence: Triage recorded configuration evidence
Orders sandbox · explainer — 
(example) For the supplied noncompliant resource, compare recorded configuration, evaluation result and rule parameters. Describe the mismatched setting, retaining any unexpected rule-parameter discrepancy. Preserve that evidence with the governing policy’s remediation or escalation choice; do not infer an attacker or invent an unapproved change. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) Noncompliant describes configuration against desired conditions, not proof of compromise. The governing policy determines the response. ⟦A.f1 A.f3 A:tb5⟧

### s03 · check · Check triage recorded configuration evidence
Orders sandbox · check — Read the supplied evidence in this step and choose the interpretation it supports.

### s04 · hands_on · Review triage recorded configuration evidence
Orders sandbox · hands on — Read the supplied excerpts in this step and decide which are correct, defective or unsafe.

### s05 · recap · Keep these distinctions
Orders sandbox · recap — 
(takeaway) Inspect resource, evaluation and parameters; choose the policy-governed response without treating noncompliance as attack evidence. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Cloudformation drift: Next tile: aws_devops.tile.044.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · One contrast: Triage recorded configuration evidence
(mechanism) Follow the governing policy’s established remediation or escalation path. A compliance result is not proof of an attack. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Noncompliant describes configuration against desired conditions, not proof of compromise. The governing policy determines the response. ⟦A.f1 A.f3 A:tb5⟧
### r02 · One contrast: Triage recorded configuration evidence
(mechanism) AWS Config rules compare recorded resource configuration with desired conditions and report compliance results. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Open the rule’s noncompliant resources. Inspect the affected resource, evaluation result and rule parameters to identify the configuration mismatch. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) Follow the governing policy’s established remediation or escalation path. A compliance result is not proof of an attack. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Noncompliant describes configuration against desired conditions, not proof of compromise. The governing policy determines the response. ⟦A.f1 A.f3 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction

=========

# EVALUATOR PACKET — Observe CloudFormation drift / Read update failure and rollback separately (aws_devops.tile.044)
Tile summary: Inspect the supplied evidence and distinguish what each check establishes.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws.cloudformation_drift — Cloudformation drift
B = aws.cloudformation_rollback — Cloudformation rollback

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws.cloudformation_drift)   objective: Detect CloudFormation S3 drift
A.f1: CloudFormation drift detection compares supported explicitly declared resource properties with their current values.   [sources: aws_cloudformation_user_guide#using-cfn-stack-drift.html]
A.f2: Run drift detection on the provisioned stack after the supplied out-of-band change, wait for completion and inspect the bucket’s expected and actual property values.   [sources: aws_cloudformation_user_guide#using-cfn-stack-drift.html]
A.f3: Drift detection reports differences without repairing them; unsupported or undeclared properties may not be checked.   [sources: aws_cloudformation_user_guide#using-cfn-stack-drift.html]
note: Keep detection distinct from repair; do not extend drift coverage beyond supported declared properties.
PRACTICE ANCHOR (external_proof): Provision one S3 bucket in a sandbox using the supplied CloudFormation template. Apply the supplied out-of-band change to one supported, explicitly declared bucket property, run stack drift detection, wait for completion, and inspect the bucket's expected and actual property values.  SUCCESS: Provide evidence of the provisioned bucket and completed drift detection, identifying the stack resource, checked property, and expected/actual value pair. Explain that detection reports the difference without repairing it and does not establish the correctness of unsupported or undeclared properties.
ASSESSMENT ANCHOR: identify_supported_bucket_property_difference facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_drift_detection_from_repair_and_exhaustive_verification facts=['f3']

## SOURCE FACTS — B (aws.cloudformation_rollback)   objective: Recover a failed CloudFormation EC2 stack update
B.f1: CloudFormation stack events record resource operation status and failure reasons during an update.   [sources: aws_cloudformation_user_guide#using-cfn-updating-stacks-monitor-stack.html]
B.f2: After the supplied controlled update failure, inspect the first failing resource event and subsequent rollback events.   [sources: aws_cloudformation_user_guide#using-cfn-updating-stacks-monitor-stack.html]
B.f3: UPDATE_ROLLBACK_COMPLETE indicates rollback to the previous working stack state; UPDATE_ROLLBACK_FAILED requires resolving the rollback failure before continuing.   [sources: aws_cloudformation_user_guide#using-cfn-updating-stacks-continueupdaterollback.html]
note: Do not invent failure-recovery commands; inspect supplied events and established resolution guidance.
PRACTICE ANCHOR (tool_simulation): Use a supplied CloudFormation stack template to provision one EC2 instance in a prepared sandbox simulation. Apply the supplied controlled update-failure scaffolding, inspect the first failing resource event and its failure reason, and follow subsequent rollback events to determine the final stack state.  SUCCESS: The supplied stack initially provisions one EC2 instance. After the controlled update failure, the learner records the first failing resource event and its reason separately from subsequent rollback events, and verifies that UPDATE_ROLLBACK_COMPLETE indicates return to the previous working stack state. For a supplied UPDATE_ROLLBACK_FAILED event sequence, the learner identifies that the rollback failure requires resolution through established guidance before continuing.
ASSESSMENT ANCHOR: identify_update_failure_from_stack_events facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_rollback_to_previous_working_stack_state facts=['f2', 'f3']
ASSESSMENT ANCHOR: distinguish_completed_rollback_from_rollback_requiring_resolution facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authorize an event target with least-privilege execution permissions; Automate prohibited-configuration checks; Cloudformation rollback; Configure GitHub Actions AWS role federation; Configure a CodeBuild buildspec for a supplied application; Configure a CodeDeploy deployment action for a supplied EC2 application; Configure a budget notification; Configure and verify an EC2 Auto Scaling policy under bounded load; Configure artifact repository access; Configure artifact repository retention; Configure load-balancer listeners, targets and health checks; Configure log retention; Configure managed database backups and create/restore RDS snapshots; require only native RDS and backup foundations, with existing network setup given and no routing or security-group skills assumed; Configure scoped log access; Define an ECS task for a supplied image; Diagnose an IAM denied request from request and policy evidence; Ec2 instance profile; Eks workload identity; Execute a reviewed Terraform plan provisioning EC2; directly require the native EC2 instance foundation; Execute a scoped Systems Manager remote command after external shell preparation; Gate infrastructure changes with configuration val

## LESSON, in learner order

### s01 · explainer · Observe CloudFormation drift
Orders sandbox · explainer — 
(intro) A declared-versus-current difference is evidence within a limited comparison scope. ⟦A:tb1⟧
(definition) Drift detection compares current values with supported resource properties explicitly declared in CloudFormation. ⟦A.f1 A:tb2⟧
(mechanism) After the supplied out-of-band change, run detection on the provisioned stack, wait for completion, and inspect the bucket’s expected/actual property pair. ⟦A.f2 A:tb3⟧
(mechanism) Detection reports differences but does not repair them. Unsupported or undeclared properties may not be checked. ⟦A.f3 A:tb3⟧
[SIDE_BY_SIDE] Compare the expected/actual pair after completed detection. Unsupported or undeclared properties may not be checked. left_label: Declared expectation | right_label: Changed live property
  left:
[DIAGRAM: Expected] nodes=['Bucket: supported explicitly declared property', 'Supplied declared value A'] edges=[('n1', 'n2', 'declares')] alt: Expected: Bucket: supported explicitly declared property; Supplied declared value A
  right:
[DIAGRAM: Actual] nodes=['Same checked bucket property', 'Current value B', 'Detection status: complete', 'Resource drift result: checked declared value A differs from current value B', 'Detection does not repair'] edges=[('n1', 'n2', 'current value'), ('n3', 'n4', 'completed result')] alt: Actual: Same checked bucket property; Current value B; Detection status: complete; Resource drift result: checked declared value A differs from current value B; Detection does not repair. Same checked bucket property → current value → Current value B; Detection status: complete → completed result → Resource drift result: checked declared value A differs from current value B

### s02 · explainer · Work through the evidence: Observe CloudFormation drift
Orders sandbox · explainer — 
(example) Record the checked bucket property as supplied declared value A versus current value B. Wait for completed detection before interpreting the pair. Keep the supported, explicitly declared comparison scope beside it. A missing report for another property does not establish that property’s correctness, and detection alone makes no repair. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) Detection is neither correction nor exhaustive checking of every property. Unsupported or undeclared properties may fall outside the comparison. ⟦A.f1 A.f3 A:tb5⟧

### s03 · check · Check observe CloudFormation drift
Orders sandbox · check — Read the supplied evidence in this step and choose the interpretation it supports.

### s04 · hands_on · Review observe CloudFormation drift
Orders sandbox · hands on — Read the supplied excerpts in this step and decide which are correct, defective or unsafe.

### s05 · explainer · Read update failure and rollback separately
Orders sandbox · explainer — 
(intro) The original update failure and the rollback outcome are separate evidence. ⟦B:tb1⟧
(definition) CloudFormation stack events record resource operation status and failure reasons during updates. ⟦B.f1 B:tb2⟧
(mechanism) For the supplied controlled update failure, inspect the first failing resource event, then the subsequent rollback events. ⟦B.f2 B:tb3⟧
(mechanism) UPDATE_ROLLBACK_COMPLETE means rollback to the previous working stack state. UPDATE_ROLLBACK_FAILED requires resolving the rollback failure before continuing. ⟦B.f3 B:tb3⟧
[DIAGRAM: Two illustrative ordered traces—not execution transcripts.] nodes=['1. Resource update failed—original update failure reason', '2. Subsequent rollback events', '3. Final stack status: UPDATE_ROLLBACK_COMPLETE—previous working state restored', '1. Resource update failed—original update failure reason', '2. Rollback operation failed—separate rollback failure reason', '3. Final stack status: UPDATE_ROLLBACK_FAILED—resolve rollback failure before continuing'] edges=[('n1', 'n2', 'then'), ('n2', 'n3', 'then'), ('n4', 'n5', 'then: separate rollback failure'), ('n5', 'n6', 'then')] alt: Two illustrative ordered traces—not execution transcripts.: 1. Resource update failed—original update failure reason; 2. Subsequent rollback events; 3. Final stack status: UPDATE_ROLLBACK_COMPLETE—previous working state restored; 1. Resource update failed—original update failure reason; 2. Rollback operation failed—separate rollback failure reason; 3. Final stack status: UPDATE_ROLLBACK_FAILED—resolve rollback failure before continuing. 1. Resource update failed—original update failure reason → then → 2. Subsequent rollback events; 2. Subsequent rollback events → then → 3. Final stack status: UPDATE_ROLLBACK_COMPLETE—previous working state restored; 1. Resource update failed—original update failure reason → then: separate rollback failure → 2. Rollback operation failed—separate rollback failure reason; 2. Rollback operation failed—separate rollback failure reason → then → 3. Final stack status: UPDATE_ROLLBACK_FAILED—resolve rollback failure before continuing

### s06 · explainer · Work through the evidence: Read update failure and rollback separately
Orders sandbox · explainer — 
(example) Read the first failing resource and its reason, then follow rollback events. Keep the original failure separate from a later rollback failure. UPDATE_ROLLBACK_COMPLETE describes restoration of the previous working state; UPDATE_ROLLBACK_FAILED leaves a rollback failure to resolve before continuing through the approved response path. ⟦B.f1 B.f2 B.f3 B:tb4⟧
(misconception) UPDATE_ROLLBACK_FAILED is not rollback success. UPDATE_ROLLBACK_COMPLETE is not successful deployment of the failed update. ⟦B.f3 B:tb5⟧

### s07 · check · Check read update failure and rollback separately
Orders sandbox · check — Read the supplied evidence in this step and choose the interpretation it supports.

### s08 · hands_on · Review read update failure and rollback separately
Orders sandbox · hands on — Read the supplied excerpts in this step and decide which are correct, defective or unsafe.

### s09 · recap · Keep these distinctions
Orders sandbox · recap — 
(takeaway) Drift detection reports supported declared-property differences; it neither repairs them nor promises to check every property. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Keep the first update failure and rollback outcome distinct; resolve rollback failure before continuing. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Up next: Ec2 instance profile: Next tile: aws_devops.tile.046.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · One contrast: Observe CloudFormation drift
(mechanism) Detection reports differences but does not repair them. Unsupported or undeclared properties may not be checked. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Detection is neither correction nor exhaustive checking of every property. Unsupported or undeclared properties may fall outside the comparison. ⟦A.f1 A.f3 A:tb5⟧
### r02 · One contrast: Observe CloudFormation drift
(mechanism) Drift detection compares current values with supported resource properties explicitly declared in CloudFormation. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) After the supplied out-of-band change, run detection on the provisioned stack, wait for completion, and inspect the bucket’s expected/actual property pair. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) Detection reports differences but does not repair them. Unsupported or undeclared properties may not be checked. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Detection is neither correction nor exhaustive checking of every property. Unsupported or undeclared properties may fall outside the comparison. ⟦A.f1 A.f3 A:tb5⟧
### r03 · One contrast: Read update failure and rollback separately
(mechanism) UPDATE_ROLLBACK_COMPLETE means rollback to the previous working stack state. UPDATE_ROLLBACK_FAILED requires resolving the rollback failure before continuing. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) UPDATE_ROLLBACK_FAILED is not rollback success. UPDATE_ROLLBACK_COMPLETE is not successful deployment of the failed update. ⟦B.f3 B:tb5⟧
### r04 · One contrast: Read update failure and rollback separately
(mechanism) CloudFormation stack events record resource operation status and failure reasons during updates. ⟦B.f1 B:tb2 B:tb4⟧
(mechanism) For the supplied controlled update failure, inspect the first failing resource event, then the subsequent rollback events. ⟦B.f2 B:tb3 B:tb4⟧
(mechanism) UPDATE_ROLLBACK_COMPLETE means rollback to the previous working stack state. UPDATE_ROLLBACK_FAILED requires resolving the rollback failure before continuing. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) UPDATE_ROLLBACK_FAILED is not rollback success. UPDATE_ROLLBACK_COMPLETE is not successful deployment of the failed update. ⟦B.f3 B:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction

=========

# EVALUATOR PACKET — Pass an approved role to EC2 / Scope EKS Pod Identity to the workload / Review workflow federation trust / Inspect a bounded STS session (aws_devops.tile.046)
Tile summary: Inspect the supplied evidence and distinguish what each check establishes.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws.ec2_instance_profile — Ec2 instance profile
B = aws.eks_workload_identity — Eks workload identity
C = aws.pipeline_federation — Configure GitHub Actions AWS role federation
D = aws.sts_session — Sts session

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws.ec2_instance_profile)   objective: Configure EC2 instance-profile identity
A.f1: An instance profile contains one IAM role and provides a way to pass that role to EC2.   [sources: aws_iam_user_guide#id_roles_use_switch-role-ec2_instance-profiles.html]
A.f2: Attach or replace the approved instance profile on the EC2 instance using the instance’s IAM-role setting or associate-iam-instance-profile.   [sources: aws_ec2_user_guide#attach-iam-role.html]
A.f3: Use the instance’s role credential provider rather than embedded keys, inspect the caller identity and test one allowed and one denied operation under the assigned role’s permissions.   [sources: aws_ec2_user_guide#iam-roles-for-amazon-ec2.html]
note: Use the approved role and supplied test operations; do not design unrelated policies.
PRACTICE ANCHOR (tool_simulation): Attach the supplied least-privilege instance profile to the sandbox EC2 instance using its IAM-role setting or the supplied associate-iam-instance-profile operation. From the instance, use the role credential provider, inspect caller identity, and run the supplied allowed and denied operations without changing the role’s permissions.  SUCCESS: The instance has the approved profile containing one role. Caller identity matches the assigned role, with no embedded keys used. The supplied allowed operation succeeds and the supplied denied operation is rejected; both outcomes are recorded with the assigned role context.
ASSESSMENT ANCHOR: verify_assigned_instance_profile_and_role facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_role_identity_and_bounded_permissions facts=['f3']

## SOURCE FACTS — B (aws.eks_workload_identity)   objective: Configure EKS workload identity
B.f1: EKS Pod Identity associates a Kubernetes service account in a namespace and cluster with an IAM role for application AWS access.   [sources: aws_eks_user_guide#pod-identities.html]
B.f2: Create an association for the supplied cluster, namespace, service account and approved role; run the workload with that serviceAccountName.   [sources: aws_eks_user_guide#pod-id-association.html]
B.f3: The Pod Identity agent and supported SDK credential chain supply temporary role credentials to associated Pods; verify allowed access from the intended workload and rejection from an unassociated workload.   [sources: aws_eks_user_guide#pod-identities.html]
note: Use supplied agent/access setup; do not introduce a different workload-identity mechanism.
PRACTICE ANCHOR (tool_simulation): Using the supplied agent and cluster-access setup, create a Pod Identity association for the supplied cluster, namespace, service account and approved IAM role. Run the supplied workload with that serviceAccountName and perform the supplied AWS access checks from both the intended and unassociated workloads.  SUCCESS: The association matches the supplied cluster, namespace, service account and approved role; the intended workload uses that serviceAccountName. With the supplied Pod Identity agent and supported SDK credential chain, the intended workload's approved AWS operation succeeds and the unassociated workload's attempt is rejected. Each result is recorded beside its workload identity and association scope.
ASSESSMENT ANCHOR: verify_association_scope_and_workload_service_account facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_intended_workload_access_and_unassociated_workload_rejection facts=['f3']

## SOURCE FACTS — C (aws.pipeline_federation)   objective: Configure GitHub Actions OIDC federation to an AWS role
C.f1: GitHub Actions OIDC enables a workflow to obtain temporary AWS role credentials without storing AWS access keys.   [sources: github_actions_docs#how-tos/secure-your-work/security-harden-deployments/oidc-in-aws]
C.f2: Configure the GitHub token issuer as an IAM OIDC provider and constrain the role trust policy’s aud and sub claims to the approved audience and repository/branch or environment.   [sources: github_actions_docs#how-tos/secure-your-work/security-harden-deployments/oidc-in-aws]
C.f3: Give the workflow id-token: write permission and configure the AWS credential action to assume the approved role; test that an unapproved repository or branch cannot assume it.   [sources: github_actions_docs#how-tos/secure-your-work/security-harden-deployments/oidc-in-aws]
note: Keep this GitHub OIDC mechanism separate from CodePipeline service-role trust.
PRACTICE ANCHOR (tool_simulation): Using the supplied GitHub workflow and sandbox role, configure the GitHub IAM OIDC provider, restrict aud and sub to the approved audience and repository/branch, grant id-token: write permission, and configure the AWS credentials action to obtain temporary role credentials without stored AWS keys.  SUCCESS: The approved workflow obtains temporary credentials for the intended role without stored AWS keys. The supplied unapproved repository or branch case cannot assume that role, and the configured audience condition separately matches only the approved audience.
ASSESSMENT ANCHOR: allow_approved_workflow_and_reject_unapproved_repository_or_branch facts=['f2', 'f3']

## SOURCE FACTS — D (aws.sts_session)   objective: Obtain and inspect an STS session
D.f1: Temporary AWS credentials consist of an access key ID, secret access key and session token and expire after their issued lifetime.   [sources: aws_iam_user_guide#id_credentials_temp_use-resources.html]
D.f2: Call aws sts assume-role with --role-arn, --role-session-name and the approved --duration-seconds, then use all three returned credential fields and inspect Expiration.   [sources: aws_iam_user_guide#id_credentials_temp_request.html]
D.f3: Permissions granted through a role’s identity-based policies are intersected with any session policies; resource-based grants are evaluated separately, and grants directly to the session ARN are not limited by session policies; an explicit deny in any applicable policy overrides an allow.   [sources: aws_iam_user_guide#access_policies.html#policies_session]
note: Do not expose credential values; preserve direct-session-ARN and explicit-deny qualifications.
PRACTICE ANCHOR (tool_simulation): Assume one trusted sandbox role using aws sts assume-role with the supplied approved --role-arn, --role-session-name and --duration-seconds. Inspect the returned credential field names and Expiration, then configure the session using all three credential fields without displaying their values.  SUCCESS: The request matches the approved role, session name and duration. All three returned credential fields are used, their values remain concealed, and the recorded Expiration and issued lifetime match the approved duration. Using supplied permission evidence, distinguish role identity-policy grants intersected with any session policy from separately evaluated resource-based grants, preserve the direct-session-ARN exception, and apply any applicable explicit deny.
ASSESSMENT ANCHOR: verify_session_credential_completeness_and_approved_expiry facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_session_permissions_against_supplied_policy_evidence facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authorize an event target with least-privilege execution permissions; Automate prohibited-configuration checks; Configure GitHub Actions AWS role federation; Configure a CodeBuild buildspec for a supplied application; Configure a CodeDeploy deployment action for a supplied EC2 application; Configure a budget notification; Configure and verify an EC2 Auto Scaling policy under bounded load; Configure artifact repository access; Configure artifact repository retention; Configure load-balancer listeners, targets and health checks; Configure log retention; Configure managed database backups and create/restore RDS snapshots; require only native RDS and backup foundations, with existing network setup given and no routing or security-group skills assumed; Configure scoped log access; Define an ECS task for a supplied image; Diagnose an IAM denied request from request and policy evidence; Eks workload identity; Execute a reviewed Terraform plan provisioning EC2; directly require the native EC2 instance foundation; Execute a scoped Systems Manager remote command after external shell preparation; Gate infrastructure changes with configuration validation after external declarative/configuratio

## LESSON, in learner order

### s01 · explainer · Pass an approved role to EC2
Orders sandbox · explainer — 
(intro) Profile attachment and application permission evidence are separate checks. ⟦A:tb1⟧
(definition) An instance profile holds one IAM role and is the mechanism for passing that role to EC2. ⟦A.f1 A:tb2⟧
(mechanism) Attach the approved profile with associate-iam-instance-profile when no association exists. Replace an existing profile through the console’s Modify IAM role workflow. ⟦A.f2 A:tb3⟧
(mechanism) Use the instance role credential provider, not embedded keys. Inspect caller identity and test one allowed and one denied operation under the assigned role’s permissions. ⟦A.f3 A:tb3⟧
[DIAGRAM: Illustrative permission-test evidence—not an execution transcript.] nodes=['Approved instance profile: contains one IAM role', 'Caller-identity result: assigned role', 'Supplied allowed operation: allowed', 'Supplied denied operation: denied'] edges=[('n1', 'n2', 'instance role credential provider, not embedded keys'), ('n2', 'n3', 'same assigned-role identity'), ('n2', 'n4', 'same assigned-role identity')] alt: Illustrative permission-test evidence—not an execution transcript.: Approved instance profile: contains one IAM role; Caller-identity result: assigned role; Supplied allowed operation: allowed; Supplied denied operation: denied. Approved instance profile: contains one IAM role → instance role credential provider, not embedded keys → Caller-identity result: assigned role; Caller-identity result: assigned role → same assigned-role identity → Supplied allowed operation: allowed; Caller-identity result: assigned role → same assigned-role identity → Supplied denied operation: denied

### s02 · explainer · Work through the evidence: Pass an approved role to EC2
Orders sandbox · explainer — 
(example) Review whether this is a new association or a profile replacement, selecting the supplied association operation or Modify IAM role workflow accordingly. From the instance, inspect caller identity under the role credential provider and retain the supplied allowed/denied operation outcomes with the assigned role context. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) An attached profile does not prove the application’s intended access. It passes one role, not embedded access keys. ⟦A.f1 A.f3 A:tb5⟧

### s03 · video · A closer look: Pass an approved role to EC2
Orders sandbox · video — 
[VIDEO ] bridge-before:  | bridge-after: 

### s04 · check · Check pass an approved role to EC2
Orders sandbox · check — Read the supplied evidence in this step and choose the interpretation it supports.

### s05 · hands_on · Review pass an approved role to EC2
Orders sandbox · hands on — Read the supplied excerpts in this step and decide which are correct, defective or unsafe.

### s06 · explainer · Scope EKS Pod Identity to the workload
Orders sandbox · explainer — 
(intro) The association belongs to a specific workload identity context. ⟦B:tb1⟧
(definition) EKS Pod Identity links an IAM role for application AWS access to a Kubernetes service account within a namespace and cluster. ⟦B.f1 B:tb2⟧
(mechanism) Create the association with the supplied cluster, namespace, service account and approved role. The workload must use that serviceAccountName. ⟦B.f2 B:tb3⟧
(mechanism) The Pod Identity agent and supported SDK credential chain deliver temporary role credentials to associated Pods. Verify intended-workload allowed access and unassociated-workload rejection. ⟦B.f3 B:tb3⟧
(example) Review the association’s cluster, namespace, service account and role beside the workload’s serviceAccountName. Keep the Pod Identity agent and supported SDK credential-chain qualification in the credential explanation. Compare intended-workload allowed access with the supplied unassociated-workload rejection; one Pod’s access is not another’s evidence. ⟦B.f1 B.f2 B.f3 B:tb4⟧
(misconception) A role’s existence is not the association. The serviceAccountName must match the scoped association, with the stated agent and SDK support. ⟦B.f2 B.f3 B:tb5⟧
[DIAGRAM: Scope EKS Pod Identity to the workload] nodes=['Supplied cluster', 'Supplied namespace', 'Supplied service account', 'Approved IAM role', 'Association', 'Intended workload: serviceAccountName matches the cluster/namespace/service-account association', 'Pod Identity agent + supported SDK credential chain', 'Temporary role credentials', 'Supplied allowed-access result: success', 'Unassociated workload', 'Supplied access result: rejected'] edges=[('n1', 'n5', 'cluster scope'), ('n2', 'n5', 'namespace scope'), ('n3', 'n5', 'service account'), ('n4', 'n5', 'role'), ('n5', 'n6', 'must match'), ('n7', 'n8', 'supplies to associated Pods'), ('n6', 'n9', 'intended workload'), ('n10', 'n11', 'unassociated workload'), ('n8', 'n6', 'temporary role credentials to associated Pod')] alt: Scope EKS Pod Identity to the workload: Supplied cluster; Supplied namespace; Supplied service account; Approved IAM role; Association; Intended workload: serviceAccountName matches the cluster/namespace/service-account association; Pod Identity agent + supported SDK credential chain; Temporary role credentials; Supplied allowed-access result: success; Unassociated workload; Supplied access result: rejected. Supplied cluster → cluster scope → Association; Supplied namespace → namespace scope → Association; Supplied service account → service account → Association; Approved IAM role → role → Association; Association → must match → Intended workload: serviceAccountName matches the cluster/namespace/service-account association; Pod Identity agent + supported SDK credential chain → supplies to associated Pods → Temporary role credentials; Intended workload: serviceAccountName matches the cluster/namespace/service-account association → intended workload → Supplied allowed-access result: success; Unassociated workload → unassociated workload → Supplied access result: rejected; Temporary role credentials → temporary role credentials to associated Pod → Intended workload: serviceAccountName matches the cluster/namespace/service-account association

### s07 · check · Check scope EKS Pod Identity to the workload
Orders sandbox · check — Read the supplied evidence in this step and choose the interpretation it supports.

### s08 · hands_on · Review scope EKS Pod Identity to the workload
Orders sandbox · hands on — Read the supplied excerpts in this step and decide which are correct, defective or unsafe.

### s09 · explainer · Review workflow federation trust
Orders sandbox · explainer — 
(intro) Temporary credentials still require an approved token-context trust boundary. ⟦C:tb1⟧
(definition) GitHub Actions OIDC lets a workflow obtain temporary AWS role credentials without storing AWS access keys. ⟦C.f1 C:tb2⟧
(mechanism) Configure the GitHub token issuer as an IAM OIDC provider. Restrict role-trust aud and sub to the approved audience and repository/branch or environment. ⟦C.f2 C:tb3⟧
(mechanism) Grant workflow id-token: write and configure the AWS credential action for the approved role. Test that an unapproved repository or branch cannot assume it. ⟦C.f3 C:tb3⟧
[SIDE_BY_SIDE] Review the issuer and both aud/sub restrictions alongside the credential action’s approved role. Token permission alone does not establish role trust. left_label: Provider and role trust | right_label: Workflow and boundary tests
  left:
[DIAGRAM: Trust context] nodes=['GitHub token issuer', 'IAM OIDC provider', 'aud: approved audience', 'sub: approved repository/branch or environment'] edges=[('n1', 'n2', 'configure issuer as provider'), ('n2', 'n3', 'aud restriction'), ('n2', 'n4', 'sub restriction')] alt: Trust context: GitHub token issuer; IAM OIDC provider; aud: approved audience; sub: approved repository/branch or environment
  right:
[DIAGRAM: Workflow review] nodes=['Workflow id-token: write', 'AWS credential action: approved role', 'Approved token context: expect success', 'Unapproved repository/branch: expect rejection'] edges=[('n1', 'n2', 'configure workflow'), ('n2', 'n3', 'approved case'), ('n2', 'n4', 'negative case')] alt: Workflow review: Workflow id-token: write; AWS credential action: approved role; Approved token context: expect success; Unapproved repository/branch: expect rejection

### s10 · explainer · Work through the evidence: Review workflow federation trust
Orders sandbox · explainer — 
(example) Compare the supplied issuer, aud and sub restrictions with the approved context. Review id-token: write and the AWS credential action’s role target. Keep the approved success and supplied unapproved repository/branch rejection together. Check the audience separately; a matching subject alone is not every trust test. ⟦C.f1 C.f2 C.f3 C:tb4⟧
(misconception) No stored keys does not mean unrestricted trust is acceptable. Workflow token permission alone does not establish the AWS role’s intended trust boundary. ⟦C.f2 C.f3 C:tb5⟧

### s11 · video · A closer look: Review workflow federation trust
Orders sandbox · video — 
[VIDEO ] bridge-before:  | bridge-after: 

### s12 · check · Check review workflow federation trust
Orders sandbox · check — Read the supplied evidence in this step and choose the interpretation it supports.

### s13 · hands_on · Review workflow federation trust
Orders sandbox · hands on — Read the supplied excerpts in this step and decide which are correct, defective or unsafe.

### s14 · explainer · Inspect a bounded STS session
Orders sandbox · explainer — 
(intro) Keep credential composition, lifetime and grant distinctions visible. ⟦D:tb1⟧
(definition) Temporary AWS credentials have three parts: access key ID, secret access key and session token. They expire after their issued lifetime. ⟦D.f1 D:tb2⟧
(mechanism) Use aws sts assume-role with --role-arn, --role-session-name and the approved --duration-seconds. Use all three returned credential fields and inspect Expiration. ⟦D.f2 D:tb3⟧
(mechanism) Role identity-based grants intersect with any session policies. Resource-based grants are evaluated separately; grants directly to the session ARN are not limited by session policies. An applicable explicit deny overrides an allow. ⟦D.f3 D:tb3⟧
[DIAGRAM: Inspect a bounded STS session] nodes=['aws sts assume-role', 'Approved role / session name / duration', 'access key ID', 'secret access key', 'session token', 'Expiration', 'Role grants intersect session policies', 'Resource grants evaluated separately', 'Direct session-ARN grants: not session-policy limited', 'Applicable explicit deny overrides allow'] edges=[('n1', 'n2', 'bounded request'), ('n2', 'n3', 'returned field'), ('n2', 'n4', 'returned field'), ('n2', 'n5', 'returned field'), ('n2', 'n6', 'issued lifetime ends')] alt: Inspect a bounded STS session: aws sts assume-role; Approved role / session name / duration; access key ID; secret access key; session token; Expiration; Role grants intersect session policies; Resource grants evaluated separately; Direct session-ARN grants: not session-policy limited; Applicable explicit deny overrides allow

### s15 · explainer · Work through the evidence: Inspect a bounded STS session
Orders sandbox · explainer — 
(example) Review the approved role, session name and duration beside Expiration and the three credential-field names, without displaying values. Apply session-policy intersection to role identity-based grants, not every resource-based grant. Direct session-ARN grants are not limited by session policies; an applicable explicit deny still overrides allow. ⟦D.f1 D.f2 D.f3 D:tb4⟧
(misconception) An access-key pair alone omits the session token. Session-policy intersection is not an unqualified limit on every resource-based grant. ⟦D.f1 D.f3 D:tb5⟧

### s16 · check · Check inspect a bounded STS session
Orders sandbox · check — Read the supplied evidence in this step and choose the interpretation it supports.

### s17 · hands_on · Review inspect a bounded STS session
Orders sandbox · hands on — Read the supplied excerpts in this step and decide which are correct, defective or unsafe.

### s18 · recap · Keep these distinctions
Orders sandbox · recap — 
(takeaway) Pass one approved role through the profile; inspect caller identity and role-provider allowed/denied operation evidence. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Tie the association to cluster, namespace and service account; compare associated and unassociated workload access. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
(takeaway) Constrain issuer, aud and sub; retain approved success and unapproved-context rejection evidence. ⟦C.f1 C.f2 C.f3 C:tb2 C:tb3 C:tb4 C:tb5⟧
(takeaway) Use all three temporary credential fields and inspect expiry; preserve the role/session/resource grant distinctions and explicit-deny override. ⟦D.f1 D.f2 D.f3 D:tb2 D:tb3 D:tb4 D:tb5⟧
[UP NEXT] Up next: Authorize an event target with least-privilege execution permissions: Next tile: aws_devops.tile.050.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · One contrast: Pass an approved role to EC2
(mechanism) Use the instance role credential provider, not embedded keys. Inspect caller identity and test one allowed and one denied operation under the assigned role’s permissions. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) An attached profile does not prove the application’s intended access. It passes one role, not embedded access keys. ⟦A.f1 A.f3 A:tb5⟧
### r02 · One contrast: Pass an approved role to EC2
(mechanism) An instance profile holds one IAM role and is the mechanism for passing that role to EC2. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Attach the approved profile with associate-iam-instance-profile when no association exists. Replace an existing profile through the console’s Modify IAM role workflow. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) Use the instance role credential provider, not embedded keys. Inspect caller identity and test one allowed and one denied operation under the assigned role’s permissions. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) An attached profile does not prove the application’s intended access. It passes one role, not embedded access keys. ⟦A.f1 A.f3 A:tb5⟧
### r03 · One contrast: Scope EKS Pod Identity to the workload
(mechanism) The Pod Identity agent and supported SDK credential chain deliver temporary role credentials to associated Pods. Verify intended-workload allowed access and unassociated-workload rejection. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) A role’s existence is not the association. The serviceAccountName must match the scoped association, with the stated agent and SDK support. ⟦B.f2 B.f3 B:tb5⟧
### r04 · One contrast: Scope EKS Pod Identity to the workload
(mechanism) EKS Pod Identity links an IAM role for application AWS access to a Kubernetes service account within a namespace and cluster. ⟦B.f1 B:tb2 B:tb4⟧
(mechanism) Create the association with the supplied cluster, namespace, service account and approved role. The workload must use that serviceAccountName. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(mechanism) The Pod Identity agent and supported SDK credential chain deliver temporary role credentials to associated Pods. Verify intended-workload allowed access and unassociated-workload rejection. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) A role’s existence is not the association. The serviceAccountName must match the scoped association, with the stated agent and SDK support. ⟦B.f2 B.f3 B:tb5⟧
### r05 · One contrast: Review workflow federation trust
(mechanism) Configure the GitHub token issuer as an IAM OIDC provider. Restrict role-trust aud and sub to the approved audience and repository/branch or environment. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
(mechanism) Grant workflow id-token: write and configure the AWS credential action for the approved role. Test that an unapproved repository or branch cannot assume it. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
(misconception) No stored keys does not mean unrestricted trust is acceptable. Workflow token permission alone does not establish the AWS role’s intended trust boundary. ⟦C.f2 C.f3 C:tb5⟧
### r06 · One contrast: Review workflow federation trust
(mechanism) GitHub Actions OIDC lets a workflow obtain temporary AWS role credentials without storing AWS access keys. ⟦C.f1 C:tb2 C:tb4⟧
(mechanism) Configure the GitHub token issuer as an IAM OIDC provider. Restrict role-trust aud and sub to the approved audience and repository/branch or environment. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
(mechanism) Grant workflow id-token: write and configure the AWS credential action for the approved role. Test that an unapproved repository or branch cannot assume it. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
(misconception) No stored keys does not mean unrestricted trust is acceptable. Workflow token permission alone does not establish the AWS role’s intended trust boundary. ⟦C.f2 C.f3 C:tb5⟧
### r07 · One contrast: Inspect a bounded STS session
(mechanism) Role identity-based grants intersect with any session policies. Resource-based grants are evaluated separately; grants directly to the session ARN are not limited by session policies. An applicable explicit deny overrides an allow. ⟦D.f3 D:tb3 D:tb4 D:tb5⟧
(misconception) An access-key pair alone omits the session token. Session-policy intersection is not an unqualified limit on every resource-based grant. ⟦D.f1 D.f3 D:tb5⟧
### r08 · One contrast: Inspect a bounded STS session
(mechanism) Temporary AWS credentials have three parts: access key ID, secret access key and session token. They expire after their issued lifetime. ⟦D.f1 D:tb2 D:tb4 D:tb5⟧
(mechanism) Use aws sts assume-role with --role-arn, --role-session-name and the approved --duration-seconds. Use all three returned credential fields and inspect Expiration. ⟦D.f2 D:tb3 D:tb4⟧
(mechanism) Role identity-based grants intersect with any session policies. Resource-based grants are evaluated separately; grants directly to the session ARN are not limited by session policies. An applicable explicit deny overrides an allow. ⟦D.f3 D:tb3 D:tb4 D:tb5⟧
(misconception) An access-key pair alone omits the session token. Session-policy intersection is not an unqualified limit on every resource-based grant. ⟦D.f1 D.f3 D:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction

=========

# EVALUATOR PACKET — Separate event matching from execution authority (aws_devops.tile.050)
Tile summary: Inspect the supplied evidence and distinguish what each check establishes.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.authorize_an_event_target_with_least_privilege_execution_permissions — Authorize an event target with least-privilege execution permissions

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.authorize_an_event_target_with_least_privilege_execution_permissions)   objective: Authorize an event target execution role
A.f1: EventBridge target execution authority is separate from the event pattern that selects events.   [sources: aws_eventbridge_user_guide#eb-events-iam-roles.html]
A.f2: For targets requiring an execution role, grant events.amazonaws.com permission to assume the role and attach permissions scoped to the approved target operation and resource.   [sources: aws_eventbridge_user_guide#eb-events-iam-roles.html]
A.f3: Targets such as SNS and Lambda use resource-based permissions for invocation; use the target’s required authorization model rather than assuming every target uses a role.   [sources: aws_eventbridge_user_guide#eb-use-resource-based.html]
note: Use supplied targets and least-privilege permissions; do not invent target operations.
PRACTICE ANCHOR (tool_simulation): Configure authorization for a supplied EventBridge target using its stated permission model, approved action, and resource. For a role-based target, configure EventBridge trust and scoped role permissions; for an SNS or Lambda target, configure the supplied resource-based invocation permission.  SUCCESS: The authorization record uses the target's required model and permits only the supplied bounded action on the supplied resource. A role-based target includes trust for events.amazonaws.com and scoped operation permissions; an SNS or Lambda target uses resource-based invocation permission. The event pattern remains unchanged.
ASSESSMENT ANCHOR: distinguish_event_matching_from_target_authorization facts=['f1']
ASSESSMENT ANCHOR: identify_required_role_trust_and_scoped_target_permissions facts=['f2']
ASSESSMENT ANCHOR: select_the_required_target_authorization_model facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Audit storage access; Automate prohibited-configuration checks; Configure a CodeBuild buildspec for a supplied application; Configure a CodeDeploy deployment action for a supplied EC2 application; Configure a budget notification; Configure and verify an EC2 Auto Scaling policy under bounded load; Configure artifact repository access; Configure artifact repository retention; Configure load-balancer listeners, targets and health checks; Configure log retention; Configure managed database backups and create/restore RDS snapshots; require only native RDS and backup foundations, with existing network setup given and no routing or security-group skills assumed; Configure scoped log access; Define an ECS task for a supplied image; Diagnose an IAM denied request from request and policy evidence; Execute a reviewed Terraform plan provisioning EC2; directly require the native EC2 instance foundation; Execute a scoped Systems Manager remote command after external shell preparation; Gate infrastructure changes with configuration validation after external declarative/configuration preparation; Handle AWS automation errors with bounded retries and useful reporting; AWS SDK call is a supplied rea

## LESSON, in learner order

### s01 · explainer · Separate event matching from execution authority
Orders sandbox · explainer — 
(intro) A matching event does not itself authorize the target operation. ⟦A:tb1⟧
(definition) An EventBridge pattern selects events; target execution authority is a separate requirement. ⟦A.f1 A:tb2⟧
(mechanism) When the target requires an execution role, permit events.amazonaws.com to assume it. Scope role permissions to the approved target operation and resource. ⟦A.f2 A:tb3⟧
(mechanism) Targets such as SNS and Lambda require resource-based invocation permissions. Select the target’s required authorization model rather than assigning a role to every target. ⟦A.f3 A:tb3⟧
[DIAGRAM: Separate event matching from execution authority] nodes=['Event pattern: selection only', 'Target requires execution role', 'events.amazonaws.com may assume role', 'Permissions: approved operation and resource', 'SNS / Lambda target', 'Resource-based invocation permission'] edges=[('n2', 'n3', 'required trust'), ('n3', 'n4', 'scoped role permissions'), ('n5', 'n6', 'different authorization model')] alt: Separate event matching from execution authority: Event pattern: selection only; Target requires execution role; events.amazonaws.com may assume role; Permissions: approved operation and resource; SNS / Lambda target; Resource-based invocation permission

### s02 · explainer · Work through the evidence: Separate event matching from execution authority
Orders sandbox · explainer — 
(example) For a role-requiring target, inspect both events.amazonaws.com trust and approved operation/resource permissions. For the supplied SNS or Lambda case, inspect resource-based invocation permission instead. The same selection pattern does not make these authorization records interchangeable; retain the target and its required model together. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) Matching and authority are separate. A role used by one target is not the model for every target, including SNS and Lambda. ⟦A.f1 A.f3 A:tb5⟧

### s03 · check · Check separate event matching from execution authority
Orders sandbox · check — Read the supplied evidence in this step and choose the interpretation it supports.

### s04 · hands_on · Review separate event matching from execution authority
Orders sandbox · hands on — Read the supplied excerpts in this step and decide which are correct, defective or unsafe.

### s05 · recap · Keep these distinctions
Orders sandbox · recap — 
(takeaway) Match events separately from authority; review role trust/scoped permissions or resource-based invocation according to the target. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Automate prohibited-configuration checks: Next tile: aws_devops.tile.051.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · One contrast: Separate event matching from execution authority
(mechanism) Targets such as SNS and Lambda require resource-based invocation permissions. Select the target’s required authorization model rather than assigning a role to every target. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Matching and authority are separate. A role used by one target is not the model for every target, including SNS and Lambda. ⟦A.f1 A.f3 A:tb5⟧
### r02 · One contrast: Separate event matching from execution authority
(mechanism) An EventBridge pattern selects events; target execution authority is a separate requirement. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) When the target requires an execution role, permit events.amazonaws.com to assume it. Scope role permissions to the approved target operation and resource. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) Targets such as SNS and Lambda require resource-based invocation permissions. Select the target’s required authorization model rather than assigning a role to every target. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Matching and authority are separate. A role used by one target is not the model for every target, including SNS and Lambda. ⟦A.f1 A.f3 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Review the distinction
· remediation_steps.eyebrow: Review the distinction