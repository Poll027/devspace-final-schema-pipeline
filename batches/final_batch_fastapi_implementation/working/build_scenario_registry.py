import json, re, ast
from pathlib import Path
B = Path('batches/final_batch_implementation')
source = json.loads((B/'inputs/path_glossary_bundle.json').read_text())
bundles = source['bundles']
sid = 'scenario.orders_service'
# Mine all teaching and anchor vocabulary before authoring fixtures.
texts = []
for b in bundles:
    texts += [t['content'] for t in b['teaching_blocks']]
    p = b['practice_anchor']
    texts += [p['objective'], p['success'], b['visual_anchor']['purpose']]
    live = p['live_code']
    texts += [live['starter_state_intent'], live['observable_success']] + live['allowed_syntax']
text = '\n'.join(texts)
patterns = [r'(?<![A-Za-z])/(?:[A-Za-z0-9_{}-]+/?)+', r'\b[A-Za-z][A-Za-z0-9]*_[A-Za-z0-9_]+\b', r'\b[A-Z][A-Za-z0-9]*[A-Z][A-Za-z0-9]*\b', r'\b\d+(?:\.\d+)*\b', r'\b(?:orders?|booking|shipping|start|end|quantity|status|limit|page|pagination|provider|context|router|handler|uvicorn|httpx|asyncio|pydantic|main|app|dotenv|Settings|Booking|PublicOrder|FastAPI|APIRouter|Depends|Annotated|BaseModel|BaseSettings|SettingsConfigDict|AsyncClient|ValidationError|ValueError|TimeoutError|HTTPException|BackgroundTasks|Response|TestClient|A|B)\b', r'main:app', r'\.env', r'--[a-z]+']
vocab = sorted(set(v for p in patterns for v in re.findall(p,text)))
registry = {'schema_version':'1.0','kind':'scenario_asset_registry','path_id':source['path_id'],'batch_id':B.name,'scenarios':[{'scenario_id':sid,'name':'Fictional orders service','summary':'A small fictional orders service includes booking rules, shipping lookups and optional order follow-up work. Separate exercise snapshots focus on the glossary contracts without adding persistence, authentication verification or deployment guarantees. All fixture values are authored synthetic examples, not real-world records.','domain':'orders API implementation','glossary_example_vocab':vocab}],'assets':[]}
def col(name, typ, role, **kw):
    return dict(name=name,type=typ,semantic_role=role,**kw)
def dataset(aid,title,columns,rows):
    a = dict(asset_id=aid,asset_kind='dataset',scenario_id=sid,title=title,description='Authored synthetic fixture; not a real-world record.',columns=columns,rows=rows,provenance='authored',variants=[])
    registry['assets'].append(a)
    return [dict(zip([c['name'] for c in columns],r)) for r in rows]
state = dataset('ds.order_state','Order-state fixture', [col('order_id','integer','identifier',numeric_looking_label=True),col('quantity','integer','numerical',description='Stored quantity used by the authored exercise decision.')], [[42,5],[43,0],[44,3],[45,10],[46,1]] + [[n,2] for n in sorted({int(v) for v in re.findall(r'/orders/(\d+)',text)} - {42,43,44,45,46})])
internal = dataset('ds.internal_orders','Internal order projection fixture', [col('order_id','integer','identifier',numeric_looking_label=True),col('status','string','categorical'),col('private_processing_note','string','text',description='Synthetic internal note excluded by PublicOrder.')], [[r['order_id'], 'pending' if i%2==0 else 'ready', 'synthetic internal note '+str(i+1)] for i,r in enumerate(state)])
files = {}
files[0] = {'main.py': '\n'.join(f'{name}: {typ} = {value}' for typ,names,value in [('str',['orders_collection_path','orders_item_path','orders_retrieve_method','orders_create_method','orders_replace_method','orders_remove_method','orders_created_location'],'""'),('int',['orders_created_status','orders_absent_status'],'0')] for name in names)+'\n'}
files[1] = {'main.py': '''# TODO: import FastAPI and construct app.
# TODO: register POST /orders.
def create_order():
    return {}
# TODO: register GET /orders/current before parameterized GET.
def current_order():
    return {}
# TODO: register GET /orders/{order_id}.
def retrieve_order():
    return {}
# TODO: register PUT /orders/{order_id}.
def replace_order():
    return {}
# TODO: register DELETE /orders/{order_id}.
def remove_order():
    return {}
'''}
files[2] = {'settings.py': '''from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # TODO: declare required app_name: str and dotenv model_config.
    pass

# TODO: construct Settings().
''', '.env': 'APP_NAME=synthetic-dotenv-orders\n', 'source_cases.json':json.dumps([{'name':'environment_only','environment':{'APP_NAME':'synthetic-environment-orders'},'dotenv':{}},{'name':'conflicting_sources','environment':{'APP_NAME':'synthetic-environment-orders'},'dotenv':{'APP_NAME':'synthetic-dotenv-orders'}},{'name':'absent_from_both','environment':{},'dotenv':{}}],indent=2)}
files[3] = {'main.py': '''import httpx

# Synthetic URLs: the exercise harness must intercept requests; never contact them.
lookup_urls = ("https://shipping.example.test/orders/42", "https://shipping.example.test/orders/43")

async def orders():
    # TODO: one owning AsyncClient scope, both awaited calls, then cleanup.
    pass
'''}
# Derive the specified booking pairs from the anchor rather than retyping them.
pairs = [dict(start=int(s),end=int(e)) for s,e in re.findall(r'start=(\d+)(?:,?\s+(?:and\s+)?)end=(\d+)', bundles[4]['practice_anchor']['success'])]
assert len(pairs) == 2, 'Booking anchor pairs were not mined'
files[4] = {'main.py': '''from pydantic import BaseModel, model_validator, ValidationError

class Booking(BaseModel):
    start: int
    end: int
    # TODO: add an after-model invariant validator.
''', 'checks.py': 'from main import Booking\nfrom pydantic import ValidationError\n\ncases = '+repr(pairs)+'''\nfor values in cases:
    if values['end'] <= values['start']:
        try:
            Booking(**values)
        except ValidationError:
            pass
        else:
            raise AssertionError('Inconsistent pair was accepted')
    else:
        booking = Booking(**values)
        assert booking.start == values['start'] and booking.end == values['end']
'''}
files[5] = {'main.py': '''from fastapi import FastAPI, HTTPException
app = FastAPI()
order = None

@app.get("/order")
def get_order():
    if order is None:
        # TODO: raise the intended expected rejection here.
        pass
    return order
'''}
files[6] = {'main.py': '''from fastapi import FastAPI
from supplied import shipping_client
app = FastAPI()

def shipping_utility():
    return shipping_client.lookup()

@app.get("/shipping")
async def shipping():  # TODO: choose execution mode for blocking I/O.
    return shipping_utility()

# TODO: annotate execution location of handler and direct utility call.
''', 'supplied.py': '''import time

class BlockingShippingClient:
    """Synthetic blocking I/O stand-in; no network access."""
    def lookup(self):
        time.sleep(0.01)
        return {"status": "synthetic-shipping-result"}

shipping_client = BlockingShippingClient()
'''}
files[7] = {'orders.py': '''from fastapi import APIRouter
# TODO: construct feature router and register GET /orders.
def list_orders():
    return []
''','main.py': '''from fastapi import FastAPI
app = FastAPI()
# TODO: import feature router and include with /api prefix.
'''}
files[8] = {'main.py': '''from fastapi import FastAPI
app = FastAPI()

@app.get("/orders/{order_id}")
def read_order():  # TODO: typed order_id and defaulted limit inputs.
    return {}  # Replace with the bound values if useful for inspection.
'''}
files[9] = {'main.py': 'from fastapi import FastAPI\nfrom pydantic import BaseModel\napp = FastAPI()\ninternal_order = '+repr(internal[0])+'''\n
# TODO: PublicOrder with the two public fields only.
@app.get("/orders/{order_id}")  # TODO: configure response_model.
def read_order(order_id: int):
    return internal_order
''', 'internal_cases.json':json.dumps(internal,indent=2)}
files[10] = {'main.py': '''from typing import Annotated
from fastapi import FastAPI, Depends
app = FastAPI()

def provider() -> str:
    return "synthetic-auth-context-not-verified"

@app.get("/orders")
def orders():  # TODO: declare context through Annotated and Depends.
    return {}  # TODO: return supplied context, without calling provider here.
'''}
files[11] = {'main.py': '''import httpx
shipping_url = "http://127.0.0.1:8765/shipping"

async def shipping_lookup():
    # TODO: finite HTTPX timeout and distinct timeout outcome.
    pass
''', 'harness.py': '''import asyncio
import contextlib
import main

async def stalled_upstream(reader, writer):
    try:
        await reader.readuntil(b"\\r\\n\\r\\n")
        # Accept connection but do not send a response chunk.
        await asyncio.sleep(30)
    finally:
        writer.close()
        with contextlib.suppress(ConnectionError):
            await writer.wait_closed()

async def run():
    server = await asyncio.start_server(stalled_upstream, "127.0.0.1", 0)
    port = server.sockets[0].getsockname()[1]
    main.shipping_url = f"http://127.0.0.1:{port}/shipping"
    async with server:
        result = await main.shipping_lookup()
        print(result)

if __name__ == "__main__":
    asyncio.run(run())
'''}
state_literal = repr({r['order_id']:r for r in state})
files[12] = {'main.py': 'from fastapi import FastAPI, Depends\nfrom supplied import order_state, adapter, requested_quantity\napp = FastAPI()\n\n@app.get("/orders/{order_id}")\ndef decide_order(order_id: int, quantity: int):\n    # Authored exercise rule: accept when requested quantity is at most stored quantity.\n    return quantity <= order_state[order_id]["quantity"]\n\n# TODO: plain decision callable, adapter-only state access, declared input provider.\n', 'supplied.py': 'order_state = '+state_literal+'''\n
class OrderStateAdapter:
    def quantity(self, order_id: int) -> int:
        return order_state[order_id]["quantity"]

adapter = OrderStateAdapter()

def requested_quantity(quantity: int) -> int:
    return quantity
''', 'state_cases.json':json.dumps(state,indent=2)}
files[13] = {'main.py': '''from fastapi import FastAPI, BackgroundTasks
from supplied import order_follow_up
app = FastAPI()

@app.post("/orders")
def create_order():  # TODO: declare background_tasks parameter.
    order_id = "42"
    # TODO: register optional follow-up before returning response.
    return {"order_id": order_id}
''', 'supplied.py': '''follow_ups = []

def order_follow_up(order_id: str):
    """Small optional, process-local synthetic effect; losing it is acceptable."""
    follow_ups.append(order_id)
'''}
files[14] = {'main.py': '''from typing import Annotated
from fastapi import FastAPI, Depends
app = FastAPI()

def pagination():  # TODO: typed page and page_size query inputs.
    return {}  # TODO: return page and page_size.

def order_options():  # TODO: declared dependency on pagination.
    return {}  # TODO: return supplied dictionary.

@app.get("/orders")
def orders():  # TODO: declared dependency on order_options.
    return {}  # TODO: return order-options result.
'''}
files[15] = {'main.py': '''from fastapi import FastAPI
from supplied import A, B
app = FastAPI()

@app.get("/orders")
def orders():
    return []

# Supplied configuration: A uses minimum_size=500, B uses allowed_hosts=["testserver"].
# TODO: add A first, B second using app.add_middleware.
# TODO: annotate request and resulting response traversal.
''', 'supplied.py': '''from starlette.middleware.gzip import GZipMiddleware as A
from starlette.middleware.trustedhost import TrustedHostMiddleware as B
''', 'middleware_options.json':json.dumps({'A':{'class':'starlette.middleware.gzip.GZipMiddleware','documented_options':{'minimum_size':500}},'B':{'class':'starlette.middleware.trustedhost.TrustedHostMiddleware','documented_options':{'allowed_hosts':['testserver']}}},indent=2)}
files[16] = {'main.py': '''from fastapi import FastAPI
app = FastAPI()

@app.get("/orders")
def orders():
    return []
''', 'run.sh': '#!/bin/sh\n# TODO: start the supplied application with the glossary production command.\n'}
for i,b in enumerate(bundles):
    readme = '# '+b['context']['concept_name']+'\n\nFictional authored exercise snapshot; independent from the other workspaces.\n\n'
    readme += '\n\n'.join(t['content'] for t in b['teaching_blocks'])
    readme += '\n\n## Practice contract (copied from glossary)\n'+json.dumps(b['practice_anchor'],ensure_ascii=False,indent=2)
    readme += '\n\n## Visual anchor (copied from glossary)\n'+json.dumps(b['visual_anchor'],ensure_ascii=False,indent=2)+'\n'
    readme += '\nEnvironment: Python with FastAPI, HTTPX, Pydantic v2, pydantic-settings and Uvicorn available. This registry declares starter assets, not verified execution results. TODOs are intentional.\n'
    if i == 2:
        readme += '\nEach source case is isolated: clear APP_NAME and replace .env according to source_cases.json before Settings construction. No other settings are introduced.\n'
    if i == 3:
        readme += '\nThe two lookup URLs are synthetic .test addresses supplied for inspection or an intercepted HTTPX harness. They must not be sent to the public network.\n'
    if i == 11:
        readme += '\nRun python harness.py after completing main.py. Use a read-wait limit shorter than the authored 30-second stall. The harness binds a local ephemeral port; it does not contact a real shipping service. The printed result must be computed, not transcribed.\n'
    if i == 12:
        readme += '\nThe quantity comparison is an authored exercise decision, not a real business fact. state_cases.json mirrors ds.order_state. Preserve it during refactoring.\n'
    if i == 15:
        readme += '\nA and B are aliases for supplied maintained Starlette middleware classes; middleware_options.json supplies their compatible keyword options. No implementation of their protocols is required.\n'
    files[i]['README.md'] = readme
    registry['assets'].append(dict(asset_id='ws.'+b['context']['concept_id'],asset_kind='code_workspace',scenario_id=sid,title=b['context']['concept_name'],runtime='python',files=[dict(path=p,content=c) for p,c in files[i].items()]))
# Own mistakes-to-avoid and scope checklist. No messy-table concept requires a variant.
assert len(files) == len(bundles)
assert len({a['asset_id'] for a in registry['assets']}) == len(registry['assets'])
for a in registry['assets']:
    assert a['scenario_id'] == sid
    if a['asset_kind'] == 'dataset':
        assert all(len(r)==len(a['columns']) for r in a['rows'])
        assert all(c['semantic_role'] != 'numerical' or c['type'] in ('integer','number') for c in a['columns'])
        assert all(c.get('numeric_looking_label') for c in a['columns'] if c['semantic_role']=='identifier' and c['type']=='integer')
        assert not a['variants']
    else:
        for f in a['files']:
            if f['path'].endswith('.py'): ast.parse(f['content'])
assert {c['name'] for a in registry['assets'] if a['asset_kind']=='dataset' for c in a['columns']} == {'order_id','quantity','status','private_processing_note'}
assert all(b['visual_anchor']['type'] in ('code','diagram','process_flow') for b in bundles), 'Review rendered image needs'
(B/'scenario_asset_registry.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n')
(B/'working/scenario_asset_checklist.json').write_text(json.dumps({'concept_count':len(bundles),'scenario_count':len(registry['scenarios']),'asset_count':len(registry['assets']),'dataset_count':2,'workspace_count':len(files),'image_count':0,'variant_count':0,'row_widths':'checked','semantic_roles':'checked: identifiers are labels, quantities are measures, status categorical, private note text','numeric_identifier_labels':'flagged','planted_issues':'not applicable: no variants or messy-data examples','scope':'one independent starter workspace per concept; both storage and internal projection fixtures registered','example_vocabulary':'mined from all teaching blocks and practice/visual/assessment anchors','plots':'no plot-dependent concepts; code/diagram/process_flow anchors only','starter_python_syntax':'all parsed; TODOs intentional','uncertainties':['No concrete shipping URLs, configuration values, middleware classes/options or stored-state decision are fixed by the glossary: supplied synthetic fixtures are explicitly identified as exercise choices.','Registry gate may mark code_workspace assets unverified; no execution outputs are asserted.']},indent=2)+'\n')
print('scenarios',len(registry['scenarios']),'assets',len(registry['assets']),'datasets',2,'workspaces',len(files))
print('\n'.join(a['asset_id'] for a in registry['assets']))
