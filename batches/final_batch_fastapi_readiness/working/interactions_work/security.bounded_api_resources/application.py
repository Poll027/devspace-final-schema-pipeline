import json
from pathlib import Path
import httpx
from fastapi import FastAPI, Depends
from starlette.middleware.body_limit import RequestBodyLimitMiddleware
from starter import BatchInput
budgets = json.loads(Path('fixtures.json').read_text())['hypothetical_budgets']
app = FastAPI()
expensive_calls = 0
outbound_timeout = httpx.Timeout(None)  # TODO: supplied finite timeout
async def expensive_dependency(value: BatchInput):
    global expensive_calls
    expensive_calls += 1
    transport=httpx.MockTransport(lambda request:httpx.Response(200,json={'available':True}))
    async with httpx.AsyncClient(transport=transport,timeout=outbound_timeout) as http:
        response=await http.get('http://controlled-dependency.invalid/lookup')
        return response.json()['available']
@app.post('/orders/batch')
async def batch(value: BatchInput, available=Depends(expensive_dependency)):
    return {'accepted':len(value.order_ids)}
# TODO: immediately after app construction and before requests, configure
# app.add_middleware(RequestBodyLimitMiddleware, max_body_size=...)
# Use budgets['body_bytes']; middleware_verification.json supplies the measured
# rejection contract. Leave the dependency counter intact.
