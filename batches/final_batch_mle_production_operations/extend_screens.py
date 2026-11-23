from pathlib import Path
p=Path(__file__).parent/'build_screens.py'
s=p.read_text()
s=s.replace('GROUP BY w.window_id,c.definition','GROUP BY ALL').replace('GROUP BY w.window_id','GROUP BY ALL').replace('GROUP BY INSTANCE,process_id,memory_unit','GROUP BY ALL')
s=s.replace("if ps['planned_visual_block_type'] and b['type'] not in ['prose','up_next']:assert cid if True else False", "if ps['planned_visual_block_type'] and b['type'] not in ['prose','up_next']:assert any(a.endswith('#visual') for a in b['lineage']['anchors'])")
insert='''
# Complete data visuals with query-derived summaries. No result rows are authored.
base_visual=visual
def visual(k,L):
 blocks=base_visual(k,L)
 if k=='data_drift_detection':
  blocks.append(distribution_summary(L))
  policy=policies[k];cats=policy['declared_categories'];threshold=re.search(r'>\\s*([0-9.]+)',policy['criterion']).group(1)
  definitions=' UNION ALL '.join(f"SELECT '{x}' AS category" for x in cats)
  sql=f"""WITH definitions AS ({definitions}), counts AS (SELECT d.category,(SELECT COUNT(*) FROM reference r WHERE r.category=d.category) AS reference_count,(SELECT COUNT(*) FROM production p WHERE p.category=d.category) AS current_count,(SELECT COUNT(*) FROM reference) AS reference_total,(SELECT COUNT(*) FROM production) AS current_total FROM definitions d), probabilities AS (SELECT *,1.0*reference_count/reference_total AS reference_probability,1.0*current_count/current_total AS current_probability FROM counts), distance AS (SELECT 0.5*SUM(ABS(reference_probability-current_probability)) AS distance FROM probabilities) SELECT p.*,d.distance,d.distance>{threshold} AS crosses_criterion FROM probabilities p CROSS JOIN distance d"""
  blocks.append(query(sql,[('ds.reference','reference'),('ds.production','production')],L,'Category probabilities, supplied distance and feature verdict; equality is not a crossing.'))
 if k=='delayed_label_quality':
  # Keep the pedagogical code explicit about prevalidation and missing conditioning groups.
  blocks[0]['code']=blocks[0]['code'].replace('# cohort_records are fixed before label attachment; validate unique IDs first.','# Fix the cohort first; reject duplicates before dictionary construction.\\nreject_repeated_ids(cohort_records)\\nreject_repeated_ids(label_records)').replace('len(matched) / len(eligible_cohort_ids)','len(matched) / len(eligible_cohort_ids) if eligible_cohort_ids else None').replace('sum(r["prediction"] != r["label"] for r in matched) / len(matched)','sum(r["prediction"] != r["label"] for r in matched) / len(matched) if matched else None')
 if k=='actionable_ml_alerts':
  blocks[0]['code']+='\\n    verify_emitted_owner_action(replay, resolved, policy["expected_replays"][fixture])'
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
'''
s=s.replace('\nTAKEAWAYS={',insert+'\nTAKEAWAYS={')
s=s.replace("statement=next(f['statement'] for f in cc['coverage']['required_facts'] if cid+'#'+f['id']==fid)","statement=COMPACT_FACTS[k][int(fid.split('#f')[1])-1] if k in COMPACT_FACTS else next(f['statement'] for f in cc['coverage']['required_facts'] if cid+'#'+f['id']==fid)")
p.write_text(s)
