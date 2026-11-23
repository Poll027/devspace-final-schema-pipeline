import json, csv, io, re, ast
from pathlib import Path
B = Path('batches/final_batch_persistence')
g = json.loads((B/'inputs/path_glossary_bundle.json').read_text())
bs = g['bundles']
sid = 'scenario.order_service'
# Mine literal example vocabulary before constructing the fictional fixtures.
vocab = []
for b in bs:
    texts = [t['content'] for t in b['teaching_blocks']]
    texts += [json.dumps(b.get(k, {}), ensure_ascii=False) for k in ('visual_anchor','practice_anchor','assessment_anchors')]
    for text in texts:
        for term in re.findall(r'[A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_][A-Za-z_0-9]*)*|/api|\b\d+\b', text):
            if term not in vocab:
                vocab.append(term)
# Keep technical tokens and concrete example nouns, not the surrounding prose.
concrete = {'order','orders','Order','Entity','identity','order_id','note','notes','quantity','external_reference','field','processing','Bearer','Authorization','Redis','PostgreSQL','B-tree','FastAPI','Starlette','Alembic','SQLAlchemy','Pydantic','JWT','HTTPException','HTTPAuthorizationCredentials','HTTPBearer','Annotated','Depends','BaseModel','ConfigDict','PublicInput','PublicOutput','FailureClass','JSONResponse','Content-Type','application','json','GET','method','route','outcome','window','request_counter','target_metadata','upgrade','downgrade','root_path','header_name','url','interaction_id','representation','key','token','allowed_algorithm','expected_issuer','expected_audience','exp','iss','aud','nbf','value','supplied_value','predicate','primary_sort_column','unique_key','page','page_size','offset','seconds','socket_connect_timeout','socket_timeout','TTL','HTTPS','/api'}
vocab = [v for v in vocab if v in concrete or v.isdigit() or '.' in v or '_' in v]
# Explicit literal phrases also occur in the glossary; retain the negative TTL sentinels.
all_text = '\n'.join(t['content'] for b in bs for t in b['teaching_blocks']) + '\n' + '\n'.join(json.dumps(b['practice_anchor']) for b in bs)
for term in ['external reference','storage-only processing field','application/json','Authorization: Bearer','--forwarded-allow-ips','-1','-2','100 requests','5 failures','200 requests','10 failures','5 percent']:
    if term in all_text and term not in vocab:
        vocab.append(term)
r = {'schema_version':'1.0','kind':'scenario_asset_registry','path_id':g['path_id'],'batch_id':B.name,'scenarios':[{'scenario_id':sid,'name':'Fictional order service','summary':'A fictional small order service retrieves and changes authored orders, exposes bounded public API contracts, and uses a disposable Redis copy for reads. All rows, credentials, operational observations and integration contracts are synthetic teaching fixtures, not production facts.','domain':'order API persistence and service boundaries','glossary_example_vocab':vocab}], 'assets':[]}
def col(name, typ, role, description, label=False):
    c = {'name':name,'type':typ,'semantic_role':role,'description':description}
    if label: c['numeric_looking_label'] = True
    return c
def dataset(aid,title,columns,rows,description):
    a = {'asset_id':aid,'asset_kind':'dataset','scenario_id':sid,'title':title,'description':description,'columns':columns,'rows':rows,'provenance':'authored','variants':[]}
    r['assets'].append(a)
    return a
orders = dataset('ds.orders','Synthetic persisted orders',[
 col('id','integer','identifier','Unique generated primary-key identity; a label, not a measured quantity.',True),
 col('external_reference','string','identifier','External reference used by the frequent equality-lookup workload.'),
 col('note','string','text','Editable ORM note; partial updates supply this field and omit quantity.'),
 col('quantity','integer','numerical','Authored item count; also the repeated primary sort value for pagination.'),
 col('processing','string','categorical','Storage-only processing state; excluded from the public schemas.')],
 [[42,'ref-42','old note 42',2,'queued'],[43,'ref-43','old note 43',2,'queued'],[101,'ref-101','target note',3,'queued'],[102,'ref-102','other note',3,'queued'],[103,'ref-103','third note',3,'queued'],[104,'ref-104','fourth note',4,'queued'],[105,'ref-105','fifth note',4,'queued'],[106,'ref-106','excluded note',1,'held']],
 'SQL table orders / orders.csv. Order and the creation exercise Entity alias map here. Filter processing == queued; primary sort quantity; unique tie-breaker id. Seven matching rows support adjacent three-row pages and a trailing page; held is a nonmatch. Cache representations expose note as notes, not a second persistent column. Public input: note and quantity; public output: id, note and quantity. All names not fixed by the glossary are explicitly fictional fixture choices.')
orders['variants'] = [
 {'variant_id':'orders.absent_target','derived_from':'base','purpose':'Valid missing-target lookup; absence is not a data defect.','ops':[{'op':'drop_rows','where':{'id':101}}],'planted_issues':[]},
 {'variant_id':'orders.empty_filter','derived_from':'base','purpose':'No matches for the supplied queued predicate.','ops':[{'op':'drop_rows','where':{'processing':'queued'}}],'planted_issues':[]},
 {'variant_id':'orders.changed_note','derived_from':'base','purpose':'Known committed change for cache invalidation and selective-update verification.','ops':[{'op':'set_cell','where':{'id':42},'occurrence':0,'column':'note','value':'new note 42'}],'planted_issues':[]}]
entity = dataset('ds.entity','Values for the fixed textual lookup',[
 col('field','string','text','Caller-supplied exact-match data; punctuation is data, never executable SQL.')],
 [['ordinary'],["quote' value"],["x' OR 1=1 --"],['another value']],
 'SQL table Entity / Entity.csv, used only by the glossary textual SELECT field FROM Entity WHERE field = :value. Not the mapped Order alias used in the creation exercise.')
# Equal-duration synthetic dashboard windows and histogram-derived quantiles. Rates/quantiles are computed, never typed.
bucket_bounds = [0.1,0.2,0.5,1.0,2.0,5.0]
def hist_quantile(q, observations):
    counts = [sum(x <= bound for x in observations) for bound in bucket_bounds]
    target = q*len(observations)
    previous_n, previous_bound = 0,0.0
    for bound, n in zip(bucket_bounds, counts):
        if n >= target:
            return previous_bound+(bound-previous_bound)*(target-previous_n)/(n-previous_n)
        previous_n,previous_bound = n,bound
    raise ValueError('histogram has no finite enclosing bucket')
signal_cols = [col('window','string','categorical','Bounded equal-duration dashboard case label.'),col('window_seconds','integer','numerical','Duration shared by every comparison.'),col('method','string','categorical','Bounded HTTP method.'),col('route_template','string','categorical','Bounded route template, never a raw caller URL.'),col('outcome','string','categorical','Bounded success/failure partition.'),col('request_count','integer','numerical','All requests in the method/route group.'),col('failure_count','integer','numerical','All failures in that same group.'),col('partition_count','integer','numerical','Events in this outcome partition.'),col('request_rate','number','numerical','Group requests per second.'),col('failure_rate','number','numerical','Group failures per second.'),col('failure_fraction','number','numerical','Failure rate divided by request rate.'),col('latency_p95_seconds','number','numerical','Grouped histogram-derived 0.95 quantile, computed from the supplied synthetic duration observations.')]
signal_rows=[]; signal_fixtures=[]
for window,total,fail,delay in [('baseline',100,5,False),('traffic_growth',200,10,False),('increased_failure',100,20,False),('delayed',100,5,True),('no_regression',100,5,False)]:
    durations = ([0.1]*80+[0.2]*15+[0.4]*5) if not delay else ([0.5]*80+[1.0]*15+[1.5]*5)
    durations = durations*(total//100)
    seconds=60
    for outcome,count in [('success',total-fail),('failure',fail)]:
        signal_rows.append([window,seconds,'GET','/orders/{order_id}',outcome,total,fail,count,total/seconds,fail/seconds,fail/total,hist_quantile(.95,durations)])
    signal_fixtures.append({'window':window,'durations_seconds':durations,'bucket_bounds_seconds':bucket_bounds,'cumulative_bucket_counts':[sum(x<=z for x in durations) for z in bucket_bounds]})
signals=dataset('ds.service_signals','Equal-window synthetic service dashboard',signal_cols,signal_rows,'Authored successful, failing and delayed samples. Each window has two outcome rows; group totals, rates and latency are repeated for display, not summed across outcomes. Only partition_count is additive. Exact glossary baseline 100/5 and comparison 200/10 retain an unchanged 5 percent failure fraction. Latency values are computed using bucket interpolation over synthetic duration observations, not measured production telemetry.')
def csv_text(a):
    out=io.StringIO();w=csv.writer(out,lineterminator='\n');w.writerow([c['name'] for c in a['columns']]);w.writerows(a['rows']);return out.getvalue()
# These are runnable dependency scaffolds, not learner solutions. External runtime dependencies are declared explicitly.
orm_support = '''import csv
from pathlib import Path
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

class Base(DeclarativeBase):
    pass

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    external_reference: Mapped[str] = mapped_column(String, unique=True)
    note: Mapped[str] = mapped_column(String)
    quantity: Mapped[int] = mapped_column(Integer)
    processing: Mapped[str] = mapped_column(String)

Entity = Order
async def make_store(csv_name="orders.csv"):
    # Local synthetic database only. Independent sessions share this engine.
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    with open(Path(__file__).with_name(csv_name), newline="") as handle:
        rows = list(csv.DictReader(handle))
    async with factory() as session:
        session.add_all([Order(id=int(r["id"]), external_reference=r["external_reference"],
            note=r["note"], quantity=int(r["quantity"]), processing=r["processing"]) for r in rows])
        await session.commit()
    return engine, factory
'''
cache_support = '''import csv
import time
from pathlib import Path
from redis.exceptions import ConnectionError, TimeoutError

class PrimaryStore:
    def __init__(self):
        with open(Path(__file__).with_name("orders.csv"), newline="") as handle:
            self.rows = {int(r["id"]): r for r in csv.DictReader(handle)}
        self.calls = []
    async def load(self, order_id, representation):
        self.calls.append((order_id, representation))
        r = self.rows[order_id]
        if representation == "notes":
            return {"order_id":order_id, "notes":r["note"]}
        return {"order_id":order_id, "quantity":int(r["quantity"])}
    async def committed_notes_update(self, order_id, notes):
        self.rows[order_id]["note"] = notes

class Cache:
    # Endpoint-ready adapter for cache-aside; not raw Redis serialization.
    def __init__(self):
        self.entries = {}; self.expiry = {}; self.calls = []
    async def get(self, key):
        self.calls.append(("get", key))
        if key in self.expiry and self.expiry[key] <= time.monotonic():
            self.entries.pop(key, None); self.expiry.pop(key, None)
        return self.entries.get(key)
    async def set(self, key, value, ex=None):
        self.calls.append(("set", key, ex)); self.entries[key] = value
        if ex is None: self.expiry.pop(key, None)
        else: self.expiry[key] = time.monotonic()+ex
    async def delete(self, key):
        self.calls.append(("delete", key)); self.entries.pop(key, None); self.expiry.pop(key, None)
    async def ttl(self, key):
        if await self.get(key) is None: return -2
        if key not in self.expiry: return -1
        return max(0, int(self.expiry[key]-time.monotonic()))

class FailingCache(Cache):
    def __init__(self, operation, exception):
        super().__init__(); self.operation=operation; self.exception=exception
    async def get(self, key):
        if self.operation == "get": raise self.exception("synthetic cache lookup failure")
        return None
    async def set(self, key, value, ex=None):
        if self.operation == "set": raise self.exception("synthetic cache population failure")
        return await super().set(key,value,ex)
'''
starters = {}
starters['sqlalchemy.retrieve_resource'] = '''from support import Order
async def retrieve(session, identity):
    # TODO: awaited primary-key lookup and explicit absence branch.
    raise NotImplementedError
'''
starters['sqlalchemy.transaction_boundaries'] = '''class WriteFailure(Exception):
    pass
async def first_write(session):
    await session.record("first")
async def second_write(session):
    await session.record("second")
    if session.fail_second: raise WriteFailure("synthetic second-write failure")
async def related_writes(session):
    # TODO: wrap the two supplied calls in a shared transaction scope.
    await first_write(session)
    await second_write(session)
async def recover_failed_flush(session):
    try:
        await session.flush()
    except WriteFailure:
        # TODO: rollback before the supplied reuse check.
        pass
    await session.reuse()
'''
starters['auth.bearer_dependency'] = '''from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
app = FastAPI()
@app.get("/credential")
async def credential():
    # TODO: declare the bearer dependency and return scheme and credentials.
    raise NotImplementedError
'''
starters['cache.redis_cache_aside'] = '''async def read_order(order_id, representation, cache, primary_store):
    # TODO: identity-and-representation key, hit return, miss load/populate/return.
    raise NotImplementedError
'''
starters['database.alembic_migrations'] = '''def upgrade():
    # Candidate: drop an existing column and add a replacement column.
    # TODO: add review comments; this review-only file performs no schema changes.
    pass

def downgrade():
    # Candidate inverse: drop the replacement and recreate the original column.
    # TODO: record data-loss risk, intent clarification, correction and verification.
    pass
'''
starters['database.service_query_indexes'] = '''-- Synthetic PostgreSQL workload: frequent equality lookups on orders.external_reference,
-- with ongoing order writes. Candidate only; no performance gain is promised.
-- TODO: declare one B-tree index on the supplied table and column.
-- TODO: annotate the storage and write-maintenance trade-off.
'''
starters['design.api_persistence_model_boundaries'] = '''from types import SimpleNamespace
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict
order = SimpleNamespace(id=42, note="old note 42", quantity=2, processing="queued")
# Fixture contract: input note/quantity; output id/note/quantity; processing is storage-only.
class PublicInput(BaseModel):
    pass  # TODO: public input fields
class PublicOutput(BaseModel):
    pass  # TODO: public output fields and attribute-validation configuration
app = FastAPI()
@app.get("/orders/42")  # TODO: select PublicOutput as response_model
async def read_order():
    return order
'''
starters['fastapi.domain_error_translation'] = '''from fastapi import FastAPI
from fastapi.responses import JSONResponse
class FailureClass(Exception):
    pass
class FailedSession:
    def __init__(self): self.failed=True; self.rollback_calls=0
    async def rollback(self): self.failed=False; self.rollback_calls+=1
    async def reuse(self):
        assert not self.failed, "session has not recovered"
app=FastAPI()
async def recover(session):
    # TODO: restore the failed persistence boundary.
    raise NotImplementedError
# TODO: register the handler for FailureClass; declared public outcome is 409.
async def handle_failure(request, exception):
    raise NotImplementedError
@app.get("/conflict")
async def conflict():
    raise FailureClass("synthetic private uniqueness diagnostic")
'''
starters['fastapi.public_error_envelopes'] = '''from fastapi import FastAPI, HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
app=FastAPI()
# TODO: register for StarletteHTTPException; preserve status and relevant headers.
async def public_error(request, exception):
    # Contract: body contains only {"reason": public_reason}.
    raise NotImplementedError
@app.get("/fastapi-error")
async def fastapi_error():
    raise HTTPException(status_code=401, detail="credential required", headers={"WWW-Authenticate":"Bearer"})
@app.get("/starlette-error")
async def starlette_error():
    raise StarletteHTTPException(status_code=404, detail="not found")
'''
starters['fastapi_backend.proxy_header_trust'] = '''# Existing backend launch command; complete trusted-source and external-prefix settings.
uvicorn app:app --host 127.0.0.1 --port 8000
# TODO: allow only the fixture proxy source; do not grant unrestricted trust.
# TODO: configure the stripped /api prefix and verify public HTTPS URLs.
'''
starters['integration.webhook_contracts'] = '''from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
app=FastAPI()
@app.middleware("http")
async def media_guard(request, call_next):
    if request.url.path == "/order-events" and request.method == "POST":
        media=request.headers.get("content-type", "").split(";",1)[0].strip().lower()
        if media != "application/json":
            return JSONResponse(status_code=415, content={"reason":"unsupported media type"})
    return await call_next(request)
completed=[]
async def downstream(event):
    # Supplied bounded downstream stub; acknowledgement is not business completion.
    completed.append(event)
class OrderEvent(BaseModel):
    pass  # TODO: required fields from contract.json
@app.post("/order-events")  # TODO: declared acknowledgement status
async def receive(event: OrderEvent, background_tasks: BackgroundTasks):
    # TODO: accept the valid delivery and defer the supplied task as permitted.
    raise NotImplementedError
'''
starters['observability.request_correlation'] = '''import re, uuid, logging
from typing import Annotated
import httpx
from fastapi import FastAPI, Header
header_name="X-Interaction-ID"
url="https://receiver.example.test/orders"
received=[]
async def receiver(request):
    received.append(dict(request.headers))
    return httpx.Response(200, json={"accepted":True})
client=httpx.AsyncClient(transport=httpx.MockTransport(receiver))
logger=logging.getLogger("synthetic-order-events")
# Fixture policy: bounded ASCII, no sensitive caller data; invalid input gets a new id.
def keep_or_create(value):
    if value and re.fullmatch(r"[A-Za-z0-9-]{1,32}",value): return value
    return uuid.uuid4().hex
app=FastAPI()
@app.get("/orders/{order_id}")
async def read_order(order_id: int):
    # TODO: configured header binding, request-local id, log extra and outbound header.
    raise NotImplementedError
'''
starters['rest.bounded_resource_listing'] = '''from typing import Annotated
from fastapi import Query
from sqlalchemy import select
from support import Order
Entity=Order
predicate=Order.processing == "queued"
primary_sort_column=Order.quantity
unique_key=Order.id
# Fictional contract: one-based page 1..4, page_size 1..3; offset ceiling is (4-1)*3.
async def listing(session, page, page_size):
    # TODO: bounded Query declarations, derived offset and supplied filtered order.
    raise NotImplementedError
'''
starters['security.injection_resistant_inputs'] = '''from sqlalchemy import text
async def lookup(session, supplied_value):
    # Deliberately unsafe starter. Replace interpolation, retaining fixed SQL structure.
    statement = text(f"SELECT field FROM Entity WHERE field = '{supplied_value}'")
    return await session.execute(statement)
'''
starters['sqlalchemy.create_resource'] = '''from support import Entity
async def create(session, supplied_values, session_factory):
    # TODO: construct/add/flush/capture identity/commit; verify with an independent session.
    raise NotImplementedError
'''
starters['sqlalchemy.delete_resource'] = '''from support import Order
async def delete_order(session, identity):
    # TODO: lookup/absence/delete/flush/commit; rollback and propagate failure.
    raise NotImplementedError
async def verify_deletion(session_factory, identity, other_identity):
    # TODO: independent-session check of target absence and unaffected other order.
    raise NotImplementedError
'''
starters['sqlalchemy.update_resource'] = '''from pydantic import BaseModel
from support import Order
class PartialUpdate(BaseModel):
    note: str | None = None
    quantity: int | None = None
permitted_fields={"note", "quantity"}
async def update_order(session, order_id, request, session_factory):
    # TODO: extract supplied changes, assign permitted fields, commit or rollback.
    # Independently reload and check changed note AND preserved omitted quantity.
    raise NotImplementedError
'''
starters['auth.jwt_verification'] = '''import jwt
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fixtures import key, allowed_algorithm, expected_issuer, expected_audience
app=FastAPI()
async def extract(credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]):
    return credentials.credentials
async def verify(token: Annotated[str, Depends(extract)]):
    # TODO: trusted verification arguments, required claims, rejection on library errors.
    raise NotImplementedError
@app.get("/protected")
async def protected():
    # TODO: attach verification dependency; protected output only after acceptance.
    return {"protected":True}
'''
starters['cache.freshness_policy'] = '''# Inject a connected async Redis client; helper functions are provided separately.
# Fixture staleness tolerance: 30 seconds. Choose 0 < seconds <= tolerance_seconds.
tolerance_seconds=30
async def read_notes(cache, key, load_notes, seconds):
    cached=await cache.get(key)
    if cached is not None: return cached
    notes=await load_notes()
    await cache.set(key, notes)  # TODO: finite expiry within the supplied tolerance
    return notes
async def change_notes(cache, key, committed_update, new_notes):
    await committed_update(new_notes)
    # TODO: invalidate after committed primary change
'''
starters['cache.safe_failure_policy'] = '''from redis.asyncio import Redis
from redis.exceptions import ConnectionError, TimeoutError
# TODO: construct Redis with finite socket_connect_timeout and socket_timeout.
async def safe_read(cache, key, load_primary, seconds):
    # TODO: separate lookup/population exception boundaries; preserve primary return.
    raise NotImplementedError
'''
# Fixture configuration is authored; values implied by the glossary are extracted from rows.
by_id={row[0]:dict(zip([c['name'] for c in orders['columns']],row)) for row in orders['rows']}
fixtures = {
 'sqlalchemy.retrieve_resource': {'existing_identities':list(by_id), 'absent_identities':[999,1000], 'bounded_selection':{'predicate':{'processing':'queued'},'limit':3}},
 'sqlalchemy.transaction_boundaries': {'cases':['successful_exit','failing_second_write','failed_flush_then_reuse']},
 'auth.bearer_dependency': {'cases':[{'headers':{'Authorization':'Bearer synthetic-token'},'accepted_extraction':True},{'headers':{},'accepted_extraction':False},{'headers':{'Authorization':'Basic synthetic'},'accepted_extraction':False},{'headers':{'Authorization':'Bearer'},'accepted_extraction':False}], 'validity_verification':False},
 'cache.redis_cache_aside': {'requests':[[42,'notes'],[42,'quantity'],[43,'notes'],[42,'notes']], 'permitted_reuse':True,'expected_primary_values':[{'order_id':42,'notes':by_id[42]['note']},{'order_id':42,'quantity':by_id[42]['quantity']},{'order_id':43,'notes':by_id[43]['note']}], 'cases':['miss_then_hit','identity_separation','representation_separation']},
 'database.alembic_migrations': {'review_only':True,'candidate':'drop-and-add, possible rename','directions':['upgrade','downgrade'],'database_execution':False},
 'database.service_query_indexes': {'table':'orders','column':'external_reference','workload':'frequent equality lookup with ongoing writes','dialect':'postgresql','index_name':'ix_orders_external_reference'},
 'design.api_persistence_model_boundaries': {'row':by_id[42],'public_input_fields':['note','quantity'],'public_output_fields':['id','note','quantity'],'storage_only_fields':['processing','external_reference']},
 'fastapi.domain_error_translation': {'recognized_failure':'FailureClass','declared_status':409,'public_reason':'order conflict','session_initial_state':'failed','private_diagnostic':'synthetic private uniqueness diagnostic'},
 'fastapi.public_error_envelopes': {'body_field':'reason','cases':[{'path':'/fastapi-error','status':401,'reason':'credential required','headers':{'WWW-Authenticate':'Bearer'}},{'path':'/starlette-error','status':404,'reason':'not found','headers':{}}]},
 'fastapi_backend.proxy_header_trust': {'trusted_proxy_source':'192.0.2.10','external_base':'https://orders.example.test/api','stripped_prefix':'/api','backend_base':'http://127.0.0.1:8000','network_restricted_to_trusted_proxies':False,'verification':['redirect Location scheme and prefix','documentation URL scheme and prefix']},
 'integration.webhook_contracts': {'media_type':'application/json','required_fields':{'order_id':'integer','event':'string'},'event_shape':'JSON object','acknowledgement_status':202,'deferred_processing_permitted':True,'accepted_body':{'order_id':42,'event':'order.changed'},'invalid_bodies':[{'event':'order.changed'},{'order_id':'not-an-integer','event':'order.changed'}],'unsupported_media_type':'text/plain'},
 'observability.request_correlation': {'header_name':'X-Interaction-ID','accepted_ids':['chain-a','chain-b'],'rejected_ids':['space in id','x'*33],'cases':['accepted','missing','rejected','concurrent distinct requests'],'max_length':32},
 'rest.bounded_resource_listing': {'page_min':1,'page_max':4,'page_size_min':1,'page_size_max':3,'offset_ceiling':(4-1)*3,'predicate':{'processing':'queued'},'primary_sort_column':'quantity','unique_key':'id','ordered_matching_ids':[row['id'] for row in sorted(by_id.values(),key=lambda x:(x['quantity'],x['id'])) if row['processing']=='queued']},
 'security.injection_resistant_inputs': {'table':'Entity','column':'field','supplied_values':[row[0] for row in entity['rows']]+['absent'], 'placeholder':'value'},
 'sqlalchemy.create_resource': {'supplied_values':{'external_reference':'ref-new','note':'created note','quantity':5,'processing':'queued'},'generated_identity':True,'independent_verification':True},
 'sqlalchemy.delete_resource': {'target_identity':101,'other_identity':102,'absent_identity':999,'simulate_flush_failure':True},
 'sqlalchemy.update_resource': {'order_id':42,'partial_update':{'note':'new note 42'},'expected_unchanged_quantity':by_id[42]['quantity'],'permitted_fields':['note','quantity'],'simulate_failure':True},
 'auth.jwt_verification': {'required_claims':['exp','iss','aud'],'cases':['valid','wrong signature','wrong algorithm','wrong issuer','wrong audience','missing exp','missing iss','missing aud','expired','not yet valid']},
 'cache.freshness_policy': {'order_id':42,'cache_key':'order:42:notes','old_notes':by_id[42]['note'],'new_notes':'new note 42','tolerance_seconds':30,'ttl_sentinels':{'no_expiry':-1,'absent_key':-2}},
 'cache.safe_failure_policy': {'policy':'acceleration only; return available primary value','primary_value':{'order_id':42,'notes':by_id[42]['note']},'failure_operations':['get','set'],'exception_classes':['redis.exceptions.ConnectionError','redis.exceptions.TimeoutError'],'primary_failure_must_propagate':True}
}
transaction_support = '''from starter import WriteFailure
class Transaction:
    def __init__(self, session): self.session=session
    async def __aenter__(self):
        assert not self.session.failed
        self.session.pending=[]; return self.session
    async def __aexit__(self, kind, value, traceback):
        if kind is None: await self.session.commit()
        else: await self.session.rollback()
        return False
class Session:
    def __init__(self, fail_second=False, fail_flush=False):
        self.fail_second=fail_second; self.fail_flush=fail_flush
        self.pending=[]; self.durable=[]; self.failed=False; self.rollback_calls=0
    def begin(self): return Transaction(self)
    async def record(self, value): self.pending.append(value)
    async def commit(self): self.durable.extend(self.pending); self.pending=[]
    async def rollback(self):
        self.pending=[]; self.failed=False; self.rollback_calls+=1
    async def flush(self):
        if self.fail_flush:
            self.failed=True; raise WriteFailure("synthetic flush failure")
    async def reuse(self): assert not self.failed
'''
jwt_fixtures = '''import time
import jwt
# Synthetic trusted configuration, never production credentials.
key="synthetic-test-key-not-for-production-000000000000"
allowed_algorithm="HS256"
expected_issuer="https://issuer.example.test"
expected_audience="order-service"
def credential_cases():
    now=int(time.time())
    base={"sub":"synthetic-user","exp":now+3600,"iss":expected_issuer,"aud":expected_audience,"nbf":now-60}
    cases={"valid":jwt.encode(base,key,algorithm=allowed_algorithm)}
    for claim in ("exp","iss","aud"):
        payload=dict(base);payload.pop(claim)
        cases["missing "+claim]=jwt.encode(payload,key,algorithm=allowed_algorithm)
    for name,changes in [("expired",{"exp":now-60}),("not yet valid",{"nbf":now+3600}),("wrong issuer",{"iss":"https://other.example.test"}),("wrong audience",{"aud":"other-service"})]:
        cases[name]=jwt.encode(dict(base,**changes),key,algorithm=allowed_algorithm)
    cases["wrong signature"]=jwt.encode(base,"synthetic-other-signing-key-000000000000000000",algorithm=allowed_algorithm)
    cases["wrong algorithm"]=jwt.encode(base,key,algorithm="HS384")
    return cases
'''
# Each workspace owns a concrete starter and exact source-derived objective/constraints.
for b in bs:
    cid=b['context']['concept_id']
    if b['practice_anchor']['type'] != 'live_code': continue
    extension = 'sql' if cid=='database.service_query_indexes' else 'sh' if cid=='fastapi_backend.proxy_header_trust' else 'py'
    content = starters[cid]
    if cid=='design.api_persistence_model_boundaries':
        row=by_id[42];content=content.replace('SimpleNamespace(id=42, note="old note 42", quantity=2, processing="queued")', 'SimpleNamespace(**'+repr({k:row[k] for k in ['id','note','quantity','processing']})+')')
    anchor=b['practice_anchor']
    contract=dict(fixtures[cid]); contract['source_concept_id']=cid
    contract['objective']=anchor['objective'];contract['success']=anchor['success'];contract['live_code']=anchor['live_code']
    files=[{'path':'starter.'+extension,'content':content},{'path':'contract.json','content':json.dumps(contract,indent=2)+'\n'}, {'path':'README.md','content':'# '+b['context']['concept_name']+'\n\n'+anchor['live_code']['starter_state_intent']+'\n\nAll fixtures are authored for a fictional order service. TODOs are intentional, not runnable solutions. contract.json records the supplied fields, cases, allowed/blocked syntax and observable checks. Dependency adapters model only this anchor, not production services. External runtime dependencies must be supplied by the exercise engine.\n'}]
    dependencies=[]
    if cid.startswith('sqlalchemy.') and cid!='sqlalchemy.transaction_boundaries' or cid=='rest.bounded_resource_listing':
        files += [{'path':'support.py','content':orm_support},{'path':'orders.csv','content':csv_text(orders)}]
        dependencies += ['SQLAlchemy>=2,<3','aiosqlite']
    if cid.startswith('cache.'):
        files += [{'path':'support.py','content':cache_support},{'path':'orders.csv','content':csv_text(orders)}]
        dependencies += ['redis']
    if cid=='sqlalchemy.transaction_boundaries': files.append({'path':'support.py','content':transaction_support})
    if cid.startswith('fastapi.') or cid.startswith('auth.') or cid in ['design.api_persistence_model_boundaries','integration.webhook_contracts','observability.request_correlation','rest.bounded_resource_listing']:
        dependencies += ['fastapi','pydantic>=2,<3','httpx']
    if cid=='auth.jwt_verification':
        dependencies += ['PyJWT'];files.append({'path':'fixtures.py','content':jwt_fixtures})
    if cid=='security.injection_resistant_inputs':
        dependencies += ['SQLAlchemy>=2,<3','aiosqlite'];files.append({'path':'Entity.csv','content':csv_text(entity)})
        files.append({'path':'support.py','content':'''import csv
from pathlib import Path
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
async def make_store():
    engine=create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.execute(text("CREATE TABLE Entity (field TEXT)"))
        with open(Path(__file__).with_name("Entity.csv"),newline="") as handle:
            values=list(csv.DictReader(handle))
        await connection.execute(text("INSERT INTO Entity (field) VALUES (:field)"),values)
    return engine,async_sessionmaker(engine)
'''})
    if cid=='database.service_query_indexes': files.append({'path':'orders.csv','content':csv_text(orders)})
    if cid=='fastapi_backend.proxy_header_trust':
        dependencies += ['fastapi','uvicorn']
        files.append({'path':'app.py','content':'''from fastapi import FastAPI
app=FastAPI()
@app.get("/orders/")
async def orders():
    return []
'''})
    if dependencies: files.append({'path':'requirements.txt','content':'\n'.join(sorted(set(dependencies)))+'\n'})
    r['assets'].append({'asset_id':'ws.'+cid,'asset_kind':'code_workspace','scenario_id':sid,'title':b['context']['concept_name']+' — supplied exercise scaffold','runtime':'sql' if extension=='sql' else 'python','files':files})
# Dashboard provenance fixture is available to later stages without requiring a rendered chart.
(B/'working/service_signal_histograms.json').write_text(json.dumps(signal_fixtures,indent=2)+'\n')
# Validate the author's mistakes checklist independently of the stage gate.
assert len({a['asset_id'] for a in r['assets']})==len(r['assets'])
assert set(starters)=={b['context']['concept_id'] for b in bs if b['practice_anchor']['type']=='live_code'}
for a in r['assets']:
    if a['asset_kind']=='dataset':
        assert all(len(row)==len(a['columns']) for row in a['rows'])
        for c in a['columns']:
            assert c['semantic_role'] != 'numerical' or c['type'] in ('integer','number')
            assert c['semantic_role'] != 'datetime' or c['type'] in ('date','datetime')
        for v in a['variants']:
            assert all(op['op'] in ('set_cell','duplicate_row','drop_rows','drop_columns') for op in v['ops'])
    if a['asset_kind']=='code_workspace':
        for f in a['files']:
            if f['path'].endswith('.py'): ast.parse(f['content'],filename=f['path'])
assert len(fixtures['rest.bounded_resource_listing']['ordered_matching_ids']) >= 7
assert all(i in by_id for i in [42,43,101,102])
assert by_id[42]['quantity']==fixtures['sqlalchemy.update_resource']['expected_unchanged_quantity']
assert all(a['asset_kind']!='image' for a in r['assets']) # no glossary anchor depends on seeing a rendered plot
(B/'scenario_asset_registry.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
print('Scenarios:',len(r['scenarios']),'Assets:',len(r['assets']),'Datasets:',sum(a['asset_kind']=='dataset' for a in r['assets']),'Workspaces:',sum(a['asset_kind']=='code_workspace' for a in r['assets']))
print('Asset ids:',', '.join(a['asset_id'] for a in r['assets']))
print('Author checklist passed: row widths, semantic types, exact glossary identities/columns, pagination breadth, absence variants without false issues, scaffold syntax, all 21 concepts covered. No duplicate-row ops or numeric-label misconception traps in this glossary.')
