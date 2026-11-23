import json, re, copy
from pathlib import Path
B=Path(__file__).parent
P=json.loads((B/'tile_plans.json').read_text()); G=json.loads((B/'inputs/path_glossary_bundle.json').read_text()); A=json.loads((B/'scenario_asset_registry.json').read_text())
C={c['context']['concept_id']:c for c in G['bundles']}; assets={a['asset_id']:a for a in A['assets']}
policies={a['asset_id'].removeprefix('ws.'):json.loads(next(f['content'] for f in a['files'] if f['path']=='policy.json')) for a in A['assets'] if a['asset_kind']=='code_workspace'}
# Each entry revoices one frozen teaching block. Numerical fixture values are interpolated from policies, never copied as answers.
TEXT={
'distribution_monitoring':[
'Choose the reference and production window before summarizing. Keep representations comparable.',
'Compare captured inputs using the reference constraints and the same feature representations. np.histogram(values, bins=fixed_edges) counts numerical bins; divide by each window’s eligible count. Count every declared category and predicted class, divide by that window’s total, and retain definitions and totals.',
'Record the production window, reference identity and summaries. np.mean(numeric_values) gives the selected observations’ arithmetic mean. np.std(numeric_values, ddof=0) takes the square root after dividing squared deviations by N; use ddof=1 only when the calculation requires N−1.',
'Compare the registered reference and production fixtures on their shared definitions. Retain absent categories as zero entries, and use each window’s own total—even for the larger production fixture. Fixed edges and eligible numerical counts keep bin proportions comparable. Record np.mean and np.std with the declared divisor alongside window and reference identity. These summaries support investigating a distribution change; they do not claim increased labeled error.',
'Changing bins, category mappings or denominators changes the comparison. Keep representations aligned and use each window’s own eligible total, not raw counts alone.'
],
'drift_degradation_distinction':[
'An input change and a quality change answer different questions. Identify which evidence you actually have.',
'Input drift changes the observed input distribution relative to its reference; input monitoring alone does not measure labeled quality. Concept drift changes P(Y|X), the feature–label relationship, so a previously useful model can become less useful. Observed quality degradation requires corresponding ground-truth labels and the declared quality reference.',
'Without matched available labels, report supported distribution or service evidence and leave labeled quality unresolved. P(X), P(Y|X) and matched-label errors describe different evidence; a change in one does not establish the others.',
'More long-distance orders supports an input-distribution statement about P(X), not a changed conditional target relationship P(Y|X). Matched predictions and ground truth compared with the quality reference can support observed degradation. Without matched labels, retain the distribution or service observation and the unresolved quality question: absence of labels proves neither constant quality nor worsening quality. Conditional-target evidence asks a separate question. A change in any one of these evidence categories does not logically establish changes in the other two.',
'Input drift is not labeled degradation. P(X), P(Y|X) and matched-label errors do not establish changes in one another.'
],
'data_drift_detection':[
'Fix the comparison window and criterion first. Do not choose a threshold after seeing the change.',
'Define the reference distribution, window and drift criterion before checking production. Align bin edges and category mappings; normalize each window by its own eligible total. Apply the supplied significance or threshold rule to reference/current distributions or statistics and report feature-level crossings.',
'A crossing identifies a distribution difference under that rule, not measured target-error growth. Use np.mean(numeric_values) for the arithmetic mean. np.std(numeric_values, ddof=0) divides squared deviations by N before taking the square root; ddof=1 is only for a required N−1 divisor.',
'For every aligned category, divide reference and current counts by their own window totals. Apply the supplied probability-distance equation and threshold to those vectors.',
'The registered fixtures share category definitions and fixed numerical edges. Normalize each window independently, then apply the supplied distance equation and criterion to category and numerical-bin vectors. Keep numerical means and standard deviations with their stated divisor separate from the distance verdict. Record reference identity, window, resolved comparison inputs and which features cross the rule. A distribution crossing does not by itself measure increased prediction error; matched-label quality remains a separate question.',
'A threshold crossing is not increased prediction error. Different mappings or reused reference denominators would change the comparison itself.'
],
'delayed_label_quality':[
'Preserve the prediction cohort before labels arrive. Missing ground truth is not a successful prediction.',
'Build a prediction-ID dictionary retaining cohort membership and prediction time. Attach only matching labels within the availability boundary, explicitly handling duplicate IDs and unmatched labels. Define the cohort and analysis delay so recent incomplete ground truth is not treated as mature.',
'Label maturity coverage is mature eligible IDs divided by all eligible cohort IDs; retain that denominator. Compute the declared quality quantity on matched mature predictions and report coverage. Without justified coverage, it does not estimate all-traffic quality. Use np.mean(numeric_values) on the selected numerical observations.',
'np.std(numeric_values, ddof=0) divides squared deviations by N, then takes the square root. Use ddof=1 only if the stated calculation requires N−1.',
'Keep the fixed cohort intact while labels arrive. Reject duplicates before dictionaries can overwrite them; record unmatched and unavailable labels under the supplied policy. Coverage divides mature eligible IDs by all eligible cohort IDs. Error proportion instead divides matched mature errors by matched mature predictions. Compute the specified loss mean and standard deviation on those selected observations, retaining the divisor. Report both quality and coverage rather than counting missing labels as correct predictions. The mature subset does not represent all traffic without justified coverage.',
'An absent label is not a correct prediction. Maturity and quality have different denominators; the mature subset does not automatically represent all traffic.'
],
'actionable_ml_alerts':[
'An actionable alert needs a window rule, an owner and a response—not just a changing number.',
'Use the baseline window and indicator definition to characterize normal variability. Write the existing indicator, threshold/window rule, owner and response into its YAML schema and inspect parsed fields. Apply the declared noise-tolerant rule to baseline mean/spread rather than every fluctuation.',
'Replay normal and breached windows: only a qualifying breach should emit the configured owner/action record. np.mean(numeric_values) gives the selected mean; np.std(numeric_values, ddof=0) divides squared deviations by N before taking the square root. Use ddof=1 only for a required N−1 divisor.',
'Use assert predicates for valid, boundary and failure cases; false predicates raise AssertionError in ordinary non-optimized execution. With PyYAML, import yaml, write mappings/lists with yaml.safe_dump(config, file_handle), reload with yaml.safe_load(file_handle), and inspect resolved fields. Safe loading accepts standard YAML tags, not arbitrary Python object constructors.',
'Compute the baseline mean and spread with the stated divisor. Write the supplied indicator, window rule, owner and response, then safely reload and inspect the YAML. Replay normal, boundary and breach fixtures with assertion checks. Keep both the predicate outcome and owner/action evidence: correct fields alone do not prove behavior. The rule decides whether evidence qualifies; ownership and response define what happens afterward. This implements the supplied policy, not a newly invented significance test.',
'A small indicator change need not be actionable. Verify the stated window/noise rule and its intended owner/action outcome.'
],
'production_regression_diagnosis':[
'Worsening after a release establishes timing, not cause. Start with impact and available evidence.',
'Triage client-visible impact using timeline, deployment, data, service and quality evidence. A schema/value failure identifies data conditions to investigate; a distribution difference alone does not prove labeled degradation. Compare active artifact/configuration identities with the approved deployment and run record.',
'Check matched mature labels before selecting a quality-degradation response. Calculate release/cohort error rates using each matched eligible-label denominator separately. Choose only the supplied policy-supported data repair, approved rollback or gated retraining, preserving required validation.',
'Reproduce and isolate the regression from the release/telemetry timeline. Test one causal hypothesis against the evidence, then choose only its supported response.',
'Compare active and approved artifact/configuration identities. Investigate schema failures as data conditions, and keep distribution evidence distinct from measured quality. Calculate each release/cohort’s error rate on its own matched eligible mature labels; incomplete labels are not successful predictions. Reproduce the bounded regression, isolate it from the timeline, and test a hypothesis that distinguishes alternatives. Select only the existing policy-supported repair, rollback or retraining response. Preserve authorization, corresponding validation gates and audit evidence rather than treating release correlation as causation.',
'Release timing is not causal diagnosis. Distribution evidence alone is not labeled degradation; the supported response must preserve existing gates.'
],
'retraining_trigger_policy':[
'Record why retraining is eligible and what data it intends to use. Eligibility does not approve a candidate.',
'Pipeline execution can be triggered by a schedule, new training data, observed performance degradation or significant distribution change. Select the trigger supported by supplied evidence and retain its reason and intended dataset. Label-verified performance evidence differs from a distribution-only signal; do not call drift measured prediction error.',
'A trigger starts a gated pipeline, not deployment approval. Reject unauthorized identities and uninvestigated alarms at entry. Annotate existing quality/test, training and evaluation stages with purposes and input artifacts. Promotion depends on separate authorization, not merely completed retraining.',
'Trace an eligible event through entry and required dependencies, then a failed check to identify blocked downstream stages. Keep handoff credentials runtime-injected and out of policy, YAML and captured logs.',
'For an investigated distribution signal, record distribution evidence—not labeled error—and bind its intended dataset and authorized identity. Trace entry, quality/test, training and evaluation dependencies with artifact identities and purposes. Replay unauthorized and uninvestigated entry rejection, then a failed data check to show where execution stops. Promotion still requires its own approval. Keep trigger reason, input identity and dependency outcomes in the record, without exposing runtime credentials in policy, YAML or logs.',
'Eligibility is not deployment approval. An alarm is not automatically authorized, and distribution-only evidence is not measured prediction degradation.'
],
'authorized_retraining_execution':[
'A permitted trigger needs verified input identity. Inspect what the pipeline consumes, not just what was requested.',
'Check permission to execute the pipeline and access its input resources. Resolve and verify the recorded object generation instead of a mutable dataset name. Use import boto3 and boto3.client("sagemaker").start_pipeline_execution with PipelineName, PipelineParameters containing Name/Value pairs, and ClientRequestToken from the supplied contract.',
'Retain the returned PipelineExecutionArn and actual parameters. Bind execution identity, trigger authorization and dataset version in one audit record. Existing Cloud Build steps declare execution images in name and commands in args or script; wire the function/test entry into its assigned stage.',
'Give steps IDs and required predecessor IDs in waitFor; text order alone is not a dependency. Keep gates fatal: no allowFailure or failing gate codes in allowExitCodes, and rejected Python gates must exit unsuccessfully. Use configured Pub/Sub bindings and filters, then inspect accepted/rejected stage results and resolved inputs.',
'Bind approved versions through availableSecrets.secretManager and expose them only to needed steps with secretEnv. YAML stores references, not values. Use the authorized build/step identity; promotion needs separate authorization. Check captured output for secret disclosure; never echo or serialize credentials.',
'Compare actual consumed stage inputs with the approved immutable snapshot; a start request is not consumption proof. With PyYAML, import yaml, write mappings/lists using yaml.safe_dump(config, file_handle), reload using yaml.safe_load(file_handle), and inspect resolved fields. Safe loading permits standard tags, not arbitrary Python constructors.',
'Verify approved generation and bytes before the supplied boto3 invocation. Retain returned ARN, actual parameters, trigger authorization and input version together. Wire event-bound build steps with named images, commands, explicit waitFor dependencies and fatal gates. Use approved identity and runtime Secret Manager references only for needed steps. Replay accepted and rejected fixtures; inspect consumed input identity and credential-safe output. Safely round-trip and inspect configuration before submission. Retraining execution still does not authorize promotion.',
'A start request proves neither consumed input identity nor promotion approval. Inspect actual stage inputs and keep secrets out of records and logs.'
],
'retraining_run_idempotency':[
'Concurrent workers and restarted workers must preserve one durable logical job identity while preventing different-key overlap.',
'Read run key and pipeline from the event dictionary. The supplied atomic admission operation reserves both unique key and active slot and persists job ID. Local dictionaries and separate check-then-write calls cannot provide that durable contract. Branch explicitly on accepted, duplicate and busy; only acceptance authorizes a new logical launch.',
'Launch accepted work with the persisted job ID as idempotency token. Duplicates and restarted claims resume or attach to that identity. Reconcile unknown launch responses with the same token, not a replacement. If another key holds the slot, defer or reject under policy without launching overlap.',
'Release the slot only after confirmed terminal state, retaining the completed key against later duplicate launch. Assert durable state and logical job counts for same-event concurrency, different-key contention and fresh workers after reservation and launch. Existing Cloud Build steps need images in name and commands in args or script for the assigned function/test stage.',
'Use step IDs and waitFor predecessor IDs; textual ordering is insufficient. Gates remain fatal: no allowFailure or permitted failing gate exit codes, and rejected Python gates exit unsuccessfully. Replay configured Pub/Sub payload bindings and filters, inspecting accepted/rejected stage results and resolved inputs.',
'With PyYAML, import yaml, write mapping/list configuration via yaml.safe_dump(config, file_handle), reload via yaml.safe_load(file_handle), and inspect required fields before submission. Safe loading accepts standard tags, not arbitrary Python object constructors.',
'Pass the event key and pipeline to atomic durable admission. Acceptance launches with the persisted job token; duplicates and restarts attach to it. Unknown responses reconcile the same token. Busy different-key work follows the defer/reject policy without overlap. Confirm terminal state before releasing the slot and retain completed keys. Assert durable state and logical counts across concurrent and restarted workers. Wire named build images/commands, explicit fatal dependencies and configured event bindings; safely reload configuration and inspect resolved replay inputs.',
'Local check-then-write is not durable atomic admission. A retry cannot invent a new job identity; release before terminal confirmation permits overlap.'
],
'retrained_candidate_validation':[
'Compare exact candidate and incumbent identities on one declared cohort. Aggregate improvement alone is not acceptance.',
'Use the same validation cohort and predeclared requirements for candidate and incumbent. Calculate expected cost using supplied deployment class probabilities and error costs. A required quality, slice or compatibility failure rejects the candidate even when an aggregate score improves.',
'Bind exact registry/artifact identity and verdict to controlled promotion; another artifact is not approved. FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) on actual positives. Empty conditioning groups yield undefined rates. With zero cost for correct predictions, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.',
'Never use protected test observations to fit preprocessing, select a model or tune settings: that leaks information into the chosen system. Assert valid, boundary and failure predicates; a false predicate raises AssertionError in ordinary non-optimized execution.',
'Keep candidate and incumbent on the same fixed validation cohort. Compute actual-class conditional rates and expected costs using supplied probabilities and costs; empty conditioning groups are undefined. Record quality, required-slice and compatibility gates separately. Lower cost cannot erase a failed required gate. Keep protected tests out of fitting and selection. Assert accepted, boundary and rejected verdicts with exact identity binding. Evidence for one registry artifact never approves a different artifact merely because both came from retraining.',
'Retrained is not accepted. Aggregate gain cannot bypass required gates, and one artifact’s validation cannot approve another.'
],
'ml_incident_runbook':[
'The runbook scopes recovery to one authorized instance. Reproduce the fault and test the supported hypothesis first.',
'Use the nonproduction runbook and approved identity. Reproduce and isolate the injected fault; test one recovery hypothesis before action. Record instance identity/status and process/service fault evidence. Run the approved gcloud compute instances stop INSTANCE --zone=ZONE, wait for completion, then start that same instance and wait until running.',
'Reconnect with gcloud compute ssh INSTANCE --zone=ZONE and inspect restored process/model service state. Check readiness and a bounded prediction exchange against the expected contract. Keep existing runtime-injected credentials out of code, configuration and captured output.',
'Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect identity and status before and after the authorized lifecycle action.',
'Record the authorized instance identity, lifecycle state and failed process/service evidence before recovery changes the symptom. Reproduce the fault and test the runbook’s supported hypothesis. Under the approved identity, stop and wait, start the same instance and wait until running, then reconnect. Inspect the restored service and verify readiness plus bounded prediction behavior against its contract. Preserve before/after descriptions and credential-safe output. Running VM state alone does not prove service recovery, and this runbook does not authorize restarting unrelated resources.',
'A restarted VM does not prove service recovery. Keep authorized identity, fault evidence and readiness/prediction checks in the recovery verdict.'
],
'ml_resource_utilization':[
'Choose the actual workload interval. Stopped samples and unrelated processes do not describe its active utilization.',
'Summarize CPU/memory for the defined workload window, retaining instance and process identity. Align samples with start/stop states rather than silently mixing stopped or unrelated intervals. Resolve process-state evidence against the running workload; docker top shows containerized running processes for comparison.',
'Summarize CPU and memory over the same matched interval with counts and units. np.mean(numeric_values) gives the arithmetic mean. np.std(numeric_values, ddof=0) divides squared deviations by N before the square root; use ddof=1 only for a required N−1 divisor.',
'Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect status and identity before and after the authorized lifecycle action.',
'Inspect registered telemetry for the selected instance, process and active interval. Keep CPU percent separate from memory units, and retain both series’ counts. Compute their means and standard deviations using the stated divisor. Compare running process evidence with docker top and lifecycle identity/status. Do not append stopped or unrelated samples to lower the average. These bounded descriptive summaries characterize resource usage; they do not independently establish billed cost, request success or model quality.',
'A low average needs its window and workload identity. Do not silently combine stopped or unrelated intervals with active utilization.'
],
'ml_workload_cost_attribution':[
'Workload expenditure includes attributable direct and shared charges—not just active VM compute time.',
'Select the declared training/inference workload and reporting window from billing resource/service/time records. Connect resources to workloads through existing labels or mapping. Stopping a VM can end compute charges while disks and other resources remain billable, so duration alone is incomplete expenditure.',
'Aggregate charges by workload/category and reconcile against eligible records. Declared unit cost divides attributed expenditure by corresponding completed work; retain billing and work windows. Start and connect to both tagged instances for bounded training/inference execution, record separate lifecycle windows, then stop both.',
'Allocate direct rows to matched workload/lifecycle intervals and shared rows using the explicit rule. Retain shared amounts, flag large or unmatched allocations, and reconcile allocated plus explicitly unallocated amounts to eligible billing totals. gcloud compute instances start/stop INSTANCE --zone=ZONE changes authorized VM state; wait and inspect the result.',
'Connect to the running authorized VM with gcloud compute ssh INSTANCE --zone=ZONE for execution. Inspect identity/status before and after lifecycle actions using gcloud compute instances describe INSTANCE --zone=ZONE. Use np.mean(numeric_values) for the selected arithmetic mean.',
'np.std(numeric_values, ddof=0) divides squared deviations by N before taking the square root. Use ddof=1 only when the stated calculation requires N−1.',
'The registered billing and lifecycle fixtures distinguish training from inference and preserve disk charges after compute stops. Apply the supplied direct mapping and shared rule; flag unmatched or unusually large allocations. Reconcile allocated plus explicitly unallocated credits by reporting window. Unit cost uses corresponding completed work and retains both windows. For bounded execution, start/connect each tagged test instance, then stop, wait and inspect both. Keep the lifecycle records separate from the full billing window.',
'Compute duration is not all expenditure. Shared charges stay in reconciliation; unit cost needs matching completed work and measurement windows.'
],
'ml_workload_cost_guardrail':[
'Notification and resource action are separate. A tested budget response is not a hard spending cap.',
'Configure the supplied workload budget amount, period and threshold rules in the existing platform. Connect the existing Pub/Sub topic and authorized notification path, then test receipt. Verify the separately authorized response; notification alone does not stop consumption.',
'Notifications can lag usage, so record that spending may exceed the budget. Test below-threshold and breach fixtures for notification and permitted response. The event-response YAML safe-stop command must target only the explicitly approved nonproduction instance, not an unrestricted selector.',
'Bind the existing budget event to the response pipeline and parse its YAML. Verify scope, threshold and fixed instance before applying. Simulate breach, inspect notification/response execution and confirm gcloud compute instances stop INSTANCE --zone=ZONE affected only the approved target. Use approved identity and runtime Secret Manager references/secretEnv; check logs for literal credentials.',
'Inspect before/after identity/status with gcloud compute instances describe INSTANCE --zone=ZONE. With PyYAML, import yaml, safe_dump(config, file_handle), safe_load(file_handle), and inspect resolved mapping/list fields before submission. Safe loading accepts standard tags, not arbitrary Python object constructors.',
'Write the supplied scope, period and threshold; bind the existing notification topic to its permitted pipeline. Safely reload and inspect the fixed safe-stop target before approved application. Replay below-threshold and breach fixtures, inspecting notification receipt, authorized response execution and before/after instance descriptions. Confirm only the approved target stopped. Resolve Secret Manager references at runtime, expose only needed secretEnv, and check logs for disclosure. Retain the limitation: notification lag prevents a hard-cap guarantee.',
'An alert does not stop consumption by itself. A tested response still cannot guarantee spending stays below budget or authorize broader targets.'
],
'serving_resource_cleanup':[
'Cleanup requires verified retirement and ownership. Age alone does not authorize destructive action.',
'Authorize against the retired inventory and permitted identity while preserving the active release. Compare actual ownership and release/version labels with approved active/retired inventory. Inspect container identity, State.Running/exit state, logs and compute lifecycle before declaring exclusive retirement.',
'Review commands/logs for secrets or sensitive data; runtime credentials stay out of code and output. Stop only a verified retired container with docker container stop NAME, then remove it stopped with docker container rm NAME. Delete only the verified exclusively retired nonproduction instance using gcloud compute instances delete INSTANCE --zone=ZONE under approved disk preservation.',
'Preserve active image references and required model/preprocessing artifacts; container removal does not authorize shared-artifact deletion. Check active readiness and bounded prediction, then confirm approved retired resources are absent. Record ownership, active/retired identities, authorized actions, retained artifacts and credential non-disclosure in one audit.',
'Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect identity/status before and after the authorized lifecycle action.',
'Reconcile actual labels, identity, running/exit state, logs and lifecycle against approved inventory. Stop/remove only verified retired containers; delete only the exclusively retired test VM under the disk-preservation rule. Keep active images and required model/preprocessing artifacts, including shared references. Verify active readiness and bounded prediction, and confirm approved retired-resource absence. Retain before/after instance inspection and one audit of ownership, authorized actions, artifacts and credential-safe output. Runtime secrets remain outside cleanup code and logs.',
'Retired-container removal does not authorize shared-artifact deletion. Verified ownership, permitted scope and lifecycle govern cleanup while the active release stays preserved.'
]
}

def lin(cids,tbs=(),facts=(),anchors=()): return {'concept_ids':list(cids),'teaching_block_ids':list(tbs),'fact_ids':list(facts),'anchors':list(anchors)}
def prose(text,lineage,role='definition'): return {'type':'prose','text':text,'role':role,'lineage':copy.deepcopy(lineage)}
def table(aid,L,caption=''):
 return {'type':'data_table','asset_ref':{'asset_id':aid,'columns':[c['name'] for c in assets[aid]['columns']]},'caption':caption or assets[aid]['title'],'lineage':copy.deepcopy(L)}
def query(sql,mounts,L,caption):
 return {'type':'data_table','result_of':{'runtime':'sql','sql':sql,'asset_mounts':[{'asset_id':a,'mount_path':m} for a,m in mounts]},'caption':caption,'lineage':copy.deepcopy(L)}
def diagram(title,labels,L):
 return {'type':'diagram','diagram_kind':'mapping','title':title,'nodes':[{'id':f'n{i+1}','label':v[0],'fields':v[1:]} for i,v in enumerate(labels)],'edges':[],'alt_text':title+'. '+'. '.join('; '.join(v) for v in labels),'lineage':copy.deepcopy(L)}
def flow(title,labels,L):
 return {'type':'process_flow','title':title,'direction':'LR','nodes':[{'id':f'n{i+1}','label':v,'kind':'step'} for i,v in enumerate(labels)],'edges':[{'from':f'n{i+1}','to':f'n{i+2}'} for i in range(len(labels)-1)],'alt_text':' → '.join(labels),'lineage':copy.deepcopy(L)}
def code(text,L): return {'type':'code_walkthrough','language':'python','code':text,'lineage':copy.deepcopy(L)}

# Query inputs (not results) carry data-derived registry policy literals.
def distribution_summary(L):
 p=policies['distribution_monitoring'];lo,mid,hi=p['fixed_edges'];cats=p['declared_categories'];classes=p['declared_classes'];w=p['production_window'];
 windows=f"SELECT '{p['reference_id']}' AS window_id, '{p['reference_id']}' AS reference_id, NULL AS window_start, NULL AS window_end, numeric_values, category, predicted_class FROM reference UNION ALL SELECT 'production','{p['reference_id']}','{w['start']}','{w['end']}',numeric_values,category,predicted_class FROM production"
 catdefs=' UNION ALL '.join(f"SELECT '{v}' AS definition" for v in cats);clsdefs=' UNION ALL '.join(f"SELECT '{v}' AS definition" for v in classes)
 sql=f'''WITH observations AS ({windows}), windows AS (SELECT DISTINCT window_id,reference_id,window_start,window_end FROM observations), categories AS ({catdefs}), classes AS ({clsdefs}), means AS (SELECT window_id,AVG(numeric_values) AS mean FROM observations WHERE numeric_values BETWEEN {lo} AND {hi} GROUP BY window_id)
SELECT w.*, 'category' AS summary_kind,c.definition,COUNT(o.category) AS count,(SELECT COUNT(*) FROM observations x WHERE x.window_id=w.window_id) AS eligible_total,1.0*COUNT(o.category)/(SELECT COUNT(*) FROM observations x WHERE x.window_id=w.window_id) AS proportion,NULL AS mean,NULL AS standard_deviation,NULL AS ddof FROM windows w CROSS JOIN categories c LEFT JOIN observations o ON o.window_id=w.window_id AND o.category=c.definition GROUP BY w.window_id,w.reference_id,w.window_start,w.window_end,c.definition
UNION ALL SELECT w.*,'predicted_class',c.definition,COUNT(o.predicted_class),(SELECT COUNT(*) FROM observations x WHERE x.window_id=w.window_id),1.0*COUNT(o.predicted_class)/(SELECT COUNT(*) FROM observations x WHERE x.window_id=w.window_id),NULL,NULL,NULL FROM windows w CROSS JOIN classes c LEFT JOIN observations o ON o.window_id=w.window_id AND o.predicted_class=c.definition GROUP BY w.window_id,w.reference_id,w.window_start,w.window_end,c.definition
UNION ALL SELECT w.*,'numeric_bin','[{lo},{mid})',SUM(CASE WHEN o.numeric_values>={lo} AND o.numeric_values<{mid} THEN 1 ELSE 0 END),COUNT(*),1.0*SUM(CASE WHEN o.numeric_values>={lo} AND o.numeric_values<{mid} THEN 1 ELSE 0 END)/COUNT(*),NULL,NULL,NULL FROM windows w JOIN observations o ON o.window_id=w.window_id WHERE o.numeric_values BETWEEN {lo} AND {hi} GROUP BY w.window_id,w.reference_id,w.window_start,w.window_end
UNION ALL SELECT w.*,'numeric_bin','[{mid},{hi}]',SUM(CASE WHEN o.numeric_values>={mid} AND o.numeric_values<={hi} THEN 1 ELSE 0 END),COUNT(*),1.0*SUM(CASE WHEN o.numeric_values>={mid} AND o.numeric_values<={hi} THEN 1 ELSE 0 END)/COUNT(*),NULL,NULL,NULL FROM windows w JOIN observations o ON o.window_id=w.window_id WHERE o.numeric_values BETWEEN {lo} AND {hi} GROUP BY w.window_id,w.reference_id,w.window_start,w.window_end
UNION ALL SELECT w.*,'numeric_summary','eligible numeric values',COUNT(*),COUNT(*),NULL,m.mean,SQRT(AVG((o.numeric_values-m.mean)*(o.numeric_values-m.mean))),{p['ddof']} FROM windows w JOIN observations o ON o.window_id=w.window_id JOIN means m ON m.window_id=w.window_id WHERE o.numeric_values BETWEEN {lo} AND {hi} GROUP BY w.window_id,w.reference_id,w.window_start,w.window_end,m.mean'''
 return query(sql,[('ds.reference','reference'),('ds.production','production')],L,'Aligned summaries; numerical standard deviation uses the policy divisor.')

VISUAL_DATA={
'distribution_monitoring':['ds.reference','ds.production','ds.production_200'],
'drift_degradation_distinction':['ds.evidence_scenarios'],
'data_drift_detection':['ds.reference','ds.production'],
'delayed_label_quality':['ds.predictions','ds.labels'],
'actionable_ml_alerts':['ds.alert_observations'],
'production_regression_diagnosis':['ds.release_evidence'],
'retraining_trigger_policy':['ds.trigger_events','ds.pipeline_stages'],
'authorized_retraining_execution':['ds.execution_fixtures'],
'retraining_run_idempotency':['ds.idempotency_traces'],
'retrained_candidate_validation':['ds.validation_counts'],
'ml_incident_runbook':['ds.incident_evidence'],
'ml_resource_utilization':['ds.resource_telemetry'],
'ml_workload_cost_attribution':['ds.billing_export','ds.lifecycle'],
'ml_workload_cost_guardrail':['ds.budget_replay'],
'serving_resource_cleanup':['ds.cleanup_inventory']
}

def visual(k,L):
 p=policies.get(k,{})
 if k=='distribution_monitoring': return [distribution_summary(L)]
 if k=='drift_degradation_distinction':
  return [diagram('Three distinct evidence questions',[
   ['P(X): input distribution','Compared with the reference','Does not measure labeled quality'],
   ['P(Y|X): conditional target relationship','Feature–label relationship changes','A useful model can become less useful'],
   ['Observed quality','Matched predictions and labels against quality reference','Without matched available labels: unresolved'],
   ['No implication across categories','A change in one does not establish changes in the others']],L),table('ds.evidence_scenarios',L)]
 if k=='data_drift_detection':
  return [{'type':'side_by_side','left':table('ds.reference',L),'right':table('ds.production',L),'left_label':p['reference_id'],'right_label':p['current_id'],'takeaway':p['distance_equation']+'; '+p['criterion']+'. Numerical bins use the same rule; mean/spread remain separate.','lineage':L}]
 if k=='delayed_label_quality':
  snippet='''import numpy as np
# cohort_records are fixed before label attachment; validate unique IDs first.
predictions_by_id = {r["prediction_id"]: r for r in cohort_records}
# Apply the supplied age, availability, duplicate and unmatched policies.
matched = attach_mature_labels(predictions_by_id, label_records, policy)
coverage = len(matched) / len(eligible_cohort_ids)
quality = sum(r["prediction"] != r["label"] for r in matched) / len(matched)
numeric_values = np.array([r["loss"] for r in matched])
loss_mean = np.mean(numeric_values)
loss_std = np.std(numeric_values, ddof=policy["ddof"])'''
  return [code(snippet,L),table('ds.predictions',L),table('ds.labels',L)]
 if k=='actionable_ml_alerts':
  snippet='''import numpy as np
import yaml
baseline_mean = np.mean(baseline_values)
baseline_spread = np.std(baseline_values, ddof=policy["ddof"])
with open(config_path, "w") as file_handle:
    yaml.safe_dump(config, file_handle)
with open(config_path) as file_handle:
    resolved = yaml.safe_load(file_handle)
inspect_required_fields(resolved)
# Replay the supplied rule; keep emitted owner/action records.
for fixture in ("normal", "boundary", "breached"):
    replay = replay_alert(resolved, fixture)
    assert replay["breach"] == policy["expected_replays"][fixture]'''
  return [code(snippet,L),table('ds.alert_observations',L,'Baseline and replay observations; outcomes are produced by replay, not inferred from formatting.')]
 if k=='production_regression_diagnosis':
  return [query('SELECT *, 1.0*labeled_errors/NULLIF(matched_eligible_labels,0) AS conditional_error_rate FROM release_evidence',[('ds.release_evidence','release_evidence')],L,'Separate release/cohort conditioning counts; a zero denominator gives an undefined rate.')]
 if k=='retraining_trigger_policy':
  f=flow('Eligible entry preserves required gates',['Authorized, investigated event + intended data','Data-quality/test gate','Train on approved data','Evaluate candidate','Separate promotion approval'],L)
  f['nodes'].append({'id':'failure','label':'Failed required check: downstream path blocked','kind':'end'});f['edges'].append({'from':'n2','to':'failure','label':'fails','kind':'no'})
  return [f,table('ds.trigger_events',L),table('ds.pipeline_stages',L)]
 if k=='authorized_retraining_execution':
  return [flow('Request is not proof of consumption',['Authorized event and input access','Resolve generation; verify bytes','Function/test gate: failure fatal','Invoke; retain returned ARN and actual parameters','Inspect consumed input against approved snapshot'],L),table('ds.execution_fixtures',L,'Invocation fixtures, not returned execution evidence.')]
 if k=='retraining_run_idempotency': return [table('ds.idempotency_traces',L,'Independent durable-state fixtures; persisted identity survives duplicates and restarts.')]
 if k=='retrained_candidate_validation':
  return [code('''# Counts come from the same declared validation cohort for both model roles.
fpr = FP / (FP + TN) if FP + TN else None
fnr = FN / (FN + TP) if FN + TP else None
if fpr is None or fnr is None:
    verdict = "reject"
else:
    expected_cost = policy["P_Y0"] * fpr * policy["cost_FP"] + policy["P_Y1"] * fnr * policy["cost_FN"]
    # Apply every predeclared quality, cost, slice and compatibility requirement.
    verdict = apply_required_gates(expected_cost, fpr, fnr, slice_pass, compatibility_pass)
record = {"registry_artifact_id": registry_artifact_id, "verdict": verdict}''',L),table('ds.validation_counts',L)]
 if k=='ml_incident_runbook':
  before=query("SELECT * FROM incident_evidence WHERE phase='before'",[('ds.incident_evidence','incident_evidence')],L,'Before: retained fault and authorized target evidence.')
  after=query("SELECT * FROM incident_evidence WHERE phase='after'",[('ds.incident_evidence','incident_evidence')],L,'After: expected simulator evidence; learner recovery must verify service behavior.')
  return [{'type':'before_after','before':before,'after':after,'change_summary':'Same-instance recovery requires readiness and bounded prediction checks, not running state alone.','lineage':L}]
 if k=='ml_resource_utilization':
  p=policies[k]
  sql=f'''WITH selected AS (SELECT * FROM resource_telemetry WHERE included=1 AND INSTANCE='{p['INSTANCE']}' AND process_id='{p['process_id']}' AND running_process=process_id AND instance_state='RUNNING' AND timestamp>='{p['interval_start']}' AND timestamp<'{p['interval_end_exclusive']}'), means AS (SELECT AVG(cpu_percent) AS cpu_mean,AVG(memory_value) AS memory_mean FROM selected) SELECT INSTANCE,process_id,MIN(timestamp) AS first_sample,MAX(timestamp) AS last_sample,COUNT(*) AS observation_count,'{p['interval_start']}' AS interval_start,'{p['interval_end_exclusive']}' AS interval_end_exclusive,'{p['cpu_unit']}' AS cpu_unit,memory_unit,cpu_mean,SQRT(AVG((cpu_percent-cpu_mean)*(cpu_percent-cpu_mean))) AS cpu_standard_deviation,memory_mean,SQRT(AVG((memory_value-memory_mean)*(memory_value-memory_mean))) AS memory_standard_deviation,{p['ddof']} AS ddof FROM selected CROSS JOIN means GROUP BY ALL'''
  return [query(sql,[('ds.resource_telemetry','resource_telemetry')],L,'Matched active interval: separate CPU/memory counts, units and policy divisor.'),table('ds.resource_telemetry',L,'Lifecycle and running-process evidence; excluded samples remain visible here.')]
 if k=='ml_workload_cost_attribution':return [table('ds.billing_export',L,'Eligible charges in fictional credits; shared and unmatched rows must remain in reconciliation.'),table('ds.lifecycle',L,'Separate workload/lifecycle and completed-work windows.')]
 if k=='ml_workload_cost_guardrail':
  before=diagram('Configured notification path',[[p['workload_scope'],p['period'],p['predicate']],[p['notification_topic'],'Receipt is tested separately']],L)
  after=diagram('Authorized response path',[[p['response_pipeline'],'Approved identity: '+p['authorized_identity']],[p['INSTANCE'],'Zone: '+p['ZONE'],'Safe stop only; inspect resulting state'],['Residual limitation',p['residual_limitation']]],L)
  return [{'type':'before_after','before':before,'after':after,'change_summary':'Notification receipt and authorized fixed-target stop are separate verified mechanisms.','lineage':L},table('ds.budget_replay',L,'Supplied below, boundary and breach expectations—not live cloud measurements.')]
 if k=='serving_resource_cleanup':
  return [{'type':'before_after','before':table('ds.cleanup_inventory',L,'Before: reconcile ownership, retirement, state, logs and shared references.'),'after':diagram('Verified cleanup outcome',[['Retired inventory','Only verified retired container stopped then removed','Only exclusively retired VM deleted under disk policy'],['Active release preserved','Referenced images and model/preprocessing artifacts retained','Readiness and bounded prediction checked'],['Audit','Retired absence and retained identities verified','Commands and logs checked for credential disclosure']],L),'change_summary':'Approved retired resources are removed while active serving and shared artifacts remain protected.','lineage':L}]
 raise ValueError(k)

# Complete data visuals with query-derived summaries. No result rows are authored.
base_visual=visual
def visual(k,L):
 blocks=base_visual(k,L)
 if k=='data_drift_detection':
  blocks.append(distribution_summary(L))
  policy=policies[k];cats=policy['declared_categories'];threshold=re.search(r'>\s*([0-9.]+)',policy['criterion']).group(1)
  definitions=' UNION ALL '.join(f"SELECT '{x}' AS category" for x in cats)
  distance_multiplier=re.search(r'^([0-9.]+)',policy['distance_equation']).group(1)
  sql=f"""WITH definitions AS ({definitions}), counts AS (SELECT d.category,(SELECT COUNT(*) FROM reference r WHERE r.category=d.category) AS reference_count,(SELECT COUNT(*) FROM production p WHERE p.category=d.category) AS current_count,(SELECT COUNT(*) FROM reference) AS reference_total,(SELECT COUNT(*) FROM production) AS current_total FROM definitions d), probabilities AS (SELECT *,1.0*reference_count/reference_total AS reference_probability,1.0*current_count/current_total AS current_probability FROM counts), distance AS (SELECT {distance_multiplier}*SUM(ABS(reference_probability-current_probability)) AS distance FROM probabilities) SELECT p.*,d.distance,d.distance>{threshold} AS crosses_criterion FROM probabilities p CROSS JOIN distance d"""
  blocks.append(query(sql,[('ds.reference','reference'),('ds.production','production')],L,'Category probabilities, supplied distance and feature verdict; equality is not a crossing.'))
 if k=='delayed_label_quality':
  # Keep the pedagogical code explicit about prevalidation and missing conditioning groups.
  blocks[0]['code']=blocks[0]['code'].replace('# cohort_records are fixed before label attachment; validate unique IDs first.','# Fix the cohort first; reject duplicates before dictionary construction.\nreject_repeated_ids(cohort_records)\nreject_repeated_ids(label_records)').replace('len(matched) / len(eligible_cohort_ids)','len(matched) / len(eligible_cohort_ids) if eligible_cohort_ids else None').replace('sum(r["prediction"] != r["label"] for r in matched) / len(matched)','sum(r["prediction"] != r["label"] for r in matched) / len(matched) if matched else None')
 if k=='actionable_ml_alerts':
  blocks[0]['code']+='\n    verify_emitted_owner_action(replay, resolved, policy["expected_replays"][fixture])'
 if k=='retrained_candidate_validation':
  p=policies[k]
  sql=f"""WITH rates AS (SELECT *,1.0*FP/NULLIF(FP+TN,0) AS FPR,1.0*FN/NULLIF(FN+TP,0) AS FNR FROM validation_counts) SELECT *,{p['P_Y0']}*FPR*{p['cost_FP']}+{p['P_Y1']}*FNR*{p['cost_FN']} AS expected_cost FROM rates"""
  blocks.append(query(sql,[('ds.validation_counts','validation_counts')],L,'Same-cohort actual-class rates and expected costs; required gates remain separate.'))
 if k=='ml_workload_cost_attribution':
  p=policies[k];mapping=' UNION ALL '.join(f"SELECT '{r}' AS resource_id,'{w}' AS workload" for r,w in p['resource_mapping'].items());sharing=' UNION ALL '.join(f"SELECT '{w}' AS workload,{v} AS share" for w,v in p['shared_rule'].items());unusual=re.search(r'>([0-9.]+)',p['unusual_rule']).group(1)
  sql=f"""WITH mapping AS ({mapping}),sharing AS ({sharing}), allocations AS (SELECT b.charge_id,b.reporting_window,b.charge_category,COALESCE(m.workload,'explicitly_unallocated') AS workload,b.amount AS allocated_amount FROM billing_export b LEFT JOIN mapping m ON m.resource_id=b.resource_id WHERE b.charge_category<>'shared' UNION ALL SELECT b.charge_id,b.reporting_window,b.charge_category,s.workload,b.amount*s.share AS allocated_amount FROM billing_export b CROSS JOIN sharing s WHERE b.charge_category='shared'), category_totals AS (SELECT reporting_window,workload,charge_category,SUM(allocated_amount) AS category_amount FROM allocations GROUP BY ALL), workload_totals AS (SELECT reporting_window,workload,SUM(allocated_amount) AS attributed_amount FROM allocations GROUP BY ALL), reconciliation AS (SELECT reporting_window,SUM(allocated_amount) AS allocated_plus_unallocated FROM allocations GROUP BY ALL), eligible AS (SELECT reporting_window,SUM(amount) AS eligible_total FROM billing_export GROUP BY ALL) SELECT c.*,w.attributed_amount,l.start AS work_start,l.stop AS work_end,l.completed_work,w.attributed_amount/NULLIF(l.completed_work,0) AS unit_cost,w.attributed_amount>{unusual} AS unusually_large,c.workload='explicitly_unallocated' AS unmatched,r.allocated_plus_unallocated,e.eligible_total,r.allocated_plus_unallocated=e.eligible_total AS reconciles FROM category_totals c JOIN workload_totals w USING(reporting_window,workload) LEFT JOIN lifecycle l USING(reporting_window,workload) JOIN reconciliation r USING(reporting_window) JOIN eligible e USING(reporting_window)"""
  blocks.append(query(sql,[('ds.billing_export','billing_export'),('ds.lifecycle','lifecycle')],L,'Category/workload allocations, matched completed work and per-window reconciliation in fictional credits.'))
 return blocks

COMPACT_FACTS={
'authorized_retraining_execution':[
'Before invocation, verify trigger permission for pipeline execution and intended input access.',
'Resolve and verify the approved object generation, not a mutable dataset name.',
'Import boto3; call boto3.client("sagemaker").start_pipeline_execution with supplied PipelineName, resolved Name/Value PipelineParameters and ClientRequestToken.',
'Retain returned PipelineExecutionArn and actual invocation parameters.',
'Bind trigger authorization, dataset version and returned execution identity in one auditable record.',
'Cloud Build steps need image name and args/script; wire the function/test entry into its assigned stage.',
'Use step IDs and waitFor predecessors; successful dependencies, not text position, govern downstream execution.',
'Gates stay fatal: no allowFailure or failing allowExitCodes; rejected Python gates exit unsuccessfully.',
'Use configured Pub/Sub bindings/filters; inspect actual stage results and resolved inputs for accepted/rejected fixtures.',
'availableSecrets.secretManager binds approved versions; secretEnv exposes only needed steps. YAML stores references, never secret values.',
'Use approved build/step identity; promotion requires separate authorization.',
'Check build output for disclosure; never echo or serialize runtime credentials.',
'Compare consumed stage snapshot with approved immutable input; a start request is not consumption proof.',
'Import yaml; safe_dump mapping/list configuration, safe_load it, and inspect resolved fields before submission. Standard tags only—not arbitrary Python constructors.'
],
'retraining_run_idempotency':[
'Pass run key and pipeline from the event dictionary to supplied durable atomic admission.',
'One atomic operation reserves unique key and active slot and persists job ID; local dictionaries or check-then-write cannot.',
'Branch on accepted, duplicate and busy; only acceptance authorizes a new logical launch.',
'Launch accepted work with its persisted job-ID token; retries/restarts cannot replace identity.',
'Duplicates/restarts attach to the persisted identity; unknown launch responses require same-token reconciliation, not second launch.',
'A different-key busy slot means policy-bounded defer/reject, never overlapping launch.',
'Release only after confirmed terminal state; retain completed keys so duplicates cannot relaunch.',
'Assert durable state/job count for concurrent same-key workers, different-key contention and fresh workers after reservation and launch.',
'Cloud Build steps declare image name and args/script; wire function/test into the assigned stage.',
'Use step IDs and waitFor predecessors; successful dependencies, not text position, govern downstream execution.',
'Gates stay fatal: no allowFailure or failing allowExitCodes; rejected Python gates exit unsuccessfully.',
'Use configured Pub/Sub bindings/filters; inspect actual stage results and resolved inputs for accepted/rejected fixtures.',
'Import yaml; safe_dump mapping/list configuration, safe_load it, and inspect resolved fields before submission. Standard tags only—not arbitrary Python constructors.'
],
'ml_workload_cost_attribution':[
'Select declared training/inference workload and reporting window from billing service/resource/time records.',
'Connect billed resources to workloads with existing labels or mapping.',
'Stopped compute may end compute charges; disks and other resources remain billable. Duration alone is incomplete expenditure.',
'Aggregate workload/category charges and reconcile attribution with eligible totals.',
'Unit cost divides attributed expenditure by corresponding completed work; retain billing and work windows.',
'Start/connect both tagged instances for bounded training/inference, record separate lifecycle windows, then stop both.',
'Match direct rows to workload/lifecycle; allocate shared rows by the supplied rule, never drop them.',
'Sum per window, flag large/unmatched allocations, and reconcile allocated plus explicitly unallocated amounts with eligible billing totals.',
'Authorized gcloud compute instances start/stop INSTANCE --zone=ZONE changes lifecycle; wait and inspect results.',
'Execute via gcloud compute ssh INSTANCE --zone=ZONE on the running authorized VM.',
'Inspect before/after identity/status using gcloud compute instances describe INSTANCE --zone=ZONE.',
'np.mean(numeric_values) computes the selected arithmetic mean.',
'np.std(numeric_values, ddof=0) divides squared deviations by N before the square root; ddof=1 only for required N−1.'
],
'ml_workload_cost_guardrail':[
'Configure supplied workload budget amount, reporting period and thresholds in the existing platform.',
'Connect the existing Pub/Sub topic and authorized path; test threshold-event receipt.',
'Notification and action are separate; verify the supplied authorized response rather than assuming consumption stops.',
'Record notification lag: spending can exceed budget; it is not a hard cap.',
'Replay below-threshold and breach fixtures, verifying notification and permitted response.',
'Event-response YAML safe stop targets only the explicitly approved nonproduction instance, never an unrestricted selector.',
'Bind the budget event to the pipeline; parse YAML and verify scope, threshold and fixed target before applying.',
'Simulate breach, inspect notification/response execution, and verify gcloud compute instances stop INSTANCE --zone=ZONE affected only the approved target.',
'Apply with approved identity and runtime Secret Manager references/secretEnv; check captured logs for literal credentials.',
'Inspect before/after identity/status using gcloud compute instances describe INSTANCE --zone=ZONE.',
'Import yaml; safe_dump mapping/list configuration, safe_load it, and inspect resolved fields before submission. Standard tags only—not arbitrary Python constructors.'
]
}

TAKEAWAYS={
'distribution_monitoring':'Align representations, bins and per-window denominators; retain reference/window identities and summary conventions.',
'drift_degradation_distinction':'Keep input, conditional-target and matched-label quality evidence distinct; missing labels leave quality unresolved.',
'data_drift_detection':'Use the predeclared comparison rule; a distribution crossing alone is not increased prediction error.',
'delayed_label_quality':'Preserve cohort identity and label boundaries; quality and maturity coverage use different denominators.',
'actionable_ml_alerts':'Inspect parsed policy and replay behavior; verify the configured breach owner/action record.',
'production_regression_diagnosis':'Test a supported hypothesis, retain matched-label denominators, and choose only a gated policy-supported response.',
'retraining_trigger_policy':'Bind evidence and intended data; trigger eligibility and promotion approval remain separate.',
'authorized_retraining_execution':'Verify immutable input, fatal dependencies and actual consumption; retain execution identity without disclosing credentials.',
'retraining_run_idempotency':'Atomic durable admission preserves one job token; release only after confirmed terminal state.',
'retrained_candidate_validation':'Compare the same cohort, enforce every required gate, and bind approval to the exact artifact.',
'ml_incident_runbook':'Recover only the authorized instance after testing the hypothesis; verify readiness and bounded prediction, not VM state alone.',
'ml_resource_utilization':'Match workload interval, lifecycle and process identity; retain counts, units and divisor.',
'ml_workload_cost_attribution':'Reconcile direct, shared and unallocated charges; unit cost needs matching completed work.',
'ml_workload_cost_guardrail':'Test notification and authorized response separately; lag means the budget is not a hard cap.',
'serving_resource_cleanup':'Verify ownership and retirement, preserve active/shared artifacts, and audit health and retired-resource absence.'
}
# Remediation contrasts use the same registry fixture family, with fact statements copied from evidence for precision.
CONTRAST={
'distribution_monitoring':'Contrast: each window owns its denominator; reusing the reference total changes production proportions.',
'drift_degradation_distinction':'Contrast: more long-distance inputs supports P(X); without matched labels it does not establish labeled degradation.',
'data_drift_detection':'Contrast: a distance crossing establishes the supplied distribution verdict, not a target-error verdict.',
'delayed_label_quality':'Contrast: maturity divides by all eligible cohort IDs; quality divides by matched mature IDs.',
'actionable_ml_alerts':'Contrast: parsed fields describe the rule; replay establishes whether the intended owner/action outcome occurs.',
'production_regression_diagnosis':'Contrast: release timing is correlation; the tested evidence must support the policy-bounded response.',
'retraining_trigger_policy':'Contrast: eligible retraining starts the required gates; it never substitutes for promotion approval.',
'authorized_retraining_execution':'Contrast: requested parameters are invocation evidence; inspected consumed inputs establish snapshot consumption.',
'retraining_run_idempotency':'Contrast: a duplicate attaches to the persisted job identity; it does not reserve a replacement launch.',
'retrained_candidate_validation':'Contrast: improved aggregate cost does not erase a required slice or compatibility failure.',
'ml_incident_runbook':'Contrast: a running VM is lifecycle evidence; readiness and bounded prediction establish recovered service behavior.',
'ml_resource_utilization':'Contrast: active matched samples describe the workload; stopped or unrelated samples change the population.',
'ml_workload_cost_attribution':'Contrast: stopping compute does not remove every charge; shared and explicitly unallocated credits stay in reconciliation.',
'ml_workload_cost_guardrail':'Contrast: notification receipt is not resource action, and neither creates a hard spending cap.',
'serving_resource_cleanup':'Contrast: verified retired-container removal is permitted; deletion of shared active artifacts is not.'
}

def words(s): return len(re.findall(r'\S+',s))
result={'schema_version':P['schema_version'],'kind':'screens_part','path_id':P['path_id'],'batch_id':P['batch_id'],'tiles':[]}
for tile in P['tiles']:
 out={'tile_id':tile['tile_id'],'title':' · '.join(C[c]['context']['concept_name'] for c in tile['concept_ids']),'steps':[],'remediation_steps':[]}
 for ps in tile['steps']:
  cids=ps['concept_ids'];c=C[cids[0]];k=cids[0].removeprefix('mle.');L=lin(cids,ps['teaching_block_ids'],ps['fact_ids'],ps['anchors'])
  s={'step_id':ps['step_id'],'type':ps['type'],'concept_ids':cids,'title':c['context']['concept_name'],'lineage':L}
  if ps['type'] in ['check','hands_on']:
   s['title']=('Check: ' if ps['type']=='check' else 'Practice: ')+c['context']['concept_name'];s['eyebrow']='Apply the evidence' if ps['type']=='check' else 'Fictional operations lab';s['lede']='Use the supplied fixture and declared policy.'
  elif ps['type']=='explainer':
   s['blocks']=[]
   for qtb in ps['teaching_block_ids']:
    cid,tid=qtb.split('#');tb=next(tb for tb in C[cid]['teaching_blocks'] if tb['id']==tid);idx=int(tid[2:])-1
    text=TEXT[cid.removeprefix('mle.')][idx]
    l=lin([cid],[qtb],[cid+'#'+f for f in tb['fact_ids']])
    s['blocks'].append(prose(text,l,{'intro':'intro','example':'example','misconception':'misconception'}.get(tb['purpose'],'definition')))
   s['title']=next(tb['title'] for tb in c['teaching_blocks'] if cids[0]+'#'+tb['id']==ps['teaching_block_ids'][0])
   if ps['planned_visual_block_type']:
    VL=lin(cids,ps['teaching_block_ids'],ps['fact_ids'],[cids[0]+'#visual']);s['blocks']+=visual(k,VL)
  elif ps['type']=='video':s['blocks']=[{'type':'media_group','segment_ids':ps['segment_ids']}]
  elif ps['type']=='recap':
   s['title']='Keep these distinctions';s['blocks']=[]
   for cid in cids:
    cc=C[cid];tb=cc['teaching_blocks'][-1]
    s['blocks'].append(prose(TAKEAWAYS[cid.removeprefix('mle.')],lin([cid],[cid+'#'+tb['id']],[cid+'#'+f for f in tb['fact_ids']]),'takeaway'))
   nxt=tile['next_tile_id'];nt=next((t for t in P['tiles'] if t['tile_id']==nxt),None)
   if nt:
    nc=C[nt['steps'][0]['concept_ids'][0]];s['blocks'].append({'type':'up_next','title':'Next: '+nc['context']['concept_name'],'text':TEXT[nc['context']['concept_id'].removeprefix('mle.')][0]})
   else:s['blocks'].append({'type':'up_next','title':'Path complete','text':'Review your operations records and the distinctions above.'})
  out['steps'].append(s)
 # Separate remediation for every distinct measured fact set in the plan.
 seen=set()
 for ps in tile['steps']:
  if ps['type'] not in ['check','hands_on']:continue
  key=(tuple(ps['concept_ids']),tuple(ps['fact_ids']))
  if key in seen:continue
  seen.add(key);cid=ps['concept_ids'][0];cc=C[cid];k=cid.removeprefix('mle.');facts=ps['fact_ids'];tbs=[cid+'#'+tb['id'] for tb in cc['teaching_blocks'] if set(tb['fact_ids']) & {f.split('#')[1] for f in facts}]
  L=lin(ps['concept_ids'],tbs,facts);rid=tile['tile_id']+f'.r{len(out["remediation_steps"])+1:02}'
  blocks=[]
  for fid in facts:
   statement=COMPACT_FACTS[k][int(fid.split('#f')[1])-1] if k in COMPACT_FACTS else next(f['statement'] for f in cc['coverage']['required_facts'] if cid+'#'+f['id']==fid)
   ftbs=[cid+'#'+tb['id'] for tb in cc['teaching_blocks'] if fid.split('#')[1] in tb['fact_ids']]
   blocks.append(prose(statement,lin([cid],ftbs,[fid])))
  measured_statements=[next(f['statement'] for f in cc['coverage']['required_facts'] if cid+'#'+f['id']==fid) for fid in facts]
  contrast=CONTRAST[k]
  if all(('arithmetic mean' in text or 'standard deviation' in text) for text in measured_statements):
   contrast='Contrast: np.mean summarizes the arithmetic center; np.std with ddof=0 uses N for squared deviations, not N−1 unless that divisor is required.'
  blocks.append(prose(contrast,L,'example'))
  blocks.append(table(VISUAL_DATA[k][0],L,'Revisit the same registered fixture; apply the contrast above.'))
  out['remediation_steps'].append({'step_id':rid,'type':'remediation','concept_ids':ps['concept_ids'],'title':'Revisit: '+cc['context']['concept_name'],'blocks':blocks,'lineage':L})
 result['tiles'].append(out)
(B/'screens.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
# Authoring checklist: plan fidelity, qualified lineage, block limits, budgets, framing-only steps, registry references, no fabricated outputs.
issues=[]
def walk(blocks):
 for bl in blocks:
  yield bl
  for key in ['left','right','before','after']:
   if key in bl:yield from walk([bl[key]])
for pt,ot in zip(P['tiles'],result['tiles']):
 assert [(s['step_id'],s['type']) for s in pt['steps']]==[(s['step_id'],s['type']) for s in ot['steps']]
 taught=set()
 for ps,s in zip(pt['steps'],ot['steps']):
  assert s['concept_ids']==ps['concept_ids']
  for key in ['fact_ids','teaching_block_ids']:assert s['lineage'][key]==ps[key]
  if s['type'] in ['check','hands_on']:assert 'blocks' not in s and 'interaction' not in s;assert set(ps['fact_ids'])<=taught
  count=sum(words(b['text']) for b in walk(s.get('blocks',[])) if b['type'] in ['prose','up_next'] and 'text' in b)
  # Every visible heading/lede is deliberately compact; count player text separately from code/data.
  if ps['word_budget'] and count>ps['word_budget']:issues.append((s['step_id'],'budget',count,ps['word_budget']))
  for b in walk(s.get('blocks',[])):
   if b['type']=='prose':taught.update(b['lineage']['fact_ids'])
   if ps['planned_visual_block_type'] and b['type'] not in ['prose','up_next']:assert any(a.endswith('#visual') for a in b['lineage']['anchors'])
 for s in ot['steps']+ot['remediation_steps']:
  for b in walk(s.get('blocks',[])):
   assert not any(key in b for key in ['rows','result','computed_values','output','execution_provenance'])
   if b['type']=='prose':assert 'lineage' in b and words(b['text'])<=90
   if 'lineage' in b:
    for key in ['fact_ids','teaching_block_ids','anchors']:
     for v in b['lineage'][key]:assert '#' in v and v.split('#')[0] in C
   if 'asset_ref' in b:
    ar=b['asset_ref'];assert ar['asset_id'] in assets;assert set(ar.get('columns',[]))<={c['name'] for c in assets[ar['asset_id']]['columns']}
   if 'result_of' in b:
    for m in b['result_of']['asset_mounts']:assert m['asset_id'] in assets
   if b['type']=='prose':assert not re.search(r'\bvideo\b',b['text'],re.I)
 required={cid+'#'+f['id'] for cid in pt['concept_ids'] for f in C[cid]['coverage']['required_facts']}
 assert required<=taught,required-taught
print('BUDGET ISSUES',issues)
print('COUNTS',[(t['tile_id'],len(t['steps']),len(t['remediation_steps'])) for t in result['tiles']])
(B/'screens_checklist.json').write_text(json.dumps({'budget_issues':issues,'counts':[(t['tile_id'],len(t['steps']),len(t['remediation_steps'])) for t in result['tiles']]},indent=2)+'\n')
