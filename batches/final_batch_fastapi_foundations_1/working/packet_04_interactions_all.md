# EVALUATOR PACKET — Browser same-origin policy and the CORS/authentication boundary · HTTP method safety and idempotency · HTTP headers and representation metadata (tile_000)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = browser.same_origin_boundary — Browser same-origin policy and the CORS/authentication boundary
B = http.method_safety_idempotency — HTTP method safety and idempotency
C = http.representation_headers — HTTP headers and representation metadata

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=4
  warn: tile_000.s01: prose block without lineage.fact_ids
  warn: tile_000.s04: prose block without lineage.fact_ids
  warn: tile_000.s09: prose block without lineage.fact_ids
  warn: plan: tile_000.s03 was planned to measure browser.same_origin_boundary#assessment:distinguish_browser_response_access_from_api_authentication but its interaction does not

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
QUESTION [choice, intro, grading=client] A script at https://shop.example calls https://api.example. CORS permits reading the response. What follows for endpoint access checks?
  ✔ option1: The API must still check access independently of CORS.
      why: Correct: The API must still check access independently of CORS.
  ✘ option2: CORS permission replaces endpoint access checks.
      why: CORS concerns browser response access, not the API's independent access checks.
  ✘ option3: The browser's origin restriction itself authenticates the caller.
      why: A browser restriction is not an endpoint access check.
  feedback✔: The API must still check access independently of CORS.  feedback✘: Recheck the taught rule and the specific evidence. Read the explanation for the selected option.  hints: ['Separate the roles named in the prompt; apply the taught distinction rather than treating them as interchangeable.']  remediation→r01
  MEASURES: A:distinguish_browser_response_access_from_api_authentication(f2,f3)   anchors=['assessment:distinguish_browser_response_access_from_api_authentication']
  taught-before-tested: A.f2←s01; A.f3←s01

### s03 · hands_on · Apply the rule
Browser same-origin policy and the CORS/authentication boundary — 
QUESTION [classify, core, grading=client] Classify each browser-page URL relative to the fixed API https://shop.example:443/orders. Identify the differing origin component; a path difference alone is not an origin difference.
  'https://shop.example:443/items' -> same-origin — no differing origin component  (column differing_components, role=categorical)
      feedback: Origin comparison: same-origin; differing component: none.
  'http://shop.example:443/items' -> cross-origin — different scheme  (column differing_components, role=categorical)
      feedback: Origin comparison: cross-origin; differing component: scheme.
  'https://api.example:443/items' -> cross-origin — different host  (column differing_components, role=categorical)
      feedback: Origin comparison: cross-origin; differing component: host.
  'https://shop.example:8443/items' -> cross-origin — different port  (column differing_components, role=categorical)
      feedback: Origin comparison: cross-origin; differing component: port.
  feedback✔: Each judgement follows the specific evidence in its excerpt or URL, not a package name, response alone or an unrelated permission.  feedback✘: Recheck the taught rule and the specific evidence. A browser origin is the combination of scheme, host and port; a difference in any of these makes two URLs cross-origin.  hints: ['Compare each URL’s scheme, host and port with the fixed API. Ignore path differences.']  remediation→r02
  MEASURES: A:classify_origins_by_scheme_host_and_port(f1)   anchors=['practice', 'assessment:classify_origins_by_scheme_host_and_port']
  taught-before-tested: A.f1←s01

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
QUESTION [choice, core, grading=client] A GET retrieves an order and writes an incidental log entry; a PUT replaces that order's state. Which safety/idempotency judgement is correct?
  ✘ option1: PUT is safe because repeating it has the same intended effect.
      why: Idempotency does not imply read-only requested semantics.
  ✔ option2: GET remains safe and idempotent; PUT is idempotent but not safe.
      why: Correct: GET remains safe and idempotent; PUT is idempotent but not safe.
  ✘ option3: Both are unsafe because both can write something.
      why: Safety concerns requested semantics; incidental retrieval logging does not make GET unsafe.
  feedback✔: GET remains safe and idempotent; PUT is idempotent but not safe.  feedback✘: Recheck the taught rule and the specific evidence. Read the explanation for the selected option.  hints: ['Separate the roles named in the prompt; apply the taught distinction rather than treating them as interchangeable.']  remediation→r03
  MEASURES: B:distinguish_safe_retrieval_from_idempotent_state_changes(f1,f3,f5)   anchors=['assessment:distinguish_safe_retrieval_from_idempotent_state_changes']
  taught-before-tested: B.f1←s04; B.f3←s04; B.f5←s04

### s08 · hands_on · Apply the rule
HTTP method safety and idempotency — 
QUESTION [classify, core, grading=client] For each orders operation, choose its method and safety/idempotency judgement. Repetition means identical requests and intended server effect, not identical response messages.
  'Retrieve the selected order representation. The server also writes an incidental retrieval log.' -> GET — safe, idempotent
      feedback: GET retrieves; incidental logging remains compatible with safety.
  'Request the same retrieval semantics but no response content.' -> HEAD — safe, idempotent
      feedback: HEAD has retrieval semantics without response content; it is safe and idempotent.
  'Process submitted content to create a new order, without any additional idempotency guarantee.' -> POST — not generally idempotent
      feedback: POST requests resource-specific processing and is not generally idempotent.
  'Create or replace the state of the known target /orders/42. Repeated identical requests need not have identical responses.' -> PUT — not safe, idempotent
      feedback: PUT creates or replaces target state; idempotency concerns intended effects rather than response equality.
  'Remove the association of /orders/42 with its current functionality. A later identical request may have a different response.' -> DELETE — not safe, idempotent
      feedback: DELETE is idempotent but not safe; differing responses do not disprove equal intended effects.
  feedback✔: Each judgement follows the specific evidence in its excerpt or URL, not a package name, response alone or an unrelated permission.  feedback✘: Recheck the taught rule and the specific evidence. A safe method has essentially read-only requested semantics; incidental effects such as logging do not make it unsafe.  hints: ['Identify the requested operation first. Then judge read-only semantics and the intended effect of identical repetition separately.']  remediation→r04
  MEASURES: B:determine_intended_effects_of_identical_repeated_requests(f2,f3,f4,f5); B:distinguish_safe_retrieval_from_idempotent_state_changes(f1,f3,f5)   anchors=['practice', 'assessment:determine_intended_effects_of_identical_repeated_requests', 'assessment:distinguish_safe_retrieval_from_idempotent_state_changes']
  taught-before-tested: B.f2←s04; B.f3←s04; B.f4←s04; B.f5←s04; B.f1←s04; B.f3←s04; B.f5←s04

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
QUESTION [choice, core, grading=client] A JSON request sends Content-Type: application/json and Accept: application/json. Which header identifies the media type actually returned?
  ✘ option1: The request's Accept.
      why: Accept communicates acceptable response formats, not the returned representation's metadata.
  ✘ option2: The request's Content-Type.
      why: That Content-Type describes the outgoing JSON content, not the response content.
  ✔ option3: The response's own Content-Type.
      why: Correct: The response's own Content-Type.
  feedback✔: The response's own Content-Type.  feedback✘: Recheck the taught rule and the specific evidence. Read the explanation for the selected option.  hints: ['Separate the roles named in the prompt; apply the taught distinction rather than treating them as interchangeable.']  remediation→r05
  MEASURES: C:set_json_request_headers_and_inspect_response_content_type(f3)   anchors=['assessment:set_json_request_headers_and_inspect_response_content_type']
  taught-before-tested: C.f3←s09

### s11 · hands_on · Apply the rule
HTTP headers and representation metadata — 
QUESTION [code_exercise, stretch, grading=client] Complete the two # REQUEST header lines for a prepared JSON order request. In # RESPONSE_FIELD write the response header name to inspect separately for the returned media type. The checker supplies a response Content-Type (application/json in one case and text/plain in another); inspect that response, not a request preference. Keep the Python checker unchanged. This is raw-header editing in a supplied inspection harness, not an HTTP server. In this supplied comment-source editor, Python source lines have a # PY prefix. Keep that prefix and edit the requested code after it; the unchanged compiler executes those lines. Lines belonging to the supplied checker are scaffolding, not new syntax to learn.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': []} constraints.allowed=['Content-Type: application/json', 'Accept: application/json'] blocked=7 items
  file main.py [editable]:
# REQUEST Content-Type: 
# REQUEST Accept: 
# RESPONSE_FIELD 
# PY 
# PY def inspect_exchange(response_type):
# PY     source = open('main.py').read().splitlines()
# PY     request = {}
# PY     selected = ''
# PY     for line in source:
# PY         if line.startswith('# REQUEST '):
# PY             name, value = line[len('# REQUEST '):].split(':', 1)
# PY             request[name.strip()] = value.strip()
# PY         if line.startswith('# RESPONSE_FIELD '):
# PY             selected = line[len('# RESPONSE_FIELD '):].strip()
# PY     response_headers = {'Content-Type': response_type}
# PY     return {'request': request, 'returned_media_type': response_headers.get(selected)}

# Supplied compiler: keep unchanged. It executes the # PY source lines below.
exec('\n'.join(line[5:] for line in open('main.py').read().splitlines() if line.startswith('# PY ')), globals())

  SOLUTION main.py:
# REQUEST Content-Type: application/json
# REQUEST Accept: application/json
# RESPONSE_FIELD Content-Type
# PY 
# PY def inspect_exchange(response_type):
# PY     source = open('main.py').read().splitlines()
# PY     request = {}
# PY     selected = ''
# PY     for line in source:
# PY         if line.startswith('# REQUEST '):
# PY             name, value = line[len('# REQUEST '):].split(':', 1)
# PY             request[name.strip()] = value.strip()
# PY         if line.startswith('# RESPONSE_FIELD '):
# PY             selected = line[len('# RESPONSE_FIELD '):].strip()
# PY     response_headers = {'Content-Type': response_type}
# PY     return {'request': request, 'returned_media_type': response_headers.get(selected)}

# Supplied compiler: keep unchanged. It executes the # PY source lines below.
exec('\n'.join(line[5:] for line in open('main.py').read().splitlines() if line.startswith('# PY ')), globals())

  test test1 (function_call, visible=None): {"function":"inspect_exchange","args":["application/json"],"expected":{"request":{"Content-Type":"application/json","Accept":"application/json"},"returned_media_type":"application/json"}} | on-fail: Recheck the requested edit and the supplied evidence.
  test test2 (function_call, visible=None): {"function":"inspect_exchange","args":["text/plain"],"expected":{"request":{"Content-Type":"application/json","Accept":"application/json"},"returned_media_type":"text/plain"}} | on-fail: Recheck the requested edit and the supplied evidence.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"1024dfcb74ca259fc8b4fbbc9bf8525c8510219a9d395c40defc9a54c206737f","tests_passed":2}
  feedback✔: The submitted edits meet the requested practice conditions across the supplied checks.  feedback✘: Recheck the taught rule and the specific evidence. Content-Type describes the media type of the associated representation, rather than the client's preferred response format.  hints: ['Change only the requested learner-owned lines; leave the supplied inspection or execution harness unchanged.']  remediation→r06
  MEASURES: C:distinguish_payload_media_type_from_response_preference(f1,f2); C:set_json_request_headers_and_inspect_response_content_type(f3)   anchors=['practice', 'assessment:distinguish_payload_media_type_from_response_preference', 'assessment:set_json_request_headers_and_inspect_response_content_type']
  taught-before-tested: C.f1←s09; C.f2←s09; C.f3←s09

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

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: httpx.AsyncClient(...)

=========

# EVALUATOR PACKET — Practical Python type annotations for service interfaces · Python classes and instances for service models (tile_003)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.backend_type_annotations — Practical Python type annotations for service interfaces
B = python.classes_and_instances — Python classes and instances for service models

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=3
  warn: tile_003.s01: prose block without lineage.fact_ids
  warn: tile_003.s06: prose block without lineage.fact_ids
  warn: plan: tile_003.s05 was planned to measure python.backend_type_annotations#assessment:distinguish_type_hints_from_runtime_validation but its interaction does not

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
QUESTION [choice, intro, grading=client] Compare `def a(note: str | None):` and `def b(note: str | None = None):`. Which statement correctly describes omission and runtime validation?
  ✔ option1: Only b allows omission; both annotations permit None, and neither function’s hints alone enforce runtime validation.
      why: Correct: Only b allows omission; both annotations permit None, and neither function’s hints alone enforce runtime validation.
  ✘ option2: Both allow omission, and their hints enforce runtime validation.
      why: Permitting None does not supply a default, and hints alone do not enforce runtime validation.
  ✘ option3: Neither allows omission, but b’s default enforces runtime validation.
      why: b’s default permits omission; a default is not runtime validation.
  feedback✔: Only b allows omission; both annotations permit None, and neither function’s hints alone enforce runtime validation.  feedback✘: Recheck the taught rule and the specific evidence. Read the explanation for the selected option.  hints: ['Separate the roles named in the prompt; apply the taught distinction rather than treating them as interchangeable.']  remediation→r01
  MEASURES: A:distinguish_nullable_values_from_omittable_arguments(f2); A:distinguish_type_hints_from_runtime_validation(f1)   anchors=['assessment:distinguish_nullable_values_from_omittable_arguments', 'assessment:distinguish_type_hints_from_runtime_validation']
  taught-before-tested: A.f2←s01; A.f1←s01

### s05 · hands_on · Apply the rule
Practical Python type annotations for service interfaces — 
QUESTION [code_exercise, core, grading=client] Annotate an existing order-summary service function: item_names is a list of strings, tags is a set of strings, identifier_name is an integer/string pair, counts maps strings to integers, and note accepts a string or None and may be omitted. Annotate the returned counts as a string-to-integer dictionary. Edit only the signature, leaving return counts and the supplied inspection harness unchanged. The checker inspects every annotation, the separate default and the unchanged function result. In this supplied comment-source editor, Python source lines have a # PY prefix. Keep that prefix and edit the requested code after it; the unchanged compiler executes those lines. Lines belonging to the supplied checker are scaffolding, not new syntax to learn.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': []} constraints.allowed=['def order_summary(...):', 'name: Type', '-> Type', 'str', 'int', 'None', 'str | None', '= None', 'list[str]', 'set[str]', 'tuple[int, str]', 'dict[str, int]', 'return counts'] blocked=7 items
  file main.py [editable]:
# PY def order_summary(item_names, tags, identifier_name, counts, note):
# PY     return counts
# PY 
# PY def inspect_summary(counts):
# PY     import inspect
# PY     signature = inspect.signature(order_summary)
# PY     return {'parameters': {k:str(v.annotation) for k,v in signature.parameters.items()}, 'return':str(signature.return_annotation), 'note_default_is_none':signature.parameters['note'].default is None, 'result':order_summary([],set(),(42,'order'),counts)}

# Supplied compiler: keep unchanged. It executes the # PY source lines below.
exec('\n'.join(line[5:] for line in open('main.py').read().splitlines() if line.startswith('# PY ')), globals())

  SOLUTION main.py:
# PY def order_summary(item_names: list[str], tags: set[str], identifier_name: tuple[int, str], counts: dict[str, int], note: str | None = None) -> dict[str, int]:
# PY     return counts
# PY 
# PY def inspect_summary(counts):
# PY     import inspect
# PY     signature = inspect.signature(order_summary)
# PY     return {'parameters': {k:str(v.annotation) for k,v in signature.parameters.items()}, 'return':str(signature.return_annotation), 'note_default_is_none':signature.parameters['note'].default is None, 'result':order_summary([],set(),(42,'order'),counts)}

# Supplied compiler: keep unchanged. It executes the # PY source lines below.
exec('\n'.join(line[5:] for line in open('main.py').read().splitlines() if line.startswith('# PY ')), globals())

  test test1 (function_call, visible=None): {"function":"inspect_summary","args":[{"order":3}],"expected":{"parameters":{"item_names":"list[str]","tags":"set[str]","identifier_name":"tuple[int, str]","counts":"dict[str, int]","note":"str | None"},"return":"dict[str, int]","note_default_is_none":true,"result":{"order":3}}} | on-fail: Recheck the requested edit and the supplied evidence.
  test test2 (function_call, visible=None): {"function":"inspect_summary","args":[{"order":7,"other":1}],"expected":{"parameters":{"item_names":"list[str]","tags":"set[str]","identifier_name":"tuple[int, str]","counts":"dict[str, int]","note":"str | None"},"return":"dict[str, int]","note_default_is_none":true,"result":{"order":7,"other":1}}} | on-fail: Recheck the requested edit and the supplied evidence.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"0d3f4a2363e3a24e6231d33335a48eb10b73d1b9273248c5bf84e5b4c42187c8","tests_passed":2}
  feedback✔: The submitted edits meet the requested practice conditions across the supplied checks.  feedback✘: Recheck the taught rule and the specific evidence. Annotate a function parameter with name: Type and its return value with -> Type; Python type hints alone do not enforce runtime validation.  hints: ['Change only the requested learner-owned lines; leave the supplied inspection or execution harness unchanged.']  remediation→r02
  MEASURES: A:select_parameter_and_return_annotations(f1); A:select_collection_annotations(f3)   anchors=['practice', 'assessment:select_parameter_and_return_annotations', 'assessment:select_collection_annotations']
  taught-before-tested: A.f1←s01; A.f3←s01

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
QUESTION [choice, core, grading=client] Inspect this initialization:
```python
class Draft:
    def __init__(self):
        self.items = []
draft_a = Draft()
```
Which describes the class/instance relationship?
  ✘ option1: self is the shared class object rather than the method's instance.
      why: An instance method receives the instance as its first argument.
  ✔ option2: Calling Draft creates an instance; __init__ stores items on that instance via self.
      why: Correct: Calling Draft creates an instance; __init__ stores items on that instance via self.
  ✘ option3: The class statement itself creates draft_a.
      why: The class statement creates the class; calling that class creates the instance.
  feedback✔: Calling Draft creates an instance; __init__ stores items on that instance via self.  feedback✘: Recheck the taught rule and the specific evidence. Read the explanation for the selected option.  hints: ['Separate the roles named in the prompt; apply the taught distinction rather than treating them as interchangeable.']  remediation→r03
  MEASURES: B:distinguish_class_behavior_from_instance_state(f1,f2)   anchors=['assessment:distinguish_class_behavior_from_instance_state']
  taught-before-tested: B.f1←s06; B.f2←s06

### s10 · hands_on · Apply the rule
Python classes and instances for service models — 
QUESTION [code_exercise, stretch, grading=client] Define Draft with __init__(self) assigning a fresh empty list to self.items. Create draft_a and draft_b by calling Draft, then append the supplied item only to draft_a.items. Do not change item. The checker inspects both lists, a fresh instance and whether items was stored as a shared class variable. In this supplied comment-source editor, Python source lines have a # PY prefix. Keep that prefix and edit the requested code after it; the unchanged compiler executes those lines. Lines belonging to the supplied checker are scaffolding, not new syntax to learn.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': []} constraints.allowed=['class Draft:', 'def __init__(self):', 'self.items = []', 'draft_a = Draft()', 'draft_b = Draft()', 'instance attribute access', 'list literals', 'string literals', 'items.append(...)'] blocked=7 items
  file main.py [editable]:
item = "order item"
# PY class Draft:
# PY     pass
# Create draft_a and draft_b, then append item only to draft_a.items.

# Supplied compiler: keep unchanged. It executes the # PY source lines below.
exec('\n'.join(line[5:] for line in open('main.py').read().splitlines() if line.startswith('# PY ')), globals())

  SOLUTION main.py:
item = "order item"
# PY class Draft:
# PY     def __init__(self):
# PY         self.items = []
# PY draft_a = Draft()
# PY draft_b = Draft()
# PY draft_a.items.append(item)

# Supplied compiler: keep unchanged. It executes the # PY source lines below.
exec('\n'.join(line[5:] for line in open('main.py').read().splitlines() if line.startswith('# PY ')), globals())

  test test1 (value_equals, visible=None): {"expr":"[draft_a.items, draft_b.items, Draft().items, 'items' in Draft.__dict__]","expected":[["order item"],[],[],false]} | on-fail: Recheck the requested edit and the supplied evidence.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"00d71e91f32329fc8bbcfe50c959cd5645680c17ad860c411a0eb3af50c0ccfc","tests_passed":1}
  feedback✔: The submitted edits meet the requested practice conditions across the supplied checks.  feedback✘: Recheck the taught rule and the specific evidence. A class statement creates a class whose methods define behavior, and calling the class creates an instance.  hints: ['Change only the requested learner-owned lines; leave the supplied inspection or execution harness unchanged.']  remediation→r04
  MEASURES: B:identify_shared_class_state_and_independent_instance_state(f3,f4)   anchors=['practice', 'assessment:identify_shared_class_state_and_independent_instance_state']
  taught-before-tested: B.f3←s06; B.f4←s06

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

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: tile_005.s01: prose block without lineage.fact_ids
  warn: tile_005.s08: prose block without lineage.fact_ids

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
[VIDEO File cleanup at the managed scope boundary] bridge-before: Watch for the contrast between explicitly closing a file and using a with statement. The important boundary is where work with the file ends, whether normally or through an error. | bridge-after: The clip establishes file closure after success or failure. The text supplies the complete with syntax, the successful-entry condition, and the distinction between an exit call and exception suppression.
  - -aKFBoZpiqA 0-71s facts=['f4'] label: How a with block closes a file, including after an error | summary: Context managers define resource setup and cleanup. Explicitly opening a file, writing to it, and closing it requires remembering the closing step. Using a with statement instead handles file closure when the work finishes, including when an error interrupts the work.

### s05 · check · Check the distinction
Context-managed resource cleanup — 
QUESTION [choice, intro, grading=client] A supplied context manager's __enter__ returns successfully, then the with block raises an exception. What is guaranteed about __exit__?
  ✔ option1: The with statement calls __exit__ on this exceptional exit.
      why: Correct: The with statement calls __exit__ on this exceptional exit.
  ✘ option2: __exit__ is called only when the block completes normally.
      why: After successful entry, both normal and exceptional block exits call __exit__.
  ✘ option3: Successful __enter__ means __exit__ is no longer needed.
      why: Successful entry is the condition under which with performs the exit call.
  feedback✔: The with statement calls __exit__ on this exceptional exit.  feedback✘: Recheck the taught rule and the specific evidence. Read the explanation for the selected option.  hints: ['Separate the roles named in the prompt; apply the taught distinction rather than treating them as interchangeable.']  remediation→r01
  MEASURES: A:identify_successful_entry_as_the_exit_call_condition(f2)   anchors=['assessment:identify_successful_entry_as_the_exit_call_condition']
  taught-before-tested: A.f2←s01

### s06 · check · Check the distinction
Context-managed resource cleanup — 
QUESTION [choice, core, grading=client] A manager cleans up on exceptional exit and returns False from __exit__. Does cleanup alone mean the exception is suppressed?
  ✘ option1: Yes; any cleanup suppresses the exception.
      why: Cleanup does not itself imply suppression.
  ✘ option2: Yes; a false return value is the suppression signal.
      why: A true value, not a false one, can suppress the exception.
  ✔ option3: No; cleanup and suppression are distinct, and a true exit return value can suppress it.
      why: Correct: No; cleanup and suppression are distinct, and a true exit return value can suppress it.
  feedback✔: No; cleanup and suppression are distinct, and a true exit return value can suppress it.  feedback✘: Recheck the taught rule and the specific evidence. Read the explanation for the selected option.  hints: ['Separate the roles named in the prompt; apply the taught distinction rather than treating them as interchangeable.']  remediation→r02
  MEASURES: A:distinguish_resource_cleanup_from_exception_suppression(f3)   anchors=['assessment:distinguish_resource_cleanup_from_exception_suppression']
  taught-before-tested: A.f3←s01

### s07 · hands_on · Apply the rule
Context-managed resource cleanup — 
QUESTION [code_exercise, core, grading=client] Inside the supplied managed_read function, replace unmanaged acquisition with with open("orders.txt") as file: and place file.read() in its indented block. Leave the checker unchanged. It supplies a readable file-like resource in place of open and checks closure on normal reading and on an injected reading failure; the failure must still propagate. In this supplied comment-source editor, Python source lines have a # PY prefix. Keep that prefix and edit the requested code after it; the unchanged compiler executes those lines. Lines belonging to the supplied checker are scaffolding, not new syntax to learn.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': []} constraints.allowed=['with open(...) as file:', 'indented blocks', 'string literals for the supplied file path', 'file.read()'] blocked=5 items
  file main.py [editable]:
# PY 
# PY import io
# PY import builtins
# PY _resource = None
# PY _failing = False
# PY class SuppliedFile(io.StringIO):
# PY     def read(self):
# PY         if _failing:
# PY             raise RuntimeError('supplied failure')
# PY         return super().read()
# PY def open(path):
# PY     global _resource
# PY     _resource = SuppliedFile('synthetic order')
# PY     return _resource
# PY 
# PY def managed_read():
# PY     file = open("orders.txt")
# PY     file.read()
# PY 
# PY def check_scope(fail):
# PY     global _failing
# PY     _failing = fail
# PY     raised = False
# PY     try:
# PY         managed_read()
# PY     except RuntimeError:
# PY         raised = True
# PY     return {'closed':_resource.closed, 'exception_propagated':raised}

# Supplied compiler: keep unchanged. It executes the # PY source lines below.
exec('\n'.join(line[5:] for line in open('main.py').read().splitlines() if line.startswith('# PY ')), globals())

  SOLUTION main.py:
# PY 
# PY import io
# PY import builtins
# PY _resource = None
# PY _failing = False
# PY class SuppliedFile(io.StringIO):
# PY     def read(self):
# PY         if _failing:
# PY             raise RuntimeError('supplied failure')
# PY         return super().read()
# PY def open(path):
# PY     global _resource
# PY     _resource = SuppliedFile('synthetic order')
# PY     return _resource
# PY 
# PY def managed_read():
# PY     with open("orders.txt") as file:
# PY         file.read()
# PY 
# PY def check_scope(fail):
# PY     global _failing
# PY     _failing = fail
# PY     raised = False
# PY     try:
# PY         managed_read()
# PY     except RuntimeError:
# PY         raised = True
# PY     return {'closed':_resource.closed, 'exception_propagated':raised}

# Supplied compiler: keep unchanged. It executes the # PY source lines below.
exec('\n'.join(line[5:] for line in open('main.py').read().splitlines() if line.startswith('# PY ')), globals())

  test test1 (function_call, visible=None): {"function":"check_scope","args":[false],"expected":{"closed":true,"exception_propagated":false}} | on-fail: Recheck the requested edit and the supplied evidence.
  test test2 (function_call, visible=None): {"function":"check_scope","args":[true],"expected":{"closed":true,"exception_propagated":true}} | on-fail: Recheck the requested edit and the supplied evidence.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"08c0038b0268b7a7cba7e7e3d11bb90c3bddd7df5ecdd0fd71b39a9feb0d9963","tests_passed":2}
  feedback✔: The submitted edits meet the requested practice conditions across the supplied checks.  feedback✘: Recheck the taught rule and the specific evidence. Use with manager as resource: followed by an indented block to enter a managed resource scope.  hints: ['Change only the requested learner-owned lines; leave the supplied inspection or execution harness unchanged.']  remediation→r03
  MEASURES: A:predict_file_cleanup_after_normal_and_exceptional_exit(f1,f2,f4)   anchors=['practice', 'assessment:predict_file_cleanup_after_normal_and_exceptional_exit']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f4←s01

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
QUESTION [choice, core, grading=client] Task A awaits an operation that completes immediately, then awaits a pending future. Where is an opportunity for another runnable task established?
  ✔ option1: While A is suspended waiting on the pending future; the immediate await need not hand over.
      why: Correct: While A is suspended waiting on the pending future; the immediate await need not hand over.
  ✘ option2: Every await necessarily switches to another task.
      why: An immediately completing awaited operation can finish without suspension.
  ✘ option3: Only after A has completely finished; a pending await cannot release execution.
      why: Cooperative scheduling permits other tasks to run while a task waits on a pending future.
  feedback✔: While A is suspended waiting on the pending future; the immediate await need not hand over.  feedback✘: Recheck the taught rule and the specific evidence. Read the explanation for the selected option.  hints: ['Separate the roles named in the prompt; apply the taught distinction rather than treating them as interchangeable.']  remediation→r04
  MEASURES: B:identify_pending_await_as_cooperative_scheduling_opportunity(f2,f3)   anchors=['assessment:identify_pending_await_as_cooperative_scheduling_opportunity']
  taught-before-tested: B.f2←s08; B.f3←s08

### s12 · hands_on · Apply the rule
Cooperative concurrency with async and await — 
QUESTION [code_exercise, stretch, grading=client] Annotate the supplied coroutine trace by replacing TODO only in # MARK comments. call refers to coroutine = task_a(future) before it is run; immediate refers to await immediate(); pending refers to await future when the future is pending; continuation refers to A continuing after that await; sleep refers to await asyncio.sleep(0). Use one label per comment: coroutine_creation or execution for call; no_required_handover or suspends_other_may_run for immediate/pending/sleep; after_future_ready or before_future_ready for continuation. Do not assert which other task runs first. Keep the supplied code and inspection harness unchanged. In this supplied comment-source editor, Python source lines have a # PY prefix. Keep that prefix and edit the requested code after it; the unchanged compiler executes those lines. Lines belonging to the supplied checker are scaffolding, not new syntax to learn.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': []} constraints.allowed=['async def', 'await', 'return', 'coroutine calls', 'await on a supplied future', 'variable assignment', 'integer literals', 'import asyncio', 'asyncio.sleep(0)', 'comments'] blocked=7 items
  file main.py [editable]:
# PY 
# PY import asyncio
# PY async def immediate():
# PY     return 1
# PY async def task_a(future):
# PY     value = await immediate()
# PY     value = await future
# PY     await asyncio.sleep(0)
# PY     return value
# PY 
# These annotations refer to coroutine = task_a(future), its awaits and continuation.
# MARK call: TODO
# MARK immediate: TODO
# MARK pending: TODO
# MARK continuation: TODO
# MARK sleep: TODO
# PY 
# PY def inspect_annotation(point):
# PY     for line in open('main.py').read().splitlines():
# PY         if line.startswith('# MARK '+point+':'):
# PY             return line.split(':',1)[1].strip()
# PY     return 'missing'

# Supplied compiler: keep unchanged. It executes the # PY source lines below.
exec('\n'.join(line[5:] for line in open('main.py').read().splitlines() if line.startswith('# PY ')), globals())

  SOLUTION main.py:
# PY 
# PY import asyncio
# PY async def immediate():
# PY     return 1
# PY async def task_a(future):
# PY     value = await immediate()
# PY     value = await future
# PY     await asyncio.sleep(0)
# PY     return value
# PY 
# These annotations refer to coroutine = task_a(future), its awaits and continuation.
# MARK call: coroutine_creation
# MARK immediate: no_required_handover
# MARK pending: suspends_other_may_run
# MARK continuation: after_future_ready
# MARK sleep: suspends_other_may_run
# PY 
# PY def inspect_annotation(point):
# PY     for line in open('main.py').read().splitlines():
# PY         if line.startswith('# MARK '+point+':'):
# PY             return line.split(':',1)[1].strip()
# PY     return 'missing'

# Supplied compiler: keep unchanged. It executes the # PY source lines below.
exec('\n'.join(line[5:] for line in open('main.py').read().splitlines() if line.startswith('# PY ')), globals())

  test test1 (function_call, visible=None): {"function":"inspect_annotation","args":["call"],"expected":"coroutine_creation"} | on-fail: Recheck the requested edit and the supplied evidence.
  test test2 (function_call, visible=None): {"function":"inspect_annotation","args":["immediate"],"expected":"no_required_handover"} | on-fail: Recheck the requested edit and the supplied evidence.
  test test3 (function_call, visible=None): {"function":"inspect_annotation","args":["pending"],"expected":"suspends_other_may_run"} | on-fail: Recheck the requested edit and the supplied evidence.
  test test4 (function_call, visible=None): {"function":"inspect_annotation","args":["continuation"],"expected":"after_future_ready"} | on-fail: Recheck the requested edit and the supplied evidence.
  test test5 (function_call, visible=None): {"function":"inspect_annotation","args":["sleep"],"expected":"suspends_other_may_run"} | on-fail: Recheck the requested edit and the supplied evidence.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"be208653804a46260713d4038b9020001c9f0b2b2f9fd012695e79a7f2a3623a","tests_passed":5}
  feedback✔: The submitted edits meet the requested practice conditions across the supplied checks.  feedback✘: Recheck the taught rule and the specific evidence. Calling an async def function produces a coroutine; awaiting it runs it and returns its result when it completes.  hints: ['Change only the requested learner-owned lines; leave the supplied inspection or execution harness unchanged.']  remediation→r05
  MEASURES: B:predict_immediate_coroutine_completion_without_suspension(f1,f3); B:trace_coroutine_resumption_after_future_completion(f4); B:identify_asyncio_sleep_suspension_including_zero_delay(f5)   anchors=['practice', 'assessment:predict_immediate_coroutine_completion_without_suspension', 'assessment:trace_coroutine_resumption_after_future_completion', 'assessment:identify_asyncio_sleep_suspension_including_zero_delay']
  taught-before-tested: B.f1←s08; B.f3←s08; B.f4←s08; B.f5←s08

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

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: decorator definitions and applications
· constraints.blocked_syntax: httpx.AsyncClient(...)

=========

# EVALUATOR PACKET — Python decorators as callable wrappers (tile_007)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.decorator_wrappers — Python decorators as callable wrappers

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: tile_007.s01: prose block without lineage.fact_ids

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
QUESTION [choice, intro, grading=client] Inspect the wrapper:
```python
def decorate(function):
    def inner_function():
        return function()
    return inner_function
```
What happens when the returned wrapper is later called?
  ✔ option1: inner_function calls the supplied function and returns its result.
      why: Correct: inner_function calls the supplied function and returns its result.
  ✘ option2: The original function already ran when decorate returned inner_function.
      why: Returning a callable without parentheses does not call it.
  ✘ option3: The wrapper returns the original callable without calling it.
      why: Its body uses function(), so it calls the supplied function.
  feedback✔: inner_function calls the supplied function and returns its result.  feedback✘: Recheck the taught rule and the specific evidence. Read the explanation for the selected option.  hints: ['Separate the roles named in the prompt; apply the taught distinction rather than treating them as interchangeable.']  remediation→r01
  MEASURES: A:trace_call_from_returned_wrapper_to_original_function(f3)   anchors=['assessment:trace_call_from_returned_wrapper_to_original_function']
  taught-before-tested: A.f3←s01

### s04 · hands_on · Apply the rule
Python decorators as callable wrappers — 
QUESTION [code_exercise, stretch, grading=client] Complete decorate(function) by defining inner_function, whose body calls function and returns its result, then return the inner callable without calling it. The supplied harness compares function = decorate(function) with @decorate: it inspects the original-call trace before any later call, the replacement name, and the later wrapper-to-original path. In the # BIND comments, choose labels to identify original (function_passed_to_decorate or returned_inner_callable), replacement (function_passed_to_decorate or returned_inner_callable), and later (wrapper_then_original or original_without_wrapper). Keep that harness unchanged. In this supplied comment-source editor, Python source lines have a # PY prefix. Keep that prefix and edit the requested code after it; the unchanged compiler executes those lines. Lines belonging to the supplied checker are scaffolding, not new syntax to learn.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': []} constraints.allowed=['def function():', 'def decorate(function):', 'nested def inner_function():', 'return', 'return function()', 'return inner_function', 'string literals', 'simple name assignment', 'function = decorate(function)', 'calls to locally defined functions', '@decorate'] blocked=5 items
  file main.py [editable]:
# BIND original: TODO
# BIND replacement: TODO
# BIND later: TODO
# PY def decorate(function):
# PY     pass
# PY 
# PY def inspect_decoration(text):
# PY     calls = []
# PY     def original():
# PY         calls.append('original')
# PY         return text
# PY     function = original
# PY     function = decorate(function)
# PY     before = list(calls)
# PY     explicit = function()
# PY     @decorate
# PY     def function():
# PY         calls.append('original')
# PY         return text
# PY     after_definition = list(calls)
# PY     implicit = function()
# PY     return {'before_later_call':before,'after_decorated_definition':after_definition,'explicit_result':explicit,'decorated_result':implicit,'call_path':calls,'replacement_name':function.__name__,'judgements':inspect_bindings()}
# PY 
# PY def inspect_bindings():
# PY     source = open('main.py').read().splitlines()
# PY     return {line[len('# BIND '):].split(':',1)[0]:line.split(':',1)[1].strip() for line in source if line.startswith('# BIND ')}

# Supplied compiler: keep unchanged. It executes the # PY source lines below.
exec('\n'.join(line[5:] for line in open('main.py').read().splitlines() if line.startswith('# PY ')), globals())

  SOLUTION main.py:
# BIND original: function_passed_to_decorate
# BIND replacement: returned_inner_callable
# BIND later: wrapper_then_original
# PY def decorate(function):
# PY     def inner_function():
# PY         return function()
# PY     return inner_function
# PY 
# PY def inspect_decoration(text):
# PY     calls = []
# PY     def original():
# PY         calls.append('original')
# PY         return text
# PY     function = original
# PY     function = decorate(function)
# PY     before = list(calls)
# PY     explicit = function()
# PY     @decorate
# PY     def function():
# PY         calls.append('original')
# PY         return text
# PY     after_definition = list(calls)
# PY     implicit = function()
# PY     return {'before_later_call':before,'after_decorated_definition':after_definition,'explicit_result':explicit,'decorated_result':implicit,'call_path':calls,'replacement_name':function.__name__,'judgements':inspect_bindings()}
# PY 
# PY def inspect_bindings():
# PY     source = open('main.py').read().splitlines()
# PY     return {line[len('# BIND '):].split(':',1)[0]:line.split(':',1)[1].strip() for line in source if line.startswith('# BIND ')}

# Supplied compiler: keep unchanged. It executes the # PY source lines below.
exec('\n'.join(line[5:] for line in open('main.py').read().splitlines() if line.startswith('# PY ')), globals())

  test test1 (function_call, visible=None): {"function":"inspect_decoration","args":["synthetic order"],"expected":{"before_later_call":[],"after_decorated_definition":["original"],"explicit_result":"synthetic order","decorated_result":"synthetic order","call_path":["original","original"],"replacement_name":"inner_function","judgements":{"original":"function_passed_to_decorate","replacement":"returned_inner_callable","later":"wrapper_then_original"}}} | on-fail: Recheck the requested edit and the supplied evidence.
  test test2 (function_call, visible=None): {"function":"inspect_decoration","args":["different order"],"expected":{"before_later_call":[],"after_decorated_definition":["original"],"explicit_result":"different order","decorated_result":"different order","call_path":["original","original"],"replacement_name":"inner_function","judgements":{"original":"function_passed_to_decorate","replacement":"returned_inner_callable","later":"wrapper_then_original"}}} | on-fail: Recheck the requested edit and the supplied evidence.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"e3d142985eb348d4bfff53308ef1af0595cbd8aeaed06717b4ecabcc02a195fc","tests_passed":2}
  feedback✔: The submitted edits meet the requested practice conditions across the supplied checks.  feedback✘: Recheck the taught rule and the specific evidence. A decorator expression is evaluated when a function is defined, called with the function object, and its returned value is bound to the function name.  hints: ['Change only the requested learner-owned lines; leave the supplied inspection or execution harness unchanged.']  remediation→r02
  MEASURES: A:trace_function_binding_before_and_after_decoration(f1,f2); A:trace_call_from_returned_wrapper_to_original_function(f3)   anchors=['practice', 'assessment:trace_function_binding_before_and_after_decoration', 'assessment:trace_call_from_returned_wrapper_to_original_function']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

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

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: from fastapi import ...
· constraints.blocked_syntax: from pydantic import ...
· constraints.blocked_syntax: from sqlalchemy import ...

=========

# EVALUATOR PACKET — Isolated Python environments and compatible dependency installation (tile_008)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.isolated_environments — Isolated Python environments and compatible dependency installation

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: tile_008.s01: prose block without lineage.fact_ids

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
QUESTION [choice, intro, grading=client] An activated .venv is expected. `which python` points outside .venv, and `python -m pip show jsonschema` reports a Location outside .venv. Which judgement is supported?
  ✔ option1: These outputs do not verify installation in the intended environment.
      why: Correct: These outputs do not verify installation in the intended environment.
  ✘ option2: A package name alone proves the intended environment is in use.
      why: Check the interpreter path and the package location, not just its name.
  ✘ option3: Activation text is enough; interpreter and package paths do not matter.
      why: The interpreter path confirms the environment, and pip show reports version and location.
  feedback✔: These outputs do not verify installation in the intended environment.  feedback✘: Recheck the taught rule and the specific evidence. Read the explanation for the selected option.  hints: ['Separate the roles named in the prompt; apply the taught distinction rather than treating them as interchangeable.']  remediation→r01
  MEASURES: A:verify_installed_dependency_version_and_environment_location(f3,f4)   anchors=['assessment:verify_installed_dependency_version_and_environment_location']
  taught-before-tested: A.f3←s01; A.f4←s01

### s05 · hands_on · Apply the rule
Isolated Python environments and compatible dependency installation — 
QUESTION [classify, stretch, grading=client] Inspect these hypothetical Unix transcripts independently. Does each establish creation, activation, the intended interpreter and a dependency installed inside .venv?
  'python -m venv .venv
source .venv/bin/activate
which python
/workshop/.venv/bin/python
python -m pip install jsonschema
Successfully installed jsonschema
python -m pip show jsonschema
Version: 4.26.0
Location: /workshop/.venv/lib/python3.12/site-packages' -> Verified in .venv
      feedback: The interpreter and dependency location both belong to .venv.
  'python -m venv .venv
source .venv/bin/activate
which python
/usr/bin/python
python -m pip show jsonschema
Version: 4.26.0
Location: /usr/lib/python3.12/site-packages' -> Not verified in the intended environment
      feedback: Creation and an activation command do not override evidence that the selected interpreter and package are outside .venv.
  'python -m venv .venv
which python
/usr/bin/python
python -m pip install jsonschema
Successfully installed jsonschema' -> Not verified in the intended environment
      feedback: This does not verify activation or the intended environment interpreter; a successful install alone is insufficient.
  feedback✔: Each judgement follows the specific evidence in its excerpt or URL, not a package name, response alone or an unrelated permission.  feedback✘: Recheck the taught rule and the specific evidence. A virtual environment has a particular Python installation and its own installed packages, allowing applications to use different dependency versions.  hints: ['Compare the evidence component by component. Look for an excerpt that appears successful but misses a required condition.']  remediation→r02
  MEASURES: A:explain_interpreter_and_dependency_isolation(f1); A:create_activate_and_verify_environment_interpreter(f2,f4); A:verify_installed_dependency_version_and_environment_location(f3,f4)   anchors=['practice', 'assessment:explain_interpreter_and_dependency_isolation', 'assessment:create_activate_and_verify_environment_interpreter', 'assessment:verify_installed_dependency_version_and_environment_location']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f4←s01; A.f3←s01; A.f4←s01

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

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: tile_009.s01: prose block without lineage.fact_ids

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
QUESTION [choice, intro, grading=client] For one complete HTTP request, which application-side event order is correct?
  ✔ option1: receive yields http.request, then send gets http.response.start, then http.response.body.
      why: Correct: receive yields http.request, then send gets http.response.start, then http.response.body.
  ✘ option2: send gets http.response.body before http.response.start.
      why: Response metadata precedes response body content.
  ✘ option3: The application must implement network handling before it can receive an event.
      why: The supplied server invokes the application and handles the network; the application exchanges events.
  feedback✔: receive yields http.request, then send gets http.response.start, then http.response.body.  feedback✘: Recheck the taught rule and the specific evidence. Read the explanation for the selected option.  hints: ['Separate the roles named in the prompt; apply the taught distinction rather than treating them as interchangeable.']  remediation→r01
  MEASURES: A:trace_application_request_and_response_events(f3)   anchors=['assessment:trace_application_request_and_response_events']
  taught-before-tested: A.f3←s01

### s05 · hands_on · Apply the rule
ASGI server and application request lifecycle — 
QUESTION [code_exercise, stretch, grading=client] Complete app(scope, receive, send): await receive once, then await send for http.response.start using supplied_status and supplied_headers, then await send for http.response.body using supplied_body. The checker supplies the events; do not choose statuses or implement networking. In # NETWORK_AND_INVOCATION replace TODO with server or application to identify who handles the network and invokes the app. Leave the harness unchanged; it varies the supplied metadata and body. In this supplied comment-source editor, Python source lines have a # PY prefix. Keep that prefix and edit the requested code after it; the unchanged compiler executes those lines. Lines belonging to the supplied checker are scaffolding, not new syntax to learn.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': []} constraints.allowed=['async def app(scope, receive, send):', 'await receive()', 'await send(...)', 'Local variable assignment', 'Dictionary literals for ASGI events', 'String literals for event types and keys', 'Integer literals for the supplied status', 'List and tuple literals for the supplied headers', 'Bytes literals for the supplied headers and body'] blocked=9 items
  file main.py [editable]:
# PY supplied_status = 200
# PY supplied_headers = [(b"content-type", b"application/json")]
# PY supplied_body = b"{}"
# NETWORK_AND_INVOCATION: TODO
# PY async def app(scope, receive, send):
# PY     pass
# PY 
# PY import asyncio
# PY def check_events(status, body):
# PY     trace = []
# PY     request = {'type':'http.request','body':b'','more_body':False}
# PY     async def receive():
# PY         trace.append(['receive',request['type']])
# PY         return request
# PY     async def send(event):
# PY         trace.append(['send',event['type'],event.get('status'),[[x.decode() for x in pair] for pair in event.get('headers',[])],event.get('body',b'').decode()])
# PY     global supplied_status, supplied_body
# PY     supplied_status, supplied_body = status, body.encode()
# PY     coroutine = app({'type':'http','path':'/orders/42','method':'GET'},receive,send)
# PY     try:
# PY         coroutine.send(None)
# PY     except StopIteration:
# PY         pass
# PY     responsibility = ''
# PY     for line in open('main.py').read().splitlines():
# PY         if line.startswith('# NETWORK_AND_INVOCATION:'):
# PY             responsibility = line.split(':',1)[1].strip()
# PY     return {'events':trace,'network_and_invocation':responsibility}

# Supplied compiler: keep unchanged. It executes the # PY source lines below.
exec('\n'.join(line[5:] for line in open('main.py').read().splitlines() if line.startswith('# PY ')), globals())

  SOLUTION main.py:
# PY supplied_status = 200
# PY supplied_headers = [(b"content-type", b"application/json")]
# PY supplied_body = b"{}"
# NETWORK_AND_INVOCATION: server
# PY async def app(scope, receive, send):
# PY     request = await receive()
# PY     await send({"type":"http.response.start", "status":supplied_status, "headers":supplied_headers})
# PY     await send({"type":"http.response.body", "body":supplied_body})
# PY 
# PY import asyncio
# PY def check_events(status, body):
# PY     trace = []
# PY     request = {'type':'http.request','body':b'','more_body':False}
# PY     async def receive():
# PY         trace.append(['receive',request['type']])
# PY         return request
# PY     async def send(event):
# PY         trace.append(['send',event['type'],event.get('status'),[[x.decode() for x in pair] for pair in event.get('headers',[])],event.get('body',b'').decode()])
# PY     global supplied_status, supplied_body
# PY     supplied_status, supplied_body = status, body.encode()
# PY     coroutine = app({'type':'http','path':'/orders/42','method':'GET'},receive,send)
# PY     try:
# PY         coroutine.send(None)
# PY     except StopIteration:
# PY         pass
# PY     responsibility = ''
# PY     for line in open('main.py').read().splitlines():
# PY         if line.startswith('# NETWORK_AND_INVOCATION:'):
# PY             responsibility = line.split(':',1)[1].strip()
# PY     return {'events':trace,'network_and_invocation':responsibility}

# Supplied compiler: keep unchanged. It executes the # PY source lines below.
exec('\n'.join(line[5:] for line in open('main.py').read().splitlines() if line.startswith('# PY ')), globals())

  test test1 (function_call, visible=None): {"function":"check_events","args":[200,"{}"],"expected":{"events":[["receive","http.request"],["send","http.response.start",200,[["content-type","application/json"]],""],["send","http.response.body",null,[],"{}"]],"network_and_invocation":"server"}} | on-fail: Recheck the requested edit and the supplied evidence.
  test test2 (function_call, visible=None): {"function":"check_events","args":[200,"{\"order\":42}"],"expected":{"events":[["receive","http.request"],["send","http.response.start",200,[["content-type","application/json"]],""],["send","http.response.body",null,[],"{\"order\":42}"]],"network_and_invocation":"server"}} | on-fail: Recheck the requested edit and the supplied evidence.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"43d4b2a1bb8d529539504da1e340b2ab48f4770741da279367ee56cc022c62e3","tests_passed":2}
  feedback✔: The submitted edits meet the requested practice conditions across the supplied checks.  feedback✘: Recheck the taught rule and the specific evidence. An ASGI server handles the network connection and invokes an application callable through the ASGI interface.  hints: ['Change only the requested learner-owned lines; leave the supplied inspection or execution harness unchanged.']  remediation→r02
  MEASURES: A:locate_server_network_and_invocation_responsibilities(f1); A:identify_application_callable_and_event_interface(f2); A:trace_application_request_and_response_events(f3)   anchors=['practice', 'assessment:locate_server_network_and_invocation_responsibilities', 'assessment:identify_application_callable_and_event_interface', 'assessment:trace_application_request_and_response_events']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

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

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: BaseModel subclasses
· constraints.blocked_syntax: httpx.AsyncClient(...)

=========

# EVALUATOR PACKET — Local password hashing and credential verification without an OAuth password grant (tile_010)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = auth.local_password_verification — Local password hashing and credential verification without an OAuth password grant

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=3
  warn: tile_010.s04: remediation tile_010.r03 re-teaches [] but the check measures ['auth.local_password_verification#f3'] — a learner who fails it is sent to an unrelated fact
  warn: tile_010.s01: prose block without lineage.fact_ids
  warn: tile_010.r03: prose block without lineage.fact_ids

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
QUESTION [choice, intro, grading=client] Which password-storage design separates storage, salt, and work-factor roles correctly?
  ✔ option1: Store a password hash; salts distinguish hashes, and a work factor raises guessing cost.
      why: Correct: Store a password hash; salts distinguish hashes, and a work factor raises guessing cost.
  ✘ option2: Store reversible encryption; salts make it equivalent to password hashing.
      why: Password storage should use password hashing rather than reversible encryption.
  ✘ option3: Store a password hash; the salt replaces the work factor by providing the same cost control.
      why: Salts distinguish hashes; adjustable work factors control guessing cost. Their roles differ.
  feedback✔: Store a password hash; salts distinguish hashes, and a work factor raises guessing cost.  feedback✘: Recheck the taught rule and the specific evidence. Read the explanation for the selected option.  hints: ['Separate the roles named in the prompt; apply the taught distinction rather than treating them as interchangeable.']  remediation→r01
  MEASURES: A:identify_safe_password_storage(f1); A:distinguish_salt_and_work_factor_roles(f2)   anchors=['assessment:identify_safe_password_storage', 'assessment:distinguish_salt_and_work_factor_roles']
  taught-before-tested: A.f1←s01; A.f2←s01

### s03 · check · Check the distinction
Local password hashing and credential verification without an OAuth password grant — 
QUESTION [choice, core, grading=client] Given password_hash = PasswordHash.recommended() and stored_hash = password_hash.hash(password), how should a submitted password be checked?
  ✘ option1: password_hash.verify(stored_hash, plain_password)
      why: The taught argument order is submitted plaintext first, stored hash second.
  ✘ option2: Store plain_password and compare it directly instead.
      why: Store the hash and use the library's verification method, not plaintext storage.
  ✔ option3: password_hash.verify(plain_password, stored_hash)
      why: Correct: password_hash.verify(plain_password, stored_hash)
  feedback✔: password_hash.verify(plain_password, stored_hash)  feedback✘: Recheck the taught rule and the specific evidence. Read the explanation for the selected option.  hints: ['Separate the roles named in the prompt; apply the taught distinction rather than treating them as interchangeable.']  remediation→r02
  MEASURES: A:identify_correct_pwdlib_hashing_and_verification(f3)   anchors=['assessment:identify_correct_pwdlib_hashing_and_verification']
  taught-before-tested: A.f3←s01

### s04 · hands_on · Apply the rule
Local password hashing and credential verification without an OAuth password grant — 
QUESTION [classify, stretch, grading=client] Inspect each hypothetical password-storage and verification excerpt. Judge the design, not whether a library is available in this player. The stated True/False observations are supplied evidence, not executed output.
  'from pwdlib import PasswordHash
password_hash = PasswordHash.recommended()
stored_hash = password_hash.hash(password)
matching_result = password_hash.verify(password, stored_hash)
nonmatching_result = password_hash.verify(different_password, stored_hash)
# Supplied observation: matching_result is True; nonmatching_result is False.' -> Correct storage and verification pattern
      feedback: Store the library hash and verify submitted plaintext against it; the two observations satisfy matching and nonmatching checks.
  'stored_hash = password
# Persist stored_hash as the password record.' -> Unsafe storage
      feedback: The persisted value is plaintext, not a password hash.
  'password_hash = PasswordHash.recommended()
stored_hash = password_hash.hash(password)
matching_result = password_hash.verify(stored_hash, password)' -> Incorrect verification pattern
      feedback: Verification takes submitted plaintext first and stored hash second.
  feedback✔: Each judgement follows the specific evidence in its excerpt or URL, not a package name, response alone or an unrelated permission.  feedback✘: Recheck the taught rule and the specific evidence. Password storage should use password hashing rather than plaintext storage or reversible encryption.  hints: ['Compare the evidence component by component. Look for an excerpt that appears successful but misses a required condition.']  remediation→r03
  MEASURES: A:identify_correct_pwdlib_hashing_and_verification(f3)   anchors=['practice']
  taught-before-tested: A.f3←s01

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

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: tile_011.s01: prose block without lineage.fact_ids

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
QUESTION [choice, intro, grading=client] Inspect:
```python
class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True)
```
What marks id as the persistent row key?
  ✔ option1: primary_key=True in mapped_column.
      why: Correct: primary_key=True in mapped_column.
  ✘ option2: The name id alone, without a primary-key declaration.
      why: The explicit primary-key marker declares the key; the name alone is not the marker.
  ✘ option3: Mapped[int] alone, regardless of mapped_column arguments.
      why: The integer annotation and explicit primary-key marker serve distinct purposes.
  feedback✔: primary_key=True in mapped_column.  feedback✘: Recheck the taught rule and the specific evidence. Read the explanation for the selected option.  hints: ['Separate the roles named in the prompt; apply the taught distinction rather than treating them as interchangeable.']  remediation→r01
  MEASURES: A:identify_declared_persistent_row_key(f2)   anchors=['assessment:identify_declared_persistent_row_key']
  taught-before-tested: A.f2←s01

### s05 · hands_on · Apply the rule
Orm entity mapping — 
QUESTION [code_exercise, stretch, grading=client] Declare a shared Base and map an Order entity to the orders table with an integer id primary-key attribute. Use only the supplied SQLAlchemy declarations; leave the inspection harness unchanged. The checker examines the inheritance, table name, integer annotation, explicit primary key and two instances with different id values. No database writes or HTTP endpoints are needed.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': ['sqlalchemy']} constraints.allowed=['from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column', 'class Base(DeclarativeBase):', 'pass', 'class Order(Base):', '__tablename__ = "orders"', 'id: Mapped[int] = mapped_column(primary_key=True)'] blocked=14 items
  file main.py [editable]:
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# Declare Base and Order here.

def inspect_order(identity):
    order = Order(id=identity)
    return {'table':Order.__tablename__, 'inherits_base':issubclass(Order,Base),'primary_key':[c.name for c in Order.__table__.primary_key.columns],'integer_type':str(Order.__table__.c.id.type),'annotation':str(Order.__annotations__['id']),'id':order.id}

  SOLUTION main.py:
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
class Base(DeclarativeBase):
    pass
class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)

def inspect_order(identity):
    order = Order(id=identity)
    return {'table':Order.__tablename__, 'inherits_base':issubclass(Order,Base),'primary_key':[c.name for c in Order.__table__.primary_key.columns],'integer_type':str(Order.__table__.c.id.type),'annotation':str(Order.__annotations__['id']),'id':order.id}

  test test1 (function_call, visible=None): {"function":"inspect_order","args":[42],"expected":{"table":"orders","inherits_base":true,"primary_key":["id"],"integer_type":"INTEGER","annotation":"sqlalchemy.orm.base.Mapped[int]","id":42}} | on-fail: Recheck the requested edit and the supplied evidence.
  test test2 (function_call, visible=None): {"function":"inspect_order","args":[43],"expected":{"table":"orders","inherits_base":true,"primary_key":["id"],"integer_type":"INTEGER","annotation":"sqlalchemy.orm.base.Mapped[int]","id":43}} | on-fail: Recheck the requested edit and the supplied evidence.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"e67aa8dc90ae320b5cc8fdd2f8bd46d04829954bfd902a8506c23d4005ea3508","tests_passed":2}
  feedback✔: The submitted edits meet the requested practice conditions across the supplied checks.  feedback✘: Recheck the taught rule and the specific evidence. A mapped class associates Python attributes with a database table's columns; first create the shared base with class Base(DeclarativeBase): pass, then inherit mapped entities from Base and declare attributes with Mapped[Type] and mapped_column(...).  hints: ['Change only the requested learner-owned lines; leave the supplied inspection or execution harness unchanged.']  remediation→r02
  MEASURES: A:determine_mapped_table_and_columns(f1,f3)   anchors=['practice', 'assessment:determine_mapped_table_and_columns']
  taught-before-tested: A.f1←s01; A.f3←s01

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

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: UniqueConstraint(...)
· constraints.blocked_syntax: CheckConstraint(...)
· constraints.blocked_syntax: create_async_engine(...)
· constraints.blocked_syntax: async_sessionmaker(...)
· constraints.blocked_syntax: session.execute(...)

=========

# EVALUATOR PACKET — CORS preflight behavior · Choosing HTTP success and failure statuses (tile_012)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = http.cors_preflight — CORS preflight behavior
B = http.status_selection — Choosing HTTP success and failure statuses

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: tile_012.s01: prose block without lineage.fact_ids
  warn: tile_012.s05: prose block without lineage.fact_ids

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
QUESTION [choice, intro, grading=client] A credentialed response has Access-Control-Allow-Origin: * and Access-Control-Allow-Credentials: true. Is that sufficient for credentialed cross-origin response access?
  ✔ option1: No; an explicit allowed origin is required alongside Allow-Credentials: true.
      why: Correct: No; an explicit allowed origin is required alongside Allow-Credentials: true.
  ✘ option2: Yes; true makes the wildcard sufficient.
      why: Credentialed responses require an explicit allowed origin rather than *.
  ✘ option3: Yes; the wildcard replaces the need to inspect the credentials header.
      why: The explicit origin and credentials allowance are both required.
  feedback✔: No; an explicit allowed origin is required alongside Allow-Credentials: true.  feedback✘: Recheck the taught rule and the specific evidence. Read the explanation for the selected option.  hints: ['Separate the roles named in the prompt; apply the taught distinction rather than treating them as interchangeable.']  remediation→r01
  MEASURES: A:evaluate_credentialed_origin_requirements(f4)   anchors=['assessment:evaluate_credentialed_origin_requirements']
  taught-before-tested: A.f4←s01

### s04 · hands_on · Apply the rule
CORS preflight behavior — 
QUESTION [classify, core, grading=client] Inspect each independent exchange for https://shop.example calling the API. Distinguish preflight permission from completion of PUT, and require the credentialed response rules where credentials are specified.
  'OPTIONS /orders/42 HTTP/1.1
Host: api.example
Origin: https://shop.example
Access-Control-Request-Method: PUT
Access-Control-Request-Headers: content-type


HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://shop.example
Access-Control-Allow-Methods: PUT
Access-Control-Allow-Headers: content-type

' -> Preflight permits intended PUT; PUT not yet completed
      feedback: The allowed origin, method and header match the request; an OPTIONS permission response is not completion of PUT.
  'Credentialed response to Origin: https://shop.example
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://shop.example
Access-Control-Allow-Credentials: true

' -> Credentialed response satisfies origin/credentials rules
      feedback: The explicit origin matches and Allow-Credentials is true.
  'Credentialed response to Origin: https://shop.example
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true

' -> Credentialed response fails origin/credentials rules
      feedback: A wildcard allowed origin is insufficient for credentialed response access.
  'OPTIONS /orders/42 HTTP/1.1
Host: api.example
Origin: https://shop.example
Access-Control-Request-Method: PUT
Access-Control-Request-Headers: content-type


HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://shop.example
Access-Control-Allow-Methods: GET
Access-Control-Allow-Headers: content-type

' -> Preflight does not permit intended method
      feedback: The intended PUT is not in the supplied allowed-method value.
  feedback✔: Each judgement follows the specific evidence in its excerpt or URL, not a package name, response alone or an unrelated permission.  feedback✘: Recheck the taught rule and the specific evidence. A browser preflights some cross-origin requests with OPTIONS to ask whether the intended method and headers are permitted before sending the actual request.  hints: ['Compare the evidence component by component. Look for an excerpt that appears successful but misses a required condition.']  remediation→r02
  MEASURES: A:identify_preflight_and_intended_request(f1,f2); A:determine_preflight_permission_from_headers(f2,f3); A:evaluate_credentialed_origin_requirements(f4)   anchors=['practice', 'assessment:identify_preflight_and_intended_request', 'assessment:determine_preflight_permission_from_headers', 'assessment:evaluate_credentialed_origin_requirements']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f2←s01; A.f3←s01; A.f4←s01

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
QUESTION [choice, core, grading=client] One orders request fails due to an unexpected server condition; another cannot be handled temporarily during maintenance. Which pair matches those outcomes, in that order?
  ✘ option1: 500 for both; temporary maintenance cannot be distinguished.
      why: 503 specifically denotes temporary inability to handle the request.
  ✔ option2: 500, then 503.
      why: Correct: 500, then 503.
  ✘ option3: 503, then 500.
      why: 500 is for the unexpected condition; 503 is for temporary inability such as maintenance.
  feedback✔: 500, then 503.  feedback✘: Recheck the taught rule and the specific evidence. Read the explanation for the selected option.  hints: ['Separate the roles named in the prompt; apply the taught distinction rather than treating them as interchangeable.']  remediation→r03
  MEASURES: B:distinguish_unexpected_and_temporary_server_failures(f4)   anchors=['assessment:distinguish_unexpected_and_temporary_server_failures']
  taught-before-tested: B.f4←s05

### s09 · hands_on · Apply the rule
Choosing HTTP success and failure statuses — 
QUESTION [code_exercise, stretch, grading=client] Replace the zero value in each supplied variable with the status appropriate for its named outcome. The outcomes are: order_retrieval_status = retrieval; order_creation_status = creation; order_no_content_status = no content; order_request_error_status = request error; order_missing_credentials_status = missing credentials; order_refusal_status = refusal; order_not_found_status = not found; order_conflict_status = conflict; order_unexpected_failure_status = unexpected failure; order_temporary_unavailability_status = temporary unavailability. Keep the variable names and inspection helper unchanged. The checker grades every assignment; no endpoint implementation is needed. Also label each # STATUS_CLASS pattern as informational, successful, redirection, client error or server error. Each class comment is graded. In this supplied comment-source editor, Python source lines have a # PY prefix. Keep that prefix and edit the requested code after it; the unchanged compiler executes those lines. Lines belonging to the supplied checker are scaffolding, not new syntax to learn.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': []} constraints.allowed=['simple variable assignment', 'integer literals'] blocked=11 items
  file main.py [editable]:
# PY order_retrieval_status = 0
# PY order_creation_status = 0
# PY order_no_content_status = 0
# PY order_request_error_status = 0
# PY order_missing_credentials_status = 0
# PY order_refusal_status = 0
# PY order_not_found_status = 0
# PY order_conflict_status = 0
# PY order_unexpected_failure_status = 0
# PY order_temporary_unavailability_status = 0
# PY 
# PY def inspect_status(name):
# PY     return globals()[name]
# STATUS_CLASS 1xx: TODO
# STATUS_CLASS 2xx: TODO
# STATUS_CLASS 3xx: TODO
# STATUS_CLASS 4xx: TODO
# STATUS_CLASS 5xx: TODO
# PY 
# PY def inspect_class(pattern):
# PY     for line in open('main.py').read().splitlines():
# PY         if line.startswith('# STATUS_CLASS '+pattern+':'):
# PY             return line.split(':',1)[1].strip()
# PY     return 'missing'

# Supplied compiler: keep unchanged. It executes the # PY source lines below.
exec('\n'.join(line[5:] for line in open('main.py').read().splitlines() if line.startswith('# PY ')), globals())

  SOLUTION main.py:
# PY order_retrieval_status = 200
# PY order_creation_status = 201
# PY order_no_content_status = 204
# PY order_request_error_status = 400
# PY order_missing_credentials_status = 401
# PY order_refusal_status = 403
# PY order_not_found_status = 404
# PY order_conflict_status = 409
# PY order_unexpected_failure_status = 500
# PY order_temporary_unavailability_status = 503
# PY 
# PY def inspect_status(name):
# PY     return globals()[name]
# STATUS_CLASS 1xx: informational
# STATUS_CLASS 2xx: successful
# STATUS_CLASS 3xx: redirection
# STATUS_CLASS 4xx: client error
# STATUS_CLASS 5xx: server error
# PY 
# PY def inspect_class(pattern):
# PY     for line in open('main.py').read().splitlines():
# PY         if line.startswith('# STATUS_CLASS '+pattern+':'):
# PY             return line.split(':',1)[1].strip()
# PY     return 'missing'

# Supplied compiler: keep unchanged. It executes the # PY source lines below.
exec('\n'.join(line[5:] for line in open('main.py').read().splitlines() if line.startswith('# PY ')), globals())

  test test1 (function_call, visible=None): {"function":"inspect_status","args":["order_retrieval_status"],"expected":200} | on-fail: Recheck the requested edit and the supplied evidence.
  test test2 (function_call, visible=None): {"function":"inspect_status","args":["order_creation_status"],"expected":201} | on-fail: Recheck the requested edit and the supplied evidence.
  test test3 (function_call, visible=None): {"function":"inspect_status","args":["order_no_content_status"],"expected":204} | on-fail: Recheck the requested edit and the supplied evidence.
  test test4 (function_call, visible=None): {"function":"inspect_status","args":["order_request_error_status"],"expected":400} | on-fail: Recheck the requested edit and the supplied evidence.
  test test5 (function_call, visible=None): {"function":"inspect_status","args":["order_missing_credentials_status"],"expected":401} | on-fail: Recheck the requested edit and the supplied evidence.
  test test6 (function_call, visible=None): {"function":"inspect_status","args":["order_refusal_status"],"expected":403} | on-fail: Recheck the requested edit and the supplied evidence.
  test test7 (function_call, visible=None): {"function":"inspect_status","args":["order_not_found_status"],"expected":404} | on-fail: Recheck the requested edit and the supplied evidence.
  test test8 (function_call, visible=None): {"function":"inspect_status","args":["order_conflict_status"],"expected":409} | on-fail: Recheck the requested edit and the supplied evidence.
  test test9 (function_call, visible=None): {"function":"inspect_status","args":["order_unexpected_failure_status"],"expected":500} | on-fail: Recheck the requested edit and the supplied evidence.
  test test10 (function_call, visible=None): {"function":"inspect_status","args":["order_temporary_unavailability_status"],"expected":503} | on-fail: Recheck the requested edit and the supplied evidence.
  test test11 (function_call, visible=None): {"function":"inspect_class","args":["1xx"],"expected":"informational"} | on-fail: Recheck the requested edit and the supplied evidence.
  test test12 (function_call, visible=None): {"function":"inspect_class","args":["2xx"],"expected":"successful"} | on-fail: Recheck the requested edit and the supplied evidence.
  test test13 (function_call, visible=None): {"function":"inspect_class","args":["3xx"],"expected":"redirection"} | on-fail: Recheck the requested edit and the supplied evidence.
  test test14 (function_call, visible=None): {"function":"inspect_class","args":["4xx"],"expected":"client error"} | on-fail: Recheck the requested edit and the supplied evidence.
  test test15 (function_call, visible=None): {"function":"inspect_class","args":["5xx"],"expected":"server error"} | on-fail: Recheck the requested edit and the supplied evidence.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"e969d3fa7029f5780aa068481345e6610493dd911104c4eab60b49af3a9d8a67","tests_passed":15}
  feedback✔: The submitted edits meet the requested practice conditions across the supplied checks.  feedback✘: Recheck the taught rule and the specific evidence. HTTP status classes distinguish informational 1xx, successful 2xx, redirection 3xx, client error 4xx and server error 5xx outcomes.  hints: ['Change only the requested learner-owned lines; leave the supplied inspection or execution harness unchanged.']  remediation→r04
  MEASURES: B:classify_http_exchange_outcomes(f1); B:choose_success_status_for_outcome(f2); B:choose_client_error_status_for_outcome(f3); B:distinguish_unexpected_and_temporary_server_failures(f4)   anchors=['practice', 'assessment:classify_http_exchange_outcomes', 'assessment:choose_success_status_for_outcome', 'assessment:choose_client_error_status_for_outcome', 'assessment:distinguish_unexpected_and_temporary_server_failures']
  taught-before-tested: B.f1←s05; B.f2←s05; B.f3←s05; B.f4←s05

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

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: BaseModel subclasses

=========

# EVALUATOR PACKET — Pydantic V2 model construction and input conversion (tile_014)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = pydantic.model_validation_conversion — Pydantic V2 model construction and input conversion

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: tile_014.s01: prose block without lineage.fact_ids

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
[VIDEO Constructing models with required fields and defaults] bridge-before: Watch how typed declarations determine required fields and how defaults supply omitted values. The clip calls defaulted fields “optional”; here, that means omission is allowed, not that any value is accepted. | bridge-after: The clip demonstrates construction, missing-field errors, and defaults, but not compatible input conversion or model_validate. The text covers those gaps and explains that incompatible supplied values also raise ValidationError.
  - M81pfi64eeM 535-722s facts=['f1', 'f3', 'f4'] label: Define typed fields, construct a model, and apply defaults | summary: A User class inherits from BaseModel and declares username and email as string fields. Neither field has a default, so constructing User without arguments produces validation errors identifying both missing fields. Supplying strings for both fields succeeds. Adding bio with an empty-string default and is_active with a True default allows those fields to be omitted during construction; the resulting instance receives their declared defaults. Here, “optional fields” means fields that may be omitted because they have defaults.

### s05 · check · Check the distinction
Pydantic V2 model construction and input conversion — 
QUESTION [choice, intro, grading=client] OrderInput declares quantity: int with no default. Ordinary validation accepts quantity='3', but quantity='many' fails. Which interpretation is correct?
  ✔ option1: Accepted input can be converted to integer 3; incompatible input can produce a field validation failure.
      why: Correct: Accepted input can be converted to integer 3; incompatible input can produce a field validation failure.
  ✘ option2: Accepting '3' means quantity remains a string in the validated instance.
      why: Validation can convert accepted input to the declared output type.
  ✘ option3: Any string must be accepted because the numeric-looking string was accepted.
      why: Acceptance of convertible input does not imply acceptance of incompatible input.
  feedback✔: Accepted input can be converted to integer 3; incompatible input can produce a field validation failure.  feedback✘: Recheck the taught rule and the specific evidence. Read the explanation for the selected option.  hints: ['Separate the roles named in the prompt; apply the taught distinction rather than treating them as interchangeable.']  remediation→r01
  MEASURES: A:distinguish_accepted_input_conversion_from_original_input_types(f2); A:identify_invalid_inputs_and_field_validation_failures(f3)   anchors=['assessment:distinguish_accepted_input_conversion_from_original_input_types', 'assessment:identify_invalid_inputs_and_field_validation_failures']
  taught-before-tested: A.f2←s01; A.f3←s01

### s06 · check · Check the distinction
Pydantic V2 model construction and input conversion — 
QUESTION [choice, core, grading=client] OrderInput declares quantity: int and note: str = ''. If both fields are omitted, which description is correct?
  ✘ option1: Both fields have defaults because both have annotations.
      why: An annotation alone does not supply a default.
  ✘ option2: Both are required because their types exclude None.
      why: The declared default makes note omittable; this differs from allowing None.
  ✔ option3: quantity is missing required input; note has its declared empty-string default.
      why: Correct: quantity is missing required input; note has its declared empty-string default.
  feedback✔: quantity is missing required input; note has its declared empty-string default.  feedback✘: Recheck the taught rule and the specific evidence. Read the explanation for the selected option.  hints: ['Separate the roles named in the prompt; apply the taught distinction rather than treating them as interchangeable.']  remediation→r02
  MEASURES: A:determine_required_fields_and_omitted_default_values(f4)   anchors=['assessment:determine_required_fields_and_omitted_default_values']
  taught-before-tested: A.f4←s01

### s07 · hands_on · Apply the rule
Pydantic V2 model construction and input conversion — 
QUESTION [code_exercise, stretch, grading=client] Define a standalone OrderInput request-data model with required quantity: int and note: str defaulting to an empty string. Construct it with quantity="3", and validate equivalent dictionary data with OrderInput.model_validate. Name the constructed instance constructed and the dictionary-validated instance validated. Leave the supplied helper unchanged. It checks both stored instances, required/default declarations and conversion of two different accepted quantities.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': ['pydantic']} constraints.allowed=['from pydantic import BaseModel', 'class OrderInput(BaseModel):', 'quantity: int', 'note: str = ""', 'OrderInput(quantity="3")', 'OrderInput.model_validate({"quantity": "3"})', 'variable assignment', 'instance attribute access', 'string literals', 'integer literals', 'dictionary literals'] blocked=10 items
  file main.py [editable]:
from pydantic import BaseModel
class OrderInput(BaseModel):
    pass
# Create constructed and validated with quantity="3".

def inspect_input(quantity):
    first = OrderInput(quantity=quantity)
    second = OrderInput.model_validate({'quantity':quantity})
    return {'first':[first.quantity,first.note,type(first.quantity).__name__],'second':[second.quantity,second.note,type(second.quantity).__name__],'quantity_required':OrderInput.model_fields['quantity'].is_required(),'note_default':OrderInput.model_fields['note'].default,'constructed':[constructed.quantity,constructed.note],'validated':[validated.quantity,validated.note]}

  SOLUTION main.py:
from pydantic import BaseModel
class OrderInput(BaseModel):
    quantity: int
    note: str = ""
constructed = OrderInput(quantity="3")
validated = OrderInput.model_validate({"quantity":"3"})

def inspect_input(quantity):
    first = OrderInput(quantity=quantity)
    second = OrderInput.model_validate({'quantity':quantity})
    return {'first':[first.quantity,first.note,type(first.quantity).__name__],'second':[second.quantity,second.note,type(second.quantity).__name__],'quantity_required':OrderInput.model_fields['quantity'].is_required(),'note_default':OrderInput.model_fields['note'].default,'constructed':[constructed.quantity,constructed.note],'validated':[validated.quantity,validated.note]}

  test test1 (function_call, visible=None): {"function":"inspect_input","args":["3"],"expected":{"first":[3,"","int"],"second":[3,"","int"],"quantity_required":true,"note_default":"","constructed":[3,""],"validated":[3,""]}} | on-fail: Recheck the requested edit and the supplied evidence.
  test test2 (function_call, visible=None): {"function":"inspect_input","args":["7"],"expected":{"first":[7,"","int"],"second":[7,"","int"],"quantity_required":true,"note_default":"","constructed":[3,""],"validated":[3,""]}} | on-fail: Recheck the requested edit and the supplied evidence.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"f3c363ce6e5457918f327f2e71db417e1c1cd47548c18ff37e74e8538201a401","tests_passed":2}
  feedback✔: The submitted edits meet the requested practice conditions across the supplied checks.  feedback✘: Recheck the taught rule and the specific evidence. Define a Pydantic model by subclassing BaseModel and declaring typed fields, then construct it with Model(field=value, ...) or validate data with Model.model_validate(data).  hints: ['Change only the requested learner-owned lines; leave the supplied inspection or execution harness unchanged.']  remediation→r03
  MEASURES: A:recognize_model_declaration_and_validation_entry_points(f1)   anchors=['practice', 'assessment:recognize_model_declaration_and_validation_entry_points']
  taught-before-tested: A.f1←s01

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

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: @field_validator(...)
· constraints.blocked_syntax: @model_validator(...)
· constraints.blocked_syntax: nested BaseModel field declarations
· constraints.blocked_syntax: model_dump_json(...)

=========

# EVALUATOR PACKET — Reproducible service dependency declarations · Python package organization for a service (tile_015)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.reproducible_dependencies — Reproducible service dependency declarations
B = python.service_packages — Python package organization for a service

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=3
  warn: tile_015.s01: prose block without lineage.fact_ids
  warn: tile_015.s06: prose block without lineage.fact_ids
  warn: tile_015.r04: text contains the name of blocked future concept fastapi_backend.depends ('depends') — check it is not needed to understand

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
[VIDEO Capture dependencies for a reproducible handoff] bridge-before: Watch how installed packages become a requirements.txt declaration. The clip uses bare pip in an activated environment; Devspace uses python -m pip to explicitly select the environment's Python interpreter. | bridge-after: The clip explains sharing the declaration, but omits the install -r command and committed-declaration build workflow. The text supplies both: install from requirements.txt and have the build obtain committed dependencies.
  - AMdG7IjgSPM 135-305s facts=['f1'] label: Save installed dependencies to requirements.txt | summary: The demonstration creates and activates an isolated Python environment, installs example packages, and redirects pip freeze output into requirements.txt. The resulting declaration includes dependencies of the explicitly installed packages, which explains the additional entries. Sharing this file lets another person install the listed dependencies in their own environment.

### s04 · check · Check the distinction
Reproducible service dependency declarations — 
QUESTION [choice, intro, grading=client] A clean service build has a committed requirements.txt. What should it rely on to reconstruct dependencies?
  ✔ option1: The committed declaration, installed in the clean environment.
      why: Correct: The committed declaration, installed in the clean environment.
  ✘ option2: Packages manually installed in a developer's other environment.
      why: Reconstruction uses committed declarations, not another environment's manual state.
  ✘ option3: Overwrite requirements.txt using the empty environment's freeze output before installation.
      why: That replaces the committed declaration instead of reconstructing from it.
  feedback✔: The committed declaration, installed in the clean environment.  feedback✘: Recheck the taught rule and the specific evidence. Read the explanation for the selected option.  hints: ['Separate the roles named in the prompt; apply the taught distinction rather than treating them as interchangeable.']  remediation→r01
  MEASURES: A:reconstruct_dependencies_from_committed_declarations(f3)   anchors=['assessment:reconstruct_dependencies_from_committed_declarations']
  taught-before-tested: A.f3←s01

### s05 · hands_on · Apply the rule
Reproducible service dependency declarations — 
QUESTION [classify, core, grading=client] Each excerpt describes a separate clean isolated environment. The committed requirements.txt is:
attrs==26.1.0
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
referencing==0.37.0
rpds-py==2026.9.1
typing_extensions==4.16.0

Classify whether the evidence reconstructs from that declaration or instead relies on/replaces other state.
  '# Clean environment; committed requirements unchanged
python -m pip install -r requirements.txt
# Supplied observation: installation completes successfully
python -m pip freeze
attrs==26.1.0
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
referencing==0.37.0
rpds-py==2026.9.1
typing_extensions==4.16.0
' -> Reconstructed and verified from committed requirements
      feedback: The installation uses the committed declaration and the inspected versions satisfy every entry.
  '# Original working environment
python -m pip freeze > requirements.txt' -> Captures installed versions only; does not reconstruct
      feedback: This captures existing installed versions; it is not a clean-environment installation from a committed file.
  '# Clean environment
python -m pip freeze > requirements.txt
python -m pip install -r requirements.txt
# Supplied observation: the empty freeze output replaced the committed file.' -> Does not reconstruct the committed requirements
      feedback: Replacing the committed declaration with an empty one loses the dependencies that should be reconstructed.
  '# New environment; no installation from declarations
# Use the packages that happen to be installed in the original environment.' -> Does not reconstruct the committed requirements
      feedback: Another environment's manual package state is not reconstruction from committed declarations.
  feedback✔: Each judgement follows the specific evidence in its excerpt or URL, not a package name, response alone or an unrelated permission.  feedback✘: Recheck the taught rule and the specific evidence. python -m pip freeze reports installed packages and versions, and its output can be saved to requirements.txt for a dependency declaration.  hints: ['Compare the evidence component by component. Look for an excerpt that appears successful but misses a required condition.']  remediation→r02
  MEASURES: A:capture_installed_dependency_versions(f1); A:install_dependencies_from_requirements(f2); A:reconstruct_dependencies_from_committed_declarations(f3)   anchors=['practice', 'assessment:capture_installed_dependency_versions', 'assessment:install_dependencies_from_requirements', 'assessment:reconstruct_dependencies_from_committed_declarations']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

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
QUESTION [choice, core, grading=client] Run the package module with `python -m service.orders` from the parent directory. What is its __name__ during this execution?
  ✘ option1: service
      why: The package name is not the executed module's execution name.
  ✔ option2: __main__
      why: Correct: __main__
  ✘ option3: service.orders
      why: That is the qualified import name; module execution uses __main__.
  feedback✔: __main__  feedback✘: Recheck the taught rule and the specific evidence. Read the explanation for the selected option.  hints: ['Separate the roles named in the prompt; apply the taught distinction rather than treating them as interchangeable.']  remediation→r03
  MEASURES: B:identify_module_execution_name(f3)   anchors=['assessment:identify_module_execution_name']
  taught-before-tested: B.f3←s06

### s09 · hands_on · Apply the rule
Python package organization for a service — 
QUESTION [code_exercise, stretch, grading=client] Complete # PACKAGE comment entries. Supply the empty regular-package marker path, empty orders module path, qualified import name, package-context execution command, and execution name. For relative_context select current_package or working_directory to identify what leading dots mean. The unchanged harness creates the empty files at the supplied paths, imports the module and executes it with the same package context as -m. This player runs the supplied Python filesystem checker, not a shell command. Do not edit the checker. Edit only the six `# PACKAGE` entries. Leave all `# PY` lines and the supplied compiler unchanged.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': []} constraints.allowed=['An empty __init__.py file', 'An empty orders.py module', 'import service.orders', 'Absolute package-qualified imports', 'Relative imports using leading dots', '__name__', 'python -m service.orders'] blocked=7 items
  file main.py [editable]:
# PACKAGE marker: TODO
# PACKAGE module: TODO
# PACKAGE qualified_import: TODO
# PACKAGE command: TODO
# PACKAGE execution_name: TODO
# PACKAGE relative_context: TODO
# PY 
# PY import os, importlib, runpy, sys
# PY def inspect_package(mode):
# PY     source = open('main.py').read().splitlines()
# PY     entries = {}
# PY     for line in source:
# PY         if line.startswith('# PACKAGE '):
# PY             key,value=line[len('# PACKAGE '):].split(':',1)
# PY             entries[key.strip()] = value.strip()
# PY     paths = [entries.get('marker',''),entries.get('module','')]
# PY     for path in paths:
# PY         if path in ['service/__init__.py','service/orders.py']:
# PY             os.makedirs('service',exist_ok=True)
# PY             open(path,'w').close()
# PY     if paths != ['service/__init__.py','service/orders.py']:
# PY         return {'files_correct':False}
# PY     importlib.invalidate_caches()
# PY     if mode == 'import':
# PY         module=importlib.import_module(entries.get('qualified_import',''))
# PY         return {'files_correct':True,'qualified_name':module.__name__,'declared_import':entries.get('qualified_import')}
# PY     sys.modules.pop('service.orders',None)
# PY     namespace=runpy.run_module('service.orders',run_name='__main__')
# PY     return {'files_correct':True,'command':entries.get('command'),'observed_name':namespace['__name__'],'declared_name':entries.get('execution_name'),'relative_import_context':entries.get('relative_context')}

# Supplied compiler: keep unchanged. It executes the # PY source lines below.
exec('\n'.join(line[5:] for line in open('main.py').read().splitlines() if line.startswith('# PY ')), globals())

  SOLUTION main.py:
# PACKAGE marker: service/__init__.py
# PACKAGE module: service/orders.py
# PACKAGE qualified_import: service.orders
# PACKAGE command: python -m service.orders
# PACKAGE execution_name: __main__
# PACKAGE relative_context: current_package
# PY 
# PY import os, importlib, runpy, sys
# PY def inspect_package(mode):
# PY     source = open('main.py').read().splitlines()
# PY     entries = {}
# PY     for line in source:
# PY         if line.startswith('# PACKAGE '):
# PY             key,value=line[len('# PACKAGE '):].split(':',1)
# PY             entries[key.strip()] = value.strip()
# PY     paths = [entries.get('marker',''),entries.get('module','')]
# PY     for path in paths:
# PY         if path in ['service/__init__.py','service/orders.py']:
# PY             os.makedirs('service',exist_ok=True)
# PY             open(path,'w').close()
# PY     if paths != ['service/__init__.py','service/orders.py']:
# PY         return {'files_correct':False}
# PY     importlib.invalidate_caches()
# PY     if mode == 'import':
# PY         module=importlib.import_module(entries.get('qualified_import',''))
# PY         return {'files_correct':True,'qualified_name':module.__name__,'declared_import':entries.get('qualified_import')}
# PY     sys.modules.pop('service.orders',None)
# PY     namespace=runpy.run_module('service.orders',run_name='__main__')
# PY     return {'files_correct':True,'command':entries.get('command'),'observed_name':namespace['__name__'],'declared_name':entries.get('execution_name'),'relative_import_context':entries.get('relative_context')}

# Supplied compiler: keep unchanged. It executes the # PY source lines below.
exec('\n'.join(line[5:] for line in open('main.py').read().splitlines() if line.startswith('# PY ')), globals())

  test test1 (function_call, visible=None): {"function":"inspect_package","args":["import"],"expected":{"files_correct":true,"qualified_name":"service.orders","declared_import":"service.orders"}} | on-fail: Recheck the requested edit and the supplied evidence.
  test test2 (function_call, visible=None): {"function":"inspect_package","args":["execute"],"expected":{"files_correct":true,"command":"python -m service.orders","observed_name":"__main__","declared_name":"__main__","relative_import_context":"current_package"}} | on-fail: Recheck the requested edit and the supplied evidence.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"5c2249d2a587fb65e0cfb848a4e787863b6ff48feb17d825e8a4d4f63d8b2153","tests_passed":2}
  feedback✔: The submitted edits meet the requested practice conditions across the supplied checks.  feedback✘: Recheck the taught rule and the specific evidence. Packages organize modules with qualified names such as package.module; regular packages contain an __init__.py file.  hints: ['Change only the requested learner-owned lines; leave the supplied inspection or execution harness unchanged.']  remediation→r04
  MEASURES: B:resolve_package_qualified_imports(f1,f2); B:resolve_relative_imports_in_package_context(f2); B:identify_module_execution_name(f3)   anchors=['practice', 'assessment:resolve_package_qualified_imports', 'assessment:resolve_relative_imports_in_package_context', 'assessment:identify_module_execution_name']
  taught-before-tested: B.f1←s06; B.f2←s06; B.f2←s06; B.f3←s06

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

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: app.include_router(...)

=========

# EVALUATOR PACKET — Service-schema integrity constraints (tile_017)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = database.service_integrity_constraints — Service-schema integrity constraints

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: tile_017.s01: prose block without lineage.fact_ids

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
QUESTION [choice, intro, grading=client] Under the taught PostgreSQL default UNIQUE(external_reference), an existing row has a null external_reference. A new otherwise-valid row also has null. How does the default compare with UNIQUE NULLS NOT DISTINCT?
  ✔ option1: Default UNIQUE permits the repeated null; NULLS NOT DISTINCT can reject it.
      why: Correct: Default UNIQUE permits the repeated null; NULLS NOT DISTINCT can reject it.
  ✘ option2: Both reject repeated nulls identically.
      why: Default UNIQUE retains distinct-null behavior; NULLS NOT DISTINCT changes that comparison.
  ✘ option3: Default UNIQUE rejects nulls, while NULLS NOT DISTINCT permits them.
      why: This reverses the taught null policies.
  feedback✔: Default UNIQUE permits the repeated null; NULLS NOT DISTINCT can reject it.  feedback✘: Recheck the taught rule and the specific evidence. Read the explanation for the selected option.  hints: ['Separate the roles named in the prompt; apply the taught distinction rather than treating them as interchangeable.']  remediation→r01
  MEASURES: A:identify_duplicate_combination_rejection_under_null_policy(f2)   anchors=['assessment:identify_duplicate_combination_rejection_under_null_policy']
  taught-before-tested: A.f2←s01

### s04 · check · Check the distinction
Service-schema integrity constraints — 
QUESTION [choice, core, grading=client] quantity has CHECK(quantity > 0). Which added constraint rejects absent quantities, while CHECK rejects nonpositive non-null quantities?
  ✘ option1: UNIQUE(quantity)
      why: Uniqueness does not impose the required non-null condition.
  ✘ option2: No added constraint; CHECK alone rejects null as a failed comparison.
      why: CHECK alone does not provide the NOT NULL requirement.
  ✔ option3: NOT NULL
      why: Correct: NOT NULL
  feedback✔: NOT NULL  feedback✘: Recheck the taught rule and the specific evidence. Read the explanation for the selected option.  hints: ['Separate the roles named in the prompt; apply the taught distinction rather than treating them as interchangeable.']  remediation→r02
  MEASURES: A:distinguish_failed_check_rejection_from_null_rejection(f1,f5)   anchors=['assessment:distinguish_failed_check_rejection_from_null_rejection']
  taught-before-tested: A.f1←s01; A.f5←s01

### s05 · hands_on · Apply the rule
Service-schema integrity constraints — 
QUESTION [code_exercise, stretch, grading=client] Complete the supplied CREATE TABLE declaration in # SQL comment lines: primary key on identity, foreign key on customer_reference to customers(identity), quantity NOT NULL with CHECK(quantity > 0), and default UNIQUE(external_reference). Leave customer_reference and external_reference nullable; do not use NULLS NOT DISTINCT. Keep the Python checker unchanged. It inspects the declaration and uses a supplied declaration-and-predicate checker on independent proposed rows against the supplied baseline; this is not a PostgreSQL runtime. In this supplied comment-source editor, Python source lines have a # PY prefix. Keep that prefix and edit the requested code after it; the unchanged compiler executes those lines. Lines belonging to the supplied checker are scaffolding, not new syntax to learn.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': []} constraints.allowed=['Supplied CREATE TABLE scaffold', 'Supplied INTEGER and TEXT column types', 'NOT NULL', 'PRIMARY KEY (identity)', 'FOREIGN KEY (customer_reference) REFERENCES customers (identity)', 'CHECK (quantity > 0)', 'UNIQUE (external_reference)', 'UNIQUE NULLS NOT DISTINCT (external_reference)', 'Parentheses, commas, and a terminating semicolon'] blocked=13 items
  file main.py [editable]:
# SQL CREATE TABLE orders (
# SQL     identity INTEGER,
# SQL     customer_reference INTEGER,
# SQL     quantity INTEGER,
# SQL     external_reference TEXT
# SQL );
# PY 
# PY import re
# PY customers = [[1], [2]]
# PY orders = [[42, 1, 3, 'ORD-A'], [43, 2, 1, None], [44, None, 2, None]]
# PY def inspect_constraint(candidate):
# PY     lines = open('main.py').read().splitlines()
# PY     declaration = '\n'.join(line[len('# SQL '):] for line in lines if line.startswith('# SQL '))
# PY     normalized = re.sub(r'\s+', '', declaration).lower()
# PY     quantity_column = re.search(r'\bquantity\s+integer\b([^,]*)', declaration, re.I)
# PY     flags = {
# PY         'primary_key':'primarykey(identity)' in normalized,
# PY         'foreign_key':'foreignkey(customer_reference)referencescustomers(identity)' in normalized,
# PY         'required_quantity':bool(quantity_column and re.search(r'\bnot\s+null\b', quantity_column.group(1), re.I)),
# PY         'positive_quantity':'check(quantity>0)' in normalized,
# PY         'default_unique':'unique(external_reference)' in normalized,
# PY         'nullable_customer':'customer_referenceintegernotnull' not in normalized,
# PY         'nullable_external':'external_referencetextnotnull' not in normalized,
# PY         'distinct_null_policy':'nullsnotdistinct' not in normalized
# PY     }
# PY     identity, customer, quantity, external = candidate
# PY     accepted = True
# PY     if flags['primary_key']:
# PY         accepted = accepted and identity is not None and identity not in [r[0] for r in orders]
# PY     if flags['foreign_key']:
# PY         accepted = accepted and (customer is None or customer in [r[0] for r in customers])
# PY     if flags['required_quantity']:
# PY         accepted = accepted and quantity is not None
# PY     if flags['positive_quantity']:
# PY         accepted = accepted and (quantity is None or quantity > 0)
# PY     if flags['default_unique']:
# PY         accepted = accepted and (external is None or external not in [r[3] for r in orders])
# PY     if not flags['distinct_null_policy']:
# PY         accepted = accepted and external not in [r[3] for r in orders]
# PY     return {'declared_constraints':flags,'accepted':accepted}

# Supplied compiler: keep unchanged. It executes the # PY source lines below.
exec('\n'.join(line[5:] for line in open('main.py').read().splitlines() if line.startswith('# PY ')), globals())

  SOLUTION main.py:
# SQL CREATE TABLE orders (
# SQL     identity INTEGER,
# SQL     customer_reference INTEGER,
# SQL     quantity INTEGER NOT NULL,
# SQL     external_reference TEXT,
# SQL     PRIMARY KEY (identity),
# SQL     FOREIGN KEY (customer_reference) REFERENCES customers (identity),
# SQL     CHECK (quantity > 0),
# SQL     UNIQUE (external_reference)
# SQL );
# PY 
# PY import re
# PY customers = [[1], [2]]
# PY orders = [[42, 1, 3, 'ORD-A'], [43, 2, 1, None], [44, None, 2, None]]
# PY def inspect_constraint(candidate):
# PY     lines = open('main.py').read().splitlines()
# PY     declaration = '\n'.join(line[len('# SQL '):] for line in lines if line.startswith('# SQL '))
# PY     normalized = re.sub(r'\s+', '', declaration).lower()
# PY     quantity_column = re.search(r'\bquantity\s+integer\b([^,]*)', declaration, re.I)
# PY     flags = {
# PY         'primary_key':'primarykey(identity)' in normalized,
# PY         'foreign_key':'foreignkey(customer_reference)referencescustomers(identity)' in normalized,
# PY         'required_quantity':bool(quantity_column and re.search(r'\bnot\s+null\b', quantity_column.group(1), re.I)),
# PY         'positive_quantity':'check(quantity>0)' in normalized,
# PY         'default_unique':'unique(external_reference)' in normalized,
# PY         'nullable_customer':'customer_referenceintegernotnull' not in normalized,
# PY         'nullable_external':'external_referencetextnotnull' not in normalized,
# PY         'distinct_null_policy':'nullsnotdistinct' not in normalized
# PY     }
# PY     identity, customer, quantity, external = candidate
# PY     accepted = True
# PY     if flags['primary_key']:
# PY         accepted = accepted and identity is not None and identity not in [r[0] for r in orders]
# PY     if flags['foreign_key']:
# PY         accepted = accepted and (customer is None or customer in [r[0] for r in customers])
# PY     if flags['required_quantity']:
# PY         accepted = accepted and quantity is not None
# PY     if flags['positive_quantity']:
# PY         accepted = accepted and (quantity is None or quantity > 0)
# PY     if flags['default_unique']:
# PY         accepted = accepted and (external is None or external not in [r[3] for r in orders])
# PY     if not flags['distinct_null_policy']:
# PY         accepted = accepted and external not in [r[3] for r in orders]
# PY     return {'declared_constraints':flags,'accepted':accepted}

# Supplied compiler: keep unchanged. It executes the # PY source lines below.
exec('\n'.join(line[5:] for line in open('main.py').read().splitlines() if line.startswith('# PY ')), globals())

  test test1 (function_call, visible=None): {"function":"inspect_constraint","args":[[45,1,1,"ORD-B"]],"expected":{"declared_constraints":{"primary_key":true,"foreign_key":true,"required_quantity":true,"positive_quantity":true,"default_unique":true,"nullable_customer":true,"nullable_external":true,"distinct_null_policy":true},"accepted":true}} | on-fail: Recheck the requested edit and the supplied evidence.
  test test2 (function_call, visible=None): {"function":"inspect_constraint","args":[[null,1,1,"ORD-B"]],"expected":{"declared_constraints":{"primary_key":true,"foreign_key":true,"required_quantity":true,"positive_quantity":true,"default_unique":true,"nullable_customer":true,"nullable_external":true,"distinct_null_policy":true},"accepted":false}} | on-fail: Recheck the requested edit and the supplied evidence.
  test test3 (function_call, visible=None): {"function":"inspect_constraint","args":[[42,1,1,"ORD-B"]],"expected":{"declared_constraints":{"primary_key":true,"foreign_key":true,"required_quantity":true,"positive_quantity":true,"default_unique":true,"nullable_customer":true,"nullable_external":true,"distinct_null_policy":true},"accepted":false}} | on-fail: Recheck the requested edit and the supplied evidence.
  test test4 (function_call, visible=None): {"function":"inspect_constraint","args":[[45,99,1,"ORD-B"]],"expected":{"declared_constraints":{"primary_key":true,"foreign_key":true,"required_quantity":true,"positive_quantity":true,"default_unique":true,"nullable_customer":true,"nullable_external":true,"distinct_null_policy":true},"accepted":false}} | on-fail: Recheck the requested edit and the supplied evidence.
  test test5 (function_call, visible=None): {"function":"inspect_constraint","args":[[45,null,1,"ORD-B"]],"expected":{"declared_constraints":{"primary_key":true,"foreign_key":true,"required_quantity":true,"positive_quantity":true,"default_unique":true,"nullable_customer":true,"nullable_external":true,"distinct_null_policy":true},"accepted":true}} | on-fail: Recheck the requested edit and the supplied evidence.
  test test6 (function_call, visible=None): {"function":"inspect_constraint","args":[[45,1,null,"ORD-B"]],"expected":{"declared_constraints":{"primary_key":true,"foreign_key":true,"required_quantity":true,"positive_quantity":true,"default_unique":true,"nullable_customer":true,"nullable_external":true,"distinct_null_policy":true},"accepted":false}} | on-fail: Recheck the requested edit and the supplied evidence.
  test test7 (function_call, visible=None): {"function":"inspect_constraint","args":[[45,1,0,"ORD-B"]],"expected":{"declared_constraints":{"primary_key":true,"foreign_key":true,"required_quantity":true,"positive_quantity":true,"default_unique":true,"nullable_customer":true,"nullable_external":true,"distinct_null_policy":true},"accepted":false}} | on-fail: Recheck the requested edit and the supplied evidence.
  test test8 (function_call, visible=None): {"function":"inspect_constraint","args":[[45,1,-1,"ORD-B"]],"expected":{"declared_constraints":{"primary_key":true,"foreign_key":true,"required_quantity":true,"positive_quantity":true,"default_unique":true,"nullable_customer":true,"nullable_external":true,"distinct_null_policy":true},"accepted":false}} | on-fail: Recheck the requested edit and the supplied evidence.
  test test9 (function_call, visible=None): {"function":"inspect_constraint","args":[[45,1,1,"ORD-A"]],"expected":{"declared_constraints":{"primary_key":true,"foreign_key":true,"required_quantity":true,"positive_quantity":true,"default_unique":true,"nullable_customer":true,"nullable_external":true,"distinct_null_policy":true},"accepted":false}} | on-fail: Recheck the requested edit and the supplied evidence.
  test test10 (function_call, visible=None): {"function":"inspect_constraint","args":[[45,1,1,null]],"expected":{"declared_constraints":{"primary_key":true,"foreign_key":true,"required_quantity":true,"positive_quantity":true,"default_unique":true,"nullable_customer":true,"nullable_external":true,"distinct_null_policy":true},"accepted":true}} | on-fail: Recheck the requested edit and the supplied evidence.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"2a6f90f1ba33917279d05e1eee86cb94e963ebe6e007d3b467dc0d70036c528e","tests_passed":10}
  feedback✔: The submitted edits meet the requested practice conditions across the supplied checks.  feedback✘: Recheck the taught rule and the specific evidence. Declare a column as TYPE NOT NULL to reject nulls independently of whether a write came through an application.  hints: ['Change only the requested learner-owned lines; leave the supplied inspection or execution harness unchanged.']  remediation→r03
  MEASURES: A:identify_null_required_value_rejection(f1); A:identify_null_or_duplicate_primary_key_rejection(f3); A:identify_unmatched_non_null_reference_rejection(f4)   anchors=['practice', 'assessment:identify_null_required_value_rejection', 'assessment:identify_null_or_duplicate_primary_key_rejection', 'assessment:identify_unmatched_non_null_reference_rejection']
  taught-before-tested: A.f1←s01; A.f3←s01; A.f4←s01

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