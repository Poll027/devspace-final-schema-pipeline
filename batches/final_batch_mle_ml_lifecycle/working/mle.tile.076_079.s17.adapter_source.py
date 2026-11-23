
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

class RecoverableFailure(Exception):pass
class PreconditionFailed(Exception):status=412
class Blob:
    def __init__(self,name,state):self.name=name;self.state=state;self.generation=None
    def exists(self):return self.name in self.state["objects"]
    def reload(self):self.generation=self.state["objects"][self.name]["generation"]
    def download_as_bytes(self,if_generation_match):
        obj=self.state["objects"][self.name]
        if obj["generation"]!=if_generation_match:raise PreconditionFailed("generation changed")
        return obj["bytes"]
    def upload_from_filename(self,path,if_generation_match):
        assert if_generation_match==0
        if self.name in self.state["race"]:
            self.state["objects"][self.name]={"generation":1,"bytes":output_bytes[self.name]}
            self.state["race"].remove(self.name)
            raise PreconditionFailed("race created object")
        if self.exists():raise PreconditionFailed("object exists")
        self.state["objects"][self.name]={"generation":1,"bytes":output_bytes[self.name]}
        self.state["uploads"][self.name]+=1

def recover(row):
    state={"objects":{},"race":list(row["race_outputs"]),"uploads":{name:0 for name in declared_outputs},"validations":0}
    for name in row["initial_outputs"]:
        state["objects"][name]={"generation":1,"bytes":output_bytes[name] if name not in row.get("conflicting_outputs",[]) else b"conflicting content"}
    before={k:v["generation"] for k,v in state["objects"].items()}
    failure=row["exception"]
    if failure not in (None,"RecoverableFailure"):
        return {"ok":False,"reason":"unrelated failure","failure_recorded":failure,"before":before}
    def verify(blob):
        blob.reload();data=blob.download_as_bytes(if_generation_match=blob.generation)
        state["validations"]+=1
        if hashlib.sha256(data).hexdigest()!=artifact_records[blob.name]["sha256"]:raise ValueError("content conflict")
        if blob.name in row["invalid_outputs"] or not artifact_records[blob.name]["validation_ok"]:raise ValueError("validation failed")
    try:
        for attempt in (1,2):
            for name in recovery_outputs:
                blob=Blob(name,state)
                if blob.exists():verify(blob)
                else:
                    try:blob.upload_from_filename("outputs/"+name+".txt",if_generation_match=0)
                    except PreconditionFailed:verify(blob)
                    else:verify(blob)
            if attempt==1:
                after_first={k:v["generation"] for k,v in state["objects"].items()};counts_first=dict(state["uploads"])
        after={k:v["generation"] for k,v in state["objects"].items()}
        assert after_first==after and counts_first==state["uploads"]
        ok=set(recovery_outputs)==set(declared_outputs) and row["gate_ok"]
        return {"ok":ok,"reason":None if ok else "required gate rejected","failure_recorded":failure,"before":before,"after":after,"hashes":{k:hashlib.sha256(v["bytes"]).hexdigest() for k,v in state["objects"].items()},"uploads":state["uploads"],"validation_count":state["validations"],"retry_status":"SUCCESS","downstream_status":"SUCCESS" if ok else "FAILURE","second_call_unchanged":True}
    except ValueError as e:
        return {"ok":False,"reason":str(e),"before":before,"uploads":state["uploads"],"downstream_status":"NOT_STARTED"}

def recovery_run():
    resolved=roundtrip(configured_build)
    evidence={k:recover(v) for k,v in cases.items()}
    def action(b):
        rec=recover(cases.get(b["_CASE"],cases["unrelated_failure"]))
        rec["ok"]=rec["ok"] or rec.get("reason")=="required gate rejected"
        return rec
    def validation(b):
        row=cases.get(b["_CASE"],cases["unrelated_failure"])
        return {"ok":row["gate_ok"],"resolved_artifact":b["_ARTIFACT"],"required_gate_executed":True}
    runs=[execute(resolved,trigger,e,{"recovery":action,"required_validation":validation}) for e in trigger["fixtures"]]
    assert evidence["accepted"]["ok"] and evidence["boundary_completed"]["ok"] and evidence["race_412"]["ok"]
    for k in ("invalid_existing","conflicting_content","rejected_gate","unrelated_failure"):assert not evidence[k]["ok"]
    return {"cases":evidence,"config":resolved,"runs":runs}

def exercise_case(case_id):
    all_evidence = recovery_run()
    return {"case":all_evidence["cases"].get(case_id, {"ok":False,"reason":"missing case"}),"all_evidence":all_evidence}
