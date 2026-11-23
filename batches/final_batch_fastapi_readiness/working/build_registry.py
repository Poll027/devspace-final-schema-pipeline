import ast, csv, hashlib, io, json, re
from pathlib import Path

B = Path('batches/final_batch_readiness')
G = json.loads((B/'inputs/path_glossary_bundle.json').read_text())
S = 'scenario.order_service'
assets = []

def dataset(key, title, spec, rows, description=''):
    cols = []
    for name, typ, role in spec:
        c = dict(name=name, type=typ, semantic_role=role)
        if role in ('identifier', 'categorical') and any((isinstance(r[len(cols)], str) and r[len(cols)].isdigit()) or (isinstance(r[len(cols)], int) and not isinstance(r[len(cols)], bool)) for r in rows):
            c['numeric_looking_label'] = True
        cols.append(c)
    a = dict(asset_id='ds.'+key, asset_kind='dataset', scenario_id=S, title=title,
             description='Authored fictional fixture; not production evidence. '+description,
             columns=cols, rows=rows, provenance='authored')
    assets.append(a)
    return a

orders = dataset('orders','Order fixtures', [('id','integer','identifier'),('owner_id','string','identifier'),('status','string','categorical')],
                 [[101,'caller_a','pending'],[202,'caller_b','pending'],[303,'caller_a','complete']],
                 'Order.id and Order.owner_id support trusted-context object selection; status is the public projection and webhook change target.')
principals = dataset('principals','Trusted principal contexts',[('owner_id','string','identifier'),('scopes','string','categorical')],
                     [['caller_a','orders:read'],['caller_b','orders:read'],['caller_a','']],
                     'These are trusted fixture contexts, never caller-controlled ownership parameters; scope names are fictional fixture choices.')
release_rows = [['release_current','artifact_current','config_current','schema_current',True],
                ['release_prior_compatible','artifact_prior_compatible','config_prior_compatible','schema_current',True],
                ['release_prior_incompatible','artifact_prior_incompatible','config_prior_incompatible','schema_current',False]]
releases = dataset('releases','Immutable release records and supplied fixture compatibility',
                  [('release_id','string','identifier'),('artifact','string','identifier'),('configuration','string','identifier'),('current_database_schema','string','identifier'),('compatible','boolean','categorical')],release_rows,
                  'Compatibility is authored scenario evidence, not inferred from an artifact name.')
now = 1800000000
window, future = 300, 30
freshness_rows = []
for key, offset in [('fresh',-60),('past_boundary',-window),('expired',-window-1),('future_boundary',future),('future_rejected',future+1),('now',0)]:
    freshness_rows.append([key,str(now+offset),now,window,future,True])
freshness = dataset('delivery_timestamps','Authenticated delivery-timestamp cases',
                    [('case_id','string','identifier'),('signed_delivery_timestamp','string','datetime'),('receiver_now','integer','datetime'),('acceptance_window','integer','numerical'),('future_tolerance','integer','numerical'),('signature_verified','boolean','categorical')],freshness_rows,
                    'Integer seconds encoded as strings are temporal measurements, not numeric-looking labels. Hypothetical 300-second past window and 30-second future tolerance come from the practice anchor. Original event age is not asserted.')
parents = dataset('Entity','Parent entities',[('id','integer','identifier')],[[11],[22],[33]],'Generic Entity name and relationship_attribute match the glossary; one parent has an empty collection.')
children = dataset('relationship_attribute','Parent collection fixtures',[('id','integer','identifier'),('parent_id','integer','identifier')],[[111,11],[112,11],[221,22]],'No recorded SQL output is fabricated; use the workspace capture script to obtain baseline SQL in a provisioned SQLAlchemy environment.')
items = dataset('items','Database-isolation item fixture',[('id','integer','identifier')],[[1]],'A write target, not pre-existing database state. Each isolated test database starts empty.')
events = dataset('order_events','Authenticated publisher event fixtures',[('publisher_event_id','string','identifier'),('order_id','integer','identifier'),('new_status','string','categorical')],
                 [['evt_a',101,'complete'],['evt_b',202,'complete']], 'Inputs after signature authentication, not proof of publisher signing format.')
events['variants'] = [{'variant_id':'sequential_duplicate','derived_from':'base','purpose':'Two deliveries with identical authenticated event identity; business processing should acknowledge without a second effect.',
                       'ops':[{'op':'duplicate_row','where':{'publisher_event_id':'evt_a'},'occurrence':0,'insert':'after'}],
                       'planted_issues':[{'issue_id':'issue.repeated_delivery','kind':'duplicate_row','locations':[{'where':{'publisher_event_id':'evt_a'},'occurrence':1,'column':'publisher_event_id'}], 'description':'Second fixture delivery duplicates the first. This is expected delivery behavior, not corrupt durable event state.'}]}]
matrix_rows = []
for condition, perm, order_id, gate in [
    ('absent',False,101,'authentication'),('malformed',False,101,'authentication'),
    ('invalid_signature',True,101,'authentication'),('expired',True,101,'authentication'),
    ('wrong_issuer',True,101,'authentication'),('wrong_audience',True,101,'authentication'),
    ('valid_without_permission',False,101,'operation_authorization'),
    ('valid_other_owner',True,202,'object_authorization'),('valid_authorized',True,101,'public_result')]:
    # Denial choices are scenario contracts, not universal claims about FastAPI.
    status = 200 if gate=='public_result' else 401 if gate=='authentication' else 403
    body = {'id':101,'status':'pending'} if gate=='public_result' else {'detail':'Not authenticated' if gate=='authentication' else 'Forbidden'}
    matrix_rows.append([condition,'caller_a',perm,order_id,gate,status,json.dumps(body,sort_keys=True)])
matrix = dataset('authentication_test_matrix','Order endpoint security test matrix',
                 [('credential_condition','string','categorical'),('trusted_owner_id','string','identifier'),('operation_permission','boolean','categorical'),('requested_order_id','integer','identifier'),('rejection_gate_or_result','string','categorical'),('declared_status','integer','categorical'),('safe_body_or_public_result','string','text')],matrix_rows,
                 'Statuses and exact safe bodies are explicitly authored local endpoint contracts; they are not claimed as universal security defaults. No bearer credentials are stored here.')
metrics = dataset('operation_signals','Synthetic operation-window evidence',
                  [('operation','string','categorical'),('window','string','categorical'),('request_count','integer','numerical'),('window_seconds','integer','numerical'),('failure_count','integer','numerical'),('latency_ms','number','numerical')],
                  [['create_order','baseline',60,60,0,25.0],['create_order','affected',60,60,12,2025.0]],
                  'Illustrative signals, not measurements of a running service. Rate and failure fraction must be calculated from counts.')
records = dataset('correlated_records','Synthetic correlated failure evidence',
                  [('interaction_id','string','identifier'),('offset_ms','integer','numerical'),('boundary','string','categorical'),('event','string','categorical'),('sql_statement_count','integer','numerical')],
                  [['interaction_fixture',0,'local','request_received',0],['interaction_fixture',5,'database','lookup_complete',1],['interaction_fixture',10,'outbound','lookup_started',0],['interaction_fixture',2010,'outbound','timeout',0],['interaction_fixture',2025,'local','response_504',0]],
                  'Authored timing packet makes upstream waiting distinguishable from the small completed database operation. It is not a fabricated execution trace.')

# Materialize reusable CSV files and compute file metadata; never transcribe hashes.
(B/'assets').mkdir(exist_ok=True)
for a in assets:
    stream = io.StringIO(newline='')
    w = csv.writer(stream); w.writerow([c['name'] for c in a['columns']]); w.writerows(a['rows'])
    raw = stream.getvalue().encode()
    file = Path('assets')/(a['asset_id']+'.csv')
    (B/file).write_bytes(raw)
    a['data_file'] = {'uri':str(file),'format':'csv','sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}

# Source-mining first: exact domain/tool/code vocabulary from teaching and anchor text.
texts=[]
for b in G['bundles']:
    texts.extend(t['content'] for t in b['teaching_blocks'])
    texts.append(json.dumps(b['practice_anchor']))
    texts.append(json.dumps(b['visual_anchor']))
source_text='\n'.join(texts)
candidates=['order','orders','Order.id','Order.owner_id','owner_id','Entity','relationship_attribute','item','publisher event identifier','signed_delivery_timestamp','receiver_now','acceptance_window','future_tolerance','300','30','409','500','503','502','504','five-minute','FastAPI','Python','HTTPX','HTTPStatusError','RequestError','TestClient','JSONResponse','HTTPException','Pydantic','SQLAlchemy','selectinload','joinedload','Result.unique()','echo=True','join_transaction_mode','create_savepoint','SecurityScopes','Security','HTTPBearer','OAuth2AuthorizationCodeBearer','PyJWKClient','jwt.decode','PKCE','JWKS','Retry-After','Uvicorn','--limit-concurrency','/openapi.json','response_model','status_code','response_description','responses','PublicModel','Authorization','Bearer','await request.body()','raw bytes','endpoint signing secret','immutable release','artifact','configuration','database schema','interaction identifier']
vocab=[s for s in candidates if s in source_text]
# Include exact API forms and literals that the example sentences actually use.
for text in texts:
    for token in re.findall(r'\b[A-Za-z_]\w*\.[A-Za-z_]\w*(?:\(\))?',text):
        if token not in vocab: vocab.append(token)

snippets={}
fixtures={}
def put(concept, code, data=None):
    snippets[concept]=code.strip()+'\n'
    fixtures[concept]=data or {}

put('deployment.release_rollback_boundaries', '''
import json
from pathlib import Path
fixtures = json.loads(Path('fixtures.json').read_text())
releases = fixtures['releases']
current_database_schema = fixtures['current_database_schema']
selected_release = None  # TODO: select a compatible known prior release
procedure = {'build': None, 'release': None, 'run': None,
             'database_schema_after_rollback': None}
''', {'releases':[dict(zip([c['name'] for c in releases['columns']],r)) for r in release_rows], 'current_database_schema':'schema_current'})

put('fastapi.documented_responses', '''
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.testclient import TestClient
class PublicModel(BaseModel):
    id: int
    status: str
class ConflictModel(BaseModel):
    detail: str
app = FastAPI()
# TODO: complete only response documentation, preserving the outcome implementation.
@app.post('/orders')
def create_order(conflict: bool = False):
    if conflict:
        raise HTTPException(status_code=409, detail='Order conflict')
    return {'id': 101, 'status': 'pending'}
with TestClient(app) as client:
    success = client.post('/orders')
    conflict = client.post('/orders?conflict=true')
    schema = app.openapi()
    # TODO: compare actual responses with generated entries and schemas.
''', {'success_status':200,'success_body':{'id':101,'status':'pending'},'conflict_status':409,'conflict_body':{'detail':'Order conflict'}})

put('fastapi.safe_unexpected_errors', '''
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
app = FastAPI(debug=False)
safe_records = []
def record_safe_failure(request):
    safe_records.append({'event':'unexpected_failure','code_location':'controlled_failure',
                         'interaction_context':'interaction_fixture'})
@app.get('/controlled-failure')
def controlled_failure():
    raise RuntimeError('Controlled internal failure; never disclose this string')
# TODO: register @app.exception_handler(Exception), call record_safe_failure,
# and return the fixtures.json generic 500 body. Never log exception strings.
with TestClient(app, raise_server_exceptions=False) as client:
    response = client.get('/controlled-failure')
    # TODO: assert public response and safe internal records separately.
''', {'public_status':500,'public_body':{'detail':'Internal server error'},'prohibited_record_fields':['exception_message','locals','request_body','credentials']})

put('integration.upstream_failure_translation', '''
import httpx
from fastapi import FastAPI, Depends, HTTPException
from fastapi.testclient import TestClient
UPSTREAM_URL = 'https://upstream.invalid/lookup'  # Authored mock-only URL, never a provisioned service.
app = FastAPI()
async def client_provider():
    async with httpx.AsyncClient() as client:
        yield client
async def lookup(client):
    response = await client.get(UPSTREAM_URL)
    # TODO: raise_for_status and translate HTTPStatusError versus RequestError.
    return response.json()
@app.get('/lookup')
async def route(client=Depends(client_provider)):
    return await lookup(client)
def status_failure(request):
    return httpx.Response(503, request=request)
def timeout_failure(request):
    raise httpx.ReadTimeout('Controlled timeout', request=request)
# TODO: override client_provider with a MockTransport for each failure,
# then assert the supplied local status/body through TestClient.
''', {'upstream_503':{'status':502,'detail':'Upstream unavailable'},'timeout':{'status':504,'detail':'Upstream timed out'},'fallback':{'status':502,'detail':'Upstream unavailable'}})

put('integration.webhook_authenticity', '''
# Requires publisher-supported SDK and valid signed fixture: see provisioning.json.
async def webhook(request, signing_secret, publisher_verifier, signature_header, process_event):
    raw_body = await request.body()
    # TODO: use publisher_verifier against exact raw_body, signature header and
    # configured secret, following the supplied publisher contract.
    # Reject invalid/missing signatures before parsing or process_event.
    raise NotImplementedError('Complete verification gate using provisioned provider SDK')
processed_events = []
# TODO tests: valid signed raw body; modified raw body; absent signature.
# Only valid delivery may reach processed_events; rejection discloses no internals.
''')

put('observability.evidence_based_service_diagnosis', '''
import json
from pathlib import Path
packet = json.loads(Path('fixtures.json').read_text())
signals = packet['signals']
records = packet['records']
# TODO: compute rate and failure fraction, compare latency, trace interaction.
# Execute the failing payload using a provisioned TestClient order application,
# capture its status/body and supporting evidence before proposing a change.
controlled_outcome = None
suspected_boundary = None
supporting_evidence = []
proposed_change = None
''', {'signals':[dict(zip([c['name'] for c in metrics['columns']],r)) for r in metrics['rows']],
      'records':[dict(zip([c['name'] for c in records['columns']],r)) for r in records['rows']],
      'interaction_header':'X-Interaction-ID','interaction_id':'interaction_fixture','failing_order_payload':{'id':101,'status':'pending'},
      'packet_kind':'authored synthetic fixture; not observed HTTP or SQL output'})

put('security.bounded_api_resources', '''
from pydantic import BaseModel, Field
class BatchInput(BaseModel):
    order_ids: list[int]  # TODO: Field bounds from fixtures.json
expensive_calls = 0
async def expensive_dependency(order_ids):
    global expensive_calls
    expensive_calls += 1
    return {'accepted':len(order_ids)}
# TODO: use provisioned maintained body-byte middleware, finite dependency
# timeout and supplied Uvicorn concurrency budget. Count actual body bytes.
# Assert rejected requests never reach expensive_dependency.
''', {'hypothetical_budgets':{'body_bytes':256,'batch_size':3,'dependency_timeout_seconds':2,'limit_concurrency':8},
      'within_batch':{'order_ids':[101,202]},'beyond_batch':{'order_ids':[101,202,303,404]},
      'within_body':{'order_ids':[101]},'beyond_body':{'order_ids':[101]*100},
      'public_success':{'accepted':2},'note':'Local fixture budgets; middleware package/configuration must be supplied before execution.'})

put('sqlalchemy.redundant_queries', '''
from sqlalchemy import ForeignKey, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session, selectinload
class Base(DeclarativeBase):
    pass
class Entity(Base):
    __tablename__ = 'Entity'
    id: Mapped[int] = mapped_column(primary_key=True)
    relationship_attribute: Mapped[list['Child']] = relationship(back_populates='parent')
class Child(Base):
    __tablename__ = 'relationship_attribute'
    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('Entity.id'))
    parent: Mapped[Entity] = relationship(back_populates='relationship_attribute')
engine = create_engine('sqlite://', echo=True)
Base.metadata.create_all(engine)
with Session(engine) as session:
    session.add_all([Entity(id=11),Entity(id=22),Entity(id=33),
                     Child(id=111,parent_id=11),Child(id=112,parent_id=11),Child(id=221,parent_id=22)])
    session.commit()
def listing(session):
    statement = select(Entity).order_by(Entity.id).limit(3)
    # TODO: statement.options(selectinload(Entity.relationship_attribute))
    parents = session.execute(statement).scalars().all()
    return [{'id':p.id, 'children':[c.id for c in p.relationship_attribute]} for p in parents]
# Run baseline and changed listing in separate fresh sessions and capture echo
# output; do not reuse already-loaded relationships when measuring the change.
if __name__ == '__main__':
    with Session(engine) as session:
        print(listing(session))
''', {'parent_ids':[r[0] for r in parents['rows']], 'children':[dict(zip(['id','parent_id'],r)) for r in children['rows']],
      'baseline_capture_required':True,'note':'SQLAlchemy is absent in the pack engine. No SQL output or measured baseline is asserted.'})

put('testing.database_state_isolation', '''
import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
# app, engine and session_provider must come from the provisioned item application.
@pytest.fixture
def isolated_client(app, engine, session_provider):
    original_overrides = app.dependency_overrides.copy()
    connection = engine.connect()
    outer_transaction = connection.begin()
    # TODO: bind Session with join_transaction_mode="create_savepoint".
    test_session = None
    # TODO: override session_provider with a yield provider using test_session.
    try:
        with TestClient(app) as client:
            yield client, test_session
    finally:
        # TODO: close session, roll back outer transaction, close connection,
        # restore original_overrides even if the test fails.
        pass
# TODO: test write/read within one boundary; test target absence in another.
# Run both execution orders. Never migrate/create schema inside per-test transaction.
''', {'item':dict(zip(['id'],items['rows'][0])),'initial_items':[],'execution_orders':[['writes_item','item_absent'],['item_absent','writes_item']]})

put('auth.authorization_server_integration', '''
# No issuer is provisioned in the supplied glossary. Do not replace this with
# invented endpoint URLs, locally fabricated valid tokens or verifier overrides.
def integrate(provisioned_client, issuer_configuration, existing_verifier, http_client):
    # TODO: configure registered client, code redirect and separate token POST
    # with matching PKCE verifier where applicable; use actual issued token.
    # Configure PyJWKClient and jwt.decode trust settings from supplied issuer.
    # HTTP-assert acceptance and rejection with extraction/verifier active.
    raise NotImplementedError('Requires provisioned issuer and acquisition client')
''')

put('auth.endpoint_permissions', '''
from fastapi import FastAPI, Security, HTTPException
from fastapi.security import SecurityScopes
app = FastAPI()
# verified_token_context must keep real credential verification in the HTTP graph.
def require_permissions(security_scopes: SecurityScopes, verified_token_context):
    # TODO: require every operation scope in verified_token_context scopes.
    raise NotImplementedError('Complete permission comparison')
# TODO: wire Security(provider, scopes=[...]) for the existing operation.
# Test valid verified token with and without required scope separately.
''', {'operation_scopes':['orders:read'],'verified_with_permission':{'owner_id':'caller_a','scopes':['orders:read']},'verified_without_permission':{'owner_id':'caller_a','scopes':[]},
      'note':'Contexts illustrate permission comparison; they do not replace real signed bearer fixtures in HTTP verification.'})

put('fastapi_backend.webhook_delivery_idempotency', '''
from sqlalchemy import String, Integer, UniqueConstraint, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.exc import IntegrityError
class Base(DeclarativeBase):
    pass
class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
class ProcessedEvent(Base):
    __tablename__ = 'processed_events'
    id: Mapped[int] = mapped_column(primary_key=True)
    publisher_event_id: Mapped[str] = mapped_column(String)
    __table_args__ = (UniqueConstraint('publisher_event_id'),)
async def handle_authenticated_event(event, session):
    # TODO: event record and order update inside one session.begin transaction.
    # Confirm already processed identity before acknowledging a duplicate;
    # never translate unrelated IntegrityError into successful processing.
    raise NotImplementedError('Complete atomic persistent deduplication')
# Provision async sessions and durable database before sequential/restart/
# concurrent tests. Failure must commit neither record nor order change.
''', {'authenticated_events':[dict(zip([c['name'] for c in events['columns']],r)) for r in events['rows']],
      'orders':[dict(zip([c['name'] for c in orders['columns']],r)) for r in orders['rows']],
      'tests':['sequential_duplicate','restart_with_database_retained','concurrent_duplicate','transaction_failure'],'initial_processed_events':[]})

put('fastapi_backend.webhook_replay_freshness', '''
import json
from pathlib import Path
def delivery_is_fresh(signed_delivery_timestamp, receiver_now, acceptance_window, future_tolerance):
    # Signature verification already completed. Inputs are valid integer seconds.
    # TODO: enforce both past window and future tolerance; no real clock reads.
    raise NotImplementedError('Complete signed delivery timestamp comparison')
cases = json.loads(Path('fixtures.json').read_text())['cases']
# TODO: exercise in-window, expired and future cases plus exact boundaries.
''', {'cases':[dict(zip([c['name'] for c in freshness['columns']],r)) for r in freshness_rows]})

put('integration.bounded_idempotent_retries', '''
import json
from pathlib import Path
contract = json.loads(Path('fixtures.json').read_text())
policy = {'retryable_failures':None,'max_attempts':None,'total_time_budget':None,
          'retry_after':None,'bounded_backoff':None,'retry_safe':None}
# TODO: complete policy for the provisioned maintained adapter. Respect both
# Retry-After forms. Timeout/lost response alone never proves no remote effect.
# Test transient-then-success, exhausted budget and unsafe non-idempotent case.
''', {'hypothetical_limits':{'max_attempts':3,'total_time_budget_seconds':10,'max_backoff_seconds':2},
      'operations':[{'method':'GET','contract_idempotent':True},{'method':'POST','contract_idempotent':False,'known_not_applied':False}],
      'verification_scenarios':['transient_then_success','repeated_failures','non_idempotent_lost_response'],
      'retry_after_delay_seconds':'2',
      'retry_after_http_date':__import__('email.utils',fromlist=['formatdate']).formatdate(now+2,usegmt=True),'receiver_now':now,
      'note':'Authored fixture policy. Adapter configuration names must be supplied; no client-internal implementation is implied.'})

put('auth.object_authorization', '''
from sqlalchemy import select
async def retrieve_order(order_id, principal, session, Order):
    statement = select(Order).where(Order.id == order_id)
    # TODO: also filter Order.owner_id by trusted principal.owner_id.
    return await session.scalar(statement)
# Use trusted-principal override only for this object-boundary exercise;
# do not accept owner_id from caller input. Test all four principal/order pairs.
''', {'principals':[{'owner_id':'caller_a'},{'owner_id':'caller_b'}],
      'orders':[dict(zip([c['name'] for c in orders['columns']],r)) for r in orders['rows'][:2]],
      'pairs':[[p,o] for p in ['caller_a','caller_b'] for o in [101,202]]})

put('fastapi.production_security_documentation', '''
from fastapi.security import HTTPBearer, OAuth2AuthorizationCodeBearer
bearer_scheme = HTTPBearer()
def authorization_code_scheme(issuer_configuration):
    # TODO: use actual supplied authorization/token URLs and scope descriptions.
    # No invented issuer URLs, and no password grant.
    raise NotImplementedError('Requires supplied established issuer contract')
# TODO: wire real operation dependencies/scopes; inspect securitySchemes and
# operation security declarations against deployed authority, not imagined flows.
''')

put('fastapi.openapi_contract_inspection', '''
def audit(client, models, http_evidence, security_configuration):
    response = client.get('/openapi.json')
    schema = response.json()
    findings = []
    # TODO: select supplied orders router and inspect declarations against
    # models, non-auth HTTP evidence and established security configuration.
    # Validate synthetic examples. Do not add authentication/authorization tests.
    return findings
''', {'router':'orders','synthetic_example':{'id':101,'status':'pending'},
      'audit_dimensions':['paths','parameters','requiredness','types','constraints','request_schemas','response_schemas','output_fields','statuses','examples','descriptions','security_requirements'],
      'note':'Generated OpenAPI and exercised HTTP outcomes must come from the provisioned app; this fixture makes no claim of observed behavior.'})

put('testing.api_authentication_authorization', '''
import json
from pathlib import Path
from fastapi.testclient import TestClient
cases = json.loads(Path('fixtures.json').read_text())['cases']
def test_order_gate(app, bearer_fixtures, case):
    # bearer_fixtures must be signed controlled credentials; never override
    # bearer extraction or the verifier for this exercise.
    with TestClient(app) as client:
        headers = {}  # TODO: absent/malformed/signed fixture per condition
        response = client.get(f"/orders/{case['requested_order_id']}", headers=headers)
        # TODO: exact declared status and safe denial body/public projection.
''', {'cases':[dict(zip([c['name'] for c in matrix['columns']],r)) for r in matrix_rows],
      'note':'Controlled signed tokens and the real protected endpoint are required; row labels are not bearer credentials.'})

external={
'integration.webhook_authenticity':['publisher identity and installed supported verification library','documented signature header and format','validated endpoint signing-secret configuration','valid publisher-signed raw fixture and rejection contract'],
'observability.evidence_based_service_diagnosis':['existing order application with controlled failing lookup and TestClient fixture'],
'security.bounded_api_resources':['maintained body-byte middleware and documented configuration','existing batch HTTP application'],
'sqlalchemy.redundant_queries':['SQLAlchemy package; capture actual echo SQL baseline before editing'],
 'testing.database_state_isolation':['existing item application and session provider','database engine supporting external transaction/savepoint test pattern'],
'auth.authorization_server_integration':['provisioned established issuer','registered client identifier, authorization URL, token URL and redirect URI','trusted JWKS URL, issuer, algorithms, required claims and API audience','acquisition client/harness and actual issuer-issued access tokens','real protected endpoint and existing bearer/JWT verifier'],
'auth.endpoint_permissions':['protected endpoint and real verified-token dependency','controlled signed tokens with and without operation permission'],
'fastapi_backend.webhook_delivery_idempotency':['durable database and request-scoped async sessions','HTTP sequential/restart/concurrency harness'],
'integration.bounded_idempotent_retries':['maintained adapter and documented policy fields/failure classifications'],
'auth.object_authorization':['order HTTP application, session provider and trusted-principal request harness'],
'fastapi.production_security_documentation':['existing protected operations and real dependency graph','actual supplied issuer authorization/token endpoints and scope descriptions','applicable PKCE acquisition contract'],
'fastapi.openapi_contract_inspection':['existing app/router and public models','generated schema and exercised non-authentication HTTP evidence','established issuer/bearer configuration'],
 'testing.api_authentication_authorization':['real protected order endpoint with active extraction/verifier and both authorization gates','controlled bearer fixtures for each signature/expiry/context/permission condition']}

for b in G['bundles']:
    cid=b['context']['concept_id']
    code=snippets[cid]
    ast.parse(code)
    anchor=b['practice_anchor']
    contract={'concept_id':cid,'teaching_blocks':b['teaching_blocks'],'visual_anchor':b['visual_anchor'],'practice_anchor':anchor,
              'required_facts':b['coverage']['required_facts']}
    provision={'status':'requires_external_provisioning' if cid in external else 'requires_runtime_dependencies',
               'missing_from_supplied_glossary':external.get(cid,[]),
               'policy':'Do not invent issuer URLs, provider signing formats, library APIs, execution traces or actual credentials. Fixture values are fictional scenario data, not real-world facts.'}
    files=[{'path':'starter.py','content':code},
           {'path':'fixtures.json','content':json.dumps(fixtures[cid],indent=2)+'\n'},
           {'path':'glossary_contract.json','content':json.dumps(contract,indent=2)+'\n'},
           {'path':'provisioning.json','content':json.dumps(provision,indent=2)+'\n'},
           {'path':'README.md','content':'# '+b['context']['concept_name']+'\n\nFictional order-service training workspace.\n\n'+anchor['live_code']['starter_state_intent']+'\n\nStarter code is deliberately incomplete; not a completed solution. See glossary_contract.json for exact sourced teaching and observable success. See provisioning.json for runtime or publisher/issuer prerequisites not present in the glossary. Do not treat authored evidence packets as captured code output. No hypothetical issuer may stand in for actual issuer integration.\n'}]
    assets.append({'asset_id':'ws.'+cid,'asset_kind':'code_workspace','scenario_id':S,'title':b['context']['concept_name']+' — starter workspace','runtime':'python','files':files})

registry={'schema_version':'1.0','kind':'scenario_asset_registry','path_id':G['path_id'],'batch_id':B.name,
          'scenarios':[{'scenario_id':S,'name':'Fictional order-service readiness lab',
                        'summary':'A small fictional FastAPI order service is preparing a release. Two callers have separate orders; the team exercises response contracts, upstream failures, webhook boundaries, persistence, security and release records in isolated training fixtures. Issuer integration requires an actually provisioned authorization server, which the glossary does not supply.',
                        'domain':'backend order service','glossary_example_vocab':vocab}], 'assets':assets}
(B/'scenario_asset_registry.json').write_text(json.dumps(registry,indent=2)+'\n')

# Local checklist: structural, role, source vocabulary, op/predicate and whole-scope checks.
import sys
sys.path.insert(0,str(Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
from checkers.dataset import resolve_dataset, find_row
for a in assets:
    if a['asset_kind']!='dataset':continue
    assert all(len(r)==len(a['columns']) for r in a['rows'])
    assert len({c['name'] for c in a['columns']})==len(a['columns'])
    for i,c in enumerate(a['columns']):
        assert c['semantic_role']!='numerical' or c['type'] in ('integer','number')
        for r in a['rows']:
            v=r[i]
            assert {'integer':lambda: isinstance(v,int) and not isinstance(v,bool),
                    'number':lambda:isinstance(v,(float,int)) and not isinstance(v,bool),
                    'string':lambda:isinstance(v,str), 'boolean':lambda:isinstance(v,bool)}[c['type']]()
    for variant in a.get('variants',[]):
        _,rows=resolve_dataset(registry,a['asset_id'],variant['variant_id'])
        for issue in variant.get('planted_issues',[]):
            for loc in issue['locations']:
                i=find_row(rows,loc['where'],loc['occurrence']); assert i is not None
                assert sum(r==rows[i] for r in rows)==2
                assert loc['occurrence']==1
assert set(snippets)=={b['context']['concept_id'] for b in G['bundles']}
assert all(v in source_text for v in vocab)
assert not any(a['asset_kind']=='image' for a in assets)
report={'artifact':'scenario_asset_registry.json','scenario_count':1,'concept_count':len(G['bundles']),
        'asset_count':len(assets),'dataset_count':sum(a['asset_kind']=='dataset' for a in assets),
        'workspace_count':len(snippets),'row_count':sum(len(a.get('rows',[])) for a in assets),
        'variant_count':sum(len(a.get('variants',[])) for a in assets),
        'checks':{'row_widths':'pass','declared_types_and_unambiguous_roles':'pass','planted_duplicate_after_ops_and_occurrence':'pass',
                  'all_concepts_have_workspace':'pass','example_vocab_mined_from_source':'pass',
                  'numeric_looking_label_traps':'Integer order/entity identifiers and HTTP status labels explicitly flagged; epoch timestamps are temporal measurements, not labels.',
                  'required_plots':'No visual or teaching anchor depends on seeing a rendered plot. All are code, comparison, process_flow or data_table.',
                  'domain_coverage':'Orders/owners, release records, parent collections, item target, event identities, freshness, evidence and exact security matrix are registered; contract/fixtures travel with each workspace.'},
        'uncertainties':external}
(B/'working/registry_self_check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('checks','uncertainties')},indent=2))
