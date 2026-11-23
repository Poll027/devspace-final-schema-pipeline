
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

def dependency_checks(record):
    edges={p+"->"+c:record[p]["produced"]==record[c]["consumed"] for p,c in required_edges}
    checks=dict(edges)
    checks["data_validation"]=record["data_validation"]["validation_ok"]
    checks["model_validation"]=record["model_validation"]["validation_ok"]
    return {"ok":all(checks.values()),"checks":checks,"record":record}

def dependency_run():
    resolved=roundtrip(configured_build)
    evidence={k:dependency_checks(v) for k,v in cases.items()}
    repaired=copy.deepcopy(cases["mismatch"])
    repaired["model_validation"]["consumed"]=repaired["training"]["produced"]
    repair=dependency_checks(repaired)
    def data_action(b):
        row=cases.get(b["_CASE"],cases["mismatch"])
        return {"ok":row["data_validation"]["validation_ok"],"consumed":row["data_validation"]["consumed"],"produced":row["data_validation"]["produced"],"parameters":row["data_validation"]["parameters"]}
    def training_action(b):
        row=cases.get(b["_CASE"],cases["mismatch"])
        return {"ok":row["data_validation"]["produced"]==row["training"]["consumed"],"consumed":row["training"]["consumed"],"produced":b["_RESOLVED_ARGS"][-1],"parameters":row["training"]["parameters"]}
    def model_action(b):
        row=cases.get(b["_CASE"],cases["mismatch"])
        record=dependency_checks(row)
        record["resolved_consumer_matches_producer"]=b["_RESOLVED_ARGS"][-1]==b["_ARTIFACT"]==row["training"]["produced"]==row["model_validation"]["consumed"]
        record["ok"]=record["ok"] and record["resolved_consumer_matches_producer"]
        return record
    runs=[execute(resolved,trigger,e,{"data_validation":data_action,"training":training_action,"model_validation":model_action}) for e in trigger["fixtures"]]
    assert evidence["valid"]["ok"] and evidence["boundary"]["ok"]
    assert not evidence["mismatch"]["ok"] and not evidence["rejected_data"]["ok"]
    assert repair["ok"]
    assert [s["status"] for s in runs[-2]["steps"]]==["FAILURE","NOT_STARTED","NOT_STARTED"]
    for run in runs:
        if run["triggered"]:
            for step in run["steps"]:
                if step["status"]=="SUCCESS":
                    assert step["resolved_args"]
    return {"cases":evidence,"repaired":repair,"required_edges":required_edges,"config":resolved,"runs":runs}

def exercise_case(case_id):
    all_evidence = dependency_run()
    return {"case":all_evidence["cases"].get(case_id, {"ok":False,"reason":"missing case"}),"all_evidence":all_evidence}
