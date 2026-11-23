import json, pathlib, os, sys, hashlib
B=pathlib.Path('batches/final_batch_readiness').resolve()
d=json.loads((B/'scenario_asset_registry.json').read_text())
# Structural dataset/variant checks are also covered by the deterministic gate.
for a in d['assets']:
    if a['asset_kind']=='dataset':
        cols=a['columns']
        assert all(len(r)==len(cols) for r in a['rows']),a['asset_id']
        assert all(c.get('semantic_role') for c in cols),a['asset_id']
    elif a['asset_kind']=='code_workspace':
        for f in a['files']:
            if f['path'].endswith('.py'):compile(f['content'],f['path'],'exec')
a=next(a for a in d['assets'] if a['asset_id']=='ws.auth.authorization_server_integration')
work=B/'working/repair_provisioned/auth_check';work.mkdir(exist_ok=True)
for f in a['files']:(work/f['path']).write_text(f['content'])
sys.path.insert(0,str(B/'working/repair_runtime'));sys.path.insert(0,str(work));os.chdir(work)
from acquisition_harness import AcquisitionHarness
from application import app,existing_verifier
from fastapi.testclient import TestClient
configuration=json.loads(pathlib.Path('issuer_configuration.json').read_text())
existing_verifier.configure(configuration)
token=AcquisitionHarness(configuration).acquire()
with TestClient(app) as client:
    accepted=client.get('/protected',headers={'Authorization':'Bearer '+token})
    prefix,signature=token.rsplit('.',1)
    tampered=prefix+'.'+('A' if signature[0]!='A' else 'B')+signature[1:]
    rejected=client.get('/protected',headers={'Authorization':'Bearer '+tampered})
    missing=client.get('/protected')
    assert accepted.is_success and rejected.status_code==401 and missing.status_code==401
# No learner integration settings/assertions have been completed or overridden.
assert not app.dependency_overrides
report={'compiled_python_files':sum(f['path'].endswith('.py') for a in d['assets'] if a['asset_kind']=='code_workspace' for f in a['files']), 'publisher_only_http_check':{'acceptance':accepted.status_code,'tampered_rejection':rejected.status_code,'missing_bearer_rejection':missing.status_code,'authentication_overrides':False},'mistakes_to_avoid':'Gate checks dataset widths/types/semantic roles and variant predicates. Repair leaves dataset values/roles/variants and glossary contracts unchanged. Workspaces compile; captured SQL and results derive from unchanged starter and fixtures, and captured audit source hashes derive from bundled files.'}
(B/'working/repair_self_check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
