import contextlib, copy, inspect, io, json
from pathlib import Path
p=Path('batches/final_batch_learn_python.region.02_2/screens.json')
d=json.loads(p.read_text()); before=copy.deepcopy(d)
steps={s['step_id']:s for t in d['tiles'] for s in t['steps']}
def walks(tile,step):return [b for b in steps[f'learn_python.tile.{tile}.{step}']['blocks'] if b['type']=='code_walkthrough']
def run(b):
 out=io.StringIO(); ns={}
 with contextlib.redirect_stdout(out):exec(b['code'],ns)
 return out.getvalue().splitlines(),ns
def add(b,line,text):b['annotations'].append(dict(start_line=line,end_line=line,text=text))
def replace(b,line,text):
 a=[a for a in b['annotations'] if a['start_line']==line and a['end_line']==line];assert len(a)==1;a[0]['text']=text
b=walks('046_046','s01')[0];out,_=run(b)
add(b,4,'Output: '+', then '.join(out)+'. No pencil line is printed because zip stops at the shorter quantities list.')
bs=walks('047_048','s06')
for b,lines,suffixes in zip(bs,[(3,5,8),(4,5),(3,4)],[('','',''),('','. The guarded body does not run.'),('','. Blue was encountered first.')]):
 out,_=run(b);assert len(out)==len(lines)
 for line,value,suffix in zip(lines,out,suffixes):add(b,line,'Output: '+value+suffix)
b=walks('049_050','s01')[0];out,_=run(b)
for line,value in zip((3,5),out):
 a=next(a for a in b['annotations'] if a['start_line']==line)
 replace(b,line,a['text']+' Output: '+value)
b=walks('049_050','s06')[0];_,ns=run(b);f=ns['cost'];doc=inspect.getdoc(f).splitlines()
replace(b,9,'Help displays the signature '+f.__name__+str(inspect.signature(f))+' and the documentation: '+doc[0]+' [blank line] '+' '.join(doc[2:]))
# Repair scope: no fields other than these four visuals' annotations changed.
x=copy.deepcopy(d)
for tile,step in [('046_046','s01'),('047_048','s06'),('049_050','s01'),('049_050','s06')]:
 sid=f'learn_python.tile.{tile}.{step}'
 for t,old_t in zip(x['tiles'],before['tiles']):
  for s,old_s in zip(t['steps'],old_t['steps']):
   if s['step_id']==sid:
    for b,old_b in zip(s['blocks'],old_s['blocks']):
     if b['type']=='code_walkthrough':b['annotations']=old_b['annotations']
assert x==before
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Patched 11 annotations across 4 steps / 6 visuals')
print('Tiles',len(d['tiles']),'planned steps',sum(len(t['steps']) for t in d['tiles']),'remediation steps',sum(len(t.get('remediation_steps',[])) for t in d['tiles']))
