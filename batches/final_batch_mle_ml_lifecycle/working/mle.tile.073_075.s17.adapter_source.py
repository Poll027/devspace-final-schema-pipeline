
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

from decimal import Decimal
def error_cost(row):
    negatives=row["FP"]+row["TN"];positives=row["FN"]+row["TP"]
    if negatives<=0 or positives<=0:return None
    fpr=row["FP"]/negatives;fnr=row["FN"]/positives
    return {"FPR":fpr,"FNR":fnr,"expected_error_cost":float(Decimal(str(contract["probabilities"]["P(Y=0)"]))*Decimal(row["FP"])/Decimal(negatives)*Decimal(contract["costs"]["cost_FP"])+Decimal(str(contract["probabilities"]["P(Y=1)"]))*Decimal(row["FN"])/Decimal(positives)*Decimal(contract["costs"]["cost_FN"]))}

def release_gate(row,event_artifact):
    metrics=error_cost(row)
    checks={}
    checks["evidence"]=row.get("evidence_complete") is True and row.get("latency_ms") is not None
    checks["counts"]=all(type(row.get(k)) is int and row[k]>=0 for k in ("FP","TN","FN","TP"))
    checks["denominators"]=metrics is not None
    checks["identity"]=row["candidate_id"]==event_artifact
    checks["cost"]=metrics is not None and metrics["expected_error_cost"]<=max_error_cost and metrics["expected_error_cost"]<=error_cost(cases[contract["accepted_reference"]])["expected_error_cost"]
    checks["latency"]=row.get("latency_ms") is not None and row["latency_ms"]<=max_latency
    checks["operating"]=row.get("operating_ok") is True
    ok=all(checks.get(k,False) for k in acceptance_checks) and set(acceptance_checks)==set(checks)
    return {"ok":ok,"candidate_id":row["candidate_id"],"metrics":metrics,"checks":checks,"failed_checks":[k for k,v in checks.items() if not v]}

def release_run():
    resolved=roundtrip(configured_build)
    evidence={k:release_gate(v,v["candidate_id"]) for k,v in cases.items()}
    def action(b):
        r=cases.get(b["_ARTIFACT"])
        return release_gate(r,b["_ARTIFACT"]) if r else {"ok":False,"failed_checks":["missing candidate evidence"]}
    runs=[execute(resolved,trigger,e,{"release_gate":action}) for e in trigger["fixtures"]]
    assert evidence["A"]["ok"] and evidence["boundary"]["ok"]
    assert not evidence["B"]["ok"]
    for k in ("empty_negatives","empty_positives","incomplete","cost_failure","operating_failure"):
        assert not evidence[k]["ok"]
    assert runs[0]["steps"][1]["status"]=="SUCCESS"
    assert runs[1]["steps"][1]["status"]=="NOT_STARTED"
    return {"cases":evidence,"config":resolved,"runs":runs,"protected_test_used":False}

def exercise_case(case_id):
    all_evidence = release_run()
    return {"case":all_evidence["cases"].get(case_id, {"ok":False,"reason":"missing case"}),"all_evidence":all_evidence}
