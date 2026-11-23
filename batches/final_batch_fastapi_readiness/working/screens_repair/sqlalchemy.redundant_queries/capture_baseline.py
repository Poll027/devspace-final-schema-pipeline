import json
import logging
from pathlib import Path
from sqlalchemy.orm import Session
from starter import engine, listing

# starter initialization is complete before measurement. No loading edit is made.
# SQLAlchemy echo may already have a stdout handler; this additional handler
# captures actual engine log records for the fresh listing session only.
logger = logging.getLogger('sqlalchemy.engine.Engine')
handler = logging.FileHandler('baseline_sql.txt', mode='w')
handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(handler)
try:
    with Session(engine) as session:
        result = listing(session)
finally:
    logger.removeHandler(handler)
    handler.close()
Path('baseline_result.json').write_text(json.dumps(result, indent=2) + '\n')
