import json,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from application import app,orders,security_configuration,fixtures
from models import OrderInput,PublicOrder
from acquisition_harness import AcquisitionHarness
# Supply an issuer-acquired credential to exercise non-authentication behavior;
# this capture adds no authentication/authorization cases or assertions.
issued_token=AcquisitionHarness(security_configuration['authorization_code_issuer']).acquire()
orders.clear();orders.update({row['id']:dict(row) for row in fixtures['initial_orders']})
existing=fixtures['initial_orders'][0]['id']
missing=max([row['id'] for row in fixtures['initial_orders']]+[fixtures['created_order']['id']])+1
requests=[{'method':'GET','path':f'/orders/{existing}'},
          {'method':'GET','path':f'/orders/{missing}'},
          {'method':'POST','path':'/orders','json':fixtures['created_order']},
          {'method':'POST','path':'/orders','json':fixtures['synthetic_example']},
          {'method':'POST','path':'/orders','json':{**fixtures['synthetic_example'],'id':-1}}]
records=[]
with TestClient(app) as client:
    schema=client.get('/openapi.json').json()
    for request in requests:
        response=client.request(request['method'],request['path'],json=request.get('json'),headers={'Authorization':'Bearer '+issued_token})
        records.append({'request':request,'status':response.status_code,'body':response.json()})
source_hashes={name:hashlib.sha256(Path(name).read_bytes()).hexdigest() for name in ['application.py','models.py','fixtures.json','capture.py','dependencies.py','existing_verifier.py','issuer_configuration.json','acquisition_harness.py']}
Path('http_evidence.json').write_text(json.dumps({'provenance':{'kind':'captured TestClient HTTP outcomes from supplied fictional app','source_sha256':source_hashes,'authentication_tests':False},'records':records},indent=2)+'\n')
Path('generated_schema.json').write_text(json.dumps(schema,indent=2)+'\n')
Path('security_configuration.json').write_text(json.dumps(security_configuration,indent=2)+'\n')
