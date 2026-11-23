# EVALUATOR PACKET — Application lifespan (tile_018)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi_backend.application_lifespan — Application lifespan

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (fastapi_backend.application_lifespan)   objective: Own shared resources through lifespan: initialize and close one shared resource.
A.f1: A lifespan context manages initialization before the application takes requests and cleanup after it finishes handling requests.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/events/#lifespan]
A.f2: Define an @asynccontextmanager async function with acquisition before yield and cleanup after yield, and pass it as FastAPI(lifespan=lifespan).   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/events/#lifespan-function]
A.f3: Acquire a shared application-lifetime resource once in lifespan so request handlers can use it without repeating its startup work for each request.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/events/#use-case]
note: Establish this first: Application lifetime owns resources that requests borrow.
note: Stay within the current objective: Own shared resources through lifespan. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine startup and shutdown ownership.
PRACTICE ANCHOR (live_code): Implement and register a lifespan context that initializes one supplied shared-client stand-in before yield and closes it during cleanup.  SUCCESS: The application receives the lifespan function. Entering its context creates one shared client, repeated borrowing within that context uses the same instance, and exiting closes that instance.
ASSESSMENT ANCHOR: determine_application_lifetime_resource_ownership facts=['f1', 'f3']
ASSESSMENT ANCHOR: identify_startup_and_shutdown_sides_of_yield facts=['f1', 'f2']
ASSESSMENT ANCHOR: recognize_lifespan_registration facts=['f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Async-compatible external HTTP requests; Binding request bodies to typed models; Bounded form and multipart file inputs; Bounded in-process background work and nondurable delivery limits; Choosing def versus async def from I/O behavior without blocking the event loop; Composing request dependency graphs; Configuring existing middleware in the request/response stack; Custom validation for domain invariants; Declarative field validation constraints; Depends; Expected API failures with HTTPException; FastAPI application and path-operation declarations; Modular FastAPI application composition with APIRouter; Nested request-data models; Orm relationship mapping; Outbound timeouts; Preventing unsafe outbound requests and SSRF; Production ASGI serving versus development reload; Resource-oriented REST URLs and CRUD contracts; Response-model serialization and private-field exclusion; Separating transport, testable business logic and persistence responsibilities; Structured service request and error logs; Typed path and query input binding; Validated environment-based configuration with fail-fast startup; Yield-based dependency cleanup

## LESSON, in learner order

### s01 · explainer · One owner, several requests
(None) Application lifespan owns the shared client; requests borrow it. Initialization precedes request handling, and cleanup follows it. Define an @asynccontextmanager async function: acquire before yield, clean up after yield, and register it with FastAPI(lifespan=lifespan). Acquire this application-lifetime resource once rather than repeating startup work in each handler. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3⟧
[DIAGRAM: Lifespan encloses the request intervals] nodes=['Application lifetime', 'Acquire SharedClient', 'yield: start handling requests', 'Request-handling period', 'Cleanup: close client', 'Request 1: borrow client', 'Request 2: borrow client', 'Request 3: borrow client'] edges=[('acquire', 'yield', None), ('yield', 'requests', None), ('requests', 'cleanup', None)] alt: One application lifetime encloses acquisition, yield, several request intervals borrowing the same client, and cleanup after request handling.

### s02 · explainer · Application lifetime is the outer interval
(None) Picture one application lifetime enclosing several requests. Acquire SharedClient before those requests; each handler borrows it without repeating startup work. Cleanup belongs after the request-handling period. Repeating acquisition inside each handler instead describes per-request work, not the one-time startup goal. Choose lifespan for a resource intended to have application lifetime; this does not mean every resource should be global. ⟦A.f1 A.f2 A.f3 A:tb4⟧

### s03 · explainer · Trace acquisition and cleanup
(None) In the supplied service, shared_resources holds the client. Acquisition belongs before yield in the async context manager. The yielded interval is the request-handling period; cleanup afterward releases the client when that period finishes. FastAPI(lifespan=lifespan) connects this context to the application. Requests consume the resource, but lifespan owns its startup and cleanup. ⟦A.f1 A.f2 A.f3 A:tb5⟧
(None) Application-lifetime ownership is not per-request acquisition. Sharing this intended application-lifetime client avoids repeated startup work; it is not permission to share every kind of mutable object across requests. ⟦A.f3 A:tb6⟧

### s04 · video · Lifespan review
[VIDEO Application lifetime owns shared resources] bridge-before: Watch how yield separates startup from shutdown. The clip calls this “lifespan events”; Devspace uses “lifespan context.” Its broad recommendation for reusable resources still requires choosing an appropriate application lifetime. | bridge-after: The clip covers timing, the context-manager pattern, and one-time acquisition. The text reinforces the ownership boundary: requests borrow the resource, and not every mutable object is suitable for sharing.
  - NYY6JeqS5h0 92-214s facts=['f1', 'f2', 'f3'] label: Initialize once and clean up with FastAPI lifespan | summary: Lifespan places initialization before the application accepts requests and cleanup after it stops handling them. A resource that takes 30 seconds to load illustrates the difference between repeating startup work for every request and doing it once for subsequent requests to reuse. The example introduces a shared-resource dictionary and an async lifespan function using contextlib's asynccontextmanager. Work before yield belongs to startup; work after yield closes or clears resources during shutdown. Passing the lifespan function to FastAPI connects that context to the application's lifetime.

### s05 · check · Who owns the client?
QUESTION [choice, intro, grading=client] A client is intended to live for the entire application request-handling period. Several handlers borrow it. Which ownership plan meets the one-time startup goal?
  ✔ o1: Acquire once in lifespan before request handling; let handlers borrow it; clean up after request handling.
      why: Lifespan owns startup and cleanup for this intended application-lifetime client.
  ✘ o2: Acquire a fresh client inside every handler invocation.
      why: Per-request acquisition repeats startup work instead of meeting the one-time startup goal.
  ✘ o3: Acquire once in lifespan but close it before the request-handling period starts.
      why: Cleanup follows request handling; closing beforehand does not keep the shared resource available during that period.
  feedback✔: Lifespan owns startup and cleanup for this intended application-lifetime client.  feedback✘: Compare the chosen option with the rule in the prompt; its feedback explains the specific mismatch.  hints: ['Draw the application interval around the requests. Which work belongs outside that interval?']  remediation→r01
  MEASURES: A:determine_application_lifetime_resource_ownership(f1,f3)   anchors=['assessment:determine_application_lifetime_resource_ownership']
  taught-before-tested: A.f1←s01; A.f3←s01

### s06 · check · Which side of yield?
QUESTION [choice, core, grading=client] In an @asynccontextmanager lifespan function, where do acquisition and cleanup belong relative to yield?
  ✘ o1: Acquire after yield and clean up before yield.
      why: Acquisition must precede request handling; this reverses startup and cleanup.
  ✔ o2: Acquire before yield and clean up after yield.
      why: Yield separates initialization from the request-handling interval; cleanup follows that interval.
  ✘ o3: Acquire and close the client before yield.
      why: Closing before yield puts cleanup before the request-handling interval instead of after it.
  feedback✔: Yield separates initialization from the request-handling interval; cleanup follows that interval.  feedback✘: Compare the chosen option with the rule in the prompt; its feedback explains the specific mismatch.  hints: ['Draw the application interval around the requests. Which work belongs outside that interval?']  remediation→r02
  MEASURES: A:identify_startup_and_shutdown_sides_of_yield(f1,f2)   anchors=['assessment:identify_startup_and_shutdown_sides_of_yield']
  taught-before-tested: A.f1←s01; A.f2←s01

### s07 · hands_on · Complete and register lifespan
QUESTION [code_exercise, stretch, grading=client] Complete the marked lifespan section and application construction. Acquire one supplied SharedClient before yield, store it as shared_resources["client"], close that same client after the yielded interval, and register lifespan with FastAPI. Leave the supplied stand-in and observe(borrows) harness unchanged. Its observations must show one construction, repeated borrowing of the same open instance, one close on exit, and registration.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': ['fastapi']} constraints.allowed=['from contextlib import asynccontextmanager', 'from fastapi import FastAPI', '@asynccontextmanager', 'async def lifespan(app):', 'yield', 'try/finally', 'variable assignment', 'dictionary literals and key access', 'SharedClient()', 'client.close()', 'FastAPI(lifespan=lifespan)'] blocked=7 items
  file main.py [editable]:
class SharedClient:
    constructions = 0
    closures = 0

    def __init__(self):
        type(self).constructions += 1
        self.closed = False

    def close(self):
        type(self).closures += 1
        self.closed = True

from contextlib import asynccontextmanager
from fastapi import FastAPI

shared_resources = {}

@asynccontextmanager
async def lifespan(app):
    # TODO: acquire one SharedClient and store it under the key "client".
    # TODO: close that same client during cleanup after yield.
    yield

# TODO: register lifespan when constructing the application.
app = FastAPI()

# Supplied observation harness: do not edit.
import asyncio
async def _observe(borrows):
    SharedClient.constructions = 0
    SharedClient.closures = 0
    shared_resources.clear()
    before = [SharedClient.constructions, SharedClient.closures]
    async with app.router.lifespan_context(app):
        clients = [shared_resources.get("client") for _ in range(borrows)]
        first = clients[0]
        same = first is not None and all(c is first for c in clients)
        during = [SharedClient.constructions, SharedClient.closures]
        closed_during = None if first is None else first.closed
    return {"before": before, "during": during,
            "after": [SharedClient.constructions, SharedClient.closures],
            "borrowed_same": same, "borrows": borrows,
            "closed_during": closed_during,
            "closed_after": None if first is None else first.closed,
            "registered": app.router.lifespan_context is lifespan}
def observe(borrows):
    coroutine = _observe(borrows)
    try:
        coroutine.send(None)
    except StopIteration as done:
        return done.value
    raise RuntimeError("The local stand-in must not suspend for external I/O")

  SOLUTION main.py:
class SharedClient:
    constructions = 0
    closures = 0

    def __init__(self):
        type(self).constructions += 1
        self.closed = False

    def close(self):
        type(self).closures += 1
        self.closed = True

from contextlib import asynccontextmanager
from fastapi import FastAPI

shared_resources = {}

@asynccontextmanager
async def lifespan(app):
    # TODO: acquire one SharedClient and store it under the key "client".
    # TODO: close that same client during cleanup after yield.
    client = SharedClient()
    shared_resources["client"] = client
    try:
        yield
    finally:
        client.close()

# TODO: register lifespan when constructing the application.
app = FastAPI(lifespan=lifespan)

# Supplied observation harness: do not edit.
import asyncio
async def _observe(borrows):
    SharedClient.constructions = 0
    SharedClient.closures = 0
    shared_resources.clear()
    before = [SharedClient.constructions, SharedClient.closures]
    async with app.router.lifespan_context(app):
        clients = [shared_resources.get("client") for _ in range(borrows)]
        first = clients[0]
        same = first is not None and all(c is first for c in clients)
        during = [SharedClient.constructions, SharedClient.closures]
        closed_during = None if first is None else first.closed
    return {"before": before, "during": during,
            "after": [SharedClient.constructions, SharedClient.closures],
            "borrowed_same": same, "borrows": borrows,
            "closed_during": closed_during,
            "closed_after": None if first is None else first.closed,
            "registered": app.router.lifespan_context is lifespan}
def observe(borrows):
    coroutine = _observe(borrows)
    try:
        coroutine.send(None)
    except StopIteration as done:
        return done.value
    raise RuntimeError("The local stand-in must not suspend for external I/O")

  test t0 (function_call, visible=True): {"function":"observe","args":[2],"expected":{"before":[0,0],"during":[1,0],"after":[1,1],"borrowed_same":true,"borrows":2,"closed_during":false,"closed_after":true,"registered":true}} | on-fail: The supplied observation does not meet the declared resource, association, or validation contract.
  test t1 (function_call, visible=True): {"function":"observe","args":[4],"expected":{"before":[0,0],"during":[1,0],"after":[1,1],"borrowed_same":true,"borrows":4,"closed_during":false,"closed_after":true,"registered":true}} | on-fail: The supplied observation does not meet the declared resource, association, or validation contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"037be3b665d11fc13881a8ee069bc7beeeec08c544e106d799de870e5443d171","tests_passed":2}
  feedback✔: The registered lifespan creates one shared client, lends the same open instance during its yielded interval, and closes it on exit.  feedback✘: Check acquisition before yield, cleanup after yield, the shared dictionary entry, and FastAPI lifespan registration.  hints: ['Draw the application interval around the requests. Which work belongs outside that interval?']  remediation→r03
  MEASURES: A:recognize_lifespan_registration(f2)   anchors=['practice', 'assessment:recognize_lifespan_registration']
  taught-before-tested: A.f2←s01

### s08 · recap · Keep ownership explicit
(takeaway) Lifespan initializes before request handling and cleans up afterward. ⟦A.f1 A:tb2⟧
(takeaway) Acquire before yield, clean up after yield, and register with FastAPI(lifespan=lifespan). Intended application-lifetime resources are acquired once and borrowed by handlers. ⟦A.f2 A.f3 A:tb3⟧
[UP NEXT] Orm relationship mapping: Next: distinguish a stored database association from Python object navigation.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Lifespan owns; requests borrow
(None) Initialize the intended application-lifetime SharedClient before request handling and clean it up afterward. Handlers borrow that one resource without repeating its startup work. Contrast this with constructing a client in every handler: that is per-request acquisition, not the shared-lifetime goal. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r02 · Before yield versus after yield
(None) In an @asynccontextmanager async lifespan function, acquisition comes before yield, before the application takes requests. Cleanup comes after yield, after request handling finishes. Register that context with FastAPI(lifespan=lifespan); reversing acquisition and cleanup does not describe this lifetime. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Define the context, then register it
(None) Defining lifespan alone is not registration. Use an @asynccontextmanager async function with client acquisition before yield and cleanup after yield, then pass the function through FastAPI(lifespan=lifespan), rather than leaving the supplied FastAPI() construction unchanged. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: httpx.AsyncClient(...)

=========

# EVALUATOR PACKET — Orm relationship mapping (tile_019)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi_backend.orm_relationship_mapping — Orm relationship mapping

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (fastapi_backend.orm_relationship_mapping)   objective: Map navigation between related entities: map one relationship between existing entities.
A.f1: relationship() maps object navigation between mapped entities, alongside the foreign key columns that represent the association in the database.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#working-with-orm-related-objects]
A.f2: Declare the referencing column with mapped_column(ForeignKey("table.column")) and a related-object or collection attribute with relationship().   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#declaring-mapped-classes, sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#working-with-orm-related-objects]
A.f3: Use back_populates on both relationship attributes to name each other and establish bidirectional in-Python association behavior.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#working-with-orm-related-objects]
note: Establish this first: Object navigation represents a foreign-key-backed association between entities..
note: Stay within the current objective: Map navigation between related entities. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine the association represented by a relationship.
PRACTICE ANCHOR (live_code): Map the Customer–Order association in existing mapped classes: declare Order.customer_id as a foreign key to customers.id and pair Order.customer with Customer.orders using back_populates.  SUCCESS: Order.customer_id references customers.id, Order.customer provides single-object navigation, and Customer.orders provides collection navigation. Each back_populates value names the relationship attribute on the opposite class.
ASSESSMENT ANCHOR: distinguish_stored_foreign_key_from_object_navigation facts=['f1', 'f2']
ASSESSMENT ANCHOR: determine_association_from_paired_relationship_attributes facts=['f1', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Async-compatible external HTTP requests; Binding request bodies to typed models; Bounded form and multipart file inputs; Bounded in-process background work and nondurable delivery limits; CORS origin and credential policy; Choosing def versus async def from I/O behavior without blocking the event loop; Composing request dependency graphs; Configuring existing middleware in the request/response stack; Custom validation for domain invariants; Declarative field validation constraints; Depends; Expected API failures with HTTPException; FastAPI application and path-operation declarations; Modular FastAPI application composition with APIRouter; Nested request-data models; Outbound timeouts; Preventing unsafe outbound requests and SSRF; Production ASGI serving versus development reload; Resource-oriented REST URLs and CRUD contracts; Response-model serialization and private-field exclusion; Separating transport, testable business logic and persistence responsibilities; Structured service request and error logs; Typed path and query input binding; Validated environment-based configuration with fail-fast startup; Yield-based dependency cleanup

## LESSON, in learner order

### s01 · explainer · Stored reference, object navigation
(None) An order’s stored customer reference and its Python navigation are separate declarations. Use mapped_column(ForeignKey("customers.id")) for customer_id and relationship() for related objects or collections. Customer.orders navigates to orders; Order.customer navigates to the customer. Their back_populates values name each other’s relationship attribute, establishing bidirectional in-Python association behavior. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3⟧
[DIAGRAM: Stored reference versus Python navigation] nodes=['orders: stored columns {id; customer_id}', 'customers: stored columns {id}', 'Customer: navigation {orders = relationship(back_populates="customer")}', 'Order: navigation {customer = relationship(back_populates="orders")}'] edges=[('stored_orders', 'stored_customers', 'customer_id: mapped_column(ForeignKey("customers.id"))'), ('customer_object', 'order_object', 'Customer.orders: back_populates="customer"'), ('order_object', 'customer_object', 'Order.customer: back_populates="orders"')] alt: The stored orders.customer_id reference points to customers.id. Separate Customer.orders and Order.customer navigation arrows name each other through back_populates.

### s02 · explainer · Read the counterpart names
(None) Order.customer_id represents the stored reference to customers.id. Order.customer represents navigation to a Customer object, while Customer.orders is the counterpart collection. On Customer.orders, back_populates="customer" names Order.customer; on Order.customer, back_populates="orders" names Customer.orders. These names identify counterpart attributes, not merely tables. The paired relationships establish bidirectional in-Python association behavior; they do not determine every later loading or query behavior. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(None) A relationship attribute does not replace a database foreign-key column. Stored association and object navigation are declared alongside one another. ⟦A.f1 A.f2 A:tb5⟧

### s03 · video · Association mapping review
[VIDEO Foreign-key associations and paired object navigation] bridge-before: Watch how each relationship names its counterpart. The creator’s “syncs the relationships between tables” means paired Python-object association behavior, not immediate database synchronization; single-object navigation alone does not guarantee database uniqueness. | bridge-after: The clip connects foreign keys with object navigation and paired back_populates. It does not explain the exact mapped_column(ForeignKey(...)) declaration; the text supplies that syntax using Customer and Order.
  - aAy-B6KPld8 738-829s facts=['f1', 'f3'] label: Pair relationship attributes with back_populates | summary: The User/UserAuth example uses single-object navigation, while User/posts connects a user with a collection of posts. Both examples pair relationship attributes through back_populates, with each side naming its counterpart. This establishes bidirectional association behavior between Python objects; it does not mean that database tables immediately synchronize. UserPost.userID separately represents the stored association: its foreign key refers to the identifier of a User row. The example also requires userID to have a value. Single-object navigation alone does not establish database uniqueness.

### s04 · check · Interpret the paired relationships
QUESTION [choice, intro, grading=client] Customer.orders and Order.customer are relationship attributes alongside Order.customer_id, a foreign-key column. Which reciprocal back_populates pair names the opposite relationship attributes?
  ✔ o1: Customer.orders names "customer"; Order.customer names "orders".
      why: Each value names the counterpart navigation attribute on the opposite class.
  ✘ o2: Customer.orders names "customer_id"; Order.customer names "id".
      why: These are stored column names, not the counterpart relationship attributes.
  ✘ o3: Customer.orders names "orders"; Order.customer names "customer".
      why: These name the same-side attributes rather than each other.
  feedback✔: Each value names the counterpart navigation attribute on the opposite class.  feedback✘: Compare the chosen option with the rule in the prompt; its feedback explains the specific mismatch.  hints: ['Separate stored identifiers from object navigation, then look at the opposite class.']  remediation→r01
  MEASURES: A:determine_association_from_paired_relationship_attributes(f1,f3)   anchors=['assessment:determine_association_from_paired_relationship_attributes']
  taught-before-tested: A.f1←s01; A.f3←s01

### s05 · hands_on · Map Customer and Order
QUESTION [code_exercise, stretch, grading=client] Complete Customer.orders, Order.customer_id and Order.customer in the existing classes. The stored foreign key must target customers.id; Order.customer must navigate to one Customer and Customer.orders to an Order collection. Set reciprocal back_populates names. Leave Base and the observe(customer_id, order_id) harness unchanged; it inspects declarations and verifies that assigning o.customer places o in c.orders.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': ['sqlalchemy']} constraints.allowed=['from sqlalchemy import ForeignKey', 'from sqlalchemy.orm import Mapped, mapped_column, relationship', 'class Customer(Base):', 'class Order(Base):', '__tablename__ = "customers"', '__tablename__ = "orders"', 'Mapped[int]', 'Mapped["Customer"]', 'Mapped[list["Order"]]', 'mapped_column(primary_key=True)', 'mapped_column(ForeignKey("customers.id"))', 'relationship(back_populates="orders")', 'relationship(back_populates="customer")'] blocked=10 items
  file main.py [editable]:
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    # TODO: declare the orders collection and its counterpart name.

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    # TODO: declare customer_id, customer navigation, and its counterpart name.

# Supplied inspection/association harness: do not edit.
from sqlalchemy import inspect

def observe(customer_id, order_id):
    cm, om = inspect(Customer), inspect(Order)
    c = Customer(id=customer_id)
    o = Order(id=order_id, customer_id=customer_id)
    o.customer = c
    return {"foreign_keys": sorted(f.target_fullname for f in om.columns.customer_id.foreign_keys),
            "order_customer_collection": om.relationships.customer.uselist,
            "customer_orders_collection": cm.relationships.orders.uselist,
            "order_counterpart": om.relationships.customer.back_populates,
            "customer_counterpart": cm.relationships.orders.back_populates,
            "stored_customer_id": o.customer_id,
            "navigation_customer_id": o.customer.id,
            "collection_order_ids": [item.id for item in c.orders],
            "same_customer": o.customer is c}

  SOLUTION main.py:
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    orders: Mapped[list["Order"]] = relationship(back_populates="customer")

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    customer: Mapped["Customer"] = relationship(back_populates="orders")

# Supplied inspection/association harness: do not edit.
from sqlalchemy import inspect

def observe(customer_id, order_id):
    cm, om = inspect(Customer), inspect(Order)
    c = Customer(id=customer_id)
    o = Order(id=order_id, customer_id=customer_id)
    o.customer = c
    return {"foreign_keys": sorted(f.target_fullname for f in om.columns.customer_id.foreign_keys),
            "order_customer_collection": om.relationships.customer.uselist,
            "customer_orders_collection": cm.relationships.orders.uselist,
            "order_counterpart": om.relationships.customer.back_populates,
            "customer_counterpart": cm.relationships.orders.back_populates,
            "stored_customer_id": o.customer_id,
            "navigation_customer_id": o.customer.id,
            "collection_order_ids": [item.id for item in c.orders],
            "same_customer": o.customer is c}

  test t0 (function_call, visible=True): {"function":"observe","args":[1,1],"expected":{"foreign_keys":["customers.id"],"order_customer_collection":false,"customer_orders_collection":true,"order_counterpart":"orders","customer_counterpart":"customer","stored_customer_id":1,"navigation_customer_id":1,"collection_order_ids":[1],"same_customer":true}} | on-fail: The supplied observation does not meet the declared resource, association, or validation contract.
  test t1 (function_call, visible=True): {"function":"observe","args":[2,3],"expected":{"foreign_keys":["customers.id"],"order_customer_collection":false,"customer_orders_collection":true,"order_counterpart":"orders","customer_counterpart":"customer","stored_customer_id":2,"navigation_customer_id":2,"collection_order_ids":[3],"same_customer":true}} | on-fail: The supplied observation does not meet the declared resource, association, or validation contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"4e1afdd8bee68a219094698344f6b71ca8a36c64fb8b6af1217b825d0aad0686","tests_passed":2}
  feedback✔: The foreign-key column stores the association, while reciprocal relationship attributes provide single-object and collection navigation.  feedback✘: Keep the foreign-key column separate from navigation, and name the opposite relationship attribute in each back_populates value.  hints: ['Separate stored identifiers from object navigation, then look at the opposite class.']  remediation→r02
  MEASURES: A:distinguish_stored_foreign_key_from_object_navigation(f1,f2); A:determine_association_from_paired_relationship_attributes(f1,f3)   anchors=['practice', 'assessment:distinguish_stored_foreign_key_from_object_navigation', 'assessment:determine_association_from_paired_relationship_attributes']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f1←s01; A.f3←s01

### s06 · recap · Keep the two declarations distinct
(takeaway) Foreign-key columns describe the stored association; relationship() describes object navigation alongside it. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3⟧
(takeaway) Use mapped_column(ForeignKey(...)) for the reference, and paired back_populates values to name counterpart relationships and establish bidirectional in-Python association behavior. ⟦A.f2 A.f3 A:tb3⟧
[UP NEXT] Declarative field validation constraints: Next: narrow the values admitted by typed model fields.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Stored reference versus paired navigation
(None) Order.customer_id is the database reference; relationship() supplies object navigation alongside that reference. Customer.orders and Order.customer pair through back_populates="customer" and back_populates="orders" respectively. Each names the counterpart attribute to establish bidirectional in-Python association behavior—not merely a table name. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Two kinds of declaration
(None) Declare customer_id with mapped_column(ForeignKey("customers.id")) for the stored association. Separately declare related-object or collection navigation with relationship(). Pair Customer.orders and Order.customer by naming each other with back_populates. A navigation attribute does not replace the stored foreign-key column; the paired names establish bidirectional in-Python association behavior. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: async_sessionmaker()

=========

# EVALUATOR PACKET — Declarative field validation constraints / Nested request-data models (tile_020)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = pydantic.field_constraints — Declarative field validation constraints
B = pydantic.nested_models — Nested request-data models

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (pydantic.field_constraints)   objective: Declare field constraints: constrain one model's fields.
A.f1: Use Field(gt=..., ge=..., lt=..., le=..., multiple_of=...) to enforce exclusive bounds, inclusive bounds and divisibility on numeric values.   [sources: pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/fields/#numeric-constraints]
A.f2: Use Field(min_length=..., max_length=..., pattern=...) to constrain a string's length and regular-expression match.   [sources: pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/fields/#string-constraints]
A.f3: Put Field(...) on a typed model attribute to apply its validation constraints when the model is constructed.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/body-fields/#declare-model-attributes]
note: Establish this first: Constraints narrow acceptable domains.
note: Stay within the current objective: Declare field constraints. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine constraint satisfaction.
PRACTICE ANCHOR (live_code): Constrain an order model so quantity accepts integers from 1 through 20 inclusive and order_reference accepts strings from 3 through 12 characters.  SUCCESS: Both typed attributes carry Field constraints. Construction accepts quantity boundaries 1 and 20 and reference lengths 3 and 12, while rejecting quantities 0 and 21 and reference lengths 2 and 13.
ASSESSMENT ANCHOR: determine_numeric_constraint_satisfaction facts=['f1']
ASSESSMENT ANCHOR: determine_string_constraint_satisfaction facts=['f2']
ASSESSMENT ANCHOR: identify_constraints_applied_at_model_construction facts=['f3']

## SOURCE FACTS — B (pydantic.nested_models)   objective: Compose nested models: define one nested request.
B.f1: A model field annotated with another BaseModel class composes that submodel's validation into the enclosing model.   [sources: pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/models/#nested-models]
B.f2: Declare a nested object with field: Submodel or a collection with field: list[Submodel] to validate the corresponding nested data.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/body-nested-models/#use-the-submodel-as-a-type, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/body-nested-models/#attributes-with-lists-of-submodels]
B.f3: Validation errors locate failed nested fields with a path that can include field names and collection element indexes.   [sources: pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/models/#error-handling]
note: Establish this first: Local contracts compose into a tree.
note: Stay within the current objective: Compose nested models. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine nested validation locations.
PRACTICE ANCHOR (live_code): Define an order request-data model with an address submodel and a list of line-item submodels, then construct it from nested input data.  SUCCESS: Valid nested data constructs the enclosing model. An invalid field in the second line item produces an error location identifying the collection field, index 1, and the failing field.
ASSESSMENT ANCHOR: locate_failed_fields_in_nested_validation facts=['f1', 'f3']
ASSESSMENT ANCHOR: interpret_collection_indexes_in_nested_error_paths facts=['f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Async-compatible external HTTP requests; Binding request bodies to typed models; Bounded form and multipart file inputs; Bounded in-process background work and nondurable delivery limits; CORS origin and credential policy; Choosing def versus async def from I/O behavior without blocking the event loop; Composing request dependency graphs; Configuring existing middleware in the request/response stack; Custom validation for domain invariants; Depends; Endpoint integration tests using TestClient or async HTTPX as appropriate; Expected API failures with HTTPException; FastAPI application and path-operation declarations; Modular FastAPI application composition with APIRouter; Nested request-data models; Outbound timeouts; Preventing unsafe outbound requests and SSRF; Production ASGI serving versus development reload; Request-scoped dependency reuse and lifetime; Resource-oriented REST URLs and CRUD contracts; Response-model serialization and private-field exclusion; Separating transport, testable business logic and persistence responsibilities; Structured service request and error logs; Typed path and query input binding; Validated environment-based configuration with fail-fast startup;

## LESSON, in learner order

### s01 · explainer · Narrow a typed field’s domain
(None) An integer type alone does not express an accepted quantity range. Field uses gt/lt for exclusive bounds, ge/le for inclusive bounds, and multiple_of for divisibility. Strings can use min_length, max_length and pattern for length and regular-expression restrictions. Attach Field(...) to the typed model attribute: its constraints apply when constructing the model. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3⟧
[CODE python]
from pydantic import BaseModel, Field

class Order(BaseModel):
    quantity: int = Field(ge=1, le=20)
    order_reference: str = Field(min_length=3, max_length=12)
from pydantic import ValidationError

# In each group the other field stays valid. Results are computed, not supplied.
def observe():
    results = []
    for quantity in (0, 1, 20, 21):
        data = dict(quantity=quantity, order_reference="REF")
        try:
            Order(**data)
            results.append((data, "constructed"))
        except ValidationError as error:
            results.append((data, error.errors()))
    for length in (2, 3, 12, 13):
        data = dict(quantity=1, order_reference="R" * length)
        try:
            Order(**data)
            results.append((data, "constructed"))
        except ValidationError as error:
            results.append((data, error.errors()))
    return results

if __name__ == "__main__":
    print(observe())

  annotations: ['ge/le express the inclusive quantity bounds.', 'Length bounds constrain this string; no pattern is imposed.', 'Each probe keeps the other field valid.', 'With order_reference valid, construction succeeds for quantities 1 and 20; quantities 0 and 21 fail the inclusive range constraint.', 'With quantity valid, construction succeeds for reference lengths 3 and 12; lengths 2 and 13 fail the length constraints.']

### s02 · explainer · Inspect the boundaries
(None) The supplied quantity rule runs from 1 through 20, inclusive. Check boundary and neighboring inputs with the other field held valid. ge/le include their boundary; gt/lt exclude it. multiple_of would add a divisibility condition. String length and pattern are different restrictions: meeting one does not prove the other. These are construction-time validation constraints, not just documentation. ⟦A.f1 A.f2 A.f3 A:tb4⟧

### s03 · explainer · Translate the rule into Field
(None) For quantity, use Field(ge=1, le=20) on quantity: int to express the inclusive range. If a boundary were excluded, use gt or lt on that side instead. multiple_of adds divisibility without changing the meaning of the bounds. For order_reference: str, Field(min_length=3, max_length=12) expresses the supplied length rule; pattern would express a separate regular-expression restriction. This example imposes no pattern or divisibility requirement. Construction applies the declared constraints. ⟦A.f1 A.f2 A.f3 A:tb5⟧
(None) Do not swap an exclusive bound for an inclusive bound. Work from the rule to the declaration, then inspect the exact boundary values—not just plausible-looking interior values. ⟦A.f1 A:tb6⟧

### s04 · video · Field constraints review
[VIDEO Declare constraints and check accepted values] bridge-before: Watch how Field narrows typed attributes. The first clip uses direct declarations; the second uses Annotated metadata. The second briefly misstates gt, then correctly distinguishes exclusive and inclusive bounds. | bridge-after: The first clip omits numeric constraints and patterns; the text covers both. The second covers bounds and patterns but omits multiple_of; the text supplies divisibility and completes the numeric rule.
  - 9GHxnttXxrA 226-375s facts=['f3'] label: Attach string-length constraints to typed model fields | summary: A Pydantic model inherits from BaseModel and declares title, content and author as string attributes. Type annotations support runtime validation, but a string type alone still admits empty strings. Field narrows the accepted values: title requires 1–100 characters, content requires at least one character, and author requires 1–50 characters. These declarations place the length rules alongside the typed attributes.
  - M81pfi64eeM 2045-2432s facts=['f2', 'f3'] label: Apply numeric bounds, string lengths and patterns | summary: Field constraints can be attached to typed model attributes through Annotated metadata. A user identifier must be greater than zero, a username must contain 3–20 characters, and age must be between 13 and 130 inclusive. The initial description of gt as inclusive is corrected: gt and lt exclude their boundaries, while ge and le include them. String constraints also limit a title to 1–200 characters and require content to contain at least 10 characters. A slug pattern uses beginning and end anchors to require one or more lowercase letters, digits or hyphens. Constructing a user with identifier zero, a two-character username and age 12 produces three validation errors corresponding to those violated constraints.

### s05 · check · Check the numeric rule
QUESTION [choice, intro, grading=client] For quantity: int = Field(ge=1, le=20), with all other fields valid, how should construction treat the two quantity endpoints?
  ✘ o1: Reject both endpoints because bounds are always exclusive.
      why: ge and le include their respective endpoints; gt and lt are the exclusive bounds.
  ✘ o2: Accept the lower endpoint but reject the upper endpoint.
      why: le includes the upper endpoint just as ge includes the lower one.
  ✔ o3: Accept both endpoints.
      why: ge and le express inclusive lower and upper bounds.
  feedback✔: ge and le express inclusive lower and upper bounds.  feedback✘: Compare the chosen option with the rule in the prompt; its feedback explains the specific mismatch.  hints: ['Check the exact boundary, not only an interior value.']  remediation→r01
  MEASURES: A:determine_numeric_constraint_satisfaction(f1)   anchors=['assessment:determine_numeric_constraint_satisfaction']
  taught-before-tested: A.f1←s01

### s06 · hands_on · Constrain the two fields
QUESTION [code_exercise, core, grading=client] Add Field declarations to both typed attributes of Order. Accept quantity from 1 through 20 inclusive and order_reference from 3 through 12 characters, with no additional pattern or divisibility restriction. Leave the supplied observe(quantity, order_reference) harness unchanged. Construction must accept both endpoints and reject immediately outside each range with the other field valid.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': ['pydantic']} constraints.allowed=['from pydantic import BaseModel, Field', 'class Order(BaseModel):', 'int and str attribute annotations', 'Field(gt=..., ge=..., lt=..., le=..., multiple_of=...)', 'Field(min_length=..., max_length=..., pattern=...)', 'integer and string literals', 'Order(quantity=..., order_reference=...)'] blocked=10 items
  file main.py [editable]:
from pydantic import BaseModel, Field

class Order(BaseModel):
    # TODO: quantity from 1 through 20 inclusive.
    quantity: int
    # TODO: order_reference from 3 through 12 characters.
    order_reference: str

# Supplied boundary harness: do not edit.
from pydantic import ValidationError

def observe(quantity, order_reference):
    try:
        model = Order(quantity=quantity, order_reference=order_reference)
        return {"constructed": True, "quantity": model.quantity,
                "order_reference": model.order_reference}
    except ValidationError as error:
        return {"constructed": False, "locations": [list(e["loc"]) for e in error.errors()]}

  SOLUTION main.py:
from pydantic import BaseModel, Field

class Order(BaseModel):
    # TODO: quantity from 1 through 20 inclusive.
    quantity: int = Field(ge=1, le=20)
    # TODO: order_reference from 3 through 12 characters.
    order_reference: str = Field(min_length=3, max_length=12)

# Supplied boundary harness: do not edit.
from pydantic import ValidationError

def observe(quantity, order_reference):
    try:
        model = Order(quantity=quantity, order_reference=order_reference)
        return {"constructed": True, "quantity": model.quantity,
                "order_reference": model.order_reference}
    except ValidationError as error:
        return {"constructed": False, "locations": [list(e["loc"]) for e in error.errors()]}

  test t0 (function_call, visible=True): {"function":"observe","args":[0,"REF"],"expected":{"constructed":false,"locations":[["quantity"]]}} | on-fail: The supplied observation does not meet the declared resource, association, or validation contract.
  test t1 (function_call, visible=True): {"function":"observe","args":[1,"REF"],"expected":{"constructed":true,"quantity":1,"order_reference":"REF"}} | on-fail: The supplied observation does not meet the declared resource, association, or validation contract.
  test t2 (function_call, visible=True): {"function":"observe","args":[20,"REF"],"expected":{"constructed":true,"quantity":20,"order_reference":"REF"}} | on-fail: The supplied observation does not meet the declared resource, association, or validation contract.
  test t3 (function_call, visible=True): {"function":"observe","args":[21,"REF"],"expected":{"constructed":false,"locations":[["quantity"]]}} | on-fail: The supplied observation does not meet the declared resource, association, or validation contract.
  test t4 (function_call, visible=True): {"function":"observe","args":[1,"RR"],"expected":{"constructed":false,"locations":[["order_reference"]]}} | on-fail: The supplied observation does not meet the declared resource, association, or validation contract.
  test t5 (function_call, visible=True): {"function":"observe","args":[1,"RRR"],"expected":{"constructed":true,"quantity":1,"order_reference":"RRR"}} | on-fail: The supplied observation does not meet the declared resource, association, or validation contract.
  test t6 (function_call, visible=True): {"function":"observe","args":[1,"RRRRRRRRRRRR"],"expected":{"constructed":true,"quantity":1,"order_reference":"RRRRRRRRRRRR"}} | on-fail: The supplied observation does not meet the declared resource, association, or validation contract.
  test t7 (function_call, visible=True): {"function":"observe","args":[1,"RRRRRRRRRRRRR"],"expected":{"constructed":false,"locations":[["order_reference"]]}} | on-fail: The supplied observation does not meet the declared resource, association, or validation contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"a3cc4b269a634f4688b55815c955cf15fae321585ce2e5ab48b9a6cc6e8da678","tests_passed":8}
  feedback✔: Both typed attributes carry Field constraints; inclusive quantity and reference-length boundaries pass while immediately outside values fail.  feedback✘: Attach Field to each typed attribute. Do not substitute exclusive bounds for inclusive ones or omit the reference-length constraints.  hints: ['Check the exact boundary, not only an interior value.']  remediation→r02
  MEASURES: A:determine_string_constraint_satisfaction(f2); A:identify_constraints_applied_at_model_construction(f3)   anchors=['practice', 'assessment:determine_string_constraint_satisfaction', 'assessment:identify_constraints_applied_at_model_construction']
  taught-before-tested: A.f2←s01; A.f3←s01

### s07 · explainer · Compose local models
(None) An order can compose smaller models for its address and line items. Annotating address: Address incorporates that submodel’s validation; line_items: list[LineItem] validates the corresponding collection data. Nested validation errors can locate a failed field using enclosing field names and element indexes. Follow the location inward rather than looking only at the order’s outer fields. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3⟧
[CODE python]
from pydantic import BaseModel, ValidationError

class Address(BaseModel):
    street: str

class LineItem(BaseModel):
    product: str
    quantity: int

class Order(BaseModel):
    address: Address
    line_items: list[LineItem]

valid_data = {
    "address": {"street": "7 Sample Lane"},
    "line_items": [
        {"product": "Notebook", "quantity": 1},
        {"product": "Pencil", "quantity": 2},
    ],
}
invalid_data = {
    "address": {"street": "7 Sample Lane"},
    "line_items": [
        {"product": "Notebook", "quantity": 1},
        {"product": "Pencil", "quantity": "not-a-number"},
    ],
}

  annotations: ['Input path: line_items → index 1 → quantity. This is the second item’s invalid quantity, not an outer field.', 'The address field validates the address input with Address.', 'The collection validates its input objects with LineItem.', 'Follow line_items to the second item and then quantity in this input. Error locations can include field names and indexes.']

### s08 · explainer · Follow a nested location
(None) Address declares street; LineItem declares product and quantity. Order composes one Address and a list of LineItem models. In the supplied invalid input, the second item’s quantity is a nonnumeric string. Follow a nested location through line_items, the element index, then quantity to identify that part of the input. Outer-field and nested-field failures both belong to enclosing-model validation, but their locations identify different input parts. ⟦B.f1 B.f2 B.f3 B:tb4⟧
(None) An enclosing Order does not make an invalid nested value acceptable. Each submodel’s validation participates in validation of the enclosing model. ⟦B.f1 B:tb5⟧

### s09 · check · Locate the failed field
QUESTION [choice, core, grading=client] Order uses address: Address and line_items: list[LineItem]. In this input, where does nested validation locate the invalid value?
{
  "address": {
    "street": "7 Sample Lane"
  },
  "line_items": [
    {
      "product": "Notebook",
      "quantity": 1
    },
    {
      "product": "Pencil",
      "quantity": "not-a-number"
    }
  ]
}
  ✔ o1: ('line_items', 1, 'quantity')
      why: The collection path identifies the second item and its failing quantity field.
  ✘ o2: ('address', 'street')
      why: The supplied address street is valid; the nonnumeric value belongs to a line item, not the address.
  ✘ o3: No error: enclosing the data in Order makes nested values acceptable.
      why: Submodel validation participates in enclosing-model validation; an invalid nested value does not become acceptable.
  feedback✔: The collection path identifies the second item and its failing quantity field.  feedback✘: Compare the chosen option with the rule in the prompt; its feedback explains the specific mismatch.  hints: ['Follow the input tree inward: outer field, collection position, then inner field.']  remediation→r03
  MEASURES: B:locate_failed_fields_in_nested_validation(f1,f3)   anchors=['assessment:locate_failed_fields_in_nested_validation']
  taught-before-tested: B.f1←s07; B.f3←s07

### s10 · hands_on · Compose Address, LineItem and Order
QUESTION [code_exercise, stretch, grading=client] Complete Address with street: str and LineItem with product: str and quantity: int. Complete Order with one address submodel and a line_items collection of submodels. Leave observe(data) unchanged. Valid supplied input must construct Order containing Address and LineItem instances and preserve their values. The supplied invalid second item must fail at the collection field, index 1, quantity; the harness returns error locations.
  runtime={'kind': 'python_asgi', 'version': '0.29.5', 'packages': ['pydantic']} constraints.allowed=['from pydantic import BaseModel, ValidationError', 'class declarations inheriting from BaseModel', 'field annotations using str and int', 'field annotations using a declared submodel class', 'list[Submodel] field annotations', 'dictionary, list, string, and integer literals', 'model construction with keyword arguments', 'Model.model_validate(data)', 'variable assignment', 'try and except ValidationError as error', 'error.errors()', 'list indexing and dictionary key access'] blocked=8 items
  file main.py [editable]:
from pydantic import BaseModel, ValidationError

class Address(BaseModel):
    # TODO: street string field.
    pass

class LineItem(BaseModel):
    # TODO: product string and quantity integer fields.
    pass

class Order(BaseModel):
    # TODO: address submodel and line_items collection of submodels.
    pass

# Supplied construction/location harness: do not edit.
def observe(data):
    try:
        model = Order.model_validate(data)
        return {"constructed": True, "address_type": type(model.address).__name__,
                "item_types": [type(i).__name__ for i in model.line_items],
                "street": model.address.street,
                "items": [[i.product, i.quantity] for i in model.line_items]}
    except ValidationError as error:
        return {"constructed": False, "locations": [list(e["loc"]) for e in error.errors()]}

  SOLUTION main.py:
from pydantic import BaseModel, ValidationError

class Address(BaseModel):
    street: str

class LineItem(BaseModel):
    product: str
    quantity: int

class Order(BaseModel):
    address: Address
    line_items: list[LineItem]

# Supplied construction/location harness: do not edit.
def observe(data):
    try:
        model = Order.model_validate(data)
        return {"constructed": True, "address_type": type(model.address).__name__,
                "item_types": [type(i).__name__ for i in model.line_items],
                "street": model.address.street,
                "items": [[i.product, i.quantity] for i in model.line_items]}
    except ValidationError as error:
        return {"constructed": False, "locations": [list(e["loc"]) for e in error.errors()]}

  test t0 (function_call, visible=True): {"function":"observe","args":[{"address":{"street":"7 Sample Lane"},"line_items":[{"product":"Notebook","quantity":1},{"product":"Pencil","quantity":2}]}],"expected":{"constructed":true,"address_type":"Address","item_types":["LineItem","LineItem"],"street":"7 Sample Lane","items":[["Notebook",1],["Pencil",2]]}} | on-fail: The supplied observation does not meet the declared resource, association, or validation contract.
  test t1 (function_call, visible=True): {"function":"observe","args":[{"address":{"street":"7 Sample Lane"},"line_items":[{"product":"Notebook","quantity":1},{"product":"Pencil","quantity":"not-a-number"}]}],"expected":{"constructed":false,"locations":[["line_items",1,"quantity"]]}} | on-fail: The supplied observation does not meet the declared resource, association, or validation contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"35b9bd6e4be13607d9051610e9bcb71b7dea582d9585ad87b2ba32de8c97e22d","tests_passed":2}
  feedback✔: The submodel annotations construct valid nested models and locate the invalid second item at its quantity field.  feedback✘: Use Address for one nested object and list[LineItem] for the collection; their field annotations participate in enclosing validation.  hints: ['Follow the input tree inward: outer field, collection position, then inner field.']  remediation→r04
  MEASURES: B:interpret_collection_indexes_in_nested_error_paths(f2,f3)   anchors=['practice', 'assessment:interpret_collection_indexes_in_nested_error_paths']
  taught-before-tested: B.f2←s07; B.f3←s07

### s11 · recap · Constraints and composition
(takeaway) Field constraints on typed attributes apply during construction. Distinguish inclusive/exclusive bounds, divisibility, string length and pattern. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3⟧
(takeaway) Submodel and list-of-submodel annotations compose nested validation. Error locations identify failed fields using names and collection indexes. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3⟧
[UP NEXT] Resource-oriented REST URLs and CRUD contracts: Next: resource-oriented URLs and CRUD contracts.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Inclusive is not exclusive
(None) The supplied quantity rule includes its endpoints: Field(ge=1, le=20). ge/le include the boundary, whereas gt/lt exclude it. multiple_of adds divisibility as another numeric restriction rather than changing which bound is inclusive. Compare the rule’s exact endpoint with an interior value before choosing a bound. ⟦A.f1 A:tb2 A:tb4 A:tb5 A:tb6⟧
### r02 · Length rule on the typed attribute
(None) For order_reference: str, attach Field(min_length=3, max_length=12) to the attribute so model construction applies the length constraints. pattern would add a regular-expression restriction; length alone is not proof of a pattern match. The supplied example has a length rule only. A typed attribute without this Field declaration does not express that rule. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
### r03 · Read the location inward
(None) Order.address incorporates Address validation, and Order.line_items incorporates LineItem validation. Enclosing the data in Order does not make a bad nested value acceptable. For the supplied nonnumeric quantity, follow the collection name to the second item and then the quantity field; a nested location can include both names and indexes. ⟦B.f1 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r04 · One submodel versus a collection
(None) address: Address validates one nested object; line_items: list[LineItem] validates corresponding collection data. In the supplied invalid input, follow line_items to the second element and its quantity field, not to the address. Nested error locations can use collection element indexes as well as field names. ⟦B.f2 B.f3 B:tb3 B:tb4⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: nested BaseModel attributes
· constraints.blocked_syntax: @field_validator(...)
· constraints.blocked_syntax: @model_validator(...)