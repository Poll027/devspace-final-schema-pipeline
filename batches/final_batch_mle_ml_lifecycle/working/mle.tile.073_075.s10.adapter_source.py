
import copy, json, math, hashlib, io
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

import numpy as np
from prediction_package import FittedPackage, InputContractError

def behavior_test(case,regression=None):
    try:
        actual=FittedPackage(regression).predict(case["inputs"])
        if "expected_exception" in case:return {"ok":False,"failed":"expected_exception"}
        if check_count:assert len(actual["sample_ids"])==len(case["inputs"]),"count"
        if check_alignment:assert actual["sample_ids"]==case["expected_sample_ids"],"alignment"
        if check_shape:assert list(actual["values"].shape)==case["expected_shape"],"shape"
        if check_values:
            np.testing.assert_allclose(actual["values"],np.array(case["expected_values"]).reshape(case["expected_shape"]),rtol=relative_tolerance,atol=absolute_tolerance)
        return {"ok":True,"sample_ids":actual["sample_ids"],"shape":list(actual["values"].shape),"values":actual["values"].tolist()}
    except InputContractError:
        return {"ok":"expected_exception" in case,"exception":"InputContractError"}
    except AssertionError as e:
        return {"ok":False,"failed":"numerical" if "Not equal" in str(e) else str(e)}

def behavior_run():
    resolved=roundtrip(configured_build)
    evidence={k:behavior_test(v) for k,v in cases.items()}
    regressions={r:behavior_test(cases["valid"],r) for r in contract["regressions"]}
    def action(b):
        rec=execution_cases.get(b["_CASE"])
        return behavior_test(cases[rec["fixture_id"]],rec["regression"]) if rec else {"ok":False,"failed":"unknown event case"}
    runs=[execute(resolved,trigger,e,{"behavior_tests":action}) for e in trigger["fixtures"]]
    assert all(v["ok"] for v in evidence.values())
    assert all(not v["ok"] for v in regressions.values())
    assert runs[0]["steps"][1]["status"]=="SUCCESS"
    assert runs[1]["steps"][1]["status"]=="NOT_STARTED"
    return {"cases":evidence,"regressions":regressions,"tolerances":{"rtol":relative_tolerance,"atol":absolute_tolerance},"config":resolved,"runs":runs}

def exercise_case(case_id):
    all_evidence = behavior_run()
    return {"case":all_evidence["cases"].get(case_id, {"ok":False,"reason":"missing case"}),"all_evidence":all_evidence}
