
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

def promotion_gate(row):
    approval=row["approval"];r=registry_records.get(row["registry_version"],{})
    stage={"compatibility":row["compatibility_ok"],"offline_validation":row["offline_validation_ok"],"staged_validation":row["staged_validation_ok"],"authorization":approval["authorized"]}
    identities=row["artifact_id"]==row["staged_artifact_id"]==approval["artifact_id"]==r.get("artifact_id") and row["registry_version"]==approval["registry_version"]==r.get("version") and row["run_id"]==r.get("run_id")
    ok=identities and all(stage.get(k,False) for k in required_stage_results) and set(required_stage_results)==set(stage)
    record={k:copy.deepcopy(row[k]) for k in ("approval","registry_version","run_id","artifact_id")}
    record["accountable_identity"]=approval["accountable_identity"]
    record["per_stage_results"]=stage
    return {"ok":ok,"identity_matches":identities,"record":record}

def promotion_run():
    resolved=roundtrip(configured_build)
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
    assert evidence["accepted"]["ok"]
    assert all(not v["ok"] for k,v in evidence.items() if k!="accepted")
    production=[s for s in resolved["steps"] if s["id"]=="production"][0]
    assert production["secretEnv"]==["PROMOTION_TOKEN"]
    assert all("secretEnv" not in s for s in resolved["steps"] if s["id"]!="production")
    return {"cases":evidence,"config":resolved,"runs":runs,"credential_value_serialized":False,"credential_value_echoed":False}

def exercise_case(case_id):
    all_evidence = promotion_run()
    return {"case":all_evidence["cases"].get(case_id, {"ok":False,"reason":"missing case"}),"all_evidence":all_evidence}
