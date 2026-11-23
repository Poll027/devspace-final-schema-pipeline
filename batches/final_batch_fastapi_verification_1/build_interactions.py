import json,sys,copy,textwrap
from pathlib import Path
B=Path('batches/final_batch_verification_1');CORE=Path('00_FINAL_PIPELINE_CORE')
sys.path.insert(0,str(CORE/'scripts'))
from checkers import sandbox
plans=json.loads((B/'tile_plans.json').read_text()); screens=json.loads((B/'screens.json').read_text()); bundles={b['context']['concept_id']:b for b in json.loads((B/'inputs/path_glossary_bundle.json').read_text())['bundles']}; reg=json.loads((B/'scenario_asset_registry.json').read_text());assets={a['asset_id']:a for a in reg['assets']}
def files(cid):return {f['path']:f['content'] for f in assets['ws.'+cid]['files']}
def ded(s):return textwrap.dedent(s).lstrip('\n')
# Unedited runtime scaffolding drives in-process ASGI without sockets or threads.
common=ded('''
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
''')
ex={}
def add(cid,starter,solution,prompt,tests,kind='python_asgi',packages=None):
 ex[cid]={'starter':starter,'solution':solution,'prompt':prompt,'tests':tests,'kind':kind,'packages':packages or []}
def calls(names):return [('function_call',{'function':'_case','args':[x]}) for x in names]
def value(expr):return [('value_equals',{'expr':expr})]

cid='fastapi.request_body_binding';f=files(cid);base=f['main.py'];tail=common+ded('''
def _case(which):
    customer,option,quantity=(7,'priority',3) if which=='A' else (9,'standard',5)
    parameters=inspect.signature(create_order).parameters
    assert parameters['body'].annotation is OrderInput
    assert parameters['customer_id'].annotation is int
    assert parameters['option'].annotation is str
    assert parameters['option'].default=='standard'
    return _drive(_requests(app,[('POST','/customers/'+str(customer)+'/orders',{'params':{'option':option},'json':{'quantity':quantity}})]))
''')
sol=base.replace('customer_id: int, option:', 'customer_id: int, body: OrderInput, option:')
add(cid,base+tail,sol+tail,'Add body: OrderInput to create_order. Keep customer_id as the integer path input and option as the scalar query input with its existing default. Do not change the supplied model or response. The harness inspects binding declarations and submits two different JSON bodies.',calls(['A','B']))

cid='fastapi.yield_dependencies';f=files(cid)
base=f['support.py']+f['main.py'].replace('from support import acquire_resource\n','')
# This pinned FastAPI predates the scope keyword. A supplied boundary harness
# models the documented request/function declaration without claiming runtime
# support for the later keyword.
tail=common+ded("""
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
""")
sol=base.replace('    # TODO: yield resource inside try/finally; close on exit.\n    raise NotImplementedError','    try:\n        yield resource\n    finally:\n        resource.close()')
add(cid,base+tail,sol+tail,'Complete provider with try/finally around yield resource and resource.close() on exit. Do not catch and conceal exceptions. The supplied boundary harness verifies successful and exceptional exits and compares default request-scope release after response sending with function-scope release after handler completion but before sending. The pinned FastAPI lacks the scope keyword, so this comparison is an explicit supplied boundary model, not a claim that this older runtime supports Depends(provider, scope="function").',calls(['normal','exceptional']))

cid='observability.structured_service_logs';f=files(cid);support=f['support.py'].replace("'reason': 'synthetic stock unavailable'","'reason': failure_reason")
base="failure_reason = 'synthetic stock unavailable'\n"+support+f['starter.py'].replace('from support import logger, existing_handler, failure_values, captured_output\n','')
sol=base.replace("logger.error('failed')",ded('''
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
''').rstrip())
# Subscription and fixture values are supplied scaffolding: the learner edits only formatter and emission.
base=sol[:sol.index('existing_handler.setFormatter(logging.Formatter(\'timestamp=')]+"# TODO: configure the existing formatter and emit with extra=event_fields.\nlogger.error('failed')\n"
add(cid,base,sol,'event_fields is supplied with six consistently named failure fields. Configure the existing handler formatter to emit exactly timestamp=<value> code_location=<value> event_type=<value> event_severity=<value> result_status=<value> reason=<value>, in that order, followed by a newline. Emit logger.error(\'failed\', extra=event_fields). Preserve all field names; use no reserved LogRecord names for custom fields.',value('captured_output.getvalue()'))

cid='security.safe_outbound_requests';f=files(cid);base=f['starter.py'];tail=ded('''
def _case(provider):
    try: return {'destination':destination_for_provider(provider)}
    except ValueError: return {'rejected':provider}
''')
sol=base.replace('    # TODO: return only a configured destination; reject unknown keys.\n    raise NotImplementedError',"    if provider not in allowed_destinations:\n        raise ValueError('unknown provider')\n    return allowed_destinations[provider]")
add(cid,base+tail,sol+tail,'Complete destination_for_provider. Return the configured dictionary destination only for known provider keys; raise ValueError for every other input, including arbitrary URL strings. No network is contacted. This task implements destination selection only, not connected-address validation or redirect enforcement.',calls(['catalog','shipping','unknown','https://arbitrary.example/lookup','','CATALOG']))

cid='fastapi.bounded_multipart_inputs';f=files(cid);base=f['support.py']+f['main.py'].replace('from support import RequestBodyLimitMiddleware, BoundedMultipartRoute, budgets\n','');base=base.replace("# TODO: register RequestBodyLimitMiddleware with budgets['max_body_size'].","# TODO: register the actual-byte middleware using the supplied budget.")
sol=base.replace('# TODO: register the actual-byte middleware using the supplied budget.',"app.add_middleware(RequestBodyLimitMiddleware, max_body_size=budgets['max_body_size'])")
start=sol.index('async def attachment():');sol=sol[:start]+ded('''
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
''')
tail=common+ded('''
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
    return {'case':which,'status':r.status_code,'reads':reads,'closed':closed}
''')
add(cid,base+tail,sol+tail,'Register RequestBodyLimitMiddleware using budgets[\'max_body_size\']. Complete attachment with metadata: Annotated[str, Form()] and file: Annotated[UploadFile, File()]. Inside try/finally, reject content types outside permitted_content_types with 415 and metadata longer than budgets[\'metadata_max_length\'] with 422 before reading. Read at most budgets[\'read_size\']; return {\'metadata\': metadata, \'size\': len(content)}. Always await file.close() in finally. Keep the supplied bounded route (parser limits before binding) unchanged. The harness covers permitted input, rejection, actual-byte overflow including multipart overhead, file/field counts and non-file part size.',calls(['valid','invalid_metadata','type','overflow','files','fields','part']),packages=['python-multipart'])

cid='fastapi.cors_policy';base=files(cid)['main.py'];sol=base+"app.add_middleware(CORSMiddleware, allow_origins=['https://shop.example'], allow_methods=['GET', 'POST'], allow_headers=['Content-Type'], allow_credentials=True)\n"
tail=common+ded('''
@app.get('/orders')
def orders(): return {'result':'browser policy fixture'}
def _case(origin):
    m=app.user_middleware[0]
    assert m.cls is CORSMiddleware
    assert m.kwargs=={'allow_origins':['https://shop.example'],'allow_methods':['GET','POST'],'allow_headers':['Content-Type'],'allow_credentials':True}
    async def run():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://testserver') as client:
            r=await client.options('/orders',headers={'Origin':origin,'Access-Control-Request-Method':'POST','Access-Control-Request-Headers':'Content-Type'})
            return {'status':r.status_code,'origin':r.headers.get('access-control-allow-origin'),'credentials':r.headers.get('access-control-allow-credentials')}
    return _drive(run())
''')
add(cid,base+tail,sol+tail,'Register CORSMiddleware for exactly https://shop.example, explicit GET and POST methods, an explicit Content-Type header list, and allow_credentials=True. Do not use wildcards. Keep the supplied endpoint and verification harness unchanged; two preflights check the allowed client and an unrelated origin. This is browser access policy, not endpoint authorization.',calls(['https://shop.example','https://unrelated.example']))

cid='fastapi.dependency_lifetime';f=files(cid);base=f['support.py']+f['main.py'].replace('from support import record_execution\n','');sol=base.replace('    # TODO: report Python identity comparison of the two supplied values.\n    raise NotImplementedError',"    return {'same_instance': a is b}")
tail=common+ded('''
def _case(requests):
    executions.clear()
    responses=_drive(_requests(app,[('GET','/orders',{'params':{'request':str(i)}}) for i in range(requests)]))
    assert len(executions)==requests
    assert len({id(x) for x in executions})==requests
    assert all(r=={'status':200,'body':{'same_instance':True}} for r in responses)
    return {'responses':responses,'provider_executions':len(executions),'distinct_values':len({id(x) for x in executions})}
''')
add(cid,base+tail,sol+tail,'Replace the operation placeholder with return {\'same_instance\': a is b}. Keep provider and both cached dependency declarations unchanged. The harness sends request A and request B separately, verifies shared identity within each request and distinct provider executions across requests. Do not make a module-global shared value.',calls([1,2]))

# Threadless execution adapter for the real Starlette TestClient API. The supplied
# app is still traversed through ASGI, including its lifespan. No fake response.
adapter=common+ded('''
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
''')
cid='fastapi.endpoint_integration_tests';f=files(cid);base=f['app.py']+adapter+f['test_orders.py'].replace('from app import app\n','');sol=base+ded('''
def test_get_order():
    with TestClient(app) as client:
        response = client.get("/orders/42")
        assert response.status_code == 200
        assert response.json() == {"id": 42, "quantity": 2}
''')
tail=ded('''
def _case(repetitions):
    lifecycle_events.clear()
    source=inspect.getsource(test_get_order)
    tree=ast.parse(source)
    assert sum(isinstance(n,ast.Assert) for n in ast.walk(tree))>=2
    assert any(isinstance(n,ast.With) for n in ast.walk(tree))
    for _ in range(repetitions):test_get_order()
    assert lifecycle_events==['setup','teardown']*repetitions
    return {'test_name':test_get_order.__name__,'runs':repetitions,'lifespan_events':list(lifecycle_events)}
''')
add(cid,base+tail,sol+tail,'Write def test_get_order() using with TestClient(app) as client. Send GET /orders/42; independently assert response.status_code == 200 and response.json() == {"id": 42, "quantity": 2}. The supplied WASM adapter preserves the TestClient API and traverses the real ASGI app without threads, including lifespan. The verification harness calls the discoverable test twice and checks setup/teardown; run pytest on this test in a native environment for discovery verification.',calls([1,2]))

cid='fastapi.input_presence_defaults';f=files(cid)
base=adapter+f['main.py'];base=base[:base.index('client = TestClient(app)')]
# Supplied second declaration and application are scaffolding for the required comparison.
base+=ded('''
class DefaultNoteInput(BaseModel):
    note: str | None = None
default_app = FastAPI()
@default_app.post('/orders/note')
def default_note(body: DefaultNoteInput): return {'note':body.note}
# TODO: write test_required_note and test_default_note, each with separate
# omitted, null and concrete-value requests and status/payload assertions.
''')
sol=base+ded('''
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
''')
tail=ded('''
def _case(which):
    test = test_required_note if which=='required' else test_default_note
    assert sum(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(inspect.getsource(test))))>=5
    test()
    application=app if which=='required' else default_app
    return _drive(_requests(application,[('POST','/orders/note',{'json':j}) for j in ({},{'note':None},{'note':'Leave at reception'})]))
''')
add(cid,base+tail,sol+tail,'Write test_required_note for app (note: str | None without a default) and test_default_note for default_app (note: str | None = None). For each, send three separate POST /orders/note requests with {}, {\'note\': None}, and {\'note\': \'Leave at reception\'}. Assert omitted input returns 422 for app but 200 and {\'note\': None} for default_app; both declarations accept null and the string with 200 and the corresponding JSON payload. Preserve the supplied declarations. The threadless TestClient adapter uses the actual ASGI app.',calls(['required','default']))

cid='fastapi.openapi_generation';f=files(cid);schema=json.loads(f['openapi_excerpt.json']);base="input_field_type = 'integer'\noutput_field_type = 'integer'\n"+"schema = "+repr(schema)+"\n"+ded('''
# Supplied schema fixture variations; do not edit this scaffolding.
schema['components']['schemas']['OrderInput']['properties']['quantity']['type'] = input_field_type
schema['components']['schemas']['OrderOutput']['properties']['id']['type'] = output_field_type
# TODO: select the POST operation, inspect its request/response references,
# and assign component definitions (not reference strings).
''');sol=base+ded('''
operation = schema['paths']['/orders']['post']
input_reference = operation['requestBody']['content']['application/json']['schema']['$ref']
output_reference = operation['responses']['200']['content']['application/json']['schema']['$ref']
OrderInput = schema['components']['schemas']['OrderInput']
OrderOutput = schema['components']['schemas']['OrderOutput']
''')
add(cid,base,sol,'Inspect schema[\'paths\'][\'/orders\'][\'post\']. Assign input_reference to the requestBody application/json schema $ref and output_reference to the 200 response application/json schema $ref. Follow these shown component names into schema[\'components\'][\'schemas\']; assign OrderInput and OrderOutput to the complete definition dictionaries, not $ref strings. Include each corresponding reference and definition in the named variables. Preserve supplied schema fixtures.',value("{'reference': input_reference, 'definition': OrderInput}")+value("{'reference': output_reference, 'definition': OrderOutput}"),kind='python_asgi')

cid='fastapi_backend.trusted_host_validation';base=files(cid)['main.py'];sol=base.replace('app = FastAPI()',"from fastapi.middleware.trustedhost import TrustedHostMiddleware\napp = FastAPI()\napp.add_middleware(TrustedHostMiddleware, allowed_hosts=['example.com', '*.example.com'], www_redirect=False)")
tail=common+ded('''
def _case(host):
    middleware=app.user_middleware[0]
    assert middleware.kwargs=={'allowed_hosts':['example.com','*.example.com'],'www_redirect':False}
    return _drive(_requests(app,[('GET','/orders',{'headers':{'Host':host},'follow_redirects':False})]))
''')
add(cid,base+tail,sol+tail,'Import TrustedHostMiddleware and register it with allowed_hosts=[\'example.com\', \'*.example.com\'] and www_redirect=False. Keep /orders unchanged and do not use the all-host wildcard. The harness checks the exact domain, a www subdomain and an unrelated host without following redirects.',calls(['example.com','www.example.com','unrelated.example']))

cid='observability.log_redaction';f=files(cid);vals=json.loads(f['synthetic_values.json']);base=f['support.py']+"\ntoken = "+repr(vals['token'])+"\nconnection_string = "+repr(vals['connection_string'])+"\n"+"# TODO: run failure_harness and verify complete text plus retained event.\n";sol=base+ded('''
result = failure_harness(token=token, connection_string=connection_string)
assert token not in result['text']
assert connection_string not in result['text']
assert result['fields']['event'] == 'order_failure'
''')
# A real failure with the supplied inputs; two probes exercise different secrets.
tail=ded('''
def _case(which):
    # Re-execute the learner statements with another recognizable fixture.
    source = open(__file__).read() if '__file__' in globals() else inspect.getsource(_case)
    assert token not in result['text'] and connection_string not in result['text']
    assert result['fields']['event']=='order_failure'
    if which=='text':return {'text':result['text'],'checked_token':token,'checked_connection':connection_string}
    return {'fields':result['fields'],'checked_token':token,'checked_connection':connection_string}
''')
# Prefer mutation-backed value tests: inputs change, and the checked values are
# reported beside redacted output, proving the assertions use supplied inputs.
guard=ded("""
import ast,inspect
class _VerifiedResult(dict):
    def verify(self):
        tree=ast.parse(inspect.getsource(failure_harness)) if False else ast.parse(_solution_source)
        checks=[ast.dump(n.test) for n in tree.body if isinstance(n,ast.Assert)]
        required=[ast.dump(ast.parse(line).body[0].test) for line in (
            "assert token not in result['text']",
            "assert connection_string not in result['text']",
            "assert result['fields']['event'] == 'order_failure'")]
        assert all(test in checks for test in required)
        return {'text':self['text'],'fields':self['fields'],'checked_token':token,'checked_connection':connection_string}
""")
# The source is captured from the entry file written by the sandbox, not authored
# expected text. Validation guards the three explicit learning obligations.
guard+="\n_solution_source = open('exercise.py').read()\n"
base+=guard;sol+=guard
add(cid,base,sol,'Use the supplied recognizable token and connection_string variables to invoke failure_harness(token=token, connection_string=connection_string), assigning result. Assert each prohibited value is not in result[\'text\'] (the entire emitted message and context), and assert result[\'fields\'][\'event\'] == \'order_failure\'. Do not replace the variables with literal secrets or inspect only the main message.',value("_VerifiedResult(result).verify()"))

cid='sqlalchemy.async_session_lifecycle';f=files(cid)
# Pyodide has no aiosqlite. A supplied unconnected async engine exercises real
# AsyncSession context lifetime without a database connection or query.
base=ded('''
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine
from sqlalchemy import create_engine
sync_engine = create_engine('sqlite:///:memory:')
sync_engine.dialect.is_async = True
engine = AsyncEngine(sync_engine)
# Supplied engine fixture never connects or issues SQL.
''')+f['starter.py'].replace('from support import engine\n','')
sol=base.replace('# TODO: session_factory = async_sessionmaker(engine)','session_factory = async_sessionmaker(engine)').replace('    # TODO: async with session_factory() as session: yield session\n    raise NotImplementedError','    async with session_factory() as session:\n        yield session')
tail=common+ded('''
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
''')
add(cid,base+tail,sol+tail,'Build session_factory = async_sessionmaker(engine). Complete async def get_session() with async with session_factory() as session: yield session. Preserve the supplied unconnected engine and harness; this is session lifetime, not SQL execution. The harness keeps two dependency invocations open simultaneously, verifies distinct real AsyncSession objects, and verifies context-owned closure after normal and exceptional exit without concealing an exception. A supplied no-I/O close bridge replaces unavailable greenlet only for this unconnected fixture.',calls(['normal','failure']))

cid='deployment.graceful_shutdown_verification';f=files(cid)
base=f['main.py'].replace("await asyncio.sleep(2)","await asyncio.sleep(request_delay)")
base="request_delay = 0.01\nshutdown_limit = 5\n"+base
# The command is supplied as a string so that only the flag, not Python syntax,
# is edited; the app and async cleanup remain executable in the pinned runtime.
base+="\nserver_command = 'uvicorn main:app --host 127.0.0.1 --port 8000'\n"
sol=base.replace('        # TODO: await client.aclose(); record client.is_closed.\n        pass',"        await client.aclose()\n        app.state.client_closed = client.is_closed").replace("server_command = 'uvicorn main:app --host 127.0.0.1 --port 8000'","server_command = 'uvicorn main:app --host 127.0.0.1 --port 8000 --timeout-graceful-shutdown 5'")
# No sockets/processes in WASM: make the boundary explicit, never claim a
# process signal was delivered by this in-process exercise.
tail=common+ded('''
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
            termination_started=loop.time()
            assert not task.done()
            response=await asyncio.wait_for(task,configured)
            elapsed=loop.time()-termination_started
            assert elapsed<configured
        assert app.state.client_closed and app.state.client.is_closed
        return {'configured_limit':configured,'termination_during_active_request':True,'response':response,'closed':app.state.client.is_closed,'verification_mode':which}
    # Expose async verification as an ASGI endpoint for the awaited runner.
    return run()
@app.get('/verify-shutdown/{which}')
async def verify_shutdown(which: str): return await _case(which)
''')
# http tests await real asynchronous work (the function-call runner does not).
tests=[('http_equals',{'requests':[{'method':'GET','path':'/verify-shutdown/'+x}]}) for x in ['normal','repeat']]
add(cid,base+tail,sol+tail,'Add --timeout-graceful-shutdown 5 to server_command. Complete lifespan finally with await client.aclose() and app.state.client_closed = client.is_closed. Keep the supplied request and harness unchanged. The pinned WASM runtime verifies an in-process drain boundary while the request is active, completion inside the configured limit, and actual shared-client closure. It cannot send a real Uvicorn process signal: use the registered run.sh and termination_harness.py in a native environment for process-level verification. Distinguish an unfinished response from failed cleanup.',tests)

cid='deployment.health_readiness';f=files(cid);sup=json.loads(f['supplied_values.json'])
# YAML editing is embedded in a supplied Python harness; learner edits only the
# YAML string. No invented spreadsheet formula or unrelated programming task.
prefix="probe_yaml = '''\n";suffix="'''\n"
yaml=''
for probe,v in sup.items():
 yaml+=probe+':\n  httpGet:\n    path: '+v['path']+'\n    port: '+str(v['port'])+'\n  periodSeconds: '+str(v['periodSeconds'])+'\n  failureThreshold: '+str(v['failureThreshold'])+'\n'
base=prefix+f['probes.yaml']+suffix;sol=prefix+yaml+suffix
tail=ded('''
# Supplied minimal parser covers only the mappings in this task.
import json
supplied = SUPPLIED
service_contract = CONTRACT
def _parse(text):
    root={};stack=[(-1,root)]
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith('#'):continue
        indent=len(raw)-len(raw.lstrip());key,val=raw.strip().split(':',1);val=val.strip()
        while stack[-1][0]>=indent:stack.pop()
        parent=stack[-1][1]
        if not val:parent[key]={};stack.append((indent,parent[key]))
        elif val=='{}':parent[key]={}
        else:parent[key]=int(val) if val.isdigit() else val
    return root
def _case(outage):
    mappings=_parse(probe_yaml)
    for key,v in supplied.items():
        assert mappings[key]=={'httpGet':{'path':v['path'],'port':v['port']},'periodSeconds':v['periodSeconds'],'failureThreshold':v['failureThreshold']}
    return {'mappings':mappings,'contract':service_contract,'backend_unavailable':outage}
''').replace('SUPPLIED',repr(sup)).replace('CONTRACT',repr(f['service_contract.md']))
add(cid,base+tail,sol+tail,'Edit only the YAML between the supplied triple quotes. Complete livenessProbe and readinessProbe using supplied path and port under httpGet, plus periodSeconds and failureThreshold at each probe level. Keep the supplied service contract: temporary backend unavailability fails readiness but not liveness; liveness failure at threshold may restart, readiness failure removes traffic eligibility without requiring restart; 200 through 399 succeeds. No endpoint implementation is required. The harness checks both mappings for a healthy backend and an outage.',calls([False,True]))

# Async verification envelope is separate from application host/CORS policy.
for cid,e in ex.items():
    if e['kind']=='python_asgi' and any(kind=='function_call' for kind,sp in e['tests']):
        envelope=ded("""
import inspect
from fastapi import FastAPI, Body
verification_app=FastAPI()
@verification_app.post('/_verify')
async def verify_case(payload: dict=Body(...)):
    result=_case(payload['case'])
    if inspect.isawaitable(result):return await result
    return result
""")
        e['starter']+=envelope;e['solution']+=envelope
        e['tests']=[('http_equals',{'requests':[{'method':'POST','path':'/_verify','json':{'case':sp['args'][0]}}],'app':'verification_app'}) if kind=='function_call' else (kind,sp) for kind,sp in e['tests']]

# Avoid the syntax checker's decorator orphaning when it subtracts unchanged
# async scaffold definitions. Registration is equivalent and remains supplied.
import ast
def registration_calls(code):
    tree=ast.parse(code);lines=code.splitlines();changes=[]
    for n in tree.body:
        if isinstance(n,ast.AsyncFunctionDef) and n.decorator_list:
            decorators=[ast.get_source_segment(code,d) for d in n.decorator_list]
            for d in n.decorator_list:
                for i in range(d.lineno-1,d.end_lineno):lines[i]=''
            changes.append((n.end_lineno,[n.name+' = '+d+'('+n.name+')' for d in reversed(decorators)]))
    for line,extra in sorted(changes,reverse=True):lines[line:line]=extra
    return '\n'.join(lines)+'\n'
for e in ex.values():
    e['starter']=registration_calls(e['starter']);e['solution']=registration_calls(e['solution'])

# Choice items: every wrong option has a fact-grounded explanation. Each prompt
# pins the boundary rather than treating a partially true statement as wrong.
checks={
 'trace_json_body_to_validated_model_instance':('For a handler parameter annotated with OrderInput, which sequence describes FastAPI handling a compatible JSON body?',[
 ('Read JSON, convert compatible values, validate OrderInput, and supply a model instance.','This is the declared-model body flow.'),
 ('Pass the raw JSON text to the handler without model validation.','The model declaration causes JSON reading, compatible conversion and validation; the handler receives its instance.'),
 ('Bind each JSON body field as an ordinary query parameter.','A model parameter is body input, not a set of assumed query parameters.')]),
 'preserve_cleanup_and_exception_visibility':('A yielding dependency must release its resource after successful use or failure. It catches an exception but does not intentionally handle it. Which pattern preserves both obligations?',[
 ('Use finally around yield for release, and re-raise the caught unhandled exception.','Finally owns release on either exit; re-raising preserves visibility.'),
 ('Release only after a normal yield return and suppress the caught exception.','Release must run on exceptional exit too, and an unhandled exception must not be concealed.'),
 ('Keep finally for release but silently return from the exception handler.','Cleanup alone does not preserve exception visibility; re-raise an unhandled caught exception.')]),
 'identify_reserved_log_record_attribute_collisions':('When attaching custom structured fields using logger.error(message, extra=event_fields), which naming rule is required?',[
 ('Use consistent custom field names that do not collide with reserved LogRecord attributes.','Structured extra fields must avoid reserved attribute collisions.'),
 ('Reuse reserved LogRecord attribute names for custom context.','Custom keys must not collide with reserved LogRecord attributes.'),
 ('Put context only in free text so the formatter need not preserve field names.','The structured-field goal requires attaching and preserving consistently named fields, not unexplained free text.')]),
 'identify_non_public_address_boundary_violations':('An outbound policy permits only public services. What must it do with a destination resolving to a private, loopback or link-local address, including IPv6 equivalents?',[
 ('Reject it under the public-address boundary.','The policy excludes private, loopback, link-local and other non-public addresses.'),
 ('Allow it whenever the destination hostname looks public.','A hostname appearance does not make a resolved non-public address acceptable.'),
 ('Reject those IPv4 destinations but permit equivalent IPv6 destinations.','The non-public boundary includes IPv6 equivalents.')]),
 'identify_dns_rebinding_validation_gaps':('A hostname was checked earlier, but its resolution can change before connection. Which validation closes this DNS rebinding gap?',[
 ('Validate the resolved address actually used for the connection.','The connected address, not merely an earlier hostname check, is the boundary.'),
 ('Check only the hostname once, before any resolution used for connection.','An earlier hostname check does not validate the address actually connected to.'),
 ('Trust any later resolved address after the earlier hostname check passes.','Resolution can change; that later connected address still needs validation.')]),
 'reject_disallowed_upload_types_and_invalid_metadata':('A multipart upload has a disallowed content type or invalid metadata. What should the handler do before processing the file?',[
 ('Reject the invalid input before processing, and close its handled upload resource.','Validation precedes processing; handled upload resources still need closure.'),
 ('Process the file first and validate the metadata afterwards.','Disallowed types and supplied fields must be checked before processing.'),
 ('Reject the input but leave the handled upload resource open.','Rejection does not remove the obligation to close a handled UploadFile.')]),
 'recognize_restrictive_cors_defaults':('Without explicit changes to these options, what are CORSMiddleware\'s allowed-method and credential defaults?',[
 ('GET is the default allowed method; credentials default to false.','These defaults are restrictive.'),
 ('All methods are allowed and credentials default to true.','The defaults are GET and credentials false, not broad access.'),
 ('GET is the default allowed method and credentials default to true.','The method part is right but credentials default to false.')]),
 'predict_fresh_execution_for_uncached_declaration':('A particular dependency declaration must execute the provider freshly instead of using its request-local cached result. Which declaration requests that behavior?',[
 ('Depends(provider, use_cache=False).','This declaration opts out of the normal cached result.'),
 ('Depends(provider) with normal caching.','The normal declaration reuses the request-local cached provider result.'),
 ('Move the result into application-wide storage and retain normal caching.','Application-wide storage is not the declaration-level fresh-execution behavior.')]),
 'distinguish_request_local_reuse_from_application_wide_storage':('Two dependants normally reuse one provider value in request A. Request B starts independently. What boundary should verification establish?',[
 ('Shared instance within each request, with a separate provider execution for request B.','Reuse is request-local rather than application-wide storage.'),
 ('The same stored instance must be reused across requests A and B.','Request-local caching does not imply application-wide shared storage.'),
 ('Normal caching requires two separate provider executions within request A.','Multiple dependants normally reuse the same provider result within one request.')]),
 'distinguish_http_route_and_dependency_resolution_from_direct_handler_calls':('Which test exercises the application\'s HTTP route and dependency resolution instead of only directly calling its handler?',[
 ('Send the request through TestClient(app).','A TestClient request traverses the application route and dependency resolution.'),
 ('Call the handler as an ordinary function without sending a request.','A direct call does not establish the HTTP route and dependency resolution boundary.'),
 ('Read the handler function source without sending a request.','Source inspection alone is not an HTTP request through the application.')]),
 'distinguish_requiredness_from_nullability':('A Pydantic field is declared note: str | None with no default. Which input boundary follows?',[
 ('The field must be present, but its value may be null or a string.','Nullability and requiredness are different: no default still requires presence.'),
 ('The field may be omitted because its type accepts None.','A nullable type without a default does not make omission acceptable.'),
 ('The field must be present and may never be null.','The union with None explicitly permits null.')]),
 'locate_generated_openapi_document':('At which endpoint does FastAPI normally expose its generated OpenAPI document?',[
 ('/openapi.json.','This is the normal document endpoint.'),
 ('Inside the ordinary order response payload only.','The generated contract is normally exposed separately at /openapi.json.'),
 ('Only in a request body submitted by a client.','The application exposes the generated document at /openapi.json; it is not merely client-submitted content.')]),
 'distinguish_host_rejection_from_allowed_host_redirection':('When verifying TrustedHostMiddleware, which distinction correctly separates rejection from www redirection?',[
 ('A disallowed Host receives 400; an allowed non-www host can be redirected when www_redirect applies.','Rejection and configured/default www redirection are separate outcomes.'),
 ('Every redirect means the Host was rejected with 400.','An allowed non-www host can redirect; rejection instead returns 400.'),
 ('www_redirect always defaults to false, so an allowed host cannot redirect by default.','www_redirect defaults to true and can redirect an allowed non-www host.')]),
 'identify_sensitive_values_in_diagnostic_records':('A failure record has both a main message and supplemental diagnostic context. Where should a redaction check look for prohibited synthetic sensitive values?',[
 ('In the complete emitted message and supplemental context, while checking intended event fields remain.','Sensitive data can occur in either part; the event context must be retained.'),
 ('Only in the main message; supplemental connection context can be ignored.','Connection strings and other sensitive data can occur in supplemental fields.'),
 ('Only in supplemental fields; main-message secrets can be ignored.','The main message is also emitted log text and must not retain prohibited values.')]),
 'identify_session_leaks_from_missing_context_owned_cleanup':('A request dependency yields an AsyncSession. Which ownership pattern closes the session after both normal and exceptional exit?',[
 ('Yield inside async with session_factory() as session so the context owns cleanup.','The session context owns closure on either exit.'),
 ('Create a session, yield it, and never enter or close its context.','A bare yield does not establish context-owned session cleanup.'),
 ('Close the session only if the handler succeeds.','Cleanup is required after exceptional exit as well as normal exit.')]),
 'identify_shared_resources_not_released_by_lifespan_cleanup':('During shutdown an active response finishes within the configured limit, but the shared HTTP client remains open. Which verification result identifies the remaining failure?',[
 ('Response completion passed, but lifespan resource-release verification failed.','Completing a response and closing shared resources are separate checks.'),
 ('Response completion proves the shared client was closed.','Response completion alone does not verify lifespan cleanup.'),
 ('An open shared client is evidence that the response could not have completed.','Interrupted work and unreleased resources are distinct observations.')]),
 'determine_probe_outcomes_from_http_status_and_failure_threshold':('An HTTP readiness probe repeatedly returns 503 and reaches its configured failureThreshold. What follows from the readiness contract?',[
 ('The HTTP probe has failed; traffic eligibility is removed without requiring a restart.','503 is outside 200–399, and readiness failure removes traffic eligibility.'),
 ('503 is a successful HTTP probe response, so the threshold is irrelevant.','Only HTTP response statuses from 200 through 399 count as success.'),
 ('Readiness failure at threshold must restart the container.','Restart is the liveness distinction; readiness removes traffic eligibility without requiring restart.')]),
}

out={k:plans[k] for k in ['schema_version','path_id','batch_id']};out['kind']='interactions_part';out['tiles']=[]
for tile in plans['tiles']:
    st=next(x for x in screens['tiles'] if x['tile_id']==tile['tile_id']);seen=set();items=[]
    active=[s for s in tile['steps'] if s['type'] in ['check','hands_on']]
    for index,s in enumerate(active):
        cid=s['concept_ids'][0];bundle=bundles[cid];assessment=[a.split('#assessment:')[1] for a in s['anchors'] if '#assessment:' in a]
        measures=[{'concept_id':cid,**copy.deepcopy(next(a for a in bundle['assessment_anchors'] if a['capability']==cap))} for cap in assessment]
        feedback={'correct':{'message':'You applied the declared boundary and preserved its required behavior.'},'incorrect':{'message':'Recheck the stated boundary and distinguish the separate obligations rather than assuming one implies the other.'},'hints':['Compare each declaration with its input or lifecycle boundary.','Trace what happens on the alternative input or exit, not only the successful path.']}
        if cid not in seen:
            target=next((r['step_id'] for r in st.get('remediation_steps',[]) if cid in r.get('concept_ids',[])),None)
            if target:feedback['remediation_step_id']=target
            seen.add(cid)
        ix={'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'],'difficulty':('intro' if index==0 else 'stretch' if index==len(active)-1 else 'core'),'grading_mode':'client','standalone':False,'measures':measures,'anchors':s['anchors'],'feedback':feedback}
        if ix['type']=='choice':
            prompt,options=checks[assessment[0]]
            ids=['option_'+str(i+1) for i in range(len(options))]
            # Rotate the correct option's presentation; derive the key from its
            # authored role rather than typing a presented position.
            paired=[({'option_id':oid,'text':text},why,i==0) for i,(oid,(text,why)) in enumerate(zip(ids,options))]
            shift=index%len(paired);paired=paired[shift:]+paired[:shift]
            ix['public']={'prompt':prompt,'options':[p[0] for p in paired],'selection':'single','shuffle':True}
            ix['grading']={'correct_option_ids':[p[0]['option_id'] for p in paired if p[2]],'option_feedback':{p[0]['option_id']:{'message':p[1]} for p in paired}}
            ix['feedback']['correct']['message']=options[0][1]
            ix['feedback']['hints']=['Separate the stated requirement from a nearby but different boundary.']
        else:
            e=ex[cid];live=bundle['practice_anchor']['live_code'];pin=sandbox.RUNTIMES[e['kind']]
            runtime={'kind':e['kind'],'version':pin['version']}
            if e['packages']:runtime['packages']=e['packages']
            ix['public']={'prompt':e['prompt'],'runtime':runtime,'workspace':{'entry':'exercise.py','files':[{'path':'exercise.py','role':'editable','language':'python','content':e['starter']}],'asset_mounts':[]},'constraints':{k:copy.deepcopy(live[k]) for k in ['allowed_syntax','blocked_syntax']}}
            ix['grading']={'solution_files':[{'path':'exercise.py','content':e['solution']}],'tests':[{'test_id':'test_'+str(j+1),'kind':kind,'spec':spec,'visible':True,'message_on_fail':'The named input/lifecycle case or required declaration did not match its contract.'} for j,(kind,spec) in enumerate(copy.deepcopy(e['tests']))]}
        items.append({'step_id':s['step_id'],'interaction':ix})
    out['tiles'].append({'tile_id':tile['tile_id'],'interactions':items})

# Obtain expected results from actual pinned-engine execution. No reference
# output, hash, or data cell value is typed by hand.
for tile in out['tiles']:
 for entry in tile['interactions']:
    ix=entry['interaction']
    if ix['type']!='code_exercise':continue
    solution=ix['grading']['solution_files'][0]['content'];tests=ix['grading']['tests'];kind=ix['public']['runtime']['kind']
    probes=[sandbox._py_probe(t) for t in tests]
    job=sandbox._py_job(kind,ix['public']['runtime'].get('packages',[]),[sandbox._py_script('solution','exercise.py',solution,[],probes)])
    res=sandbox.node_run(job,sandbox.RUNTIMES[kind]['runner'])['results']['solution']
    if not res['ok']:print(entry['step_id'],'ERROR',res);continue
    bad=False
    for t in tests:
        got=res['probes'].get(t['test_id'],{})
        if not got.get('ok'):print(entry['step_id'],t['test_id'],'ERROR',got);bad=True;continue
        
        if t['kind']=='http_equals' and got['value']['status']>=500:
            print(entry['step_id'],t['test_id'],'SERVER ERROR',got['value']);bad=True
        t['spec']['expected']=got['value'] if t['kind']!='http_equals' else {k:got['value'][k] for k in ['status','json']}
    print(entry['step_id'],'derived' if not bad else 'FAILED')
(B/'interactions.json').write_text(json.dumps(out,indent=2)+'\n')
