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
