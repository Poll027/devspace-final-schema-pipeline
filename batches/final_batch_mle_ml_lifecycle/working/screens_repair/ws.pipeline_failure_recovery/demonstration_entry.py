import json, sys, math, hashlib
from pathlib import Path
load = lambda p: json.loads(Path(p).read_text())

from storage_sim import StorageClient, RecoverableFailure, PreconditionFailed
case_id=sys.argv[1]; stage=sys.argv[2]; case=load('fixtures/recovery_cases.json')[case_id]
contract=load('fixtures/recovery_contract.json'); state_path=Path('state.'+case_id+'.json')
if not state_path.exists():
 state={'objects':{k:{'generation':contract['outputs'][k]['generation'],'data':Path('outputs/'+k+'.txt').read_text()} for k in case['initial_outputs']},'uploads':[], 'invocations':0}
else: state=load(state_path)
client=StorageClient({k:{'generation':v['generation'],'data':v['data'].encode()} for k,v in state['objects'].items()})
def inspect():
 result={}
 for k, expected in contract['outputs'].items():
  b=client.blob(k); exists=b.exists()
  if exists:
   b.reload(); digest=hashlib.sha256(b.download_as_bytes(if_generation_match=b.generation)).hexdigest()
   result[k]={'exists':True,'generation':b.generation,'sha256':digest,'validation_ok':digest==expected['sha256'] and expected['validation_ok']}
  else: result[k]={'exists':False,'generation':None,'sha256':None,'validation_ok':False}
 return result
before=inspect()
if stage=='recovery':
 for k, expected in contract['outputs'].items():
  b=client.blob(k)
  if b.exists():
   if not inspect()[k]['validation_ok']: raise ValueError('invalid completed artifact '+k)
  else:
   try: b.upload_from_filename('outputs/'+k+'.txt',if_generation_match=0)
   except PreconditionFailed:
    if not inspect()[k]['validation_ok']: raise ValueError('conflicting artifact '+k)
 state['invocations']+=1; state['uploads']+=client.uploads
 state['objects']={k:{'generation':v['generation'],'data':v['data'].decode()} for k,v in client.objects.items()}
 state_path.write_text(json.dumps(state))
passed=all(v['validation_ok'] for v in inspect().values()) and (stage=='recovery' or case['gate_ok'])
print(json.dumps({'stage':stage,'before':before,'after':inspect(),'upload_count':len(state['uploads']),'uploads':state['uploads'],'invocations':state['invocations'],'required_validation_ok':all(v['validation_ok'] for v in inspect().values()) and case['gate_ok']}))
sys.exit(not passed)
