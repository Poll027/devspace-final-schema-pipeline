import json, re, ast
from pathlib import Path
B=Path(__file__).resolve().parents[1]
g=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
sid='scenario.order_service'
# Vocabulary is selected only when it occurs literally in teaching blocks or anchors.
texts=[]
for b in g['bundles']:
    texts.extend(t['content'] for t in b['teaching_blocks'])
    for key in ('assessment_anchors','practice_anchor','visual_anchor'):
        def strings(v):
            if isinstance(v,str): yield v
            elif isinstance(v,list):
                for z in v: yield from strings(z)
            elif isinstance(v,dict):
                for z in v.values(): yield from strings(z)
        texts.extend(strings(b[key]))
text='\n'.join(texts)
terms=['order','customer','shared external client','SharedClient','shared_resources','lifespan','yield','asynccontextmanager','FastAPI','FastAPI(lifespan=lifespan)','Customer','Order','customers','orders','customers.id','customer_id','customer','back_populates','ForeignKey','mapped_column','relationship','Base','Mapped','quantity','order_reference','Field','ge=1','le=20','min_length=3','max_length=12','gt','ge','lt','le','multiple_of','min_length','max_length','pattern','Address','LineItem','BaseModel','ValidationError','address','line_items','street','product','model_validate','error.errors()',"('line_items', 1, 'quantity')"]
vocab=list(dict.fromkeys(t for t in terms if t in text))
# Mine numbers from the teaching/anchor strings as well, rather than inventing vocabulary.
vocab.extend(n for n in dict.fromkeys(re.findall(r'(?<![\w])\d+(?![\w])',text)) if n not in vocab)
assets=[]
def workspace(id,title,files):
    for path,content in files.items():
        if path.endswith('.py'): ast.parse(content)
    assets.append(dict(asset_id=id,asset_kind='code_workspace',scenario_id=sid,title=title,runtime='python',files=[dict(path=p,content=c) for p,c in files.items()]))
def dataset(id,title,columns,rows,description):
    assets.append(dict(asset_id=id,asset_kind='dataset',scenario_id=sid,title=title,description=description,columns=[dict(name=n,type=t,semantic_role=r,description=d) for n,t,r,d in columns],rows=rows,provenance='authored'))
dataset('ds.customers','customers',[('id','integer','identifier','Customer identifier, not a measured quantity.')],[[1],[2],[3]],'Fictional customers for the customers.id reference. Identifiers are labels; no personal data is supplied.')
dataset('ds.orders','orders',[('id','integer','identifier','Order identifier.'),('customer_id','integer','identifier','Stored reference to customers.id.')],[[1,1],[2,1],[3,2]],'Fictional stored associations: one customer has several orders and one has none. Navigation attributes are not stored columns.')
workspace('ws.application_lifespan','Shared-client application lifetime',{
'standins.py':'''class SharedClient:
    constructions = 0
    closures = 0

    def __init__(self):
        type(self).constructions += 1
        self.closed = False

    def close(self):
        type(self).closures += 1
        self.closed = True
''',
'main.py':'''from contextlib import asynccontextmanager
from fastapi import FastAPI
from standins import SharedClient

shared_resources = {}

@asynccontextmanager
async def lifespan(app):
    # TODO: acquire one SharedClient and store it under the key "client".
    # TODO: close that same client during cleanup after yield.
    yield

# TODO: register lifespan when constructing the application.
app = FastAPI()
''',
'observe.py':'''import asyncio
import main
from standins import SharedClient

async def observe():
    before = (SharedClient.constructions, SharedClient.closures)
    async with main.app.router.lifespan_context(main.app):
        first = main.shared_resources.get("client")
        second = main.shared_resources.get("client")
        during = (SharedClient.constructions, SharedClient.closures)
        borrowed_same = first is not None and first is second
        closed_during = None if first is None else first.closed
    return {"before": before, "during": during,
            "after": (SharedClient.constructions, SharedClient.closures),
            "borrowed_same": borrowed_same, "closed_during": closed_during,
            "closed_after": None if first is None else first.closed,
            "registered": main.app.router.lifespan_context is main.lifespan}

if __name__ == "__main__":
    print(asyncio.run(observe()))
''',
'README.md':'Local stand-in only; no network calls or request handlers. Complete main.py, then run observe.py to observe the application context. Requires FastAPI. The supplied resource belongs to this application lifetime, not to every request.'})
workspace('ws.orm_relationship_mapping','Customer–Order association declarations',{
'base.py':'''from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
''',
'models.py':'''from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from base import Base

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    # TODO: declare the orders collection and its counterpart name.

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    # TODO: declare customer_id, customer navigation, and its counterpart name.
''',
'README.md':'Requires SQLAlchemy 2.x. Complete the existing classes without database operations. The registered customers and orders tables show the stored identifiers only; Customer.orders and Order.customer are object-navigation attributes, not stored columns.'})
workspace('ws.field_constraints','Order quantity and reference boundaries',{
'main.py':'''from pydantic import BaseModel, Field

class Order(BaseModel):
    # TODO: quantity from 1 through 20 inclusive.
    quantity: int
    # TODO: order_reference from 3 through 12 characters.
    order_reference: str
''',
'observe.py':'''from pydantic import ValidationError
from main import Order

# In each group the other field stays valid. Results are computed, not supplied.
def observe():
    results = []
    for quantity in (0, 1, 20, 21):
        data = dict(quantity=quantity, order_reference="REF")
        try:
            Order(**data)
            results.append((data, "constructed"))
        except ValidationError as error:
            results.append((data, error.errors()))
    for length in (2, 3, 12, 13):
        data = dict(quantity=1, order_reference="R" * length)
        try:
            Order(**data)
            results.append((data, "constructed"))
        except ValidationError as error:
            results.append((data, error.errors()))
    return results

if __name__ == "__main__":
    print(observe())
''',
'README.md':'Requires Pydantic 2.x. Add Field declarations to the two typed attributes. Run observe.py to see boundary construction results. The current rule specifies range and length only; no extra pattern or divisibility requirement is imposed.'})
workspace('ws.nested_models','Nested address and line-item data',{
'main.py':'''from pydantic import BaseModel, ValidationError

class Address(BaseModel):
    # TODO: street string field.
    pass

class LineItem(BaseModel):
    # TODO: product string and quantity integer fields.
    pass

class Order(BaseModel):
    # TODO: address submodel and line_items collection of submodels.
    pass
''',
'inputs.py':'''valid_data = {
    "address": {"street": "7 Sample Lane"},
    "line_items": [
        {"product": "Notebook", "quantity": 1},
        {"product": "Pencil", "quantity": 2},
    ],
}
invalid_data = {
    "address": {"street": "7 Sample Lane"},
    "line_items": [
        {"product": "Notebook", "quantity": 1},
        {"product": "Pencil", "quantity": "not-a-number"},
    ],
}
''',
'observe.py':'''from pydantic import ValidationError
from main import Order
from inputs import valid_data, invalid_data

def observe():
    results = []
    for data in (valid_data, invalid_data):
        try:
            model = Order.model_validate(data)
            results.append(model)
        except ValidationError as error:
            results.append(error.errors())
    return results

if __name__ == "__main__":
    print(observe())
''',
'README.md':'Requires Pydantic 2.x. Complete Address, LineItem and Order with the supplied field names and annotations. Inputs are authored fictional data. Run observe.py to inspect construction and nested error locations. This exercise composes plain typed submodels, not the separately constrained Order model.'})
registry=dict(schema_version='1.0',kind='scenario_asset_registry',path_id=g['path_id'],batch_id=g['batch_id'],scenarios=[dict(scenario_id=sid,name='Fictional order service',summary='A small fictional order service associates customers with orders, validates quantity and reference inputs, composes address and line-item data, and borrows one shared client owned by application lifespan. Each workspace isolates its own concept; the ORM and validation Order classes are separate examples.',domain='backend order service',glossary_example_vocab=vocab)],assets=assets)
# Stage checklist: width, types/roles, declared association values, anchor coverage, and plot need.
for a in assets:
    if a['asset_kind']=='dataset':
        assert all(len(row)==len(a['columns']) for row in a['rows'])
        for col in a['columns']:
            assert col['semantic_role']=='identifier' and col['type']=='integer'
        assert all(isinstance(v,int) for row in a['rows'] for v in row)
customers={r[0] for r in assets[0]['rows']}
assert all(r[1] in customers for r in assets[1]['rows'])
assert len({a['asset_id'] for a in assets})==len(assets)
assert len([a for a in assets if a['asset_kind']=='code_workspace'])==len(g['bundles'])
assert all(b['visual_anchor']['type'] in ('diagram','code') for b in g['bundles'])
assert all(t in text for t in vocab)
# No variants: no planted issues or duplicate occurrences to verify.
(B/'scenario_asset_registry.json').write_text(json.dumps(registry,indent=2)+'\n')
print('Checklist PASS: widths; identifier roles; FK references; vocabulary; four practice workspaces; no plotted anchors; no variants.')
print('Scenarios:',len(registry['scenarios']),'assets:',len(assets))
print('Asset ids:', ', '.join(a['asset_id'] for a in assets))
