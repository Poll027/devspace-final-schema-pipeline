# EVALUATOR PACKET — Finding evidence before response / Verify the audit access boundary / Separate object and key authority (aws_devops.tile.074)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.triage_a_representative_guardduty_finding — Triage a representative GuardDuty finding
B = security.audit_storage_access — Audit storage access
C = security.audit_storage_encryption — Audit KMS-backed audit-storage encryption (SSE-KMS): verify encryption and KMS key-use authority; key-use authority is required for SSE-KMS, not SSE-S3

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.triage_a_representative_guardduty_finding)   objective: Triage a GuardDuty finding
A.f1: A GuardDuty finding contains a finding type, severity, affected resource and details of suspicious activity.   [sources: aws_guardduty_user_guide#guardduty_findings-summary.html]
A.f2: Inspect resource identity, activity timestamps and finding details, and preserve the evidence supporting investigation.   [sources: aws_guardduty_user_guide#guardduty_findings-summary.html]
A.f3: Follow the established investigation and escalation procedure for the finding type rather than taking destructive action from severity alone.   [sources: aws_guardduty_user_guide#guardduty_remediate.html]
note: Do not invent compromise conclusions or specialist incident-containment actions.
PRACTICE ANCHOR (tool_simulation): Triage one supplied GuardDuty finding using a read-only finding interface and its established investigation and escalation procedure. Record the finding type, severity, affected resource identity, activity timestamps and suspicious activity details; preserve the supporting evidence and identify the procedure-supported next step.  SUCCESS: The triage record accurately identifies the affected identity or resource, retains the supplied activity timestamps and supporting finding details, and selects the next investigation or escalation step specified by the supplied procedure. It neither asserts compromise without supporting evidence nor takes destructive action from severity alone.
ASSESSMENT ANCHOR: identify_affected_identity_or_resource_from_finding_evidence facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_evidence_supported_escalation_under_established_procedure facts=['f2', 'f3']

## SOURCE FACTS — B (security.audit_storage_access)   objective: Authorize access to audit storage
B.f1: S3 bucket policies can grant or deny object operations to specified principals and resource paths.   [sources: aws_s3_user_guide#example-bucket-policies.html]
B.f2: Give approved audit writers and readers only their required actions on the intended bucket or object ARNs; inspect other applicable grants and denies.   [sources: aws_s3_user_guide#example-bucket-policies.html]
B.f3: Test a write and read with approved identities and a read with the unapproved identity; encryption or retention settings do not replace authorization checks.   [sources: aws_s3_user_guide#example-bucket-policies.html]
note: Use supplied audit paths and policy; do not broaden principal access for convenience.
PRACTICE ANCHOR (tool_simulation): Apply least-privilege access to the supplied S3 audit bucket policy using the supplied approved writers, approved readers and audit paths. Inspect other applicable grants and denies, then test an approved write, an approved read and an unapproved read.  SUCCESS: The policy grants approved writers and readers only their required actions on the intended bucket or object ARNs without broadening principal access. Applicable grants and denies have been inspected. The approved write and read succeed, and the unapproved read is denied, with the identity, resource path and result recorded for each test. Encryption or retention settings are not treated as authorization evidence.
ASSESSMENT ANCHOR: distinguish_approved_and_denied_principal_operations facts=['f1', 'f2']
ASSESSMENT ANCHOR: evaluate_action_and_resource_scope_with_applicable_grants_and_denies facts=['f2']
ASSESSMENT ANCHOR: verify_authorization_using_approved_and_unapproved_identity_tests facts=['f3']

## SOURCE FACTS — C (security.audit_storage_encryption)   objective: Verify KMS-backed audit-storage encryption
C.f1: SSE-KMS encrypts S3 objects with an AWS KMS key, while SSE-S3 uses S3-managed keys.   [sources: aws_s3_user_guide#UsingKMSEncryption.html]
C.f2: Reading an SSE-KMS object requires both s3:GetObject permission and kms:Decrypt authority for its key; SSE-S3 does not require KMS key-use permission.   [sources: aws_s3_user_guide#UsingKMSEncryption.html]
C.f3: Configure the supplied KMS key as bucket default encryption and test reads with approved object/key authority and with KMS use denied; inspect the object’s encryption metadata.   [sources: aws_s3_user_guide#UsingKMSEncryption.html]
C.m1 (misconception): Changing bucket default encryption does not re-encrypt objects that already exist; their individual encryption settings still matter.   [sources: aws_s3_user_guide#bucket-encryption.html]
note: Keep existing-object/default distinction explicit; do not invent key-policy setup or re-encryption procedures.
PRACTICE ANCHOR (tool_simulation): Configure the supplied KMS key as default encryption on one sandbox audit bucket. Inspect the supplied SSE-KMS object's encryption metadata, then test reads using prepared identities with approved object/key authority and with KMS use denied. Compare the KMS authority requirement with SSE-S3.  SUCCESS: The bucket default identifies the supplied KMS key, and the object's metadata confirms SSE-KMS and its key. The read with approved s3:GetObject and kms:Decrypt authority succeeds; the read with s3:GetObject allowed but KMS use denied fails. The learner identifies that SSE-S3 needs no KMS key-use authority and that changing the bucket default does not re-encrypt existing objects.
ASSESSMENT ANCHOR: distinguish_s3_object_permission_from_kms_key_use_authority facts=['f1', 'f2']
ASSESSMENT ANCHOR: determine_sse_kms_read_authorization_from_object_and_key_authority facts=['f2']

## DATA ASSETS USED
ds.audit_access_tests: Audit object authorization checks — columns: test_id(identifier), principal(identifier), requested_action(categorical), resource_arn(identifier), scoped_policy_statement(text), other_grants_and_denies_review(text), observed_result(categorical)
   ["approved-write","audit-writer","s3:PutObject","arn:aws:s3:::sandbox-audit/audit/record.json","Allow audit-writer s3:PutObject on arn:aws:s3:::sandbox-audit/audit/* only.","Applicable grants and denies reviewed for this request.","allowed"]
   ["approved-read","audit-reader","s3:GetObject","arn:aws:s3:::sandbox-audit/audit/record.json","Allow audit-reader s3:GetObject on arn:aws:s3:::sandbox-audit/audit/* only.","Applicable grants and denies reviewed for this request.","allowed"]
   ["unapproved-read","unapproved-reader","s3:GetObject","arn:aws:s3:::sandbox-audit/audit/record.json","No grant to unapproved-reader in the supplied scoped policy.","Applicable grants and denies reviewed; no applicable permission permits this read.","denied"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply an approved security baseline to sandbox accounts; Apply bounded EKS workload configuration and secrets after external configuration/secrets preparation; Audit KMS-backed audit-storage encryption (SSE-KMS): verify encryption and KMS key-use authority; key-use authority is required for SSE-KMS, not SSE-S3; Audit storage access; Configure CodePipeline source-to-deploy actions; directly require native IAM identity-policy evaluation and role trust for the service execution role, not pipeline federation; Credential expiry; Deploy a supplied CloudFormation S3 environment across accounts and Regions with assumed roles; directly require the native S3 object-storage concept; Destroy review; Diagnose AWS connectivity failures using prepared DNS, HTTP, ports and CIDR foundations; Dry run; Ecs task identity; Execute an established fleet patch task after external package-management and shell preparation; Expose an EKS workload using a Kubernetes Service; Inject a controlled failure and verify alarm behavior; Partial failure; Perform a Lambda version-and-alias release with rollback; Perform a managed EKS Deployment rollout; Perform an EC2 blue/green deployment with CodeDeploy; Perform clea

## LESSON, in learner order

### s01 · explainer · Finding evidence before response
Explain — 
(mechanism) A GuardDuty finding contains its type, severity, affected resource and suspicious-activity details. Inspect resource identity, activity timestamps and details; preserve the supporting evidence. Follow the established investigation and escalation procedure for that finding type. Severity alone is not a reason for destructive action. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3⟧
[DIAGRAM: Illustrative fictional finding panel — not a live finding] nodes=['Finding type: supplied type A; Severity: high', 'Affected resource: node A', 'Activity: 10:00–10:05 UTC', 'Suspicious activity: supplied activity detail', 'Opened: 10:20 UTC', 'Preserve 10:00–10:05 as the activity timeline; follow the established type-A procedure. Severity alone does not establish compromise.'] edges=[('n0', 'n5', 'context'), ('n1', 'n5', 'identity'), ('n2', 'n5', 'timeline'), ('n3', 'n5', 'details'), ('n4', 'n2', 'do not substitute')] alt: Illustrative fictional finding panel — not a live finding. Finding type: supplied type A; Severity: high; Affected resource: node A; Activity: 10:00–10:05 UTC; Suspicious activity: supplied activity detail; Opened: 10:20 UTC; Preserve 10:00–10:05 as the activity timeline; follow the established type-A procedure. Severity alone does not establish compromise.

### s02 · explainer · Inspect the evidence and the contrast
Worked review — 
(example) Record the supplied finding’s type, severity, resource identity and activity timestamps. Keep those activity timestamps rather than replacing them with the time the finding was opened. Preserve the detailed activity evidence and follow the finding-type procedure. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧
(example) A severe finding adds urgency, not proof of compromise or permission to destroy a resource. If detail is incomplete, preserve what is available and escalate under the established procedure. Missing detail does not establish an attack mechanism. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · check · Check finding evidence before response
Knowledge check — Choose the interpretation supported by the supplied evidence.

### s04 · hands_on · Review finding evidence before response
Evidence judgement — Read the supplied excerpts in this step and decide which interpretations or proposed actions are correct, defective or unsafe.

### s05 · explainer · Verify the audit access boundary
Explain — 
(mechanism) S3 bucket policies can grant or deny object operations for specified principals and resource paths. Limit approved audit writers and readers to required actions on intended bucket or object ARNs, and inspect other applicable grants and denies. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Verify the boundary with an approved write, an approved read and an unapproved read. Keep identity and resource path with each result. Encryption or retention settings do not replace these authorization checks. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[SIDE_BY_SIDE] Check identity, action and resource with each result. left_label: Policy scope and applicable authority | right_label: Three observed authorization tests
  left:
[TABLE ds.audit_access_tests cols=['principal', 'requested_action', 'resource_arn', 'scoped_policy_statement', 'other_grants_and_denies_review'] ] caption: 
  right:
[TABLE ds.audit_access_tests cols=['test_id', 'principal', 'requested_action', 'resource_arn', 'observed_result'] ] caption: 

### s06 · check · Check verify the audit access boundary
Knowledge check — Choose the interpretation supported by the supplied evidence.

### s07 · hands_on · Review the audit access boundary
Evidence judgement — Read the supplied excerpts in this step and decide which interpretations or proposed actions are correct, defective or unsafe.

### s08 · explainer · Separate object and key authority
Explain — 
(mechanism) SSE-KMS uses an AWS KMS key; SSE-S3 uses S3-managed keys. An SSE-KMS read needs both s3:GetObject permission and kms:Decrypt authority for that key. SSE-S3 does not require KMS key-use permission. Configure the supplied key as bucket default encryption, test approved object/key authority and denied KMS use, and inspect object metadata. ⟦C.f1 C.f2 C.f3 C:tb1 C:tb2 C:tb3⟧
[DIAGRAM: Two encryption models, separate authority boundaries] nodes=['Audit reader', 's3:GetObject permission', 'kms:Decrypt authority for object key', 'SSE-KMS object metadata', 'SSE-S3 object metadata: S3-managed keys; no KMS key-use permission', 'Bucket default: does not re-encrypt existing objects'] edges=[('n0', 'n1', 'object permission'), ('n1', 'n2', 'SSE-KMS also needs'), ('n2', 'n3', 'key authority'), ('n1', 'n4', 'SSE-S3 path'), ('n5', 'n3', 'inspect individual metadata'), ('n5', 'n4', 'inspect individual metadata')] alt: Two encryption models, separate authority boundaries. Audit reader; s3:GetObject permission; kms:Decrypt authority for object key; SSE-KMS object metadata; SSE-S3 object metadata: S3-managed keys; no KMS key-use permission; Bucket default: does not re-encrypt existing objects

### s09 · explainer · Inspect the evidence and the contrast
Worked review — 
(example) For the supplied SSE-KMS object, compare a read with approved s3:GetObject and kms:Decrypt authority against a read with KMS use denied. Inspect that object’s encryption metadata to determine its encryption model. ⟦C.f1 C.f2 C.f3 C.m1 C:tb4 C:tb5 C:tb6⟧
(example) Changing bucket default encryption does not re-encrypt existing objects. A default setting is therefore not proof of an older object’s encryption. Keep SSE-KMS’s key-use requirement separate from SSE-S3, which needs no KMS key-use permission. ⟦C.f1 C.f2 C.f3 C.m1 C:tb4 C:tb5 C:tb6⟧

### s10 · check · Check separate object and key authority
Knowledge check — Choose the interpretation supported by the supplied evidence.

### s11 · hands_on · Review object and key authority
Evidence judgement — Read the supplied excerpts in this step and decide which interpretations or proposed actions are correct, defective or unsafe.

### s12 · recap · Keep the evidence boundaries clear
(takeaway) Preserve finding evidence and follow the established procedure, not severity alone. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Verify scoped authorization with approved and unapproved identity tests. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
(takeaway) Separate SSE-KMS object permission, KMS authority and individual-object metadata. ⟦C.f1 C.f2 C.f3 C:tb2 C:tb3 C:tb4 C:tb5 C:tb6⟧
[UP NEXT] Up next: Review every Terraform action: Next: review a saved Terraform plan, including additions, updates, replacements and deletions.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit finding evidence before response
(mechanism) Inspect resource identity, activity timestamps and finding details, and preserve the evidence supporting investigation. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Follow the established investigation and escalation procedure for the finding type rather than taking destructive action from severity alone. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast: severity adds urgency; resource and activity evidence support the established investigation path, not destruction from severity alone. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit finding evidence before response
(mechanism) A GuardDuty finding contains a finding type, severity, affected resource and details of suspicious activity. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Inspect resource identity, activity timestamps and finding details, and preserve the evidence supporting investigation. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Follow the established investigation and escalation procedure for the finding type rather than taking destructive action from severity alone. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast: severity adds urgency; resource and activity evidence support the established investigation path, not destruction from severity alone. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
### r03 · Revisit verify the audit access boundary
(mechanism) Test a write and read with approved identities and a read with the unapproved identity; encryption or retention settings do not replace authorization checks. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) Contrast: encryption or retention describes storage protection, not proof that an unapproved reader is denied. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
[SIDE_BY_SIDE] Check identity, action and resource with each result. left_label: Policy scope and applicable authority | right_label: Three observed authorization tests
  left:
[TABLE ds.audit_access_tests cols=['principal', 'requested_action', 'resource_arn', 'scoped_policy_statement', 'other_grants_and_denies_review'] ] caption: 
  right:
[TABLE ds.audit_access_tests cols=['test_id', 'principal', 'requested_action', 'resource_arn', 'observed_result'] ] caption: 
### r04 · Revisit verify the audit access boundary
(mechanism) S3 bucket policies can grant or deny object operations to specified principals and resource paths. ⟦B.f1 B:tb2 B:tb4⟧
(mechanism) Give approved audit writers and readers only their required actions on the intended bucket or object ARNs; inspect other applicable grants and denies. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Test a write and read with approved identities and a read with the unapproved identity; encryption or retention settings do not replace authorization checks. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) Contrast: encryption or retention describes storage protection, not proof that an unapproved reader is denied. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
[SIDE_BY_SIDE] Check identity, action and resource with each result. left_label: Policy scope and applicable authority | right_label: Three observed authorization tests
  left:
[TABLE ds.audit_access_tests cols=['principal', 'requested_action', 'resource_arn', 'scoped_policy_statement', 'other_grants_and_denies_review'] ] caption: 
  right:
[TABLE ds.audit_access_tests cols=['test_id', 'principal', 'requested_action', 'resource_arn', 'observed_result'] ] caption: 
### r05 · Revisit separate object and key authority
(mechanism) Reading an SSE-KMS object requires both s3:GetObject permission and kms:Decrypt authority for its key; SSE-S3 does not require KMS key-use permission. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
(misconception) Contrast: SSE-KMS needs object permission and KMS authority; SSE-S3 has no KMS key-use requirement. Inspect object metadata, not just bucket defaults. ⟦C.f1 C.f2 C.m1 C:tb2 C:tb3 C:tb4 C:tb5 C:tb6⟧
### r06 · Revisit separate object and key authority
(mechanism) SSE-KMS encrypts S3 objects with an AWS KMS key, while SSE-S3 uses S3-managed keys. ⟦C.f1 C:tb2 C:tb4⟧
(mechanism) Reading an SSE-KMS object requires both s3:GetObject permission and kms:Decrypt authority for its key; SSE-S3 does not require KMS key-use permission. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
(misconception) Contrast: SSE-KMS needs object permission and KMS authority; SSE-S3 has no KMS key-use requirement. Inspect object metadata, not just bucket defaults. ⟦C.f1 C.f2 C.m1 C:tb2 C:tb3 C:tb4 C:tb5 C:tb6⟧

=========

# EVALUATOR PACKET — Review every Terraform action (aws_devops.tile.077)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = terraform.destroy_review — Destroy review

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (terraform.destroy_review)   objective: Authorize or block Terraform EC2 plan impact, with mandatory destruction review
A.f1: A Terraform plan describes proposed additions, updates, deletions and replacements based on configuration, state and observed infrastructure.   [sources: terraform_language#../cli/commands/plan]
A.f2: Create a saved plan with terraform plan -out=PLAN_FILE and inspect it with terraform show PLAN_FILE; replacement includes destruction and creation, not merely an in-place update.   [sources: terraform_language#../cli/commands/plan, terraform_language#../cli/commands/show]
A.f3: Compare affected resource identities and every proposed action, including the mandatory deletion case, with the supplied scope and impact criteria and record accept or block with plan evidence; review does not require destructive execution.   [sources: terraform_language#../cli/commands/plan]
note: Do not execute destructive review cases; keep replacement controls for their later concept.
PRACTICE ANCHOR (live_code): Provision one EC2 instance using the supplied preapproved Terraform configuration and apply scaffold. Create and inspect a subsequent saved EC2 change plan, compare every affected resource identity and proposed action against supplied scope and impact criteria, and record accept or block with supporting evidence. Include a mandatory deletion case without executing destructive changes.  SUCCESS: One EC2 instance is provisioned through the supplied preapproved scaffold. The review identifies additions, updates, replacements and deletions in the supplied cases, treats replacement as destruction plus creation, and records an evidence-backed accept/block decision against the supplied criteria. No destructive review plan is applied.
ASSESSMENT ANCHOR: identify_saved_ec2_plan_actions_and_resource_identities facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_replacement_from_in_place_update facts=['f2']
ASSESSMENT ANCHOR: accept_or_block_plan_scope_and_destructive_impact_with_evidence facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply an approved security baseline to sandbox accounts; Apply bounded EKS workload configuration and secrets after external configuration/secrets preparation; Configure CodePipeline source-to-deploy actions; directly require native IAM identity-policy evaluation and role trust for the service execution role, not pipeline federation; Credential expiry; Deploy a supplied CloudFormation S3 environment across accounts and Regions with assumed roles; directly require the native S3 object-storage concept; Diagnose AWS connectivity failures using prepared DNS, HTTP, ports and CIDR foundations; Dry run; Ecs task identity; Execute an established fleet patch task after external package-management and shell preparation; Expose an EKS workload using a Kubernetes Service; Inject a controlled failure and verify alarm behavior; Partial failure; Perform a Lambda version-and-alias release with rollback; Perform a managed EKS Deployment rollout; Perform an EC2 blue/green deployment with CodeDeploy; Perform cleanup after supplied-script failure; Reconcile Terraform EC2 drift; directly require the native EC2 instance foundation; Reuse a supplied Terraform module provisioning EC2; directly require the

## LESSON, in learner order

### s01 · explainer · Review every Terraform action
Explain — 
(mechanism) A Terraform plan describes proposed additions, updates, deletions and replacements using configuration, state and observed infrastructure. Save it with terraform plan -out=PLAN_FILE and inspect it with terraform show PLAN_FILE. Replacement includes destruction and creation, not just an in-place update. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3⟧
(mechanism) Compare affected resource identities and every proposed action, including the mandatory deletion case, with supplied scope and impact criteria. Record accept or block with plan evidence. Review does not require destructive execution. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3⟧
[CODE bash]
terraform plan -out=PLAN_FILE
terraform show PLAN_FILE
# Approved illustrative scope: add new; update existing; replace replacement; retain retained.
# + aws_instance.new — addition — ACCEPT: approved addition
# ~ aws_instance.existing — in-place update — ACCEPT: approved update
# -/+ aws_instance.replacement — destruction and creation — ACCEPT: both impacts approved
# - aws_instance.retained — deletion — BLOCK: retention required
  annotations: ['Save and inspect; no destructive execution is required.', 'These are illustrative review annotations; inspect the actual saved plan before recording its decision.']

### s02 · explainer · Inspect the evidence and the contrast
Worked review — 
(example) Keep each resource identity beside its proposed action. Check additions, updates, replacements and the supplied deletion against approved scope and impact criteria. A replacement includes destruction as well as creation. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧
(example) Record accept or block with the relevant saved-plan evidence. Do not execute a deletion merely to demonstrate that you identified it, and do not treat a general description of an “update” as proof that no infrastructure will be removed. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · check · Check review every terraform action
Knowledge check — Choose the interpretation supported by the supplied evidence.

### s04 · hands_on · Review every Terraform action
Evidence judgement — Read the supplied excerpts in this step and decide which interpretations or proposed actions are correct, defective or unsafe.

### s05 · recap · Keep the evidence boundaries clear
(takeaway) Inspect every saved-plan action, including deletion and replacement; record an evidence-backed accept/block decision. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Preview scope, check permissions: Continue to aws_devops.tile.078.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit review every terraform action
(mechanism) Compare affected resource identities and every proposed action, including the mandatory deletion case, with the supplied scope and impact criteria and record accept or block with plan evidence; review does not require destructive execution. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast: replacement includes destruction and creation; an in-place update is not the same action. Review evidence does not require destructive execution. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit review every terraform action
(mechanism) A Terraform plan describes proposed additions, updates, deletions and replacements based on configuration, state and observed infrastructure. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Create a saved plan with terraform plan -out=PLAN_FILE and inspect it with terraform show PLAN_FILE; replacement includes destruction and creation, not merely an in-place update. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Compare affected resource identities and every proposed action, including the mandatory deletion case, with the supplied scope and impact criteria and record accept or block with plan evidence; review does not require destructive execution. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast: replacement includes destruction and creation; an in-place update is not the same action. Review evidence does not require destructive execution. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Preview scope, check permissions / Keep fleet outcomes separate (aws_devops.tile.078)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = automation.dry_run — Dry run
B = automation.partial_failure — Partial failure

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (automation.dry_run)   objective: Preview a fleet operation with a dry run
A.f1: For EC2 API operations that support DryRun, the dry-run request checks permissions without executing the operation; DryRunOperation indicates sufficient permission and UnauthorizedOperation indicates insufficient permission.   [sources: aws_ec2_user_guide#../../../AWSEC2/latest/APIReference/API_StartInstances.html]
A.f2: Use the supplied fleet wrapper’s preview mode, inspect its proposed targets and actions and compare them with approved scope without enabling mutation.   [sources: aws_well_architected_framework#ops04-bp01.html]
A.f3: Dry-run permission success does not guarantee later operation success or provide a universal preview of every AWS service’s changes.   [sources: aws_ec2_user_guide#../../../AWSEC2/latest/APIReference/API_StartInstances.html]
note: Use supplied wrapper preview; do not generalize DryRun to unsupported operations or services.
PRACTICE ANCHOR (tool_simulation): Run one supplied fleet operation in the wrapper's preview mode and compare its proposed targets and actions with the supplied approved scope, without enabling mutation.  SUCCESS: Preview mode remains enabled and mutation remains disabled. The learner identifies whether the proposed targets and actions match the approved scope and records any discrepancies.
ASSESSMENT ANCHOR: verify_preview_targets_and_actions_against_approved_scope_without_mutation facts=['f2']
ASSESSMENT ANCHOR: distinguish_ec2_dry_run_permission_results_from_execution_and_change_preview facts=['f1', 'f3']

## SOURCE FACTS — B (automation.partial_failure)   objective: Handle partial fleet-operation failure
B.f1: A fleet command has separate invocation results for individual targets, which may differ within one command.   [sources: aws_systems_manager_user_guide#monitor-commands.html]
B.f2: Inspect invocation statuses and outputs and record successful, failed and unresolved targets separately.   [sources: aws_systems_manager_user_guide#monitor-commands.html]
B.f3: Use target-specific results to choose the scoped follow-up rather than blindly repeating the entire operation on already successful targets.   [sources: aws_systems_manager_user_guide#monitor-commands.html]
note: Do not invent retry safety or remedial commands; use supplied target-specific follow-up.
PRACTICE ANCHOR (field_selection): Inspect supplied invocation statuses and outputs for one operation on node A, node B and node C. Record each target as successful, failed or unresolved, then select the supplied target-specific follow-up appropriate to each outcome.  SUCCESS: Node A's successful result remains recorded and is excluded from repeat execution. Node B is reported as failed with its failure evidence and the supplied scoped follow-up. Node C remains separately recorded as unresolved pending further inspection. No fleet-wide rerun or invented remedial action is selected.
ASSESSMENT ANCHOR: classify_and_record_per_target_outcomes facts=['f1', 'f2']
ASSESSMENT ANCHOR: preserve_successful_targets_and_report_scoped_follow_up facts=['f2', 'f3']

## DATA ASSETS USED
ds.ec2_dryrun_evidence: Supported EC2 DryRun permission outcomes — columns: case_id(identifier), operation(text), dry_run(categorical), response_code(categorical), permission_evidence(text), operation_executed(categorical), later_success_guaranteed(categorical)
   ["permission-sufficient","Supplied EC2 operation that supports DryRun",true,"DryRunOperation","sufficient permission",false,false]
   ["permission-insufficient","Supplied EC2 operation that supports DryRun",true,"UnauthorizedOperation","insufficient permission",false,false]
ds.fleet_invocations: Separate fleet invocation results — columns: command_id(identifier), target_id(identifier), invocation_status(categorical), output_evidence(text), outcome_category(categorical), supplied_follow_up(text)
   ["command-review","node A","Success","Successful output confirms completion.","successful","Retain completion evidence; exclude from repeat execution."]
   ["command-review","node B","Failed","Invocation output reports failure.","failed","Retain node B’s failure evidence and route node B alone for review under the supplied procedure; do not repeat execution on node A."]
   ["command-review","node C","Unresolved","Available invocation evidence does not establish completion or failure.","unresolved","Inspect further before assigning an outcome or considering repeat execution."]
ds.wrapper_preview: Wrapper preview versus approved scope — columns: target_id(identifier), proposed_action(categorical), approved_target(categorical), approved_action(categorical), preview_mode(categorical), mutation_enabled(categorical)
   ["node A","supplied fleet operation",true,"supplied fleet operation",true,false]
   ["node B","supplied fleet operation",true,"supplied fleet operation",true,false]
   ["node C","supplied fleet operation",false,null,true,false]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply an approved security baseline to sandbox accounts; Apply bounded EKS workload configuration and secrets after external configuration/secrets preparation; Configure CodePipeline source-to-deploy actions; directly require native IAM identity-policy evaluation and role trust for the service execution role, not pipeline federation; Credential expiry; Credential readiness; Deploy a supplied CloudFormation S3 environment across accounts and Regions with assumed roles; directly require the native S3 object-storage concept; Diagnose AWS connectivity failures using prepared DNS, HTTP, ports and CIDR foundations; Ecs task identity; Execute an established fleet patch task after external package-management and shell preparation; Expose an EKS workload using a Kubernetes Service; Inject a controlled failure and verify alarm behavior; Partial failure; Perform a Lambda version-and-alias release with rollback; Perform a managed EKS Deployment rollout; Perform an EC2 blue/green deployment with CodeDeploy; Perform cleanup after supplied-script failure; Reconcile Terraform EC2 drift; directly require the native EC2 instance foundation; Reuse a supplied Terraform module provisioning EC2; directl

## LESSON, in learner order

### s01 · explainer · Preview scope, check permissions
Explain — 
(mechanism) For supported EC2 operations, DryRun checks permissions without executing the operation. DryRunOperation means sufficient permission; UnauthorizedOperation means insufficient permission. Neither is a real operation result or a guarantee of later success. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3⟧
(mechanism) The supplied fleet wrapper’s preview is a separate check: compare proposed targets and actions with approved scope while mutation stays disabled. EC2 DryRun is not a universal preview of every AWS service’s changes. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3⟧
[SIDE_BY_SIDE] Neither permission success nor preview is a guarantee of later execution success. left_label: Wrapper: proposed scope, mutation disabled | right_label: EC2: supported-operation permission evidence
  left:
[TABLE ds.wrapper_preview cols=all ] caption: 
  right:
[TABLE ds.ec2_dryrun_evidence cols=all ] caption: 

### s02 · explainer · Inspect the evidence and the contrast
Worked review — 
(example) Compare the wrapper’s proposed targets and actions with approved fleet scope and record discrepancies without enabling mutation. Retain that proposed-action evidence separately from the supported EC2 operation’s permission result. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧
(example) DryRunOperation means the dry-run permission check succeeded, not that the real operation ran. UnauthorizedOperation means insufficient permission. Permission success neither guarantees later operation success nor provides a service-wide change preview. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · check · Check preview scope, check permissions
Knowledge check — Choose the interpretation supported by the supplied evidence.

### s04 · hands_on · Review scope and permissions
Evidence judgement — Read the supplied excerpts in this step and decide which interpretations or proposed actions are correct, defective or unsafe.

### s05 · explainer · Keep fleet outcomes separate
Explain — 
(mechanism) One fleet command has separate invocation results for individual targets, and those results may differ. Inspect statuses and outputs; record successful, failed and unresolved targets separately. Choose the supplied scoped follow-up from target-specific evidence rather than blindly repeating successful work. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3⟧
[TABLE ds.fleet_invocations cols=all ] caption: 

### s06 · explainer · Inspect the evidence and the contrast
Worked review — 
(example) The supplied three-target case keeps successful, failed and unresolved outcomes separate. Retain target identity, invocation status and output evidence with each category. An unresolved outcome is not a failure established by evidence. ⟦B.f1 B.f2 B.f3 B:tb4 B:tb5⟧
(example) Keep successful work visible when selecting the supplied scoped follow-up. A single overall command label cannot replace per-target results, and one failure does not justify repeating the whole operation. Preserve uncertainty until inspection establishes the unresolved target’s outcome. ⟦B.f1 B.f2 B.f3 B:tb4 B:tb5⟧

### s07 · check · Check keep fleet outcomes separate
Knowledge check — Choose the interpretation supported by the supplied evidence.

### s08 · hands_on · Review separate fleet outcomes
Evidence judgement — Read the supplied excerpts in this step and decide which interpretations or proposed actions are correct, defective or unsafe.

### s09 · recap · Keep the evidence boundaries clear
(takeaway) Keep wrapper scope preview separate from supported EC2 DryRun permission evidence. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Record successful, failed and unresolved targets separately for scoped follow-up. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Up next: Renew identity, inspect outcomes: Continue to aws_devops.tile.080.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit preview scope, check permissions
(mechanism) For EC2 API operations that support DryRun, the dry-run request checks permissions without executing the operation; DryRunOperation indicates sufficient permission and UnauthorizedOperation indicates insufficient permission. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Dry-run permission success does not guarantee later operation success or provide a universal preview of every AWS service’s changes. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast: wrapper preview describes proposed scope; supported EC2 DryRun describes permissions, not execution or guaranteed later success. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[SIDE_BY_SIDE] Neither permission success nor preview is a guarantee of later execution success. left_label: Wrapper: proposed scope, mutation disabled | right_label: EC2: supported-operation permission evidence
  left:
[TABLE ds.wrapper_preview cols=all ] caption: 
  right:
[TABLE ds.ec2_dryrun_evidence cols=all ] caption: 
### r02 · Revisit preview scope, check permissions
(mechanism) Use the supplied fleet wrapper’s preview mode, inspect its proposed targets and actions and compare them with approved scope without enabling mutation. ⟦A.f2 A:tb3 A:tb4⟧
(misconception) Contrast: wrapper preview describes proposed scope; supported EC2 DryRun describes permissions, not execution or guaranteed later success. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[SIDE_BY_SIDE] Neither permission success nor preview is a guarantee of later execution success. left_label: Wrapper: proposed scope, mutation disabled | right_label: EC2: supported-operation permission evidence
  left:
[TABLE ds.wrapper_preview cols=all ] caption: 
  right:
[TABLE ds.ec2_dryrun_evidence cols=all ] caption: 
### r03 · Revisit keep fleet outcomes separate
(mechanism) Inspect invocation statuses and outputs and record successful, failed and unresolved targets separately. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Use target-specific results to choose the scoped follow-up rather than blindly repeating the entire operation on already successful targets. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) Contrast: an unresolved target is not an evidenced failure. Keep successful work distinct and use only the supplied scoped follow-up. ⟦B.f2 B.f3 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.fleet_invocations cols=all ] caption: 
### r04 · Revisit keep fleet outcomes separate
(mechanism) A fleet command has separate invocation results for individual targets, which may differ within one command. ⟦B.f1 B:tb2 B:tb4⟧
(mechanism) Inspect invocation statuses and outputs and record successful, failed and unresolved targets separately. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Use target-specific results to choose the scoped follow-up rather than blindly repeating the entire operation on already successful targets. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) Contrast: an unresolved target is not an evidenced failure. Keep successful work distinct and use only the supplied scoped follow-up. ⟦B.f2 B.f3 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.fleet_invocations cols=all ] caption: 

=========

# EVALUATOR PACKET — Renew identity, inspect outcomes (aws_devops.tile.080)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws.credential_expiry — Credential expiry

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws.credential_expiry)   objective: Recover from expired AWS credentials
A.f1: Temporary credentials stop being usable after expiration and must be replaced with a newly authorized session.   [sources: aws_iam_user_guide#id_credentials_temp_use-resources.html]
A.f2: On an expired-session error, renew the approved session through its credential provider and use the new access key, secret key and token together.   [sources: aws_iam_user_guide#id_credentials_temp_use-resources.html]
A.f3: Before retrying a resource-changing operation, inspect its known outcome and use a supported idempotency token where the supplied operation offers one to avoid duplicate effects.   [sources: aws_ec2_user_guide#../../../ec2/latest/devguide/ec2-api-idempotency.html]
note: Do not expose credentials or claim every AWS operation supports idempotency tokens.
PRACTICE ANCHOR (tool_simulation): Recover one supplied resource-changing automation operation from an expired session using the approved credential provider, without extending permissions. Inspect the operation's known outcome before deciding whether to retry, and use its supported idempotency token if a retry is warranted.  SUCCESS: The expired session is replaced through the approved provider with the new access key, secret key and session token used together, without displaying credential values or changing permissions. The learner checks the supplied outcome evidence, avoids repeating a known completed operation, and uses the supplied supported idempotency token for any warranted retry.
ASSESSMENT ANCHOR: recognize_temporary_credential_expiration facts=['f1']
ASSESSMENT ANCHOR: renew_approved_session_with_complete_credential_set facts=['f2']
ASSESSMENT ANCHOR: determine_safe_retry_from_known_outcome_and_supported_idempotency facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply an approved security baseline to sandbox accounts; Apply bounded EKS workload configuration and secrets after external configuration/secrets preparation; Configure CodePipeline source-to-deploy actions; directly require native IAM identity-policy evaluation and role trust for the service execution role, not pipeline federation; Credential readiness; Deploy a supplied CloudFormation S3 environment across accounts and Regions with assumed roles; directly require the native S3 object-storage concept; Diagnose AWS connectivity failures using prepared DNS, HTTP, ports and CIDR foundations; Ecs task identity; Execute an established fleet patch task after external package-management and shell preparation; Expose an EKS workload using a Kubernetes Service; Inject a controlled failure and verify alarm behavior; Perform a Lambda version-and-alias release with rollback; Perform a managed EKS Deployment rollout; Perform an EC2 blue/green deployment with CodeDeploy; Perform cleanup after supplied-script failure; Reconcile Terraform EC2 drift; directly require the native EC2 instance foundation; Rehearsal isolation; Reuse a supplied Terraform module provisioning EC2; directly require the n

## LESSON, in learner order

### s01 · explainer · Renew identity, inspect outcomes
Explain — 
(mechanism) Expired temporary credentials are no longer usable. Renew the approved session through its credential provider and use the new access key, secret key and session token together. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3⟧
(mechanism) Before retrying a resource-changing request, inspect its known outcome. Where the supplied operation supports an idempotency token, use it to avoid duplicate effects. Renewed credentials alone do not settle the earlier request’s outcome. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3⟧
[PROCESS_FLOW: Expired identity and safe retry are separate checks] nodes=['Expired session', 'Renew through approved provider', 'New access key + secret key + token', 'Inspect original operation outcome', 'Known completed: do not repeat merely due to expiry', 'Retry warranted: supported idempotency token where available'] edges=[('n0', 'n1', 'replace'), ('n1', 'n2', 'use together'), ('n2', 'n3', 'before mutation retry'), ('n3', 'n4', 'completed'), ('n3', 'n5', 'after outcome inspection')] alt: Expired identity and safe retry are separate checks. Expired session; Renew through approved provider; New access key + secret key + token; Inspect original operation outcome; Known completed: do not repeat merely due to expiry; Retry warranted: supported idempotency token where available

### s02 · explainer · Inspect the evidence and the contrast
Worked review — 
(example) Replace the expired credential set through the approved provider, keeping the new access key, secret key and token together. For a mutation, record whether the original request is known to have taken effect before considering a repeat. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧
(example) Compare a known completed mutation with an unresolved result. Neither case makes expired credentials usable again, but completion is not a reason to repeat the mutation. For an unresolved case, inspect available outcome evidence before retrying and use supported idempotency where available. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · check · Check renew identity, inspect outcomes
Knowledge check — Choose the interpretation supported by the supplied evidence.

### s04 · hands_on · Review identity renewal and outcomes
Evidence judgement — Read the supplied excerpts in this step and decide which interpretations or proposed actions are correct, defective or unsafe.

### s05 · recap · Keep the evidence boundaries clear
(takeaway) Renew the entire credential set, then inspect mutation outcomes before considering retries. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Separate ECS role responsibilities: Continue to aws_devops.tile.081.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit renew identity, inspect outcomes
(mechanism) Temporary credentials stop being usable after expiration and must be replaced with a newly authorized session. ⟦A.f1 A:tb2 A:tb4⟧
(misconception) Contrast: renewing credentials restores a usable identity, not certainty about the earlier mutation. Inspect the outcome before retrying. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit renew identity, inspect outcomes
(mechanism) On an expired-session error, renew the approved session through its credential provider and use the new access key, secret key and token together. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Before retrying a resource-changing operation, inspect its known outcome and use a supported idempotency token where the supplied operation offers one to avoid duplicate effects. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast: renewing credentials restores a usable identity, not certainty about the earlier mutation. Inspect the outcome before retrying. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Separate ECS role responsibilities (aws_devops.tile.081)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws.ecs_task_identity — Ecs task identity

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws.ecs_task_identity)   objective: Configure ECS task identity
A.f1: The ECS task role supplies credentials for AWS calls made by the application containers.   [sources: aws_ecs_developer_guide#task-iam-roles.html]
A.f2: The task execution role authorizes ECS startup work such as pulling an image and publishing logs; it is distinct from application AWS permissions.   [sources: aws_ecs_developer_guide#task_execution_IAM_role.html]
A.f3: Set taskRoleArn to the approved least-privilege application role in the task definition and test allowed and denied application operations from the task.   [sources: aws_ecs_developer_guide#task-iam-roles.html]
note: Do not broaden startup permissions to cover application work; use approved roles.
PRACTICE ANCHOR (tool_simulation): Assign the approved least-privilege application role to taskRoleArn in a supplied ECS task definition, then run the supplied allowed and denied application operations from the task.  SUCCESS: taskRoleArn references the approved application role, the allowed application operation succeeds, and the denied application operation returns an access denial. The task execution role remains unchanged.
ASSESSMENT ANCHOR: distinguish_application_task_role_permissions_from_execution_role_startup_permissions facts=['f1', 'f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply an approved security baseline to sandbox accounts; Apply bounded EKS workload configuration and secrets after external configuration/secrets preparation; Approval stop; Configure CodePipeline source-to-deploy actions; directly require native IAM identity-policy evaluation and role trust for the service execution role, not pipeline federation; Credential readiness; Deploy a supplied CloudFormation S3 environment across accounts and Regions with assumed roles; directly require the native S3 object-storage concept; Diagnose AWS connectivity failures using prepared DNS, HTTP, ports and CIDR foundations; Execute an established fleet patch task after external package-management and shell preparation; Expose an EKS workload using a Kubernetes Service; Inject a controlled failure and verify alarm behavior; Perform a Lambda version-and-alias release with rollback; Perform a managed EKS Deployment rollout; Perform an EC2 blue/green deployment with CodeDeploy; Perform cleanup after supplied-script failure; Reconcile Terraform EC2 drift; directly require the native EC2 instance foundation; Rehearsal isolation; Reuse a supplied Terraform module provisioning EC2; directly require the nativ

## LESSON, in learner order

### s01 · explainer · Separate ECS role responsibilities
Explain — 
(mechanism) The ECS task role supplies credentials for application containers’ AWS calls. The task execution role instead authorizes startup work such as pulling images and publishing logs. These roles do not substitute for each other. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Set taskRoleArn in the task definition to the approved least-privilege application role. Test supplied allowed and denied application operations from the task, and associate results with that application identity. Successful startup work does not establish application AWS access. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[DIAGRAM: ECS has two permission paths] nodes=['Task execution role', 'Startup: image pulling / log publication', 'taskRoleArn → approved least-privilege task role', 'Application containers’ AWS calls', 'Allowed and denied application-operation tests'] edges=[('n0', 'n1', 'startup authority'), ('n2', 'n3', 'application credentials'), ('n3', 'n4', 'verify application identity')] alt: ECS has two permission paths. Task execution role; Startup: image pulling / log publication; taskRoleArn → approved least-privilege task role; Application containers’ AWS calls; Allowed and denied application-operation tests

### s02 · check · Check separate ecs role responsibilities
Knowledge check — Choose the interpretation supported by the supplied evidence.

### s03 · hands_on · Review ECS role responsibilities
Evidence judgement — Read the supplied excerpts in this step and decide which interpretations or proposed actions are correct, defective or unsafe.

### s04 · recap · Keep the evidence boundaries clear
(takeaway) Task execution authority is not application authority; verify allowed and denied task-role operations. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Verify each baseline control: Continue to aws_devops.tile.082.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit separate ecs role responsibilities
(mechanism) The ECS task role supplies credentials for AWS calls made by the application containers. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) The task execution role authorizes ECS startup work such as pulling an image and publishing logs; it is distinct from application AWS permissions. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast: image pulling and log publication concern startup authority, not application AWS permissions under taskRoleArn. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Verify each baseline control (aws_devops.tile.082)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.apply_an_approved_security_baseline_to_sandbox_accounts — Apply an approved security baseline to sandbox accounts

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.apply_an_approved_security_baseline_to_sandbox_accounts)   objective: Apply an approved account security baseline
A.f1: A governed account baseline applies standardized organizational controls and configuration to accounts.   [sources: aws_control_tower_user_guide#how-controls-work.html]
A.f2: Apply the supplied approved control configuration to the sandbox account and inspect each stated control’s deployment or evaluation result.   [sources: aws_control_tower_user_guide#how-controls-work.html]
A.f3: Distinguish preventive controls that restrict actions from detective controls that report noncompliance when interpreting the baseline checks.   [sources: aws_control_tower_user_guide#how-controls-work.html]
note: Use supplied approved controls only; do not add organizational-policy behaviors absent from the brief.
PRACTICE ANCHOR (tool_simulation): Apply one supplied approved baseline to the designated sandbox account, inspect every stated control's deployment or evaluation result, and record the control-check results.  SUCCESS: The supplied approved configuration is applied to the designated sandbox account. Every stated control has a recorded deployment or evaluation result, with preventive controls interpreted as action restrictions and detective controls interpreted as noncompliance reporting. No additional controls are introduced.
ASSESSMENT ANCHOR: verify_stated_baseline_controls_in_a_sandbox_account facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_preventive_restrictions_from_detective_noncompliance_results facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply bounded EKS workload configuration and secrets after external configuration/secrets preparation; Approval stop; Audit evidence; Configure CodePipeline source-to-deploy actions; directly require native IAM identity-policy evaluation and role trust for the service execution role, not pipeline federation; Credential readiness; Deploy a supplied CloudFormation S3 environment across accounts and Regions with assumed roles; directly require the native S3 object-storage concept; Diagnose AWS connectivity failures using prepared DNS, HTTP, ports and CIDR foundations; Execute an established fleet patch task after external package-management and shell preparation; Expose an EKS workload using a Kubernetes Service; Inject a controlled failure and verify alarm behavior; Perform a Lambda version-and-alias release with rollback; Perform a managed EKS Deployment rollout; Perform an EC2 blue/green deployment with CodeDeploy; Perform cleanup after supplied-script failure; Reconcile Terraform EC2 drift; directly require the native EC2 instance foundation; Rehearsal isolation; Reuse a supplied Terraform module provisioning EC2; directly require the native EC2 instance foundation; Rightsize a re

## LESSON, in learner order

### s01 · explainer · Verify each baseline control
Explain — 
(mechanism) A governed account baseline applies standardized organizational controls and configuration. Apply the supplied approved configuration to the sandbox account and inspect each stated control’s deployment or evaluation result. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Preventive controls restrict actions; detective controls report noncompliance. Record those different checkpoints by control. A detective report is not a preventive restriction, and configuration presence is not verification of every control’s result. This is an established baseline, not a task to design new controls. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[DIAGRAM: Illustrative fictional baseline checkpoint case — not actual AWS execution] nodes=['Sandbox account: 111111111111', 'Approved baseline: applied', 'Supplied preventive control A: deployment verified; restricts the stated action', 'Supplied detective control B: evaluation reports noncompliance; does not itself restrict the action', 'Verification record: retain each control’s separate result'] edges=[('n1', 'n0', 'apply approved baseline'), ('n0', 'n2', 'inspect checkpoint'), ('n0', 'n3', 'inspect checkpoint'), ('n2', 'n4', 'retain result'), ('n3', 'n4', 'retain result')] alt: Illustrative fictional baseline checkpoint case — not actual AWS execution. Sandbox account: 111111111111; Approved baseline: applied; Supplied preventive control A: deployment verified; restricts the stated action; Supplied detective control B: evaluation reports noncompliance; does not itself restrict the action; Verification record: retain each control’s separate result

### s02 · check · Check verify each baseline control
Knowledge check — Choose the interpretation supported by the supplied evidence.

### s03 · hands_on · Review each baseline control
Evidence judgement — Read the supplied excerpts in this step and decide which interpretations or proposed actions are correct, defective or unsafe.

### s04 · recap · Keep the evidence boundaries clear
(takeaway) Inspect each approved baseline checkpoint; preventive restrictions and detective reports are different results. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Reference configuration safely: Continue to aws_devops.tile.083.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit verify each baseline control
(mechanism) Distinguish preventive controls that restrict actions from detective controls that report noncompliance when interpreting the baseline checks. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast: preventive controls restrict actions; detective controls report noncompliance. Configuration presence is not a per-control result. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit verify each baseline control
(mechanism) A governed account baseline applies standardized organizational controls and configuration to accounts. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Apply the supplied approved control configuration to the sandbox account and inspect each stated control’s deployment or evaluation result. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Distinguish preventive controls that restrict actions from detective controls that report noncompliance when interpreting the baseline checks. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast: preventive controls restrict actions; detective controls report noncompliance. Configuration presence is not a per-control result. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Reference configuration safely (aws_devops.tile.083)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.apply_bounded_eks_workload_configuration_and_secrets — Apply bounded EKS workload configuration and secrets after external configuration/secrets preparation

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.apply_bounded_eks_workload_configuration_and_secrets)   objective: Inject configuration into an EKS workload
A.f1: A ConfigMap supplies nonconfidential configuration separately from the container image.   [sources: kubernetes_overview#../../tasks/configure-pod-container/configure-pod-configmap/]
A.f2: Reference a ConfigMap with envFrom.configMapRef or env.valueFrom.configMapKeyRef in the supplied Pod template.   [sources: kubernetes_overview#../../tasks/configure-pod-container/configure-pod-configmap/]
A.f3: Reference a Secret with env.valueFrom.secretKeyRef or a secret-backed volume and test the consuming workload without printing the secret values.   [sources: kubernetes_overview#../configuration/secret/]
A.f4: Secrets require access control and appropriate storage protection; base64 encoding is not encryption.   [sources: kubernetes_overview#../configuration/secret/]
A.m1 (misconception): Environment variables populated from a ConfigMap do not automatically update inside already-running containers when the ConfigMap changes.   [sources: kubernetes_overview#../../tasks/configure-pod-container/configure-pod-configmap/#mounted-configmaps-are-updated-automatically]
note: Use supplied configuration/secret objects; avoid secret display and untaught rollout/update procedures.
PRACTICE ANCHOR (live_code): Configure the supplied Deployment's Pod template with references to the supplied ConfigMap and Secret, then use the supplied safe consumer check to verify consumption without displaying secret values.  SUCCESS: The Pod template references the intended ConfigMap and Secret names and keys, and the supplied consumer check confirms successful consumption without exposing secret values.
ASSESSMENT ANCHOR: verify_nonconfidential_configmap_references facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_secret_consumption_without_exposing_values facts=['f3']
ASSESSMENT ANCHOR: distinguish_secret_encoding_from_required_protection facts=['f4']
ASSESSMENT ANCHOR: recognize_running_container_environment_update_limits facts=['m1']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Approval stop; Audit evidence; Audit evidence integrity; Configure CodePipeline source-to-deploy actions; directly require native IAM identity-policy evaluation and role trust for the service execution role, not pipeline federation; Credential readiness; Deploy a supplied CloudFormation S3 environment across accounts and Regions with assumed roles; directly require the native S3 object-storage concept; Diagnose AWS connectivity failures using prepared DNS, HTTP, ports and CIDR foundations; Execute an established fleet patch task after external package-management and shell preparation; Expose an EKS workload using a Kubernetes Service; Inject a controlled failure and verify alarm behavior; Perform a Lambda version-and-alias release with rollback; Perform a managed EKS Deployment rollout; Perform an EC2 blue/green deployment with CodeDeploy; Perform cleanup after supplied-script failure; Reconcile Terraform EC2 drift; directly require the native EC2 instance foundation; Rehearsal isolation; Reuse a supplied Terraform module provisioning EC2; directly require the native EC2 instance foundation; Rightsize a resource using a supplied workload baseline; Route a security finding with evid

## LESSON, in learner order

### s01 · explainer · Reference configuration safely
Explain — 
(mechanism) A ConfigMap supplies nonconfidential configuration separately from the container image. In the Pod template, use envFrom.configMapRef or env.valueFrom.configMapKeyRef. Reference a Secret with env.valueFrom.secretKeyRef or a secret-backed volume; test the consumer without printing secret values. Secrets need access control and appropriate storage protection: base64 encoding is not encryption. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3⟧
[CODE bash]
# Illustrative YAML Deployment Pod-template excerpt; no secret value
spec:
  template:
    spec:
      containers:
        - name: supplied-consumer
          env: [{name: APP_MODE, valueFrom: {configMapKeyRef: {name: supplied-config, key: mode}}}, {name: APP_TOKEN, valueFrom: {secretKeyRef: {name: supplied-secret, key: token}}}]
  annotations: ['APP_MODE ← supplied-config / mode: nonconfidential configuration', 'APP_TOKEN ← supplied-secret / token: value hidden; test the consumer without printing it']

### s02 · explainer · Inspect the evidence and the contrast
Worked review — 
(example) Check the intended ConfigMap and Secret references in the supplied Pod template, then test the consuming workload without exposing secret values. Nonconfidential configuration belongs in the ConfigMap; the Secret still needs access control and storage protection. ⟦A.f1 A.f2 A.f3 A.f4 A.m1 A:tb4 A:tb5 A:tb6⟧
(example) A ConfigMap change does not automatically update ConfigMap-backed environment variables inside already-running containers. Tie consumer evidence to the actual references and running consumer rather than assuming the updated ConfigMap alone proves a change. Base64 encoding is not encryption. ⟦A.f1 A.f2 A.f3 A.f4 A.m1 A:tb4 A:tb5 A:tb6⟧

### s03 · check · Check reference configuration safely
Knowledge check — Choose the interpretation supported by the supplied evidence.

### s04 · check · Check reference configuration safely
Knowledge check — Choose the interpretation supported by the supplied evidence.

### s05 · hands_on · Review configuration references safely
Evidence judgement — Read the supplied excerpts in this step and decide which interpretations or proposed actions are correct, defective or unsafe.

### s06 · recap · Keep the evidence boundaries clear
(takeaway) Use intended configuration and secret references, protect secret values, and test the consumer without assuming environment variables refresh. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
[UP NEXT] Up next: Trace the intended pipeline revision: Continue to aws_devops.tile.084.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit reference configuration safely
(mechanism) Secrets require access control and appropriate storage protection; base64 encoding is not encryption. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast: base64 encoding is not encryption; a Secret still needs access control and appropriate storage protection. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit reference configuration safely
(mechanism) Environment variables populated from a ConfigMap do not automatically update inside already-running containers when the ConfigMap changes. ⟦A.m1 A:tb4 A:tb5 A:tb6⟧
(misconception) Contrast: an updated ConfigMap is not proof that environment variables inside an already-running container have changed automatically. ⟦A.m1 A:tb4 A:tb5 A:tb6⟧
### r03 · Revisit reference configuration safely
(mechanism) A ConfigMap supplies nonconfidential configuration separately from the container image. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Reference a ConfigMap with envFrom.configMapRef or env.valueFrom.configMapKeyRef in the supplied Pod template. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) Reference a Secret with env.valueFrom.secretKeyRef or a secret-backed volume and test the consuming workload without printing the secret values. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) Contrast: a configuration or Secret reference is not the consumer test. Check intended references and test the workload without printing secret values. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4⟧

=========

# EVALUATOR PACKET — Trace the intended pipeline revision (aws_devops.tile.084)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.configure_codepipeline_source_to_deploy_actions — Configure CodePipeline source-to-deploy actions; directly require native IAM identity-policy evaluation and role trust for the service execution role, not pipeline federation

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.configure_codepipeline_source_to_deploy_actions)   objective: Configure CodePipeline source-to-deploy actions
A.f1: A pipeline has stages containing actions that pass declared input and output artifacts between source, build and deployment operations.   [sources: aws_codepipeline_user_guide#concepts-how-it-works.html]
A.f2: Configure source output, CodeBuild input/output and CodeDeploy input artifact names so each action receives the intended revision’s output.   [sources: aws_codepipeline_user_guide#welcome-introducing-artifacts.html]
A.f3: The CodePipeline service role requires trust for codepipeline.amazonaws.com and permissions for its actions and artifact access; this service role is not GitHub OIDC federation.   [sources: aws_codepipeline_user_guide#pipelines-create-service-role.html]
A.f4: Verify action execution evidence carries the intended source revision through deployment and a failed action prevents normal progression to dependent actions.   [sources: aws_codepipeline_user_guide#concepts-how-it-works.html]
note: Use supplied action structure and roles; do not introduce Jenkins/GitLab or independent application builds.
PRACTICE ANCHOR (tool_simulation): Configure the supplied source, CodeBuild build and CodeDeploy EC2 deployment actions in a CodePipeline simulation. Connect their declared artifact names and select the supplied service execution role after checking its service trust and action/artifact permissions.  SUCCESS: Source output matches CodeBuild input, and CodeBuild output matches CodeDeploy input. The selected role trusts codepipeline.amazonaws.com and permits the supplied actions and artifact access. Execution evidence links the intended source revision to deployment; the supplied failed-action case shows no normal progression to dependent actions.
ASSESSMENT ANCHOR: verify_source_revision_artifact_continuity_through_deployment facts=['f1', 'f2', 'f4']
ASSESSMENT ANCHOR: verify_codepipeline_service_role_trust_and_permissions facts=['f3']
ASSESSMENT ANCHOR: verify_failed_action_stops_dependent_action_progression facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Approval stop; Audit evidence; Audit evidence integrity; Audit storage retention; Credential readiness; Deploy a supplied CloudFormation S3 environment across accounts and Regions with assumed roles; directly require the native S3 object-storage concept; Diagnose AWS connectivity failures using prepared DNS, HTTP, ports and CIDR foundations; Execute an established fleet patch task after external package-management and shell preparation; Expose an EKS workload using a Kubernetes Service; Inject a controlled failure and verify alarm behavior; Perform a Lambda version-and-alias release with rollback; Perform a managed EKS Deployment rollout; Perform an EC2 blue/green deployment with CodeDeploy; Perform cleanup after supplied-script failure; Reconcile Terraform EC2 drift; directly require the native EC2 instance foundation; Rehearsal isolation; Reuse a supplied Terraform module provisioning EC2; directly require the native EC2 instance foundation; Rightsize a resource using a supplied workload baseline; Route a security finding with evidence to its responsible owner; Route an operational event to a notification or established Systems Manager action; Run an ECS service with a desired ta

## LESSON, in learner order

### s01 · explainer · Trace the intended pipeline revision
Explain — 
(mechanism) Pipeline stages contain actions that pass declared input and output artifacts. Connect source output to CodeBuild input, and CodeBuild output to CodeDeploy input, for the intended revision. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3⟧
(mechanism) The CodePipeline service role needs trust for codepipeline.amazonaws.com and action/artifact permissions; it is not GitHub OIDC federation. Verify the intended revision through deployment evidence. A failed action prevents normal progression to dependent actions. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3⟧
[PROCESS_FLOW: Stage/action artifact continuity] nodes=['Source action: intended revision / declared output', 'CodeBuild action: matching input / declared output', 'CodeDeploy action: matching input / revision evidence', 'Service role: codepipeline.amazonaws.com trust + action/artifact permissions', 'Failed action: dependent progression stops'] edges=[('n0', 'n1', 'source output = build input'), ('n1', 'n2', 'build output = deploy input'), ('n3', 'n0', 'service authority'), ('n3', 'n1', 'service authority'), ('n3', 'n2', 'service authority'), ('n1', 'n4', 'failure case')] alt: Stage/action artifact continuity. Source action: intended revision / declared output; CodeBuild action: matching input / declared output; CodeDeploy action: matching input / revision evidence; Service role: codepipeline.amazonaws.com trust + action/artifact permissions; Failed action: dependent progression stops

### s02 · explainer · Inspect the evidence and the contrast
Worked review — 
(example) Compare source output names with CodeBuild input names, then build output names with CodeDeploy input names. A stage list alone does not prove artifact continuity. Inspect the service role’s trust for codepipeline.amazonaws.com and required action/artifact permissions, not GitHub OIDC trust. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧
(example) Follow execution evidence for the intended source revision through deployment. In the failure case, check that the failed action stops normal progression to dependent actions. Success on a different input is not evidence for the intended release. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Check trace the intended pipeline revision
Knowledge check — Choose the interpretation supported by the supplied evidence.

### s04 · hands_on · Review the intended pipeline revision
Evidence judgement — Read the supplied excerpts in this step and decide which interpretations or proposed actions are correct, defective or unsafe.

### s05 · recap · Keep the evidence boundaries clear
(takeaway) Link declared artifacts, verify service-role authority and trace revision evidence; failed actions stop dependent progression. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Verify every account and Region: Continue to aws_devops.tile.085.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit trace the intended pipeline revision
(mechanism) Verify action execution evidence carries the intended source revision through deployment and a failed action prevents normal progression to dependent actions. ⟦A.f4 A:tb3 A:tb4⟧
(misconception) Contrast: a stage list is not artifact continuity. Compare linked artifact names and intended revision evidence, with failures stopping dependent progression. ⟦A.f1 A.f2 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit trace the intended pipeline revision
(mechanism) A pipeline has stages containing actions that pass declared input and output artifacts between source, build and deployment operations. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Configure source output, CodeBuild input/output and CodeDeploy input artifact names so each action receives the intended revision’s output. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) The CodePipeline service role requires trust for codepipeline.amazonaws.com and permissions for its actions and artifact access; this service role is not GitHub OIDC federation. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(mechanism) Verify action execution evidence carries the intended source revision through deployment and a failed action prevents normal progression to dependent actions. ⟦A.f4 A:tb3 A:tb4⟧
(misconception) Contrast: a stage list is not artifact continuity. Compare linked artifact names and intended revision evidence, with failures stopping dependent progression. ⟦A.f1 A.f2 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Verify every account and Region (aws_devops.tile.085)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.deploy_a_supplied_cloudformation_s3_environment_across_accounts_and_regions_with_assumed_roles — Deploy a supplied CloudFormation S3 environment across accounts and Regions with assumed roles; directly require the native S3 object-storage concept

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.deploy_a_supplied_cloudformation_s3_environment_across_accounts_and_regions_with_assumed_roles)   objective: Deploy a supplied CloudFormation S3 environment across accounts and Regions
A.f1: The same CloudFormation template can provision equivalent resource declarations in multiple approved target environments.   [sources: aws_cloudformation_user_guide#Welcome.html#welcome-quickly-replicate-your-infrastructure]
A.f2: For each approved account/Region pair, use a named role profile with role_arn and source_profile, verify its caller with aws sts get-caller-identity --profile NAME, and create the supplied stack with that profile and explicit --region REGION.   [sources: aws_cli_user_guide#cli-configure-role.html]
A.f3: Inspect stack outputs and S3 bucket identity and location in every intended target and check the supplied unapproved targets received no stack.   [sources: aws_cloudformation_user_guide#cfn-console-view-stack-data-resources.html]
note: Deploy the same supplied template; do not design new cross-account infrastructure or target discovery.
PRACTICE ANCHOR (tool_simulation): Deploy the same supplied CloudFormation S3 template to exactly two approved sandbox account/Region pairs. Use each target's named role profile configured with role_arn and source_profile, verify its caller with aws sts get-caller-identity --profile NAME, and create the stack with that profile and explicit --region REGION. Inspect each stack's outputs and bucket identity and location, then check the supplied unapproved targets for absence of the stack.  SUCCESS: A per-target record confirms that both approved targets have the expected caller account, successfully created stacks, and S3 bucket identities and locations matching their stack outputs and approved Regions. Checks of every supplied unapproved target confirm that no deployment stack is present; an access error does not count as proof of absence.
ASSESSMENT ANCHOR: verify_template_deployment_targets_and_assumed_callers facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_per_target_stack_and_bucket_identity facts=['f3']
ASSESSMENT ANCHOR: verify_no_stack_in_supplied_unapproved_targets facts=['f3']

## DATA ASSETS USED
ds.account_region_deployments: Per-target CloudFormation S3 evidence — columns: target_id(identifier), account_id(identifier,digits-as-label), region(categorical), approved(categorical), role_profile(identifier), role_arn(identifier), source_profile(identifier), verified_caller_account(identifier,digits-as-label), explicit_region(categorical), stack_name(identifier), stack_status(categorical), stack_output_bucket(identifier), observed_bucket_identity(identifier), observed_bucket_location(categorical), absence_check_result(categorical)
   ["approved-1",111111111111,"us-east-1",true,"sandbox-east","arn:aws:iam::111111111111:role/SandboxDeployment","sandbox-source",111111111111,"us-east-1","sandbox-audit","CREATE_COMPLETE","sandbox-audit-111111111111-us-east-1","sandbox-audit-111111111111-us-east-1","us-east-1","not applicable: approve
   ["approved-2",222222222222,"us-west-2",true,"sandbox-west","arn:aws:iam::222222222222:role/SandboxDeployment","sandbox-source",222222222222,"us-west-2","sandbox-audit","CREATE_COMPLETE","sandbox-audit-222222222222-us-west-2","sandbox-audit-222222222222-us-west-2","us-west-2","not applicable: approve
   ["unapproved-1",333333333333,"us-east-1",false,null,null,null,null,null,"sandbox-audit","ABSENT",null,null,null,"confirmed absent"]
   ["unapproved-2",333333333333,"us-west-2",false,null,null,null,null,null,"sandbox-audit","ABSENT",null,null,null,"confirmed absent"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Approval stop; Audit evidence; Audit evidence integrity; Audit storage retention; Backend configuration; Credential readiness; Diagnose AWS connectivity failures using prepared DNS, HTTP, ports and CIDR foundations; Execute an established fleet patch task after external package-management and shell preparation; Expose an EKS workload using a Kubernetes Service; Inject a controlled failure and verify alarm behavior; Perform a Lambda version-and-alias release with rollback; Perform a managed EKS Deployment rollout; Perform an EC2 blue/green deployment with CodeDeploy; Perform cleanup after supplied-script failure; Reconcile Terraform EC2 drift; directly require the native EC2 instance foundation; Rehearsal isolation; Reuse a supplied Terraform module provisioning EC2; directly require the native EC2 instance foundation; Rightsize a resource using a supplied workload baseline; Route a security finding with evidence to its responsible owner; Route an operational event to a notification or established Systems Manager action; Run an ECS service with a desired task count; Run supplied unit and integration tests as blocking pipeline gates after external testing preparation; Safe teardown; 

## LESSON, in learner order

### s01 · explainer · Verify every account and Region
Explain — 
(mechanism) The same CloudFormation template can provision equivalent declarations in multiple approved environments. Each approved account/Region pair still needs its own verified deployment record. Use a named role profile with role_arn and source_profile; verify the caller with aws sts get-caller-identity --profile NAME. Create the supplied stack with that profile and explicit --region REGION. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Inspect stack outputs, S3 bucket identity and bucket location in every intended target. Separately check that supplied unapproved targets received no stack. One successful target does not prove the others; distinguish confirmed absence from a failed absence check. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.account_region_deployments cols=all ] caption: 

### s02 · check · Check verify every account and region
Knowledge check — Choose the interpretation supported by the supplied evidence.

### s03 · hands_on · Review each account/Region deployment
Evidence judgement — Read the supplied excerpts in this step and decide which interpretations or proposed actions are correct, defective or unsafe.

### s04 · recap · Keep the evidence boundaries clear
(takeaway) Verify caller, stack outputs and bucket location per approved target; separately confirm unapproved-target absence. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Localize the failing network layer: Continue to aws_devops.tile.086.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit verify every account and region
(mechanism) Inspect stack outputs and S3 bucket identity and location in every intended target and check the supplied unapproved targets received no stack. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast: equivalent template declarations are not one shared deployment result. Keep approved deployments and unapproved-target absence checks separate. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.account_region_deployments cols=all ] caption: 
### r02 · Revisit verify every account and region
(mechanism) The same CloudFormation template can provision equivalent resource declarations in multiple approved target environments. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) For each approved account/Region pair, use a named role profile with role_arn and source_profile, verify its caller with aws sts get-caller-identity --profile NAME, and create the supplied stack with that profile and explicit --region REGION. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Inspect stack outputs and S3 bucket identity and location in every intended target and check the supplied unapproved targets received no stack. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast: equivalent template declarations are not one shared deployment result. Keep approved deployments and unapproved-target absence checks separate. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.account_region_deployments cols=all ] caption: 

=========

# EVALUATOR PACKET — Localize the failing network layer (aws_devops.tile.086)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.diagnose_aws_connectivity_failures — Diagnose AWS connectivity failures using prepared DNS, HTTP, ports and CIDR foundations

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.diagnose_aws_connectivity_failures)   objective: Diagnose an AWS connectivity failure
A.f1: The subnet’s route table must contain a matching destination route to a usable target for the required network path.   [sources: aws_vpc_user_guide#VPC_Route_Tables.html]
A.f2: Check DNS resolution and the intended endpoint address using the supplied tools, then inspect route association, required protocol/port rules and response traffic to localize the failing layer.   [sources: aws_vpc_user_guide#vpc-security-groups.html]
A.f3: Network ACLs are stateless, so required requests and responses need permitted traffic in their respective directions.   [sources: aws_vpc_user_guide#vpc-network-acls.html]
A.f4: Make the approved correction supported by the failing layer’s evidence and repeat the endpoint connection test.   [sources: aws_vpc_user_guide#VPC_Route_Tables.html]
note: Require external networking preparation; do not add command syntax or control behaviors absent from allowed facts.
PRACTICE ANCHOR (tool_simulation): Resolve one seeded endpoint failure in a supplied sandbox topology using supplied DNS and connection tools, route-association evidence, and protocol/port and network-ACL rules. Apply only the approved correction supported by the failing layer's evidence.  SUCCESS: The learner identifies the broken layer from the supplied evidence, applies the approved correction without changing unrelated controls, and repeats the endpoint connection test to confirm that the connection succeeds.
ASSESSMENT ANCHOR: localize_a_failure_using_dns_endpoint_and_route_evidence facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_a_blocked_request_or_response_direction facts=['f2', 'f3']
ASSESSMENT ANCHOR: select_an_evidence_supported_correction_and_confirm_by_retesting facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Approval stop; Audit evidence; Audit evidence integrity; Audit storage retention; Backend configuration; Credential readiness; Execute an established fleet patch task after external package-management and shell preparation; Expose an EKS workload using a Kubernetes Service; Inject a controlled failure and verify alarm behavior; Perform a Lambda version-and-alias release with rollback; Perform a managed EKS Deployment rollout; Perform an EC2 blue/green deployment with CodeDeploy; Perform cleanup after supplied-script failure; Reconcile Terraform EC2 drift; directly require the native EC2 instance foundation; Rehearsal isolation; Replacement controls; Reuse a supplied Terraform module provisioning EC2; directly require the native EC2 instance foundation; Rightsize a resource using a supplied workload baseline; Route a security finding with evidence to its responsible owner; Route an operational event to a notification or established Systems Manager action; Run an ECS service with a desired task count; Run supplied unit and integration tests as blocking pipeline gates after external testing preparation; Safe teardown; Submit small reviewable infrastructure changes after registry Git a

## LESSON, in learner order

### s01 · explainer · Localize the failing network layer
Explain — 
(mechanism) A required path needs the subnet’s actual route-table association and a matching destination route to a usable target. Check DNS resolution and intended endpoint address, then inspect route association, required protocol/port rules and response traffic to locate the failing layer. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3⟧
(mechanism) Network ACLs are stateless: requests and responses need permission in their respective directions. Make only the approved correction supported by that layer’s evidence, then repeat the endpoint connection test. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3⟧
[DIAGRAM: Illustrative fictional endpoint path and correction] nodes=['DNS resolves to intended endpoint', 'Subnet uses route table A; matching route has a usable target', 'Required request traffic permitted', 'Required response traffic denied by network ACL — observed failing layer', 'Approved correction: permit the required response traffic', 'Repeated endpoint connection test: successful', 'Stateless network ACL: request and response directions require separate allowance'] edges=[('n0', 'n1', 'inspect path'), ('n1', 'n2', 'request →'), ('n2', 'n1', '← response: denied by network ACL (n3)'), ('n2', 'n3', 'inspect response evidence'), ('n3', 'n4', 'correct observed failing layer'), ('n4', 'n5', 'verify correction'), ('n6', 'n3', 'separate response allowance required')] alt: Illustrative fictional endpoint path and correction. DNS resolves to intended endpoint; Subnet uses route table A; matching route has a usable target; Required request traffic permitted; Required response traffic denied by network ACL — observed failing layer; Approved correction: permit the required response traffic; Repeated endpoint connection test: successful; Stateless network ACL: request and response directions require separate allowance

### s02 · explainer · Inspect the evidence and the contrast
Worked review — 
(example) Start with DNS resolution and the intended endpoint address. Inspect the used subnet route-table association, matching destination route and usable target, then protocol/port rules and response traffic. A connection symptom alone does not identify the failing layer. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧
(example) If the supplied evidence identifies a missing response allowance in a network ACL, use the approved correction for that layer. A permitted request direction is not sufficient for a stateless ACL. Retest the endpoint connection after correction rather than altering every control or accepting an edited route table as proof of the used path. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · video · Locate the operational evidence
[VIDEO ] bridge-before:  | bridge-after: 

### s04 · check · Check localize the failing network layer
Knowledge check — Choose the interpretation supported by the supplied evidence.

### s05 · hands_on · Review the failing network layer
Evidence judgement — Read the supplied excerpts in this step and decide which interpretations or proposed actions are correct, defective or unsafe.

### s06 · recap · Keep the evidence boundaries clear
(takeaway) Localize the failing layer, check request and response directions, make the approved correction and retest. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Preserve patch-task bounds: Continue to aws_devops.tile.087.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit localize the failing network layer
(mechanism) Check DNS resolution and the intended endpoint address using the supplied tools, then inspect route association, required protocol/port rules and response traffic to localize the failing layer. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Network ACLs are stateless, so required requests and responses need permitted traffic in their respective directions. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast: request permission alone is insufficient for a stateless ACL. Response-direction evidence and a repeated connection test matter too. ⟦A.f3 A.f4 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit localize the failing network layer
(mechanism) The subnet’s route table must contain a matching destination route to a usable target for the required network path. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Check DNS resolution and the intended endpoint address using the supplied tools, then inspect route association, required protocol/port rules and response traffic to localize the failing layer. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Make the approved correction supported by the failing layer’s evidence and repeat the endpoint connection test. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast: request permission alone is insufficient for a stateless ACL. Response-direction evidence and a repeated connection test matter too. ⟦A.f3 A.f4 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Preserve patch-task bounds (aws_devops.tile.087)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.execute_an_established_fleet_patch_task — Execute an established fleet patch task after external package-management and shell preparation

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.execute_an_established_fleet_patch_task)   objective: Execute an established fleet patch task
A.f1: Patch Manager uses patch baselines and managed-node targets to scan or install patches and report compliance.   [sources: aws_systems_manager_user_guide#patch-manager.html]
A.f2: Use the established maintenance-window task with the approved target set, patch document parameters, concurrency and error limits.   [sources: aws_systems_manager_user_guide#sysman-maintenance-assign-tasks.html]
A.f3: Inspect task execution and per-node patch compliance results to verify which approved instances were patched and which require follow-up.   [sources: aws_systems_manager_user_guide#patch-manager-view-compliance-results.html]
note: Require external Linux package-management and fleet preparation; use established patch tasks only.
PRACTICE ANCHOR (tool_simulation): Run one supplied maintenance-window patch task on a small sandbox fleet, retaining its approved targets, patch-document parameters, concurrency and error limits.  SUCCESS: The supplied task runs with its approved configuration unchanged. Execution recipients are compared with the approved target IDs, and execution evidence and per-node patch compliance results are used to record which instances were patched and which require follow-up.
ASSESSMENT ANCHOR: verify_task_recipients_against_approved_targets facts=['f2', 'f3']
ASSESSMENT ANCHOR: interpret_per_node_patch_results_and_compliance facts=['f1', 'f3']
ASSESSMENT ANCHOR: distinguish_patched_instances_from_instances_requiring_follow_up facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Approval stop; Audit evidence; Audit evidence integrity; Audit storage retention; Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template; directly require the native EC2 instance foundation; Backend configuration; Credential readiness; Expose an EKS workload using a Kubernetes Service; Inject a controlled failure and verify alarm behavior; Perform a Lambda version-and-alias release with rollback; Perform a managed EKS Deployment rollout; Perform an EC2 blue/green deployment with CodeDeploy; Perform cleanup after supplied-script failure; Reconcile Terraform EC2 drift; directly require the native EC2 instance foundation; Rehearsal isolation; Replacement controls; Reuse a supplied Terraform module provisioning EC2; directly require the native EC2 instance foundation; Rightsize a resource using a supplied workload baseline; Route a security finding with evidence to its responsible owner; Route an operational event to a notification or established Systems Manager action; Run an ECS service with a desired task count; Run supplied unit and integration tests as blocking pipeline gates after external testing preparation; Safe teardown; Submit small reviewa

## LESSON, in learner order

### s01 · explainer · Preserve patch-task bounds
Explain — 
(mechanism) Patch Manager uses patch baselines and managed-node targets to scan or install patches and report compliance. Use the established maintenance-window task with approved targets, patch document parameters, concurrency and error limits. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Inspect task execution and per-node patch compliance to identify which approved instances were patched and which need follow-up. Keep node identity with its result. A maintenance-window summary does not replace per-node evidence or justify changing the approved task bounds. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[DIAGRAM: Separate illustrative fictional patch case — not command-review] nodes=['Approved targets: node A, node B', 'Document operation: Install', 'Concurrency: 1; Error limit: 1', 'Execution recipients: node A, node B', 'node A: install completed; compliance verified; patched', 'node B: execution failed; compliance not verified; follow-up required'] edges=[('n0', 'n1', 'preserve scope'), ('n1', 'n2', 'preserve bounds'), ('n2', 'n3', 'inspect recipients'), ('n3', 'n4', 'node A → its execution and compliance evidence'), ('n3', 'n5', 'node B → its execution and compliance evidence')] alt: Separate illustrative fictional patch case — not command-review. Approved targets: node A, node B; Document operation: Install; Concurrency: 1; Error limit: 1; Execution recipients: node A, node B; node A: install completed; compliance verified; patched; node B: execution failed; compliance not verified; follow-up required

### s02 · video · Locate the operational evidence
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Check preserve patch-task bounds
Knowledge check — Choose the interpretation supported by the supplied evidence.

### s04 · hands_on · Review patch-task bounds
Evidence judgement — Read the supplied excerpts in this step and decide which interpretations or proposed actions are correct, defective or unsafe.

### s05 · recap · Keep the evidence boundaries clear
(takeaway) Preserve approved task bounds and inspect each node’s execution and patch-compliance evidence. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Verify the Service traffic path: Continue to aws_devops.tile.088.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit preserve patch-task bounds
(mechanism) Inspect task execution and per-node patch compliance results to verify which approved instances were patched and which require follow-up. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast: an overall task label does not establish each approved node’s patch outcome. Keep per-node compliance and follow-up evidence. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit preserve patch-task bounds
(mechanism) Patch Manager uses patch baselines and managed-node targets to scan or install patches and report compliance. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Use the established maintenance-window task with the approved target set, patch document parameters, concurrency and error limits. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Inspect task execution and per-node patch compliance results to verify which approved instances were patched and which require follow-up. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast: an overall task label does not establish each approved node’s patch outcome. Keep per-node compliance and follow-up evidence. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Verify the Service traffic path (aws_devops.tile.088)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.expose_an_eks_workload_using_a_kubernetes_service — Expose an EKS workload using a Kubernetes Service

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.expose_an_eks_workload_using_a_kubernetes_service)   objective: Expose an EKS workload through a Service
A.f1: A Kubernetes Service provides a stable network endpoint for a changing set of selected Pods.   [sources: kubernetes_overview#../services-networking/service/]
A.f2: Set spec.selector to match the intended Pod labels and ports.port and ports.targetPort to map the Service port to the application’s container port.   [sources: kubernetes_overview#../services-networking/service/]
A.f3: Apply the supplied Service, inspect its EndpointSlices or endpoints and test the Service address from the supplied client to verify selected Pods receive traffic.   [sources: kubernetes_overview#../services-networking/service/]
note: Use supplied apply/access procedure; do not introduce cluster networking administration or unsupported Service types.
PRACTICE ANCHOR (tool_simulation): Create one Service for the supplied Deployment using the supplied access and apply procedure. Match its selector to the intended Pod labels, map the Service port to the application's container port, inspect EndpointSlices or endpoints, and test the Service address from the supplied client.  SUCCESS: The applied Service selects the intended Pods and maps its port to the application's container port. EndpointSlice or endpoint evidence identifies those Pods, and the supplied client receives the expected application response through the Service address.
ASSESSMENT ANCHOR: explain_stable_service_endpoint_for_changing_pods facts=['f1']
ASSESSMENT ANCHOR: verify_service_selector_and_port_mapping facts=['f2']
ASSESSMENT ANCHOR: verify_intended_pods_receive_service_traffic facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Approval stop; Audit evidence; Audit evidence integrity; Audit storage retention; Automate isolated infrastructure restoration using a supplied CloudFormation EC2 template; directly require the native EC2 instance foundation; Backend configuration; Block release on actionable dependency or image security findings; Credential readiness; Inject a controlled failure and verify alarm behavior; Perform a Lambda version-and-alias release with rollback; Perform a managed EKS Deployment rollout; Perform an EC2 blue/green deployment with CodeDeploy; Perform cleanup after supplied-script failure; Reconcile Terraform EC2 drift; directly require the native EC2 instance foundation; Rehearsal isolation; Replacement controls; Reuse a supplied Terraform module provisioning EC2; directly require the native EC2 instance foundation; Rightsize a resource using a supplied workload baseline; Route a security finding with evidence to its responsible owner; Route an operational event to a notification or established Systems Manager action; Run an ECS service with a desired task count; Run supplied unit and integration tests as blocking pipeline gates after external testing preparation; Safe teardown; Subm

## LESSON, in learner order

### s01 · explainer · Verify the Service traffic path
Explain — 
(mechanism) A Kubernetes Service provides a stable network endpoint for a changing set of selected Pods. Match spec.selector to intended Pod labels, and map ports.port through ports.targetPort to the application’s container port. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Apply the supplied Service, inspect EndpointSlices or endpoints, and test its address from the supplied client. Keep selector, port mapping, endpoint evidence and client result together to verify selected Pods receive traffic. A Service object’s name or declaration alone is not proof of application reachability. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[DIAGRAM: Stable Service endpoint, verified selected Pods] nodes=['Supplied client', 'Stable Service address / ports.port', 'spec.selector ↔ intended Pod labels', 'EndpointSlices or endpoints', 'Selected Pods / application container port', 'ports.targetPort', 'Client connection result'] edges=[('n0', 'n1', 'request'), ('n2', 'n3', 'verify selected endpoints'), ('n1', 'n5', 'port mapping'), ('n5', 'n4', 'application port'), ('n3', 'n4', 'endpoint evidence'), ('n4', 'n6', 'verify selected Pods receive traffic')] alt: Stable Service endpoint, verified selected Pods. Supplied client; Stable Service address / ports.port; spec.selector ↔ intended Pod labels; EndpointSlices or endpoints; Selected Pods / application container port; ports.targetPort; Client connection result

### s02 · check · Check verify the service traffic path
Knowledge check — Choose the interpretation supported by the supplied evidence.

### s03 · hands_on · Review the service traffic path
Evidence judgement — Read the supplied excerpts in this step and decide which interpretations or proposed actions are correct, defective or unsafe.

### s04 · recap · Keep the evidence boundaries clear
(takeaway) Verify selector and port mapping with endpoint evidence and the supplied-client result. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Inject a controlled failure and verify alarm behavior: Continue to aws_devops.tile.089.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit verify the service traffic path
(mechanism) Apply the supplied Service, inspect its EndpointSlices or endpoints and test the Service address from the supplied client to verify selected Pods receive traffic. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast: a Service declaration is not a traffic test. Selector, targetPort, observed endpoints and supplied-client results must agree. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit verify the service traffic path
(mechanism) A Kubernetes Service provides a stable network endpoint for a changing set of selected Pods. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Set spec.selector to match the intended Pod labels and ports.port and ports.targetPort to map the Service port to the application’s container port. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Apply the supplied Service, inspect its EndpointSlices or endpoints and test the Service address from the supplied client to verify selected Pods receive traffic. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast: a Service declaration is not a traffic test. Selector, targetPort, observed endpoints and supplied-client results must agree. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧