# EVALUATOR PACKET — Application lifespan (tile_018)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi_backend.application_lifespan — Application lifespan

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
[VIDEO ] bridge-before:  | bridge-after: 

### s05 · check · Who owns the client?

### s06 · check · Which side of yield?

### s07 · hands_on · Complete and register lifespan

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

=========

# EVALUATOR PACKET — Orm relationship mapping (tile_019)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi_backend.orm_relationship_mapping — Orm relationship mapping

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
[VIDEO ] bridge-before:  | bridge-after: 

### s04 · check · Interpret the paired relationships

### s05 · hands_on · Map Customer and Order

### s06 · recap · Keep the two declarations distinct
(takeaway) Foreign-key columns describe the stored association; relationship() describes object navigation alongside it. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3⟧
(takeaway) Use mapped_column(ForeignKey(...)) for the reference, and paired back_populates values to name counterpart relationships and establish bidirectional in-Python association behavior. ⟦A.f2 A.f3 A:tb3⟧
[UP NEXT] Declarative field validation constraints: Next: narrow the values admitted by typed model fields.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Stored reference versus paired navigation
(None) Order.customer_id is the database reference; relationship() supplies object navigation alongside that reference. Customer.orders and Order.customer pair through back_populates="customer" and back_populates="orders" respectively. Each names the counterpart attribute to establish bidirectional in-Python association behavior—not merely a table name. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Two kinds of declaration
(None) Declare customer_id with mapped_column(ForeignKey("customers.id")) for the stored association. Separately declare related-object or collection navigation with relationship(). Pair Customer.orders and Order.customer by naming each other with back_populates. A navigation attribute does not replace the stored foreign-key column; the paired names establish bidirectional in-Python association behavior. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Declarative field validation constraints / Nested request-data models (tile_020)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = pydantic.field_constraints — Declarative field validation constraints
B = pydantic.nested_models — Nested request-data models

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
[VIDEO ] bridge-before:  | bridge-after: 

### s05 · check · Check the numeric rule

### s06 · hands_on · Constrain the two fields

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

### s10 · hands_on · Compose Address, LineItem and Order

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