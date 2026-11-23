import httpx
from fastapi import FastAPI, Depends, HTTPException
from fastapi.testclient import TestClient
UPSTREAM_URL = 'https://upstream.invalid/lookup'  # Authored mock-only URL, never a provisioned service.
app = FastAPI()
async def client_provider():
    async with httpx.AsyncClient() as client:
        yield client
async def lookup(client):
    response = await client.get(UPSTREAM_URL)
    # TODO: raise_for_status and translate HTTPStatusError versus RequestError.
    return response.json()
@app.get('/lookup')
async def route(client=Depends(client_provider)):
    return await lookup(client)
def status_failure(request):
    return httpx.Response(503, request=request)
def timeout_failure(request):
    raise httpx.ReadTimeout('Controlled timeout', request=request)
# TODO: override client_provider with a MockTransport for each failure,
# then assert the supplied local status/body through TestClient.
