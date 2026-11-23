import json, re, sys, importlib.metadata as metadata
from pathlib import Path
from urllib.parse import urlsplit
B=Path('batches/final_batch_foundations_1')
G=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
bundles={b['context']['concept_id']:b for b in G['bundles']}
S='scenario.orders_service'
assets=[]
def col(name,type,role,description='',label=False):
    c=dict(name=name,type=type,semantic_role=role)
    if description:c['description']=description
    if label:c['numeric_looking_label']=True
    return c
def dataset(id,title,columns,rows,description):
    a=dict(asset_id=id,asset_kind='dataset',scenario_id=S,title=title,description=description,columns=columns,rows=rows,provenance='authored')
    assets.append(a);return a
def ws(concept,runtime,files):
    b=bundles[concept]
    instructions={'concept_id':concept,'practice_anchor':b['practice_anchor'],'visual_anchor':b['visual_anchor']}
    files={**files,'exercise_intent.json':json.dumps(instructions,indent=2)+'\n'}
    assets.append(dict(asset_id='ws.'+concept,asset_kind='code_workspace',scenario_id=S,title=b['context']['concept_name']+' — starter',runtime=runtime,files=[dict(path=k,content=v) for k,v in files.items()]))
# Mine actual teaching and anchor text, not source references or future concepts.
texts=[]
for b in G['bundles']:
    texts.extend(t['content'] for t in b['teaching_blocks'])
    texts.append(json.dumps(b['practice_anchor'],ensure_ascii=False))
    texts.append(json.dumps(b['visual_anchor'],ensure_ascii=False))
text='\n'.join(texts)
terms=['orders','customers','identity','customer_reference','quantity','external_reference','id','Order','OrderInput','Draft','draft_a','draft_b','self.items','__init__','note','item_names','tags','identifier_name','counts','order_summary','Content-Type','Accept','application/json','GET','HEAD','POST','PUT','DELETE','OPTIONS','Origin','Access-Control-Request-Method','Access-Control-Request-Headers','content-type','Access-Control-Allow-Origin','Access-Control-Allow-Methods','Access-Control-Allow-Headers','Access-Control-Allow-Credentials','CORS','ASGI','scope','receive','send','http.request','http.response.start','http.response.body','asyncio.sleep(0)','function','decorate','inner_function','pwdlib','PasswordHash.recommended()','hash(password)','verify(plain_password, stored_hash)','Base','DeclarativeBase','Mapped[int]','mapped_column(primary_key=True)','BaseModel','ValidationError','model_validate','many','service/__init__.py','service/orders.py','service.orders','__main__','.venv','requirements.txt','python -m pip freeze','python -m pip install -r requirements.txt','python -m service.orders','NOT NULL','PRIMARY KEY','FOREIGN KEY','CHECK','UNIQUE','NULLS NOT DISTINCT','PostgreSQL']
vocab=sorted(set(t for t in terms if t in text)|set(re.findall(r'https?://[A-Za-z0-9.:/]+',text))|set(re.findall(r'\b\d+\b',text)))
# A fixed API and every browser-page URL supplied by the glossary.
origin_b=bundles['browser.same_origin_boundary']
api=re.search(r'https://[^\s]+',origin_b['practice_anchor']['objective']).group().rstrip('.')
urls=re.findall(r'https?://[A-Za-z0-9.:/]+',origin_b['practice_anchor']['success'])
def origin(url):
    p=urlsplit(url);return p.scheme,p.hostname,p.port or (443 if p.scheme=='https' else 80)
fixed=origin(api)
origin_rows=[]
for url in urls:
    p=urlsplit(url); parts=origin(url)
    differs=[n for n,x,y in zip(['scheme','host','port'],fixed,parts) if x!=y]
    origin_rows.append([api,*fixed,url,*parts,p.path,'cross-origin' if differs else 'same-origin',','.join(differs) or 'none'])
dataset('ds.browser_origins','Calls to one fixed API',[
 col('api_url','string','text'),col('api_scheme','string','categorical'),col('api_host','string','categorical'),col('api_port','integer','categorical','Origin component, not a measured magnitude.',True),
 col('browser_url','string','text'),col('browser_scheme','string','categorical'),col('browser_host','string','categorical'),col('browser_port','integer','categorical','Origin component, not a measured magnitude.',True),col('browser_path','string','text'),col('origin_classification','string','categorical'),col('differing_components','string','categorical')],origin_rows,'Authored hypothetical URL comparison. Origin classifications are computed from scheme, host and port. Browser response access and endpoint authorization are independent and not encoded as inferred permissions here.')
# The status table is extracted from the paired success/observable-success lists.
st=bundles['http.status_selection']['practice_anchor']['live_code']
variables=re.findall(r'order_[a-z_]+_status',st['starter_state_intent'])
codes=list(map(int,re.search(r'hold ([0-9, and]+) respectively',st['observable_success']).group(1).replace('and','').split(',') ))
classes={1:'informational',2:'successful',3:'redirection',4:'client error',5:'server error'}
status_rows=[[v,v.removeprefix('order_').removesuffix('_status').replace('_',' '),classes[c//100],c] for v,c in zip(variables,codes)]
dataset('ds.order_outcomes','Orders HTTP outcomes',[col('variable_name','string','identifier'),col('outcome','string','categorical'),col('status_class','string','categorical'),col('selected_status','integer','categorical','Protocol outcome label, not a quantity.',True)],status_rows,'Named workflow outcomes and selected status labels from the glossary practice. Codes are extracted from its ordered observable-success list.')
dataset('ds.http_status_classes','Five HTTP status classes',[col('status_class_pattern','string','categorical'),col('meaning','string','categorical')],[[str(k)+'xx',v] for k,v in classes.items()],'Compact key including informational and redirection outcomes; no particular informational or redirection status is asserted.')
customers=dataset('ds.customers','customers',[col('identity','integer','identifier','Synthetic customer primary key.',True)],[[1],[2]],'Authored referenced identities for constraint examples, not real customer records.')
orders=dataset('ds.orders','orders',[col('identity','integer','identifier','Synthetic non-null order row identity.',True),col('customer_reference','integer','identifier','Nullable reference to customers.identity.',True),col('quantity','integer','numerical','Required positive item count.'),col('external_reference','string','identifier','Optional external order label; nulls are distinct under the taught UNIQUE default.')],[[42,1,3,'ORD-A'],[43,2,1,None],[44,None,2,None]],'Authored valid baseline. quantity has NOT NULL and CHECK (quantity > 0); identity is the primary key; customer_reference is optional but non-null references must exist; external_reference is optional and unique when non-null.')
variants=[]
def variant(name,ops,issues=[]):
    variants.append(dict(variant_id='var.orders.'+name,derived_from=orders['asset_id'],purpose=name.replace('_',' '),ops=ops,planted_issues=issues))
def issue(name,kind,column,where,rule=None,occurrence=0):
    d=dict(issue_id='issue.'+name,kind=kind,locations=[dict(where=where,occurrence=occurrence,column=column)],description=name.replace('_',' '))
    if rule:d['rule']=rule
    return d
def setop(column,value):return dict(op='set_cell',where={'identity':42},occurrence=0,column=column,value=value)
variant('null_quantity',[setop('quantity',None)],[issue('null_quantity','missing_value','quantity',{'identity':42})])
variant('nonpositive_quantity',[setop('quantity',0)],[issue('nonpositive_quantity','impossible_value','quantity',{'identity':42},{'column':'quantity','op':'le','value':0})])
variant('negative_quantity',[setop('quantity',-1)],[issue('negative_quantity','impossible_value','quantity',{'identity':42},{'column':'quantity','op':'lt','value':0})])
variant('duplicate_row',[dict(op='duplicate_row',where={'identity':42},occurrence=0,insert='end')],[issue('duplicate_order','duplicate_row','identity',{'identity':42},occurrence=1)])
variant('null_identity',[setop('identity',None)],[issue('null_identity','missing_value','identity',{'identity':None})])
variant('unmatched_customer',[setop('customer_reference',99)],[issue('customer_reference_not_in_supplied_customers','other','customer_reference',{'identity':42},{'column':'customer_reference','op':'eq','value':99})])
variant('duplicate_external_reference',[dict(op='set_cell',where={'identity':43},occurrence=0,column='external_reference',value=orders['rows'][0][3])],[issue('external_reference_matches_existing_order_42','other','external_reference',{'identity':43},{'column':'external_reference','op':'eq','value':orders['rows'][0][3]})])
orders['variants']=variants
# Every proposed row is evaluated as one independent insertion against the baseline.
proposals=[('valid_new_order',[45,1,1,'ORD-B']),('null_identity',[None,1,1,'ORD-B']),('duplicate_identity',[42,1,1,'ORD-B']),('unmatched_customer',[45,99,1,'ORD-B']),('null_customer',[45,None,1,'ORD-B']),('null_quantity',[45,1,None,'ORD-B']),('zero_quantity',[45,1,0,'ORD-B']),('negative_quantity',[45,1,-1,'ORD-B']),('duplicate_external',[45,1,1,'ORD-A']),('repeated_null_external',[45,1,1,None])]
base=orders['rows'];customer_ids={r[0] for r in customers['rows']}
proposal_rows=[]
for case,row in proposals:
    identity,customer,q,ext=row
    pk=identity is not None and all(r[0]!=identity for r in base)
    fk=customer is None or customer in customer_ids
    nn=q is not None
    check=q is None or q>0
    unique=ext is None or all(r[3]!=ext for r in base)
    unique_nd=all(r[3]!=ext for r in base)
    rejected=[name for name,ok in [('PRIMARY KEY',pk),('FOREIGN KEY',fk),('NOT NULL',nn),('CHECK',check),('UNIQUE',unique)] if not ok]
    proposal_rows.append([case,*row,pk,fk,nn,check,unique,unique_nd,'accept' if not rejected else 'reject',', '.join(rejected) or 'none'])
dataset('ds.proposed_orders','Independent proposed orders and constraint outcomes',[col('case_id','string','identifier'),*orders['columns'],*[col(n,'boolean','categorical') for n in ['primary_key_passes','foreign_key_passes','not_null_passes','check_alone_passes','unique_default_passes','unique_nulls_not_distinct_passes']],col('combined_outcome','string','categorical'),col('rejecting_constraints','string','text')],proposal_rows,'Each candidate is evaluated independently against ds.orders and ds.customers, not sequentially inserted. Computed CHECK-alone results accept null; combined results require NOT NULL. The hypothetical NULLS NOT DISTINCT comparison is separate from the requested default unique-null policy.')
ws('http.representation_headers','raw_http',{'request.http':'POST /orders HTTP/1.1\nHost: shop.example\nContent-Type: \nAccept: \n\n{"quantity": 3}\n','response.http':'HTTP/1.1 201 Created\nContent-Type: application/json\n\n{"quantity": 3}\n'})
ws('python.backend_type_annotations','python',{'main.py':'def order_summary(item_names, tags, identifier_name, counts, note):\n    return counts\n'})
ws('python.classes_and_instances','python',{'main.py':'class Draft:\n    # Initialize independent items on each instance.\n    pass\n\n# Create draft_a and draft_b; append one item only to draft_a.\n'})
ws('python.context_managed_cleanup','python',{'main.py':'# Use with open("orders.txt") as file: and keep file.read() in its scope.\n','orders.txt':'Synthetic order note\n','harness.py':'''import builtins
from pathlib import Path
# Infrastructure, not learner-authored syntax. Execute completed main.py twice.
source = Path("main.py").read_text()
real_open = builtins.open
for failing in (False, True):
    opened = []
    class ReadingFailure:
        def __init__(self, f): self.f = f
        def __enter__(self): self.f.__enter__(); return self
        def read(self): raise RuntimeError("injected read failure")
        def __exit__(self, *args): return self.f.__exit__(*args)
    def supplied_open(*args, **kwargs):
        f = real_open(*args, **kwargs)
        opened.append(f)
        return ReadingFailure(f) if failing else f
    propagated = False
    try:
        exec(source, {"open": supplied_open})
    except RuntimeError:
        propagated = True
    assert opened and all(f.closed for f in opened)
    assert propagated == failing
'''})
ws('python.cooperative_async','python',{'main.py':'''import asyncio
async def immediate():
    return 1
async def task_a(pending_io):
    result = await immediate()
    io_result = await pending_io
    await asyncio.sleep(0)
    return result
# Annotate creation, execution, waiting and continuation without exact task-order claims.
''','harness.py':'''import asyncio
from main import task_a
async def run():
    future = asyncio.get_running_loop().create_future()
    coroutine = task_a(future)
    task = asyncio.create_task(coroutine)
    await asyncio.sleep(0)
    future.set_result(1)
    return await task
if __name__ == "__main__":
    asyncio.run(run())
'''})
ws('python.decorator_wrappers','python',{'main.py':'def function():\n    return "synthetic order"\n\ndef decorate(function):\n    # Define inner_function and return the callable, not a call result.\n    pass\n\n# Compare explicit decoration with @decorate in a separate example.\n'})
# Use a locally installed, inspectable Python package instead of inventing versions.
package='jsonschema'
seen={}
def visit(name):
    dist=metadata.distribution(name);key=dist.metadata['Name']
    if key in seen:return
    seen[key]=dist.version
    from pip._vendor.packaging.requirements import Requirement
    for raw in dist.requires or []:
        r=Requirement(raw)
        if r.marker is None or r.marker.evaluate({'extra':''}): visit(r.name)
visit(package)
requirements=''.join(f'{n}=={v}\n' for n,v in sorted(seen.items()))
host={'python_executable':sys.executable,'package':package,'version':metadata.version(package),'package_location':str(metadata.distribution(package).locate_file(''))}
ws('python.isolated_environments','terminal',{'commands.txt':'# Create .venv, activate it, verify its interpreter, install jsonschema, and inspect it.\n','supplied_dependencies.json':json.dumps({'dependency_names':[package],'host_comparison':host},indent=2)+'\n'})
ws('asgi.request_lifecycle','python',{'main.py':'async def app(scope, receive, send):\n    # Receive once, then send response start and body using supplied literals.\n    pass\n','supplied_events.json':json.dumps({'scope':{'type':'http','method':'GET','path':'/orders/42'},'request':{'type':'http.request','body':'','more_body':False},'status':200,'headers':[['content-type','application/json']],'body':'{}'},indent=2)+'\n','harness.py':'''import asyncio
import json
from main import app
async def run():
    supplied = json.load(open("supplied_events.json"))
    request = dict(supplied["request"], body=b"")
    trace = []
    async def receive():
        trace.append(("receive", request))
        return request
    async def send(event):
        trace.append(("send", event))
    await app(supplied["scope"], receive, send)
    expected = [("receive", request), ("send", {"type":"http.response.start", "status":supplied["status"], "headers":[tuple(x.encode() for x in pair) for pair in supplied["headers"]]}), ("send", {"type":"http.response.body", "body":supplied["body"].encode()})]
    assert trace == expected
    return trace
if __name__ == "__main__":
    asyncio.run(run())
'''})
ws('auth.local_password_verification','python',{'main.py':'from pwdlib import PasswordHash\n\npassword = "synthetic-order-password"\ndifferent_password = "different-synthetic-password"\n# Create password_hash, stored_hash, matching_result and nonmatching_result.\n','environment_notes.txt':'Requires pwdlib with its recommended hashing backend. Do not store plaintext as stored_hash. Runtime dependency availability must be verified by the exercise runner.\n'})
ws('fastapi_backend.orm_entity_mapping','python',{'main.py':'from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column\n\n# Declare shared Base, then Order mapped to orders with an integer id primary key.\n','environment_notes.txt':'Requires SQLAlchemy providing DeclarativeBase, Mapped and mapped_column. No database write is needed.\n'})
ws('http.cors_preflight','http_tool_simulation',{'request.http':'OPTIONS /orders/42 HTTP/1.1\nHost: api.example\nOrigin: \nAccess-Control-Request-Method: \nAccess-Control-Request-Headers: \n\n','response.http':'HTTP/1.1 204 No Content\nAccess-Control-Allow-Origin: https://shop.example\nAccess-Control-Allow-Methods: PUT\nAccess-Control-Allow-Headers: content-type\n\n','credentialed_response.http':'HTTP/1.1 200 OK\nAccess-Control-Allow-Origin: https://shop.example\nAccess-Control-Allow-Credentials: true\n\n','wildcard_credentialed_response.http':'HTTP/1.1 200 OK\nAccess-Control-Allow-Origin: *\nAccess-Control-Allow-Credentials: true\n\n','tool_notes.txt':'Static hypothetical exchanges for comparison. An OPTIONS permission response is not completion of PUT. Tool-simulation execution must be provided by a later runner; these files are not a live server.\n'})
ws('http.status_selection','python',{'main.py':''.join(v+' = 0\n' for v in variables)})
ws('pydantic.model_validation_conversion','python',{'main.py':'from pydantic import BaseModel\n\nclass OrderInput(BaseModel):\n    # Declare required quantity and defaulted note.\n    pass\n\n# Construct with quantity="3" and validate equivalent dictionary input.\n','input_cases.json':json.dumps([{'quantity':'3'},{'quantity':3},{},{'quantity':'many'}],indent=2)+'\n','environment_notes.txt':'Requires Pydantic supporting BaseModel.model_validate. Input fixtures are authored; validated outputs and error details must be executed, not guessed.\n'})
ws('python.reproducible_dependencies','terminal',{'requirements.txt':requirements,'commands.txt':'# In the supplied clean environment, install from committed requirements.txt.\n# Inspect installed versions with python -m pip freeze. Do not change the declaration.\n','environment_notes.txt':'Pins are computed from the locally installed jsonschema dependency tree. A clean runner needs these exact packages available for installation; no claim of offline availability is made.\n'})
ws('python.service_packages','python_terminal',{'orders.py':'','service/README.txt':'Place orders.py here and add an empty __init__.py.\n','answers.txt':'qualified_import = \nexecution_command = \nexecution_name = \n'})
ws('database.service_integrity_constraints','postgresql',{'schema.sql':'-- customers already exists with identity as its primary key.\nCREATE TABLE orders (\n    identity INTEGER,\n    customer_reference INTEGER,\n    quantity INTEGER,\n    external_reference TEXT\n    -- Complete supplied field and table constraint positions.\n);\n','existing_customers.json':json.dumps({'table':'customers','primary_key':['identity'],'columns':customers['columns'],'rows':customers['rows']},indent=2)+'\n','environment_notes.txt':'PostgreSQL semantics are required for the stated default UNIQUE null policy and optional NULLS NOT DISTINCT contrast. Starter does not perform writes. Registered proposed rows are independent examples against the supplied baseline.\n'})
registry=dict(schema_version='1.0',kind='scenario_asset_registry',path_id=G['path_id'],batch_id=B.name,scenarios=[dict(scenario_id=S,name='Fictional orders service workshop',summary='A fictional shop maintains an orders service at shop.example and api.example. Learners inspect hypothetical browser and HTTP exchanges, edit small independent Python modules, and compare synthetic order rows with database constraints. All records, passwords and HTTP fixtures are authored teaching examples, not real accounts or production traffic.',domain='orders backend development',glossary_example_vocab=vocab)],assets=assets)
(B/'scenario_asset_registry.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n')
print('Scenarios',len(registry['scenarios']),'assets',len(assets),'datasets',sum(a['asset_kind']=='dataset' for a in assets),'workspaces',sum(a['asset_kind']=='code_workspace' for a in assets))
