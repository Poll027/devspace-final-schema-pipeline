import json, copy, re
from pathlib import Path
P=Path('batches/final_batch_readiness')
plans=json.loads((P/'tile_plans.json').read_text())
g=json.loads((P/'inputs/path_glossary_bundle.json').read_text())
r=json.loads((P/'scenario_asset_registry.json').read_text())
B={b['context']['concept_id']:b for b in g['bundles']}
A={a['asset_id']:a for a in r['assets']}
def file(c,path):
    return next(f['content'] for f in A['ws.'+c]['files'] if f['path']==path)
def fixture(c): return json.loads(file(c,'fixtures.json'))
def rows(a): return [dict(zip([c['name'] for c in A[a]['columns']],row)) for row in A[a]['rows']]
# Editorial text is authored here; all concrete scenario values come from inputs.
F={
'deployment.release_rollback_boundaries':[
'Build makes an executable artifact. Release combines it with deploy-specific configuration. Run starts processes from that selected release.',
'Give each immutable release a unique identifier. A change creates a new release, not an edit to the running one.',
'Record each release’s artifact and configuration. Rollback redeploys a known prior release with its intended configuration.',
'Before selecting that prior release, check compatibility with the current database schema. Application replacement does not itself reverse a migration.'],
'fastapi.documented_responses':[
'Declare known outcomes with responses={status: {"model": PublicModel, "description": ...}}, beside the main response_model and status_code.',
'That metadata documents additional outcomes; it does not produce them. The handler must return the matching response or raise the corresponding expected exception.',
'Use response_description and outcome descriptions to explain what success and expected-error bodies mean to clients.',
'Exercise both real outcomes through HTTP. Compare their statuses and bodies with generated response entries and schemas; do not document an outcome the endpoint never emits.'],
'fastapi.safe_unexpected_errors':[
'Unexpected failures should expose generic public information—not stack traces, exception messages or implementation details.',
'Register a fallback exception handler: record the exception internally and return stable generic JSON with status 500 for an unexpected server condition.',
'Internal evidence should identify the event, code location and interaction context, while omitting prohibited secrets and sensitive data.',
'Disable production debug traceback responses. Debug mode substitutes a traceback response for the configured 500 handler.',
'Use TestClient(app, raise_server_exceptions=False) to exercise the fallback. Assert the generic public response and inspect the safe internal record separately.'],
'integration.upstream_failure_translation':[
'HTTPX separates transport RequestError failures from HTTPStatusError raised by response.raise_for_status() for an unsuccessful HTTP status.',
'Call raise_for_status() when status failures need translation. Classify HTTPStatusError with exc.response.status_code; catch RequestError for failures without a usable response.',
'Remote failures are inputs to the declared local integration contract, not public responses to trust or expose blindly.',
'For a gateway, 502 denotes an invalid upstream response and 504 an upstream timeout. Choose the local status or domain exception from the service’s mapping, not by forwarding every upstream status.',
'Test a supplied upstream status failure and a transport failure. Assert the mapped local response or domain failure, with no raw upstream internals.'],
'integration.webhook_authenticity':[
'Read await request.body() for raw bytes before parsing or modifying the webhook body.',
'Verify every delivery using the publisher-supported SDK or library, raw bytes and endpoint signing secret. Follow the publisher’s signing format; do not invent canonicalization.',
'Reject missing or invalid signatures before processing. Public rejection must not disclose the secret or verification internals.',
'Test a valid signed delivery, a modified body and an absent signature. Only the valid delivery should reach event processing.'],
'observability.evidence_based_service_diagnosis':[
'Compare request rate, failure fraction and latency for the same affected operation and time window. Increased traffic, increased failures and longer waits are different signals.',
'Follow the affected interaction identifier through local and outbound logs. Locate the first recorded failure or delay; the endpoint’s final error need not identify its origin.',
'Compare integration timeout evidence and emitted database work with that request’s context. Distinguish an upstream wait from persistence work or a local input rejection.',
'Reproduce the supplied failure with a controlled request. Record the outcome and evidence, and change the suspected boundary only after checking that the evidence supports it.'],
'security.bounded_api_resources':[
'Apply finite limits to expensive untrusted work, including input size, result count, duration and costly concurrency; do not accept unrestricted resource consumption.',
'Use maintained middleware to enforce actual body-byte limits. Constrain caller-selected batch or page sizes with Field bounds, not claimed sizes.',
'Configure finite dependency timeouts and the supplied Uvicorn --limit-concurrency budget where service policy needs to bound concurrent accepted work.',
'Test within-budget and beyond-budget inputs. Reject excess before expensive work, while accepted work keeps its intended contract.'],
'sqlalchemy.redundant_queries':[
'Lazy relationship access can emit extra SELECTs. Loading each parent’s relationship during iteration can produce an N+1 query pattern.',
'Use statement.options(selectinload(Entity.relationship_attribute)) to fetch collections for selected parents with an additional batched query rather than one per parent.',
'joinedload(...) is an eager-loading alternative using a join. For collection loading, apply Result.unique() as required to deduplicate parents.',
'With engine echo=True, compare emitted SQL before and after the change. Confirm fewer relationship queries and unchanged returned entity data.'],
'testing.database_state_isolation':[
'A yield fixture runs setup before yield and teardown afterward, making cleanup explicit for each test’s scope.',
'Open an outer connection transaction. Bind the test session to that connection with join_transaction_mode="create_savepoint"; roll back the outer transaction during teardown.',
'Override the application session provider with the test provider. Write through TestClient and read the resulting state through that same test database boundary.',
'Close the test session and connection and restore overrides during teardown. Verify that a subsequent test does not inherit the first test’s written state.'],
'auth.authorization_server_integration':[
'Obtain an actual issuer-issued access token using the supplied established authorization-server client or harness, through authorization code with PKCE where applicable. Do not add a resource-owner password grant.',
'Configure the registered client identifier, issuer authorization and token endpoints, and redirect URI. Complete the code redirect, then a separate token POST with the matching PKCE verifier using that client.',
'Configure the existing verifier with trusted JWKS URL, expected issuer, allowed algorithms and API audience. Resolve a key with PyJWKClient and require intended claims during jwt.decode.',
'Send the issued token as Authorization: Bearer token to the protected HTTP endpoint, exercising real bearer extraction and the configured verifier.',
'Assert acceptance of the valid issued token and rejection of a tampered or wrong-audience issued token. Keep authentication and verification active; do not override them or fabricate locally valid tokens.'],
'auth.endpoint_permissions':[
'OAuth2 scopes express requested or granted operation permissions. Authentication alone does not establish every required permission.',
'Declare Security(provider, scopes=[...]) on the protected operation. Accept SecurityScopes in the provider to read those requirements.',
'Compare every required scope with the verified token context. Reject the request if any required scope is missing.',
'Test verified tokens with and without the required scope. Only the sufficiently scoped request should succeed.'],
'fastapi_backend.webhook_delivery_idempotency':[
'Deduplicate with the authenticated publisher event identifier. Retain its record across application restarts for the required replay window.',
'Record that identifier atomically with durable state changes in a transaction backed by uniqueness, so concurrent deliveries cannot both apply the effect.',
'Acknowledge an already processed event as a successful duplicate without another state change. Test duplicate and concurrent deliveries separately.'],
'fastapi_backend.webhook_replay_freshness':[
'Use the provider-signature-authenticated delivery timestamp. Providers can refresh it and the signature on retries: it establishes delivery-timestamp freshness, not original event age. An unsigned timestamp cannot establish authenticated freshness.',
'After signature verification, parse the signed timestamp. Reject deliveries outside the configured window, including unacceptably future timestamps under provider policy.',
'Keep the receiver clock synchronized. Clock drift would distort the intended window when comparing the authenticated timestamp with local time.',
'Test valid signatures with in-window, expired and impermissibly future delivery timestamps. Authenticity alone does not make every signed delivery fresh.'],
'integration.bounded_idempotent_retries':[
'Repeating non-idempotent requests can duplicate effects. Retry only when the method or application contract establishes idempotency, or proves the original request was not applied.',
'Retry-After may be an HTTP date or a delay in seconds. Incorporate a valid supplied delay instead of immediately retrying against that instruction.',
'Set finite attempt and total-time budgets, with a maintained client’s bounded backoff where applicable. Repeated transient failures must eventually stop.',
'Classify failures as retryable or terminal under the operation contract. A timeout or lost response alone does not prove the remote operation had no effect.',
'Verify transient failure then success, repeated failures exhausting limits, and no blind repetition of non-idempotent work without a retry-safe contract.'],
'auth.object_authorization':[
'Check permission for the specific object identifier. An authenticated caller and valid identifier do not establish ownership.',
'Select by both object identity and authorized owner or tenant context. Do not trust an owner identifier supplied by the caller.',
'Test distinct authorized contexts. Each should access its permitted object but be unable to obtain or change the other context’s object by substituting its identifier.'],
'fastapi.production_security_documentation':[
'Use HTTPBearer for deployed bearer-token presentation. Its generated securitySchemes entry must not imply that this API issues passwords or tokens.',
'For an established authorization-code issuer, configure OAuth2AuthorizationCodeBearer(authorizationUrl=..., tokenUrl=..., scopes=...) with supplied issuer endpoints and permission descriptions.',
'Describe deployed authorization-code and PKCE acquisition where applicable. Do not present an OAuth2 password flow as production guidance.',
'Attach the scheme and required scopes through real operation dependencies, so generated security requirements agree with accepted authority.',
'Inspect components.securitySchemes and protected operations’ security entries. Compare issuer URLs, bearer presentation and required permissions with the deployed contract.'],
'fastapi.openapi_contract_inspection':[
'Retrieve /openapi.json. Inspect router paths, parameters, request and response schemas, and security requirements as public contract artifacts.',
'Compare generated requiredness, types, constraints and output fields with executable input and output behavior to locate drift.',
'Compare documented success and expected-error statuses with exercised HTTP outcomes. Additional response metadata does not prove that the handler emits an outcome.',
'Audit public examples and descriptions for secrets and sensitive personal data. Use model-valid examples, not realistic private values.',
'Check public security schemes and operation requirements against configured bearer presentation and the established issuer contract. Do not introduce an undeployed password grant.'],
'testing.api_authentication_authorization':[
'Send absent, malformed and supplied bearer credentials through the real protected HTTP endpoint. Keep authentication and verification gates active.',
'Test invalid signatures, expiry and wrong token context separately from a valid token. Assert credential rejection before protected output.',
'Compare valid credentials lacking operation permission with valid sufficiently permitted credentials, separating authentication from operation authorization.',
'Test a valid caller substituting another caller’s object identifier as a distinct denial path from missing operation permission.',
'For each denial, assert declared status and safe body. For full authorization, assert the public projected result—not just failure versus success.']}
T={
'deployment.release_rollback_boundaries': 'Select a release, not a schema reversal',
'fastapi.documented_responses':'Declarations are not implementation',
'fastapi.safe_unexpected_errors':'Separate public errors from internal evidence',
'integration.upstream_failure_translation':'Translate remote failures through the local contract',
'integration.webhook_authenticity':'Verify delivered bytes before processing',
'observability.evidence_based_service_diagnosis':'Locate the boundary supported by evidence',
'security.bounded_api_resources':'Bound expensive work before it starts',
'sqlalchemy.redundant_queries':'Inspect relationship queries',
'testing.database_state_isolation':'One test database boundary, then cleanup',
'auth.authorization_server_integration':'Acquire issued authority and verify it at the API',
'auth.endpoint_permissions':'Verified identity still needs operation permission',
'fastapi_backend.webhook_delivery_idempotency':'A duplicate delivery must not repeat its effect',
'fastapi_backend.webhook_replay_freshness':'Signed does not necessarily mean fresh',
'integration.bounded_idempotent_retries':'Retry only safe work within finite limits',
'auth.object_authorization':'Check authority for the requested object',
'fastapi.production_security_documentation':'Document deployed token authority',
'fastapi.openapi_contract_inspection':'Compare public declarations with behavior',
'testing.api_authentication_authorization':'Prove each protected endpoint gate separately'}
# Compact second explainers: same facts, one scenario-based trace.
W={
'deployment.release_rollback_boundaries': 'In the release records, {release} pairs {artifact} with {configuration}. Build supplies the artifact; release adds configuration; run starts its processes. Changes create new uniquely identified immutable releases. Rollback selects a recorded prior release with its intended configuration only after checking the current schema. An application rollback does not itself undo migrations.',
'integration.upstream_failure_translation':'Trace the supplied status failure through raise_for_status() and HTTPStatusError, using exc.response.status_code. Trace the timeout separately through RequestError. The declared contract selects local responses; remote statuses are not automatically local meanings. For gateways, 502 means invalid upstream response and 504 upstream timeout. Test both paths, asserting the mapped local response or domain failure and exclusion of raw upstream internals.',
'integration.webhook_authenticity':'For this {publisher} fixture, read await request.body() before parsing. Verify every delivery with the publisher-supported library, raw bytes and endpoint secret, following its signing format—not invented canonicalization. Reject absent or invalid signatures without secret or internal-detail disclosure. Test the valid, modified-body and absent-signature deliveries: only the valid one should reach processing.',
'observability.evidence_based_service_diagnosis':'Compare the affected operation’s request rate, failure fraction and latency over matching windows. Follow {interaction} through local and outbound records to the first delay or failure, not just the final endpoint error. Compare timeout evidence and emitted database work in that context to distinguish upstream waiting, persistence work and local input rejection. Reproduce the controlled request, record its outcome and evidence, and change a suspected boundary only when the evidence supports it.',
'security.bounded_api_resources':'In this fixture, the supplied body budget is {body_bytes} bytes and batch budget is {batch_size} items. Enforce actual bytes with maintained middleware and batch bounds with Field. Bound result count, duration and costly concurrency too; use the finite dependency timeout and supplied Uvicorn concurrency policy where required. Test within and beyond budget, rejecting excess before expensive work while preserving the accepted contract. Claimed size is not measured size.',
'sqlalchemy.redundant_queries':'Compare the original listing with statement.options(selectinload(Entity.relationship_attribute)). Lazy per-parent collection access can emit N+1 SELECTs; selectinload adds batched collection retrieval. joinedload instead uses a join and requires Result.unique() for collection parent deduplication. Enable echo=True, capture both versions in fresh sessions, and compare SQL plus returned entity data. Fewer relationship queries must accompany unchanged data, not substitute for checking it.',
'testing.database_state_isolation':'For item {item_id}, open an outer connection transaction and bind Session with join_transaction_mode="create_savepoint". Override the session provider; TestClient writes and database reads share that connection boundary. Yield separates setup from teardown. Close the session, roll back the outer transaction, close the connection and restore overrides. Then verify a subsequent test sees no inherited write. The first successful write alone does not prove isolation.',
'auth.authorization_server_integration':'Use the supplied registered client identifier, issuer endpoints and redirect URI. Complete the authorization-code redirect and separate token POST with the matching PKCE verifier where applicable; add no password grant. Configure trusted JWKS, issuer, algorithms, required claims and API audience in the existing verifier, resolving a key with PyJWKClient for jwt.decode. Send the issued access token as Authorization: Bearer token. Assert valid acceptance and tampered or wrong-audience rejection through real extraction and verification, without overrides or locally fabricated tokens.',
'auth.endpoint_permissions':'The operation requires {scope}. Declare it with Security(provider, scopes=[...]); SecurityScopes exposes that requirement in the provider. Compare every requirement against verified token scopes and deny if any is missing. Test otherwise verified credentials with and without that scope. Only the sufficiently scoped request should succeed: authentication alone does not grant every operation permission.',
'fastapi_backend.webhook_delivery_idempotency':'For authenticated event {event}, use the publisher event identifier as the durable deduplication key. Retain it across restarts for the required replay window. A uniqueness-backed transaction records the identifier atomically with its state change, preventing concurrent deliveries from both applying the effect. An already processed event receives successful duplicate acknowledgment without another change. Test sequential duplicates and concurrent attempts separately.',
'fastapi_backend.webhook_replay_freshness':'First verify the provider signature, then parse its authenticated delivery timestamp and compare it with the synchronized receiver clock. Reject expired and impermissibly future deliveries under the configured policy. Test valid signatures for in-window, expired and too-far-future timestamps. A valid signature alone is not freshness; providers can refresh timestamps on retries, so the check establishes delivery-timestamp freshness, not original event age. Unsigned timestamps cannot establish authenticated freshness.',
'integration.bounded_idempotent_retries':'The fixture separates an idempotent {safe_method} from a {unsafe_method} without a retry-safe contract or proof it was not applied. A timeout or lost response is not that proof. Classify failures using the operation contract. Respect valid Retry-After dates or seconds. Use finite attempts and total time with maintained bounded backoff where applicable. Test transient failure then success, repeated failures exhausting limits, and no blind retry of unsafe work.',
'fastapi.production_security_documentation':'Declare HTTPBearer for presentation; it does not mean the API issues credentials. Configure OAuth2AuthorizationCodeBearer with supplied issuer endpoints and scope descriptions for the established authorization-code contract. Describe PKCE where applicable, not a production password grant. Attach real dependencies and required scopes; inspect components.securitySchemes and operation security entries against deployed bearer authority, issuer URLs and permissions.',
'fastapi.openapi_contract_inspection':'Retrieve /openapi.json and review router paths, parameters, input/output schemas and security requirements. Compare requiredness, types, constraints and output fields with executable behavior; compare success/error statuses with HTTP evidence. Validate public examples and remove secrets or sensitive personal data from descriptions. Security metadata must match configured bearer and established issuer authority, without an undeployed password grant. Declarations alone do not prove outcomes.',
'testing.api_authentication_authorization':'Exercise the real endpoint without replacing authentication or verification. Separate absent and malformed credentials, invalid signature, expiry and wrong context from a valid token. Then isolate missing operation permission, and a valid caller substituting another caller’s object identifier. Finally exercise full authorization. Assert each denial’s declared status and safe body before protected output, and the authorized public projection. One denial plus one success does not prove every gate.'}
C={
'deployment.release_rollback_boundaries':'Contrast a compatible recorded prior release with an incompatible one: only the former is a rollback candidate; neither reverses the schema.',
'fastapi.documented_responses':'Contrast declaring an outcome with emitting it: documentation changes metadata, while the handler still supplies the actual response.',
'fastapi.safe_unexpected_errors':'Contrast generic public information with safe internal diagnostics: event and location belong internally, not in the public error body.',
'integration.upstream_failure_translation':'Contrast an unsuccessful HTTP response with a transport failure: only the former supplies a response status to classify.',
'integration.webhook_authenticity':'Contrast the signed raw body with a modified body: only a successfully verified delivery reaches processing.',
'observability.evidence_based_service_diagnosis':'Contrast the endpoint’s final error with the first recorded delay: diagnose from correlated evidence, not the last message alone.',
'security.bounded_api_resources':'Contrast within-budget work with excess work: reject excess before expensive processing, while accepted work retains its contract.',
'sqlalchemy.redundant_queries':'Contrast one explicit parent SELECT with one database round trip: lazy relationship access can still emit more SELECTs.',
'testing.database_state_isolation':'Contrast seeing this test’s write with leaving it for the next test: shared reads prove visibility, teardown plus a clean next test proves isolation.',
'auth.authorization_server_integration':'Contrast an issuer-issued token through the real verifier with an overridden verifier: only the real path proves issuer integration.',
'auth.endpoint_permissions':'Contrast verified identity with sufficient scope: a verified token missing a required permission must still be denied.',
'fastapi_backend.webhook_delivery_idempotency':'Contrast duplicate acknowledgment with duplicate effect: acknowledge an already processed identity successfully without repeating the state change.',
'fastapi_backend.webhook_replay_freshness':'Contrast authentic with fresh: an expired signed timestamp is authentic but outside the acceptance window.',
'integration.bounded_idempotent_retries':'Contrast a retry-safe contract with a lost response: loss alone does not prove that repeating an operation is safe.',
'auth.object_authorization':'Contrast a valid object identifier with permission for that object: authenticated identity alone does not establish ownership.',
'fastapi.production_security_documentation':'Contrast bearer presentation with token acquisition: public schemes describe deployed authority, not an invented password grant.',
'fastapi.openapi_contract_inspection':'Contrast a documented outcome with exercised HTTP evidence: metadata alone cannot prove that the endpoint emits it.',
'testing.api_authentication_authorization':'Contrast a missing-permission denial with another-owner denial: they prove separate authorization gates.'}
def params(c):
    f=fixture(c)
    if c=='deployment.release_rollback_boundaries':
        v=rows('ds.releases')[0];return {'release':v['release_id'],'artifact':v['artifact'],'configuration':v['configuration']}
    if c=='integration.webhook_authenticity':return {'publisher':json.loads(file(c,'test_config.json'))['publisher']}
    if c=='observability.evidence_based_service_diagnosis':return {'interaction':rows('ds.correlated_records')[0]['interaction_id']}
    if c=='security.bounded_api_resources':return f['hypothetical_budgets']
    if c=='testing.database_state_isolation':return {'item_id':f['item']['id']}
    if c=='auth.endpoint_permissions':return {'scope':f['operation_scopes'][0]}
    if c=='fastapi_backend.webhook_delivery_idempotency':return {'event':f['authenticated_events'][0]['publisher_event_id']}
    if c=='integration.bounded_idempotent_retries':return {'safe_method':f['operations'][0]['method'],'unsafe_method':f['operations'][1]['method']}
    return {}
def lin(c,fids=None,tbs=None,visual=False):
    return {'concept_ids':[c], 'fact_ids':[c+'#'+f for f in (fids or [])], 'teaching_block_ids':[c+'#'+t for t in (tbs or [])], **({'anchors':[c+'#visual']} if visual else {})}
def prose(text,c,fids,tbs,role='mechanism'):
    return {'type':'prose','text':text,'role':role,'lineage':lin(c,fids,tbs)}
def fact_prose(c,fid,tbs=None,role='mechanism'):
    eligible=[tb['id'] for tb in B[c]['teaching_blocks'] if fid in tb['fact_ids'] and (tbs is None or tb['id'] in tbs)]
    return prose(F[c][int(fid[1:])-1],c,[fid],eligible,role)
def table(c,a,caption):
    return {'type':'data_table','asset_ref':{'asset_id':a,'columns':[x['name'] for x in A[a]['columns']]},'caption':caption,'lineage':lin(c,visual=True)}
def diagram(c,labels,alt,edges=None):
    nodes=[{'id':'n'+str(i+1),'label':v} for i,v in enumerate(labels)]
    return {'type':'diagram','diagram_kind':'mapping','nodes':nodes,'edges':edges or [],'alt_text':alt,'lineage':lin(c,visual=True)}
def flow(c,labels,edges,alt):
    return {'type':'process_flow','direction':'TB','nodes':[{'id':'n'+str(i+1),'label':v,'kind':k} for i,(v,k) in enumerate(labels)],'edges':[{'from':'n'+str(a),'to':'n'+str(b),'label':l,'kind':k} for a,b,l,k in edges],'alt_text':alt,'lineage':lin(c,visual=True)}
def code(c,text,annotations=None,language='python'):
    return {'type':'code_walkthrough','language':language,'code':text,'annotations':annotations or [],'reveal':'all','lineage':lin(c,visual=True)}
def pair(c,left,right,ll,rl,takeaway):
    return {'type':'side_by_side','left':left,'right':right,'left_label':ll,'right_label':rl,'takeaway':takeaway,'lineage':lin(c,visual=True)}
# Snippets illustrate mechanisms, not executed results. Computation is reserved for stage 05.
CODE={
'integration.webhook_authenticity':'''raw = await request.body()
signature = request.headers.get(config['signature_header'])
if not signature:
    raise HTTPException(status_code=400, detail='Invalid signature')
try:
    event = publisher_verifier(raw, signature, signing_secret)
except (ValueError, stripe.error.SignatureVerificationError):
    raise HTTPException(status_code=400, detail='Invalid signature')
process_event(event)
return {'received': True}''',
'auth.endpoint_permissions':'''def require_permissions(security_scopes: SecurityScopes,
                        verified_context=Depends(verified_token_context)):
    for required in security_scopes.scopes:
        if required not in verified_context['scopes']:
            raise HTTPException(status_code=403, detail='Forbidden')
    return verified_context
# Use the supplied operation requirement, not a caller-selected scope.
Security(require_permissions, scopes=fixtures['operation_scopes'])''',
'auth.object_authorization':'''statement = select(Order).where(
    Order.id == requested_order_id,
    Order.owner_id == principal.owner_id,
)
order = await session.scalar(statement)
if order is None:
    unavailable = fixtures['unavailable_object']
    raise HTTPException(status_code=unavailable['status'],
                        detail=unavailable['body']['detail'])''',
'fastapi.documented_responses':'''@app.post('/orders', response_model=PublicModel,
          status_code=fixtures['success_status'],
          response_description='The public order state',
          responses={fixtures['conflict_status']: {
              'model': ConflictModel,
              'description': 'The requested order conflicts'}})
def create_order(conflict: bool = False):
    if conflict:
        raise HTTPException(status_code=fixtures['conflict_status'],
                            detail=fixtures['conflict_body']['detail'])
    return fixtures['success_body']''',
'fastapi.safe_unexpected_errors':'''app = FastAPI(debug=False)
@app.exception_handler(Exception)
async def fallback(request: Request, exc: Exception):
    record_safe_failure(request)
    return JSONResponse(status_code=fixtures['public_status'],
                        content=fixtures['public_body'])
# Exercise fallback output instead of re-raising the server exception.
with TestClient(app, raise_server_exceptions=False) as client:
    response = client.get('/controlled-failure')
    assert response.status_code == fixtures['public_status']
    assert response.json() == fixtures['public_body']
    # Inspect safe_records separately: no exception messages or secrets.''',
'sqlalchemy.redundant_queries':'''statement = select(Entity).order_by(Entity.id).limit(len(fixtures['parent_ids']))
statement = statement.options(selectinload(Entity.relationship_attribute))
parents = session.execute(statement).scalars().all()
return [{'id': p.id, 'children': [c.id for c in p.relationship_attribute]}
        for p in parents]
# Capture emitted SQL with echo=True in a fresh session.
# Compare unchanged entity data, not just fewer relationship SELECTs.''',
'fastapi.production_security_documentation':'''bearer_scheme = HTTPBearer(scheme_name='OrderBearer')
code_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=issuer_configuration['authorization_url'],
    tokenUrl=issuer_configuration['token_url'],
    scopes=issuer_configuration['scopes'],
    scheme_name='OrderAuthorizationCode',
)
# Attach through the real dependencies that enforce each operation's scope.
# Inspect components.securitySchemes and each operation's security entry.'''}

def visual(c,planned):
    f=fixture(c)
    if c=='deployment.release_rollback_boundaries':
        return [flow(c,[('Build → executable artifact','step'),('Artifact + deploy configuration → unique immutable release','step'),('Run → selected release processes','step'),('Prior release compatible with current schema?','decision'),('Redeploy recorded prior artifact + intended configuration','step'),('Do not select incompatible prior release','end')],[(1,2,'build artifact','next'),(2,3,'select release','next'),(3,4,'rollback candidate','next'),(4,5,'yes','yes'),(4,6,'no','no'),(5,3,'run prior release; schema not reversed','loop_back')], 'Build, release and run are distinct; rollback checks schema compatibility without reversing migrations.'),table(c,'ds.releases','Recorded releases and supplied compatibility evidence')]
    if c=='fastapi.documented_responses':
        vals=[f"Success: {f['success_status']} {json.dumps(f['success_body'])}",f"Conflict: {f['conflict_status']} {json.dumps(f['conflict_body'])}"]
        return [pair(c,code(c,CODE[c]),diagram(c,vals,'Supplied HTTP outcome contract, not newly computed query or code output.'),'Response declarations + handler','Supplied HTTP contract','Compare generated status entries and schemas with HTTP tests of both outcomes.')]
    if c=='fastapi.safe_unexpected_errors':
        public=diagram(c,[str(f['public_status'])+' '+json.dumps(f['public_body'])],'Supplied generic public response; no internal details.')
        # The authored record is copied from the starter AST, never invented.
        import ast
        tree=ast.parse(file(c,'starter.py'))
        fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='record_safe_failure')
        record=ast.literal_eval(fn.body[0].value.args[0])
        internal=diagram(c,[k+': '+v for k,v in record.items()]+['Omit prohibited fields: '+', '.join(f['prohibited_record_fields'])],'Safe internal diagnostic record, separate from the public response.')
        return [pair(c,public,internal,'Public response contract','Internal diagnostic record','Generic output and actionable safe evidence have separate disclosure rules.'),code(c,CODE[c])]
    if c=='integration.upstream_failure_translation':
        s=f['upstream_503'];t=f['timeout']
        return [flow(c,[('Upstream unsuccessful status','io'),('raise_for_status() → HTTPStatusError; inspect response.status_code','step'),(f"Declared mapping → {s['status']} {s['detail']}",'end'),('Upstream timeout','io'),('RequestError: transport failure','step'),(f"Declared mapping → {t['status']} {t['detail']}",'end')],[(1,2,'status classification','next'),(2,3,'local contract','next'),(4,5,'transport classification','next'),(5,6,'local contract','next')],'Separate remote status and transport paths; exclude raw upstream internals.')]
    if c=='integration.webhook_authenticity':
        annotations=[{'start_line':1,'end_line':1,'text':'Raw bytes first: do not parse or rewrite them.'},{'start_line':2,'end_line':4,'text':'Absent signature test: reject before event processing.'},{'start_line':5,'end_line':8,'text':'Publisher-supported verification: modified-body test rejects safely.'},{'start_line':9,'end_line':10,'text':'Valid signed delivery test: only this branch reaches processing.'}]
        return [code(c,CODE[c],annotations)]
    if c=='observability.evidence_based_service_diagnosis':
        return [pair(c,table(c,'ds.operation_signals','Matched operation/time-window signals'),table(c,'ds.correlated_records','Chronological correlated boundary records'),'Rate, failures, latency evidence','Interaction-correlated records','Locate the first recorded delay before proposing a boundary change. Compute rates from matching-window counts; do not infer origin from the final error.')]
    if c=='security.bounded_api_resources':
        snippet = '''from starlette.middleware.body_limit import RequestBodyLimitMiddleware
class BatchInput(BaseModel):
    order_ids: list[int] = Field(max_length=budgets['batch_size'])
app.add_middleware(RequestBodyLimitMiddleware,
                   max_body_size=budgets['body_bytes'])
outbound_timeout = httpx.Timeout(budgets['dependency_timeout_seconds'])
# Supply the configured Uvicorn --limit-concurrency budget at launch.
# Test within/beyond limits before expensive_dependency executes.'''
        q=f['hypothetical_budgets']
        return [code(c,snippet,[{'start_line':2,'end_line':3,'text':'Field bounds caller-selected batch size.'},{'start_line':4,'end_line':5,'text':'Maintained middleware counts actual body bytes.'},{'start_line':6,'end_line':8,'text':'Finite timeout and supplied concurrency policy bound accepted work; test excess rejection.'}]),flow(c,[(f"Actual body bytes ≤ supplied {q['body_bytes']} budget?",'decision'),(f"Field batch bound ≤ supplied {q['batch_size']} budget?",'decision'),(f"Dependency duration ≤ supplied {q['dependency_timeout_seconds']} seconds; Uvicorn concurrency budget {q['limit_concurrency']}",'step'),('Accepted work retains intended contract','end'),('Reject excess before expensive work','end')],[(1,2,'within size budget','yes'),(1,5,'excess bytes','no'),(2,3,'within batch budget','yes'),(2,5,'excess batch','no'),(3,4,'within configured policy','next')],'Actual size, batch count, finite timeout and concurrency are separate resource boundaries.')]
    if c=='sqlalchemy.redundant_queries':
        old=file(c,'starter.py');old=old[old.index('def listing(session):'):old.index('# Run baseline')]
        baseline=file(c,'baseline_sql.txt')
        captures=re.findall(r'SELECT .*?(?=\n\[)',baseline,re.S)
        baseline_panel=diagram(c,captures,'Previously captured baseline SQL from the registered fresh-session listing; repeated relationship SELECTs are visible.')
        return [pair(c,code(c,old),code(c,CODE[c]),'Original listing: lazy relationships','Revised listing: selectinload','Capture SQL in fresh sessions with echo=True and verify unchanged parent/collection data.'),pair(c,baseline_panel,diagram(c,['Revised capture: use echo=True in a fresh Session.', 'selectinload batches collection retrieval for selected parents instead of per-parent queries.', 'Compare captured SQL and returned entity data after running the revision.'],'Revised SQL must be computed in the execution stage; no revised output is authored.'),'Registered baseline SQL capture','Revised capture to verify','The loading change targets repeated relationship queries, not the returned entity data.'),pair(c,table(c,'ds.Entity','Parent fixture'),table(c,'ds.relationship_attribute','Collection fixture'),'Parents','Relationships','The same fixture data must remain in the returned entities after the loading change.')]
    if c=='testing.database_state_isolation':
        snippet='''@pytest.fixture
def isolated_client():
    original = app.dependency_overrides.copy()
    connection = engine.connect()
    outer = connection.begin()
    test_session = Session(bind=connection,
                           join_transaction_mode='create_savepoint')
    def test_provider():
        yield test_session
    app.dependency_overrides[session_provider] = test_provider
    try:
        with TestClient(app) as client:
            yield client, test_session
    finally:
        try:
            test_session.close()
        finally:
            try:
                outer.rollback()
            finally:
                try:
                    connection.close()
                finally:
                    app.dependency_overrides.clear()
                    app.dependency_overrides.update(original)'''
        annotations=[{'start_line':3,'end_line':10,'text':'Setup: the request session and test database reads share the outer connection.'},{'start_line':11,'end_line':13,'text':'Yield: write through TestClient, then read through the yielded test session.'},{'start_line':14,'end_line':25,'text':'Teardown: cleanup and restore overrides even if the test fails. Verify no state leaks into the next test.'}]
        tests=file(c,'test_items.py');tests=tests[tests.index('def test_writes_item'):]
        orders=[' → '.join(order) for order in f['execution_orders']]
        return [code(c,snippet,annotations),pair(c,code(c,tests),diagram(c,orders+['Run both orders; verify no inherited write.'],'Required execution orders; passing results must be computed, not authored.'),'Two separate tests','Execution-order verification','A write and a subsequent clean test boundary are both required; execute both orders.')]
    if c=='auth.authorization_server_integration':
        cfg=json.loads(file(c,'issuer_configuration.json'))
        return [flow(c,[(f"Registered client: {cfg['client_id']}; redirect {cfg['redirect_uri']}",'start'),('Authorization-code redirect: '+cfg['authorization_url'],'step'),('Separate token POST + matching PKCE verifier: '+cfg['token_url'],'step'),('Issued access token → Authorization: Bearer token','io'),('API verifies trusted JWKS: '+cfg['jwks_url'],'step'),('Check issuer, algorithms, required claims, API audience','decision'),('Assert valid issued-token acceptance','end'),('Assert tampered or wrong-audience rejection','end')],[(1,2,'client acquisition boundary','next'),(2,3,'code exchange','next'),(3,4,'issued authority','next'),(4,5,'API verification boundary','next'),(5,6,'PyJWKClient + jwt.decode','next'),(6,7,'valid','yes'),(6,8,'invalid','no')],'Token acquisition and protected API verification are separate trust boundaries; keep real dependencies active.')]
    if c=='auth.endpoint_permissions':
        return [code(c,CODE[c],[{'start_line':1,'end_line':2,'text':'Operation requirements reach SecurityScopes while real token verification stays active.'},{'start_line':3,'end_line':5,'text':'Compare every scope; an otherwise verified token missing permission is denied.'},{'start_line':6,'end_line':8,'text':'Only sufficient scope reaches the operation. Test both verified credential conditions.'}])]
    if c=='fastapi_backend.webhook_delivery_idempotency':
        return [flow(c,[('Authenticated publisher event identifier','start'),('Begin uniqueness-backed transaction for event identity','step'),('Already processed identity?','decision'),('Successful duplicate acknowledgment; no repeated state change','end'),('New event: record identity + durable change atomically; retain record across restarts','end')],[(1,2,'deduplication key','next'),(2,3,'atomic decision boundary','next'),(3,4,'duplicate','yes'),(3,5,'new event','no')],'Durable atomic event identity and effect prevent concurrent double application; test duplicates and concurrency separately.'),table(c,'ds.order_events','Authenticated event fixture')]
    if c=='fastapi_backend.webhook_replay_freshness':
        # A diagram is an allowed alternate of a planned flow; it expresses policy without computing expected answers.
        return [flow(c,[('Provider signature verified?','decision'),('Parse authenticated delivery timestamp','step'),('Compare with synchronized receiver clock and configured past/future bounds','decision'),('Fresh authenticated delivery','end'),('Reject unverifiable or out-of-window delivery','end')],[(1,2,'yes','yes'),(1,5,'no','no'),(2,3,'delivery timestamp, not event age','next'),(3,4,'inside window','yes'),(3,5,'expired or too far future','no')],'Verify signature before freshness; signed timestamp does not establish original event age.'),table(c,'ds.delivery_timestamps','Authenticated delivery-timestamp cases; evaluate configured bounds')]
    if c=='integration.bounded_idempotent_retries':
        q=f['hypothetical_limits']
        return [flow(c,[('Method/contract idempotent or original proven not applied?','decision'),('Classify retryable versus terminal under contract','decision'),('Respect valid Retry-After date or seconds; bounded maintained backoff','step'),(f"Stop at {q['max_attempts']} attempts or {q['total_time_budget_seconds']} seconds total budget",'decision'),('Attempt retry-safe operation','step'),('Stop; surface declared outcome','end')],[(1,2,'retry-safe','yes'),(1,6,'unsafe; loss alone is not proof','no'),(2,3,'retryable','yes'),(2,6,'terminal','no'),(3,4,'delay fits finite policy','next'),(4,5,'budget remains','yes'),(4,6,'budget exhausted','no'),(5,2,'if another failure','loop_back')],'Retry-safe authority, contract classification, server delay and finite limits all bound repetition.')]
    if c=='auth.object_authorization':
        return [table(c,'ds.orders','Object identity and trusted owner context'),code(c,CODE[c])]
    if c=='fastapi.production_security_documentation':
        cfg=f['authorization_code_issuer']
        labels=['Bearer presentation: '+json.dumps(f['bearer_scheme']), 'Issuer authorization URL: '+cfg['authorization_url'], 'Issuer token URL: '+cfg['token_url']]
        labels += [op+': '+v['dependency']+' requires '+v['scope'] for op,v in f['operation_requirements'].items()]
        return [pair(c,diagram(c,labels,'Supplied deployed contract: bearer presentation, issuer URLs and operation permissions.'),code(c,CODE[c]),'Supplied deployed contract','Security declarations','Inspect generated schemes and operation requirements against this same accepted authority; do not advertise a password grant.')]
    if c=='fastapi.openapi_contract_inspection':
        schema=json.loads(file(c,'generated_schema.json')); http=json.loads(file(c,'http_evidence.json'))
        paths=schema['paths']; post=paths['/orders']['post']
        declarations=[f"POST /orders: documented statuses {', '.join(post['responses'])}"]
        declarations += ['OrderInput '+json.dumps(schema['components']['schemas']['OrderInput']), 'PublicOrder '+json.dumps(schema['components']['schemas']['PublicOrder'])]
        duplicate=next(x for x in http['records'] if x['request']['method']=='POST' and x['request'].get('json')==f['initial_orders'][0] if False) if False else next(x for x in http['records'] if x['request']['method']=='POST' and x['request'].get('json',{}).get('id')==f['initial_orders'][0]['id'])
        declared=next(status for status,v in post['responses'].items() if v['description']=='Duplicate order')
        declarations.append('Drift marker: duplicate outcome declares '+declared+'; captured HTTP status is '+str(duplicate['status']))
        evidence=[x['request']['method']+' '+x['request']['path']+' → '+str(x['status'])+' '+json.dumps(x['body']) for x in http['records'][:4]]
        return [pair(c,diagram(c,declarations,'Selected captured generated declarations; inspect complete public schema in the registered workspace.'),diagram(c,evidence,'Selected captured HTTP evidence from the registered workspace; not newly computed output.'),'Captured generated schema','Captured HTTP evidence','Compare the documented duplicate-order status with the exercised duplicate case; audit model constraints, output fields, examples and configured security too.')]
    if c=='testing.api_authentication_authorization':return [table(c,'ds.authentication_test_matrix','Separate credential, operation-permission and object-permission test cases')]
    raise ValueError(c)

TAKE={
'deployment.release_rollback_boundaries':'Keep build, release and run distinct; verify rollback compatibility without assuming migration reversal.',
'fastapi.documented_responses':'Response declarations must match actual success and expected-error behavior.',
'fastapi.safe_unexpected_errors':'Keep public unexpected errors generic and internal evidence safe; disable debug tracebacks.',
'integration.upstream_failure_translation':'Separate transport from status failures, then use the declared local mapping and test both.',
'integration.webhook_authenticity':'Verify raw bytes using the publisher contract; missing or invalid signatures never reach processing.',
'observability.evidence_based_service_diagnosis':'Compare matching-window signals, trace correlated evidence and reproduce before changing the suspected boundary.',
'security.bounded_api_resources':'Bound size, count, duration and costly concurrency; test rejection before excess work.',
'sqlalchemy.redundant_queries':'Use eager loading deliberately; compare emitted SQL and unchanged entity data.',
'testing.database_state_isolation':'Share the test connection for writes and reads, then clean up and verify the next test is isolated.',
'auth.authorization_server_integration':'Use actually issued tokens through real acquisition and configured API verification, not a password grant or overrides.',
'auth.endpoint_permissions':'Verified identity still needs every operation scope; test permitted and missing-scope requests.',
'fastapi_backend.webhook_delivery_idempotency':'Persist event identity atomically with effects; acknowledge duplicates without repeating them.',
'fastapi_backend.webhook_replay_freshness':'After signature verification, check delivery-timestamp freshness with a synchronized clock—not original event age.',
'integration.bounded_idempotent_retries':'Retry only contract-safe work; respect server delay and finite limits.',
'auth.object_authorization':'Bind object identity to trusted owner context and test cross-owner substitutions.',
'fastapi.production_security_documentation':'Document deployed bearer and issuer authority through real scoped dependencies.',
'fastapi.openapi_contract_inspection':'Compare generated contracts with behavior and audit safe, model-valid examples.',
'testing.api_authentication_authorization':'Keep real gates active and assert exact denial contracts and the authorized public projection.'}


CF={
'deployment.release_rollback_boundaries':['f4'],
'fastapi.documented_responses':['f2'],
'fastapi.safe_unexpected_errors':['f1','f3'],
'integration.upstream_failure_translation':['f1','f2'],
'integration.webhook_authenticity':['f1','f3'],
'observability.evidence_based_service_diagnosis':['f2'],
'security.bounded_api_resources':['f4'],
'sqlalchemy.redundant_queries':['f1'],
'testing.database_state_isolation':['f3','f4'],
'auth.authorization_server_integration':['f1','f4','f5'],
'auth.endpoint_permissions':['f1','f3'],
'fastapi_backend.webhook_delivery_idempotency':['f3'],
'fastapi_backend.webhook_replay_freshness':['f2','f4'],
'integration.bounded_idempotent_retries':['f1','f4'],
'auth.object_authorization':['f1'],
'fastapi.production_security_documentation':['f1','f3'],
'fastapi.openapi_contract_inspection':['f3'],
'testing.api_authentication_authorization':['f3','f4']}
TF={
'deployment.release_rollback_boundaries':['f1','f4'],
'fastapi.documented_responses':['f2','f4'],
'fastapi.safe_unexpected_errors':['f1','f3','f4'],
'integration.upstream_failure_translation':['f1','f3','f4','f5'],
'integration.webhook_authenticity':['f1','f2','f3'],
'observability.evidence_based_service_diagnosis':['f1','f2','f4'],
'security.bounded_api_resources':['f1','f4'],
'sqlalchemy.redundant_queries':['f2','f3','f4'],
'testing.database_state_isolation':['f3','f4'],
'auth.authorization_server_integration':['f1','f4','f5'],
'auth.endpoint_permissions':['f1','f3','f4'],
'fastapi_backend.webhook_delivery_idempotency':['f1','f2','f3'],
'fastapi_backend.webhook_replay_freshness':['f1','f2','f3'],
'integration.bounded_idempotent_retries':['f1','f2','f3'],
'auth.object_authorization':['f2','f3'],
'fastapi.production_security_documentation':['f1','f2','f4'],
'fastapi.openapi_contract_inspection':['f2','f3','f4'],
'testing.api_authentication_authorization':['f1','f5']}

out={'schema_version':plans['schema_version'],'kind':'screens_part','path_id':plans['path_id'],'batch_id':plans['batch_id'],'tiles':[]}
rem_map={}
for tile in plans['tiles']:
    tid=tile['tile_id'];cs=tile['concept_ids']
    o={'tile_id':tid,'title':' / '.join(T[c] for c in cs),'summary':' '.join(TAKE[c] for c in cs),'steps':[],'remediation_steps':[]}
    for s in tile['steps']:
        c=s['concept_ids'][0]
        lineage={'teaching_block_ids':copy.deepcopy(s['teaching_block_ids']),'fact_ids':copy.deepcopy(s['fact_ids']),'segment_ids':copy.deepcopy(s['segment_ids']),'anchors':copy.deepcopy(s['anchors'])}
        step={'step_id':s['step_id'],'type':s['type'],'concept_ids':copy.deepcopy(s['concept_ids']),'title':T[c],'eyebrow':{'explainer':'Understand','check':'Check your boundary','hands_on':'Apply it','video':'Trace the boundary','recap':'Keep the distinctions'}[s['type']],'lineage':lineage}
        if s['type']=='explainer':
            tbs=[v.split('#')[1] for v in s['teaching_block_ids']]
            if 'tb4' in tbs and 'tb2' not in tbs:
                text=W[c].format(**params(c));step['title']='Trace the fixture: '+T[c].lower()
                # Split into short idea-sized paragraphs, retaining exact fact meaning.
                sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z])',text)
                blocks=[];cur=[]
                for sent in sentences:
                    if len((' '.join(cur+[sent])).split())>90 and cur:
                        blocks.append(prose(' '.join(cur),c,[x.split('#')[1] for x in s['fact_ids']],tbs,'walkthrough'));cur=[]
                    cur.append(sent)
                if cur:blocks.append(prose(' '.join(cur),c,[x.split('#')[1] for x in s['fact_ids']],tbs,'walkthrough'))
                # Refine paragraph fact lineage below based on taught sentences.
                step['blocks']=blocks
            else:
                step['blocks']=[fact_prose(c,f['id'],tbs) for f in B[c]['coverage']['required_facts'] if c+'#'+f['id'] in s['fact_ids']]
            if s['planned_visual_block_type']:
                step['blocks']+=visual(c,s['planned_visual_block_type'])
        elif s['type']=='video':
            step['blocks']=[{'type':'media_group','segment_ids':copy.deepcopy(s['segment_ids'])}]
        elif s['type']=='check':
            step['title']='Choose the supported distinction'
        elif s['type']=='hands_on':
            step['title']='Apply the boundary in the registered fixture'
        elif s['type']=='recap':
            step['title']='Readiness takeaways'
            step['blocks']=[prose(TAKE[v],v,TF[v],[tb['id'] for tb in B[v]['teaching_blocks'] if set(tb['fact_ids']) & set(TF[v])],'takeaway') for v in cs]
            nxt=next((v for v in plans['tiles'] if v['tile_id']==tile['next_tile_id']),None)
            if nxt:step['blocks'].append({'type':'up_next','title':'Next: '+T[nxt['concept_ids'][0]],'text':'Continue with '+nxt['tile_id']+'.'})
            else:step['blocks'].append({'type':'up_next','title':'Path complete','text':'Review the readiness boundaries you have practiced.'})
        o['steps'].append(step)
    # One target per distinct measured fact set, including first hands-on when it measures different facts.
    seen={}
    for s in tile['steps']:
        if s['type'] not in ('check','hands_on'):continue
        for c in s['concept_ids']:
            fs=[v.split('#')[1] for v in s['fact_ids'] if v.split('#')[0]==c]
            if not fs:
                for a in s['anchors']:
                    if '#assessment:' in a:
                        cap=a.split('#assessment:')[1]
                        for anchor in B[c]['assessment_anchors']:
                            if anchor['capability']==cap:fs+=anchor['fact_ids']
                if not fs:fs=[v['id'] for v in B[c]['coverage']['required_facts']]
            fs=list(dict.fromkeys(fs));key=(c,tuple(fs))
            if key in seen:rem_map[s['step_id']]=seen[key];continue
            rid=tid+'.r'+str(len(o['remediation_steps'])+1).zfill(2);seen[key]=rid;rem_map[s['step_id']]=rid
            tbs=[v['id'] for v in B[c]['teaching_blocks'] if set(v['fact_ids'])&set(fs)]
            rem={'step_id':rid,'type':'remediation','required':False,'concept_ids':[c],'eyebrow':'Try the contrast','title':T[c],'lineage':lin(c,fs,tbs),'blocks':[prose(C[c],c,CF[c],[tb['id'] for tb in B[c]['teaching_blocks'] if set(tb['fact_ids']) & set(CF[c])],'misconception')]+[fact_prose(c,f) for f in fs]}
            # Same scenario, same datasets; no fabricated rows or result values.
            dataset={'deployment.release_rollback_boundaries':'ds.releases','observability.evidence_based_service_diagnosis':'ds.correlated_records','sqlalchemy.redundant_queries':'ds.relationship_attribute','fastapi_backend.webhook_delivery_idempotency':'ds.order_events','fastapi_backend.webhook_replay_freshness':'ds.delivery_timestamps','auth.object_authorization':'ds.orders','testing.api_authentication_authorization':'ds.authentication_test_matrix'}.get(c)
            if dataset:rem['blocks'].append(table(c,dataset,'Revisit the same fixture for this contrast'))
            else:
                # Keep remediation to one contrast in the same registered workspace.
                context = {'fastapi.documented_responses': 'Same order success/conflict fixture',
                    'fastapi.safe_unexpected_errors': 'Same controlled-failure fixture',
                    'integration.upstream_failure_translation': 'Same supplied remote status and timeout fixture',
                    'integration.webhook_authenticity': 'Same publisher-signed body fixture',
                    'security.bounded_api_resources': 'Same body and batch budget fixture',
                    'testing.database_state_isolation': 'Same isolated item database fixture',
                    'auth.authorization_server_integration': 'Same supplied issuer and registered client',
                    'auth.endpoint_permissions': 'Same protected order operation and verified credentials',
                    'integration.bounded_idempotent_retries': 'Same idempotent and non-idempotent operation fixture',
                    'fastapi.production_security_documentation': 'Same issuer and order-operation contract',
                    'fastapi.openapi_contract_inspection': 'Same orders router schema and HTTP evidence'}[c]
                rem['blocks'].append(diagram(c,[context,C[c]],context+': one boundary contrast.'))
            o['remediation_steps'].append(rem)
    out['tiles'].append(o)
(P/'screens.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(P/'working/screens_remediation_targets.json').write_text(json.dumps(rem_map,indent=2)+'\n')
print('Wrote',len(out['tiles']),'tiles;',sum(len(t['steps']) for t in out['tiles']),'planned steps;',sum(len(t['remediation_steps']) for t in out['tiles']),'remediation steps')
# Check words using the same text-block scope as the stage validator, plus each prose independently.
def iter_blocks(blocks):
    for b in blocks:
        yield b
        for k in ['left','right','before','after']:
            if isinstance(b.get(k),dict):yield from iter_blocks([b[k]])
for tile,o in zip(plans['tiles'],out['tiles']):
    for ps,s in zip(tile['steps'],o['steps']):
        count=sum(len(b.get('text','').split()) for b in iter_blocks(s.get('blocks',[])) if b['type']=='prose')
        if count>ps['word_budget'] and ps['type'] in ['explainer','recap']:print('OVER BUDGET',s['step_id'],count,ps['word_budget'])
    for s in o['steps']+o['remediation_steps']:
        for b in iter_blocks(s.get('blocks',[])):
            if b['type']=='prose' and len(b['text'].split())>90:print('LONG PROSE',s['step_id'])
