import json, ast, copy
from pathlib import Path
p=Path('batches/final_batch_learn_python.region.02_1/interactions.json')
x=json.loads(p.read_text()); before=copy.deepcopy(x)
prompts={
('027_028','s07'): 'Keep the supplied labels and loop unchanged. Set numbered_labels using enumerate so the loop obtains each label together with a counter starting at one.',
('029_029','s03'): 'Keep the numeric inputs and supplied comparisons unchanged. Choose positive_tolerance from the supplied values so the near-zero comparison accepts the small nonzero difference. The checker reads False, True, True on three separate lines.',
('032_034','s04'): 'Keep the supplied order structure and bracket-selection assignment unchanged. Choose replacement_quantity from the supplied quantity values so only the second quantity of the first order becomes 5. Preserve the surrounding list and dictionary.',
('032_034','s07'): 'Keep rows unchanged. Write an outer for row in rows: loop and an indented inner for cell in row: loop. Print each cell once on its own line, completing each row before advancing to the next.',
('032_034','s11'): 'Keep the supplied inputs and loop unchanged. Set positions using range so the loop prints every second position starting at zero, excludes limit, and prints each selected position once on its own line.',
('038_040','s08'): 'Keep quantity unchanged. Write cost = quantity * 4 as the next top-level statement. Before running, predict quantity and cost and explain which current binding the expression uses. The checker reads quantity and cost; no printed output is required.',
('045_045','s05'): 'Keep text unchanged. Assign its UTF-8 encoding to payload, decode payload using UTF-8 into restored, and assign restored == text to matches. The checker reads payload, restored, and matches; no printed output is required.'}
for t in x['tiles']:
 for e in t['interactions']:
  key=(t['tile_id'].split('.')[-1],e['step_id'].split('.')[-1])
  if key not in prompts:continue
  i=e['interaction'];i['public']['prompt']=prompts[key]
  starter=i['public']['workspace']['files'][0];solution=i['grading']['solution_files'][0]
  if key==('032_034','s07'):
   lines=solution['content'].splitlines(keepends=True)
   rowline=next(l for l in lines if l.startswith('input_rows = ')).replace('input_rows = ','rows = ',1)
   scaffold=''.join(lines[:4])+rowline
   starter['content']=scaffold
   solution['content']=scaffold+''.join(lines[next(n for n,l in enumerate(lines) if l.startswith('for row in rows:')):])
  elif key==('038_040','s08'):
   lines=solution['content'].splitlines(keepends=True)
   binding=lines[0].replace('supplied_quantity = ','quantity = ',1)
   starter['content']=binding;solution['content']=binding+lines[-1]
  elif key==('045_045','s05'):
   lines=solution['content'].splitlines(keepends=True)
   encoding=lines[1].split(' = ',1)[1].strip()
   starter['content']=lines[0]
   solution['content']=lines[0]+''.join(lines[2:]).replace('(encoding)','('+encoding+')')
# Ensure only named fields changed and tests/anchors remain byte-equivalent data.
changes=[]
def diff(a,b,path=()):
 if isinstance(a,dict):
  assert a.keys()==b.keys()
  for k in a:diff(a[k],b[k],path+(k,))
 elif isinstance(a,list):
  assert len(a)==len(b)
  for n,(v,w) in enumerate(zip(a,b)):diff(v,w,path+(n,))
 elif a!=b:changes.append(path)
diff(before,x)
assert len(changes)==13,changes
for path in changes: assert path[-1] in ('prompt','content'),path
p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
print('Patched',len(prompts),'interactions;',len(changes),'fields')
print('Counts',len(x['tiles']),'tiles',sum(len(t['interactions']) for t in x['tiles']),'interactions')
