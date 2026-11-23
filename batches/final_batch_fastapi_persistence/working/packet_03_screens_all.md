# EVALUATOR PACKET — Retrieve resource / Transaction commit and rollback boundaries (tile_061)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = sqlalchemy.retrieve_resource — Retrieve resource
B = sqlalchemy.transaction_boundaries — Transaction commit and rollback boundaries

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (sqlalchemy.retrieve_resource)   objective: Retrieve a resource through the ORM: retrieve one resource by identity and test the not-found case.
A.f1: Select mapped entities with await session.scalars(select(Entity).where(condition)) and inspect the resulting entity values rather than treating the result as an unbounded application-wide lookup.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-orm, sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#the-select-sql-expression-construct]
A.f2: Use await session.get(Entity, identity) for a primary-key lookup; it returns the identified entity or None when no row exists.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#orm-session-api-documentation, sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#getting-objects-by-primary-key-from-the-identity-map]
A.f3: Add .limit(n) when selecting a bounded number of rows, and explicitly handle an empty result or None as absence.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.GenerativeSelect.limit]
note: Establish this first: A bounded selection maps matching persistent rows to entities; absence is a valid query outcome..
note: Stay within the current objective: Retrieve a resource through the ORM. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Select the intended resource using a bounded query and distinguish a matching row from absence.
PRACTICE ANCHOR (live_code): Retrieve an Order using await session.get(Order, identity), explicitly handle None before accessing entity attributes, and test the lookup with an existing identity and an absent identity.  SUCCESS: The existing identity yields the intended Order entity. The absent identity yields None and follows an explicit absence branch without attribute access.
ASSESSMENT ANCHOR: select_entities_with_a_condition_and_explicit_row_bound facts=['f1', 'f3']
ASSESSMENT ANCHOR: retrieve_an_entity_by_primary_key facts=['f2']
ASSESSMENT ANCHOR: distinguish_matching_entities_from_absence facts=['f1', 'f2', 'f3']

## SOURCE FACTS — B (sqlalchemy.transaction_boundaries)   objective: Choose transaction boundaries: implement one multi-write operation.
B.f1: Use async with session.begin(): around related writes to commit on successful exit and roll back on exceptional exit.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-orm, sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#managing-transactions]
B.f2: A commit makes transaction changes durable, while a rollback discards uncommitted changes; multiple related writes belong in one transaction when they must succeed or fail together.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#working-with-transactions-and-the-dbapi]
B.f3: After a flush failure, explicitly roll back before reusing that session; a failed flush leaves its transactional state requiring recovery.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/session_basics.html#flushing]
note: Establish this first: Related writes succeed or fail together.
note: Stay within the current objective: Choose transaction boundaries. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine commit and rollback effects.
note: The multi-write objective overlaps later persistence-operation concepts, so practice supplies the write helpers and asks learners to implement only transaction grouping and session recovery.
PRACTICE ANCHOR (live_code): Implement one transaction boundary around two supplied asynchronous order-write helpers so that the writes succeed or fail together, without implementing their persistence details.  SUCCESS: Both helper calls run inside the same session.begin() scope. Successful exit commits the pair; an exception escaping the scope rolls back the uncommitted changes. A supplied standalone flush-failure recovery branch explicitly rolls back before session reuse.
ASSESSMENT ANCHOR: determine_commit_and_rollback_effects facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_required_recovery_after_flush_failure facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Basic index selection for actual service queries; Bearer-token extraction into an authentication dependency; Bounded resource listing with stable pagination and filtering; Consistent public error envelopes through exception handlers; Create resource; Delete resource; Diagnose service failures from emitted and interpreted evidence; Documenting expected success and error responses; Freshness policy; Injection-resistant database and input handling; Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels; JWT signature, issuer, audience and expiry verification; Keeping API schemas distinct from persistence entities; Proxy header trust; Redis cache-aside selection and population; Request correlation context across service logs; Safe failure policy; Safe unexpected-error responses with actionable server evidence; Service release and rollback workflow with build, release and run separation; Transaction commit and rollback boundaries; Translating domain and persistence failures at the API boundary; Update resource; Upstream failure translation; Webhook authenticity verification; Webhook req

## LESSON, in learner order

### s01 · explainer · Choose the boundary: Retrieve resource
(mechanism) Use await session.scalars(select(Order).where(condition)) for conditional entity selection. Inspect the returned entities; this is not an unbounded application-wide lookup. ⟦A.f1 A:tb1 A:tb2 A:tb3⟧
(mechanism) For a primary-key identity, await session.get(Order, identity) returns that Order or None if no row exists. ⟦A.f2 A:tb1 A:tb2 A:tb3⟧
(mechanism) Use .limit(n) to bound a selection. Treat an empty selection or None explicitly as absence. ⟦A.f3 A:tb1 A:tb2 A:tb3⟧
[CODE python]
async def by_identity(session, identity):
    entity = await session.get(Order, identity)
    if entity is None:
        return None
    return entity

async def by_condition(session):
    result = await session.scalars(
        select(Order).where(Order.processing == 'queued').limit(3)
    )
    entities = list(result)
    if not entities:
        return []
    return entities
  annotations: ['Identity lookup: handle None before attribute use.', 'Conditional entity selection: bound rows and handle emptiness.']

### s02 · explainer · Trace the distinction: Retrieve resource
(mental_model) An identity lookup and a conditional selection answer different questions. Check None before attributes on an identified Order. For a condition, inspect the entities under the intended limit, including an empty selection. Successful execution does not guarantee a matching row. ⟦A.f1 A.f2 A.f3 A:tb4⟧

### s03 · explainer · Trace the distinction: Retrieve resource
(walkthrough) Trace the registered existing identity 42 and absent identity 999. Then select the registered condition under its row bound. An entity, None and an empty selection need different handling; neither kind of absence is an existing Order. ⟦A.f1 A.f2 A.f3 A:tb5 A:tb6⟧

### s04 · check · Distinguish: Retrieve resource
Check your understanding — 

### s05 · check · Distinguish: Retrieve resource
Check your understanding — 

### s06 · hands_on · Practice: Retrieve resource
Apply the rule — 

### s07 · explainer · Choose the boundary: Transaction commit and rollback boundaries
(mechanism) Wrap related writes in async with session.begin():. Successful exit commits; exceptional exit rolls back. ⟦B.f1 B:tb1 B:tb2 B:tb3⟧
(mechanism) Commit makes changes durable; rollback discards uncommitted changes. Writes required to succeed or fail together belong in one transaction. ⟦B.f2 B:tb1 B:tb2 B:tb3⟧
(mechanism) A failed flush leaves the session needing transactional recovery. Explicitly await session.rollback() before reusing it, even if the error was caught. ⟦B.f3 B:tb1 B:tb2 B:tb3⟧
[PROCESS_FLOW] nodes=['One session.begin() scope', 'first_order_write(session)', 'second_order_write(session)', 'Successful exit: commit; durable pair', 'Exceptional exit: rollback; discard uncommitted changes', 'Separate failed flush', 'Explicit rollback', 'Session reuse'] edges=[('0', '1', None), ('1', '2', None), ('2', '3', 'success'), ('1', '4', 'exception'), ('2', '4', 'exception'), ('5', '6', None), ('6', '7', None)] alt: One session.begin() scope; first_order_write(session); second_order_write(session); Successful exit: commit; durable pair; Exceptional exit: rollback; discard uncommitted changes; Separate failed flush; Explicit rollback; Session reuse

### s08 · explainer · Trace the distinction: Transaction commit and rollback boundaries
(mental_model) The two supplied write helpers share a requirement: succeed or fail together. A caught error does not show whether uncommitted data was discarded or session state recovered. Follow both responsibilities before reuse. ⟦B.f1 B.f2 B.f3 B:tb4⟧

### s09 · explainer · Trace the distinction: Transaction commit and rollback boundaries
(walkthrough) Contrast a completed pair with a failing second write. Successful transaction exit makes the pair durable; exceptional exit discards uncommitted changes. In the separate caught-flush case, await rollback before reuse. Catching the message alone is not recovery. ⟦B.f1 B.f2 B.f3 B:tb5 B:tb6⟧

### s10 · check · Distinguish: Transaction commit and rollback boundaries
Check your understanding — 

### s11 · hands_on · Practice: Transaction commit and rollback boundaries
Apply the rule — 

### s12 · recap · Keep the boundaries clear
(takeaway) Contrast a returned Order with None or an empty conditional result: operation success is not evidence of a match. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(takeaway) Contrast handling an error message with recovering the transaction: catching a failed flush does not make the session reusable. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧
[UP NEXT] Bearer-token extraction into an authentication dependency: Next: tile_063.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try again: select entities with a condition and explicit row bound
(mechanism) Use await session.scalars(select(Order).where(condition)) for conditional entity selection. Inspect the returned entities; this is not an unbounded application-wide lookup. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Use .limit(n) to bound a selection. Treat an empty selection or None explicitly as absence. ⟦A.f3 A:tb3 A:tb4 A:tb5 A:tb6⟧
(misconception) Contrast a returned Order with None or an empty conditional result: operation success is not evidence of a match. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r02 · Try again: distinguish matching entities from absence
(mechanism) Use await session.scalars(select(Order).where(condition)) for conditional entity selection. Inspect the returned entities; this is not an unbounded application-wide lookup. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) For a primary-key identity, await session.get(Order, identity) returns that Order or None if no row exists. ⟦A.f2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(mechanism) Use .limit(n) to bound a selection. Treat an empty selection or None explicitly as absence. ⟦A.f3 A:tb3 A:tb4 A:tb5 A:tb6⟧
(misconception) Contrast a returned Order with None or an empty conditional result: operation success is not evidence of a match. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r03 · Try again: retrieve an entity by primary key
(mechanism) For a primary-key identity, await session.get(Order, identity) returns that Order or None if no row exists. ⟦A.f2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(misconception) Contrast a returned Order with None or an empty conditional result: operation success is not evidence of a match. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r04 · Try again: determine commit and rollback effects
(mechanism) Wrap related writes in async with session.begin():. Successful exit commits; exceptional exit rolls back. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(mechanism) Commit makes changes durable; rollback discards uncommitted changes. Writes required to succeed or fail together belong in one transaction. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(misconception) Contrast handling an error message with recovering the transaction: catching a failed flush does not make the session reusable. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧
### r05 · Try again: identify required recovery after flush failure
(mechanism) A failed flush leaves the session needing transactional recovery. Explicitly await session.rollback() before reusing it, even if the error was caught. ⟦B.f3 B:tb3 B:tb4 B:tb5 B:tb6⟧
(misconception) Contrast handling an error message with recovering the transaction: catching a failed flush does not make the session reusable. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧

=========

# EVALUATOR PACKET — Bearer-token extraction into an authentication dependency (tile_063)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = auth.bearer_dependency — Bearer-token extraction into an authentication dependency

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (auth.bearer_dependency)   objective: Extract bearer credentials from an API request: declare one bearer extraction dependency and verify absent and malformed credentials.
A.f1: A bearer extraction dependency reads a credential from Authorization: Bearer token; receiving the credential does not itself establish that it is valid.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/reference/security/#fastapi.security.HTTPBearer]
A.f2: Declare Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())] on a handler input and read its scheme and credentials fields to obtain the supplied bearer credential.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/reference/security/#fastapi.security.HTTPBearer]
A.f3: With HTTPBearer's default auto_error=True, absent credentials or a non-bearer scheme are rejected instead of supplied to the handler; verify absent and malformed Authorization headers separately.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/reference/security/#fastapi.security.HTTPBearer]
note: Establish this first: Bearer extraction locates credentials; it does not verify their claims or issue tokens..
note: Stay within the current objective: Extract bearer credentials from an API request. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine whether a request supplies a usable bearer credential.
PRACTICE ANCHOR (live_code): Declare one bearer extraction dependency on a handler input, read the supplied scheme and credentials, and separately test absent and malformed Authorization headers with default auto_error=True.  SUCCESS: A nonempty Bearer credential reaches the handler with its scheme and credential text available. An absent header, a non-bearer scheme, and a Bearer header without credential text are each rejected before the handler executes. Extraction is not treated as proof of credential validity.
ASSESSMENT ANCHOR: distinguish_bearer_extraction_from_credential_validity facts=['f1']
ASSESSMENT ANCHOR: declare_and_read_bearer_credentials facts=['f2']
ASSESSMENT ANCHOR: determine_whether_authorization_headers_pass_the_extraction_gate facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Basic index selection for actual service queries; Bounded resource listing with stable pagination and filtering; Bounding payloads, expensive requests and API resource consumption; Consistent public error envelopes through exception handlers; Create resource; Delete resource; Diagnose service failures from emitted and interpreted evidence; Documenting expected success and error responses; Freshness policy; Injection-resistant database and input handling; Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels; JWT signature, issuer, audience and expiry verification; Keeping API schemas distinct from persistence entities; Proxy header trust; Redis cache-aside selection and population; Request correlation context across service logs; Safe failure policy; Safe unexpected-error responses with actionable server evidence; Service release and rollback workflow with build, release and run separation; Translating domain and persistence failures at the API boundary; Update resource; Upstream failure translation; Webhook authenticity verification; Webhook request contracts and acknowledgement 

## LESSON, in learner order

### s01 · explainer · Choose the boundary: Bearer-token extraction into an authentication dependency
(mechanism) HTTPBearer extracts a presented credential from Authorization: Bearer token. Obtaining that credential does not establish validity. ⟦A.f1 A:tb1 A:tb2 A:tb3⟧
(mechanism) On a handler input, declare Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]. Read scheme and credentials for the supplied scheme and token text. ⟦A.f2 A:tb1 A:tb2 A:tb3⟧
(mechanism) With default auto_error=True, missing credentials and non-bearer schemes are rejected before the handler. Test absent and malformed Authorization headers separately. ⟦A.f3 A:tb1 A:tb2 A:tb3⟧
[CODE python]
from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

@app.get("/credential")
def handler(credential: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]):
    scheme = credential.scheme
    token = credential.credentials
    return {"extracted": True}

client.get("/credential", headers={'Authorization': 'Bearer synthetic-token'})

client.get("/credential", headers={})

client.get("/credential", headers={'Authorization': 'Basic synthetic'})

client.get("/credential", headers={'Authorization': 'Bearer'})
  annotations: ['Extract scheme and credential text; do not return or log the token. This does not verify validity.', 'Nonempty Bearer: extraction only.', 'Rejected before handler execution with default auto_error=True.', 'Rejected before handler execution with default auto_error=True.', 'Rejected before handler execution with default auto_error=True.']

### s02 · explainer · Trace the distinction: Bearer-token extraction into an authentication dependency
(mental_model) Trace four inputs separately: nonempty Bearer, absent header, non-bearer scheme, and Bearer without text. Only extraction is being examined. Even when scheme and credentials are available, that text is not proof of valid claims; do not return or log the supplied credential. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧

### s03 · check · Distinguish: Bearer-token extraction into an authentication dependency
Check your understanding — 

### s04 · hands_on · Practice: Bearer-token extraction into an authentication dependency
Apply the rule — 

### s05 · recap · Keep the boundaries clear
(takeaway) Contrast a nonempty Bearer header with an empty Bearer header. Passing extraction still does not verify validity. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Redis cache-aside selection and population: Next: tile_064.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try again: determine whether authorization headers pass the extraction gate
(mechanism) With default auto_error=True, missing credentials and non-bearer schemes are rejected before the handler. Test absent and malformed Authorization headers separately. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) Contrast a nonempty Bearer header with an empty Bearer header. Passing extraction still does not verify validity. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Try again: distinguish bearer extraction from credential validity
(mechanism) HTTPBearer extracts a presented credential from Authorization: Bearer token. Obtaining that credential does not establish validity. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) On a handler input, declare Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]. Read scheme and credentials for the supplied scheme and token text. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) With default auto_error=True, missing credentials and non-bearer schemes are rejected before the handler. Test absent and malformed Authorization headers separately. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) Contrast a nonempty Bearer header with an empty Bearer header. Passing extraction still does not verify validity. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Redis cache-aside selection and population (tile_064)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = cache.redis_cache_aside — Redis cache-aside selection and population

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (cache.redis_cache_aside)   objective: Implement cache-aside retrieval: add cache-aside retrieval to one read endpoint.
A.f1: Cache-aside keeps a cache in front of a primary store; the primary store remains the source of truth rather than the cache becoming authoritative storage.   [sources: redis_docs#https://redis.io/docs/latest/develop/use-cases/cache-aside/#when-to-use-redis-cache-aside]
A.f2: On a read, get the cache key first; on a miss, load from the primary store, cache the result and return it to the caller.   [sources: redis_docs#https://redis.io/docs/latest/develop/use-cases/cache-aside/redis-py/#how-it-works]
A.f3: Cache-aside is useful for read-heavy data where repeated reads can reuse a copy and the application's staleness requirements permit that reuse.   [sources: redis_docs#https://redis.io/docs/latest/develop/use-cases/cache-aside/#when-to-use-redis-cache-aside]
A.f4: Construct the cache key from the identity and parameters of the represented result so requests for different results do not reuse the wrong cached value.   [sources: redis_docs#https://redis.io/docs/latest/develop/use-cases/cache-aside/redis-py/#how-it-works]
note: Establish this first: The cache is a disposable copy and the database remains authoritative.
note: Stay within the current objective: Implement cache-aside retrieval. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Choose cache eligibility and recover a miss from authoritative storage.
PRACTICE ANCHOR (live_code): Add cache-aside retrieval to one order read endpoint. Build a key from the order identity and representation parameter, return a cached result on a hit, and load, cache, and return the primary-store result on a miss.  SUCCESS: An initial read for order 42 loads the primary-store result and populates its cache key. An identical read returns the cached result without another primary-store load. Order 43 and a different representation use distinct keys.
ASSESSMENT ANCHOR: choose_cache_eligible_reads facts=['f3']
ASSESSMENT ANCHOR: recover_cache_miss_from_authoritative_storage facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_results_in_cache_keys facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authoring, reviewing and applying Alembic schema migrations; Basic index selection for actual service queries; Bounded resource listing with stable pagination and filtering; Bounding payloads, expensive requests and API resource consumption; Consistent public error envelopes through exception handlers; Create resource; Delete resource; Diagnose service failures from emitted and interpreted evidence; Documenting expected success and error responses; Freshness policy; Injection-resistant database and input handling; Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels; JWT signature, issuer, audience and expiry verification; Keeping API schemas distinct from persistence entities; Proxy header trust; Recognizing and avoiding redundant ORM queries; Request correlation context across service logs; Safe failure policy; Safe unexpected-error responses with actionable server evidence; Service release and rollback workflow with build, release and run separation; Translating domain and persistence failures at the API boundary; Update resource; Upstream failure translation; Webhook authenticity verification; Webhook request contracts and acknowledgem

## LESSON, in learner order

### s01 · explainer · Choose the boundary: Redis cache-aside selection and population
(mechanism) The cache is a copy in front of the primary store. The primary store, not the cache, remains authoritative. ⟦A.f1 A:tb1 A:tb2 A:tb3⟧
(mechanism) Check the cache key first. On a miss, load the primary-store result, cache it, and return it. ⟦A.f2 A:tb1 A:tb2 A:tb3⟧
(mechanism) Cache-aside suits repeated, read-heavy access when the application permits reuse within its staleness requirements. ⟦A.f3 A:tb1 A:tb2 A:tb3⟧
(mechanism) Build keys from result identity and parameters. Different represented results must not accidentally share a cached value. ⟦A.f4 A:tb1 A:tb2 A:tb3⟧
[PROCESS_FLOW] nodes=['Identity + representation key', 'Cache lookup: disposable copy', 'Return cached copy', 'Load authoritative primary result', 'Populate same cache key', 'Return primary result'] edges=[('0', '1', None), ('1', '2', 'hit'), ('1', '3', 'miss'), ('3', '4', None), ('4', '5', None)] alt: Identity + representation key; Cache lookup: disposable copy; Return cached copy; Load authoritative primary result; Populate same cache key; Return primary result

### s02 · explainer · Trace the distinction: Redis cache-aside selection and population
(mental_model) Order 42 with representation notes and the same order with quantity represent different results. Order 43 differs in identity. Keep their keys distinct. A repeated identical read may reuse its copy under this fixture’s permitted staleness policy; a miss still loads from the authoritative primary store. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · video · Follow the sequence: Redis cache-aside selection and population
[VIDEO ] bridge-before:  | bridge-after: 

### s04 · check · Distinguish: Redis cache-aside selection and population
Check your understanding — 

### s05 · hands_on · Practice: Redis cache-aside selection and population
Apply the rule — 

### s06 · recap · Keep the boundaries clear
(takeaway) Contrast identical represented reads with reads that differ in identity or representation. Only the identical result can reuse that copy. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Authoring, reviewing and applying Alembic schema migrations: Next: tile_065.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try again: distinguish results in cache keys
(mechanism) Build keys from result identity and parameters. Different represented results must not accidentally share a cached value. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast identical represented reads with reads that differ in identity or representation. Only the identical result can reuse that copy. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Try again: choose cache eligible reads
(mechanism) The cache is a copy in front of the primary store. The primary store, not the cache, remains authoritative. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Check the cache key first. On a miss, load the primary-store result, cache it, and return it. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) Cache-aside suits repeated, read-heavy access when the application permits reuse within its staleness requirements. ⟦A.f3 A:tb3 A:tb4⟧
(mechanism) Build keys from result identity and parameters. Different represented results must not accidentally share a cached value. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast identical represented reads with reads that differ in identity or representation. Only the identical result can reuse that copy. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Authoring, reviewing and applying Alembic schema migrations / Basic index selection for actual service queries (tile_065)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = database.alembic_migrations — Authoring, reviewing and applying Alembic schema migrations
B = database.service_query_indexes — Basic index selection for actual service queries

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (database.alembic_migrations)   objective: Manage Alembic migrations: review one reversible migration.
A.f1: Alembic maintains a migration environment and versioned revision scripts that describe schema changes through upgrade() and downgrade().   [sources: alembic_docs#https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment]
A.f2: Generate a candidate revision with alembic revision --autogenerate -m "description", comparing the database schema with supplied target_metadata.   [sources: alembic_docs#https://alembic.sqlalchemy.org/en/latest/autogenerate.html#auto-generating-migrations]
A.f3: Autogeneration produces candidate changes that require manual review and correction; it does not reliably infer every schema intent such as table or column renames.   [sources: alembic_docs#https://alembic.sqlalchemy.org/en/latest/autogenerate.html#auto-generating-migrations]
A.f4: Apply revisions with alembic upgrade head and exercise alembic downgrade revision on a test database to verify a proposed reversal before using it operationally.   [sources: alembic_docs#https://alembic.sqlalchemy.org/en/latest/tutorial.html#running-our-first-migration, alembic_docs#https://alembic.sqlalchemy.org/en/latest/tutorial.html#downgrading]
A.f5: Review an autogenerated drop-and-add pair for a possible rename before applying it; dropping a column deletes the data stored in that column, so an apparent reversal may not recover that data.   [sources: alembic_docs#https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect, postgresql_docs#https://www.postgresql.org/docs/current/ddl-alter.html#DDL-ALTER-REMOVING-A-COLUMN]
note: Establish this first: Versioned migrations explicitly evolve shared schema.
note: Stay within the current objective: Manage Alembic migrations. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Detect unintended schema changes.
PRACTICE ANCHOR (live_code): Review one candidate revision by annotating its upgrade() and downgrade() functions. Flag a proposed drop-and-add pair as a possible rename, explain its data-loss risk, and record the checks required before approval.  SUCCESS: The review flags the potentially unintended drop-and-add pair, explains that recreating a column does not restore deleted data, and requires manual correction and test-database upgrade and downgrade verification before approval.
ASSESSMENT ANCHOR: inspect_candidate_upgrade_and_downgrade_for_unintended_changes facts=['f1', 'f3']
ASSESSMENT ANCHOR: recognize_possible_rename_in_drop_and_add_pair facts=['f3', 'f5']
ASSESSMENT ANCHOR: distinguish_schema_reversal_from_deleted_data_recovery facts=['f4', 'f5']

## SOURCE FACTS — B (database.service_query_indexes)   objective: Select basic indexes: propose indexes for a small workload.
B.f1: An index can speed up access to selected rows but adds overhead, so choose it for a query workload rather than indexing every column automatically.   [sources: postgresql_docs#https://www.postgresql.org/docs/current/indexes.html#INDEXES]
B.f2: PostgreSQL B-tree indexes support equality and ordered comparisons, making them candidates for frequently filtered or ordered values.   [sources: postgresql_docs#https://www.postgresql.org/docs/current/indexes-types.html#INDEXES-TYPES-BTREE]
B.f3: Propose CREATE INDEX name ON table (column) for a frequent lookup, accounting for extra storage and the cost of maintaining the index during writes.   [sources: postgresql_docs#https://www.postgresql.org/docs/current/indexes.html#INDEXES]
note: Establish this first: Indexes trade write and storage cost for access paths.
note: Stay within the current objective: Select basic indexes. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Choose indexes for frequent queries.
PRACTICE ANCHOR (live_code): Propose a basic index for frequent equality lookups on an order's external reference. Write the CREATE INDEX declaration and explain the storage and write-maintenance trade-off.  SUCCESS: The declaration targets the external-reference column, follows CREATE INDEX name ON table (column), and is justified by frequent equality lookups rather than by the column's mere existence. The explanation acknowledges extra storage and maintenance during writes without guaranteeing a performance gain.
ASSESSMENT ANCHOR: choose_indexes_by_query_workload facts=['f1']
ASSESSMENT ANCHOR: identify_b_tree_index_candidates facts=['f2']
ASSESSMENT ANCHOR: propose_index_declarations_with_cost_tradeoffs facts=['f1', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Basic index selection for actual service queries; Bounded resource listing with stable pagination and filtering; Bounding payloads, expensive requests and API resource consumption; Consistent public error envelopes through exception handlers; Create resource; Database test-state isolation; Delete resource; Diagnose service failures from emitted and interpreted evidence; Documenting expected success and error responses; Established authorization-server integration using authorization code and PKCE where applicable; no resource-owner password grant; Freshness policy; Injection-resistant database and input handling; Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels; JWT signature, issuer, audience and expiry verification; Keeping API schemas distinct from persistence entities; Proxy header trust; Recognizing and avoiding redundant ORM queries; Request correlation context across service logs; Safe failure policy; Safe unexpected-error responses with actionable server evidence; Service release and rollback workflow with build, release and run separation; Translating domain and persistence failures at the API boundary; Update resource; Upstre

## LESSON, in learner order

### s01 · explainer · Choose the boundary: Authoring, reviewing and applying Alembic schema migrations
(mechanism) Alembic uses a migration environment and versioned revision scripts. upgrade() and downgrade() describe schema-change directions. ⟦A.f1 A:tb1 A:tb2 A:tb3⟧
(mechanism) Generate a candidate with alembic revision --autogenerate -m "description", comparing the database schema against supplied target_metadata. ⟦A.f2 A:tb1 A:tb2 A:tb3⟧
(mechanism) Review and correct that candidate manually. Autogeneration does not reliably infer every intent, including table or column renames. ⟦A.f3 A:tb1 A:tb2 A:tb3⟧
(mechanism) Apply with alembic upgrade head. Before operational use, test the proposed reversal with alembic downgrade revision on a test database. ⟦A.f4 A:tb1 A:tb2 A:tb3⟧
(mechanism) Inspect drop-and-add for possible rename intent. Dropping a column deletes its data; recreating a column may not recover that data. ⟦A.f5 A:tb1 A:tb2 A:tb3⟧
[CODE python]
def upgrade():
    # Candidate: drop an existing column and add a replacement column.
    # Review: possible rename; clarify intent and correct before approval.
    # Dropping the column deletes its data. No schema changes run here.
    pass

def downgrade():
    # Candidate inverse: drop the replacement and recreate the original column.
    # Review: recreating the column may not recover deleted data.
    # On a test database, verify alembic upgrade head and alembic downgrade revision.
    pass
  annotations: ['Candidate only: review both directions for possible rename intent and data loss; exercise reversal on a test database.']

### s02 · explainer · Trace the distinction: Authoring, reviewing and applying Alembic schema migrations
(mental_model) Compare upgrade and downgrade as reviewed directions, not promises of recovered data. A candidate drop-and-add may conceal a rename. Test the proposed downgrade separately: restoring a schema shape may leave deleted column data unrecovered. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb4 A:tb5⟧

### s03 · check · Distinguish: Authoring, reviewing and applying Alembic schema migrations
Check your understanding — 

### s04 · hands_on · Practice: Authoring, reviewing and applying Alembic schema migrations
Apply the rule — 

### s05 · explainer · Choose the boundary: Basic index selection for actual service queries
(mechanism) An index can speed selected-row access, but adds overhead. Choose for an actual query workload, not automatically for every column. ⟦B.f1 B:tb1 B:tb2 B:tb3⟧
(mechanism) PostgreSQL B-tree indexes support equality and ordered comparisons. Frequently filtered or ordered values are candidates, not guaranteed speedups. ⟦B.f2 B:tb1 B:tb2 B:tb3⟧
(mechanism) For a frequent lookup, propose CREATE INDEX name ON table (column), accounting for extra storage and index maintenance during writes. ⟦B.f3 B:tb1 B:tb2 B:tb3⟧
[CODE sql]
CREATE INDEX orders_external_reference_idx ON orders (external_reference);
  annotations: ['orders_external_reference_idx: index name; orders: table; external_reference: frequent equality-lookup column. Candidate benefit adds storage and write maintenance.']

### s06 · explainer · Trace the distinction: Basic index selection for actual service queries
(mental_model) The fixture workload is frequent equality lookup with ongoing writes on orders.external_reference. A B-tree is a candidate for that equality lookup. Pair the proposed declaration with storage and write-maintenance costs. Merely having a column, or needing an ordered comparison, does not guarantee a particular performance gain. ⟦B.f1 B.f2 B.f3 B:tb4 B:tb5⟧

### s07 · check · Distinguish: Basic index selection for actual service queries
Check your understanding — 

### s08 · check · Distinguish: Basic index selection for actual service queries
Check your understanding — 

### s09 · hands_on · Practice: Basic index selection for actual service queries
Apply the rule — 

### s10 · recap · Keep the boundaries clear
(takeaway) Contrast recreating a dropped column with recovering its deleted data. A reversed schema shape does not necessarily restore values. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Contrast a frequent equality lookup with simply having a column. Workload benefit must be weighed against storage and write overhead. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Keeping API schemas distinct from persistence entities: Next: tile_067.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try again: distinguish schema reversal from deleted data recovery
(mechanism) Apply with alembic upgrade head. Before operational use, test the proposed reversal with alembic downgrade revision on a test database. ⟦A.f4 A:tb3 A:tb4⟧
(mechanism) Inspect drop-and-add for possible rename intent. Dropping a column deletes its data; recreating a column may not recover that data. ⟦A.f5 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast recreating a dropped column with recovering its deleted data. A reversed schema shape does not necessarily restore values. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Try again: inspect candidate upgrade and downgrade for unintended changes
(mechanism) Alembic uses a migration environment and versioned revision scripts. upgrade() and downgrade() describe schema-change directions. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Review and correct that candidate manually. Autogeneration does not reliably infer every intent, including table or column renames. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(mechanism) Inspect drop-and-add for possible rename intent. Dropping a column deletes its data; recreating a column may not recover that data. ⟦A.f5 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast recreating a dropped column with recovering its deleted data. A reversed schema shape does not necessarily restore values. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Try again: choose indexes by query workload
(mechanism) An index can speed selected-row access, but adds overhead. Choose for an actual query workload, not automatically for every column. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(misconception) Contrast a frequent equality lookup with simply having a column. Workload benefit must be weighed against storage and write overhead. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r04 · Try again: identify b tree index candidates
(mechanism) PostgreSQL B-tree indexes support equality and ordered comparisons. Frequently filtered or ordered values are candidates, not guaranteed speedups. ⟦B.f2 B:tb3 B:tb4⟧
(misconception) Contrast a frequent equality lookup with simply having a column. Workload benefit must be weighed against storage and write overhead. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r05 · Try again: propose index declarations with cost tradeoffs
(mechanism) An index can speed selected-row access, but adds overhead. Choose for an actual query workload, not automatically for every column. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(mechanism) For a frequent lookup, propose CREATE INDEX name ON table (column), accounting for extra storage and index maintenance during writes. ⟦B.f3 B:tb3 B:tb4⟧
(misconception) Contrast a frequent equality lookup with simply having a column. Workload benefit must be weighed against storage and write overhead. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧

=========

# EVALUATOR PACKET — Keeping API schemas distinct from persistence entities / Translating domain and persistence failures at the API boundary / Consistent public error envelopes through exception handlers (tile_067)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = design.api_persistence_model_boundaries — Keeping API schemas distinct from persistence entities
B = fastapi.domain_error_translation — Translating domain and persistence failures at the API boundary
C = fastapi.public_error_envelopes — Consistent public error envelopes through exception handlers

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (design.api_persistence_model_boundaries)   objective: Separate API and ORM models: define public schemas around one entity.
A.f1: A persistence model maps stored rows, while a public response model declares the fields clients receive; these are separate contracts even when they describe the same entity.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/response-model/#add-an-output-model, sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#using-orm-declarative-forms-to-define-table-metadata]
A.f2: Define separate public input and output BaseModel classes and use response_model=PublicOutput to prevent persistence-only or sensitive fields from automatically becoming API fields.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/response-model/#add-an-output-model]
A.f3: Use model_config = ConfigDict(from_attributes=True) when a Pydantic public model should validate values from an object's attributes, rather than requiring its persistence class to be the public schema.   [sources: pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/models/#arbitrary-class-instances]
note: Establish this first: Storage and external contracts evolve for different reasons.
note: Stay within the current objective: Separate API and ORM models. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Detect persistence changes leaking into contracts.
PRACTICE ANCHOR (live_code): Define separate public input and output schemas for the supplied order entity, exclude its storage-only processing field, and configure the output schema to validate object attributes.  SUCCESS: Public input and output are distinct BaseModel classes. PublicOutput contains only intended client fields, uses ConfigDict(from_attributes=True), and is selected by the supplied route's response_model. The storage-only processing field is absent from the public output.
ASSESSMENT ANCHOR: detect_storage_fields_leaking_into_public_contracts facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_separate_public_input_and_output_boundaries facts=['f2']
ASSESSMENT ANCHOR: distinguish_attribute_validation_from_field_exposure facts=['f3']

## SOURCE FACTS — B (fastapi.domain_error_translation)   objective: Translate internal failures at the API boundary: translate one storage conflict into a stable API error.
B.f1: Register @app.exception_handler(FailureClass) to translate a recognized internal failure into an intentional public HTTP response.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers]
B.f2: A write conflicting with an existing uniqueness rule can be represented as 409 when that is the API's declared conflict outcome, instead of exposing database exception text.   [sources: rfc_9110_http_semantics#https://www.rfc-editor.org/rfc/rfc9110.html#section-15.5.10, postgresql_docs#https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-UNIQUE-CONSTRAINTS]
B.f3: Recover a failed persistence transaction with rollback and translate the recognized failure at the API boundary rather than treating the failed session as usable or disclosing its internals.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/session_basics.html#flushing, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers]
note: Establish this first: Internal failure types map into public contract semantics.
note: Stay within the current objective: Translate internal failures at the API boundary. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Map a domain or persistence failure into the correct public API outcome.
PRACTICE ANCHOR (live_code): Complete a supplied recognized uniqueness-conflict path: roll back the failed transaction, raise FailureClass, and register an API exception handler that returns the declared 409 outcome with a fixed public message.  SUCCESS: The supplied conflict simulation records rollback before FailureClass is raised. The registered handler returns HTTP 409 with the fixed public message and no database exception text.
ASSESSMENT ANCHOR: map_recognized_failure_to_declared_public_outcome facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_transaction_recovery_from_api_translation facts=['f3']
ASSESSMENT ANCHOR: avoid_disclosing_persistence_failure_details facts=['f2', 'f3']

## SOURCE FACTS — C (fastapi.public_error_envelopes)   objective: Standardize public error envelopes: install an exception handler producing one stable envelope.
C.f1: An exception handler receives the request and exception and can return JSONResponse(status_code=..., content=...) with a stable public error structure.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers]
C.f2: Register the handler for Starlette's HTTPException when both FastAPI and Starlette HTTP exceptions should share the envelope.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/handling-errors/#override-the-httpexception-error-handler]
C.f3: Populate the public envelope with intended client-facing information, not internal stack traces or raw exception details.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html#error-handling]
C.f4: Preserve the recognized exception's status code and relevant headers when constructing the envelope so its body format does not change the underlying HTTP outcome.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/handling-errors/#override-the-httpexception-error-handler]
note: Establish this first: A public error envelope is a versioned contract independent of internal exception classes.
note: Stay within the current objective: Standardize public error envelopes. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Keep expected error bodies consistent without exposing internal exception data.
PRACTICE ANCHOR (live_code): Install a handler for Starlette's HTTPException that returns one stable JSON error envelope containing an intentionally chosen public reason while preserving the exception's status code and relevant headers.  SUCCESS: Expected FastAPI and Starlette HTTP exceptions produce the same body structure, retain their original status codes and relevant headers, and expose neither raw exception details nor stack traces.
ASSESSMENT ANCHOR: register_shared_http_exception_envelope facts=['f1', 'f2']
ASSESSMENT ANCHOR: restrict_envelope_to_public_information facts=['f3']
ASSESSMENT ANCHOR: preserve_error_status_and_relevant_headers facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Bounded resource listing with stable pagination and filtering; Bounding payloads, expensive requests and API resource consumption; Consistent public error envelopes through exception handlers; Create resource; Database test-state isolation; Delete resource; Diagnose service failures from emitted and interpreted evidence; Documenting expected success and error responses; Endpoint authorization with required permissions or scopes; Established authorization-server integration using authorization code and PKCE where applicable; no resource-owner password grant; Freshness policy; Injection-resistant database and input handling; Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels; JWT signature, issuer, audience and expiry verification; Proxy header trust; Recognizing and avoiding redundant ORM queries; Request correlation context across service logs; Safe failure policy; Safe unexpected-error responses with actionable server evidence; Service release and rollback workflow with build, release and run separation; Translating domain and persistence failures at the API boundary; Update resource; Upstream failure translation; Webhook authenticity v

## LESSON, in learner order

### s01 · explainer · Choose the boundary: Keeping API schemas distinct from persistence entities
(mechanism) Persistence models map stored rows; public response models select client-facing fields. These contracts remain separate even for the same entity. ⟦A.f1 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Define separate public input and output BaseModel classes. response_model=PublicOutput keeps persistence-only or sensitive fields from automatically becoming API fields. ⟦A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) For validation from object attributes, use model_config = ConfigDict(from_attributes=True) on the public model. The persistence class need not become the public schema. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[SIDE_BY_SIDE] response_model=PublicOutput selects output fields; from_attributes=True supports validation, not automatic exposure. left_label: Persistence mapping | right_label: Public contracts
  left:
[DIAGRAM] nodes=['Stored Order {id; external_reference; note; quantity; processing}'] edges=[] alt: Stored row fields include storage-only processing and external_reference.
  right:
[DIAGRAM] nodes=['PublicInput {note; quantity}', 'PublicOutput {id; note; quantity}'] edges=[] alt: Separate public input and output omit storage-only fields. PublicOutput may validate attributes with ConfigDict(from_attributes=True).
(walkthrough) The row carries storage-only processing state. Choose separate input and output fields; attribute-based validation does not authorize every attribute to become public. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧

### s02 · check · Distinguish: Keeping API schemas distinct from persistence entities
Check your understanding — 

### s03 · hands_on · Practice: Keeping API schemas distinct from persistence entities
Apply the rule — 

### s04 · explainer · Choose the boundary: Translating domain and persistence failures at the API boundary
(mechanism) Use @app.exception_handler(FailureClass) to translate a recognized internal failure into an intentional public HTTP outcome. ⟦B.f1 B:tb1 B:tb2 B:tb3⟧
(mechanism) For a recognized uniqueness conflict, use 409 when the API declares that conflict outcome. Do not expose database exception text. ⟦B.f2 B:tb1 B:tb2 B:tb3⟧
(mechanism) Roll back a failed persistence transaction before session reuse. Translate the recognized failure at the API boundary without disclosing internals; an HTTP response alone does not recover the session. ⟦B.f3 B:tb1 B:tb2 B:tb3⟧
[PROCESS_FLOW] nodes=['Recognized uniqueness failure', 'Rollback failed transaction before reuse', 'FailureClass at API boundary', 'Registered exception handler', 'Declared HTTP 409: order conflict', 'Database exception text excluded'] edges=[('0', '1', None), ('1', '2', None), ('2', '3', None), ('3', '4', None), ('3', '5', 'public boundary')] alt: Recognized uniqueness failure; Rollback failed transaction before reuse; FailureClass at API boundary; Registered exception handler; Declared HTTP 409: order conflict; Database exception text excluded

### s05 · explainer · Trace the distinction: Translating domain and persistence failures at the API boundary
(mental_model) The fixture declares 409 for its recognized uniqueness conflict and the public reason order conflict. Rollback recovers persistence state; the handler expresses client-facing meaning. Neither responsibility substitutes for the other. Do not classify every write failure as conflict or disclose the private diagnostic. ⟦B.f1 B.f2 B.f3 B:tb4 B:tb5⟧

### s06 · check · Distinguish: Translating domain and persistence failures at the API boundary
Check your understanding — 

### s07 · check · Distinguish: Translating domain and persistence failures at the API boundary
Check your understanding — 

### s08 · hands_on · Practice: Translating domain and persistence failures at the API boundary
Apply the rule — 

### s09 · explainer · Choose the boundary: Consistent public error envelopes through exception handlers
(mechanism) A handler receives request and exception, and can return JSONResponse(status_code=..., content=...) with a stable public error shape. ⟦C.f1 C:tb1 C:tb2 C:tb3⟧
(mechanism) Register for Starlette HTTPException when FastAPI and Starlette HTTP exceptions should share that envelope. ⟦C.f2 C:tb1 C:tb2 C:tb3⟧
(mechanism) Use intended client-facing information in the envelope, not raw exception details or internal stack traces. ⟦C.f3 C:tb1 C:tb2 C:tb3⟧
(mechanism) Keep the recognized status code and relevant headers. Reformatting the body must not change the underlying HTTP outcome. ⟦C.f4 C:tb1 C:tb2 C:tb3⟧
[CODE python]
from starlette.exceptions import HTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def public_http_error(request, exception):
    public_reason = choose_intended_public_reason(exception)
    return JSONResponse(
        status_code=exception.status_code,
        content={'reason': public_reason},
        headers=exception.headers,
    )
  annotations: ['Starlette registration covers both HTTPException families.', 'choose_intended_public_reason is a supplied policy helper, not raw exception text. Preserve recognized status and headers.']

### s10 · explainer · Trace the distinction: Consistent public error envelopes through exception handlers
(mental_model) Compare the registered error cases with and without relevant headers. Changing the body shape must preserve recognized status and metadata. The public reason is intentional client information; an exception’s raw details are not a ready-made public envelope. ⟦C.f1 C.f2 C.f3 C.f4 C:tb4 C:tb5⟧

### s11 · check · Distinguish: Consistent public error envelopes through exception handlers
Check your understanding — 

### s12 · hands_on · Practice: Consistent public error envelopes through exception handlers
Apply the rule — 

### s13 · recap · Keep the boundaries clear
(takeaway) Contrast processing on the stored row with the selected public fields. Attribute validation does not grant field exposure. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Contrast returning the declared conflict response with recovering the failed session. Translation alone is not rollback. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
(takeaway) Contrast a changed public body with changed HTTP metadata. Formatting must preserve recognized status and relevant headers. ⟦C.f1 C.f2 C.f3 C.f4 C:tb2 C:tb3 C:tb4 C:tb5⟧
[UP NEXT] Proxy header trust: Next: tile_070.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try again: detect storage fields leaking into public contracts
(mechanism) Persistence models map stored rows; public response models select client-facing fields. These contracts remain separate even for the same entity. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Define separate public input and output BaseModel classes. response_model=PublicOutput keeps persistence-only or sensitive fields from automatically becoming API fields. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast processing on the stored row with the selected public fields. Attribute validation does not grant field exposure. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Try again: identify separate public input and output boundaries
(mechanism) Define separate public input and output BaseModel classes. response_model=PublicOutput keeps persistence-only or sensitive fields from automatically becoming API fields. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) For validation from object attributes, use model_config = ConfigDict(from_attributes=True) on the public model. The persistence class need not become the public schema. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast processing on the stored row with the selected public fields. Attribute validation does not grant field exposure. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Try again: distinguish transaction recovery from api translation
(mechanism) Roll back a failed persistence transaction before session reuse. Translate the recognized failure at the API boundary without disclosing internals; an HTTP response alone does not recover the session. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) Contrast returning the declared conflict response with recovering the failed session. Translation alone is not rollback. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r04 · Try again: avoid disclosing persistence failure details
(mechanism) For a recognized uniqueness conflict, use 409 when the API declares that conflict outcome. Do not expose database exception text. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Roll back a failed persistence transaction before session reuse. Translate the recognized failure at the API boundary without disclosing internals; an HTTP response alone does not recover the session. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) Contrast returning the declared conflict response with recovering the failed session. Translation alone is not rollback. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r05 · Try again: map recognized failure to declared public outcome
(mechanism) Use @app.exception_handler(FailureClass) to translate a recognized internal failure into an intentional public HTTP outcome. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(mechanism) For a recognized uniqueness conflict, use 409 when the API declares that conflict outcome. Do not expose database exception text. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(misconception) Contrast returning the declared conflict response with recovering the failed session. Translation alone is not rollback. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r06 · Try again: preserve error status and relevant headers
(mechanism) Keep the recognized status code and relevant headers. Reformatting the body must not change the underlying HTTP outcome. ⟦C.f4 C:tb3 C:tb4 C:tb5⟧
(misconception) Contrast a changed public body with changed HTTP metadata. Formatting must preserve recognized status and relevant headers. ⟦C.f1 C.f2 C.f3 C.f4 C:tb2 C:tb3 C:tb4 C:tb5⟧
### r07 · Try again: register shared http exception envelope
(mechanism) A handler receives request and exception, and can return JSONResponse(status_code=..., content=...) with a stable public error shape. ⟦C.f1 C:tb2 C:tb4⟧
(mechanism) Register for Starlette HTTPException when FastAPI and Starlette HTTP exceptions should share that envelope. ⟦C.f2 C:tb3 C:tb4⟧
(mechanism) Use intended client-facing information in the envelope, not raw exception details or internal stack traces. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
(mechanism) Keep the recognized status code and relevant headers. Reformatting the body must not change the underlying HTTP outcome. ⟦C.f4 C:tb3 C:tb4 C:tb5⟧
(misconception) Contrast a changed public body with changed HTTP metadata. Formatting must preserve recognized status and relevant headers. ⟦C.f1 C.f2 C.f3 C.f4 C:tb2 C:tb3 C:tb4 C:tb5⟧

=========

# EVALUATOR PACKET — Proxy header trust (tile_070)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = fastapi_backend.proxy_header_trust — Proxy header trust

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (fastapi_backend.proxy_header_trust)   objective: Trust forwarded metadata only from known proxies: configure one trusted proxy boundary.
A.f1: A TLS-terminating proxy can communicate the original request scheme and client information in forwarded headers, but the application server should trust those headers only from configured proxy sources.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/behind-a-proxy/#proxy-forwarded-headers]
A.f2: Configure --forwarded-allow-ips with the trusted proxy addresses; allowing * trusts all senders and is appropriate only when network access is restricted to trusted proxies.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/behind-a-proxy/#enable-proxy-forwarded-headers]
A.f3: If a proxy strips an external path prefix before forwarding, configure root_path for that prefix so generated API URLs and documentation reflect the external address.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/behind-a-proxy/#proxy-with-a-stripped-path-prefix]
A.f4: Verify redirects and documentation through the public HTTPS proxy address, checking that their scheme and prefix match the externally visible URL rather than the backend's internal address.   [sources: fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/behind-a-proxy/#check-the-responses, fastapi_docs_advanced#https://fastapi.tiangolo.com/advanced/behind-a-proxy/#proxy-with-a-stripped-path-prefix]
note: Establish this first: Forwarded authority derives from the trusted sender, not from a client-supplied header..
note: Stay within the current objective: Trust forwarded metadata only from known proxies. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine whether forwarded metadata may be trusted.
PRACTICE ANCHOR (live_code): Edit an existing application-server launch command to trust only the supplied proxy address and set root_path to /api when that proxy strips the external prefix.  SUCCESS: The launch command explicitly allows only the supplied proxy address and sets /api as the root path. Redirects and documentation checked through the public HTTPS address preserve the external scheme and prefix.
ASSESSMENT ANCHOR: determine_forwarded_metadata_trust_from_sender_and_configuration facts=['f1', 'f2']
ASSESSMENT ANCHOR: evaluate_network_restrictions_before_allowing_wildcard_trust facts=['f2']
ASSESSMENT ANCHOR: verify_external_scheme_and_prefix_in_redirects_and_documentation facts=['f3', 'f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Bounded resource listing with stable pagination and filtering; Bounded retry decisions respecting HTTP idempotency; Bounding payloads, expensive requests and API resource consumption; Create resource; Database test-state isolation; Delete resource; Diagnose service failures from emitted and interpreted evidence; Documenting expected success and error responses; Endpoint authorization with required permissions or scopes; Established authorization-server integration using authorization code and PKCE where applicable; no resource-owner password grant; Freshness policy; Injection-resistant database and input handling; Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels; JWT signature, issuer, audience and expiry verification; Recognizing and avoiding redundant ORM queries; Request correlation context across service logs; Safe failure policy; Safe unexpected-error responses with actionable server evidence; Service release and rollback workflow with build, release and run separation; Update resource; Upstream failure translation; Webhook authenticity verification; Webhook delivery idempotency; Webhook replay freshness; Webhook request contracts

## LESSON, in learner order

### s01 · explainer · Choose the boundary: Proxy header trust
(mechanism) A TLS-terminating proxy can forward original scheme and client information. Accept those headers only from configured trusted proxy sources. ⟦A.f1 A:tb1 A:tb2 A:tb3⟧
(mechanism) Set --forwarded-allow-ips to trusted addresses. The wildcard * trusts every sender and is appropriate only with network access restricted to trusted proxies. ⟦A.f2 A:tb1 A:tb2 A:tb3⟧
(mechanism) If the proxy strips an external prefix, set root_path to that prefix so generated API URLs and documentation reflect the public address. ⟦A.f3 A:tb1 A:tb2 A:tb3⟧
(mechanism) Check redirects and documentation through the public HTTPS proxy URL. Their scheme and prefix should match the external URL, not the internal backend. ⟦A.f4 A:tb1 A:tb2 A:tb3⟧
[DIAGRAM] nodes=['Public HTTPS: https://orders.example.test/api', 'Trusted proxy: 192.0.2.10', 'Internal backend: http://127.0.0.1:8000', "root_path='/api'", 'Public redirects and documentation', 'Untrusted sender: forwarded metadata rejected'] edges=[('0', '1', None), ('1', '2', 'original scheme/client; strip prefix'), ('2', '3', None), ('3', '4', 'external scheme + prefix'), ('5', '2', 'not a trusted source')] alt: Public HTTPS: https://orders.example.test/api; Trusted proxy: 192.0.2.10; Internal backend: http://127.0.0.1:8000; root_path='/api'; Public redirects and documentation; Untrusted sender: forwarded metadata rejected

### s02 · explainer · Trace the distinction: Proxy header trust
(mental_model) The public address is https://orders.example.test/api; the backend address is http://127.0.0.1:8000. Trust the configured source 192.0.2.10, not a familiar header name. The fixture does not restrict network access to trusted proxies, so wildcard trust is not appropriate. Check the public scheme and stripped prefix through redirects and documentation. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Distinguish: Proxy header trust
Check your understanding — 

### s04 · check · Distinguish: Proxy header trust
Check your understanding — 

### s05 · hands_on · Practice: Proxy header trust
Apply the rule — 

### s06 · recap · Keep the boundaries clear
(takeaway) Contrast the configured proxy source with an untrusted sender. Forwarded header names do not establish trust. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Webhook request contracts and acknowledgement behavior: Next: tile_071.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try again: determine forwarded metadata trust from sender and configuration
(mechanism) A TLS-terminating proxy can forward original scheme and client information. Accept those headers only from configured trusted proxy sources. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Set --forwarded-allow-ips to trusted addresses. The wildcard * trusts every sender and is appropriate only with network access restricted to trusted proxies. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast the configured proxy source with an untrusted sender. Forwarded header names do not establish trust. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Try again: evaluate network restrictions before allowing wildcard trust
(mechanism) Set --forwarded-allow-ips to trusted addresses. The wildcard * trusts every sender and is appropriate only with network access restricted to trusted proxies. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast the configured proxy source with an untrusted sender. Forwarded header names do not establish trust. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Try again: verify external scheme and prefix in redirects and documentation
(mechanism) If the proxy strips an external prefix, set root_path to that prefix so generated API URLs and documentation reflect the public address. ⟦A.f3 A:tb3 A:tb4⟧
(mechanism) Check redirects and documentation through the public HTTPS proxy URL. Their scheme and prefix should match the external URL, not the internal backend. ⟦A.f4 A:tb3 A:tb4⟧
(misconception) Contrast the configured proxy source with an untrusted sender. Forwarded header names do not establish trust. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Webhook request contracts and acknowledgement behavior (tile_071)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = integration.webhook_contracts — Webhook request contracts and acknowledgement behavior

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (integration.webhook_contracts)   objective: Define webhook acceptance and acknowledgement behavior: implement one webhook input and acknowledgement contract.
A.f1: Define the webhook's accepted media type, event shape and required fields, and validate the incoming body against that contract before accepting its downstream work.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html#input-validation]
A.f2: A webhook acknowledgment communicates the receiver's accepted delivery outcome; it is not evidence that all downstream business work has completed.   [sources: owasp_api_security_top10_2023#https://docs.stripe.com/webhooks#webhook-endpoint-def]
A.f3: Return the declared 2xx acknowledgment promptly after accepted delivery, and keep slow downstream work out of the acknowledgment path when the integration's contract allows deferred processing.   [sources: owasp_api_security_top10_2023#https://docs.stripe.com/webhooks#webhook-endpoint-def]
A.f4: Declare a typed input model on the webhook handler and status_code on its operation decorator, then verify accepted and invalid input against the intended acknowledgment contract.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/body/#declare-it-as-a-parameter, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/response-status-code/#response-status-code]
note: Establish this first: Acknowledgement communicates delivery acceptance, not necessarily completion of downstream work.
note: Stay within the current objective: Define webhook acceptance and acknowledgement behavior. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Distinguish acceptance and acknowledgement timing from completed side effects.
PRACTICE ANCHOR (live_code): Implement a hypothetical order-event webhook that accepts application/json, validates the contract's required fields through a typed input model, and declares a 202 acknowledgement. Under the supplied contract's permission for deferred processing, keep a bounded downstream task outside the acknowledgement path.  SUCCESS: Accepted order-event input receives the declared 202 acknowledgement; an unsupported media type or invalid body is rejected without scheduling downstream work. The handler schedules permitted deferred work without waiting for its completion, and the acknowledgement makes no claim that business work has finished.
ASSESSMENT ANCHOR: distinguish_validated_delivery_acceptance_from_completed_business_work facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_acknowledgement_timing_when_deferred_processing_is_permitted facts=['f2', 'f3']
ASSESSMENT ANCHOR: verify_accepted_and_invalid_input_against_the_declared_acknowledgement_contract facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Bounded resource listing with stable pagination and filtering; Bounded retry decisions respecting HTTP idempotency; Bounding payloads, expensive requests and API resource consumption; Create resource; Database test-state isolation; Delete resource; Diagnose service failures from emitted and interpreted evidence; Documenting expected success and error responses; Endpoint authorization with required permissions or scopes; Established authorization-server integration using authorization code and PKCE where applicable; no resource-owner password grant; Freshness policy; Injection-resistant database and input handling; Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels; JWT signature, issuer, audience and expiry verification; Object-level authorization against the authenticated principal; Recognizing and avoiding redundant ORM queries; Request correlation context across service logs; Safe failure policy; Safe unexpected-error responses with actionable server evidence; Service release and rollback workflow with build, release and run separation; Update resource; Upstream failure translation; Webhook authenticity verification; Webhook delivery 

## LESSON, in learner order

### s01 · explainer · Choose the boundary: Webhook request contracts and acknowledgement behavior
(mechanism) Declare accepted media type, event shape and required fields. Validate the body against that contract before accepting downstream work. ⟦A.f1 A:tb1 A:tb2 A:tb3⟧
(mechanism) Acknowledgment expresses accepted delivery, not proof that all downstream business work finished. ⟦A.f2 A:tb1 A:tb2 A:tb3⟧
(mechanism) When the integration permits deferred processing, promptly return its declared 2xx after acceptance and keep slow downstream work outside the acknowledgment path. ⟦A.f3 A:tb1 A:tb2 A:tb3⟧
(mechanism) Bind a typed input model and declare status_code on the operation decorator. Verify both accepted and invalid inputs against the acknowledgment contract. ⟦A.f4 A:tb1 A:tb2 A:tb3⟧
[PROCESS_FLOW] nodes=['application/json body: order_id + event', 'Typed-model validation', 'Invalid input: reject', 'Accepted delivery', 'Prompt declared 202 acknowledgment', 'Deferred downstream work'] edges=[('0', '1', None), ('1', '2', 'invalid'), ('1', '3', 'valid'), ('3', '4', None), ('3', '5', 'fixture permits deferral')] alt: Validation precedes accepted delivery. Invalid bodies are rejected. The declared acknowledgment does not depend on completion of permitted deferred work.

### s02 · explainer · Trace the distinction: Webhook request contracts and acknowledgement behavior
(mental_model) This fixture accepts application/json with required order_id and event fields, and permits deferred processing. Its declared acknowledgment is 202. Compare the accepted body with missing or invalid fields. Acceptance, acknowledgment and downstream completion are distinct observations; prompt acknowledgment must not claim finished business work. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Distinguish: Webhook request contracts and acknowledgement behavior
Check your understanding — 

### s04 · hands_on · Practice: Webhook request contracts and acknowledgement behavior
Apply the rule — 

### s05 · recap · Keep the boundaries clear
(takeaway) Contrast accepted delivery with completed downstream work. The declared acknowledgment proves only the former. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Request correlation context across service logs: Next: tile_072.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try again: distinguish validated delivery acceptance from completed business work
(mechanism) Declare accepted media type, event shape and required fields. Validate the body against that contract before accepting downstream work. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Acknowledgment expresses accepted delivery, not proof that all downstream business work finished. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast accepted delivery with completed downstream work. The declared acknowledgment proves only the former. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Try again: identify acknowledgement timing when deferred processing is permitted
(mechanism) Acknowledgment expresses accepted delivery, not proof that all downstream business work finished. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) When the integration permits deferred processing, promptly return its declared 2xx after acceptance and keep slow downstream work outside the acknowledgment path. ⟦A.f3 A:tb3 A:tb4⟧
(mechanism) Bind a typed input model and declare status_code on the operation decorator. Verify both accepted and invalid inputs against the acknowledgment contract. ⟦A.f4 A:tb3 A:tb4⟧
(misconception) Contrast accepted delivery with completed downstream work. The declared acknowledgment proves only the former. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Request correlation context across service logs / Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels (tile_072)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = observability.request_correlation — Request correlation context across service logs
B = observability.service_signal_interpretation — Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (observability.request_correlation)   objective: Propagate request correlation: carry one identifier through an outbound call.
A.f1: Use a nonsensitive interaction identifier to connect records for one request chain rather than reconstructing the chain from timestamps alone.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#event-attributes]
A.f2: Bind the configured correlation header with Header(alias=header_name), keep or create a bounded nonsensitive identifier under the service policy, and send the same identifier with client.get(url, headers={header_name: identifier}).   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/header-params/#declare-header-parameters, fastapi_docs_advanced#https://www.python-httpx.org/async/#making-async-requests]
A.f3: Include the interaction identifier in the local events associated with that request; it provides correlation context, not proof of a caller's authority.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#event-attributes]
A.f4: Verify a local-to-outbound request chain by checking the received header and the related logs, including concurrent requests that must retain distinct correlation contexts.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/testing/#using-testclient, owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#verification]
note: Establish this first: Correlation links related but distinct events.
note: Stay within the current objective: Propagate request correlation. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify broken cross-service correlation.
PRACTICE ANCHOR (live_code): Carry one bounded nonsensitive interaction identifier from an order request through its local events and an outbound call, using the configured correlation header.  SUCCESS: The outbound receiver and related local events contain the same policy-compliant identifier for each order request. Concurrent requests with distinct identifiers retain distinct contexts.
ASSESSMENT ANCHOR: identify_broken_cross_service_correlation facts=['f1', 'f2', 'f4']
ASSESSMENT ANCHOR: distinguish_correlation_context_from_caller_authority facts=['f3']
ASSESSMENT ANCHOR: identify_correlation_context_leakage_between_concurrent_requests facts=['f4']

## SOURCE FACTS — B (observability.service_signal_interpretation)   objective: Interpret request-rate, error-rate and latency signals: interpret one dashboard containing success, failure and delay samples.
B.f1: Request rate measures request events per time interval, while error rate measures failure events per time interval; changing traffic alone can change the absolute error count.   [sources: prometheus_client_python#https://prometheus.io/docs/prometheus/latest/querying/basics/#range-vector-selectors, prometheus_client_python#https://prometheus.github.io/client_python/instrumenting/counter/#constructor]
B.f2: Compute a request rate with rate(request_counter[window]) and a failure fraction with the failure rate divided by the request rate over the same window and label grouping.   [sources: prometheus_client_python#https://prometheus.io/docs/prometheus/latest/querying/functions/#rate, prometheus_client_python#https://prometheus.github.io/client_python/instrumenting/counter/#constructor]
B.f3: Duration observations measure latency independently of event frequency; inspect a histogram-derived latency quantile to distinguish slower responses from simply more requests.   [sources: prometheus_client_python#https://prometheus.github.io/client_python/instrumenting/histogram/#constructor, prometheus_client_python#https://prometheus.io/docs/prometheus/latest/querying/functions/#histogram_quantile]
B.f4: Partition the compared signals by bounded nonsensitive categories such as method, route template and outcome, not by raw caller or request identifiers.   [sources: prometheus_client_python#https://prometheus.github.io/client_python/instrumenting/labels/#main-content]
B.f5: Compare the same time windows and label groups for successful, failing and delayed samples, asking separately whether traffic increased, the failure fraction increased or the duration distribution worsened.   [sources: prometheus_client_python#https://prometheus.io/docs/prometheus/latest/querying/functions/#rate, prometheus_client_python#https://prometheus.github.io/client_python/instrumenting/histogram/#constructor]
note: Establish this first: Signals summarize behavior; labels partition observations without identifying individual users.
note: Stay within the current objective: Interpret request-rate, error-rate and latency signals. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Distinguish traffic changes from error or latency regressions using nonsensitive low-cardinality labels.
PRACTICE ANCHOR (matching): Interpret one dashboard containing successful, failing and delayed request samples. Match each comparison to traffic growth, an increased failure fraction, worsened latency, or no regression, using equal time windows and the same bounded method and route-template groups.  SUCCESS: Correctly identify that 100 requests with 5 failures versus 200 requests with 10 failures represents doubled traffic with an unchanged 5 percent failure fraction; distinguish an increased failure-rate-to-request-rate ratio from a higher histogram-derived latency quantile; and compare outcome partitions within the same window and method/route-template group without using caller or request identifiers.
ASSESSMENT ANCHOR: distinguish_traffic_growth_from_increased_failure_fraction facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_latency_regression_from_increased_request_frequency facts=['f3']
ASSESSMENT ANCHOR: select_bounded_nonsensitive_signal_labels facts=['f4']
ASSESSMENT ANCHOR: compare_signals_using_aligned_windows_and_label_groups facts=['f2', 'f4', 'f5']

## DATA ASSETS USED
ds.service_signals: Equal-window synthetic service dashboard — columns: window(categorical), window_seconds(numerical), method(categorical), route_template(categorical), outcome(categorical), request_count(numerical), failure_count(numerical), partition_count(numerical), request_rate(numerical), failure_rate(numerical), failure_fraction(numerical), latency_p95_seconds(numerical)
   ["baseline",60,"GET","/orders/{order_id}","success",100,5,95,1.6666666666666667,0.08333333333333333,0.05,0.2]
   ["baseline",60,"GET","/orders/{order_id}","failure",100,5,5,1.6666666666666667,0.08333333333333333,0.05,0.2]
   ["traffic_growth",60,"GET","/orders/{order_id}","success",200,10,190,3.3333333333333335,0.16666666666666666,0.05,0.2]
   ["traffic_growth",60,"GET","/orders/{order_id}","failure",200,10,10,3.3333333333333335,0.16666666666666666,0.05,0.2]
   ["increased_failure",60,"GET","/orders/{order_id}","success",100,20,80,1.6666666666666667,0.3333333333333333,0.2,0.2]
   ["increased_failure",60,"GET","/orders/{order_id}","failure",100,20,20,1.6666666666666667,0.3333333333333333,0.2,0.2]
   ["delayed",60,"GET","/orders/{order_id}","success",100,5,95,1.6666666666666667,0.08333333333333333,0.05,1.0]
   ["delayed",60,"GET","/orders/{order_id}","failure",100,5,5,1.6666666666666667,0.08333333333333333,0.05,1.0]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Bounded resource listing with stable pagination and filtering; Bounded retry decisions respecting HTTP idempotency; Bounding payloads, expensive requests and API resource consumption; Create resource; Database test-state isolation; Declaring the deployed bearer-access-token and authorization-server security contract without a password grant; Delete resource; Diagnose service failures from emitted and interpreted evidence; Documenting expected success and error responses; Endpoint authorization with required permissions or scopes; Established authorization-server integration using authorization code and PKCE where applicable; no resource-owner password grant; Freshness policy; Injection-resistant database and input handling; Inspecting generated OpenAPI for drift and sensitive exposure; Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels; JWT signature, issuer, audience and expiry verification; Object-level authorization against the authenticated principal; Recognizing and avoiding redundant ORM queries; Safe failure policy; Safe unexpected-error responses with actionable server evidence; Service release and rollback workflow with build, r

## LESSON, in learner order

### s01 · explainer · Choose the boundary: Request correlation context across service logs
(mechanism) Connect a request chain with a nonsensitive interaction identifier instead of reconstructing it from timestamps alone. ⟦A.f1 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Bind Header(alias=header_name). Under service policy, keep or create a bounded nonsensitive identifier and forward that same value with client.get(url, headers={header_name: identifier}). ⟦A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Include the identifier in related local events. Correlation context is not evidence of caller authority. ⟦A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Check the outbound receiver header and related logs. Concurrent requests must retain distinct correlation contexts. ⟦A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[DIAGRAM] nodes=['Incoming X-Interaction-ID: chain-a', 'Local events: chain-a', 'Outbound receiver X-Interaction-ID: chain-a', 'Incoming X-Interaction-ID: chain-b', 'Local events: chain-b', 'Outbound receiver X-Interaction-ID: chain-b', 'Changed identifier at boundary: broken chain', 'Shared identifier between concurrent chains: mixed context'] edges=[('0', '1', None), ('1', '2', None), ('3', '4', None), ('4', '5', None)] alt: Two concurrent chains retain separate registered identifiers from header through local records to the outbound receiver. Changed boundary values break a chain; shared values mix chains. These identifiers are not authority.
(walkthrough) Compare two concurrent chains. Keep one consistent identifier from incoming header through local events to the receiver, but distinct identifiers between chains. A changed boundary value breaks correlation; accidentally sharing one value mixes contexts. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧

### s02 · check · Distinguish: Request correlation context across service logs
Check your understanding — 

### s03 · hands_on · Practice: Request correlation context across service logs
Apply the rule — 

### s04 · explainer · Choose the boundary: Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels
(mechanism) Request rate counts request events per time interval; error rate counts failures per interval. Traffic changes alone can change absolute failure counts. ⟦B.f1 B:tb1 B:tb2 B:tb3⟧
(mechanism) Use rate(request_counter[window]) for request rate. Divide failure rate by request rate for failure fraction, using the same window and label group. ⟦B.f2 B:tb1 B:tb2 B:tb3⟧
(mechanism) Latency comes from duration observations, independently of frequency. Inspect a histogram-derived quantile to distinguish slower responses from more requests. ⟦B.f3 B:tb1 B:tb2 B:tb3⟧
(mechanism) Group signals by bounded nonsensitive categories such as method, route template and outcome, not raw caller or request identifiers. ⟦B.f4 B:tb1 B:tb2 B:tb3⟧
(mechanism) Align windows and label groups across successful, failing and delayed samples. Ask separately about traffic, failure fraction and worsened duration distribution. ⟦B.f5 B:tb1 B:tb2 B:tb3⟧
[TABLE ds.service_signals cols=['window', 'window_seconds', 'method', 'route_template', 'outcome', 'request_count', 'failure_count', 'partition_count', 'request_rate', 'failure_rate', 'failure_fraction', 'latency_p95_seconds'] ] caption: Equal-window synthetic dashboard. Group totals, rates and latency repeat across outcome rows; do not sum them across partitions. Only partition_count is additive.

### s05 · explainer · Trace the distinction: Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels
(mental_model) Use the registered equal-window dashboard to compare baseline, traffic growth, failing and delayed samples. Request and failure totals describe frequency; failure fraction describes proportion; the histogram-derived quantile describes latency. A rise in absolute failures alone does not establish worse reliability. Match time windows and label groups before comparing. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb4 B:tb5⟧

### s06 · check · Distinguish: Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels
Check your understanding — 

### s07 · hands_on · Practice: Interpret request-rate, error-rate and latency signals with nonsensitive low-cardinality labels
Apply the rule — 

### s08 · recap · Keep the boundaries clear
(takeaway) Contrast one consistent identifier within a chain with one accidentally shared between concurrent chains. Correlation is not caller authority. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Contrast frequency with duration. More requests or absolute failures alone do not establish a higher failure fraction or slower responses. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Bounded resource listing with stable pagination and filtering: Next: tile_074.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try again: identify broken cross service correlation
(mechanism) Connect a request chain with a nonsensitive interaction identifier instead of reconstructing it from timestamps alone. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Bind Header(alias=header_name). Under service policy, keep or create a bounded nonsensitive identifier and forward that same value with client.get(url, headers={header_name: identifier}). ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) Check the outbound receiver header and related logs. Concurrent requests must retain distinct correlation contexts. ⟦A.f4 A:tb3 A:tb4⟧
(misconception) Contrast one consistent identifier within a chain with one accidentally shared between concurrent chains. Correlation is not caller authority. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Try again: distinguish correlation context from caller authority
(mechanism) Include the identifier in related local events. Correlation context is not evidence of caller authority. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(mechanism) Check the outbound receiver header and related logs. Concurrent requests must retain distinct correlation contexts. ⟦A.f4 A:tb3 A:tb4⟧
(misconception) Contrast one consistent identifier within a chain with one accidentally shared between concurrent chains. Correlation is not caller authority. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Try again: select bounded nonsensitive signal labels
(mechanism) Group signals by bounded nonsensitive categories such as method, route template and outcome, not raw caller or request identifiers. ⟦B.f4 B:tb3 B:tb4⟧
(misconception) Contrast frequency with duration. More requests or absolute failures alone do not establish a higher failure fraction or slower responses. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.service_signals cols=['window', 'window_seconds', 'method', 'route_template', 'outcome', 'request_count', 'failure_count', 'partition_count', 'request_rate', 'failure_rate', 'failure_fraction', 'latency_p95_seconds'] ] caption: Use the same synthetic fixture to trace the distinction.
### r04 · Try again: distinguish traffic growth from increased failure fraction
(mechanism) Request rate counts request events per time interval; error rate counts failures per interval. Traffic changes alone can change absolute failure counts. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(mechanism) Use rate(request_counter[window]) for request rate. Divide failure rate by request rate for failure fraction, using the same window and label group. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Latency comes from duration observations, independently of frequency. Inspect a histogram-derived quantile to distinguish slower responses from more requests. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(mechanism) Group signals by bounded nonsensitive categories such as method, route template and outcome, not raw caller or request identifiers. ⟦B.f4 B:tb3 B:tb4⟧
(mechanism) Align windows and label groups across successful, failing and delayed samples. Ask separately about traffic, failure fraction and worsened duration distribution. ⟦B.f5 B:tb3 B:tb4⟧
(misconception) Contrast frequency with duration. More requests or absolute failures alone do not establish a higher failure fraction or slower responses. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.service_signals cols=['window', 'window_seconds', 'method', 'route_template', 'outcome', 'request_count', 'failure_count', 'partition_count', 'request_rate', 'failure_rate', 'failure_fraction', 'latency_p95_seconds'] ] caption: Use the same synthetic fixture to trace the distinction.

=========

# EVALUATOR PACKET — Bounded resource listing with stable pagination and filtering / Injection-resistant database and input handling (tile_074)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = rest.bounded_resource_listing — Bounded resource listing with stable pagination and filtering
B = security.injection_resistant_inputs — Injection-resistant database and input handling

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (rest.bounded_resource_listing)   objective: Design bounded resource listing: implement a filtered paginated collection with deterministic order.
A.f1: Build bounded results with select(Entity).where(predicate).order_by(order_columns).limit(page_size).offset(offset).   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#the-where-clause, sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#order-by, sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.GenerativeSelect.limit]
A.f2: Choose a deterministic ordering with a unique tie-breaker when the primary sort value can repeat, so page boundaries do not depend on unspecified ordering among tied rows.   [sources: postgresql_docs#https://www.postgresql.org/docs/current/queries-limit.html#QUERIES-LIMIT]
A.f3: OFFSET skips the requested number of result rows and LIMIT caps the number returned afterward; use the same filter and unique ordering for the page selections.   [sources: postgresql_docs#https://www.postgresql.org/docs/current/queries-limit.html#QUERIES-LIMIT, sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.GenerativeSelect.offset]
A.f4: Bound accepted page size and offset with declared numeric constraints and compute offset from the requested page contract instead of accepting an unbounded read.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/query-params/#defaults, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/query-params/#required-query-parameters, pydantic_models_docs#https://pydantic.dev/docs/validation/latest/concepts/fields/#numeric-constraints]
note: Establish this first: A listing returns a bounded window over a defined ordered result set.
note: Stay within the current objective: Design bounded resource listing. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Choose stable pagination and filtering without unbounded responses.
PRACTICE ANCHOR (live_code): Complete an orders collection handler using the supplied filter, primary sort column and unique key. Declare bounded pagination inputs, derive the offset from a one-based page contract, and construct a filtered, deterministically ordered, bounded selection.  SUCCESS: The handler accepts only the declared pagination range, computes offset as (page - 1) * page_size, and selects orders with the supplied predicate, primary sort column and unique tie-breaker. Adjacent page requests preserve the filter and ordering.
ASSESSMENT ANCHOR: choose_filtered_bounded_page_selection facts=['f1', 'f3']
ASSESSMENT ANCHOR: choose_consistent_ordering_with_unique_tie_breaker facts=['f2', 'f3']
ASSESSMENT ANCHOR: choose_constrained_pagination_inputs_and_derived_offset facts=['f4']

## SOURCE FACTS — B (security.injection_resistant_inputs)   objective: Bind query values safely: parameterize one unsafe query.
B.f1: Parameterized queries keep SQL structure separate from caller-controlled data instead of interpolating that data into executable SQL text.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html#parameterized-queries]
B.f2: Use a SQLAlchemy expression such as select(Entity).where(Entity.field == supplied_value) so the supplied value becomes a bound value rather than SQL syntax.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#the-where-clause]
B.f3: For a supplied textual query, use text("... WHERE field = :value") with an execute parameter dictionary {"value": supplied_value}, not string formatting or concatenation of the input.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#sending-parameters]
B.f4: Parameters represent data values, not arbitrary table names, column names or sort direction; map a requested structural choice through a defined allowlist when binding a value cannot express it.   [sources: owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html#allow-list-input-validation]
note: Establish this first: Query structure and values remain separate.
note: Stay within the current objective: Bind query values safely. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify unsafe SQL interpolation.
PRACTICE ANCHOR (live_code): Replace interpolation of supplied_value in one textual lookup query with a named placeholder and an execute parameter dictionary.  SUCCESS: The query uses WHERE field = :value, and execution supplies {"value": supplied_value} separately without inserting caller-controlled data into SQL text.
ASSESSMENT ANCHOR: identify_unsafe_sql_interpolation facts=['f1', 'f3']
ASSESSMENT ANCHOR: recognize_bound_query_values facts=['f2', 'f3']
ASSESSMENT ANCHOR: distinguish_value_binding_from_structural_selection facts=['f4']

## DATA ASSETS USED
ds.orders: Synthetic persisted orders — columns: id(identifier,digits-as-label), external_reference(identifier), note(text), quantity(numerical), processing(categorical)
   [42,"ref-42","old note 42",2,"queued"]
   [43,"ref-43","old note 43",2,"queued"]
   [101,"ref-101","target note",3,"queued"]
   [102,"ref-102","other note",3,"queued"]
   [103,"ref-103","third note",3,"queued"]
   [104,"ref-104","fourth note",4,"queued"]
   [105,"ref-105","fifth note",4,"queued"]
   [106,"ref-106","excluded note",1,"held"]
   variant orders.absent_target: 1 ops; planted: 
   variant orders.empty_filter: 1 ops; planted: 
   variant orders.changed_note: 1 ops; planted: 

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authentication and authorization tests including invalid-token rejection; Bounded retry decisions respecting HTTP idempotency; Bounding payloads, expensive requests and API resource consumption; Create resource; Database test-state isolation; Declaring the deployed bearer-access-token and authorization-server security contract without a password grant; Delete resource; Diagnose service failures from emitted and interpreted evidence; Documenting expected success and error responses; Endpoint authorization with required permissions or scopes; Established authorization-server integration using authorization code and PKCE where applicable; no resource-owner password grant; Freshness policy; Injection-resistant database and input handling; Inspecting generated OpenAPI for drift and sensitive exposure; JWT signature, issuer, audience and expiry verification; Object-level authorization against the authenticated principal; Recognizing and avoiding redundant ORM queries; Safe failure policy; Safe unexpected-error responses with actionable server evidence; Service release and rollback workflow with build, release and run separation; Update resource; Upstream failure translation; Webhook auth

## LESSON, in learner order

### s01 · explainer · Choose the boundary: Bounded resource listing with stable pagination and filtering
(mechanism) Build a bounded page with select(Order).where(predicate).order_by(order_columns).limit(page_size).offset(offset). ⟦A.f1 A:tb1 A:tb2 A:tb3⟧
(mechanism) When primary sort values repeat, add a unique tie-breaker for deterministic order rather than leaving ties unspecified. ⟦A.f2 A:tb1 A:tb2 A:tb3⟧
(mechanism) OFFSET skips result rows; LIMIT caps rows returned afterward. Keep the same filter and unique ordering across page selections. ⟦A.f3 A:tb1 A:tb2 A:tb3⟧
(mechanism) Declare numeric limits on accepted page size and offset. Derive offset from the requested page contract rather than permitting an unbounded read. ⟦A.f4 A:tb1 A:tb2 A:tb3⟧
[TABLE computed result ] caption: Ordered page: OFFSET 0, LIMIT 3; quantity ties resolved by id.
  produced by sql: SELECT id, quantity, processing FROM orders WHERE processing = 'queued' ORDER BY quantity, id LIMIT 3 OFFSET 0
[TABLE computed result ] caption: Ordered page: OFFSET 3, LIMIT 3; quantity ties resolved by id.
  produced by sql: SELECT id, quantity, processing FROM orders WHERE processing = 'queued' ORDER BY quantity, id LIMIT 3 OFFSET 3

### s02 · explainer · Trace the distinction: Bounded resource listing with stable pagination and filtering
(mental_model) The fixture filters processing by queued, orders by quantity and breaks ties with id. Keep that predicate and order on adjacent pages. At page size 3, the next page skips that many result rows before returning a bounded window. Derive the offset from the page contract and enforce its declared ceiling. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Distinguish: Bounded resource listing with stable pagination and filtering
Check your understanding — 

### s04 · hands_on · Practice: Bounded resource listing with stable pagination and filtering
Apply the rule — 

### s05 · explainer · Choose the boundary: Injection-resistant database and input handling
(mechanism) Keep SQL structure separate from caller data through parameterization. Do not interpolate caller values into executable query text. ⟦B.f1 B:tb1 B:tb2 B:tb3⟧
(mechanism) In select(Entity).where(Entity.field == supplied_value), the supplied value is bound data, not SQL syntax. ⟦B.f2 B:tb1 B:tb2 B:tb3⟧
(mechanism) For textual SQL, use text("... WHERE field = :value") and execute with {"value": supplied_value}. Do not concatenate or format the input into SQL. ⟦B.f3 B:tb1 B:tb2 B:tb3⟧
(mechanism) Parameters stand for data values, not arbitrary tables, columns or sort directions. Map requested structural choices through a defined allowlist. ⟦B.f4 B:tb1 B:tb2 B:tb3⟧
[CODE python]
# Unsafe: supplied data becomes executable query text.
unsafe = "SELECT field FROM Entity WHERE field = '" + supplied_value + "'"

# Replacement: fixed structure and a separate bound value.
statement = text("SELECT field FROM Entity WHERE field = :value")
result = await session.execute(statement, {"value": supplied_value})
  annotations: ['Do not execute the unsafe interpolation.', 'The placeholder binds data, not arbitrary SQL structure.']

### s06 · explainer · Trace the distinction: Injection-resistant database and input handling
(mental_model) A quote or SQL-looking phrase in supplied data remains a value when bound. A requested sort direction is different: it chooses structure and needs an allowlist. Do not assume a placeholder can express arbitrary SQL identifiers or direction. ⟦B.f1 B.f2 B.f3 B.f4 B:tb4 B:tb5⟧

### s07 · check · Distinguish: Injection-resistant database and input handling
Check your understanding — 

### s08 · hands_on · Practice: Injection-resistant database and input handling
Apply the rule — 

### s09 · recap · Keep the boundaries clear
(takeaway) Contrast a repeated primary sort value with the unique tie-breaker. LIMIT bounds the window after OFFSET skips rows. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Contrast caller data with a requested SQL structural choice. Bind the value; allowlist the structural choice. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Create resource: Next: tile_076.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try again: choose constrained pagination inputs and derived offset
(mechanism) Declare numeric limits on accepted page size and offset. Derive offset from the requested page contract rather than permitting an unbounded read. ⟦A.f4 A:tb3 A:tb4⟧
(misconception) Contrast a repeated primary sort value with the unique tie-breaker. LIMIT bounds the window after OFFSET skips rows. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.orders cols=['id', 'external_reference', 'note', 'quantity', 'processing'] ] caption: Use the same synthetic fixture to trace the distinction.
### r02 · Try again: choose filtered bounded page selection
(mechanism) Build a bounded page with select(Order).where(predicate).order_by(order_columns).limit(page_size).offset(offset). ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) When primary sort values repeat, add a unique tie-breaker for deterministic order rather than leaving ties unspecified. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) OFFSET skips result rows; LIMIT caps rows returned afterward. Keep the same filter and unique ordering across page selections. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(mechanism) Declare numeric limits on accepted page size and offset. Derive offset from the requested page contract rather than permitting an unbounded read. ⟦A.f4 A:tb3 A:tb4⟧
(misconception) Contrast a repeated primary sort value with the unique tie-breaker. LIMIT bounds the window after OFFSET skips rows. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.orders cols=['id', 'external_reference', 'note', 'quantity', 'processing'] ] caption: Use the same synthetic fixture to trace the distinction.
### r03 · Try again: distinguish value binding from structural selection
(mechanism) Parameters stand for data values, not arbitrary tables, columns or sort directions. Map requested structural choices through a defined allowlist. ⟦B.f4 B:tb3 B:tb4 B:tb5⟧
(misconception) Contrast caller data with a requested SQL structural choice. Bind the value; allowlist the structural choice. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r04 · Try again: identify unsafe sql interpolation
(mechanism) Keep SQL structure separate from caller data through parameterization. Do not interpolate caller values into executable query text. ⟦B.f1 B:tb2 B:tb4⟧
(mechanism) In select(Entity).where(Entity.field == supplied_value), the supplied value is bound data, not SQL syntax. ⟦B.f2 B:tb3 B:tb4⟧
(mechanism) For textual SQL, use text("... WHERE field = :value") and execute with {"value": supplied_value}. Do not concatenate or format the input into SQL. ⟦B.f3 B:tb3 B:tb4⟧
(misconception) Contrast caller data with a requested SQL structural choice. Bind the value; allowlist the structural choice. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧

=========

# EVALUATOR PACKET — Create resource / Delete resource / Update resource (tile_076)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = sqlalchemy.create_resource — Create resource
B = sqlalchemy.delete_resource — Delete resource
C = sqlalchemy.update_resource — Update resource

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (sqlalchemy.create_resource)   objective: Create a resource through the ORM: insert one mapped resource and verify its stored state.
A.f1: Construct Entity(field=value, ...) with the supplied fields and call session.add(entity) to put a new entity into the pending insert state.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-orm, sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#instances-of-classes-represent-rows]
A.f2: await session.flush() emits the pending insert and assigns database-generated identity values back to the mapped entity when supported by its mapping and database.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#flushing, sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#orm-session-api-documentation]
A.f3: Commit the successful creation with await session.commit() or a successfully exiting session.begin() context; a flush alone is not a commit.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-orm, sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#managing-transactions]
A.f4: Verify the generated identity and committed field values with await fresh_session.get(Entity, identity) in an independent session rather than checking only that a Python object was constructed.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#orm-session-api-documentation, sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#getting-objects-by-primary-key-from-the-identity-map]
note: Establish this first: A newly constructed entity becomes a persistent row when the session flushes its insert..
note: Stay within the current objective: Create a resource through the ORM. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Persist a new mapped entity with the supplied fields and verify its generated persistent identity.
PRACTICE ANCHOR (live_code): Construct one mapped order entity with the supplied fields, add it to the session, flush to obtain its generated identity, commit, and retrieve it in an independent session to verify its stored fields.  SUCCESS: An independent session retrieves the committed order by its generated identity, and its identity and supplied field values match the expected values.
ASSESSMENT ANCHOR: construct_and_register_new_entity facts=['f1']
ASSESSMENT ANCHOR: obtain_generated_identity_and_commit_creation facts=['f2', 'f3']
ASSESSMENT ANCHOR: verify_committed_identity_and_fields_in_independent_session facts=['f4']

## SOURCE FACTS — B (sqlalchemy.delete_resource)   objective: Delete a resource through the ORM: delete one identified resource and verify its absence.
B.f1: Load the intended entity with await session.get(Entity, identity) and handle None as absence before attempting deletion.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#orm-session-api-documentation, sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#getting-objects-by-primary-key-from-the-identity-map]
B.f2: await session.delete(entity) marks that persistent entity for removal, and flushing emits the row deletion.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#orm-session-api-documentation, sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#deleting-orm-objects-using-the-unit-of-work-pattern]
B.f3: Commit the successful deletion under the transaction contract and roll back a failed deletion instead of reporting an uncommitted removal as durable.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#managing-transactions, sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-orm]
B.f4: Verify deletion with a fresh primary-key lookup or independent session, asserting absence and that the intended identity, not another row, was removed.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#deleting-orm-objects-using-the-unit-of-work-pattern, sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#orm-session-api-documentation]
note: Establish this first: An ORM deletion schedules removal of the identified persistent row at flush..
note: Stay within the current objective: Delete a resource through the ORM. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Remove the intended persistent resource and verify it is no longer retrievable.
PRACTICE ANCHOR (live_code): Delete one identified order through an async ORM session, handle an absent target without attempting deletion, and verify committed absence through an independent session.  SUCCESS: The target order is absent after successful commitment, a second order remains retrievable, an absent target is handled before deletion, and a failed deletion is rolled back rather than reported as successful.
ASSESSMENT ANCHOR: identify_target_and_handle_absence facts=['f1']
ASSESSMENT ANCHOR: complete_durable_deletion_with_failure_rollback facts=['f2', 'f3']
ASSESSMENT ANCHOR: verify_target_absence_and_other_row_preservation facts=['f4']

## SOURCE FACTS — C (sqlalchemy.update_resource)   objective: Update a resource through the ORM: update one existing resource and verify changed and preserved fields.
C.f1: Assign new values to attributes of a loaded persistent entity; the session tracks those changes and emits an UPDATE when it flushes.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#updating-orm-objects-using-the-unit-of-work-pattern]
C.f2: Obtain supplied changes with model_dump(exclude_unset=True) and assign only those permitted fields to the loaded entity so omitted values are preserved.   [sources: fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/body-updates/#using-pydantics-exclude-unset-parameter]
C.f3: Commit the successful update under the transaction contract and roll back a failed update before further session use.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-orm, sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#managing-transactions]
C.f4: Reload the committed entity in an independent session and verify both the changed supplied fields and the unchanged omitted fields, rather than inspecting only the request model.   [sources: sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#updating-orm-objects-using-the-unit-of-work-pattern, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/testing/#using-testclient]
note: Establish this first: Changing a persistent entity records a row update; omitted fields retain their prior values..
note: Stay within the current objective: Update a resource through the ORM. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Apply supplied changes to the intended persistent entity without overwriting omitted fields.
PRACTICE ANCHOR (live_code): Update the note of one existing order using supplied permitted changes while preserving its omitted quantity. Commit the update and verify both fields after reloading the order in an independent session.  SUCCESS: The intended order has the supplied note and its original quantity in committed storage. The update commits on success, and the failure path rolls back before further session use.
ASSESSMENT ANCHOR: apply_only_supplied_permitted_fields_to_loaded_entity facts=['f1', 'f2']
ASSESSMENT ANCHOR: commit_successful_update_and_rollback_failure facts=['f3']
ASSESSMENT ANCHOR: verify_changed_and_preserved_fields_in_independent_session facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authentication and authorization tests including invalid-token rejection; Bounded retry decisions respecting HTTP idempotency; Bounding payloads, expensive requests and API resource consumption; Database test-state isolation; Declaring the deployed bearer-access-token and authorization-server security contract without a password grant; Delete resource; Diagnose service failures from emitted and interpreted evidence; Documenting expected success and error responses; Endpoint authorization with required permissions or scopes; Established authorization-server integration using authorization code and PKCE where applicable; no resource-owner password grant; Freshness policy; Inspecting generated OpenAPI for drift and sensitive exposure; JWT signature, issuer, audience and expiry verification; Object-level authorization against the authenticated principal; Recognizing and avoiding redundant ORM queries; Safe failure policy; Safe unexpected-error responses with actionable server evidence; Service release and rollback workflow with build, release and run separation; Update resource; Upstream failure translation; Webhook authenticity verification; Webhook delivery idempotency; Webhook repla

## LESSON, in learner order

### s01 · explainer · Choose the boundary: Create resource
(mechanism) Construct Entity(field=value, ...) with supplied fields. session.add(entity) puts it into pending-insert state. ⟦A.f1 A:tb1 A:tb2 A:tb3⟧
(mechanism) await session.flush() emits the pending insert. Generated identity values are assigned back when the mapping and database support that behavior. ⟦A.f2 A:tb1 A:tb2 A:tb3⟧
(mechanism) Complete successful creation with await session.commit() or successful exit from session.begin(). Flush alone is not commit. ⟦A.f3 A:tb1 A:tb2 A:tb3⟧
(mechanism) Use await fresh_session.get(Entity, identity) in an independent session to verify generated identity and committed fields, not just object construction. ⟦A.f4 A:tb1 A:tb2 A:tb3⟧
[DIAGRAM] nodes=["Construct Entity with supplied fields: external_reference='ref-new', note='created note', quantity=5, processing='queued'", 'session.add(entity): pending insert', 'await session.flush(): insert; generated identity when supported', 'await session.commit(): durable creation', 'await fresh_session.get(Entity, identity): independently verify identity and fields'] edges=[('0', '1', None), ('1', '2', None), ('2', '3', None), ('3', '4', None)] alt: Creation states are separate boundaries. Flush may assign an identity but is not commit. Independent retrieval verifies committed values.

### s02 · explainer · Trace the distinction: Create resource
(mental_model) Follow construction, pending insertion, flush and commit as separate states. An identity observed after flush is not evidence of commitment. Retrieve independently after successful commit and compare the supplied fields. The mapped Entity alias uses the orders fixture here, not the separate textual-lookup dataset. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Distinguish: Create resource
Check your understanding — 

### s04 · hands_on · Practice: Create resource
Apply the rule — 

### s05 · explainer · Choose the boundary: Delete resource
(mechanism) Load the target with await session.get(Order, identity). Handle None as absence before attempting deletion. ⟦B.f1 B:tb1 B:tb2 B:tb3⟧
(mechanism) await session.delete(entity) marks the persistent entity for removal; flush emits the row deletion. ⟦B.f2 B:tb1 B:tb2 B:tb3⟧
(mechanism) Commit successful deletion under the transaction contract; roll back failed deletion. Do not report uncommitted removal as durable. ⟦B.f3 B:tb1 B:tb2 B:tb3⟧
(mechanism) Verify with a fresh primary-key lookup or independent session: the intended identity is absent and another row was not removed instead. ⟦B.f4 B:tb1 B:tb2 B:tb3⟧
[CODE python]
async def remove(session, fresh_session):
    entity = await session.get(Order, 101)
    if entity is None:
        return None
    try:
        await session.delete(entity)
        await session.flush()
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    assert await fresh_session.get(Order, 101) is None
    assert await fresh_session.get(Order, 102) is not None
  annotations: ['Select the intended identity; handle absence.', 'Mark, flush, commit; roll back failed deletion.', 'Independent verification: target absent, other row preserved.']

### s06 · explainer · Trace the distinction: Delete resource
(mental_model) The registered target is 101; 102 is the comparison row, and 999 exercises absence. Lookup, marking, flush and durable removal are distinct. After success, independently check target absence and preservation of the other row. After failure, roll back rather than reporting durable deletion. ⟦B.f1 B.f2 B.f3 B.f4 B:tb4 B:tb5⟧

### s07 · check · Distinguish: Delete resource
Check your understanding — 

### s08 · hands_on · Practice: Delete resource
Apply the rule — 

### s09 · explainer · Choose the boundary: Update resource
(mechanism) Assign attributes on a loaded persistent entity. The session tracks the changes and emits UPDATE at flush. ⟦C.f1 C:tb1 C:tb2 C:tb3⟧
(mechanism) Use model_dump(exclude_unset=True), then assign only supplied permitted fields. Omitted values must stay unchanged. ⟦C.f2 C:tb1 C:tb2 C:tb3⟧
(mechanism) Commit successful updates under the transaction contract. Roll back failures before further session use. ⟦C.f3 C:tb1 C:tb2 C:tb3⟧
(mechanism) Reload in an independent session after commit. Verify both changed supplied fields and unchanged omitted fields; inspecting the request model is not persistence evidence. ⟦C.f4 C:tb1 C:tb2 C:tb3⟧
[CODE python]
async def update(session, fresh_session, changes):
    entity = await session.get(Order, 42)
    if entity is None:
        return None
    supplied = changes.model_dump(exclude_unset=True)
    previous_quantity = entity.quantity
    try:
        for field, value in supplied.items():
            if field in ['note', 'quantity']:
                setattr(entity, field, value)
        await session.flush()
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    stored = await fresh_session.get(Order, entity.id)
    assert stored.note == supplied["note"]
    assert stored.quantity == previous_quantity
  annotations: ["Fixture supplies only note='new note 42'; omitted quantity stays unchanged.", 'Flush emits UPDATE; commit success or roll back failure before reuse.', 'Independent reload checks both changed and preserved fields.']

### s10 · explainer · Trace the distinction: Update resource
(mental_model) For order 42, the supplied partial update changes note and omits quantity. Extract only supplied permitted fields. After commitment, independently reload and compare both fields: check the changed note and preserved quantity. Roll back failure before reuse; the request model alone proves neither stored result. ⟦C.f1 C.f2 C.f3 C.f4 C:tb4 C:tb5⟧

### s11 · check · Distinguish: Update resource
Check your understanding — 

### s12 · hands_on · Practice: Update resource
Apply the rule — 

### s13 · recap · Keep the boundaries clear
(takeaway) Contrast an identity after flush with independently verified committed fields. Flush is not commitment. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Contrast deletion marking with committed target absence. Independently check the intended row and the preserved other row. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
(takeaway) Contrast a supplied note with omitted quantity. A correct partial update changes the former and preserves the latter in committed state. ⟦C.f1 C.f2 C.f3 C.f4 C:tb2 C:tb3 C:tb4 C:tb5⟧
[UP NEXT] JWT signature, issuer, audience and expiry verification: Next: tile_079.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try again: verify committed identity and fields in independent session
(mechanism) Use await fresh_session.get(Entity, identity) in an independent session to verify generated identity and committed fields, not just object construction. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast an identity after flush with independently verified committed fields. Flush is not commitment. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Try again: construct and register new entity
(mechanism) Construct Entity(field=value, ...) with supplied fields. session.add(entity) puts it into pending-insert state. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) await session.flush() emits the pending insert. Generated identity values are assigned back when the mapping and database support that behavior. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Complete successful creation with await session.commit() or successful exit from session.begin(). Flush alone is not commit. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(mechanism) Use await fresh_session.get(Entity, identity) in an independent session to verify generated identity and committed fields, not just object construction. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast an identity after flush with independently verified committed fields. Flush is not commitment. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Try again: complete durable deletion with failure rollback
(mechanism) await session.delete(entity) marks the persistent entity for removal; flush emits the row deletion. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Commit successful deletion under the transaction contract; roll back failed deletion. Do not report uncommitted removal as durable. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) Contrast deletion marking with committed target absence. Independently check the intended row and the preserved other row. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r04 · Try again: identify target and handle absence
(mechanism) Load the target with await session.get(Order, identity). Handle None as absence before attempting deletion. ⟦B.f1 B:tb2 B:tb4⟧
(mechanism) Verify with a fresh primary-key lookup or independent session: the intended identity is absent and another row was not removed instead. ⟦B.f4 B:tb3 B:tb4 B:tb5⟧
(misconception) Contrast deletion marking with committed target absence. Independently check the intended row and the preserved other row. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r05 · Try again: verify changed and preserved fields in independent session
(mechanism) Reload in an independent session after commit. Verify both changed supplied fields and unchanged omitted fields; inspecting the request model is not persistence evidence. ⟦C.f4 C:tb3 C:tb4 C:tb5⟧
(misconception) Contrast a supplied note with omitted quantity. A correct partial update changes the former and preserves the latter in committed state. ⟦C.f1 C.f2 C.f3 C.f4 C:tb2 C:tb3 C:tb4 C:tb5⟧
### r06 · Try again: apply only supplied permitted fields to loaded entity
(mechanism) Assign attributes on a loaded persistent entity. The session tracks the changes and emits UPDATE at flush. ⟦C.f1 C:tb2 C:tb4⟧
(mechanism) Use model_dump(exclude_unset=True), then assign only supplied permitted fields. Omitted values must stay unchanged. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
(mechanism) Commit successful updates under the transaction contract. Roll back failures before further session use. ⟦C.f3 C:tb3 C:tb4⟧
(mechanism) Reload in an independent session after commit. Verify both changed supplied fields and unchanged omitted fields; inspecting the request model is not persistence evidence. ⟦C.f4 C:tb3 C:tb4 C:tb5⟧
(misconception) Contrast a supplied note with omitted quantity. A correct partial update changes the former and preserves the latter in committed state. ⟦C.f1 C.f2 C.f3 C.f4 C:tb2 C:tb3 C:tb4 C:tb5⟧

=========

# EVALUATOR PACKET — JWT signature, issuer, audience and expiry verification (tile_079)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = auth.jwt_verification — JWT signature, issuer, audience and expiry verification

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (auth.jwt_verification)   objective: Verify JWTs before trusting claims: protect one endpoint with token verification.
A.f1: JWT decoding without verification reveals claims but does not establish that the claims are trustworthy.   [sources: fastapi_docs_tutorial#https://pyjwt.readthedocs.io/en/latest/usage.html#reading-the-claimset-without-validation]
A.f2: Verify with jwt.decode(token, key, algorithms=[allowed_algorithm], issuer=expected_issuer, audience=expected_audience, options={"require": ["exp", "iss", "aud"]}); choose the allowed algorithm from trusted configuration, not from the token alone.   [sources: fastapi_docs_tutorial#https://pyjwt.readthedocs.io/en/latest/api.html#jwt.decode]
A.f3: Expiration and not-before claims constrain token time validity; checks for a claim's value are distinct from requiring that the claim be present.   [sources: fastapi_docs_tutorial#https://pyjwt.readthedocs.io/en/latest/usage.html#expiration-time-claim-exp, fastapi_docs_tutorial#https://pyjwt.readthedocs.io/en/latest/usage.html#not-before-time-claim-nbf, fastapi_docs_tutorial#https://pyjwt.readthedocs.io/en/latest/usage.html#requiring-presence-of-claims]
A.f4: Treat a library verification exception as an invalid credential and reject the protected request rather than using its unverified claims.   [sources: fastapi_docs_tutorial#https://pyjwt.readthedocs.io/en/latest/usage.html#registered-claim-names, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#update-the-dependencies]
note: Establish this first: Claims are untrusted until verification succeeds.
note: Stay within the current objective: Verify JWTs before trusting claims. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Identify signature, expiry and contextual failures.
PRACTICE ANCHOR (live_code): Protect one endpoint by composing the existing bearer-token extraction dependency with JWT verification using trusted configuration, required claims and credential rejection on verification failure.  SUCCESS: The endpoint returns its protected output only after verification succeeds. Verification uses the configured key, allowed algorithm, issuer and audience, requires exp, iss and aud, and rejects library verification exceptions with HTTP 401 without falling back to unverified claims.
ASSESSMENT ANCHOR: distinguish_readable_claims_from_verified_claims facts=['f1']
ASSESSMENT ANCHOR: identify_signature_verification_failure_and_reject_credentials facts=['f2', 'f4']
ASSESSMENT ANCHOR: identify_expiration_and_not_before_failures facts=['f3', 'f4']
ASSESSMENT ANCHOR: identify_issuer_and_audience_mismatches facts=['f2', 'f4']
ASSESSMENT ANCHOR: distinguish_required_claim_presence_from_claim_value_checks facts=['f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authentication and authorization tests including invalid-token rejection; Bounded retry decisions respecting HTTP idempotency; Bounding payloads, expensive requests and API resource consumption; Database test-state isolation; Declaring the deployed bearer-access-token and authorization-server security contract without a password grant; Diagnose service failures from emitted and interpreted evidence; Documenting expected success and error responses; Endpoint authorization with required permissions or scopes; Established authorization-server integration using authorization code and PKCE where applicable; no resource-owner password grant; Freshness policy; Inspecting generated OpenAPI for drift and sensitive exposure; Object-level authorization against the authenticated principal; Recognizing and avoiding redundant ORM queries; Safe failure policy; Safe unexpected-error responses with actionable server evidence; Service release and rollback workflow with build, release and run separation; Upstream failure translation; Webhook authenticity verification; Webhook delivery idempotency; Webhook replay freshness

## LESSON, in learner order

### s01 · explainer · Choose the boundary: JWT signature, issuer, audience and expiry verification
(mechanism) Unverified decoding makes JWT claims readable, not trustworthy. ⟦A.f1 A:tb1 A:tb2 A:tb3⟧
(mechanism) Verify with jwt.decode(token, key, algorithms=[allowed_algorithm], issuer=expected_issuer, audience=expected_audience, options={"require": ["exp", "iss", "aud"]}). Choose the algorithm from trusted configuration, not the token alone. ⟦A.f2 A:tb1 A:tb2 A:tb3⟧
(mechanism) Expiration and not-before constrain time validity. Requiring a claim to exist and checking its value are separate responsibilities. ⟦A.f3 A:tb1 A:tb2 A:tb3⟧
(mechanism) A library verification exception means reject the credential and protected request. Never fall back to using unverified claims. ⟦A.f4 A:tb1 A:tb2 A:tb3⟧
[CODE python]
import jwt
from fastapi import Depends, HTTPException

# key, allowed_algorithm, expected_issuer and expected_audience are trusted configuration.
def verify(token=Depends(existing_bearer_dependency)):
    try:
        return jwt.decode(
            token, key, algorithms=[allowed_algorithm],
            issuer=expected_issuer, audience=expected_audience,
            options={"require": ["exp", "iss", "aud"]},
        )
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid credential",
                            headers={"WWW-Authenticate": "Bearer"})

@app.get("/protected")
def protected(context=Depends(verify)):
    return protected_output(context)
  annotations: ['Require claim presence and verify configured values. Expiration and not-before constrain time validity.', 'Verification failure rejects the request; protected output cannot use unverified fallback claims.']

### s02 · explainer · Trace the distinction: JWT signature, issuer, audience and expiry verification
(mental_model) Keep readable claims, required presence and verified values distinct. Reading a payload establishes only the first. Trusted key, algorithm, issuer and audience configuration set the verification boundary; time checks do not substitute for claim-presence requirements. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧

### s03 · explainer · Trace the distinction: JWT signature, issuer, audience and expiry verification
(walkthrough) Trace valid, expired, future not-before, issuer-mismatch and audience-mismatch fixtures through the verifier. Protected output follows successful verification only. A library rejection must not trigger fallback to the readable payload. The token must not select its own allowed algorithm. ⟦A.f1 A.f2 A.f3 A.f4 A:tb5 A:tb6⟧

### s04 · check · Distinguish: JWT signature, issuer, audience and expiry verification
Check your understanding — 

### s05 · check · Distinguish: JWT signature, issuer, audience and expiry verification
Check your understanding — 

### s06 · hands_on · Practice: JWT signature, issuer, audience and expiry verification
Apply the rule — 

### s07 · recap · Keep the boundaries clear
(takeaway) Contrast a readable payload with successful configured verification. Rejection must not reuse unverified claims. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
[UP NEXT] Freshness policy: Next: tile_080.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try again: identify expiration and not before failures
(mechanism) Expiration and not-before constrain time validity. Requiring a claim to exist and checking its value are separate responsibilities. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(mechanism) A library verification exception means reject the credential and protected request. Never fall back to using unverified claims. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast a readable payload with successful configured verification. Rejection must not reuse unverified claims. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r02 · Try again: distinguish required claim presence from claim value checks
(mechanism) Verify with jwt.decode(token, key, algorithms=[allowed_algorithm], issuer=expected_issuer, audience=expected_audience, options={"require": ["exp", "iss", "aud"]}). Choose the algorithm from trusted configuration, not the token alone. ⟦A.f2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(mechanism) Expiration and not-before constrain time validity. Requiring a claim to exist and checking its value are separate responsibilities. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast a readable payload with successful configured verification. Rejection must not reuse unverified claims. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
### r03 · Try again: distinguish readable claims from verified claims
(mechanism) Unverified decoding makes JWT claims readable, not trustworthy. ⟦A.f1 A:tb2 A:tb4 A:tb5 A:tb6⟧
(mechanism) Verify with jwt.decode(token, key, algorithms=[allowed_algorithm], issuer=expected_issuer, audience=expected_audience, options={"require": ["exp", "iss", "aud"]}). Choose the algorithm from trusted configuration, not the token alone. ⟦A.f2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(mechanism) A library verification exception means reject the credential and protected request. Never fall back to using unverified claims. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast a readable payload with successful configured verification. Rejection must not reuse unverified claims. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧

=========

# EVALUATOR PACKET — Freshness policy / Safe failure policy (tile_080)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = cache.freshness_policy — Freshness policy
B = cache.safe_failure_policy — Safe failure policy

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (cache.freshness_policy)   objective: Control cached-data freshness after writes: implement expiry and write invalidation for one cached resource.
A.f1: Choose a cache TTL from the tolerated staleness window: a shorter TTL refreshes sooner but causes more primary-store reads, while a longer TTL reduces reads and can serve older values longer.   [sources: redis_docs#https://redis.io/docs/latest/develop/use-cases/cache-aside/redis-py/#choose-a-ttl-that-matches-your-staleness-tolerance]
A.f2: For a string cache entry, pass ex=seconds to Redis set(key, value, ex=seconds) to assign an expiry when writing it.   [sources: redis_docs#https://redis.readthedocs.io/en/stable/commands.html#redis.commands.core.CoreCommands.set]
A.f3: After the primary record changes, delete its cache key so the next cache-aside read reloads it instead of serving the old copy.   [sources: redis_docs#https://redis.io/docs/latest/develop/use-cases/cache-aside/redis-py/#invalidate-dont-try-to-keep-the-cache-in-sync]
A.f4: Inspect ttl(key): it reports remaining seconds, -1 for a key without expiry and -2 for an absent key; change the primary record and verify that invalidation makes the next read return the changed value.   [sources: redis_docs#https://redis.io/commands/ttl, redis_docs#https://redis.io/docs/latest/develop/use-cases/cache-aside/redis-py/#inspect-cached-entries-directly-in-redis]
note: Establish this first: Freshness is bounded by lifetime and invalidation of derived copies.
note: Stay within the current objective: Control cached-data freshness after writes. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Select expiry and invalidation satisfying a stated stale-data tolerance.
PRACTICE ANCHOR (live_code): Implement expiry and write invalidation for one cached order. Choose a positive TTL within a stated stale-data tolerance, assign it when caching the order's notes, delete the cache key after a committed notes change, and verify the next cache-aside read returns the changed notes.  SUCCESS: The cached notes have a positive remaining TTL no greater than the chosen lifetime. After the primary notes change and the cache key is deleted, ttl(key) returns -2 before the next read. That read returns the new notes and repopulates the cache with expiry.
ASSESSMENT ANCHOR: select_and_configure_expiry_for_staleness_tolerance facts=['f1', 'f2']
ASSESSMENT ANCHOR: select_write_invalidation_after_primary_changes facts=['f3']
ASSESSMENT ANCHOR: interpret_ttl_and_verify_freshness_after_invalidation facts=['f4']

## SOURCE FACTS — B (cache.safe_failure_policy)   objective: Preserve correctness when the cache is unavailable: implement a correct database fallback for one cache-backed read.
B.f1: Catch Redis connection and timeout exceptions at the cache boundary so the application can apply its declared cache-outage policy rather than letting an incidental cache exception choose the outcome.   [sources: redis_docs#https://redis.io/docs/latest/develop/clients/redis-py/produsage/#exception-handling]
B.f2: When the cache is only an acceleration layer and the primary store is available, the miss path can load and return the primary-store value without a successful cache read or write.   [sources: redis_docs#https://redis.io/docs/latest/develop/use-cases/cache-aside/redis-py/#the-cache-aside-helper, redis_docs#https://redis.io/docs/latest/develop/use-cases/cache-aside/#when-to-use-redis-cache-aside]
B.f3: Configure finite socket_connect_timeout and socket_timeout values on the Redis client so a failed cache does not cause unbounded connection or response waits.   [sources: redis_docs#https://redis.io/docs/latest/develop/clients/redis-py/produsage/#timeouts]
B.f4: Verify the policy with a controlled failing cache dependency, asserting the primary-store result or the declared failure outcome rather than assuming that a cache outage is equivalent to lost primary data.   [sources: redis_docs#https://redis.io/docs/latest/develop/clients/redis-py/produsage/#exception-handling, fastapi_docs_tutorial#https://fastapi.tiangolo.com/tutorial/testing/#using-testclient]
note: Establish this first: A cache outage may degrade performance but must not change the authoritative result..
note: Stay within the current objective: Preserve correctness when the cache is unavailable. Avoid extending the example into blocked later concepts.
note: Use the worked case to support this target: Determine whether cache failure changes authoritative outcomes.
PRACTICE ANCHOR (live_code): Implement one cache-backed read that returns the available primary-store value when Redis connection or timeout failures prevent cache lookup or population. Configure finite Redis connection and response timeouts and verify the fallback using a controlled failing cache dependency.  SUCCESS: The read returns the primary-store value when cache lookup fails and when cache population fails after a miss. Controlled connection and timeout failures do not escape the cache boundary, and both Redis socket timeout settings are finite.
ASSESSMENT ANCHOR: determine_whether_cache_failure_changes_authoritative_outcomes facts=['f1', 'f2', 'f4']
ASSESSMENT ANCHOR: identify_finite_cache_connection_and_response_waits facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Authentication and authorization tests including invalid-token rejection; Bounded retry decisions respecting HTTP idempotency; Bounding payloads, expensive requests and API resource consumption; Database test-state isolation; Declaring the deployed bearer-access-token and authorization-server security contract without a password grant; Diagnose service failures from emitted and interpreted evidence; Documenting expected success and error responses; Endpoint authorization with required permissions or scopes; Established authorization-server integration using authorization code and PKCE where applicable; no resource-owner password grant; Inspecting generated OpenAPI for drift and sensitive exposure; Object-level authorization against the authenticated principal; Recognizing and avoiding redundant ORM queries; Safe failure policy; Safe unexpected-error responses with actionable server evidence; Service release and rollback workflow with build, release and run separation; Upstream failure translation; Webhook authenticity verification; Webhook delivery idempotency; Webhook replay freshness

## LESSON, in learner order

### s01 · explainer · Choose the boundary: Freshness policy
(mechanism) Choose TTL from tolerated staleness. Shorter TTL refreshes sooner but increases primary reads; longer TTL reduces reads but may serve older values longer. ⟦A.f1 A:tb1 A:tb2 A:tb3⟧
(mechanism) For a Redis string entry, set(key, value, ex=seconds) assigns expiry when writing. ⟦A.f2 A:tb1 A:tb2 A:tb3⟧
(mechanism) After the primary record changes, delete its cache key. The next cache-aside read then reloads instead of returning the old copy. ⟦A.f3 A:tb1 A:tb2 A:tb3⟧
(mechanism) ttl(key) reports remaining seconds, -1 for no expiry, and -2 for absence. Change the primary record and verify invalidation makes the next read return the changed value. ⟦A.f4 A:tb1 A:tb2 A:tb3⟧
[PROCESS_FLOW] nodes=['Old copy: old note 42; set(..., ex=seconds)', 'TTL: remaining seconds; -1 means no expiry', 'Committed primary change: new note 42', 'Delete order:42:notes', 'TTL -2: absent key', 'Next read: cache miss', 'Reload changed primary value; populate with expiry'] edges=[('0', '1', None), ('1', '2', None), ('2', '3', None), ('3', '4', None), ('4', '5', None), ('5', '6', None)] alt: Old copy: old note 42; set(..., ex=seconds); TTL: remaining seconds; -1 means no expiry; Committed primary change: new note 42; Delete order:42:notes; TTL -2: absent key; Next read: cache miss; Reload changed primary value; populate with expiry

### s02 · explainer · Trace the distinction: Freshness policy
(mental_model) The fixture permits 30 seconds of staleness for order:42:notes. Compare old notes old note 42 with changed notes new note 42. After the committed primary change, delete the key and inspect TTL before the next read. No expiry and no key are different states. Verify fresh reload and expiry when the copy is populated again. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · video · Follow the sequence: Freshness policy
[VIDEO ] bridge-before:  | bridge-after: 

### s04 · check · Distinguish: Freshness policy
Check your understanding — 

### s05 · hands_on · Practice: Freshness policy
Apply the rule — 

### s06 · explainer · Choose the boundary: Safe failure policy
(mechanism) Catch Redis connection and timeout exceptions at the cache boundary, then apply the declared outage policy rather than letting the incidental exception decide. ⟦B.f1 B:tb1 B:tb2 B:tb3⟧
(mechanism) With an acceleration-only cache and available primary store, load and return primary data on the miss path even if cache reading or writing fails. ⟦B.f2 B:tb1 B:tb2 B:tb3⟧
(mechanism) Set finite socket_connect_timeout and socket_timeout on the Redis client to bound connection and response waits. ⟦B.f3 B:tb1 B:tb2 B:tb3⟧
(mechanism) Use a controlled failing cache dependency to verify the primary result or declared failure outcome. Cache failure alone does not establish lost primary data. ⟦B.f4 B:tb1 B:tb2 B:tb3⟧
[CODE python]
from redis.asyncio import Redis
from redis.exceptions import ConnectionError, TimeoutError

# finite_connect_seconds and finite_response_seconds are finite service settings.
redis = Redis(socket_connect_timeout=finite_connect_seconds,
              socket_timeout=finite_response_seconds)

async def safe_read(cache, key, load, seconds):
    try:
        cached = await cache.get(key)
    except (ConnectionError, TimeoutError):
        cached = None
    if cached is not None:
        return cached
    value = await load()
    try:
        await cache.set(key, value, ex=seconds)
    except (ConnectionError, TimeoutError):
        pass
    return value

# Supplied controlled substitute and registered primary result:
for operation in contract["failure_operations"]:
    for exception in (ConnectionError, TimeoutError):
        cache = FailingCache(operation, exception)
        assert await safe_read(cache, key, load, seconds) == contract["primary_value"]
  annotations: ['Lookup exception boundary.', 'Primary loading stays outside cache catches; population failure does not discard the available value.', 'Controlled lookup and population failures verify the acceleration-only policy.']

### s07 · explainer · Trace the distinction: Safe failure policy
(mental_model) Test both lookup and population failure with controlled Redis connection and timeout exceptions. The fixture’s cache is acceleration only: available primary data still returns. Keep exception handling around cache operations, not the primary loader. Finite waits bound the cache failure; they do not promise every primary store is available. ⟦B.f1 B.f2 B.f3 B.f4 B:tb4 B:tb5⟧

### s08 · check · Distinguish: Safe failure policy
Check your understanding — 

### s09 · hands_on · Practice: Safe failure policy
Apply the rule — 

### s10 · recap · Keep the boundaries clear
(takeaway) Contrast a key without expiry with an absent key. Invalidation removes the stale copy so the next read reloads. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Contrast unavailable acceleration with unavailable primary data. Apply the declared policy without masking a primary failure. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Service release and rollback workflow with build, release and run separation: Next: tile_082.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try again: interpret ttl and verify freshness after invalidation
(mechanism) ttl(key) reports remaining seconds, -1 for no expiry, and -2 for absence. Change the primary record and verify invalidation makes the next read return the changed value. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast a key without expiry with an absent key. Invalidation removes the stale copy so the next read reloads. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Try again: select and configure expiry for staleness tolerance
(mechanism) Choose TTL from tolerated staleness. Shorter TTL refreshes sooner but increases primary reads; longer TTL reduces reads but may serve older values longer. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) For a Redis string entry, set(key, value, ex=seconds) assigns expiry when writing. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) After the primary record changes, delete its cache key. The next cache-aside read then reloads instead of returning the old copy. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(mechanism) ttl(key) reports remaining seconds, -1 for no expiry, and -2 for absence. Change the primary record and verify invalidation makes the next read return the changed value. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast a key without expiry with an absent key. Invalidation removes the stale copy so the next read reloads. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Try again: determine whether cache failure changes authoritative outcomes
(mechanism) Catch Redis connection and timeout exceptions at the cache boundary, then apply the declared outage policy rather than letting the incidental exception decide. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(mechanism) With an acceleration-only cache and available primary store, load and return primary data on the miss path even if cache reading or writing fails. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Use a controlled failing cache dependency to verify the primary result or declared failure outcome. Cache failure alone does not establish lost primary data. ⟦B.f4 B:tb3 B:tb4⟧
(misconception) Contrast unavailable acceleration with unavailable primary data. Apply the declared policy without masking a primary failure. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r04 · Try again: identify finite cache connection and response waits
(mechanism) Set finite socket_connect_timeout and socket_timeout on the Redis client to bound connection and response waits. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) Contrast unavailable acceleration with unavailable primary data. Apply the declared policy without masking a primary failure. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧