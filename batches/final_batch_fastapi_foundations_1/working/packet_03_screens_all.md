# EVALUATOR PACKET — Browser same-origin policy and the CORS/authentication boundary · HTTP method safety and idempotency · HTTP headers and representation metadata (tile_000)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = browser.same_origin_boundary — Browser same-origin policy and the CORS/authentication boundary
B = http.method_safety_idempotency — HTTP method safety and idempotency
C = http.representation_headers — HTTP headers and representation metadata

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (browser.same_origin_boundary)   objective: Explain the browser origin boundary: classify same-origin and cross-origin calls to one API.
A.f1: A browser origin is the combination of scheme, host and port; a difference in any of these makes two URLs cross-origin.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/cors/#origin]
A.f2: Browser same-origin restrictions limit a script's access to cross-origin responses unless the server permits that access through CORS.   [sources: mdn_http#https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS#functional_overview]
A.f3: An API must check access at its endpoints independently of the browser's cross-origin restrictions.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html#access-control]
note: Establish this first: Origins combine scheme, host and port; browser enforcement is not server authorization.
note: Stay within the current objective: Explain the browser origin boundary. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Distinguish browser access restrictions from API authentication.
PRACTICE ANCHOR (matching): Classify calls from browser pages to https://shop.example:443/orders as same-origin or cross-origin by comparing scheme, host and port.  SUCCESS: Correctly classify https://shop.example:443/items as same-origin and http://shop.example:443/items, https://api.example:443/items, and https://shop.example:8443/items as cross-origin, identifying the differing origin component in each cross-origin case.
ASSESSMENT ANCHOR: classify_origins_by_scheme_host_and_port facts=['f1']
ASSESSMENT ANCHOR: distinguish_browser_response_access_from_api_authentication facts=['f2', 'f3']

## SOURCE FACTS — B (http.method_safety_idempotency)   objective: Choose HTTP methods: select methods for one workflow.
B.f1: A safe method has essentially read-only requested semantics; incidental effects such as logging do not make it unsafe.   [sources: rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.1]
B.f2: A method is idempotent when multiple identical requests have the same intended server effect as one request, even if responses differ.   [sources: rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2]
B.f3: GET retrieves a selected representation and HEAD requests the same semantics without response content; both are safe and idempotent.   [sources: rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-9.3.1, rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-9.3.2]
B.f4: POST requests resource-specific processing of submitted content and is not generally idempotent.   [sources: rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-9.3.3]
B.f5: PUT creates or replaces the target resource's state and DELETE removes its association with current functionality; both are idempotent but not safe.   [sources: rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-9.3.4, rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-9.3.5]
note: Establish this first: Method semantics constrain effects and repetition.
note: Stay within the current objective: Choose HTTP methods. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine repeated operation effects.
PRACTICE ANCHOR (matching): Select HTTP methods for an orders workflow: retrieve an order representation, request the same semantics without response content, process a new order submission, create or replace a known order's state, and remove its association with current functionality.  SUCCESS: Match the operations to GET, HEAD, POST, PUT, and DELETE respectively. Identify GET and HEAD as safe and idempotent, PUT and DELETE as idempotent but not safe, and POST as not generally idempotent. Judge repetition by intended server effects rather than identical responses, and treat incidental retrieval logging as compatible with safety.
ASSESSMENT ANCHOR: determine_intended_effects_of_identical_repeated_requests facts=['f2', 'f3', 'f4', 'f5']
ASSESSMENT ANCHOR: distinguish_safe_retrieval_from_idempotent_state_changes facts=['f1', 'f3', 'f5']

## SOURCE FACTS — C (http.representation_headers)   objective: Use representation metadata consistently: implement and test representation headers for one JSON operation.
C.f1: Content-Type describes the media type of the associated representation, rather than the client's preferred response format.   [sources: rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-8.3]
C.f2: Accept communicates acceptable response media types.   [sources: rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-12.5.1]
C.f3: For a JSON exchange, send Content-Type: application/json for JSON content and Accept: application/json to request a JSON response, and inspect the response Content-Type separately.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html#validate-content-types, rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-8.3]
note: Establish this first: Client preferences and actual payload media types are different claims.
note: Stay within the current objective: Use representation metadata consistently. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Distinguish payload Content-Type from requested Accept negotiation.
note: Implementing an operation and writing endpoint integration tests require later concepts. Adapt the objective to completing raw HTTP headers in a prepared JSON order exchange and checking its supplied response metadata, without service declarations or test libraries.
PRACTICE ANCHOR (live_code): Complete the representation headers in a prepared HTTP request that sends an order as JSON, then check the returned representation using the response's own Content-Type.  SUCCESS: The request contains Content-Type: application/json and Accept: application/json. The learner identifies the returned media type from the response Content-Type, independently of the request headers.
ASSESSMENT ANCHOR: distinguish_payload_media_type_from_response_preference facts=['f1', 'f2']
ASSESSMENT ANCHOR: set_json_request_headers_and_inspect_response_content_type facts=['f3']

## DATA ASSETS USED
ds.browser_origins: Calls to one fixed API — columns: api_url(text), api_scheme(categorical), api_host(categorical), api_port(categorical,digits-as-label), browser_url(text), browser_scheme(categorical), browser_host(categorical), browser_port(categorical,digits-as-label), browser_path(text), origin_classification(categorical), differing_components(categorical)
   ["https://shop.example:443/orders","https","shop.example",443,"https://shop.example:443/items","https","shop.example",443,"/items","same-origin","none"]
   ["https://shop.example:443/orders","https","shop.example",443,"http://shop.example:443/items","http","shop.example",443,"/items","cross-origin","scheme"]
   ["https://shop.example:443/orders","https","shop.example",443,"https://api.example:443/items","https","api.example",443,"/items","cross-origin","host"]
   ["https://shop.example:443/orders","https","shop.example",443,"https://shop.example:8443/items","https","shop.example",8443,"/items","cross-origin","port"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): ASGI server and application request lifecycle; Application lifespan; Async-compatible external HTTP requests; CORS preflight behavior; Choosing HTTP success and failure statuses; Context-managed resource cleanup; Cooperative concurrency with async and await; Custom validation for domain invariants; Declarative field validation constraints; Expected API failures with HTTPException; FastAPI application and path-operation declarations; HTTP headers and representation metadata; HTTP method safety and idempotency; Isolated Python environments and compatible dependency installation; Local password hashing and credential verification without an OAuth password grant; Nested request-data models; Orm entity mapping; Orm relationship mapping; Practical Python type annotations for service interfaces; Pydantic V2 model construction and input conversion; Python classes and instances for service models; Python decorators as callable wrappers; Python package organization for a service; Reproducible service dependency declarations; Resource-oriented REST URLs and CRUD contracts; Service-schema integrity constraints; Validated environment-based configuration with fail-fast startup

## LESSON, in learner order

### s01 · explainer · Establish the rule
Browser same-origin policy and the CORS/authentication boundary — 
(intro) For a browser page calling an API, separate address matching from permission to access the endpoint. ⟦A:tb1⟧
(definition) An origin combines scheme, host and port. A difference in any one makes URLs cross-origin. ⟦A.f1 A:tb2⟧
(mechanism) Browser restrictions limit a script’s access to cross-origin responses unless the server permits it through CORS. The API must independently check endpoint access. ⟦A.f2 A.f3 A:tb3⟧
(example) https://shop.example:443/orders and https://shop.example:443/items share an origin despite different paths. Changing the host to api.example or the port to 8443 makes the call cross-origin. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) Browser permission to read a response is not authentication. The API still needs its own access checks. ⟦A.f3 A:tb5⟧
[TABLE ds.browser_origins cols=all ] caption: 

### s02 · check · Check the distinction
Browser same-origin policy and the CORS/authentication boundary — 

### s03 · hands_on · Apply the rule
Browser same-origin policy and the CORS/authentication boundary — 

### s04 · explainer · Establish the rule
HTTP method safety and idempotency — 
(intro) Choose an order operation’s method by its intended effect, not by a convenient label. ⟦B:tb1⟧
(definition) Safe methods request essentially read-only semantics. Incidental logging does not make them unsafe. ⟦B.f1 B:tb2⟧
(mechanism) Idempotency means identical repetition has the same intended server effect as one request, even if replies differ. GET retrieves a representation; HEAD has the same semantics without response content. Both are safe and idempotent. POST requests resource-specific processing and is not generally idempotent. PUT creates or replaces target state; DELETE removes its association with current functionality. Both are idempotent, not safe. ⟦B.f2 B.f3 B.f4 B.f5 B:tb3⟧
[SIDE_BY_SIDE] Safety and idempotency are separate properties. left_label: Read-only requested semantics | right_label: State-changing requested semantics
  left:
[DIAGRAM] nodes=['GET: retrieve representation', 'HEAD: same semantics, no content', 'Safe and idempotent'] edges=[('n1', 'n3', ''), ('n2', 'n3', '')] alt: GET retrieves a representation and HEAD requests the same semantics without response content; both map to safe and idempotent.
  right:
[DIAGRAM] nodes=['PUT: create or replace target state', 'DELETE: remove association', 'Idempotent, not safe', 'POST: resource-specific processing; not generally idempotent'] edges=[('n1', 'n3', ''), ('n2', 'n3', '')] alt: PUT creates or replaces target state and DELETE removes its association; both map to idempotent, not safe. POST requests resource-specific processing and is not generally idempotent.

### s05 · explainer · Why the distinction matters
HTTP method safety and idempotency — 
(walkthrough) Reading an order and replacing it can both be idempotent, but only reading is safe. Repeated PUT requests the same target state; POST processing is not generally idempotent. Describe the requested change and identical repetition separately. Matching replies are not the test. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb4⟧

### s06 · explainer · Reason through an example
HTTP method safety and idempotency — 
(walkthrough) At /orders/42, GET retrieves a representation and HEAD requests the same semantics without content. Logging is incidental. Repeating a PUT replacement requests the same target state, even if replies differ. Repeated DELETE also need not return identical replies. POST collection processing is not generally idempotent. Ask separately: does this request a change, and does identical repetition preserve the intended effect? ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb5⟧
(misconception) Safety does not prohibit all incidental effects. Idempotency does not require identical replies. PUT and DELETE can be idempotent yet unsafe. ⟦B.f1 B.f2 B.f5 B:tb6⟧

### s07 · check · Check the distinction
HTTP method safety and idempotency — 

### s08 · hands_on · Apply the rule
HTTP method safety and idempotency — 

### s09 · explainer · Establish the rule
HTTP headers and representation metadata — 
(intro) An order’s outgoing body format, preferred response format and actual response format are separate information. ⟦C:tb1⟧
(definition) Content-Type labels the media type of its associated representation, not the preferred response format. ⟦C.f1 C:tb2⟧
(mechanism) Accept lists acceptable response media types. For JSON content, send Content-Type: application/json; request a JSON response with Accept: application/json. Inspect the reply’s Content-Type separately. ⟦C.f2 C.f3 C:tb3⟧
(example) In this JSON exchange, the request Content-Type labels the submitted content. Accept states the response preference. Read the response’s own Content-Type to identify what came back. ⟦C.f1 C.f2 C.f3 C:tb4⟧
(misconception) Content-Type labels content. Accept carries the client’s response preference. ⟦C.f1 C.f2 C:tb5⟧
[SIDE_BY_SIDE] Inspect the reply’s own Content-Type. left_label: Request: body label and response preference | right_label: Response: actual content label
  left:
[DIAGRAM] nodes=['POST /orders HTTP/1.1', 'Host: shop.example', 'Content-Type: application/json', 'Accept: application/json', '{"quantity": 3}'] edges=[] alt: POST /orders HTTP/1.1 → Host: shop.example → Content-Type: application/json → Accept: application/json → {"quantity": 3}
  right:
[DIAGRAM] nodes=['HTTP/1.1 201 Created', 'Content-Type: application/json', '{"quantity": 3}'] edges=[] alt: HTTP/1.1 201 Created → Content-Type: application/json → {"quantity": 3}

### s10 · check · Check the distinction
HTTP headers and representation metadata — 

### s11 · hands_on · Apply the rule
HTTP headers and representation metadata — 

### s12 · recap · Keep these takeaways
Review — 
(takeaway) Compare scheme, host and port; browser response access and API access checks stay separate. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Safety concerns requested changes; idempotency concerns repeated intended effects, not identical replies. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧
(takeaway) Content-Type labels content; Accept states response preferences. ⟦C.f1 C.f2 C.f3 C:tb1 C:tb2 C:tb3 C:tb4 C:tb5⟧
[UP NEXT] Practical Python type annotations for service interfaces: Continue to tile_003.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit tile_000.s02
(definition) Browser same-origin restrictions limit a script's access to cross-origin responses unless the server permits that access through CORS. ⟦A.f2 A:tb3 A:tb4⟧
(definition) An API must check access at its endpoints independently of the browser's cross-origin restrictions. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) Contrast changing only /items with changing host: paths do not change origins, but host changes do. Neither replaces API access checks. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.browser_origins cols=all ] caption: 
### r02 · Revisit tile_000.s03
(definition) A browser origin is the combination of scheme, host and port; a difference in any of these makes two URLs cross-origin. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Browser same-origin restrictions limit a script's access to cross-origin responses unless the server permits that access through CORS. ⟦A.f2 A:tb3 A:tb4⟧
(definition) An API must check access at its endpoints independently of the browser's cross-origin restrictions. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) Contrast changing only /items with changing host: paths do not change origins, but host changes do. Neither replaces API access checks. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.browser_origins cols=all ] caption: 
### r03 · Revisit tile_000.s07
(definition) A safe method has essentially read-only requested semantics; incidental effects such as logging do not make it unsafe. ⟦B.f1 B:tb2 B:tb4 B:tb5 B:tb6⟧
(definition) GET retrieves a selected representation and HEAD requests the same semantics without response content; both are safe and idempotent. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(definition) PUT creates or replaces the target resource's state and DELETE removes its association with current functionality; both are idempotent but not safe. ⟦B.f5 B:tb3 B:tb4 B:tb5 B:tb6⟧
(example) Contrast GET retrieval with PUT replacement: both are idempotent, but replacement requests a change and is not safe. ⟦B.f1 B.f3 B.f5 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧
### r04 · Revisit tile_000.s08
(definition) A safe method has essentially read-only requested semantics; incidental effects such as logging do not make it unsafe. ⟦B.f1 B:tb2 B:tb4 B:tb5 B:tb6⟧
(definition) A method is idempotent when multiple identical requests have the same intended server effect as one request, even if responses differ. ⟦B.f2 B:tb3 B:tb4 B:tb5 B:tb6⟧
(definition) GET retrieves a selected representation and HEAD requests the same semantics without response content; both are safe and idempotent. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(definition) POST requests resource-specific processing of submitted content and is not generally idempotent. ⟦B.f4 B:tb3 B:tb4 B:tb5⟧
(definition) PUT creates or replaces the target resource's state and DELETE removes its association with current functionality; both are idempotent but not safe. ⟦B.f5 B:tb3 B:tb4 B:tb5 B:tb6⟧
(example) Contrast GET retrieval with PUT replacement: both are idempotent, but replacement requests a change and is not safe. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧
### r05 · Revisit tile_000.s10
(definition) For a JSON exchange, send Content-Type: application/json for JSON content and Accept: application/json to request a JSON response, and inspect the response Content-Type separately. ⟦C.f3 C:tb3 C:tb4⟧
(example) Content-Type labels content; Accept states response preferences. ⟦C.f3 C:tb3 C:tb4⟧
### r06 · Revisit tile_000.s11
(definition) Content-Type describes the media type of the associated representation, rather than the client's preferred response format. ⟦C.f1 C:tb2 C:tb4 C:tb5⟧
(definition) Accept communicates acceptable response media types. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
(definition) For a JSON exchange, send Content-Type: application/json for JSON content and Accept: application/json to request a JSON response, and inspect the response Content-Type separately. ⟦C.f3 C:tb3 C:tb4⟧
(example) Content-Type labels content; Accept states response preferences. ⟦C.f1 C.f2 C.f3 C:tb2 C:tb3 C:tb4 C:tb5⟧

=========

# EVALUATOR PACKET — Practical Python type annotations for service interfaces · Python classes and instances for service models (tile_003)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.backend_type_annotations — Practical Python type annotations for service interfaces
B = python.classes_and_instances — Python classes and instances for service models

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.backend_type_annotations)   objective: Annotate API data types: annotate one service function.
A.f1: Annotate a function parameter with name: Type and its return value with -> Type; Python type hints alone do not enforce runtime validation.   [sources: fastapi_docs_python_types#https://fastapi.tiangolo.com/python-types/#type-hints-in-fastapi]
A.f2: Type | None permits None, while a default such as = None separately permits omitting a Python function argument.   [sources: fastapi_docs_python_types#https://fastapi.tiangolo.com/python-types/#union]
A.f3: list[str], set[str], tuple[int, str] and dict[str, int] annotate a list of strings, a set of strings, a two-element integer/string tuple and a string-to-integer dictionary respectively.   [sources: fastapi_docs_python_types#https://fastapi.tiangolo.com/python-types/#generic-types]
note: Establish this first: Annotations describe shapes but do not themselves validate values.
note: Stay within the current objective: Annotate API data types. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Select annotations for required, nullable and collection values.
PRACTICE ANCHOR (live_code): Annotate an existing order-summary service function: item_names is a list of strings, tags is a set of strings, identifier_name is an integer/string pair, counts maps strings to integers, and note accepts a string or None and may be omitted. Annotate the returned counts as a string-to-integer dictionary.  SUCCESS: The function declares all parameter and return types correctly, and note has both a nullable annotation and a None default. The existing body remains unchanged; no runtime validation is added.
ASSESSMENT ANCHOR: select_parameter_and_return_annotations facts=['f1']
ASSESSMENT ANCHOR: distinguish_type_hints_from_runtime_validation facts=['f1']
ASSESSMENT ANCHOR: distinguish_nullable_values_from_omittable_arguments facts=['f2']
ASSESSMENT ANCHOR: select_collection_annotations facts=['f3']

## SOURCE FACTS — B (python.classes_and_instances)   objective: Represent state with classes and instances: implement two independent instances.
B.f1: A class statement creates a class whose methods define behavior, and calling the class creates an instance.   [sources: python_tutorial#https://docs.python.org/3/tutorial/classes.html#class-definition-syntax]
B.f2: Define __init__(self, ...) to initialize an instance and assign self.attribute to store that instance's state; an instance method receives that instance as its first argument.   [sources: python_tutorial#https://docs.python.org/3/tutorial/classes.html#class-objects, python_tutorial#https://docs.python.org/3/tutorial/classes.html#method-objects]
B.f3: Instance variables hold data specific to each instance, while class variables are shared by instances of the class.   [sources: python_tutorial#https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables]
B.f4: A mutable class variable can be shared unintentionally; initialize a fresh mutable value on self inside __init__ when instances need independent values.   [sources: python_tutorial#https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables]
note: Establish this first: Classes define behavior; instances own state.
note: Stay within the current objective: Represent state with classes and instances. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Distinguish instance from class state.
PRACTICE ANCHOR (live_code): Implement Draft so that draft_a and draft_b each start with an independent empty items list, then add an item only to draft_a.  SUCCESS: Both instances are created by calling Draft. Each receives a fresh items list inside __init__; after adding an item to draft_a.items, draft_b.items remains empty.
ASSESSMENT ANCHOR: distinguish_class_behavior_from_instance_state facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_shared_class_state_and_independent_instance_state facts=['f3', 'f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): ASGI server and application request lifecycle; Application lifespan; Async-compatible external HTTP requests; CORS preflight behavior; Choosing HTTP success and failure statuses; Choosing def versus async def from I/O behavior without blocking the event loop; Context-managed resource cleanup; Cooperative concurrency with async and await; Custom validation for domain invariants; Declarative field validation constraints; Expected API failures with HTTPException; FastAPI application and path-operation declarations; Isolated Python environments and compatible dependency installation; Local password hashing and credential verification without an OAuth password grant; Modular FastAPI application composition with APIRouter; Nested request-data models; Orm entity mapping; Orm relationship mapping; Pydantic V2 model construction and input conversion; Python classes and instances for service models; Python decorators as callable wrappers; Python package organization for a service; Reproducible service dependency declarations; Resource-oriented REST URLs and CRUD contracts; Service-schema integrity constraints; Validated environment-based configuration with fail-fast startup

## LESSON, in learner order

### s01 · explainer · Establish the rule
Practical Python type annotations for service interfaces — 
(intro) Describe the service function’s inputs and result. Distinguish accepting None from allowing the caller to omit an argument. ⟦A:tb1⟧
(definition) Use name: Type for a parameter and -> Type for the result. Hints alone do not validate runtime values. ⟦A.f1 A:tb2⟧
(mechanism) Type | None admits None; = None separately allows omission. list[str] is a list of strings; set[str] a set of strings; tuple[int, str] a two-element integer/string tuple; dict[str, int] a string-to-integer dictionary. ⟦A.f2 A.f3 A:tb3⟧
[CODE python]
def order_summary(
    item_names: list[str], tags: set[str],
    identifier_name: tuple[int, str], counts: dict[str, int],
    note: str | None = None
) -> dict[str, int]:
    return counts

  annotations: ['Collection shapes describe element and key/value types.', 'The union allows None; the default separately allows omission.', 'The return hint describes the result, not runtime validation.']

### s02 · explainer · Why the distinction matters
Practical Python type annotations for service interfaces — 
(walkthrough) Read shapes first, then defaults. Removing = None changes whether note can be omitted, not whether its type admits None. Removing | None changes admitted values, not defaults. An annotated interface still does not validate runtime values by itself. ⟦A.f1 A.f2 A:tb4⟧

### s03 · explainer · Reason through an example
Practical Python type annotations for service interfaces — 
(walkthrough) For order_summary, item_names uses list[str], tags uses set[str], identifier_name uses tuple[int, str], and counts uses dict[str, int]. The return annotation describes the result. note: str | None still requires an argument; adding = None permits omission. These are interface descriptions, not runtime checks. ⟦A.f1 A.f2 A.f3 A:tb5⟧
(misconception) Adding a hint does not add runtime validation. Accepting None and allowing omission are different decisions. ⟦A.f1 A.f2 A:tb6⟧

### s04 · check · Check the distinction
Practical Python type annotations for service interfaces — 

### s05 · hands_on · Apply the rule
Practical Python type annotations for service interfaces — 

### s06 · explainer · Establish the rule
Python classes and instances for service models — 
(intro) Two order drafts need independent items, even though they share the class’s behavior. ⟦B:tb1⟧
(definition) A class statement creates a class with methods defining behavior. Calling that class creates an instance. ⟦B.f1 B:tb2⟧
(mechanism) __init__(self, ...) initializes an instance; self.attribute stores its state. An instance method receives that instance first. Instance variables are specific to each instance; class variables are shared. For independent mutable values, create a fresh value on self inside __init__. ⟦B.f2 B.f3 B.f4 B:tb3⟧
[DIAGRAM] nodes=['Draft: shared method definitions', 'draft_a: self.items → fresh collection', 'draft_b: self.items → another fresh collection', 'Alternative: one mutable class items shared by both'] edges=[('n1', 'n2', 'calling Draft'), ('n1', 'n3', 'calling Draft'), ('n2', 'n4', 'shared-state contrast'), ('n3', 'n4', 'shared-state contrast')] alt: Draft: shared method definitions → draft_a: self.items → fresh collection → draft_b: self.items → another fresh collection → Alternative: one mutable class items shared by both

### s07 · explainer · Why the distinction matters
Python classes and instances for service models — 
(walkthrough) Change only draft_a’s items and inspect draft_b. Calling Draft twice does not fix shared mutable class state. Assign a fresh collection to self during initialization. Shared methods use self to identify the instance being changed. ⟦B.f1 B.f2 B.f3 B.f4 B:tb4⟧

### s08 · explainer · Reason through an example
Python classes and instances for service models — 
(walkthrough) Draft defines behavior; draft_a and draft_b are instances. A fresh self.items in each __init__ gives each draft its own collection. One mutable items value on the class can instead be shared. Follow ownership: the method’s first argument identifies the instance, not a new copy of every attribute. ⟦B.f1 B.f2 B.f3 B.f4 B:tb5⟧
(misconception) Two instances can still share a mutable class variable. Initialize fresh mutable state on self when independence is required. ⟦B.f4 B:tb6⟧

### s09 · check · Check the distinction
Python classes and instances for service models — 

### s10 · hands_on · Apply the rule
Python classes and instances for service models — 

### s11 · recap · Keep these takeaways
Review — 
(takeaway) Hints describe types, not runtime checks. None permission differs from argument omission. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(takeaway) Classes share behavior; fresh self state gives drafts independent mutable collections. ⟦B.f1 B.f2 B.f3 B.f4 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧
[UP NEXT] Context-managed resource cleanup: Continue to tile_005.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit tile_003.s04
(definition) Type | None permits None, while a default such as = None separately permits omitting a Python function argument. ⟦A.f2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(example) Contrast note: str | None with note: str | None = None: only the second permits omission. ⟦A.f2 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r02 · Revisit tile_003.s05
(definition) Annotate a function parameter with name: Type and its return value with -> Type; Python type hints alone do not enforce runtime validation. ⟦A.f1 A:tb2 A:tb4 A:tb5 A:tb6⟧
(definition) list[str], set[str], tuple[int, str] and dict[str, int] annotate a list of strings, a set of strings, a two-element integer/string tuple and a string-to-integer dictionary respectively. ⟦A.f3 A:tb3 A:tb5⟧
(example) Contrast note: str | None with note: str | None = None: only the second permits omission. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r03 · Revisit tile_003.s09
(definition) A class statement creates a class whose methods define behavior, and calling the class creates an instance. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(definition) Define __init__(self, ...) to initialize an instance and assign self.attribute to store that instance's state; an instance method receives that instance as its first argument. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(example) Contrast a fresh self.items in each Draft initializer with one mutable items on Draft: only the former supplies independent collections. ⟦B.f1 B.f2 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r04 · Revisit tile_003.s10
(definition) Instance variables hold data specific to each instance, while class variables are shared by instances of the class. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(definition) A mutable class variable can be shared unintentionally; initialize a fresh mutable value on self inside __init__ when instances need independent values. ⟦B.f4 B:tb3 B:tb4 B:tb5 B:tb6⟧
(example) Contrast a fresh self.items in each Draft initializer with one mutable items on Draft: only the former supplies independent collections. ⟦B.f3 B.f4 B:tb3 B:tb4 B:tb5 B:tb6⟧

=========

# EVALUATOR PACKET — Context-managed resource cleanup · Cooperative concurrency with async and await (tile_005)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.context_managed_cleanup — Context-managed resource cleanup
B = python.cooperative_async — Cooperative concurrency with async and await

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.context_managed_cleanup)   objective: Use context-managed cleanup: manage one acquired resource.
A.f1: Use with manager as resource: followed by an indented block to enter a managed resource scope.   [sources: python_tutorial#https://docs.python.org/3/reference/compound_stmts.html#the-with-statement]
A.f2: If __enter__ returns successfully, the with statement calls __exit__ when the block exits normally or through an exception.   [sources: python_tutorial#https://docs.python.org/3/reference/compound_stmts.html#the-with-statement]
A.f3: __exit__ receives exception details on exceptional exit and can suppress the exception by returning a true value; cleanup does not itself imply suppression.   [sources: python_tutorial#https://docs.python.org/3/reference/compound_stmts.html#the-with-statement]
A.f4: Using with open(...) as file closes the file after the block, including when an exception occurs.   [sources: python_tutorial#https://docs.python.org/3/tutorial/errors.html#predefined-clean-up-actions]
note: Establish this first: Lexical boundaries guarantee exit cleanup.
note: Stay within the current objective: Use context-managed cleanup. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Predict cleanup after success and failure.
PRACTICE ANCHOR (live_code): Manage one supplied file resource using with open(...) as file, keeping the file-reading operation inside the indented block.  SUCCESS: The file-reading operation runs inside the managed scope, and the file closes after both normal completion and a supplied failure during that operation.
ASSESSMENT ANCHOR: predict_file_cleanup_after_normal_and_exceptional_exit facts=['f1', 'f2', 'f4']
ASSESSMENT ANCHOR: identify_successful_entry_as_the_exit_call_condition facts=['f2']
ASSESSMENT ANCHOR: distinguish_resource_cleanup_from_exception_suppression facts=['f3']

## SOURCE FACTS — B (python.cooperative_async)   objective: Reason about cooperative coroutine execution and conditional suspension at await: trace one coroutine with an immediately completing await and an await on a pending I/O operation, identifying where another runnable task can execute.
B.f1: Calling an async def function produces a coroutine; awaiting it runs it and returns its result when it completes.   [sources: python_tutorial#https://docs.python.org/3/library/asyncio-task.html#coroutines, python_tutorial#https://docs.python.org/3/reference/expressions.html#await-expression]
B.f2: An event loop uses cooperative scheduling, running one task at a time and allowing other tasks to run while a task waits on a pending future.   [sources: python_tutorial#https://docs.python.org/3/library/asyncio-task.html#task-object]
B.f3: An await can complete without suspension when its awaited operation completes immediately; the presence of await alone does not establish a switch to another task.   [sources: python_tutorial#https://docs.python.org/3/reference/datamodel.html#coroutines, python_tutorial#https://docs.python.org/3/library/asyncio-task.html#task-object]
B.f4: When a future awaited by a suspended task completes, execution of that task's coroutine resumes.   [sources: python_tutorial#https://docs.python.org/3/library/asyncio-task.html#task-object]
B.f5: To trace suspension concretely, mark await asyncio.sleep(...) as a suspension point; sleep suspends the current task, including when its delay is zero.   [sources: python_tutorial#https://docs.python.org/3/library/asyncio-task.html#sleeping]
note: Establish this first: Await yields control only when the awaited operation suspends; an immediately completing coroutine can return without suspending the current task..
note: Stay within the current objective: Reason about cooperative coroutine execution and conditional suspension at await. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Predict whether an await continues immediately or suspends the current task, and how a suspended task resumes when its awaited operation is ready.
PRACTICE ANCHOR (live_code): Annotate supplied coroutine code for task A: trace an immediately completing await, an await on a supplied pending I/O future, and await asyncio.sleep(0). Identify suspension points, opportunities for another runnable task to execute, and where A continues after the pending future completes.  SUCCESS: The annotations distinguish coroutine creation from execution, show no required handover at the immediately completing await, mark the pending-future await and zero-delay sleep as suspension points, and place A's continuation after its awaited future becomes ready without asserting an exact task execution order.
ASSESSMENT ANCHOR: predict_immediate_coroutine_completion_without_suspension facts=['f1', 'f3']
ASSESSMENT ANCHOR: identify_pending_await_as_cooperative_scheduling_opportunity facts=['f2', 'f3']
ASSESSMENT ANCHOR: trace_coroutine_resumption_after_future_completion facts=['f4']
ASSESSMENT ANCHOR: identify_asyncio_sleep_suspension_including_zero_delay facts=['f5']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): ASGI server and application request lifecycle; Application lifespan; Async-compatible external HTTP requests; CORS preflight behavior; Choosing HTTP success and failure statuses; Choosing def versus async def from I/O behavior without blocking the event loop; Cooperative concurrency with async and await; Custom validation for domain invariants; Declarative field validation constraints; Expected API failures with HTTPException; FastAPI application and path-operation declarations; Isolated Python environments and compatible dependency installation; Local password hashing and credential verification without an OAuth password grant; Modular FastAPI application composition with APIRouter; Nested request-data models; Orm entity mapping; Orm relationship mapping; Pydantic V2 model construction and input conversion; Python decorators as callable wrappers; Python package organization for a service; Reproducible service dependency declarations; Resource-oriented REST URLs and CRUD contracts; Response-model serialization and private-field exclusion; Service-schema integrity constraints; Typed path and query input binding; Validated environment-based configuration with fail-fast startup

## LESSON, in learner order

### s01 · explainer · Establish the rule
Context-managed resource cleanup — 
(intro) File-reading work may fail. Mark cleanup on both normal and exceptional exit. ⟦A:tb1⟧
(definition) Use with manager as resource: and an indented block to enter a managed resource scope. ⟦A.f1 A:tb2⟧
(mechanism) After __enter__ succeeds, __exit__ runs on normal or exceptional block exit. It receives exception details and can suppress an exception by returning true; cleanup alone does not imply suppression. with open(...) as file closes the file after the block, even on an exception. ⟦A.f2 A.f3 A.f4 A:tb3⟧
[DIAGRAM] nodes=['with open("orders.txt") as file:', '    file.read() inside managed scope', 'Normal exit → file closed', 'Exception exit → file closed', 'General __exit__: true may suppress; cleanup alone does not'] edges=[('n1', 'n2', 'successful entry'), ('n2', 'n3', 'normal departure'), ('n2', 'n4', 'exceptional departure'), ('n4', 'n5', 'separate suppression decision')] alt: with open("orders.txt") as file: →     file.read() inside managed scope → Normal exit → file closed → Exception exit → file closed → General __exit__: true may suppress; cleanup alone does not

### s02 · explainer · Why the distinction matters
Context-managed resource cleanup — 
(walkthrough) Mark successful entry, work inside the block and departure. Normal departure and an exception both close the file. For a general manager, a true __exit__ return may suppress an exception, but releasing the resource is a separate decision. A cleanup trace is not proof the work succeeded. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧

### s03 · explainer · Reason through an example
Context-managed resource cleanup — 
(walkthrough) In with open(...) as file, keep reading inside the indented scope. After successful entry, normal exit closes the file; exceptional exit also closes it. A general manager’s __exit__ receives exception details and may suppress by returning true. Ask separately whether cleanup occurred and whether the exception propagated. ⟦A.f1 A.f2 A.f3 A.f4 A:tb5⟧
(misconception) Successful entry guarantees an exit call, not disappearing exceptions. Cleanup and suppression are separate. ⟦A.f2 A.f3 A:tb6⟧

### s04 · video · Follow the worked trace
Context-managed resource cleanup — 
[VIDEO ] bridge-before:  | bridge-after: 

### s05 · check · Check the distinction
Context-managed resource cleanup — 

### s06 · check · Check the distinction
Context-managed resource cleanup — 

### s07 · hands_on · Apply the rule
Context-managed resource cleanup — 

### s08 · explainer · Establish the rule
Cooperative concurrency with async and await — 
(intro) Trace actual suspension in an asynchronous task; counting await keywords is not enough. ⟦B:tb1⟧
(definition) Calling async def creates a coroutine. Awaiting it runs it and returns its result on completion. ⟦B.f1 B:tb2⟧
(mechanism) The event loop cooperatively runs one task at a time. While a task waits on a pending future, other tasks may run; completion lets the suspended coroutine resume. An immediately completing await need not suspend. asyncio.sleep suspends the current task, even with delay zero. ⟦B.f2 B.f3 B.f4 B.f5 B:tb3⟧
[PROCESS_FLOW] nodes=['Call async function: coroutine created', 'Await: coroutine runs', 'Await immediate work: may not suspend', 'Await pending future: suspend; other tasks may run', 'Future completes: task resumes', 'await asyncio.sleep(0): suspends'] edges=[('n1', 'n2', ''), ('n2', 'n3', ''), ('n3', 'n4', 'task_a continues'), ('n4', 'n5', ''), ('n5', 'n6', '')] alt: Call async function: coroutine created; Await: coroutine runs; Await immediate work: may not suspend; Await pending future: suspend; other tasks may run; Future completes: task resumes; await asyncio.sleep(0): suspends

### s09 · explainer · Why the distinction matters
Cooperative concurrency with async and await — 
(walkthrough) An immediately completing await leaves no pending wait requiring a handover. Waiting on a pending future gives another runnable task an opportunity to run; completion lets the first resume. This does not establish which task runs next. asyncio.sleep(0) still suspends. ⟦B.f2 B.f3 B.f4 B.f5 B:tb4⟧

### s10 · explainer · Reason through an example
Cooperative concurrency with async and await — 
(walkthrough) In task_a, calling immediate creates a coroutine; awaiting it runs it and obtains its result. If it completes immediately, no suspension is required. Awaiting pending_io can suspend until its future completes, after which task_a resumes. await asyncio.sleep(0) explicitly suspends. Mark those distinctions without promising an exact interleaving. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb5⟧
(misconception) An await is not proof that another task ran. Immediate work may finish without suspension; asyncio.sleep suspends even at zero delay. ⟦B.f3 B.f5 B:tb6⟧

### s11 · check · Check the distinction
Cooperative concurrency with async and await — 

### s12 · hands_on · Apply the rule
Cooperative concurrency with async and await — 

### s13 · recap · Keep these takeaways
Review — 
(takeaway) Successful entry leads to managed exit; cleanup and exception suppression remain separate. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(takeaway) Trace actual suspension. Immediate await may not suspend; asyncio.sleep(0) does. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧
[UP NEXT] Python decorators as callable wrappers: Continue to tile_007.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit tile_005.s05
(definition) If __enter__ returns successfully, the with statement calls __exit__ when the block exits normally or through an exception. ⟦A.f2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(example) Contrast a file closing after failed reading with the failure disappearing: closure does not itself suppress the exception. ⟦A.f2 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r02 · Revisit tile_005.s06
(definition) __exit__ receives exception details on exceptional exit and can suppress the exception by returning a true value; cleanup does not itself imply suppression. ⟦A.f3 A:tb3 A:tb4 A:tb5 A:tb6⟧
(example) Contrast a file closing after failed reading with the failure disappearing: closure does not itself suppress the exception. ⟦A.f3 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r03 · Revisit tile_005.s07
(definition) Use with manager as resource: followed by an indented block to enter a managed resource scope. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) If __enter__ returns successfully, the with statement calls __exit__ when the block exits normally or through an exception. ⟦A.f2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(definition) Using with open(...) as file closes the file after the block, including when an exception occurs. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(example) Contrast a file closing after failed reading with the failure disappearing: closure does not itself suppress the exception. ⟦A.f1 A.f2 A.f4 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r04 · Revisit tile_005.s11
(definition) An event loop uses cooperative scheduling, running one task at a time and allowing other tasks to run while a task waits on a pending future. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(definition) An await can complete without suspension when its awaited operation completes immediately; the presence of await alone does not establish a switch to another task. ⟦B.f3 B:tb3 B:tb4 B:tb5 B:tb6⟧
(example) Contrast await immediate() with await asyncio.sleep(0): the first can finish without suspension; sleep suspends even at zero. ⟦B.f2 B.f3 B:tb3 B:tb4 B:tb5 B:tb6⟧
### r05 · Revisit tile_005.s12
(definition) Calling an async def function produces a coroutine; awaiting it runs it and returns its result when it completes. ⟦B.f1 B:tb2 B:tb5⟧
(definition) An await can complete without suspension when its awaited operation completes immediately; the presence of await alone does not establish a switch to another task. ⟦B.f3 B:tb3 B:tb4 B:tb5 B:tb6⟧
(definition) When a future awaited by a suspended task completes, execution of that task's coroutine resumes. ⟦B.f4 B:tb3 B:tb4 B:tb5⟧
(definition) To trace suspension concretely, mark await asyncio.sleep(...) as a suspension point; sleep suspends the current task, including when its delay is zero. ⟦B.f5 B:tb3 B:tb4 B:tb5 B:tb6⟧
(example) Contrast await immediate() with await asyncio.sleep(0): the first can finish without suspension; sleep suspends even at zero. ⟦B.f1 B.f3 B.f4 B.f5 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧

=========

# EVALUATOR PACKET — Python decorators as callable wrappers (tile_007)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.decorator_wrappers — Python decorators as callable wrappers

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.decorator_wrappers)   objective: Understand decorators as callable wrappers: write and inspect one simple callable wrapper.
A.f1: A decorator expression is evaluated when a function is defined, called with the function object, and its returned value is bound to the function name.   [sources: python_tutorial#https://docs.python.org/3/reference/compound_stmts.html#function-definitions]
A.f2: @decorate above def function(...): applies decoration roughly like function = decorate(function).   [sources: python_tutorial#https://docs.python.org/3/reference/compound_stmts.html#function-definitions]
A.f3: A callable wrapper can be built by defining an inner function that calls the supplied function and returning that inner function from the decorator.   [sources: python_tutorial#https://docs.python.org/3/reference/compound_stmts.html#function-definitions, python_tutorial#https://docs.python.org/3/tutorial/controlflow.html#defining-functions]
note: Establish this first: Decoration replaces or registers a callable by applying another callable.
note: Stay within the current objective: Understand decorators as callable wrappers. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Trace the callable before and after decoration.
PRACTICE ANCHOR (live_code): Write a simple decorate callable that accepts function, defines an inner callable that calls function, and returns that inner callable. Inspect the binding produced by explicit decoration and by @decorate.  SUCCESS: The decorator returns the inner callable without calling it. The learner identifies the original callable, the replacement binding, and the later call path through the wrapper to the original callable.
ASSESSMENT ANCHOR: trace_function_binding_before_and_after_decoration facts=['f1', 'f2']
ASSESSMENT ANCHOR: trace_call_from_returned_wrapper_to_original_function facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): ASGI server and application request lifecycle; Application lifespan; Async-compatible external HTTP requests; CORS preflight behavior; Choosing HTTP success and failure statuses; Choosing def versus async def from I/O behavior without blocking the event loop; Custom validation for domain invariants; Declarative field validation constraints; Depends; Expected API failures with HTTPException; FastAPI application and path-operation declarations; Isolated Python environments and compatible dependency installation; Local password hashing and credential verification without an OAuth password grant; Modular FastAPI application composition with APIRouter; Nested request-data models; Orm entity mapping; Orm relationship mapping; Pydantic V2 model construction and input conversion; Python package organization for a service; Reproducible service dependency declarations; Resource-oriented REST URLs and CRUD contracts; Response-model serialization and private-field exclusion; Service-schema integrity constraints; Typed path and query input binding; Validated environment-based configuration with fail-fast startup

## LESSON, in learner order

### s01 · explainer · Establish the rule
Python decorators as callable wrappers — 
(intro) A decorator can add behavior around a service callable without rewriting that callable. ⟦A:tb1⟧
(definition) At function definition, the decorator expression is evaluated and called with the function object. Its returned value becomes the function name’s binding. ⟦A.f1 A:tb2⟧
(mechanism) @decorate above def function(...): is roughly function = decorate(function). Build a callable wrapper by defining an inner function that calls the supplied function, then returning the inner function. ⟦A.f2 A.f3 A:tb3⟧
[DIAGRAM] nodes=['@decorate above def function', 'Definition: decorate(function object)', 'Returned inner_function bound to function name', 'Later call: inner_function calls original function', 'Equivalent binding: function = decorate(function)'] edges=[('n1', 'n2', ''), ('n2', 'n3', ''), ('n3', 'n4', ''), ('n5', 'n3', '')] alt: @decorate above def function → Definition: decorate(function object) → Returned inner_function bound to function name → Later call: inner_function calls original function → Equivalent binding: function = decorate(function)
[CODE python]
def decorate(function):
    def inner_function():
        return function()
    return inner_function

@decorate
def function():
    return "synthetic order"

result = function()
  annotations: ['Definition time binds the returned inner callable to function. The later call enters inner_function, which calls the original function.']

### s02 · explainer · Reason through an example
Python decorators as callable wrappers — 
(walkthrough) Trace two times: definition applies decorate to the function object and binds the returned value; a later call uses that binding. If the returned value is an inner wrapper, that later call goes through it to the original function. The decorator receives the function, not the result of calling it with service data. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) A decorator is not a comment. Its returned value becomes the function name’s binding. ⟦A.f1 A.f2 A:tb5⟧

### s03 · check · Check the distinction
Python decorators as callable wrappers — 

### s04 · hands_on · Apply the rule
Python decorators as callable wrappers — 

### s05 · recap · Keep these takeaways
Review — 
(takeaway) Decoration binds its returned value at definition; later calls use that binding. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Isolated Python environments and compatible dependency installation: Continue to tile_008.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit tile_007.s03
(definition) A callable wrapper can be built by defining an inner function that calls the supplied function and returning that inner function from the decorator. ⟦A.f3 A:tb3 A:tb4⟧
(example) Decoration binds its returned value at definition; later calls use that binding. ⟦A.f3 A:tb3 A:tb4⟧
### r02 · Revisit tile_007.s04
(definition) A decorator expression is evaluated when a function is defined, called with the function object, and its returned value is bound to the function name. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) @decorate above def function(...): applies decoration roughly like function = decorate(function). ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) A callable wrapper can be built by defining an inner function that calls the supplied function and returning that inner function from the decorator. ⟦A.f3 A:tb3 A:tb4⟧
(example) Decoration binds its returned value at definition; later calls use that binding. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Isolated Python environments and compatible dependency installation (tile_008)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.isolated_environments — Isolated Python environments and compatible dependency installation

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.isolated_environments)   objective: Install service dependencies in an isolated environment: create an environment and install a compatible dependency set.
A.f1: A virtual environment has a particular Python installation and its own installed packages, allowing applications to use different dependency versions.   [sources: python_tutorial#https://docs.python.org/3/tutorial/venv.html#virtual-environments-and-packages]
A.f2: Create an environment with python -m venv .venv and activate it with source .venv/bin/activate on Unix or .venv\Scripts\activate on Windows.   [sources: python_tutorial#https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments]
A.f3: Use python -m pip install package within the environment to install a dependency, and python -m pip show package to inspect its installed version and location.   [sources: python_tutorial#https://docs.python.org/3/tutorial/venv.html#managing-packages-with-pip]
A.f4: Check which python on Unix or where python on Windows to confirm that the interpreter path belongs to the activated environment.   [sources: fastapi_docs_tutorial#https://tiangolo.com/guides/virtual-environments/#check-the-virtual-environment-is-active]
note: Establish this first: An environment isolates an interpreter's dependency namespace.
note: Stay within the current objective: Install service dependencies in an isolated environment. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Demonstrate interpreter and dependency isolation from the host.
PRACTICE ANCHOR (live_code): Create and activate .venv for one project, verify its interpreter path, and install a supplied dependency set compatible with the available Python installation. Inspect each installed dependency's version and location.  SUCCESS: The interpreter path belongs to .venv, installation succeeds for every supplied dependency, and package inspection reports each dependency's installed version and a location inside .venv rather than the host package location.
ASSESSMENT ANCHOR: explain_interpreter_and_dependency_isolation facts=['f1']
ASSESSMENT ANCHOR: create_activate_and_verify_environment_interpreter facts=['f2', 'f4']
ASSESSMENT ANCHOR: verify_installed_dependency_version_and_environment_location facts=['f3', 'f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): ASGI server and application request lifecycle; Application lifespan; Async-compatible external HTTP requests; CORS preflight behavior; Choosing HTTP success and failure statuses; Choosing def versus async def from I/O behavior without blocking the event loop; Custom validation for domain invariants; Declarative field validation constraints; Depends; Expected API failures with HTTPException; FastAPI application and path-operation declarations; Local password hashing and credential verification without an OAuth password grant; Modular FastAPI application composition with APIRouter; Nested request-data models; Orm entity mapping; Orm relationship mapping; Outbound timeouts; Pydantic V2 model construction and input conversion; Python package organization for a service; Reproducible service dependency declarations; Resource-oriented REST URLs and CRUD contracts; Response-model serialization and private-field exclusion; Service-schema integrity constraints; Typed path and query input binding; Validated environment-based configuration with fail-fast startup

## LESSON, in learner order

### s01 · explainer · Establish the rule
Isolated Python environments and compatible dependency installation — 
(intro) Two projects can need different dependency versions. Identify which interpreter and packages each uses. ⟦A:tb1⟧
(definition) A virtual environment has a particular Python installation and its own installed packages, allowing applications to use different dependency versions. ⟦A.f1 A:tb2⟧
(mechanism) Create it with python -m venv .venv. Activate using source .venv/bin/activate on Unix or .venv\Scripts\activate on Windows. Install with python -m pip install package; inspect version and location with python -m pip show package. Confirm the interpreter path with which python on Unix or where python on Windows. ⟦A.f2 A.f3 A.f4 A:tb3⟧
[SIDE_BY_SIDE] Package versions may match while interpreter paths and package locations remain separate. left_label: Registered host comparison | right_label: Illustrative activated .venv inspection; paths vary
  left:
[CODE bash]
Interpreter: /home/azureuser/env/bin/python3
jsonschema version: 4.26.0
Package location: /home/azureuser/env/lib/python3.12/site-packages
  annotations: []
  right:
[CODE bash]
Interpreter: <project>/.venv/bin/python
jsonschema version: 4.26.0
Package location: <project>/.venv/lib/python3.12/site-packages
  annotations: []
[CODE bash]
python -m venv .venv
source .venv/bin/activate
which python
python -m pip install jsonschema
python -m pip show jsonschema

  annotations: ['Unix shell commands']
[CODE bash]
python -m venv .venv
.venv\Scripts\activate
where python
python -m pip install jsonschema
python -m pip show jsonschema

  annotations: ['Windows shell commands']

### s02 · explainer · Why the distinction matters
Isolated Python environments and compatible dependency installation — 
(walkthrough) Compare interpreter paths and package locations before assuming a project changed versions. The resolved Python path identifies the interpreter; pip show identifies its package version and location. Each environment has its own installed packages and a particular Python installation. ⟦A.f1 A.f3 A.f4 A:tb4⟧

### s03 · explainer · Reason through an example
Isolated Python environments and compatible dependency installation — 
(walkthrough) Create and activate .venv, then check which python or where python. With that interpreter identified, install the supplied dependency using python -m pip install and inspect it using python -m pip show. Compare both version and location. Repeat for another project rather than assuming both commands use the same environment. ⟦A.f1 A.f2 A.f3 A.f4 A:tb5⟧
(misconception) Activation alone is not inspection. Confirm the interpreter path, then inspect the package’s version and location. ⟦A.f3 A.f4 A:tb6⟧

### s04 · check · Check the distinction
Isolated Python environments and compatible dependency installation — 

### s05 · hands_on · Apply the rule
Isolated Python environments and compatible dependency installation — 

### s06 · recap · Keep these takeaways
Review — 
(takeaway) Each environment has its own packages. Verify interpreter path and package version and location. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
[UP NEXT] ASGI server and application request lifecycle: Continue to tile_009.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit tile_008.s04
(definition) Use python -m pip install package within the environment to install a dependency, and python -m pip show package to inspect its installed version and location. ⟦A.f3 A:tb3 A:tb4 A:tb5 A:tb6⟧
(definition) Check which python on Unix or where python on Windows to confirm that the interpreter path belongs to the activated environment. ⟦A.f4 A:tb3 A:tb4 A:tb5 A:tb6⟧
(example) Each environment has its own packages. Verify interpreter path and package version and location. ⟦A.f3 A.f4 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r02 · Revisit tile_008.s05
(definition) A virtual environment has a particular Python installation and its own installed packages, allowing applications to use different dependency versions. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Create an environment with python -m venv .venv and activate it with source .venv/bin/activate on Unix or .venv\Scripts\activate on Windows. ⟦A.f2 A:tb3 A:tb5⟧
(definition) Use python -m pip install package within the environment to install a dependency, and python -m pip show package to inspect its installed version and location. ⟦A.f3 A:tb3 A:tb4 A:tb5 A:tb6⟧
(definition) Check which python on Unix or where python on Windows to confirm that the interpreter path belongs to the activated environment. ⟦A.f4 A:tb3 A:tb4 A:tb5 A:tb6⟧
(example) Each environment has its own packages. Verify interpreter path and package version and location. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧

=========

# EVALUATOR PACKET — ASGI server and application request lifecycle (tile_009)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = asgi.request_lifecycle — ASGI server and application request lifecycle

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (asgi.request_lifecycle)   objective: Explain ASGI lifecycle: trace one request.
A.f1: An ASGI server handles the network connection and invokes an application callable through the ASGI interface.   [sources: fastapi_docs_advanced#https://florimond.dev/en/posts/2019/08/introduction-to-asgi-async-python-web/#asgi-basics]
A.f2: The application callable has the shape async def app(scope, receive, send), where scope describes the connection and receive and send exchange protocol events.   [sources: fastapi_docs_advanced#https://florimond.dev/en/posts/2019/08/introduction-to-asgi-async-python-web/#asgi-basics]
A.f3: Trace the application receiving http.request events through receive(), then sending http.response.start with status and headers followed by http.response.body through send().   [sources: fastapi_docs_advanced#https://asgi.readthedocs.io/en/latest/specs/www.html#request-receive-event, fastapi_docs_advanced#https://asgi.readthedocs.io/en/latest/specs/www.html#response-start-send-event, fastapi_docs_advanced#https://asgi.readthedocs.io/en/latest/specs/www.html#response-body-send-event]
note: Establish this first: Servers adapt traffic to application protocol lifecycle.
note: Stay within the current objective: Explain ASGI lifecycle. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Locate server and application responsibilities.
PRACTICE ANCHOR (live_code): Complete async def app(scope, receive, send) to trace one HTTP request: await the supplied receive callable, then send response metadata followed by body content using the supplied send callable.  SUCCESS: The application receives the supplied http.request event and sends http.response.start with the supplied status and headers before sending http.response.body with the supplied body. The trace identifies network handling and application invocation as server responsibilities.
ASSESSMENT ANCHOR: locate_server_network_and_invocation_responsibilities facts=['f1']
ASSESSMENT ANCHOR: identify_application_callable_and_event_interface facts=['f2']
ASSESSMENT ANCHOR: trace_application_request_and_response_events facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Application lifespan; Async-compatible external HTTP requests; CORS preflight behavior; Choosing HTTP success and failure statuses; Choosing def versus async def from I/O behavior without blocking the event loop; Custom validation for domain invariants; Declarative field validation constraints; Depends; Expected API failures with HTTPException; FastAPI application and path-operation declarations; Local password hashing and credential verification without an OAuth password grant; Modular FastAPI application composition with APIRouter; Nested request-data models; Orm entity mapping; Orm relationship mapping; Outbound timeouts; Pydantic V2 model construction and input conversion; Python package organization for a service; Reproducible service dependency declarations; Resource-oriented REST URLs and CRUD contracts; Response-model serialization and private-field exclusion; Separating transport, testable business logic and persistence responsibilities; Service-schema integrity constraints; Typed path and query input binding; Validated environment-based configuration with fail-fast startup

## LESSON, in learner order

### s01 · explainer · Establish the rule
ASGI server and application request lifecycle — 
(intro) The network server and Python application have different roles. ASGI connects them through protocol events. ⟦A:tb1⟧
(definition) The ASGI server handles the network connection and invokes the application callable through ASGI. ⟦A.f1 A:tb2⟧
(mechanism) The callable is async def app(scope, receive, send). scope describes the connection; receive and send exchange events. Receive http.request through receive(), then send http.response.start with status and headers, followed by http.response.body through send(). ⟦A.f2 A.f3 A:tb3⟧
[PROCESS_FLOW] nodes=['ASGI server: network connection', 'Invoke async app(scope, receive, send)', 'scope: connection description', 'receive(): http.request', 'send(): http.response.start (status, headers)', 'send(): http.response.body'] edges=[('n1', 'n2', ''), ('n2', 'n3', 'connection context'), ('n2', 'n4', 'protocol event'), ('n4', 'n5', ''), ('n5', 'n6', '')] alt: ASGI server: network connection; Invoke async app(scope, receive, send); scope: connection description; receive(): http.request; send(): http.response.start (status, headers); send(): http.response.body

### s02 · explainer · Why the distinction matters
ASGI server and application request lifecycle — 
(walkthrough) Keep scope separate from events: it describes the connection, while receive and send exchange events. Send response status and headers in http.response.start before the http.response.body event. The server owns network handling; the application participates through the ASGI callable. ⟦A.f1 A.f2 A.f3 A:tb4⟧

### s03 · explainer · Reason through an example
ASGI server and application request lifecycle — 
(walkthrough) Trace the server invoking app with scope, receive and send. The application receives http.request, sends http.response.start containing status and headers, then sends http.response.body. Draw separate arrows for metadata and body, not one handler return. Keep the network connection in the server box. ⟦A.f1 A.f2 A.f3 A:tb5⟧
(misconception) The application does not directly own all network handling. The ASGI server handles the connection and invokes the callable. ⟦A.f1 A:tb6⟧

### s04 · check · Check the distinction
ASGI server and application request lifecycle — 

### s05 · hands_on · Apply the rule
ASGI server and application request lifecycle — 

### s06 · recap · Keep these takeaways
Review — 
(takeaway) The server owns network handling; app exchanges request, response-start and response-body events. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
[UP NEXT] Local password hashing and credential verification without an OAuth password grant: Continue to tile_010.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit tile_009.s04
(definition) Trace the application receiving http.request events through receive(), then sending http.response.start with status and headers followed by http.response.body through send(). ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) The server owns network handling; app exchanges request, response-start and response-body events. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit tile_009.s05
(definition) An ASGI server handles the network connection and invokes an application callable through the ASGI interface. ⟦A.f1 A:tb2 A:tb4 A:tb5 A:tb6⟧
(definition) The application callable has the shape async def app(scope, receive, send), where scope describes the connection and receive and send exchange protocol events. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Trace the application receiving http.request events through receive(), then sending http.response.start with status and headers followed by http.response.body through send(). ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) The server owns network handling; app exchanges request, response-start and response-body events. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧

=========

# EVALUATOR PACKET — Local password hashing and credential verification without an OAuth password grant (tile_010)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = auth.local_password_verification — Local password hashing and credential verification without an OAuth password grant

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (auth.local_password_verification)   objective: Verify passwords securely: use one established hashing library.
A.f1: Password storage should use password hashing rather than plaintext storage or reversible encryption.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#introduction]
A.f2: Salts distinguish password hashes, while an adjustable work factor increases the cost of password guessing.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#salting, owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#using-work-factors]
A.f3: Create PasswordHash.recommended() from pwdlib, store the result of its hash(password) method, and verify a submitted password with verify(plain_password, stored_hash).   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#hash-and-verify-the-passwords]
note: Establish this first: Passwords require one-way work-factor-based verification.
note: Stay within the current objective: Verify passwords securely. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify safe storage and verification designs.
PRACTICE ANCHOR (live_code): Use pwdlib to create a recommended password hasher, hash a synthetic password, and verify matching and nonmatching submissions against the stored hash.  SUCCESS: The stored value is the result of hash(password), and verify(plain_password, stored_hash) returns true for the matching submission and false for a different submission.
ASSESSMENT ANCHOR: identify_safe_password_storage facts=['f1']
ASSESSMENT ANCHOR: distinguish_salt_and_work_factor_roles facts=['f2']
ASSESSMENT ANCHOR: identify_correct_pwdlib_hashing_and_verification facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Application lifespan; Async-compatible external HTTP requests; Bounded in-process background work and nondurable delivery limits; CORS preflight behavior; Choosing HTTP success and failure statuses; Choosing def versus async def from I/O behavior without blocking the event loop; Custom validation for domain invariants; Declarative field validation constraints; Depends; Expected API failures with HTTPException; FastAPI application and path-operation declarations; Modular FastAPI application composition with APIRouter; Nested request-data models; Orm entity mapping; Orm relationship mapping; Outbound timeouts; Pydantic V2 model construction and input conversion; Python package organization for a service; Reproducible service dependency declarations; Resource-oriented REST URLs and CRUD contracts; Response-model serialization and private-field exclusion; Separating transport, testable business logic and persistence responsibilities; Service-schema integrity constraints; Typed path and query input binding; Validated environment-based configuration with fail-fast startup

## LESSON, in learner order

### s01 · explainer · Establish the rule
Local password hashing and credential verification without an OAuth password grant — 
(intro) For a local password check, store verification material rather than a password intended to be recovered later. ⟦A:tb1⟧
(definition) Use password hashing, not plaintext storage or reversible encryption. ⟦A.f1 A:tb2⟧
(mechanism) Salts distinguish hashes; an adjustable work factor increases guessing cost. Create pwdlib’s PasswordHash.recommended(), store hash(password), and check submissions with verify(plain_password, stored_hash). ⟦A.f2 A.f3 A:tb3⟧
(example) Use the registered synthetic passwords. Create the recommended hasher, store its hash(password) result, then supply the submitted plaintext first and stored hash second to verify. Salt distinguishes hashes; work factor increases guessing cost. Do not replace hashing with reversible storage. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) Verification checks a submission against a stored hash. It does not recover the original password through decryption. ⟦A.f1 A.f3 A:tb5⟧
[CODE python]
from pwdlib import PasswordHash

password = "synthetic-order-password"
different_password = "different-synthetic-password"
password_hash = PasswordHash.recommended()
stored_hash = password_hash.hash(password)
matching_result = password_hash.verify(password, stored_hash)
nonmatching_result = password_hash.verify(different_password, stored_hash)

  annotations: ['Create the recommended hasher and store the hash, not plaintext.', 'Submitted password first; stored hash second. matching_result is True; nonmatching_result is False. Verification checks the submission without decrypting the stored hash.']

### s02 · check · Check the distinction
Local password hashing and credential verification without an OAuth password grant — 

### s03 · check · Check the distinction
Local password hashing and credential verification without an OAuth password grant — 

### s04 · hands_on · Apply the rule
Local password hashing and credential verification without an OAuth password grant — 

### s05 · recap · Keep these takeaways
Review — 
(takeaway) Store a password hash. Salt distinguishes hashes; work factor increases guessing cost. Verify plaintext first, hash second. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Orm entity mapping: Continue to tile_011.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit tile_010.s02
(definition) Password storage should use password hashing rather than plaintext storage or reversible encryption. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Salts distinguish password hashes, while an adjustable work factor increases the cost of password guessing. ⟦A.f2 A:tb3 A:tb4⟧
(example) Contrast storing hash(password) with storing password: verification needs a stored hash, not recoverable plaintext. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit tile_010.s03
(definition) Create PasswordHash.recommended() from pwdlib, store the result of its hash(password) method, and verify a submitted password with verify(plain_password, stored_hash). ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) Contrast storing hash(password) with storing password: verification needs a stored hash, not recoverable plaintext. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r03 · Revisit tile_010.s04
(example) Contrast storing hash(password) with storing password: verification needs a stored hash, not recoverable plaintext.

=========

# EVALUATOR PACKET — Orm entity mapping (tile_011)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi_backend.orm_entity_mapping — Orm entity mapping

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (fastapi_backend.orm_entity_mapping)   objective: Map entities to database tables: map one entity with a primary key.
A.f1: A mapped class associates Python attributes with a database table's columns; first create the shared base with class Base(DeclarativeBase): pass, then inherit mapped entities from Base and declare attributes with Mapped[Type] and mapped_column(...).   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#establishing-a-declarative-base, sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#declaring-mapped-classes]
A.f2: Declare a primary-key attribute with mapped_column(primary_key=True) to identify persistent rows.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#declaring-mapped-classes]
A.f3: __tablename__ gives the table name in a declarative mapped class, while mapped_column arguments and annotations describe column details.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#declaring-mapped-classes]
note: Establish this first: Entity state is associated with a persistent row identified by a key..
note: Stay within the current objective: Map entities to database tables. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine persistent row identity and columns.
PRACTICE ANCHOR (live_code): Declare a shared Base and map an Order entity to the orders table with an integer id primary-key attribute.  SUCCESS: Order inherits from Base, names the orders table, and declares id using Mapped[int] and mapped_column(primary_key=True).
ASSESSMENT ANCHOR: identify_declared_persistent_row_key facts=['f2']
ASSESSMENT ANCHOR: determine_mapped_table_and_columns facts=['f1', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Application lifespan; Async-compatible external HTTP requests; Bounded in-process background work and nondurable delivery limits; CORS preflight behavior; Choosing HTTP success and failure statuses; Choosing def versus async def from I/O behavior without blocking the event loop; Composing request dependency graphs; Custom validation for domain invariants; Declarative field validation constraints; Depends; Expected API failures with HTTPException; FastAPI application and path-operation declarations; Modular FastAPI application composition with APIRouter; Nested request-data models; Orm relationship mapping; Outbound timeouts; Pydantic V2 model construction and input conversion; Python package organization for a service; Reproducible service dependency declarations; Resource-oriented REST URLs and CRUD contracts; Response-model serialization and private-field exclusion; Separating transport, testable business logic and persistence responsibilities; Service-schema integrity constraints; Typed path and query input binding; Validated environment-based configuration with fail-fast startup

## LESSON, in learner order

### s01 · explainer · Establish the rule
Orm entity mapping — 
(intro) Mapping connects an Order’s Python attributes to database columns and declares row identity. ⟦A:tb1⟧
(definition) Create class Base(DeclarativeBase): pass, then inherit mapped entities from Base. Use Mapped[Type] and mapped_column(...) to associate Python attributes with table columns. ⟦A.f1 A:tb2⟧
(mechanism) mapped_column(primary_key=True) declares persistent row identity. __tablename__ names the table; annotations and mapped_column arguments describe columns. ⟦A.f2 A.f3 A:tb3⟧
[CODE python]
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)

  annotations: ['Shared declarative base.', 'Entity inherits Base and names its table.', 'Integer attribute maps to a column; primary_key=True declares row identity.']

### s02 · explainer · Why the distinction matters
Orm entity mapping — 
(walkthrough) Inspect inheritance, table naming and identity separately. Base is shared by mapped entities; Order inherits it. __tablename__ names orders. Mapped and mapped_column describe attributes’ column associations. A familiar name such as id is not enough: primary_key=True supplies the row-identity role. ⟦A.f1 A.f2 A.f3 A:tb4⟧

### s03 · explainer · Reason through an example
Orm entity mapping — 
(walkthrough) Declare shared Base, then Order(Base) with __tablename__ = "orders". Mapped[int] and mapped_column describe id’s column association; primary_key=True marks persistent row identity. Merely naming an ordinary attribute id is not that declaration. Inspecting mapping is separate from completing a database write. ⟦A.f1 A.f2 A.f3 A:tb5⟧
(misconception) This declaration describes attribute-to-column mapping and row identity, not a completed database write. ⟦A.f1 A.f2 A:tb6⟧

### s04 · check · Check the distinction
Orm entity mapping — 

### s05 · hands_on · Apply the rule
Orm entity mapping — 

### s06 · recap · Keep these takeaways
Review — 
(takeaway) Base, table name and mapped attributes declare association; primary_key=True declares row identity. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
[UP NEXT] CORS preflight behavior: Continue to tile_012.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit tile_011.s04
(definition) Declare a primary-key attribute with mapped_column(primary_key=True) to identify persistent rows. ⟦A.f2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(example) Base, table name and mapped attributes declare association; primary_key=True declares row identity. ⟦A.f2 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r02 · Revisit tile_011.s05
(definition) A mapped class associates Python attributes with a database table's columns; first create the shared base with class Base(DeclarativeBase): pass, then inherit mapped entities from Base and declare attributes with Mapped[Type] and mapped_column(...). ⟦A.f1 A:tb2 A:tb4 A:tb5 A:tb6⟧
(definition) __tablename__ gives the table name in a declarative mapped class, while mapped_column arguments and annotations describe column details. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) Base, table name and mapped attributes declare association; primary_key=True declares row identity. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧

=========

# EVALUATOR PACKET — CORS preflight behavior · Choosing HTTP success and failure statuses (tile_012)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = http.cors_preflight — CORS preflight behavior
B = http.status_selection — Choosing HTTP success and failure statuses

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (http.cors_preflight)   objective: Handle CORS preflight: verify one preflight exchange.
A.f1: A browser preflights some cross-origin requests with OPTIONS to ask whether the intended method and headers are permitted before sending the actual request.   [sources: mdn_http#https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS#preflighted_requests]
A.f2: A CORS preflight includes Origin and Access-Control-Request-Method; Access-Control-Request-Headers identifies requested headers when applicable.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/cors/#cors-preflight-requests]
A.f3: Verify a preflight by sending the caller's Origin and intended method and headers, then comparing Access-Control-Allow-Origin, Access-Control-Allow-Methods and Access-Control-Allow-Headers with that request.   [sources: mdn_http#https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS#preflighted_requests]
A.f4: A credentialed cross-origin response requires an explicit allowed origin rather than * and Access-Control-Allow-Credentials: true.   [sources: mdn_http#https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS#requests_with_credentials]
note: Establish this first: Preflight negotiates browser permission before an operation.
note: Stay within the current objective: Handle CORS preflight. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine whether preflight permits a request.
PRACTICE ANCHOR (tool_simulation): Verify one preflight exchange in a simulated HTTP request tool. Send OPTIONS for the supplied destination with Origin: https://shop.example, Access-Control-Request-Method: PUT, and Access-Control-Request-Headers: content-type, then inspect the supplied response headers.  SUCCESS: Compare Access-Control-Allow-Origin with https://shop.example, check that Access-Control-Allow-Methods permits PUT, and check that Access-Control-Allow-Headers permits content-type. Record whether the preflight permits the intended request without treating permission as completion of PUT. For the supplied credentialed-response check, require the explicit allowed origin and Access-Control-Allow-Credentials: true; reject * as the allowed origin.
ASSESSMENT ANCHOR: identify_preflight_and_intended_request facts=['f1', 'f2']
ASSESSMENT ANCHOR: determine_preflight_permission_from_headers facts=['f2', 'f3']
ASSESSMENT ANCHOR: evaluate_credentialed_origin_requirements facts=['f4']

## SOURCE FACTS — B (http.status_selection)   objective: Select HTTP statuses: assign one resource's statuses.
B.f1: HTTP status classes distinguish informational 1xx, successful 2xx, redirection 3xx, client error 4xx and server error 5xx outcomes.   [sources: rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-15]
B.f2: Use 200 for a successful request, 201 when the request creates a resource, and 204 for successful completion with no response content.   [sources: rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-15.3.1, rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-15.3.2, rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-15.3.5]
B.f3: 400 denotes a perceived client request error, 401 lacks valid authentication credentials, 403 refuses fulfillment, 404 does not find or disclose the target, and 409 conflicts with current resource state.   [sources: rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-15.5.1, rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-15.5.2, rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-15.5.4, rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-15.5.5, rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-15.5.10]
B.f4: 500 denotes an unexpected server condition and 503 denotes temporary inability to handle the request, such as overload or maintenance.   [sources: rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-15.6.1, rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-15.6.4]
note: Establish this first: Status communicates exchange outcome class.
note: Stay within the current objective: Select HTTP statuses. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Choose statuses matching outcomes.
PRACTICE ANCHOR (live_code): Assign integer HTTP statuses to named variables representing successful and failed outcomes for the hypothetical orders workflow, without implementing request handling.  SUCCESS: The order outcome assignments use 200 for successful retrieval, 201 for creation, 204 for successful completion without response content, 400 for a perceived client request error, 401 for missing valid authentication credentials, 403 for refusal, 404 for an order not found or disclosed, 409 for a current-state conflict, 500 for an unexpected server condition, and 503 for temporary inability to handle the request.
ASSESSMENT ANCHOR: classify_http_exchange_outcomes facts=['f1']
ASSESSMENT ANCHOR: choose_success_status_for_outcome facts=['f2']
ASSESSMENT ANCHOR: choose_client_error_status_for_outcome facts=['f3']
ASSESSMENT ANCHOR: distinguish_unexpected_and_temporary_server_failures facts=['f4']

## DATA ASSETS USED
ds.http_status_classes: Five HTTP status classes — columns: status_class_pattern(categorical), meaning(categorical)
   ["1xx","informational"]
   ["2xx","successful"]
   ["3xx","redirection"]
   ["4xx","client error"]
   ["5xx","server error"]
ds.order_outcomes: Orders HTTP outcomes — columns: variable_name(identifier), outcome(categorical), status_class(categorical), selected_status(categorical,digits-as-label)
   ["order_retrieval_status","retrieval","successful",200]
   ["order_creation_status","creation","successful",201]
   ["order_no_content_status","no content","successful",204]
   ["order_request_error_status","request error","client error",400]
   ["order_missing_credentials_status","missing credentials","client error",401]
   ["order_refusal_status","refusal","client error",403]
   ["order_not_found_status","not found","client error",404]
   ["order_conflict_status","conflict","client error",409]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Application lifespan; Async-compatible external HTTP requests; Bounded in-process background work and nondurable delivery limits; Choosing HTTP success and failure statuses; Choosing def versus async def from I/O behavior without blocking the event loop; Composing request dependency graphs; Configuring existing middleware in the request/response stack; Custom validation for domain invariants; Declarative field validation constraints; Depends; Expected API failures with HTTPException; FastAPI application and path-operation declarations; Modular FastAPI application composition with APIRouter; Nested request-data models; Orm relationship mapping; Outbound timeouts; Production ASGI serving versus development reload; Pydantic V2 model construction and input conversion; Python package organization for a service; Reproducible service dependency declarations; Resource-oriented REST URLs and CRUD contracts; Response-model serialization and private-field exclusion; Separating transport, testable business logic and persistence responsibilities; Service-schema integrity constraints; Typed path and query input binding; Validated environment-based configuration with fail-fast startup

## LESSON, in learner order

### s01 · explainer · Establish the rule
CORS preflight behavior — 
(intro) For some cross-origin calls, the browser asks permission before sending the intended method and headers. ⟦A:tb1⟧
(definition) An OPTIONS preflight asks whether an intended method and headers are permitted. Not every cross-origin request is preflighted. ⟦A.f1 A:tb2⟧
(mechanism) Include Origin and Access-Control-Request-Method; include Access-Control-Request-Headers when applicable. Compare the caller’s origin, method and headers with Access-Control-Allow-Origin, Access-Control-Allow-Methods and Access-Control-Allow-Headers. A credentialed response needs an explicit allowed origin, not *, plus Access-Control-Allow-Credentials: true. ⟦A.f2 A.f3 A.f4 A:tb3⟧
[PROCESS_FLOW] nodes=['OPTIONS /orders/42 HTTP/1.1\nHost: api.example\nOrigin: https://shop.example\nAccess-Control-Request-Method: PUT\nAccess-Control-Request-Headers: content-type', 'HTTP/1.1 204 No Content\nAccess-Control-Allow-Origin: https://shop.example\nAccess-Control-Allow-Methods: PUT\nAccess-Control-Allow-Headers: content-type', 'Actual PUT: separate next request only if permitted', 'HTTP/1.1 200 OK\nAccess-Control-Allow-Origin: https://shop.example\nAccess-Control-Allow-Credentials: true', 'Credentialed response: explicit origin and allow-credentials true; wildcard is not sufficient'] edges=[('n1', 'n2', 'compare origin, intended method and headers'), ('n2', 'n3', 'permission, not completion'), ('n4', 'n5', 'credentialed requirements')] alt: OPTIONS /orders/42 HTTP/1.1
Host: api.example
Origin: https://shop.example
Access-Control-Request-Method: PUT
Access-Control-Request-Headers: content-type; HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://shop.example
Access-Control-Allow-Methods: PUT
Access-Control-Allow-Headers: content-type; Actual PUT: separate next request only if permitted; HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://shop.example
Access-Control-Allow-Credentials: true; Credentialed response: explicit origin and allow-credentials true; wildcard is not sufficient

### s02 · explainer · Reason through an example
CORS preflight behavior — 
(walkthrough) Compare the supplied OPTIONS exchange: its caller origin, intended PUT and requested content-type must align with the corresponding allow headers. The actual PUT is a separate conditional next step, not completed by OPTIONS. For a credentialed response, check both the explicit allowed origin and Access-Control-Allow-Credentials: true. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧
(misconception) Only some cross-origin requests are preflighted. A wildcard allowed origin is not the required response for a credentialed exchange. ⟦A.f1 A.f4 A:tb5⟧

### s03 · check · Check the distinction
CORS preflight behavior — 

### s04 · hands_on · Apply the rule
CORS preflight behavior — 

### s05 · explainer · Establish the rule
Choosing HTTP success and failure statuses — 
(intro) Order creation, an absent target and unexpected failure need distinct HTTP outcomes. ⟦B:tb1⟧
(definition) The classes are informational 1xx, successful 2xx, redirection 3xx, client error 4xx and server error 5xx. ⟦B.f1 B:tb2⟧
(mechanism) Use 200 for success, 201 for resource creation and 204 for success without response content. 400 means a perceived request error; 401 lacks valid authentication credentials; 403 refuses fulfillment; 404 does not find or disclose the target; 409 conflicts with current state. 500 denotes an unexpected server condition; 503 temporary inability, such as overload or maintenance. ⟦B.f2 B.f3 B.f4 B:tb3⟧
[TABLE ds.order_outcomes cols=['outcome', 'status_class', 'selected_status'] ] caption: 
[TABLE ds.http_status_classes cols=all ] caption: 

### s06 · explainer · Why the distinction matters
Choosing HTTP success and failure statuses — 
(walkthrough) Choose the outcome class, then its specific meaning. Retrieval differs from creation; missing valid credentials differ from refusal; conflict differs from a target not found or disclosed. Unexpected failure differs from temporary inability. Producing a JSON body does not itself justify a successful status. ⟦B.f1 B.f2 B.f3 B.f4 B:tb4⟧

### s07 · explainer · Reason through an example
Choosing HTTP success and failure statuses — 
(walkthrough) Use the orders outcome table: retrieval 200, creation 201, no-content success 204. Compare 400 request error, 401 missing valid credentials, 403 refusal, 404 target not found or disclosed and 409 current-state conflict. Unexpected server failure is 500; temporary inability is 503. These meanings do not promise automatic framework behavior. ⟦B.f1 B.f2 B.f3 B.f4 B:tb5⟧
(misconception) Client and server errors are different classes. A 204 success has no response content. ⟦B.f1 B.f2 B:tb6⟧

### s08 · check · Check the distinction
Choosing HTTP success and failure statuses — 

### s09 · hands_on · Apply the rule
Choosing HTTP success and failure statuses — 

### s10 · recap · Keep these takeaways
Review — 
(takeaway) OPTIONS checks permission, not completion. Credentialed responses require explicit origin and allow-credentials true. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Choose the outcome class, then the particular success or failure meaning. ⟦B.f1 B.f2 B.f3 B.f4 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧
[UP NEXT] Pydantic V2 model construction and input conversion: Continue to tile_014.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit tile_012.s03
(definition) A credentialed cross-origin response requires an explicit allowed origin rather than * and Access-Control-Allow-Credentials: true. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(example) OPTIONS checks permission, not completion. Credentialed responses require explicit origin and allow-credentials true. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit tile_012.s04
(definition) A browser preflights some cross-origin requests with OPTIONS to ask whether the intended method and headers are permitted before sending the actual request. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) A CORS preflight includes Origin and Access-Control-Request-Method; Access-Control-Request-Headers identifies requested headers when applicable. ⟦A.f2 A:tb3 A:tb4⟧
(definition) Verify a preflight by sending the caller's Origin and intended method and headers, then comparing Access-Control-Allow-Origin, Access-Control-Allow-Methods and Access-Control-Allow-Headers with that request. ⟦A.f3 A:tb3 A:tb4⟧
(definition) A credentialed cross-origin response requires an explicit allowed origin rather than * and Access-Control-Allow-Credentials: true. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(example) OPTIONS checks permission, not completion. Credentialed responses require explicit origin and allow-credentials true. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Revisit tile_012.s08
(definition) 500 denotes an unexpected server condition and 503 denotes temporary inability to handle the request, such as overload or maintenance. ⟦B.f4 B:tb3 B:tb4 B:tb5⟧
(example) Contrast retrieval success with creation success: the selected meanings are 200 and 201, not one generic success label. ⟦B.f4 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.order_outcomes cols=['outcome', 'status_class', 'selected_status'] ] caption: 
### r04 · Revisit tile_012.s09
(definition) HTTP status classes distinguish informational 1xx, successful 2xx, redirection 3xx, client error 4xx and server error 5xx outcomes. ⟦B.f1 B:tb2 B:tb4 B:tb5 B:tb6⟧
(definition) Use 200 for a successful request, 201 when the request creates a resource, and 204 for successful completion with no response content. ⟦B.f2 B:tb3 B:tb4 B:tb5 B:tb6⟧
(definition) 400 denotes a perceived client request error, 401 lacks valid authentication credentials, 403 refuses fulfillment, 404 does not find or disclose the target, and 409 conflicts with current resource state. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(definition) 500 denotes an unexpected server condition and 503 denotes temporary inability to handle the request, such as overload or maintenance. ⟦B.f4 B:tb3 B:tb4 B:tb5⟧
(example) Contrast retrieval success with creation success: the selected meanings are 200 and 201, not one generic success label. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧
[TABLE ds.order_outcomes cols=['outcome', 'status_class', 'selected_status'] ] caption: 

=========

# EVALUATOR PACKET — Pydantic V2 model construction and input conversion (tile_014)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = pydantic.model_validation_conversion — Pydantic V2 model construction and input conversion

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (pydantic.model_validation_conversion)   objective: Construct validated models: define one request model.
A.f1: Define a Pydantic model by subclassing BaseModel and declaring typed fields, then construct it with Model(field=value, ...) or validate data with Model.model_validate(data).   [sources: pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/models/#basic-model-usage]
A.f2: Pydantic validation can convert compatible inputs to declared types; its default validation is not a guarantee that input values already had those types.   [sources: pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/models/#data-conversion]
A.f3: Inputs that cannot satisfy a model raise ValidationError with details about the failed fields.   [sources: pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/models/#error-handling]
A.f4: A field without a default is required; a declared default supplies its value when it is omitted.   [sources: pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/models/#basic-model-usage]
note: Establish this first: Construction converts and validates against a shape.
note: Stay within the current objective: Construct validated models. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine accepted values and conversions.
PRACTICE ANCHOR (live_code): Define a standalone OrderInput request-data model with required quantity: int and note: str defaulting to an empty string. Construct it with quantity="3", and validate equivalent dictionary data with OrderInput.model_validate.  SUCCESS: Both resulting instances contain integer quantity 3 and an empty-string note. The quantity declaration has no default, while note has its declared default.
ASSESSMENT ANCHOR: recognize_model_declaration_and_validation_entry_points facts=['f1']
ASSESSMENT ANCHOR: distinguish_accepted_input_conversion_from_original_input_types facts=['f2']
ASSESSMENT ANCHOR: identify_invalid_inputs_and_field_validation_failures facts=['f3']
ASSESSMENT ANCHOR: determine_required_fields_and_omitted_default_values facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Application lifespan; Async-compatible external HTTP requests; Binding request bodies to typed models; Bounded in-process background work and nondurable delivery limits; Choosing def versus async def from I/O behavior without blocking the event loop; Composing request dependency graphs; Configuring existing middleware in the request/response stack; Custom validation for domain invariants; Declarative field validation constraints; Depends; Expected API failures with HTTPException; FastAPI application and path-operation declarations; Modular FastAPI application composition with APIRouter; Nested request-data models; Orm relationship mapping; Outbound timeouts; Production ASGI serving versus development reload; Python package organization for a service; Reproducible service dependency declarations; Resource-oriented REST URLs and CRUD contracts; Response-model serialization and private-field exclusion; Separating transport, testable business logic and persistence responsibilities; Service-schema integrity constraints; Typed path and query input binding; Validated environment-based configuration with fail-fast startup

## LESSON, in learner order

### s01 · explainer · Establish the rule
Pydantic V2 model construction and input conversion — 
(intro) Order input needs a declared shape. Validation can convert compatible values; it is not merely an original-type check. ⟦A:tb1⟧
(definition) Subclass BaseModel and declare typed fields. Construct with Model(field=value, ...) or validate data with Model.model_validate(data). ⟦A.f1 A:tb2⟧
(mechanism) Compatible inputs can convert to declared types; default validation does not prove their original types matched. Inputs that cannot satisfy the model raise ValidationError with failed-field details. Fields without defaults are required; declared defaults supply omitted values. ⟦A.f2 A.f3 A.f4 A:tb3⟧
[CODE python]
from pydantic import BaseModel, ValidationError

class OrderInput(BaseModel):
    quantity: int
    note: str | None = None

first = OrderInput(quantity='3')
cases = [{'quantity': '3'}, {'quantity': 3}, {}, {'quantity': 'many'}]
for data in cases:
    try:
        model = OrderInput.model_validate(data)
        print(model)
    except ValidationError as error:
        print(error.errors())

  annotations: ['quantity required; note default supplied on omission.', 'Compare compatible string input, integer input, omitted quantity and incompatible input.', "Expected outcomes: {'quantity': '3'} and {'quantity': 3} both produce quantity=3 and note=None. {} fails because quantity is required. {'quantity': 'many'} fails integer validation for quantity. Failures raise ValidationError with field details."]

### s02 · explainer · Why the distinction matters
Pydantic V2 model construction and input conversion — 
(walkthrough) Check presence and conversion separately. Missing required quantity differs from present quantity that cannot satisfy int. Missing defaulted note uses its default. Compatible conversion can yield the declared type without proving the input originally had that type. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧

### s03 · explainer · Reason through an example
Pydantic V2 model construction and input conversion — 
(walkthrough) For OrderInput, quantity has no default and must be present; omitted note uses its declared default. Construct or model_validate compatible quantity input, compare incompatible input and omission, and inspect ValidationError field details for failures. Read the model as validated output, not a historical guarantee of input types. ⟦A.f1 A.f2 A.f3 A.f4 A:tb5⟧
(misconception) An integer in the model does not prove the original input was an integer. Ordinary validation can convert compatible inputs. ⟦A.f2 A:tb6⟧

### s04 · video · Follow the worked trace
Pydantic V2 model construction and input conversion — 
[VIDEO ] bridge-before:  | bridge-after: 

### s05 · check · Check the distinction
Pydantic V2 model construction and input conversion — 

### s06 · check · Check the distinction
Pydantic V2 model construction and input conversion — 

### s07 · hands_on · Apply the rule
Pydantic V2 model construction and input conversion — 

### s08 · recap · Keep these takeaways
Review — 
(takeaway) Models can convert compatible input. Required fields, defaults and field errors answer different questions. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
[UP NEXT] Reproducible service dependency declarations: Continue to tile_015.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit tile_014.s05
(definition) Pydantic validation can convert compatible inputs to declared types; its default validation is not a guarantee that input values already had those types. ⟦A.f2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(definition) Inputs that cannot satisfy a model raise ValidationError with details about the failed fields. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) Contrast omitted required quantity with omitted defaulted note: absence fails the first field but supplies the second field’s default. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r02 · Revisit tile_014.s06
(definition) A field without a default is required; a declared default supplies its value when it is omitted. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(example) Contrast omitted required quantity with omitted defaulted note: absence fails the first field but supplies the second field’s default. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
### r03 · Revisit tile_014.s07
(definition) Define a Pydantic model by subclassing BaseModel and declaring typed fields, then construct it with Model(field=value, ...) or validate data with Model.model_validate(data). ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(example) Contrast omitted required quantity with omitted defaulted note: absence fails the first field but supplies the second field’s default. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Reproducible service dependency declarations · Python package organization for a service (tile_015)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.reproducible_dependencies — Reproducible service dependency declarations
B = python.service_packages — Python package organization for a service

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.reproducible_dependencies)   objective: Declare reproducible service dependencies: install a service in a clean environment from dependency files.
A.f1: python -m pip freeze reports installed packages and versions, and its output can be saved to requirements.txt for a dependency declaration.   [sources: python_tutorial#https://docs.python.org/3/tutorial/venv.html#managing-packages-with-pip]
A.f2: Install declared dependencies in an environment with python -m pip install -r requirements.txt.   [sources: python_tutorial#https://docs.python.org/3/tutorial/venv.html#managing-packages-with-pip]
A.f3: Reconstruct the environment from committed dependency declarations rather than relying on packages installed manually in another environment; the build stage obtains the declared dependencies.   [sources: python_tutorial#https://docs.python.org/3/tutorial/venv.html#managing-packages-with-pip, twelve_factor_app#https://12factor.net/build-release-run#v_build_release_run]
note: Establish this first: Dependency declarations are part of the build contract, not memory of local installations.
note: Stay within the current objective: Declare reproducible service dependencies. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Recreate a compatible dependency set from committed declarations.
PRACTICE ANCHOR (live_code): Install the service's declared dependencies in a provided clean, isolated environment using the committed requirements.txt file.  SUCCESS: The declared dependencies install successfully, and the installed package versions satisfy the committed requirements.txt entries without relying on packages from the original working environment.
ASSESSMENT ANCHOR: capture_installed_dependency_versions facts=['f1']
ASSESSMENT ANCHOR: install_dependencies_from_requirements facts=['f2']
ASSESSMENT ANCHOR: reconstruct_dependencies_from_committed_declarations facts=['f3']

## SOURCE FACTS — B (python.service_packages)   objective: Organize an importable package: arrange one runnable service package.
B.f1: Packages organize modules with qualified names such as package.module; regular packages contain an __init__.py file.   [sources: python_tutorial#https://docs.python.org/3/tutorial/modules.html#packages]
B.f2: Import across a package with an absolute package-qualified import or a relative import using leading dots, whose meaning depends on the current package.   [sources: python_tutorial#https://docs.python.org/3/tutorial/modules.html#intra-package-references]
B.f3: Run a module in its package context with python -m package.module; its __name__ is then __main__.   [sources: python_tutorial#https://docs.python.org/3/tutorial/modules.html#executing-modules-as-scripts]
note: Establish this first: Packages establish qualified module identity.
note: Stay within the current objective: Organize an importable package. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Resolve package-qualified imports.
PRACTICE ANCHOR (live_code): Arrange service/__init__.py and service/orders.py as a regular package, identify service.orders as the qualified import name, and run orders in package context using python -m service.orders.  SUCCESS: The regular package contains __init__.py, service.orders is importable, and python -m service.orders runs successfully from the directory containing service. The learner identifies __main__ as the module's execution name.
ASSESSMENT ANCHOR: resolve_package_qualified_imports facts=['f1', 'f2']
ASSESSMENT ANCHOR: resolve_relative_imports_in_package_context facts=['f2']
ASSESSMENT ANCHOR: identify_module_execution_name facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Application lifespan; Async-compatible external HTTP requests; Binding request bodies to typed models; Bounded in-process background work and nondurable delivery limits; Choosing def versus async def from I/O behavior without blocking the event loop; Composing request dependency graphs; Configuring existing middleware in the request/response stack; Custom validation for domain invariants; Declarative field validation constraints; Depends; Expected API failures with HTTPException; FastAPI application and path-operation declarations; Modular FastAPI application composition with APIRouter; Nested request-data models; Orm relationship mapping; Outbound timeouts; Production ASGI serving versus development reload; Python package organization for a service; Resource-oriented REST URLs and CRUD contracts; Response-model serialization and private-field exclusion; Separating transport, testable business logic and persistence responsibilities; Service-schema integrity constraints; Structured service request and error logs; Typed path and query input binding; Validated environment-based configuration with fail-fast startup; Yield-based dependency cleanup

## LESSON, in learner order

### s01 · explainer · Establish the rule
Reproducible service dependency declarations — 
(intro) A teammate needs committed dependency declarations, not a memory of local installation steps. ⟦A:tb1⟧
(definition) python -m pip freeze reports installed packages and versions. Save that output to requirements.txt as a dependency declaration. ⟦A.f1 A:tb2⟧
(mechanism) Install with python -m pip install -r requirements.txt. Reconstruct from committed declarations, not manually installed packages elsewhere; the build stage obtains the declared dependencies. ⟦A.f2 A.f3 A:tb3⟧
[SIDE_BY_SIDE] After successful installation, compare the inspected versions with every committed entry; this expected output is not evidence that installation has already run. left_label: Committed declaration | right_label: Reconstruct and inspect installed versions
  left:
[CODE bash]
attrs==26.1.0
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
referencing==0.37.0
rpds-py==2026.9.1
typing_extensions==4.16.0

  annotations: []
  right:
[CODE bash]
python -m pip install -r requirements.txt
python -m pip freeze

# Expected python -m pip freeze output after successful reconstruction
attrs==26.1.0
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
referencing==0.37.0
rpds-py==2026.9.1
typing_extensions==4.16.0

  annotations: []

### s02 · explainer · Reason through an example
Reproducible service dependency declarations — 
(walkthrough) Inspect versions with python -m pip freeze, save requirements.txt and commit the declaration. Install from it in the environment being reconstructed. Compare declared packages with those obtained for the build. A local installation is not the handoff contract, and freeze alone does not reproduce every external service condition. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) One successful run in a manually prepared environment is not a dependency declaration. Reconstruct from the committed declaration. ⟦A.f3 A:tb5⟧

### s03 · video · Follow the worked trace
Reproducible service dependency declarations — 
[VIDEO ] bridge-before:  | bridge-after: 

### s04 · check · Check the distinction
Reproducible service dependency declarations — 

### s05 · hands_on · Apply the rule
Reproducible service dependency declarations — 

### s06 · explainer · Establish the rule
Python package organization for a service — 
(intro) Qualified names show which package owns a service module. ⟦B:tb1⟧
(definition) Packages organize modules as package.module. Regular packages contain __init__.py. ⟦B.f1 B:tb2⟧
(mechanism) Use absolute package-qualified imports or relative imports with leading dots interpreted in the current package. Run in package context with python -m package.module; __name__ then becomes __main__. ⟦B.f2 B.f3 B:tb3⟧
[CODE python]
# Regular package marker: service/__init__.py (empty)
# Service module: service/orders.py
import service.orders
# In package context, leading-dot imports use the current package.
# Run from the shell: python -m service.orders
# Execution name: __main__

  annotations: ['Regular package marker and module location.', 'Qualified identity versus package-relative import context.', 'Run in package context; distinguish qualified identity from execution name.']

### s07 · explainer · Reason through an example
Python package organization for a service — 
(walkthrough) With service/__init__.py and service/orders.py, the qualified module is service.orders. An absolute import names the package; leading-dot imports depend on that package context. python -m service.orders runs it in package context with __name__ equal to __main__. Import identity and execution name serve different roles. ⟦B.f1 B.f2 B.f3 B:tb4⟧
(misconception) Relative imports depend on the current package. File location alone does not explain a leading dot. ⟦B.f2 B:tb5⟧

### s08 · check · Check the distinction
Python package organization for a service — 

### s09 · hands_on · Apply the rule
Python package organization for a service — 

### s10 · recap · Keep these takeaways
Review — 
(takeaway) Commit dependency declarations and reconstruct from them rather than accidental local installations. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Qualified imports and leading-dot imports use package context; -m runs with __name__ set to __main__. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Service-schema integrity constraints: Continue to tile_017.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit tile_015.s04
(definition) Reconstruct the environment from committed dependency declarations rather than relying on packages installed manually in another environment; the build stage obtains the declared dependencies. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) Commit dependency declarations and reconstruct from them rather than accidental local installations. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit tile_015.s05
(definition) python -m pip freeze reports installed packages and versions, and its output can be saved to requirements.txt for a dependency declaration. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Install declared dependencies in an environment with python -m pip install -r requirements.txt. ⟦A.f2 A:tb3 A:tb4⟧
(definition) Reconstruct the environment from committed dependency declarations rather than relying on packages installed manually in another environment; the build stage obtains the declared dependencies. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) Commit dependency declarations and reconstruct from them rather than accidental local installations. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Revisit tile_015.s08
(definition) Run a module in its package context with python -m package.module; its __name__ is then __main__. ⟦B.f3 B:tb3 B:tb4⟧
(example) Qualified imports and leading-dot imports use package context; -m runs with __name__ set to __main__. ⟦B.f3 B:tb3 B:tb4⟧
### r04 · Revisit tile_015.s09
(definition) Packages organize modules with qualified names such as package.module; regular packages contain an __init__.py file. ⟦B.f1 B:tb2 B:tb4⟧
(definition) Import across a package with an absolute package-qualified import or a relative import using leading dots, whose meaning depends on the current package. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(definition) Run a module in its package context with python -m package.module; its __name__ is then __main__. ⟦B.f3 B:tb3 B:tb4⟧
(example) Qualified imports and leading-dot imports use package context; -m runs with __name__ set to __main__. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧

=========

# EVALUATOR PACKET — Service-schema integrity constraints (tile_017)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = database.service_integrity_constraints — Service-schema integrity constraints

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (database.service_integrity_constraints)   objective: Enforce database constraints: declare one table's constraints.
A.f1: Declare a column as TYPE NOT NULL to reject nulls independently of whether a write came through an application.   [sources: postgresql_docs#https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-NOT-NULL]
A.f2: Declare UNIQUE (columns) to reject duplicate combinations; PostgreSQL treats nulls as distinct by default unless NULLS NOT DISTINCT is specified.   [sources: postgresql_docs#https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-UNIQUE-CONSTRAINTS]
A.f3: Declare PRIMARY KEY (columns) for unique non-null row identity; a primary key can contain more than one column.   [sources: postgresql_docs#https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-PRIMARY-KEYS]
A.f4: Declare FOREIGN KEY (columns) REFERENCES target (columns) so non-null referencing values must match referenced rows.   [sources: postgresql_docs#https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK]
A.f5: Declare CHECK (condition) to constrain values in a row; a check passes when its expression is true or null, so use NOT NULL separately when absence must be rejected.   [sources: postgresql_docs#https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-CHECK-CONSTRAINTS]
note: Establish this first: Integrity holds independently of application callers.
note: Stay within the current objective: Enforce database constraints. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify rejected integrity-breaking writes.
PRACTICE ANCHOR (live_code): Complete the supplied orders table declaration with a primary key on identity, a foreign key on customer_reference, NOT NULL and a positive-value CHECK on quantity, and UNIQUE on external_reference.  SUCCESS: The declaration gives orders unique non-null identity, requires non-null customer references to match existing customer identities, rejects absent or nonpositive quantities, and rejects duplicate non-null external references while retaining PostgreSQL's default distinct-null behavior.
ASSESSMENT ANCHOR: identify_null_required_value_rejection facts=['f1']
ASSESSMENT ANCHOR: identify_duplicate_combination_rejection_under_null_policy facts=['f2']
ASSESSMENT ANCHOR: identify_null_or_duplicate_primary_key_rejection facts=['f3']
ASSESSMENT ANCHOR: identify_unmatched_non_null_reference_rejection facts=['f4']
ASSESSMENT ANCHOR: distinguish_failed_check_rejection_from_null_rejection facts=['f1', 'f5']

## DATA ASSETS USED
ds.customers: customers — columns: identity(identifier,digits-as-label)
   [1]
   [2]
ds.orders: orders — columns: identity(identifier,digits-as-label), customer_reference(identifier,digits-as-label), quantity(numerical), external_reference(identifier)
   [42,1,3,"ORD-A"]
   [43,2,1,null]
   [44,null,2,null]
   variant var.orders.null_quantity: 1 ops; planted: issue.null_quantity(missing_value)
   variant var.orders.nonpositive_quantity: 1 ops; planted: issue.nonpositive_quantity(impossible_value)
   variant var.orders.negative_quantity: 1 ops; planted: issue.negative_quantity(impossible_value)
   variant var.orders.duplicate_row: 1 ops; planted: issue.duplicate_order(duplicate_row)
   variant var.orders.null_identity: 1 ops; planted: issue.null_identity(missing_value)
   variant var.orders.unmatched_customer: 1 ops; planted: issue.customer_reference_not_in_supplied_customers(other)
   variant var.orders.duplicate_external_reference: 1 ops; planted: issue.external_reference_matches_existing_order_42(other)
ds.proposed_orders: Independent proposed orders and constraint outcomes — columns: case_id(identifier), identity(identifier,digits-as-label), customer_reference(identifier,digits-as-label), quantity(numerical), external_reference(identifier), primary_key_passes(categorical), foreign_key_passes(categorical), not_null_passes(categorical), check_alone_passes(categorical), unique_default_passes(categorical), unique_nulls_not_distinct_passes(categorical), combined_outcome(categorical), rejecting_constraints(text)
   ["valid_new_order",45,1,1,"ORD-B",true,true,true,true,true,true,"accept","none"]
   ["null_identity",null,1,1,"ORD-B",false,true,true,true,true,true,"reject","PRIMARY KEY"]
   ["duplicate_identity",42,1,1,"ORD-B",false,true,true,true,true,true,"reject","PRIMARY KEY"]
   ["unmatched_customer",45,99,1,"ORD-B",true,false,true,true,true,true,"reject","FOREIGN KEY"]
   ["null_customer",45,null,1,"ORD-B",true,true,true,true,true,true,"accept","none"]
   ["null_quantity",45,1,null,"ORD-B",true,true,false,true,true,true,"reject","NOT NULL"]
   ["zero_quantity",45,1,0,"ORD-B",true,true,true,false,true,true,"reject","CHECK"]
   ["negative_quantity",45,1,-1,"ORD-B",true,true,true,false,true,true,"reject","CHECK"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Application lifespan; Async-compatible external HTTP requests; Binding request bodies to typed models; Bounded in-process background work and nondurable delivery limits; Choosing def versus async def from I/O behavior without blocking the event loop; Composing request dependency graphs; Configuring existing middleware in the request/response stack; Custom validation for domain invariants; Declarative field validation constraints; Depends; Expected API failures with HTTPException; FastAPI application and path-operation declarations; Modular FastAPI application composition with APIRouter; Nested request-data models; Orm relationship mapping; Outbound timeouts; Preventing unsafe outbound requests and SSRF; Production ASGI serving versus development reload; Resource-oriented REST URLs and CRUD contracts; Response-model serialization and private-field exclusion; Separating transport, testable business logic and persistence responsibilities; Structured service request and error logs; Typed path and query input binding; Validated environment-based configuration with fail-fast startup; Yield-based dependency cleanup

## LESSON, in learner order

### s01 · explainer · Establish the rule
Service-schema integrity constraints — 
(intro) Database constraints enforce order integrity even when writes bypass the API. ⟦A:tb1⟧
(definition) TYPE NOT NULL rejects nulls independently of the application path. ⟦A.f1 A:tb2⟧
(mechanism) UNIQUE rejects duplicate combinations; PostgreSQL treats nulls as distinct by default unless NULLS NOT DISTINCT is specified. PRIMARY KEY gives unique non-null row identity and may span columns. FOREIGN KEY requires non-null references to match referenced rows. CHECK constrains row values but passes on true or null; add NOT NULL to reject absence. ⟦A.f2 A.f3 A.f4 A.f5 A:tb3⟧
[TABLE ds.orders cols=all ] caption: 
[TABLE ds.customers cols=all ] caption: 
[TABLE ds.proposed_orders cols=all ] caption: 
[CODE sql]
CREATE TABLE orders (
    identity INTEGER,
    customer_reference INTEGER,
    quantity INTEGER NOT NULL,
    external_reference TEXT,
    PRIMARY KEY (identity),
    FOREIGN KEY (customer_reference) REFERENCES customers (identity),
    CHECK (quantity > 0),
    UNIQUE (external_reference)
);
  annotations: ['customers already exists with identity as its primary key. PRIMARY KEY may list multiple columns. CHECK passes on true or null, so quantity also needs NOT NULL. UNIQUE preserves PostgreSQL’s default distinct-null behavior; UNIQUE NULLS NOT DISTINCT (external_reference) is the alternative when null duplicates must also be rejected.']

### s02 · explainer · Reason through an example
Service-schema integrity constraints — 
(walkthrough) Inspect proposed orders independently against the baseline. PRIMARY KEY protects unique non-null identity, and FOREIGN KEY checks non-null customer references. quantity needs NOT NULL as well as CHECK. UNIQUE rejects duplicate external references, but PostgreSQL’s default permits distinct nulls; NULLS NOT DISTINCT changes that null comparison. Match each violation to its constraint. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb4⟧
(misconception) CHECK passing on null does not replace NOT NULL. PostgreSQL UNIQUE treats nulls as distinct by default. ⟦A.f2 A.f5 A:tb5⟧

### s03 · check · Check the distinction
Service-schema integrity constraints — 

### s04 · check · Check the distinction
Service-schema integrity constraints — 

### s05 · hands_on · Apply the rule
Service-schema integrity constraints — 

### s06 · recap · Keep these takeaways
Review — 
(takeaway) Database constraints enforce integrity beyond the API. CHECK does not reject null by itself; default UNIQUE treats nulls as distinct. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Application lifespan: Continue to tile_018.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit tile_017.s03
(definition) Declare UNIQUE (columns) to reject duplicate combinations; PostgreSQL treats nulls as distinct by default unless NULLS NOT DISTINCT is specified. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(example) Contrast CHECK (quantity > 0) alone with adding NOT NULL: null passes CHECK alone but is rejected by NOT NULL. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.proposed_orders cols=all ] caption: 
### r02 · Revisit tile_017.s04
(definition) Declare a column as TYPE NOT NULL to reject nulls independently of whether a write came through an application. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Declare CHECK (condition) to constrain values in a row; a check passes when its expression is true or null, so use NOT NULL separately when absence must be rejected. ⟦A.f5 A:tb3 A:tb4 A:tb5⟧
(example) Contrast CHECK (quantity > 0) alone with adding NOT NULL: null passes CHECK alone but is rejected by NOT NULL. ⟦A.f1 A.f5 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.proposed_orders cols=all ] caption: 
### r03 · Revisit tile_017.s05
(definition) Declare a column as TYPE NOT NULL to reject nulls independently of whether a write came through an application. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Declare PRIMARY KEY (columns) for unique non-null row identity; a primary key can contain more than one column. ⟦A.f3 A:tb3 A:tb4⟧
(definition) Declare FOREIGN KEY (columns) REFERENCES target (columns) so non-null referencing values must match referenced rows. ⟦A.f4 A:tb3 A:tb4⟧
(example) Contrast CHECK (quantity > 0) alone with adding NOT NULL: null passes CHECK alone but is rejected by NOT NULL. ⟦A.f1 A.f3 A.f4 A:tb2 A:tb3 A:tb4⟧
[TABLE ds.proposed_orders cols=all ] caption: 