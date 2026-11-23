import json
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
packet = json.loads(Path('fixtures.json').read_text())
app = FastAPI()
runtime_evidence = []
async def controlled_lookup():
    # Deterministic timeout injection: no real remote service and no measured
    # 2010ms delay. Packet offsets remain authored synthetic data.
    raise TimeoutError('controlled outbound lookup timeout')
@app.post('/orders')
async def create_order(request: Request):
    payload = await request.json()
    interaction = packet['interaction_id']
    if payload != packet['failing_order_payload']:
        return JSONResponse({'detail':'Unknown controlled payload'}, status_code=422)
    runtime_evidence.append({'interaction_id':interaction,'boundary':'local','event':'request_received'})
    runtime_evidence.append({'interaction_id':interaction,'boundary':'database','event':'lookup_complete','provenance':'simulated database lookup; no SQL executed'})
    runtime_evidence.append({'interaction_id':interaction,'boundary':'outbound','event':'lookup_started'})
    try:
        await controlled_lookup()
    except TimeoutError:
        runtime_evidence.append({'interaction_id':interaction,'boundary':'outbound','event':'timeout','provenance':'controlled exception injection'})
        return JSONResponse({'detail':'Lookup timeout'}, status_code=504,
                            headers={packet['interaction_header']:interaction})
def client():
    return TestClient(app)
