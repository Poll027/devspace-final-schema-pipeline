import json, pathlib, copy, subprocess, sys, os
B=pathlib.Path('batches/final_batch_readiness'); W=B/'working/interactions_work'
plans=json.loads((B/'tile_plans.json').read_text()); screens=json.loads((B/'screens.json').read_text()); glossary=json.loads((B/'inputs/path_glossary_bundle.json').read_text()); registry=json.loads((B/'scenario_asset_registry.json').read_text()); pins=json.loads(pathlib.Path('00_FINAL_PIPELINE_CORE/registry/runtimes.json').read_text())['runtimes']
bundles={x['context']['concept_id']:x for x in glossary['bundles']}; assets={x['asset_id']:x for x in registry['assets']}; screenmap={x['tile_id']:x for x in screens['tiles']}
def load(c,p):return (W/c/p).read_text()
def fixture(c):return json.loads(load(c,'fixtures.json'))
# Each tuple explicitly marks the correct alternative; the key is derived from this designation.
Q={}
def q(s,p,good,bad1,why1,bad2,why2):Q[s]=(p,[(good,True,'This matches the declared contract and the evidence the question asks for.'),(bad1,False,why1),(bad2,False,why2)])
q('tile_082.s03','A uniquely identified prior release is compatible with the current schema; another prior release is incompatible. Which rollback procedure is justified?', 'Select the compatible prior artifact with its recorded configuration; leave the current database schema unchanged.', 'Select either prior artifact; application rollback automatically reverses migrations.', 'Application rollback does not automatically reverse database schema changes; compatibility must be checked.', 'Edit the running release to use only the prior artifact and keep whichever configuration is live.', 'Release records are immutable, and the recorded artifact and intended configuration belong together.')
q('tile_083.s02','An operation declares a 409 response but the exercised conflict path returns 400. What has been established?', 'The declaration and observed HTTP outcome disagree; the declaration alone does not implement 409.', 'The responses declaration makes the conflict path return 409.', 'Additional response metadata documents an outcome; it does not change the handler response.', 'The response description proves that the actual body matches the declared model.', 'A description is documentation, not evidence that an exercised body matches its model.')
q('tile_083.s05','Which public response is appropriate for a controlled unexpected failure?', 'A fixed generic JSON error body with status 500 and no exception details.', 'A JSON error body containing the exception message for easier client diagnosis.', 'Exception messages can expose implementation details and do not belong in the generic public error.', 'A JSON error body containing the full traceback but omitting credentials.', 'Removing credentials does not make a traceback safe public information.')
q('tile_083.s06','Which separation keeps unexpected-error evidence useful without exposing prohibited data?', 'Return generic public information; record event, code location and interaction context internally without secrets or sensitive payloads.', 'Return internal code location and exception text publicly, but keep request credentials only in logs.', 'Internal implementation details must not be disclosed publicly, and credentials must not be logged.', 'Use a generic public body and log the complete request body and local variables.', 'A safe public response does not justify storing sensitive payloads or local variables internally.')
q('tile_085.s03','The supplied mapping says upstream 503 becomes local 502 with a fixed public detail, and timeout becomes local 504 with a fixed public detail. Which implementation follows that mapping?', 'Translate each classified failure to its declared local status and fixed detail.', 'Always pass through the upstream status and raw body.', 'Local outcomes follow the declared mapping, not an uncontrolled upstream body or status.', 'Return the raw timeout exception as the public 504 detail.', 'The public detail must be fixed and safe rather than exposing exception internals.')
q('tile_085.s04','Which test provides evidence for both the mapped failure and safe public output?', 'Assert the exact declared local status and fixed body for each failure, checking that upstream internals are absent.', 'Assert only that the HTTP status is an error.', 'An arbitrary error does not prove the declared mapping or safe body.', 'Assert that raw upstream exception text appears in the body.', 'Raw upstream internals must be absent, not required in the public output.')
q('tile_086.s03','A delivery has no signature, or verification fails. What must happen before event processing?', 'Reject it with a safe response and do not process the event.', 'Process it first, then reject it if verification fails.', 'Rejection must prevent processing, not occur after its effects.', 'Accept it if the parsed payload resembles a known event.', 'A familiar payload is not successful signature verification.')
q('tile_087.s03','Correlated evidence shows local input accepted, database lookup completed, then the outbound call timed out before the final local error. Which boundary does this evidence support investigating first?', 'The outbound dependency boundary, using the timeout evidence rather than only the final local error.', 'The database boundary solely because the endpoint returns an error.', 'A final endpoint error does not override evidence that database work completed before the outbound timeout.', 'Local input handling solely because the response was generated locally.', 'Generating the final response locally does not identify local input handling as the first failing boundary.')
q('tile_088.s03','Which policy actually bounds expensive work for a batch endpoint?', 'Enforce actual received-body bytes and validated batch cardinality before expensive work.', 'Trust a client-declared size while accepting any actual body and batch size.', 'A claimed size does not enforce the received-body or batch budget.', 'Validate the batch only after the expensive dependency has run.', 'Late validation does not bound expensive work before it happens.')
q('tile_088.s04','Which observation demonstrates rejection before expensive work?', 'An out-of-budget input receives the declared rejection and the dependency invocation count remains zero.', 'An out-of-budget input receives an error after the dependency is called.', 'An error after invocation does not prove rejection before expensive work.', 'The request succeeds but the response says that a limit exists.', 'A stated limit is not evidence of actual enforcement.')
q('tile_089.s04','A parent listing emits one relationship SELECT per parent. Which change targets this repeated collection-loading pattern?', 'Use statement.options(selectinload(Entity.relationship_attribute)) to batch collection loading.', 'Keep lazy collection access for every parent and call it eager loading.', 'Renaming the pattern does not remove per-parent relationship queries.', 'Remove every parent with an unloaded relationship from the result.', 'Dropping parents changes the returned data instead of fixing collection loading.')
q('tile_089.s05','Which comparison proves query reduction without changing the listing?', 'Capture emitted SQL in fresh sessions and compare parent identities and collection contents before and after.', 'Count fewer SQL statements but do not compare returned data.', 'A smaller query count can accompany missing or altered data; both must be checked.', 'Reuse already-loaded relationships and compare only parent count.', 'Already-loaded collections hide loading queries, and parent count alone does not prove collection equivalence.')
q('tile_090.s04','A fixture opens a connection and outer transaction and binds a test session. Which teardown is complete even when an assertion fails?', 'Close the session, roll back the outer transaction, close the connection and restore the previous dependency overrides in finally.', 'Close only the TestClient and leave the transaction and overrides intact.', 'Client closure alone does not clean up the database boundary or dependency overrides.', 'Commit the outer transaction and clear all previous overrides permanently.', 'Committing preserves test writes, and clearing previous overrides does not restore the original configuration.')
q('tile_090.s05','The writer test passes, but the absence test sees its item only when run after the writer. What does this show?', 'A test write leaked across test boundaries; run both orders after repairing isolation.', 'Correct isolation because each test passes when run alone.', 'Passing alone does not prove independence from earlier writes.', 'A harmless ordering preference that should be fixed by always running absence first.', 'Forcing one order hides leakage rather than proving isolation.')
q('tile_091.s04','Which evidence proves the supplied issuer integration rather than bypassing it?', 'Send an actual issuer-issued access token through the protected HTTP endpoint; separately reject a tampered token and a wrong-audience issuer token with extraction and verification active.', 'Override authentication to return an authorized principal and call the endpoint.', 'An authentication override bypasses the issuer integration being tested.', 'Fabricate a locally accepted valid token in the resource server and skip HTTP.', 'Local token fabrication and helper-only checks do not prove acceptance of an actual issuer-issued token through the endpoint.')
q('tile_091.s08','Two otherwise verified requests differ only in whether they carry orders:write. What comparison proves the operation permission boundary?', 'The request with orders:write succeeds; the request lacking it receives the declared denial.', 'Both succeed because token verification has already completed.', 'Verified identity does not supply a missing operation permission.', 'Reject the insufficient request before verification and call that a scope check.', 'A credential rejection does not isolate permission enforcement on an otherwise verified request.')
q('tile_093.s03','An authenticated event identifier has already committed its order change and event record. The application restarts and receives the same identifier. What should persistent deduplication do?', 'Acknowledge the duplicate successfully without another committed order change.', 'Apply it again because the in-memory process state was lost.', 'The deduplication record must persist across process restarts.', 'Keep only an in-memory set and assume it survives a restart.', 'Process-local memory is not a persistent processed-event record.')
q('tile_093.s07','Why does signed-delivery freshness require an accurate receiver clock?', 'The receiver compares the authenticated delivery timestamp against its current time and finite tolerances.', 'A valid signature makes the receiver clock irrelevant.', 'Signature validity and time-window classification are separate checks.', 'The check uses original event age only, never receiver time.', 'Delivery freshness compares signed delivery time with receiver time, not solely original event age.')
q('tile_093.s08','Which test set isolates timestamp freshness from authenticity?', 'Establish valid signatures, then test in-window, expired and beyond-future-tolerance delivery timestamps.', 'Use invalid signatures for every case and infer freshness from rejection.', 'Signature rejection alone does not exercise the timestamp-freshness decision.', 'Test only one in-window signed delivery.', 'One acceptance does not prove rejection at either time boundary.')
q('tile_093.s12','Which supplied checks establish the bounded retry policy?', 'Transient failure followed by success, repeated-failure exhaustion, and no blind repetition of an unsafe non-idempotent operation.', 'Only retry repeatedly until a transient failure eventually succeeds.', 'Eventual success alone does not prove stopping budgets or prevention of unsafe repetition.', 'Treat a lost response as proof that a non-idempotent remote operation had no effect.', 'A lost response does not establish that the remote effect did not occur.')
q('tile_096.s02','A valid caller can retrieve another caller’s order by changing only the order identifier. Which boundary is missing?', 'Object authorization binding the requested order to the trusted owner context.', 'Only authentication, because valid identity guarantees every order is available.', 'Valid identity does not authorize access to every object.', 'A caller-controlled owner_id query parameter as the source of authority.', 'Caller input cannot replace trusted owner identity in the object filter.')
q('tile_096.s03','Which HTTP test matrix proves isolation between two trusted owner contexts?', 'Each caller retrieves its own order, and both swapped order identifiers return the declared unavailable result without order data.', 'One caller retrieves its own order; skip both cross-owner requests.', 'Own-object success alone does not test cross-owner denial.', 'Send both callers as the same trusted owner and compare only response status.', 'Using the same owner fails to exercise separation between owners.')
q('tile_097.s03','What does a deployed HTTPBearer OpenAPI scheme describe?', 'Bearer-token presentation to the API, not a claim that the API issues tokens.', 'A password grant provided by the API.', 'Bearer presentation does not imply password-grant acquisition.', 'The authorization server’s token issuance implementation.', 'HTTPBearer describes presentation, not the issuer implementation.')
q('tile_097.s04','Which inspection checks security declarations against existing operation authority?', 'Compare generated schemes and each protected operation’s security requirements with supplied issuer URLs, bearer presentation and required scopes.', 'Check only that components.securitySchemes is non-empty.', 'A non-empty scheme collection does not prove issuer or operation agreement.', 'Add scope names only to a description while removing permission dependencies.', 'Documentation cannot replace the real operation authority or permission enforcement.')
q('tile_097.s08','The established contract supplies bearer presentation and authorization-code/PKCE acquisition. Which public declaration is drift?', 'An OAuth2 password grant that is not part of the established deployed contract.', 'The supplied authorization-code URLs and permission descriptions.', 'Accurate supplied authorization-code metadata agrees with the deployed contract.', 'Bearer presentation plus operation requirements matching the configured authority.', 'Accurate bearer and operation declarations are not mismatches.')
q('tile_097.s12','What must each denial and fully authorized request assert?', 'The exact declared denial status and safe body without protected output, or the expected public projected result for full authorization.', 'Only that denials fail and one request succeeds.', 'Generic pass/fail observations do not verify complete declared response contracts.', 'The entire internal stored order including owner details for the successful response.', 'The success assertion must check the public projection, not require internal stored fields.')
solutions={}; tasks={}; native_commands={}; native_expected={}; supported={}
def add(c,code,task,command=None):
 solutions[c]=code;tasks[c]=task
 if command:native_commands[c]=command
# Python entry scaffolding has all supplied fixtures inline because the pinned runner
# executes the entry file, not arbitrary side modules.
c='deployment.release_rollback_boundaries'; f=fixture(c)
pre='import json\nfixtures = json.loads('+repr(json.dumps(f))+')\nreleases = fixtures["releases"]\ncurrent_database_schema = fixtures["current_database_schema"]\n'
start=pre+"prior_release = releases[1]\nselected_release = None\nprocedure = {}\n"
sol=pre+"prior_release = releases[1]\n"+'''selected_release = prior_release
procedure = {'build': selected_release['artifact'],
             'release': {'artifact': selected_release['artifact'], 'configuration': selected_release['configuration']},
             'run': selected_release['release_id'],
             'database_schema_after_rollback': current_database_schema}
'''
ns={};exec(sol,ns);supported[c]=(start,sol,[('value_equals',{'expr':'procedure','expected':ns['procedure']}),('value_equals',{'expr':'releases','expected':f['releases']})],'python',[])
tasks[c]='Complete selected_release and procedure for the supplied compatible prior release (releases[1]). Set build to its artifact; release to a dictionary with artifact and configuration; run to its unique release_id. Record database_schema_after_rollback as the current schema. Preserve all existing release records. Application rollback does not reverse the schema.'
c='fastapi_backend.webhook_replay_freshness'
start='def delivery_is_fresh(signed_delivery_timestamp, receiver_now, acceptance_window, future_tolerance):\n    # Inputs are integer seconds; signature verification is already complete.\n    raise NotImplementedError("Complete both timestamp bounds")\n'
sol='def delivery_is_fresh(signed_delivery_timestamp, receiver_now, acceptance_window, future_tolerance):\n    return -future_tolerance <= receiver_now - signed_delivery_timestamp <= acceptance_window\n'
ns={};exec(sol,ns);ts=[]
for case in fixture(c)['cases']:
 args=[int(case[k]) for k in ['signed_delivery_timestamp','receiver_now','acceptance_window','future_tolerance']];ts.append(('function_call',{'function':'delivery_is_fresh','args':args,'expected':ns['delivery_is_fresh'](*args)}))
supported[c]=(start,sol,ts,'python',[]);tasks[c]='Complete delivery_is_fresh to return a boolean: accept integer signed delivery seconds in the inclusive interval [receiver_now - acceptance_window, receiver_now + future_tolerance]. Test the in-window, expired, future and exact-boundary inputs. Signatures have already been verified; this is delivery-timestamp freshness, not original event age.'
# Native workspaces retain their supplied external/runtime boundaries. No simulated
# authentication or publisher verification is substituted for native fixtures.
# Supported FastAPI exercises in the pinned in-process ASGI engine.
c='fastapi.documented_responses';f=fixture(c)
base=load(c,'starter.py').split('with TestClient')[0]
sol=base.replace("@app.post('/orders')", "@app.post('/orders', response_model=PublicModel, status_code="+repr(f['success_status'])+", response_description='Order created', responses={409: {'model': ConflictModel, 'description': 'Order conflicts with an existing order'}})")
probe='''\ndef response_contract(status):
    return app.openapi()['paths']['/orders']['post']['responses'][status]
'''
tests=[]
for label in ['success','conflict']:
 tests.append(('http_equals',{'requests':[{'method':'POST','path':'/orders'+('?conflict=true' if label=='conflict' else '')}], 'expected':{'status':f[label+'_status'],'json':f[label+'_body']}}))
# Expected schema response entries are computed by executing the decorated app locally.
np=B/'working/native_probe.py';np.write_text(sol+probe+"\nimport json\nprint(json.dumps([response_contract('200'),response_contract('409')]))\n")
env=os.environ.copy();env['PYTHONPATH']=os.pathsep.join(str((B/folder).resolve()) for folder in ['working/offline_runtime','working/repair_runtime'])
r=subprocess.run([sys.executable,str(np)],env=env,capture_output=True,text=True,check=True)
for status,exp in zip(['200','409'],json.loads(r.stdout)): tests.append(('function_call',{'function':'response_contract','args':[status],'expected':exp}))
supported[c]=(base+probe,sol+probe,tests,'python_asgi',['fastapi']);tasks[c]='Edit only the POST /orders response declaration. Declare PublicModel, status_code 200, response_description "Order created", and a 409 response using ConflictModel with description "Order conflicts with an existing order". Preserve both outcome branches. The tests compare actual success/conflict status and JSON with fixtures and generated response entries/model references.'
c='fastapi.safe_unexpected_errors';f=fixture(c)
base=load(c,'starter.py').split('with TestClient')[0]
handler='''@app.exception_handler(Exception)
async def unexpected_handler(request: Request, exc: Exception):
    record_safe_failure(request)
    return JSONResponse(status_code=500, content={'detail':'Internal server error'})
'''
# Tests use the supplied capture helper and verify records independently of public output.
probe='''\ndef failure_contract(path):
    safe_records.clear()
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get(path)
    return {'status':response.status_code, 'body':response.json(), 'records':list(safe_records)}
'''
np.write_text(base+handler+probe+"\nimport json\nprint(json.dumps([failure_contract('/controlled-failure'),failure_contract('/not-a-route')]))\n")
r=subprocess.run([sys.executable,str(np)],env=env,capture_output=True,text=True,check=True);exps=json.loads(r.stdout)
tests=[('function_call',{'function':'failure_contract','args':[path],'expected':exp}) for path,exp in zip(['/controlled-failure','/not-a-route'],exps)]
supported[c]=(base+probe,base+handler+probe,tests,'python_asgi',['fastapi']);tasks[c]='Register an Exception handler on the supplied non-debug app. Call record_safe_failure(request), return status 500 with the exact fixtures.json generic public_body, and never return or record exception text. The controlled failure test separately checks public status/body and the safe internal record identifying event, code location and interaction context; the missing-route control must not create such a record.'
c='integration.upstream_failure_translation';f=fixture(c)
base=load(c,'starter.py').split('# TODO: override')[0]
old="    # TODO: raise_for_status and translate HTTPStatusError versus RequestError.\n    return response.json()"
# The await must itself be inside try to catch transport failures.
start=base.index('async def lookup');end=base.index("@app.get('/lookup')")
lookup='''async def lookup(client):
    try:
        response = await client.get(UPSTREAM_URL)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=502, detail='Upstream unavailable') from None
    except httpx.RequestError as exc:
        if isinstance(exc, httpx.TimeoutException):
            raise HTTPException(status_code=504, detail='Upstream timed out') from None
        else:
            raise HTTPException(status_code=502, detail='Upstream unavailable') from None
'''
sol=base[:start]+lookup+base[end:]
probe='''\ndef mapped_failure(condition):
    handler = status_failure if condition == 'upstream_503' else timeout_failure
    async def supplied_client():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            yield client
    original = app.dependency_overrides.copy()
    app.dependency_overrides[client_provider] = supplied_client
    try:
        with TestClient(app) as client:
            response = client.get('/lookup')
        return {'status':response.status_code, 'body':response.json()}
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(original)
'''
tests=[('function_call',{'function':'mapped_failure','args':[condition],'expected':{'status':f[condition]['status'],'body':{'detail':f[condition]['detail']}}}) for condition in ['upstream_503','timeout']]
supported[c]=(base+probe,sol+probe,tests,'python_asgi',['fastapi','httpx']);tasks[c]='Complete lookup with raise_for_status and separate HTTPStatusError and RequestError handling. The supplied contract maps upstream 503 to local 502 {"detail":"Upstream unavailable"}, and timeout to local 504 {"detail":"Upstream timed out"}; use the supplied 502 fallback for other request failures. Do not expose raw upstream details. The readonly test scaffolding makes both actual HTTP requests using supplied MockTransport replacements and exercises the test-only controlled replacement.'
native={}
def n(c,updates,commands,task):
 native[c]={'updates':updates,'commands':commands};tasks[c]=task
c='integration.webhook_authenticity'
code='''from fastapi import HTTPException
import stripe
async def webhook(request, signing_secret, publisher_verifier, signature_header, process_event):
    raw_body = await request.body()
    signature = request.headers.get(signature_header)
    if not signature:
        raise HTTPException(status_code=400, detail='Invalid signature')
    try:
        event = publisher_verifier(raw_body, signature, signing_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        raise HTTPException(status_code=400, detail='Invalid signature') from None
    process_event(event)
    return {'received': True}
'''
test=load(c,'test_delivery.py').replace("        # TODO: http.post('/webhook', content=body, headers=headers).\n        # Assert exact status/body and recorder length (one only for valid).\n        raise NotImplementedError('Complete this delivery test')", "        response = http.post('/webhook', content=body, headers=headers)\n        if condition == 'valid':\n            assert response.status_code == 200\n            assert response.json() == {'received': True}\n            assert len(processed_events) == 1\n        else:\n            assert response.status_code == 400\n            assert response.json() == {'detail': 'Invalid signature'}\n            assert processed_events == []")
n(c,{'starter.py':code,'test_delivery.py':test},['python -m pytest -q test_delivery.py'],'Complete webhook and the three supplied HTTP tests using the actual Stripe SDK verifier: valid raw bytes, modified raw bytes with the same signature, and missing signature. Read raw bytes before parsing, reject verification failures with 400 {"detail":"Invalid signature"} before processing, and return {"received":true} only after verified processing. The stored fixture disables timestamp expiry only for this authenticity lab, not as deployment guidance.')
c='observability.evidence_based_service_diagnosis'
code='''from application import client, packet, runtime_evidence
signals = packet['signals']
records = packet['records']
with client() as http:
    response = http.post('/orders', json=packet['failing_order_payload'])
    controlled_outcome = {'status':response.status_code,
                         'interaction_id':response.headers[packet['interaction_header']],
                         'body':response.json()}
assert controlled_outcome['interaction_id'] == packet['interaction_id']
# Synthetic packet evidence and observed controlled outcome are kept distinct.
comparison = {'baseline':signals[0], 'affected':signals[1]}
first_failure = records[3]
suspected_boundary = first_failure['boundary']
supporting_evidence = {'input':records[0], 'database':records[1],
                       'outbound_start':records[2], 'first_failure':first_failure,
                       'final_response':records[4],
                       'controlled_runtime':runtime_evidence}
proposed_change = None  # A proposed intervention is not an observation.
'''
check='''import starter as s
from application import packet
assert s.controlled_outcome['status'] == 504
assert s.controlled_outcome['body'] == {'detail':'Lookup timeout'}
assert s.comparison['baseline']['request_count'] == s.comparison['affected']['request_count']
assert s.comparison['baseline']['window_seconds'] == s.comparison['affected']['window_seconds']
assert s.comparison['affected']['failure_count'] > s.comparison['baseline']['failure_count']
assert s.comparison['affected']['latency_ms'] > s.comparison['baseline']['latency_ms']
assert s.first_failure['event'] == 'timeout'
assert s.suspected_boundary == 'outbound'
assert s.supporting_evidence['database']['event'] == 'lookup_complete'
assert s.supporting_evidence['database']['sql_statement_count'] == 1
assert s.supporting_evidence['input']['event'] == 'request_received'
assert s.proposed_change is None
'''
n(c,{'starter.py':code,'check_diagnosis.py':check},['python check_diagnosis.py'],'Execute exactly one supplied POST /orders. Record status, JSON, interaction identifier and controlled runtime_evidence, separately from authored signals and records. Populate comparison with baseline/affected signals; identify the first recorded failure, suspected_boundary and supporting_evidence from local input, database completion and outbound timing. Distinguish unchanged traffic from increased failures/latency. Keep proposed_change None; do not present the injected timeout or simulated database lookup as real measured latency or emitted SQL.')
c='security.bounded_api_resources';f=fixture(c);bud=f['hypothetical_budgets']
code=load(c,'starter.py').replace("order_ids: list[int]  # TODO: Field(max_length=3), from supplied budget", "order_ids: list[int] = Field(max_length="+str(bud['batch_size'])+")")
app=load(c,'application.py').replace("httpx.Timeout(None)","httpx.Timeout(budgets['dependency_timeout_seconds'])").replace("app = FastAPI()", "app = FastAPI()\napp.add_middleware(RequestBodyLimitMiddleware, max_body_size=budgets['body_bytes'])")
test=load(c,'test_boundaries.py').replace("            # TODO: assert exact accepted contract or independent byte/batch\n            # rejection, plus counted invocation for accepted requests only.", "            if condition in ('within_batch', 'within_body'):\n                assert response.status_code == 200\n                assert response.json() == {'accepted': len(fixtures[condition]['order_ids'])}\n                assert calls == [True]\n            else:\n                assert response.status_code == (413 if condition == 'beyond_body' else 422)\n                assert calls == []")
configcheck="from application import outbound_timeout, budgets\nassert outbound_timeout.connect == budgets['dependency_timeout_seconds']\nassert outbound_timeout.read == budgets['dependency_timeout_seconds']\nfrom pathlib import Path\nassert '--limit-concurrency '+str(budgets['limit_concurrency']) in Path('launch.sh').read_text()\n"
launch="#!/usr/bin/env bash\nexec uvicorn application:app --host 127.0.0.1 --port 8000 --limit-concurrency "+str(bud['limit_concurrency'])+"\n"
n(c,{'starter.py':code,'application.py':app,'test_boundaries.py':test,'launch.sh':launch,'check_config.py':configcheck},['python install_middleware.py','python check_config.py','python -m pytest -q test_boundaries.py'],'Complete BatchInput max_length, supplied maintained actual-body-byte middleware, finite HTTPX timeout and launch.sh --limit-concurrency from hypothetical_budgets. Complete four HTTP checks: valid inputs retain accepted-count JSON; oversized body and oversized batch reject with zero expensive dependency calls. Verify the timeout and launcher budgets independently; do not trust Content-Length as actual body size.')
c='sqlalchemy.redundant_queries'
code=load(c,'starter.py').replace('    # TODO: statement.options(selectinload(Entity.relationship_attribute))','    statement = statement.options(selectinload(Entity.relationship_attribute))')
check='''import io, logging
from sqlalchemy import select
from sqlalchemy.orm import Session
from starter import engine, Entity, listing
stream=io.StringIO()
handler=logging.StreamHandler(stream)
logger=logging.getLogger('sqlalchemy.engine.Engine');logger.addHandler(handler)
def baseline(session):
    parents=session.execute(select(Entity).order_by(Entity.id).limit(3)).scalars().all()
    return [{'id':p.id,'children':[c.id for c in p.relationship_attribute]} for p in parents]
with Session(engine) as session:
    before=baseline(session)
before_sql=stream.getvalue();stream.seek(0);stream.truncate(0)
with Session(engine) as session:
    after=listing(session)
after_sql=stream.getvalue()
logger.removeHandler(handler)
assert before == after
# Count actual SELECT statements in each separately captured echo stream.
assert after_sql.count('SELECT ') < before_sql.count('SELECT ')
'''
n(c,{'starter.py':code,'check_listing.py':check},['python check_listing.py'],'Add exactly statement.options(selectinload(Entity.relationship_attribute)) to the supplied listing. The supplied check runs baseline and changed listings in separate fresh sessions with echo logging, requires fewer SELECTs, and requires equal parent identities and collection contents. Do not drop parents, change cardinality or reuse warm relationships to claim query reduction.')
c='testing.database_state_isolation'
code=load(c,'starter.py').replace('@pytest.fixture','@pytest.fixture(scope="function")').replace('    test_session = None','    test_session = Session(bind=connection, join_transaction_mode="create_savepoint")').replace('    # TODO: override session_provider with a yield provider using test_session.', '    def provider():\n        yield test_session\n    app.dependency_overrides[session_provider] = provider').replace('        pass','        try:\n            test_session.close()\n        finally:\n            try:\n                outer_transaction.rollback()\n            finally:\n                connection.close()\n                app.dependency_overrides.clear()\n                app.dependency_overrides.update(original_overrides)')
test=load(c,'test_items.py');start=test.index('# Initially sharing');end=test.index('def test_writes_item');test=test[:start]+'from starter import isolated_client\n'+test[end:]
n(c,{'starter.py':code,'test_items.py':test},['python run_orders.py','python check_failure_cleanup.py'],'Complete function-scoped isolated_client with a connection-bound Session(join_transaction_mode="create_savepoint") and yield dependency override. Guarantee finally closes the session, rolls back the outer transaction, closes the connection and restores previous overrides even on failure. Replace the shared fixture in test_items.py with this fixture; run both supplied execution orders and injected-failure cleanup. Keep schema initialization outside per-test transactions.')
c='auth.authorization_server_integration'
code=load(c,'starter.py').replace('    client_configuration = None', "    client_configuration = {'client_id':issuer_configuration['client_id'],\n        'authorization_url':issuer_configuration['authorization_url'],\n        'token_url':issuer_configuration['token_url'],\n        'redirect_uri':issuer_configuration['redirect_uri'],\n        'scopes':issuer_configuration['scopes'], 'pkce':issuer_configuration['pkce']}").replace('    trust_configuration = None',"    trust_configuration = {'jwks_url':issuer_configuration['jwks_url'],\n        'issuer':issuer_configuration['issuer'], 'algorithms':issuer_configuration['algorithms'],\n        'required_claims':issuer_configuration['required_claims'], 'audience':issuer_configuration['audience']}")
test=load(c,'test_integration.py').replace("        raise NotImplementedError('Complete HTTP assertions')", "        assert accepted.status_code == 200\n        assert rejected.status_code == 401\n        # Acquire from the actual issuer again with its supplied alternate API audience.\n        wrong_configuration = configuration.copy()\n        wrong_configuration['scopes'] = {'other:api': 'Controlled wrong audience'}\n        from acquisition_harness import AcquisitionHarness\n        wrong_token = AcquisitionHarness(wrong_configuration).acquire()\n        wrong = client.get('/protected', headers={'Authorization':'Bearer '+wrong_token})\n        assert wrong.status_code == 401")
# The alternate audience must be the issuer's actual supported contract, not invented.
issuer=load(c,'issuer_service.py')
# Record the supported wrong-audience scope only when the supplied server states it.
if 'other:api' not in issuer:
 test=test.replace("{'other:api': 'Controlled wrong audience'}", "{'other-api': 'Controlled wrong audience'}")
n(c,{'starter.py':code,'test_integration.py':test},['python -m pytest -q test_integration.py'],'Configure AcquisitionHarness and ExistingVerifier only from issuer_configuration.json. Obtain an actual access token through the supplied separate authorization-code server and registered PKCE client. Complete real endpoint checks for issuer-token acceptance, signature-tampered rejection and a separately issuer-issued wrong-audience token. Keep extraction/verifier active; do not fabricate valid tokens locally or override authentication. The native issuer must be running at the supplied loopback configuration.')
c='auth.endpoint_permissions'
code=load(c,'starter.py').replace("    raise NotImplementedError('Complete permission comparison')", "    for required_scope in security_scopes.scopes:\n        if required_scope not in verified_context['scopes']:\n            raise HTTPException(status_code=403, detail='Forbidden')\n    return verified_context")
app=load(c,'application.py');print('permission app',app,file=sys.stderr)
# Replace only existing unfinished operation dependency.
app=app.replace('from fastapi import FastAPI, Depends','from fastapi import FastAPI, Depends, Security').replace('Depends(require_permissions)',"Security(require_permissions, scopes=['orders:write'])")
if 'Security(require_permissions' not in app: app=app.replace('principal=None',"principal=Security(require_permissions, scopes=['orders:write'])")
test=load(c,'test_permissions.py');print('permission test',test,file=sys.stderr)
test=test.replace("        raise NotImplementedError('Complete HTTP assertions')", "        assert response.status_code == case['expected_status']")
n(c,{'starter.py':code,'application.py':app,'test_permissions.py':test},['python prepare_credentials.py','python -m pytest -q test_permissions.py'],'Complete the SecurityScopes provider by requiring every declared scope on the verified token context. Wire the operation using Security(require_permissions, scopes=["orders:write"]). Preserve real verification. Complete the two supplied signed-token HTTP tests to show success only with orders:write and exact declared denial without it.')
# The supplied issuer has one audience and no alternate-audience acquisition
# contract. Exercise the success anchor's tampered-token alternative instead.
c='auth.authorization_server_integration'
t=native[c]['updates']['test_integration.py'];t=t[:t.index('        # Acquire from the actual issuer again')]
native[c]['updates']['test_integration.py']=t
tasks[c]=tasks[c].replace('and a separately issuer-issued wrong-audience token','using the tampered-token rejection alternative in the success criterion')
c='auth.endpoint_permissions'
app=load(c,'application.py').replace('context=Depends(verified_token_context)',"context=Security(require_permissions, scopes=['orders:write'])")
test=load(c,'test_permissions.py').replace('        # TODO: assert 200/public result for sufficiently scoped context;\n        # separately 403 {"detail":"Forbidden"} and unchanged order for no scope.', "        if condition == 'verified_with_permission':\n            assert response.status_code == 200\n            assert response.json() == {'id': fixtures['order']['id'], 'status': fixtures['modification']['status']}\n        else:\n            assert response.status_code == 403\n            assert response.json() == {'detail':'Forbidden'}\n            assert order == {key:fixtures['order'][key] for key in ['id','status']}")
native[c]['updates']['application.py']=app;native[c]['updates']['test_permissions.py']=test
c='fastapi_backend.webhook_delivery_idempotency'
base=load(c,'starter.py');i=base.index('async def handle_authenticated_event')
code=base[:i]+'''async def handle_authenticated_event(event, session):
    event_id = event['publisher_event_id']
    try:
        async with session.begin():
            existing = await session.scalar(select(ProcessedEvent).where(ProcessedEvent.publisher_event_id == event_id))
            if existing is not None:
                return {'received': True}
            session.add(ProcessedEvent(publisher_event_id=event_id))
            await session.flush()
            order = await session.scalar(select(Order).where(Order.id == event['order_id']))
            if order is None:
                raise ValueError('Unknown controlled order')
            order.status = event['new_status']
        return {'received': True}
    except IntegrityError:
        # The failed transaction has rolled back. Confirm the persistent
        # identity rather than treating unrelated constraint errors as success.
        existing = await session.scalar(select(ProcessedEvent).where(ProcessedEvent.publisher_event_id == event_id))
        if existing is not None:
            return {'received': True}
        raise
'''
f=fixture(c);print('delivery fixtures',f,file=sys.stderr)
# Match the event's actual supplied field names, never invent schema fields.
if f.get('authenticated_events'):
 ev=f['authenticated_events'][0]
 if 'status' in ev and 'new_status' not in ev: code=code.replace("event['new_status']","event['status']")
test=load(c,'delivery_checks.py').replace('            # TODO: assert successful acknowledgements, one event identity and\n            # one intended state update; failure response must retain before.', "            if name == 'failure':\n                assert responses[0].status_code == 500\n                assert after == before\n            else:\n                assert all(r.status_code == 200 and r.json() == {'received': True} for r in responses)\n                assert after['events'] == [event['publisher_event_id']]\n                expected_orders = [dict(row) for row in before['orders']]\n                for row in expected_orders:\n                    if row['id'] == event['order_id']:\n                        row['status'] = event.get('new_status', event.get('status'))\n                assert after['orders'] == expected_orders").replace('                # TODO: retained and final equal after, duplicate acknowledged.', "                assert retained == after\n                assert final == after\n                assert response.status_code == 200\n                assert response.json() == {'received': True}")
n(c,{'starter.py':code,'delivery_checks.py':test},['python run_sequential.py','python run_restart.py','python run_concurrent.py','python run_failure.py'],'Complete persistent event-id deduplication and order update in one transaction, with a unique publisher_event_id record. Acknowledge only a confirmed processed duplicate; do not swallow unrelated IntegrityError. Complete the supplied sequential, restart, concurrent and injected-failure checks: one committed event/order change, successful duplicate acknowledgment, and complete rollback on failure. Authenticity is already established before this exercise; keep durable storage across restarts.')
c='integration.bounded_idempotent_retries';f=fixture(c)
# Classifications below are the controlled failures the supplied adapter/tests use.
limits=f['hypothetical_limits']
policy={'retryable_failures':['connect_timeout','read_timeout','http_503','http_429'],'max_attempts':limits['max_attempts'],'total_time_budget':limits['total_time_budget_seconds'],'retry_after':True,'bounded_backoff':limits['max_backoff_seconds'],'retry_safe':True}
code=load(c,'starter.py');i=code.index('policy =');code=code[:i]+'policy = '+repr(policy)+'\n'
n(c,{'starter.py':code},['python run_transient.py','python run_delays.py','python run_exhaustion.py','python run_unsafe_post.py'],'Fill the supplied policy dictionary for the maintained Tenacity adapter using the hypothetical_limits. Permit the supplied transient classifications (connect_timeout, read_timeout, http_503, http_429), enable Retry-After and contract-based retry-safety, and set finite attempts, total time and client backoff. Run all four supplied checks, including delay-seconds/HTTP-date Retry-After, oversized server delay, elapsed-time exhaustion, terminal failure and unsafe POST. A lost response is not proof of no remote effect.')
c='auth.object_authorization'
code=load(c,'starter.py').replace('select(Order).where(Order.id == order_id)','select(Order).where(Order.id == order_id, Order.owner_id == principal.owner_id)')
test=load(c,'test_ownership.py').replace('            # TODO: both own successes and both cross-owner unavailable results.\n            # Read the database through client.portal.call(snapshot) and assert\n            # every id, owner_id and status equals fixtures[\'orders\'].', "            rows = client.portal.call(snapshot)\n            assert rows == fixtures['orders']\n            expected = [row for row in rows if row['id'] == order_id and row['owner_id'] == caller]\n            if expected:\n                assert response.status_code == 200\n                assert response.json() == {key:expected[0][key] for key in ['id','status']}\n            else:\n                assert response.status_code == fixtures['unavailable_object']['status']\n                assert response.json() == fixtures['unavailable_object']['body']\n            spoofed = client.get(f'/orders/{order_id}', params={'owner_id': 'caller_b' if caller == 'caller_a' else 'caller_a'})\n            assert spoofed.status_code == response.status_code\n            assert spoofed.json() == response.json()\n            assert client.portal.call(snapshot) == fixtures['orders']")
print('object fixtures',fixture(c),file=sys.stderr)
n(c,{'starter.py':code,'test_ownership.py':test},['python -m pytest -q test_ownership.py'],'Bind order identity and owner identity in the SQLAlchemy predicate using only trusted principal.owner_id. Complete all four supplied HTTP principal/order pairs: both own-object successes and both cross-owner unavailable contracts with no order data. Also show caller-controlled owner_id cannot override trusted identity and database rows remain unchanged. Trusted-principal overrides are only for this object-boundary lab, not proof of authentication.')
c='fastapi.production_security_documentation'
code='''from fastapi import Depends, Security
from fastapi.security import HTTPBearer, OAuth2AuthorizationCodeBearer
bearer_scheme = HTTPBearer(auto_error=False, scheme_name='OrderBearer')
def authorization_code_scheme(issuer_configuration):
    return OAuth2AuthorizationCodeBearer(
        authorizationUrl=issuer_configuration['authorization_url'],
        tokenUrl=issuer_configuration['token_url'], scopes=issuer_configuration['scopes'],
        scheme_name='OrderAuthorizationCode', auto_error=False)
'''
app=load(c,'application.py').replace('from fastapi import FastAPI, Depends','from fastapi import FastAPI, Depends, Security').replace('app=FastAPI()',"from starter import bearer_scheme, authorization_code_scheme\nfrom dependencies import configuration\ncode_scheme=authorization_code_scheme(configuration)\napp=FastAPI(description='Acquire access using the supplied authorization-code issuer and registered client with S256 PKCE. Present the access token as Bearer; this API does not provide a password grant.')")
app=app.replace("@app.get('/orders/{order_id}')", "@app.get('/orders/{order_id}', dependencies=[Security(bearer_scheme), Security(code_scheme, scopes=['orders:read'])])").replace("@app.post('/orders',status_code=201)","@app.post('/orders',status_code=201, dependencies=[Security(bearer_scheme), Security(code_scheme, scopes=['orders:write'])])")
check='''from application import app
from dependencies import configuration
schema=app.openapi()
schemes=schema['components']['securitySchemes']
assert schemes['OrderBearer']['type'] == 'http'
assert schemes['OrderBearer']['scheme'] == 'bearer'
flow=schemes['OrderAuthorizationCode']['flows']['authorizationCode']
assert flow['authorizationUrl'] == configuration['authorization_url']
assert flow['tokenUrl'] == configuration['token_url']
assert flow['scopes'] == configuration['scopes']
assert 'password' not in schemes['OrderAuthorizationCode']['flows']
for path,method,scope in [('/orders/{order_id}','get','orders:read'),('/orders','post','orders:write')]:
    requirements=schema['paths'][path][method]['security']
    assert {'OrderAuthorizationCode':[scope]} in requirements
    assert {'OrderBearer':[]} in requirements
assert 'S256 PKCE' in schema['info']['description']
'''
n(c,{'starter.py':code,'application.py':app,'check_declarations.py':check,'ACQUISITION.md':'Use the supplied issuer_configuration.json authorization_url and token_url with its registered client_id and redirect_uri. Obtain authorization code with the S256 PKCE challenge; exchange the code using the matching verifier. Present the resulting access token as Bearer. This resource API does not offer a password grant.\n'},['python check_declarations.py'],'Declare OrderBearer for presentation and OrderAuthorizationCode from supplied actual URLs/scopes. Add Security requirements for orders:read/write beside unchanged read_orders/write_orders enforcement. Include authorization-code and S256 PKCE guidance without a password grant. Compare generated schemes and operation requirements against configuration and existing dependency graph; documentation must not replace verification or permission checks.')
c='fastapi.openapi_contract_inspection'
code='''import json
from pathlib import Path
expected_models = json.loads(Path('expected_models.json').read_text())
def audit(client, models, http_evidence, security_configuration):
    response = client.get('/openapi.json')
    assert response.status_code == 200
    schema = response.json()
    findings = []
    paths = schema['paths']
    components = schema['components']['schemas']
    # Inventory and model comparison cover requiredness, types, constraints,
    # request/response schemas and public output fields separately from statuses.
    for name in expected_models:
        if components.get(name) != expected_models[name]:
            findings.append({'dimension':'model_schema', 'location':name, 'declared':components.get(name), 'expected':expected_models[name]})
    for record in http_evidence['records']:
        request = record['request']
        path = request['path']
        method = request['method']
        operation_path = path
        if method == 'GET':
            operation_path = '/orders/{order_id}'
        operation = paths.get(operation_path, {}).get(method.lower())
        if operation is None:
            findings.append({'dimension':'paths','location':method+' '+operation_path})
        else:
            status = str(record['status'])
            if status not in operation['responses']:
                findings.append({'dimension':'observed_status','location':method+' '+operation_path,'observed':record['status'],'declared':list(operation['responses'])})
            if method == 'GET':
                parameters = operation.get('parameters', [])
                if not parameters:
                    findings.append({'dimension':'parameters','location':operation_path})
                for parameter in parameters:
                    if parameter['name'] == 'order_id':
                        if parameter.get('required') != True or parameter.get('schema',{}).get('type') != 'integer':
                            findings.append({'dimension':'parameter_contract','location':operation_path})
            if method == 'POST':
                request_schema=operation['requestBody']['content']['application/json']['schema']
                if request_schema.get('$ref') != '#/components/schemas/OrderInput':
                    findings.append({'dimension':'request_schema','location':operation_path})
            if record['status'] in [200,201]:
                models['PublicOrder'].model_validate(record['body'])
                if 'owner_id' in record['body']:
                    findings.append({'dimension':'sensitive_output','location':operation_path})
                result_schema=operation['responses'][status]['content']['application/json']['schema']
                if result_schema.get('$ref') != '#/components/schemas/PublicOrder':
                    findings.append({'dimension':'response_schema','location':operation_path})
    # The supplied public examples are synthetic and must validate; never copy
    # realistic personal data into documentation to make examples convincing.
    for name in ['OrderInput','PublicOrder','ErrorBody']:
        for example in components.get(name,{}).get('examples',[]):
            models[name].model_validate(example)
            for prohibited in ['owner_id','password','access_token','secret','email']:
                if prohibited in example:
                    findings.append({'dimension':'sensitive_example','location':name,'field':prohibited})
    for path in paths:
        for method in paths[path]:
            operation=paths[path][method]
            for text in [operation.get('description',''), operation.get('summary','')]:
                for prohibited in ['access_token=','password=','secret=','@example.com']:
                    if prohibited in text:
                        findings.append({'dimension':'sensitive_description','location':method+' '+path})
    schemes=schema['components'].get('securitySchemes',{})
    for name in security_configuration['schemes']:
        if schemes.get(name) != security_configuration['schemes'][name]:
            findings.append({'dimension':'security_scheme','location':name,'declared':schemes.get(name),'expected':security_configuration['schemes'][name]})
    for location in security_configuration['operations']:
        method,path=location.split(' ')
        declared=paths[path][method.lower()].get('security',[])
        if declared != security_configuration['operations'][location]:
            findings.append({'dimension':'operation_security','location':location,'declared':declared,'expected':security_configuration['operations'][location]})
    return findings
'''
# Model schema values are computed from supplied model definitions, never typed.
np.write_text(load(c,'models.py')+"\nimport json\nprint(json.dumps({name:model.model_json_schema() for name,model in [('OrderInput',OrderInput),('PublicOrder',PublicOrder),('ErrorBody',ErrorBody)]}))\n")
r=subprocess.run([sys.executable,str(np)],env=env,capture_output=True,text=True,check=True)
check='''import json
from pathlib import Path
from fastapi.testclient import TestClient
from application import app, security_configuration
from models import OrderInput, PublicOrder, ErrorBody
from starter import audit
with TestClient(app) as client:
    findings=audit(client, {'OrderInput':OrderInput,'PublicOrder':PublicOrder,'ErrorBody':ErrorBody},json.loads(Path('http_evidence.json').read_text()),security_configuration)
assert any(f['dimension']=='observed_status' and f['observed']==400 for f in findings)
assert any(f['dimension']=='security_scheme' and f['location']=='OrderAuthorizationCode' for f in findings)
assert any(f['dimension']=='operation_security' for f in findings)
'''
n(c,{'starter.py':code,'expected_models.json':r.stdout,'check_audit.py':check},['python check_audit.py'],'Complete audit of the supplied orders router: retrieve /openapi.json; cover paths/parameters, requiredness/types/constraints, request/response schemas and output fields against model schemas and captured non-auth HTTP evidence. Compare documented statuses with observed outcomes, validate synthetic examples and review examples/descriptions for sensitive data. Compare security schemes/requirements with supplied established configuration. Return findings with dimension/location and declared/observed or expected evidence; do not add authentication tests or claim a declaration proves execution.')
c='testing.api_authentication_authorization'
code=load(c,'starter.py').replace("        # TODO: send bearer_fixtures[case['credential_condition']] as headers\n        # to GET /orders/{requested_order_id}; assert exact declared_status and\n        # json.loads(case['safe_body_or_public_result']). No dependency overrides.\n        pass", "        response = client.get(f\"/orders/{case['requested_order_id']}\", headers=bearer_fixtures[case['credential_condition']])\n        assert response.status_code == case['declared_status']\n        assert response.json() == json.loads(case['safe_body_or_public_result'])")
n(c,{'starter.py':code},['python prepare_credentials.py','python -m pytest -q starter.py'],'Complete the parametrized real HTTP test for every supplied credential/ownership matrix row. Preserve bearer extraction, JWT verification, permission and object gates. Send the supplied headers to GET /orders/{requested_order_id}, assert exact declared_status and parsed safe_body_or_public_result. Keep separate absent, malformed, bad-signature, expired, wrong-context, missing-permission, cross-owner and fully authorized cases; do not override authentication or require internal owner fields in the public result.')
# Runner-compatible, readonly testing scaffolds and precise allowed learner edits.
c='deployment.release_rollback_boundaries';f=fixture(c);prior=f['releases'][1]
pre='prior_artifact = '+repr(prior['artifact'])+'\nprior_configuration = '+repr(prior['configuration'])+'\nprior_id = '+repr(prior['release_id'])+'\ncurrent_schema = '+repr(f['current_database_schema'])+'\n'
pre+='releases = '+repr(f['releases'])+'\nprior_release = {"release_id":prior_id, "artifact":prior_artifact, "configuration":prior_configuration, "schema_compatible":True}\n'
pre+='def rollback_procedure(record):\n    if record is None:\n        return {}\n    return {"build": record["artifact"], "release": {"artifact":record["artifact"], "configuration":record["configuration"]}, "run":record["release_id"], "database_schema_after_rollback":current_schema}\n'
starter=pre+'selected_release = None\nprocedure = rollback_procedure(selected_release)\n';sol=starter.replace('selected_release = None','selected_release = prior_release')
ns={};exec(sol,ns)
supported[c]=(starter,sol,[('value_equals',{'expr':'procedure','expected':ns['procedure']}),('value_equals',{'expr':'selected_release','expected':ns['selected_release']})],'python',[])
tasks[c]='Set selected_release to the supplied compatible prior_release. The readonly rollback_procedure computes the build artifact, release artifact/configuration, unique run identity and unchanged current schema. Check each phase against the immutable supplied release records. Application rollback does not reverse database schema changes.'
c='fastapi_backend.webhook_replay_freshness'
start,sol,tests,kind,pkgs=supported[c]
start='def delivery_is_fresh(signed_delivery_timestamp, receiver_now, acceptance_window, future_tolerance):\n    age = receiver_now - signed_delivery_timestamp\n    return False\n'
sol='def delivery_is_fresh(signed_delivery_timestamp, receiver_now, acceptance_window, future_tolerance):\n    age = receiver_now - signed_delivery_timestamp\n    return -future_tolerance <= age <= acceptance_window\n'
supported[c]=(start,sol,tests,kind,pkgs)
c='fastapi.safe_unexpected_errors'
start,sol,tests,kind,pkgs=supported[c]
start=start[:start.index('def failure_contract')];sol=sol[:sol.index('def failure_contract')]
readonly='@app.get("/__test_records")\nasync def test_records():\n    return safe_records\n'
start+=readonly;sol+=readonly
# Expected safe internal records were captured by the supplied native helper above.
tests=[('http_equals',{'requests':[{'method':'GET','path':'/controlled-failure'},{'method':'GET','path':'/__test_records'}], 'expected':[{'status':exps[0]['status'],'json':exps[0]['body']},{'status':200,'json':exps[0]['records']}]}),('http_equals',{'requests':[{'method':'GET','path':'/not-a-route'},{'method':'GET','path':'/__test_records'}], 'expected':[{'status':exps[1]['status'],'json':exps[1]['body']},{'status':200,'json':exps[1]['records']}]})]
supported[c]=(start,sol,tests,kind,pkgs)
tasks[c]+=' The readonly /__test_records route exists only to expose the supplied test recorder to this in-process test harness, not as a public deployment route.'
c='integration.upstream_failure_translation'
start,sol,tests,kind,pkgs=supported[c]
start=start[:start.index('def mapped_failure')];sol=sol[:sol.index('def mapped_failure')]
readonly='from fastapi import Request\nasync def controlled_client(request: Request):\n    handler = status_failure if request.headers.get("X-Fixture") == "upstream_503" else timeout_failure\n    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:\n        yield client\napp.dependency_overrides[client_provider] = controlled_client\n'
start+=readonly;sol+=readonly
f=fixture(c)
tests=[('http_equals',{'requests':[{'method':'GET','path':'/lookup','headers':{'X-Fixture':condition}}], 'expected':{'status':f[condition]['status'],'json':{'detail':f[condition]['detail']}}}) for condition in ['upstream_503','timeout']]
supported[c]=(start,sol,tests,kind,pkgs)

# Provide unsupported helper syntax as unchanged readonly execution scaffolding.
# The learner edits only a release selection or the finite comparison predicate.
c='deployment.release_rollback_boundaries'
start,sol,tests,kind,pkgs=supported[c]
helper=start[start.index('def rollback_procedure'):start.index('selected_release =')]
start=start.replace(helper,'exec('+repr(helper)+')\n');sol=sol.replace(helper,'exec('+repr(helper)+')\n')
supported[c]=(start,sol,tests,kind,pkgs)
c='fastapi_backend.webhook_replay_freshness'
start,sol,tests,kind,pkgs=supported[c]
helper='exec('+repr('def delivery_age(signed_delivery_timestamp, receiver_now):\n    return receiver_now - signed_delivery_timestamp\n')+')\n'
start=helper+start.replace('age = receiver_now - signed_delivery_timestamp','age = delivery_age(signed_delivery_timestamp, receiver_now)')
sol=helper+sol.replace('age = receiver_now - signed_delivery_timestamp','age = delivery_age(signed_delivery_timestamp, receiver_now)')
supported[c]=(start,sol,tests,kind,pkgs)
tasks[c]+=' Use the unchanged delivery_age helper for the supplied receiver-time subtraction; edit only the finite comparison return.'
c='fastapi.safe_unexpected_errors'
start,sol,tests,kind,pkgs=supported[c]
tests=[('http_equals',{'requests':[{'method':'GET','path':'/controlled-failure'}],'expected':{'status':exps[0]['status'],'json':exps[0]['body']}}),('http_equals',{'requests':[{'method':'GET','path':'/controlled-failure'},{'method':'GET','path':'/__test_records'}],'expected':{'status':200,'json':exps[0]['records']}}),('http_equals',{'requests':[{'method':'GET','path':'/not-a-route'}],'expected':{'status':exps[1]['status'],'json':exps[1]['body']}}),('http_equals',{'requests':[{'method':'GET','path':'/not-a-route'},{'method':'GET','path':'/__test_records'}],'expected':{'status':200,'json':exps[1]['records']}})]
supported[c]=(start,sol,tests,kind,pkgs)

c='fastapi_backend.webhook_replay_freshness'
start='def delivery_is_fresh(age, acceptance_window, future_tolerance):\n    # age is receiver_now minus authenticated delivery timestamp, in seconds.\n    return False\n'
sol='def delivery_is_fresh(age, acceptance_window, future_tolerance):\n    return -future_tolerance <= age <= acceptance_window\n'
ns={};exec(sol,ns);tests=[]
for case in fixture(c)['cases']:
    args=[int(case['receiver_now'])-int(case['signed_delivery_timestamp']),int(case['acceptance_window']),int(case['future_tolerance'])]
    tests.append(('function_call',{'function':'delivery_is_fresh','args':args,'expected':ns['delivery_is_fresh'](*args)}))
supported[c]=(start,sol,tests,'python',[])
tasks[c]='Complete delivery_is_fresh(age, acceptance_window, future_tolerance), returning a boolean for inclusive freshness bounds. The readonly scenario preparation supplies age = receiver_now minus the authenticated delivery timestamp, in integer seconds; positive age is past, negative age is future. Accept no older than acceptance_window and no farther in the future than future_tolerance. The fixture-derived tests cover in-window, expired, future and exact boundaries after valid signature verification. This finite-comparison edit does not ask you to implement signature verification or a clock source.'
c='fastapi.safe_unexpected_errors'
start,sol,tests,kind,pkgs=supported[c]
readonly='@app.get("/__test_records")\nasync def test_records():\n    return safe_records\n'
start=start.replace(readonly,'exec('+repr(readonly)+')\n');sol=sol.replace(readonly,'exec('+repr(readonly)+')\n')
old="def controlled_failure():\n    raise RuntimeError('Controlled internal failure; never disclose this string')"
new="def controlled_failure(fail: bool = True):\n    if not fail:\n        return {'ok': True}\n    raise RuntimeError('Controlled internal failure; never disclose this string')"
start=start.replace(old,new);sol=sol.replace(old,new)
# Observe the new control and error contracts natively before writing expectations.
np.write_text(sol+"\nimport json\nwith TestClient(app,raise_server_exceptions=False) as client:\n    first=client.get('/controlled-failure')\n    a={'status':first.status_code,'json':first.json()}\n    records=list(safe_records)\n    second=client.get('/controlled-failure',params={'fail':False})\n    b={'status':second.status_code,'json':second.json()}\nprint(json.dumps([a,b,records]))\n")
r=subprocess.run([sys.executable,str(np)],env=env,capture_output=True,text=True,check=True)
a,b,records=json.loads(r.stdout)
tests=[('http_equals',{'requests':[{'method':'GET','path':'/controlled-failure'}],'expected':a}),('http_equals',{'requests':[{'method':'GET','path':'/controlled-failure','params':{'fail':False}}],'expected':b}),('http_equals',{'requests':[{'method':'GET','path':'/controlled-failure'},{'method':'GET','path':'/__test_records'}],'expected':{'status':200,'json':records}}),('http_equals',{'requests':[{'method':'GET','path':'/controlled-failure','params':{'fail':False}},{'method':'GET','path':'/__test_records'}],'expected':{'status':200,'json':[]}})]
supported[c]=(start,sol,tests,kind,pkgs)

# A native SQLAlchemy collection-loading exercise also fits the pinned ASGI
# engine without sockets or async drivers; its baseline remains actual SQL.
c='sqlalchemy.redundant_queries'
model_code=load(c,'starter.py').split('def listing(session):')[0]
helper="""
import io, logging
from sqlalchemy import select
from sqlalchemy.orm import Session

def audit_listing(take):
    stream=io.StringIO()
    handler=logging.StreamHandler(stream)
    logger=logging.getLogger('sqlalchemy.engine.Engine')
    logger.addHandler(handler)
    with Session(engine) as session:
        parents=session.execute(select(Entity).order_by(Entity.id).limit(take)).scalars().all()
        before=[{'id':p.id,'children':[child.id for child in p.relationship_attribute]} for p in parents]
    before_sql=stream.getvalue();stream.seek(0);stream.truncate(0)
    with Session(engine) as session:
        parents=session.execute(statement.order_by(Entity.id).limit(take)).scalars().all()
        after=[{'id':p.id,'children':[child.id for child in p.relationship_attribute]} for p in parents]
    after_sql=stream.getvalue()
    logger.removeHandler(handler)
    return {'before':before,'after':after,'before_selects':before_sql.count('SELECT '),'after_selects':after_sql.count('SELECT ')}
"""
start='exec('+repr(model_code)+')\nstatement = select(Entity)\nexec('+repr(helper)+')\n'
sol=start.replace('statement = select(Entity)','statement = select(Entity).options(selectinload(Entity.relationship_attribute))')
np.write_text(sol+"\nimport json\nprint('RESULT='+json.dumps([audit_listing(2),audit_listing(3)]))\n")
r=subprocess.run([sys.executable,str(np)],env=env,capture_output=True,text=True,check=True)
expected=json.loads(r.stdout.split('RESULT=')[-1])
for item in expected:
    assert item['before']==item['after']
    assert item['after_selects']<item['before_selects']
tests=[('function_call',{'function':'audit_listing','args':[take],'expected':value}) for take,value in zip([2,3],expected)]
supported[c]=(start,sol,tests,'python_asgi',[])
tasks[c]='Edit statement to use statement.options(selectinload(Entity.relationship_attribute)) for collection loading, without changing the entities or filtering parents. The readonly audit_listing runs baseline and changed listing in separate fresh sessions for two- and three-parent pages, captures actual SQL echo and returns before/after public id-and-children records plus before_selects/after_selects. Tests require exact parent/collection equivalence and fewer emitted SELECT statements for both page sizes. Do not claim lower counts from warm relationships or changed cardinality.'
native.pop(c)

# Build deterministic interactions and native runnable workspaces. Native Bash is
# explicitly UNVERIFIED by this pack: these dependencies/services cannot be
# replaced by invented pure-Python proxies merely to obtain a green sandbox gate.
bash_version=subprocess.run(['bash','--version'],capture_output=True,text=True,check=True).stdout.splitlines()[0]
def fileobj(path,content,role='readonly'):
 return {'path':path,'content':content,'role':role,'language':('python' if path.endswith('.py') else 'bash' if path.endswith('.sh') else 'json' if path.endswith('.json') else 'text')}
def shell_entry(updates,commands):
 out='#!/usr/bin/env bash\nset -euo pipefail\n# Requires the supplied native workspace dependencies and any provisioned service.\n'
 for index,(path,content) in enumerate(updates.items()):
  delimiter='DEVSPACE_FILE_'+str(index)
  out+='cat > '+repr(path)+' <<\''+delimiter+'\'\n'+content.rstrip()+'\n'+delimiter+'\n'
 for command in commands: out+=command+'\n'
 return out
out={k:plans[k] for k in ['schema_version','path_id','batch_id']};out['kind']='interactions_part';out['tiles']=[]
seen=set()
for tile in plans['tiles']:
 entries=[]; ixsteps=[s for s in tile['steps'] if s['type'] in ['check','hands_on']]
 for ixindex,s in enumerate(ixsteps):
  cid=s['concept_ids'][0];bundle=bundles[cid]
  measures=[]
  for anchor in s['anchors']:
   if '#assessment:' in anchor:
    capability=anchor.split('#assessment:')[1];a=next(a for a in bundle['assessment_anchors'] if a['capability']==capability)
    measures.append({'concept_id':cid,'capability':capability,'fact_ids':a['fact_ids']})
  if not measures:
   measures=[{'concept_id':cid,'capability':a['capability'],'fact_ids':a['fact_ids']} for a in bundle['assessment_anchors']]
  ix={'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'],'difficulty':'intro' if ixindex==0 else 'stretch' if ixindex==len(ixsteps)-1 else 'core','grading_mode':'client','standalone':True,'measures':measures,'anchors':s['anchors']}
  if s['type']=='check':
   prompt,options=Q[s['step_id']]
   # Rotate answer placement, derive keys from authored truth markers.
   shift=ixindex%len(options);options=options[shift:]+options[:shift]
   ix['public']={'prompt':prompt,'options':[{'option_id':'o'+str(i+1),'text':x[0]} for i,x in enumerate(options)],'selection':'single','shuffle':True}
   ix['grading']={'correct_option_ids':['o'+str(i+1) for i,x in enumerate(options) if x[1]],'option_feedback':{'o'+str(i+1):{'message':x[2]} for i,x in enumerate(options)}}
   hint='Identify the boundary this question asks you to prove; do not substitute a neighboring boundary.'
  else:
   hint='Use the supplied fixture contracts to check both intended success and rejection or isolation cases.'
   if cid in supported:
    starter,sol,tests,kind,pkgs=supported[cid]
    files=[fileobj('exercise.py',starter,'editable')]
    # Supply glossary/scenario material as readonly references as well.
    files += [fileobj(f['path'],f['content']) for f in assets['ws.'+cid]['files'] if f['path'] in ['fixtures.json','README.md']]
    ix['public']={'prompt':tasks[cid],'runtime':{'kind':kind,'version':pins[kind]['version'],'packages':pkgs},'workspace':{'entry':'exercise.py','files':files,'asset_mounts':[]}}
    ix['grading']={'solution_files':[{'path':'exercise.py','content':sol}],'tests':[{'test_id':'t'+str(i+1),'kind':kind_,'spec':sp,'visible':True,'message_on_fail':'Compare the computed outcome with the exact supplied contract.'} for i,(kind_,sp) in enumerate(tests)]}
   else:
    d=native[cid];asset=assets['ws.'+cid]
    # A single editable shell entry contains the learner's Python edits as
    # here-documents; all other original/native fixtures are readonly.
    starter_updates={p:next((f['content'] for f in asset['files'] if f['path']==p),'# TODO: complete the supplied contract checks.\nraise NotImplementedError("Complete contract checks")\n' if p.endswith('.py') else '') for p in d['updates']}
    starter=shell_entry(starter_updates,d['commands']);sol=shell_entry(d['updates'],d['commands'])
    files=[fileobj('exercise.sh',starter,'editable')]+[fileobj(f['path'],f['content']) for f in asset['files']]
    ix['public']={'prompt':tasks[cid]+' Edit the embedded files in exercise.sh, then run it in the supplied native environment. This native runner is not implemented by the pinned WASM pack; do not interpret an UNVERIFIED warning as executed evidence.','runtime':{'kind':'bash','version':bash_version},'workspace':{'entry':'exercise.sh','files':files,'asset_mounts':[]}}
    # Native grading commands are transparent and assert their own exact
    # contracts. They are NOT claimed to have run in the unsupported gate.
    ix['grading']={'solution_files':[{'path':'exercise.sh','content':sol}],'tests':[{'test_id':'native_contracts','kind':'stdout_equals','spec':{'command':'bash exercise.sh >/dev/null','expected':subprocess.run(['bash','-c',':'],capture_output=True,text=True,check=True).stdout},'visible':True,'message_on_fail':'Run every supplied native assertion command successfully; a WASM-only verification is unavailable for this workspace.'}]}
   ix['public']['constraints']={k:copy.deepcopy(bundle['practice_anchor']['live_code'][k]) for k in ['allowed_syntax','blocked_syntax']}
  ix['feedback']={'correct':{'message':'The declared outcome and the tested boundary agree.'},'incorrect':{'message':'Check the exact contract and keep the neighboring boundaries separate.'},'hints':[hint]}
  if cid not in seen:
   for rem in screenmap[tile['tile_id']].get('remediation_steps',[]):
    if cid in rem.get('concept_ids',[]):ix['feedback']['remediation_step_id']=rem['step_id'];break
   seen.add(cid)
  entries.append({'step_id':s['step_id'],'interaction':ix})
 out['tiles'].append({'tile_id':tile['tile_id'],'interactions':entries})
(B/'interactions.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('tiles',len(out['tiles']),'interactions',sum(len(t['interactions']) for t in out['tiles']),'supported code',len(supported),'native unverified',len(native))
