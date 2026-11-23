import json, pathlib, subprocess, sys, os, hashlib, copy
P=pathlib.Path('batches/final_batch_readiness').resolve(); W=P/'working/screens_repair'
s=json.loads((P/'screens.json').read_text()); original=copy.deepcopy(s)
r=json.loads((P/'scenario_asset_registry.json').read_text())
assets={a['asset_id']:a for a in r['assets']}
for directory in W.iterdir():
 if directory.is_dir() and 'ws.'+directory.name in assets:
  for f in assets['ws.'+directory.name]['files']:
   if 'glossary' not in f['path']:
    dst=directory/f['path'];dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(f['content'])
steps={st['step_id']:st for t in s['tiles'] for st in t['steps']}
env=os.environ.copy();env['PYTHONPATH']=str(P/'working/repair_runtime')+os.pathsep+str(P/'working/offline_runtime')
def run(c, code, filename='capture_repair.py'):
 d=W/c; (d/filename).write_text(code)
 p=subprocess.run([sys.executable,filename],cwd=d,env=env,text=True,capture_output=True)
 (d/(filename+'.stdout')).write_text(p.stdout);(d/(filename+'.stderr')).write_text(p.stderr)
 if p.returncode: raise RuntimeError(c+'\n'+p.stdout+'\n'+p.stderr)
 return p.stdout

def panel(code, output, lineage, language='python'):
 return dict(type='code_walkthrough',language=language,code=code,annotations=[],reveal='all',output={'kind':'text','text':output},execution_provenance={'runtime':'python','runtime_version':sys.version.split()[0],'code_sha256':hashlib.sha256(code.encode()).hexdigest(),'output_sha256':hashlib.sha256(output.encode()).hexdigest()},lineage=copy.deepcopy(lineage))
def pair(l,r,ll,rl,caption,lineage):
 return dict(type='side_by_side',left=l,right=r,left_label=ll,right_label=rl,takeaway=caption,lineage=copy.deepcopy(lineage))
# Concrete advisory wording, with no new diagnosis or promised timeout.
b=steps['tile_085.s01']['blocks'][-1]; b['nodes'][0]['label']='Upstream HTTP 503'
b=steps['tile_087.s01']['blocks'][-1];b['takeaway']='Observed: outbound wait from 10 ms to timeout at 2010 ms; final local response at 2025 ms. Suspected boundary: outbound integration. Proposed change: only after controlled reproduction confirms this evidence.'
b=steps['tile_088.s01']['blocks'][-1]
next(n for n in b['nodes'] if n['id']=='n3')['label']='HTTPX dependency timeout configured to 2 seconds; Uvicorn --limit-concurrency configured to 8'
next(e for e in b['edges'] if e['from']=='n3')['label']='accepted work uses these configured limits'
b=steps['tile_093.s10']['blocks'][-1];next(n for n in b['nodes'] if n['id']=='n4')['label']='Attempts and total elapsed time still below the supplied limits?'
# 083: complete exactly the illustrated declarations, capture generated schema.
c='fastapi.documented_responses';d=W/c
code=(d/'starter.py').read_text().split('with TestClient(app)')[0]
code='import json\nfrom pathlib import Path\nfixtures=json.loads(Path("fixtures.json").read_text())\n'+code
illustrated=steps['tile_083.s01']['blocks'][-1]['left']['code']
code=code[:code.index('# TODO:')]+illustrated+'\n'
code+='schema=app.openapi()\nprint(json.dumps({"responses": {str(status):schema["paths"]["/orders"]["post"]["responses"][str(status)] for status in (fixtures["success_status"], fixtures["conflict_status"])}, "components": {"schemas": {name:schema["components"]["schemas"][name] for name in ("PublicModel","ConflictModel")}}}, indent=2))\n'
out=run(c,code)
old=steps['tile_083.s01']['blocks'][-1];steps['tile_083.s01']['blocks'].append(pair(panel(code,out,old['lineage']),copy.deepcopy(old['right']),'Generated response entries and schemas','Supplied HTTP outcomes','Generated response entries and schemas',old['lineage']))
# 088: configure completed application; execute boundary assertions without overrides.
c='security.bounded_api_resources';d=W/c
(d/'starter.py').write_text("from pydantic import BaseModel, Field\nimport json\nfrom pathlib import Path\nbudgets=json.loads(Path('fixtures.json').read_text())['hypothetical_budgets']\nclass BatchInput(BaseModel):\n    order_ids: list[int] = Field(max_length=budgets['batch_size'])\n")
application=(d/'application.py').read_text().replace('app = FastAPI()',"app = FastAPI()\napp.add_middleware(RequestBodyLimitMiddleware,max_body_size=budgets['body_bytes'])").replace('httpx.Timeout(None)  # TODO: supplied finite timeout',"httpx.Timeout(budgets['dependency_timeout_seconds'])")
application=application[:application.index('# TODO: immediately')];(d/'application.py').write_text(application)
code="""import json
from pathlib import Path
from fastapi.testclient import TestClient
import application
fixtures=json.loads(Path('fixtures.json').read_text())
with TestClient(application.app) as client:
    for condition in ('within_batch','within_body','beyond_body','beyond_batch'):
        before=application.expensive_calls
        if condition=='beyond_body':
            response=client.post('/orders/batch', content=fixtures[condition],
                                 headers={'Content-Type':'application/json'})
        else:
            response=client.post('/orders/batch', json=fixtures[condition])
        calls=application.expensive_calls-before
        if condition.startswith('within'):
            assert response.status_code==200
            assert response.json()=={'accepted':len(fixtures[condition]['order_ids'])}
            assert calls==1
        elif condition=='beyond_body':
            measured=json.loads(Path('middleware_verification.json').read_text())['records'][1]
            assert response.status_code==measured['status']
            assert response.text==measured['body_text']
            assert calls==0
        else:
            assert response.status_code==422
            assert all(error['type']=='too_long' for error in response.json()['detail'])
            assert calls==0
        print(json.dumps({'case':condition,'status':response.status_code,
                          'body':response.json() if response.headers['content-type'].startswith('application/json') else response.text,
                          'dependency_invocations':calls,'assertions':'passed'}))
"""
out=run(c,code)
old=steps['tile_088.s01']['blocks'][4] if False else next(b for b in steps['tile_088.s01']['blocks'] if b['type']=='code_walkthrough')
full=(d/'starter.py').read_text()+'\n'+application+'\n'+code
new=panel(full,out,old['lineage']); steps['tile_088.s01']['blocks'][steps['tile_088.s01']['blocks'].index(old)]=pair(new,{'type':'code_walkthrough','language':'bash','code':'uvicorn application:app --limit-concurrency '+str(json.loads((d/'fixtures.json').read_text())['hypothetical_budgets']['limit_concurrency']), 'annotations':[],'reveal':'all','lineage':copy.deepcopy(old['lineage'])},'Completed configuration and executed assertions','Configured Uvicorn launch','Accepted inputs preserve the response contract; excess bytes or batch items are rejected without invoking the expensive dependency.',old['lineage'])
# 089: execute both listings in fresh sessions and capture actual echo records.
c='sqlalchemy.redundant_queries'; d=W/c
base=(d/'starter.py').read_text(); baseline_code=base[base.index('def listing'):base.index('# Run baseline')]
revision=baseline_code.replace('# TODO: statement.options(selectinload(Entity.relationship_attribute))','statement = statement.options(selectinload(Entity.relationship_attribute))')
code="""import json, logging
from sqlalchemy.orm import Session
from starter import engine, Entity, select, selectinload, listing
"""+revision.replace('def listing(', 'def revised_listing(')+"""
class Capture(logging.Handler):
    def __init__(self):
        super().__init__(); self.messages=[]
    def emit(self,record):
        message=record.getMessage()
        if message.lstrip().startswith('SELECT'):
            self.messages.append(message)
handler=Capture()
logger=logging.getLogger('sqlalchemy.engine.Engine')
logger.addHandler(handler)
captures={}
for name,fn in [('before',listing),('after',revised_listing)]:
    handler.messages=[]
    with Session(engine) as session:
        result=fn(session)
    captures[name]={'sql':handler.messages.copy(),'returned':result}
logger.removeHandler(handler)
assert captures['before']['returned']==captures['after']['returned']
from pathlib import Path
Path('listing_capture.json').write_text(json.dumps(captures,indent=2))
"""
run(c,code);captures=json.loads((d/'listing_capture.json').read_text())
bs=steps['tile_089.s01']['blocks']; comps=[b for b in bs if b['type']=='side_by_side']; li=comps[1]['lineage']
comps[1]['right']=panel(code,'\n\n'.join(captures['after']['sql']),li);comps[1]['right_label']='Revised emitted SQL (fresh session, echo=True)';comps[1]['takeaway']='Before and after: repeated per-parent relationship SELECTs become batched collection retrieval; returned parent and collection data remain unchanged.'
comps[2]['left']=panel(baseline_code,json.dumps(captures['before']['returned'],indent=2),li)
comps[2]['right']=panel(revision,json.dumps(captures['after']['returned'],indent=2),li)
comps[2]['left_label']='Before: returned parent and collection data';comps[2]['right_label']='After: returned parent and collection data';comps[2]['takeaway']=comps[1]['takeaway']
# 090: execute the illustrated completed fixture with supplied tests in both orders.
c='testing.database_state_isolation';d=W/c
fixture=next(b for b in steps['tile_090.s01']['blocks'] if b['type']=='code_walkthrough')['code']
(d/'starter.py').write_text('import pytest\nfrom sqlalchemy.orm import Session\nfrom fastapi.testclient import TestClient\nfrom application import app, engine, session_provider\n'+fixture+'\n')
tests=(d/'test_items.py').read_text();start=tests.index('# Initially');end=tests.index('def test_writes_item');tests=tests[:start]+'from starter import isolated_client\n'+tests[end:];(d/'test_items.py').write_text(tests)
code="""import ast, json
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from application import app, engine, session_provider
# Execute the completed fixture generator body and the supplied test functions.
# No pytest runner is available in this offline runtime.
fixture_ast=ast.parse(Path('starter.py').read_text())
fixture_function=next(node for node in fixture_ast.body
                      if isinstance(node,ast.FunctionDef) and node.name=='isolated_client')
fixture_function.decorator_list=[]
exec(compile(ast.Module(body=[fixture_function],type_ignores=[]),'starter.py','exec'))
test_ast=ast.parse(Path('test_items.py').read_text())
exec(compile(ast.Module(body=[node for node in test_ast.body if isinstance(node,ast.FunctionDef)],
                        type_ignores=[]),'test_items.py','exec'))
fixtures=json.loads(Path('fixtures.json').read_text())
item=fixtures['item']
for order in fixtures['execution_orders']:
    print(' → '.join(order))
    for name in order:
        boundary=isolated_client()
        supplied=next(boundary)
        try:
            globals()['test_'+name](supplied)
        finally:
            try:
                next(boundary)
            except StopIteration:
                pass
        print('test_'+name+': PASS (all supplied assertions)')
    print('Execution order: PASS')
"""
out=run(c,code);b=next(b for b in steps['tile_090.s01']['blocks'] if b['type']=='side_by_side');b['right']=panel(code,out,b['lineage']);b['takeaway']='Both execution orders pass: writes_item → item_absent and item_absent → writes_item.'
# 093: computed companion to registered timestamp cases.
b=next(b for b in steps['tile_093.s05']['blocks'] if b['type']=='data_table')
rows=assets[b['asset_ref']['asset_id']]['rows']
code="""import json
from pathlib import Path
cases=json.loads(Path('fixtures.json').read_text())['cases']
for case in cases:
    difference=case['receiver_now']-int(case['signed_delivery_timestamp'])
    accepted=(-case['future_tolerance'] <= difference <= case['acceptance_window'])
    print(f"{case['case_id']}: {difference}/{'accept' if accepted else 'reject'}")
"""
c='fastapi_backend.webhook_replay_freshness';out=run(c,code)
steps['tile_093.s05']['blocks'][steps['tile_093.s05']['blocks'].index(b)]=pair(b,panel(code,out,b['lineage']),'Authenticated timestamps and configured limits','Signed differences and outcomes','Authenticated delivery freshness—not original event age.',b['lineage'])
# 096: derive supplied-contract combinations from fixture ownership, not typed rows.
c='auth.object_authorization';d=W/c;f=json.loads((d/'fixtures.json').read_text());orders={o['id']:o for o in f['orders']}
labels=[]
for owner,oid in f['pairs']:
 o=orders[oid]
 if o['owner_id']==owner: status=200;body={k:o[k] for k in ('id','status')}
 else: status=f['unavailable_object']['status'];body=f['unavailable_object']['body']
 labels.append(f"{owner}/{oid} → {status} "+json.dumps(body,separators=(',',':')))
b=next(b for b in steps['tile_096.s01']['blocks'] if b['type']=='data_table');li=b['lineage']
steps['tile_096.s01']['blocks'].append({'type':'diagram','diagram_kind':'mapping','nodes':[{'id':'n'+str(i+1),'label':label} for i,label in enumerate(labels)],'edges':[],'alt_text':'Each caller can retrieve its own order; cross-owner substitutions return no order data.','lineage':copy.deepcopy(li)})
# 097: complete declarations wired beside the unchanged verifier and permission dependencies.
c='fastapi.production_security_documentation';d=W/c
code="""import json
from pathlib import Path
from fastapi import Depends, Security
from fastapi.security import HTTPBearer, OAuth2AuthorizationCodeBearer
issuer_configuration=json.loads(Path('issuer_configuration.json').read_text())
bearer_scheme=HTTPBearer(scheme_name='OrderBearer')
code_scheme=OAuth2AuthorizationCodeBearer(
    authorizationUrl=issuer_configuration['authorization_url'],
    tokenUrl=issuer_configuration['token_url'],
    scopes=issuer_configuration['scopes'],scheme_name='OrderAuthorizationCode')
"""
(d/'starter.py').write_text(code)
app=(d/'application.py').read_text();app=app.replace('from fastapi import FastAPI, Depends','from fastapi import FastAPI, Depends, Security\nfrom starter import bearer_scheme, code_scheme')
app=app.replace("@app.get('/orders/{order_id}')","@app.get('/orders/{order_id}', dependencies=[Security(bearer_scheme), Security(code_scheme, scopes=['orders:read'])])")
app=app.replace("@app.post('/orders',status_code=201)","@app.post('/orders',status_code=201, dependencies=[Security(bearer_scheme), Security(code_scheme, scopes=['orders:write'])])")
app=app[:app.index('# TODO: operation')];(d/'application.py').write_text(app)
capture="""import json
from application import app
schema=app.openapi()
print(json.dumps({'components':{'securitySchemes':schema['components']['securitySchemes']},
                  'operations':{method.upper()+' '+path:operation['security']
                     for path,methods in schema['paths'].items()
                     for method,operation in methods.items()}},indent=2))
"""
out=run(c,capture)
b=next(b for b in steps['tile_097.s01']['blocks'] if b['type']=='side_by_side')
# Replace the instruction-only declarations with the completed ones; retain enforcement.
b['right']['code']=code+'\n'+app+'\n'+(d/'dependencies.py').read_text()
steps['tile_097.s01']['blocks'].append(pair(copy.deepcopy(b['right']),panel(code+'\n'+app+'\n'+capture,out,b['lineage']),'Declarations beside unchanged verification and permission enforcement','Generated security schemes and operation requirements','Generated security schemes and operation requirements',b['lineage']))
allowed={'tile_083.s01','tile_085.s01','tile_087.s01','tile_088.s01','tile_089.s01','tile_090.s01','tile_093.s05','tile_093.s10','tile_096.s01','tile_097.s01'}
for old,new in zip(original['tiles'],s['tiles']):
 assert {k:v for k,v in old.items() if k!='steps'}=={k:v for k,v in new.items() if k!='steps'}
 for a,b in zip(old['steps'],new['steps']):
  if a!=b: assert a['step_id'] in allowed
  assert {k:v for k,v in a.items() if k!='blocks'}=={k:v for k,v in b.items() if k!='blocks'}
(P/'screens.json').write_text(json.dumps(s,indent=2,ensure_ascii=False)+'\n')
print('Patched',len(allowed),'named steps; tiles',len(s['tiles']),'steps',sum(len(t['steps']) for t in s['tiles']),'remediation',sum(len(t.get('remediation_steps',[])) for t in s['tiles']))
