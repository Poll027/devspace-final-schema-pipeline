# EVALUATOR PACKET — Operator profiles (aws_devops.tile.000)
Tile summary: Select the named profile explicitly. Check caller ARN and account separately from effective configuration and its origin. A command’s Region option overrides the configured Region.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws.operator_profiles — Operator profiles

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws.operator_profiles)   objective: Select an operator AWS CLI profile
A.f1: A named AWS CLI profile groups credential and configuration settings; select it with --profile NAME.   [sources: aws_cli_user_guide#cli-configure-files.html#cli-configure-files-using-profiles]
A.f2: Run aws sts get-caller-identity --profile NAME to inspect the caller ARN and account ID.   [sources: aws_cli_user_guide#cli-configure-files.html, aws_cli_user_guide#../../../STS/latest/APIReference/API_GetCallerIdentity.html]
A.f3: Run aws configure list --profile NAME to inspect the effective configuration and where its values came from; --region REGION overrides the configured Region for a command.   [sources: aws_cli_user_guide#cli-configure-files.html]
note: Keep credential creation out of scope; use supplied approved operator credentials and require the external secrets-handling preparation.
PRACTICE ANCHOR (tool_simulation): Select the supplied approved lab-operator context and confirm its caller identity, account and effective Region before proceeding with a supplied sandbox command.  SUCCESS: Use aws sts get-caller-identity --profile lab-operator and compare the returned ARN and account ID with the supplied expected context. Use aws configure list --profile lab-operator to identify the effective Region and its source. Keep --profile lab-operator on the supplied sandbox command and, when its approved target Region differs from the configured Region, select that target with --region REGION. Complete these checks before proceeding, without creating or changing credentials.
ASSESSMENT ANCHOR: select_explicit_named_profile facts=['f1']
ASSESSMENT ANCHOR: verify_caller_arn_and_account_id facts=['f2']
ASSESSMENT ANCHOR: verify_effective_region_and_configuration_origin facts=['f3']
ASSESSMENT ANCHOR: identify_command_region_override facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Allocate VPC and subnet CIDRs after external IP-addressing/CIDR preparation; Attribute an AWS change using CloudTrail evidence; Attribute workload spend using resource tags; Centralize structured application logs in CloudWatch Logs; Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation; Choose rolling, blue/green or canary delivery for stated availability and rollback requirements; Cloudformation change sets; Collect host telemetry with the CloudWatch agent; Compare ECS and managed EKS operational ownership; Configure role trust; directly require native IAM identity-policy evaluation; Configure subnet internet routing, teaching route-table association and CIDR destination routes; assume only external CIDR/IP addressing; Define recovery time and recovery point objectives; Distinguish AWS-managed and customer operational responsibilities; Distinguish capacity requirements from availability requirements; Establish service ownership and escalation; Evaluate an IAM identity policy for a requested operation after external access-control preparation; Execute a GitHub Actions workflow with an appropriate runner; Input targe

## LESSON, in learner order

### s01 · explainer · Check the operating model
Learn — 
(intro) Make the sandbox context explicit before changing resources. A profile name starts the identity check; it does not replace it. ⟦A:tb1⟧
(definition) A named AWS CLI profile groups credential and configuration settings; select it with --profile NAME. ⟦A.f1 A:tb2⟧
(mechanism) Run aws sts get-caller-identity --profile NAME to inspect the caller ARN and account ID. ⟦A.f2 A:tb3⟧
(mechanism) Run aws configure list --profile NAME to inspect the effective configuration and where its values came from; --region REGION overrides the configured Region for a command. ⟦A.f3 A:tb3⟧
[DIAGRAM: Illustrative operator-context checks] nodes=['aws sts get-caller-identity --profile lab-operator {Account: [REDACTED_ACCOUNT]; Arn: arn:aws:iam::[REDACTED_ACCOUNT]:user/[REDACTED_OPERATOR]}', 'aws configure list --profile lab-operator {Region Value: us-west-2; Type: config-file; Location: ~/.aws/config}', 'Command Region selection {Keep the explicit named profile; An explicit --region REGION overrides the configured Region for this command}'] edges=[] alt: Illustrative operator-context checks. aws sts get-caller-identity --profile lab-operator: Account: [REDACTED_ACCOUNT], Arn: arn:aws:iam::[REDACTED_ACCOUNT]:user/[REDACTED_OPERATOR]; aws configure list --profile lab-operator: Region Value: us-west-2, Type: config-file, Location: ~/.aws/config; Command Region selection: Keep the explicit named profile, An explicit --region REGION overrides the configured Region for this command

### s02 · explainer · Read the sandbox case
Learn — 
(example) Select lab-operator explicitly with --profile. The illustrative caller check shows Account: [REDACTED_ACCOUNT] and Arn: arn:aws:iam::[REDACTED_ACCOUNT]:user/[REDACTED_OPERATOR]. Compare both with the supplied operator context. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(example) The illustrative configure list Region row shows us-west-2, Type config-file, Location ~/.aws/config. That evidence answers configuration and origin, not caller identity. A command's explicit --region option overrides this configured Region; keep the same explicit profile. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) A profile label is not caller evidence, and caller evidence is not a Region check. ⟦A.f2 A.f3 A:tb5⟧

### s03 · check · Choose the supported conclusion
Check — Read the supplied excerpts in this step and decide which conclusions are correct, defective or unsafe.

### s04 · hands_on · Review the supplied evidence
Review — Read the supplied excerpts in this step and decide which conclusions are correct, defective or unsafe.

### s05 · recap · Keep the distinctions
Recap — 
(takeaway) Select the named profile explicitly. Check caller ARN and account separately from effective configuration and its origin. A command’s Region option overrides the configured Region. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Allocate VPC and subnet CIDRs after external IP-addressing/CIDR preparation: Continue to aws_devops.tile.001.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the two kinds of evidence
(definition) A named AWS CLI profile groups credential and configuration settings; select it with --profile NAME. ⟦A.f1 A:tb2 A:tb4⟧
(misconception) A profile label is not caller evidence, and caller evidence is not a Region check. ⟦A.f2 A.f3 A:tb5⟧
(example) Return to the same lab-operator example: compare the caller check with the configuration check. ⟦A.f1 A.f2 A.f3 A:tb4⟧
### r02 · Separate the two kinds of evidence
(definition) Run aws sts get-caller-identity --profile NAME to inspect the caller ARN and account ID. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Run aws configure list --profile NAME to inspect the effective configuration and where its values came from; --region REGION overrides the configured Region for a command. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) A profile label is not caller evidence, and caller evidence is not a Region check. ⟦A.f2 A.f3 A:tb5⟧
(example) Return to the same lab-operator example: compare the caller check with the configuration check. ⟦A.f1 A.f2 A.f3 A:tb4⟧

=========

# EVALUATOR PACKET — Allocate VPC and subnet CIDRs after external IP-addressing/CIDR preparation (aws_devops.tile.001)
Tile summary: Require containment, nonoverlap, allowed subnet size and capacity after reservations. Use separate subnets for separate Availability Zones.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.allocate_vpc_and_subnet_cidrs — Allocate VPC and subnet CIDRs after external IP-addressing/CIDR preparation

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.allocate_vpc_and_subnet_cidrs)   objective: Allocate nonoverlapping VPC and subnet CIDRs
A.f1: An IPv4 subnet CIDR must be within its VPC CIDR and must not overlap another subnet in that VPC.   [sources: aws_vpc_user_guide#subnet-sizing.html]
A.f2: IPv4 subnet sizes range from /16 to /28; AWS reserves the first four addresses and the last address of each subnet.   [sources: aws_vpc_user_guide#subnet-sizing.html]
A.f3: Choose subnet ranges inside the VPC that do not intersect, and allow for the five reserved addresses when checking usable capacity.   [sources: aws_vpc_user_guide#subnet-sizing.html]
A.f4: Each subnet resides entirely in one Availability Zone; create separate subnets for workloads in different Availability Zones.   [sources: aws_vpc_user_guide#configure-subnets.html]
note: Do not reteach CIDR arithmetic; require demonstrated external networking.ip_addressing_and_cidr mastery.
PRACTICE ANCHOR (field_selection): Allocate two subnet CIDRs within the supplied VPC 10.20.0.0/16, assigning one subnet to each of two supplied Availability Zones. Select from candidate ranges to provide at least 200 usable IPv4 addresses per subnet.  SUCCESS: Both selected subnet CIDRs are within 10.20.0.0/16, do not overlap, and have prefix lengths within /16 through /28. Each provides at least 200 usable addresses after subtracting the five AWS-reserved addresses, and each is assigned entirely to a different supplied Availability Zone.
ASSESSMENT ANCHOR: identify_subnet_containment_and_overlap_errors facts=['f1', 'f3']
ASSESSMENT ANCHOR: identify_subnet_size_and_usable_capacity_errors facts=['f2', 'f3']
ASSESSMENT ANCHOR: identify_invalid_subnet_availability_zone_assignments facts=['f4']

## DATA ASSETS USED
ds.subnet_candidates: Subnet allocation candidates — columns: candidate_id(identifier), vpc_cidr(identifier), subnet_cidr(identifier), availability_zone(categorical), total_addresses(numerical), usable_addresses(numerical), required_usable_addresses(numerical), reserved_addresses(text)
   ["candidate.1","10.20.0.0/16","10.20.1.0/24","Zone A",256,251,200,"10.20.1.0 through 10.20.1.3; 10.20.1.255"]
   ["candidate.2","10.20.0.0/16","10.20.2.0/24","Zone B",256,251,200,"10.20.2.0 through 10.20.2.3; 10.20.2.255"]
   ["candidate.3","10.20.0.0/16","10.20.1.128/25","Zone B",128,123,200,"10.20.1.128 through 10.20.1.131; 10.20.1.255"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute an AWS change using CloudTrail evidence; Attribute workload spend using resource tags; Centralize structured application logs in CloudWatch Logs; Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation; Choose rolling, blue/green or canary delivery for stated availability and rollback requirements; Cloudformation change sets; Collect host telemetry with the CloudWatch agent; Compare ECS and managed EKS operational ownership; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure role trust; directly require native IAM identity-policy evaluation; Configure subnet internet routing, teaching route-table association and CIDR destination routes; assume only external CIDR/IP addressing; Define recovery time and recovery point objectives; Distinguish AWS-managed and customer operational responsibilities; Distinguish capacity requirements from availability requirements; Establish service ownership and escalation; Evaluate an IAM identity policy for a requested operation after external access-control preparation; Execute a GitHub Actions workflow with an approp

## LESSON, in learner order

### s01 · explainer · Check the operating model
Learn — 
(intro) For two Availability Zones, check both address fit and usable capacity. Complete the external IP-addressing and CIDR preparation first. ⟦A:tb1⟧
(definition) An IPv4 subnet CIDR must be within its VPC CIDR and must not overlap another subnet in that VPC. ⟦A.f1 A:tb2⟧
(mechanism) IPv4 subnet sizes range from /16 to /28; AWS reserves the first four addresses and the last address of each subnet. ⟦A.f2 A:tb3⟧
(mechanism) Choose subnet ranges inside the VPC that do not intersect, and allow for the five reserved addresses when checking usable capacity. ⟦A.f3 A:tb3⟧
(mechanism) Each subnet resides entirely in one Availability Zone; create separate subnets for workloads in different Availability Zones. ⟦A.f4 A:tb3⟧
[DIAGRAM: Contained ranges: separate zones, separate usable-capacity checks] nodes=['10.20.0.0/16 {VPC range}', '10.20.1.0/24 {Zone A; Reserved: 10.20.1.0 through 10.20.1.3; 10.20.1.255; Usable addresses: 251}', '10.20.2.0/24 {Zone B; Reserved: 10.20.2.0 through 10.20.2.3; 10.20.2.255; Usable addresses: 251}', '10.20.1.128/25 {Zone B; Reserved: 10.20.1.128 through 10.20.1.131; 10.20.1.255; Usable addresses: 123}'] edges=[('n0', 'n1', 'inside VPC'), ('n0', 'n2', 'inside VPC'), ('n0', 'n3', 'inside VPC'), ('n1', 'n2', 'nonintersecting ranges'), ('n1', 'n3', 'candidate lies within first subnet: overlap')] alt: Contained ranges: separate zones, separate usable-capacity checks. 10.20.0.0/16: VPC range; 10.20.1.0/24: Zone A, Reserved: 10.20.1.0 through 10.20.1.3; 10.20.1.255, Usable addresses: 251; 10.20.2.0/24: Zone B, Reserved: 10.20.2.0 through 10.20.2.3; 10.20.2.255, Usable addresses: 251; 10.20.1.128/25: Zone B, Reserved: 10.20.1.128 through 10.20.1.131; 10.20.1.255, Usable addresses: 123
[TABLE ds.subnet_candidates cols=['candidate_id', 'vpc_cidr', 'subnet_cidr', 'availability_zone', 'total_addresses', 'usable_addresses', 'required_usable_addresses', 'reserved_addresses'] ] caption: Subnet allocation candidates

### s02 · explainer · Read the sandbox case
Learn — 
(example) The allocation worksheet places separate, nonintersecting subnets inside the VPC in different zones. Compare usable addresses, not total addresses, with the requirement. The overlapping candidate remains invalid even though it fits inside the VPC. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧
(misconception) VPC containment does not excuse overlap, and total addresses do not establish usable capacity. One subnet cannot span zones. ⟦A.f1 A.f2 A.f3 A.f4 A:tb5⟧

### s03 · check · Choose the supported conclusion
Check — Read the supplied excerpts in this step and decide which conclusions are correct, defective or unsafe.

### s04 · hands_on · Review the supplied evidence
Review — Inspect the supplied table and select the entries that satisfy the stated requirement.

### s05 · recap · Keep the distinctions
Recap — 
(takeaway) Require containment, nonoverlap, allowed subnet size and capacity after reservations. Use separate subnets for separate Availability Zones. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Compare ECS and managed EKS operational ownership: Continue to aws_devops.tile.002.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the two kinds of evidence
(definition) Each subnet resides entirely in one Availability Zone; create separate subnets for workloads in different Availability Zones. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) VPC containment does not excuse overlap, and total addresses do not establish usable capacity. One subnet cannot span zones. ⟦A.f1 A.f2 A.f3 A.f4 A:tb5⟧
[TABLE ds.subnet_candidates cols=['candidate_id', 'vpc_cidr', 'subnet_cidr', 'availability_zone', 'total_addresses', 'usable_addresses', 'required_usable_addresses', 'reserved_addresses'] ] caption: Subnet allocation candidates
### r02 · Separate the two kinds of evidence
(definition) An IPv4 subnet CIDR must be within its VPC CIDR and must not overlap another subnet in that VPC. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) IPv4 subnet sizes range from /16 to /28; AWS reserves the first four addresses and the last address of each subnet. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Choose subnet ranges inside the VPC that do not intersect, and allow for the five reserved addresses when checking usable capacity. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(definition) Each subnet resides entirely in one Availability Zone; create separate subnets for workloads in different Availability Zones. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) VPC containment does not excuse overlap, and total addresses do not establish usable capacity. One subnet cannot span zones. ⟦A.f1 A.f2 A.f3 A.f4 A:tb5⟧
[TABLE ds.subnet_candidates cols=['candidate_id', 'vpc_cidr', 'subnet_cidr', 'availability_zone', 'total_addresses', 'usable_addresses', 'required_usable_addresses', 'reserved_addresses'] ] caption: Subnet allocation candidates

=========

# EVALUATOR PACKET — Compare ECS and managed EKS operational ownership (aws_devops.tile.002)
Tile summary: ECS manages scheduling; managed EKS manages the Kubernetes control plane. Retain application duties and the compute-dependent worker-node qualification. Compare Kubernetes needs with team willingness.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.compare_ecs_and_managed_eks_operational_ownership — Compare ECS and managed EKS operational ownership

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.compare_ecs_and_managed_eks_operational_ownership)   objective: Choose ECS or managed EKS from an operational-ownership requirement
A.f1: ECS is a managed container orchestration service that schedules container workloads; customers supply and operate their applications.   [sources: aws_ecs_developer_guide#Welcome.html]
A.f2: Managed EKS runs the Kubernetes control plane; customers retain responsibility for workload configuration and, depending on the compute option, worker nodes.   [sources: aws_eks_user_guide#security.html]
A.f3: Choose between ECS and EKS by comparing the need for Kubernetes APIs and ecosystem with the team’s willingness to operate Kubernetes workloads.   [sources: aws_eks_user_guide#what-is-eks.html]
note: Keep this comparison short; do not introduce self-managed Kubernetes administration.
PRACTICE ANCHOR (field_selection): Select ECS or managed EKS for a supplied team's Kubernetes API and ecosystem requirements and willingness to operate Kubernetes workloads. Select the corresponding platform and customer responsibilities, preserving the compute-option qualification for EKS worker nodes.  SUCCESS: The selected platform fits the supplied requirements and operating constraints. The responsibility selections identify ECS-managed container scheduling and customer-operated applications, or the EKS-managed Kubernetes control plane and customer workload configuration, with worker-node responsibility dependent on the compute option.
ASSESSMENT ANCHOR: assign_ecs_platform_and_application_responsibilities facts=['f1']
ASSESSMENT ANCHOR: assign_managed_eks_control_plane_workload_and_compute_dependent_node_responsibilities facts=['f2']
ASSESSMENT ANCHOR: align_platform_choice_and_retained_responsibilities_with_team_constraints facts=['f1', 'f2', 'f3']

## DATA ASSETS USED
ds.container_ownership: Container platform requirements and retained duties — columns: requirement_case(categorical), needs_kubernetes_apis_and_ecosystem(categorical), willing_to_operate_kubernetes_workloads(categorical), platform(categorical), managed_platform_duties(text), customer_workload_duties(text), worker_node_qualification(text)
   ["Kubernetes requirement",true,true,"ECS","Container workload scheduling","Supply and operate applications","Not specified by this ECS comparison"]
   ["Kubernetes requirement",true,true,"managed EKS","Kubernetes control plane","Configure and operate Kubernetes workloads","Worker-node responsibility depends on the selected compute option"]
   ["No Kubernetes dependency",false,false,"ECS","Container workload scheduling","Supply and operate applications","Not specified by this ECS comparison"]
   ["No Kubernetes dependency",false,false,"managed EKS","Kubernetes control plane","Configure and operate Kubernetes workloads","Worker-node responsibility depends on the selected compute option"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute an AWS change using CloudTrail evidence; Attribute workload spend using resource tags; Centralize structured application logs in CloudWatch Logs; Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation; Choose rolling, blue/green or canary delivery for stated availability and rollback requirements; Cloudformation change sets; Collect host telemetry with the CloudWatch agent; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure role trust; directly require native IAM identity-policy evaluation; Configure secure human access with temporary credentials; Configure subnet internet routing, teaching route-table association and CIDR destination routes; assume only external CIDR/IP addressing; Define recovery time and recovery point objectives; Distinguish AWS-managed and customer operational responsibilities; Distinguish capacity requirements from availability requirements; Establish service ownership and escalation; Evaluate an IAM identity policy for a requested operation after external access-control preparation; Execute a GitHub Actions workflow with an

## LESSON, in learner order

### s01 · explainer · Check the operating model
Learn — 
(intro) Compare platform work with the application work the team retains, not just the word managed. ⟦A:tb1⟧
(definition) ECS is a managed container orchestration service that schedules container workloads; customers supply and operate their applications. ⟦A.f1 A:tb2⟧
(mechanism) Managed EKS runs the Kubernetes control plane; customers retain responsibility for workload configuration and, depending on the compute option, worker nodes. ⟦A.f2 A:tb3⟧
(mechanism) Choose between ECS and EKS by comparing the need for Kubernetes APIs and ecosystem with the team’s willingness to operate Kubernetes workloads. ⟦A.f3 A:tb3⟧
[TABLE ds.container_ownership cols=['requirement_case', 'needs_kubernetes_apis_and_ecosystem', 'willing_to_operate_kubernetes_workloads', 'platform', 'managed_platform_duties', 'customer_workload_duties', 'worker_node_qualification'] ] caption: Container platform requirements and retained duties

### s02 · explainer · Read the sandbox case
Learn — 
(example) A Kubernetes API and ecosystem requirement points the comparison toward managed EKS, provided the team is willing to operate Kubernetes workloads. Without that dependency, compare the ECS scheduling option. Neither proposal transfers application operation to AWS; retain the compute-option qualification for EKS worker-node duties. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) Managed does not mean AWS operates the application. EKS worker-node duties remain compute-dependent. ⟦A.f1 A.f2 A:tb5⟧

### s03 · check · Choose the supported conclusion
Check — Read the supplied excerpts in this step and decide which conclusions are correct, defective or unsafe.

### s04 · hands_on · Review the supplied evidence
Review — Inspect the supplied table and select the entries that satisfy the stated requirement.

### s05 · recap · Keep the distinctions
Recap — 
(takeaway) ECS manages scheduling; managed EKS manages the Kubernetes control plane. Retain application duties and the compute-dependent worker-node qualification. Compare Kubernetes needs with team willingness. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Configure subnet internet routing, teaching route-table association and CIDR destination routes; assume only external CIDR/IP addressing: Continue to aws_devops.tile.003.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the two kinds of evidence
(definition) ECS is a managed container orchestration service that schedules container workloads; customers supply and operate their applications. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Managed EKS runs the Kubernetes control plane; customers retain responsibility for workload configuration and, depending on the compute option, worker nodes. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Choose between ECS and EKS by comparing the need for Kubernetes APIs and ecosystem with the team’s willingness to operate Kubernetes workloads. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) Managed does not mean AWS operates the application. EKS worker-node duties remain compute-dependent. ⟦A.f1 A.f2 A:tb5⟧
[TABLE ds.container_ownership cols=['requirement_case', 'needs_kubernetes_apis_and_ecosystem', 'willing_to_operate_kubernetes_workloads', 'platform', 'managed_platform_duties', 'customer_workload_duties', 'worker_node_qualification'] ] caption: Container platform requirements and retained duties

=========

# EVALUATOR PACKET — Configure subnet internet routing, teaching route-table association and CIDR destination routes; assume only external CIDR/IP addressing (aws_devops.tile.003)
Tile summary: Establish explicit association or main-table fallback first. Prefer the most specific matching prefix. The attached internet-gateway default serves destinations without a more specific match.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.configure_subnet_internet_routing — Configure subnet internet routing, teaching route-table association and CIDR destination routes; assume only external CIDR/IP addressing

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.configure_subnet_internet_routing)   objective: Configure subnet internet routing
A.f1: A subnet uses its explicitly associated route table or, without an explicit association, the VPC main route table.   [sources: aws_vpc_user_guide#subnet-route-tables.html]
A.f2: Among matching destination routes, the most specific destination prefix takes priority.   [sources: aws_vpc_user_guide#route-tables-priority.html]
A.f3: Associate the subnet with the intended route table and add an IPv4 0.0.0.0/0 route targeting the attached internet gateway for internet-bound destinations not matched by a more specific route.   [sources: aws_vpc_user_guide#VPC_Internet_Gateway.html]
note: Teach route selection only; leave security rules and end-to-end connectivity diagnosis to their later concepts.
PRACTICE ANCHOR (tool_simulation): Associate the supplied subnet with the intended route table and configure an IPv4 0.0.0.0/0 route targeting the supplied internet gateway, which is already attached to the VPC.  SUCCESS: The subnet is explicitly associated with the intended route table. That table retains its 10.20.0.0/16 route and contains a 0.0.0.0/0 route targeting the supplied attached internet gateway.
ASSESSMENT ANCHOR: select_effective_subnet_route_table facts=['f1']
ASSESSMENT ANCHOR: select_most_specific_matching_destination_route facts=['f2', 'f3']
ASSESSMENT ANCHOR: select_ipv4_default_route_and_internet_gateway_target facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute an AWS change using CloudTrail evidence; Attribute workload spend using resource tags; Centralize structured application logs in CloudWatch Logs; Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation; Choose rolling, blue/green or canary delivery for stated availability and rollback requirements; Cloudformation change sets; Collect host telemetry with the CloudWatch agent; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure role trust; directly require native IAM identity-policy evaluation; Configure secure human access with temporary credentials; Configure security groups after external ports/firewall preparation; Define recovery time and recovery point objectives; Distinguish AWS-managed and customer operational responsibilities; Distinguish capacity requirements from availability requirements; Establish service ownership and escalation; Evaluate an IAM identity policy for a requested operation after external access-control preparation; Execute a GitHub Actions workflow with an appropriate runner; Input target validation; Interpret DORA delivery

## LESSON, in learner order

### s01 · explainer · Check the operating model
Learn — 
(intro) Check which route table the subnet uses before comparing destination matches. ⟦A:tb1⟧
(definition) A subnet uses its explicitly associated route table or, without an explicit association, the VPC main route table. ⟦A.f1 A:tb2⟧
(mechanism) Among matching destination routes, the most specific destination prefix takes priority. ⟦A.f2 A:tb3⟧
(mechanism) Associate the subnet with the intended route table and add an IPv4 0.0.0.0/0 route targeting the attached internet gateway for internet-bound destinations not matched by a more specific route. ⟦A.f3 A:tb3⟧
[DIAGRAM: Before and after explicit subnet association] nodes=['Subnet: before {No explicit route-table association}', 'VPC main route table {Used by fallback before association}', 'Subnet: afterward {Explicitly associated with intended table}', 'Intended route table {10.20.0.0/16; 0.0.0.0/0 → attached internet gateway}', '10.20.2.10 {Matches both displayed prefixes; select the more specific /16}', '198.51.100.8 {Select internet-gateway default when no more specific route matches}'] edges=[('n0', 'n1', 'main-table fallback'), ('n2', 'n3', 'explicit association'), ('n3', 'n4', 'more specific match'), ('n3', 'n5', 'default match')] alt: Before and after explicit subnet association. Subnet: before: No explicit route-table association; VPC main route table: Used by fallback before association; Subnet: afterward: Explicitly associated with intended table; Intended route table: 10.20.0.0/16, 0.0.0.0/0 → attached internet gateway; 10.20.2.10: Matches both displayed prefixes; select the more specific /16; 198.51.100.8: Select internet-gateway default when no more specific route matches

### s02 · explainer · Read the sandbox case
Learn — 
(example) In the intended table, 10.20.2.10 matches both 10.20.0.0/16 and 0.0.0.0/0; the more specific prefix wins. 198.51.100.8 uses the internet-gateway default when no more specific route matches. First verify association: without an explicit association, the subnet uses the main table, not necessarily the table you edited. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) Editing a table does not establish association. A default route does not override more specific matches or prove a working connection. ⟦A.f1 A.f2 A.f3 A:tb5⟧

### s03 · check · Choose the supported conclusion
Check — Read the supplied excerpts in this step and decide which conclusions are correct, defective or unsafe.

### s04 · hands_on · Review the supplied evidence
Review — Read the supplied excerpts in this step and decide which conclusions are correct, defective or unsafe.

### s05 · recap · Keep the distinctions
Recap — 
(takeaway) Establish explicit association or main-table fallback first. Prefer the most specific matching prefix. The attached internet-gateway default serves destinations without a more specific match. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Define recovery time and recovery point objectives: Continue to aws_devops.tile.004.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the two kinds of evidence
(definition) Among matching destination routes, the most specific destination prefix takes priority. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Associate the subnet with the intended route table and add an IPv4 0.0.0.0/0 route targeting the attached internet gateway for internet-bound destinations not matched by a more specific route. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Editing a table does not establish association. A default route does not override more specific matches or prove a working connection. ⟦A.f1 A.f2 A.f3 A:tb5⟧
(example) Return to the same intended route table: distinguish the internal destination’s more specific match from the external destination’s default match. ⟦A.f1 A.f2 A.f3 A:tb4⟧
### r02 · Separate the two kinds of evidence
(definition) A subnet uses its explicitly associated route table or, without an explicit association, the VPC main route table. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Associate the subnet with the intended route table and add an IPv4 0.0.0.0/0 route targeting the attached internet gateway for internet-bound destinations not matched by a more specific route. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Editing a table does not establish association. A default route does not override more specific matches or prove a working connection. ⟦A.f1 A.f2 A.f3 A:tb5⟧
(example) Return to the same intended route table: distinguish the internal destination’s more specific match from the external destination’s default match. ⟦A.f1 A.f2 A.f3 A:tb4⟧

=========

# EVALUATOR PACKET — Define recovery time and recovery point objectives (aws_devops.tile.004)
Tile summary: Derive RTO and RPO from business requirements. Compare recovery capabilities with both restoration-time and time-based data-loss limits.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.define_recovery_time_and_recovery_point_objectives — Define recovery time and recovery point objectives

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.define_recovery_time_and_recovery_point_objectives)   objective: Set recovery time and recovery point objectives
A.f1: Recovery time objective (RTO) is the maximum acceptable time to restore service after a disruption.   [sources: aws_wa_devops_guidance#ag.dlm.1-define-recovery-objectives-to-maintain-business-continuity.html]
A.f2: Recovery point objective (RPO) is the maximum acceptable data loss measured in time.   [sources: aws_wa_devops_guidance#ag.dlm.1-define-recovery-objectives-to-maintain-business-continuity.html]
A.f3: Set recovery objectives from business requirements and use them to choose recovery capabilities that meet the tolerated downtime and data loss.   [sources: aws_wa_devops_guidance#ag.dlm.1-define-recovery-objectives-to-maintain-business-continuity.html]
note: Keep measurement and rehearsal procedures for the later recovery-verification concept.
PRACTICE ANCHOR (field_selection): For one supplied workload, select RTO and RPO from the owner's stated downtime and data-loss tolerances. Choose a recovery approach from supplied options with stated restoration times and data-loss intervals, and justify the choice against both objectives.  SUCCESS: RTO matches the maximum tolerated service-restoration time, RPO matches the maximum tolerated data loss measured in time, and the selected approach meets both limits. The justification compares each supplied capability with its corresponding business requirement.
ASSESSMENT ANCHOR: distinguish_downtime_tolerance_from_acceptable_data_loss facts=['f1', 'f2']

## DATA ASSETS USED
ds.recovery_options: Business recovery limits and candidate capabilities — columns: approach_id(identifier), rto_minutes(numerical), rpo_minutes(numerical), restoration_minutes(numerical), data_loss_minutes(numerical)
   ["approach.both",30,5,30,5]
   ["approach.stale_data",30,5,30,20]
   ["approach.slow_restore",30,5,60,5]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute an AWS change using CloudTrail evidence; Attribute workload spend using resource tags; Centralize structured application logs in CloudWatch Logs; Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation; Choose rolling, blue/green or canary delivery for stated availability and rollback requirements; Cloudformation change sets; Collect host telemetry with the CloudWatch agent; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure role trust; directly require native IAM identity-policy evaluation; Configure secure human access with temporary credentials; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Distinguish AWS-managed and customer operational responsibilities; Distinguish capacity requirements from availability requirements; Establish service ownership and escalation; Evaluate an IAM identity policy for a requested operation after external access-control preparation; Execute a GitHub Actions workflow with an ap

## LESSON, in learner order

### s01 · explainer · Check the operating model
Learn — 
(intro) Name tolerated downtime and tolerated data loss separately; they are different business requirements. ⟦A:tb1⟧
(definition) Recovery time objective (RTO) is the maximum acceptable time to restore service after a disruption. ⟦A.f1 A:tb2⟧
(mechanism) Recovery point objective (RPO) is the maximum acceptable data loss measured in time. ⟦A.f2 A:tb3⟧
(mechanism) Set recovery objectives from business requirements and use them to choose recovery capabilities that meet the tolerated downtime and data loss. ⟦A.f3 A:tb3⟧
[TABLE ds.recovery_options cols=['approach_id', 'rto_minutes', 'rpo_minutes', 'restoration_minutes', 'data_loss_minutes'] ] caption: Business recovery limits and candidate capabilities

### s02 · explainer · Read the sandbox case
Learn — 
(example) Compare each recovery approach with both business limits in the table. Meeting restoration time while losing too much recent data fails the data-loss requirement. Recent data alone does not establish timely restoration. These are illustrative business limits, not recommended AWS defaults. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) RTO bounds restoration time; RPO bounds data loss measured in time. Neither substitutes for the other. ⟦A.f1 A.f2 A.f3 A:tb5⟧

### s03 · check · Choose the supported conclusion
Check — Read the supplied excerpts in this step and decide which conclusions are correct, defective or unsafe.

### s04 · hands_on · Review the supplied evidence
Review — Inspect the supplied table and select the entries that satisfy the stated requirement.

### s05 · recap · Keep the distinctions
Recap — 
(takeaway) Derive RTO and RPO from business requirements. Compare recovery capabilities with both restoration-time and time-based data-loss limits. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Distinguish AWS-managed and customer operational responsibilities: Continue to aws_devops.tile.005.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the two kinds of evidence
(definition) Recovery time objective (RTO) is the maximum acceptable time to restore service after a disruption. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Recovery point objective (RPO) is the maximum acceptable data loss measured in time. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) RTO bounds restoration time; RPO bounds data loss measured in time. Neither substitutes for the other. ⟦A.f1 A.f2 A.f3 A:tb5⟧
[TABLE ds.recovery_options cols=['approach_id', 'rto_minutes', 'rpo_minutes', 'restoration_minutes', 'data_loss_minutes'] ] caption: Business recovery limits and candidate capabilities

=========

# EVALUATOR PACKET — Distinguish AWS-managed and customer operational responsibilities (aws_devops.tile.005)
Tile summary: EC2 guest-OS updates remain customer work. RDS infrastructure and OS maintenance are AWS work; customer data, access and controlled engine configuration remain customer duties.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.distinguish_aws_managed_and_customer_operational_responsibilities — Distinguish AWS-managed and customer operational responsibilities

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.distinguish_aws_managed_and_customer_operational_responsibilities)   objective: Assign AWS and customer operating responsibility
A.f1: With EC2, customers manage the guest operating system, including updates and security patches.   [sources: aws_rds_user_guide#Welcome.html#Welcome.Concepts.SharedResponsibility]
A.f2: With RDS, AWS manages database infrastructure and operating-system maintenance, while customers manage their data and application use.   [sources: aws_rds_user_guide#Welcome.html#Welcome.Concepts.SharedResponsibility]
A.f3: Assign duties by the service boundary: AWS manages its infrastructure, while customers retain responsibilities for data, access and customer-controlled configuration.   [sources: aws_rds_user_guide#Welcome.html#Welcome.Concepts.SharedResponsibility]
A.f4: Interpret the supplied EC2 OS-update report as customer guest-OS work and the supplied RDS parameter-check report as customer-controlled database configuration; RDS parameter groups contain database engine configuration values.   [sources: aws_rds_user_guide#USER_WorkingWithParamGroups.html]
note: Do not introduce database capacity selection or specialist database administration.
PRACTICE ANCHOR (matching): Produce one responsibility assignment for a workload using EC2 and RDS by matching the supplied duties and reports to AWS or the customer and identifying the relevant service boundary.  SUCCESS: The assignment places EC2 guest-OS updates and security patches with the customer; RDS database infrastructure and operating-system maintenance with AWS; and data, access, application use and customer-controlled configuration with the customer. It classifies the EC2 OS-update report as customer guest-OS work and the RDS parameter-check report as customer-controlled database engine configuration.
ASSESSMENT ANCHOR: assign_operating_system_maintenance_by_service facts=['f1', 'f2']
ASSESSMENT ANCHOR: assign_data_access_and_configuration_responsibilities facts=['f2', 'f3']
ASSESSMENT ANCHOR: classify_supplied_reports_by_service_boundary facts=['f4']

## DATA ASSETS USED
ds.service_responsibilities: EC2 and RDS responsibility boundaries — columns: service(categorical), duty_or_report(text), responsible_party(categorical), boundary_rationale(text)
   ["EC2","Guest-OS updates and security patches","Customer","Customer guest-operating-system maintenance"]
   ["EC2","Supplied OS-update report","Customer","Report concerns guest-operating-system work"]
   ["RDS","Database infrastructure","AWS","Managed database infrastructure"]
   ["RDS","Operating-system maintenance","AWS","Managed operating-system maintenance"]
   ["RDS","Supplied parameter-check report","Customer","Parameter groups contain customer-controlled database engine configuration values"]
   ["RDS","Data, access and application use","Customer","Retained customer responsibilities"]
   ["EC2","Data, access and customer-controlled configuration","Customer","Retained customer responsibilities"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute an AWS change using CloudTrail evidence; Attribute workload spend using resource tags; Centralize structured application logs in CloudWatch Logs; Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation; Choose rolling, blue/green or canary delivery for stated availability and rollback requirements; Cloudformation change sets; Collect host telemetry with the CloudWatch agent; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure role trust; directly require native IAM identity-policy evaluation; Configure secure human access with temporary credentials; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Distinguish capacity requirements from availability requirements; Establish service ownership and escalation; Evaluate an IAM identity policy for a requested operation after external access-control preparation; Evaluate resource-based permissions for a requested operation; Execute a GitHub Actions workflow with an approp

## LESSON, in learner order

### s01 · explainer · Check the operating model
Learn — 
(intro) Route the EC2 update and RDS parameter-check reports by the service boundary. ⟦A:tb1⟧
(definition) With EC2, customers manage the guest operating system, including updates and security patches. ⟦A.f1 A:tb2⟧
(mechanism) With RDS, AWS manages database infrastructure and operating-system maintenance, while customers manage their data and application use. ⟦A.f2 A:tb3⟧
(mechanism) Assign duties by the service boundary: AWS manages its infrastructure, while customers retain responsibilities for data, access and customer-controlled configuration. ⟦A.f3 A:tb3⟧
(mechanism) Interpret the supplied EC2 OS-update report as customer guest-OS work and the supplied RDS parameter-check report as customer-controlled database configuration; RDS parameter groups contain database engine configuration values. ⟦A.f4 A:tb3⟧
[TABLE ds.service_responsibilities cols=['service', 'duty_or_report', 'responsible_party', 'boundary_rationale'] ] caption: EC2 and RDS responsibility boundaries

### s02 · explainer · Read the sandbox case
Learn — 
(example) The EC2 OS-update report concerns customer guest-OS work. The RDS parameter-check report concerns customer-controlled engine configuration values, not AWS-managed OS maintenance. Name that boundary in the handoff; customer data and access duties remain. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧
(misconception) EC2 guest-OS patching is customer work; RDS OS maintenance is AWS work. RDS customer configuration and data duties remain. ⟦A.f1 A.f2 A.f3 A.f4 A:tb5⟧

### s03 · check · Choose the supported conclusion
Check — Read the supplied excerpts in this step and decide which conclusions are correct, defective or unsafe.

### s04 · hands_on · Review the supplied evidence
Review — Read the supplied excerpts in this step and decide which conclusions are correct, defective or unsafe.

### s05 · recap · Keep the distinctions
Recap — 
(takeaway) EC2 guest-OS updates remain customer work. RDS infrastructure and OS maintenance are AWS work; customer data, access and controlled engine configuration remain customer duties. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Distinguish capacity requirements from availability requirements: Continue to aws_devops.tile.006.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the two kinds of evidence
(definition) Interpret the supplied EC2 OS-update report as customer guest-OS work and the supplied RDS parameter-check report as customer-controlled database configuration; RDS parameter groups contain database engine configuration values. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) EC2 guest-OS patching is customer work; RDS OS maintenance is AWS work. RDS customer configuration and data duties remain. ⟦A.f1 A.f2 A.f3 A.f4 A:tb5⟧
[TABLE ds.service_responsibilities cols=['service', 'duty_or_report', 'responsible_party', 'boundary_rationale'] ] caption: EC2 and RDS responsibility boundaries
### r02 · Separate the two kinds of evidence
(definition) With EC2, customers manage the guest operating system, including updates and security patches. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) With RDS, AWS manages database infrastructure and operating-system maintenance, while customers manage their data and application use. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Assign duties by the service boundary: AWS manages its infrastructure, while customers retain responsibilities for data, access and customer-controlled configuration. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(definition) Interpret the supplied EC2 OS-update report as customer guest-OS work and the supplied RDS parameter-check report as customer-controlled database configuration; RDS parameter groups contain database engine configuration values. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) EC2 guest-OS patching is customer work; RDS OS maintenance is AWS work. RDS customer configuration and data duties remain. ⟦A.f1 A.f2 A.f3 A.f4 A:tb5⟧
[TABLE ds.service_responsibilities cols=['service', 'duty_or_report', 'responsible_party', 'boundary_rationale'] ] caption: EC2 and RDS responsibility boundaries

=========

# EVALUATOR PACKET — Distinguish capacity requirements from availability requirements (aws_devops.tile.006)
Tile summary: Match capacity to demand. Separately evaluate independent surviving capacity for a component-failure constraint; equal totals do not settle availability.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.distinguish_capacity_requirements_from_availability_requirements — Distinguish capacity requirements from availability requirements

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.distinguish_capacity_requirements_from_availability_requirements)   objective: Distinguish capacity from availability requirements
A.f1: Redundant components and multiple locations can keep a workload available when a component fails.   [sources: aws_well_architected_framework#rel11.html]
A.f2: Capacity must accommodate workload demand; adding or removing resources helps match capacity to changing demand.   [sources: aws_well_architected_framework#rel07.html]
A.f3: For a component-failure constraint, evaluate independent redundant capacity rather than merely increasing the size of the same component.   [sources: aws_well_architected_framework#rel11.html]
note: Defer specific scaling-policy and controlled-AZ-failure procedures.
PRACTICE ANCHOR (field_selection): Select one design change from supplied proposals for a lab facing either changing demand or loss of one component.  SUCCESS: For changing demand, select a resource adjustment that matches capacity to the supplied demand. For component loss, select independent redundant capacity whose surviving components meet the supplied service requirement, rather than merely enlarging the same component.
ASSESSMENT ANCHOR: identify_demand_constraints_requiring_scaling facts=['f2']
ASSESSMENT ANCHOR: identify_failure_constraints_requiring_independent_redundancy facts=['f1', 'f3']

## DATA ASSETS USED
ds.capacity_proposals: Ordinary demand versus surviving capacity — columns: proposal(categorical), independent_components(numerical), capacity_per_component(numerical), total_capacity(numerical), surviving_capacity_after_one_loss(numerical), ordinary_demand(numerical), required_capacity_after_one_loss(numerical), placement(text)
   ["One larger component",1,400,400,0,200,200,"One location"]
   ["Two independent components",2,200,400,200,200,200,"Two independent locations"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute an AWS change using CloudTrail evidence; Attribute workload spend using resource tags; Centralize structured application logs in CloudWatch Logs; Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation; Choose rolling, blue/green or canary delivery for stated availability and rollback requirements; Cloudformation change sets; Collect host telemetry with the CloudWatch agent; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure role trust; directly require native IAM identity-policy evaluation; Configure secure human access with temporary credentials; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Establish service ownership and escalation; Evaluate an IAM identity policy for a requested operation after external access-control preparation; Evaluate resource-based permissions for a requested operation; Execute a GitHub Actions workflow with an appropriate runner; Execute an established managed account-onboarding wo

## LESSON, in learner order

### s01 · explainer · Check the operating model
Learn — 
(intro) Separate ordinary demand from the service requirement after a component fails. ⟦A:tb1⟧
(definition) Redundant components and multiple locations can keep a workload available when a component fails. ⟦A.f1 A:tb2⟧
(mechanism) Capacity must accommodate workload demand; adding or removing resources helps match capacity to changing demand. ⟦A.f2 A:tb3⟧
(mechanism) For a component-failure constraint, evaluate independent redundant capacity rather than merely increasing the size of the same component. ⟦A.f3 A:tb3⟧
[SIDE_BY_SIDE] Equal total capacity does not settle surviving capacity after one component is lost. left_label: One larger component | right_label: Two independent components
  left:
[DIAGRAM: One larger component] nodes=['Single component {Loss removes this component’s capacity}'] edges=[] alt: One larger component. Single component: Loss removes this component’s capacity
  right:
[DIAGRAM: Two independent components] nodes=['Independent component A {Capacity remains if the other component is lost}', 'Independent component B {Capacity remains if the other component is lost}'] edges=[] alt: Two independent components. Independent component A: Capacity remains if the other component is lost; Independent component B: Capacity remains if the other component is lost
[TABLE ds.capacity_proposals cols=['proposal', 'independent_components', 'capacity_per_component', 'total_capacity', 'surviving_capacity_after_one_loss', 'ordinary_demand', 'required_capacity_after_one_loss', 'placement'] ] caption: Ordinary demand versus surviving capacity

### s02 · explainer · Read the sandbox case
Learn — 
(example) Both proposals have equal total capacity. Evaluate that capacity against ordinary demand, then evaluate independent surviving capacity against the post-loss service requirement. A larger single component can address demand without answering the failure requirement. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) Increasing one component’s size is not independent redundancy. Ordinary capacity and post-loss capacity answer separate requirements. ⟦A.f1 A.f2 A.f3 A:tb5⟧

### s03 · check · Choose the supported conclusion
Check — Read the supplied excerpts in this step and decide which conclusions are correct, defective or unsafe.

### s04 · check · Choose the supported conclusion
Check — Read the supplied excerpts in this step and decide which conclusions are correct, defective or unsafe.

### s05 · hands_on · Review the supplied evidence
Review — Inspect the supplied table and select the entries that satisfy the stated requirement.

### s06 · recap · Keep the distinctions
Recap — 
(takeaway) Match capacity to demand. Separately evaluate independent surviving capacity for a component-failure constraint; equal totals do not settle availability. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Establish service ownership and escalation: Continue to aws_devops.tile.007.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the two kinds of evidence
(definition) Capacity must accommodate workload demand; adding or removing resources helps match capacity to changing demand. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) Increasing one component’s size is not independent redundancy. Ordinary capacity and post-loss capacity answer separate requirements. ⟦A.f1 A.f2 A.f3 A:tb5⟧
[TABLE ds.capacity_proposals cols=['proposal', 'independent_components', 'capacity_per_component', 'total_capacity', 'surviving_capacity_after_one_loss', 'ordinary_demand', 'required_capacity_after_one_loss', 'placement'] ] caption: Ordinary demand versus surviving capacity
### r02 · Separate the two kinds of evidence
(definition) Redundant components and multiple locations can keep a workload available when a component fails. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) For a component-failure constraint, evaluate independent redundant capacity rather than merely increasing the size of the same component. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Increasing one component’s size is not independent redundancy. Ordinary capacity and post-loss capacity answer separate requirements. ⟦A.f1 A.f2 A.f3 A:tb5⟧
[TABLE ds.capacity_proposals cols=['proposal', 'independent_components', 'capacity_per_component', 'total_capacity', 'surviving_capacity_after_one_loss', 'ordinary_demand', 'required_capacity_after_one_loss', 'placement'] ] caption: Ordinary demand versus surviving capacity
### r03 · Separate the two kinds of evidence
(misconception) Increasing one component’s size is not independent redundancy. Ordinary capacity and post-loss capacity answer separate requirements. ⟦A.f1 A.f2 A.f3 A:tb5⟧
[TABLE ds.capacity_proposals cols=['proposal', 'independent_components', 'capacity_per_component', 'total_capacity', 'surviving_capacity_after_one_loss', 'ordinary_demand', 'required_capacity_after_one_loss', 'placement'] ] caption: Ordinary demand versus surviving capacity

=========

# EVALUATOR PACKET — Establish service ownership and escalation (aws_devops.tile.007)
Tile summary: Identify resource and process owners. Assign event response and document both the unresolved-issue escalation condition and the next recipient.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.establish_service_ownership_and_escalation — Establish service ownership and escalation

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.establish_service_ownership_and_escalation)   objective: Establish service ownership and escalation
A.f1: Operational events need response processes with identified owners and escalation paths.   [sources: aws_well_architected_framework#ops06.html]
A.f2: Assign event-response responsibility and document when and to whom unresolved issues are escalated.   [sources: aws_well_architected_framework#ops06.html]
A.f3: Identify a team responsible for each resource and process so operators know whom to engage.   [sources: aws_well_architected_framework#fnd01-bp02.html]
note: Use established owners and escalation conditions; do not author an organization-wide incident policy.
PRACTICE ANCHOR (field_selection): Complete an ownership and escalation record for the sandbox orders service using supplied established teams and escalation conditions. Select the service owner, associated-process owner, initial event responder, unresolved-issue escalation condition, and escalation recipient.  SUCCESS: The completed record matches the supplied responsibilities for both the service and its associated process, identifies who initially acts on an event, and specifies when and to whom an unresolved issue is escalated without inventing a new policy.
ASSESSMENT ANCHOR: identify_responsible_team_for_supplied_operational_alert facts=['f1', 'f3']
ASSESSMENT ANCHOR: identify_escalation_condition_and_next_responder facts=['f2']

## DATA ASSETS USED
ds.ownership_escalation: Sandbox orders service ownership and escalation — columns: resource(identifier), resource_owner(categorical), associated_process(identifier), process_owner(categorical), initial_event_responder(categorical), unresolved_issue_condition(text), escalation_recipient(categorical)
   ["sandbox orders service","application operations team","orders event-response process","process operations team","application operations team","Issue remains unresolved after the established routine response checklist is completed","process operations team"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute an AWS change using CloudTrail evidence; Attribute workload spend using resource tags; Centralize structured application logs in CloudWatch Logs; Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation; Choose rolling, blue/green or canary delivery for stated availability and rollback requirements; Cloudformation change sets; Collect host telemetry with the CloudWatch agent; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure role trust; directly require native IAM identity-policy evaluation; Configure secure human access with temporary credentials; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Evaluate an IAM identity policy for a requested operation after external access-control preparation; Evaluate resource-based permissions for a requested operation; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute a GitHub Actions workflow with an appr

## LESSON, in learner order

### s01 · explainer · Check the operating model
Learn — 
(intro) An unresolved event needs an accountable owner and a defined next responder. ⟦A:tb1⟧
(definition) Operational events need response processes with identified owners and escalation paths. ⟦A.f1 A:tb2⟧
(mechanism) Assign event-response responsibility and document when and to whom unresolved issues are escalated. ⟦A.f2 A:tb3⟧
(mechanism) Identify a team responsible for each resource and process so operators know whom to engage. ⟦A.f3 A:tb3⟧
[TABLE ds.ownership_escalation cols=['resource', 'resource_owner', 'associated_process', 'process_owner', 'initial_event_responder', 'unresolved_issue_condition', 'escalation_recipient'] ] caption: Sandbox orders service ownership and escalation

### s02 · explainer · Read the sandbox case
Learn — 
(example) Read the resource owner, process owner, initial responder, unresolved-issue condition and next recipient together. When the supplied checklist condition is reached, the established record identifies the recipient. These fictional team assignments and conditions are exercise inputs, not a universal escalation chain. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) Contacts alone are not an escalation path. Document when an unresolved issue moves on and to whom; name resource and process owners. ⟦A.f1 A.f2 A.f3 A:tb5⟧

### s03 · check · Choose the supported conclusion
Check — Read the supplied excerpts in this step and decide which conclusions are correct, defective or unsafe.

### s04 · hands_on · Review the supplied evidence
Review — Read the supplied excerpts in this step and decide which conclusions are correct, defective or unsafe.

### s05 · recap · Keep the distinctions
Recap — 
(takeaway) Identify resource and process owners. Assign event response and document both the unresolved-issue escalation condition and the next recipient. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Evaluate an IAM identity policy for a requested operation after external access-control preparation: Continue to aws_devops.tile.008.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the two kinds of evidence
(definition) Assign event-response responsibility and document when and to whom unresolved issues are escalated. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contacts alone are not an escalation path. Document when an unresolved issue moves on and to whom; name resource and process owners. ⟦A.f1 A.f2 A.f3 A:tb5⟧
[TABLE ds.ownership_escalation cols=['resource', 'resource_owner', 'associated_process', 'process_owner', 'initial_event_responder', 'unresolved_issue_condition', 'escalation_recipient'] ] caption: Sandbox orders service ownership and escalation
### r02 · Separate the two kinds of evidence
(definition) Operational events need response processes with identified owners and escalation paths. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Assign event-response responsibility and document when and to whom unresolved issues are escalated. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Identify a team responsible for each resource and process so operators know whom to engage. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contacts alone are not an escalation path. Document when an unresolved issue moves on and to whom; name resource and process owners. ⟦A.f1 A.f2 A.f3 A:tb5⟧
[TABLE ds.ownership_escalation cols=['resource', 'resource_owner', 'associated_process', 'process_owner', 'initial_event_responder', 'unresolved_issue_condition', 'escalation_recipient'] ] caption: Sandbox orders service ownership and escalation

=========

# EVALUATOR PACKET — Evaluate an IAM identity policy for a requested operation after external access-control preparation (aws_devops.tile.008)
Tile summary: Match action, resource and conditions to identity-policy statements. Applicable explicit deny overrides allow; no applicable allow means implicit deny.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.evaluate_an_iam_identity_policy_for_a_requested_operation — Evaluate an IAM identity policy for a requested operation after external access-control preparation

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.evaluate_an_iam_identity_policy_for_a_requested_operation)   objective: Evaluate an IAM identity policy
A.f1: An identity-based policy attaches to an identity and specifies permitted or denied actions on resources.   [sources: aws_iam_user_guide#reference_policies_elements.html]
A.f2: A statement uses Effect, Action and Resource, with optional Condition tests to scope when it applies.   [sources: aws_iam_user_guide#reference_policies_elements.html]
A.f3: For a request, compare action, resource and condition values with applicable statements; explicit deny overrides an allow, and absent an applicable allow the request is implicitly denied.   [sources: aws_iam_user_guide#reference_policies_evaluation-logic.html]
note: Do not introduce session policies, boundaries or organization policies before their allowed contexts.
PRACTICE ANCHOR (tool_simulation): Evaluate supplied identity-policy statements against sandbox object-read requests with named actions, resource targets and condition values. Identify applicable statements and classify each request as allowed, explicitly denied or implicitly denied.  SUCCESS: Each request has the correct outcome supported by action, resource and condition comparisons. The results include an applicable allow, an unsatisfied condition leaving no applicable allow, a resource mismatch leaving no applicable allow, and an applicable explicit deny overriding an allow.
ASSESSMENT ANCHOR: determine_request_outcome_under_supplied_identity_policy_conditions facts=['f1', 'f2', 'f3']

## DATA ASSETS USED
ds.identity_policy_evaluation: Object-read requests matched to identity-policy statements — columns: request_id(identifier), request_action(categorical), request_resource(identifier), request_approved(categorical), request_blocked(categorical), statement_id(identifier), Effect(categorical), Action(categorical), Resource(identifier), Condition(text), statement_applicable(categorical), identity_policy_result(categorical)
   ["request.allowed","s3:GetObject","arn:aws:s3:::sandbox-orders/order-a","yes","no","statement.allow","Allow","s3:GetObject","arn:aws:s3:::sandbox-orders/*","{\"StringEquals\":{\"aws:PrincipalTag/approved\":\"yes\"}}",true,"allow"]
   ["request.allowed","s3:GetObject","arn:aws:s3:::sandbox-orders/order-a","yes","no","statement.deny","Deny","s3:GetObject","arn:aws:s3:::sandbox-orders/*","{\"StringEquals\":{\"aws:PrincipalTag/blocked\":\"yes\"}}",false,"allow"]
   ["request.condition","s3:GetObject","arn:aws:s3:::sandbox-orders/order-a","no","no","statement.allow","Allow","s3:GetObject","arn:aws:s3:::sandbox-orders/*","{\"StringEquals\":{\"aws:PrincipalTag/approved\":\"yes\"}}",false,"implicit deny"]
   ["request.condition","s3:GetObject","arn:aws:s3:::sandbox-orders/order-a","no","no","statement.deny","Deny","s3:GetObject","arn:aws:s3:::sandbox-orders/*","{\"StringEquals\":{\"aws:PrincipalTag/blocked\":\"yes\"}}",false,"implicit deny"]
   ["request.resource","s3:GetObject","arn:aws:s3:::other-sandbox/order-a","yes","no","statement.allow","Allow","s3:GetObject","arn:aws:s3:::sandbox-orders/*","{\"StringEquals\":{\"aws:PrincipalTag/approved\":\"yes\"}}",false,"implicit deny"]
   ["request.resource","s3:GetObject","arn:aws:s3:::other-sandbox/order-a","yes","no","statement.deny","Deny","s3:GetObject","arn:aws:s3:::sandbox-orders/*","{\"StringEquals\":{\"aws:PrincipalTag/blocked\":\"yes\"}}",false,"implicit deny"]
   ["request.denied","s3:GetObject","arn:aws:s3:::sandbox-orders/order-a","yes","yes","statement.allow","Allow","s3:GetObject","arn:aws:s3:::sandbox-orders/*","{\"StringEquals\":{\"aws:PrincipalTag/approved\":\"yes\"}}",true,"explicit deny"]
   ["request.denied","s3:GetObject","arn:aws:s3:::sandbox-orders/order-a","yes","yes","statement.deny","Deny","s3:GetObject","arn:aws:s3:::sandbox-orders/*","{\"StringEquals\":{\"aws:PrincipalTag/blocked\":\"yes\"}}",true,"explicit deny"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute an AWS change using CloudTrail evidence; Attribute workload spend using resource tags; Centralize structured application logs in CloudWatch Logs; Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation; Choose rolling, blue/green or canary delivery for stated availability and rollback requirements; Cloudformation change sets; Collect host telemetry with the CloudWatch agent; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure role trust; directly require native IAM identity-policy evaluation; Configure secure human access with temporary credentials; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Evaluate resource-based permissions for a requested operation; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute a GitHub Actions workflow with an appropriate runner; Execute an established managed account-onboarding workflow; Extract structured AWS CL

## LESSON, in learner order

### s01 · explainer · Check the operating model
Learn — 
(intro) Evaluate the requested action and resource, not whether the policy looks permissive. Complete the external access-control preparation first. ⟦A:tb1⟧
(definition) An identity-based policy attaches to an identity and specifies permitted or denied actions on resources. ⟦A.f1 A:tb2⟧
(mechanism) A statement uses Effect, Action and Resource, with optional Condition tests to scope when it applies. ⟦A.f2 A:tb3⟧
(mechanism) For a request, compare action, resource and condition values with applicable statements; explicit deny overrides an allow, and absent an applicable allow the request is implicitly denied. ⟦A.f3 A:tb3⟧
[TABLE ds.identity_policy_evaluation cols=['request_id', 'request_action', 'request_resource', 'request_approved', 'request_blocked', 'statement_id', 'Effect', 'Action', 'Resource', 'Condition', 'statement_applicable', 'identity_policy_result'] ] caption: Object-read requests matched to identity-policy statements

### s02 · explainer · Read the sandbox case
Learn — 
(example) Compare the object-read request with Action, Resource and Condition. An unmet condition or unmatched resource can leave no applicable allow: implicit deny. When an applicable Deny also covers the request, it overrides the Allow. The supplied table evaluates these identity-policy rules, not every AWS policy type. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) An Allow elsewhere does not allow this request. Scope and conditions must match; applicable explicit deny wins. ⟦A.f2 A.f3 A:tb5⟧

### s03 · check · Choose the supported conclusion
Check — Read the supplied excerpts in this step and decide which conclusions are correct, defective or unsafe.

### s04 · hands_on · Review the supplied evidence
Review — Read the supplied excerpts in this step and decide which conclusions are correct, defective or unsafe.

### s05 · recap · Keep the distinctions
Recap — 
(takeaway) Match action, resource and conditions to identity-policy statements. Applicable explicit deny overrides allow; no applicable allow means implicit deny. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Execute a GitHub Actions workflow with an appropriate runner: Continue to aws_devops.tile.009.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the two kinds of evidence
(definition) An identity-based policy attaches to an identity and specifies permitted or denied actions on resources. ⟦A.f1 A:tb2 A:tb4⟧
(definition) A statement uses Effect, Action and Resource, with optional Condition tests to scope when it applies. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) For a request, compare action, resource and condition values with applicable statements; explicit deny overrides an allow, and absent an applicable allow the request is implicitly denied. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) An Allow elsewhere does not allow this request. Scope and conditions must match; applicable explicit deny wins. ⟦A.f2 A.f3 A:tb5⟧
[TABLE ds.identity_policy_evaluation cols=['request_id', 'request_action', 'request_resource', 'request_approved', 'request_blocked', 'statement_id', 'Effect', 'Action', 'Resource', 'Condition', 'statement_applicable', 'identity_policy_result'] ] caption: Object-read requests matched to identity-policy statements

=========

# EVALUATOR PACKET — Execute a GitHub Actions workflow with an appropriate runner (aws_devops.tile.009)
Tile summary: Read triggers, jobs, runner selection and uses/run steps in the workflow. Verify actual execution and success or failure with that run’s job and step logs.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.execute_a_github_actions_workflow_with_an_appropriate_runner — Execute a GitHub Actions workflow with an appropriate runner

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.execute_a_github_actions_workflow_with_an_appropriate_runner)   objective: Execute a GitHub Actions workflow
A.f1: Workflow YAML files are stored in .github/workflows; on defines the triggering events.   [sources: github_actions_docs#reference/workflows-and-actions/workflow-syntax]
A.f2: jobs defines jobs, runs-on selects the runner, and steps lists actions invoked with uses or commands executed with run.   [sources: github_actions_docs#reference/workflows-and-actions/workflow-syntax]
A.f3: Inspect a workflow run’s job and step logs to verify which steps ran and which succeeded or failed.   [sources: github_actions_docs#how-tos/monitor-workflows/use-workflow-run-logs]
note: Require external Git and pipeline-stage preparation; use supplied commands instead of introducing new shell syntax.
PRACTICE ANCHOR (tool_simulation): Run a supplied build-and-test workflow in a prepared repository. Locate its YAML, identify the triggering event, and select the supplied runner option that matches the stated job requirements through runs-on. Use the prepared event control to start the workflow, then inspect its job and step logs.  SUCCESS: One workflow execution is associated with the expected event and runner selection. The learner records which supplied build-and-test steps ran and which succeeded or failed, using logs from that same execution rather than inferring outcomes from YAML.
ASSESSMENT ANCHOR: verify_workflow_location_and_triggering_events facts=['f1']
ASSESSMENT ANCHOR: verify_job_runner_selection_and_step_definitions facts=['f2']
ASSESSMENT ANCHOR: verify_executed_steps_and_results_from_logs facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute an AWS change using CloudTrail evidence; Attribute workload spend using resource tags; Centralize structured application logs in CloudWatch Logs; Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation; Choose rolling, blue/green or canary delivery for stated availability and rollback requirements; Cloudformation change sets; Collect host telemetry with the CloudWatch agent; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure role trust; directly require native IAM identity-policy evaluation; Configure secure human access with temporary credentials; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Evaluate resource-based permissions for a requested operation; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute an established managed account-onboarding workflow; Extract structured AWS CLI inventory across paginated results; Hand over an actionable 

## LESSON, in learner order

### s01 · explainer · Check the operating model
Learn — 
(intro) Read when the workflow starts, where jobs run and what steps declare. Logs provide execution evidence. ⟦A:tb1⟧
(definition) Workflow YAML files are stored in .github/workflows; on defines the triggering events. ⟦A.f1 A:tb2⟧
(mechanism) jobs defines jobs, runs-on selects the runner, and steps lists actions invoked with uses or commands executed with run. ⟦A.f2 A:tb3⟧
(mechanism) Inspect a workflow run’s job and step logs to verify which steps ran and which succeeded or failed. ⟦A.f3 A:tb3⟧
[DIAGRAM: Workflow declaration versus illustrative execution evidence] nodes=['Authored read-only workflow example {Location: .github/workflows; on: workflow_dispatch; jobs: review; runs-on: ubuntu-latest; Step 1 — uses: actions/checkout@v4; Step 2 — run: echo review; Step 3 — run: exit 1}', 'Illustrative logs from the same execution {Event: workflow_dispatch; Job: review; Runner: ubuntu-latest; Step 1: executed, succeeded; Step 2: executed, succeeded; Step 3: executed, failed; Job: failed.}'] edges=[('n0', 'n1', 'The workflow declares the trigger, runner and steps. These illustrative same-run logs supply the executed-step statuses; declaration alone does not establish success.')] alt: Two labelled panes compare an authored read-only workflow with illustrative logs from the same execution. Authored read-only workflow example — Location: .github/workflows; on: workflow_dispatch; jobs: review; runs-on: ubuntu-latest; Step 1 — uses: actions/checkout@v4; Step 2 — run: echo review; Step 3 — run: exit 1. Illustrative logs from the same execution — Event: workflow_dispatch; Job: review; Runner: ubuntu-latest; Step 1: executed, succeeded; Step 2: executed, succeeded; Step 3: executed, failed; Job: failed.. The workflow declares the trigger, runner and steps. These illustrative same-run logs supply the executed-step statuses; declaration alone does not establish success.

### s02 · explainer · Read the sandbox case
Learn — 
(example) Follow the intended job and its selected runner, then distinguish uses actions from run commands. Inspect job and step logs from that same workflow execution. In this illustrative execution, the first two steps succeed and the third fails; declared steps alone would not establish those outcomes. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) YAML declares steps; logs establish execution and status. Runner selection alone does not prove success. ⟦A.f2 A.f3 A:tb5⟧

### s03 · video · Follow the evidence
[VIDEO ] bridge-before:  | bridge-after: 

### s04 · check · Choose the supported conclusion
Check — Read the supplied excerpts in this step and decide which conclusions are correct, defective or unsafe.

### s05 · hands_on · Review the supplied evidence
Review — Read the supplied excerpts in this step and decide which conclusions are correct, defective or unsafe.

### s06 · recap · Keep the distinctions
Recap — 
(takeaway) Read triggers, jobs, runner selection and uses/run steps in the workflow. Verify actual execution and success or failure with that run’s job and step logs. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Interpret DORA delivery and recovery evidence: Continue to aws_devops.tile.010.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the two kinds of evidence
(definition) Inspect a workflow run’s job and step logs to verify which steps ran and which succeeded or failed. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) YAML declares steps; logs establish execution and status. Runner selection alone does not prove success. ⟦A.f2 A.f3 A:tb5⟧
(example) Return to the same illustrative workflow: compare declared steps with that execution’s job and step logs. ⟦A.f1 A.f2 A.f3 A:tb4⟧
### r02 · Separate the two kinds of evidence
(definition) Workflow YAML files are stored in .github/workflows; on defines the triggering events. ⟦A.f1 A:tb2 A:tb4⟧
(definition) jobs defines jobs, runs-on selects the runner, and steps lists actions invoked with uses or commands executed with run. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Inspect a workflow run’s job and step logs to verify which steps ran and which succeeded or failed. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) YAML declares steps; logs establish execution and status. Runner selection alone does not prove success. ⟦A.f2 A.f3 A:tb5⟧
(example) Return to the same illustrative workflow: compare declared steps with that execution’s job and step logs. ⟦A.f1 A.f2 A.f3 A:tb4⟧

=========

# EVALUATOR PACKET — Interpret DORA delivery and recovery evidence (aws_devops.tile.010)
Tile summary: Compare deployment frequency and change lead time with change fail rate and failed deployment recovery time. Interpret all four over time within application context, not as individual rankings.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.interpret_dora_delivery_and_recovery_evidence — Interpret DORA delivery and recovery evidence

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.interpret_dora_delivery_and_recovery_evidence)   objective: Interpret DORA delivery and recovery evidence
A.f1: Deployment frequency measures how often changes are deployed; change lead time measures the elapsed time for a committed change to reach production.   [sources: dora_capabilities#../guides/dora-metrics/]
A.f2: Change fail rate measures the proportion of deployments requiring intervention; failed deployment recovery time measures how long recovery from a failed deployment takes.   [sources: dora_capabilities#../guides/dora-metrics/]
A.f3: Compare throughput and instability measures together over time and within application context rather than using one measure to rank individuals.   [sources: dora_capabilities#../guides/dora-metrics/]
note: Keep metric definitions and interpretation bounded; do not introduce unsupported performance benchmarks.
PRACTICE ANCHOR (field_selection): Interpret a supplied delivery dataset for the same application across two periods. Select the measures that support a throughput or stability concern and identify the supported concern.  SUCCESS: Correctly distinguishes deployment frequency and change lead time from change fail rate and failed deployment recovery time, selects evidence supporting the concern, and interprets it alongside the other measures without treating one metric as a complete performance score or ranking individuals.
ASSESSMENT ANCHOR: distinguish_deployment_frequency_from_change_lead_time facts=['f1']
ASSESSMENT ANCHOR: distinguish_change_fail_rate_from_failed_deployment_recovery_time facts=['f2']
ASSESSMENT ANCHOR: interpret_throughput_and_stability_together_in_application_context facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: recognize_limits_of_single_metric_performance_judgments facts=['f3']

## DATA ASSETS USED
ds.delivery_evidence: Orders delivery throughput and instability over two periods — columns: application(identifier), reporting_period(categorical), deployment_frequency(numerical), change_lead_time(numerical), change_fail_rate(numerical), failed_deployment_recovery_time(numerical)
   ["sandbox orders service","Period A",10,24,10,30]
   ["sandbox orders service","Period B",20,12,20,45]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute an AWS change using CloudTrail evidence; Attribute workload spend using resource tags; Centralize structured application logs in CloudWatch Logs; Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation; Choose rolling, blue/green or canary delivery for stated availability and rollback requirements; Cloudformation change sets; Collect host telemetry with the CloudWatch agent; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure role trust; directly require native IAM identity-policy evaluation; Configure secure human access with temporary credentials; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Evaluate resource-based permissions for a requested operation; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute an established managed account-onboarding workflow; Extract structured AWS CLI inventory across paginated results; Hand over an actionable 

## LESSON, in learner order

### s01 · explainer · Check the operating model
Learn — 
(intro) Read throughput and instability together before interpreting a delivery report. ⟦A:tb1⟧
(definition) Deployment frequency measures how often changes are deployed; change lead time measures the elapsed time for a committed change to reach production. ⟦A.f1 A:tb2⟧
(mechanism) Change fail rate measures the proportion of deployments requiring intervention; failed deployment recovery time measures how long recovery from a failed deployment takes. ⟦A.f2 A:tb3⟧
(mechanism) Compare throughput and instability measures together over time and within application context rather than using one measure to rank individuals. ⟦A.f3 A:tb3⟧
(example) For the same application, more deployments and shorter commit-to-production time concern throughput. A greater proportion needing intervention concerns change fail rate; recovery duration supplies the other instability measure. Keep all four measures together across reporting periods, rather than ranking individuals by one improving measure. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) Frequent delivery alone does not describe stability. Interpret the combined evidence within application context. ⟦A.f3 A:tb5⟧
[TABLE ds.delivery_evidence cols=['application', 'reporting_period', 'deployment_frequency', 'change_lead_time', 'change_fail_rate', 'failed_deployment_recovery_time'] ] caption: Orders delivery throughput and instability over two periods

### s02 · check · Choose the supported conclusion
Check — Read the supplied excerpts in this step and decide which conclusions are correct, defective or unsafe.

### s03 · hands_on · Review the supplied evidence
Review — Inspect the supplied table and select the entries that satisfy the stated requirement.

### s04 · recap · Keep the distinctions
Recap — 
(takeaway) Compare deployment frequency and change lead time with change fail rate and failed deployment recovery time. Interpret all four over time within application context, not as individual rankings. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Match operational events with EventBridge rules: Continue to aws_devops.tile.011.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the two kinds of evidence
(definition) Compare throughput and instability measures together over time and within application context rather than using one measure to rank individuals. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Frequent delivery alone does not describe stability. Interpret the combined evidence within application context. ⟦A.f3 A:tb5⟧
[TABLE ds.delivery_evidence cols=['application', 'reporting_period', 'deployment_frequency', 'change_lead_time', 'change_fail_rate', 'failed_deployment_recovery_time'] ] caption: Orders delivery throughput and instability over two periods
### r02 · Separate the two kinds of evidence
(definition) Deployment frequency measures how often changes are deployed; change lead time measures the elapsed time for a committed change to reach production. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Change fail rate measures the proportion of deployments requiring intervention; failed deployment recovery time measures how long recovery from a failed deployment takes. ⟦A.f2 A:tb3 A:tb4⟧
(definition) Compare throughput and instability measures together over time and within application context rather than using one measure to rank individuals. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Frequent delivery alone does not describe stability. Interpret the combined evidence within application context. ⟦A.f3 A:tb5⟧
[TABLE ds.delivery_evidence cols=['application', 'reporting_period', 'deployment_frequency', 'change_lead_time', 'change_fail_rate', 'failed_deployment_recovery_time'] ] caption: Orders delivery throughput and instability over two periods

=========

# EVALUATOR PACKET — Match operational events with EventBridge rules (aws_devops.tile.011)
Tile summary: Patterns constrain named fields to acceptable values. Omitted fields need not match. Test matching and nonmatching samples before using a pattern in a rule.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.match_operational_events_with_eventbridge_rules — Match operational events with EventBridge rules

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.match_operational_events_with_eventbridge_rules)   objective: Match events using EventBridge rules
A.f1: An EventBridge event pattern describes event fields and values that an event must match.   [sources: aws_eventbridge_user_guide#eb-event-patterns.html]
A.f2: Write a JSON object containing the fields to filter and arrays of acceptable values; fields omitted from the pattern are not required to match.   [sources: aws_eventbridge_user_guide#eb-event-patterns.html]
A.f3: Test a pattern against both matching and nonmatching sample events with the EventBridge sandbox or TestEventPattern before using it in a rule.   [sources: aws_eventbridge_user_guide#eb-event-pattern-sandbox.html]
note: Keep target authorization and delivery retries for their later concepts.
PRACTICE ANCHOR (live_code): Write one JSON event pattern accepting source lab.orders and detail-type OrderReady. Test supplied matching and nonmatching samples in the EventBridge sandbox before using the pattern in a rule.  SUCCESS: The pattern uses arrays of acceptable values under source and detail-type. A sample with lab.orders and OrderReady matches; a sample with lab.orders and OrderCancelled does not match. Both sandbox results agree with the intended selection.
ASSESSMENT ANCHOR: predict_event_pattern_matches facts=['f1', 'f2']
ASSESSMENT ANCHOR: recognize_omitted_fields_as_unconstrained facts=['f2']
ASSESSMENT ANCHOR: verify_matching_and_nonmatching_test_results facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute an AWS change using CloudTrail evidence; Attribute workload spend using resource tags; Centralize structured application logs in CloudWatch Logs; Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation; Choose rolling, blue/green or canary delivery for stated availability and rollback requirements; Cloudformation change sets; Collect host telemetry with the CloudWatch agent; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure role trust; directly require native IAM identity-policy evaluation; Configure secure human access with temporary credentials; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Evaluate resource-based permissions for a requested operation; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute an established managed account-onboarding workflow; Extract structured AWS CLI inventory across paginated results; Hand over an actionable 

## LESSON, in learner order

### s01 · explainer · Check the operating model
Learn — 
(intro) Specify the event fields to select, then test both sides of that selection boundary. ⟦A:tb1⟧
(definition) An EventBridge event pattern describes event fields and values that an event must match. ⟦A.f1 A:tb2⟧
(mechanism) Write a JSON object containing the fields to filter and arrays of acceptable values; fields omitted from the pattern are not required to match. ⟦A.f2 A:tb3⟧
(mechanism) Test a pattern against both matching and nonmatching sample events with the EventBridge sandbox or TestEventPattern before using it in a rule. ⟦A.f3 A:tb3⟧
[CODE javascript]
const pattern = {
  "source": [
    "lab.orders"
  ],
  "detail-type": [
    "OrderReady"
  ]
};
  annotations: ['Constrain source and detail-type to arrays of acceptable values.']
[CODE javascript]
const readyEvent = {
  "source": "lab.orders",
  "detail-type": "OrderReady",
  "id": "OrderReady"
};
  annotations: ['Positive sample: both constrained values satisfy the pattern. id is omitted from the pattern.']
[CODE javascript]
const cancelledEvent = {
  "source": "lab.orders",
  "detail-type": "OrderCancelled",
  "id": "OrderReady"
};
  annotations: ['Negative sample: detail-type differs from its acceptable value.']
[CODE javascript]
const changedIdEvent = {
  "source": "lab.orders",
  "detail-type": "OrderReady",
  "id": "OrderCancelled"
};
  annotations: ['Only id changes from the positive sample. Because id is omitted, the matching decision is unchanged.']

### s02 · explainer · Read the sandbox case
Learn — 
(example) The pattern accepts source lab.orders and detail-type OrderReady. Test those values, then test a sample with detail-type OrderCancelled. Also vary an omitted field: it is not required to match. Compare test results with the intended requirement before using a rule; these names are invented sample data. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) An event need not duplicate every field of a sample. Omitted fields are not required to match; positive and negative tests expose the boundary. ⟦A.f2 A.f3 A:tb5⟧

### s03 · check · Choose the supported conclusion
Check — Read the supplied excerpts in this step and decide which conclusions are correct, defective or unsafe.

### s04 · hands_on · Review the supplied evidence
Review — Read the supplied excerpts in this step and decide which conclusions are correct, defective or unsafe.

### s05 · recap · Keep the distinctions
Recap — 
(takeaway) Patterns constrain named fields to acceptable values. Omitted fields need not match. Test matching and nonmatching samples before using a pattern in a rule. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Operate an EC2 instance: Continue to aws_devops.tile.012.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the two kinds of evidence
(definition) Write a JSON object containing the fields to filter and arrays of acceptable values; fields omitted from the pattern are not required to match. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) An event need not duplicate every field of a sample. Omitted fields are not required to match; positive and negative tests expose the boundary. ⟦A.f2 A.f3 A:tb5⟧
(example) Return to the same lab.orders samples: contrast OrderReady with OrderCancelled while keeping the pattern fixed. ⟦A.f1 A.f2 A.f3 A:tb4⟧
### r02 · Separate the two kinds of evidence
(definition) An EventBridge event pattern describes event fields and values that an event must match. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Write a JSON object containing the fields to filter and arrays of acceptable values; fields omitted from the pattern are not required to match. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Test a pattern against both matching and nonmatching sample events with the EventBridge sandbox or TestEventPattern before using it in a rule. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) An event need not duplicate every field of a sample. Omitted fields are not required to match; positive and negative tests expose the boundary. ⟦A.f2 A.f3 A:tb5⟧
(example) Return to the same lab.orders samples: contrast OrderReady with OrderCancelled while keeping the pattern fixed. ⟦A.f1 A.f2 A.f3 A:tb4⟧