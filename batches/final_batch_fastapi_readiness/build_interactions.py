import json, sys, copy
from pathlib import Path
B=Path('batches/final_batch_readiness')
sys.path.insert(0,str(Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
from checkers import sandbox
P=json.loads((B/'tile_plans.json').read_text()); S=json.loads((B/'screens.json').read_text()); G=json.loads((B/'inputs/path_glossary_bundle.json').read_text()); R=json.loads((B/'scenario_asset_registry.json').read_text())
bs={b['context']['concept_id']:b for b in G['bundles']}; assets={a['asset_id']:a for a in R['assets']}
def files(c):return {f['path']:f['content'] for f in assets['ws.'+c]['files']}
def fixture(c):return json.loads(files(c)['fixtures.json'])
def rows(a):
 d=assets[a];return [dict(zip([c['name'] for c in d['columns']],r)) for r in d['rows']]
Q={}
def q(s,p,a,b,c,why_b,why_c):Q[s]=(p,[a,b,c],[None,why_b,why_c])
q('tile_082.s03','A known prior release is compatible with the current database schema. Which rollback selection respects the release record?', 'Redeploy its recorded artifact with its intended configuration; leave the database schema unchanged.', 'Redeploy the old artifact with the current release configuration without checking the pair.', 'Edit the running release record and assume its database migration is undone.', 'A rollback selects the recorded artifact/configuration pair, not an unverified mixed pair.', 'Release records are immutable, and application rollback does not reverse migrations.')
q('tile_083.s02','An endpoint declares a 409 public conflict model in responses, but its exercised conflict branch returns 200 with the success body. What does this demonstrate?', 'Documentation and actual conflict behavior disagree; the declaration alone does not emit 409.', 'The responses declaration automatically converts the branch into 409.', 'A description is enough to make the emitted body match the public conflict model.', 'Additional response declarations document outcomes; the handler still must emit them.', 'Descriptions explain bodies; they do not change HTTP status or returned bodies.')
q('tile_083.s05','A production controlled-failure route exposes a traceback even though a generic 500 handler is configured. debug=True is set. Which change addresses this disclosure?', 'Disable debug traceback responses and keep the stable generic 500 handler.', 'Keep debug=True because the fallback always takes precedence.', 'Return the exception message as the generic public detail.', 'Debug mode substitutes traceback responses for the configured handler.', 'Unexpected exception messages are implementation details, not generic public information.')
q('tile_083.s06','Which paired check correctly separates a fallback error response from its internal diagnostic record?', 'Assert the exact generic 500 body publicly; separately inspect an internal record for event, code location and interaction context without sensitive fields.', 'Assert that the public body includes code location and the exception message.', 'Only check status 500; put request credentials in the internal record.', 'Public unexpected-error information must not expose implementation details or exception messages.', 'Status alone misses disclosure; internal records must omit prohibited secrets and sensitive data.')
q('tile_085.s03','The local gateway contract maps an upstream 503 to 502 with a fixed public detail and an upstream timeout to 504 with another fixed detail. Which translation follows that contract?', 'Translate the unsuccessful status and timeout separately into those local outcomes.', 'Forward upstream 503 and its raw body as the local outcome.', 'Return 502 for both, ignoring the declared timeout mapping.', 'Remote failures are inputs to an explicit local contract; blind forwarding does not follow this mapping.', 'The supplied local mapping distinguishes timeout from an unsuccessful upstream status.')
q('tile_085.s04','Which test pair establishes safe upstream-failure translation?', 'Exercise upstream 503 and a transport timeout separately; assert each mapped local status and exact fixed public body.', 'Exercise only 503 and assert any non-200 status.', 'Exercise both but assert their raw upstream exception messages publicly.', 'One broad status assertion does not verify both declared mappings or safe output.', 'Public outcomes must not disclose raw upstream internals.')
q('tile_086.s03','A valid signed delivery is copied, but its raw body bytes are modified while the signature is unchanged. What must the webhook do before processing?', 'Reject the signature failure without exposing secrets or verification internals.', 'Process it because an earlier copy had a valid signature.', 'Process it if its parsed JSON still contains an event identifier.', 'Every delivery must be verified against its own raw bytes.', 'An event identifier does not establish authenticity; failed verification must prevent processing.')
q('tile_087.s03','Synthetic evidence for one interaction records an accepted input, a small completed database operation, then a long outbound wait ending in a timeout before the final endpoint error. Which boundary is supported for investigation?', 'The upstream wait, traced by the same interaction identifier.', 'Persistence, solely because the endpoint accesses a database.', 'Local input rejection, solely because the final endpoint response is an error.', 'Completed small database work does not locate this recorded wait in persistence.', 'The packet records accepted input; the final response alone does not identify the origin.')
q('tile_088.s03','A batch endpoint trusts Content-Length and accepts any caller-selected batch count before invoking an expensive dependency. Which policy actually bounds that input work?', 'Enforce actual body bytes with maintained middleware and bound batch size with Field constraints.', 'Accept the claimed Content-Length as proof of actual size and leave batch count unbounded.', 'Only describe a recommended batch size in documentation.', 'Claimed sizes are not enforced actual-byte limits, and an unbounded batch still permits expensive work.', 'A recommendation does not enforce finite limits on untrusted operations.')
q('tile_088.s04','Which observation demonstrates rejection before expensive work?', 'An in-budget request keeps its intended response; oversized body and excessive batch requests are rejected with zero dependency invocations.', 'Oversized requests eventually return an error after invoking the dependency.', 'All requests return the intended response, including those over budget.', 'Rejection after invocation does not demonstrate prevention of expensive work.', 'Accepting excess inputs fails to enforce the supplied budgets.')
q('tile_089.s04','A listing lazily accesses each selected parent collection, emitting one relationship SELECT per parent. Which change batches collection loading?', 'Apply statement.options(selectinload(Entity.relationship_attribute)).', 'Keep lazy access and describe each SELECT as a batched query.', 'Remove the collection contents from the returned result.', 'One SELECT per parent is the per-parent pattern, not batched loading.', 'Removing required data changes the listing rather than preserving it while reducing queries.')
q('tile_089.s05','What evidence verifies the relationship-loading improvement?', 'Compare echo SQL in fresh sessions before and after; confirm fewer relationship SELECTs and identical parent/collection results.', 'Run twice in one session with already-loaded relationships and only compare elapsed time.', 'Count fewer SELECTs after deleting parents from the listing.', 'Already-loaded relationships can hide queries; elapsed time alone does not verify the loading change.', 'Changing returned entities is not the required unchanged-data improvement.')
q('tile_090.s04','A yield fixture binds its session to an outer connection transaction and saves overrides, but teardown only closes the session. What is missing?', 'Roll back the outer transaction, close the connection and restore the saved overrides.', 'Commit the outer transaction so later tests inherit the write.', 'Leave overrides installed because the session has closed.', 'Committing preserves state instead of isolating the subsequent test.', 'Closing a session does not restore dependency overrides or close its connection boundary.')
q('tile_090.s05','The write test reads its committed API write through the test session. A separate initially-empty test inherits that row when run second. What conclusion is supported?', 'State isolation is broken; verify outer rollback and teardown and run both test orders.', 'The inherited row proves both tests are isolated.', 'Reading the write in its own test is itself forbidden.', 'Isolation requires a subsequent test not to inherit the first test write.', 'The writing test must observe its own resulting state through the same boundary.')
q('tile_091.s04','Which pair proves integration with the established issuer rather than merely a local token fixture?', 'Send an actual issuer-issued access token to the real protected endpoint, then a tampered token or issuer token for the wrong audience, keeping extraction and verification active.', 'Override verification and pass a fabricated token through the route.', 'Decode a locally signed token in a helper without sending an HTTP request.', 'Authentication overrides bypass the authority whose integration is being tested.', 'A helper-only local-token check does not prove issuer-issued credentials work through the protected HTTP gates.')
q('tile_091.s08','Two verified credentials differ only in the required operation scope. Which test establishes endpoint permission enforcement?', 'The sufficiently scoped request succeeds; the otherwise valid insufficient-scope request is denied without protected output.', 'Both succeed because signature verification grants operation permission.', 'Reject only a malformed token and assume scope enforcement follows.', 'Authentication establishes a verified credential, not every operation permission.', 'Malformed-token rejection checks authentication rather than the insufficient-permission path.')
q('tile_093.s03','An authenticated event was committed, then the application restarts with its event-record database retained. The same publisher event identifier arrives again. What effect is required?', 'Confirm the persistent processed-event record and acknowledge without another committed order change.', 'Apply the change again because process memory is empty.', 'Treat any database integrity error as proof this event was processed.', 'Restart does not erase the persistent event identity used for deduplication.', 'Only a confirmed duplicate identity justifies successful duplicate acknowledgment; unrelated integrity failures do not.')
q('tile_093.s07','A signed delivery timestamp is compared with receiver_now. Why must the receiver clock be synchronized accurately?', 'Clock error can distort the computed past age or future offset and thus the freshness decision.', 'A valid signature automatically synchronizes the receiver clock.', 'Freshness proves when the original business event occurred regardless of delivery time.', 'Signature authenticity does not establish receiver clock accuracy.', 'The check concerns signed delivery-timestamp freshness, not original event age.')
q('tile_093.s08','Under an inclusive policy of 300 seconds past age and 30 seconds future tolerance, what should tests of already-authenticated deliveries establish?', 'Accept 60 seconds behind; reject 301 seconds behind and 31 seconds ahead; accept both exact policy boundaries.', 'Accept every signed timestamp because authenticity implies freshness.', 'Reject all future timestamps, including the permitted future boundary.', 'Authenticity is established before a separate freshness decision.', 'The supplied future tolerance explicitly permits the inclusive future boundary.')
q('tile_093.s12','Which supplied retry-check outcome meets a bounded retry-safe contract?', 'A permitted transient failure can reach success, repeated failure stops at finite limits, and an unsafe non-idempotent lost response gets no blind retry.', 'Retry every timeout indefinitely because it proves the remote operation had no effect.', 'Retry an unsafe POST just like an idempotent GET whenever the response is lost.', 'A timeout does not prove lack of remote effect, and finite limits are required.', 'A lost response alone does not authorize repetition of a non-idempotent operation.')
q('tile_096.s02','The protected order lookup selects only Order.id even though a trusted principal supplies owner_id. What permits cross-owner disclosure?', 'The query lacks the trusted owner-identity predicate.', 'Using the trusted owner-identity predicate prevents the caller retrieving any own order.', 'The request identifier alone proves the caller owns the order.', 'Selecting by both identities allows the trusted principal to retrieve its own order.', 'An object identifier is not evidence of ownership or authorization.')
q('tile_096.s03','Which request matrix verifies the object boundary for two trusted contexts with distinct orders?', 'Both own-order requests succeed, both cross-owner requests return unavailable without order data, and caller owner input cannot override the trusted owner.', 'Only one own-order request succeeds; no cross-owner case is sent.', 'Caller-supplied owner_id can switch which owner the query trusts.', 'Own-order success alone does not verify cross-owner isolation.', 'The owner must come from the trusted principal, not caller-controlled ownership input.')
q('tile_097.s03','What does a deployed HTTPBearer security scheme describe in OpenAPI?', 'Bearer-token presentation to the API, not a password or token issuing endpoint.', 'A password grant implemented automatically by the API.', 'Proof that every bearer string is authorized for every operation.', 'HTTPBearer describes token presentation; it does not establish a password grant.', 'Security documentation must agree with real operation authority; bearer presentation is not universal permission.')
q('tile_097.s04','A protected operation enforces orders:read through its real dependencies. Its generated security entry requires no scope. What should be checked?', 'Compare generated operation requirements with the existing dependencies and required permissions, and correct the mismatch.', 'Accept the mismatch because a securitySchemes entry alone proves scope agreement.', 'Remove actual scope enforcement solely to fit the empty declaration.', 'A scheme entry alone does not establish agreement at the protected operation.', 'The declaration must describe deployed authority, not erase its required permission.')
q('tile_097.s08','The deployed contract uses bearer tokens acquired from an established authorization-code issuer. The public security description advertises a password grant on this API. What is the audit finding?', 'The public acquisition/security declaration differs from the deployed contract.', 'The description proves that a password endpoint has been deployed.', 'The acquisition description is irrelevant to the public security audit.', 'Public declarations are contract artifacts, not proof an undeployed outcome exists.', 'The audit includes security requirements and their agreement with the configured bearer and issuer contract.')
q('tile_097.s12','Which assertion set checks a protected order endpoint completely?', 'Assert exact declared status and safe body for each separate denial, and exact public projection for fully authorized success.', 'Assert only that invalid requests fail and a valid request succeeds.', 'Accept a denial body containing the protected order if its status is non-200.', 'Coarse pass/fail does not verify declared denial bodies or public output.', 'Denied requests must return safe bodies without protected output.')

# Inspect-and-judge: all excerpts are hypothetical review candidates, never claimed runtime observations.
C={}
def classify(c,p,items):C[c]=(p,items)
classify('fastapi.documented_responses','Review each candidate independently. Accept only documentation plus assertions that match the supplied success and conflict contracts.',[
 ('good',"@app.post('/orders', response_model=PublicModel, status_code=200,\n response_description='Public created order',\n responses={409: {'model': ConflictModel, 'description': 'Order conflict'}})\n# Handler: success returns public order; conflict raises HTTPException(409, 'Order conflict').\n# Review assertions: success status/body match PublicModel; conflict status/body match ConflictModel; generated 200 and 409 schemas and descriptions match both HTTP cases.",'The declaration includes models and descriptions and compares generated entries with actual outcomes.'),
 ('bad',"@app.post('/orders', response_model=PublicModel, status_code=200,\n responses={409: {'description': 'Order conflict'}})\n# Conflict handler returns the success body with 200.\n# Reviewer checks only that '409' appears in app.openapi().",'A status declaration does not emit the conflict outcome; its model and meaningful success description are missing, and the checks do not compare the emitted contract.')])
classify('fastapi.safe_unexpected_errors','Judge whether each fallback and verification packet meets both the generic public response and safe internal evidence requirements.',[
 ('good',"app = FastAPI(debug=False)\n@app.exception_handler(Exception)\nasync def fallback(request, exc):\n    record_safe_failure(request)  # event, code_location, interaction_context only\n    return JSONResponse(status_code=500, content={'detail':'Internal server error'})\n# Controlled failure HTTP check uses TestClient(app, raise_server_exceptions=False).\n# Assert exact 500 generic JSON; separately inspect event/location/context and absence of exception_message, locals, request_body and credentials.",'Public output remains generic while the diagnostic check is separate and safe.'),
 ('bad',"app = FastAPI(debug=True)\n@app.exception_handler(Exception)\nasync def fallback(request, exc):\n    safe_records.append({'credentials': request.headers.get('Authorization')})\n    return JSONResponse(status_code=500, content={'detail':str(exc)})\n# Only assertion: response.status_code == 500",'Debug tracebacks, exception details and credentials violate the public/internal boundary; status-only checking misses those leaks.')])
classify('integration.webhook_authenticity','Review candidate webhook gates and their test coverage. Accept only a gate where valid signatures reach processing and modified/absent-signature deliveries cannot.',[
 ('good',"raw_body = await request.body()\nsignature = request.headers.get(signature_header)\n# Reject absent signature with fixed 400 {'detail':'Invalid signature'}.\n# publisher_verifier is the supplied publisher-supported SDK verifier.\n# Call publisher_verifier(raw_body, signature, signing_secret); on its documented verification failure return the same fixed 400.\n# Only the verified event reaches process_event.\n# Separate HTTP tests: valid signed body -> processed once; modified bytes with original signature -> rejected, zero calls; absent signature -> rejected, zero calls. Each rejection asserts exact safe body without secret or verifier details.",'The supported verifier consumes unmodified bytes, gates processing, and the tests cover all three required deliveries.'),
 ('bad',"event = await request.json()\nraw_body = json.dumps(event).encode()\nprocess_event(event)\n# Verify reconstructed bytes afterward. On failure return str(exc).\n# Test only a valid signature.",'Reconstruction changes the signing input, processing occurs before verification, error details are disclosed and failure tests are absent.')])
classify('security.bounded_api_resources','Review enforcement packets against the supplied finite body, batch, timeout and concurrency budgets. Each packet is independent.',[
 ('good',"# Maintained middleware enforces actual received body bytes <= supplied_body_budget.\n# Batch model: Field(ge=1, le=supplied_batch_budget).\n# HTTP dependency uses httpx.Timeout(supplied_timeout).\n# Launch setting: uvicorn ... --limit-concurrency <supplied_concurrency_budget>.\n# Checks: in-budget input retains exact endpoint response; oversized actual body -> rejected with dependency calls == 0; excessive batch -> rejected with dependency calls == 0. Settings compared to supplied finite budgets.",'Actual size, selected count, dependency duration and accepted concurrency are bounded; excess work is rejected before invocation.'),
 ('bad',"# Reject only if claimed Content-Length exceeds the body budget.\n# Batch count has no Field upper bound.\n# Dependency timeout=None; Uvicorn concurrency budget omitted.\n# Invoke dependency then check whether the batch was excessive.\n# Assert only that some error occurred.",'Claimed sizes and post-work checks are not enforced early budgets; duration and concurrency remain unbounded.')])
classify('testing.database_state_isolation','Judge complete transaction-isolation fixtures and checks. Accept only a packet that isolates the actual API database and restores every resource/override.',[
 ('good',"connection = engine.connect()\ntransaction = connection.begin()\nsession = Session(bind=connection, join_transaction_mode='create_savepoint')\nsaved_overrides = app.dependency_overrides.copy()\napp.dependency_overrides[session_provider] = test_session_provider\ntry:\n    yield session\nfinally:\n    session.close()\n    transaction.rollback()\n    connection.close()\n    app.dependency_overrides.clear()\n    app.dependency_overrides.update(saved_overrides)\n# Writer uses TestClient to write then reads through this session.\n# Empty-state test does not inherit that write. Run each ordering with fresh fixtures; both checks pass.",'The HTTP write and read share the test connection boundary, and teardown restores all resources and overrides.'),
 ('bad',"test_session = Session(engine)\n# Application session_provider is not overridden.\nyield test_session\ntest_session.close()\n# Writer calls the API, then checks a different session. No outer rollback or override restoration. Empty test relies on running first.",'The API can write outside the test boundary; teardown and execution-order independence are not established.')])
classify('auth.authorization_server_integration','These are integration-test candidates, not claims of executed tests. Accept only the candidate that uses the supplied issuer/client contract through active HTTP security gates.',[
 ('good',"# Supplied registered client identifier, authorization endpoint, token endpoint and redirect URI come unchanged from issuer configuration.\n# Supplied maintained client completes code redirect then separate token POST with the matching PKCE verifier, obtaining an actual issuer-issued access token.\n# Existing verifier: trusted supplied JWKS URL via PyJWKClient; jwt.decode requires intended claims with supplied issuer, API audience and allowed algorithms.\n# Test 1 sends that access token as Authorization: Bearer to the protected endpoint and asserts authorized public output.\n# Test 2 sends a tampered token and asserts credential rejection without protected output. No extraction/verification overrides; no locally minted valid token or password-grant route.",'Both HTTP tests exercise the real issuer-configured extraction and verification, with genuine acquisition rather than local fabrication.'),
 ('bad',"app.dependency_overrides[verified_token_context] = lambda: {'subject':'caller_a'}\n# Locally fabricate a token and send it to the endpoint.\n# Accepting the request is reported as issuer integration.\n# No tampered or wrong-audience case is sent.",'The override bypasses the issuer verifier; local fabrication and missing rejection testing cannot establish issuer integration.')])
classify('auth.endpoint_permissions','Judge operation-permission gates and test packets for an already verified token context.',[
 ('good',"# Security dependency receives declared required scopes and the verified token context.\n# Deny when a required operation scope is absent; return the trusted context only after the check.\n# GET /orders requires orders:read.\n# Separate HTTP cases: otherwise valid context with orders:read -> exact public success; otherwise valid context without orders:read -> exact safe permission denial and no protected output.",'Permission is checked against the verified context and sufficient/insufficient cases isolate operation authorization.'),
 ('bad',"# GET /orders declares orders:read in documentation but checks only token signature.\n# An otherwise valid context with no required scope reaches the handler.\n# The only negative test uses a malformed bearer token.",'A declaration alone does not enforce permission, and malformed-token rejection does not test a valid insufficient-scope credential.')])
classify('fastapi.production_security_documentation','Review security documentation proposals against the supplied deployed bearer and authorization-code/PKCE contract. Names below refer to supplied configuration, not invented issuer URLs.',[
 ('good',"bearer = HTTPBearer()\nissuer_scheme = OAuth2AuthorizationCodeBearer(\n authorizationUrl=supplied_authorization_url, tokenUrl=supplied_token_url,\n scopes=supplied_permission_descriptions)\n# Existing protected-operation dependencies attach the scheme and required orders:read scope.\n# Generated components.securitySchemes checked against supplied issuer URLs and bearer presentation; GET /orders security entry checked for its deployed scheme and orders:read requirement.\n# Acquisition description: established authorization-code client uses PKCE; no password-flow guidance.",'Schemes, operation requirements and acquisition guidance agree with deployed authority.'),
 ('bad',"# OpenAPI proposal adds an OAuth2 password flow on this API.\n# GET /orders security entry omits orders:read although the real operation requires it.\n# Reviewer inspects only components.securitySchemes, not protected operation entries.",'The undeployed password flow misrepresents acquisition, and operation requirements do not match their authority.')])
classify('fastapi.openapi_contract_inspection','Classify each audit finding as supported or unsupported by the quoted hypothetical evidence. Declarations must be distinguished from exercised behavior; examine every packet.',[
 ('good',"# GET /openapi.json audit inventory covers router paths, path/query parameters, request/response schemas and operation security.\n# Finding: an input declared required integer with supplied bounds is accepted without that field in the exercised request; requiredness drifts.\n# Compare types, constraints and output fields with executable cases, not only schema text.\n# Finding: declared 409 ConflictModel branch instead emits 200 success in its HTTP test. A declaration did not prove emission.",'The findings compare declarations with behavior and include paths/parameters and both input/output contract boundaries.'),
 ('good',"# Public examples/descriptions audit: a required integer is shown as a nonnumeric string and fails supplied model validation; an example includes a credential field. Flag invalid example and sensitive publication.\n# Security audit: deployed contract is supplied bearer plus established authorization-code issuer, but public guidance introduces a password grant on this API. Flag scheme/acquisition mismatch and compare every protected operation requirement.",'Invalid examples, sensitive publication and mismatched acquisition declarations are in scope for this audit.'),
 ('bad',"# /openapi.json lists 409, therefore the endpoint certainly emitted 409 without running its conflict case.\n# Public example contains a credential, but documentation need not be audited for sensitive values.\n# Ignore operation security requirements.",'A status declaration is not an exercised outcome; sensitive examples and operation security remain audit obligations.')])
classify('testing.api_authentication_authorization','Judge test designs for the supplied protected order endpoint. Accept only tests that keep authentication active and assert complete isolated denial/success contracts.',[
 ('good',"# No overrides of extraction, verification, operation permission or object lookup.\n# Separate actual HTTP requests with controlled fixtures: absent, malformed, invalid_signature, expired, wrong_issuer, wrong_audience; each asserts its exact declared rejection status and safe JSON without order data.\n# Otherwise valid credential lacking orders:read: independent operation-denial status/body check.\n# Valid sufficiently scoped caller asking for other caller order: independent object-denial status/body check.\n# Fully authorized own-order request: exact declared success status and public {id,status} projection. Credentials generated by supplied controlled harness, not row labels passed as bearer tokens.",'The distinct credential, permission and object denials are independently exercised through active gates and checked for complete safe contracts.'),
 ('bad',"app.dependency_overrides[verified_token_context] = lambda: trusted_context\n# Only two requests: one returns an error; one succeeds.\nassert bad.status_code != 200\nassert good.status_code == 200\n# No exact safe denial bodies or projected success body; no separate permission or cross-object cases.",'The override bypasses credential verification; coarse statuses and missing isolated deny paths do not meet the response-contract requirements.')])
# Registry-derived synthetic diagnosis packet, explicitly not measured SQL/latency.
f=fixture('observability.evidence_based_service_diagnosis')
signal_view=[dict(window=x['window'],rate=x['request_count']/x['window_seconds'],failure_fraction=x['failure_count']/x['request_count'],latency_ms=x['latency_ms']) for x in f['signals']]
classify('observability.evidence_based_service_diagnosis','Review independent investigation candidates. The timing/count packet is authored synthetic evidence, not measurements from the controlled reproduction. Accept a candidate only when it records reproduction separately and supports its chosen boundary.',[
 ('good','Synthetic operation-window comparison: '+json.dumps(signal_view)+'\nSynthetic correlated records: '+json.dumps(f['records'])+"\nwith client() as http:\n    response = http.post('/orders', json=packet['failing_order_payload'])\n    controlled_outcome = {'status':response.status_code, 'body':response.json(), 'interaction':response.headers[packet['interaction_header']]}\n    reproduction_evidence = list(runtime_evidence)\n# Compare the reproduced timeout control-flow and interaction to the packet, label its simulated database boundary.\n# Rate unchanged, failure fraction and latency increased in synthetic packet; completed database lookup precedes outbound delay/timeout. Investigate upstream waiting, not final local response. Keep proposed timeout-boundary change separate from observations.",'The investigation records a controlled HTTP outcome and control-flow separately, compares all operation signals and traces the first delay to outbound work.'),
 ('bad',"# Read only the final local response error in the packet.\nsuspected_boundary = 'database'\nproposed_change = 'change persistence immediately'\n# Do not execute controlled request, inspect correlation, compare operation windows or examine upstream timeout.",'The selected boundary lacks correlated support, the controlled reproduction is missing and the proposed change is not separated from observed evidence.')])

E={}
def exercise(c,p,scaffold,starter,solution,tests,packages):
 E[c]=(p,scaffold+starter,scaffold+solution,tests,packages)
def v(t,expr):return {'test_id':t,'kind':'value_equals','spec':{'expr':expr}}
def h(t,requests,keys=('status','json')):return {'test_id':t,'kind':'http_equals','spec':{'requests':requests,'expected':{k:None for k in keys}}}
def call(t,fn,args):return {'test_id':t,'kind':'function_call','spec':{'function':fn,'args':args}}
# Release-record exercise: constants derived from registered fixtures; only assignments/key access in the learner region.
c='deployment.release_rollback_boundaries';f=fixture(c)
sc="from fastapi import FastAPI\napp = FastAPI()\nreleases = "+repr({x['release_id']:x for x in f['releases']})+'\ncurrent_database_schema = '+repr(f['current_database_schema'])+'\n'
prior=next(x for x in f['releases'][1:] if x['compatible'])
sc+="artifact_suffix = ''\nfor record in releases.values(): record['artifact'] += artifact_suffix\n"
sc+='prior_release_id = '+repr(prior['release_id'])+'\n# Supplied compatibility evidence identifies prior_release_id as the compatible prior record.\n'
sol="selected_release = releases[prior_release_id]\nprocedure = {'build': {'action':'create executable artifact'}, 'release': {'action':'bind artifact and intended configuration in immutable release', 'release_id':selected_release['release_id'], 'artifact':selected_release['artifact'], 'configuration':selected_release['configuration']}, 'run': {'action':'start selected release processes', 'release_id':selected_release['release_id']}, 'database_schema_after_rollback':current_database_schema}\n"
exercise(c,'Complete selected_release and procedure without modifying releases or current_database_schema. Select the prior release identified by supplied compatibility evidence, not the current or incompatible release. In procedure, build.action must be "create executable artifact"; release.action must be "bind artifact and intended configuration in immutable release", with release_id, artifact and configuration from the selected record; run.action must be "start selected release processes" with its release_id. Record database_schema_after_rollback as the unchanged current schema. These are records, not deployment commands.',sc,"selected_release = None\nprocedure = {}\n",sol,[v('selection','selected_release'),v('procedure','procedure'),v('records_unchanged','releases'),v('schema_unchanged','current_database_schema')],['fastapi'])
# Upstream HTTPX MockTransport: supplied failure mappings, no network.
c='integration.upstream_failure_translation';f=fixture(c)
sc='''import httpx
from fastapi import FastAPI, HTTPException
app = FastAPI()
'''+ 'mapping = '+repr(f)+'''
UPSTREAM_URL = 'https://upstream.invalid/lookup'
def status_failure(request):
    return httpx.Response(503, text='Controlled upstream internals', request=request)
def timeout_failure(request):
    raise httpx.ReadTimeout('Controlled timeout internals', request=request)
@app.get('/lookup')
async def route(case: str):
    transport = httpx.MockTransport(timeout_failure if case == 'timeout' else status_failure)
    async with httpx.AsyncClient(transport=transport) as client:
        return await lookup(client)
# Complete only lookup below; supplied MockTransport never accesses the network.
'''
sol='''async def lookup(client):
    try:
        response = await client.get(UPSTREAM_URL)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 503:
            raise HTTPException(status_code=mapping['upstream_503']['status'], detail=mapping['upstream_503']['detail']) from None
        else:
            raise HTTPException(status_code=mapping['fallback']['status'], detail=mapping['fallback']['detail']) from None
    except httpx.RequestError as exc:
        raise HTTPException(status_code=mapping['timeout']['status'], detail=mapping['timeout']['detail']) from None
'''
exercise(c,'Complete lookup(client): call raise_for_status(), distinguish HTTPStatusError by exc.response.status_code from RequestError, The supplied RequestError transport case is a controlled timeout. Apply the supplied mapping: upstream 503 and fallback become their fixed local status/detail, timeout its separate status/detail. Suppress raw upstream internals. Tests send GET /lookup with case=status and case=timeout to the real local route with supplied mock transports and assert exact mapped status and JSON {detail}.',sc,'async def lookup(client):\n    return {"detail":"TODO"}\n',sol,[h('status',[{'method':'GET','path':'/lookup','params':{'case':'status'}}]),h('timeout',[{'method':'GET','path':'/lookup','params':{'case':'timeout'}}])],['fastapi','httpx'])
# Relationship-loading exercise includes actual SQL capture before/after in separate fresh sessions.
c='sqlalchemy.redundant_queries';f=fixture(c)
sc='''from fastapi import FastAPI
from sqlalchemy import ForeignKey, create_engine, select, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session, selectinload
from sqlalchemy.pool import StaticPool
app = FastAPI()
'''+ 'fixture = '+repr(f)+'''
class Base(DeclarativeBase): pass
class Entity(Base):
    __tablename__ = 'Entity'
    id: Mapped[int] = mapped_column(primary_key=True)
    relationship_attribute: Mapped[list['Child']] = relationship(back_populates='parent', order_by='Child.id')
class Child(Base):
    __tablename__ = 'relationship_attribute'
    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('Entity.id'))
    parent: Mapped[Entity] = relationship(back_populates='relationship_attribute')
engine = create_engine('sqlite://', echo=True, poolclass=StaticPool, connect_args={'check_same_thread':False})
Base.metadata.create_all(engine)
with Session(engine) as session:
    session.add_all([Entity(id=i) for i in fixture['parent_ids']] + [Child(**x) for x in fixture['children']])
    session.commit()
sql_capture = []
@event.listens_for(engine, 'before_cursor_execute')
def capture(conn, cursor, statement, parameters, context, executemany):
    if statement.lstrip().upper().startswith('SELECT'): sql_capture.append(statement)
def projection(parents):
    return [{'id':p.id, 'children':[c.id for c in p.relationship_attribute]} for p in parents]
def baseline(session, parent_limit):
    return projection(session.execute(select(Entity).order_by(Entity.id).limit(parent_limit)).scalars().all())
@app.get('/compare')
def compare(parent_limit:int=3):
    sql_capture.clear()
    with Session(engine) as session: before = baseline(session, parent_limit)
    before_sql = list(sql_capture)
    sql_capture.clear()
    with Session(engine) as session: after = listing(session, parent_limit)
    after_sql = list(sql_capture)
    return {'before':before, 'after':after, 'before_relationship_selects':sum('FROM relationship_attribute' in x for x in before_sql), 'after_relationship_selects':sum('FROM relationship_attribute' in x for x in after_sql), 'same_result':before == after}
# Complete listing using the same ordered parent selection, limiting to three.
'''
sol='''def listing(session, parent_limit):
    statement = select(Entity).order_by(Entity.id).limit(parent_limit)
    statement = statement.options(selectinload(Entity.relationship_attribute))
    parents = session.execute(statement).scalars().all()
    return projection(parents)
'''
exercise(c,'Complete listing(session, parent_limit) with statement.options(selectinload(Entity.relationship_attribute)). Preserve the ordered selection of the requested parent_limit Entity parents (tests request three and two) and the supplied {id, children} projection, including empty collections. GET /compare?parent_limit=... runs the unchanged and completed versions in separate fresh sessions with echo=True and captures real emitted SELECTs. It grades identical before/after data, same_result=true, and reduced relationship SELECT counts; do not edit the supplied capture or projection.',sc,sol.replace('    statement = statement.options(selectinload(Entity.relationship_attribute))\n',''),sol,[h('compare_'+str(n),[{'method':'GET','path':'/compare','params':{'parent_limit':n}}]) for n in [3,2]],['fastapi','sqlalchemy'])
# Freshness callable is graded for every registry case plus altered limits.
c='fastapi_backend.webhook_replay_freshness';f=fixture(c)
sc='from fastapi import FastAPI\napp = FastAPI()\n'
sol='''def delivery_is_fresh(signed_delivery_timestamp, receiver_now, acceptance_window, future_tolerance):
    age = receiver_now - int(signed_delivery_timestamp)
    return -future_tolerance <= age and age <= acceptance_window
'''
ts=[call(x['case_id'],'delivery_is_fresh',[x[k] for k in ['signed_delivery_timestamp','receiver_now','acceptance_window','future_tolerance']]) for x in f['cases']]
fresh=f['cases'][0];ts.append(call('changed_past_limit','delivery_is_fresh',[fresh['signed_delivery_timestamp'],fresh['receiver_now'],fresh['acceptance_window']//10,fresh['future_tolerance']]))
exercise(c,'Implement delivery_is_fresh(signed_delivery_timestamp, receiver_now, acceptance_window, future_tolerance) returning bool. Parse the authenticated valid integer-seconds string with int; compute receiver time minus delivery time. Accept inclusive past-age and future-offset bounds using the supplied limits. Signatures are verified beforehand; this is delivery-timestamp freshness, not original event age. Tests cover in-window, expired, future-outside, both exact boundaries, now, and changed limits. Do not read the real clock or hard-code the policy.',sc,'def delivery_is_fresh(signed_delivery_timestamp, receiver_now, acceptance_window, future_tolerance):\n    return False\n',sol,ts,['fastapi'])
# Object boundary: synchronous SQLite supplied scaffolding, only trusted-context predicate is edited.
c='auth.object_authorization';f=fixture(c)
sc='''from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, select, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.pool import StaticPool
from types import SimpleNamespace
'''+ 'fixtures = '+repr(f)+'''
class Base(DeclarativeBase): pass
class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
engine = create_engine('sqlite://', poolclass=StaticPool, connect_args={'check_same_thread':False})
Base.metadata.create_all(engine)
with Session(engine) as session:
    session.add_all([Order(**x) for x in fixtures['orders']]); session.commit()
class ScalarSession:
    def __init__(self, session): self.session = session
    async def scalar(self, statement): return self.session.scalar(statement)
# Each app substitutes only the trusted principal for object-boundary testing.
# This is not a token-verification exercise; caller owner_id query input is ignored.
def make_app(context):
    api = FastAPI()
    def trusted_principal(): return SimpleNamespace(owner_id=context['owner_id'])
    @api.get('/orders/{order_id}')
    async def endpoint(order_id:int, principal=Depends(trusted_principal)):
        with Session(engine) as session:
            order = await retrieve_order(order_id, principal, ScalarSession(session))
            if order is None:
                raise HTTPException(status_code=fixtures['unavailable_object']['status'], detail=fixtures['unavailable_object']['body']['detail'])
            return {'id':order.id, 'status':order.status}
    return api
app = make_app(fixtures['principals'][0])
app_b = make_app(fixtures['principals'][1])
# Complete the supplied lookup; do not modify make_app or accept an owner argument.
'''
sol='''async def retrieve_order(order_id, principal, session):
    statement = select(Order).where(Order.id == order_id, Order.owner_id == principal.owner_id)
    return await session.scalar(statement)
'''
ts=[]
for i,(owner,oid) in enumerate(f['pairs']):
 t=h('pair_'+str(i),[{'method':'GET','path':'/orders/'+str(oid),'params':{'owner_id':next(x['owner_id'] for x in f['orders'] if x['id']==oid)}}]);t['spec']['app']='app' if owner==f['principals'][0]['owner_id'] else 'app_b';ts.append(t)
exercise(c,'Complete retrieve_order(order_id, principal, session) using both Order.id and Order.owner_id predicates, taking owner identity only from principal.owner_id. Return await session.scalar(statement), yielding an order or None. The supplied local route returns only {id,status}, or the supplied 404 {detail:"Not found"}. Tests use both trusted contexts against both orders and send caller owner_id query inputs attempting override. Own requests must succeed; cross-owner requests must return the unavailable-object response with no order data. Do not alter fixtures, trusted context scaffolding or returned projection.',sc,sol.replace(', Order.owner_id == principal.owner_id',''),sol,ts,['fastapi','sqlalchemy'])
# Persistent transactional duplicate suppression in an in-memory database retained across app reconstruction.
c='fastapi_backend.webhook_delivery_idempotency';f=fixture(c)
sc='''import asyncio, httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, String, ForeignKey, select, event, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import IntegrityError
'''+ 'fixtures = '+repr(f)+'''
class Base(DeclarativeBase): pass
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
class OrderChange(Base):
    __tablename__ = 'order_changes'
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
@event.listens_for(Order, 'after_update')
def count_change(mapper, connection, target):
    connection.execute(OrderChange.__table__.insert().values(order_id=target.id))
engine = create_engine('sqlite://', poolclass=StaticPool, connect_args={'check_same_thread':False})
Base.metadata.create_all(engine)
with Session(engine) as session:
    session.add_all([Order(**x) for x in fixtures['orders']]); session.commit()
# Supplied async facade preserves a sync SQLite transaction; no threads/network.
class AsyncSessionFacade:
    def __init__(self, session): self.session = session
    @asynccontextmanager
    async def begin(self):
        with self.session.begin(): yield self
    def add(self, value): self.session.add(value)
    async def flush(self): self.session.flush()
    async def scalar(self, statement): return self.session.scalar(statement)
def snapshot():
    with Session(engine) as session:
        orders = session.scalars(select(Order).order_by(Order.id)).all()
        events = session.scalars(select(ProcessedEvent).order_by(ProcessedEvent.publisher_event_id)).all()
        changes = session.scalars(select(OrderChange).order_by(OrderChange.id)).all()
        return {'orders':[{'id':o.id,'owner_id':o.owner_id,'status':o.status} for o in orders], 'events':[e.publisher_event_id for e in events], 'committed_changes':[x.order_id for x in changes]}
def make_app():
    api = FastAPI()
    @api.exception_handler(Exception)
    async def failed(request, exc): return JSONResponse(status_code=500,content={'detail':'Internal server error'})
    @api.post('/authenticated-events')
    async def deliver(value:dict, failure:str='none'):
        # Exercise begins after signature authentication; this is a controlled trusted-event harness.
        with Session(engine) as session:
            if failure != 'none':
                @event.listens_for(session, 'after_flush_postexec', once=True)
                def inject(session, context):
                    if failure == 'integrity': raise IntegrityError('unrelated controlled constraint',{},Exception('internal'))
                    raise RuntimeError('controlled transaction failure')
            return await handle_authenticated_event(value, AsyncSessionFacade(session))
    return api
app = FastAPI()
@app.post('/scenario/{kind}')
async def scenario(kind:str, value:dict):
    child = make_app()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=child,raise_app_exceptions=False),base_url='http://test') as client:
        if kind == 'concurrent':
            responses = await asyncio.gather(client.post('/authenticated-events',json=value),client.post('/authenticated-events',json=value))
        elif kind == 'failure' or kind == 'integrity':
            responses = [await client.post('/authenticated-events',params={'failure':kind},json=value)]
        else:
            responses = [await client.post('/authenticated-events',json=value)]
            if kind == 'sequential': responses.append(await client.post('/authenticated-events',json=value))
    if kind == 'restart':
        # Reconstruct a new app and request-local session, retain the same persistent engine.
        child = make_app()
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=child,raise_app_exceptions=False),base_url='http://test') as client:
            responses.append(await client.post('/authenticated-events',json=value))
    return {'responses':[{'status':r.status_code,'json':r.json()} for r in responses], 'snapshot':snapshot()}
# Complete only the transactional handler below, not the durable models or harness.
'''
sol='''async def handle_authenticated_event(event, session):
    try:
        async with session.begin():
            order = await session.scalar(select(Order).where(Order.id == event['order_id']))
            if order is None:
                raise HTTPException(status_code=404, detail='Not found')
            session.add(ProcessedEvent(publisher_event_id=event['publisher_event_id']))
            await session.flush()
            order.status = event['new_status']
    except IntegrityError:
        existing = await session.scalar(select(ProcessedEvent).where(ProcessedEvent.publisher_event_id == event['publisher_event_id']))
        if existing is None:
            raise
    return {'received':True}
'''
ts=[]
for kind in ['sequential','restart','concurrent','failure','integrity']:
 for i,value in enumerate(f['authenticated_events']):ts.append(h(kind+'_'+str(i),[{'method':'POST','path':'/scenario/'+kind,'json':value}]))
exercise(c,'Complete handle_authenticated_event(event, session) after authenticity has already been established by the supplied controlled harness. Persist the unique publisher_event_id and order status update in one async with session.begin() transaction. On IntegrityError, acknowledge only after confirming that exact processed event identity; otherwise re-raise. Return {received:true} after commit or confirmed duplicate. Do not change the facade, models, failure hooks or harness. Tests dispatch the same authenticated event sequentially, concurrently, and across actual child-app reconstruction with the database retained: each must acknowledge both and leave one persistent identity and exactly one committed order change. Controlled transaction failure and unrelated integrity failure must return the generic 500 and leave no event or change committed. Each test grades the complete response/snapshot for both fixture event inputs.',sc,'async def handle_authenticated_event(event, session):\n    return {"received":False}\n',sol,ts,['fastapi','httpx','sqlalchemy'])
# Configuration-only retry practice. The immutable supplied adapter is quoted for inspection.
# Runtime checks validate its policy inputs and simulate its deterministic scheduling, not network/client internals.
c='integration.bounded_idempotent_retries';f=fixture(c);ff=files(c)
sc='''from fastapi import FastAPI
from email.utils import parsedate_to_datetime
app = FastAPI()
'''+ 'contract = '+repr(f)+'''
# Runtime verification mirror of the supplied maintained-client adapter's configuration contract.
# No outbound network occurs; these scripted checks exercise policy decisions only.
def server_delay(value, now):
    if value is None: return None
    try:
        if str(value).isdigit(): return float(value)
        return max(0, parsedate_to_datetime(value).timestamp() - now)
    except (ValueError,TypeError,OverflowError): return None
def verify_policy(operation, steps, receiver_now):
    if any(policy.get(k) is None for k in ['retryable_failures','max_attempts','total_time_budget','retry_after','bounded_backoff','retry_safe']):
        return {'error':'Incomplete policy'}
    calls, elapsed, delays = 0, 0, []
    safe = policy['retry_safe'] and (operation.get('contract_idempotent',False) or operation.get('known_not_applied',False))
    while True:
        calls += 1
        step = steps[min(calls-1,len(steps)-1)]
        elapsed += step.get('duration',0)
        if 'failure' not in step: return {'outcome':'success','calls':calls,'elapsed':elapsed,'delays':delays}
        if not safe or step['failure'] not in policy['retryable_failures']:
            return {'outcome':'terminal','calls':calls,'elapsed':elapsed,'delays':delays}
        delay = server_delay(step.get('retry_after'),receiver_now + elapsed) if policy['retry_after'] else None
        if delay is None: delay = min(2**(calls-1),policy['bounded_backoff'])
        if calls >= policy['max_attempts'] or elapsed + delay >= policy['total_time_budget']:
            return {'outcome':'exhausted','calls':calls,'elapsed':elapsed,'delays':delays}
        delays.append(delay); elapsed += delay
@app.get('/verify')
def verify(case:str):
    safe, unsafe = contract['operations']
    scripts = {
      'transient':[{'failure':'transient'},{'result':{'ok':True}}],
      'exhausted':[{'failure':'transient'}],
      'delay_seconds':[{'failure':'transient','retry_after':contract['retry_after_delay_seconds']},{'result':{'ok':True}}],
      'delay_date':[{'failure':'transient','retry_after':contract['retry_after_http_date']},{'result':{'ok':True}}],
      'over_budget_delay':[{'failure':'transient','retry_after':str(contract['hypothetical_limits']['total_time_budget_seconds'] + 1)}],
      'terminal':[{'failure':'terminal'}],
      'unsafe':[{'failure':'transient'}]}
    return {'policy':policy, 'result':verify_policy(unsafe if case=='unsafe' else safe, scripts[case], contract['receiver_now'])}
# Edit only the mapping. No loop or retry engine is requested from the learner.
'''
limits=f['hypothetical_limits']
policy={'retryable_failures':['transient'],'max_attempts':limits['max_attempts'],'total_time_budget':limits['total_time_budget_seconds'],'retry_after':True,'bounded_backoff':limits['max_backoff_seconds'],'retry_safe':True}
sol='policy = '+repr(policy)+'\n'
ts=[h(k,[{'method':'GET','path':'/verify','params':{'case':k}}]) for k in ['transient','exhausted','delay_seconds','delay_date','over_budget_delay','terminal','unsafe']]
exercise(c,'Complete only policy for the supplied maintained-client adapter: retryable_failures=["transient"] (terminal failures excluded), max_attempts and total_time_budget from contract.hypothetical_limits, retry_after=true to honor both delay-seconds and HTTP-date forms, bounded_backoff from max_backoff_seconds, and retry_safe=true subject to the adapter enforcing the operation contract. Use literal values matching the supplied fixture. The runtime verification mirror tests deterministic configuration decisions (not live outbound execution): transient then success, repeated-failure exhaustion, both server-delay forms, over-budget delay, terminal failure and one attempt only for an unsafe POST with a lost response. A timeout never establishes no remote effect. No retry engine changes are permitted.',sc,"policy = {'retryable_failures':None,'max_attempts':None,'total_time_budget':None,'retry_after':None,'bounded_backoff':None,'retry_safe':None}\n",sol,ts,['fastapi'])

exec((B/'refine_review_packets.py').read_text())

# One interaction per planned step; glossary anchors and remediation targets copied, never guessed.
output={k:P[k] for k in ['schema_version','path_id','batch_id']};output['kind']='interactions_part';output['tiles']=[]
for tile in P['tiles']:
 st=next(t for t in S['tiles'] if t['tile_id']==tile['tile_id'])
 rem=st.get('remediation_steps',[])
 out={'tile_id':tile['tile_id'],'interactions':[]};seen=set();step_count=0
 for step in tile['steps']:
  if step['type'] not in ['check','hands_on']:continue
  cid=step['concept_ids'][0];b=bs[cid]
  measures=[]
  for a in step['anchors']:
   if '#assessment:' in a:
    ac,cap=a.split('#assessment:');ass=next(x for x in bs[ac]['assessment_anchors'] if x['capability']==cap)
    measures.append({'concept_id':ac,'capability':cap,'fact_ids':ass['fact_ids']})
  if not measures:
   measures=[{'concept_id':cid,'capability':a['capability'],'fact_ids':a['fact_ids']} for a in b['assessment_anchors']]
  feedback={'correct':{'message':'Your response respects the stated boundary and the supplied evidence.'},'incorrect':{'message':'Recheck which evidence establishes the boundary; a declaration or successful single case is not a substitute for the required checks.'},'hints':['Trace the inputs, the decision boundary, and the observable output separately.']}
  if cid not in seen:
   measured={m['concept_id']+'#'+fid for m in measures for fid in m['fact_ids']}
   relevant=[r for r in rem if cid in r['concept_ids'] and measured.intersection(r['lineage']['fact_ids'])]
   if relevant:feedback['remediation_step_id']=max(relevant,key=lambda r:len(measured.intersection(r['lineage']['fact_ids'])))['step_id']
  ix={'type':step['planned_interaction_type'],'interaction_id':'ix.'+step['step_id'],'difficulty':'intro' if step_count==0 else ('stretch' if step_count==sum(x['type'] in ['check','hands_on'] for x in tile['steps'])-1 else 'core'),'grading_mode':'client','standalone':True,'measures':measures,'anchors':step['anchors'],'feedback':feedback}
  if ix['type']=='choice':
   prompt,opts,whys=Q[step['step_id']]
   options=[{'option_id':'o'+str(i+1),'text':text} for i,text in enumerate(opts)]
   ix['public']={'prompt':prompt,'selection':'single','shuffle':True,'options':options}
   ix['grading']={'correct_option_ids':[options[0]['option_id']],'option_feedback':{o['option_id']:{'message':why or 'This option applies the taught boundary to the evidence.'} for o,why in zip(options,whys)}}
   # Concept-specific feedback copied from the required facts, not a novel claim.
   fact_text=' '.join(next(f['statement'] for f in b['coverage']['required_facts'] if f['id']==fid) for m in measures for fid in m['fact_ids'])
   feedback['correct']['message']=fact_text
   feedback['incorrect']['message']='Check this rule: '+fact_text
  elif ix['type']=='classify':
   prompt,items=C[cid]
   ix['public']={'prompt':prompt+' Each excerpt is a hypothetical candidate, not a report of observed execution. Classify every item.','buckets':[{'bucket_id':'good','label':'Meets the stated review requirements'},{'bucket_id':'bad','label':'Fails the stated review requirements'}],'items':[{'item_id':'i'+str(i+1),'text':text} for i,(bucket,text,why) in enumerate(items)]}
   ix['grading']={'assignments':{'i'+str(i+1):bucket for i,(bucket,text,why) in enumerate(items)},'item_feedback':{'i'+str(i+1):{'message':why} for i,(bucket,text,why) in enumerate(items)}}
  elif ix['type']=='code_exercise':
   prompt,starter,solution,tests,packages=E[cid]
   if cid=='integration.bounded_idempotent_retries':
    prompt+=' Read adapter_reference.py for the supplied maintained-client implementation; it is reference-only because tenacity is outside this in-process runtime.'
   lc=b['practice_anchor']['live_code']
   ix['public']={'prompt':prompt,'runtime':{'kind':'python_asgi','version':sandbox.RUNTIMES['python_asgi']['version'],'packages':packages},'workspace':{'entry':'main.py','files':[{'path':'main.py','role':'editable','language':'python','content':starter}],'asset_mounts':[]},'constraints':{k:lc.get(k,[]) for k in ['allowed_syntax','blocked_syntax']}}
   if cid=='integration.bounded_idempotent_retries':
    ix['public']['workspace']['files'].append({'path':'adapter_reference.py','role':'readonly','language':'python','content':files(cid)['adapter.py']})
   ix['grading']={'solution_files':[{'path':'main.py','content':solution}],'tests':copy.deepcopy(tests)}
   # Derive expected outputs by executing solution in the actual pinned runner.
   probes=[sandbox._py_probe(t) for t in tests]
   result=sandbox.node_run(sandbox._py_job('python_asgi',packages,[sandbox._py_script('derive','main.py',solution,[],probes)]),sandbox.RUNTIMES['python_asgi']['runner'])['results']['derive']
   if not result['ok']:raise RuntimeError((cid,result))
   for t in ix['grading']['tests']:
    t['message_on_fail']='The '+t['test_id']+' case does not match the prompt contract. Recheck the learner-completed boundary without changing the supplied harness.'
    got,err=sandbox._py_result(t['kind'],t['spec'],result,t['test_id'])
    if err:raise RuntimeError((cid,t['test_id'],err,result))
    t['spec']['expected']=sandbox._http_view(got,t['spec']['expected']) if t['kind']=='http_equals' else got
   print('Derived',cid,len(tests),'tests',flush=True)
  else:raise ValueError(ix['type'])
  out['interactions'].append({'step_id':step['step_id'],'interaction':ix});seen.add(cid);step_count+=1
 output['tiles'].append(out)
(B/'interactions.json').write_text(json.dumps(output,indent=2)+'\n')
print('Wrote',sum(len(t['interactions']) for t in output['tiles']),'interactions')
