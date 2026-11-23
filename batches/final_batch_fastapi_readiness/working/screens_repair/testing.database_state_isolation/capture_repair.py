import ast, json
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from application import app, engine, session_provider
# Execute the completed fixture generator body and the supplied test functions.
# No pytest runner is available in this offline runtime.
fixture_ast=ast.parse(Path('starter.py').read_text())
fixture_function=next(node for node in fixture_ast.body
                      if isinstance(node,ast.FunctionDef) and node.name=='isolated_client')
fixture_function.decorator_list=[]
exec(compile(ast.Module(body=[fixture_function],type_ignores=[]),'starter.py','exec'))
test_ast=ast.parse(Path('test_items.py').read_text())
exec(compile(ast.Module(body=[node for node in test_ast.body if isinstance(node,ast.FunctionDef)],
                        type_ignores=[]),'test_items.py','exec'))
fixtures=json.loads(Path('fixtures.json').read_text())
item=fixtures['item']
for order in fixtures['execution_orders']:
    print(' → '.join(order))
    for name in order:
        boundary=isolated_client()
        supplied=next(boundary)
        try:
            globals()['test_'+name](supplied)
        finally:
            try:
                next(boundary)
            except StopIteration:
                pass
        print('test_'+name+': PASS (all supplied assertions)')
    print('Execution order: PASS')
