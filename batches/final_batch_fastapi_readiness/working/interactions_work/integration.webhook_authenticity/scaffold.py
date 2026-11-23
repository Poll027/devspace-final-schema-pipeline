import json
from pathlib import Path
import stripe
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from starter import webhook
config = json.loads(Path('test_config.json').read_text())
raw_body = Path('signed_body.json').read_bytes()
processed_events = []
def process_event(event):
    processed_events.append(event)
# Test-only snapshot: Stripe SDK still verifies the signature. Suppress age
# expiry of a stored teaching fixture; do not use tolerance=0 in deployment.
def publisher_verifier(raw, signature, signing_secret):
    return stripe.Webhook.construct_event(raw, signature, signing_secret, tolerance=0)
# Fail during setup if the supplied fixture is not actually SDK-verifiable.
publisher_verifier(raw_body, config['signature'], config['endpoint_signing_secret'])
app = FastAPI()
@app.post('/webhook')
async def endpoint(request: Request):
    return await webhook(request, config['endpoint_signing_secret'],
                         publisher_verifier, config['signature_header'], process_event)
def client():
    return TestClient(app)
