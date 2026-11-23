from pydantic import BaseModel, Field
import json
from pathlib import Path
budgets=json.loads(Path('fixtures.json').read_text())['hypothetical_budgets']
class BatchInput(BaseModel):
    order_ids: list[int] = Field(max_length=budgets['batch_size'])

import json
from pathlib import Path
import httpx
from fastapi import FastAPI, Depends
from starlette.middleware.body_limit import RequestBodyLimitMiddleware
from starter import BatchInput
budgets = json.loads(Path('fixtures.json').read_text())['hypothetical_budgets']
app = FastAPI()
app.add_middleware(RequestBodyLimitMiddleware,max_body_size=budgets['body_bytes'])
expensive_calls = 0
outbound_timeout = httpx.Timeout(budgets['dependency_timeout_seconds'])
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

import json
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
