import ast,json,re
from pathlib import Path
B=Path('batches/final_batch_mle.region.production_operations');p=B/'interactions.json';d=json.loads(p.read_text())
for t in d['tiles']:
 for x in t['interactions']:
  k=x['step_id'].removeprefix('mle.tile.');i=x['interaction']
  if k=='090_090.s05':
   i['public']['prompt']='Practice — Complete the symbolic action sequence under the supplied runbook and inspect the simulator’s recovery checks.\n\n'+i['public']['prompt']
  if k not in ['080_082.s04','083_085.s06','086_089.s16','086_089.s21','083_085.s16','091_094.s14']:continue
  sol=i['grading']['solution_files'][0];s=sol['content'];parts=[]
  for n in ast.parse(s).body:
   text=ast.get_source_segment(s,n)
   if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='exec' and isinstance(n.value.args[0],ast.Constant):
    inner=ast.literal_eval(n.value.args[0])
    if any('def '+name in inner for name in ['summarize','quality','supplied_admit','supplied_evaluate']):text=inner.replace('def supplied_admit','def admit').replace('def supplied_evaluate','def evaluate')
   if k in ['086_089.s16','086_089.s21'] and text in ['admit = supplied_admit','evaluate = supplied_evaluate']:continue
   if k=='083_085.s16':
    if text=='rollback_response = label_approved_rollback':continue
    text=text.replace('response = rollback_response','response = label_approved_rollback')
   if k=='091_094.s14':
    if re.match(r'^(safe_dump_interface|safe_load_interface|dump_config|load_config) =',text):continue
    text=text.replace('dump_config(config, h)','yaml.safe_dump(config, h)').replace('resolved = load_config(h)','resolved = yaml.safe_load(h)')
   parts.append(text)
  sol['content']='\n\n'.join(parts)+'\n';ast.parse(sol['content'])
  if k=='091_094.s14':
   f=i['public']['workspace']['files'][0];f['content']=f['content'].replace("'args': ['compute', 'instances', 'stop', None, None]", "'args': ['compute', 'instances', 'stop', None, '--zone=' + None]")
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
