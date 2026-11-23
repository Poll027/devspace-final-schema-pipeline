import json
from pathlib import Path
path=Path('batches/final_batch_readiness/interactions.json')
old=json.loads(path.read_text()); data=json.loads(path.read_text())
def ix(tile,step):
    return next(i['interaction'] for t in data['tiles'] if t['tile_id']==tile for i in t['interactions'] if i['step_id']==tile+'.'+step)
ix('tile_090','s06')['feedback']['hints']=['Bind request writes and test reads to the same connection; verify rollback and override restoration in both test orders and after an injected failure.']
ix('tile_091','s09')['feedback']['hints']=['Compare every SecurityScopes requirement with the verified token scopes; confirm missing permission returns 403 without changing the order.']
i=ix('tile_093','s04')
needle=" and probe['commits']==2"
for files in [i['public']['workspace']['files'],i['grading']['solution_files']]:
    changed=0
    for f in files:
        if needle in f['content']:
            assert f['content'].count(needle)==1
            f['content']=f['content'].replace(needle,'')
            changed+=1
    assert changed==1
# Limit edits to exactly the three repair targets and named fields.
for ot,nt in zip(old['tiles'],data['tiles']):
    for oi,ni in zip(ot['interactions'],nt['interactions']):
        if oi!=ni:
            assert (nt['tile_id'],ni['step_id']) in {
                ('tile_090','tile_090.s06'),('tile_091','tile_091.s09'),('tile_093','tile_093.s04')}
            print('Changed',ni['step_id'])
path.write_text(json.dumps(data,indent=2)+'\n')
print('tiles',len(data['tiles']))
from collections import Counter
print('interaction counts',dict(Counter(i['interaction']['type'] for t in data['tiles'] for i in t['interactions'])))
