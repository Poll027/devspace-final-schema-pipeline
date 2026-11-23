# EVALUATOR PACKET — Binding request bodies to typed models (tile_039)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.request_body_binding — Binding request bodies to typed models

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: remediation step tile_039.r02 is never referenced

## SOURCE FACTS — A (fastapi.request_body_binding)   objective: Declare JSON bodies: add one typed create body.
A.f1: Define a BaseModel subclass and annotate a handler parameter with that model to bind a structured JSON request body.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/body/#create-your-data-model, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/body/#declare-it-as-a-parameter]
A.f2: FastAPI reads the JSON body, converts compatible values, validates the declared model and passes the model instance to the handler.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/body/#results]
A.f3: Path-declared parameters bind from the path, scalar parameters generally bind from the query, and model parameters bind from the body, so these inputs can coexist in one operation.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/body/#request-body-path-query-parameters]
note: Establish this first: Structured bodies are distinct from URL inputs.
note: Stay within the current objective: Declare JSON bodies. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine body binding.
PRACTICE ANCHOR (live_code): Add a body parameter annotated with OrderInput to the supplied order-creation handler, preserving its existing customer identifier and scalar query option.  SUCCESS: The handler declares one structured body using OrderInput. The customer identifier remains bound from the path, and the ordinary scalar option remains bound from the query.
ASSESSMENT ANCHOR: determine_body_path_and_query_binding facts=['f1', 'f3']
ASSESSMENT ANCHOR: trace_json_body_to_validated_model_instance facts=['f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Backward-compatible REST contract changes; Bearer-token extraction into an authentication dependency; Bounded form and multipart file inputs; CORS origin and credential policy; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Credential and sensitive-data redaction from emitted logs; Distinct create and partial-update contracts; Endpoint integration tests using TestClient or async HTTPX as appropriate; FastAPI OpenAPI generation from typed route contracts; Graceful termination and shutdown verification; Header and cookie input binding; Meaningful contract examples and operation metadata; Preventing unsafe outbound requests and SSRF; Redis cache-aside selection and population; Request-scoped async-compatible PostgreSQL session lifecycle; Request-scoped dependency reuse and lifetime; Request-validation error behavior; Required, optional and default input semantics; Retrieve resource; Service health and readiness checks; Structured service request and error logs; Test dependency replacement; Transaction commit and rollback boundaries; Trusted host validation; Yield-based dependency cleanup

## LESSON, in learner order

### s01 · explainer · Declare the boundary: Binding request bodies to typed models
Explainer — 
(mechanism) Structured JSON bodies are distinct from URL inputs: path-declared parameters come from the path, ordinary scalars generally come from the query, and model parameters come from the body. One operation can receive all three. ⟦A.f3 A:tb3⟧
(mechanism) Bind structured JSON by defining a BaseModel subclass and typing a handler parameter with that model. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) FastAPI reads JSON, converts compatible values, validates the declared model, then gives the handler a model instance. ⟦A.f2 A:tb3⟧
[CODE python]
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
class OrderInput(BaseModel):
    quantity: int
@app.post('/customers/{customer_id}/orders')
def create_order(customer_id: int, body: OrderInput, option: str = 'standard'):
    return {'customer_id': customer_id, 'option': option}

  annotations: ['BaseModel describes the structured body.', 'customer_id: path; option: generally query; body: JSON model.']

### s02 · explainer · Trace the contract
Explainer — 
(mental_model) Read the signature as a source map: the customer identifier is path input, an ordinary scalar option generally comes from the query, and OrderInput is structured body input. For the body, trace JSON reading, compatible conversion, model validation and delivery of the model instance. A body field is not an assumed query parameter. ⟦A.f1 A.f2 A.f3 A:tb4⟧

### s03 · explainer · Work through the supplied example
Explainer — 
(walkthrough) OrderInput declares the body’s shape. Add a body parameter typed with it while keeping the path identifier and ordinary scalar option. Trace JSON to compatible conversion to validation to the model supplied to the handler. A combined operation can receive these inputs together; the model declaration identifies the structured body rather than scattering its fields into assumed query inputs. ⟦A.f1 A.f2 A.f3 A:tb5 A:tb6⟧

### s04 · check · Check the boundary: Binding request bodies to typed models
Check — Use the supplied order-service scenario to reason about this contract.
QUESTION [choice, intro, grading=client] For a handler parameter annotated with OrderInput, which sequence describes FastAPI handling a compatible JSON body?
  ✔ option_1: Read JSON, convert compatible values, validate OrderInput, and supply a model instance.
      why: This is the declared-model body flow.
  ✘ option_2: Pass the raw JSON text to the handler without model validation.
      why: The model declaration causes JSON reading, compatible conversion and validation; the handler receives its instance.
  ✘ option_3: Bind each JSON body field as an ordinary query parameter.
      why: A model parameter is body input, not a set of assumed query parameters.
  feedback✔: This is the declared-model body flow.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Separate the stated requirement from a nearby but different boundary.']  remediation→r01
  MEASURES: A:trace_json_body_to_validated_model_instance(f2)   anchors=['assessment:trace_json_body_to_validated_model_instance']
  taught-before-tested: A.f2←s01

### s05 · hands_on · Apply the contract: Binding request bodies to typed models
Hands On — Complete the supplied workspace within its stated contract.
QUESTION [code_exercise, stretch, grading=client] Add body: OrderInput to create_order. Keep customer_id as the integer path input and option as the scalar query input with its existing default. Do not change the supplied model or response. The harness inspects binding declarations and submits two different JSON bodies.
  runtime={'kind': 'python_asgi', 'version': '0.29.5'} constraints.allowed=['from fastapi import FastAPI', 'from pydantic import BaseModel', 'class OrderInput(BaseModel):', 'model field annotations using str and int', 'def handler declarations', 'FastAPI path-operation decorators', 'handler parameter annotations', 'body: OrderInput', 'model attribute access', 'return statements', 'dictionary literals', 'string and integer literals'] blocked=10 items
  file exercise.py [editable]:
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
class OrderInput(BaseModel):
    quantity: int
@app.post('/customers/{customer_id}/orders')
def create_order(customer_id: int, option: str = 'standard'):
    # TODO: declare body: OrderInput, preserving path and query inputs.
    return {'customer_id': customer_id, 'option': option}
import asyncio, inspect, json, ast
import httpx
from contextlib import contextmanager

def _drive(coro):
    try:
        pending = coro.send(None)
    except StopIteration as done:
        return done.value
    raise RuntimeError('Harness encountered a suspending operation: ' + repr(pending))

async def _requests(application, requests):
    async with application.router.lifespan_context(application):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application, raise_app_exceptions=False), base_url='http://testserver') as client:
            out=[]
            for method,path,kwargs in requests:
                response=await client.request(method,path,**kwargs)
                try: body=response.json()
                except ValueError: body=response.text
                out.append({'status':response.status_code,'body':body})
            return out
def _case(which):
    customer,option,quantity=(7,'priority',3) if which=='A' else (9,'standard',5)
    parameters=inspect.signature(create_order).parameters
    assert parameters['body'].annotation is OrderInput
    assert parameters['customer_id'].annotation is int
    assert parameters['option'].annotation is str
    assert parameters['option'].default=='standard'
    return _drive(_requests(app,[('POST','/customers/'+str(customer)+'/orders',{'params':{'option':option},'json':{'quantity':quantity}})]))
import inspect
from fastapi import FastAPI, Body
verification_app=FastAPI()

async def verify_case(payload: dict=Body(...)):
    result=_case(payload['case'])
    if inspect.isawaitable(result):return await result
    return result
verify_case = verification_app.post('/_verify')(verify_case)

  SOLUTION exercise.py:
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
class OrderInput(BaseModel):
    quantity: int
@app.post('/customers/{customer_id}/orders')
def create_order(customer_id: int, body: OrderInput, option: str = 'standard'):
    # TODO: declare body: OrderInput, preserving path and query inputs.
    return {'customer_id': customer_id, 'option': option}
import asyncio, inspect, json, ast
import httpx
from contextlib import contextmanager

def _drive(coro):
    try:
        pending = coro.send(None)
    except StopIteration as done:
        return done.value
    raise RuntimeError('Harness encountered a suspending operation: ' + repr(pending))

async def _requests(application, requests):
    async with application.router.lifespan_context(application):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application, raise_app_exceptions=False), base_url='http://testserver') as client:
            out=[]
            for method,path,kwargs in requests:
                response=await client.request(method,path,**kwargs)
                try: body=response.json()
                except ValueError: body=response.text
                out.append({'status':response.status_code,'body':body})
            return out
def _case(which):
    customer,option,quantity=(7,'priority',3) if which=='A' else (9,'standard',5)
    parameters=inspect.signature(create_order).parameters
    assert parameters['body'].annotation is OrderInput
    assert parameters['customer_id'].annotation is int
    assert parameters['option'].annotation is str
    assert parameters['option'].default=='standard'
    return _drive(_requests(app,[('POST','/customers/'+str(customer)+'/orders',{'params':{'option':option},'json':{'quantity':quantity}})]))
import inspect
from fastapi import FastAPI, Body
verification_app=FastAPI()

async def verify_case(payload: dict=Body(...)):
    result=_case(payload['case'])
    if inspect.isawaitable(result):return await result
    return result
verify_case = verification_app.post('/_verify')(verify_case)

  test test_1 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"A"}}],"app":"verification_app","expected":{"status":200,"json":[{"status":200,"body":{"customer_id":7,"option":"priority"}}]}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  test test_2 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"B"}}],"app":"verification_app","expected":{"status":200,"json":[{"status":200,"body":{"customer_id":9,"option":"standard"}}]}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"4daf877da491a21a5f3af4a02a9e53176cf34ec51fe87c9ff932950ef1b557e5","tests_passed":2}
  feedback✔: You applied the declared boundary and preserved its required behavior.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Compare each declaration with its input or lifecycle boundary.', 'Trace what happens on the alternative input or exit, not only the successful path.']
  MEASURES: A:determine_body_path_and_query_binding(f1,f3)   anchors=['practice', 'assessment:determine_body_path_and_query_binding']
  taught-before-tested: A.f1←s01; A.f3←s01

### s06 · recap · Keep these distinctions
Recap — 
(takeaway) Type a model parameter for JSON; trace conversion and validation; distinguish path, ordinary query and body inputs. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
[UP NEXT] Next: tile_040 — Yield-based dependency cleanup: Start with Yield-based dependency cleanup.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Binding request bodies to typed models
(definition) FastAPI reads JSON, converts compatible values, validates the declared model, then gives the handler a model instance. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(example) For OrderInput, the handler receives a model after compatible conversion and validation, not merely an assumed-valid JSON body. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast: Binding request bodies to typed models
(definition) Bind structured JSON by defining a BaseModel subclass and typing a handler parameter with that model. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Path-declared parameters come from the path; ordinary scalars generally come from the query; model parameters come from the body. One operation can receive all three. ⟦A.f3 A:tb3 A:tb4 A:tb5 A:tb6⟧
(example) For the order handler, a body typed as OrderInput is structured JSON input, not an ordinary scalar query option. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: model_dump(exclude_unset=True)

=========

# EVALUATOR PACKET — Yield-based dependency cleanup (tile_040)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.yield_dependencies — Yield-based dependency cleanup

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: remediation step tile_040.r02 is never referenced
  warn: plan: tile_040.s04 was planned to measure fastapi.yield_dependencies#assessment:distinguish_request_and_function_cleanup_boundaries but its interaction does not

## SOURCE FACTS — A (fastapi.yield_dependencies)   objective: Release yield dependency resources: provide and close one request resource.
A.f1: A dependency with yield acquires a resource before yielding it and supplies that yielded value to the operation.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#a-database-dependency-with-yield]
A.f2: Put resource release in a finally block surrounding yield so exit cleanup runs after successful use or an exception.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#a-dependency-with-yield-and-try]
A.f3: A yielding dependency defaults to request scope, ending after the response is sent; Depends(provider, scope="function") ends it after the handler finishes but before sending the response.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#early-exit-and-scope]
A.f4: If a yielding dependency catches an exception without intentionally handling it, re-raise it rather than silently concealing the failure from FastAPI.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#always-raise-in-dependencies-with-yield-and-except]
note: Establish this first: Yield encloses execution in a resource boundary.
note: Stay within the current objective: Release yield dependency resources. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine cleanup after success and failure.
PRACTICE ANCHOR (live_code): Implement a yielding provider that supplies one resource to an operation and closes it in finally. Compare default request scope with explicit function scope, and preserve any unhandled exception.  SUCCESS: The operation receives the yielded resource. Release runs on both successful and exceptional exits. Default request-scope cleanup occurs after response sending; function-scope cleanup occurs after handler completion but before response sending. Any caught, unhandled exception is re-raised.
ASSESSMENT ANCHOR: determine_resource_cleanup_after_success_and_failure facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_request_and_function_cleanup_boundaries facts=['f3']
ASSESSMENT ANCHOR: preserve_cleanup_and_exception_visibility facts=['f2', 'f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Bearer-token extraction into an authentication dependency; Bounded form and multipart file inputs; CORS origin and credential policy; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Credential and sensitive-data redaction from emitted logs; Distinct create and partial-update contracts; Endpoint integration tests using TestClient or async HTTPX as appropriate; FastAPI OpenAPI generation from typed route contracts; Graceful termination and shutdown verification; Header and cookie input binding; Meaningful contract examples and operation metadata; Preventing unsafe outbound requests and SSRF; Redis cache-aside selection and population; Request-scoped async-compatible PostgreSQL session lifecycle; Request-scoped dependency reuse and lifetime; Request-validation error behavior; Required, optional and default input semantics; Retrieve resource; Service health and readiness checks; Structured service request and error logs; Test dependency replacement; Transaction commit and rollback boundaries; T

## LESSON, in learner order

### s01 · explainer · Declare the boundary: Yield-based dependency cleanup
Explainer — 
(mechanism) Acquire the resource before yield. The dependency supplies the yielded resource to the operation. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) Surround yield with try/finally and release the resource in finally, covering successful use and exceptions. ⟦A.f2 A:tb3⟧
(mechanism) Default request scope ends after response sending. Depends(provider, scope="function") ends after handler completion, before the response is sent. ⟦A.f3 A:tb3⟧
(mechanism) If you catch an exception without intentionally handling it, re-raise it. Do not conceal the failure from FastAPI. ⟦A.f4 A:tb3⟧
[PROCESS_FLOW: Resource ownership and scope boundaries] nodes=['Acquire resource', 'Yield to operation', 'Operation uses resource', 'Handler completion', 'Declared scope', 'Function scope: finally releases resource', 'Send response', 'Default request scope: finally releases resource', 'Exceptional use', 'Re-raise unhandled exception', 'finally: release resource'] edges=[('acquire', 'yield', None), ('yield', 'use', None), ('use', 'done', 'success'), ('done', 'choice', None), ('choice', 'function', 'scope="function"'), ('function', 'response', None), ('choice', 'response', 'default request scope'), ('response', 'request', 'default only'), ('use', 'exception', 'failure'), ('exception', 'raise', 'not intentionally handled'), ('raise', 'finally', None)] alt: Resource ownership and scope boundaries: Acquire resource; Yield to operation; Operation uses resource; Handler completion; Declared scope; Function scope: finally releases resource; Send response; Default request scope: finally releases resource; Exceptional use; Re-raise unhandled exception; finally: release resource

### s02 · explainer · Trace the contract
Explainer — 
(mental_model) Trace acquisition, yield and operation use separately. Put release in finally so both successful and exceptional paths clean up. Default request scope ends after response sending; function scope ends after handler completion, before sending. If a caught exception was not intentionally handled, re-raise it. Yield is not a promise that every dependency ends at handler completion. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Check the boundary: Yield-based dependency cleanup
Check — Use the supplied order-service scenario to reason about this contract.
QUESTION [choice, intro, grading=client] Which pattern releases resources on both exits, preserves an unhandled caught exception, and correctly distinguishes cleanup scopes?
  ✔ option_1: Release in finally, re-raise the unhandled exception; default request scope cleans up after response sending, while function scope cleans up after handler completion but before sending.
      why: Finally releases on successful and exceptional exits; re-raising preserves the unhandled exception. Request scope cleans up after sending; function scope after handler completion but before sending.
  ✘ option_2: Release in finally, suppress the unhandled caught exception; default request scope cleans up after response sending, while function scope cleans up after handler completion but before sending.
      why: Suppressing the unhandled caught exception conceals it even though finally releases the resource.
  ✘ option_3: Release in finally, re-raise the unhandled exception; default request scope cleans up before response sending, while function scope cleans up after sending.
      why: The scope timings are reversed: default request cleanup follows response sending, while function cleanup follows handler completion and precedes sending.
  feedback✔: Finally releases on successful and exceptional exits; re-raising preserves the unhandled exception. Request scope cleans up after sending; function scope after handler completion but before sending.  feedback✘: Suppressing the unhandled caught exception conceals it even though finally releases the resource. The scope timings are reversed: default request cleanup follows response sending, while function cleanup follows handler completion and precedes sending.  hints: ['Separate the stated requirement from a nearby but different boundary.']  remediation→r01
  MEASURES: A:preserve_cleanup_and_exception_visibility(f2,f4); A:distinguish_request_and_function_cleanup_boundaries(f3)   anchors=['assessment:preserve_cleanup_and_exception_visibility', 'assessment:distinguish_request_and_function_cleanup_boundaries']
  taught-before-tested: A.f2←s01; A.f4←s01; A.f3←s01

### s04 · hands_on · Apply the contract: Yield-based dependency cleanup
Hands On — Complete the supplied workspace within its stated contract.
QUESTION [code_exercise, stretch, grading=client] Complete provider with try/finally around yield resource and resource.close() on exit. Do not catch and conceal exceptions. The supplied boundary harness verifies successful and exceptional exits and compares default request-scope release after response sending with function-scope release after handler completion but before sending. The pinned FastAPI lacks the scope keyword, so this comparison is an explicit supplied boundary model, not a claim that this older runtime supports Depends(provider, scope="function").
  runtime={'kind': 'python_asgi', 'version': '0.29.5'} constraints.allowed=['def provider():', 'resource = supplied acquisition callable', 'try:', 'yield resource', 'finally:', 'resource.close()', 'except Exception:', 'raise', 'Depends(provider)', 'Depends(provider, scope="function")', 'def operation(...):', 'return', 'raise HTTPException(status_code=..., detail=...)'] blocked=5 items
  file exercise.py [editable]:
events = []
class Resource:
    def __init__(self):
        self.closed = False
        events.append('acquire')
    def use(self):
        events.append('operation use')
    def close(self):
        self.closed = True
        events.append('cleanup')
def acquire_resource():
    return Resource()
from fastapi import FastAPI, Depends, HTTPException
app = FastAPI()
def provider():
    resource = acquire_resource()
    # TODO: yield resource inside try/finally; close on exit.
    raise NotImplementedError
@app.get('/orders')
def operation(fail: bool = False, resource=Depends(provider)):
    resource.use()
    if fail:
        raise HTTPException(status_code=400, detail='synthetic failure')
    return {'result': 'used'}
# Compare this declaration with Depends(provider, scope="function").
import asyncio, inspect, json, ast
import httpx
from contextlib import contextmanager

def _drive(coro):
    try:
        pending = coro.send(None)
    except StopIteration as done:
        return done.value
    raise RuntimeError('Harness encountered a suspending operation: ' + repr(pending))

async def _requests(application, requests):
    async with application.router.lifespan_context(application):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application, raise_app_exceptions=False), base_url='http://testserver') as client:
            out=[]
            for method,path,kwargs in requests:
                response=await client.request(method,path,**kwargs)
                try: body=response.json()
                except ValueError: body=response.text
                out.append({'status':response.status_code,'body':body})
            return out
def _case(which):
    fail=which=='exceptional'
    results=[]
    for scope in ('request','function'):
        events.clear()
        generator=provider()
        resource=next(generator)
        events.append('yield')
        failure=None
        try:
            operation(fail=fail,resource=resource)
            events.append('handler completion')
        except HTTPException as exc:
            failure=exc;events.append('exception')
        def finish():
            if failure is None:
                generator.close()
            else:
                try:generator.throw(failure)
                except HTTPException as caught:assert caught is failure
                else:raise AssertionError('unhandled exception concealed')
        if scope=='function':finish()
        events.append('response sending')
        if scope=='request':finish()
        assert resource.closed and events.count('cleanup')==1
        assert (events.index('cleanup')>events.index('response sending'))==(scope=='request')
        results.append({'scope':scope,'status':400 if fail else 200,'events':list(events)})
    return results
import inspect
from fastapi import FastAPI, Body
verification_app=FastAPI()

async def verify_case(payload: dict=Body(...)):
    result=_case(payload['case'])
    if inspect.isawaitable(result):return await result
    return result
verify_case = verification_app.post('/_verify')(verify_case)

  SOLUTION exercise.py:
events = []
class Resource:
    def __init__(self):
        self.closed = False
        events.append('acquire')
    def use(self):
        events.append('operation use')
    def close(self):
        self.closed = True
        events.append('cleanup')
def acquire_resource():
    return Resource()
from fastapi import FastAPI, Depends, HTTPException
app = FastAPI()
def provider():
    resource = acquire_resource()
    try:
        yield resource
    finally:
        resource.close()
@app.get('/orders')
def operation(fail: bool = False, resource=Depends(provider)):
    resource.use()
    if fail:
        raise HTTPException(status_code=400, detail='synthetic failure')
    return {'result': 'used'}
# Compare this declaration with Depends(provider, scope="function").
import asyncio, inspect, json, ast
import httpx
from contextlib import contextmanager

def _drive(coro):
    try:
        pending = coro.send(None)
    except StopIteration as done:
        return done.value
    raise RuntimeError('Harness encountered a suspending operation: ' + repr(pending))

async def _requests(application, requests):
    async with application.router.lifespan_context(application):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application, raise_app_exceptions=False), base_url='http://testserver') as client:
            out=[]
            for method,path,kwargs in requests:
                response=await client.request(method,path,**kwargs)
                try: body=response.json()
                except ValueError: body=response.text
                out.append({'status':response.status_code,'body':body})
            return out
def _case(which):
    fail=which=='exceptional'
    results=[]
    for scope in ('request','function'):
        events.clear()
        generator=provider()
        resource=next(generator)
        events.append('yield')
        failure=None
        try:
            operation(fail=fail,resource=resource)
            events.append('handler completion')
        except HTTPException as exc:
            failure=exc;events.append('exception')
        def finish():
            if failure is None:
                generator.close()
            else:
                try:generator.throw(failure)
                except HTTPException as caught:assert caught is failure
                else:raise AssertionError('unhandled exception concealed')
        if scope=='function':finish()
        events.append('response sending')
        if scope=='request':finish()
        assert resource.closed and events.count('cleanup')==1
        assert (events.index('cleanup')>events.index('response sending'))==(scope=='request')
        results.append({'scope':scope,'status':400 if fail else 200,'events':list(events)})
    return results
import inspect
from fastapi import FastAPI, Body
verification_app=FastAPI()

async def verify_case(payload: dict=Body(...)):
    result=_case(payload['case'])
    if inspect.isawaitable(result):return await result
    return result
verify_case = verification_app.post('/_verify')(verify_case)

  test test_1 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"normal"}}],"app":"verification_app","expected":{"status":200,"json":[{"scope":"request","status":200,"events":["acquire","yield","operation use","handler completion","response sending","cleanup"]},{"scope":"function","status":200,"events":["acquire","yield","operation use","handler completion","cleanup","response sending"]}]}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  test test_2 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"exceptional"}}],"app":"verification_app","expected":{"status":200,"json":[{"scope":"request","status":400,"events":["acquire","yield","operation use","exception","response sending","cleanup"]},{"scope":"function","status":400,"events":["acquire","yield","operation use","exception","cleanup","response sending"]}]}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"9b212c4bd70e717aee4c2120587fa08c2abca169db4a7c01c43ba108938dfcd2","tests_passed":2}
  feedback✔: You applied the declared boundary and preserved its required behavior.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Compare each declaration with its input or lifecycle boundary.', 'Trace what happens on the alternative input or exit, not only the successful path.']
  MEASURES: A:determine_resource_cleanup_after_success_and_failure(f1,f2); A:preserve_cleanup_and_exception_visibility(f2,f4)   anchors=['practice', 'assessment:determine_resource_cleanup_after_success_and_failure', 'assessment:preserve_cleanup_and_exception_visibility']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f2←s01; A.f4←s01

### s05 · recap · Keep these distinctions
Recap — 
(takeaway) Acquire before yield; release in finally; distinguish request and function scope; re-raise unhandled exceptions. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: tile_041 — Structured service request and error logs: Start with Structured service request and error logs.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Yield-based dependency cleanup
(definition) Surround yield with try/finally and release the resource in finally, covering successful use and exceptions. ⟦A.f2 A:tb3 A:tb4⟧
(definition) If you catch an exception without intentionally handling it, re-raise it. Do not conceal the failure from FastAPI. ⟦A.f4 A:tb3 A:tb4⟧
(example) For the supplied resource, cleanup on failure and failure visibility are separate: finally releases it, while re-raising an unhandled exception keeps the failure visible. ⟦A.f2 A.f4 A:tb3 A:tb4⟧
### r02 · Try the contrast: Yield-based dependency cleanup
(definition) Acquire the resource before yield. The dependency supplies the yielded resource to the operation. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Surround yield with try/finally and release the resource in finally, covering successful use and exceptions. ⟦A.f2 A:tb3 A:tb4⟧
(definition) Default request scope ends after response sending. Depends(provider, scope="function") ends after handler completion, before the response is sent. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(definition) If you catch an exception without intentionally handling it, re-raise it. Do not conceal the failure from FastAPI. ⟦A.f4 A:tb3 A:tb4⟧
(example) For the supplied resource, cleanup in finally covers failure too; cleanup only on the successful return branch does not. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: app.dependency_overrides[...]

=========

# EVALUATOR PACKET — Structured service request and error logs (tile_041)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = observability.structured_service_logs — Structured service request and error logs

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: remediation step tile_041.r02 is never referenced

## SOURCE FACTS — A (observability.structured_service_logs)   objective: Emit structured diagnostics: add structured logs for one failure.
A.f1: A useful event log records when and where an event happened, its type and severity, and enough context to interpret the event's outcome.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#event-attributes]
A.f2: For a failure, record consistently named fields for timestamp, application or code location, event type, severity, result status and reason rather than an unexplained free-text message.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#event-attributes]
A.f3: Emit logger.error(message, extra=event_fields) with the standard logging library to attach structured fields to the LogRecord, and configure the existing formatter or collection pipeline to preserve those field names; custom keys must not collide with reserved LogRecord attributes.   [sources: python_tutorial#https://docs.python.org/3/library/logging.html#logging.Logger.debug, owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#event-collection]
note: Establish this first: Logs are structured event records.
note: Stay within the current objective: Emit structured diagnostics. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify insufficient failure logs.
PRACTICE ANCHOR (live_code): Add structured logging for one synthetic order failure using consistently named event fields, and configure the supplied formatter to preserve those fields.  SUCCESS: The emitted failure record preserves timestamp, code location, event type, severity, result status and reason under consistent field names. The logging call uses extra=event_fields, and custom keys do not collide with reserved LogRecord attributes.
ASSESSMENT ANCHOR: identify_missing_failure_event_context facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_structured_field_emission_and_preservation_gaps facts=['f3']
ASSESSMENT ANCHOR: identify_reserved_log_record_attribute_collisions facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; Bounded form and multipart file inputs; CORS origin and credential policy; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Credential and sensitive-data redaction from emitted logs; Distinct create and partial-update contracts; Endpoint integration tests using TestClient or async HTTPX as appropriate; FastAPI OpenAPI generation from typed route contracts; Graceful termination and shutdown verification; Header and cookie input binding; Meaningful contract examples and operation metadata; Preventing unsafe outbound requests and SSRF; Redis cache-aside selection and population; Request-scoped async-compatible PostgreSQL session lifecycle; Request-scoped dependency reuse and lifetime; Request-validation error behavior; Required, optional and default input semantics; Retrieve resource; Service health and readiness checks; Test dependency replacement; Transaction commit and rollback bounda

## LESSON, in learner order

### s01 · explainer · Declare the boundary: Structured service request and error logs
Explainer — 
(mechanism) An interpretable event log says when and where an event happened, its type and severity, and enough context to understand the outcome. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) For a failure, use consistent field names for timestamp, application or code location, event type, severity, result status and reason—not just unexplained free text. ⟦A.f2 A:tb3⟧
(mechanism) logger.error(message, extra=event_fields) attaches fields to the LogRecord. Configure the existing formatter or collector to preserve their names, and avoid custom keys that collide with reserved LogRecord attributes. ⟦A.f3 A:tb3⟧
[BEFORE_AFTER] Before: unexplained message. After: preserve the six named failure fields through the existing formatter. Emitted output is computed, not an observed production event.
  before:
[CODE python]
import io
import logging
captured_output = io.StringIO()
logger = logging.getLogger('order.failure.exercise')
logger.handlers.clear()
logger.propagate = False
logger.setLevel(logging.ERROR)
existing_handler = logging.StreamHandler(captured_output)
existing_handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(existing_handler)
failure_values = {
    'timestamp': '2026-01-01T12:00:00Z',
    'code_location': 'orders.create_order',
    'event_type': 'order_failure',
    'event_severity': 'error',
    'result_status': 'failed',
    'reason': 'synthetic stock unavailable',
}
reserved_attributes = sorted(set(logging.makeLogRecord({}).__dict__) | {'message', 'asctime'})

logger.error('failed')
print(captured_output.getvalue(), end='')

  annotations: []
  after:
[CODE python]
import io
import logging
captured_output = io.StringIO()
logger = logging.getLogger('order.failure.exercise')
logger.handlers.clear()
logger.propagate = False
logger.setLevel(logging.ERROR)
existing_handler = logging.StreamHandler(captured_output)
existing_handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(existing_handler)
failure_values = {
    'timestamp': '2026-01-01T12:00:00Z',
    'code_location': 'orders.create_order',
    'event_type': 'order_failure',
    'event_severity': 'error',
    'result_status': 'failed',
    'reason': 'synthetic stock unavailable',
}
reserved_attributes = sorted(set(logging.makeLogRecord({}).__dict__) | {'message', 'asctime'})

event_fields = dict(failure_values)
existing_handler.setFormatter(logging.Formatter('timestamp=%(timestamp)s code_location=%(code_location)s event_type=%(event_type)s event_severity=%(event_severity)s result_status=%(result_status)s reason=%(reason)s'))
logger.error('order failure', extra=event_fields)
print(captured_output.getvalue(), end='')

  annotations: []

### s02 · explainer · Trace the contract
Explainer — 
(mental_model) Follow the fields from event_fields into the LogRecord and then into the emitted record. Use timestamp, code location, event type, severity, result status and reason consistently. Passing extra is not enough: inspect the existing formatter or collector to ensure those names survive. Custom names must not collide with reserved LogRecord attributes. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · check · Check the boundary: Structured service request and error logs
Check — Use the supplied order-service scenario to reason about this contract.
QUESTION [choice, intro, grading=client] When attaching custom structured fields using logger.error(message, extra=event_fields), which naming rule is required?
  ✔ option_1: Use consistent custom field names that do not collide with reserved LogRecord attributes.
      why: Structured extra fields must avoid reserved attribute collisions.
  ✘ option_2: Reuse reserved LogRecord attribute names for custom context.
      why: Custom keys must not collide with reserved LogRecord attributes.
  ✘ option_3: Put context only in free text so the formatter need not preserve field names.
      why: The structured-field goal requires attaching and preserving consistently named fields, not unexplained free text.
  feedback✔: Structured extra fields must avoid reserved attribute collisions.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Separate the stated requirement from a nearby but different boundary.']  remediation→r01
  MEASURES: A:identify_reserved_log_record_attribute_collisions(f3)   anchors=['assessment:identify_reserved_log_record_attribute_collisions']
  taught-before-tested: A.f3←s01

### s04 · hands_on · Apply the contract: Structured service request and error logs
Hands On — Complete the supplied workspace within its stated contract.
QUESTION [code_exercise, stretch, grading=client] event_fields is supplied with six consistently named failure fields. Configure the existing handler formatter to emit exactly timestamp=<value> code_location=<value> event_type=<value> event_severity=<value> result_status=<value> reason=<value>, in that order, followed by a newline. Emit logger.error('failed', extra=event_fields). Preserve all field names; use no reserved LogRecord names for custom fields.
  runtime={'kind': 'python_asgi', 'version': '0.29.5'} constraints.allowed=['import logging', 'logging.getLogger(...)', 'variable assignment', 'dictionary literals with string keys and string values', 'logger.error(message, extra=event_fields)', 'logging.Formatter(...)', 'existing_handler.setFormatter(...)', '%(field_name)s formatter placeholders'] blocked=4 items
  file exercise.py [editable]:
failure_reason = 'synthetic stock unavailable'
import io
import logging
captured_output = io.StringIO()
logger = logging.getLogger('order.failure.exercise')
logger.handlers.clear()
logger.propagate = False
logger.setLevel(logging.ERROR)
existing_handler = logging.StreamHandler(captured_output)
existing_handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(existing_handler)
failure_values = {
    'timestamp': '2026-01-01T12:00:00Z',
    'code_location': 'orders.create_order',
    'event_type': 'order_failure',
    'event_severity': 'error',
    'result_status': 'failed',
    'reason': failure_reason,
}
reserved_attributes = sorted(set(logging.makeLogRecord({}).__dict__) | {'message', 'asctime'})
import logging
# TODO: copy the six failure values into event_fields and preserve their
# names in the existing formatter. Emit logger.error(..., extra=event_fields).
event_fields = {
    'timestamp': failure_values['timestamp'],
    'code_location': failure_values['code_location'],
    'event_type': failure_values['event_type'],
    'event_severity': failure_values['event_severity'],
    'result_status': failure_values['result_status'],
    'reason': failure_values['reason'],
}
# TODO: configure the existing formatter and emit with extra=event_fields.
logger.error('failed')

  SOLUTION exercise.py:
failure_reason = 'synthetic stock unavailable'
import io
import logging
captured_output = io.StringIO()
logger = logging.getLogger('order.failure.exercise')
logger.handlers.clear()
logger.propagate = False
logger.setLevel(logging.ERROR)
existing_handler = logging.StreamHandler(captured_output)
existing_handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(existing_handler)
failure_values = {
    'timestamp': '2026-01-01T12:00:00Z',
    'code_location': 'orders.create_order',
    'event_type': 'order_failure',
    'event_severity': 'error',
    'result_status': 'failed',
    'reason': failure_reason,
}
reserved_attributes = sorted(set(logging.makeLogRecord({}).__dict__) | {'message', 'asctime'})
import logging
# TODO: copy the six failure values into event_fields and preserve their
# names in the existing formatter. Emit logger.error(..., extra=event_fields).
event_fields = {
    'timestamp': failure_values['timestamp'],
    'code_location': failure_values['code_location'],
    'event_type': failure_values['event_type'],
    'event_severity': failure_values['event_severity'],
    'result_status': failure_values['result_status'],
    'reason': failure_values['reason'],
}
existing_handler.setFormatter(logging.Formatter('timestamp=%(timestamp)s code_location=%(code_location)s event_type=%(event_type)s event_severity=%(event_severity)s result_status=%(result_status)s reason=%(reason)s'))
logger.error('failed', extra=event_fields)

  test test_1 (value_equals, visible=True): {"expr":"captured_output.getvalue()","expected":"timestamp=2026-01-01T12:00:00Z code_location=orders.create_order event_type=order_failure event_severity=error result_status=failed reason=synthetic stock unavailable\n"} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"d58a288e30cd623eac650bb537b661726d1b2f5f510c37c12d4e87fec93ac6b2","tests_passed":1}
  feedback✔: You applied the declared boundary and preserved its required behavior.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Follow each event_fields key into its matching formatter placeholder', 'Passing extra attaches fields; the formatter must also emit all six named fields.']
  MEASURES: A:identify_missing_failure_event_context(f1,f2); A:identify_structured_field_emission_and_preservation_gaps(f3); A:identify_reserved_log_record_attribute_collisions(f3)   anchors=['practice', 'assessment:identify_missing_failure_event_context', 'assessment:identify_structured_field_emission_and_preservation_gaps', 'assessment:identify_reserved_log_record_attribute_collisions']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f3←s01

### s05 · recap · Keep these distinctions
Recap — 
(takeaway) Name failure fields consistently, attach them with extra, avoid reserved names and preserve them in emitted output. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: tile_042 — Preventing unsafe outbound requests and SSRF: Start with Preventing unsafe outbound requests and SSRF.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Structured service request and error logs
(definition) logger.error(message, extra=event_fields) attaches fields to the LogRecord. Configure the existing formatter or collector to preserve their names, and avoid custom keys that collide with reserved LogRecord attributes. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) For the supplied order failure, attaching extra fields differs from preserving them in emitted output. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast: Structured service request and error logs
(definition) An interpretable event log says when and where an event happened, its type and severity, and enough context to understand the outcome. ⟦A.f1 A:tb2 A:tb4⟧
(definition) For a failure, use consistent field names for timestamp, application or code location, event type, severity, result status and reason—not just unexplained free text. ⟦A.f2 A:tb3 A:tb4⟧
(definition) logger.error(message, extra=event_fields) attaches fields to the LogRecord. Configure the existing formatter or collector to preserve their names, and avoid custom keys that collide with reserved LogRecord attributes. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) For the supplied order failure, attaching extra fields differs from preserving them in emitted output. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: app.dependency_overrides[...] = ...
· constraints.blocked_syntax: @app.exception_handler(...)
· spec.expected: timestamp=2026-01-01T12:00:00Z code_location=orders.create_order event_type=order_failure event_severity=error result_status=failed reason=synthetic stock unavailable

· ops.value: synthetic stock unavailable_x
· expected.value: timestamp=2026-01-01T12:00:00Z code_location=orders.create_order event_type=order_failure event_severity=error result_status=failed reason=synthetic stock unavailable_x


=========

# EVALUATOR PACKET — Preventing unsafe outbound requests and SSRF (tile_042)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = security.safe_outbound_requests — Preventing unsafe outbound requests and SSRF

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=3
  warn: remediation step tile_042.r02 is never referenced
  warn: remediation step tile_042.r03 is never referenced
  warn: plan: tile_042.s05 was planned to measure security.safe_outbound_requests#assessment:identify_redirect_destination_policy_bypasses but its interaction does not

## SOURCE FACTS — A (security.safe_outbound_requests)   objective: Constrain outbound destinations: implement one destination policy.
A.f1: When destinations are known, enforce a destination allowlist instead of allowing an untrusted value to choose an arbitrary outbound URL.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html#application-layer]
A.f2: A destination policy must reject private, loopback, link-local and other non-public addresses, including IPv6 equivalents, when access is intended only to public services.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html#case-2-application-can-send-requests-to-any-external-ip-address-or-domain-name]
A.f3: Validate the resolved address actually used for the connection, not merely a hostname checked earlier, to avoid a DNS rebinding gap.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html#ssrf-prevention-publisher-side]
A.f4: Disable automatic redirects or apply the same destination checks to each redirect target so a permitted initial URL cannot redirect into a forbidden destination.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html#application-layer, owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html#ssrf-prevention-publisher-side]
note: Establish this first: Untrusted input must not select privileged destinations.
note: Stay within the current objective: Constrain outbound destinations. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify SSRF network-trust violations.
PRACTICE ANCHOR (live_code): Implement a destination allowlist that maps a requested provider to a fixed, approved destination and rejects unknown providers instead of treating their input as an outbound URL.  SUCCESS: Known provider values return only their configured destinations. Unknown provider values, including arbitrary URL strings, are rejected. This implements destination selection, not the separate connected-address and redirect checks.
ASSESSMENT ANCHOR: identify_arbitrary_destination_selection facts=['f1']
ASSESSMENT ANCHOR: identify_non_public_address_boundary_violations facts=['f2']
ASSESSMENT ANCHOR: identify_dns_rebinding_validation_gaps facts=['f3']
ASSESSMENT ANCHOR: identify_redirect_destination_policy_bypasses facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; Bounded form and multipart file inputs; CORS origin and credential policy; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Credential and sensitive-data redaction from emitted logs; Distinct create and partial-update contracts; Endpoint integration tests using TestClient or async HTTPX as appropriate; FastAPI OpenAPI generation from typed route contracts; Graceful termination and shutdown verification; Header and cookie input binding; Keeping API schemas distinct from persistence entities; Meaningful contract examples and operation metadata; Redis cache-aside selection and population; Request-scoped async-compatible PostgreSQL session lifecycle; Request-scoped dependency reuse and lifetime; Request-validation error behavior; Required, optional and default input semantics; Retrieve resource; Service health and readiness checks; Test dependency replacement; Transaction commit and rollb

## LESSON, in learner order

### s01 · explainer · Declare the boundary: Preventing unsafe outbound requests and SSRF
Explainer — 
(mechanism) For known destinations, map untrusted provider input to an allowed destination instead of accepting an arbitrary outbound URL. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) For public-only access, reject private, loopback, link-local and other non-public addresses, including IPv6 equivalents. ⟦A.f2 A:tb3⟧
(mechanism) Validate the resolved address actually used for the connection. Checking a hostname earlier is insufficient against a DNS rebinding gap. ⟦A.f3 A:tb3⟧
(mechanism) Disable automatic redirects or enforce the same destination checks on every redirect target. An allowed starting URL can redirect somewhere forbidden. ⟦A.f4 A:tb3⟧
[DIAGRAM: Outbound destination trust boundary] nodes=['Requested provider', 'Allowlist: catalog → https://catalog.example/lookup; shipping → https://shipping.example/lookup', 'Validate resolved address actually used', 'Reject private, loopback, link-local and other non-public IPv4/IPv6', 'Redirect target: same checks or disable automatic redirects', 'Public-only connection boundary'] edges=[('input', 'map', 'reject arbitrary destinations'), ('map', 'address', 'not just earlier hostname check'), ('address', 'deny', 'non-public'), ('address', 'public', 'policy permits'), ('public', 'redirect', 'redirect response'), ('redirect', 'map', 'reapply destination checks')] alt: Outbound destination trust boundary: Requested provider; Allowlist: catalog → https://catalog.example/lookup; shipping → https://shipping.example/lookup; Validate resolved address actually used; Reject private, loopback, link-local and other non-public IPv4/IPv6; Redirect target: same checks or disable automatic redirects; Public-only connection boundary

### s02 · explainer · Trace the contract
Explainer — 
(mental_model) Trace three boundaries, not just one hostname: requested provider, address actually connected to, and redirect target. Map known providers to allowed destinations. Reject non-public IPv4 and IPv6 addresses for public-only access, and validate the resolved address used by the connection. Disable redirects or check each target. A permitted-looking hostname alone leaves the connected-address and redirect boundaries unverified. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Check the boundary: Preventing unsafe outbound requests and SSRF
Check — Use the supplied order-service scenario to reason about this contract.
QUESTION [choice, intro, grading=client] An outbound policy permits only public services. What must it do with a destination resolving to a private, loopback or link-local address, including IPv6 equivalents?
  ✔ option_1: Reject it under the public-address boundary.
      why: The policy excludes private, loopback, link-local and other non-public addresses.
  ✘ option_2: Allow it whenever the destination hostname looks public.
      why: A hostname appearance does not make a resolved non-public address acceptable.
  ✘ option_3: Reject those IPv4 destinations but permit equivalent IPv6 destinations.
      why: The non-public boundary includes IPv6 equivalents.
  feedback✔: The policy excludes private, loopback, link-local and other non-public addresses.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Separate the stated requirement from a nearby but different boundary.']  remediation→r01
  MEASURES: A:identify_non_public_address_boundary_violations(f2)   anchors=['assessment:identify_non_public_address_boundary_violations']
  taught-before-tested: A.f2←s01

### s04 · check · Check the boundary: Preventing unsafe outbound requests and SSRF
Check — Use the supplied order-service scenario to reason about this contract.
QUESTION [choice, core, grading=client] Resolution can change after an earlier hostname check, and an approved URL can redirect. Which policy closes both gaps?
  ✘ option_2: Trust later resolution and check only the initial URL
      why: Trusting later resolution omits validation of the connected address, and checking only the initial URL omits the redirect-target boundary.
  ✘ option_3: Validate the connected address but follow redirects without checking their targets.
      why: Connected-address validation does not cover redirect targets; automatic redirects must be disabled or every target must undergo the same destination checks.
  ✔ option_1: Validate the resolved address actually used for connection, and disable automatic redirects or apply the same destination checks to every redirect target.
      why: Checking the connected address closes the resolution gap; disabling redirects or checking every target preserves the destination policy across redirects.
  feedback✔: Checking the connected address closes the resolution gap; disabling redirects or checking every target preserves the destination policy across redirects.  feedback✘: Trusting later resolution omits validation of the connected address, and checking only the initial URL omits the redirect-target boundary. Connected-address validation does not cover redirect targets; automatic redirects must be disabled or every target must undergo the same destination checks.  hints: ['Separate the stated requirement from a nearby but different boundary.']
  MEASURES: A:identify_dns_rebinding_validation_gaps(f3); A:identify_redirect_destination_policy_bypasses(f4)   anchors=['assessment:identify_dns_rebinding_validation_gaps', 'assessment:identify_redirect_destination_policy_bypasses']
  taught-before-tested: A.f3←s01; A.f4←s01

### s05 · hands_on · Apply the contract: Preventing unsafe outbound requests and SSRF
Hands On — Complete the supplied workspace within its stated contract.
QUESTION [code_exercise, stretch, grading=client] Complete destination_for_provider. Return the configured dictionary destination only for known provider keys; raise ValueError for every other input, including arbitrary URL strings. No network is contacted. This task implements destination selection only, not connected-address validation or redirect enforcement.
  runtime={'kind': 'python_asgi', 'version': '0.29.5'} constraints.allowed=['def', 'str parameter and return annotations', 'string literals', 'dictionary literals', 'dictionary key lookup', 'if', 'not in', 'return', 'raise ValueError'] blocked=5 items
  file exercise.py [editable]:
allowed_destinations = {
    'catalog': 'https://catalog.example/lookup',
    'shipping': 'https://shipping.example/lookup',
}
def destination_for_provider(provider: str) -> str:
    # TODO: return only a configured destination; reject unknown keys.
    raise NotImplementedError
def _case(provider):
    try: return {'destination':destination_for_provider(provider)}
    except ValueError: return {'rejected':provider}
import inspect
from fastapi import FastAPI, Body
verification_app=FastAPI()

async def verify_case(payload: dict=Body(...)):
    result=_case(payload['case'])
    if inspect.isawaitable(result):return await result
    return result
verify_case = verification_app.post('/_verify')(verify_case)

  SOLUTION exercise.py:
allowed_destinations = {
    'catalog': 'https://catalog.example/lookup',
    'shipping': 'https://shipping.example/lookup',
}
def destination_for_provider(provider: str) -> str:
    if provider not in allowed_destinations:
        raise ValueError('unknown provider')
    return allowed_destinations[provider]
def _case(provider):
    try: return {'destination':destination_for_provider(provider)}
    except ValueError: return {'rejected':provider}
import inspect
from fastapi import FastAPI, Body
verification_app=FastAPI()

async def verify_case(payload: dict=Body(...)):
    result=_case(payload['case'])
    if inspect.isawaitable(result):return await result
    return result
verify_case = verification_app.post('/_verify')(verify_case)

  test test_1 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"catalog"}}],"app":"verification_app","expected":{"status":200,"json":{"destination":"https://catalog.example/lookup"}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  test test_2 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"shipping"}}],"app":"verification_app","expected":{"status":200,"json":{"destination":"https://shipping.example/lookup"}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  test test_3 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"unknown"}}],"app":"verification_app","expected":{"status":200,"json":{"rejected":"unknown"}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  test test_4 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"https://arbitrary.example/lookup"}}],"app":"verification_app","expected":{"status":200,"json":{"rejected":"https://arbitrary.example/lookup"}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  test test_5 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":""}}],"app":"verification_app","expected":{"status":200,"json":{"rejected":""}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  test test_6 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"CATALOG"}}],"app":"verification_app","expected":{"status":200,"json":{"rejected":"CATALOG"}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"c98e2b8dae82eeb03acec24e514ed260eaf1a92a0ae6c20d3afd8016e4eb19f8","tests_passed":6}
  feedback✔: You applied the declared boundary and preserved its required behavior.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Compare each declaration with its input or lifecycle boundary.', 'Trace what happens on the alternative input or exit, not only the successful path.']
  MEASURES: A:identify_arbitrary_destination_selection(f1)   anchors=['practice', 'assessment:identify_arbitrary_destination_selection']
  taught-before-tested: A.f1←s01

### s06 · recap · Keep these distinctions
Recap — 
(takeaway) Allowlist destinations; reject non-public IPv4/IPv6; validate connected addresses; disable or recheck redirects. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: tile_043 — Bounded form and multipart file inputs: Start with Bounded form and multipart file inputs.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Preventing unsafe outbound requests and SSRF
(definition) For public-only access, reject private, loopback, link-local and other non-public addresses, including IPv6 equivalents. ⟦A.f2 A:tb3 A:tb4⟧
(example) For public-only outbound access, a loopback address is forbidden even in IPv6 form; changing address family does not change that boundary. ⟦A.f2 A:tb3 A:tb4⟧
### r02 · Try the contrast: Preventing unsafe outbound requests and SSRF
(definition) Validate the resolved address actually used for the connection. Checking a hostname earlier is insufficient against a DNS rebinding gap. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) For the provider lookup, an earlier hostname check differs from validating the resolved address actually used for the connection. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r03 · Try the contrast: Preventing unsafe outbound requests and SSRF
(definition) For known destinations, map untrusted provider input to an allowed destination instead of accepting an arbitrary outbound URL. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Disable automatic redirects or enforce the same destination checks on every redirect target. An allowed starting URL can redirect somewhere forbidden. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(example) A configured provider destination is allowed as a starting point, but a redirect from it must still satisfy the destination policy or be disabled. ⟦A.f1 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Bounded form and multipart file inputs (tile_043)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.bounded_multipart_inputs — Bounded form and multipart file inputs

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: remediation step tile_043.r02 is never referenced
  warn: plan: tile_043.s04 was planned to measure fastapi.bounded_multipart_inputs#assessment:distinguish_multipart_parser_limits_from_total_body_limit but its interaction does not

## SOURCE FACTS — A (fastapi.bounded_multipart_inputs)   objective: Accept bounded form and multipart inputs: implement one bounded multipart endpoint with form metadata and a file.
A.f1: Declare form metadata with Annotated[Type, Form()] and an uploaded file with Annotated[UploadFile, File()] in the same multipart handler; multipart parsing requires python-multipart.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/request-forms-and-files/#define-file-and-form-parameters]
A.f2: UploadFile uses a spooled file rather than requiring the entire upload to be represented as bytes in memory, and exposes asynchronous read, seek and close methods.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/request-files/#uploadfile]
A.f3: Apply RequestBodyLimitMiddleware with a finite max_body_size to count actual incoming body bytes, including multipart overhead, and return 413 when the limit is exceeded.   [sources: fastapi_docs_advanced#https://starlette.dev/middleware/#requestbodylimitmiddleware]
A.f4: Multipart parsing can separately bound file count, field count and non-file field size with request.form(max_files=..., max_fields=..., max_part_size=...); these controls do not replace a total body limit.   [sources: fastapi_docs_advanced#https://starlette.dev/requests/#request-files]
A.f5: Reject disallowed content types and validate the supplied fields before processing, then close an UploadFile with await file.close() when finished with its resource.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html#input-validation, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/request-files/#uploadfile]
note: Establish this first: Multipart is an untrusted structured stream, not an unlimited in-memory value.
note: Stay within the current objective: Accept bounded form and multipart inputs. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Reject oversized or disallowed multipart data while binding form values and handling file resources safely.
PRACTICE ANCHOR (live_code): Implement one bounded attachment endpoint that binds form metadata and an uploaded file, enforces a finite total body budget and separate multipart parser limits, validates inputs before processing, and closes the uploaded file.  SUCCESS: The endpoint accepts permitted metadata and attachment content, rejects disallowed attachment content types and invalid metadata before processing, returns 413 when actual body bytes exceed the budget, applies the configured parser limits before binding, and closes every file resource it handles.
ASSESSMENT ANCHOR: bind_form_metadata_and_uploaded_file facts=['f1']
ASSESSMENT ANCHOR: handle_spooled_upload_resources_safely facts=['f2', 'f5']
ASSESSMENT ANCHOR: enforce_actual_multipart_body_byte_limit facts=['f3']
ASSESSMENT ANCHOR: distinguish_multipart_parser_limits_from_total_body_limit facts=['f3', 'f4']
ASSESSMENT ANCHOR: reject_disallowed_upload_types_and_invalid_metadata facts=['f5']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; CORS origin and credential policy; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Credential and sensitive-data redaction from emitted logs; Distinct create and partial-update contracts; Endpoint integration tests using TestClient or async HTTPX as appropriate; FastAPI OpenAPI generation from typed route contracts; Graceful termination and shutdown verification; Header and cookie input binding; Keeping API schemas distinct from persistence entities; Meaningful contract examples and operation metadata; Redis cache-aside selection and population; Request-scoped async-compatible PostgreSQL session lifecycle; Request-scoped dependency reuse and lifetime; Request-validation error behavior; Required, optional and default input semantics; Retrieve resource; Service health and readiness checks; Test dependency replacement; Transaction commit and rollback boundaries; Translating domain and p

## LESSON, in learner order

### s01 · explainer · Declare the boundary: Bounded form and multipart file inputs
Explainer — 
(mechanism) In one multipart handler, declare metadata with Annotated[Type, Form()] and the file with Annotated[UploadFile, File()]. Install python-multipart for parsing. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) UploadFile uses a spooled file rather than requiring the entire upload as in-memory bytes. Its read, seek and close methods are asynchronous. ⟦A.f2 A:tb3⟧
(mechanism) Set a finite RequestBodyLimitMiddleware max_body_size. Count actual incoming bytes, including multipart overhead; exceeding that limit returns 413. ⟦A.f3 A:tb3⟧
(mechanism) request.form(max_files=..., max_fields=..., max_part_size=...) separately limits file count, field count and non-file field size. These limits do not replace the total-body limit. ⟦A.f4 A:tb3⟧
(mechanism) Reject disallowed content types and validate fields before processing. When finished, release the upload with await file.close(). ⟦A.f5 A:tb3⟧
[CODE python]
from typing import Annotated
from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from support import (RequestBodyLimitMiddleware, BoundedMultipartRoute,
                     budgets, permitted_content_types)
app = FastAPI()
app.router.route_class = BoundedMultipartRoute
app.add_middleware(RequestBodyLimitMiddleware,
                   max_body_size=budgets['max_body_size'])
@app.post('/orders/attachments')
async def attachment(metadata: Annotated[str, Form()],
                     file: Annotated[UploadFile, File()]):
    try:
        if file.content_type not in permitted_content_types:
            raise HTTPException(status_code=400, detail='disallowed content type')
        if len(metadata) > budgets['metadata_max_length']:
            raise HTTPException(status_code=400, detail='invalid metadata')
        data = await file.read(budgets['read_size'])
        await file.seek(0)
        return {'metadata': metadata}
    finally:
        await file.close()

  annotations: ['Total actual-body-byte boundary, including multipart overhead.', 'Typed form metadata and spooled file; python-multipart required.', 'Validate before reading.', 'Asynchronous cleanup on success or rejection.']
[CODE python]
from fastapi.routing import APIRoute
from support import budgets
class BoundedMultipartRoute(APIRoute):
    def get_route_handler(self):
        original = super().get_route_handler()
        async def bounded(request):
            # Parsing precedes automatic typed parameter binding.
            form = await request.form(max_files=budgets['max_files'],
                max_fields=budgets['max_fields'], max_part_size=budgets['max_part_size'])
            try:
                return await original(request)
            finally:
                await form.close()
        return bounded

  annotations: ['Parser limits run before automatic typed parameter binding; non-file part size is separate from the total body budget.']

### s02 · explainer · Trace the contract
Explainer — 
(mental_model) Treat limits as separate controls. Form and File declarations need python-multipart; a spooled UploadFile offers asynchronous resource methods, not unlimited input. The finite body budget counts actual bytes including overhead and returns 413 on excess. Parser options bound file count, field count and non-file field size, but do not replace that budget. Validate fields and content type before processing, and close the file afterward. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb4 A:tb5⟧

### s03 · check · Check the boundary: Bounded form and multipart file inputs
Check — Use the supplied order-service scenario to reason about this contract.
QUESTION [choice, intro, grading=client] Which policy correctly handles invalid uploads and the separate input limits?
  ✔ option_1: Reject invalid metadata or content types before processing and close handled uploads; parser file-count, field-count and non-file-part-size limits remain separate from the actual total-body-byte limit.
      why: Validation precedes processing and handled uploads are closed. Parser counts and non-file-part sizes do not replace the actual total-body-byte budget.
  ✘ option_2: Process uploads before checking metadata or content types, then close handled uploads; keep parser limits separate from the total-body-byte limit.
      why: Processing before checking metadata and content types violates validation-before-processing, even if the upload is later closed.
  ✘ option_3: Reject invalid metadata or content types before processing and close handled uploads; parser limits replace the total-body-byte limit.
      why: Parser file-count, field-count and non-file-part-size limits are separate from, not replacements for, the actual total-body-byte limit.
  feedback✔: Validation precedes processing and handled uploads are closed. Parser counts and non-file-part sizes do not replace the actual total-body-byte budget.  feedback✘: Processing before checking metadata and content types violates validation-before-processing, even if the upload is later closed. Parser file-count, field-count and non-file-part-size limits are separate from, not replacements for, the actual total-body-byte limit.  hints: ['Separate the stated requirement from a nearby but different boundary.']  remediation→r01
  MEASURES: A:reject_disallowed_upload_types_and_invalid_metadata(f5); A:distinguish_multipart_parser_limits_from_total_body_limit(f3,f4)   anchors=['assessment:reject_disallowed_upload_types_and_invalid_metadata', 'assessment:distinguish_multipart_parser_limits_from_total_body_limit']
  taught-before-tested: A.f5←s01; A.f3←s01; A.f4←s01

### s04 · hands_on · Apply the contract: Bounded form and multipart file inputs
Hands On — Complete the supplied workspace within its stated contract.
QUESTION [code_exercise, stretch, grading=client] Register RequestBodyLimitMiddleware using budgets['max_body_size']. Complete attachment with metadata: Annotated[str, Form()] and file: Annotated[UploadFile, File()]. Inside try/finally, reject content types outside permitted_content_types with 415 and metadata longer than budgets['metadata_max_length'] with 422 before reading. Read at most budgets['read_size']; return {'metadata': metadata, 'size': len(content)}. Always await file.close() in finally. Keep the supplied bounded route (parser limits before binding) unchanged. The harness covers permitted input, rejection, actual-byte overflow including multipart overhead, file/field counts and non-file part size.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': ['python-multipart']} constraints.allowed=['from typing import Annotated', 'from fastapi import FastAPI, Form, File, UploadFile, Request, HTTPException', 'app = FastAPI()', '@app.post(...)', 'async def', 'Annotated[str, Form()]', 'Annotated[UploadFile, File()]', 'app.add_middleware(RequestBodyLimitMiddleware, max_body_size=...)', 'await request.form(max_files=..., max_fields=..., max_part_size=...)', 'await file.read(size)', 'await file.seek(0)', 'await file.close()', 'file.content_type', 'if', 'not in', 'len(metadata)', 'raise HTTPException(status_code=..., detail=...)', 'try', 'finally', 'return', 'assignment', 'string and integer literals', 'tuple literals', 'dictionary literals', 'comparison operators'] blocked=8 items
  file exercise.py [editable]:
from fastapi.routing import APIRoute
from starlette.datastructures import UploadFile
from starlette.responses import Response
budgets = {'max_body_size': 4096, 'max_files': 1, 'max_fields': 1,
           'max_part_size': 256, 'read_size': 1024, 'metadata_max_length': 80}
permitted_content_types = ('text/plain',)
class RequestBodyLimitMiddleware:
    def __init__(self, app, max_body_size):
        self.app, self.limit = app, max_body_size
    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)
        messages, size = [], 0
        while True:
            message = await receive()
            if message['type'] == 'http.disconnect':
                return
            size += len(message.get('body', b''))
            if size > self.limit:
                return await Response(status_code=413)(scope, receive, send)
            messages.append(message)
            if not message.get('more_body', False):
                break
        async def replay():
            if messages:
                return messages.pop(0)
            return await receive()
        await self.app(scope, replay, send)
class BoundedMultipartRoute(APIRoute):
    def get_route_handler(self):
        original = super().get_route_handler()
        async def bounded(request):
            # Parsing precedes automatic typed parameter binding.
            form = await request.form(max_files=budgets['max_files'],
                max_fields=budgets['max_fields'], max_part_size=budgets['max_part_size'])
            try:
                return await original(request)
            finally:
                await form.close()
        return bounded
from typing import Annotated
from fastapi import FastAPI, Form, File, UploadFile, Request, HTTPException
app = FastAPI()
app.router.route_class = BoundedMultipartRoute
# TODO: register the actual-byte middleware using the supplied budget.

async def attachment():
    # TODO: bind only metadata and file using Form/File/UploadFile.
    # Validate before processing, read at most budgets['read_size'],
    # and await file.close() in finally.
    raise NotImplementedError
attachment = app.post('/orders/attachments')(attachment)
import asyncio, inspect, json, ast
import httpx
from contextlib import contextmanager

def _drive(coro):
    try:
        pending = coro.send(None)
    except StopIteration as done:
        return done.value
    raise RuntimeError('Harness encountered a suspending operation: ' + repr(pending))

async def _requests(application, requests):
    async with application.router.lifespan_context(application):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application, raise_app_exceptions=False), base_url='http://testserver') as client:
            out=[]
            for method,path,kwargs in requests:
                response=await client.request(method,path,**kwargs)
                try: body=response.json()
                except ValueError: body=response.text
                out.append({'status':response.status_code,'body':body})
            return out
def _case(which):
    from unittest.mock import patch
    from starlette.datastructures import UploadFile as StarletteUploadFile
    reads=[]; closed=[]
    old_read=StarletteUploadFile.read; old_close=StarletteUploadFile.close
    async def read(file,size=-1):
        reads.append(size)
        return await old_read(file,size)
    async def close(file):
        await old_close(file)
        closed.append(file.file.closed)
    async def run():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app,raise_app_exceptions=False),base_url='http://testserver') as client:
            metadata='valid';type_='text/plain';payload=b'attachment'
            parts=None
            if which=='invalid_metadata': metadata='m'*(budgets['metadata_max_length']+1)
            if which=='type': type_='application/octet-stream'
            if which=='overflow':payload=b'x'*(budgets['max_body_size']+1)
            parts=[('metadata',(None,metadata)),('file',('attachment.txt',payload,type_))]
            if which=='files': parts.append(('file',('extra.txt',b'extra','text/plain')))
            if which=='fields': parts.append(('extra',(None,'extra')))
            if which=='part': parts[0]=('metadata',(None,'m'*(budgets['max_part_size']+1)))
            response=await client.post('/orders/attachments',files=parts)
            return response
    with patch.object(StarletteUploadFile,'read',read),patch.object(StarletteUploadFile,'close',close):
        r=_drive(run())
    expected={'valid':200,'invalid_metadata':422,'type':415,'overflow':413,'files':400,'fields':400,'part':400}[which]
    assert r.status_code==expected, (which,r.status_code,r.text)
    if which=='valid':assert reads==[budgets['read_size']]
    if which in ('invalid_metadata','type'): assert reads==[]
    if which in ('valid','invalid_metadata','type'): assert closed and all(closed)
    result = {'case':which,'status':r.status_code,'reads':reads}
    if which in ('valid','invalid_metadata','type'):
        result['handled_uploads_closed'] = bool(closed) and all(closed)
    else:
        result['closed'] = closed
    return result
import inspect
from fastapi import FastAPI, Body
verification_app=FastAPI()

async def verify_case(payload: dict=Body(...)):
    result=_case(payload['case'])
    if inspect.isawaitable(result):return await result
    return result
verify_case = verification_app.post('/_verify')(verify_case)

  SOLUTION exercise.py:
from fastapi.routing import APIRoute
from starlette.datastructures import UploadFile
from starlette.responses import Response
budgets = {'max_body_size': 4096, 'max_files': 1, 'max_fields': 1,
           'max_part_size': 256, 'read_size': 1024, 'metadata_max_length': 80}
permitted_content_types = ('text/plain',)
class RequestBodyLimitMiddleware:
    def __init__(self, app, max_body_size):
        self.app, self.limit = app, max_body_size
    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)
        messages, size = [], 0
        while True:
            message = await receive()
            if message['type'] == 'http.disconnect':
                return
            size += len(message.get('body', b''))
            if size > self.limit:
                return await Response(status_code=413)(scope, receive, send)
            messages.append(message)
            if not message.get('more_body', False):
                break
        async def replay():
            if messages:
                return messages.pop(0)
            return await receive()
        await self.app(scope, replay, send)
class BoundedMultipartRoute(APIRoute):
    def get_route_handler(self):
        original = super().get_route_handler()
        async def bounded(request):
            # Parsing precedes automatic typed parameter binding.
            form = await request.form(max_files=budgets['max_files'],
                max_fields=budgets['max_fields'], max_part_size=budgets['max_part_size'])
            try:
                return await original(request)
            finally:
                await form.close()
        return bounded
from typing import Annotated
from fastapi import FastAPI, Form, File, UploadFile, Request, HTTPException
app = FastAPI()
app.router.route_class = BoundedMultipartRoute
app.add_middleware(RequestBodyLimitMiddleware, max_body_size=budgets['max_body_size'])

async def attachment(metadata: Annotated[str, Form()], file: Annotated[UploadFile, File()]):
    try:
        if file.content_type not in permitted_content_types:
            raise HTTPException(status_code=415, detail='disallowed attachment')
        if len(metadata) > budgets['metadata_max_length']:
            raise HTTPException(status_code=422, detail='invalid metadata')
        content = await file.read(budgets['read_size'])
        return {'metadata': metadata, 'size': len(content)}
    finally:
        await file.close()
attachment = app.post('/orders/attachments')(attachment)
import asyncio, inspect, json, ast
import httpx
from contextlib import contextmanager

def _drive(coro):
    try:
        pending = coro.send(None)
    except StopIteration as done:
        return done.value
    raise RuntimeError('Harness encountered a suspending operation: ' + repr(pending))

async def _requests(application, requests):
    async with application.router.lifespan_context(application):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application, raise_app_exceptions=False), base_url='http://testserver') as client:
            out=[]
            for method,path,kwargs in requests:
                response=await client.request(method,path,**kwargs)
                try: body=response.json()
                except ValueError: body=response.text
                out.append({'status':response.status_code,'body':body})
            return out
def _case(which):
    from unittest.mock import patch
    from starlette.datastructures import UploadFile as StarletteUploadFile
    reads=[]; closed=[]
    old_read=StarletteUploadFile.read; old_close=StarletteUploadFile.close
    async def read(file,size=-1):
        reads.append(size)
        return await old_read(file,size)
    async def close(file):
        await old_close(file)
        closed.append(file.file.closed)
    async def run():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app,raise_app_exceptions=False),base_url='http://testserver') as client:
            metadata='valid';type_='text/plain';payload=b'attachment'
            parts=None
            if which=='invalid_metadata': metadata='m'*(budgets['metadata_max_length']+1)
            if which=='type': type_='application/octet-stream'
            if which=='overflow':payload=b'x'*(budgets['max_body_size']+1)
            parts=[('metadata',(None,metadata)),('file',('attachment.txt',payload,type_))]
            if which=='files': parts.append(('file',('extra.txt',b'extra','text/plain')))
            if which=='fields': parts.append(('extra',(None,'extra')))
            if which=='part': parts[0]=('metadata',(None,'m'*(budgets['max_part_size']+1)))
            response=await client.post('/orders/attachments',files=parts)
            return response
    with patch.object(StarletteUploadFile,'read',read),patch.object(StarletteUploadFile,'close',close):
        r=_drive(run())
    expected={'valid':200,'invalid_metadata':422,'type':415,'overflow':413,'files':400,'fields':400,'part':400}[which]
    assert r.status_code==expected, (which,r.status_code,r.text)
    if which=='valid':assert reads==[budgets['read_size']]
    if which in ('invalid_metadata','type'): assert reads==[]
    if which in ('valid','invalid_metadata','type'): assert closed and all(closed)
    result = {'case':which,'status':r.status_code,'reads':reads}
    if which in ('valid','invalid_metadata','type'):
        result['handled_uploads_closed'] = bool(closed) and all(closed)
    else:
        result['closed'] = closed
    return result
import inspect
from fastapi import FastAPI, Body
verification_app=FastAPI()

async def verify_case(payload: dict=Body(...)):
    result=_case(payload['case'])
    if inspect.isawaitable(result):return await result
    return result
verify_case = verification_app.post('/_verify')(verify_case)

  test test_1 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"valid"}}],"app":"verification_app","expected":{"status":200,"json":{"case":"valid","status":200,"reads":[1024],"handled_uploads_closed":true}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  test test_2 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"invalid_metadata"}}],"app":"verification_app","expected":{"status":200,"json":{"case":"invalid_metadata","status":422,"reads":[],"handled_uploads_closed":true}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  test test_3 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"type"}}],"app":"verification_app","expected":{"status":200,"json":{"case":"type","status":415,"reads":[],"handled_uploads_closed":true}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  test test_4 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"overflow"}}],"app":"verification_app","expected":{"status":200,"json":{"case":"overflow","status":413,"reads":[],"closed":[]}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  test test_5 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"files"}}],"app":"verification_app","expected":{"status":200,"json":{"case":"files","status":400,"reads":[],"closed":[]}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  test test_6 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"fields"}}],"app":"verification_app","expected":{"status":200,"json":{"case":"fields","status":400,"reads":[],"closed":[]}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  test test_7 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"part"}}],"app":"verification_app","expected":{"status":200,"json":{"case":"part","status":400,"reads":[],"closed":[]}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"a0859454534832c0f1b8cf5a252221a905cb6704c4d928880807569e8c732f99","tests_passed":7}
  feedback✔: You applied the declared boundary and preserved its required behavior.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Compare each declaration with its input or lifecycle boundary.', 'Trace what happens on the alternative input or exit, not only the successful path.']
  MEASURES: A:bind_form_metadata_and_uploaded_file(f1); A:handle_spooled_upload_resources_safely(f2,f5); A:enforce_actual_multipart_body_byte_limit(f3); A:reject_disallowed_upload_types_and_invalid_metadata(f5)   anchors=['practice', 'assessment:bind_form_metadata_and_uploaded_file', 'assessment:handle_spooled_upload_resources_safely', 'assessment:enforce_actual_multipart_body_byte_limit', 'assessment:reject_disallowed_upload_types_and_invalid_metadata']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f5←s01; A.f3←s01; A.f5←s01

### s05 · recap · Keep these distinctions
Recap — 
(takeaway) Bind Form/File inputs; use spooled asynchronous uploads; enforce total and parser limits separately; validate before processing and close files. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: tile_044 — CORS origin and credential policy: Start with CORS origin and credential policy.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Bounded form and multipart file inputs
(definition) Reject disallowed content types and validate fields before processing. When finished, release the upload with await file.close(). ⟦A.f5 A:tb3 A:tb4⟧
(example) For the supplied attachment, a permitted content type does not excuse invalid metadata; both must pass before processing. ⟦A.f5 A:tb3 A:tb4⟧
### r02 · Try the contrast: Bounded form and multipart file inputs
(definition) In one multipart handler, declare metadata with Annotated[Type, Form()] and the file with Annotated[UploadFile, File()]. Install python-multipart for parsing. ⟦A.f1 A:tb2 A:tb4⟧
(definition) UploadFile uses a spooled file rather than requiring the entire upload as in-memory bytes. Its read, seek and close methods are asynchronous. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Set a finite RequestBodyLimitMiddleware max_body_size. Count actual incoming bytes, including multipart overhead; exceeding that limit returns 413. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(definition) request.form(max_files=..., max_fields=..., max_part_size=...) separately limits file count, field count and non-file field size. These limits do not replace the total-body limit. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(definition) Reject disallowed content types and validate fields before processing. When finished, release the upload with await file.close(). ⟦A.f5 A:tb3 A:tb4⟧
(example) For the supplied attachment, a permitted content type does not excuse invalid metadata; both must pass before processing. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: app.dependency_overrides[...]
· constraints.blocked_syntax: @app.exception_handler(...)
· constraints.blocked_syntax: TrustedHostMiddleware(...)
· constraints.blocked_syntax: model_dump(exclude_unset=True)

=========

# EVALUATOR PACKET — CORS origin and credential policy (tile_044)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.cors_policy — CORS origin and credential policy

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: remediation step tile_044.r02 is never referenced
  warn: plan: tile_044.s04 was planned to measure fastapi.cors_policy#assessment:distinguish_browser_access_from_endpoint_access_control but its interaction does not

## SOURCE FACTS — A (fastapi.cors_policy)   objective: Set safe CORS policy: configure one browser-client policy.
A.f1: Configure app.add_middleware(CORSMiddleware, allow_origins=[...], allow_methods=[...], allow_headers=[...], allow_credentials=...) with the origins, methods and headers the browser client actually needs.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/cors/#use-corsmiddleware]
A.f2: CORSMiddleware defaults are restrictive: allowed methods default to GET and credentials default to false.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/cors/#use-corsmiddleware]
A.f3: When allow_credentials=True, explicitly specify allowed origins, methods and headers rather than wildcard lists.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/cors/#use-corsmiddleware]
A.f4: CORS signals browser access permission; it does not replace access-control checks at API endpoints.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html#cors, owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html#access-control]
note: Establish this first: CORS controls browser response access, not authentication.
note: Stay within the current objective: Set safe CORS policy. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify unsafe origin and credential combinations.
PRACTICE ANCHOR (live_code): Configure CORSMiddleware for the browser client at https://shop.example, allowing GET and POST requests with the Content-Type header and credentialed browser access.  SUCCESS: The application registers CORSMiddleware with the exact client origin, explicit GET and POST methods, an explicit Content-Type header list, and allow_credentials=True, without wildcard entries.
ASSESSMENT ANCHOR: identify_unsafe_origin_and_credential_combinations facts=['f1', 'f3']
ASSESSMENT ANCHOR: recognize_restrictive_cors_defaults facts=['f2']
ASSESSMENT ANCHOR: distinguish_browser_access_from_endpoint_access_control facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Consistent public error envelopes through exception handlers; Credential and sensitive-data redaction from emitted logs; Distinct create and partial-update contracts; Endpoint integration tests using TestClient or async HTTPX as appropriate; FastAPI OpenAPI generation from typed route contracts; Graceful termination and shutdown verification; Header and cookie input binding; Keeping API schemas distinct from persistence entities; Meaningful contract examples and operation metadata; Redis cache-aside selection and population; Request-scoped async-compatible PostgreSQL session lifecycle; Request-scoped dependency reuse and lifetime; Request-validation error behavior; Required, optional and default input semantics; Retrieve resource; Service health and readiness checks; Test dependency replacement; Transaction commit and rollback boundarie

## LESSON, in learner order

### s01 · explainer · Declare the boundary: CORS origin and credential policy
Explainer — 
(mechanism) Use app.add_middleware(CORSMiddleware, ...) with allow_origins, allow_methods, allow_headers and allow_credentials matching the browser client’s actual needs. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) Defaults are restrictive: allowed methods default to GET, and credentials default to false. ⟦A.f2 A:tb3⟧
(mechanism) With allow_credentials=True, specify origins, methods and headers explicitly rather than using wildcard lists. ⟦A.f3 A:tb3⟧
(mechanism) CORS grants browser access permission; endpoint access-control checks remain separate and necessary. ⟦A.f4 A:tb3⟧
[CODE python]
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
# Content-Type, and credentials; use explicit lists with no wildcards.
app.add_middleware(CORSMiddleware,
    allow_origins=['https://shop.example'],
    allow_methods=['GET', 'POST'],
    allow_headers=['Content-Type'],
    allow_credentials=True)

  annotations: ['Explicit shop-client permissions; credentials enabled. Browser permission does not replace endpoint access checks.']

### s02 · explainer · Trace the contract
Explainer — 
(mental_model) The shop browser needs its origin, methods and headers listed explicitly, with credentials enabled for this scenario. Defaults alone allow GET and leave credentials false. When credentials are true, do not use wildcard lists for origins, methods or headers. CORS answers a browser-permission question, not whether an endpoint should grant access. Keep endpoint access-control checks separate. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Check the boundary: CORS origin and credential policy
Check — Use the supplied order-service scenario to reason about this contract.
QUESTION [choice, intro, grading=client] Which statement correctly describes CORS defaults and its access-control boundary?
  ✔ option_1: Allowed methods default to GET and credentials to false; CORS controls browser access permission and does not replace endpoint access-control checks.
      why: Allowed methods default to GET and credentials to false. Browser access permission is separate from endpoint access-control checks.
  ✘ option_2: Allowed methods default to all methods and credentials to true; CORS controls browser access permission and does not replace endpoint access-control checks.
      why: These defaults are not permissive: allowed methods default to GET and credentials to false.
  ✘ option_3: Allowed methods default to GET and credentials to false; CORS replaces endpoint access-control checks.
      why: CORS controls browser access permission, not endpoint access control; endpoint checks remain necessary.
  feedback✔: Allowed methods default to GET and credentials to false. Browser access permission is separate from endpoint access-control checks.  feedback✘: These defaults are not permissive: allowed methods default to GET and credentials to false. CORS controls browser access permission, not endpoint access control; endpoint checks remain necessary.  hints: ['Separate the stated requirement from a nearby but different boundary.']  remediation→r01
  MEASURES: A:recognize_restrictive_cors_defaults(f2); A:distinguish_browser_access_from_endpoint_access_control(f4)   anchors=['assessment:recognize_restrictive_cors_defaults', 'assessment:distinguish_browser_access_from_endpoint_access_control']
  taught-before-tested: A.f2←s01; A.f4←s01

### s04 · hands_on · Apply the contract: CORS origin and credential policy
Hands On — Complete the supplied workspace within its stated contract.
QUESTION [code_exercise, stretch, grading=client] Register CORSMiddleware for exactly https://shop.example, explicit GET and POST methods, an explicit Content-Type header list, and allow_credentials=True. Do not use wildcards. Keep the supplied endpoint and verification harness unchanged; two preflights check the allowed client and an unrelated origin. This is browser access policy, not endpoint authorization.
  runtime={'kind': 'python_asgi', 'version': '0.29.5'} constraints.allowed=['from fastapi import FastAPI', 'from fastapi.middleware.cors import CORSMiddleware', 'app = FastAPI()', 'app.add_middleware(CORSMiddleware, allow_origins=[...], allow_methods=[...], allow_headers=[...], allow_credentials=...)', 'String literals', 'List literals', 'True and False boolean literals', 'Keyword arguments'] blocked=6 items
  file exercise.py [editable]:
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
# TODO: add middleware for https://shop.example with GET, POST,
# Content-Type, and credentials; use explicit lists with no wildcards.
import asyncio, inspect, json, ast
import httpx
from contextlib import contextmanager

def _drive(coro):
    try:
        pending = coro.send(None)
    except StopIteration as done:
        return done.value
    raise RuntimeError('Harness encountered a suspending operation: ' + repr(pending))

async def _requests(application, requests):
    async with application.router.lifespan_context(application):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application, raise_app_exceptions=False), base_url='http://testserver') as client:
            out=[]
            for method,path,kwargs in requests:
                response=await client.request(method,path,**kwargs)
                try: body=response.json()
                except ValueError: body=response.text
                out.append({'status':response.status_code,'body':body})
            return out
@app.get('/orders')
def orders(): return {'result':'browser policy fixture'}
def _case(origin):
    m=app.user_middleware[0]
    assert m.cls is CORSMiddleware
    methods=m.kwargs.get('allow_methods', [])
    assert len(methods)==2 and '*' not in methods and set(methods)=={'GET','POST'}
    assert {k:v for k,v in m.kwargs.items() if k!='allow_methods'}=={'allow_origins':['https://shop.example'],'allow_headers':['Content-Type'],'allow_credentials':True}
    async def run():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://testserver') as client:
            r=await client.options('/orders',headers={'Origin':origin,'Access-Control-Request-Method':'POST','Access-Control-Request-Headers':'Content-Type'})
            return {'status':r.status_code,'origin':r.headers.get('access-control-allow-origin'),'credentials':r.headers.get('access-control-allow-credentials')}
    return _drive(run())
import inspect
from fastapi import FastAPI, Body
verification_app=FastAPI()

async def verify_case(payload: dict=Body(...)):
    result=_case(payload['case'])
    if inspect.isawaitable(result):return await result
    return result
verify_case = verification_app.post('/_verify')(verify_case)

  SOLUTION exercise.py:
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
# TODO: add middleware for https://shop.example with GET, POST,
# Content-Type, and credentials; use explicit lists with no wildcards.
app.add_middleware(CORSMiddleware, allow_origins=['https://shop.example'], allow_methods=['GET', 'POST'], allow_headers=['Content-Type'], allow_credentials=True)
import asyncio, inspect, json, ast
import httpx
from contextlib import contextmanager

def _drive(coro):
    try:
        pending = coro.send(None)
    except StopIteration as done:
        return done.value
    raise RuntimeError('Harness encountered a suspending operation: ' + repr(pending))

async def _requests(application, requests):
    async with application.router.lifespan_context(application):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application, raise_app_exceptions=False), base_url='http://testserver') as client:
            out=[]
            for method,path,kwargs in requests:
                response=await client.request(method,path,**kwargs)
                try: body=response.json()
                except ValueError: body=response.text
                out.append({'status':response.status_code,'body':body})
            return out
@app.get('/orders')
def orders(): return {'result':'browser policy fixture'}
def _case(origin):
    m=app.user_middleware[0]
    assert m.cls is CORSMiddleware
    methods=m.kwargs.get('allow_methods', [])
    assert len(methods)==2 and '*' not in methods and set(methods)=={'GET','POST'}
    assert {k:v for k,v in m.kwargs.items() if k!='allow_methods'}=={'allow_origins':['https://shop.example'],'allow_headers':['Content-Type'],'allow_credentials':True}
    async def run():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://testserver') as client:
            r=await client.options('/orders',headers={'Origin':origin,'Access-Control-Request-Method':'POST','Access-Control-Request-Headers':'Content-Type'})
            return {'status':r.status_code,'origin':r.headers.get('access-control-allow-origin'),'credentials':r.headers.get('access-control-allow-credentials')}
    return _drive(run())
import inspect
from fastapi import FastAPI, Body
verification_app=FastAPI()

async def verify_case(payload: dict=Body(...)):
    result=_case(payload['case'])
    if inspect.isawaitable(result):return await result
    return result
verify_case = verification_app.post('/_verify')(verify_case)

  test test_1 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"https://shop.example"}}],"app":"verification_app","expected":{"status":200,"json":{"status":200,"origin":"https://shop.example","credentials":"true"}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  test test_2 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"https://unrelated.example"}}],"app":"verification_app","expected":{"status":200,"json":{"status":400,"origin":null,"credentials":"true"}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"3cf40373883b8d60ca2927c6392eb98f77d3b65478d460fe7d49fddd6459a45d","tests_passed":2}
  feedback✔: You applied the declared boundary and preserved its required behavior.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Compare each declaration with its input or lifecycle boundary.', 'Trace what happens on the alternative input or exit, not only the successful path.']
  MEASURES: A:identify_unsafe_origin_and_credential_combinations(f1,f3)   anchors=['practice', 'assessment:identify_unsafe_origin_and_credential_combinations']
  taught-before-tested: A.f1←s01; A.f3←s01

### s05 · recap · Keep these distinctions
Recap — 
(takeaway) Match explicit CORS lists to the browser; remember restrictive defaults; credentials require explicit lists; endpoint access checks remain separate. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: tile_045 — Request-scoped dependency reuse and lifetime: Start with Request-scoped dependency reuse and lifetime.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: CORS origin and credential policy
(definition) Defaults are restrictive: allowed methods default to GET, and credentials default to false. ⟦A.f2 A:tb3 A:tb4⟧
(example) For the shop client, do not assume permissive defaults: default allowed methods are GET and default credentials are false. ⟦A.f2 A:tb3 A:tb4⟧
### r02 · Try the contrast: CORS origin and credential policy
(definition) Use app.add_middleware(CORSMiddleware, ...) with allow_origins, allow_methods, allow_headers and allow_credentials matching the browser client’s actual needs. ⟦A.f1 A:tb2 A:tb4⟧
(definition) With allow_credentials=True, specify origins, methods and headers explicitly rather than using wildcard lists. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(definition) CORS grants browser access permission; endpoint access-control checks remain separate and necessary. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(example) For the shop browser, explicit client permissions differ from endpoint access control; CORS does not replace it. ⟦A.f1 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: app.dependency_overrides[...]
· constraints.blocked_syntax: @app.exception_handler(...)

=========

# EVALUATOR PACKET — Request-scoped dependency reuse and lifetime · Endpoint integration tests using TestClient or async HTTPX as appropriate (tile_045)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.dependency_lifetime — Request-scoped dependency reuse and lifetime
B = fastapi.endpoint_integration_tests — Endpoint integration tests using TestClient or async HTTPX as appropriate

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=3
  warn: remediation step tile_045.r02 is never referenced
  warn: remediation step tile_045.r03 is never referenced
  warn: remediation step tile_045.r05 is never referenced

## SOURCE FACTS — A (fastapi.dependency_lifetime)   objective: Control dependency reuse: verify one shared provider's identity.
A.f1: FastAPI normally caches a dependency's returned value within one request when multiple dependants declare the same dependency.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/#using-the-same-dependency-multiple-times]
A.f2: Set Depends(provider, use_cache=False) when that declaration needs a fresh execution instead of the cached result.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/#using-the-same-dependency-multiple-times]
A.f3: Verify request-local reuse by having two dependants receive the same provider result during one request and checking a fresh request independently; this cache is not application-wide storage.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/#using-the-same-dependency-multiple-times]
note: Establish this first: Caching has request-local identity and lifetime.
note: Stay within the current objective: Control dependency reuse. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Predict reuse within one request.
PRACTICE ANCHOR (live_code): Have two dependants declare the same provider, compare their received values by identity during one request, and repeat the check in a fresh request.  SUCCESS: Requests A and B each report that both dependants received the same instance. Provider execution records show one execution in A and a separate execution in B, establishing reuse within each request rather than across requests.
ASSESSMENT ANCHOR: predict_shared_dependency_reuse_within_one_request facts=['f1']
ASSESSMENT ANCHOR: predict_fresh_execution_for_uncached_declaration facts=['f2']
ASSESSMENT ANCHOR: distinguish_request_local_reuse_from_application_wide_storage facts=['f3']

## SOURCE FACTS — B (fastapi.endpoint_integration_tests)   objective: Test an endpoint through its HTTP interface: write one integration test with TestClient or compatible async HTTPX setup.
B.f1: Create TestClient(app), send an HTTP request with client.get(...) or another request method, and assert response.status_code and response.json() in a test_ function run by pytest.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/testing/#using-testclient]
B.f2: Use with TestClient(app) as client when the test must execute application lifespan setup and teardown.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/testing-events/#testing-events-lifespan-and-startup-shutdown]
B.f3: Sending a request through TestClient exercises the application's route and dependency resolution rather than only calling the handler function directly.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/testing/#using-testclient, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/#declare-the-dependency-in-the-dependant]
note: Establish this first: Integration tests exercise the application boundary rather than calling a handler directly.
note: Stay within the current objective: Test an endpoint through its HTTP interface. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Assert status and payload including dependency and lifespan behavior.
PRACTICE ANCHOR (live_code): Write one pytest test for the supplied application's GET /orders/42 endpoint using a TestClient context manager, asserting status 200 and the JSON body {"id": 42, "quantity": 2}.  SUCCESS: Pytest discovers and passes the test. The test sends an HTTP request through the supplied application, asserts both status and JSON, and uses the context manager to include lifespan setup and teardown.
ASSESSMENT ANCHOR: assert_endpoint_status_and_json_payload facts=['f1']
ASSESSMENT ANCHOR: include_application_lifespan_in_test_boundary facts=['f2']
ASSESSMENT ANCHOR: distinguish_http_route_and_dependency_resolution_from_direct_handler_calls facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Consistent public error envelopes through exception handlers; Credential and sensitive-data redaction from emitted logs; Distinct create and partial-update contracts; Endpoint integration tests using TestClient or async HTTPX as appropriate; FastAPI OpenAPI generation from typed route contracts; Graceful termination and shutdown verification; Header and cookie input binding; Keeping API schemas distinct from persistence entities; Meaningful contract examples and operation metadata; Proxy header trust; Redis cache-aside selection and population; Request-scoped async-compatible PostgreSQL session lifecycle; Request-validation error behavior; Required, optional and default input semantics; Retrieve resource; Service health and readiness checks; Test dependency replacement; Transaction commit and rollback boundaries; Translating domain and 

## LESSON, in learner order

### s01 · explainer · Declare the boundary: Request-scoped dependency reuse and lifetime
Explainer — 
(mechanism) FastAPI normally caches a dependency result within a request when several dependants declare the same dependency. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) Use Depends(provider, use_cache=False) on a declaration that needs fresh execution instead of the cached result. ⟦A.f2 A:tb3⟧
(mechanism) Check that two dependants receive the same provider result in one request, then examine a fresh request independently. This cache is request-local, not application-wide storage. ⟦A.f3 A:tb3⟧
[DIAGRAM: Separate request-cache boundaries] nodes=['Request A', 'Provider execution → value A', 'First dependant: same value A', 'Second dependant: same value A', 'Depends(provider, use_cache=False): fresh execution', 'Request B', 'Independent provider execution → value B', 'First dependant: value B', 'Second dependant: value B'] edges=[('a', 'pa', 'normal request-local cache'), ('pa', 'a1', 'reuse'), ('pa', 'a2', 'reuse'), ('a', 'fresh', 'explicit uncached declaration'), ('b', 'pb', 'new request'), ('pb', 'b1', 'reuse'), ('pb', 'b2', 'reuse')] alt: Separate request-cache boundaries: Request A; Provider execution → value A; First dependant: same value A; Second dependant: same value A; Depends(provider, use_cache=False): fresh execution; Request B; Independent provider execution → value B; First dependant: value B; Second dependant: value B

### s02 · explainer · Trace the contract
Explainer — 
(mental_model) Draw request A around its provider result and both dependants. Verify reuse inside that boundary, then inspect request B independently. On a declaration needing another execution, use Depends(provider, use_cache=False). The normal cache reduces repeat execution within one request; it does not turn a request-specific value into storage shared by all clients. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · check · Check the boundary: Request-scoped dependency reuse and lifetime
Check — Use the supplied order-service scenario to reason about this contract.
QUESTION [choice, intro, grading=client] A particular dependency declaration must execute the provider freshly instead of using its request-local cached result. Which declaration requests that behavior?
  ✔ option_1: Depends(provider, use_cache=False).
      why: This declaration opts out of the normal cached result.
  ✘ option_2: Depends(provider) with normal caching.
      why: The normal declaration reuses the request-local cached provider result.
  ✘ option_3: Move the result into application-wide storage and retain normal caching.
      why: Application-wide storage is not the declaration-level fresh-execution behavior.
  feedback✔: This declaration opts out of the normal cached result.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Separate the stated requirement from a nearby but different boundary.']  remediation→r01
  MEASURES: A:predict_fresh_execution_for_uncached_declaration(f2)   anchors=['assessment:predict_fresh_execution_for_uncached_declaration']
  taught-before-tested: A.f2←s01

### s04 · check · Check the boundary: Request-scoped dependency reuse and lifetime
Check — Use the supplied order-service scenario to reason about this contract.
QUESTION [choice, core, grading=client] Two dependants normally reuse one provider value in request A. Request B starts independently. What boundary should verification establish?
  ✘ option_2: The same stored instance must be reused across requests A and B.
      why: Request-local caching does not imply application-wide shared storage.
  ✘ option_3: Normal caching requires two separate provider executions within request A.
      why: Multiple dependants normally reuse the same provider result within one request.
  ✔ option_1: Shared instance within each request, with a separate provider execution for request B.
      why: Reuse is request-local rather than application-wide storage.
  feedback✔: Reuse is request-local rather than application-wide storage.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Separate the stated requirement from a nearby but different boundary.']
  MEASURES: A:distinguish_request_local_reuse_from_application_wide_storage(f3)   anchors=['assessment:distinguish_request_local_reuse_from_application_wide_storage']
  taught-before-tested: A.f3←s01

### s05 · hands_on · Apply the contract: Request-scoped dependency reuse and lifetime
Hands On — Complete the supplied workspace within its stated contract.
QUESTION [code_exercise, core, grading=client] Replace the operation placeholder with return {'same_instance': a is b}. Keep provider and both cached dependency declarations unchanged. The harness sends request A and request B separately, verifies shared identity within each request and distinct provider executions across requests. Do not make a module-global shared value.
  runtime={'kind': 'python_asgi', 'version': '0.29.5'} constraints.allowed=['from fastapi import FastAPI, Depends', 'class declarations', 'def declarations', 'instance construction', 'parameter annotations', 'Depends(provider)', 'Depends(provider, use_cache=False)', 'path-operation decorators', 'local assignment', 'return statements', 'is identity comparison', 'dictionary literals', 'string and boolean literals', 'calls to the existing structured logger'] blocked=5 items
  file exercise.py [editable]:
import logging
logger = logging.getLogger('order.provider.exercise')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)
executions = []
def record_execution(value):
    executions.append(value)
    logger.info('provider execution', extra={'event_type': 'provider_execution'})
from fastapi import FastAPI, Depends
app = FastAPI()
class Value:
    pass
def provider():
    value = Value()
    record_execution(value)
    return value
def first(value=Depends(provider)):
    return value
def second(value=Depends(provider)):
    return value
@app.get('/orders')
def operation(a=Depends(first), b=Depends(second)):
    # TODO: report Python identity comparison of the two supplied values.
    raise NotImplementedError
# Then compare a declaration using Depends(provider, use_cache=False).
import asyncio, inspect, json, ast
import httpx
from contextlib import contextmanager

def _drive(coro):
    try:
        pending = coro.send(None)
    except StopIteration as done:
        return done.value
    raise RuntimeError('Harness encountered a suspending operation: ' + repr(pending))

async def _requests(application, requests):
    async with application.router.lifespan_context(application):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application, raise_app_exceptions=False), base_url='http://testserver') as client:
            out=[]
            for method,path,kwargs in requests:
                response=await client.request(method,path,**kwargs)
                try: body=response.json()
                except ValueError: body=response.text
                out.append({'status':response.status_code,'body':body})
            return out
def _case(requests):
    executions.clear()
    responses=_drive(_requests(app,[('GET','/orders',{'params':{'request':str(i)}}) for i in range(requests)]))
    assert len(executions)==requests
    assert len({id(x) for x in executions})==requests
    assert all(r=={'status':200,'body':{'same_instance':True}} for r in responses)
    return {'responses':responses,'provider_executions':len(executions),'distinct_values':len({id(x) for x in executions})}
import inspect
from fastapi import FastAPI, Body
verification_app=FastAPI()

async def verify_case(payload: dict=Body(...)):
    result=_case(payload['case'])
    if inspect.isawaitable(result):return await result
    return result
verify_case = verification_app.post('/_verify')(verify_case)

  SOLUTION exercise.py:
import logging
logger = logging.getLogger('order.provider.exercise')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)
executions = []
def record_execution(value):
    executions.append(value)
    logger.info('provider execution', extra={'event_type': 'provider_execution'})
from fastapi import FastAPI, Depends
app = FastAPI()
class Value:
    pass
def provider():
    value = Value()
    record_execution(value)
    return value
def first(value=Depends(provider)):
    return value
def second(value=Depends(provider)):
    return value
@app.get('/orders')
def operation(a=Depends(first), b=Depends(second)):
    return {'same_instance': a is b}
# Then compare a declaration using Depends(provider, use_cache=False).
import asyncio, inspect, json, ast
import httpx
from contextlib import contextmanager

def _drive(coro):
    try:
        pending = coro.send(None)
    except StopIteration as done:
        return done.value
    raise RuntimeError('Harness encountered a suspending operation: ' + repr(pending))

async def _requests(application, requests):
    async with application.router.lifespan_context(application):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application, raise_app_exceptions=False), base_url='http://testserver') as client:
            out=[]
            for method,path,kwargs in requests:
                response=await client.request(method,path,**kwargs)
                try: body=response.json()
                except ValueError: body=response.text
                out.append({'status':response.status_code,'body':body})
            return out
def _case(requests):
    executions.clear()
    responses=_drive(_requests(app,[('GET','/orders',{'params':{'request':str(i)}}) for i in range(requests)]))
    assert len(executions)==requests
    assert len({id(x) for x in executions})==requests
    assert all(r=={'status':200,'body':{'same_instance':True}} for r in responses)
    return {'responses':responses,'provider_executions':len(executions),'distinct_values':len({id(x) for x in executions})}
import inspect
from fastapi import FastAPI, Body
verification_app=FastAPI()

async def verify_case(payload: dict=Body(...)):
    result=_case(payload['case'])
    if inspect.isawaitable(result):return await result
    return result
verify_case = verification_app.post('/_verify')(verify_case)

  test test_1 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":1}}],"app":"verification_app","expected":{"status":200,"json":{"responses":[{"status":200,"body":{"same_instance":true}}],"provider_executions":1,"distinct_values":1}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  test test_2 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":2}}],"app":"verification_app","expected":{"status":200,"json":{"responses":[{"status":200,"body":{"same_instance":true}},{"status":200,"body":{"same_instance":true}}],"provider_executions":2,"distinct_values":2}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"b6f92e6ce24bcc191cbb6df9ccf61e2b89cd582680c4f82b914021ae229f8309","tests_passed":2}
  feedback✔: You applied the declared boundary and preserved its required behavior.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Compare each declaration with its input or lifecycle boundary.', 'Trace what happens on the alternative input or exit, not only the successful path.']
  MEASURES: A:predict_shared_dependency_reuse_within_one_request(f1)   anchors=['practice', 'assessment:predict_shared_dependency_reuse_within_one_request']
  taught-before-tested: A.f1←s01

### s06 · explainer · Declare the boundary: Endpoint integration tests using TestClient or async HTTPX as appropriate
Explainer — 
(mechanism) Create TestClient(app), send a request such as client.get(...), and assert both response.status_code and response.json() in a pytest test_ function. ⟦B.f1 B:tb1 B:tb2⟧
(mechanism) When setup and teardown matter, use with TestClient(app) as client to execute application lifespan. ⟦B.f2 B:tb3⟧
(mechanism) A TestClient request exercises route and dependency resolution through the application. Calling the handler directly does not exercise that HTTP boundary. ⟦B.f3 B:tb3⟧
[CODE python]
from fastapi.testclient import TestClient
from app import app

def test_get_order():
    with TestClient(app) as client:
        response = client.get('/orders/42')
        assert response.status_code == 200
        assert response.json() == {'id': 42, 'quantity': 2}

  annotations: ['Context runs lifespan setup and teardown.', 'HTTP request exercises routing and dependency resolution.', 'Independent status and public JSON assertions; pytest executes test_get_order.']

### s07 · explainer · Trace the contract
Explainer — 
(mental_model) Specify an HTTP exchange, not merely a call that avoids crashing: method, path, expected status and expected public JSON. TestClient sends it through route and dependency resolution. Add the context manager when lifespan setup and teardown belong in the test. A direct handler call checks a different boundary and cannot establish the registered endpoint’s complete exchange. ⟦B.f1 B.f2 B.f3 B:tb4⟧

### s08 · explainer · Work through the supplied example
Explainer — 
(walkthrough) Use the supplied order fixture to make separate status and JSON assertions in test_get_order. Send the GET through TestClient rather than invoking get_order directly. Run the test_ function with pytest; use the context manager to execute lifespan when the case needs it. The status assertion checks the HTTP outcome, and the JSON assertion checks public content. Neither substitutes for the other. ⟦B.f1 B.f2 B.f3 B:tb5 B:tb6⟧

### s09 · video · Optional deeper walkthrough
Video — 
[VIDEO Verify an endpoint's HTTP response] bridge-before: Watch how TestClient sends a GET request and how separate status and JSON assertions define the expected response. Notice how changing the response makes the test fail. | bridge-after: The clip demonstrates request and response assertions, but does not explain lifespan execution or dependency resolution. The text covers both, including when to use the TestClient context manager.
  - 9gC3Ot0LoUQ 327-429s facts=['f1'] label: Send a TestClient request and assert status and JSON | summary: An endpoint test imports TestClient and the application, creates a client, and sends a GET request from a test function. It checks that the response status is 200 and the decoded JSON equals the string "server is running". Running pytest produces a passing test. Adding an exclamation mark to the endpoint's response makes the same test fail, demonstrating that the payload assertion detects a changed response. The original response is then restored.

### s10 · check · Check the boundary: Endpoint integration tests using TestClient or async HTTPX as appropriate
Check — Use the supplied order-service scenario to reason about this contract.
QUESTION [choice, core, grading=client] Which test exercises the application's HTTP route and dependency resolution instead of only directly calling its handler?
  ✔ option_1: Send the request through TestClient(app).
      why: A TestClient request traverses the application route and dependency resolution.
  ✘ option_2: Call the handler as an ordinary function without sending a request.
      why: A direct call does not establish the HTTP route and dependency resolution boundary.
  ✘ option_3: Read the handler function source without sending a request.
      why: Source inspection alone is not an HTTP request through the application.
  feedback✔: A TestClient request traverses the application route and dependency resolution.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Separate the stated requirement from a nearby but different boundary.']  remediation→r04
  MEASURES: B:distinguish_http_route_and_dependency_resolution_from_direct_handler_calls(f3)   anchors=['assessment:distinguish_http_route_and_dependency_resolution_from_direct_handler_calls']
  taught-before-tested: B.f3←s06

### s11 · hands_on · Apply the contract: Endpoint integration tests using TestClient or async HTTPX as appropriate
Hands On — Complete the supplied workspace within its stated contract.
QUESTION [code_exercise, stretch, grading=client] Write def test_get_order() using with TestClient(app) as client. Send GET /orders/42; independently assert response.status_code == 200 and response.json() == {"id": 42, "quantity": 2}. The supplied WASM adapter preserves the TestClient API and traverses the real ASGI app without threads, including lifespan. The verification harness calls the discoverable test twice and checks setup/teardown; run pytest on this test in a native environment for discovery verification.
  runtime={'kind': 'python_asgi', 'version': '0.29.5'} constraints.allowed=['from fastapi.testclient import TestClient', 'def test_get_order():', 'with TestClient(app) as client:', 'response = client.get("/orders/42")', 'assert response.status_code == 200', 'assert response.json() == {"id": 42, "quantity": 2}'] blocked=8 items
  file exercise.py [editable]:
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
lifecycle_events = []

# Supplied harness scaffolding (unchanged in the solution).
if True:
    async def lifespan(app):
        lifecycle_events.append('setup')
        try:
            yield
        finally:
            lifecycle_events.append('teardown')
lifespan = asynccontextmanager(lifespan)
app = FastAPI(lifespan=lifespan)
# Supplied harness scaffolding (unchanged in the solution).
if True:
    def order_dependency():
        return {'id': 42, 'quantity': 2}
# Supplied harness scaffolding (unchanged in the solution).
if True:
    @app.get('/orders/42')
    def get_order(order=Depends(order_dependency)):
        return order
import asyncio, inspect, json, ast
import httpx
from contextlib import contextmanager

# Supplied harness scaffolding (unchanged in the solution).
if True:
    def _drive(coro):
        try:
            pending = coro.send(None)
        except StopIteration as done:
            return done.value
        raise RuntimeError('Harness encountered a suspending operation: ' + repr(pending))

# Supplied harness scaffolding (unchanged in the solution).
if True:
    async def _requests(application, requests):
        async with application.router.lifespan_context(application):
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application, raise_app_exceptions=False), base_url='http://testserver') as client:
                out=[]
                for method,path,kwargs in requests:
                    response=await client.request(method,path,**kwargs)
                    try: body=response.json()
                    except ValueError: body=response.text
                    out.append({'status':response.status_code,'body':body})
                return out
from fastapi.testclient import TestClient
# Supplied harness scaffolding (unchanged in the solution).
if True:
    class _InlineTransport(httpx.BaseTransport):
        def __init__(self,application):self.application=application
        def handle_request(self,request):
            response=_drive(self._handle(request))
            return httpx.Response(response.status_code,headers=response.headers,content=response.content,request=request)
        async def _handle(self,request):
            transport=httpx.ASGITransport(app=self.application)
            async with httpx.AsyncClient(transport=transport) as c:
                return await c.send(request)
# Supplied harness scaffolding (unchanged in the solution).
if True:
    def _client_init(self,application,**kwargs):
        self.app=application
        httpx.Client.__init__(self,transport=_InlineTransport(application),base_url='http://testserver',follow_redirects=True)
# Supplied harness scaffolding (unchanged in the solution).
if True:
    def _client_enter(self):
        self._lifespan=self.app.router.lifespan_context(self.app)
        _drive(self._lifespan.__aenter__())
        return self
# Supplied harness scaffolding (unchanged in the solution).
if True:
    def _client_exit(self,*exc):
        _drive(self._lifespan.__aexit__(*exc));self.close()
TestClient.__init__=_client_init
TestClient.__enter__=_client_enter
TestClient.__exit__=_client_exit
from fastapi.testclient import TestClient
# TODO: write test_get_order with a TestClient context manager,
# GET /orders/42, and independent status and JSON assertions.
# Supplied harness scaffolding (unchanged in the solution).
if True:
    def _case(repetitions):
        lifecycle_events.clear()
        source=inspect.getsource(test_get_order)
        tree=ast.parse(source)
        assert sum(isinstance(n,ast.Assert) for n in ast.walk(tree))>=2
        assert any(isinstance(n,ast.With) for n in ast.walk(tree))
        for _ in range(repetitions):test_get_order()
        assert lifecycle_events==['setup','teardown']*repetitions
        return {'test_name':test_get_order.__name__,'runs':repetitions,'lifespan_events':list(lifecycle_events)}
import inspect
from fastapi import FastAPI, Body
verification_app=FastAPI()

# Supplied harness scaffolding (unchanged in the solution).
if True:
    async def verify_case(payload: dict=Body(...)):
        result=_case(payload['case'])
        if inspect.isawaitable(result):return await result
        return result
verify_case = verification_app.post('/_verify')(verify_case)

  SOLUTION exercise.py:
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
lifecycle_events = []

# Supplied harness scaffolding (unchanged in the solution).
if True:
    async def lifespan(app):
        lifecycle_events.append('setup')
        try:
            yield
        finally:
            lifecycle_events.append('teardown')
lifespan = asynccontextmanager(lifespan)
app = FastAPI(lifespan=lifespan)
# Supplied harness scaffolding (unchanged in the solution).
if True:
    def order_dependency():
        return {'id': 42, 'quantity': 2}
# Supplied harness scaffolding (unchanged in the solution).
if True:
    @app.get('/orders/42')
    def get_order(order=Depends(order_dependency)):
        return order
import asyncio, inspect, json, ast
import httpx
from contextlib import contextmanager

# Supplied harness scaffolding (unchanged in the solution).
if True:
    def _drive(coro):
        try:
            pending = coro.send(None)
        except StopIteration as done:
            return done.value
        raise RuntimeError('Harness encountered a suspending operation: ' + repr(pending))

# Supplied harness scaffolding (unchanged in the solution).
if True:
    async def _requests(application, requests):
        async with application.router.lifespan_context(application):
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application, raise_app_exceptions=False), base_url='http://testserver') as client:
                out=[]
                for method,path,kwargs in requests:
                    response=await client.request(method,path,**kwargs)
                    try: body=response.json()
                    except ValueError: body=response.text
                    out.append({'status':response.status_code,'body':body})
                return out
from fastapi.testclient import TestClient
# Supplied harness scaffolding (unchanged in the solution).
if True:
    class _InlineTransport(httpx.BaseTransport):
        def __init__(self,application):self.application=application
        def handle_request(self,request):
            response=_drive(self._handle(request))
            return httpx.Response(response.status_code,headers=response.headers,content=response.content,request=request)
        async def _handle(self,request):
            transport=httpx.ASGITransport(app=self.application)
            async with httpx.AsyncClient(transport=transport) as c:
                return await c.send(request)
# Supplied harness scaffolding (unchanged in the solution).
if True:
    def _client_init(self,application,**kwargs):
        self.app=application
        httpx.Client.__init__(self,transport=_InlineTransport(application),base_url='http://testserver',follow_redirects=True)
# Supplied harness scaffolding (unchanged in the solution).
if True:
    def _client_enter(self):
        self._lifespan=self.app.router.lifespan_context(self.app)
        _drive(self._lifespan.__aenter__())
        return self
# Supplied harness scaffolding (unchanged in the solution).
if True:
    def _client_exit(self,*exc):
        _drive(self._lifespan.__aexit__(*exc));self.close()
TestClient.__init__=_client_init
TestClient.__enter__=_client_enter
TestClient.__exit__=_client_exit
from fastapi.testclient import TestClient
# TODO: write test_get_order with a TestClient context manager,
# GET /orders/42, and independent status and JSON assertions.
def test_get_order():
    with TestClient(app) as client:
        response = client.get("/orders/42")
        assert response.status_code == 200
        assert response.json() == {"id": 42, "quantity": 2}
# Supplied harness scaffolding (unchanged in the solution).
if True:
    def _case(repetitions):
        lifecycle_events.clear()
        source=inspect.getsource(test_get_order)
        tree=ast.parse(source)
        assert sum(isinstance(n,ast.Assert) for n in ast.walk(tree))>=2
        assert any(isinstance(n,ast.With) for n in ast.walk(tree))
        for _ in range(repetitions):test_get_order()
        assert lifecycle_events==['setup','teardown']*repetitions
        return {'test_name':test_get_order.__name__,'runs':repetitions,'lifespan_events':list(lifecycle_events)}
import inspect
from fastapi import FastAPI, Body
verification_app=FastAPI()

# Supplied harness scaffolding (unchanged in the solution).
if True:
    async def verify_case(payload: dict=Body(...)):
        result=_case(payload['case'])
        if inspect.isawaitable(result):return await result
        return result
verify_case = verification_app.post('/_verify')(verify_case)

  test test_1 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":1}}],"app":"verification_app","expected":{"status":200,"json":{"test_name":"test_get_order","runs":1,"lifespan_events":["setup","teardown"]}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  test test_2 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":2}}],"app":"verification_app","expected":{"status":200,"json":{"test_name":"test_get_order","runs":2,"lifespan_events":["setup","teardown","setup","teardown"]}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"875fea5ad974066baeda4b17af20c3798bdc3c3bc865ca2bd9b63a3b4a6bd005","tests_passed":2}
  feedback✔: You applied the declared boundary and preserved its required behavior.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Compare each declaration with its input or lifecycle boundary.', 'Trace what happens on the alternative input or exit, not only the successful path.']
  MEASURES: B:assert_endpoint_status_and_json_payload(f1); B:include_application_lifespan_in_test_boundary(f2)   anchors=['practice', 'assessment:assert_endpoint_status_and_json_payload', 'assessment:include_application_lifespan_in_test_boundary']
  taught-before-tested: B.f1←s06; B.f2←s06

### s12 · recap · Keep these distinctions
Recap — 
(takeaway) Verify request-local reuse, check a fresh request independently, and request fresh execution with use_cache=False when needed. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Use a pytest test_ function to request the HTTP endpoint and assert status plus JSON; include lifespan through the TestClient context when needed. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧
[UP NEXT] Next: tile_047 — Required, optional and default input semantics: Start with Required, optional and default input semantics.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Request-scoped dependency reuse and lifetime
(definition) Use Depends(provider, use_cache=False) on a declaration that needs fresh execution instead of the cached result. ⟦A.f2 A:tb3 A:tb4⟧
(example) For a dependant needing a fresh provider execution, use_cache=False differs from relying on the normally cached result. ⟦A.f2 A:tb3 A:tb4⟧
### r02 · Try the contrast: Request-scoped dependency reuse and lifetime
(definition) Check that two dependants receive the same provider result in one request, then examine a fresh request independently. This cache is request-local, not application-wide storage. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) The order provider can reuse a result inside request A without making that result application-wide storage for request B. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r03 · Try the contrast: Request-scoped dependency reuse and lifetime
(definition) FastAPI normally caches a dependency result within a request when several dependants declare the same dependency. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(example) Within one order request, multiple dependants declaring the same provider normally reuse its returned value rather than requiring repeated execution. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
### r04 · Try the contrast: Endpoint integration tests using TestClient or async HTTPX as appropriate
(definition) A TestClient request exercises route and dependency resolution through the application. Calling the handler directly does not exercise that HTTP boundary. ⟦B.f3 B:tb3 B:tb4 B:tb5 B:tb6⟧
(example) For order retrieval, an HTTP request through TestClient differs from a direct call to get_order. ⟦B.f3 B:tb3 B:tb4 B:tb5 B:tb6⟧
### r05 · Try the contrast: Endpoint integration tests using TestClient or async HTTPX as appropriate
(definition) Create TestClient(app), send a request such as client.get(...), and assert both response.status_code and response.json() in a pytest test_ function. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(definition) When setup and teardown matter, use with TestClient(app) as client to execute application lifespan. ⟦B.f2 B:tb3 B:tb4 B:tb5 B:tb6⟧
(example) For the supplied order test, an HTTP status assertion does not substitute for the JSON assertion; use the TestClient context when lifespan must run. ⟦B.f1 B.f2 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: httpx.AsyncClient(...)
· constraints.blocked_syntax: @app.exception_handler
· constraints.blocked_syntax: session.execute(...)

=========

# EVALUATOR PACKET — Required, optional and default input semantics · FastAPI OpenAPI generation from typed route contracts (tile_047)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.input_presence_defaults — Required, optional and default input semantics
B = fastapi.openapi_generation — FastAPI OpenAPI generation from typed route contracts

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: remediation step tile_047.r02 is never referenced
  warn: remediation step tile_047.r04 is never referenced

## SOURCE FACTS — A (fastapi.input_presence_defaults)   objective: Define required, nullable and default inputs: test omitted, null and concrete values for one input.
A.f1: Requiredness depends on whether a declaration supplies a default, while nullability depends on whether its type admits None.   [sources: pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/fields/#default-values, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/body/#request-body-path-query-parameters]
A.f2: A nullable field without a default still requires presence; writing field: Type | None = None permits both omission and an explicit null.   [sources: pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/fields/#default-values]
A.f3: Test absence, an explicit JSON null and a concrete value as separate requests and compare them with the field's declared default and nullable type.   [sources: pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/models/#basic-model-usage, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/testing/#using-testclient]
note: Establish this first: Presence and nullability are independent contract dimensions.
note: Stay within the current objective: Define required, nullable and default inputs. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Distinguish omission from explicit null and supplied values.
PRACTICE ANCHOR (live_code): Test three separate request bodies for note: an omitted field, explicit JSON null and a concrete string. Compare the results for note: str | None and note: str | None = None.  SUCCESS: Tests establish that the declaration without a default requires note to be present but accepts null or a string, while the declaration defaulting to None accepts all three inputs and uses None when note is omitted.
ASSESSMENT ANCHOR: distinguish_requiredness_from_nullability facts=['f1', 'f2']
ASSESSMENT ANCHOR: compare_omitted_null_and_concrete_inputs facts=['f2', 'f3']

## SOURCE FACTS — B (fastapi.openapi_generation)   objective: Generate OpenAPI from declarations: inspect one endpoint schema.
B.f1: FastAPI normally exposes the generated OpenAPI document at /openapi.json, describing the application's operations and data schemas.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/first-steps/#check-the-openapi-json]
B.f2: Typed body declarations and response models contribute input and output schemas to the generated API contract.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/body/#results, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/response-model/#response-model-parameter]
B.f3: Inspect the method entry under paths for an endpoint and follow its schema references into components to see the generated public input and output definitions.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/first-steps/#check-the-openapi-json]
note: Establish this first: Executable declarations drive generated contracts.
note: Stay within the current objective: Generate OpenAPI from declarations. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify generated input and output schemas.
PRACTICE ANCHOR (live_code): Inspect the supplied POST /orders contract, trace its request-body and response schema references, and assign the corresponding component definitions to OrderInput and OrderOutput.  SUCCESS: OrderInput refers to the component definition containing required integer quantity, and OrderOutput refers to the component definition containing required integer id. Both selections agree with the references under paths → /orders → post.
ASSESSMENT ANCHOR: locate_generated_openapi_document facts=['f1']
ASSESSMENT ANCHOR: identify_declaration_sources_for_input_and_output_schemas facts=['f2']
ASSESSMENT ANCHOR: trace_operation_references_to_input_and_output_definitions facts=['f3']

## DATA ASSETS USED
ds.orders: Synthetic order retrieval fixture — columns: id(identifier,digits-as-label), quantity(numerical)
   [42,2]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Consistent public error envelopes through exception handlers; Credential and sensitive-data redaction from emitted logs; Distinct create and partial-update contracts; FastAPI OpenAPI generation from typed route contracts; Graceful termination and shutdown verification; Header and cookie input binding; Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels; Keeping API schemas distinct from persistence entities; Meaningful contract examples and operation metadata; Proxy header trust; Redis cache-aside selection and population; Request correlation context across service logs; Request-scoped async-compatible PostgreSQL session lifecycle; Request-validation error behavior; Retrieve resource; Service health and readiness checks; Test dependency replacement; Transaction commit and rollback boundaries; 

## LESSON, in learner order

### s01 · explainer · Declare the boundary: Required, optional and default input semantics
Explainer — 
(mechanism) A default determines requiredness; a type that admits None determines nullability. These are different questions. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) A nullable field with no default still requires presence. field: Type | None = None allows both omission and explicit null. ⟦A.f2 A:tb3⟧
(mechanism) Send absence, explicit JSON null and a concrete value as separate requests. Compare each with the declared default and nullable type. ⟦A.f3 A:tb3⟧
[TABLE computed result ] caption: Declaration comparison derived from the presence rule and supplied request bodies, not an HTTP run. Read resulting_note only where accepted is true.
  produced by sql: WITH inputs(ordinal, supplied, note) AS (VALUES (1,FALSE,NULL),(2,TRUE,NULL),(3,TRUE,'Leave at reception')), declarations(label, has_default) AS (VALUES ('note: str | None', FALSE), ('note: str | None = None', TRUE))
SELECT CASE WHEN NOT supplied THEN 'omitted' WHEN note IS NULL THEN 'explicit null' ELSE 'concrete string' END AS input,
 label AS declaration, (supplied OR has_default) AS accepted,
 CASE WHEN supplied OR has_default THEN note ELSE NULL END AS resulting_note
FROM orders CROSS JOIN inputs CROSS JOIN declarations ORDER BY ordinal, has_default
  result columns=['input', 'declaration', 'accepted', 'resulting_note'] rows(6)=[["omitted","note: str | None",false,null],["omitted","note: str | None = None",true,null],["explicit null","note: str | None",true,null],["explicit null","note: str | None = None",true,null],["concrete string","note: str | None",true,"Leave at reception"],["concrete string","note: str | None = None",true,"Leave at reception"]]

### s02 · explainer · Trace the contract
Explainer — 
(mental_model) Keep two columns in your mental model: must the field appear, and may its value be null? note: str | None requires presence but admits null. Adding = None allows omission too. Test missing, null and a concrete string separately against those declarations; “optional” alone does not identify both rules. ⟦A.f1 A.f2 A.f3 A:tb4⟧

### s03 · explainer · Work through the supplied example
Explainer — 
(walkthrough) Start with the supplied nullable note declaration, then add its default. Send each supplied body separately before and after the change. Without a default, the field must appear even though null is allowed; with = None, omission is also allowed. Compare the declared presence rule with the admitted values instead of collapsing all three requests into one optional case. ⟦A.f1 A.f2 A.f3 A:tb5 A:tb6⟧

### s04 · check · Check the boundary: Required, optional and default input semantics
Check — Use the supplied order-service scenario to reason about this contract.
QUESTION [choice, intro, grading=client] A Pydantic field is declared note: str | None with no default. Which input boundary follows?
  ✔ option_1: The field must be present, but its value may be null or a string.
      why: Nullability and requiredness are different: no default still requires presence.
  ✘ option_2: The field may be omitted because its type accepts None.
      why: A nullable type without a default does not make omission acceptable.
  ✘ option_3: The field must be present and may never be null.
      why: The union with None explicitly permits null.
  feedback✔: Nullability and requiredness are different: no default still requires presence.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Separate the stated requirement from a nearby but different boundary.']  remediation→r01
  MEASURES: A:distinguish_requiredness_from_nullability(f1,f2)   anchors=['assessment:distinguish_requiredness_from_nullability']
  taught-before-tested: A.f1←s01; A.f2←s01

### s05 · hands_on · Apply the contract: Required, optional and default input semantics
Hands On — Complete the supplied workspace within its stated contract.
QUESTION [code_exercise, core, grading=client] Write test_required_note for app (note: str | None without a default) and test_default_note for default_app (note: str | None = None). For each, send three separate POST /orders/note requests with {}, {'note': None}, and {'note': 'Leave at reception'}. Assert omitted input returns 422 for app but 200 and {'note': None} for default_app; both declarations accept null and the string with 200 and the corresponding JSON payload. Preserve the supplied declarations. The threadless TestClient adapter uses the actual ASGI app.
  runtime={'kind': 'python_asgi', 'version': '0.29.5'} constraints.allowed=['from pydantic import BaseModel', 'from fastapi import FastAPI', 'from fastapi.testclient import TestClient', 'class declarations inheriting from BaseModel', 'note: str | None', 'note: str | None = None', 'app = FastAPI()', '@app.post(...)', 'def path-operation functions with typed request-model parameters', 'request-model instance attribute access', 'return statements', 'dictionary literals containing only the note field', 'empty dictionary literals', 'string literals', 'None', 'client = TestClient(app)', 'client.post(..., json=...)', 'response.status_code', 'response.json()', 'assert statements', 'equality comparisons'] blocked=8 items
  file exercise.py [editable]:
import asyncio, inspect, json, ast
import httpx
from contextlib import contextmanager

def _drive(coro):
    try:
        pending = coro.send(None)
    except StopIteration as done:
        return done.value
    raise RuntimeError('Harness encountered a suspending operation: ' + repr(pending))

async def _requests(application, requests):
    async with application.router.lifespan_context(application):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application, raise_app_exceptions=False), base_url='http://testserver') as client:
            out=[]
            for method,path,kwargs in requests:
                response=await client.request(method,path,**kwargs)
                try: body=response.json()
                except ValueError: body=response.text
                out.append({'status':response.status_code,'body':body})
            return out
from fastapi.testclient import TestClient
class _InlineTransport(httpx.BaseTransport):
    def __init__(self,application):self.application=application
    def handle_request(self,request):
        response=_drive(self._handle(request))
        return httpx.Response(response.status_code,headers=response.headers,content=response.content,request=request)
    async def _handle(self,request):
        transport=httpx.ASGITransport(app=self.application)
        async with httpx.AsyncClient(transport=transport) as c:
            return await c.send(request)
def _client_init(self,application,**kwargs):
    self.app=application
    httpx.Client.__init__(self,transport=_InlineTransport(application),base_url='http://testserver',follow_redirects=True)
def _client_enter(self):
    self._lifespan=self.app.router.lifespan_context(self.app)
    _drive(self._lifespan.__aenter__())
    return self
def _client_exit(self,*exc):
    _drive(self._lifespan.__aexit__(*exc));self.close()
TestClient.__init__=_client_init
TestClient.__enter__=_client_enter
TestClient.__exit__=_client_exit
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.testclient import TestClient
class NoteInput(BaseModel):
    note: str | None
app = FastAPI()
@app.post('/orders/note')
def set_note(body: NoteInput):
    return {'note': body.note}
class DefaultNoteInput(BaseModel):
    note: str | None = None
default_app = FastAPI()
@default_app.post('/orders/note')
def default_note(body: DefaultNoteInput): return {'note':body.note}
# TODO: write test_required_note and test_default_note, each with separate
# omitted, null and concrete-value requests and status/payload assertions.
def _case(which):
    test = test_required_note if which=='required' else test_default_note
    assert sum(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(inspect.getsource(test))))>=5
    test()
    application=app if which=='required' else default_app
    return _drive(_requests(application,[('POST','/orders/note',{'json':j}) for j in ({},{'note':None},{'note':'Leave at reception'})]))
import inspect
from fastapi import FastAPI, Body
verification_app=FastAPI()

async def verify_case(payload: dict=Body(...)):
    result=_case(payload['case'])
    if inspect.isawaitable(result):return await result
    return result
verify_case = verification_app.post('/_verify')(verify_case)

  SOLUTION exercise.py:
import asyncio, inspect, json, ast
import httpx
from contextlib import contextmanager

def _drive(coro):
    try:
        pending = coro.send(None)
    except StopIteration as done:
        return done.value
    raise RuntimeError('Harness encountered a suspending operation: ' + repr(pending))

async def _requests(application, requests):
    async with application.router.lifespan_context(application):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application, raise_app_exceptions=False), base_url='http://testserver') as client:
            out=[]
            for method,path,kwargs in requests:
                response=await client.request(method,path,**kwargs)
                try: body=response.json()
                except ValueError: body=response.text
                out.append({'status':response.status_code,'body':body})
            return out
from fastapi.testclient import TestClient
class _InlineTransport(httpx.BaseTransport):
    def __init__(self,application):self.application=application
    def handle_request(self,request):
        response=_drive(self._handle(request))
        return httpx.Response(response.status_code,headers=response.headers,content=response.content,request=request)
    async def _handle(self,request):
        transport=httpx.ASGITransport(app=self.application)
        async with httpx.AsyncClient(transport=transport) as c:
            return await c.send(request)
def _client_init(self,application,**kwargs):
    self.app=application
    httpx.Client.__init__(self,transport=_InlineTransport(application),base_url='http://testserver',follow_redirects=True)
def _client_enter(self):
    self._lifespan=self.app.router.lifespan_context(self.app)
    _drive(self._lifespan.__aenter__())
    return self
def _client_exit(self,*exc):
    _drive(self._lifespan.__aexit__(*exc));self.close()
TestClient.__init__=_client_init
TestClient.__enter__=_client_enter
TestClient.__exit__=_client_exit
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.testclient import TestClient
class NoteInput(BaseModel):
    note: str | None
app = FastAPI()
@app.post('/orders/note')
def set_note(body: NoteInput):
    return {'note': body.note}
class DefaultNoteInput(BaseModel):
    note: str | None = None
default_app = FastAPI()
@default_app.post('/orders/note')
def default_note(body: DefaultNoteInput): return {'note':body.note}
# TODO: write test_required_note and test_default_note, each with separate
# omitted, null and concrete-value requests and status/payload assertions.
def test_required_note():
    client = TestClient(app)
    response = client.post('/orders/note', json={})
    assert response.status_code == 422
    response = client.post('/orders/note', json={'note': None})
    assert response.status_code == 200
    assert response.json() == {'note': None}
    response = client.post('/orders/note', json={'note': 'Leave at reception'})
    assert response.status_code == 200
    assert response.json() == {'note': 'Leave at reception'}
def test_default_note():
    client = TestClient(default_app)
    response = client.post('/orders/note', json={})
    assert response.status_code == 200
    assert response.json() == {'note': None}
    response = client.post('/orders/note', json={'note': None})
    assert response.status_code == 200
    assert response.json() == {'note': None}
    response = client.post('/orders/note', json={'note': 'Leave at reception'})
    assert response.status_code == 200
    assert response.json() == {'note': 'Leave at reception'}
def _case(which):
    test = test_required_note if which=='required' else test_default_note
    assert sum(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(inspect.getsource(test))))>=5
    test()
    application=app if which=='required' else default_app
    return _drive(_requests(application,[('POST','/orders/note',{'json':j}) for j in ({},{'note':None},{'note':'Leave at reception'})]))
import inspect
from fastapi import FastAPI, Body
verification_app=FastAPI()

async def verify_case(payload: dict=Body(...)):
    result=_case(payload['case'])
    if inspect.isawaitable(result):return await result
    return result
verify_case = verification_app.post('/_verify')(verify_case)

  test test_1 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"required"}}],"app":"verification_app","expected":{"status":200,"json":[{"status":422,"body":{"detail":[{"type":"missing","loc":["body","note"],"msg":"Field required","input":{}}]}},{"status":200,"body":{"note":null}},{"status":200,"body":{"note":"Leave at reception"}}]}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  test test_2 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"default"}}],"app":"verification_app","expected":{"status":200,"json":[{"status":200,"body":{"note":null}},{"status":200,"body":{"note":null}},{"status":200,"body":{"note":"Leave at reception"}}]}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"0fbcc85413a953d8d486dc6c8d43127ef4fdd9bc9f8a624d345fc373494b3ef2","tests_passed":2}
  feedback✔: You applied the declared boundary and preserved its required behavior.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Compare each declaration with its input or lifecycle boundary.', 'Trace what happens on the alternative input or exit, not only the successful path.']
  MEASURES: A:compare_omitted_null_and_concrete_inputs(f2,f3)   anchors=['practice', 'assessment:compare_omitted_null_and_concrete_inputs']
  taught-before-tested: A.f2←s01; A.f3←s01

### s06 · explainer · Declare the boundary: FastAPI OpenAPI generation from typed route contracts
Explainer — 
(mechanism) FastAPI normally serves the generated OpenAPI document at /openapi.json. It describes operations and data schemas. ⟦B.f1 B:tb1 B:tb2⟧
(mechanism) Typed body declarations contribute input schemas; response models contribute output schemas to the generated public contract. ⟦B.f2 B:tb3⟧
(mechanism) Locate the endpoint’s method entry under paths, then follow its schema references into components to find the public input and output definitions. ⟦B.f3 B:tb3⟧
[CODE python]
import json
schema = {'paths': {'/orders': {'post': {'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/OrderInput'}}}},
                                'responses': {'200': {'description': 'Successful '
                                                                     'Response',
                                                      'content': {'application/json': {'schema': {'$ref': '#/components/schemas/OrderOutput'}}}}}}}},
 'components': {'schemas': {'OrderInput': {'type': 'object',
                                           'properties': {'quantity': {'type': 'integer'}},
                                           'required': ['quantity']},
                            'OrderOutput': {'type': 'object',
                                            'properties': {'id': {'type': 'integer'}},
                                            'required': ['id']}}}}
print(json.dumps(schema, indent=2))

  annotations: ['POST /orders: requestBody reference → components.schemas.OrderInput; response reference → OrderOutput. quantity is input, id is output.']

### s07 · explainer · Trace the contract
Explainer — 
(mental_model) Navigate by endpoint path and method first. Follow the body and response references into components, then compare their field definitions with the typed declarations. OpenAPI is generated from those declarations; it describes operations and schemas. Reading the document does not establish every runtime outcome, and schema details need not be inline in the operation entry. ⟦B.f1 B.f2 B.f3 B:tb4⟧

### s08 · explainer · Work through the supplied example
Explainer — 
(walkthrough) In the supplied POST /orders excerpt, follow the request-body reference to OrderInput and the response reference to OrderOutput. The input definition has quantity; the output definition has id. These are different public definitions contributed by the body and response-model declarations. Retrieve the generated document at /openapi.json and navigate through paths and components rather than assuming every field is inline. This is contract structure, not proof of every runtime result. ⟦B.f1 B.f2 B.f3 B:tb5 B:tb6⟧

### s09 · check · Check the boundary: FastAPI OpenAPI generation from typed route contracts
Check — Use the supplied order-service scenario to reason about this contract.
QUESTION [choice, core, grading=client] At which endpoint does FastAPI normally expose its generated OpenAPI document?
  ✘ option_3: Only in a request body submitted by a client.
      why: The application exposes the generated document at /openapi.json; it is not merely client-submitted content.
  ✔ option_1: /openapi.json.
      why: This is the normal document endpoint.
  ✘ option_2: Inside the ordinary order response payload only.
      why: The generated contract is normally exposed separately at /openapi.json.
  feedback✔: This is the normal document endpoint.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Separate the stated requirement from a nearby but different boundary.']  remediation→r03
  MEASURES: B:locate_generated_openapi_document(f1)   anchors=['assessment:locate_generated_openapi_document']
  taught-before-tested: B.f1←s06

### s10 · hands_on · Apply the contract: FastAPI OpenAPI generation from typed route contracts
Hands On — Complete the supplied workspace within its stated contract.
QUESTION [code_exercise, stretch, grading=client] Inspect schema['paths']['/orders']['post']. Assign input_reference to the requestBody application/json schema $ref and output_reference to the 200 response application/json schema $ref. Follow these shown component names into schema['components']['schemas']; assign OrderInput and OrderOutput to the complete definition dictionaries, not $ref strings. Include each corresponding reference and definition in the named variables. Preserve supplied schema fixtures.
  runtime={'kind': 'python_asgi', 'version': '0.29.5'} constraints.allowed=['Variable assignment', 'Dictionary subscription with string keys', 'String literals'] blocked=5 items
  file exercise.py [editable]:
input_field_type = 'integer'
output_field_type = 'integer'
schema = {'paths': {'/orders': {'post': {'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/OrderInput'}}}}, 'responses': {'200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/OrderOutput'}}}}}}}}, 'components': {'schemas': {'OrderInput': {'type': 'object', 'properties': {'quantity': {'type': 'integer'}}, 'required': ['quantity']}, 'OrderOutput': {'type': 'object', 'properties': {'id': {'type': 'integer'}}, 'required': ['id']}}}}
# Supplied schema fixture variations; do not edit this scaffolding.
schema['components']['schemas']['OrderInput']['properties']['quantity']['type'] = input_field_type
schema['components']['schemas']['OrderOutput']['properties']['id']['type'] = output_field_type
# TODO: select the POST operation, inspect its request/response references,
# and assign component definitions (not reference strings).

  SOLUTION exercise.py:
input_field_type = 'integer'
output_field_type = 'integer'
schema = {'paths': {'/orders': {'post': {'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/OrderInput'}}}}, 'responses': {'200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/OrderOutput'}}}}}}}}, 'components': {'schemas': {'OrderInput': {'type': 'object', 'properties': {'quantity': {'type': 'integer'}}, 'required': ['quantity']}, 'OrderOutput': {'type': 'object', 'properties': {'id': {'type': 'integer'}}, 'required': ['id']}}}}
# Supplied schema fixture variations; do not edit this scaffolding.
schema['components']['schemas']['OrderInput']['properties']['quantity']['type'] = input_field_type
schema['components']['schemas']['OrderOutput']['properties']['id']['type'] = output_field_type
# TODO: select the POST operation, inspect its request/response references,
# and assign component definitions (not reference strings).
operation = schema['paths']['/orders']['post']
input_reference = operation['requestBody']['content']['application/json']['schema']['$ref']
output_reference = operation['responses']['200']['content']['application/json']['schema']['$ref']
OrderInput = schema['components']['schemas']['OrderInput']
OrderOutput = schema['components']['schemas']['OrderOutput']

  test test_1 (value_equals, visible=True): {"expr":"{'reference': input_reference, 'definition': OrderInput}","expected":{"reference":"#/components/schemas/OrderInput","definition":{"type":"object","properties":{"quantity":{"type":"integer"}},"required":["quantity"]}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  test test_2 (value_equals, visible=True): {"expr":"{'reference': output_reference, 'definition': OrderOutput}","expected":{"reference":"#/components/schemas/OrderOutput","definition":{"type":"object","properties":{"id":{"type":"integer"}},"required":["id"]}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"28f462cf370659a80e95e0216aad9c6f8e7a88a2ee4cbcd4ac53d139afb1d63e","tests_passed":2}
  feedback✔: You applied the declared boundary and preserved its required behavior.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Compare each declaration with its input or lifecycle boundary.', 'Trace what happens on the alternative input or exit, not only the successful path.']
  MEASURES: B:identify_declaration_sources_for_input_and_output_schemas(f2); B:trace_operation_references_to_input_and_output_definitions(f3)   anchors=['practice', 'assessment:identify_declaration_sources_for_input_and_output_schemas', 'assessment:trace_operation_references_to_input_and_output_definitions']
  taught-before-tested: B.f2←s06; B.f3←s06

### s11 · recap · Keep these distinctions
Recap — 
(takeaway) Defaults govern presence; nullable types govern null. Compare omitted, null and concrete inputs separately. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(takeaway) Locate /openapi.json; connect typed body and response declarations to schemas; follow path/method references into components. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧
[UP NEXT] Next: tile_049 — Trusted host validation: Start with Trusted host validation.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Required, optional and default input semantics
(definition) A default determines requiredness; a type that admits None determines nullability. These are different questions. ⟦A.f1 A:tb2 A:tb4 A:tb5 A:tb6⟧
(definition) A nullable field with no default still requires presence. field: Type | None = None allows both omission and explicit null. ⟦A.f2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(example) For the supplied note, admitting null differs from permitting omission; only the declaration with a default permits both. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r02 · Try the contrast: Required, optional and default input semantics
(definition) A nullable field with no default still requires presence. field: Type | None = None allows both omission and explicit null. ⟦A.f2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(definition) Send absence, explicit JSON null and a concrete value as separate requests. Compare each with the declared default and nullable type. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) For the supplied note bodies, omission and explicit null are different requests. Without a default, omission fails the presence requirement, while explicit null and a concrete string satisfy it. Adding = None permits omission too. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r03 · Try the contrast: FastAPI OpenAPI generation from typed route contracts
(definition) FastAPI normally serves the generated OpenAPI document at /openapi.json. It describes operations and data schemas. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(example) The order operation path differs from the document location: /openapi.json normally serves the generated description of operations and schemas. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
### r04 · Try the contrast: FastAPI OpenAPI generation from typed route contracts
(definition) Typed body declarations contribute input schemas; response models contribute output schemas to the generated public contract. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(definition) Locate the endpoint’s method entry under paths, then follow its schema references into components to find the public input and output definitions. ⟦B.f3 B:tb3 B:tb4 B:tb5 B:tb6⟧
(example) For POST /orders, a schema reference differs from the field definition it points to in components. ⟦B.f2 B.f3 B:tb3 B:tb4 B:tb5 B:tb6⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: Field(json_schema_extra=...)
· constraints.blocked_syntax: @app.exception_handler(...)
· constraints.blocked_syntax: model_dump(exclude_unset=True)
· constraints.blocked_syntax: app.openapi() overrides
· constraints.blocked_syntax: @app.exception_handler

=========

# EVALUATOR PACKET — Trusted host validation (tile_049)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi_backend.trusted_host_validation — Trusted host validation

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: remediation step tile_049.r02 is never referenced

## SOURCE FACTS — A (fastapi_backend.trusted_host_validation)   objective: Enforce accepted HTTP hosts: configure one deployment host allowlist.
A.f1: TrustedHostMiddleware validates the request Host against an allowed_hosts list and responds with 400 when the host is not allowed.   [sources: fastapi_docs_advanced#https://starlette.dev/middleware/#trustedhostmiddleware]
A.f2: Configure app.add_middleware(TrustedHostMiddleware, allowed_hosts=[...]) using domain names; *.example.com permits subdomains and ["*"] permits any host.   [sources: fastapi_docs_advanced#https://starlette.dev/middleware/#trustedhostmiddleware]
A.f3: www_redirect defaults to true and can redirect an allowed non-www host to its www counterpart, so account for it when verifying an allowlist's response.   [sources: fastapi_docs_advanced#https://starlette.dev/middleware/#trustedhostmiddleware]
note: Establish this first: A host allowlist validates the requested host identity independently of proxy metadata..
note: Stay within the current objective: Enforce accepted HTTP hosts. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify requests rejected by a host allowlist.
PRACTICE ANCHOR (live_code): Configure a deployment allowlist that accepts example.com and its subdomains, rejects unrelated hosts, and explicitly disables www redirection for predictable verification.  SUCCESS: The application registers TrustedHostMiddleware with allowed_hosts=["example.com", "*.example.com"] and www_redirect=False. Supplied checks confirm that intended hosts pass the host boundary and an unrelated host receives 400.
ASSESSMENT ANCHOR: identify_hosts_rejected_by_an_allowlist facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_exact_domain_subdomain_and_all_host_policies facts=['f2']
ASSESSMENT ANCHOR: distinguish_host_rejection_from_allowed_host_redirection facts=['f1', 'f3']

## DATA ASSETS USED
ds.host_checks: Authored host-policy comparison — columns: policy(categorical), allowed_hosts(text), www_redirect(categorical), Host(identifier), outcome(categorical), status(categorical,digits-as-label)
   ["deployment","example.com, *.example.com",false,"example.com","accepted",200]
   ["deployment","example.com, *.example.com",false,"www.example.com","accepted",200]
   ["deployment","example.com, *.example.com",false,"unrelated.example","rejected",400]
   ["exact","example.com",false,"www.example.com","rejected",400]
   ["subdomain wildcard","*.example.com",false,"example.com","rejected",400]
   ["all-host wildcard","*",false,"unrelated.example","accepted",200]
   ["www redirect","www.example.com",true,"example.com","redirected to www.example.com",null]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; Bounded resource listing with stable pagination and filtering; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Consistent public error envelopes through exception handlers; Credential and sensitive-data redaction from emitted logs; Distinct create and partial-update contracts; Graceful termination and shutdown verification; Header and cookie input binding; Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels; Keeping API schemas distinct from persistence entities; Meaningful contract examples and operation metadata; Proxy header trust; Redis cache-aside selection and population; Request correlation context across service logs; Request-scoped async-compatible PostgreSQL session lifecycle; Request-validation error behavior; Retrieve resource; Service health and readiness checks; Test dependency replacement; Transaction commit and rollback boun

## LESSON, in learner order

### s01 · explainer · Declare the boundary: Trusted host validation
Explainer — 
(mechanism) TrustedHostMiddleware checks Host against allowed_hosts. An unallowed host receives 400. ⟦A.f1 A:tb1 A:tb2 A:tb4⟧
(mechanism) Register TrustedHostMiddleware through app.add_middleware with domain names in allowed_hosts. *.example.com allows subdomains; ["*"] allows any host. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) www_redirect defaults to true and can redirect an allowed non-www host to its www counterpart. Account for redirects when checking the allowlist’s response. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.host_checks cols=['policy', 'allowed_hosts', 'www_redirect', 'Host', 'outcome', 'status'] ] caption: Authored host-policy comparison. Null redirect status means the glossary does not specify its code.

### s02 · check · Check the boundary: Trusted host validation
Check — Use the supplied order-service scenario to reason about this contract.
QUESTION [choice, intro, grading=client] When verifying TrustedHostMiddleware, which distinction correctly separates rejection from www redirection?
  ✔ option_1: A disallowed Host receives 400; an allowed non-www host can be redirected when www_redirect applies.
      why: Rejection and configured/default www redirection are separate outcomes.
  ✘ option_2: Every redirect means the Host was rejected with 400.
      why: An allowed non-www host can redirect; rejection instead returns 400.
  ✘ option_3: www_redirect always defaults to false, so an allowed host cannot redirect by default.
      why: www_redirect defaults to true and can redirect an allowed non-www host.
  feedback✔: Rejection and configured/default www redirection are separate outcomes.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Separate the stated requirement from a nearby but different boundary.']  remediation→r01
  MEASURES: A:distinguish_host_rejection_from_allowed_host_redirection(f1,f3)   anchors=['assessment:distinguish_host_rejection_from_allowed_host_redirection']
  taught-before-tested: A.f1←s01; A.f3←s01

### s03 · hands_on · Apply the contract: Trusted host validation
Hands On — Complete the supplied workspace within its stated contract.
QUESTION [code_exercise, stretch, grading=client] Import TrustedHostMiddleware and register it with allowed_hosts=['example.com', '*.example.com'] and www_redirect=False. Keep /orders unchanged and do not use the all-host wildcard. The harness checks the exact domain, a www subdomain and an unrelated host without following redirects.
  runtime={'kind': 'python_asgi', 'version': '0.29.5'} constraints.allowed=['from fastapi import FastAPI', 'from fastapi.middleware.trustedhost import TrustedHostMiddleware', 'app = FastAPI()', 'app.add_middleware(TrustedHostMiddleware, allowed_hosts=[...], www_redirect=False)', 'Lists of domain-name strings', 'Exact domain strings and wildcard domain strings', 'True and False keyword argument values'] blocked=4 items
  file exercise.py [editable]:
from fastapi import FastAPI
app = FastAPI()
# TODO: import and register TrustedHostMiddleware for example.com and
# *.example.com, with www_redirect=False and without the all-host wildcard.
@app.get('/orders')
def orders():
    return {'result': 'host boundary passed'}
import asyncio, inspect, json, ast
import httpx
from contextlib import contextmanager

def _drive(coro):
    try:
        pending = coro.send(None)
    except StopIteration as done:
        return done.value
    raise RuntimeError('Harness encountered a suspending operation: ' + repr(pending))

async def _requests(application, requests):
    async with application.router.lifespan_context(application):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application, raise_app_exceptions=False), base_url='http://testserver') as client:
            out=[]
            for method,path,kwargs in requests:
                response=await client.request(method,path,**kwargs)
                try: body=response.json()
                except ValueError: body=response.text
                out.append({'status':response.status_code,'body':body})
            return out
def _case(host):
    middleware=app.user_middleware[0]
    assert middleware.kwargs=={'allowed_hosts':['example.com','*.example.com'],'www_redirect':False}
    return _drive(_requests(app,[('GET','/orders',{'headers':{'Host':host},'follow_redirects':False})]))
import inspect
from fastapi import FastAPI, Body
verification_app=FastAPI()

async def verify_case(payload: dict=Body(...)):
    result=_case(payload['case'])
    if inspect.isawaitable(result):return await result
    return result
verify_case = verification_app.post('/_verify')(verify_case)

  SOLUTION exercise.py:
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
app = FastAPI()
app.add_middleware(TrustedHostMiddleware, allowed_hosts=['example.com', '*.example.com'], www_redirect=False)
# TODO: import and register TrustedHostMiddleware for example.com and
# *.example.com, with www_redirect=False and without the all-host wildcard.
@app.get('/orders')
def orders():
    return {'result': 'host boundary passed'}
import asyncio, inspect, json, ast
import httpx
from contextlib import contextmanager

def _drive(coro):
    try:
        pending = coro.send(None)
    except StopIteration as done:
        return done.value
    raise RuntimeError('Harness encountered a suspending operation: ' + repr(pending))

async def _requests(application, requests):
    async with application.router.lifespan_context(application):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application, raise_app_exceptions=False), base_url='http://testserver') as client:
            out=[]
            for method,path,kwargs in requests:
                response=await client.request(method,path,**kwargs)
                try: body=response.json()
                except ValueError: body=response.text
                out.append({'status':response.status_code,'body':body})
            return out
def _case(host):
    middleware=app.user_middleware[0]
    assert middleware.kwargs=={'allowed_hosts':['example.com','*.example.com'],'www_redirect':False}
    return _drive(_requests(app,[('GET','/orders',{'headers':{'Host':host},'follow_redirects':False})]))
import inspect
from fastapi import FastAPI, Body
verification_app=FastAPI()

async def verify_case(payload: dict=Body(...)):
    result=_case(payload['case'])
    if inspect.isawaitable(result):return await result
    return result
verify_case = verification_app.post('/_verify')(verify_case)

  test test_1 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"example.com"}}],"app":"verification_app","expected":{"status":200,"json":[{"status":200,"body":{"result":"host boundary passed"}}]}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  test test_2 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"www.example.com"}}],"app":"verification_app","expected":{"status":200,"json":[{"status":200,"body":{"result":"host boundary passed"}}]}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  test test_3 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"unrelated.example"}}],"app":"verification_app","expected":{"status":200,"json":[{"status":400,"body":"Invalid host header"}]}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"38d24d78227b4f4204c23962567be24e7288a0fa27293da3b9021a15eef27b9b","tests_passed":3}
  feedback✔: You applied the declared boundary and preserved its required behavior.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Compare each declaration with its input or lifecycle boundary.', 'Trace what happens on the alternative input or exit, not only the successful path.']
  MEASURES: A:identify_hosts_rejected_by_an_allowlist(f1,f2); A:distinguish_exact_domain_subdomain_and_all_host_policies(f2); A:distinguish_host_rejection_from_allowed_host_redirection(f1,f3)   anchors=['practice', 'assessment:identify_hosts_rejected_by_an_allowlist', 'assessment:distinguish_exact_domain_subdomain_and_all_host_policies', 'assessment:distinguish_host_rejection_from_allowed_host_redirection']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f2←s01; A.f1←s01; A.f3←s01

### s04 · recap · Keep these distinctions
Recap — 
(takeaway) Check Host against domain policies; distinguish rejection from www redirection; an all-host wildcard permits every host. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: tile_050 — Credential and sensitive-data redaction from emitted logs: Start with Credential and sensitive-data redaction from emitted logs.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Trusted host validation
(definition) TrustedHostMiddleware checks Host against allowed_hosts. An unallowed host receives 400. ⟦A.f1 A:tb2 A:tb4⟧
(definition) www_redirect defaults to true and can redirect an allowed non-www host to its www counterpart. Account for redirects when checking the allowlist’s response. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) For the supplied host policy, a rejected host differs from an allowed host redirected to its www counterpart. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast: Trusted host validation
(definition) TrustedHostMiddleware checks Host against allowed_hosts. An unallowed host receives 400. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Register TrustedHostMiddleware through app.add_middleware with domain names in allowed_hosts. *.example.com allows subdomains; ["*"] allows any host. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) www_redirect defaults to true and can redirect an allowed non-www host to its www counterpart. Account for redirects when checking the allowlist’s response. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) For the supplied host policy, a rejected host differs from an allowed host redirected to its www counterpart. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: app.dependency_overrides[...] = ...
· constraints.blocked_syntax: @app.exception_handler(...)

=========

# EVALUATOR PACKET — Credential and sensitive-data redaction from emitted logs (tile_050)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = observability.log_redaction — Credential and sensitive-data redaction from emitted logs

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (observability.log_redaction)   objective: Redact sensitive logs: verify one failure's redaction.
A.f1: Access tokens, passwords, primary secrets and sensitive personal data should usually not be recorded directly in logs; remove or mask them according to the logging policy.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#data-to-exclude]
A.f2: Review diagnostic context as well as the main log message, because connection strings, session identifiers and other sensitive values can appear in supplemental fields.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#data-to-exclude]
A.f3: Exercise a failure with recognizable synthetic sensitive values, inspect the emitted records and confirm that the redaction policy removes the prohibited values while retaining the intended event fields.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#verification]
note: Establish this first: Diagnostics must not become exposure channels.
note: Stay within the current objective: Redact sensitive logs. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify diagnostic credentials.
PRACTICE ANCHOR (live_code): Exercise one supplied failure with a recognizable fake token and fake connection-string secret, then verify redaction across the complete emitted record.  SUCCESS: Neither prohibited synthetic value appears in the emitted message or supplemental context, and the intended event field remains intact.
ASSESSMENT ANCHOR: identify_sensitive_values_in_diagnostic_records facts=['f1', 'f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; Bounded resource listing with stable pagination and filtering; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Consistent public error envelopes through exception handlers; Distinct create and partial-update contracts; Graceful termination and shutdown verification; Header and cookie input binding; Injection-resistant database and input handling; Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels; Keeping API schemas distinct from persistence entities; Meaningful contract examples and operation metadata; Proxy header trust; Redis cache-aside selection and population; Request correlation context across service logs; Request-scoped async-compatible PostgreSQL session lifecycle; Request-validation error behavior; Retrieve resource; Service health and readiness checks; Test dependency replacement; Transaction commit and rollback boundaries; Tr

## LESSON, in learner order

### s01 · explainer · Declare the boundary: Credential and sensitive-data redaction from emitted logs
Explainer — 
(mechanism) Access tokens, passwords, primary secrets and sensitive personal data should usually not appear directly in logs. Remove or mask them under the logging policy. ⟦A.f1 A:tb1 A:tb2 A:tb4⟧
(mechanism) Inspect supplemental context as well as the message: connection strings, session identifiers and other sensitive values can appear there. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Trigger a failure with recognizable synthetic sensitive values. Inspect emitted records to confirm prohibited values are removed while intended event fields remain. ⟦A.f3 A:tb3 A:tb4⟧
[BEFORE_AFTER] Before: the same synthetic failure with masking disabled. After: policy masks prohibited strings throughout message and context while retaining the event field. Output is computed from this fixture.
  before:
[CODE python]
import io
import logging
class RedactingFormatter(logging.Formatter):
    def __init__(self, secrets):
        super().__init__('%(message)s context=%(context)s event=%(event)s')
        self.secrets = secrets
    def format(self, record):
        text = super().format(record)
        for secret in self.secrets:
            text = text
        return text
def failure_harness(*, token, connection_string):
    output = io.StringIO()
    logger = logging.getLogger('order.redaction.exercise')
    logger.handlers.clear()
    logger.propagate = False
    logger.setLevel(logging.ERROR)
    handler = logging.StreamHandler(output)
    handler.setFormatter(RedactingFormatter([token, connection_string]))
    logger.addHandler(handler)
    logger.error('synthetic failure token=' + token, extra={
        'context': 'connection=' + connection_string + ' token=' + token,
        'event': 'order_failure'})
    text = output.getvalue()
    message, tail = text.rstrip('\n').split(' context=', 1)
    context, event = tail.rsplit(' event=', 1)
    return {'text': text, 'fields': {'event': event, 'context': context}}

result = failure_harness(token='FAKE_ORDER_TOKEN_ABC', connection_string='FAKE_CONNECTION_SECRET_XYZ')
print(result['text'], end='')

  annotations: []
  after:
[CODE python]
import io
import logging
class RedactingFormatter(logging.Formatter):
    def __init__(self, secrets):
        super().__init__('%(message)s context=%(context)s event=%(event)s')
        self.secrets = secrets
    def format(self, record):
        text = super().format(record)
        for secret in self.secrets:
            text = text.replace(secret, '[REDACTED]')
        return text
def failure_harness(*, token, connection_string):
    output = io.StringIO()
    logger = logging.getLogger('order.redaction.exercise')
    logger.handlers.clear()
    logger.propagate = False
    logger.setLevel(logging.ERROR)
    handler = logging.StreamHandler(output)
    handler.setFormatter(RedactingFormatter([token, connection_string]))
    logger.addHandler(handler)
    logger.error('synthetic failure token=' + token, extra={
        'context': 'connection=' + connection_string + ' token=' + token,
        'event': 'order_failure'})
    text = output.getvalue()
    message, tail = text.rstrip('\n').split(' context=', 1)
    context, event = tail.rsplit(' event=', 1)
    return {'text': text, 'fields': {'event': event, 'context': context}}

result = failure_harness(token='FAKE_ORDER_TOKEN_ABC', connection_string='FAKE_CONNECTION_SECRET_XYZ')
print(result['text'], end='')

  annotations: []

### s02 · check · Check the boundary: Credential and sensitive-data redaction from emitted logs
Check — Use the supplied order-service scenario to reason about this contract.
QUESTION [choice, intro, grading=client] A failure record has both a main message and supplemental diagnostic context. Where should a redaction check look for prohibited synthetic sensitive values?
  ✔ option_1: In the complete emitted message and supplemental context, while checking intended event fields remain.
      why: Sensitive data can occur in either part; the event context must be retained.
  ✘ option_2: Only in the main message; supplemental connection context can be ignored.
      why: Connection strings and other sensitive data can occur in supplemental fields.
  ✘ option_3: Only in supplemental fields; main-message secrets can be ignored.
      why: The main message is also emitted log text and must not retain prohibited values.
  feedback✔: Sensitive data can occur in either part; the event context must be retained.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Separate the stated requirement from a nearby but different boundary.']  remediation→r01
  MEASURES: A:identify_sensitive_values_in_diagnostic_records(f1,f2)   anchors=['assessment:identify_sensitive_values_in_diagnostic_records']
  taught-before-tested: A.f1←s01; A.f2←s01

### s03 · hands_on · Apply the contract: Credential and sensitive-data redaction from emitted logs
Hands On — Complete the supplied workspace within its stated contract.
QUESTION [code_exercise, stretch, grading=client] Use the supplied recognizable token and connection_string variables to invoke failure_harness(token=token, connection_string=connection_string), assigning result. Assert each prohibited value is not in result['text'] (the entire emitted message and context), and assert result['fields']['event'] == 'order_failure'. Do not replace the variables with literal secrets or inspect only the main message.
  runtime={'kind': 'python_asgi', 'version': '0.29.5'} constraints.allowed=['variable assignment', 'string literals', 'function calls with keyword arguments', 'dictionary key access', 'assert statements', 'string membership checks using not in', 'equality comparison using =='] blocked=5 items
  file exercise.py [editable]:
import io
import logging
class RedactingFormatter(logging.Formatter):
    def __init__(self, secrets):
        super().__init__('%(message)s context=%(context)s event=%(event)s')
        self.secrets = secrets
    def format(self, record):
        text = super().format(record)
        for secret in self.secrets:
            text = text.replace(secret, '[REDACTED]')
        return text
def failure_harness(*, token, connection_string):
    output = io.StringIO()
    logger = logging.getLogger('order.redaction.exercise')
    logger.handlers.clear()
    logger.propagate = False
    logger.setLevel(logging.ERROR)
    handler = logging.StreamHandler(output)
    handler.setFormatter(RedactingFormatter([token, connection_string]))
    logger.addHandler(handler)
    logger.error('synthetic failure token=' + token, extra={
        'context': 'connection=' + connection_string + ' token=' + token,
        'event': 'order_failure'})
    text = output.getvalue()
    message, tail = text.rstrip('\n').split(' context=', 1)
    context, event = tail.rsplit(' event=', 1)
    return {'text': text, 'fields': {'event': event, 'context': context}}

token = 'FAKE_ORDER_TOKEN_ABC'
connection_string = 'FAKE_CONNECTION_SECRET_XYZ'
# TODO: run failure_harness and verify complete text plus retained event.
import ast,inspect
class _VerifiedResult(dict):
    def verify(self):
        tree=ast.parse(inspect.getsource(failure_harness)) if False else ast.parse(_solution_source)
        def normalized(node):
            if isinstance(node,ast.Compare) and len(node.ops)==1 and isinstance(node.ops[0],ast.Eq):
                return ('Eq',tuple(sorted((ast.dump(node.left),ast.dump(node.comparators[0])))))
            return ast.dump(node)
        checks=[normalized(n.test) for n in ast.walk(tree) if isinstance(n,ast.Assert)]
        required=[normalized(ast.parse(line).body[0].test) for line in (
            "assert token not in result['text']",
            "assert connection_string not in result['text']",
            "assert result['fields']['event'] == 'order_failure'")]
        assert all(test in checks for test in required)
        return {'text':self['text'],'fields':self['fields'],'checked_token':token,'checked_connection':connection_string}

_solution_source = open('exercise.py').read()

  SOLUTION exercise.py:
import io
import logging
class RedactingFormatter(logging.Formatter):
    def __init__(self, secrets):
        super().__init__('%(message)s context=%(context)s event=%(event)s')
        self.secrets = secrets
    def format(self, record):
        text = super().format(record)
        for secret in self.secrets:
            text = text.replace(secret, '[REDACTED]')
        return text
def failure_harness(*, token, connection_string):
    output = io.StringIO()
    logger = logging.getLogger('order.redaction.exercise')
    logger.handlers.clear()
    logger.propagate = False
    logger.setLevel(logging.ERROR)
    handler = logging.StreamHandler(output)
    handler.setFormatter(RedactingFormatter([token, connection_string]))
    logger.addHandler(handler)
    logger.error('synthetic failure token=' + token, extra={
        'context': 'connection=' + connection_string + ' token=' + token,
        'event': 'order_failure'})
    text = output.getvalue()
    message, tail = text.rstrip('\n').split(' context=', 1)
    context, event = tail.rsplit(' event=', 1)
    return {'text': text, 'fields': {'event': event, 'context': context}}

token = 'FAKE_ORDER_TOKEN_ABC'
connection_string = 'FAKE_CONNECTION_SECRET_XYZ'
# TODO: run failure_harness and verify complete text plus retained event.
result = failure_harness(token=token, connection_string=connection_string)
assert token not in result['text']
assert connection_string not in result['text']
assert result['fields']['event'] == 'order_failure'
import ast,inspect
class _VerifiedResult(dict):
    def verify(self):
        tree=ast.parse(inspect.getsource(failure_harness)) if False else ast.parse(_solution_source)
        def normalized(node):
            if isinstance(node,ast.Compare) and len(node.ops)==1 and isinstance(node.ops[0],ast.Eq):
                return ('Eq',tuple(sorted((ast.dump(node.left),ast.dump(node.comparators[0])))))
            return ast.dump(node)
        checks=[normalized(n.test) for n in ast.walk(tree) if isinstance(n,ast.Assert)]
        required=[normalized(ast.parse(line).body[0].test) for line in (
            "assert token not in result['text']",
            "assert connection_string not in result['text']",
            "assert result['fields']['event'] == 'order_failure'")]
        assert all(test in checks for test in required)
        return {'text':self['text'],'fields':self['fields'],'checked_token':token,'checked_connection':connection_string}

_solution_source = open('exercise.py').read()

  test test_1 (value_equals, visible=True): {"expr":"_VerifiedResult(result).verify()","expected":{"text":"synthetic failure token=[REDACTED] context=connection=[REDACTED] token=[REDACTED] event=order_failure\n","fields":{"event":"order_failure","context":"connection=[REDACTED] token=[REDACTED]"},"checked_token":"FAKE_ORDER_TOKEN_ABC","checked_connection":"FAKE_CONNECTION_SECRET_XYZ"}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"04a2366470bc86b77b7a52f09a558d14144849fc01079b6a30930e1f6e92c53f","tests_passed":1}
  feedback✔: You applied the declared boundary and preserved its required behavior.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ["Check result['text'], not only the message portion", 'Verify both supplied sensitive values are absent while the event field remains order_failure.']
  MEASURES: A:identify_sensitive_values_in_diagnostic_records(f1,f2)   anchors=['practice', 'assessment:identify_sensitive_values_in_diagnostic_records']
  taught-before-tested: A.f1←s01; A.f2←s01

### s04 · recap · Keep these distinctions
Recap — 
(takeaway) Apply logging policy to sensitive values in both message and context; verify emitted records with synthetic failures while retaining intended fields. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: tile_051 — Request-scoped async-compatible PostgreSQL session lifecycle: Start with Request-scoped async-compatible PostgreSQL session lifecycle.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Credential and sensitive-data redaction from emitted logs
(definition) Access tokens, passwords, primary secrets and sensitive personal data should usually not appear directly in logs. Remove or mask them under the logging policy. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Inspect supplemental context as well as the message: connection strings, session identifiers and other sensitive values can appear there. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(example) For the synthetic order failure, a safe main message can still have prohibited values in supplemental context. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: @app.exception_handler(...)
· expected.text: synthetic failure token=[REDACTED] context=connection=[REDACTED] token=[REDACTED] event=order_failure

· value.text: synthetic failure token=[REDACTED] context=connection=[REDACTED] token=[REDACTED] event=order_failure

· value.text: synthetic failure token=[REDACTED] context=connection=[REDACTED] token=[REDACTED] event=order_failure


=========

# EVALUATOR PACKET — Request-scoped async-compatible PostgreSQL session lifecycle (tile_051)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = sqlalchemy.async_session_lifecycle — Request-scoped async-compatible PostgreSQL session lifecycle

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: remediation step tile_051.r02 is never referenced

## SOURCE FACTS — A (sqlalchemy.async_session_lifecycle)   objective: Own an async-compatible database session for a request: supply and close one async-compatible session per request.
A.f1: AsyncSession maintains mutable state for current database work and is not safe to share across concurrent tasks; use a separate session for each concurrent unit of work.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#using-asyncsession-with-concurrent-tasks]
A.f2: Build an async_sessionmaker bound to an async engine and use async with session_factory() as session to obtain and close a session for the request's unit of work.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-orm]
A.f3: A request dependency can yield a session from its async context, leaving session cleanup to that context on both normal and exceptional exit.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-orm, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#a-dependency-with-yield-and-try]
note: Establish this first: A mutable database session belongs to one request unit of work, not concurrent application-wide users..
note: Stay within the current objective: Own an async-compatible database session for a request. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify leaked sessions or unsafe sharing across concurrent requests.
PRACTICE ANCHOR (live_code): Using a supplied async engine, build a session_factory and implement an async request dependency that yields one session from an async context.  SUCCESS: Separate concurrent request dependency invocations receive distinct sessions, and each session's context closes on both normal and exceptional exit.
ASSESSMENT ANCHOR: identify_unsafe_session_sharing_across_concurrent_requests facts=['f1']
ASSESSMENT ANCHOR: identify_session_leaks_from_missing_context_owned_cleanup facts=['f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; Bounded resource listing with stable pagination and filtering; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Consistent public error envelopes through exception handlers; Create resource; Distinct create and partial-update contracts; Graceful termination and shutdown verification; Header and cookie input binding; Injection-resistant database and input handling; Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels; Keeping API schemas distinct from persistence entities; Meaningful contract examples and operation metadata; Proxy header trust; Redis cache-aside selection and population; Request correlation context across service logs; Request-validation error behavior; Retrieve resource; Service health and readiness checks; Test dependency replacement; Transaction commit and rollback boundaries; Translating domain and persistence failures at 

## LESSON, in learner order

### s01 · explainer · Declare the boundary: Request-scoped async-compatible PostgreSQL session lifecycle
Explainer — 
(mechanism) AsyncSession holds mutable state for database work. It is unsafe to share across concurrent tasks; give each concurrent unit of work a separate session. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) Bind async_sessionmaker to an async engine. async with session_factory() as session obtains and closes a session for the request’s unit of work. ⟦A.f2 A:tb3⟧
(mechanism) A request dependency can yield the session from that async context. The context still owns cleanup on normal and exceptional exit. ⟦A.f3 A:tb3⟧
[DIAGRAM: One factory, separate concurrent sessions] nodes=['async_sessionmaker(async engine)', 'Session A: mutable work state', 'Session B: mutable work state', 'Dependency yields session A', 'Dependency yields session B', 'async context exit closes A', 'async context exit closes B'] edges=[('factory', 'sa', 'async with session_factory()'), ('factory', 'sb', 'async with session_factory()'), ('sa', 'ya', 'operation use'), ('sb', 'yb', 'operation use'), ('ya', 'ca', 'normal or exceptional exit'), ('yb', 'cb', 'normal or exceptional exit')] alt: One factory, separate concurrent sessions: async_sessionmaker(async engine); Session A: mutable work state; Session B: mutable work state; Dependency yields session A; Dependency yields session B; async context exit closes A; async context exit closes B

### s02 · explainer · Trace the contract
Explainer — 
(mental_model) Separate the engine-bound factory from the mutable sessions it creates. Concurrent request A and request B need separate sessions. Each request’s async context owns closure, including exceptional exit. Yield supplies the session to the operation without transferring that cleanup responsibility. A shared factory is not a shared AsyncSession. ⟦A.f1 A.f2 A.f3 A:tb4⟧

### s03 · explainer · Work through the supplied example
Explainer — 
(walkthrough) Bind the factory to the async engine, then open a session with async with for each request’s work. Yield that session from inside the context so both normal and exceptional exit close it. Draw session A and session B separately for concurrent requests. Sharing factory setup does not permit both tasks to borrow one mutable session, and cleanup must not depend only on a successful return. ⟦A.f1 A.f2 A.f3 A:tb5 A:tb6⟧

### s04 · video · Optional deeper walkthrough
Video — 
[VIDEO Create a factory and supply a request-owned async session] bridge-before: Watch how the engine-bound factory supplies a session inside an async context. The clip calls the factory async_session_local; Devspace uses session_factory to distinguish the factory from an individual session. | bridge-after: The clip demonstrates factory setup and yielding with context cleanup, but does not explain concurrent-sharing safety or exceptional-exit cleanup. The text covers separate sessions for concurrent work and cleanup on both normal and exceptional exit.
  - T0JXFhJ7pM0 216-441s facts=['f2'] label: Build an async session factory and yield a session from its context | summary: The example replaces a synchronous engine with create_async_engine and explains that the database driver must support asynchronous operation. It then builds an async_sessionmaker bound to that engine. An async dependency opens a session using async with, yields it to the endpoint, and leaves cleanup to the context manager when its block finishes. FastAPI's Depends supplies the yielded session to a route parameter.

### s05 · check · Check the boundary: Request-scoped async-compatible PostgreSQL session lifecycle
Check — Use the supplied order-service scenario to reason about this contract.
QUESTION [choice, intro, grading=client] A request dependency yields an AsyncSession. Which ownership pattern closes the session after both normal and exceptional exit?
  ✔ option_1: Yield inside async with session_factory() as session so the context owns cleanup.
      why: The session context owns closure on either exit.
  ✘ option_2: Create a session, yield it, and never enter or close its context.
      why: A bare yield does not establish context-owned session cleanup.
  ✘ option_3: Close the session only if the handler succeeds.
      why: Cleanup is required after exceptional exit as well as normal exit.
  feedback✔: The session context owns closure on either exit.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Separate the stated requirement from a nearby but different boundary.']  remediation→r01
  MEASURES: A:identify_session_leaks_from_missing_context_owned_cleanup(f2,f3)   anchors=['assessment:identify_session_leaks_from_missing_context_owned_cleanup']
  taught-before-tested: A.f2←s01; A.f3←s01

### s06 · hands_on · Apply the contract: Request-scoped async-compatible PostgreSQL session lifecycle
Hands On — Complete the supplied workspace within its stated contract.
QUESTION [code_exercise, stretch, grading=client] Build session_factory = async_sessionmaker(engine). Complete async def get_session() with async with session_factory() as session: yield session. Preserve the supplied unconnected engine and harness; this is session lifetime, not SQL execution. The harness keeps two dependency invocations open simultaneously, verifies distinct real AsyncSession objects, and verifies context-owned closure after normal and exceptional exit without concealing an exception. A supplied no-I/O close bridge replaces unavailable greenlet only for this unconnected fixture.
  runtime={'kind': 'python_asgi', 'version': '0.29.5'} constraints.allowed=['from sqlalchemy.ext.asyncio import async_sessionmaker', 'session_factory = async_sessionmaker(engine)', 'async def get_session():', 'async with session_factory() as session:', 'yield session'] blocked=12 items
  file exercise.py [editable]:
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine
from sqlalchemy import create_engine
sync_engine = create_engine('sqlite:///:memory:')
sync_engine.dialect.is_async = True
engine = AsyncEngine(sync_engine)
# Supplied engine fixture never connects or issues SQL.
from sqlalchemy.ext.asyncio import async_sessionmaker
# TODO: session_factory = async_sessionmaker(engine)
async def get_session():
    # TODO: async with session_factory() as session: yield session
    raise NotImplementedError
import asyncio, inspect, json, ast
import httpx
from contextlib import contextmanager

def _drive(coro):
    try:
        pending = coro.send(None)
    except StopIteration as done:
        return done.value
    raise RuntimeError('Harness encountered a suspending operation: ' + repr(pending))

async def _requests(application, requests):
    async with application.router.lifespan_context(application):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application, raise_app_exceptions=False), base_url='http://testserver') as client:
            out=[]
            for method,path,kwargs in requests:
                response=await client.request(method,path,**kwargs)
                try: body=response.json()
                except ValueError: body=response.text
                out.append({'status':response.status_code,'body':body})
            return out
async def _case(which):
    from unittest.mock import patch
    from sqlalchemy.ext.asyncio import AsyncSession
    entered=[];closed=[];exits=[]
    old_enter=AsyncSession.__aenter__;old_close=AsyncSession.close;old_exit=AsyncSession.__aexit__
    import sqlalchemy.ext.asyncio.session as session_module
    # No SQL or asynchronous driver IO occurs in this fixture. This bridge
    # executes the real underlying Session.close where WASM lacks greenlet.
    async def no_io_bridge(fn,*args,**kwargs):return fn(*args,**kwargs)
    async def enter(s):
        value=await old_enter(s);entered.append(s);return value
    async def close(s):
        await old_close(s);closed.append(s)
    async def exit(s,t,v,tb):
        value=await old_exit(s,t,v,tb);exits.append((s,t));return value
    async def run():
        a,b=get_session(),get_session()
        sa=await anext(a);sb=await anext(b)
        assert sa is not sb and entered==[sa,sb] and not closed
        await a.aclose()
        assert closed==[sa]
        if which=='failure':
            failure=RuntimeError('request B failure')
            try:await b.athrow(failure)
            except RuntimeError as e:assert e is failure
            else:raise AssertionError('failure concealed')
        else:await b.aclose()
        assert closed==[sa,sb]
        return {'distinct_sessions':sa is not sb,'entered':len(entered),'closed':len(closed),'B_exit':exits[-1][1].__name__}
    with patch.object(session_module,'greenlet_spawn',no_io_bridge),patch.object(AsyncSession,'__aenter__',enter),patch.object(AsyncSession,'close',close),patch.object(AsyncSession,'__aexit__',exit):return await run()
import inspect
from fastapi import FastAPI, Body
verification_app=FastAPI()

async def verify_case(payload: dict=Body(...)):
    result=_case(payload['case'])
    if inspect.isawaitable(result):return await result
    return result
verify_case = verification_app.post('/_verify')(verify_case)

  SOLUTION exercise.py:
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine
from sqlalchemy import create_engine
sync_engine = create_engine('sqlite:///:memory:')
sync_engine.dialect.is_async = True
engine = AsyncEngine(sync_engine)
# Supplied engine fixture never connects or issues SQL.
from sqlalchemy.ext.asyncio import async_sessionmaker
session_factory = async_sessionmaker(engine)
async def get_session():
    async with session_factory() as session:
        yield session
import asyncio, inspect, json, ast
import httpx
from contextlib import contextmanager

def _drive(coro):
    try:
        pending = coro.send(None)
    except StopIteration as done:
        return done.value
    raise RuntimeError('Harness encountered a suspending operation: ' + repr(pending))

async def _requests(application, requests):
    async with application.router.lifespan_context(application):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application, raise_app_exceptions=False), base_url='http://testserver') as client:
            out=[]
            for method,path,kwargs in requests:
                response=await client.request(method,path,**kwargs)
                try: body=response.json()
                except ValueError: body=response.text
                out.append({'status':response.status_code,'body':body})
            return out
async def _case(which):
    from unittest.mock import patch
    from sqlalchemy.ext.asyncio import AsyncSession
    entered=[];closed=[];exits=[]
    old_enter=AsyncSession.__aenter__;old_close=AsyncSession.close;old_exit=AsyncSession.__aexit__
    import sqlalchemy.ext.asyncio.session as session_module
    # No SQL or asynchronous driver IO occurs in this fixture. This bridge
    # executes the real underlying Session.close where WASM lacks greenlet.
    async def no_io_bridge(fn,*args,**kwargs):return fn(*args,**kwargs)
    async def enter(s):
        value=await old_enter(s);entered.append(s);return value
    async def close(s):
        await old_close(s);closed.append(s)
    async def exit(s,t,v,tb):
        value=await old_exit(s,t,v,tb);exits.append((s,t));return value
    async def run():
        a,b=get_session(),get_session()
        sa=await anext(a);sb=await anext(b)
        assert sa is not sb and entered==[sa,sb] and not closed
        await a.aclose()
        assert closed==[sa]
        if which=='failure':
            failure=RuntimeError('request B failure')
            try:await b.athrow(failure)
            except RuntimeError as e:assert e is failure
            else:raise AssertionError('failure concealed')
        else:await b.aclose()
        assert closed==[sa,sb]
        return {'distinct_sessions':sa is not sb,'entered':len(entered),'closed':len(closed),'B_exit':exits[-1][1].__name__}
    with patch.object(session_module,'greenlet_spawn',no_io_bridge),patch.object(AsyncSession,'__aenter__',enter),patch.object(AsyncSession,'close',close),patch.object(AsyncSession,'__aexit__',exit):return await run()
import inspect
from fastapi import FastAPI, Body
verification_app=FastAPI()

async def verify_case(payload: dict=Body(...)):
    result=_case(payload['case'])
    if inspect.isawaitable(result):return await result
    return result
verify_case = verification_app.post('/_verify')(verify_case)

  test test_1 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"normal"}}],"app":"verification_app","expected":{"status":200,"json":{"distinct_sessions":true,"entered":2,"closed":2,"B_exit":"GeneratorExit"}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  test test_2 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":"failure"}}],"app":"verification_app","expected":{"status":200,"json":{"distinct_sessions":true,"entered":2,"closed":2,"B_exit":"RuntimeError"}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"6accd8a8c9a834c488ccf5d00907ea469cffb3f3fcf1a38a24ce041db75716ea","tests_passed":2}
  feedback✔: You applied the declared boundary and preserved its required behavior.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Compare each declaration with its input or lifecycle boundary.', 'Trace what happens on the alternative input or exit, not only the successful path.']
  MEASURES: A:identify_unsafe_session_sharing_across_concurrent_requests(f1)   anchors=['practice', 'assessment:identify_unsafe_session_sharing_across_concurrent_requests']
  taught-before-tested: A.f1←s01

### s07 · recap · Keep these distinctions
Recap — 
(takeaway) Share factory setup, not mutable sessions across concurrent tasks. Obtain sessions with async contexts and yield without losing normal or exceptional cleanup. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
[UP NEXT] Next: tile_052 — Graceful termination and shutdown verification: Start with Graceful termination and shutdown verification.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Request-scoped async-compatible PostgreSQL session lifecycle
(definition) Bind async_sessionmaker to an async engine. async with session_factory() as session obtains and closes a session for the request’s unit of work. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) A request dependency can yield the session from that async context. The context still owns cleanup on normal and exceptional exit. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) For the order request, obtaining a session is not the whole ownership boundary: yield stays inside async with so context exit closes it even on failure. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast: Request-scoped async-compatible PostgreSQL session lifecycle
(definition) AsyncSession holds mutable state for database work. It is unsafe to share across concurrent tasks; give each concurrent unit of work a separate session. ⟦A.f1 A:tb2 A:tb4 A:tb5 A:tb6⟧
(example) Concurrent request A and request B need separate mutable sessions rather than concurrent use of one AsyncSession. ⟦A.f1 A:tb2 A:tb4 A:tb5 A:tb6⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: session.execute(...)
· constraints.blocked_syntax: session.scalars(...)
· constraints.blocked_syntax: app.dependency_overrides[...]

=========

# EVALUATOR PACKET — Graceful termination and shutdown verification · Service health and readiness checks (tile_052)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = deployment.graceful_shutdown_verification — Graceful termination and shutdown verification
B = deployment.health_readiness — Service health and readiness checks

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=3
  warn: remediation step tile_052.r02 is never referenced
  warn: remediation step tile_052.r04 is never referenced
  warn: plan: tile_052.s07 was planned to measure deployment.health_readiness#assessment:distinguish_restart_from_traffic_removal but its interaction does not

## SOURCE FACTS — A (deployment.graceful_shutdown_verification)   objective: Verify graceful shutdown: verify termination during one request.
A.f1: Graceful server termination stops old processes accepting new connections and permits active responses and background tasks to finish within configured time limits.   [sources: fastapi_docs_tutorial#https://uvicorn.dev/server-behavior/#graceful-process-shutdown]
A.f2: Configure --timeout-graceful-shutdown seconds as the maximum wait before Uvicorn starts terminating remaining requests.   [sources: fastapi_docs_tutorial#https://uvicorn.dev/settings/#timeouts]
A.f3: Verify termination during an active request by observing whether its response completes within the limit and whether lifespan cleanup releases the application's shared resources.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/events/#lifespan-function, fastapi_docs_tutorial#https://uvicorn.dev/server-behavior/#graceful-process-shutdown]
note: Establish this first: Termination stops new work and permits bounded cleanup.
note: Stay within the current objective: Verify graceful shutdown. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify interrupted work and leaked resources.
PRACTICE ANCHOR (live_code): Configure Uvicorn's graceful-shutdown wait for the supplied order application, ensure its lifespan cleanup closes the shared HTTP client, and initiate termination while one controlled order request is active.  SUCCESS: Record the configured limit, confirm that termination began during the request, observe whether the response completed within that limit, and verify that lifespan cleanup closed the shared HTTP client. Distinguish interrupted work from an unreleased resource.
ASSESSMENT ANCHOR: identify_interrupted_work_against_shutdown_limit facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: identify_shared_resources_not_released_by_lifespan_cleanup facts=['f3']

## SOURCE FACTS — B (deployment.health_readiness)   objective: Design health probe contracts: specify one service's probes.
B.f1: A failed liveness probe can cause a container restart, whereas a failed readiness probe removes its eligibility to receive service traffic without requiring a restart.   [sources: fastapi_docs_tutorial#https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/]
B.f2: Readiness can depend on temporary conditions such as required backend availability, even while the process is alive.   [sources: fastapi_docs_tutorial#https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-readiness-probes]
B.f3: Configure separate livenessProbe and readinessProbe HTTP checks with path, port, periodSeconds and failureThreshold that match the service's intended restart and traffic-eligibility contracts.   [sources: fastapi_docs_tutorial#https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-a-liveness-http-request, fastapi_docs_tutorial#https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-readiness-probes]
B.f4: An HTTP probe regards response status codes from 200 through 399 as success; other codes are failure.   [sources: fastapi_docs_tutorial#https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-a-liveness-http-request]
note: Establish this first: Probe contracts distinguish survival from traffic eligibility.
note: Stay within the current objective: Design health probe contracts. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine whether failure restarts or removes traffic.
PRACTICE ANCHOR (live_code): Specify separate livenessProbe and readinessProbe HTTP checks for one service using supplied endpoint paths, port, check periods and failure thresholds. Keep temporary required-backend unavailability in the readiness contract rather than treating it as a reason to restart an otherwise live process.  SUCCESS: Both probe mappings contain the intended HTTP path and port, periodSeconds and failureThreshold. The liveness contract permits restart after its failure threshold; the readiness contract removes traffic eligibility after its failure threshold without requiring restart. Endpoint response contracts classify 200 through 399 as success and other codes as failure.
ASSESSMENT ANCHOR: distinguish_restart_from_traffic_removal facts=['f1', 'f2']
ASSESSMENT ANCHOR: determine_probe_outcomes_from_http_status_and_failure_threshold facts=['f1', 'f3', 'f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; Bounded resource listing with stable pagination and filtering; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Consistent public error envelopes through exception handlers; Create resource; Delete resource; Distinct create and partial-update contracts; Header and cookie input binding; Injection-resistant database and input handling; Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels; Keeping API schemas distinct from persistence entities; Meaningful contract examples and operation metadata; Proxy header trust; Redis cache-aside selection and population; Request correlation context across service logs; Request-validation error behavior; Retrieve resource; Service health and readiness checks; Test dependency replacement; Transaction commit and rollback boundaries; Translating domain and persistence failures at the API boundary; Update resour

## LESSON, in learner order

### s01 · explainer · Declare the boundary: Graceful termination and shutdown verification
Explainer — 
(mechanism) Graceful termination stops old processes accepting new connections and lets active responses and background tasks finish within configured limits. ⟦A.f1 A:tb1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Set --timeout-graceful-shutdown seconds as Uvicorn’s maximum wait before it starts terminating remaining requests. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Terminate during an active request. Observe whether its response completes within the limit and whether lifespan cleanup releases shared application resources. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[PROCESS_FLOW: Bounded shutdown and evidence to inspect] nodes=['Controlled order request active', 'Initiate termination', 'Old processes stop accepting new connections', 'Responses and background tasks may finish; maximum wait 5 seconds', 'Wait limit reached: Uvicorn starts terminating remaining requests', 'Lifespan cleanup releases shared client', 'Inspect recorded response outcome and client.is_closed'] edges=[('active', 'terminate', None), ('terminate', 'stop', None), ('stop', 'wait', None), ('wait', 'limit', 'remaining work at boundary'), ('wait', 'cleanup', 'finish within limit'), ('limit', 'cleanup', None), ('cleanup', 'evidence', 'verify, do not assume')] alt: Bounded shutdown and evidence to inspect: Controlled order request active; Initiate termination; Old processes stop accepting new connections; Responses and background tasks may finish; maximum wait 5 seconds; Wait limit reached: Uvicorn starts terminating remaining requests; Lifespan cleanup releases shared client; Inspect recorded response outcome and client.is_closed

### s02 · check · Check the boundary: Graceful termination and shutdown verification
Check — Use the supplied order-service scenario to reason about this contract.
QUESTION [choice, intro, grading=client] During shutdown an active response finishes within the configured limit, but the shared HTTP client remains open. Which verification result identifies the remaining failure?
  ✔ option_1: Response completion passed, but lifespan resource-release verification failed.
      why: Completing a response and closing shared resources are separate checks.
  ✘ option_2: Response completion proves the shared client was closed.
      why: Response completion alone does not verify lifespan cleanup.
  ✘ option_3: An open shared client is evidence that the response could not have completed.
      why: Interrupted work and unreleased resources are distinct observations.
  feedback✔: Completing a response and closing shared resources are separate checks.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Separate the stated requirement from a nearby but different boundary.']  remediation→r01
  MEASURES: A:identify_shared_resources_not_released_by_lifespan_cleanup(f3)   anchors=['assessment:identify_shared_resources_not_released_by_lifespan_cleanup']
  taught-before-tested: A.f3←s01

### s03 · hands_on · Apply the contract: Graceful termination and shutdown verification
Hands On — Complete the supplied workspace within its stated contract.
QUESTION [code_exercise, core, grading=client] Add --timeout-graceful-shutdown 5 to server_command. Complete lifespan finally with await client.aclose() and app.state.client_closed = client.is_closed. Keep the supplied request and harness unchanged. The WASM result is in-process completion and cleanup only, not termination evidence. After saving exercise.py, run the supplied termination_harness.py in a native environment with FastAPI, Uvicorn and httpx installed. It applies the configured limit to Uvicorn, starts the controlled HTTP request, sends SIGTERM after request_started while the request is unfinished, and records actual response completion and lifespan client closure. Termination practice succeeds only with that native evidence; distinguish interrupted work from an unreleased resource.
  runtime={'kind': 'python_asgi', 'version': '0.29.5'} constraints.allowed=['uvicorn --timeout-graceful-shutdown <seconds>', 'async def', 'await', 'try/finally', '@asynccontextmanager', 'yield', 'FastAPI(lifespan=...)', '@app.get(...)', 'await asyncio.sleep(...)', 'httpx.AsyncClient()', 'await client.aclose()', 'client.is_closed'] blocked=6 items
  file exercise.py [editable]:
request_delay = 0.01
shutdown_limit = 5
import asyncio
from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI

async def lifespan(app):
    client = httpx.AsyncClient()
    app.state.client = client
    try:
        yield
    finally:
        # TODO: await client.aclose(); record client.is_closed.
        pass
lifespan = asynccontextmanager(lifespan)
app = FastAPI(lifespan=lifespan)

async def controlled_order():
    print('request_started', flush=True)
    await asyncio.sleep(request_delay)
    print('request_completed', flush=True)
    return {'id': 42, 'quantity': 2}
controlled_order = app.get('/orders/42')(controlled_order)

server_command = 'uvicorn main:app --host 127.0.0.1 --port 8000'
import asyncio, inspect, json, ast
import httpx
from contextlib import contextmanager

def _drive(coro):
    try:
        pending = coro.send(None)
    except StopIteration as done:
        return done.value
    raise RuntimeError('Harness encountered a suspending operation: ' + repr(pending))

async def _requests(application, requests):
    async with application.router.lifespan_context(application):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application, raise_app_exceptions=False), base_url='http://testserver') as client:
            out=[]
            for method,path,kwargs in requests:
                response=await client.request(method,path,**kwargs)
                try: body=response.json()
                except ValueError: body=response.text
                out.append({'status':response.status_code,'body':body})
            return out
def _case(which):
    import shlex
    command=shlex.split(server_command)
    configured=float(command[command.index('--timeout-graceful-shutdown')+1])
    assert configured==shutdown_limit
    async def run():
        async with app.router.lifespan_context(app):
            loop=asyncio.get_running_loop()
            started=loop.time()
            task=asyncio.create_task(controlled_order())
            await asyncio.sleep(0)
            completion_wait_started=loop.time()
            assert not task.done()
            response=await asyncio.wait_for(task,configured)
            elapsed=loop.time()-completion_wait_started
            assert elapsed<configured
        assert app.state.client_closed and app.state.client.is_closed
        return {'configured_limit':configured,'termination_during_active_request':False,'response':response,'closed':app.state.client.is_closed,'verification_mode':'in-process completion and cleanup only'}
    # Expose async verification as an ASGI endpoint for the awaited runner.
    return run()

async def verify_shutdown(which: str): return await _case(which)
verify_shutdown = app.get('/verify-shutdown/{which}')(verify_shutdown)

  file termination_harness.py [readonly]:
# Native adaptation of the registered termination harness. Run beside exercise.py.
# This report, not the in-process WASM result, establishes termination practice.
import ast
import json
import os
from pathlib import Path
import shlex
import signal
import subprocess
import tempfile
import threading
import time
import httpx

source = Path('exercise.py').read_text().split('import asyncio, inspect, json, ast', 1)[0]
values = {}
for node in ast.parse(source).body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        if node.targets[0].id in ('server_command', 'shutdown_limit'):
            values[node.targets[0].id] = ast.literal_eval(node.value)
command = shlex.split(values['server_command'])
configured = float(command[command.index('--timeout-graceful-shutdown') + 1])
assert configured == values['shutdown_limit']
# Use the registry's controlled request delay to leave time for actual process signaling.
controlled_delay = 2
source += '\nimport json\nrequest_delay = ' + repr(controlled_delay) + '\n'
source += '''
_original_lifespan = app.router.lifespan_context
@asynccontextmanager
async def _observed_lifespan(application):
    try:
        async with _original_lifespan(application):
            yield
    finally:
        print('lifespan_client_closed=' + json.dumps({
            'closed': application.state.client.is_closed,
            'recorded_closed': getattr(application.state, 'client_closed', False)
        }), flush=True)
app.router.lifespan_context = _observed_lifespan
'''
command[command.index('main:app')] = 'main:app'
with tempfile.TemporaryDirectory() as workspace:
    Path(workspace, 'main.py').write_text(source)
    p = subprocess.Popen(command, cwd=workspace, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True, start_new_session=True)
    events = []
    ready = threading.Event()
    active = threading.Event()
    finished = threading.Event()
    lock = threading.Lock()
    result = {}
    closure = {}
    def collect():
        for line in p.stdout:
            line = line.strip()
            with lock:
                events.append({'at': time.monotonic(), 'line': line})
                if 'Application startup complete' in line:
                    ready.set()
                if line == 'request_started':
                    active.set()
                if line.startswith('lifespan_client_closed='):
                    closure.update(json.loads(line.split('=', 1)[1]))
    collector = threading.Thread(target=collect, daemon=True)
    collector.start()
    def request():
        try:
            response = httpx.get('http://127.0.0.1:8000/orders/42', timeout=configured + controlled_delay + 10)
            with lock:
                result.update(status=response.status_code, json=response.json())
        except Exception as exc:
            with lock:
                result['error'] = type(exc).__name__
        finally:
            with lock:
                result['finished_at'] = time.monotonic()
                finished.set()
    try:
        if not ready.wait(10):
            raise RuntimeError('startup did not complete')
        t = threading.Thread(target=request, daemon=True)
        t.start()
        if not active.wait(10):
            raise RuntimeError('controlled request did not start')
        with lock:
            # An already-finished request can never count as termination-during-request.
            assert not finished.is_set()
            assert not any(e['line'] == 'request_completed' for e in events)
            assert p.poll() is None
            termination_at = time.monotonic()
            os.killpg(p.pid, signal.SIGTERM)
            signal_sent = True
        t.join(configured + 10)
        p.wait(timeout=configured + 10)
        collector.join(5)
        starts = [e['at'] for e in events if e['line'] == 'request_started']
        completions = [e['at'] for e in events if e['line'] == 'request_completed']
        observed_active = (signal_sent and bool(starts) and starts[0] <= termination_at
            and (not completions or termination_at < completions[0])
            and ('finished_at' not in result or termination_at < result['finished_at']))
        completed_in_limit = (result.get('status') == 200 and 'finished_at' in result
            and 0 <= result['finished_at'] - termination_at < configured)
        client_closed = closure.get('closed') is True and closure.get('recorded_closed') is True
        report = {'configured_limit': configured,
            'termination_at': termination_at,
            'termination_during_active_request': observed_active,
            'response': result, 'response_completed_within_limit': completed_in_limit,
            'lifespan_client_closure': closure, 'closed': client_closed,
            'practice_success': observed_active and completed_in_limit and client_closed,
            'events': events, 'process_returncode': p.returncode}
        print(json.dumps(report, indent=2))
        assert report['practice_success'], 'See response outcome and separate client-closure evidence'
    finally:
        if p.poll() is None:
            os.killpg(p.pid, signal.SIGKILL)
            p.wait()

  SOLUTION exercise.py:
request_delay = 0.01
shutdown_limit = 5
import asyncio
from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI

async def lifespan(app):
    client = httpx.AsyncClient()
    app.state.client = client
    try:
        yield
    finally:
        await client.aclose()
        app.state.client_closed = client.is_closed
lifespan = asynccontextmanager(lifespan)
app = FastAPI(lifespan=lifespan)

async def controlled_order():
    print('request_started', flush=True)
    await asyncio.sleep(request_delay)
    print('request_completed', flush=True)
    return {'id': 42, 'quantity': 2}
controlled_order = app.get('/orders/42')(controlled_order)

server_command = 'uvicorn main:app --host 127.0.0.1 --port 8000 --timeout-graceful-shutdown 5'
import asyncio, inspect, json, ast
import httpx
from contextlib import contextmanager

def _drive(coro):
    try:
        pending = coro.send(None)
    except StopIteration as done:
        return done.value
    raise RuntimeError('Harness encountered a suspending operation: ' + repr(pending))

async def _requests(application, requests):
    async with application.router.lifespan_context(application):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application, raise_app_exceptions=False), base_url='http://testserver') as client:
            out=[]
            for method,path,kwargs in requests:
                response=await client.request(method,path,**kwargs)
                try: body=response.json()
                except ValueError: body=response.text
                out.append({'status':response.status_code,'body':body})
            return out
def _case(which):
    import shlex
    command=shlex.split(server_command)
    configured=float(command[command.index('--timeout-graceful-shutdown')+1])
    assert configured==shutdown_limit
    async def run():
        async with app.router.lifespan_context(app):
            loop=asyncio.get_running_loop()
            started=loop.time()
            task=asyncio.create_task(controlled_order())
            await asyncio.sleep(0)
            completion_wait_started=loop.time()
            assert not task.done()
            response=await asyncio.wait_for(task,configured)
            elapsed=loop.time()-completion_wait_started
            assert elapsed<configured
        assert app.state.client_closed and app.state.client.is_closed
        return {'configured_limit':configured,'termination_during_active_request':False,'response':response,'closed':app.state.client.is_closed,'verification_mode':'in-process completion and cleanup only'}
    # Expose async verification as an ASGI endpoint for the awaited runner.
    return run()

async def verify_shutdown(which: str): return await _case(which)
verify_shutdown = app.get('/verify-shutdown/{which}')(verify_shutdown)

  test test_1 (http_equals, visible=True): {"requests":[{"method":"GET","path":"/verify-shutdown/normal"}],"expected":{"status":200,"json":{"configured_limit":5,"termination_during_active_request":false,"response":{"id":42,"quantity":2},"closed":true,"verification_mode":"in-process completion and cleanup only"}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  test test_2 (http_equals, visible=True): {"requests":[{"method":"GET","path":"/verify-shutdown/repeat"}],"expected":{"status":200,"json":{"configured_limit":5,"termination_during_active_request":false,"response":{"id":42,"quantity":2},"closed":true,"verification_mode":"in-process completion and cleanup only"}}} | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"004bb763b0237960382eeffd60b8fcbb4464c72c8da4ad49d561591552f6f185","tests_passed":2}
  feedback✔: In-process completion and cleanup passed. Termination practice still requires the native SIGTERM report showing an active request, response completion within the configured limit, and lifespan client closure.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Compare each declaration with its input or lifecycle boundary.', 'Trace what happens on the alternative input or exit, not only the successful path.']
  MEASURES: A:identify_interrupted_work_against_shutdown_limit(f1,f2,f3); A:identify_shared_resources_not_released_by_lifespan_cleanup(f3)   anchors=['practice', 'assessment:identify_interrupted_work_against_shutdown_limit', 'assessment:identify_shared_resources_not_released_by_lifespan_cleanup']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f3←s01

### s04 · explainer · Declare the boundary: Service health and readiness checks
Explainer — 
(mechanism) Failed liveness can cause a container restart. Failed readiness removes service-traffic eligibility without requiring restart. ⟦B.f1 B:tb1 B:tb2⟧
(mechanism) Readiness can reflect temporary required-backend unavailability even when the process remains alive. ⟦B.f2 B:tb3⟧
(mechanism) Configure separate livenessProbe and readinessProbe HTTP checks with path, port, periodSeconds and failureThreshold matching the intended restart and traffic contracts. ⟦B.f3 B:tb3⟧
(mechanism) HTTP probes count statuses 200 through 399 as success; other statuses are failure. ⟦B.f4 B:tb3⟧
[PROCESS_FLOW: Separate restart and traffic decisions] nodes=['Temporary required-backend outage; process alive', 'livenessProbe: /live:8000, periodSeconds=10, failureThreshold=3', 'readinessProbe: /ready:8000, periodSeconds=5, failureThreshold=2', 'HTTP 200–399 success; other statuses failure', 'Liveness failures reach threshold', 'Readiness failures reach threshold', 'Can cause container restart', 'Remove service-traffic eligibility; no restart required'] edges=[('outage', 'live', 'can remain successful'), ('outage', 'ready', 'can fail'), ('live', 'status', 'classify response'), ('ready', 'status', 'classify response'), ('status', 'lf', 'liveness failure'), ('status', 'rf', 'readiness failure'), ('lf', 'restart', None), ('rf', 'traffic', None)] alt: Separate restart and traffic decisions: Temporary required-backend outage; process alive; livenessProbe: /live:8000, periodSeconds=10, failureThreshold=3; readinessProbe: /ready:8000, periodSeconds=5, failureThreshold=2; HTTP 200–399 success; other statuses failure; Liveness failures reach threshold; Readiness failures reach threshold; Can cause container restart; Remove service-traffic eligibility; no restart required

### s05 · explainer · Trace the contract
Explainer — 
(mental_model) Configure each probe’s path, port, periodSeconds and failureThreshold for its own contract. A temporary required-backend outage can leave liveness successful while readiness removes traffic eligibility. Failed liveness can cause restart; failed readiness does not require it. Classify HTTP statuses 200 through 399 as success, including 3xx. An “unready” response body is insufficient if the status still counts as successful. ⟦B.f1 B.f2 B.f3 B.f4 B:tb4 B:tb5⟧

### s06 · check · Check the boundary: Service health and readiness checks
Check — Use the supplied order-service scenario to reason about this contract.
QUESTION [choice, core, grading=client] During temporary required-backend unavailability, the live process returns 200 from liveness and readiness repeatedly returns 503 until its failure threshold. What follows?
  ✘ option_3: 503 counts as success, so traffic eligibility remains.
      why: Only statuses 200 through 399 count as HTTP probe success. Readiness returning 503 fails and, at its threshold, removes traffic eligibility.
  ✔ option_1: Liveness succeeds; readiness fails and removes traffic eligibility without requiring restart.
      why: 200 is a successful HTTP probe status; 503 is a failure. Readiness reaching its threshold removes traffic eligibility without requiring restart, while liveness succeeds.
  ✘ option_2: The readiness failures require a restart
      why: Readiness failure removes traffic eligibility without requiring restart. Restart is the separate consequence of failed liveness; here liveness returns a successful 200.
  feedback✔: 200 is a successful HTTP probe status; 503 is a failure. Readiness reaching its threshold removes traffic eligibility without requiring restart, while liveness succeeds.  feedback✘: Readiness failure removes traffic eligibility without requiring restart. Restart is the separate consequence of failed liveness; here liveness returns a successful 200. Only statuses 200 through 399 count as HTTP probe success. Readiness returning 503 fails and, at its threshold, removes traffic eligibility.  hints: ['Separate the stated requirement from a nearby but different boundary.']  remediation→r03
  MEASURES: B:determine_probe_outcomes_from_http_status_and_failure_threshold(f1,f3,f4); B:distinguish_restart_from_traffic_removal(f1,f2)   anchors=['assessment:determine_probe_outcomes_from_http_status_and_failure_threshold', 'assessment:distinguish_restart_from_traffic_removal']
  taught-before-tested: B.f1←s04; B.f3←s04; B.f4←s04; B.f1←s04; B.f2←s04

### s07 · hands_on · Apply the contract: Service health and readiness checks
Hands On — Complete the supplied workspace within its stated contract.
QUESTION [code_exercise, stretch, grading=client] Edit only the YAML between the supplied triple quotes. Complete livenessProbe and readinessProbe using supplied path and port under httpGet, plus periodSeconds and failureThreshold at each probe level. Keep the supplied service contract: temporary backend unavailability fails readiness but not liveness; liveness failure at threshold may restart, readiness failure removes traffic eligibility without requiring restart; 200 through 399 succeeds. No endpoint implementation is required. The harness checks both mappings for a healthy backend and an outage.
  runtime={'kind': 'python_asgi', 'version': '0.29.5'} constraints.allowed=['YAML mappings and indentation', 'livenessProbe', 'readinessProbe', 'httpGet', 'path', 'port', 'periodSeconds', 'failureThreshold', 'String path values', 'Integer port, period and threshold values'] blocked=3 items
  file exercise.py [editable]:
probe_yaml = '''
# TODO: complete each mapping using supplied_values.json.
livenessProbe:
  httpGet: {}
readinessProbe:
  httpGet: {}
'''
# Supplied minimal parser covers only the mappings in this task.
import json
supplied = {'livenessProbe': {'path': '/live', 'port': 8000, 'periodSeconds': 10, 'failureThreshold': 3}, 'readinessProbe': {'path': '/ready', 'port': 8000, 'periodSeconds': 5, 'failureThreshold': 2}}
service_contract = 'Fictional order service: a live process returns a successful liveness status even during temporary required-backend unavailability. Readiness uses a failure status during that outage. HTTP statuses 200 through 399 count as success; other statuses count as failure. A liveness failure reaching its configured threshold can cause restart. A readiness failure reaching its threshold removes traffic eligibility without requiring restart. No endpoint implementation is required.\n'
def _parse(text):
    root={};stack=[(-1,root)]
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith('#'):continue
        indent=len(raw)-len(raw.lstrip());key,val=raw.strip().split(':',1);val=val.strip()
        while stack[-1][0]>=indent:stack.pop()
        parent=stack[-1][1]
        if not val:parent[key]={};stack.append((indent,parent[key]))
        elif val=='{}':parent[key]={}
        elif val.startswith('"') and val.endswith('"'):parent[key]=json.loads(val)
        elif val.startswith("'") and val.endswith("'"):parent[key]=val[1:-1].replace("''","'")
        else:parent[key]=int(val) if val.isdigit() else val
    return root
def _case(outage):
    mappings=_parse(probe_yaml)
    for key,v in supplied.items():
        assert mappings[key]=={'httpGet':{'path':v['path'],'port':v['port']},'periodSeconds':v['periodSeconds'],'failureThreshold':v['failureThreshold']}
    return {'mappings':mappings,'contract':service_contract,'backend_unavailable':outage}
import inspect
from fastapi import FastAPI, Body
verification_app=FastAPI()

async def verify_case(payload: dict=Body(...)):
    result=_case(payload['case'])
    if inspect.isawaitable(result):return await result
    return result
verify_case = verification_app.post('/_verify')(verify_case)

  SOLUTION exercise.py:
probe_yaml = '''
livenessProbe:
  httpGet:
    path: /live
    port: 8000
  periodSeconds: 10
  failureThreshold: 3
readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  periodSeconds: 5
  failureThreshold: 2
'''
# Supplied minimal parser covers only the mappings in this task.
import json
supplied = {'livenessProbe': {'path': '/live', 'port': 8000, 'periodSeconds': 10, 'failureThreshold': 3}, 'readinessProbe': {'path': '/ready', 'port': 8000, 'periodSeconds': 5, 'failureThreshold': 2}}
service_contract = 'Fictional order service: a live process returns a successful liveness status even during temporary required-backend unavailability. Readiness uses a failure status during that outage. HTTP statuses 200 through 399 count as success; other statuses count as failure. A liveness failure reaching its configured threshold can cause restart. A readiness failure reaching its threshold removes traffic eligibility without requiring restart. No endpoint implementation is required.\n'
def _parse(text):
    root={};stack=[(-1,root)]
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith('#'):continue
        indent=len(raw)-len(raw.lstrip());key,val=raw.strip().split(':',1);val=val.strip()
        while stack[-1][0]>=indent:stack.pop()
        parent=stack[-1][1]
        if not val:parent[key]={};stack.append((indent,parent[key]))
        elif val=='{}':parent[key]={}
        elif val.startswith('"') and val.endswith('"'):parent[key]=json.loads(val)
        elif val.startswith("'") and val.endswith("'"):parent[key]=val[1:-1].replace("''","'")
        else:parent[key]=int(val) if val.isdigit() else val
    return root
def _case(outage):
    mappings=_parse(probe_yaml)
    for key,v in supplied.items():
        assert mappings[key]=={'httpGet':{'path':v['path'],'port':v['port']},'periodSeconds':v['periodSeconds'],'failureThreshold':v['failureThreshold']}
    return {'mappings':mappings,'contract':service_contract,'backend_unavailable':outage}
import inspect
from fastapi import FastAPI, Body
verification_app=FastAPI()

async def verify_case(payload: dict=Body(...)):
    result=_case(payload['case'])
    if inspect.isawaitable(result):return await result
    return result
verify_case = verification_app.post('/_verify')(verify_case)

  test test_1 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":false}}],"app":"verification_app","expected":{"status":200,"json":{"mappings":{"livenessProbe":{"httpGet":{"path":"/live","port":8000},"periodSeconds":10,"failureThreshold":3},"readinessProbe":{"httpGet":{"path":"/ready","port":8000},"periodSeconds":5,"failureThreshold":2}},"contract":"Fictional order service: a live process returns a successful liveness status even during temporary required-backend unavailability. Readiness uses a f | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  test test_2 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/_verify","json":{"case":true}}],"app":"verification_app","expected":{"status":200,"json":{"mappings":{"livenessProbe":{"httpGet":{"path":"/live","port":8000},"periodSeconds":10,"failureThreshold":3},"readinessProbe":{"httpGet":{"path":"/ready","port":8000},"periodSeconds":5,"failureThreshold":2}},"contract":"Fictional order service: a live process returns a successful liveness status even during temporary required-backend unavailability. Readiness uses a fa | on-fail: The named input/lifecycle case or required declaration did not match its contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"9ccd3398c7f1719d020ea5cf851ec089cdb9d7a319600e120486f42d74202eb9","tests_passed":2}
  feedback✔: You applied the declared boundary and preserved its required behavior.  feedback✘: Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.  hints: ['Compare each declaration with its input or lifecycle boundary.', 'Trace what happens on the alternative input or exit, not only the successful path.']
  MEASURES: B:determine_probe_outcomes_from_http_status_and_failure_threshold(f1,f3,f4)   anchors=['practice', 'assessment:determine_probe_outcomes_from_http_status_and_failure_threshold']
  taught-before-tested: B.f1←s04; B.f3←s04; B.f4←s04

### s08 · recap · Keep these distinctions
Recap — 
(takeaway) Bound shutdown waiting, terminate during active work, and verify response completion plus shared-resource cleanup. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Separate liveness restart and readiness traffic contracts; temporary backend outages can affect readiness while alive; HTTP 200–399 counts as probe success. ⟦B.f1 B.f2 B.f3 B.f4 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Next: tile_054 — Meaningful contract examples and operation metadata: Start with Meaningful contract examples and operation metadata.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Graceful termination and shutdown verification
(definition) Terminate during an active request. Observe whether its response completes within the limit and whether lifespan cleanup releases shared application resources. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) For the delayed order request, response completion does not by itself establish that the shared client was closed. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast: Graceful termination and shutdown verification
(definition) Graceful termination stops old processes accepting new connections and lets active responses and background tasks finish within configured limits. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Set --timeout-graceful-shutdown seconds as Uvicorn’s maximum wait before it starts terminating remaining requests. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Terminate during an active request. Observe whether its response completes within the limit and whether lifespan cleanup releases shared application resources. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) For the delayed order request, response completion does not by itself establish that the shared client was closed. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Try the contrast: Service health and readiness checks
(definition) Failed liveness can cause a container restart. Failed readiness removes service-traffic eligibility without requiring restart. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(definition) Configure separate livenessProbe and readinessProbe HTTP checks with path, port, periodSeconds and failureThreshold matching the intended restart and traffic contracts. ⟦B.f3 B:tb3 B:tb4⟧
(definition) HTTP probes count statuses 200 through 399 as success; other statuses are failure. ⟦B.f4 B:tb3 B:tb4 B:tb5⟧
(example) For the supplied HTTP probe contract, an unready body with a successful status still counts as probe success. Failure thresholds belong to separate restart and traffic-eligibility decisions. ⟦B.f1 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r04 · Try the contrast: Service health and readiness checks
(definition) Failed liveness can cause a container restart. Failed readiness removes service-traffic eligibility without requiring restart. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(definition) Readiness can reflect temporary required-backend unavailability even when the process remains alive. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(definition) Configure separate livenessProbe and readinessProbe HTTP checks with path, port, periodSeconds and failureThreshold matching the intended restart and traffic contracts. ⟦B.f3 B:tb3 B:tb4⟧
(definition) HTTP probes count statuses 200 through 399 as success; other statuses are failure. ⟦B.f4 B:tb3 B:tb4 B:tb5⟧
(example) During the supplied backend outage, an alive process can be unready; removing traffic differs from restarting it. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: @app.exception_handler(...)
· json.contract: Fictional order service: a live process returns a successful liveness status even during temporary required-backend unavailability. Readiness uses a failure status during that outage. HTTP statuses 200 through 399 count as success; other statuses count as failure. A liveness failure reaching its configured threshold can cause restart. A readiness failure reaching its threshold removes traffic eligibility without requiring restart. No endpoint implementation is required.

· json.contract: Fictional order service: a live process returns a successful liveness status even during temporary required-backend unavailability. Readiness uses a failure status during that outage. HTTP statuses 200 through 399 count as success; other statuses count as failure. A liveness failure reaching its configured threshold can cause restart. A readiness failure reaching its threshold removes traffic eligibility without requiring restart. No endpoint implementation is required.

· ops.value: Fictional order service: a live process returns a successful liveness status even during temporary required-backend unavailability. Readiness uses a failure status during that outage. HTTP statuses 200 through 399 count as success; other statuses count as failure. A liveness failure reaching its configured threshold can cause restart. A readiness failure reaching its threshold removes traffic eligibility without requiring restart. No endpoint implementation is required.
_x
· json.contract: Fictional order service: a live process returns a successful liveness status even during temporary required-backend unavailability. Readiness uses a failure status during that outage. HTTP statuses 200 through 399 count as success; other statuses count as failure. A liveness failure reaching its configured threshold can cause restart. A readiness failure reaching its threshold removes traffic eligibility without requiring restart. No endpoint implementation is required.
_x
· ops.value: Fictional order service: a live process returns a successful liveness status even during temporary required-backend unavailability. Readiness uses a failure status during that outage. HTTP statuses 200 through 399 count as success; other statuses count as failure. A liveness failure reaching its configured threshold can cause restart. A readiness failure reaching its threshold removes traffic eligibility without requiring restart. No endpoint implementation is required.
_x
· json.contract: Fictional order service: a live process returns a successful liveness status even during temporary required-backend unavailability. Readiness uses a failure status during that outage. HTTP statuses 200 through 399 count as success; other statuses count as failure. A liveness failure reaching its configured threshold can cause restart. A readiness failure reaching its threshold removes traffic eligibility without requiring restart. No endpoint implementation is required.
_x