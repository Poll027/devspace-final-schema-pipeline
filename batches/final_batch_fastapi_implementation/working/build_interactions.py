import json,sys,ast,copy,subprocess
from pathlib import Path
B=Path('batches/final_batch_implementation'); CORE=Path('00_FINAL_PIPELINE_CORE')
sys.path.insert(0,str(CORE/'scripts'))
from checkers import sandbox
plans=json.loads((B/'tile_plans.json').read_text()); screens=json.loads((B/'screens.json').read_text()); reg=json.loads((B/'scenario_asset_registry.json').read_text()); bundles={x['context']['concept_id']:x for x in json.loads((B/'inputs/path_glossary_bundle.json').read_text())['bundles']}; assets={x['asset_id']:x for x in reg['assets']}; pins=json.loads((CORE/'registry/runtimes.json').read_text())['runtimes']
def file(c,p='main.py'): return next(x['content'] for x in assets['ws.'+c]['files'] if x['path']==p)
# Each tuple: prompt, correct option, two misconception-based distractors, explanations, hint.
Q={
'specify_created_resource_and_absent_item_responses':('For an orders contract using the taught creation and absence responses, which pair is appropriate?','Creation: 201 with Location identifying the created item; absent item: 404.','Creation: 404; absent item: 201 with Location.','Creation: 201 with no created-resource identification; absent item: 201.','201 describes creation; 404 describes an absent item, not the reverse.','The taught creation contract identifies the created resource with Location; 201 is not the absent-item response.','Separate the newly created resource from an item that does not exist.'),
'distinguish_operations_sharing_a_path':('GET and PUT are registered on /orders/{order_id}. How many distinct path operations do these declarations represent?','Two: each method-and-path pair is a distinct operation.','One: sharing the path makes the handlers the same operation.','Two, but only the first method declared can serve that path.','An operation combines a method and path; sharing a path does not merge methods.','Different HTTP methods on the same path serve different operations; declaration order does not erase the other method.','Identify both parts of a path operation.'),
'determine_handler_from_conflicting_route_order':('A GET /orders/{order_id} route is declared before GET /orders/current, with no input conversion restrictions. Which route first captures GET /orders/current?','The parameterized GET route, because it is evaluated first and matches current.','The fixed GET route, regardless of declaration order.','Neither route: fixed and parameterized routes cannot share a prefix.','Routes are evaluated in order; specificity does not override the earlier conflicting match.','A fixed route can coexist with a parameterized one; declare the fixed route first to prevent capture.','Trace the declarations from first to last.'),
'determine_effective_settings_source_and_validation_outcome':('Settings declares required app_name: str and env_file=".env", with no constructor override. APP_NAME is set to "environment-orders" in the environment and "dotenv-orders" in .env. Which value is effective?','environment-orders','dotenv-orders','Construction fails solely because both sources supply a value.','An environment variable takes priority over the dotenv value.','Conflicting sources are resolved by precedence; that conflict alone is not a missing required setting.','Distinguish source precedence from validation.'),
'identify_async_client_lifetime_mistakes':('Two outbound calls belong to one owning async scope. Which client-lifetime plan matches the taught approach?','Reuse one scoped AsyncClient, await both calls, and close it when its scope ends.','Construct a new AsyncClient for each call and leave both open.','Reuse one AsyncClient but call get without awaiting and never close it.','Per-call client creation loses the taught reuse pattern; leaving clients open omits required cleanup.','Async requests must be awaited and the owning scope must close the client.','Check reuse, awaiting and ownership separately.'),
'distinguish_cross_field_invariants_from_single_field_checks':('Booking requires end > start after both integer fields have validated. Where should this relationship be checked?','An after-model instance validator comparing self.end and self.start.','A field validator that checks only whether end is an integer.','No custom check: successful integer conversion proves end > start.','A single-field type check does not establish the relationship between the two validated fields.','Both fields can be valid integers while their relationship violates the invariant.','Ask whether the rule depends on one field or the pair.'),
'identify_inputs_that_isolate_cross_field_validity':('Booking has integer start and end and requires end > start. Which invalid case isolates the cross-field rule, paired with a consistent case?','Invalid: start=5, end=3; consistent: start=3, end=5.','Invalid: start="not-an-integer", end=3; consistent: start=3, end=5.','Invalid: start=3, end=5; consistent: start=5, end=3.','A non-integer start fails field validation, so it does not isolate a rule on already-validated fields.','The proposed invalid pair satisfies end > start; the proposed consistent pair violates it.','Keep both individual fields valid before examining their relationship.'),
'determine_deliberate_rejection_control_flow':('An absent order requires a deliberate HTTP rejection. Which action stops the operation with that rejection?','Raise HTTPException with the intended status_code and detail.','Return the HTTPException object as a normal result.','Create an HTTPException object but continue returning the normal result.','Returning the exception object is not the taught rejection control flow: raise it.','Merely constructing an exception does not stop the operation; raising does.','Distinguish constructing, returning and raising an exception.'),
'identify_required_rejection_headers':('A deliberate rejection contract requires response metadata in a header. How should HTTPException carry that metadata?','Use its headers keyword with the required header name and value.','Put the header name only in the detail message.','Return an HTTPException instead of raising it to turn detail into headers.','detail is response detail, not the headers argument for required metadata.','The exception must be raised, and headers must be supplied explicitly rather than inferred from detail.','Separate body detail from response metadata.'),
'identify_blocking_io_inside_async_execution':('An async def handler directly calls a normal utility that performs blocking I/O. What does FastAPI do with this direct utility call?','It is not automatically offloaded; the blocking call can block the event loop.','It automatically offloads every normal utility called by async def.','The utility becomes awaitable solely because its caller is async def.','Automatic thread-pool execution for normal path operations does not apply to arbitrary direct utility calls.','A normal utility is not made awaitable by an async caller; its blocking I/O remains blocking.','Separate path-operation execution from ordinary direct calls.'),
'distinguish_feature_registration_from_application_inclusion':('orders.py registers GET /orders on an APIRouter. What connects that router to the served FastAPI application?','Import its router in the application module and call app.include_router(router).','Import the feature module but never include its router.','Register with @router.get and assume that every FastAPI app discovers it.','An import alone does not perform the required application inclusion.','Feature registration belongs to the router; the application must explicitly include it.','Distinguish registration on a router from application inclusion.'),
'determine_query_requiredness_and_conversion':('A handler has limit: int = 10, and limit is not in its route path. What happens when limit is omitted or supplied as "3"?','Omission uses 10; supplying "3" converts the query value to integer 3.','Omission is rejected because every int parameter is required.','Supplying "3" remains a string because query values are never converted.','A default permits omission; the type annotation does not cancel the default.','The declared type controls conversion of a supplied query string.','Inspect both the default and the declared type.'),
'determine_path_conversion_and_rejection':('GET /orders/{order_id} declares order_id: int. What happens to GET /orders/not-an-integer?','Validation rejects the path value instead of invoking the handler with that unconverted value.','The handler receives the original string despite its integer annotation.','The value becomes a query parameter because conversion failed.','An unconvertible typed path value produces validation error rather than being passed through unchanged.','Binding comes from the route placeholder; conversion failure does not move the value to the query.','Determine binding first, then conversion.'),
'determine_publicly_projected_fields':('An internal order has order_id, status and private_processing_note. PublicOrder defines only order_id and status, and response_model=PublicOrder is set. Which fields are returned from a valid internal value?','order_id and status only.','All three fields because they are present internally.','Only private_processing_note because excluded fields override the model.','The public model filters the returned value; internal presence alone does not expose the private field.','The output model includes its declared public fields, not the omitted private field.','Compare the internal value with the public model fields.'),
'recognize_direct_response_filtering_bypass':('An operation declares response_model=PublicOrder but returns a Response object directly. Who is responsible for that direct response content?','The application: direct Response return bypasses automatic response-model conversion and filtering.','FastAPI always projects every direct Response through PublicOrder.','The return annotation restores automatic filtering of the direct Response.','Direct Response return bypasses the automatic model-processing path.','A return annotation does not restore model conversion for a directly returned Response.','Distinguish ordinary returned values from direct Response objects.'),
'identify_explicit_shared_input_provision_logic':('Several handlers need the same reusable input-provision logic. Which structure makes that need explicit?','A provider declared as a handler dependency.','Copy the provision logic into each handler with no dependency declaration.','Hide a direct provider call inside each handler and omit the needed input from its parameters.','Copying logic does not extract the reusable input provision into an explicit dependency.','A hidden direct call does not declare the supplied input as a handler dependency.','Look for a reusable provider and an explicit consuming parameter.'),
'distinguish_finite_io_limits_from_total_elapsed_budget':('Does httpx.AsyncClient(timeout=5) by itself establish a five-second total elapsed budget across all asynchronous work?','No: HTTPX wait limits are distinct from a total elapsed-time budget.','Yes: read timeout measures the entire operation from beginning to end.','No, because timeout=5 disables all HTTPX timeouts.','Read and write limits bound waits for individual chunks, not the whole elapsed operation.','A finite timeout enables wait limits; timeout=None disables enforcement.','Separate chunk waits from total elapsed work.'),
'identify_total_budget_timeout_outside_async_context':('Work is wrapped in async with asyncio.timeout(seconds) for a total elapsed budget. Where is its cancellation converted to TimeoutError for handling?','Outside the timeout context.','Only inside the timeout context before it exits.','It becomes an HTTPX PoolTimeout regardless of which work was running.','The context converts cancellation to TimeoutError on exit, so handle it outside.','An asyncio total-budget timeout is not automatically an HTTPX pool-wait exception.','Follow the context exit before selecting the exception handler.'),
'identify_reusable_input_provisioning':('A quantity-input provider is needed by several order handlers. How can the handlers receive the reusable provision result explicitly?','Declare a handler parameter with Depends(provider).','Copy input-provision code into every handler.','Move copied handlers into separate files but keep all input-provision code duplicated.','A declared dependency extracts provision logic instead of duplicating it.','File placement alone does not extract reusable input-provision responsibility.','Look for the declared input boundary, not just file placement.'),
'identify_misplaced_transport_business_and_persistence_logic':('Which placement respects the taught responsibility boundaries for an order decision?','Handler: HTTP adaptation; plain callable: business decision; adapter: stored-state access.','Handler: stored-state access and business decision; adapter: HTTP response adaptation.','Separate files, but every function still reads HTTP objects and stored-state fixtures directly.','The business rule and stored-state access have their own responsibilities, distinct from HTTP adaptation.','Separate files alone do not establish boundaries when protocol and persistence access remain mixed.','Assign each responsibility by what it does, not where its file lives.'),
'distinguish_bounded_in_process_work_from_durable_execution_needs':('An order follow-up must be guaranteed to complete despite application-process failure. Is BackgroundTasks alone sufficient?','No: process-local background work does not guarantee survival or delivery after process failure.','Yes: add_task makes the work durable across process failure.','Yes, if the callable uses async def rather than def.','Registration defers work but does not provide durability across process failure.','Both callable forms are supported; async def does not create a survival guarantee.','Check the failure requirement, not merely when the task runs.'),
'determine_provider_execution_order':('order_options depends on pagination, and an operation depends on order_options. What is the execution order of these three consumers/providers?','pagination, then order_options, then the operation.','The operation, then order_options, then pagination.','order_options first, with pagination resolved after it returns.','Prerequisites are resolved before their consumers, not after the operation.','The pagination input must be resolved before order_options can consume its result.','Trace dependency edges from prerequisites toward consumers.'),
'predict_request_and_response_stack_traversal':('Middleware A is added first and B second. Which traversal is correct?','Request: B → A → handler; response: handler → A → B.','Request: A → B → handler; response: handler → B → A.','Request: B → A → handler; response: handler → B → A.','The last addition B is outermost and sees the request first and the response last.','The response exits the nested wrappers in reverse request order: A then B.','Place the last addition on the outside, then trace inward and outward.'),
'identify_reload_as_development_only':('Which reload choice matches the taught production ASGI serving guidance?','Omit --reload in production; use it for development.','Enable --reload in production to make serving more stable.','Enable --reload only when production uses several workers.','Development reload consumes resources and is less stable; it is not the taught production choice.','Workers and reload are mutually exclusive, and reload is development-only.','Separate development convenience from stable production serving.'),
'distinguish_worker_processes_from_development_reload':('A deployment selects multiple Uvicorn workers. Which statement matches the worker/reload contract?','--workers starts multiple worker processes and cannot be combined with --reload.','--reload starts the selected number of worker processes.','--workers requires --reload to manage those processes.','Reload is not worker process management; worker count is selected with --workers.','Uvicorn workers and reload are mutually exclusive.','Identify which option controls workers and which is for development.')
}
Q["identify_protocol_coupling_and_responsibility_boundaries"] = Q["identify_misplaced_transport_business_and_persistence_logic"]
# Build exercises from registered scaffolds; probes are evaluated by the real pinned runner below.
E={}
def exercise(c,prompt,starter,solution,tests,kind='python_asgi',mounts=None,entry='main.py',extra=None):
 E[c]={'prompt':prompt,'starter':starter,'solution':solution,'tests':tests,'kind':kind,'mounts':mounts or [],'entry':entry,'extra':extra or []}
def expr(x): return {'kind':'value_equals','spec':{'expr':x}}
def call(fn,*args): return {'kind':'function_call','spec':{'function':fn,'args':list(args)}}
def http(path,method='GET',params=None,headers=None):
 r={'method':method,'path':path}
 if params:r['params']=params
 if headers:r['headers']=headers
 return {'kind':'http_equals','spec':{'requests':[r]},'expected_keys':['status','json']}
c='rest.resource_contract_design'; st=file(c); vals={'orders_collection_path':'/orders','orders_item_path':'/orders/{order_id}','orders_retrieve_method':'GET','orders_create_method':'POST','orders_replace_method':'PUT','orders_remove_method':'DELETE','orders_created_location':'/orders/42','orders_created_status':201,'orders_absent_status':404}
# These literals are the glossary contract, not data-derived output. All test expected values are obtained from executing it.
sol=''.join(f'{n}: {"str" if isinstance(v,str) else "int"} = {json.dumps(v)}\n' for n,v in vals.items())
sc='\n# Supplied inspection harness; do not edit.\ndef inspect_contract(name):\n    return globals()[name]\n'
exercise(c,'Fill the nine annotated contract variables: collection /orders; item /orders/{order_id}; retrieval GET, collection creation POST, replacement PUT, removal DELETE; creation 201 with Location /orders/42; absent item 404. Do not implement handlers. Leave the supplied inspection harness unchanged.',st+sc,sol+sc,[call('inspect_contract',n) for n in vals])
c='fastapi.path_operations';st=file(c);sol='from fastapi import FastAPI\napp = FastAPI()\n'+st.split('# TODO: register POST')[0].replace('# TODO: import FastAPI and construct app.\n','') if False else 'from fastapi import FastAPI\napp = FastAPI()\n'
for meth,path,name in [('post','/orders','create_order'),('get','/orders/current','current_order'),('get','/orders/{order_id}','retrieve_order'),('put','/orders/{order_id}','replace_order'),('delete','/orders/{order_id}','remove_order')]:sol+=f'@app.{meth}("{path}")\ndef {name}():\n    return {{"handler": "{name}"}}\n'
exercise(c,'Import FastAPI, construct app, and register POST /orders as create_order, GET /orders/current as current_order, then GET, PUT and DELETE /orders/{order_id} as retrieve_order, replace_order and remove_order. Fixed GET must precede parameterized GET. Each handler returns exactly {"handler": "<its function name>"}; read no request inputs.',st,sol,[http('/orders','POST',params={'case':'first'}),http('/orders','POST',params={'case':'second'}),http('/orders/current',params={'case':'first'}),http('/orders/current',params={'case':'second'}),http('/orders/42'),http('/orders/7'),http('/orders/42','PUT'),http('/orders/7','PUT'),http('/orders/42','DELETE'),http('/orders/7','DELETE')])
# Real settings and real production serving need native packages/processes, absent from the pinned in-process runner. Keep native shell workspaces, never substitute simulations.
c='fastapi.validated_environment_configuration';cases=json.loads(file(c,'source_cases.json'));dotenv=file(c,'.env')
pre='#!/bin/sh\n# The native exercise environment must provide pydantic-settings.\npython3 - <<\'PY\'\n'
post='\n# Supplied verification, unchanged.\nimport os, json\nfrom pydantic import ValidationError\nfrom pathlib import Path\ncases = '+repr(cases)+'\nout = []\nfor case in cases:\n    os.environ.pop("APP_NAME", None)\n    os.environ.update(case["environment"])\n    Path(".env").write_text("".join(k + "=" + v + "\\n" for k,v in case["dotenv"].items()))\n    try:\n        out.append({"case": case["name"], "app_name": Settings().app_name})\n    except ValidationError:\n        out.append({"case": case["name"], "validation_error": True})\nprint(json.dumps(out, separators=(",", ":")))\nPY\n'
st=file(c,'settings.py');sol='from pydantic_settings import BaseSettings, SettingsConfigDict\n\nclass Settings(BaseSettings):\n    app_name: str\n    model_config = SettingsConfigDict(env_file=".env")\n\nsettings = Settings()\n'
# Put the supplied initial .env in place before constructing settings; setup is identical in both files.
setup='from pathlib import Path\nPath(".env").write_text('+repr(dotenv)+')\n'
expected_cases=[{'case':x['name'],**({'app_name':(x['environment'] or x['dotenv'])['APP_NAME']} if x['environment'] or x['dotenv'] else {'validation_error':True})} for x in cases]
exercise(c,'In the marked Python block of run.sh, declare Settings(BaseSettings) with required app_name: str, model_config = SettingsConfigDict(env_file=".env"), and construct settings = Settings() before serving. Keep the supplied shell/setup/case harness unchanged. Run the script in the native environment with pydantic-settings installed. It checks environment-only, conflicting environment/dotenv, and absent-both cases; failures in required settings must occur at construction.',pre+setup+st+post,pre+setup+sol+post,[{'kind':'stdout_equals','spec':{'expected':json.dumps(expected_cases,separators=(',',':'))}}],kind='bash',entry='run.sh')
c='integration.async_http_requests'; st=file(c)
sc='''# Supplied isolated HTTPX harness: no network. Leave unchanged.
import asyncio
from fastapi import FastAPI
app = FastAPI()
opened = []
first_url, second_url = lookup_urls
_OriginalClient = httpx.AsyncClient
class TrackedClient(_OriginalClient):
    def __init__(self, *args, **kwargs):
        self.seen = []
        def respond(request):
            self.seen.append(str(request.url))
            return httpx.Response(200, json={"ok": True})
        super().__init__(*args, transport=httpx.MockTransport(respond), **kwargs)
        opened.append(self)
from types import SimpleNamespace
httpx = SimpleNamespace(**{**vars(httpx), "AsyncClient": TrackedClient})
@app.get("/audit")
async def audit(case: str):
    opened.clear()
    await orders()
    return {"clients": len(opened), "closed": all(c.is_closed for c in opened), "urls": [u for c in opened for u in c.seen]}
'''
# The audit is supplied setup, defined before the learner's function.
st=st.replace('async def orders():',sc+'\nasync def orders():'); sol=st.replace('    # TODO: one owning AsyncClient scope, both awaited calls, then cleanup.\n    pass','    async with httpx.AsyncClient() as client:\n        first = await client.get(first_url)\n        second = await client.get(second_url)')
exercise(c,'Complete orders(): use one owning async with httpx.AsyncClient() as client scope and await GET for both supplied lookup_urls in order inside it. The client must close on scope exit. Leave the supplied no-network audit harness unchanged; /audit reports the client count, closure and visited URLs.',st,sol,[http('/audit',params={'case':'first'}),http('/audit',params={'case':'second'})])
c='pydantic.domain_validation';st=file(c)
sc='''\n# Supplied construction harness, unchanged.
def check_booking(start, end):
    try:
        booking = Booking(start=start, end=end)
        return {"accepted": True, "start": booking.start, "end": booking.end}
    except ValidationError:
        return {"accepted": False}
'''
sol=st.replace('    # TODO: add an after-model invariant validator.','''    @model_validator(mode='after')
    def validate_order(self):
        if self.end <= self.start:
            raise ValueError("end must exceed start")
        return self''')
exercise(c,'Add an after-model instance validator validate_order to Booking. Reject end <= start with ValueError and return self when end > start. Preserve the supplied integer fields and harness. The tests include independently valid integer pairs that violate the invariant, equality, and consistent pairs.',st+sc,sol+sc,[call('check_booking',5,3),call('check_booking',3,3),call('check_booking',3,5),call('check_booking',2,7)])
c='fastapi.expected_http_errors';st=file(c);sol=st.replace('        # TODO: raise the intended expected rejection here.\n        pass','        raise HTTPException(status_code=404, detail="Order not found")')
exercise(c,'Complete get_order: if the supplied order is None, raise HTTPException(status_code=404, detail="Order not found"). Do not return an exception or fall through to success. Keep the existing route and return order. The default rejection body must be {"detail": "Order not found"}.',st,sol,[http('/order',params={'case':'one'}),http('/order',params={'case':'two'})])
c='fastapi.handler_execution_choice';st=file(c); supplied=file(c,'supplied.py'); st=st.replace('from supplied import shipping_client',supplied)
sc='''\n# Supplied inspection harness, unchanged.
import inspect
def inspect_execution(part):
    if part == "handler":
        return {"is_async": inspect.iscoroutinefunction(shipping), "result": shipping()}
    return {"is_async": inspect.iscoroutinefunction(shipping_utility), "result": shipping_utility()}
'''
sol=st.replace('async def shipping():  # TODO: choose execution mode for blocking I/O.','def shipping():').replace('# TODO: annotate execution location of handler and direct utility call.','# FastAPI runs this def path operation in its external thread pool.\n# The direct utility call runs there with the handler; it is not separately offloaded.')
exercise(c,'The supplied shipping_client performs blocking I/O. Choose the handler declaration that matches it, preserving the direct shipping_utility() call and returned result. Add comments: FastAPI executes the normal path operation in its thread pool; the direct utility runs with that handler, not by separate automatic offload. Do not await the blocking utility. Keep the stand-in and inspection harness unchanged.',st+sc,sol+sc,[call('inspect_execution','handler'),call('inspect_execution','utility')])
c='fastapi.modular_application';f=file(c,'orders.py'); main=file(c)
# The runner executes a single entry. The supplied loader materializes the feature module from the marked block.
loader='\n# Supplied module loader; leave unchanged.\nfrom pathlib import Path\nPath("orders.py").write_text(feature_source)\n'
st='feature_source = '+repr(f)+loader+main
feature='from fastapi import APIRouter\nrouter = APIRouter()\n@router.get("/orders")\ndef list_orders():\n    return []\n';sol='feature_source = '+repr(feature)+loader+'from fastapi import FastAPI\nfrom orders import router\napp = FastAPI()\napp.include_router(router, prefix="/api")\n'
exercise(c,'Edit the Python feature_source block that the supplied loader writes to orders.py: construct router = APIRouter(), register GET /orders as list_orders, and return []. Then in the application section import router from orders and include it in app with prefix="/api". Leave the file-loader scaffolding unchanged. The served route is GET /api/orders, not GET /orders.',st,sol,[http('/api/orders',params={'case':'one'}),http('/api/orders',params={'case':'two'}),http('/orders',params={'case':'one'}),http('/orders',params={'case':'two'})])
c='fastapi.path_query_binding';st=file(c);sol=st.replace('def read_order():  # TODO: typed order_id and defaulted limit inputs.','def read_order(order_id: int, limit: int = 10):')
exercise(c,'Complete read_order(order_id: int, limit: int = 10) for the existing /orders/{order_id} route. Return exactly {"order_id": order_id, "limit": limit}. order_id binds from the path, limit from query, omitted limit uses 10, and unconvertible path values must be rejected rather than passed to the handler.',st,sol,[http('/orders/42'),http('/orders/7',params={'limit':'3'}),http('/orders/not-an-integer',params={'case':'first'}),http('/orders/not-an-integer',params={'case':'second'})])
c='fastapi.response_model_serialization';st=file(c).replace('def read_order(order_id: int):','def read_order(order_id: int) -> dict:')
original = next(n for n in ast.parse(st).body if isinstance(n,ast.Assign) and n.targets[0].id == 'internal_order')
old = ast.get_source_segment(st,original)
fixture = 'import csv\n_fixture = next(csv.DictReader(open("internal_orders.csv")))\ninternal_order = {"order_id": int(_fixture["order_id"]), "status": _fixture["status"], "private_processing_note": _fixture["private_processing_note"]}'
st = st.replace(old, '# Supplied registry CSV loader; leave unchanged.\n'+fixture)
sol=st.replace('# TODO: PublicOrder with the two public fields only.','class PublicOrder(BaseModel):\n    order_id: int\n    status: str').replace('@app.get("/orders/{order_id}")  # TODO: configure response_model.','@app.get("/orders/{order_id}", response_model=PublicOrder)')
exercise(c,'Define PublicOrder(BaseModel) with only order_id: int and status: str. Configure response_model=PublicOrder on the existing GET decorator, keep the supplied -> dict return annotation, and return internal_order unchanged. The body must contain only order_id and status; private_processing_note must be filtered. Leave the supplied CSV loader unchanged. The declared response model takes priority over the return annotation.',st,sol,[http('/orders/42'),http('/orders/7')],mounts=[{'asset_id':'ds.internal_orders','mount_path':'internal_orders.csv'}])
c='fastapi_backend.depends';st=file(c);sol=st.replace('def orders():  # TODO: declare context through Annotated and Depends.','def orders(context: Annotated[str, Depends(provider)]):').replace('    return {}  # TODO: return supplied context, without calling provider here.','    return {"context": context}')
sc = '''\n# Supplied declaration inspector; leave unchanged.\ndef inspect_dependency(part):\n    import inspect\n    annotation = inspect.signature(orders).parameters["context"].annotation\n    metadata = getattr(annotation, "__metadata__", ())\n    dependency = next((x.dependency for x in metadata if hasattr(x, "dependency")), None)\n    if part == "provider":\n        return getattr(dependency, "__name__", None)\n    return dependency is provider\n'''
st += sc; sol += sc
exercise(c,'Declare orders(context: Annotated[str, Depends(provider)]) and return exactly {"context": context}. Pass the provider callable, not provider(), to Depends; do not call it in the handler body. Preserve the supplied provider. Its fixture string is not verified authentication. Leave the supplied declaration inspector unchanged.',st,sol,[http('/orders',params={'case':'one'}),http('/orders',params={'case':'two'}),call('inspect_dependency','provider'),call('inspect_dependency','identity')])
c='integration.outbound_timeouts';st=file(c);sc='''# Supplied no-network timeout fixture and async test adapter; leave unchanged.
from fastapi import FastAPI
app = FastAPI()
mode = "read"
clients = []
_OriginalClient = httpx.AsyncClient
class FixtureClient(_OriginalClient):
    def __init__(self, *args, **kwargs):
        self.explicit_timeout = kwargs.get("timeout")
        clients.append(self)
        def respond(request):
            exc = {"read": httpx.ReadTimeout, "connect": httpx.ConnectTimeout, "write": httpx.WriteTimeout, "pool": httpx.PoolTimeout}.get(mode)
            if exc:
                raise exc("supplied exceeded wait", request=request)
            return httpx.Response(200, text="shipping-ok")
        super().__init__(*args, transport=httpx.MockTransport(respond), **kwargs)
from types import SimpleNamespace
httpx = SimpleNamespace(**{**vars(httpx), "AsyncClient": FixtureClient})
@app.get("/probe")
async def probe(case: str):
    global mode
    mode = case
    clients.clear()
    result = await shipping_lookup()
    return {"result": result, "timeouts": [c.explicit_timeout for c in clients], "closed": all(c.is_closed for c in clients)}
'''
st=st.replace('async def shipping_lookup():',sc+'\nasync def shipping_lookup():');sol=st.replace('    # TODO: finite HTTPX timeout and distinct timeout outcome.\n    pass','''    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(shipping_url)
            return "shipping-ok"
    except httpx.ConnectTimeout:
        return "connect-timeout"
    except httpx.ReadTimeout:
        return "read-timeout"
    except httpx.WriteTimeout:
        return "write-timeout"
    except httpx.PoolTimeout:
        return "pool-timeout"''')
exercise(c,'Complete shipping_lookup with a finite five-second HTTPX timeout and an awaited GET of shipping_url. Return "shipping-ok" after success; handle ConnectTimeout, ReadTimeout, WriteTimeout and PoolTimeout separately, returning "connect-timeout", "read-timeout", "write-timeout" and "pool-timeout" respectively. Keep the supplied no-network fixture unchanged. These are wait limits, not a total elapsed budget.',st,sol,[http('/probe',params={'case':x}) for x in ['read','connect','write','pool','success']])
c='design.backend_separation_of_concerns';st=file(c).replace('from supplied import order_state, adapter, requested_quantity',file(c,'supplied.py'))
# Preserve supplied adapter, expose plain rule and declare provider. No new database syntax.
start=st.index('@app.get');sol=st[:start]+'''def accepts_quantity(requested: int, stored: int) -> bool:
    return requested <= stored

@app.get("/orders/{order_id}")
def decide_order(order_id: int, quantity: int = Depends(requested_quantity)):
    stored = adapter.quantity(order_id)
    return accepts_quantity(quantity, stored)
'''
exercise(c,'Refactor only the handler area. Define plain accepts_quantity(requested: int, stored: int) -> bool returning requested <= stored. In decide_order declare quantity: int = Depends(requested_quantity), retrieve stored quantity only through adapter.quantity(order_id), call accepts_quantity with explicit values, and return its boolean result. Leave the supplied fixture, adapter and provider unchanged. No FastAPI objects or stored-state access belong in the plain rule.',st,sol,[call('accepts_quantity',5,5),call('accepts_quantity',6,5),http('/orders/42',params={'quantity':'5'}),http('/orders/42',params={'quantity':'6'}),http('/orders/43',params={'quantity':'1'})])
c='fastapi.bounded_background_tasks';st=file(c).replace('from supplied import order_follow_up',file(c,'supplied.py'));sol=st.replace('def create_order():  # TODO: declare background_tasks parameter.','def create_order(background_tasks: BackgroundTasks):').replace('    # TODO: register optional follow-up before returning response.','    background_tasks.add_task(order_follow_up, order_id)').replace('    return {"order_id": order_id}','    # Process-local optional work; this would NOT meet guaranteed completion.\n    return {"order_id": order_id}')
sc='''\n# Supplied registration inspection, unchanged.
def inspect_registration(order_id):
    import inspect
    tasks = BackgroundTasks()
    follow_ups.clear()
    response = create_order(tasks)
    return {"response": response, "before_response_follow_ups": list(follow_ups), "tasks": [{"callable": t.func.__name__, "args": list(t.args)} for t in tasks.tasks], "durability_annotation": "NOT meet guaranteed completion" in inspect.getsource(create_order)}
'''
exercise(c,'Declare background_tasks: BackgroundTasks and register order_follow_up with the supplied local order_id using add_task; do not invoke the callable immediately. Return the existing order response. Add a comment saying this process-local optional work would NOT meet guaranteed completion. The supplied inspector checks registration before response and that explicit limitation; leave it unchanged.',st+sc,sol+sc,[call('inspect_registration','first'),call('inspect_registration','second')])
c='fastapi.dependency_composition';st=file(c);sol=st.replace('def pagination():  # TODO: typed page and page_size query inputs.','def pagination(page: int, page_size: int) -> dict[str, int]:').replace('    return {}  # TODO: return page and page_size.','    return {"page": page, "page_size": page_size}').replace('def order_options():  # TODO: declared dependency on pagination.','def order_options(pagination_value: Annotated[dict[str, int], Depends(pagination)]) -> dict[str, int]:').replace('    return {}  # TODO: return supplied dictionary.','    return pagination_value').replace('def orders():  # TODO: declared dependency on order_options.','def orders(options: Annotated[dict[str, int], Depends(order_options)]):').replace('    return {}  # TODO: return order-options result.','    return options')
sc = '''\n# Supplied graph inspector; leave unchanged.\ndef inspect_edge(part):\n    import inspect\n    fn = order_options if part == "order_options" else orders\n    parameter = next(iter(inspect.signature(fn).parameters.values()))\n    metadata = getattr(parameter.annotation, "__metadata__", ())\n    dependency = next((x.dependency for x in metadata if hasattr(x, "dependency")), None)\n    return getattr(dependency, "__name__", None)\n'''
st += sc; sol += sc
exercise(c,'Complete pagination(page: int, page_size: int) -> dict[str, int] returning exactly page and page_size keys. Declare order_options input through Annotated[dict[str, int], Depends(pagination)] and return that dictionary. Declare the operation input through Annotated[dict[str, int], Depends(order_options)] and return it. Both query inputs are required; the dependency edges must resolve pagination before order_options before the operation.',st,sol,[http('/orders',params={'page':'2','page_size':'10'}),http('/orders',params={'page':'3','page_size':'5'}),call('inspect_edge','order_options'),call('inspect_edge','orders')])
c='fastapi.existing_middleware_stack';st=file(c).replace('from supplied import A, B',file(c,'supplied.py'));opts=json.loads(file(c,'middleware_options.json'));sol=st.replace('# TODO: add A first, B second using app.add_middleware.','app.add_middleware(A, minimum_size='+repr(opts['A']['documented_options']['minimum_size'])+')\napp.add_middleware(B, allowed_hosts='+repr(opts['B']['documented_options']['allowed_hosts'])+')').replace('# TODO: annotate request and resulting response traversal.','# B is outermost. Request: B -> A -> handler\n# Response: handler -> A -> B')
sc='''\n# Supplied inspection harness, unchanged.
def inspect_stack(direction):
    from pathlib import Path
    import tokenize, io
    source = Path("main.py").read_text()
    comments = [t.string for t in tokenize.generate_tokens(io.StringIO(source).readline) if t.type == tokenize.COMMENT]
    wrappers = [{"class": m.cls.__name__, "options": m.kwargs} for m in app.user_middleware]
    if direction == "request":
        return {"wrappers": wrappers, "annotation": "# B is outermost. Request: B -> A -> handler" in comments}
    return {"wrappers": list(reversed(wrappers)), "annotation": "# Response: handler -> A -> B" in comments}
'''
exercise(c,'Configure the supplied A first with minimum_size=500, then B with allowed_hosts=["testserver"], using app.add_middleware. Do not implement middleware. Add exact comments "# B is outermost. Request: B -> A -> handler" and "# Response: handler -> A -> B". Leave supplied imports, handler and inspector unchanged; it checks real configuration order/options and both annotations.',st+sc,sol+sc,[call('inspect_stack','request'),call('inspect_stack','response')])
c='fastapi.production_asgi_serving';st=file(c,'run.sh');sol='#!/bin/sh\nuvicorn main:app --host 0.0.0.0 --port 8000\n'
exercise(c,'Run the supplied main.py application from its directory with uvicorn main:app --host 0.0.0.0 --port 8000. Put that command in run.sh. Do not enable --reload or edit the application. Success requires actual startup on the specified host and port in the native Uvicorn environment, not merely parsing a command.',st,sol,[{'kind':'http_equals','spec':{'launch':{'entry':'run.sh','host':'0.0.0.0','port':8000,'forbid_flags':['--reload']},'requests':[{'method':'GET','path':'/orders'}],'expected':{'status':__import__('http').HTTPStatus.OK.value,'json':ast.literal_eval(next(n.value for n in ast.walk(ast.parse(file(c))) if isinstance(n,ast.Return))) }},'message_on_fail':'The native launch must serve the supplied /orders endpoint on the specified host/port, without --reload.'}],kind='bash',entry='run.sh',extra=[{'path':'main.py','role':'readonly','content':file(c)}])
# Derived runtime version for native shell exercises (no shell engine is pinned in the registry).
shell_version=subprocess.check_output(['bash','--version'],text=True).splitlines()[0]
out={k:plans[k] for k in ['schema_version','path_id','batch_id']};out['kind']='interactions_part';out['tiles']=[]
for t in plans['tiles']:
 entries=[];seen=set();checks=[s for s in t['steps'] if s['type'] in ('check','hands_on')]
 for idx,s in enumerate(checks):
  c=s['concept_ids'][0]; anchors=s['anchors']; b=bundles[c]
  measures=[]
  for a in anchors:
   if '#assessment:' in a:
    cap=a.split('#assessment:')[1]; an=next(x for x in b['assessment_anchors'] if x['capability']==cap)
    measures.append({'concept_id':c,'capability':cap,'fact_ids':an['fact_ids']})
  if not measures:
   measures=[{'concept_id':c,'capability':an['capability'],'fact_ids':an['fact_ids']} for an in b['assessment_anchors']]
  ix={'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'],'difficulty':'intro' if idx==0 else ('stretch' if idx==len(checks)-1 and len(checks)>=3 else 'core'),'grading_mode':'client','standalone':True,'measures':measures,'anchors':anchors}
  facts=' '.join(next(f['statement'] for f in b['coverage']['required_facts'] if f['id']==fid) for fid in dict.fromkeys(fid for m in measures for fid in m['fact_ids']))
  facts = facts or b['practice_anchor']['success']
  fb={'correct':{'message':facts},'incorrect':{'message':'Review the distinction and try again. '+facts},'hints':['Separate the declared contract from incidental implementation details.']}
  if c not in seen:
   rem=next((r['step_id'] for r in next(x for x in screens['tiles'] if x['tile_id']==t['tile_id']).get('remediation_steps',[]) if c in r['concept_ids']),None)
   if rem:fb['remediation_step_id']=rem
   seen.add(c)
  if ix['type']=='choice':
   cap=measures[0]['capability'];prompt,right,w1,w2,why1,why2,hint=Q[cap]
   # Assign key by matching authored correct text, not by assuming a position.
   texts=[w1,right,w2] if idx%2 else [right,w2,w1]
   options=[{'option_id':'o'+str(i+1),'text':tx} for i,tx in enumerate(texts)]
   ix['public']={'prompt':prompt,'options':options,'selection':'single','shuffle':True}
   explanations={right:facts,w1:why1,w2:why2};ix['grading']={'correct_option_ids':[x['option_id'] for x in options if x['text']==right],'option_feedback':{x['option_id']:{'message':explanations[x['text']]} for x in options}};fb['hints']=[hint]
  else:
   e=E[c];kind=e['kind'];lc=b['practice_anchor']['live_code'];tests=copy.deepcopy(e['tests'])
   for i,test in enumerate(tests):
    test['test_id']='test.'+s['step_id']+'.'+str(i+1);test['visible']=True;test.setdefault('message_on_fail','Check the exact output and the required declaration in the prompt.')
   ix['public']={'prompt':e['prompt'],'runtime':{'kind':kind,'version':shell_version if kind=='bash' else pins[kind]['version']},'workspace':{'entry':e['entry'],'files':[{'path':e['entry'],'role':'editable','language':'bash' if kind=='bash' else 'python','content':e['starter']}]+e['extra'],'asset_mounts':e['mounts']},'constraints':{k:lc[k] for k in ['allowed_syntax','blocked_syntax']}}
   ix['grading']={'solution_files':[{'path':e['entry'],'content':e['solution']}],'tests':tests}
   fb['hints']=['Identify the owning scope or declared boundary before filling the edit slots.','Compare each required result with the practice contract.']
   if kind!='bash':
    # Real pinned execution: no expected result is hand-written.
    probes=[sandbox._py_probe(x) for x in tests]
    job=sandbox._py_job(kind,[],[sandbox._py_script('derive',e['entry'],e['solution'],sandbox._py_mounts(sandbox._tables(reg,e['mounts'],{},[])[0]),probes)])
    res=sandbox.node_run(job,pins[kind]['runner'])['results']['derive']
    if not res['ok']:raise RuntimeError(c+': '+res.get('error','unknown'))
    for test in tests:
     got=res['probes'][test['test_id']]
     if not got['ok']:raise RuntimeError(c+': '+str(got))
     value=got['value'];keys=test.pop('expected_keys',None)
     test['spec']['expected']={k:value[k] for k in keys} if keys else value
    print(c,'derived',len(tests),'tests',flush=True)
  ix['feedback']=fb;entries.append({'step_id':s['step_id'],'interaction':ix})
 out['tiles'].append({'tile_id':t['tile_id'],'interactions':entries})
(B/'interactions.json').write_text(json.dumps(out,indent=2)+'\n')
print('Wrote',sum(len(t['interactions']) for t in out['tiles']),'interactions')
