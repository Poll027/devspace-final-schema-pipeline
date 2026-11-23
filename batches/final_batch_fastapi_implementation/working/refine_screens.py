import json,copy,re
from pathlib import Path
B=Path('batches/final_batch_implementation'); S=json.loads((B/'screens.json').read_text());G=json.loads((B/'inputs/path_glossary_bundle.json').read_text());bs={b['context']['concept_id']:b for b in G['bundles']}
# Each prose block identifies only the facts it actually teaches.
paragraph_facts={
'022.s01':[[1,2],[3],[4]],'022.s02':[[1,2,3],[1,4]],'022.s05':[[1,2],[3]],'022.s06':[[3],[2]],'022.s07':[[1,2],[3]],
'024.s01':[[1,2],[3]],'024.s02':[[2],[2,3]],'024.s03':[[1,2,3],[2,3]],
'025.s01':[[1],[2,3]],'025.s02':[[2],[1,3]],'025.s03':[[1,2],[3]],
'026.s01':[[1,2],[3],[4]],'026.s02':[[1,2,4],[3,4]],'026.s07':[[1],[2,3],[1,2,3]],'026.s08':[[1],[2,3]],
'028.s01':[[1,2],[2,3]],'028.s02':[[1,2],[3]],
'029.s01':[[1,2],[3]],'029.s02':[[2,3],[1,2]],
'030.s01':[[1,2],[3],[4]],'030.s02':[[1,2,3],[1,4]],'030.s03':[[1,2,3],[1,2,4]],'030.s08':[[1,2],[3,4]],'030.s09':[[1,2],[4]],'030.s10':[[1,2],[3,4]],
'032.s01':[[1,2],[3]],'032.s02':[[1,2],[2,3]],'032.s03':[[1,2],[3]],
'033.s01':[[1,2],[3],[4]],'033.s02':[[1,2],[1,3,4]],
'034.s01':[[1],[2],[3]],'034.s02':[[1,2,3],[2,3]],'034.s05':[[1],[2,3]],'034.s06':[[1,2],[3]],'034.s10':[[1,2],[3]],'034.s11':[[1,2,3],[2]],
'037.s01':[[2],[1,3]],'037.s02':[[1,3],[1,2]],'037.s05':[[1],[2],[3]]}
def lineage(c,ids):
 fs=[c+'#f'+str(i) for i in ids]
 tbs=[c+'#'+b['id'] for b in bs[c]['teaching_blocks'] if set(b['fact_ids']) & set('f'+str(i) for i in ids)]
 return {'concept_ids':[c],'fact_ids':fs,'teaching_block_ids':tbs}
# Short authored contrasts stay within the same scenario and the measured fact's boundary.
contrasts={
'rest.resource_contract_design':{1:'For the same order path, GET and PUT request different operations; the URL alone does not choose one.',2:'The orders collection has no item identifier; an item resource includes its identifier.',3:'On the item, PUT means replacement, not retrieval; GET means retrieval.',4:'The creation contract can use 201 with a Location; an absent-item contract can use 404 instead.'},
'fastapi.path_operations':{1:'A handler definition is not the registration: its method-and-path decorator binds the operation.',2:'GET and PUT on the order item share path text, not operation identity.',3:'The fixed current-order route must precede a conflicting parameterized route; declaring it later does not make it win.'},
'fastapi.validated_environment_configuration':{1:'Declaring a typed required setting differs from treating an external string as unchecked input.',2:'Constructing settings with a missing required value fails validation; it is not a valid empty configuration.',3:'A configured dotenv value does not override a conflicting environment value.'},
'integration.async_http_requests':{1:'Await the shipping request method; merely constructing the client does not perform the request.',2:'Reuse one client across the shipping lookups, rather than constructing a new one for every repeated call.',3:'A completed shipping request is not client cleanup; close the client when its owning scope ends.'},
'pydantic.domain_validation':{1:'The booking relationship needs an after-model instance method; it is not just a check on one field.',2:'On invariant failure, raise ValueError; on success, return self rather than dropping the model result.',3:'The booking model validator returns self, while a single-field after-validator returns the accepted field value.',4:'Choose individually valid booking fields with an inconsistent relationship, not a value that already fails its field type.'},
'fastapi.expected_http_errors':{1:'Raise the expected order rejection to stop normal work; returning the exception object is different.',2:'Required rejection metadata belongs in the exception headers, not solely in the detail value.',3:'The default rejection body uses detail as its key, not an invented alternative key.'},
'fastapi.handler_execution_choice':{1:'The supplied shipping library blocks; choose a normal def handler rather than assuming async def changes the library.',2:'A normal def path operation uses FastAPI’s external thread pool; an async def path operation uses asynchronous execution.',3:'Calling a blocking shipping utility directly inside async def does not automatically offload it to the thread pool.'},
'fastapi.modular_application':{1:'Register the orders feature on its router; defining every operation in the main module is not required.',2:'Defining the orders router does not include it; the application must call include_router.',3:'The local orders path and the inclusion-prefixed application path differ; follow the include point.'},
'fastapi.path_query_binding':{1:'The order identifier binds from the path only when its name appears in the placeholder and handler declaration.',2:'The scalar limit outside the order path binds from the query, not from a path placeholder.',3:'A defaulted query limit permits omission; the same declaration without a default requires it.',4:'An unconvertible order identifier produces a validation error, not a handler call with the original string.'},
'fastapi.response_model_serialization':{1:'Ordinary response-model processing filters the internal order to the declared public model, not every internal field.',2:'Leave the private processing note out of PublicOrder; its presence internally does not make it a public field.',3:'For response processing, response_model takes priority over a simultaneous return annotation.',4:'An ordinary dictionary return uses automatic model processing; a direct Response bypasses its conversion and filtering.'},
'fastapi_backend.depends':{1:'The provider supplies the handler’s declared context; the handler need not perform a hidden global lookup.',2:'Depends takes provider, the callable, not provider(), its already-called result.',3:'Several order operations can declare the same input supplier; shared provisioning need not be hidden in globals.'},
'integration.outbound_timeouts':{1:'A shipping read limit bounds each chunk wait, not the whole lookup’s elapsed duration.',2:'A finite shipping timeout enables enforcement; timeout=None disables it.',3:'Identify whether the exceeded wait is connect, read, write or pool; each has its corresponding HTTPX exception.',4:'The total-budget TimeoutError is raised outside asyncio.timeout, rather than being an HTTPX per-wait exception.'},
'design.backend_separation_of_concerns':{1:'Declare reusable order inputs through a provider, rather than burying their provisioning inside each handler.',2:'HTTP adaptation, the order decision and stored-state access are different responsibilities, not just different filenames.',3:'Move the decision to a plain callable with explicit inputs and storage access to an adapter; relocating the same mixture is not separation.'},
'fastapi.bounded_background_tasks':{1:'Register follow-up work with add_task; it runs after response sending, not before it.',2:'The follow-up callable can be def or async def; either form fits this scheduling mechanism.',3:'Sending the order response is not durable follow-up completion: process failure can lose pending work.'},
'fastapi.dependency_composition':{1:'Order-options can declare its own pagination dependency; the handler is not the only place dependencies can be declared.',2:'Resolve pagination before calling order-options, not afterward.',3:'Extract the pagination provider’s typed query inputs before supplying its result to order-options.'},
'fastapi.existing_middleware_stack':{1:'The last addition is outermost: it sees requests first but responses last.',2:'Configure the supplied maintained components with documented add_middleware options rather than writing their protocols.',3:'After adding A then B, requests go B then A; responses go A then B.'},
'fastapi.production_asgi_serving':{1:'The import string identifies a module and its application object, not just a filename.',2:'Use reload for development, not production serving.',3:'Workers are separate processes; reload is not their substitute and cannot be combined with --workers.'}}
for t in S['tiles']:
 for s in t['steps']:
  if s['type']=='explainer':
   c=s['concept_ids'][0];ps=[b for b in s['blocks'] if b['type']=='prose']
   spec=paragraph_facts[s['step_id'].removeprefix('tile_')];assert len(ps)==len(spec)
   allowed=set(s['lineage']['teaching_block_ids'])
   for b,ids in zip(ps,spec):
    l=lineage(c,ids);l['teaching_block_ids']=[x for x in l['teaching_block_ids'] if x in allowed];b['lineage']=l
  elif s['type']=='recap':
   for b in s['blocks']:
    if b['type']=='prose':
     c=b['lineage']['concept_ids'][0]
     # Summary mental models are takeaways rather than assertions that every fact was restated.
     b['lineage']['fact_ids']=[c+'#'+bs[c]['coverage']['required_facts'][0]['id']]
 for s in t['remediation_steps']:
  c=s['concept_ids'][0];fs=s['lineage']['fact_ids'];f=int(fs[-1].split('#f')[1])
  s['lede']='Use the same orders-service exercise to separate these cases.'
  s['blocks'][-1]={'type':'prose','role':'misconception','text':contrasts[c][f],'lineage':lineage(c,[f])}
# Tighten code annotations without adding computed output.
for t in S['tiles']:
 for s in t['steps']:
  for b in s.get('blocks',[]):
   if b['type']=='code_walkthrough' and s['concept_ids']==['fastapi.expected_http_errors']:
    b['annotations'][0]['text']='Absent-order rejection: status 404; normal work stops here. FastAPI places the supplied value under the default JSON key detail.'
(B/'screens.json').write_text(json.dumps(S,indent=2,ensure_ascii=False)+'\n')
