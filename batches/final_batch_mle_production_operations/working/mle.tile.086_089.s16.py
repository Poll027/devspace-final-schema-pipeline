import csv, json, datetime
import numpy as np
SCHEMAS = {'idempotency_traces': {'fixture': 'string', 'step': 'integer', 'run_key': 'string', 'pipeline': 'string', 'admission_status': 'string', 'job_id': 'string', 'active_slot_owner': 'string', 'terminal_confirmed': 'boolean', 'logical_job_count': 'integer', 'event': 'string'}, 'trigger_events': {'event_id': 'string', 'event_type': 'string', 'identity': 'string', 'authorized': 'boolean', 'investigated': 'boolean', 'dataset_ref': 'string', 'evidence': 'string', 'entry_stage': 'string', 'data_quality_pass': 'boolean', 'promotion_approved': 'boolean'}, 'pipeline_stages': {'stage_id': 'string', 'purpose': 'string', 'required_artifacts': 'string', 'dependencies': 'string', 'separate_authorization_required': 'boolean'}}
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
        self.trigger_results=[]
        inventory=load('pipeline_stages')
        for event in load('trigger_events'):
            accepted=event['authorized'] and event['investigated'] and event['entry_stage']=='entry'
            quality=accepted and event['data_quality_pass']
            self.trigger_results.append({'event':event['event_id'],'entry':'accepted' if accepted else 'rejected','resolved_input':event['dataset_ref'] if accepted else None,'data_quality':'pass' if quality else 'blocked','train':quality,'evaluate':quality,'promote':quality and event['promotion_approved'],'credential_reference':'runtime references only; no credential values'})
            if not accepted or not event['data_quality_pass']:
                assert not self.trigger_results[-1]['train']
        self.config['stage_inventory']=inventory
        self.config['trigger_policy']={'entry':'authorization, investigation and intended immutable snapshot','required_failure':'fatal','separate_promotion_approval':True,'credential_reference':'runtime references only; no credential values'}
        with open('build.yaml','w') as f:yaml.safe_dump(self.config,f)
        with open('build.yaml') as f:loaded=yaml.safe_load(f)
        assert loaded==self.config
        self.phase=6
    def report(self):
        if self.phase!=6:raise ValueError('required gates missing')
        return {'policy':self.policy,'durable_assertions':self.evidence,'build':self.config,'source_traces':self.events,'trigger_results':self.trigger_results,'scope':'simulated atomic linearization and fresh-worker reconciliation; no live pipeline launch'}


# OUTER

policy = {'event': {'run_key': 'K', 'pipeline': 'order-retrain-lab'}, 'busy_policy': 'defer', 'coordinator_contract': {'atomic_admit(run_key,pipeline)': 'Atomically reserve unique run key AND pipeline slot and persist job_id. Return accepted, duplicate or busy plus persisted identity; durable coordinator is external to learner process.', 'inspect(run_key)': 'Read durable record; completed records retained.', 'confirm_terminal_and_release(run_key,job_id)': 'Release active slot only after executor confirms terminal; retain completed key.'}, 'executor_contract': {'launch(job_id)': 'Idempotent executor token; at most one logical job per job_id. Unknown response must be reconciled with same token.', 'attach(job_id)': 'Resume or reconcile existing identity.', 'status(job_id)': 'Return running or confirmed terminal.'}, 'test_scenarios': ['concurrent_same_key', 'concurrent_different_key', 'restart_after_reservation', 'restart_after_launch', 'unknown_launch_response', 'completed_duplicate'], 'fatal_dependencies': ['admission', 'function_test', 'execute']}
lab = AdmissionLab(load('idempotency_traces'),policy)

lab.concurrency_and_reservation()
lab.restart_and_launch()
lab.unknown_response_reconcile()
lab.confirm_terminal_and_release()
lab.completed_duplicate()
lab.fatal_build_gates()
report = lab.report()
