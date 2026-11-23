import asyncio, httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, String, ForeignKey, select, event, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import IntegrityError
fixtures = {'authenticated_events': [{'publisher_event_id': 'evt_a', 'order_id': 101, 'new_status': 'complete'}, {'publisher_event_id': 'evt_b', 'order_id': 202, 'new_status': 'complete'}], 'orders': [{'id': 101, 'owner_id': 'caller_a', 'status': 'pending'}, {'id': 202, 'owner_id': 'caller_b', 'status': 'pending'}, {'id': 303, 'owner_id': 'caller_a', 'status': 'complete'}], 'tests': ['sequential_duplicate', 'restart_with_database_retained', 'concurrent_duplicate', 'transaction_failure'], 'initial_processed_events': []}
class Base(DeclarativeBase): pass
class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
class ProcessedEvent(Base):
    __tablename__ = 'processed_events'
    id: Mapped[int] = mapped_column(primary_key=True)
    publisher_event_id: Mapped[str] = mapped_column(String)
    __table_args__ = (UniqueConstraint('publisher_event_id'),)
class OrderChange(Base):
    __tablename__ = 'order_changes'
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
@event.listens_for(Order, 'after_update')
def count_change(mapper, connection, target):
    connection.execute(OrderChange.__table__.insert().values(order_id=target.id))
engine = create_engine('sqlite://', poolclass=StaticPool, connect_args={'check_same_thread':False})
Base.metadata.create_all(engine)
with Session(engine) as session:
    session.add_all([Order(**x) for x in fixtures['orders']]); session.commit()
# Supplied async facade preserves a sync SQLite transaction; no threads/network.
class AsyncSessionFacade:
    def __init__(self, session): self.session = session
    @asynccontextmanager
    async def begin(self):
        with self.session.begin(): yield self
    def add(self, value): self.session.add(value)
    async def flush(self): self.session.flush()
    async def scalar(self, statement): return self.session.scalar(statement)
def snapshot():
    with Session(engine) as session:
        orders = session.scalars(select(Order).order_by(Order.id)).all()
        events = session.scalars(select(ProcessedEvent).order_by(ProcessedEvent.publisher_event_id)).all()
        changes = session.scalars(select(OrderChange).order_by(OrderChange.id)).all()
        return {'orders':[{'id':o.id,'owner_id':o.owner_id,'status':o.status} for o in orders], 'events':[e.publisher_event_id for e in events], 'committed_changes':[x.order_id for x in changes]}
def make_app():
    api = FastAPI()
    @api.exception_handler(Exception)
    async def failed(request, exc): return JSONResponse(status_code=500,content={'detail':'Internal server error'})
    @api.post('/authenticated-events')
    async def deliver(value:dict, failure:str='none'):
        # Exercise begins after signature authentication; this is a controlled trusted-event harness.
        with Session(engine) as session:
            if failure != 'none':
                @event.listens_for(session, 'after_flush_postexec', once=True)
                def inject(session, context):
                    if failure == 'integrity': raise IntegrityError('unrelated controlled constraint',{},Exception('internal'))
                    raise RuntimeError('controlled transaction failure')
            return await handle_authenticated_event(value, AsyncSessionFacade(session))
    return api
app = FastAPI()
@app.post('/scenario/{kind}')
async def scenario(kind:str, value:dict):
    child = make_app()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=child,raise_app_exceptions=False),base_url='http://test') as client:
        if kind == 'concurrent':
            responses = await asyncio.gather(client.post('/authenticated-events',json=value),client.post('/authenticated-events',json=value))
        elif kind == 'failure' or kind == 'integrity':
            responses = [await client.post('/authenticated-events',params={'failure':kind},json=value)]
        else:
            responses = [await client.post('/authenticated-events',json=value)]
            if kind == 'sequential': responses.append(await client.post('/authenticated-events',json=value))
    if kind == 'restart':
        # Reconstruct a new app and request-local session, retain the same persistent engine.
        child = make_app()
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=child,raise_app_exceptions=False),base_url='http://test') as client:
            responses.append(await client.post('/authenticated-events',json=value))
    return {'responses':[{'status':r.status_code,'json':r.json()} for r in responses], 'snapshot':snapshot()}
# Complete only the transactional handler below, not the durable models or harness.
async def handle_authenticated_event(event, session):
    return {"received":False}
