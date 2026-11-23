from fastapi import FastAPI, Depends, Security
from starter import bearer_scheme, code_scheme
from dependencies import read_orders, write_orders
app=FastAPI()
orders={101: {'id': 101, 'status': 'pending'}}
# Existing enforcement is fixed. Add documentation/security dependencies beside
# these, never replace verification or permissions with metadata-only schemes.
@app.get('/orders/{order_id}', dependencies=[Security(bearer_scheme), Security(code_scheme, scopes=['orders:read'])])
def retrieve_order(order_id:int,principal=Depends(read_orders)):
    from fastapi import HTTPException
    if order_id not in orders:raise HTTPException(404,'Not found')
    return orders[order_id]
@app.post('/orders',status_code=201, dependencies=[Security(bearer_scheme), Security(code_scheme, scopes=['orders:write'])])
def create_order(value:dict,principal=Depends(write_orders)):
    orders[value['id']]=value
    return value
