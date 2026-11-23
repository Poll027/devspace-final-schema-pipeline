import json,ast
from pathlib import Path
B=Path('batches/final_batch_mle.region.ml_lifecycle');P=B/'interactions.json';d=json.loads(P.read_text())
targets={'mle.tile.073_075.s05','mle.tile.073_075.s10','mle.tile.073_075.s17','mle.tile.076_079.s05','mle.tile.076_079.s17'}
for t in d['tiles']:
 for x in t['interactions']:
  tag=x['step_id']
  if tag not in targets:continue
  i=x['interaction'];ws=i['public']['workspace'];f=next(f for f in ws['files'] if f['path']==ws['entry']);s=f['content'];lines=s.splitlines(True)
  for n in reversed(ast.parse(s).body):
   if isinstance(n,ast.Import) and any(a.name in ['yaml','numpy','math','hashlib'] for a in n.names):
    lines[n.lineno-1:n.end_lineno]=['# TODO: write the required dependency imports.\n']
  f['content']=''.join(lines)
  if tag=='mle.tile.073_075.s17':
   i['public']['prompt']=i['public']['prompt'].replace('Calculate FPR=', 'Return error_rates as [FPR, FNR]. Calculate FPR=')
  if tag=='mle.tile.076_079.s17':
   sol=next(f for f in i['grading']['solution_files'] if f['path']==ws['entry'])
   sol['content']=sol['content'].replace("    assert hashlib.sha256(data).hexdigest() == expected['sha256']", "    assert blob.generation == expected['generation']\n    assert hashlib.sha256(data).hexdigest() == expected['sha256']")
P.write_text(json.dumps(d,indent=2)+'\n')
print('Updated import stubs, return contract and recovery generation assertion.')
