import json
from pathlib import Path
fixtures = json.loads(Path('fixtures.json').read_text())
releases = fixtures['releases']
current_database_schema = fixtures['current_database_schema']
selected_release = None  # TODO: select a compatible known prior release
procedure = {'build': None, 'release': None, 'run': None,
             'database_schema_after_rollback': None}
