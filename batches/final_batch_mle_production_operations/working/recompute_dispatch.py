import json,os,tempfile,shutil,traceback
from pathlib import Path
import numpy as np
B=Path('batches/final_batch_mle.region.production_operations').resolve();p=B/'interactions.json';d=json.loads(p.read_text())
def plain(v):
 if isinstance(v,dict):return {k:plain(x) for k,x in v.items()}
 if isinstance(v,(tuple,list)):return [plain(x) for x in v]
 if isinstance(v,np.ndarray):return v.tolist()
 if isinstance(v,np.generic):return v.item()
 return v
for t in d['tiles']:
 for x in t['interactions']:
  i=x['interaction'];k=x['step_id']
  if i['type']!='code_exercise':continue
  with tempfile.TemporaryDirectory(dir=B/'working') as tmp:
   for m in i['public']['workspace']['asset_mounts']:shutil.copyfile(B/'assets'/m['mount_path'],Path(tmp)/m['mount_path'])
   wd=os.getcwd();os.chdir(tmp)
   try:
    env={};exec(i['grading']['solution_files'][0]['content'],env)
    report=plain(env['report']);tests=i['grading']['tests'];tests[0]['spec']['expected']=report
    if k.endswith('080_082.s04'):
     tests=[tests[0],{'test_id':'single_emission','kind':'value_equals','spec':{'expr':'emitted_records','expected':plain(env['emitted_records'])}},{'test_id':'emitted_jsonl','kind':'value_equals','spec':{'expr':"[json.loads(line) for line in open('summary.jsonl')]",'expected':plain(env['emitted_records'])}}]
    if k.endswith('083_085.s06'):
     tests=[tests[0],{'test_id':'illustrative_cohort','kind':'value_equals','spec':{'expr':'illustrative_report','expected':plain(env['illustrative_report'])}}]
    if k.endswith('091_094.s14'):
     tests=[tests[0],{'test_id':'verification','kind':'value_equals','spec':{'expr':'verification','expected':plain(env['verification'])}}]
    i['grading']['tests']=tests
    print('OK',k)
   except Exception as e:print('FAIL',k,str(e));traceback.print_exc()
   finally:os.chdir(wd)
p.write_text(json.dumps(d,indent=2)+'\n')
