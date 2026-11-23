import json, logging
from sqlalchemy.orm import Session
from starter import engine, Entity, select, selectinload, listing
def revised_listing(session):
    statement = select(Entity).order_by(Entity.id).limit(3)
    statement = statement.options(selectinload(Entity.relationship_attribute))
    parents = session.execute(statement).scalars().all()
    return [{'id':p.id, 'children':[c.id for c in p.relationship_attribute]} for p in parents]

class Capture(logging.Handler):
    def __init__(self):
        super().__init__(); self.messages=[]
    def emit(self,record):
        message=record.getMessage()
        if message.lstrip().startswith('SELECT'):
            self.messages.append(message)
handler=Capture()
logger=logging.getLogger('sqlalchemy.engine.Engine')
logger.addHandler(handler)
captures={}
for name,fn in [('before',listing),('after',revised_listing)]:
    handler.messages=[]
    with Session(engine) as session:
        result=fn(session)
    captures[name]={'sql':handler.messages.copy(),'returned':result}
logger.removeHandler(handler)
assert captures['before']['returned']==captures['after']['returned']
from pathlib import Path
Path('listing_capture.json').write_text(json.dumps(captures,indent=2))
