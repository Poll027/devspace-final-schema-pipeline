import json
from pathlib import Path
from collections import Counter
B=Path(__file__).parent;x=json.loads((B/'interactions.json').read_text());p=json.loads((B/'tile_plans.json').read_text());s=json.loads((B/'screens.json').read_text());g={b['context']['concept_id']:b for b in json.loads((B/'inputs/path_glossary_bundle.json').read_text())['bundles']}
hints={
'rest.resource_contract_design':'Separate resource identity, operation semantics and response metadata.',
'fastapi.path_operations':'Compare the HTTP method as well as the path; for overlapping GET paths, inspect declaration order.',
'fastapi.validated_environment_configuration':'Check source precedence separately from whether a required field has a usable value.',
'integration.async_http_requests':'Trace the client’s owning scope from construction through its last use and cleanup.',
'pydantic.domain_validation':'Ask whether a failure belongs to one field or to the relationship between validated fields.',
'fastapi.expected_http_errors':'Distinguish constructing an exception, raising it, and returning a normal value.',
'fastapi.handler_execution_choice':'Inspect what the library call actually does, not just the handler’s spelling.',
'fastapi.modular_application':'Trace feature registration separately from inclusion in the application.',
'fastapi.path_query_binding':'Compare placeholder names, annotations and defaults independently.',
'fastapi.response_model_serialization':'Compare the declared public fields with the internal dictionary and the return path.',
'fastapi_backend.depends':'Look at whether the handler declares a provider-supplied input or fetches a value itself.',
'integration.outbound_timeouts':'Identify which wait exceeded its limit and which exception the excerpt handles.',
'design.backend_separation_of_concerns':'Locate HTTP adaptation, the decision rule and stored-state access separately.',
'fastapi.bounded_background_tasks':'Distinguish registering a callable from invoking it; consider the process-failure boundary.',
'fastapi.dependency_composition':'Draw each provider-to-consumer dependency before tracing request inputs.',
'fastapi.existing_middleware_stack':'Trace nested wrappers inward for the request and outward for the response.',
'fastapi.production_asgi_serving':'Check the import string and startup evidence separately from development-only options.'}
for t in x['tiles']:
 for e in t['interactions']:
  i=e['interaction'];cid=i['anchors'][0].split('#')[0];i['feedback']['hints']=[hints[cid]]
  if e['step_id']=='tile_030.s13':
   for f in [i['public']['workspace']['files'][0],i['grading']['solution_files'][0]]:
    f['content']=f['content'].replace('def read_order(order_id: int):','def read_order(order_id: int) -> dict:')
   i['public']['prompt']+=' Keep the supplied -> dict return annotation; the explicit response_model takes priority over it.'
  if e['step_id']=='tile_029.s05':
   bridge='''
# Supplied single-file feature-module loader, used only because the runner executes one entry.
import sys, types
feature_module = types.ModuleType("orders")
feature_module.router = router
sys.modules["orders"] = feature_module
from orders import router
'''
   for f in [i['public']['workspace']['files'][0],i['grading']['solution_files'][0]]:
    if 'app.include_router' in f['content']:f['content']=f['content'].replace('app.include_router',bridge+'app.include_router')
    else:f['content']=f['content'].replace('# TODO: register on router, then include it with /api.',bridge+'# TODO: register on router, then include it with /api.')
   i['public']['prompt']+=' The supplied module loader publishes the completed feature router as orders.router; retain the actual from orders import router import in the application section.'
(B/'interactions.json').write_text(json.dumps(x,indent=2)+'\n')
# Mechanical portion of the mistakes-to-avoid review.
counts=Counter();checks=[]
for pt in p['tiles']:
 it=next(t for t in x['tiles'] if t['tile_id']==pt['tile_id']);st=next(t for t in s['tiles'] if t['tile_id']==pt['tile_id']);planned={a['step_id']:a for a in pt['steps'] if a['type'] in ['check','hands_on']}
 assert set(planned)=={a['step_id'] for a in it['interactions']}
 for e in it['interactions']:
  i=e['interaction'];plan=planned[e['step_id']];cid=plan['concept_ids'][0];counts[i['type']]+=1
  assert i['type']==plan['planned_interaction_type']
  assert i['grading_mode']=='client'
  for m in i['measures']:
   assert all('#' not in f for f in m['fact_ids'])
   assert any(a['capability']==m['capability'] and a['fact_ids']==m['fact_ids'] for a in g[m['concept_id']]['assessment_anchors'])
  target=i['feedback'].get('remediation_step_id')
  if target:assert any(r['step_id']==target for r in st.get('remediation_steps',[]))
  assert 1<=len(i['feedback']['hints'])<=2
  if plan['type']=='hands_on':assert cid+'#practice' in i['anchors']
  if i['type']=='choice':
   assert len(i['grading']['correct_option_ids'])==1
   assert set(i['grading']['option_feedback'])=={a['option_id'] for a in i['public']['options']}
   assert 'the table above' not in i['public']['prompt'].lower()
  if i['type']=='code_exercise':
   assert 'execution_provenance' not in i['grading'] and 'hidden_checks' not in i['grading']
   for k in ['allowed_syntax','blocked_syntax']:assert i['public']['constraints'][k]==g[cid]['practice_anchor']['live_code'][k]
   assert i['public']['workspace']['files'][0]['content']!=i['grading']['solution_files'][0]['content']
  checks.append(e['step_id'])
review={'tiles':len(x['tiles']),'counts':dict(counts),'mechanically_reviewed_steps':checks,'manual_review':['Choice prompts are self-contained, with one answer and a grounded explanation for every distractor.','Inspect-and-judge excerpts include trap items and distinguish authored fixture evidence from native execution.','Expected code results were derived by executing the submitted solutions, never entered from memory.','The strict gate checks taught-before-tested, runtime results, starter failure and anti-hard-coding.','The contract exercise copies supplied literal values because the glossary’s descriptive syntax strings have no literal detector; constraints remain verbatim.'],'limitations':['Settings uses genuine Pydantic v1 BaseSettings with a supplied dotenv-source adapter because pydantic-settings and python-dotenv are unavailable; this does not verify SettingsConfigDict or actual dotenv parsing.','Native FastAPI thread-pool placement is not measured by Pyodide, which runs sync endpoints inline.','Serving and outbound timeout practices are authored inspect-and-judge fixtures, not native process/network execution.']}
(B/'interactions_checklist.json').write_text(json.dumps(review,indent=2)+'\n')
print(review['counts'])
