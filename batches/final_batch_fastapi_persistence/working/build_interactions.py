import json,sys,textwrap,re,zipfile,ast
from pathlib import Path
B=Path('batches/final_batch_persistence')
sys.path.insert(0,str(Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
from checkers import sandbox
R=json.loads((B/'scenario_asset_registry.json').read_text()); P=json.loads((B/'tile_plans.json').read_text()); S=json.loads((B/'screens.json').read_text()); G=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
gloss={x['context']['concept_id']:x for x in G['bundles']}
assets={a['asset_id']:a for a in R['assets']}
def files(cid):return {f['path']:f['content'] for f in assets['ws.'+cid]['files']}
def contract(cid):return json.loads(files(cid)['contract.json'])
def ded(s):return textwrap.dedent(s).lstrip('\n')
exercises={}
def exercise(cid,prompt,starter,solution,harness='',prefix='',cases=None,packages=None,mounts=None):
 if 'return asyncio.run(run())' in harness:
  harness=re.sub(r'^def (check_[a-z_]+)\(',r'async def \1(',harness,flags=re.M).replace('return asyncio.run(run())','return await run()')
 cases=cases or []
 if any(t['kind']=='function_call' for t in cases):
  harness+=ded("""
import inspect
from fastapi import FastAPI
if 'app' not in globals(): app=FastAPI()
@app.post('/__exercise_check')
async def exercise_check(payload: dict):
    result=globals()[payload['function']](*payload.get('args',[]))
    if inspect.isawaitable(result): result=await result
    return result
""")
  cases=[{'kind':'http_equals','spec':{'requests':[{'method':'POST','path':'/__exercise_check','json':{'function':t['spec']['function'],'args':t['spec'].get('args',[])}}]}} if t['kind']=='function_call' else t for t in cases]
 exercises[cid]={'prompt':prompt,'starter':prefix+'\n# BEGIN LEARNER EDITS\n'+starter+'\n# END LEARNER EDITS\n'+harness,'solution':prefix+'\n# BEGIN LEARNER EDITS\n'+solution+'\n# END LEARNER EDITS\n'+harness,'cases':cases,'packages':packages or [],'mounts':mounts or []}
def call(fn,*args):return {'kind':'function_call','spec':{'function':fn,'args':list(args)}}
def http(path,**kwargs):return {'kind':'http_equals','spec':{'requests':[{'method':kwargs.pop('method','GET'),'path':path,**kwargs}]}}
# Supplied executable SQLAlchemy adapter: real local SQLite persistence, synchronous driver behind awaitable exercise interface.
ORM=ded('''
import asyncio,csv,json,ast
from pathlib import Path
from sqlalchemy import create_engine,Integer,String,select,text
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,Session as SyncSession
class Base(DeclarativeBase): pass
class Order(Base):
    __tablename__='orders'
    id: Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True)
    external_reference: Mapped[str]=mapped_column(String,unique=True)
    note: Mapped[str]=mapped_column(String)
    quantity: Mapped[int]=mapped_column(Integer)
    processing: Mapped[str]=mapped_column(String)
Entity=Order
class AsyncAdapter:
    def __init__(self,engine,fail=False):
        self.inner=SyncSession(engine,expire_on_commit=False);self.fail=fail;self.events=[]
    async def __aenter__(self): return self
    async def __aexit__(self,*args): self.inner.close()
    async def get(self,cls,key):
        self.events.append('get');return self.inner.get(cls,key)
    def add(self,obj): self.events.append('add');self.inner.add(obj)
    async def flush(self):
        self.events.append('flush')
        if self.fail: raise RuntimeError('synthetic flush failure')
        self.inner.flush()
    async def commit(self):
        self.events.append('commit')
        if self.fail: raise RuntimeError('synthetic commit failure')
        self.inner.commit()
    async def rollback(self): self.events.append('rollback');self.inner.rollback()
    async def delete(self,obj): self.events.append('delete');self.inner.delete(obj)
    async def scalars(self,stmt): return self.inner.scalars(stmt)
    async def execute(self,stmt,params=None): return self.inner.execute(stmt,params or {})
def make_store():
    engine=create_engine('sqlite:///:memory:');Base.metadata.create_all(engine)
    with open('orders.csv',newline='') as f: rows=list(csv.DictReader(f))
    with SyncSession(engine) as s:
        s.add_all([Order(id=int(r['id']),external_reference=r['external_reference'],note=r['note'],quantity=int(r['quantity']),processing=r['processing']) for r in rows]);s.commit()
    return engine,lambda:AsyncAdapter(engine)
def snapshot(obj):
    return None if obj is None else {k:getattr(obj,k) for k in ('id','external_reference','note','quantity','processing')}
def learner_source():
    content=Path('exercise.py').read_text()
    return content.split('# BEGIN LEARNER EDITS\\n',1)[1].split('# END LEARNER EDITS',1)[0]
''')
orders=[{'asset_id':'ds.orders','mount_path':'orders.csv'}]
c='sqlalchemy.retrieve_resource'
exercise(c,'Complete retrieve(session, identity): await the Order primary-key lookup, explicitly branch on entity is None before using any attributes, returning None for absence and the entity otherwise. The supplied harness calls existing and absent identities and returns their persisted fields; leave the adapter and harness unchanged.',files(c)['starter.py'].replace('from support import Order\n',''),ded('''
async def retrieve(session, identity):
    entity = await session.get(Order, identity)
    if entity is None:
        return None
    else:
        return entity
'''),ded('''
def check_retrieve(identity):
    async def run():
        engine,factory=make_store()
        async with factory() as session:
            result=await retrieve(session,identity)
            tree=ast.parse(learner_source())
            branch=any(isinstance(n,ast.If) and isinstance(n.test,ast.Compare) and any(isinstance(o,ast.Is) for o in n.test.ops) and any(isinstance(v,ast.Constant) and v.value is None for v in n.test.comparators) for n in ast.walk(tree))
            assert branch,'Explicit None branch required'
            return snapshot(result)
    return asyncio.run(run())
'''),ORM,[call('check_retrieve',i) for i in contract(c)['existing_identities'][:2]+contract(c)['absent_identities']],['sqlalchemy'],orders)
c='sqlalchemy.transaction_boundaries'
prefix=ded('''
import asyncio
''')+files(c)['starter.py'].split('async def related_writes')[0]+files(c)['support.py'].replace('from starter import WriteFailure\n','')
starter=files(c)['starter.py'].split('async def related_writes',1)[1];starter='async def related_writes'+starter
solution=ded('''
async def related_writes(session):
    async with session.begin():
        await first_order_write(session)
        await second_order_write(session)
async def recover_failed_flush(session):
    try:
        await session.flush()
    except WriteFailure:
        await session.rollback()
    await session.reuse()
''')
harness=ded('''
def check_transaction(case):
    async def run():
        s=Session(fail_second=case=='failing_second_write',fail_flush=case=='failed_flush_then_reuse')
        if s.fail_flush: await recover_failed_flush(s)
        else:
            try: await related_writes(s)
            except WriteFailure: pass
        return {'durable':s.durable,'pending':s.pending,'failed':s.failed,'rollbacks':s.rollback_calls}
    return asyncio.run(run())
''')
exercise(c,'Wrap the two provided writes in one session.begin() scope. Complete only the rollback placeholder in the supplied standalone flush-failure branch before reuse. The harness checks success, a second-write exception, and flush-failure recovery; do not catch the write exception inside the transaction.',starter,solution,harness,prefix,[call('check_transaction',v) for v in contract(c)['cases']])
c='auth.bearer_dependency'
solution=files(c)['starter.py'].replace('async def credential():','def credential(credential: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]):').replace('    raise NotImplementedError',"    assert credential.scheme == 'Bearer'\n    assert credential.credentials != ''\n    return {'accepted': True}")
exercise(c,'Declare HTTPBearer() with its default auto_error=True as the Annotated dependency on /credential. Inside the handler assert that scheme is Bearer and credential text is nonempty, without returning or logging that text. Return only {"accepted": True}. Run the four header cases; extraction alone does not verify credential validity.',files(c)['starter.py'],solution,cases=[http('/credential',headers=v['headers']) for v in contract(c)['cases']],packages=['fastapi'])
# Endpoint-ready cache/primary adapters from registry (not a real network Redis deployment).
CACHE=ded('''
import asyncio,csv,time,json
from pathlib import Path
''')+files('cache.redis_cache_aside')['support.py'].replace('import csv\n','').replace('import time\n','').replace('from pathlib import Path\n','')
CACHE=CACHE.replace('Path(__file__).with_name("orders.csv")','Path("orders.csv")').replace('from redis.exceptions import ConnectionError, TimeoutError\n','')
c='cache.redis_cache_aside'
solution=ded('''
async def read_order(order_id, representation, cache, primary_store):
    key = f"order:{order_id}:{representation}"
    order = await cache.get(key)
    if order is not None:
        return order
    order = await primary_store.load_order(order_id, representation)
    await cache.set(key, order)
    return order
''')
# PrimaryStore registry adapter names load, glossary names load_order. Supplied alias, no learner change.
prefix=CACHE
harness=ded('''
def check_cache(order_id,representation):
    async def run():
        cache=Cache();primary=PrimaryStore()
        first=await read_order(order_id,representation,cache,primary)
        second=await read_order(order_id,representation,cache,primary)
        assert len(primary.calls)==1 and first==second,'Repeat must hit cache'
        other=await read_order(43 if order_id==42 else 42,representation,cache,primary)
        alternate=await read_order(order_id,'quantity' if representation=='notes' else 'notes',cache,primary)
        assert len(cache.entries)==3,'Identity and representation need distinct keys'
        assert cache.calls[0][0]=='get','Cache first'
        return {'first':first,'repeat':second,'other':other,'alternate':alternate,'loads':primary.calls,'keys':sorted(cache.entries)}
    return asyncio.run(run())
''')
exercise(c,'Complete read_order: build order:{order_id}:{representation}, get the cache first, return hits, and on a miss load from primary_store.load_order, cache and return the endpoint-ready result. The read-heavy fixture permits reuse. Tests repeat identical reads and change identity/representation. Leave the adapters and check_cache unchanged.',files(c)['starter.py'],solution,harness,prefix,[call('check_cache',*v) for v in contract(c)['requests'][:3]],mounts=orders)
c='database.alembic_migrations'
solution=ded('''
def upgrade():
    # REVIEW: possible rename; withhold approval pending clarification.
    # REVIEW: manual correction required before approval.
    # REVIEW: test-database upgrade and downgrade verification required before approval.
    # REVIEW: alembic upgrade head followed by alembic downgrade revision on a test database.
    pass

def downgrade():
    # REVIEW: recreating a column does not restore deleted data.
    # REVIEW: manual correction required before approval.
    # REVIEW: test-database upgrade and downgrade verification required before approval.
    # REVIEW: alembic upgrade head followed by alembic downgrade revision on a test database.
    pass
''')
harness=ded('''
def check_review(direction):
    src=Path('exercise.py').read_text().split('# BEGIN LEARNER EDITS\\n',1)[1].split('# END LEARNER EDITS',1)[0]
    block=src.split('def '+direction+'():',1)[1].split('def ',1)[0].lower()
    assert 'manual correction' in block and 'before approval' in block
    assert 'test-database upgrade and downgrade verification' in block
    assert 'alembic upgrade head' in block and 'alembic downgrade revision' in block
    if direction=='upgrade': assert 'possible rename' in block and 'withhold approval pending clarification' in block
    else: assert 'does not restore deleted data' in block
    return {'direction':direction,'review': [line.strip()[2:] for line in block.splitlines() if line.strip().startswith('# review:')]}
''')
exercise(c,'Review only; do not execute schema changes. In upgrade() add REVIEW comments stating "possible rename", "manual correction required before approval", and "test-database upgrade and downgrade verification required before approval". In downgrade() state "recreating a column does not restore deleted data" and the same correction and verification requirements. Leave both pass statements. These phrases make the review findings machine-checkable, not approval to apply the candidate.',files(c)['starter.py'],solution,harness,'from pathlib import Path\n',[call('check_review',d) for d in contract(c)['directions']])
exercises[c]['prompt']+='\nCandidate generated revision to review (do not execute):\n'+json.dumps({k:contract(c)[k] for k in ('candidate','directions','review_only','database_execution')},indent=2)
c='database.service_query_indexes';cc=contract(c)
# SQL inside a supplied Python carrier: SQLite executes exactly the basic declaration, no query syntax added by learner.
starter='proposal = """\n'+files(c)['starter.sql']+'"""\n'
solution='proposal = """\nCREATE INDEX '+cc['index_name']+' ON '+cc['table']+' ('+cc['column']+');\n-- Frequent equality lookups justify this B-tree candidate.\n-- Extra storage and maintenance during writes; no guaranteed performance gain.\n"""\n'
harness=ded('''
def check_index(reference):
    assert 'frequent equality' in proposal.lower() and 'b-tree' in proposal.lower()
    assert 'storage' in proposal.lower() and 'maintenance during writes' in proposal.lower()
    assert 'no guaranteed performance gain' in proposal.lower()
    engine,factory=make_store()
    with engine.begin() as connection:
        connection.exec_driver_sql(proposal)
        names=connection.exec_driver_sql("PRAGMA index_info('"+index_name+"')").fetchall()
        assert [r[2] for r in names]==[index_column]
        return {'index_columns':[r[2] for r in names],'matching_ids':[r[0] for r in connection.execute(text('SELECT id FROM orders WHERE external_reference=:reference'),{'reference':reference})]}
''')
exercise(c,'Edit only the SQL proposal string: write CREATE INDEX '+cc['index_name']+' ON '+cc['table']+' ('+cc['column']+'); and SQL comments saying "Frequent equality lookups" justify a "B-tree" candidate with "Extra storage" and "maintenance during writes" and "no guaranteed performance gain". The supplied carrier verifies the basic declaration on local SQLite, not PostgreSQL performance. No other SQL statements are needed.',starter,solution,harness,ORM+'\nindex_name='+repr(cc['index_name'])+'\nindex_column='+repr(cc['column'])+'\n',[call('check_index',v) for v in [assets['ds.orders']['rows'][0][1],assets['ds.orders']['rows'][1][1]]],['sqlalchemy'],orders)
c='design.api_persistence_model_boundaries'
solution=files(c)['starter.py'].replace('    pass  # TODO: public input fields','    note: str\n    quantity: int').replace('    pass  # TODO: public output fields and attribute-validation configuration','    model_config = ConfigDict(from_attributes=True)\n    id: int\n    note: str\n    quantity: int').replace('@app.get("/orders/42")','@app.get("/orders/42", response_model=PublicOutput)')
harness=ded('''
def check_models(values):
    assert PublicInput is not PublicOutput
    assert set(PublicInput.model_fields)==set(public_input_fields)
    assert set(PublicOutput.model_fields)==set(public_output_fields)
    candidate=SimpleNamespace(**values)
    return {'input':PublicInput.model_validate(values).model_dump(),'output':PublicOutput.model_validate(candidate).model_dump()}
''')
cc=contract(c); prefix='public_input_fields='+repr(cc['public_input_fields'])+'\npublic_output_fields='+repr(cc['public_output_fields'])+'\n'
exercise(c,'Define distinct PublicInput (note: str, quantity: int) and PublicOutput (id: int, note: str, quantity: int), configure PublicOutput for validation from attributes, and set it as /orders/42 response_model. Do not declare processing or external_reference in public models. Tests validate input/output and ensure the HTTP result exposes only the output fields.',files(c)['starter.py'],solution,harness,prefix,[http('/orders/42'),call('check_models',cc['row']),call('check_models',dict(cc['row'],note='another public note',quantity=7))],['fastapi','pydantic'])
c='fastapi.domain_error_translation'
solution=files(c)['starter.py'].replace('    raise NotImplementedError','    await session.rollback()\n    raise FailureClass()',1).replace('async def handle_failure(request, exception):\n    raise NotImplementedError','@app.exception_handler(FailureClass)\nasync def handle_failure(request, exception):\n    return JSONResponse(status_code=409, content={"detail": "Uniqueness conflict"})')
harness=ded('''
def check_recovery(initial_failed):
    async def run():
        s=FailedSession();s.failed=initial_failed
        try: await recover(s)
        except FailureClass:
            assert s.rollback_calls==1 and not s.failed
            return {'raised':'FailureClass','rollbacks':s.rollback_calls,'failed':s.failed,'initial_failed':initial_failed}
        raise AssertionError('Recovery must raise recognized failure after rollback')
    return asyncio.run(run())
''')
exercise(c,'Complete recover(session) by awaiting rollback and then raising FailureClass(). Register handle_failure for FailureClass and return JSONResponse(status_code=409, content={"detail": "Uniqueness conflict"}). This fixed glossary public message replaces private persistence details. Do not reuse the failed session or add persistence writes.',files(c)['starter.py'],solution,harness,'import asyncio\n',[http('/conflict'),call('check_recovery',True),call('check_recovery',False)],['fastapi'])
c='fastapi.public_error_envelopes'
solution=files(c)['starter.py'].replace('async def public_error(request, exception):','@app.exception_handler(StarletteHTTPException)\nasync def public_error(request, exception):').replace('    raise NotImplementedError','    return JSONResponse(status_code=exception.status_code, content={"error": {"reason": "The request could not be completed."}}, headers=exception.headers)')
exercise(c,'Register public_error for StarletteHTTPException. Return the same {"error": {"reason": "The request could not be completed."}} envelope for recognized FastAPI and Starlette HTTP exceptions. Preserve exception.status_code and exception.headers. Do not include raw detail or a stack trace; the supplied routes exercise 401 with WWW-Authenticate and 404 without headers.',files(c)['starter.py'],solution,cases=[http(v['path']) for v in contract(c)['cases']],packages=['fastapi'])
c='fastapi_backend.proxy_header_trust';cc=contract(c)
starter='launch_command = '+repr(files(c)['starter.sh'].splitlines()[1])+'\n'
solution='launch_command = '+repr(files(c)['starter.sh'].splitlines()[1]+' --forwarded-allow-ips '+cc['trusted_proxy_source']+' --root-path '+cc['stripped_prefix'])+'\n'
prefix='import asyncio,shlex,json\nimport httpx\nfrom fastapi import FastAPI\nproxy_contract='+repr(cc)+'\n'
harness=ded('''
def check_proxy(sender):
    async def run():
        argv=shlex.split(launch_command)
        trusted=argv[argv.index('--forwarded-allow-ips')+1];root=argv[argv.index('--root-path')+1]
        assert trusted==proxy_contract['trusted_proxy_source'] and root==proxy_contract['stripped_prefix']
        # Supplied boundary adapter applies forwarded scheme only for explicitly trusted source.
        scheme='https' if sender==trusted else 'http'
        app=FastAPI(root_path=root)
        @app.get('/orders/')
        async def listing(): return {'accepted':True}
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app,client=(sender,1234),root_path=root),base_url=scheme+'://orders.example.test') as cl:
            redirect=await cl.get(root+'/orders',follow_redirects=False)
            docs=await cl.get(root+'/docs');schema=await cl.get(root+'/openapi.json')
            return {'sender':sender,'trust':trusted,'redirect':redirect.headers.get('location'),'docs_has_prefixed_schema':(root+'/openapi.json') in docs.text,'servers':schema.json().get('servers')}
    return asyncio.run(run())
''')
exercise(c,'Edit only launch_command: add --forwarded-allow-ips '+cc['trusted_proxy_source']+' and --root-path '+cc['stripped_prefix']+'. Do not use wildcard trust. The in-process boundary adapter checks redirects and documentation at the public HTTPS prefix for the trusted sender and ignores forwarded HTTPS for a different sender. This verifies configuration intent without launching Uvicorn or a real proxy.',starter,solution,harness,prefix,[call('check_proxy',cc['trusted_proxy_source']),call('check_proxy','192.0.2.11')],['fastapi','httpx'])
c='integration.webhook_contracts';cc=contract(c)
solution=files(c)['starter.py'].replace('    pass  # TODO: required fields from contract.json','    order_id: int\n    event: str').replace('@app.post("/order-events")','@app.post("/order-events", status_code=202)').replace('    raise NotImplementedError','    background_tasks.add_task(downstream, event)\n    return {"accepted": True}')
harness=ded('''
def check_schedule(body):
    async def run():
        class Recorder:
            def __init__(self): self.tasks=[]
            def add_task(self,*args): self.tasks.append(args)
        recorder=Recorder();completed.clear()
        response=await receive(OrderEvent(**body),recorder)
        assert not completed and len(recorder.tasks)==1
        assert recorder.tasks[0][0] is downstream
        return {'ack':response,'scheduled':recorder.tasks[0][1].model_dump(),'completed':completed}
    return asyncio.run(run())
''')
cases=[http('/order-events',method='POST',json=cc['accepted_body'])]+[http('/order-events',method='POST',json=v) for v in cc['invalid_bodies']]+[http('/order-events',method='POST',data='not json',headers={'Content-Type':cc['unsupported_media_type']}),http('/order-events',method='POST',json=cc['accepted_body'],headers={'Content-Type':cc['unsupported_media_type']}),call('check_schedule',cc['accepted_body']),call('check_schedule',dict(cc['accepted_body'],order_id=43))]
# Verify invalid submissions do not schedule by capturing every add_task call during real request validation.
harness+=ded('''
def check_rejected(body,media):
    async def run():
        scheduled=[]
        original=BackgroundTasks.add_task
        def record(self,*args,**kwargs): scheduled.append(args)
        BackgroundTasks.add_task=record
        try:
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as cl:
                r=await cl.post('/order-events',json=body,headers={'Content-Type':media})
            return {'status':r.status_code,'scheduled_count':len(scheduled)}
        finally: BackgroundTasks.add_task=original
    return asyncio.run(run())
''')
cases += [call('check_rejected',v,cc['media_type']) for v in cc['invalid_bodies']]+[call('check_rejected',{},cc['unsupported_media_type'])]
exercise(c,'Complete OrderEvent with required order_id: int and event: str. Declare /order-events status_code=202, add downstream(event) as a BackgroundTasks task, and return only {"accepted": True}. Leave the pre-routing application/json guard unchanged. Check valid 202, invalid 422, unsupported media 415 (including an otherwise invalid body), and the task-recording harness: only accepted delivery schedules work, without executing it inside the handler.',files(c)['starter.py'],solution,harness,'import asyncio,httpx\n',cases,['fastapi','httpx','pydantic'])
c='observability.request_correlation';cc=contract(c)
solution=files(c)['starter.py'].replace('async def read_order(order_id: int):','async def read_order(order_id: int, incoming: Annotated[str | None, Header(alias=header_name)] = None):').replace('    raise NotImplementedError','    identifier = keep_or_create(incoming)\n    logger.info("order request", extra={"interaction_id": identifier})\n    await client.get(url, headers={header_name: identifier})\n    return {"accepted": True}')
harness=ded('''
def check_correlation(inputs):
    async def run():
        class Capture(logging.Handler):
            def emit(self,record): events.append((_request_chain.get(),record.interaction_id))
        class OutboundSpy:
            def __init__(self,wrapped): self.wrapped=wrapped
            async def get(self,url,headers):
                outgoing.append((_request_chain.get(),headers[header_name]))
                return await self.wrapped.get(url,headers=headers)
        global client
        original_client=client;outgoing=[];client=OutboundSpy(client)
        events=[];received.clear();h=Capture();logger.addHandler(h);logger.setLevel(logging.INFO)
        try:
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as cl:
                async def send(i,value):
                    headers={} if value is None else {header_name:value}
                    return await cl.get('/orders/'+str(i),headers=headers)
                responses=await asyncio.gather(*[send(i+42,v) for i,v in enumerate(inputs)])
            outbound=[v[header_name.lower()] for v in received]
            assert sorted(events)==sorted(outgoing) and len(events)==len(inputs)
            assert sorted(v for path,v in outgoing)==sorted(outbound)
            for v in inputs:
                if v and re.fullmatch(r'[A-Za-z0-9-]{1,32}',v): assert v in outbound
            assert all(re.fullmatch(r'[A-Za-z0-9-]{1,32}',v) for v in outbound)
            # Random generated ids checked as policy booleans, not a nondeterministic literal.
            return {'statuses':[r.status_code for r in responses],'valid_preserved':[v for v in inputs if v in outbound],'same_context':sorted(events)==sorted(outgoing),'distinct':len(set(outbound))==len(inputs),'generated_count':sum(v not in inputs for v in outbound)}
        finally:
            logger.removeHandler(h);client=original_client
    return asyncio.run(run())
''')
harness+=ded("""
from contextvars import ContextVar
_request_chain=ContextVar('exercise_request_chain',default='')
@app.middleware('http')
async def supplied_chain_context(request,call_next):
    token=_request_chain.set(request.url.path)
    try: return await call_next(request)
    finally: _request_chain.reset(token)
""")
exercise(c,'Bind incoming through Annotated[str | None, Header(alias=header_name)] with default None. Keep identifier request-local using keep_or_create(incoming); logger.info("order request", extra={"interaction_id": identifier}) and client.get(url, headers={header_name: identifier}) must use that same identifier. Return {"accepted": True}, not credentials or authority claims. Run supplied concurrent accepted, missing and rejected-header cases; leave the policy helper, receiver and logger scaffold unchanged.',files(c)['starter.py'],solution,harness,'import asyncio\n',[call('check_correlation',cc['accepted_ids']),call('check_correlation',[None]+cc['rejected_ids']),call('check_correlation',list(reversed(cc['accepted_ids'])))],['fastapi','httpx'])
c='rest.bounded_resource_listing';cc=contract(c)
starter=files(c)['starter.py'].replace('from support import Order\n','')
solution=starter.replace('page: int = 1, page_size: int = 1','page: int = Query(default=1, ge=1, le=4), page_size: int = Query(default=1, ge=1, le=3)').replace('    raise NotImplementedError','    offset = (page - 1) * page_size\n    statement = select(Entity).where(predicate).order_by(primary_sort_column, unique_key).limit(page_size).offset(offset)\n    result = await session.execute(statement)\n    return result.scalars().all()')
# list(result) is supplied conversion scaffolding; learner only fills selection and Query boundaries.
starter=starter.replace('    raise NotImplementedError','    # TODO: define offset and statement using the supplied selection contract\n    raise NotImplementedError\n    result = await session.execute(statement)\n    return result.scalars().all()')
harness=ded('''
engine,factory=make_store()
app.state.session_factory=factory
def check_pages(page,page_size):
    async def run():
        engine,factory=make_store()
        app.state.session_factory=factory
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as cl:
            r=await cl.get('/orders',params={'page':page,'page_size':page_size})
        return {'status':r.status_code,'rows':r.json() if r.status_code==200 else None}
    return asyncio.run(run())
''')
exercise(c,'Keep the supplied result-to-list return and session dependency. Declare page=Query(default=1, ge=1, le=4) and page_size=Query(default=1, ge=1, le=3). Compute offset=(page - 1)*page_size. Set statement to select(Entity).where(predicate).order_by(primary_sort_column, unique_key).limit(page_size).offset(offset). Tests check adjacent and trailing pages, an empty page, rejected bounds, the queued filter and ascending quantity/id order. Return the supplied OrderResponse columns in their declared order.',starter,solution,harness,ORM+'\nimport httpx\n',[call('check_pages',page,size) for page,size in [(1,3),(2,3),(3,3),(4,3),(0,3),(5,3),(1,0),(1,4)]],['fastapi','httpx','sqlalchemy','pydantic'],orders)
c='security.injection_resistant_inputs';cc=contract(c)
solution=ded('''
from sqlalchemy import text
async def lookup(session, supplied_value):
    statement = text("SELECT field FROM Entity WHERE field = :value")
    return await session.execute(statement, {"value": supplied_value})
''')
prefix=ded('''
import asyncio,csv
from sqlalchemy import create_engine,text
class LookupSession:
    def __init__(self,connection): self.connection=connection;self.sql=None;self.params=None
    async def execute(self,statement,params=None):
        self.sql=str(statement);self.params=params
        return self.connection.execute(statement,params or {})
''')
harness=ded('''
def check_lookup(supplied_value):
    async def run():
        engine=create_engine('sqlite:///:memory:')
        with engine.begin() as con:
            con.execute(text('CREATE TABLE Entity (field TEXT)'))
            with open('Entity.csv',newline='') as f: rows=list(csv.DictReader(f))
            con.execute(text('INSERT INTO Entity (field) VALUES (:field)'),rows)
            session=LookupSession(con);result=await lookup(session,supplied_value)
            assert session.sql=='SELECT field FROM Entity WHERE field = :value' and session.params=={'value':supplied_value}
            return {'rows':[[r[0]] for r in result],'sql':session.sql,'bound_value':session.params['value']}
    return asyncio.run(run())
''')
exercise(c,'Replace interpolated SQL with exactly text("SELECT field FROM Entity WHERE field = :value"), then pass {"value": supplied_value} separately to await session.execute. The harness checks ordinary text, a quote, SQL-looking text and absence as exact-match data, never SQL structure. Do not alter the fixed selected column, table or placeholder.',files(c)['starter.py'],solution,harness,prefix,[call('check_lookup',v) for v in cc['supplied_values']],['sqlalchemy'],[{'asset_id':'ds.entity','mount_path':'Entity.csv'}])
c='sqlalchemy.create_resource';cc=contract(c)
starter=files(c)['starter.py'].replace('from support import Entity\n','')
solution=ded('''
async def create(session, supplied_values, session_factory):
    entity = Entity(external_reference=supplied_values['external_reference'], note=supplied_values['note'], quantity=supplied_values['quantity'], processing=supplied_values['processing'])
    session.add(entity)
    await session.flush()
    identity = entity.id
    await session.commit()
    async with session_factory() as fresh_session:
        stored = await fresh_session.get(Entity, identity)
        assert stored is not None
        assert stored.id == identity
        assert stored.external_reference == supplied_values['external_reference']
        assert stored.note == supplied_values['note']
        assert stored.quantity == supplied_values['quantity']
        assert stored.processing == supplied_values['processing']
    return identity
''')
# Return is scaffold, not an added learner requirement for this anchor.
starter=starter.replace('    raise NotImplementedError','    raise NotImplementedError\n    return identity')
harness=ded('''
def check_create(values):
    async def run():
        engine,factory=make_store()
        async with factory() as s:
            identity=await create(s,values,factory)
            assert s.events[:3]==['add','flush','commit']
        async with factory() as independent:
            stored=await independent.get(Entity,identity)
            return snapshot(stored)
    return asyncio.run(run())
''')
exercise(c,'Construct Entity using every supplied_values field, add it, flush, capture identity=entity.id before commit, then commit. In a fresh session retrieve by identity and assert its id and all four supplied fields match. Keep the scaffold return identity. check_create also independently reloads committed storage; construction alone is insufficient.',starter,solution,harness,ORM,[call('check_create',cc['supplied_values']),call('check_create',dict(cc['supplied_values'],external_reference='ref-another-new',note='another created note',quantity=8))],['sqlalchemy'],orders)
c='sqlalchemy.delete_resource';cc=contract(c)
solution=ded('''
async def delete_order(session, identity):
    entity = await session.get(Order, identity)
    if entity is None:
        return None
    try:
        await session.delete(entity)
        await session.flush()
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    return identity
async def verify_deletion(session_factory, identity, other_identity):
    async with session_factory() as fresh_session:
        target = await fresh_session.get(Order, identity)
        other = await fresh_session.get(Order, other_identity)
        assert target is None
        assert other is not None
''')
harness=ded('''
def check_delete(identity,fail):
    async def run():
        engine,factory=make_store();s=AsyncAdapter(engine,fail)
        raised=False
        try: result=await delete_order(s,identity)
        except RuntimeError: raised=True;result=None
        if fail:
            assert raised and 'rollback' in s.events and 'commit' not in s.events
        elif result is not None: await verify_deletion(factory,identity,other_identity)
        else: assert 'delete' not in s.events
        async with factory() as fresh:
            target=await fresh.get(Order,identity);other=await fresh.get(Order,other_identity)
            return {'target':snapshot(target),'other':snapshot(other),'raised':raised,'events':s.events}
    return asyncio.run(run())
''')
exercise(c,'Complete delete_order: get the identified Order, return None for absence before delete, then await delete, flush and commit. On failure rollback and re-raise, never report success. Return identity after success. Complete verify_deletion using a fresh session to assert target is None and other is not None. The harness tests target '+str(cc['target_identity'])+', absent '+str(cc['absent_identity'])+' and failed flush while preserving order '+str(cc['other_identity'])+'.',files(c)['starter.py'].replace('from support import Order\n',''),solution,harness,ORM+'\nother_identity='+repr(cc['other_identity'])+'\n',[call('check_delete',cc['target_identity'],False),call('check_delete',cc['absent_identity'],False),call('check_delete',cc['target_identity'],True)],['sqlalchemy'],orders)
c='sqlalchemy.update_resource';cc=contract(c)
starter=files(c)['starter.py'].replace('from support import Order\n','')
solution=starter.replace('    raise NotImplementedError',ded('''
    order = await session.get(Order, order_id)
    original_quantity = order.quantity
    changes = request.model_dump(exclude_unset=True)
    for field, value in changes.items():
        if field in permitted_fields:
            setattr(order, field, value)
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    async with session_factory() as session:
        stored = await session.get(Order, order_id)
        assert stored.note == request.note
        assert stored.quantity == original_quantity
''').rstrip().replace('\n','\n    ').join(['    ','']))
# Replace indentation construction above with a straightforward block.
solution=starter.split('async def update_order')[0]+ded('''
async def update_order(session, order_id, request, session_factory):
    order = await session.get(Order, order_id)
    original_quantity = order.quantity
    changes = request.model_dump(exclude_unset=True)
    for field, value in changes.items():
        if field in permitted_fields:
            setattr(order, field, value)
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    async with session_factory() as session:
        stored = await session.get(Order, order_id)
        assert stored.note == request.note
        assert stored.quantity == original_quantity
''')
harness=ded('''
def check_update(body,fail):
    async def run():
        engine,factory=make_store();s=AsyncAdapter(engine,fail)
        raised=False
        try: await update_order(s,order_id,PartialUpdate(**body),factory)
        except RuntimeError: raised=True
        if fail: assert raised and s.events[-1]=='rollback'
        async with factory() as fresh:
            stored=await fresh.get(Order,order_id)
            return {'stored':snapshot(stored),'raised':raised,'events':s.events}
    return asyncio.run(run())
''')
exercise(c,'For the supplied note-only PartialUpdate, load Order, capture its original quantity, obtain model_dump(exclude_unset=True), and assign only permitted fields with the supplied loop pattern. Commit success; rollback and re-raise failure. In an independent session assert the committed note equals request.note and omitted quantity equals the original. Tests independently inspect stored fields on success and injected failure.',starter,solution,harness,ORM+'\norder_id='+repr(cc['order_id'])+'\n',[call('check_update',cc['partial_update'],False),call('check_update',{'note':'second changed note'},False),call('check_update',cc['partial_update'],True)],['sqlalchemy','pydantic'],orders)
c='auth.jwt_verification'
fixtures=files(c)['fixtures.py']
starter=files(c)['starter.py'].replace('from fixtures import key, allowed_algorithm, expected_issuer, expected_audience\n','')
solution=starter.replace('    raise NotImplementedError','    try:\n        return jwt.decode(token, key, algorithms=[allowed_algorithm], issuer=expected_issuer, audience=expected_audience, options={"require": ["exp", "iss", "aud"]})\n    except jwt.exceptions.InvalidTokenError:\n        raise HTTPException(status_code=401, detail="Invalid credential", headers={"WWW-Authenticate": "Bearer"})').replace('async def protected():','async def protected(claims: Annotated[dict, Depends(verify)]):')
harness=ded('''
def check_jwt(case):
    async def run():
        token=credential_cases()[case]
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app,raise_app_exceptions=False),base_url='http://test') as cl:
            r=await cl.get('/protected',headers={'Authorization':'Bearer '+token})
        return {'case':case,'status':r.status_code,'body':r.json(),'challenge':r.headers.get('www-authenticate')}
    return asyncio.run(run())
''')
exercise(c,'Verify the existing extracted token with jwt.decode using trusted key, algorithms=[allowed_algorithm], expected issuer/audience and options={"require": ["exp", "iss", "aud"]}. Catch only jwt.exceptions.InvalidTokenError and raise HTTPException(401, detail="Invalid credential", headers={"WWW-Authenticate": "Bearer"}). Attach Depends(verify) to /protected; return {"protected": True} only after verification. Run every supplied valid and invalid fixture, including time and required-claim cases. Never fall back to unverified claims.',starter,solution,harness,'import asyncio,httpx\n'+fixtures,[call('check_jwt',v) for v in contract(c)['cases']],['fastapi','httpx','pyjwt'])
c='cache.freshness_policy';cc=contract(c)
solution=files(c)['starter.py'].replace('await cache.set(key, notes)','await cache.set(key, notes, ex=seconds)').replace('    # TODO: invalidate after committed primary change','    await cache.delete(key)')
prefix=CACHE+'\nfreshness_contract='+repr(cc)+'\n'
harness=ded('''
def check_freshness(new_notes):
    async def run():
        cache=Cache();primary={'notes':freshness_contract['old_notes']};key=freshness_contract['cache_key']
        async def load(): return primary['notes']
        async def update(notes): primary['notes']=notes
        await cache.set(key,primary['notes'])
        no_expiry=await cache.ttl(key);await cache.delete(key)
        old=await read_notes(cache,key,load,tolerance_seconds)
        initial_ttl=await cache.ttl(key)
        assert 0<initial_ttl<=tolerance_seconds<=freshness_contract['tolerance_seconds']
        await change_notes(cache,key,update,new_notes)
        absent=await cache.ttl(key)
        assert absent==-2
        changed=await read_notes(cache,key,load,tolerance_seconds)
        final_ttl=await cache.ttl(key)
        assert 0<final_ttl<=tolerance_seconds
        return {'no_expiry':no_expiry,'absent_after_delete':absent,'old':old,'changed':changed,'initial_expiry_valid':0<initial_ttl<=tolerance_seconds,'final_expiry_valid':0<final_ttl<=tolerance_seconds,'primary':primary['notes']}
    return asyncio.run(run())
''')
exercise(c,'The '+str(cc['tolerance_seconds'])+'-second tolerance is supplied. Add ex=seconds to the cache population write, preserving a positive lifetime no greater than tolerance_seconds. After the supplied committed notes update, await cache.delete(key). The harness distinguishes old/new notes, -1 without expiry, -2 after deletion, positive TTL after both populations, and the next read of changed primary notes. Keep all helper code unchanged.',files(c)['starter.py'],solution,harness,prefix,[call('check_freshness',cc['new_notes']),call('check_freshness','another new note')],mounts=orders)
c='cache.safe_failure_policy'
# redis is not installed: supplied controlled API adapter, explicit simulation, not network Redis.
prefix=ded('''
import asyncio,math,json
class ConnectionError(Exception): pass
class TimeoutError(Exception): pass
class Redis:
    def __init__(self,*,socket_connect_timeout=None,socket_timeout=None):
        self.settings={'socket_connect_timeout':socket_connect_timeout,'socket_timeout':socket_timeout}
''')+CACHE.split('class Cache:',1)[1].join(['class Cache:',''])
# only class Cache and FailingCache, without registry redis import.
prefix=ded('''
import asyncio,time,math
class ConnectionError(Exception): pass
class TimeoutError(Exception): pass
class Redis:
    def __init__(self,*,socket_connect_timeout=None,socket_timeout=None):
        self.settings={'socket_connect_timeout':socket_connect_timeout,'socket_timeout':socket_timeout}
''')+'class Cache:'+CACHE.split('class Cache:',1)[1]
starter=files(c)['starter.py'].replace('from redis.asyncio import Redis\n','').replace('from redis.exceptions import ConnectionError, TimeoutError\n','')+'\nconfigured_cache = Redis()\n'
solution=ded('''
configured_cache = Redis(socket_connect_timeout=1, socket_timeout=1)
async def safe_read(cache, key, load_primary, seconds):
    try:
        value = await cache.get(key)
    except (ConnectionError, TimeoutError):
        value = None
    if value is not None:
        return value
    value = await load_primary()
    try:
        await cache.set(key, value, ex=seconds)
    except (ConnectionError, TimeoutError):
        pass
    return value
''')
harness=ded('''
def check_safe(operation,exception_name,value):
    async def run():
        settings=configured_cache.settings
        assert all(isinstance(v,(int,float)) and math.isfinite(v) and v>0 for v in settings.values())
        exception=ConnectionError if exception_name=='ConnectionError' else TimeoutError
        cache=FailingCache(operation,exception)
        async def load(): return value
        result=await safe_read(cache,'synthetic-key',load,30)
        assert result==value
        async def unavailable(): raise RuntimeError('synthetic primary failure')
        propagated=False
        try: await safe_read(Cache(),'synthetic-key',unavailable,30)
        except RuntimeError: propagated=True
        assert propagated
        return {'result':result,'timeouts':settings,'primary_failure_propagated':propagated,'operation':operation,'exception':exception_name}
    return asyncio.run(run())
''')
cc=contract(c)
exercise(c,'Configure configured_cache = Redis(socket_connect_timeout=1, socket_timeout=1). Complete safe_read with separate ConnectionError/TimeoutError boundaries around get and set(ex=seconds); load_primary stays outside those boundaries. Return a hit, or the primary value even if lookup/population fails. Do not retry or hide primary failures. Supplied controlled Redis API adapters model these operations without a network connection; tests inspect finite settings and both exception classes at each cache boundary.',starter,solution,harness,prefix,[call('check_safe',op,exc,cc['primary_value']) for op in cc['failure_operations'] for exc in ['ConnectionError','TimeoutError']])
# Supply the registered pinned pure-Python PyJWT modules as readonly runtime support.
# The sandbox resets its work directory after wheel extraction, so explicit files preserve imports.
with zipfile.ZipFile(Path('00_FINAL_PIPELINE_CORE/sandbox/node_modules/pyodide')/'PyJWT-2.10.1-py3-none-any.whl') as wheel:
    jwt_support=[{'path':n,'role':'readonly','language':'python','content':wheel.read(n).decode()} for n in wheel.namelist() if n.startswith('jwt/') and n.endswith('.py')]
exercises['auth.jwt_verification']['support']=jwt_support
# Keep unchanged scaffolding out of the syntax-judged learner region. It is executed,
# transparently displayed as a supplied string, in the same namespace as learner code.
def node_text(code,node):
    start=min([node.lineno]+[d.lineno for d in getattr(node,'decorator_list',[])])-1
    return '\n'.join(code.splitlines()[start:node.end_lineno])+'\n'
for cid,e in exercises.items():
    unchanged={node_text(e['starter'],n) for n in ast.parse(e['starter']).body}
    supplied=[];learner=[]
    for n in ast.parse(e['solution']).body:
        source=node_text(e['solution'],n)
        (supplied if source in unchanged else learner).append(source)
    kept_starter=[node_text(e['starter'],n) for n in ast.parse(e['starter']).body if node_text(e['starter'],n) not in set(supplied)]
    runtime_support=''
    if e.get('support'):
        runtime_support="from pathlib import Path\n_runtime_modules="+repr({f['path']:f['content'] for f in e['support']})+"\nfor _p,_c in _runtime_modules.items():\n    Path(_p).parent.mkdir(parents=True,exist_ok=True)\n    Path(_p).write_text(_c)\n"
    bootstrap=runtime_support+'\n'.join(supplied)
    shared='# Unchanged supplied runtime/scaffold source; edit only the learner region below.\n_SUPPLIED_SCAFFOLD = '+repr(bootstrap)+'\nexec(_SUPPLIED_SCAFFOLD, globals())\n'
    e['solution']=shared+'# BEGIN LEARNER EDITS\n'+'\n'.join(learner)+'# END LEARNER EDITS\n'
    e['starter']=shared+'# BEGIN LEARNER EDITS\n'+'\n'.join(kept_starter)+'# END LEARNER EDITS\n'
    e.pop('support',None)
# Choice specifications:
# the correct option is a single boundary decision, not an unqualified assertion.
choices={}
def choice(cap,q,right,wrongs):choices[cap]=(q,right,wrongs)
choice('select_entities_with_a_condition_and_explicit_row_bound','A request needs at most three Orders matching a condition. Which retrieval shape expresses both requirements?', 'Await session.scalars(select(Order).where(condition).limit(3)) and inspect the returned entities.', [('Select all Orders and assume the caller will not see more than three.','The condition and explicit row bound belong in the selection, not an assumption about callers.'),('Use session.get(Order, condition) to retrieve several matching Orders.','get represents a primary-key identity lookup, not a conditional multi-row selection.')])
choice('distinguish_matching_entities_from_absence','A primary-key get returns None and a conditional selection returns no entities. What do these outcomes mean?', 'Both represent absence in their respective retrieval forms and need explicit handling before entity use.', [('Both prove the intended Order exists because the lookup executed.','Successful execution does not guarantee a matching row.'),('Only None is absence; an empty selection is an existing Order.','An empty selection has no matching entities to use.')])
choice('determine_commit_and_rollback_effects','Two related writes must succeed or fail together. The second raises an exception that escapes their shared session.begin() scope. What is the transaction outcome?', 'The uncommitted pair is rolled back; successful exit would commit both.', [('The first write remains durable just because its helper returned.','A helper returning is not a commit; the related writes share the transaction.'),('The exception makes both writes durable automatically.','Exceptional scope exit rolls back rather than committing the pair.')])
choice('determine_whether_authorization_headers_pass_the_extraction_gate','With HTTPBearer default auto_error=True, which presented header can pass the extraction gate (without proving validity)?', 'Authorization: Bearer synthetic-token', [('No Authorization header.','Absent credentials are rejected rather than supplied to the handler.'),('Authorization: Basic synthetic','A non-bearer scheme is rejected by this extraction gate.'),('Authorization: Bearer','Bearer without credential text is malformed and rejected.')])
choice('distinguish_results_in_cache_keys','An order read supports both notes and quantity representations. What belongs in its cache key?', 'Both the order identity and the representation parameter.', [('Only the order identity.','Different representations are different results and must not reuse the wrong cached value.'),('Only the representation parameter.','Different order identities must not share one represented result.')])
choice('distinguish_schema_reversal_from_deleted_data_recovery','A candidate migration drops a populated column; its downgrade recreates the column. What can the reviewer conclude?', 'Recreating the schema does not restore the deleted column data; review and test the proposed reversal before approval.', [('The downgrade necessarily restores every deleted value.','Dropping the column deletes its data; recreation is not data recovery.'),('Autogeneration makes both directions safe without manual review.','Candidate changes require manual review, including possible unintended drop-and-add renames.')])
choice('choose_indexes_by_query_workload','A service performs frequent equality lookups on external_reference and also writes Orders. What is the defensible index decision?', 'Consider an index for that workload while accounting for storage and write-maintenance overhead.', [('Index every column automatically.','Workload, not the mere existence of a column, justifies an index.'),('An index has no cost during writes.','Index maintenance adds overhead during writes.')])
choice('identify_b_tree_index_candidates','Which supplied query pattern is a B-tree index candidate?', 'Frequent equality or ordered comparisons on a filtered or ordered column.', [('A column merely exists but is never used by the stated lookup workload.','The workload must justify the candidate, not the column\'s existence.'),('Every column is always a candidate with guaranteed improvement.','Indexes add overhead and do not guarantee a gain for every column.')])
choice('detect_storage_fields_leaking_into_public_contracts','A stored Order includes processing, but the declared public output is id, note and quantity. What preserves the public boundary?', 'Declare those output fields in a separate PublicOutput and use it as response_model.', [('Use the persistence model as the public contract so processing appears automatically.','Persistence-only fields should not automatically become API fields.'),('Enable from_attributes=True and omit a public output field declaration.','Attribute validation concerns how values are read, not which fields clients receive.')])
choice('distinguish_transaction_recovery_from_api_translation','A recognized storage conflict leaves the session failed. Which sequence separates recovery from the public outcome?', 'Rollback the failed transaction, then translate the recognized failure at the API boundary.', [('Return a public conflict response and keep using the failed session without rollback.','API translation does not recover failed transactional state.'),('Rollback and include private database exception text in the response.','Recovery does not justify disclosing persistence internals.')])
choice('avoid_disclosing_persistence_failure_details','The API declares HTTP 409 for a recognized uniqueness conflict. What should its public response contain?', 'The declared 409 outcome and a fixed intentional public message.', [('HTTP 409 plus raw database diagnostic text.','The declared conflict outcome replaces, rather than exposes, internal exception text.'),('A successful outcome merely because the exception was recognized.','Recognition enables translation into the declared conflict outcome, not success.')])
choice('preserve_error_status_and_relevant_headers','A recognized HTTP exception has status 401 and a relevant WWW-Authenticate header. What should a shared error envelope preserve?', 'The original status and relevant header while using the chosen public body structure.', [('Status 200 because all envelope bodies have the same shape.','A common body structure must not change the underlying HTTP outcome.'),('Status 401 but discard all exception headers.','Relevant headers are part of the HTTP outcome to preserve.')])
choice('determine_forwarded_metadata_trust_from_sender_and_configuration','Forwarded headers claim HTTPS, but the sender is not in the configured trusted proxy sources. What controls trust?', 'Trust depends on the sender and configured allowed proxy sources, not the header claim alone.', [('The HTTPS header claim alone establishes trust.','Only configured proxy sources should supply trusted forwarded metadata.'),('Trust every sender because one legitimate proxy exists.','An allowed proxy does not authorize unrelated senders.')])
choice('evaluate_network_restrictions_before_allowing_wildcard_trust','Backend network access is not restricted to trusted proxies. Is --forwarded-allow-ips * appropriate?', 'No; explicitly allow known proxy sources rather than trusting all senders.', [('Yes, wildcard trust only names the one intended proxy.','Wildcard trust accepts all senders, not a single known source.'),('Yes, an external HTTPS URL makes network restrictions irrelevant.','Wildcard trust is appropriate only with access restricted to trusted proxies.')])
choice('distinguish_validated_delivery_acceptance_from_completed_business_work','A webhook contract allows deferred processing and acknowledges a validated delivery with 202. What does that acknowledgement establish?', 'The delivery was accepted under the contract, not that all downstream work has completed.', [('All downstream business work has already completed.','Delivery acceptance and completed business work are distinct.'),('Validation can be skipped because work is deferred.','The incoming body must meet the contract before downstream work is accepted.')])
choice('identify_broken_cross_service_correlation','An order request logs interaction chain-a locally but sends chain-b to the outbound receiver. What is broken?', 'The local and outbound records do not retain the same request-chain context.', [('Nothing: timestamps alone replace the identifier chain.','The identifier connects request-chain records instead of reconstructing them from timestamps alone.'),('chain-b proves the caller has greater authority.','Interaction identifiers provide correlation context, not authority.')])
choice('select_bounded_nonsensitive_signal_labels','Which grouping keeps compared service signals bounded and nonsensitive?', 'HTTP method, route template and outcome over the same time window.', [('Raw caller identifiers and raw request URLs.','Use bounded categories, not caller or request identifiers.'),('Request identifiers as the main comparison labels.','Request identifiers are not the bounded grouping for service-signal comparisons.')])
choice('derive_and_bound_listing_inputs','A one-based page contract bounds page and page_size. How should offset be obtained?', 'Validate both inputs against their declared bounds and compute (page - 1) * page_size.', [('Use page * page_size so page one skips a full page.','A one-based first page must begin at offset zero.'),('Leave page_size unbounded because LIMIT is present.','LIMIT must use an explicitly constrained input; the keyword alone does not bound caller demand.')])
choice('identify_unsafe_value_interpolation','A supplied value contains a quote and SQL-looking text. Which handling keeps it separate from fixed query structure?', 'Use a named placeholder in sqlalchemy.text and supply a separate execution parameter dictionary.', [('Build the SQL with an f-string containing the supplied value.','Interpolation places caller data into SQL structure.'),('Concatenate the supplied value into the WHERE clause after wrapping it in quotes.','Quoting with concatenation still mixes caller data with the SQL structure.')])
choice('verify_committed_identity_and_fields_in_independent_session','After constructing and flushing a new entity, what verifies durable creation?', 'Commit and retrieve it by generated identity in an independent session, checking the stored fields.', [('Check only that a Python entity object was constructed.','Object construction does not verify committed storage.'),('Flush and assume it is durable without commitment.','Flush obtains database-generated identity; successful creation must be committed and independently checked.')])
choice('complete_durable_deletion_with_failure_rollback','A deletion flush fails before a successful commit. What should the deletion path do?', 'Rollback and propagate failure rather than report durable deletion.', [('Report successful removal because delete was called.','Marking for removal is not durable commitment, especially after failure.'),('Continue using the failed session without rollback.','A failed transaction must be recovered before session reuse.')])
choice('verify_changed_and_preserved_fields_in_independent_session','A note-only partial update omits quantity. What should an independent post-commit check verify?', 'The stored note changed and the omitted quantity retains its original value.', [('Only the request model contains the new note.','The request model does not verify committed entity fields.'),('Quantity becomes the request model\'s default because it was omitted.','exclude_unset=True preserves omitted fields rather than overwriting them with defaults.')])
choice('identify_expiration_and_not_before_failures','A verified-signature token is expired, or its not-before time is still in the future. What should happen?', 'Reject the credential for failing its time-validity constraint.', [('Accept it because signature verification cancels time checks.','Signature and time validity are distinct constraints.'),('Use decoded claims without verification as a fallback.','Readable claims do not establish trust and verification failures must be rejected.')])
choice('distinguish_required_claim_presence_from_claim_value_checks','Why configure options={"require": ["exp", "iss", "aud"]} as well as the trusted issuer and audience?', 'Required presence and valid claim values are distinct checks.', [('Matching issuer/audience configuration makes every required claim automatically present.','Claim-value expectations are not the same as requiring claim presence.'),('Claim presence alone proves the signature and every value valid.','Presence is only one constraint; trusted verification must still check signature and configured values.')])
choice('interpret_ttl_and_verify_freshness_after_invalidation','After a committed notes change, the cache key is deleted and ttl(key) reports -2. What is the expected next cache-aside read?', 'Load the changed primary notes and repopulate with expiry; -2 means the key is absent.', [('Serve the old cached notes because -2 means no expiry.','-1 means an existing key without expiry; -2 means absence.'),('Return the old notes from the cache because deleting the key changes primary truth.','Invalidation removes a cached copy; the next miss loads changed primary data.')])
choice('determine_whether_cache_failure_changes_authoritative_outcomes','The cache is acceleration-only and primary data is available. A Redis population write fails after a miss. What outcome follows the declared policy?', 'Return the available primary-store value while handling the cache connection/timeout failure at the cache boundary.', [('Discard the available primary value because the cache write failed.','An incidental acceleration-layer failure should not discard the authoritative value under this policy.'),('Mask all primary-store errors inside the same Redis exception handler.','Exception handling belongs at the cache operations, not around unrelated primary failures.')])
choice('distinguish_value_binding_from_structural_selection','A caller requests a column name or sort direction. How should the application handle this structural choice?', 'Map it through a defined allowlist; parameters bind data values, not arbitrary SQL structure.', [('Bind the arbitrary column name as a data parameter and assume it selects that column.','Data-value parameters do not stand for arbitrary column names or sort direction.'),('Insert any requested column or sort direction directly into SQL.','A structural request needs a defined allowlist, not unrestricted caller-selected SQL structure.')])
# Bind checks to their exact planned anchor. Reject a missing author specification.
result={k:P[k] for k in ['schema_version','path_id','batch_id']};result.update(kind='interactions_part',tiles=[])
for tile in P['tiles']:
    items=[];seen=set();stretch=False;screen=next(t for t in S['tiles'] if t['tile_id']==tile['tile_id'])
    interactive=[s for s in tile['steps'] if s['type'] in ('check','hands_on')]
    for index,step in enumerate(interactive):
        cid=step['concept_ids'][0];g=gloss[cid]
        measured=[]
        for anchor in step['anchors']:
            if '#assessment:' in anchor:
                ac=anchor.split('#assessment:',1)[1]
                aa=next(a for a in g['assessment_anchors'] if a['capability']==ac)
                measured.append({'concept_id':cid,'capability':ac,'fact_ids':aa['fact_ids'][:]})
        fact_text=' '.join(f['statement'] for f in g['coverage']['required_facts'] if f['id'] in {f for m in measured for f in m['fact_ids']})
        feedback={'correct':{'message':'You preserved the intended boundary. '+fact_text},'incorrect':{'message':'Review the relevant boundary and compare each required outcome. '+fact_text},'hints':['Identify the intended input, outcome and boundary before choosing or editing.','Check the missing, malformed or failed case as well as success.']}
        if cid not in seen:
            rem=next((s for s in screen.get('remediation_steps',[]) if cid in s['concept_ids']),None)
            if rem: feedback['remediation_step_id']=rem['step_id']
        seen.add(cid)
        stretch = stretch or step['type']=='hands_on'
        ix={'type':step['planned_interaction_type'],'interaction_id':'ix.'+step['step_id'],'difficulty':'stretch' if stretch else ('intro' if index==0 else 'core'),'grading_mode':'client','standalone':False,'measures':measured,'anchors':step['anchors'][:],'feedback':feedback}
        if ix['type']=='choice':
            cap=measured[0]['capability']
            # A few planner capability names are more specific than the conceptual question label.
            aliases={'choose_constrained_pagination_inputs_and_derived_offset':'derive_and_bound_listing_inputs','derive_pagination_offset_from_one_based_contract':'derive_and_bound_listing_inputs','identify_unsafe_sql_value_interpolation':'identify_unsafe_value_interpolation'}
            key=aliases.get(cap,cap)
            if key not in choices:
                print('MISSING CHOICE',cap);raise KeyError(cap)
            q,right,wrong=choices[key]
            options=[{'option_id':'o1','text':right}]+[{'option_id':'o'+str(i+2),'text':text} for i,(text,why) in enumerate(wrong)]
            ix['public']={'prompt':q,'options':options,'selection':'single','shuffle':True}
            ix['grading']={'correct_option_ids':[options[0]['option_id']],'option_feedback':{options[i+1]['option_id']:{'message':why} for i,(text,why) in enumerate(wrong)}}
            ix['standalone']=True
        elif ix['type']=='code_exercise':
            e=exercises[cid]
            tests=[]
            for i,t in enumerate(e['cases']):
                tests.append({'test_id':step['step_id']+'.t'+str(i+1),**t,'visible':True,'message_on_fail':'The supplied case does not meet the stated boundary. '+g['practice_anchor']['success']})
            ix['public']={'prompt':e['prompt']+' Edit only BEGIN LEARNER EDITS; the rest is supplied scaffolding.','runtime':{'kind':'python_asgi','version':sandbox.RUNTIMES['python_asgi']['version'],'packages':e['packages']},'workspace':{'entry':'exercise.py','files':[{'path':'exercise.py','role':'editable','language':'python','content':e['starter']}]+e.get('support',[]),'asset_mounts':e['mounts']},'constraints':{k:g['practice_anchor']['live_code'][k][:] for k in ('allowed_syntax','blocked_syntax')}}
            ix['grading']={'solution_files':[{'path':'exercise.py','content':e['solution']}],'tests':tests}
        elif ix['type']=='classify':
            ds=assets['ds.service_signals'];cols=[c['name'] for c in ds['columns']];rows=[dict(zip(cols,row)) for row in ds['rows']]
            baseline=next(r for r in rows if r['window']=='baseline' and r['outcome']=='success')
            bucket_names={'traffic':'Traffic growth; unchanged failure fraction and latency','failure':'Increased failure fraction; no traffic or latency increase','latency':'Worsened latency; unchanged traffic and failure fraction','none':'No regression in the compared signals'}
            classify_items=[];assignments={};item_feedback={}
            for n,r in enumerate(r for r in rows if r['window']!='baseline' and r['outcome']=='success'):
                # Derive the interpretation from numeric signals, never from a case's name.
                if r['failure_fraction']>baseline['failure_fraction']: bucket='failure';source_col='failure_fraction'
                elif r['latency_p95_seconds']>baseline['latency_p95_seconds']:bucket='latency';source_col='latency_p95_seconds'
                elif r['request_rate']>baseline['request_rate']:bucket='traffic';source_col='request_rate'
                else:bucket='none';source_col='request_rate'
                label='item'+str(n+1)
                fmt=lambda v:format(v,'.6g')
                frow=next(v for v in rows if v['window']==r['window'] and v['outcome']=='failure')
                text=f"Comparison {chr(65+n)}: {r['window_seconds']} seconds, {r['method']} {r['route_template']}; {r['request_count']} requests, {r['failure_count']} failures; success/failure partitions {r['partition_count']}/{frow['partition_count']}; request rate {fmt(r['request_rate'])}/s, failure rate {fmt(r['failure_rate'])}/s; failure fraction {fmt(r['failure_fraction']*100)}%; p95 latency {fmt(r['latency_p95_seconds'])} seconds."
                classify_items.append({'item_id':label,'text':text,'source':{'asset_id':ds['asset_id'],'row':{'where':{'window':r['window'],'method':r['method'],'route_template':r['route_template'],'outcome':r['outcome']},'occurrence':0},'column':source_col}})
                assignments[label]=bucket;item_feedback[label]={'message':bucket_names[bucket]+'. Compare rates, their ratio and p95 separately in the same window/group; do not sum repeated group totals across outcome rows.'}
            fmt=lambda v:format(v,'.6g')
            prompt=f"Match each comparison to baseline in the same {baseline['window_seconds']}-second {baseline['method']} {baseline['route_template']} group: {baseline['request_count']} requests, {baseline['failure_count']} failures, success/failure partitions {baseline['request_count']-baseline['failure_count']}/{baseline['failure_count']}, request rate {fmt(baseline['request_rate'])}/s, failure rate {fmt(baseline['failure_rate'])}/s, failure fraction {fmt(baseline['failure_fraction']*100)}%, p95 {fmt(baseline['latency_p95_seconds'])} seconds. Treat partitions as outcomes of the same group, not different caller identifiers. Decide separately whether traffic, failure fraction or latency increased; a larger failure count alone is not a larger fraction."
            ix['public']={'prompt':prompt,'buckets':[{'bucket_id':k,'label':v} for k,v in bucket_names.items()],'items':classify_items}
            ix['grading']={'assignments':assignments,'role_map':{k:'numerical' for k in bucket_names},'item_feedback':item_feedback}
            ix['standalone']=True
        items.append({'step_id':step['step_id'],'interaction':ix})
    result['tiles'].append({'tile_id':tile['tile_id'],'interactions':items})
# Same endpoint, different request inputs: preserves observable cases and anti-constant checks.
for tile in result['tiles']:
    for item in tile['interactions']:
        ix=item['interaction']
        if ix['type']!='code_exercise': continue
        e=exercises[ix['measures'][0]['concept_id']]
        tests=ix['grading']['tests']
        added=[]
        for t in tests:
            if t['kind']!='http_equals': continue
            rq=t['spec']['requests'][-1]
            if rq['path']=='/__exercise_check': continue
            key=sandbox._call_key(t)[0]
            if sum(sandbox._call_key(v)[0]==key for v in tests if v['kind']=='http_equals')<2:
                import copy
                extra=copy.deepcopy(t);extra['test_id']=t['test_id']+'.repeat'
                extra['spec']['requests'][-1]['params']={'comparison':'second'}
                added.append(extra)
        tests.extend(added)
# Run reference solutions
# in the pinned engine to derive every expected. No typed outputs.
cache_path=B/'working/reference_results.json'
cache=json.loads(cache_path.read_text()) if cache_path.exists() else {}
for tile in result['tiles']:
    for item in tile['interactions']:
        ix=item['interaction']
        if ix['type']!='code_exercise':continue
        cid=ix['measures'][0]['concept_id'];e=exercises[cid]
        key=sandbox.sha(e['solution']+json.dumps(ix['grading']['tests'],sort_keys=True))
        if key in cache: values=cache[key]
        else:
            problems=[];tables,_=sandbox._tables(R,e['mounts'],{},problems);assert not problems,problems
            probes=[sandbox._py_probe(t) for t in ix['grading']['tests']]
            script=sandbox._py_script('reference','exercise.py',e['solution'],sandbox._py_mounts(tables),probes)
            script['files'] += [{'path':f['path'],'content':f['content']} for f in e.get('support',[])]
            job=sandbox._py_job('python_asgi',e['packages'],[script])
            print('RUN REFERENCE',cid,flush=True)
            run=sandbox.node_run(job,sandbox.RUNTIMES['python_asgi']['runner'])['results']['reference']
            if not run['ok']:raise RuntimeError(cid+' '+run.get('error',''))
            values={}
            for test in ix['grading']['tests']:
                p=run['probes'][test['test_id']]
                if not p['ok']:raise RuntimeError(cid+' '+test['test_id']+' '+p.get('error',''))
                value=p['value']
                if test['kind']=='http_equals' and test['spec']['requests'][-1]['path']=='/__exercise_check' and value['status']!=200: raise RuntimeError(cid+' harness failed '+str(value))
                if test['kind']=='http_equals':
                    # Only contract outcome keys, and relevant response headers, not incidental generated headers.
                    value={k:value[k] for k in ['status','json']}
                    raw=p['value']['headers']
                    if 'www-authenticate' in raw:value['headers']={'www-authenticate':raw['www-authenticate']}
                values[test['test_id']]=value
            cache[key]=values;cache_path.write_text(json.dumps(cache,indent=2)+'\n')
        for test in ix['grading']['tests']:test['spec']['expected']=values[test['test_id']]
(B/'interactions.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print('WROTE',sum(len(t['interactions']) for t in result['tiles']),'interactions')
