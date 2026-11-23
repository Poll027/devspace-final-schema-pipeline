import json, re, copy
from pathlib import Path
P=Path('batches/final_batch_readiness')
plan=json.loads((P/'tile_plans.json').read_text()); glossary=json.loads((P/'inputs/path_glossary_bundle.json').read_text()); registry=json.loads((P/'scenario_asset_registry.json').read_text())
B={b['context']['concept_id']:b for b in glossary['bundles']}; A={a['asset_id']:a for a in registry['assets']}
def source(c,path):
 return next(f['content'] for f in A['ws.'+c]['files'] if f['path']==path)
def fixture(c):return json.loads(source(c,'fixtures.json'))
# Each entry revoices one required fact, in the glossary's order.
F={
'deployment.release_rollback_boundaries':[
'Build makes the executable artifact. Release pairs it with deploy-specific configuration. Run starts processes from the selected release.',
'Each release has a unique, immutable identifier: changes create a new release, not edits to the running one.',
'Record each artifact/configuration pair. Rollback redeploys a known prior release with its intended configuration.',
'Before rollback, check compatibility with the current database schema. Replacing the application release does not reverse a migration.'],
'fastapi.documented_responses':[
'Declare known outcomes with responses={status: {"model": PublicModel, "description": ...}}, alongside response_model and status_code.',
'Metadata does not implement an outcome. Return the matching response or raise its expected exception.',
'Use response_description and outcome descriptions to explain what success and expected-error bodies mean to clients.',
'Compare generated status entries and schemas against real HTTP success and expected-error tests; document only bodies and statuses the endpoint emits.'],
'fastapi.safe_unexpected_errors':[
'Keep unexpected failures generic publicly: no stack traces, exception messages or implementation details.',
'Register a fallback exception handler returning stable generic JSON with status 500 while recording the exception internally.',
'Internal evidence needs the event, code location and interaction context, excluding prohibited secrets and sensitive data.',
'Disable production debug traceback responses: debug mode replaces the configured 500 handler with a traceback response.',
'Use TestClient(app, raise_server_exceptions=False) to assert the public response; inspect the safe internal record separately.'],
'integration.upstream_failure_translation':[
'HTTPX RequestError describes transport failure. HTTPStatusError comes from response.raise_for_status() on an unsuccessful HTTP status.',
'Call raise_for_status() when translating status failures. Classify HTTPStatusError using exc.response.status_code; catch RequestError when no usable response exists.',
'Map remote failures through an explicit local integration contract; do not blindly expose or trust the remote response.',
'For gateways, 502 means invalid upstream response and 504 means upstream timeout. Use the declared local mapping, not automatic status forwarding.',
'Test a supplied status failure and a transport failure. Assert the mapped local response or domain failure without raw upstream internals.'],
'integration.webhook_authenticity':[
'Acquire raw bytes with await request.body() before parsing or changing the body.',
'For every delivery, use the publisher-supported SDK or verifier with those bytes and the endpoint signing secret. Follow its signing format; invent no canonicalization.',
'Reject absent or invalid signatures before processing. Keep the secret and internal verification details out of responses.',
'Test valid, modified-body and missing-signature deliveries: only the valid signed delivery may reach processing.'],
'observability.evidence_based_service_diagnosis':[
'Compare request rate, failure fraction and latency for the same affected operation and window. Separate traffic growth from more failures or longer waits before choosing a boundary.',
'Trace the interaction identifier through local and outbound logs to the first recorded failure or delay; the final endpoint error need not identify its origin.',
'Compare integration timeouts and emitted database work with that request’s log context to separate upstream waiting, persistence work and local input rejection.',
'Reproduce the supplied failure with a controlled request. Record outcome and related evidence; change the suspected boundary only when evidence supports that location.'],
'security.bounded_api_resources':[
'Put finite limits on expensive untrusted work, including input size, result count, duration and costly concurrency.',
'Enforce actual body bytes with maintained middleware. Use Field bounds for caller-selected batch or page sizes; claimed sizes are insufficient.',
'Configure finite dependency timeouts and the supplied Uvicorn --limit-concurrency budget where policy bounds concurrent accepted work.',
'Test within-budget and over-budget input: reject excess before expensive work while preserving the accepted request’s contract.'],
'sqlalchemy.redundant_queries':[
'Lazy relationship access can emit extra SELECTs. Loading a relationship separately for each parent can produce N+1 queries.',
'Use statement.options(selectinload(Entity.relationship_attribute)) to fetch the selected parents’ collection with an additional batched query, not one per parent.',
'joinedload(...) instead uses a join. For collection loading, apply Result.unique() as required to deduplicate parents.',
'Compare emitted SQL before and after with engine echo=True; confirm fewer relationship queries and unchanged returned entity data.'],
'testing.database_state_isolation':[
'A yield fixture sets up before yield and tears down afterward, making cleanup explicit for its test scope.',
'Open an outer connection transaction; bind Session to that connection with join_transaction_mode="create_savepoint". Roll back the outer transaction during teardown.',
'Override the application session provider with the test provider. Write through TestClient and read resulting state across the same test database boundary.',
'Close session and connection, restore overrides, and verify a subsequent test does not inherit the earlier write.'],
'auth.authorization_server_integration':[
'Obtain an actually issued access token using the supplied established client or harness: authorization code with PKCE where applicable, never a resource-owner password endpoint.',
'Configure registered client ID, authorization/token endpoints and redirect URI. Complete the code redirect and separate token POST with the matching PKCE verifier.',
'Configure the existing verifier’s trusted JWKS URL, issuer, allowed algorithms and API audience. Resolve the key with PyJWKClient and require intended claims in jwt.decode.',
'Send the issued access token as Authorization: Bearer token to the protected endpoint, exercising real extraction and verification.',
'Assert HTTP acceptance for the valid issued token and rejection for tampering or wrong API audience. Keep verification active; neither override it nor fabricate locally valid tokens.'],
'auth.endpoint_permissions':[
'OAuth2 scopes express requested or granted operation permissions. Authentication alone does not establish every permission.',
'Declare Security(provider, scopes=[...]) on the operation. Accept SecurityScopes in the provider to read required scopes.',
'Compare every required scope with the verified token context; reject if any required scope is absent.',
'Test verified tokens with and without the required scope: only the sufficiently scoped request succeeds.'],
'fastapi_backend.webhook_delivery_idempotency':[
'Deduplicate on an authenticated publisher event ID; persist its record across restarts for the required replay window.',
'In one transaction, atomically record the event ID and durable state changes. A uniqueness constraint prevents concurrent deliveries from both applying the effect.',
'Acknowledge an already processed event successfully without changing state again. Test duplicate and concurrent deliveries separately.'],
'fastapi_backend.webhook_replay_freshness':[
'Freshness needs a provider-signature-authenticated delivery timestamp. Providers can refresh it and its signature on retries: it measures delivery freshness, not original event age. Unsigned time proves no authenticated freshness.',
'After signature verification, parse signed time and reject timestamps outside the configured window, including impermissibly future timestamps under provider policy.',
'Synchronize the receiver clock so clock drift does not distort the intended freshness window.',
'Test valid signatures with in-window, expired and impermissibly future timestamps: authentic does not necessarily mean fresh.'],
'integration.bounded_idempotent_retries':[
'Repeating non-idempotent requests can duplicate effects. Retry only when method or application contract establishes idempotency, or proves the original was not applied.',
'Retry-After may be an HTTP date or seconds of delay. Incorporate a valid supplied delay instead of immediately retrying against it.',
'Bound attempts and total time; use a maintained client’s bounded backoff where applicable so transient failures eventually stop.',
'Classify the supplied failure as retryable or terminal under the operation contract. A timeout or lost response alone does not prove no remote effect.',
'Test transient failure then success and repeated failures reaching the limit. Do not blindly repeat a non-idempotent operation lacking a retry-safe contract.'],
'auth.object_authorization':[
'Check permission for the specific requested object. A valid identifier plus an authenticated caller does not establish ownership.',
'Select by object identity and authorized owner or tenant context together. Do not trust a caller-supplied owner identifier.',
'Test distinct authorized contexts: each accesses its permitted object, but substituting the other context’s ID must neither obtain nor change that object.'],
'fastapi.production_security_documentation':[
'Use HTTPBearer to document deployed bearer-token presentation in securitySchemes, not to imply this API issues passwords or tokens.',
'For an established code issuer, configure OAuth2AuthorizationCodeBearer(authorizationUrl=..., tokenUrl=..., scopes=...) with supplied endpoints and permission descriptions.',
'Describe deployed authorization-code acquisition and PKCE where applicable. Do not guide production access through an OAuth2 password flow.',
'Attach schemes and required scopes through real operation dependencies so generated security requirements match accepted authority.',
'Inspect components.securitySchemes and protected operations’ security entries against the deployed issuer URLs, bearer presentation and required permissions.'],
'fastapi.openapi_contract_inspection':[
'Retrieve /openapi.json. Review router paths, parameters, request/response schemas and security requirements as public artifacts.',
'Compare requiredness, types, constraints and output fields with executable input/output behavior to find contract drift.',
'Compare success and expected-error statuses with exercised HTTP outcomes: declaring an additional response does not implement it.',
'Audit examples and descriptions for secrets and sensitive personal data. Validate examples against models rather than publishing realistic private values.',
'Check public security schemes and operation requirements against configured bearer presentation and established issuer contract; introduce no undeployed password grant.'],
'testing.api_authentication_authorization':[
'Exercise the real protected HTTP endpoint with absent, malformed and supplied bearer credentials; keep authentication and verification active.',
'Separate invalid-signature, expired and wrong-context tokens from a valid token. Assert credential rejection before protected output.',
'Compare a valid credential missing permission with a sufficiently permitted one to distinguish authentication from operation authorization.',
'Separately test a valid caller substituting another caller’s object ID; this is not the missing-operation-permission path.',
'Assert declared status and safe body for each denial, and the public projected result for full authorization—not just failure versus success.']}
C={
'deployment.release_rollback_boundaries':'An old artifact is not enough: the prior release needs its intended configuration and compatibility with today’s schema.',
'fastapi.documented_responses':'A documented conflict and an implemented conflict are different things. Compare the declared model and status with the actual HTTP case.',
'fastapi.safe_unexpected_errors':'A safe public failure and an actionable internal record are separate checks. Debug tracebacks cross the public boundary.',
'integration.upstream_failure_translation':'A remote status and a local outcome are separate decisions. A transport failure is not an unsuccessful HTTP response.',
'integration.webhook_authenticity':'Modified bytes must fail verification even when the body still parses. Verify first; process only the verified event.',
'observability.evidence_based_service_diagnosis':'The final endpoint error is an observation, not proof of origin. Follow correlated evidence before changing a boundary.',
'security.bounded_api_resources':'A bounded batch can still have an oversized body. Size, result count, duration and costly concurrency need their supplied limits.',
'sqlalchemy.redundant_queries':'Unchanged entity data does not prove unchanged database work. Check emitted SQL as well as the returned collections.',
'testing.database_state_isolation':'A successful write/read test is not isolation proof. The next test must start without the earlier write and with restored overrides.',
'auth.authorization_server_integration':'A fabricated valid token would bypass the acquisition evidence. Use the issued token and keep the API’s real verifier active.',
'auth.endpoint_permissions':'A verified token can still lack the operation’s required permission. Check every required scope, not just whether authentication succeeded.',
'fastapi_backend.webhook_delivery_idempotency':'Successful duplicate acknowledgment is not a second state change. Persistence and atomic uniqueness must also hold across restart and concurrent delivery.',
'fastapi_backend.webhook_replay_freshness':'A valid signature authenticates the timestamp, not its freshness. Retry timestamps also do not establish original event age.',
'integration.bounded_idempotent_retries':'A lost response leaves the remote effect uncertain. A retry budget limits repetition but does not make unsafe repetition idempotent.',
'auth.object_authorization':'Authentication and a real object ID are not enough. Selection must include the trusted context; substituting another owner’s ID must deny access.',
'fastapi.production_security_documentation':'Bearer presentation and issuer acquisition describe the same deployed authority. Documentation must not invent a password grant or replace enforcement.',
'fastapi.openapi_contract_inspection':'Generated documentation is public evidence to audit, not proof of runtime behavior. Check drift, sensitive examples and deployed security together.',
'testing.api_authentication_authorization':'One rejection plus one success leaves gates unproven. Separate credential rejection, missing permission and cross-object denial, then assert complete contracts.'}
# Primary prose covers the plan's assigned blocks; separate prose ideas by fact.
def lin(c, facts, tbs, anchors=()):return {'concept_ids':[c],'fact_ids':list(facts),'teaching_block_ids':list(tbs),'anchors':list(anchors)}
def fact_id(c,i):return c+'#'+B[c]['coverage']['required_facts'][i]['id']
def tbs_for(c,facts):
 return [c+'#'+t['id'] for t in B[c]['teaching_blocks'] if set(c+'#'+f for f in t['fact_ids']) & set(facts)]
def prose(c,text,facts,tbs,role='definition'):return {'type':'prose','text':text,'role':role,'lineage':lin(c,facts,tbs)}
def table(c,aid,caption=None):return {'type':'data_table','asset_ref':{'asset_id':aid,'columns':[x['name'] for x in A[aid]['columns']]},'caption':caption or A[aid]['title'],'lineage':lin(c,[c+'#'+f['id'] for f in B[c]['coverage']['required_facts']],tbs_for(c,[c+'#'+f['id'] for f in B[c]['coverage']['required_facts']]),[c+'#visual'])}
def code(c,text):return {'type':'code_walkthrough','language':'python','code':text,'reveal':'all','lineage':lin(c,[c+'#'+f['id'] for f in B[c]['coverage']['required_facts']],tbs_for(c,[c+'#'+f['id'] for f in B[c]['coverage']['required_facts']]),[c+'#visual'])}
def diagram(c,labels,title):
 return {'type':'diagram','diagram_kind':'container','title':title,'nodes':[{'id':'n'+str(i),'label':x} for i,x in enumerate(labels)],'alt_text':'; '.join(labels),'lineage':lin(c,[c+'#'+f['id'] for f in B[c]['coverage']['required_facts']],tbs_for(c,[c+'#'+f['id'] for f in B[c]['coverage']['required_facts']]),[c+'#visual'])}
def flow(c,labels,edges=None):
 return {'type':'process_flow','direction':'TB','nodes':[{'id':'n'+str(i),'label':x,'kind':'step'} for i,x in enumerate(labels)],'edges':edges or [{'from':'n'+str(i),'to':'n'+str(i+1)} for i in range(len(labels)-1)],'alt_text':'; '.join(labels),'lineage':lin(c,[c+'#'+f['id'] for f in B[c]['coverage']['required_facts']],tbs_for(c,[c+'#'+f['id'] for f in B[c]['coverage']['required_facts']]),[c+'#visual'])}
def pair(c,left,right,ll,rl,take):return {'type':'side_by_side','left':left,'right':right,'left_label':ll,'right_label':rl,'takeaway':take,'lineage':lin(c,[c+'#'+f['id'] for f in B[c]['coverage']['required_facts']],tbs_for(c,[c+'#'+f['id'] for f in B[c]['coverage']['required_facts']]),[c+'#visual'])}
V={}
c='deployment.release_rollback_boundaries'
rr=[dict(zip([x['name'] for x in A['ds.releases']['columns']],r)) for r in A['ds.releases']['rows']]
prior=next(r for r in rr if r['compatible'] and r['release_id']!=rr[0]['release_id'])
V[c]=flow(c,['Build → executable artifact','Release → artifact + deploy-specific configuration; unique immutable ID','Run → selected release’s processes','Rollback candidate: '+prior['release_id']+' / '+prior['artifact']+' / '+prior['configuration'],'Check current schema compatibility before selection','Compatible → redeploy intended prior release; database migration is not reversed','Incompatible → do not select'],[{'from':'n0','to':'n1'},{'from':'n1','to':'n2'},{'from':'n2','to':'n3'},{'from':'n3','to':'n4'},{'from':'n4','to':'n5','label':'compatible','kind':'yes'},{'from':'n4','to':'n6','label':'incompatible','kind':'no'}])
c='fastapi.documented_responses'
V[c]=pair(c,code(c,source(c,'starter.py')),code(c,'# Inspect declarations and exercise both outcomes; outputs are not authored.\nschema = app.openapi()\nresponses = schema["paths"]["/orders/{order_id}"]["get"]["responses"]\n# Compare status entries and body schemas with the supplied HTTP cases.\n'+source(c,'fixtures.json')),'Endpoint declarations and implementation','Supplied outcome contract / inspection','Declarations need matching HTTP behavior, models and descriptions.')
c='fastapi.safe_unexpected_errors';f=fixture(c)
# This is the authored fixture contract, not a computed HTTP result.
V[c]=pair(c,diagram(c,['Declared public status: '+str(f['public_status']),'Declared generic JSON: '+json.dumps(f['public_body']),'Exclude traces, exception messages and implementation details'],'Public response contract'),code(c,'\n'.join(source(c,'starter.py').splitlines()[4:8])),'Public boundary','Separate internal safe record','Inspect public response and internal diagnostics separately; keep production debug disabled.')
c='integration.upstream_failure_translation';f=fixture(c)
V[c]=flow(c,['Remote observation','Unsuccessful HTTP status → raise_for_status() → HTTPStatusError → exc.response.status_code','No usable response / timeout → RequestError','Apply supplied mapping: '+json.dumps(f),'Return local contract; exclude raw upstream internals'],[{'from':'n0','to':'n1','kind':'branch'},{'from':'n0','to':'n2','kind':'branch'},{'from':'n1','to':'n3'},{'from':'n2','to':'n3'},{'from':'n3','to':'n4'}])
c='integration.webhook_authenticity'
V[c]=code(c,'from fastapi import HTTPException\nimport stripe\nasync def webhook(request, signing_secret, publisher_verifier, signature_header, process_event):\n    raw_body = await request.body()\n    signature = request.headers.get(signature_header)\n    if not signature:\n        raise HTTPException(400, "Invalid signature")\n    try:\n        event = publisher_verifier(raw_body, signature, signing_secret)\n    except (ValueError, stripe.error.SignatureVerificationError):\n        raise HTTPException(400, "Invalid signature")\n    process_event(event)\n    return {"received": True}\n\n'+source(c,'test_delivery.py'))
c='observability.evidence_based_service_diagnosis'
V[c]=pair(c,table(c,'ds.operation_signals','Compare the same operation/window: rate, failure fraction and latency.'),table(c,'ds.correlated_records','Read chronologically within each interaction; locate first supported delay/failure before changing code.'),'Operation-window signals','Interaction-correlated timeline','Record observed outcome; corroborate the suspected boundary with a controlled request.')
c='security.bounded_api_resources';f=fixture(c)
budget=f['hypothetical_budgets']
V[c]=code(c,'# Supplied fictional budgets, not universal defaults\nbudgets = '+repr(budget)+'\n\n'+source(c,'starter.py')+'\n'+source(c,'application.py')+'\n'+source(c,'test_boundaries.py'))
V[c]['annotations']=[{'start_line':1,'end_line':2,'text':'Apply the supplied byte, batch, dependency timeout and concurrency limits; launch Uvicorn with its supplied --limit-concurrency budget.'}]
c='sqlalchemy.redundant_queries'
base=source(c,'starter.py');changed=base.replace('    # TODO: statement.options(selectinload(Entity.relationship_attribute))','    statement = statement.options(selectinload(Entity.relationship_attribute))')
V[c]=pair(c,code(c,base),code(c,changed),'Before: lazy per-parent access','After: batched collection loading','Capture emitted SQL in fresh sessions with echo=True; compare fewer relationship queries and identical entity data. Outputs belong to execution.')
c='testing.database_state_isolation'
s=source(c,'starter.py').replace('    # TODO: bind Session with join_transaction_mode="create_savepoint".\n    test_session = None','    test_session = Session(bind=connection, join_transaction_mode="create_savepoint")').replace('    # TODO: override session_provider with a yield provider using test_session.','    def test_provider():\n        yield test_session\n    app.dependency_overrides[session_provider] = test_provider').replace('        # TODO: close session, roll back outer transaction, close connection,\n        # restore original_overrides even if the test fails.\n        pass','        test_session.close()\n        outer_transaction.rollback()\n        connection.close()\n        app.dependency_overrides.clear()\n        app.dependency_overrides.update(original_overrides)')
tests=source(c,'test_items.py');tests=tests[tests.index('def test_writes_item'):]
V[c]=code(c,s+'\n# Tests use this fixture and the supplied item. Run both orders.\n'+tests)
c='auth.authorization_server_integration';f=fixture(c)
V[c]=flow(c,['Supplied registered client / endpoints / redirect: '+json.dumps(f),'Authorization redirect with PKCE where applicable','Separate token POST with matching verifier → issuer-issued access token','Protected HTTP endpoint: Authorization: Bearer token','PyJWKClient trusted JWKS key → jwt.decode checks issuer, allowed algorithms, audience and required claims','HTTP assertions: accept valid issued token; reject tampered or wrong-audience token; keep real verifier active'])
c='auth.endpoint_permissions'
s=source(c,'starter.py');s=s.replace('    # TODO: compare all security_scopes.scopes to verified_context[\'scopes\'].\n    # Deny missing permission with 403 {"detail":"Forbidden"}.\n    raise NotImplementedError(\'Complete permission comparison\')','    for required in security_scopes.scopes:\n        if required not in verified_context["scopes"]:\n            raise HTTPException(403, "Forbidden")\n    return verified_context')
V[c]=code(c,s+'\n'+source(c,'application.py').replace('context=Depends(verified_token_context)','context=Security(require_permissions, scopes=["orders:write"])')+'\n'+source(c,'test_permissions.py'))
c='fastapi_backend.webhook_delivery_idempotency'
V[c]=flow(c,['Delivery A: authenticated publisher event ID','Delivery B: same authenticated publisher event ID','Persistent uniqueness boundary (survives application restart)','One transaction: record ID atomically with durable order change','New ID → one committed effect','Already processed → successful duplicate acknowledgment, no repeated change'],[{'from':'n0','to':'n2'},{'from':'n1','to':'n2'},{'from':'n2','to':'n3'},{'from':'n3','to':'n4','label':'new','kind':'yes'},{'from':'n3','to':'n5','label':'duplicate','kind':'no'}])
c='fastapi_backend.webhook_replay_freshness'
V[c]={'type':'data_table','result_of':{'runtime':'sql','sql':'''SELECT case_id, signature_verified, signed_delivery_timestamp, receiver_now, CAST(signed_delivery_timestamp AS INTEGER)-receiver_now AS signed_time_difference, acceptance_window, future_tolerance, CASE WHEN signature_verified AND CAST(signed_delivery_timestamp AS INTEGER) BETWEEN receiver_now-acceptance_window AND receiver_now+future_tolerance THEN 'accept' ELSE 'reject' END AS delivery_freshness FROM deliveries''','asset_mounts':[{'asset_id':'ds.delivery_timestamps','mount_path':'deliveries'}]},'caption':'Supplied timestamp policy, including boundaries. Delivery freshness is not original event age; the receiver clock must be synchronized.','lineage':lin(c,[c+'#'+f['id'] for f in B[c]['coverage']['required_facts']],tbs_for(c,[c+'#'+f['id'] for f in B[c]['coverage']['required_facts']]),[c+'#visual'])}
c='integration.bounded_idempotent_retries'
V[c]=flow(c,['Permission to repeat: idempotent contract or proof original was not applied?','No → stop; lost response may hide an already-applied effect','Yes → classify supplied failure under operation contract','Terminal → stop','Retryable → honor valid Retry-After (date or seconds) and bounded backoff','Remaining finite attempts AND total time?','Yes → retry; transient success ends repetition','No → stop at limit'],[{'from':'n0','to':'n1','kind':'no'},{'from':'n0','to':'n2','kind':'yes'},{'from':'n2','to':'n3','label':'terminal'},{'from':'n2','to':'n4','label':'retryable'},{'from':'n4','to':'n5'},{'from':'n5','to':'n6','kind':'yes'},{'from':'n5','to':'n7','kind':'no'},{'from':'n6','to':'n2','kind':'loop_back','label':'another failure'}])
c='auth.object_authorization';f=fixture(c)
# Four supplied principal/order combinations are derived by query, not typed result rows.
owners=','.join("'"+x['owner_id']+"'" for x in f['principals']);ids=','.join(str(x['id']) for x in f['orders'])
V[c]={'type':'data_table','result_of':{'runtime':'sql','sql':f'''SELECT p.owner_id AS trusted_caller, o.id AS requested_order_id, CASE WHEN p.owner_id=o.owner_id THEN 'permitted public result' ELSE 'denied; no order data' END AS access_outcome FROM (SELECT DISTINCT owner_id FROM principals WHERE owner_id IN ({owners})) p CROSS JOIN orders o WHERE o.id IN ({ids}) ORDER BY p.owner_id,o.id''','asset_mounts':[{'asset_id':'ds.principals','mount_path':'principals'},{'asset_id':'ds.orders','mount_path':'orders'}]},'caption':'Four trusted-context retrieval combinations. The endpoint must also deny cross-context changes; never take ownership from caller input.','lineage':lin(c,[c+'#'+f['id'] for f in B[c]['coverage']['required_facts']],tbs_for(c,[c+'#'+f['id'] for f in B[c]['coverage']['required_facts']]),[c+'#visual'])}
c='fastapi.production_security_documentation';f=fixture(c)
V[c]=pair(c,diagram(c,['Supplied bearer presentation: '+json.dumps(f['bearer_scheme']),'Established acquisition: '+json.dumps(f['authorization_code_scheme']),'Operation dependencies: '+json.dumps(f['operation_requirements']),f['representation']],'Deployed training contract'),code(c,source(c,'starter.py')+'\n'+source(c,'dependencies.py')+'\n# Inspect app.openapi()["components"]["securitySchemes"] and operation security entries.'),'Supplied deployed contract','Declarations and enforcement dependencies','Compare issuer URLs and required permissions; document code/PKCE acquisition without an undeployed password flow.')
c='fastapi.openapi_contract_inspection'
V[c]=pair(c,code(c,source(c,'starter.py')+'\n# Review paths/parameters, requiredness/types/constraints, outputs, statuses, examples/descriptions and security.'),code(c,source(c,'models.py')+'\n'+source(c,'dependencies.py')+'\n# Compare against bundled exercised HTTP evidence; validate synthetic examples.'),'Generated contract inspection','Executable models and security configuration','Mark drift only after comparison; audit public examples for sensitive exposure. Additional response declarations do not prove HTTP outcomes.')
c='testing.api_authentication_authorization';V[c]=table(c,'ds.authentication_test_matrix','Supplied local endpoint contracts, not universal status defaults. Separate authentication, operation permission, object access and public-result assertions.')
# Build complete stage artifact from the immutable plan.
out={k:plan[k] for k in ['schema_version','path_id','batch_id']};out['kind']='screens_part';out['tiles']=[]
for tile in plan['tiles']:
 title=' / '.join(B[c]['context']['concept_name'] for c in tile['concept_ids'])
 t={'tile_id':tile['tile_id'],'title':title,'steps':[],'remediation_steps':[]}
 for ps in tile['steps']:
  c=ps['concept_ids'][0]
  st={'step_id':ps['step_id'],'type':ps['type'],'concept_ids':ps['concept_ids'],'title':B[c]['context']['concept_name'],'lineage':{k:copy.deepcopy(ps[k]) for k in ['teaching_block_ids','fact_ids','segment_ids','anchors']}}
  if ps['type']=='explainer':
   st['eyebrow']='Work the boundary' if any(x.endswith('#tb4') for x in ps['teaching_block_ids']) and not any(x.endswith('#tb1') for x in ps['teaching_block_ids']) else 'Learn the rule'
   st['blocks']=[]
   if st['eyebrow']=='Learn the rule':
    for i,text in enumerate(F[c]):
     fid=fact_id(c,i)
     if fid in ps['fact_ids']:st['blocks'].append(prose(c,text,[fid],[tb for tb in ps['teaching_block_ids'] if tb in tbs_for(c,[fid])]))
   else:
    # A focused worked contrast; prior explainer has already taught the full rule.
    st['title']='Keep the boundary clear'
    st['blocks']=[prose(c,C[c],[],ps['teaching_block_ids'],'walkthrough')]
    # Attribute only the facts actually expressed in this contrast.
    contrast_facts={
     'deployment.release_rollback_boundaries':[2,3], 'integration.webhook_authenticity':[2,3], 'fastapi.safe_unexpected_errors':[0,2,3], 'integration.upstream_failure_translation':[0,2,3],
     'observability.evidence_based_service_diagnosis':[1,3], 'security.bounded_api_resources':[0,1], 'sqlalchemy.redundant_queries':[3],
     'testing.database_state_isolation':[3], 'auth.authorization_server_integration':[0,3,4], 'auth.endpoint_permissions':[0,2],
     'fastapi_backend.webhook_delivery_idempotency':[0,1,2], 'fastapi_backend.webhook_replay_freshness':[0,1,3],
     'integration.bounded_idempotent_retries':[0,2,3], 'fastapi.production_security_documentation':[2,3],
     'fastapi.openapi_contract_inspection':[1,3,4], 'testing.api_authentication_authorization':[1,2,3,4]}
    st['blocks'][0]['lineage']['fact_ids']=[fact_id(c,i) for i in contrast_facts.get(c,[])]
   if ps['planned_visual_block_type']:st['blocks'].append(copy.deepcopy(V[c]))
  elif ps['type']=='video':st['blocks']=[{'type':'media_group','segment_ids':ps['segment_ids']}]
  elif ps['type'] in ('check','hands_on'):
   st['title']='Choose the boundary' if ps['type']=='check' else 'Apply the contract'
   st['eyebrow']='Check' if ps['type']=='check' else 'Practice'
  elif ps['type']=='recap':
   st['title']='Take the rule with you';st['blocks']=[]
   for cc in tile['concept_ids']:
    st['blocks'].append(prose(cc,C[cc],[cc+'#'+f for f in B[cc]['teaching_blocks'][-1]['fact_ids']],[cc+'#'+B[cc]['teaching_blocks'][-1]['id']],'takeaway'))
   nxt=tile['next_tile_id']
   if nxt:
    nt=next(x for x in plan['tiles'] if x['tile_id']==nxt);nc=nt['concept_ids'][0]
    st['blocks'].append({'type':'up_next','title':B[nc]['context']['concept_name'],'text':B[nc]['teaching_blocks'][0]['content']})
  t['steps'].append(st)
 # One remediation per distinct measured-fact set, in planned encounter order.
 seen=set()
 for ps in tile['steps']:
  if ps['type'] not in ('check','hands_on'):continue
  key=tuple(ps['fact_ids'])
  if key in seen:continue
  seen.add(key);c=ps['concept_ids'][0];facts=ps['fact_ids'] or [c+'#'+f['id'] for f in B[c]['coverage']['required_facts']];tb=tbs_for(c,facts)
  r={'step_id':tile['tile_id']+'.r'+str(len(t['remediation_steps'])+1).zfill(2),'type':'remediation','title':'Review: '+B[c]['context']['concept_name'],'concept_ids':ps['concept_ids'],'lineage':lin(c,facts,tb),'blocks':[]}
  for i,text in enumerate(F[c]):
   fid=fact_id(c,i)
   if fid in facts:r['blocks'].append(prose(c,text,[fid],tbs_for(c,[fid])))
  r['blocks'].append(prose(c,C[c],facts,tb,'misconception'))
  # Keep the same registered scenario; a fixture selection uses references, never inline output.
  aid={'deployment.release_rollback_boundaries':'ds.releases','observability.evidence_based_service_diagnosis':'ds.correlated_records','sqlalchemy.redundant_queries':'ds.Entity','fastapi_backend.webhook_delivery_idempotency':'ds.order_events','fastapi_backend.webhook_replay_freshness':'ds.delivery_timestamps','auth.object_authorization':'ds.orders','testing.api_authentication_authorization':'ds.authentication_test_matrix'}.get(c)
  if aid:r['blocks'].append(table(c,aid))
  t['remediation_steps'].append(r)
 out['tiles'].append(t)
(P/'screens.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('tiles',len(out['tiles']),'planned steps',sum(len(t['steps']) for t in out['tiles']),'remediation steps',sum(len(t['remediation_steps']) for t in out['tiles']))
