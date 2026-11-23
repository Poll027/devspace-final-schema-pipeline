# EVALUATOR PACKET — Service release and rollback workflow with build, release and run separation (tile_082)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = deployment.release_rollback_boundaries — Service release and rollback workflow with build, release and run separation

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (deployment.release_rollback_boundaries)   objective: Separate build release and run: specify one release/rollback procedure.
A.f1: Build creates an executable artifact, release combines that artifact with deploy-specific configuration, and run starts processes from the selected release.   [sources: twelve_factor_app#https://12factor.net/build-release-run#v_build_release_run]
A.f2: Releases have unique identifiers and are immutable; a new change produces a new release rather than mutating a running release.   [sources: twelve_factor_app#https://12factor.net/build-release-run#v_build_release_run]
A.f3: Record the artifact and configuration for each release and define rollback by redeploying a known prior release with its intended configuration.   [sources: twelve_factor_app#https://12factor.net/build-release-run#v_build_release_run]
A.f4: Check the prior release's compatibility with the current database schema before selecting it for rollback; replacing an application release does not itself reverse a database migration.   [sources: alembic_docs#https://alembic.sqlalchemy.org/en/latest/autogenerate.html#auto-generating-migrations, twelve_factor_app#https://12factor.net/build-release-run#v_build_release_run]
note: Establish this first: Releases bind artifacts and configuration and can be replaced.
note: Stay within the current objective: Separate build release and run. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine a rollback release.
PRACTICE ANCHOR (live_code): Represent one release and rollback procedure in Python: record uniquely identified releases with their artifacts and intended configurations, then select a known prior release supported by supplied compatibility evidence for the current database schema.  SUCCESS: The procedure separates build, release and run, preserves existing release records, selects the prior artifact together with its intended configuration, and explicitly records that application rollback leaves the current database schema unchanged.
ASSESSMENT ANCHOR: distinguish_build_release_and_run facts=['f1']
ASSESSMENT ANCHOR: determine_compatible_prior_release_for_rollback facts=['f2', 'f3', 'f4']

## DATA ASSETS USED
ds.releases: Immutable release records and supplied fixture compatibility — columns: release_id(identifier), artifact(identifier), configuration(identifier), current_database_schema(identifier), compatible(categorical)
   ["release_current","artifact_current","config_current","schema_current",true]
   ["release_prior_compatible","artifact_prior_compatible","config_prior_compatible","schema_current",true]
   ["release_prior_incompatible","artifact_prior_incompatible","config_prior_incompatible","schema_current",false]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authentication and authorization tests including invalid-token rejection; Bounded retry decisions respecting HTTP idempotency; Bounding payloads, expensive requests and API resource consumption; Database test-state isolation; Declaring the deployed bearer-access-token and authorization-server security contract without a password grant; Diagnose service failures from emitted and interpreted evidence; Documenting expected success and error responses; Endpoint authorization with required permissions or scopes; Established authorization-server integration using authorization code and PKCE where applicable; no resource-owner password grant; Inspecting generated OpenAPI for drift and sensitive exposure; Object-level authorization against the authenticated principal; Recognizing and avoiding redundant ORM queries; Safe unexpected-error responses with actionable server evidence; Upstream failure translation; Webhook authenticity verification; Webhook delivery idempotency; Webhook replay freshness

## LESSON, in learner order

### s01 · explainer · Service release and rollback workflow with build, release and run separation
Learn the rule — 
(definition) Build makes the executable artifact. Release pairs it with deploy-specific configuration. Run starts processes from the selected release. ⟦A.f1 A:tb2⟧
(definition) Each release has a unique, immutable identifier: changes create a new release, not edits to the running one. ⟦A.f2 A:tb3⟧
(definition) Record each artifact/configuration pair. Rollback redeploys a known prior release with its intended configuration. ⟦A.f3 A:tb3⟧
(definition) Before rollback, check compatibility with the current database schema. Replacing the application release does not reverse a migration. ⟦A.f4 A:tb3⟧
[PROCESS_FLOW] nodes=['Build → executable artifact', 'Release → artifact + deploy-specific configuration; unique immutable ID', 'Run → selected release’s processes', 'Rollback candidate: release_prior_compatible / artifact_prior_compatible / config_prior_compatible', 'Check current schema compatibility before selection', 'Compatible → redeploy intended prior release; database migration is not reversed', 'Incompatible → do not select'] edges=[('n0', 'n1', None), ('n1', 'n2', None), ('n2', 'n3', None), ('n3', 'n4', None), ('n4', 'n5', 'compatible'), ('n4', 'n6', 'incompatible')] alt: Build → executable artifact; Release → artifact + deploy-specific configuration; unique immutable ID; Run → selected release’s processes; Rollback candidate: release_prior_compatible / artifact_prior_compatible / config_prior_compatible; Check current schema compatibility before selection; Compatible → redeploy intended prior release; database migration is not reversed; Incompatible → do not select

### s02 · explainer · Keep the boundary clear
Work the boundary — 
(walkthrough) An old artifact is not enough: the prior release needs its intended configuration and compatibility with today’s schema. ⟦A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Choose the boundary
Check — 

### s04 · hands_on · Apply the contract
Practice — 

### s05 · recap · Take the rule with you
(takeaway) An old artifact is not enough: the prior release needs its intended configuration and compatibility with today’s schema. ⟦A.f4 A:tb5⟧
[UP NEXT] Documenting expected success and error responses: A documented order conflict is useful only when the endpoint actually emits the declared status and body. Additional response metadata does not implement the outcome.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: Service release and rollback workflow with build, release and run separation
(definition) Each release has a unique, immutable identifier: changes create a new release, not edits to the running one. ⟦A.f2 A:tb3 A:tb4⟧
(definition) Record each artifact/configuration pair. Rollback redeploys a known prior release with its intended configuration. ⟦A.f3 A:tb3 A:tb4⟧
(definition) Before rollback, check compatibility with the current database schema. Replacing the application release does not reverse a migration. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) An old artifact is not enough: the prior release needs its intended configuration and compatibility with today’s schema. ⟦A.f2 A.f3 A.f4 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.releases cols=['release_id', 'artifact', 'configuration', 'current_database_schema', 'compatible'] ] caption: Immutable release records and supplied fixture compatibility
### r02 · Review: Service release and rollback workflow with build, release and run separation
(definition) Build makes the executable artifact. Release pairs it with deploy-specific configuration. Run starts processes from the selected release. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Each release has a unique, immutable identifier: changes create a new release, not edits to the running one. ⟦A.f2 A:tb3 A:tb4⟧
(definition) Record each artifact/configuration pair. Rollback redeploys a known prior release with its intended configuration. ⟦A.f3 A:tb3 A:tb4⟧
(definition) Before rollback, check compatibility with the current database schema. Replacing the application release does not reverse a migration. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) An old artifact is not enough: the prior release needs its intended configuration and compatibility with today’s schema. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.releases cols=['release_id', 'artifact', 'configuration', 'current_database_schema', 'compatible'] ] caption: Immutable release records and supplied fixture compatibility

=========

# EVALUATOR PACKET — Documenting expected success and error responses / Safe unexpected-error responses with actionable server evidence (tile_083)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.documented_responses — Documenting expected success and error responses
B = fastapi.safe_unexpected_errors — Safe unexpected-error responses with actionable server evidence

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (fastapi.documented_responses)   objective: Document responses: document one endpoint's outcomes.
A.f1: Declare known outcomes with responses={status: {"model": PublicModel, "description": ...}} alongside the main response_model and status_code.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/additional-responses/#additional-response-with-model]
A.f2: A responses declaration documents additional outcomes but does not make the handler produce them; return the actual matching response or raise the corresponding expected exception.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/additional-responses/#additional-response-with-model]
A.f3: Use response_description and outcome descriptions to explain what the successful and expected error bodies mean to clients.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#response-description]
A.f4: Compare generated response status entries and schemas with HTTP tests of the real success and expected error cases so documentation does not claim a body or status the endpoint does not emit.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/first-steps/#check-the-openapi-json, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/testing/#using-testclient]
note: Establish this first: Documentation describes actual public outcomes.
note: Stay within the current objective: Document responses. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify missing or misleading cases.
PRACTICE ANCHOR (live_code): Document an existing order endpoint's successful response and expected 409 conflict using its supplied public models, then verify those declarations against HTTP results.  SUCCESS: The endpoint declares its main response_model and status_code, a meaningful response_description, and a 409 responses entry with the matching public model and description. Generated response entries and schemas agree with the supplied success and conflict HTTP tests.
ASSESSMENT ANCHOR: identify_missing_outcome_models_and_descriptions facts=['f1', 'f3']
ASSESSMENT ANCHOR: identify_documented_outcomes_that_do_not_match_http_results facts=['f2', 'f4']

## SOURCE FACTS — B (fastapi.safe_unexpected_errors)   objective: Contain unexpected exceptions: add one safe failure fallback.
B.f1: Unexpected internal failures should return generic public error information without stack traces, exception messages or implementation details.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html#error-handling]
B.f2: Register a fallback exception handler that returns a stable generic JSON response with 500 for an unexpected server condition while recording the exception internally.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers, rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-15.6.1]
B.f3: Internal failure evidence should identify the event, code location and interaction context while omitting prohibited secrets and sensitive data.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#event-attributes, owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#data-to-exclude]
B.f4: Disable debug traceback responses in production because debug mode substitutes a traceback response for the configured 500 handler.   [sources: fastapi_docs_advanced#https://starlette.dev/exceptions/#errors-and-handled-exceptions]
B.f5: Exercise the fallback with TestClient(app, raise_server_exceptions=False), asserting the generic public response and inspecting the safe internal diagnostic record separately.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/testing/#using-testclient, owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html#error-handling, fastapi_docs_advanced#https://starlette.dev/testclient/]
note: Establish this first: Diagnostics stay internal while public output stays safe.
note: Stay within the current objective: Contain unexpected exceptions. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify internal disclosure.
PRACTICE ANCHOR (live_code): Add one fallback exception handler to the supplied FastAPI application, returning stable generic JSON with status 500 and recording safe internal failure evidence. Disable debug responses and verify the fallback with the supplied controlled failure route.  SUCCESS: The controlled failure returns the exact generic JSON body with status 500, without exception messages, traces or implementation details. A separate check confirms that the internal record identifies the event, code location and interaction context without prohibited secrets or sensitive data.
ASSESSMENT ANCHOR: identify_internal_disclosure_in_public_error_responses facts=['f1', 'f4']
ASSESSMENT ANCHOR: distinguish_safe_internal_evidence_from_public_error_information facts=['f3', 'f5']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authentication and authorization tests including invalid-token rejection; Bounded retry decisions respecting HTTP idempotency; Bounding payloads, expensive requests and API resource consumption; Database test-state isolation; Declaring the deployed bearer-access-token and authorization-server security contract without a password grant; Diagnose service failures from emitted and interpreted evidence; Endpoint authorization with required permissions or scopes; Established authorization-server integration using authorization code and PKCE where applicable; no resource-owner password grant; Inspecting generated OpenAPI for drift and sensitive exposure; Object-level authorization against the authenticated principal; Recognizing and avoiding redundant ORM queries; Safe unexpected-error responses with actionable server evidence; Upstream failure translation; Webhook authenticity verification; Webhook delivery idempotency; Webhook replay freshness

## LESSON, in learner order

### s01 · explainer · Documenting expected success and error responses
Learn the rule — 
(definition) Declare known outcomes with responses={status: {"model": PublicModel, "description": ...}}, alongside response_model and status_code. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Metadata does not implement an outcome. Return the matching response or raise its expected exception. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Use response_description and outcome descriptions to explain what success and expected-error bodies mean to clients. ⟦A.f3 A:tb3 A:tb4⟧
(definition) Compare generated status entries and schemas against real HTTP success and expected-error tests; document only bodies and statuses the endpoint emits. ⟦A.f4 A:tb3 A:tb4⟧
[SIDE_BY_SIDE] Declarations need matching HTTP behavior, models and descriptions. left_label: Endpoint declarations and implementation | right_label: Supplied outcome contract / inspection
  left:
[CODE python]
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.testclient import TestClient
class PublicModel(BaseModel):
    id: int
    status: str
class ConflictModel(BaseModel):
    detail: str
app = FastAPI()
# Response declarations do not replace implementation.
@app.post('/orders', response_model=PublicModel, status_code=200, response_description="Created order", responses={409: {"model": ConflictModel, "description": "Order conflict"}})
def create_order(conflict: bool = False):
    if conflict:
        raise HTTPException(status_code=409, detail='Order conflict')
    return {'id': 101, 'status': 'pending'}
with TestClient(app) as client:
    success = client.post('/orders')
    conflict = client.post('/orders?conflict=true')
    schema = app.openapi()
    # TODO: compare actual responses with generated entries and schemas.

  annotations: []
  right:
[CODE python]
# Inspect generated declarations and exercise the real HTTP cases.
fixtures = {'success_status': 200, 'success_body': {'id': 101, 'status': 'pending'}, 'conflict_status': 409, 'conflict_body': {'detail': 'Order conflict'}}
with TestClient(app) as client:
    success = client.post('/orders')
    conflict = client.post('/orders?conflict=true')
    assert success.status_code == fixtures["success_status"]
    assert success.json() == fixtures["success_body"]
    assert conflict.status_code == fixtures["conflict_status"]
    assert conflict.json() == fixtures["conflict_body"]
response_entries = app.openapi()["paths"]['/orders']["post"]["responses"]
# Compare each entry’s schema and descriptions with the exercised bodies.

  annotations: []
[COMPARISON] cols=['Declared/generated contract', 'Exercised HTTP bodies']
  - Success: {"documented":"declared/generated 200, schema PublicModel requiring integer id and string status; Success description: Created order.","http":"HTTP 200, {\"id\":101,\"status\":\"pending\"}."}
  - Conflict: {"documented":"declared/generated 409, schema ConflictModel requiring string detail; Conflict description: Order conflict.","http":"HTTP 409, {\"detail\":\"Order conflict\"}."}
  - Schema agreement: {"documented":"Both exercised bodies match their documented schemas.","http":"Both exercised bodies match their documented schemas."}

### s02 · check · Choose the boundary
Check — 

### s03 · hands_on · Apply the contract
Practice — 

### s04 · explainer · Safe unexpected-error responses with actionable server evidence
Learn the rule — 
(definition) Keep unexpected failures generic publicly: no stack traces, exception messages or implementation details. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(definition) Register a fallback exception handler returning stable generic JSON with status 500 while recording the exception internally. ⟦B.f2 B:tb3 B:tb4⟧
(definition) Internal evidence needs the event, code location and interaction context, excluding prohibited secrets and sensitive data. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(definition) Disable production debug traceback responses: debug mode replaces the configured 500 handler with a traceback response. ⟦B.f4 B:tb3 B:tb4 B:tb5⟧
(definition) Use TestClient(app, raise_server_exceptions=False) to assert the public response; inspect the safe internal record separately. ⟦B.f5 B:tb3 B:tb4⟧
[SIDE_BY_SIDE] Inspect public response and internal diagnostics separately; keep production debug disabled. left_label: Public boundary | right_label: Separate internal safe record
  left:
[DIAGRAM: Public response contract] nodes=['Declared public status: 500', 'Declared generic JSON: {"detail": "Internal server error"}', 'Exclude traces, exception messages and implementation details'] edges=[] alt: Declared public status: 500; Declared generic JSON: {"detail": "Internal server error"}; Exclude traces, exception messages and implementation details
  right:
[CODE python]
safe_records = []
def record_safe_failure(request):
    safe_records.append({'event':'unexpected_failure','code_location':'controlled_failure',
                         'interaction_context':'interaction_fixture'})
  annotations: []

### s05 · check · Choose the boundary
Check — 

### s06 · check · Choose the boundary
Check — 

### s07 · hands_on · Apply the contract
Practice — 

### s08 · recap · Take the rule with you
(takeaway) A documented conflict and an implemented conflict are different things. Compare the declared model and status with the actual HTTP case. ⟦A.f2 A:tb5⟧
(takeaway) A safe public failure and an actionable internal record are separate checks. Debug tracebacks cross the public boundary. ⟦B.f1 B.f3 B.f4 B:tb5⟧
[UP NEXT] Upstream failure translation: An external service failure is input to the local integration contract. The local API should not blindly forward every remote status or raw response.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: Documenting expected success and error responses
(definition) Metadata does not implement an outcome. Return the matching response or raise its expected exception. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Compare generated status entries and schemas against real HTTP success and expected-error tests; document only bodies and statuses the endpoint emits. ⟦A.f4 A:tb3 A:tb4⟧
(misconception) In the supplied order contract, success is 200 and conflict is 409. Compare both bodies with their public models; declaring the conflict does not implement it. ⟦A.f2 A.f4 A:tb3 A:tb4 A:tb5⟧
### r02 · Review: Documenting expected success and error responses
(definition) Declare known outcomes with responses={status: {"model": PublicModel, "description": ...}}, alongside response_model and status_code. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Use response_description and outcome descriptions to explain what success and expected-error bodies mean to clients. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) In the supplied order contract, success is 200 and conflict is 409. Compare both bodies with their public models; declaring the conflict does not implement it. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4⟧
### r03 · Review: Safe unexpected-error responses with actionable server evidence
(definition) Keep unexpected failures generic publicly: no stack traces, exception messages or implementation details. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(definition) Disable production debug traceback responses: debug mode replaces the configured 500 handler with a traceback response. ⟦B.f4 B:tb3 B:tb4 B:tb5⟧
(misconception) The supplied public contract is 500 with {"detail": "Internal server error"}. Keep the diagnostic event, code location and interaction context in the separate internal record. ⟦B.f1 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r04 · Review: Safe unexpected-error responses with actionable server evidence
(definition) Internal evidence needs the event, code location and interaction context, excluding prohibited secrets and sensitive data. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(definition) Use TestClient(app, raise_server_exceptions=False) to assert the public response; inspect the safe internal record separately. ⟦B.f5 B:tb3 B:tb4⟧
(misconception) The supplied public contract is 500 with {"detail": "Internal server error"}. Keep the diagnostic event, code location and interaction context in the separate internal record. ⟦B.f3 B.f5 B:tb3 B:tb4 B:tb5⟧
### r05 · Review: Safe unexpected-error responses with actionable server evidence
(definition) Keep unexpected failures generic publicly: no stack traces, exception messages or implementation details. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(definition) Register a fallback exception handler returning stable generic JSON with status 500 while recording the exception internally. ⟦B.f2 B:tb3 B:tb4⟧
(definition) Internal evidence needs the event, code location and interaction context, excluding prohibited secrets and sensitive data. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(definition) Disable production debug traceback responses: debug mode replaces the configured 500 handler with a traceback response. ⟦B.f4 B:tb3 B:tb4 B:tb5⟧
(definition) Use TestClient(app, raise_server_exceptions=False) to assert the public response; inspect the safe internal record separately. ⟦B.f5 B:tb3 B:tb4⟧
(misconception) The supplied public contract is 500 with {"detail": "Internal server error"}. Keep the diagnostic event, code location and interaction context in the separate internal record. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3 B:tb4 B:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· blocks.title: Response declarations, resolved schemas and HTTP contract
· cells.http: HTTP 200, {"id":101,"status":"pending"}.
· cells.http: HTTP 409, {"detail":"Order conflict"}.

=========

# EVALUATOR PACKET — Upstream failure translation (tile_085)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = integration.upstream_failure_translation — Upstream failure translation

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (integration.upstream_failure_translation)   objective: Translate upstream failures into local service behavior: map one integration failure to a stable local response or domain failure.
A.f1: HTTPX distinguishes transport RequestError failures from HTTPStatusError raised for an unsuccessful HTTP status by response.raise_for_status().   [sources: fastapi_docs_advanced#https://www.python-httpx.org/exceptions/#the-exception-hierarchy]
A.f2: Call response.raise_for_status() when status failures require translation and classify caught HTTPStatusError by exc.response.status_code, while catching RequestError for failures without a usable response.   [sources: fastapi_docs_advanced#https://www.python-httpx.org/exceptions/#the-exception-hierarchy]
A.f3: Treat remote failures as inputs to an explicit local integration contract rather than blindly trusting or exposing a remote response as the local outcome.   [sources: owasp_api_security_top10_2023#https://api-security.owasp.org/editions/2023/en/0xaa-unsafe-consumption-of-apis/#how-to-prevent]
A.f4: When acting as a gateway, 502 denotes an invalid upstream response and 504 denotes an upstream timeout; select the local status or domain exception from the service's declared mapping rather than forwarding every upstream status unchanged.   [sources: rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-15.6.3, rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-15.6.5]
A.f5: Test one supplied upstream status failure and one transport failure, asserting the mapped local response or domain failure and absence of raw upstream internals.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/testing/#using-testclient, fastapi_docs_advanced#https://www.python-httpx.org/exceptions/#the-exception-hierarchy]
note: Establish this first: External failures cross a boundary through explicit local semantics, not blind status forwarding..
note: Stay within the current objective: Translate upstream failures into local service behavior. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine the local outcome for a supplied upstream status or transport failure.
PRACTICE ANCHOR (live_code): Implement translation of an integration failure using a supplied local contract, then test one unsuccessful upstream status and one transport failure.  SUCCESS: An upstream 503 maps to the supplied local 502 response with a fixed public detail, and an upstream timeout maps to the supplied local 504 response with a fixed public detail. Both tests assert the local outcome and confirm that raw upstream internals are absent.
ASSESSMENT ANCHOR: classify_upstream_status_and_transport_failures facts=['f1', 'f2']
ASSESSMENT ANCHOR: determine_local_outcome_from_declared_failure_mapping facts=['f3', 'f4']
ASSESSMENT ANCHOR: identify_assertions_for_mapped_failures_and_safe_public_output facts=['f5']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authentication and authorization tests including invalid-token rejection; Bounded retry decisions respecting HTTP idempotency; Bounding payloads, expensive requests and API resource consumption; Database test-state isolation; Declaring the deployed bearer-access-token and authorization-server security contract without a password grant; Diagnose service failures from emitted and interpreted evidence; Endpoint authorization with required permissions or scopes; Established authorization-server integration using authorization code and PKCE where applicable; no resource-owner password grant; Inspecting generated OpenAPI for drift and sensitive exposure; Object-level authorization against the authenticated principal; Recognizing and avoiding redundant ORM queries; Webhook authenticity verification; Webhook delivery idempotency; Webhook replay freshness

## LESSON, in learner order

### s01 · explainer · Upstream failure translation
Learn the rule — 
(definition) HTTPX RequestError describes transport failure. HTTPStatusError comes from response.raise_for_status() on an unsuccessful HTTP status. ⟦A.f1 A:tb2⟧
(definition) Call raise_for_status() when translating status failures. Classify HTTPStatusError using exc.response.status_code; catch RequestError when no usable response exists. ⟦A.f2 A:tb3⟧
(definition) Map remote failures through an explicit local integration contract; do not blindly expose or trust the remote response. ⟦A.f3 A:tb3⟧
(definition) For gateways, 502 means invalid upstream response and 504 means upstream timeout. Use the declared local mapping, not automatic status forwarding. ⟦A.f4 A:tb3⟧
(definition) Test a supplied status failure and a transport failure. Assert the mapped local response or domain failure without raw upstream internals. ⟦A.f5 A:tb3⟧
[PROCESS_FLOW] nodes=['Remote observation', 'Unsuccessful HTTP status → raise_for_status() → HTTPStatusError → exc.response.status_code', 'No usable response / timeout → RequestError', 'Apply supplied mapping: {"upstream_503": {"status": 502, "detail": "Upstream unavailable"}, "timeout": {"status": 504, "detail": "Upstream timed out"}, "fallback": {"status": 502, "detail": "Upstream unavailable"}}', 'Return local contract; exclude raw upstream internals'] edges=[('n0', 'n1', None), ('n0', 'n2', None), ('n1', 'n3', None), ('n2', 'n3', None), ('n3', 'n4', None)] alt: Remote observation; Unsuccessful HTTP status → raise_for_status() → HTTPStatusError → exc.response.status_code; No usable response / timeout → RequestError; Apply supplied mapping: {"upstream_503": {"status": 502, "detail": "Upstream unavailable"}, "timeout": {"status": 504, "detail": "Upstream timed out"}, "fallback": {"status": 502, "detail": "Upstream unavailable"}}; Return local contract; exclude raw upstream internals

### s02 · explainer · Keep the boundary clear
Work the boundary — 
(walkthrough) A remote status and a local outcome are separate decisions. A transport failure is not an unsuccessful HTTP response. ⟦A.f1 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Choose the boundary
Check — 

### s04 · check · Choose the boundary
Check — 

### s05 · hands_on · Apply the contract
Practice — 

### s06 · recap · Take the rule with you
(takeaway) A remote status and a local outcome are separate decisions. A transport failure is not an unsuccessful HTTP response. ⟦A.f1 A.f3 A.f4 A:tb5⟧
[UP NEXT] Webhook authenticity verification: A webhook signature authenticates the delivered bytes. Parsing and rewriting a body before verification can lose the exact input the publisher signed.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: Upstream failure translation
(definition) Map remote failures through an explicit local integration contract; do not blindly expose or trust the remote response. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(definition) For gateways, 502 means invalid upstream response and 504 means upstream timeout. Use the declared local mapping, not automatic status forwarding. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Under this fixture’s local mapping, the supplied upstream status failure maps to 502 and timeout maps to 504. These are declared local outcomes, not automatic forwarding. ⟦A.f3 A.f4 A:tb3 A:tb4 A:tb5⟧
### r02 · Review: Upstream failure translation
(definition) Test a supplied status failure and a transport failure. Assert the mapped local response or domain failure without raw upstream internals. ⟦A.f5 A:tb3 A:tb4⟧
(misconception) Under this fixture’s local mapping, the supplied upstream status failure maps to 502 and timeout maps to 504. These are declared local outcomes, not automatic forwarding. ⟦A.f5 A:tb3 A:tb4⟧
### r03 · Review: Upstream failure translation
(definition) HTTPX RequestError describes transport failure. HTTPStatusError comes from response.raise_for_status() on an unsuccessful HTTP status. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Call raise_for_status() when translating status failures. Classify HTTPStatusError using exc.response.status_code; catch RequestError when no usable response exists. ⟦A.f2 A:tb3 A:tb4⟧
(misconception) Under this fixture’s local mapping, the supplied upstream status failure maps to 502 and timeout maps to 504. These are declared local outcomes, not automatic forwarding. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Webhook authenticity verification (tile_086)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = integration.webhook_authenticity — Webhook authenticity verification

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (integration.webhook_authenticity)   objective: Verify webhook authenticity: verify one provider's raw signed payload.
A.f1: Read await request.body() to obtain the raw request bytes for signature verification before parsing or modifying the webhook body.   [sources: fastapi_docs_advanced#https://starlette.dev/requests/#body]
A.f2: Verify every delivery with the publisher's supported SDK or verification library against the raw bytes and endpoint signing secret, following that publisher's signing format rather than inventing a canonicalization.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html#signature-verification]
A.f3: Reject missing or invalid signatures before processing the event, and do not disclose the verification secret or failure's internal details in the response.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html#signature-verification]
A.f4: Test a valid signed delivery and deliveries with a modified body or absent signature, checking that only the valid delivery reaches event processing.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html#security-testing]
note: Establish this first: Authenticity binds bytes to a trusted signer.
note: Stay within the current objective: Verify webhook authenticity. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify invalid byte signatures.
PRACTICE ANCHOR (live_code): Implement one provider's webhook authenticity check using await request.body(), the supplied signature header, the endpoint signing secret, and the provider-supported verification library.  SUCCESS: A valid signed delivery reaches event processing. The same delivery with modified body bytes, and a delivery without a signature, are rejected before processing with responses that expose neither the secret nor verification internals.
ASSESSMENT ANCHOR: identify_invalid_signatures_for_modified_raw_bytes facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_signature_failures_that_must_prevent_event_processing facts=['f3', 'f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authentication and authorization tests including invalid-token rejection; Bounded retry decisions respecting HTTP idempotency; Bounding payloads, expensive requests and API resource consumption; Database test-state isolation; Declaring the deployed bearer-access-token and authorization-server security contract without a password grant; Diagnose service failures from emitted and interpreted evidence; Endpoint authorization with required permissions or scopes; Established authorization-server integration using authorization code and PKCE where applicable; no resource-owner password grant; Inspecting generated OpenAPI for drift and sensitive exposure; Object-level authorization against the authenticated principal; Recognizing and avoiding redundant ORM queries; Webhook delivery idempotency; Webhook replay freshness

## LESSON, in learner order

### s01 · explainer · Webhook authenticity verification
Learn the rule — 
(definition) Acquire raw bytes with await request.body() before parsing or changing the body. ⟦A.f1 A:tb2⟧
(definition) For every delivery, use the publisher-supported SDK or verifier with those bytes and the endpoint signing secret. Follow its signing format; invent no canonicalization. ⟦A.f2 A:tb3⟧
(definition) Reject absent or invalid signatures before processing. Keep the secret and internal verification details out of responses. ⟦A.f3 A:tb3⟧
(definition) Test valid, modified-body and missing-signature deliveries: only the valid signed delivery may reach processing. ⟦A.f4 A:tb3⟧
[CODE python]
from fastapi import HTTPException
import stripe
async def webhook(request, signing_secret, publisher_verifier, signature_header, process_event):
    raw_body = await request.body()
    signature = request.headers.get(signature_header)
    if not signature:
        raise HTTPException(400, "Invalid signature")
    try:
        event = publisher_verifier(raw_body, signature, signing_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        raise HTTPException(400, "Invalid signature")
    process_event(event)
    return {"received": True}

from scaffold import client, config, raw_body, processed_events
import pytest
@pytest.fixture(autouse=True)
def clear_recorder():
    processed_events.clear()
@pytest.mark.parametrize('condition', ['valid', 'modified', 'absent'])
def test_delivery(condition):
    body = raw_body if condition != 'modified' else raw_body + b' '
    headers = {} if condition == 'absent' else {config['signature_header']: config['signature']}
    with client() as http:
        # TODO: http.post('/webhook', content=body, headers=headers).
        # Assert exact status/body and recorder length (one only for valid).
        raise NotImplementedError('Complete this delivery test')

  annotations: []
[COMPARISON] cols=['HTTP outcome', 'Processing recorder']
  - Valid signed original bytes: {"http":"200 {\"received\":true}","processed":"processed events: 1."}
  - Modified bytes with the original signature: {"http":"400 {\"detail\":\"Invalid signature\"}","processed":"processed events: 0."}
  - Absent signature: {"http":"400 {\"detail\":\"Invalid signature\"}","processed":"processed events: 0."}

### s02 · explainer · Keep the boundary clear
Work the boundary — 
(walkthrough) Modified bytes must fail verification even when the body still parses. Verify first; process only the verified event. ⟦A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Choose the boundary
Check — 

### s04 · hands_on · Apply the contract
Practice — 

### s05 · recap · Take the rule with you
(takeaway) Modified bytes must fail verification even when the body still parses. Verify first; process only the verified event. ⟦A.f1 A.f2 A:tb5⟧
[UP NEXT] Diagnose service failures from emitted and interpreted evidence: An order endpoint becomes slow and emits failures. Changing code at the endpoint immediately may miss where the first delay or failure actually occurred.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: Webhook authenticity verification
(definition) Reject absent or invalid signatures before processing. Keep the secret and internal verification details out of responses. ⟦A.f3 A:tb3 A:tb4⟧
(definition) Test valid, modified-body and missing-signature deliveries: only the valid signed delivery may reach processing. ⟦A.f4 A:tb3 A:tb4⟧
(misconception) For the supplied signed delivery, compare unchanged raw bytes with the modified-body case and the absent-signature case. Only verified input reaches process_event; parsing a modified body successfully does not make its signature valid. ⟦A.f3 A.f4 A:tb3 A:tb4⟧
### r02 · Review: Webhook authenticity verification
(definition) Acquire raw bytes with await request.body() before parsing or changing the body. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) For every delivery, use the publisher-supported SDK or verifier with those bytes and the endpoint signing secret. Follow its signing format; invent no canonicalization. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Reject absent or invalid signatures before processing. Keep the secret and internal verification details out of responses. ⟦A.f3 A:tb3 A:tb4⟧
(definition) Test valid, modified-body and missing-signature deliveries: only the valid signed delivery may reach processing. ⟦A.f4 A:tb3 A:tb4⟧
(misconception) For the supplied signed delivery, compare unchanged raw bytes with the modified-body case and the absent-signature case. Only verified input reaches process_event; parsing a modified body successfully does not make its signature valid. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· blocks.title: Counts are measured independently after clearing the recorder.
· cells.http: 200 {"received":true}
· cells.http: 400 {"detail":"Invalid signature"}
· cells.http: 400 {"detail":"Invalid signature"}

=========

# EVALUATOR PACKET — Diagnose service failures from emitted and interpreted evidence (tile_087)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = observability.evidence_based_service_diagnosis — Diagnose service failures from emitted and interpreted evidence

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (observability.evidence_based_service_diagnosis)   objective: Localize service failures: investigate one supplied failure.
A.f1: Compare request rate, failure fraction and latency for the affected operation and time window before choosing a diagnostic boundary, distinguishing increased traffic from increased failures or longer waits.   [sources: prometheus_client_python#https://prometheus.io/docs/prometheus/latest/querying/functions/#rate, prometheus_client_python#https://prometheus.github.io/client_python/instrumenting/histogram/#constructor]
A.f2: Follow the affected interaction identifier through related local and outbound logs to locate the first recorded failure or delayed operation rather than assuming the endpoint's final error identifies its origin.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#event-attributes]
A.f3: Compare integration timeout evidence and emitted database work with the failing request's log context to distinguish an upstream wait from persistence work or a local input rejection.   [sources: fastapi_docs_advanced#https://www.python-httpx.org/advanced/timeouts/#fine-tuning-the-configuration, sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#working-with-transactions-and-the-dbapi]
A.f4: Reproduce the supplied failure with a controlled request, record the observed outcome and related evidence, and change the suspected boundary only after checking that the evidence supports that location.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#verification, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/testing/#using-testclient]
note: Establish this first: Multiple signals narrow location before code changes.
note: Stay within the current objective: Localize service failures. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Choose diagnostic boundaries from signals.
PRACTICE ANCHOR (live_code): Investigate the supplied order-endpoint failure. Compare the supplied request-rate, failure-fraction and latency evidence for the affected operation and time window. Write one controlled request using the supplied test setup, record its outcome, and follow its interaction identifier through the supplied local, outbound and database evidence before choosing a diagnostic boundary.  SUCCESS: The controlled request reproduces the supplied failure and its outcome is recorded. The investigation distinguishes traffic growth from increased failures or latency, identifies the first recorded failure or delay, and compares timeout evidence with emitted database work and local input handling. The selected boundary is supported by that evidence rather than by the endpoint's final error alone; any proposed change remains separate from the observations.
ASSESSMENT ANCHOR: distinguish_traffic_growth_from_failures_and_latency facts=['f1']
ASSESSMENT ANCHOR: locate_first_recorded_failure_in_correlated_logs facts=['f2']
ASSESSMENT ANCHOR: distinguish_upstream_persistence_and_input_boundaries facts=['f3']
ASSESSMENT ANCHOR: verify_suspected_boundary_with_controlled_reproduction facts=['f4']

## DATA ASSETS USED
ds.correlated_records: Synthetic correlated failure evidence — columns: interaction_id(identifier), offset_ms(numerical), boundary(categorical), event(categorical), sql_statement_count(numerical)
   ["interaction_fixture",0,"local","request_received",0]
   ["interaction_fixture",5,"database","lookup_complete",1]
   ["interaction_fixture",10,"outbound","lookup_started",0]
   ["interaction_fixture",2010,"outbound","timeout",0]
   ["interaction_fixture",2025,"local","response_504",0]
ds.operation_signals: Synthetic operation-window evidence — columns: operation(categorical), window(categorical), request_count(numerical), window_seconds(numerical), failure_count(numerical), latency_ms(numerical)
   ["create_order","baseline",60,60,0,25.0]
   ["create_order","affected",60,60,12,2025.0]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authentication and authorization tests including invalid-token rejection; Bounded retry decisions respecting HTTP idempotency; Bounding payloads, expensive requests and API resource consumption; Database test-state isolation; Declaring the deployed bearer-access-token and authorization-server security contract without a password grant; Endpoint authorization with required permissions or scopes; Established authorization-server integration using authorization code and PKCE where applicable; no resource-owner password grant; Inspecting generated OpenAPI for drift and sensitive exposure; Object-level authorization against the authenticated principal; Recognizing and avoiding redundant ORM queries; Webhook delivery idempotency; Webhook replay freshness

## LESSON, in learner order

### s01 · explainer · Diagnose service failures from emitted and interpreted evidence
Learn the rule — 
(definition) Compare request rate, failure fraction and latency for the same affected operation and window. Separate traffic growth from more failures or longer waits before choosing a boundary. ⟦A.f1 A:tb2⟧
(definition) Trace the interaction identifier through local and outbound logs to the first recorded failure or delay; the final endpoint error need not identify its origin. ⟦A.f2 A:tb3⟧
(definition) Compare integration timeouts and emitted database work with that request’s log context to separate upstream waiting, persistence work and local input rejection. ⟦A.f3 A:tb3⟧
(definition) Reproduce the supplied failure with a controlled request. Record outcome and related evidence; change the suspected boundary only when evidence supports that location. ⟦A.f4 A:tb3⟧
[SIDE_BY_SIDE] Record observed outcome; corroborate the suspected boundary with a controlled request. left_label: Operation-window signals | right_label: Interaction-correlated timeline
  left:
[TABLE computed result ] caption: Compare the same operation/window: rate, failure fraction and latency.
  produced by sql: SELECT operation, "window", request_count * 1.0 / window_seconds AS request_rate_per_second, failure_count * 1.0 / request_count AS failure_fraction, latency_ms FROM signals
  right:
[TABLE computed result ] caption: Read chronologically within each interaction; locate first supported delay/failure before changing code.
  produced by sql: SELECT * FROM records ORDER BY interaction_id, offset_ms

### s02 · explainer · Keep the boundary clear
Work the boundary — 
(walkthrough) The final endpoint error is an observation, not proof of origin. Follow correlated evidence before changing a boundary. ⟦A.f2 A.f4 A:tb4 A:tb5⟧

### s03 · check · Choose the boundary
Check — 

### s04 · hands_on · Apply the contract
Practice — 

### s05 · recap · Take the rule with you
(takeaway) The final endpoint error is an observation, not proof of origin. Follow correlated evidence before changing a boundary. ⟦A.f2 A.f4 A:tb5⟧
[UP NEXT] Bounding payloads, expensive requests and API resource consumption: An API accepts untrusted work, so budgets should limit the expensive operation rather than merely describe it.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: Diagnose service failures from emitted and interpreted evidence
(definition) Compare integration timeouts and emitted database work with that request’s log context to separate upstream waiting, persistence work and local input rejection. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) The final endpoint error is an observation, not proof of origin. Follow correlated evidence before changing a boundary. ⟦A.f3 A:tb3 A:tb4⟧
[TABLE ds.correlated_records cols=['interaction_id', 'offset_ms', 'boundary', 'event', 'sql_statement_count'] ] caption: Synthetic correlated failure evidence
### r02 · Review: Diagnose service failures from emitted and interpreted evidence
(definition) Compare request rate, failure fraction and latency for the same affected operation and window. Separate traffic growth from more failures or longer waits before choosing a boundary. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Trace the interaction identifier through local and outbound logs to the first recorded failure or delay; the final endpoint error need not identify its origin. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Reproduce the supplied failure with a controlled request. Record outcome and related evidence; change the suspected boundary only when evidence supports that location. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) The final endpoint error is an observation, not proof of origin. Follow correlated evidence before changing a boundary. ⟦A.f1 A.f2 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.correlated_records cols=['interaction_id', 'offset_ms', 'boundary', 'event', 'sql_statement_count'] ] caption: Synthetic correlated failure evidence

=========

# EVALUATOR PACKET — Bounding payloads, expensive requests and API resource consumption (tile_088)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = security.bounded_api_resources — Bounding payloads, expensive requests and API resource consumption

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (security.bounded_api_resources)   objective: Bound API resource use: apply one costly endpoint's budget.
A.f1: Apply finite limits to expensive untrusted operations, including input size, result count, operation duration and costly concurrent work rather than accepting unrestricted resource consumption.   [sources: owasp_api_security_top10_2023#https://api-security.owasp.org/editions/2023/en/0xa4-unrestricted-resource-consumption/#how-to-prevent]
A.f2: Enforce an actual body-byte limit with maintained middleware and constrain caller-selected batch or page sizes with Field bounds rather than trusting claimed sizes.   [sources: fastapi_docs_advanced#https://starlette.dev/middleware/#requestbodylimitmiddleware, pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/fields/#numeric-constraints]
A.f3: Configure finite dependency timeouts and a supplied Uvicorn --limit-concurrency budget where the service policy needs to bound concurrent accepted work.   [sources: fastapi_docs_advanced#https://www.python-httpx.org/advanced/timeouts/#setting-and-disabling-timeouts, fastapi_docs_tutorial#https://uvicorn.dev/settings/#resource-limits]
A.f4: Test an input within the supplied budget and one beyond it, asserting that excess work is rejected before the expensive operation and accepted work retains the intended contract.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/testing/#using-testclient, fastapi_docs_advanced#https://starlette.dev/middleware/#requestbodylimitmiddleware]
note: Establish this first: Untrusted operations need finite budgets.
note: Stay within the current objective: Bound API resource use. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify unbounded expensive operations.
PRACTICE ANCHOR (live_code): Apply supplied resource budgets to one costly batch endpoint: configure maintained body-byte middleware, bound batch size with Field, configure a finite outbound dependency timeout, and apply the supplied Uvicorn concurrency setting. Verify accepted and over-budget requests.  SUCCESS: An input within the supplied budgets retains the endpoint's intended response contract. Oversized bodies and excessive batch sizes are rejected without invoking the expensive dependency. The dependency timeout and Uvicorn concurrency setting match the supplied finite budgets.
ASSESSMENT ANCHOR: identify_unbounded_expensive_operations facts=['f1']
ASSESSMENT ANCHOR: distinguish_enforced_input_limits_from_claimed_sizes facts=['f2']
ASSESSMENT ANCHOR: identify_missing_duration_and_concurrency_budgets facts=['f3']
ASSESSMENT ANCHOR: identify_evidence_of_rejection_before_expensive_work facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authentication and authorization tests including invalid-token rejection; Bounded retry decisions respecting HTTP idempotency; Database test-state isolation; Declaring the deployed bearer-access-token and authorization-server security contract without a password grant; Endpoint authorization with required permissions or scopes; Established authorization-server integration using authorization code and PKCE where applicable; no resource-owner password grant; Inspecting generated OpenAPI for drift and sensitive exposure; Object-level authorization against the authenticated principal; Recognizing and avoiding redundant ORM queries; Webhook delivery idempotency; Webhook replay freshness

## LESSON, in learner order

### s01 · explainer · Bounding payloads, expensive requests and API resource consumption
Learn the rule — 
(definition) Put finite limits on expensive untrusted work, including input size, result count, duration and costly concurrency. ⟦A.f1 A:tb2⟧
(definition) Enforce actual body bytes with maintained middleware. Use Field bounds for caller-selected batch or page sizes; claimed sizes are insufficient. ⟦A.f2 A:tb3⟧
(definition) Configure finite dependency timeouts and the supplied Uvicorn --limit-concurrency budget where policy bounds concurrent accepted work. ⟦A.f3 A:tb3⟧
(definition) Test within-budget and over-budget input: reject excess before expensive work while preserving the accepted request’s contract. ⟦A.f4 A:tb3⟧
[CODE python]
# starter.py: supplied finite batch bound
from pydantic import BaseModel, Field
from pathlib import Path
import json
budgets = json.loads(Path("fixtures.json").read_text())["hypothetical_budgets"]
class BatchInput(BaseModel):
    order_ids: list[int] = Field(max_length=budgets["batch_size"])

# application.py: enforce actual bytes and finite dependency wait
import json
from pathlib import Path
import httpx
from fastapi import FastAPI, Depends
from starlette.middleware.body_limit import RequestBodyLimitMiddleware
from starter import BatchInput
budgets = json.loads(Path('fixtures.json').read_text())['hypothetical_budgets']
app = FastAPI()
app.add_middleware(RequestBodyLimitMiddleware, max_body_size=budgets["body_bytes"])
expensive_calls = 0
outbound_timeout = httpx.Timeout(budgets["dependency_timeout_seconds"])
async def expensive_dependency(value: BatchInput):
    global expensive_calls
    expensive_calls += 1
    transport=httpx.MockTransport(lambda request:httpx.Response(200,json={'available':True}))
    async with httpx.AsyncClient(transport=transport,timeout=outbound_timeout) as http:
        response=await http.get('http://controlled-dependency.invalid/lookup')
        return response.json()['available']
@app.post('/orders/batch')
async def batch(value: BatchInput, available=Depends(expensive_dependency)):
    return {'accepted':len(value.order_ids)}

# Supplied launch policy
# uvicorn application:app --host 127.0.0.1 --port 8000 --limit-concurrency 8

import json
from pathlib import Path
import application
from fastapi.testclient import TestClient
import pytest
fixtures = json.loads(Path('fixtures.json').read_text())
@pytest.mark.parametrize('condition', ['within_batch','beyond_batch','within_body','beyond_body'])
def test_boundary(condition):
    calls = []
    async def counted(value: application.BatchInput):
        calls.append(True)
        return True
    previous = application.app.dependency_overrides.copy()
    application.app.dependency_overrides[application.expensive_dependency] = counted
    try:
        with TestClient(application.app) as client:
            if condition == 'beyond_body':
                response = client.post('/orders/batch', content=fixtures[condition], headers={'Content-Type':'application/json'})
            else:
                response = client.post('/orders/batch', json=fixtures[condition])
            if condition in ('within_batch', 'within_body'):
                assert response.status_code == 200
                assert response.json() == {'accepted': len(fixtures[condition]['order_ids'])}
                assert calls == [True]
            elif condition == 'beyond_batch':
                assert response.status_code == 422
                assert calls == []
            else:
                assert response.status_code == 413
                assert response.text == 'Content Too Large'
                assert calls == []
    finally:
        application.app.dependency_overrides.clear()
        application.app.dependency_overrides.update(previous)

  annotations: ['Batch count is not body size. Test byte and batch limits independently, and check rejection before costly dependency invocation.']

### s02 · explainer · Keep the boundary clear
Work the boundary — 
(walkthrough) A bounded batch can still have an oversized body. Size, result count, duration and costly concurrency need their supplied limits. ⟦A.f1 A.f2 A:tb4 A:tb5⟧

### s03 · check · Choose the boundary
Check — 

### s04 · check · Choose the boundary
Check — 

### s05 · hands_on · Apply the contract
Practice — 

### s06 · recap · Take the rule with you
(takeaway) A bounded batch can still have an oversized body. Size, result count, duration and costly concurrency need their supplied limits. ⟦A.f1 A:tb5⟧
[UP NEXT] Recognizing and avoiding redundant ORM queries: Listing several parent entities can hide extra database round trips when their relationships are accessed individually. Inspect emitted SQL rather than counting only explicit selects in the handler.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: Bounding payloads, expensive requests and API resource consumption
(definition) Put finite limits on expensive untrusted work, including input size, result count, duration and costly concurrency. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Enforce actual body bytes with maintained middleware. Use Field bounds for caller-selected batch or page sizes; claimed sizes are insufficient. ⟦A.f2 A:tb3 A:tb4⟧
(misconception) This fictional budget uses 256 body bytes and 3 batch items. A passing batch-size check does not establish the independent body-byte boundary. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Review: Bounding payloads, expensive requests and API resource consumption
(definition) Test within-budget and over-budget input: reject excess before expensive work while preserving the accepted request’s contract. ⟦A.f4 A:tb3 A:tb4⟧
(misconception) This fictional budget uses 256 body bytes and 3 batch items. A passing batch-size check does not establish the independent body-byte boundary. ⟦A.f4 A:tb3 A:tb4⟧
### r03 · Review: Bounding payloads, expensive requests and API resource consumption
(definition) Configure finite dependency timeouts and the supplied Uvicorn --limit-concurrency budget where policy bounds concurrent accepted work. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) This fictional budget uses 256 body bytes and 3 batch items. A passing batch-size check does not establish the independent body-byte boundary. ⟦A.f3 A:tb3 A:tb4⟧

=========

# EVALUATOR PACKET — Recognizing and avoiding redundant ORM queries (tile_089)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = sqlalchemy.redundant_queries — Recognizing and avoiding redundant ORM queries

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (sqlalchemy.redundant_queries)   objective: Recognize N+1 access: remove one N+1 listing read.
A.f1: Lazy relationship access can emit additional SELECT statements; iterating parent entities and loading each parent's relationship separately can produce an N+1 query pattern.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#loader-strategies]
A.f2: Add selectinload(Entity.relationship_attribute) through statement.options(...) to fetch a collection relationship for the selected parents with an additional batched query rather than one query per parent.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#selectin-load]
A.f3: joinedload(...) is an alternative eager-loading strategy using a join; when loading a collection this way, apply Result.unique() as required to deduplicate parent entities.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#joined-load]
A.f4: Compare emitted SQL before and after the loading change with engine echo=True logging enabled, confirming both reduced relationship queries and unchanged returned entity data.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#loader-strategies, sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#working-with-transactions-and-the-dbapi]
note: Establish this first: Object navigation can hide database round trips.
note: Stay within the current objective: Recognize N+1 access. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify repeated relationship queries.
PRACTICE ANCHOR (live_code): Update one parent-entity listing statement with selectinload(Entity.relationship_attribute) so its collection relationship is loaded in batches, then compare SQL and returned entity data before and after.  SUCCESS: The listing uses statement.options(selectinload(Entity.relationship_attribute)); echo logging confirms fewer relationship SELECTs, and the returned parents and their collection contents remain unchanged.
ASSESSMENT ANCHOR: identify_repeated_relationship_selects facts=['f1']
ASSESSMENT ANCHOR: distinguish_per_parent_queries_from_batched_collection_loading facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_query_reduction_without_changing_returned_data facts=['f4']

## DATA ASSETS USED
ds.Entity: Parent entities — columns: id(identifier,digits-as-label)
   [11]
   [22]
   [33]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authentication and authorization tests including invalid-token rejection; Bounded retry decisions respecting HTTP idempotency; Database test-state isolation; Declaring the deployed bearer-access-token and authorization-server security contract without a password grant; Endpoint authorization with required permissions or scopes; Established authorization-server integration using authorization code and PKCE where applicable; no resource-owner password grant; Inspecting generated OpenAPI for drift and sensitive exposure; Object-level authorization against the authenticated principal; Webhook delivery idempotency; Webhook replay freshness

## LESSON, in learner order

### s01 · explainer · Recognizing and avoiding redundant ORM queries
Learn the rule — 
(definition) Lazy relationship access can emit extra SELECTs. Loading a relationship separately for each parent can produce N+1 queries. ⟦A.f1 A:tb2⟧
(definition) Use statement.options(selectinload(Entity.relationship_attribute)) to fetch the selected parents’ collection with an additional batched query, not one per parent. ⟦A.f2 A:tb3⟧
(definition) joinedload(...) instead uses a join. For collection loading, apply Result.unique() as required to deduplicate parents. ⟦A.f3 A:tb3⟧
(definition) Compare emitted SQL before and after with engine echo=True; confirm fewer relationship queries and unchanged returned entity data. ⟦A.f4 A:tb3⟧
[SIDE_BY_SIDE] Capture emitted SQL in fresh sessions with echo=True; compare fewer relationship queries and identical entity data. Outputs belong to execution. left_label: Before: lazy per-parent access | right_label: After: batched collection loading
  left:
[CODE python]
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

  annotations: []
  right:
[CODE python]
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
    statement = statement.options(selectinload(Entity.relationship_attribute))
    parents = session.execute(statement).scalars().all()
    return [{'id':p.id, 'children':[c.id for c in p.relationship_attribute]} for p in parents]
# Run baseline and changed listing in separate fresh sessions and capture echo
# output; do not reuse already-loaded relationships when measuring the change.
if __name__ == '__main__':
    with Session(engine) as session:
        print(listing(session))

  annotations: []
[COMPARISON] cols=['Captured baseline SQL and results', 'Expected illustration — not captured execution evidence']
  - Query-pattern summary: {"baseline":"Captured baseline: one parent SELECT, then relationship SELECTs with parent parameters (11,), (22,), and (33,). Returned data: [{\"id\":11,\"children\":[111,112]},{\"id\":22,\"children\":[221]},{\"id\":33,\"children\":[]}].","revised":"Expected selectinload pattern for these three parents: the same parent SELECT, then one relationship SELECT using WHERE relationship_attribute.parent_i
  - SQL panel: {"baseline":"BEGIN (implicit)\nSELECT \"Entity\".id \nFROM \"Entity\" ORDER BY \"Entity\".id\n LIMIT ? OFFSET ?\n[generated in 0.00006s] (3, 0)\nSELECT relationship_attribute.id, relationship_attribute.parent_id \nFROM relationship_attribute \nWHERE ? = relationship_attribute.parent_id\n[generated in 0.00006s] (11,)\nSELECT relationship_attribute.id, relationship_attribute.parent_id \nFROM relatio
  - Returned collections: {"baseline":"[{\"id\":11,\"children\":[111,112]},{\"id\":22,\"children\":[221]},{\"id\":33,\"children\":[]}]","revised":"Expected identical returned data: [{\"id\":11,\"children\":[111,112]},{\"id\":22,\"children\":[221]},{\"id\":33,\"children\":[]}]"}

### s02 · explainer · Keep the boundary clear
Work the boundary — 
(walkthrough) Unchanged entity data does not prove unchanged database work. Check emitted SQL as well as the returned collections. ⟦A.f4 A:tb4 A:tb5⟧

### s03 · video · Recognizing and avoiding redundant ORM queries
[VIDEO ] bridge-before:  | bridge-after: 

### s04 · check · Choose the boundary
Check — 

### s05 · check · Choose the boundary
Check — 

### s06 · hands_on · Apply the contract
Practice — 

### s07 · recap · Take the rule with you
(takeaway) Unchanged entity data does not prove unchanged database work. Check emitted SQL as well as the returned collections. ⟦A.f1 A:tb5⟧
[UP NEXT] Database test-state isolation: A database test must see its own writes without leaving them behind for the next test. The fixture, session override and transaction boundary should form one isolated setup.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: Recognizing and avoiding redundant ORM queries
(definition) Lazy relationship access can emit extra SELECTs. Loading a relationship separately for each parent can produce N+1 queries. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Use statement.options(selectinload(Entity.relationship_attribute)) to fetch the selected parents’ collection with an additional batched query, not one per parent. ⟦A.f2 A:tb3 A:tb4⟧
(misconception) Unchanged entity data does not prove unchanged database work. Check emitted SQL as well as the returned collections. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.Entity cols=['id'] ] caption: Parent entities
### r02 · Review: Recognizing and avoiding redundant ORM queries
(definition) Compare emitted SQL before and after with engine echo=True; confirm fewer relationship queries and unchanged returned entity data. ⟦A.f4 A:tb3 A:tb4⟧
(misconception) Unchanged entity data does not prove unchanged database work. Check emitted SQL as well as the returned collections. ⟦A.f4 A:tb3 A:tb4⟧
[TABLE ds.Entity cols=['id'] ] caption: Parent entities
### r03 · Review: Recognizing and avoiding redundant ORM queries
(definition) Lazy relationship access can emit extra SELECTs. Loading a relationship separately for each parent can produce N+1 queries. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(misconception) Unchanged entity data does not prove unchanged database work. Check emitted SQL as well as the returned collections. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
[TABLE ds.Entity cols=['id'] ] caption: Parent entities

## OTHER CONTENT (fields without a dedicated renderer)
· blocks.title: SQL query pattern and returned collections
· cells.baseline: Captured baseline: one parent SELECT, then relationship SELECTs with parent parameters (11,), (22,), and (33,). Returned data: [{"id":11,"children":[111,112]},{"id":22,"children":[221]},{"id":33,"children":[]}].
· cells.revised: Expected selectinload pattern for these three parents: the same parent SELECT, then one relationship SELECT using WHERE relationship_attribute.parent_id IN (?, ?, ?) with parameters (11,22,33). Expected returned data are identical.
· cells.baseline: BEGIN (implicit)
SELECT "Entity".id 
FROM "Entity" ORDER BY "Entity".id
 LIMIT ? OFFSET ?
[generated in 0.00006s] (3, 0)
SELECT relationship_attribute.id, relationship_attribute.parent_id 
FROM relationship_attribute 
WHERE ? = relationship_attribute.parent_id
[generated in 0.00006s] (11,)
SELECT relationship_attribute.id, relationship_attribute.parent_id 
FROM relationship_attribute 
WHERE ? = relationship_attribute.parent_id
[cached since 0.0003609s ago] (22,)
SELECT relationship_attribute.id, relationship_attribute.parent_id 
FROM relationship_attribute 
WHERE ? = relationship_attribute.parent_id
[cached since 0.0005504s ago] (33,)
ROLLBACK

· cells.revised: Expected illustration: same parent SELECT; then SELECT relationship_attribute.parent_id, relationship_attribute.id FROM relationship_attribute WHERE relationship_attribute.parent_id IN (?, ?, ?) with parameters (11,22,33).
· cells.baseline: [{"id":11,"children":[111,112]},{"id":22,"children":[221]},{"id":33,"children":[]}]
· cells.revised: Expected identical returned data: [{"id":11,"children":[111,112]},{"id":22,"children":[221]},{"id":33,"children":[]}]

=========

# EVALUATOR PACKET — Database test-state isolation (tile_090)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = testing.database_state_isolation — Database test-state isolation

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (testing.database_state_isolation)   objective: Isolate database tests: make two tests order independent.
A.f1: A yield fixture performs setup before yield and teardown afterward, making resource cleanup explicit for each test's scope.   [sources: pytest_getting_started#https://docs.pytest.org/en/stable/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization]
A.f2: For transaction-isolated database tests, open an outer connection transaction, bind the test session to that connection with join_transaction_mode="create_savepoint", and roll back the outer transaction during teardown.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites]
A.f3: Override the application session provider with the test session provider, exercise a write through TestClient and read its resulting state through the same test database boundary.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/testing-dependencies/#use-the-app-dependency-overrides-attribute, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/testing/#using-testclient]
A.f4: Close the test session and connection and restore overrides in teardown, verifying that a subsequent test does not inherit the first test's written state.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites, pytest_getting_started#https://docs.pytest.org/en/stable/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization]
note: Establish this first: Each test needs an isolated persistence boundary.
note: Stay within the current objective: Isolate database tests. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Detect persistence leakage.
PRACTICE ANCHOR (live_code): Make two existing database tests order independent: one writes an item through TestClient and verifies its state, while the other verifies that the item is absent within its own isolated database boundary.  SUCCESS: Both tests pass in either execution order. The writing test reads its own resulting state, and the other test never inherits that write. Teardown closes the session and connection, rolls back the outer transaction, and restores dependency overrides.
ASSESSMENT ANCHOR: detect_incomplete_fixture_teardown facts=['f1', 'f4']
ASSESSMENT ANCHOR: detect_writes_outside_the_test_database_boundary facts=['f2', 'f3']
ASSESSMENT ANCHOR: detect_persistence_leakage_between_tests facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authentication and authorization tests including invalid-token rejection; Bounded retry decisions respecting HTTP idempotency; Declaring the deployed bearer-access-token and authorization-server security contract without a password grant; Endpoint authorization with required permissions or scopes; Established authorization-server integration using authorization code and PKCE where applicable; no resource-owner password grant; Inspecting generated OpenAPI for drift and sensitive exposure; Object-level authorization against the authenticated principal; Webhook delivery idempotency; Webhook replay freshness

## LESSON, in learner order

### s01 · explainer · Database test-state isolation
Learn the rule — 
(definition) A yield fixture sets up before yield and tears down afterward, making cleanup explicit for its test scope. ⟦A.f1 A:tb2⟧
(definition) Open an outer connection transaction; bind Session to that connection with join_transaction_mode="create_savepoint". Roll back the outer transaction during teardown. ⟦A.f2 A:tb3⟧
(definition) Override the application session provider with the test provider. Write through TestClient and read resulting state across the same test database boundary. ⟦A.f3 A:tb3⟧
(definition) Close session and connection, restore overrides, and verify a subsequent test does not inherit the earlier write. ⟦A.f4 A:tb3⟧
[CODE python]
import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from application import app, engine, session_provider
@pytest.fixture
def isolated_client():
    original_overrides = app.dependency_overrides.copy()
    connection = engine.connect()
    outer_transaction = connection.begin()
    test_session = Session(bind=connection, join_transaction_mode="create_savepoint")
    def test_provider():
        yield test_session
    app.dependency_overrides[session_provider] = test_provider
    try:
        with TestClient(app) as client:
            yield client, test_session
    finally:
        test_session.close()
        outer_transaction.rollback()
        connection.close()
        app.dependency_overrides.clear()
        app.dependency_overrides.update(original_overrides)
# TODO: test write/read within one boundary; test target absence in another.
# Run both execution orders. Never migrate/create schema inside per-test transaction.

# Tests use this fixture and the supplied item. Run both orders.
import json
from pathlib import Path
item = json.loads(Path('fixtures.json').read_text())['item']
def test_writes_item(isolated_client):
    client, _ = isolated_client
    assert client.post('/items', json=item).json() == item
    assert client.get(f"/items/{item['id']}").json() == item
def test_item_absent(isolated_client):
    client, _ = isolated_client
    response = client.get(f"/items/{item['id']}")
    assert response.status_code == 404
    assert response.json() == {'detail':'Not found'}

  annotations: []

### s02 · explainer · Keep the boundary clear
Work the boundary — 
(walkthrough) A successful write/read test is not isolation proof. The next test must start without the earlier write and with restored overrides. ⟦A.f4 A:tb4 A:tb5⟧

### s03 · video · Database test-state isolation
[VIDEO ] bridge-before:  | bridge-after: 

### s04 · check · Choose the boundary
Check — 

### s05 · check · Choose the boundary
Check — 

### s06 · hands_on · Apply the contract
Practice — 

### s07 · recap · Take the rule with you
(takeaway) A successful write/read test is not isolation proof. The next test must start without the earlier write and with restored overrides. ⟦A.f4 A:tb5⟧
[UP NEXT] Established authorization-server integration using authorization code and PKCE where applicable; no resource-owner password grant: The API needs to accept tokens actually issued by its established authorization server. A locally fabricated token or overridden verifier would not prove that integration.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: Database test-state isolation
(definition) A yield fixture sets up before yield and tears down afterward, making cleanup explicit for its test scope. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Close session and connection, restore overrides, and verify a subsequent test does not inherit the earlier write. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Write/read the supplied item {"id": 1} through the isolated test boundary. Then test its absence in a fresh test. Run both supplied execution orders; a successful first write does not prove the next test starts clean. ⟦A.f1 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Review: Database test-state isolation
(definition) Close session and connection, restore overrides, and verify a subsequent test does not inherit the earlier write. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Write/read the supplied item {"id": 1} through the isolated test boundary. Then test its absence in a fresh test. Run both supplied execution orders; a successful first write does not prove the next test starts clean. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
### r03 · Review: Database test-state isolation
(definition) Open an outer connection transaction; bind Session to that connection with join_transaction_mode="create_savepoint". Roll back the outer transaction during teardown. ⟦A.f2 A:tb3 A:tb4⟧
(definition) Override the application session provider with the test provider. Write through TestClient and read resulting state across the same test database boundary. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) Write/read the supplied item {"id": 1} through the isolated test boundary. Then test its absence in a fresh test. Run both supplied execution orders; a successful first write does not prove the next test starts clean. ⟦A.f2 A.f3 A:tb3 A:tb4⟧

=========

# EVALUATOR PACKET — Established authorization-server integration using authorization code and PKCE where applicable; no resource-owner password grant / Endpoint authorization with required permissions or scopes (tile_091)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = auth.authorization_server_integration — Established authorization-server integration using authorization code and PKCE where applicable; no resource-owner password grant
B = auth.endpoint_permissions — Endpoint authorization with required permissions or scopes

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (auth.authorization_server_integration)   objective: Wire one established authorization server's issued access tokens into a FastAPI resource server's existing bearer/JWT verifier: integrate one supplied established authorization-server instance with one protected FastAPI endpoint. Use the supplied client/test harness for authorization-code/PKCE acquisition where applicable; wire its issued access token through the already-taught bearer dependency and JWT verifier. Execute an HTTP test accepting the valid issued token and a test rejecting a tampered token or an issuer-issued token for the wrong API audience. Keep issuer provisioning and client registration supplied; do not build an authorization server, frontend, vendor-console workflow, cryptography implementation or password-grant endpoint.
A.f1: Use the supplied established authorization-server client or test harness to obtain an actual issued access token through authorization code with PKCE where applicable; do not add a resource-owner password-grant endpoint.   [sources: ietf_rfc9700#https://www.rfc-editor.org/rfc/rfc9700.txt#2.1.1, ietf_rfc9700#https://www.rfc-editor.org/rfc/rfc9700.txt#2.4]
A.f2: Configure the supplied client with its registered client identifier, authorization and token endpoints and redirect URI; complete the code redirect and the separate token POST with the matching PKCE verifier using that client.   [sources: ietf_rfc9700#https://www.rfc-editor.org/rfc/rfc6749.html#4.1.1, ietf_rfc9700#https://www.rfc-editor.org/rfc/rfc6749.html#4.1.3, ietf_rfc9700#https://www.rfc-editor.org/rfc/rfc9700.txt#2.1.1]
A.f3: Configure the existing verifier with the supplied issuer's trusted JWKS URL, expected issuer, allowed algorithms and API audience; resolve a signing key with PyJWKClient and require the intended claims during jwt.decode.   [sources: fastapi_docs_tutorial#https://pyjwt.readthedocs.io/en/latest/usage.html#retrieve-rsa-signing-keys-from-a-jwks-endpoint, fastapi_docs_tutorial#https://pyjwt.readthedocs.io/en/latest/api.html#jwt.decode]
A.f4: Send the issuer's issued access token to the protected endpoint as Authorization: Bearer token so the request executes the real bearer extraction and configured verifier.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/reference/security/#fastapi.security.HTTPBearer, ietf_rfc9700#https://www.rfc-editor.org/rfc/rfc6749.html#7]
A.f5: Execute an HTTP assertion accepting the valid issuer-issued token and another rejecting a tampered token or an issuer-issued token for the wrong API audience; keep authentication and verification dependencies active rather than overriding them or fabricating a locally valid token.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/testing/#using-testclient, fastapi_docs_tutorial#https://pyjwt.readthedocs.io/en/latest/usage.html#audience-claim-aud, fastapi_docs_tutorial#https://pyjwt.readthedocs.io/en/latest/usage.html#registered-claim-names]
note: Establish this first: The issuer produces authority; the API accepts it only through a configured trust boundary. Integration is proved by exercising real issued tokens through the resource-server verifier, not by specifying a flow or substituting authentication..
note: Stay within the current objective: Wire one established authorization server's issued access tokens into a FastAPI resource server's existing bearer/JWT verifier.. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Demonstrate executable issuer-to-API wiring: obtain an access token from the selected established authorization server using a supplied client or test harness (authorization code with PKCE where applicable), configure the API's existing verifier for that issuer's verification keys, expected issuer and API audience, and show through HTTP tests that a valid issued access token is accepted while an invalid or contextually wrong token is rejected. Authentication or verifier overrides and locally fabricated valid tokens do not satisfy this assessment..
PRACTICE ANCHOR (live_code): Integrate the supplied established authorization server with one protected FastAPI endpoint. Configure the supplied registered client or harness, acquire an issued access token through authorization code with PKCE where applicable, configure the existing bearer/JWT verifier, and execute HTTP assertions for acceptance and rejection.  SUCCESS: An actual issuer-issued access token is accepted by the protected endpoint, and a tampered token or an issuer-issued token for the wrong API audience is rejected. Both requests execute the real bearer extraction and configured verifier without authentication overrides or locally fabricated valid tokens.
ASSESSMENT ANCHOR: obtain_issuer_issued_access_token_with_supplied_client facts=['f1', 'f2']
ASSESSMENT ANCHOR: configure_existing_verifier_for_supplied_issuer facts=['f3']
ASSESSMENT ANCHOR: prove_issuer_integration_through_real_http_requests facts=['f4', 'f5']

## SOURCE FACTS — B (auth.endpoint_permissions)   objective: Enforce endpoint permissions: add one role or scope check.
B.f1: OAuth2 scopes express permissions requested or granted for protected operations; authentication alone does not establish that all operation permissions are present.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/#oauth2-scopes-and-openapi]
B.f2: Declare Security(provider, scopes=[...]) on a protected operation and accept SecurityScopes in the provider to access the operation's required scopes.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/#use-securityscopes]
B.f3: Compare each required scope with the scopes in the verified token context and reject the request if a required scope is absent.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/#verify-the-scopes]
B.f4: Test a verified token with the required scope and another without it, asserting that only the sufficiently scoped request succeeds.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/testing/#using-testclient, fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/#verify-the-scopes]
note: Establish this first: Identity is evaluated against operation policy.
note: Stay within the current objective: Enforce endpoint permissions. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine permission for an operation.
PRACTICE ANCHOR (live_code): Add an orders:write scope requirement to an order-modification operation and enforce it against the verified token context.  SUCCESS: The operation declares orders:write through Security, the provider checks every required scope, and two otherwise verified requests demonstrate that only the request carrying orders:write succeeds.
ASSESSMENT ANCHOR: determine_operation_permission_from_verified_scopes facts=['f1', 'f3']
ASSESSMENT ANCHOR: identify_required_scope_declaration_and_enforcement facts=['f2', 'f3']
ASSESSMENT ANCHOR: verify_permission_behavior_with_sufficient_and_insufficient_scopes facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authentication and authorization tests including invalid-token rejection; Bounded retry decisions respecting HTTP idempotency; Declaring the deployed bearer-access-token and authorization-server security contract without a password grant; Endpoint authorization with required permissions or scopes; Inspecting generated OpenAPI for drift and sensitive exposure; Object-level authorization against the authenticated principal; Webhook delivery idempotency; Webhook replay freshness

## LESSON, in learner order

### s01 · explainer · Established authorization-server integration using authorization code and PKCE where applicable; no resource-owner password grant
Learn the rule — 
(definition) Obtain an actually issued access token using the supplied established client or harness: authorization code with PKCE where applicable, never a resource-owner password endpoint. ⟦A.f1 A:tb2⟧
[PROCESS_FLOW] nodes=['Supplied registered client / endpoints / redirect: {"issuer": "http://127.0.0.1:37353", "authorization_url": "http://127.0.0.1:37353/authorize", "token_url": "http://127.0.0.1:37353/token", "jwks_url": "http://127.0.0.1:37353/jwks", "client_id": "order-training-client", "redirect_uri": "http://127.0.0.1:37353/client/callback", "algorithms": ["RS256"], "required_claims": ["iss", "aud", "sub", "exp", "iat"], "audience": "order-api", "scopes": {"orders:read": "Read orders", "orders:write": "Create orders"}, "pkce": {"required": true, "code_challenge_method": "S256"}, "runtime_boundary": "Publisher-provisioned isolated loopback training issuer; not a public production service."}', 'Authorization redirect with PKCE where applicable', 'Separate token POST with matching verifier → issuer-issued access token', 'Protected HTTP endpoint: Authorization: Bearer token', 'PyJWKClient trusted JWKS key → jwt.decode checks issuer, allowed algorithms, audience and required claims', 'HTTP assertions: accept valid issued token; reject tampered or wrong-audience token; keep real verifier active'] edges=[('n0', 'n1', None), ('n1', 'n2', None), ('n2', 'n3', None), ('n3', 'n4', None), ('n4', 'n5', None)] alt: Supplied registered client / endpoints / redirect: {"issuer": "http://127.0.0.1:37353", "authorization_url": "http://127.0.0.1:37353/authorize", "token_url": "http://127.0.0.1:37353/token", "jwks_url": "http://127.0.0.1:37353/jwks", "client_id": "order-training-client", "redirect_uri": "http://127.0.0.1:37353/client/callback", "algorithms": ["RS256"], "required_claims": ["iss", "aud", "sub", "exp", "iat"], "audience": "order-api", "scopes": {"orders:read": "Read orders", "orders:write": "Create orders"}, "pkce": {"required": true, "code_challenge_method": "S256"}, "runtime_boundary": "Publisher-provisioned isolated loopback training issuer; not a public production service."}; Authorization redirect with PKCE where applicable; Separate token POST with matching verifier → issuer-issued access token; Protected HTTP endpoint: Authorization: Bearer token; PyJWKClient trusted JWKS key → jwt.decode checks issuer, allowed algorithms, audience and required claims; HTTP assertions: accept valid issued token; reject tampered or wrong-audience token; keep real verifier active

### s02 · explainer · Established authorization-server integration using authorization code and PKCE where applicable; no resource-owner password grant
Learn the rule — 
(definition) Configure registered client ID, authorization/token endpoints and redirect URI. Complete the code redirect and separate token POST with the matching PKCE verifier. ⟦A.f2 A:tb3⟧
(definition) Configure the existing verifier’s trusted JWKS URL, issuer, allowed algorithms and API audience. Resolve the key with PyJWKClient and require intended claims in jwt.decode. ⟦A.f3 A:tb3⟧
(definition) Send the issued access token as Authorization: Bearer token to the protected endpoint, exercising real extraction and verification. ⟦A.f4 A:tb3⟧
(definition) Assert HTTP acceptance for the valid issued token and rejection for tampering or wrong API audience. Keep verification active; neither override it nor fabricate locally valid tokens. ⟦A.f5 A:tb3⟧

### s03 · explainer · Keep the boundary clear
Work the boundary — 
(walkthrough) A fabricated valid token would bypass the acquisition evidence. Use the issued token and keep the API’s real verifier active. ⟦A.f1 A.f4 A.f5 A:tb4 A:tb5⟧

### s04 · check · Choose the boundary
Check — 

### s05 · hands_on · Apply the contract
Practice — 

### s06 · explainer · Endpoint authorization with required permissions or scopes
Learn the rule — 
(definition) OAuth2 scopes express requested or granted operation permissions. Authentication alone does not establish every permission. ⟦B.f1 B:tb2⟧
(definition) Declare Security(provider, scopes=[...]) on the operation. Accept SecurityScopes in the provider to read required scopes. ⟦B.f2 B:tb3⟧
(definition) Compare every required scope with the verified token context; reject if any required scope is absent. ⟦B.f3 B:tb3⟧
(definition) Test verified tokens with and without the required scope: only the sufficiently scoped request succeeds. ⟦B.f4 B:tb3⟧
[CODE python]
from fastapi import Depends, HTTPException
from fastapi.security import SecurityScopes
from security import verified_token_context
# Active verification remains a dependency, not a plain unbound parameter.
def require_permissions(security_scopes: SecurityScopes,
                        verified_context=Depends(verified_token_context)):
    for required in security_scopes.scopes:
        if required not in verified_context["scopes"]:
            raise HTTPException(403, "Forbidden")
    return verified_context
# Wire Security(provider, scopes=['orders:write']) for the supplied order-modification operation.

import json
from pathlib import Path
from fastapi import FastAPI, Depends, Security
from pydantic import BaseModel
from security import verified_token_context
from starter import require_permissions
app=FastAPI()
fixtures=json.loads(Path('fixtures.json').read_text())
order={key:fixtures['order'][key] for key in ['id','status']}
class Modification(BaseModel):
    status: str
@app.patch('/orders/'+str(fixtures['order']['id']))
def modify_order(body:Modification, context=Security(require_permissions, scopes=["orders:write"])):
    # Security passes orders:write to require_permissions; the verified-token dependency remains active.
    order['status']=body.status
    return dict(order)

import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from application import app, order, fixtures
@pytest.mark.parametrize('condition',['verified_with_permission','verified_without_permission'])
def test_modify(condition):
    tokens=json.loads(Path('bearer_fixtures.json').read_text())
    order.update({key:fixtures['order'][key] for key in ['id','status']})
    with TestClient(app) as client:
        response=client.patch('/orders/'+str(fixtures['order']['id']),json=fixtures['modification'],
                              headers={'Authorization':'Bearer '+tokens[condition]})
        # TODO: assert 200/public result for sufficiently scoped context;
        # separately 403 {"detail":"Forbidden"} and unchanged order for no scope.

  annotations: []

### s07 · explainer · Keep the boundary clear
Work the boundary — 
(walkthrough) A verified token can still lack the operation’s required permission. Check every required scope, not just whether authentication succeeded. ⟦B.f1 B.f3 B:tb4 B:tb5⟧

### s08 · check · Choose the boundary
Check — 

### s09 · hands_on · Apply the contract
Practice — 

### s10 · recap · Take the rule with you
(takeaway) A fabricated valid token would bypass the acquisition evidence. Use the issued token and keep the API’s real verifier active. ⟦A.f1 A.f4 A.f5 A:tb5⟧
(takeaway) A verified token can still lack the operation’s required permission. Check every required scope, not just whether authentication succeeded. ⟦B.f1 B.f3 B:tb5⟧
[UP NEXT] Webhook delivery idempotency: A webhook event can arrive twice or concurrently. Prevent repeated business effects with durable authenticated event identity, not only a process-local memory check.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: Established authorization-server integration using authorization code and PKCE where applicable; no resource-owner password grant
(definition) Send the issued access token as Authorization: Bearer token to the protected endpoint, exercising real extraction and verification. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(definition) Assert HTTP acceptance for the valid issued token and rejection for tampering or wrong API audience. Keep verification active; neither override it nor fabricate locally valid tokens. ⟦A.f5 A:tb3 A:tb4 A:tb5⟧
(misconception) Use the supplied registered client order-training-client and API audience order-api. Obtain the issuer-issued access token through the client, then exercise the protected HTTP endpoint with real verification. ⟦A.f4 A.f5 A:tb3 A:tb4 A:tb5⟧
### r02 · Review: Established authorization-server integration using authorization code and PKCE where applicable; no resource-owner password grant
(definition) Obtain an actually issued access token using the supplied established client or harness: authorization code with PKCE where applicable, never a resource-owner password endpoint. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Configure registered client ID, authorization/token endpoints and redirect URI. Complete the code redirect and separate token POST with the matching PKCE verifier. ⟦A.f2 A:tb3 A:tb4⟧
(definition) Configure the existing verifier’s trusted JWKS URL, issuer, allowed algorithms and API audience. Resolve the key with PyJWKClient and require intended claims in jwt.decode. ⟦A.f3 A:tb3 A:tb4⟧
(definition) Send the issued access token as Authorization: Bearer token to the protected endpoint, exercising real extraction and verification. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(definition) Assert HTTP acceptance for the valid issued token and rejection for tampering or wrong API audience. Keep verification active; neither override it nor fabricate locally valid tokens. ⟦A.f5 A:tb3 A:tb4 A:tb5⟧
(misconception) Use the supplied registered client order-training-client and API audience order-api. Obtain the issuer-issued access token through the client, then exercise the protected HTTP endpoint with real verification. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Review: Endpoint authorization with required permissions or scopes
(definition) Test verified tokens with and without the required scope: only the sufficiently scoped request succeeds. ⟦B.f4 B:tb3 B:tb4⟧
(misconception) The supplied operation requires orders:write. Compare the verified context with those scopes: the supplied no-permission context is still distinct from failed authentication. ⟦B.f4 B:tb3 B:tb4⟧
### r04 · Review: Endpoint authorization with required permissions or scopes
(definition) OAuth2 scopes express requested or granted operation permissions. Authentication alone does not establish every permission. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(definition) Declare Security(provider, scopes=[...]) on the operation. Accept SecurityScopes in the provider to read required scopes. ⟦B.f2 B:tb3 B:tb4⟧
(definition) Compare every required scope with the verified token context; reject if any required scope is absent. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) The supplied operation requires orders:write. Compare the verified context with those scopes: the supplied no-permission context is still distinct from failed authentication. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧

=========

# EVALUATOR PACKET — Webhook delivery idempotency / Webhook replay freshness / Bounded retry decisions respecting HTTP idempotency (tile_093)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi_backend.webhook_delivery_idempotency — Webhook delivery idempotency
B = fastapi_backend.webhook_replay_freshness — Webhook replay freshness
C = integration.bounded_idempotent_retries — Bounded retry decisions respecting HTTP idempotency

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (fastapi_backend.webhook_delivery_idempotency)   objective: Suppress duplicate webhook effects: implement duplicate-safe handling of one event.
A.f1: Use an authenticated publisher event identifier as the deduplication key and retain the deduplication record across application restarts for the required replay window.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html#idempotency-and-duplicate-events]
A.f2: Record the event identifier atomically with its durable state changes in a transaction, backed by a uniqueness constraint, so concurrent deliveries cannot both apply the effect.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html#idempotency-and-duplicate-events, postgresql_docs#https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-UNIQUE-CONSTRAINTS, sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#managing-transactions]
A.f3: Treat an already processed event as a successful duplicate acknowledgment without repeating its state change, and test duplicate and concurrent deliveries separately.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html#idempotency-and-duplicate-events]
note: Establish this first: Persistent event identity suppresses repeated business effects..
note: Stay within the current objective: Suppress duplicate webhook effects. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine effects of repeated event identifiers.
PRACTICE ANCHOR (live_code): Implement duplicate-safe handling of one authenticated order event, recording its publisher event identifier and durable order change in the same transaction.  SUCCESS: The first processing commits one order change and its event record. Sequential duplicates, including after an application restart, receive successful acknowledgments without another change. Concurrent deliveries with the same identifier produce exactly one committed change.
ASSESSMENT ANCHOR: determine_effects_of_repeated_event_identifiers_across_restarts facts=['f1', 'f3']
ASSESSMENT ANCHOR: determine_effects_of_concurrent_deliveries_with_the_same_event_identifier facts=['f2', 'f3']

## SOURCE FACTS — B (fastapi_backend.webhook_replay_freshness)   objective: Reject stale signed webhook replays: validate one signed timestamp against an acceptance window.
B.f1: A replay freshness check uses a delivery timestamp authenticated by the provider's signature; providers can refresh that timestamp and signature for each retry, so it establishes delivery-timestamp freshness, not the original event's age, and an unsigned timestamp cannot establish authenticated delivery freshness.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html#replay-attack-protection]
B.f2: After signature verification, parse the signed delivery timestamp and reject a delivery outside the configured acceptance window, including timestamps unacceptably far in the future under the provider's policy.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html#replay-attack-protection]
B.f3: Keep the receiver clock synchronized so comparing an authenticated timestamp with the local clock enforces the intended freshness window rather than a window distorted by clock drift.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html#replay-attack-protection]
B.f4: Test valid signatures for an in-window delivery timestamp, an expired delivery timestamp and an impermissibly future delivery timestamp, verifying that authenticity alone does not make every signed delivery fresh.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html#security-testing, owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html#replay-attack-protection]
note: Establish this first: An authenticated delivery timestamp bounds delivery freshness, not the original event age.
note: Stay within the current objective: Reject stale signed webhook replays. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine whether an authenticated event is too old.
PRACTICE ANCHOR (live_code): Implement a freshness function that parses one already-authenticated delivery timestamp and compares it with a supplied synchronized receiver time, acceptance window and provider-defined future tolerance.  SUCCESS: With valid signatures established beforehand, accept an in-window delivery and reject both an expired delivery and a delivery beyond the permitted future tolerance. Treat the result as delivery-timestamp freshness, not original event age.
ASSESSMENT ANCHOR: distinguish_authenticated_delivery_freshness_from_original_event_age facts=['f1']
ASSESSMENT ANCHOR: classify_signed_delivery_timestamp_against_acceptance_window facts=['f2']
ASSESSMENT ANCHOR: explain_receiver_clock_accuracy_requirement facts=['f3']
ASSESSMENT ANCHOR: verify_freshness_outcomes_for_validly_signed_deliveries facts=['f4']

## SOURCE FACTS — C (integration.bounded_idempotent_retries)   objective: Choose bounded safe retries: specify one operation's retry policy.
C.f1: Automatically repeating a non-idempotent request can duplicate effects; retry only when the method or application contract establishes idempotency or proves that the original request was not applied.   [sources: rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2]
C.f2: Retry-After can be an HTTP date or delay in seconds; incorporate a valid server-supplied delay into a retry policy rather than retrying immediately against that instruction.   [sources: rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-10.2.3]
C.f3: Configure a finite attempt count and finite total time budget, with a maintained client's bounded backoff where applicable, so repeated transient failures eventually stop.   [sources: redis_docs#https://redis.io/docs/latest/develop/clients/redis-py/produsage/#retries, python_tutorial#https://docs.python.org/3/library/asyncio-task.html#timeouts]
C.f4: Classify the supplied failure as retryable or terminal under the operation contract, recognizing that a timeout or lost response alone does not prove the remote operation had no effect.   [sources: fastapi_docs_advanced#https://www.python-httpx.org/exceptions/#the-exception-hierarchy, rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2]
C.f5: Verify a transient failure followed by success and repeated failures exhausting the configured limit, and confirm that a non-idempotent operation without a retry-safe contract is not blindly repeated.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/testing/#using-testclient, rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2]
note: Establish this first: Retries repeat effects; idempotency and limits govern them.
note: Stay within the current objective: Choose bounded safe retries. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Decide whether to retry and when to stop.
PRACTICE ANCHOR (live_code): Specify one outbound operation's retry policy in a supplied Python configuration mapping: identify its retry-safety basis, classify supplied failures, honor valid Retry-After values, and set finite attempt and total-time limits with bounded client backoff.  SUCCESS: The policy permits only contract-approved, retry-safe repetition; honors both forms of Retry-After without exceeding its total-time budget; and stops on terminal failures or exhausted limits. Supplied checks demonstrate transient failure followed by success, repeated-failure exhaustion, and no blind repetition of a non-idempotent operation without a retry-safe contract.
ASSESSMENT ANCHOR: decide_whether_repetition_is_safe facts=['f1', 'f4']
ASSESSMENT ANCHOR: classify_retryable_and_terminal_failures facts=['f4']
ASSESSMENT ANCHOR: determine_retry_timing_and_stopping_limits facts=['f2', 'f3']
ASSESSMENT ANCHOR: verify_retry_success_exhaustion_and_unsafe_repetition_prevention facts=['f5']

## DATA ASSETS USED
ds.delivery_timestamps: Authenticated delivery-timestamp cases — columns: case_id(identifier), signed_delivery_timestamp(datetime), receiver_now(datetime), acceptance_window(numerical), future_tolerance(numerical), signature_verified(categorical)
   ["fresh","1799999940",1800000000,300,30,true]
   ["past_boundary","1799999700",1800000000,300,30,true]
   ["expired","1799999699",1800000000,300,30,true]
   ["future_boundary","1800000030",1800000000,300,30,true]
   ["future_rejected","1800000031",1800000000,300,30,true]
   ["now","1800000000",1800000000,300,30,true]
ds.order_events: Authenticated publisher event fixtures — columns: publisher_event_id(identifier), order_id(identifier,digits-as-label), new_status(categorical)
   ["evt_a",101,"complete"]
   ["evt_b",202,"complete"]
   variant sequential_duplicate: 1 ops; planted: issue.repeated_delivery(duplicate_row)

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authentication and authorization tests including invalid-token rejection; Bounded retry decisions respecting HTTP idempotency; Declaring the deployed bearer-access-token and authorization-server security contract without a password grant; Inspecting generated OpenAPI for drift and sensitive exposure; Object-level authorization against the authenticated principal; Webhook replay freshness

## LESSON, in learner order

### s01 · explainer · Webhook delivery idempotency
Learn the rule — 
(definition) Deduplicate on an authenticated publisher event ID; persist its record across restarts for the required replay window. ⟦A.f1 A:tb2⟧
(definition) In one transaction, atomically record the event ID and durable state changes. A uniqueness constraint prevents concurrent deliveries from both applying the effect. ⟦A.f2 A:tb3⟧
(definition) Acknowledge an already processed event successfully without changing state again. Test duplicate and concurrent deliveries separately. ⟦A.f3 A:tb3⟧
[PROCESS_FLOW] nodes=['Delivery A: authenticated publisher event ID', 'Delivery B: same authenticated publisher event ID', 'Persistent uniqueness boundary (survives application restart)', 'One transaction: record ID atomically with durable order change', 'New ID → one committed effect', 'Already processed → successful duplicate acknowledgment, no repeated change'] edges=[('n0', 'n2', None), ('n1', 'n2', None), ('n2', 'n3', None), ('n3', 'n4', 'new'), ('n3', 'n5', 'duplicate')] alt: Delivery A: authenticated publisher event ID; Delivery B: same authenticated publisher event ID; Persistent uniqueness boundary (survives application restart); One transaction: record ID atomically with durable order change; New ID → one committed effect; Already processed → successful duplicate acknowledgment, no repeated change

### s02 · explainer · Keep the boundary clear
Work the boundary — 
(walkthrough) Successful duplicate acknowledgment is not a second state change. Persistence and atomic uniqueness must also hold across restart and concurrent delivery. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · check · Choose the boundary
Check — 

### s04 · hands_on · Apply the contract
Practice — 

### s05 · explainer · Webhook replay freshness
Learn the rule — 
(definition) Freshness needs a provider-signature-authenticated delivery timestamp. Providers can refresh it and its signature on retries: it measures delivery freshness, not original event age. Unsigned time proves no authenticated freshness. ⟦B.f1 B:tb2⟧
(definition) After signature verification, parse signed time and reject timestamps outside the configured window, including impermissibly future timestamps under provider policy. ⟦B.f2 B:tb3⟧
(definition) Synchronize the receiver clock so clock drift does not distort the intended freshness window. ⟦B.f3 B:tb3⟧
(definition) Test valid signatures with in-window, expired and impermissibly future timestamps: authentic does not necessarily mean fresh. ⟦B.f4 B:tb3⟧
[TABLE computed result ] caption: Supplied timestamp policy, including boundaries. Delivery freshness is not original event age; the receiver clock must be synchronized.
  produced by sql: SELECT case_id, signature_verified, signed_delivery_timestamp, receiver_now, CAST(signed_delivery_timestamp AS INTEGER)-receiver_now AS signed_time_difference, acceptance_window, future_tolerance, CASE WHEN signature_verified AND CAST(signed_delivery_timestamp AS INTEGER) BETWEEN receiver_now-acceptance_window AND receiver_now+future_tolerance THEN 'accept' ELSE 'reject' END AS delivery_freshness FROM deliveries

### s06 · explainer · Keep the boundary clear
Work the boundary — 
(walkthrough) A valid signature authenticates the timestamp, not its freshness. Retry timestamps also do not establish original event age. ⟦B.f1 B.f2 B.f4 B:tb4 B:tb5⟧

### s07 · check · Choose the boundary
Check — 

### s08 · check · Choose the boundary
Check — 

### s09 · hands_on · Apply the contract
Practice — 

### s10 · explainer · Bounded retry decisions respecting HTTP idempotency
Learn the rule — 
(definition) Repeating non-idempotent requests can duplicate effects. Retry only when method or application contract establishes idempotency, or proves the original was not applied. ⟦C.f1 C:tb2⟧
(definition) Retry-After may be an HTTP date or seconds of delay. Incorporate a valid supplied delay instead of immediately retrying against it. ⟦C.f2 C:tb3⟧
(definition) Bound attempts and total time; use a maintained client’s bounded backoff where applicable so transient failures eventually stop. ⟦C.f3 C:tb3⟧
(definition) Classify the supplied failure as retryable or terminal under the operation contract. A timeout or lost response alone does not prove no remote effect. ⟦C.f4 C:tb3⟧
(definition) Test transient failure then success and repeated failures reaching the limit. Do not blindly repeat a non-idempotent operation lacking a retry-safe contract. ⟦C.f5 C:tb3⟧
[PROCESS_FLOW] nodes=['Permission to repeat: idempotent contract or proof original was not applied?', 'No → stop; lost response may hide an already-applied effect', 'Yes → classify supplied failure under operation contract', 'Terminal → stop', 'Retryable → honor valid Retry-After (date or seconds) and bounded backoff', 'Remaining finite attempts AND total time?', 'Yes → retry; transient success ends repetition', 'No → stop at limit'] edges=[('n0', 'n1', None), ('n0', 'n2', None), ('n2', 'n3', 'terminal'), ('n2', 'n4', 'retryable'), ('n4', 'n5', None), ('n5', 'n6', None), ('n5', 'n7', None), ('n6', 'n2', 'another failure')] alt: Permission to repeat: idempotent contract or proof original was not applied?; No → stop; lost response may hide an already-applied effect; Yes → classify supplied failure under operation contract; Terminal → stop; Retryable → honor valid Retry-After (date or seconds) and bounded backoff; Remaining finite attempts AND total time?; Yes → retry; transient success ends repetition; No → stop at limit

### s11 · explainer · Keep the boundary clear
Work the boundary — 
(walkthrough) A lost response leaves the remote effect uncertain. A retry budget limits repetition but does not make unsafe repetition idempotent. ⟦C.f1 C.f3 C.f4 C:tb4 C:tb5⟧

### s12 · check · Choose the boundary
Check — 

### s13 · hands_on · Apply the contract
Practice — 

### s14 · recap · Take the rule with you
(takeaway) Successful duplicate acknowledgment is not a second state change. Persistence and atomic uniqueness must also hold across restart and concurrent delivery. ⟦A.f1 A.f2 A:tb5⟧
(takeaway) A valid signature authenticates the timestamp, not its freshness. Retry timestamps also do not establish original event age. ⟦B.f1 B.f2 B.f4 B:tb5⟧
(takeaway) A lost response leaves the remote effect uncertain. A retry budget limits repetition but does not make unsafe repetition idempotent. ⟦C.f1 C.f4 C:tb5⟧
[UP NEXT] Object-level authorization against the authenticated principal: An authenticated caller can substitute another order identifier in a request. Permission for the specific object must not be inferred from a valid identifier.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: Webhook delivery idempotency
(definition) Deduplicate on an authenticated publisher event ID; persist its record across restarts for the required replay window. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Acknowledge an already processed event successfully without changing state again. Test duplicate and concurrent deliveries separately. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) Successful duplicate acknowledgment is not a second state change. Persistence and atomic uniqueness must also hold across restart and concurrent delivery. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.order_events cols=['publisher_event_id', 'order_id', 'new_status'] ] caption: Authenticated publisher event fixtures
### r02 · Review: Webhook delivery idempotency
(definition) In one transaction, atomically record the event ID and durable state changes. A uniqueness constraint prevents concurrent deliveries from both applying the effect. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Acknowledge an already processed event successfully without changing state again. Test duplicate and concurrent deliveries separately. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) Successful duplicate acknowledgment is not a second state change. Persistence and atomic uniqueness must also hold across restart and concurrent delivery. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.order_events cols=['publisher_event_id', 'order_id', 'new_status'] ] caption: Authenticated publisher event fixtures
### r03 · Review: Webhook replay freshness
(definition) Synchronize the receiver clock so clock drift does not distort the intended freshness window. ⟦B.f3 B:tb3 B:tb4⟧
(misconception) A valid signature authenticates the timestamp, not its freshness. Retry timestamps also do not establish original event age. ⟦B.f3 B:tb3 B:tb4⟧
[TABLE ds.delivery_timestamps cols=['case_id', 'signed_delivery_timestamp', 'receiver_now', 'acceptance_window', 'future_tolerance', 'signature_verified'] ] caption: Authenticated delivery-timestamp cases
### r04 · Review: Webhook replay freshness
(definition) Test valid signatures with in-window, expired and impermissibly future timestamps: authentic does not necessarily mean fresh. ⟦B.f4 B:tb3 B:tb4 B:tb5⟧
(misconception) A valid signature authenticates the timestamp, not its freshness. Retry timestamps also do not establish original event age. ⟦B.f4 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.delivery_timestamps cols=['case_id', 'signed_delivery_timestamp', 'receiver_now', 'acceptance_window', 'future_tolerance', 'signature_verified'] ] caption: Authenticated delivery-timestamp cases
### r05 · Review: Webhook replay freshness
(definition) Freshness needs a provider-signature-authenticated delivery timestamp. Providers can refresh it and its signature on retries: it measures delivery freshness, not original event age. Unsigned time proves no authenticated freshness. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(definition) After signature verification, parse signed time and reject timestamps outside the configured window, including impermissibly future timestamps under provider policy. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(misconception) A valid signature authenticates the timestamp, not its freshness. Retry timestamps also do not establish original event age. ⟦B.f1 B.f2 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.delivery_timestamps cols=['case_id', 'signed_delivery_timestamp', 'receiver_now', 'acceptance_window', 'future_tolerance', 'signature_verified'] ] caption: Authenticated delivery-timestamp cases
### r06 · Review: Bounded retry decisions respecting HTTP idempotency
(definition) Test transient failure then success and repeated failures reaching the limit. Do not blindly repeat a non-idempotent operation lacking a retry-safe contract. ⟦C.f5 C:tb3 C:tb4⟧
(misconception) The supplied policy bounds attempts at 3 and total time at 10 seconds. The fixture contrasts GET with POST lacking a retry-safe contract. ⟦C.f5 C:tb3 C:tb4⟧
### r07 · Review: Bounded retry decisions respecting HTTP idempotency
(definition) Repeating non-idempotent requests can duplicate effects. Retry only when method or application contract establishes idempotency, or proves the original was not applied. ⟦C.f1 C:tb2 C:tb4 C:tb5⟧
(definition) Retry-After may be an HTTP date or seconds of delay. Incorporate a valid supplied delay instead of immediately retrying against it. ⟦C.f2 C:tb3 C:tb4⟧
(definition) Bound attempts and total time; use a maintained client’s bounded backoff where applicable so transient failures eventually stop. ⟦C.f3 C:tb3 C:tb4⟧
(definition) Classify the supplied failure as retryable or terminal under the operation contract. A timeout or lost response alone does not prove no remote effect. ⟦C.f4 C:tb3 C:tb4 C:tb5⟧
(definition) Test transient failure then success and repeated failures reaching the limit. Do not blindly repeat a non-idempotent operation lacking a retry-safe contract. ⟦C.f5 C:tb3 C:tb4⟧
(misconception) The supplied policy bounds attempts at 3 and total time at 10 seconds. The fixture contrasts GET with POST lacking a retry-safe contract. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C:tb2 C:tb3 C:tb4 C:tb5⟧

=========

# EVALUATOR PACKET — Object-level authorization against the authenticated principal (tile_096)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = auth.object_authorization — Object-level authorization against the authenticated principal

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (auth.object_authorization)   objective: Enforce object ownership: protect one item endpoint.
A.f1: An endpoint taking an object identifier must check the caller's permission for that specific object; a valid identifier and authenticated caller do not establish ownership.   [sources: owasp_api_security_top10_2023#https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/#how-to-prevent]
A.f2: Enforce the object boundary by selecting with both object identity and the authorized owner or tenant context, rather than trusting an owner identifier from caller-controlled input.   [sources: owasp_api_security_top10_2023#https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/#how-to-prevent, sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#the-where-clause]
A.f3: Create distinct authorized contexts and verify that each can access its permitted object but cannot obtain or change the other context's object by substituting its identifier.   [sources: owasp_api_security_top10_2023#https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/#how-to-prevent, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/testing/#using-testclient]
note: Establish this first: Authorization binds caller to specific object.
note: Stay within the current objective: Enforce object ownership. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Detect another user's object access.
PRACTICE ANCHOR (live_code): Protect one order retrieval endpoint by selecting the requested order using both its identifier and the owner identity supplied by the authenticated principal dependency.  SUCCESS: Each of two synthetic authorized contexts can retrieve its own order. Substituting the other context's order identifier returns no order data, and caller-controlled owner input cannot override the trusted owner identity.
ASSESSMENT ANCHOR: detect_cross_owner_object_access facts=['f1']
ASSESSMENT ANCHOR: identify_trusted_context_object_filtering facts=['f2']
ASSESSMENT ANCHOR: verify_object_access_isolation facts=['f3']

## DATA ASSETS USED
ds.orders: Order fixtures — columns: id(identifier,digits-as-label), owner_id(identifier), status(categorical)
   [101,"caller_a","pending"]
   [202,"caller_b","pending"]
   [303,"caller_a","complete"]
ds.principals: Trusted principal contexts — columns: owner_id(identifier), scopes(categorical)
   ["caller_a","orders:read"]
   ["caller_b","orders:read"]
   ["caller_a",""]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authentication and authorization tests including invalid-token rejection; Declaring the deployed bearer-access-token and authorization-server security contract without a password grant; Inspecting generated OpenAPI for drift and sensitive exposure

## LESSON, in learner order

### s01 · explainer · Object-level authorization against the authenticated principal
Learn the rule — 
(definition) Check permission for the specific requested object. A valid identifier plus an authenticated caller does not establish ownership. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Select by object identity and authorized owner or tenant context together. Do not trust a caller-supplied owner identifier. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Test distinct authorized contexts: each accesses its permitted object, but substituting the other context’s ID must neither obtain nor change that object. ⟦A.f3 A:tb3 A:tb4⟧
[TABLE computed result ] caption: Four trusted-context retrieval combinations. The endpoint must also deny cross-context changes; never take ownership from caller input.
  produced by sql: SELECT p.owner_id AS trusted_caller, o.id AS requested_order_id, CASE WHEN p.owner_id=o.owner_id THEN 'permitted public result' ELSE 'denied; no order data' END AS access_outcome FROM (SELECT DISTINCT owner_id FROM principals WHERE owner_id IN ('caller_a','caller_b')) p CROSS JOIN orders o WHERE o.id IN (101,202) ORDER BY p.owner_id,o.id

### s02 · check · Choose the boundary
Check — 

### s03 · check · Choose the boundary
Check — 

### s04 · hands_on · Apply the contract
Practice — 

### s05 · recap · Take the rule with you
(takeaway) Authentication and a real object ID are not enough. Selection must include the trusted context; substituting another owner’s ID must deny access. ⟦A.f1 A.f2 A:tb5⟧
[UP NEXT] Declaring the deployed bearer-access-token and authorization-server security contract without a password grant: Public security documentation should describe how the deployed API actually accepts authority, not advertise an undeployed way to acquire tokens.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: Object-level authorization against the authenticated principal
(definition) Check permission for the specific requested object. A valid identifier plus an authenticated caller does not establish ownership. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(misconception) Authentication and a real object ID are not enough. Selection must include the trusted context; substituting another owner’s ID must deny access. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
[TABLE ds.orders cols=['id', 'owner_id', 'status'] ] caption: Order fixtures
### r02 · Review: Object-level authorization against the authenticated principal
(definition) Test distinct authorized contexts: each accesses its permitted object, but substituting the other context’s ID must neither obtain nor change that object. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) Authentication and a real object ID are not enough. Selection must include the trusted context; substituting another owner’s ID must deny access. ⟦A.f3 A:tb3 A:tb4⟧
[TABLE ds.orders cols=['id', 'owner_id', 'status'] ] caption: Order fixtures
### r03 · Review: Object-level authorization against the authenticated principal
(definition) Select by object identity and authorized owner or tenant context together. Do not trust a caller-supplied owner identifier. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) Authentication and a real object ID are not enough. Selection must include the trusted context; substituting another owner’s ID must deny access. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.orders cols=['id', 'owner_id', 'status'] ] caption: Order fixtures

=========

# EVALUATOR PACKET — Declaring the deployed bearer-access-token and authorization-server security contract without a password grant / Inspecting generated OpenAPI for drift and sensitive exposure / Authentication and authorization tests including invalid-token rejection (tile_097)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.production_security_documentation — Declaring the deployed bearer-access-token and authorization-server security contract without a password grant
B = fastapi.openapi_contract_inspection — Inspecting generated OpenAPI for drift and sensitive exposure
C = testing.api_authentication_authorization — Authentication and authorization tests including invalid-token rejection

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (fastapi.production_security_documentation)   objective: Document the deployed API authentication contract: document one deployed bearer scheme and established authorization-server flow without a password grant.
A.f1: Declare HTTPBearer for a deployed bearer-token scheme so the generated OpenAPI securitySchemes entry describes token presentation rather than implying that the API issues passwords or tokens.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/reference/security/#fastapi.security.HTTPBearer]
A.f2: For an established authorization-code issuer contract, configure OAuth2AuthorizationCodeBearer(authorizationUrl=..., tokenUrl=..., scopes=...) with the actual supplied issuer endpoints and permission descriptions.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/reference/security/#fastapi.security.OAuth2AuthorizationCodeBearer]
A.f3: Describe the deployed authorization-code and PKCE acquisition contract where applicable, and do not present an OAuth2 password flow as production access guidance.   [sources: ietf_rfc9700#https://www.rfc-editor.org/rfc/rfc9700.txt#2.1.1, ietf_rfc9700#https://www.rfc-editor.org/rfc/rfc9700.txt#2.4]
A.f4: Attach the scheme and required scopes through the real operation dependencies so generated operation security requirements agree with the authority the endpoint accepts.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/reference/security/#fastapi.security.HTTPBearer, fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/#oauth2-scopes-and-openapi]
A.f5: Inspect components.securitySchemes and each protected operation's security entry, checking issuer URLs, bearer presentation and required permissions against the deployed contract.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/first-steps/#check-the-openapi-json]
note: Establish this first: OpenAPI security declares how clients obtain and present the authority the deployed service actually accepts..
note: Stay within the current objective: Document the deployed API authentication contract. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Detect security documentation that misrepresents the deployed bearer or authorization-code flow.
PRACTICE ANCHOR (live_code): Document the supplied deployed bearer scheme and established authorization-code issuer contract using HTTPBearer and OAuth2AuthorizationCodeBearer. Preserve the existing verification and permission dependencies, connect the appropriate scheme and required scopes, and describe PKCE where applicable without offering a password grant.  SUCCESS: The generated security schemes describe bearer presentation and the supplied authorization-code endpoints and permissions accurately. Protected operation security entries match their existing dependencies and required scopes, and the acquisition description agrees with the supplied PKCE contract without advertising a password flow.
ASSESSMENT ANCHOR: distinguish_bearer_presentation_from_token_issuance facts=['f1']
ASSESSMENT ANCHOR: detect_misrepresented_authorization_server_acquisition_contract facts=['f2', 'f3']
ASSESSMENT ANCHOR: check_security_declarations_against_deployed_operation_authority facts=['f4', 'f5']

## SOURCE FACTS — B (fastapi.openapi_contract_inspection)   objective: Review generated documentation: audit one router's schema.
B.f1: Retrieve /openapi.json and inspect the router's paths, parameters, request schemas, response schemas and security requirements as public contract artifacts.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/first-steps/#check-the-openapi-json]
B.f2: Compare generated requiredness, types, constraints and output fields with executable input and output behavior to identify drift between documentation and the accepted or emitted contract.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/body/#results, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/response-model/#response-model-parameter]
B.f3: Compare documented success and expected-error statuses with exercised HTTP outcomes, because an additional response declaration does not prove the handler actually emits that outcome.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/additional-responses/#additional-response-with-model, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/testing/#using-testclient]
B.f4: Audit public examples and descriptions for secrets and sensitive personal data, and ensure examples validate against the model rather than publishing realistic private values.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/schema-extra-example/#extra-json-schema-data-in-pydantic-models, owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#data-to-exclude]
B.f5: Check that public security schemes and operation requirements describe the configured bearer and established issuer contract and do not introduce an undeployed password grant.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/reference/security/#fastapi.security.OAuth2AuthorizationCodeBearer, ietf_rfc9700#https://www.rfc-editor.org/rfc/rfc9700.txt#2.4]
note: Establish this first: Generated docs are public artifacts requiring review.
note: Stay within the current objective: Review generated documentation. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify drift and sensitive examples.
PRACTICE ANCHOR (live_code): Retrieve /openapi.json and audit one existing router's generated contract against its models, supplied non-authentication HTTP outcomes and established security configuration. Record drift and unsafe public examples without adding authentication or authorization tests.  SUCCESS: The audit covers paths, parameters, request and response schemas, requiredness, types, constraints, output fields, documented statuses, examples, descriptions and security requirements. Findings distinguish declarations from observed behavior, identify sensitive or invalid examples, and flag security declarations that differ from the deployed contract.
ASSESSMENT ANCHOR: identify_schema_and_behavior_drift facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_documented_statuses_from_exercised_outcomes facts=['f3']
ASSESSMENT ANCHOR: identify_sensitive_or_model_invalid_public_examples facts=['f4']
ASSESSMENT ANCHOR: identify_mismatched_public_security_declarations facts=['f5']

## SOURCE FACTS — C (testing.api_authentication_authorization)   objective: Verify API authentication and authorization rejection: test one protected resource with invalid, insufficient and valid credentials.
C.f1: Send requests through the real protected HTTP endpoint with absent, malformed and supplied bearer credentials, keeping the authentication and verification gates active.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/testing/#using-testclient, fastapi_docs_advanced#https://fastapi.tiangolo.com/reference/security/#fastapi.security.HTTPBearer]
C.f2: Test invalid-signature, expired and contextually wrong tokens separately from a valid token, asserting credential rejection before protected output is returned.   [sources: fastapi_docs_tutorial#https://pyjwt.readthedocs.io/en/latest/usage.html#registered-claim-names, fastapi_docs_tutorial#https://pyjwt.readthedocs.io/en/latest/api.html#jwt.decode]
C.f3: Test an otherwise valid credential lacking the required permission separately from a valid sufficiently permitted credential to distinguish authentication from operation authorization.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/#verify-the-scopes]
C.f4: Test a valid caller against another caller's object identifier as a separate deny path from missing operation permission.   [sources: owasp_api_security_top10_2023#https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/#how-to-prevent]
C.f5: Assert the declared status and safe body for each denial and the public projected result for the fully authorized request, not merely that some requests fail and one succeeds.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/testing/#using-testclient, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/response-model/#response-model-parameter]
note: Establish this first: Security tests prove deny paths as well as successful authenticated requests.
note: Stay within the current objective: Verify API authentication and authorization rejection. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Separate invalid-token rejection from missing permission and cross-object rejection.
PRACTICE ANCHOR (live_code): Test one protected order endpoint through real HTTP requests with absent, malformed, invalid-signature, expired, wrong-context, insufficient-permission and fully authorized credentials. Include a separately tested request for another caller's order.  SUCCESS: Each credential rejection, missing-permission denial and cross-object denial has its own test asserting the declared status and safe body without protected output. The fully authorized request returns the expected public projection, with authentication and verification active throughout.
ASSESSMENT ANCHOR: distinguish_credential_rejection_from_authorization_denial facts=['f1', 'f2']
ASSESSMENT ANCHOR: separate_operation_permission_denial_from_cross_object_denial facts=['f3', 'f4']
ASSESSMENT ANCHOR: verify_denial_contracts_and_authorized_public_output facts=['f5']

## DATA ASSETS USED
ds.authentication_test_matrix: Order endpoint security test matrix — columns: credential_condition(categorical), trusted_owner_id(identifier), operation_permission(categorical), requested_order_id(identifier,digits-as-label), rejection_gate_or_result(categorical), declared_status(categorical,digits-as-label), safe_body_or_public_result(text)
   ["absent","caller_a",false,101,"authentication",401,"{\"detail\": \"Not authenticated\"}"]
   ["malformed","caller_a",false,101,"authentication",401,"{\"detail\": \"Not authenticated\"}"]
   ["invalid_signature","caller_a",true,101,"authentication",401,"{\"detail\": \"Not authenticated\"}"]
   ["expired","caller_a",true,101,"authentication",401,"{\"detail\": \"Not authenticated\"}"]
   ["wrong_issuer","caller_a",true,101,"authentication",401,"{\"detail\": \"Not authenticated\"}"]
   ["wrong_audience","caller_a",true,101,"authentication",401,"{\"detail\": \"Not authenticated\"}"]
   ["valid_without_permission","caller_a",false,101,"operation_authorization",403,"{\"detail\": \"Forbidden\"}"]
   ["valid_other_owner","caller_a",true,202,"object_authorization",403,"{\"detail\": \"Forbidden\"}"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authentication and authorization tests including invalid-token rejection; Inspecting generated OpenAPI for drift and sensitive exposure

## LESSON, in learner order

### s01 · explainer · Declaring the deployed bearer-access-token and authorization-server security contract without a password grant
Learn the rule — 
(definition) Use HTTPBearer to document deployed bearer-token presentation in securitySchemes, not to imply this API issues passwords or tokens. ⟦A.f1 A:tb2⟧
(definition) For an established code issuer, configure OAuth2AuthorizationCodeBearer(authorizationUrl=..., tokenUrl=..., scopes=...) with supplied endpoints and permission descriptions. ⟦A.f2 A:tb3⟧
(definition) Describe deployed authorization-code acquisition and PKCE where applicable. Do not guide production access through an OAuth2 password flow. ⟦A.f3 A:tb3⟧
(definition) Attach schemes and required scopes through real operation dependencies so generated security requirements match accepted authority. ⟦A.f4 A:tb3⟧
(definition) Inspect components.securitySchemes and protected operations’ security entries against the deployed issuer URLs, bearer presentation and required permissions. ⟦A.f5 A:tb3⟧
[SIDE_BY_SIDE] Compare issuer URLs and required permissions; document code/PKCE acquisition without an undeployed password flow. left_label: Supplied deployed contract | right_label: Declarations and enforcement dependencies
  left:
[DIAGRAM: Deployed training contract] nodes=['Supplied bearer presentation: {"OrderBearer": {"type": "http", "scheme": "bearer"}}', 'Established acquisition: {"OrderAuthorizationCode": {"type": "oauth2", "flows": {"authorizationCode": {"authorizationUrl": "http://127.0.0.1:37353/authorize", "tokenUrl": "http://127.0.0.1:37353/token", "scopes": {"orders:read": "Read orders", "orders:write": "Create orders"}}}}}', 'Operation dependencies: {"GET /orders/{order_id}": {"dependency": "read_orders", "scope": "orders:read"}, "POST /orders": {"dependency": "write_orders", "scope": "orders:write"}}', 'Bearer presentation and issuer acquisition describe the same access-token authority, not separate independently accepted credentials.'] edges=[] alt: Supplied bearer presentation: {"OrderBearer": {"type": "http", "scheme": "bearer"}}; Established acquisition: {"OrderAuthorizationCode": {"type": "oauth2", "flows": {"authorizationCode": {"authorizationUrl": "http://127.0.0.1:37353/authorize", "tokenUrl": "http://127.0.0.1:37353/token", "scopes": {"orders:read": "Read orders", "orders:write": "Create orders"}}}}}; Operation dependencies: {"GET /orders/{order_id}": {"dependency": "read_orders", "scope": "orders:read"}, "POST /orders": {"dependency": "write_orders", "scope": "orders:write"}}; Bearer presentation and issuer acquisition describe the same access-token authority, not separate independently accepted credentials.
  right:
[CODE python]
from fastapi import Depends, Security
from fastapi.security import HTTPBearer, OAuth2AuthorizationCodeBearer
bearer_scheme = HTTPBearer(auto_error=False, scheme_name='OrderBearer')
def authorization_code_scheme(issuer_configuration):
    return OAuth2AuthorizationCodeBearer(authorizationUrl=issuer_configuration['authorization_url'], tokenUrl=issuer_configuration['token_url'], scopes=issuer_configuration['scopes'], scheme_name='OrderAuthorizationCode')
# TODO: add scheme/scopes to each operation while keeping read_orders and
# write_orders enforcement dependencies unchanged. See fixtures.json.

import json
from pathlib import Path
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from existing_verifier import ExistingVerifier
configuration=json.loads(Path('issuer_configuration.json').read_text())
existing_verifier=ExistingVerifier();existing_verifier.configure(configuration)
extraction=HTTPBearer(auto_error=False)
async def authenticated(request:Request):
    credential=await extraction(request)
    if credential is None:raise HTTPException(401,'Bearer token required')
    return existing_verifier.verify(credential.credentials)
def enforce_permission(principal,required):
    if required not in principal.get('scope','').split():raise HTTPException(403,'Permission required')
    return principal
from fastapi import Depends
def read_orders(principal=Depends(authenticated)):
    return enforce_permission(principal,'orders:read')
def write_orders(principal=Depends(authenticated)):
    return enforce_permission(principal,'orders:write')

# Inspect app.openapi()["components"]["securitySchemes"] and operation security entries.
  annotations: []
[COMPARISON] cols=['Supplied contract', 'Generated operation comparison']
  - Bearer presentation: {"target":"OrderBearer: type http, scheme bearer.","inspect":"Compare the generated operation security entries after wiring the real dependencies; these are target declarations, not captured output."}
  - Issuer acquisition: {"target":"OrderAuthorizationCode: authorizationCode flow; authorizationUrl http://127.0.0.1:37353/authorize; tokenUrl http://127.0.0.1:37353/token; scopes orders:read—Read orders and orders:write—Create orders.","inspect":"Compare the generated operation security entries after wiring the real dependencies; these are target declarations, not captured output."}
  - Operation permissions: {"target":"Protected GET requires orders:read; protected POST requires orders:write.","inspect":"Compare the generated operation security entries after wiring the real dependencies; these are target declarations, not captured output."}

### s02 · explainer · Keep the boundary clear
Work the boundary — 
(walkthrough) Bearer presentation and issuer acquisition describe the same deployed authority. Documentation must not invent a password grant or replace enforcement. ⟦A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Choose the boundary
Check — 

### s04 · check · Choose the boundary
Check — 

### s05 · hands_on · Apply the contract
Practice — 

### s06 · explainer · Inspecting generated OpenAPI for drift and sensitive exposure
Learn the rule — 
(definition) Retrieve /openapi.json. Review router paths, parameters, request/response schemas and security requirements as public artifacts. ⟦B.f1 B:tb2⟧
(definition) Compare requiredness, types, constraints and output fields with executable input/output behavior to find contract drift. ⟦B.f2 B:tb3⟧
(definition) Compare success and expected-error statuses with exercised HTTP outcomes: declaring an additional response does not implement it. ⟦B.f3 B:tb3⟧
(definition) Audit examples and descriptions for secrets and sensitive personal data. Validate examples against models rather than publishing realistic private values. ⟦B.f4 B:tb3⟧
(definition) Check public security schemes and operation requirements against configured bearer presentation and established issuer contract; introduce no undeployed password grant. ⟦B.f5 B:tb3⟧
[SIDE_BY_SIDE] Mark drift only after comparison; audit public examples for sensitive exposure. Additional response declarations do not prove HTTP outcomes. left_label: Application source — not generated declarations | right_label: Executable models and security configuration
  left:
[CODE python]
import json
from pathlib import Path
from fastapi import FastAPI,APIRouter,HTTPException,Depends
from fastapi.security import HTTPBearer
from dependencies import read_orders, write_orders
from models import OrderInput,PublicOrder,ErrorBody
router=APIRouter(prefix='/orders',tags=['orders'])
# Established training issuer; verification and permissions are active.
# Bearer metadata is present; the unfinished audit compares issuer declarations.
bearer=HTTPBearer(auto_error=False,scheme_name='OrderBearer')
fixtures=json.loads(Path('fixtures.json').read_text())
orders={row['id']:dict(row) for row in fixtures['initial_orders']}
@router.post('',response_model=PublicOrder,status_code=201,
             responses={409:{'model':ErrorBody,'description':'Duplicate order'}})
def create_order(value:OrderInput,credential=Depends(bearer),principal=Depends(write_orders)):
    if value.id in orders:
        # Deliberate documentation drift: actual conflict is 400, not declared 409.
        raise HTTPException(400,'Duplicate order')
    row={**value.model_dump(),'owner_id':fixtures['initial_orders'][0]['owner_id']}
    orders[value.id]=row
    return row
@router.get('/{order_id}',response_model=PublicOrder,
            responses={404:{'model':ErrorBody,'description':'Order unavailable'}})
def retrieve_order(order_id:int,credential=Depends(bearer),principal=Depends(read_orders)):
    if order_id not in orders: raise HTTPException(404,'Not found')
    return orders[order_id]
app=FastAPI()
app.include_router(router)

# Retrieve /openapi.json and compare with source models, HTTP evidence and deployed security configuration.

  annotations: ['The supplied source marks conflict-status drift here. Compare this emitted status with the additional response declaration and exercised HTTP evidence.']
  right:
[CODE python]
from pydantic import BaseModel,Field,ConfigDict
from typing import Literal
class OrderInput(BaseModel):
    id:int=Field(gt=0)
    status:Literal['pending','complete']='pending'
class PublicOrder(BaseModel):
    id:int
    status:Literal['pending','complete']
    model_config=ConfigDict(json_schema_extra={'examples':[{'id':101,'status':'pending'}]})
class ErrorBody(BaseModel):
    detail:str

import json
from pathlib import Path
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from existing_verifier import ExistingVerifier
configuration=json.loads(Path('issuer_configuration.json').read_text())
existing_verifier=ExistingVerifier();existing_verifier.configure(configuration)
extraction=HTTPBearer(auto_error=False)
async def authenticated(request:Request):
    credential=await extraction(request)
    if credential is None:raise HTTPException(401,'Bearer token required')
    return existing_verifier.verify(credential.credentials)
def enforce_permission(principal,required):
    if required not in principal.get('scope','').split():raise HTTPException(403,'Permission required')
    return principal
from fastapi import Depends
def read_orders(principal=Depends(authenticated)):
    return enforce_permission(principal,'orders:read')
def write_orders(principal=Depends(authenticated)):
    return enforce_permission(principal,'orders:write')

# Compare against bundled exercised HTTP evidence; validate synthetic examples.
  annotations: []
[COMPARISON] cols=['Generated public contract', 'Captured execution / supplied issuer comparison']
  - POST /orders: {"generated":"Generated POST /orders: 201 → PublicOrder; 409 → ErrorBody.","captured":"Captured create: 201 {\"id\":202,\"status\":\"pending\"}. Captured duplicate: 400 {\"detail\":\"Duplicate order\"}—status drift from documented 409."}
  - GET /orders/{order_id}: {"generated":"Generated GET /orders/{order_id}: required integer order_id; 200 → PublicOrder; 404 → ErrorBody.","captured":"Captured own listing: 200 {\"id\":101,\"status\":\"pending\"}; missing order: 404 {\"detail\":\"Not found\"}."}
  - Input and public output: {"generated":"OrderInput requires id > 0; status is optional with default pending. PublicOrder requires id and status and excludes owner_id.","captured":"Captured create: 201 {\"id\":202,\"status\":\"pending\"}."}
  - Security: {"generated":"Generated security exposes OrderBearer only; authorization-code metadata and operation scope requirements need comparison with the deployed issuer contract.","captured":"Compare with the registered security_configuration.json deployed issuer contract."}

### s07 · explainer · Keep the boundary clear
Work the boundary — 
(walkthrough) Generated documentation is public evidence to audit, not proof of runtime behavior. Check drift, sensitive examples and deployed security together. ⟦B.f2 B.f4 B.f5 B:tb4 B:tb5⟧

### s08 · check · Choose the boundary
Check — 

### s09 · hands_on · Apply the contract
Practice — 

### s10 · explainer · Authentication and authorization tests including invalid-token rejection
Learn the rule — 
(definition) Exercise the real protected HTTP endpoint with absent, malformed and supplied bearer credentials; keep authentication and verification active. ⟦C.f1 C:tb2⟧
(definition) Separate invalid-signature, expired and wrong-context tokens from a valid token. Assert credential rejection before protected output. ⟦C.f2 C:tb3⟧
(definition) Compare a valid credential missing permission with a sufficiently permitted one to distinguish authentication from operation authorization. ⟦C.f3 C:tb3⟧
(definition) Separately test a valid caller substituting another caller’s object ID; this is not the missing-operation-permission path. ⟦C.f4 C:tb3⟧
(definition) Assert declared status and safe body for each denial, and the public projected result for full authorization—not just failure versus success. ⟦C.f5 C:tb3⟧
[TABLE ds.authentication_test_matrix cols=['credential_condition', 'trusted_owner_id', 'operation_permission', 'requested_order_id', 'rejection_gate_or_result', 'declared_status', 'safe_body_or_public_result'] ] caption: Supplied local endpoint contracts, not universal status defaults. Separate authentication, operation permission, object access and public-result assertions.

### s11 · explainer · Keep the boundary clear
Work the boundary — 
(walkthrough) One rejection plus one success leaves gates unproven. Separate credential rejection, missing permission and cross-object denial, then assert complete contracts. ⟦C.f2 C.f3 C.f4 C.f5 C:tb4 C:tb5⟧

### s12 · check · Choose the boundary
Check — 

### s13 · hands_on · Apply the contract
Practice — 

### s14 · recap · Take the rule with you
(takeaway) Bearer presentation and issuer acquisition describe the same deployed authority. Documentation must not invent a password grant or replace enforcement. ⟦A.f1 A.f3 A.f4 A.f5 A:tb5⟧
(takeaway) Generated documentation is public evidence to audit, not proof of runtime behavior. Check drift, sensitive examples and deployed security together. ⟦B.f3 B.f4 B:tb5⟧
(takeaway) One rejection plus one success leaves gates unproven. Separate credential rejection, missing permission and cross-object denial, then assert complete contracts. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C:tb5⟧

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: Declaring the deployed bearer-access-token and authorization-server security contract without a password grant
(definition) Use HTTPBearer to document deployed bearer-token presentation in securitySchemes, not to imply this API issues passwords or tokens. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(misconception) The supplied operation permissions are orders:read, orders:write. Match their real dependencies to generated security entries, without adding a password grant. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
### r02 · Review: Declaring the deployed bearer-access-token and authorization-server security contract without a password grant
(definition) Attach schemes and required scopes through real operation dependencies so generated security requirements match accepted authority. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(definition) Inspect components.securitySchemes and protected operations’ security entries against the deployed issuer URLs, bearer presentation and required permissions. ⟦A.f5 A:tb3 A:tb4 A:tb5⟧
(misconception) The supplied operation permissions are orders:read, orders:write. Match their real dependencies to generated security entries, without adding a password grant. ⟦A.f4 A.f5 A:tb3 A:tb4 A:tb5⟧
### r03 · Review: Declaring the deployed bearer-access-token and authorization-server security contract without a password grant
(definition) For an established code issuer, configure OAuth2AuthorizationCodeBearer(authorizationUrl=..., tokenUrl=..., scopes=...) with supplied endpoints and permission descriptions. ⟦A.f2 A:tb3 A:tb4⟧
(definition) Describe deployed authorization-code acquisition and PKCE where applicable. Do not guide production access through an OAuth2 password flow. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) The supplied operation permissions are orders:read, orders:write. Match their real dependencies to generated security entries, without adding a password grant. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
### r04 · Review: Inspecting generated OpenAPI for drift and sensitive exposure
(definition) Check public security schemes and operation requirements against configured bearer presentation and established issuer contract; introduce no undeployed password grant. ⟦B.f5 B:tb3 B:tb4⟧
(misconception) Audit the supplied orders router. Its synthetic example is {"id": 101, "status": "pending"}; validate public examples against models and compare declarations with exercised HTTP behavior. ⟦B.f5 B:tb3 B:tb4⟧
### r05 · Review: Inspecting generated OpenAPI for drift and sensitive exposure
(definition) Retrieve /openapi.json. Review router paths, parameters, request/response schemas and security requirements as public artifacts. ⟦B.f1 B:tb2 B:tb4⟧
(definition) Compare requiredness, types, constraints and output fields with executable input/output behavior to find contract drift. ⟦B.f2 B:tb3 B:tb4⟧
(definition) Compare success and expected-error statuses with exercised HTTP outcomes: declaring an additional response does not implement it. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(definition) Audit examples and descriptions for secrets and sensitive personal data. Validate examples against models rather than publishing realistic private values. ⟦B.f4 B:tb3 B:tb4 B:tb5⟧
(definition) Check public security schemes and operation requirements against configured bearer presentation and established issuer contract; introduce no undeployed password grant. ⟦B.f5 B:tb3 B:tb4⟧
(misconception) Audit the supplied orders router. Its synthetic example is {"id": 101, "status": "pending"}; validate public examples against models and compare declarations with exercised HTTP behavior. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r06 · Review: Authentication and authorization tests including invalid-token rejection
(definition) Assert declared status and safe body for each denial, and the public projected result for full authorization—not just failure versus success. ⟦C.f5 C:tb3 C:tb4 C:tb5⟧
(misconception) One rejection plus one success leaves gates unproven. Separate credential rejection, missing permission and cross-object denial, then assert complete contracts. ⟦C.f5 C:tb3 C:tb4 C:tb5⟧
[TABLE ds.authentication_test_matrix cols=['credential_condition', 'trusted_owner_id', 'operation_permission', 'requested_order_id', 'rejection_gate_or_result', 'declared_status', 'safe_body_or_public_result'] ] caption: Order endpoint security test matrix
### r07 · Review: Authentication and authorization tests including invalid-token rejection
(definition) Exercise the real protected HTTP endpoint with absent, malformed and supplied bearer credentials; keep authentication and verification active. ⟦C.f1 C:tb2 C:tb4 C:tb5⟧
(definition) Separate invalid-signature, expired and wrong-context tokens from a valid token. Assert credential rejection before protected output. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
(definition) Compare a valid credential missing permission with a sufficiently permitted one to distinguish authentication from operation authorization. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
(definition) Separately test a valid caller substituting another caller’s object ID; this is not the missing-operation-permission path. ⟦C.f4 C:tb3 C:tb4 C:tb5⟧
(definition) Assert declared status and safe body for each denial, and the public projected result for full authorization—not just failure versus success. ⟦C.f5 C:tb3 C:tb4 C:tb5⟧
(misconception) One rejection plus one success leaves gates unproven. Separate credential rejection, missing permission and cross-object denial, then assert complete contracts. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C:tb2 C:tb3 C:tb4 C:tb5⟧
[TABLE ds.authentication_test_matrix cols=['credential_condition', 'trusted_owner_id', 'operation_permission', 'requested_order_id', 'rejection_gate_or_result', 'declared_status', 'safe_body_or_public_result'] ] caption: Order endpoint security test matrix

## OTHER CONTENT (fields without a dedicated renderer)
· blocks.title: Target declarations — not captured output
· blocks.title: Registered generated_schema.json versus captured http_evidence.json
· cells.captured: Captured create: 201 {"id":202,"status":"pending"}. Captured duplicate: 400 {"detail":"Duplicate order"}—status drift from documented 409.
· cells.captured: Captured own listing: 200 {"id":101,"status":"pending"}; missing order: 404 {"detail":"Not found"}.
· cells.captured: Captured create: 201 {"id":202,"status":"pending"}.