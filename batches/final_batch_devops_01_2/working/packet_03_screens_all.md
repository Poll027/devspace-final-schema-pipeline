# EVALUATOR PACKET — Inspect EC2 launch and health evidence (aws_devops.tile.012)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.operate_an_ec2_instance — Operate an EC2 instance after external cloud compute-lifecycle preparation

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.operate_an_ec2_instance)   objective: Operate an EC2 instance in AWS and inspect its supplied instance profile: an instance role is an IAM role whose temporary credentials provide the instance's AWS permissions; an instance profile is the container used to attach that role to EC2. Inspecting the supplied profile is not independently configuring role trust.
A.f1: Launching an EC2 instance requires choices such as AMI, instance type and network placement; an AMI supplies the initial software image.   [sources: aws_ec2_user_guide#ec2-launch-instance-wizard.html]
A.f2: In the launch workflow, use the approved AMI, subnet and supplied IAM instance profile, then inspect the created instance’s ID and settings.   [sources: aws_ec2_user_guide#ec2-launch-instance-wizard.html]
A.f3: An instance profile contains an IAM role and attaches it to EC2; applications on the instance can use that role’s temporary credentials.   [sources: aws_iam_user_guide#id_roles_use_switch-role-ec2_instance-profiles.html]
A.f4: Inspect instance state and status checks to distinguish lifecycle state from reported host or instance health.   [sources: aws_ec2_user_guide#monitoring-system-instance-status-check.html]
note: Require external compute preparation; defer detailed health diagnosis and Linux service configuration.
PRACTICE ANCHOR (tool_simulation): Launch one EC2 instance using the supplied approved AMI, instance type, network setup and IAM instance profile. Inspect the created instance's ID and settings, identify the IAM role attached through the supplied profile, and inspect lifecycle state and status checks without changing the supplied configuration.  SUCCESS: One instance is created with the approved launch choices. Its recorded ID, AMI, instance type, subnet and supplied instance profile match the created resource. The attached IAM role is correctly identified, and lifecycle state and status-check results are recorded separately rather than treating a running state as proof of health.
ASSESSMENT ANCHOR: verify_instance_identity_ami_type_and_network_placement facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_role_attached_through_supplied_instance_profile facts=['f2', 'f3']
ASSESSMENT ANCHOR: distinguish_lifecycle_state_from_status_check_health facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute an AWS change using CloudTrail evidence; Attribute workload spend using resource tags; Centralize structured application logs in CloudWatch Logs; Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation; Choose rolling, blue/green or canary delivery for stated availability and rollback requirements; Cloudformation change sets; Collect host telemetry with the CloudWatch agent; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure role trust; directly require native IAM identity-policy evaluation; Configure secure human access with temporary credentials; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Evaluate resource-based permissions for a requested operation; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute an established managed account-onboarding workflow; Extract structured AWS CLI inventory across paginated results; Hand over an actionable 

## LESSON, in learner order

### s01 · explainer · Connect choices to the instance
Inspect the model — 
(mechanism) Launch choices include AMI, instance type and network placement. The AMI supplies the initial software image. Use the approved AMI, subnet and supplied instance profile; inspect the created ID and settings. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3⟧
(mechanism) The profile attaches its IAM role; applications can use temporary role credentials. Read lifecycle state separately from reported host or instance health. ⟦A.f3 A.f4 A:tb3⟧
[DIAGRAM] nodes=['Approved choices {ami: ami-0a000000000000001; instance_type: t3.micro; subnet: subnet-0b000000000000001; instance_profile: orders-sandbox-instance-profile; attached_role: orders-sandbox-instance-role}', 'Created instance {instance_id: i-0c000000000000001; ami: ami-0a000000000000001; instance_type: t3.micro; subnet: subnet-0b000000000000001; instance_profile: orders-sandbox-instance-profile; attached_role: orders-sandbox-instance-role}', 'Lifecycle {lifecycle_state: running}', 'Status checks {system_status_check: ok; instance_status_check: impaired}'] edges=[('approved', 'created', 'Compare settings'), ('created', 'state', None), ('created', 'health', None)] alt: Approved selections and created EC2 details; lifecycle state and status checks are separate panels.

### s02 · explainer · Read identity and health separately
Inspect the model — 
(example) The observed instance i-0c000000000000001 matches the approved AMI ami-0a000000000000001, type t3.micro and subnet subnet-0b000000000000001. The AMI is its initial software image. The supplied profile orders-sandbox-instance-profile attaches orders-sandbox-instance-role; applications can use that role’s temporary credentials. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(example) Its lifecycle state is running, while the system check is ok and the instance check is impaired. Keep both kinds of evidence: running is not proof of health, and a completed launch does not replace status checks. The profile is a role container, not embedded application access keys. ⟦A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Distinguish state from health
Quick check — Read the supplied evidence and choose the interpretation that keeps lifecycle and health separate.

### s04 · hands_on · Review EC2 operating evidence
Evidence review — Read the supplied excerpts in this step and judge which interpretations correctly connect launch choices, instance identity, the attached role and health evidence.

### s05 · recap · Keep the operating evidence distinct
Takeaways — 
(takeaway) Use approved launch choices, inspect the created identity and settings, and identify the role through its profile. Applications can use temporary role credentials. Record lifecycle state and status checks separately. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Trace S3 object transfers: Next: identify an S3 object by bucket and key.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate lifecycle from health
(misconception) In the same EC2 evidence, state is running but the instance status check is impaired. State describes lifecycle; status checks report host or instance health. Retain both rather than treating running as proof of health. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
### r02 · Reconnect launch choices and observed details
(misconception) Launch choices include AMI, type and network placement; the AMI supplies the initial software image. Compare the created ID i-0c000000000000001 and settings with the approved AMI, subnet and supplied profile. The profile orders-sandbox-instance-profile attaches role orders-sandbox-instance-role; applications can use its temporary credentials. Contrast an approved request with observed instance evidence. Inspect state and status checks separately: running does not establish reported health. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Trace S3 object transfers (aws_devops.tile.013)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.operate_s3_object_storage — Operate S3 object storage for deployment artifacts after external cloud object-storage preparation

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.operate_s3_object_storage)   objective: Operate S3 storage for deployment artifacts
A.f1: An S3 object consists of data and metadata and is identified within a bucket by its object key.   [sources: aws_s3_user_guide#UsingObjects.html]
A.f2: Use aws s3 cp LOCAL_FILE s3://BUCKET/KEY --profile NAME --region REGION to upload, and reverse the source and destination to download.   [sources: aws_cli_user_guide#cli-services-s3-commands.html]
A.f3: A bucket is created in an AWS Region; verify the intended bucket location and caller access when storing or retrieving an object.   [sources: aws_s3_user_guide#UsingBucket.html]
note: Require external object-storage preparation; leave versioning and retention to later concepts.
PRACTICE ANCHOR (live_code): Upload orders-release.zip to releases/orders-release.zip in the supplied sandbox bucket, then retrieve that same object using an explicit operator profile and Region.  SUCCESS: The upload and download succeed for the intended bucket/key. Both commands specify the supplied profile and verified bucket Region, and the retrieved artifact matches the supplied file.
ASSESSMENT ANCHOR: identify_object_by_bucket_and_key facts=['f1']
ASSESSMENT ANCHOR: verify_upload_and_download_endpoints facts=['f2']
ASSESSMENT ANCHOR: verify_artifact_transfer_with_explicit_aws_context facts=['f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute an AWS change using CloudTrail evidence; Attribute workload spend using resource tags; Centralize structured application logs in CloudWatch Logs; Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation; Choose rolling, blue/green or canary delivery for stated availability and rollback requirements; Cloudformation change sets; Collect host telemetry with the CloudWatch agent; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure role trust; directly require native IAM identity-policy evaluation; Configure secure human access with temporary credentials; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Evaluate resource-based permissions for a requested operation; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute an established managed account-onboarding workflow; Extract structured AWS CLI inventory across paginated results; Hand over an actionable 

## LESSON, in learner order

### s01 · explainer · Trace both S3 transfer directions
Inspect the model — 
(mechanism) An S3 object contains data and metadata; its key identifies it within a bucket. Upload with aws s3 cp from local file to bucket/key; download reverses the endpoints. Keep profile and Region explicit. Buckets are created in an AWS Region; verify location and caller access. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3⟧
[CODE bash]
aws s3 cp orders-release.zip s3://orders-sandbox-artifacts-lab/releases/orders-release.zip --profile orders-sandbox-operator --region us-east-1
aws s3 cp s3://orders-sandbox-artifacts-lab/releases/orders-release.zip retrieved/orders-release.zip --profile orders-sandbox-operator --region us-east-1
  annotations: ['Upload: local → bucket/key; explicit profile and Region.', 'Download: same bucket/key → local; same explicit context.']

### s02 · explainer · Verify the intended object and context
Inspect the model — 
(example) The upload goes from orders-release.zip to s3://orders-sandbox-artifacts-lab/releases/orders-release.zip. The download reads that same bucket/key into retrieved/orders-release.zip. The key releases/orders-release.zip identifies the object within orders-sandbox-artifacts-lab; a familiar local filename or key alone does not establish the intended storage location. ⟦A.f1 A.f2 A:tb4 A:tb5⟧
(example) Both commands use profile orders-sandbox-operator and verified bucket Region us-east-1. The supplied access evidence says: Caller can upload and retrieve the intended bucket/key. After retrieval, the supplied comparison says: Retrieved artifact matches the supplied orders-release.zip file. A file arriving locally is not enough if its bucket/key differs from the intended object. Check endpoints, location and access rather than inferring them from the filename. ⟦A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · check · Check transfer context
Quick check — Read the supplied transfer evidence and choose the interpretation that verifies direction, bucket location and caller access.

### s04 · hands_on · Review S3 transfer excerpts
Evidence review — Read the supplied excerpts in this step and judge which transfers use the intended bucket/key and correct upload or download endpoints.

### s05 · recap · Identify the object, then trace the transfer
Takeaways — 
(takeaway) An object contains data and metadata; identify it by bucket and key. Upload points from local to S3; download reverses the endpoints. Use explicit profile and Region, and verify bucket location and caller access. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Publish and select workload metrics: Next: match a workload metric’s complete identity.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Keep direction and context together
(misconception) In the same transfer evidence, upload has local source orders-release.zip and S3 destination s3://orders-sandbox-artifacts-lab/releases/orders-release.zip; download reverses the direction into a local destination. Use aws s3 cp with explicit profile orders-sandbox-operator and Region us-east-1 in both directions. A bucket is created in a Region: verify its intended location and caller access, rather than assuming them from the filename. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Distinguish key from local filename
(misconception) An S3 object consists of data and metadata. In the same evidence, releases/orders-release.zip is the key within bucket orders-sandbox-artifacts-lab; orders-release.zip is the local upload source. Those are different roles. With aws s3 cp, upload goes local → S3 bucket/key and download goes from that same S3 bucket/key → local, keeping explicit profile and Region. A familiar local filename is not a substitute for verifying the intended bucket/key. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Publish and select workload metrics (aws_devops.tile.014)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = aws_devops.publish_workload_metrics_with_interpretable_dimensions — Publish workload metrics with interpretable dimensions

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (aws_devops.publish_workload_metrics_with_interpretable_dimensions)   objective: Publish metrics with interpretable dimensions
A.f1: A custom CloudWatch metric is identified by its namespace, name and dimension combination.   [sources: aws_cloudwatch_user_guide#publishingMetrics.html]
A.f2: Publish a metric with put-metric-data, specifying namespace, metric name, value and the intended dimensions.   [sources: aws_cloudwatch_user_guide#publishingMetrics.html#publishingDataPoints, aws_cli_user_guide#cli-usage-parameters.html]
A.f3: Each distinct dimension combination identifies a distinct metric; query the same combination that was published to select the intended series.   [sources: aws_cloudwatch_user_guide#cloudwatch_concepts.html#Dimension]
note: Do not introduce dimension-cost claims or alarm thresholds not present in the brief.
PRACTICE ANCHOR (tool_simulation): Emit the supplied QueueDepth value in namespace Lab/Orders using put-metric-data with exactly the supplied dimensions Environment=sandbox and Service=orders.  SUCCESS: The publication specifies Lab/Orders, QueueDepth, the supplied value and both intended dimensions without adding dimension combinations. The exercise record associates the observed value with that complete metric identity.
ASSESSMENT ANCHOR: verify_query_matches_published_workload_series facts=['f1', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute an AWS change using CloudTrail evidence; Attribute workload spend using resource tags; Centralize structured application logs in CloudWatch Logs; Change and validate a Linux service configuration after external filesystem, permissions and process/service preparation; Choose rolling, blue/green or canary delivery for stated availability and rollback requirements; Cloudformation change sets; Collect host telemetry with the CloudWatch agent; Configure CloudWatch alarm evaluation and missing-data behavior from supplied signals and thresholds; Configure role trust; directly require native IAM identity-policy evaluation; Configure secure human access with temporary credentials; Configure security groups after external ports/firewall preparation; Define an EC2 instance with Terraform HCL and a pinned provider; directly require the native EC2 instance foundation; Evaluate resource-based permissions for a requested operation; Execute Python AWS automation in an isolated dependency environment after active registry language preparation; Execute an established managed account-onboarding workflow; Extract structured AWS CLI inventory across paginated results; Hand over an actionable 

## LESSON, in learner order

### s01 · explainer · Match a metric’s full identity
Inspect the model — 
(mechanism) A custom CloudWatch metric’s identity is namespace, name and dimension combination. Publish with put-metric-data, supplying namespace, name, value and intended dimensions. Distinct combinations identify distinct metrics; query the published combination to select the intended series. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3⟧
[SIDE_BY_SIDE] Match the complete identity. left_label: Published | right_label: Queried
  left:
[DIAGRAM] nodes=['Lab/Orders | QueueDepth | Environment=sandbox, Service=orders', 'Lab/Orders | QueueDepth | Environment=staging, Service=orders'] edges=[] alt: Two published metric identities.
  right:
[DIAGRAM] nodes=['Lab/Orders | QueueDepth | Environment=sandbox, Service=orders', 'Lab/Orders | QueueDepth | Environment=staging, Service=orders', 'Lab/Orders | QueueDepth | Environment=sandbox'] edges=[] alt: Two complete queries and one query omitting Service.

### s02 · explainer · Compare combinations, not names
Inspect the model — 
(example) The sandbox publication is Lab/Orders | QueueDepth | Environment=sandbox, Service=orders, with supplied value 7. Publish using put-metric-data with that namespace, name, value and both dimensions. The staging publication is Lab/Orders | QueueDepth | Environment=staging, Service=orders, with supplied value 3. It is a distinct metric despite sharing the name. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(example) The complete sandbox query selects Lab/Orders | QueueDepth | Environment=sandbox, Service=orders. A query omitting Service uses Lab/Orders | QueueDepth | Environment=sandbox: that is not the published sandbox orders combination. Compare the full published and queried identities, not only the metric name. These query records describe selections, not returned values; do not describe a staging series as the sandbox orders value. ⟦A.f1 A.f3 A:tb4 A:tb5⟧

### s03 · check · Check the selected series
Quick check — Read the supplied identities and choose the query interpretation that matches the full published combination.

### s04 · hands_on · Review metric publication excerpts
Evidence review — Read the supplied excerpts in this step and judge which publications specify the supplied namespace, metric name, value and intended dimensions.

### s05 · recap · Preserve complete metric identity
Takeaways — 
(takeaway) Publish namespace, name, supplied value and intended dimensions with put-metric-data. A custom metric’s identity includes the complete dimension combination; query that same combination, not just a familiar name. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: aws_devops.tile.015: Continue to aws_devops.tile.015.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast complete and incomplete identities
(misconception) A custom metric is identified by namespace, name and dimension combination. In the same evidence, Lab/Orders | QueueDepth | Environment=sandbox, Service=orders and Lab/Orders | QueueDepth | Environment=staging, Service=orders are distinct metrics. Query the complete published combination. Keeping Environment=sandbox but omitting Service=orders does not select the stated sandbox orders identity; matching the name alone is insufficient. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Keep publication inputs together
(misconception) Use put-metric-data to publish the supplied namespace Lab/Orders, metric name QueueDepth, value 7 and dimensions Environment=sandbox, Service=orders. Contrast a complete publication with one missing an intended dimension. Namespace, name and the complete combination identify the metric; a different combination is a distinct metric. Query the same combination that was published. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4⟧