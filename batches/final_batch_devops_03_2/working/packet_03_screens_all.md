# EVALUATOR PACKET — Automate prohibited-configuration checks (aws_devops.tile.051)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.automate_prohibited_configuration_checks — Automate prohibited-configuration checks

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.automate_prohibited_configuration_checks)   objective: Automate a prohibited-configuration check
A.f1: A Config managed rule evaluates supported resource configuration against the rule’s criteria and configured parameters.   [sources: aws_config_developer_guide#evaluate-config_use-managed-rules.html]
A.f2: Choose the supplied rule, resource scope and parameters, run or inspect its evaluation, and compare compliant and noncompliant sample resources.   [sources: aws_config_developer_guide#evaluate-config_use-managed-rules.html]
A.f3: Read each evaluation’s resource ID and compliance result rather than treating the presence of the rule as proof that all resources passed.   [sources: aws_config_developer_guide#evaluate-config_view-compliance.html]
note: Do not add remediation behavior to a detection-only rule task.
PRACTICE ANCHOR (tool_simulation): Run the supplied Config managed rule in a prepared sandbox using the approved resource scope and parameters, then inspect evaluations for the supplied compliant and noncompliant sample resources.  SUCCESS: The selected rule, scope and parameters match the supplied requirement. Each sample's resource ID and compliance result are recorded: the compliant sample passes and the noncompliant sample is flagged. Rule presence alone is not accepted as evidence of compliance, and no remediation is performed.
ASSESSMENT ANCHOR: select_rule_scope_and_parameters_for_supplied_criteria facts=['f1', 'f2']
ASSESSMENT ANCHOR: detect_noncompliant_configuration_without_false_positives facts=['f2', 'f3']
ASSESSMENT ANCHOR: verify_compliance_from_individual_resource_evaluations facts=['f3']

## DATA ASSETS USED
ds.config_evaluations: Supplied configuration evaluation evidence — columns: resource_id(identifier), selected_rule(identifier), resource_scope(categorical), parameters(text), sample_configuration(categorical), compliance_result(categorical)
   ["sample-acceptable","supplied Config managed rule","approved sandbox resource scope","supplied approved parameters","supplied compliant sample","COMPLIANT"]
   ["sample-prohibited","supplied Config managed rule","approved sandbox resource scope","supplied approved parameters","supplied noncompliant sample","NON_COMPLIANT"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Audit KMS-backed audit-storage encryption (SSE-KMS): verify encryption and KMS key-use authority; key-use authority is required for SSE-KMS, not SSE-S3; Audit storage access; Configure a CodeBuild buildspec for a supplied application; Configure a CodeDeploy deployment action for a supplied EC2 application; Configure a budget notification; Configure and verify an EC2 Auto Scaling policy under bounded load; Configure artifact repository access; Configure artifact repository retention; Configure load-balancer listeners, targets and health checks; Configure log retention; Configure managed database backups and create/restore RDS snapshots; require only native RDS and backup foundations, with existing network setup given and no routing or security-group skills assumed; Configure scoped log access; Define an ECS task for a supplied image; Diagnose an IAM denied request from request and policy evidence; Execute a reviewed Terraform plan provisioning EC2; directly require the native EC2 instance foundation; Execute a scoped Systems Manager remote command after external shell preparation; Gate infrastructure changes with configuration validation after external declarative/configuration prep

## LESSON, in learner order

### s01 · explainer · Rule presence is not a passing result
(mechanism) A Config managed rule evaluates supported resource configuration against its criteria and configured parameters. Its presence is setup evidence, not proof that every resource passed. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) Choose the supplied rule, resource scope and parameters. Run or inspect its evaluation, comparing compliant and noncompliant samples. Read each resource ID and compliance result. ⟦A.f2 A.f3 A:tb3⟧
[DIAGRAM: Supplied settings and evidence] nodes=['Rule settings {selected rule: supplied Config managed rule; resource scope: approved sandbox resource scope; parameters: supplied approved parameters}', 'sample-acceptable {resource id: sample-acceptable; compliance result: COMPLIANT}', 'sample-prohibited {resource id: sample-prohibited; compliance result: NON_COMPLIANT}'] edges=[] alt: Read-only schematic of the supplied settings. Rule settings; selected rule: supplied Config managed rule; resource scope: approved sandbox resource scope; parameters: supplied approved parameters. sample-acceptable; resource id: sample-acceptable; compliance result: COMPLIANT. sample-prohibited; resource id: sample-prohibited; compliance result: NON_COMPLIANT

### s02 · explainer · Check both sides of the boundary
(example) For the supplied rule, compare the approved scope and parameters with the requirement, then inspect both sample evaluations. Tie each resource ID and compliance result to the rule criteria. The acceptable sample should pass; the prohibited sample should be flagged. A sample outside the configured scope cannot validate the intended in-scope criterion. ⟦A.f1 A.f2 A.f3 A:tb4⟧
[TABLE ds.config_evaluations cols=['resource_id', 'selected_rule', 'resource_scope', 'parameters', 'sample_configuration', 'compliance_result'] ] caption: 
(misconception) If the prohibited sample is reported as compliant, inspect scope and parameters against the supplied requirement rather than accepting rule presence as success. Individual results matter. This detection check does not install remediation, and a compliance report does not establish malicious activity. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · check · Check the individual evidence
 — Read the supplied evidence and choose the interpretation that matches the approved settings and individual results.

### s04 · hands_on · Review the configuration evidence
 — Read the supplied excerpts in this step and decide which correctly select the rule, scope and parameters and verify the individual sample results.

### s05 · recap · Takeaways
(takeaway) The rule evaluates supported configuration against its criteria and parameters. Select the supplied rule, scope and parameters, then run or inspect evaluations for both sample configurations. Read individual resource IDs and compliance results: rule presence alone does not mean all resources passed. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Configure a budget notification: Next: comparing cost or usage with a budget amount over a selected period.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast the evidence
(mechanism) Choose the supplied rule, approved resource scope and parameters, then run or inspect evaluations for both sample configurations. Read each resource ID alongside its compliance result. Rule presence alone cannot distinguish an acceptable sample from a prohibited one. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.config_evaluations cols=['resource_id', 'selected_rule', 'resource_scope', 'parameters', 'sample_configuration', 'compliance_result'] ] caption: 
### r02 · Contrast the evidence
(mechanism) The managed rule evaluates supported configuration against its criteria and configured parameters. Choose the supplied rule, approved resource scope and parameters, then run or inspect evaluations for both sample configurations. Read each resource ID alongside its compliance result. Rule presence alone cannot distinguish an acceptable sample from a prohibited one. ⟦A.f1 A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.config_evaluations cols=['resource_id', 'selected_rule', 'resource_scope', 'parameters', 'sample_configuration', 'compliance_result'] ] caption: 

=========

# EVALUATOR PACKET — Configure a budget notification (aws_devops.tile.052)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.configure_a_budget_notification — Configure a budget notification

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.configure_a_budget_notification)   objective: Configure an AWS budget notification
A.f1: An AWS budget compares cost or usage with a configured budget amount over a selected period.   [sources: aws_cost_management_user_guide#budgets-create.html]
A.f2: Create a cost budget with the approved scope, amount and period, then configure an actual or forecast threshold and approved notification recipient.   [sources: aws_cost_management_user_guide#budgets-create.html]
A.f3: A notification alerts its recipients; stopping resources requires separately configured actions rather than the notification itself.   [sources: aws_cost_management_user_guide#budgets-create.html]
note: Use supplied amounts and thresholds; do not estimate workload cost or configure unrequested budget actions.
PRACTICE ANCHOR (tool_simulation): Set one sandbox cost budget using the supplied approved scope, amount and period, with one actual or forecast threshold notification sent to the approved recipient.  SUCCESS: The saved budget matches the supplied scope, amount and period. Exactly one notification matches the supplied threshold value, actual or forecast basis, and approved recipient. No resource-stopping actions are configured.
ASSESSMENT ANCHOR: verify_budget_threshold_and_recipient_against_spend_policy facts=['f2']

## DATA ASSETS USED
ds.budget_notification: Approved and saved budget notification settings — columns: settings_record(categorical), budget_id(identifier), scope(categorical), amount(numerical), period(categorical), notification_id(identifier), threshold_value(numerical), threshold_basis(categorical), recipient(text), resource_stopping_actions_configured(categorical)
   ["approved inputs","sandbox-cost-budget","sandbox workload",1000,"monthly","sandbox-cost-alert",80,"actual","budget-owner@example.invalid",false]
   ["saved configuration","sandbox-cost-budget","sandbox workload",1000,"monthly","sandbox-cost-alert",80,"actual","budget-owner@example.invalid",false]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Audit KMS-backed audit-storage encryption (SSE-KMS): verify encryption and KMS key-use authority; key-use authority is required for SSE-KMS, not SSE-S3; Audit storage access; Configure a CodeBuild buildspec for a supplied application; Configure a CodeDeploy deployment action for a supplied EC2 application; Configure and verify an EC2 Auto Scaling policy under bounded load; Configure artifact repository access; Configure artifact repository retention; Configure load-balancer listeners, targets and health checks; Configure log retention; Configure managed database backups and create/restore RDS snapshots; require only native RDS and backup foundations, with existing network setup given and no routing or security-group skills assumed; Configure scoped log access; Define an ECS task for a supplied image; Destroy review; Diagnose an IAM denied request from request and policy evidence; Execute a reviewed Terraform plan provisioning EC2; directly require the native EC2 instance foundation; Execute a scoped Systems Manager remote command after external shell preparation; Gate infrastructure changes with configuration validation after external declarative/configuration preparation; Handle A

## LESSON, in learner order

### s01 · explainer · An alert has settings, not stopping power
(mechanism) An AWS budget compares cost or usage with a configured amount over a selected period. Create a cost budget using the approved scope, amount and period; configure an actual or forecast threshold and the approved recipient. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3⟧
(example) Here the scope is sandbox workload, the supplied budget amount is 1000, and the period is monthly. The single notification uses the supplied threshold value of 80 on an actual basis, sent to budget-owner@example.invalid. Compare the saved settings with the approved inputs and retain the recipient setting. ⟦A.f1 A.f2 A:tb4⟧
[DIAGRAM: Supplied settings and evidence] nodes=['Cost budget {budget id: sandbox-cost-budget; scope: sandbox workload; amount: 1000; period: monthly}', 'Single notification {notification id: sandbox-cost-alert; threshold value: 80; threshold basis: actual; recipient: budget-owner@example.invalid}'] edges=[] alt: Read-only schematic of the supplied settings. Cost budget; budget id: sandbox-cost-budget; scope: sandbox workload; amount: 1000; period: monthly. Single notification; notification id: sandbox-cost-alert; threshold value: 80; threshold basis: actual; recipient: budget-owner@example.invalid
(misconception) A notification alerts recipients. It does not itself stop resources or cap spending; stopping requires separately configured actions. No resource-stopping actions are configured in this example. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧

### s02 · check · Check the notification settings
 — Compare the supplied notification settings with the approved inputs and choose the matching configuration.

### s03 · hands_on · Judge the budget notification excerpts
 — Read the supplied excerpts in this step and decide which match the approved budget and single notification settings.

### s04 · recap · Takeaways
(takeaway) A budget compares cost or usage with an amount over a period. Match the approved scope, amount and period, plus the single notification’s threshold value, actual or forecast basis, and recipient. Notifications alert recipients; stopping resources needs separately configured actions. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Continue to the next tile in this path.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast the evidence
(mechanism) Match the cost budget’s approved scope, amount and period, then its single notification’s threshold value, actual or forecast basis, and approved recipient. A matching threshold alone is not enough if the basis or recipient differs. Compare the approved-input record with the saved-configuration record. ⟦A.f2 A:tb3 A:tb4⟧
[TABLE ds.budget_notification cols=['settings_record', 'budget_id', 'scope', 'amount', 'period', 'notification_id', 'threshold_value', 'threshold_basis', 'recipient', 'resource_stopping_actions_configured'] ] caption: 