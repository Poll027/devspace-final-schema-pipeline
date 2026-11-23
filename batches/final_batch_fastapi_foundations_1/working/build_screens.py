import json, copy, re
from pathlib import Path
B=Path('batches/final_batch_foundations_1')
p=json.loads((B/'tile_plans.json').read_text()); g=json.loads((B/'inputs/path_glossary_bundle.json').read_text()); reg=json.loads((B/'scenario_asset_registry.json').read_text())
bundles={x['context']['concept_id']:x for x in g['bundles']}; assets={x['asset_id']:x for x in reg['assets']}
# Short, independently readable re-voicing of each named teaching block.
texts={
'browser.same_origin_boundary':[
'For a browser page calling an API, separate address matching from permission to access the endpoint.',
'An origin combines scheme, host and port. A difference in any one makes URLs cross-origin.',
'Browser restrictions limit a script’s access to cross-origin responses unless the server permits it through CORS. The API must independently check endpoint access.',
'https://shop.example:443/orders and https://shop.example:443/items share an origin despite different paths. Changing the host to api.example or the port to 8443 makes the call cross-origin.',
'Browser permission to read a response is not authentication. The API still needs its own access checks.'],
'http.method_safety_idempotency':[
'Choose an order operation’s method by its intended effect, not by a convenient label.',
'Safe methods request essentially read-only semantics. Incidental logging does not make them unsafe.',
'Idempotency means identical repetition has the same intended server effect as one request, even if replies differ. GET retrieves a representation; HEAD has the same semantics without response content. Both are safe and idempotent. POST requests resource-specific processing and is not generally idempotent. PUT creates or replaces target state; DELETE removes its association with current functionality. Both are idempotent, not safe.',
'Reading an order and replacing it can both be idempotent, but only reading is safe. Repeated PUT requests the same target state; POST processing is not generally idempotent. Describe the requested change and identical repetition separately. Matching replies are not the test.',
'At /orders/42, GET retrieves a representation and HEAD requests the same semantics without content. Logging is incidental. Repeating a PUT replacement requests the same target state, even if replies differ. Repeated DELETE also need not return identical replies. POST collection processing is not generally idempotent. Ask separately: does this request a change, and does identical repetition preserve the intended effect?',
'Safety does not prohibit all incidental effects. Idempotency does not require identical replies. PUT and DELETE can be idempotent yet unsafe.'],
'http.representation_headers':[
'An order’s outgoing body format, preferred response format and actual response format are separate information.',
'Content-Type labels the media type of its associated representation, not the preferred response format.',
'Accept lists acceptable response media types. For JSON content, send Content-Type: application/json; request a JSON response with Accept: application/json. Inspect the reply’s Content-Type separately.',
'In this JSON exchange, the request Content-Type labels the submitted content. Accept states the response preference. Read the response’s own Content-Type to identify what came back.',
'Content-Type labels content. Accept carries the client’s response preference.'],
'python.backend_type_annotations':[
'Describe the service function’s inputs and result. Distinguish accepting None from allowing the caller to omit an argument.',
'Use name: Type for a parameter and -> Type for the result. Hints alone do not validate runtime values.',
'Type | None admits None; = None separately allows omission. list[str] is a list of strings; set[str] a set of strings; tuple[int, str] a two-element integer/string tuple; dict[str, int] a string-to-integer dictionary.',
'Read shapes first, then defaults. Removing = None changes whether note can be omitted, not whether its type admits None. Removing | None changes admitted values, not defaults. An annotated interface still does not validate runtime values by itself.',
'For order_summary, item_names uses list[str], tags uses set[str], identifier_name uses tuple[int, str], and counts uses dict[str, int]. The return annotation describes the result. note: str | None still requires an argument; adding = None permits omission. These are interface descriptions, not runtime checks.',
'Adding a hint does not add runtime validation. Accepting None and allowing omission are different decisions.'],
'python.classes_and_instances':[
'Two order drafts need independent items, even though they share the class’s behavior.',
'A class statement creates a class with methods defining behavior. Calling that class creates an instance.',
'__init__(self, ...) initializes an instance; self.attribute stores its state. An instance method receives that instance first. Instance variables are specific to each instance; class variables are shared. For independent mutable values, create a fresh value on self inside __init__.',
'Change only draft_a’s items and inspect draft_b. Calling Draft twice does not fix shared mutable class state. Assign a fresh collection to self during initialization. Shared methods use self to identify the instance being changed.',
'Draft defines behavior; draft_a and draft_b are instances. A fresh self.items in each __init__ gives each draft its own collection. One mutable items value on the class can instead be shared. Follow ownership: the method’s first argument identifies the instance, not a new copy of every attribute.',
'Two instances can still share a mutable class variable. Initialize fresh mutable state on self when independence is required.'],
'python.context_managed_cleanup':[
'File-reading work may fail. Mark cleanup on both normal and exceptional exit.',
'Use with manager as resource: and an indented block to enter a managed resource scope.',
'After __enter__ succeeds, __exit__ runs on normal or exceptional block exit. It receives exception details and can suppress an exception by returning true; cleanup alone does not imply suppression. with open(...) as file closes the file after the block, even on an exception.',
'Mark successful entry, work inside the block and departure. Normal departure and an exception both close the file. For a general manager, a true __exit__ return may suppress an exception, but releasing the resource is a separate decision. A cleanup trace is not proof the work succeeded.',
'In with open(...) as file, keep reading inside the indented scope. After successful entry, normal exit closes the file; exceptional exit also closes it. A general manager’s __exit__ receives exception details and may suppress by returning true. Ask separately whether cleanup occurred and whether the exception propagated.',
'Successful entry guarantees an exit call, not disappearing exceptions. Cleanup and suppression are separate.'],
'python.cooperative_async':[
'Trace actual suspension in an asynchronous task; counting await keywords is not enough.',
'Calling async def creates a coroutine. Awaiting it runs it and returns its result on completion.',
'The event loop cooperatively runs one task at a time. While a task waits on a pending future, other tasks may run; completion lets the suspended coroutine resume. An immediately completing await need not suspend. asyncio.sleep suspends the current task, even with delay zero.',
'An immediately completing await leaves no pending wait requiring a handover. Waiting on a pending future gives another runnable task an opportunity to run; completion lets the first resume. This does not establish which task runs next. asyncio.sleep(0) still suspends.',
'In task_a, calling immediate creates a coroutine; awaiting it runs it and obtains its result. If it completes immediately, no suspension is required. Awaiting pending_io can suspend until its future completes, after which task_a resumes. await asyncio.sleep(0) explicitly suspends. Mark those distinctions without promising an exact interleaving.',
'An await is not proof that another task ran. Immediate work may finish without suspension; asyncio.sleep suspends even at zero delay.'],
'python.decorator_wrappers':[
'A decorator can add behavior around a service callable without rewriting that callable.',
'At function definition, the decorator expression is evaluated and called with the function object. Its returned value becomes the function name’s binding.',
'@decorate above def function(...): is roughly function = decorate(function). Build a callable wrapper by defining an inner function that calls the supplied function, then returning the inner function.',
'Trace two times: definition applies decorate to the function object and binds the returned value; a later call uses that binding. If the returned value is an inner wrapper, that later call goes through it to the original function. The decorator receives the function, not the result of calling it with service data.',
'A decorator is not a comment. Its returned value becomes the function name’s binding.'],
'python.isolated_environments':[
'Two projects can need different dependency versions. Identify which interpreter and packages each uses.',
'A virtual environment has a particular Python installation and its own installed packages, allowing applications to use different dependency versions.',
'Create it with python -m venv .venv. Activate using source .venv/bin/activate on Unix or .venv\\Scripts\\activate on Windows. Install with python -m pip install package; inspect version and location with python -m pip show package. Confirm the interpreter path with which python on Unix or where python on Windows.',
'Compare interpreter paths and package locations before assuming a project changed versions. The resolved Python path identifies the interpreter; pip show identifies its package version and location. Each environment has its own installed packages and a particular Python installation.',
'Create and activate .venv, then check which python or where python. With that interpreter identified, install the supplied dependency using python -m pip install and inspect it using python -m pip show. Compare both version and location. Repeat for another project rather than assuming both commands use the same environment.',
'Activation alone is not inspection. Confirm the interpreter path, then inspect the package’s version and location.'],
'asgi.request_lifecycle':[
'The network server and Python application have different roles. ASGI connects them through protocol events.',
'The ASGI server handles the network connection and invokes the application callable through ASGI.',
'The callable is async def app(scope, receive, send). scope describes the connection; receive and send exchange events. Receive http.request through receive(), then send http.response.start with status and headers, followed by http.response.body through send().',
'Keep scope separate from events: it describes the connection, while receive and send exchange events. Send response status and headers in http.response.start before the http.response.body event. The server owns network handling; the application participates through the ASGI callable.',
'Trace the server invoking app with scope, receive and send. The application receives http.request, sends http.response.start containing status and headers, then sends http.response.body. Draw separate arrows for metadata and body, not one handler return. Keep the network connection in the server box.',
'The application does not directly own all network handling. The ASGI server handles the connection and invokes the callable.'],
'auth.local_password_verification':[
'For a local password check, store verification material rather than a password intended to be recovered later.',
'Use password hashing, not plaintext storage or reversible encryption.',
'Salts distinguish hashes; an adjustable work factor increases guessing cost. Create pwdlib’s PasswordHash.recommended(), store hash(password), and check submissions with verify(plain_password, stored_hash).',
'Use the registered synthetic passwords. Create the recommended hasher, store its hash(password) result, then supply the submitted plaintext first and stored hash second to verify. Salt distinguishes hashes; work factor increases guessing cost. Do not replace hashing with reversible storage.',
'Verification checks a submission against a stored hash. It does not recover the original password through decryption.'],
'fastapi_backend.orm_entity_mapping':[
'Mapping connects an Order’s Python attributes to database columns and declares row identity.',
'Create class Base(DeclarativeBase): pass, then inherit mapped entities from Base. Use Mapped[Type] and mapped_column(...) to associate Python attributes with table columns.',
'mapped_column(primary_key=True) declares persistent row identity. __tablename__ names the table; annotations and mapped_column arguments describe columns.',
'Inspect inheritance, table naming and identity separately. Base is shared by mapped entities; Order inherits it. __tablename__ names orders. Mapped and mapped_column describe attributes’ column associations. A familiar name such as id is not enough: primary_key=True supplies the row-identity role.',
'Declare shared Base, then Order(Base) with __tablename__ = "orders". Mapped[int] and mapped_column describe id’s column association; primary_key=True marks persistent row identity. Merely naming an ordinary attribute id is not that declaration. Inspecting mapping is separate from completing a database write.',
'This declaration describes attribute-to-column mapping and row identity, not a completed database write.'],
'http.cors_preflight':[
'For some cross-origin calls, the browser asks permission before sending the intended method and headers.',
'An OPTIONS preflight asks whether an intended method and headers are permitted. Not every cross-origin request is preflighted.',
'Include Origin and Access-Control-Request-Method; include Access-Control-Request-Headers when applicable. Compare the caller’s origin, method and headers with Access-Control-Allow-Origin, Access-Control-Allow-Methods and Access-Control-Allow-Headers. A credentialed response needs an explicit allowed origin, not *, plus Access-Control-Allow-Credentials: true.',
'Compare the supplied OPTIONS exchange: its caller origin, intended PUT and requested content-type must align with the corresponding allow headers. The actual PUT is a separate conditional next step, not completed by OPTIONS. For a credentialed response, check both the explicit allowed origin and Access-Control-Allow-Credentials: true.',
'Only some cross-origin requests are preflighted. A wildcard allowed origin is not the required response for a credentialed exchange.'],
'http.status_selection':[
'Order creation, an absent target and unexpected failure need distinct HTTP outcomes.',
'The classes are informational 1xx, successful 2xx, redirection 3xx, client error 4xx and server error 5xx.',
'Use 200 for success, 201 for resource creation and 204 for success without response content. 400 means a perceived request error; 401 lacks valid authentication credentials; 403 refuses fulfillment; 404 does not find or disclose the target; 409 conflicts with current state. 500 denotes an unexpected server condition; 503 temporary inability, such as overload or maintenance.',
'Choose the outcome class, then its specific meaning. Retrieval differs from creation; missing valid credentials differ from refusal; conflict differs from a target not found or disclosed. Unexpected failure differs from temporary inability. Producing a JSON body does not itself justify a successful status.',
'Use the orders outcome table: retrieval 200, creation 201, no-content success 204. Compare 400 request error, 401 missing valid credentials, 403 refusal, 404 target not found or disclosed and 409 current-state conflict. Unexpected server failure is 500; temporary inability is 503. These meanings do not promise automatic framework behavior.',
'Client and server errors are different classes. A 204 success has no response content.'],
'pydantic.model_validation_conversion':[
'Order input needs a declared shape. Validation can convert compatible values; it is not merely an original-type check.',
'Subclass BaseModel and declare typed fields. Construct with Model(field=value, ...) or validate data with Model.model_validate(data).',
'Compatible inputs can convert to declared types; default validation does not prove their original types matched. Inputs that cannot satisfy the model raise ValidationError with failed-field details. Fields without defaults are required; declared defaults supply omitted values.',
'Check presence and conversion separately. Missing required quantity differs from present quantity that cannot satisfy int. Missing defaulted note uses its default. Compatible conversion can yield the declared type without proving the input originally had that type.',
'For OrderInput, quantity has no default and must be present; omitted note uses its declared default. Construct or model_validate compatible quantity input, compare incompatible input and omission, and inspect ValidationError field details for failures. Read the model as validated output, not a historical guarantee of input types.',
'An integer in the model does not prove the original input was an integer. Ordinary validation can convert compatible inputs.'],
'python.reproducible_dependencies':[
'A teammate needs committed dependency declarations, not a memory of local installation steps.',
'python -m pip freeze reports installed packages and versions. Save that output to requirements.txt as a dependency declaration.',
'Install with python -m pip install -r requirements.txt. Reconstruct from committed declarations, not manually installed packages elsewhere; the build stage obtains the declared dependencies.',
'Inspect versions with python -m pip freeze, save requirements.txt and commit the declaration. Install from it in the environment being reconstructed. Compare declared packages with those obtained for the build. A local installation is not the handoff contract, and freeze alone does not reproduce every external service condition.',
'One successful run in a manually prepared environment is not a dependency declaration. Reconstruct from the committed declaration.'],
'python.service_packages':[
'Qualified names show which package owns a service module.',
'Packages organize modules as package.module. Regular packages contain __init__.py.',
'Use absolute package-qualified imports or relative imports with leading dots interpreted in the current package. Run in package context with python -m package.module; __name__ then becomes __main__.',
'With service/__init__.py and service/orders.py, the qualified module is service.orders. An absolute import names the package; leading-dot imports depend on that package context. python -m service.orders runs it in package context with __name__ equal to __main__. Import identity and execution name serve different roles.',
'Relative imports depend on the current package. File location alone does not explain a leading dot.'],
'database.service_integrity_constraints':[
'Database constraints enforce order integrity even when writes bypass the API.',
'TYPE NOT NULL rejects nulls independently of the application path.',
'UNIQUE rejects duplicate combinations; PostgreSQL treats nulls as distinct by default unless NULLS NOT DISTINCT is specified. PRIMARY KEY gives unique non-null row identity and may span columns. FOREIGN KEY requires non-null references to match referenced rows. CHECK constrains row values but passes on true or null; add NOT NULL to reject absence.',
'Inspect proposed orders independently against the baseline. PRIMARY KEY protects unique non-null identity, and FOREIGN KEY checks non-null customer references. quantity needs NOT NULL as well as CHECK. UNIQUE rejects duplicate external references, but PostgreSQL’s default permits distinct nulls; NULLS NOT DISTINCT changes that null comparison. Match each violation to its constraint.',
'CHECK passing on null does not replace NOT NULL. PostgreSQL UNIQUE treats nulls as distinct by default.']}

def lin(c,tbs=(),facts=(),anchors=()):return {'concept_ids':[c], 'teaching_block_ids':list(tbs),'fact_ids':list(facts),'anchors':list(anchors)}
def prose(text,c,tbs=(),facts=(),role='walkthrough'):return {'type':'prose','text':text,'role':role,'lineage':lin(c,tbs,facts)}
def files(c):return {f['path']:f['content'] for f in assets['ws.'+c]['files']}
def code(src,lang='python',annotations=()):return {'type':'code_walkthrough','language':lang,'code':src,'annotations':list(annotations)}
def diagram(labels,kind='mapping',edges=None):
 labels=[s for s in labels if s.strip()]
 nodes=[{'id':'n'+str(i+1),'label':s} for i,s in enumerate(labels)]
 return {'type':'diagram','diagram_kind':kind,'nodes':nodes,'edges':edges or [],'alt_text':' → '.join(labels),'layout':'auto'}
def flow(labels,edges):return {'type':'process_flow','direction':'LR','nodes':[{'id':'n'+str(i+1),'label':s} for i,s in enumerate(labels)],'edges':edges,'alt_text':'; '.join(labels)}
def e(a,b,label=''):return {'from':'n'+str(a),'to':'n'+str(b),'label':label}
def pair(left,right,ll,rl,take):return {'type':'side_by_side','left':left,'right':right,'left_label':ll,'right_label':rl,'takeaway':take}
def table(asset,columns=None):
 x={'type':'data_table','asset_ref':{'asset_id':asset}}
 if columns:x['asset_ref']['columns']=columns
 return x

def visual(c):
 if c=='browser.same_origin_boundary':return [table('ds.browser_origins')]
 if c=='http.method_safety_idempotency':return [pair(diagram(['GET: retrieve representation','HEAD: same semantics, no content','Safe and idempotent'],edges=[e(1,3),e(2,3)]),diagram(['PUT: create or replace target state','DELETE: remove association','Idempotent, not safe','POST: resource-specific processing; not generally idempotent'],edges=[e(1,3),e(2,3)]),'Read-only requested semantics','State-changing requested semantics','Safety and idempotency are separate properties.')]
 if c=='http.representation_headers':
  fs=files(c);req=fs['request.http'].replace('Content-Type: \n','Content-Type: application/json\n').replace('Accept: \n','Accept: application/json\n')
  return [pair(diagram(req.strip().splitlines(),kind='container'),diagram(fs['response.http'].strip().splitlines(),kind='container'),'Request: body label and response preference','Response: actual content label','Inspect the reply’s own Content-Type.')]
 if c=='python.backend_type_annotations':return [code('def order_summary(\n    item_names: list[str], tags: set[str],\n    identifier_name: tuple[int, str], counts: dict[str, int],\n    note: str | None = None\n) -> dict[str, int]:\n    return counts\n',annotations=[{'start_line':2,'end_line':3,'text':'Collection shapes describe element and key/value types.'},{'start_line':4,'end_line':4,'text':'The union allows None; the default separately allows omission.'},{'start_line':5,'end_line':5,'text':'The return hint describes the result, not runtime validation.'}])]
 if c=='python.classes_and_instances':return [diagram(['Draft: shared method definitions','draft_a: self.items → fresh collection','draft_b: self.items → another fresh collection','Alternative: one mutable class items shared by both'],kind='container',edges=[e(1,2,'calling Draft'),e(1,3,'calling Draft'),e(2,4,'shared-state contrast'),e(3,4,'shared-state contrast')])]
 if c=='python.context_managed_cleanup':return [diagram(['with open("orders.txt") as file:','    file.read() inside managed scope','Normal exit → file closed','Exception exit → file closed','General __exit__: true may suppress; cleanup alone does not'],kind='container',edges=[e(1,2,'successful entry'),e(2,3,'normal departure'),e(2,4,'exceptional departure'),e(4,5,'separate suppression decision')])]
 if c=='python.cooperative_async':return [flow(['Call async function: coroutine created','Await: coroutine runs','Await immediate work: may not suspend','Await pending future: suspend; other tasks may run','Future completes: task resumes','await asyncio.sleep(0): suspends'],[e(1,2),e(2,3),e(3,4,'task_a continues'),e(4,5),e(5,6)])]
 if c=='python.decorator_wrappers':return [diagram(['@decorate above def function','Definition: decorate(function object)','Returned inner_function bound to function name','Later call: inner_function calls original function','Equivalent binding: function = decorate(function)'],edges=[e(1,2),e(2,3),e(3,4),e(5,3)],kind='mapping')]
 if c=='python.isolated_environments':
  dep=json.loads(files(c)['supplied_dependencies.json'])['dependency_names'][0]
  return [pair(code('python -m venv .venv\nsource .venv/bin/activate\nwhich python\npython -m pip install '+dep+'\npython -m pip show '+dep+'\n','bash'),code('python -m venv .venv\n.venv\\Scripts\\activate\nwhere python\npython -m pip install '+dep+'\npython -m pip show '+dep+'\n','bash'),'Unix shell','Windows shell','Verify interpreter path, then package version and location.')]
 if c=='asgi.request_lifecycle':return [flow(['ASGI server: network connection','Invoke async app(scope, receive, send)','scope: connection description','receive(): http.request','send(): http.response.start (status, headers)','send(): http.response.body'],[e(1,2),e(2,3,'connection context'),e(2,4,'protocol event'),e(4,5),e(5,6)])]
 if c=='auth.local_password_verification':
  src=files(c)['main.py'].split('# Create')[0]+'password_hash = PasswordHash.recommended()\nstored_hash = password_hash.hash(password)\nmatching_result = password_hash.verify(password, stored_hash)\nnonmatching_result = password_hash.verify(different_password, stored_hash)\n'
  return [code(src,annotations=[{'start_line':5,'end_line':6,'text':'Create the recommended hasher and store the hash, not plaintext.'},{'start_line':7,'end_line':8,'text':'Submitted password first; stored hash second. Inspect both verification outcomes when run.'}])]
 if c=='fastapi_backend.orm_entity_mapping':return [code('from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column\n\nclass Base(DeclarativeBase):\n    pass\n\nclass Order(Base):\n    __tablename__ = "orders"\n    id: Mapped[int] = mapped_column(primary_key=True)\n',annotations=[{'start_line':3,'end_line':4,'text':'Shared declarative base.'},{'start_line':6,'end_line':7,'text':'Entity inherits Base and names its table.'},{'start_line':8,'end_line':8,'text':'Integer attribute maps to a column; primary_key=True declares row identity.'}])]
 if c=='http.cors_preflight':
  fs=files(c);allowed=fs['response.http'];cred=fs['credentialed_response.http']
  origin=re.search(r'Access-Control-Allow-Origin: (.+)',allowed).group(1);method=re.search(r'Access-Control-Allow-Methods: (.+)',allowed).group(1);header=re.search(r'Access-Control-Allow-Headers: (.+)',allowed).group(1)
  req=fs['request.http'].replace('Origin: \n','Origin: '+origin+'\n').replace('Access-Control-Request-Method: \n','Access-Control-Request-Method: '+method+'\n').replace('Access-Control-Request-Headers: \n','Access-Control-Request-Headers: '+header+'\n')
  return [flow([req.strip(),allowed.strip(),'Actual '+method+': separate next request only if permitted',cred.strip(),'Credentialed response: explicit origin and allow-credentials true; wildcard is not sufficient'],[e(1,2,'compare origin, intended method and headers'),e(2,3,'permission, not completion'),e(4,5,'credentialed requirements')])]
 if c=='http.status_selection':return [table('ds.order_outcomes',['outcome','status_class','selected_status']),table('ds.http_status_classes')]
 if c=='pydantic.model_validation_conversion':
  cases=json.loads(files(c)['input_cases.json']);src='from pydantic import BaseModel, ValidationError\n\nclass OrderInput(BaseModel):\n    quantity: int\n    note: str | None = None\n\nfirst = OrderInput(quantity='+repr(cases[0]['quantity'])+')\ncases = '+repr(cases)+'\nfor data in cases:\n    try:\n        model = OrderInput.model_validate(data)\n        print(model)\n    except ValidationError as error:\n        print(error.errors())\n'
  return [code(src,annotations=[{'start_line':4,'end_line':5,'text':'quantity required; note default supplied on omission.'},{'start_line':7,'end_line':8,'text':'Compare compatible string input, integer input, omitted quantity and incompatible input.'},{'start_line':9,'end_line':14,'text':'Run to inspect conversion, defaults and field failure details; original types need not match model types.'}])]
 if c=='python.reproducible_dependencies':return [pair(code(files(c)['requirements.txt'],'bash'),code('python -m pip install -r requirements.txt\npython -m pip freeze\n','bash'),'Committed declaration','Reconstruct and inspect installed versions','Compare inspection output with the committed declaration when run.')]
 if c=='python.service_packages':return [code('# Regular package marker: service/__init__.py (empty)\n# Service module: service/orders.py\nimport service.orders\n# In package context, leading-dot imports use the current package.\n# Run from the shell: python -m service.orders\n# Execution name: __main__\n',annotations=[{'start_line':1,'end_line':2,'text':'Regular package marker and module location.'},{'start_line':3,'end_line':4,'text':'Qualified identity versus package-relative import context.'},{'start_line':5,'end_line':6,'text':'Run in package context; distinguish qualified identity from execution name.'}])]
 if c=='database.service_integrity_constraints':return [table('ds.orders'),table('ds.customers'),table('ds.proposed_orders')]
 raise ValueError(c)

recaps={
'browser.same_origin_boundary':'Compare scheme, host and port; browser response access and API access checks stay separate.',
'http.method_safety_idempotency':'Safety concerns requested changes; idempotency concerns repeated intended effects, not identical replies.',
'http.representation_headers':'Content-Type labels content; Accept states response preferences.',
'python.backend_type_annotations':'Hints describe types, not runtime checks. None permission differs from argument omission.',
'python.classes_and_instances':'Classes share behavior; fresh self state gives drafts independent mutable collections.',
'python.context_managed_cleanup':'Successful entry leads to managed exit; cleanup and exception suppression remain separate.',
'python.cooperative_async':'Trace actual suspension. Immediate await may not suspend; asyncio.sleep(0) does.',
'python.decorator_wrappers':'Decoration binds its returned value at definition; later calls use that binding.',
'python.isolated_environments':'Each environment has its own packages. Verify interpreter path and package version and location.',
'asgi.request_lifecycle':'The server owns network handling; app exchanges request, response-start and response-body events.',
'auth.local_password_verification':'Store a password hash. Salt distinguishes hashes; work factor increases guessing cost. Verify plaintext first, hash second.',
'fastapi_backend.orm_entity_mapping':'Base, table name and mapped attributes declare association; primary_key=True declares row identity.',
'http.cors_preflight':'OPTIONS checks permission, not completion. Credentialed responses require explicit origin and allow-credentials true.',
'http.status_selection':'Choose the outcome class, then the particular success or failure meaning.',
'pydantic.model_validation_conversion':'Models can convert compatible input. Required fields, defaults and field errors answer different questions.',
'python.reproducible_dependencies':'Commit dependency declarations and reconstruct from them rather than accidental local installations.',
'python.service_packages':'Qualified imports and leading-dot imports use package context; -m runs with __name__ set to __main__.',
'database.service_integrity_constraints':'Database constraints enforce integrity beyond the API. CHECK does not reject null by itself; default UNIQUE treats nulls as distinct.'}
contrasts={c:recaps[c] for c in bundles}
contrasts.update({
'browser.same_origin_boundary':'Contrast changing only /items with changing host: paths do not change origins, but host changes do. Neither replaces API access checks.',
'http.method_safety_idempotency':'Contrast GET retrieval with PUT replacement: both are idempotent, but replacement requests a change and is not safe.',
'python.backend_type_annotations':'Contrast note: str | None with note: str | None = None: only the second permits omission.',
'python.classes_and_instances':'Contrast a fresh self.items in each Draft initializer with one mutable items on Draft: only the former supplies independent collections.',
'python.context_managed_cleanup':'Contrast a file closing after failed reading with the failure disappearing: closure does not itself suppress the exception.',
'python.cooperative_async':'Contrast await immediate() with await asyncio.sleep(0): the first can finish without suspension; sleep suspends even at zero.',
'auth.local_password_verification':'Contrast storing hash(password) with storing password: verification needs a stored hash, not recoverable plaintext.',
'http.status_selection':'Contrast retrieval success with creation success: the selected meanings are 200 and 201, not one generic success label.',
'pydantic.model_validation_conversion':'Contrast omitted required quantity with omitted defaulted note: absence fails the first field but supplies the second field’s default.',
'database.service_integrity_constraints':'Contrast CHECK (quantity > 0) alone with adding NOT NULL: null passes CHECK alone but is rejected by NOT NULL.'})
# Reference only source fact statements in remediation; concrete contrast uses the same scenario.
out={k:p[k] for k in ['schema_version','path_id','batch_id']};out['kind']='screens_part';out['tiles']=[]
for t in p['tiles']:
 tile={'tile_id':t['tile_id'],'title':' · '.join(bundles[c]['context']['concept_name'] for c in t['concept_ids']),'steps':[],'remediation_steps':[]}
 for s in t['steps']:
  cs=s['concept_ids'];c=cs[0];b=bundles[c]
  lineage={k:copy.deepcopy(s[k]) for k in ['concept_ids','teaching_block_ids','fact_ids','segment_ids','anchors']}
  title={'check':'Check the distinction','hands_on':'Apply the rule','video':'Follow the worked trace','recap':'Keep these takeaways'}.get(s['type'])
  if not title:
   first=s['teaching_block_ids'][0].split('#')[1];tb=next(x for x in b['teaching_blocks'] if x['id']==first)
   title={'intro':'Establish the rule','mechanism':'Trace the boundary','example':'Work through the order example','misconception':'Keep the distinction'}.get(tb['purpose'],tb['title'])
  step={'step_id':s['step_id'],'type':s['type'],'concept_ids':copy.deepcopy(cs),'eyebrow':b['context']['concept_name'] if s['type']!='recap' else 'Review','title':title,'lineage':lineage}
  if s['type'] in ['check','hands_on']:tile['steps'].append(step);continue
  step['blocks']=[]
  if s['type']=='video':step['blocks']=[{'type':'media_group','segment_ids':copy.deepcopy(s['segment_ids'])}]
  elif s['type']=='recap':
   for cc in cs:
    bb=bundles[cc];step['blocks'].append(prose(recaps[cc],cc,[cc+'#'+tb['id'] for tb in bb['teaching_blocks']],[cc+'#'+f['id'] for f in bb['coverage']['required_facts']],role='takeaway'))
   nt=next((tt for tt in p['tiles'] if tt['tile_id']==t['next_tile_id']),None)
   next_name=bundles[nt['concept_ids'][0]]['context']['concept_name'] if nt else g['names'][b['context']['blocked_future_concepts'][0]]
   step['blocks'].append({'type':'up_next','title':next_name,'text':'Continue to '+t['next_tile_id']+'.'})
  else:
   for tbid in s['teaching_block_ids']:
    tb=next(tb for tb in b['teaching_blocks'] if c+'#'+tb['id']==tbid)
    i=b['teaching_blocks'].index(tb);step['blocks'].append(prose(texts[c][i],c,[tbid],[c+'#'+fid for fid in tb['fact_ids']],tb['purpose'] if tb['purpose'] in ['intro','definition','mechanism','example','misconception'] else 'walkthrough'))
   if s['planned_visual_block_type']:
    for v in visual(c):
     v['lineage']=lin(c,s['teaching_block_ids'],s['fact_ids'],[c+'#visual'])
     for side in ['left','right']:
      if side in v:v[side]['lineage']=copy.deepcopy(v['lineage'])
     step['blocks'].append(v)
  for i,bl in enumerate(step['blocks'],1):bl['block_id']=s['step_id']+'.b'+str(i).zfill(2)
  tile['steps'].append(step)
 # Every distinct measured-fact set gets its own remedial target, in plan interaction order.
 seen=set()
 for s in t['steps']:
  if s['type'] not in ['check','hands_on']:continue
  c=s['concept_ids'][0];key=(c,tuple(sorted(s['fact_ids'])))
  if key in seen:continue
  seen.add(key);b=bundles[c];facts=s['fact_ids'];tbs=[c+'#'+tb['id'] for tb in b['teaching_blocks'] if any(c+'#'+f in facts for f in tb['fact_ids'])]
  rid=t['tile_id']+'.r'+str(len(tile['remediation_steps'])+1).zfill(2)
  rem={'step_id':rid,'type':'remediation','concept_ids':[c],'eyebrow':'Try the contrast','title':'Revisit '+s['step_id'],'lineage':lin(c,tbs,facts),'blocks':[]}
  for f in b['coverage']['required_facts']:
   fid=c+'#'+f['id']
   if fid not in facts:continue
   ftbs=[c+'#'+tb['id'] for tb in b['teaching_blocks'] if f['id'] in tb['fact_ids']]
   rem['blocks'].append(prose(f['statement'],c,ftbs,[fid],role='definition'))
  rem['blocks'].append(prose(contrasts[c],c,tbs,facts,role='example'))
  # Data references retain exactly the same registry scenario, never copied rows.
  if c=='browser.same_origin_boundary':rem['blocks'].append(table('ds.browser_origins'))
  if c=='http.status_selection':rem['blocks'].append(table('ds.order_outcomes',['outcome','status_class','selected_status']))
  if c=='database.service_integrity_constraints':rem['blocks'].append(table('ds.proposed_orders'))
  for i,bl in enumerate(rem['blocks'],1):
   bl['block_id']=rid+'.b'+str(i).zfill(2)
   if bl['type']=='data_table':bl['lineage']=lin(c,tbs,facts,[c+'#visual'])
  tile['remediation_steps'].append(rem)
 out['tiles'].append(tile)
(B/'screens.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Tiles:',len(out['tiles']),'Steps:',sum(len(t['steps']) for t in out['tiles']),'Remediation:',sum(len(t['remediation_steps']) for t in out['tiles']))
# Own mistakes-to-avoid checks, stricter than the schema-only gate.
for tt,t in zip(out['tiles'],p['tiles']):
 assert [s['step_id'] for s in tt['steps']]==[s['step_id'] for s in t['steps']]
 for s,ps in zip(tt['steps'],t['steps']):
  assert s['type']==ps['type'] and s['concept_ids']==ps['concept_ids']
  for k in ['teaching_block_ids','fact_ids']:assert s['lineage'][k]==ps[k]
  if s['type'] in ['check','hands_on']:assert 'blocks' not in s
  if s['type']=='explainer':
   words=sum(len(bl['text'].split()) for bl in s['blocks'] if bl['type']=='prose')
   assert words<=ps['word_budget'],(s['step_id'],words,ps['word_budget'])
   if ps['planned_visual_block_type']:assert any(s['concept_ids'][0]+'#visual' in bl.get('lineage',{}).get('anchors',[]) for bl in s['blocks'])
 for s in tt['steps']+tt['remediation_steps']:
  for bl in s.get('blocks',[]):
   assert 'output' not in bl and 'result' not in bl and 'computed_values' not in bl
   if bl['type']=='prose':
    assert 'lineage' in bl and len(bl['text'].split())<=90
    assert 'video' not in bl['text'].lower()
    assert all('#f' in f for f in bl['lineage']['fact_ids'])
   if 'asset_ref' in bl:
    aa=assets[bl['asset_ref']['asset_id']]
    assert set(bl['asset_ref'].get('columns',[]))<={x['name'] for x in aa['columns']}
print('Own checklist passed: plan order/lineage, framing-only interactions, qualified facts, prose length/budgets, standalone text, visual anchors, registered columns, no typed outputs.')
