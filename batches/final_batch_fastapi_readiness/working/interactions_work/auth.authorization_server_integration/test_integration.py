import json
from pathlib import Path
from fastapi.testclient import TestClient
from application import app, existing_verifier
from starter import integrate
def test_issuer_integration():
    configuration=json.loads(Path('issuer_configuration.json').read_text())
    token=integrate(configuration,existing_verifier)
    with TestClient(app) as client:
        accepted=client.get('/protected',headers={'Authorization':'Bearer '+token})
        # Change a signature character (not its final padding bits).
        prefix,signature=token.rsplit('.',1)
        tampered=prefix+'.'+('A' if signature[0]!='A' else 'B')+signature[1:]
        rejected=client.get('/protected',headers={'Authorization':'Bearer '+tampered})
        # TODO: HTTP acceptance and rejection assertions. No dependency overrides.
        raise NotImplementedError('Complete HTTP assertions')
