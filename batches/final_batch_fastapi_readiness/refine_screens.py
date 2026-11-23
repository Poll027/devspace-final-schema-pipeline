import json,re,copy
from pathlib import Path
P=Path('batches/final_batch_readiness');S=json.loads((P/'screens.json').read_text());R=json.loads((P/'scenario_asset_registry.json').read_text());G=json.loads((P/'inputs/path_glossary_bundle.json').read_text())
A={a['asset_id']:a for a in R['assets']};B={b['context']['concept_id']:b for b in G['bundles']}
def source(c,path):return next(f['content'] for f in A['ws.'+c]['files'] if f['path']==path)
def fixture(c):return json.loads(source(c,'fixtures.json'))
def visual(c):return next(b for t in S['tiles'] for s in t['steps'] if s['concept_ids'][0]==c for b in s.get('blocks',[]) if b['type']!='prose')
def walk(b):
 yield b
 for k in ['left','right','before','after']:
  if k in b:yield from walk(b[k])
c='fastapi.documented_responses';v=visual(c);f=fixture(c);src=source(c,'starter.py')
# Statuses and source routes are supplied by the registry, not invented.
route=re.search(r"@app.post\('([^']+)'\)",src).group(1)
metadata='@app.post('+repr(route)+', response_model=PublicModel, status_code='+repr(f['success_status'])+', response_description="Created order", responses={'+repr(f['conflict_status'])+': {"model": ConflictModel, "description": "Order conflict"}})'
v['left']['code']=src.replace("@app.post("+repr(route)+")",metadata).replace('# TODO: complete only response documentation, preserving the outcome implementation.','# Response declarations do not replace implementation.')
v['right']['code']='# Inspect generated declarations and exercise the real HTTP cases.\nfixtures = '+repr(f)+'\nwith TestClient(app) as client:\n    success = client.post('+repr(route)+')\n    conflict = client.post('+repr(route+'?conflict=true')+')\n    assert success.status_code == fixtures["success_status"]\n    assert success.json() == fixtures["success_body"]\n    assert conflict.status_code == fixtures["conflict_status"]\n    assert conflict.json() == fixtures["conflict_body"]\nresponse_entries = app.openapi()["paths"]['+repr(route)+']["post"]["responses"]\n# Compare each entry’s schema and descriptions with the exercised bodies.\n'
c='observability.evidence_based_service_diagnosis';v=visual(c)
v['left'].pop('asset_ref');v['left']['result_of']={'runtime':'sql','sql':'SELECT operation, "window", request_count * 1.0 / window_seconds AS request_rate_per_second, failure_count * 1.0 / request_count AS failure_fraction, latency_ms FROM signals','asset_mounts':[{'asset_id':'ds.operation_signals','mount_path':'signals'}]}
v['right'].pop('asset_ref');v['right']['result_of']={'runtime':'sql','sql':'SELECT * FROM records ORDER BY interaction_id, offset_ms','asset_mounts':[{'asset_id':'ds.correlated_records','mount_path':'records'}]}
c='security.bounded_api_resources';v=visual(c);f=fixture(c)
app=source(c,'application.py').replace('httpx.Timeout(None)  # TODO: supplied finite timeout','httpx.Timeout(budgets["dependency_timeout_seconds"])').replace('app = FastAPI()','app = FastAPI()\napp.add_middleware(RequestBodyLimitMiddleware, max_body_size=budgets["body_bytes"])')
app=app[:app.index('# TODO: immediately after app construction')]
model='from pydantic import BaseModel, Field\nfrom pathlib import Path\nimport json\nbudgets = json.loads(Path("fixtures.json").read_text())["hypothetical_budgets"]\nclass BatchInput(BaseModel):\n    order_ids: list[int] = Field(max_length=budgets["batch_size"])\n'
launch=source(c,'launch.sh').split('exec ',1)[1].strip()+' --limit-concurrency '+str(f['hypothetical_budgets']['limit_concurrency'])
v['code']='# starter.py: supplied finite batch bound\n'+model+'\n# application.py: enforce actual bytes and finite dependency wait\n'+app+'\n# Supplied launch policy\n# '+launch+'\n\n'+source(c,'test_boundaries.py')
v['annotations']=[{'start_line':1,'end_line':7,'text':'Batch count is not body size. Test byte and batch limits independently, and check rejection before costly dependency invocation.'}]
c='fastapi.openapi_contract_inspection';v=visual(c)
# Actual source declarations, not fabricated generated schema or HTTP output.
app=source(c,'application.py');decl=app[:app.index('security_configuration=')]
v['left']['code']=decl+'\n# Retrieve /openapi.json and compare with source models, HTTP evidence and deployed security configuration.\n'
lines=decl.splitlines();conflict_line=next(i+1 for i,l in enumerate(lines) if 'raise HTTPException(400' in l)
v['left']['annotations']=[{'start_line':conflict_line,'end_line':conflict_line,'text':'The supplied source marks conflict-status drift here. Compare this emitted status with the additional response declaration and exercised HTTP evidence.'}]
# Remediation contrasts remain in the identical fixture scenario, without importing future concepts.
context={
'fastapi.documented_responses':lambda f:'In the supplied order contract, success is '+str(f['success_status'])+' and conflict is '+str(f['conflict_status'])+'. Compare both bodies with their public models; declaring the conflict does not implement it.',
'fastapi.safe_unexpected_errors':lambda f:'The supplied public contract is '+str(f['public_status'])+' with '+json.dumps(f['public_body'])+'. Keep the diagnostic event, code location and interaction context in the separate internal record.',
'integration.upstream_failure_translation':lambda f:'Under this fixture’s local mapping, the supplied upstream status failure maps to '+str(f['upstream_503']['status'])+' and timeout maps to '+str(f['timeout']['status'])+'. These are declared local outcomes, not automatic forwarding.',
'security.bounded_api_resources':lambda f:'This fictional budget uses '+str(f['hypothetical_budgets']['body_bytes'])+' body bytes and '+str(f['hypothetical_budgets']['batch_size'])+' batch items. A passing batch-size check does not establish the independent body-byte boundary.',
'auth.endpoint_permissions':lambda f:'The supplied operation requires '+', '.join(f['operation_scopes'])+'. Compare the verified context with those scopes: the supplied no-permission context is still distinct from failed authentication.',
'auth.authorization_server_integration':lambda f:'Use the supplied registered client '+f['client_id']+' and API audience '+f['audience']+'. Obtain the issuer-issued access token through the client, then exercise the protected HTTP endpoint with real verification.',
'integration.bounded_idempotent_retries':lambda f:'The supplied policy bounds attempts at '+str(f['hypothetical_limits']['max_attempts'])+' and total time at '+str(f['hypothetical_limits']['total_time_budget_seconds'])+' seconds. The fixture contrasts '+f['operations'][0]['method']+' with '+f['operations'][1]['method']+' lacking a retry-safe contract.',
'fastapi.production_security_documentation':lambda f:'The supplied operation permissions are '+', '.join(x['scope'] for x in f['operation_requirements'].values())+'. Match their real dependencies to generated security entries, without adding a password grant.',
'fastapi.openapi_contract_inspection':lambda f:'Audit the supplied '+f['router']+' router. Its synthetic example is '+json.dumps(f['synthetic_example'])+'; validate public examples against models and compare declarations with exercised HTTP behavior.',
}
for t in S['tiles']:
 for r in t['remediation_steps']:
  c=r['concept_ids'][0]
  if c in context:
   # Replace generic final contrast with fixture-specific contrast, preserving its lineage.
   r['blocks'][-1]['text']=context[c](fixture(c))
  elif c=='integration.webhook_authenticity':
   r['blocks'][-1]['text']='For the supplied signed delivery, compare unchanged raw bytes with the modified-body case and the absent-signature case. Only verified input reaches process_event; parsing a modified body successfully does not make its signature valid.'
  elif c=='testing.database_state_isolation':
   f=fixture(c);r['blocks'][-1]['text']='Write/read the supplied item '+json.dumps(f['item'])+' through the isolated test boundary. Then test its absence in a fresh test. Run both supplied execution orders; a successful first write does not prove the next test starts clean.'
 # Every code walkthrough contains source only; never authored execution output.
 for st in t['steps']+t['remediation_steps']:
  for block in st.get('blocks',[]):
   for b in walk(block):
    if b['type']=='code_walkthrough':assert 'output' not in b
(P/'screens.json').write_text(json.dumps(S,indent=2,ensure_ascii=False)+'\n')
