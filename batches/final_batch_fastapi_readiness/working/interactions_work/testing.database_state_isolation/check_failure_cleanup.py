from starter import isolated_client
from application import app, engine, Item
from sqlalchemy.orm import Session
import json
from pathlib import Path
item=json.loads(Path('fixtures.json').read_text())['item']
original=app.dependency_overrides.copy()
# Drive the supplied yield fixture directly to exercise exception cleanup,
# independent of the order runners. Run on a clean database.
generator=isolated_client.__wrapped__()
client, session=next(generator)
client.post('/items',json=item)
try:
    generator.throw(RuntimeError('injected test failure'))
except RuntimeError:
    pass
assert app.dependency_overrides == original
with Session(engine) as probe:
    assert probe.get(Item,item['id']) is None
