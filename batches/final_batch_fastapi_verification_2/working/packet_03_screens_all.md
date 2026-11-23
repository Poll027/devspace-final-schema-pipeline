# EVALUATOR PACKET — Meaningful contract examples and operation metadata (tile_054)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.contract_examples_metadata — Meaningful contract examples and operation metadata

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (fastapi.contract_examples_metadata)   objective: Make operation documentation actionable: add realistic examples and operation metadata to one route.
A.f1: Set model_config = ConfigDict(json_schema_extra={"examples": [...]}) on a model to provide schema examples, or use Field(examples=[...]) for field-level examples.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/schema-extra-example/#extra-json-schema-data-in-pydantic-models]
A.f2: Supply Body(openapi_examples={...}) for named request-body examples in the operation documentation.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/schema-extra-example/#using-the-openapi-examples-parameter]
A.f3: Use tags, summary and description on a path operation decorator to describe and group the operation without changing its runtime behavior.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#summary-and-description]
A.f4: Validate proposed examples with Model.model_validate(example) before including them so their content agrees with the executable model.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/schema-extra-example/#extra-json-schema-data-in-pydantic-models, pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/models/#validating-data]
note: Establish this first: Documentation metadata clarifies the executable contract rather than implying another one.
note: Stay within the current objective: Make operation documentation actionable. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Select schema-valid examples and metadata communicating one actual operation contract.
PRACTICE ANCHOR (live_code): Add a realistic synthetic quantity example and operation metadata to one existing order route. Validate the sample, add model-level or field-level schema examples, and configure a named request-body example plus tags, summary and description without changing the handler's behavior.  SUCCESS: The quantity-2 sample passes OrderInput.model_validate. Schema metadata and the named body example use that validated sample. The route's tags, summary and description accurately describe its existing behavior, and its handler and quantity constraint remain unchanged.
ASSESSMENT ANCHOR: select_model_valid_schema_examples facts=['f1', 'f4']
ASSESSMENT ANCHOR: select_valid_named_request_body_examples facts=['f2', 'f4']
ASSESSMENT ANCHOR: select_metadata_matching_the_actual_operation_contract facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; Bounded resource listing with stable pagination and filtering; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Consistent public error envelopes through exception handlers; Create resource; Delete resource; Distinct create and partial-update contracts; Header and cookie input binding; Injection-resistant database and input handling; Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels; JWT signature, issuer, audience and expiry verification; Keeping API schemas distinct from persistence entities; Proxy header trust; Redis cache-aside selection and population; Request correlation context across service logs; Request-validation error behavior; Retrieve resource; Test dependency replacement; Transaction commit and rollback boundaries; Translating domain and persistence failures at the API boundary; Update resource; Webhook request contracts and

## LESSON, in learner order

### s01 · explainer · Examples that match the contract
(mechanism) Use model_config = ConfigDict(json_schema_extra={"examples": [...]}) for model schema examples, or Field(examples=[...]) for field examples. Validate each proposed sample with Model.model_validate(example) before publishing it. ⟦A.f1 A.f4 A:tb1 A:tb2 A:tb3⟧
(mechanism) Body(openapi_examples={...}) supplies named request-body examples. Decorator tags, summary and description group and describe the operation; they do not change runtime behavior. ⟦A.f2 A.f3 A:tb3⟧
[CODE python]
from typing import Annotated
from fastapi import FastAPI, Body
from pydantic import BaseModel, ConfigDict, Field

example = {"quantity": 2}

class OrderInput(BaseModel):
    quantity: int = Field(gt=0)
    model_config = ConfigDict(json_schema_extra={"examples": [example]})

OrderInput.model_validate(example)
app = FastAPI()

@app.post("/orders", tags=["orders"], summary="Validate an order",
          description="Return the validated order input without persistence.")
def create_order(order: Annotated[OrderInput, Body(openapi_examples={
    "positive_quantity": {"summary": "Positive quantity", "description": "Synthetic order input.", "value": example}
})]):
    return order

  annotations: []

### s02 · explainer · Documentation is not a constraint override
(mechanism) A documentation sample must satisfy the executable model. Validate the synthetic order sample before putting it in schema examples or named body examples. Review the quantity bound, not just whether the payload looks plausible. ⟦A.f1 A.f2 A.f4 A:tb4⟧
(mechanism) A summary can explain the operation, but cannot loosen its constraint. Ask whether the documentation illustrates the declared contract or implies a different one. ⟦A.f3 A:tb4⟧

### s03 · explainer · Review the synthetic order example
(mechanism) The registered OrderInput declares a positive quantity. Its synthetic example supplies 2. OrderInput.model_validate(example) checks that sample before publication; ConfigDict places it in model-level schema examples. Field(examples=[...]) is the field-level alternative. ⟦A.f1 A.f4 A:tb5⟧
(mechanism) Use the same validated sample in Body(openapi_examples={...}) for a named body example. The POST /orders metadata describes returning validated input without persistence. Tags, summary and description do not change that behavior or make an invalid example valid. ⟦A.f2 A.f3 A.f4 A:tb5 A:tb6⟧

### s04 · check · Choose accurate operation metadata

### s05 · hands_on · Publish a validated order example

### s06 · recap · Keep these distinctions
(takeaway) Schema examples use ConfigDict/json_schema_extra or Field(examples=[...]); validate the sample with model_validate before publishing. ⟦A.f1 A.f4 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(takeaway) Body(openapi_examples={...}) supplies named body examples. Tags, summary and description describe the operation without changing runtime behavior. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5 A:tb6⟧
[UP NEXT] Test dependency replacement: An endpoint test needs a controlled provider result. Substitute at the declared dependency boundary and exercise its use through HTTP.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Choose accurate operation metadata
(mental_model) Compare the validated synthetic order example with metadata that would imply another contract. Documentation illustrates acceptance; it does not redefine it. ⟦A.f3 A:tb3 A:tb4 A:tb5 A:tb6⟧
(definition) Decorator tags, summary and description group and describe the operation without changing its runtime behavior. ⟦A.f3 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r02 · Revisit: Publish a validated order example
(mental_model) Compare the validated synthetic order example with metadata that would imply another contract. Documentation illustrates acceptance; it does not redefine it. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(definition) Model-level schema examples use model_config = ConfigDict(json_schema_extra={"examples": [...]}). Field(examples=[...]) is the field-level alternative. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Use Body(openapi_examples={...}) for named request-body examples in operation documentation. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Decorator tags, summary and description group and describe the operation without changing its runtime behavior. ⟦A.f3 A:tb3 A:tb4 A:tb5 A:tb6⟧
(definition) Validate proposed samples with Model.model_validate(example) before publication so they agree with the executable model. ⟦A.f4 A:tb3 A:tb4 A:tb5 A:tb6⟧

=========

# EVALUATOR PACKET — Test dependency replacement (tile_055)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.dependency_overrides — Test dependency replacement

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (fastapi.dependency_overrides)   objective: Replace dependencies for isolated tests: override and restore one provider in an endpoint test.
A.f1: app.dependency_overrides maps an original provider callable to a replacement callable that FastAPI uses when resolving that dependency in a test.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/testing-dependencies/#use-the-app-dependency-overrides-attribute]
A.f2: Assign app.dependency_overrides[original] = replacement, send the test request and assert the replacement's observable behavior.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/testing-dependencies/#use-the-app-dependency-overrides-attribute]
A.f3: Restore overrides after the test, such as by resetting app.dependency_overrides to an empty dictionary when no previous overrides existed, to avoid substitutions leaking into other tests.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/testing-dependencies/#use-the-app-dependency-overrides-attribute]
note: Establish this first: A test substitutes a dependency at its declared boundary.
note: Stay within the current objective: Replace dependencies for isolated tests. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine which provider runs under an override.
PRACTICE ANCHOR (live_code): Override one string-returning provider in an endpoint test, assert its synthetic value in the endpoint response, and restore the original override state.  SUCCESS: The test request returns the replacement provider’s value, an assertion verifies that value, and cleanup restores the initially empty override dictionary even if the assertion fails.
ASSESSMENT ANCHOR: determine_provider_used_under_override facts=['f1']
ASSESSMENT ANCHOR: determine_provider_used_after_override_restoration facts=['f1', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; Bounded resource listing with stable pagination and filtering; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Consistent public error envelopes through exception handlers; Create resource; Delete resource; Distinct create and partial-update contracts; Freshness policy; Header and cookie input binding; Injection-resistant database and input handling; Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels; JWT signature, issuer, audience and expiry verification; Keeping API schemas distinct from persistence entities; Proxy header trust; Redis cache-aside selection and population; Request correlation context across service logs; Request-validation error behavior; Retrieve resource; Transaction commit and rollback boundaries; Translating domain and persistence failures at the API boundary; Update resource; Webhook request contracts and acknowledg

## LESSON, in learner order

### s01 · explainer · Substitute at the dependency boundary
(mechanism) An isolated endpoint test substitutes at the declared dependency boundary. app.dependency_overrides maps the original provider callable to a replacement callable. FastAPI uses that replacement when resolving the dependency; the mapping is not keyed by a provider name or returned value. ⟦A.f1 A:tb1 A:tb2 A:tb4⟧
(mechanism) Assign app.dependency_overrides[original] = replacement, send the HTTP request, then assert the replacement is observable in the response. In this synthetic fixture, original returns 'actual user' and replacement returns 'mock user'; the handler exposes the selected value under user. ⟦A.f1 A.f2 A:tb3 A:tb4⟧
(mechanism) Save and restore the previous override state in try/finally. Reset to an empty dictionary only when there were no previous overrides. An active replacement can leak into later tests; restoration is not automatic. Trace setup, request, assertion and cleanup together. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[CODE python]
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

app = FastAPI()

def original():
    return "actual user"

@app.get("/")
def hello(user: str = Depends(original)):
    return {"user": user}

def replacement():
    return "mock user"

from main import app, original, replacement
from fastapi.testclient import TestClient

def test_override():
    previous = app.dependency_overrides.copy()
    app.dependency_overrides[original] = replacement
    try:
        with TestClient(app) as client:
            response = client.get("/")
            assert response.json()["user"] == replacement()
    finally:
        app.dependency_overrides = previous

  annotations: []

### s02 · video · Trace provider substitution
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Follow the active provider mapping

### s04 · check · Follow the restored provider mapping

### s05 · hands_on · Override, request, assert, restore

### s06 · recap · Keep these distinctions
(takeaway) Map original callable to replacement callable, send the test request and assert the replacement is observable. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4⟧
(takeaway) Restore the earlier override state afterward. An empty dictionary is appropriate only when the earlier state was empty. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Header and cookie input binding: A handler needs a header and a cookie. Explicit source markers keep these metadata inputs from becoming ordinary query parameters.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Follow the active provider mapping
(mental_model) In the same fixture, distinguish an active original-to-replacement mapping from the restored mapping. Follow the callable selected for the request, not the name of the test. ⟦A.f1 A:tb2 A:tb4⟧
(definition) app.dependency_overrides maps the original provider callable to a replacement callable; FastAPI uses the replacement to resolve that dependency. ⟦A.f1 A:tb2 A:tb4⟧
### r02 · Revisit: Follow the restored provider mapping
(mental_model) In the same fixture, distinguish an active original-to-replacement mapping from the restored mapping. Follow the callable selected for the request, not the name of the test. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(definition) app.dependency_overrides maps the original provider callable to a replacement callable; FastAPI uses the replacement to resolve that dependency. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Restore the earlier overrides after the test to prevent leakage. Reset to an empty dictionary only if no prior overrides existed. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r03 · Revisit: Override, request, assert, restore
(mental_model) In the same fixture, distinguish an active original-to-replacement mapping from the restored mapping. Follow the callable selected for the request, not the name of the test. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(definition) app.dependency_overrides maps the original provider callable to a replacement callable; FastAPI uses the replacement to resolve that dependency. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Assign app.dependency_overrides[original] = replacement, send the test request, and assert the replacement’s observable behavior. ⟦A.f2 A:tb3 A:tb4⟧
(definition) Restore the earlier overrides after the test to prevent leakage. Reset to an empty dictionary only if no prior overrides existed. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Bind and validate request metadata (tile_056)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.header_cookie_binding — Header and cookie input binding
B = fastapi.request_validation_errors — Request-validation error behavior

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (fastapi.header_cookie_binding)   objective: Extract request metadata: declare one endpoint's metadata inputs.
A.f1: Declare a request header with Annotated[Type, Header()] so the value is read from headers rather than interpreted as a query parameter.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/header-params/#declare-header-parameters]
A.f2: Header converts underscores in Python parameter names to hyphens by default, and header names are case-insensitive; use alias or convert_underscores=False to control the name mapping.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/header-params/#automatic-conversion]
A.f3: Declare Annotated[Type, Cookie()] to bind a cookie by name, using a default when its omission should be accepted.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/cookie-params/#declare-cookie-parameters]
note: Establish this first: Metadata binds through named request sources.
note: Stay within the current objective: Extract request metadata. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine header and cookie binding sources.
PRACTICE ANCHOR (live_code): Declare one endpoint's metadata inputs: bind user_agent to a request header and a cookie input by name, accepting omission of the cookie.  SUCCESS: The endpoint uses Annotated with Header() for user_agent and Cookie() for the cookie input. user_agent maps to user-agent regardless of header-name case, and the cookie has a default of None.
ASSESSMENT ANCHOR: determine_header_and_cookie_binding_sources facts=['f1', 'f3']
ASSESSMENT ANCHOR: resolve_header_name_mapping facts=['f2']
ASSESSMENT ANCHOR: determine_cookie_omission_behavior facts=['f3']

## SOURCE FACTS — B (fastapi.request_validation_errors)   objective: Interpret input validation errors: assert one invalid-input response.
B.f1: FastAPI raises RequestValidationError for invalid request data and handles it before normal operation logic receives that input.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/handling-errors/#override-request-validation-exceptions]
B.f2: Assert the default invalid-input response status of 422 and inspect the JSON detail entries to identify the failed input location and error type.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/path-params/#data-validation, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/handling-errors/#override-request-validation-exceptions]
B.f3: Invalid request input is distinct from a model-validation failure in response or application code, which indicates a server-side bug rather than a client's invalid request.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/handling-errors/#override-request-validation-exceptions]
note: Establish this first: Invalid inputs are rejected before handler logic.
note: Stay within the current objective: Interpret input validation errors. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Locate rejected input and outcome.
PRACTICE ANCHOR (live_code): Assert one invalid-input response from the supplied order endpoint, including its default status and the rejected input's location and error type.  SUCCESS: The test sends the supplied invalid order input, asserts status 422, and verifies the expected location and error type in a JSON detail entry.
ASSESSMENT ANCHOR: locate_rejected_request_input_and_default_outcome facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_invalid_request_input_from_server_side_validation_failure facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; Bounded resource listing with stable pagination and filtering; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Consistent public error envelopes through exception handlers; Create resource; Delete resource; Distinct create and partial-update contracts; Freshness policy; Injection-resistant database and input handling; Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels; JWT signature, issuer, audience and expiry verification; Keeping API schemas distinct from persistence entities; Proxy header trust; Redis cache-aside selection and population; Request correlation context across service logs; Request-validation error behavior; Retrieve resource; Safe failure policy; Service release and rollback workflow with build, release and run separation; Transaction commit and rollback boundaries; Translating domain and persistence failures at the API b

## LESSON, in learner order

### s01 · explainer · Choose the metadata source explicitly
(mechanism) Bind a header explicitly with Annotated[Type, Header()]. A metadata-looking parameter name alone does not select headers instead of query parameters. ⟦A.f1 A:tb1 A:tb2 A:tb5⟧
(mechanism) Header converts underscores to hyphens by default: user_agent reads user-agent. Header names are case-insensitive. Header(alias="user-agent") explicitly chooses that name; Header(convert_underscores=False) keeps the literal user_agent mapping instead. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Annotated[Type, Cookie()] binds a cookie by name. The fixture declares cookie with a None default so omission is accepted. Source selection and omission behavior are separate: Cookie chooses the source, while the default permits absence. ⟦A.f3 A:tb3 A:tb4⟧
[CODE python]
from typing import Annotated
from fastapi import FastAPI, Header, Cookie
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/metadata")
def endpoint(user_agent: Annotated[str, Header()],
             cookie: Annotated[str | None, Cookie()] = None):
    return {"user_agent": user_agent, "cookie": cookie}

# Computed request/declaration evidence; no hand-written response output.
def evidence():
    with TestClient(app) as client:
        for headers, cookies in [({"user-agent": "synthetic client"}, {}),
                                 ({"USER-AGENT": "synthetic client"}, {"cookie": "synthetic cookie"})]:
            response = client.get("/metadata", headers=headers, cookies=cookies)
            yield {"headers": headers, "cookies": cookies,
                   "status": response.status_code, "response": response.json()}

# Explicitly binds the user-agent header.
def alias_example(user_agent: Annotated[str, Header(alias="user-agent")], cookie: Annotated[str | None, Cookie()] = None):
    return {"user_agent": user_agent, "cookie": cookie}

# Binds the literal user_agent header (underscore conversion disabled).
def underscore_example(user_agent: Annotated[str, Header(convert_underscores=False)], cookie: Annotated[str | None, Cookie()] = None):
    return {"user_agent": user_agent, "cookie": cookie}

  annotations: []

### s02 · check · Resolve the header name

### s03 · hands_on · Bind a header and an omittable cookie

### s04 · explainer · Inspect invalid request data
(mechanism) Invalid request data raises RequestValidationError. FastAPI handles it before normal operation logic receives that input. In the order fixture, the quantity value 'not an integer' cannot satisfy the declared integer field. ⟦B.f1 B:tb1 B:tb2 B:tb4⟧
(mechanism) Assert the default status 422, then inspect response.json()["detail"]. Each relevant entry identifies the failed input location through loc and the error kind through type. The fixture derives these expectations from the unchanged contract; do not guess them. ⟦B.f2 B:tb3 B:tb4⟧
(mechanism) A model-validation failure while application code builds a result, or during response validation, indicates a server-side bug. It is not the same as invalid client request data, and not every validation failure is a client 422. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
[CODE python]
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

class OrderInput(BaseModel):
    quantity: int = Field(gt=0)

app = FastAPI()

@app.post("/orders")
def create_order(order: OrderInput):
    return order

client = TestClient(app)
invalid_order = {"quantity": "not an integer"}

# Derive the expected loc/type from this untouched fixture, not a typed output.
def validation_expectations():
    reference = client.post("/orders", json=invalid_order)
    entry = reference.json()["detail"][0]
    return entry["loc"], entry["type"]


  annotations: ['fixture.py']
[CODE python]
from fixture import client, invalid_order, validation_expectations

def evidence():
    expected_location, expected_type = validation_expectations()
    response = client.post("/orders", json=invalid_order)
    assert response.status_code == 422
    entry = response.json()["detail"][0]
    assert entry["loc"] == expected_location
    assert entry["type"] == expected_type
    return {"request": invalid_order, "status": response.status_code, "detail": response.json()["detail"]}

  annotations: ['visual_reference.py']

### s05 · check · Client input or server-side bug?

### s06 · hands_on · Assert the invalid-order response

### s07 · recap · Keep these distinctions
(takeaway) Header and Cookie choose request sources explicitly. Header names are case-insensitive; underscores become hyphens by default. A cookie default permits omission. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Invalid request data is handled before normal operation logic. Assert default status 422 and inspect detail loc/type. Server-side model-validation failures are a different problem. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests: A metrics endpoint existing does not prove counters and durations measure intended request events. Compare maintained instrumentation against known requests.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Resolve the header name
(mental_model) In /metadata, compare the declared source with a metadata-looking name alone. Header or Cookie selects the source; the cookie default separately permits omission. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Header names are case-insensitive. By default user_agent maps to user-agent; alias or convert_underscores=False controls that mapping. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit: Bind a header and an omittable cookie
(mental_model) In /metadata, compare the declared source with a metadata-looking name alone. Header or Cookie selects the source; the cookie default separately permits omission. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(definition) Annotated[Type, Header()] reads a header instead of treating the parameter as a query input. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Annotated[Type, Cookie()] reads a cookie by name. Provide a default when omission should be accepted. ⟦A.f3 A:tb3 A:tb4⟧
### r03 · Revisit: Client input or server-side bug?
(mental_model) Contrast the fixture’s invalid order request with a failure while the service validates its own result. The location of validation separates client input from a server-side bug. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(definition) Validation failures in response or application code indicate a server-side bug, not the same client-input rejection. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
### r04 · Revisit: Assert the invalid-order response
(mental_model) Contrast the fixture’s invalid order request with a failure while the service validates its own result. The location of validation separates client input from a server-side bug. ⟦B.f1 B.f2 B:tb2 B:tb3 B:tb4 B:tb5⟧
(definition) Invalid request data raises RequestValidationError, which FastAPI handles before normal operation logic receives the input. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(definition) Assert the default invalid-input status 422 and inspect JSON detail entries for the failed location and error type. ⟦B.f2 B:tb3 B:tb4⟧

=========

# EVALUATOR PACKET — Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests (tile_058)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = observability.verified_request_metrics — Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (observability.verified_request_metrics)   objective: Configure and verify request metrics instrumentation: instrument one API with a maintained library and exercise three controlled requests.
A.f1: Maintained request instrumentation records request and response counters and a duration histogram around the application boundary rather than requiring each handler to implement its own metrics.   [sources: fastapi_docs_advanced#https://github.com/perdy/starlette-prometheus/blob/master/starlette_prometheus/middleware.py#L12-L27]
A.f2: Install the documented PrometheusMiddleware with app.add_middleware(PrometheusMiddleware, filter_unhandled_paths=True) and expose its metrics view with app.add_route("/metrics/", metrics), importing both from starlette_prometheus.   [sources: fastapi_docs_advanced#https://github.com/perdy/starlette-prometheus#repo-content-turbo-frame]
A.f3: Use bounded nonsensitive labels such as method, matched route template and response status; filter unmatched paths so arbitrary requested paths do not generate unlimited metric series.   [sources: fastapi_docs_advanced#https://github.com/perdy/starlette-prometheus/blob/master/starlette_prometheus/middleware.py#L92-L103, fastapi_docs_advanced#https://github.com/perdy/starlette-prometheus#repo-content-turbo-frame, prometheus_client_python#https://prometheus.io/docs/practices/instrumentation/#use-labels]
A.f4: Verify wiring with controlled successful, expected-error and delayed responses, comparing request and response counter changes and the completed responses' duration observations with those known requests.   [sources: fastapi_docs_advanced#https://github.com/perdy/starlette-prometheus/blob/master/starlette_prometheus/middleware.py#L44-L85, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/testing/#using-testclient]
A.f5: Interpret the selected middleware's measurement boundary accurately: its response counter is updated even for a raised exception, but its processing-time histogram is observed only when the inner application returns a response.   [sources: fastapi_docs_advanced#https://github.com/perdy/starlette-prometheus/blob/master/starlette_prometheus/middleware.py#L60-L85]
note: Establish this first: Metrics correctness is checked against known events before production aggregates are trusted.
note: Stay within the current objective: Configure and verify request metrics instrumentation. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Verify successful, failing and delayed requests update counters and latency observations correctly with nonsensitive low-cardinality labels.
PRACTICE ANCHOR (live_code): Configure one FastAPI API with the documented starlette_prometheus middleware and metrics view. Exercise one successful request, one expected-error request and one deliberately delayed request, then compare their metric changes against those known events.  SUCCESS: The API exposes /metrics/, filters unmatched paths and uses bounded nonsensitive labels. Each controlled request increments the relevant request and response counters once. Each response returned through the instrumentation boundary adds one duration observation, and the delayed response's duration reflects its controlled delay. Comparisons isolate the exercised routes from metrics-view traffic.
ASSESSMENT ANCHOR: verify_application_boundary_instrumentation facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_bounded_nonsensitive_metric_labels facts=['f3']
ASSESSMENT ANCHOR: verify_counters_and_durations_against_controlled_requests facts=['f4']
ASSESSMENT ANCHOR: distinguish_response_counting_from_duration_observation facts=['f5']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; Bounded resource listing with stable pagination and filtering; Consistent public error envelopes through exception handlers; Create resource; Delete resource; Distinct create and partial-update contracts; Documenting expected success and error responses; Freshness policy; Injection-resistant database and input handling; Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels; JWT signature, issuer, audience and expiry verification; Keeping API schemas distinct from persistence entities; Proxy header trust; Redis cache-aside selection and population; Request correlation context across service logs; Retrieve resource; Safe failure policy; Service release and rollback workflow with build, release and run separation; Transaction commit and rollback boundaries; Translating domain and persistence failures at the API boundary; Update resource; Webhook request contracts and acknowledgement behavior

## LESSON, in learner order

### s01 · explainer · Instrument the boundary and verify it
(mechanism) Use maintained instrumentation around the application boundary for request counters, response counters and a duration histogram. Handlers need not each implement their own metrics; an exposed metrics endpoint alone does not verify the wiring. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) Import PrometheusMiddleware and metrics from starlette_prometheus. Register app.add_middleware(PrometheusMiddleware, filter_unhandled_paths=True), then app.add_route("/metrics/", metrics). Use bounded nonsensitive labels such as method, matched route template and response status. Filtering unmatched paths avoids unlimited series from arbitrary requested paths. ⟦A.f2 A.f3 A:tb3⟧
(mechanism) Send controlled successful, expected-error and delayed requests. Compare request and response counter changes and completed-response duration observations with those requests. This middleware updates its response counter even for a raised exception, but observes processing time only when the inner application returns a response. ⟦A.f4 A.f5 A:tb3⟧
[SIDE_BY_SIDE] Compare returned responses with an escaping exception; counting and duration observation differ. left_label: Configure and send known requests | right_label: Observe matched-route changes
  left:
[CODE python]
from fixture import app, CASES
from starlette_prometheus import PrometheusMiddleware, metrics

app.add_middleware(PrometheusMiddleware, filter_unhandled_paths=True)
app.add_route("/metrics/", metrics)

  annotations: []
  right:
[CODE python]
from fixture import app
from fastapi.testclient import TestClient
from prometheus_client.parser import text_string_to_metric_families
from fixture import CASES

def snapshot(client, route):
    text = client.get("/metrics/").text
    values = {}
    for family in text_string_to_metric_families(text):
        for sample in family.samples:
            # Only the exercised template; do not mix in metrics-view requests.
            if sample.labels.get("path") == route:
                key = (sample.name, tuple(sorted(sample.labels.items())))
                values[key] = sample.value
    return values

def observe(app):
    with TestClient(app, raise_server_exceptions=False) as client:
        for case in CASES:
            route = case["route_template"]
            before = snapshot(client, route)
            response = client.get(route)
            after = snapshot(client, route)
            keys = sorted(set(before) | set(after))
            yield {"case": case, "actual_status": response.status_code,
                   "samples": [{"metric": key[0], "labels": dict(key[1]),
                                "before": before.get(key, 0), "after": after.get(key, 0),
                                "change": after.get(key, 0) - before.get(key, 0)} for key in keys]}

def evidence():
    return list(observe(app))

  annotations: []

### s02 · explainer · A response count is not a duration observation
(mechanism) The registered fixture separates success, expected-error, delayed response and escaping-exception cases. Compare before/after samples for each matched route, rather than mixing them with metrics-view requests. The maintained counters and duration histogram should be checked against these controlled events, not assumed correct because /metrics/ exists. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧
(mechanism) An expected-error response still returns a response. An escaping exception differs: this middleware updates its response counter but has no normal processing-time observation for that exception. Counts and completed-response durations therefore need not cover identical cases. ⟦A.f5 A:tb4 A:tb5⟧

### s03 · check · Compare measurement boundaries

### s04 · hands_on · Verify controlled request metrics

### s05 · recap · Keep these distinctions
(takeaway) Install maintained boundary instrumentation and expose /metrics/. Use bounded nonsensitive labels and filter unmatched paths. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4⟧
(takeaway) Verify known successful, expected-error and delayed requests against counter changes and duration observations. A raised exception updates this middleware’s response counter, but its normal processing-time observation requires a returned response. ⟦A.f4 A.f5 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Distinct create and partial-update contracts: A partial update must distinguish "leave unchanged" from "set to null." Presence carries intent separately from value.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Compare measurement boundaries
(mental_model) Contrast the fixture’s returned expected-error response with its escaping exception. A response count and a normal duration observation do not have identical boundaries. ⟦A.f5 A:tb3 A:tb4 A:tb5⟧
(definition) This middleware updates its response counter even for a raised exception. Its processing-time histogram is observed only when the inner application returns a response. ⟦A.f5 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit: Verify controlled request metrics
(mental_model) Contrast the fixture’s returned expected-error response with its escaping exception. A response count and a normal duration observation do not have identical boundaries. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3 A:tb4 A:tb5⟧
(definition) Maintained boundary instrumentation supplies request/response counters and a duration histogram, rather than metrics implemented separately in each handler. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Import PrometheusMiddleware and metrics from starlette_prometheus. Use app.add_middleware(PrometheusMiddleware, filter_unhandled_paths=True) and app.add_route("/metrics/", metrics). ⟦A.f2 A:tb3 A:tb4⟧
(definition) Choose bounded nonsensitive labels such as method, matched route template and response status. Filter unmatched paths to avoid unlimited series from arbitrary paths. ⟦A.f3 A:tb3 A:tb4⟧
(definition) Compare controlled successful, expected-error and delayed requests with request/response counter changes and completed-response duration observations. ⟦A.f4 A:tb3 A:tb4⟧
(definition) This middleware updates its response counter even for a raised exception. Its processing-time histogram is observed only when the inner application returns a response. ⟦A.f5 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Preserve input intent as contracts evolve (tile_059)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = pydantic.partial_update_contracts — Distinct create and partial-update contracts
B = rest.compatible_contract_changes — Backward-compatible REST contract changes

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (pydantic.partial_update_contracts)   objective: Preserve partial-update intent: implement one patch extraction.
A.f1: Pydantic tracks explicitly supplied fields in model_fields_set; model_dump(exclude_unset=True) excludes fields that were not supplied.   [sources: pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/serialization/#excluding-and-including-fields-based-on-their-value]
A.f2: Extract a partial update with update = model.model_dump(exclude_unset=True) so defaults for omitted fields do not overwrite stored values.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/body-updates/#using-pydantics-exclude-unset-parameter]
A.f3: Explicitly supplied None remains supplied under exclude_unset=True; exclude_none=True separately removes None-valued fields and can erase an intentional null update.   [sources: pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/serialization/#excluding-and-including-fields-based-on-their-value]
note: Establish this first: Presence carries intent separately from value.
note: Stay within the current objective: Preserve partial-update intent. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Distinguish absent, null and supplied fields.
PRACTICE ANCHOR (live_code): Implement one partial-update extraction using update = model.model_dump(exclude_unset=True), then compare its results for an omitted note, an explicitly null note and a supplied string note.  SUCCESS: A quantity-only input produces only quantity in the extracted update. An explicitly supplied note=None produces a note key with value None, and a supplied string note retains that string. Omitted defaults never enter the extracted update.
ASSESSMENT ANCHOR: distinguish_omitted_fields_from_supplied_fields facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_explicit_null_from_omission facts=['f1', 'f3']
ASSESSMENT ANCHOR: differentiate_exclude_unset_and_exclude_none facts=['f3']

## SOURCE FACTS — B (rest.compatible_contract_changes)   objective: Evaluate compatibility: review one schema change.
B.f1: Changing an omittable request field into a required field rejects requests that were previously accepted, so a schema review must compare requiredness as well as types.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/body/#request-body-path-query-parameters, pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/fields/#default-values]
B.f2: Tightening a type or field constraint can invalidate previously accepted client input; test representative previously valid inputs against the revised model.   [sources: pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/models/#data-conversion, pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/fields/#numeric-constraints, pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/fields/#string-constraints]
B.f3: Removing or changing a public response field or operation can change a client's documented expectations; compare the generated paths and response schemas with the previous contract before approving the change.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/response-model/#response-model-parameter, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/first-steps/#check-the-openapi-json]
note: Establish this first: Compatibility preserves previously valid expectations.
note: Stay within the current objective: Evaluate compatibility. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify client-breaking changes.
PRACTICE ANCHOR (live_code): Review one order request-schema change that makes note required instead of omittable. Validate representative previously accepted inputs against both models and identify the compatibility consequence.  SUCCESS: Demonstrate that a request omitting note passes the previous model but fails the revision, while a request supplying a string note passes both. Identify the new requiredness as client-breaking and preserve the previous default to retain omission support.
ASSESSMENT ANCHOR: identify_breaking_requiredness_changes facts=['f1']
ASSESSMENT ANCHOR: identify_input_rejection_from_tightened_types_or_constraints facts=['f2']
ASSESSMENT ANCHOR: identify_breaking_public_response_or_operation_changes facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Backward-compatible REST contract changes; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; Bounded resource listing with stable pagination and filtering; Consistent public error envelopes through exception handlers; Create resource; Delete resource; Documenting expected success and error responses; Freshness policy; Injection-resistant database and input handling; Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels; JWT signature, issuer, audience and expiry verification; Keeping API schemas distinct from persistence entities; Proxy header trust; Redis cache-aside selection and population; Request correlation context across service logs; Retrieve resource; Safe failure policy; Safe unexpected-error responses with actionable server evidence; Service release and rollback workflow with build, release and run separation; Transaction commit and rollback boundaries; Translating domain and persistence failures at the API boundary; Update resource; Upstream failure translation; Webhook request contracts and acknowledgement beh

## LESSON, in learner order

### s01 · explainer · Preserve supplied-field intent
(mechanism) A partial update separates presence from value. Pydantic records explicitly supplied fields in model_fields_set; model_dump(exclude_unset=True) excludes fields that were not supplied. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) Extract update = model.model_dump(exclude_unset=True) so omitted fields do not introduce defaults that overwrite stored values. Inspect the extracted data before changing storage. A quantity-only input leaves note out of the update rather than treating its default as a supplied value. ⟦A.f1 A.f2 A:tb3 A:tb4⟧
(mechanism) An explicitly supplied note=None remains supplied with exclude_unset=True. A supplied string keeps its value. Adding exclude_none=True separately removes None-valued fields and can erase an intentional null update. A final model value alone cannot distinguish omission from explicit supply. ⟦A.f1 A.f3 A:tb3 A:tb4⟧
[SIDE_BY_SIDE] Inspect supplied fields and execute the extraction; exclude_none removes null separately from omission. left_label: Three supplied-field cases | right_label: Compare extraction options
  left:
[CODE python]
from pydantic import BaseModel

class OrderUpdate(BaseModel):
    note: str | None = None
    quantity: int | None = None

quantity_only = OrderUpdate(quantity=2)
explicit_null = OrderUpdate(note=None)
concrete_note = OrderUpdate(note='Leave at reception')

  annotations: []
  right:
[CODE python]
from main import quantity_only, explicit_null, concrete_note

def evidence():
    for name, model in [("note omitted", quantity_only),
                        ("explicit null note", explicit_null),
                        ("concrete note", concrete_note)]:
        yield {"case": name, "model_fields_set": sorted(model.model_fields_set),
               "exclude_unset": model.model_dump(exclude_unset=True),
               "exclude_unset_and_none": model.model_dump(exclude_unset=True, exclude_none=True)}

  annotations: []

### s02 · explainer · Omission and null are different updates
(mechanism) Compare the registered cases: quantity-only input, explicit note=None, and note='Leave at reception'. model_fields_set reveals what was supplied; model_dump(exclude_unset=True) extracts those fields without omitted defaults. This preserves the difference between leaving note unchanged and supplying a replacement value. ⟦A.f1 A.f2 A:tb5⟧
(mechanism) exclude_unset asks whether a field was supplied. exclude_none asks whether its value is None. They are not interchangeable cleanup flags: adding exclude_none can remove the explicit null that the update contract intended to preserve. ⟦A.f1 A.f3 A:tb5 A:tb6⟧

### s03 · video · Trace supplied-field extraction
[VIDEO ] bridge-before:  | bridge-after: 

### s04 · check · Separate omitted and supplied fields

### s05 · hands_on · Extract updates without losing null intent

### s06 · explainer · Review the previous contract too
(mechanism) Compatibility review compares old client expectations, not just matching type names. Changing an omittable note field into a required field rejects previously accepted requests that omit it. Compare requiredness as well as types. ⟦B.f1 B:tb1 B:tb2 B:tb5⟧
(mechanism) Tightening a type or field constraint can reject previously valid input. Test representative old inputs against the revised model. The registered comparison keeps an old quantity sample alongside the previous and tightened constraints, so both validations can be inspected. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Removing or changing a public response field or operation can change documented client expectations. Compare the generated paths and response schemas against the previous contract before approving the revision. Matching input type names alone says nothing about those public output changes. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
[SIDE_BY_SIDE] Compare old inputs and generated public schemas, not just type names. left_label: Previous and revised requiredness | right_label: Constraints and public contracts
  left:
[CODE python]
from pydantic import BaseModel, ValidationError

class PreviousOrderInput(BaseModel):
    note: str | None = None

class RevisedOrderInput(BaseModel):
    note: str | None

omitted_note = {}
supplied_note = {"note": 'Leave at reception'}

  annotations: []
  right:
[CODE python]
from fastapi import FastAPI
from pydantic import BaseModel, Field, ValidationError
from main import PreviousOrderInput, RevisedOrderInput, omitted_note, supplied_note

# Independent synthetic comparisons; do not combine these changes with the practice task.
class PreviousQuantity(BaseModel):
    quantity: int = Field(gt=0)

class TightenedQuantity(BaseModel):
    quantity: int = Field(gt=2)

class PreviousResponse(BaseModel):
    quantity: int
    note: str | None = None

class RemovedNoteResponse(BaseModel):
    quantity: int

def validation_evidence():
    for old, new, payload in [(PreviousOrderInput, RevisedOrderInput, omitted_note),
                              (PreviousOrderInput, RevisedOrderInput, supplied_note),
                              (PreviousQuantity, TightenedQuantity, {"quantity": 2})]:
        results = []
        for model in (old, new):
            try:
                value = model.model_validate(payload)
                results.append({"model": model.__name__, "accepted": True, "value": value.model_dump()})
            except ValidationError as exc:
                results.append({"model": model.__name__, "accepted": False, "errors": exc.errors()})
        yield {"input": payload, "results": results}

def contract_app(response_model, include_operation=True):
    app = FastAPI()
    if include_operation:
        @app.get("/orders/{order_id}", response_model=response_model)
        def retrieve_order(order_id: int):
            return {"quantity": 2, "note": 'Leave at reception'}
    return app

def schema_evidence():
    for name, app in [("previous", contract_app(PreviousResponse)),
                      ("response field removed", contract_app(RemovedNoteResponse)),
                      ("operation removed", contract_app(PreviousResponse, False))]:
        schema = app.openapi()
        yield {"case": name, "paths": schema["paths"],
               "schemas": schema.get("components", {}).get("schemas", {})}

  annotations: []

### s07 · check · Review tightened input constraints

### s08 · check · Review public fields and operations

### s09 · hands_on · Compare requiredness across revisions

### s10 · recap · Keep these distinctions
(takeaway) model_fields_set tracks supply; exclude_unset extracts supplied fields without omitted defaults. Explicit None remains supplied; exclude_none can erase intentional null. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(takeaway) Review requiredness, tightened types or constraints, public response fields and operations. Test previously valid inputs and compare generated paths and response schemas before approving changes. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Retrieve resource: Next: Retrieve resource.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Separate omitted and supplied fields
(mental_model) Compare quantity-only input, note=None, and the registered string note. Omission is not explicit null; supplied-field extraction preserves that distinction. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(definition) model_fields_set records explicitly supplied fields; model_dump(exclude_unset=True) leaves out fields that were not supplied. ⟦A.f1 A:tb2 A:tb4 A:tb5 A:tb6⟧
(definition) Extract update = model.model_dump(exclude_unset=True) so defaults for omitted fields do not overwrite stored values. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit: Extract updates without losing null intent
(mental_model) Compare quantity-only input, note=None, and the registered string note. Omission is not explicit null; supplied-field extraction preserves that distinction. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(definition) model_fields_set records explicitly supplied fields; model_dump(exclude_unset=True) leaves out fields that were not supplied. ⟦A.f1 A:tb2 A:tb4 A:tb5 A:tb6⟧
(definition) Explicit None remains supplied with exclude_unset=True. exclude_none=True separately removes None-valued fields and can erase an intentional null update. ⟦A.f3 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r03 · Revisit: Review tightened input constraints
(mental_model) Compare the same old order request against the previous and revised note declarations. Matching type names do not establish matching requiredness or the rest of the public contract. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(definition) Tightening a type or constraint can reject previously valid input. Test representative old inputs against the revision. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
### r04 · Revisit: Review public fields and operations
(mental_model) Compare the same old order request against the previous and revised note declarations. Matching type names do not establish matching requiredness or the rest of the public contract. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(definition) Changing or removing a public response field or operation can change documented client expectations. Compare generated paths and response schemas with the previous contract. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
### r05 · Revisit: Compare requiredness across revisions
(mental_model) Compare the same old order request against the previous and revised note declarations. Matching type names do not establish matching requiredness or the rest of the public contract. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(definition) Making an omittable request field required rejects formerly accepted requests. Compare requiredness as well as types. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧