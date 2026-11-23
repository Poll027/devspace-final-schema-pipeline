import json, copy, ast, re
from pathlib import Path
B=Path('batches/final_batch_verification_2')
plan=json.loads((B/'tile_plans.json').read_text())
gloss=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
registry=json.loads((B/'scenario_asset_registry.json').read_text())
bundles={x['context']['concept_id']:x for x in gloss['bundles']}
assets={x['asset_id']:x for x in registry['assets']}
C=list(bundles)
EX,DEP,HEAD,ERR,MET,PART,COMP=C

def file(c,path):
    return next(f['content'] for f in assets['cw.'+c]['files'] if f['path']==path)
def before(code,marker): return code.split(marker)[0].rstrip()+'\n'
def node(code,name):
    n=next(n for n in ast.parse(code).body if getattr(n,'name',None)==name)
    return '\n'.join(code.splitlines()[n.lineno-1:n.end_lineno])+'\n'
def lineage(cs,tbs=(),facts=(),anchors=()):
    return {'concept_ids':list(cs),'teaching_block_ids':list(tbs),'fact_ids':list(facts),'anchors':list(anchors)}
def prose(text,lin,role='mechanism'):
    return {'type':'prose','text':text,'role':role,'lineage':copy.deepcopy(lin)}
def code(text,lin):
    return {'type':'code_walkthrough','language':'python','code':text,'reveal':'all','lineage':copy.deepcopy(lin)}
def pair(left,right,ll,rl,takeaway,lin):
    return {'type':'side_by_side','left':code(left,lin),'right':code(right,lin),'left_label':ll,'right_label':rl,'takeaway':takeaway,'lineage':copy.deepcopy(lin)}

# Each authored paragraph names only the teaching blocks and facts it re-voices.
texts={
 'tile_054.s01':[
  ('Use model_config = ConfigDict(json_schema_extra={"examples": [...]}) for model schema examples, or Field(examples=[...]) for field examples. Validate each proposed sample with Model.model_validate(example) before publishing it.', ['tb1','tb2','tb3'],['f1','f4']),
  ('Body(openapi_examples={...}) supplies named request-body examples. Decorator tags, summary and description group and describe the operation; they do not change runtime behavior.', ['tb3'],['f2','f3'])],
 'tile_054.s02':[
  ('A documentation sample must satisfy the executable model. Validate the synthetic order sample before putting it in schema examples or named body examples. Review the quantity bound, not just whether the payload looks plausible.', ['tb4'],['f1','f2','f4']),
  ('A summary can explain the operation, but cannot loosen its constraint. Ask whether the documentation illustrates the declared contract or implies a different one.', ['tb4'],['f3'])],
 'tile_054.s03':[
  ('The registered OrderInput declares a positive quantity. Its synthetic example supplies {quantity}. OrderInput.model_validate(example) checks that sample before publication; ConfigDict places it in model-level schema examples. Field(examples=[...]) is the field-level alternative.', ['tb5'],['f1','f4']),
  ('Use the same validated sample in Body(openapi_examples={...}) for a named body example. The POST /orders metadata describes returning validated input without persistence. Tags, summary and description do not change that behavior or make an invalid example valid.', ['tb5','tb6'],['f2','f3','f4'])],
 'tile_055.s01':[
  ('An isolated endpoint test substitutes at the declared dependency boundary. app.dependency_overrides maps the original provider callable to a replacement callable. FastAPI uses that replacement when resolving the dependency; the mapping is not keyed by a provider name or returned value.', ['tb1','tb2','tb4'],['f1']),
  ('Assign app.dependency_overrides[original] = replacement, send the HTTP request, then assert the replacement is observable in the response. In this synthetic fixture, original returns {original_value} and replacement returns {replacement_value}; the handler exposes the selected value under user.', ['tb3','tb4'],['f1','f2']),
  ('Save and restore the previous override state in try/finally. Reset to an empty dictionary only when there were no previous overrides. An active replacement can leak into later tests; restoration is not automatic. Trace setup, request, assertion and cleanup together.', ['tb3','tb4','tb5'],['f3'])],
 'tile_056.s01':[
  ('Bind a header explicitly with Annotated[Type, Header()]. A metadata-looking parameter name alone does not select headers instead of query parameters.', ['tb1','tb2','tb5'],['f1']),
  ('Header converts underscores to hyphens by default: user_agent reads user-agent. Header names are case-insensitive. Header(alias="user-agent") explicitly chooses that name; Header(convert_underscores=False) keeps the literal user_agent mapping instead.', ['tb3','tb4','tb5'],['f2']),
  ('Annotated[Type, Cookie()] binds a cookie by name. The fixture declares cookie with a None default so omission is accepted. Source selection and omission behavior are separate: Cookie chooses the source, while the default permits absence.', ['tb3','tb4'],['f3'])],
 'tile_056.s04':[
  ('Invalid request data raises RequestValidationError. FastAPI handles it before normal operation logic receives that input. In the order fixture, the quantity value {invalid_quantity} cannot satisfy the declared integer field.', ['tb1','tb2','tb4'],['f1']),
  ('Assert the default status 422, then inspect response.json()["detail"]. Each relevant entry identifies the failed input location through loc and the error kind through type. The fixture derives these expectations from the unchanged contract; do not guess them.', ['tb3','tb4'],['f2']),
  ('A model-validation failure while application code builds a result, or during response validation, indicates a server-side bug. It is not the same as invalid client request data, and not every validation failure is a client 422.', ['tb3','tb4','tb5'],['f3'])],
 'tile_058.s01':[
  ('Use maintained instrumentation around the application boundary for request counters, response counters and a duration histogram. Handlers need not each implement their own metrics; an exposed metrics endpoint alone does not verify the wiring.', ['tb1','tb2'],['f1']),
  ('Import PrometheusMiddleware and metrics from starlette_prometheus. Register app.add_middleware(PrometheusMiddleware, filter_unhandled_paths=True), then app.add_route("/metrics/", metrics). Use bounded nonsensitive labels such as method, matched route template and response status. Filtering unmatched paths avoids unlimited series from arbitrary requested paths.', ['tb3'],['f2','f3']),
  ('Send controlled successful, expected-error and delayed requests. Compare request and response counter changes and completed-response duration observations with those requests. This middleware updates its response counter even for a raised exception, but observes processing time only when the inner application returns a response.', ['tb3'],['f4','f5'])],
 'tile_058.s02':[
  ('The registered fixture separates success, expected-error, delayed response and escaping-exception cases. Compare before/after samples for each matched route, rather than mixing them with metrics-view requests. The maintained counters and duration histogram should be checked against these controlled events, not assumed correct because /metrics/ exists.', ['tb4'],['f1','f2','f3','f4']),
  ('An expected-error response still returns a response. An escaping exception differs: this middleware updates its response counter but has no normal processing-time observation for that exception. Counts and completed-response durations therefore need not cover identical cases.', ['tb4','tb5'],['f5'])],
 'tile_059.s01':[
  ('A partial update separates presence from value. Pydantic records explicitly supplied fields in model_fields_set; model_dump(exclude_unset=True) excludes fields that were not supplied.', ['tb1','tb2'],['f1']),
  ('Extract update = model.model_dump(exclude_unset=True) so omitted fields do not introduce defaults that overwrite stored values. Inspect the extracted data before changing storage. A quantity-only input leaves note out of the update rather than treating its default as a supplied value.', ['tb3','tb4'],['f1','f2']),
  ('An explicitly supplied note=None remains supplied with exclude_unset=True. A supplied string keeps its value. Adding exclude_none=True separately removes None-valued fields and can erase an intentional null update. A final model value alone cannot distinguish omission from explicit supply.', ['tb3','tb4'],['f1','f3'])],
 'tile_059.s02':[
  ('Compare the registered cases: quantity-only input, explicit note=None, and note={note_value}. model_fields_set reveals what was supplied; model_dump(exclude_unset=True) extracts those fields without omitted defaults. This preserves the difference between leaving note unchanged and supplying a replacement value.', ['tb5'],['f1','f2']),
  ('exclude_unset asks whether a field was supplied. exclude_none asks whether its value is None. They are not interchangeable cleanup flags: adding exclude_none can remove the explicit null that the update contract intended to preserve.', ['tb5','tb6'],['f1','f3'])],
 'tile_059.s06':[
  ('Compatibility review compares old client expectations, not just matching type names. Changing an omittable note field into a required field rejects previously accepted requests that omit it. Compare requiredness as well as types.', ['tb1','tb2','tb5'],['f1']),
  ('Tightening a type or field constraint can reject previously valid input. Test representative old inputs against the revised model. The registered comparison keeps an old quantity sample alongside the previous and tightened constraints, so both validations can be inspected.', ['tb3','tb4','tb5'],['f2']),
  ('Removing or changing a public response field or operation can change documented client expectations. Compare the generated paths and response schemas against the previous contract before approving the revision. Matching input type names alone says nothing about those public output changes.', ['tb3','tb4','tb5'],['f3'])]
}

step_titles={
 'tile_054.s01':'Examples that match the contract','tile_054.s02':'Documentation is not a constraint override','tile_054.s03':'Review the synthetic order example','tile_054.s04':'Choose accurate operation metadata','tile_054.s05':'Publish a validated order example',
 'tile_055.s01':'Substitute at the dependency boundary','tile_055.s02':'Trace provider substitution','tile_055.s03':'Follow the active provider mapping','tile_055.s04':'Follow the restored provider mapping','tile_055.s05':'Override, request, assert, restore',
 'tile_056.s01':'Choose the metadata source explicitly','tile_056.s02':'Resolve the header name','tile_056.s03':'Bind a header and an omittable cookie','tile_056.s04':'Inspect invalid request data','tile_056.s05':'Client input or server-side bug?','tile_056.s06':'Assert the invalid-order response',
 'tile_058.s01':'Instrument the boundary and verify it','tile_058.s02':'A response count is not a duration observation','tile_058.s03':'Compare measurement boundaries','tile_058.s04':'Verify controlled request metrics',
 'tile_059.s01':'Preserve supplied-field intent','tile_059.s02':'Omission and null are different updates','tile_059.s03':'Trace supplied-field extraction','tile_059.s04':'Separate omitted and supplied fields','tile_059.s05':'Extract updates without losing null intent','tile_059.s06':'Review the previous contract too','tile_059.s07':'Review tightened input constraints','tile_059.s08':'Review public fields and operations','tile_059.s09':'Compare requiredness across revisions'
}

# Values are taken from registered source fixtures, never retyped.
example=ast.literal_eval(next(n.value for n in ast.parse(file(EX,'main.py')).body if isinstance(n,ast.Assign) and any(getattr(t,'id',None)=='example' for t in n.targets)))
def returned(c,name):
    fn=next(n for n in ast.parse(file(c,'main.py')).body if getattr(n,'name',None)==name)
    return ast.literal_eval(next(n.value for n in fn.body if isinstance(n,ast.Return)))
invalid=ast.literal_eval(next(n.value for n in ast.parse(file(ERR,'fixture.py')).body if isinstance(n,ast.Assign) and any(getattr(t,'id',None)=='invalid_order' for t in n.targets)))
part_tree=ast.parse(file(PART,'main.py'))
note=next(n.value.keywords[0].value.value for n in part_tree.body if isinstance(n,ast.Assign) and any(getattr(t,'id',None)=='concrete_note' for t in n.targets))
values={'quantity':example['quantity'],'original_value':repr(returned(DEP,'original')),'replacement_value':repr(returned(DEP,'replacement')),'invalid_quantity':repr(invalid['quantity']),'note_value':repr(note)}
def substitute(text):
    for k,v in values.items():text=text.replace('{'+k+'}',str(v))
    return text

recaps={
 'tile_054':[(EX,'Schema examples use ConfigDict/json_schema_extra or Field(examples=[...]); validate the sample with model_validate before publishing.', ['f1','f4']), (EX,'Body(openapi_examples={...}) supplies named body examples. Tags, summary and description describe the operation without changing runtime behavior.', ['f2','f3'])],
 'tile_055':[(DEP,'Map original callable to replacement callable, send the test request and assert the replacement is observable.', ['f1','f2']), (DEP,'Restore the earlier override state afterward. An empty dictionary is appropriate only when the earlier state was empty.', ['f3'])],
 'tile_056':[(HEAD,'Header and Cookie choose request sources explicitly. Header names are case-insensitive; underscores become hyphens by default. A cookie default permits omission.', ['f1','f2','f3']), (ERR,'Invalid request data is handled before normal operation logic. Assert default status 422 and inspect detail loc/type. Server-side model-validation failures are a different problem.', ['f1','f2','f3'])],
 'tile_058':[(MET,'Install maintained boundary instrumentation and expose /metrics/. Use bounded nonsensitive labels and filter unmatched paths.', ['f1','f2','f3']), (MET,'Verify known successful, expected-error and delayed requests against counter changes and duration observations. A raised exception updates this middleware’s response counter, but its normal processing-time observation requires a returned response.', ['f4','f5'])],
 'tile_059':[(PART,'model_fields_set tracks supply; exclude_unset extracts supplied fields without omitted defaults. Explicit None remains supplied; exclude_none can erase intentional null.', ['f1','f2','f3']), (COMP,'Review requiredness, tightened types or constraints, public response fields and operations. Test previously valid inputs and compare generated paths and response schemas before approving changes.', ['f1','f2','f3'])]
}

fact_voice={
 EX:{'f1':'Model-level schema examples use model_config = ConfigDict(json_schema_extra={"examples": [...]}). Field(examples=[...]) is the field-level alternative.', 'f2':'Use Body(openapi_examples={...}) for named request-body examples in operation documentation.', 'f3':'Decorator tags, summary and description group and describe the operation without changing its runtime behavior.', 'f4':'Validate proposed samples with Model.model_validate(example) before publication so they agree with the executable model.'},
 DEP:{'f1':'app.dependency_overrides maps the original provider callable to a replacement callable; FastAPI uses the replacement to resolve that dependency.', 'f2':'Assign app.dependency_overrides[original] = replacement, send the test request, and assert the replacement’s observable behavior.', 'f3':'Restore the earlier overrides after the test to prevent leakage. Reset to an empty dictionary only if no prior overrides existed.'},
 HEAD:{'f1':'Annotated[Type, Header()] reads a header instead of treating the parameter as a query input.', 'f2':'Header names are case-insensitive. By default user_agent maps to user-agent; alias or convert_underscores=False controls that mapping.', 'f3':'Annotated[Type, Cookie()] reads a cookie by name. Provide a default when omission should be accepted.'},
 ERR:{'f1':'Invalid request data raises RequestValidationError, which FastAPI handles before normal operation logic receives the input.', 'f2':'Assert the default invalid-input status 422 and inspect JSON detail entries for the failed location and error type.', 'f3':'Validation failures in response or application code indicate a server-side bug, not the same client-input rejection.'},
 MET:{'f1':'Maintained boundary instrumentation supplies request/response counters and a duration histogram, rather than metrics implemented separately in each handler.', 'f2':'Import PrometheusMiddleware and metrics from starlette_prometheus. Use app.add_middleware(PrometheusMiddleware, filter_unhandled_paths=True) and app.add_route("/metrics/", metrics).', 'f3':'Choose bounded nonsensitive labels such as method, matched route template and response status. Filter unmatched paths to avoid unlimited series from arbitrary paths.', 'f4':'Compare controlled successful, expected-error and delayed requests with request/response counter changes and completed-response duration observations.', 'f5':'This middleware updates its response counter even for a raised exception. Its processing-time histogram is observed only when the inner application returns a response.'},
 PART:{'f1':'model_fields_set records explicitly supplied fields; model_dump(exclude_unset=True) leaves out fields that were not supplied.', 'f2':'Extract update = model.model_dump(exclude_unset=True) so defaults for omitted fields do not overwrite stored values.', 'f3':'Explicit None remains supplied with exclude_unset=True. exclude_none=True separately removes None-valued fields and can erase an intentional null update.'},
 COMP:{'f1':'Making an omittable request field required rejects formerly accepted requests. Compare requiredness as well as types.', 'f2':'Tightening a type or constraint can reject previously valid input. Test representative old inputs against the revision.', 'f3':'Changing or removing a public response field or operation can change documented client expectations. Compare generated paths and response schemas with the previous contract.'}
}

contrast={
 EX:'Compare the validated synthetic order example with metadata that would imply another contract. Documentation illustrates acceptance; it does not redefine it.',
 DEP:'In the same fixture, distinguish an active original-to-replacement mapping from the restored mapping. Follow the callable selected for the request, not the name of the test.',
 HEAD:'In /metadata, compare the declared source with a metadata-looking name alone. Header or Cookie selects the source; the cookie default separately permits omission.',
 ERR:'Contrast the fixture’s invalid order request with a failure while the service validates its own result. The location of validation separates client input from a server-side bug.',
 MET:'Contrast the fixture’s returned expected-error response with its escaping exception. A response count and a normal duration observation do not have identical boundaries.',
 PART:'Compare quantity-only input, note=None, and the registered string note. Omission is not explicit null; supplied-field extraction preserves that distinction.',
 COMP:'Compare the same old order request against the previous and revised note declarations. Matching type names do not establish matching requiredness or the rest of the public contract.'
}

def visual(ps,lin):
    c=ps['concept_ids'][0]
    vl=copy.deepcopy(lin);vl['anchors']=[c+'#visual']
    if c==EX:return code(file(c,'visual_reference.py'),vl)
    if c==DEP:return code(file(c,'main.py').split('def test_override():')[0]+file(c,'visual_reference.py'),vl)
    if c==HEAD:return code(file(c,'visual_reference.py'),vl)
    if c==ERR:return code(file(c,'fixture.py')+'\n'+file(c,'visual_reference.py'),vl)
    if c==MET:
        config=before(file(c,'visual_reference.py'),'def evidence():')
        # Both panels are source/reference material, not pre-authored metric results.
        return pair(config+file(c,'fixture.py'),file(c,'harness.py')+'\n'+node(file(c,'visual_reference.py'),'evidence'), 'Configure and send known requests','Observe matched-route changes','Compare returned responses with an escaping exception; counting and duration observation differ.',vl)
    if c==PART:
        models=before(file(c,'main.py'),'# TODO:')
        return pair(models,file(c,'visual_reference.py'),'Three supplied-field cases','Compare extraction options','Inspect supplied fields and execute the extraction; exclude_none removes null separately from omission.',vl)
    if c==COMP:
        return pair(before(file(c,'main.py'),'# TODO:'),file(c,'visual_reference.py'),'Previous and revised requiredness','Constraints and public contracts','Compare old inputs and generated public schemas, not just type names.',vl)
    raise AssertionError(c)

out={k:plan[k] for k in ['schema_version','path_id','batch_id']};out['kind']='screens_part';out['tiles']=[]
cluster_titles={c['tile_id']:c['title'] for c in gloss['clusters']}
for t in plan['tiles']:
    title=cluster_titles.get(t['tile_id'],bundles[t['concept_ids'][0]]['context']['concept_name'])
    tile={'tile_id':t['tile_id'],'title':title,'steps':[],'remediation_steps':[]}
    for ps in t['steps']:
        lin=lineage(ps['concept_ids'],ps['teaching_block_ids'],ps['fact_ids'],ps['anchors'])
        lin['segment_ids']=copy.deepcopy(ps['segment_ids'])
        st={'step_id':ps['step_id'],'type':ps['type'],'concept_ids':copy.deepcopy(ps['concept_ids']),'title':step_titles.get(ps['step_id'],'Keep these distinctions'),'lineage':lin}
        if ps['type']=='explainer':
            c=ps['concept_ids'][0];st['blocks']=[]
            for text,tbs,fs in texts[ps['step_id']]:
                pl=lineage([c],[c+'#'+x for x in tbs],[c+'#'+x for x in fs])
                st['blocks'].append(prose(substitute(text),pl))
            if ps['planned_visual_block_type']:st['blocks'].append(visual(ps,lin))
        elif ps['type']=='video':
            st['blocks']=[{'type':'media_group','segment_ids':copy.deepcopy(ps['segment_ids'])}]
        elif ps['type']=='recap':
            st['blocks']=[]
            for c,text,fs in recaps[t['tile_id']]:
                # Takeaways point back to the text teaching each fact.
                tbs=[c+'#'+tb['id'] for tb in bundles[c]['teaching_blocks'] if set(tb['fact_ids']) & set(fs)]
                st['blocks'].append(prose(text,lineage([c],tbs,[c+'#'+f for f in fs]),'takeaway'))
            nt=next((x for x in plan['tiles'] if x['tile_id']==t['next_tile_id']),None)
            if nt:
                nc=nt['steps'][0]['concept_ids'][0]
                next_title=bundles[nc]['context']['concept_name']
                next_text=bundles[nc]['teaching_blocks'][0]['content']
            else:
                # The supplied glossary has a name, but no teaching block for the next tile.
                nc=next(c for c in bundles[COMP]['context']['blocked_future_concepts'] if c not in bundles)
                next_title=gloss['names'][nc]
                next_text='Next: '+next_title+'.'
            st['blocks'].append({'type':'up_next','title':next_title,'text':next_text})
        # Check/hands_on deliberately contain framing only. Stage 04 owns interactions.
        tile['steps'].append(st)
    # Distinct measured fact sets receive distinct remediation. Infer practice-only
    # coverage from the glossary when a practice step has no planned fact ids.
    seen=set()
    for ps in t['steps']:
        if ps['type'] not in ('check','hands_on'):continue
        c=ps['concept_ids'][0]
        fs=list(ps['fact_ids'])
        for anchor in ps['anchors']:
            if '#assessment:' in anchor:
                capability=anchor.split('#assessment:')[1]
                assessment=next(a for a in bundles[c]['assessment_anchors'] if a['capability']==capability)
                for f in assessment['fact_ids']:
                    q=c+'#'+f
                    if q not in fs:fs.append(q)
        if not fs:fs=[c+'#'+f['id'] for f in bundles[c]['coverage']['required_facts']]
        key=(c,tuple(sorted(fs)))
        if key in seen:continue
        seen.add(key)
        tbs=[c+'#'+tb['id'] for tb in bundles[c]['teaching_blocks'] if set(tb['fact_ids']) & {f.split('#')[1] for f in fs}]
        rlin=lineage([c],tbs,fs)
        r={'step_id':t['tile_id']+'.r'+str(len(tile['remediation_steps'])+1).zfill(2),'type':'remediation','concept_ids':[c],'title':'Revisit: '+step_titles[ps['step_id']],'lineage':rlin,'blocks':[]}
        r['blocks'].append(prose(contrast[c],rlin,'mental_model'))
        for q in fs:
            f=q.split('#')[1]
            ftbs=[c+'#'+tb['id'] for tb in bundles[c]['teaching_blocks'] if f in tb['fact_ids']]
            r['blocks'].append(prose(fact_voice[c][f],lineage([c],ftbs,[q]),'definition'))
        tile['remediation_steps'].append(r)
    out['tiles'].append(tile)

# Self-review: plan identity, framing-only interactions, qualified lineage, visual
# anchors, source-matched code, no typed outputs, and strict narrative budgets.
def walk(x):
    if isinstance(x,dict):
        yield x
        for v in x.values():yield from walk(v)
    elif isinstance(x,list):
        for v in x:yield from walk(v)
for pt,ot in zip(plan['tiles'],out['tiles']):
    assert pt['tile_id']==ot['tile_id']
    for ps,st in zip(pt['steps'],ot['steps']):
        for k in ['step_id','type','concept_ids']:assert st[k]==ps[k]
        for k in ['fact_ids','teaching_block_ids']:assert st['lineage'][k]==ps[k]
        if st['type'] in ('check','hands_on'):assert 'blocks' not in st and 'interaction' not in st
        if st['type']=='video':assert st['blocks']==[{'type':'media_group','segment_ids':ps['segment_ids']}]
        if st['type'] in ('explainer','recap'):
            # Includes visual captions/labels but not source code.
            narrative=[]
            for x in walk(st['blocks']):
                for k in ['text','takeaway','left_label','right_label','alt_text']:
                    if k in x and isinstance(x[k],str):narrative.append(x[k])
            count=sum(len(s.split()) for s in narrative)
            assert count<=ps['word_budget'],(st['step_id'],count,ps['word_budget'])
        if ps['planned_visual_block_type'] in ('code_walkthrough','side_by_side'):
            assert any(x.get('type')==ps['planned_visual_block_type'] and set(ps['anchors'])<=set(x.get('lineage',{}).get('anchors',[])) for x in walk(st['blocks']))
    for x in walk(ot):
        if x.get('type')=='prose':
            assert 'lineage' in x and len(x['text'].split())<=90
            assert not re.search(r'\bvideo\b',x['text'],re.I)
        if 'lineage' in x:
            for k in ['fact_ids','teaching_block_ids','anchors']:
                assert all('#' in q for q in x['lineage'].get(k,[]))
        assert not any(k in x for k in ['output','execution_provenance','computed_values','result'])
(B/'screens.json').write_text(json.dumps(out,indent=2)+'\n')
print('Checklist passed: plan, lineage, budgets, framing, visual anchors, no typed outputs.')
print('Tiles:',len(out['tiles']))
for t in out['tiles']:print(t['tile_id'],len(t['steps']),'planned steps;',len(t['remediation_steps']),'remediation steps')
