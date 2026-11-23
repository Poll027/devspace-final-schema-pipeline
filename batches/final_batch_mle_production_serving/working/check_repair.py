import ast, json, os, subprocess, sys, tempfile, time
from pathlib import Path
root=Path.cwd()
d=json.loads((root/'batches/final_batch_mle.region.production_serving/scenario_asset_registry.json').read_text())
working=root/'batches/final_batch_mle.region.production_serving/working'
assets={a['asset_id']:a for a in d['assets']}
# Mistakes-to-avoid: untouched authored datasets remain width-consistent; the
# deterministic registry gate checks roles, variants and planted predicates.
for a in d['assets']:
    if a['asset_kind']=='dataset':
        assert all(len(r)==len(a['columns']) for r in a['rows'])
for a in d['assets']:
    for f in a.get('files',[]):
        if f['path'].endswith('.py'): ast.parse(f['content'])

def mount(asset, folder):
    for f in asset['files']:
        p=folder/f['path']; p.parent.mkdir(parents=True,exist_ok=True);p.write_text(f['content'])

with tempfile.TemporaryDirectory(dir=working) as name:
    p=Path(name); mount(assets['ws.prediction_authentication'],p)
    check='''import os, secrets
from google.oauth2 import id_token
from google.auth.transport import requests
from google.auth.exceptions import GoogleAuthError
import auth_fixture
assert GoogleAuthError is auth_fixture.GoogleAuthError
assert id_token.verify_oauth2_token is auth_fixture.verify_oauth2_token
os.environ[auth_fixture.contract["injected_secret_variable"]] = secrets.token_urlsafe()
token = auth_fixture.runtime_secret()
claims = id_token.verify_oauth2_token(token, requests.Request(), audience=auth_fixture.contract["expected_audience"])
assert claims == auth_fixture.cases["authorized"]["verified_claims"]
from supplied_prediction import reject_malformed, contract
try: reject_malformed({"features": []})
except ValueError: pass
else: raise AssertionError("empty matrix accepted")
assert reject_malformed(contract["expected_request"]) == contract["expected_request"]["features"]
'''
    subprocess.run([sys.executable,'-c',check],cwd=p,check=True)
with tempfile.TemporaryDirectory(dir=working) as name:
    p=Path(name); mount(assets['ws.model_service_readiness'],p)
    # Exercise the supplied monitor directly with a configured command that
    # changes from failure to success; no learner solution is installed.
    contract=json.loads((p/'contract.json').read_text())
    timing=contract['healthcheck']
    interval=timing['interval_seconds']/100
    hc={'test':['CMD',sys.executable,'-c','from pathlib import Path; raise SystemExit(not Path("healthy.marker").exists())'],
        'interval':str(interval)+'s','timeout':str(timing['timeout_seconds'])+'s','retries':timing['retries']}
    result=p/'health.json'
    monitor=subprocess.Popen([sys.executable,'offline_runtime.py','--health-worker',str(os.getpid()),json.dumps({'healthcheck':hc,'environment':{}}),str(result)],cwd=p)
    try:
        deadline=time.monotonic()+timing['timeout_seconds']*timing['retries']
        while time.monotonic()<deadline:
            if result.exists():
                health=json.loads(result.read_text())
                if health['Status']=='unhealthy': break
            time.sleep(interval)
        else: raise AssertionError('configured failures not reflected')
        assert health['FailingStreak']>=hc['retries']
        assert all(x['ExitCode']!=0 for x in health['Log'])
        (p/'healthy.marker').touch()
        while time.monotonic()<deadline:
            health=json.loads(result.read_text())
            if health['Status']=='healthy': break
            time.sleep(interval)
        else: raise AssertionError('configured success not reflected')
        assert health['FailingStreak']==0 and health['Log'][-1]['ExitCode']==0
    finally:
        monitor.terminate();monitor.wait()
# All copies of the shared contracts receive identical corresponding repairs.
malformed=[f['content'] for a in d['assets'] for f in a.get('files',[]) if f['path']=='supplied_prediction.py']
assert all('if not isinstance(values, list) or not values:' in s for s in malformed)
runtimes=[f['content'] for a in d['assets'] for f in a.get('files',[]) if f['path']=='offline_runtime.py']
assert len(set(runtimes))==1
assert all('healthcheck=svc.get("healthcheck")' in s and 'urllib.request' not in s for s in runtimes)
print('Repair smoke checks PASS; datasets, Python syntax, Google fixture binding, empty matrices, configured health retries/success and shared-copy consistency checked.')
