import json,re,copy
from pathlib import Path
P=Path('batches/final_batch_implementation')
plan=json.loads((P/'tile_plans.json').read_text()); g=json.loads((P/'inputs/path_glossary_bundle.json').read_text()); registry=json.loads((P/'scenario_asset_registry.json').read_text())
B={b['context']['concept_id']:b for b in g['bundles']}; A={a['asset_id']:a for a in registry['assets']}
def lineage(c,tbs,facts,anchors=None):
 d={'concept_ids':c,'teaching_block_ids':tbs,'fact_ids':facts}
 if anchors:d['anchors']=anchors
 return d
def prose(text,lin,role='walkthrough'):return {'type':'prose','text':text,'role':role,'lineage':copy.deepcopy(lin)}
# Short worked traces: each stays inside its own glossary boundary.
walk={
'rest.resource_contract_design':'Keep resource identity separate from the operation: /orders is the collection; /orders/{order_id} identifies an item. GET retrieves, POST processes collection creation, PUT replaces the target, and DELETE removes it. A creation contract can pair 201 with Location /orders/42; an absent item can use 404. Changing the method changes the semantics even when the item path stays the same.',
'fastapi.path_operations':'Review method, path, and declaration order together. GET and PUT on the item path register different operations. Declare /orders/current before a conflicting /orders/{order_id} route: the earlier parameterized route can capture the fixed path. A later fixed declaration does not automatically win.',
'fastapi.validated_environment_configuration':'Declare required typed fields on a BaseSettings subclass, then construct Settings(). Compare valid, missing, and invalid external values: missing required settings and invalid values fail validation. Configure a dotenv file with SettingsConfigDict(env_file=".env"). If both sources supply a key, the environment takes precedence; priority does not remove type validation.',
'integration.async_http_requests':'One owning scope can reuse an AsyncClient for several awaited lookups, benefiting from connection pooling. Avoid constructing a new client inside a hot loop. Awaiting get or post performs a request; it does not close the client. Close at the end of the owning scope with the async context manager or await client.aclose().',
'pydantic.domain_validation':'For the booking rule, end must be later than start. Use individually valid values that violate that relationship to isolate the invariant. An after-model instance validator raises ValueError on failure; construction then raises ValidationError. A consistent pair succeeds and the validator returns self. For a custom single-field check, use an after-field classmethod validator and return the accepted value.',
'fastapi.expected_http_errors':'At the absent-order branch, raise HTTPException with the intended status and client-facing detail. The raise stops normal operation work and produces a deliberate HTTP rejection; returning the exception object is different. FastAPI puts the supplied detail under the default JSON key detail. Supply headers when the rejection requires metadata, such as an authentication challenge.',
'fastapi.handler_execution_choice':'Match the handler to the I/O library. Awaitable operations fit async def with await. Blocking I/O fits a normal def path operation, which FastAPI runs in an external thread pool. Moving a blocking call into a directly called helper does not automatically offload it: inside async def, that call can block the event loop.',
'fastapi.modular_application':'Register feature operations on an APIRouter, then import and include it in the application assembly module. Defining the router alone does not assemble it. Including a local /orders operation with prefix /api produces /api/orders. The include point can also supply tags, dependencies, and responses.',
'fastapi.path_query_binding':'In /orders/{order_id}, declare order_id: int to bind and convert the path value. An ordinary scalar limit outside the path binds from the query. A default permits omission; no default makes it required. A nonconvertible path value fails validation instead of reaching the handler unconverted. Source, conversion, and omission are separate decisions.',
'fastapi.response_model_serialization':'PublicOrder lists intended public fields, leaving out the internal private processing note. Set response_model=PublicOrder to validate, serialize, and filter a normally returned value. response_model takes priority over a return annotation. Inspect the return form too: returning a Response directly bypasses automatic model conversion and filtering, leaving its content to the application.',
'fastapi_backend.depends':'Declare a typed parameter with Annotated[Type, Depends(provider)]. Pass the callable, not provider(). FastAPI resolves the provider and supplies its result before calling the operation. Another operation can declare the same provider for reusable input-provision logic. This is an explicit input, not an application-wide hidden value store.',
'integration.outbound_timeouts':'Configure a finite HTTPX timeout for the shipping lookup. Connect, pool, read, and write have distinct waits; read and write limits apply to individual chunks, not total elapsed time. Timely successive chunks can still extend total duration. For a total budget, use async with asyncio.timeout(seconds) and catch TimeoutError outside the context. Keep that separate from HTTPX timeout exceptions; timeout=None disables enforcement.',
'design.backend_separation_of_concerns':'Keep HTTP adaptation in the handler, the order decision in a plain callable with explicit inputs, and stored-state access in a persistence adapter. A dependency can supply reusable input provisioning through a declared handler parameter. Separate responsibilities, not just files: moving the same mixture into several modules does not establish those boundaries.',
'fastapi.bounded_background_tasks':'Declare BackgroundTasks and register a callable with background_tasks.add_task(callable, *args, **kwargs). The response is sent before follow-up work runs in the application process. The callable may use def or async def. If the process fails, survival or delivery cannot be guaranteed. Scheduling therefore does not prove durable completion.',
'fastapi.dependency_composition':'The pagination provider declares typed page and page_size query inputs. FastAPI extracts those inputs and resolves pagination before supplying its result to order-options; the consuming operation then receives the order-options result. A provider declares a prerequisite with Annotated[Type, Depends(other_provider)]. Trace from prerequisites toward consumers, not the reverse.',
'fastapi.existing_middleware_stack':'Add A first and B second with app.add_middleware and each maintained component’s documented options. B is the outermost wrapper. Requests traverse B → A → handler; the resulting response traverses handler → A → B. Addition order explains both directions, but the traversal sequences are not identical. Configure the components rather than implementing their protocols.',
'fastapi.production_asgi_serving':'Use an ASGI server import string: main:app names module main and application object app. The supplied command selects its host and port without reload. --reload is useful in development, but consumes resources and is less stable, so do not enable it in production. --workers starts multiple processes and is mutually exclusive with --reload; choose worker count for the deployment.'
}

contrasts={
'rest.resource_contract_design':{'f1':'GET and PUT can address the same order item but request different operations.','f2':'/orders names the collection; /orders/{order_id} names an identified item.','f3':'Retrieval uses GET; replacement uses PUT, even on the same item path.','f4':'Contrast a creation contract using 201 and Location /orders/42 with an absent-item contract using 404.'},
'fastapi.path_operations':{'f1':'The application decorator registers a handler; the path text alone does not register a method.','f2':'GET and PUT on the same order-item path are two operations, not one.','f3':'Put /orders/current first; an earlier conflicting /orders/{order_id} can capture that request.'},
'fastapi.validated_environment_configuration':{'f1':'Declare app_name as a required typed setting, rather than accepting unchecked external configuration.','f2':'Compare a valid setting with a missing required setting: only the valid case satisfies construction.','f3':'When APP_NAME appears in both sources, the environment wins, not the dotenv file.'},
'integration.async_http_requests':{'f1':'Await the outbound lookup; writing an AsyncClient request without await is not the taught asynchronous call.','f2':'Reuse one client for the repeated shipping lookups, rather than constructing one for every loop iteration.','f3':'Finishing a lookup is not cleanup; the owning scope still closes its client.'},
'pydantic.domain_validation':{'f1':'The booking start/end relationship is a model invariant, not just a check on one field.','f2':'The failing booking branch raises ValueError; the successful branch returns self.','f3':'A one-field after validator returns its accepted value; an after-model validator returns self.','f4':'Compare a booking with end before start against one with end later than start; both inputs must first satisfy their field types.'},
'fastapi.expected_http_errors':{'f1':'Raise at the absent-order branch rather than returning the exception object.','f2':'Put required rejection metadata in headers, not just in the detail message.','f3':'For the absent-order rejection, the default body key is detail, not an invented key.'},
'fastapi.handler_execution_choice':{'f1':'The supplied shipping client blocks: choose a normal def path operation, not async def merely by spelling.','f2':'A normal def path operation is run in the external thread pool; async def uses asynchronous execution.','f3':'Moving shipping_client.lookup into a directly called helper does not automatically offload it from an async handler.'},
'fastapi.modular_application':{'f1':'Register orders operations on the feature router, rather than requiring the main module to contain every handler.','f2':'An orders router definition alone is not assembly; the application must include it.','f3':'The local /orders path plus inclusion prefix /api gives /api/orders, not the unchanged local path.'},
'fastapi.path_query_binding':{'f1':'order_id occurs in the path placeholder; limit does not.','f2':'An ordinary scalar limit outside the path is a query input, not another path input.','f3':'Compare limit with a default against limit without one: omission is allowed only in the defaulted declaration.','f4':'A nonconvertible order_id stops at validation; it does not enter the handler as the original string.'},
'fastapi.response_model_serialization':{'f1':'A normally returned internal order is processed against PublicOrder, not serialized indiscriminately.','f2':'The public fields omit private_processing_note even though the internal order contains it.','f3':'If both are supplied, response_model wins over the return annotation, not the reverse.','f4':'A directly returned Response bypasses filtering; a normally returned internal order follows response-model processing.'},
'fastapi_backend.depends':{'f1':'Declare the provider-supplied context as a handler parameter, rather than calling provider in the operation.','f2':'Depends(provider) passes the callable; Depends(provider()) calls it in the declaration instead.','f3':'Several order operations can declare the same provider; the needed input remains visible at each consumer.'},
'integration.outbound_timeouts':{'f1':'Repeated timely chunks can satisfy the read wait limit while total shipping-lookup duration keeps growing.','f2':'A finite shipping timeout bounds waits; timeout=None disables enforcement.','f3':'A stalled read chunk corresponds to ReadTimeout; an exceeded connect wait corresponds to ConnectTimeout.','f4':'Catch the total-budget TimeoutError outside asyncio.timeout, rather than treating it as an HTTPX ReadTimeout.'},
'design.backend_separation_of_concerns':{'f1':'Declare reusable quantity provisioning as a handler parameter, rather than repeating that input logic inside each operation.','f2':'The handler adapts HTTP, the plain callable decides the order rule, and the adapter accesses stored state.','f3':'Three files containing the same mixture are not three responsibility boundaries.'},
'fastapi.bounded_background_tasks':{'f1':'Register the follow-up callable and arguments; its scheduled work runs after the response.','f2':'The follow-up callable may use either def or async def.','f3':'An order response can be sent before a process failure loses pending follow-up work: scheduling is not guaranteed delivery.'},
'fastapi.dependency_composition':{'f1':'Order-options declares pagination as a prerequisite, not a hidden global value.','f2':'Resolve pagination before order-options, not after calling its consumer.','f3':'The typed query inputs are extracted before pagination supplies its result to order-options.'},
'fastapi.existing_middleware_stack':{'f1':'Adding A then B puts B outside A, not inside it.','f2':'Configure supplied maintained A and B through their documented keyword options; do not implement their protocols.','f3':'Requests travel B → A → handler; responses travel handler → A → B, not the same sequence.'},
'fastapi.production_asgi_serving':{'f1':'In main:app, main is the module and app is the application object, not the reverse.','f2':'Leave reload to development; the production command does not enable it.','f3':'Workers provide multiple processes; reload is not process management and cannot be combined with workers.'}
}

# Data and fixture contents are read, never retyped.
def file(c,name):return next(f['content'] for f in A['ws.'+c]['files'] if f['path']==name)
def code_visual(c,lin):
 code=file(c,'settings.py' if c=='fastapi.validated_environment_configuration' else 'main.py')
 if c=='fastapi.path_operations':
  code=code.replace('# TODO: import FastAPI and construct app.','from fastapi import FastAPI\napp = FastAPI()')
  code=re.sub(r'# TODO: register (GET|POST|PUT|DELETE) ([^ .]+)[^\n]*',lambda m:'@app.'+m[1].lower()+'('+repr(m[2])+')',code)
 elif c=='fastapi.validated_environment_configuration':
  code=code.replace('    # TODO: declare required app_name: str and dotenv model_config.\n    pass','    app_name: str\n    model_config = SettingsConfigDict(env_file=".env")').replace('# TODO: construct Settings().','settings = Settings()')
  # Fixture inputs are displayed as comments; no construction results are authored.
  cases=json.loads(file(c,'source_cases.json'))
  code+='\n# Source cases (external inputs):\n'+''.join('# '+json.dumps(case)+'\n' for case in cases)
 elif c=='integration.async_http_requests':
  code=code.replace('    # TODO: one owning AsyncClient scope, both awaited calls, then cleanup.\n    pass','    async with httpx.AsyncClient() as client:\n        for url in lookup_urls:\n            await client.get(url)\n    # Scope exit closes the client.')
  code+='\n# Repeated calls with a separate client for each iteration:\nasync def separate_clients():\n    for url in lookup_urls:\n        async with httpx.AsyncClient() as client:\n            await client.get(url)\n'
 elif c=='pydantic.domain_validation':
  code=code.replace('    # TODO: add an after-model invariant validator.',"    @model_validator(mode='after')\n    def validate_booking(self):\n        if self.end <= self.start:\n            raise ValueError('end must be later than start')\n        return self")
  code+='\n# checks.py\n'+file(c,'checks.py').replace('from main import Booking\n','')
 elif c=='fastapi.expected_http_errors':
  f=next(f for f in B[c]['coverage']['required_facts'] if f['id']=='f1')
  status=re.search(r'\b404\b',B[c]['visual_anchor']['purpose']).group()
  code=code.replace('        # TODO: raise the intended expected rejection here.\n        pass','        raise HTTPException(status_code='+status+', detail="Order not found")')
 elif c=='fastapi.modular_application':
  local=re.search(r'GET (/[\w/]+)',file(c,'orders.py')).group(1)
  prefix=re.search(r'with (/[\w/]+) prefix',code).group(1)
  code='# orders.py\n'+file(c,'orders.py').replace('# TODO: construct feature router and register GET '+local+'.','router = APIRouter()\n@router.get('+repr(local)+')')+'\n# main.py\n'+code.replace('# TODO: import feature router and include with '+prefix+' prefix.','from orders import router\napp.include_router(router, prefix='+repr(prefix)+')')
 elif c=='fastapi.path_query_binding':
  default=next(row[1] for row in A['ds.order_state']['rows'])
  code=code.replace('def read_order():  # TODO: typed order_id and defaulted limit inputs.','def read_order(order_id: int, limit: int = '+str(default)+'):')
 elif c=='fastapi.response_model_serialization':
  cols=[x['name'] for x in A['ds.internal_orders']['columns'] if x['name']!='private_processing_note']
  model='class PublicOrder(BaseModel):\n'+''.join('    '+name+': '+('int' if next(x for x in A['ds.internal_orders']['columns'] if x['name']==name)['type']=='integer' else 'str')+'\n' for name in cols)
  code=code.replace('# TODO: PublicOrder with the two public fields only.',model).replace(')  # TODO: configure response_model.',', response_model=PublicOrder)')
 elif c=='fastapi_backend.depends':
  code=code.replace('def orders():  # TODO: declare context through Annotated and Depends.','def orders(context: Annotated[str, Depends(provider)]):').replace('return {}  # TODO: return supplied context, without calling provider here.','return {"context": context}')
 elif c=='fastapi.production_asgi_serving':
  code=re.search(r'uvicorn main:app --host [\d.]+ --port \d+',B[c]['teaching_blocks'][1]['content']).group()
 return {'type':'code_walkthrough','language':'bash' if c=='fastapi.production_asgi_serving' else 'python','code':code,'annotations':[{'start_line':1,'end_line':len(code.splitlines()),'text':walk[c]}],'reveal':'all','lineage':lin}
# Explicit labelled diagrams show boundaries and direction, without typed execution outputs.
flows={
'rest.resource_contract_design':(['Collection /orders','Item /orders/{order_id}','Created item /orders/42'],[(0,1,'GET retrieves; PUT replaces; DELETE removes'),(0,2,'POST collection creation: can use 201 + Location'),(1,1,'Absent item: can use 404')]),
'fastapi.handler_execution_choice':(['Awaitable I/O library','async def handler + await','Blocking I/O library','def path operation: external thread pool','async def → directly called blocking utility'],[(0,1,'awaitable execution'),(2,3,'choose normal def handler'),(2,4,'not automatically offloaded; can block event loop')]),
'integration.outbound_timeouts':(['Connect wait: ConnectTimeout','Pool wait: PoolTimeout','Read chunk wait: ReadTimeout','Write chunk wait: WriteTimeout','Total asynchronous elapsed budget: asyncio.timeout','TimeoutError outside context'],[(0,4,'distinct wait and total boundaries'),(2,2,'successive chunks: each wait can fit; total can exceed read limit'),(4,5,'cancellation converted outside context')]),
'design.backend_separation_of_concerns':(['HTTP adaptation: handler','Business rule: plain callable','Stored state: persistence adapter','Reusable input provisioning: dependency'],[(3,0,'declared handler parameter'),(0,1,'explicit decision inputs'),(0,2,'stored-state access; not embedded in handler')]),
'fastapi.bounded_background_tasks':(['Handler registers add_task','Response sent','Follow-up task: def or async def','Application process boundary','Process failure after response'],[(0,1,'register callable and arguments'),(1,2,'task runs after response'),(3,2,'in-process work'),(4,2,'pending work can be lost; no guaranteed survival or delivery')]),
'fastapi.dependency_composition':(['Typed page and page_size query inputs','Pagination provider','Order-options provider','Consuming operation'],[(0,1,'extract and convert request inputs'),(1,2,'resolve prerequisite and supply its result'),(2,3,'supply provider result')]),
'fastapi.existing_middleware_stack':(['B: added second; outermost','A: added first; inside B','Handler: inside A'],[(0,1,'request inward'),(1,2,'request inward'),(2,1,'response outward'),(1,0,'response outward')])}
def diagram(c,lin):
 labels,edges=flows[c]
 return {'type':'diagram','diagram_kind':'layers' if c=='fastapi.existing_middleware_stack' else 'sequence','nodes':[{'id':'n'+str(i),'label':v} for i,v in enumerate(labels)],'edges':[{'from':'n'+str(a),'to':'n'+str(b),'label':l,'directed':True} for a,b,l in edges],'alt_text':B[c]['visual_anchor']['purpose'],'lineage':lin}
# Keep each prose block to one small teaching unit; split long text at sentence boundaries.
def split_prose(text,lin,role):
 sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z])',text); parts=[]; current=''
 for s in sentences:
  if current and len((current+' '+s).split())>85:parts.append(prose(current,lin,role));current=''
  current=(current+' '+s).strip()
 if current:parts.append(prose(current,lin,role))
 return parts
out={k:plan[k] for k in ['schema_version','path_id','batch_id']};out['kind']='screens_part';out['tiles']=[]
for t in plan['tiles']:
 tile={'tile_id':t['tile_id'],'title':' · '.join(g['names'][c] for c in t['concept_ids']),'steps':[],'remediation_steps':[]}
 for s in t['steps']:
  cs=s['concept_ids'];c=cs[0];lin=lineage(cs,s['teaching_block_ids'],s['fact_ids'],s['anchors'])
  st={'step_id':s['step_id'],'type':s['type'],'concept_ids':cs,'title':g['names'][c],'lineage':lin}
  if s['type']=='explainer':
   tbs=[next(tb for tb in B[c]['teaching_blocks'] if c+'#'+tb['id']==q) for q in s['teaching_block_ids']]
   if any(tb['id']=='tb2' for tb in tbs):
    # Glossary rules preserve all hedges; introduce them directly rather than copying narrative lead-ins.
    st['title']='The rule: '+g['names'][c]
    st['blocks']=[]
    for tb in tbs:
     if tb['id']=='tb1':continue
     if tb['id'] in ('tb2','tb3'):
      text=tb['content'].replace('Use ','Choose ',1) if tb['content'].startswith('Use ') else tb['content']
      tl=lineage(cs,[c+'#'+tb['id']],[c+'#'+f for f in tb['fact_ids']])
      st['blocks']+=split_prose(text,tl,tb['purpose'])
    if any(tb['id']=='tb4' for tb in tbs):st['blocks']+=split_prose(walk[c],lineage(cs,[c+'#tb4'],[c+'#'+f for f in next(tb for tb in tbs if tb['id']=='tb4')['fact_ids']]),'walkthrough')
   else:
    st['title']='Trace the boundary: '+g['names'][c]
    st['blocks']=split_prose(walk[c],lin,'walkthrough')
   if s['planned_visual_block_type']:
    vl=copy.deepcopy(lin);vl['anchors']=[c+'#visual']
    st['blocks'].append(code_visual(c,vl) if s['planned_visual_block_type']=='code_walkthrough' else diagram(c,vl))
  elif s['type']=='video':st['blocks']=[{'type':'media_group','segment_ids':s['segment_ids']}]
  elif s['type'] in ('check','hands_on'):
   st['eyebrow']='Check your understanding' if s['type']=='check' else 'Apply the contract'
   st['title']=('Choose the distinction: ' if s['type']=='check' else 'Practice: ')+g['names'][c]
   # Interaction content and execution claims belong to later stages, not these frames.
   st['lede']='Use the declared contract to distinguish the outcomes.' if s['type']=='check' else 'Work in the supplied orders-service exercise snapshot.'
   # Every distinct measured fact set gets a separate repair route.
   rlin=lineage(cs,[c+'#'+tb['id'] for tb in B[c]['teaching_blocks'] if set(tb['fact_ids']) & {q.split('#')[1] for q in s['fact_ids']}],s['fact_ids'])
   text=' '.join(f['statement'] for f in B[c]['coverage']['required_facts'] if c+'#'+f['id'] in s['fact_ids'])
   contrast=' '.join(contrasts[c][q.split('#')[1]] for q in s['fact_ids'])
   r={'step_id':t['tile_id']+'.r'+str(len(tile['remediation_steps'])+1).zfill(2),'type':'remediation','concept_ids':cs,'title':'Try the contrast again: '+g['names'][c],'lineage':rlin,'blocks':split_prose(text,rlin,'definition')}
   # Reuse the same worked scenario; its contrasting cases are the learner's repair cue.
   r['blocks']+=split_prose(contrast,rlin,'example')
   tile['remediation_steps'].append(r)
  elif s['type']=='recap':
   st['title']='Keep these boundaries'
   st['blocks']=[]
   for cc in cs:
    tb=next((tb for tb in reversed(B[cc]['teaching_blocks']) if tb['purpose']=='misconception'),B[cc]['teaching_blocks'][-1])
    tl=lineage([cc],[cc+'#'+tb['id']],[cc+'#'+f for f in tb['fact_ids']])
    st['blocks']+=split_prose(tb['content'],tl,'takeaway')
   nxt=next((tt['concept_ids'][0] for tt in plan['tiles'] if tt['tile_id']==t['next_tile_id']),None)
   if nxt is None:
    # The bundle's name order follows the frozen path concept order.
    keys=list(g['names']);nxt=keys[keys.index(cs[-1])+1]
   st['blocks'].append({'type':'up_next','title':g['names'][nxt],'text':'Next: '+g['names'][nxt]+'.'})
  tile['steps'].append(st)
 out['tiles'].append(tile)
(P/'screens.json').write_text(json.dumps(out,indent=2)+'\n')
print('tiles',len(out['tiles']),'steps',sum(len(t['steps']) for t in out['tiles']),'remediation',sum(len(t['remediation_steps']) for t in out['tiles']))
