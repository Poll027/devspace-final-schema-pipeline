import json
from pathlib import Path
from fastapi.testclient import TestClient
from application import app,security_configuration
from models import OrderInput,PublicOrder,ErrorBody
from starter import audit
http_evidence=json.loads(Path('http_evidence.json').read_text())
with TestClient(app) as client:
    findings=audit(client,{'OrderInput':OrderInput,'PublicOrder':PublicOrder,'ErrorBody':ErrorBody},http_evidence,security_configuration)
print(json.dumps(findings,indent=2))
