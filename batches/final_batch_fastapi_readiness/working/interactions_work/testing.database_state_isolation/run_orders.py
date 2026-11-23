import json, subprocess, sys
from pathlib import Path
from application import engine, Item
from sqlalchemy.orm import Session
orders = json.loads(Path('fixtures.json').read_text())['execution_orders']
results=[]
for order in orders:
    # Initialize empty state only before a complete order, not between tests.
    with Session(engine) as session:
        session.query(Item).delete()
        session.commit()
    result = subprocess.run([sys.executable,'-m','pytest','-q'] + ['test_items.py::test_'+name for name in order])
    results.append(result.returncode)
raise SystemExit(any(results))
