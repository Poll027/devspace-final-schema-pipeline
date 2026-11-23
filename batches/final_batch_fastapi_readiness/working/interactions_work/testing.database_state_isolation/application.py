from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
class Base(DeclarativeBase):
    pass
class Item(Base):
    __tablename__ = 'items'
    id: Mapped[int] = mapped_column(primary_key=True)
class ItemInput(BaseModel):
    id: int
engine = create_engine('sqlite:///state_sharing.sqlite', connect_args={'check_same_thread':False})
# Explicit SQLite transaction control makes nested savepoints subordinate
# to the outer transaction (including Python sqlite legacy transaction mode).
@event.listens_for(engine, 'connect')
def configure(dbapi_connection, _):
    dbapi_connection.isolation_level = None
@event.listens_for(engine, 'begin')
def begin(connection):
    connection.exec_driver_sql('BEGIN')
Base.metadata.create_all(engine)  # only once, never in a per-test transaction
app = FastAPI()
def session_provider():
    with Session(engine) as session:
        yield session
@app.post('/items')
def write_item(item: ItemInput, session=Depends(session_provider)):
    session.add(Item(id=item.id))
    session.commit()
    return {'id':item.id}
@app.get('/items/{item_id}')
def read_item(item_id: int, session=Depends(session_provider)):
    item = session.get(Item, item_id)
    if item is None:
        raise HTTPException(404, 'Not found')
    return {'id':item.id}
