import ast, copy, json, re
from pathlib import Path
B=Path('batches/final_batch_mle.region.data_readiness')
p=B/'interactions.json'; d=json.loads(p.read_text()); before=copy.deepcopy(d)
ix={e['step_id']:e['interaction'] for t in d['tiles'] for e in t['interactions']}
def get(s): return ix['mle.tile.'+s]
requests={
'001_003.s05':('inspect','Write the NumPy import, implement `inspect(fixture)`, and write `learner_checks()` under the contract below. Keep the checking scaffolding unchanged.'),
'001_003.s10':('compare','Write the NumPy import and implement `compare(reference, candidates, tolerance, budget)` under the contract below. Keep `evaluate` unchanged.'),
'001_003.s16':('transform','Write the NumPy import and implement `transform(fixture)`, including an independent list-comprehension reference, an intended-shape assertion and an agreement check with `rtol=1e-7` and `atol=1e-9`.'),
'004_006.s11':('scan','Write the pandas import and implement `scan(path, budget, feature_count, element_width, declared_types)` under the contract below. Keep `evaluate` unchanged.'),
'004_006.s16':('readiness','Write the NumPy import and implement `readiness(columns, numeric_values, ddof=0)` under the contract below. Keep `evaluate` unchanged.'),
'007_008.s05':('validate','Write the pandas import, implement `validate(table)`, and write `learner_checks()` under the contract below. Keep the checking scaffolding unchanged.'),
'007_008.s10':('clean_orders','Implement `clean_orders(records, policy)` and write `learner_checks()` under the contract below. Keep the checking scaffolding unchanged.'),
'009_011.s06':('evaluate_statistics','Write the NumPy import and implement `evaluate_statistics(fixture)` under the contract below.'),
'009_011.s11':('audit','Implement `audit(observations, labels, boundary)` and write `learner_checks()` using the supplied acceptance predicates. Keep the checking scaffolding unchanged.'),
'009_011.s16':('partition','Implement `partition(records, scenario, training_groups, cutoff, end)` and write `learner_checks()` under the contract below. Keep the checking scaffolding unchanged.'),
'012_015.s05':('replace_missing','Write the NumPy and SimpleImputer imports, implement `replace_missing(train, validation, single_missing)`, and write `learner_checks()` under the contract below.'),
'012_015.s11':('scale','Write the NumPy and StandardScaler imports, implement `scale(train, validation)`, and write `learner_checks()` under the contract below.'),
'012_015.s16':('encode','Write the NumPy and OneHotEncoder imports, implement `encode(training, cases, policy)`, and write `learner_checks()` under the contract below.'),
'016_017.s05':('corrected','Implement `corrected(training, held_out, preprocessor, predictor)` and write `boundary_check(...)` under the contract below. Keep the trace interfaces and leaked variant unchanged.'),
'016_017.s11':('feature','Write the datetime import, implement `feature(records, prediction_time)`, and write `learner_checks()` under the contract below. The supplied adapter passes datetime-valued timestamps.'),
'018_018.s05':('permitted_record','Implement `permitted_record(identity, sample, permitted_fields)` under the contract below. Keep the authorized runtime interfaces and `evaluate` unchanged.')}

def patch_source(src, name, starter):
    lines=src.splitlines(keepends=True); changes=[]
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.FunctionDef) and n.name in ['supplied_'+name+'_workflow','learner_checks','boundary_check']:
            if starter:
                header=lines[n.lineno-1].replace('supplied_'+name+'_workflow',name)
                changes.append((n.lineno-1,n.end_lineno,header+' '*(n.col_offset+4)+'# TODO: implement the contract and checks.\n'+' '*(n.col_offset+4)+'raise NotImplementedError\n'))
            elif n.name=='supplied_'+name+'_workflow':
                changes.append((n.lineno-1,n.lineno,lines[n.lineno-1].replace(n.name,name)))
        if isinstance(n,(ast.Import,ast.ImportFrom)) and n.col_offset==0 and starter:
            changes.append((n.lineno-1,n.end_lineno,'# TODO: write the required import.\n'))
    for start,end,text in sorted(changes,reverse=True):lines[start:end]=[text]
    src=''.join(lines)
    src=src.split('# Supplied inactive entry point; activate the workflow below.')[0].rstrip()+'\n'
    return src

for s,(name,instruction) in requests.items():
    i=get(s); contract=i['public']['prompt'].split('Contract: ',1)[1]
    i['public']['prompt']=instruction+'\n\nContract: '+contract
    for f in i['public']['workspace']['files']:f['content']=patch_source(f['content'],name,True)
    for f in i['grading']['solution_files']:f['content']=patch_source(f['content'],name,False)

# Explicit shape in the independent-reference solution.
i=get('001_003.s16'); f=i['grading']['solution_files'][0]
f['content']=f['content'].replace('assert result.shape == a.shape','assert result.shape == (len(fixture), 2)')

# Pin schemas by quoting their existing return keys/justifications, not introducing new fields.
for s,name in [('001_003.s10','compare'),('009_011.s11','audit'),('012_015.s05','replace_missing'),('012_015.s11','scale')]:
    i=get(s); src=i['grading']['solution_files'][0]['content']; tree=ast.parse(src)
    func=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name==name)
    keys=[]
    for n in ast.walk(func):
        if isinstance(n,ast.Dict):
            for k in n.keys:
                if isinstance(k,ast.Constant) and isinstance(k.value,str) and k.value not in keys:keys.append(k.value)
    i['public']['prompt']+='\n'+('Each candidate report' if name=='compare' else 'The returned report')+' must contain these fields: '+', '.join('`'+k+'`' for k in keys)+'.'

get('004_006.s16')['public']['prompt']+=' Use the caller-selected ddof: divide by N-ddof for each feature, with ddof=0 by default and ddof=1 when requested.'
i=get('009_011.s06');src=i['grading']['solution_files'][0]['content'];tree=ast.parse(src)
returns=[n for n in ast.walk(tree) if isinstance(n,ast.Return) and isinstance(n.value,ast.List)]
ordered=ast.unparse(returns[-1].value)
strings=[n.value for n in ast.walk(tree) if isinstance(n,ast.Constant) and isinstance(n.value,str) and 'counts do not identify a cause' in n.value]
i['public']['prompt']=i['public']['prompt'].replace('Return the existing ordered fields and a count-supported limitation without asserting an unobserved cause or inevitable prediction failure.',f'Return `{ordered}`. For the supplied positive-denominator fixture, use limitation exactly {strings[0]!r}. For the supplied zero-category-denominator fixture, use exactly {strings[1]!r}.')
i=get('009_011.s16');i['public']['prompt']+=' Group validation contains records whose groups are not in training_groups. Preserve input order in both partitions. Return keys training, validation, training_proportion, validation_proportion and justification. Use justification exactly \'disjoint groups\' for group splits and \'training before cutoff; validation in later interval\' for time splits.'

# Add the unexpected-column rejection fixture and tests; compute expected by running the reference.
i=get('007_008.s05');fixture=copy.deepcopy(i['grading']['tests'][0]['spec']['args'][0])
fixture['columns'].append('extra')
for row in fixture['rows']:row.append(0)
runtime=json.loads((B/'scratch/authoring_expected.json').read_text())
expected=runtime['schema']
node=next(n for n in ast.walk(ast.parse(i['grading']['solution_files'][0]['content'])) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CHECK_FIXTURES' for t in n.targets))
index=len(ast.literal_eval(node.value))
for f in i['public']['workspace']['files']+i['grading']['solution_files']:
    text=f['content'];node=next(n for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CHECK_FIXTURES' for t in n.targets))
    fixtures=ast.literal_eval(node.value)+[[fixture]]
    ls=text.splitlines(keepends=True);ls[node.lineno-1:node.end_lineno]=[' '*node.col_offset+'CHECK_FIXTURES = '+repr(fixtures)+'\n'];f['content']=''.join(ls)
    if f in i['grading']['solution_files']:f['content']+=f'\n# Unexpected-column fixture rejection and nonmutation.\n' # assertion inserted into learner checks below
# insert into learner_checks rather than standalone
f=i['grading']['solution_files'][0];n=next(n for n in ast.walk(ast.parse(f['content'])) if isinstance(n,ast.FunctionDef) and n.name=='learner_checks');ls=f['content'].splitlines(keepends=True);ls.insert(n.end_lineno,' '*(n.col_offset+4)+f'assert check_fixture({index}, {expected!r})\n');f['content']=''.join(ls)
for function in ['evaluate','run_checks']:
    test=copy.deepcopy(next(t for t in i['grading']['tests'] if t['spec'].get('function')==function));test['test_id']='unexpected_columns_'+function;test['spec']['args']=[fixture];test['spec']['expected']=expected;i['grading']['tests'].append(test)

# Deliberately incorrect checks now expect wrong computed replacement/transformed values.
for s,field in [('012_015.s05','single_missing'),('012_015.s11','validation')]:
    i=get(s);f=i['grading']['solution_files'][0];src=f['content'];tree=ast.parse(src)
    checks=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='learner_checks')
    calls=[n for n in ast.walk(checks) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='check_fixture' and len(n.args)>1 and isinstance(n.args[1],ast.Dict) and n.args[1].keys]
    correct=ast.literal_eval(calls[0].args[1]); wrong=copy.deepcopy(correct);wrong[field][0][0]+=1
    f['content']=src.replace('assert check_fixture(0, {})','assert check_fixture(0, '+repr(wrong)+')',1)

# Chunk expectation comes from the registered mounted data through the reference code.
i=get('004_006.s11')
t=next(t for t in i['grading']['tests'] if t['test_id']=='t1')
t['spec']['expected']=runtime['chunk']
registry=json.loads((B/'scenario_asset_registry.json').read_text())

# Existing choice now asks about the complete record, preserving the input restriction.
i=get('000_000.s05');oldmeasure=copy.deepcopy(get('000_000.s06')['measures'][0]);i['measures'].insert(0,oldmeasure)
i['anchors'].insert(0,'mle.prediction_task_definition#assessment:'+oldmeasure['capability'])
asset=next(a for a in registry['assets'] if a['asset_id']=='ds.outcome_counts'); cols=[c['name'] for c in asset['columns']]; row=dict(zip(cols,asset['rows'][0]));N=row['population_count'];h=row['horizon_minutes']
correct=f'Unit: one order at acceptance; population: all {N} supplied accepted orders; target: arrival more than {h} minutes after acceptance; prediction time: acceptance; horizon: {h} minutes; inputs: distance and promised delivery zone; exclude eventual arrival time.'
i['public']['prompt']=f'The supplied population contains {N} accepted orders. Predictions are made at acceptance for arrival more than {h} minutes later. Distance and promised delivery zone are known at acceptance; eventual arrival time is recorded later. Which complete task record correctly defines the unit, population, target, prediction time, horizon and permitted inputs?'
i['public']['options']=[{'option_id':'correct','text':correct},{'option_id':'wrong1','text':correct.replace('inputs: distance and promised delivery zone; exclude eventual arrival time.','inputs: distance, promised delivery zone and eventual arrival time.')},{'option_id':'wrong2','text':correct.replace('target: arrival more than','target: arrival no more than')}]
i['grading']['option_feedback']={'correct':{'message':'The record separates the order-level unit, target and horizon, and uses only inputs available at acceptance.'},'wrong1':{'message':'Eventual arrival is recorded later and cannot be an input at acceptance.'},'wrong2':{'message':'This reverses the stated target event: the task concerns arrival more than the horizon after acceptance.'}}

for s,hint in [('004_006.s15','Read the shape in the declared order: observation axis first, feature axis second.'),('007_008.s09','An assert checks its predicate; it does not perform a cleaning action.'),('009_011.s10','A deliberately wrong expected verdict should make the assertion predicate false.')]:get(s)['feedback']['hints']=[hint]

changed=[s for s in ix if ix[s]!=next(e['interaction'] for t in before['tiles'] for e in t['interactions'] if e['step_id']==s)]
assert get('000_000.s06')==before['tiles'][0]['interactions'][1]['interaction'] # unresolved human plan correction
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print('Changed',len(changed),'interactions:',changed)
print('Interactions',len(ix),'tiles',len(d['tiles']))
