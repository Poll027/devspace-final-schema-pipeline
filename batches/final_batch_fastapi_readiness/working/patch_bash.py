import json,re,base64,zipfile,io,sys
from pathlib import Path
sys.path.insert(0,str(Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
from checkers import sandbox
B=Path('batches/final_batch_readiness')
p=B/'interactions.json'; d=json.loads((B/'working/interactions_before_runtime_repair.json').read_text())
pin=json.loads(Path('00_FINAL_PIPELINE_CORE/registry/runtimes.json').read_text())['runtimes']['python_asgi']['version']
# Preserve the original for narrowly scoped repair assertions.
if not (B/'working/interactions_before_runtime_repair.json').exists():
 (B/'working/interactions_before_runtime_repair.json').write_text(p.read_text())
compat='''import sys, types, inspect
import httpx
from contextlib import contextmanager

def drive(coro):
    try:
        pending=coro.send(None)
        while pending is None:
            pending=coro.send(None)
        raise RuntimeError('This in-process adapter cannot run blocking I/O')
    except StopIteration as done:
        return done.value
request_count=0
class InProcessClient:
    def __init__(self, app, raise_server_exceptions=True):
        self.app=app
        self.http=httpx.AsyncClient(transport=httpx.ASGITransport(app=app,raise_app_exceptions=raise_server_exceptions),base_url='http://exercise')
        self.portal=types.SimpleNamespace(call=lambda fn,*args:drive(fn(*args)))
    def __enter__(self):
        self.life=self.app.router.lifespan_context(self.app)
        drive(self.life.__aenter__())
        return self
    def __exit__(self,*exc):
        drive(self.http.aclose())
        drive(self.life.__aexit__(*exc))
    def request(self,method,path,**kw):
        global request_count
        request_count+=1
        return drive(self.http.request(method,path,**kw))
    def get(self,path,**kw):return self.request('GET',path,**kw)
    def post(self,path,**kw):return self.request('POST',path,**kw)
    def patch(self,path,**kw):return self.request('PATCH',path,**kw)
import fastapi.testclient
fastapi.testclient.TestClient=InProcessClient
# Decorator metadata only. The explicit harness below drives each function and
# yield fixture; there is no pytest process, socket or background thread.
pytest=types.ModuleType('pytest')
def fixture(fn=None,**kw):
    def decorate(f):
        f.__wrapped__=f
        f._fixture=True
        return f
    return decorate(fn) if fn else decorate
def parametrize(names,values,**kw):
    def decorate(f):
        f._parameters=(names,values)
        return f
    return decorate
pytest.fixture=fixture
pytest.mark=types.SimpleNamespace(parametrize=parametrize)
sys.modules['pytest']=pytest
'''
# A sync SQLite implementation of the async session API keeps actual SQLAlchemy
# constraints and transaction rollback in WASM; it does not simulate DB outcomes.
sqlcompat='''from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import asyncio
class AsyncSessionAdapter:
    def __init__(self, engine):
        self.sync_session=Session(engine,expire_on_commit=False)
        self.lock=engine._exercise_lock
    async def __aenter__(self):return self
    async def __aexit__(self,*exc):self.sync_session.close()
    def add(self,value):self.sync_session.add(value)
    async def flush(self):self.sync_session.flush()
    async def scalar(self,q):return self.sync_session.scalar(q)
    async def scalars(self,q):return self.sync_session.scalars(q)
    async def get(self,*a):return self.sync_session.get(*a)
    @asynccontextmanager
    async def begin(self):
        async with self.lock:
            with self.sync_session.begin():yield self
class EngineAdapter:
    def __init__(self,url,**kw):
        self.engine=create_engine(url.replace('sqlite+aiosqlite:', 'sqlite:'),**kw)
        self.engine._exercise_lock=asyncio.Lock()
    @asynccontextmanager
    async def begin(self):
        with self.engine.begin() as c:
            class Connection:
                async def run_sync(self,fn):return fn(c)
            yield Connection()
    async def dispose(self):self.engine.dispose()
class SessionsAdapter:
    def __init__(self,engine,**kw):self.engine=engine.engine
    def __call__(self):return AsyncSessionAdapter(self.engine)
    @asynccontextmanager
    async def begin(self):
        async with self() as session:
            async with session.begin():yield session
create_async_engine=EngineAdapter
async_sessionmaker=SessionsAdapter
'''

def heredocs(s):return {m[0]:m[1] for m in re.findall(r"cat > '([^']+)' <<'(DEVSPACE_FILE_\d+)'\n(.*?)\n\2",s,re.S) for m in [(m[0],m[2]+'\n')]}

def build(files,run):
 return 'from pathlib import Path\nimport json\n# Supplied readonly programs are materialized inside the sandbox workspace.\nprograms = '+repr(files)+'\nfor name, content in programs.items():\n    path=Path(name)\n    path.parent.mkdir(parents=True,exist_ok=True)\n    path.write_text(content)\nimport compatibility\n'+run

for tile in d['tiles']:
 for entry in tile['interactions']:
  x=entry['interaction'];pub=x['public']
  if pub.get('runtime',{}).get('kind')!='bash':continue
  sid=entry['step_id'];ws={f['path']:f['content'] for f in pub['workspace']['files']}
  solmods=heredocs(x['grading']['solution_files'][0]['content'])
  keep={k:v for k,v in ws.items() if k.endswith('.json') or k.endswith('.py') or k.endswith('.md')}
  keep.pop('README.md',None);keep.pop('glossary_contract.json',None);keep.pop('provisioning.json',None)
  keep['compatibility.py']=compat
  if sid in ['tile_091.s09','tile_097.s05','tile_097.s09','tile_097.s13']:
   jwtzip=zipfile.ZipFile('00_FINAL_PIPELINE_CORE/sandbox/node_modules/pyodide/PyJWT-2.10.1-py3-none-any.whl')
   keep.update({k:jwtzip.read(k).decode() for k in jwtzip.namelist() if k.startswith('jwt/') and k.endswith('.py')})
  cases=[];run='';note=''
  if sid=='tile_086.s04':
   # No provider SDK is installed in the pinned sandbox. Keep the taught
   # verification gate with a supplied deterministic verification callable.
   keep['stripe.py']="class SignatureVerificationError(ValueError): pass\nclass error: SignatureVerificationError=SignatureVerificationError\n"
   scaffold=keep['scaffold.py']
   scaffold=scaffold.replace('import stripe','import stripe\nimport hashlib,hmac,json')
   scaffold=re.sub(r'stripe.Webhook.construct_event\([^\n]+',"provider_verify(raw_body, signature, signing_secret)",scaffold)
   # Replace the SDK call with a raw-byte contract adapter, not an SDK claim.
   scaffold=scaffold.replace('provider_verify(raw_body, signature, signing_secret)','provider_verify(raw, signature, signing_secret)')
   scaffold=scaffold.replace('# Test-only snapshot: Stripe SDK still verifies the signature. Suppress age\n# expiry of a stored teaching fixture; do not use tolerance=0 in deployment.', '# Supplied raw-byte contract adapter; SDK execution is unavailable here.')
   scaffold=scaffold.replace('# Fail during setup if the supplied fixture is not actually SDK-verifiable.', '# Check the supplied signed fixture against the raw-byte contract.')
   scaffold=scaffold.replace('def publisher_verifier', "def provider_verify(raw, signature, signing_secret):\n    parts=dict(part.split('=',1) for part in signature.split(','))\n    expected=hmac.new(signing_secret.encode(),parts['t'].encode()+b'.'+raw,hashlib.sha256).hexdigest()\n    if not hmac.compare_digest(expected,parts.get('v1','')):raise stripe.error.SignatureVerificationError('Invalid signature')\n    return json.loads(raw)\ndef publisher_verifier")
   keep['scaffold.py']=scaffold
   print(sid,'scaffold',scaffold)
   cases=['valid','modified','absent'];run="from test_delivery import test_delivery, processed_events\ndef run_case(case):\n    processed_events.clear()\n    test_delivery(case)\n    return {'case':case,'processed_count':len(processed_events)}\n"
   note='This pinned-runtime lab uses a supplied raw-byte verifier adapter; it does not execute the native Stripe SDK.'
  elif sid=='tile_087.s04':
   run="import starter as s\ndef run_case(case):\n    exec(programs['check_diagnosis.py'], {})\n    return {'case':case,'outcome':s.controlled_outcome,'boundary':s.suspected_boundary,'comparison':s.comparison}\n"
   cases=['signals','correlation']
   keep['check_diagnosis.py']=solmods.pop('check_diagnosis.py')
  elif sid=='tile_088.s05':
   z=zipfile.ZipFile(io.BytesIO(base64.b64decode(ws[next(k for k in ws if k.endswith('.whl.b64'))])))
   # Use the real supplied maintained middleware source without installing a
   # second Starlette distribution over the pinned FastAPI dependency.
   keep['body_limit.py']=z.read('starlette/middleware/body_limit.py').decode().replace('from starlette.exceptions import','from starlette.exceptions import')
   for pool in (keep,solmods):
    if 'application.py' in pool:pool['application.py']=pool['application.py'].replace('from starlette.middleware.body_limit import','from body_limit import')
   keep['launch.sh']=ws['launch.sh'];solmods['launch.sh']=solmods.get('launch.sh',ws['launch.sh'])
   cases=['within_batch','beyond_batch','within_body','beyond_body']
   run="import application\nfrom test_boundaries import test_boundary\ndef run_case(case):\n    test_boundary(case)\n    from pathlib import Path\n    assert application.outbound_timeout.read == application.budgets['dependency_timeout_seconds']\n    assert '--limit-concurrency '+str(application.budgets['limit_concurrency']) in Path('launch.sh').read_text()\n    return {'case':case,'timeout':application.outbound_timeout.read,'concurrency':application.budgets['limit_concurrency']}\n"
   note='HTTP requests run in-process. The supplied Uvicorn launch command is inspected, not launched.'
  elif sid=='tile_090.s06':
   keep['test_items.py']=solmods.pop('test_items.py')
   cases=['write_first','absence_first','failure_cleanup']
   run="from starter import isolated_client\nfrom test_items import test_writes_item,test_item_absent\nfrom application import app,engine,Item\nfrom sqlalchemy.orm import Session\ndef run_case(case):\n    if case=='failure_cleanup':\n        exec(programs['check_failure_cleanup.py'], {})\n    else:\n        tests=[test_writes_item,test_item_absent] if case=='write_first' else [test_item_absent,test_writes_item]\n        for test in tests:\n            g=isolated_client()\n            value=next(g)\n            try:test(value)\n            finally:g.close()\n    with Session(engine) as s:\n        assert s.get(Item,json.loads(programs['fixtures.json'])['item']['id']) is None\n    return {'case':case,'isolated':True}\n"
   note='The supplied fixture decorator records metadata; the in-process harness drives each yield fixture and failure cleanup explicitly, without a pytest process.'
  elif sid=='tile_091.s05':
   # Smallest allowed task: selecting configuration. Do not counterfeit an
   # established issuer, JWKS network exchange or issuer-issued valid token.
   for pool in (keep,solmods):
    pool['starter.py']=pool['starter.py'].replace('from acquisition_harness import AcquisitionHarness','').replace('    existing_verifier.configure(trust_configuration)\n    return AcquisitionHarness(client_configuration).acquire()',"    return {'client':client_configuration,'trust':trust_configuration}")
   cases=['registered_client','trusted_verifier'];run="from starter import integrate\nconfiguration=json.loads(programs['issuer_configuration.json'])\ndef run_case(case):\n    result=integrate(configuration,None)\n    return result['client' if case=='registered_client' else 'trust']\n"
   note='Configuration-only pinned-runtime lab: select supplied registered-client and verifier settings. The native established issuer cannot run here; no issuer-acquired token or live acceptance/rejection is claimed.'
  elif sid=='tile_091.s09':
   cases=['verified_with_permission','verified_without_permission']
   run="exec(programs['prepare_credentials.py'], {})\nfrom test_permissions import test_modify\nfrom application import order\ndef run_case(case):\n    test_modify(case)\n    return {'case':case,'public_order':dict(order)}\n"
  elif sid=='tile_093.s04':
   keep['sql_adapter.py']=sqlcompat
   keep['application.py']=keep['application.py'].replace('from sqlalchemy.ext.asyncio import','from sql_adapter import')
   # Replace native threaded dispatch with cooperative in-process requests.
   code=solmods['delivery_checks.py'].replace('from concurrent.futures import ThreadPoolExecutor','')
   code=re.sub(r'                with ThreadPoolExecutor\(max_workers=2\) as workers:\n                    responses=.*?\n',"                responses=[client.post('/authenticated-events',json=event),client.post('/authenticated-events',json=event)]\n",code)
   solmods['delivery_checks.py']=code
   cases=['sequential','restart','failure','concurrent'];run="from delivery_checks import scenario\nimport httpx,asyncio,tempfile\nfrom pathlib import Path\nimport application\nasync def concurrent_case():\n    with tempfile.TemporaryDirectory() as folder:\n        application.DATABASE='sqlite+aiosqlite:///'+str(Path(folder)/'concurrent.sqlite')\n        app=application.make_app()\n        event=application.fixtures['authenticated_events'][0]\n        async with app.router.lifespan_context(app):\n            before=await application.snapshot(app)\n            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://exercise') as client:\n                responses=await asyncio.gather(client.post('/authenticated-events',json=event),client.post('/authenticated-events',json=event))\n            after=await application.snapshot(app)\n            assert all(r.status_code==200 and r.json()=={'received':True} for r in responses)\n            assert after['events']==[event['publisher_event_id']]\n            expected=[dict(row) for row in before['orders']]\n            for row in expected:\n                if row['id']==event['order_id']:row['status']=event['new_status']\n            assert after['orders']==expected\n            return {'case':'concurrent','contracts_passed':True}\ndef run_case(case):\n    if case=='concurrent':return concurrent_case()\n    scenario(case)\n    return {'case':case,'contracts_passed':True}\n"
   note='Uses real SQLite constraints and transactions through a synchronous SQLAlchemy adapter. Sequential, retained-database restart, rollback and two concurrent in-process requests execute. A supplied lock serializes SQLite transaction access; no native threaded concurrency is claimed.'
  elif sid=='tile_093.s13':
   adapter=keep['adapter.py']
   adapter=adapter.replace('from tenacity import Retrying, retry_if_exception','')
   cut=adapter.index('    runner=Retrying(')
   adapter=adapter[:cut]+"    attempt=0\n    while True:\n        attempt+=1\n        try:return transport()\n        except ControlledFailure as failure:\n            if not retry(failure):raise\n            delay=server_delay(failure.retry_after,clock.now()) if policy['retry_after'] else None\n            delay=delay if delay is not None else min(2**(attempt-1),policy['bounded_backoff'])\n            if attempt>=policy['max_attempts'] or clock.elapsed-start+delay>=policy['total_time_budget']:raise\n            clock.sleep(delay)\n"
   keep['adapter.py']=adapter
   cases=['transient','delays','exhaustion','unsafe_post'];run="import checks\nfrom starter import policy\ndef run_case(case):\n    getattr(checks,case)()\n    return {'case':case,'policy':policy}\n"
   note='The supplied deterministic in-process adapter checks the same policy contracts, including both Retry-After forms, finite exhaustion and unsafe repetition. This does not run the native Tenacity distribution.'
  elif sid in ['tile_097.s05','tile_097.s09']:
   # Schema generation does not invoke the existing verifier or the issuer.
   # Its imports are kept; the native PyJWKClient cache must not fetch JWKS
   # merely to construct declarations.
   keep['existing_verifier.py']=keep['existing_verifier.py'].replace("self.jwks=PyJWKClient(configuration['jwks_url'])","self.jwks=None  # lazy JWKS client: schema generation performs no network I/O")
   keep['existing_verifier.py']=keep['existing_verifier.py'].replace('signing_key=self.jwks.get_signing_key_from_jwt(token)',"if self.jwks is None:self.jwks=PyJWKClient(self.configuration['jwks_url'])\n            signing_key=self.jwks.get_signing_key_from_jwt(token)")
   if sid=='tile_097.s05':
    keep['check_declarations.py']=solmods.pop('check_declarations.py')
    cases=['schemes','operations'];run="from application import app\ndef run_case(case):\n    exec(programs['check_declarations.py'], {})\n    schema=app.openapi()\n    return schema['components']['securitySchemes'] if case=='schemes' else {p:{m:v.get('security') for m,v in ops.items()} for p,ops in schema['paths'].items()}\n"
   else:
    cases=['model_and_status','security_metadata'];run="from application import app,security_configuration\nfrom models import OrderInput,PublicOrder,ErrorBody\nfrom starter import audit\nfrom fastapi.testclient import TestClient\ndef run_case(case):\n    with TestClient(app) as client:\n        findings=audit(client,{'OrderInput':OrderInput,'PublicOrder':PublicOrder,'ErrorBody':ErrorBody},json.loads(programs['http_evidence.json']),security_configuration)\n    return [f for f in findings if (f['dimension'].startswith('security') or f['dimension']=='operation_security') == (case=='security_metadata')]\n"
  elif sid=='tile_097.s13':
   cases=[c['credential_condition'] for c in json.loads(keep['fixtures.json'])['cases']]
   run="exec(programs['prepare_credentials.py'], {})\nfrom test_trust import unused\n" if False else "exec(programs['prepare_credentials.py'], {})\nfrom starter import test_order_gate\nimport compatibility\nfixtures=json.loads(programs['fixtures.json'])\ndef run_case(case):\n    record=next(c for c in fixtures['cases'] if c['credential_condition']==case)\n    before=compatibility.request_count\n    test_order_gate(record)\n    assert compatibility.request_count > before, 'No HTTP request executed'\n    return {'case':case,'declared_status':record['declared_status'],'public_body':json.loads(record['safe_body_or_public_result'])}\n"
  else:raise AssertionError(sid)
  remove={'capture.py','issuer_service.py','acquisition_harness.py','run_orders.py','install_middleware.py','run_sequential.py','run_restart.py','run_concurrent.py','run_failure.py','run_transient.py','run_delays.py','run_exhaustion.py','run_unsafe_post.py','run_audit.py'}
  for name in remove:keep.pop(name,None);solmods.pop(name,None)
  startermods=dict(keep); solutionmods={**keep,**solmods}
  # Validation is performed by real calls, and expectations are supplied by
  # running the solution in the pinned engine below, not typed by hand.
  def endpoint(mods):
   prefix=build(mods,'')
   return prefix+"from fastapi import FastAPI\ngrade_app=FastAPI()\nasync def grade(body:dict):\n    namespace={'programs':programs,'json':json}\n    exec("+repr(run)+",namespace)\n    result=namespace['run_case'](body['case'])\n    import inspect\n    return await result if inspect.isawaitable(result) else result\ngrade_app.add_api_route('/grade',grade,methods=['POST'])\n"
  starter=endpoint(startermods);solution=endpoint(solutionmods)
  pub['runtime']={'kind':'python_asgi','version':pin,'packages':['fastapi','httpx']+(['pydantic'] if any('from pydantic' in c for c in solutionmods.values()) else [])+(['sqlalchemy'] if any('from sqlalchemy' in c for c in solutionmods.values()) else [])+(['pyjwt'] if 'jwt/__init__.py' in solutionmods else [])}
  pub['workspace']={'entry':'exercise.py','files':[{'path':'exercise.py','content':starter,'role':'editable','language':'python'}],'asset_mounts':[]}
  oldprompt=pub['prompt'].split(' Edit the embedded files')[0]
  oldprompt=oldprompt.replace('using the actual Stripe SDK verifier','using the supplied raw-byte verification callable').replace('for the maintained Tenacity adapter','for the supplied deterministic policy adapter')
  pub['prompt']=oldprompt+' Edit the embedded Python programs in exercise.py. The supplied in-process harness runs the cases '+', '.join(cases)+'. Each case must satisfy its complete supplied assertions. '+note
  if sid=='tile_091.s05':
   pub['prompt']=note+' Complete only the supplied mappings in starter.py embedded in exercise.py. Use the registered settings and budgets in the embedded fixture, without inventing values. The grader reads '+', '.join(cases)+'.'
  x['grading']={'solution_files':[{'path':'exercise.py','content':solution}],'tests':[]}
  probes=[{'id':str(j),'kind':'http','app':'grade_app','requests':[{'method':'POST','path':'/grade','json':{'case':c}}]} for j,c in enumerate(cases)]
  result=sandbox.node_run(sandbox._py_job('python_asgi',pub['runtime']['packages'],[sandbox._py_script('solution','exercise.py',solution,[],probes)]),sandbox.RUNTIMES['python_asgi']['runner'])['results']['solution']
  (B/'working'/f'{sid}.probe.json').write_text(json.dumps(result,indent=2))
  if not result['ok'] or any(not q['ok'] for q in result.get('probes',{}).values()):
   print('PROBE FAILURE',sid,json.dumps(result)[:3000]);continue
  for j,c in enumerate(cases):
   x['grading']['tests'].append({'test_id':'case_'+str(j),'kind':'http_equals','spec':{'app':'grade_app','requests':[{'method':'POST','path':'/grade','json':{'case':c}}],'expected':{'status':result['probes'][str(j)]['value']['status'],'json':result['probes'][str(j)]['value']['json']}},'visible':True,'message_on_fail':'Complete the supplied case assertions and preserve the declared boundary.'})
  print('PATCHED',sid,len(cases))
p.write_text(json.dumps(d,indent=2)+'\n')
