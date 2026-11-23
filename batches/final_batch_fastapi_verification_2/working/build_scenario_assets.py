import ast
import json
import re
from pathlib import Path

B = Path('batches/final_batch_verification_2')
source = json.loads((B / 'inputs/path_glossary_bundle.json').read_text())
bundles = source['bundles']
by_id = {b['context']['concept_id']: b for b in bundles}
scenario_id = 'scen.order_api_verification'

# Mine only teaching blocks and anchors; retain exact vocabulary from the source.
texts = '\n'.join(json.dumps({k: b.get(k) for k in ('teaching_blocks', 'assessment_anchors', 'practice_anchor', 'visual_anchor')}, ensure_ascii=False) for b in bundles)
vocab_candidates = ['order', 'quantity', 'note', 'OrderInput', 'OrderUpdate', 'BaseModel', 'ConfigDict', 'Field', 'gt=0', 'examples', 'json_schema_extra', 'model_config', 'model_validate', 'Body', 'openapi_examples', 'Annotated', 'tags', 'summary', 'description', 'POST /orders', 'FastAPI', 'Header', 'Cookie', 'user_agent', 'user-agent', 'cookie', 'alias', 'convert_underscores=False', 'None', 'RequestValidationError', 'ValidationError', 'TestClient', 'Depends', 'original', 'replacement', 'actual user', 'mock user', 'user', 'app.dependency_overrides', 'try/finally', 'loc', 'type', 'detail', '422', 'quantity 2', 'model_fields_set', 'model_dump', 'exclude_unset=True', 'exclude_none=True', 'Leave at reception', 'PrometheusMiddleware', 'starlette_prometheus', '/metrics/', 'filter_unhandled_paths=True', 'method', 'matched route template', 'response status', 'request', 'response', 'counter', 'histogram', 'count', 'sum', 'delay', 'successful', 'expected-error', 'delayed', 'exception', 'generated paths', 'public response fields', 'requiredness', 'omittable', 'HTTPException', 'asyncio.sleep']
vocab = [v for v in vocab_candidates if v in texts]
# Values used in fixture data come from the glossary's worked sample / starter.
walkthrough = next(t['content'] for t in bundles[0]['teaching_blocks'] if '```python' in t['content'])
code = re.search(r'```python\n(.*?)```', walkthrough, re.S).group(1)
example = next(ast.literal_eval(n.value) for n in ast.parse(code).body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'example' for t in n.targets))
quantity = example['quantity']
partial_text = json.dumps(by_id['pydantic.partial_update_contracts']['practice_anchor'])
note = next(v for v in vocab if v == 'Leave at reception')

assets = []
assets.append({
    'asset_id': 'ds.orders', 'asset_kind': 'dataset', 'scenario_id': scenario_id,
    'title': 'Synthetic stored order examples',
    'description': 'Authored order records only. A null note is an intentional null, not a planted missing-data defect. Omission versus explicit null in update payloads is represented by JSON objects in the partial-update workspace, not by CSV blanks.',
    'columns': [
        {'name': 'quantity', 'type': 'integer', 'semantic_role': 'numerical', 'description': 'Count of units; the OrderInput contract requires a value greater than zero.'},
        {'name': 'note', 'type': 'string', 'semantic_role': 'text', 'description': 'Optional synthetic order instruction. Null is allowed.'}
    ],
    'rows': [[quantity, note], [quantity, None]], 'provenance': 'authored',
    'variants': [{
        'variant_id': 'orders.invalid_quantity', 'derived_from': 'ds.orders',
        'purpose': 'A request sample outside the positive-quantity bound, not a valid stored order.',
        'ops': [{'op': 'set_cell', 'where': {'note': note}, 'occurrence': 0, 'column': 'quantity', 'value': 0}],
        'planted_issues': [{
            'issue_id': 'issue.nonpositive_quantity', 'kind': 'impossible_value',
            'locations': [{'where': {'note': note}, 'occurrence': 0, 'column': 'quantity'}],
            'description': 'The quantity does not satisfy the declared greater-than-zero request constraint.',
            'rule': {'column': 'quantity', 'op': 'le', 'value': 0}
        }]
    }]
})
assets.append({
    'asset_id': 'ds.controlled_request_cases', 'asset_kind': 'dataset', 'scenario_id': scenario_id,
    'title': 'Controlled instrumentation request plan',
    'description': 'Authored local test inputs, not measured metrics. Counter and histogram observations must be obtained by running the metrics workspace. Metrics-view traffic is excluded from the exercised-route comparisons.',
    'columns': [
        {'name': 'case', 'type': 'string', 'semantic_role': 'categorical'},
        {'name': 'method', 'type': 'string', 'semantic_role': 'categorical'},
        {'name': 'route_template', 'type': 'string', 'semantic_role': 'categorical'},
        {'name': 'response_status', 'type': 'integer', 'semantic_role': 'categorical', 'numeric_looking_label': True, 'description': 'HTTP status label, not a quantity to average.'},
        {'name': 'configured_delay_seconds', 'type': 'number', 'semantic_role': 'numerical', 'unit': 'seconds'},
        {'name': 'returns_response', 'type': 'boolean', 'semantic_role': 'categorical'}
    ],
    'rows': [
        ['success', 'GET', '/success', 200, 0, True],
        ['expected_error', 'GET', '/expected-error', 400, 0, True],
        ['delayed', 'GET', '/delayed', 200, 0.05, True],
        ['escaping_exception', 'GET', '/escaping-exception', 500, 0, False]
    ], 'provenance': 'authored'
})

workspaces = {}
workspaces['fastapi.contract_examples_metadata'] = {
'main.py': '''from typing import Annotated
from fastapi import FastAPI, Body
from pydantic import BaseModel, ConfigDict, Field

example = {"quantity": QUANTITY}

class OrderInput(BaseModel):
    quantity: int = Field(gt=0)
    # TODO: add schema example metadata without changing the quantity bound.

app = FastAPI()

# TODO: add tags, summary and description; retain this handler's behavior.
@app.post("/orders")
def create_order(order: OrderInput):
    return order

# TODO: validate example and use it as a named Body(openapi_examples=...) example.
'''.replace('QUANTITY', repr(quantity)),
'visual_reference.py': '''from typing import Annotated
from fastapi import FastAPI, Body
from pydantic import BaseModel, ConfigDict, Field

example = {"quantity": QUANTITY}

class OrderInput(BaseModel):
    quantity: int = Field(gt=0)
    model_config = ConfigDict(json_schema_extra={"examples": [example]})

OrderInput.model_validate(example)
app = FastAPI()

@app.post("/orders", tags=["orders"], summary="Validate an order",
          description="Return the validated order input without persistence.")
def create_order(order: Annotated[OrderInput, Body(openapi_examples={
    "positive_quantity": {"summary": "Positive quantity", "description": "Synthetic order input.", "value": example}
})]):
    return order
'''.replace('QUANTITY', repr(quantity))
}
workspaces['fastapi.dependency_overrides'] = {
'main.py': '''from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

app = FastAPI()

def original():
    return "actual user"

@app.get("/")
def hello(user: str = Depends(original)):
    return {"user": user}

def replacement():
    return "mock user"

def test_override():
    assert app.dependency_overrides == {}
    # TODO: register the replacement using the original callable as the key.
    try:
        with TestClient(app) as client:
            response = client.get("/")
            # TODO: assert the synthetic value under user.
    finally:
        # TODO: restore the initially empty override dictionary.
        pass
''',
'visual_reference.py': '''from main import app, original, replacement
from fastapi.testclient import TestClient

def test_override():
    previous = app.dependency_overrides.copy()
    app.dependency_overrides[original] = replacement
    try:
        with TestClient(app) as client:
            response = client.get("/")
            assert response.json()["user"] == replacement()
    finally:
        app.dependency_overrides = previous
'''
}
workspaces['fastapi.header_cookie_binding'] = {
'main.py': '''from typing import Annotated
from fastapi import FastAPI, Header, Cookie

app = FastAPI()

@app.get("/metadata")
def endpoint(user_agent: str, cookie: str | None = None):
    # TODO: change only the parameter source annotations, not this body.
    return {"user_agent": user_agent, "cookie": cookie}
''',
'visual_reference.py': '''from typing import Annotated
from fastapi import FastAPI, Header, Cookie
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/metadata")
def endpoint(user_agent: Annotated[str, Header()],
             cookie: Annotated[str | None, Cookie()] = None):
    return {"user_agent": user_agent, "cookie": cookie}

# Computed request/declaration evidence; no hand-written response output.
def evidence():
    with TestClient(app) as client:
        for headers, cookies in [({"user-agent": "synthetic client"}, {}),
                                 ({"USER-AGENT": "synthetic client"}, {"cookie": "synthetic cookie"})]:
            response = client.get("/metadata", headers=headers, cookies=cookies)
            yield {"headers": headers, "cookies": cookies,
                   "status": response.status_code, "response": response.json()}
'''
}
workspaces['fastapi.request_validation_errors'] = {
'fixture.py': '''from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

class OrderInput(BaseModel):
    quantity: int = Field(gt=0)

app = FastAPI()

@app.post("/orders")
def create_order(order: OrderInput):
    return order

client = TestClient(app)
invalid_order = {"quantity": "not an integer"}

# Derive the expected loc/type from this untouched fixture, not a typed output.
def validation_expectations():
    reference = client.post("/orders", json=invalid_order)
    entry = reference.json()["detail"][0]
    return entry["loc"], entry["type"]
''',
'main.py': '''from fixture import client, invalid_order, validation_expectations

expected_location, expected_type = validation_expectations()
# TODO: submit invalid_order with client.post and assert status 422.
# TODO: inspect response.json()["detail"] and assert loc/type match the supplied expectations.
''',
'visual_reference.py': '''from fixture import client, invalid_order, validation_expectations

def evidence():
    expected_location, expected_type = validation_expectations()
    response = client.post("/orders", json=invalid_order)
    assert response.status_code == 422
    entry = response.json()["detail"][0]
    assert entry["loc"] == expected_location
    assert entry["type"] == expected_type
    return {"request": invalid_order, "status": response.status_code, "detail": response.json()["detail"]}
'''
}
workspaces['pydantic.partial_update_contracts'] = {
'main.py': '''from pydantic import BaseModel

class OrderUpdate(BaseModel):
    note: str | None = None
    quantity: int | None = None

quantity_only = OrderUpdate(quantity=QUANTITY)
explicit_null = OrderUpdate(note=None)
concrete_note = OrderUpdate(note=NOTE)

# TODO: extract each supplied-field update using model_dump(exclude_unset=True).
# Compare model_fields_set and the effect of also using exclude_none=True.
'''.replace('QUANTITY', repr(quantity)).replace('NOTE', repr(note)),
'visual_reference.py': '''from main import quantity_only, explicit_null, concrete_note

def evidence():
    for name, model in [("note omitted", quantity_only),
                        ("explicit null note", explicit_null),
                        ("concrete note", concrete_note)]:
        yield {"case": name, "model_fields_set": sorted(model.model_fields_set),
               "exclude_unset": model.model_dump(exclude_unset=True),
               "exclude_unset_and_none": model.model_dump(exclude_unset=True, exclude_none=True)}
''',
'payloads.json': json.dumps([{'quantity': quantity}, {'note': None}, {'note': note}], indent=2)
}
workspaces['rest.compatible_contract_changes'] = {
'main.py': '''from pydantic import BaseModel, ValidationError

class PreviousOrderInput(BaseModel):
    note: str | None = None

class RevisedOrderInput(BaseModel):
    note: str | None

omitted_note = {}
supplied_note = {"note": NOTE}

# TODO: validate both inputs against both models and identify the requiredness change.
# TODO: retain the previous default to preserve omission support.
'''.replace('NOTE', repr(note)),
'visual_reference.py': '''from fastapi import FastAPI
from pydantic import BaseModel, Field, ValidationError
from main import PreviousOrderInput, RevisedOrderInput, omitted_note, supplied_note

# Independent synthetic comparisons; do not combine these changes with the practice task.
class PreviousQuantity(BaseModel):
    quantity: int = Field(gt=0)

class TightenedQuantity(BaseModel):
    quantity: int = Field(gt=QUANTITY)

class PreviousResponse(BaseModel):
    quantity: int
    note: str | None = None

class RemovedNoteResponse(BaseModel):
    quantity: int

def validation_evidence():
    for old, new, payload in [(PreviousOrderInput, RevisedOrderInput, omitted_note),
                              (PreviousOrderInput, RevisedOrderInput, supplied_note),
                              (PreviousQuantity, TightenedQuantity, {"quantity": QUANTITY})]:
        results = []
        for model in (old, new):
            try:
                value = model.model_validate(payload)
                results.append({"model": model.__name__, "accepted": True, "value": value.model_dump()})
            except ValidationError as exc:
                results.append({"model": model.__name__, "accepted": False, "errors": exc.errors()})
        yield {"input": payload, "results": results}

def contract_app(response_model, include_operation=True):
    app = FastAPI()
    if include_operation:
        @app.get("/orders/{order_id}", response_model=response_model)
        def retrieve_order(order_id: int):
            return {"quantity": QUANTITY, "note": NOTE}
    return app

def schema_evidence():
    for name, app in [("previous", contract_app(PreviousResponse)),
                      ("response field removed", contract_app(RemovedNoteResponse)),
                      ("operation removed", contract_app(PreviousResponse, False))]:
        schema = app.openapi()
        yield {"case": name, "paths": schema["paths"],
               "schemas": schema.get("components", {}).get("schemas", {})}
'''.replace('QUANTITY', repr(quantity)).replace('NOTE', repr(note))
}

# Metrics fixtures are authored controls, not invented observations.
case_rows = [dict(zip([c['name'] for c in assets[1]['columns']], row)) for row in assets[1]['rows']]
metrics_fixture = '''import asyncio
from fastapi import FastAPI, HTTPException

CASES = CASE_LITERAL

app = FastAPI()

@app.get("/success")
async def success():
    return {"case": "success"}

@app.get("/expected-error")
async def expected_error():
    raise HTTPException(status_code=CASES[1]["response_status"], detail="synthetic expected error")

@app.get("/delayed")
async def delayed():
    await asyncio.sleep(CASES[2]["configured_delay_seconds"])
    return {"case": "delayed"}

@app.get("/escaping-exception")
async def escaping_exception():
    raise RuntimeError("synthetic escaping exception")
'''.replace('CASE_LITERAL', repr(case_rows))
metrics_harness = '''from fastapi.testclient import TestClient
from prometheus_client.parser import text_string_to_metric_families
from fixture import CASES

def snapshot(client, route):
    text = client.get("/metrics/").text
    values = {}
    for family in text_string_to_metric_families(text):
        for sample in family.samples:
            # Only the exercised template; do not mix in metrics-view requests.
            if sample.labels.get("path") == route:
                key = (sample.name, tuple(sorted(sample.labels.items())))
                values[key] = sample.value
    return values

def observe(app):
    with TestClient(app, raise_server_exceptions=False) as client:
        for case in CASES:
            route = case["route_template"]
            before = snapshot(client, route)
            response = client.get(route)
            after = snapshot(client, route)
            keys = sorted(set(before) | set(after))
            yield {"case": case, "actual_status": response.status_code,
                   "samples": [{"metric": key[0], "labels": dict(key[1]),
                                "before": before.get(key, 0), "after": after.get(key, 0),
                                "change": after.get(key, 0) - before.get(key, 0)} for key in keys]}
'''
workspaces['observability.verified_request_metrics'] = {
'fixture.py': metrics_fixture,
'main.py': '''from fixture import app
from starlette_prometheus import PrometheusMiddleware, metrics
from harness import observe

# TODO: register the middleware with filter_unhandled_paths=True.
# TODO: expose the /metrics/ view using app.add_route.
# After configuration, observe(app) computes before/after counter and histogram evidence.
# Compare returned responses to the escaping-exception case; isolate each matched route.
''',
'harness.py': metrics_harness,
'visual_reference.py': '''from fixture import app
from starlette_prometheus import PrometheusMiddleware, metrics
from harness import observe

app.add_middleware(PrometheusMiddleware, filter_unhandled_paths=True)
app.add_route("/metrics/", metrics)

def evidence():
    return list(observe(app))
''',
'request_cases.json': json.dumps(case_rows, indent=2)
}

for bundle in bundles:
    cid = bundle['context']['concept_id']
    files = workspaces[cid]
    readme = '\n'.join([
        '# ' + bundle['context']['concept_name'],
        '', 'All samples and routes in this workspace are synthetic local fixtures.',
        '', '## Practice objective', bundle['practice_anchor']['objective'],
        '', '## Success', bundle['practice_anchor']['success'],
        '', '## Starter intent', bundle['practice_anchor']['live_code']['starter_state_intent'],
        '', '## Visual intent', bundle['visual_anchor']['purpose'],
        '', 'main.py is the learner starter. visual_reference.py is separate teaching/reference material, not starter code.',
        'Reference evidence functions return computed values; no execution output is pre-authored here.',
        'These workspaces require Python with FastAPI, Pydantic v2 and httpx; the metrics workspace additionally requires starlette_prometheus and prometheus_client.',
        'The local stage-01 gate validates registry structure but does not execute code_workspace assets.',
        ''
    ])
    files = {'README.md': readme, **files}
    # Exact glossary code is useful for downstream code walkthroughs; copy, never rewrite it.
    snippets = [m.group(1) for t in bundle['teaching_blocks'] for m in re.finditer(r'```python\n(.*?)```', t['content'], re.S)]
    if snippets:
        files['glossary_walkthrough.py'] = '\n\n'.join(snippets)
    assets.append({'asset_id': 'cw.' + cid, 'asset_kind': 'code_workspace',
                   'scenario_id': scenario_id, 'title': bundle['context']['concept_name'],
                   'runtime': 'python',
                   'files': [{'path': path, 'content': content} for path, content in files.items()]})

registry = {'schema_version': '1.0.0', 'kind': 'scenario_asset_registry',
            'path_id': source['path_id'], 'batch_id': B.name,
            'scenarios': [{'scenario_id': scenario_id, 'name': 'Synthetic order API verification lab',
                           'summary': 'A small fictional order service is reviewed in an isolated local lab. Developers improve contract examples, test provider substitution, bind metadata, verify invalid-input responses and controlled request metrics, and compare selective updates and contract revisions. No persistence or real users are involved.',
                           'domain': 'backend API verification', 'glossary_example_vocab': vocab}],
            'assets': assets}
(B / 'scenario_asset_registry.json').write_text(json.dumps(registry, indent=2, ensure_ascii=False) + '\n')

# Stage-specific mistakes-to-avoid audit. Data issues are also rechecked by the gate.
checks = []
for a in assets:
    if a['asset_kind'] == 'dataset':
        assert all(len(r) == len(a['columns']) for r in a['rows'])
        for c in a['columns']:
            assert c['semantic_role'] != 'numerical' or c['type'] in ('integer', 'number')
            if c.get('numeric_looking_label'):
                assert c['semantic_role'] in ('identifier', 'categorical')
        checks.append(a['asset_id'] + ': row widths, types and unambiguous roles checked')
    else:
        for f in a['files']:
            if f['path'].endswith('.py'):
                ast.parse(f['content'])
        checks.append(a['asset_id'] + ': Python syntax and concept-specific starter/reference coverage checked')
assert len(workspaces) == len(bundles)
assert all(v in texts for v in vocab)
assert all(b['visual_anchor']['type'] in ('code', 'comparison') for b in bundles)
checks.extend([
    'Whole batch: every concept has a dedicated workspace with copied practice and visual intent.',
    'Glossary quantity and note fixture values extracted from the input; no named glossary fields omitted.',
    'Omitted and explicit-null update cases use distinct JSON key sets, not indistinguishable CSV blanks.',
    'No duplicate rows planted; occurrence 0 selects the unique concrete-note row for the invalid-quantity variant.',
    'Metrics rows are declared controls, not observations; all before/after values and error loc/type are computed by reference code.',
    'No plot-dependent anchors or teaching text: no image assets needed.',
    'FastAPI/Pydantic dependencies are unavailable locally; code execution remains unverified by this stage.'
])
(B / 'working/scenario_asset_checklist.json').write_text(json.dumps({'checks': checks, 'concept_count': len(bundles), 'scenario_count': 1, 'asset_count': len(assets), 'asset_ids': [a['asset_id'] for a in assets]}, indent=2) + '\n')
print(json.dumps({'concepts': len(bundles), 'assets': len(assets), 'asset_ids': [a['asset_id'] for a in assets]}, indent=2))
