import json,re,copy,csv,io
from pathlib import Path
B=Path('batches/final_batch_mle.region.production_operations')
p=json.loads((B/'tile_plans.json').read_text());g=json.loads((B/'inputs/path_glossary_bundle.json').read_text());r=json.loads((B/'scenario_asset_registry.json').read_text())
bs={b['context']['concept_id']:b for b in g['bundles']};assets={a['asset_id']:a for a in r['assets']}
def policy(c):
 return json.loads(next(f['content'] for f in assets['ws.'+c]['files'] if f['path']=='policy.json'))
def rows(a):
 a=assets[a];return [dict(zip([c['name'] for c in a['columns']],x)) for x in a['rows']]
def lin(c,tbs=(),facts=(),visual=False):
 return {'concept_ids':[c],'teaching_block_ids':list(tbs),'fact_ids':list(facts),**({'anchors':[c+'#visual']} if visual else {})}
def prose(text,L,role='definition'):return {'type':'prose','text':text,'role':role,'lineage':copy.deepcopy(L)}
# Shorter screen voice; preserve qualifiers, API names and policy boundaries.
def voice(s):
 replacements=[('Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations.','For the selected numeric observations, np.mean(numeric_values) gives the arithmetic mean.'),('Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor.','Use np.std(numeric_values, ddof=0): divide squared deviations by N, then take the square root. Use ddof=1 only when the calculation calls for N−1.'),('With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading accepts standard YAML tags, not arbitrary Python object constructors.','With the declared PyYAML dependency, import yaml. Write mappings/lists with yaml.safe_dump(config, file_handle); reload with yaml.safe_load(file_handle). Inspect required resolved fields before runtime submission. Safe loading accepts standard YAML tags, not arbitrary Python object constructors.'),('Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.','Check declared valid, boundary and failure cases with assert predicates. A false predicate raises AssertionError in ordinary non-optimized execution.'),('Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect the instance status and identity before and after the authorized lifecycle action.','Before and after the authorized lifecycle action, inspect identity and status with gcloud compute instances describe INSTANCE --zone=ZONE.'),('In an existing Cloud Build YAML/JSON configuration, each steps item declares its execution image in name and its command in args or script; wire the function/test entry point into the assigned stage.','In the existing Cloud Build YAML/JSON, a steps item uses name for its execution image and args or script for its command. Wire the function/test entry point into the assigned stage.'),('Keep required gate failures fatal: do not set allowFailure or add failing gate exit codes to allowExitCodes, and ensure a rejected Python gate exits unsuccessfully.','Required gate failures must stay fatal. Do not set allowFailure or put failing gate exit codes in allowExitCodes. A rejected Python gate must exit unsuccessfully.')]
 for a,b in replacements:s=s.replace(a,b)
 # Reorder a few common instructions without changing their scope.
 s=s.replace('retaining the denominator','keeping the denominator visible').replace('rather than asserting','instead of asserting').replace('rather than assuming','instead of assuming').replace('so the invocation can be audited','to make the invocation auditable').replace('before checking production data','before inspecting production data').replace('before comparing expenditure','before comparing costs').replace('rather than selecting resources by age alone','instead of selecting by age alone').replace('not just their textual location','not merely their position in the file')
 return s
examples={
'distribution_monitoring':'In the order fixture, compare the reference and production category summaries using the declared category positions, including absent categories. Each window uses its own total; an alternate window must not borrow the reference denominator. Numerical bins keep the fixed edges and eligible constraints. Retain the window and reference identities with means and standard deviations using the stated divisor. Contrast aligned proportions with raw counts or changed bins: the latter do not preserve a comparable measurement.',
'drift_degradation_distinction':'More long-distance orders support an input-distribution statement, not a conclusion about the conditional target relationship or prediction errors. To report observed quality degradation, compare matched ground truth with predictions and the declared quality reference. Missing labels leave that question unresolved; they do not prove quality stayed constant. Conversely, conditional-target evidence can reveal a relationship change without establishing an input-marginal change. Keep supported evidence and unresolved questions in separate parts of the report.',
'data_drift_detection':'Use the declared reference and current window with aligned categories and fixed numerical edges. Calculate each probability vector with its own eligible total, then apply the supplied distance equation and predeclared crossing rule. Retain numerical means and standard deviations separately. Report which features cross the criterion; the distance verdict concerns distributions, not a measured increase in prediction error. A larger current window changes the denominator, not the category definitions or threshold after inspection.',
'delayed_label_quality':'Build the prediction-ID dictionary only after duplicate checks. Keep prediction time and cohort membership; attach only labels meeting the availability boundary. Exclude and record unmatched or outside-cohort labels. Maturity divides mature eligible IDs by all eligible cohort IDs. Quality uses the matched mature subset, with coverage reported beside it. Selected loss means and standard deviations describe that subset. They do not establish quality for all traffic without justified coverage.',
'actionable_ml_alerts':'Use the registered baseline window and indicator, then inspect the safely reloaded YAML fields for threshold, window, owner and response. Compute baseline mean and spread with the stated divisor. Replay normal, boundary and breached fixtures with assertion predicates, checking emitted owner/action records against the supplied rule. A single fluctuation is not automatically actionable. Safe loading does not replace field inspection, and a configuration file alone does not prove that replay emitted the intended action.',
'production_regression_diagnosis':'Begin with client impact and the release/telemetry timeline. Compare active and approved artifacts and configurations, then separate schema failures, distribution evidence and mature-label evidence. Calculate each release/cohort error rate using its own matched eligible count. Reproduce the issue and test the supplied configuration-mismatch hypothesis. Choose only the response supported under the incident policy, retaining validation gates. A release correlation or distribution difference is not, by itself, a measured quality regression or a demonstrated cause.',
'retraining_trigger_policy':'Trace an authorized, investigated event through entry with its trigger reason and intended dataset. Preserve whether evidence is distribution-only or label-verified. Annotate quality/test, training and evaluation stages with artifact inputs and purposes. A failed required check blocks its downstream path. Reject unauthorized identities and uninvestigated alarms. Keep promotion approval separate, even after retraining succeeds. Runtime-injected handoff credentials belong neither in policy/YAML values nor captured stage logs.',
'authorized_retraining_execution':'Resolve and verify the approved snapshot generation before invoking the supplied pipeline. Retain authorization, input identity, resolved parameters and returned execution ARN together. Wire existing event bindings and fatal step dependencies; scope runtime secret references to the required authorized steps. Replay accepted and rejected fixtures. Inspect actual consumed stage inputs against the approved immutable snapshot: the start request is not proof of consumption. Safely reload and inspect configuration, review captured output for credential disclosure, and retain separate promotion authorization.',
'retraining_run_idempotency':'Submit the run key and pipeline identity to one durable atomic admission operation. Accepted claims launch with the persisted job ID as token; duplicates and restarted workers attach or reconcile using that same identity. A different key encountering a busy slot follows defer/reject policy without overlap. Release the slot only after terminal confirmation and retain the completed key record. Assert durable state and logical-job count for concurrent same-key workers, different-key contention and restarts after reservation and launch. Keep required build gates fatal.',
'retrained_candidate_validation':'Compare candidate and incumbent on the same cohort under fixed acceptance requirements, deployment probabilities and error costs. Derive FPR from actual negatives and FNR from actual positives; an empty conditioning group leaves its rate undefined. Lower expected cost cannot bypass required slice or compatibility gates. Keep protected test observations out of fitting and selection. Bind the exact artifact identity to the verdict and use passing, boundary and failing assertion fixtures. Approval for one candidate cannot be transferred to another.',
'ml_incident_runbook':'Record the authorized instance, lifecycle and process/service fault before acting. Reproduce the injected fault and test the runbook-supported recovery hypothesis. Stop the same approved instance, wait, start it and wait until running; reconnect and inspect the service. Verify readiness and a bounded prediction against the expected contract. A running VM alone does not prove recovery. Retain before/after identity and status plus service results, using runtime-injected credentials without embedding or printing them.',
'ml_resource_utilization':'Select the active workload interval using instance, process and lifecycle evidence. Keep CPU and memory measurements aligned to that same interval, with observation counts and separate units. Use the declared mean and standard-deviation divisor. Compare container process evidence with docker top and inspect instance identity/status before and after the permitted action. Do not append stopped or unrelated rows to make utilization appear lower. These are descriptive resource summaries, not an independent measurement of billed cost or model quality.',
'ml_workload_cost_attribution':'Select the training and inference identities and reporting windows. Allocate direct charges to their matching lifecycle intervals and shared charges under the supplied explicit rule. Keep persistent-disk charges even after compute stops. Reconcile allocated plus explicitly unallocated amounts with every eligible billing row; flag unusually large or unmatched allocations. Unit cost divides attributed expense by matching completed work and retains both windows. Start, connect, execute, stop and inspect both authorized tagged instances, keeping their lifecycle windows separate.',
'ml_workload_cost_guardrail':'Inspect budget scope, period, threshold and the fixed approved target before applying safely reloaded configuration. Bind the existing notification topic to the authorized response pipeline, not a broad selector. Replay below-threshold and breach fixtures; inspect notification receipt, response execution and before/after target status. Scope Secret Manager runtime references to the approved identity and review captured logs. Record the limitation: notifications can lag usage, so a tested safe-stop response still is not a hard spending cap.',
'serving_resource_cleanup':'Reconcile actual container ownership, release labels, running/exit state and logs against the approved inventory and compute lifecycle. Stop and remove only a verified retired container; delete only the exclusively retired test instance with the approved disk treatment. Preserve shared active images and required model/preprocessing artifacts. Inspect before/after identities, verify active readiness and a bounded prediction, and confirm retired resources are absent. Record ownership, permitted actions, retained artifacts and credential non-disclosure. Age alone does not authorize cleanup.'}

def split_prose(text,L,role):
 # Sentence boundaries require whitespace and an uppercase start, avoiding API dots.
 sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z])',text.strip())
 out=[prose(sent,L,role) for sent in sentences if sent.strip()]
 return out

def table(a,c,L=None,columns=None):
 return {'type':'data_table','asset_ref':{'asset_id':a,**({'columns':columns} if columns else {})},'lineage':L or lin(c,visual=True)}
def query(sql,mounts,c):return {'type':'data_table','result_of':{'runtime':'sql','sql':sql,'asset_mounts':[{'asset_id':a,'mount_path':n} for a,n in mounts]},'lineage':lin(c,visual=True)}
def code(text,c):return {'type':'code_walkthrough','language':'python','code':text,'reveal':'line_by_line','lineage':lin(c,visual=True)}
def diagram(c,nodes,title,edges=[]):return {'type':'diagram','diagram_kind':'mapping','title':title,'nodes':[{'id':'n'+str(i),'label':label,'fields':fields} for i,(label,fields) in enumerate(nodes)],'edges':edges,'alt_text':title,'lineage':lin(c,visual=True)}
def pair(c,left,right,l,r,take):return {'type':'side_by_side','left':left,'right':right,'left_label':l,'right_label':r,'takeaway':take,'lineage':lin(c,visual=True)}
def before(c,left,right,text):return {'type':'before_after','before':left,'after':right,'change_summary':text,'lineage':lin(c,visual=True)}

def summary_query(a,c,pol):
 # All values come from declared policy; SQL results remain unfilled until assembly.
 cats=pol['declared_categories'];edges=pol['fixed_edges'];lo,hi=pol['eligible_numeric_range'];
 cat_cte=' UNION ALL '.join('SELECT '+json.dumps(x)+(' AS category' if i==0 else '') for i,x in enumerate(cats))
 identity=pol['reference_id'] if a=='ds.reference' else ('production' if a=='ds.production' else a.split('.')[-1])
 window=pol.get('comparison_window') or '/'.join(pol['production_window'].values())
 common=f"{json.dumps(identity)} AS dataset_id, {json.dumps(window)} AS production_window"
 sql=f'''WITH declared AS ({cat_cte}), eligible AS (SELECT numeric_values FROM observations WHERE numeric_values BETWEEN {lo} AND {hi})
SELECT {common}, 'category' AS summary_kind, d.category AS definition, COUNT(o.category) AS observation_count, (SELECT COUNT(*) FROM observations) AS denominator, 1.0*COUNT(o.category)/(SELECT COUNT(*) FROM observations) AS proportion, NULL AS mean, NULL AS standard_deviation, NULL AS ddof FROM declared d LEFT JOIN observations o ON o.category=d.category GROUP BY d.category'''
 if 'declared_classes' in pol:
  cls=' UNION ALL '.join('SELECT '+json.dumps(x)+(' AS category' if i==0 else '') for i,x in enumerate(pol['declared_classes']))
  sql=sql.replace('eligible AS',f'classes AS ({cls}), eligible AS')
  sql+=f" UNION ALL SELECT {common}, 'predicted_class', d.category, COUNT(o.predicted_class), (SELECT COUNT(*) FROM observations), 1.0*COUNT(o.predicted_class)/(SELECT COUNT(*) FROM observations), NULL,NULL,NULL FROM classes d LEFT JOIN observations o ON o.predicted_class=d.category GROUP BY d.category"
 for i,(low,high) in enumerate(zip(edges,edges[1:])):
  comp='<=' if i==len(edges)-2 else '<';definition=f'[{low},{high}'+(']' if comp=='<=' else ')')
  sql+=f" UNION ALL SELECT {common}, 'numeric_bin', {json.dumps(definition)}, SUM(CASE WHEN numeric_values>={low} AND numeric_values{comp}{high} THEN 1 ELSE 0 END), COUNT(*), 1.0*SUM(CASE WHEN numeric_values>={low} AND numeric_values{comp}{high} THEN 1 ELSE 0 END)/COUNT(*),NULL,NULL,NULL FROM eligible"
 sql+=f" UNION ALL SELECT {common}, 'numeric_summary', 'eligible observations', COUNT(*), COUNT(*), NULL, AVG(numeric_values), sqrt(AVG(numeric_values*numeric_values)-AVG(numeric_values)*AVG(numeric_values)), {pol['ddof']} FROM eligible"
 return query(sql,[(a,'observations')],c)

visuals={}
c='mle.distribution_monitoring';pol=policy('distribution_monitoring');visuals[c]=[summary_query('ds.reference',c,pol),summary_query('ds.production',c,pol)]
c='mle.drift_degradation_distinction';visuals[c]=[diagram(c,[(x['supported_evidence'],[x['observation'],x['unresolved']]) for x in rows('ds.evidence_scenarios')],'Three distinct evidence questions')]
c='mle.data_drift_detection';pol=policy('data_drift_detection');visuals[c]=[pair(c,summary_query('ds.reference',c,pol),summary_query('ds.production',c,pol),'Reference','Current','Distribution evidence only; labeled quality remains unresolved.'),code('''import csv, json, numpy as np
policy = json.load(open("policy.json"))
reference = list(csv.DictReader(open("reference.csv")))
current = list(csv.DictReader(open("production.csv")))
def vectors(rows):
    values = np.asarray([float(r["numeric_values"]) for r in rows])
    low, high = policy["eligible_numeric_range"]
    values = values[(values >= low) & (values <= high)]
    return {"category": np.asarray([sum(r["category"] == c for r in rows)/len(rows) for c in policy["declared_categories"]]),
            "numeric_bins": np.histogram(values, bins=policy["fixed_edges"])[0]/len(values)}
a, b = vectors(reference), vectors(current)
for feature in a:
    distance = 0.5 * np.sum(np.abs(a[feature] - b[feature]))
    print(feature, distance, distance > '''+str(float(re.search(r'> ([\d.]+)',pol['criterion']).group(1)))+''')
print(policy["quality_claim"])
''',c)]
c='mle.delayed_label_quality';visuals[c]=[code('''import csv, json, numpy as np
from datetime import datetime, timedelta
policy = json.load(open("policy.json"))
predictions = list(csv.DictReader(open("predictions.csv")))
labels = list(csv.DictReader(open("labels.csv")))
def dt(s): return datetime.fromisoformat(s.replace("Z", "+00:00"))
assert len({r["prediction_id"] for r in predictions}) == len(predictions)
assert len({r["prediction_id"] for r in labels}) == len(labels)
cohort = {r["prediction_id"]: r for r in predictions if r["cohort_id"] == policy["cohort"] and r["eligible"].lower() in ("true", "1")}
cutoff = dt(policy["label_available_through"])
analysis = dt(policy["analysis_time"])
matched = []
for label in labels:
    prediction = cohort.get(label["prediction_id"])
    if prediction is None or dt(label["label_timestamp"]) > cutoff:
        continue  # excluded IDs must also be recorded by the learner
    if analysis-dt(prediction["prediction_timestamp"]) < timedelta(hours=policy["minimum_age_hours"]):
        continue
    matched.append((prediction, label))
print("eligible IDs", len(cohort), "mature matched IDs", len(matched))
print("maturity", len(matched)/len(cohort))
print("matched error proportion", np.mean([p["prediction"] != l["label"] for p,l in matched]))
loss = np.asarray([float(l["loss"]) for p,l in matched])
print("matched loss", len(loss), np.mean(loss), np.std(loss, ddof=policy["ddof"]))
''',c),table('ds.predictions',c),table('ds.labels',c)]
c='mle.actionable_ml_alerts';pol=policy('actionable_ml_alerts');offset=float(re.search(r'\+([\d.]+)',pol['window_rule']).group(1));visuals[c]=[code('''import csv, json, io, yaml, numpy as np
policy = json.load(open("policy.json"))
config = {k: policy[k] for k in ("indicator", "baseline_window", "window_rule", "owner", "response")}
stream = io.StringIO()
yaml.safe_dump(config, stream)
stream.seek(0)
resolved = yaml.safe_load(stream)
assert all(resolved[k] == config[k] for k in config)
rows = list(csv.DictReader(open("alert_observations.csv")))
def values(window): return np.asarray([float(r["numeric_values"]) for r in rows if r["window_id"] == window])
baseline = values(resolved["baseline_window"])
mean, spread = np.mean(baseline), np.std(baseline, ddof=policy["ddof"])
print("baseline", len(baseline), mean, spread)
print("resolved", resolved)
for fixture, expected in policy["expected_replays"].items():
    breach = bool(np.mean(values(fixture)) > mean + '''+str(offset)+''')
    assert breach == expected
    emitted = {"owner": resolved["owner"], "action": resolved["response"]} if breach else None
    print(fixture, "assertion passed", emitted)
''',c)]
c='mle.production_regression_diagnosis';visuals[c]=[query('SELECT *, CASE WHEN matched_eligible_labels > 0 THEN 1.0*labeled_errors/matched_eligible_labels ELSE NULL END AS conditional_error_rate FROM evidence ORDER BY timestamp',[('ds.release_evidence','evidence')],c)]
c='mle.retraining_trigger_policy';stages=rows('ds.pipeline_stages');nodes=[{'id':x['stage_id'],'label':x['stage_id'],'detail':x['purpose']+'; inputs: '+x['required_artifacts'],'kind':'step'} for x in stages];nodes += [{'id':'promotion_approval','label':'Separate promotion approval','kind':'decision'},{'id':'blocked','label':'Failed required check: downstream blocked','kind':'end'}];edges=[{'from':dep.strip(),'to':x['stage_id'],'label':'required success','kind':'next'} for x in stages for dep in x['dependencies'].split(';') if dep.strip()];edges.append({'from':'data_quality_test','to':'blocked','label':'failure','kind':'no'});visuals[c]=[{'type':'process_flow','nodes':nodes,'edges':edges,'alt_text':'Existing dependencies: failure blocks downstream execution; promotion has separate approval.','lineage':lin(c,visual=True)},table('ds.trigger_events',c)]
c='mle.authorized_retraining_execution';pol=policy('authorized_retraining_execution');ids=pol['stage_contract'].split(';')[0].strip().split(' -> ');visuals[c]=[{'type':'process_flow','nodes':[{'id':x,'label':x,'kind':'step'} for x in ids]+[{'id':'reject','label':'Rejected identity, snapshot or fatal gate','kind':'end'}],'edges':[{'from':a,'to':b,'label':'required success','kind':'next'} for a,b in zip(ids,ids[1:])]+[{'from':ids[1],'to':'reject','label':'failure','kind':'no'}],'alt_text':'Verify before invoking; inspect actual consumed input after execution. A failed required gate blocks downstream steps.','lineage':lin(c,visual=True)},table('ds.execution_fixtures',c)]
c='mle.retraining_run_idempotency';visuals[c]=[table('ds.idempotency_traces',c)]
c='mle.retrained_candidate_validation';visuals[c]=[code('''import csv, json
policy = json.load(open("policy.json"))
rows = list(csv.DictReader(open("validation_counts.csv")))
def evaluate(row):
    fp, tn, fn, tp = (int(row[k]) for k in ("FP", "TN", "FN", "TP"))
    fpr = fp/(fp+tn) if fp+tn else None
    fnr = fn/(fn+tp) if fn+tp else None
    cost = None if fpr is None or fnr is None else policy["P_Y0"]*fpr*policy["cost_FP"]+policy["P_Y1"]*fnr*policy["cost_FN"]
    limits = policy["acceptance"]
    quality = cost is not None and fpr <= limits["maximum_FPR"] and fnr <= limits["maximum_FNR"]
    return {"registry_artifact_id": row["registry_artifact_id"], "cohort_id": row["cohort_id"], "FPR": fpr, "FNR": fnr, "expected_cost": cost, "quality_pass": quality,
            "slice_pass": row["slice_pass"].lower() in ("true","1"), "compatibility_pass": row["compatibility_pass"].lower() in ("true","1")}
for fixture in sorted({r["fixture"] for r in rows}):
    group = [r for r in rows if r["fixture"] == fixture]
    incumbent = evaluate(next(r for r in group if r["model_role"] == "incumbent"))
    candidate = evaluate(next(r for r in group if r["model_role"] == "candidate"))
    assert candidate["cohort_id"] == incumbent["cohort_id"]
    cost_pass = candidate["expected_cost"] is not None and incumbent["expected_cost"] is not None and candidate["expected_cost"] <= incumbent["expected_cost"]
    candidate["verdict"] = "accept" if candidate["quality_pass"] and cost_pass and candidate["slice_pass"] and candidate["compatibility_pass"] else "reject"
    assert candidate["verdict"] != "accept" or candidate["slice_pass"] and candidate["compatibility_pass"] and cost_pass
    print(fixture, incumbent, candidate, "assertions passed")
''',c),table('ds.validation_counts',c)]
c='mle.ml_incident_runbook';phases=[x['phase'] for x in rows('ds.incident_evidence')];visuals[c]=[before(c,query('SELECT * FROM evidence WHERE phase='+json.dumps(phases[0]),[('ds.incident_evidence','evidence')],c),query('SELECT * FROM evidence WHERE phase='+json.dumps(phases[1]),[('ds.incident_evidence','evidence')],c),'Authored expected recovery evidence, not proof of learner execution.')]
c='mle.ml_resource_utilization';visuals[c]=[table('ds.resource_telemetry',c),query('''WITH matched AS (SELECT * FROM telemetry WHERE included=1), series AS (SELECT INSTANCE, process_id, 'CPU' AS metric, 'percent' AS unit, timestamp, cpu_percent AS value FROM matched UNION ALL SELECT INSTANCE, process_id, 'memory', memory_unit, timestamp, memory_value FROM matched) SELECT INSTANCE,process_id,metric,unit,MIN(timestamp) AS interval_start,MAX(timestamp) AS interval_end,COUNT(*) AS observation_count,AVG(value) AS mean,sqrt(AVG(value*value)-AVG(value)*AVG(value)) AS standard_deviation,0 AS ddof FROM series GROUP BY INSTANCE,process_id,metric,unit''',[('ds.resource_telemetry','telemetry')],c)]
c='mle.ml_workload_cost_attribution';pol=policy('ml_workload_cost_attribution');mapping=' UNION ALL '.join('SELECT '+json.dumps(k)+(' AS resource_id' if i==0 else '')+', '+json.dumps(v)+(' AS workload' if i==0 else '') for i,(k,v) in enumerate(pol['resource_mapping'].items()));sharing=' UNION ALL '.join('SELECT '+json.dumps(k)+(' AS workload' if i==0 else '')+', '+str(v)+(' AS share' if i==0 else '') for i,(k,v) in enumerate(pol['shared_rule'].items()));
ct=f'''WITH mapping AS ({mapping}), shares AS ({sharing}), allocations AS (SELECT b.charge_id,b.reporting_window,b.resource_id,b.charge_category,COALESCE(m.workload,'unallocated') AS workload,b.amount AS allocation FROM billing b LEFT JOIN mapping m ON b.resource_id=m.resource_id WHERE b.charge_category != 'shared' UNION ALL SELECT b.charge_id,b.reporting_window,b.resource_id,b.charge_category,s.workload,b.amount*s.share FROM billing b CROSS JOIN shares s WHERE b.charge_category='shared')'''
visuals[c]=[table('ds.lifecycle',c),table('ds.billing_export',c),query(ct+' SELECT *, workload=\'unallocated\' AS unmatched FROM allocations ORDER BY reporting_window,workload,charge_id',[('ds.billing_export','billing')],c),query(ct+''' SELECT reporting_window,workload,SUM(allocation) AS window_total,SUM(allocation)>'''+re.search(r'>([\d.]+)',pol['unusual_rule']).group(1)+''' AS unusually_large,(SELECT SUM(amount) FROM billing b WHERE b.reporting_window=a.reporting_window) AS eligible_export_total,(SELECT SUM(allocation) FROM allocations x WHERE x.reporting_window=a.reporting_window) AS reconciled_total FROM allocations a GROUP BY reporting_window,workload''',[('ds.billing_export','billing')],c),query(ct+''', totals AS (SELECT reporting_window,workload,SUM(allocation) AS value FROM allocations GROUP BY reporting_window,workload) SELECT workload,COUNT(*) AS window_count,AVG(value) AS mean,sqrt(AVG(value*value)-AVG(value)*AVG(value)) AS standard_deviation,0 AS ddof FROM totals GROUP BY workload''',[('ds.billing_export','billing')],c)]
c='mle.ml_workload_cost_guardrail';visuals[c]=[before(c,query('SELECT fixture,workload_scope,budget_amount,period,threshold_ratio,observed_spend,INSTANCE,ZONE FROM replay',[('ds.budget_replay','replay')],c),query('SELECT fixture,INSTANCE,ZONE,notification_expected,response_expected,expected_after_state FROM replay',[('ds.budget_replay','replay')],c),'Authored replay expectations; notification and resource response are separate.')]
c='mle.serving_resource_cleanup';evidence=next(f['content'] for f in assets['ws.serving_resource_cleanup']['files'] if f['path']=='cleanup_evidence.csv');er=list(csv.DictReader(io.StringIO(evidence)));after_nodes=[('Expected '+x.get('phase','')+' cleanup evidence',[k+': '+v for k,v in x.items() if k!='phase']) for x in er if x.get('phase')=='after'];visuals[c]=[before(c,table('ds.cleanup_inventory',c),diagram(c,after_nodes,'Authored expected post-cleanup evidence'),'Expected fixture evidence: preserve active health and shared artifacts; verify retired-resource absence.')]

out={k:p[k] for k in ['schema_version','path_id','batch_id']};out['kind']='screens_part';out['tiles']=[]
titles=['Align production distributions','Labels, alerts and regression diagnosis','Execute quality-gated retraining','Use an ML incident runbook','Control workload cost and retire resources']
recaps={
'mle.tile.080_082':'Keep reference representations and window denominators aligned. Distinguish input distributions, conditional relationships and matched-label quality. Apply the predeclared drift rule without treating drift alone as measured prediction error.',
'mle.tile.083_085':'Preserve prediction IDs, timestamps and mature-cohort denominators. Inspect alert configuration and replay its rule. Diagnose from impact, identity and evidence; test a hypothesis before choosing the supported response.',
'mle.tile.086_089':'Bind triggers to evidence, authorization and intended data. Verify actual immutable-input consumption. Preserve one durable job identity through retries. Validate the exact candidate under every required gate; promotion remains separately authorized.',
'mle.tile.090_090':'Record authorized identity and fault evidence before runbook recovery. Stop/wait/start/wait on the same instance, reconnect, then verify readiness and bounded predictions. Runtime credentials stay out of code, configuration and captured output.',
'mle.tile.091_094':'Align telemetry with active workload identity and units. Reconcile direct, shared and unallocated billing charges. Test notification and authorized budget response without claiming a hard cap. Retire only verified resources while preserving active health, required artifacts and credential confidentiality.'}
for ti,t in enumerate(p['tiles']):
 tile={'tile_id':t['tile_id'],'title':titles[ti],'steps':[],'remediation_steps':[]}
 for s in t['steps']:
  c=s['concept_ids'][0];bundle=bs[c];short=c.split('.')[1];L={'concept_ids':s['concept_ids'],'teaching_block_ids':s['teaching_block_ids'],'fact_ids':s['fact_ids'],'anchors':s['anchors']}
  step={'step_id':s['step_id'],'type':s['type'],'concept_ids':s['concept_ids'],'title':bundle['context']['concept_name'],'eyebrow':{'explainer':'Understand','video':'Watch','check':'Check','hands_on':'Practice','recap':'Takeaways'}[s['type']],'lineage':L}
  if s['type']=='explainer':
   blocks=[];tbmap={c+'#'+x['id']:x for x in bundle['teaching_blocks']}
   for q in s['teaching_block_ids']:
    tb=tbmap[q];BL=lin(c,[q],[c+'#'+f for f in tb['fact_ids']]);content=tb['content']
    if tb['purpose']=='intro':continue
    if tb['purpose']=='example':content=examples[short]
    elif tb['purpose'] not in ['misconception','intro'] and tb['fact_ids']:
     fm={f['id']:f['statement'] for f in bundle['coverage']['required_facts']}
     for f in tb['fact_ids']:
      blocks+=split_prose(voice(fm[f]),lin(c,[q],[c+'#'+f]),'definition')
     continue
    else:content=voice(content)
    blocks+=split_prose(content,BL,tb['purpose'] if tb['purpose'] in ['intro','definition','mechanism','example','misconception'] else 'workflow')
   if not blocks:
    for q in s['teaching_block_ids']:
     tb=tbmap[q];blocks+=split_prose(voice(tb['content']),lin(c,[q],[c+'#'+f for f in tb['fact_ids']]),'intro')
   # Preserve all planned teaching-block identities even for the skipped framing intro.
   intro_ids=[q for q in s['teaching_block_ids'] if tbmap[q]['purpose']=='intro']
   if intro_ids:blocks[0]['lineage']['teaching_block_ids']=intro_ids+blocks[0]['lineage']['teaching_block_ids']
   step['title']=('Use the fixture contract' if s['planned_visual_block_type'] else tbmap[s['teaching_block_ids'][0]]['title'])
   step['blocks']=blocks+(copy.deepcopy(visuals[c]) if s['planned_visual_block_type'] else [])
  elif s['type']=='video':step['blocks']=[{'type':'media_group','segment_ids':s['segment_ids']}]
  elif s['type']=='recap':
   step['title']=titles[ti]+' — recap';RL={'concept_ids':s['concept_ids'],'teaching_block_ids':[],'fact_ids':[]}
   # Recap lineage points to the facts the takeaway actually reiterates, not new teaching.
   for cc in s['concept_ids']:
    RL['teaching_block_ids'] += [cc+'#'+tb['id'] for tb in bs[cc]['teaching_blocks'] if tb['purpose']=='misconception']
    RL['fact_ids'] += [cc+'#'+f for tb in bs[cc]['teaching_blocks'] if tb['purpose']=='misconception' for f in tb['fact_ids']]
   RL['fact_ids']=list(dict.fromkeys(RL['fact_ids']))
   step['blocks']=[prose(recaps[t['tile_id']],RL,'takeaway')]
   if t.get('next_tile_id'):
    nt=next(x for x in p['tiles'] if x['tile_id']==t['next_tile_id']);idea=bs[nt['steps'][0]['concept_ids'][0]]['context']['concept_name'];step['blocks'].append({'type':'up_next','title':'Up next: '+idea})
   else:step['blocks'].append({'type':'up_next','title':'Path complete','text':'This is the final tile in the supplied path.'})
  else:
   step['title']=('Check: ' if s['type']=='check' else 'Practice: ')+bundle['context']['concept_name']
   step['lede']='Use the supplied fictional fixture and its declared policy.'
  tile['steps'].append(step)
  if s['type'] in ['check','hands_on']:
   # Separate fact-set remediation for each assessed framing step, ready for stage 04 routing.
   rid=t['tile_id']+'.r'+str(len(tile['remediation_steps'])+1).zfill(2)
   factmap={c+'#'+f['id']:f['statement'] for f in bundle['coverage']['required_facts']}
   rtbs=[c+'#'+tb['id'] for tb in bundle['teaching_blocks'] if any(c+'#'+f in s['fact_ids'] for f in tb['fact_ids'])]
   blocks=[]
   for fid in s['fact_ids']:
    relevant=[c+'#'+tb['id'] for tb in bundle['teaching_blocks'] if fid.split('#')[1] in tb['fact_ids'] and tb['purpose']!='example']
    blocks+=split_prose(voice(factmap[fid]),lin(c,relevant,[fid]),'definition')
   contrast=next((tb for tb in reversed(bundle['teaching_blocks']) if tb['purpose']=='misconception'),None)
   if contrast:blocks+=split_prose(voice(contrast['content']),lin(c,[c+'#'+contrast['id']],[c+'#'+f for f in contrast['fact_ids']]),'misconception')
   # Context is the same registered dataset, not a second invented example.
   data=next((a for a in {'distribution_monitoring':'ds.production','drift_degradation_distinction':'ds.evidence_scenarios','data_drift_detection':'ds.production','delayed_label_quality':'ds.predictions','actionable_ml_alerts':'ds.alert_observations','production_regression_diagnosis':'ds.release_evidence','retraining_trigger_policy':'ds.trigger_events','authorized_retraining_execution':'ds.execution_fixtures','retraining_run_idempotency':'ds.idempotency_traces','retrained_candidate_validation':'ds.validation_counts','ml_incident_runbook':'ds.incident_evidence','ml_resource_utilization':'ds.resource_telemetry','ml_workload_cost_attribution':'ds.billing_export','ml_workload_cost_guardrail':'ds.budget_replay','serving_resource_cleanup':'ds.cleanup_inventory'}.get(short,'').split() if a),None)
   if data:blocks.append(table(data,c,lin(c,rtbs,s['fact_ids'],visual=True)))
   tile['remediation_steps'].append({'step_id':rid,'type':'remediation','concept_ids':[c],'title':'Try the contrast: '+bundle['context']['concept_name'],'eyebrow':'Review','lede':'Return to the same supplied fixture before retrying.','lineage':lin(c,rtbs,s['fact_ids']),'blocks':blocks})
 out['tiles'].append(tile)
(B/'screens.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('Wrote screens.json:',len(out['tiles']),'tiles',sum(len(t['steps']) for t in out['tiles']),'planned steps',sum(len(t['remediation_steps']) for t in out['tiles']),'remediations')
for tile,t in zip(out['tiles'],p['tiles']):
 for s,ps in zip(tile['steps'],t['steps']):
  count=sum(len(b['text'].split()) for b in s.get('blocks',[]) if b['type']=='prose')
  if count>ps['word_budget'] and ps['word_budget']: print('OVER',s['step_id'],count,ps['word_budget'])
