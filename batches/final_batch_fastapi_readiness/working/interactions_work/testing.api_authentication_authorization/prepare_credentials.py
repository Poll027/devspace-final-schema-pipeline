import json,time
from pathlib import Path
import jwt
config=json.loads(Path('test_trust.json').read_text())
cases=json.loads(Path('fixtures.json').read_text())['cases']
now=int(time.time())
headers={}
for case in cases:
    condition=case['credential_condition']
    if condition=='absent': headers[condition]={}; continue
    if condition=='malformed': headers[condition]={'Authorization':'Bearer not.a.jwt'}; continue
    claims={'iss':config['issuer'],'aud':config['audience'],'sub':case['trusted_owner_id'],
            'exp':now+3600,'scope':'orders:read' if case['operation_permission'] else ''}
    if condition=='expired': claims['exp']=now-3600
    if condition=='wrong_issuer': claims['iss']='wrong-controlled-issuer'
    if condition=='wrong_audience': claims['aud']='wrong-controlled-audience'
    key=config['test_key'] if condition!='invalid_signature' else config['test_key']+'wrong'
    token=jwt.encode(claims,key,algorithm='HS256')
    headers[condition]={'Authorization':'Bearer '+token}
Path('bearer_fixtures.json').write_text(json.dumps(headers,indent=2)+'\n')
