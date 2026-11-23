import json, re, textwrap, ast
from pathlib import Path
B=Path('batches/final_batch_verification_1')
g=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
bs=g['bundles']; sid='scenario.order_service'
# Mine literal and named vocabulary from the teaching blocks and anchors, not external sources.
vocab=[]
def add(s):
    if s and s not in vocab: vocab.append(s)
def strings(x):
    if isinstance(x,str): yield x
    elif isinstance(x,dict):
        for v in x.values(): yield from strings(v)
    elif isinstance(x,list):
        for v in x: yield from strings(v)
texts=[]
for b in bs:
    texts.extend(t['content'] for t in b['teaching_blocks'])
    texts.append(b['visual_anchor']['purpose'])
    pa=b['practice_anchor']
    texts.extend(strings({k:v for k,v in pa.items() if k!='live_code'}))
    texts.extend(strings({k:v for k,v in pa['live_code'].items() if k!='blocked_syntax'}))
for t in texts:
    for s in re.findall(r'https?://[^\s\"\]\),]+|/[a-z]+(?:/[a-z0-9{}._]+)*|\b(?:\d+|[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*)\b',t):
        if s[0].isdigit() or '_' in s or '.' in s or s.startswith('/') or s in ['OrderInput','OrderOutput','BaseModel','FastAPI','Depends','Form','File','UploadFile','Request','HTTPException','CORSMiddleware','TrustedHostMiddleware','TestClient','LogRecord','Uvicorn','IPv4','IPv6','GET','POST','Content-Type','metadata','file','note','quantity','id','timestamp','reason','provider','engine','session_factory','schema','OrderInput','OrderOutput']:
            add(s)
    for q in re.findall(r'[\"\']([^\"\'\n]+)[\"\']',t):
        if len(q)<100 and re.fullmatch(r'[A-Za-z0-9_/$#.*: -]+',q) and q.strip()==q: add(q)
for term in ['order','customer identifier','ordinary scalar query option','request A','request B','session A','session B','value A','private','loopback','link-local','non-public','Content-Type']:
    if any(term in t for t in texts): add(term)
assets=[]
def ws(i,files,runtime='python'):
    b=bs[i]
    contract={k:b[k] for k in ['practice_anchor','visual_anchor']}
    files={'README.md':'# '+b['context']['concept_name']+'\n\nFictional order-service exercise. Values in fixtures are authored, not observations of a real service.\n\n'+b['practice_anchor']['objective']+'\n\n'+b['practice_anchor']['live_code']['starter_state_intent']+'\n\nSee anchor_contract.json for the supplied success criteria and syntax boundary. Only edit the starter file(s); support files represent the supplied environment.\n',**files,'anchor_contract.json':json.dumps(contract,indent=2)+'\n'}
    assets.append(dict(asset_id='ws.'+b['context']['concept_id'],asset_kind='code_workspace',scenario_id=sid,title=b['context']['concept_name'],runtime=runtime,files=[dict(path=p,content=textwrap.dedent(c).lstrip('\n')) for p,c in files.items()]))
ws(0,{'main.py':'''from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
class OrderInput(BaseModel):
    quantity: int
@app.post('/customers/{customer_id}/orders')
def create_order(customer_id: int, option: str = 'standard'):
    # TODO: declare body: OrderInput, preserving path and query inputs.
    return {'customer_id': customer_id, 'option': option}
'''})
ws(1,{'main.py':'''from fastapi import FastAPI, Depends, HTTPException
from support import acquire_resource
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
''','support.py':'''events = []
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
''','trace_contract.json':json.dumps({'normal':['acquire','yield','operation use','handler completion','response sending'],'exceptional':['acquire','yield','operation use','exception'],'comparison':['default request scope','function scope'],'instruction':'Insert cleanup at the declared scope boundary; re-raise a caught exception that is not intentionally handled.'},indent=2)})
ws(2,{'starter.py':'''import logging
from support import logger, existing_handler, failure_values, captured_output
# TODO: copy the six failure values into event_fields and preserve their
# names in the existing formatter. Emit logger.error(..., extra=event_fields).
logger.error('failed')
''','support.py':'''import io
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
'''})
ws(3,{'starter.py':'''allowed_destinations = {
    'catalog': 'https://catalog.example/lookup',
    'shipping': 'https://shipping.example/lookup',
}
def destination_for_provider(provider: str) -> str:
    # TODO: return only a configured destination; reject unknown keys.
    raise NotImplementedError
''','checks.py':'''from starter import allowed_destinations, destination_for_provider
for provider, destination in allowed_destinations.items():
    assert destination_for_provider(provider) == destination
for value in ['unknown', 'https://arbitrary.example/lookup', '', 'CATALOG']:
    try:
        destination_for_provider(value)
    except ValueError:
        pass
    else:
        raise AssertionError('unknown input was not rejected')
''','boundary.md':'No network is used. Fixed URLs are fictional policy fixtures, not evidence of public address resolution. Destination selection alone does not implement connected-address validation or redirect enforcement.\n'})
ws(4,{'main.py':'''from typing import Annotated
from fastapi import FastAPI, Form, File, UploadFile, Request, HTTPException
from support import RequestBodyLimitMiddleware, BoundedMultipartRoute, budgets
app = FastAPI()
app.router.route_class = BoundedMultipartRoute
# TODO: register RequestBodyLimitMiddleware with budgets['max_body_size'].
@app.post('/orders/attachments')
async def attachment():
    # TODO: bind only metadata and file using Form/File/UploadFile.
    # Validate before processing, read at most budgets['read_size'],
    # and await file.close() in finally.
    raise NotImplementedError
''','support.py':'''from fastapi.routing import APIRoute
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
''','fixtures.json':json.dumps({'budgets':{'max_body_size':4096,'max_files':1,'max_fields':1,'max_part_size':256,'read_size':1024,'metadata_max_length':80},'permitted_content_types':['text/plain'],'cases':['permitted metadata and file','metadata length beyond rule','disallowed file content type','actual bytes including multipart overhead beyond body budget','excess file count','excess field count','non-file field beyond max_part_size','handler rejection closes file']},indent=2),'requirements.txt':'fastapi\npython-multipart\n'})
ws(5,{'main.py':'''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
# TODO: add middleware for https://shop.example with GET, POST,
# Content-Type, and credentials; use explicit lists with no wildcards.
'''})
ws(6,{'main.py':'''from fastapi import FastAPI, Depends
from support import record_execution
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
''','support.py':'''import logging
logger = logging.getLogger('order.provider.exercise')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)
executions = []
def record_execution(value):
    executions.append(value)
    logger.info('provider execution', extra={'event_type': 'provider_execution'})
''','manual_check.md':'Send request A and then request B to GET /orders. Compare shared identity in each response and separate provider executions in the records. No TestClient or HTTPX code is required in the learner file.\n'})
ws(7,{'app.py':'''from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
lifecycle_events = []
@asynccontextmanager
async def lifespan(app):
    lifecycle_events.append('setup')
    try:
        yield
    finally:
        lifecycle_events.append('teardown')
app = FastAPI(lifespan=lifespan)
def order_dependency():
    return {'id': 42, 'quantity': 2}
@app.get('/orders/42')
def get_order(order=Depends(order_dependency)):
    return order
''','test_orders.py':'''from fastapi.testclient import TestClient
from app import app
# TODO: write test_get_order with a TestClient context manager,
# GET /orders/42, and independent status and JSON assertions.
''','requirements.txt':'fastapi\nhttpx\npytest\n'})
ws(8,{'main.py':'''from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.testclient import TestClient
class NoteInput(BaseModel):
    note: str | None
app = FastAPI()
@app.post('/orders/note')
def set_note(body: NoteInput):
    return {'note': body.note}
client = TestClient(app)
# TODO: test {}, {'note': None}, {'note': 'Leave at reception'} separately.
# Repeat after adding = None to the declaration; compare returned values.
''','requests.json':json.dumps([{}, {'note':None},{'note':'Leave at reception'}],indent=2)})
# Extract the exact illustrative OpenAPI excerpt from the glossary.
b=bs[9]; matches=[]
for t in b['teaching_blocks']:
    matches.extend(re.findall(r'```json\s*(.*?)```',t['content'],flags=re.S))
assert len(matches)==1
schema=json.loads(matches[0])
ws(9,{'starter.py':'''from support import schema
# TODO: use paths['/orders']['post'], requestBody and responses,
# then follow references to components.schemas. Assign the definitions
# to variables OrderInput and OrderOutput, not the $ref strings.
''','support.py':'import json\nfrom pathlib import Path\nschema = json.loads(Path(__file__).with_name("openapi_excerpt.json").read_text())\n','openapi_excerpt.json':json.dumps(schema,indent=2)+'\n'})
ws(10,{'main.py':'''from fastapi import FastAPI
app = FastAPI()
# TODO: import and register TrustedHostMiddleware for example.com and
# *.example.com, with www_redirect=False and without the all-host wildcard.
@app.get('/orders')
def orders():
    return {'result': 'host boundary passed'}
''','verify.py':'''from fastapi.testclient import TestClient
from main import app
with TestClient(app) as client:
    for host in ['example.com', 'www.example.com', 'unrelated.example']:
        response = client.get('/orders', headers={'Host': host}, follow_redirects=False)
        print(host, response.status_code)
'''})
ws(11,{'starter.py':'''from support import failure_harness
# TODO: invoke failure_harness(token=..., connection_string=...)
# using recognizable fake values. Assert that neither prohibited string
# occurs in the complete emitted text and that fields['event'] is retained.
''','support.py':'''import io
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
    return {'text': output.getvalue(), 'fields': {
        'event': 'order_failure', 'context': '[REDACTED]'}}
''','synthetic_values.json':json.dumps({'token':'FAKE_ORDER_TOKEN_ABC','connection_string':'FAKE_CONNECTION_SECRET_XYZ','retained_event':'order_failure'},indent=2)})
ws(12,{'starter.py':'''from sqlalchemy.ext.asyncio import async_sessionmaker
from support import engine
# TODO: session_factory = async_sessionmaker(engine)
async def get_session():
    # TODO: async with session_factory() as session: yield session
    raise NotImplementedError
''','support.py':'''from sqlalchemy.ext.asyncio import create_async_engine
engine = create_async_engine('sqlite+aiosqlite:///:memory:')
''','harness.py':'''import asyncio
from starter import get_session
async def lifecycle_check():
    a, b = get_session(), get_session()
    sa, sb = await asyncio.gather(anext(a), anext(b))
    assert sa is not sb
    await a.aclose()
    try:
        await b.athrow(RuntimeError('synthetic request B failure'))
    except RuntimeError:
        pass
    else:
        raise AssertionError('exception was swallowed')
if __name__ == '__main__':
    asyncio.run(lifecycle_check())
''','requirements.txt':'sqlalchemy\naiosqlite\n'})
ws(13,{'main.py':'''import asyncio
from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI
@asynccontextmanager
async def lifespan(app):
    client = httpx.AsyncClient()
    app.state.client = client
    try:
        yield
    finally:
        # TODO: await client.aclose(); record client.is_closed.
        pass
app = FastAPI(lifespan=lifespan)
@app.get('/orders/42')
async def controlled_order():
    print('request_started', flush=True)
    await asyncio.sleep(2)
    print('request_completed', flush=True)
    return {'id': 42, 'quantity': 2}
''','run.sh':'#!/bin/sh\n# TODO: add --timeout-graceful-shutdown with the supplied 5-second limit.\nexec uvicorn main:app --host 127.0.0.1 --port 8000\n','termination_harness.py':'''import json
import os
import signal
import subprocess
import threading
import time
import httpx
# Run after completing main.py and run.sh. Only loopback is contacted.
p = subprocess.Popen(['sh', 'run.sh'], stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT, text=True, start_new_session=True)
events = []
ready = threading.Event()
active = threading.Event()
def collect():
    for line in p.stdout:
        events.append({'at': time.monotonic(), 'line': line.strip()})
        if 'Application startup complete' in line:
            ready.set()
        if 'request_started' in line:
            active.set()
threading.Thread(target=collect, daemon=True).start()
result = {}
def request():
    try:
        r = httpx.get('http://127.0.0.1:8000/orders/42', timeout=10)
        result.update(status=r.status_code, json=r.json())
    except Exception as exc:
        result['error'] = type(exc).__name__
    result['finished_at'] = time.monotonic()
try:
    if not ready.wait(10):
        raise RuntimeError('startup did not complete')
    t = threading.Thread(target=request)
    t.start()
    if not active.wait(10):
        raise RuntimeError('controlled request did not start')
    termination_at = time.monotonic()
    os.killpg(p.pid, signal.SIGTERM)
    t.join(10)
    p.wait(timeout=10)
    print(json.dumps({'supplied_limit_seconds': 5,
        'termination_at': termination_at, 'response': result,
        'events': events}, indent=2))
finally:
    if p.poll() is None:
        os.killpg(p.pid, signal.SIGKILL)
        p.wait()
''','requirements.txt':'fastapi\nuvicorn\nhttpx\n'})
ws(14,{'probes.yaml':'''# TODO: complete each mapping using supplied_values.json.
livenessProbe:
  httpGet: {}
readinessProbe:
  httpGet: {}
''','supplied_values.json':json.dumps({'livenessProbe':{'path':'/live','port':8000,'periodSeconds':10,'failureThreshold':3},'readinessProbe':{'path':'/ready','port':8000,'periodSeconds':5,'failureThreshold':2}},indent=2),'service_contract.md':'Fictional order service: a live process returns a successful liveness status even during temporary required-backend unavailability. Readiness uses a failure status during that outage. HTTP statuses 200 through 399 count as success; other statuses count as failure. A liveness failure reaching its configured threshold can cause restart. A readiness failure reaching its threshold removes traffic eligibility without requiring restart. No endpoint implementation is required.\n'},runtime='yaml')
def dataset(aid,title,columns,rows):
    assets.append(dict(asset_id=aid,asset_kind='dataset',scenario_id=sid,title=title,columns=[dict(name=n,type=t,semantic_role=r,**extra) for n,t,r,extra in columns],rows=rows,variants=[],provenance='authored'))
# Recover the glossary's exact public exchange instead of retyping its output.
order_text='\n'.join(t['content'] for t in bs[7]['teaching_blocks'])
order_response=json.loads(re.search(r'JSON body (\{[^}]+\})',order_text).group(1))
accepted_status=int(re.search(r'return status (\d+)',order_text).group(1))
host_text='\n'.join(t['content'] for t in bs[10]['teaching_blocks'])
rejected_status=int(re.search(r'gets (\d+)',host_text).group(1))
dataset('ds.orders','Synthetic order retrieval fixture',[
    ('id','integer','identifier',{'numeric_looking_label':True,'description':'Synthetic order identifier, not a measured quantity.'}),
    ('quantity','integer','numerical',{'unit':'items'})],
    [[order_response['id'],order_response['quantity']]])
# Boundary predictions from the glossary's exact/subdomain/all-host rules.
# Redirect status is deliberately unspecified: no code is asserted by the glossary.
host_inputs=[
    ('deployment',['example.com','*.example.com'],False,'example.com'),
    ('deployment',['example.com','*.example.com'],False,'www.example.com'),
    ('deployment',['example.com','*.example.com'],False,'unrelated.example'),
    ('exact',['example.com'],False,'www.example.com'),
    ('subdomain wildcard',['*.example.com'],False,'example.com'),
    ('all-host wildcard',['*'],False,'unrelated.example'),
    ('www redirect',['www.example.com'],True,'example.com'),
]
def matches(host, entry):
    return entry=='*' or entry==host or (entry.startswith('*.') and host.endswith(entry[1:]))
host_rows=[]
for policy, entries, redirect, host in host_inputs:
    if any(matches(host,e) for e in entries):
        outcome,status='accepted',accepted_status
    elif redirect and any(matches('www.'+host,e) for e in entries):
        outcome,status='redirected to www.'+host,None
    else:
        outcome,status='rejected',rejected_status
    host_rows.append([policy,', '.join(entries),redirect,host,outcome,status])
dataset('ds.host_checks','Authored host-policy comparison',[
    ('policy','string','categorical',{}),('allowed_hosts','string','text',{}),
    ('www_redirect','boolean','categorical',{}),('Host','string','identifier',{}),
    ('outcome','string','categorical',{}),('status','integer','categorical',{'numeric_looking_label':True,'description':'Predicted HTTP code for the supplied route on accept or host rejection; null means redirect status is not specified by the glossary.'})],host_rows)
registry=dict(schema_version='1.0',kind='scenario_asset_registry',path_id=g['path_id'],batch_id=B.name,
    scenarios=[dict(scenario_id=sid,name='Fictional order-service verification lab',domain='order API',summary='A fictional shop order API supplies isolated request, resource-lifecycle, logging and deployment exercises. All order rows, failure values, destinations and service settings are authored lab fixtures; no external service or production observation is implied.',glossary_example_vocab=vocab)],assets=assets)
(B/'scenario_asset_registry.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n')
# Own checklist: complete batch coverage, row widths and roles, no unused variant
# issue declarations or invalid occurrences, preserve named examples, no plot need.
assert {a['asset_id'][3:] for a in assets if a['asset_kind']=='code_workspace'}=={b['context']['concept_id'] for b in bs}
for a in assets:
    if a['asset_kind']=='dataset':
        assert all(len(row)==len(a['columns']) for row in a['rows'])
        assert len({c['name'] for c in a['columns']})==len(a['columns'])
        for c in a['columns']:
            assert c['semantic_role']!='numerical' or c['type'] in ['integer','number']
            assert c['semantic_role']!='datetime' or c['type'] in ['date','datetime']
    else:
        for f in a['files']:
            if f['path'].endswith('.py'): ast.parse(f['content'])
assert schema['paths']['/orders']['post']['requestBody']['content']['application/json']['schema']['$ref'].endswith('/OrderInput')
assert [order_response['id'],order_response['quantity']] in next(a for a in assets if a['asset_id']=='ds.orders')['rows']
assert all(b['visual_anchor']['type'] in ['code','diagram','process_flow','before_after','data_table'] for b in bs)
print('Checklist PASS:',len(bs),'concepts;',len(assets),'assets;',len(vocab),'vocabulary entries')
