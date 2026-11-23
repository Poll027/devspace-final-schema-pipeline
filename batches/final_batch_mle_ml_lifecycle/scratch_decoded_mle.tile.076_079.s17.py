def assert_recovery_invariants(state, before, before_hashes, after, unchanged, validations_first):
    assert unchanged and state['validations'] > validations_first
    assert all((after[k] == generation for k, generation in before.items()))
    assert all((hashlib.sha256(state['objects'][k]['bytes']).hexdigest() == value for k, value in before_hashes.items()))


cases = {'accepted': {'initial_outputs': ['A'], 'race_outputs': [], 'invalid_outputs': [], 'gate_ok': True, 'exception': 'RecoverableFailure'}, 'boundary_completed': {'initial_outputs': ['A', 'B'], 'race_outputs': [], 'invalid_outputs': [], 'gate_ok': True, 'exception': None}, 'race_412': {'initial_outputs': ['A'], 'race_outputs': ['B'], 'invalid_outputs': [], 'gate_ok': True, 'exception': 'RecoverableFailure'}, 'invalid_existing': {'initial_outputs': ['A'], 'race_outputs': [], 'invalid_outputs': ['A'], 'gate_ok': True, 'exception': 'RecoverableFailure'}, 'conflicting_content': {'initial_outputs': ['A'], 'race_outputs': [], 'invalid_outputs': [], 'conflicting_outputs': ['A'], 'gate_ok': True, 'exception': 'RecoverableFailure'}, 'rejected_gate': {'initial_outputs': ['A'], 'race_outputs': [], 'invalid_outputs': [], 'gate_ok': False, 'exception': 'RecoverableFailure'}, 'unrelated_failure': {'initial_outputs': ['A'], 'race_outputs': [], 'invalid_outputs': [], 'gate_ok': True, 'exception': 'ValueError'}}

contract = {'injection_point': 'after A upload before B', 'recoverable_exception': 'storage_sim.RecoverableFailure', 'precondition_exception': 'storage_sim.PreconditionFailed', 'outputs': {'A': {'artifact_id': 'A', 'uri': 'gs://fixture-artifacts/A.txt', 'generation': 1, 'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6', 'validation_ok': True}, 'B': {'artifact_id': 'B', 'uri': 'gs://fixture-artifacts/B.txt', 'generation': 1, 'sha256': '6d5f5cbc73990d86a040e72f9e6d1cad2cb36297b10887e5444900c7286f634a', 'validation_ok': True}}, 'requirements': ['record and isolate failure', 'verify exact existing generation bytes/hash and validation', 'skip only verified completed upload', 'create missing output with if_generation_match=0', 'on 412 reload and verify, never overwrite', 'unrelated exceptions remain fatal', 'run retried stage and downstream required gates', 'second call preserves generations and upload counts but revalidates'], 'evidence_fields': ['initial_and_final_generations', 'hashes', 'validation_results', 'upload_counts', 'retry_status', 'downstream_status', 'resolved_inputs']}

trigger = {'id': 'fixture-artifact-trigger', 'topic': 'projects/fixture-project/topics/artifacts', 'bindings': {'_CASE': 'case_id', '_ARTIFACT': 'artifact_id'}, 'filters': {'event_type': 'artifact_ready'}, 'fixtures': [{'event_type': 'artifact_ready', 'case_id': 'accepted', 'artifact_id': 'A'}, {'event_type': 'artifact_ready', 'case_id': 'rejected_gate', 'artifact_id': 'A'}, {'event_type': 'unrelated', 'case_id': 'accepted', 'artifact_id': 'A'}]}

declared_outputs = ['A', 'B']

artifact_records = {'A': {'artifact_id': 'A', 'uri': 'gs://fixture-artifacts/A.txt', 'generation': 1, 'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6', 'validation_ok': True}, 'B': {'artifact_id': 'B', 'uri': 'gs://fixture-artifacts/B.txt', 'generation': 1, 'sha256': '6d5f5cbc73990d86a040e72f9e6d1cad2cb36297b10887e5444900c7286f634a', 'validation_ok': True}}

output_bytes = {'A': b'fictional fitted package A\npreprocess: divide feature by 5\nthreshold: 0.4\n', 'B': b'fictional fitted package B\npreprocess: divide feature by 5\nthreshold: 0.5\n'}

adapter_source = "evidence_fields = ['A', 'B', '_ARTIFACT', '_CASE', '_SNAPSHOT', 'accepted', 'after', 'all_evidence', 'before', 'bindings', 'boundary_completed', 'case', 'cases', 'conflicting_content', 'downstream_status', 'evidence', 'exit_code', 'failure_recorded', 'hashes', 'id', 'invalid_existing', 'name', 'ok', 'race_412', 'rejected_gate', 'required_gate_executed', 'resolved_args', 'resolved_artifact', 'retry_status', 'runs', 'second_call_unchanged', 'status', 'steps', 'triggered', 'unrelated_failure', 'uploads', 'waitFor']\n\ndef execute(config, trigger, event, actions):\n    import re\n    if 'branch_filter' in trigger:\n        if re.fullmatch(trigger['branch_filter'], event.get('branch', '')) is None:\n            return {'triggered': False, 'steps': []}\n    elif any((event.get(k) != v for k, v in trigger['filters'].items())):\n        return {'triggered': False, 'steps': []}\n    binding = dict(config.get('substitutions', {}))\n    binding.update({k: event[v] for k, v in trigger['bindings'].items()})\n    results = []\n    statuses = {}\n    for step in config['steps']:\n        args = [str(a) for a in step.get('args', [])]\n        for k, v in binding.items():\n            args = [a.replace('${' + k + '}', str(v)) for a in args]\n        deps = [x for x in step['waitFor'] if x != '-']\n        record = {'id': step['id'], 'name': step['name'], 'resolved_args': args, 'waitFor': deps}\n        if any((statuses.get(d) != 'SUCCESS' for d in deps)):\n            record.update(status='NOT_STARTED', exit_code=None, evidence=None)\n        else:\n            if step.get('allowFailure') or any((x != 0 for x in step.get('allowExitCodes', []))):\n                raise ValueError('required gate failure allowances are forbidden')\n            callback = actions.get(step['id'])\n            context = dict(binding)\n            context['_RESOLVED_ARGS'] = args\n            result = callback(context) if callback else {'ok': True}\n            record.update(status='SUCCESS' if result['ok'] else 'FAILURE', exit_code=0 if result['ok'] else 1, evidence=result)\n        statuses[step['id']] = record['status']\n        results.append(record)\n    return {'triggered': True, 'bindings': binding, 'steps': results}\n\nclass RecoverableFailure(Exception):\n    pass\n\nclass PreconditionFailed(Exception):\n    status = 412\n\nclass Blob:\n\n    def __init__(self, name, state):\n        self.name = name\n        self.state = state\n        self.generation = None\n\n    def exists(self):\n        return self.name in self.state['objects']\n\n    def reload(self):\n        self.generation = self.state['objects'][self.name]['generation']\n\n    def download_as_bytes(self, if_generation_match):\n        obj = self.state['objects'][self.name]\n        if obj['generation'] != if_generation_match:\n            raise PreconditionFailed('generation changed')\n        return obj['bytes']\n\n    def upload_from_filename(self, path, if_generation_match):\n        assert if_generation_match == 0\n        if self.name in self.state['race']:\n            self.state['objects'][self.name] = {'generation': 1, 'bytes': output_bytes[self.name]}\n            self.state['race'].remove(self.name)\n            raise PreconditionFailed('race created object')\n        if self.exists():\n            raise PreconditionFailed('object exists')\n        self.state['objects'][self.name] = {'generation': 1, 'bytes': output_bytes[self.name]}\n        self.state['uploads'][self.name] += 1\n\ndef exercise_case(case_id):\n    all_evidence = recovery_run()\n    return semantic_evidence({'case': all_evidence['cases'].get(case_id, {'ok': False, 'reason': 'missing case'}), 'all_evidence': all_evidence})\n\ndef semantic_evidence(value):\n    if isinstance(value, dict):\n        return {k: semantic_evidence(v) for k, v in value.items() if k in evidence_fields and k not in ('reason', 'failed', 'validation_count', 'config')}\n    if isinstance(value, list):\n        return [semantic_evidence(v) for v in value]\n    return value\n"

exec(adapter_source)

import hashlib

import yaml

recovery_outputs = list(declared_outputs)

configured_build = {'steps': [{'id': 'recovery', 'name': 'python:3.11', 'args': ['python', 'learner.py', '${_CASE}'], 'waitFor': ['-']}, {'id': 'required_validation', 'name': 'python:3.11', 'args': ['python', 'learner.py', '${_CASE}'], 'waitFor': []}, {'id': 'promotion', 'name': 'python:3.11', 'args': ['python', 'downstream_entry.py', '${_ARTIFACT}'], 'waitFor': []}], 'substitutions': {'_SNAPSHOT': 'valid', '_CASE': 'accepted', '_ARTIFACT': 'A'}, 'serviceAccount': 'projects/fixture-project/serviceAccounts/fixture-build@fixture-project.iam.gserviceaccount.com'}

initial_build = __import__("copy").deepcopy(configured_build)

configured_build['steps'][1]['waitFor'] = ['recovery']

configured_build['steps'][2]['waitFor'] = ['required_validation']

def verify_output(blob, state, row):
    blob.reload()
    data = blob.download_as_bytes(if_generation_match=blob.generation)
    state['validations'] += 1
    if hashlib.sha256(data).hexdigest() != artifact_records[blob.name]['sha256']:
        raise ValueError('content conflict')
    if blob.name in row['invalid_outputs'] or not artifact_records[blob.name]['validation_ok']:
        raise ValueError('validation failed')


def recovery(state, row, inject_failure=False):
    if inject_failure:
        try:
            a = Blob('A', state)
            if not a.exists():
                a.upload_from_filename('outputs/A.txt', if_generation_match=0)
            if row['exception'] == 'RecoverableFailure':
                raise RecoverableFailure('after A upload before B')
            if row['exception'] is not None:
                raise RuntimeError(row['exception'])
        except RecoverableFailure as failure:
            state['failure_recorded'] = type(failure).__name__
    for name in recovery_outputs:
        blob = Blob(name, state)
        if blob.exists():
            verify_output(blob, state, row)
        else:
            try:
                blob.upload_from_filename('outputs/' + name + '.txt', if_generation_match=0)
            except PreconditionFailed:
                verify_output(blob, state, row)
            else:
                verify_output(blob, state, row)
    return {'ok': set(recovery_outputs) == set(declared_outputs)}


def recover(row):
    state = {'objects': {}, 'race': list(row['race_outputs']), 'uploads': {name: 0 for name in declared_outputs}, 'validations': 0, 'failure_recorded': None}
    for name in row['initial_outputs']:
        Blob(name, state).upload_from_filename('outputs/' + name + '.txt', if_generation_match=0)
        if name in row.get('conflicting_outputs', []):
            state['objects'][name]['bytes'] = b'conflicting content'
    before = {k: v['generation'] for k, v in state['objects'].items()}
    before_hashes = {k: hashlib.sha256(v['bytes']).hexdigest() for k, v in state['objects'].items()}
    reason = None
    try:
        first = recovery(state, row, True)
        after_first = {k: v['generation'] for k, v in state['objects'].items()}
        counts_first = dict(state['uploads'])
        validations_first = state['validations']
        second = recovery(state, row)
        after = {k: v['generation'] for k, v in state['objects'].items()}
        unchanged = after_first == after and counts_first == state['uploads']
        assert_recovery_invariants(state, before, before_hashes, after, unchanged, validations_first)
        retry = {'ok': first['ok'] and second['ok']}
    except RuntimeError as failure:
        reason = 'unrelated failure'
        retry = {'ok': False}
        state['failure_recorded'] = str(failure)
    except ValueError as failure:
        reason = str(failure)
        retry = {'ok': False}
    event = {'event_type': 'artifact_ready', 'case_id': 'retained', 'artifact_id': 'A'}
    execution = execute(configured_build, trigger, event, {'recovery': lambda bindings: retry, 'required_validation': lambda bindings: {'ok': row['gate_ok'], 'required_gate_executed': True}, 'promotion': lambda bindings: {'ok': True}})
    stages = {s['id']: s for s in execution['steps']}
    retry_status = stages['recovery']['status']
    downstream_status = stages['required_validation']['status']
    if reason is not None:
        result = {'ok': False, 'reason': reason, 'before': before, 'uploads': state['uploads'], 'downstream_status': downstream_status}
        if reason == 'unrelated failure':
            result['failure_recorded'] = state['failure_recorded']
        return result
    ok = stages['promotion']['status'] == 'SUCCESS' and downstream_status == 'SUCCESS' and (retry_status == 'SUCCESS')
    return {'ok': ok, 'reason': None if ok else 'required gate rejected', 'failure_recorded': state['failure_recorded'], 'before': before, 'after': after, 'hashes': {k: hashlib.sha256(v['bytes']).hexdigest() for k, v in state['objects'].items()}, 'uploads': state['uploads'], 'validation_count': state['validations'], 'retry_status': retry_status, 'downstream_status': downstream_status, 'second_call_unchanged': unchanged}


exec(supplied_recover_source)

def recovery_run():
    resolved = reloaded_build
    assert resolved == configured_build
    assert resolved['steps'][0]['id'] == 'recovery'
    assert resolved['steps'][0]['name'] == 'python:3.11'
    assert resolved['steps'][0]['args'] == ['python', 'learner.py', '${_CASE}']
    assert resolved['steps'][0]['waitFor'] == ['-']
    assert resolved['steps'][1]['id'] == 'required_validation'
    assert resolved['steps'][1]['name'] == 'python:3.11'
    assert resolved['steps'][1]['args'] == ['python', 'learner.py', '${_CASE}']
    assert resolved['steps'][1]['waitFor'] == ['recovery']
    assert resolved['steps'][2]['id'] == 'promotion'
    assert resolved['steps'][2]['name'] == 'python:3.11'
    assert resolved['steps'][2]['args'] == ['python', 'downstream_entry.py', '${_ARTIFACT}']
    assert resolved['steps'][2]['waitFor'] == ['required_validation']
    for step in resolved['steps']:
        assert not step.get('allowFailure')
        assert all((code == 0 for code in step.get('allowExitCodes', [])))
    evidence = {k: recover(v) for k, v in cases.items()}

    def action(b):
        rec = recover(cases.get(b['_CASE'], cases['unrelated_failure']))
        rec['ok'] = rec['ok'] or rec.get('reason') == 'required gate rejected'
        return rec

    def validation(b):
        row = cases.get(b['_CASE'], cases['unrelated_failure'])
        return {'ok': row['gate_ok'], 'resolved_artifact': b['_ARTIFACT'], 'required_gate_executed': True}
    runs = [execute(resolved, trigger, e, {'recovery': action, 'required_validation': validation}) for e in trigger['fixtures']]
    assert_recovery_run_fixtures(evidence, runs)
    return {'cases': evidence, 'config': resolved, 'runs': runs}


exec(supplied_recovery_run_source)

build_to_write = configured_build

candidate_build = __import__("copy").deepcopy(configured_build)

configured_build = initial_build

with open('exercise_configuration.yaml', 'w') as file_handle:
    yaml.safe_dump(configured_build, file_handle)

with open('exercise_configuration.yaml') as file_handle:
    reloaded_build = yaml.safe_load(file_handle)

def assert_recovery_run_fixtures(evidence, runs):
    assert evidence['accepted']['ok'] and evidence['boundary_completed']['ok'] and evidence['race_412']['ok']
    for k in ('invalid_existing', 'conflicting_content', 'rejected_gate', 'unrelated_failure'):
        assert not evidence[k]['ok']
    assert evidence['accepted']['failure_recorded'] == 'RecoverableFailure'
    assert evidence['race_412']['second_call_unchanged']
    assert runs[1]['steps'][-1]['status'] == 'NOT_STARTED'


result = recovery_run()