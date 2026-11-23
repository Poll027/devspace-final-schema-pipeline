import json,sys,pathlib,copy
B=pathlib.Path('batches/final_batch_mle.region.production_operations'); CORE=pathlib.Path('00_FINAL_PIPELINE_CORE');sys.path.insert(0,str(CORE/'scripts'))
from checkers import sandbox,pysyntax
P=json.load(open(B/'tile_plans.json')); S=json.load(open(B/'screens.json'));G=json.load(open(B/'inputs/path_glossary_bundle.json'));R=json.load(open(B/'scenario_asset_registry.json'))
g={x['context']['concept_id']:x for x in G['bundles']};assets={a['asset_id']:a for a in R['assets']}
def rows(a):
 a=assets[a];names=[c['name'] for c in a['columns']];return [dict(zip(names,r)) if isinstance(r,list) else r for r in a['rows']]
def policy(c):return json.loads(next(f['content'] for f in assets['ws.'+c.split('.')[1]]['files'] if f['path']=='policy.json'))
def msg(s):return {'message':s}
checks={
'distribution_monitoring':('You need descriptive spread for every eligible value in a production window. Which divisor matches np.std(values, ddof=0)?','N, the number of eligible values.','N−1, regardless of the stated ddof.','ddof=0 divides squared deviations by N; N−1 requires ddof=1.'),
'drift_degradation_distinction':('Input proportions changed, but no matched labels or declared quality reference are available. Which conclusion is supported?','There is input distribution shift; quality loss and conditional relationship change remain unestablished.','All three—input drift, concept drift and quality loss—are proven.','Evidence about P(X) alone does not establish a P(Y|X) change or matched-label quality degradation.'),
'data_drift_detection':('A feature exceeds its declared aligned probability-distance threshold. No matched labels are available. What does this establish?','A feature-level distribution difference under the declared rule, not prediction-quality loss.','A measured increase in prediction errors.','A distribution-only rule detects input differences; quality loss needs matched-label evidence.'),
'delayed_label_quality':('For the supplied mature matched labeled losses, the contract calls for np.std(losses, ddof=0). Which report is defensible?','Report mean loss and spread with divisor N, scoped to the mature matched cohort.','Use divisor N−1 and describe the result as established quality for all traffic.','ddof=0 uses N, and immature traffic is not included in the mature-label estimate.'),
'actionable_ml_alerts':('Replay has a normal window and a qualifying breach. What owner/action output should the breach-only interface emit?','No breach record for the normal window; the configured owner and response for the qualifying breach.','The same breach owner/action record for every replayed window.','Breach-only output must distinguish normal windows from a qualifying breach and resolve the configured owner/action.'),
'production_regression_diagnosis':('Investigation supports the supplied rollback response. What is still required before treating the rollback as restored service?','The required readiness and bounded prediction validation gates.','Nothing: choosing an approved rollback proves recovery.','Response selection does not substitute for the supplied validation gates.'),
'retraining_trigger_policy':('Where should handoff credential values reside in the supplied pipeline policy?','Only in runtime-resolved secrets; policy and captured logs contain references, not values.','Copy credential values into the YAML and logs to make the handoff reproducible.','The permitted handoff keeps secret values out of policy, YAML and captured logs.'),
'authorized_retraining_execution':('A build step needs an injected execution credential. Which configuration and evidence respects the supplied boundary?','Use its Secret Manager version reference and step-scoped secretEnv; captured output contains no value.','Embed the resolved value in args and print it to prove the step received it.','The reference and scoped binding provide runtime injection without disclosing credentials.'),
'retraining_run_idempotency':('Required admission and function-test steps appear before execute in YAML. What actually prevents launch after admission failure?','Explicit successful-step waitFor dependencies and fatal required gates.','Textual order alone, with admission failure allowed.','Required gates must succeed through explicit dependencies; YAML position alone is not enforcement.'),
'retrained_candidate_validation':('A candidate passes cost and quality but its recorded artifact differs from the artifact being promoted. Which gate outcome is required?','Reject the identity mismatch even though those other gates passed.','Accept because cost and quality override candidate identity.','The verdict is bound to the evaluated artifact; it does not approve another identity.'),
'ml_incident_runbook':('After an authorized same-instance restart, describe reports RUNNING. What additional recovery evidence is required?','Restored model-service readiness and a bounded prediction exchange that meets the contract.','None: RUNNING guarantees a healthy model service.','Instance state alone does not verify model-service readiness or prediction behavior.'),
'ml_resource_utilization':('A matched running-workload interval has persistently high CPU with evidence of saturation. What is the bounded conclusion?','Identify saturation for that workload and interval using the matched resource observations.','Describe all resources as saturated, including stopped and unrelated observations.','Utilization conclusions retain workload identity and interval; stopped and unrelated samples are excluded.'),
'ml_workload_cost_attribution':('An eligible export includes shared and unmatched charges. Which reconciliation is valid?','Allocated plus explicitly unallocated amounts equal the eligible export total; shared charges follow the supplied rule.','Drop shared and unmatched amounts, then reconcile only direct charges.','Shared and unmatched eligible amounts remain accounted for rather than disappearing from reconciliation.'),
'ml_workload_cost_guardrail':('The configured budget event response can stop a fixed approved test instance. Is its budget amount a hard cap?','No. Delayed notifications permit spending to exceed the amount.','Yes. The response guarantees spending cannot exceed the budget.','Budget notifications can lag actual usage, so the record must state the residual limitation.'),
'serving_resource_cleanup':('Post-cleanup, the active release is healthy and retired resources are absent. What must the single audit record also retain?','Verified ownership and identities, authorization, inspection/actions, retained artifacts and credential non-disclosure review.','Only resource ages, because older resources are eligible for deletion.','Cleanup eligibility follows verified authorization and lifecycle identity, and the audit retains the required evidence rather than ages alone.')}
# Runtime scaffolding: parse supplied datasets; no calculated outputs in the starter.
BASE='''import csv, json, datetime
import numpy as np
SCHEMAS = __SCHEMAS__
def load(name):
    with open(name+'.csv') as f:
        data=list(csv.DictReader(f))
    for r in data:
        for k,t in SCHEMAS[name].items():
            v=r[k]
            r[k] = None if v=='' else (v=='True' if t=='boolean' else int(v) if t=='integer' else float(v) if t=='number' else v)
    return data
def column(data,key):
    return np.asarray([r[key] for r in data])
def emit(value):
    return value
'''
code_ix=[]
def code(c,prompt,mount_ids,pre,work,post,extra='',packages=['numpy']):
 schemas={a.split('.')[1]:{co['name']:co['type'] for co in assets[a]['columns']} for a in mount_ids}
 lib=BASE.replace('__SCHEMAS__',repr(schemas))+extra
 starter=pre+'\n# Complete the calculations below; retain the supplied report contract.\n'+'\n'.join(n+' = None' for n,e in work)+'\n'+post
 solution=pre+'\n'+'\n'.join(n+' = '+e for n,e in work)+'\n'+post
 live=g[c]['practice_anchor']['live_code']
 pub={'prompt':prompt,'runtime':{'kind':'python','version':sandbox.RUNTIMES['python']['version'],'packages':packages},'workspace':{'entry':'main.py','files':[{'path':'main.py','role':'editable','language':'python','content':starter},{'path':'lab.py','role':'readonly','language':'python','content':lib}], 'asset_mounts':[{'asset_id':a,'mount_path':a.split('.')[1]+'.csv'} for a in mount_ids]},'constraints':{k:live[k] for k in ['allowed_syntax','blocked_syntax']}}
 ix={'type':'code_exercise','public':pub,'grading':{'solution_files':[{'path':'main.py','content':solution}],'tests':[{'test_id':'report','kind':'value_equals','spec':{'expr':'report','expected':None}}]}}
 code_ix.append(ix)
 return ix
# Reordering scaffold command/interface calls: supplied Python wrappers model operations; no shell/network.
def reorder(c,prompt,mount_ids,pre,lines,extra,post='report = lab.report()\n',packages=['numpy']):
 ix=code(c,prompt,mount_ids,pre,[],post,extra,packages)
 ix['public']['workspace']['files'][0]['content']=pre+'\n# Reorder the supplied operations. Do not change target arguments.\n'+'\n'.join(list(reversed(lines)))+'\n'+post
 ix['grading']['solution_files'][0]['content']=pre+'\n'+'\n'.join(lines)+'\n'+post
 return ix
C={}
c='mle.distribution_monitoring'; pol=policy(c)
C[c]=code(c,'Complete the single monitoring record for reference.csv and production.csv. Use the supplied reference and production window, fixed edges and declared category/class order. Include numeric eligible counts, bin proportions, category and predicted-class probabilities including absent categories, and numeric mean/std with ddof=0 for each window. Retain definitions and totals. Do not infer quality loss.', ['ds.reference','ds.production'], 'from lab import *\npolicy = '+repr(pol)+'''\nreference = load('reference')
production = load('production')
r = column(reference,'numeric_values')
p = column(production,'numeric_values')
rc = column(reference,'category')
pc = column(production,'category')
rpred = column(reference,'predicted_class')
ppred = column(production,'predicted_class')
fixed_edges = np.asarray(policy['fixed_edges'])
category_names = np.asarray(policy['categories'])
class_names = np.asarray(policy['predicted_classes'])
''', [('r_count','len(r)'),('p_count','len(p)'),('r_bins','np.histogram(r, bins=fixed_edges)[0] / r_count'),('p_bins','np.histogram(p, bins=fixed_edges)[0] / p_count'),('r_category','np.sum(rc[:, None] == category_names, axis=0) / len(rc)'),('p_category','np.sum(pc[:, None] == category_names, axis=0) / len(pc)'),('r_class','np.sum(rpred[:, None] == class_names, axis=0) / len(rpred)'),('p_class','np.sum(ppred[:, None] == class_names, axis=0) / len(ppred)'),('r_mean','np.mean(r)'),('p_mean','np.mean(p)'),('r_std','np.std(r, ddof=0)'),('p_std','np.std(p, ddof=0)')], "report = {'definitions':policy,'reference':{'eligible':r_count,'bins':r_bins,'category':r_category,'classes':r_class,'mean':r_mean,'std':r_std},'production':{'eligible':p_count,'bins':p_bins,'category':p_category,'classes':p_class,'mean':p_mean,'std':p_std}}\n")
# Matrix counts are infrastructural alignment; learner computes denominators, probabilities, distance and decisions.
c='mle.data_drift_detection';pol=policy(c)
extra='''
def aligned_counts(data,names):
    return np.asarray([np.count_nonzero(column(data,'category')==k) for k in names])
'''
C[c]=code(c,'Complete the feature drift report for the aligned reference and production fixtures. Preserve the supplied reference/window, categories, bin edges and eligibility. Calculate numerical mean and population std for each; normalize aligned category counts by each window total; calculate sum(abs(p_prod-p_ref)) and flag it using the supplied strict distance rule. Calculate the numeric mean difference and apply its declared threshold. Return both feature decisions; detected drift is distribution difference, not quality loss.', ['ds.reference','ds.production'], 'from lab import *\npolicy = '+repr(pol)+'''\nreference = load('reference')
production = load('production')
r = column(reference,'numeric_values')
p = column(production,'numeric_values')
r_total = len(reference)
p_total = len(production)
r_counts = aligned_counts(reference,policy['categories'])
p_counts = aligned_counts(production,policy['categories'])
''', [('r_mean','np.mean(r)'),('p_mean','np.mean(p)'),('r_std','np.std(r, ddof=0)'),('p_std','np.std(p, ddof=0)'),('r_prob','r_counts / r_total'),('p_prob','p_counts / p_total'),('distance','np.sum(np.abs(p_prob-r_prob))'),('numeric_distance','np.abs(p_mean-r_mean)'),('category_drift',"distance > policy['category_distance_threshold']"),('numeric_drift',"numeric_distance > policy['numeric_mean_difference_threshold']")], "report = {'definitions':policy,'r_total':r_total,'p_total':p_total,'r_mean':r_mean,'p_mean':p_mean,'r_std':r_std,'p_std':p_std,'r_prob':r_prob,'p_prob':p_prob,'category_distance':distance,'numeric_distance':numeric_distance,'category_drift':category_drift,'numeric_drift':numeric_drift,'interpretation':'distribution difference only'}\n",extra)
# Delayed-label join is performed by learner code; timestamp boundary and maturity helper supplied.
c='mle.delayed_label_quality';pol=policy(c)
extra='''
def mature(pred,label,policy):
    cutoff=datetime.datetime.fromisoformat(policy['evaluation_cutoff'].replace('Z','+00:00'))
    pt=datetime.datetime.fromisoformat(pred['prediction_timestamp'].replace('Z','+00:00'))
    lt=datetime.datetime.fromisoformat(label['label_timestamp'].replace('Z','+00:00'))
    return lt<=cutoff and (cutoff-pt).total_seconds()>=policy['maturity_hours']*3600
'''
# main loop blocks have exact teaching syntax; construct directly later.
C[c]=code(c,'Implement the fixed prediction cohort join and its mature-label report. Preserve original prediction timestamps and membership. Reject duplicate label IDs, list unmatched labels, exclude labels after the cutoff or predictions below maturity age, and retain all eligible cohort IDs in the coverage denominator. Compute matched errors/eligible mature IDs and mean/std(ddof=0) of mature losses. Scope the result to mature matched traffic, not all traffic.', ['ds.predictions','ds.labels'], 'from lab import *\npolicy = '+repr(pol)+"\npredictions = load('predictions')\nlabels = load('labels')\n",[], 'report = result\n',extra)
# Alerts YAML and replay supplied runtime, learner authors rule.
c='mle.actionable_ml_alerts';pol=policy(c)
extra='''
def replay(config,data):
    windows={}
    for r in data: windows.setdefault(r['window_id'],[]).append(r['numeric_values'])
    return [{'window':k,'owner':config['owner'],'response':config['response']} for k,v in windows.items() if k!='baseline' and np.mean(v)>config['threshold']]
'''
C[c]=code(c,'Compute baseline mean and population std from alert_observations.csv. Author the supplied owner/response YAML with threshold baseline mean plus the declared margin, safely dump and reload it. The rule is strict >: assert false below and at equality, true above. Replay all windows and return statistics, reloaded config and breach-only owner/action records.', ['ds.alert_observations'], 'from lab import *\nimport yaml\npolicy = '+repr(pol)+"\ndata = load('alert_observations')\nbaseline = np.asarray([r['numeric_values'] for r in data if r['window_id']=='baseline'])\n", [('mean','np.mean(baseline)'),('std','np.std(baseline, ddof=0)'),('threshold',"mean + policy['margin']"),('config',"{'threshold': threshold, 'owner': policy['owner'], 'response': policy['response'], 'ddof': 0}" )], '''with open('alert.yaml','w') as file_handle:
    yaml.safe_dump(config, file_handle)
with open('alert.yaml') as file_handle:
    loaded = yaml.safe_load(file_handle)
assert (threshold-1 > threshold) == False
assert (threshold > threshold) == False
assert (threshold+1 > threshold) == True
records = replay(loaded,data)
report = {'mean':mean,'std':std,'config':loaded,'records':records}
''',extra,packages=['numpy','pyyaml'])
# Regression structured rows retained with evidence, learner calculations and policy response.
c='mle.production_regression_diagnosis';pol=policy(c)
C[c]=code(c,'For every release/cohort in release_evidence.csv, retain client impact/time, compare active versus approved artifact and config, retain schema and distinguishing hypothesis evidence, and compute errors/mature eligible labels only when that denominator is nonzero (otherwise unavailable). Select the supplied evidence-supported response and include its required validation gates. Class mix alone never proves quality loss.', ['ds.release_evidence'], 'from lab import *\npolicy = '+repr(pol)+"\ndata = load('release_evidence')\n",[], 'report = results\n')
# Candidate validation complete function main loop, with scaffolding parser only.
c='mle.retrained_candidate_validation';pol=policy(c)
C[c]=code(c,'Validate every candidate fixture against its incumbent on the same declared validation cohort. Compute FPR=FP/(FP+TN), FNR=FN/(FN+TP), and P(Y=0)*FPR*cost_FP+P(Y=1)*FNR*cost_FN; empty groups are undefined and reject. Accept only if cost is no above incumbent and all quality, slice, compatibility and exact identity gates pass. Record exact candidate identity, cohort, rates, cost and verdict. Exercise valid, boundary, failing and identity-mismatch cases using the supplied fixtures; never access protected test data.', ['ds.validation_counts'], 'from lab import *\npolicy = '+repr(pol)+"\ndata = load('validation_counts')\n",[], 'report = results\n')
# Utilization input arrays: learner masks and summaries.
c='mle.ml_resource_utilization';pol=policy(c)
C[c]=code(c,'Select only running observations for the supplied instance/model process in [interval_start,interval_end_exclusive). Match CPU and memory on that same mask, exclude stopped and unrelated rows, and report counts, CPU percent, memory MiB, means and population std(ddof=0). Keep identity and interval in the single summary. Identify only workload-local utilization, not every machine.', ['ds.resource_telemetry'], 'from lab import *\npolicy = '+repr(pol)+'''\ndata = load('resource_telemetry')
instance = column(data,'INSTANCE')
process = column(data,'process_id')
running_process = column(data,'running_process')
state = column(data,'instance_state')
time = column(data,'timestamp')
cpu_all = column(data,'cpu_percent')
memory_all = column(data,'memory_value')
''',[('mask',"(instance == policy['INSTANCE']) & (process == policy['process_id']) & (running_process == policy['process_id']) & (state == 'RUNNING') & (time >= policy['interval_start']) & (time < policy['interval_end_exclusive'])"),('cpu','cpu_all[mask]'),('memory','memory_all[mask]'),('count','len(cpu)'),('cpu_mean','np.mean(cpu)'),('cpu_std','np.std(cpu, ddof=0)'),('memory_mean','np.mean(memory)'),('memory_std','np.std(memory, ddof=0)')],"report = {'scope':policy,'count':count,'cpu_mean':cpu_mean,'cpu_std':cpu_std,'memory_mean':memory_mean,'memory_std':memory_std}\n")
# Simulator operation ordering: main calls all supplied, but only correct ordering completes state transitions.
c='mle.ml_incident_runbook';pol=policy(c)
extra='''
class Recovery:
    def __init__(self,data,policy): self.data=data; self.policy=policy; self.trace=[]; self.state='initial'
    def step(self,action,required,next_state):
        if self.state!=required: raise ValueError('operation lacks required prior evidence/completion')
        self.trace.append(action); self.state=next_state
    def describe_before(self): self.step('gcloud compute instances describe '+self.policy['INSTANCE']+' --zone='+self.policy['ZONE'],'initial','inspected')
    def reproduce_and_test(self): self.step('gcloud compute ssh; preserve fault evidence and test runbook hypothesis','inspected','tested')
    def stop_and_wait(self): self.step('gcloud compute instances stop; confirm TERMINATED','tested','stopped')
    def start_and_wait(self): self.step('gcloud compute instances start; confirm RUNNING','stopped','started')
    def reconnect(self): self.step('gcloud compute ssh same target','started','connected')
    def verify_service(self): self.step('readiness and bounded prediction; credential review','connected','verified')
    def describe_after(self): self.step('gcloud compute instances describe same target','verified','done')
    def report(self):
        if self.state!='done': raise ValueError('incomplete recovery')
        before=self.data[0]; after=self.data[-1]
        return {'target':self.policy,'pre_fault':before['fault_evidence'],'hypothesis':before['hypothesis_result'],'trace':self.trace,'after':after,'credentials':'runtime references only','scope':'fixture-backed simulator, not live cloud evidence'}
'''
C[c]=reorder(c,'This Python workspace supplies fixture-backed wrappers for the taught gcloud commands; it never runs a shell or touches live resources. Reorder the existing operations (keep their arguments) to inspect authorized identity/target, preserve and reproduce fault evidence and test the runbook hypothesis, stop and confirm stopped before start, confirm running, reconnect, verify readiness/bounded prediction/non-disclosure, and inspect the same target afterward. Return the single recovery record.', ['ds.incident_evidence'],'from lab import *\npolicy = '+repr(pol)+"\nlab = Recovery(load('incident_evidence'),policy)\n",['lab.describe_before()','lab.reproduce_and_test()','lab.stop_and_wait()','lab.start_and_wait()','lab.reconnect()','lab.verify_service()','lab.describe_after()'],extra)
# Cleanup modeled operations verify exclusivity from runtime evidence, never ages.
c='mle.serving_resource_cleanup';pol=policy(c)
extra='''
class Cleanup:
    def __init__(self,data,policy): self.data=data; self.policy=policy; self.trace=[]; self.state='initial'; self.retired=None
    def step(self,name,req,nxt):
        if self.state!=req: raise ValueError('unsafe cleanup order')
        self.trace.append(name);self.state=nxt
    def inspect_inventory_and_logs(self):
        self.retired=[r for r in self.data if r['owner_label']==self.policy['authorized_owner'] and r['NAME']==self.policy['retired_container'] and r['INSTANCE']==self.policy['retired_instance'] and r['ZONE']==self.policy['ZONE'] and r['approved_inventory']=='retired' and r['exclusively_retired']]
        if len(self.retired)!=1: raise ValueError('retirement not verified')
        self.step('docker inspect and logs; describe compute; reconcile labels, release, state, ownership','initial','verified')
    def stop_retired_container(self): self.step('docker container stop '+self.retired[0]['NAME'],'verified','stopped')
    def remove_stopped_container(self): self.step('docker container rm '+self.retired[0]['NAME'],'stopped','removed')
    def delete_retired_instance_preserve_disks(self): self.step('gcloud compute instances delete '+self.retired[0]['INSTANCE']+' --zone='+self.policy['ZONE']+'; '+self.policy['disk_policy'],'removed','deleted')
    def inspect_absence_and_active_health(self): self.step('describe confirms retired absence; active readiness and bounded prediction; artifacts retained','deleted','checked')
    def review_credentials_and_audit(self): self.step('review captured commands and logs; runtime references only; write audit','checked','done')
    def report(self):
        if self.state!='done':raise ValueError('incomplete cleanup')
        active=[r for r in self.data if r['approved_inventory']=='active']
        return {'authorization':self.policy,'runtime_retired_identity':self.retired,'active_retained':active,'actions':self.trace,'retired_absent':True,'artifacts_retained':self.policy['required_retained_artifacts'],'postchecks':self.policy['required_postchecks'],'credentials':'no literal values; runtime injection','scope':'fixture-backed command simulator'}
'''
C[c]=reorder(c,'Reorder the supplied fixture-backed Docker/gcloud operations; this Python simulator executes no shell and has no live credentials. Establish permitted identity, actual ownership/release labels, running/exit state, logs and exclusive retirement before actions. Stop the verified retired container before rm; delete only the verified retired instance preserving attached disks. Preserve the healthy active release and shared artifacts, verify absence/readiness/bounded prediction, review captured output and write one audit. Keep supplied fixed target arguments unchanged.', ['ds.cleanup_inventory'],'from lab import *\npolicy = '+repr(pol)+"\nlab = Cleanup(load('cleanup_inventory'),policy)\n",['lab.inspect_inventory_and_logs()','lab.stop_retired_container()','lab.remove_stopped_container()','lab.delete_retired_instance_preserve_disks()','lab.inspect_absence_and_active_health()','lab.review_credentials_and_audit()'],extra)
# Cost attribution: simulator supplies lifecycle wrappers only, learner allocates and summarizes.
c='mle.ml_workload_cost_attribution';pol=policy(c)
extra='''
def verified_lifecycles(data):
    records=[]
    for r in data:
        if r['before_state']!='TERMINATED' or r['after_state']!='TERMINATED':raise ValueError('lifecycle not stopped')
        records.append({'identity':r['INSTANCE'],'ZONE':r['ZONE'],'window':r['reporting_window'],'start':r['start'],'stop':r['stop'],'work':r['completed_work'],'trace':['describe before','start and wait running','ssh and bounded workload','stop and wait stopped','describe after']})
    return records
'''
C[c]=code(c,'Use the supplied simulator lifecycle evidence for both authorized training/inference instances and retain their inspection/start/connect/bounded-work/stop/inspection records. Allocate eligible direct and persistent-disk rows using the declared mapping and intervals; allocate shared rows by the supplied shares; explicitly retain unmatched amounts as unallocated. Report per-workload/window attributed costs, mean/std(ddof=0) across each workload series, corresponding unit cost, unusual allocations under the supplied criterion, and reconciliation allocated+unallocated=eligible export. No live cloud action is performed here.', ['ds.lifecycle','ds.billing_export'],'from lab import *\npolicy = '+repr(pol)+"\nlifecycles = verified_lifecycles(load('lifecycle'))\ncharges = load('billing_export')\n",[], 'report = result\n',extra)
# Budget safe YAML authored; runtime replay follows target only.
c='mle.ml_workload_cost_guardrail';pol=policy(c)
extra='''
def budget_replay(config,data):
    outputs=[]
    for row in data:
        breached=row['observed_spend']>=config['budget_amount']*config['threshold_ratio']
        outputs.append({'fixture':row['fixture'],'observed_spend':row['observed_spend'],'notified':breached,'topic':config['notification_topic'] if breached else None,'executed':('gcloud compute instances stop '+config['INSTANCE']+' --zone='+config['ZONE']) if breached else None,'before':{'INSTANCE':config['INSTANCE'],'ZONE':config['ZONE'],'state':'RUNNING'},'after':{'INSTANCE':config['INSTANCE'],'ZONE':config['ZONE'],'state':'TERMINATED' if breached else 'RUNNING'},'credentials':'runtime Secret Manager reference; captured output reviewed'})
    return outputs
'''
C[c]=code(c,'Author and safely reload the fixed-target budget response YAML using every supplied policy field. Verify workload scope, amount, monthly period, threshold, existing Pub/Sub binding, authorized identity and Secret Manager reference; never write a credential value. Replay below, equality and breach rows: predicate is spend>=amount*ratio. Retain notification and same-target stop evidence with before/after descriptions and non-disclosure review. Return config, replay evidence and the stated delayed-notification limitation; no hard cap or live resource operation is claimed.', ['ds.budget_replay'],'from lab import *\nimport yaml\npolicy = '+repr(pol)+"\ndata = load('budget_replay')\n",[('config','policy')],'''with open('budget.yaml','w') as file_handle:
    yaml.safe_dump(config, file_handle)
with open('budget.yaml') as file_handle:
    loaded = yaml.safe_load(file_handle)
outputs = budget_replay(loaded,data)
report = {'config':loaded,'replay':outputs,'limitation':policy['residual_limitation']}
''',extra,packages=['numpy','pyyaml'])
# Atomic admission/executor are supplied infrastructure, exercise their ordering across independent restart/concurrency cases.
c='mle.retraining_run_idempotency';pol=policy(c)
extra='''
class AdmissionLab:
    def __init__(self,events,policy): self.events=events;self.policy=policy;self.phase=0;self.evidence=[];self.records={};self.slot=None;self.jobs={}
    def reserve(self,key,pipeline):
        if key in self.records:return self.records[key], 'duplicate'
        if self.slot is not None:return None,'busy'
        job='job.'+key;self.records[key]={'key':key,'pipeline':pipeline,'job_id':job,'terminal':False};self.slot=key
        return self.records[key],'accepted'
    def invoke(self,record):self.jobs.setdefault(record['job_id'],'running')
    def concurrency_and_reservation(self):
        if self.phase!=0:raise ValueError('must reserve first')
        key=self.policy['event']['run_key'];pipe=self.policy['event']['pipeline']
        first,status=self.reserve(key,pipe);second,dup=self.reserve(key,pipe);other,busy=self.reserve(key+'2',pipe)
        assert status=='accepted' and dup=='duplicate' and first['job_id']==second['job_id'] and busy=='busy'
        self.evidence.append({'case':'concurrent admission','record':dict(first),'duplicate':dup,'different_key':busy,'logical_jobs':len(self.jobs)});self.phase=1
    def restart_and_launch(self):
        if self.phase!=1:raise ValueError('reservation missing')
        key=self.policy['event']['run_key'];record,status=self.reserve(key,self.policy['event']['pipeline'])
        self.invoke(record);self.evidence.append({'case':'fresh worker after reservation','job_id':record['job_id'],'logical_jobs':len(self.jobs)});self.phase=2
    def unknown_response_reconcile(self):
        if self.phase!=2:raise ValueError('no persisted launch')
        record=self.records[self.policy['event']['run_key']];self.invoke(record)
        assert len(self.jobs)==1
        self.evidence.append({'case':'restart after launch and unknown response','job_id':record['job_id'],'logical_jobs':len(self.jobs)});self.phase=3
    def confirm_terminal_and_release(self):
        if self.phase!=3:raise ValueError('reconciliation missing')
        record=self.records[self.policy['event']['run_key']];self.jobs[record['job_id']]='terminal';record['terminal']=True;self.slot=None;self.phase=4
    def completed_duplicate(self):
        if self.phase!=4:raise ValueError('terminal not confirmed')
        record,status=self.reserve(self.policy['event']['run_key'],self.policy['event']['pipeline'])
        assert status=='duplicate' and record['terminal'] and len(self.jobs)==1
        self.evidence.append({'case':'completed duplicate','record':dict(record),'logical_jobs':len(self.jobs),'active_slot':self.slot});self.phase=5
    def fatal_build_gates(self):
        if self.phase!=5:raise ValueError('durable checks incomplete')
        self.config={'steps':[{'id':'admission','waitFor':['-'],'allowFailure':False},{'id':'function_test','waitFor':['admission'],'allowFailure':False},{'id':'execute','waitFor':['function_test'],'allowFailure':False}]}
        import yaml
        with open('build.yaml','w') as f:yaml.safe_dump(self.config,f)
        with open('build.yaml') as f:loaded=yaml.safe_load(f)
        assert loaded==self.config
        self.phase=6
    def report(self):
        if self.phase!=6:raise ValueError('required gates missing')
        return {'policy':self.policy,'durable_assertions':self.evidence,'build':self.config,'source_trace_count':len(self.events),'scope':'simulated atomic linearization and fresh-worker reconciliation; no live pipeline launch'}
'''
C[c]=reorder(c,'Reorder the supplied bounded coordinator/executor fixture operations. The infrastructure supplies atomic reserve/attach/terminal methods, not process-local deduplication. Prove same-key concurrent deliveries share one persisted job identity, a different key is busy, fresh workers after reservation/launch and unknown response reconcile that identity, terminal release retains completed keys, and required admission/function-test gates fatally precede execute with YAML round-trip intact. Each operation asserts durable records/counts. This is a deterministic concurrency/restart simulator, not a live launch.', ['ds.idempotency_traces'],'from lab import *\npolicy = '+repr(pol)+"\nlab = AdmissionLab(load('idempotency_traces'),policy)\n",['lab.concurrency_and_reservation()','lab.restart_and_launch()','lab.unknown_response_reconcile()','lab.confirm_terminal_and_release()','lab.completed_duplicate()','lab.fatal_build_gates()'],extra,packages=['numpy','pyyaml'])
# Write interim for follow-on main-code expansion.
json.dump({'code':C},open(B/'04_code_draft.json','w'),indent=2)
# Correct exact registry contract field names and parse threshold literals from policy text.
import re
ix=C['mle.distribution_monitoring']
for f in [ix['public']['workspace']['files'][0],ix['grading']['solution_files'][0]]:f['content']=f['content'].replace("policy['categories']","policy['declared_categories']").replace("policy['predicted_classes']","policy['declared_classes']")
ix=C['mle.data_drift_detection'];pol=policy('mle.data_drift_detection');threshold=float(re.search(r'distance > ([0-9.]+)',pol['criterion'])[1]);factor=float(re.match(r'([0-9.]+)',pol['distance_equation'])[1])
pre='from lab import *\npolicy = '+repr(pol)+f'\nthreshold = {threshold!r}\nfactor = {factor!r}\n'+'''reference = load('reference')
production = load('production')
r = column(reference,'numeric_values')
p = column(production,'numeric_values')
r_total = len(reference)
p_total = len(production)
r_counts = aligned_counts(reference,policy['declared_categories'])
p_counts = aligned_counts(production,policy['declared_categories'])
fixed_edges = np.asarray(policy['fixed_edges'])
r_bin_counts = np.histogram(r,bins=fixed_edges)[0]
p_bin_counts = np.histogram(p,bins=fixed_edges)[0]
'''
work=[('r_mean','np.mean(r)'),('p_mean','np.mean(p)'),('r_std','np.std(r, ddof=0)'),('p_std','np.std(p, ddof=0)'),('r_prob','r_counts / r_total'),('p_prob','p_counts / p_total'),('r_bin_prob','r_bin_counts / r_total'),('p_bin_prob','p_bin_counts / p_total'),('distance','factor * np.sum(np.abs(p_prob-r_prob))'),('numeric_distance','factor * np.sum(np.abs(p_bin_prob-r_bin_prob))'),('category_drift','distance > threshold'),('numeric_drift','numeric_distance > threshold')]
post="report = {'definitions':policy,'r_total':r_total,'p_total':p_total,'r_mean':r_mean,'p_mean':p_mean,'r_std':r_std,'p_std':p_std,'r_prob':r_prob,'p_prob':p_prob,'r_bin_prob':r_bin_prob,'p_bin_prob':p_bin_prob,'category_distance':distance,'numeric_distance':numeric_distance,'category_drift':category_drift,'numeric_drift':numeric_drift,'interpretation':'distribution difference only'}\n"
ix['public']['prompt']='Complete the aligned feature drift report for reference.csv and production.csv. Retain declared reference/window, bin edges, category order and eligibility. Compute numeric means and population std; normalize categorical counts and fixed numerical-bin counts by each window total. For each feature calculate the supplied distance 0.5*sum(abs(p_ref-p_prod)); flag only distance>0.20, not equality. Report both decisions as distribution differences, never inferred quality loss.'
ix['public']['workspace']['files'][0]['content']=pre+'\n'.join(n+' = None' for n,e in work)+'\n'+post
ix['grading']['solution_files'][0]['content']=pre+'\n'.join(n+' = '+e for n,e in work)+'\n'+post
ix=C['mle.delayed_label_quality'];ix['public']['workspace']['files'][1]['content']=ix['public']['workspace']['files'][1]['content'].replace("policy['evaluation_cutoff']","policy['analysis_time']").replace("policy['maturity_hours']","policy['minimum_age_hours']")
pre=ix['grading']['solution_files'][0]['content'].split('report = result')[0]
body='''pred_by_id = {}
for pred in predictions:
    if pred['prediction_id'] in pred_by_id:
        raise ValueError('duplicate prediction ID')
    pred_by_id[pred['prediction_id']] = pred
label_by_id = {}
for label in labels:
    if label['prediction_id'] in label_by_id:
        raise ValueError('duplicate label ID')
    label_by_id[label['prediction_id']] = label
eligible = []
matched = []
losses = []
errors = []
unmatched = []
excluded = []
for pred in predictions:
    if pred['eligible'] and pred['cohort_id'] == policy['cohort']:
        eligible.append({'prediction_id':pred['prediction_id'],'prediction_timestamp':pred['prediction_timestamp']})
for label in labels:
    if label['prediction_id'] not in pred_by_id:
        unmatched.append(label['prediction_id'])
    else:
        pred = pred_by_id[label['prediction_id']]
        if pred['eligible'] and pred['cohort_id']==policy['cohort'] and mature(pred,label,policy):
            matched.append(pred['prediction_id'])
            losses.append(label['loss'])
            errors.append(pred['prediction'] != label['label'])
        else:
            excluded.append(label['prediction_id'])
coverage = len(matched) / len(eligible)
error_count = sum(errors)
error_proportion = error_count / len(matched)
mean_loss = np.mean(losses)
std_loss = np.std(losses, ddof=0)
result = {'cohort':policy,'eligible_predictions':eligible,'mature_matched_ids':matched,'unmatched_labels':unmatched,'excluded_labels':excluded,'maturity_coverage':coverage,'error_count':error_count,'error_proportion':error_proportion,'mean_loss':mean_loss,'std_loss':std_loss,'scope':'mature matched cohort only; all traffic quality unestablished'}
report = result
'''
ix['grading']['solution_files'][0]['content']=pre+body
ix['public']['workspace']['files'][0]['content']=pre+"# Implement cohort preservation and bounded label joining here.\nreport = None\n"
ix=C['mle.actionable_ml_alerts'];margin=int(re.search(r'\+(\d+)',policy('mle.actionable_ml_alerts')['window_rule'])[1])
for f in [ix['public']['workspace']['files'][0],ix['grading']['solution_files'][0]]:f['content']=f['content'].replace("baseline = np.asarray",'margin = '+repr(margin)+'\nbaseline = np.asarray').replace("policy['margin']","margin")
ix=C['mle.production_regression_diagnosis'];pre=ix['grading']['solution_files'][0]['content'].split('report = results')[0]
body='''results = []
for r in data:
    denominator = r['matched_eligible_labels']
    rate = None
    if denominator > 0:
        rate = r['labeled_errors'] / denominator
    response = r['supported_response']
    gates = []
    if response == 'approved_rollback':
        gates = ['readiness','bounded prediction']
    results.append({'release':r['release_id'],'cohort':r['cohort_id'],'time':r['timestamp'],'impact':r['client_impact'],'artifact_match':r['active_artifact']==r['approved_artifact'],'config_match':r['active_config']==r['approved_config'],'schema_pass':r['schema_pass'],'hypothesis_test':r['hypothesis_test'],'distribution_distance':r['distribution_distance'],'denominator':denominator,'errors':r['labeled_errors'],'error_proportion':rate,'response':response,'gates':gates,'scope':'distribution difference alone does not establish quality loss'})
report = results
'''
ix['grading']['solution_files'][0]['content']=pre+body;ix['public']['workspace']['files'][0]['content']=pre+'# Complete the evidence analysis.\nreport = None\n'
ix=C['mle.retrained_candidate_validation'];pre=ix['grading']['solution_files'][0]['content'].split('report = results')[0]
body='''def rates(r):
    fpr = None
    fnr = None
    cost = None
    if r['FP']+r['TN'] > 0 and r['FN']+r['TP'] > 0:
        fpr = r['FP']/(r['FP']+r['TN'])
        fnr = r['FN']/(r['FN']+r['TP'])
        cost = policy['P_Y0']*fpr*policy['cost_FP'] + policy['P_Y1']*fnr*policy['cost_FN']
    return {'FPR':fpr,'FNR':fnr,'expected_cost':cost}
results = []
for r in data:
    if r['model_role']=='candidate':
        incumbent = None
        for other in data:
            if other['fixture']==r['fixture'] and other['model_role']=='incumbent':
                incumbent = other
        rr = rates(r)
        ir = rates(incumbent)
        defined = rr['expected_cost'] != None and ir['expected_cost'] != None
        quality_pass = False
        cost_pass = False
        if defined:
            quality_pass = rr['FPR'] <= policy['acceptance']['maximum_FPR'] and rr['FNR'] <= policy['acceptance']['maximum_FNR']
            cost_pass = rr['expected_cost'] <= ir['expected_cost']
        cohort_pass = r['cohort_id']==incumbent['cohort_id'] and r['cohort_id']==policy['cohort']
        for identity_match in [True,False]:
            accept = defined and quality_pass and cost_pass and r['slice_pass'] and r['compatibility_pass'] and cohort_pass and identity_match
            if not identity_match:
                assert not accept
            results.append({'fixture':r['fixture'],'candidate':r['registry_artifact_id'],'cohort':r['cohort_id'],'rates':rr,'incumbent_rates':ir,'quality_pass':quality_pass,'cost_pass':cost_pass,'slice_pass':r['slice_pass'],'compatibility_pass':r['compatibility_pass'],'cohort_pass':cohort_pass,'promotion_identity_matches':identity_match,'verdict':accept})
report = results
'''
ix['grading']['solution_files'][0]['content']=pre+body;ix['public']['workspace']['files'][0]['content']=pre+'# Implement candidate gating; protected tests are not supplied.\nreport = None\n'
ix=C['mle.ml_workload_cost_attribution'];pre=ix['grading']['solution_files'][0]['content'].split('report = result')[0]
body='''allocated = {'training':{'w1':0,'w2':0},'inference':{'w1':0,'w2':0}}
unallocated = []
eligible_total = 0
for r in charges:
    eligible_total = eligible_total + r['amount']
    if r['resource_id'] in policy['resource_mapping']:
        workload = policy['resource_mapping'][r['resource_id']]
        allocated[workload][r['reporting_window']] = allocated[workload][r['reporting_window']] + r['amount']
    elif r['charge_category']=='shared':
        for workload in ['training','inference']:
            allocated[workload][r['reporting_window']] = allocated[workload][r['reporting_window']] + r['amount']*policy['shared_rule'][workload]
    else:
        unallocated.append(r)
summary = {}
unusual = []
allocated_total = 0
for workload in ['training','inference']:
    numeric_values = np.array([allocated[workload]['w1'],allocated[workload]['w2']])
    works = []
    unit_costs = []
    for window in ['w1','w2']:
        amount = allocated[workload][window]
        allocated_total = allocated_total + amount
        if amount > unusual_threshold:
            unusual.append({'workload':workload,'window':window,'amount':amount})
        completed = 0
        for l in lifecycles:
            if l['identity']==workload+'-lab' and l['window']==window:
                completed = completed + l['work']
        works.append(completed)
        unit = None
        if completed > 0:
            unit = amount/completed
        unit_costs.append(unit)
    summary[workload] = {'window_costs':numeric_values,'mean':np.mean(numeric_values),'std':np.std(numeric_values, ddof=0),'work':works,'unit_costs':unit_costs}
unallocated_total = sum([r['amount'] for r in unallocated])
assert allocated_total + unallocated_total == eligible_total
result = {'lifecycle_evidence':lifecycles,'allocations':allocated,'summaries':summary,'unallocated':unallocated,'unusual':unusual,'allocated_total':allocated_total,'unallocated_total':unallocated_total,'eligible_export_total':eligible_total,'unit':policy['unit']}
report = result
'''
unusual=float(re.search(r'>([0-9.]+)',policy('mle.ml_workload_cost_attribution')['unusual_rule'])[1]);pre+='unusual_threshold = '+repr(unusual)+'\n';ix['grading']['solution_files'][0]['content']=pre+body;ix['public']['workspace']['files'][0]['content']=pre+'# Implement complete allocation and reconciliation.\nreport = None\n'
json.dump({'code':C},open(B/'04_code_draft.json','w'),indent=2)
# local syntax audit: report every descriptor conflict before execution.
for c,ix in C.items():
 s=ix['grading']['solution_files'][0]['content'];st=ix['public']['workspace']['files'][0]['content'];live=ix['public']['constraints'];print(c,pysyntax.judge(s,live['allowed_syntax'],live['blocked_syntax'],st)[0])
# Supplied serialization adapter normalizes NumPy scalars before PyYAML.
ix=C['mle.actionable_ml_alerts']
for f in [ix['public']['workspace']['files'][0],ix['grading']['solution_files'][0]]:
 f['content']=f['content'].replace("with open('alert.yaml','w')","config['threshold'] = float(config['threshold'])\nwith open('alert.yaml','w')")
# Detector vocabulary is narrower than the anchor's human-readable descriptors.
# Keep lists verbatim. Use a dependency-order repair task on supplied statements
# for those constructs; all runtime scaffolding is supplied unchanged.
import ast
for c,ix in C.items():
 f=ix['grading']['solution_files'][0]; st=ix['public']['workspace']['files'][0]
 solution=f['content']; starter=st['content'];lib=ix['public']['workspace']['files'][1]['content']
 solution=solution.replace('from lab import *\n','');starter=starter.replace('from lab import *\n','')
 tree=ast.parse(solution);lines=solution.splitlines(keepends=True)
 # Definitions are supplied infrastructure. Make them visibly available before editable statements.
 defs=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))]
 lib+='\n'+''.join(''.join(lines[n.lineno-1:n.end_lineno])+'\n' for n in defs)
 nodes=[n for n in tree.body if n not in defs]
 blocks=[''.join(lines[n.lineno-1:n.end_lineno]).rstrip() for n in nodes]
 scaf='# Supplied fixture infrastructure; learner edits only the statements below.\n_fixture_support = '+repr(lib)+'\nexec(_fixture_support)\n'
 if pysyntax.judge(solution,ix['public']['constraints']['allowed_syntax'],ix['public']['constraints']['blocked_syntax'],starter)[0]:
  # Preserve imports/input loading first. Invert dependent calculations and output
  # statements; restoring their dependency order is the simplest runnable task
  # supported without broadening the glossary descriptor lists.
  boundary=next((i for i,b in enumerate(blocks) if b.startswith(('r_count =','r_mean =','pred_by_id =','mean =','results =','mask =','allocated ='))),0)
  given=blocks[:boundary];editable=blocks[boundary:]
  starter=scaf+'\n'.join(given)+'\n# Repair dependency order of these supplied statements; do not change formulas.\n'+'\n\n'.join(reversed(editable))+'\n'
  solution=scaf+'\n'.join(given)+'\n'+'\n\n'.join(editable)+'\n'
  ix['public']['prompt']+='\nRuntime note: the formulas/contract operations are supplied as scaffolding. Repair their execution order so inputs and intermediate values exist before use and the final report is assembled last. Keep formulas and fixed policy fields unchanged. Inspect the resulting report against the task contract.'
 else:
  solution=scaf+solution;starter=scaf+starter
 f['content']=solution;st['content']=starter
 ix['public']['workspace']['files']=[st]
 print('FINAL SYNTAX',c,pysyntax.judge(solution,ix['public']['constraints']['allowed_syntax'],ix['public']['constraints']['blocked_syntax'],starter)[0])
# Execute reference programs with pinned engine; derive test values, never type them.
for c,ix in C.items():
 tables,_=sandbox._tables(R,ix['public']['workspace']['asset_mounts'],{},[])
 probes=[{'id':'report','kind':'expr','expr':'report'}]
 result=sandbox.node_run(sandbox._py_job('python',ix['public']['runtime']['packages'],[sandbox._py_script('solution','main.py',ix['grading']['solution_files'][0]['content'],sandbox._py_mounts(tables),probes)]),sandbox.RUNTIMES['python']['runner'])['results']['solution']
 if not result['ok'] or not result['probes']['report']['ok']:
  print('EXECUTION ERROR',c,result);raise SystemExit(1)
 ix['grading']['tests'][0]['spec']['expected']=result['probes']['report']['value']
 print('EXECUTED',c)
json.dump({'code':C},open(B/'04_code_draft.json','w'),indent=2)
# Build interactions exactly from plan; measures copied from planned assessment anchors.
def classify(c):
 if c=='mle.drift_degradation_distinction':
  ds=assets['ds.evidence_scenarios'];data=rows(ds['asset_id']); buckets={'P(X)':'Input distribution shift only','P(Y|X)':'Conditional feature–label change only','matched_label_errors':'Observed quality degradation only'}
  pub={'prompt':'Classify each bounded evidence scenario by the change it establishes, not by changes it could merely suggest. Each item explicitly states what remains unresolved; the quality item has matched labels and a declared reference.','buckets':[{'bucket_id':'b'+str(i),'label':label} for i,label in enumerate(buckets.values())],'items':[]}; gr={'assignments':{},'role_map':{},'item_feedback':{}}
  role=next(co['semantic_role'] for co in ds['columns'] if co['name']=='supported_evidence');mapping={v:'b'+str(i) for i,v in enumerate(buckets)}
  for i,r in enumerate(data):
   it='i'+str(i);pub['items'].append({'item_id':it,'text':r['observation']+' Matched labels available: '+str(r['matched_labels_available'])+'. Unresolved: '+r['unresolved'],'source':{'asset_id':ds['asset_id'],'row':{'where':{'scenario_id':r['scenario_id']},'occurrence':0},'column':'supported_evidence'}});gr['assignments'][it]=mapping[r['supported_evidence']];gr['role_map'][mapping[r['supported_evidence']]]=role;gr['item_feedback'][it]=msg('This establishes '+buckets[r['supported_evidence']]+'. '+r['unresolved'])
  return {'type':'classify','public':pub,'grading':gr}
 if c=='mle.retraining_trigger_policy':
  stages=rows('ds.pipeline_stages');events=rows('ds.trigger_events');chain='\n'.join(json.dumps(r) for r in stages)
  items=[]
  for r in events:
   if not r['authorized'] or not r['investigated']:judgement='reject';why='Entry rejects unauthorized or uninvestigated events.'
   elif not r['data_quality_pass']:judgement='blocked';why='Failed data quality blocks train, evaluate and promote; eligibility alone does not bypass required checks.'
   else:judgement='eligible';why='Authorized investigated evidence enters the existing entry stage with the intended snapshot; promotion remains separately approved.'
   text=json.dumps(r)+'\nPolicy trace: credentials are runtime references only; no credential values in YAML/logs. Entry checks identity, investigation and intended dataset. Train waits for data_quality_test success; evaluate waits for train success; promote waits for evaluate and separate approval. Required checks are fatal.'
   items.append((text,judgement,why))
  prompt='Inspect the event/policy traces against this existing stage inventory. Classify as rejected at entry, eligible for the required retraining path (NOT promotion approval), or eligible but blocked at required data quality. Treat investigated schedule/new-data/label-supported degradation as supplied eligibility evidence; a bare uninvestigated alarm is rejected.\n'+chain
 else:
  pol=policy(c);pipeline=pol['PipelineName'] if 'PipelineName' in pol else pol.get('pipeline','order-retrain-lab')
  snapshot={k:v for k,v in pol.items() if k in ['snapshot_ref','object_generation','sha256','PipelineParameters','ClientRequestToken']}
  base='Fixture contract: '+json.dumps(pol)+'\n'
  items=[(base+'Trace: authorized trigger accepted; retrieved immutable version bytes verified; required function test succeeded. Each execution step waitFor its prior required successful step; allowFailure=false and no allowExitCodes bypass. Step-scoped availableSecrets.secretManager version reference and secretEnv are used; no values printed. One start_pipeline_execution uses the approved snapshot parameters and client token; its returned PipelineExecutionArn is recorded with trigger authorization, dataset identity and actual parameters. inspect_consumed_input matches the retrieved immutable snapshot. No promotion performed.','eligible','The accepted trace binds authorization, immutable consumed input, returned execution identity and fatal scoped configuration without credential values.'),
  (base+'Trace: authorization rejected at entry with unsuccessful exit. No training launched. Required downstream steps depend on successful entry. Captured output contains only safe denial evidence, not injected credentials.','blocked','The rejected entry exits unsuccessfully and cannot launch dependent training.'),
  (base+'Trace: authorized trigger, but actual consumed input refers to latest mutable data rather than the retrieved approved immutable generation. The trace claims success merely because submission parameters name the approved snapshot.','reject','Submission parameters alone are insufficient; actual stage input must match the retrieved approved immutable snapshot.'),
  (base+'YAML excerpt: execute.waitFor=[function_test]; function_test.allowFailure=true. The required test fails but execute launches training. availableSecrets references are scoped and logs are credential-safe.','reject','The fatal required test was bypassed; correct secret handling does not repair a broken successful-step dependency.')]
  prompt='Inspect each independent execution/configuration trace against the supplied contract. Classify as a compliant accepted execution, a compliant fail-closed rejection with no training, or an unsafe/noncompliant trace. Judge actual consumed snapshot evidence, authorization, fatal dependencies and scoped secret injection—not submission alone.'
 labels={'eligible':'Compliant accepted path','blocked':'Compliant blocked/rejected path','reject':'Unsafe or entry-rejected path'} if c=='mle.authorized_retraining_execution' else {'eligible':'Eligible required retraining path; promotion separate','blocked':'Required data quality blocks dependent stages','reject':'Reject at entry'}
 pub={'prompt':prompt,'buckets':[{'bucket_id':k,'label':v} for k,v in labels.items()],'items':[]};gr={'assignments':{},'item_feedback':{}}
 for i,(text,bucket,why) in enumerate(items):
  it='i'+str(i);pub['items'].append({'item_id':it,'text':text});gr['assignments'][it]=bucket;gr['item_feedback'][it]=msg(why)
 return {'type':'classify','public':pub,'grading':gr}
out={k:P[k] for k in ['schema_version','path_id','batch_id']};out.update(kind='interactions_part',tiles=[])
for t in P['tiles']:
 tile={'tile_id':t['tile_id'],'interactions':[]};seen=set();rem=next(x for x in S['tiles'] if x['tile_id']==t['tile_id']).get('remediation_steps',[])
 for step in t['steps']:
  if step['type'] not in ['check','hands_on']:continue
  c=step['concept_ids'][0];name=c.split('.')[1];planned=step['planned_interaction_type']
  if step['type']=='check':
   prompt,right,wrong,why=checks[name];options=[{'option_id':'correct','text':right},{'option_id':'misconception','text':wrong}]
   ix={'type':'choice','public':{'prompt':prompt,'options':options,'selection':'single','shuffle':True},'grading':{'correct_option_ids':[o['option_id'] for o in options if o['text']==right],'option_feedback':{'correct':msg(why),'misconception':msg(why)}}}
  elif planned=='classify':ix=classify(c)
  else:ix=C[c]
  measures=[]
  for anchor in step['anchors']:
   if '#assessment:' in anchor:
    capability=anchor.split('#assessment:')[1];a=next(a for a in g[c]['assessment_anchors'] if a['capability']==capability);measures.append({'concept_id':c,'capability':a['capability'],'fact_ids':a['fact_ids']})
  ix.update(interaction_id='ix.'+step['step_id'],difficulty='intro' if step['type']=='check' and not seen else 'stretch' if step['type']=='hands_on' else 'core',grading_mode='client',standalone=True,measures=measures,anchors=step['anchors'])
  ix['feedback']={'correct':msg('Your result follows the declared evidence and contract boundaries.'),'incorrect':msg('Recheck the declared scope, eligible observations and required evidence before accepting the result.'),'hints':['Identify which observations or operations the stated contract makes eligible.','Keep the declared identities, definitions and required gates intact.']}
  if c not in seen:
   target=next((r['step_id'] for r in rem if c in r['concept_ids']),None)
   if target:ix['feedback']['remediation_step_id']=target
  seen.add(c);tile['interactions'].append({'step_id':step['step_id'],'interaction':ix})
 out['tiles'].append(tile)
json.dump(out,open(B/'interactions.json','w'),indent=2,ensure_ascii=False)
print('WROTE',sum(len(t['interactions']) for t in out['tiles']))
