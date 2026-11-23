# EVALUATOR PACKET — Input target validation (aws_devops.tile.015)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = automation.input_target_validation — Input target validation

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (automation.input_target_validation)   objective: Validate automation inputs and targets using the supplied Python wrapper's environment-variable validation configuration
A.f1: Process environment variables provide named string values that a supplied program can read as configuration.   [sources: python_tutorial#../library/os.html#os.environ]
A.f2: Set the supplied allowlist environment variable FLEET_ALLOWED_INSTANCE_IDS to the approved comma-separated IDs and the supplied FLEET_MAX_TARGETS variable to the approved positive integer limit; these are configuration inputs to the supplied validator, not Python language keywords.   [sources: python_tutorial#../library/os.html#os.environ]
A.f3: Exercise malformed and out-of-scope inputs and check the supplied validator rejects them before invoking a resource-changing operation.   [sources: aws_well_architected_framework#ops03-bp02.html]
note: Use the supplied validator; do not author general-purpose Bash control flow or new Python parsing logic.
PRACTICE ANCHOR (tool_simulation): Set FLEET_ALLOWED_INSTANCE_IDS to the supplied approved comma-separated instance IDs and FLEET_MAX_TARGETS to the supplied approved positive integer limit in the fleet-command wrapper's environment-variable configuration. Run the supplied malformed-input and out-of-scope-target verification commands without modifying Python or Bash code.  SUCCESS: Both configuration values match the supplied approval. The supplied validator rejects the malformed-input and out-of-scope-target cases, and the supplied operation evidence confirms that neither case invokes a resource-changing operation.
ASSESSMENT ANCHOR: configure_approved_target_scope_and_limit facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_malformed_input_rejection_before_mutation facts=['f3']
ASSESSMENT ANCHOR: verify_out_of_scope_target_rejection_before_mutation facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute an AWS change using CloudTrail evidence; Attribute workload spend using resource tags; Centralize structured application logs in CloudWatch Logs; Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation; Choose rolling, blue/green or canary delivery for stated availability and rollback requirements; Cloudformation change sets; Collect host telemetry with the CloudWatch agent; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure role trust; directly require native IAM identity-policy evaluation; Configure secure human access with temporary credentials; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Evaluate resource-based permissions for a requested operation; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute an established managed account-onboarding workflow; Extract structured AWS CLI inventory across paginated results; Hand over an actionable 

## LESSON, in learner order

### s01 · explainer · Input target validation
Understand — 
(mechanism) Environment variables are named strings that a supplied program reads as configuration. ⟦A.f1 A:tb2⟧
(mechanism) Configure FLEET_ALLOWED_INSTANCE_IDS with approved comma-separated IDs and FLEET_MAX_TARGETS with the approved positive integer limit. These names configure the supplied validator; they are not Python keywords. ⟦A.f2 A:tb3⟧
(mechanism) Test malformed and out-of-scope inputs. Confirm rejection happens before any resource-changing operation. ⟦A.f3 A:tb3⟧
[DIAGRAM: Authored read-only example] nodes=['Approved scope {Approved IDs: i-00000000000000001, i-00000000000000002; maximum targets: 2}', "Environment configuration {FLEET_ALLOWED_INSTANCE_IDS = i-00000000000000001,i-00000000000000002; FLEET_MAX_TARGETS = '2'}", 'Rejection boundary {Malformed-input case: rejected; resource-changing calls: 0; Outside-allowlist case, i-00000000000000003: rejected; resource-changing calls: 0}'] edges=[] alt: Authored read-only example: Approved scope: Approved IDs: i-00000000000000001, i-00000000000000002; maximum targets: 2; Environment configuration: FLEET_ALLOWED_INSTANCE_IDS = i-00000000000000001,i-00000000000000002; FLEET_MAX_TARGETS = '2'; Rejection boundary: Malformed-input case: rejected; resource-changing calls: 0; Outside-allowlist case, i-00000000000000003: rejected; resource-changing calls: 0

### s02 · explainer · Compare the evidence, not the label
Apply the evidence — 
(example) For the approved two-ID, two-target example, keep the approval beside both environment-variable settings. Inspect the malformed-input and outside-allowlist cases together with operation evidence: both must be rejected before a resource-changing call. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) Setting configuration is not proof of enforcement: rejection evidence must precede resource changes. ⟦A.f2 A.f3 A:tb5⟧

### s03 · check · Judge the evidence
Check your understanding — Read the supplied case and choose the interpretation supported by its evidence.

### s04 · check · Judge the evidence
Check your understanding — Read the supplied case and choose the interpretation supported by its evidence.

### s05 · hands_on · Review Input target validation
Evidence review — Read the supplied excerpts in this step and decide which satisfy the stated requirements and which are defective or unsafe.

### s06 · recap · Keep the boundary clear
Takeaways — 
(takeaway) Environment variables configure the supplied validator. Match approved IDs and a positive target limit; verify malformed and out-of-scope rejection before resource changes. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] CloudFormation change sets: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Evidence versus assumption
(mechanism) Test malformed and out-of-scope inputs. Confirm rejection happens before any resource-changing operation. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Setting configuration is not proof of enforcement: rejection evidence must precede resource changes. ⟦A.f2 A.f3 A:tb5⟧
### r02 · Evidence versus assumption
(mechanism) Environment variables are named strings that a supplied program reads as configuration. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Configure FLEET_ALLOWED_INSTANCE_IDS with approved comma-separated IDs and FLEET_MAX_TARGETS with the approved positive integer limit. These names configure the supplied validator; they are not Python keywords. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) Setting configuration is not proof of enforcement: rejection evidence must precede resource changes. ⟦A.f2 A.f3 A:tb5⟧

=========

# EVALUATOR PACKET — CloudFormation change sets (aws_devops.tile.016)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws.cloudformation_change_sets — Cloudformation change sets

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws.cloudformation_change_sets)   objective: Preview CloudFormation EC2 changes with a change set
A.f1: A change set previews proposed stack resource changes without executing them.   [sources: aws_cloudformation_user_guide#using-cfn-updating-stacks-changesets.html]
A.f2: Review additions, modifications, removals and replacement indicators before authorizing execution; a preview does not guarantee that execution will succeed.   [sources: aws_cloudformation_user_guide#using-cfn-updating-stacks-changesets.html]
A.f3: For a new stack, create a CREATE change set from the supplied template, wait for creation to complete, inspect it, and execute the approved set to provision the resources.   [sources: aws_cloudformation_user_guide#using-cfn-updating-stacks-changesets-create.html]
note: Use the supplied template and approval path; leave rollback diagnosis to its dedicated concept.
PRACTICE ANCHOR (tool_simulation): Using the supplied template and approval path, create a CREATE change set for one sandbox EC2 instance, wait for change-set creation to complete, inspect the proposed actions, and execute the approved set. Then review a supplied update change set for unintended EC2 replacement before making an authorization decision.  SUCCESS: The CREATE change set is inspected before execution, its proposed additions match the approved scope, and execution of that specific approved set provisions one sandbox EC2 instance. The supplied update review identifies the EC2 action and its replacement indicator, withholding authorization if replacement is unintended. Review results and execution outcomes remain distinct; a successful preview is not treated as a guarantee of execution success.
ASSESSMENT ANCHOR: identify_proposed_ec2_additions_modifications_and_replacement_indicators facts=['f1', 'f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute an AWS change using CloudTrail evidence; Attribute workload spend using resource tags; Centralize structured application logs in CloudWatch Logs; Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation; Choose rolling, blue/green or canary delivery for stated availability and rollback requirements; Collect host telemetry with the CloudWatch agent; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure role trust; directly require native IAM identity-policy evaluation; Configure secure human access with temporary credentials; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Evaluate resource-based permissions for a requested operation; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute an established managed account-onboarding workflow; Extract structured AWS CLI inventory across paginated results; Hand over an actionable operational runbook; Mfa enf

## LESSON, in learner order

### s01 · explainer · CloudFormation change sets
Understand — 
(mechanism) A change set previews proposed stack changes without executing them. ⟦A.f1 A:tb2⟧
(mechanism) Before authorizing execution, review additions, modifications, removals and replacement indicators. A preview does not guarantee execution success. ⟦A.f2 A:tb3⟧
(mechanism) For a new stack, create a CREATE change set from the supplied template, wait for completion, inspect it, then execute the approved set to provision resources. ⟦A.f3 A:tb3⟧
[DIAGRAM: Authored read-only change-set evidence: CloudFormation change sets] nodes=['New-stack CREATE preview {New-stack change set: CREATE; creation status: CREATE_COMPLETE; OrdersHost: Add, AWS::EC2::Instance; execution: not yet authorized}', 'Separate execution action {Separate execution action: execute this specific set only after approval; preview does not provision resources or guarantee execution success}', 'Update preview review {Update change set: creation status CREATE_COMPLETE; OrdersHost: Modify, AWS::EC2::Instance; Replacement: True; execution: not authorized—review replacement against approved scope}'] edges=[] alt: Authored read-only change-set evidence: CloudFormation change sets: New-stack CREATE preview: New-stack change set: CREATE; creation status: CREATE_COMPLETE; OrdersHost: Add, AWS::EC2::Instance; execution: not yet authorized; Separate execution action: Separate execution action: execute this specific set only after approval; preview does not provision resources or guarantee execution success; Update preview review: Update change set: creation status CREATE_COMPLETE; OrdersHost: Modify, AWS::EC2::Instance; Replacement: True; execution: not authorized—review replacement against approved scope

### s02 · explainer · Compare the evidence, not the label
Apply the evidence — 
(example) For the supplied new-stack template, wait for CREATE change-set completion and compare its additions with the approved scope. An extra unapproved addition is a discrepancy, not permission to proceed. Keep the requested scope, preview and later execution outcome separate; a matching preview can still be followed by failed execution. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) A preview is not execution evidence, and approval is not a guarantee of execution success. ⟦A.f1 A.f2 A.f3 A:tb5⟧

### s03 · check · Judge the evidence
Check your understanding — Read the supplied case and choose the interpretation supported by its evidence.

### s04 · hands_on · Review CloudFormation change sets
Evidence review — Read the supplied excerpts in this step and decide which satisfy the stated requirements and which are defective or unsafe.

### s05 · recap · Keep the boundary clear
Takeaways — 
(takeaway) Preview first. Review resource actions and replacement indicators before approval. For a new stack, wait for CREATE completion, inspect, then execute the approved set; execution success is not guaranteed. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] MFA enforcement: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Evidence versus assumption
(mechanism) A change set previews proposed stack changes without executing them. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Before authorizing execution, review additions, modifications, removals and replacement indicators. A preview does not guarantee execution success. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) A preview is not execution evidence, and approval is not a guarantee of execution success. ⟦A.f1 A.f2 A.f3 A:tb5⟧

=========

# EVALUATOR PACKET — MFA enforcement (aws_devops.tile.017)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws.mfa_enforcement — Mfa enforcement

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws.mfa_enforcement)   objective: Require MFA for identity access
A.f1: The aws:MultiFactorAuthPresent condition indicates whether qualifying temporary credentials were authenticated with MFA.   [sources: aws_iam_user_guide#reference_policies_examples_aws_my-sec-creds-self-manage.html]
A.f2: A Deny with BoolIfExists on aws:MultiFactorAuthPresent set to false can block non-MFA requests, including requests where the key is absent, subject to the statement’s scoped actions.   [sources: aws_iam_user_guide#reference_policies_examples_aws_my-sec-creds-self-manage.html]
A.f3: Apply the supplied scoped MFA policy and compare an allowed MFA-authenticated request with a denied request without MFA.   [sources: aws_iam_user_guide#reference_policies_examples_aws_my-sec-creds-self-manage.html]
note: Keep the qualifying-temporary-credential limitation; apply only the supplied scoped MFA policy.
PRACTICE ANCHOR (tool_simulation): Apply the supplied scoped MFA policy to a sandbox identity and run two supplied test requests for the same covered action: one with qualifying MFA-authenticated temporary credentials and one without MFA.  SUCCESS: The supplied policy is applied without expanding its action scope. The MFA-authenticated request is allowed and the request without MFA is denied. Record each request's action, aws:MultiFactorAuthPresent context, and result; explain that the supplied BoolIfExists Deny set to false also covers an absent key for actions within its scope.
ASSESSMENT ANCHOR: distinguish_permitted_mfa_access_from_denied_non_mfa_access facts=['f1', 'f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute an AWS change using CloudTrail evidence; Attribute workload spend using resource tags; Centralize structured application logs in CloudWatch Logs; Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation; Choose rolling, blue/green or canary delivery for stated availability and rollback requirements; Collect host telemetry with the CloudWatch agent; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure role trust; directly require native IAM identity-policy evaluation; Configure secure human access with temporary credentials; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Evaluate resource-based permissions for a requested operation; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute an established managed account-onboarding workflow; Extract structured AWS CLI inventory across paginated results; Hand over an actionable operational runbook; Operate

## LESSON, in learner order

### s01 · explainer · MFA enforcement
Understand — 
(mechanism) aws:MultiFactorAuthPresent describes MFA authentication for qualifying temporary credentials. ⟦A.f1 A:tb2⟧
(mechanism) A scoped Deny using BoolIfExists with aws:MultiFactorAuthPresent set to false can block non-MFA requests, including an absent key. Keep the statement’s action scope in view. ⟦A.f2 A:tb3⟧
(mechanism) Apply the supplied scoped policy and compare an allowed MFA-authenticated request with a denied request without MFA. ⟦A.f3 A:tb3⟧
[SIDE_BY_SIDE] Read authentication context and action scope together. left_label: Policy scope | right_label: Request contexts
  left:
[DIAGRAM: Statement boundary] nodes=['Scoped Deny {BoolIfExists; aws:MultiFactorAuthPresent = false; Only statement-scoped actions}'] edges=[] alt: Statement boundary: Scoped Deny: BoolIfExists, aws:MultiFactorAuthPresent = false, Only statement-scoped actions
  right:
[DIAGRAM: Request comparison] nodes=['Covered action with existing Allow {true: this Deny does not match; false: this Deny matches; absent: this Deny matches}', 'Outside action scope {This statement does not establish the request outcome}'] edges=[] alt: Request comparison: Covered action with existing Allow: true: this Deny does not match, false: this Deny matches, absent: this Deny matches; Outside action scope: This statement does not establish the request outcome

### s02 · explainer · Compare the evidence, not the label
Apply the evidence — 
(example) Compare covered actions under the supplied policy. For qualifying MFA-authenticated temporary credentials, the true context does not match this Deny. False and absent contexts match the BoolIfExists Deny set to false. Compare the allowed MFA case with the denied non-MFA case without extending the result to actions outside the statement’s scope. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) An absent key is not automatically exempt from this scoped BoolIfExists Deny. ⟦A.f1 A.f2 A:tb5⟧

### s03 · check · Judge the evidence
Check your understanding — Read the supplied case and choose the interpretation supported by its evidence.

### s04 · hands_on · Review MFA enforcement
Evidence review — Read the supplied excerpts in this step and decide which satisfy the stated requirements and which are defective or unsafe.

### s05 · recap · Keep the boundary clear
Takeaways — 
(takeaway) Keep qualifying temporary credentials and scoped actions explicit. A BoolIfExists Deny set to false can match false and absent MFA contexts. Compare allowed MFA and denied non-MFA requests. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Configure role trust; directly require native IAM identity-policy evaluation: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Evidence versus assumption
(mechanism) aws:MultiFactorAuthPresent describes MFA authentication for qualifying temporary credentials. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) A scoped Deny using BoolIfExists with aws:MultiFactorAuthPresent set to false can block non-MFA requests, including an absent key. Keep the statement’s action scope in view. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Apply the supplied scoped policy and compare an allowed MFA-authenticated request with a denied request without MFA. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) An absent key is not automatically exempt from this scoped BoolIfExists Deny. ⟦A.f1 A.f2 A:tb5⟧

=========

# EVALUATOR PACKET — Configure role trust; directly require native IAM identity-policy evaluation (aws_devops.tile.018)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws.role_trust — Configure role trust; directly require native IAM identity-policy evaluation

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws.role_trust)   objective: Configure an AWS role trust policy
A.f1: A role trust policy identifies principals allowed to assume the role and any conditions for assumption.   [sources: aws_iam_user_guide#id_roles_create_for-user.html]
A.f2: Set Principal to the approved principal and Action to sts:AssumeRole with the supplied conditions in the role’s trust policy.   [sources: aws_iam_user_guide#id_roles_create_for-user.html]
A.f3: For cross-account assumption, the caller also needs permission to call sts:AssumeRole on the role; test approved and unapproved principals.   [sources: aws_iam_user_guide#id_roles_create_for-user.html]
A.f4: A role’s permissions policy controls what an assumed session may do, rather than who may assume it.   [sources: aws_iam_user_guide#id_roles.html]
note: Use approved principals and supplied conditions; avoid advanced federation design.
PRACTICE ANCHOR (tool_simulation): Configure the sandbox orders-operator role's trust policy with the supplied approved principal, sts:AssumeRole action and conditions. Check the supplied cross-account caller permissions, then test assumption by the approved and unapproved principals.  SUCCESS: The trust policy names only the supplied approved principal and preserves the supplied conditions. The approved caller has permission to call sts:AssumeRole on the role and succeeds when those conditions are met; the unapproved caller is rejected. Both test outcomes are retained.
ASSESSMENT ANCHOR: evaluate_named_principal_against_role_trust_and_conditions facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_cross_account_caller_assume_role_permission facts=['f3']
ASSESSMENT ANCHOR: distinguish_role_entry_from_assumed_session_permissions facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute an AWS change using CloudTrail evidence; Attribute workload spend using resource tags; Centralize structured application logs in CloudWatch Logs; Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation; Choose rolling, blue/green or canary delivery for stated availability and rollback requirements; Collect host telemetry with the CloudWatch agent; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure secure human access with temporary credentials; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Evaluate resource-based permissions for a requested operation; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute an established managed account-onboarding workflow; Extract structured AWS CLI inventory across paginated results; Hand over an actionable operational runbook; Operate an EKS Pod using supplied cluster-access setup; Operate an RDS managed databa

## LESSON, in learner order

### s01 · explainer · Configure role trust
Understand — 
(mechanism) A role trust policy identifies who may assume the role and the conditions for assumption. ⟦A.f1 A:tb2⟧
(mechanism) In the trust policy, use the approved Principal, Action sts:AssumeRole and the supplied conditions. ⟦A.f2 A:tb3⟧
(mechanism) Cross-account callers also need permission to call sts:AssumeRole on the role. Test approved and unapproved principals. ⟦A.f3 A:tb3⟧
(mechanism) The role’s permissions policy governs an assumed session’s work, not who may enter the role. ⟦A.f4 A:tb3⟧
[DIAGRAM: Review map: Configure role trust] nodes=['Cross-account caller {Approved or unapproved principal; Caller permission: sts:AssumeRole on the role}', 'Role trust: entry {Principal: approved principal; Action: sts:AssumeRole; Supplied conditions}', 'Assumed session: work {Role permissions policy controls allowed operations}'] edges=[('n1', 'n2', 'AssumeRole: caller permission and trust checks'), ('n2', 'n3', 'After approved assumption')] alt: Review map: Configure role trust: Cross-account caller: Approved or unapproved principal, Caller permission: sts:AssumeRole on the role; Role trust: entry: Principal: approved principal, Action: sts:AssumeRole, Supplied conditions; Assumed session: work: Role permissions policy controls allowed operations

### s02 · explainer · Compare the evidence, not the label
Apply the evidence — 
(example) For cross-account entry to the orders-operator role, inspect both trust and caller-side AssumeRole permission. Compare approved and unapproved principals under the supplied conditions. After assumption, look to the role’s permissions policy for the session’s allowed work; the trust policy is not an operations allowlist. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧
(misconception) Role entry and session work are different checks; trust alone does not complete cross-account caller permission. ⟦A.f1 A.f3 A.f4 A:tb5⟧

### s03 · check · Judge the evidence
Check your understanding — Read the supplied case and choose the interpretation supported by its evidence.

### s04 · hands_on · Review Configure role trust
Evidence review — Read the supplied excerpts in this step and decide which satisfy the stated requirements and which are defective or unsafe.

### s05 · recap · Keep the boundary clear
Takeaways — 
(takeaway) Trust governs role entry; role permissions govern session work. Use the approved principal, AssumeRole action and conditions. Cross-account entry also needs caller-side permission and approved/unapproved tests. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Root protection: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Evidence versus assumption
(mechanism) The role’s permissions policy governs an assumed session’s work, not who may enter the role. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Role entry and session work are different checks; trust alone does not complete cross-account caller permission. ⟦A.f1 A.f3 A.f4 A:tb5⟧
### r02 · Evidence versus assumption
(mechanism) A role trust policy identifies who may assume the role and the conditions for assumption. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) In the trust policy, use the approved Principal, Action sts:AssumeRole and the supplied conditions. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) Cross-account callers also need permission to call sts:AssumeRole on the role. Test approved and unapproved principals. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Role entry and session work are different checks; trust alone does not complete cross-account caller permission. ⟦A.f1 A.f3 A.f4 A:tb5⟧

=========

# EVALUATOR PACKET — Root protection (aws_devops.tile.019)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws.root_protection — Root protection

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws.root_protection)   objective: Protect and stop routine use of the AWS root user
A.f1: The AWS account root user has broad account authority and should not be used for routine tasks.   [sources: aws_iam_user_guide#root-user-best-practices.html]
A.f2: Protect root access with MFA and do not create root access keys; delete existing root access keys when they are no longer needed.   [sources: aws_iam_user_guide#root-user-best-practices.html]
A.f3: Review root-use and access-key evidence against the root-protection checklist, using non-root identities for routine operations.   [sources: aws_iam_user_guide#root-user-best-practices.html]
note: Review supplied evidence; do not introduce or perform unapproved root-only operations.
PRACTICE ANCHOR (tool_simulation): Review a supplied root-protection checklist alongside simulated MFA, root-use, and access-key evidence. Identify routine root use and remove simulated root access keys marked as no longer needed, without accessing a real root account.  SUCCESS: The completed checklist records MFA protection separately from access-key findings, flags routine root use as a violation, and identifies non-root identities for routine operations. Simulated root access keys marked as no longer needed are removed, and no root access keys are created.
ASSESSMENT ANCHOR: identify_root_access_key_policy_violations facts=['f2', 'f3']
ASSESSMENT ANCHOR: identify_routine_root_use_policy_violations facts=['f1', 'f3']

## DATA ASSETS USED
ds.root_protection: Root-protection checklist evidence — columns: record_id(identifier), checklist_item(categorical), identity_or_key(identifier), evidence(text), key_remains_needed(categorical), removal_status(categorical), finding(text)
   ["mfa","MFA protection","root sign-in","MFA enabled",null,null,"MFA protection confirmed independently of key hygiene"]
   ["routine-root","Routine identity use","root","Routine orders operation used root",null,null,"Violation: use a non-root identity for routine tasks"]
   ["routine-nonroot","Routine identity use","orders-operator","Routine orders operation used a non-root identity",null,null,"Non-root routine-use boundary satisfied"]
   ["key-obsolete","Root access-key hygiene","simulated-root-key-a","Existing simulated root access key",false,"removed","No longer needed; simulated removal recorded"]
   ["key-needed","Root access-key hygiene","simulated-root-key-b","Existing simulated root access key",true,"retained","Still marked needed in supplied evidence; not the obsolete-key removal case"]
   ["no-new-keys","Root access-key hygiene","root","No root access keys created during review",null,null,"Review did not create root access keys"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute an AWS change using CloudTrail evidence; Attribute workload spend using resource tags; Centralize structured application logs in CloudWatch Logs; Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation; Choose rolling, blue/green or canary delivery for stated availability and rollback requirements; Cloudformation drift; Collect host telemetry with the CloudWatch agent; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure secure human access with temporary credentials; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Evaluate resource-based permissions for a requested operation; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute an established managed account-onboarding workflow; Extract structured AWS CLI inventory across paginated results; Hand over an actionable operational runbook; Operate an EKS Pod using supplied cluster-access setup; Operate

## LESSON, in learner order

### s01 · explainer · Root protection
Understand — 
(mechanism) Root has broad account authority, but routine tasks belong under non-root identities. ⟦A.f1 A:tb2⟧
(mechanism) Protect root access with MFA. Do not create root access keys; delete existing keys when they are no longer needed. ⟦A.f2 A:tb3⟧
(mechanism) Compare root-use and access-key evidence with the protection checklist. Use non-root identities for routine operations. ⟦A.f3 A:tb3⟧
[TABLE ds.root_protection cols=['record_id', 'checklist_item', 'identity_or_key', 'evidence', 'key_remains_needed', 'removal_status', 'finding'] ] caption: Root-protection checklist evidence

### s02 · explainer · Compare the evidence, not the label
Apply the evidence — 
(example) Review the supplied root checklist item by item. Keep MFA protection, routine identity use and existing-key hygiene separate. A satisfactory MFA finding does not erase routine root use. Check whether each existing key remains needed and its removal status; do not create keys during the review. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) Root’s broad authority is not a reason to use it for routine operations. ⟦A.f1 A.f2 A.f3 A:tb5⟧

### s03 · check · Judge the evidence
Check your understanding — Read the supplied case and choose the interpretation supported by its evidence.

### s04 · hands_on · Review Root protection
Evidence review — Read the supplied excerpts in this step and decide which satisfy the stated requirements and which are defective or unsafe.

### s05 · recap · Keep the boundary clear
Takeaways — 
(takeaway) Keep root out of routine tasks. Review MFA, root-use evidence and key hygiene independently. Do not create root access keys; delete existing keys when no longer needed. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Attribute an AWS change using CloudTrail evidence: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Evidence versus assumption
(mechanism) Root has broad account authority, but routine tasks belong under non-root identities. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Compare root-use and access-key evidence with the protection checklist. Use non-root identities for routine operations. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Root’s broad authority is not a reason to use it for routine operations. ⟦A.f1 A.f2 A.f3 A:tb5⟧
[TABLE ds.root_protection cols=['record_id', 'checklist_item', 'identity_or_key', 'evidence', 'key_remains_needed', 'removal_status', 'finding'] ] caption: Revisit the same supplied evidence
### r02 · Evidence versus assumption
(mechanism) Root has broad account authority, but routine tasks belong under non-root identities. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Protect root access with MFA. Do not create root access keys; delete existing keys when they are no longer needed. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Compare root-use and access-key evidence with the protection checklist. Use non-root identities for routine operations. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Root’s broad authority is not a reason to use it for routine operations. ⟦A.f1 A.f2 A.f3 A:tb5⟧
[TABLE ds.root_protection cols=['record_id', 'checklist_item', 'identity_or_key', 'evidence', 'key_remains_needed', 'removal_status', 'finding'] ] caption: Revisit the same supplied evidence

=========

# EVALUATOR PACKET — Attribute an AWS change using CloudTrail evidence (aws_devops.tile.020)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.attribute_an_aws_change_using_cloudtrail_evidence — Attribute an AWS change using CloudTrail evidence

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.attribute_an_aws_change_using_cloudtrail_evidence)   objective: Attribute an AWS change using CloudTrail
A.f1: CloudTrail event history exposes recent management events for the selected Region; it does not represent all application activity.   [sources: aws_cloudtrail_user_guide#view-cloudtrail-events.html]
A.f2: Filter event history by an attribute such as event name, resource name or user name and the relevant time interval.   [sources: aws_cloudtrail_user_guide#view-cloudtrail-events.html]
A.f3: Inspect eventTime, eventName, userIdentity and requestParameters or resources to attribute a change to an actor, operation, target and time.   [sources: aws_cloudtrail_user_guide#cloudtrail-event-reference-record-contents.html]
note: Do not introduce X-Ray/request tracing or infer causation beyond the supplied change evidence.
PRACTICE ANCHOR (tool_simulation): Find the event for a supplied sandbox configuration change in CloudTrail event history using the supplied Region, resource name and 09:00–09:15 interval.  SUCCESS: Select the supplied Region, filter by the relevant attribute and time interval, and identify the matching event by comparing its operation and target with the supplied change. Record the actor from userIdentity, operation from eventName, target from requestParameters or resources, and time from eventTime rather than choosing the closest timestamp alone.
ASSESSMENT ANCHOR: identify_actor_operation_resource_and_time_from_event_fields facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute workload spend using resource tags; Centralize structured application logs in CloudWatch Logs; Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation; Choose rolling, blue/green or canary delivery for stated availability and rollback requirements; Cloudformation drift; Cloudformation rollback; Collect host telemetry with the CloudWatch agent; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure secure human access with temporary credentials; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Evaluate resource-based permissions for a requested operation; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute an established managed account-onboarding workflow; Extract structured AWS CLI inventory across paginated results; Hand over an actionable operational runbook; Operate an EKS Pod using supplied cluster-access setup; Operate an RDS managed database a

## LESSON, in learner order

### s01 · explainer · Attribute an AWS change using CloudTrail evidence
Understand — 
(mechanism) CloudTrail event history shows recent management events in the selected Region, not all application activity. ⟦A.f1 A:tb2⟧
(mechanism) Filter by an attribute such as event name, resource name or user name, plus the relevant time interval. ⟦A.f2 A:tb3⟧
(mechanism) Read eventTime, eventName, userIdentity and requestParameters or resources to identify the time, operation, actor and target of a change. ⟦A.f3 A:tb3⟧
[DIAGRAM: Authored read-only event-history example] nodes=['Event history filter {Region: us-east-1; filter: Event name = StopInstances; interval: 09:00–09:15 UTC, 2026-01-15; requested target: i-00000000000000001}', 'Candidate comparison {Candidate A: eventTime 2026-01-15T09:05:00Z; eventName StopInstances; userIdentity arn:aws:iam::111122223333:user/orders-operator; requestParameters instanceId i-00000000000000002; Candidate B: eventTime 2026-01-15T09:10:00Z; eventName StopInstances; userIdentity arn:aws:iam::111122223333:user/orders-operator; requestParameters instanceId i-00000000000000001}', 'Matching event fields {B matches the requested operation and target; A does not match the target}'] edges=[] alt: Authored read-only event-history example: Event history filter: Region: us-east-1; filter: Event name = StopInstances; interval: 09:00–09:15 UTC, 2026-01-15; requested target: i-00000000000000001; Candidate comparison: Candidate A: eventTime 2026-01-15T09:05:00Z; eventName StopInstances; userIdentity arn:aws:iam::111122223333:user/orders-operator; requestParameters instanceId i-00000000000000002; Candidate B: eventTime 2026-01-15T09:10:00Z; eventName StopInstances; userIdentity arn:aws:iam::111122223333:user/orders-operator; requestParameters instanceId i-00000000000000001; Matching event fields: B matches the requested operation and target; A does not match the target

### s02 · explainer · Compare the evidence, not the label
Apply the evidence — 
(example) For the supplied 09:00–09:15 example, filter by the relevant attribute and compare candidate events. Use the operation and target fields as well as the timestamp. Record actor, operation, target and time together; a nearby event or a guessed resource owner is not attribution evidence. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) Event history covers recent regional management events, not the sequence of all application requests. ⟦A.f1 A.f3 A:tb5⟧

### s03 · check · Judge the evidence
Check your understanding — Read the supplied case and choose the interpretation supported by its evidence.

### s04 · hands_on · Review Attribute an AWS change using CloudTrail evidence
Evidence review — Read the supplied excerpts in this step and decide which satisfy the stated requirements and which are defective or unsafe.

### s05 · recap · Keep the boundary clear
Takeaways — 
(takeaway) Filter recent regional management events by a relevant attribute and interval. Attribute the change from event time, operation, identity and target evidence, not a guessed owner. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Attribute workload spend using resource tags: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Evidence versus assumption
(mechanism) Read eventTime, eventName, userIdentity and requestParameters or resources to identify the time, operation, actor and target of a change. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Event history covers recent regional management events, not the sequence of all application requests. ⟦A.f1 A.f3 A:tb5⟧

=========

# EVALUATOR PACKET — Attribute workload spend using resource tags (aws_devops.tile.021)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.attribute_workload_spend_using_resource_tags — Attribute workload spend using resource tags

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.attribute_workload_spend_using_resource_tags)   objective: Attribute AWS spend to a workload using tags
A.f1: Cost-allocation tags categorize costs by resource-associated tag keys and values after activation for billing.   [sources: aws_cost_management_user_guide#../../../awsaccountbilling/latest/aboutv2/custom-tags.html]
A.f2: Activate the desired cost-allocation tag, then group Cost Explorer costs by that tag for the chosen period.   [sources: aws_cost_management_user_guide#ce-filtering.html]
A.f3: Resources without the relevant active tag can leave spend unallocated to the intended workload category.   [sources: aws_cost_management_user_guide#../../../awsaccountbilling/latest/aboutv2/custom-tags.html]
note: Defer workload cost estimation; use observed Cost Explorer evidence only.
PRACTICE ANCHOR (tool_simulation): Produce an orders workload cost breakdown using supplied resource tags and observed billing evidence. Activate the Workload cost-allocation tag, select the supplied period, and group Cost Explorer costs by Workload.  SUCCESS: The breakdown records the chosen period and Workload grouping, reports the observed orders amount, and preserves other allocated and unallocated categories. Resources missing the relevant active tag are flagged for investigation without assigning their spend to orders based on resource names.
ASSESSMENT ANCHOR: group_tagged_charges_by_active_cost_allocation_tag facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_spend_unallocated_to_the_intended_workload facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Centralize structured application logs in CloudWatch Logs; Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation; Choose rolling, blue/green or canary delivery for stated availability and rollback requirements; Cloudformation drift; Cloudformation rollback; Collect host telemetry with the CloudWatch agent; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure secure human access with temporary credentials; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Ec2 instance profile; Evaluate resource-based permissions for a requested operation; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute an established managed account-onboarding workflow; Extract structured AWS CLI inventory across paginated results; Hand over an actionable operational runbook; Operate an EKS Pod using supplied cluster-access setup; Operate an RDS managed database as the native backup-reso

## LESSON, in learner order

### s01 · explainer · Attribute workload spend using resource tags
Understand — 
(mechanism) After billing activation, cost-allocation tags categorize costs by resource-associated tag keys and values. ⟦A.f1 A:tb2⟧
(mechanism) Activate the desired cost-allocation tag, then group Cost Explorer costs by that tag for the chosen period. ⟦A.f2 A:tb3⟧
(mechanism) Without the relevant active tag, resource spend can remain unallocated to the intended workload. ⟦A.f3 A:tb3⟧
[DIAGRAM: Workload billing review] nodes=['Billing grouping {Tag: Workload; Active: true; Period: 2026-01-01 to 2026-02-01 (end exclusive)}', 'orders {Billed amount: 40 exercise currency units; orders-host-a: Workload=orders; orders-host-b: Workload=orders; Preserve allocated category}', 'support {Billed amount: 12 exercise currency units; support-host: Workload=support; Preserve allocated category}', 'unallocated {Billed amount: 8 exercise currency units; orders-untagged: Workload=absent; Investigate missing relevant active tag; do not assign by resource name}'] edges=[] alt: Workload billing review: Billing grouping: Tag: Workload, Active: true, Period: 2026-01-01 to 2026-02-01 (end exclusive); orders: Billed amount: 40 exercise currency units, orders-host-a: Workload=orders; orders-host-b: Workload=orders, Preserve allocated category; support: Billed amount: 12 exercise currency units, support-host: Workload=support, Preserve allocated category; unallocated: Billed amount: 8 exercise currency units, orders-untagged: Workload=absent, Investigate missing relevant active tag; do not assign by resource name

### s02 · explainer · Compare the evidence, not the label
Apply the evidence — 
(example) For Workload=orders, compare the active billing grouping and selected period with resource-tag evidence. Preserve the report’s allocated and unallocated categories. An orders-looking resource name does not justify moving unallocated spend into orders; investigate the relevant active tag instead. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) A resource label alone does not establish active billing grouping. ⟦A.f1 A.f3 A:tb5⟧

### s03 · check · Judge the evidence
Check your understanding — Read the supplied case and choose the interpretation supported by its evidence.

### s04 · hands_on · Review Attribute workload spend using resource tags
Evidence review — Read the supplied excerpts in this step and decide which satisfy the stated requirements and which are defective or unsafe.

### s05 · recap · Keep the boundary clear
Takeaways — 
(takeaway) Activate the billing tag and group by it for the selected period. Compare resource-associated labels with allocated categories; missing relevant active tags can leave spend unallocated. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Centralize structured application logs in CloudWatch Logs: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Evidence versus assumption
(mechanism) Without the relevant active tag, resource spend can remain unallocated to the intended workload. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) A resource label alone does not establish active billing grouping. ⟦A.f1 A.f3 A:tb5⟧
### r02 · Evidence versus assumption
(mechanism) After billing activation, cost-allocation tags categorize costs by resource-associated tag keys and values. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Activate the desired cost-allocation tag, then group Cost Explorer costs by that tag for the chosen period. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) Without the relevant active tag, resource spend can remain unallocated to the intended workload. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) A resource label alone does not establish active billing grouping. ⟦A.f1 A.f3 A:tb5⟧

=========

# EVALUATOR PACKET — Centralize structured application logs in CloudWatch Logs (aws_devops.tile.022)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.centralize_structured_application_logs_in_cloudwatch_logs — Centralize structured application logs in CloudWatch Logs

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.centralize_structured_application_logs_in_cloudwatch_logs)   objective: Centralize application logs in CloudWatch Logs
A.f1: A log group holds log streams with shared retention and access settings; a stream is a sequence of events from one source.   [sources: aws_cloudwatch_user_guide#../logs/Working-with-log-groups-and-streams.html]
A.f2: Configure the supplied log collector with the application file path, log group and stream name, and verify a known JSON event arrives in that stream.   [sources: aws_cloudwatch_user_guide#CloudWatch-Agent-Configuration-File-Details.html]
A.f3: CloudWatch Logs Insights can discover fields in JSON log events, so preserving structured event fields makes them queryable.   [sources: aws_cloudwatch_user_guide#../logs/CWL_AnalyzeLogData-discoverable-fields.html]
note: Do not teach later query syntax here or redesign application logging.
PRACTICE ANCHOR (tool_simulation): Configure a supplied, ready-to-use log collector with the orders application's supplied file path, intended log group and stream name, then ship the supplied JSON events into that group.  SUCCESS: The known orders event appears in the intended stream within the intended group, with its request ID, outcome and timestamp preserved. The recorded collection evidence identifies the event and its arrival group and stream.
ASSESSMENT ANCHOR: locate_known_structured_event_in_intended_log_stream facts=['f1', 'f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation; Choose rolling, blue/green or canary delivery for stated availability and rollback requirements; Cloudformation drift; Cloudformation rollback; Collect host telemetry with the CloudWatch agent; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure secure human access with temporary credentials; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Ec2 instance profile; Eks workload identity; Evaluate resource-based permissions for a requested operation; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute an established managed account-onboarding workflow; Extract structured AWS CLI inventory across paginated results; Hand over an actionable operational runbook; Operate an EKS Pod using supplied cluster-access setup; Operate an RDS managed database as the native backup-resource foundation; Protect recoverable

## LESSON, in learner order

### s01 · explainer · Centralize structured application logs in CloudWatch Logs
Understand — 
(mechanism) A log group shares retention and access settings across streams. A stream sequences events from one source. ⟦A.f1 A:tb2⟧
(mechanism) Set the supplied collector’s application file path, group and stream name. Verify a known JSON event arrives in that stream. ⟦A.f2 A:tb3⟧
(mechanism) Preserve structured fields: CloudWatch Logs Insights can discover fields in JSON events and make them queryable. ⟦A.f3 A:tb3⟧
[DIAGRAM: Authored read-only collection evidence] nodes=['Collector configuration {Collector application file path: /var/log/orders/application.json; log group: /orders/sandbox; stream: orders-host-a}', 'Destination stream check {Observed destination: /orders/sandbox → orders-host-a; Observed JSON event: {"request_id":"orders-001","outcome":"success","timestamp":"2026-01-15T09:10:00Z"}}', 'Group and stream {Group: shared retention and access settings; Stream: event sequence from one source}'] edges=[] alt: Authored read-only collection evidence: Collector configuration: Collector application file path: /var/log/orders/application.json; log group: /orders/sandbox; stream: orders-host-a; Destination stream check: Observed destination: /orders/sandbox → orders-host-a; Observed JSON event: {"request_id":"orders-001","outcome":"success","timestamp":"2026-01-15T09:10:00Z"}; Group and stream: Group: shared retention and access settings; Stream: event sequence from one source

### s02 · explainer · Compare the evidence, not the label
Apply the evidence — 
(example) For the known orders JSON event, compare the collector’s application path, destination group and destination stream with its arrival location. Verify that request ID, outcome and timestamp remain structured. Creating a group alone does not prove that the collector delivered the intended event. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) A group shares settings; a stream holds a source’s events. Setup needs known-event arrival evidence. ⟦A.f1 A.f2 A:tb5⟧

### s03 · check · Judge the evidence
Check your understanding — Read the supplied case and choose the interpretation supported by its evidence.

### s04 · hands_on · Review Centralize structured application logs in CloudWatch Logs
Evidence review — Read the supplied excerpts in this step and decide which satisfy the stated requirements and which are defective or unsafe.

### s05 · recap · Keep the boundary clear
Takeaways — 
(takeaway) Groups share retention and access settings; streams sequence source events. Configure the collector and verify known-event arrival in the intended stream with structured JSON fields preserved for discovery. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Evidence versus assumption
(mechanism) A log group shares retention and access settings across streams. A stream sequences events from one source. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Set the supplied collector’s application file path, group and stream name. Verify a known JSON event arrives in that stream. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) A group shares settings; a stream holds a source’s events. Setup needs known-event arrival evidence. ⟦A.f1 A.f2 A:tb5⟧

=========

# EVALUATOR PACKET — Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation (aws_devops.tile.023)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.change_and_validate_a_linux_service_configuration — Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.change_and_validate_a_linux_service_configuration)   objective: Change a Linux service configuration safely on an AWS host
A.f1: A configuration change needs validation of its intended effect and a defined way to return to the previous working configuration.   [sources: aws_well_architected_framework#ops04-bp01.html]
A.f2: Identify and verify the supplied rollback files, change the supplied setting and run the supplied syntax or configuration check before activation.   [sources: aws_well_architected_framework#ops04-bp01.html]
A.f3: Use the service’s supported reload or restart procedure to activate a valid change, then inspect status and the supplied effective-setting check; on failure restore and reactivate the saved configuration.   [sources: linux_man_pages#man5/systemd.service.5.html]
note: Use supplied rollback files; do not teach backup creation, boot-startup policy or independent Bash authoring.
PRACTICE ANCHOR (tool_simulation): Change one supplied setting in a sandbox Linux service using prepared controls and supplied rollback files. Verify the rollback files, run the supplied configuration check before activation, then activate and verify the change. Restore and reactivate the saved configuration if validation fails.  SUCCESS: The supplied rollback files are verified before editing, only the designated setting changes, and a passing configuration check precedes activation. Service status and the supplied effective-setting check confirm the outcome. In the supplied failure case, the saved configuration is restored and reactivated, and both checks confirm the previous working state.
ASSESSMENT ANCHOR: verify_changed_setting_is_active facts=['f1', 'f3']
ASSESSMENT ANCHOR: restore_and_reactivate_supplied_prior_configuration_on_failure facts=['f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Choose rolling, blue/green or canary delivery for stated availability and rollback requirements; Cloudformation drift; Cloudformation rollback; Collect host telemetry with the CloudWatch agent; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure GitHub Actions AWS role federation; Configure secure human access with temporary credentials; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Ec2 instance profile; Eks workload identity; Evaluate resource-based permissions for a requested operation; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute an established managed account-onboarding workflow; Extract structured AWS CLI inventory across paginated results; Hand over an actionable operational runbook; Operate an EKS Pod using supplied cluster-access setup; Operate an RDS managed database as the native backup-resource foundation; Protect recoverable S3 objects with versioning and lifecycle controls; Publish a container imag

## LESSON, in learner order

### s01 · explainer · Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation
Understand — 
(mechanism) Define how to return to the previous working configuration and verify the change’s intended effect. ⟦A.f1 A:tb2⟧
(mechanism) Identify and verify the supplied rollback files. Change the supplied setting, then run the syntax or configuration check before activation. ⟦A.f2 A:tb3⟧
(mechanism) Activate a valid change with the supported reload or restart. Inspect status and the supplied effective-setting check; on failure, restore and reactivate the saved configuration. ⟦A.f3 A:tb3⟧
[DIAGRAM: Authored read-only sandbox-service record] nodes=['Before activation {Configuration: /etc/orders/service.conf; previous request_timeout_seconds: 30; requested value: 45; Rollback file: /etc/orders/service.conf.saved; verified as previous working configuration}', 'Activate valid change {Changed configuration check: PASS; supported reload result: completed; service status: running; effective-setting check: FAIL—observed 30, expected 45}', 'Failure return {Restored saved configuration; supported reload result: completed; service status: running; effective-setting check: PASS—observed 30}'] edges=[] alt: Authored read-only sandbox-service record: Before activation: Configuration: /etc/orders/service.conf; previous request_timeout_seconds: 30; requested value: 45; Rollback file: /etc/orders/service.conf.saved; verified as previous working configuration; Activate valid change: Changed configuration check: PASS; supported reload result: completed; service status: running; effective-setting check: FAIL—observed 30, expected 45; Failure return: Restored saved configuration; supported reload result: completed; service status: running; effective-setting check: PASS—observed 30

### s02 · explainer · Compare the evidence, not the label
Apply the evidence — 
(example) For the sandbox service, verify rollback files before changing the supplied setting. Check syntax before activation, then inspect service status and the effective setting. If validation fails, restore the saved configuration and reactivate it. Retain each result separately: a reload or restart request is not a verified outcome. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) Activation is not validation. Restoring a file also needs reactivation. ⟦A.f2 A.f3 A:tb5⟧

### s03 · check · Judge the evidence
Check your understanding — Read the supplied case and choose the interpretation supported by its evidence.

### s04 · hands_on · Review Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation
Evidence review — Read the supplied excerpts in this step and decide which satisfy the stated requirements and which are defective or unsafe.

### s05 · recap · Keep the boundary clear
Takeaways — 
(takeaway) Verify rollback files, change the setting and check before activation. Then inspect status and effective settings. On failure, restore and reactivate; an activation request is not validation. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Choose rolling, blue/green or canary delivery for stated availability and rollback requirements: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Evidence versus assumption
(mechanism) Identify and verify the supplied rollback files. Change the supplied setting, then run the syntax or configuration check before activation. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Activate a valid change with the supported reload or restart. Inspect status and the supplied effective-setting check; on failure, restore and reactivate the saved configuration. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Activation is not validation. Restoring a file also needs reactivation. ⟦A.f2 A.f3 A:tb5⟧
### r02 · Evidence versus assumption
(mechanism) Define how to return to the previous working configuration and verify the change’s intended effect. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Identify and verify the supplied rollback files. Change the supplied setting, then run the syntax or configuration check before activation. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Activate a valid change with the supported reload or restart. Inspect status and the supplied effective-setting check; on failure, restore and reactivate the saved configuration. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Activation is not validation. Restoring a file also needs reactivation. ⟦A.f2 A.f3 A:tb5⟧

=========

# EVALUATOR PACKET — Choose rolling, blue/green or canary delivery for stated availability and rollback requirements (aws_devops.tile.024)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.choose_rolling_blue_green_or_canary_delivery_for_stated_availability_and_rollback_requirements — Choose rolling, blue/green or canary delivery for stated availability and rollback requirements

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.choose_rolling_blue_green_or_canary_delivery_for_stated_availability_and_rollback_requirements)   objective: Choose a deployment strategy from availability and rollback constraints
A.f1: Rolling delivery replaces portions of the workload progressively rather than replacing all instances simultaneously.   [sources: aws_well_architected_framework#ops04-bp01.html]
A.f2: Blue/green delivery maintains separate old and new environments and switches traffic to the new environment.   [sources: aws_well_architected_framework#ops04-bp01.html]
A.f3: Canary delivery exposes a new version to a limited share of traffic before broader rollout.   [sources: aws_well_architected_framework#ops04-bp01.html]
A.f4: Choose a strategy by comparing traffic exposure, available parallel capacity and the ability to return traffic to a known-good version.   [sources: aws_well_architected_framework#ops04-bp01.html]
note: Defer product-specific rollout procedures; keep examples tied to stated exposure, capacity and rollback requirements.
PRACTICE ANCHOR (field_selection): Select rolling, blue/green or canary delivery for a supplied service scenario and defend the choice using its traffic-exposure limit, available parallel capacity and required return to a known-good version. Use supplied strategy descriptions rather than configuring a deployment.  SUCCESS: The selected strategy meets the scenario's stated exposure, capacity and rollback requirements. The justification accurately describes its replacement or traffic behavior, cites the supplied return-to-known-good arrangement and explains why the alternatives are less suitable.
ASSESSMENT ANCHOR: justify_delivery_strategy_for_stated_workload_requirements facts=['f1', 'f2', 'f3', 'f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Cloudformation drift; Cloudformation rollback; Collect host telemetry with the CloudWatch agent; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure GitHub Actions AWS role federation; Configure secure human access with temporary credentials; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Ec2 instance profile; Eks workload identity; Evaluate resource-based permissions for a requested operation; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute an established managed account-onboarding workflow; Extract structured AWS CLI inventory across paginated results; Hand over an actionable operational runbook; Operate an EKS Pod using supplied cluster-access setup; Operate an RDS managed database as the native backup-resource foundation; Protect recoverable S3 objects with versioning and lifecycle controls; Publish a container image to ECR after external Docker preparation; Publish a traceable immutable build artifact; Read an

## LESSON, in learner order

### s01 · explainer · Choose rolling, blue/green or canary delivery for stated availability and rollback requirements
Understand — 
(mechanism) Rolling delivery replaces workload portions progressively, not all instances simultaneously. ⟦A.f1 A:tb2⟧
(mechanism) Blue/green keeps separate old and new environments, then switches traffic to the new environment. ⟦A.f2 A:tb3⟧
(mechanism) Canary exposes a new version to a limited traffic share before broader rollout. ⟦A.f3 A:tb3⟧
(mechanism) Compare traffic exposure, available parallel capacity and the route back to a known-good version when choosing a strategy. ⟦A.f4 A:tb3⟧
[SIDE_BY_SIDE] Match the proposal to stated requirements, not a universal ranking. left_label: Progressive workload replacement | right_label: Environment switch or limited exposure
  left:
[DIAGRAM: Supplied fictional proposals—not universal strategy guarantees — Rolling] nodes=['Replacement pattern {Replace portions progressively; new-version exposure after first batch: 25%; additional capacity: one batch; return route: replace changed portions with known-good version}', 'Requirement comparison {Requirements: initial new-version traffic no more than 10%; available additional capacity: one full workload; return traffic to retained known-good version}'] edges=[] alt: Supplied fictional proposals—not universal strategy guarantees — Rolling: Replacement pattern: Replace portions progressively; new-version exposure after first batch: 25%; additional capacity: one batch; return route: replace changed portions with known-good version; Requirement comparison: Requirements: initial new-version traffic no more than 10%; available additional capacity: one full workload; return traffic to retained known-good version
  right:
[DIAGRAM: Supplied fictional proposals—not universal strategy guarantees — Blue/green and canary] nodes=['Blue/green {Separate old/new environments; proposed switch: 100% to new; additional capacity: one full workload; return route: switch traffic to retained old environment}', 'Canary {Initial new-version traffic: 10%; additional capacity: 10% workload; return route: route traffic back to retained known-good version}', 'Requirement comparison {Requirements: initial new-version traffic no more than 10%; available additional capacity: one full workload; return traffic to retained known-good version}'] edges=[] alt: Supplied fictional proposals—not universal strategy guarantees — Blue/green and canary: Blue/green: Separate old/new environments; proposed switch: 100% to new; additional capacity: one full workload; return route: switch traffic to retained old environment; Canary: Initial new-version traffic: 10%; additional capacity: 10% workload; return route: route traffic back to retained known-good version; Requirement comparison: Requirements: initial new-version traffic no more than 10%; available additional capacity: one full workload; return traffic to retained known-good version

### s02 · explainer · Compare the evidence, not the label
Apply the evidence — 
(example) Compare three proposals for the same release. Separate old and new environments address that stated arrangement; limited initial traffic exposure points to the canary proposal. For each, compare available parallel capacity and the route back to the known-good version. A strategy name is not a recovery guarantee or a universal ranking. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧
(misconception) Rolling describes progressive replacement; canary describes limited traffic exposure. They are not interchangeable names. ⟦A.f1 A.f2 A.f3 A:tb5⟧

### s03 · check · Judge the evidence
Check your understanding — Read the supplied case and choose the interpretation supported by its evidence.

### s04 · hands_on · Review Choose rolling, blue/green or canary delivery for stated availability and rollback requirements
Evidence review — Read the supplied excerpts in this step and decide which satisfy the stated requirements and which are defective or unsafe.

### s05 · recap · Keep the boundary clear
Takeaways — 
(takeaway) Rolling progressively replaces portions; blue/green separates environments and switches traffic; canary starts with limited traffic exposure. Choose against exposure, parallel-capacity and known-good return requirements. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Collect host telemetry with the CloudWatch agent: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Evidence versus assumption
(mechanism) Rolling delivery replaces workload portions progressively, not all instances simultaneously. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Blue/green keeps separate old and new environments, then switches traffic to the new environment. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Canary exposes a new version to a limited traffic share before broader rollout. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(mechanism) Compare traffic exposure, available parallel capacity and the route back to a known-good version when choosing a strategy. ⟦A.f4 A:tb3 A:tb4⟧
(misconception) Rolling describes progressive replacement; canary describes limited traffic exposure. They are not interchangeable names. ⟦A.f1 A.f2 A.f3 A:tb5⟧

=========

# EVALUATOR PACKET — Collect host telemetry with the CloudWatch agent (aws_devops.tile.025)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.collect_host_telemetry_with_the_cloudwatch_agent — Collect host telemetry with the CloudWatch agent

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.collect_host_telemetry_with_the_cloudwatch_agent)   objective: Collect host telemetry with the CloudWatch agent
A.f1: The CloudWatch agent collects configured host metrics and logs and sends them to CloudWatch.   [sources: aws_cloudwatch_user_guide#CloudWatch-Agent-Configuration-File-Details.html]
A.f2: In the agent configuration, choose metrics under metrics_collected and append instance-identifying dimensions such as InstanceId.   [sources: aws_cloudwatch_user_guide#CloudWatch-Agent-Configuration-File-Details.html]
A.f3: Start the agent with amazon-cloudwatch-agent-ctl using fetch-config, the supplied configuration location and -s, then verify the expected metric and instance dimension in CloudWatch.   [sources: aws_cloudwatch_user_guide#start-CloudWatch-Agent-on-premise-SSM-onprem.html]
note: Use supplied configuration and agent-control procedure; require external package and Linux service preparation.
PRACTICE ANCHOR (tool_simulation): Configure the supplied agent profile on a prepared sandbox EC2 host: select the supplied metrics under metrics_collected, append the InstanceId dimension, and start the agent with amazon-cloudwatch-agent-ctl using fetch-config, the supplied configuration location and -s. Verify the resulting metric in CloudWatch.  SUCCESS: The supplied profile selects the required host metric and appends InstanceId; the agent is started using the supplied configuration location; and the expected metric appears in CloudWatch with an InstanceId matching the approved sandbox host.
ASSESSMENT ANCHOR: verify_expected_host_metric_and_instance_identity facts=['f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authorize an event target with least-privilege execution permissions; Cloudformation drift; Cloudformation rollback; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure GitHub Actions AWS role federation; Configure secure human access with temporary credentials; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Ec2 instance profile; Eks workload identity; Evaluate resource-based permissions for a requested operation; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute an established managed account-onboarding workflow; Extract structured AWS CLI inventory across paginated results; Hand over an actionable operational runbook; Operate an EKS Pod using supplied cluster-access setup; Operate an RDS managed database as the native backup-resource foundation; Protect recoverable S3 objects with versioning and lifecycle controls; Publish a container image to ECR after external Docker preparation; Publish a traceable immutable bui

## LESSON, in learner order

### s01 · explainer · Collect host telemetry with the CloudWatch agent
Understand — 
(mechanism) The CloudWatch agent sends configured host metrics and logs to CloudWatch. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Choose metrics under metrics_collected and append instance-identifying dimensions such as InstanceId. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Start with amazon-cloudwatch-agent-ctl, fetch-config, the supplied configuration location and -s. Verify the expected metric and instance dimension in CloudWatch. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[DIAGRAM: Authored read-only host-telemetry evidence] nodes=['Approved host and configuration {Approved host InstanceId: i-00000000000000001; expected metric: mem_used_percent; Supplied profile selects mem_used_percent under metrics_collected and appends InstanceId}', 'Agent start {Supplied start evidence: amazon-cloudwatch-agent-ctl; fetch-config; configuration location /opt/orders/agent.json; -s; result: started}', 'CloudWatch verification {Observed CloudWatch metric: mem_used_percent; InstanceId: i-00000000000000001; metric and source both match}'] edges=[] alt: Authored read-only host-telemetry evidence: Approved host and configuration: Approved host InstanceId: i-00000000000000001; expected metric: mem_used_percent; Supplied profile selects mem_used_percent under metrics_collected and appends InstanceId; Agent start: Supplied start evidence: amazon-cloudwatch-agent-ctl; fetch-config; configuration location /opt/orders/agent.json; -s; result: started; CloudWatch verification: Observed CloudWatch metric: mem_used_percent; InstanceId: i-00000000000000001; metric and source both match
(example) Compare the intended host with the observed CloudWatch series. Match both the expected metric and InstanceId; a matching metric name from another instance does not verify this host. ⟦A.f1 A.f2 A.f3 A:tb4⟧

### s02 · check · Judge the evidence
Check your understanding — Read the supplied case and choose the interpretation supported by its evidence.

### s03 · hands_on · Review Collect host telemetry with the CloudWatch agent
Evidence review — Read the supplied excerpts in this step and decide which satisfy the stated requirements and which are defective or unsafe.

### s04 · recap · Keep the boundary clear
Takeaways — 
(takeaway) Configure metrics_collected and instance dimensions. Start with fetch-config and -s through amazon-cloudwatch-agent-ctl. Verify the expected CloudWatch metric and InstanceId, not merely agent startup. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Evidence versus assumption
(mechanism) Choose metrics under metrics_collected and append instance-identifying dimensions such as InstanceId. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Start with amazon-cloudwatch-agent-ctl, fetch-config, the supplied configuration location and -s. Verify the expected metric and instance dimension in CloudWatch. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Starting the agent is not verification; check the observed metric and instance identity. ⟦A.f2 A.f3 A:tb5⟧

=========

# EVALUATOR PACKET — Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds (aws_devops.tile.026)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.configure_cloudwatch_alarm_evaluation_and_missing_data_behavior_from_supplied_signals_and_thresholds — Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.configure_cloudwatch_alarm_evaluation_and_missing_data_behavior_from_supplied_signals_and_thresholds)   objective: Configure CloudWatch alarm evaluation
A.f1: A metric alarm evaluates a statistic over periods against a threshold and has OK, ALARM and INSUFFICIENT_DATA states.   [sources: aws_cloudwatch_user_guide#alarm-evaluation.html]
A.f2: EvaluationPeriods is the number of evaluated periods, and DatapointsToAlarm is the number of breaching datapoints required within that window.   [sources: aws_cloudwatch_user_guide#alarm-evaluation.html]
A.f3: Set the supplied metric, statistic, period, comparison operator and threshold along with the evaluation counts; compare the resulting state with the supplied samples.   [sources: aws_cloudwatch_user_guide#ConsoleAlarms.html]
A.f4: Missing-data settings are breaching, notBreaching, ignore (retain current state), and missing (insufficient data when all datapoints are missing); missing is the default.   [sources: aws_cloudwatch_user_guide#alarms-and-missing-data.html]
note: Use supplied signals and thresholds; do not introduce unsupported sparse-data evaluation rules.
PRACTICE ANCHOR (tool_simulation): Configure one metric alarm with the supplied metric, statistic, period, comparison operator, threshold, EvaluationPeriods, DatapointsToAlarm and missing-data policy. Evaluate supplied complete-sample and all-missing windows to verify state transitions.  SUCCESS: The saved configuration matches the supplied settings. For complete-sample windows, the resulting OK or ALARM state matches the required breach count. For all-missing windows, breaching yields ALARM, notBreaching yields OK, ignore retains the supplied current state, and missing yields INSUFFICIENT_DATA.
ASSESSMENT ANCHOR: predict_alarm_state_from_supplied_metric_samples_and_threshold facts=['f1', 'f3']
ASSESSMENT ANCHOR: apply_evaluation_periods_and_datapoints_to_alarm facts=['f2']
ASSESSMENT ANCHOR: predict_all_missing_alarm_state_from_missing_data_policy facts=['f1', 'f4']

## DATA ASSETS USED
ds.alarm_evaluation: Alarm windows and missing-data policies — columns: window_id(identifier,digits-as-label), metric(identifier), statistic(categorical), period_seconds(numerical), comparison_operator(categorical), threshold(numerical), EvaluationPeriods(numerical), DatapointsToAlarm(numerical), period_1_sample(numerical), period_2_sample(numerical), period_3_sample(numerical), period_1_comparison(categorical), period_2_comparison(categorical), period_3_comparison(categorical), breach_count(numerical), missing_data_policy(categorical), prior_state(categorical), resulting_state(categorical)
   [1,"orders_host_signal","Average",60,"GreaterThanThreshold",60,3,2,80,40,80,"above","below","above",2,"missing","OK","ALARM"]
   [2,"orders_host_signal","Average",60,"GreaterThanThreshold",60,3,2,40,80,40,"below","above","below",1,"missing","ALARM","OK"]
   [3,"orders_host_signal","Average",60,"GreaterThanThreshold",60,3,2,0,80,0,"below","above","below",1,"missing","ALARM","OK"]
   [4,"orders_host_signal","Average",60,"GreaterThanThreshold",60,3,2,null,null,null,"missing","missing","missing",0,"breaching","ALARM","ALARM"]
   [5,"orders_host_signal","Average",60,"GreaterThanThreshold",60,3,2,null,null,null,"missing","missing","missing",0,"notBreaching","ALARM","OK"]
   [6,"orders_host_signal","Average",60,"GreaterThanThreshold",60,3,2,null,null,null,"missing","missing","missing",0,"ignore","ALARM","ALARM"]
   [7,"orders_host_signal","Average",60,"GreaterThanThreshold",60,3,2,null,null,null,"missing","missing","missing",0,"missing","ALARM","INSUFFICIENT_DATA"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authorize an event target with least-privilege execution permissions; Automate prohibited-configuration checks; Cloudformation drift; Cloudformation rollback; Configure GitHub Actions AWS role federation; Configure secure human access with temporary credentials; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Ec2 instance profile; Eks workload identity; Evaluate resource-based permissions for a requested operation; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute an established managed account-onboarding workflow; Extract structured AWS CLI inventory across paginated results; Hand over an actionable operational runbook; Operate an EKS Pod using supplied cluster-access setup; Operate an RDS managed database as the native backup-resource foundation; Protect recoverable S3 objects with versioning and lifecycle controls; Publish a container image to ECR after external Docker preparation; Publish a traceable immutable build artifact; Read and modify a standard CloudFormation S3 te

## LESSON, in learner order

### s01 · explainer · Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds
Understand — 
(mechanism) A metric alarm compares a statistic over periods with a threshold. Its states are OK, ALARM and INSUFFICIENT_DATA. ⟦A.f1 A:tb2⟧
(mechanism) EvaluationPeriods counts evaluated periods; DatapointsToAlarm counts breaches required within that window. ⟦A.f2 A:tb3⟧
(mechanism) Set the supplied metric, statistic, period, comparison operator, threshold and evaluation counts. Compare the resulting state with the supplied samples. ⟦A.f3 A:tb3⟧
(mechanism) Missing-data policies are breaching, notBreaching, ignore (retain current state), and missing (INSUFFICIENT_DATA when all datapoints are missing). The default is missing. ⟦A.f4 A:tb3⟧
[TABLE ds.alarm_evaluation cols=['window_id', 'metric', 'statistic', 'period_seconds', 'comparison_operator', 'threshold', 'EvaluationPeriods', 'DatapointsToAlarm', 'period_1_sample', 'period_2_sample', 'period_3_sample', 'period_1_comparison', 'period_2_comparison', 'period_3_comparison', 'breach_count', 'missing_data_policy', 'prior_state', 'resulting_state'] ] caption: Alarm windows and missing-data policies

### s02 · explainer · Compare the evidence, not the label
Apply the evidence — 
(example) Compare the registered complete-sample windows with their evaluation settings and threshold comparisons. Then inspect all-missing windows under each policy. Keep real zero observations distinct from missing samples. Retain configuration, prior state and resulting state together rather than interpreting a gap as an observed zero or breach. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧
(misconception) EvaluationPeriods is not the required breach count. Default missing does not mean every isolated gap immediately produces INSUFFICIENT_DATA. ⟦A.f2 A.f4 A:tb5⟧

### s03 · check · Judge the evidence
Check your understanding — Read the supplied case and choose the interpretation supported by its evidence.

### s04 · hands_on · Review Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds
Evidence review — Read the supplied excerpts in this step and decide which satisfy the stated requirements and which are defective or unsafe.

### s05 · recap · Keep the boundary clear
Takeaways — 
(takeaway) Keep evaluated periods distinct from required breaches. Compare the configured signal and threshold with samples. For all-missing windows: breaching → ALARM, notBreaching → OK, ignore retains state, and default missing → INSUFFICIENT_DATA. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Configure secure human access with temporary credentials: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Evidence versus assumption
(mechanism) A metric alarm compares a statistic over periods with a threshold. Its states are OK, ALARM and INSUFFICIENT_DATA. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Missing-data policies are breaching, notBreaching, ignore (retain current state), and missing (INSUFFICIENT_DATA when all datapoints are missing). The default is missing. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) EvaluationPeriods is not the required breach count. Default missing does not mean every isolated gap immediately produces INSUFFICIENT_DATA. ⟦A.f2 A.f4 A:tb5⟧
[TABLE ds.alarm_evaluation cols=['window_id', 'metric', 'statistic', 'period_seconds', 'comparison_operator', 'threshold', 'EvaluationPeriods', 'DatapointsToAlarm', 'period_1_sample', 'period_2_sample', 'period_3_sample', 'period_1_comparison', 'period_2_comparison', 'period_3_comparison', 'breach_count', 'missing_data_policy', 'prior_state', 'resulting_state'] ] caption: Revisit the same supplied evidence
### r02 · Evidence versus assumption
(mechanism) A metric alarm compares a statistic over periods with a threshold. Its states are OK, ALARM and INSUFFICIENT_DATA. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) EvaluationPeriods counts evaluated periods; DatapointsToAlarm counts breaches required within that window. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Set the supplied metric, statistic, period, comparison operator, threshold and evaluation counts. Compare the resulting state with the supplied samples. ⟦A.f3 A:tb3 A:tb4⟧
(mechanism) Missing-data policies are breaching, notBreaching, ignore (retain current state), and missing (INSUFFICIENT_DATA when all datapoints are missing). The default is missing. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) EvaluationPeriods is not the required breach count. Default missing does not mean every isolated gap immediately produces INSUFFICIENT_DATA. ⟦A.f2 A.f4 A:tb5⟧
[TABLE ds.alarm_evaluation cols=['window_id', 'metric', 'statistic', 'period_seconds', 'comparison_operator', 'threshold', 'EvaluationPeriods', 'DatapointsToAlarm', 'period_1_sample', 'period_2_sample', 'period_3_sample', 'period_1_comparison', 'period_2_comparison', 'period_3_comparison', 'breach_count', 'missing_data_policy', 'prior_state', 'resulting_state'] ] caption: Revisit the same supplied evidence