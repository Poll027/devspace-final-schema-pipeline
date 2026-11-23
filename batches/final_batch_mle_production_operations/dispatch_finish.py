import json,pathlib,ast
B=pathlib.Path(__file__).parent;P=B/'interactions.json';d=json.loads(P.read_text())
ix={r['step_id']:r['interaction'] for t in d['tiles'] for r in t['interactions']}
i=ix['mle.tile.091_094.s09']
# Grade the same supplied simulator on distinct sequences, including valid execution.
for t in i['grading']['tests']:
 if t['test_id'] in ['no_workload','no_stop']:
  call=ast.parse(t['spec']['expr'],mode='eval').body.value
  sequence=ast.literal_eval(call.args[0])
  t['kind']='function_call';t['spec']={'function':'simulate_sequences','args':[sequence]}
i['grading']['tests'].append({'test_id':'complete_lifecycle','kind':'function_call','spec':{'function':'simulate_sequences','args':[{'training':['describe','start','ssh','workload','stop','describe'],'inference':['describe','start','ssh','workload','stop','describe']}]},'visible':True,'message_on_fail':'Only complete approved sequences may verify stopped workloads.'})
i=ix['mle.tile.086_089.s16']
t=next(t for t in i['grading']['tests'] if t['test_id']=='unknown_response_durable_job')
# Return the persisted identity as well as the invariant, so the evidence changes with the event input.
t['spec']={'expr':"{'job_id':result['unknown_response']['result']['job_id'], 'jobs':result['unknown_response']['state']['jobs'], 'single_persisted_job':len(result['unknown_response']['state']['jobs']) == 1 and result['unknown_response']['result']['job_id'] in result['unknown_response']['state']['jobs']}"}
P.write_text(json.dumps(d,indent=2)+'\n')
