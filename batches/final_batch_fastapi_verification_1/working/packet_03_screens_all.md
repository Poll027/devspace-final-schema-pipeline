# EVALUATOR PACKET — Binding request bodies to typed models (tile_039)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.request_body_binding — Binding request bodies to typed models

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (fastapi.request_body_binding)   objective: Declare JSON bodies: add one typed create body.
A.f1: Define a BaseModel subclass and annotate a handler parameter with that model to bind a structured JSON request body.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/body/#create-your-data-model, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/body/#declare-it-as-a-parameter]
A.f2: FastAPI reads the JSON body, converts compatible values, validates the declared model and passes the model instance to the handler.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/body/#results]
A.f3: Path-declared parameters bind from the path, scalar parameters generally bind from the query, and model parameters bind from the body, so these inputs can coexist in one operation.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/body/#request-body-path-query-parameters]
note: Establish this first: Structured bodies are distinct from URL inputs.
note: Stay within the current objective: Declare JSON bodies. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine body binding.
PRACTICE ANCHOR (live_code): Add a body parameter annotated with OrderInput to the supplied order-creation handler, preserving its existing customer identifier and scalar query option.  SUCCESS: The handler declares one structured body using OrderInput. The customer identifier remains bound from the path, and the ordinary scalar option remains bound from the query.
ASSESSMENT ANCHOR: determine_body_path_and_query_binding facts=['f1', 'f3']
ASSESSMENT ANCHOR: trace_json_body_to_validated_model_instance facts=['f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Backward-compatible REST contract changes; Bearer-token extraction into an authentication dependency; Bounded form and multipart file inputs; CORS origin and credential policy; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Credential and sensitive-data redaction from emitted logs; Distinct create and partial-update contracts; Endpoint integration tests using TestClient or async HTTPX as appropriate; FastAPI OpenAPI generation from typed route contracts; Graceful termination and shutdown verification; Header and cookie input binding; Meaningful contract examples and operation metadata; Preventing unsafe outbound requests and SSRF; Redis cache-aside selection and population; Request-scoped async-compatible PostgreSQL session lifecycle; Request-scoped dependency reuse and lifetime; Request-validation error behavior; Required, optional and default input semantics; Retrieve resource; Service health and readiness checks; Structured service request and error logs; Test dependency replacement; Transaction commit and rollback boundaries; Trusted host validation; Yield-based dependency cleanup

## LESSON, in learner order

### s01 · explainer · Declare the boundary: Binding request bodies to typed models
Explainer — 
(mechanism) Bind structured JSON by defining a BaseModel subclass and typing a handler parameter with that model. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) FastAPI reads JSON, converts compatible values, validates the declared model, then gives the handler a model instance. ⟦A.f2 A:tb3⟧
(mechanism) Path-declared parameters come from the path; ordinary scalars generally come from the query; model parameters come from the body. One operation can receive all three. ⟦A.f3 A:tb3⟧
[CODE python]
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
class OrderInput(BaseModel):
    quantity: int
@app.post('/customers/{customer_id}/orders')
def create_order(customer_id: int, body: OrderInput, option: str = 'standard'):
    return {'customer_id': customer_id, 'option': option}

  annotations: ['BaseModel describes the structured body.', 'customer_id: path; option: generally query; body: JSON model.']

### s02 · explainer · Trace the contract
Explainer — 
(mental_model) Read the signature as a source map: the customer identifier is path input, an ordinary scalar option generally comes from the query, and OrderInput is structured body input. For the body, trace JSON reading, compatible conversion, model validation and delivery of the model instance. A body field is not an assumed query parameter. ⟦A.f1 A.f2 A.f3 A:tb4⟧

### s03 · explainer · Work through the supplied example
Explainer — 
(walkthrough) OrderInput declares the body’s shape. Add a body parameter typed with it while keeping the path identifier and ordinary scalar option. Trace JSON to compatible conversion to validation to the model supplied to the handler. A combined operation can receive these inputs together; the model declaration identifies the structured body rather than scattering its fields into assumed query inputs. ⟦A.f1 A.f2 A.f3 A:tb5 A:tb6⟧

### s04 · check · Check the boundary: Binding request bodies to typed models
Check — Use the supplied order-service scenario to reason about this contract.

### s05 · hands_on · Apply the contract: Binding request bodies to typed models
Hands On — Complete the supplied workspace within its stated contract.

### s06 · recap · Keep these distinctions
Recap — 
(takeaway) Type a model parameter for JSON; trace conversion and validation; distinguish path, ordinary query and body inputs. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
[UP NEXT] Next: tile_040 — Yield-based dependency cleanup: Start with Yield-based dependency cleanup.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Binding request bodies to typed models
(definition) FastAPI reads JSON, converts compatible values, validates the declared model, then gives the handler a model instance. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(example) For OrderInput, the handler receives a model after compatible conversion and validation, not merely an assumed-valid JSON body. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast: Binding request bodies to typed models
(definition) Bind structured JSON by defining a BaseModel subclass and typing a handler parameter with that model. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Path-declared parameters come from the path; ordinary scalars generally come from the query; model parameters come from the body. One operation can receive all three. ⟦A.f3 A:tb3 A:tb4 A:tb5 A:tb6⟧
(example) For the order handler, a body typed as OrderInput is structured JSON input, not an ordinary scalar query option. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧

=========

# EVALUATOR PACKET — Yield-based dependency cleanup (tile_040)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.yield_dependencies — Yield-based dependency cleanup

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (fastapi.yield_dependencies)   objective: Release yield dependency resources: provide and close one request resource.
A.f1: A dependency with yield acquires a resource before yielding it and supplies that yielded value to the operation.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#a-database-dependency-with-yield]
A.f2: Put resource release in a finally block surrounding yield so exit cleanup runs after successful use or an exception.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#a-dependency-with-yield-and-try]
A.f3: A yielding dependency defaults to request scope, ending after the response is sent; Depends(provider, scope="function") ends it after the handler finishes but before sending the response.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#early-exit-and-scope]
A.f4: If a yielding dependency catches an exception without intentionally handling it, re-raise it rather than silently concealing the failure from FastAPI.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#always-raise-in-dependencies-with-yield-and-except]
note: Establish this first: Yield encloses execution in a resource boundary.
note: Stay within the current objective: Release yield dependency resources. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine cleanup after success and failure.
PRACTICE ANCHOR (live_code): Implement a yielding provider that supplies one resource to an operation and closes it in finally. Compare default request scope with explicit function scope, and preserve any unhandled exception.  SUCCESS: The operation receives the yielded resource. Release runs on both successful and exceptional exits. Default request-scope cleanup occurs after response sending; function-scope cleanup occurs after handler completion but before response sending. Any caught, unhandled exception is re-raised.
ASSESSMENT ANCHOR: determine_resource_cleanup_after_success_and_failure facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_request_and_function_cleanup_boundaries facts=['f3']
ASSESSMENT ANCHOR: preserve_cleanup_and_exception_visibility facts=['f2', 'f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Bearer-token extraction into an authentication dependency; Bounded form and multipart file inputs; CORS origin and credential policy; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Credential and sensitive-data redaction from emitted logs; Distinct create and partial-update contracts; Endpoint integration tests using TestClient or async HTTPX as appropriate; FastAPI OpenAPI generation from typed route contracts; Graceful termination and shutdown verification; Header and cookie input binding; Meaningful contract examples and operation metadata; Preventing unsafe outbound requests and SSRF; Redis cache-aside selection and population; Request-scoped async-compatible PostgreSQL session lifecycle; Request-scoped dependency reuse and lifetime; Request-validation error behavior; Required, optional and default input semantics; Retrieve resource; Service health and readiness checks; Structured service request and error logs; Test dependency replacement; Transaction commit and rollback boundaries; T

## LESSON, in learner order

### s01 · explainer · Declare the boundary: Yield-based dependency cleanup
Explainer — 
(mechanism) Acquire the resource before yield. The dependency supplies the yielded resource to the operation. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) Surround yield with try/finally and release the resource in finally, covering successful use and exceptions. ⟦A.f2 A:tb3⟧
(mechanism) Default request scope ends after response sending. Depends(provider, scope="function") ends after handler completion, before the response is sent. ⟦A.f3 A:tb3⟧
(mechanism) If you catch an exception without intentionally handling it, re-raise it. Do not conceal the failure from FastAPI. ⟦A.f4 A:tb3⟧
[PROCESS_FLOW: Resource ownership and scope boundaries] nodes=['Acquire resource', 'Yield to operation', 'Operation uses resource', 'Handler completion', 'Declared scope', 'Function scope: cleanup', 'Send response', 'Default request scope: cleanup', 'Exceptional use', 'Re-raise unhandled exception', 'finally: release resource'] edges=[('acquire', 'yield', None), ('yield', 'use', None), ('use', 'done', 'success'), ('done', 'choice', None), ('choice', 'function', 'scope="function"'), ('function', 'response', None), ('choice', 'response', 'default request scope'), ('response', 'request', 'default only'), ('use', 'exception', 'failure'), ('exception', 'raise', 'not intentionally handled'), ('raise', 'finally', None)] alt: Resource ownership and scope boundaries: Acquire resource; Yield to operation; Operation uses resource; Handler completion; Declared scope; Function scope: cleanup; Send response; Default request scope: cleanup; Exceptional use; Re-raise unhandled exception; finally: release resource

### s02 · explainer · Trace the contract
Explainer — 
(mental_model) Trace acquisition, yield and operation use separately. Put release in finally so both successful and exceptional paths clean up. Default request scope ends after response sending; function scope ends after handler completion, before sending. If a caught exception was not intentionally handled, re-raise it. Yield is not a promise that every dependency ends at handler completion. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Check the boundary: Yield-based dependency cleanup
Check — Use the supplied order-service scenario to reason about this contract.

### s04 · hands_on · Apply the contract: Yield-based dependency cleanup
Hands On — Complete the supplied workspace within its stated contract.

### s05 · recap · Keep these distinctions
Recap — 
(takeaway) Acquire before yield; release in finally; distinguish request and function scope; re-raise unhandled exceptions. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: tile_041 — Structured service request and error logs: Start with Structured service request and error logs.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Yield-based dependency cleanup
(definition) Surround yield with try/finally and release the resource in finally, covering successful use and exceptions. ⟦A.f2 A:tb3 A:tb4⟧
(definition) If you catch an exception without intentionally handling it, re-raise it. Do not conceal the failure from FastAPI. ⟦A.f4 A:tb3 A:tb4⟧
(example) For the supplied resource, cleanup on failure and failure visibility are separate: finally releases it, while re-raising an unhandled exception keeps the failure visible. ⟦A.f2 A.f4 A:tb3 A:tb4⟧
### r02 · Try the contrast: Yield-based dependency cleanup
(definition) Acquire the resource before yield. The dependency supplies the yielded resource to the operation. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Surround yield with try/finally and release the resource in finally, covering successful use and exceptions. ⟦A.f2 A:tb3 A:tb4⟧
(definition) Default request scope ends after response sending. Depends(provider, scope="function") ends after handler completion, before the response is sent. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(definition) If you catch an exception without intentionally handling it, re-raise it. Do not conceal the failure from FastAPI. ⟦A.f4 A:tb3 A:tb4⟧
(example) For the supplied resource, cleanup in finally covers failure too; cleanup only on the successful return branch does not. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Structured service request and error logs (tile_041)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = observability.structured_service_logs — Structured service request and error logs

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (observability.structured_service_logs)   objective: Emit structured diagnostics: add structured logs for one failure.
A.f1: A useful event log records when and where an event happened, its type and severity, and enough context to interpret the event's outcome.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#event-attributes]
A.f2: For a failure, record consistently named fields for timestamp, application or code location, event type, severity, result status and reason rather than an unexplained free-text message.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#event-attributes]
A.f3: Emit logger.error(message, extra=event_fields) with the standard logging library to attach structured fields to the LogRecord, and configure the existing formatter or collection pipeline to preserve those field names; custom keys must not collide with reserved LogRecord attributes.   [sources: python_tutorial#https://docs.python.org/3/library/logging.html#logging.Logger.debug, owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#event-collection]
note: Establish this first: Logs are structured event records.
note: Stay within the current objective: Emit structured diagnostics. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify insufficient failure logs.
PRACTICE ANCHOR (live_code): Add structured logging for one synthetic order failure using consistently named event fields, and configure the supplied formatter to preserve those fields.  SUCCESS: The emitted failure record preserves timestamp, code location, event type, severity, result status and reason under consistent field names. The logging call uses extra=event_fields, and custom keys do not collide with reserved LogRecord attributes.
ASSESSMENT ANCHOR: identify_missing_failure_event_context facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_structured_field_emission_and_preservation_gaps facts=['f3']
ASSESSMENT ANCHOR: identify_reserved_log_record_attribute_collisions facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; Bounded form and multipart file inputs; CORS origin and credential policy; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Credential and sensitive-data redaction from emitted logs; Distinct create and partial-update contracts; Endpoint integration tests using TestClient or async HTTPX as appropriate; FastAPI OpenAPI generation from typed route contracts; Graceful termination and shutdown verification; Header and cookie input binding; Meaningful contract examples and operation metadata; Preventing unsafe outbound requests and SSRF; Redis cache-aside selection and population; Request-scoped async-compatible PostgreSQL session lifecycle; Request-scoped dependency reuse and lifetime; Request-validation error behavior; Required, optional and default input semantics; Retrieve resource; Service health and readiness checks; Test dependency replacement; Transaction commit and rollback bounda

## LESSON, in learner order

### s01 · explainer · Declare the boundary: Structured service request and error logs
Explainer — 
(mechanism) An interpretable event log says when and where an event happened, its type and severity, and enough context to understand the outcome. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) For a failure, use consistent field names for timestamp, application or code location, event type, severity, result status and reason—not just unexplained free text. ⟦A.f2 A:tb3⟧
(mechanism) logger.error(message, extra=event_fields) attaches fields to the LogRecord. Configure the existing formatter or collector to preserve their names, and avoid custom keys that collide with reserved LogRecord attributes. ⟦A.f3 A:tb3⟧
[BEFORE_AFTER] Before: unexplained message. After: preserve the six named failure fields through the existing formatter. Emitted output is computed, not an observed production event.
  before:
[CODE python]
import io
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

logger.error('failed')
print(captured_output.getvalue(), end='')

  annotations: []
  after:
[CODE python]
import io
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

event_fields = dict(failure_values)
existing_handler.setFormatter(logging.Formatter('timestamp=%(timestamp)s code_location=%(code_location)s event_type=%(event_type)s event_severity=%(event_severity)s result_status=%(result_status)s reason=%(reason)s'))
logger.error('order failure', extra=event_fields)
print(captured_output.getvalue(), end='')

  annotations: []

### s02 · explainer · Trace the contract
Explainer — 
(mental_model) Follow the fields from event_fields into the LogRecord and then into the emitted record. Use timestamp, code location, event type, severity, result status and reason consistently. Passing extra is not enough: inspect the existing formatter or collector to ensure those names survive. Custom names must not collide with reserved LogRecord attributes. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · check · Check the boundary: Structured service request and error logs
Check — Use the supplied order-service scenario to reason about this contract.

### s04 · hands_on · Apply the contract: Structured service request and error logs
Hands On — Complete the supplied workspace within its stated contract.

### s05 · recap · Keep these distinctions
Recap — 
(takeaway) Name failure fields consistently, attach them with extra, avoid reserved names and preserve them in emitted output. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: tile_042 — Preventing unsafe outbound requests and SSRF: Start with Preventing unsafe outbound requests and SSRF.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Structured service request and error logs
(definition) logger.error(message, extra=event_fields) attaches fields to the LogRecord. Configure the existing formatter or collector to preserve their names, and avoid custom keys that collide with reserved LogRecord attributes. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) For the supplied order failure, attaching extra fields differs from preserving them in emitted output. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast: Structured service request and error logs
(definition) An interpretable event log says when and where an event happened, its type and severity, and enough context to understand the outcome. ⟦A.f1 A:tb2 A:tb4⟧
(definition) For a failure, use consistent field names for timestamp, application or code location, event type, severity, result status and reason—not just unexplained free text. ⟦A.f2 A:tb3 A:tb4⟧
(definition) logger.error(message, extra=event_fields) attaches fields to the LogRecord. Configure the existing formatter or collector to preserve their names, and avoid custom keys that collide with reserved LogRecord attributes. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) For the supplied order failure, attaching extra fields differs from preserving them in emitted output. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Preventing unsafe outbound requests and SSRF (tile_042)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = security.safe_outbound_requests — Preventing unsafe outbound requests and SSRF

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (security.safe_outbound_requests)   objective: Constrain outbound destinations: implement one destination policy.
A.f1: When destinations are known, enforce a destination allowlist instead of allowing an untrusted value to choose an arbitrary outbound URL.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html#application-layer]
A.f2: A destination policy must reject private, loopback, link-local and other non-public addresses, including IPv6 equivalents, when access is intended only to public services.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html#case-2-application-can-send-requests-to-any-external-ip-address-or-domain-name]
A.f3: Validate the resolved address actually used for the connection, not merely a hostname checked earlier, to avoid a DNS rebinding gap.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html#ssrf-prevention-publisher-side]
A.f4: Disable automatic redirects or apply the same destination checks to each redirect target so a permitted initial URL cannot redirect into a forbidden destination.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html#application-layer, owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html#ssrf-prevention-publisher-side]
note: Establish this first: Untrusted input must not select privileged destinations.
note: Stay within the current objective: Constrain outbound destinations. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify SSRF network-trust violations.
PRACTICE ANCHOR (live_code): Implement a destination allowlist that maps a requested provider to a fixed, approved destination and rejects unknown providers instead of treating their input as an outbound URL.  SUCCESS: Known provider values return only their configured destinations. Unknown provider values, including arbitrary URL strings, are rejected. This implements destination selection, not the separate connected-address and redirect checks.
ASSESSMENT ANCHOR: identify_arbitrary_destination_selection facts=['f1']
ASSESSMENT ANCHOR: identify_non_public_address_boundary_violations facts=['f2']
ASSESSMENT ANCHOR: identify_dns_rebinding_validation_gaps facts=['f3']
ASSESSMENT ANCHOR: identify_redirect_destination_policy_bypasses facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; Bounded form and multipart file inputs; CORS origin and credential policy; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Credential and sensitive-data redaction from emitted logs; Distinct create and partial-update contracts; Endpoint integration tests using TestClient or async HTTPX as appropriate; FastAPI OpenAPI generation from typed route contracts; Graceful termination and shutdown verification; Header and cookie input binding; Keeping API schemas distinct from persistence entities; Meaningful contract examples and operation metadata; Redis cache-aside selection and population; Request-scoped async-compatible PostgreSQL session lifecycle; Request-scoped dependency reuse and lifetime; Request-validation error behavior; Required, optional and default input semantics; Retrieve resource; Service health and readiness checks; Test dependency replacement; Transaction commit and rollb

## LESSON, in learner order

### s01 · explainer · Declare the boundary: Preventing unsafe outbound requests and SSRF
Explainer — 
(mechanism) For known destinations, map untrusted provider input to an allowed destination instead of accepting an arbitrary outbound URL. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) For public-only access, reject private, loopback, link-local and other non-public addresses, including IPv6 equivalents. ⟦A.f2 A:tb3⟧
(mechanism) Validate the resolved address actually used for the connection. Checking a hostname earlier is insufficient against a DNS rebinding gap. ⟦A.f3 A:tb3⟧
(mechanism) Disable automatic redirects or enforce the same destination checks on every redirect target. An allowed starting URL can redirect somewhere forbidden. ⟦A.f4 A:tb3⟧
[DIAGRAM: Outbound destination trust boundary] nodes=['Requested provider', 'Allowlist: catalog → https://catalog.example/lookup; shipping → https://shipping.example/lookup', 'Validate resolved address actually used', 'Reject private, loopback, link-local and other non-public IPv4/IPv6', 'Redirect target: same checks or disable automatic redirects', 'Public-only connection boundary'] edges=[('input', 'map', 'reject arbitrary destinations'), ('map', 'address', 'not just earlier hostname check'), ('address', 'deny', 'non-public'), ('address', 'public', 'policy permits'), ('public', 'redirect', 'redirect response'), ('redirect', 'map', 'reapply destination checks')] alt: Outbound destination trust boundary: Requested provider; Allowlist: catalog → https://catalog.example/lookup; shipping → https://shipping.example/lookup; Validate resolved address actually used; Reject private, loopback, link-local and other non-public IPv4/IPv6; Redirect target: same checks or disable automatic redirects; Public-only connection boundary

### s02 · explainer · Trace the contract
Explainer — 
(mental_model) Trace three boundaries, not just one hostname: requested provider, address actually connected to, and redirect target. Map known providers to allowed destinations. Reject non-public IPv4 and IPv6 addresses for public-only access, and validate the resolved address used by the connection. Disable redirects or check each target. A permitted-looking hostname alone leaves the connected-address and redirect boundaries unverified. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Check the boundary: Preventing unsafe outbound requests and SSRF
Check — Use the supplied order-service scenario to reason about this contract.

### s04 · check · Check the boundary: Preventing unsafe outbound requests and SSRF
Check — Use the supplied order-service scenario to reason about this contract.

### s05 · hands_on · Apply the contract: Preventing unsafe outbound requests and SSRF
Hands On — Complete the supplied workspace within its stated contract.

### s06 · recap · Keep these distinctions
Recap — 
(takeaway) Allowlist destinations; reject non-public IPv4/IPv6; validate connected addresses; disable or recheck redirects. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: tile_043 — Bounded form and multipart file inputs: Start with Bounded form and multipart file inputs.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Preventing unsafe outbound requests and SSRF
(definition) For public-only access, reject private, loopback, link-local and other non-public addresses, including IPv6 equivalents. ⟦A.f2 A:tb3 A:tb4⟧
(example) For public-only outbound access, a loopback address is forbidden even in IPv6 form; changing address family does not change that boundary. ⟦A.f2 A:tb3 A:tb4⟧
### r02 · Try the contrast: Preventing unsafe outbound requests and SSRF
(definition) Validate the resolved address actually used for the connection. Checking a hostname earlier is insufficient against a DNS rebinding gap. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) For the provider lookup, an earlier hostname check differs from validating the resolved address actually used for the connection. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r03 · Try the contrast: Preventing unsafe outbound requests and SSRF
(definition) For known destinations, map untrusted provider input to an allowed destination instead of accepting an arbitrary outbound URL. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Disable automatic redirects or enforce the same destination checks on every redirect target. An allowed starting URL can redirect somewhere forbidden. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(example) A configured provider destination is allowed as a starting point, but a redirect from it must still satisfy the destination policy or be disabled. ⟦A.f1 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Bounded form and multipart file inputs (tile_043)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.bounded_multipart_inputs — Bounded form and multipart file inputs

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (fastapi.bounded_multipart_inputs)   objective: Accept bounded form and multipart inputs: implement one bounded multipart endpoint with form metadata and a file.
A.f1: Declare form metadata with Annotated[Type, Form()] and an uploaded file with Annotated[UploadFile, File()] in the same multipart handler; multipart parsing requires python-multipart.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/request-forms-and-files/#define-file-and-form-parameters]
A.f2: UploadFile uses a spooled file rather than requiring the entire upload to be represented as bytes in memory, and exposes asynchronous read, seek and close methods.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/request-files/#uploadfile]
A.f3: Apply RequestBodyLimitMiddleware with a finite max_body_size to count actual incoming body bytes, including multipart overhead, and return 413 when the limit is exceeded.   [sources: fastapi_docs_advanced#https://starlette.dev/middleware/#requestbodylimitmiddleware]
A.f4: Multipart parsing can separately bound file count, field count and non-file field size with request.form(max_files=..., max_fields=..., max_part_size=...); these controls do not replace a total body limit.   [sources: fastapi_docs_advanced#https://starlette.dev/requests/#request-files]
A.f5: Reject disallowed content types and validate the supplied fields before processing, then close an UploadFile with await file.close() when finished with its resource.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html#input-validation, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/request-files/#uploadfile]
note: Establish this first: Multipart is an untrusted structured stream, not an unlimited in-memory value.
note: Stay within the current objective: Accept bounded form and multipart inputs. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Reject oversized or disallowed multipart data while binding form values and handling file resources safely.
PRACTICE ANCHOR (live_code): Implement one bounded attachment endpoint that binds form metadata and an uploaded file, enforces a finite total body budget and separate multipart parser limits, validates inputs before processing, and closes the uploaded file.  SUCCESS: The endpoint accepts permitted metadata and attachment content, rejects disallowed attachment content types and invalid metadata before processing, returns 413 when actual body bytes exceed the budget, applies the configured parser limits before binding, and closes every file resource it handles.
ASSESSMENT ANCHOR: bind_form_metadata_and_uploaded_file facts=['f1']
ASSESSMENT ANCHOR: handle_spooled_upload_resources_safely facts=['f2', 'f5']
ASSESSMENT ANCHOR: enforce_actual_multipart_body_byte_limit facts=['f3']
ASSESSMENT ANCHOR: distinguish_multipart_parser_limits_from_total_body_limit facts=['f3', 'f4']
ASSESSMENT ANCHOR: reject_disallowed_upload_types_and_invalid_metadata facts=['f5']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; CORS origin and credential policy; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Credential and sensitive-data redaction from emitted logs; Distinct create and partial-update contracts; Endpoint integration tests using TestClient or async HTTPX as appropriate; FastAPI OpenAPI generation from typed route contracts; Graceful termination and shutdown verification; Header and cookie input binding; Keeping API schemas distinct from persistence entities; Meaningful contract examples and operation metadata; Redis cache-aside selection and population; Request-scoped async-compatible PostgreSQL session lifecycle; Request-scoped dependency reuse and lifetime; Request-validation error behavior; Required, optional and default input semantics; Retrieve resource; Service health and readiness checks; Test dependency replacement; Transaction commit and rollback boundaries; Translating domain and p

## LESSON, in learner order

### s01 · explainer · Declare the boundary: Bounded form and multipart file inputs
Explainer — 
(mechanism) In one multipart handler, declare metadata with Annotated[Type, Form()] and the file with Annotated[UploadFile, File()]. Install python-multipart for parsing. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) UploadFile uses a spooled file rather than requiring the entire upload as in-memory bytes. Its read, seek and close methods are asynchronous. ⟦A.f2 A:tb3⟧
(mechanism) Set a finite RequestBodyLimitMiddleware max_body_size. Count actual incoming bytes, including multipart overhead; exceeding that limit returns 413. ⟦A.f3 A:tb3⟧
(mechanism) request.form(max_files=..., max_fields=..., max_part_size=...) separately limits file count, field count and non-file field size. These limits do not replace the total-body limit. ⟦A.f4 A:tb3⟧
(mechanism) Reject disallowed content types and validate fields before processing. When finished, release the upload with await file.close(). ⟦A.f5 A:tb3⟧
[CODE python]
from typing import Annotated
from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from support import (RequestBodyLimitMiddleware, BoundedMultipartRoute,
                     budgets, permitted_content_types)
app = FastAPI()
app.router.route_class = BoundedMultipartRoute
app.add_middleware(RequestBodyLimitMiddleware,
                   max_body_size=budgets['max_body_size'])
@app.post('/orders/attachments')
async def attachment(metadata: Annotated[str, Form()],
                     file: Annotated[UploadFile, File()]):
    try:
        if file.content_type not in permitted_content_types:
            raise HTTPException(status_code=400, detail='disallowed content type')
        if len(metadata) > budgets['metadata_max_length']:
            raise HTTPException(status_code=400, detail='invalid metadata')
        data = await file.read(budgets['read_size'])
        await file.seek(0)
        return {'metadata': metadata}
    finally:
        await file.close()

  annotations: ['Total actual-body-byte boundary, including multipart overhead.', 'Typed form metadata and spooled file; python-multipart required.', 'Validate before reading.', 'Asynchronous cleanup on success or rejection.']
[CODE python]
from fastapi.routing import APIRoute
from support import budgets
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

  annotations: ['Parser limits run before automatic typed parameter binding; non-file part size is separate from the total body budget.']

### s02 · explainer · Trace the contract
Explainer — 
(mental_model) Treat limits as separate controls. Form and File declarations need python-multipart; a spooled UploadFile offers asynchronous resource methods, not unlimited input. The finite body budget counts actual bytes including overhead and returns 413 on excess. Parser options bound file count, field count and non-file field size, but do not replace that budget. Validate fields and content type before processing, and close the file afterward. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb4 A:tb5⟧

### s03 · check · Check the boundary: Bounded form and multipart file inputs
Check — Use the supplied order-service scenario to reason about this contract.

### s04 · hands_on · Apply the contract: Bounded form and multipart file inputs
Hands On — Complete the supplied workspace within its stated contract.

### s05 · recap · Keep these distinctions
Recap — 
(takeaway) Bind Form/File inputs; use spooled asynchronous uploads; enforce total and parser limits separately; validate before processing and close files. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: tile_044 — CORS origin and credential policy: Start with CORS origin and credential policy.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Bounded form and multipart file inputs
(definition) Reject disallowed content types and validate fields before processing. When finished, release the upload with await file.close(). ⟦A.f5 A:tb3 A:tb4⟧
(example) For the supplied attachment, a permitted content type does not excuse invalid metadata; both must pass before processing. ⟦A.f5 A:tb3 A:tb4⟧
### r02 · Try the contrast: Bounded form and multipart file inputs
(definition) In one multipart handler, declare metadata with Annotated[Type, Form()] and the file with Annotated[UploadFile, File()]. Install python-multipart for parsing. ⟦A.f1 A:tb2 A:tb4⟧
(definition) UploadFile uses a spooled file rather than requiring the entire upload as in-memory bytes. Its read, seek and close methods are asynchronous. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Set a finite RequestBodyLimitMiddleware max_body_size. Count actual incoming bytes, including multipart overhead; exceeding that limit returns 413. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(definition) request.form(max_files=..., max_fields=..., max_part_size=...) separately limits file count, field count and non-file field size. These limits do not replace the total-body limit. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(definition) Reject disallowed content types and validate fields before processing. When finished, release the upload with await file.close(). ⟦A.f5 A:tb3 A:tb4⟧
(example) For the supplied attachment, a permitted content type does not excuse invalid metadata; both must pass before processing. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — CORS origin and credential policy (tile_044)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.cors_policy — CORS origin and credential policy

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (fastapi.cors_policy)   objective: Set safe CORS policy: configure one browser-client policy.
A.f1: Configure app.add_middleware(CORSMiddleware, allow_origins=[...], allow_methods=[...], allow_headers=[...], allow_credentials=...) with the origins, methods and headers the browser client actually needs.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/cors/#use-corsmiddleware]
A.f2: CORSMiddleware defaults are restrictive: allowed methods default to GET and credentials default to false.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/cors/#use-corsmiddleware]
A.f3: When allow_credentials=True, explicitly specify allowed origins, methods and headers rather than wildcard lists.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/cors/#use-corsmiddleware]
A.f4: CORS signals browser access permission; it does not replace access-control checks at API endpoints.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html#cors, owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html#access-control]
note: Establish this first: CORS controls browser response access, not authentication.
note: Stay within the current objective: Set safe CORS policy. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify unsafe origin and credential combinations.
PRACTICE ANCHOR (live_code): Configure CORSMiddleware for the browser client at https://shop.example, allowing GET and POST requests with the Content-Type header and credentialed browser access.  SUCCESS: The application registers CORSMiddleware with the exact client origin, explicit GET and POST methods, an explicit Content-Type header list, and allow_credentials=True, without wildcard entries.
ASSESSMENT ANCHOR: identify_unsafe_origin_and_credential_combinations facts=['f1', 'f3']
ASSESSMENT ANCHOR: recognize_restrictive_cors_defaults facts=['f2']
ASSESSMENT ANCHOR: distinguish_browser_access_from_endpoint_access_control facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Consistent public error envelopes through exception handlers; Credential and sensitive-data redaction from emitted logs; Distinct create and partial-update contracts; Endpoint integration tests using TestClient or async HTTPX as appropriate; FastAPI OpenAPI generation from typed route contracts; Graceful termination and shutdown verification; Header and cookie input binding; Keeping API schemas distinct from persistence entities; Meaningful contract examples and operation metadata; Redis cache-aside selection and population; Request-scoped async-compatible PostgreSQL session lifecycle; Request-scoped dependency reuse and lifetime; Request-validation error behavior; Required, optional and default input semantics; Retrieve resource; Service health and readiness checks; Test dependency replacement; Transaction commit and rollback boundarie

## LESSON, in learner order

### s01 · explainer · Declare the boundary: CORS origin and credential policy
Explainer — 
(mechanism) Use app.add_middleware(CORSMiddleware, ...) with allow_origins, allow_methods, allow_headers and allow_credentials matching the browser client’s actual needs. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) Defaults are restrictive: allowed methods default to GET, and credentials default to false. ⟦A.f2 A:tb3⟧
(mechanism) With allow_credentials=True, specify origins, methods and headers explicitly rather than using wildcard lists. ⟦A.f3 A:tb3⟧
(mechanism) CORS grants browser access permission; endpoint access-control checks remain separate and necessary. ⟦A.f4 A:tb3⟧
[CODE python]
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
# Content-Type, and credentials; use explicit lists with no wildcards.
app.add_middleware(CORSMiddleware,
    allow_origins=['https://shop.example'],
    allow_methods=['GET', 'POST'],
    allow_headers=['Content-Type'],
    allow_credentials=True)

  annotations: ['Explicit shop-client permissions; credentials enabled. Browser permission does not replace endpoint access checks.']

### s02 · explainer · Trace the contract
Explainer — 
(mental_model) The shop browser needs its origin, methods and headers listed explicitly, with credentials enabled for this scenario. Defaults alone allow GET and leave credentials false. When credentials are true, do not use wildcard lists for origins, methods or headers. CORS answers a browser-permission question, not whether an endpoint should grant access. Keep endpoint access-control checks separate. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Check the boundary: CORS origin and credential policy
Check — Use the supplied order-service scenario to reason about this contract.

### s04 · hands_on · Apply the contract: CORS origin and credential policy
Hands On — Complete the supplied workspace within its stated contract.

### s05 · recap · Keep these distinctions
Recap — 
(takeaway) Match explicit CORS lists to the browser; remember restrictive defaults; credentials require explicit lists; endpoint access checks remain separate. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: tile_045 — Request-scoped dependency reuse and lifetime: Start with Request-scoped dependency reuse and lifetime.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: CORS origin and credential policy
(definition) Defaults are restrictive: allowed methods default to GET, and credentials default to false. ⟦A.f2 A:tb3 A:tb4⟧
(example) For the shop client, do not assume permissive defaults: default allowed methods are GET and default credentials are false. ⟦A.f2 A:tb3 A:tb4⟧
### r02 · Try the contrast: CORS origin and credential policy
(definition) Use app.add_middleware(CORSMiddleware, ...) with allow_origins, allow_methods, allow_headers and allow_credentials matching the browser client’s actual needs. ⟦A.f1 A:tb2 A:tb4⟧
(definition) With allow_credentials=True, specify origins, methods and headers explicitly rather than using wildcard lists. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(definition) CORS grants browser access permission; endpoint access-control checks remain separate and necessary. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(example) For the shop browser, explicit client permissions differ from endpoint access control; CORS does not replace it. ⟦A.f1 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Request-scoped dependency reuse and lifetime · Endpoint integration tests using TestClient or async HTTPX as appropriate (tile_045)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.dependency_lifetime — Request-scoped dependency reuse and lifetime
B = fastapi.endpoint_integration_tests — Endpoint integration tests using TestClient or async HTTPX as appropriate

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (fastapi.dependency_lifetime)   objective: Control dependency reuse: verify one shared provider's identity.
A.f1: FastAPI normally caches a dependency's returned value within one request when multiple dependants declare the same dependency.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/#using-the-same-dependency-multiple-times]
A.f2: Set Depends(provider, use_cache=False) when that declaration needs a fresh execution instead of the cached result.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/#using-the-same-dependency-multiple-times]
A.f3: Verify request-local reuse by having two dependants receive the same provider result during one request and checking a fresh request independently; this cache is not application-wide storage.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/#using-the-same-dependency-multiple-times]
note: Establish this first: Caching has request-local identity and lifetime.
note: Stay within the current objective: Control dependency reuse. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Predict reuse within one request.
PRACTICE ANCHOR (live_code): Have two dependants declare the same provider, compare their received values by identity during one request, and repeat the check in a fresh request.  SUCCESS: Requests A and B each report that both dependants received the same instance. Provider execution records show one execution in A and a separate execution in B, establishing reuse within each request rather than across requests.
ASSESSMENT ANCHOR: predict_shared_dependency_reuse_within_one_request facts=['f1']
ASSESSMENT ANCHOR: predict_fresh_execution_for_uncached_declaration facts=['f2']
ASSESSMENT ANCHOR: distinguish_request_local_reuse_from_application_wide_storage facts=['f3']

## SOURCE FACTS — B (fastapi.endpoint_integration_tests)   objective: Test an endpoint through its HTTP interface: write one integration test with TestClient or compatible async HTTPX setup.
B.f1: Create TestClient(app), send an HTTP request with client.get(...) or another request method, and assert response.status_code and response.json() in a test_ function run by pytest.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/testing/#using-testclient]
B.f2: Use with TestClient(app) as client when the test must execute application lifespan setup and teardown.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/testing-events/#testing-events-lifespan-and-startup-shutdown]
B.f3: Sending a request through TestClient exercises the application's route and dependency resolution rather than only calling the handler function directly.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/testing/#using-testclient, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/#declare-the-dependency-in-the-dependant]
note: Establish this first: Integration tests exercise the application boundary rather than calling a handler directly.
note: Stay within the current objective: Test an endpoint through its HTTP interface. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Assert status and payload including dependency and lifespan behavior.
PRACTICE ANCHOR (live_code): Write one pytest test for the supplied application's GET /orders/42 endpoint using a TestClient context manager, asserting status 200 and the JSON body {"id": 42, "quantity": 2}.  SUCCESS: Pytest discovers and passes the test. The test sends an HTTP request through the supplied application, asserts both status and JSON, and uses the context manager to include lifespan setup and teardown.
ASSESSMENT ANCHOR: assert_endpoint_status_and_json_payload facts=['f1']
ASSESSMENT ANCHOR: include_application_lifespan_in_test_boundary facts=['f2']
ASSESSMENT ANCHOR: distinguish_http_route_and_dependency_resolution_from_direct_handler_calls facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Consistent public error envelopes through exception handlers; Credential and sensitive-data redaction from emitted logs; Distinct create and partial-update contracts; Endpoint integration tests using TestClient or async HTTPX as appropriate; FastAPI OpenAPI generation from typed route contracts; Graceful termination and shutdown verification; Header and cookie input binding; Keeping API schemas distinct from persistence entities; Meaningful contract examples and operation metadata; Proxy header trust; Redis cache-aside selection and population; Request-scoped async-compatible PostgreSQL session lifecycle; Request-validation error behavior; Required, optional and default input semantics; Retrieve resource; Service health and readiness checks; Test dependency replacement; Transaction commit and rollback boundaries; Translating domain and 

## LESSON, in learner order

### s01 · explainer · Declare the boundary: Request-scoped dependency reuse and lifetime
Explainer — 
(mechanism) FastAPI normally caches a dependency result within a request when several dependants declare the same dependency. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) Use Depends(provider, use_cache=False) on a declaration that needs fresh execution instead of the cached result. ⟦A.f2 A:tb3⟧
(mechanism) Check that two dependants receive the same provider result in one request, then examine a fresh request independently. This cache is request-local, not application-wide storage. ⟦A.f3 A:tb3⟧
[DIAGRAM: Separate request-cache boundaries] nodes=['Request A', 'Provider execution → value A', 'First dependant: same value A', 'Second dependant: same value A', 'Depends(provider, use_cache=False): fresh execution', 'Request B', 'Independent provider execution → value B', 'First dependant: value B', 'Second dependant: value B'] edges=[('a', 'pa', 'normal request-local cache'), ('pa', 'a1', 'reuse'), ('pa', 'a2', 'reuse'), ('a', 'fresh', 'explicit uncached declaration'), ('b', 'pb', 'new request'), ('pb', 'b1', 'reuse'), ('pb', 'b2', 'reuse')] alt: Separate request-cache boundaries: Request A; Provider execution → value A; First dependant: same value A; Second dependant: same value A; Depends(provider, use_cache=False): fresh execution; Request B; Independent provider execution → value B; First dependant: value B; Second dependant: value B

### s02 · explainer · Trace the contract
Explainer — 
(mental_model) Draw request A around its provider result and both dependants. Verify reuse inside that boundary, then inspect request B independently. On a declaration needing another execution, use Depends(provider, use_cache=False). The normal cache reduces repeat execution within one request; it does not turn a request-specific value into storage shared by all clients. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · check · Check the boundary: Request-scoped dependency reuse and lifetime
Check — Use the supplied order-service scenario to reason about this contract.

### s04 · check · Check the boundary: Request-scoped dependency reuse and lifetime
Check — Use the supplied order-service scenario to reason about this contract.

### s05 · hands_on · Apply the contract: Request-scoped dependency reuse and lifetime
Hands On — Complete the supplied workspace within its stated contract.

### s06 · explainer · Declare the boundary: Endpoint integration tests using TestClient or async HTTPX as appropriate
Explainer — 
(mechanism) Create TestClient(app), send a request such as client.get(...), and assert both response.status_code and response.json() in a pytest test_ function. ⟦B.f1 B:tb1 B:tb2⟧
(mechanism) When setup and teardown matter, use with TestClient(app) as client to execute application lifespan. ⟦B.f2 B:tb3⟧
(mechanism) A TestClient request exercises route and dependency resolution through the application. Calling the handler directly does not exercise that HTTP boundary. ⟦B.f3 B:tb3⟧
[CODE python]
from fastapi.testclient import TestClient
from app import app

def test_get_order():
    with TestClient(app) as client:
        response = client.get('/orders/42')
        assert response.status_code == 200
        assert response.json() == {'id': 42, 'quantity': 2}

  annotations: ['Context runs lifespan setup and teardown.', 'HTTP request exercises routing and dependency resolution.', 'Independent status and public JSON assertions; pytest executes test_get_order.']

### s07 · explainer · Trace the contract
Explainer — 
(mental_model) Specify an HTTP exchange, not merely a call that avoids crashing: method, path, expected status and expected public JSON. TestClient sends it through route and dependency resolution. Add the context manager when lifespan setup and teardown belong in the test. A direct handler call checks a different boundary and cannot establish the registered endpoint’s complete exchange. ⟦B.f1 B.f2 B.f3 B:tb4⟧

### s08 · explainer · Work through the supplied example
Explainer — 
(walkthrough) Use the supplied order fixture to make separate status and JSON assertions in test_get_order. Send the GET through TestClient rather than invoking get_order directly. Run the test_ function with pytest; use the context manager to execute lifespan when the case needs it. The status assertion checks the HTTP outcome, and the JSON assertion checks public content. Neither substitutes for the other. ⟦B.f1 B.f2 B.f3 B:tb5 B:tb6⟧

### s09 · video · Optional deeper walkthrough
Video — 
[VIDEO ] bridge-before:  | bridge-after: 

### s10 · check · Check the boundary: Endpoint integration tests using TestClient or async HTTPX as appropriate
Check — Use the supplied order-service scenario to reason about this contract.

### s11 · hands_on · Apply the contract: Endpoint integration tests using TestClient or async HTTPX as appropriate
Hands On — Complete the supplied workspace within its stated contract.

### s12 · recap · Keep these distinctions
Recap — 
(takeaway) Verify request-local reuse, check a fresh request independently, and request fresh execution with use_cache=False when needed. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Use a pytest test_ function to request the HTTP endpoint and assert status plus JSON; include lifespan through the TestClient context when needed. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧
[UP NEXT] Next: tile_047 — Required, optional and default input semantics: Start with Required, optional and default input semantics.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Request-scoped dependency reuse and lifetime
(definition) Use Depends(provider, use_cache=False) on a declaration that needs fresh execution instead of the cached result. ⟦A.f2 A:tb3 A:tb4⟧
(example) For a dependant needing a fresh provider execution, use_cache=False differs from relying on the normally cached result. ⟦A.f2 A:tb3 A:tb4⟧
### r02 · Try the contrast: Request-scoped dependency reuse and lifetime
(definition) Check that two dependants receive the same provider result in one request, then examine a fresh request independently. This cache is request-local, not application-wide storage. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) The order provider can reuse a result inside request A without making that result application-wide storage for request B. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r03 · Try the contrast: Request-scoped dependency reuse and lifetime
(definition) FastAPI normally caches a dependency result within a request when several dependants declare the same dependency. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(example) Within one order request, multiple dependants declaring the same provider normally reuse its returned value rather than requiring repeated execution. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
### r04 · Try the contrast: Endpoint integration tests using TestClient or async HTTPX as appropriate
(definition) A TestClient request exercises route and dependency resolution through the application. Calling the handler directly does not exercise that HTTP boundary. ⟦B.f3 B:tb3 B:tb4 B:tb5 B:tb6⟧
(example) For order retrieval, an HTTP request through TestClient differs from a direct call to get_order. ⟦B.f3 B:tb3 B:tb4 B:tb5 B:tb6⟧
### r05 · Try the contrast: Endpoint integration tests using TestClient or async HTTPX as appropriate
(definition) Create TestClient(app), send a request such as client.get(...), and assert both response.status_code and response.json() in a pytest test_ function. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(definition) When setup and teardown matter, use with TestClient(app) as client to execute application lifespan. ⟦B.f2 B:tb3 B:tb4 B:tb5 B:tb6⟧
(example) For the supplied order test, an HTTP status assertion does not substitute for the JSON assertion; use the TestClient context when lifespan must run. ⟦B.f1 B.f2 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧

=========

# EVALUATOR PACKET — Required, optional and default input semantics · FastAPI OpenAPI generation from typed route contracts (tile_047)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.input_presence_defaults — Required, optional and default input semantics
B = fastapi.openapi_generation — FastAPI OpenAPI generation from typed route contracts

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (fastapi.input_presence_defaults)   objective: Define required, nullable and default inputs: test omitted, null and concrete values for one input.
A.f1: Requiredness depends on whether a declaration supplies a default, while nullability depends on whether its type admits None.   [sources: pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/fields/#default-values, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/body/#request-body-path-query-parameters]
A.f2: A nullable field without a default still requires presence; writing field: Type | None = None permits both omission and an explicit null.   [sources: pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/fields/#default-values]
A.f3: Test absence, an explicit JSON null and a concrete value as separate requests and compare them with the field's declared default and nullable type.   [sources: pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/models/#basic-model-usage, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/testing/#using-testclient]
note: Establish this first: Presence and nullability are independent contract dimensions.
note: Stay within the current objective: Define required, nullable and default inputs. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Distinguish omission from explicit null and supplied values.
PRACTICE ANCHOR (live_code): Test three separate request bodies for note: an omitted field, explicit JSON null and a concrete string. Compare the results for note: str | None and note: str | None = None.  SUCCESS: Tests establish that the declaration without a default requires note to be present but accepts null or a string, while the declaration defaulting to None accepts all three inputs and uses None when note is omitted.
ASSESSMENT ANCHOR: distinguish_requiredness_from_nullability facts=['f1', 'f2']
ASSESSMENT ANCHOR: compare_omitted_null_and_concrete_inputs facts=['f2', 'f3']

## SOURCE FACTS — B (fastapi.openapi_generation)   objective: Generate OpenAPI from declarations: inspect one endpoint schema.
B.f1: FastAPI normally exposes the generated OpenAPI document at /openapi.json, describing the application's operations and data schemas.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/first-steps/#check-the-openapi-json]
B.f2: Typed body declarations and response models contribute input and output schemas to the generated API contract.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/body/#results, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/response-model/#response-model-parameter]
B.f3: Inspect the method entry under paths for an endpoint and follow its schema references into components to see the generated public input and output definitions.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/first-steps/#check-the-openapi-json]
note: Establish this first: Executable declarations drive generated contracts.
note: Stay within the current objective: Generate OpenAPI from declarations. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify generated input and output schemas.
PRACTICE ANCHOR (live_code): Inspect the supplied POST /orders contract, trace its request-body and response schema references, and assign the corresponding component definitions to OrderInput and OrderOutput.  SUCCESS: OrderInput refers to the component definition containing required integer quantity, and OrderOutput refers to the component definition containing required integer id. Both selections agree with the references under paths → /orders → post.
ASSESSMENT ANCHOR: locate_generated_openapi_document facts=['f1']
ASSESSMENT ANCHOR: identify_declaration_sources_for_input_and_output_schemas facts=['f2']
ASSESSMENT ANCHOR: trace_operation_references_to_input_and_output_definitions facts=['f3']

## DATA ASSETS USED
ds.orders: Synthetic order retrieval fixture — columns: id(identifier,digits-as-label), quantity(numerical)
   [42,2]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Consistent public error envelopes through exception handlers; Credential and sensitive-data redaction from emitted logs; Distinct create and partial-update contracts; FastAPI OpenAPI generation from typed route contracts; Graceful termination and shutdown verification; Header and cookie input binding; Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels; Keeping API schemas distinct from persistence entities; Meaningful contract examples and operation metadata; Proxy header trust; Redis cache-aside selection and population; Request correlation context across service logs; Request-scoped async-compatible PostgreSQL session lifecycle; Request-validation error behavior; Retrieve resource; Service health and readiness checks; Test dependency replacement; Transaction commit and rollback boundaries; 

## LESSON, in learner order

### s01 · explainer · Declare the boundary: Required, optional and default input semantics
Explainer — 
(mechanism) A default determines requiredness; a type that admits None determines nullability. These are different questions. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) A nullable field with no default still requires presence. field: Type | None = None allows both omission and explicit null. ⟦A.f2 A:tb3⟧
(mechanism) Send absence, explicit JSON null and a concrete value as separate requests. Compare each with the declared default and nullable type. ⟦A.f3 A:tb3⟧
[TABLE computed result ] caption: Declaration comparison derived from the presence rule and supplied request bodies, not an HTTP run. Read resulting_note only where accepted is true.
  produced by sql: WITH inputs(ordinal, supplied, note) AS (VALUES (1,FALSE,NULL),(2,TRUE,NULL),(3,TRUE,'Leave at reception')), declarations(label, has_default) AS (VALUES ('note: str | None', FALSE), ('note: str | None = None', TRUE))
SELECT CASE WHEN NOT supplied THEN 'omitted' WHEN note IS NULL THEN 'explicit null' ELSE 'concrete string' END AS input,
 label AS declaration, (supplied OR has_default) AS accepted,
 CASE WHEN supplied OR has_default THEN note ELSE NULL END AS resulting_note
FROM orders CROSS JOIN inputs CROSS JOIN declarations ORDER BY ordinal, has_default

### s02 · explainer · Trace the contract
Explainer — 
(mental_model) Keep two columns in your mental model: must the field appear, and may its value be null? note: str | None requires presence but admits null. Adding = None allows omission too. Test missing, null and a concrete string separately against those declarations; “optional” alone does not identify both rules. ⟦A.f1 A.f2 A.f3 A:tb4⟧

### s03 · explainer · Work through the supplied example
Explainer — 
(walkthrough) Start with the supplied nullable note declaration, then add its default. Send each supplied body separately before and after the change. Without a default, the field must appear even though null is allowed; with = None, omission is also allowed. Compare the declared presence rule with the admitted values instead of collapsing all three requests into one optional case. ⟦A.f1 A.f2 A.f3 A:tb5 A:tb6⟧

### s04 · check · Check the boundary: Required, optional and default input semantics
Check — Use the supplied order-service scenario to reason about this contract.

### s05 · hands_on · Apply the contract: Required, optional and default input semantics
Hands On — Complete the supplied workspace within its stated contract.

### s06 · explainer · Declare the boundary: FastAPI OpenAPI generation from typed route contracts
Explainer — 
(mechanism) FastAPI normally serves the generated OpenAPI document at /openapi.json. It describes operations and data schemas. ⟦B.f1 B:tb1 B:tb2⟧
(mechanism) Typed body declarations contribute input schemas; response models contribute output schemas to the generated public contract. ⟦B.f2 B:tb3⟧
(mechanism) Locate the endpoint’s method entry under paths, then follow its schema references into components to find the public input and output definitions. ⟦B.f3 B:tb3⟧
[CODE python]
import json
schema = {'paths': {'/orders': {'post': {'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/OrderInput'}}}},
                                'responses': {'200': {'description': 'Successful '
                                                                     'Response',
                                                      'content': {'application/json': {'schema': {'$ref': '#/components/schemas/OrderOutput'}}}}}}}},
 'components': {'schemas': {'OrderInput': {'type': 'object',
                                           'properties': {'quantity': {'type': 'integer'}},
                                           'required': ['quantity']},
                            'OrderOutput': {'type': 'object',
                                            'properties': {'id': {'type': 'integer'}},
                                            'required': ['id']}}}}
print(json.dumps(schema, indent=2))

  annotations: ['POST /orders: requestBody reference → components.schemas.OrderInput; response reference → OrderOutput. quantity is input, id is output.']

### s07 · explainer · Trace the contract
Explainer — 
(mental_model) Navigate by endpoint path and method first. Follow the body and response references into components, then compare their field definitions with the typed declarations. OpenAPI is generated from those declarations; it describes operations and schemas. Reading the document does not establish every runtime outcome, and schema details need not be inline in the operation entry. ⟦B.f1 B.f2 B.f3 B:tb4⟧

### s08 · explainer · Work through the supplied example
Explainer — 
(walkthrough) In the supplied POST /orders excerpt, follow the request-body reference to OrderInput and the response reference to OrderOutput. The input definition has quantity; the output definition has id. These are different public definitions contributed by the body and response-model declarations. Retrieve the generated document at /openapi.json and navigate through paths and components rather than assuming every field is inline. This is contract structure, not proof of every runtime result. ⟦B.f1 B.f2 B.f3 B:tb5 B:tb6⟧

### s09 · check · Check the boundary: FastAPI OpenAPI generation from typed route contracts
Check — Use the supplied order-service scenario to reason about this contract.

### s10 · hands_on · Apply the contract: FastAPI OpenAPI generation from typed route contracts
Hands On — Complete the supplied workspace within its stated contract.

### s11 · recap · Keep these distinctions
Recap — 
(takeaway) Defaults govern presence; nullable types govern null. Compare omitted, null and concrete inputs separately. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(takeaway) Locate /openapi.json; connect typed body and response declarations to schemas; follow path/method references into components. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧
[UP NEXT] Next: tile_049 — Trusted host validation: Start with Trusted host validation.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Required, optional and default input semantics
(definition) A default determines requiredness; a type that admits None determines nullability. These are different questions. ⟦A.f1 A:tb2 A:tb4 A:tb5 A:tb6⟧
(definition) A nullable field with no default still requires presence. field: Type | None = None allows both omission and explicit null. ⟦A.f2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(example) For the supplied note, admitting null differs from permitting omission; only the declaration with a default permits both. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r02 · Try the contrast: Required, optional and default input semantics
(definition) A nullable field with no default still requires presence. field: Type | None = None allows both omission and explicit null. ⟦A.f2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(definition) Send absence, explicit JSON null and a concrete value as separate requests. Compare each with the declared default and nullable type. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) For the supplied note bodies, omitted and explicit null are different requests. Without a default only the explicit null satisfies presence; adding = None permits omission too. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r03 · Try the contrast: FastAPI OpenAPI generation from typed route contracts
(definition) FastAPI normally serves the generated OpenAPI document at /openapi.json. It describes operations and data schemas. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(example) The order operation path differs from the document location: /openapi.json normally serves the generated description of operations and schemas. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
### r04 · Try the contrast: FastAPI OpenAPI generation from typed route contracts
(definition) Typed body declarations contribute input schemas; response models contribute output schemas to the generated public contract. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(definition) Locate the endpoint’s method entry under paths, then follow its schema references into components to find the public input and output definitions. ⟦B.f3 B:tb3 B:tb4 B:tb5 B:tb6⟧
(example) For POST /orders, a schema reference differs from the field definition it points to in components. ⟦B.f2 B.f3 B:tb3 B:tb4 B:tb5 B:tb6⟧

=========

# EVALUATOR PACKET — Trusted host validation (tile_049)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi_backend.trusted_host_validation — Trusted host validation

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (fastapi_backend.trusted_host_validation)   objective: Enforce accepted HTTP hosts: configure one deployment host allowlist.
A.f1: TrustedHostMiddleware validates the request Host against an allowed_hosts list and responds with 400 when the host is not allowed.   [sources: fastapi_docs_advanced#https://starlette.dev/middleware/#trustedhostmiddleware]
A.f2: Configure app.add_middleware(TrustedHostMiddleware, allowed_hosts=[...]) using domain names; *.example.com permits subdomains and ["*"] permits any host.   [sources: fastapi_docs_advanced#https://starlette.dev/middleware/#trustedhostmiddleware]
A.f3: www_redirect defaults to true and can redirect an allowed non-www host to its www counterpart, so account for it when verifying an allowlist's response.   [sources: fastapi_docs_advanced#https://starlette.dev/middleware/#trustedhostmiddleware]
note: Establish this first: A host allowlist validates the requested host identity independently of proxy metadata..
note: Stay within the current objective: Enforce accepted HTTP hosts. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify requests rejected by a host allowlist.
PRACTICE ANCHOR (live_code): Configure a deployment allowlist that accepts example.com and its subdomains, rejects unrelated hosts, and explicitly disables www redirection for predictable verification.  SUCCESS: The application registers TrustedHostMiddleware with allowed_hosts=["example.com", "*.example.com"] and www_redirect=False. Supplied checks confirm that intended hosts pass the host boundary and an unrelated host receives 400.
ASSESSMENT ANCHOR: identify_hosts_rejected_by_an_allowlist facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_exact_domain_subdomain_and_all_host_policies facts=['f2']
ASSESSMENT ANCHOR: distinguish_host_rejection_from_allowed_host_redirection facts=['f1', 'f3']

## DATA ASSETS USED
ds.host_checks: Authored host-policy comparison — columns: policy(categorical), allowed_hosts(text), www_redirect(categorical), Host(identifier), outcome(categorical), status(categorical,digits-as-label)
   ["deployment","example.com, *.example.com",false,"example.com","accepted",200]
   ["deployment","example.com, *.example.com",false,"www.example.com","accepted",200]
   ["deployment","example.com, *.example.com",false,"unrelated.example","rejected",400]
   ["exact","example.com",false,"www.example.com","rejected",400]
   ["subdomain wildcard","*.example.com",false,"example.com","rejected",400]
   ["all-host wildcard","*",false,"unrelated.example","accepted",200]
   ["www redirect","www.example.com",true,"example.com","redirected to www.example.com",null]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; Bounded resource listing with stable pagination and filtering; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Consistent public error envelopes through exception handlers; Credential and sensitive-data redaction from emitted logs; Distinct create and partial-update contracts; Graceful termination and shutdown verification; Header and cookie input binding; Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels; Keeping API schemas distinct from persistence entities; Meaningful contract examples and operation metadata; Proxy header trust; Redis cache-aside selection and population; Request correlation context across service logs; Request-scoped async-compatible PostgreSQL session lifecycle; Request-validation error behavior; Retrieve resource; Service health and readiness checks; Test dependency replacement; Transaction commit and rollback boun

## LESSON, in learner order

### s01 · explainer · Declare the boundary: Trusted host validation
Explainer — 
(mechanism) TrustedHostMiddleware checks Host against allowed_hosts. An unallowed host receives 400. ⟦A.f1 A:tb1 A:tb2 A:tb4⟧
(mechanism) Register TrustedHostMiddleware through app.add_middleware with domain names in allowed_hosts. *.example.com allows subdomains; ["*"] allows any host. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) www_redirect defaults to true and can redirect an allowed non-www host to its www counterpart. Account for redirects when checking the allowlist’s response. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.host_checks cols=['policy', 'allowed_hosts', 'www_redirect', 'Host', 'outcome', 'status'] ] caption: Authored host-policy comparison. Null redirect status means the glossary does not specify its code.

### s02 · check · Check the boundary: Trusted host validation
Check — Use the supplied order-service scenario to reason about this contract.

### s03 · hands_on · Apply the contract: Trusted host validation
Hands On — Complete the supplied workspace within its stated contract.

### s04 · recap · Keep these distinctions
Recap — 
(takeaway) Check Host against domain policies; distinguish rejection from www redirection; an all-host wildcard permits every host. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: tile_050 — Credential and sensitive-data redaction from emitted logs: Start with Credential and sensitive-data redaction from emitted logs.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Trusted host validation
(definition) TrustedHostMiddleware checks Host against allowed_hosts. An unallowed host receives 400. ⟦A.f1 A:tb2 A:tb4⟧
(definition) www_redirect defaults to true and can redirect an allowed non-www host to its www counterpart. Account for redirects when checking the allowlist’s response. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) For the supplied host policy, a rejected host differs from an allowed host redirected to its www counterpart. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast: Trusted host validation
(definition) TrustedHostMiddleware checks Host against allowed_hosts. An unallowed host receives 400. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Register TrustedHostMiddleware through app.add_middleware with domain names in allowed_hosts. *.example.com allows subdomains; ["*"] allows any host. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) www_redirect defaults to true and can redirect an allowed non-www host to its www counterpart. Account for redirects when checking the allowlist’s response. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) For the supplied host policy, a rejected host differs from an allowed host redirected to its www counterpart. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Credential and sensitive-data redaction from emitted logs (tile_050)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = observability.log_redaction — Credential and sensitive-data redaction from emitted logs

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (observability.log_redaction)   objective: Redact sensitive logs: verify one failure's redaction.
A.f1: Access tokens, passwords, primary secrets and sensitive personal data should usually not be recorded directly in logs; remove or mask them according to the logging policy.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#data-to-exclude]
A.f2: Review diagnostic context as well as the main log message, because connection strings, session identifiers and other sensitive values can appear in supplemental fields.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#data-to-exclude]
A.f3: Exercise a failure with recognizable synthetic sensitive values, inspect the emitted records and confirm that the redaction policy removes the prohibited values while retaining the intended event fields.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#verification]
note: Establish this first: Diagnostics must not become exposure channels.
note: Stay within the current objective: Redact sensitive logs. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify diagnostic credentials.
PRACTICE ANCHOR (live_code): Exercise one supplied failure with a recognizable fake token and fake connection-string secret, then verify redaction across the complete emitted record.  SUCCESS: Neither prohibited synthetic value appears in the emitted message or supplemental context, and the intended event field remains intact.
ASSESSMENT ANCHOR: identify_sensitive_values_in_diagnostic_records facts=['f1', 'f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; Bounded resource listing with stable pagination and filtering; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Consistent public error envelopes through exception handlers; Distinct create and partial-update contracts; Graceful termination and shutdown verification; Header and cookie input binding; Injection-resistant database and input handling; Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels; Keeping API schemas distinct from persistence entities; Meaningful contract examples and operation metadata; Proxy header trust; Redis cache-aside selection and population; Request correlation context across service logs; Request-scoped async-compatible PostgreSQL session lifecycle; Request-validation error behavior; Retrieve resource; Service health and readiness checks; Test dependency replacement; Transaction commit and rollback boundaries; Tr

## LESSON, in learner order

### s01 · explainer · Declare the boundary: Credential and sensitive-data redaction from emitted logs
Explainer — 
(mechanism) Access tokens, passwords, primary secrets and sensitive personal data should usually not appear directly in logs. Remove or mask them under the logging policy. ⟦A.f1 A:tb1 A:tb2 A:tb4⟧
(mechanism) Inspect supplemental context as well as the message: connection strings, session identifiers and other sensitive values can appear there. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Trigger a failure with recognizable synthetic sensitive values. Inspect emitted records to confirm prohibited values are removed while intended event fields remain. ⟦A.f3 A:tb3 A:tb4⟧
[BEFORE_AFTER] Before: the same synthetic failure with masking disabled. After: policy masks prohibited strings throughout message and context while retaining the event field. Output is computed from this fixture.
  before:
[CODE python]
import io
import logging
class RedactingFormatter(logging.Formatter):
    def __init__(self, secrets):
        super().__init__('%(message)s context=%(context)s event=%(event)s')
        self.secrets = secrets
    def format(self, record):
        text = super().format(record)
        for secret in self.secrets:
            text = text
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
    text = output.getvalue()
    message, tail = text.rstrip('\n').split(' context=', 1)
    context, event = tail.rsplit(' event=', 1)
    return {'text': text, 'fields': {'event': event, 'context': context}}

result = failure_harness(token='FAKE_ORDER_TOKEN_ABC', connection_string='FAKE_CONNECTION_SECRET_XYZ')
print(result['text'], end='')

  annotations: []
  after:
[CODE python]
import io
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
    text = output.getvalue()
    message, tail = text.rstrip('\n').split(' context=', 1)
    context, event = tail.rsplit(' event=', 1)
    return {'text': text, 'fields': {'event': event, 'context': context}}

result = failure_harness(token='FAKE_ORDER_TOKEN_ABC', connection_string='FAKE_CONNECTION_SECRET_XYZ')
print(result['text'], end='')

  annotations: []

### s02 · check · Check the boundary: Credential and sensitive-data redaction from emitted logs
Check — Use the supplied order-service scenario to reason about this contract.

### s03 · hands_on · Apply the contract: Credential and sensitive-data redaction from emitted logs
Hands On — Complete the supplied workspace within its stated contract.

### s04 · recap · Keep these distinctions
Recap — 
(takeaway) Apply logging policy to sensitive values in both message and context; verify emitted records with synthetic failures while retaining intended fields. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: tile_051 — Request-scoped async-compatible PostgreSQL session lifecycle: Start with Request-scoped async-compatible PostgreSQL session lifecycle.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Credential and sensitive-data redaction from emitted logs
(definition) Access tokens, passwords, primary secrets and sensitive personal data should usually not appear directly in logs. Remove or mask them under the logging policy. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Inspect supplemental context as well as the message: connection strings, session identifiers and other sensitive values can appear there. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(example) For the synthetic order failure, a safe main message can still have prohibited values in supplemental context. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Request-scoped async-compatible PostgreSQL session lifecycle (tile_051)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = sqlalchemy.async_session_lifecycle — Request-scoped async-compatible PostgreSQL session lifecycle

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (sqlalchemy.async_session_lifecycle)   objective: Own an async-compatible database session for a request: supply and close one async-compatible session per request.
A.f1: AsyncSession maintains mutable state for current database work and is not safe to share across concurrent tasks; use a separate session for each concurrent unit of work.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#using-asyncsession-with-concurrent-tasks]
A.f2: Build an async_sessionmaker bound to an async engine and use async with session_factory() as session to obtain and close a session for the request's unit of work.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-orm]
A.f3: A request dependency can yield a session from its async context, leaving session cleanup to that context on both normal and exceptional exit.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-orm, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#a-dependency-with-yield-and-try]
note: Establish this first: A mutable database session belongs to one request unit of work, not concurrent application-wide users..
note: Stay within the current objective: Own an async-compatible database session for a request. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify leaked sessions or unsafe sharing across concurrent requests.
PRACTICE ANCHOR (live_code): Using a supplied async engine, build a session_factory and implement an async request dependency that yields one session from an async context.  SUCCESS: Separate concurrent request dependency invocations receive distinct sessions, and each session's context closes on both normal and exceptional exit.
ASSESSMENT ANCHOR: identify_unsafe_session_sharing_across_concurrent_requests facts=['f1']
ASSESSMENT ANCHOR: identify_session_leaks_from_missing_context_owned_cleanup facts=['f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; Bounded resource listing with stable pagination and filtering; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Consistent public error envelopes through exception handlers; Create resource; Distinct create and partial-update contracts; Graceful termination and shutdown verification; Header and cookie input binding; Injection-resistant database and input handling; Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels; Keeping API schemas distinct from persistence entities; Meaningful contract examples and operation metadata; Proxy header trust; Redis cache-aside selection and population; Request correlation context across service logs; Request-validation error behavior; Retrieve resource; Service health and readiness checks; Test dependency replacement; Transaction commit and rollback boundaries; Translating domain and persistence failures at 

## LESSON, in learner order

### s01 · explainer · Declare the boundary: Request-scoped async-compatible PostgreSQL session lifecycle
Explainer — 
(mechanism) AsyncSession holds mutable state for database work. It is unsafe to share across concurrent tasks; give each concurrent unit of work a separate session. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) Bind async_sessionmaker to an async engine. async with session_factory() as session obtains and closes a session for the request’s unit of work. ⟦A.f2 A:tb3⟧
(mechanism) A request dependency can yield the session from that async context. The context still owns cleanup on normal and exceptional exit. ⟦A.f3 A:tb3⟧
[DIAGRAM: One factory, separate concurrent sessions] nodes=['async_sessionmaker(async engine)', 'Session A: mutable work state', 'Session B: mutable work state', 'Dependency yields session A', 'Dependency yields session B', 'async context exit closes A', 'async context exit closes B'] edges=[('factory', 'sa', 'async with session_factory()'), ('factory', 'sb', 'async with session_factory()'), ('sa', 'ya', 'operation use'), ('sb', 'yb', 'operation use'), ('ya', 'ca', 'normal or exceptional exit'), ('yb', 'cb', 'normal or exceptional exit')] alt: One factory, separate concurrent sessions: async_sessionmaker(async engine); Session A: mutable work state; Session B: mutable work state; Dependency yields session A; Dependency yields session B; async context exit closes A; async context exit closes B

### s02 · explainer · Trace the contract
Explainer — 
(mental_model) Separate the engine-bound factory from the mutable sessions it creates. Concurrent request A and request B need separate sessions. Each request’s async context owns closure, including exceptional exit. Yield supplies the session to the operation without transferring that cleanup responsibility. A shared factory is not a shared AsyncSession. ⟦A.f1 A.f2 A.f3 A:tb4⟧

### s03 · explainer · Work through the supplied example
Explainer — 
(walkthrough) Bind the factory to the async engine, then open a session with async with for each request’s work. Yield that session from inside the context so both normal and exceptional exit close it. Draw session A and session B separately for concurrent requests. Sharing factory setup does not permit both tasks to borrow one mutable session, and cleanup must not depend only on a successful return. ⟦A.f1 A.f2 A.f3 A:tb5 A:tb6⟧

### s04 · video · Optional deeper walkthrough
Video — 
[VIDEO ] bridge-before:  | bridge-after: 

### s05 · check · Check the boundary: Request-scoped async-compatible PostgreSQL session lifecycle
Check — Use the supplied order-service scenario to reason about this contract.

### s06 · hands_on · Apply the contract: Request-scoped async-compatible PostgreSQL session lifecycle
Hands On — Complete the supplied workspace within its stated contract.

### s07 · recap · Keep these distinctions
Recap — 
(takeaway) Share factory setup, not mutable sessions across concurrent tasks. Obtain sessions with async contexts and yield without losing normal or exceptional cleanup. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
[UP NEXT] Next: tile_052 — Graceful termination and shutdown verification: Start with Graceful termination and shutdown verification.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Request-scoped async-compatible PostgreSQL session lifecycle
(definition) Bind async_sessionmaker to an async engine. async with session_factory() as session obtains and closes a session for the request’s unit of work. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) A request dependency can yield the session from that async context. The context still owns cleanup on normal and exceptional exit. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) For the order request, obtaining a session is not the whole ownership boundary: yield stays inside async with so context exit closes it even on failure. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast: Request-scoped async-compatible PostgreSQL session lifecycle
(definition) AsyncSession holds mutable state for database work. It is unsafe to share across concurrent tasks; give each concurrent unit of work a separate session. ⟦A.f1 A:tb2 A:tb4 A:tb5 A:tb6⟧
(example) Concurrent request A and request B need separate mutable sessions rather than concurrent use of one AsyncSession. ⟦A.f1 A:tb2 A:tb4 A:tb5 A:tb6⟧

=========

# EVALUATOR PACKET — Graceful termination and shutdown verification · Service health and readiness checks (tile_052)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = deployment.graceful_shutdown_verification — Graceful termination and shutdown verification
B = deployment.health_readiness — Service health and readiness checks

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (deployment.graceful_shutdown_verification)   objective: Verify graceful shutdown: verify termination during one request.
A.f1: Graceful server termination stops old processes accepting new connections and permits active responses and background tasks to finish within configured time limits.   [sources: fastapi_docs_tutorial#https://uvicorn.dev/server-behavior/#graceful-process-shutdown]
A.f2: Configure --timeout-graceful-shutdown seconds as the maximum wait before Uvicorn starts terminating remaining requests.   [sources: fastapi_docs_tutorial#https://uvicorn.dev/settings/#timeouts]
A.f3: Verify termination during an active request by observing whether its response completes within the limit and whether lifespan cleanup releases the application's shared resources.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/events/#lifespan-function, fastapi_docs_tutorial#https://uvicorn.dev/server-behavior/#graceful-process-shutdown]
note: Establish this first: Termination stops new work and permits bounded cleanup.
note: Stay within the current objective: Verify graceful shutdown. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify interrupted work and leaked resources.
PRACTICE ANCHOR (live_code): Configure Uvicorn's graceful-shutdown wait for the supplied order application, ensure its lifespan cleanup closes the shared HTTP client, and initiate termination while one controlled order request is active.  SUCCESS: Record the configured limit, confirm that termination began during the request, observe whether the response completed within that limit, and verify that lifespan cleanup closed the shared HTTP client. Distinguish interrupted work from an unreleased resource.
ASSESSMENT ANCHOR: identify_interrupted_work_against_shutdown_limit facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: identify_shared_resources_not_released_by_lifespan_cleanup facts=['f3']

## SOURCE FACTS — B (deployment.health_readiness)   objective: Design health probe contracts: specify one service's probes.
B.f1: A failed liveness probe can cause a container restart, whereas a failed readiness probe removes its eligibility to receive service traffic without requiring a restart.   [sources: fastapi_docs_tutorial#https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/]
B.f2: Readiness can depend on temporary conditions such as required backend availability, even while the process is alive.   [sources: fastapi_docs_tutorial#https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-readiness-probes]
B.f3: Configure separate livenessProbe and readinessProbe HTTP checks with path, port, periodSeconds and failureThreshold that match the service's intended restart and traffic-eligibility contracts.   [sources: fastapi_docs_tutorial#https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-a-liveness-http-request, fastapi_docs_tutorial#https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-readiness-probes]
B.f4: An HTTP probe regards response status codes from 200 through 399 as success; other codes are failure.   [sources: fastapi_docs_tutorial#https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-a-liveness-http-request]
note: Establish this first: Probe contracts distinguish survival from traffic eligibility.
note: Stay within the current objective: Design health probe contracts. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine whether failure restarts or removes traffic.
PRACTICE ANCHOR (live_code): Specify separate livenessProbe and readinessProbe HTTP checks for one service using supplied endpoint paths, port, check periods and failure thresholds. Keep temporary required-backend unavailability in the readiness contract rather than treating it as a reason to restart an otherwise live process.  SUCCESS: Both probe mappings contain the intended HTTP path and port, periodSeconds and failureThreshold. The liveness contract permits restart after its failure threshold; the readiness contract removes traffic eligibility after its failure threshold without requiring restart. Endpoint response contracts classify 200 through 399 as success and other codes as failure.
ASSESSMENT ANCHOR: distinguish_restart_from_traffic_removal facts=['f1', 'f2']
ASSESSMENT ANCHOR: determine_probe_outcomes_from_http_status_and_failure_threshold facts=['f1', 'f3', 'f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; Bounded resource listing with stable pagination and filtering; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Consistent public error envelopes through exception handlers; Create resource; Delete resource; Distinct create and partial-update contracts; Header and cookie input binding; Injection-resistant database and input handling; Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels; Keeping API schemas distinct from persistence entities; Meaningful contract examples and operation metadata; Proxy header trust; Redis cache-aside selection and population; Request correlation context across service logs; Request-validation error behavior; Retrieve resource; Service health and readiness checks; Test dependency replacement; Transaction commit and rollback boundaries; Translating domain and persistence failures at the API boundary; Update resour

## LESSON, in learner order

### s01 · explainer · Declare the boundary: Graceful termination and shutdown verification
Explainer — 
(mechanism) Graceful termination stops old processes accepting new connections and lets active responses and background tasks finish within configured limits. ⟦A.f1 A:tb1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Set --timeout-graceful-shutdown seconds as Uvicorn’s maximum wait before it starts terminating remaining requests. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Terminate during an active request. Observe whether its response completes within the limit and whether lifespan cleanup releases shared application resources. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[PROCESS_FLOW: Bounded shutdown and evidence to inspect] nodes=['Controlled order request active', 'Initiate termination', 'Old processes stop accepting new connections', 'Responses and background tasks may finish; maximum wait 5 seconds', 'Wait limit reached: Uvicorn starts terminating remaining requests', 'Lifespan cleanup releases shared client', 'Inspect recorded response outcome and client.is_closed'] edges=[('active', 'terminate', None), ('terminate', 'stop', None), ('stop', 'wait', None), ('wait', 'limit', 'remaining work at boundary'), ('wait', 'cleanup', 'finish within limit'), ('limit', 'cleanup', None), ('cleanup', 'evidence', 'verify, do not assume')] alt: Bounded shutdown and evidence to inspect: Controlled order request active; Initiate termination; Old processes stop accepting new connections; Responses and background tasks may finish; maximum wait 5 seconds; Wait limit reached: Uvicorn starts terminating remaining requests; Lifespan cleanup releases shared client; Inspect recorded response outcome and client.is_closed

### s02 · check · Check the boundary: Graceful termination and shutdown verification
Check — Use the supplied order-service scenario to reason about this contract.

### s03 · hands_on · Apply the contract: Graceful termination and shutdown verification
Hands On — Complete the supplied workspace within its stated contract.

### s04 · explainer · Declare the boundary: Service health and readiness checks
Explainer — 
(mechanism) Failed liveness can cause a container restart. Failed readiness removes service-traffic eligibility without requiring restart. ⟦B.f1 B:tb1 B:tb2⟧
(mechanism) Readiness can reflect temporary required-backend unavailability even when the process remains alive. ⟦B.f2 B:tb3⟧
(mechanism) Configure separate livenessProbe and readinessProbe HTTP checks with path, port, periodSeconds and failureThreshold matching the intended restart and traffic contracts. ⟦B.f3 B:tb3⟧
(mechanism) HTTP probes count statuses 200 through 399 as success; other statuses are failure. ⟦B.f4 B:tb3⟧
[PROCESS_FLOW: Separate restart and traffic decisions] nodes=['Temporary required-backend outage; process alive', 'livenessProbe: /live:8000, periodSeconds=10, failureThreshold=3', 'readinessProbe: /ready:8000, periodSeconds=5, failureThreshold=2', 'HTTP 200–399 success; other statuses failure', 'Liveness failures reach threshold', 'Readiness failures reach threshold', 'Can cause container restart', 'Remove service-traffic eligibility; no restart required'] edges=[('outage', 'live', 'can remain successful'), ('outage', 'ready', 'can fail'), ('live', 'status', 'classify response'), ('ready', 'status', 'classify response'), ('status', 'lf', 'liveness failure'), ('status', 'rf', 'readiness failure'), ('lf', 'restart', None), ('rf', 'traffic', None)] alt: Separate restart and traffic decisions: Temporary required-backend outage; process alive; livenessProbe: /live:8000, periodSeconds=10, failureThreshold=3; readinessProbe: /ready:8000, periodSeconds=5, failureThreshold=2; HTTP 200–399 success; other statuses failure; Liveness failures reach threshold; Readiness failures reach threshold; Can cause container restart; Remove service-traffic eligibility; no restart required

### s05 · explainer · Trace the contract
Explainer — 
(mental_model) Configure each probe’s path, port, periodSeconds and failureThreshold for its own contract. A temporary required-backend outage can leave liveness successful while readiness removes traffic eligibility. Failed liveness can cause restart; failed readiness does not require it. Classify HTTP statuses 200 through 399 as success, including 3xx. An “unready” response body is insufficient if the status still counts as successful. ⟦B.f1 B.f2 B.f3 B.f4 B:tb4 B:tb5⟧

### s06 · check · Check the boundary: Service health and readiness checks
Check — Use the supplied order-service scenario to reason about this contract.

### s07 · hands_on · Apply the contract: Service health and readiness checks
Hands On — Complete the supplied workspace within its stated contract.

### s08 · recap · Keep these distinctions
Recap — 
(takeaway) Bound shutdown waiting, terminate during active work, and verify response completion plus shared-resource cleanup. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Separate liveness restart and readiness traffic contracts; temporary backend outages can affect readiness while alive; HTTP 200–399 counts as probe success. ⟦B.f1 B.f2 B.f3 B.f4 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Next: tile_054 — Meaningful contract examples and operation metadata: Start with Meaningful contract examples and operation metadata.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Graceful termination and shutdown verification
(definition) Terminate during an active request. Observe whether its response completes within the limit and whether lifespan cleanup releases shared application resources. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) For the delayed order request, response completion does not by itself establish that the shared client was closed. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast: Graceful termination and shutdown verification
(definition) Graceful termination stops old processes accepting new connections and lets active responses and background tasks finish within configured limits. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Set --timeout-graceful-shutdown seconds as Uvicorn’s maximum wait before it starts terminating remaining requests. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Terminate during an active request. Observe whether its response completes within the limit and whether lifespan cleanup releases shared application resources. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) For the delayed order request, response completion does not by itself establish that the shared client was closed. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Try the contrast: Service health and readiness checks
(definition) Failed liveness can cause a container restart. Failed readiness removes service-traffic eligibility without requiring restart. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(definition) Configure separate livenessProbe and readinessProbe HTTP checks with path, port, periodSeconds and failureThreshold matching the intended restart and traffic contracts. ⟦B.f3 B:tb3 B:tb4⟧
(definition) HTTP probes count statuses 200 through 399 as success; other statuses are failure. ⟦B.f4 B:tb3 B:tb4 B:tb5⟧
(example) For the supplied HTTP probe contract, an unready body with a successful status still counts as probe success. Failure thresholds belong to separate restart and traffic-eligibility decisions. ⟦B.f1 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r04 · Try the contrast: Service health and readiness checks
(definition) Failed liveness can cause a container restart. Failed readiness removes service-traffic eligibility without requiring restart. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(definition) Readiness can reflect temporary required-backend unavailability even when the process remains alive. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(definition) Configure separate livenessProbe and readinessProbe HTTP checks with path, port, periodSeconds and failureThreshold matching the intended restart and traffic contracts. ⟦B.f3 B:tb3 B:tb4⟧
(definition) HTTP probes count statuses 200 through 399 as success; other statuses are failure. ⟦B.f4 B:tb3 B:tb4 B:tb5⟧
(example) During the supplied backend outage, an alive process can be unready; removing traffic differs from restarting it. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧