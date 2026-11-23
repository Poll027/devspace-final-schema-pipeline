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
class Coordinator:
    def __init__(self): self.records={}; self.slot=None
    def atomic_admit(self,key,pipeline):
        if key in self.records: return {'status':'duplicate',**self.records[key]}
        if self.slot is not None: return {'status':'busy','job_id':None}
        record={'run_key':key,'pipeline':pipeline,'job_id':'job.'+key,'terminal':False}
        self.records[key]=record; self.slot=key
        return {'status':'accepted',**record}
    def inspect(self,key): return dict(self.records[key])
    def confirm_terminal_and_release(self,key,job_id):
        record=self.records[key]
        if record['job_id']!=job_id: raise ValueError('identity mismatch')
        record['terminal']=True; self.slot=None
class Executor:
    def __init__(self): self.jobs={}; self.tokens=[]
    def launch(self,job_id): self.tokens.append(job_id); self.jobs.setdefault(job_id,'running')
    def attach(self,job_id): self.tokens.append(job_id); self.jobs.setdefault(job_id,'running')
    def status(self,job_id): return self.jobs.get(job_id,'absent')
def fixture(handler,case):
    c=Coordinator();e=Executor(); event=policy['event'];key=event['run_key'];pipe=event['pipeline']
    if case=='concurrent_delivery':
        # Supplied atomic interface linearizes the competing delivery attempts.
        first=handler(event,c,e); duplicate=handler(event,c,e)
        busy=handler({'run_key':key+'2','pipeline':pipe},c,e)
        return {'first':first,'duplicate':duplicate,'busy':busy,'logical_jobs':len(e.jobs),'active_slot':c.slot,'tokens':e.tokens}
    if case=='restart_after_reservation':
        record=c.atomic_admit(key,pipe)
        resumed=handler(event,c,e)
        return {'persisted_job_id':record['job_id'],'result':resumed,'logical_jobs':len(e.jobs),'tokens':e.tokens}
    if case=='restart_after_launch':
        record=c.atomic_admit(key,pipe);e.launch(record['job_id'])
        resumed=handler(event,c,e)
        return {'persisted_job_id':record['job_id'],'result':resumed,'logical_jobs':len(e.jobs),'tokens':e.tokens}
    if case=='unknown_launch_response':
        record=c.atomic_admit(key,pipe);e.launch(record['job_id'])
        resumed=handler(event,c,e)
        return {'persisted_job_id':record['job_id'],'result':resumed,'logical_jobs':len(e.jobs),'tokens':e.tokens,'active_slot':c.slot}
    if case=='completed_duplicate':
        record=c.atomic_admit(key,pipe);e.launch(record['job_id']);e.jobs[record['job_id']]='terminal'
        terminal=handler(event,c,e); duplicate=handler(event,c,e)
        return {'result':terminal,'duplicate':duplicate,'logical_jobs':len(e.jobs),'active_slot':c.slot,'completed':c.inspect(key)['terminal']}
def trigger_replay():
    outputs=[]
    for event in load('trigger_events'):
        accepted=event['authorized'] and event['investigated'] and event['entry_stage']=='entry'
        quality=accepted and event['data_quality_pass']
        outputs.append({'event':event['event_id'],'entry':'accepted' if accepted else 'rejected','resolved_input':event['dataset_ref'] if accepted else None,'data_quality':'pass' if quality else 'blocked','train':quality,'evaluate':quality,'promote':quality and event['promotion_approved'],'credential_reference':'runtime references only; no credential values'})
    return outputs
def build_entry(step_id):
    if step_id=='admission': return load('idempotency_traces')
    if step_id=='function_test': return fixture(handle_event,'concurrent_delivery')
    if step_id=='execute': return trigger_replay()
    raise SystemExit('unknown step')
def execute_build_steps(config):
    return {s['id']:build_entry(s['args'][-1]) for s in config['steps']}
policy = {'event': {'run_key': 'K', 'pipeline': 'order-retrain-lab'}, 'busy_policy': 'defer', 'coordinator_contract': {'atomic_admit(run_key,pipeline)': 'Atomically reserve unique run key AND pipeline slot and persist job_id. Return accepted, duplicate or busy plus persisted identity; durable coordinator is external to learner process.', 'inspect(run_key)': 'Read durable record; completed records retained.', 'confirm_terminal_and_release(run_key,job_id)': 'Release active slot only after executor confirms terminal; retain completed key.'}, 'executor_contract': {'launch(job_id)': 'Idempotent executor token; at most one logical job per job_id. Unknown response must be reconciled with same token.', 'attach(job_id)': 'Resume or reconcile existing identity.', 'status(job_id)': 'Return running or confirmed terminal.'}, 'test_scenarios': ['concurrent_same_key', 'concurrent_different_key', 'restart_after_reservation', 'restart_after_launch', 'unknown_launch_response', 'completed_duplicate'], 'fatal_dependencies': ['admission', 'function_test', 'execute']}


# Supplied orchestration; operations are selected by the learner.
import yaml
supplied_safe_dump = yaml.safe_dump
supplied_safe_load = yaml.safe_load
def supplied_atomic_admission(event, coordinator):
    return coordinator.atomic_admit(event['run_key'], event['pipeline'])

def handle_event(event, coordinator, executor):
    admission = admission_operation(event, coordinator)
    if admission['status'] == 'busy':
        return {'status': 'busy', 'job_id': None, 'released': False}
    job_id = admission['job_id']
    record = coordinator.inspect(event['run_key'])
    if admission['status'] == 'accepted':
        executor.launch(job_id)
    elif admission['status'] == 'duplicate' and (not record['terminal']):
        executor.attach(job_id)
    released = False
    if executor.status(job_id) == 'terminal' and (not record['terminal']):
        coordinator.confirm_terminal_and_release(event['run_key'], job_id)
        released = True
    return {'status': admission['status'], 'job_id': job_id, 'released': released}

#TAIL

admission_operation = supplied_atomic_admission
dump_operation = supplied_safe_dump
load_operation = supplied_safe_load
import yaml
supplied_safe_dump = yaml.safe_dump
supplied_safe_load = yaml.safe_load
dump_operation = supplied_safe_dump
load_operation = supplied_safe_load
concurrent = fixture(handle_event, 'concurrent_delivery')
reserved_restart = fixture(handle_event, 'restart_after_reservation')
launch_restart = fixture(handle_event, 'restart_after_launch')
unknown = fixture(handle_event, 'unknown_launch_response')
completed = fixture(handle_event, 'completed_duplicate')
assert concurrent['first']['status'] == 'accepted' and concurrent['duplicate']['status'] == 'duplicate' and (concurrent['busy']['status'] == 'busy')
assert concurrent['first']['job_id'] == concurrent['duplicate']['job_id'] and concurrent['logical_jobs'] == 1
assert reserved_restart['result']['job_id'] == reserved_restart['persisted_job_id'] and reserved_restart['logical_jobs'] == 1
assert launch_restart['result']['job_id'] == launch_restart['persisted_job_id'] and launch_restart['logical_jobs'] == 1
assert unknown['result']['job_id'] == unknown['persisted_job_id'] and unknown['logical_jobs'] == 1 and (unknown['active_slot'] == policy['event']['run_key'])
assert completed['result']['released'] and completed['completed'] and (completed['active_slot'] == None) and (completed['logical_jobs'] == 1)
assert completed['duplicate']['status'] == 'duplicate' and (not completed['duplicate']['released'])
import yaml
configuration_a = {'steps': [{'id': 'admission', 'waitFor': ['-'], 'allowFailure': False, 'name': 'python:3.11', 'args': ['python', 'main.py', 'admission']}, {'id': 'function_test', 'waitFor': ['admission'], 'allowFailure': False, 'name': 'python:3.11', 'args': ['python', 'main.py', 'function_test']}, {'id': 'execute', 'waitFor': ['function_test'], 'allowFailure': False, 'name': 'python:3.11', 'args': ['python', 'main.py', 'execute']}], 'stage_inventory': load('pipeline_stages'), 'trigger_policy': {'entry': 'authorization, investigation and intended immutable snapshot', 'required_failure': 'fatal', 'separate_promotion_approval': True, 'credential_reference': 'runtime references only; no credential values'}}
config = configuration_a
file_handle = open('build.yaml', 'w')
dump_operation(config, file_handle)
file_handle.close()
file_handle = open('build.yaml')
loaded = load_operation(file_handle)
file_handle.close()
assert loaded == config
assert loaded['steps'][0]['waitFor'] == ['-'] and loaded['steps'][1]['waitFor'] == ['admission'] and (loaded['steps'][2]['waitFor'] == ['function_test'])
assert loaded['steps'][0]['name'] == 'python:3.11' and loaded['steps'][1]['name'] == 'python:3.11' and (loaded['steps'][2]['name'] == 'python:3.11')
assert loaded['steps'][0]['args'] == ['python', 'main.py', 'admission'] and loaded['steps'][1]['args'] == ['python', 'main.py', 'function_test'] and (loaded['steps'][2]['args'] == ['python', 'main.py', 'execute'])
assert not loaded['steps'][0]['allowFailure'] and (not loaded['steps'][1]['allowFailure']) and (not loaded['steps'][2]['allowFailure'])
build_results = execute_build_steps(loaded)
report = {'policy': policy, 'durable_assertions': [concurrent, reserved_restart, launch_restart, unknown, completed], 'build': loaded, 'source_traces': load('idempotency_traces'), 'trigger_results': build_results['execute'], 'scope': 'simulated atomic linearization and fresh-worker reconciliation; no live pipeline launch'}
import sys
if len(sys.argv) > 1 and sys.argv[1] in ['admission', 'function_test', 'execute']:
    print(json.dumps(build_entry(sys.argv[1])))
