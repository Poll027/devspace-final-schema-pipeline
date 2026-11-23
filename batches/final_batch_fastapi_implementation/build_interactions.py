import json,sys,copy
from pathlib import Path
B=Path(__file__).parent
P=json.loads((B/'tile_plans.json').read_text()); S=json.loads((B/'screens.json').read_text()); G={b['context']['concept_id']:b for b in json.loads((B/'inputs/path_glossary_bundle.json').read_text())['bundles']}; R=json.loads((B/'scenario_asset_registry.json').read_text()); A={a['asset_id']:a for a in R['assets']}
PIN=json.loads(Path('00_FINAL_PIPELINE_CORE/registry/runtimes.json').read_text())['runtimes']
choices={}
def q(s,p,correct,wrong1,why1,wrong2,why2):choices[s]=(p,correct,wrong1,why1,wrong2,why2)
q('tile_022.s03','An orders contract creates item /orders/42; a separate retrieval asks for an absent item. Which response pair fits these two cases?','Creation: 201 with Location /orders/42; absent item: 404.','Creation: 404; absent item: 201.','This reverses creation and absence.','Creation: 201 with Location /orders; absent item: 404.','The Location must identify the created item, not just its collection.')
q('tile_022.s09','GET /orders and POST /orders are registered to distinct handlers. How many path operations do these declarations define?','Two: each method-path combination is an operation.','One: identical paths merge the handlers.','The method is part of the operation identity.','Two only if the paths are renamed.','Different methods already distinguish operations on one path.')
q('tile_022.s10','The following GET routes are declared in this order; order_id has no type restriction. Which handler receives GET /orders/current?\n```python\n@app.get("/orders/{order_id}")\ndef item(order_id): return "item"\n@app.get("/orders/current")\ndef current(): return "current"\n```','item: the earlier parameterized route captures current.','current: fixed routes always take priority.','Routes are evaluated in declaration order.','Neither: sharing a prefix prevents registration.','Overlapping routes can register; their evaluation order matters.')
q('tile_024.s05','APP_NAME is an environment variable containing "environment-orders". The configured .env contains APP_NAME=dotenv-orders. With no initializer override, what should validated settings use?','environment-orders, because environment values take precedence.','dotenv-orders, because the file was configured explicitly.','Configuring a dotenv file does not give it priority over environment variables.','Construction must fail whenever the two sources differ.','A conflicting source is resolved by precedence, not automatically a validation failure.')
q('tile_025.s05','Two sequential shipping lookups belong to one owning scope. Which client placement preserves reuse and cleanup?','Open one async client scope, await both requests inside it, then leave the scope.','Open and close a different client for each lookup.','That loses reuse across these lookups.','Exit the client scope after lookup one, then use it for lookup two.','The owning scope must finish using the client before cleanup.')
q('tile_026.s04','Booking has individually valid integer start and end fields. Which rule requires their relationship to be checked together?','end must be later than start.','start must be an integer.','This concerns one field rather than the relationship.','end must be an integer.','This also concerns one field rather than comparing both values.')
q('tile_026.s05','Which supplied pair isolates a failure of end > start while keeping both inputs individually valid integers?','start=5, end=3.','start=3, end=5.','This pair satisfies end > start.','start="not-an-integer", end=5.','This introduces a single-field type failure instead of isolating the invariant.')
q('tile_026.s09','An absent-order branch must reject deliberately and stop before the normal return. Which form does that?','raise HTTPException(status_code=404, detail="Order not found")','return HTTPException(status_code=404, detail="Order not found")','Returning an exception is not raising a deliberate rejection.','Construct HTTPException, then continue to the normal return.','Construction alone does not stop control flow.')
q('tile_026.s10','A deliberate HTTP rejection requires a client-facing header X-Reason: absent. Where should the rejection attach it?','HTTPException(..., headers={"X-Reason": "absent"})','Only inside the detail text.','Text in detail is not a response header.','Nowhere: deliberate rejections cannot carry headers.','HTTPException supports headers for the rejection.')
q('tile_028.s04','An async def handler directly calls a normal utility that performs blocking I/O. Is the call automatically moved into FastAPI’s external thread pool?','No; the direct utility call runs where the async handler calls it.','Yes; all normal utility functions are automatically offloaded.','FastAPI does not automatically offload directly called utilities.','Yes; spelling the handler async makes blocking I/O nonblocking.','The async declaration does not change a blocking library call’s behavior.')
q('tile_029.s04','orders.py registers GET /orders on an APIRouter, but main.py never includes that router. What is missing for the main application to expose the feature?','Import and include the feature router on the application.','Rename the local path to /api/orders without including the router.','A path rename does not include a feature router.','Nothing: creating APIRouter automatically attaches it to every app.','Router registration and application inclusion are separate steps.')
q('tile_030.s05','For a handler input limit: int = 10 that is not in the route path, what happens when the query string omits limit?','The handler receives the default integer 10.','The query input is required despite its default.','The default makes omission valid.','The handler receives the string "10".','The input is annotated int, including the default used here.')
q('tile_030.s06','GET /orders/{order_id} binds order_id: int. A request uses /orders/not-an-integer. Which result follows from path conversion?','Validation rejects the unconvertible path value before the handler runs.','The handler receives the original string.','The int annotation requires conversion and validation.','The value is taken from a query input instead.','The matching path placeholder determines the binding source.')
q('tile_030.s11','PublicOrder declares only order_id and status. A handler returns an internal dictionary containing those fields plus private_processing_note through response_model=PublicOrder. Which fields appear publicly?','order_id and status only.','All three dictionary fields.','Normal response-model processing projects the declared public fields.','private_processing_note only.','The private note is not declared in PublicOrder.')
q('tile_030.s12','A route declares response_model=PublicOrder but returns a directly constructed Response. Can you rely on response-model filtering for that returned response?','No; a directly returned Response bypasses that normal model processing.','Yes; the decorator filters every returned Response.','Direct Response return is the bypass case.','Yes; a return annotation restores filtering of the Response.','A return annotation does not remove the direct-response bypass.')
q('tile_032.s05','A shared provider must produce one context string for several handlers. What makes its input-provision behavior explicit?','Put the reusable provision logic in a callable and declare it as a dependency parameter.','Read an unrelated global context in each handler instead.','That does not declare provider-supplied input.','Treat the provider as a handler decorator rather than a supplied input.','The callable supplies a value through the declared dependency input.')
q('tile_033.s03','HTTPX has a finite read timeout. A response keeps supplying chunks within that wait limit, but the whole request takes longer than the timeout number. Which interpretation is correct?','The read limit bounds individual chunk waits, not total elapsed request duration.','The read limit always enforces that whole-request elapsed deadline.','Read timeouts concern individual chunk waits.','Finite timeout and timeout=None both disable enforcement.','timeout=None disables enforcement; a finite limit does not.')
q('tile_033.s04','An asynchronous operation exceeds a budget inside async with asyncio.timeout(seconds). Where is the converted TimeoutError caught?','Outside the timeout context.','Only inside the context before it exits.','The cancellation is converted to TimeoutError outside that context.','As httpx.ReadTimeout regardless of the work inside.','The total-budget context converts to TimeoutError, not an HTTPX read-wait exception.')
q('tile_034.s03','A reusable business decision takes a FastAPI request object and builds an HTTP response. What boundary should a refactor restore?','Use ordinary values for the business decision; keep HTTP adaptation in the handler.','Move HTTP response construction into the persistence adapter.','Stored-state access and HTTP adaptation are different responsibilities.','Make every business caller construct a FastAPI request.','That preserves protocol coupling instead of removing it.')
q('tile_034.s08','Which task fits optional in-process BackgroundTasks rather than a durable execution guarantee?','A small optional follow-up whose loss on process failure is acceptable.','A required job that must finish despite process failure.','Process-local deferred work does not provide that guarantee.','A long critical job whose completion must survive restart.','Critical durable completion needs are not satisfied by this placement.')
q('tile_034.s12','The operation depends on order_options, which depends on pagination. What prerequisite-first execution order follows?','pagination → order_options → operation.','operation → order_options → pagination.','A consumer needs its prerequisites resolved first.','order_options → pagination → operation.','order_options consumes pagination, so pagination must be resolved first.')
q('tile_037.s03','A is added with app.add_middleware before B. Which wrapper traversal matches this ordering?','Request: B → A → handler; resulting response: handler → A → B.','Request: A → B → handler; response: handler → B → A.','The later-added B is outermost.','Request and response both travel B → A → handler.','The resulting response travels back outward through the wrappers.')
q('tile_037.s06','A deployment specifies multiple Uvicorn worker processes. Which option combination respects the workers/reload boundary?','Use --workers with the supplied count and omit --reload.','Use --reload as a replacement for worker processes.','Reload is development support, not worker process management.','Combine --workers and --reload for production.','The two options are mutually exclusive.')
EX={}
def ex(cid,starter,solution,prompt,tests,kind='python_asgi',packages=None):EX[cid]=(starter,solution,prompt,tests,kind,packages or [])
def vt(expr):return ('value_equals',{'expr':expr})
def ft(name,*args):return ('function_call',{'function':name,'args':list(args)})
def ht(method,path,**kw):return ('http_equals',{'requests':[{'method':method,'path':path,**kw}],'expected_keys':['status','json']})
# Scaffolding is present unchanged in starter and solution. Tests inspect the completed contract itself.
cid='rest.resource_contract_design'; fields=['orders_collection_path','orders_item_path','orders_retrieve_method','orders_create_method','orders_replace_method','orders_remove_method','orders_created_location','orders_created_status','orders_absent_status']
values=['/orders','/orders/{order_id}','GET','POST','PUT','DELETE','/orders/42',201,404]
sc='\n# Supplied read-only contract inspector.\ndef inspect_contract(section):\n    if section == "identity_and_methods":\n        return ['+', '.join(fields[:6])+']\n    return ['+', '.join(fields[6:])+']\n'
start=A['ws.'+cid]['files'][0]['content']+sc
sol=''.join(f'{n}: {"int" if isinstance(v,int) else "str"} = {v!r}\n' for n,v in zip(fields,values))+sc
ex(cid,start,sol,'Complete the nine annotated contract variables: collection /orders, item /orders/{order_id}; retrieval GET, collection creation POST, replacement PUT, removal DELETE; creation 201 with Location /orders/42 and absent-item status 404. Do not implement handlers. The supplied inspector checks identity/methods and response details separately.',[ft('inspect_contract','identity_and_methods'),ft('inspect_contract','responses')],kind='python')
# Actual method/path dispatch with static, supplied distinct markers.
sc='from fastapi import FastAPI\napp = FastAPI()\ncreated = "created"\ncurrent = "current"\nretrieved = "retrieved"\nreplaced = "replaced"\nremoved = "removed"\n'
body='''def create_order(): return created
def current_order(): return current
def retrieve_order(): return retrieved
def replace_order(): return replaced
def remove_order(): return removed
'''
sol=sc+'''@app.post("/orders")
def create_order(): return created
@app.get("/orders/current")
def current_order(): return current
@app.get("/orders/{order_id}")
def retrieve_order(): return retrieved
@app.put("/orders/{order_id}")
def replace_order(): return replaced
@app.delete("/orders/{order_id}")
def remove_order(): return removed
'''
# Additional constant mutations cover remove too, via function-call route inspector.
sc2='''
# Supplied registration inspector: no request handling by the learner.
def registration(index):
    routes = [r for r in app.routes if r.path.startswith("/orders")]
    r = routes[index]
    return [r.path, sorted(r.methods), r.endpoint.__name__]
'''
ex('fastapi.path_operations',sc+body+sc2,sol+sc2,'Register POST /orders, then fixed GET /orders/current before GET /orders/{order_id}, plus PUT and DELETE on that item path. Keep the five supplied distinct handler names and static return markers; do not add handler parameters. Tests inspect all registrations and request dispatch.',[ht('POST','/orders'),ht('GET','/orders/current'),ht('GET','/orders/42'),ht('GET','/orders/7'),ht('PUT','/orders/42'),ht('PUT','/orders/7'),ht('DELETE','/orders/42'),ht('DELETE','/orders/7'),*[ft('registration',i) for i in range(5)]],packages=['fastapi'])
# Compatibility settings source harness: real Pydantic v1 BaseSettings, because pydantic-settings is absent from the pinned runtime.
sc='''from pydantic.v1 import BaseSettings, ValidationError
import os
# Supplied source adapter for this compatibility exercise. No network or host files.
def dotenv_source(settings):
    return {"app_name": os.environ["FIXTURE_DOTENV_APP_NAME"]} if "FIXTURE_DOTENV_APP_NAME" in os.environ else {}
'''
config='''    class Config:
        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            return init_settings, env_settings, dotenv_source, file_secret_settings
'''
sc2='''
# Supplied construction harness; each invocation resets its source fixtures.
def construct_case(environment, dotenv):
    os.environ.pop("APP_NAME", None)
    os.environ.pop("FIXTURE_DOTENV_APP_NAME", None)
    if environment is not None: os.environ["APP_NAME"] = environment
    if dotenv is not None: os.environ["FIXTURE_DOTENV_APP_NAME"] = dotenv
    try:
        settings = Settings()
        return {"accepted": True, "app_name": settings.app_name}
    except ValidationError:
        return {"accepted": False}
'''
cs=json.loads(next(f['content'] for f in A['ws.fastapi.validated_environment_configuration']['files'] if f['path']=='source_cases.json'))
ex('fastapi.validated_environment_configuration',sc+'class Settings(BaseSettings):\n    app_name: str = ""\n'+config+sc2,sc+'class Settings(BaseSettings):\n    app_name: str\n'+config+sc2,'The pinned sandbox lacks pydantic-settings and python-dotenv. This compatibility exercise uses genuine Pydantic v1 BaseSettings with a supplied source adapter standing in for the .env reader; it is not execution of SettingsConfigDict(env_file=".env"). Remove the empty-string default so app_name is required. Keep the supplied precedence adapter unchanged. Run the constructor harness for environment-only, conflicting-source and absent-source cases; it must accept supplied names, prefer the environment, and reject absence before serving.',[ft('construct_case',c['environment'].get('APP_NAME'),c['dotenv'].get('APP_NAME')) for c in cs],packages=['pydantic'])
# Supplied HTTPX MockTransport intercepts fictional URLs; the learner still uses real AsyncClient lifetime/await semantics.
sc='''import httpx
from fastapi import FastAPI
app = FastAPI()
lookup_one = "https://shipping.example.test/orders/42"
lookup_two = "https://shipping.example.test/orders/43"
events = []
_RealClient = httpx.AsyncClient
class SuppliedClient(_RealClient):
    def __init__(self, **kwargs):
        self.fixture_owned = not kwargs
        if kwargs:
            super().__init__(**kwargs)
            return
        async def respond(request):
            events.append(["request", str(request.url)])
            return httpx.Response(200, json={"status": "supplied"})
        super().__init__(transport=httpx.MockTransport(respond))
        events.append(["opened"])
    async def aclose(self):
        if self.fixture_owned: events.append(["closed"])
        await super().aclose()
    async def __aexit__(self, *args):
        if self.fixture_owned: events.append(["closed"])
        return await super().__aexit__(*args)
httpx.AsyncClient = SuppliedClient
'''
wrap='''
# Supplied invocation bridge; no endpoint wiring is required from the learner.
@app.get("/fixture")
async def run_fixture():
    events.clear()
    await orders()
    return events
'''
ex('integration.async_http_requests',sc+'async def orders():\n    pass\n'+wrap,sc+'''async def orders():
    async with httpx.AsyncClient() as client:
        await client.get(lookup_one)
        await client.get(lookup_two)
'''+wrap,'Complete orders(): create one AsyncClient owning scope, await the lookup_one and lookup_two requests sequentially on that same client, then close it after both uses. Leave the supplied MockTransport/invocation bridge unchanged: it records real awaited requests without any network access. /fixture must report one opening, both requests in order, then closure.',[ht('GET','/fixture')],packages=['httpx','fastapi'])
sc=A['ws.pydantic.domain_validation']['files'][0]['content']
bridge='''
# Supplied constructor inspector returns validation outcome and accepted field values.
def booking_case(start, end):
    try:
        b = Booking(start=start, end=end)
        return {"accepted": True, "start": b.start, "end": b.end}
    except ValidationError:
        return {"accepted": False}
'''
ex('pydantic.domain_validation',sc+bridge,sc+'''    @model_validator(mode="after")
    def validate_order(self):
        if self.end <= self.start:
            raise ValueError("end must be later than start")
        return self
'''+bridge,'Add Booking.validate_order as an after-model instance validator. Require end > start, raise ValueError on failure, and return self on success. Constructor checks include (5,3), (3,3), (3,5) and (2,7); reject the first two and preserve the accepted integer fields.',[ft('booking_case',5,3),ft('booking_case',3,3),ft('booking_case',3,5),ft('booking_case',2,7)],packages=['pydantic'])
sc='''from fastapi import FastAPI, HTTPException
app = FastAPI()
order = None
missing_detail = "Order not found"
'''
ex('fastapi.expected_http_errors',sc+'''@app.get("/order")
def get_order():
    if order is None:
        pass
    return order
''',sc+'''@app.get("/order")
def get_order():
    if order is None:
        raise HTTPException(status_code=404, detail=missing_detail)
    return order
''','Complete the absent-order branch with a raised HTTPException: status 404 and the supplied missing_detail. Do not return the exception or proceed to the normal return in that branch. The /order rejection must carry {"detail": missing_detail}.',[ht('GET','/order')],packages=['fastapi'])
# No claim of measured native thread execution: Pyodide runs sync handlers inline.
sc='''from fastapi import FastAPI
import inspect
app = FastAPI()
shipping_result = "synthetic-shipping-result"
class SuppliedBlockingClient:
    # Native-library stand-in: this snapshot returns immediately; no timing inference.
    def lookup(self): return {"status": shipping_result}
shipping_client = SuppliedBlockingClient()
def shipping_utility(): return shipping_client.lookup()
'''
bridge='''
# Supplied declaration inspector; native thread placement is not measured here.
def inspect_shipping(view):
    if view == "declaration":
        return {"async": inspect.iscoroutinefunction(shipping), "doc": shipping.__doc__}
    return {"async": inspect.iscoroutinefunction(shipping_utility), "result": shipping_utility()}
'''
ex('fastapi.handler_execution_choice',sc+'@app.get("/shipping")\nasync def shipping():\n    return shipping_utility()\n'+bridge,sc+'''@app.get("/shipping")
def shipping():
    """Native FastAPI: handler and direct utility execute in the external thread pool."""
    return shipping_utility()
'''+bridge,'Change shipping to normal def for the supplied blocking-library call and return shipping_utility() without await. Add this exact explanatory docstring: "Native FastAPI: handler and direct utility execute in the external thread pool." Tests check the declaration, direct utility result and /shipping output. The pinned WASM runner executes sync endpoints inline: native thread-pool placement is inferred from the taught declaration rule, not measured in this run.',[ht('GET','/shipping'),ft('inspect_shipping','declaration'),ft('inspect_shipping','utility')],packages=['fastapi'])
sc='''from fastapi import FastAPI, APIRouter
# Supplied feature-module boundary; the sandbox assembles it in one entry file.
app = FastAPI()
orders_result = "synthetic-orders"
'''
ex('fastapi.modular_application',sc+'''router = APIRouter()
def list_orders(): return orders_result
# TODO: register on router, then include it with /api.
''',sc+'''router = APIRouter()
@router.get("/orders")
def list_orders(): return orders_result
app.include_router(router, prefix="/api")
''','Complete feature-router registration and application inclusion: create router, register GET /orders on it, and include it on app with prefix /api. The supplied entry combines the feature and application sections so no filesystem imports are required. Preserve list_orders and its supplied static result. GET /api/orders must reach the feature; local /orders must not be exposed on app.',[ht('GET','/api/orders'),ft('router_paths','feature'),ft('router_paths','application')],packages=['fastapi'])
# Add supplied boundary inspector to both files.
a=list(EX['fastapi.modular_application']); helper='''
def router_paths(scope):
    routes = router.routes if scope == "feature" else app.routes
    return [r.path for r in routes if "orders" in r.path]
''';a[0]+=helper;a[1]+=helper;EX['fastapi.modular_application']=tuple(a)
sc='from fastapi import FastAPI\napp = FastAPI()\n'
ex('fastapi.path_query_binding',sc+'@app.get("/orders/{order_id}")\ndef read_order(): return {}\n',sc+'@app.get("/orders/{order_id}")\ndef read_order(order_id: int, limit: int = 10):\n    return {"order_id": order_id, "limit": limit}\n','Bind the order_id path placeholder to order_id: int; declare limit: int = 10 as a query input absent from the path. Return exactly {"order_id": order_id, "limit": limit}. Tests cover /orders/42 without limit and /orders/7?limit=3.',[ht('GET','/orders/42'),ht('GET','/orders/7',params={'limit':3})],packages=['fastapi'])
row=dict(zip([c['name'] for c in A['ds.internal_orders']['columns']],A['ds.internal_orders']['rows'][0]))
sc='from fastapi import FastAPI\nfrom pydantic import BaseModel\napp = FastAPI()\norder_status = '+repr(row['status'])+'\nprivate_note = '+repr(row['private_processing_note'])+'\ninternal_order = {"order_id": '+str(row['order_id'])+', "status": order_status, "private_processing_note": private_note}\n'
ex('fastapi.response_model_serialization',sc+'@app.get("/orders/{order_id}")\ndef read_order(order_id: int): return internal_order\n',sc+'''class PublicOrder(BaseModel):
    order_id: int
    status: str
@app.get("/orders/{order_id}", response_model=PublicOrder)
def read_order(order_id: int):
    return internal_order
''','Define PublicOrder with order_id: int and status: str only. Set response_model=PublicOrder on GET /orders/{order_id}; return the supplied internal_order dictionary normally, not a direct Response. The public JSON must contain exactly order_id and status and exclude private_processing_note for both fixture requests.',[ht('GET','/orders/42'),ht('GET','/orders/7')],packages=['fastapi','pydantic'])
sc='''from typing import Annotated
from fastapi import FastAPI, Depends
app = FastAPI()
provided_context = "synthetic-auth-context-not-verified"
def provider() -> str: return provided_context
'''
ex('fastapi_backend.depends',sc+'@app.get("/orders")\ndef orders(): return {}\n',sc+'@app.get("/orders")\ndef orders(context: Annotated[str, Depends(provider)]):\n    return context\n','Wire orders(context: Annotated[str, Depends(provider)]) and return context exactly. Pass provider, not provider(); do not call the provider inside the handler or return a global value. This is demonstration input provisioning, not credential verification.',[ht('GET','/orders')],packages=['fastapi'])
state={r[0]:{'order_id':r[0],'quantity':r[1]} for r in A['ds.order_state']['rows']}
sc='''from fastapi import FastAPI, Depends
app = FastAPI()
order_state = '''+repr(state)+'''
class OrderStateAdapter:
    def quantity(self, order_id: int) -> int:
        return order_state[order_id]["quantity"]
adapter = OrderStateAdapter()
def requested_quantity(quantity: int) -> int: return quantity
'''
ex('design.backend_separation_of_concerns',sc+'''@app.get("/orders/{order_id}")
def decide_order(order_id: int, quantity: int):
    return quantity <= order_state[order_id]["quantity"]
''',sc+'''def can_accept(requested: int, stored: int) -> bool:
    return requested <= stored
@app.get("/orders/{order_id}")
def decide_order(order_id: int, quantity: int = Depends(requested_quantity)):
    stored = adapter.quantity(order_id)
    return can_accept(quantity, stored)
''','Refactor without changing the supplied quantity rule: define plain can_accept(requested: int, stored: int) -> bool using requested <= stored. Keep stored-state access solely in the supplied adapter. The endpoint receives quantity via Depends(requested_quantity), obtains stored quantity from adapter.quantity(order_id), calls can_accept, and returns its bool. Direct business calls and requests must preserve the rule.',[ft('can_accept',2,5),ft('can_accept',6,5),ht('GET','/orders/42',params={'quantity':2}),ht('GET','/orders/42',params={'quantity':6})],packages=['fastapi'])
sc='''from fastapi import FastAPI, BackgroundTasks
app = FastAPI()
order_id = "42"
follow_ups = []
def order_follow_up(order_id: str): follow_ups.append(order_id)
'''
helper='''
# Supplied deferred-registration inspector; it calls the handler, not a server.
def inspect_follow_up(identifier):
    global order_id
    order_id = identifier
    follow_ups.clear()
    tasks = BackgroundTasks()
    response = create_order(tasks)
    return {"response": response, "called_immediately": list(follow_ups), "registered": [[t.func.__name__, list(t.args)] for t in tasks.tasks], "placement": create_order.__doc__}
'''
ex('fastapi.bounded_background_tasks',sc+'@app.post("/orders")\ndef create_order(background_tasks: BackgroundTasks):\n    return {"order_id": order_id}\n'+helper,sc+'''@app.post("/orders")
def create_order(background_tasks: BackgroundTasks):
    """Optional process-local follow-up; this is not guaranteed completion."""
    background_tasks.add_task(order_follow_up, order_id)
    return {"order_id": order_id}
'''+helper,'Register the supplied optional order_follow_up callable with background_tasks.add_task(order_follow_up, order_id), not an immediate call, before returning {"order_id": order_id}. Declare background_tasks: BackgroundTasks. Add the exact docstring "Optional process-local follow-up; this is not guaranteed completion." The inspector checks registration before response sending with identifiers 42 and 7; this task may be lost on process failure.',[ft('inspect_follow_up','42'),ft('inspect_follow_up','7')],packages=['fastapi'])
sc='from typing import Annotated\nfrom fastapi import FastAPI, Depends\napp = FastAPI()\n'
ex('fastapi.dependency_composition',sc+'''def pagination(): return {}
def order_options(): return {}
@app.get("/orders")
def orders(): return {}
''',sc+'''def pagination(page: int, page_size: int) -> dict[str, int]:
    return {"page": page, "page_size": page_size}
def order_options(pagination: Annotated[dict[str, int], Depends(pagination)]) -> dict[str, int]:
    return pagination
@app.get("/orders")
def orders(options: Annotated[dict[str, int], Depends(order_options)]):
    return options
''','Complete pagination(page: int, page_size: int) to return those two keys. Make order_options receive that dictionary through Annotated[..., Depends(pagination)] and return it. Make orders receive order_options through a declared dependency and return it. /orders?page=2&page_size=10 and page=3&page_size=5 must return exactly the typed query values; prerequisites resolve before consumers.',[ht('GET','/orders',params={'page':2,'page_size':10}),ht('GET','/orders',params={'page':3,'page_size':5})],packages=['fastapi'])
opts=json.loads(next(f['content'] for f in A['ws.fastapi.existing_middleware_stack']['files'] if f['path']=='middleware_options.json'))
sc='''from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware as A
from starlette.middleware.trustedhost import TrustedHostMiddleware as B
app = FastAPI()
minimum_size = '''+repr(opts['A']['documented_options']['minimum_size'])+'''
allowed_host = '''+repr(opts['B']['documented_options']['allowed_hosts'][0])+'''
@app.get("/orders")
def orders(): return []
'''
helper='''
# Supplied inspection of configuration and source annotations, not a custom middleware.
def middleware_inspection(index):
    import pathlib
    source = pathlib.Path("main.py").read_text()
    wrappers = app.user_middleware
    component = wrappers[index]
    return {"class": component.cls.__name__, "options": component.kwargs, "request_annotation": "# Request: B -> A -> handler" in source, "response_annotation": "# Response: handler -> A -> B" in source}
'''
ex('fastapi.existing_middleware_stack',sc+'# TODO: add supplied A then B and annotate traversal.\n'+helper,sc+'''app.add_middleware(A, minimum_size=minimum_size)
app.add_middleware(B, allowed_hosts=[allowed_host])
# Request: B -> A -> handler
# Response: handler -> A -> B
'''+helper,'Configure maintained A first with minimum_size=minimum_size and B second with allowed_hosts=[allowed_host], using app.add_middleware. B is outermost. Add exact comments "# Request: B -> A -> handler" and "# Response: handler -> A -> B". Tests inspect both wrapper configurations and annotations; do not implement middleware.',[ft('middleware_inspection',0),ft('middleware_inspection',1)],packages=['fastapi','starlette'])
# Assemble interaction metadata exclusively from plan and glossary anchors.
out={k:P[k] for k in ['schema_version','path_id','batch_id']};out['kind']='interactions_part';out['tiles']=[]
for t in P['tiles']:
 tile={'tile_id':t['tile_id'],'interactions':[]};seen=set();rem=next(x for x in S['tiles'] if x['tile_id']==t['tile_id']).get('remediation_steps',[])
 for s in t['steps']:
  if s['type'] not in ['check','hands_on']:continue
  c=s['concept_ids'][0];facts={f['id']:f['statement'] for f in G[c]['coverage']['required_facts']}; measures=[]
  for anchor in s['anchors']:
   if '#assessment:' in anchor:
    capability=anchor.split('#assessment:')[1];a=next(a for a in G[c]['assessment_anchors'] if a['capability']==capability);measures.append({'concept_id':c,'capability':capability,'fact_ids':a['fact_ids']})
  feedback={'correct':'Correct. '+(facts[s['fact_ids'][0].split('#')[1]] if s['fact_ids'] else G[c]['practice_anchor']['success']),'incorrect':'Recheck the distinction: '+(facts[s['fact_ids'][0].split('#')[1]] if s['fact_ids'] else G[c]['practice_anchor']['success']),'hints':['Identify the relevant boundary before choosing an implementation.']}
  if c not in seen:
   rs=next((r for r in rem if c in r['concept_ids']),None)
   if rs:feedback['remediation_step_id']=rs['step_id']
   seen.add(c)
  ix={'interaction_id':'ix.'+s['step_id'],'type':s['planned_interaction_type'],'difficulty':'stretch' if s['type']=='hands_on' else ('intro' if len(tile['interactions'])==0 else 'core'),'grading_mode':'client','standalone':s['type']=='check','measures':measures,'anchors':s['anchors'],'feedback':feedback}
  if ix['type']=='choice':
   p,correct,w1,why1,w2,why2=choices[s['step_id']];ix['public']={'prompt':p,'options':[{'option_id':oid,'text':txt} for oid,txt in [('a',correct),('b',w1),('c',w2)]],'selection':'single','shuffle':True};ix['grading']={'correct_option_ids':['a'],'option_feedback':{'a':{'message':feedback['correct']},'b':{'message':why1},'c':{'message':why2}}}
  elif ix['type']=='code_exercise':
   starter,solution,prompt,tests,kind,packages=EX[c];live=G[c]['practice_anchor']['live_code'];ix['public']={'prompt':prompt,'runtime':{'kind':kind,'version':PIN[kind]['version'],'packages':packages},'workspace':{'entry':'main.py','files':[{'path':'main.py','role':'editable','content':starter}],'asset_mounts':[]},'constraints':{k:live[k] for k in ['allowed_syntax','blocked_syntax']}};ix['grading']={'solution_files':[{'path':'main.py','content':solution}],'tests':[]}
   for i,(kind,spec) in enumerate(tests):ix['grading']['tests'].append({'test_id':'t'+str(i+1),'kind':kind,'spec':copy.deepcopy(spec),'message_on_fail':'The completed implementation does not meet this observable contract.','visible':True})
  else:
   if c=='integration.outbound_timeouts':
    items=[('a','async with httpx.AsyncClient(timeout=2) as client:\n    try:\n        await client.get(shipping_url)\n    except httpx.ReadTimeout:\n        return "shipping-read-timeout"\nEvidence: connection succeeds, no response chunk arrives before the read limit, and the function returns shipping-read-timeout.','bounded'),('b','async with httpx.AsyncClient(timeout=None) as client:\n    await client.get(shipping_url)\nEvidence: the upstream accepts the connection but never supplies a response chunk; no timeout outcome is returned.','unbounded'),('c','async with httpx.AsyncClient(timeout=2) as client:\n    try:\n        await client.get(shipping_url)\n    except httpx.ConnectTimeout:\n        return "shipping-timeout"\nEvidence: connection succeeds, the response chunk stalls, and an unhandled ReadTimeout escapes.','wrong_outcome')];buckets=[('bounded','Finite wait limit and handled read-timeout outcome'),('unbounded','Timeout enforcement disabled'),('wrong_outcome','Finite wait limit but wrong exception handled')];prompt='Inspect the shipping lookup excerpts and their supplied stalled-upstream evidence. Classify whether each bounds the read wait and returns a distinct handled timeout outcome. This is inspect-and-judge, not executable network practice; a read limit is not a total elapsed deadline.'
   else:
    base='uvicorn main:app --host 0.0.0.0 --port 8000';items=[('a',base+'\nSupplied startup output: application startup complete; serving on http://0.0.0.0:8000. No reload is enabled.','ready'),('b',base+' --reload\nSupplied startup output: reloader process started; serving on http://0.0.0.0:8000.','reload'),('c','uvicorn main:missing --host 0.0.0.0 --port 8000\nSupplied output: attribute missing not found in module main; application did not start.','failed')];buckets=[('ready','Specified application starts without reload'),('reload','Starts with development-only reload'),('failed','Specified application was not imported or started')];prompt='The supplied module main.py defines app; the serving contract is host 0.0.0.0 and port 8000 without reload. Inspect each command AND its startup excerpt. Classify whether it demonstrates that contract. These excerpts are authored inspection fixtures, not verified native process execution.'
   ix['public']={'prompt':prompt,'buckets':[{'bucket_id':k,'label':l} for k,l in buckets],'items':[{'item_id':k,'text':text} for k,text,role in items]};ix['grading']={'assignments':{k:role for k,text,role in items},'role_map':{k:l for k,l in buckets},'item_feedback':{k:{'message':dict(buckets)[role]+'. '+facts[s['fact_ids'][0].split('#')[1]] if s['fact_ids'] else G[c]['practice_anchor']['success']} for k,text,role in items}}
  tile['interactions'].append({'step_id':s['step_id'],'interaction':ix})
 out['tiles'].append(tile)
(B/'interactions.json').write_text(json.dumps(out,indent=2)+'\n')
print('Wrote',sum(len(t['interactions']) for t in out['tiles']),'interactions')
