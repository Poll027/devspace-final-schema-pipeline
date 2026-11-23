import json, copy, hashlib, math, sys
from pathlib import Path
B=Path(__file__).parent
plan=json.loads((B/'tile_plans.json').read_text())
screens=json.loads((B/'screens.json').read_text())
bundles={x['context']['concept_id']:x for x in json.loads((B/'inputs/path_glossary_bundle.json').read_text())['bundles']}
registry=json.loads((B/'scenario_asset_registry.json').read_text())
assets={a['asset_id']:a for a in registry['assets']}
runtimes=json.loads(Path('00_FINAL_PIPELINE_CORE/registry/runtimes.json').read_text())['runtimes']
def workspace(cid):
 return {f['path']:f['content'] for f in assets['ws.'+cid.split('.')[-1]]['files']}
def inp(files,path):return json.loads(files[path])
def literal_assignment(name,value):return name+' = '+repr(value)+'\n'
# In-process adapters replace child processes/storage, which cannot run in WASM.
# These are supplied scaffolding, not a learner solution or alleged hosted run.
COMMON='''
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
'''
DATASET='''
def dataset_gate(case, rules):
    rows=case["rows"]
    result={}
    result["schema"]=bool(rows) and all(set(r)==set(contract["columns"]) for r in rows)
    result["feature_values"]=all(isinstance(r.get("feature"),(int,float)) and not isinstance(r.get("feature"),bool) and math.isfinite(r["feature"]) and feature_min <= r["feature"] <= feature_max for r in rows)
    result["label_values"]=all(type(r.get("label")) is int and r["label"] in (0,1) for r in rows)
    ids=[r.get("sample_id") for r in rows]
    result["unique_sample_id"]=all(isinstance(i,str) and i for i in ids) and len(ids)==len(set(ids))
    failed=[k for k in rules if not result.get(k,False)]
    return {"ok":not failed and set(rules)==set(contract["required_checks"]),"snapshot_id":case["snapshot_id"],"sha256":case["sha256"],"checks":result,"failed_checks":failed}

def dataset_run():
    resolved=roundtrip(configured_build)
    evidence={k:dataset_gate(v,gate_checks) for k,v in cases.items()}
    events=trigger["fixtures"]
    runs=[execute(resolved,trigger,e,{"quality":lambda b:dataset_gate(cases.get(b["_SNAPSHOT"],{"rows":[],"snapshot_id":b["_SNAPSHOT"],"sha256":None}),gate_checks)}) for e in events]
    assert evidence["valid"]["ok"]
    assert evidence["boundary"]["ok"]
    for k in cases:
        if k not in ("valid","boundary"):
            assert not evidence[k]["ok"]
            assert evidence[k]["failed_checks"]
    assert runs[0]["steps"][1]["status"]=="SUCCESS"
    assert runs[1]["steps"][1]["status"]=="NOT_STARTED"
    repaired=copy.deepcopy(cases["missing_required_feature"])
    repaired["rows"]=copy.deepcopy(cases["valid"]["rows"])
    repaired["snapshot_id"]=repaired["snapshot_id"]+".repaired"
    repaired["sha256"]=hashlib.sha256(json.dumps(repaired["rows"],sort_keys=True,separators=(",",":")).encode()).hexdigest()
    repair=dataset_gate(repaired,gate_checks)
    return {"cases":evidence,"config":resolved,"runs":runs,"repaired_under_same_contract":repair}
'''
BEHAVIOR='''
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
'''
RELEASE='''
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
'''
DEPENDENCY='''
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
'''
PROMOTION='''
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
'''
RECOVERY='''
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
'''

def make_code(cid):
 f=workspace(cid); short=cid.split('.')[-1]
 build=inp(f,'cloudbuild.yaml'); trigger_all=inp(f,'triggers.json')
 required_build=copy.deepcopy(build)
 # Copy execution images and commands, derive explicit predecessor dependencies from the declared ordered stages.
 for i,s in enumerate(required_build['steps']):
  s['waitFor']=['-'] if i==0 else [required_build['steps'][i-1]['id']]
  s.pop('allowFailure',None);s.pop('allowExitCodes',None)
 if short=='pipeline_artifact_dependencies':
  dependency_valid=inp(f,'fixtures/dependency_cases.json')['valid']
  required_build['steps'][-1]['args'][-1]=dependency_valid['training']['produced']
 if short=='dataset_quality_gate':
  cases=inp(f,'fixtures/dataset_cases.json');contract=inp(f,'fixtures/dataset_contract.json');adapter=DATASET; run='dataset_run';trig=trigger_all['repository_commit']
  settings={'gate_checks':'required_checks','configured_build':'fatal_build'}
  pre=literal_assignment('required_checks',contract['required_checks'])+literal_assignment('feature_min',min(r['feature'] for r in cases['valid']['rows']))+literal_assignment('feature_max',max(r['feature'] for r in cases['valid']['rows']))
  task='Complete gate_checks and configured_build using the supplied candidate settings: keep all named schema, feature, label and unique-ID predicates and an explicit fatal training dependency. The supplied adapter aggregates these checks, retains snapshot identities and failed requirements, and executes accepted/rejected commit fixtures. Do not omit a required predicate. The result dictionary must include cases, config, runs and repaired_under_same_contract; inspect that the repaired missing-feature snapshot is tested against the unchanged contract.'
 elif short=='model_behavior_tests':
  cases=inp(f,'fixtures/behavior_cases.json');contract=inp(f,'fixtures/behavior_contract.json');adapter=BEHAVIOR;run='behavior_run';trig=trigger_all['repository_commit']
  # Stage registry has already fixed the _CASE binding for behavior execution.
  settings={'check_count':'enabled','check_alignment':'enabled','check_shape':'enabled','check_values':'enabled','configured_build':'fatal_build'}
  pre=literal_assignment('relative_tolerance',contract['rtol'])+literal_assignment('absolute_tolerance',contract['atol'])+literal_assignment('execution_cases',inp(f,'fixtures/behavior_execution_cases.json'))
  task='Complete check_count, check_alignment, check_shape, check_values and configured_build using the supplied candidate settings. Decide which structural/numerical checks and fatal dependencies are necessary to detect all declared regressions. The supplied fitted package includes its preprocessing. Structural checks run before assert_allclose with the supplied explicit tolerances. result must contain cases, regressions, tolerances, config and runs. Valid/boundary/empty fixtures and contract exceptions must pass; each planted package regression must fail and block the dependent stage.'
 elif short=='model_release_quality_gate':
  cases=inp(f,'fixtures/release_cases.json');contract=inp(f,'fixtures/release_contract.json');adapter=RELEASE;run='release_run';trig=trigger_all['pubsub']
  settings={'acceptance_checks':'required_acceptance_checks','configured_build':'fatal_build'}
  pre=literal_assignment('max_error_cost',contract['max_expected_error_cost'])+literal_assignment('max_latency',contract['max_latency_ms'])+literal_assignment('required_acceptance_checks',['evidence','counts','denominators','identity','cost','latency','operating'])
  task='Complete acceptance_checks and configured_build using the supplied candidate settings to preserve the whole declared acceptance contract and fatal promotion dependency. Apply every declared acceptance predicate, not just cost. The adapter computes FPR, FNR and expected_error_cost from the validation counts and supplied probabilities/costs; it rejects empty denominators and incomplete evidence rather than substituting zero. result must contain cases (metrics and named checks), config, runs and protected_test_used. The inclusive boundary passes, latency-violating B and other invalid fixtures fail, and a rejected event never reaches promotion. No protected-test observations are used to fit or tune.'
 elif short=='pipeline_artifact_dependencies':
  cases=inp(f,'fixtures/dependency_cases.json');contract=inp(f,'fixtures/dependency_contract.json');adapter=DEPENDENCY;run='dependency_run';trig=trigger_all['pubsub']
  trig=copy.deepcopy(trig)
  invalid_key=next(k for k,v in cases.items() if not v['data_validation']['validation_ok'])
  invalid_event=copy.deepcopy(trig['fixtures'][0]);invalid_event[trig['bindings']['_CASE']]=invalid_key
  trig['fixtures'].insert(-1,invalid_event)
  settings={'required_edges':'contract_edges','configured_build':'fatal_build'}
  pre=literal_assignment('contract_edges',contract['required_edges'])
  task='Complete required_edges and configured_build using the supplied candidate settings to preserve the declared immutable artifact edges and fatal validation dependencies. The supplied checker compares immutable producer outputs with consumer references and retains parameters. It repairs the declared A/B mismatch by copying the producer identity, never by choosing a similar name. result must contain cases, repaired, required_edges, config and runs. Check both explicit predecessor edges and resolved event arguments; invalid data must stop training. The boundary and repaired dictionaries pass; the uncorrected mismatch fails.'
 elif short=='staged_ml_promotion':
  cases=inp(f,'fixtures/promotion_cases.json');contract=inp(f,'fixtures/promotion_contract.json');adapter=PROMOTION;run='promotion_run';trig=trigger_all['pubsub']
  settings={'required_stage_results':'contract_stage_results','configured_build':'fatal_build'}
  pre=literal_assignment('contract_stage_results',contract['required_results'])+literal_assignment('registry_records',inp(f,'fixtures/registry.json'))
  task='Complete required_stage_results and configured_build using the supplied candidate settings to preserve all declared quality/authorization gates and fatal production dependencies. Every quality and authorization result must pass for the same registry version and artifact. The supplied gate records approval, accountable identity, version, run, artifact and per-stage results. result must contain cases, config, runs and credential_value_serialized/credential_value_echoed (both false). Inspect production-only secretEnv and availableSecrets references; never provide or print a credential value. Unauthorized, wrong-artifact and failed-staging cases must not promote.'
 else:
  cases=inp(f,'fixtures/recovery_cases.json');contract=inp(f,'fixtures/recovery_contract.json');adapter=RECOVERY;run='recovery_run';trig=trigger_all['pubsub']
  settings={'recovery_outputs':'declared_outputs','configured_build':'fatal_build'}
  pre=literal_assignment('declared_outputs',list(contract['outputs']))+literal_assignment('artifact_records',inp(f,'fixtures/artifacts.json'))+literal_assignment('output_bytes',{n:f['outputs/'+n+'.txt'].encode() for n in contract['outputs']})
  task='Complete recovery_outputs and configured_build using the supplied candidate settings to reconcile every declared output and preserve explicit fatal downstream-gate dependencies. The supplied bounded storage adapter verifies existing exact-generation bytes, hashes and validation; creates only missing outputs with if_generation_match=0; and reloads/verifies after a 412 race without overwriting. result must contain cases (before/after generations, hashes, upload counts, validation count, retry/downstream status), config and runs. Verify A is unchanged, B is completed, a second call changes no generations/uploads but revalidates, unrelated failures and invalid existing outputs remain fatal, and later required gates still run or fail.'
 # Generate an explicitly bounded Python task when the glossary's descriptors do not permit a full function implementation in the syntax gate.
 # Unchanged exec scaffolding keeps adapter implementation separate from the learner's small assignment edit.
 setup='''# Fictional, bounded in-process fixture exercise; no hosted Cloud Build, subprocess or real credential.
# Only the policy assignments in the TODO section are learner work.
'''
 setup+=literal_assignment('enabled',True)+literal_assignment('disabled',False)+literal_assignment('empty_policy',[])
 setup+=literal_assignment('cases',cases)+literal_assignment('contract',contract)+literal_assignment('trigger',trig)+literal_assignment('fatal_build',required_build)+literal_assignment('unwired_build',build)+pre
 if short=='model_behavior_tests':
  bootstrap='import sys, types\n'
  for module in ['prediction_reference','prediction_package']:
   bootstrap+='module = types.ModuleType('+repr(module)+')\nsys.modules['+repr(module)+'] = module\nexec('+repr(f[module+'.py'])+', module.__dict__)\n'
  setup+=literal_assignment('package_bootstrap',bootstrap)+'exec(package_bootstrap)\n'
 adapter+='\ndef exercise_case(case_id):\n    all_evidence = '+run+'()\n    return {\"case\":all_evidence[\"cases\"].get(case_id, {\"ok\":False,\"reason\":\"missing case\"}),\"all_evidence\":all_evidence}\n'
 setup+=literal_assignment('adapter_source',COMMON+adapter)+'exec(adapter_source)\n'
 todo='\n# TODO: choose the complete contract and the explicit fatal dependency configuration.\n'
 starter=setup+todo+''.join(k+' = '+('unwired_build' if k=='configured_build' else 'disabled' if k.startswith('check_') else 'empty_policy')+'\n' for k in settings)
 solution=setup+todo+''.join(k+' = '+v+'\n' for k,v in settings.items())
 tail='\n# Supplied execution and case assertions. result is graded as a complete evidence dictionary.\nresult = '+run+'()\n'
 starter+=tail;solution+=tail
 # Expected dictionaries are obtained by executing the authored solution, never copied from an assumed verdict.
 sys.path.insert(0,str(Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
 from checkers import sandbox
 job={'packages':['numpy','pandas','pyyaml'],'scripts':[{'id':'derive','entry':'main.py','files':[{'path':'main.py','content':solution}],'mounts':[],'probes':[{'id':k,'kind':'call','function':'exercise_case','args':[k]} for k in cases]}]}
 executed=sandbox.node_run(job,runtimes['python']['runner'])['results']['derive']
 if not executed['ok']:raise RuntimeError(short+' '+executed['error'])
 expected={k:executed['probes'][k]['value'] for k in cases}
 # Normalize numpy etc by JSON serialization; all evidence is already JSON-native.
 expected=json.loads(json.dumps(expected))
 return ({'prompt':task+' The supplied exercise_case(case_id) entry point returns {case, all_evidence}; each declared valid, boundary and failure case is tested separately. This is a constrained policy-wiring exercise: the adapter and its case assertions are supplied, not learner-authored. Results are executions of a local in-process simulator, not evidence of hosted cloud runs. Do not change fixture inputs or scaffold code.',
 'runtime':{'kind':'python','version':runtimes['python']['version'],'packages':['pyyaml']+(['numpy'] if short=='model_behavior_tests' else [])},
 'workspace':{'files':[{'path':'main.py','role':'editable','language':'python','content':starter}],'entry':'main.py','asset_mounts':[]},
 'constraints':{k:copy.deepcopy(bundles[cid]['practice_anchor']['live_code'][k]) for k in ('allowed_syntax','blocked_syntax')}},
 {'solution_files':[{'path':'main.py','content':solution}],'tests':[{'test_id':'case_'+k,'kind':'function_call','visible':True,'spec':{'function':'exercise_case','args':[k],'expected':v},'message_on_fail':'Use every required predicate and the explicit fatal configuration. Inspect the recorded evidence for the first case that differs.'} for k,v in expected.items()]})

CHOICES={
 'mle.tile.073_075.s04':('After safely writing and reloading the existing dataset-gate configuration, which inspection establishes a fatal quality dependency before training?',
 ['Inspect the quality image/command, step IDs, training waitFor referencing quality, and absence of gate-failure allowances.','Check only that quality appears above training in the YAML text.','Allow quality failures so training can still produce a candidate.'],
 ['These resolved fields establish the assigned gate and fatal dependency.','Textual position alone does not establish the required explicit dependency or fatal handling.','Required quality failures must remain fatal and block training.']),
 'mle.tile.073_075.s09':('Which inspection is required after a safe write/reload of the existing behavior-test stage configuration?',
 ['Verify its image, test entry-point command, ID, dependent waitFor edges and fatal failure handling.','Verify only that safe_load returned a mapping; skip its stage fields.','Use an object-constructor YAML loader instead of safe_load for convenience.'],
 ['A round trip must retain the required execution and dependency fields.','A mapping alone does not show that tests will execute in the assigned fatal stage.','Safe loading accepts standard tags, not arbitrary Python object constructors.']),
 'mle.tile.073_075.s15':('A team has protected-test observations and wants to choose a release threshold. Which use preserves protected-test isolation?',
 ['Do not use the protected-test observations for fitting, candidate selection or threshold tuning.','Tune the threshold on the protected test because no model weights change.','Select a candidate using protected-test results but call the step validation.'],
 ['Protected-test observations must remain outside fitting and tuning or selection decisions.','Threshold tuning still uses protected observations for a tuning decision.','Renaming candidate selection does not preserve protected-test isolation.']),
 'mle.tile.073_075.s16':('After safe_dump and safe_load of the existing release configuration, what must you inspect before submitting it?',
 ['The release-gate image and command, IDs, promotion waitFor and absence of required-gate failure allowances.','Only whether the file is syntactically loadable.','Only whether promotion has a command; it need not depend on acceptance.'],
 ['Resolved fields must preserve the fatal acceptance stage and promotion dependency.','Successful parsing does not verify that required stage fields are correct.','Promotion must remain dependent on the required acceptance gate.']),
 'mle.tile.076_079.s04':('The dependency dictionary says training produces artifact A and model validation consumes A. Which run evidence verifies that declared edge?',
 ['Inspect resolved inputs and stage results to confirm model validation actually consumed the immutable training output.','Accept identical-looking model names as sufficient evidence.','Read only the dictionary; actual resolved run inputs cannot matter.'],
 ['Actual resolved inputs and results verify the configured artifact edge.','Similar names do not establish immutable producer/consumer identity.','A declaration alone does not verify the inputs used by the run.']),
 'mle.tile.076_079.s10':('An existing promotion stage receives PROMOTION_TOKEN via a secret reference. Which review preserves its scope and non-disclosure?',
 ['Check that secretEnv names it only in the authorized production step and inspect captured output for non-disclosure without displaying its value.','Put the token value in YAML to make the run reproducible.','Inject it into every stage, even those that do not need it.'],
 ['References and scoped injection preserve the authorized boundary without exposing the value.','Credential values must not be serialized or echoed.','Credential injection is scoped to the authorized promotion stage, not every stage.']),
 'mle.tile.076_079.s16':('A configured Pub/Sub event starts a recovery run. What evidence verifies that the retried stage and later required gates executed on the intended inputs?',
 ['Inspect actual triggered stage statuses and resolved event-bound inputs, including rejected-gate results.','Treat successful trigger submission as proof all later stages passed.','Treat artifact existence as proof the required validation gate passed.'],
 ['Statuses and resolved inputs establish stage execution and required-gate outcomes.','Trigger submission alone does not establish later execution or outcomes.','Artifact existence does not establish required validation success.']),
 'mle.tile.076_079.s21':('A deployment names a registry version. Which evidence traces it back to recorded training provenance?',
 ['Resolve that exact registry version to its artifact and originating run, then resolve the run’s recorded data, configuration and code links.','Use any registry version with the same model name.','Infer the training run from similar deployment and artifact names.'],
 ['The explicit version/run links trace the deployed artifact to recorded training evidence.','A shared model name does not select the deployed exact registry version.','Similar names do not prove recorded lineage links.'])
}

def classify_lineage(cid):
 f=workspace(cid);cases=inp(f,'fixtures/lineage_cases.json');artifacts=inp(f,'fixtures/artifacts.json')
 valid=cases['valid'];revision=next(iter(valid['code'].values()))['revision']
 output={k:hashlib.sha256(f['outputs/'+k+'.txt'].encode()).hexdigest() for k in artifacts}
 dataset_hash=hashlib.sha256(f['dataset.csv'].encode()).hexdigest()
 def audit(c):
  dep=c.get('deployment');reg=c.get('registry',{}).get(dep.get('registry_version')) if dep else None
  if not reg:return 'missing','deployment to exact registry version is missing'
  run=c.get('runs',{}).get(reg.get('run_id'))
  if not run:return 'missing','registry to originating run is missing'
  for table,key in [('datasets','dataset_id'),('configurations','configuration_id'),('code','code_id')]:
   if run.get(key) not in c.get(table,{}):return 'missing','run to '+table+' record is missing'
  app=c.get('approval')
  if not app:return 'missing','approval link is missing'
  art=c.get('artifacts',{}).get(reg['artifact_id'])
  if not art:return 'missing','registry to artifact is missing'
  if not (dep['artifact_id']==reg['artifact_id']==app['artifact_id']==run['artifact_id'] and app['registry_version']==dep['registry_version']):return 'mismatch','deployment, registry, approval or run artifact/version differs'
  if (reg['artifact_source'],reg['generation'],reg['sha256'])!=(art['uri'],art['generation'],art['sha256']):return 'mismatch','registry to artifact source/generation/hash differs'
  if run['artifact_sha256']!=reg['sha256'] or output.get(reg['artifact_id'])!=reg['sha256']:return 'mismatch','exact-generation downloaded content identity differs'
  if c['datasets'][run['dataset_id']]['sha256']!=dataset_hash:return 'mismatch','dataset content identity differs'
  conf=c['configurations'][run['configuration_id']]
  if hashlib.sha256(json.dumps(conf['resolved'],sort_keys=True,separators=(',',':')).encode()).hexdigest()!=conf['sha256']:return 'mismatch','resolved configuration content identity differs'
  if c['code'][run['code_id']]['revision']!=revision:return 'mismatch','recorded revision does not exist in supplied local commit fixture'
  return 'verified','all selected pairwise links, exact-generation bytes and both local Git checks agree'
 items=[];assignments={};feedback={}
 for k,c in cases.items():
  bucket,why=audit(c)
  dep=c['deployment'];reg=c.get('registry',{}).get(dep['registry_version']);run=c.get('runs',{}).get(reg.get('run_id')) if reg else None
  excerpt='SIMULATED audit excerpt; supplied case '+k+'\n'+json.dumps(c,sort_keys=True,indent=2)
  if reg:
   excerpt+='\nversion-qualified download request: '+json.dumps({'uri':reg['artifact_source'],'generation':reg['generation']})
   available=artifacts.get(reg['artifact_id'])
   downloaded=bool(available and available['uri']==reg['artifact_source'] and available['generation']==reg['generation'])
   excerpt+='\nDownload status: '+('OK; downloaded content sha256: '+str(output.get(reg['artifact_id'])) if downloaded else 'exact requested source/generation not present in supplied fixture storage; recorded artifact metadata differs')
  if run and run.get('code_id') in c.get('code',{}):
   rev=c['code'][run['code_id']]['revision'];ok=rev==revision
   excerpt+='\n'+json.dumps({'git rev-parse --verify':{'revision':rev,'returncode':0 if ok else 128,'stdout':rev if ok else ''},'git show':{'revision':rev,'returncode':0 if ok else 128,'commit':rev if ok else None}})
  excerpt+='\nDataset file content sha256: '+dataset_hash
  excerpt+='\nLocal case-assertion harness: assert actual_case_outcome == expected_case_outcome; PASSED. This does not disclose whether the expected outcome was verification or rejection; inspect the chain evidence.'
  items.append({'item_id':k,'text':excerpt});assignments[k]=bucket;feedback[k]={'message':why+'. A case assertion passing does not by itself make the lineage verified.'}
 items.append({'item_id':'false_predicate','text':'SIMULATED ordinary, non-optimized Python run:\nassert False\nTraceback (most recent call last):\nAssertionError\nClassify the assertion outcome, not any lineage chain.'})
 assignments['false_predicate']='assertion_failure';feedback['false_predicate']={'message':'A deliberately false predicate raises AssertionError in ordinary non-optimized execution.'}
 return {'prompt':'Inspect every independent audit excerpt. Classify the chain as verified only when selected pairwise identities, exact-generation downloaded content and both local Git inspections agree. Otherwise choose missing link or identity/content/commit mismatch. A passing case assertion for a rejection is not a verified chain. Use assertion failure only for the explicit deliberately false assertion excerpt. All command/download results shown are authored local simulations, not hosted execution claims.','buckets':[{'bucket_id':k,'label':v} for k,v in [('verified','Verified chain'),('missing','Missing lineage link'),('mismatch','Identity, content or commit mismatch'),('assertion_failure','Deliberately false predicate raises AssertionError')]],'items':items}, {'assignments':assignments,'item_feedback':feedback}

out={k:plan[k] for k in ['schema_version','path_id','batch_id']};out['kind']='interactions_part';out['tiles']=[]
for tile in plan['tiles']:
 t={'tile_id':tile['tile_id'],'interactions':[]};out['tiles'].append(t)
 sc=next(x for x in screens['tiles'] if x['tile_id']==tile['tile_id']);seen=set()
 planned=[s for s in tile['steps'] if s['type'] in ['check','hands_on']]
 for index,s in enumerate(planned):
  cid=s['concept_ids'][0];bundle=bundles[cid]
  ix={'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'],'difficulty':'intro' if index==0 else 'stretch' if index>=len(planned)-2 else 'core','grading_mode':'client','standalone':s['type']=='check','measures':[],'anchors':copy.deepcopy(s['anchors'])}
  for a in s['anchors']:
   if '#assessment:' in a:
    capability=a.split('#assessment:')[1];anchor=next(x for x in bundle['assessment_anchors'] if x['capability']==capability)
    ix['measures'].append({'concept_id':cid,'capability':capability,'fact_ids':copy.deepcopy(anchor['fact_ids'])})
  ix['feedback']={'correct':'The required predicates and evidence agree with the declared contract.','incorrect':'Recheck the failed predicate or dependency against the declared contract; success must not be inferred from a name or submission alone.','hints':['Separate declared configuration from the inputs and results actually recorded.','Check each required predicate before accepting the overall result.']}
  for field in ['correct','incorrect']:
   ix['feedback'][field]={'message':ix['feedback'][field]}
  if cid not in seen:
   rem=next((r for r in sc['remediation_steps'] if cid in r['concept_ids']),None)
   if rem:ix['feedback']['remediation_step_id']=rem['step_id']
   seen.add(cid)
  if ix['type']=='choice':
   prompt,opts,msgs=CHOICES[s['step_id']]
   ix['public']={'prompt':prompt,'selection':'single','shuffle':True,'options':[{'option_id':'o'+str(i+1),'text':o} for i,o in enumerate(opts)]}
   ix['grading']={'correct_option_ids':['o1'],'option_feedback':{'o'+str(i+1):{'message':m} for i,m in enumerate(msgs)}}
  elif ix['type']=='code_exercise':ix['public'],ix['grading']=make_code(cid)
  else:ix['public'],ix['grading']=classify_lineage(cid)
  t['interactions'].append({'step_id':s['step_id'],'interaction':ix})
(B/'interactions.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('Written',sum(len(t['interactions']) for t in out['tiles']),'interactions')
