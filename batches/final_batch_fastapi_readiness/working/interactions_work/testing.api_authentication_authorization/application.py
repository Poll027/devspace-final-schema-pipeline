import json
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException
from security import verified_token_context
fixtures=json.loads(Path('fixtures.json').read_text())
orders={row['id']:row for row in fixtures['orders']}
app=FastAPI()
def operation_permission(context=Depends(verified_token_context)):
    if 'orders:read' not in context['scopes']:
        raise HTTPException(403,'Forbidden')
    return context
@app.get('/orders/{order_id}')
def order(order_id:int, context=Depends(operation_permission)):
    row=orders.get(order_id)
    if row is None or row['owner_id']!=context['owner_id']:
        raise HTTPException(403,'Forbidden')
    return {'id':row['id'],'status':row['status']}
