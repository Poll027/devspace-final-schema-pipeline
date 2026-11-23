import json, ast, copy
from pathlib import Path
P=Path('batches/final_batch_readiness/interactions.json')
d=json.loads(P.read_text())
ix={x['step_id']:x['interaction'] for t in d['tiles'] for x in t['interactions']}
def sources(k):
 i=ix[k]
 return i['public']['workspace']['files']+i['grading'].get('solution_files',[])
def nested_patch(s,fn):
 tree=ast.parse(s); lines=s.splitlines(keepends=True); edits=[]
 for n in ast.walk(tree):
  if isinstance(n,ast.Assign) and any(isinstance(a,ast.Name) and a.id=='programs' for a in n.targets):
   programs=ast.literal_eval(n.value);fn(programs)
   edits.append((n.lineno-1,n.end_lineno,'programs = '+repr(programs)+'\n'))
 for a,b,r in reversed(edits):lines[a:b]=[r]
 return ''.join(lines)
def programs(k,fn):
 for f in sources(k):
  if f['path']=='exercise.py': f['content']=nested_patch(f['content'],fn)
def replace_exec(k,old,new):
 for f in sources(k):
  if f['path']!='exercise.py':continue
  s=f['content']; tree=ast.parse(s);lines=s.splitlines(keepends=True);edits=[]
  for n in ast.walk(tree):
   if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='exec':
    call=n.value
    if isinstance(call.args[0],ast.Constant) and old in call.args[0].value:
     a=call.args[0];v=a.value.replace(old,new)
     line=lines[a.lineno-1];lines[a.lineno-1]=line[:a.col_offset]+repr(v)+line[a.end_col_offset:]
  f['content']=''.join(lines)
# Release selection: remove helper-computed answer; authored dictionary and immutable records check.
k='tile_082.s04';i=ix[k]
i['public']['prompt']="Select the supplied compatible prior_release without modifying releases. Populate procedure with build = selected_release['artifact'], release = {'artifact': selected_release['artifact'], 'configuration': selected_release['configuration']}, run = selected_release['release_id'], and database_schema_after_rollback = current_schema. Keep the prior artifact and its recorded configuration together; application rollback leaves the current database schema unchanged."
for f in sources(k):
 if f['path']=='exercise.py':
  s=f['content']; start=s.index('exec(');s=s[:start]+s[s.index('selected_release =',start):];s=s.replace('procedure = rollback_procedure(selected_release)',"procedure = {'build': None, 'release': None, 'run': None, 'database_schema_after_rollback': None}")
  if f in i['grading']['solution_files']:
   s=s[:s.index('selected_release =')]+"selected_release = prior_release\nprocedure = {'build': selected_release['artifact'], 'release': {'artifact': selected_release['artifact'], 'configuration': selected_release['configuration']}, 'run': selected_release['release_id'], 'database_schema_after_rollback': current_schema}\n"
  f['content']=s
records=next(ast.literal_eval(n.value) for n in ast.parse(i['public']['workspace']['files'][0]['content']).body if isinstance(n,ast.Assign) and n.targets[0].id=='releases')
t=copy.deepcopy(i['grading']['tests'][0]);t['test_id']='t3';t['spec']={'expr':'releases','expected':records};t['message_on_fail']='Do not modify the supplied release records.';i['grading']['tests'].append(t)
# Precise observation shapes.
ix['tile_087.s04']['public']['prompt']+=" In starter.py, controlled_outcome must contain exactly status, interaction_id and body, taken from the HTTP response. Set comparison to {'baseline': signals[0], 'affected': signals[1]}; first_failure to the first failure record; suspected_boundary to its boundary; and supporting_evidence to a dictionary with input, database, outbound_start, first_failure, final_response and controlled_runtime, containing the corresponding supplied records and runtime_evidence. Keep proposed_change = None."
# Parse executable launcher rather than comments.
old="assert '--limit-concurrency '+str(application.budgets['limit_concurrency']) in Path('launch.sh').read_text()"
new="""import shlex
    commands=[]
    for line in Path('launch.sh').read_text().replace('\\\\\\n',' ').splitlines():
        words=shlex.split(line,comments=True)
        if words and words[0]=='exec':words=words[1:]
        if words and (Path(words[0]).name=='uvicorn' or (Path(words[0]).name in ('python','python3') and words[1:3]==['-m','uvicorn'])):
            commands.append(words)
    assert len(commands)==1, 'Supply one executable Uvicorn launch command'
    words=commands[0]
    value=None
    for index,word in enumerate(words):
        if word=='--limit-concurrency':value=int(words[index+1])
        elif word.startswith('--limit-concurrency='):value=int(word.split('=',1)[1])
    assert value == application.budgets['limit_concurrency']"""
replace_exec('tile_088.s05',old,new)
# Concurrent-only rendezvous and lock contention instrumentation.
def concurrency(p):
 s=p['sql_adapter.py'];s=s.replace("self.lock=engine._exercise_lock","self.lock=engine._exercise_lock\n        self.probe=getattr(engine,'_concurrency_probe',None)")
 s=s.replace('async with self.lock:\n            with self.sync_session.begin():yield self',"""if self.probe is not None and self.lock.locked():
            self.probe['waited']+=1
        async with self.lock:
            with self.sync_session.begin():
                if self.probe is not None:
                    self.probe['lock_entries']+=1
                    await asyncio.sleep(0)
                yield self
            if self.probe is not None:self.probe['commits']+=1""")
 p['sql_adapter.py']=s
 s=p['application.py'].replace('import json','import asyncio\nimport json',1)
 s=s.replace('app.state.inject_failure=False',"app.state.inject_failure=False\n    app.state.concurrency_probe=None")
 s=s.replace('result=await handle_authenticated_event(value,session)\n        return result',"""probe=app.state.concurrency_probe
        if probe is not None:
            probe['entered']+=1
            if probe['entered']==2:probe['ready'].set()
            await probe['ready'].wait()
        result=await handle_authenticated_event(value,session)
        if probe is not None:
            assert probe['entered']==2
            probe['completed']+=1
        return result""")
 p['application.py']=s
programs('tile_093.s04',concurrency)
replace_exec('tile_093.s04',"before=await application.snapshot(app)\n            async with httpx.AsyncClient", "before=await application.snapshot(app)\n            probe={'entered':0,'completed':0,'waited':0,'commits':0,'lock_entries':0,'ready':asyncio.Event()}\n            app.state.concurrency_probe=probe\n            app.state.sessions.engine._concurrency_probe=probe\n            async with httpx.AsyncClient")
replace_exec('tile_093.s04',"after=await application.snapshot(app)\n            assert all", "assert probe['entered']==2 and probe['completed']==2\n            assert probe['waited']>=1 and probe['commits']==2\n            app.state.sessions.engine._concurrency_probe=None\n            after=await application.snapshot(app)\n            assert all")
# Move freshness distinction assessment to existing conceptual check.
a=ix['tile_093.s07'];b=ix['tile_093.s09'];cap='distinguish_authenticated_delivery_freshness_from_original_event_age'
m=next(m for m in b['measures'] if m['capability']==cap);b['measures'].remove(m);a['measures'].append(m)
anchor=next(z for z in b['anchors'] if z.endswith('assessment:'+cap));b['anchors'].remove(anchor);a['anchors'].append(anchor)
a['public']['prompt']='A provider retries an old event with a newly signed delivery timestamp. Why must the receiver use a synchronized clock?'
texts={'o2':'Compare the authenticated delivery timestamp—not the original event age—with receiver time and configured tolerances.','o1':'Reject solely because the original event is old','o3':'Accept every valid signature regardless of receiver time.'}
for o in a['public']['options']:o['text']=texts[o['option_id']]
for f in b['public']['workspace']['files']:
 if f['path']=='README.md':
  start=f['content'].index('Provide a function stub');end=f['content'].index('\n\nStarter',start)
  f['content']=f['content'][:start]+'Complete delivery_is_fresh(age, acceptance_window, future_tolerance); the supplied preparation has already parsed the authenticated timestamp and calculated age in integer seconds.'+f['content'][end:]
# Membership rather than order; preserve all other exact policy fields.
replace_exec('tile_093.s13',"return {'case':case,'policy':policy}","assert set(policy['retryable_failures']) == {'connect_timeout','read_timeout','http_503','http_429'}\n    normalized=dict(policy)\n    normalized['retryable_failures']=['connect_timeout','read_timeout','http_503','http_429']\n    return {'case':case,'policy':normalized}")
# Enforce remaining deadline inside each scripted attempt.
def deadline(p):
 s=p['adapter.py'].replace('def __call__(self):','def __call__(self,remaining=None):')
 s=s.replace("self.clock.sleep(step.get('duration',0))", "duration=step.get('duration',0)\n        if remaining is not None and duration>remaining:\n            self.clock.sleep(max(0,remaining))\n            raise ControlledFailure('total_time_budget_exhausted')\n        self.clock.sleep(duration)")
 s=s.replace('try:return transport()',"remaining=policy['total_time_budget']-(clock.elapsed-start)\n        if remaining<=0:raise ControlledFailure('total_time_budget_exhausted')\n        try:return transport(remaining=remaining)")
 p['adapter.py']=s
 s=p['checks.py'];loc=s.index('\ndef unsafe_post():')
 s=s[:loc]+"""
    # Neither a late success nor a late failure may escape the total deadline.
    budget=limits['total_time_budget_seconds']
    for step in [{'duration':budget+1,'result':{'ok':True}}, {'duration':budget+1,'failure':'read_timeout'}]:
        result,calls,elapsed=run(get,[step])
        assert result is None and calls==1 and elapsed<=budget
    for step in [{'duration':budget,'result':{'ok':True}}, {'duration':budget,'failure':'read_timeout'}]:
        result,calls,elapsed=run(get,[{'failure':'connect_timeout'},step])
        assert result is None and calls==2 and elapsed<=budget
"""+s[loc:];p['checks.py']=s
programs('tile_093.s13',deadline)
# Combined OpenAPI declarations with readonly normalization from lesson.
normalization="""
from fastapi.openapi.utils import get_openapi
def documented_openapi():
    if app.openapi_schema is not None:return app.openapi_schema
    schema=get_openapi(title=app.title,version=app.version,description=app.description,routes=app.routes)
    for path,method in [('/orders/{order_id}','get'),('/orders','post')]:
        operation=schema['paths'][path][method]
        requirements=operation.get('security',[])
        if any('OrderBearer' in r for r in requirements) and any('OrderAuthorizationCode' in r for r in requirements):
            combined={}
            for requirement in requirements:combined.update(requirement)
            operation['security']=[combined]
    app.openapi_schema=schema
    return schema
app.openapi=documented_openapi
"""
def combined(p):
 p['application.py']+=normalization
 p['check_declarations.py']=p['check_declarations.py'].replace("assert {'OrderAuthorizationCode':[scope]} in requirements\n    assert {'OrderBearer':[]} in requirements", "assert requirements == [{'OrderBearer':[], 'OrderAuthorizationCode':[scope]}]")
programs('tile_097.s05',combined)
i=ix['tile_097.s05'];i['public']['prompt']+=' The readonly documented_openapi normalization combines bearer presentation and the documented authorization-code scope into one requirement object per protected operation; preserve it and the existing verification and permission dependencies.'
for t in i['grading']['tests']:
 if t['test_id']=='case_1':
  for path,ops in t['spec']['expected']['json'].items():
   for method,reqs in ops.items():
    obj={}
    for req in reqs:obj.update(req)
    ops[method]=[obj]
# Semantic audit grading: specified minimal schema, evidence, arbitrary order/extras.
i=ix['tile_097.s09']
i['public']['prompt']+=" Findings are dictionaries with dimension and location strings. For the required POST /orders mismatch use dimension='observed_status', observed equal to the exercised HTTP status and declared containing the documented response status strings. For the missing scheme use dimension='security_scheme', location='OrderAuthorizationCode', declared equal to its schema entry (None when missing), and expected equal to security_configuration['schemes'][location]. For each protected operation use dimension='operation_security', location='METHOD /path', declared equal to its documented security and expected equal to security_configuration['operations'][location]. Finding order is irrelevant; additional evidence-supported findings are allowed."
old="return [f for f in findings if (f['dimension'].startswith('security') or f['dimension']=='operation_security') == (case=='security_metadata')]"
new="""schema=app.openapi()
    index={(f['dimension'],f['location']):f for f in findings}
    if case=='security_metadata':
        required=[]
        name='OrderAuthorizationCode'
        declared=schema['components'].get('securitySchemes',{}).get(name)
        expected=security_configuration['schemes'][name]
        f=index[('security_scheme',name)]
        assert f['declared']==declared and f['expected']==expected and declared!=expected
        required.append({'dimension':'security_scheme','location':name,'declared':declared,'expected':expected})
        for location,expected in security_configuration['operations'].items():
            method,path=location.split(' ')
            declared=schema['paths'][path][method.lower()].get('security',[])
            f=index[('operation_security',location)]
            assert f['declared']==declared and f['expected']==expected and declared!=expected
            required.append({'dimension':'operation_security','location':location,'declared':declared,'expected':expected})
        return required
    evidence=json.loads(programs['http_evidence.json'])
    record=next(r for r in evidence['records'] if r['request']['method']=='POST' and str(r['status']) not in schema['paths']['/orders']['post']['responses'])
    declared=list(schema['paths']['/orders']['post']['responses'])
    f=index[('observed_status','POST /orders')]
    assert f['observed']==record['status'] and set(f['declared'])==set(declared)
    return [{'dimension':'observed_status','location':'POST /orders','observed':record['status'],'declared':declared}]"""
replace_exec('tile_097.s09',old,new)
# Advisory wording only.
i=ix['tile_083.s07'];s=i['public']['prompt'];print('083 prompt',s)
# Replace its precise stale sentence without adding another claim.
s=s.replace('The supplied tests include a missing-route control.', 'The non-failing controlled-route request must not create an unexpected-failure record.')
s=s.replace('The tests include a missing-route control.', 'The non-failing controlled-route request must not create an unexpected-failure record.')
i['public']['prompt']=s
k='tile_090.s06';s=ix[k]['public']['prompt'];print('090 prompt',s)
s=s.replace('Replace the shared fixture in test_items.py with isolated_client.', 'Preserve the two supplied tests using isolated_client; complete that fixture and verify both execution orders and injected-failure cleanup.')
ix[k]['public']['prompt']=s
hints={
 'tile_082':'Keep the prior artifact and its recorded configuration together.',
 'tile_083':'Compare the declared status and public body with the exercised response; keep safe failure records separate.',
 'tile_085':'Compare each supplied upstream condition with its local status and fixed public detail.',
 'tile_086':'Check raw bytes, the signature header and whether any event was processed.',
 'tile_087':'Correlate the first failure with the supplied records and keep runtime evidence separate from synthetic offsets.',
 'tile_088':'Check each independent budget and whether the expensive dependency ran.',
 'tile_089':'Check ownership in both returned rows and the SQL predicate.',
 'tile_090':'Capture both listings in fresh sessions and compare their returned collections.',
 'tile_091':'Keep registered-client acquisition settings separate from API verifier trust settings.',
 'tile_093':'Check the supplied event identity, authenticated delivery age or retry policy against the boundary this task asks about.',
 'tile_096':'Compare each permission decision with its declared public status and body.',
 'tile_097':'Compare the documented operation contract with supplied HTTP and security evidence.'}
for t in d['tiles']:
 for x in t['interactions']:
  fb=x['interaction'].get('feedback',{})
  if t['tile_id'] in hints:
   fb['hints']=[hints[t['tile_id']] if ('rejection or isolation' in h or 'supplied fixture contracts' in h) else h for h in fb.get('hints',[])]
P.write_text(json.dumps(d,indent=2)+'\n')
