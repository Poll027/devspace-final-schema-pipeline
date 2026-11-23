# EVALUATOR PACKET — Configure secure human access with temporary credentials (aws_devops.tile.027)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.configure_secure_human_access_with_temporary_credentials — Configure secure human access with temporary credentials

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.configure_secure_human_access_with_temporary_credentials)   objective: Grant secure human AWS access using IAM Identity Center
A.f1: IAM Identity Center permission sets define permissions made available through assignments to users or groups in specified AWS accounts.   [sources: aws_iam_user_guide#../../../singlesignon/latest/userguide/permissionsetsconcept.html]
A.f2: Use the supplied Identity Center assignment workflow to assign the approved user or group, account and permission set, then sign in to that account and test the intended access.   [sources: aws_iam_user_guide#../../../singlesignon/latest/userguide/assignusers.html]
A.f3: Configure a named SSO profile with aws configure sso and establish a session with aws sso login --profile NAME rather than storing long-lived IAM user keys.   [sources: aws_cli_user_guide#cli-configure-sso.html]
note: Use supplied assignments; do not create a new enterprise identity architecture.
PRACTICE ANCHOR (tool_simulation): Use the supplied Identity Center workflow to assign one approved permission set to a sandbox user in the specified account, sign in, and test the intended access. Configure a named SSO profile with aws configure sso and establish its session with aws sso login --profile NAME.  SUCCESS: The assignment matches the supplied user, account, and approved permission set. The user signs in to that account, and the supplied access test produces the expected result. The named SSO profile is configured and its session established without storing long-lived IAM user keys.
ASSESSMENT ANCHOR: verify_person_permission_set_assignment_and_intended_access facts=['f1', 'f2']
ASSESSMENT ANCHOR: establish_named_sso_profile_access_without_long_lived_user_keys facts=['f3']

## DATA ASSETS USED
ds.human_access: Approved assignment and access-test evidence — columns: case_id(identifier), user(identifier), operator_group(categorical), approved_account(identifier,digits-as-label), approved_permission_set(categorical), assigned_account(identifier,digits-as-label), assigned_permission_set(categorical), signed_in_account(identifier,digits-as-label), signed_in_permission_set(categorical), intended_access_test(text), expected_result(categorical), observed_result(categorical), profile_name(identifier), profile_configuration(text), session_evidence(text), credential_storage(categorical)
   ["access.complete","cedar-operator","cedar-operators",111111111111,"CedarObjectRead",111111111111,"CedarObjectRead",111111111111,"CedarObjectRead","Read sandbox evidence object","success","success","cedar-sandbox","aws configure sso; named profile cedar-sandbox configured","aws sso login --profile c
   ["access.sign_in_only","cedar-operator","cedar-operators",111111111111,"CedarObjectRead",111111111111,"CedarObjectRead",111111111111,"CedarObjectRead","Read sandbox evidence object","success","not tested","cedar-sandbox","aws configure sso; named profile cedar-sandbox configured","aws sso login --pr
   ["access.assignment_mismatch","cedar-operator","cedar-operators",111111111111,"CedarObjectRead",111111111111,"CedarOtherPermission",111111111111,"CedarOtherPermission","Read sandbox evidence object","success","not tested","cedar-sandbox","aws configure sso; named profile cedar-sandbox configured","a

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authorize an event target with least-privilege execution permissions; Automate prohibited-configuration checks; Cloudformation drift; Cloudformation rollback; Configure GitHub Actions AWS role federation; Configure a budget notification; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Ec2 instance profile; Eks workload identity; Evaluate resource-based permissions for a requested operation; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute an established managed account-onboarding workflow; Extract structured AWS CLI inventory across paginated results; Hand over an actionable operational runbook; Operate an EKS Pod using supplied cluster-access setup; Operate an RDS managed database as the native backup-resource foundation; Protect recoverable S3 objects with versioning and lifecycle controls; Publish a container image to ECR after external Docker preparation; Publish a traceable immutable build artifact; Read and modify a standard CloudFormation S3 template; directly require 

## LESSON, in learner order

### s01 · explainer · Approved assignment, session and access
Learn — 
(definition) Permissions are made available through IAM Identity Center permission-set assignments to users or groups in specified AWS accounts. An operator needs approved access, not saved long-lived IAM user keys. ⟦A.f1 A:tb1 A:tb2⟧
(workflow) Use the supplied assignment workflow to assign the approved user or group, account and permission set. Then sign in to that account and test the intended access. Keep the assignment, signed-in permission-set context and test result together: sign-in alone is not the complete access check. ⟦A.f1 A.f2 A:tb3 A:tb4 A:tb5⟧
(example) For cedar-operator in cedar-operators, compare the assigned account and permission set with the approved context. The intended test is read sandbox evidence object. Keep its expected and observed results alongside the signed-in context. ⟦A.f1 A.f2 A:tb4⟧
(mechanism) Configure a named SSO profile with aws configure sso. Establish its session with aws sso login --profile NAME, replacing NAME with the profile name. Use this session workflow rather than storing long-lived IAM user keys. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[DIAGRAM: Approved access context and test] nodes=['Approved assignment {User: cedar-operator; Group: cedar-operators; Account: 111111111111; Permission set: CedarObjectRead}', 'Assigned context {Account: 111111111111; Permission set: CedarObjectRead}', 'Signed-in context {Account: 111111111111; Permission set: CedarObjectRead}', 'Intended access {Read sandbox evidence object; Expected: success; Observed: success}', 'Named SSO profile {aws configure sso; named profile cedar-sandbox configured; aws sso login --profile cedar-sandbox; session established; no long-lived IAM user keys}'] edges=[('approved', 'assigned', 'Match approval'), ('assigned', 'signed', 'Sign in'), ('signed', 'test', 'Test intended access'), ('signed', 'profile', 'Use named session')] alt: Approved access context and test

### s02 · video · From assignment to signed-in context
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Choose the named-session workflow
Check your understanding — 

### s04 · hands_on · Review human-access evidence
Evidence review — Read the supplied assignment, sign-in, test and named-profile excerpts in this step. Decide which records demonstrate the approved access checks and which are defective.

### s05 · recap · Keep the evidence distinct
Takeaways — 
(takeaway) Permission sets make permissions available through user or group assignments in specified accounts. Match the approved assignment, sign in, and test intended access. Configure a named SSO profile and establish its session instead of storing long-lived IAM user keys. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Configure security groups after external ports/firewall preparation: Allow rules at associated network interfaces.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit the check
(misconception) Configure a named SSO profile with aws configure sso, then establish its session with aws sso login --profile NAME. Use the supplied profile’s name for NAME. This named-session workflow, rather than storing long-lived IAM user keys, is the required access approach. ⟦A.f3 A:tb3 A:tb5⟧
[TABLE ds.human_access cols=['case_id', 'user', 'operator_group', 'approved_account', 'approved_permission_set', 'assigned_account', 'assigned_permission_set', 'signed_in_account', 'signed_in_permission_set', 'intended_access_test', 'expected_result', 'observed_result', 'profile_name', 'profile_configuration', 'session_evidence', 'credential_storage'] ] caption: Approved assignment and access-test evidence
### r02 · Revisit the evidence review
(misconception) Permission sets define permissions made available through assignments to users or groups in specified accounts. Match the approved user or group, account and permission set using the supplied workflow, then sign in and test intended access. Compare a completed test with sign-in alone: an untested operation is not a completed access check. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Keep the named SSO profile configuration and session evidence too: aws configure sso configures the profile; aws sso login --profile NAME establishes its session. Use that session workflow rather than saving long-lived IAM user keys. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.human_access cols=['case_id', 'user', 'operator_group', 'approved_account', 'approved_permission_set', 'assigned_account', 'assigned_permission_set', 'signed_in_account', 'signed_in_permission_set', 'intended_access_test', 'expected_result', 'observed_result', 'profile_name', 'profile_configuration', 'session_evidence', 'credential_storage'] ] caption: Approved assignment and access-test evidence

=========

# EVALUATOR PACKET — Configure security groups after external ports/firewall preparation (aws_devops.tile.028)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.configure_security_groups — Configure security groups after external ports/firewall preparation

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.configure_security_groups)   objective: Configure AWS security-group rules to enforce required workload flows and an approved ingress baseline
A.f1: Security groups contain allow rules for traffic evaluated at associated network interfaces; they have no explicit deny rules.   [sources: aws_vpc_user_guide#vpc-security-groups.html]
A.f2: Security groups are stateful: response traffic for an allowed connection is allowed regardless of rules in the response direction.   [sources: aws_vpc_user_guide#vpc-security-groups.html]
A.f3: Add inbound rules specifying the required protocol, port range and approved source, remove unnecessary ingress, and test the required connections and their responses.   [sources: aws_vpc_user_guide#security-group-rules.html]
A.m1 (misconception): Using a security-group ID as an allowed source does not import the referenced group’s rules into the destination group.   [sources: aws_vpc_user_guide#security-group-rules.html#security-group-referencing]
note: Keep DNS/IMDS filtering exceptions explicit; do not imply security groups filter every AWS-service flow.
PRACTICE ANCHOR (tool_simulation): Configure one EC2 workload security group using a supplied approved baseline requiring TCP port 443 from an approved source range. Add the required inbound rule, remove unnecessary ingress, and use supplied connection tests to verify the required connection and its stateful response.  SUCCESS: The security group associated with the workload network interface admits TCP port 443 from the approved source range and contains no unnecessary inbound rules. Supplied tests confirm that the approved connection and its response succeed without a separate response-direction allow rule, while a new connection from an unapproved source is not admitted.
ASSESSMENT ANCHOR: determine_allow_only_rules_at_associated_network_interfaces facts=['f1']
ASSESSMENT ANCHOR: determine_stateful_response_traffic_behavior facts=['f2']
ASSESSMENT ANCHOR: enforce_approved_ingress_and_verify_required_connections facts=['f3']
ASSESSMENT ANCHOR: interpret_source_group_references_without_importing_rules facts=['m1']

## DATA ASSETS USED
ds.connection_tests: Security-group connection and response evidence — columns: test_id(identifier), network_interface(identifier), destination_group(identifier), traffic_case(categorical), protocol(categorical), port(identifier,digits-as-label), source(text), inbound_rule(text), response_direction_rule(text), observed_result(categorical), interpretation(text)
   ["net.approved","eni-cedar-workload","sg-cedar-workload","new connection","TCP",443,"approved source range: 192.0.2.0/24","allow TCP 443 from 192.0.2.0/24","none","connection succeeds","Approved inbound traffic"]
   ["net.response","eni-cedar-workload","sg-cedar-workload","tracked response","TCP",443,"workload response to allowed tracked connection","allow TCP 443 from 192.0.2.0/24","none","response succeeds","Stateful response; no separate response-direction allow required"]
   ["net.unapproved","eni-cedar-workload","sg-cedar-workload","new connection","TCP",443,"unapproved source range: 198.51.100.0/24","allow TCP 443 from 192.0.2.0/24","none","not admitted","No matching inbound allow"]
   ["net.group_reference","eni-cedar-workload","sg-cedar-workload","new connection","TCP",443,"sg-cedar-source","allow TCP 443 from sg-cedar-source","none","connection succeeds","Source-group reference identifies allowed source; does not import its rules"]
   ["net.dns","eni-cedar-workload","sg-cedar-workload","Amazon-provided DNS","not specified",null,"workload","not used for this traffic","not used for this traffic","outside security-group filtering","Do not infer filtering from this traffic"]
   ["net.metadata","eni-cedar-workload","sg-cedar-workload","instance metadata","not specified",null,"workload","not used for this traffic","not used for this traffic","outside security-group filtering","Do not infer filtering from this traffic"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authorize an event target with least-privilege execution permissions; Automate prohibited-configuration checks; Cloudformation drift; Cloudformation rollback; Configure GitHub Actions AWS role federation; Configure a CodeBuild buildspec for a supplied application; Configure a budget notification; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Ec2 instance profile; Eks workload identity; Evaluate resource-based permissions for a requested operation; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute an established managed account-onboarding workflow; Extract structured AWS CLI inventory across paginated results; Hand over an actionable operational runbook; Operate an EKS Pod using supplied cluster-access setup; Operate an RDS managed database as the native backup-resource foundation; Protect recoverable S3 objects with versioning and lifecycle controls; Publish a container image to ECR after external Docker preparation; Publish a traceable immutable build artifact; Read and modify a standard CloudFormation S3 template; directly require the nativ

## LESSON, in learner order

### s01 · explainer · Allow the required connection
Learn — 
(definition) Security groups contain allow rules evaluated at associated network interfaces, not explicit deny rules. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) They are stateful: responses to allowed connections are allowed regardless of response-direction rules. Add inbound rules for the required protocol, port range and approved source; remove unnecessary ingress, then test required connections and responses. ⟦A.f2 A.f3 A:tb3⟧
[DIAGRAM: Connection, tracked response and filtering boundary] nodes=['approved source range: 192.0.2.0/24', 'eni-cedar-workload {sg-cedar-workload; allow TCP 443 from 192.0.2.0/24}', 'tracked response {response succeeds}', 'unapproved source range: 198.51.100.0/24 {not admitted}', 'sg-cedar-source {Identifies source; no rule import}', 'Outside filtering {Amazon-provided DNS; instance metadata}'] edges=[('source', 'eni', 'TCP 443: connection succeeds'), ('eni', 'response', 'Allowed regardless of response-direction rules'), ('other', 'eni', 'No matching inbound allow'), ('group', 'eni', 'Allowed source reference')] alt: Connection, tracked response and filtering boundary

### s02 · explainer · Keep the filtering boundary clear
Learn — 
(example) Use the supplied TCP ingress rule and approved source on the workload’s associated security group. Remove unnecessary ingress and test both the required connection and its response. A tracked response is allowed regardless of response-direction rules; a new connection from an unapproved source is a different case. Do not widen ingress to make an unexplained test pass. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) A security-group ID used as an allowed source identifies that source; it does not import the referenced group’s rules into the destination group. Security groups contain allow rules, not explicit deny rules. ⟦A.f1 A.m1 A:tb4 A:tb5 A:tb6⟧
(misconception) Security groups do not filter traffic to Amazon-provided DNS or EC2 instance metadata services. Those cases are outside the filtering boundary, so their results do not demonstrate that ordinary ingress is allowed. ⟦A.f4 A:tb4 A:tb5 A:tb6⟧
[TABLE ds.connection_tests cols=['test_id', 'network_interface', 'destination_group', 'traffic_case', 'protocol', 'port', 'source', 'inbound_rule', 'response_direction_rule', 'observed_result', 'interpretation'] ] caption: Compare supplied connection cases, not DNS or metadata as ingress evidence.

### s03 · check · Distinguish response from new ingress
Check your understanding — 

### s04 · hands_on · Review connection-rule evidence
Evidence review — Read the supplied connection and rule excerpts in this step. Decide which interpretations correctly enforce approved ingress and interpret source-group references.

### s05 · recap · Keep the evidence distinct
Takeaways — 
(takeaway) Security groups use allow rules at associated network interfaces. Tracked responses are statefully allowed. Use required protocol, port range and approved source, remove unnecessary ingress, and test connections and responses. Source-group references do not import rules; DNS and metadata traffic are outside security-group filtering. ⟦A.f1 A.f2 A.f3 A.f4 A.m1 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
[UP NEXT] Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation: An approved provider pin and a supplied EC2 declaration.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit the check
(misconception) Security groups are stateful. A tracked response to an allowed connection is allowed regardless of response-direction rules. Contrast that response with a new connection from an unapproved source: the response is not a fresh ingress request needing a separate response-direction allow. ⟦A.f2 A:tb3 A:tb4⟧
[TABLE ds.connection_tests cols=['test_id', 'network_interface', 'destination_group', 'traffic_case', 'protocol', 'port', 'source', 'inbound_rule', 'response_direction_rule', 'observed_result', 'interpretation'] ] caption: Security-group connection and response evidence
### r02 · Revisit the evidence review
(misconception) Security groups contain allow rules at associated network interfaces, not explicit deny rules. Specify the required protocol, port range and approved source, remove unnecessary ingress, then test the required connections and responses. Compare a matching approved-source rule with a new unapproved-source connection that has no matching inbound allow. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) A source-group ID identifies an allowed source without importing that group’s rule list. Compare a source reference with rule import: only the former describes the supplied evidence. ⟦A.m1 A:tb4 A:tb5 A:tb6⟧
[TABLE ds.connection_tests cols=['test_id', 'network_interface', 'destination_group', 'traffic_case', 'protocol', 'port', 'source', 'inbound_rule', 'response_direction_rule', 'observed_result', 'interpretation'] ] caption: Security-group connection and response evidence

=========

# EVALUATOR PACKET — Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation (aws_devops.tile.029)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.define_an_ec2_instance_with_terraform_hcl_and_a_pinned_provider — Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.define_an_ec2_instance_with_terraform_hcl_and_a_pinned_provider)   objective: Declare an EC2 instance in Terraform
A.f1: Pin the approved provider version with this declaration, substituting the approved version:
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "= APPROVED_VERSION"
    }
  }
}   [sources: terraform_language#providers/requirements]
A.f2: Declare resource "aws_instance" "NAME" with ami, instance_type and subnet_id set to the supplied values.   [sources: terraform_aws_provider#resources/instance#argument-reference]
A.f3: Run terraform init to install providers, terraform plan to inspect intended changes, and the approved terraform apply step to create the instance; verify the instance settings.   [sources: terraform_language#../cli/run, terraform_language#../cli/commands/init, terraform_language#../cli/commands/plan, terraform_language#../cli/commands/apply]
note: Treat the HCL as a substitution template, not runnable with APPROVED_VERSION; do not introduce modules or backend configuration yet.
PRACTICE ANCHOR (live_code): Write a minimal Terraform configuration that pins the supplied approved AWS provider version and declares one aws_instance with the supplied AMI, instance type and subnet ID. Initialize providers, inspect the plan, perform the approved apply step in the sandbox, and verify the resulting instance settings.  SUCCESS: The configuration uses the exact approved provider version and supplied instance values. Initialization succeeds, the plan proposes one intended EC2 instance, and the approved apply creates an instance whose AMI, instance type and subnet ID match the specification.
ASSESSMENT ANCHOR: verify_exact_approved_provider_pin facts=['f1']
ASSESSMENT ANCHOR: verify_declared_ec2_settings_against_supplied_values facts=['f2']
ASSESSMENT ANCHOR: verify_planned_ec2_instance_matches_specification facts=['f2', 'f3']
ASSESSMENT ANCHOR: distinguish_initialization_planning_creation_and_verification facts=['f3']

## DATA ASSETS USED
ds.terraform_execution: Separate declaration from execution evidence — columns: sequence(numerical), command(text), review_evidence(text), approval_evidence(text), result(text)
   [1,"terraform init","Provider installation checked","Not the apply step","Provider installation succeeded"]
   [2,"terraform plan","Planned instance values match supplied specification","Not the apply step","One intended EC2 instance proposed"]
   [3,"terraform apply","Reviewed intended instance change","Supplied apply approval recorded","Instance creation completed; resulting settings compared"]
ds.terraform_settings: Terraform specification, declaration, plan and verification — columns: evidence_stage(categorical), provider_source(categorical), provider_version(categorical), resource_type(categorical), resource_label(identifier), ami(identifier), instance_type(categorical), subnet_id(identifier)
   ["supplied specification","hashicorp/aws","6.0.0","aws_instance","cedar_workload","ami-00000000000000001","t3.micro","subnet-00000000000000001"]
   ["HCL declaration","hashicorp/aws","6.0.0","aws_instance","cedar_workload","ami-00000000000000001","t3.micro","subnet-00000000000000001"]
   ["inspected plan","hashicorp/aws","6.0.0","aws_instance","cedar_workload","ami-00000000000000001","t3.micro","subnet-00000000000000001"]
   ["verified instance settings","hashicorp/aws","6.0.0","aws_instance","cedar_workload","ami-00000000000000001","t3.micro","subnet-00000000000000001"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authorize an event target with least-privilege execution permissions; Automate prohibited-configuration checks; Cloudformation drift; Cloudformation rollback; Configure GitHub Actions AWS role federation; Configure a CodeBuild buildspec for a supplied application; Configure a CodeDeploy deployment action for a supplied EC2 application; Configure a budget notification; Ec2 instance profile; Eks workload identity; Evaluate resource-based permissions for a requested operation; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute an established managed account-onboarding workflow; Extract structured AWS CLI inventory across paginated results; Hand over an actionable operational runbook; Operate an EKS Pod using supplied cluster-access setup; Operate an RDS managed database as the native backup-resource foundation; Protect recoverable S3 objects with versioning and lifecycle controls; Publish a container image to ECR after external Docker preparation; Publish a traceable immutable build artifact; Read and modify a standard CloudFormation S3 template; directly require the native S3 object-storage concept; Retrieve a manag

## LESSON, in learner order

### s01 · explainer · Pin and declare the supplied instance
Learn — 
(definition) Pin the approved hashicorp/aws version in terraform.required_providers. Declare resource "aws_instance" "NAME" with the supplied ami, instance_type and subnet_id; NAME is the chosen resource label. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3⟧
(workflow) Run terraform init to install providers, terraform plan to inspect intended changes, and the approved terraform apply step to create the instance. Verify the resulting instance settings. ⟦A.f3 A:tb3⟧
[SIDE_BY_SIDE] Compare the same supplied values at each evidence stage. left_label: Exact provider pin and resource | right_label: Specification, declaration, plan and verified settings
  left:
[DIAGRAM: Exact provider pin and supplied resource] nodes=['HCL declaration {terraform {;   required_providers {;     aws = {;       source = "hashicorp/aws";       version = "= 6.0.0";     };   }; }; resource "aws_instance" "cedar_workload" {;   ami = "ami-00000000000000001";   instance_type = "t3.micro";   subnet_id = "subnet-00000000000000001"; }}'] edges=[] alt: Exact provider pin and supplied resource
  right:
[TABLE ds.terraform_settings cols=['evidence_stage', 'provider_source', 'provider_version', 'resource_type', 'resource_label', 'ami', 'instance_type', 'subnet_id'] ] caption: Terraform specification, declaration, plan and verification

### s02 · explainer · Compare declaration with execution
Learn — 
(syntax) Use this exact approved provider declaration:

```hcl
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "= 6.0.0"
    }
  }
}
``` ⟦A.f1 A:tb2 A:tb4⟧
(example) Compare the exact provider pin and resource settings against the supplied specification, then compare the inspected plan with those same values before the approved apply step. Keep provider selection, declaration, plan and verified instance settings separate in the evidence. The native EC2 foundation comes before interpreting these settings. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) A plausible declaration and provider pin are not execution evidence. Initialization installs providers; planning inspects intended changes; the approved apply creates the instance. Completion still needs verification of the resulting instance settings, not just a matching declaration. Use the supplied version and bounded resource settings rather than designing different infrastructure. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧
[TABLE ds.terraform_execution cols=['sequence', 'command', 'review_evidence', 'approval_evidence', 'result'] ] caption: Separate declaration from execution evidence

### s03 · check · Separate Terraform execution stages
Check your understanding — 

### s04 · hands_on · Review Terraform provisioning evidence
Evidence review — Read the supplied declaration and execution excerpts in this step. Decide which records correctly show the approved pin, supplied instance settings and verified provisioning.

### s05 · recap · Keep the evidence distinct
Takeaways — 
(takeaway) Pin the approved provider version and declare the supplied EC2 settings. Initialization installs providers, planning inspects changes, and the approved apply creates the instance. Verify the resulting settings: declaration alone is not execution evidence. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Evaluate resource-based permissions for a requested operation: A resource policy attached to the requested resource.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit the check
(misconception) terraform init installs providers. terraform plan inspects intended changes. The approved terraform apply step creates the instance, after which the instance settings must be verified. Compare a declaration with verified live settings: the declaration alone is not execution evidence. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.terraform_execution cols=['sequence', 'command', 'review_evidence', 'approval_evidence', 'result'] ] caption: Separate declaration from execution evidence
### r02 · Revisit the evidence review
(misconception) Use the exact approved version in the hashicorp/aws required_providers declaration, then declare resource "aws_instance" "NAME" with the supplied ami, instance_type and subnet_id. Compare the declaration and plan with the specification rather than substituting different settings. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4⟧
(syntax) Use this exact approved provider declaration:

```hcl
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "= 6.0.0"
    }
  }
}
``` ⟦A.f1 A:tb2 A:tb4⟧
(misconception) Initialization installs providers, planning inspects intended changes, and the approved apply creates the instance. Verification needs the resulting instance settings. A matching declaration is not the same as verified provisioning evidence. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.terraform_settings cols=['evidence_stage', 'provider_source', 'provider_version', 'resource_type', 'resource_label', 'ami', 'instance_type', 'subnet_id'] ] caption: Terraform specification, declaration, plan and verification
[TABLE ds.terraform_execution cols=['sequence', 'command', 'review_evidence', 'approval_evidence', 'result'] ] caption: Separate declaration from execution evidence

=========

# EVALUATOR PACKET — Evaluate resource-based permissions for a requested operation (aws_devops.tile.030)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.evaluate_resource_based_permissions_for_a_requested_operation — Evaluate resource-based permissions for a requested operation

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.evaluate_resource_based_permissions_for_a_requested_operation)   objective: Evaluate AWS resource-based permissions
A.f1: A resource-based policy is attached to a resource and specifies the principals, actions and resources covered by its statements.   [sources: aws_iam_user_guide#access_policies_identity-vs-resource.html]
A.f2: For an S3 bucket policy, compare Principal, Action, Resource and Condition with the caller’s request; bucket and object ARNs identify different resource scopes.   [sources: aws_iam_user_guide#access_policies_identity-vs-resource.html]
A.f3: Same-account identity and resource permissions can contribute allows, but applicable explicit denies override them; cross-account access generally requires permission on both sides.   [sources: aws_iam_user_guide#reference_policies_evaluation-logic.html]
note: Preserve generally for cross-account requirements; avoid advanced grant exceptions not in this brief.
PRACTICE ANCHOR (field_selection): Evaluate one supplied S3 bucket policy against object requests from approved and unapproved callers. Select the matching Principal, Action, Resource and Condition evidence, then use supplied identity-permission and explicit-deny evidence to determine whether each request is permitted.  SUCCESS: For each request, correctly identify which policy fields match, distinguish bucket scope from object scope, and record the permission outcome. An applicable explicit deny overrides allows; same-account permissions can contribute allows, while cross-account access generally requires permission on both sides.
ASSESSMENT ANCHOR: match_resource_policy_statements_to_supplied_requests facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_bucket_and_object_arn_scopes facts=['f2']
ASSESSMENT ANCHOR: evaluate_contributed_allows_and_explicit_deny_precedence facts=['f3']
ASSESSMENT ANCHOR: determine_general_cross_account_permission_requirements facts=['f3']

## DATA ASSETS USED
ds.bucket_policy: Supplied S3 resource-policy fields — columns: statement_id(identifier), Effect(categorical), Principal(text), Action(categorical), Resource(text), Condition(text)
   ["same_account_read","Allow","arn:aws:iam::111111111111:role/CedarReader","s3:GetObject","arn:aws:s3:::cedar-sandbox-evidence/*","aws:SecureTransport = true"]
   ["cross_account_read","Allow","arn:aws:iam::222222222222:role/CedarReader","s3:GetObject","arn:aws:s3:::cedar-sandbox-evidence/*","aws:SecureTransport = true"]
ds.object_requests: S3 caller, request fields and supplied permission evidence — columns: request_id(identifier), Principal(text), Action(categorical), Resource(text), Condition(text), account_relationship(categorical), identity_allow(categorical), resource_allow(categorical), explicit_deny(categorical), permission_outcome(categorical), evidence_note(text)
   ["request.same","arn:aws:iam::111111111111:role/CedarReader","s3:GetObject","arn:aws:s3:::cedar-sandbox-evidence/evidence.txt","aws:SecureTransport = true","same-account","absent","matching","none applicable","permitted","Matching resource allow contributes permission"]
   ["request.denied","arn:aws:iam::111111111111:role/CedarReader","s3:GetObject","arn:aws:s3:::cedar-sandbox-evidence/evidence.txt","aws:SecureTransport = true","same-account","matching","matching","applicable supplied explicit deny","not permitted","Applicable explicit deny overrides contributed allow
   ["request.cross_both","arn:aws:iam::222222222222:role/CedarReader","s3:GetObject","arn:aws:s3:::cedar-sandbox-evidence/evidence.txt","aws:SecureTransport = true","cross-account","matching","matching","none applicable","permitted","Supplied ordinary cross-account case: permission on both sides"]
   ["request.cross_missing","arn:aws:iam::222222222222:role/CedarReader","s3:GetObject","arn:aws:s3:::cedar-sandbox-evidence/evidence.txt","aws:SecureTransport = true","cross-account","absent","matching","none applicable","not permitted","Supplied ordinary cross-account case lacks identity-side permiss
   ["request.unapproved","arn:aws:iam::222222222222:role/CedarUnapproved","s3:GetObject","arn:aws:s3:::cedar-sandbox-evidence/evidence.txt","aws:SecureTransport = true","cross-account","matching","no matching principal","none applicable","not permitted","Resource-side principal does not match"]
   ["request.bucket_scope","arn:aws:iam::111111111111:role/CedarReader","s3:GetObject","arn:aws:s3:::cedar-sandbox-evidence","aws:SecureTransport = true","same-account","absent","no matching object scope","none applicable","not permitted","Bucket ARN differs from object ARN; does not match the supplied
   ["request.condition","arn:aws:iam::111111111111:role/CedarReader","s3:GetObject","arn:aws:s3:::cedar-sandbox-evidence/evidence.txt","aws:SecureTransport = false","same-account","absent","no matching condition","none applicable","not permitted","Supplied condition does not match"]
   ["request.action","arn:aws:iam::111111111111:role/CedarReader","s3:DeleteObject","arn:aws:s3:::cedar-sandbox-evidence/evidence.txt","aws:SecureTransport = true","same-account","absent","no matching action","none applicable","not permitted","Supplied read action does not match the requested operation

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authorize an event target with least-privilege execution permissions; Automate prohibited-configuration checks; Cloudformation drift; Cloudformation rollback; Configure GitHub Actions AWS role federation; Configure a CodeBuild buildspec for a supplied application; Configure a CodeDeploy deployment action for a supplied EC2 application; Configure a budget notification; Configure and verify an EC2 Auto Scaling policy under bounded load; Ec2 instance profile; Eks workload identity; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute an established managed account-onboarding workflow; Extract structured AWS CLI inventory across paginated results; Hand over an actionable operational runbook; Operate an EKS Pod using supplied cluster-access setup; Operate an RDS managed database as the native backup-resource foundation; Protect recoverable S3 objects with versioning and lifecycle controls; Publish a container image to ECR after external Docker preparation; Publish a traceable immutable build artifact; Read and modify a standard CloudFormation S3 template; directly require the native S3 object-storage concept; Retrieve a 

## LESSON, in learner order

### s01 · explainer · Match a request to its resource policy
Learn — 
(definition) A resource-based policy is attached to a resource and specifies the principals, actions and resources covered by its statements. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) For an S3 bucket policy, compare Principal, Action, Resource and Condition with the request. Bucket and object ARNs have different scopes. Same-account identity and resource permissions can contribute allows; applicable explicit denies override them. Cross-account access generally requires permission on both sides. ⟦A.f2 A.f3 A:tb3⟧
[DIAGRAM: Caller, statement fields and distinct ARN scopes] nodes=['arn:aws:iam::111111111111:role/CedarReader', 'Request {Action: s3:GetObject; Resource: arn:aws:s3:::cedar-sandbox-evidence/evidence.txt; Condition: aws:SecureTransport = true}', 'Attached bucket policy {Principal: arn:aws:iam::111111111111:role/CedarReader; Action: s3:GetObject; Resource: arn:aws:s3:::cedar-sandbox-evidence/*; Condition: aws:SecureTransport = true}', 'Bucket scope {arn:aws:s3:::cedar-sandbox-evidence}', 'Object scope {arn:aws:s3:::cedar-sandbox-evidence/evidence.txt}', 'Permission evaluation {Same-account allows can contribute; Explicit deny overrides; Cross-account generally needs both sides}'] edges=[('caller', 'request', 'Principal'), ('request', 'policy', 'Compare four fields'), ('policy', 'bucket', 'Attached to bucket'), ('request', 'object', 'Requested object'), ('policy', 'allows', 'Combine supplied evidence')] alt: Caller, statement fields and distinct ARN scopes

### s02 · explainer · Use scope and permission evidence
Learn — 
(example) Compare the caller with Principal, the operation with Action, the object ARN with Resource, and request values with Condition. A bucket ARN is not automatically the scope of an object request. A resource policy includes principal scope; it is not just an identity policy moved to another file. ⟦A.f1 A.f2 A:tb4 A:tb5⟧
(misconception) Use the supplied permission evidence alongside the field matches. In a same-account request, identity and resource permissions can contribute allows, but an applicable explicit deny overrides them. For cross-account access, permission is generally required on both sides. Keep that qualification: the supplied ordinary cases are not an exhaustive account of special cases. ⟦A.f3 A:tb4 A:tb5⟧
[TABLE ds.bucket_policy cols=['statement_id', 'Effect', 'Principal', 'Action', 'Resource', 'Condition'] ] caption: Supplied S3 resource-policy fields
[TABLE ds.object_requests cols=['request_id', 'Principal', 'Action', 'Resource', 'Condition', 'account_relationship', 'identity_allow', 'resource_allow', 'explicit_deny', 'permission_outcome', 'evidence_note'] ] caption: S3 caller, request fields and supplied permission evidence

### s03 · check · Judge cross-account permission evidence
Check your understanding — 

### s04 · hands_on · Review policy and request fields
Evidence review — Read the supplied policy and request evidence. Select the matching fields and permission evidence, keeping bucket scope distinct from object scope.

### s05 · recap · Keep the evidence distinct
Takeaways — 
(takeaway) Match Principal, Action, Resource and Condition to the request. Distinguish bucket from object scope. Same-account permissions can contribute allows, but applicable explicit denies override them. Cross-account access generally needs permission on both sides. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Execute an established managed account-onboarding workflow: Standardized account provisioning and enrollment.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit the check
(misconception) Same-account identity and resource permissions can contribute allows, but applicable explicit denies override them. Cross-account access generally requires permission on both sides. Compare the supplied cross-account cases with both sides allowing and with identity-side permission absent; do not treat a resource-side allow as generally sufficient by itself. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.object_requests cols=['request_id', 'Principal', 'Action', 'Resource', 'Condition', 'account_relationship', 'identity_allow', 'resource_allow', 'explicit_deny', 'permission_outcome', 'evidence_note'] ] caption: S3 caller, request fields and supplied permission evidence
### r02 · Revisit the evidence review
(misconception) A resource policy is attached to a resource and specifies principals, actions and resource scope. Match the request’s Principal, Action, Resource and Condition to the S3 policy. Compare the bucket ARN with the object ARN: they identify different scopes. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(misconception) Same-account identity and resource permissions can contribute allows, but an applicable explicit deny overrides them. Cross-account permission is generally needed on both sides. Matching policy fields alone do not replace the supplied identity-permission and deny evidence. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.bucket_policy cols=['statement_id', 'Effect', 'Principal', 'Action', 'Resource', 'Condition'] ] caption: Supplied S3 resource-policy fields
[TABLE ds.object_requests cols=['request_id', 'Principal', 'Action', 'Resource', 'Condition', 'account_relationship', 'identity_allow', 'resource_allow', 'explicit_deny', 'permission_outcome', 'evidence_note'] ] caption: S3 caller, request fields and supplied permission evidence

=========

# EVALUATOR PACKET — Execute an established managed account-onboarding workflow (aws_devops.tile.031)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.execute_an_established_managed_account_onboarding_workflow — Execute an established managed account-onboarding workflow

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.execute_an_established_managed_account_onboarding_workflow)   objective: Execute managed-account onboarding
A.f1: Account Factory provisions and enrolls accounts into a governed landing zone using standardized account settings.   [sources: aws_control_tower_user_guide#account-factory.html]
A.f2: Execute the established provisioning workflow with the approved account inputs and inspect the account’s enrollment and organizational-unit placement.   [sources: aws_control_tower_user_guide#methods-of-provisioning.html]
A.f3: Verify the supplied baseline checkpoints against the account’s applied controls; creating an account alone does not demonstrate governance completion.   [sources: aws_control_tower_user_guide#how-controls-work.html]
note: Execute the established workflow only; do not design a landing zone or invent baseline controls.
PRACTICE ANCHOR (tool_simulation): Run the established Account Factory onboarding workflow for one sandbox account using supplied approved inputs, then inspect enrollment, organizational-unit placement and baseline outputs.  SUCCESS: The workflow uses the approved account settings. The resulting account's enrollment and organizational-unit placement match the supplied expectations, and each baseline checkpoint is compared with evidence of the account's applied controls. Any checkpoint without supporting evidence is recorded as unverified rather than treating account creation as governance completion.
ASSESSMENT ANCHOR: verify_account_factory_enrollment_and_organizational_unit_placement facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_supplied_baseline_checkpoints_against_applied_controls facts=['f3']
ASSESSMENT ANCHOR: distinguish_account_creation_from_verified_governance_completion facts=['f2', 'f3']

## DATA ASSETS USED
ds.onboarding_checkpoints: Managed-account inputs and governance evidence — columns: case_id(identifier), account_name(identifier), account_id(identifier,digits-as-label), approved_inputs(text), observed_inputs(text), creation_result(categorical), expected_enrollment(categorical), observed_enrollment(categorical), expected_organizational_unit(categorical), observed_organizational_unit(categorical), checkpoint_id(identifier), supplied_baseline_checkpoint(text), applied_control_evidence(text), verification_status(categorical)
   ["onboard.complete","cedar-sandbox",111111111111,"account cedar-sandbox; OU CedarSandbox","account cedar-sandbox; OU CedarSandbox","created","enrolled","enrolled","CedarSandbox","CedarSandbox","baseline.a","Compare supplied checkpoint A with its applied-control result","Supplied checkpoint A result 
   ["onboard.complete","cedar-sandbox",111111111111,"account cedar-sandbox; OU CedarSandbox","account cedar-sandbox; OU CedarSandbox","created","enrolled","enrolled","CedarSandbox","CedarSandbox","baseline.b","Compare supplied checkpoint B with its applied-control result","Supplied checkpoint B result 
   ["onboard.incomplete","cedar-sandbox",111111111111,"account cedar-sandbox; OU CedarSandbox","account cedar-sandbox; OU CedarSandbox","created","enrolled","enrolled","CedarSandbox","CedarSandbox","baseline.a","Compare supplied checkpoint A with its applied-control result","Supplied checkpoint A resul
   ["onboard.incomplete","cedar-sandbox",111111111111,"account cedar-sandbox; OU CedarSandbox","account cedar-sandbox; OU CedarSandbox","created","enrolled","enrolled","CedarSandbox","CedarSandbox","baseline.b","Compare supplied checkpoint B with its applied-control result",null,"unverified"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authorize an event target with least-privilege execution permissions; Automate prohibited-configuration checks; Cloudformation drift; Cloudformation rollback; Configure GitHub Actions AWS role federation; Configure a CodeBuild buildspec for a supplied application; Configure a CodeDeploy deployment action for a supplied EC2 application; Configure a budget notification; Configure and verify an EC2 Auto Scaling policy under bounded load; Configure artifact repository access; Ec2 instance profile; Eks workload identity; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Extract structured AWS CLI inventory across paginated results; Hand over an actionable operational runbook; Operate an EKS Pod using supplied cluster-access setup; Operate an RDS managed database as the native backup-resource foundation; Protect recoverable S3 objects with versioning and lifecycle controls; Publish a container image to ECR after external Docker preparation; Publish a traceable immutable build artifact; Read and modify a standard CloudFormation S3 template; directly require the native S3 object-storage concept; Retrieve a managed workload secre

## LESSON, in learner order

### s01 · explainer · Creation is not governance completion
Learn — 
(definition) Account Factory provisions and enrolls accounts into a governed landing zone using standardized account settings. The onboarding request supplies approved inputs and baseline checkpoints; creation is only part of the task. ⟦A.f1 A:tb1 A:tb2⟧
(workflow) Execute the established provisioning workflow with the approved account inputs. Inspect enrollment and organizational-unit placement, then verify each supplied baseline checkpoint against evidence of the account’s applied controls. Do not invent new baseline controls. ⟦A.f2 A.f3 A:tb3 A:tb4⟧
(misconception) If the account was created but a checkpoint has no supporting result, record that distinction. Creation, enrollment and placement do not replace the checkpoint comparison. A created account alone does not demonstrate governance completion. ⟦A.f2 A.f3 A:tb4 A:tb5⟧
[DIAGRAM: Account onboarding evidence, not creation alone] nodes=['Approved inputs {account cedar-sandbox; OU CedarSandbox}', 'Account creation {cedar-sandbox; 111111111111; created}', 'Enrollment {Expected: enrolled; Observed: enrolled}', 'Organizational-unit placement {Expected: CedarSandbox; Observed: CedarSandbox}', 'Baseline evidence {Compare supplied checkpoint A with its applied-control result; Compare supplied checkpoint B with its applied-control result}', 'Alternative evidence cases {onboard.complete: baseline.a: Supplied checkpoint A result matches; verified; onboard.complete: baseline.b: Supplied checkpoint B result matches; verified; onboard.incomplete: baseline.a: Supplied checkpoint A result matches; verified; onboard.incomplete: baseline.b: No supporting result; unverified}'] edges=[('inputs', 'created', 'Established workflow'), ('created', 'enrolled', 'Inspect'), ('enrolled', 'ou', 'Inspect'), ('ou', 'checkpoints', 'Verify applied controls'), ('checkpoints', 'contrast', 'Compare each checkpoint')] alt: Account onboarding evidence, not creation alone

### s02 · check · Distinguish creation from governance
Check your understanding — 

### s03 · hands_on · Review managed-account onboarding evidence
Evidence review — Read the supplied onboarding excerpts in this step. Decide which records demonstrate enrollment, placement and baseline verification, and which leave governance unverified.

### s04 · recap · Keep the evidence distinct
Takeaways — 
(takeaway) Account Factory provisions and enrolls accounts using standardized settings. Use approved inputs, inspect enrollment and organizational-unit placement, then compare every supplied baseline checkpoint with applied-control evidence. Account creation alone does not demonstrate governance completion. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Execute Python AWS automation in an isolated dependency environment after active registry language preparation: Next: Python AWS automation in an isolated dependency environment.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit the check
(misconception) Use approved inputs in the established onboarding workflow, inspect enrollment and organizational-unit placement, and compare supplied baseline checkpoints against applied-control evidence. Contrast creation completed with every checkpoint verified: creation alone does not demonstrate governance completion. Keep a checkpoint without supporting evidence unverified. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.onboarding_checkpoints cols=['case_id', 'account_name', 'account_id', 'approved_inputs', 'observed_inputs', 'creation_result', 'expected_enrollment', 'observed_enrollment', 'expected_organizational_unit', 'observed_organizational_unit', 'checkpoint_id', 'supplied_baseline_checkpoint', 'applied_control_evidence', 'verification_status'] ] caption: Managed-account inputs and governance evidence
### r02 · Revisit the evidence review
(misconception) Account Factory provisions and enrolls accounts into a governed landing zone using standardized settings. Use the established workflow with approved inputs; inspect enrollment and organizational-unit placement. Compare each supplied baseline checkpoint with applied-control evidence. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4⟧
(misconception) A created, enrolled account with correct placement still differs from an account whose supplied checkpoints all have supporting results. Record a missing checkpoint result as unverified rather than declaring governance complete. ⟦A.f2 A.f3 A:tb4 A:tb5⟧
[TABLE ds.onboarding_checkpoints cols=['case_id', 'account_name', 'account_id', 'approved_inputs', 'observed_inputs', 'creation_result', 'expected_enrollment', 'observed_enrollment', 'expected_organizational_unit', 'observed_organizational_unit', 'checkpoint_id', 'supplied_baseline_checkpoint', 'applied_control_evidence', 'verification_status'] ] caption: Managed-account inputs and governance evidence