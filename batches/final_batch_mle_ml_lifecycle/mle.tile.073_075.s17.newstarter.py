# Fictional bounded in-process exercise; no hosted cloud runs or real credentials.
# Keep supplied fixtures and execution helpers unchanged.
cases = {'reference': {'candidate_id': 'reference', 'FP': 10, 'TN': 90, 'FN': 10, 'TP': 90, 'latency_ms': 18, 'operating_ok': True, 'evidence_complete': True}, 'A': {'candidate_id': 'A', 'FP': 5, 'TN': 95, 'FN': 5, 'TP': 95, 'latency_ms': 20, 'operating_ok': True, 'evidence_complete': True}, 'B': {'candidate_id': 'B', 'FP': 4, 'TN': 96, 'FN': 4, 'TP': 96, 'latency_ms': 21, 'operating_ok': True, 'evidence_complete': True}, 'boundary': {'candidate_id': 'boundary', 'FP': 10, 'TN': 90, 'FN': 10, 'TP': 90, 'latency_ms': 20, 'operating_ok': True, 'evidence_complete': True}, 'empty_negatives': {'candidate_id': 'empty_negatives', 'FP': 0, 'TN': 0, 'FN': 5, 'TP': 95, 'latency_ms': 15, 'operating_ok': True, 'evidence_complete': True}, 'empty_positives': {'candidate_id': 'empty_positives', 'FP': 5, 'TN': 95, 'FN': 0, 'TP': 0, 'latency_ms': 15, 'operating_ok': True, 'evidence_complete': True}, 'incomplete': {'candidate_id': 'incomplete', 'FP': 5, 'TN': 95, 'FN': 5, 'TP': 95, 'latency_ms': None, 'operating_ok': True, 'evidence_complete': False}, 'cost_failure': {'candidate_id': 'cost_failure', 'FP': 40, 'TN': 60, 'FN': 40, 'TP': 60, 'latency_ms': 15, 'operating_ok': True, 'evidence_complete': True}, 'operating_failure': {'candidate_id': 'operating_failure', 'FP': 5, 'TN': 95, 'FN': 5, 'TP': 95, 'latency_ms': 15, 'operating_ok': False, 'evidence_complete': True}, 'missing_field': {'candidate_id': 'A', 'TN': 95, 'FN': 5, 'TP': 95, 'latency_ms': 20, 'operating_ok': True, 'evidence_complete': True}, 'invalid_count': {'candidate_id': 'A', 'FP': -5, 'TN': 95, 'FN': 5, 'TP': 95, 'latency_ms': 20, 'operating_ok': True, 'evidence_complete': True}, 'case_artifact_mismatch': {'candidate_id': 'B', 'FP': 4, 'TN': 96, 'FN': 4, 'TP': 96, 'latency_ms': 20, 'operating_ok': True, 'evidence_complete': True}}
contract = {'probabilities': {'P(Y=0)': 0.8, 'P(Y=1)': 0.2}, 'costs': {'cost_FP': 1, 'cost_FN': 4, 'correct_prediction': 0}, 'max_expected_error_cost': 0.16, 'max_latency_ms': 20, 'accepted_reference': 'reference', 'requirements': ['all evidence fields present', 'nonnegative integer counts', 'both actual-class denominators nonempty', 'candidate identity matches event', 'expected error cost <= fixed maximum and <= accepted reference cost', 'latency_ms <= fixed maximum', 'operating_ok is True', 'evidence_complete is True'], 'protected_test_use': 'Never fit, select, or tune using protected-test observations.'}
trigger = {'id': 'fixture-artifact-trigger', 'topic': 'projects/fixture-project/topics/artifacts', 'bindings': {'_CASE': 'case_id', '_ARTIFACT': 'artifact_id'}, 'filters': {'event_type': 'artifact_ready'}, 'fixtures': [{'event_type': 'artifact_ready', 'case_id': 'A', 'artifact_id': 'A'}, {'event_type': 'artifact_ready', 'case_id': 'B', 'artifact_id': 'B'}, {'event_type': 'unrelated', 'case_id': 'A', 'artifact_id': 'A'}, {'event_type': 'artifact_ready', 'case_id': 'case_artifact_mismatch', 'artifact_id': 'A'}]}
max_error_cost = 0.16
max_latency = 20
required_acceptance_checks = ['evidence', 'counts', 'denominators', 'identity', 'cost', 'latency', 'operating']
adapter_source = 'import io\nimport yaml\ndef roundtrip(build):\n    stream = io.StringIO()\n    yaml.safe_dump(build, stream)\n    stream.seek(0)\n    return yaml.safe_load(stream)\n\ndef execute(config, trigger, event, actions):\n    import re\n    if "branch_filter" in trigger:\n        if re.fullmatch(trigger["branch_filter"], event.get("branch", "")) is None:\n            return {"triggered": False, "steps": []}\n    else:\n        if any(event.get(k) != v for k,v in trigger["filters"].items()):\n            return {"triggered": False, "steps": []}\n    binding = dict(config.get("substitutions", {}))\n    binding.update({k:event[v] for k,v in trigger["bindings"].items()})\n    results=[]; statuses={}\n    for step in config["steps"]:\n        args=[str(a) for a in step.get("args", [])]\n        for k,v in binding.items():\n            args=[a.replace("${"+k+"}",str(v)) for a in args]\n        deps=[x for x in step["waitFor"] if x!="-"]\n        record={"id":step["id"],"name":step["name"],"resolved_args":args,"waitFor":deps}\n        if any(statuses.get(d)!="SUCCESS" for d in deps):\n            record.update(status="NOT_STARTED",exit_code=None,evidence=None)\n        else:\n            if step.get("allowFailure") or any(x!=0 for x in step.get("allowExitCodes",[])):\n                raise ValueError("required gate failure allowances are forbidden")\n            callback=actions.get(step["id"])\n            context=dict(binding);context["_RESOLVED_ARGS"]=args\n            result=callback(context) if callback else {"ok":True}\n            record.update(status="SUCCESS" if result["ok"] else "FAILURE",exit_code=0 if result["ok"] else 1,evidence=result)\n        statuses[step["id"]]=record["status"];results.append(record)\n    return {"triggered":True,"bindings":binding,"steps":results}\n\ndef exercise_case(case_id):\n    all_evidence = release_run()\n    return {"case":all_evidence["cases"].get(case_id, {"ok":False,"reason":"missing case"}),"all_evidence":all_evidence}\n'
exec(adapter_source)

# Learner-authored imports, configuration edits, implementations and assertions.

# TODO: write required imports.
# TODO: write required imports.
# TODO: write required imports.

acceptance_checks = list(required_acceptance_checks)
configured_build = {'steps': [{'id': 'release_gate', 'name': 'python:3.11', 'args': ['python', 'learner.py', '${_CASE}', '${_ARTIFACT}'], 'waitFor': ['-']}, {'id': 'promotion', 'name': 'python:3.11', 'args': ['python', 'downstream_entry.py', '${_ARTIFACT}'], 'waitFor': []}], 'substitutions': {'_SNAPSHOT': 'valid', '_CASE': 'A', '_ARTIFACT': 'A'}, 'serviceAccount': 'projects/fixture-project/serviceAccounts/fixture-build@fixture-project.iam.gserviceaccount.com'}
# TODO: edit required dependency / artifact / secret configuration fields.
pass

def error_cost(row):
    # TODO: implement error_cost using the supplied contract and fixtures.
    raise NotImplementedError("learner implementation required")

def release_gate(row,event_artifact):
    # TODO: implement release_gate using the supplied contract and fixtures.
    raise NotImplementedError("learner implementation required")

def release_run():
    # TODO: safely write/reload configured_build with PyYAML.
    resolved = None
    # TODO: safely write/reload configured_build with PyYAML.
    resolved = None
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: write the configuration or fixture assertion here.
    pass
    for step in resolved["steps"]:
        # TODO: write the configuration or fixture assertion here.
        pass
        # TODO: write the configuration or fixture assertion here.
        pass
    evidence={k:release_gate(v,(cases["A"]["candidate_id"] if k=="case_artifact_mismatch" else v.get("candidate_id"))) for k,v in cases.items()}
    def action(b):
        # TODO: implement action using the supplied contract and fixtures.
        raise NotImplementedError("learner implementation required")
    runs=[execute(resolved,trigger,e,{"release_gate":action}) for e in trigger["fixtures"]]
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: write the configuration or fixture assertion here.
    pass
    for k in ("empty_negatives","empty_positives","incomplete","cost_failure","operating_failure","missing_field","invalid_count","case_artifact_mismatch"):
        # TODO: write the configuration or fixture assertion here.
        pass
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: write the configuration or fixture assertion here.
    pass
    return {"cases":evidence,"config":resolved,"runs":runs,"protected_test_used":False}


result = release_run()
