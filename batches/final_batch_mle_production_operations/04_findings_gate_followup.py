import ast,json,copy,os,tempfile
from pathlib import Path
B=Path('batches/final_batch_mle.region.production_operations');P=B/'interactions.json'
d=json.loads(P.read_text());ix={e['step_id']:e['interaction'] for t in d['tiles'] for e in t['interactions']}
# Retain a mutable run-key fixture input so the existing report test remains data-sensitive.
i=ix['mle.tile.086_089.s16']
code=i['grading']['solution_files'][0]['content'];ns={}
prefix=ast.literal_eval(ast.parse(code).body[0].value.args[0])
policy_node=next(n for n in ast.parse(prefix).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='policy' for t in n.targets))
policy=ast.literal_eval(policy_node.value)
for f in [i['public']['workspace']['files'][0],i['grading']['solution_files'][0]]:
 code=f['content'];n=ast.parse(code).body[0];pref=ast.literal_eval(n.value.args[0]);pref+="policy['event']['run_key']=event_run_key\n"
 f['content']='event_run_key = '+repr(policy['event']['run_key'])+'\nexec('+repr(pref)+')'+code[n.end_col_offset+sum(len(l)+1 for l in code.splitlines()[:n.end_lineno-1]):] if False else 'event_run_key = '+repr(policy['event']['run_key'])+'\nexec('+repr(pref)+')\n'+'\n'.join(code.splitlines()[n.end_lineno:])+'\n'
# New count test includes the persisted run key, not only an invariant Boolean.
t=next(t for t in i['grading']['tests'] if t['test_id']=='overlap_logical_jobs');t['spec']['expr']="{'counts':logical_job_counts,'run_key':policy['event']['run_key']}"
# Execute solutions natively against registry-selected mounts solely to derive new test values.
registry=json.loads((B/'scenario_asset_registry.json').read_text());assets={a['asset_id']:a for a in registry['assets']}
import sys
sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts')
from checkers import sandbox as sb
def probe(i,expr):
 tables,_=sb._tables(registry,i['public']['workspace'].get('asset_mounts',[]),{},[])
 sc=sb._py_script('solution',i['public']['workspace']['entry'],i['grading']['solution_files'][0]['content'],sb._py_mounts(tables),[{'id':'value','kind':'expr','expr':expr}])
 result=sb.node_run(sb._py_job('python',i['public']['runtime'].get('packages',[]),[sc]),sb.RUNTIMES['python']['runner'])['results']['solution']
 assert result['ok'],result
 assert result['probes']['value']['ok'],result
 return result['probes']['value']['value']
t['spec']['expected']=probe(i,t['spec']['expr'])
i=ix['mle.tile.083_085.s06']
values=probe(i,"{'duplicates':outside_duplicate_rows,'labels':label_rows,'expected':quality(outside_duplicate_rows,label_rows),'control':quality([outside_prediction],[])}")
t=next(t for t in i['grading']['tests'] if t['test_id']=='excluded_prediction_duplicates');t['kind']='function_call';t['spec']={'function':'quality','args':[values['duplicates'],values['labels']],'expected':values['expected']}
nt=copy.deepcopy(t);nt['test_id']='excluded_prediction_control';nt['spec']={'function':'quality','args':[[values['duplicates'][0]],[]],'expected':values['control']};i['grading']['tests'].append(nt)
P.write_text(json.dumps(d,indent=2)+'\n')
print('Updated mutation-sensitive fixtures and derived function-test expectations')
