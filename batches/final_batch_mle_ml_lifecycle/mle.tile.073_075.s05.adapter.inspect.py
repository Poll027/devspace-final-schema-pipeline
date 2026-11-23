import io
import yaml
def roundtrip(build):
    stream = io.StringIO()
    yaml.safe_dump(build, stream)
    stream.seek(0)
    return yaml.safe_load(stream)

def execute(config, trigger, event, actions):
    import re
    if "branch_filter" in trigger:
        if re.fullmatch(trigger["branch_filter"], event.get("branch", "")) is None:
            return {"triggered": False, "steps": []}
    else:
        if any(event.get(k) != v for k,v in trigger["filters"].items()):
            return {"triggered": False, "steps": []}
    binding = dict(config.get("substitutions", {}))
    binding.update({k:event[v] for k,v in trigger["bindings"].items()})
    results=[]; statuses={}
    for step in config["steps"]:
        args=[str(a) for a in step.get("args", [])]
        for k,v in binding.items():
            args=[a.replace("${"+k+"}",str(v)) for a in args]
        deps=[x for x in step["waitFor"] if x!="-"]
        record={"id":step["id"],"name":step["name"],"resolved_args":args,"waitFor":deps}
        if any(statuses.get(d)!="SUCCESS" for d in deps):
            record.update(status="NOT_STARTED",exit_code=None,evidence=None)
        else:
            if step.get("allowFailure") or any(x!=0 for x in step.get("allowExitCodes",[])):
                raise ValueError("required gate failure allowances are forbidden")
            callback=actions.get(step["id"])
            context=dict(binding);context["_RESOLVED_ARGS"]=args
            result=callback(context) if callback else {"ok":True}
            record.update(status="SUCCESS" if result["ok"] else "FAILURE",exit_code=0 if result["ok"] else 1,evidence=result)
        statuses[step["id"]]=record["status"];results.append(record)
    return {"triggered":True,"bindings":binding,"steps":results}

def exercise_case(case_id):
    all_evidence = dataset_run()
    return {"case":all_evidence["cases"].get(case_id, {"ok":False,"reason":"missing case"}),"all_evidence":all_evidence}

def dataset_gate(case, rules):
    rows = case['rows']
    result = {}
    result['schema'] = bool(rows) and all((set(r) == set(contract['columns']) for r in rows))
    result['feature_values'] = all((isinstance(r.get('feature'), (int, float)) and (not isinstance(r.get('feature'), bool)) and math.isfinite(r['feature']) and (feature_min <= r['feature'] <= feature_max) for r in rows))
    result['label_values'] = all((type(r.get('label')) is int and r['label'] in (0, 1) for r in rows))
    ids = [r.get('sample_id') for r in rows]
    result['unique_sample_id'] = all((isinstance(i, str) and i for i in ids)) and len(ids) == len(set(ids))
    failed = [k for k in contract['required_checks'] if k not in rules or not result.get(k, False)]
    return {'ok': not failed and set(rules) == set(contract['required_checks']), 'snapshot_id': case['snapshot_id'], 'sha256': case['sha256'], 'checks': result, 'failed_checks': failed}
def dataset_run():
    resolved = reloaded_build
    assert resolved == configured_build
    assert resolved['steps'][0]['id'] == 'quality'
    assert resolved['steps'][0]['name'] == 'python:3.11'
    assert resolved['steps'][0]['args'] == ['python', 'learner.py', '${_SNAPSHOT}']
    assert resolved['steps'][0]['waitFor'] == ['-']
    assert resolved['steps'][1]['id'] == 'training'
    assert resolved['steps'][1]['name'] == 'python:3.11'
    assert resolved['steps'][1]['args'] == ['python', 'training_entry.py', '${_SNAPSHOT}']
    assert resolved['steps'][1]['waitFor'] == ['quality']
    for step in resolved['steps']:
        assert not step.get('allowFailure')
        assert all((code == 0 for code in step.get('allowExitCodes', [])))
    evidence = {k: dataset_gate(v, gate_checks) for k, v in cases.items()}
    events = trigger['fixtures']
    runs = [execute(resolved, trigger, e, {'quality': lambda b: dataset_gate(cases.get(b['_SNAPSHOT'], {'rows': [], 'snapshot_id': b['_SNAPSHOT'], 'sha256': None}), gate_checks)}) for e in events]
    assert evidence['valid']['ok']
    assert evidence['boundary']['ok']
    for k in cases:
        if k not in ('valid', 'boundary'):
            assert not evidence[k]['ok']
            assert evidence[k]['failed_checks']
    assert runs[0]['steps'][1]['status'] == 'SUCCESS'
    assert runs[1]['steps'][1]['status'] == 'NOT_STARTED'
    repaired = copy.deepcopy(cases['missing_required_feature'])
    repaired['rows'] = copy.deepcopy(cases['valid']['rows'])
    repaired['snapshot_id'] = repaired['snapshot_id'] + '.repaired'
    repaired['sha256'] = hashlib.sha256(json.dumps(repaired['rows'], sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    repair = dataset_gate(repaired, gate_checks)
    assert repair['ok'] and repair['snapshot_id'] != evidence['missing_required_feature']['snapshot_id']
    assert repair['sha256'] != evidence['missing_required_feature']['sha256']
    assert not dataset_gate(cases['valid'], gate_checks[:-1])['ok']
    return {'cases': evidence, 'config': resolved, 'runs': runs, 'repaired_under_same_contract': repair}
