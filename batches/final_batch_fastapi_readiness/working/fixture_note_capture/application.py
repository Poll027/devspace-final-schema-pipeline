import json
from pathlib import Path
from fastapi import FastAPI,APIRouter,HTTPException,Depends
from fastapi.security import HTTPBearer
from dependencies import read_orders, write_orders
from models import OrderInput,PublicOrder,ErrorBody
router=APIRouter(prefix='/orders',tags=['orders'])
# Established training issuer; verification and permissions are active.
# Bearer metadata is present; the unfinished audit compares issuer declarations.
bearer=HTTPBearer(auto_error=False,scheme_name='OrderBearer')
fixtures=json.loads(Path('fixtures.json').read_text())
orders={row['id']:dict(row) for row in fixtures['initial_orders']}
@router.post('',response_model=PublicOrder,status_code=201,
             responses={409:{'model':ErrorBody,'description':'Duplicate order'}})
def create_order(value:OrderInput,credential=Depends(bearer),principal=Depends(write_orders)):
    if value.id in orders:
        # Deliberate documentation drift: actual conflict is 400, not declared 409.
        raise HTTPException(400,'Duplicate order')
    row={**value.model_dump(),'owner_id':fixtures['initial_orders'][0]['owner_id']}
    orders[value.id]=row
    return row
@router.get('/{order_id}',response_model=PublicOrder,
            responses={404:{'model':ErrorBody,'description':'Order unavailable'}})
def retrieve_order(order_id:int,credential=Depends(bearer),principal=Depends(read_orders)):
    if order_id not in orders: raise HTTPException(404,'Not found')
    return orders[order_id]
app=FastAPI()
app.include_router(router)
security_configuration={'schemes': {'OrderBearer': {'type': 'http', 'scheme': 'bearer'}, 'OrderAuthorizationCode': {'type': 'oauth2', 'flows': {'authorizationCode': {'authorizationUrl': 'http://127.0.0.1:37353/authorize', 'tokenUrl': 'http://127.0.0.1:37353/token', 'scopes': {'orders:read': 'Read orders', 'orders:write': 'Create orders'}}}}}, 'operations': {'GET /orders/{order_id}': [{'OrderBearer': [], 'OrderAuthorizationCode': ['orders:read']}], 'POST /orders': [{'OrderBearer': [], 'OrderAuthorizationCode': ['orders:write']}]}, 'authorization_code_issuer': {'issuer': 'http://127.0.0.1:37353', 'authorization_url': 'http://127.0.0.1:37353/authorize', 'token_url': 'http://127.0.0.1:37353/token', 'jwks_url': 'http://127.0.0.1:37353/jwks', 'client_id': 'order-training-client', 'redirect_uri': 'http://127.0.0.1:37353/client/callback', 'algorithms': ['RS256'], 'required_claims': ['iss', 'aud', 'sub', 'exp', 'iat'], 'audience': 'order-api', 'scopes': {'orders:read': 'Read orders', 'orders:write': 'Create orders'}, 'pkce': {'required': True, 'code_challenge_method': 'S256'}, 'runtime_boundary': 'Publisher-provisioned isolated loopback training issuer; not a public production service.'}, 'dependency_graph': ['operation -> read_orders/write_orders -> authenticated -> HTTPBearer extraction -> ExistingVerifier.verify -> JWKS signature/issuer/audience/required claims', 'read_orders/write_orders -> enforce_permission -> required scope'], 'operation_dependencies': {'GET /orders/{order_id}': {'dependency': 'read_orders', 'scope': 'orders:read'}, 'POST /orders': {'dependency': 'write_orders', 'scope': 'orders:write'}}, 'provenance': 'Supplied application configuration backed by the separately provisioned loopback training issuer and active verification/permission dependencies.', 'note': 'Compare generated security declarations with this supplied established configuration; do not add authentication or authorization tests to this audit.'}
