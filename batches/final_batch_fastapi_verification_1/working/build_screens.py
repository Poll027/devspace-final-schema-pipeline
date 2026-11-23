import json, re, ast, copy, pprint
from pathlib import Path
P=Path('batches/final_batch_verification_1')
plan=json.loads((P/'tile_plans.json').read_text()); glossary=json.loads((P/'inputs/path_glossary_bundle.json').read_text()); registry=json.loads((P/'scenario_asset_registry.json').read_text())
B={b['context']['concept_id']:b for b in glossary['bundles']}; A={a['asset_id']:a for a in registry['assets']}
C=list(B)
def file(cid,name):return next(f['content'] for f in A['ws.'+cid]['files'] if f['path']==name)
def assigned(source,name):
 for n in ast.walk(ast.parse(source)):
  if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets):return ast.literal_eval(n.value)
 raise ValueError(name)
# Re-voiced facts: no fixture outputs or answer values are authored here.
F={
C[0]:['Bind structured JSON by defining a BaseModel subclass and typing a handler parameter with that model.','FastAPI reads JSON, converts compatible values, validates the declared model, then gives the handler a model instance.','Path-declared parameters come from the path; ordinary scalars generally come from the query; model parameters come from the body. One operation can receive all three.'],
C[1]:['Acquire the resource before yield. The dependency supplies the yielded resource to the operation.','Surround yield with try/finally and release the resource in finally, covering successful use and exceptions.','Default request scope ends after response sending. Depends(provider, scope="function") ends after handler completion, before the response is sent.','If you catch an exception without intentionally handling it, re-raise it. Do not conceal the failure from FastAPI.'],
C[2]:['An interpretable event log says when and where an event happened, its type and severity, and enough context to understand the outcome.','For a failure, use consistent field names for timestamp, application or code location, event type, severity, result status and reason—not just unexplained free text.','logger.error(message, extra=event_fields) attaches fields to the LogRecord. Configure the existing formatter or collector to preserve their names, and avoid custom keys that collide with reserved LogRecord attributes.'],
C[3]:['For known destinations, map untrusted provider input to an allowed destination instead of accepting an arbitrary outbound URL.','For public-only access, reject private, loopback, link-local and other non-public addresses, including IPv6 equivalents.','Validate the resolved address actually used for the connection. Checking a hostname earlier is insufficient against a DNS rebinding gap.','Disable automatic redirects or enforce the same destination checks on every redirect target. An allowed starting URL can redirect somewhere forbidden.'],
C[4]:['In one multipart handler, declare metadata with Annotated[Type, Form()] and the file with Annotated[UploadFile, File()]. Install python-multipart for parsing.','UploadFile uses a spooled file rather than requiring the entire upload as in-memory bytes. Its read, seek and close methods are asynchronous.','Set a finite RequestBodyLimitMiddleware max_body_size. Count actual incoming bytes, including multipart overhead; exceeding that limit returns 413.','request.form(max_files=..., max_fields=..., max_part_size=...) separately limits file count, field count and non-file field size. These limits do not replace the total-body limit.','Reject disallowed content types and validate fields before processing. When finished, release the upload with await file.close().'],
C[5]:['Use app.add_middleware(CORSMiddleware, ...) with allow_origins, allow_methods, allow_headers and allow_credentials matching the browser client’s actual needs.','Defaults are restrictive: allowed methods default to GET, and credentials default to false.','With allow_credentials=True, specify origins, methods and headers explicitly rather than using wildcard lists.','CORS grants browser access permission; endpoint access-control checks remain separate and necessary.'],
C[6]:['FastAPI normally caches a dependency result within a request when several dependants declare the same dependency.','Use Depends(provider, use_cache=False) on a declaration that needs fresh execution instead of the cached result.','Check that two dependants receive the same provider result in one request, then examine a fresh request independently. This cache is request-local, not application-wide storage.'],
C[7]:['Create TestClient(app), send a request such as client.get(...), and assert both response.status_code and response.json() in a pytest test_ function.','When setup and teardown matter, use with TestClient(app) as client to execute application lifespan.','A TestClient request exercises route and dependency resolution through the application. Calling the handler directly does not exercise that HTTP boundary.'],
C[8]:['A default determines requiredness; a type that admits None determines nullability. These are different questions.','A nullable field with no default still requires presence. field: Type | None = None allows both omission and explicit null.','Send absence, explicit JSON null and a concrete value as separate requests. Compare each with the declared default and nullable type.'],
C[9]:['FastAPI normally serves the generated OpenAPI document at /openapi.json. It describes operations and data schemas.','Typed body declarations contribute input schemas; response models contribute output schemas to the generated public contract.','Locate the endpoint’s method entry under paths, then follow its schema references into components to find the public input and output definitions.'],
C[10]:['TrustedHostMiddleware checks Host against allowed_hosts. An unallowed host receives 400.','Register TrustedHostMiddleware through app.add_middleware with domain names in allowed_hosts. *.example.com allows subdomains; ["*"] allows any host.','www_redirect defaults to true and can redirect an allowed non-www host to its www counterpart. Account for redirects when checking the allowlist’s response.'],
C[11]:['Access tokens, passwords, primary secrets and sensitive personal data should usually not appear directly in logs. Remove or mask them under the logging policy.','Inspect supplemental context as well as the message: connection strings, session identifiers and other sensitive values can appear there.','Trigger a failure with recognizable synthetic sensitive values. Inspect emitted records to confirm prohibited values are removed while intended event fields remain.'],
C[12]:['AsyncSession holds mutable state for database work. It is unsafe to share across concurrent tasks; give each concurrent unit of work a separate session.','Bind async_sessionmaker to an async engine. async with session_factory() as session obtains and closes a session for the request’s unit of work.','A request dependency can yield the session from that async context. The context still owns cleanup on normal and exceptional exit.'],
C[13]:['Graceful termination stops old processes accepting new connections and lets active responses and background tasks finish within configured limits.','Set --timeout-graceful-shutdown seconds as Uvicorn’s maximum wait before it starts terminating remaining requests.','Terminate during an active request. Observe whether its response completes within the limit and whether lifespan cleanup releases shared application resources.'],
C[14]:['Failed liveness can cause a container restart. Failed readiness removes service-traffic eligibility without requiring restart.','Readiness can reflect temporary required-backend unavailability even when the process remains alive.','Configure separate livenessProbe and readinessProbe HTTP checks with path, port, periodSeconds and failureThreshold matching the intended restart and traffic contracts.','HTTP probes count statuses 200 through 399 as success; other statuses are failure.']}
# Later explainers elaborate only their assigned teaching blocks.
LATER={
C[0]:['Read the signature as a source map: the customer identifier is path input, an ordinary scalar option generally comes from the query, and OrderInput is structured body input. For the body, trace JSON reading, compatible conversion, model validation and delivery of the model instance. A body field is not an assumed query parameter.','OrderInput declares the body’s shape. Add a body parameter typed with it while keeping the path identifier and ordinary scalar option. Trace JSON to compatible conversion to validation to the model supplied to the handler. A combined operation can receive these inputs together; the model declaration identifies the structured body rather than scattering its fields into assumed query inputs.'],
C[1]:['Trace acquisition, yield and operation use separately. Put release in finally so both successful and exceptional paths clean up. Default request scope ends after response sending; function scope ends after handler completion, before sending. If a caught exception was not intentionally handled, re-raise it. Yield is not a promise that every dependency ends at handler completion.'],
C[2]:['Follow the fields from event_fields into the LogRecord and then into the emitted record. Use timestamp, code location, event type, severity, result status and reason consistently. Passing extra is not enough: inspect the existing formatter or collector to ensure those names survive. Custom names must not collide with reserved LogRecord attributes.'],
C[3]:['Trace three boundaries, not just one hostname: requested provider, address actually connected to, and redirect target. Map known providers to allowed destinations. Reject non-public IPv4 and IPv6 addresses for public-only access, and validate the resolved address used by the connection. Disable redirects or check each target. A permitted-looking hostname alone leaves the connected-address and redirect boundaries unverified.'],
C[4]:['Treat limits as separate controls. Form and File declarations need python-multipart; a spooled UploadFile offers asynchronous resource methods, not unlimited input. The finite body budget counts actual bytes including overhead and returns 413 on excess. Parser options bound file count, field count and non-file field size, but do not replace that budget. Validate fields and content type before processing, and close the file afterward.'],
C[5]:['The shop browser needs its origin, methods and headers listed explicitly, with credentials enabled for this scenario. Defaults alone allow GET and leave credentials false. When credentials are true, do not use wildcard lists for origins, methods or headers. CORS answers a browser-permission question, not whether an endpoint should grant access. Keep endpoint access-control checks separate.'],
C[6]:['Draw request A around its provider result and both dependants. Verify reuse inside that boundary, then inspect request B independently. On a declaration needing another execution, use Depends(provider, use_cache=False). The normal cache reduces repeat execution within one request; it does not turn a request-specific value into storage shared by all clients.'],
C[7]:['Specify an HTTP exchange, not merely a call that avoids crashing: method, path, expected status and expected public JSON. TestClient sends it through route and dependency resolution. Add the context manager when lifespan setup and teardown belong in the test. A direct handler call checks a different boundary and cannot establish the registered endpoint’s complete exchange.','Use the supplied order fixture to make separate status and JSON assertions in test_get_order. Send the GET through TestClient rather than invoking get_order directly. Run the test_ function with pytest; use the context manager to execute lifespan when the case needs it. The status assertion checks the HTTP outcome, and the JSON assertion checks public content. Neither substitutes for the other.'],
C[8]:['Keep two columns in your mental model: must the field appear, and may its value be null? note: str | None requires presence but admits null. Adding = None allows omission too. Test missing, null and a concrete string separately against those declarations; “optional” alone does not identify both rules.','Start with the supplied nullable note declaration, then add its default. Send each supplied body separately before and after the change. Without a default, the field must appear even though null is allowed; with = None, omission is also allowed. Compare the declared presence rule with the admitted values instead of collapsing all three requests into one optional case.'],
C[9]:['Navigate by endpoint path and method first. Follow the body and response references into components, then compare their field definitions with the typed declarations. OpenAPI is generated from those declarations; it describes operations and schemas. Reading the document does not establish every runtime outcome, and schema details need not be inline in the operation entry.','In the supplied POST /orders excerpt, follow the request-body reference to OrderInput and the response reference to OrderOutput. The input definition has quantity; the output definition has id. These are different public definitions contributed by the body and response-model declarations. Retrieve the generated document at /openapi.json and navigate through paths and components rather than assuming every field is inline. This is contract structure, not proof of every runtime result.'],
C[12]:['Separate the engine-bound factory from the mutable sessions it creates. Concurrent request A and request B need separate sessions. Each request’s async context owns closure, including exceptional exit. Yield supplies the session to the operation without transferring that cleanup responsibility. A shared factory is not a shared AsyncSession.','Bind the factory to the async engine, then open a session with async with for each request’s work. Yield that session from inside the context so both normal and exceptional exit close it. Draw session A and session B separately for concurrent requests. Sharing factory setup does not permit both tasks to borrow one mutable session, and cleanup must not depend only on a successful return.'],
C[14]:['Configure each probe’s path, port, periodSeconds and failureThreshold for its own contract. A temporary required-backend outage can leave liveness successful while readiness removes traffic eligibility. Failed liveness can cause restart; failed readiness does not require it. Classify HTTP statuses 200 through 399 as success, including 3xx. An “unready” response body is insufficient if the status still counts as successful.']}
CONTRAST={
C[0]:'For the order handler, a body typed as OrderInput is structured JSON input, not an ordinary scalar query option.',
C[1]:'For the supplied resource, cleanup in finally covers failure too; cleanup only on the successful return branch does not.',
C[2]:'For the supplied order failure, attaching extra fields differs from preserving them in emitted output.',
C[3]:'For the supplied provider lookup, selecting an allowed URL is only the first boundary, not connected-address or redirect enforcement.',
C[4]:'For the supplied attachment, a permitted content type does not excuse invalid metadata; both must pass before processing.',
C[5]:'For the shop browser, explicit client permissions differ from endpoint access control; CORS does not replace it.',
C[6]:'The order provider can reuse a result inside request A without making that result application-wide storage for request B.',
C[7]:'For order retrieval, an HTTP request through TestClient differs from a direct call to get_order.',
C[8]:'For the supplied note, admitting null differs from permitting omission; only the declaration with a default permits both.',
C[9]:'For POST /orders, a schema reference differs from the field definition it points to in components.',
C[10]:'For the supplied host policy, a rejected host differs from an allowed host redirected to its www counterpart.',
C[11]:'For the synthetic order failure, a safe main message can still have prohibited values in supplemental context.',
C[12]:'For concurrent request A and request B, sharing the engine-bound factory differs from sharing one mutable session.',
C[13]:'For the delayed order request, response completion does not by itself establish that the shared client was closed.',
C[14]:'During the supplied backend outage, an alive process can be unready; removing traffic differs from restarting it.'}

TARGETED={
 (C[0],('f2',)):'For OrderInput, the handler receives a model after compatible conversion and validation, not merely an assumed-valid JSON body.',
 (C[1],('f2','f4')):'For the supplied resource, cleanup on failure and failure visibility are separate: finally releases it, while re-raising an unhandled exception keeps the failure visible.',
 (C[3],('f2',)):'For public-only outbound access, a loopback address is forbidden even in IPv6 form; changing address family does not change that boundary.',
 (C[3],('f3',)):'For the provider lookup, an earlier hostname check differs from validating the resolved address actually used for the connection.',
 (C[3],('f1','f4')):'A configured provider destination is allowed as a starting point, but a redirect from it must still satisfy the destination policy or be disabled.',
 (C[5],('f2',)):'For the shop client, do not assume permissive defaults: default allowed methods are GET and default credentials are false.',
 (C[6],('f2',)):'For a dependant needing a fresh provider execution, use_cache=False differs from relying on the normally cached result.',
 (C[6],('f1',)):'Within one order request, multiple dependants declaring the same provider normally reuse its returned value rather than requiring repeated execution.',
 (C[7],('f1','f2')):'For the supplied order test, an HTTP status assertion does not substitute for the JSON assertion; use the TestClient context when lifespan must run.',
 (C[8],('f2','f3')):'For the supplied note bodies, omitted and explicit null are different requests. Without a default only the explicit null satisfies presence; adding = None permits omission too.',
 (C[9],('f1',)):'The order operation path differs from the document location: /openapi.json normally serves the generated description of operations and schemas.',
 (C[12],('f2','f3')):'For the order request, obtaining a session is not the whole ownership boundary: yield stays inside async with so context exit closes it even on failure.',
 (C[12],('f1',)):'Concurrent request A and request B need separate mutable sessions rather than concurrent use of one AsyncSession.',
 (C[14],('f1','f3','f4')):'For the supplied HTTP probe contract, an unready body with a successful status still counts as probe success. Failure thresholds belong to separate restart and traffic-eligibility decisions.'
}
def lineage(cids,tbs,facts,anchors=None):
 d={'concept_ids':cids,'teaching_block_ids':tbs,'fact_ids':facts}
 if anchors is not None:d['anchors']=anchors
 return d
def prose(text,lin,role='mechanism'):return {'type':'prose','text':text,'role':role,'lineage':copy.deepcopy(lin)}
def code(text,lin,annotations=None,language='python'):
 d={'type':'code_walkthrough','language':language,'code':text,'reveal':'all','lineage':copy.deepcopy(lin)}
 if annotations:d['annotations']=[{'start_line':i,'end_line':j,'text':s} for i,j,s in annotations]
 return d
def flow(labels,edges,lin,title):return {'type':'process_flow','title':title,'direction':'TB','nodes':[{'id':k,'label':v} for k,v in labels.items()],'edges':[{'from':a,'to':b,**({'label':c} if c else {})} for a,b,c in edges],'alt_text':title+': '+'; '.join(labels.values()),'lineage':copy.deepcopy(lin)}
def diagram(nodes,edges,lin,title,kind='mapping'):
 return {'type':'diagram','diagram_kind':kind,'title':title,'nodes':[{'id':k,'label':v,**({'group':g} if g else {})} for k,v,g in nodes],'edges':[{'from':a,'to':b,'label':c,'directed':True} for a,b,c in edges],'layout':'auto','alt_text':title+': '+'; '.join(v for _,v,_ in nodes),'lineage':copy.deepcopy(lin)}
def visual(cid,lin):
 lin=copy.deepcopy(lin);lin['anchors']=[cid+'#visual']
 if cid==C[0]:
  s=file(cid,'main.py');s=s.replace("option: str = 'standard'", "body: OrderInput, option: str = 'standard'")
  s='\n'.join(x for x in s.splitlines() if '# TODO' not in x)+'\n'
  annotations=[]
  for i,l in enumerate(s.splitlines(),1):
   if 'class OrderInput' in l:annotations.append((i,i+1,'BaseModel describes the structured body.'))
   if 'def create_order' in l:annotations.append((i,i,'customer_id: path; option: generally query; body: JSON model.'))
  return [code(s,lin,annotations)]
 if cid==C[1]:
  return [flow({'acquire':'Acquire resource','yield':'Yield to operation','use':'Operation uses resource','done':'Handler completion','choice':'Declared scope','function':'Function scope: cleanup','response':'Send response','request':'Default request scope: cleanup','exception':'Exceptional use','raise':'Re-raise unhandled exception','finally':'finally: release resource'},[('acquire','yield',''),('yield','use',''),('use','done','success'),('done','choice',''),('choice','function','scope="function"'),('function','response',''),('choice','response','default request scope'),('response','request','default only'),('use','exception','failure'),('exception','raise','not intentionally handled'),('raise','finally','')],lin,'Resource ownership and scope boundaries')]
 if cid==C[2]:
  src=file(cid,'support.py');values=assigned(src,'failure_values'); fields=list(values)
  before=src+"\nlogger.error('failed')\nprint(captured_output.getvalue(), end='')\n"
  fmt=' '.join(k+'=%('+k+')s' for k in fields)
  after=src+'\nevent_fields = dict(failure_values)\nexisting_handler.setFormatter(logging.Formatter('+repr(fmt)+"))\nlogger.error('order failure', extra=event_fields)\nprint(captured_output.getvalue(), end='')\n"
  return [{'type':'before_after','before':code(before,lin),'after':code(after,lin),'change_summary':'Before: unexplained message. After: preserve the six named failure fields through the existing formatter. Emitted output is computed, not an observed production event.','lineage':lin}]
 if cid==C[3]:
  dest=assigned(file(cid,'starter.py'),'allowed_destinations')
  return [diagram([('input','Requested provider',None),('map','Allowlist: '+ '; '.join(k+' → '+v for k,v in dest.items()),None),('address','Validate resolved address actually used',None),('deny','Reject private, loopback, link-local and other non-public IPv4/IPv6',None),('redirect','Redirect target: same checks or disable automatic redirects',None),('public','Public-only connection boundary',None)],[('input','map','reject arbitrary destinations'),('map','address','not just earlier hostname check'),('address','deny','non-public'),('address','public','policy permits'),('public','redirect','redirect response'),('redirect','map','reapply destination checks')],lin,'Outbound destination trust boundary','network')]
 if cid==C[4]:
  src=file(cid,'support.py'); route=src[src.index('class BoundedMultipartRoute'):]
  endpoint_path=re.search(r"@app.post\('([^']+)'\)",file(cid,'main.py')).group(1)
  rejection_status=next(n.left.value for n in ast.walk(ast.parse(file(cid,'harness.py'))) if isinstance(n,ast.Compare) and isinstance(n.left,ast.Constant) and n.left.value == 400)
  scaffold="from typing import Annotated\nfrom fastapi import FastAPI, Form, File, UploadFile, HTTPException\nfrom support import (RequestBodyLimitMiddleware, BoundedMultipartRoute,\n                     budgets, permitted_content_types)\napp = FastAPI()\napp.router.route_class = BoundedMultipartRoute\napp.add_middleware(RequestBodyLimitMiddleware,\n                   max_body_size=budgets['max_body_size'])\n@app.post('/orders/attachments')\nasync def attachment(metadata: Annotated[str, Form()],\n                     file: Annotated[UploadFile, File()]):\n    try:\n        if file.content_type not in permitted_content_types:\n            raise HTTPException(status_code=400, detail='disallowed content type')\n        if len(metadata) > budgets['metadata_max_length']:\n            raise HTTPException(status_code=400, detail='invalid metadata')\n        data = await file.read(budgets['read_size'])\n        await file.seek(0)\n        return {'metadata': metadata}\n    finally:\n        await file.close()\n"
  scaffold=scaffold.replace('/orders/attachments',endpoint_path).replace('status_code=400','status_code='+str(rejection_status))
  return [code(scaffold,lin,[(6,8,'Total actual-body-byte boundary, including multipart overhead.'),(10,11,'Typed form metadata and spooled file; python-multipart required.'),(12,16,'Validate before reading.'),(20,21,'Asynchronous cleanup on success or rejection.')]),code('from fastapi.routing import APIRoute\nfrom support import budgets\n'+route,lin,[(6,8,'Parser limits run before automatic typed parameter binding; non-file part size is separate from the total body budget.')])]
 if cid==C[5]:
  # Required scenario values are supplied in the registered starter comments.
  src=file(cid,'main.py');origin=re.search(r'https://[^ ]+',src).group(0);methods=re.search(r'with (GET), (POST),',src).groups();header=re.search(r'(Content-Type)',src).group(1)
  s='\n'.join(x for x in src.splitlines() if '# TODO' not in x)+'\napp.add_middleware(CORSMiddleware,\n    allow_origins='+repr([origin])+',\n    allow_methods='+repr(list(methods))+',\n    allow_headers='+repr([header])+',\n    allow_credentials=True)\n'
  return [code(s,lin,[(4,8,'Explicit shop-client permissions; credentials enabled. Browser permission does not replace endpoint access checks.')])]
 if cid==C[6]:
  return [diagram([('a','Request A','A'),('pa','Provider execution → value A','A'),('a1','First dependant: same value A','A'),('a2','Second dependant: same value A','A'),('fresh','Depends(provider, use_cache=False): fresh execution','A'),('b','Request B','B'),('pb','Independent provider execution → value B','B'),('b1','First dependant: value B','B'),('b2','Second dependant: value B','B')],[('a','pa','normal request-local cache'),('pa','a1','reuse'),('pa','a2','reuse'),('a','fresh','explicit uncached declaration'),('b','pb','new request'),('pb','b1','reuse'),('pb','b2','reuse')],lin,'Separate request-cache boundaries','container')]
 if cid==C[7]:
  ds=A['ds.orders']; row=dict(zip([c['name'] for c in ds['columns']],ds['rows'][0]));app=file(cid,'app.py');path=re.search(r"@app.get\('([^']+)'\)",app).group(1)
  # The expected fixture body and status are read from the registered app/fixture.
  tb=next(t for t in B[cid]['teaching_blocks'] if t['id']=='tb5')['content']
  example=re.search(r'```python\n(.*?)```',tb,re.S).group(1)
  status=next(n.comparators[0].value for n in ast.walk(ast.parse(example)) if isinstance(n,ast.Compare) and isinstance(n.left,ast.Attribute) and n.left.attr=='status_code')
  s='from fastapi.testclient import TestClient\nfrom app import app\n\ndef test_get_order():\n    with TestClient(app) as client:\n        response = client.get('+repr(path)+')\n        assert response.status_code == '+str(status)+'\n        assert response.json() == '+repr(row)+'\n'
  return [code(s,lin,[(5,5,'Context runs lifespan setup and teardown.'),(6,6,'HTTP request exercises routing and dependency resolution.'),(7,8,'Independent status and public JSON assertions; pytest executes test_get_order.')])]
 if cid==C[8]:
  # Compute the presence comparison as a relational rendering of the glossary rule.
  # Inputs are the three registered requests, not authored result rows.
  requests=json.loads(file(cid,'requests.json'))
  field=next(n for n in ast.walk(ast.parse(file(cid,'main.py'))) if isinstance(n,ast.AnnAssign)).target.id
  def literal(v):return 'NULL' if v is None else "'"+str(v).replace("'","''")+"'"
  rows=[]
  for i,r in enumerate(requests):rows.append('('+str(i+1)+','+('TRUE' if field in r else 'FALSE')+','+literal(r.get(field))+')')
  sql='WITH inputs(ordinal, supplied, note) AS (VALUES '+','.join(rows)+'''), declarations(label, has_default) AS (VALUES ('note: str | None', FALSE), ('note: str | None = None', TRUE))
SELECT CASE WHEN NOT supplied THEN 'omitted' WHEN note IS NULL THEN 'explicit null' ELSE 'concrete string' END AS input,
 label AS declaration, (supplied OR has_default) AS accepted,
 CASE WHEN supplied OR has_default THEN note ELSE NULL END AS resulting_note
FROM orders CROSS JOIN inputs CROSS JOIN declarations ORDER BY ordinal, has_default'''
  return [{'type':'data_table','result_of':{'runtime':'sql','sql':sql,'asset_mounts':[{'asset_id':'ds.orders','mount_path':'orders'}]},'caption':'Declaration comparison derived from the presence rule and supplied request bodies, not an HTTP run. Read resulting_note only where accepted is true.','lineage':lin}]
 if cid==C[9]:
  schema=json.loads(file(cid,'openapi_excerpt.json'))
  s='import json\nschema = '+pprint.pformat(schema, width=88, sort_dicts=False)+'\nprint(json.dumps(schema, indent=2))\n'
  # Represent the supplied excerpt verbatim as executable Python; no output is typed.
  return [code(s,lin,[(2,2,'POST /orders: requestBody reference → components.schemas.OrderInput; response reference → OrderOutput. quantity is input, id is output.')])]
 if cid==C[10]:
  return [{'type':'data_table','asset_ref':{'asset_id':'ds.host_checks','columns':[c['name'] for c in A['ds.host_checks']['columns']]},'caption':'Authored host-policy comparison. Null redirect status means the glossary does not specify its code.','lineage':lin}]
 if cid==C[11]:
  vals=json.loads(file(cid,'synthetic_values.json'));support=file(cid,'support.py')
  invoke='result = failure_harness(token='+repr(vals['token'])+', connection_string='+repr(vals['connection_string'])+")\nprint(result['text'], end='')\n"
  before=support.replace("text = text.replace(secret, '[REDACTED]')",'text = text')+'\n'+invoke
  after=support+'\n'+invoke
  return [{'type':'before_after','before':code(before,lin),'after':code(after,lin),'change_summary':'Before: the same synthetic failure with masking disabled. After: policy masks prohibited strings throughout message and context while retaining the event field. Output is computed from this fixture.','lineage':lin}]
 if cid==C[12]:
  return [diagram([('factory','async_sessionmaker(async engine)',None),('sa','Session A: mutable work state','request A'),('sb','Session B: mutable work state','request B'),('ya','Dependency yields session A','request A'),('yb','Dependency yields session B','request B'),('ca','async context exit closes A','request A'),('cb','async context exit closes B','request B')],[('factory','sa','async with session_factory()'),('factory','sb','async with session_factory()'),('sa','ya','operation use'),('sb','yb','operation use'),('ya','ca','normal or exceptional exit'),('yb','cb','normal or exceptional exit')],lin,'One factory, separate concurrent sessions','container')]
 if cid==C[13]:
  script=file(cid,'run.sh');limit=re.search(r'(\d+)-second limit',script).group(1)
  return [flow({'active':'Controlled order request active','terminate':'Initiate termination','stop':'Old processes stop accepting new connections','wait':'Responses and background tasks may finish; maximum wait '+limit+' seconds','limit':'Wait limit reached: Uvicorn starts terminating remaining requests','cleanup':'Lifespan cleanup releases shared client','evidence':'Inspect recorded response outcome and client.is_closed'},[('active','terminate',''),('terminate','stop',''),('stop','wait',''),('wait','limit','remaining work at boundary'),('wait','cleanup','finish within limit'),('limit','cleanup',''),('cleanup','evidence','verify, do not assume')],lin,'Bounded shutdown and evidence to inspect')]
 if cid==C[14]:
  vals=json.loads(file(cid,'supplied_values.json'))
  def label(key):
   d=vals[key];return key+': '+d['path']+':'+str(d['port'])+', periodSeconds='+str(d['periodSeconds'])+', failureThreshold='+str(d['failureThreshold'])
  return [flow({'outage':'Temporary required-backend outage; process alive','live':label('livenessProbe'),'ready':label('readinessProbe'),'status':'HTTP 200–399 success; other statuses failure','lf':'Liveness failures reach threshold','rf':'Readiness failures reach threshold','restart':'Can cause container restart','traffic':'Remove service-traffic eligibility; no restart required'},[('outage','live','can remain successful'),('outage','ready','can fail'),('live','status','classify response'),('ready','status','classify response'),('status','lf','liveness failure'),('status','rf','readiness failure'),('lf','restart',''),('rf','traffic','')],lin,'Separate restart and traffic decisions')]
 raise ValueError(cid)

TAKE={
C[0]:'Type a model parameter for JSON; trace conversion and validation; distinguish path, ordinary query and body inputs.',
C[1]:'Acquire before yield; release in finally; distinguish request and function scope; re-raise unhandled exceptions.',
C[2]:'Name failure fields consistently, attach them with extra, avoid reserved names and preserve them in emitted output.',
C[3]:'Allowlist destinations; reject non-public IPv4/IPv6; validate connected addresses; disable or recheck redirects.',
C[4]:'Bind Form/File inputs; use spooled asynchronous uploads; enforce total and parser limits separately; validate before processing and close files.',
C[5]:'Match explicit CORS lists to the browser; remember restrictive defaults; credentials require explicit lists; endpoint access checks remain separate.',
C[6]:'Verify request-local reuse, check a fresh request independently, and request fresh execution with use_cache=False when needed.',
C[7]:'Use a pytest test_ function to request the HTTP endpoint and assert status plus JSON; include lifespan through the TestClient context when needed.',
C[8]:'Defaults govern presence; nullable types govern null. Compare omitted, null and concrete inputs separately.',
C[9]:'Locate /openapi.json; connect typed body and response declarations to schemas; follow path/method references into components.',
C[10]:'Check Host against domain policies; distinguish rejection from www redirection; an all-host wildcard permits every host.',
C[11]:'Apply logging policy to sensitive values in both message and context; verify emitted records with synthetic failures while retaining intended fields.',
C[12]:'Share factory setup, not mutable sessions across concurrent tasks. Obtain sessions with async contexts and yield without losing normal or exceptional cleanup.',
C[13]:'Bound shutdown waiting, terminate during active work, and verify response completion plus shared-resource cleanup.',
C[14]:'Separate liveness restart and readiness traffic contracts; temporary backend outages can affect readiness while alive; HTTP 200–399 counts as probe success.'}
# Next tiles inside the batch are identified by the plan, not guessed.
bytile={t['tile_id']:t for t in plan['tiles']}
intro_count={};out={'schema_version':plan['schema_version'],'kind':'screens_part','path_id':plan['path_id'],'batch_id':plan['batch_id'],'tiles':[]}
for tile in plan['tiles']:
 title=' · '.join(B[c]['context']['concept_name'] for c in tile['concept_ids'])
 result={'tile_id':tile['tile_id'],'title':title,'steps':[],'remediation_steps':[]}
 for s in tile['steps']:
  cid=s['concept_ids'][0]; lin=lineage(s['concept_ids'],s['teaching_block_ids'],s['fact_ids'],s['anchors'])
  step={'step_id':s['step_id'],'type':s['type'],'concept_ids':s['concept_ids'],'title':B[cid]['context']['concept_name'],'eyebrow':s['type'].replace('_',' ').title(),'lineage':lin}
  if s['type']=='explainer':
   idx=intro_count.get(cid,0);intro_count[cid]=idx+1
   if idx==0:
    step['title']='Declare the boundary: '+B[cid]['context']['concept_name']
    step['blocks']=[]
    for f in s['fact_ids']:
     fid=f.split('#')[1];idxf=int(fid[1:])-1
     tbs=[cid+'#'+t['id'] for t in B[cid]['teaching_blocks'] if cid+'#'+t['id'] in s['teaching_block_ids'] and fid in t['fact_ids']]
     if idxf==0:tbs=list(dict.fromkeys([tb for tb in s['teaching_block_ids'] if tb.endswith('#tb1')]+tbs))
     step['blocks'].append(prose(F[cid][idxf],lineage([cid],tbs,[f])))
    step['blocks']+=visual(cid,lin)
   else:
    step['title']='Trace the contract' if idx==1 else 'Work through the supplied example'
    text=LATER[cid][idx-1]
    step['blocks']=[prose(text,lin,'mental_model' if idx==1 else 'walkthrough')]
  elif s['type']=='video':
   step['title']='Optional deeper walkthrough'
   step['blocks']=[{'type':'media_group','segment_ids':s['segment_ids']}]
  elif s['type'] in ['check','hands_on']:
   step['title']=('Check the boundary' if s['type']=='check' else 'Apply the contract')+': '+B[cid]['context']['concept_name']
   step['lede']='Use the supplied order-service scenario to reason about this contract.' if s['type']=='check' else 'Complete the supplied workspace within its stated contract.'
  elif s['type']=='recap':
   step['title']='Keep these distinctions'
   step['blocks']=[]
   for c in s['concept_ids']:
    facts=[c+'#'+f['id'] for f in B[c]['coverage']['required_facts']]
    tbs=[c+'#'+t['id'] for t in B[c]['teaching_blocks']]
    step['blocks'].append(prose(TAKE[c],lineage([c],tbs,facts),'takeaway'))
   nxt=tile['next_tile_id']
   if nxt in bytile:
    nc=bytile[nxt]['concept_ids'][0];name=B[nc]['context']['concept_name']
   else:
    # Names are in frozen concept order. The next bundle is not included in this stage input.
    keys=list(glossary['names']);nc=keys[keys.index(tile['concept_ids'][-1])+1];name=glossary['names'][nc]
   step['blocks'].append({'type':'up_next','title':'Next: '+nxt+' — '+name,'text':'Start with '+name+'.'})
  result['steps'].append(step)
 # One targeted remediation per distinct measured-fact set; identical sets share one target.
 seen=set()
 for s in tile['steps']:
  if s['type'] not in ['check','hands_on']:continue
  sig=tuple(s['fact_ids'])
  if sig in seen:continue
  seen.add(sig);cid=s['concept_ids'][0];facts=s['fact_ids'];local={f.split('#')[1] for f in facts}
  tbs=[cid+'#'+t['id'] for t in B[cid]['teaching_blocks'] if set(t['fact_ids']) & local]
  lin=lineage([cid],tbs,facts)
  blocks=[]
  for f in facts:
   fid=f.split('#')[1];tb=[cid+'#'+t['id'] for t in B[cid]['teaching_blocks'] if fid in t['fact_ids']]
   blocks.append(prose(F[cid][int(fid[1:])-1],lineage([cid],tb,[f]),'definition'))
  # The contrast is grounded in the same concept; include its complete teaching lineage.
  contrast=TARGETED.get((cid,tuple(f.split('#')[1] for f in facts)),CONTRAST[cid])
  blocks.append(prose(contrast,lin,'example'))
  result['remediation_steps'].append({'step_id':tile['tile_id']+'.r'+str(len(result['remediation_steps'])+1).zfill(2),'type':'remediation','concept_ids':[cid],'title':'Try the contrast: '+B[cid]['context']['concept_name'],'eyebrow':'Review','blocks':blocks,'lineage':lin})
 out['tiles'].append(result)
(P/'screens.json').write_text(json.dumps(out,indent=2)+'\n')
print('Written',len(out['tiles']),'tiles;',sum(len(t['steps']) for t in out['tiles']),'planned steps;',sum(len(t['remediation_steps']) for t in out['tiles']),'remediation steps')
