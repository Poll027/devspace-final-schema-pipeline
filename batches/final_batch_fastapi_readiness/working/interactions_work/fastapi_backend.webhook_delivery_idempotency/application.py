import json, os
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import select, event
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from starter import Base, Order, ProcessedEvent, handle_authenticated_event
fixtures=json.loads(Path('fixtures.json').read_text())
DATABASE=os.environ.get('TEST_DATABASE','sqlite+aiosqlite:///delivery.sqlite')
def make_app():
    engine=create_async_engine(DATABASE,connect_args={'timeout':30})
    Sessions=async_sessionmaker(engine,expire_on_commit=False)
    @asynccontextmanager
    async def lifespan(app):
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        async with Sessions.begin() as session:
            for row in fixtures['orders']:
                if await session.get(Order,row['id']) is None: session.add(Order(**row))
        yield
        await engine.dispose()  # never drop persistent tables on restart
    app=FastAPI(lifespan=lifespan)
    app.state.sessions=Sessions
    app.state.inject_failure=False
    async def session_provider():
        async with Sessions() as session:
            if app.state.inject_failure:
                # SQLAlchemy hook fails during transaction flush, regardless
                # of where learner flushes: both writes must be rolled back.
                @event.listens_for(session.sync_session,'after_flush_postexec',once=True)
                def fail(_session,_context):
                    raise RuntimeError('controlled transaction failure')
            yield session
    @app.post('/authenticated-events')
    async def deliver(value:dict,session=Depends(session_provider)):
        # This exercise starts AFTER publisher authenticity; supplied literals
        # are trusted controlled authenticated events, not public webhook input.
        result=await handle_authenticated_event(value,session)
        return result
    return app
async def snapshot(app):
    async with app.state.sessions() as session:
        orders=(await session.scalars(select(Order).order_by(Order.id))).all()
        events=(await session.scalars(select(ProcessedEvent).order_by(ProcessedEvent.publisher_event_id))).all()
        return {'orders':[{'id':o.id,'owner_id':o.owner_id,'status':o.status} for o in orders],
                'events':[e.publisher_event_id for e in events]}
app=make_app()
