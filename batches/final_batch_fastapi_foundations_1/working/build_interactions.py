import json, sys, re
from pathlib import Path
B=Path('batches/final_batch_foundations_1')
sys.path.insert(0,str(Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
from checkers import sandbox
plan=json.loads((B/'tile_plans.json').read_text())
screens=json.loads((B/'screens.json').read_text())
reg=json.loads((B/'scenario_asset_registry.json').read_text())
gloss=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
bundles={b['context']['concept_id']:b for b in gloss['bundles']}
assets={a['asset_id']:a for a in reg['assets']}
runtimes=json.loads(Path('00_FINAL_PIPELINE_CORE/registry/runtimes.json').read_text())['runtimes']
# Each tuple is a question, its defensible answer, and misconception-based alternatives with reasons.
Q={
 'tile_000.s02':("A script at https://shop.example calls https://api.example. CORS permits reading the response. What follows for endpoint access checks?", "The API must still check access independently of CORS.",[("CORS permission replaces endpoint access checks.","CORS concerns browser response access, not the API's independent access checks."),("The browser's origin restriction itself authenticates the caller.","A browser restriction is not an endpoint access check.")]),
 'tile_000.s07':("A GET retrieves an order and writes an incidental log entry; a PUT replaces that order's state. Which safety/idempotency judgement is correct?","GET remains safe and idempotent; PUT is idempotent but not safe.",[("Both are unsafe because both can write something.","Safety concerns requested semantics; incidental retrieval logging does not make GET unsafe."),("PUT is safe because repeating it has the same intended effect.","Idempotency does not imply read-only requested semantics.")]),
 'tile_000.s10':("A JSON request sends Content-Type: application/json and Accept: application/json. Which header identifies the media type actually returned?","The response's own Content-Type.",[("The request's Accept.","Accept communicates acceptable response formats, not the returned representation's metadata."),("The request's Content-Type.","That Content-Type describes the outgoing JSON content, not the response content.")]),
 'tile_003.s04':("Compare def a(note: str | None): and def b(note: str | None = None):. Which accepts an omitted note argument?","Only b; both annotations permit None, but only b supplies a default.",[("Both, because permitting None makes an argument omittable.","Nullability and a default have separate roles."),("Neither, because an annotation prevents omission even with a default.","The default independently permits omission.")]),
 'tile_003.s09':("Inspect this initialization:\n```python\nclass Draft:\n    def __init__(self):\n        self.items = []\ndraft_a = Draft()\n```\nWhich describes the class/instance relationship?","Calling Draft creates an instance; __init__ stores items on that instance via self.",[("The class statement itself creates draft_a.","The class statement creates the class; calling that class creates the instance."),("self is the shared class object rather than the method's instance.","An instance method receives the instance as its first argument.")]),
 'tile_005.s05':("A supplied context manager's __enter__ returns successfully, then the with block raises an exception. What is guaranteed about __exit__?","The with statement calls __exit__ on this exceptional exit.",[("__exit__ is called only when the block completes normally.","After successful entry, both normal and exceptional block exits call __exit__."),("Successful __enter__ means __exit__ is no longer needed.","Successful entry is the condition under which with performs the exit call.")]),
 'tile_005.s06':("A manager cleans up on exceptional exit and returns False from __exit__. Does cleanup alone mean the exception is suppressed?","No; cleanup and suppression are distinct, and a true exit return value can suppress it.",[("Yes; any cleanup suppresses the exception.","Cleanup does not itself imply suppression."),("Yes; a false return value is the suppression signal.","A true value, not a false one, can suppress the exception.")]),
 'tile_005.s11':("Task A awaits an operation that completes immediately, then awaits a pending future. Where is an opportunity for another runnable task established?","While A is suspended waiting on the pending future; the immediate await need not hand over.",[("Every await necessarily switches to another task.","An immediately completing awaited operation can finish without suspension."),("Only after A has completely finished; a pending await cannot release execution.","Cooperative scheduling permits other tasks to run while a task waits on a pending future.")]),
 'tile_007.s03':("Inspect the wrapper:\n```python\ndef decorate(function):\n    def inner_function():\n        return function()\n    return inner_function\n```\nWhat happens when the returned wrapper is later called?","inner_function calls the supplied function and returns its result.",[("The original function already ran when decorate returned inner_function.","Returning a callable without parentheses does not call it."),("The wrapper returns the original callable without calling it.","Its body uses function(), so it calls the supplied function.")]),
 'tile_008.s04':("An activated .venv is expected. `which python` points outside .venv, and `python -m pip show jsonschema` reports a Location outside .venv. Which judgement is supported?","These outputs do not verify installation in the intended environment.",[("A package name alone proves the intended environment is in use.","Check the interpreter path and the package location, not just its name."),("Activation text is enough; interpreter and package paths do not matter.","The interpreter path confirms the environment, and pip show reports version and location.")]),
 'tile_009.s04':("For one complete HTTP request, which application-side event order is correct?","receive yields http.request, then send gets http.response.start, then http.response.body.",[("send gets http.response.body before http.response.start.","Response metadata precedes response body content."),("The application must implement network handling before it can receive an event.","The supplied server invokes the application and handles the network; the application exchanges events.")]),
 'tile_010.s02':("Which password-storage design separates storage, salt, and work-factor roles correctly?","Store a password hash; salts distinguish hashes, and a work factor raises guessing cost.",[("Store reversible encryption; salts make it equivalent to password hashing.","Password storage should use password hashing rather than reversible encryption."),("Store a password hash; the salt replaces the work factor by providing the same cost control.","Salts distinguish hashes; adjustable work factors control guessing cost. Their roles differ.")]),
 'tile_010.s03':("Given password_hash = PasswordHash.recommended() and stored_hash = password_hash.hash(password), how should a submitted password be checked?","password_hash.verify(plain_password, stored_hash)",[("password_hash.verify(stored_hash, plain_password)","The taught argument order is submitted plaintext first, stored hash second."),("Store plain_password and compare it directly instead.","Store the hash and use the library's verification method, not plaintext storage.")]),
 'tile_011.s04':("Inspect:\n```python\nclass Order(Base):\n    __tablename__ = 'orders'\n    id: Mapped[int] = mapped_column(primary_key=True)\n```\nWhat marks id as the persistent row key?","primary_key=True in mapped_column.",[("The name id alone, without a primary-key declaration.","The explicit primary-key marker declares the key; the name alone is not the marker."),("Mapped[int] alone, regardless of mapped_column arguments.","The integer annotation and explicit primary-key marker serve distinct purposes.")]),
 'tile_012.s03':("A credentialed response has Access-Control-Allow-Origin: * and Access-Control-Allow-Credentials: true. Is that sufficient for credentialed cross-origin response access?","No; an explicit allowed origin is required alongside Allow-Credentials: true.",[("Yes; true makes the wildcard sufficient.","Credentialed responses require an explicit allowed origin rather than *."),("Yes; the wildcard replaces the need to inspect the credentials header.","The explicit origin and credentials allowance are both required.")]),
 'tile_012.s08':("One orders request fails due to an unexpected server condition; another cannot be handled temporarily during maintenance. Which pair matches those outcomes, in that order?","500, then 503.",[("503, then 500.","500 is for the unexpected condition; 503 is for temporary inability such as maintenance."),("500 for both; temporary maintenance cannot be distinguished.","503 specifically denotes temporary inability to handle the request.")]),
 'tile_014.s05':("OrderInput declares quantity: int with no default. Ordinary validation accepts quantity='3', but quantity='many' fails. Which interpretation is correct?","Accepted input can be converted to integer 3; incompatible input can produce a field validation failure.",[("Accepting '3' means quantity remains a string in the validated instance.","Validation can convert accepted input to the declared output type."),("Any string must be accepted because the numeric-looking string was accepted.","Acceptance of convertible input does not imply acceptance of incompatible input.")]),
 'tile_014.s06':("OrderInput declares quantity: int and note: str = ''. If both fields are omitted, which description is correct?","quantity is missing required input; note has its declared empty-string default.",[("Both fields have defaults because both have annotations.","An annotation alone does not supply a default."),("Both are required because their types exclude None.","The declared default makes note omittable; this differs from allowing None.")]),
 'tile_015.s04':("A clean service build has a committed requirements.txt. What should it rely on to reconstruct dependencies?","The committed declaration, installed in the clean environment.",[("Packages manually installed in a developer's other environment.","Reconstruction uses committed declarations, not another environment's manual state."),("Overwrite requirements.txt using the empty environment's freeze output before installation.","That replaces the committed declaration instead of reconstructing from it.")]),
 'tile_015.s08':("Run the package module with `python -m service.orders` from the parent directory. What is its __name__ during this execution?","__main__",[("service.orders", "That is the qualified import name; module execution uses __main__."),("service", "The package name is not the executed module's execution name.")]),
 'tile_017.s03':("Under the taught PostgreSQL default UNIQUE(external_reference), an existing row has a null external_reference. A new otherwise-valid row also has null. How does the default compare with UNIQUE NULLS NOT DISTINCT?","Default UNIQUE permits the repeated null; NULLS NOT DISTINCT can reject it.",[("Both reject repeated nulls identically.","Default UNIQUE retains distinct-null behavior; NULLS NOT DISTINCT changes that comparison."),("Default UNIQUE rejects nulls, while NULLS NOT DISTINCT permits them.","This reverses the taught null policies.")]),
 'tile_017.s04':("quantity has CHECK(quantity > 0). Which added constraint rejects absent quantities, while CHECK rejects nonpositive non-null quantities?","NOT NULL",[("UNIQUE(quantity)","Uniqueness does not impose the required non-null condition."),("No added constraint; CHECK alone rejects null as a failed comparison.","CHECK alone does not provide the NOT NULL requirement.")])
}
C={}
def inline(cid,prompt,buckets,items):
 C[cid]={'public':{'prompt':prompt,'buckets':[{'bucket_id':k,'label':v} for k,v in buckets.items()],'items':[{'item_id':'item'+str(i+1),'text':text} for i,(text,key,why) in enumerate(items)]},'grading':{'assignments':{'item'+str(i+1):key for i,(text,key,why) in enumerate(items)},'item_feedback':{'item'+str(i+1):{'message':why} for i,(text,key,why) in enumerate(items)}}}
# Derived URL predicates preserve exactly the registry's rows and comparison results.
a=assets['ds.browser_origins']; rows=[dict(zip([c['name'] for c in a['columns']],r)) for r in a['rows']]
keys={r['differing_components']:'bucket'+str(i+1) for i,r in enumerate(rows)}
C['browser.same_origin_boundary']={'public':{'prompt':'Classify each browser-page URL relative to the fixed API '+rows[0]['api_url']+'. Identify the differing origin component; a path difference alone is not an origin difference.','buckets':[{'bucket_id':keys[r['differing_components']],'label':r['origin_classification']+' — '+('no differing origin component' if r['differing_components']=='none' else 'different '+r['differing_components'])} for r in rows], 'items':[{'item_id':'item'+str(i+1),'text':r['browser_url'],'source':{'asset_id':a['asset_id'],'row':{'where':{'browser_url':r['browser_url']},'occurrence':0},'column':'differing_components'}} for i,r in enumerate(rows)]},'grading':{'assignments':{'item'+str(i+1):keys[r['differing_components']] for i,r in enumerate(rows)},'role_map':{key:next(c['semantic_role'] for c in a['columns'] if c['name']=='differing_components') for key in keys.values()},'item_feedback':{'item'+str(i+1):{'message':'Origin comparison: '+r['origin_classification']+'; differing component: '+r['differing_components']+'.'} for i,r in enumerate(rows)}}}
inline('http.method_safety_idempotency','For each orders operation, choose its method and safety/idempotency judgement. Repetition means identical requests and intended server effect, not identical response messages.',{'get':'GET — safe, idempotent','head':'HEAD — safe, idempotent','post':'POST — not generally idempotent','put':'PUT — not safe, idempotent','delete':'DELETE — not safe, idempotent'},[
 ('Retrieve the selected order representation. The server also writes an incidental retrieval log.','get','GET retrieves; incidental logging remains compatible with safety.'),
 ('Request the same retrieval semantics but no response content.','head','HEAD has retrieval semantics without response content; it is safe and idempotent.'),
 ('Process submitted content to create a new order, without any additional idempotency guarantee.','post','POST requests resource-specific processing and is not generally idempotent.'),
 ('Create or replace the state of the known target /orders/42. Repeated identical requests need not have identical responses.','put','PUT creates or replaces target state; idempotency concerns intended effects rather than response equality.'),
 ('Remove the association of /orders/42 with its current functionality. A later identical request may have a different response.','delete','DELETE is idempotent but not safe; differing responses do not disprove equal intended effects.')])
inline('python.isolated_environments','Inspect these hypothetical Unix transcripts independently. Does each establish creation, activation, the intended interpreter and a dependency installed inside .venv?',{'verified':'Verified in .venv','wrong':'Not verified in the intended environment'},[
 ('python -m venv .venv\nsource .venv/bin/activate\nwhich python\n/workshop/.venv/bin/python\npython -m pip install jsonschema\nSuccessfully installed jsonschema\npython -m pip show jsonschema\nVersion: __SUPPLIED_VERSION__\nLocation: /workshop/.venv/lib/python3.12/site-packages','verified','The interpreter and dependency location both belong to .venv.'),
 ('python -m venv .venv\nsource .venv/bin/activate\nwhich python\n/usr/bin/python\npython -m pip show jsonschema\nVersion: __SUPPLIED_VERSION__\nLocation: /usr/lib/python3.12/site-packages','wrong','Creation and an activation command do not override evidence that the selected interpreter and package are outside .venv.'),
 ('python -m venv .venv\nwhich python\n/usr/bin/python\npython -m pip install jsonschema\nSuccessfully installed jsonschema','wrong','This does not verify activation or the intended environment interpreter; a successful install alone is insufficient.')])
inline('auth.local_password_verification','Inspect each hypothetical password-storage and verification excerpt. Judge the design, not whether a library is available in this player. The stated True/False observations are supplied evidence, not executed output.',{'correct':'Correct storage and verification pattern','unsafe':'Unsafe storage','wrong':'Incorrect verification pattern'},[
 ('from pwdlib import PasswordHash\npassword_hash = PasswordHash.recommended()\nstored_hash = password_hash.hash(password)\nmatching_result = password_hash.verify(password, stored_hash)\nnonmatching_result = password_hash.verify(different_password, stored_hash)\n# Supplied observation: matching_result is True; nonmatching_result is False.','correct','Store the library hash and verify submitted plaintext against it; the two observations satisfy matching and nonmatching checks.'),
 ('stored_hash = password\n# Persist stored_hash as the password record.','unsafe','The persisted value is plaintext, not a password hash.'),
 ('password_hash = PasswordHash.recommended()\nstored_hash = password_hash.hash(password)\nmatching_result = password_hash.verify(stored_hash, password)','wrong','Verification takes submitted plaintext first and stored hash second.')])
supplied_dependencies=json.loads(next(f['content'] for f in assets['ws.python.isolated_environments']['files'] if f['path']=='supplied_dependencies.json'))
for item in C['python.isolated_environments']['public']['items']:
 item['text']=item['text'].replace('__SUPPLIED_VERSION__',supplied_dependencies['host_comparison']['version'])
# Copy the HTTP evidence from the prepared registry workspace; add only a judgement question.
ws=assets['ws.http.cors_preflight']; files={f['path']:f['content'] for f in ws['files']}
preflight=files['request.http'].replace('Origin: \n','Origin: https://shop.example\n').replace('Access-Control-Request-Method: \n','Access-Control-Request-Method: PUT\n').replace('Access-Control-Request-Headers: \n','Access-Control-Request-Headers: content-type\n')
inline('http.cors_preflight','Inspect each independent exchange for https://shop.example calling the API. Distinguish preflight permission from completion of PUT, and require the credentialed response rules where credentials are specified.',{'permit':'Preflight permits intended PUT; PUT not yet completed','credential':'Credentialed response satisfies origin/credentials rules','reject':'Credentialed response fails origin/credentials rules','deny':'Preflight does not permit intended method'},[
 (preflight+'\n'+files['response.http'],'permit','The allowed origin, method and header match the request; an OPTIONS permission response is not completion of PUT.'),
 ('Credentialed response to Origin: https://shop.example\n'+files['credentialed_response.http'],'credential','The explicit origin matches and Allow-Credentials is true.'),
 ('Credentialed response to Origin: https://shop.example\n'+files['wildcard_credentialed_response.http'],'reject','A wildcard allowed origin is insufficient for credentialed response access.'),
 (preflight+'\n'+files['response.http'].replace('Allow-Methods: PUT','Allow-Methods: GET'),'deny','The intended PUT is not in the supplied allowed-method value.')])
requirements=next(f['content'] for f in assets['ws.python.reproducible_dependencies']['files'] if f['path']=='requirements.txt')
inline('python.reproducible_dependencies','Each excerpt describes a separate clean isolated environment. The committed requirements.txt is:\n'+requirements+'\nClassify whether the evidence reconstructs from that declaration or instead relies on/replaces other state.',{'reconstructed':'Reconstructed and verified from committed requirements','capture':'Captures installed versions only; does not reconstruct','wrong':'Does not reconstruct the committed requirements'},[
 ('# Clean environment; committed requirements unchanged\npython -m pip install -r requirements.txt\n# Supplied observation: installation completes successfully\npython -m pip freeze\n'+requirements,'reconstructed','The installation uses the committed declaration and the inspected versions satisfy every entry.'),
 ('# Original working environment\npython -m pip freeze > requirements.txt','capture','This captures existing installed versions; it is not a clean-environment installation from a committed file.'),
 ('# Clean environment\npython -m pip freeze > requirements.txt\npython -m pip install -r requirements.txt\n# Supplied observation: the empty freeze output replaced the committed file.','wrong','Replacing the committed declaration with an empty one loses the dependencies that should be reconstructed.'),
 ('# New environment; no installation from declarations\n# Use the packages that happen to be installed in the original environment.','wrong','Another environment\'s manual package state is not reconstruction from committed declarations.')])
EX={}
def exercise(cid,starter,solution,prompt,probes,kind='python',packages=None,mounts=None):
 EX[cid]={'starter':starter,'solution':solution,'prompt':prompt,'probes':probes,'kind':kind,'packages':packages or [],'mounts':mounts or []}
# Probe specifications intentionally omit expected: all expected values are computed by the pinned engine below.
def val(expr): return ('value_equals',{'expr':expr})
def call(name,*args): return ('function_call',{'function':name,'args':list(args)})
# Raw-HTTP authoring is carried as comment lines so only taught raw headers are edited.
raw_scaffold='''
def inspect_exchange(response_type):
    source = open('main.py').read().splitlines()
    request = {}
    selected = ''
    for line in source:
        if line.startswith('# REQUEST '):
            name, value = line[len('# REQUEST '):].split(':', 1)
            request[name.strip()] = value.strip()
        if line.startswith('# RESPONSE_FIELD '):
            selected = line[len('# RESPONSE_FIELD '):].strip()
    response_headers = {'Content-Type': response_type}
    return {'request': request, 'returned_media_type': response_headers.get(selected)}
'''
raw_start='# REQUEST Content-Type: \n# REQUEST Accept: \n# RESPONSE_FIELD \n'+raw_scaffold
raw_sol='# REQUEST Content-Type: application/json\n# REQUEST Accept: application/json\n# RESPONSE_FIELD Content-Type\n'+raw_scaffold
exercise('http.representation_headers',raw_start,raw_sol,'Complete the two # REQUEST header lines for a prepared JSON order request. In # RESPONSE_FIELD write the response header name to inspect separately for the returned media type. The checker supplies a response Content-Type (application/json in one case and text/plain in another); inspect that response, not a request preference. Keep the Python checker unchanged. This is raw-header editing in a supplied inspection harness, not an HTTP server.',[call('inspect_exchange','application/json'),call('inspect_exchange','text/plain')])
annotation_harness='''
def inspect_summary(counts):
    import inspect
    signature = inspect.signature(order_summary)
    return {'parameters': {k:str(v.annotation) for k,v in signature.parameters.items()}, 'return':str(signature.return_annotation), 'note_default_is_none':signature.parameters['note'].default is None, 'result':order_summary([],set(),(42,'order'),counts)}
'''
type_start='def order_summary(item_names, tags, identifier_name, counts, note):\n    return counts\n'+annotation_harness
type_sol='def order_summary(item_names: list[str], tags: set[str], identifier_name: tuple[int, str], counts: dict[str, int], note: str | None = None) -> dict[str, int]:\n    return counts\n'+annotation_harness
exercise('python.backend_type_annotations',type_start,type_sol,bundles['python.backend_type_annotations']['practice_anchor']['objective']+' Edit only the signature, leaving return counts and the supplied inspection harness unchanged. The checker inspects every annotation, the separate default and the unchanged function result.',[call('inspect_summary',{'order':3}),call('inspect_summary',{'order':7,'other':1})])
class_start='item = "order item"\nclass Draft:\n    pass\n# Create draft_a and draft_b, then append item only to draft_a.items.\n'
class_sol='item = "order item"\nclass Draft:\n    def __init__(self):\n        self.items = []\ndraft_a = Draft()\ndraft_b = Draft()\ndraft_a.items.append(item)\n'
exercise('python.classes_and_instances',class_start,class_sol,'Define Draft with __init__(self) assigning a fresh empty list to self.items. Create draft_a and draft_b by calling Draft, then append the supplied item only to draft_a.items. Do not change item. The checker inspects both lists, a fresh instance and whether items was stored as a shared class variable.',[val("[draft_a.items, draft_b.items, Draft().items, 'items' in Draft.__dict__]")])
context_scaffold='''
import io
import builtins
_resource = None
_failing = False
class SuppliedFile(io.StringIO):
    def read(self):
        if _failing:
            raise RuntimeError('supplied failure')
        return super().read()
def open(path):
    global _resource
    _resource = SuppliedFile('synthetic order')
    return _resource
'''
context_tail='''
def check_scope(fail):
    global _failing
    _failing = fail
    raised = False
    try:
        managed_read()
    except RuntimeError:
        raised = True
    return {'closed':_resource.closed, 'exception_propagated':raised}
'''
context_start=context_scaffold+'\ndef managed_read():\n    file = open("orders.txt")\n    file.read()\n'+context_tail
context_sol=context_scaffold+'\ndef managed_read():\n    with open("orders.txt") as file:\n        file.read()\n'+context_tail
exercise('python.context_managed_cleanup',context_start,context_sol,'Inside the supplied managed_read function, replace unmanaged acquisition with with open("orders.txt") as file: and place file.read() in its indented block. Leave the checker unchanged. It supplies a readable file-like resource in place of open and checks closure on normal reading and on an injected reading failure; the failure must still propagate.',[call('check_scope',False),call('check_scope',True)])
async_body='''
import asyncio
async def immediate():
    return 1
async def task_a(future):
    value = await immediate()
    value = await future
    await asyncio.sleep(0)
    return value
'''
async_harness='''
def inspect_annotation(point):
    for line in open('main.py').read().splitlines():
        if line.startswith('# MARK '+point+':'):
            return line.split(':',1)[1].strip()
    return 'missing'
'''
marks={'call':'coroutine_creation','immediate':'no_required_handover','pending':'suspends_other_may_run','continuation':'after_future_ready','sleep':'suspends_other_may_run'}
async_start=async_body+'\n# These annotations refer to coroutine = task_a(future), its awaits and continuation.\n'+''.join('# MARK '+k+': TODO\n' for k in marks)+async_harness
async_sol=async_body+'\n# These annotations refer to coroutine = task_a(future), its awaits and continuation.\n'+''.join('# MARK '+k+': '+v+'\n' for k,v in marks.items())+async_harness
exercise('python.cooperative_async',async_start,async_sol,'Annotate the supplied coroutine trace by replacing TODO only in # MARK comments. call refers to coroutine = task_a(future) before it is run; immediate refers to await immediate(); pending refers to await future when the future is pending; continuation refers to A continuing after that await; sleep refers to await asyncio.sleep(0). Use one label per comment: coroutine_creation or execution for call; no_required_handover or suspends_other_may_run for immediate/pending/sleep; after_future_ready or before_future_ready for continuation. Do not assert which other task runs first. Keep the supplied code and inspection harness unchanged.',[call('inspect_annotation',k) for k in marks])
dec_harness='''
def inspect_decoration(text):
    calls = []
    def original():
        calls.append('original')
        return text
    function = original
    function = decorate(function)
    before = list(calls)
    explicit = function()
    @decorate
    def function():
        calls.append('original')
        return text
    after_definition = list(calls)
    implicit = function()
    return {'before_later_call':before,'after_decorated_definition':after_definition,'explicit_result':explicit,'decorated_result':implicit,'call_path':calls,'replacement_name':function.__name__,'judgements':inspect_bindings()}
'''
dec_labels={'original':'function_passed_to_decorate','replacement':'returned_inner_callable','later':'wrapper_then_original'}
dec_comments_start=''.join('# BIND '+k+': TODO\n' for k in dec_labels)
dec_comments_sol=''.join('# BIND '+k+': '+v+'\n' for k,v in dec_labels.items())
dec_harness+='''
def inspect_bindings():
    source = open('main.py').read().splitlines()
    return {line[len('# BIND '):].split(':',1)[0]:line.split(':',1)[1].strip() for line in source if line.startswith('# BIND ')}
'''
dec_start=dec_comments_start+'def decorate(function):\n    pass\n'+dec_harness
dec_sol=dec_comments_sol+'def decorate(function):\n    def inner_function():\n        return function()\n    return inner_function\n'+dec_harness
exercise('python.decorator_wrappers',dec_start,dec_sol,'Complete decorate(function) by defining inner_function, whose body calls function and returns its result, then return the inner callable without calling it. The supplied harness compares function = decorate(function) with @decorate: it inspects the original-call trace before any later call, the replacement name, and the later wrapper-to-original path. In the # BIND comments, choose labels to identify original (function_passed_to_decorate or returned_inner_callable), replacement (function_passed_to_decorate or returned_inner_callable), and later (wrapper_then_original or original_without_wrapper). Keep that harness unchanged.',[call('inspect_decoration','synthetic order'),call('inspect_decoration','different order')])
asgi_harness='''
import asyncio
def check_events(status, body):
    trace = []
    request = {'type':'http.request','body':b'','more_body':False}
    async def receive():
        trace.append(['receive',request['type']])
        return request
    async def send(event):
        trace.append(['send',event['type'],event.get('status'),[[x.decode() for x in pair] for pair in event.get('headers',[])],event.get('body',b'').decode()])
    global supplied_status, supplied_body
    supplied_status, supplied_body = status, body.encode()
    coroutine = app({'type':'http','path':'/orders/42','method':'GET'},receive,send)
    try:
        coroutine.send(None)
    except StopIteration:
        pass
    responsibility = ''
    for line in open('main.py').read().splitlines():
        if line.startswith('# NETWORK_AND_INVOCATION:'):
            responsibility = line.split(':',1)[1].strip()
    return {'events':trace,'network_and_invocation':responsibility}
'''
asgi_start='supplied_status = 200\nsupplied_headers = [(b"content-type", b"application/json")]\nsupplied_body = b"{}"\n# NETWORK_AND_INVOCATION: TODO\nasync def app(scope, receive, send):\n    pass\n'+asgi_harness
asgi_sol='supplied_status = 200\nsupplied_headers = [(b"content-type", b"application/json")]\nsupplied_body = b"{}"\n# NETWORK_AND_INVOCATION: server\nasync def app(scope, receive, send):\n    request = await receive()\n    await send({"type":"http.response.start", "status":supplied_status, "headers":supplied_headers})\n    await send({"type":"http.response.body", "body":supplied_body})\n'+asgi_harness
exercise('asgi.request_lifecycle',asgi_start,asgi_sol,'Complete app(scope, receive, send): await receive once, then await send for http.response.start using supplied_status and supplied_headers, then await send for http.response.body using supplied_body. The checker supplies the events; do not choose statuses or implement networking. In # NETWORK_AND_INVOCATION replace TODO with server or application to identify who handles the network and invokes the app. Leave the harness unchanged; it varies the supplied metadata and body.',[call('check_events',200,'{}'),call('check_events',200,'{"order":42}')])
orm_harness='''
def inspect_order(identity):
    order = Order(id=identity)
    return {'table':Order.__tablename__, 'inherits_base':issubclass(Order,Base),'primary_key':[c.name for c in Order.__table__.primary_key.columns],'integer_type':str(Order.__table__.c.id.type),'annotation':str(Order.__annotations__['id']),'id':order.id}
'''
orm_import=next(f['content'] for f in assets['ws.fastapi_backend.orm_entity_mapping']['files'] if f['path']=='main.py').split('\n')[0]+'\n'
orm_sol=orm_import+'class Base(DeclarativeBase):\n    pass\nclass Order(Base):\n    __tablename__ = "orders"\n    id: Mapped[int] = mapped_column(primary_key=True)\n'+orm_harness
exercise('fastapi_backend.orm_entity_mapping',orm_import+'# Declare Base and Order here.\n'+orm_harness,orm_sol,bundles['fastapi_backend.orm_entity_mapping']['practice_anchor']['objective']+' Use only the supplied SQLAlchemy declarations; leave the inspection harness unchanged. The checker examines the inheritance, table name, integer annotation, explicit primary key and two instances with different id values. No database writes or HTTP endpoints are needed.',[call('inspect_order',42),call('inspect_order',43)],'python_asgi',['sqlalchemy'])
# Status labels are derived from the registry and remain integer assignments as the anchor requests.
status_asset=assets['ds.order_outcomes']; status_rows=[dict(zip([c['name'] for c in status_asset['columns']],r)) for r in status_asset['rows']]
status_start=next(f['content'] for f in assets['ws.http.status_selection']['files'] if f['path']=='main.py')
status_sol=''.join(r['variable_name']+' = '+repr(r['selected_status'])+'\n' for r in status_rows)
status_tail='''
def inspect_status(name):
    return globals()[name]
'''
exercise('http.status_selection',status_start+status_tail,status_sol+status_tail,'Replace the zero value in each supplied variable with the status appropriate for its named outcome. The outcomes are: '+ '; '.join(r['variable_name']+' = '+r['outcome'] for r in status_rows)+'. Keep the variable names and inspection helper unchanged. The checker grades every assignment; no endpoint implementation is needed.',[call('inspect_status',r['variable_name']) for r in status_rows])
pyd_harness='''
def inspect_input(quantity):
    first = OrderInput(quantity=quantity)
    second = OrderInput.model_validate({'quantity':quantity})
    return {'first':[first.quantity,first.note,type(first.quantity).__name__],'second':[second.quantity,second.note,type(second.quantity).__name__],'quantity_required':OrderInput.model_fields['quantity'].is_required(),'note_default':OrderInput.model_fields['note'].default,'constructed':[constructed.quantity,constructed.note],'validated':[validated.quantity,validated.note]}
'''
pyd_start='from pydantic import BaseModel\nclass OrderInput(BaseModel):\n    pass\n# Create constructed and validated with quantity="3".\n'+pyd_harness
pyd_sol='from pydantic import BaseModel\nclass OrderInput(BaseModel):\n    quantity: int\n    note: str = ""\nconstructed = OrderInput(quantity="3")\nvalidated = OrderInput.model_validate({"quantity":"3"})\n'+pyd_harness
exercise('pydantic.model_validation_conversion',pyd_start,pyd_sol,bundles['pydantic.model_validation_conversion']['practice_anchor']['objective']+' Name the constructed instance constructed and the dictionary-validated instance validated. Leave the supplied helper unchanged. It checks both stored instances, required/default declarations and conversion of two different accepted quantities.',[call('inspect_input','3'),call('inspect_input','7')],'python_asgi',['pydantic'])
# A filesystem harness gives a runnable regular-package exercise without a shell runtime.
package_harness='''
import os, importlib, runpy, sys
def inspect_package(mode):
    source = open('main.py').read().splitlines()
    entries = {}
    for line in source:
        if line.startswith('# PACKAGE '):
            key,value=line[len('# PACKAGE '):].split(':',1)
            entries[key.strip()] = value.strip()
    paths = [entries.get('marker',''),entries.get('module','')]
    for path in paths:
        if path in ['service/__init__.py','service/orders.py']:
            os.makedirs('service',exist_ok=True)
            open(path,'w').close()
    if paths != ['service/__init__.py','service/orders.py']:
        return {'files_correct':False}
    importlib.invalidate_caches()
    if mode == 'import':
        module=importlib.import_module(entries.get('qualified_import',''))
        return {'files_correct':True,'qualified_name':module.__name__,'declared_import':entries.get('qualified_import')}
    sys.modules.pop('service.orders',None)
    namespace=runpy.run_module('service.orders',run_name='__main__')
    return {'files_correct':True,'command':entries.get('command'),'observed_name':namespace['__name__'],'declared_name':entries.get('execution_name'),'relative_import_context':entries.get('relative_context')}
'''
package_answers={'marker':'service/__init__.py','module':'service/orders.py','qualified_import':'service.orders','command':'python -m service.orders','execution_name':'__main__','relative_context':'current_package'}
package_start=''.join('# PACKAGE '+k+': TODO\n' for k in package_answers)+package_harness
package_sol=''.join('# PACKAGE '+k+': '+v+'\n' for k,v in package_answers.items())+package_harness
exercise('python.service_packages',package_start,package_sol,'Complete # PACKAGE comment entries. Supply the empty regular-package marker path, empty orders module path, qualified import name, package-context execution command, and execution name. For relative_context select current_package or working_directory to identify what leading dots mean. The unchanged harness creates the empty files at the supplied paths, imports the module and executes it with the same package context as -m. This player runs the supplied Python filesystem checker, not a shell command. Do not edit the checker.',[call('inspect_package','import'),call('inspect_package','execute')])
# SQL declaration edited as comments; the supplied Python checker checks declared constraints on independent proposed rows.
schema_harness='''
import re
customers = CUSTOMER_BASELINE
orders = ORDER_BASELINE
def inspect_constraint(candidate):
    lines = open('main.py').read().splitlines()
    declaration = '\\n'.join(line[len('# SQL '):] for line in lines if line.startswith('# SQL '))
    normalized = re.sub(r'\\s+', '', declaration).lower()
    flags = {
        'primary_key':'primarykey(identity)' in normalized,
        'foreign_key':'foreignkey(customer_reference)referencescustomers(identity)' in normalized,
        'required_quantity':'quantityintegernotnull' in normalized,
        'positive_quantity':'check(quantity>0)' in normalized,
        'default_unique':'unique(external_reference)' in normalized,
        'nullable_customer':'customer_referenceintegernotnull' not in normalized,
        'nullable_external':'external_referencetextnotnull' not in normalized,
        'distinct_null_policy':'nullsnotdistinct' not in normalized
    }
    identity, customer, quantity, external = candidate
    accepted = True
    if flags['primary_key']:
        accepted = accepted and identity is not None and identity not in [r[0] for r in orders]
    if flags['foreign_key']:
        accepted = accepted and (customer is None or customer in [r[0] for r in customers])
    if flags['required_quantity']:
        accepted = accepted and quantity is not None
    if flags['positive_quantity']:
        accepted = accepted and (quantity is None or quantity > 0)
    if flags['default_unique']:
        accepted = accepted and (external is None or external not in [r[3] for r in orders])
    if not flags['distinct_null_policy']:
        accepted = accepted and external not in [r[3] for r in orders]
    return {'declared_constraints':flags,'accepted':accepted}
'''
schema_harness=schema_harness.replace('CUSTOMER_BASELINE',repr(assets['ds.customers']['rows'])).replace('ORDER_BASELINE',repr(assets['ds.orders']['rows']))
schema_start='# SQL CREATE TABLE orders (\n# SQL     identity INTEGER,\n# SQL     customer_reference INTEGER,\n# SQL     quantity INTEGER,\n# SQL     external_reference TEXT\n# SQL );\n'+schema_harness
schema_text='CREATE TABLE orders (\n    identity INTEGER,\n    customer_reference INTEGER,\n    quantity INTEGER NOT NULL,\n    external_reference TEXT,\n    PRIMARY KEY (identity),\n    FOREIGN KEY (customer_reference) REFERENCES customers (identity),\n    CHECK (quantity > 0),\n    UNIQUE (external_reference)\n);'
schema_sol=''.join('# SQL '+line+'\n' for line in schema_text.splitlines())+schema_harness
proposed=assets['ds.proposed_orders']; proposed_rows=[dict(zip([c['name'] for c in proposed['columns']],r)) for r in proposed['rows']]
exercise('database.service_integrity_constraints',schema_start,schema_sol,'Complete the supplied CREATE TABLE declaration in # SQL comment lines: primary key on identity, foreign key on customer_reference to customers(identity), quantity NOT NULL with CHECK(quantity > 0), and default UNIQUE(external_reference). Leave customer_reference and external_reference nullable; do not use NULLS NOT DISTINCT. Keep the Python checker unchanged. It inspects the declaration and uses a supplied declaration-and-predicate checker on independent proposed rows against the supplied baseline; this is not a PostgreSQL runtime.',[call('inspect_constraint',[r[k] for k in ['identity','customer_reference','quantity','external_reference']]) for r in proposed_rows])
# Replace fixed fixture literals in the schema checker with registry-supplied baseline data.
for key in ['starter','solution']:
 text=EX['database.service_integrity_constraints'][key]
 text=text.replace("[(1,),(2,)]",repr([tuple(r) for r in assets['ds.customers']['rows']]))
 text=text.replace("[(42,1,3,'ORD-A'),(43,2,1,None),(44,None,2,None)]",repr([tuple(r) for r in assets['ds.orders']['rows']]))
 EX['database.service_integrity_constraints'][key]=text
status_classes=assets['ds.http_status_classes']
class_rows=[dict(zip([c['name'] for c in status_classes['columns']],row)) for row in status_classes['rows']]
class_helper='''
def inspect_class(pattern):
    for line in open('main.py').read().splitlines():
        if line.startswith('# STATUS_CLASS '+pattern+':'):
            return line.split(':',1)[1].strip()
    return 'missing'
'''
for key in ['starter','solution']:
 e=EX['http.status_selection']
 e[key]+=''.join('# STATUS_CLASS '+r['status_class_pattern']+': '+('TODO' if key=='starter' else r['meaning'])+'\n' for r in class_rows)+class_helper
EX['http.status_selection']['probes'] += [call('inspect_class',r['status_class_pattern']) for r in class_rows]
EX['http.status_selection']['prompt'] += ' Also label each # STATUS_CLASS pattern as informational, successful, redirection, client error or server error. Each class comment is graded.'
# The glossary uses intent descriptors (e.g. `class Draft:`) without Python AST detectors.
# Provide a small comment-source editor and unchanged compiler scaffold: only learner lines
# execute as the requested Python/raw declaration, while the supplied harness remains scaffold.
# This avoids widening the frozen syntax lists for an implementation limitation.
compiler="\n# Supplied compiler: keep unchanged. It executes the # PY source lines below.\nexec('\\n'.join(line[5:] for line in open('main.py').read().splitlines() if line.startswith('# PY ')), globals())\n"
for cid,e in EX.items():
 if e['kind']=='python_asgi': continue
 for key in ['starter','solution']:
  code=e[key]
  external=''
  if cid=='python.classes_and_instances':
   external=code.splitlines()[0]+'\n'; code='\n'.join(code.splitlines()[1:])+'\n'
  e[key]=external+'\n'.join(line if line.startswith('#') else '# PY '+line for line in code.splitlines())+'\n'+compiler
 e['prompt']+=' In this supplied comment-source editor, Python source lines have a # PY prefix. Keep that prefix and edit the requested code after it; the unchanged compiler executes those lines. Lines belonging to the supplied checker are scaffolding, not new syntax to learn.'
# Assemble all expected values in one pinned-engine run per runtime group.
results={}
for kind in ['python','python_asgi']:
 scripts=[]
 for cid,e in EX.items():
  if e['kind']!=kind: continue
  scripts.append({'id':cid,'files':[{'path':'main.py','content':e['solution']}],'entry':'main.py','mounts':[], 'probes':[{'id':'test'+str(i+1),'kind':'call' if k=='function_call' else 'expr',**({'function':sp['function'],'args':sp.get('args',[]),'kwargs':sp.get('kwargs',{})} if k=='function_call' else {'expr':sp['expr']})} for i,(k,sp) in enumerate(e['probes'])]})
 job=sandbox._py_job(kind,list(set(p for e in EX.values() if e['kind']==kind for p in e['packages'])),scripts)
 results.update(sandbox.node_run(job,'run_py.mjs')['results'])
(B/'working/expected_execution.json').write_text(json.dumps(results,indent=2))
for cid,e in EX.items():
 result=results[cid]
 if not result['ok']: raise RuntimeError((cid,result))
 tests=[]
 for i,(kind,spec) in enumerate(e['probes']):
  tid='test'+str(i+1); probe=result['probes'][tid]
  if not probe['ok']: raise RuntimeError((cid,tid,probe))
  tests.append({'test_id':tid,'kind':kind,'message_on_fail':'Recheck the requested edit and the supplied evidence.','spec':{**spec,'expected':probe['value']}})
 e['tests']=tests
# Feedback targets are copied, never fabricated.
rem={}
for t in screens['tiles']:
 for s in t.get('remediation_steps',[]):
  for cid in s['concept_ids']: rem.setdefault(cid,[]).append(s['step_id'])
out={k:plan[k] for k in ['schema_version','path_id','batch_id']};out.update(kind='interactions_part',tiles=[])
for t in plan['tiles']:
 interactions=[]
 planned=[s for s in t['steps'] if s['type'] in ['check','hands_on']]
 seen=set()
 for n,s in enumerate(planned):
  cid=s['concept_ids'][0];b=bundles[cid]
  measures=[]
  for anchor in s['anchors']:
   if '#assessment:' in anchor:
    capability=anchor.split('#assessment:')[1]
    a=next(a for a in b['assessment_anchors'] if a['capability']==capability)
    measures.append({'concept_id':cid,'capability':capability,'fact_ids':a['fact_ids']})
  if not measures:
   assessment=b['assessment_anchors'][-1]
   measures=[{'concept_id':cid,'capability':assessment['capability'],'fact_ids':assessment['fact_ids']}]
  ix={'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'],'difficulty':'intro' if n==0 else ('stretch' if n==len(planned)-1 else 'core'),'grading_mode':'client','standalone':True,'measures':measures,'anchors':s['anchors']}
  if ix['type']=='choice':
   prompt,answer,wrong=Q[s['step_id']]
   options=[(answer,'Correct: '+answer)]+wrong
   # Rotate the key deterministically so correct answers are not always first.
   rotate=n%len(options); options=options[rotate:]+options[:rotate]
   ids=['option'+str(i+1) for i in range(len(options))]
   ix['public']={'prompt':prompt,'options':[{'option_id':k,'text':v[0]} for k,v in zip(ids,options)],'selection':'single','shuffle':True}
   ix['grading']={'correct_option_ids':[k for k,v in zip(ids,options) if v[0]==answer],'option_feedback':{k:{'message':v[1]} for k,v in zip(ids,options)}}
   correct=answer; hint='Separate the roles named in the prompt; apply the taught distinction rather than treating them as interchangeable.'
  elif ix['type']=='classify':
   ix.update(C[cid]);correct='Each judgement follows the specific evidence in its excerpt or URL, not a package name, response alone or an unrelated permission.';hint='Compare the evidence component by component. Look for an excerpt that appears successful but misses a required condition.'
  else:
   e=EX[cid];lc=b['practice_anchor']['live_code']
   ix['public']={'prompt':e['prompt'],'runtime':{'kind':e['kind'],'version':runtimes[e['kind']]['version'],'packages':e['packages']},'workspace':{'files':[{'path':'main.py','role':'editable','language':'python','content':e['starter']}],'entry':'main.py','asset_mounts':e['mounts']},'constraints':{k:lc[k] for k in ['allowed_syntax','blocked_syntax']}}
   ix['grading']={'solution_files':[{'path':'main.py','content':e['solution']}],'tests':e['tests']}
   correct='The submitted edits meet the requested practice conditions across the supplied checks.';hint='Change only the requested learner-owned lines; leave the supplied inspection or execution harness unchanged.'
  ix['feedback']={'correct':{'message':correct},'incorrect':{'message':'Recheck the taught rule and the specific evidence. '+(b['coverage']['required_facts'][0]['statement'] if ix['type']!='choice' else 'Read the explanation for the selected option.')},'hints':[hint]}
  if rem.get(cid): ix['feedback']['remediation_step_id']=rem[cid].pop(0)
  seen.add(cid)
  interactions.append({'step_id':s['step_id'],'interaction':ix})
 out['tiles'].append({'tile_id':t['tile_id'],'interactions':interactions})
(B/'interactions.json').write_text(json.dumps(out,indent=2)+'\n')
print('Wrote',sum(len(t['interactions']) for t in out['tiles']),'interactions')
