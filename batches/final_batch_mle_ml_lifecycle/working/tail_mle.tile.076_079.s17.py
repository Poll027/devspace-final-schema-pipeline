trigger_event_type = "artifact_ready"
selected_case = 'accepted'
import os
from pathlib import Path
for path, content in support_files.items():
    os.makedirs(os.path.dirname(path) or ".",exist_ok=True)
    Path(path).write_text(content)
import yaml
import hashlib
from storage_sim import RecoverableFailure, PreconditionFailed
from support import read, inject, record_failure, apply_recovery, validate_output, recovery_suite
Path("gate_impl.py").write_text("def verify(context, output, blob):\n    blob.reload()\n    data=blob.download_as_bytes(if_generation_match=blob.generation)\n    expected=context['contract']['outputs'][output]\n    assert hashlib.sha256(data).hexdigest()==expected['sha256']\n    assert validate_output(context,output)\n    return {'generation':blob.generation,'sha256':hashlib.sha256(data).hexdigest(),'validation_ok':True}\n\n\ndef reconcile_outputs(context):\n    try:\n        inject(context)\n    except RecoverableFailure as error:\n        record_failure(context,error)\n        apply_recovery(context)\n    verified={}\n    for output in context['contract']['outputs']:\n        blob=context['client'].blob(output)\n        if not blob.exists():\n            try:\n                blob.upload_from_filename('outputs/'+output+'.txt',if_generation_match=0)\n            except PreconditionFailed:\n                blob.reload()\n        verified[output]=verify(context,output,blob)\n    return verified\n\n\ndef ignore_failure(context):\n    return {}\n")
exec(Path("gate_impl.py").read_text())
recover = reconcile_outputs
config=read('cloudbuild.yaml')
config['steps'][1]['waitFor']=['recovery']
config['steps'][2]['waitFor']=['required_validation']
with open('resolved.yaml','w') as file_handle:
    yaml.safe_dump(config,file_handle)
with open('resolved.yaml') as file_handle:
    resolved=yaml.safe_load(file_handle)
report=recovery_suite(resolved,recover,selected_case,trigger_event_type)
assert report['runs']['accepted']['steps'][2]['status']=='SUCCESS'
assert report['runs']['rejected_gate']['steps'][1]['status']=='FAILURE'
assert report['runs']['rejected_gate']['steps'][2]['status']=='SKIPPED'
assert not report['outcomes']['invalid_existing']['first']['accepted']
assert not report['outcomes']['conflicting_content']['first']['accepted']
assert not report['outcomes']['unrelated_failure']['first']['accepted']
