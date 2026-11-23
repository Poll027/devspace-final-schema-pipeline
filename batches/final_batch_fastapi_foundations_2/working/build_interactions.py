import json,sys,ast
from pathlib import Path
sys.path.insert(0,str(Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
from checkers import sandbox
B=Path('batches/final_batch_foundations_2')
load=lambda p:json.loads(p.read_text())
p=load(B/'tile_plans.json'); sc=load(B/'screens.json'); g=load(B/'inputs/path_glossary_bundle.json'); reg=load(B/'scenario_asset_registry.json')
gloss={x['context']['concept_id']:x for x in g['bundles']}; assets={x['asset_id']:x for x in reg['assets']}
pin=load(Path('00_FINAL_PIPELINE_CORE/registry/runtimes.json'))['runtimes']['python_asgi']
file=lambda aid,path:next(f['content'] for f in assets[aid]['files'] if f['path']==path)
# Scaffolding is supplied unchanged in both entry versions. Only marked learner sections differ.
life=file('ws.application_lifespan','main.py').replace('from standins import SharedClient\n','')
life_prefix=file('ws.application_lifespan','standins.py')+'\n'
life_runner='''
# Supplied observation harness: do not edit.
import asyncio
async def _observe(borrows):
    SharedClient.constructions = 0
    SharedClient.closures = 0
    shared_resources.clear()
    before = [SharedClient.constructions, SharedClient.closures]
    async with app.router.lifespan_context(app):
        clients = [shared_resources.get("client") for _ in range(borrows)]
        first = clients[0]
        same = first is not None and all(c is first for c in clients)
        during = [SharedClient.constructions, SharedClient.closures]
        closed_during = None if first is None else first.closed
    return {"before": before, "during": during,
            "after": [SharedClient.constructions, SharedClient.closures],
            "borrowed_same": same, "borrows": borrows,
            "closed_during": closed_during,
            "closed_after": None if first is None else first.closed,
            "registered": app.router.lifespan_context is lifespan}
def observe(borrows):
    coroutine = _observe(borrows)
    try:
        coroutine.send(None)
    except StopIteration as done:
        return done.value
    raise RuntimeError("The local stand-in must not suspend for external I/O")
'''
life_sol=life.replace('    yield\n','    client = SharedClient()\n    shared_resources["client"] = client\n    try:\n        yield\n    finally:\n        client.close()\n').replace('app = FastAPI()','app = FastAPI(lifespan=lifespan)')
orm=file('ws.orm_relationship_mapping','models.py').replace('from base import Base\n',file('ws.orm_relationship_mapping','base.py'))
orm_sol=orm.replace('    # TODO: declare the orders collection and its counterpart name.','    orders: Mapped[list["Order"]] = relationship(back_populates="customer")').replace('    # TODO: declare customer_id, customer navigation, and its counterpart name.','    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))\n    customer: Mapped["Customer"] = relationship(back_populates="orders")')
orm_runner='''
# Supplied inspection/association harness: do not edit.
from sqlalchemy import inspect

def observe(customer_id, order_id):
    cm, om = inspect(Customer), inspect(Order)
    c = Customer(id=customer_id)
    o = Order(id=order_id, customer_id=customer_id)
    o.customer = c
    return {"foreign_keys": sorted(f.target_fullname for f in om.columns.customer_id.foreign_keys),
            "order_customer_collection": om.relationships.customer.uselist,
            "customer_orders_collection": cm.relationships.orders.uselist,
            "order_counterpart": om.relationships.customer.back_populates,
            "customer_counterpart": cm.relationships.orders.back_populates,
            "stored_customer_id": o.customer_id,
            "navigation_customer_id": o.customer.id,
            "collection_order_ids": [item.id for item in c.orders],
            "same_customer": o.customer is c}
'''
field=file('ws.field_constraints','main.py')
field_sol=field.replace('    quantity: int\n','    quantity: int = Field(ge=1, le=20)\n').replace('    order_reference: str\n','    order_reference: str = Field(min_length=3, max_length=12)\n')
field_runner='''
# Supplied boundary harness: do not edit.
from pydantic import ValidationError

def observe(quantity, order_reference):
    try:
        model = Order(quantity=quantity, order_reference=order_reference)
        return {"constructed": True, "quantity": model.quantity,
                "order_reference": model.order_reference}
    except ValidationError as error:
        return {"constructed": False, "locations": [list(e["loc"]) for e in error.errors()]}
'''
nested=file('ws.nested_models','main.py')
nested_sol=nested.replace('    # TODO: street string field.\n    pass','    street: str').replace('    # TODO: product string and quantity integer fields.\n    pass','    product: str\n    quantity: int').replace('    # TODO: address submodel and line_items collection of submodels.\n    pass','    address: Address\n    line_items: list[LineItem]')
nested_runner='''
# Supplied construction/location harness: do not edit.
def observe(data):
    try:
        model = Order.model_validate(data)
        return {"constructed": True, "address_type": type(model.address).__name__,
                "item_types": [type(i).__name__ for i in model.line_items],
                "street": model.address.street,
                "items": [[i.product, i.quantity] for i in model.line_items]}
    except ValidationError as error:
        return {"constructed": False, "locations": [list(e["loc"]) for e in error.errors()]}
'''
inputs={};exec(file('ws.nested_models','inputs.py'),inputs)
# Derive test inputs from supplied assets, rather than retyping their values.
qs=[];lengths=[]
for n in ast.walk(ast.parse(file('ws.field_constraints','observe.py'))):
 if isinstance(n,ast.For) and isinstance(n.target,ast.Name):
  if n.target.id=='quantity':qs=list(ast.literal_eval(n.iter))
  if n.target.id=='length':lengths=list(ast.literal_eval(n.iter))
records=lambda aid:[dict(zip([c['name'] for c in assets[aid]['columns']],r)) for r in assets[aid]['rows']]
customers=records('ds.customers');orders=records('ds.orders')
# Dataset records have named columns.
print('dataset rows',customers,orders)
code={
 'fastapi_backend.application_lifespan':(life_prefix+life+life_runner,life_prefix+life_sol+life_runner,[[2],[4]],['fastapi'],
 'Complete the marked lifespan section and application construction. Acquire one supplied SharedClient before yield, store it as shared_resources["client"], close that same client after the yielded interval, and register lifespan with FastAPI. Leave the supplied stand-in and observe(borrows) harness unchanged. Its observations must show one construction, repeated borrowing of the same open instance, one close on exit, and registration.'),
 'fastapi_backend.orm_relationship_mapping':(orm+orm_runner,orm_sol+orm_runner,[],['sqlalchemy'],
 'Complete Customer.orders, Order.customer_id and Order.customer in the existing classes. The stored foreign key must target customers.id; Order.customer must navigate to one Customer and Customer.orders to an Order collection. Set reciprocal back_populates names. Leave Base and the observe(customer_id, order_id) harness unchanged; it inspects declarations and verifies that assigning o.customer places o in c.orders.'),
 'pydantic.field_constraints':(field+field_runner,field_sol+field_runner,[[q,'REF'] for q in qs]+[[qs[1],'R'*n] for n in lengths],['pydantic'],
 'Add Field declarations to both typed attributes of Order. Accept quantity from 1 through 20 inclusive and order_reference from 3 through 12 characters, with no additional pattern or divisibility restriction. Leave the supplied observe(quantity, order_reference) harness unchanged. Construction must accept both endpoints and reject immediately outside each range with the other field valid.'),
 'pydantic.nested_models':(nested+nested_runner,nested_sol+nested_runner,[[inputs['valid_data']],[inputs['invalid_data']]],['pydantic'],
 'Complete Address with street: str and LineItem with product: str and quantity: int. Complete Order with one address submodel and a line_items collection of submodels. Leave observe(data) unchanged. Valid supplied input must construct Order containing Address and LineItem instances and preserve their values. The supplied invalid second item must fail at the collection field, index 1, quantity; the harness returns error locations.')}
# ORM test identifiers copied from the registered dataset records.
code['fastapi_backend.orm_relationship_mapping'][2].extend([[o['customer_id'],o['id']] for o in (orders[0],orders[-1])])
# Run the pinned engine to compute every expected result.
computed={}
for cid,(starter,solution,args,packages,prompt) in code.items():
 probes=[{'id':f't{i}','kind':'call','function':'observe','args':a,'kwargs':{}} for i,a in enumerate(args)]
 script=sandbox._py_script('compute','main.py',solution,[],probes)
 results=sandbox.node_run(sandbox._py_job('python_asgi',packages,[script]),pin['runner'])['results']['compute']
 if not results['ok']: raise RuntimeError(results)
 computed[cid]=results['probes']
 for v in results['probes'].values():
  if not v['ok']:raise RuntimeError(v)
(B/'working/computed_interaction_results.json').write_text(json.dumps(computed,indent=2)+'\n')
choices={
 'tile_018.s05':('A client is intended to live for the entire application request-handling period. Several handlers borrow it. Which ownership plan meets the one-time startup goal?',[
 ('Acquire once in lifespan before request handling; let handlers borrow it; clean up after request handling.','Lifespan owns startup and cleanup for this intended application-lifetime client.'),
 ('Acquire a fresh client inside every handler invocation.','Per-request acquisition repeats startup work instead of meeting the one-time startup goal.'),
 ('Acquire once in lifespan but close it before the request-handling period starts.','Cleanup follows request handling; closing beforehand does not keep the shared resource available during that period.')],0),
 'tile_018.s06':('In an @asynccontextmanager lifespan function, where do acquisition and cleanup belong relative to yield?',[
 ('Acquire after yield and clean up before yield.','Acquisition must precede request handling; this reverses startup and cleanup.'),
 ('Acquire before yield and clean up after yield.','Yield separates initialization from the request-handling interval; cleanup follows that interval.'),
 ('Acquire and close the client before yield.','Closing before yield puts cleanup before the request-handling interval instead of after it.')],1),
 'tile_019.s04':('Customer.orders and Order.customer are relationship attributes alongside Order.customer_id, a foreign-key column. Which reciprocal back_populates pair names the opposite relationship attributes?',[
 ('Customer.orders names "customer"; Order.customer names "orders".','Each value names the counterpart navigation attribute on the opposite class.'),
 ('Customer.orders names "customer_id"; Order.customer names "id".','These are stored column names, not the counterpart relationship attributes.'),
 ('Customer.orders names "orders"; Order.customer names "customer".','These name the same-side attributes rather than each other.')],0),
 'tile_020.s05':('For quantity: int = Field(ge=1, le=20), with all other fields valid, how should construction treat the two quantity endpoints?',[
 ('Reject both endpoints because bounds are always exclusive.','ge and le include their respective endpoints; gt and lt are the exclusive bounds.'),
 ('Accept the lower endpoint but reject the upper endpoint.','le includes the upper endpoint just as ge includes the lower one.'),
 ('Accept both endpoints.','ge and le express inclusive lower and upper bounds.')],2),
}
# The nested check's key is derived from validation of the registered invalid input.
loc=computed['pydantic.nested_models']['t1']['value']['locations'][0]
choices['tile_020.s09']=(f'Order uses address: Address and line_items: list[LineItem]. In this input, where does nested validation locate the invalid value?\n{json.dumps(inputs["invalid_data"],indent=2)}',[
 (str(tuple(loc)),'The collection path identifies the second item and its failing quantity field.'),
 (str(('address','street')),'The supplied address street is valid; the nonnumeric value belongs to a line item, not the address.'),
 ('No error: enclosing the data in Order makes nested values acceptable.','Submodel validation participates in enclosing-model validation; an invalid nested value does not become acceptable.')],0)
rem={t['tile_id']:t.get('remediation_steps',[]) for t in sc['tiles']}
out={k:p[k] for k in ['schema_version','path_id','batch_id']};out.update(kind='interactions_part',tiles=[])
for t in p['tiles']:
 entries=[];steps=[s for s in t['steps'] if s['type'] in ('check','hands_on')];seen=set()
 for i,s in enumerate(steps):
  cid=s['concept_ids'][0];bundle=gloss[cid]
  measures=[]
  for a in s['anchors']:
   if '#assessment:' in a:
    cap=a.split('#assessment:')[1];anchor=next(x for x in bundle['assessment_anchors'] if x['capability']==cap)
    measures.append({'concept_id':cid,**anchor})
  ix={'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'],'difficulty':'intro' if i==0 else ('stretch' if i==len(steps)-1 else 'core'),'grading_mode':'client','standalone':s['type']=='check','measures':measures,'anchors':s['anchors']}
  if ix['type']=='choice':
   prompt,opts,key=choices[s['step_id']];oids=[f'o{j+1}' for j in range(len(opts))]
   ix['public']={'prompt':prompt,'options':[{'option_id':oid,'text':text} for oid,(text,msg) in zip(oids,opts)],'selection':'single','shuffle':True}
   ix['grading']={'correct_option_ids':[oids[key]],'option_feedback':{oid:{'message':msg} for oid,(_,msg) in zip(oids,opts)}}
   correct=opts[key][1];incorrect='Compare the chosen option with the rule in the prompt; its feedback explains the specific mismatch.'
  else:
   starter,solution,args,packages,prompt=code[cid]
   ix['public']={'prompt':prompt,'runtime':{'kind':'python_asgi','version':pin['version'],'packages':packages},'workspace':{'files':[{'path':'main.py','role':'editable','language':'python','content':starter}],'entry':'main.py'},'constraints':{k:bundle['practice_anchor']['live_code'][k] for k in ['allowed_syntax','blocked_syntax']}}
   ix['grading']={'solution_files':[{'path':'main.py','content':solution}],'tests':[{'test_id':f't{j}','kind':'function_call','spec':{'function':'observe','args':a,'expected':computed[cid][f't{j}']['value']},'visible':True,'message_on_fail':'The supplied observation does not meet the declared resource, association, or validation contract.'} for j,a in enumerate(args)]}
   correct={'fastapi_backend.application_lifespan':'The registered lifespan creates one shared client, lends the same open instance during its yielded interval, and closes it on exit.', 'fastapi_backend.orm_relationship_mapping':'The foreign-key column stores the association, while reciprocal relationship attributes provide single-object and collection navigation.', 'pydantic.field_constraints':'Both typed attributes carry Field constraints; inclusive quantity and reference-length boundaries pass while immediately outside values fail.', 'pydantic.nested_models':'The submodel annotations construct valid nested models and locate the invalid second item at its quantity field.'}[cid];incorrect={'fastapi_backend.application_lifespan':'Check acquisition before yield, cleanup after yield, the shared dictionary entry, and FastAPI lifespan registration.', 'fastapi_backend.orm_relationship_mapping':'Keep the foreign-key column separate from navigation, and name the opposite relationship attribute in each back_populates value.', 'pydantic.field_constraints':'Attach Field to each typed attribute. Do not substitute exclusive bounds for inclusive ones or omit the reference-length constraints.', 'pydantic.nested_models':'Use Address for one nested object and list[LineItem] for the collection; their field annotations participate in enclosing validation.'}[cid]
  hints={
   'fastapi_backend.application_lifespan':['Draw the application interval around the requests. Which work belongs outside that interval?'],
   'fastapi_backend.orm_relationship_mapping':['Separate stored identifiers from object navigation, then look at the opposite class.'],
   'pydantic.field_constraints':['Check the exact boundary, not only an interior value.'],
   'pydantic.nested_models':['Follow the input tree inward: outer field, collection position, then inner field.']}
  ix['feedback']={'correct':{'message':correct},'incorrect':{'message':incorrect},'hints':hints[cid]}
  rs=[r for r in rem[t['tile_id']] if cid in r['concept_ids']]
  if rs:
   used=sum(1 for e in entries if any(m['concept_id']==cid for m in e['interaction']['measures']))
   ix['feedback']['remediation_step_id']=rs[min(used,len(rs)-1)]['step_id']
  seen.add(cid);entries.append({'step_id':s['step_id'],'interaction':ix})
 out['tiles'].append({'tile_id':t['tile_id'],'interactions':entries})
(B/'interactions.json').write_text(json.dumps(out,indent=2)+'\n')
