# Fictional bounded in-process exercise; no hosted cloud runs or real credentials.
# Keep supplied fixtures and execution helpers unchanged.
cases = {'valid': {'snapshot_id': 'snapshot.valid', 'sha256': '9a80d8aba1a479286779fd296606d795b9d7b91cfc0feaceacddeaffa24b8572', 'rows': [{'sample_id': 'sample.101', 'feature': 0, 'label': 0}, {'sample_id': 'sample.102', 'feature': 1, 'label': 0}, {'sample_id': 'sample.103', 'feature': 2, 'label': 1}, {'sample_id': 'sample.104', 'feature': 3, 'label': 1}, {'sample_id': 'sample.105', 'feature': 4, 'label': 1}, {'sample_id': 'sample.106', 'feature': 5, 'label': 1}]}, 'boundary': {'snapshot_id': 'snapshot.boundary', 'sha256': 'c81549aaab713d3575bd3451098b0ab3ee279d25cbb02cae30cad01b31e868a7', 'rows': [{'sample_id': 'sample.101', 'feature': 0, 'label': 0}, {'sample_id': 'sample.106', 'feature': 5, 'label': 1}]}, 'missing_required_feature': {'snapshot_id': 'snapshot.missing_required_feature', 'sha256': '09398d2fd8847ec08e07b24bc0cd5cfc4f10e9f7ac6c9bc3e6c507ad8f8e1257', 'rows': [{'sample_id': 'sample.101', 'label': 0}, {'sample_id': 'sample.102', 'label': 0}, {'sample_id': 'sample.103', 'label': 1}, {'sample_id': 'sample.104', 'label': 1}, {'sample_id': 'sample.105', 'label': 1}, {'sample_id': 'sample.106', 'label': 1}]}, 'unexpected_feature': {'snapshot_id': 'snapshot.unexpected_feature', 'sha256': '057671d877a61bee1e3aee03fba3b290deab50f1a6de31d4793382768386af90', 'rows': [{'sample_id': 'sample.101', 'feature': 0, 'label': 0, 'extra': 1}, {'sample_id': 'sample.102', 'feature': 1, 'label': 0, 'extra': 1}, {'sample_id': 'sample.103', 'feature': 2, 'label': 1, 'extra': 1}, {'sample_id': 'sample.104', 'feature': 3, 'label': 1, 'extra': 1}, {'sample_id': 'sample.105', 'feature': 4, 'label': 1, 'extra': 1}, {'sample_id': 'sample.106', 'feature': 5, 'label': 1, 'extra': 1}]}, 'invalid_feature': {'snapshot_id': 'snapshot.invalid_feature', 'sha256': '56bae9661e829f0a8aca48f80561bdeb123014f4f5994765a853a98bc6894984', 'rows': [{'sample_id': 'sample.101', 'feature': 0, 'label': 0}, {'sample_id': 'sample.102', 'feature': 1, 'label': 0}, {'sample_id': 'sample.103', 'feature': -1, 'label': 1}, {'sample_id': 'sample.104', 'feature': 3, 'label': 1}, {'sample_id': 'sample.105', 'feature': 4, 'label': 1}, {'sample_id': 'sample.106', 'feature': 5, 'label': 1}]}, 'missing_value': {'snapshot_id': 'snapshot.missing_value', 'sha256': 'd94863c4f043e3bd39e094416882b06d61af509d5ad40d905dab17604f9e8bec', 'rows': [{'sample_id': 'sample.101', 'feature': 0, 'label': 0}, {'sample_id': 'sample.102', 'feature': 1, 'label': 0}, {'sample_id': 'sample.103', 'feature': 2, 'label': 1}, {'sample_id': 'sample.104', 'feature': None, 'label': 1}, {'sample_id': 'sample.105', 'feature': 4, 'label': 1}, {'sample_id': 'sample.106', 'feature': 5, 'label': 1}]}, 'duplicate_sample': {'snapshot_id': 'snapshot.duplicate_sample', 'sha256': '7e1e2cd307a9d9c17f1a84ec4b93d807206deeeab580a7c0d35a9c63af7d9597', 'rows': [{'sample_id': 'sample.101', 'feature': 0, 'label': 0}, {'sample_id': 'sample.102', 'feature': 1, 'label': 0}, {'sample_id': 'sample.103', 'feature': 2, 'label': 1}, {'sample_id': 'sample.104', 'feature': 3, 'label': 1}, {'sample_id': 'sample.105', 'feature': 4, 'label': 1}, {'sample_id': 'sample.106', 'feature': 5, 'label': 1}, {'sample_id': 'sample.102', 'feature': 1, 'label': 0}]}}
contract = {'columns': {'sample_id': 'unique nonempty string label', 'feature': 'finite number in [0,5], inclusive', 'label': 'integer category 0 or 1'}, 'schema_policy': 'exactly declared columns', 'required_checks': ['schema', 'feature_values', 'label_values', 'unique_sample_id'], 'gate_policy': 'all required named checks must be present and true; otherwise raise or exit nonzero', 'evidence': 'retain snapshot_id, sha256, named results and failed checks; repaired inputs use unchanged requirements'}
trigger = {'id': 'fixture-commit-trigger', 'repository': 'local_repo', 'branch_filter': '^main$', 'bindings': {'_SNAPSHOT': 'snapshot_id'}, 'fixtures': [{'branch': 'main', 'snapshot_id': 'valid'}, {'branch': 'main', 'snapshot_id': 'missing_required_feature'}, {'branch': 'other', 'snapshot_id': 'valid'}]}
required_checks = ['schema', 'feature_values', 'label_values', 'unique_sample_id']
feature_min = 0
feature_max = 5
adapter_source = 'import io\nimport yaml\ndef roundtrip(build):\n    stream = io.StringIO()\n    yaml.safe_dump(build, stream)\n    stream.seek(0)\n    return yaml.safe_load(stream)\n\ndef execute(config, trigger, event, actions):\n    import re\n    if "branch_filter" in trigger:\n        if re.fullmatch(trigger["branch_filter"], event.get("branch", "")) is None:\n            return {"triggered": False, "steps": []}\n    else:\n        if any(event.get(k) != v for k,v in trigger["filters"].items()):\n            return {"triggered": False, "steps": []}\n    binding = dict(config.get("substitutions", {}))\n    binding.update({k:event[v] for k,v in trigger["bindings"].items()})\n    results=[]; statuses={}\n    for step in config["steps"]:\n        args=[str(a) for a in step.get("args", [])]\n        for k,v in binding.items():\n            args=[a.replace("${"+k+"}",str(v)) for a in args]\n        deps=[x for x in step["waitFor"] if x!="-"]\n        record={"id":step["id"],"name":step["name"],"resolved_args":args,"waitFor":deps}\n        if any(statuses.get(d)!="SUCCESS" for d in deps):\n            record.update(status="NOT_STARTED",exit_code=None,evidence=None)\n        else:\n            if step.get("allowFailure") or any(x!=0 for x in step.get("allowExitCodes",[])):\n                raise ValueError("required gate failure allowances are forbidden")\n            callback=actions.get(step["id"])\n            context=dict(binding);context["_RESOLVED_ARGS"]=args\n            result=callback(context) if callback else {"ok":True}\n            record.update(status="SUCCESS" if result["ok"] else "FAILURE",exit_code=0 if result["ok"] else 1,evidence=result)\n        statuses[step["id"]]=record["status"];results.append(record)\n    return {"triggered":True,"bindings":binding,"steps":results}\n\ndef exercise_case(case_id):\n    all_evidence = dataset_run()\n    return {"case":all_evidence["cases"].get(case_id, {"ok":False,"reason":"missing case"}),"all_evidence":all_evidence}\n'
exec(adapter_source)

# Learner-authored imports, configuration edits, implementations and assertions.

# TODO: write required imports.
# TODO: write required imports.

gate_checks = list(contract["required_checks"])
configured_build = {'steps': [{'id': 'quality', 'name': 'python:3.11', 'args': ['python', 'learner.py', '${_SNAPSHOT}'], 'waitFor': ['-']}, {'id': 'training', 'name': 'python:3.11', 'args': ['python', 'training_entry.py', '${_SNAPSHOT}'], 'waitFor': []}], 'substitutions': {'_SNAPSHOT': 'valid', '_CASE': 'accepted', '_ARTIFACT': 'A'}, 'serviceAccount': 'projects/fixture-project/serviceAccounts/fixture-build@fixture-project.iam.gserviceaccount.com'}
# TODO: edit required dependency / artifact / secret configuration fields.
pass

def dataset_gate(case, rules):
    # TODO: implement dataset_gate using the supplied contract and fixtures.
    raise NotImplementedError("learner implementation required")

def dataset_run():
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
    evidence={k:dataset_gate(v,gate_checks) for k,v in cases.items()}
    events=trigger["fixtures"]
    runs=[execute(resolved,trigger,e,{"quality":lambda b:dataset_gate(cases.get(b["_SNAPSHOT"],{"rows":[],"snapshot_id":b["_SNAPSHOT"],"sha256":None}),gate_checks)}) for e in events]
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: write the configuration or fixture assertion here.
    pass
    for k in cases:
        if k not in ("valid","boundary"):
            # TODO: write the configuration or fixture assertion here.
            pass
            # TODO: write the configuration or fixture assertion here.
            pass
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: write the configuration or fixture assertion here.
    pass
    repaired=copy.deepcopy(cases["missing_required_feature"])
    repaired["rows"]=copy.deepcopy(cases["valid"]["rows"])
    repaired["snapshot_id"]=repaired["snapshot_id"]+".repaired"
    repaired["sha256"]=hashlib.sha256(json.dumps(repaired["rows"],sort_keys=True,separators=(",",":")).encode()).hexdigest()
    repair=dataset_gate(repaired,gate_checks)
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: write the configuration or fixture assertion here.
    pass
    return {"cases":evidence,"config":resolved,"runs":runs,"repaired_under_same_contract":repair}


result = dataset_run()
