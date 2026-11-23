import json,re,copy,sqlite3,math
from pathlib import Path
B=Path('batches/final_batch_mle.region.production_operations')
P=json.load(open(B/'tile_plans.json')); G=json.load(open(B/'inputs/path_glossary_bundle.json')); R=json.load(open(B/'scenario_asset_registry.json'))
C={x['context']['concept_id']:x for x in G['bundles']}; A={x['asset_id']:x for x in R['assets']}
POL={}
for a in R['assets']:
 if a['asset_kind']=='code_workspace':
  for f in a['files']:
   if f['path']=='policy.json':POL[a['asset_id'][3:]]=json.loads(f['content'])
def q(v): return "'"+str(v).replace("'","''")+"'"
def lineage(cid,tbs=(),facts=(),visual=False):
 return dict(concept_ids=[cid],teaching_block_ids=[cid+'#'+x for x in tbs],fact_ids=[cid+'#'+x for x in facts],**({'anchors':[cid+'#visual']} if visual else {}))
def prose(cid,tb,text=None):
 return dict(type='prose',role=tb['purpose'] if tb['purpose'] in ['intro','definition','mechanism','example','misconception'] else 'mechanism',text=text or tb['content'],lineage=lineage(cid,[tb['id']],tb['fact_ids']))
def table(cid,asset,caption=None,cols=None):
 return dict(type='data_table',asset_ref=dict(asset_id=asset,columns=cols or [x['name'] for x in A[asset]['columns']]),caption=caption or A[asset]['title'],lineage=lineage(cid,visual=True))
def query(cid,sql,mounts,caption):
 return dict(type='data_table',result_of=dict(runtime='sql',sql=sql,asset_mounts=[dict(asset_id=a,mount_path=t) for a,t in mounts]),caption=caption,lineage=lineage(cid,visual=True))
def code(cid,text,language='python'):
 return dict(type='code_walkthrough',language=language,code=text,reveal='all',lineage=lineage(cid,visual=True))
def flow(cid,labels,edges,title):
 return dict(type='process_flow',title=title,direction='TB',nodes=[dict(id='n'+str(i),label=x) for i,x in enumerate(labels)],edges=[dict(**{'from':'n'+str(a),'to':'n'+str(b)},label=l) for a,b,l in edges],alt_text=title+': '+ '; '.join(labels),lineage=lineage(cid,visual=True))
def pair(cid,a,b,left,right,takeaway,kind='side_by_side'):
 if kind=='before_after':return dict(type=kind,before=a,after=b,change_summary=takeaway,lineage=lineage(cid,visual=True))
 return dict(type=kind,left=a,right=b,left_label=left,right_label=right,takeaway=takeaway,lineage=lineage(cid,visual=True))
# Re-voiced introductions and bounded examples: no outputs are authored here.
INTRO={
'distribution_monitoring':'Start with a named reference and production window. Use matching representations and categories; changed bins or denominators can make the comparison misleading.',
'drift_degradation_distinction':'Ask three separate questions: did inputs change, did the feature–label relationship change, and did measured prediction quality worsen? With labels unavailable, input evidence cannot answer all three.',
'data_drift_detection':'Choose the reference, window and comparison rule before inspecting the current data. Do not select a threshold afterward to make the change qualify.',
'delayed_label_quality':'Freeze the prediction cohort before labels arrive. Attach ground truth by prediction identity; recent predictions with incomplete labels are not a fully mature quality cohort.',
'actionable_ml_alerts':'An actionable alert needs an indicator, window rule, owner and response. Apply the supplied noise-tolerant rule rather than treating every fluctuation as a breach.',
'production_regression_diagnosis':'A release preceded worse client outcomes. That timeline is a starting point, not a cause. Gather release, data, service and mature-label evidence, then test one supported hypothesis.',
'retraining_trigger_policy':'A schedule, new data or supported operational evidence may trigger retraining. Record the reason and intended dataset; eligibility to execute is not candidate deployment approval.',
'authorized_retraining_execution':'Before invoking the existing pipeline, check execution permission and the approved input snapshot. After invocation, inspect the input the pipeline actually consumed.',
'retraining_run_idempotency':'Two workers may receive the same event; either may restart. Durable coordination must preserve one logical job identity and exclude another run key from the active pipeline slot.',
'retrained_candidate_validation':'Compare candidate and incumbent on a shared validation cohort. Record every required gate and the exact candidate identity; aggregate improvement alone is not acceptance.',
'ml_incident_runbook':'Recovery is scoped to one authorized nonproduction instance. Reproduce and isolate the injected service fault, then test the supported hypothesis before the lifecycle action.',
'ml_resource_utilization':'Define the ML workload interval before summarizing telemetry. Stopped intervals or unrelated processes must not silently enter an active-workload summary.',
'ml_workload_cost_attribution':'Choose workload identities and reporting windows, then reconcile direct and shared charges. Training compute time alone is not total workload expenditure.',
'ml_workload_cost_guardrail':'Test notification and the authorized resource response separately. A configured budget—even with a tested response—is not a guarantee against spending above it.',
'serving_resource_cleanup':'Verify ownership and retired release status before cleanup. Age is not authorization, and an old container may still reference artifacts needed by the active release.'}
EXAMPLE={
'distribution_monitoring':'Compare the registered reference and production windows using the declared categories and predicted classes. Keep absent categories in position. Normalize each window with its own eligible total, including the independent larger-window fixture. Keep fixed numerical edges, reference identity, window and the stated standard-deviation divisor with the summaries. This supports investigation of distribution change, not a labeled-error claim.',
'drift_degradation_distinction':'More long-distance orders support an input-distribution observation. They do not establish a changed feature–label relationship or worse labeled quality. Compare corresponding predictions and ground truth against the quality reference for the quality question. If labels are unavailable, retain the useful input or service evidence and mark quality unresolved. Missing labels prove neither stable quality nor degraded quality.',
'data_drift_detection':'Compare the registered windows with aligned category and numerical-bin proportions. Apply the supplied distance equation and threshold, not a newly chosen rule. Keep each window’s eligible total, fixed edges, reference identity, window, mean and stated spread. Name the crossing features. The verdict concerns distribution difference under that criterion, not increased target error.',
'delayed_label_quality':'Keep the fixed cohort separate from newer predictions. Reject duplicate identities before dictionary construction; record unmatched or unavailable labels separately. Maturity uses all eligible prediction IDs as its denominator. Quality uses only matched mature observations, with label coverage reported alongside it. Compute loss summaries on those specified observations. Missing labels are not successful predictions, and the mature subset does not automatically estimate quality for all traffic.',
'actionable_ml_alerts':'Use the fixture’s baseline, indicator, window rule, owner and response. Compute the requested mean and spread, then write and reload the existing YAML fields. Inspect what the runtime will read. Replay normal, boundary and breached cases with assertions: an owner/action record belongs only to a qualifying breach. Formatting alone does not verify behavior; a predicate alone does not verify the actionable outcome.',
'production_regression_diagnosis':'Compare active artifact and configuration identities with the approved run. Investigate a failed schema as a data condition; do not call distribution difference labeled degradation. Keep each release/cohort’s mature matched denominator separate. Reproduce and isolate the regression, then test the configuration-mismatch hypothesis against the fixture evidence. Choose only a supported data repair, approved rollback or gated retraining response, preserving validation. Timing and class mix alone do not establish cause.',
'retraining_trigger_policy':'An investigated distribution event can be eligible under the existing policy without being labeled-error evidence. Bind its intended dataset and trace entry, quality/test, training and evaluation. A failed required check blocks dependent stages. Reject unauthorized identities and uninvestigated alarms. Promotion still needs separate approval. Keep handoff credentials runtime-injected, never in policy values, YAML or captured logs.',
'authorized_retraining_execution':'Resolve and verify the approved object generation before invocation. Retain trigger authorization, immutable input, resolved parameters and returned execution ARN together. Wire the existing event-bound stages with fatal dependencies and the authorized step identity. Use scoped Secret Manager references, not secret values. Inspect consumed stage inputs, replay accepted and rejected fixtures, and review output for non-disclosure. A start request alone proves neither consumption nor promotion approval.',
'retraining_run_idempotency':'Use the single atomic admission operation for run key and pipeline slot. An accepted claim launches with its persisted job token; duplicates and restarted workers resume that identity. Reconcile an unknown response with the same token. Defer a different key while the slot is busy. Release only after confirmed terminal state, retaining the completed key. Assert durable state and logical job counts for concurrent and restarted workers; keep pipeline gates fatal.',
'retrained_candidate_validation':'Lower expected cost cannot override a failed required slice or compatibility gate. Compare both models under the same deployment probabilities, error costs and actual-class conditional rates. Reject undefined conditioning rates. Keep protected-test observations out of fitting and setting choice. Bind the exact candidate artifact and verdict to the promotion record, and assert valid, boundary and failure cases. Approval for one candidate is not approval for another.',
'ml_incident_runbook':'Retain instance, process and fault evidence before action. Test the runbook hypothesis, then stop and start the same authorized instance, waiting for each lifecycle transition. Reconnect and inspect the model service. Check readiness and a bounded prediction exchange against the contract; a running VM is not sufficient. Describe identity/state before and after. Keep runtime credentials out of commands, configuration and captured output.',
'ml_resource_utilization':'Inspect telemetry for the declared instance, process and active interval. Compare running-process evidence with the workload identity, using docker top for a containerized process. Summarize CPU and memory over that same interval, retaining observation counts, units, mean and the specified spread divisor. Inspect lifecycle state before and after where authorized. Do not append stopped or unrelated intervals to make the average look lower; these are descriptive utilization summaries, not expenditure calculations.',
'ml_workload_cost_attribution':'Retain each tagged workload’s lifecycle and reporting windows. Allocate direct rows by the supplied mapping, keep persistent-disk charges after compute stops, and share eligible rows under the explicit rule. Flag large or unmatched amounts and reconcile allocated plus explicitly unallocated charges to the export. Unit cost uses corresponding completed work and both windows. Start, connect, stop and inspect both authorized workload instances; retain per-workload mean and spread with the stated divisor.',
'ml_workload_cost_guardrail':'Bind the supplied workload budget and threshold to the existing Pub/Sub path and permitted response pipeline. Reload YAML and inspect scope, threshold and fixed nonproduction target before applying with the approved identity. Replay below-threshold and breach cases; inspect notification receipt, response execution and target state. Keep Secret Manager references runtime-resolved and review logs for non-disclosure. Notifications may lag usage: the verified fixture is not a hard spending cap.',
'serving_resource_cleanup':'Compare labels, identity, running/exit state and logs with the approved inventory and compute lifecycle. Stop and remove only verified retired containers; delete only the exclusively retired nonproduction instance under disk-preservation policy. Preserve images and model/preprocessing artifacts required by the active release, including shared references. Verify active readiness and bounded prediction, then confirm retired-resource absence. Record ownership, actions, retained artifacts and credential non-disclosure.'}
# Text transforms shorten sentences without altering the declared APIs, hedges or conditions.
def voice(cid,tb):
 key=cid[4:]
 if tb['purpose']=='intro':return INTRO[key]
 if tb['purpose']=='example':return EXAMPLE[key]
 text=tb['content']
 replacements={
 'Compute the arithmetic mean with':'For the arithmetic mean, use',
 'Compute standard deviation with':'For standard deviation, use',
 'over the selected numeric observations.':'on the selected numeric observations.',
 'before taking the square root;':'and then takes the square root;',
 'use ddof=1 only when the stated calculation requires':'use ddof=1 only if the stated calculation requires',
 'Write assert predicate checks for the declared valid, boundary and failure cases;':'Use assert predicates for declared valid, boundary and failure cases;',
 'during ordinary non-optimized execution.':'in ordinary non-optimized execution.',
 'With the declared PyYAML dependency, import yaml;':'Using the declared PyYAML dependency, import yaml;',
 'Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect':'Inspect with gcloud compute instances describe INSTANCE --zone=ZONE:',
 'Use the baseline measurement window and indicator definition to distinguish':'Distinguish, using the baseline measurement window and indicator definition,',
 'Keep required gate failures fatal:':'Required gate failures must stay fatal:',
 'A process-local dictionary or separate check-then-write calls cannot supply':'Neither a process-local dictionary nor separate check-then-write calls supplies',
 }
 for a,b in replacements.items():text=text.replace(a,b)
 return text

def split_text(text,maxwords=85):
 sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z])',text)
 chunks=[];current=''
 for sentence in sentences:
  if len((current+' '+sentence).split())>maxwords and current:chunks.append(current);current=sentence
  else:current=(current+' '+sentence).strip()
 if current:chunks.append(current)
 # A sentence can contain many clauses; split at semicolon if needed.
 out=[]
 for x in chunks:
  if len(x.split())>90:
   parts=x.split('; ');cur=''
   for part in parts:
    if cur and len((cur+'; '+part).split())>85:out.append(cur+'.');cur=part
    else:cur=(cur+'; '+part) if cur else part
   out.append(cur)
  else:out.append(x)
 return out

def distribution_query(cid,asset,window):
 p=POL['distribution_monitoring'];categories=p['declared_categories'];classes=p['declared_classes'];edges=p['fixed_edges'];lo,hi=p['eligible_numeric_range']
 vals=lambda xs: ' UNION ALL '.join('SELECT '+q(v)+' AS definition' for v in xs)
 sql=f"""WITH cats AS ({vals(categories)}), classes AS ({vals(classes)}),
 eligible AS (SELECT numeric_values AS v FROM samples WHERE numeric_values BETWEEN {lo} AND {hi}),
 summaries AS (
 SELECT 'category' AS representation, definition, COUNT(s.category) AS observations, (SELECT COUNT(*) FROM samples) AS eligible_total,
 1.0*COUNT(s.category)/(SELECT COUNT(*) FROM samples) AS proportion, NULL AS mean, NULL AS stddev, NULL AS ddof
 FROM cats LEFT JOIN samples s ON s.category=cats.definition GROUP BY definition
 UNION ALL
 SELECT 'predicted_class', definition, COUNT(s.predicted_class), (SELECT COUNT(*) FROM samples),
 1.0*COUNT(s.predicted_class)/(SELECT COUNT(*) FROM samples), NULL,NULL,NULL
 FROM classes LEFT JOIN samples s ON s.predicted_class=classes.definition GROUP BY definition
 UNION ALL
 """
 bins=[]
 for i,(a,b) in enumerate(zip(edges,edges[1:])):
  interval=f'[{a},{b}'+(']' if i==len(edges)-2 else ')')
  cond=f'v>={a} AND v'+('<=' if i==len(edges)-2 else '<')+str(b)
  bins.append(f"SELECT 'numeric_bin', {q(interval)}, SUM(CASE WHEN {cond} THEN 1 ELSE 0 END),COUNT(*),1.0*SUM(CASE WHEN {cond} THEN 1 ELSE 0 END)/COUNT(*),NULL,NULL,NULL FROM eligible")
 sql+=' UNION ALL '.join(bins)+f" UNION ALL SELECT 'numeric_summary','numeric_values',COUNT(*),COUNT(*),NULL,AVG(v),sqrt(GREATEST(0,AVG(v*v)-AVG(v)*AVG(v))),{p['ddof']} FROM eligible) SELECT {q(p['reference_id'])} AS reference_id,{q(window)} AS measurement_window,* FROM summaries"
 return query(cid,sql,[(asset,'samples')],'Aligned definitions, per-window denominators and numeric summaries; authored fictional fixture.')

def visuals(cid):
 k=cid[4:];p=POL.get(k,{})
 if k=='distribution_monitoring':
  w=p['production_window'];win=w['start']+'/'+w['end']
  return [distribution_query(cid,'ds.reference','approved reference'),distribution_query(cid,'ds.production',win)]
 if k=='drift_degradation_distinction':
  rows=A['ds.evidence_scenarios']['rows'];cols=[x['name'] for x in A['ds.evidence_scenarios']['columns']]
  nodes=[]
  for i,row in enumerate(rows):
   r=dict(zip(cols,row));nodes.append(dict(id='e'+str(i),label=r['supported_evidence'],fields=[r['observation'],r['unresolved']]))
  return [dict(type='diagram',diagram_kind='mapping',nodes=nodes,edges=[],alt_text='Separate evidence for input distribution, conditional target relationship and matched-label quality; none logically establishes the other two.',lineage=lineage(cid,visual=True))]
 if k=='data_drift_detection':
  left=distribution_query(cid,'ds.reference','approved reference');right=distribution_query(cid,'ds.production',p['comparison_window'])
  cats=p['declared_categories'];edges=p['fixed_edges'];lo,hi=p['eligible_numeric_range']
  defs=' UNION ALL '.join('SELECT '+q(v)+' AS definition' for v in cats)
  distributions=f"SELECT 'category' AS feature,definition,1.0*(SELECT COUNT(*) FROM reference WHERE category=definition)/(SELECT COUNT(*) FROM reference) AS rp,1.0*(SELECT COUNT(*) FROM current WHERE category=definition)/(SELECT COUNT(*) FROM current) AS cp FROM cats"
  for i,(a,b) in enumerate(zip(edges,edges[1:])):
   cond=f'numeric_values>={a} AND numeric_values'+('<=' if i==len(edges)-2 else '<')+str(b)
   distributions+=f" UNION ALL SELECT 'numeric_bins',{q(str([a,b]))},1.0*(SELECT COUNT(*) FROM reference WHERE {cond})/(SELECT COUNT(*) FROM reference WHERE numeric_values BETWEEN {lo} AND {hi}),1.0*(SELECT COUNT(*) FROM current WHERE {cond})/(SELECT COUNT(*) FROM current WHERE numeric_values BETWEEN {lo} AND {hi})"
  threshold=re.search(r'distance > ([0-9.]+)',p['criterion']).group(1)
  sql=f"WITH cats AS ({defs}), probabilities AS ({distributions}), distances AS (SELECT feature,0.5*SUM(ABS(rp-cp)) AS distance FROM probabilities GROUP BY feature) SELECT *,{q(p['distance_equation'])} AS equation,{q(p['criterion'])} AS criterion, distance>{threshold} AS crosses,{q(p['quality_claim'])} AS quality FROM distances"
  return [pair(cid,left,right,'Reference','Current','Apply aligned comparisons; a crossing does not measure prediction error.'),query(cid,sql,[('ds.reference','reference'),('ds.production','current')],'Feature-level distribution decisions under the supplied rule.')]
 if k=='delayed_label_quality':
  snippet='''import numpy as np
# Reject repeated prediction or label IDs before dictionary construction.
cohort_by_id = {row["prediction_id"]: row for row in eligible_predictions}
# Preserve each prediction_timestamp and the frozen cohort membership.
# Attach only cohort labels within the availability boundary and analysis delay.
# Record unmatched and unavailable labels separately.
maturity = len(matched_mature) / len(cohort_by_id)
error_proportion = sum(errors) / len(matched_mature)
mean_loss = np.mean(mature_losses)
spread_loss = np.std(mature_losses, ddof=0)'''
  cohort=q(p['cohort']);bound=q(p['label_available_through']);time=q(p['analysis_time']);age=p['minimum_age_hours']
  base=f"WITH cohort AS (SELECT * FROM predictions WHERE cohort_id={cohort} AND eligible=1), unique_labels AS (SELECT * FROM labels WHERE prediction_id IN (SELECT prediction_id FROM labels GROUP BY prediction_id HAVING COUNT(*)=1)), mature AS (SELECT c.*,l.label,l.loss,l.label_timestamp FROM cohort c JOIN unique_labels l USING(prediction_id) WHERE l.label_timestamp<={bound} AND (epoch(CAST({time} AS TIMESTAMP))-epoch(CAST(c.prediction_timestamp AS TIMESTAMP)))/3600>={age}) "
  return [code(cid,snippet),query(cid,base+f"SELECT {cohort} AS cohort_id,(SELECT COUNT(*) FROM cohort) AS eligible_ids,COUNT(*) AS matched_mature_ids,1.0*COUNT(*)/(SELECT COUNT(*) FROM cohort) AS maturity,SUM(CASE WHEN prediction!=label THEN 1 ELSE 0 END) AS matched_errors,1.0*SUM(CASE WHEN prediction!=label THEN 1 ELSE 0 END)/COUNT(*) AS mature_error_proportion,AVG(loss) AS mean_loss,sqrt(GREATEST(0,AVG(loss*loss)-AVG(loss)*AVG(loss))) AS stddev_loss,{p['ddof']} AS ddof FROM mature",[('ds.predictions','predictions'),('ds.labels','labels')],'Mature-cohort quantities only. Duplicate IDs reject; unmatched/late labels are excluded, not counted as successes.'),query(cid,base+'SELECT prediction_id,prediction_timestamp,label_timestamp,prediction,label,loss FROM mature',[('ds.predictions','predictions'),('ds.labels','labels')],'Identity-preserving mature join with retained timestamps.')]
 if k=='actionable_ml_alerts':
  snippet='''import numpy as np
import yaml
baseline_mean = np.mean(baseline_values)
baseline_spread = np.std(baseline_values, ddof=0)
with open(config_path, "w") as handle:
    yaml.safe_dump(config, handle)
with open(config_path) as handle:
    resolved = yaml.safe_load(handle)
# Inspect indicator, window rule, owner and response before replay.
assert normal_record is None
assert boundary_record is None
assert breached_record["owner"] == resolved["owner"]'''
  offset=re.search(r'\+([0-9.]+)',p['window_rule']).group(1)
  sql=f"WITH stats AS (SELECT window_id,COUNT(*) AS observations,AVG(numeric_values) AS mean,sqrt(GREATEST(0,AVG(numeric_values*numeric_values)-AVG(numeric_values)*AVG(numeric_values))) AS stddev FROM observations GROUP BY window_id), replay AS (SELECT *,mean>(SELECT mean FROM stats WHERE window_id={q(p['baseline_window'])})+{offset} AS breach FROM stats) SELECT *,{p['ddof']} AS ddof,{q(p['indicator'])} AS indicator,{q(p['window_rule'])} AS window_rule,CASE WHEN breach THEN {q(p['owner'])} END AS owner,CASE WHEN breach THEN {q(p['response'])} END AS response FROM replay"
  return [code(cid,snippet),query(cid,sql,[('ds.alert_observations','observations')],'Baseline/window statistics and configured breach-only owner/action record; replay assertions still require execution evidence.')]
 if k=='production_regression_diagnosis':
  return [query(cid,'SELECT *,1.0*labeled_errors/NULLIF(matched_eligible_labels,0) AS conditional_error_rate FROM evidence ORDER BY timestamp',[('ds.release_evidence','evidence')],'Timeline, approved-versus-active identities, mature-label denominators and tested hypothesis evidence.')]
 if k=='retraining_trigger_policy':
  labels=['Entry: permitted identity, investigated evidence, intended dataset','Data quality/test: validate intended input','Training: quality-approved data → candidate','Evaluation: candidate → validation evidence','Promotion: separate authorization','Rejected entry / failed required check']
  f=flow(cid,labels,[(0,1,'eligible'),(0,5,'unauthorized or uninvestigated'),(1,2,'quality passes'),(1,5,'quality fails: training/evaluation/promotion blocked'),(2,3,'training succeeds'),(3,4,'acceptance and promotion authorization')],'Existing gated pipeline; failed checks stop dependent stages')
  return [f,table(cid,'ds.trigger_events'),table(cid,'ds.pipeline_stages')]
 if k=='authorized_retraining_execution':
  stages=p['stage_contract'].split(';')[0].split(' -> ')
  labels=[x.replace('_',' ') for x in stages]+['Rejected entry or fatal gate failure: no invocation','Record returned execution ARN and actual parameters; separately authorize promotion']
  e=[(i,i+1,'required predecessor succeeds') for i in range(len(stages)-1)]+[(0,len(stages),'identity rejected'),(1,len(stages),'generation/bytes rejected'),(2,len(stages),'required gate fails'),(len(stages)-1,len(stages)+1,'verify consumed snapshot')]
  return [flow(cid,labels,e,'Authorized invocation and actual-input verification'),table(cid,'ds.execution_fixtures',cols=[x['name'] for x in A['ds.execution_fixtures']['columns'] if x['name']!='sha256']),code(cid,'# Approved reference values, not credentials or execution evidence\n'+json.dumps({x:p[x] for x in ['trigger_topic','build_identity','secret_version_reference','secretEnv','PipelineParameters']},indent=2),language='python')]
 if k=='retraining_run_idempotency':return [table(cid,'ds.idempotency_traces','Independent expected trace fixtures—not a single chronological transaction. Durable admission preserves job identity and terminal completion retains the key.')]
 if k=='retrained_candidate_validation':
  rates='SELECT *,1.0*FP/NULLIF(FP+TN,0) AS FPR,1.0*FN/NULLIF(FN+TP,0) AS FNR FROM counts'
  costs=f"SELECT *,{p['P_Y0']}*FPR*{p['cost_FP']}+{p['P_Y1']}*FNR*{p['cost_FN']} AS expected_cost FROM rates"
  acc=p['acceptance'];sql=f"WITH rates AS ({rates}), costs AS ({costs}), gates AS (SELECT *,FPR<={acc['maximum_FPR']} AND FNR<={acc['maximum_FNR']} AS quality_pass,expected_cost<=(SELECT i.expected_cost FROM costs i WHERE i.fixture=c.fixture AND i.model_role='incumbent') AS cost_pass FROM costs c) SELECT *, CASE WHEN quality_pass AND cost_pass AND slice_pass AND compatibility_pass THEN 'accept' ELSE 'reject' END AS verdict FROM gates"
  return [code(cid,'''negative_count = FP + TN
positive_count = FN + TP
# Empty actual-class groups yield undefined rates; reject explicitly.
FPR = FP / negative_count
FNR = FN / positive_count
expected_cost = P_Y0 * FPR * cost_FP + P_Y1 * FNR * cost_FN
# Acceptance requires cost, quality, slice and compatibility gates.
# Bind the exact registry_artifact_id and cohort_id to the verdict.
assert not accepted_when_required_gate_fails'''),query(cid,sql,[('ds.validation_counts','counts')],'Conditional rates, incumbent-relative costs and identity-bound gates; undefined groups reject.')]
 if k=='ml_incident_runbook':
  a=query(cid,"SELECT * FROM evidence WHERE phase='before'",[('ds.incident_evidence','evidence')],'Expected simulator state before recovery; no learner execution is claimed.')
  b=query(cid,"SELECT * FROM evidence WHERE phase='after'",[('ds.incident_evidence','evidence')],'Expected simulator state after same-instance recovery and service verification.')
  return [pair(cid,a,b,'Before','After','The same authorized instance needs process, readiness and prediction verification—not merely RUNNING.',kind='before_after')]
 if k=='ml_resource_utilization':
  sql=f"SELECT INSTANCE,process_id,MIN(timestamp) AS first_observation,MAX(timestamp) AS last_observation,COUNT(*) AS observations,{q(p['cpu_unit'])} AS cpu_unit,AVG(cpu_percent) AS cpu_mean,sqrt(GREATEST(0,AVG(cpu_percent*cpu_percent)-AVG(cpu_percent)*AVG(cpu_percent))) AS cpu_stddev,memory_unit,AVG(memory_value) AS memory_mean,sqrt(GREATEST(0,AVG(memory_value*memory_value)-AVG(memory_value)*AVG(memory_value))) AS memory_stddev,{p['ddof']} AS ddof FROM telemetry WHERE included=1 AND INSTANCE={q(p['INSTANCE'])} AND process_id={q(p['process_id'])} AND running_process={q(p['process_id'])} AND instance_state='RUNNING' AND timestamp>={q(p['interval_start'])} AND timestamp<{q(p['interval_end_exclusive'])} GROUP BY INSTANCE,process_id,memory_unit"
  return [table(cid,'ds.resource_telemetry','Inclusion status separates active workload telemetry from stopped or unrelated rows.'),query(cid,sql,[('ds.resource_telemetry','telemetry')],'CPU and memory share the declared matched interval, identity, counts and units.')]
 if k=='ml_workload_cost_attribution':
  mapping=p['resource_mapping'];shared=p['shared_rule'];arms=[]
  for resource,workload in mapping.items():arms.append(f"SELECT reporting_window,{q(workload)} AS workload,charge_id,charge_category,amount AS allocated FROM billing WHERE resource_id={q(resource)}")
  for workload,ratio in shared.items():arms.append(f"SELECT reporting_window,{q(workload)},charge_id,charge_category,amount*{ratio} FROM billing WHERE charge_category='shared'")
  mapped=','.join(q(x) for x in mapping)
  arms.append(f"SELECT reporting_window,'explicitly_unallocated',charge_id,charge_category,amount FROM billing WHERE resource_id NOT IN ({mapped}) AND charge_category!='shared'")
  allocation=' UNION ALL '.join(arms)
  sql=f"WITH allocations AS ({allocation}), totals AS (SELECT reporting_window,workload,SUM(allocated) AS attributed_total FROM allocations GROUP BY reporting_window,workload) SELECT t.*,l.start,l.stop,l.completed_work,1.0*t.attributed_total/NULLIF(l.completed_work,0) AS unit_cost,(SELECT SUM(amount) FROM billing b WHERE b.reporting_window=t.reporting_window) AS eligible_export_total,(SELECT SUM(attributed_total) FROM totals a WHERE a.reporting_window=t.reporting_window) AS allocated_plus_unallocated,attributed_total>10 AS unusually_large FROM totals t LEFT JOIN lifecycle l ON l.workload=t.workload AND l.reporting_window=t.reporting_window"
  stats=f"WITH allocations AS ({allocation}), totals AS (SELECT reporting_window,workload,SUM(allocated) AS value FROM allocations GROUP BY reporting_window,workload) SELECT workload,COUNT(*) AS reporting_windows,AVG(value) AS mean_per_window,sqrt(GREATEST(0,AVG(value*value)-AVG(value)*AVG(value))) AS stddev_per_window,{p['ddof']} AS ddof,{q(p['unit'])} AS unit FROM totals GROUP BY workload"
  return [table(cid,'ds.billing_export'),table(cid,'ds.lifecycle'),query(cid,f'WITH allocations AS ({allocation}) SELECT * FROM allocations',[('ds.billing_export','billing')],'Direct and explicitly shared allocations retain every eligible amount.'),query(cid,sql,[('ds.billing_export','billing'),('ds.lifecycle','lifecycle')],'Per-window attribution, unit costs and eligible-total reconciliation in fictional credits.'),query(cid,stats,[('ds.billing_export','billing')],'Per-workload descriptive statistics across the supplied reporting windows; do not mix workload series.')]
 if k=='ml_workload_cost_guardrail':
  before=query(cid,"SELECT fixture,workload_scope,budget_amount,period,threshold_ratio,observed_spend,INSTANCE,ZONE,'RUNNING' AS instance_state FROM replay",[('ds.budget_replay','replay')],'Expected pre-response states and workload budget configuration.')
  after=query(cid,'SELECT *,observed_spend>=budget_amount*threshold_ratio AS threshold_event FROM replay',[('ds.budget_replay','replay')],'Expected below/boundary/breach notifications, responses and after states—not learner execution evidence.')
  return [pair(cid,before,after,'Before','After','Notification receipt and authorized safe stop are separate checks. Notifications can lag usage; this is not a hard cap.',kind='before_after')]
 if k=='serving_resource_cleanup':
  before=table(cid,'ds.cleanup_inventory','Approved inventory and credential-safe expected runtime evidence before cleanup.')
  after=query(cid,'SELECT NAME,INSTANCE,ZONE,owner_label,release_label,expected_after,image_ref,model_artifact,preprocessing_artifact FROM inventory',[('ds.cleanup_inventory','inventory')],'Expected cleanup inventory outcomes; retained artifact references remain visible even on an absent retired container.')
  return [pair(cid,before,after,'Before','After','Only verified retired resources are removed. Preserve active/shared artifacts and verify active readiness, bounded prediction and retired absence.',kind='before_after')]
 raise ValueError(cid)

CHECK_CONTRAST={
'distribution_monitoring':'A mean uses the selected observations. For standard deviation, ddof=0 divides by N; ddof=1 uses N−1 only when required. Changing the divisor changes the requested calculation.',
'drift_degradation_distinction':'Input or service evidence can be reported with quality unresolved. Without matched available labels, neither “quality worsened” nor “quality stayed constant” follows from the input change.',
'data_drift_detection':'Crossing the declared rule identifies a feature-level distribution difference. It is not a measured increase in labeled prediction error.',
'delayed_label_quality':'Summarize only the selected mature matched losses. Keep the requested mean and spread divisor; missing labels are not zero-loss observations.',
'actionable_ml_alerts':'A normal replay must not emit the breach owner/action record. A qualifying breached replay must emit it. Use assertions for valid, boundary and failure cases, not formatting alone.',
'production_regression_diagnosis':'A release-correlated timeline is not a causal test. Use the supported policy response only after testing the hypothesis; preserve required validation gates.',
'retraining_trigger_policy':'Runtime injection keeps handoff credentials out of policy, YAML and captured logs. Writing credential values into any of those records violates that boundary.',
'authorized_retraining_execution':'Secret Manager versions belong in availableSecrets.secretManager references and scoped secretEnv, not literal credential values. Check captured output too: a reference-only YAML does not excuse leaked logs.',
'retraining_run_idempotency':'A textual stage order is not a successful-dependency gate. Use required waitFor IDs, keep failing gates fatal and inspect actual accepted/rejected stage results and resolved inputs.',
'retrained_candidate_validation':'An assertion for a valid case is not enough. Test declared boundary and failure predicates too; a false assert raises AssertionError in ordinary non-optimized execution.',
'ml_incident_runbook':'A RUNNING instance is not a recovered model service. Describe identity/state, reconnect, and verify restored readiness and a bounded prediction against the expected contract.',
'ml_resource_utilization':'An active-workload mean is not a mixture of stopped, unrelated and running observations. Match window, instance and process first; retain count, CPU/memory units and the specified divisor.',
'ml_workload_cost_attribution':'A unit cost divides attributed expenditure by corresponding completed work. A denominator from a different work window does not define the declared quantity.',
'ml_workload_cost_guardrail':'Inspect scope, threshold and fixed target after safe YAML reload and before application. A configuration that parses is not automatically the authorized budget-response binding.',
'serving_resource_cleanup':'An audit is not just a deletion list. Record verified ownership, active/retired identities, authorized actions, retained artifacts and credential non-disclosure checks.'}
SHORTEN={
'With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading accepts standard YAML tags, not arbitrary Python object constructors.':'Import yaml from the declared PyYAML dependency. Write mappings/lists with yaml.safe_dump(config, file_handle), reload with yaml.safe_load(file_handle), and inspect resolved fields before runtime submission. Safe loading accepts standard YAML tags, not arbitrary Python constructors.',
'In an existing Cloud Build YAML/JSON configuration, each steps item declares its execution image in name and its command in args or script; wire the function/test entry point into the assigned stage.':'In existing Cloud Build YAML/JSON steps, name specifies the execution image; args or script specifies the command. Wire the function/test entry into its assigned stage.',
'Assign step IDs and set waitFor to the required preceding step IDs; downstream execution depends on those steps completing successfully, not just their textual location.':'Assign step IDs and required predecessor IDs in waitFor. Successful dependencies, not textual order, permit downstream execution.',
'Keep required gate failures fatal: do not set allowFailure or add failing gate exit codes to allowExitCodes, and ensure a rejected Python gate exits unsuccessfully.':'Required failures stay fatal: no allowFailure or failing codes in allowExitCodes; rejected Python gates must exit unsuccessfully.',
'Use the configured Pub/Sub artifact/event trigger with its configured payload bindings and filters to run the existing pipeline, then inspect actual stage results and resolved inputs for accepted and rejected fixtures.':'Use the existing Pub/Sub artifact/event trigger, payload bindings and filters. Inspect actual stage results and resolved inputs for accepted and rejected fixtures.',
'Use the supplied single atomic operation that reserves both the unique run key and pipeline active slot and persists the job ID; a process-local dictionary or separate check-then-write calls cannot supply that durable admission contract.':'One supplied atomic operation reserves both unique run key and pipeline slot and persists job ID. Process-local dictionaries and separate check-then-write calls cannot supply this durable contract.',
'For a duplicate or restarted claim, resume or attach to that same persisted job identity; an unknown launch response requires same-token reconciliation rather than a second logical launch.':'Duplicates and restarted claims attach or resume the persisted job. Reconcile unknown launch responses with that same token, not a second logical launch.',
'Assert durable state and logical job count for two concurrent same-event workers, two different-key workers contending for one slot, and fresh workers after reservation and after launch.':'Assert durable state and logical job count for concurrent same-event workers, different-key slot contenders, and fresh workers after both reservation and launch.',
'Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect the instance status and identity before and after the authorized lifecycle action.':'Inspect identity/status before and after authorized lifecycle action with gcloud compute instances describe INSTANCE --zone=ZONE.',
}
TITLES=['Comparable production distributions','Labels, alerts and regression diagnosis','Controlled retraining and candidate acceptance','Runbook-scoped service recovery','Workload utilization, costs and safe cleanup']
RECAPS=[
'Keep representations, bins and per-window denominators aligned. Separate input distribution, conditional-target and matched-label quality evidence. Apply only the declared drift criterion; a crossing alone does not measure target error.',
'Freeze cohorts before delayed-label joins and keep maturity separate from mature-cohort quality. Inspect alert configuration and verify breach-only owner/action behavior. Diagnose with matched evidence and a tested hypothesis, then preserve gates in the supported response.',
'Bind trigger reason and intended dataset without confusing retraining with deployment approval. Verify permitted invocation and actual immutable-input consumption. Preserve durable job identity across retries. Accept only the exact candidate that passes every required gate.',
'Use only the authorized nonproduction recovery identity. Retain fault evidence and test the hypothesis before the same-instance stop/start sequence. Verify restored model readiness and bounded prediction behavior, with runtime credentials kept out of captured output.',
'Align CPU/memory evidence with the active workload. Reconcile direct, shared and explicitly unallocated charges. Test budget notification and fixed-target response separately without promising a spending cap. Remove only verified retired resources, preserve required artifacts and verify active health.'
]
OUT=dict(schema_version=P['schema_version'],kind='screens_part',path_id=P['path_id'],batch_id=P['batch_id'],tiles=[])
for ti,t in enumerate(P['tiles']):
 ot=dict(tile_id=t['tile_id'],title=TITLES[ti],steps=[],remediation_steps=[])
 seen=set()
 for s in t['steps']:
  cid=s['concept_ids'][0];base=dict(step_id=s['step_id'],type=s['type'],concept_ids=copy.deepcopy(s['concept_ids']),title=C[cid]['context']['concept_name'],lineage={x:copy.deepcopy(s[x]) for x in ['concept_ids','teaching_block_ids','fact_ids','segment_ids','anchors']})
  if s['type']=='explainer':
   base['blocks']=[]
   tbs={x['id']:x for x in C[cid]['teaching_blocks']}
   selected=[tbs[x.split('#')[1]] for x in s['teaching_block_ids']]
   base['title']= ('Work the contrast: ' if selected[0]['purpose']=='misconception' else 'Apply the rule: ' if selected[0]['purpose']=='example' else '')+ C[cid]['context']['concept_name']
   for tb in selected:
    for text in split_text(voice(cid,tb)):base['blocks'].append(prose(cid,tb,text))
   if s.get('planned_visual_block_type'):base['blocks']+=visuals(cid)
  elif s['type']=='video':base['blocks']=[dict(type='media_group',segment_ids=copy.deepcopy(s['segment_ids']))]
  elif s['type']=='recap':
   base['title']='Keep these distinctions';base['blocks']=[dict(type='prose',role='takeaway',text=RECAPS[ti],lineage=dict(concept_ids=s['concept_ids'],teaching_block_ids=[],fact_ids=[]))]
   nextid=t.get('next_tile_id')
   if nextid:
    nc=next(x for x in P['tiles'] if x['tile_id']==nextid)['steps'][0]['concept_ids'][0]
    base['blocks'].append(dict(type='up_next',title=C[nc]['context']['concept_name'],text=INTRO[nc[4:]]))
   else:base['blocks'].append(dict(type='up_next',title='Path complete',text='Review the distinctions from these production-operations lessons.'))
  else:
   base['eyebrow']='Check the distinction' if s['type']=='check' else 'Practice'
   if s['planned_interaction_type'] in ['choice','classify']:
    base['title']='Review '+C[cid]['context']['concept_name'].lower()
    base['lede']='Read the supplied excerpt(s) in this step and decide which interpretation or action is correct, defective or unsafe.'
   else:
    base['title']='Apply '+C[cid]['context']['concept_name'].lower()
    base['lede']='Complete the learner-defined function and required imports under the supplied policy; use the declared cases to verify the single deliverable.'
   key=(cid,tuple(s['fact_ids']))
   if key not in seen:
    seen.add(key)
    fids=[x.split('#')[1] for x in s['fact_ids']]
    tbids=[x['id'] for x in C[cid]['teaching_blocks'] if set(x['fact_ids'])&set(fids) and x['purpose'] not in ['example','misconception']]
    r=dict(step_id=t['tile_id']+'.r'+str(len(ot['remediation_steps'])+1).zfill(2),type='remediation',concept_ids=[cid],title='Revisit: '+C[cid]['context']['concept_name'],lineage=lineage(cid,tbids,fids),blocks=[])
    facts={x['id']:x['statement'] for x in C[cid]['coverage']['required_facts']}
    # Each fact is its own bounded idea. Re-teach exactly the measured set.
    for fid in fids:
     related=[x['id'] for x in C[cid]['teaching_blocks'] if fid in x['fact_ids'] and x['purpose'] not in ['example','misconception']]
     for txt in split_text(SHORTEN.get(facts[fid],facts[fid])):r['blocks'].append(dict(type='prose',role='mechanism',text=txt,lineage=lineage(cid,related,[fid])))
    # One clear contrast, reusing the same scenario rather than introducing a new dataset.
    contrast=next(x['content'] for x in reversed(C[cid]['teaching_blocks']) if x['purpose']=='misconception') if s['type']=='hands_on' else CHECK_CONTRAST[cid[4:]]
    r['blocks'].append(dict(type='prose',role='misconception',text=contrast,lineage=lineage(cid,tbids,fids)))
    ot['remediation_steps'].append(r)
  ot['steps'].append(base)
 OUT['tiles'].append(ot)
(B/'screens.json').write_text(json.dumps(OUT,indent=2)+'\n')
print('tiles',len(OUT['tiles']),'steps',sum(len(t['steps']) for t in OUT['tiles']),'remediations',sum(len(t['remediation_steps']) for t in OUT['tiles']))
