import json, copy, shutil
from pathlib import Path
B=Path('batches/final_batch_implementation')
p=B/'interactions.json'
d=json.loads(p.read_text()); before=copy.deepcopy(d)
i=next(i['interaction'] for t in d['tiles'] if t['tile_id']=='tile_037' for i in t['interactions'] if i['step_id']=='tile_037.s07')
start=i['public']['prompt'].index('In the supplied terminal,')
end=i['public']['prompt'].index('\n\nRelease requires',start)
i['public']['prompt']=i['public']['prompt'][:start]+'In the supplied terminal, work from the directory containing main.py. Leave main.py unchanged. Run uvicorn main:app --host 0.0.0.0 --port 8000 without --reload. Submit the executed run for verification.'+i['public']['prompt'][end:]
# Only the inactive pinned prompt changes; keep the explicit publication hold.
oldi=next(i['interaction'] for t in before['tiles'] if t['tile_id']=='tile_037' for i in t['interactions'] if i['step_id']=='tile_037.s07')
oldi['public']['prompt']=i['public']['prompt'];assert before==d
p.write_text(json.dumps(d,indent=2)+'\n')
from collections import Counter
print('tiles',len(d['tiles']),'interactions',sum(len(t['interactions']) for t in d['tiles']),Counter(i['interaction']['type'] for t in d['tiles'] for i in t['interactions']))
G=B/'scratch_s07_pinned_prompt_current_gate';G.mkdir(exist_ok=True)
for name in ['batch_run_context.json','tile_plans.json','scenario_asset_registry.json','screens.json','interactions.json']:
 shutil.copy2(B/name,G/name)
shutil.copytree(B/'inputs',G/'inputs',dirs_exist_ok=True)
