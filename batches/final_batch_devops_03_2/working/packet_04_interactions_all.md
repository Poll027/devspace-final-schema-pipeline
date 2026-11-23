# EVALUATOR PACKET — Automate prohibited-configuration checks (aws_devops.tile.051)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.automate_prohibited_configuration_checks — Automate prohibited-configuration checks

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: remediation step aws_devops.tile.051.r02 is never referenced

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
QUESTION [choice, intro, grading=client] Read these supplied in-scope sample evaluation rows. Which conclusion is supported?
```json
[
  {
    "resource_id": "sample-acceptable",
    "selected_rule": "supplied Config managed rule",
    "resource_scope": "approved sandbox resource scope",
    "parameters": "supplied approved parameters",
    "sample_configuration": "supplied compliant sample",
    "compliance_result": "COMPLIANT"
  },
  {
    "resource_id": "sample-prohibited",
    "selected_rule": "supplied Config managed rule",
    "resource_scope": "approved sandbox resource scope",
    "parameters": "supplied approved parameters",
    "sample_configuration": "supplied noncompliant sample",
    "compliance_result": "NON_COMPLIANT"
  }
]
```
  ✔ individual: sample-acceptable passes and sample-prohibited is flagged; rule presence alone does not prove all resources passed.
      why: Each conclusion is tied to an individual resource ID and compliance result.
  ✘ presence: Both samples passed because the supplied managed rule is present.
      why: Rule presence is setup evidence, not each resource’s compliance result. One supplied row is noncompliant.
  ✘ all_fail: Both samples failed because one noncompliant result invalidates the compliant result.
      why: Read individual resource IDs and results. The compliant sample still has its own passing result.
  feedback✔: You used both individual results, not just rule presence.  feedback✘: Tie each conclusion to its own evaluation row.  hints: ['Compare the two compliance results.', 'Does the existence of a rule tell you the outcome for each resource?']  remediation→r01
  MEASURES: A:detect_noncompliant_configuration_without_false_positives(f2,f3)   anchors=['assessment:detect_noncompliant_configuration_without_false_positives']
  taught-before-tested: A.f2←s01; A.f3←s01

### s04 · hands_on · Review the configuration evidence
 — Read the supplied excerpts in this step and decide which correctly select the rule, scope and parameters and verify the individual sample results.
QUESTION [classify, stretch, grading=client] Read each proposed Config review excerpt and decide whether it meets ALL supplied criteria. Required settings:
```json
{
  "selected_rule": "supplied Config managed rule",
  "resource_scope": "approved sandbox resource scope",
  "parameters": "supplied approved parameters"
}
```
Required sample evidence:
```json
[
  {
    "resource_id": "sample-acceptable",
    "selected_rule": "supplied Config managed rule",
    "resource_scope": "approved sandbox resource scope",
    "parameters": "supplied approved parameters",
    "sample_configuration": "supplied compliant sample",
    "compliance_result": "COMPLIANT"
  },
  {
    "resource_id": "sample-prohibited",
    "selected_rule": "supplied Config managed rule",
    "resource_scope": "approved sandbox resource scope",
    "parameters": "supplied approved parameters",
    "sample_configuration": "supplied noncompliant sample",
    "compliance_result": "NON_COMPLIANT"
  }
]
```
Both samples are in the approved scope. A valid review matches the rule, scope and parameters, retains each resource ID and its expected compliance result, does not accept rule presence alone, and performs no remediation.
  '{
  "selected_settings": {
    "selected_rule": "supplied Config managed rule",
    "resource_scope": "approved sandbox resource scope",
    "parameters": "supplied approved parameters"
  },
  "evaluation_rows": [
    {
      "resource_id": "sample-acceptable",
      "selected_rule": "supplied Config managed rule",
      "resource_scope": "approved sandbox resource scope",
      "parameters": "supplied approved parameters",
      "sample_configuration": "supplied compliant sample",
      "compliance_result": "COMPLIANT"
    },
    {
      "resource_id": "sample-prohibited",
      "selected_rule": "supplied Config managed rule",
      "resource_scope": "approved sandbox resource scope",
      "parameters": "supplied approved parameters",
      "sample_configuration": "supplied noncompliant sample",
      "compliance_result": "NON_COMPLIANT"
    }
  ],
  "compliance_evidence": "individual resource IDs and compliance results",
  "remediation_performed": false
}' -> Meets the supplied review criteria
      feedback: The rule, scope and parameters match, both resource IDs and their expected results are retained, and no remediation is performed.
  '{
  "selected_settings": {
    "selected_rule": "supplied Config managed rule",
    "resource_scope": "approved sandbox resource scope",
    "parameters": "supplied approved parameters"
  },
  "evaluation_rows": [
    {
      "resource_id": "sample-acceptable",
      "selected_rule": "supplied Config managed rule",
      "resource_scope": "approved sandbox resource scope",
      "parameters": "supplied approved parameters",
      "sample_configuration": "supplied compliant sample",
      "compliance_result": "COMPLIANT"
    },
    {
      "resource_id": "sample-prohibited",
      "selected_rule": "supplied Config managed rule",
      "resource_scope": "approved sandbox resource scope",
      "parameters": "supplied approved parameters",
      "sample_configuration": "supplied noncompliant sample",
      "compliance_result": "COMPLIANT"
    }
  ],
  "compliance_evidence": "individual resource IDs and compliance results",
  "remediation_performed": false
}' -> Fails the supplied review criteria
      feedback: The supplied prohibited sample must be flagged. Reporting both samples as compliant fails the boundary check; inspect scope and parameters.
  '{
  "selected_settings": {
    "selected_rule": "supplied Config managed rule",
    "resource_scope": "approved sandbox resource scope",
    "parameters": "supplied approved parameters"
  },
  "evaluation_rows": [],
  "compliance_evidence": "rule presence alone",
  "remediation_performed": false
}' -> Fails the supplied review criteria
      feedback: Rule presence alone omits both individual evaluations and cannot prove compliance.
  '{
  "selected_settings": {
    "selected_rule": "supplied Config managed rule",
    "resource_scope": "scope excludes the supplied noncompliant sample",
    "parameters": "supplied approved parameters"
  },
  "evaluation_rows": [
    {
      "resource_id": "sample-acceptable",
      "selected_rule": "supplied Config managed rule",
      "resource_scope": "approved sandbox resource scope",
      "parameters": "supplied approved parameters",
      "sample_configuration": "supplied compliant sample",
      "compliance_result": "COMPLIANT"
    },
    {
      "resource_id": "sample-prohibited",
      "selected_rule": "supplied Config managed rule",
      "resource_scope": "approved sandbox resource scope",
      "parameters": "supplied approved parameters",
      "sample_configuration": "supplied noncompliant sample",
      "compliance_result": "NON_COMPLIANT"
    }
  ],
  "compliance_evidence": "individual resource IDs and compliance results",
  "remediation_performed": false
}' -> Fails the supplied review criteria
      feedback: The scope excludes a required sample, so its result cannot validate the intended in-scope criterion.
  feedback✔: You checked settings, both sample results and the evidence boundary.  feedback✘: A complete review needs matching settings and both expected individual evaluations, without remediation.  hints: ['Check the selected scope before trusting a sample result.', 'Look for both resource IDs, not merely a rule name.']
  MEASURES: A:select_rule_scope_and_parameters_for_supplied_criteria(f1,f2); A:verify_compliance_from_individual_resource_evaluations(f3)   anchors=['practice', 'assessment:select_rule_scope_and_parameters_for_supplied_criteria', 'assessment:verify_compliance_from_individual_resource_evaluations']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

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

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.configure_a_budget_notification)   objective: Configure an AWS budget notification
A.f1: An AWS budget compares cost or usage with a configured budget amount over a selected period.   [sources: aws_cost_management_user_guide#budgets-create.html]
A.f2: Create a cost budget with the approved scope, amount and period, then configure an actual or forecast threshold and approved notification recipient.   [sources: aws_cost_management_user_guide#budgets-create.html]
A.f3: A notification alerts its recipients; stopping resources requires separately configured actions rather than the notification itself.   [sources: aws_cost_management_user_guide#budgets-create.html]
note: Use supplied amounts and thresholds; do not estimate workload cost or configure unrequested budget actions.
PRACTICE ANCHOR (tool_simulation): Set one sandbox cost budget using the supplied approved scope, amount and period, with one actual or forecast threshold notification sent to the approved recipient.  SUCCESS: The saved budget matches the supplied scope, amount and period. Exactly one notification matches the supplied threshold value, actual or forecast basis, and approved recipient. No resource-stopping actions are configured.
ASSESSMENT ANCHOR: verify_budget_threshold_and_recipient_against_spend_policy facts=['f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Audit KMS-backed audit-storage encryption (SSE-KMS): verify encryption and KMS key-use authority; key-use authority is required for SSE-KMS, not SSE-S3; Audit storage access; Configure a CodeBuild buildspec for a supplied application; Configure a CodeDeploy deployment action for a supplied EC2 application; Configure and verify an EC2 Auto Scaling policy under bounded load; Configure artifact repository access; Configure artifact repository retention; Configure load-balancer listeners, targets and health checks; Configure log retention; Configure managed database backups and create/restore RDS snapshots; require only native RDS and backup foundations, with existing network setup given and no routing or security-group skills assumed; Configure scoped log access; Define an ECS task for a supplied image; Destroy review; Diagnose an IAM denied request from request and policy evidence; Execute a reviewed Terraform plan provisioning EC2; directly require the native EC2 instance foundation; Execute a scoped Systems Manager remote command after external shell preparation; Gate infrastructure changes with configuration validation after external declarative/configuration preparation; Handle A

## LESSON, in learner order

### s01 · explainer · An alert has settings, not stopping power
(mechanism) An AWS budget compares cost or usage with a configured amount over a selected period. Create a cost budget using the approved scope, amount and period; configure an actual or forecast threshold and the approved recipient. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3⟧
(example) Here the scope is sandbox workload, the supplied budget amount is 1000, and the period is monthly. The single notification uses the supplied threshold value of 80 on an actual basis, sent to budget-owner@example.invalid. Compare the saved settings with the approved inputs and retain the recipient setting. ⟦A.f1 A.f2 A:tb4⟧
[DIAGRAM: Supplied settings and evidence] nodes=['Cost budget {budget id: sandbox-cost-budget; scope: sandbox workload; amount: 1000; period: monthly}', 'Single notification {notification id: sandbox-cost-alert; threshold value: 80; threshold basis: actual; recipient: budget-owner@example.invalid}'] edges=[] alt: Read-only schematic of the supplied settings. Cost budget; budget id: sandbox-cost-budget; scope: sandbox workload; amount: 1000; period: monthly. Single notification; notification id: sandbox-cost-alert; threshold value: 80; threshold basis: actual; recipient: budget-owner@example.invalid
(misconception) A notification alerts recipients. It does not itself stop resources or cap spending; stopping requires separately configured actions. No resource-stopping actions are configured in this example. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧

### s02 · check · Check the notification settings
 — Compare the supplied notification settings with the approved inputs and choose the matching configuration.
QUESTION [choice, intro, grading=client] Read the approved notification settings below. Which candidate matches the threshold value (percent of budget amount), actual or forecast basis, and recipient?
```json
{
  "threshold_value": 80,
  "threshold_basis": "actual",
  "recipient": "budget-owner@example.invalid"
}
```
  ✔ option1: {
  "threshold_value": 80,
  "threshold_basis": "actual",
  "recipient": "budget-owner@example.invalid"
}
      why: All three settings match the approved inputs.
  ✘ option2: {
  "threshold_value": 80,
  "threshold_basis": "forecast",
  "recipient": "budget-owner@example.invalid"
}
      why: The threshold basis differs from the approved input; the same threshold value does not make actual and forecast interchangeable for this requirement.
  ✘ option3: {
  "threshold_value": 80,
  "threshold_basis": "actual",
  "recipient": ""
}
      why: The approved recipient is missing; a matching threshold alone is insufficient.
  feedback✔: The threshold value, basis and recipient all match.  feedback✘: Compare all three settings; one matching field is not enough.  hints: ['Check the threshold basis separately from its value.', 'The recipient must also match the approved input.']  remediation→r01
  MEASURES: A:verify_budget_threshold_and_recipient_against_spend_policy(f2)   anchors=['assessment:verify_budget_threshold_and_recipient_against_spend_policy']
  taught-before-tested: A.f2←s01

### s03 · hands_on · Judge the budget notification excerpts
 — Read the supplied excerpts in this step and decide which match the approved budget and single notification settings.
QUESTION [classify, stretch, grading=client] Read each saved-settings excerpt and decide whether it meets ALL approved criteria below. The threshold value is a percent of the budget amount. A valid result has matching scope, amount and period, exactly one matching notification (threshold value, actual or forecast basis, and approved recipient), and no resource-stopping actions.
Approved criteria:
```json
{
  "budget": {
    "budget_id": "sandbox-cost-budget",
    "scope": "sandbox workload",
    "amount": 1000,
    "period": "monthly"
  },
  "notifications": [
    {
      "notification_id": "sandbox-cost-alert",
      "threshold_value": 80,
      "threshold_basis": "actual",
      "recipient": "budget-owner@example.invalid"
    }
  ],
  "resource_stopping_actions_configured": false
}
```
  '{
  "budget": {
    "budget_id": "sandbox-cost-budget",
    "scope": "sandbox workload",
    "amount": 1000,
    "period": "monthly"
  },
  "notifications": [
    {
      "notification_id": "sandbox-cost-alert",
      "threshold_value": 80,
      "threshold_basis": "actual",
      "recipient": "budget-owner@example.invalid"
    }
  ],
  "resource_stopping_actions_configured": false
}' -> Meets the supplied review criteria
      feedback: The saved budget and its exactly one notification match every approved setting, with no resource-stopping actions.
  '{
  "budget": {
    "budget_id": "sandbox-cost-budget",
    "scope": "sandbox workload",
    "amount": 1000,
    "period": "monthly"
  },
  "notifications": [
    {
      "notification_id": "sandbox-cost-alert",
      "threshold_value": 80,
      "threshold_basis": "forecast",
      "recipient": "budget-owner@example.invalid"
    }
  ],
  "resource_stopping_actions_configured": false
}' -> Fails the supplied review criteria
      feedback: The notification basis differs from the approved basis, even though its threshold and recipient match.
  '{
  "budget": {
    "budget_id": "sandbox-cost-budget",
    "scope": "sandbox workload",
    "amount": 2000,
    "period": "monthly"
  },
  "notifications": [
    {
      "notification_id": "sandbox-cost-alert",
      "threshold_value": 80,
      "threshold_basis": "actual",
      "recipient": "budget-owner@example.invalid"
    }
  ],
  "resource_stopping_actions_configured": false
}' -> Fails the supplied review criteria
      feedback: The saved budget amount differs from the approved amount; matching notification settings do not fix that.
  '{
  "budget": {
    "budget_id": "sandbox-cost-budget",
    "scope": "sandbox workload",
    "amount": 1000,
    "period": "monthly"
  },
  "notifications": [
    {
      "notification_id": "sandbox-cost-alert",
      "threshold_value": 80,
      "threshold_basis": "actual",
      "recipient": "budget-owner@example.invalid"
    },
    {
      "notification_id": "sandbox-cost-alert",
      "threshold_value": 80,
      "threshold_basis": "actual",
      "recipient": "budget-owner@example.invalid"
    }
  ],
  "resource_stopping_actions_configured": false
}' -> Fails the supplied review criteria
      feedback: Two notification entries violate the exactly-one requirement, even though their settings match.
  '{
  "budget": {
    "budget_id": "sandbox-cost-budget",
    "scope": "sandbox workload",
    "amount": 1000,
    "period": "monthly"
  },
  "notifications": [
    {
      "notification_id": "sandbox-cost-alert",
      "threshold_value": 80,
      "threshold_basis": "actual",
      "recipient": "budget-owner@example.invalid"
    }
  ],
  "resource_stopping_actions_configured": true
}' -> Fails the supplied review criteria
      feedback: Resource-stopping actions are configured, contrary to this notification-only task.
  feedback✔: You checked the full saved budget, exactly one notification and the absence of stopping actions.  feedback✘: Check every budget and notification field, the notification count and the action setting.  hints: ['A matching threshold does not establish that the budget amount matches.', 'Inspect the full notification list and the action setting.']
  MEASURES: A:verify_budget_threshold_and_recipient_against_spend_policy(f2)   anchors=['practice', 'assessment:verify_budget_threshold_and_recipient_against_spend_policy']
  taught-before-tested: A.f2←s01

### s04 · recap · Takeaways
(takeaway) A budget compares cost or usage with an amount over a period. Match the approved scope, amount and period, plus the single notification’s threshold value, actual or forecast basis, and recipient. Notifications alert recipients; stopping resources needs separately configured actions. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Continue to the next tile in this path.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast the evidence
(mechanism) Match the cost budget’s approved scope, amount and period, then its single notification’s threshold value, actual or forecast basis, and approved recipient. A matching threshold alone is not enough if the basis or recipient differs. Compare the approved-input record with the saved-configuration record. ⟦A.f2 A:tb3 A:tb4⟧
[TABLE ds.budget_notification cols=['settings_record', 'budget_id', 'scope', 'amount', 'period', 'notification_id', 'threshold_value', 'threshold_basis', 'recipient', 'resource_stopping_actions_configured'] ] caption: 