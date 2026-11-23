import copy,json
from pathlib import Path
p=Path('batches/final_batch_aws_devops.region.06_1/interactions.json')
d=json.loads(p.read_text()); old=copy.deepcopy(d)
entries={i['step_id']:i['interaction'] for t in d['tiles'] for i in t['interactions']}
for sid,count,label in [('aws_devops.tile.103.s04',6,'scope and ordering context'),('aws_devops.tile.110.s04',4,'backend and migration context')]:
 pub=entries[sid]['public']; items=pub['items'][:count]
 prefix=items[0]['text'].split('```text',1)[0]
 assert prefix and all(it['text'].startswith(prefix) for it in items)
 ids=', '.join(it['item_id'] for it in items)
 pub['prompt']+='\n\nShared '+label+' — applies to all '+str(count)+' original records ('+ids+'), not to the independent alternate excerpts:\n'+prefix.rstrip()
 for it in items: it['text']=it['text'][len(prefix):]
pub=entries['aws_devops.tile.106.s06']['public']
pub['intro']+='\n\nThe tasks are grouped into two sections: “Successful step” and “Failed step.” In each section, select the entire step record first, preserving its execution, authority, target, times, inputs, outputs and failure details. Then select each named evidence cell from that same step record.'
for task in pub['tasks']:
 if task['target_kind']=='row':
  label='Successful step' if task['task_id'].endswith('0') else 'Failed step'
  task['prompt']='### '+label+'\nSelect the entire step record.'
 else:
  task['prompt']=task['prompt'].split('select the cell containing the ',1)[1].capitalize()
pub=entries['aws_devops.tile.108.s07']['public']
for item in pub['items']:
 text=item['text']
 if 'each shown date covers that interval.' in text:
  item['text']=text.replace('Version-specific retain-until dates were inspected against required_start_date and required_end_date; each shown date covers that interval.', 'Compare each version’s retain-until date with the supplied required interval.')
# Repair scope: only the four named public objects; every key and other field unchanged.
old_entries={i['step_id']:i['interaction'] for t in old['tiles'] for i in t['interactions']}
changed=[]
for sid,i in entries.items():
 before=old_entries[sid]
 if i!=before:
  changed.append(sid)
  assert {k:v for k,v in i.items() if k!='public'}=={k:v for k,v in before.items() if k!='public'}
  if sid!='aws_devops.tile.106.s06':
   for a,b in zip(i['public']['items'],before['public']['items']):
    assert {k:v for k,v in a.items() if k!='text'}=={k:v for k,v in b.items() if k!='text'}
  else:
   assert len(i['public']['tasks'])==len(before['public']['tasks'])
   for a,b in zip(i['public']['tasks'],before['public']['tasks']):
    assert {k:v for k,v in a.items() if k!='prompt'}=={k:v for k,v in b.items() if k!='prompt'}
assert set(changed)=={'aws_devops.tile.103.s04','aws_devops.tile.106.s06','aws_devops.tile.108.s07','aws_devops.tile.110.s04'}
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Patched:',', '.join(changed))
print('Tiles:',len(d['tiles']),'Interactions:',len(entries))
from collections import Counter
print('Types:',dict(Counter(i['type'] for i in entries.values())))
