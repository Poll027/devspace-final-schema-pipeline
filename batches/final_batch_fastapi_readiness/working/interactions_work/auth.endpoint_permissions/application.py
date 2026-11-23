import json
from pathlib import Path
from fastapi import FastAPI, Depends, Security
from pydantic import BaseModel
from security import verified_token_context
from starter import require_permissions
app=FastAPI()
fixtures=json.loads(Path('fixtures.json').read_text())
order={key:fixtures['order'][key] for key in ['id','status']}
class Modification(BaseModel):
    status: str
@app.patch('/orders/'+str(fixtures['order']['id']))
def modify_order(body:Modification, context=Depends(verified_token_context)):
    # TODO: replace context Depends with Security(require_permissions,
    # scopes=['orders:write']); keep the verification dependency active.
    order['status']=body.status
    return dict(order)
