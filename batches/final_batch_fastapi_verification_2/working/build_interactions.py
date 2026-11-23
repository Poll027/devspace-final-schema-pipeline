import json, sys, copy
from pathlib import Path
sys.path.insert(0,str(Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
from checkers import sandbox
B=Path('batches/final_batch_verification_2')
load=lambda f:json.loads((B/f).read_text())
plan=load('tile_plans.json'); screens=load('screens.json'); reg=load('scenario_asset_registry.json')
bundles={b['context']['concept_id']:b for b in load('inputs/path_glossary_bundle.json')['bundles']}
assets={a['asset_id']:a for a in reg['assets']}
pin=json.load(open('00_FINAL_PIPELINE_CORE/registry/runtimes.json'))['runtimes']['python_asgi']
main=lambda c:next(f['content'] for f in assets['cw.'+c]['files'] if f['path']=='main.py')
file=lambda c,p:next(f['content'] for f in assets['cw.'+c]['files'] if f['path']==p)
# Questions only reference the precise cases and rules explicitly taught in the text.
choices={
 'tile_054.s04':('POST /orders validates a positive quantity and returns that input without persistence. Which decorator metadata describes this existing behavior?',[
 ('orders tag; summary: Validate an order input; description: Return the validated quantity without storing it.','These labels describe and group the existing operation without changing it.'),
 ('orders tag; summary: Store an order; description: Persist the quantity.','The supplied handler does not store anything; descriptive metadata must agree with its behavior.'),
 ('orders tag; summary: Accept any quantity; description: Disable the positive quantity bound.','Metadata does not change runtime validation; the positive quantity constraint remains in force.')]),
 'tile_055.s03':('An endpoint uses Depends(original). While app.dependency_overrides[original] = replacement is active, which provider resolves this dependency?',[
 ('replacement','The original callable maps to the replacement callable during dependency resolution.'),('original','The active override substitutes the replacement for this original callable.'),('Both providers in sequence','The mapping selects a replacement; it does not define a sequence of both providers.')]),
 'tile_055.s04':('The override dictionary was initially empty. After a test, finally resets app.dependency_overrides = {}. Which provider resolves the next request using Depends(original)?',[
 ('original','Restoring the empty mapping removes the substitution.'),('replacement','The replacement no longer has an active mapping after cleanup.'),('No provider; the dependency is removed','Resetting overrides removes substitutions, not the endpoint dependency.')]),
 'tile_056.s02':('An endpoint declares user_agent: Annotated[str, Header()] with no alias or conversion override. Which incoming header name matches?',[
 ('user-agent, regardless of header-name case','Default underscore conversion produces a hyphen, and header names are case-insensitive.'),('Only user_agent with an underscore','The default mapping converts underscores to hyphens.'),('Only exactly lowercase user-agent','Header-name case does not affect this binding.')]),
 'tile_056.s05':('A response-model validation failure occurs in server application code, not in incoming request data. Which interpretation follows the taught distinction?',[
 ('A server-side bug, not a client invalid-input error','Response or application model-validation failures differ from invalid request data.'),('A client request-validation failure merely because validation failed','The location of the failure matters; server-side validation is not invalid client input.'),('The default 422 invalid-request response necessarily applies','The default invalid-input outcome applies to rejected request data, not this server-side failure.')]),
 'tile_058.s03':('For the selected PrometheusMiddleware, an exception escapes the inner application rather than returning a response. Which boundary interpretation is correct?',[
 ('The response counter updates, but no normal processing-time histogram observation is added.','The counter and histogram have different boundaries for an escaping exception.'),('Neither response counting nor duration observation occurs.','The response counter is updated even for a raised exception.'),('Both update as for a normally returned response.','The histogram is observed only when the inner application returns a response.')]),
 'tile_059.s04':('OrderUpdate gives note and quantity defaults of None. For OrderUpdate(quantity=2), which supplied-field extraction rule applies?',[
 ('exclude_unset=True retains the supplied quantity and omits the unsupplied note.','Supplied-field extraction preserves explicitly provided fields rather than all defaults.'),('exclude_unset=True adds note=None because it has a default.','The unsupplied default note is excluded by exclude_unset.'),('exclude_unset=True removes quantity because note was omitted.','Omitting one field does not remove a different explicitly supplied field.')]),
 'tile_059.s07':('The previous quantity constraint is gt=0; a revision tightens it to gt=2. What should the compatibility review verify?',[
 ('Test representative previously valid inputs against the revision; tightened constraints can reject them.','A tighter bound can invalidate previously accepted inputs.'),('Matching the int type alone proves compatibility.','The constraint also controls acceptance, so a matching type is insufficient.'),('Only compare names; constraint changes cannot affect clients.','Tightening constraints can change which client inputs validate.')]),
 'tile_059.s08':('A proposed revision removes a public response field or an operation. Which review checks the documented client expectations?',[
 ('Compare generated paths and response schemas with the previous contract.','These comparisons expose removed or changed public fields and operations.'),('Compare request type names only.','Request type names do not check public response fields or operation paths.'),('Approve because request requiredness is unchanged.','Unchanged request requiredness does not preserve changed public response or operation expectations.')])}
ex={}
def call_tests(name,args):return [{'test_id':f't{i+1}','kind':'function_call','spec':{'function':name,'args':[a]}} for i,a in enumerate(args)]
def value_tests(exprs):return [{'test_id':f't{i+1}','kind':'value_equals','spec':{'expr':x}} for i,x in enumerate(exprs)]
c='fastapi.contract_examples_metadata'
start=main(c)
helper='''
# Read-only verification scaffold: no learner edits below this line.
def contract_probe(payload):
    from fastapi.testclient import TestClient
    assert OrderInput.model_validate(example).quantity == example["quantity"]
    schema = OrderInput.model_json_schema()
    assert schema["examples"] == [example]
    assert schema["properties"]["quantity"]["exclusiveMinimum"] == 0
    operation = app.openapi()["paths"]["/orders"]["post"]
    assert operation["tags"] == ["orders"]
    assert operation["summary"] == "Validate an order input"
    assert operation["description"] == "Return the validated quantity without storing it."
    named = operation["requestBody"]["content"]["application/json"]["examples"]["quantity_two"]
    assert named["value"] == example
    assert named["summary"] == "Positive quantity"
    assert named["description"] == "Synthetic order input with a positive quantity."
    validated = OrderInput.model_validate(payload)
    return {"body": create_order(validated).model_dump(), "metadata_checked": True}
'''
sol=start.replace('# TODO: add schema example metadata without changing the quantity bound.','model_config = ConfigDict(json_schema_extra={"examples": [example]})').replace('@app.post("/orders")','@app.post("/orders", tags=["orders"], summary="Validate an order input", description="Return the validated quantity without storing it.")').replace('order: OrderInput','order: Annotated[OrderInput, Body(openapi_examples={"quantity_two": {"summary": "Positive quantity", "description": "Synthetic order input with a positive quantity.", "value": example}})]')+'\nOrderInput.model_validate(example)\n'
ex[c]=(start+helper,sol+helper,call_tests('contract_probe',[{'quantity':2},{'quantity':3}]),'Validate example with OrderInput.model_validate. Add model-level schema examples using that sample and a named Body example quantity_two with summary "Positive quantity", description "Synthetic order input with a positive quantity.", and value example. Set tags to ["orders"], summary to "Validate an order input", and description to "Return the validated quantity without storing it." Preserve the handler body and gt=0 constraint. Run the supplied contract_probe checks.')
c='fastapi.dependency_overrides';start=main(c)
helper='''
# Read-only verification scaffold.
def override_probe(value):
    global replacement
    def replacement():
        return value
    test_override()
    assert app.dependency_overrides == {}
    # Force the response assertion to fail and verify cleanup in that path too.
    from unittest.mock import patch
    try:
        with patch.object(TestClient, "get", side_effect=AssertionError("controlled failure")):
            test_override()
    except AssertionError:
        assert app.dependency_overrides == {}
    with TestClient(app) as client:
        restored = client.get("/").json()
    return {"substitution": value, "restored": restored, "overrides": app.dependency_overrides}
'''
# The asserted value is supplied by immutable scaffolding so verification can vary it.
start='expected_user = "mock user"\n'+start
helper=helper.replace('global replacement','global replacement, expected_user\n    expected_user = value')
sol=start.replace('# TODO: register the replacement using the original callable as the key.','app.dependency_overrides[original] = replacement').replace('# TODO: assert the synthetic value under user.','assert response.json()["user"] == expected_user').replace('# TODO: restore the initially empty override dictionary.\n        pass','app.dependency_overrides = {}')
ex[c]=(start+helper,sol+helper,call_tests('override_probe',['mock user','alternate synthetic user']),'Complete test_override: map the original callable to replacement, assert response.json()["user"] equals the supplied expected_user, and restore the initially empty overrides in finally. Keep endpoint and providers unchanged. The verification scaffold runs the test normally and on a controlled assertion-failure path, then checks that the original provider is restored.')
c='fastapi.header_cookie_binding';start=main(c);sol=start.replace('user_agent: str, cookie: str | None = None','user_agent: Annotated[str, Header()], cookie: Annotated[str | None, Cookie()] = None')
tests=[]
for i,r in enumerate([{'method':'GET','path':'/metadata','headers':{'user-agent':'synthetic-agent'}},{'method':'GET','path':'/metadata','headers':{'USER-AGENT':'another-agent','cookie':'cookie=synthetic-cookie'}},{'method':'GET','path':'/metadata','headers':{'user-agent':'third-agent','cookie':'cookie=another-cookie'}}]):tests.append({'test_id':f't{i+1}','kind':'http_equals','spec':{'requests':[r]}})
ex[c]=(start,sol,tests,'Change only the /metadata parameter annotations: use Annotated[str, Header()] for user_agent and Annotated[str | None, Cookie()] = None for cookie. Preserve the handler. Verify user-agent header case-insensitivity, cookie-by-name binding and accepted cookie omission; return the existing user_agent and cookie keys.')
c='fastapi.request_validation_errors'
fixture=file(c,'fixture.py').replace('client = TestClient(app)','')
start=fixture+'''
# Read-only test scaffold; submit the supplied input in the body below.
def invalid_probe(payload):
    global client, invalid_order
    client = TestClient(app)
    invalid_order = payload
    expected_location, expected_type = validation_expectations()
    # TODO: send invalid_order and assert status, detail loc and type.
    return {"status": response.status_code, "location": entry["loc"], "type": entry["type"]}
'''
sol=start.replace('# TODO: send invalid_order and assert status, detail loc and type.','response = client.post("/orders", json=invalid_order)\n    assert response.status_code == 422\n    entry = response.json()["detail"][0]\n    assert entry["loc"] == expected_location\n    assert entry["type"] == expected_type')
ex[c]=(start,sol,call_tests('invalid_probe',[{'quantity':'not an integer'},{'quantity':0}]),'Complete invalid_probe with a POST to /orders using invalid_order. Assert status 422, then assert the first JSON detail entry loc and type equal the supplied expected_location and expected_type. Do not change the endpoint or default error handling. Return the scaffold diagnostic keys status, location and type. Tests supply the original invalid string and a quantity-bound violation.')
c='pydantic.partial_update_contracts';start=main(c)
# Scaffold uses a mutable starter input; extraction must track its value.
start=start.replace("concrete_note = OrderUpdate(note='Leave at reception')","note_text = 'Leave at reception'\nconcrete_note = OrderUpdate(note=note_text)")
helper='''
# Read-only verification scaffold: include input value so mutations check extraction.
def update_probe(value):
    global note_text, concrete_note
    concrete_note = OrderUpdate(note=value)
    concrete_update = concrete_note.model_dump(exclude_unset=True)
    assert quantity_update == quantity_only.model_dump(exclude_unset=True)
    assert null_update == explicit_null.model_dump(exclude_unset=True)
    assert null_without_none == explicit_null.model_dump(exclude_unset=True, exclude_none=True)
    assert quantity_fields == quantity_only.model_fields_set
    assert null_fields == explicit_null.model_fields_set
    assert note_fields == concrete_note.model_fields_set
    return {"quantity": quantity_update, "null": null_update, "note": note_update, "null_without_none": null_without_none, "input": value}
'''
# Use a scaffold function for varying all three inputs and grade learner extraction directly.
start=main(c).split('quantity_only =')[0]+'''
def update_probe(value):
    # Scaffold inputs; edit only the TODO extraction assignments.
    quantity_only = OrderUpdate(quantity=2)
    explicit_null = OrderUpdate(note=None)
    concrete_note = OrderUpdate(note=value)
    # TODO: extract three updates, three field sets and the null-with-exclude_none contrast.
    return {"quantity": quantity_update, "null": null_update, "note": note_update, "fields": [quantity_fields, null_fields, note_fields], "null_without_none": null_without_none}
'''
sol=start.replace('# TODO: extract three updates, three field sets and the null-with-exclude_none contrast.','quantity_update = quantity_only.model_dump(exclude_unset=True)\n    null_update = explicit_null.model_dump(exclude_unset=True)\n    note_update = concrete_note.model_dump(exclude_unset=True)\n    quantity_fields = quantity_only.model_fields_set\n    null_fields = explicit_null.model_fields_set\n    note_fields = concrete_note.model_fields_set\n    null_without_none = explicit_null.model_dump(exclude_unset=True, exclude_none=True)')
ex[c]=(start,sol,call_tests('update_probe',['Leave at reception','Synthetic alternate note']),'Inside the scaffold update_probe, assign quantity_update, null_update and note_update using model_dump(exclude_unset=True) on the corresponding supplied models. Assign quantity_fields, null_fields and note_fields from model_fields_set. Assign null_without_none by additionally using exclude_none=True on explicit_null. Preserve the returned diagnostic structure. This must distinguish omission, explicit null and a supplied string without storage operations.')
c='rest.compatible_contract_changes'
start=main(c).split('omitted_note =')[0]+'''
# Previous/revised models above stay unchanged for the comparison.
class CompatibleOrderInput(BaseModel):
    note: str | None

# Scaffold input and return shape; fill only the TODO validation block/default.
def compatibility_probe(payload):
    # TODO: establish previous/revised acceptance and validate the repaired model.
    return {"previous_accepts": previous_accepts, "revised_accepts": revised_accepts, "client_breaking": client_breaking, "repaired_note": repaired.note}
'''
sol=start.replace('class CompatibleOrderInput(BaseModel):\n    note: str | None','class CompatibleOrderInput(BaseModel):\n    note: str | None = None').replace('# TODO: establish previous/revised acceptance and validate the repaired model.','PreviousOrderInput.model_validate(payload)\n    previous_accepts = True\n    try:\n        RevisedOrderInput.model_validate(payload)\n        revised_accepts = True\n    except ValidationError:\n        revised_accepts = False\n    client_breaking = True\n    repaired = CompatibleOrderInput.model_validate(payload)')
ex[c]=(start,sol,call_tests('compatibility_probe',[{}, {'note':'Leave at reception'}]),'Compare the unchanged PreviousOrderInput and RevisedOrderInput with the supplied payload: assign previous_accepts and revised_accepts according to model_validate (catch ValidationError for the revision). Assign client_breaking=True to identify the loss of omission support. Restore = None in CompatibleOrderInput without changing its type, and assign repaired by validating payload with it. The tests use both an omitted note and a string note; preserve the scaffold diagnostic return structure.')
# Genuine maintained instrumentation; do not replace the unavailable library with a mock.
c='observability.verified_request_metrics'
start=file(c,'fixture.py')+'\n'+file(c,'harness.py').replace('from fixture import CASES\n','')+'\n'+main(c).replace('from fixture import app\n','').replace('from harness import observe\n','')
sol=start.replace('# TODO: register the middleware with filter_unhandled_paths=True.','app.add_middleware(PrometheusMiddleware, filter_unhandled_paths=True)').replace('# TODO: expose the /metrics/ view using app.add_route.','app.add_route("/metrics/", metrics)')
helper='''
# Read-only verification scaffold.
def metrics_probe(route):
    with TestClient(app, raise_server_exceptions=False) as client:
        before = snapshot(client, route)
        response = client.get(route)
        after = snapshot(client, route)
        assert response.status_code in (200, 400)
        def delta(name):
            return sum(v - before.get(k, 0) for k, v in after.items() if k[0] == name)
        # Discover names from actual exposition, never guess library metric names.
        families = list(text_string_to_metric_families(client.get("/metrics/").text))
        counter_samples = [sample for family in families if family.type == "counter" for sample in family.samples if sample.labels.get("path") == route and sample.name.endswith("_total")]
        request_names = {sample.name for sample in counter_samples if "status_code" not in sample.labels}
        response_names = {sample.name for sample in counter_samples if "status_code" in sample.labels}
        histogram_samples = [sample for family in families if family.type == "histogram" for sample in family.samples if sample.labels.get("path") == route]
        count_names = {sample.name for sample in histogram_samples if sample.name.endswith("_count")}
        sum_names = {sample.name for sample in histogram_samples if sample.name.endswith("_sum")}
        assert len(request_names) == len(response_names) == len(count_names) == len(sum_names) == 1
        request_delta = delta(next(iter(request_names)))
        response_delta = delta(next(iter(response_names)))
        duration_count = delta(next(iter(count_names)))
        duration_sum = delta(next(iter(sum_names)))
        assert request_delta == 1
        assert response_delta == 1
        assert duration_count == 1
        if route == "/delayed":
            assert duration_sum >= CASES[2]["configured_delay_seconds"]
        for key in after:
            assert set(dict(key[1])) <= {"method", "path", "status_code"}
        return {"route": route, "status": response.status_code, "request_delta": request_delta, "response_delta": response_delta, "duration_count": duration_count}
'''
ex[c]=(start+helper,sol+helper,call_tests('metrics_probe',['/success','/expected-error','/delayed']),'Register the documented PrometheusMiddleware with filter_unhandled_paths=True and expose /metrics/ with metrics. Keep fixture handlers and verification scaffold unchanged. Run metrics_probe for /success, /expected-error and /delayed. Compare per-route request/response counter deltas and completed-response histogram count deltas, each once; verify the delayed duration reflects the controlled sleep and labels are bounded nonsensitive method, path and status_code. Snapshots isolate the exercised route from metrics-view traffic.')
output={k:plan[k] for k in ['schema_version','path_id','batch_id']};output['kind']='interactions_part';output['tiles']=[]
blocked=[]
for tile in plan['tiles']:
 items=[]; first=set(); relevant=[s for s in tile['steps'] if s['type'] in ['check','hands_on']]
 for index,s in enumerate(relevant):
  cid=s['concept_ids'][0]; b=bundles[cid]
  measures=[copy.deepcopy({'concept_id':cid,**a}) for a in b['assessment_anchors'] if cid+'#assessment:'+a['capability'] in s['anchors']]
  if not measures and s['type']=='hands_on':
   measures=[{'concept_id':cid,**copy.deepcopy(a)} for a in b['assessment_anchors']]
  fb={'correct':{'message':'Your answer agrees with the taught contract and its verification boundary.'},'incorrect':{'message':'Revisit the stated boundary and compare it with the supplied case.'},'hints':['Separate the declared contract from assumptions about names or behavior.']}
  if cid not in first:
   rem=next((r['step_id'] for t in screens['tiles'] if t['tile_id']==tile['tile_id'] for r in t.get('remediation_steps',[]) if cid in r['concept_ids']),None)
   if rem:fb['remediation_step_id']=rem
   first.add(cid)
  ix={'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'],'difficulty':('intro' if index==0 else 'stretch' if index==len(relevant)-1 else 'core'),'grading_mode':'client','standalone':True,'measures':measures,'anchors':s['anchors'],'feedback':fb}
  if ix['type']=='choice':
   prompt,opts=choices[s['step_id']]
   ix['public']={'prompt':prompt,'options':[{'option_id':f'o{i+1}','text':o[0]} for i,o in enumerate(opts)],'selection':'single','shuffle':True}
   # Key follows the option marked by the authored fact-grounded rationale, not an external data value.
   ix['grading']={'correct_option_ids':[ix['public']['options'][0]['option_id']],'option_feedback':{f'o{i+1}':{'message':o[1]} for i,o in enumerate(opts)}}
   fb['correct']['message']=opts[0][1];fb['hints']=['Identify which boundary or declared source the question specifies.']
  else:
   starter,solution,tests,prompt=ex[cid]
   ix['public']={'prompt':prompt,'runtime':{'kind':'python_asgi','version':pin['version'],'packages':[]},'workspace':{'entry':'main.py','files':[{'path':'main.py','role':'editable','language':'python','content':starter}],'asset_mounts':[]},'constraints':{k:b['practice_anchor']['live_code'][k] for k in ['allowed_syntax','blocked_syntax']}}
   ix['grading']={'solution_files':[{'path':'main.py','content':solution}],'tests':tests}
   for t in tests:t['message_on_fail']='Compare this case with the supplied contract and complete the verification without changing fixture behavior.'
   probes=[sandbox._py_probe(t) for t in tests]
   result=sandbox.node_run(sandbox._py_job('python_asgi',[],[sandbox._py_script(cid,'main.py',solution,[],probes)]),pin['runner'])['results'][cid]
   if result.get('ok'):
    for t in tests:
     p=result['probes'][t['test_id']]
     if not p['ok']:
      blocked.append({'concept':cid,'test':t['test_id'],'error':p['error']});t['spec']['expected']=None;continue
     v=p['value'];t['spec']['expected']=({k:v[k] for k in ['status','json']} if t['kind']=='http_equals' else v)
   else:
    blocked.append({'concept':cid,'error':result.get('error')})
    # Unavailable runtime dependency: keep explicit null, never invent executed output.
    for t in tests:t['spec']['expected']=None
   fb['hints']=['Use the explicit glossary API shown in the starter comments.','Keep fixture behavior unchanged while completing the declared task.']
   fb['correct']['message']='The completed verification matches the supplied cases and preserves the contract.'
  items.append({'step_id':s['step_id'],'interaction':ix})
 output['tiles'].append({'tile_id':tile['tile_id'],'interactions':items})
(B/'interactions.json').write_text(json.dumps(output,indent=2)+'\n')
(B/'working/interaction_build_report.json').write_text(json.dumps({'blocked':blocked,'counts':{t['tile_id']:len(t['interactions']) for t in output['tiles']}},indent=2)+'\n')
print(json.dumps({'blocked':blocked,'counts':{t['tile_id']:len(t['interactions']) for t in output['tiles']}},indent=2))
