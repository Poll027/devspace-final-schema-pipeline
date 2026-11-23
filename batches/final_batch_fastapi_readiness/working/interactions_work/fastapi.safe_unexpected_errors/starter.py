from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
app = FastAPI(debug=False)
safe_records = []
def record_safe_failure(request):
    safe_records.append({'event':'unexpected_failure','code_location':'controlled_failure',
                         'interaction_context':'interaction_fixture'})
@app.get('/controlled-failure')
def controlled_failure():
    raise RuntimeError('Controlled internal failure; never disclose this string')
# TODO: register @app.exception_handler(Exception), call record_safe_failure,
# and return the fixtures.json generic 500 body. Never log exception strings.
with TestClient(app, raise_server_exceptions=False) as client:
    response = client.get('/controlled-failure')
    # TODO: assert public response and safe internal records separately.
