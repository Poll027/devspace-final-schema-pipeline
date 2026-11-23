# Fictional bounded in-process exercise; no hosted cloud runs or real credentials.
# Keep supplied fixtures and execution helpers unchanged.
cases = {'accepted': {'registry_version': '1', 'artifact_id': 'A', 'run_id': 'run.A', 'approval': {'approval_id': 'approval.A', 'registry_version': '1', 'artifact_id': 'A', 'authorized': True, 'accountable_identity': 'fixture-promoter'}, 'compatibility_ok': True, 'offline_validation_ok': True, 'staged_validation_ok': True, 'staged_artifact_id': 'A'}, 'unauthorized': {'registry_version': '1', 'artifact_id': 'A', 'run_id': 'run.A', 'approval': {'approval_id': 'approval.A', 'registry_version': '1', 'artifact_id': 'A', 'authorized': False, 'accountable_identity': 'fixture-promoter'}, 'compatibility_ok': True, 'offline_validation_ok': True, 'staged_validation_ok': True, 'staged_artifact_id': 'A'}, 'wrong_artifact': {'registry_version': '1', 'artifact_id': 'B', 'run_id': 'run.A', 'approval': {'approval_id': 'approval.A', 'registry_version': '1', 'artifact_id': 'A', 'authorized': True, 'accountable_identity': 'fixture-promoter'}, 'compatibility_ok': True, 'offline_validation_ok': True, 'staged_validation_ok': True, 'staged_artifact_id': 'A'}, 'failed_staging': {'registry_version': '1', 'artifact_id': 'A', 'run_id': 'run.A', 'approval': {'approval_id': 'approval.A', 'registry_version': '1', 'artifact_id': 'A', 'authorized': True, 'accountable_identity': 'fixture-promoter'}, 'compatibility_ok': True, 'offline_validation_ok': True, 'staged_validation_ok': False, 'staged_artifact_id': 'A'}}
contract = {'scope': 'fixture-promoter may promote approved artifact A, registry version 1, only', 'required_results': ['compatibility', 'offline_validation', 'staged_validation', 'authorization'], 'record_fields': ['approval', 'accountable_identity', 'registry_version', 'run_id', 'artifact_id', 'per_stage_results'], 'secret_reference_only': 'PROMOTION_TOKEN is provided only by the authorized runtime to production. Do not serialize or echo it; inspect captured output without displaying its value. The local adapter never supplies real credentials.'}
trigger = {'id': 'fixture-artifact-trigger', 'topic': 'projects/fixture-project/topics/artifacts', 'bindings': {'_CASE': 'case_id', '_ARTIFACT': 'artifact_id'}, 'filters': {'event_type': 'artifact_ready'}, 'fixtures': [{'event_type': 'artifact_ready', 'case_id': 'accepted', 'artifact_id': 'A'}, {'event_type': 'artifact_ready', 'case_id': 'unauthorized', 'artifact_id': 'A'}, {'event_type': 'unrelated', 'case_id': 'accepted', 'artifact_id': 'A'}]}
contract_stage_results = ['compatibility', 'offline_validation', 'staged_validation', 'authorization']
registry_records = {'1': {'model_name': 'fixture_model', 'version': '1', 'artifact_id': 'A', 'artifact_source': 'gs://fixture-artifacts/A.txt', 'generation': 1, 'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6', 'run_id': 'run.A'}}
approved_secret_references = [{'versionName': 'projects/fixture-project/secrets/promotion-token/versions/1', 'env': 'PROMOTION_TOKEN'}]
captured_output = {'stdout': 'staging accepted; authorized promotion recorded for A', 'stderr': ''}
adapter_source = 'import io\nimport yaml\ndef roundtrip(build):\n    stream = io.StringIO()\n    yaml.safe_dump(build, stream)\n    stream.seek(0)\n    return yaml.safe_load(stream)\n\ndef execute(config, trigger, event, actions):\n    import re\n    if "branch_filter" in trigger:\n        if re.fullmatch(trigger["branch_filter"], event.get("branch", "")) is None:\n            return {"triggered": False, "steps": []}\n    else:\n        if any(event.get(k) != v for k,v in trigger["filters"].items()):\n            return {"triggered": False, "steps": []}\n    binding = dict(config.get("substitutions", {}))\n    binding.update({k:event[v] for k,v in trigger["bindings"].items()})\n    results=[]; statuses={}\n    for step in config["steps"]:\n        args=[str(a) for a in step.get("args", [])]\n        for k,v in binding.items():\n            args=[a.replace("${"+k+"}",str(v)) for a in args]\n        deps=[x for x in step["waitFor"] if x!="-"]\n        record={"id":step["id"],"name":step["name"],"resolved_args":args,"waitFor":deps}\n        if any(statuses.get(d)!="SUCCESS" for d in deps):\n            record.update(status="NOT_STARTED",exit_code=None,evidence=None)\n        else:\n            if step.get("allowFailure") or any(x!=0 for x in step.get("allowExitCodes",[])):\n                raise ValueError("required gate failure allowances are forbidden")\n            callback=actions.get(step["id"])\n            context=dict(binding);context["_RESOLVED_ARGS"]=args\n            result=callback(context) if callback else {"ok":True}\n            record.update(status="SUCCESS" if result["ok"] else "FAILURE",exit_code=0 if result["ok"] else 1,evidence=result)\n        statuses[step["id"]]=record["status"];results.append(record)\n    return {"triggered":True,"bindings":binding,"steps":results}\n\ndef promotion_gate(row):\n    approval=row["approval"];r=registry_records.get(row["registry_version"],{})\n    stage={"compatibility":row["compatibility_ok"],"offline_validation":row["offline_validation_ok"],"staged_validation":row["staged_validation_ok"],"authorization":approval["authorized"]}\n    identities=row["artifact_id"]==row["staged_artifact_id"]==approval["artifact_id"]==r.get("artifact_id") and row["registry_version"]==approval["registry_version"]==r.get("version") and row["run_id"]==r.get("run_id")\n    ok=identities and all(stage.get(k,False) for k in required_stage_results) and set(required_stage_results)==set(stage)\n    record={k:copy.deepcopy(row[k]) for k in ("approval","registry_version","run_id","artifact_id")}\n    record["accountable_identity"]=approval["accountable_identity"]\n    record["per_stage_results"]=stage\n    return {"ok":ok,"identity_matches":identities,"record":record}\n\ndef exercise_case(case_id):\n    all_evidence = promotion_run()\n    return {"case":all_evidence["cases"].get(case_id, {"ok":False,"reason":"missing case"}),"all_evidence":all_evidence}\n'
exec(adapter_source)

# Learner-authored imports, configuration edits, implementations and assertions.

# TODO: write required imports.
# TODO: write required imports.

required_stage_results = list(contract["required_results"])
configured_build = {'steps': [{'id': 'compatibility', 'name': 'python:3.11', 'args': ['python', 'learner.py', '${_CASE}'], 'waitFor': ['-']}, {'id': 'staging_quality', 'name': 'python:3.11', 'args': ['python', 'learner.py', '${_CASE}'], 'waitFor': []}, {'id': 'authorization', 'name': 'python:3.11', 'args': ['python', 'learner.py', '${_CASE}'], 'waitFor': []}, {'id': 'production', 'name': 'python:3.11', 'args': ['python', 'downstream_entry.py', 'TODO_APPROVED_ARTIFACT_REFERENCE'], 'waitFor': []}], 'substitutions': {'_SNAPSHOT': 'valid', '_CASE': 'accepted', '_ARTIFACT': 'A'}, 'serviceAccount': 'projects/fixture-project/serviceAccounts/fixture-build@fixture-project.iam.gserviceaccount.com'}
# TODO: edit required dependency / artifact / secret configuration fields.
pass
# TODO: edit required dependency / artifact / secret configuration fields.
pass
# TODO: edit required dependency / artifact / secret configuration fields.
pass
# TODO: edit required dependency / artifact / secret configuration fields.
pass
# TODO: edit required dependency / artifact / secret configuration fields.
pass
# TODO: edit required dependency / artifact / secret configuration fields.
pass

def promotion_run():
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
    evidence={k:promotion_gate(v) for k,v in cases.items()}
    def action(b):
        row=cases.get(b["_CASE"])
        if row is None:return {"ok":False,"reason":"unknown case"}
        result=promotion_gate(row)
        result["event_identity_matches"]=row["artifact_id"]==b["_ARTIFACT"]
        result["ok"]=result["ok"] and result["event_identity_matches"]
        return result
    def compatibility(b):
        row=cases.get(b["_CASE"])
        return {"ok":bool(row and row["compatibility_ok"]),"stage":"compatibility"}
    def staging(b):
        row=cases.get(b["_CASE"])
        return {"ok":bool(row and row["offline_validation_ok"] and row["staged_validation_ok"] and row["staged_artifact_id"]==b["_ARTIFACT"]),"stage":"staging_quality"}
    runs=[execute(resolved,trigger,e,{"compatibility":compatibility,"staging_quality":staging,"authorization":action,"production":action}) for e in trigger["fixtures"]]
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: inspect configuration and captured stdout/stderr without displaying credentials.
    production = None
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: inspect configuration and captured stdout/stderr without displaying credentials.
    serialized = None
    # TODO: inspect configuration and captured stdout/stderr without displaying credentials.
    credential_value_serialized = None
    # TODO: inspect configuration and captured stdout/stderr without displaying credentials.
    credential_value_echoed = None
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: inspect configuration and captured stdout/stderr without displaying credentials.
    approved_secret = None
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: write the configuration or fixture assertion here.
    pass
    for case in evidence.values():
        # TODO: write the configuration or fixture assertion here.
        pass
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: write the configuration or fixture assertion here.
    pass
    return {"cases":evidence,"config":resolved,"runs":runs,"credential_value_serialized":credential_value_serialized,"credential_value_echoed":credential_value_echoed}


result = promotion_run()
