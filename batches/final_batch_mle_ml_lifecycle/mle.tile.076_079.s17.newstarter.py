# Fictional bounded in-process exercise; no hosted cloud runs or real credentials.
# Keep supplied fixtures and execution helpers unchanged.
cases = {'accepted': {'initial_outputs': ['A'], 'race_outputs': [], 'invalid_outputs': [], 'gate_ok': True, 'exception': 'RecoverableFailure'}, 'boundary_completed': {'initial_outputs': ['A', 'B'], 'race_outputs': [], 'invalid_outputs': [], 'gate_ok': True, 'exception': None}, 'race_412': {'initial_outputs': ['A'], 'race_outputs': ['B'], 'invalid_outputs': [], 'gate_ok': True, 'exception': 'RecoverableFailure'}, 'invalid_existing': {'initial_outputs': ['A'], 'race_outputs': [], 'invalid_outputs': ['A'], 'gate_ok': True, 'exception': 'RecoverableFailure'}, 'conflicting_content': {'initial_outputs': ['A'], 'race_outputs': [], 'invalid_outputs': [], 'conflicting_outputs': ['A'], 'gate_ok': True, 'exception': 'RecoverableFailure'}, 'rejected_gate': {'initial_outputs': ['A'], 'race_outputs': [], 'invalid_outputs': [], 'gate_ok': False, 'exception': 'RecoverableFailure'}, 'unrelated_failure': {'initial_outputs': ['A'], 'race_outputs': [], 'invalid_outputs': [], 'gate_ok': True, 'exception': 'ValueError'}}
contract = {'injection_point': 'after A upload before B', 'recoverable_exception': 'storage_sim.RecoverableFailure', 'precondition_exception': 'storage_sim.PreconditionFailed', 'outputs': {'A': {'artifact_id': 'A', 'uri': 'gs://fixture-artifacts/A.txt', 'generation': 1, 'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6', 'validation_ok': True}, 'B': {'artifact_id': 'B', 'uri': 'gs://fixture-artifacts/B.txt', 'generation': 1, 'sha256': '6d5f5cbc73990d86a040e72f9e6d1cad2cb36297b10887e5444900c7286f634a', 'validation_ok': True}}, 'requirements': ['record and isolate failure', 'verify exact existing generation bytes/hash and validation', 'skip only verified completed upload', 'create missing output with if_generation_match=0', 'on 412 reload and verify, never overwrite', 'unrelated exceptions remain fatal', 'run retried stage and downstream required gates', 'second call preserves generations and upload counts but revalidates'], 'evidence_fields': ['initial_and_final_generations', 'hashes', 'validation_results', 'upload_counts', 'retry_status', 'downstream_status', 'resolved_inputs']}
trigger = {'id': 'fixture-artifact-trigger', 'topic': 'projects/fixture-project/topics/artifacts', 'bindings': {'_CASE': 'case_id', '_ARTIFACT': 'artifact_id'}, 'filters': {'event_type': 'artifact_ready'}, 'fixtures': [{'event_type': 'artifact_ready', 'case_id': 'accepted', 'artifact_id': 'A'}, {'event_type': 'artifact_ready', 'case_id': 'rejected_gate', 'artifact_id': 'A'}, {'event_type': 'unrelated', 'case_id': 'accepted', 'artifact_id': 'A'}]}
declared_outputs = ['A', 'B']
artifact_records = {'A': {'artifact_id': 'A', 'uri': 'gs://fixture-artifacts/A.txt', 'generation': 1, 'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6', 'validation_ok': True}, 'B': {'artifact_id': 'B', 'uri': 'gs://fixture-artifacts/B.txt', 'generation': 1, 'sha256': '6d5f5cbc73990d86a040e72f9e6d1cad2cb36297b10887e5444900c7286f634a', 'validation_ok': True}}
output_bytes = {'A': b'fictional fitted package A\npreprocess: divide feature by 5\nthreshold: 0.4\n', 'B': b'fictional fitted package B\npreprocess: divide feature by 5\nthreshold: 0.5\n'}
adapter_source = 'import io\nimport yaml\ndef roundtrip(build):\n    stream = io.StringIO()\n    yaml.safe_dump(build, stream)\n    stream.seek(0)\n    return yaml.safe_load(stream)\n\ndef execute(config, trigger, event, actions):\n    import re\n    if "branch_filter" in trigger:\n        if re.fullmatch(trigger["branch_filter"], event.get("branch", "")) is None:\n            return {"triggered": False, "steps": []}\n    else:\n        if any(event.get(k) != v for k,v in trigger["filters"].items()):\n            return {"triggered": False, "steps": []}\n    binding = dict(config.get("substitutions", {}))\n    binding.update({k:event[v] for k,v in trigger["bindings"].items()})\n    results=[]; statuses={}\n    for step in config["steps"]:\n        args=[str(a) for a in step.get("args", [])]\n        for k,v in binding.items():\n            args=[a.replace("${"+k+"}",str(v)) for a in args]\n        deps=[x for x in step["waitFor"] if x!="-"]\n        record={"id":step["id"],"name":step["name"],"resolved_args":args,"waitFor":deps}\n        if any(statuses.get(d)!="SUCCESS" for d in deps):\n            record.update(status="NOT_STARTED",exit_code=None,evidence=None)\n        else:\n            if step.get("allowFailure") or any(x!=0 for x in step.get("allowExitCodes",[])):\n                raise ValueError("required gate failure allowances are forbidden")\n            callback=actions.get(step["id"])\n            context=dict(binding);context["_RESOLVED_ARGS"]=args\n            result=callback(context) if callback else {"ok":True}\n            record.update(status="SUCCESS" if result["ok"] else "FAILURE",exit_code=0 if result["ok"] else 1,evidence=result)\n        statuses[step["id"]]=record["status"];results.append(record)\n    return {"triggered":True,"bindings":binding,"steps":results}\n\nclass RecoverableFailure(Exception):pass\n\nclass PreconditionFailed(Exception):status=412\n\nclass Blob:\n    def __init__(self,name,state):self.name=name;self.state=state;self.generation=None\n    def exists(self):return self.name in self.state["objects"]\n    def reload(self):self.generation=self.state["objects"][self.name]["generation"]\n    def download_as_bytes(self,if_generation_match):\n        obj=self.state["objects"][self.name]\n        if obj["generation"]!=if_generation_match:raise PreconditionFailed("generation changed")\n        return obj["bytes"]\n    def upload_from_filename(self,path,if_generation_match):\n        assert if_generation_match==0\n        if self.name in self.state["race"]:\n            self.state["objects"][self.name]={"generation":1,"bytes":output_bytes[self.name]}\n            self.state["race"].remove(self.name)\n            raise PreconditionFailed("race created object")\n        if self.exists():raise PreconditionFailed("object exists")\n        self.state["objects"][self.name]={"generation":1,"bytes":output_bytes[self.name]}\n        self.state["uploads"][self.name]+=1\n\ndef exercise_case(case_id):\n    all_evidence = recovery_run()\n    return {"case":all_evidence["cases"].get(case_id, {"ok":False,"reason":"missing case"}),"all_evidence":all_evidence}\n'
exec(adapter_source)

# Learner-authored imports, configuration edits, implementations and assertions.

# TODO: write required imports.
# TODO: write required imports.

recovery_outputs = list(declared_outputs)
configured_build = {'steps': [{'id': 'recovery', 'name': 'python:3.11', 'args': ['python', 'learner.py', '${_CASE}'], 'waitFor': ['-']}, {'id': 'required_validation', 'name': 'python:3.11', 'args': ['python', 'learner.py', '${_CASE}'], 'waitFor': []}, {'id': 'promotion', 'name': 'python:3.11', 'args': ['python', 'downstream_entry.py', '${_ARTIFACT}'], 'waitFor': []}], 'substitutions': {'_SNAPSHOT': 'valid', '_CASE': 'accepted', '_ARTIFACT': 'A'}, 'serviceAccount': 'projects/fixture-project/serviceAccounts/fixture-build@fixture-project.iam.gserviceaccount.com'}
# TODO: edit required dependency / artifact / secret configuration fields.
pass
# TODO: edit required dependency / artifact / secret configuration fields.
pass

def verify_output(blob, state, row):
    # TODO: implement verify_output using the supplied contract and fixtures.
    raise NotImplementedError("learner implementation required")

def recovery(state, row, inject_failure=False):
    # Only the named recoverable failure is caught here. Other exceptions propagate.
    # TODO: implement recovery using the supplied contract and fixtures.
    raise NotImplementedError("learner implementation required")

def recover(row):
    # Fixture runner retains one state across TWO distinct recovery invocations.
    state={"objects":{},"race":list(row["race_outputs"]),"uploads":{name:0 for name in declared_outputs},"validations":0,"failure_recorded":None}
    for name in row["initial_outputs"]:
        Blob(name,state).upload_from_filename("outputs/"+name+".txt",if_generation_match=0)
        if name in row.get("conflicting_outputs",[]): state["objects"][name]["bytes"]=b"conflicting content"
    before={k:v["generation"] for k,v in state["objects"].items()}
    before_hashes={k:hashlib.sha256(v["bytes"]).hexdigest() for k,v in state["objects"].items()}
    # TODO: invoke recovery twice on retained state; assert generation/hash and second-call invariance.
    # Execute required gates and derive retry/downstream statuses, preserving rejection evidence.
    raise NotImplementedError("recovery orchestration required")

def recovery_run():
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
    for step in resolved["steps"]:
        # TODO: write the configuration or fixture assertion here.
        pass
        # TODO: write the configuration or fixture assertion here.
        pass
    evidence={k:recover(v) for k,v in cases.items()}
    def action(b):
        rec=recover(cases.get(b["_CASE"],cases["unrelated_failure"]))
        rec["ok"]=rec["ok"] or rec.get("reason")=="required gate rejected"
        return rec
    def validation(b):
        row=cases.get(b["_CASE"],cases["unrelated_failure"])
        return {"ok":row["gate_ok"],"resolved_artifact":b["_ARTIFACT"],"required_gate_executed":True}
    runs=[execute(resolved,trigger,e,{"recovery":action,"required_validation":validation}) for e in trigger["fixtures"]]
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
    return {"cases":evidence,"config":resolved,"runs":runs}


result = recovery_run()
