import json, sys, math, hashlib
from pathlib import Path
load = lambda p: json.loads(Path(p).read_text())

from storage_sim import StorageClient, RecoverableFailure
client=StorageClient()
try:
 client.blob('A').upload_from_filename('outputs/A.txt',if_generation_match=0)
 raise RecoverableFailure('injected after A upload, before B')
except RecoverableFailure as e:
 state={'objects':{k:{'generation':v['generation'],'data':v['data'].decode()} for k,v in client.objects.items()},'uploads':client.uploads,'invocations':0}
 Path('state.'+sys.argv[1]+'.json').write_text(json.dumps(state))
 print(json.dumps({'failure':str(e),'exception':type(e).__name__,'A':{'exists':True,'generation':client.objects['A']['generation'],'sha256':hashlib.sha256(client.objects['A']['data']).hexdigest()},'B':{'exists':False,'generation':None,'sha256':None}}))
 sys.exit(1)
