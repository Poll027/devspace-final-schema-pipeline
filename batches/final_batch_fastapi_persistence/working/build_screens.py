import json, re
from pathlib import Path
B=Path('batches/final_batch_persistence')
P=json.loads((B/'tile_plans.json').read_text()); G=json.loads((B/'inputs/path_glossary_bundle.json').read_text()); A=json.loads((B/'scenario_asset_registry.json').read_text())
bundles={b['context']['concept_id']:b for b in G['bundles']}
assets={a['asset_id']:a for a in A['assets']}
contracts={k[3:]:json.loads(next(f['content'] for f in a['files'] if f['path']=='contract.json')) for k,a in assets.items() if a['asset_kind']=='code_workspace'}
# Re-voiced facts, in the glossary's fact order. Concrete fixture values below are read from the registry.
F={
'sqlalchemy.retrieve_resource':[
'Use await session.scalars(select(Order).where(condition)) for conditional entity selection. Inspect the returned entities; this is not an unbounded application-wide lookup.',
'For a primary-key identity, await session.get(Order, identity) returns that Order or None if no row exists.',
'Use .limit(n) to bound a selection. Treat an empty selection or None explicitly as absence.'],
'sqlalchemy.transaction_boundaries':[
'Wrap related writes in async with session.begin():. Successful exit commits; exceptional exit rolls back.',
'Commit makes changes durable; rollback discards uncommitted changes. Writes required to succeed or fail together belong in one transaction.',
'A failed flush leaves the session needing transactional recovery. Explicitly await session.rollback() before reusing it, even if the error was caught.'],
'auth.bearer_dependency':[
'HTTPBearer extracts a presented credential from Authorization: Bearer token. Obtaining that credential does not establish validity.',
'On a handler input, declare Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]. Read scheme and credentials for the supplied scheme and token text.',
'With default auto_error=True, missing credentials and non-bearer schemes are rejected before the handler. Test absent and malformed Authorization headers separately.'],
'cache.redis_cache_aside':[
'The cache is a copy in front of the primary store. The primary store, not the cache, remains authoritative.',
'Check the cache key first. On a miss, load the primary-store result, cache it, and return it.',
'Cache-aside suits repeated, read-heavy access when the application permits reuse within its staleness requirements.',
'Build keys from result identity and parameters. Different represented results must not accidentally share a cached value.'],
'database.alembic_migrations':[
'Alembic uses a migration environment and versioned revision scripts. upgrade() and downgrade() describe schema-change directions.',
'Generate a candidate with alembic revision --autogenerate -m "description", comparing the database schema against supplied target_metadata.',
'Review and correct that candidate manually. Autogeneration does not reliably infer every intent, including table or column renames.',
'Apply with alembic upgrade head. Before operational use, test the proposed reversal with alembic downgrade revision on a test database.',
'Inspect drop-and-add for possible rename intent. Dropping a column deletes its data; recreating a column may not recover that data.'],
'database.service_query_indexes':[
'An index can speed selected-row access, but adds overhead. Choose for an actual query workload, not automatically for every column.',
'PostgreSQL B-tree indexes support equality and ordered comparisons. Frequently filtered or ordered values are candidates, not guaranteed speedups.',
'For a frequent lookup, propose CREATE INDEX name ON table (column), accounting for extra storage and index maintenance during writes.'],
'design.api_persistence_model_boundaries':[
'Persistence models map stored rows; public response models select client-facing fields. These contracts remain separate even for the same entity.',
'Define separate public input and output BaseModel classes. response_model=PublicOutput keeps persistence-only or sensitive fields from automatically becoming API fields.',
'For validation from object attributes, use model_config = ConfigDict(from_attributes=True) on the public model. The persistence class need not become the public schema.'],
'fastapi.domain_error_translation':[
'Use @app.exception_handler(FailureClass) to translate a recognized internal failure into an intentional public HTTP outcome.',
'For a recognized uniqueness conflict, use 409 when the API declares that conflict outcome. Do not expose database exception text.',
'Roll back a failed persistence transaction before session reuse. Translate the recognized failure at the API boundary without disclosing internals; an HTTP response alone does not recover the session.'],
'fastapi.public_error_envelopes':[
'A handler receives request and exception, and can return JSONResponse(status_code=..., content=...) with a stable public error shape.',
'Register for Starlette HTTPException when FastAPI and Starlette HTTP exceptions should share that envelope.',
'Use intended client-facing information in the envelope, not raw exception details or internal stack traces.',
'Keep the recognized status code and relevant headers. Reformatting the body must not change the underlying HTTP outcome.'],
'fastapi_backend.proxy_header_trust':[
'A TLS-terminating proxy can forward original scheme and client information. Accept those headers only from configured trusted proxy sources.',
'Set --forwarded-allow-ips to trusted addresses. The wildcard * trusts every sender and is appropriate only with network access restricted to trusted proxies.',
'If the proxy strips an external prefix, set root_path to that prefix so generated API URLs and documentation reflect the public address.',
'Check redirects and documentation through the public HTTPS proxy URL. Their scheme and prefix should match the external URL, not the internal backend.'],
'integration.webhook_contracts':[
'Declare accepted media type, event shape and required fields. Validate the body against that contract before accepting downstream work.',
'Acknowledgment expresses accepted delivery, not proof that all downstream business work finished.',
'When the integration permits deferred processing, promptly return its declared 2xx after acceptance and keep slow downstream work outside the acknowledgment path.',
'Bind a typed input model and declare status_code on the operation decorator. Verify both accepted and invalid inputs against the acknowledgment contract.'],
'observability.request_correlation':[
'Connect a request chain with a nonsensitive interaction identifier instead of reconstructing it from timestamps alone.',
'Bind Header(alias=header_name). Under service policy, keep or create a bounded nonsensitive identifier and forward that same value with client.get(url, headers={header_name: identifier}).',
'Include the identifier in related local events. Correlation context is not evidence of caller authority.',
'Check the outbound receiver header and related logs. Concurrent requests must retain distinct correlation contexts.'],
'observability.service_signal_interpretation':[
'Request rate counts request events per time interval; error rate counts failures per interval. Traffic changes alone can change absolute failure counts.',
'Use rate(request_counter[window]) for request rate. Divide failure rate by request rate for failure fraction, using the same window and label group.',
'Latency comes from duration observations, independently of frequency. Inspect a histogram-derived quantile to distinguish slower responses from more requests.',
'Group signals by bounded nonsensitive categories such as method, route template and outcome, not raw caller or request identifiers.',
'Align windows and label groups across successful, failing and delayed samples. Ask separately about traffic, failure fraction and worsened duration distribution.'],
'rest.bounded_resource_listing':[
'Build a bounded page with select(Order).where(predicate).order_by(order_columns).limit(page_size).offset(offset).',
'When primary sort values repeat, add a unique tie-breaker for deterministic order rather than leaving ties unspecified.',
'OFFSET skips result rows; LIMIT caps rows returned afterward. Keep the same filter and unique ordering across page selections.',
'Declare numeric limits on accepted page size and offset. Derive offset from the requested page contract rather than permitting an unbounded read.'],
'security.injection_resistant_inputs':[
'Keep SQL structure separate from caller data through parameterization. Do not interpolate caller values into executable query text.',
'In select(Entity).where(Entity.field == supplied_value), the supplied value is bound data, not SQL syntax.',
'For textual SQL, use text("... WHERE field = :value") and execute with {"value": supplied_value}. Do not concatenate or format the input into SQL.',
'Parameters stand for data values, not arbitrary tables, columns or sort directions. Map requested structural choices through a defined allowlist.'],
'sqlalchemy.create_resource':[
'Construct Entity(field=value, ...) with supplied fields. session.add(entity) puts it into pending-insert state.',
'await session.flush() emits the pending insert. Generated identity values are assigned back when the mapping and database support that behavior.',
'Complete successful creation with await session.commit() or successful exit from session.begin(). Flush alone is not commit.',
'Use await fresh_session.get(Entity, identity) in an independent session to verify generated identity and committed fields, not just object construction.'],
'sqlalchemy.delete_resource':[
'Load the target with await session.get(Order, identity). Handle None as absence before attempting deletion.',
'await session.delete(entity) marks the persistent entity for removal; flush emits the row deletion.',
'Commit successful deletion under the transaction contract; roll back failed deletion. Do not report uncommitted removal as durable.',
'Verify with a fresh primary-key lookup or independent session: the intended identity is absent and another row was not removed instead.'],
'sqlalchemy.update_resource':[
'Assign attributes on a loaded persistent entity. The session tracks the changes and emits UPDATE at flush.',
'Use model_dump(exclude_unset=True), then assign only supplied permitted fields. Omitted values must stay unchanged.',
'Commit successful updates under the transaction contract. Roll back failures before further session use.',
'Reload in an independent session after commit. Verify both changed supplied fields and unchanged omitted fields; inspecting the request model is not persistence evidence.'],
'auth.jwt_verification':[
'Unverified decoding makes JWT claims readable, not trustworthy.',
'Verify with jwt.decode(token, key, algorithms=[allowed_algorithm], issuer=expected_issuer, audience=expected_audience, options={"require": ["exp", "iss", "aud"]}). Choose the algorithm from trusted configuration, not the token alone.',
'Expiration and not-before constrain time validity. Requiring a claim to exist and checking its value are separate responsibilities.',
'A library verification exception means reject the credential and protected request. Never fall back to using unverified claims.'],
'cache.freshness_policy':[
'Choose TTL from tolerated staleness. Shorter TTL refreshes sooner but increases primary reads; longer TTL reduces reads but may serve older values longer.',
'For a Redis string entry, set(key, value, ex=seconds) assigns expiry when writing.',
'After the primary record changes, delete its cache key. The next cache-aside read then reloads instead of returning the old copy.',
'ttl(key) reports remaining seconds, -1 for no expiry, and -2 for absence. Change the primary record and verify invalidation makes the next read return the changed value.'],
'cache.safe_failure_policy':[
'Catch Redis connection and timeout exceptions at the cache boundary, then apply the declared outage policy rather than letting the incidental exception decide.',
'With an acceleration-only cache and available primary store, load and return primary data on the miss path even if cache reading or writing fails.',
'Set finite socket_connect_timeout and socket_timeout on the Redis client to bound connection and response waits.',
'Use a controlled failing cache dependency to verify the primary result or declared failure outcome. Cache failure alone does not establish lost primary data.']}
# Contextual reasoning used after the initial rule screen; placeholders are supplied from registered contracts.
N={
'sqlalchemy.retrieve_resource':[
'An identity lookup and a conditional selection answer different questions. Check None before attributes on an identified Order. For a condition, inspect the entities under the intended limit, including an empty selection. Successful execution does not guarantee a matching row.',
'Trace the registered existing identity {existing_identities[0]} and absent identity {absent_identities[0]}. Then select the registered condition under its row bound. An entity, None and an empty selection need different handling; neither kind of absence is an existing Order.'],
'sqlalchemy.transaction_boundaries':[
'The two supplied write helpers share a requirement: succeed or fail together. A caught error does not show whether uncommitted data was discarded or session state recovered. Follow both responsibilities before reuse.',
'Contrast a completed pair with a failing second write. Successful transaction exit makes the pair durable; exceptional exit discards uncommitted changes. In the separate caught-flush case, await rollback before reuse. Catching the message alone is not recovery.'],
'auth.bearer_dependency':[
'Trace four inputs separately: nonempty Bearer, absent header, non-bearer scheme, and Bearer without text. Only extraction is being examined. Even when scheme and credentials are available, that text is not proof of valid claims; do not return or log the supplied credential.'],
'cache.redis_cache_aside':[
'Order {requests[0][0]} with representation {requests[0][1]} and the same order with {requests[1][1]} represent different results. Order {requests[2][0]} differs in identity. Keep their keys distinct. A repeated identical read may reuse its copy under this fixture’s permitted staleness policy; a miss still loads from the authoritative primary store.'],
'database.alembic_migrations':[
'Compare upgrade and downgrade as reviewed directions, not promises of recovered data. A candidate drop-and-add may conceal a rename. Test the proposed downgrade separately: restoring a schema shape may leave deleted column data unrecovered.'],
'database.service_query_indexes':[
'The fixture workload is {workload} on {table}.{column}. A B-tree is a candidate for that equality lookup. Pair the proposed declaration with storage and write-maintenance costs. Merely having a column, or needing an ordered comparison, does not guarantee a particular performance gain.'],
'design.api_persistence_model_boundaries':[
'The row carries storage-only processing state. Choose separate input and output fields; attribute-based validation does not authorize every attribute to become public.'],
'fastapi.domain_error_translation':[
'The fixture declares {declared_status} for its recognized uniqueness conflict and the public reason {public_reason}. Rollback recovers persistence state; the handler expresses client-facing meaning. Neither responsibility substitutes for the other. Do not classify every write failure as conflict or disclose the private diagnostic.'],
'fastapi.public_error_envelopes':[
'Compare the registered error cases with and without relevant headers. Changing the body shape must preserve recognized status and metadata. The public reason is intentional client information; an exception’s raw details are not a ready-made public envelope.'],
'fastapi_backend.proxy_header_trust':[
'The public address is {external_base}; the backend address is {backend_base}. Trust the configured source {trusted_proxy_source}, not a familiar header name. The fixture does not restrict network access to trusted proxies, so wildcard trust is not appropriate. Check the public scheme and stripped prefix through redirects and documentation.'],
'integration.webhook_contracts':[
'This fixture accepts {media_type} with required order_id and event fields, and permits deferred processing. Its declared acknowledgment is {acknowledgement_status}. Compare the accepted body with missing or invalid fields. Acceptance, acknowledgment and downstream completion are distinct observations; prompt acknowledgment must not claim finished business work.'],
'observability.request_correlation':[
'Compare two concurrent chains. Keep one consistent identifier from incoming header through local events to the receiver, but distinct identifiers between chains. A changed boundary value breaks correlation; accidentally sharing one value mixes contexts.'],
'observability.service_signal_interpretation':[
'Use the registered equal-window dashboard to compare baseline, traffic growth, failing and delayed samples. Request and failure totals describe frequency; failure fraction describes proportion; the histogram-derived quantile describes latency. A rise in absolute failures alone does not establish worse reliability. Match time windows and label groups before comparing.'],
'rest.bounded_resource_listing':[
'The fixture filters processing by {predicate[processing]}, orders by {primary_sort_column} and breaks ties with {unique_key}. Keep that predicate and order on adjacent pages. At page size {page_size_max}, the next page skips that many result rows before returning a bounded window. Derive the offset from the page contract and enforce its declared ceiling.'],
'security.injection_resistant_inputs':[
'A quote or SQL-looking phrase in supplied data remains a value when bound. A requested sort direction is different: it chooses structure and needs an allowlist. Do not assume a placeholder can express arbitrary SQL identifiers or direction.'],
'sqlalchemy.create_resource':[
'Follow construction, pending insertion, flush and commit as separate states. An identity observed after flush is not evidence of commitment. Retrieve independently after successful commit and compare the supplied fields. The mapped Entity alias uses the orders fixture here, not the separate textual-lookup dataset.'],
'sqlalchemy.delete_resource':[
'The registered target is {target_identity}; {other_identity} is the comparison row, and {absent_identity} exercises absence. Lookup, marking, flush and durable removal are distinct. After success, independently check target absence and preservation of the other row. After failure, roll back rather than reporting durable deletion.'],
'sqlalchemy.update_resource':[
'For order {order_id}, the supplied partial update changes note and omits quantity. Extract only supplied permitted fields. After commitment, independently reload and compare both fields: check the changed note and preserved quantity. Roll back failure before reuse; the request model alone proves neither stored result.'],
'auth.jwt_verification':[
'Keep readable claims, required presence and verified values distinct. Reading a payload establishes only the first. Trusted key, algorithm, issuer and audience configuration set the verification boundary; time checks do not substitute for claim-presence requirements.',
'Trace valid, expired, future not-before, issuer-mismatch and audience-mismatch fixtures through the verifier. Protected output follows successful verification only. A library rejection must not trigger fallback to the readable payload. The token must not select its own allowed algorithm.'],
'cache.freshness_policy':[
'The fixture permits {tolerance_seconds} seconds of staleness for {cache_key}. Compare old notes {old_notes} with changed notes {new_notes}. After the committed primary change, delete the key and inspect TTL before the next read. No expiry and no key are different states. Verify fresh reload and expiry when the copy is populated again.'],
'cache.safe_failure_policy':[
'Test both lookup and population failure with controlled Redis connection and timeout exceptions. The fixture’s cache is acceleration only: available primary data still returns. Keep exception handling around cache operations, not the primary loader. Finite waits bound the cache failure; they do not promise every primary store is available.']}
CONTRAST={
'sqlalchemy.retrieve_resource':'Contrast a returned Order with None or an empty conditional result: operation success is not evidence of a match.',
'sqlalchemy.transaction_boundaries':'Contrast handling an error message with recovering the transaction: catching a failed flush does not make the session reusable.',
'auth.bearer_dependency':'Contrast a nonempty Bearer header with an empty Bearer header. Passing extraction still does not verify validity.',
'cache.redis_cache_aside':'Contrast identical represented reads with reads that differ in identity or representation. Only the identical result can reuse that copy.',
'database.alembic_migrations':'Contrast recreating a dropped column with recovering its deleted data. A reversed schema shape does not necessarily restore values.',
'database.service_query_indexes':'Contrast a frequent equality lookup with simply having a column. Workload benefit must be weighed against storage and write overhead.',
'design.api_persistence_model_boundaries':'Contrast processing on the stored row with the selected public fields. Attribute validation does not grant field exposure.',
'fastapi.domain_error_translation':'Contrast returning the declared conflict response with recovering the failed session. Translation alone is not rollback.',
'fastapi.public_error_envelopes':'Contrast a changed public body with changed HTTP metadata. Formatting must preserve recognized status and relevant headers.',
'fastapi_backend.proxy_header_trust':'Contrast the configured proxy source with an untrusted sender. Forwarded header names do not establish trust.',
'integration.webhook_contracts':'Contrast accepted delivery with completed downstream work. The declared acknowledgment proves only the former.',
'observability.request_correlation':'Contrast one consistent identifier within a chain with one accidentally shared between concurrent chains. Correlation is not caller authority.',
'observability.service_signal_interpretation':'Contrast frequency with duration. More requests or absolute failures alone do not establish a higher failure fraction or slower responses.',
'rest.bounded_resource_listing':'Contrast a repeated primary sort value with the unique tie-breaker. LIMIT bounds the window after OFFSET skips rows.',
'security.injection_resistant_inputs':'Contrast caller data with a requested SQL structural choice. Bind the value; allowlist the structural choice.',
'sqlalchemy.create_resource':'Contrast an identity after flush with independently verified committed fields. Flush is not commitment.',
'sqlalchemy.delete_resource':'Contrast deletion marking with committed target absence. Independently check the intended row and the preserved other row.',
'sqlalchemy.update_resource':'Contrast a supplied note with omitted quantity. A correct partial update changes the former and preserves the latter in committed state.',
'auth.jwt_verification':'Contrast a readable payload with successful configured verification. Rejection must not reuse unverified claims.',
'cache.freshness_policy':'Contrast a key without expiry with an absent key. Invalidation removes the stale copy so the next read reloads.',
'cache.safe_failure_policy':'Contrast unavailable acceleration with unavailable primary data. Apply the declared policy without masking a primary failure.'}
for cid,b in bundles.items():
 assert len(F[cid])==len(b['coverage']['required_facts'])

class Format(dict):
 def __missing__(self,k): raise KeyError(k)
def scenario_text(cid,text): return text.format_map(contracts.get(cid,{}))
def lin(cids,tbs,facts,anchors=None):
 d={'concept_ids':list(cids),'teaching_block_ids':list(tbs),'fact_ids':list(facts)}
 if anchors: d['anchors']=list(anchors)
 return d
def prose(text,L,role='mechanism'): return {'type':'prose','text':text,'role':role,'lineage':L}
def fact_text(cid,fid): return F[cid][int(fid[1:])-1]
def fact_tbs(cid,fids): return [cid+'#'+tb['id'] for tb in bundles[cid]['teaching_blocks'] if set(tb['fact_ids']) & set(fids)]
def fact_blocks(cid,fids,tbs=None):
 return [prose(fact_text(cid,f),lin([cid],tbs if tbs is not None else fact_tbs(cid,[f]),[cid+'#'+f])) for f in fids]
def code(src,L,annotations=None,language='python'):
 return {'type':'code_walkthrough','language':language,'code':src.strip(),'annotations':annotations or [],'lineage':L}
def graph(labels,edges,L,diagram=False,alt=''):
 d={'type':'diagram' if diagram else 'process_flow','nodes':[{'id':str(i),'label':v} for i,v in enumerate(labels)],'edges':[{'from':str(e[0]),'to':str(e[1]),**({'label':e[2]} if len(e)>2 else {})} for e in edges],'alt_text':alt or '; '.join(labels),'lineage':L}
 if diagram:d['diagram_kind']='sequence'
 else:d['direction']='LR'
 return d

def visual(cid,L):
 c=contracts.get(cid,{})
 if cid=='sqlalchemy.retrieve_resource':
  x=c['bounded_selection']; field,value=next(iter(x['predicate'].items()))
  src=f'''async def by_identity(session, identity):
    entity = await session.get(Order, identity)
    if entity is None:
        return None
    return entity

async def by_condition(session):
    result = await session.scalars(
        select(Order).where(Order.{field} == {value!r}).limit({x['limit']})
    )
    entities = list(result)
    if not entities:
        return []
    return entities'''
  return [code(src,L,[{'start_line':2,'end_line':4,'text':'Identity lookup: handle None before attribute use.'},{'start_line':8,'end_line':13,'text':'Conditional entity selection: bound rows and handle emptiness.'}])]
 if cid=='sqlalchemy.transaction_boundaries':
  return [graph(['One session.begin() scope','first_order_write(session)','second_order_write(session)','Successful exit: commit; durable pair','Exceptional exit: rollback; discard uncommitted changes','Separate failed flush','Explicit rollback','Session reuse'],[(0,1),(1,2),(2,3,'success'),(1,4,'exception'),(2,4,'exception'),(5,6),(6,7)],L)]
 if cid=='auth.bearer_dependency':
  route=re.search(r'@app\.get\(([^)]+)\)',next(f['content'] for f in assets['ws.'+cid]['files'] if f['path']=='starter.py')).group(1)
  src='''from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

@app.get("/extract")
def handler(credential: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]):
    scheme = credential.scheme
    token = credential.credentials
    return {"extracted": True}'''
  src=src.replace(repr('/extract').replace("'",'"'),route)
  annotations=[{'start_line':6,'end_line':8,'text':'Extract scheme and credential text; do not return or log the token. This does not verify validity.'}]
  for case in c['cases']:
   src+='\n\nclient.get('+route+', headers='+repr(case['headers'])+')'
   line=len(src.splitlines()); annotations.append({'start_line':line,'end_line':line,'text':'Nonempty Bearer: extraction only.' if case['accepted_extraction'] else 'Rejected before handler execution with default auto_error=True.'})
  return [code(src,L,annotations)]
 if cid=='cache.redis_cache_aside':
  return [graph(['Identity + representation key','Cache lookup: disposable copy','Return cached copy','Load authoritative primary result','Populate same cache key','Return primary result'],[(0,1),(1,2,'hit'),(1,3,'miss'),(3,4),(4,5)],L)]
 if cid=='database.alembic_migrations':
  starter=next(f['content'] for f in assets['ws.'+cid]['files'] if f['path']=='starter.py')
  starter=starter.replace('# TODO: add review comments; this review-only file performs no schema changes.', '# Review: possible rename; clarify intent and correct before approval.\n    # Dropping the column deletes its data. No schema changes run here.')
  starter=starter.replace('# TODO: record data-loss risk, intent clarification, correction and verification.', '# Review: recreating the column may not recover deleted data.\n    # On a test database, verify alembic upgrade head and alembic downgrade revision.')
  return [code(starter,L,[{'start_line':1,'end_line':len(starter.splitlines()),'text':'Candidate only: review both directions for possible rename intent and data loss; exercise reversal on a test database.'}])]
 if cid=='database.service_query_indexes':
  src=f"CREATE INDEX {c['index_name']} ON {c['table']} ({c['column']});"
  return [code(src,L,[{'start_line':1,'end_line':1,'text':f"{c['index_name']}: index name; {c['table']}: table; {c['column']}: frequent equality-lookup column. Candidate benefit adds storage and write maintenance."}],language='sql')]
 if cid=='design.api_persistence_model_boundaries':
  left={'type':'diagram','diagram_kind':'container','nodes':[{'id':'stored','label':'Stored Order','fields':list(c['row'])}],'alt_text':'Stored row fields include storage-only processing and external_reference.','lineage':L}
  right={'type':'diagram','diagram_kind':'container','nodes':[{'id':'input','label':'PublicInput','fields':c['public_input_fields']},{'id':'output','label':'PublicOutput','fields':c['public_output_fields']}],'alt_text':'Separate public input and output omit storage-only fields. PublicOutput may validate attributes with ConfigDict(from_attributes=True).','lineage':L}
  return [{'type':'side_by_side','left':left,'right':right,'left_label':'Persistence mapping','right_label':'Public contracts','takeaway':'response_model=PublicOutput selects output fields; from_attributes=True supports validation, not automatic exposure.','lineage':L}]
 if cid=='fastapi.domain_error_translation':
  return [graph(['Recognized uniqueness failure','Rollback failed transaction before reuse','FailureClass at API boundary','Registered exception handler',f"Declared HTTP {c['declared_status']}: {c['public_reason']}",'Database exception text excluded'],[(0,1),(1,2),(2,3),(3,4),(3,5,'public boundary')],L)]
 if cid=='fastapi.public_error_envelopes':
  return [code(f'''from starlette.exceptions import HTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def public_http_error(request, exception):
    public_reason = choose_intended_public_reason(exception)
    return JSONResponse(
        status_code=exception.status_code,
        content={{{c['body_field']!r}: public_reason}},
        headers=exception.headers,
    )''',L,[{'start_line':4,'end_line':5,'text':'Starlette registration covers both HTTPException families.'},{'start_line':6,'end_line':10,'text':'choose_intended_public_reason is a supplied policy helper, not raw exception text. Preserve recognized status and headers.'}])]
 if cid=='fastapi_backend.proxy_header_trust':
  return [graph([f"Public HTTPS: {c['external_base']}",f"Trusted proxy: {c['trusted_proxy_source']}",f"Internal backend: {c['backend_base']}",f"root_path={c['stripped_prefix']!r}",'Public redirects and documentation','Untrusted sender: forwarded metadata rejected'],[(0,1),(1,2,'original scheme/client; strip prefix'),(2,3),(3,4,'external scheme + prefix'),(5,2,'not a trusted source')],L,True)]
 if cid=='integration.webhook_contracts':
  return [graph([f"{c['media_type']} body: order_id + event",'Typed-model validation','Invalid input: reject','Accepted delivery',f"Prompt declared {c['acknowledgement_status']} acknowledgment",'Deferred downstream work'],[(0,1),(1,2,'invalid'),(1,3,'valid'),(3,4),(3,5,'fixture permits deferral')],L,alt='Validation precedes accepted delivery. Invalid bodies are rejected. The declared acknowledgment does not depend on completion of permitted deferred work.')]
 if cid=='observability.request_correlation':
  ids=c['accepted_ids']; header=c['header_name']
  labels=[]; edges=[]
  for n,val in enumerate(ids):
   start=len(labels); labels.extend([f'Incoming {header}: {val}',f'Local events: {val}',f'Outbound receiver {header}: {val}']);edges.extend([(start,start+1),(start+1,start+2)])
  labels.extend(['Changed identifier at boundary: broken chain','Shared identifier between concurrent chains: mixed context'])
  return [graph(labels,edges,L,True,alt='Two concurrent chains retain separate registered identifiers from header through local records to the outbound receiver. Changed boundary values break a chain; shared values mix chains. These identifiers are not authority.')]
 if cid=='observability.service_signal_interpretation':
  return [{'type':'data_table','asset_ref':{'asset_id':'ds.service_signals','columns':[x['name'] for x in assets['ds.service_signals']['columns']]},'caption':'Equal-window synthetic dashboard. Group totals, rates and latency repeat across outcome rows; do not sum them across partitions. Only partition_count is additive.','lineage':L}]
 if cid=='rest.bounded_resource_listing':
  size=c['page_size_max'];field,value=next(iter(c['predicate'].items())); table='orders'
  blocks=[]
  for off in [0,size]:
   blocks.append({'type':'data_table','result_of':{'runtime':'sql','sql':f"SELECT id, quantity, processing FROM {table} WHERE {field} = {value!r} ORDER BY {c['primary_sort_column']}, {c['unique_key']} LIMIT {size} OFFSET {off}",'asset_mounts':[{'asset_id':'ds.orders','mount_path':table}]},'caption':f'Ordered page: OFFSET {off}, LIMIT {size}; quantity ties resolved by id.','lineage':L})
  return blocks
 if cid=='security.injection_resistant_inputs':
  return [code('''# Unsafe: supplied data becomes executable query text.
unsafe = "SELECT field FROM Entity WHERE field = '" + supplied_value + "'"

# Replacement: fixed structure and a separate bound value.
statement = text("SELECT field FROM Entity WHERE field = :value")
result = await session.execute(statement, {"value": supplied_value})''',L,[{'start_line':2,'end_line':2,'text':'Do not execute the unsafe interpolation.'},{'start_line':5,'end_line':6,'text':'The placeholder binds data, not arbitrary SQL structure.'}])]
 if cid=='sqlalchemy.create_resource':
  values=c['supplied_values']; labels=['Construct Entity with supplied fields: '+', '.join(f'{k}={v!r}' for k,v in values.items()),'session.add(entity): pending insert','await session.flush(): insert; generated identity when supported','await session.commit(): durable creation','await fresh_session.get(Entity, identity): independently verify identity and fields']
  return [graph(labels,[(i,i+1) for i in range(len(labels)-1)],L,True,alt='Creation states are separate boundaries. Flush may assign an identity but is not commit. Independent retrieval verifies committed values.')]
 if cid=='sqlalchemy.delete_resource':
  return [code(f'''async def remove(session, fresh_session):
    entity = await session.get(Order, {c['target_identity']})
    if entity is None:
        return None
    try:
        await session.delete(entity)
        await session.flush()
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    assert await fresh_session.get(Order, {c['target_identity']}) is None
    assert await fresh_session.get(Order, {c['other_identity']}) is not None''',L,[{'start_line':2,'end_line':4,'text':'Select the intended identity; handle absence.'},{'start_line':6,'end_line':11,'text':'Mark, flush, commit; roll back failed deletion.'},{'start_line':12,'end_line':13,'text':'Independent verification: target absent, other row preserved.'}])]
 if cid=='sqlalchemy.update_resource':
  fields=c['permitted_fields']; note=c['partial_update']['note']
  return [code(f'''async def update(session, fresh_session, changes):
    entity = await session.get(Order, {c['order_id']})
    if entity is None:
        return None
    supplied = changes.model_dump(exclude_unset=True)
    previous_quantity = entity.quantity
    try:
        for field, value in supplied.items():
            if field in {fields!r}:
                setattr(entity, field, value)
        await session.flush()
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    stored = await fresh_session.get(Order, entity.id)
    assert stored.note == supplied["note"]
    assert stored.quantity == previous_quantity''',L,[{'start_line':5,'end_line':10,'text':f'Fixture supplies only note={note!r}; omitted quantity stays unchanged.'},{'start_line':11,'end_line':15,'text':'Flush emits UPDATE; commit success or roll back failure before reuse.'},{'start_line':16,'end_line':18,'text':'Independent reload checks both changed and preserved fields.'}])]
 if cid=='auth.jwt_verification':
  return [code('''import jwt
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
    return protected_output(context)''',L,[{'start_line':7,'end_line':11,'text':'Require claim presence and verify configured values. Expiration and not-before constrain time validity.'},{'start_line':12,'end_line':18,'text':'Verification failure rejects the request; protected output cannot use unverified fallback claims.'}])]
 if cid=='cache.freshness_policy':
  return [graph([f"Old copy: {c['old_notes']}; set(..., ex=seconds)",'TTL: remaining seconds; -1 means no expiry',f"Committed primary change: {c['new_notes']}",f"Delete {c['cache_key']}",'TTL -2: absent key','Next read: cache miss','Reload changed primary value; populate with expiry'],[(i,i+1) for i in range(6)],L)]
 if cid=='cache.safe_failure_policy':
  return [code('''from redis.asyncio import Redis
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
        assert await safe_read(cache, key, load, seconds) == contract["primary_value"]''',L,[{'start_line':9,'end_line':12,'text':'Lookup exception boundary.'},{'start_line':15,'end_line':20,'text':'Primary loading stays outside cache catches; population failure does not discard the available value.'},{'start_line':22,'end_line':26,'text':'Controlled lookup and population failures verify the acceleration-only policy.'}])]
 raise ValueError(cid)

out={k:P[k] for k in ['schema_version','path_id','batch_id']};out['kind']='screens_part';out['tiles']=[]
for t in P['tiles']:
 tile={'tile_id':t['tile_id'],'title':' / '.join(bundles[c]['context']['concept_name'] for c in t['concept_ids']),'steps':[],'remediation_steps':[]}
 seen_explain={}; seen_remed=set()
 for s in t['steps']:
  cids=s['concept_ids']; cid=cids[0]; kind=s['type']; L=lin(cids,s['teaching_block_ids'],s['fact_ids'],s['anchors'])
  step={'step_id':s['step_id'],'type':kind,'concept_ids':cids,'title':bundles[cid]['context']['concept_name'],'lineage':L}
  if kind in ['check','hands_on']:
   step['eyebrow']='Check your understanding' if kind=='check' else 'Apply the rule'
   step['title']=('Distinguish: ' if kind=='check' else 'Practice: ')+bundles[cid]['context']['concept_name']
   key=(cid,tuple(s['fact_ids']))
   if key not in seen_remed:
    seen_remed.add(key); fids=[x.partition('#')[2] for x in s['fact_ids']]; rL=lin(cids,fact_tbs(cid,fids),s['fact_ids'],s['anchors'])
    rid=t['tile_id']+'.r'+str(len(tile['remediation_steps'])+1).zfill(2)
    remed={'step_id':rid,'type':'remediation','concept_ids':cids,'title':'Try the distinction again: '+bundles[cid]['context']['concept_name'],'lineage':rL,'blocks':fact_blocks(cid,fids)}
    # A single contrast in the same scenario, without supplying answer keys.
    allfids=[f['id'] for f in bundles[cid]['coverage']['required_facts']]
    contrastL=lin([cid],fact_tbs(cid,allfids),[cid+'#'+f for f in allfids])
    remed['blocks'].append(prose(CONTRAST[cid],contrastL,'misconception'))
    remed['title']='Try again: '+next((a.partition('#assessment:')[2].replace('_',' ') for a in s['anchors'] if '#assessment:' in a),bundles[cid]['context']['concept_name'])
    if cid in ('observability.service_signal_interpretation','rest.bounded_resource_listing'):
     aid='ds.service_signals' if cid.startswith('observability.') else 'ds.orders'
     cols=[x['name'] for x in assets[aid]['columns']]
     remed['blocks'].append({'type':'data_table','asset_ref':{'asset_id':aid,'columns':cols},'caption':'Use the same synthetic fixture to trace the distinction.','lineage':contrastL})
    tile['remediation_steps'].append(remed)
  elif kind=='video':
   step['title']='Follow the sequence: '+bundles[cid]['context']['concept_name']
   step['blocks']=[{'type':'media_group','segment_ids':s['segment_ids']}]
  elif kind=='recap':
   step['title']='Keep the boundaries clear';step['blocks']=[]
   for cc in cids:
    # Short glossary-grounded takeaways; detailed rule teaching already occurred above.
    fids=[f['id'] for f in bundles[cc]['coverage']['required_facts']]
    step['blocks'].append(prose(CONTRAST[cc],lin([cc],fact_tbs(cc,fids),[cc+'#'+f for f in fids]),'takeaway'))
   nxt=next((pt for pt in P['tiles'] if pt['tile_id']==t['next_tile_id']),None)
   nextcid=nxt['concept_ids'][0] if nxt else next(iter(bundles[cids[-1]]['context']['blocked_future_concepts']))
   # For the final batch tile, only name the next idea from glossary names; do not teach its absent facts.
   if not nxt:
    ordered_names=list(G['names']); nextcid=ordered_names[ordered_names.index(cids[-1])+1]
   step['blocks'].append({'type':'up_next','title':G['names'][nextcid],'text':'Next: '+t['next_tile_id']+'.'})
  else:
   n=seen_explain.get(cid,0);seen_explain[cid]=n+1
   step['blocks']=[]
   if n==0:
    fids=[]
    for qtb in s['teaching_block_ids']:
     tb=next(tb for tb in bundles[cid]['teaching_blocks'] if tb['id']==qtb.partition('#')[2])
     for f in tb['fact_ids']:
      if f not in fids:fids.append(f)
    step['blocks']=fact_blocks(cid,fids,s['teaching_block_ids'])
    if s['planned_visual_block_type']:
     step['blocks']+=visual(cid,L)
    # Single planned screen also includes the contextual mental model/walkthrough.
    if any(x.endswith('#tb5') for x in s['teaching_block_ids']):
     step['blocks'].append(prose(scenario_text(cid,N[cid][0]),L,'walkthrough'))
   else:
    text=scenario_text(cid,N[cid][min(n-1,len(N[cid])-1)])
    step['blocks']=[prose(text,L,'mental_model' if n==1 else 'walkthrough')]
   step['title']=('Choose the boundary: ' if n==0 else 'Trace the distinction: ')+bundles[cid]['context']['concept_name']
  tile['steps'].append(step)
 out['tiles'].append(tile)
(B/'screens.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('Wrote',len(out['tiles']),'tiles;',sum(len(t['steps']) for t in out['tiles']),'planned steps;',sum(len(t['remediation_steps']) for t in out['tiles']),'remediation steps')
