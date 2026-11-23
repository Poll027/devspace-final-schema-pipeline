# EVALUATOR PACKET — Resource-oriented REST URLs and CRUD contracts · FastAPI application and path-operation declarations (tile_022)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = rest.resource_contract_design — Resource-oriented REST URLs and CRUD contracts
B = fastapi.path_operations — FastAPI application and path-operation declarations

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=4
  warn: remediation step tile_022.r02 is never referenced
  warn: remediation step tile_022.r04 is never referenced
  warn: remediation step tile_022.r05 is never referenced
  warn: tile_022.s04/ix.tile_022.s04: ADVISORY — syntax descriptors with no detector: ['Annotated variable assignments using str and int', 'Integer literals for HTTP response statuses']

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
[DIAGRAM] nodes=['Collection /orders', 'Item /orders/{order_id}', 'Created item /orders/42'] edges=[('n1', 'n1', 'On this item: GET retrieves; PUT replaces; DELETE removes.'), ('n0', 'n2', 'POST collection creation: can use 201 + Location'), ('n1', 'n1', 'Absent item: can use 404')] alt: Make the orders collection and identified item visible as distinct resources. Annotate GET retrieval, POST collection creation processing, PUT item replacement and DELETE item removal, with 201 and Location /orders/42 for creation and 404 for an absent item.

### s02 · explainer · Trace the boundary: Resource-oriented REST URLs and CRUD contracts
(walkthrough) Keep resource identity separate from the operation: /orders is the collection; /orders/{order_id} identifies an item. GET retrieves, POST processes collection creation, PUT replaces the target, and DELETE removes it. A creation contract can pair 201 with Location /orders/42; an absent item can use 404. Changing the method changes the semantics even when the item path stays the same. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Choose the distinction: Resource-oriented REST URLs and CRUD contracts
Check your understanding — Use the declared contract to distinguish the outcomes.
QUESTION [choice, intro, grading=client] An orders contract creates item /orders/42; a separate retrieval asks for an absent item. Which response pair fits these two cases?
  ✔ a: Creation: 201 with Location /orders/42; absent item: 404.
      why: Correct. A creation contract can use 201 with a Location identifying the created resource, while an absent item can use 404.
  ✘ b: Creation: 404; absent item: 201.
      why: This reverses creation and absence.
  ✘ c: Creation: 201 with Location /orders; absent item: 404.
      why: The Location must identify the created item, not just its collection.
  feedback✔: Correct. A creation contract can use 201 with a Location identifying the created resource, while an absent item can use 404.  feedback✘: Recheck the distinction: A creation contract can use 201 with a Location identifying the created resource, while an absent item can use 404.  hints: ['Separate resource identity, operation semantics and response metadata.']  remediation→r01
  MEASURES: A:specify_created_resource_and_absent_item_responses(f4)   anchors=['assessment:specify_created_resource_and_absent_item_responses']
  taught-before-tested: A.f4←s01

### s04 · hands_on · Practice: Resource-oriented REST URLs and CRUD contracts
Apply the contract — Work in the supplied orders-service exercise snapshot.
QUESTION [code_exercise, intro, grading=client] Guided contract representation: Complete the nine annotated contract variables: collection /orders, item /orders/{order_id}; retrieval GET, collection creation POST, replacement PUT, removal DELETE; creation 201 with Location /orders/42 and absent-item status 404. Do not implement handlers. The supplied inspector checks identity/methods and response details separately. The supplied_* variables provide the literal contract values; complete each annotated orders_* assignment by copying its matching supplied_* value. Keep the supplied literals and inspector unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['Annotated variable assignments using str and int', 'String literals for resource paths, HTTP methods and Location values', 'Integer literals for HTTP response statuses'] blocked=7 items
  file main.py [editable]:
supplied_orders_collection_path = '/orders'
supplied_orders_item_path = '/orders/{order_id}'
supplied_orders_retrieve_method = 'GET'
supplied_orders_create_method = 'POST'
supplied_orders_replace_method = 'PUT'
supplied_orders_remove_method = 'DELETE'
supplied_orders_created_location = '/orders/42'
supplied_orders_created_status = 201
supplied_orders_absent_status = 404
orders_collection_path: str = ''
orders_item_path: str = ''
orders_retrieve_method: str = ''
orders_create_method: str = ''
orders_replace_method: str = ''
orders_remove_method: str = ''
orders_created_location: str = ''
orders_created_status: int = 0
orders_absent_status: int = 0

# Supplied contract inspector.
inspect_contract = lambda section: [orders_collection_path, orders_item_path, orders_retrieve_method, orders_create_method, orders_replace_method, orders_remove_method] if section == "identity_and_methods" else [orders_created_location, orders_created_status, orders_absent_status]

  SOLUTION main.py:
supplied_orders_collection_path = '/orders'
supplied_orders_item_path = '/orders/{order_id}'
supplied_orders_retrieve_method = 'GET'
supplied_orders_create_method = 'POST'
supplied_orders_replace_method = 'PUT'
supplied_orders_remove_method = 'DELETE'
supplied_orders_created_location = '/orders/42'
supplied_orders_created_status = 201
supplied_orders_absent_status = 404
orders_collection_path: str = supplied_orders_collection_path
orders_item_path: str = supplied_orders_item_path
orders_retrieve_method: str = supplied_orders_retrieve_method
orders_create_method: str = supplied_orders_create_method
orders_replace_method: str = supplied_orders_replace_method
orders_remove_method: str = supplied_orders_remove_method
orders_created_location: str = supplied_orders_created_location
orders_created_status: int = supplied_orders_created_status
orders_absent_status: int = supplied_orders_absent_status

# Supplied contract inspector.
inspect_contract = lambda section: [orders_collection_path, orders_item_path, orders_retrieve_method, orders_create_method, orders_replace_method, orders_remove_method] if section == "identity_and_methods" else [orders_created_location, orders_created_status, orders_absent_status]

  test t1 (function_call, visible=True): {"function":"inspect_contract","args":["identity_and_methods"],"expected":["/orders","/orders/{order_id}","GET","POST","PUT","DELETE"]} | on-fail: The completed implementation does not meet this observable contract.
  test t2 (function_call, visible=True): {"function":"inspect_contract","args":["responses"],"expected":["/orders/42",201,404]} | on-fail: The completed implementation does not meet this observable contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"092da720eb48223a8502eee5c0a98b72d8e067edbf10ae8afebff98d947c0b03","tests_passed":2}
  feedback✔: Correct. A URL path identifies a resource, and an HTTP method supplies the operation semantics rather than the path alone determining the action.  feedback✘: Recheck the distinction: A URL path identifies a resource, and an HTTP method supplies the operation semantics rather than the path alone determining the action.  hints: ['Separate resource identity, operation semantics and response metadata.']
  MEASURES: A:distinguish_collection_and_item_resource_identity(f1,f2); A:map_crud_methods_to_collection_and_item_resources(f1,f2,f3); A:specify_created_resource_and_absent_item_responses(f4)   anchors=['practice', 'assessment:distinguish_collection_and_item_resource_identity', 'assessment:map_crud_methods_to_collection_and_item_resources', 'assessment:specify_created_resource_and_absent_item_responses']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f1←s01; A.f2←s01; A.f3←s01; A.f4←s01

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
(walkthrough) Trace GET /orders/current through the registration list: first identify the method-and-path operation, then check which matching route was declared first. An earlier conflicting /orders/{order_id} declaration can capture this request. Separately, compare @app.get and @app.put on the item path: each registers its own handler for a different operation, even with identical path text. ⟦B.f1 B.f2 B.f3 B:tb5 B:tb6⟧

### s08 · video · FastAPI application and path-operation declarations
[VIDEO Create the application and declare a path operation] bridge-before: Watch how the application instance, method decorator, path string and handler fit together. The creator calls this a route; Devspace identifies the method-and-path combination as a path operation. | bridge-after: The clip demonstrates GET registration. The text also covers POST, PUT and DELETE, explains different methods on the same path, and teaches fixed-before-parameterized declaration order, which the clip does not address.
  - 7AMjmCTumuo 493-608s facts=['f1'] label: Create a FastAPI instance and register a GET handler | summary: Import FastAPI and create the application instance with app = FastAPI(). The application object provides decorators for registering handlers. Applying @app.get("/") to a function registers it for GET requests at the root path. The example handler returns a dictionary containing a greeting. A brief editor detour corrects the selected Python interpreter so the import resolves.

### s09 · check · Choose the distinction: FastAPI application and path-operation declarations
Check your understanding — Use the declared contract to distinguish the outcomes.
QUESTION [choice, core, grading=client] GET /orders and POST /orders are registered to distinct handlers. How many path operations do these declarations define?
  ✔ a: Two: each method-path combination is an operation.
      why: Correct. A path operation is the combination of an HTTP method and a path; handlers registered for different methods on the same path serve different operations.
  ✘ b: One: identical paths merge the handlers.
      why: The method is part of the operation identity.
  ✘ c: Two only if the paths are renamed.
      why: Different methods already distinguish operations on one path.
  feedback✔: Correct. A path operation is the combination of an HTTP method and a path; handlers registered for different methods on the same path serve different operations.  feedback✘: Recheck the distinction: A path operation is the combination of an HTTP method and a path; handlers registered for different methods on the same path serve different operations.  hints: ['Compare the HTTP method as well as the path; for overlapping GET paths, inspect declaration order.']  remediation→r03
  MEASURES: B:distinguish_operations_sharing_a_path(f2)   anchors=['assessment:distinguish_operations_sharing_a_path']
  taught-before-tested: B.f2←s05

### s10 · check · Choose the distinction: FastAPI application and path-operation declarations
Check your understanding — Use the declared contract to distinguish the outcomes.
QUESTION [choice, core, grading=client] The following GET routes are declared in this order; order_id has no type restriction. Which handler receives GET /orders/current?
```python
@app.get("/orders/{order_id}")
def item(order_id): return "item"
@app.get("/orders/current")
def current(): return "current"
```
  ✔ a: item: the earlier parameterized route captures current.
      why: Correct. Routes are evaluated in order, so declare a fixed path before a conflicting parameterized path to prevent the latter from capturing it.
  ✘ b: current: fixed routes always take priority.
      why: Routes are evaluated in declaration order.
  ✘ c: Neither: sharing a prefix prevents registration.
      why: Overlapping routes can register; their evaluation order matters.
  feedback✔: Correct. Routes are evaluated in order, so declare a fixed path before a conflicting parameterized path to prevent the latter from capturing it.  feedback✘: Recheck the distinction: Routes are evaluated in order, so declare a fixed path before a conflicting parameterized path to prevent the latter from capturing it.  hints: ['Compare the HTTP method as well as the path; for overlapping GET paths, inspect declaration order.']
  MEASURES: B:determine_handler_from_conflicting_route_order(f3)   anchors=['assessment:determine_handler_from_conflicting_route_order']
  taught-before-tested: B.f3←s05

### s11 · hands_on · Practice: FastAPI application and path-operation declarations
Apply the contract — Work in the supplied orders-service exercise snapshot.
QUESTION [code_exercise, stretch, grading=client] Declare the five handlers in exactly this order: POST /orders, GET /orders/current, GET /orders/{order_id}, PUT /orders/{order_id}, DELETE /orders/{order_id}. Preserve the supplied handler names and static return markers. do not add handler parameters. Tests inspect all registrations and request dispatch.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': ['fastapi']} constraints.allowed=['from fastapi import FastAPI', 'app = FastAPI()', '@app.get("/orders/current")', '@app.get("/orders/{order_id}")', '@app.post("/orders")', '@app.put("/orders/{order_id}")', '@app.delete("/orders/{order_id}")', 'def handler_name():', 'return', 'Static string literals', 'Static dictionary literals'] blocked=10 items
  file main.py [editable]:
from fastapi import FastAPI
app = FastAPI()
created = "created"
current = "current"
retrieved = "retrieved"
replaced = "replaced"
removed = "removed"
def create_order(): return created
def current_order(): return current
def retrieve_order(): return retrieved
def replace_order(): return replaced
def remove_order(): return removed

# Supplied registration inspector: no request handling by the learner.
def registration(index):
    routes = [r for r in app.routes if r.path.startswith("/orders")]
    r = routes[index]
    return [r.path, sorted(r.methods), r.endpoint.__name__]

  SOLUTION main.py:
from fastapi import FastAPI
app = FastAPI()
created = "created"
current = "current"
retrieved = "retrieved"
replaced = "replaced"
removed = "removed"
@app.post("/orders")
def create_order(): return created
@app.get("/orders/current")
def current_order(): return current
@app.get("/orders/{order_id}")
def retrieve_order(): return retrieved
@app.put("/orders/{order_id}")
def replace_order(): return replaced
@app.delete("/orders/{order_id}")
def remove_order(): return removed

# Supplied registration inspector: no request handling by the learner.
def registration(index):
    routes = [r for r in app.routes if r.path.startswith("/orders")]
    r = routes[index]
    return [r.path, sorted(r.methods), r.endpoint.__name__]

  test t1 (http_equals, visible=True): {"requests":[{"method":"POST","path":"/orders"}],"expected":{"status":200,"json":"created"}} | on-fail: The completed implementation does not meet this observable contract.
  test t2 (http_equals, visible=True): {"requests":[{"method":"GET","path":"/orders/current"}],"expected":{"status":200,"json":"current"}} | on-fail: The completed implementation does not meet this observable contract.
  test t3 (http_equals, visible=True): {"requests":[{"method":"GET","path":"/orders/42"}],"expected":{"status":200,"json":"retrieved"}} | on-fail: The completed implementation does not meet this observable contract.
  test t4 (http_equals, visible=True): {"requests":[{"method":"GET","path":"/orders/7"}],"expected":{"status":200,"json":"retrieved"}} | on-fail: The completed implementation does not meet this observable contract.
  test t5 (http_equals, visible=True): {"requests":[{"method":"PUT","path":"/orders/42"}],"expected":{"status":200,"json":"replaced"}} | on-fail: The completed implementation does not meet this observable contract.
  test t6 (http_equals, visible=True): {"requests":[{"method":"PUT","path":"/orders/7"}],"expected":{"status":200,"json":"replaced"}} | on-fail: The completed implementation does not meet this observable contract.
  test t7 (http_equals, visible=True): {"requests":[{"method":"DELETE","path":"/orders/42"}],"expected":{"status":200,"json":"removed"}} | on-fail: The completed implementation does not meet this observable contract.
  test t8 (http_equals, visible=True): {"requests":[{"method":"DELETE","path":"/orders/7"}],"expected":{"status":200,"json":"removed"}} | on-fail: The completed implementation does not meet this observable contract.
  test t9 (function_call, visible=True): {"function":"registration","args":[0],"expected":["/orders",["POST"],"create_order"]} | on-fail: The completed implementation does not meet this observable contract.
  test t10 (function_call, visible=True): {"function":"registration","args":[1],"expected":["/orders/current",["GET"],"current_order"]} | on-fail: The completed implementation does not meet this observable contract.
  test t11 (function_call, visible=True): {"function":"registration","args":[2],"expected":["/orders/{order_id}",["GET"],"retrieve_order"]} | on-fail: The completed implementation does not meet this observable contract.
  test t12 (function_call, visible=True): {"function":"registration","args":[3],"expected":["/orders/{order_id}",["PUT"],"replace_order"]} | on-fail: The completed implementation does not meet this observable contract.
  test t13 (function_call, visible=True): {"function":"registration","args":[4],"expected":["/orders/{order_id}",["DELETE"],"remove_order"]} | on-fail: The completed implementation does not meet this observable contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"247990db1d599e6e18406cdd654f84f7dd4297e74a71c3df20669b65f03f275c","tests_passed":13}
  feedback✔: Correct. Create a FastAPI instance and register a handler with @app.get("/path"), @app.post("/path"), @app.put("/path") or @app.delete("/path") for the intended method and path.  feedback✘: Recheck the distinction: Create a FastAPI instance and register a handler with @app.get("/path"), @app.post("/path"), @app.put("/path") or @app.delete("/path") for the intended method and path.  hints: ['Compare the HTTP method as well as the path; for overlapping GET paths, inspect declaration order.']
  MEASURES: B:determine_handler_from_method_and_path(f1,f2)   anchors=['practice', 'assessment:determine_handler_from_method_and_path']
  taught-before-tested: B.f1←s05; B.f2←s05

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

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: FastAPI() application construction
· constraints.blocked_syntax: @app.get(), @app.post(), @app.put() and @app.delete() declarations
· constraints.blocked_syntax: APIRouter() construction
· constraints.blocked_syntax: Path(), Query() and Body() declarations
· ops.value: /orders/{order_id}_x
· expected.value: /orders/{order_id}_x
· constraints.blocked_syntax: Handler parameters for path or query input binding
· constraints.blocked_syntax: app.include_router(...)

=========

# EVALUATOR PACKET — Validated environment-based configuration with fail-fast startup (tile_024)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.validated_environment_configuration — Validated environment-based configuration with fail-fast startup

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: remediation step tile_024.r02 is never referenced

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

# environment_only → app_name='synthetic-environment-orders'
# conflicting_sources → app_name='synthetic-environment-orders'
# absent_from_both → Settings() raises ValidationError.

  annotations: ['Declare required typed fields on a BaseSettings subclass, then construct Settings(). Compare valid, missing, and invalid external values: missing required settings and invalid values fail validation. Configure a dotenv file with SettingsConfigDict(env_file=".env"). If both sources supply a key, the environment takes precedence; priority does not remove type validation.']

### s02 · explainer · Trace the boundary: Validated environment-based configuration with fail-fast startup
(walkthrough) Declare required typed fields on a BaseSettings subclass, then construct Settings(). Compare valid, missing, and invalid external values: missing required settings and invalid values fail validation. Configure a dotenv file with SettingsConfigDict(env_file=".env"). If both sources supply a key, the environment takes precedence; priority does not remove type validation. ⟦A.f1 A.f2 A.f3 A:tb4⟧

### s03 · explainer · Trace the boundary: Validated environment-based configuration with fail-fast startup
(walkthrough) Use the source cases to review the Settings declaration. app_name is a required typed field on the BaseSettings subclass; SettingsConfigDict(env_file=".env") enables the dotenv source. In conflicting_sources, inspect the environment value before the dotenv value because the environment takes precedence. In absent_from_both, the required field has no supplied value, so Settings() fails validation. Source priority chooses a value; construction still validates its declared type. ⟦A.f1 A.f2 A.f3 A:tb5 A:tb6⟧

### s04 · video · Validated environment-based configuration with fail-fast startup
[VIDEO Typed settings and environment-supplied values] bridge-before: Watch how the typed app_name declaration becomes a constructed settings object. The clip uses a default; the text also teaches required settings without defaults. | bridge-after: The clip demonstrates environment loading, but not missing-required or invalid-value failures, dotenv configuration, or dotenv precedence. The text covers those rules so configuration can be validated before serving.
  - FcWdzqCpj5c 125-327s facts=['f1'] label: Declare typed settings and replace a default through the environment | summary: A configuration module defines Settings by importing BaseSettings from pydantic_settings and subclassing it. The class declares app_name as a string with a default. Constructing Settings creates an object whose fields can be accessed by the application. The example first uses the default name, then supplies APP_NAME in the environment for a command. The resulting settings object uses that environment value instead of the default.

### s05 · check · Choose the distinction: Validated environment-based configuration with fail-fast startup
Check your understanding — Use the declared contract to distinguish the outcomes.
QUESTION [choice, intro, grading=client] APP_NAME is an environment variable containing "environment-orders". The configured .env contains APP_NAME=dotenv-orders. With no initializer override, what should validated settings use?
  ✔ a: environment-orders, because environment values take precedence.
      why: Environment variables take precedence over configured .env values. Here APP_NAME therefore supplies environment-orders; differing source values do not themselves cause validation failure.
  ✘ b: dotenv-orders, because the file was configured explicitly.
      why: Configuring a dotenv file does not give it priority over environment variables.
  ✘ c: Construction must fail whenever the two sources differ.
      why: A conflicting source is resolved by precedence, not automatically a validation failure.
  feedback✔: Correct. Environment variables take precedence over configured .env values, so app_name uses environment-orders.  feedback✘: Environment variables take precedence over configured .env values. Here APP_NAME therefore supplies environment-orders; differing source values do not themselves cause validation failure.  hints: ['Check source precedence separately from whether a required field has a usable value.']  remediation→r01
  MEASURES: A:determine_effective_settings_source_and_validation_outcome(f2,f3)   anchors=['assessment:determine_effective_settings_source_and_validation_outcome']
  taught-before-tested: A.f2←s01; A.f3←s01

### s06 · hands_on · Practice: Validated environment-based configuration with fail-fast startup
Apply the contract — Work in the supplied orders-service exercise snapshot.
QUESTION [code_exercise, stretch, grading=client] Complete Settings as a BaseSettings subclass with required app_name: str and model_config = SettingsConfigDict(env_file='.env'). Keep the supplied construction harness unchanged. The supplied sandbox adapter uses Pydantic’s bundled v1 BaseSettings because pydantic_settings is unavailable here; leave the adapter unchanged. It supports the model_config/env_file spelling for these controlled APP_NAME fixtures, not the full pydantic_settings API.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': ['pydantic']} constraints.allowed=['from pydantic_settings import BaseSettings, SettingsConfigDict', 'class Settings(BaseSettings):', 'app_name: str', 'model_config = SettingsConfigDict(env_file=".env")', 'settings = Settings()', 'settings.app_name', 'string literals'] blocked=6 items
  file main.py [editable]:
# Supplied sandbox compatibility scaffold: pydantic_settings is not installed.
# Use Pydantic's bundled v1 BaseSettings with a controlled dotenv source.
# This adapter supports the model_config/env_file spelling used in this exercise;
# it is not the full pydantic_settings package. Leave this scaffold unchanged.
from pydantic.v1 import BaseSettings as _BaseSettings, ValidationError
from typing import ClassVar
import shlex

SettingsConfigDict = dict

class BaseSettings(_BaseSettings):
    model_config: ClassVar[dict] = {}

    class Config:
        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            def dotenv_settings(settings):
                filename = settings.model_config.get("env_file")
                if not filename or not Path(filename).exists():
                    return {}
                entries = {}
                for line in Path(filename).read_text(encoding="utf-8").splitlines():
                    if "=" in line:
                        name, raw = line.split("=", 1)
                        tokens = shlex.split(raw)
                        entries[name.strip().upper()] = tokens[0] if tokens else ""
                return {name: entries[name.upper()] for name in settings.__fields__
                        if name.upper() in entries}
            return init_settings, env_settings, dotenv_settings, file_secret_settings
import os
from pathlib import Path
from tempfile import TemporaryDirectory

class Settings(BaseSettings):
    # TODO: declare the required field and configure .env loading.
    pass

# Supplied construction harness: actual .env files in isolated workspace fixtures.
# Each call restores the working directory and environment, even after failure.
def construct_case(environment, dotenv):
    previous_directory = os.getcwd()
    previous_environment = dict(os.environ)
    try:
        os.environ.clear()
        if environment is not None:
            os.environ["APP_NAME"] = environment
        with TemporaryDirectory(dir=previous_directory) as fixture_directory:
            try:
                os.chdir(fixture_directory)
                if dotenv is not None:
                    Path(".env").write_text("APP_NAME=" + "\'" + dotenv.replace("\\", "\\\\").replace("\'", "\\\'") + "\'" + "\n", encoding="utf-8")
                try:
                    settings = Settings()
                    return {"accepted": True, "app_name": settings.app_name}
                except ValidationError:
                    return {"accepted": False}
            finally:
                os.chdir(previous_directory)
    finally:
        os.environ.clear()
        os.environ.update(previous_environment)

  SOLUTION main.py:
# Supplied sandbox compatibility scaffold: pydantic_settings is not installed.
# Use Pydantic's bundled v1 BaseSettings with a controlled dotenv source.
# This adapter supports the model_config/env_file spelling used in this exercise;
# it is not the full pydantic_settings package. Leave this scaffold unchanged.
from pydantic.v1 import BaseSettings as _BaseSettings, ValidationError
from typing import ClassVar
import shlex

SettingsConfigDict = dict

class BaseSettings(_BaseSettings):
    model_config: ClassVar[dict] = {}

    class Config:
        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            def dotenv_settings(settings):
                filename = settings.model_config.get("env_file")
                if not filename or not Path(filename).exists():
                    return {}
                entries = {}
                for line in Path(filename).read_text(encoding="utf-8").splitlines():
                    if "=" in line:
                        name, raw = line.split("=", 1)
                        tokens = shlex.split(raw)
                        entries[name.strip().upper()] = tokens[0] if tokens else ""
                return {name: entries[name.upper()] for name in settings.__fields__
                        if name.upper() in entries}
            return init_settings, env_settings, dotenv_settings, file_secret_settings
import os
from pathlib import Path
from tempfile import TemporaryDirectory

class Settings(BaseSettings):
    app_name: str
    model_config = SettingsConfigDict(env_file='.env')

# Supplied construction harness: actual .env files in isolated workspace fixtures.
# Each call restores the working directory and environment, even after failure.
def construct_case(environment, dotenv):
    previous_directory = os.getcwd()
    previous_environment = dict(os.environ)
    try:
        os.environ.clear()
        if environment is not None:
            os.environ["APP_NAME"] = environment
        with TemporaryDirectory(dir=previous_directory) as fixture_directory:
            try:
                os.chdir(fixture_directory)
                if dotenv is not None:
                    Path(".env").write_text("APP_NAME=" + "\'" + dotenv.replace("\\", "\\\\").replace("\'", "\\\'") + "\'" + "\n", encoding="utf-8")
                try:
                    settings = Settings()
                    return {"accepted": True, "app_name": settings.app_name}
                except ValidationError:
                    return {"accepted": False}
            finally:
                os.chdir(previous_directory)
    finally:
        os.environ.clear()
        os.environ.update(previous_environment)

  test t1 (function_call, visible=True): {"function":"construct_case","args":["synthetic-environment-orders",null],"expected":{"accepted":true,"app_name":"synthetic-environment-orders"}} | on-fail: The completed implementation does not meet this observable contract.
  test t2 (function_call, visible=True): {"function":"construct_case","args":["synthetic-environment-orders","synthetic-dotenv-orders"],"expected":{"accepted":true,"app_name":"synthetic-environment-orders"}} | on-fail: The completed implementation does not meet this observable contract.
  test t4 (function_call, visible=True): {"function":"construct_case","args":[null,"synthetic-dotenv-orders"],"expected":{"accepted":true,"app_name":"synthetic-dotenv-orders"}} | on-fail: The completed implementation does not meet this observable contract.
  test t3 (function_call, visible=True): {"function":"construct_case","args":[null,null],"expected":{"accepted":false}} | on-fail: The completed implementation does not meet this observable contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"d6791ba20e83028f0088d047a309fd84a529baa243fa2b0ff70f1a155e58f6f8","tests_passed":4}
  feedback✔: Correct. Subclass BaseSettings from pydantic_settings and declare typed fields to load and validate external configuration.  feedback✘: Recheck the distinction: Subclass BaseSettings from pydantic_settings and declare typed fields to load and validate external configuration.  hints: ['Check source precedence separately from whether a required field has a usable value.']
  MEASURES: A:identify_settings_construction_failures_before_serving(f1,f2)   anchors=['practice', 'assessment:identify_settings_construction_failures_before_serving']
  taught-before-tested: A.f1←s01; A.f2←s01

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

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: remediation step tile_025.r02 is never referenced

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
(walkthrough) Compare orders() with separate_clients() in the shipping-lookup example. In orders(), the loop sits inside one async with httpx.AsyncClient() scope, so each awaited client.get(url) reuses that client and can benefit from connection pooling. In separate_clients(), client construction sits inside the loop instead. For either layout, distinguish awaiting the request from closing the client: cleanup belongs at the end of the owning scope, through context-manager exit or await client.aclose(). ⟦A.f1 A.f2 A.f3 A:tb5 A:tb6⟧

### s04 · video · Async-compatible external HTTP requests
[VIDEO Own, reuse, and close an asynchronous HTTP client] bridge-before: Watch how one client serves repeated requests before the example moves to AsyncClient. The reuse loop uses the synchronous client; our target is the asynchronous context-managed pattern introduced afterward. | bridge-after: The clip establishes pooling and async-with requests. The text makes scope-end cleanup explicit, supplies await client.aclose() as an alternative, and explains why completing a request does not close its client.
  - qAh5dDODJ5k 235-368s facts=['f1', 'f2', 'f3'] label: Connection pooling first, then AsyncClient and awaited requests | summary: An HTTPX client owns pooled connections that can be reused across requests. The example first uses a synchronous context-managed client for repeated calls and shared headers. It then introduces the asynchronous equivalent: enter async with httpx.AsyncClient() as client and await client.get(...) or client.post(...) to receive a response. The asynchronous call is placed inside an async function and executed. The reuse loop is demonstrated with the synchronous client; the asynchronous example establishes the corresponding context-managed request pattern.

### s05 · check · Choose the distinction: Async-compatible external HTTP requests
Check your understanding — Use the declared contract to distinguish the outcomes.
QUESTION [choice, intro, grading=client] Two sequential shipping lookups belong to one owning scope. Which client placement preserves reuse and cleanup?
  ✔ a: Open one async client scope, await both requests inside it, then leave the scope.
      why: Correct. Use httpx.AsyncClient and await client.get(...), client.post(...) or another request method for an asynchronous outbound call.
  ✘ b: Open and close a different client for each lookup.
      why: That loses reuse across these lookups.
  ✘ c: Exit the client scope after lookup one, then use it for lookup two.
      why: The owning scope must finish using the client before cleanup.
  feedback✔: Correct. Both awaited lookups reuse one AsyncClient, and leaving its owning scope closes it only after its last use.  feedback✘: Recheck the distinction: Use httpx.AsyncClient and await client.get(...), client.post(...) or another request method for an asynchronous outbound call.  hints: ['Trace the client’s owning scope from construction through its last use and cleanup.']  remediation→r01
  MEASURES: A:identify_async_client_lifetime_mistakes(f1,f2,f3)   anchors=['assessment:identify_async_client_lifetime_mistakes']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s06 · hands_on · Practice: Async-compatible external HTTP requests
Apply the contract — Work in the supplied orders-service exercise snapshot.
QUESTION [code_exercise, stretch, grading=client] Complete orders(): create one AsyncClient owning scope, await the lookup_one and lookup_two requests sequentially on that same client, then close it after both uses. Leave the supplied MockTransport/invocation bridge unchanged: it records real awaited requests without any network access. /fixture must report one opening, both requests in order, then closure. The supplied httpx facade constructs real HTTPX clients with the synthetic transport; it does not replace the server bridge client.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': ['httpx', 'fastapi']} constraints.allowed=['import httpx', 'async def', 'assignment', 'string literals', 'return', 'async with httpx.AsyncClient() as client', 'httpx.AsyncClient()', 'await client.get(...)', 'await client.post(...)', 'await client.aclose()', 'try/finally'] blocked=9 items
  file main.py [editable]:
import httpx as _httpx
from fastapi import FastAPI
app = FastAPI()
lookup_one = "https://shipping.example.test/orders/42"
lookup_two = "https://shipping.example.test/orders/43"
events = []
_RealClient = _httpx.AsyncClient
class SuppliedClient(_RealClient):
    def __init__(self, **kwargs):
        self.fixture_owned = not kwargs
        if kwargs:
            super().__init__(**kwargs)
            return
        async def respond(request):
            events.append(["request", str(request.url)])
            return _httpx.Response(200, json={"status": "supplied"})
        super().__init__(transport=_httpx.MockTransport(respond))
        events.append(["opened"])
    async def aclose(self):
        if self.fixture_owned: events.append(["closed"])
        await super().aclose()
    async def __aexit__(self, *args):
        if self.fixture_owned: events.append(["closed"])
        return await super().__aexit__(*args)
from types import SimpleNamespace
httpx = SimpleNamespace(AsyncClient=SuppliedClient)
async def orders():
    pass

# Supplied invocation bridge; no endpoint wiring is required from the learner.
class SuppliedBridge:
    async def run_fixture():
        events.clear()
        await orders()
        return list(events)
app.add_api_route("/fixture", SuppliedBridge.run_fixture, methods=["GET"])

  SOLUTION main.py:
import httpx as _httpx
from fastapi import FastAPI
app = FastAPI()
lookup_one = "https://shipping.example.test/orders/42"
lookup_two = "https://shipping.example.test/orders/43"
events = []
_RealClient = _httpx.AsyncClient
class SuppliedClient(_RealClient):
    def __init__(self, **kwargs):
        self.fixture_owned = not kwargs
        if kwargs:
            super().__init__(**kwargs)
            return
        async def respond(request):
            events.append(["request", str(request.url)])
            return _httpx.Response(200, json={"status": "supplied"})
        super().__init__(transport=_httpx.MockTransport(respond))
        events.append(["opened"])
    async def aclose(self):
        if self.fixture_owned: events.append(["closed"])
        await super().aclose()
    async def __aexit__(self, *args):
        if self.fixture_owned: events.append(["closed"])
        return await super().__aexit__(*args)
from types import SimpleNamespace
httpx = SimpleNamespace(AsyncClient=SuppliedClient)
async def orders():
    async with httpx.AsyncClient() as client:
        await client.get(lookup_one)
        await client.get(lookup_two)

# Supplied invocation bridge; no endpoint wiring is required from the learner.
class SuppliedBridge:
    async def run_fixture():
        events.clear()
        await orders()
        return list(events)
app.add_api_route("/fixture", SuppliedBridge.run_fixture, methods=["GET"])

  test t1 (http_equals, visible=True): {"requests":[{"method":"GET","path":"/fixture"}],"expected":{"status":200,"json":[["opened"],["request","https://shipping.example.test/orders/42"],["request","https://shipping.example.test/orders/43"],["closed"]]}} | on-fail: The completed implementation does not meet this observable contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"0e259a680bd97aba90b920a321a31bccf023446f9ce36b682a276dad36904958","tests_passed":1}
  feedback✔: Correct. Use httpx.AsyncClient and await client.get(...), client.post(...) or another request method for an asynchronous outbound call.  feedback✘: Recheck the distinction: Use httpx.AsyncClient and await client.get(...), client.post(...) or another request method for an asynchronous outbound call.  hints: ['Trace the client’s owning scope from construction through its last use and cleanup.']
  MEASURES: A:identify_async_client_lifetime_mistakes(f1,f2,f3)   anchors=['practice', 'assessment:identify_async_client_lifetime_mistakes']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

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

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: raise HTTPException(...)
· constraints.blocked_syntax: @field_validator(...)
· constraints.blocked_syntax: @model_validator(...)
· constraints.blocked_syntax: BackgroundTasks(...)
· ops.value: https://shipping.example.test/orders/42_x
· value.json: https://shipping.example.test/orders/42_x
· ops.value: https://shipping.example.test/orders/43_x
· value.json: https://shipping.example.test/orders/43_x

=========

# EVALUATOR PACKET — Custom validation for domain invariants · Expected API failures with HTTPException (tile_026)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = pydantic.domain_validation — Custom validation for domain invariants
B = fastapi.expected_http_errors — Expected API failures with HTTPException

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=4
  warn: remediation step tile_026.r02 is never referenced
  warn: remediation step tile_026.r03 is never referenced
  warn: remediation step tile_026.r05 is never referenced
  warn: remediation step tile_026.r06 is never referenced

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
[VIDEO Checking relationships after field validation] bridge-before: Watch how the validator receives the whole instance after individual field validation. The clip checks password confirmation using a mismatched pair; our booking example applies the same cross-field principle. | bridge-after: The clip demonstrates a mismatch failure. The text also covers returning self on success, the complete single-field validator pattern, and verifying both rejection of individually valid but inconsistent inputs and acceptance of consistent inputs.
  - M81pfi64eeM 3409-3542s facts=['f1'] label: Check a password-confirmation invariant after field validation | summary: A registration model contains email, password and confirmation fields. A model validator compares the two password fields after individual field validation. It receives self, giving it access to the model instance rather than just one value, and does not use the classmethod decorator used for field validators. Constructing the model with two different password strings produces a validation error reporting that the passwords do not match.

### s04 · check · Choose the distinction: Custom validation for domain invariants
Check your understanding — Use the declared contract to distinguish the outcomes.
QUESTION [choice, intro, grading=client] Booking has individually valid integer start and end fields. Which rule requires their relationship to be checked together?
  ✔ a: end must be later than start.
      why: Correct. Use @model_validator(mode='after') on an instance method to check an invariant involving multiple already-validated fields.
  ✘ b: start must be an integer.
      why: This concerns one field rather than the relationship.
  ✘ c: end must be an integer.
      why: This also concerns one field rather than comparing both values.
  feedback✔: Correct. Use @model_validator(mode='after') on an instance method to check an invariant involving multiple already-validated fields.  feedback✘: Recheck the distinction: Use @model_validator(mode='after') on an instance method to check an invariant involving multiple already-validated fields.  hints: ['Ask whether a failure belongs to one field or to the relationship between validated fields.']  remediation→r01
  MEASURES: A:distinguish_cross_field_invariants_from_single_field_checks(f1,f3)   anchors=['assessment:distinguish_cross_field_invariants_from_single_field_checks']
  taught-before-tested: A.f1←s01; A.f3←s01

### s05 · check · Choose the distinction: Custom validation for domain invariants
Check your understanding — Use the declared contract to distinguish the outcomes.
QUESTION [choice, core, grading=client] Which supplied pair isolates a failure of end > start while keeping both inputs individually valid integers?
  ✔ a: start=5, end=3.
      why: Correct. Verify a cross-field rule with input that passes each individual field's validation but violates the model invariant, asserting that model construction raises ValidationError; also verify a consistent input is accepted.
  ✘ b: start=3, end=5.
      why: This pair satisfies end > start.
  ✘ c: start="not-an-integer", end=5.
      why: This introduces a single-field type failure instead of isolating the invariant.
  feedback✔: Correct. Verify a cross-field rule with input that passes each individual field's validation but violates the model invariant, asserting that model construction raises ValidationError; also verify a consistent input is accepted.  feedback✘: Recheck the distinction: Verify a cross-field rule with input that passes each individual field's validation but violates the model invariant, asserting that model construction raises ValidationError; also verify a consistent input is accepted.  hints: ['Ask whether a failure belongs to one field or to the relationship between validated fields.']
  MEASURES: A:identify_inputs_that_isolate_cross_field_validity(f4)   anchors=['assessment:identify_inputs_that_isolate_cross_field_validity']
  taught-before-tested: A.f4←s01

### s06 · hands_on · Practice: Custom validation for domain invariants
Apply the contract — Work in the supplied orders-service exercise snapshot.
QUESTION [code_exercise, stretch, grading=client] Add Booking.validate_order as an after-model instance validator. Require end > start, raise ValueError on failure, and return self on success. Constructor checks include (5,3), (3,3), (3,5) and (2,7); reject the first two and preserve the accepted integer fields.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': ['pydantic']} constraints.allowed=['from pydantic import BaseModel, model_validator, ValidationError', 'class Booking(BaseModel):', 'start: int', 'end: int', "@model_validator(mode='after')", 'def validate_order(self):', 'self.start', 'self.end', 'if', '<=', 'raise ValueError(...)', 'return self', 'integer literals', 'string literals', 'Booking(start=..., end=...)'] blocked=6 items
  file main.py [editable]:
from pydantic import BaseModel, model_validator, ValidationError

class Booking(BaseModel):
    start: int
    end: int
    # TODO: add an after-model invariant validator.

# Supplied constructor inspector returns validation outcome and accepted field values.
def booking_case(start, end):
    try:
        b = Booking(start=start, end=end)
        return {"accepted": True, "start": b.start, "end": b.end}
    except ValidationError:
        return {"accepted": False}

  SOLUTION main.py:
from pydantic import BaseModel, model_validator, ValidationError

class Booking(BaseModel):
    start: int
    end: int
    # TODO: add an after-model invariant validator.
    @model_validator(mode="after")
    def validate_order(self):
        if self.end <= self.start:
            raise ValueError("end must be later than start")
        return self

# Supplied constructor inspector returns validation outcome and accepted field values.
def booking_case(start, end):
    try:
        b = Booking(start=start, end=end)
        return {"accepted": True, "start": b.start, "end": b.end}
    except ValidationError:
        return {"accepted": False}

  test t1 (function_call, visible=True): {"function":"booking_case","args":[5,3],"expected":{"accepted":false}} | on-fail: The completed implementation does not meet this observable contract.
  test t2 (function_call, visible=True): {"function":"booking_case","args":[3,3],"expected":{"accepted":false}} | on-fail: The completed implementation does not meet this observable contract.
  test t3 (function_call, visible=True): {"function":"booking_case","args":[3,5],"expected":{"accepted":true,"start":3,"end":5}} | on-fail: The completed implementation does not meet this observable contract.
  test t4 (function_call, visible=True): {"function":"booking_case","args":[2,7],"expected":{"accepted":true,"start":2,"end":7}} | on-fail: The completed implementation does not meet this observable contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"d0ad6a2cb4a6cf6ba412423b4c25b91e597526063cfbfcfab3bd43e370a75906","tests_passed":4}
  feedback✔: Correct. Use @model_validator(mode='after') on an instance method to check an invariant involving multiple already-validated fields.  feedback✘: Recheck the distinction: Use @model_validator(mode='after') on an instance method to check an invariant involving multiple already-validated fields.  hints: ['Ask whether a failure belongs to one field or to the relationship between validated fields.']
  MEASURES: A:identify_after_model_invariant_validation_requirements(f1,f2)   anchors=['practice', 'assessment:identify_after_model_invariant_validation_requirements']
  taught-before-tested: A.f1←s01; A.f2←s01

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
QUESTION [choice, core, grading=client] An absent-order branch must reject deliberately and stop before the normal return. Which form does that?
  ✔ a: raise HTTPException(status_code=404, detail="Order not found")
      why: Correct. Raise HTTPException(status_code=..., detail=...) to stop the operation and return a deliberate HTTP rejection rather than returning the exception object.
  ✘ b: return HTTPException(status_code=404, detail="Order not found")
      why: Returning an exception is not raising a deliberate rejection.
  ✘ c: Construct HTTPException, then continue to the normal return.
      why: Construction alone does not stop control flow.
  feedback✔: Correct. Raise HTTPException(status_code=..., detail=...) to stop the operation and return a deliberate HTTP rejection rather than returning the exception object.  feedback✘: Recheck the distinction: Raise HTTPException(status_code=..., detail=...) to stop the operation and return a deliberate HTTP rejection rather than returning the exception object.  hints: ['Distinguish constructing an exception, raising it, and returning a normal value.']  remediation→r04
  MEASURES: B:determine_deliberate_rejection_control_flow(f1)   anchors=['assessment:determine_deliberate_rejection_control_flow']
  taught-before-tested: B.f1←s07

### s10 · check · Choose the distinction: Expected API failures with HTTPException
Check your understanding — Use the declared contract to distinguish the outcomes.
QUESTION [choice, core, grading=client] A deliberate HTTP rejection requires a client-facing header X-Reason: absent. Where should the rejection attach it?
  ✔ a: HTTPException(..., headers={"X-Reason": "absent"})
      why: Correct. HTTPException accepts headers for required response metadata, such as an authentication challenge.
  ✘ b: Only inside the detail text.
      why: Text in detail is not a response header.
  ✘ c: Nowhere: deliberate rejections cannot carry headers.
      why: HTTPException supports headers for the rejection.
  feedback✔: Correct. HTTPException accepts headers for required response metadata, such as an authentication challenge.  feedback✘: Recheck the distinction: HTTPException accepts headers for required response metadata, such as an authentication challenge.  hints: ['Distinguish constructing an exception, raising it, and returning a normal value.']
  MEASURES: B:identify_required_rejection_headers(f2)   anchors=['assessment:identify_required_rejection_headers']
  taught-before-tested: B.f2←s07

### s11 · hands_on · Practice: Expected API failures with HTTPException
Apply the contract — Work in the supplied orders-service exercise snapshot.
QUESTION [code_exercise, stretch, grading=client] Complete the absent-order branch with a raised HTTPException: status 404 and the supplied missing_detail. Do not return the exception or proceed to the normal return in that branch. The /order rejection must carry {"detail": missing_detail}.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': ['fastapi']} constraints.allowed=['from fastapi import FastAPI, HTTPException', 'app = FastAPI()', '@app.get("/order")', 'def', 'if order is None:', 'raise HTTPException(status_code=404, detail="Order not found")', 'HTTPException headers keyword with a string-to-string dictionary', 'return', 'variable assignment', 'None', 'string and integer literals', 'dictionary literals'] blocked=12 items
  file main.py [editable]:
from fastapi import FastAPI, HTTPException
app = FastAPI()
order = None
missing_detail = "Order not found"
@app.get("/order")
def get_order():
    if order is None:
        pass
    return order

  SOLUTION main.py:
from fastapi import FastAPI, HTTPException
app = FastAPI()
order = None
missing_detail = "Order not found"
@app.get("/order")
def get_order():
    if order is None:
        raise HTTPException(status_code=404, detail=missing_detail)
    return order

  test t1 (http_equals, visible=True): {"requests":[{"method":"GET","path":"/order"}],"expected":{"status":404,"json":{"detail":"Order not found"}}} | on-fail: The completed implementation does not meet this observable contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"d7a4ae7cf22a553bba48b81846c8af8a10ffbe59527ccb7d17c53d5f9349863d","tests_passed":1}
  feedback✔: Correct. FastAPI's default HTTPException response contains the supplied detail under the JSON key detail.  feedback✘: Recheck the distinction: FastAPI's default HTTPException response contains the supplied detail under the JSON key detail.  hints: ['Distinguish constructing an exception, raising it, and returning a normal value.']
  MEASURES: B:determine_default_rejection_body(f3)   anchors=['practice', 'assessment:determine_default_rejection_body']
  taught-before-tested: B.f3←s07

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

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: model_dump(exclude_unset=True)
· constraints.blocked_syntax: @app.exception_handler

=========

# EVALUATOR PACKET — Choosing def versus async def from I/O behavior without blocking the event loop (tile_028)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.handler_execution_choice — Choosing def versus async def from I/O behavior without blocking the event loop

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: remediation step tile_028.r02 is never referenced

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
[VIDEO Handler execution and the event-loop boundary] bridge-before: Watch for the execution boundary of each handler. Interpret the clip’s instruction to await I/O as applying to awaitable operations; adding await does not make a blocking library asynchronous. | bridge-after: The clip distinguishes handler execution modes but does not teach library-based selection or ordinary-helper dispatch. The text covers both: choose by I/O behavior, and trace directly called helpers within the handler’s execution boundary.
  - 2JPDt-Jp6fM 193-254s facts=['f2'] label: How FastAPI executes def and async def handlers | summary: FastAPI automatically runs a normal def path operation in a separate thread pool, allowing the main event loop to continue processing other requests. An async def path operation runs on the event loop itself, where blocking I/O can stop other work from progressing. A normal def handler is therefore a valid execution choice, not inherently a wrong or slow one.

### s04 · check · Choose the distinction: Choosing def versus async def from I/O behavior without blocking the event loop
Check your understanding — Use the declared contract to distinguish the outcomes.
QUESTION [choice, intro, grading=client] In native FastAPI, a registered normal `def` handler directly calls a blocking normal utility. A registered `async def` handler also directly calls that utility. Which execution trace is correct?
  ✔ a: Normal handler and its direct utility: external thread pool. Async handler and its direct utility: event loop; the blocking utility can block it.
      why: The normal def handler runs in FastAPI’s external thread pool, and its direct utility runs there with it. The async def handler and its direct utility run on the event loop; the blocking utility can block it.
  ✘ b: Both utilities are automatically offloaded
      why: FastAPI does not automatically offload directly called utilities. The utility called by the async def handler stays on the event loop; only the normal def handler and its direct utility run in the external thread pool.
  ✘ c: Both handlers execute on the event loop.
      why: The registered normal def handler runs in FastAPI’s external thread pool, not on the event loop, and its direct utility runs there with it. The async def handler and its direct utility run on the event loop.
  feedback✔: The normal def handler runs in FastAPI’s external thread pool, and its direct utility runs there with it. The async def handler and its direct utility run on the event loop; the blocking utility can block it.  feedback✘: Trace the registered handler first: normal def uses the external thread pool, whereas async def uses the event loop. A directly called utility stays within its caller’s execution boundary.  hints: ['Trace the registered handler’s execution boundary before tracing its direct utility call.']  remediation→r01
  MEASURES: A:identify_blocking_io_inside_async_execution(f2,f3)   anchors=['assessment:identify_blocking_io_inside_async_execution', 'practice']
  taught-before-tested: A.f2←s01; A.f3←s01

### s05 · hands_on · Practice: Choosing def versus async def from I/O behavior without blocking the event loop
Apply the contract — Work in the supplied orders-service exercise snapshot.
QUESTION [code_exercise, stretch, grading=client] Change shipping to normal def for the supplied blocking-library call and return shipping_utility() without await. Complete the normal-def implementation here; the preceding check verifies its native execution placement. This sandbox checks declarations and results, not native thread placement.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': ['fastapi']} constraints.allowed=['def function declarations', 'async def function declarations', 'await expressions for awaitable operations only', 'return statements', 'function calls', 'attribute access and method calls', 'local variable assignment', 'existing @app.get route decorator'] blocked=5 items
  file main.py [editable]:
from fastapi import FastAPI
import inspect
app = FastAPI()
shipping_result = "synthetic-shipping-result"
class SuppliedBlockingClient:
    # Native-library stand-in: this snapshot returns immediately; no timing inference.
    def lookup(self): return {"status": shipping_result}
shipping_client = SuppliedBlockingClient()
def shipping_utility(): return shipping_client.lookup()
@app.get("/shipping")
async def shipping():
    return shipping_utility()

# Supplied declaration inspector; native thread placement is not measured here.
def inspect_shipping(view):
    if view == "declaration":
        return {"async": inspect.iscoroutinefunction(shipping)}
    return {"async": inspect.iscoroutinefunction(shipping_utility), "result": shipping_utility()}

  SOLUTION main.py:
from fastapi import FastAPI
import inspect
app = FastAPI()
shipping_result = "synthetic-shipping-result"
class SuppliedBlockingClient:
    # Native-library stand-in: this snapshot returns immediately; no timing inference.
    def lookup(self): return {"status": shipping_result}
shipping_client = SuppliedBlockingClient()
def shipping_utility(): return shipping_client.lookup()
@app.get("/shipping")
def shipping():
    return shipping_utility()

# Supplied declaration inspector; native thread placement is not measured here.
def inspect_shipping(view):
    if view == "declaration":
        return {"async": inspect.iscoroutinefunction(shipping)}
    return {"async": inspect.iscoroutinefunction(shipping_utility), "result": shipping_utility()}

  test t1 (http_equals, visible=True): {"requests":[{"method":"GET","path":"/shipping"}],"expected":{"status":200,"json":{"status":"synthetic-shipping-result"}}} | on-fail: The completed implementation does not meet this observable contract.
  test t2 (function_call, visible=True): {"function":"inspect_shipping","args":["declaration"],"expected":{"async":false}} | on-fail: The completed implementation does not meet this observable contract.
  test t3 (function_call, visible=True): {"function":"inspect_shipping","args":["utility"],"expected":{"async":false,"result":{"status":"synthetic-shipping-result"}}} | on-fail: The completed implementation does not meet this observable contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"d69ccdec4cc6731380514b9e9ec75be979869dd847c1c66d7636efde48e5332d","tests_passed":3}
  feedback✔: Correct. Use async def and await for an I/O library with awaitable operations; use a normal def handler for a blocking I/O library.  feedback✘: Recheck the distinction: Use async def and await for an I/O library with awaitable operations; use a normal def handler for a blocking I/O library.  hints: ['Inspect what the library call actually does, not just the handler’s spelling.']
  MEASURES: A:select_handler_execution_for_library_io(f1,f2); A:identify_blocking_io_inside_async_execution(f2,f3)   anchors=['practice', 'assessment:select_handler_execution_for_library_io', 'assessment:identify_blocking_io_inside_async_execution']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f2←s01; A.f3←s01

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

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: BackgroundTasks(...)
· constraints.blocked_syntax: response_model= route arguments

=========

# EVALUATOR PACKET — Modular FastAPI application composition with APIRouter (tile_029)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.modular_application — Modular FastAPI application composition with APIRouter

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: remediation step tile_029.r02 is never referenced

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
[VIDEO Feature registration and application assembly] bridge-before: Watch for the distinction between registering operations on APIRouter and including that router in the application. The other-framework analogy is optional; focus on the FastAPI declarations. | bridge-after: The clip names prefixes and tags but does not explain path concatenation or inclusion-level dependencies and responses. The text supplies these details, including how /api and /orders become /api/orders.
  - NkgIHa6KtHg 67-145s facts=['f1', 'f2'] label: Register feature operations on APIRouter and include them in the application | summary: APIRouter organizes related operations in separate modules. Create a router in a feature module, then register operations with router.get or router.post instead of app.get or app.post. The main module includes the router with app.include_router. Moving existing operations into feature modules can preserve their external URLs and behavior while improving internal organization. Inclusion also supports common prefixes and tags.

### s04 · check · Choose the distinction: Modular FastAPI application composition with APIRouter
Check your understanding — Use the declared contract to distinguish the outcomes.
QUESTION [choice, intro, grading=client] orders.py registers GET /orders on an APIRouter, but main.py never includes that router. What is missing for the main application to expose the feature?
  ✔ a: Import and include the feature router on the application.
      why: Correct. Import feature routers and call app.include_router(router) to assemble their operations into the application.
  ✘ b: Rename the local path to /api/orders without including the router.
      why: A path rename does not include a feature router.
  ✘ c: Nothing: creating APIRouter automatically attaches it to every app.
      why: Router registration and application inclusion are separate steps.
  feedback✔: Correct. Import feature routers and call app.include_router(router) to assemble their operations into the application.  feedback✘: Recheck the distinction: Import feature routers and call app.include_router(router) to assemble their operations into the application.  hints: ['Trace feature registration separately from inclusion in the application.']  remediation→r01
  MEASURES: A:distinguish_feature_registration_from_application_inclusion(f2,f3)   anchors=['assessment:distinguish_feature_registration_from_application_inclusion']
  taught-before-tested: A.f2←s01; A.f3←s01

### s05 · hands_on · Practice: Modular FastAPI application composition with APIRouter
Apply the contract — Work in the supplied orders-service exercise snapshot.
QUESTION [code_exercise, stretch, grading=client] Complete feature-router registration and application inclusion: create router, register GET /orders on it, and include it on app with prefix /api. The supplied entry combines the feature and application sections so no filesystem imports are required. Preserve list_orders and its supplied static result. GET /api/orders must reach the feature; local /orders must not be exposed on app. The supplied module loader publishes the completed feature router as orders.router; retain the actual from orders import router import in the application section.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': ['fastapi']} constraints.allowed=['from fastapi import APIRouter', 'from fastapi import FastAPI', 'from orders import router', 'router = APIRouter()', 'app = FastAPI()', '@router.get("/orders")', 'def with no parameters', 'return []', 'app.include_router(router)', 'app.include_router(router, prefix="/api")'] blocked=11 items
  file main.py [editable]:
from fastapi import FastAPI, APIRouter
# Supplied feature-module boundary; the sandbox assembles it in one entry file.
app = FastAPI()
orders_result = "synthetic-orders"
router = APIRouter()
def list_orders(): return orders_result

# Supplied single-file feature-module loader, used only because the runner executes one entry.
import sys, types
feature_module = types.ModuleType("orders")
feature_module.router = router
sys.modules["orders"] = feature_module
from orders import router
# TODO: register on router, then include it with /api.

def router_paths(scope):
    routes = router.routes if scope == "feature" else app.routes
    return [r.path for r in routes if "orders" in r.path]

  SOLUTION main.py:
from fastapi import FastAPI, APIRouter
# Supplied feature-module boundary; the sandbox assembles it in one entry file.
app = FastAPI()
orders_result = "synthetic-orders"
router = APIRouter()
@router.get("/orders")
def list_orders(): return orders_result

# Supplied single-file feature-module loader, used only because the runner executes one entry.
import sys, types
feature_module = types.ModuleType("orders")
feature_module.router = router
sys.modules["orders"] = feature_module
from orders import router
app.include_router(router, prefix="/api")

def router_paths(scope):
    routes = router.routes if scope == "feature" else app.routes
    return [r.path for r in routes if "orders" in r.path]

  test t1 (http_equals, visible=True): {"requests":[{"method":"GET","path":"/api/orders"}],"expected":{"status":200,"json":"synthetic-orders"}} | on-fail: The completed implementation does not meet this observable contract.
  test t2 (function_call, visible=True): {"function":"router_paths","args":["feature"],"expected":["/orders"]} | on-fail: The completed implementation does not meet this observable contract.
  test t3 (function_call, visible=True): {"function":"router_paths","args":["application"],"expected":["/api/orders"]} | on-fail: The completed implementation does not meet this observable contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"50f353f4602f2ac5a4dbef8b174cdd17df10bdef8702da275281fa6c7e96bfe4","tests_passed":3}
  feedback✔: Correct. Create an APIRouter for a feature's operations and register those operations on that router rather than requiring all handlers to live in the main module.  feedback✘: Recheck the distinction: Create an APIRouter for a feature's operations and register those operations on that router rather than requiring all handlers to live in the main module.  hints: ['Trace feature registration separately from inclusion in the application.']
  MEASURES: A:determine_included_operation_paths(f1,f2,f3)   anchors=['practice', 'assessment:determine_included_operation_paths']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

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

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: app.add_middleware(...)
· constraints.blocked_syntax: app.dependency_overrides[...]

=========

# EVALUATOR PACKET — Typed path and query input binding · Response-model serialization and private-field exclusion (tile_030)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.path_query_binding — Typed path and query input binding
B = fastapi.response_model_serialization — Response-model serialization and private-field exclusion

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=4
  warn: remediation step tile_030.r02 is never referenced
  warn: remediation step tile_030.r03 is never referenced
  warn: remediation step tile_030.r05 is never referenced
  warn: remediation step tile_030.r06 is never referenced

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
(walkthrough) Read the read_order signature against /orders/{order_id}. The placeholder supplies order_id, whose int annotation controls conversion; a nonconvertible path value produces a validation error rather than being passed through unchanged. limit has no placeholder, so this ordinary scalar input comes from the query. Its declared default permits omission. Removing that default would make limit required, without changing its query source or the conversion of a supplied string. ⟦A.f1 A.f2 A.f3 A.f4 A:tb5 A:tb6⟧

### s04 · video · Typed path and query input binding
[VIDEO Bind a typed identifier from the URL path] bridge-before: Watch how the path placeholder matches the typed handler argument. The clip uses posts rather than orders; its temporary not-found dictionary is explicitly not a correct failure-handling pattern. | bridge-after: The clip explains typed path binding and rejection of a noninteger identifier. It does not cover query binding or query defaults; the text teaches both, including conversion and requiredness.
  - WRjXIA5pMtk 85-345s facts=['f1', 'f4'] label: Declare a path placeholder and an integer handler argument | summary: A path parameter is a variable part of a URL. The example adds a post_id placeholder to a route and declares the matching handler argument as an integer. FastAPI uses that declaration to capture and validate the supplied value. The handler searches an in-memory list for a matching post. Browser requests using identifiers 1 and 2 return the corresponding posts. The explanation also states that supplying hello instead of an integer produces a validation error; an invalid request is not demonstrated in this range. The temporary not-found dictionary is explicitly identified as an incorrect way to handle that failure.

### s05 · check · Choose the distinction: Typed path and query input binding
Check your understanding — Use the declared contract to distinguish the outcomes.
QUESTION [choice, intro, grading=client] For a handler input limit: int = 10 that is not in the route path, what happens when the query string omits limit?
  ✔ a: The handler receives the default integer 10.
      why: Correct. A query parameter with a default may be omitted, while a parameter without a default is required; the type controls conversion of a supplied string.
  ✘ b: The query input is required despite its default.
      why: The default makes omission valid.
  ✘ c: The handler receives the string "10".
      why: The input is annotated int, including the default used here.
  feedback✔: Correct. A query parameter with a default may be omitted, while a parameter without a default is required; the type controls conversion of a supplied string.  feedback✘: Recheck the distinction: A query parameter with a default may be omitted, while a parameter without a default is required; the type controls conversion of a supplied string.  hints: ['Compare placeholder names, annotations and defaults independently.']  remediation→r01
  MEASURES: A:determine_query_requiredness_and_conversion(f3)   anchors=['assessment:determine_query_requiredness_and_conversion']
  taught-before-tested: A.f3←s01

### s06 · check · Choose the distinction: Typed path and query input binding
Check your understanding — Use the declared contract to distinguish the outcomes.
QUESTION [choice, core, grading=client] GET /orders/{order_id} binds order_id: int. A request uses /orders/not-an-integer. Which result follows from path conversion?
  ✔ a: Validation rejects the unconvertible path value before the handler runs.
      why: Correct. Put a name in the route path as {name} and declare name: Type in the handler to bind and convert that path value.
  ✘ b: The handler receives the original string.
      why: The int annotation requires conversion and validation.
  ✘ c: The value is taken from a query input instead.
      why: The matching path placeholder determines the binding source.
  feedback✔: Correct. Put a name in the route path as {name} and declare name: Type in the handler to bind and convert that path value.  feedback✘: Recheck the distinction: Put a name in the route path as {name} and declare name: Type in the handler to bind and convert that path value.  hints: ['Compare placeholder names, annotations and defaults independently.']
  MEASURES: A:determine_path_conversion_and_rejection(f1,f4)   anchors=['assessment:determine_path_conversion_and_rejection']
  taught-before-tested: A.f1←s01; A.f4←s01

### s07 · hands_on · Practice: Typed path and query input binding
Apply the contract — Work in the supplied orders-service exercise snapshot.
QUESTION [code_exercise, stretch, grading=client] Bind the order_id path placeholder to order_id: int; declare limit: int = 10 as a query input absent from the path. Return exactly {"order_id": order_id, "limit": limit}. Tests cover /orders/42 without limit and /orders/7?limit=3.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': ['fastapi']} constraints.allowed=['from fastapi import FastAPI', 'app = FastAPI()', '@app.get("/orders/{order_id}")', 'def', 'integer parameter annotations with int', 'parameter defaults using integer literals', 'return', 'dictionary literals', 'string literals', 'parameter references'] blocked=11 items
  file main.py [editable]:
from fastapi import FastAPI
app = FastAPI()
@app.get("/orders/{order_id}")
def read_order(): return {}

  SOLUTION main.py:
from fastapi import FastAPI
app = FastAPI()
@app.get("/orders/{order_id}")
def read_order(order_id: int, limit: int = 10):
    return {"order_id": order_id, "limit": limit}

  test t1 (http_equals, visible=True): {"requests":[{"method":"GET","path":"/orders/42"}],"expected":{"status":200,"json":{"order_id":42,"limit":10}}} | on-fail: The completed implementation does not meet this observable contract.
  test t2 (http_equals, visible=True): {"requests":[{"method":"GET","path":"/orders/7","params":{"limit":3}}],"expected":{"status":200,"json":{"order_id":7,"limit":3}}} | on-fail: The completed implementation does not meet this observable contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"67751e3e4f3dfdd802527f4ab860a14d346caf7c0407e877deed4dfa818f59f4","tests_passed":2}
  feedback✔: Correct. Put a name in the route path as {name} and declare name: Type in the handler to bind and convert that path value.  feedback✘: Recheck the distinction: Put a name in the route path as {name} and declare name: Type in the handler to bind and convert that path value.  hints: ['Compare placeholder names, annotations and defaults independently.']
  MEASURES: A:determine_path_and_query_binding(f1,f2)   anchors=['practice', 'assessment:determine_path_and_query_binding']
  taught-before-tested: A.f1←s01; A.f2←s01

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
(walkthrough) Start with the return internal_order line, then inspect the decorator and PublicOrder fields. This normally returned value follows response_model=PublicOrder for validation, serialization and filtering; a return annotation would not take priority over that model. The internal private_processing_note is not an output-model field, so its presence internally does not make it public. Contrast a directly returned Response: automatic model conversion and filtering are bypassed, leaving the application responsible for the content. ⟦B.f1 B.f2 B.f3 B.f4 B:tb5 B:tb6⟧

### s11 · check · Choose the distinction: Response-model serialization and private-field exclusion
Check your understanding — Use the declared contract to distinguish the outcomes.
QUESTION [choice, core, grading=client] PublicOrder declares only order_id and status. A handler returns an internal dictionary containing those fields plus private_processing_note through response_model=PublicOrder. Which fields appear publicly?
  ✔ a: order_id and status only.
      why: Correct. Set response_model=PublicModel on the operation decorator to validate, serialize and filter the returned value to that public model.
  ✘ b: All three dictionary fields.
      why: Normal response-model processing projects the declared public fields.
  ✘ c: private_processing_note only.
      why: The private note is not declared in PublicOrder.
  feedback✔: Correct. Set response_model=PublicModel on the operation decorator to validate, serialize and filter the returned value to that public model.  feedback✘: Recheck the distinction: Set response_model=PublicModel on the operation decorator to validate, serialize and filter the returned value to that public model.  hints: ['Compare the declared public fields with the internal dictionary and the return path.']  remediation→r04
  MEASURES: B:determine_publicly_projected_fields(f1,f2)   anchors=['assessment:determine_publicly_projected_fields']
  taught-before-tested: B.f1←s08; B.f2←s08

### s12 · check · Choose the distinction: Response-model serialization and private-field exclusion
Check your understanding — Use the declared contract to distinguish the outcomes.
QUESTION [choice, core, grading=client] A route declares response_model=PublicOrder but returns a directly constructed Response. Can you rely on response-model filtering for that returned response?
  ✔ a: No; a directly returned Response bypasses that normal model processing.
      why: Correct. Returning a Response object directly bypasses automatic response-model conversion and filtering, so the application is responsible for that content.
  ✘ b: Yes; the decorator filters every returned Response.
      why: Direct Response return is the bypass case.
  ✘ c: Yes; a return annotation restores filtering of the Response.
      why: A return annotation does not remove the direct-response bypass.
  feedback✔: Correct. Returning a Response object directly bypasses automatic response-model conversion and filtering, so the application is responsible for that content.  feedback✘: Recheck the distinction: Returning a Response object directly bypasses automatic response-model conversion and filtering, so the application is responsible for that content.  hints: ['Compare the declared public fields with the internal dictionary and the return path.']
  MEASURES: B:recognize_direct_response_filtering_bypass(f4)   anchors=['assessment:recognize_direct_response_filtering_bypass']
  taught-before-tested: B.f4←s08

### s13 · hands_on · Practice: Response-model serialization and private-field exclusion
Apply the contract — Work in the supplied orders-service exercise snapshot.
QUESTION [code_exercise, stretch, grading=client] Define PublicOrder with order_id: int and status: str only. Set response_model=PublicOrder on GET /orders/{order_id}; return the supplied internal_order dictionary normally, not a direct Response. The public JSON must contain exactly order_id and status and exclude private_processing_note for both fixture requests. Keep the supplied -> dict return annotation; the explicit response_model takes priority over it.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': ['fastapi', 'pydantic']} constraints.allowed=['from fastapi import FastAPI', 'from pydantic import BaseModel', 'app = FastAPI()', 'class PublicOrder(BaseModel):', 'order_id: int', 'status: str', 'dictionary literals with order_id, status, and private_processing_note keys', 'integer and string literals', 'variable assignment', '@app.get("/orders/{order_id}", response_model=PublicOrder)', 'def function declarations with an order_id: int parameter', 'return internal_order'] blocked=11 items
  file main.py [editable]:
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
order_status = 'pending'
private_note = 'synthetic internal note 1'
internal_order = {"order_id": 42, "status": order_status, "private_processing_note": private_note}
@app.get("/orders/{order_id}")
def read_order(order_id: int) -> dict: return internal_order

  SOLUTION main.py:
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
order_status = 'pending'
private_note = 'synthetic internal note 1'
internal_order = {"order_id": 42, "status": order_status, "private_processing_note": private_note}
class PublicOrder(BaseModel):
    order_id: int
    status: str
@app.get("/orders/{order_id}", response_model=PublicOrder)
def read_order(order_id: int) -> dict:
    return internal_order

  test t1 (http_equals, visible=True): {"requests":[{"method":"GET","path":"/orders/42"}],"expected":{"status":200,"json":{"order_id":42,"status":"pending"}}} | on-fail: The completed implementation does not meet this observable contract.
  test t2 (http_equals, visible=True): {"requests":[{"method":"GET","path":"/orders/7"}],"expected":{"status":200,"json":{"order_id":42,"status":"pending"}}} | on-fail: The completed implementation does not meet this observable contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"e1cd16d0598193019ec78bb8dc1464c05b39e07796614e30540786242fc8a9c7","tests_passed":2}
  feedback✔: Correct. When both a return annotation and response_model are supplied, response_model takes priority for FastAPI's response processing.  feedback✘: Recheck the distinction: When both a return annotation and response_model are supplied, response_model takes priority for FastAPI's response processing.  hints: ['Compare the declared public fields with the internal dictionary and the return path.']
  MEASURES: B:identify_response_model_priority_over_return_annotation(f3)   anchors=['practice', 'assessment:identify_response_model_priority_over_return_annotation']
  taught-before-tested: B.f3←s08

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

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: @app.middleware(...)
· constraints.blocked_syntax: @app.exception_handler(...)
· constraints.blocked_syntax: app.dependency_overrides[...]

=========

# EVALUATOR PACKET — Depends (tile_032)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi_backend.depends — Depends

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: remediation step tile_032.r02 is never referenced

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
(walkthrough) Read the orders handler backward from return {"context": context} to its Annotated[str, Depends(provider)] parameter. The returned context is the explicit handler argument supplied when FastAPI executes the provider and resolves its inputs. Depends receives provider itself, not provider() evaluated in the declaration. Another operation can declare the same supplier for shared input-provision logic; reuse is visible at each consuming parameter rather than hidden in an application-wide value store. ⟦A.f1 A.f2 A.f3 A:tb5 A:tb6⟧

### s04 · video · Depends
[VIDEO Make a handler’s supplied service input explicit] bridge-before: Watch how construction moves from the handler into a provider, then becomes an Annotated input. The clip’s wording about avoiding repeated instantiation means avoiding manual construction in handlers, not sharing one application-wide object. | bridge-after: The clip demonstrates supplied inputs and reusable declarations. It does not explain why Depends receives the callable rather than its result; the text covers that distinction so FastAPI can resolve the provider’s inputs.
  - f270BoTicMA 323-534s facts=['f1', 'f3'] label: Supply a service object with Depends and Annotated | summary: A simple Logger class illustrates a service object that an endpoint needs. Constructing that object inside each handler repeats the provision logic. Moving construction into get_logger gives handlers a reusable provider that returns a new Logger. Depends connects the handler’s declared input to that provider. An Annotated[Logger, Depends(get_logger)] alias then makes the same declaration reusable without repeating it in every handler. The reuse concerns the declaration and provision logic; the provider still constructs a new object.

### s05 · check · Choose the distinction: Depends
Check your understanding — Use the declared contract to distinguish the outcomes.
QUESTION [choice, intro, grading=client] A shared provider must produce one context string for several handlers. What makes its input-provision behavior explicit?
  ✔ a: Put the reusable provision logic in a callable and declare it as a dependency parameter.
      why: Correct. A dependency makes a handler's needed input explicit and can be reused by multiple operations for shared input-provision logic.
  ✘ b: Read an unrelated global context in each handler instead.
      why: That does not declare provider-supplied input.
  ✘ c: Treat the provider as a handler decorator rather than a supplied input.
      why: The callable supplies a value through the declared dependency input.
  feedback✔: Correct. A dependency makes a handler's needed input explicit and can be reused by multiple operations for shared input-provision logic.  feedback✘: Recheck the distinction: A dependency makes a handler's needed input explicit and can be reused by multiple operations for shared input-provision logic.  hints: ['Look at whether the handler declares a provider-supplied input or fetches a value itself.']  remediation→r01
  MEASURES: A:identify_explicit_shared_input_provision_logic(f3)   anchors=['assessment:identify_explicit_shared_input_provision_logic']
  taught-before-tested: A.f3←s01

### s06 · hands_on · Practice: Depends
Apply the contract — Work in the supplied orders-service exercise snapshot.
QUESTION [code_exercise, stretch, grading=client] Wire orders(context: Annotated[str, Depends(provider)]) and return context exactly. Pass provider, not provider(); do not call the provider inside the handler or return a global value. This is demonstration input provisioning, not credential verification.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': ['fastapi']} constraints.allowed=['from typing import Annotated', 'from fastapi import FastAPI, Depends', 'app = FastAPI()', '@app.get("/orders")', 'def', 'str annotations', 'string literals', 'return', 'dictionary literals with string keys and values', 'Annotated[str, Depends(provider)]', 'handler parameter references'] blocked=10 items
  file main.py [editable]:
from typing import Annotated
from fastapi import FastAPI, Depends
app = FastAPI()
provided_context = "synthetic-auth-context-not-verified"
def provider() -> str: return provided_context
@app.get("/orders")
def orders(): return {}

  SOLUTION main.py:
from typing import Annotated
from fastapi import FastAPI, Depends
app = FastAPI()
provided_context = "synthetic-auth-context-not-verified"
def provider() -> str: return provided_context
@app.get("/orders")
def orders(context: Annotated[str, Depends(provider)]):
    return context

  test t1 (http_equals, visible=True): {"requests":[{"method":"GET","path":"/orders"}],"expected":{"status":200,"json":"synthetic-auth-context-not-verified"}} | on-fail: The completed implementation does not meet this observable contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"f8c317aff3ea52af5ce6740930829d949a7e8e9e4edd8ef72b035cc499c7a238","tests_passed":1}
  feedback✔: Correct. Declare a handler input with Annotated[Type, Depends(provider)] to have FastAPI execute the provider and supply its returned value.  feedback✘: Recheck the distinction: Declare a handler input with Annotated[Type, Depends(provider)] to have FastAPI execute the provider and supply its returned value.  hints: ['Look at whether the handler declares a provider-supplied input or fetches a value itself.']
  MEASURES: A:determine_provider_supplied_handler_context(f1,f2)   anchors=['practice', 'assessment:determine_provider_supplied_handler_context']
  taught-before-tested: A.f1←s01; A.f2←s01

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

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: nested Depends declarations inside providers
· constraints.blocked_syntax: OAuth2PasswordBearer(...)

=========

# EVALUATOR PACKET — Outbound timeouts (tile_033)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = integration.outbound_timeouts — Outbound timeouts

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: remediation step tile_033.r02 is never referenced
  warn: remediation step tile_033.r03 is never referenced

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
QUESTION [choice, intro, grading=client] HTTPX has a finite read timeout. A response keeps supplying chunks within that wait limit, but the whole request takes longer than the timeout number. Which interpretation is correct?
  ✔ a: The read limit bounds individual chunk waits, not total elapsed request duration.
      why: Correct. HTTPX distinguishes connect, read, write and pool timeouts; read and write limits bound waiting for individual chunks rather than a whole request's elapsed duration.
  ✘ b: The read limit always enforces that whole-request elapsed deadline.
      why: Read timeouts concern individual chunk waits.
  ✘ c: Finite timeout and timeout=None both disable enforcement.
      why: timeout=None disables enforcement; a finite limit does not.
  feedback✔: Correct. HTTPX distinguishes connect, read, write and pool timeouts; read and write limits bound waiting for individual chunks rather than a whole request's elapsed duration.  feedback✘: Recheck the distinction: HTTPX distinguishes connect, read, write and pool timeouts; read and write limits bound waiting for individual chunks rather than a whole request's elapsed duration.  hints: ['Identify which wait exceeded its limit and which exception the excerpt handles.']  remediation→r01
  MEASURES: A:distinguish_finite_io_limits_from_total_elapsed_budget(f1,f2)   anchors=['assessment:distinguish_finite_io_limits_from_total_elapsed_budget']
  taught-before-tested: A.f1←s01; A.f2←s01

### s04 · check · Choose the distinction: Outbound timeouts
Check your understanding — Use the declared contract to distinguish the outcomes.
QUESTION [choice, core, grading=client] An asynchronous operation exceeds a budget inside async with asyncio.timeout(seconds). Where is the converted TimeoutError caught?
  ✔ a: Outside the timeout context.
      why: Correct. When the contract requires a total elapsed-time budget across asynchronous work, wrap the operation in async with asyncio.timeout(seconds); its cancellation is converted to TimeoutError outside the context.
  ✘ b: Only inside the context before it exits.
      why: The cancellation is converted to TimeoutError outside that context.
  ✘ c: As httpx.ReadTimeout regardless of the work inside.
      why: The total-budget context converts to TimeoutError, not an HTTPX read-wait exception.
  feedback✔: Correct. When the contract requires a total elapsed-time budget across asynchronous work, wrap the operation in async with asyncio.timeout(seconds); its cancellation is converted to TimeoutError outside the context.  feedback✘: Recheck the distinction: When the contract requires a total elapsed-time budget across asynchronous work, wrap the operation in async with asyncio.timeout(seconds); its cancellation is converted to TimeoutError outside the context.  hints: ['Identify which wait exceeded its limit and which exception the excerpt handles.']
  MEASURES: A:identify_total_budget_timeout_outside_async_context(f4)   anchors=['assessment:identify_total_budget_timeout_outside_async_context']
  taught-before-tested: A.f4←s01

### s05 · hands_on · Practice: Outbound timeouts
Apply the contract — Work in the supplied orders-service exercise snapshot.
QUESTION [classify, stretch, grading=client] Inspect the shipping lookup excerpts and their supplied stalled-upstream evidence. Classify whether each bounds the read wait and returns a distinct handled timeout outcome. This is inspect-and-judge, not executable network practice; a read limit is not a total elapsed deadline.
  'async with httpx.AsyncClient(timeout=2) as client:
    try:
        await client.get(shipping_url)
    except httpx.ReadTimeout:
        return "shipping-read-timeout"
Evidence: connection succeeds, no response chunk arrives before the read limit, and the function returns shipping-read-timeout.' -> Finite wait limit and handled read-timeout outcome
      feedback: Finite wait limit and handled read-timeout outcome. HTTPX distinguishes connect, read, write and pool timeouts; read and write limits bound waiting for individual chunks rather than a whole request's elapsed duration.
  'async with httpx.AsyncClient(timeout=None) as client:
    await client.get(shipping_url)
Evidence: the upstream accepts the connection but never supplies a response chunk; no timeout outcome is returned.' -> Timeout enforcement disabled
      feedback: Timeout enforcement disabled. HTTPX distinguishes connect, read, write and pool timeouts; read and write limits bound waiting for individual chunks rather than a whole request's elapsed duration.
  'async with httpx.AsyncClient(timeout=2) as client:
    try:
        await client.get(shipping_url)
    except httpx.ConnectTimeout:
        return "shipping-timeout"
Evidence: connection succeeds, the response chunk stalls, and an unhandled ReadTimeout escapes.' -> Finite wait limit but wrong exception handled
      feedback: Finite wait limit but wrong exception handled. HTTPX distinguishes connect, read, write and pool timeouts; read and write limits bound waiting for individual chunks rather than a whole request's elapsed duration.
  feedback✔: Correct. HTTPX distinguishes connect, read, write and pool timeouts; read and write limits bound waiting for individual chunks rather than a whole request's elapsed duration.  feedback✘: Recheck the distinction: HTTPX distinguishes connect, read, write and pool timeouts; read and write limits bound waiting for individual chunks rather than a whole request's elapsed duration.  hints: ['Identify which wait exceeded its limit and which exception the excerpt handles.']
  MEASURES: A:determine_httpx_timeout_outcome_for_exceeded_wait(f1,f3)   anchors=['practice', 'assessment:determine_httpx_timeout_outcome_for_exceeded_wait']
  taught-before-tested: A.f1←s01; A.f3←s01

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

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=3
  warn: remediation step tile_034.r02 is never referenced
  warn: remediation step tile_034.r04 is never referenced
  warn: remediation step tile_034.r06 is never referenced

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
QUESTION [choice, intro, grading=client] A reusable business decision takes a FastAPI request object and builds an HTTP response. What boundary should a refactor restore?
  ✔ a: Use ordinary values for the business decision; keep HTTP adaptation in the handler.
      why: Correct. Transport handlers adapt HTTP inputs and outputs, business callables enforce application rules, and persistence adapters access stored state; separate these responsibilities so each can change without embedding the other responsibilities.
  ✘ b: Move HTTP response construction into the persistence adapter.
      why: Stored-state access and HTTP adaptation are different responsibilities.
  ✘ c: Make every business caller construct a FastAPI request.
      why: That preserves protocol coupling instead of removing it.
  feedback✔: Correct. Transport handlers adapt HTTP inputs and outputs, business callables enforce application rules, and persistence adapters access stored state; separate these responsibilities so each can change without embedding the other responsibilities.  feedback✘: Recheck the distinction: Transport handlers adapt HTTP inputs and outputs, business callables enforce application rules, and persistence adapters access stored state; separate these responsibilities so each can change without embedding the other responsibilities.  hints: ['Locate HTTP adaptation, the decision rule and stored-state access separately.']  remediation→r01
  MEASURES: A:identify_protocol_coupling_and_responsibility_boundaries(f2,f3)   anchors=['assessment:identify_protocol_coupling_and_responsibility_boundaries']
  taught-before-tested: A.f2←s01; A.f3←s01

### s04 · hands_on · Practice: Separating transport, testable business logic and persistence responsibilities
Apply the contract — Work in the supplied orders-service exercise snapshot.
QUESTION [code_exercise, stretch, grading=client] Refactor without changing the supplied quantity rule: define plain can_accept(requested: int, stored: int) -> bool using requested <= stored. Keep stored-state access solely in the supplied adapter. The endpoint receives quantity via Depends(requested_quantity), obtains stored quantity from adapter.quantity(order_id), calls can_accept, and returns its bool. Direct business calls and requests must preserve the rule.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': ['fastapi']} constraints.allowed=['def function_name(...):', 'int and bool parameter and return annotations', 'return statements', 'ordinary function calls with explicit arguments', 'local variable assignment', 'integer literals and comparison operators used by the supplied order rule', 'dictionary literals and indexing used by the supplied order-state fixture', '@app.get(...)', 'typed path and query parameters', 'Depends(provider) as a declared handler parameter'] blocked=10 items
  file main.py [editable]:
from fastapi import FastAPI, Depends
app = FastAPI()
order_state = {42: {'order_id': 42, 'quantity': 5}, 43: {'order_id': 43, 'quantity': 0}, 44: {'order_id': 44, 'quantity': 3}, 45: {'order_id': 45, 'quantity': 10}, 46: {'order_id': 46, 'quantity': 1}, 7: {'order_id': 7, 'quantity': 2}}
class OrderStateAdapter:
    def quantity(self, order_id: int) -> int:
        return order_state[order_id]["quantity"]
adapter = OrderStateAdapter()
def requested_quantity(quantity: int) -> int: return quantity
@app.get("/orders/{order_id}")
def decide_order(order_id: int, quantity: int):
    return quantity <= order_state[order_id]["quantity"]

  SOLUTION main.py:
from fastapi import FastAPI, Depends
app = FastAPI()
order_state = {42: {'order_id': 42, 'quantity': 5}, 43: {'order_id': 43, 'quantity': 0}, 44: {'order_id': 44, 'quantity': 3}, 45: {'order_id': 45, 'quantity': 10}, 46: {'order_id': 46, 'quantity': 1}, 7: {'order_id': 7, 'quantity': 2}}
class OrderStateAdapter:
    def quantity(self, order_id: int) -> int:
        return order_state[order_id]["quantity"]
adapter = OrderStateAdapter()
def requested_quantity(quantity: int) -> int: return quantity
def can_accept(requested: int, stored: int) -> bool:
    return requested <= stored
@app.get("/orders/{order_id}")
def decide_order(order_id: int, quantity: int = Depends(requested_quantity)):
    stored = adapter.quantity(order_id)
    return can_accept(quantity, stored)

  test t1 (function_call, visible=True): {"function":"can_accept","args":[2,5],"expected":true} | on-fail: The completed implementation does not meet this observable contract.
  test t2 (function_call, visible=True): {"function":"can_accept","args":[6,5],"expected":false} | on-fail: The completed implementation does not meet this observable contract.
  test t3 (http_equals, visible=True): {"requests":[{"method":"GET","path":"/orders/42","params":{"quantity":2}}],"expected":{"status":200,"json":true}} | on-fail: The completed implementation does not meet this observable contract.
  test t4 (http_equals, visible=True): {"requests":[{"method":"GET","path":"/orders/42","params":{"quantity":6}}],"expected":{"status":200,"json":false}} | on-fail: The completed implementation does not meet this observable contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"543901360c62d6c6d9f71056f47de4177ef1f02bb613a4b94a6dab12078d3202","tests_passed":4}
  feedback✔: Correct. A dependency can extract reusable input-provision logic from individual operation handlers and expose the supplied value as a declared handler parameter.  feedback✘: Recheck the distinction: A dependency can extract reusable input-provision logic from individual operation handlers and expose the supplied value as a declared handler parameter.  hints: ['Locate HTTP adaptation, the decision rule and stored-state access separately.']
  MEASURES: A:identify_reusable_input_provisioning(f1); A:identify_misplaced_transport_business_and_persistence_logic(f2)   anchors=['practice', 'assessment:identify_reusable_input_provisioning', 'assessment:identify_misplaced_transport_business_and_persistence_logic']
  taught-before-tested: A.f1←s01; A.f2←s01

### s05 · explainer · The rule: Bounded in-process background work and nondurable delivery limits
(definition) Declare a BackgroundTasks handler parameter and call background_tasks.add_task(callable, *args, **kwargs) to schedule work after sending the response. ⟦B.f1 B:tb2⟧
(mechanism) A background task callable can be a normal def or async def function; FastAPI handles either form. BackgroundTasks work runs in the application process and cannot guarantee survival or delivery when that process fails. ⟦B.f2 B.f3 B:tb3⟧
[DIAGRAM] nodes=['Handler registers add_task', 'Response sent', 'Follow-up task: def or async def', 'Application process boundary', 'Process failure after response'] edges=[('n0', 'n1', 'register callable and arguments'), ('n1', 'n2', 'task runs after response'), ('n3', 'n2', 'in-process work'), ('n4', 'n2', 'pending work can be lost; no guaranteed survival or delivery')] alt: Show an order handler registering follow-up work, sending its response, and then running the task inside the application-process boundary. Mark a process failure after the response as a point where pending work can be lost, separating response delivery from follow-up completion.

### s06 · explainer · Trace the boundary: Bounded in-process background work and nondurable delivery limits
(walkthrough) Declare BackgroundTasks and register a callable with background_tasks.add_task(callable, *args, **kwargs). The response is sent before follow-up work runs in the application process. The callable may use def or async def. If the process fails, survival or delivery cannot be guaranteed. Scheduling therefore does not prove durable completion. ⟦B.f1 B.f2 B.f3 B:tb4 B:tb5⟧

### s07 · video · Bounded in-process background work and nondurable delivery limits
[VIDEO Response-first work and the process-failure boundary] bridge-before: Watch for the response-first sequence and the loss of pending work on a server crash. The clip's email example assumes requesting another email is acceptable; suitability depends on the operation's required outcome. | bridge-after: The clip explains the delivery limitation but omits the handler parameter, add_task syntax, and supported callable forms. The text supplies those details and makes the application-process boundary explicit.
  - 4HxjBvZMAg8 1514-1562s facts=['f3'] label: Deferred email work and the risk of losing pending tasks | summary: Sending email can delay a response while the application communicates with an email server. FastAPI background tasks let the response go first and the email work run afterward. Pending tasks are lost if the server crashes. Work requiring guaranteed delivery needs a different execution arrangement. The example treats a password-reset email as acceptable to defer because the user can request another.

### s08 · check · Choose the distinction: Bounded in-process background work and nondurable delivery limits
Check your understanding — Use the declared contract to distinguish the outcomes.
QUESTION [choice, core, grading=client] Which task fits optional in-process BackgroundTasks rather than a durable execution guarantee?
  ✔ a: A small optional follow-up whose loss on process failure is acceptable.
      why: Correct. BackgroundTasks work runs in the application process and cannot guarantee survival or delivery when that process fails.
  ✘ b: A required job that must finish despite process failure.
      why: Process-local deferred work does not provide that guarantee.
  ✘ c: A long critical job whose completion must survive restart.
      why: Critical durable completion needs are not satisfied by this placement.
  feedback✔: Correct. BackgroundTasks work runs in the application process and cannot guarantee survival or delivery when that process fails.  feedback✘: Recheck the distinction: BackgroundTasks work runs in the application process and cannot guarantee survival or delivery when that process fails.  hints: ['Distinguish registering a callable from invoking it; consider the process-failure boundary.']  remediation→r03
  MEASURES: B:distinguish_bounded_in_process_work_from_durable_execution_needs(f3)   anchors=['assessment:distinguish_bounded_in_process_work_from_durable_execution_needs']
  taught-before-tested: B.f3←s05

### s09 · hands_on · Practice: Bounded in-process background work and nondurable delivery limits
Apply the contract — Work in the supplied orders-service exercise snapshot.
QUESTION [code_exercise, stretch, grading=client] Register the supplied optional order_follow_up callable with background_tasks.add_task(order_follow_up, order_id), not an immediate call, before returning {"order_id": order_id}. Declare background_tasks: BackgroundTasks. Add the exact docstring "Optional process-local follow-up; this is not guaranteed completion." The inspector checks registration before response sending with identifiers 42 and 7; this task may be lost on process failure.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': ['fastapi']} constraints.allowed=['from fastapi import FastAPI, BackgroundTasks', 'FastAPI()', '@app.post(...)', 'def', 'async def', 'function parameter annotations', 'str', 'string literals', 'return', 'function calls', 'background_tasks.add_task(callable, *args, **kwargs)'] blocked=10 items
  file main.py [editable]:
from fastapi import FastAPI, BackgroundTasks
app = FastAPI()
order_id = "42"
follow_ups = []
def order_follow_up(order_id: str): follow_ups.append(order_id)
@app.post("/orders")
def create_order(background_tasks: BackgroundTasks):
    return {"order_id": order_id}

# Supplied deferred-registration inspector; it calls the handler, not a server.
def inspect_follow_up(identifier):
    global order_id
    order_id = identifier
    follow_ups.clear()
    tasks = BackgroundTasks()
    response = create_order(tasks)
    return {"response": response, "called_immediately": list(follow_ups), "registered": [[t.func.__name__, list(t.args)] for t in tasks.tasks]}

  SOLUTION main.py:
from fastapi import FastAPI, BackgroundTasks
app = FastAPI()
order_id = "42"
follow_ups = []
def order_follow_up(order_id: str): follow_ups.append(order_id)
@app.post("/orders")
def create_order(background_tasks: BackgroundTasks):
    """Optional process-local follow-up; this is not guaranteed completion."""
    background_tasks.add_task(order_follow_up, order_id)
    return {"order_id": order_id}

# Supplied deferred-registration inspector; it calls the handler, not a server.
def inspect_follow_up(identifier):
    global order_id
    order_id = identifier
    follow_ups.clear()
    tasks = BackgroundTasks()
    response = create_order(tasks)
    return {"response": response, "called_immediately": list(follow_ups), "registered": [[t.func.__name__, list(t.args)] for t in tasks.tasks]}

  test t1 (function_call, visible=True): {"function":"inspect_follow_up","args":["42"],"expected":{"response":{"order_id":"42"},"called_immediately":[],"registered":[["order_follow_up",["42"]]]}} | on-fail: The completed implementation does not meet this observable contract.
  test t2 (function_call, visible=True): {"function":"inspect_follow_up","args":["7"],"expected":{"response":{"order_id":"7"},"called_immediately":[],"registered":[["order_follow_up",["7"]]]}} | on-fail: The completed implementation does not meet this observable contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"b7f2dc3018f375ceeefa631ad0ee380c48d31913ca5581a8e3470ecc19909a63","tests_passed":2}
  feedback✔: Correct. The handler registers the supplied follow-up callable without calling it immediately, returns the order response, and the learner identifies that this placement would not satisfy a guaranteed-completion requirement.  feedback✘: Recheck the distinction: The handler registers the supplied follow-up callable without calling it immediately, returns the order response, and the learner identifies that this placement would not satisfy a guaranteed-completion requirement.  hints: ['Distinguish registering a callable from invoking it; consider the process-failure boundary.']
  MEASURES: B:distinguish_bounded_in_process_work_from_durable_execution_needs(f3)   anchors=['practice']
  taught-before-tested: B.f3←s05

### s10 · explainer · The rule: Composing request dependency graphs
(definition) A provider can declare its own Annotated[Type, Depends(other_provider)] parameter, forming a dependency graph. ⟦C.f1 C:tb2⟧
(mechanism) FastAPI resolves a provider's prerequisite inputs before calling that provider and supplies its result to the consuming operation. A sub-dependency can declare typed query inputs of its own; those inputs are extracted from the request before its returned value is supplied to the dependent provider. ⟦C.f2 C.f3 C:tb3⟧
[DIAGRAM] nodes=['Typed page and page_size query inputs', 'Pagination provider', 'Order-options provider', 'Consuming operation'] edges=[('n0', 'n1', 'extract and convert request inputs'), ('n1', 'n2', 'resolve prerequisite and supply its result'), ('n2', 'n3', 'supply provider result')] alt: Make the dependency direction and execution order visible: typed page and page_size request inputs → pagination provider → order-options provider → consuming operation.

### s11 · explainer · Trace the boundary: Composing request dependency graphs
(walkthrough) The pagination provider declares typed page and page_size query inputs. FastAPI extracts those inputs and resolves pagination before supplying its result to order-options; the consuming operation then receives the order-options result. A provider declares a prerequisite with Annotated[Type, Depends(other_provider)]. Trace from prerequisites toward consumers, not the reverse. ⟦C.f1 C.f2 C.f3 C:tb4 C:tb5⟧

### s12 · check · Choose the distinction: Composing request dependency graphs
Check your understanding — Use the declared contract to distinguish the outcomes.
QUESTION [choice, core, grading=client] The operation depends on order_options, which depends on pagination. What prerequisite-first execution order follows?
  ✔ a: pagination → order_options → operation.
      why: Correct. A provider can declare its own Annotated[Type, Depends(other_provider)] parameter, forming a dependency graph.
  ✘ b: operation → order_options → pagination.
      why: A consumer needs its prerequisites resolved first.
  ✘ c: order_options → pagination → operation.
      why: order_options consumes pagination, so pagination must be resolved first.
  feedback✔: Correct. A provider can declare its own Annotated[Type, Depends(other_provider)] parameter, forming a dependency graph.  feedback✘: Recheck the distinction: A provider can declare its own Annotated[Type, Depends(other_provider)] parameter, forming a dependency graph.  hints: ['Draw each provider-to-consumer dependency before tracing request inputs.']  remediation→r05
  MEASURES: C:determine_provider_execution_order(f1,f2,f3)   anchors=['assessment:determine_provider_execution_order']
  taught-before-tested: C.f1←s10; C.f2←s10; C.f3←s10

### s13 · hands_on · Practice: Composing request dependency graphs
Apply the contract — Work in the supplied orders-service exercise snapshot.
QUESTION [code_exercise, stretch, grading=client] Complete pagination(page: int, page_size: int) to return those two keys. Make order_options receive that dictionary through Annotated[..., Depends(pagination)] and return it. Make orders receive order_options through a declared dependency and return it. /orders?page=2&page_size=10 and page=3&page_size=5 must return exactly the typed query values; prerequisites resolve before consumers.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': ['fastapi']} constraints.allowed=['from typing import Annotated', 'from fastapi import FastAPI, Depends', 'FastAPI()', '@app.get(...)', 'def', 'typed parameters and return annotations', 'Annotated[Type, Depends(provider)]', 'int and str query parameters', 'dict[str, int]', 'dictionary literals and key access', 'return'] blocked=11 items
  file main.py [editable]:
from typing import Annotated
from fastapi import FastAPI, Depends
app = FastAPI()
def pagination(): return {}
def order_options(): return {}
@app.get("/orders")
def orders(): return {}

  SOLUTION main.py:
from typing import Annotated
from fastapi import FastAPI, Depends
app = FastAPI()
def pagination(page: int, page_size: int) -> dict[str, int]:
    return {"page": page, "page_size": page_size}
def order_options(pagination: Annotated[dict[str, int], Depends(pagination)]) -> dict[str, int]:
    return pagination
@app.get("/orders")
def orders(options: Annotated[dict[str, int], Depends(order_options)]):
    return options

  test t1 (http_equals, visible=True): {"requests":[{"method":"GET","path":"/orders","params":{"page":2,"page_size":10}}],"expected":{"status":200,"json":{"page":2,"page_size":10}}} | on-fail: The completed implementation does not meet this observable contract.
  test t2 (http_equals, visible=True): {"requests":[{"method":"GET","path":"/orders","params":{"page":3,"page_size":5}}],"expected":{"status":200,"json":{"page":3,"page_size":5}}} | on-fail: The completed implementation does not meet this observable contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"ce8d537909c62b6fceb91ae2593f8959175c2b516301c0d228089528ac80f92f","tests_passed":2}
  feedback✔: Correct. The pagination provider receives typed query inputs and returns a value consumed by order-options. The path operation receives the order-options result, with prerequisites resolved before their consumers.  feedback✘: Recheck the distinction: The pagination provider receives typed query inputs and returns a value consumed by order-options. The path operation receives the order-options result, with prerequisites resolved before their consumers.  hints: ['Draw each provider-to-consumer dependency before tracing request inputs.']
  MEASURES: C:determine_provider_execution_order(f1,f2,f3)   anchors=['practice']
  taught-before-tested: C.f1←s10; C.f2←s10; C.f3←s10

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

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: yield in dependency providers
· constraints.blocked_syntax: Depends(...) inside dependency providers
· constraints.blocked_syntax: app.dependency_overrides[...]
· constraints.blocked_syntax: Session.execute(...)
· constraints.blocked_syntax: Session.rollback(...)
· constraints.blocked_syntax: app.add_middleware(...)
· constraints.blocked_syntax: app.dependency_overrides[...]
· constraints.blocked_syntax: yield in dependency providers
· constraints.blocked_syntax: Depends(..., use_cache=...)
· constraints.blocked_syntax: @app.middleware(...)
· constraints.blocked_syntax: app.add_middleware(...)

=========

# EVALUATOR PACKET — Configuring existing middleware in the request/response stack · Production ASGI serving versus development reload (tile_037)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi.existing_middleware_stack — Configuring existing middleware in the request/response stack
B = fastapi.production_asgi_serving — Production ASGI serving versus development reload

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: remediation step tile_037.r02 is never referenced
  warn: remediation step tile_037.r04 is never referenced

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
QUESTION [choice, intro, grading=client] A is added with app.add_middleware before B. Which wrapper traversal matches this ordering?
  ✔ a: Request: B → A → handler; resulting response: handler → A → B.
      why: Correct. The last middleware added is the outermost wrapper: requests traverse it first, while responses traverse it last.
  ✘ b: Request: A → B → handler; response: handler → B → A.
      why: The later-added B is outermost.
  ✘ c: Request and response both travel B → A → handler.
      why: The resulting response travels back outward through the wrappers.
  feedback✔: Correct. The last middleware added is the outermost wrapper: requests traverse it first, while responses traverse it last.  feedback✘: Recheck the distinction: The last middleware added is the outermost wrapper: requests traverse it first, while responses traverse it last.  hints: ['Trace nested wrappers inward for the request and outward for the response.']  remediation→r01
  MEASURES: A:predict_request_and_response_stack_traversal(f1,f3)   anchors=['assessment:predict_request_and_response_stack_traversal']
  taught-before-tested: A.f1←s01; A.f3←s01

### s04 · hands_on · Practice: Configuring existing middleware in the request/response stack
Apply the contract — Work in the supplied orders-service exercise snapshot.
QUESTION [code_exercise, stretch, grading=client] Configure maintained A first with minimum_size=minimum_size and B second with allowed_hosts=[allowed_host], using app.add_middleware. B is outermost. Add exact comments "# Request: B -> A -> handler" and "# Response: handler -> A -> B". Tests inspect both wrapper configurations and annotations; do not implement middleware.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': ['fastapi', 'starlette']} constraints.allowed=['app.add_middleware(A, option=value)', 'app.add_middleware(B, option=value)', "Keyword arguments using each supplied component's documented option names", 'Python comments for traversal annotations'] blocked=6 items
  file main.py [editable]:
from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware as A
from starlette.middleware.trustedhost import TrustedHostMiddleware as B
app = FastAPI()
minimum_size = 500
allowed_host = 'testserver'
@app.get("/orders")
def orders(): return []
# TODO: add supplied A then B and annotate traversal.

# Supplied inspection of configuration and source annotations, not a custom middleware.
def middleware_inspection(index):
    import pathlib
    source = pathlib.Path("main.py").read_text()
    wrappers = app.user_middleware
    component = wrappers[index]
    return {"class": component.cls.__name__, "options": component.kwargs, "request_annotation": "# Request: B -> A -> handler" in source, "response_annotation": "# Response: handler -> A -> B" in source}

  SOLUTION main.py:
from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware as A
from starlette.middleware.trustedhost import TrustedHostMiddleware as B
app = FastAPI()
minimum_size = 500
allowed_host = 'testserver'
@app.get("/orders")
def orders(): return []
app.add_middleware(A, minimum_size=minimum_size)
app.add_middleware(B, allowed_hosts=[allowed_host])
# Request: B -> A -> handler
# Response: handler -> A -> B

# Supplied inspection of configuration and source annotations, not a custom middleware.
def middleware_inspection(index):
    import pathlib
    source = pathlib.Path("main.py").read_text()
    wrappers = app.user_middleware
    component = wrappers[index]
    return {"class": component.cls.__name__, "options": component.kwargs, "request_annotation": "# Request: B -> A -> handler" in source, "response_annotation": "# Response: handler -> A -> B" in source}

  test t1 (function_call, visible=True): {"function":"middleware_inspection","args":[0],"expected":{"class":"TrustedHostMiddleware","options":{"allowed_hosts":["testserver"]},"request_annotation":true,"response_annotation":true}} | on-fail: The completed implementation does not meet this observable contract.
  test t2 (function_call, visible=True): {"function":"middleware_inspection","args":[1],"expected":{"class":"GZipMiddleware","options":{"minimum_size":500},"request_annotation":true,"response_annotation":true}} | on-fail: The completed implementation does not meet this observable contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"a1e7800d7a111996212767bcc19311db656bf4e962d6c1705e399a44144e5cce","tests_passed":2}
  feedback✔: Correct. The last middleware added is the outermost wrapper: requests traverse it first, while responses traverse it last.  feedback✘: Recheck the distinction: The last middleware added is the outermost wrapper: requests traverse it first, while responses traverse it last.  hints: ['Trace nested wrappers inward for the request and outward for the response.']
  MEASURES: A:predict_request_and_response_stack_traversal(f1,f3)   anchors=['practice', 'assessment:predict_request_and_response_stack_traversal']
  taught-before-tested: A.f1←s01; A.f3←s01

### s05 · explainer · The rule: Production ASGI serving versus development reload
(definition) Run the application with an ASGI server import string, such as uvicorn main:app --host 0.0.0.0 --port 8000, where main names the module and app names its application object. ⟦B.f1 B:tb2⟧
(mechanism) --reload is useful during development but should not be enabled in production because it consumes resources and is less stable. Uvicorn's --workers option starts multiple worker processes and is mutually exclusive with --reload; choose the worker count for the deployment rather than treating reload as process management. ⟦B.f2 B.f3 B:tb3⟧
(walkthrough) Use an ASGI server import string: main:app names module main and application object app. The supplied command selects its host and port without reload. --reload is useful in development, but consumes resources and is less stable, so do not enable it in production. --workers starts multiple processes and is mutually exclusive with --reload; choose worker count for the deployment. ⟦B.f1 B.f2 B.f3 B:tb4⟧
[CODE bash]
uvicorn main:app --host 0.0.0.0 --port 8000
  annotations: ['Use an ASGI server import string: main:app names module main and application object app. The supplied command selects its host and port without reload. --reload is useful in development, but consumes resources and is less stable, so do not enable it in production. --workers starts multiple processes and is mutually exclusive with --reload; choose worker count for the deployment.']

### s06 · check · Choose the distinction: Production ASGI serving versus development reload
Check your understanding — Use the declared contract to distinguish the outcomes.
QUESTION [choice, core, grading=client] A deployment specifies multiple Uvicorn worker processes. Which option combination respects the workers/reload boundary?
  ✔ a: Use --workers with the supplied count and omit --reload.
      why: Correct. Uvicorn's --workers option starts multiple worker processes and is mutually exclusive with --reload; choose the worker count for the deployment rather than treating reload as process management.
  ✘ b: Use --reload as a replacement for worker processes.
      why: Reload is development support, not worker process management.
  ✘ c: Combine --workers and --reload for production.
      why: The two options are mutually exclusive.
  feedback✔: Correct. Uvicorn's --workers option starts multiple worker processes and is mutually exclusive with --reload; choose the worker count for the deployment rather than treating reload as process management.  feedback✘: Recheck the distinction: Uvicorn's --workers option starts multiple worker processes and is mutually exclusive with --reload; choose the worker count for the deployment rather than treating reload as process management.  hints: ['Check the import string and startup evidence separately from development-only options.']  remediation→r03
  MEASURES: B:distinguish_worker_processes_from_development_reload(f3)   anchors=['assessment:distinguish_worker_processes_from_development_reload']
  taught-before-tested: B.f3←s05

### s07 · hands_on · Practice: Production ASGI serving versus development reload
Apply the contract — Work in the supplied orders-service exercise snapshot.
QUESTION [classify, stretch, grading=client] The supplied module main.py defines app; the serving contract is host 0.0.0.0 and port 8000 without reload. Inspect each command AND its startup excerpt. Classify whether it demonstrates that contract. These excerpts are authored inspection fixtures, not verified native process execution.
  'uvicorn main:app --host 0.0.0.0 --port 8000
Supplied startup output: application startup complete; serving on http://0.0.0.0:8000. No reload is enabled.' -> Specified application starts without reload
      feedback: Specified application starts without reload. --reload is useful during development but should not be enabled in production because it consumes resources and is less stable.
  'uvicorn main:app --host 0.0.0.0 --port 8000 --reload
Supplied startup output: reloader process started; serving on http://0.0.0.0:8000.' -> Starts with development-only reload
      feedback: Starts with development-only reload. --reload is useful during development but should not be enabled in production because it consumes resources and is less stable.
  'uvicorn main:missing --host 0.0.0.0 --port 8000
Supplied output: attribute missing not found in module main; application did not start.' -> Specified application was not imported or started
      feedback: Specified application was not imported or started. --reload is useful during development but should not be enabled in production because it consumes resources and is less stable.
  feedback✔: Correct. --reload is useful during development but should not be enabled in production because it consumes resources and is less stable.  feedback✘: Recheck the distinction: --reload is useful during development but should not be enabled in production because it consumes resources and is less stable.  hints: ['Check the import string and startup evidence separately from development-only options.']
  MEASURES: B:identify_reload_as_development_only(f2)   anchors=['practice', 'assessment:identify_reload_as_development_only']
  taught-before-tested: B.f2←s05

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

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: @app.exception_handler(...)