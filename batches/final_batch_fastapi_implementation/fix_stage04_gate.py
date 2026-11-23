import json
from pathlib import Path
B=Path(__file__).parent;x=json.loads((B/'interactions.json').read_text())
for t in x['tiles']:
 for e in t['interactions']:
  i=e['interaction']
  if e['step_id']=='tile_022.s04':
   fields=['orders_collection_path','orders_item_path','orders_retrieve_method','orders_create_method','orders_replace_method','orders_remove_method','orders_created_location','orders_created_status','orders_absent_status']
   old=i['grading']['solution_files'][0]['content'];ns={};exec(old,ns)
   scaffold=''.join('supplied_'+name+' = '+repr(ns[name])+'\n' for name in fields)
   inspector='\n# Supplied contract inspector.\ninspect_contract = lambda section: ['+', '.join(fields[:6])+'] if section == "identity_and_methods" else ['+', '.join(fields[6:])+']\n'
   starter=scaffold+''.join(name+': '+('int' if isinstance(ns[name],int) else 'str')+' = '+repr(0 if isinstance(ns[name],int) else '')+'\n' for name in fields)+inspector
   solution=scaffold+''.join(name+': '+('int' if isinstance(ns[name],int) else 'str')+' = supplied_'+name+'\n' for name in fields)+inspector
   i['public']['workspace']['files'][0]['content']=starter;i['grading']['solution_files'][0]['content']=solution
   i['public']['prompt']+=' The supplied_* variables provide the literal contract values; complete each annotated orders_* assignment by copying its matching supplied_* value. Keep the supplied literals and inspector unchanged.'
  if e['step_id']=='tile_025.s06':
   for f in [i['public']['workspace']['files'][0],i['grading']['solution_files'][0]]:
    s=f['content'].replace('httpx.AsyncClient = SuppliedClient','from types import SimpleNamespace\nhttpx = SimpleNamespace(AsyncClient=SuppliedClient)')
    # Retain the real library for response/transport creation inside the fixture class.
    s=s.replace('import httpx\n','import httpx as _httpx\n').replace('_RealClient = httpx.AsyncClient','_RealClient = _httpx.AsyncClient').replace('return httpx.Response','return _httpx.Response').replace('transport=httpx.MockTransport','transport=_httpx.MockTransport')
    s=s.replace('@app.get("/fixture")\nasync def run_fixture():\n    events.clear()\n    await orders()\n    return events','class SuppliedBridge:\n    async def run_fixture():\n        events.clear()\n        await orders()\n        return list(events)\napp.add_api_route("/fixture", SuppliedBridge.run_fixture, methods=["GET"])')
    f['content']=s
   i['public']['prompt']+=' The supplied httpx facade constructs real HTTPX clients with the synthetic transport; it does not replace the server bridge client.'
(B/'interactions.json').write_text(json.dumps(x,indent=2)+'\n')
