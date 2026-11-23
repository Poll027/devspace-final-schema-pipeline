# EVALUATOR PACKET — Configure secure human access with temporary credentials (aws_devops.tile.027)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.configure_secure_human_access_with_temporary_credentials — Configure secure human access with temporary credentials

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.configure_secure_human_access_with_temporary_credentials)   objective: Grant secure human AWS access using IAM Identity Center
A.f1: IAM Identity Center permission sets define permissions made available through assignments to users or groups in specified AWS accounts.   [sources: aws_iam_user_guide#../../../singlesignon/latest/userguide/permissionsetsconcept.html]
A.f2: Use the supplied Identity Center assignment workflow to assign the approved user or group, account and permission set, then sign in to that account and test the intended access.   [sources: aws_iam_user_guide#../../../singlesignon/latest/userguide/assignusers.html]
A.f3: Configure a named SSO profile with aws configure sso and establish a session with aws sso login --profile NAME rather than storing long-lived IAM user keys.   [sources: aws_cli_user_guide#cli-configure-sso.html]
note: Use supplied assignments; do not create a new enterprise identity architecture.
PRACTICE ANCHOR (tool_simulation): Use the supplied Identity Center workflow to assign one approved permission set to a sandbox user in the specified account, sign in, and test the intended access. Configure a named SSO profile with aws configure sso and establish its session with aws sso login --profile NAME.  SUCCESS: The assignment matches the supplied user, account, and approved permission set. The user signs in to that account, and the supplied access test produces the expected result. The named SSO profile is configured and its session established without storing long-lived IAM user keys.
ASSESSMENT ANCHOR: verify_person_permission_set_assignment_and_intended_access facts=['f1', 'f2']
ASSESSMENT ANCHOR: establish_named_sso_profile_access_without_long_lived_user_keys facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authorize an event target with least-privilege execution permissions; Automate prohibited-configuration checks; Cloudformation drift; Cloudformation rollback; Configure GitHub Actions AWS role federation; Configure a budget notification; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Ec2 instance profile; Eks workload identity; Evaluate resource-based permissions for a requested operation; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute an established managed account-onboarding workflow; Extract structured AWS CLI inventory across paginated results; Hand over an actionable operational runbook; Operate an EKS Pod using supplied cluster-access setup; Operate an RDS managed database as the native backup-resource foundation; Protect recoverable S3 objects with versioning and lifecycle controls; Publish a container image to ECR after external Docker preparation; Publish a traceable immutable build artifact; Read and modify a standard CloudFormation S3 template; directly require 

## LESSON, in learner order

### s01 · explainer · Approved assignment, session and access
Learn — 
(definition) Permissions are made available through IAM Identity Center permission-set assignments to users or groups in specified AWS accounts. An operator needs approved access, not saved long-lived IAM user keys. ⟦A.f1 A:tb1 A:tb2⟧
(workflow) Use the supplied assignment workflow to assign the approved user or group, account and permission set. Then sign in to that account and test the intended access. Keep the assignment, signed-in permission-set context and test result together: sign-in alone is not the complete access check. ⟦A.f1 A.f2 A:tb3 A:tb4 A:tb5⟧
(example) For cedar-operator in cedar-operators, compare the assigned account and permission set with the approved context. The intended test is read sandbox evidence object. Keep its expected and observed results alongside the signed-in context. ⟦A.f1 A.f2 A:tb4⟧
(mechanism) Configure a named SSO profile with aws configure sso. Establish its session with aws sso login --profile NAME, replacing NAME with the profile name. Use this session workflow rather than storing long-lived IAM user keys. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[DIAGRAM: Approved access context and test] nodes=['Approved assignment {User: cedar-operator; Group: cedar-operators; Account: 111111111111; Permission set: CedarObjectRead}', 'Assigned context {Account: 111111111111; Permission set: CedarObjectRead}', 'Signed-in context {Account: 111111111111; Permission set: CedarObjectRead}', 'Intended access {Read sandbox evidence object; Expected: success; Observed: success}', 'Named SSO profile {aws configure sso; named profile cedar-sandbox configured; aws sso login --profile cedar-sandbox; session established; no long-lived IAM user keys}'] edges=[('approved', 'assigned', 'Match approval'), ('assigned', 'signed', 'Sign in'), ('signed', 'test', 'Test intended access'), ('signed', 'profile', 'Use named session')] alt: The approved user cedar-operator in cedar-operators has matching assigned and signed-in account 111111111111 and permission set CedarObjectRead. The intended object-read test succeeds as expected, and named profile cedar-sandbox has an established SSO session without long-lived IAM user keys.

### s02 · video · From assignment to signed-in context
[VIDEO From an account assignment to permission-set sign-in] bridge-before: Watch how the group, account, and permission sets connect, then how the user selects access. Use your supplied approved sandbox assignment, not the demonstration’s administrative choices. | bridge-after: The clip shows assignment and console sign-in, not approval checks or an intended-operation test. The text covers those requirements and the named SSO profile configuration and login commands.
  - bVjwu1WN42I 253-379s facts=['f1'] label: Assign account permissions to a group and sign in through the access portal | summary: The demonstration assigns a group and two existing permission sets to an AWS account. A user in that group receives access through the assignment. The user accepts an invitation, sets a password, signs in, and registers an authenticator app for MFA. The access portal then presents the assigned account and its permission-set choices. Selecting ViewOnlyAccess opens the AWS Management Console with that permission set identified in the interface. This demonstrates assignment and console sign-in, but does not test an intended operation or configure a named SSO CLI profile.

### s03 · check · Choose the named-session workflow
Check your understanding — 
QUESTION [choice, intro, grading=client] Which workflow establishes a named AWS CLI SSO session without storing long-lived IAM user keys?
  ✔ o1: Configure the named profile with aws configure sso, then use aws sso login --profile NAME for that profile.
      why: The named SSO profile is configured first, then its session is established using that profile.
  ✘ o2: Save long-lived IAM user keys under a profile name instead of using SSO login.
      why: A profile name does not change the credential method. The taught workflow uses SSO rather than storing long-lived IAM user keys.
  ✘ o3: Configure the named SSO profile and treat configuration alone as an established session.
      why: Configuration and session establishment are separate: aws sso login --profile NAME establishes the session.
  feedback✔: The named SSO profile is configured first, then its session is established using that profile.  feedback✘: A named profile must use the taught SSO configuration and session workflow rather than stored long-lived IAM user keys.  hints: ['Profile configuration and session establishment are separate steps.']  remediation→r01
  MEASURES: A:establish_named_sso_profile_access_without_long_lived_user_keys(f3)   anchors=['assessment:establish_named_sso_profile_access_without_long_lived_user_keys']
  taught-before-tested: A.f3←s01

### s04 · hands_on · Review human-access evidence
Evidence review — Read the supplied assignment, sign-in, test and named-profile excerpts in this step. Decide which records demonstrate the approved access checks and which are defective.
QUESTION [classify, stretch, grading=client] Read each alternative access-review excerpt. Decide whether it meets all supplied assignment, account sign-in, intended-access test and named-SSO requirements, or identify its single unmet requirement. Permission-set names denote supplied approvals, not inferred AWS definitions.
  '```text
case_id: access.complete
user: cedar-operator
operator_group: cedar-operators
approved_account: 111111111111
approved_permission_set: CedarObjectRead
assigned_account: 111111111111
assigned_permission_set: CedarObjectRead
signed_in_account: 111111111111
signed_in_permission_set: CedarObjectRead
intended_access_test: Read sandbox evidence object
expected_result: success
observed_result: success
profile_name: cedar-sandbox
profile_configuration: aws configure sso; named profile cedar-sandbox configured
session_evidence: aws sso login --profile cedar-sandbox; session established
credential_storage: no long-lived IAM user keys
```' -> All supplied requirements met
      feedback: Assignment and signed-in context match the approval, the intended access test matches its expected result, and named SSO configuration and session evidence show no stored long-lived IAM user keys.
  '```text
case_id: access.sign_in_only
user: cedar-operator
operator_group: cedar-operators
approved_account: 111111111111
approved_permission_set: CedarObjectRead
assigned_account: 111111111111
assigned_permission_set: CedarObjectRead
signed_in_account: 111111111111
signed_in_permission_set: CedarObjectRead
intended_access_test: Read sandbox evidence object
expected_result: success
observed_result: not tested
profile_name: cedar-sandbox
profile_configuration: aws configure sso; named profile cedar-sandbox configured
session_evidence: aws sso login --profile cedar-sandbox; session established
credential_storage: no long-lived IAM user keys
```' -> Intended access test not verified
      feedback: The intended access test is not tested. Successful sign-in does not establish its expected result.
  '```text
case_id: access.assignment_mismatch
user: cedar-operator
operator_group: cedar-operators
approved_account: 111111111111
approved_permission_set: CedarObjectRead
assigned_account: 111111111111
assigned_permission_set: CedarOtherPermission
signed_in_account: 111111111111
signed_in_permission_set: CedarOtherPermission
intended_access_test: Read sandbox evidence object
expected_result: success
observed_result: success
profile_name: cedar-sandbox
profile_configuration: aws configure sso; named profile cedar-sandbox configured
session_evidence: aws sso login --profile cedar-sandbox; session established
credential_storage: no long-lived IAM user keys
```' -> Approved assignment/context mismatch
      feedback: The assigned and signed-in permission set differs from the supplied approval. The access test and named SSO requirements are otherwise evidenced, but they do not make the unapproved context acceptable.
  '```text
user: cedar-operator
operator_group: cedar-operators
approved_account: 111111111111
approved_permission_set: CedarObjectRead
assigned_account: 111111111111
assigned_permission_set: CedarObjectRead
signed_in_account: 111111111111
signed_in_permission_set: CedarObjectRead
intended_access_test: Read sandbox evidence object
expected_result: success
observed_result: success
profile_name: cedar-sandbox
profile_configuration: named profile populated with stored IAM user keys
session_evidence: no SSO login session evidence
credential_storage: long-lived IAM user keys stored
```' -> Required SSO credential/session method not met
      feedback: Matching account, permission set and access-test results do not satisfy the separate requirement for named SSO configuration and a session without stored long-lived IAM user keys.
  feedback✔: Your judgement follows the supplied evidence and the taught checks.  feedback✘: Separate the individual evidence checks; success at one stage does not establish all required conditions.  hints: ['Keep assignment, sign-in and intended-operation results as separate checks.', 'Distinguish profile configuration from establishing its session.']  remediation→r02
  MEASURES: A:verify_person_permission_set_assignment_and_intended_access(f1,f2); A:establish_named_sso_profile_access_without_long_lived_user_keys(f3)   anchors=['practice', 'assessment:verify_person_permission_set_assignment_and_intended_access', 'assessment:establish_named_sso_profile_access_without_long_lived_user_keys']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

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

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: aws_devops.tile.028.s02: prose block without lineage.fact_ids

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
[DIAGRAM: Connection, tracked response and filtering boundary] nodes=['approved source range: 192.0.2.0/24', 'eni-cedar-workload {sg-cedar-workload; allow TCP 443 from 192.0.2.0/24}', 'tracked response {response succeeds}', 'unapproved source range: 198.51.100.0/24 {not admitted}', 'sg-cedar-source {Identifies source; no rule import}', 'Outside filtering {Amazon-provided DNS; instance metadata}'] edges=[('source', 'eni', 'TCP 443: connection succeeds'), ('eni', 'response', 'Allowed regardless of response-direction rules'), ('other', 'eni', 'No matching inbound allow'), ('group', 'eni', 'Alternative inbound rule: allow TCP 443 from sg-cedar-source; no rule import.')] alt: Connection, tracked response and filtering boundary

### s02 · explainer · Keep the filtering boundary clear
Learn — 
(example) Use the supplied TCP ingress rule and approved source on the workload’s associated security group. Remove unnecessary ingress and test both the required connection and its response. A tracked response is allowed regardless of response-direction rules; a new connection from an unapproved source is a different case. Do not widen ingress to make an unexplained test pass. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) A security-group ID used as an allowed source identifies that source; it does not import the referenced group’s rules into the destination group. Security groups contain allow rules, not explicit deny rules. ⟦A.f1 A.m1 A:tb4 A:tb5 A:tb6⟧
(misconception) Security groups do not filter traffic to Amazon-provided DNS or EC2 instance metadata services. Those cases are outside the filtering boundary, so their results do not demonstrate that ordinary ingress is allowed. ⟦A:tb4 A:tb5 A:tb6⟧
[TABLE ds.connection_tests cols=['test_id', 'network_interface', 'destination_group', 'traffic_case', 'protocol', 'port', 'source', 'inbound_rule', 'response_direction_rule', 'observed_result', 'interpretation'] ] caption: Compare supplied connection cases, not DNS or metadata as ingress evidence.

### s03 · check · Distinguish response from new ingress
Check your understanding — 
QUESTION [choice, intro, grading=client] A security group allowed a new connection. For the response to that tracked connection, there is no allow rule in the response direction. What follows from security-group statefulness?
  ✔ o1: The response is allowed regardless of response-direction rules.
      why: Statefulness allows response traffic for the allowed connection.
  ✘ o2: The response is blocked until a separate response-direction allow is added.
      why: Statefulness means this response does not require a separate response-direction allow rule.
  ✘ o3: Every later new connection from any source is also allowed.
      why: A tracked response is not a new connection from an arbitrary source; new connections still need applicable allows.
  feedback✔: Statefulness allows response traffic for the allowed connection.  feedback✘: Judge the response as response traffic for the already allowed connection, not as an arbitrary new connection.  hints: ['Distinguish a tracked response from a new connection.']  remediation→r01
  MEASURES: A:determine_stateful_response_traffic_behavior(f2)   anchors=['assessment:determine_stateful_response_traffic_behavior']
  taught-before-tested: A.f2←s01

### s04 · hands_on · Review connection-rule evidence
Evidence review — Read the supplied connection and rule excerpts in this step. Decide which interpretations correctly enforce approved ingress and interpret source-group references.
QUESTION [classify, stretch, grading=client] Read the ingress-review excerpts and decide whether the associated group meets the stated approved-ingress baseline and required connection checks. For the separate source-reference explanations, decide whether the interpretation is correct. A new unapproved-source connection is not a tracked response.
  '```text
Associated network interface: eni-cedar-workload
Security group: sg-cedar-workload
Approved ingress: allow TCP 443 from 192.0.2.0/24
Complete inbound rule list:
- allow TCP 443 from 192.0.2.0/24
No other inbound rules.
Response-direction allow rule: none
Test: approved source range: 192.0.2.0/24 -> connection succeeds
Tracked response: response succeeds
New connection: unapproved source range: 198.51.100.0/24 -> not admitted
```' -> Ingress baseline and connection checks met
      feedback: The only ingress rule admits the approved TCP connection, its tracked response succeeds without a separate response-direction rule, and the unapproved new connection is not admitted.
  '```text
Associated network interface: eni-cedar-workload
Security group: sg-cedar-workload
Approved ingress: allow TCP 443 from 192.0.2.0/24
Complete inbound rule list:
- allow TCP 443 from 192.0.2.0/24
- allow TCP 443 from 198.51.100.0/24
Response-direction allow rule: none
Test: approved source range: 192.0.2.0/24 -> connection succeeds
Tracked response: response succeeds
New connection: unapproved source range: 198.51.100.0/24 -> connection succeeds
```' -> Ingress baseline or checks violated
      feedback: The extra rule admits a new connection from an unapproved source. That unnecessary ingress violates the supplied baseline; statefulness does not justify it.
  '```text
network_interface: eni-cedar-workload
destination_group: sg-cedar-workload
traffic_case: new connection
protocol: TCP
port: 443
source: sg-cedar-source
inbound_rule: allow TCP 443 from sg-cedar-source
response_direction_rule: none
observed_result: connection succeeds
Reviewer explanation: The source-group ID identifies the allowed source; the destination group does not acquire the source group rules.
```' -> Source-reference explanation correct
      feedback: A source-group reference identifies an allowed source, not imported rules.
  '```text
network_interface: eni-cedar-workload
destination_group: sg-cedar-workload
traffic_case: new connection
protocol: TCP
port: 443
source: sg-cedar-source
inbound_rule: allow TCP 443 from sg-cedar-source
response_direction_rule: none
observed_result: connection succeeds
Reviewer explanation: The source-group ID imports all rules of that group into the destination group.
```' -> Source-reference explanation incorrect
      feedback: A security-group source reference does not import the referenced group rules into the destination group.
  feedback✔: Your judgement follows the supplied evidence and the taught checks.  feedback✘: Separate the individual evidence checks; success at one stage does not establish all required conditions.  hints: ['Distinguish a tracked response from a new connection.', 'Read the complete inbound rule list and the source-reference explanation separately.']  remediation→r02
  MEASURES: A:determine_allow_only_rules_at_associated_network_interfaces(f1); A:enforce_approved_ingress_and_verify_required_connections(f3); A:interpret_source_group_references_without_importing_rules(m1)   anchors=['practice', 'assessment:determine_allow_only_rules_at_associated_network_interfaces', 'assessment:enforce_approved_ingress_and_verify_required_connections', 'assessment:interpret_source_group_references_without_importing_rules']
  taught-before-tested: A.f1←s01; A.f3←s01; A.m1←s01

### s05 · recap · Keep the evidence distinct
Takeaways — 
(takeaway) Security groups use allow rules at associated network interfaces. Tracked responses are statefully allowed. Use required protocol, port range and approved source, remove unnecessary ingress, and test connections and responses. Source-group references do not import rules; DNS and metadata traffic are outside security-group filtering. ⟦A.f1 A.f2 A.f3 A.m1 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
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

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

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
QUESTION [choice, intro, grading=client] A matching Terraform declaration is supplied. Which sequence distinguishes provider installation, intended-change inspection, creation and verification?
  ✔ o1: terraform init; terraform plan and inspect the intended instance; approved terraform apply; compare resulting instance settings with the specification.
      why: Initialization installs providers, planning inspects changes, approved apply creates the instance, and the resulting settings still need verification.
  ✘ o2: terraform init, then regard provider installation as proof that the instance was created.
      why: Initialization installs providers; it is not instance creation or verification.
  ✘ o3: terraform plan, then regard the proposed instance as a verified created instance without apply.
      why: A plan describes intended changes; the approved apply creates the instance and resulting settings must be verified.
  feedback✔: Initialization installs providers, planning inspects changes, approved apply creates the instance, and the resulting settings still need verification.  feedback✘: Separate provider installation, intended changes, actual creation and resulting-setting verification.  hints: ['Separate provider installation, proposed changes, instance creation and verification.']  remediation→r01
  MEASURES: A:distinguish_initialization_planning_creation_and_verification(f3)   anchors=['assessment:distinguish_initialization_planning_creation_and_verification']
  taught-before-tested: A.f3←s01

### s04 · hands_on · Review Terraform provisioning evidence
Evidence review — Read the supplied declaration and execution excerpts in this step. Decide which records correctly show the approved pin, supplied instance settings and verified provisioning.
QUESTION [classify, stretch, grading=client] Read each alternative Terraform declaration and supplied execution/result excerpt. Compare the provider requirement and instance settings with the included specification; decide whether all declaration, initialization, one-instance plan, approved-apply and resulting-setting checks are met, or identify the single defect.
  'Supplied specification:
```text
provider_source: hashicorp/aws
provider_version: 6.0.0
resource_type: aws_instance
resource_label: cedar_workload
ami: ami-00000000000000001
instance_type: t3.micro
subnet_id: subnet-00000000000000001
```
Observed declaration:
```hcl
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "= 6.0.0"
    }
  }
}
resource "aws_instance" "cedar_workload" {
  ami = "ami-00000000000000001"
  instance_type = "t3.micro"
  subnet_id = "subnet-00000000000000001"
}
```
Supplied execution log:
```text
terraform init: Provider installation succeeded
terraform plan: One intended EC2 instance proposed
terraform apply: Instance creation completed; resulting settings compared
```
Inspected plan: one intended instance
```text
provider_source: hashicorp/aws
provider_version: 6.0.0
resource_type: aws_instance
resource_label: cedar_workload
ami: ami-00000000000000001
instance_type: t3.micro
subnet_id: subnet-00000000000000001
```
Apply approval: Supplied apply approval recorded
Resulting instance settings:
```text
provider_source: hashicorp/aws
provider_version: 6.0.0
resource_type: aws_instance
resource_label: cedar_workload
ami: ami-00000000000000001
instance_type: t3.micro
subnet_id: subnet-00000000000000001
```' -> All supplied checks met
      feedback: The exact provider pin and declared instance values match the specification, initialization succeeds, the plan contains one intended instance, and approved apply plus resulting settings are evidenced.
  'Supplied specification:
```text
provider_source: hashicorp/aws
provider_version: 6.0.0
resource_type: aws_instance
resource_label: cedar_workload
ami: ami-00000000000000001
instance_type: t3.micro
subnet_id: subnet-00000000000000001
```
Observed declaration:
```hcl
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = ">= 6.0.0"
    }
  }
}
resource "aws_instance" "cedar_workload" {
  ami = "ami-00000000000000001"
  instance_type = "t3.micro"
  subnet_id = "subnet-00000000000000001"
}
```
Supplied execution log:
```text
terraform init: Provider installation succeeded
terraform plan: One intended EC2 instance proposed
terraform apply: Instance creation completed; resulting settings compared
```
Inspected plan: one intended instance
```text
provider_source: hashicorp/aws
provider_version: 6.0.0
resource_type: aws_instance
resource_label: cedar_workload
ami: ami-00000000000000001
instance_type: t3.micro
subnet_id: subnet-00000000000000001
```
Apply approval: Supplied apply approval recorded
Resulting instance settings:
```text
provider_source: hashicorp/aws
provider_version: 6.0.0
resource_type: aws_instance
resource_label: cedar_workload
ami: ami-00000000000000001
instance_type: t3.micro
subnet_id: subnet-00000000000000001
```' -> Provider requirement is not an exact approved pin
      feedback: A greater-than-or-equal provider constraint is not an exact approved version pin, even if the supplied execution evidence used that approved version.
  'Supplied specification:
```text
provider_source: hashicorp/aws
provider_version: 6.0.0
resource_type: aws_instance
resource_label: cedar_workload
ami: ami-00000000000000001
instance_type: t3.micro
subnet_id: subnet-00000000000000001
```
Observed declaration:
```hcl
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "= 6.0.0"
    }
  }
}
resource "aws_instance" "cedar_workload" {
  ami = "ami-00000000000000001"
  instance_type = "t3.micro"
}
```
Supplied execution log:
```text
terraform init: Provider installation succeeded
terraform plan: One intended EC2 instance proposed
terraform apply: Instance creation completed; resulting settings compared
```
Inspected plan: one intended instance
```text
provider_source: hashicorp/aws
provider_version: 6.0.0
resource_type: aws_instance
resource_label: cedar_workload
ami: ami-00000000000000001
instance_type: t3.micro
subnet_id: subnet-00000000000000001
```
Apply approval: Supplied apply approval recorded
Resulting instance settings:
```text
provider_source: hashicorp/aws
provider_version: 6.0.0
resource_type: aws_instance
resource_label: cedar_workload
ami: ami-00000000000000001
instance_type: t3.micro
subnet_id: subnet-00000000000000001
```' -> Declared instance values incomplete
      feedback: The declaration omits the supplied subnet_id. Matching plan and result evidence cannot make the incomplete declaration satisfy the requirement to declare all three supplied settings.
  'Supplied specification:
```text
provider_source: hashicorp/aws
provider_version: 6.0.0
resource_type: aws_instance
resource_label: cedar_workload
ami: ami-00000000000000001
instance_type: t3.micro
subnet_id: subnet-00000000000000001
```
Observed declaration:
```hcl
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "= 6.0.0"
    }
  }
}
resource "aws_instance" "cedar_workload" {
  ami = "ami-00000000000000001"
  instance_type = "t3.micro"
  subnet_id = "subnet-00000000000000001"
}
```
Supplied execution log:
```text
terraform init: Provider installation succeeded
terraform plan: One intended EC2 instance proposed
```
Inspected plan: one intended instance
```text
provider_source: hashicorp/aws
provider_version: 6.0.0
resource_type: aws_instance
resource_label: cedar_workload
ami: ami-00000000000000001
instance_type: t3.micro
subnet_id: subnet-00000000000000001
```
No apply or resulting-instance evidence supplied.' -> Creation/result verification evidence missing
      feedback: A matching declaration and plan do not demonstrate creation or resulting-instance verification; the approved apply and resulting settings need evidence.
  feedback✔: Your judgement follows the supplied evidence and the taught checks.  feedback✘: Separate the individual evidence checks; success at one stage does not establish all required conditions.  hints: ['Compare each declared setting and the provider requirement with the specification.', 'Keep proposed changes distinct from created-instance evidence.']  remediation→r02
  MEASURES: A:verify_exact_approved_provider_pin(f1); A:verify_declared_ec2_settings_against_supplied_values(f2); A:verify_planned_ec2_instance_matches_specification(f2,f3)   anchors=['practice', 'assessment:verify_exact_approved_provider_pin', 'assessment:verify_declared_ec2_settings_against_supplied_values', 'assessment:verify_planned_ec2_instance_matches_specification']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f2←s01; A.f3←s01

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

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

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
QUESTION [choice, intro, grading=client] For an ordinary supplied cross-account S3 request with no applicable explicit deny, the resource side allows the request but identity-side permission is absent. Which judgement follows from the taught general rule?
  ✔ o1: Permission is not demonstrated: cross-account access generally requires permission on both sides.
      why: The ordinary supplied case lacks identity-side permission; the general cross-account rule requires permission on both sides.
  ✘ o2: The resource allow alone is sufficient because same-account contributed-allow reasoning always applies across accounts.
      why: Same-account contributed allows do not replace the general cross-account requirement for permission on both sides.
  ✘ o3: The identity side alone would be sufficient even if the resource side did not permit the request.
      why: The general cross-account rule requires permission on both sides, not only identity-side permission.
  feedback✔: The ordinary supplied case lacks identity-side permission; the general cross-account rule requires permission on both sides.  feedback✘: Apply the general cross-account requirement rather than treating this as a same-account contributed-allow case.  hints: ['Check whether both the identity side and resource side supply permission.']  remediation→r01
  MEASURES: A:determine_general_cross_account_permission_requirements(f3)   anchors=['assessment:determine_general_cross_account_permission_requirements']
  taught-before-tested: A.f3←s01

### s04 · hands_on · Review policy and request fields
Evidence review — Read the supplied policy and request evidence. Select the matching fields and permission evidence, keeping bucket scope distinct from object scope.
QUESTION [table_select, stretch, grading=client] 
  intro shown to learner: Read the supplied bucket-policy statements and request evidence. Select one request row per judgement; compare Principal, Action, Resource and Condition before considering identity-side permission and explicit deny. These are ordinary supplied permission cases.
Bucket policy attached to the sandbox evidence bucket:
```text
statement_id: same_account_read
Effect: Allow
Principal: arn:aws:iam::111111111111:role/CedarReader
Action: s3:GetObject
Resource: arn:aws:s3:::cedar-sandbox-evidence/*
Condition: aws:SecureTransport = true

statement_id: cross_account_read
Effect: Allow
Principal: arn:aws:iam::222222222222:role/CedarReader
Action: s3:GetObject
Resource: arn:aws:s3:::cedar-sandbox-evidence/*
Condition: aws:SecureTransport = true
```
  task t1 (row): Which same-account request is permitted by a matching resource allow even though identity-side allow evidence is absent?  KEY: row={'request_id': 'request.same'} column=None expect=None dataset-says={'request_id': 'request.same', 'Principal': 'arn:aws:iam::111111111111:role/CedarReader', 'Action': 's3:GetObject', 'Resource': 'arn:aws:s3:::cedar-sandbox-evidence/evidence.txt', 'Condition': 'aws:SecureTransport = true', 'account_relationship': 'same-account', 'identity_allow': 'absent', 'resource_allow': 'matching', 'explicit_deny': 'none applicable', 'permission_outcome': 'permitted', 'evidence_note': 'Matching resource allow contributes permission'}
      feedback: {'correct': 'A matching resource allow contributes permission in this same-account case with no applicable explicit deny.', 'incorrect': 'Recheck the four policy fields, the account relationship, contributed allows and applicable explicit deny. A matching resource allow contributes permission in this same-account case with no applicable explicit deny.'}
  task t2 (row): Which request has matching identity and resource allows but is not permitted because an applicable explicit deny overrides them?  KEY: row={'request_id': 'request.denied'} column=None expect=None dataset-says={'request_id': 'request.denied', 'Principal': 'arn:aws:iam::111111111111:role/CedarReader', 'Action': 's3:GetObject', 'Resource': 'arn:aws:s3:::cedar-sandbox-evidence/evidence.txt', 'Condition': 'aws:SecureTransport = true', 'account_relationship': 'same-account', 'identity_allow': 'matching', 'resource_allow': 'matching', 'explicit_deny': 'applicable supplied explicit deny', 'permission_outcome': 'not permitted', 'evidence_note': 'Applicable explicit deny overrides contributed allows'}
      feedback: {'correct': 'An applicable explicit deny overrides both contributed allows.', 'incorrect': 'Recheck the four policy fields, the account relationship, contributed allows and applicable explicit deny. An applicable explicit deny overrides both contributed allows.'}
  task t3 (row): Which ordinary cross-account request is permitted because both identity and resource permission are present and no applicable explicit deny is supplied?  KEY: row={'request_id': 'request.cross_both'} column=None expect=None dataset-says={'request_id': 'request.cross_both', 'Principal': 'arn:aws:iam::222222222222:role/CedarReader', 'Action': 's3:GetObject', 'Resource': 'arn:aws:s3:::cedar-sandbox-evidence/evidence.txt', 'Condition': 'aws:SecureTransport = true', 'account_relationship': 'cross-account', 'identity_allow': 'matching', 'resource_allow': 'matching', 'explicit_deny': 'none applicable', 'permission_outcome': 'permitted', 'evidence_note': 'Supplied ordinary cross-account case: permission on both sides'}
      feedback: {'correct': 'Both sides supply permission and no applicable explicit deny overrides it.', 'incorrect': 'Recheck the four policy fields, the account relationship, contributed allows and applicable explicit deny. Both sides supply permission and no applicable explicit deny overrides it.'}
  task t4 (row): Which ordinary cross-account request matches all four policy fields but is not permitted because identity-side permission is absent?  KEY: row={'request_id': 'request.cross_missing'} column=None expect=None dataset-says={'request_id': 'request.cross_missing', 'Principal': 'arn:aws:iam::222222222222:role/CedarReader', 'Action': 's3:GetObject', 'Resource': 'arn:aws:s3:::cedar-sandbox-evidence/evidence.txt', 'Condition': 'aws:SecureTransport = true', 'account_relationship': 'cross-account', 'identity_allow': 'absent', 'resource_allow': 'matching', 'explicit_deny': 'none applicable', 'permission_outcome': 'not permitted', 'evidence_note': 'Supplied ordinary cross-account case lacks identity-side permission'}
      feedback: {'correct': 'A field-matching resource allow does not replace absent identity-side permission in this ordinary cross-account case.', 'incorrect': 'Recheck the four policy fields, the account relationship, contributed allows and applicable explicit deny. A field-matching resource allow does not replace absent identity-side permission in this ordinary cross-account case.'}
  task t5 (row): Which request is not permitted because the caller fails to match Principal, although identity-side allow evidence is present?  KEY: row={'request_id': 'request.unapproved'} column=None expect=None dataset-says={'request_id': 'request.unapproved', 'Principal': 'arn:aws:iam::222222222222:role/CedarUnapproved', 'Action': 's3:GetObject', 'Resource': 'arn:aws:s3:::cedar-sandbox-evidence/evidence.txt', 'Condition': 'aws:SecureTransport = true', 'account_relationship': 'cross-account', 'identity_allow': 'matching', 'resource_allow': 'no matching principal', 'explicit_deny': 'none applicable', 'permission_outcome': 'not permitted', 'evidence_note': 'Resource-side principal does not match'}
      feedback: {'correct': 'The unapproved caller does not match a resource-side Principal; the cross-account request lacks permission on that side.', 'incorrect': 'Recheck the four policy fields, the account relationship, contributed allows and applicable explicit deny. The unapproved caller does not match a resource-side Principal; the cross-account request lacks permission on that side.'}
  task t6 (row): Which request is not permitted because its bucket ARN does not match the policy object-resource scope, with no identity allow to contribute permission?  KEY: row={'request_id': 'request.bucket_scope'} column=None expect=None dataset-says={'request_id': 'request.bucket_scope', 'Principal': 'arn:aws:iam::111111111111:role/CedarReader', 'Action': 's3:GetObject', 'Resource': 'arn:aws:s3:::cedar-sandbox-evidence', 'Condition': 'aws:SecureTransport = true', 'account_relationship': 'same-account', 'identity_allow': 'absent', 'resource_allow': 'no matching object scope', 'explicit_deny': 'none applicable', 'permission_outcome': 'not permitted', 'evidence_note': 'Bucket ARN differs from object ARN; does not match the supplied object resource scope'}
      feedback: {'correct': 'The bucket ARN and object ARN identify different scopes; this request does not match the object-resource scope.', 'incorrect': 'Recheck the four policy fields, the account relationship, contributed allows and applicable explicit deny. The bucket ARN and object ARN identify different scopes; this request does not match the object-resource scope.'}
  task t7 (row): Which request has a matching caller, action and object scope but is not permitted because Condition does not match and identity-side allow is absent?  KEY: row={'request_id': 'request.condition'} column=None expect=None dataset-says={'request_id': 'request.condition', 'Principal': 'arn:aws:iam::111111111111:role/CedarReader', 'Action': 's3:GetObject', 'Resource': 'arn:aws:s3:::cedar-sandbox-evidence/evidence.txt', 'Condition': 'aws:SecureTransport = false', 'account_relationship': 'same-account', 'identity_allow': 'absent', 'resource_allow': 'no matching condition', 'explicit_deny': 'none applicable', 'permission_outcome': 'not permitted', 'evidence_note': 'Supplied condition does not match'}
      feedback: {'correct': 'The supplied condition value fails to match the policy condition and no identity allow contributes permission.', 'incorrect': 'Recheck the four policy fields, the account relationship, contributed allows and applicable explicit deny. The supplied condition value fails to match the policy condition and no identity allow contributes permission.'}
  task t8 (row): Which request has a matching caller, object scope and condition but is not permitted because Action does not match and identity-side allow is absent?  KEY: row={'request_id': 'request.action'} column=None expect=None dataset-says={'request_id': 'request.action', 'Principal': 'arn:aws:iam::111111111111:role/CedarReader', 'Action': 's3:DeleteObject', 'Resource': 'arn:aws:s3:::cedar-sandbox-evidence/evidence.txt', 'Condition': 'aws:SecureTransport = true', 'account_relationship': 'same-account', 'identity_allow': 'absent', 'resource_allow': 'no matching action', 'explicit_deny': 'none applicable', 'permission_outcome': 'not permitted', 'evidence_note': 'Supplied read action does not match the requested operation'}
      feedback: {'correct': 'The requested operation differs from the policy Action; no matching resource or identity allow supplies permission.', 'incorrect': 'Recheck the four policy fields, the account relationship, contributed allows and applicable explicit deny. The requested operation differs from the policy Action; no matching resource or identity allow supplies permission.'}
  feedback✔: Your judgement follows the supplied evidence and the taught checks.  feedback✘: Separate the individual evidence checks; success at one stage does not establish all required conditions.  hints: ['Match the four request fields before considering contributed permission.', 'Keep account relationship and explicit-deny evidence in the decision.']  remediation→r02
  MEASURES: A:match_resource_policy_statements_to_supplied_requests(f1,f2); A:distinguish_bucket_and_object_arn_scopes(f2); A:evaluate_contributed_allows_and_explicit_deny_precedence(f3); A:determine_general_cross_account_permission_requirements(f3)   anchors=['practice', 'assessment:match_resource_policy_statements_to_supplied_requests', 'assessment:distinguish_bucket_and_object_arn_scopes', 'assessment:evaluate_contributed_allows_and_explicit_deny_precedence', 'assessment:determine_general_cross_account_permission_requirements']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f2←s01; A.f3←s01; A.f3←s01

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

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

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
QUESTION [choice, intro, grading=client] An Account Factory account was created and its enrollment and organizational-unit placement match the approved inputs. One supplied baseline checkpoint has no supporting applied-control result. Which completion judgement is supported?
  ✔ o1: Record that checkpoint as unverified; account creation alone does not demonstrate governance completion.
      why: The missing checkpoint evidence remains unverified even though creation, enrollment and placement have evidence.
  ✘ o2: Mark governance complete solely because account creation succeeded.
      why: Creating an account does not substitute for checking enrollment, placement and supplied baseline evidence.
  ✘ o3: Treat the missing checkpoint as verified because enrollment and placement match.
      why: Enrollment and placement do not supply the missing applied-control evidence for that checkpoint.
  feedback✔: The missing checkpoint evidence remains unverified even though creation, enrollment and placement have evidence.  feedback✘: Creation, enrollment and placement do not provide a missing applied-control checkpoint result.  hints: ['Matching enrollment and placement do not supply missing baseline-checkpoint evidence.']  remediation→r01
  MEASURES: A:distinguish_account_creation_from_verified_governance_completion(f2,f3)   anchors=['assessment:distinguish_account_creation_from_verified_governance_completion']
  taught-before-tested: A.f2←s01; A.f3←s01

### s03 · hands_on · Review managed-account onboarding evidence
Evidence review — Read the supplied onboarding excerpts in this step. Decide which records demonstrate enrollment, placement and baseline verification, and which leave governance unverified.
QUESTION [classify, stretch, grading=client] Read each checkpoint-review excerpt from two alternative onboarding cases for the same account. Compare approved and observed inputs, enrollment and OU placement, then judge each baseline checkpoint against its applied-control evidence. Decide whether the checkpoint is verified or remains unverified; all checkpoints need supporting evidence before governance completion is demonstrated.
  '```text
case_id: onboard.complete
account_name: cedar-sandbox
account_id: 111111111111
approved_inputs: account cedar-sandbox; OU CedarSandbox
observed_inputs: account cedar-sandbox; OU CedarSandbox
creation_result: created
expected_enrollment: enrolled
observed_enrollment: enrolled
expected_organizational_unit: CedarSandbox
observed_organizational_unit: CedarSandbox
checkpoint_id: baseline.a
supplied_baseline_checkpoint: Compare supplied checkpoint A with its applied-control result
applied_control_evidence: Supplied checkpoint A result matches
```' -> Context matches and checkpoint verified
      feedback: Approved inputs, enrollment and OU placement match. The supplied checkpoint has matching applied-control evidence.
  '```text
case_id: onboard.complete
account_name: cedar-sandbox
account_id: 111111111111
approved_inputs: account cedar-sandbox; OU CedarSandbox
observed_inputs: account cedar-sandbox; OU CedarSandbox
creation_result: created
expected_enrollment: enrolled
observed_enrollment: enrolled
expected_organizational_unit: CedarSandbox
observed_organizational_unit: CedarSandbox
checkpoint_id: baseline.b
supplied_baseline_checkpoint: Compare supplied checkpoint B with its applied-control result
applied_control_evidence: Supplied checkpoint B result matches
```' -> Context matches and checkpoint verified
      feedback: Approved inputs, enrollment and OU placement match. The supplied checkpoint has matching applied-control evidence.
  '```text
case_id: onboard.incomplete
account_name: cedar-sandbox
account_id: 111111111111
approved_inputs: account cedar-sandbox; OU CedarSandbox
observed_inputs: account cedar-sandbox; OU CedarSandbox
creation_result: created
expected_enrollment: enrolled
observed_enrollment: enrolled
expected_organizational_unit: CedarSandbox
observed_organizational_unit: CedarSandbox
checkpoint_id: baseline.a
supplied_baseline_checkpoint: Compare supplied checkpoint A with its applied-control result
applied_control_evidence: Supplied checkpoint A result matches
```' -> Context matches and checkpoint verified
      feedback: Approved inputs, enrollment and OU placement match. The supplied checkpoint has matching applied-control evidence.
  '```text
case_id: onboard.incomplete
account_name: cedar-sandbox
account_id: 111111111111
approved_inputs: account cedar-sandbox; OU CedarSandbox
observed_inputs: account cedar-sandbox; OU CedarSandbox
creation_result: created
expected_enrollment: enrolled
observed_enrollment: enrolled
expected_organizational_unit: CedarSandbox
observed_organizational_unit: CedarSandbox
checkpoint_id: baseline.b
supplied_baseline_checkpoint: Compare supplied checkpoint B with its applied-control result
applied_control_evidence: no supplied evidence
```' -> Checkpoint remains unverified
      feedback: The account exists and enrollment and placement match, but this checkpoint has no supporting applied-control result. It remains unverified; creation does not establish governance completion.
  feedback✔: Your judgement follows the supplied evidence and the taught checks.  feedback✘: Separate the individual evidence checks; success at one stage does not establish all required conditions.  hints: ['Compare the approved context with the observed context.', 'Check each baseline result separately from the creation result.']  remediation→r02
  MEASURES: A:verify_account_factory_enrollment_and_organizational_unit_placement(f1,f2); A:verify_supplied_baseline_checkpoints_against_applied_controls(f3); A:distinguish_account_creation_from_verified_governance_completion(f2,f3)   anchors=['practice', 'assessment:verify_account_factory_enrollment_and_organizational_unit_placement', 'assessment:verify_supplied_baseline_checkpoints_against_applied_controls', 'assessment:distinguish_account_creation_from_verified_governance_completion']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f2←s01; A.f3←s01

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