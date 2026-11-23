# EVALUATOR PACKET — Resource-oriented REST URLs and CRUD contracts · FastAPI application and path-operation declarations (tile_022)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = rest.resource_contract_design — Resource-oriented REST URLs and CRUD contracts
B = fastapi.path_operations — FastAPI application and path-operation declarations

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (rest.resource_contract_design)   objective: Design resource contracts: specify one resource's CRUD contract.
A.f1: A URL path identifies a resource, and an HTTP method supplies the operation semantics rather than the path alone determining the action.   [sources: rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-9.3.1, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/first-steps/#path]
A.f2: Model an item resource with a path parameter for its identifier and a collection resource without that item identifier.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/query-params/#query-parameters, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/path-params/#path-parameters]
A.f3: Specify retrieval with GET, collection-specific creation processing with POST, target replacement with PUT and removal with DELETE, preserving each method's semantics.   [sources: rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-9.3.1, rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-9.3.3, rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-9.3.4, rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-9.3.5]
A.f4: A creation contract can use 201 with a Location identifying the created resource, while an absent item can use 404.   [sources: rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-15.3.2, rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-15.5.5]
note: Establish this first: Resource identity organizes operations.
note: Stay within the current objective: Design resource contracts. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Map operations to item and collection resources.
PRACTICE ANCHOR (live_code): Specify an orders resource's CRUD contract using annotated Python variables for resource paths, HTTP methods, response statuses and the created item's Location. Represent the contract without implementing request handling.  SUCCESS: The contract distinguishes /orders from /orders/{order_id}, assigns GET to retrieval, POST to collection creation processing, PUT to item replacement and DELETE to item removal, and records 201 with Location /orders/42 for creation and 404 for an absent item.
ASSESSMENT ANCHOR: distinguish_collection_and_item_resource_identity facts=['f1', 'f2']
ASSESSMENT ANCHOR: map_crud_methods_to_collection_and_item_resources facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: specify_created_resource_and_absent_item_responses facts=['f4']

## SOURCE FACTS — B (fastapi.path_operations)   objective: Register path operations: register one resource's routes.
B.f1: Create a FastAPI instance and register a handler with @app.get("/path"), @app.post("/path"), @app.put("/path") or @app.delete("/path") for the intended method and path.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/first-steps/#define-a-path-operation-decorator]
B.f2: A path operation is the combination of an HTTP method and a path; handlers registered for different methods on the same path serve different operations.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/first-steps/#step-3-create-a-path-operation]
B.f3: Routes are evaluated in order, so declare a fixed path before a conflicting parameterized path to prevent the latter from capturing it.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/path-params/#order-matters]
note: Establish this first: Method and path map requests to handlers.
note: Stay within the current objective: Register path operations. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine method-path handler selection.
PRACTICE ANCHOR (live_code): Create a FastAPI instance and register order-resource handlers: POST /orders, GET /orders/current, and GET, PUT and DELETE /orders/{order_id}. Declare the fixed GET path before the conflicting parameterized GET path. Use static return values without reading request inputs.  SUCCESS: The declarations associate each intended method and path with a distinct handler, and GET /orders/current precedes GET /orders/{order_id}. Handler bodies return static values; request-input binding and persistence are not needed.
ASSESSMENT ANCHOR: determine_handler_from_method_and_path facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_operations_sharing_a_path facts=['f2']
ASSESSMENT ANCHOR: determine_handler_from_conflicting_route_order facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Async-compatible external HTTP requests; Binding request bodies to typed models; Bounded form and multipart file inputs; Bounded in-process background work and nondurable delivery limits; CORS origin and credential policy; Choosing def versus async def from I/O behavior without blocking the event loop; Composing request dependency graphs; Configuring existing middleware in the request/response stack; Custom validation for domain invariants; Depends; Endpoint integration tests using TestClient or async HTTPX as appropriate; Expected API failures with HTTPException; FastAPI OpenAPI generation from typed route contracts; FastAPI application and path-operation declarations; Modular FastAPI application composition with APIRouter; Outbound timeouts; Preventing unsafe outbound requests and SSRF; Production ASGI serving versus development reload; Request-scoped dependency reuse and lifetime; Required, optional and default input semantics; Response-model serialization and private-field exclusion; Separating transport, testable business logic and persistence responsibilities; Structured service request and error logs; Typed path and query input binding; Validated environment-based configurat

## LESSON, in learner order

### s01 · explainer · The rule: Resource-oriented REST URLs and CRUD contracts
(definition) A URL path identifies a resource, and an HTTP method supplies the operation semantics rather than the path alone determining the action. ⟦A.f1 A:tb2⟧
(mechanism) Model an item resource with a path parameter for its identifier and a collection resource without that item identifier. Specify retrieval with GET, collection-specific creation processing with POST, target replacement with PUT and removal with DELETE, preserving each method's semantics. A creation contract can use 201 with a Location identifying the created resource, while an absent item can use 404. ⟦A.f2 A.f3 A.f4 A:tb3⟧
[DIAGRAM] nodes=['Collection /orders', 'Item /orders/{order_id}', 'Created item /orders/42'] edges=[('n0', 'n1', 'GET retrieves; PUT replaces; DELETE removes'), ('n0', 'n2', 'POST collection creation: can use 201 + Location'), ('n1', 'n1', 'Absent item: can use 404')] alt: Make the orders collection and identified item visible as distinct resources. Annotate GET retrieval, POST collection creation processing, PUT item replacement and DELETE item removal, with 201 and Location /orders/42 for creation and 404 for an absent item.

### s02 · explainer · Trace the boundary: Resource-oriented REST URLs and CRUD contracts
(walkthrough) Keep resource identity separate from the operation: /orders is the collection; /orders/{order_id} identifies an item. GET retrieves, POST processes collection creation, PUT replaces the target, and DELETE removes it. A creation contract can pair 201 with Location /orders/42; an absent item can use 404. Changing the method changes the semantics even when the item path stays the same. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Choose the distinction: Resource-oriented REST URLs and CRUD contracts
Check your understanding — Use the declared contract to distinguish the outcomes.

### s04 · hands_on · Practice: Resource-oriented REST URLs and CRUD contracts
Apply the contract — Work in the supplied orders-service exercise snapshot.

### s05 · explainer · The rule: FastAPI application and path-operation declarations
(definition) Create a FastAPI instance and register a handler with @app.get("/path"), @app.post("/path"), @app.put("/path") or @app.delete("/path") for the intended method and path. ⟦B.f1 B:tb2⟧
(mechanism) A path operation is the combination of an HTTP method and a path; handlers registered for different methods on the same path serve different operations. Routes are evaluated in order, so declare a fixed path before a conflicting parameterized path to prevent the latter from capturing it. ⟦B.f2 B.f3 B:tb3⟧
[CODE python]
from fastapi import FastAPI
app = FastAPI()
@app.post('/orders')
def create_order():
    return {}
@app.get('/orders/current')
def current_order():
    return {}
@app.get('/orders/{order_id}')
def retrieve_order():
    return {}
@app.put('/orders/{order_id}')
def replace_order():
    return {}
@app.delete('/orders/{order_id}')
def remove_order():
    return {}

  annotations: ['Review method, path, and declaration order together. GET and PUT on the item path register different operations. Declare /orders/current before a conflicting /orders/{order_id} route: the earlier parameterized route can capture the fixed path. A later fixed declaration does not automatically win.']

### s06 · explainer · Trace the boundary: FastAPI application and path-operation declarations
(walkthrough) Review method, path, and declaration order together. GET and PUT on the item path register different operations. Declare /orders/current before a conflicting /orders/{order_id} route: the earlier parameterized route can capture the fixed path. A later fixed declaration does not automatically win. ⟦B.f1 B.f2 B.f3 B:tb4⟧

### s07 · explainer · Trace the boundary: FastAPI application and path-operation declarations
(walkthrough) Review method, path, and declaration order together. GET and PUT on the item path register different operations. Declare /orders/current before a conflicting /orders/{order_id} route: the earlier parameterized route can capture the fixed path. A later fixed declaration does not automatically win. ⟦B.f1 B.f2 B.f3 B:tb5 B:tb6⟧

### s08 · video · FastAPI application and path-operation declarations
[VIDEO ] bridge-before:  | bridge-after: 

### s09 · check · Choose the distinction: FastAPI application and path-operation declarations
Check your understanding — Use the declared contract to distinguish the outcomes.

### s10 · check · Choose the distinction: FastAPI application and path-operation declarations
Check your understanding — Use the declared contract to distinguish the outcomes.

### s11 · hands_on · Practice: FastAPI application and path-operation declarations
Apply the contract — Work in the supplied orders-service exercise snapshot.

### s12 · recap · Keep these boundaries
(takeaway) A path is not a complete operation definition. The method supplies semantics alongside resource identity. ⟦A.f1 A:tb5⟧
(takeaway) Do not assume the framework always chooses a fixed route over an earlier conflicting parameterized route. Declaration order matters. ⟦B.f3 B:tb6⟧
[UP NEXT] Validated environment-based configuration with fail-fast startup: Next: Validated environment-based configuration with fail-fast startup.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast again: Resource-oriented REST URLs and CRUD contracts
(definition) A creation contract can use 201 with a Location identifying the created resource, while an absent item can use 404. ⟦A.f4 A:tb3 A:tb4⟧
(example) Contrast a creation contract using 201 and Location /orders/42 with an absent-item contract using 404. ⟦A.f4 A:tb3 A:tb4⟧
### r02 · Try the contrast again: Resource-oriented REST URLs and CRUD contracts
(definition) A URL path identifies a resource, and an HTTP method supplies the operation semantics rather than the path alone determining the action. Model an item resource with a path parameter for its identifier and a collection resource without that item identifier. Specify retrieval with GET, collection-specific creation processing with POST, target replacement with PUT and removal with DELETE, preserving each method's semantics. A creation contract can use 201 with a Location identifying the created resource, while an absent item can use 404. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) GET and PUT can address the same order item but request different operations. /orders names the collection; /orders/{order_id} names an identified item. Retrieval uses GET; replacement uses PUT, even on the same item path. Contrast a creation contract using 201 and Location /orders/42 with an absent-item contract using 404. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Try the contrast again: FastAPI application and path-operation declarations
(definition) A path operation is the combination of an HTTP method and a path; handlers registered for different methods on the same path serve different operations. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(example) GET and PUT on the same order-item path are two operations, not one. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
### r04 · Try the contrast again: FastAPI application and path-operation declarations
(definition) Routes are evaluated in order, so declare a fixed path before a conflicting parameterized path to prevent the latter from capturing it. ⟦B.f3 B:tb3 B:tb4 B:tb5 B:tb6⟧
(example) Put /orders/current first; an earlier conflicting /orders/{order_id} can capture that request. ⟦B.f3 B:tb3 B:tb4 B:tb5 B:tb6⟧
### r05 · Try the contrast again: FastAPI application and path-operation declarations
(definition) Create a FastAPI instance and register a handler with @app.get("/path"), @app.post("/path"), @app.put("/path") or @app.delete("/path") for the intended method and path. A path operation is the combination of an HTTP method and a path; handlers registered for different methods on the same path serve different operations. ⟦B.f1 B.f2 B:tb2 B:tb3 B:tb4 B:tb5⟧
(example) The application decorator registers a handler; the path text alone does not register a method. GET and PUT on the same order-item path are two operations, not one. ⟦B.f1 B.f2 B:tb2 B:tb3 B:tb4 B:tb5⟧

=========

# EVALUATOR PACKET — Validated environment-based configuration with fail-fast startup (tile_024)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.validated_environment_configuration — Validated environment-based configuration with fail-fast startup

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (fastapi.validated_environment_configuration)   objective: Validate environment settings: define one environment's settings.
A.f1: Subclass BaseSettings from pydantic_settings and declare typed fields to load and validate external configuration.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/settings/#pydantic-settings]
A.f2: Construct Settings() to read environment variables and validate their types, with missing required settings or invalid values producing validation failures.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/settings/#create-the-settings-object]
A.f3: Use SettingsConfigDict(env_file=".env") as model_config when a dotenv file should provide settings; environment variables take precedence over its values.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/settings/#reading-a-env-file]
note: Establish this first: Configuration is external input validated at construction.
note: Stay within the current objective: Validate environment settings. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify invalid settings before serving.
PRACTICE ANCHOR (live_code): Define one environment's Settings class with a required string app_name, configure .env loading, and construct the settings before serving.  SUCCESS: Settings construction accepts the supplied app_name, uses the environment value when .env supplies a different value, and fails when neither source supplies the required setting.
ASSESSMENT ANCHOR: identify_settings_construction_failures_before_serving facts=['f1', 'f2']
ASSESSMENT ANCHOR: determine_effective_settings_source_and_validation_outcome facts=['f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Async-compatible external HTTP requests; Binding request bodies to typed models; Bounded form and multipart file inputs; Bounded in-process background work and nondurable delivery limits; CORS origin and credential policy; Choosing def versus async def from I/O behavior without blocking the event loop; Composing request dependency graphs; Configuring existing middleware in the request/response stack; Custom validation for domain invariants; Depends; Endpoint integration tests using TestClient or async HTTPX as appropriate; Expected API failures with HTTPException; FastAPI OpenAPI generation from typed route contracts; Modular FastAPI application composition with APIRouter; Outbound timeouts; Preventing unsafe outbound requests and SSRF; Production ASGI serving versus development reload; Request-scoped dependency reuse and lifetime; Required, optional and default input semantics; Response-model serialization and private-field exclusion; Separating transport, testable business logic and persistence responsibilities; Structured service request and error logs; Trusted host validation; Typed path and query input binding; Yield-based dependency cleanup

## LESSON, in learner order

### s01 · explainer · The rule: Validated environment-based configuration with fail-fast startup
(definition) Subclass BaseSettings from pydantic_settings and declare typed fields to load and validate external configuration. ⟦A.f1 A:tb2⟧
(mechanism) Construct Settings() to read environment variables and validate their types, with missing required settings or invalid values producing validation failures. Use SettingsConfigDict(env_file=".env") as model_config when a dotenv file should provide settings; environment variables take precedence over its values. ⟦A.f2 A.f3 A:tb3⟧
[CODE python]
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

# Source cases (external inputs):
# {"name": "environment_only", "environment": {"APP_NAME": "synthetic-environment-orders"}, "dotenv": {}}
# {"name": "conflicting_sources", "environment": {"APP_NAME": "synthetic-environment-orders"}, "dotenv": {"APP_NAME": "synthetic-dotenv-orders"}}
# {"name": "absent_from_both", "environment": {}, "dotenv": {}}

  annotations: ['Declare required typed fields on a BaseSettings subclass, then construct Settings(). Compare valid, missing, and invalid external values: missing required settings and invalid values fail validation. Configure a dotenv file with SettingsConfigDict(env_file=".env"). If both sources supply a key, the environment takes precedence; priority does not remove type validation.']

### s02 · explainer · Trace the boundary: Validated environment-based configuration with fail-fast startup
(walkthrough) Declare required typed fields on a BaseSettings subclass, then construct Settings(). Compare valid, missing, and invalid external values: missing required settings and invalid values fail validation. Configure a dotenv file with SettingsConfigDict(env_file=".env"). If both sources supply a key, the environment takes precedence; priority does not remove type validation. ⟦A.f1 A.f2 A.f3 A:tb4⟧

### s03 · explainer · Trace the boundary: Validated environment-based configuration with fail-fast startup
(walkthrough) Declare required typed fields on a BaseSettings subclass, then construct Settings(). Compare valid, missing, and invalid external values: missing required settings and invalid values fail validation. Configure a dotenv file with SettingsConfigDict(env_file=".env"). If both sources supply a key, the environment takes precedence; priority does not remove type validation. ⟦A.f1 A.f2 A.f3 A:tb5 A:tb6⟧

### s04 · video · Validated environment-based configuration with fail-fast startup
[VIDEO ] bridge-before:  | bridge-after: 

### s05 · check · Choose the distinction: Validated environment-based configuration with fail-fast startup
Check your understanding — Use the declared contract to distinguish the outcomes.

### s06 · hands_on · Practice: Validated environment-based configuration with fail-fast startup
Apply the contract — Work in the supplied orders-service exercise snapshot.

### s07 · recap · Keep these boundaries
(takeaway) A dotenv value does not override an environment variable. Missing required configuration and invalid values are validation failures, not silent valid settings. ⟦A.f2 A.f3 A:tb6⟧
[UP NEXT] Async-compatible external HTTP requests: Next: Async-compatible external HTTP requests.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast again: Validated environment-based configuration with fail-fast startup
(definition) Construct Settings() to read environment variables and validate their types, with missing required settings or invalid values producing validation failures. Use SettingsConfigDict(env_file=".env") as model_config when a dotenv file should provide settings; environment variables take precedence over its values. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5 A:tb6⟧
(example) Compare a valid setting with a missing required setting: only the valid case satisfies construction. When APP_NAME appears in both sources, the environment wins, not the dotenv file. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r02 · Try the contrast again: Validated environment-based configuration with fail-fast startup
(definition) Subclass BaseSettings from pydantic_settings and declare typed fields to load and validate external configuration. Construct Settings() to read environment variables and validate their types, with missing required settings or invalid values producing validation failures. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(example) Declare app_name as a required typed setting, rather than accepting unchecked external configuration. Compare a valid setting with a missing required setting: only the valid case satisfies construction. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧

=========

# EVALUATOR PACKET — Async-compatible external HTTP requests (tile_025)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = integration.async_http_requests — Async-compatible external HTTP requests

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (integration.async_http_requests)   objective: Make managed async HTTP calls: use one reusable client with cleanup.
A.f1: Use httpx.AsyncClient and await client.get(...), client.post(...) or another request method for an asynchronous outbound call.   [sources: fastapi_docs_advanced#https://www.python-httpx.org/async/#making-async-requests]
A.f2: Reuse a scoped AsyncClient instead of creating clients inside a hot loop to benefit from connection pooling.   [sources: fastapi_docs_advanced#https://www.python-httpx.org/async/#opening-and-closing-clients]
A.f3: Close a client with async with httpx.AsyncClient() as client or await client.aclose() at the end of its owning scope.   [sources: fastapi_docs_advanced#https://www.python-httpx.org/async/#opening-and-closing-clients]
note: Establish this first: Connection-owning clients outlive calls.
note: Stay within the current objective: Make managed async HTTP calls. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify client lifetime mistakes.
PRACTICE ANCHOR (live_code): Implement sequential external-service lookups for an orders handler using one reusable AsyncClient, awaited requests, and cleanup at the end of the owning scope.  SUCCESS: Both lookups use the same AsyncClient, each request is awaited, and the client is closed only after the scope finishes using it.
ASSESSMENT ANCHOR: identify_async_client_lifetime_mistakes facts=['f1', 'f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Binding request bodies to typed models; Bounded form and multipart file inputs; Bounded in-process background work and nondurable delivery limits; CORS origin and credential policy; Choosing def versus async def from I/O behavior without blocking the event loop; Composing request dependency graphs; Configuring existing middleware in the request/response stack; Credential and sensitive-data redaction from emitted logs; Custom validation for domain invariants; Depends; Endpoint integration tests using TestClient or async HTTPX as appropriate; Expected API failures with HTTPException; FastAPI OpenAPI generation from typed route contracts; Modular FastAPI application composition with APIRouter; Outbound timeouts; Preventing unsafe outbound requests and SSRF; Production ASGI serving versus development reload; Request-scoped dependency reuse and lifetime; Required, optional and default input semantics; Response-model serialization and private-field exclusion; Separating transport, testable business logic and persistence responsibilities; Structured service request and error logs; Trusted host validation; Typed path and query input binding; Yield-based dependency cleanup

## LESSON, in learner order

### s01 · explainer · The rule: Async-compatible external HTTP requests
(definition) Choose httpx.AsyncClient and await client.get(...), client.post(...) or another request method for an asynchronous outbound call. ⟦A.f1 A:tb2⟧
(mechanism) Reuse a scoped AsyncClient instead of creating clients inside a hot loop to benefit from connection pooling. Close a client with async with httpx.AsyncClient() as client or await client.aclose() at the end of its owning scope. ⟦A.f2 A.f3 A:tb3⟧
[CODE python]
import httpx

# Synthetic URLs: the exercise harness must intercept requests; never contact them.
lookup_urls = ("https://shipping.example.test/orders/42", "https://shipping.example.test/orders/43")

async def orders():
    async with httpx.AsyncClient() as client:
        for url in lookup_urls:
            await client.get(url)
    # Scope exit closes the client.

# Repeated calls with a separate client for each iteration:
async def separate_clients():
    for url in lookup_urls:
        async with httpx.AsyncClient() as client:
            await client.get(url)

  annotations: ['One owning scope can reuse an AsyncClient for several awaited lookups, benefiting from connection pooling. Avoid constructing a new client inside a hot loop. Awaiting get or post performs a request; it does not close the client. Close at the end of the owning scope with the async context manager or await client.aclose().']

### s02 · explainer · Trace the boundary: Async-compatible external HTTP requests
(walkthrough) One owning scope can reuse an AsyncClient for several awaited lookups, benefiting from connection pooling. Avoid constructing a new client inside a hot loop. Awaiting get or post performs a request; it does not close the client. Close at the end of the owning scope with the async context manager or await client.aclose(). ⟦A.f1 A.f2 A.f3 A:tb4⟧

### s03 · explainer · Trace the boundary: Async-compatible external HTTP requests
(walkthrough) One owning scope can reuse an AsyncClient for several awaited lookups, benefiting from connection pooling. Avoid constructing a new client inside a hot loop. Awaiting get or post performs a request; it does not close the client. Close at the end of the owning scope with the async context manager or await client.aclose(). ⟦A.f1 A.f2 A.f3 A:tb5 A:tb6⟧

### s04 · video · Async-compatible external HTTP requests
[VIDEO ] bridge-before:  | bridge-after: 

### s05 · check · Choose the distinction: Async-compatible external HTTP requests
Check your understanding — Use the declared contract to distinguish the outcomes.

### s06 · hands_on · Practice: Async-compatible external HTTP requests
Apply the contract — Work in the supplied orders-service exercise snapshot.

### s07 · recap · Keep these boundaries
(takeaway) An awaited request does not replace client cleanup. Reuse a scoped client where appropriate and close it at the end of that scope. ⟦A.f2 A.f3 A:tb6⟧
[UP NEXT] Custom validation for domain invariants: Next: Custom validation for domain invariants.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast again: Async-compatible external HTTP requests
(definition) Use httpx.AsyncClient and await client.get(...), client.post(...) or another request method for an asynchronous outbound call. Reuse a scoped AsyncClient instead of creating clients inside a hot loop to benefit from connection pooling. Close a client with async with httpx.AsyncClient() as client or await client.aclose() at the end of its owning scope. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(example) Await the outbound lookup; writing an AsyncClient request without await is not the taught asynchronous call. Reuse one client for the repeated shipping lookups, rather than constructing one for every loop iteration. Finishing a lookup is not cleanup; the owning scope still closes its client. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r02 · Try the contrast again: Async-compatible external HTTP requests
(definition) Use httpx.AsyncClient and await client.get(...), client.post(...) or another request method for an asynchronous outbound call. Reuse a scoped AsyncClient instead of creating clients inside a hot loop to benefit from connection pooling. Close a client with async with httpx.AsyncClient() as client or await client.aclose() at the end of its owning scope. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(example) Await the outbound lookup; writing an AsyncClient request without await is not the taught asynchronous call. Reuse one client for the repeated shipping lookups, rather than constructing one for every loop iteration. Finishing a lookup is not cleanup; the owning scope still closes its client. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧

=========

# EVALUATOR PACKET — Custom validation for domain invariants · Expected API failures with HTTPException (tile_026)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = pydantic.domain_validation — Custom validation for domain invariants
B = fastapi.expected_http_errors — Expected API failures with HTTPException

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (pydantic.domain_validation)   objective: Validate domain invariants: add one custom invariant validator.
A.f1: Use @model_validator(mode='after') on an instance method to check an invariant involving multiple already-validated fields.   [sources: pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/validators/#model-validators]
A.f2: An after-model validator raises ValueError when its invariant fails and returns self when validation succeeds.   [sources: pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/validators/#model-validators]
A.f3: Use @field_validator('field', mode='after') with a classmethod for a custom check on one validated field, returning the validated value when accepted.   [sources: pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/validators/#field-validators]
A.f4: Verify a cross-field rule with input that passes each individual field's validation but violates the model invariant, asserting that model construction raises ValidationError; also verify a consistent input is accepted.   [sources: pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/validators/#model-validators, pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/models/#error-handling]
note: Establish this first: Validity can depend on relationships among values.
note: Stay within the current objective: Validate domain invariants. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify cross-field validity requirements.
PRACTICE ANCHOR (live_code): Add one after-model invariant validator to a booking model with integer start and end fields, requiring end to be later than start.  SUCCESS: The validator raises ValueError when end is not later than start and returns self otherwise. Model construction with start=5 and end=3 raises ValidationError, while start=3 and end=5 is accepted.
ASSESSMENT ANCHOR: distinguish_cross_field_invariants_from_single_field_checks facts=['f1', 'f3']
ASSESSMENT ANCHOR: identify_after_model_invariant_validation_requirements facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_inputs_that_isolate_cross_field_validity facts=['f4']

## SOURCE FACTS — B (fastapi.expected_http_errors)   objective: Raise expected HTTP failures: implement one HTTPException rejection.
B.f1: Raise HTTPException(status_code=..., detail=...) to stop the operation and return a deliberate HTTP rejection rather than returning the exception object.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/handling-errors/#use-httpexception]
B.f2: HTTPException accepts headers for required response metadata, such as an authentication challenge.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/handling-errors/#add-custom-headers]
B.f3: FastAPI's default HTTPException response contains the supplied detail under the JSON key detail.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/handling-errors/#the-resulting-response]
note: Establish this first: Expected failure is controlled protocol output.
note: Stay within the current objective: Raise expected HTTP failures. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine deliberate rejection responses.
PRACTICE ANCHOR (live_code): Implement one HTTPException rejection in a supplied order operation when the order is absent.  SUCCESS: The absent-order branch raises HTTPException with status_code=404 and a client-facing detail, stopping before the normal return. The default rejection body contains the supplied message under detail.
ASSESSMENT ANCHOR: determine_deliberate_rejection_control_flow facts=['f1']
ASSESSMENT ANCHOR: determine_default_rejection_body facts=['f3']
ASSESSMENT ANCHOR: identify_required_rejection_headers facts=['f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Binding request bodies to typed models; Bounded form and multipart file inputs; Bounded in-process background work and nondurable delivery limits; CORS origin and credential policy; Choosing def versus async def from I/O behavior without blocking the event loop; Composing request dependency graphs; Configuring existing middleware in the request/response stack; Credential and sensitive-data redaction from emitted logs; Depends; Endpoint integration tests using TestClient or async HTTPX as appropriate; Expected API failures with HTTPException; FastAPI OpenAPI generation from typed route contracts; Graceful termination and shutdown verification; Modular FastAPI application composition with APIRouter; Outbound timeouts; Preventing unsafe outbound requests and SSRF; Production ASGI serving versus development reload; Request-scoped async-compatible PostgreSQL session lifecycle; Request-scoped dependency reuse and lifetime; Required, optional and default input semantics; Response-model serialization and private-field exclusion; Separating transport, testable business logic and persistence responsibilities; Structured service request and error logs; Trusted host validation; Typed path and 

## LESSON, in learner order

### s01 · explainer · The rule: Custom validation for domain invariants
(definition) Choose @model_validator(mode='after') on an instance method to check an invariant involving multiple already-validated fields. ⟦A.f1 A:tb2⟧
(mechanism) An after-model validator raises ValueError when its invariant fails and returns self when validation succeeds. Use @field_validator('field', mode='after') with a classmethod for a custom check on one validated field, returning the validated value when accepted. Verify a cross-field rule with input that passes each individual field's validation but violates the model invariant, asserting that model construction raises ValidationError; also verify a consistent input is accepted. ⟦A.f2 A.f3 A.f4 A:tb3⟧
[CODE python]
from pydantic import BaseModel, model_validator, ValidationError

class Booking(BaseModel):
    start: int
    end: int
    @model_validator(mode='after')
    def validate_booking(self):
        if self.end <= self.start:
            raise ValueError('end must be later than start')
        return self

# checks.py
from pydantic import ValidationError

cases = [{'start': 5, 'end': 3}, {'start': 3, 'end': 3}, {'start': 3, 'end': 5}]
for values in cases:
    if values['end'] <= values['start']:
        try:
            Booking(**values)
        except ValidationError:
            pass
        else:
            raise AssertionError('Inconsistent pair was accepted')
    else:
        booking = Booking(**values)
        assert booking.start == values['start'] and booking.end == values['end']

  annotations: ['For the booking rule, end must be later than start. Use individually valid values that violate that relationship to isolate the invariant. An after-model instance validator raises ValueError on failure; construction then raises ValidationError. A consistent pair succeeds and the validator returns self. For a custom single-field check, use an after-field classmethod validator and return the accepted value.']

### s02 · explainer · Trace the boundary: Custom validation for domain invariants
(walkthrough) For the booking rule, end must be later than start. Use individually valid values that violate that relationship to isolate the invariant. An after-model instance validator raises ValueError on failure; construction then raises ValidationError. A consistent pair succeeds and the validator returns self. For a custom single-field check, use an after-field classmethod validator and return the accepted value. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · video · Custom validation for domain invariants
[VIDEO ] bridge-before:  | bridge-after: 

### s04 · check · Choose the distinction: Custom validation for domain invariants
Check your understanding — Use the declared contract to distinguish the outcomes.

### s05 · check · Choose the distinction: Custom validation for domain invariants
Check your understanding — Use the declared contract to distinguish the outcomes.

### s06 · hands_on · Practice: Custom validation for domain invariants
Apply the contract — Work in the supplied orders-service exercise snapshot.

### s07 · explainer · The rule: Expected API failures with HTTPException
(definition) Raise HTTPException(status_code=..., detail=...) to stop the operation and return a deliberate HTTP rejection rather than returning the exception object. ⟦B.f1 B:tb2⟧
(mechanism) HTTPException accepts headers for required response metadata, such as an authentication challenge. FastAPI's default HTTPException response contains the supplied detail under the JSON key detail. ⟦B.f2 B.f3 B:tb3⟧
(walkthrough) At the absent-order branch, raise HTTPException with the intended status and client-facing detail. The raise stops normal operation work and produces a deliberate HTTP rejection; returning the exception object is different. FastAPI puts the supplied detail under the default JSON key detail. Supply headers when the rejection requires metadata, such as an authentication challenge. ⟦B.f1 B.f2 B.f3 B:tb4⟧
[CODE python]
from fastapi import FastAPI, HTTPException
app = FastAPI()
order = None

@app.get("/order")
def get_order():
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

  annotations: ['At the absent-order branch, raise HTTPException with the intended status and client-facing detail. The raise stops normal operation work and produces a deliberate HTTP rejection; returning the exception object is different. FastAPI puts the supplied detail under the default JSON key detail. Supply headers when the rejection requires metadata, such as an authentication challenge.']

### s08 · explainer · Trace the boundary: Expected API failures with HTTPException
(walkthrough) At the absent-order branch, raise HTTPException with the intended status and client-facing detail. The raise stops normal operation work and produces a deliberate HTTP rejection; returning the exception object is different. FastAPI puts the supplied detail under the default JSON key detail. Supply headers when the rejection requires metadata, such as an authentication challenge. ⟦B.f1 B.f2 B.f3 B:tb5 B:tb6⟧

### s09 · check · Choose the distinction: Expected API failures with HTTPException
Check your understanding — Use the declared contract to distinguish the outcomes.

### s10 · check · Choose the distinction: Expected API failures with HTTPException
Check your understanding — Use the declared contract to distinguish the outcomes.

### s11 · hands_on · Practice: Expected API failures with HTTPException
Apply the contract — Work in the supplied orders-service exercise snapshot.

### s12 · recap · Keep these boundaries
(takeaway) A cross-field rule is not proved by an input that already fails individual field validation. Isolate the invariant with individually valid values. ⟦A.f4 A:tb5⟧
(takeaway) Raise HTTPException rather than returning it. The default body puts the supplied information under detail, not under an arbitrary invented key. ⟦B.f1 B.f3 B:tb6⟧
[UP NEXT] Choosing def versus async def from I/O behavior without blocking the event loop: Next: Choosing def versus async def from I/O behavior without blocking the event loop.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast again: Custom validation for domain invariants
(definition) Use @model_validator(mode='after') on an instance method to check an invariant involving multiple already-validated fields. Use @field_validator('field', mode='after') with a classmethod for a custom check on one validated field, returning the validated value when accepted. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4⟧
(example) The booking start/end relationship is a model invariant, not just a check on one field. A one-field after validator returns its accepted value; an after-model validator returns self. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4⟧
### r02 · Try the contrast again: Custom validation for domain invariants
(definition) Verify a cross-field rule with input that passes each individual field's validation but violates the model invariant, asserting that model construction raises ValidationError; also verify a consistent input is accepted. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(example) Compare a booking with end before start against one with end later than start; both inputs must first satisfy their field types. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
### r03 · Try the contrast again: Custom validation for domain invariants
(definition) Use @model_validator(mode='after') on an instance method to check an invariant involving multiple already-validated fields. An after-model validator raises ValueError when its invariant fails and returns self when validation succeeds. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4⟧
(example) The booking start/end relationship is a model invariant, not just a check on one field. The failing booking branch raises ValueError; the successful branch returns self. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4⟧
### r04 · Try the contrast again: Expected API failures with HTTPException
(definition) Raise HTTPException(status_code=..., detail=...) to stop the operation and return a deliberate HTTP rejection rather than returning the exception object. ⟦B.f1 B:tb2 B:tb4 B:tb5 B:tb6⟧
(example) Raise at the absent-order branch rather than returning the exception object. ⟦B.f1 B:tb2 B:tb4 B:tb5 B:tb6⟧
### r05 · Try the contrast again: Expected API failures with HTTPException
(definition) HTTPException accepts headers for required response metadata, such as an authentication challenge. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(example) Put required rejection metadata in headers, not just in the detail message. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
### r06 · Try the contrast again: Expected API failures with HTTPException
(definition) FastAPI's default HTTPException response contains the supplied detail under the JSON key detail. ⟦B.f3 B:tb3 B:tb4 B:tb5 B:tb6⟧
(example) For the absent-order rejection, the default body key is detail, not an invented key. ⟦B.f3 B:tb3 B:tb4 B:tb5 B:tb6⟧

=========

# EVALUATOR PACKET — Choosing def versus async def from I/O behavior without blocking the event loop (tile_028)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.handler_execution_choice — Choosing def versus async def from I/O behavior without blocking the event loop

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (fastapi.handler_execution_choice)   objective: Choose handler execution without blocking the event loop: choose and verify the handler execution mode for one I/O operation.
A.f1: Use async def and await for an I/O library with awaitable operations; use a normal def handler for a blocking I/O library.   [sources: fastapi_docs_async#https://fastapi.tiangolo.com/async/#in-a-hurry]
A.f2: FastAPI runs a normal def path operation in an external thread pool, whereas an async def path operation runs as asynchronous execution.   [sources: fastapi_docs_async#https://fastapi.tiangolo.com/async/#path-operation-functions]
A.f3: FastAPI does not automatically move ordinary utility functions called directly by a handler to a thread pool; a blocking call inside async def can block the event loop.   [sources: fastapi_docs_async#https://fastapi.tiangolo.com/async/#other-utility-functions]
note: Establish this first: Cooperative event-loop work must yield; blocking calls require an appropriate execution boundary..
note: Stay within the current objective: Choose handler execution without blocking the event loop. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify whether a library call belongs in async execution or a threadpool-backed handler.
PRACTICE ANCHOR (live_code): Choose the handler execution mode for a supplied blocking shipping-client operation, then verify the choice by tracing where the handler and its directly called utility execute.  SUCCESS: The path operation uses normal def, calls the supplied blocking operation without await, and returns its result. The execution trace places the handler and its direct utility call in FastAPI’s external thread pool rather than on the event loop.
ASSESSMENT ANCHOR: select_handler_execution_for_library_io facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_blocking_io_inside_async_execution facts=['f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Binding request bodies to typed models; Bounded form and multipart file inputs; Bounded in-process background work and nondurable delivery limits; CORS origin and credential policy; Composing request dependency graphs; Configuring existing middleware in the request/response stack; Credential and sensitive-data redaction from emitted logs; Depends; Endpoint integration tests using TestClient or async HTTPX as appropriate; FastAPI OpenAPI generation from typed route contracts; Graceful termination and shutdown verification; Modular FastAPI application composition with APIRouter; Outbound timeouts; Preventing unsafe outbound requests and SSRF; Production ASGI serving versus development reload; Request-scoped async-compatible PostgreSQL session lifecycle; Request-scoped dependency reuse and lifetime; Required, optional and default input semantics; Response-model serialization and private-field exclusion; Separating transport, testable business logic and persistence responsibilities; Service health and readiness checks; Structured service request and error logs; Trusted host validation; Typed path and query input binding; Yield-based dependency cleanup

## LESSON, in learner order

### s01 · explainer · The rule: Choosing def versus async def from I/O behavior without blocking the event loop
(definition) Choose async def and await for an I/O library with awaitable operations; use a normal def handler for a blocking I/O library. ⟦A.f1 A:tb2⟧
(mechanism) FastAPI runs a normal def path operation in an external thread pool, whereas an async def path operation runs as asynchronous execution. FastAPI does not automatically move ordinary utility functions called directly by a handler to a thread pool; a blocking call inside async def can block the event loop. ⟦A.f2 A.f3 A:tb3⟧
[DIAGRAM] nodes=['Awaitable I/O library', 'async def handler + await', 'Blocking I/O library', 'def path operation: external thread pool', 'async def → directly called blocking utility'] edges=[('n0', 'n1', 'awaitable execution'), ('n2', 'n3', 'choose normal def handler'), ('n2', 'n4', 'not automatically offloaded; can block event loop')] alt: Make three execution paths visible: an async def handler awaiting an awaitable shipping operation on the event loop; a normal def handler performing blocking shipping I/O in the external thread pool; and an async def handler directly calling a blocking utility that remains on and can block the event loop.

### s02 · explainer · Trace the boundary: Choosing def versus async def from I/O behavior without blocking the event loop
(walkthrough) Match the handler to the I/O library. Awaitable operations fit async def with await. Blocking I/O fits a normal def path operation, which FastAPI runs in an external thread pool. Moving a blocking call into a directly called helper does not automatically offload it: inside async def, that call can block the event loop. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · video · Choosing def versus async def from I/O behavior without blocking the event loop
[VIDEO ] bridge-before:  | bridge-after: 

### s04 · check · Choose the distinction: Choosing def versus async def from I/O behavior without blocking the event loop
Check your understanding — Use the declared contract to distinguish the outcomes.

### s05 · hands_on · Practice: Choosing def versus async def from I/O behavior without blocking the event loop
Apply the contract — Work in the supplied orders-service exercise snapshot.

### s06 · recap · Keep these boundaries
(takeaway) FastAPI's handling of normal def path operations does not apply automatically to ordinary utility calls made directly inside an async handler. ⟦A.f3 A:tb5⟧
[UP NEXT] Modular FastAPI application composition with APIRouter: Next: Modular FastAPI application composition with APIRouter.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast again: Choosing def versus async def from I/O behavior without blocking the event loop
(definition) FastAPI runs a normal def path operation in an external thread pool, whereas an async def path operation runs as asynchronous execution. FastAPI does not automatically move ordinary utility functions called directly by a handler to a thread pool; a blocking call inside async def can block the event loop. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
(example) A normal def path operation is run in the external thread pool; async def uses asynchronous execution. Moving shipping_client.lookup into a directly called helper does not automatically offload it from an async handler. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast again: Choosing def versus async def from I/O behavior without blocking the event loop
(definition) Use async def and await for an I/O library with awaitable operations; use a normal def handler for a blocking I/O library. FastAPI runs a normal def path operation in an external thread pool, whereas an async def path operation runs as asynchronous execution. FastAPI does not automatically move ordinary utility functions called directly by a handler to a thread pool; a blocking call inside async def can block the event loop. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) The supplied shipping client blocks: choose a normal def path operation, not async def merely by spelling. A normal def path operation is run in the external thread pool; async def uses asynchronous execution. Moving shipping_client.lookup into a directly called helper does not automatically offload it from an async handler. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Modular FastAPI application composition with APIRouter (tile_029)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.modular_application — Modular FastAPI application composition with APIRouter

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (fastapi.modular_application)   objective: Compose routers: assemble one service from feature routers.
A.f1: Create an APIRouter for a feature's operations and register those operations on that router rather than requiring all handlers to live in the main module.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter]
A.f2: Import feature routers and call app.include_router(router) to assemble their operations into the application.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-the-apirouters-for-users-and-items]
A.f3: An include_router prefix adds to the included operations' paths, and tags, dependencies and responses can be supplied at inclusion.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies]
note: Establish this first: Feature organization differs from application assembly.
note: Stay within the current objective: Compose routers. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine namespaces after inclusion.
PRACTICE ANCHOR (live_code): Assemble an orders service by registering its operation on a feature router, importing that router into the application assembly module, and including it with an /api prefix.  SUCCESS: The orders operation is registered on the feature router, the application imports and includes that router, and the local /orders path becomes /api/orders.
ASSESSMENT ANCHOR: determine_included_operation_paths facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: distinguish_feature_registration_from_application_inclusion facts=['f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Binding request bodies to typed models; Bounded form and multipart file inputs; Bounded in-process background work and nondurable delivery limits; CORS origin and credential policy; Composing request dependency graphs; Configuring existing middleware in the request/response stack; Credential and sensitive-data redaction from emitted logs; Depends; Endpoint integration tests using TestClient or async HTTPX as appropriate; FastAPI OpenAPI generation from typed route contracts; Graceful termination and shutdown verification; Meaningful contract examples and operation metadata; Outbound timeouts; Preventing unsafe outbound requests and SSRF; Production ASGI serving versus development reload; Request-scoped async-compatible PostgreSQL session lifecycle; Request-scoped dependency reuse and lifetime; Required, optional and default input semantics; Response-model serialization and private-field exclusion; Separating transport, testable business logic and persistence responsibilities; Service health and readiness checks; Structured service request and error logs; Trusted host validation; Typed path and query input binding; Yield-based dependency cleanup

## LESSON, in learner order

### s01 · explainer · The rule: Modular FastAPI application composition with APIRouter
(definition) Create an APIRouter for a feature's operations and register those operations on that router rather than requiring all handlers to live in the main module. ⟦A.f1 A:tb2⟧
(mechanism) Import feature routers and call app.include_router(router) to assemble their operations into the application. An include_router prefix adds to the included operations' paths, and tags, dependencies and responses can be supplied at inclusion. ⟦A.f2 A.f3 A:tb3⟧
[CODE python]
# orders.py
from fastapi import APIRouter
router = APIRouter()
@router.get('/orders')
def list_orders():
    return []

# main.py
from fastapi import FastAPI
app = FastAPI()
from orders import router
app.include_router(router, prefix='/api')

  annotations: ['Register feature operations on an APIRouter, then import and include it in the application assembly module. Defining the router alone does not assemble it. Including a local /orders operation with prefix /api produces /api/orders. The include point can also supply tags, dependencies, and responses.']

### s02 · explainer · Trace the boundary: Modular FastAPI application composition with APIRouter
(walkthrough) Register feature operations on an APIRouter, then import and include it in the application assembly module. Defining the router alone does not assemble it. Including a local /orders operation with prefix /api produces /api/orders. The include point can also supply tags, dependencies, and responses. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · video · Modular FastAPI application composition with APIRouter
[VIDEO ] bridge-before:  | bridge-after: 

### s04 · check · Choose the distinction: Modular FastAPI application composition with APIRouter
Check your understanding — Use the declared contract to distinguish the outcomes.

### s05 · hands_on · Practice: Modular FastAPI application composition with APIRouter
Apply the contract — Work in the supplied orders-service exercise snapshot.

### s06 · recap · Keep these boundaries
(takeaway) Defining a router is not the same as including it in the application. Trace include_router and any prefix it adds. ⟦A.f2 A.f3 A:tb5⟧
[UP NEXT] Typed path and query input binding: Next: Typed path and query input binding.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast again: Modular FastAPI application composition with APIRouter
(definition) Import feature routers and call app.include_router(router) to assemble their operations into the application. An include_router prefix adds to the included operations' paths, and tags, dependencies and responses can be supplied at inclusion. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
(example) An orders router definition alone is not assembly; the application must include it. The local /orders path plus inclusion prefix /api gives /api/orders, not the unchanged local path. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast again: Modular FastAPI application composition with APIRouter
(definition) Create an APIRouter for a feature's operations and register those operations on that router rather than requiring all handlers to live in the main module. Import feature routers and call app.include_router(router) to assemble their operations into the application. An include_router prefix adds to the included operations' paths, and tags, dependencies and responses can be supplied at inclusion. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Register orders operations on the feature router, rather than requiring the main module to contain every handler. An orders router definition alone is not assembly; the application must include it. The local /orders path plus inclusion prefix /api gives /api/orders, not the unchanged local path. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Typed path and query input binding · Response-model serialization and private-field exclusion (tile_030)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.path_query_binding — Typed path and query input binding
B = fastapi.response_model_serialization — Response-model serialization and private-field exclusion

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (fastapi.path_query_binding)   objective: Declare typed URL inputs: declare one handler's URL inputs.
A.f1: Put a name in the route path as {name} and declare name: Type in the handler to bind and convert that path value.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/path-params/#path-parameters-with-types]
A.f2: Handler parameters not present in the path are interpreted as query parameters when they are ordinary scalar types.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/query-params/#query-parameters]
A.f3: A query parameter with a default may be omitted, while a parameter without a default is required; the type controls conversion of a supplied string.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/query-params/#defaults, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/query-params/#required-query-parameters]
A.f4: A path value that cannot be converted to its declared type produces a validation error instead of invoking the handler with that unconverted value.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/path-params/#data-validation]
note: Establish this first: Declarations bind URL strings to typed arguments.
note: Stay within the current objective: Declare typed URL inputs. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine requiredness and conversion.
PRACTICE ANCHOR (live_code): Declare one handler for /orders/{order_id} with an integer path input order_id and an integer query input limit that defaults to 10.  SUCCESS: The route placeholder and handler argument share the name order_id. Both inputs are annotated as int, and limit has a default of 10 without appearing in the path.
ASSESSMENT ANCHOR: determine_path_and_query_binding facts=['f1', 'f2']
ASSESSMENT ANCHOR: determine_query_requiredness_and_conversion facts=['f3']
ASSESSMENT ANCHOR: determine_path_conversion_and_rejection facts=['f1', 'f4']

## SOURCE FACTS — B (fastapi.response_model_serialization)   objective: Serialize public responses: project one internal object.
B.f1: Set response_model=PublicModel on the operation decorator to validate, serialize and filter the returned value to that public model.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/response-model/#response-model-parameter]
B.f2: Define the output model without private fields so those fields are not returned merely because they exist on the internal object.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/response-model/#add-an-output-model]
B.f3: When both a return annotation and response_model are supplied, response_model takes priority for FastAPI's response processing.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/response-model/#response-model-priority]
B.f4: Returning a Response object directly bypasses automatic response-model conversion and filtering, so the application is responsible for that content.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/response-model/#return-a-response-directly]
note: Establish this first: Response schemas allowlist output.
note: Stay within the current objective: Serialize public responses. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine publicly projected fields.
PRACTICE ANCHOR (live_code): Define PublicOrder with only the intended public order fields and configure an operation to project one internal order dictionary through response_model=PublicOrder, excluding its private processing note.  SUCCESS: The operation returns the internal dictionary through normal response-model processing. Its public response contains only the fields declared in PublicOrder and excludes private_processing_note.
ASSESSMENT ANCHOR: determine_publicly_projected_fields facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_response_model_priority_over_return_annotation facts=['f3']
ASSESSMENT ANCHOR: recognize_direct_response_filtering_bypass facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Binding request bodies to typed models; Bounded form and multipart file inputs; Bounded in-process background work and nondurable delivery limits; CORS origin and credential policy; Composing request dependency graphs; Configuring existing middleware in the request/response stack; Credential and sensitive-data redaction from emitted logs; Depends; Endpoint integration tests using TestClient or async HTTPX as appropriate; FastAPI OpenAPI generation from typed route contracts; Graceful termination and shutdown verification; Header and cookie input binding; Meaningful contract examples and operation metadata; Outbound timeouts; Preventing unsafe outbound requests and SSRF; Production ASGI serving versus development reload; Request-scoped async-compatible PostgreSQL session lifecycle; Request-scoped dependency reuse and lifetime; Required, optional and default input semantics; Response-model serialization and private-field exclusion; Separating transport, testable business logic and persistence responsibilities; Service health and readiness checks; Structured service request and error logs; Test dependency replacement; Trusted host validation; Yield-based dependency cleanup

## LESSON, in learner order

### s01 · explainer · The rule: Typed path and query input binding
(definition) Put a name in the route path as {name} and declare name: Type in the handler to bind and convert that path value. ⟦A.f1 A:tb2⟧
(mechanism) Handler parameters not present in the path are interpreted as query parameters when they are ordinary scalar types. A query parameter with a default may be omitted, while a parameter without a default is required; the type controls conversion of a supplied string. A path value that cannot be converted to its declared type produces a validation error instead of invoking the handler with that unconverted value. ⟦A.f2 A.f3 A.f4 A:tb3⟧
[CODE python]
from fastapi import FastAPI
app = FastAPI()

@app.get("/orders/{order_id}")
def read_order(order_id: int, limit: int = 5):
    return {"order_id": order_id, "limit": limit}

  annotations: ['In /orders/{order_id}, declare order_id: int to bind and convert the path value. An ordinary scalar limit outside the path binds from the query. A default permits omission; no default makes it required. A nonconvertible path value fails validation instead of reaching the handler unconverted. Source, conversion, and omission are separate decisions.']

### s02 · explainer · Trace the boundary: Typed path and query input binding
(walkthrough) In /orders/{order_id}, declare order_id: int to bind and convert the path value. An ordinary scalar limit outside the path binds from the query. A default permits omission; no default makes it required. A nonconvertible path value fails validation instead of reaching the handler unconverted. Source, conversion, and omission are separate decisions. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧

### s03 · explainer · Trace the boundary: Typed path and query input binding
(walkthrough) In /orders/{order_id}, declare order_id: int to bind and convert the path value. An ordinary scalar limit outside the path binds from the query. A default permits omission; no default makes it required. A nonconvertible path value fails validation instead of reaching the handler unconverted. Source, conversion, and omission are separate decisions. ⟦A.f1 A.f2 A.f3 A.f4 A:tb5 A:tb6⟧

### s04 · video · Typed path and query input binding
[VIDEO ] bridge-before:  | bridge-after: 

### s05 · check · Choose the distinction: Typed path and query input binding
Check your understanding — Use the declared contract to distinguish the outcomes.

### s06 · check · Choose the distinction: Typed path and query input binding
Check your understanding — Use the declared contract to distinguish the outcomes.

### s07 · hands_on · Practice: Typed path and query input binding
Apply the contract — Work in the supplied orders-service exercise snapshot.

### s08 · explainer · The rule: Response-model serialization and private-field exclusion
(definition) Set response_model=PublicModel on the operation decorator to validate, serialize and filter the returned value to that public model. ⟦B.f1 B:tb2⟧
(mechanism) Define the output model without private fields so those fields are not returned merely because they exist on the internal object. When both a return annotation and response_model are supplied, response_model takes priority for FastAPI's response processing. Returning a Response object directly bypasses automatic response-model conversion and filtering, so the application is responsible for that content. ⟦B.f2 B.f3 B.f4 B:tb3⟧
[CODE python]
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
internal_order = {'order_id': 42, 'status': 'pending', 'private_processing_note': 'synthetic internal note 1'}

class PublicOrder(BaseModel):
    order_id: int
    status: str

@app.get("/orders/{order_id}", response_model=PublicOrder)
def read_order(order_id: int):
    return internal_order

  annotations: ['PublicOrder lists intended public fields, leaving out the internal private processing note. Set response_model=PublicOrder to validate, serialize, and filter a normally returned value. response_model takes priority over a return annotation. Inspect the return form too: returning a Response directly bypasses automatic model conversion and filtering, leaving its content to the application.']

### s09 · explainer · Trace the boundary: Response-model serialization and private-field exclusion
(walkthrough) PublicOrder lists intended public fields, leaving out the internal private processing note. Set response_model=PublicOrder to validate, serialize, and filter a normally returned value. response_model takes priority over a return annotation. Inspect the return form too: returning a Response directly bypasses automatic model conversion and filtering, leaving its content to the application. ⟦B.f1 B.f2 B.f3 B.f4 B:tb4⟧

### s10 · explainer · Trace the boundary: Response-model serialization and private-field exclusion
(walkthrough) PublicOrder lists intended public fields, leaving out the internal private processing note. Set response_model=PublicOrder to validate, serialize, and filter a normally returned value. response_model takes priority over a return annotation. Inspect the return form too: returning a Response directly bypasses automatic model conversion and filtering, leaving its content to the application. ⟦B.f1 B.f2 B.f3 B.f4 B:tb5 B:tb6⟧

### s11 · check · Choose the distinction: Response-model serialization and private-field exclusion
Check your understanding — Use the declared contract to distinguish the outcomes.

### s12 · check · Choose the distinction: Response-model serialization and private-field exclusion
Check your understanding — Use the declared contract to distinguish the outcomes.

### s13 · hands_on · Practice: Response-model serialization and private-field exclusion
Apply the contract — Work in the supplied orders-service exercise snapshot.

### s14 · recap · Keep these boundaries
(takeaway) A parameter's name alone does not make it a path input. It must occur in the path declaration; ordinary scalar inputs outside the path bind from the query. ⟦A.f1 A.f2 A:tb6⟧
(takeaway) A response model is not an automatic safety net for a directly returned Response object. That path bypasses its conversion and filtering. ⟦B.f4 B:tb6⟧
[UP NEXT] Depends: Next: Depends.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast again: Typed path and query input binding
(definition) A query parameter with a default may be omitted, while a parameter without a default is required; the type controls conversion of a supplied string. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) Compare limit with a default against limit without one: omission is allowed only in the defaulted declaration. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast again: Typed path and query input binding
(definition) Put a name in the route path as {name} and declare name: Type in the handler to bind and convert that path value. A path value that cannot be converted to its declared type produces a validation error instead of invoking the handler with that unconverted value. ⟦A.f1 A.f4 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(example) order_id occurs in the path placeholder; limit does not. A nonconvertible order_id stops at validation; it does not enter the handler as the original string. ⟦A.f1 A.f4 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r03 · Try the contrast again: Typed path and query input binding
(definition) Put a name in the route path as {name} and declare name: Type in the handler to bind and convert that path value. Handler parameters not present in the path are interpreted as query parameters when they are ordinary scalar types. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(example) order_id occurs in the path placeholder; limit does not. An ordinary scalar limit outside the path is a query input, not another path input. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r04 · Try the contrast again: Response-model serialization and private-field exclusion
(definition) Set response_model=PublicModel on the operation decorator to validate, serialize and filter the returned value to that public model. Define the output model without private fields so those fields are not returned merely because they exist on the internal object. ⟦B.f1 B.f2 B:tb2 B:tb3 B:tb4 B:tb5⟧
(example) A normally returned internal order is processed against PublicOrder, not serialized indiscriminately. The public fields omit private_processing_note even though the internal order contains it. ⟦B.f1 B.f2 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r05 · Try the contrast again: Response-model serialization and private-field exclusion
(definition) Returning a Response object directly bypasses automatic response-model conversion and filtering, so the application is responsible for that content. ⟦B.f4 B:tb3 B:tb4 B:tb5 B:tb6⟧
(example) A directly returned Response bypasses filtering; a normally returned internal order follows response-model processing. ⟦B.f4 B:tb3 B:tb4 B:tb5 B:tb6⟧
### r06 · Try the contrast again: Response-model serialization and private-field exclusion
(definition) When both a return annotation and response_model are supplied, response_model takes priority for FastAPI's response processing. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(example) If both are supplied, response_model wins over the return annotation, not the reverse. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧

=========

# EVALUATOR PACKET — Depends (tile_032)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi_backend.depends — Depends

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (fastapi_backend.depends)   objective: Inject service access with Depends: wire one endpoint to an authentication or database provider.
A.f1: Declare a handler input with Annotated[Type, Depends(provider)] to have FastAPI execute the provider and supply its returned value.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/#declare-the-dependency-in-the-dependant]
A.f2: Pass the provider callable to Depends rather than calling it in the declaration, so FastAPI can resolve its inputs.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/#declare-the-dependency-in-the-dependant]
A.f3: A dependency makes a handler's needed input explicit and can be reused by multiple operations for shared input-provision logic.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/#what-is-dependency-injection]
note: Establish this first: Dependencies supply explicit inputs without hidden globals.
note: Stay within the current objective: Inject service access with Depends. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine supplied handler context.
PRACTICE ANCHOR (live_code): Wire one order endpoint to a supplied demonstration authentication-context provider using Annotated[str, Depends(provider)], passing the provider callable rather than calling it.  SUCCESS: The order handler declares its context through Depends and returns the supplied string without calling the provider itself or reading a global context value.
ASSESSMENT ANCHOR: determine_provider_supplied_handler_context facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_explicit_shared_input_provision_logic facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Binding request bodies to typed models; Bounded form and multipart file inputs; Bounded in-process background work and nondurable delivery limits; CORS origin and credential policy; Composing request dependency graphs; Configuring existing middleware in the request/response stack; Credential and sensitive-data redaction from emitted logs; Endpoint integration tests using TestClient or async HTTPX as appropriate; FastAPI OpenAPI generation from typed route contracts; Graceful termination and shutdown verification; Header and cookie input binding; Meaningful contract examples and operation metadata; Outbound timeouts; Preventing unsafe outbound requests and SSRF; Production ASGI serving versus development reload; Request-scoped async-compatible PostgreSQL session lifecycle; Request-scoped dependency reuse and lifetime; Request-validation error behavior; Required, optional and default input semantics; Separating transport, testable business logic and persistence responsibilities; Service health and readiness checks; Structured service request and error logs; Test dependency replacement; Trusted host validation; Yield-based dependency cleanup

## LESSON, in learner order

### s01 · explainer · The rule: Depends
(definition) Declare a handler input with Annotated[Type, Depends(provider)] to have FastAPI execute the provider and supply its returned value. ⟦A.f1 A:tb2⟧
(mechanism) Pass the provider callable to Depends rather than calling it in the declaration, so FastAPI can resolve its inputs. A dependency makes a handler's needed input explicit and can be reused by multiple operations for shared input-provision logic. ⟦A.f2 A.f3 A:tb3⟧
[CODE python]
from typing import Annotated
from fastapi import FastAPI, Depends
app = FastAPI()

def provider() -> str:
    return "synthetic-auth-context-not-verified"

@app.get("/orders")
def orders(context: Annotated[str, Depends(provider)]):
    return {"context": context}

  annotations: ['Declare a typed parameter with Annotated[Type, Depends(provider)]. Pass the callable, not provider(). FastAPI resolves the provider and supplies its result before calling the operation. Another operation can declare the same provider for reusable input-provision logic. This is an explicit input, not an application-wide hidden value store.']

### s02 · explainer · Trace the boundary: Depends
(walkthrough) Declare a typed parameter with Annotated[Type, Depends(provider)]. Pass the callable, not provider(). FastAPI resolves the provider and supplies its result before calling the operation. Another operation can declare the same provider for reusable input-provision logic. This is an explicit input, not an application-wide hidden value store. ⟦A.f1 A.f2 A.f3 A:tb4⟧

### s03 · explainer · Trace the boundary: Depends
(walkthrough) Declare a typed parameter with Annotated[Type, Depends(provider)]. Pass the callable, not provider(). FastAPI resolves the provider and supplies its result before calling the operation. Another operation can declare the same provider for reusable input-provision logic. This is an explicit input, not an application-wide hidden value store. ⟦A.f1 A.f2 A.f3 A:tb5 A:tb6⟧

### s04 · video · Depends
[VIDEO ] bridge-before:  | bridge-after: 

### s05 · check · Choose the distinction: Depends
Check your understanding — Use the declared contract to distinguish the outcomes.

### s06 · hands_on · Practice: Depends
Apply the contract — Work in the supplied orders-service exercise snapshot.

### s07 · recap · Keep these boundaries
(takeaway) Depends(provider) passes a callable. Calling provider in the declaration would not express the same input-resolution instruction. ⟦A.f2 A:tb6⟧
[UP NEXT] Outbound timeouts: Next: Outbound timeouts.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast again: Depends
(definition) A dependency makes a handler's needed input explicit and can be reused by multiple operations for shared input-provision logic. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) Several order operations can declare the same provider; the needed input remains visible at each consumer. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast again: Depends
(definition) Declare a handler input with Annotated[Type, Depends(provider)] to have FastAPI execute the provider and supply its returned value. Pass the provider callable to Depends rather than calling it in the declaration, so FastAPI can resolve its inputs. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(example) Declare the provider-supplied context as a handler parameter, rather than calling provider in the operation. Depends(provider) passes the callable; Depends(provider()) calls it in the declaration instead. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧

=========

# EVALUATOR PACKET — Outbound timeouts (tile_033)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = integration.outbound_timeouts — Outbound timeouts

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (integration.outbound_timeouts)   objective: Bound the duration of an outbound HTTP call: configure and verify a finite timeout for one outbound operation.
A.f1: HTTPX distinguishes connect, read, write and pool timeouts; read and write limits bound waiting for individual chunks rather than a whole request's elapsed duration.   [sources: fastapi_docs_advanced#https://www.python-httpx.org/advanced/timeouts/#fine-tuning-the-configuration]
A.f2: Configure a finite timeout with httpx.AsyncClient(timeout=seconds) or a request's timeout= argument; timeout=None disables timeout enforcement.   [sources: fastapi_docs_advanced#https://www.python-httpx.org/advanced/timeouts/#setting-and-disabling-timeouts]
A.f3: HTTPX raises timeout exceptions such as ConnectTimeout, ReadTimeout, WriteTimeout and PoolTimeout when the corresponding wait exceeds its limit.   [sources: fastapi_docs_advanced#https://www.python-httpx.org/exceptions/#the-exception-hierarchy]
A.f4: When the contract requires a total elapsed-time budget across asynchronous work, wrap the operation in async with asyncio.timeout(seconds); its cancellation is converted to TimeoutError outside the context.   [sources: python_tutorial#https://docs.python.org/3/library/asyncio-task.html#timeouts]
note: Establish this first: An external operation consumes a finite local time budget..
note: Stay within the current objective: Bound the duration of an outbound HTTP call. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine the timeout outcome when an upstream fails to respond within the budget.
PRACTICE ANCHOR (live_code): Configure a finite HTTPX timeout for one asynchronous shipping lookup and verify the outcome against a supplied upstream that stalls before sending its response.  SUCCESS: The shipping lookup uses a finite timeout and returns a distinct timeout outcome when the supplied upstream exceeds the read-wait limit, rather than waiting indefinitely.
ASSESSMENT ANCHOR: determine_httpx_timeout_outcome_for_exceeded_wait facts=['f1', 'f3']
ASSESSMENT ANCHOR: distinguish_finite_io_limits_from_total_elapsed_budget facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_total_budget_timeout_outside_async_context facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Binding request bodies to typed models; Bounded form and multipart file inputs; Bounded in-process background work and nondurable delivery limits; CORS origin and credential policy; Composing request dependency graphs; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Configuring existing middleware in the request/response stack; Credential and sensitive-data redaction from emitted logs; Endpoint integration tests using TestClient or async HTTPX as appropriate; FastAPI OpenAPI generation from typed route contracts; Graceful termination and shutdown verification; Header and cookie input binding; Meaningful contract examples and operation metadata; Preventing unsafe outbound requests and SSRF; Production ASGI serving versus development reload; Request-scoped async-compatible PostgreSQL session lifecycle; Request-scoped dependency reuse and lifetime; Request-validation error behavior; Required, optional and default input semantics; Separating transport, testable business logic and persistence responsibilities; Service health and readiness checks; Structured service request and error logs; Test dep

## LESSON, in learner order

### s01 · explainer · The rule: Outbound timeouts
(definition) HTTPX distinguishes connect, read, write and pool timeouts; read and write limits bound waiting for individual chunks rather than a whole request's elapsed duration. ⟦A.f1 A:tb2⟧
(mechanism) Configure a finite timeout with httpx.AsyncClient(timeout=seconds) or a request's timeout= argument; timeout=None disables timeout enforcement. HTTPX raises timeout exceptions such as ConnectTimeout, ReadTimeout, WriteTimeout and PoolTimeout when the corresponding wait exceeds its limit. When the contract requires a total elapsed-time budget across asynchronous work, wrap the operation in async with asyncio.timeout(seconds); its cancellation is converted to TimeoutError outside the context. ⟦A.f2 A.f3 A.f4 A:tb3⟧
[DIAGRAM] nodes=['Connect wait: ConnectTimeout', 'Pool wait: PoolTimeout', 'Read chunk wait: ReadTimeout', 'Write chunk wait: WriteTimeout', 'Total asynchronous elapsed budget: asyncio.timeout', 'TimeoutError outside context'] edges=[('n0', 'n4', 'distinct wait and total boundaries'), ('n2', 'n2', 'successive chunks: each wait can fit; total can exceed read limit'), ('n4', 'n5', 'cancellation converted outside context')] alt: Make the shipping lookup's connect, pool, read and write wait boundaries visible alongside a separate total elapsed-time boundary. Show that successive chunks can each arrive within the read limit while total elapsed time exceeds that limit, and distinguish HTTPX timeout exceptions from TimeoutError outside asyncio.timeout.

### s02 · explainer · Trace the boundary: Outbound timeouts
(walkthrough) Configure a finite HTTPX timeout for the shipping lookup. Connect, pool, read, and write have distinct waits; read and write limits apply to individual chunks, not total elapsed time. Timely successive chunks can still extend total duration. For a total budget, use async with asyncio.timeout(seconds) and catch TimeoutError outside the context. Keep that separate from HTTPX timeout exceptions; timeout=None disables enforcement. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Choose the distinction: Outbound timeouts
Check your understanding — Use the declared contract to distinguish the outcomes.

### s04 · check · Choose the distinction: Outbound timeouts
Check your understanding — Use the declared contract to distinguish the outcomes.

### s05 · hands_on · Practice: Outbound timeouts
Apply the contract — Work in the supplied orders-service exercise snapshot.

### s06 · recap · Keep these boundaries
(takeaway) HTTPX read and write timeouts are not whole-request elapsed deadlines. Also, timeout=None disables timeout enforcement. ⟦A.f1 A.f2 A:tb5⟧
[UP NEXT] Separating transport, testable business logic and persistence responsibilities: Next: Separating transport, testable business logic and persistence responsibilities.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast again: Outbound timeouts
(definition) HTTPX distinguishes connect, read, write and pool timeouts; read and write limits bound waiting for individual chunks rather than a whole request's elapsed duration. Configure a finite timeout with httpx.AsyncClient(timeout=seconds) or a request's timeout= argument; timeout=None disables timeout enforcement. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Repeated timely chunks can satisfy the read wait limit while total shipping-lookup duration keeps growing. A finite shipping timeout bounds waits; timeout=None disables enforcement. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast again: Outbound timeouts
(definition) When the contract requires a total elapsed-time budget across asynchronous work, wrap the operation in async with asyncio.timeout(seconds); its cancellation is converted to TimeoutError outside the context. ⟦A.f4 A:tb3 A:tb4⟧
(example) Catch the total-budget TimeoutError outside asyncio.timeout, rather than treating it as an HTTPX ReadTimeout. ⟦A.f4 A:tb3 A:tb4⟧
### r03 · Try the contrast again: Outbound timeouts
(definition) HTTPX distinguishes connect, read, write and pool timeouts; read and write limits bound waiting for individual chunks rather than a whole request's elapsed duration. HTTPX raises timeout exceptions such as ConnectTimeout, ReadTimeout, WriteTimeout and PoolTimeout when the corresponding wait exceeds its limit. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Repeated timely chunks can satisfy the read wait limit while total shipping-lookup duration keeps growing. A stalled read chunk corresponds to ReadTimeout; an exceeded connect wait corresponds to ConnectTimeout. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Separating transport, testable business logic and persistence responsibilities · Bounded in-process background work and nondurable delivery limits · Composing request dependency graphs (tile_034)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = design.backend_separation_of_concerns — Separating transport, testable business logic and persistence responsibilities
B = fastapi.bounded_background_tasks — Bounded in-process background work and nondurable delivery limits
C = fastapi.dependency_composition — Composing request dependency graphs

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (design.backend_separation_of_concerns)   objective: Separate service responsibilities: refactor one endpoint into boundaries.
A.f1: A dependency can extract reusable input-provision logic from individual operation handlers and expose the supplied value as a declared handler parameter.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/#what-is-dependency-injection]
A.f2: Transport handlers adapt HTTP inputs and outputs, business callables enforce application rules, and persistence adapters access stored state; separate these responsibilities so each can change without embedding the other responsibilities.   [sources: fastapi_docs_advanced#https://www.cosmicpython.com/book/chapter_04_service_layer.html#_a_typical_service_function, fastapi_docs_advanced#https://www.cosmicpython.com/book/chapter_04_service_layer.html#_wrap_up]
A.f3: Move a business decision from a handler into a plain callable with explicit inputs, keep the HTTP adaptation in the handler, and call a separate persistence adapter for stored state rather than treating separate files alone as a responsibility boundary.   [sources: fastapi_docs_advanced#https://www.cosmicpython.com/book/chapter_04_service_layer.html#_a_typical_service_function, fastapi_docs_advanced#https://www.cosmicpython.com/book/chapter_04_service_layer.html#_wrap_up]
note: Establish this first: Layers isolate reasons to change rather than just files.
note: Stay within the current objective: Separate service responsibilities. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify misplaced logic and protocol coupling.
PRACTICE ANCHOR (live_code): Refactor a supplied order endpoint so the handler retains HTTP adaptation, a plain callable receives explicit inputs and makes the existing order decision, and a separate supplied persistence adapter accesses stored state. Expose reusable input provisioning through a declared dependency parameter.  SUCCESS: The endpoint preserves its supplied behavior while the business callable can be called directly with ordinary Python values. HTTP adaptation stays in the handler, stored-state access stays in the adapter, and reusable input provisioning is declared as a dependency parameter.
ASSESSMENT ANCHOR: identify_reusable_input_provisioning facts=['f1']
ASSESSMENT ANCHOR: identify_misplaced_transport_business_and_persistence_logic facts=['f2']
ASSESSMENT ANCHOR: identify_protocol_coupling_and_responsibility_boundaries facts=['f2', 'f3']

## SOURCE FACTS — B (fastapi.bounded_background_tasks)   objective: Choose suitable background work: choose one deferred operation's location.
B.f1: Declare a BackgroundTasks handler parameter and call background_tasks.add_task(callable, *args, **kwargs) to schedule work after sending the response.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/background-tasks/#using-backgroundtasks]
B.f2: A background task callable can be a normal def or async def function; FastAPI handles either form.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/background-tasks/#create-a-task-function]
B.f3: BackgroundTasks work runs in the application process and cannot guarantee survival or delivery when that process fails.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/background-tasks/#caveat]
note: Establish this first: In-process tasks cannot guarantee survival or delivery.
note: Stay within the current objective: Choose suitable background work. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Distinguish bounded tasks from durable execution needs.
PRACTICE ANCHOR (live_code): Choose where a small, optional order follow-up belongs when its contract permits loss on process failure, and schedule it after the response using BackgroundTasks.  SUCCESS: The handler registers the supplied follow-up callable without calling it immediately, returns the order response, and the learner identifies that this placement would not satisfy a guaranteed-completion requirement.
ASSESSMENT ANCHOR: distinguish_bounded_in_process_work_from_durable_execution_needs facts=['f3']

## SOURCE FACTS — C (fastapi.dependency_composition)   objective: Compose subdependencies: compose one provider graph.
C.f1: A provider can declare its own Annotated[Type, Depends(other_provider)] parameter, forming a dependency graph.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/#second-dependency-dependable-and-dependant]
C.f2: FastAPI resolves a provider's prerequisite inputs before calling that provider and supplies its result to the consuming operation.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/#use-the-dependency]
C.f3: A sub-dependency can declare typed query inputs of its own; those inputs are extracted from the request before its returned value is supplied to the dependent provider.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/#first-dependency-dependable, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/#second-dependency-dependable-and-dependant]
note: Establish this first: Prerequisites resolve before consumers.
note: Stay within the current objective: Compose subdependencies. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine provider execution order.
PRACTICE ANCHOR (live_code): Compose a pagination provider, an order-options provider that depends on it, and a consuming path operation. Declare typed query inputs on the pagination provider and connect both dependency edges with Annotated and Depends.  SUCCESS: The pagination provider receives typed query inputs and returns a value consumed by order-options. The path operation receives the order-options result, with prerequisites resolved before their consumers.
ASSESSMENT ANCHOR: determine_provider_execution_order facts=['f1', 'f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Backward-compatible REST contract changes; Binding request bodies to typed models; Bounded form and multipart file inputs; Bounded in-process background work and nondurable delivery limits; CORS origin and credential policy; Composing request dependency graphs; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Configuring existing middleware in the request/response stack; Credential and sensitive-data redaction from emitted logs; Distinct create and partial-update contracts; Endpoint integration tests using TestClient or async HTTPX as appropriate; FastAPI OpenAPI generation from typed route contracts; Graceful termination and shutdown verification; Header and cookie input binding; Meaningful contract examples and operation metadata; Preventing unsafe outbound requests and SSRF; Production ASGI serving versus development reload; Request-scoped async-compatible PostgreSQL session lifecycle; Request-scoped dependency reuse and lifetime; Request-validation error behavior; Required, optional and default input semantics; Retrieve resource; Service health and readiness checks; Structured service requ

## LESSON, in learner order

### s01 · explainer · The rule: Separating transport, testable business logic and persistence responsibilities
(definition) A dependency can extract reusable input-provision logic from individual operation handlers and expose the supplied value as a declared handler parameter. ⟦A.f1 A:tb2⟧
(mechanism) Transport handlers adapt HTTP inputs and outputs, business callables enforce application rules, and persistence adapters access stored state; separate these responsibilities so each can change without embedding the other responsibilities. Move a business decision from a handler into a plain callable with explicit inputs, keep the HTTP adaptation in the handler, and call a separate persistence adapter for stored state rather than treating separate files alone as a responsibility boundary. ⟦A.f2 A.f3 A:tb3⟧
[DIAGRAM] nodes=['HTTP adaptation: handler', 'Business rule: plain callable', 'Stored state: persistence adapter', 'Reusable input provisioning: dependency'] edges=[('n3', 'n0', 'declared handler parameter'), ('n0', 'n1', 'explicit decision inputs'), ('n0', 'n2', 'stored-state access; not embedded in handler')] alt: Make the order flow visible across three responsibility boundaries: HTTP adaptation in the handler, the order decision in a plain business callable, and stored-state access in a persistence adapter. Show reusable input provisioning entering through a declared handler parameter, and distinguish responsibility boundaries from file boundaries.

### s02 · explainer · Trace the boundary: Separating transport, testable business logic and persistence responsibilities
(walkthrough) Keep HTTP adaptation in the handler, the order decision in a plain callable with explicit inputs, and stored-state access in a persistence adapter. A dependency can supply reusable input provisioning through a declared handler parameter. Separate responsibilities, not just files: moving the same mixture into several modules does not establish those boundaries. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · check · Choose the distinction: Separating transport, testable business logic and persistence responsibilities
Check your understanding — Use the declared contract to distinguish the outcomes.

### s04 · hands_on · Practice: Separating transport, testable business logic and persistence responsibilities
Apply the contract — Work in the supplied orders-service exercise snapshot.

### s05 · explainer · The rule: Bounded in-process background work and nondurable delivery limits
(definition) Declare a BackgroundTasks handler parameter and call background_tasks.add_task(callable, *args, **kwargs) to schedule work after sending the response. ⟦B.f1 B:tb2⟧
(mechanism) A background task callable can be a normal def or async def function; FastAPI handles either form. BackgroundTasks work runs in the application process and cannot guarantee survival or delivery when that process fails. ⟦B.f2 B.f3 B:tb3⟧
[DIAGRAM] nodes=['Handler registers add_task', 'Response sent', 'Follow-up task: def or async def', 'Application process boundary', 'Process failure after response'] edges=[('n0', 'n1', 'register callable and arguments'), ('n1', 'n2', 'task runs after response'), ('n3', 'n2', 'in-process work'), ('n4', 'n2', 'pending work can be lost; no guaranteed survival or delivery')] alt: Show an order handler registering follow-up work, sending its response, and then running the task inside the application-process boundary. Mark a process failure after the response as a point where pending work can be lost, separating response delivery from follow-up completion.

### s06 · explainer · Trace the boundary: Bounded in-process background work and nondurable delivery limits
(walkthrough) Declare BackgroundTasks and register a callable with background_tasks.add_task(callable, *args, **kwargs). The response is sent before follow-up work runs in the application process. The callable may use def or async def. If the process fails, survival or delivery cannot be guaranteed. Scheduling therefore does not prove durable completion. ⟦B.f1 B.f2 B.f3 B:tb4 B:tb5⟧

### s07 · video · Bounded in-process background work and nondurable delivery limits
[VIDEO ] bridge-before:  | bridge-after: 

### s08 · check · Choose the distinction: Bounded in-process background work and nondurable delivery limits
Check your understanding — Use the declared contract to distinguish the outcomes.

### s09 · hands_on · Practice: Bounded in-process background work and nondurable delivery limits
Apply the contract — Work in the supplied orders-service exercise snapshot.

### s10 · explainer · The rule: Composing request dependency graphs
(definition) A provider can declare its own Annotated[Type, Depends(other_provider)] parameter, forming a dependency graph. ⟦C.f1 C:tb2⟧
(mechanism) FastAPI resolves a provider's prerequisite inputs before calling that provider and supplies its result to the consuming operation. A sub-dependency can declare typed query inputs of its own; those inputs are extracted from the request before its returned value is supplied to the dependent provider. ⟦C.f2 C.f3 C:tb3⟧
[DIAGRAM] nodes=['Typed page and page_size query inputs', 'Pagination provider', 'Order-options provider', 'Consuming operation'] edges=[('n0', 'n1', 'extract and convert request inputs'), ('n1', 'n2', 'resolve prerequisite and supply its result'), ('n2', 'n3', 'supply provider result')] alt: Make the dependency direction and execution order visible: typed page and page_size request inputs → pagination provider → order-options provider → consuming operation.

### s11 · explainer · Trace the boundary: Composing request dependency graphs
(walkthrough) The pagination provider declares typed page and page_size query inputs. FastAPI extracts those inputs and resolves pagination before supplying its result to order-options; the consuming operation then receives the order-options result. A provider declares a prerequisite with Annotated[Type, Depends(other_provider)]. Trace from prerequisites toward consumers, not the reverse. ⟦C.f1 C.f2 C.f3 C:tb4 C:tb5⟧

### s12 · check · Choose the distinction: Composing request dependency graphs
Check your understanding — Use the declared contract to distinguish the outcomes.

### s13 · hands_on · Practice: Composing request dependency graphs
Apply the contract — Work in the supplied orders-service exercise snapshot.

### s14 · recap · Keep these boundaries
(takeaway) Separate files alone are not separate concerns. Responsibilities must be separated so one can change without embedding the others. ⟦A.f2 A.f3 A:tb5⟧
(takeaway) Adding a background task does not prove that it survives process failure or delivers its effect. In-process scheduling is not durable completion. ⟦B.f3 B:tb5⟧
(takeaway) A provider does not run before its unresolved prerequisite inputs are available. Resolve the graph from prerequisites to consumers. ⟦C.f2 C:tb5⟧
[UP NEXT] Configuring existing middleware in the request/response stack: Next: Configuring existing middleware in the request/response stack.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast again: Separating transport, testable business logic and persistence responsibilities
(definition) Transport handlers adapt HTTP inputs and outputs, business callables enforce application rules, and persistence adapters access stored state; separate these responsibilities so each can change without embedding the other responsibilities. Move a business decision from a handler into a plain callable with explicit inputs, keep the HTTP adaptation in the handler, and call a separate persistence adapter for stored state rather than treating separate files alone as a responsibility boundary. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
(example) The handler adapts HTTP, the plain callable decides the order rule, and the adapter accesses stored state. Three files containing the same mixture are not three responsibility boundaries. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast again: Separating transport, testable business logic and persistence responsibilities
(definition) A dependency can extract reusable input-provision logic from individual operation handlers and expose the supplied value as a declared handler parameter. Transport handlers adapt HTTP inputs and outputs, business callables enforce application rules, and persistence adapters access stored state; separate these responsibilities so each can change without embedding the other responsibilities. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Declare reusable quantity provisioning as a handler parameter, rather than repeating that input logic inside each operation. The handler adapts HTTP, the plain callable decides the order rule, and the adapter accesses stored state. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Try the contrast again: Bounded in-process background work and nondurable delivery limits
(definition) BackgroundTasks work runs in the application process and cannot guarantee survival or delivery when that process fails. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(example) An order response can be sent before a process failure loses pending follow-up work: scheduling is not guaranteed delivery. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
### r04 · Try the contrast again: Bounded in-process background work and nondurable delivery limits
### r05 · Try the contrast again: Composing request dependency graphs
(definition) A provider can declare its own Annotated[Type, Depends(other_provider)] parameter, forming a dependency graph. FastAPI resolves a provider's prerequisite inputs before calling that provider and supplies its result to the consuming operation. A sub-dependency can declare typed query inputs of its own; those inputs are extracted from the request before its returned value is supplied to the dependent provider. ⟦C.f1 C.f2 C.f3 C:tb2 C:tb3 C:tb4 C:tb5⟧
(example) Order-options declares pagination as a prerequisite, not a hidden global value. Resolve pagination before order-options, not after calling its consumer. The typed query inputs are extracted before pagination supplies its result to order-options. ⟦C.f1 C.f2 C.f3 C:tb2 C:tb3 C:tb4 C:tb5⟧
### r06 · Try the contrast again: Composing request dependency graphs

=========

# EVALUATOR PACKET — Configuring existing middleware in the request/response stack · Production ASGI serving versus development reload (tile_037)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.existing_middleware_stack — Configuring existing middleware in the request/response stack
B = fastapi.production_asgi_serving — Production ASGI serving versus development reload

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (fastapi.existing_middleware_stack)   objective: Configure existing middleware coherently: configure two maintained middleware components and trace their effects.
A.f1: The last middleware added is the outermost wrapper: requests traverse it first, while responses traverse it last.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/middleware/#multiple-middleware-execution-order]
A.f2: Configure each selected maintained middleware with app.add_middleware(MiddlewareClass, option=value), passing the component's documented options rather than writing its protocol implementation.   [sources: fastapi_docs_advanced#https://starlette.dev/middleware/#using-middleware]
A.f3: For two middleware additions, trace the request through the second addition then the first and into the handler, and trace the resulting response through the first addition then the second.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/middleware/#multiple-middleware-execution-order]
note: Establish this first: Middleware wraps the application, so request and response traversal run in opposite directions.
note: Stay within the current objective: Configure existing middleware coherently. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Predict request and response traversal order of the configured stack.
PRACTICE ANCHOR (live_code): Configure supplied maintained middleware components A and B using their documented options, adding A first and B second. Annotate the request and response traversal through both components and the handler.  SUCCESS: Both components are configured with app.add_middleware and the supplied documented options. The annotations identify B as outermost, show requests traversing B → A → handler, and show the resulting response traversing A → B.
ASSESSMENT ANCHOR: predict_request_and_response_stack_traversal facts=['f1', 'f3']

## SOURCE FACTS — B (fastapi.production_asgi_serving)   objective: Choose production ASGI serving: run one production-appropriate command.
B.f1: Run the application with an ASGI server import string, such as uvicorn main:app --host 0.0.0.0 --port 8000, where main names the module and app names its application object.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/deployment/manually/#run-the-server-program]
B.f2: --reload is useful during development but should not be enabled in production because it consumes resources and is less stable.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/deployment/manually/#run-the-server-program]
B.f3: Uvicorn's --workers option starts multiple worker processes and is mutually exclusive with --reload; choose the worker count for the deployment rather than treating reload as process management.   [sources: fastapi_docs_tutorial#https://uvicorn.dev/settings/#production]
note: Establish this first: Production prioritizes stable process behavior.
note: Stay within the current objective: Choose production ASGI serving. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify development-only behavior.
PRACTICE ANCHOR (live_code): Run uvicorn main:app --host 0.0.0.0 --port 8000 for the supplied application without development reload.  SUCCESS: The command starts the supplied application on the specified host and port without enabling reload.
ASSESSMENT ANCHOR: identify_reload_as_development_only facts=['f2']
ASSESSMENT ANCHOR: distinguish_worker_processes_from_development_reload facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Backward-compatible REST contract changes; Bearer-token extraction into an authentication dependency; Binding request bodies to typed models; Bounded form and multipart file inputs; CORS origin and credential policy; Configure established request-metrics instrumentation and verify counts, errors and latency with successful, failing and delayed requests; Credential and sensitive-data redaction from emitted logs; Distinct create and partial-update contracts; Endpoint integration tests using TestClient or async HTTPX as appropriate; FastAPI OpenAPI generation from typed route contracts; Graceful termination and shutdown verification; Header and cookie input binding; Meaningful contract examples and operation metadata; Preventing unsafe outbound requests and SSRF; Production ASGI serving versus development reload; Request-scoped async-compatible PostgreSQL session lifecycle; Request-scoped dependency reuse and lifetime; Request-validation error behavior; Required, optional and default input semantics; Retrieve resource; Service health and readiness checks; Structured service request and error logs; Test dependency replacement; Transaction commit and rollback boundaries; Trusted host va

## LESSON, in learner order

### s01 · explainer · The rule: Configuring existing middleware in the request/response stack
(definition) The last middleware added is the outermost wrapper: requests traverse it first, while responses traverse it last. ⟦A.f1 A:tb2⟧
(mechanism) Configure each selected maintained middleware with app.add_middleware(MiddlewareClass, option=value), passing the component's documented options rather than writing its protocol implementation. For two middleware additions, trace the request through the second addition then the first and into the handler, and trace the resulting response through the first addition then the second. ⟦A.f2 A.f3 A:tb3⟧
[DIAGRAM] nodes=['B: added second; outermost', 'A: added first; inside B', 'Handler: inside A'] edges=[('n0', 'n1', 'request inward'), ('n1', 'n2', 'request inward'), ('n2', 'n1', 'response outward'), ('n1', 'n0', 'response outward')] alt: Show the handler nested inside middleware A inside middleware B, label A as the first addition and B as the second, and draw separate request and response arrows in opposite directions.

### s02 · explainer · Trace the boundary: Configuring existing middleware in the request/response stack
(walkthrough) Add A first and B second with app.add_middleware and each maintained component’s documented options. B is the outermost wrapper. Requests traverse B → A → handler; the resulting response traverses handler → A → B. Addition order explains both directions, but the traversal sequences are not identical. Configure the components rather than implementing their protocols. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · check · Choose the distinction: Configuring existing middleware in the request/response stack
Check your understanding — Use the declared contract to distinguish the outcomes.

### s04 · hands_on · Practice: Configuring existing middleware in the request/response stack
Apply the contract — Work in the supplied orders-service exercise snapshot.

### s05 · explainer · The rule: Production ASGI serving versus development reload
(definition) Run the application with an ASGI server import string, such as uvicorn main:app --host 0.0.0.0 --port 8000, where main names the module and app names its application object. ⟦B.f1 B:tb2⟧
(mechanism) --reload is useful during development but should not be enabled in production because it consumes resources and is less stable. Uvicorn's --workers option starts multiple worker processes and is mutually exclusive with --reload; choose the worker count for the deployment rather than treating reload as process management. ⟦B.f2 B.f3 B:tb3⟧
(walkthrough) Use an ASGI server import string: main:app names module main and application object app. The supplied command selects its host and port without reload. --reload is useful in development, but consumes resources and is less stable, so do not enable it in production. --workers starts multiple processes and is mutually exclusive with --reload; choose worker count for the deployment. ⟦B.f1 B.f2 B.f3 B:tb4⟧
[CODE bash]
uvicorn main:app --host 0.0.0.0 --port 8000
  annotations: ['Use an ASGI server import string: main:app names module main and application object app. The supplied command selects its host and port without reload. --reload is useful in development, but consumes resources and is less stable, so do not enable it in production. --workers starts multiple processes and is mutually exclusive with --reload; choose worker count for the deployment.']

### s06 · check · Choose the distinction: Production ASGI serving versus development reload
Check your understanding — Use the declared contract to distinguish the outcomes.

### s07 · hands_on · Practice: Production ASGI serving versus development reload
Apply the contract — Work in the supplied orders-service exercise snapshot.

### s08 · recap · Keep these boundaries
(takeaway) The last addition sees requests first and responses last. Request traversal and response traversal are not identical sequences. ⟦A.f1 A.f3 A:tb5⟧
(takeaway) Reload is not production process management. Worker count belongs to the deployment decision, and workers cannot be combined with reload. ⟦B.f2 B.f3 B:tb5⟧
[UP NEXT] Binding request bodies to typed models: Next: Binding request bodies to typed models.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast again: Configuring existing middleware in the request/response stack
(definition) The last middleware added is the outermost wrapper: requests traverse it first, while responses traverse it last. For two middleware additions, trace the request through the second addition then the first and into the handler, and trace the resulting response through the first addition then the second. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Adding A then B puts B outside A, not inside it. Requests travel B → A → handler; responses travel handler → A → B, not the same sequence. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast again: Configuring existing middleware in the request/response stack
(definition) The last middleware added is the outermost wrapper: requests traverse it first, while responses traverse it last. For two middleware additions, trace the request through the second addition then the first and into the handler, and trace the resulting response through the first addition then the second. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Adding A then B puts B outside A, not inside it. Requests travel B → A → handler; responses travel handler → A → B, not the same sequence. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Try the contrast again: Production ASGI serving versus development reload
(definition) Uvicorn's --workers option starts multiple worker processes and is mutually exclusive with --reload; choose the worker count for the deployment rather than treating reload as process management. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(example) Workers provide multiple processes; reload is not process management and cannot be combined with workers. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
### r04 · Try the contrast again: Production ASGI serving versus development reload
(definition) --reload is useful during development but should not be enabled in production because it consumes resources and is less stable. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(example) Leave reload to development; the production command does not enable it. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧