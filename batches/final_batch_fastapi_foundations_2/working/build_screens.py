import json, re, ast, copy
from pathlib import Path
B=Path('batches/final_batch_foundations_2')
p=json.loads((B/'tile_plans.json').read_text())
g=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
r=json.loads((B/'scenario_asset_registry.json').read_text())
bundles={b['context']['concept_id']:b for b in g['bundles']}
assets={a['asset_id']:a for a in r['assets']}
def file(a,path): return next(f['content'] for f in assets[a]['files'] if f['path']==path)
constraint_starter=file('ws.field_constraints','main.py')
lo,hi=map(int,re.search(r'quantity from (\d+) through (\d+)',constraint_starter).groups())
mn,mx=map(int,re.search(r'order_reference from (\d+) through (\d+)',constraint_starter).groups())
constraint_code='\n'.join(l for l in constraint_starter.splitlines() if '# TODO' not in l).replace('quantity: int',f'quantity: int = Field(ge={lo}, le={hi})').replace('order_reference: str',f'order_reference: str = Field(min_length={mn}, max_length={mx})')
nested_code=file('ws.nested_models','main.py')
nested_code=re.sub(r'    # TODO: street string field.\n    pass','    street: str',nested_code)
nested_code=re.sub(r'    # TODO: product string and quantity integer fields.\n    pass','    product: str\n    quantity: int',nested_code)
nested_code=re.sub(r'    # TODO: address submodel and line_items collection of submodels.\n    pass','    address: Address\n    line_items: list[LineItem]',nested_code)
# The inputs are copied from the registry; no result/error output is authored.
nested_code+='\n'+file('ws.nested_models','inputs.py')
texts={
 'tile_018.s01': [('Application lifespan owns the shared client; requests borrow it. Initialization precedes request handling, and cleanup follows it. Define an @asynccontextmanager async function: acquire before yield, clean up after yield, and register it with FastAPI(lifespan=lifespan). Acquire this application-lifetime resource once rather than repeating startup work in each handler.', [1,2,3])],
 'tile_018.s02': [('Picture one application lifetime enclosing several requests. Acquire SharedClient before those requests; each handler borrows it without repeating startup work. Cleanup belongs after the request-handling period. Repeating acquisition inside each handler instead describes per-request work, not the one-time startup goal. Choose lifespan for a resource intended to have application lifetime; this does not mean every resource should be global.', [4])],
 'tile_018.s03': [('In the supplied service, shared_resources holds the client. Acquisition belongs before yield in the async context manager. The yielded interval is the request-handling period; cleanup afterward releases the client when that period finishes. FastAPI(lifespan=lifespan) connects this context to the application. Requests consume the resource, but lifespan owns its startup and cleanup.', [5]), ('Application-lifetime ownership is not per-request acquisition. Sharing this intended application-lifetime client avoids repeated startup work; it is not permission to share every kind of mutable object across requests.', [6])],
 'tile_019.s01': [('An order’s stored customer reference and its Python navigation are separate declarations. Use mapped_column(ForeignKey("customers.id")) for customer_id and relationship() for related objects or collections. Customer.orders navigates to orders; Order.customer navigates to the customer. Their back_populates values name each other’s relationship attribute, establishing bidirectional in-Python association behavior.', [1,2,3])],
 'tile_019.s02': [('Order.customer_id represents the stored reference to customers.id. Order.customer represents navigation to a Customer object, while Customer.orders is the counterpart collection. On Customer.orders, back_populates="customer" names Order.customer; on Order.customer, back_populates="orders" names Customer.orders. These names identify counterpart attributes, not merely tables. The paired relationships establish bidirectional in-Python association behavior; they do not determine every later loading or query behavior.', [4]), ('A relationship attribute does not replace a database foreign-key column. Stored association and object navigation are declared alongside one another.', [5])],
 'tile_020.s01': [('An integer type alone does not express an accepted quantity range. Field uses gt/lt for exclusive bounds, ge/le for inclusive bounds, and multiple_of for divisibility. Strings can use min_length, max_length and pattern for length and regular-expression restrictions. Attach Field(...) to the typed model attribute: its constraints apply when constructing the model.', [1,2,3])],
 'tile_020.s02': [(f'The supplied quantity rule runs from {lo} through {hi}, inclusive. Check boundary and neighboring inputs with the other field held valid. ge/le include their boundary; gt/lt exclude it. multiple_of would add a divisibility condition. String length and pattern are different restrictions: meeting one does not prove the other. These are construction-time validation constraints, not just documentation.', [4])],
 'tile_020.s03': [(f'For quantity, use Field(ge={lo}, le={hi}) on quantity: int to express the inclusive range. If a boundary were excluded, use gt or lt on that side instead. multiple_of adds divisibility without changing the meaning of the bounds. For order_reference: str, Field(min_length={mn}, max_length={mx}) expresses the supplied length rule; pattern would express a separate regular-expression restriction. This example imposes no pattern or divisibility requirement. Construction applies the declared constraints.', [5]), ('Do not swap an exclusive bound for an inclusive bound. Work from the rule to the declaration, then inspect the exact boundary values—not just plausible-looking interior values.', [6])],
 'tile_020.s07': [('An order can compose smaller models for its address and line items. Annotating address: Address incorporates that submodel’s validation; line_items: list[LineItem] validates the corresponding collection data. Nested validation errors can locate a failed field using enclosing field names and element indexes. Follow the location inward rather than looking only at the order’s outer fields.', [1,2,3])],
 'tile_020.s08': [('Address declares street; LineItem declares product and quantity. Order composes one Address and a list of LineItem models. In the supplied invalid input, the second item’s quantity is a nonnumeric string. Follow a nested location through line_items, the element index, then quantity to identify that part of the input. Outer-field and nested-field failures both belong to enclosing-model validation, but their locations identify different input parts.', [4]), ('An enclosing Order does not make an invalid nested value acceptable. Each submodel’s validation participates in validation of the enclosing model.', [5])]
}
titles={
'tile_018':['One owner, several requests','Application lifetime is the outer interval','Trace acquisition and cleanup','Lifespan review','Who owns the client?','Which side of yield?','Complete and register lifespan','Keep ownership explicit'],
'tile_019':['Stored reference, object navigation','Read the counterpart names','Association mapping review','Interpret the paired relationships','Map Customer and Order','Keep the two declarations distinct'],
'tile_020':['Narrow a typed field’s domain','Inspect the boundaries','Translate the rule into Field','Field constraints review','Check the numeric rule','Constrain the two fields','Compose local models','Follow a nested location','Locate the failed field','Compose Address, LineItem and Order','Constraints and composition']}
def lineage(cid,tbs,facts=None,anchors=None):
 if facts is None:
  facts=list(dict.fromkeys(f for n in tbs for f in bundles[cid]['teaching_blocks'][n-1]['fact_ids']))
 d={'concept_ids':[cid],'teaching_block_ids':[cid+'#tb'+str(n) for n in tbs],'fact_ids':[cid+'#'+f for f in facts]}
 if anchors:d['anchors']=anchors
 return d
def prose(text,cid,tbs,facts=None,role=None):
 d={'type':'prose','text':text,'lineage':lineage(cid,tbs,facts)}
 if role:d['role']=role
 return d
def visual_lin(s):
 return dict(copy.deepcopy(s['lineage']),anchors=[c+'#visual' for c in s['concept_ids']])
def diagram(s):
 cid=s['concept_ids'][0]
 if cid.endswith('application_lifespan'):
  nodes=[{'id':'lifetime','label':'Application lifetime','kind':'container'}, {'id':'acquire','label':'Acquire SharedClient','group':'lifetime'}, {'id':'yield','label':'yield: start handling requests','group':'lifetime'}, {'id':'requests','label':'Request-handling period','kind':'container','group':'lifetime'}, {'id':'cleanup','label':'Cleanup: close client','group':'lifetime'}]
  for n in range(3):nodes.append({'id':f'request_{n}','label':f'Request {n+1}: borrow client','group':'requests'})
  edges=[{'from':'acquire','to':'yield'}, {'from':'yield','to':'requests'},{'from':'requests','to':'cleanup'}]
  return {'type':'diagram','diagram_kind':'container','title':'Lifespan encloses the request intervals','nodes':nodes,'edges':edges,'alt_text':'One application lifetime encloses acquisition, yield, several request intervals borrowing the same client, and cleanup after request handling.','lineage':visual_lin(s)}
 nodes=[{'id':'stored_orders','label':'orders: stored columns','fields':[c['name'] for c in assets['ds.orders']['columns']]}, {'id':'stored_customers','label':'customers: stored columns','fields':[c['name'] for c in assets['ds.customers']['columns']]}, {'id':'customer_object','label':'Customer: navigation','fields':['orders = relationship(back_populates="customer")']}, {'id':'order_object','label':'Order: navigation','fields':['customer = relationship(back_populates="orders")']}]
 return {'type':'diagram','diagram_kind':'erd','title':'Stored reference versus Python navigation','nodes':nodes,'edges':[{'from':'stored_orders','to':'stored_customers','label':'customer_id: mapped_column(ForeignKey("customers.id"))','cardinality':'N:1'}, {'from':'customer_object','to':'order_object','label':'Customer.orders: back_populates="customer"','cardinality':'1:N'}, {'from':'order_object','to':'customer_object','label':'Order.customer: back_populates="orders"','cardinality':'N:1'}],'alt_text':'The stored orders.customer_id reference points to customers.id. Separate Customer.orders and Order.customer navigation arrows name each other through back_populates.','lineage':visual_lin(s)}
def walkthrough(s):
 if s['concept_ids'][0]=='pydantic.field_constraints':
  code=constraint_code+'\n'+file('ws.field_constraints','observe.py').replace('from main import Order\n','')
  # Annotate declaration lines by searching their actual positions.
  notes=[('quantity: int','ge/le express the inclusive quantity bounds.'),('order_reference: str','Length bounds constrain this string; no pattern is imposed.'),('def observe():','Run the supplied construction probes to inspect boundary results; the other field stays valid.')]
 else:
  code=nested_code
  notes=[('address: Address','The address field validates the address input with Address.'),('line_items: list[LineItem]','The collection validates its input objects with LineItem.'),('invalid_data =','Follow line_items to the second item and then quantity in this input. Error locations can include field names and indexes.')]
 annotations=[]
 if s['concept_ids'][0]=='pydantic.nested_models':
  parsed=ast.parse(file('ws.nested_models','inputs.py'))
  assigned={n.targets[0].id:ast.literal_eval(n.value) for n in parsed.body if isinstance(n,ast.Assign)}
  valid,invalid=assigned['valid_data'],assigned['invalid_data']
  collection=next(k for k,v in invalid.items() if isinstance(v,list))
  index=next(i for i,(a,b) in enumerate(zip(valid[collection],invalid[collection])) if a!=b)
  field=next(k for k in invalid[collection][index] if valid[collection][index][k]!=invalid[collection][index][k])
  bad=invalid[collection][index][field]
  line=next(i for i,l in enumerate(code.splitlines(),1) if bad in l)
  annotations.append({'start_line':line,'end_line':line,'text':f'Input path: {collection} → index {index} → {field}. This is the second item’s invalid quantity, not an outer field.'})
 for needle,text in notes:
  i=next(i for i,l in enumerate(code.splitlines(),1) if needle in l)
  annotations.append({'start_line':i,'end_line':i,'text':text})
 return {'type':'code_walkthrough','language':'python','code':code,'annotations':annotations,'reveal':'all','lineage':visual_lin(s)}
rem_text={
 'tile_018.s05':('Lifespan owns; requests borrow','Initialize the intended application-lifetime SharedClient before request handling and clean it up afterward. Handlers borrow that one resource without repeating its startup work. Contrast this with constructing a client in every handler: that is per-request acquisition, not the shared-lifetime goal.'),
 'tile_018.s06':('Before yield versus after yield','In an @asynccontextmanager async lifespan function, acquisition comes before yield, before the application takes requests. Cleanup comes after yield, after request handling finishes. Register that context with FastAPI(lifespan=lifespan); reversing acquisition and cleanup does not describe this lifetime.'),
 'tile_018.s07':('Define the context, then register it','Defining lifespan alone is not registration. Use an @asynccontextmanager async function with client acquisition before yield and cleanup after yield, then pass the function through FastAPI(lifespan=lifespan), rather than leaving the supplied FastAPI() construction unchanged.'),
 'tile_019.s04':('Stored reference versus paired navigation','Order.customer_id is the database reference; relationship() supplies object navigation alongside that reference. Customer.orders and Order.customer pair through back_populates="customer" and back_populates="orders" respectively. Each names the counterpart attribute to establish bidirectional in-Python association behavior—not merely a table name.'),
 'tile_019.s05':('Two kinds of declaration','Declare customer_id with mapped_column(ForeignKey("customers.id")) for the stored association. Separately declare related-object or collection navigation with relationship(). Pair Customer.orders and Order.customer by naming each other with back_populates. A navigation attribute does not replace the stored foreign-key column; the paired names establish bidirectional in-Python association behavior.'),
 'tile_020.s05':('Inclusive is not exclusive',f'The supplied quantity rule includes its endpoints: Field(ge={lo}, le={hi}). ge/le include the boundary, whereas gt/lt exclude it. multiple_of adds divisibility as another numeric restriction rather than changing which bound is inclusive. Compare the rule’s exact endpoint with an interior value before choosing a bound.'),
 'tile_020.s06':('Length rule on the typed attribute',f'For order_reference: str, attach Field(min_length={mn}, max_length={mx}) to the attribute so model construction applies the length constraints. pattern would add a regular-expression restriction; length alone is not proof of a pattern match. The supplied example has a length rule only. A typed attribute without this Field declaration does not express that rule.'),
 'tile_020.s09':('Read the location inward','Order.address incorporates Address validation, and Order.line_items incorporates LineItem validation. Enclosing the data in Order does not make a bad nested value acceptable. For the supplied nonnumeric quantity, follow the collection name to the second item and then the quantity field; a nested location can include both names and indexes.'),
 'tile_020.s10':('One submodel versus a collection','address: Address validates one nested object; line_items: list[LineItem] validates corresponding collection data. In the supplied invalid input, follow line_items to the second element and its quantity field, not to the address. Nested error locations can use collection element indexes as well as field names.')
}
recaps={
 'tile_018': [('Lifespan initializes before request handling and cleans up afterward.', 'fastapi_backend.application_lifespan',[2]), ('Acquire before yield, clean up after yield, and register with FastAPI(lifespan=lifespan). Intended application-lifetime resources are acquired once and borrowed by handlers.', 'fastapi_backend.application_lifespan',[3])],
 'tile_019': [('Foreign-key columns describe the stored association; relationship() describes object navigation alongside it.', 'fastapi_backend.orm_relationship_mapping',[2,3]), ('Use mapped_column(ForeignKey(...)) for the reference, and paired back_populates values to name counterpart relationships and establish bidirectional in-Python association behavior.', 'fastapi_backend.orm_relationship_mapping',[3])],
 'tile_020': [('Field constraints on typed attributes apply during construction. Distinguish inclusive/exclusive bounds, divisibility, string length and pattern.', 'pydantic.field_constraints',[2,3]), ('Submodel and list-of-submodel annotations compose nested validation. Error locations identify failed fields using names and collection indexes.', 'pydantic.nested_models',[2,3])]
}
next_titles={'tile_018':bundles['fastapi_backend.orm_relationship_mapping']['context']['concept_name'],'tile_019':bundles['pydantic.field_constraints']['context']['concept_name'],'tile_020':g['names']['rest.resource_contract_design']}
next_text={'tile_018':'Next: distinguish a stored database association from Python object navigation.','tile_019':'Next: narrow the values admitted by typed model fields.','tile_020':'Next: resource-oriented URLs and CRUD contracts.'}
out={k:p[k] for k in ['schema_version','path_id','batch_id']};out.update(kind='screens_part',tiles=[])
for t in p['tiles']:
 tile={'tile_id':t['tile_id'],'title':' / '.join(bundles[c]['context']['concept_name'] for c in t['concept_ids']),'steps':[],'remediation_steps':[]}
 for i,ps in enumerate(t['steps']):
  s={k:copy.deepcopy(ps[k]) for k in ['step_id','type','concept_ids']}
  s['title']=titles[t['tile_id']][i]
  s['lineage']={k:copy.deepcopy(ps[k]) for k in ['teaching_block_ids','fact_ids','segment_ids','anchors']}
  cid=s['concept_ids'][0]
  if s['type']=='explainer':
   s['blocks']=[prose(txt,cid,tbs) for txt,tbs in texts[s['step_id']]]
   if ps['planned_visual_block_type']=='diagram':s['blocks'].append(diagram(s))
   if ps['planned_visual_block_type']=='code_walkthrough':s['blocks'].append(walkthrough(s))
  elif s['type']=='video':s['blocks']=[{'type':'media_group','segment_ids':copy.deepcopy(ps['segment_ids'])}]
  elif s['type']=='recap':
   s['blocks']=[prose(txt,c,tbs,role='takeaway') for txt,c,tbs in recaps[t['tile_id']]]
   s['blocks'].append({'type':'up_next','title':next_titles[t['tile_id']],'text':next_text[t['tile_id']]})
  tile['steps'].append(s)
  if s['type'] in ['check','hands_on']:
   # Each distinct planned measured-fact set has its own short reteaching target.
   title,txt=rem_text[s['step_id']]
   facts=[f.split('#')[1] for f in ps['fact_ids']]
   tbs=[int(b['id'][2:]) for b in bundles[cid]['teaching_blocks'] if set(b['fact_ids'])&set(facts)]
   rid=t['tile_id']+'.r'+str(len(tile['remediation_steps'])+1).zfill(2)
   lin=lineage(cid,tbs,facts)
   tile['remediation_steps'].append({'step_id':rid,'type':'remediation','title':title,'concept_ids':[cid],'lineage':copy.deepcopy(lin),'blocks':[prose(txt,cid,tbs,facts)]})
 out['tiles'].append(tile)
(B/'screens.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
# Mistakes-to-avoid checks: structure, qualified IDs, standalone text, budgets,
# registry-backed input examples, output absence, and visual anchor presence.
for t,ot in zip(p['tiles'],out['tiles']):
 assert [s['step_id'] for s in t['steps']]==[s['step_id'] for s in ot['steps']]
 for ps,s in zip(t['steps'],ot['steps']):
  assert all(ps[k]==s[k] for k in ['step_id','type','concept_ids'])
  assert all(ps[k]==s['lineage'][k] for k in ['teaching_block_ids','fact_ids'])
  if s['type'] in ['check','hands_on']:assert 'blocks' not in s
  words=sum(len(b['text'].split()) for b in s.get('blocks',[]) if b['type']=='prose')
  if ps['word_budget']:assert words<=ps['word_budget'],(s['step_id'],words,ps['word_budget'])
 for s in ot['steps']+ot['remediation_steps']:
  for b in s.get('blocks',[]):
   assert not any(k in b for k in ['output','result','computed_values','segments'])
   if b['type']=='prose':
    assert 'lineage' in b and len(b['text'].split())<=90
    assert not re.search(r'\bvideo\b',b['text'],re.I)
   if b['type'] in ['diagram','code_walkthrough']:assert b['lineage']['anchors']==[c+'#visual' for c in s['concept_ids']]
   for f in b.get('lineage',{}).get('fact_ids',[]):
    c,fid=f.split('#');assert any(x['id']==fid for x in bundles[c]['coverage']['required_facts'])
print('Checklist PASS: structure, lineage, budgets, standalone prose, visual anchors, no typed outputs.')
for t in out['tiles']:print(t['tile_id'],len(t['steps']),'planned steps;',len(t['remediation_steps']),'remediation steps')
print('Total prose blocks:',sum(b['type']=='prose' for t in out['tiles'] for s in t['steps']+t['remediation_steps'] for b in s.get('blocks',[])))
