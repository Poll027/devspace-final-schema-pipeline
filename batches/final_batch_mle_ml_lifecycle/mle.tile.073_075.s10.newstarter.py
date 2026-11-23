# Fictional bounded in-process exercise; no hosted cloud runs or real credentials.
# Keep supplied fixtures and execution helpers unchanged.
cases = {'valid': {'inputs': [{'sample_id': 'sample.201', 'feature': 0}, {'sample_id': 'sample.202', 'feature': 1}, {'sample_id': 'sample.203', 'feature': 2}, {'sample_id': 'sample.204', 'feature': 5}], 'expected_sample_ids': ['sample.201', 'sample.202', 'sample.203', 'sample.204'], 'expected_values': [[0.0], [0.0], [1.0], [1.0]], 'expected_shape': [4, 1]}, 'boundary_low': {'inputs': [{'sample_id': 'sample.201', 'feature': 0}], 'expected_sample_ids': ['sample.201'], 'expected_values': [[0.0]], 'expected_shape': [1, 1]}, 'boundary_high': {'inputs': [{'sample_id': 'sample.204', 'feature': 5}], 'expected_sample_ids': ['sample.204'], 'expected_values': [[1.0]], 'expected_shape': [1, 1]}, 'empty': {'inputs': [], 'expected_sample_ids': [], 'expected_values': [], 'expected_shape': [0, 1]}, 'malformed': {'inputs': [{'sample_id': 'sample.203', 'feature': 'bad'}], 'expected_exception': 'InputContractError'}, 'missing_feature': {'inputs': [{'sample_id': 'sample.203'}], 'expected_exception': 'InputContractError'}, 'out_of_bounds': {'inputs': [{'sample_id': 'sample.203', 'feature': -1}], 'expected_exception': 'InputContractError'}}
contract = {'rtol': 1e-07, 'atol': 1e-08, 'output_shape': '(n,1)', 'expected_correspondence': 'returned sample_ids exactly match fixture input order', 'empty_input': 'permitted with shape (0,1)', 'regressions': ['reverse_rows', 'wrong_shape', 'wrong_values', 'drops_row'], 'exception': 'prediction_package.InputContractError', 'order': 'check count, alignment and shape before assert_allclose'}
trigger = {'id': 'fixture-commit-trigger', 'repository': 'local_repo', 'branch_filter': '^main$', 'bindings': {'_SNAPSHOT': 'snapshot_id', '_CASE': 'case_id'}, 'fixtures': [{'branch': 'main', 'snapshot_id': 'valid', 'case_id': 'accepted'}, {'branch': 'main', 'snapshot_id': 'missing_required_feature', 'case_id': 'regressed'}, {'branch': 'other', 'snapshot_id': 'valid'}]}
relative_tolerance = 1e-07
absolute_tolerance = 1e-08
execution_cases = {'accepted': {'fixture_id': 'valid', 'regression': None}, 'regressed': {'fixture_id': 'valid', 'regression': 'reverse_rows'}}
package_bootstrap = 'import sys, types\nmodule = types.ModuleType(\'prediction_reference\')\nsys.modules[\'prediction_reference\'] = module\nexec(\'"""Underlying fitted preprocessing and inference, shared by the supplied package."""\\nimport math\\nclass InputContractError(ValueError):\\n    pass\\ndef predict_records(records):\\n    ids, values = [], []\\n    for row in records:\\n        if set(row) != {"sample_id", "feature"}:\\n            raise InputContractError("required input columns")\\n        x = row["feature"]\\n        if isinstance(x, bool) or not isinstance(x, (int,float)) or not math.isfinite(x) or not 0 <= x <= 5:\\n            raise InputContractError("feature must be finite in [0,5]")\\n        ids.append(row["sample_id"])\\n        values.append([float(x / 5.0 >= 0.4)])\\n    return {"sample_ids": ids, "values": values}\\n\', module.__dict__)\nmodule = types.ModuleType(\'prediction_package\')\nsys.modules[\'prediction_package\'] = module\nexec(\'"""Supplied fitted package, including preprocessing through its inference path."""\\nimport numpy as np\\nfrom prediction_reference import predict_records, InputContractError\\nclass FittedPackage:\\n    def __init__(self, regression=None):\\n        self.regression = regression\\n    def predict(self, records):\\n        result = predict_records(records)\\n        ids = result["sample_ids"]\\n        values = np.array(result["values"], dtype=float).reshape((-1,1))\\n        if self.regression == "reverse_rows":\\n            ids, values = ids[::-1], values[::-1]\\n        elif self.regression == "wrong_shape":\\n            values = values.ravel()\\n        elif self.regression == "wrong_values":\\n            values = values + 0.1\\n        elif self.regression == "drops_row":\\n            ids, values = ids[:-1], values[:-1]\\n        return {"sample_ids": ids, "values": values}\\npredict = FittedPackage().predict\\n\', module.__dict__)\n'
exec(package_bootstrap)
adapter_source = 'import io\nimport yaml\ndef roundtrip(build):\n    stream = io.StringIO()\n    yaml.safe_dump(build, stream)\n    stream.seek(0)\n    return yaml.safe_load(stream)\n\ndef execute(config, trigger, event, actions):\n    import re\n    if "branch_filter" in trigger:\n        if re.fullmatch(trigger["branch_filter"], event.get("branch", "")) is None:\n            return {"triggered": False, "steps": []}\n    else:\n        if any(event.get(k) != v for k,v in trigger["filters"].items()):\n            return {"triggered": False, "steps": []}\n    binding = dict(config.get("substitutions", {}))\n    binding.update({k:event[v] for k,v in trigger["bindings"].items()})\n    results=[]; statuses={}\n    for step in config["steps"]:\n        args=[str(a) for a in step.get("args", [])]\n        for k,v in binding.items():\n            args=[a.replace("${"+k+"}",str(v)) for a in args]\n        deps=[x for x in step["waitFor"] if x!="-"]\n        record={"id":step["id"],"name":step["name"],"resolved_args":args,"waitFor":deps}\n        if any(statuses.get(d)!="SUCCESS" for d in deps):\n            record.update(status="NOT_STARTED",exit_code=None,evidence=None)\n        else:\n            if step.get("allowFailure") or any(x!=0 for x in step.get("allowExitCodes",[])):\n                raise ValueError("required gate failure allowances are forbidden")\n            callback=actions.get(step["id"])\n            context=dict(binding);context["_RESOLVED_ARGS"]=args\n            result=callback(context) if callback else {"ok":True}\n            record.update(status="SUCCESS" if result["ok"] else "FAILURE",exit_code=0 if result["ok"] else 1,evidence=result)\n        statuses[step["id"]]=record["status"];results.append(record)\n    return {"triggered":True,"bindings":binding,"steps":results}\n\ndef exercise_case(case_id):\n    all_evidence = behavior_run()\n    return {"case":all_evidence["cases"].get(case_id, {"ok":False,"reason":"missing case"}),"all_evidence":all_evidence}\n'
exec(adapter_source)

# Learner-authored imports, configuration edits, implementations and assertions.

# TODO: write required imports.
# TODO: write required imports.
# TODO: write required imports.
# TODO: write required imports.

configured_build = {'steps': [{'id': 'behavior_tests', 'name': 'python:3.11', 'args': ['python', 'learner.py', '${_CASE}'], 'waitFor': ['-']}, {'id': 'release_gate', 'name': 'python:3.11', 'args': ['python', 'downstream_entry.py', '${_ARTIFACT}'], 'waitFor': []}], 'substitutions': {'_SNAPSHOT': 'valid', '_CASE': 'accepted', '_ARTIFACT': 'A'}, 'serviceAccount': 'projects/fixture-project/serviceAccounts/fixture-build@fixture-project.iam.gserviceaccount.com'}
# TODO: edit required dependency / artifact / secret configuration fields.
pass

def behavior_test(case,regression=None):
    # TODO: implement behavior_test using the supplied contract and fixtures.
    raise NotImplementedError("learner implementation required")

def behavior_run():
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
    evidence={k:behavior_test(v) for k,v in cases.items()}
    regressions={r:behavior_test(cases["valid"],r) for r in contract["regressions"]}
    def action(b):
        rec=execution_cases.get(b["_CASE"])
        return behavior_test(cases[rec["fixture_id"]],rec["regression"]) if rec else {"ok":False,"failed":"unknown event case"}
    runs=[execute(resolved,trigger,e,{"behavior_tests":action}) for e in trigger["fixtures"]]
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: write the configuration or fixture assertion here.
    pass
    # TODO: write the configuration or fixture assertion here.
    pass
    return {"cases":evidence,"regressions":regressions,"tolerances":{"rtol":relative_tolerance,"atol":absolute_tolerance},"config":resolved,"runs":runs}


result = behavior_run()
